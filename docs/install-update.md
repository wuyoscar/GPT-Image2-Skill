# Install and update

To let a coding agent handle detection, installation and verification, give it
[the agent installation guide](install.md). The commands below explain each route.

Use the updater that matches the original installation. Plugin files, standalone
skills and the Python CLI are separate installs; updating one does not necessarily
update the others. Start a new agent session after updating its instructions.

## Claude Code plugin

Install once inside Claude Code:

```text
/plugin marketplace add wuyoscar/gpt_image_2_skill
/plugin install gpt-image@wuyoscar-skills
```

Update from a terminal:

```bash
claude plugin update gpt-image@wuyoscar-skills
```

For automatic updates, open `/plugin`, select **Marketplaces**, choose
**wuyoscar-skills**, and enable auto-update. Third-party marketplaces do not
have auto-update enabled by default. Use `/reload-plugins` or a new session to
load the updated files. A bare `claude plugin marketplace update` refreshes
listings, not all installed plugins.

Source: [Claude Code plugin management](https://code.claude.com/docs/en/discover-plugins#keep-plugins-updated).

## Codex, OpenClaw and other skill runtimes

The `skills` installer records the remote source so it can pull updates later.
The current installer requires Node.js 22.20 or later. For a project-local Codex install:

```bash
npx --yes skills@latest add wuyoscar/gpt_image_2_skill --skill gpt-image get-prompt-from-image --agent codex --copy
```

Update only these two skills:

```bash
npx --yes skills@latest update gpt-image get-prompt-from-image --project
```

For an installation originally made with `--global`, use `--global` instead of
`--project`. Choose `--agent claude-code`, `openclaw`, or another supported agent
at install time. Plain `npx skills update` can update other installed skills too.
A folder copied by hand or installed by a different tool may not have the source
record that this updater needs; use its original installer or the linked-checkout
method below rather than assuming it is managed by `skills`.

Source: [vercel-labs/skills](https://github.com/vercel-labs/skills).

## Codex native plugin

The repo includes a portable `plugin.json`, a `.codex-plugin/plugin.json`
compatibility manifest and a repo marketplace at `.agents/plugins/marketplace.json`.
On a Codex version with `codex plugin` support:

```bash
codex plugin marketplace add wuyoscar/gpt_image_2_skill --ref main
codex plugin add gpt-image@wuyoscar-skills
```

Refresh that Git marketplace and request installation from the refreshed catalog:

```bash
codex plugin marketplace upgrade wuyoscar-skills && codex plugin add gpt-image@wuyoscar-skills
```

Start a new session and check the installed version in `/plugins`. The refresh
command alone updates the Git marketplace snapshot; it is not proof that a running
session has loaded new plugin files. Older Codex versions can use the `skills`
route above. Repo marketplaces are distinct from the hosted public plugin directory.

Sources: [OpenAI plugin packaging](https://developers.openai.com/plugins/build/plugins)
and the installed `codex plugin`, `add`, and `marketplace upgrade --help` contracts
checked on 2026-11-09. Native install/update commands have not been run against a
user's global configuration for this branch.

## Standalone Python CLI

For a CLI installed from this Git repository with `uv tool install`:

```bash
uv tool upgrade gpt-image-cli
```

Check the installed version with `gpt-image --version`. This updates the Python
CLI, including the local animation tool; it does not update separately copied skill
folders. For a one-off run that refreshes the cached Git source:

```bash
uvx --refresh --from git+https://github.com/wuyoscar/gpt_image_2_skill gpt-image --help
```

## Linked checkout

If the runtime's skills are symlinks to a clean repository checkout, update the
checkout and keep using those same links:

```bash
git -C /path/to/gpt_image_2_skill pull --ff-only
```

Resolve local edits before updating. Do not use a hard reset or overwrite a
hand-edited skill to make an update succeed. Copy-based installs need their files
refreshed separately; pulling an unrelated checkout does not update those copies.

## Release boundary

Remote commands fetch the published repository or package. Local uncommitted
changes do not reach other users. Plugin and CLI versions must match the release;
verify the installed version after publication, not just the updater's exit code.
