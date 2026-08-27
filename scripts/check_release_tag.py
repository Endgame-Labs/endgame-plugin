#!/usr/bin/env python3
"""Verify a release tag matches the plugin manifest version."""

from __future__ import annotations

import json
import re
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


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: check_release_tag.py <tag>")
        return 2

    try:
        tag_version = expected_version(sys.argv[1])
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        manifest_version = manifest.get("version")
        if manifest_version != tag_version:
            raise ValueError(
                f"release tag {sys.argv[1]} does not match plugin version "
                f"{manifest_version!r}"
            )
    except (json.JSONDecodeError, OSError, ValueError) as exc:
        print(f"release tag error: {exc}")
        return 1

    print(f"release tag ok: {sys.argv[1]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
