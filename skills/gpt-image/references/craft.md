# GPT Image 2 Prompt Craft

Cross-cutting principles distilled from the full 162-prompt Gallery Atlas. Use this file as the prompt-design checklist; use `gallery.md` as the routing index for the split concrete reference/case atlas as `gallery-*.md` files.

## Table of contents

0. Use the Reference Gallery before writing from scratch
1. Exact text goes in quotes
2. Put canvas, aspect ratio, and layout before subject
3. JSON / config-style prompts are a core pattern
4. Use fixed-region schemas for infographics and educational boards
5. Research/data figures need diagram grammar
6. UI prompts should read like product specs
7. Multi-panel boards need consistency constraints
8. Camera and capture context unlock photorealism
9. Scene density beats adjectives
10. Style anchors should be specific and bounded
11. Promotional hierarchy for commercial posters
12. Material, lighting, and palette are separate controls
13. Edit endpoint prompts must preserve invariants
14. Negation is for strong priors
15. Category-specific mini-schemas
16. Dense Chinese and multilingual layouts need extra constraints
17. Attribution and gallery metadata
18. Safety and copyright notes

## 0. Use the Reference Gallery before writing from scratch

For Image 2's gallery-first workflow, open `gallery.md`, then read nearby cases in the matching category. For 2.5, use only the craft section needed; do not restart a gallery search or load the whole checklist.

Fast routing examples:
- Anime/manga or multi-character boards → No. 1–12.
- Product/food commercial render, especially structured config prompts → No. 56–58.
- Brand, poster, typography, dense Chinese copy → No. 33–44, 59–61, 66–73.
- Research, data, technical, scientific figures → No. 75–95, 107–128.
- UI / app / dashboard mockups → No. 102–106.
- Edit endpoint / reference transformations → No. 100–101.

## 1. Exact text goes in quotes

GPT Image 2 renders typography well when literal copy is explicit.

Weak:
> Create a tea poster with the brand name and promo copy.

Strong:
> Design a 3:4 vertical poster. The poster must accurately display the following exact Chinese copy: "山川茶事" / "冷泡系列" / "中杯 16 元" / "大杯 19 元".

Rules:
- Wrap every displayed string in `"…"`.
- Keep user-supplied Chinese verbatim; do not paraphrase.
- Separate text blocks with `/`, bullets, or layout labels.
- For dense text, include title, subtitle, module labels, legend labels, numbers, fine print, and any required axes/tabs.
- If text is only decorative, say so. If it must be readable, say `crisp`, `legible`, `large enough`, and `no garbled characters`.

## 2. Put canvas, aspect ratio, and layout before subject

The strongest gallery prompts allocate space before describing surface detail.

Useful first clauses:
- `Landscape 16:9 academic concept figure…` (No. 75–95).
- `Design a 3:4 vertical poster…` (No. 33–45).
- `Create a square 3×3 grid…` (No. 22, No. 25).
- `A 6-panel film storyboard laid out as a 3×2 grid…` (No. 28).
- `Create one tall manga chapter proof sheet containing 19 numbered miniature pages…` (No. 10).

When structure matters, state the structure before the subject. Otherwise the model spends detail budget on the object and improvises the layout.

## 3. JSON / config-style prompts are a core pattern

Do not omit this. The gallery uses JSON-like structured prompts for premium product and food rendering (No. 57, No. 58). This pattern works when the output has many interacting systems: environment, subject, materials, lighting, particles, motion, and render goals.

When to use:
- Product hero renders with material/lighting precision.
- Food photography with suspended ingredients or motion.
- Complex scenes where you want a controllable schema rather than prose.
- Any prompt that benefits from reusable slots.

Recommended schema:

```text
/* PRODUCT_RENDER_CONFIG: Short Name
   VERSION: 1.0.0
   AESTHETIC: Premium Commercial Photography */
{
  "GLOBAL_SETTINGS": {
    "aspect_ratio": "2:3 vertical",
    "style": "hyper-realistic commercial photography",
    "clarity": "sharp foreground, micro-texture visibility",
    "render_flags": ["8K_UHD", "sharp_foreground", "editorial_finish"]
  },
  "ENVIRONMENT": {
    "background": "warm gradient studio backdrop",
    "lighting": "directional softbox with glossy highlights",
    "atmosphere": ["floating particles", "cinematic bokeh"]
  },
  "CORE_ASSETS": {
    "primary_subject": "hero product",
    "materials": ["brushed metal", "condensation", "paper label"],
    "composition": "diagonal zero-gravity arrangement"
  },
  "MOTION_OR_DETAIL_SYSTEMS": [
    { "object": "ingredient fragments", "state": "suspended mid-air" },
    { "object": "liquid splash", "behavior": "thick glossy arc" }
  ],
  "OUTPUT": {
    "mood": "premium, indulgent, editorial",
    "avoid": ["cheap e-commerce banner", "plastic CGI", "fake brand logos"]
  }
}
```

Craft rules:
- Keys should describe visual subsystems, not implementation internals.
- A short header comment can carry `VERSION:` and `AESTHETIC:`. The version is not for code execution; it makes the prompt feel like a deliberate spec and helps future agents compare variants.
- Values should be concrete visual constraints, not vague praise.
- Arrays are good for visible elements; nested objects are good for materials, physics, lighting, and output goals.
- Use `render_flags` / `quality_flags` for output-level constraints such as `8K_UHD`, `sharp_foreground`, `micro_texture`, `editorial_finish`, or `no_CGI_tell`.
- JSON does not have to be machine-valid if comments help the model, but keep it clean and readable.
- Still include aspect ratio and output mood inside the schema.

## 4. Use fixed-region schemas for infographics and educational boards

Several high-performing prompts are not just descriptions; they are layout contracts. See the museum catalog disassembly infographic (No. 68), field guides (No. 69, No. 74), travel/cooking cards (No. 70, No. 72), and anatomy/science posters (No. 122–127).

Pattern:
1. Name the artifact type: `museum catalog-style Chinese disassembly infographic`, `field guide`, `classroom wall chart`.
2. Define the fixed layout zones: top title, left disassembly, right summary, bottom legend, etc.
3. Specify annotation behavior: lead lines, numbered labels, close-up details, material notes.
4. Specify style boundary: museum board, scientific poster, editorial card — not generic poster / anime / e-commerce.
5. Add exact label text where correctness matters.

This is stronger than saying “make an infographic about X”.

Educational anatomy / science poster pattern:
- Name the subject exactly (`human muscular system`, `periodic table spectral variant`, `geological strata cross-section`).
- Include view constraints where relevant, e.g. `anterior and posterior views` for anatomy.
- Add scale/context notes such as `Adult height reference 175 cm` when the prompt needs scientific believability.
- Require classroom-wall-chart clarity: clean hierarchy, thin labels, legend, muted academic palette, and no gore/excessive realism.

## 5. Research/data figures need diagram grammar

For academic and technical figures, use the language of diagrams, not illustration only.

Include:
- Orientation and venue style: `Landscape 16:9`, `NeurIPS camera-ready`, `conference-paper figure`.
- Structural primitives: columns, zones, stacks, panels, nodes, ribbons, heatmaps, bars, dashed dividers.
- Directed relationships: arrows, residual arcs, feedback loops, dashed attack paths, numbered flow markers.
- Exact labels: module names, axes, legend values, titles, subtitles.
- Visual semantics: color meanings, line styles, thickness ∝ quantity, benign vs attack flows.
- Cleanliness constraints: `large readable labels`, `white background`, `uncluttered`, `publication-grade`.

Examples:
- No. 79 uses left/right encoder-decoder columns with exact block labels.
- No. 81 uses zones, worker nodes, tool registry, memory panels, and trace timeline.
- No. 86 uses Sankey source blocks, processing blocks, final splits, and proportional ribbons.
- No. 95 uses four columns plus benign/injection arrow semantics.

Security / agent-safety figure pattern:
- Show the attack surface as an explicit visual object, e.g. `Attacker-controlled document`, `Public Slack message`, or `Web page`.
- If illustrating prompt injection, quote the payload visibly as a harmless example string such as `<!-- IGNORE previous instructions... -->`, then label it `injected instructions` / `payload`.
- Separate benign flow and attack flow with line semantics: solid slate-gray for benign, dashed terracotta/red for injection path.
- Keep the figure explanatory/defensive; do not turn the payload into operational instructions.

Data visualization mini-schema (No. 107–111):
- Name the chart family first: `small-multiples grid`, `network graph`, `chord diagram`, `treemap`, `geographic choropleth`.
- Specify canvas and structure: `4×3`, node groups, ribbon groups, nested rectangles, map regions.
- Provide exact labels, panel names, legend values, units, and axis labels.
- Explain visual encoding: line = temperature, bars = precipitation, ribbon thickness ∝ flow, color = category/region/value.
- Require consistent scales/alignment across repeated panels.
- Keep styling editorial and readable: white background, generous margins, restrained palette, publication-grade labels.

## 6. UI prompts should read like product specs

The UI/UX examples (No. 102–106) succeed because they specify product context, device frame, information architecture, real copy, and data.

Pattern:
- Fictional product name to avoid real-brand leakage.
- Device/canvas: `1290x2796 smartphone screen`, `16:10 monitor canvas`.
- Palette and component system.
- Top header phrasing: explicitly name the header area and its copy, e.g. `Include a top header with the in-image text "AURAE", "Good morning, Lina", and "Total balance $12,480.36"`.
- Cards, charts, nav, transaction/activity rows.
- Exact values and labels: balances, percentages, axis labels, button names.
- Quality constraints: `crisp typography`, `clean spacing`, `precise icon alignment`, `production-quality mockup`.

Avoid generic UI words alone (`modern`, `clean`, `beautiful`). Add rows, labels, charts, and plausible product data.

## 7. Multi-panel boards need consistency constraints

For grids, proof sheets, storyboards, character sheets, and worldbuilding boards, the key is not “many images”; it is coherence across panels.

Examples:
- No. 5: 16-panel expression grid.
- No. 9: ten-panel character grid.
- No. 10: 19-page manga proof sheet.
- No. 22: 3×3 dark-fantasy worldbuilding set.
- No. 28: 6-panel storyboard with shot/camera metadata.
- No. 31: official character reference sheet.
- No. 107: 4×3 small-multiples data grid with consistent axes.

Rules:
- State the grid/page count exactly: `3×3`, `4×3`, `3×2`, `16-panel`, `19 numbered miniature pages`.
- For data grids, use the exact phrase `small-multiples grid`, specify rows/columns, and require consistent axes/labels across mini-panels.
- Give each panel a role or beat.
- Specify shared art direction, palette, costume motifs, symbols, lighting, and character identity.
- For storyboards, add camera language: WIDE, OTS, CU, low angle, aerial, match cut, pan/tilt/static, duration.
- For character sheets, require front/side/back views, expression variations, parts breakdown, palette, and setting notes.

## 8. Camera and capture context unlock photorealism

The strongest photorealistic prompts name how the image was captured, not just that it is realistic.

Useful phrases:

| Phrase | Effect |
|---|---|
| `RAW, unprocessed, full iPhone camera quality` | Reduces AI polish; adds casual realism. |
| `amateur iPhone photo` | Tourist / spectator feel. |
| `shot from the crowd at a distance` | Real-event perspective. |
| `eye level with a 28 mm lens feel` | Architectural realism. |
| `low three-quarter angle` | Product/vehicle hero composition. |
| `natural morning side light` | Beauty/lifestyle softness. |

Pick one dominant capture frame. Too many camera specs can conflict.

## 9. Scene density beats adjectives

Vague: `a convenience store at night`.

Strong: name concrete objects, surfaces, and situational details: freezer stickers, promotional posters, trash cans, entrance mats, glass reflections, shared bikes, water droplets, phone glow, wet asphalt.

Rule of thumb: include 5–12 concrete nouns for the scene and 2–4 material/lighting constraints. Do not stack empty adjectives like `stunning`, `professional`, `beautiful`, `high quality` without visual anchors.

## 10. Style anchors should be specific and bounded

Name an aesthetic, medium, movement, or production context:
- `MAPPA-style digital 2D animation`, `Studio Pierrot Naruto-Shippuden aesthetic`.
- `New Chinese visual style, light-luxury and restrained`.
- `Swiss grid discipline meets friendly risograph community poster`.
- `gongbi-level architectural detail combined with loose ink atmosphere`.
- `traditional Japanese irezumi tattoo aesthetics`.
- `NeurIPS camera-ready style`.

If using a living studio/IP aesthetic, keep characters original and avoid direct copying where the output is meant for publication.

## 11. Promotional hierarchy for commercial posters

Posters, ads, menus, and campaign visuals should specify hierarchy.

Include:
- Product/event name largest.
- Prefer the wording `Exact readable text:` when every displayed string matters, especially event posters and wayfinding.
- Claim/tagline.
- SKU / variants / modules.
- Prices or dates if relevant.
- CTA or ordering/info module.
- Fine print.
- Distance readability: `legible from a distance`, `clear promotional hierarchy`.
- Add a targeted avoid-line for text failures: `avoid unreadable microtext`, `avoid fake sponsor logos`, `avoid garbled characters`.

This prevents flat banner layouts where every text block has the same weight.

Three-glances test for hero posters:
- First glance: the silhouette/theme is immediately recognizable.
- Second glance: the viewer can read the narrative world, product/event promise, or campaign message.
- Third glance: close inspection reveals texture, small labels, background details, and aftertaste.

Use this for cinematic posters, city posters, fashion/editorial covers, and premium narrative ads where detail must work at multiple viewing distances.

## 12. Material, lighting, and palette are separate controls

Do not compress them into “premium”. Split them:
- Materials: brushed steel, brass, ruby jewel accents, travertine, linen, glass thickness, condensation, rice paper.
- Lighting: softbox, rim light, natural morning side light, neon reflections, warm-copper highlights, cold blue-grey evening.
- Palette: muted teal/rust/bone, cream/warm stone/pale green, slate/amber/teal, indigo/red-orange/cream.

This is especially important for product renders, interiors, architecture, tattoo flash, beauty lifestyle, and technical exploded views.

Brand/label control:
- For original commercial images, say `No visible brand logos` when you do not want fake trademarks.
- If tiny labels are acceptable but should not hallucinate brands, use `no readable fake labels except a tiny generic mark "AM ROUTINE"`.
- For event posters, avoid fake sponsor strips unless the prompt supplies exact sponsor names.

## 13. Edit endpoint prompts must preserve invariants

For `images.edit`, be surgical. State what changes and what must remain unchanged.

Pattern:
> Make it a winter evening with heavy snowfall, snow dusted on the board and pieces, breath vapor in the air, cold blue-grey lighting, chess position still clearly readable.

Rules:
- Name the target transformation first.
- Preserve identity/layout/position/readability explicitly.
- If editing a poster/mockup, preserve original text unless translation/replacement is requested.
- Use `-i` reference images; use masks for localized changes.

Reference-based unlocks:
- `maintain composition and image details consistently`
- `same subject, absolutely consistent in appearance and coloring`
- `in the original positions`
- `change only X; keep everything else the same`

Multi-reference rule:
- Identify each input by index and role: `Image 1: product photo`, `Image 2: style reference`, `Image 3: logo/packaging`.
- Say exactly how references interact: apply style from Image 2 to subject from Image 1; place logo from Image 3 on the package; preserve layout from Image 1.
- Repeat invariants on each iteration if identity, text, geometry, or brand elements must not drift.

## 14. Negation is for strong priors

Use explicit avoid-lines when the model has a likely bad default.

Examples:
- `Avoid anime style, avoid modern cyberpunk, avoid random fake kanji clutter.`
- `Avoid motorcycle aggression, sci-fi excess, fake brand logos, and toy-like proportions.`
- `Avoid generic festival chaos, fake sponsor logos, and unreadable microtext.`
- `No gore, no body horror, no actual person, no photorealistic skin photo.`

Avoid lists should be short and targeted. Too many negatives can dominate the prompt.

## 15. Category-specific mini-schemas

Reusable category formulas from the atlas:

- **Anime/Manga:** style anchor + original characters + action/pose + environment + palette + line/cel-shading direction + safety/IP boundary.
- **Gaming:** game-camera context + HUD elements + playable scene detail + screenshot/monitor realism.
- **Cyberpunk/Retro:** board/grid format + named subcharacters/items + neon material vocabulary + original designs.
- **Brand systems:** logo/wordmark + color palette + type system + packaging/social/touchpoints in one showcase board.
- **Photography:** capture device + time/place + ordinary imperfections + real-world props.
- **Architecture/Interior:** room type + camera/lens + materials + light direction + negative space + realistic shadows.
- **Technical illustration:** exploded/cutaway structure + ordered components + numbered callouts + materials + blueprint/plate style.
- **Tattoo:** tattooable placement + linework/shading/color tradition + negative-space gaps + flash-sheet presentation + no real skin photo. Use exact style tokens where helpful, e.g. `BLACK & GREY`, `FOREARM SLEEVE`, `NEGATIVE SPACE`, `traditional Japanese irezumi`, `dark surrealism`.

## 16. Dense Chinese and multilingual layouts need extra constraints

For Chinese-heavy outputs:
- Say `Simplified Chinese` or `Traditional Chinese` if it matters.
- Provide all copy exactly.
- Specify layout modules and hierarchy.
- Require readable, neat text without garbled characters, typos, English, or pinyin unless desired.
- Use high quality for final assets.

Chinese calligraphy or brush-signage prompts should specify style (`brush style`, `calligraphy-style labels`, `rice-paper texture`) and avoid fake clutter.

## 17. Attribution and gallery metadata

Every split `gallery-*.md` entry preserves either `Curated` metadata for repo-curated/reworked entries or visible `Author + Source` attribution when it came from an outside source. When adapting an outside-source pattern into README/gallery entries, keep attribution in the metadata/footer.

Use `Curated` for repo-created, repo-curated, or substantially reworked prompts/images; keep `Author + Source` for outside-source entries.

## 18. Safety and copyright notes

- Real-person likeness edits often fail at the API moderation layer; surface the API error verbatim.
- Keep adult/fashion prompts clearly adult, tasteful, non-explicit, and non-nude.
- Brand/IP aesthetics appear in the gallery; use original characters/products when creating reusable or public examples.
- For research/security figures, preserve benign framing and avoid operational instructions beyond defensive illustration.
