#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "openai>=2.32.0",
#     "python-dotenv>=1.0",
# ]
# ///
"""Skill launcher for the shared gpt-image CLI.

Resolution order:
1. Repo checkout / full plugin install: import ../../../src/gpt_image_cli/cli.py.
2. Python environment already has gpt_image_cli installed: import it directly.
3. Shell has a gpt-image executable: delegate to it.
4. Final fallback: uvx installs/runs the GitHub CLI package transiently.

This keeps `skills/gpt-image` usable when copied as a standalone skill folder
while preserving one canonical implementation for the installable Python CLI.
"""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

_REPO_URL = "git+https://github.com/wuyoscar/gpt_image_2_skill"


def _import_local_or_installed_main():
    """Return gpt_image_cli.cli.main from repo-local src or installed package."""
    script_path = Path(__file__).resolve()

    # Full plugin/repo layout: <repo>/skills/gpt-image/scripts/generate.py
    # Standalone skill installs do not have this sibling src/ tree, so guard it.
    if len(script_path.parents) > 3:
        repo_src = script_path.parents[3] / "src"
        if (repo_src / "gpt_image_cli" / "cli.py").is_file():
            sys.path.insert(0, str(repo_src))

    try:
        from gpt_image_cli.cli import main  # type: ignore
    except ModuleNotFoundError:
        return None
    return main


def _delegate(command: list[str]) -> int:
    """Run another CLI process with the original argv and return its exit code."""
    completed = subprocess.run(command + sys.argv[1:], check=False)
    return completed.returncode


def main() -> int:
    cli_main = _import_local_or_installed_main()
    if cli_main is not None:
        return int(cli_main() or 0)

    executable = shutil.which("gpt-image")
    if executable:
        return _delegate([executable])

    uvx = shutil.which("uvx") or shutil.which("uv")
    if uvx:
        if Path(uvx).name == "uv":
            return _delegate([uvx, "tool", "run", "--from", _REPO_URL, "gpt-image"])
        return _delegate([uvx, "--from", _REPO_URL, "gpt-image"])

    print(
        "error: could not find the gpt-image CLI backend. Install uv and run this skill "
        "again, or install the CLI first with:\n"
        f"  uv tool install {_REPO_URL}\n"
        "Then retry the same command.",
        file=sys.stderr,
    )
    return 2


if __name__ == "__main__":
    sys.exit(main())
