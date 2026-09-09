# GPT Image 2.5: references and preservation

Read for reference edits, translation, inpainting and transparent cutouts.
Source check: **2026-09-09**;
[provenance and validation boundary](openai-image-2.5.md#source-boundaries).

## Official examples to consult selectively

- [Translation with layout preservation](https://developers.openai.com/api/docs/guides/image-prompting?model=gpt-image-2.5#translate-while-preserving-layout)
- [Identity and clothing](https://developers.openai.com/api/docs/guides/image-prompting?model=gpt-image-2.5#preserve-identity-and-change-clothing)
- [Combining references](https://developers.openai.com/api/docs/guides/image-prompting?model=gpt-image-2.5#combine-references)
- [Transparent product cutouts](https://developers.openai.com/api/docs/guides/image-prompting?model=gpt-image-2.5#create-a-transparent-product-cutout)
- [Character consistency across turns](https://developers.openai.com/api/docs/guides/image-prompting?model=gpt-image-2.5#keep-a-character-consistent)

Improved preservation is not a pixel lock. Repeated edits can drift; exact
unchanged regions require compositing rather than relying on prompts alone.
[Official migration caution](https://developers.openai.com/api/docs/guides/image-prompting?model=gpt-image-2.5#migrate-an-existing-workflow)

## Local workflow using the existing CLI

1. Inspect the actual inputs. Assign each a role: base scene, identity, garment,
   style or inserted object. Keep this order consistent with repeated `-i` flags.
2. Separate the requested change from invariants; do not turn a small edit into a
   restyle. Consult [craft.md](craft.md) section 13 only if this needs clarification.
3. Keep the selected model explicit. Use [models.md](models.md#parameters) for
   API settings; do not infer that 2.5 requires `--input-fidelity high`.
4. Compare the changed region and the rest of the image. For another authorized
   edit, pass the actual approved output through `-i`; the CLI does not retain
   a conversation or attach an image merely because its filename is in the prompt.

| Task | Inspect before accepting |
|---|---|
| Translation | Approved replacement copy, untranslated remnants, original layout and logos |
| Try-on / identity edit | Face, expression, pose, garment details and plausible body geometry |
| Multi-reference composition | Correct source for each inserted element, scale, perspective and lighting |
| Cutout | Product outline/labels, edge halos, hair/glass/shadows and real alpha transparency |
| Multi-step edit | Current requested change plus accumulated drift from the original invariants |

## Masks and transparent output

A mask is edit guidance, not a guaranteed hard pixel boundary. With multiple
inputs it applies to the first image. Match mask dimensions to that image and
check its alpha channel; use `-i` plus `-m`. See the
[official mask requirements](https://developers.openai.com/api/docs/guides/image-generation#edit-an-image-using-a-mask)
for input constraints.

For cutouts, use `--background transparent --format png` (or WebP), not JPEG.
Inspect the decoded alpha channel; a painted checkerboard is not transparency.
The prompt's preservation list alone does not establish that anything was
preserved. If the job requires exact untouched pixels, explain the need for a
separate compositing step; do not claim the generative edit supplies that guarantee.

For a reusable change-only prompt, read **Single-change preservation edit** in
[community templates](templates-gpt-image-2.5.md). API access and local output
validation remain governed by [models.md](models.md#validation-boundary).
