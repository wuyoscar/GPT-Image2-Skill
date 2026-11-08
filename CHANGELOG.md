# Changelog

## v0.3.0 — 2026-11-09

- Default generation and editing to GPT Image 2.6 Flare while preserving explicit Image 2 and 2.5 models.
- Add native GIF generation/edit flags and a local `gpt-image animate` tool for sprite-sheet slicing, GIF assembly and an offline HTML player.
- Add an interactive illustration website, animation examples, and community-inspired 2.6 prompts. The atlas now has 171 entries; older examples and original PNGs remain available.
- Add portable and Codex plugin manifests, source-specific update commands, an agent-readable install/update guide, and `gpt-image --version`.
- Refresh both README layouts and prose while preserving the long gallery and 2.5 showcase.
- Run offline tests, CLI smoke checks and package builds in GitHub Actions on Python 3.11 and 3.13.

- Clarified the GPT Image skill as a gallery-first, CLI-first agent runbook: analyze user prompts, search Reference Gallery/craft files, confer when useful, then invoke the packaged CLI.
- Added safer install and API-key guidance: check existing CLI/skill state first, avoid blind reinstall/overwrite, keep global/shared installs opt-in, and never write secrets unless explicitly requested.
- Updated cross-agent installation wording for Codex, OpenClaw, Claude Code, and manual skill runtimes.

## v0.2.0 — 2026-04-25

This release collects the recent documentation, gallery, skill, and discoverability updates after the initial public release.

### Highlights

- **Full split Reference Gallery Atlas** — expanded the skill references into category-level `gallery-*.md` files so agents can load the relevant prompt slice without filling the context window.
- **README selected showcase refresh** — compacted the README into representative visual panels while keeping the full 162-prompt catalog in the Reference Gallery.
- **New and reorganized gallery material** — added/updated examples for research paper figures, scientific education, screen photography, gaming HUDs, events maps, beauty/lifestyle, cinematic references, and more.
- **Codex installation clarity** — clarified that `$skill-installer` is a built-in Codex skill-management helper and added a manual Codex fallback path.
- **Bilingual README navigation** — added visible English / 中文 switching near the README top.
- **SEO and discovery polish** — added natural search terms, expanded package/plugin keywords, GitHub topics, and Star History.

### Merged PRs

- #1 — Sync the full prompt gallery into the skill reference atlas
- #3 — Polish README showcase and sync split gallery atlas
- #4 — Add README language switch
- #5 — Clarify Codex skill installation
- #6 — Improve README SEO and add star history
