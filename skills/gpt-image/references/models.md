# GPT Image model selection and API notes

2.6 model IDs and quality options checked against official OpenAI documentation on 2026-11-06. Earlier validation records below retain their original dates. This is the active
API reference for this skill; `openai-cookbook.md` remains an earlier GPT Image 2
cookbook, not a current model catalog. The [2.5 index](openai-image-2.5.md) is
optional; use [migration notes](openai-image-2.5-migration.md) only for comparisons.

## Default and explicit model selection

| Choice | Exact API model ID | Typical use |
|---|---|---|
| 2.6 Flare (default) | `gpt-image-2.6-flare` | Fast generation and editing |
| 2.6 Sunburst | `gpt-image-2.6-sunburst` | Detailed visual work and precise editing |
| 2.5 Flare | `gpt-image-2.5-flare` | Fast, everyday generation |
| 2.5 Sunburst | `gpt-image-2.5-sunburst` | Precise edits and detail-sensitive work |
| Image 2 | `gpt-image-2` | Existing workflows and explicit compatibility requests |

The 2.5 models also have snapshots ending in `-2026-09-08`. There is no documented
bare `gpt-image-2.5` API alias. A name such as “GPT 2.5” is a request to clarify,
not a reason to silently choose a model or send an invented ID.

Use 2.6 Flare when no model is specified or the user requests “latest” / “Image
2.6”. No confirmation is needed for that default. Preserve explicit model IDs
and previously selected models. Unqualified Flare/Sunburst means the 2.6 variant
unless this task already selected another version. Clarify an ambiguous older
family or typo. Always pass the resolved ID explicitly with `--model`.

The CLI default is now `gpt-image-2.6-flare`, replacing `gpt-image-2`. To reproduce
an older workflow, pin its model explicitly. This is a fixed default for this
revision, not a runtime lookup that automatically switches to future releases.
Do not change models after permission, quota, or policy errors.
The CLI disables automatic SDK retries; report errors rather than
silently repeating potentially billable requests.

## Parameters

The 2.5 and 2.6 models use the existing `/v1/images/generations` and `/v1/images/edits`
endpoints. No Responses API migration is needed.

| Parameter | Contract |
|---|---|
| `quality` | 2.5/2.6: `low`, `medium`, `high`, `xhigh`, `max`, `auto`. Image 2: through `high` plus `auto`. CLI default remains `high`. |
| `size` | `auto`, a CLI shortcut, or `WIDTHxHEIGHT`; see limits below. |
| `background` | `auto`, `opaque`, `transparent`. Transparency requires `png` or `webp`, not `jpeg`. |
| `output_format` | `png` (default), `jpeg`, `webp`; 2.6 also `gif` in this CLI. |
| `output_compression` | Integer 0–100 for JPEG/WebP. Do not request compression for PNG. |
| `n` | 1–10; default 1. More images require the user's authorization. |
| `user` | Optional end-user identifier, forwarded unchanged. |
| `moderation` | `auto` or `low`; this CLI exposes it for generation only. Existing CLI default remains `low`. |
| `input_fidelity` | Edits only, omitted by default. See the qualification below. |

For Image 2 and 2.5, both edges must be positive multiples of 16 and at most
3840 pixels, the long/short ratio at most 3:1, and total pixels between 655,360
and 8,294,400 inclusive. Above 2560×1440 is experimental. A size shortcut controls
the actual request; saying “4K” inside a prompt does not set the API dimensions.

For 2.6, the official reference confirms standard sizes `1024x1024`,
`1536x1024` and `1024x1536`. Its custom-size limits are not yet explicitly
listed in the fetched reference; the CLI forwards custom sizes for API-side
validation rather than imposing the older models' limits.

For references, repeat `-i`; for a mask, use `-i` plus `-m`. Validate the actual
input image and mask requirements before a live call. The CLI checks file
existence; that alone does not prove valid format, alpha channel, or size.

### Parameters requiring care

- **Input fidelity:** official documentation explicitly requires omission for
  `gpt-image-2`. The CLI drops it only for Image 2 and its dated snapshots, not
  all names starting with `gpt-image-2`. Explicit `low`/`high` on 2.5/2.6 is passed
  through as an opt-in request, not advertised as verified API support. Prefer
  omission until the chosen model's behavior is confirmed.
- **Edit moderation:** the generic HTTP reference lists it, but the Python
  edit signature used here does not. Do not add it to edits merely because the
  generation method accepts it.
- **Cost:** equal per-token rates do not imply equal per-image cost. Compare
  returned usage for the selected model, size, and quality. Do not promise a
  fixed multiplier per quality level or assume Flare is always cheaper.
- **Output:** save `data[].b64_json`; a successful response is not proof that
  text, identity, or layout is correct. Check the actual image. Do not add
  `response_format` for GPT Image models.

## Validation boundary

2.6 support covers the existing raster generation and edit endpoints, including
explicit model selection and the new CLI default. Offline tests cover request
serialization for both 2.6 variants, default endpoint routing, output saving,
and errors without model fallback. Live checks on 2026-11-09 completed four
Flare generations and four single-reference edits through the repository CLI.
One further generation was rejected at output moderation with no retry.
The saved outputs were visually inspected; see the [sample record](../../../docs/image-2.6-samples.md)
for prompts, settings and limitations. 2.6 Sunburst and the other parameter
combinations remain unverified.

The CLI outputs PNG/JPEG/WebP and native GIF on 2.6. GIF accepts `--frames`
(2-16) and `--frame-duration` (20-2000 ms), defaults to `size=auto`, and rejects
masks and compression. Frame sizes must be multiples of 16; the API checks the
request pixel budget. A native 9-frame Flare GIF edit was inspected on 2026-11-09.
`gpt-image animate` also assembles a sprite sheet locally with no API request.
See [creative workflows](../../../docs/creative-workflows.md) for results and limits.
SVG, complexity control and markup-guided editing are not exposed by this CLI yet.
Historical 2.5 samples are not evidence of 2.6 output quality.

The dependency floor is `openai>=2.32.0`. This 2.6 update was tested with
OpenAI SDK 2.32.0 from the lockfile. The earlier 2.5 update also recorded passing
tests on SDK 3.10.0 (httpx2); that historical result is not a new 2.6 check.
These records do not establish API access or support across all SDK versions.
Run `PYTHONPATH=src python -m unittest discover -s tests -v` for offline tests.
They use in-process HTTP responses, no credentials or paid image generation.

Live checks on 2026-09-09: the model list omitted 2.5 and
`models.retrieve` returned `404 model_not_found`, while the repository CLI
successfully completed three Sunburst generation requests and two reference edits
(HTTP 200, `quality=high`, PNG, one image per request). The initial three runs
did not record credential fingerprints. The two replacement-showcase runs
captured a private fingerprint and passed the verified credential to the CLI.
A separate read-only audit verified the current local credential and account
through `/v1/me` and `/v1/models` (HTTP 200). Model metadata lookup
alone cannot establish generation availability. See the
[samples, exact settings and visual checks](../../../docs/sunburst-samples.md).

These runs cover Sunburst generation and single-reference editing. Flare,
masks, transparency, `xhigh`/`max`, explicit 2.5 input fidelity, and the separate
community templates still require live validation. The poster's knife shadow
points in the wrong direction despite successful generation.

Before release testing, verify the effective key source, endpoint, project
and organization. Keep a non-secret credential fingerprint in private run
evidence; never publish keys or account details. Report blocking failures
before proposing a release. Run a separately authorized small live sample for
each selected model and endpoint. Record exact model, prompt, size, quality,
response/error, and output path. Check transparency, exact text, requested edits and preserved regions.
Do not treat mocked requests, model listings, or another author's examples as
successful local image generation.

## Official sources

- [2.6 Flare model](https://developers.openai.com/api/docs/models/gpt-image-2.6-flare)
- [2.6 Sunburst model](https://developers.openai.com/api/docs/models/gpt-image-2.6-sunburst)

- [Flare model](https://developers.openai.com/api/docs/models/gpt-image-2.5-flare)
- [Sunburst model](https://developers.openai.com/api/docs/models/gpt-image-2.5-sunburst)
- [Image generation guide](https://developers.openai.com/api/docs/guides/image-generation)
- [Python generation reference](https://developers.openai.com/api/reference/python/resources/images/methods/generate)
- [Python edit reference](https://developers.openai.com/api/reference/python/resources/images/methods/edit)
- [Image prompting guide](https://developers.openai.com/api/docs/guides/image-prompting)
