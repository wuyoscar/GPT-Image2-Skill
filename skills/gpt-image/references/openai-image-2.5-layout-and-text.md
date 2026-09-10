# GPT Image 2.5: layout and exact text

Read for posters, UI previews, educational diagrams and multi-panel images.
Source check: **2026-09-09**;
[provenance and validation boundary](openai-image-2.5.md#source-boundaries).

## Official examples to consult selectively

- [Exact text](https://developers.openai.com/api/docs/guides/image-prompting?model=gpt-image-2.5#render-exact-text)
- [Interface previews](https://developers.openai.com/api/docs/guides/image-prompting?model=gpt-image-2.5#create-an-interface-preview)
- [Scientific and educational visuals](https://developers.openai.com/api/docs/guides/image-prompting?model=gpt-image-2.5#create-scientific-and-educational-visuals)
- [Slides, diagrams and charts](https://developers.openai.com/api/docs/guides/image-prompting?model=gpt-image-2.5#build-slides-diagrams-and-charts)
- [Comic strips](https://developers.openai.com/api/docs/guides/image-prompting?model=gpt-image-2.5#turn-a-story-into-a-comic-strip)

Treat these as task examples, not guarantees of spelling or factual accuracy.
Do not infer that all text-heavy tasks require the highest quality setting.

## Local brief-to-QA checklist

Use the checklist below first. If a specific gap remains, consult only the relevant
[craft.md](craft.md) section (1–7, 11 or 16); these are shared techniques, not 2.5 syntax.

| Task | Freeze in the brief | Acceptance check |
|---|---|---|
| Poster | Exact approved strings, text block positions, hierarchy, margins | Every character, repeated/missing copy, clipping and reading order |
| UI preview | Screen count, layout regions, component names, state and data | Labels, alignment, plausible controls; image output is not working UI |
| Diagram/chart | Supplied facts/data, nodes, directed edges, axes, units and legend | Relations and values against the brief, not just visual attractiveness |
| Comic/panel sheet | Grid dimensions, panel order, identity anchors and per-panel action | Panel count, sequence, consistent character/outfit and no unwanted duplicates |

Keep required copy verbatim and distinguish it from explanatory instructions.
Do not invent missing data, captions or citations. An attractive scientific
visual still needs subject-matter checking; rendering does not validate it.

For an event-poster starting point, consult **Typography-led event poster** in
[community templates](templates-gpt-image-2.5.md). Its older source image is not
evidence of 2.5 reproduction. A reference-based pose sheet also needs the
[editing](openai-image-2.5-editing.md) attachment and preservation checks.

## Refinement decision

Compare the output against the frozen brief at readable zoom. Name the failed
string, region or relation before suggesting one focused correction. If the
user authorizes another call, keep the chosen model and approved copy unless
they explicitly agree to change them. For translation of an existing design,
start with the editing slice rather than regenerating a new layout.
