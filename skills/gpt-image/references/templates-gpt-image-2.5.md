# GPT Image 2.5 Prompt Templates

Four original adaptations of Reddit prompting examples, researched on **2026-09-09**. These are reusable templates, not numbered Gallery Atlas entries or verified new image examples.

## Before generation

- Resolve the model using the Skill rules, separately from the image prompt: do not ask again for an explicit choice, and explain then proceed when the user delegates. Otherwise ask once and offer `gpt-image-2.5-flare`, `gpt-image-2.5-sunburst`, and `gpt-image-2` when legacy output is wanted. An ambiguous name such as "GPT 2.5" does not select a variant.
- The settings below are proposed starting points, not an automatic selection or measured quality ranking. Use the user's confirmed model and settings; do not silently switch models or generate a comparison batch.
- Resolve every `[PLACEHOLDER]` from the user's brief before calling the API. Ask about missing essential details; never send clarification questions or unresolved slots as image content.
- Keep API model, size, and quality settings outside the image prompt. Match the prompt's canvas description to the selected size. For reference-based work, attach the actual image; a filename in the prompt is not an attachment.
- **Verification boundary:** the linked Reddit pages and supplied prompts were read. Source model claims are author reports. These four adapted templates have not been locally reproduced on GPT Image 2.5; no generated examples are included. Preservation instructions are requests, not fidelity guarantees.

## Numbered character pose sheet

**Source:** [One 16 panel pose sheet from GPT Image 2.5 was the only reference the video model got](https://www.reddit.com/r/aivideos/comments/1wbgidh/one_16_panel_pose_sheet_from_gpt_image_25_was_the/) — **u/Fun_Walk_4965**, **2026-09-09**. A complete sheet prompt is supplied in the author's comment.

**Source model:** GPT Image 2.5, author self-report; Flare/Sunburst variant unspecified. **Proposed model:** `gpt-image-2.5-flare`, subject to confirmation. **Starting settings:** edit with a character reference, `size=1024x1024`, `quality=medium`.

```text
Using reference image 1 as the character design, create a square
4-by-4 contact sheet showing [ACTION SEQUENCE] in 16 distinct full-body
poses. Read left to right, top to bottom. Number each cell 1-16 in
its upper-left corner. Preserve [IDENTITY FEATURES], [OUTFIT],
[COLORS], and [ACCESSORIES] across every pose. Use a white background
and consistent character scale. Do not crop limbs. Include no text
except the panel numbers.
```

**Visual QA:** count 16 cells and numbers; check identity, accessory placement, garment patterns, anatomy, and pose order. Numbering is the explicit exception to the no-text rule. This produces one image, not an animation.

## Typography-led event poster

**Source:** [PROMPT SHARING - World Cup 2026 Poster](https://www.reddit.com/r/ImagineAiArt/comments/1u0rf7f/prompt_sharing_world_cup_2026_poster/) — **u/lukmanfebrianto**, **2026-06-09**. The post supplies a placeholder template and a filled example.

**Source model:** GPT Image 2 and Nano Banana 2, according to the author; this is an older inspiration, not a GPT Image 2.5 result. **Proposed model:** `gpt-image-2.5-flare`, subject to confirmation. **Starting settings:** generate, `size=1024x1536`, `quality=medium`.

```text
Create a 2:3 portrait editorial poster for [EVENT].
Background: [VENUE AND SETTING]. Main visual: [SUBJECTS OR PRODUCT].
Reserve a clear headline area. Render only these exact text strings:
title "[HEADLINE]"; subtitle "[VENUE AND DATE]"; footer "[CTA]".
Use [PALETTE] and [TYPE STYLE], strong reading hierarchy, generous
margins, and separation between text and imagery. Do not invent
dates, logos, claims, or additional text.
```

**Visual QA:** compare every displayed character with the approved copy; inspect hierarchy, margins, cropping, and subject placement. Verify event facts before generation rather than inheriting the old example's names or dates.

## Natural editorial photograph

**Source:** [How to write better image prompts - the SSCLD framework](https://www.reddit.com/r/VeniceAI/comments/1sxkco1/how_to_write_better_image_prompts_the_sscld/) — **u/JaeSwift**, **2026-04-27**. The post supplies an editorial-portrait prompt and subject/style/composition/lighting/detail guidance; the author does not claim to have invented the framework.

**Source model:** GPT Image 2, according to the author; this is an older inspiration, not a GPT Image 2.5 result. **Proposed model:** `gpt-image-2.5-flare`, subject to confirmation. **Starting settings:** generate, `size=1024x1536`, `quality=medium`.

```text
Create a 2:3 portrait natural editorial photograph of [ADULT SUBJECT]
doing [ACTION] in [LOCATION]. Frame [SHOT TYPE] from [CAMERA POSITION].
Use soft light from [LIGHT DIRECTION], believable contact shadows,
and neutral color. Retain fine skin and material texture, natural
proportions, and a plausible background. Avoid beauty-filter
smoothing, exaggerated saturation, excessive sharpening, and
artificial-looking blur. No text.
```

**Visual QA:** inspect skin, hands, reflections, perspective, and agreement between subject and background lighting. A textual subject description does not establish or preserve a particular person's identity; use an attached reference when that is required.

## Single-change preservation edit

**Source:** [Here's the prompting template and workflow to get amazing images from the latest version of ChatGPT images](https://www.reddit.com/r/promptingmagic/comments/1qqmrw7/heres_the_prompting_template_and_workflow_to_get/) — **u/Beginning-Willow-801**, **2026-01-29**. The post supplies several change-only edit templates.

**Source model:** GPT Image 1.5, explicitly named in the post; "latest" in its title is historical, not a GPT Image 2.5 claim. **Proposed model:** `gpt-image-2.5-sunburst`, subject to confirmation. **Starting settings:** edit with a base image, `size=auto`, `quality=medium`; inspect the returned dimensions rather than assuming they match the input.

```text
Edit reference image 1. Change only [TARGET OBJECT OR REGION]:
[PRECISE REQUESTED CHANGE]. Preserve the subject's identity,
expression, pose, framing, camera viewpoint, lighting, background,
and all existing text unless the requested change requires otherwise.
Maintain the original material texture and image character. Do not
add unrelated objects, crop, or restyle the scene.
```

**Visual QA:** compare the requested region before and after, then inspect everything that should remain unchanged, especially text, identity, texture, framing, and dimensions. Confirm success visually; do not describe a prompt-only constraint as a pixel-level lock.
