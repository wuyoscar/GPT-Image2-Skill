---
name: gpt-image
description: "Generate or edit images through the packaged CLI and Reference Gallery, defaulting to GPT Image 2.6 Flare. Use for posters, typography, reference edits, inpainting, native GIFs, sprite animation, image-led websites, and explicit Image 2/2.5/2.6 requests."
compatibility: "Requires Python 3.11+ and either `gpt-image`, `uv`, or `uvx`. CLI/API calls read `OPENAI_API_KEY` and may incur OpenAI API charges."
metadata: {"openclaw":{"requires":{"anyBins":["gpt-image","uv","uvx"]},"primaryEnv":"OPENAI_API_KEY","homepage":"https://github.com/wuyoscar/gpt_image_2_skill"}}
---

# gpt-image

Agent runbook for GPT Image 2 / 2.5 / 2.6 generation/editing. Use the prompt library + packaged CLI. Do not reimplement image API code.

## Operating loop

1. **Classify request and resolve model**: `generate`, `edit`, `inpaint`, or `multi-reference`; identify asset type, exact text, aspect ratio, references, safety constraints, and budget/quality. Apply the model-choice rules below before any API call.
2. **Choose the reference path**: Image 2 keeps the gallery-first workflow below. For 2.5/2.6, a precise brief needs no reference loading; otherwise choose one short task slice.
3. **Refine only as needed**: preserve the brief. Add a specific gallery case, craft section or template only to fill a concrete gap; do not load them as a bundle for 2.5/2.6.
4. **Confer when useful**: before costly/ambiguous/high-polish calls, present 1–3 matched directions plus planned size/quality; ask at most one concise question at a time. Skip long discussion for precise “generate now” requests with a resolved model.
5. **Preflight, no side effects**: use existing CLI/skill if present. Check command availability (`command -v gpt-image`), installed tool lists when the tool manager exists, or the runtime’s own skill registry when available. Do not assume a local home path in cloud/hosted runtimes.
6. **No blind setup**: do not reinstall, overwrite skill folders, create/modify `.env`, or write API keys unless the user explicitly requested setup. Global/shared installs are opt-in only.
7. **Execute via CLI only**: call `gpt-image` or `scripts/generate.py` with an explicit `--model`. Do not create a new `generate.py`, SDK wrapper, or ad-hoc script for normal image requests.
8. **Report**: output file path(s), key flags, and one concise refinement suggestion if useful.

Fast path: default 2.6 Flare or an explicit 2.5/2.6 model + precise prompt + “generate now” → preflight and CLI, without a mandatory reference/craft pass. Do not reconfirm an exact valid model.

## Model choice and prompt adaptation

| Choice | API model ID | Suggested use |
|---|---|---|
| 2.6 Flare (default) | `gpt-image-2.6-flare` | Fast generation and editing |
| 2.6 Sunburst | `gpt-image-2.6-sunburst` | Detailed visual work and precise editing |
| 2.5 Flare | `gpt-image-2.5-flare` | Fast general generation and drafts |
| 2.5 Sunburst | `gpt-image-2.5-sunburst` | Precise reference edits and detailed control |
| Image 2 | `gpt-image-2` | Existing Image 2 workflows and compatibility |

- With no model specified, or a request for “latest” / “Image 2.6”, use `gpt-image-2.6-flare` directly without model confirmation. Unqualified “Flare” / “Sunburst” means the 2.6 variant unless an earlier version was already selected for this task.
- Preserve an exact model ID or a previously confirmed choice. If an explicit older family is ambiguous (for example “GPT 2.5”), ask which variant; for a misspelled model, clarify rather than silently replacing it. Bare `gpt-image-2.5` and `gpt-image-2.6` are not API IDs.
- Always pass the resolved ID through `--model`, including the default. The standalone CLI also defaults to `gpt-image-2.6-flare`. Users can pin `--model gpt-image-2` or a 2.5 model to retain earlier behavior.
- Keep model confirmation, cost discussion, and API flags separate from the final image prompt. Use the model-specific reference path below only when it helps the task. Preserve the user's exact text, intended content, reference identity, and edit invariants; obtain confirmation before material prompt changes.
- Generate one image unless the user requested more. Do not silently switch models, change material prompt content, or run multiple model/prompt variants or comparisons. Ask before additional paid variants. For an authorized same-prompt comparison, keep the prompt, size, and quality identical unless the user asks to vary them.
- Consult `references/models.md` when parameter support or validation status needs checking. On an invalid-model, access/403, quota, or policy failure, report the failure and stop; do not switch models or rewrite the prompt to retry automatically.

## CLI resolution

Preferred call order:

```bash
# Existing CLI on PATH
gpt-image --model MODEL_ID -p "PROMPT" [-f OUT] [-i REF...] [-m MASK] [options]

# Installed skill folder; use runtime-provided skill path when available
uv run "$SKILL_DIR/scripts/generate.py" --model MODEL_ID -p "PROMPT" [-f OUT] [-i REF...] [-m MASK] [options]

# Direct transient CLI when the user requested setup/one-off CLI execution
uvx --from git+https://github.com/wuyoscar/gpt_image_2_skill gpt-image --model MODEL_ID -p "PROMPT" [options]
```

`scripts/generate.py` is a launcher: repo-local `src/gpt_image_cli` → installed `gpt-image` → PATH `gpt-image` → transient `uvx`/`uv` fallback.

## Image to animation or website

Match the deliverable, not just the first image:

- **Native GIF**: use `--format gif`, optional `--frames` (2-16) and `--frame-duration` (20-2000 ms). Size defaults to `auto` for GIF. Inspect all frames and actual playback. Do not use masks or compression with GIF.
- **Sprite sheet to GIF**: generate one evenly divided grid with a fixed camera, scale, anchor and explicit cell order, then run `gpt-image animate --sheet sheet.png --columns 4 --rows 2 --duration 160 -f loop.gif --preview player.html`. This local step needs no key and makes no API calls. It slices existing frames; it does not invent motion from a still or fix registration errors. `--ping-pong`, `--margin`, `--gutter` and `--count` handle playback and spacing. Inspect alpha, every cell, loop seam and jitter.
- **Image-led website**: generate visual assets, then build real HTML/CSS/JS around them. Keep controls and readable interface text in HTML. Test clicks, pause/reduced-motion behaviour, mobile layout and asset paths. A screenshot is not a working website.

Read [creative workflows](../../../docs/creative-workflows.md) in a full repo/plugin checkout. In a standalone skill folder, use `references/models.md` and CLI `--help` / `animate --help`; the examples are also at https://github.com/wuyoscar/gpt_image_2_skill/blob/main/docs/creative-workflows.md.

## Key and cost rules

- CLI reads `OPENAI_API_KEY` from process env, then `.env`, then `~/.env` without overriding existing env; successful API calls may bill the user’s OpenAI account.
- If host/runtime has native platform-managed image generation and the user wants that path, use the host tool instead of this CLI.
- If `OPENAI_API_KEY` is unset, report missing key or use host-native generation when requested; do not write secrets.
- If user wants to avoid local-key use, respect `unset OPENAI_API_KEY`; if a key exists in `.env`/`~/.env`, tell them to remove/rename it for the session rather than working around it.
- Never print secret values.

## Flags

| Flag | Values | Use |
|---|---|---|
| `-p, --prompt` | string | Required prompt/edit instruction |
| `-f, --file` | path | Output path; auto-named if omitted |
| `-i, --image` | repeatable path | Use edits endpoint; supports multiple references |
| `-m, --mask` | PNG path | Inpaint with alpha mask; requires `-i` |
| `--model` | Exact ID from the model table | Default 2.6 Flare; agent passes the resolved ID explicitly |
| `--size` | `1k`, `2k`, `4k`, `portrait`, `landscape`, `square`, `wide`, `tall`, or literal | Canvas size |
| `--quality` | `low`, `medium`, `high`, `auto`; 2.5/2.6 also `xhigh`, `max` | Cost/quality dial; check model-specific limits |
| `-n, --n` | integer | Number of images |
| `--background` | `auto`, `opaque`; 2.5/2.6 also `transparent` | Transparency requires PNG or WebP, not JPEG |
| `--input-fidelity` | `low`, `high`; omitted by default | Edit-only; explicit 2.5/2.6 values are forwarded to the API, not assumed supported |
| `--moderation` | `auto`, `low` | Generation moderation setting |
| `--format` | `png`, `jpeg`, `webp`, `gif` | GIF uses 2.6; default remains PNG |
| `--frames` / `--frame-duration` | 2-16 / 20-2000 ms | Native GIF only; API defaults 9 / 200 |
| `--compression` | `0-100` | JPEG/WebP compression |
| `--user` | string | Optional end-user identifier |

Quality starting points (not guarantees; keep the user's agreed setting). For 2.5/2.6, these take precedence over fixed quality advice in older craft references:
- `low`: cheap drafts and broad exploration; multiple variants require user authorization.
- `medium`: normal exploration, style probing, balanced cost.
- `high`: CLI default and a candidate for final assets, dense text, diagrams and UI. On 2.5/2.6, evaluate against the task requirements; do not assume `medium` fails or a higher setting always wins.
- `xhigh` / `max`: 2.5/2.6 options for higher-quality work; discuss the cost trade-off before increasing an already agreed quality. Do not use them automatically for budget-conscious requests.

Size policy:
- default/social square: `1k` / `1024x1024`
- poster/mobile/beauty: `portrait`
- landscape/gameplay/photo: `landscape`
- print/paper figure: `2k`
- widescreen hero: `4k`
- vertical story/banner: `tall`

## Endpoint routing

| Mode | Trigger | Endpoint |
|---|---|---|
| Text-to-image | no `-i` | `/v1/images/generations` |
| Reference edit | one or more `-i` | `/v1/images/edits` |
| Inpaint | `-i` + `-m` | `/v1/images/edits` with mask |

Surface API errors verbatim enough for debugging; exit codes: `0` success, `1` API/refusal, `2` bad args/missing key.

## Reference loading

- **Image 2**: open `references/gallery.md`, then one matching `references/gallery-*.md` category and its actual prompt text. Read only relevant sections of `references/craft.md` or the historical `references/openai-cookbook.md` when needed.
- **Image 2.6**: use `references/models.md` for current compatibility and verification status. For prompt inspiration, reuse a relevant 2.5 task slice below; these are historical guidance, not 2.6-verified examples.
- **Image 2.5**: no mandatory references for a precise brief. If guidance is needed, choose **one** directly: `references/openai-image-2.5-generation.md` (photo/product/illustration), `references/openai-image-2.5-layout-and-text.md` (text/UI/diagrams/panels), or `references/openai-image-2.5-editing.md` (references/masks/translation).
- **Other questions**: `references/openai-image-2.5.md` is an optional index; `references/openai-image-2.5-migration.md` covers migration/comparison; `references/models.md` owns current API parameters and validation status.
- **Extra inspiration only**: gallery cases, a targeted craft section, or `references/templates-gpt-image-2.5.md` (community adaptations, not verified outputs). Do not preload them or the old Cookbook for 2.5/2.6.

Load the smallest useful slice, not both model routes. Add a second task slice only for a genuine hybrid. Historical examples do not override current API notes or the user's model/settings.

## Verification

- Before API call: check the resolved model and explicit `--model`, endpoint mode, size, quality, output path, and required reference/mask files. Omit `--input-fidelity` unless explicitly needed; do not assume 2.5/2.6 always uses or accepts `high`.
- After CLI call: report path(s) printed by the CLI and surface stderr on failure.
- For edits/inpaints: verify `-i` paths exist; verify `-m` exists when used.

Preserve `Curated` vs `Author + Source` metadata when adapting examples. Add new collected prompts to the Reference Gallery before README promotion.
