# Install or update GPT Image Skill

For the coding agent carrying out the user's request. Use this guide for both a
first install and an update. Run the commands, inspect the results, and report
what is available. Keep the user's existing installation scope and API settings.

## 1. Identify the existing installation

Check the current runtime's plugin/skill list, `command -v gpt-image`, and, if uv is
available, `uv tool list`. Inspect only the relevant skill folders and installer
records. Do not print environment variables, API keys, or credential files.

- Claude Code plugin `gpt-image@wuyoscar-skills`: use the Claude update below.
- Skills managed by `skills`: keep their project or global scope.
- Codex native plugin: use the native plugin instructions in
  [install and update](install-update.md#codex-native-plugin).
- A standalone CLI managed by uv: update it separately if present.
- Hand-copied or locally edited files: preserve them. Use their original installer
  or a clean linked checkout; do not overwrite them to force an update.

## 2. Update an existing installation

Run only the commands matching the installations found above:

```bash
# Claude Code plugin
claude plugin update gpt-image@wuyoscar-skills

# Project-local skills installed by skills
npx --yes skills@latest update gpt-image get-prompt-from-image --project

# Standalone CLI installed from this repository by uv
uv tool upgrade gpt-image-cli
```

For skills originally installed globally, replace `--project` with `--global`.
Do not update unrelated skills. A plugin normally includes the CLI source; a
copied skill can delegate to an independently installed CLI, which may also need
updating. Use [the installation guide](install-update.md) for other sources.

## 3. First install

Use the user's current runtime. For Claude Code, install the plugin at project
scope unless the user requested a global installation:

```bash
claude plugin marketplace add wuyoscar/GPT-Image2-Skill
claude plugin install gpt-image@wuyoscar-skills --scope project
```

For Codex, install the two skills into the current project:

```bash
npx --yes skills@latest add wuyoscar/GPT-Image2-Skill --skill gpt-image get-prompt-from-image --agent codex --copy
```

The skills installer requires Node.js 22.20 or later. Other supported runtimes can
replace `codex` with their agent name. If the user only wants the CLI, or the skill
needs a backend, use an existing uv installation to run it without a global install:

```bash
uvx --refresh --from git+https://github.com/wuyoscar/GPT-Image2-Skill gpt-image --help
```

If a required package manager is absent, explain the missing dependency and use
the user's approved setup method. Do not silently switch to a global install.

## 4. Verify and report

Confirm that the intended plugin or skill is listed in the selected scope. For
an installed CLI, run `gpt-image --version`, `gpt-image --help`, and
`gpt-image animate --help`. For a plugin's bundled CLI, run the same flags through
`uv run <plugin-root>/skills/gpt-image/scripts/generate.py`; package metadata may
be absent there, so also inspect the plugin manifest version.

Report the installed source, scope, version and checks. Tell the user to start a
new agent session to load updated instructions. Installation does not require an
API key or a paid image request. Existing API-key settings must remain unchanged;
if the user later requests generation, check availability without revealing the
key. Never claim a successful image call based only on installation or `--help`.

The single-guide entry point was inspired by
[Agent Reach's install/update guide](https://github.com/Panniantong/Agent-Reach/blob/main/docs/install.md).
