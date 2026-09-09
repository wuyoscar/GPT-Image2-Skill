# GPT Image 2.5: generation

Read for new photos, illustrations or product scenes. For existing-image changes,
use [editing](openai-image-2.5-editing.md) instead. Source check: **2026-09-09**;
[provenance and validation boundary](openai-image-2.5.md#source-boundaries).

## Official examples to consult selectively

- [Style and lighting](https://developers.openai.com/api/docs/guides/image-prompting?model=gpt-image-2.5#control-style-and-lighting)
- [Historical and real-world context](https://developers.openai.com/api/docs/guides/image-prompting?model=gpt-image-2.5#use-historical-and-real-world-context)
- [Reusable logos](https://developers.openai.com/api/docs/guides/image-prompting?model=gpt-image-2.5#design-a-reusable-logo)

Open only the matching example, not the whole guide. Camera specifications are
appearance cues, not exact physical simulation. The examples do not establish
which variant will win on the user's brief.

## Local workflow using the existing gallery and craft

These are repo application notes, not locally measured 2.5 performance claims.
Start from the user's brief; consult a gallery case only for missing inspiration.
Do not append every possible quality adjective.

| Deliverable | Resolve before generation | Inspect in the actual output |
|---|---|---|
| Natural photograph | Subject/action, framing, light direction, texture and retouching limits | Skin, hands, contact shadows, reflections and background perspective |
| Product scene | Product features, placement, materials, scene palette, required label copy | Geometry, label spelling, reflections and contact with the surface |
| Illustration | Medium, shape language, composition, palette and intended use | Consistent medium, silhouette readability, unwanted photorealism |
| Logo concept | Approved name, symbol, use size and background | Spelling and small-size legibility; a raster concept is not editable vector artwork |

If a capture/material question remains, consult the relevant section (8, 10 or 12)
of [craft.md](craft.md), not the full file. For type-led deliverables, switch to
[layout and text](openai-image-2.5-layout-and-text.md). If a reusable portrait
starting point is needed, see the **Natural editorial photograph** section of
[community templates](templates-gpt-image-2.5.md), retaining its source label.

## Before calling the CLI

- Resolve factual details from the brief; do not inherit dates or claims from a
  historical gallery example.
- Use the confirmed model and settings. Description words such as “4K” do not
  set API dimensions; check [models.md](models.md#parameters).
- Do not add a reference-identity promise to text-only generation. Attach the
  relevant input and follow the editing slice when identity must be preserved.
- State the failed visual requirement before proposing a paid refinement;
  request permission rather than automatically increasing quality or switching models.
