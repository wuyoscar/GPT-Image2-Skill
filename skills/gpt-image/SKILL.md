---
name: gpt-image
description: "Generate or edit images with GPT Image 2 or 2.5 through the packaged CLI and Reference Gallery. Use for image requests including imprecise 'GPT 2.5' model names, posters, typography, reference edits, and inpainting; resolve the model choice before generation."
compatibility: "Requires Python 3.11+ and either `gpt-image`, `uv`, or `uvx`. CLI/API calls read `OPENAI_API_KEY` for OpenAI, or `ATLASCLOUD_API_KEY` / `ATLAS_CLOUD_API_KEY` for the optional Atlas Cloud text-to-image provider, and may incur API charges."
metadata: {"openclaw":{"requires":{"anyBins":["gpt-image","uv","uvx"]},"primaryEnv":"OPENAI_API_KEY","homepage":"https://github.com/wuyoscar/gpt_image_2_skill"}}
---

# gpt-image

Agent runbook for GPT Image 2 / 2.5 generation/editing. Use the prompt library + packaged CLI. Do not reimplement image API code.

## Operating loop

1. **Classify request and resolve model**: `generate`, `edit`, `inpaint`, or `multi-reference`; identify asset type, exact text, aspect ratio, references, safety constraints, and budget/quality. Apply the model-choice rules below before any API call.
2. **Choose the reference path**: Image 2 keeps the gallery-first workflow below. For 2.5, a precise brief needs no reference loading; otherwise choose one short task slice.
3. **Refine only as needed**: preserve the brief. Add a specific gallery case, craft section or template only to fill a concrete gap; do not load them as a bundle for 2.5.
4. **Confer when useful**: before costly/ambiguous/high-polish calls, present 1–3 matched directions plus planned size/quality; ask at most one concise question at a time. Skip long discussion for precise “generate now” requests with a resolved model.
5. **Preflight, no side effects**: use existing CLI/skill if present. Check command availability (`command -v gpt-image`), installed tool lists when the tool manager exists, or the runtime’s own skill registry when available. Do not assume a local home path in cloud/hosted runtimes.
6. **No blind setup**: do not reinstall, overwrite skill folders, create/modify `.env`, or write API keys unless the user explicitly requested setup. Global/shared installs are opt-in only.
7. **Execute via CLI only**: call `gpt-image` or `scripts/generate.py` with an explicit `--model`. Do not create a new `generate.py`, SDK wrapper, or ad-hoc script for normal image requests.
8. **Report**: output file path(s), key flags, and one concise refinement suggestion if useful.

Fast path: confirmed 2.5 model + precise prompt + “generate now” → preflight and CLI, without a mandatory reference/craft pass. Do not reconfirm an exact valid model.

## Model choice and prompt adaptation

| Choice | API model ID | Suggested use |
|---|---|---|
| Flare | `gpt-image-2.5-flare` | Fast general generation and drafts |
| Sunburst | `gpt-image-2.5-sunburst` | Precise reference edits and detailed control |
| Image 2 | `gpt-image-2` | Existing Image 2 workflows and compatibility |

- If the model is absent, ambiguous (such as “GPT 2.5”), or misspelled, ask one clear question offering **Flare, Sunburst, and Image 2** with these trade-offs, then wait. For a typo, suggest the likely intended choice without silently correcting it. Do not treat `gpt-image-2.5` as an API model ID.
- Use an exact supported model ID, an unambiguous choice from this menu, or the user's already confirmed choice for the current task without asking again. If the user explicitly says “you choose,” explain the pick briefly and proceed; consider their task and budget rather than always selecting the most expensive settings.
- Always pass the chosen ID through `--model`. The CLI retains `gpt-image-2` as its backward-compatible default, but that default is not a substitute for the agent resolving the user's choice.
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

## Key and cost rules

- CLI reads `OPENAI_API_KEY` from process env, then `.env`, then `~/.env` without overriding existing env; successful API calls may bill the user's OpenAI account.
- Optional `--provider atlascloud` reads `ATLASCLOUD_API_KEY` or `ATLAS_CLOUD_API_KEY` and uses Atlas Cloud's async text-to-image API.
- If host/runtime has native platform-managed image generation and the user wants that path, use the host tool instead of this CLI.
- If `OPENAI_API_KEY` is unset, report missing key or use host-native generation when requested; do not write secrets.
- If user wants to avoid local-key use, respect `unset OPENAI_API_KEY`; if a key exists in `.env`/`~/.env`, tell them to remove/rename it for the session rather than working around it.
- Never print secret values.

## Flags

| Flag | Values | Use |
|---|---|---|
| `-p, --prompt` | string | Required prompt/edit instruction |
| `--provider` | `openai`, `atlascloud` | Provider; `atlascloud` currently supports text-to-image generation |
| `-f, --file` | path | Output path; auto-named if omitted |
| `-i, --image` | repeatable path | Use edits endpoint; supports multiple references |
| `-m, --mask` | PNG path | Inpaint with alpha mask; requires `-i` |
| `--model` | `gpt-image-2`, `gpt-image-2.5-flare`, `gpt-image-2.5-sunburst` | Agent must pass the resolved choice explicitly; with `--provider atlascloud` the default maps to `openai/gpt-image-2/text-to-image` |
| `--size` | `1k`, `2k`, `4k`, `portrait`, `landscape`, `square`, `wide`, `tall`, or literal | Canvas size |
| `--quality` | `low`, `medium`, `high`, `auto`; 2.5 also `xhigh`, `max` | Cost/quality dial; check model-specific limits |
| `-n, --n` | integer | Number of images |
| `--background` | `auto`, `opaque`; 2.5 also `transparent` | Transparency requires PNG or WebP, not JPEG |
| `--input-fidelity` | `low`, `high`; omitted by default | Edit-only; explicit 2.5 values are forwarded to the API, not assumed supported |
| `--moderation` | `auto`, `low` | Generation moderation setting |
| `--format` | `png`, `jpeg`, `webp` | Output encoding |
| `--compression` | `0-100` | JPEG/WebP compression |
| `--user` | string | Optional end-user identifier |

Quality starting points (not guarantees; keep the user's agreed setting). For 2.5, these take precedence over fixed quality advice in older craft references:
- `low`: cheap drafts and broad exploration; multiple variants require user authorization.
- `medium`: normal exploration, style probing, balanced cost.
- `high`: CLI default and a candidate for final assets, dense text, diagrams and UI. On 2.5, evaluate against the task requirements; do not assume `medium` fails or a higher setting always wins.
- `xhigh` / `max`: 2.5-only options for higher-quality work; discuss the cost trade-off before increasing an already agreed quality. Do not use them automatically for budget-conscious requests.

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
| Atlas Cloud text-to-image | `--provider atlascloud`, no `-i` | `/api/v1/model/generateImage` + prediction polling |
| Reference edit | one or more `-i` | `/v1/images/edits` |
| Inpaint | `-i` + `-m` | `/v1/images/edits` with mask |

Surface API errors verbatim enough for debugging; exit codes: `0` success, `1` API/refusal, `2` bad args/missing key.

## Reference loading

- **Image 2**: open `references/gallery.md`, then one matching `references/gallery-*.md` category and its actual prompt text. Read only relevant sections of `references/craft.md` or the historical `references/openai-cookbook.md` when needed.
- **Image 2.5**: no mandatory references for a precise brief. If guidance is needed, choose **one** directly: `references/openai-image-2.5-generation.md` (photo/product/illustration), `references/openai-image-2.5-layout-and-text.md` (text/UI/diagrams/panels), or `references/openai-image-2.5-editing.md` (references/masks/translation).
- **Other questions**: `references/openai-image-2.5.md` is an optional index; `references/openai-image-2.5-migration.md` covers migration/comparison; `references/models.md` owns current API parameters and validation status.
- **Extra inspiration only**: gallery cases, a targeted craft section, or `references/templates-gpt-image-2.5.md` (community adaptations, not verified outputs). Do not preload them or the old Cookbook for 2.5.

Load the smallest useful slice, not both model routes. Add a second task slice only for a genuine hybrid. Historical examples do not override current API notes or the user's model/settings.

## Verification

- Before API call: check the resolved model and explicit `--model`, endpoint mode, size, quality, output path, and required reference/mask files. Omit `--input-fidelity` unless explicitly needed; do not assume 2.5 always uses or accepts `high`.
- After CLI call: report path(s) printed by the CLI and surface stderr on failure.
- For edits/inpaints: verify `-i` paths exist; verify `-m` exists when used.

Preserve `Curated` vs `Author + Source` metadata when adapting examples. Add new collected prompts to the Reference Gallery before README promotion.
