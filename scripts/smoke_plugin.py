#!/usr/bin/env python3
"""Confirm Claude Code discovers the plugin-provided Endgame MCP server."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / ".claude-plugin" / "plugin.json"
ENDGAME_MCP_URL = "https://app.endgame.io/api/v1/mcp"
EXPECTED_PREFIX = f"plugin:endgame:endgame: {ENDGAME_MCP_URL} (HTTP)"


def plugin_path(use_package: bool) -> Path:
    if not use_package:
        return ROOT

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    return ROOT / "dist" / f"endgame-plugin-{manifest['version']}.zip"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--package",
        action="store_true",
        help="load the packaged ZIP from dist instead of the source directory",
    )
    args = parser.parse_args()

    claude = shutil.which("claude")
    if claude is None:
        print("Claude Code is required for the plugin smoke test")
        return 1

    target = plugin_path(args.package)
    if not target.exists():
        print(f"plugin smoke target does not exist: {target.relative_to(ROOT)}")
        return 1

    try:
        result = subprocess.run(
            [claude, "--plugin-dir", str(target), "mcp", "list"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=60,
            check=False,
        )
    except subprocess.TimeoutExpired:
        print("Claude MCP discovery timed out after 60 seconds")
        return 1

    output = "\n".join([result.stdout, result.stderr])
    match = next(
        (
            line.strip()
            for line in output.splitlines()
            if line.strip().startswith(EXPECTED_PREFIX)
        ),
        None,
    )
    if match is None:
        print("Claude did not discover the plugin-provided Endgame MCP server")
        return 1

    source = "package" if args.package else "source"
    print(f"{source} plugin MCP discovery ok: {match}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
