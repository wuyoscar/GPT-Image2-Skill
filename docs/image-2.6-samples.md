# Image 2.6 community samples

Run date: 2026-11-09 (Australia/Melbourne). The repository CLI used the official
OpenAI endpoint and the project-local credential. No credentials are recorded here.
The first three calls used `gpt-image-2.6-flare`, `n=1`, PNG output, and SDK retries disabled.
Each exited successfully, saved a PNG, and was visually inspected. No model fallback
or regeneration was used. HTTP status and token usage were not separately captured.

## First round

| Output | Source prompt | Mode | Size | Quality |
|---|---|---|---|---|
| [Failed camera roll](photography/failed-camera-roll-26.png) | [@8co28 original](https://x.com/8co28/status/2099164852560539975), [copyable prompt](https://x.com/8co28/status/2099257877231972428) | Reference edit | 864×1536 | high |
| [Engineer share life](architecture-interior/engineer-share-life-26.png) | [@_a5_s_ original](https://x.com/_a5_s_/status/2118282184821784645), [prompt reply](https://x.com/_a5_s_/status/2118282185845174678) | Reference edit | 1152×1536 | high |

The failed camera roll is featured in README; the shared room is reference-only.
Both use the existing [Ling Yuan character sheet](character-design/character-sheet.png),
whose reference prompt is credited to @MANISH1027512 in [No. 31](../skills/gpt-image/references/gallery-character-design.md).
The image itself identifies Ling Yuan as a fictional adult, age 26.

Exact executed prompts, CLI commands, attribution and visual limitations are in
[No. 164](../skills/gpt-image/references/gallery-photography.md) and
[No. 165](../skills/gpt-image/references/gallery-architecture-and-interior.md).
The first preserves the source's short Japanese instruction and adds the adult
reference sentence. The second is an English adaptation, not a full translation.
The first source labels its example Image 2.5; our reproduction uses 2.6.

## Visual checks

- Failed camera roll: nine panels, blocked lens, motion blur, awkward framing,
  spills and rain. Silver hair, glasses and jacket cues recur. The character
  becomes more like a live-action cosplayer; exact facial identity is not established.
- Engineer share life: recognisable hair and glasses, new indoor outfit and pose,
  tool wall, repair equipment and Neo-Shanghai skyline. The second resident is
  not sufficiently clear; do not advertise perfect instruction compliance.
- Smoke test: a 1024×1024, medium-quality raccoon coffee storyboard confirmed the
  generation endpoint. The user rejected the idea as too ordinary for this gallery;
  it stays in local scratch storage and is not included in the numbered atlas.

These runs cover one Flare generation and two single-reference Flare edits.
Sunburst 2.6, masks, transparency, xhigh/max, SVG/GIF, complexity and markup editing
were not tested in these still-image rounds. The later [animation follow-up](creative-workflows.md) adds a native GIF edit, a transparent sprite-sheet generation, local GIF assembly and interactive pages.

## Loading and storage

The existing long README, original images and 2.5 showcase are retained. The first round embedded two
new images. Its measurements below are retained as historical evidence; see the
second-round section for the current showcase selection. Their full-resolution lossless WebP display derivatives
are linked to authoritative PNG originals. Decoded RGBA bytes were compared and
match exactly; no resizing or lossy encoding was used. WebP derivatives are for
display and are not substitutes for the PNG originals' provenance metadata.

| Asset | Original PNG bytes | Display WebP bytes |
|---|---:|---:|
| Failed camera roll | 2,048,891 | 1,270,102 |
| Engineer share life | 2,605,551 | 1,815,988 |
| Total | 4,654,442 | 3,086,090 |

New embedded image bytes: 2.94 MiB, 33.7% less than embedding the two PNGs.
Added image storage including both originals and derivatives: 7.38 MiB.
These are file-size measurements, not a measured browser speedup. The existing
English README referenced 322.16 MiB of local embedded images before this addition;
the Chinese README referenced 327.53 MiB. GitHub caching and image delivery affect
actual transfer and loading time.

## Community research

X originals and author replies were read using the existing browser session.
The failed-photo source screenshot was also opened to check that the short prompt
matched the pictured example. Reddit search was attempted but its adapter returned
HTML instead of JSON; no successful Reddit original read is claimed.

Another promising workflow is [@hAru_mAki_ch's animated desktop cursors](https://x.com/hAru_mAki_ch/status/2119072107196035314),
with an [author tutorial](https://note.com/sunwood_ai_labs/n/na0dbbfa3811f).
The tutorial describes generating cat cursor frame sheets and converting them into
Windows cursor files. The later [animation follow-up](creative-workflows.md)
adapts that workflow into a fire-sword GIF and browser player. An installable
operating-system cursor has not been produced or tested.

## Second round: six community candidates

Run date: 2026-11-09. Six independent prompts were attempted once each through
the same repository CLI with `gpt-image-2.6-flare`, `quality=high`, `n=1`, PNG
output and SDK retries disabled. Five outputs were saved and visually reviewed.
The sixth request was rejected at output moderation; it was not retried,
reworded or switched to another model.

| Candidate | Mode | Result | Placement |
|---|---|---|---|
| [No. 166 · What is in a cyber engineer’s bag?](../skills/gpt-image/references/gallery-gaming.md) | Reference edit | PNG saved; visually reviewed | README + Reference Gallery |
| [No. 167 · Inside the overthinking department](../skills/gpt-image/references/gallery-infographics-and-field-guides.md) | Generation | PNG saved; visually reviewed | README + Reference Gallery |
| [No. 168 · The five-minute fix](../skills/gpt-image/references/gallery-anime-and-manga.md) | Generation | PNG saved; visually reviewed | README + Reference Gallery |
| [No. 169 · Flat-pack dragon assembly](../skills/gpt-image/references/gallery-infographics-and-field-guides.md) | Generation | PNG saved; visually reviewed | README + Reference Gallery |
| [No. 170 · Find Ling Yuan in the night market](../skills/gpt-image/references/gallery-illustration.md) | Reference edit | PNG saved; visually reviewed | Reference Gallery only |
| Villains caught playing a farming game | Generation | API 400 `moderation_blocked`, stage `output`, category `other`; no image | Not collected |

The API did not give a more specific explanation for the rejected output; no
cause is inferred. Its source was the [Reddit flash-photo crossover](https://www.reddit.com/r/ChatGPT/comments/1jskeib/prompt_adherence_is_unreal_prompt_in_description/)
by u/--lily-rose--. The attempted adaptation depicted fictional villains
playing a cosy farming game; no generated image or gallery entry is claimed.

### Review findings

- **What is in a cyber engineer’s bag?:** The output has 24 illustrated inventory cells, short item descriptions and character reactions. The source character cues recur, but HUXING (the company name in the reference) is used like the character name. This is a fictional UI illustration, not a working inventory or a verified item-count system.
- **Inside the overthinking department:** The labelled departments, citation forklift, awkward-handshake cinema, coffee machinery, sleeping staff and ignored deadline alarm are visible. The floor structure is not an exact six-storey building; this is a satirical cutaway, not a validated floor plan.
- **The five-minute fix:** Six panels show the escalating task and the final blue button. Main captions are readable and the character is consistent. The initial button is not visible, so unchanged colour is conveyed by the final joke rather than demonstrated; the requested twelve monitors are not all present.
- **Flat-pack dragon assembly:** The parts list, six numbered stages, spare screw, fire sneeze, eaten hex key, broken sofa and warning are readable. The drawing is a fantasy joke, not mechanically meaningful assembly guidance.
- **Find Ling Yuan in the night market:** The night market contains the six-armed chef, robot queue stopped by a sleeping cat, rooftop plants, chess players, pigeon repair scene and octopus booth. A sufficiently recognisable single instance of the supplied character could not be confirmed. Keep reference-only; do not present it as a solved seek-and-find puzzle.

The night-market picture has strong scene detail, but the requested hidden
character is unconfirmed. It is archived as a limited result, not promoted as
a functioning puzzle. The earlier ordinary shared-room image is also kept in
Reference Gallery only. README now presents five 2.6 images: the failed camera
roll plus four stronger second-round outputs. The pre-existing long gallery
and 2.5 showcase are retained.

### Source verification

This round successfully read Reddit originals through the browser adapter,
including the [30 personal-image concepts](https://www.reddit.com/r/ChatGPT/comments/1w0jh1w/i_started_asking_chatgpt_to_create_images_using/)
by u/Ohsusannamarie and the [impossible furniture manual](https://www.reddit.com/r/ChatGPT/comments/1pd0qeu/from_nuclear_to_summoning_a_dragon_ais_cursed/)
by u/Mary_ry. The [inventory prompt](https://x.com/chachaai_jp/status/2049066868502405257)
by @chachaai_jp was read through X and its source image visually inspected.
The earlier Reddit search failure was specific to that request path, not proof
that all Reddit reading was unavailable.

Personalised concepts use a self-contained fictional persona, not the user's
private history. Exact executed adaptations and source links live in the
matching category files. Original-model labels are preserved when known;
none of these older posts is relabelled as a new 2.6 release demonstration.

### Second-round storage check

All five new WebP derivatives were decoded and compared byte-for-byte in RGBA
against their PNG originals. All match at the original dimensions.

| Image | PNG bytes | Lossless WebP bytes |
|---|---:|---:|
| What is in a cyber engineer’s bag? | 2,641,047 | 1,860,524 |
| Inside the overthinking department | 4,069,694 | 2,813,822 |
| The five-minute fix | 3,352,057 | 2,385,142 |
| Flat-pack dragon assembly | 2,724,459 | 1,812,972 |
| Find Ling Yuan in the night market | 4,185,030 | 2,899,348 |

The four promoted second-round WebPs total 8.46 MiB.
After removing the shared-room preview from README, the net increase over the
first-round README is 6.73 MiB.
The current English and Chinese README local embedded-image inventories are
331.83 MiB and 337.20 MiB respectively.
Second-round added image storage, counting originals and derivatives, is
27.41 MiB.
These are static asset byte totals, not measured network transfer or load times.

The local rendered README panel was checked in Chrome. This is a local layout
check; the branch has not been pushed and GitHub public rendering is unverified.
