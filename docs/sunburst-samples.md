# Sunburst sample runs

Five authorized outputs across two rounds, generated on 2026-09-09 through the repository CLI
with the official Python SDK 2.32.0. All requests used
`gpt-image-2.5-sunburst`, `quality=high`, `n=1` and PNG output. Automatic retries
were disabled. Four runs reuse original gallery prompts; the cafe edit uses
a new cutaway brief with the existing gallery image as its reference.

| Sample | Prompt and attribution | Endpoint | Size | Result |
|---|---|---|---|---|
| [Watch assembly](technical-illustration/meridian8-sunburst.png) | [No. 113, Curated](../skills/gpt-image/references/gallery-technical-illustration.md) | `/v1/images/generations` | `2048x2048` | HTTP 200 |
| [Cafe cutaway](isometric/cafe-cutaway-sunburst.png) | [No. 54, Curated adaptation; reference: EvoLinkAI](../skills/gpt-image/references/gallery-isometric.md) | `/v1/images/edits` | `2048x2048` | HTTP 200 |
| [Thriller poster](typography-posters/saul-bass-sunburst.png) | [No. 35, Curated](../skills/gpt-image/references/gallery-typography-and-posters.md) | `/v1/images/generations` | `768x1024` | HTTP 200 |
| [Oolong product](product-food/aurora-oolong-sunburst.png) | [No. 59, source credited in gallery](../skills/gpt-image/references/gallery-product-and-food.md) | `/v1/images/generations` | `1024x1024` | HTTP 200 |
| [Winter chess edit](edit-endpoint-showcase/chess-winter-sunburst.png) | [No. 101, OpenAI Cookbook](../skills/gpt-image/references/gallery-edit-endpoint-showcase.md) | `/v1/images/edits` | `1536x1024` | HTTP 200 |

The watch and cafe are the current README showcase. The earlier poster,
product and chess outputs remain in the Reference Gallery.

All three generation requests used `moderation=auto`. The cafe edit used
[`isometric-cafe.png`](isometric/isometric-cafe.png); the chess edit used
[`chess-midgame.png`](photography/chess-midgame.png). Each edit had one
reference; mask, input fidelity and edit moderation were omitted. Output PNG
dimensions match the requested dimensions. There were five requests and five
saved images, with no retries or model switches.

## Visual review

- **Watch:** the required headline strings and numbered callouts 01–10 are
  readable. The image separates metal, glass, brass, jewel and leather parts,
  with inset views and a specifications panel. The model supplied additional
  dimensions and specifications; treat them as fictional design details until
  checked. Mechanical geometry and fine dial markings need specialist review.
- **Cafe:** the overall street layout, fountain and cafe/bookstore/bakery
  arrangement follow the reference. All three requested shop names are
  readable, with cutaway interiors, a jazz lounge, spiral staircase, greenhouse
  and wet-street lighting. The image shows two enclosed storeys plus rooftop
  spaces, short of the requested three enclosed storeys. Full circulation and
  architectural feasibility remain outside this visual check.
- **Poster:** the title, tagline and credit names are legible and match the
  prompt. The flat palette, running figure, yellow eye and ink splatter appear.
  The knife-shaped shadow points down-right; the prompt asked it to point up
  into the title. Keep this as a visible limitation of the sample.
- **Product:** the bottle, tea glass, condensation and product name appear.
  The model added advertising copy, including “NO SUGAR”. Treat that copy as
  invented artwork text; replace it with approved claims before commercial use.
- **Edit:** snowfall, snow cover and cold lighting appear. Visual comparison
  shows the board framing and visible piece arrangement retained. Chess legality and
  pixel-exact preservation remain outside this visual review.

## Metadata lookup and generation gave different results

The initial `models.list` check omitted the 2.5 models and
`models.retrieve("gpt-image-2.5-sunburst")` returned `404 model_not_found`.
The subsequent image requests above succeeded. The initial metadata result
was insufficient grounds to stop the authorized generation test.

OpenAI documents the [Sunburst model ID](https://developers.openai.com/api/docs/models/gpt-image-2.5-sunburst)
and separates [model metadata permissions from image-request permissions](https://developers.openai.com/api/docs/guides/rbac).
The initial three sample requests did not record credential fingerprints.
Their exact key identity was therefore not captured. A later audit verified the current
local credential, its file source and account through `/v1/me` and
`/v1/models` (HTTP 200). Credential fingerprints and account details are kept
in private evidence, outside this repository. The two replacement-showcase
requests captured the selected key fingerprint before invoking the unchanged
CLI with that credential in its child-process environment. The original metadata error
remains unresolved. Verify credentials and request context first, then use
the actual image endpoint response to diagnose a generation failure.

## Validation scope

The offline suite includes 13 request/CLI tests and five credential-source
tests. The latter exercise process, working-directory and home-file
precedence, missing/empty keys and SDK key forwarding with temporary fake
credentials. Run the suite on SDK 2.32.0 and 3.10.0 before release.
These five live runs cover Sunburst generation and single-reference editing.
Flare, masks, transparency, `xhigh`/`max`, explicit input fidelity and the
separate community templates still need their own live checks. The results apply
to these five prompts and settings.
