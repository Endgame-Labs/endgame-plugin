#!/usr/bin/env python3
"""Build a deterministic, installable Endgame plugin ZIP archive."""

from __future__ import annotations

import hashlib
import json
import stat
import subprocess
import zipfile
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
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


@dataclass(frozen=True)
class PackageEntry:
    name: str
    data: bytes
    mode: int


def git_bytes(args: list[str]) -> bytes:
    return subprocess.check_output(["git", "-C", str(ROOT), *args])


def package_version() -> str:
    manifest = json.loads(
        git_bytes(["show", "HEAD:.claude-plugin/plugin.json"]).decode("utf-8")
    )
    version = manifest.get("version")
    if not isinstance(version, str) or not version:
        raise ValueError("plugin manifest is missing a version")
    return version


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
    tracked = set(
        path.decode("utf-8", "surrogateescape")
        for path in git_bytes(["ls-tree", "-r", "--name-only", "-z", "HEAD"]).split(
            b"\0"
        )
        if path
    )
    names = package_names_from(tracked)

    untracked_runtime = []
    for raw_name in git_bytes(
        ["ls-files", "-z", "--others", "--exclude-standard"]
    ).split(b"\0"):
        if not raw_name:
            continue
        name = raw_name.decode("utf-8", "surrogateescape")
        if any(name.startswith(f"skills/{skill}/") for skill in PUBLIC_SKILLS):
            untracked_runtime.append(name)
    if untracked_runtime:
        raise ValueError(
            "public skill directories contain untracked runtime files: "
            + ", ".join(sorted(untracked_runtime))
        )

    return names


def git_entry(name: str) -> PackageEntry:
    tree_output = git_bytes(["ls-tree", "-z", "HEAD", "--", name])
    records = [record for record in tree_output.split(b"\0") if record]
    if len(records) != 1 or b"\t" not in records[0]:
        raise ValueError(f"package source is not a committed file: {name}")

    metadata, raw_name = records[0].split(b"\t", 1)
    mode_text, object_type, _object_id = metadata.split(b" ", 2)
    committed_name = raw_name.decode("utf-8", "surrogateescape")
    if committed_name != name or object_type != b"blob":
        raise ValueError(f"package source is not a committed file: {name}")

    git_mode = int(mode_text, 8)
    if git_mode not in {0o100644, 0o100755}:
        raise ValueError(f"package source must be a regular file: {name}")

    return PackageEntry(
        name=name,
        data=git_bytes(["show", f"HEAD:{name}"]),
        mode=git_mode & 0o777,
    )


def source_entries() -> list[PackageEntry]:
    return [git_entry(name) for name in package_names()]


def write_archive(output: Path) -> None:
    entries = source_entries()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.unlink(missing_ok=True)

    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for entry in entries:
            info = zipfile.ZipInfo(entry.name, date_time=ZIP_TIMESTAMP)
            info.create_system = 3
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = (stat.S_IFREG | entry.mode) << 16
            archive.writestr(info, entry.data)


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
