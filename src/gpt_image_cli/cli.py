#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "openai>=2.32.0",
#     "python-dotenv>=1.0",
# ]
# ///
"""General-purpose CLI for OpenAI GPT Image 2 and 2.5.

Mirrors the two official endpoints from the OpenAI cookbook using the official
`openai` Python SDK:

    client.images.generate(...)   — text → image          (no  -i)
    client.images.edit(...)       — text + image(s) → image (with -i; mask via -m)

Common generation and editing parameters are exposed as flags. Reads OPENAI_API_KEY from
process env, then .env, then ~/.env without overriding existing env. Writes the
returned PNG/JPEG/WebP bytes to disk and prints the output path(s) on stdout.

Exit codes: 0 success, 1 API error, 2 bad args.

Examples:
    # Basic generate, auto filename, 1K square
    gpt-image -p "a cat astronaut on the moon"

    # Named output, portrait 2K, high quality
    gpt-image -p "Chinese tea poster" -f poster.png --size 2k --quality high

    # Edit existing image (colorize, restyle, translate text, etc.)
    gpt-image -p "colorize this manga page" -i page.jpg -f colored.png

    # Multi-reference edit (outfit transfer, pet + brand, etc.)
    gpt-image -p "77 × KFC collab poster" -i cat.png -i kfc_logo.png -f collab.png

    # Alpha-channel inpaint (mask opaque = keep, transparent = regenerate)
    gpt-image -p "replace sky with aurora" -i photo.jpg -m sky_mask.png -f aurora.png

    # Grid of 4, opaque background, webp
    gpt-image -p "isometric chair, minimalist" -n 4 --background opaque --format webp

    # Skill launcher (same implementation, installed skill-folder path)
    uv run "$SKILL_DIR/scripts/generate.py" -p "a cat astronaut on the moon"
"""
from __future__ import annotations

import argparse
import base64
import os
import re
import sys
import urllib.request
from datetime import datetime
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from openai import APIError, OpenAI


def _load_env_chain() -> None:
    """Resolve OPENAI_API_KEY without overriding runtime-provided env.

    Order: process env → ./.env → ~/.env. Existing process env wins so
    hosted agents or explicit shell exports are not replaced by local files.
    """
    load_dotenv(Path.cwd() / ".env", override=False)
    load_dotenv(Path.home() / ".env", override=False)


SIZE_SHORTCUTS: dict[str, str] = {
    "1k": "1024x1024",
    "2k": "2048x2048",
    "4k": "3840x2160",
    "portrait": "1024x1536",
    "landscape": "1536x1024",
    "square": "1024x1024",
    "wide": "2048x1152",
    "tall": "2160x3840",
}

DEFAULT_MODEL = "gpt-image-2"
DEFAULT_SIZE = "1024x1024"
DEFAULT_MODERATION = "low"


def slugify(text: str, max_len: int = 30) -> str:
    s = re.sub(r"[^\w\s-]", "", text.lower()).strip()
    s = re.sub(r"[-\s]+", "-", s)[:max_len]
    return s or "image"


def default_output_path(prompt: str, extension: str) -> Path:
    cwd = Path.cwd()
    target_dir = cwd / "fig" if (cwd / "fig").is_dir() else cwd
    stamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    return target_dir / f"{stamp}-{slugify(prompt)}.{extension}"


def resolve_size(value: str) -> str:
    return SIZE_SHORTCUTS.get(value.lower(), value)


def model_rejects_input_fidelity(model: str) -> bool:
    return re.fullmatch(r"gpt-image-2(?:-\d{4}-\d{2}-\d{2})?", model) is not None


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        prog="gpt-image",
        description="Call OpenAI GPT Image 2/2.5 (generations or edits) via the official openai Python SDK.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument("-p", "--prompt", required=True, help="Text prompt / edit instruction.")
    p.add_argument(
        "-f", "--file",
        help="Output path. Auto-generated as YYYY-MM-DD-HH-MM-SS-<slug>.<ext> if omitted "
             "(written to ./fig/ if that dir exists, else ./).",
    )
    p.add_argument(
        "-i", "--image", action="append", type=Path, default=None,
        help="Reference image path. Repeat flag for multi-reference edits. "
             "Presence of any -i switches endpoint to client.images.edit().",
    )
    p.add_argument(
        "-m", "--mask", type=Path, default=None,
        help="Alpha-channel PNG mask (opaque = preserved, transparent = regenerated). "
             "Edits endpoint only; requires -i.",
    )
    p.add_argument("--model", default=DEFAULT_MODEL, help=f"Model ID: gpt-image-2.5-flare, gpt-image-2.5-sunburst, or {DEFAULT_MODEL} (compatibility default).")
    p.add_argument(
        "--size", default=DEFAULT_SIZE,
        help="Image size. Accepts literals (1024x1024, 1536x1024, 2048x2048, 3840x2160, "
             "any 16px-multiple up to 3840 max edge, 3:1 ratio cap) or shortcuts "
             "(1k, 2k, 4k, portrait, landscape, square, wide, tall). Default 1024x1024.",
    )
    p.add_argument(
        "--quality", default="high", choices=["auto", "low", "medium", "high", "xhigh", "max"],
        help="Rendering fidelity / budget knob. Default high; xhigh/max require GPT Image 2.5. "
             "Use low for cheap drafts, medium for normal exploration, high for final text-heavy or shipping-facing assets.",
    )
    p.add_argument("-n", "--n", type=int, default=1, help="Number of images to return. Default 1.")
    p.add_argument(
        "--background", default=None, choices=["auto", "opaque", "transparent"],
        help="`transparent` requires png or webp. Default API-side auto.",
    )
    p.add_argument(
        "--moderation", default=DEFAULT_MODERATION, choices=["auto", "low"],
        help="Generations only. Default low. Use `auto` if you want the stricter API-side default.",
    )
    p.add_argument(
        "--input-fidelity", dest="input_fidelity", default=None, choices=["low", "high"],
        help="Edits only; omitted by default. Dropped for gpt-image-2; explicit 2.5 values are passed to the API (support unverified).",
    )
    p.add_argument(
        "--format", dest="output_format", default=None,
        choices=["png", "jpeg", "webp"],
        help="Output encoding. Default png.",
    )
    p.add_argument(
        "--compression", dest="output_compression", type=int, default=None,
        help="0-100 compression level for jpeg/webp. Ignored for png.",
    )
    p.add_argument(
        "--user", default=None,
        help="Optional end-user identifier forwarded to OpenAI for abuse tracking.",
    )
    args = p.parse_args()
    image25 = re.fullmatch(r"gpt-image-2\.5-(?:flare|sunburst)(?:-\d{4}-\d{2}-\d{2})?", args.model) is not None
    if args.quality in ("xhigh", "max") and not image25:
        p.error("--quality xhigh/max requires --model gpt-image-2.5-flare or gpt-image-2.5-sunburst")
    if args.background == "transparent" and args.output_format == "jpeg":
        p.error("--background transparent requires --format png or webp")
    if not 1 <= args.n <= 10:
        p.error("--n must be between 1 and 10")
    if args.output_compression is not None and not 0 <= args.output_compression <= 100:
        p.error("--compression must be between 0 and 100")
    if args.mask and not args.image:
        p.error("--mask requires --image (edits endpoint only)")
    size = resolve_size(args.size)
    if (image25 or model_rejects_input_fidelity(args.model)) and size != "auto":
        match = re.fullmatch(r"(\d+)x(\d+)", size)
        if not match:
            p.error("--size must be auto, a size shortcut, or WIDTHxHEIGHT")
        width, height = map(int, match.groups())
        if (min(width, height) <= 0 or max(width, height) > 3840
                or width % 16 or height % 16 or max(width, height) > 3 * min(width, height)
                or not 655360 <= width * height <= 8294400):
            p.error("--size requires 16px multiples, edges <=3840px, aspect ratio <=3:1, and 655360–8294400 pixels")
    return args


def _filter_none(d: dict[str, Any]) -> dict[str, Any]:
    """Drop keys whose value is None — SDK treats missing vs None differently."""
    return {k: v for k, v in d.items() if v is not None}


def call_generate(client: OpenAI, args: argparse.Namespace) -> Any:
    return client.images.generate(**_filter_none({
        "model": args.model,
        "prompt": args.prompt,
        "size": resolve_size(args.size),
        "quality": args.quality,
        "n": args.n,
        "background": args.background,
        "moderation": args.moderation,
        "output_format": args.output_format,
        "output_compression": args.output_compression if args.output_format in ("jpeg", "webp") else None,
        "user": args.user,
    }))


def call_edit(client: OpenAI, args: argparse.Namespace) -> Any:
    for p in args.image:
        if not p.is_file():
            print(f"error: --image not found: {p}", file=sys.stderr)
            sys.exit(2)
    if args.mask and not args.mask.is_file():
        print(f"error: --mask not found: {args.mask}", file=sys.stderr)
        sys.exit(2)

    input_fidelity = args.input_fidelity
    if input_fidelity and model_rejects_input_fidelity(args.model):
        print(
            "note: dropping --input-fidelity because gpt-image-2 rejects that parameter.",
            file=sys.stderr,
        )
        input_fidelity = None

    image_handles = [p.open("rb") for p in args.image]
    mask_handle = args.mask.open("rb") if args.mask else None
    try:
        return client.images.edit(**_filter_none({
            "model": args.model,
            "image": image_handles,
            "mask": mask_handle,
            "prompt": args.prompt,
            "size": resolve_size(args.size),
            "quality": args.quality,
            "n": args.n,
            "background": args.background,
            "input_fidelity": input_fidelity,
            "output_format": args.output_format,
            "output_compression": args.output_compression if args.output_format in ("jpeg", "webp") else None,
            "user": args.user,
        }))
    finally:
        for h in image_handles:
            h.close()
        if mask_handle:
            mask_handle.close()


def write_outputs(data: list[Any], out_path: Path, n: int) -> list[Path]:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    for i, item in enumerate(data):
        b64 = getattr(item, "b64_json", None)
        url = getattr(item, "url", None)
        if b64:
            raw = base64.b64decode(b64)
        elif url:
            with urllib.request.urlopen(url, timeout=300) as r:  # noqa: S310 — OpenAI-owned host
                raw = r.read()
        else:
            print(f"error: response item {i} has neither b64_json nor url", file=sys.stderr)
            sys.exit(1)

        if n == 1:
            target = out_path
        else:
            stem = out_path.with_suffix("")
            target = stem.parent / f"{stem.name}_{i}{out_path.suffix}"
        target.write_bytes(raw)
        written.append(target)
    return written


def main() -> int:
    args = parse_args()

    _load_env_chain()
    if not os.environ.get("OPENAI_API_KEY"):
        print(
            "error: OPENAI_API_KEY not set. Add it to env / .env / ~/.env, or use your host agent's native image tool.",
            file=sys.stderr,
        )
        return 2

    ext = args.output_format or "png"
    out_path = Path(args.file).expanduser().resolve() if args.file else default_output_path(args.prompt, ext)

    client = OpenAI(max_retries=0)  # No hidden retries of potentially billable generation requests.

    try:
        result = call_edit(client, args) if args.image else call_generate(client, args)
    except APIError as e:
        print(f"error: {type(e).__name__}: {e}", file=sys.stderr)
        return 1

    data = result.data or []
    if not data:
        print(f"error: no image data in response: {result}", file=sys.stderr)
        return 1

    for p in write_outputs(data, out_path, args.n):
        print(p)
    return 0


if __name__ == "__main__":
    sys.exit(main())
