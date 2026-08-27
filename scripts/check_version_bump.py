#!/usr/bin/env python3
"""Require a plugin version bump when a pull request changes runtime files."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from package_plugin import PUBLIC_SKILLS


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ".claude-plugin/plugin.json"
RUNTIME_ROOT_FILES = {MANIFEST, "LICENSE", "mcp/endgame.json"}
RUNTIME_PREFIXES = tuple(f"skills/{skill}/" for skill in PUBLIC_SKILLS)


def git_output(args: list[str]) -> str:
    return subprocess.check_output(
        ["git", "-C", str(ROOT), *args], text=True
    ).strip()


def manifest_version(revision: str) -> str:
    manifest = json.loads(git_output(["show", f"{revision}:{MANIFEST}"]))
    version = manifest.get("version")
    if not isinstance(version, str) or not version:
        raise ValueError(f"{revision} has no plugin manifest version")
    return version


def runtime_changes(base: str, head: str) -> list[str]:
    changed = git_output(["diff", "--name-only", base, head]).splitlines()
    return sorted(
        path
        for path in changed
        if path in RUNTIME_ROOT_FILES or path.startswith(RUNTIME_PREFIXES)
    )


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: check_version_bump.py <base-revision> <head-revision>")
        return 2

    base, head = sys.argv[1:]
    try:
        changed = runtime_changes(base, head)
        if not changed:
            print("plugin version check ok: no runtime changes")
            return 0

        base_version = manifest_version(base)
        head_version = manifest_version(head)
    except (json.JSONDecodeError, OSError, subprocess.CalledProcessError, ValueError) as exc:
        print(f"plugin version check error: {exc}")
        return 1

    if base_version == head_version:
        print(
            "plugin runtime changed without updating "
            f"{MANIFEST} version ({base_version}): {', '.join(changed)}"
        )
        return 1

    print(f"plugin version check ok: {base_version} -> {head_version}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
