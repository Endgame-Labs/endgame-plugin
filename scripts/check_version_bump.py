#!/usr/bin/env python3
"""Require a plugin version bump when a pull request changes runtime files."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ".claude-plugin/plugin.json"
RUNTIME_ROOT_FILES = {MANIFEST, "LICENSE", "mcp/endgame.json"}
RUNTIME_PREFIXES = ("skills/",)
VERSION_RE = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")


def git_output(args: list[str]) -> str:
    return subprocess.check_output(
        ["git", "-C", str(ROOT), *args], text=True
    ).strip()


def git_paths(args: list[str]) -> list[str]:
    output = subprocess.check_output(["git", "-C", str(ROOT), *args])
    return [
        path.decode("utf-8", "surrogateescape")
        for path in output.split(b"\0")
        if path
    ]


def semantic_version(version: str) -> tuple[int, int, int]:
    match = VERSION_RE.fullmatch(version)
    if match is None:
        raise ValueError(f"invalid plugin version {version!r}; expected MAJOR.MINOR.PATCH")
    return tuple(int(part) for part in match.groups())


def manifest_version(revision: str) -> str:
    manifest = json.loads(git_output(["show", f"{revision}:{MANIFEST}"]))
    version = manifest.get("version")
    if not isinstance(version, str) or not version:
        raise ValueError(f"{revision} has no plugin manifest version")
    return version


def runtime_changes(base: str, head: str) -> list[str]:
    # Disabling rename detection exposes both sides of a move. NUL delimiters
    # preserve every valid Git filename, including whitespace and non-ASCII.
    changed = git_paths(["diff", "--no-renames", "--name-only", "-z", base, head])
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

    if semantic_version(head_version) <= semantic_version(base_version):
        print(
            "plugin runtime changed without a greater semantic version in "
            f"{MANIFEST} ({base_version} -> {head_version}): {', '.join(changed)}"
        )
        return 1

    print(f"plugin version check ok: {base_version} -> {head_version}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
