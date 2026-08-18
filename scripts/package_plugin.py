#!/usr/bin/env python3
"""Build a deterministic, installable Endgame plugin ZIP archive."""

from __future__ import annotations

import hashlib
import json
import stat
import subprocess
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / ".claude-plugin" / "plugin.json"
DIST = ROOT / "dist"
PACKAGE_FILES = [
    ".claude-plugin/plugin.json",
    "LICENSE",
    "mcp/endgame.json",
    "skills/account-brief/SKILL.md",
    "skills/call-review/SKILL.md",
    "skills/customer-evidence/SKILL.md",
    "skills/meeting-follow-up/SKILL.md",
    "skills/meeting-prep/SKILL.md",
    "skills/pipeline-review/SKILL.md",
    "skills/stakeholder-map/SKILL.md",
]
ZIP_TIMESTAMP = (1980, 1, 1, 0, 0, 0)


def package_version() -> str:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    version = manifest.get("version")
    if not isinstance(version, str) or not version:
        raise ValueError("plugin manifest is missing a version")
    return version


def source_files() -> list[Path]:
    paths = [ROOT / name for name in PACKAGE_FILES]

    candidates = sorted(set(paths), key=lambda path: path.relative_to(ROOT).as_posix())
    tracked = {
        ROOT / name
        for name in subprocess.check_output(
            ["git", "-C", str(ROOT), "ls-files"], text=True
        ).splitlines()
    }
    untracked = [path for path in candidates if path not in tracked]
    if untracked:
        names = ", ".join(path.relative_to(ROOT).as_posix() for path in untracked)
        raise ValueError(f"package source contains untracked files: {names}")

    for path in candidates:
        if path.is_symlink():
            raise ValueError(f"package source must not be a symlink: {path.relative_to(ROOT)}")

    return candidates


def write_archive(output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    output.unlink(missing_ok=True)

    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in source_files():
            relative = path.relative_to(ROOT).as_posix()
            mode = path.stat().st_mode & 0o777
            info = zipfile.ZipInfo(relative, date_time=ZIP_TIMESTAMP)
            info.create_system = 3
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = (stat.S_IFREG | mode) << 16
            archive.writestr(info, path.read_bytes())


def verify_archive(output: Path, name: str, version: str) -> None:
    required = set(PACKAGE_FILES)
    forbidden = {"skills/user-context/SKILL.md"}
    with zipfile.ZipFile(output) as archive:
        names = archive.namelist()
        if len(names) != len(set(names)):
            raise ValueError("plugin package contains duplicate paths")
        if required - set(names):
            missing = ", ".join(sorted(required - set(names)))
            raise ValueError(f"plugin package is missing required files: {missing}")
        if forbidden & set(names):
            unexpected = ", ".join(sorted(forbidden & set(names)))
            raise ValueError(f"plugin package contains removed files: {unexpected}")
        for archive_name in names:
            path = Path(archive_name)
            if path.is_absolute() or ".." in path.parts:
                raise ValueError(f"plugin package contains an unsafe path: {archive_name}")

        manifest = json.loads(archive.read(".claude-plugin/plugin.json"))
        if manifest.get("name") != name or manifest.get("version") != version:
            raise ValueError("packaged manifest identity does not match the build")


def main() -> int:
    try:
        version = package_version()
        output = DIST / f"endgame-plugin-{version}.zip"
        write_archive(output)
        verify_archive(output, "endgame", version)
        digest = hashlib.sha256(output.read_bytes()).hexdigest()
    except (OSError, ValueError, subprocess.CalledProcessError) as exc:
        print(f"package error: {exc}")
        return 1

    print(f"plugin package: {output.relative_to(ROOT)}")
    print(f"sha256: {digest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
