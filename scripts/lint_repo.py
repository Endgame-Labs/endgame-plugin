#!/usr/bin/env python3
"""Small repository hygiene checks for the plugin scaffold."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKIP_DIRS = {".git", "__pycache__", ".venv", "dist", "tmp"}
TEXT_NAMES = {"Makefile"}
TEXT_SUFFIXES = {
    ".json",
    ".md",
    ".py",
    ".txt",
    ".yml",
    ".yaml",
    ".toml",
    ".gitignore",
    ".editorconfig",
}
PLACEHOLDER_MARKERS = ["[" + "TODO", "TODO" + ":"]
LOCAL_STATE_MARKERS = [
    "/" + "Users/",
    "/var/" + "folders/",
    "/.codex/" + "attachments/",
    "codex-" + "clipboard-",
    "pasted-" + "text.txt",
]
SECRET_PATTERNS = [
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(
        r"(?i)\b(?:api[_-]?key|client[_-]?secret|access[_-]?token|"
        r"refresh[_-]?token|password)\b\s*[:=]\s*[\"']?[A-Za-z0-9_./+=-]{8,}"
    ),
]


def should_skip(path: Path) -> bool:
    return any(part in SKIP_DIRS for part in path.parts)


def is_text_file(path: Path) -> bool:
    return path.name in TEXT_NAMES or path.suffix in TEXT_SUFFIXES or path.name.startswith(".")


def main() -> int:
    errors: list[str] = []

    for path in sorted(ROOT.rglob("*")):
        if should_skip(path) or not path.is_file():
            continue
        if path.name == ".DS_Store":
            errors.append(f"remove Finder metadata: {path.relative_to(ROOT)}")
            continue
        if not is_text_file(path):
            continue

        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue

        rel = path.relative_to(ROOT)
        if text and not text.endswith("\n"):
            errors.append(f"missing final newline: {rel}")
        if "\r\n" in text:
            errors.append(f"contains CRLF line endings: {rel}")
        if any(marker in text for marker in PLACEHOLDER_MARKERS):
            errors.append(f"contains unresolved placeholder: {rel}")
        for marker in LOCAL_STATE_MARKERS:
            if marker in text:
                errors.append(f"contains machine-local state marker {marker}: {rel}")
        if any(pattern.search(text) for pattern in SECRET_PATTERNS):
            errors.append(f"contains credential-like content: {rel}")

        for line_number, line in enumerate(text.splitlines(), start=1):
            if line.rstrip(" \t") != line:
                errors.append(f"trailing whitespace: {rel}:{line_number}")

    if errors:
        for error in errors:
            print(error)
        return 1

    print("lint ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
