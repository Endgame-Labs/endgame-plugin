#!/usr/bin/env python3
"""Verify a release tag matches the plugin manifest version."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / ".claude-plugin" / "plugin.json"
TAG_RE = re.compile(r"^v(?P<version>0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")


def expected_version(tag: str) -> str:
    match = TAG_RE.fullmatch(tag)
    if match is None:
        raise ValueError("release tag must use vMAJOR.MINOR.PATCH")
    return tag[1:]


def git_output(args: list[str]) -> str:
    return subprocess.check_output(
        ["git", "-C", str(ROOT), *args], text=True, stderr=subprocess.STDOUT
    ).strip()


def verify_release_commit(tag: str) -> str:
    tag_commit = git_output(["rev-parse", "--verify", f"refs/tags/{tag}^{{}}"])
    head_commit = git_output(["rev-parse", "--verify", "HEAD"])
    if tag_commit != head_commit:
        raise ValueError(
            f"checked-out HEAD {head_commit} does not match {tag} commit {tag_commit}"
        )

    result = subprocess.run(
        [
            "git",
            "-C",
            str(ROOT),
            "merge-base",
            "--is-ancestor",
            tag_commit,
            "refs/remotes/origin/main",
        ],
        check=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
        text=True,
    )
    if result.returncode == 1:
        raise ValueError(f"release tag {tag} is not contained in origin/main")
    if result.returncode != 0:
        raise subprocess.CalledProcessError(
            result.returncode, result.args, stderr=result.stderr
        )
    return tag_commit


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: check_release_tag.py <tag>")
        return 2

    try:
        tag = sys.argv[1]
        tag_version = expected_version(tag)
        verify_release_commit(tag)
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        manifest_version = manifest.get("version")
        if manifest_version != tag_version:
            raise ValueError(
                f"release tag {sys.argv[1]} does not match plugin version "
                f"{manifest_version!r}"
            )
    except (json.JSONDecodeError, OSError, subprocess.CalledProcessError, ValueError) as exc:
        print(f"release tag error: {exc}")
        return 1

    print(f"release tag ok: {sys.argv[1]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
