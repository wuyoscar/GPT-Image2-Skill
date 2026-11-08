"""Local sprite-sheet assembly. This module never calls an image API."""
from __future__ import annotations

import argparse
import base64
import html
import io
import json
from pathlib import Path

from PIL import Image, ImageColor


def grid_boxes(size: tuple[int, int], columns: int, rows: int,
               margin: int = 0, gutter: int = 0) -> list[tuple[int, int, int, int]]:
    if min(columns, rows) < 1 or columns * rows > 256 or min(margin, gutter) < 0:
        raise ValueError("Use positive rows/columns, at most 256 cells, and nonnegative margin/gutter")
    width = size[0] - 2 * margin - (columns - 1) * gutter
    height = size[1] - 2 * margin - (rows - 1) * gutter
    if width <= 0 or height <= 0 or width % columns or height % rows:
        raise ValueError("The usable sheet must divide evenly into the requested grid")
    w, h = width // columns, height // rows
    return [(margin + x * (w + gutter), margin + y * (h + gutter),
             margin + x * (w + gutter) + w, margin + y * (h + gutter) + h)
            for y in range(rows) for x in range(columns)]

def playback_order(count: int, ping_pong: bool) -> list[int]:
    order = list(range(count))
    return order + order[-2:0:-1] if ping_pong else order


def save_gif(frames: list[Image.Image], path: Path, duration: int,
             background: str | None) -> None:
    # One palette for the whole sequence avoids per-frame colour shifts.
    rgb = []
    masks = []
    for frame in frames:
        matte = Image.new("RGBA", frame.size, background or "white")
        matte.alpha_composite(frame)
        rgb.append(matte.convert("RGB"))
        masks.append(frame.getchannel("A").point(lambda value: 255 if value < 128 else 0))
    w, h = frames[0].size
    atlas = Image.new("RGB", (w, h * len(frames)))
    for i, frame in enumerate(rgb):
        atlas.paste(frame, (0, i * h))
    palette = atlas.quantize(colors=255, method=Image.Quantize.MEDIANCUT)
    encoded = []
    for frame, mask in zip(rgb, masks):
        out = frame.quantize(palette=palette, dither=Image.Dither.NONE)
        if background is None:
            out.paste(255, mask=mask)
        encoded.append(out)
    options = {"transparency": 255, "background": 255} if background is None else {}
    encoded[0].save(path, format="GIF", save_all=True, append_images=encoded[1:],
                    duration=duration, loop=0, disposal=2, optimize=False, **options)


def preview_html(sheet: Image.Image, boxes: list[tuple[int, int, int, int]],
                 order: list[int], duration: int, title: str, gif: bytes) -> str:
    buf = io.BytesIO()
    sheet.save(buf, format="PNG")
    data = json.dumps({"image": "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode(),
                       "boxes": boxes, "order": order, "duration": duration})
    safe_title = html.escape(title)
    gif_data = base64.b64encode(gif).decode()
    return f'''<!doctype html>
<html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{safe_title}</title>
<style>
:root{{color-scheme:dark}}*{{box-sizing:border-box}}body{{margin:0;background:#11171b;color:#e9eee9;font:16px/1.5 system-ui}}
main{{max-width:1000px;margin:0 auto;padding:40px 24px}}h1{{font-size:clamp(28px,5vw,52px);line-height:1.1;font-weight:600}}
.stage{{background:repeating-conic-gradient(#202a2f 0% 25%,#283239 0% 50%) 50%/24px 24px;border-radius:18px;padding:24px;text-align:center}}
canvas{{display:block;max-width:100%;max-height:65vh;width:auto;height:auto;margin:auto;object-fit:contain}}
.controls{{display:flex;flex-wrap:wrap;align-items:center;gap:14px;padding:20px 0}}button,select,a{{border:1px solid #586267;border-radius:7px;background:#253238;color:inherit;padding:9px 14px;text-decoration:none;font:inherit}}
button{{cursor:pointer}}input{{accent-color:#b9df87}}#scrub{{flex:1;min-width:140px}}small{{color:#a7b5b9}}:focus-visible{{outline:3px solid #b9df87;outline-offset:3px}}
</style><main><small>SPRITE PLAYER</small><h1>{safe_title}</h1>
<div class="stage"><canvas id="stage" aria-label="Animation preview"></canvas></div>
<div class="controls"><button id="play" type="button">Pause</button><input id="scrub" type="range" min="0" value="0" aria-label="Frame">
<output id="position"></output><label>Speed <select id="speed"><option value="0.5">0.5×</option><option value="1" selected>1×</option><option value="2">2×</option></select></label>
<a href="data:image/gif;base64,{gif_data}" download="animation.gif">Download GIF</a></div>
<p><small>Pause to inspect a frame, drag the slider, or change the playback speed. This page works offline.</small></p></main>
<script>
const data={data};
const canvas=document.getElementById('stage'),ctx=canvas.getContext('2d'),scrub=document.getElementById('scrub');
const button=document.getElementById('play'),position=document.getElementById('position'),speed=document.getElementById('speed');
const img=new Image();let index=0,playing=!matchMedia('(prefers-reduced-motion: reduce)').matches,last=0;
const b=data.boxes[0];canvas.width=b[2]-b[0];canvas.height=b[3]-b[1];scrub.max=data.order.length-1;
function draw(){{const r=data.boxes[data.order[index]];ctx.clearRect(0,0,canvas.width,canvas.height);ctx.drawImage(img,r[0],r[1],r[2]-r[0],r[3]-r[1],0,0,canvas.width,canvas.height);scrub.value=index;position.textContent=(index+1)+' / '+data.order.length;button.textContent=playing?'Pause':'Play';}}
function tick(t){{if(playing&&t-last>=data.duration/Number(speed.value)){{index=(index+1)%data.order.length;draw();last=t;}}requestAnimationFrame(tick);}}
button.onclick=()=>{{playing=!playing;last=performance.now();draw();}};
scrub.oninput=()=>{{playing=false;index=Number(scrub.value);draw();}};
img.onload=()=>{{draw();last=performance.now();requestAnimationFrame(tick);}};img.src=data.image;
</script></html>'''


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="gpt-image animate", description="Turn a sprite sheet into a GIF locally. No API key required.")
    p.add_argument("--sheet", type=Path, required=True)
    p.add_argument("--columns", type=int, required=True)
    p.add_argument("--rows", type=int, required=True)
    p.add_argument("--count", type=int, help="Use only the first N cells")
    p.add_argument("--margin", type=int, default=0, help="Outer margin in pixels")
    p.add_argument("--gutter", type=int, default=0, help="Gap between cells in pixels")
    p.add_argument("--duration", type=int, default=160, help="Frame duration in ms, a multiple of 10")
    p.add_argument("--ping-pong", action="store_true", help="Play forward then backward without duplicate endpoints")
    p.add_argument("--background", help="Flatten alpha onto this colour; otherwise preserve binary GIF transparency")
    p.add_argument("-f", "--file", type=Path, required=True)
    p.add_argument("--preview", type=Path, help="Save a self-contained HTML player")
    p.add_argument("--title", default="Animation study")
    p.add_argument("--force", action="store_true", help="Replace existing outputs, never the source sheet")
    args = p.parse_args(argv)
    try:
        if not 20 <= args.duration <= 2000 or args.duration % 10:
            raise ValueError("--duration must be a multiple of 10 between 20 and 2000 ms")
        if args.file.suffix.lower() != ".gif":
            raise ValueError("Output filename must end in .gif")
        if args.background:
            ImageColor.getrgb(args.background)
        targets = [args.file] + ([args.preview] if args.preview else [])
        resolved = [path.resolve() for path in targets]
        if args.sheet.resolve() in resolved or len(set(resolved)) != len(resolved):
            raise ValueError("Input, GIF and preview must be different files")
        for target in targets:
            if target.exists() and not args.force:
                raise ValueError(f"Output already exists: {target}; use --force to replace it")
        with Image.open(args.sheet) as source:
            sheet = source.convert("RGBA")
        boxes = grid_boxes(sheet.size, args.columns, args.rows, args.margin, args.gutter)
        count = args.count if args.count is not None else len(boxes)
        if not 2 <= count <= len(boxes):
            raise ValueError("--count must select at least two cells and fit within the grid")
        boxes = boxes[:count]
        order = playback_order(count, args.ping_pong)
        frames = [sheet.crop(boxes[i]) for i in order]
        for target in targets:
            target.parent.mkdir(parents=True, exist_ok=True)
        save_gif(frames, args.file, args.duration, args.background)
        print(args.file.resolve())
        if args.preview:
            args.preview.write_text(preview_html(sheet, boxes, order, args.duration,
                                                args.title, args.file.read_bytes()), encoding="utf-8")
            print(args.preview.resolve())
        return 0
    except (ValueError, OSError) as exc:
        p.error(str(exc))
