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
PACKAGE_ROOT_FILES = [
    ".claude-plugin/plugin.json",
    "LICENSE",
    "mcp/endgame.json",
]
PUBLIC_SKILLS = [
    "account-brief",
    "call-review",
    "customer-evidence",
    "meeting-follow-up",
    "meeting-prep",
    "pipeline-review",
    "stakeholder-map",
]
ZIP_TIMESTAMP = (1980, 1, 1, 0, 0, 0)


def package_version() -> str:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    version = manifest.get("version")
    if not isinstance(version, str) or not version:
        raise ValueError("plugin manifest is missing a version")
    return version


def git_paths(args: list[str]) -> list[str]:
    output = subprocess.check_output(["git", "-C", str(ROOT), *args])
    return [
        path.decode("utf-8", "surrogateescape")
        for path in output.split(b"\0")
        if path
    ]


def package_names_from(tracked: set[str]) -> list[str]:
    names = set(PACKAGE_ROOT_FILES)
    for skill in PUBLIC_SKILLS:
        prefix = f"skills/{skill}/"
        skill_files = {name for name in tracked if name.startswith(prefix)}
        skill_entrypoint = f"{prefix}SKILL.md"
        if skill_entrypoint not in skill_files:
            raise ValueError(f"package source is missing required skill: {skill_entrypoint}")
        names.update(skill_files)

    missing = sorted(name for name in names if name not in tracked)
    if missing:
        raise ValueError(f"package source contains untracked files: {', '.join(missing)}")

    return sorted(names)


def package_names() -> list[str]:
    tracked = set(git_paths(["ls-files", "-z"]))
    names = package_names_from(tracked)

    untracked_runtime = [
        name
        for name in git_paths(
            ["ls-files", "-z", "--others", "--exclude-standard"]
        )
        if any(name.startswith(f"skills/{skill}/") for skill in PUBLIC_SKILLS)
    ]
    if untracked_runtime:
        raise ValueError(
            "public skill directories contain untracked runtime files: "
            + ", ".join(sorted(untracked_runtime))
        )

    return names


def source_files() -> list[Path]:
    names = package_names()
    subprocess.check_call(
        [
            "git",
            "-C",
            str(ROOT),
            "-c",
            "core.fileMode=true",
            "diff",
            "--quiet",
            "HEAD",
            "--",
            *names,
        ]
    )

    candidates = [ROOT / name for name in names]
    for path in candidates:
        if not path.is_file():
            raise ValueError(
                f"package source must be a regular file: {path.relative_to(ROOT)}"
            )
        if path.is_symlink():
            raise ValueError(f"package source must not be a symlink: {path.relative_to(ROOT)}")
    return candidates


def write_archive(output: Path) -> None:
    files = source_files()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.unlink(missing_ok=True)

    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in files:
            relative = path.relative_to(ROOT).as_posix()
            mode = path.stat().st_mode & 0o777
            info = zipfile.ZipInfo(relative, date_time=ZIP_TIMESTAMP)
            info.create_system = 3
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = (stat.S_IFREG | mode) << 16
            archive.writestr(info, path.read_bytes())


def verify_archive(output: Path, name: str, version: str) -> None:
    required = set(package_names())
    forbidden = {"skills/user-context/SKILL.md"}
    with zipfile.ZipFile(output) as archive:
        names = archive.namelist()
        if len(names) != len(set(names)):
            raise ValueError("plugin package contains duplicate paths")
        if required - set(names):
            missing = ", ".join(sorted(required - set(names)))
            raise ValueError(f"plugin package is missing required files: {missing}")
        if set(names) - required:
            unexpected = ", ".join(sorted(set(names) - required))
            raise ValueError(f"plugin package contains unexpected files: {unexpected}")
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
