#!/usr/bin/env python3
"""Normalize JSON files that are part of the plugin scaffold."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    ROOT / ".claude-plugin" / "plugin.json",
    ROOT / "mcp" / "endgame.json",
]


def normalized_json(path: Path) -> str:
    data = json.loads(path.read_text(encoding="utf-8"))
    return json.dumps(data, indent=2, ensure_ascii=True) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="fail if files need formatting")
    args = parser.parse_args()

    changed: list[Path] = []
    for path in TARGETS:
        expected = normalized_json(path)
        current = path.read_text(encoding="utf-8")
        if current != expected:
            changed.append(path)
            if not args.check:
                path.write_text(expected, encoding="utf-8")

    if changed and args.check:
        for path in changed:
            print(f"needs formatting: {path.relative_to(ROOT)}")
        return 1

    if changed:
        for path in changed:
            print(f"formatted: {path.relative_to(ROOT)}")
    else:
        print("json format ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
