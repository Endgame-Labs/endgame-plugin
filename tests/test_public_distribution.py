from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]


def load_script(name: str):
    path = ROOT / "scripts" / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


package_plugin = load_script("package_plugin")
check_release_tag = load_script("check_release_tag")
check_version_bump = load_script("check_version_bump")


class PublicDistributionTests(unittest.TestCase):
    def test_marketplace_uses_repository_root(self) -> None:
        marketplace = json.loads(
            (ROOT / ".claude-plugin" / "marketplace.json").read_text(encoding="utf-8")
        )
        self.assertEqual(marketplace["plugins"][0]["source"], "./")

    def test_package_includes_every_tracked_public_skill_file(self) -> None:
        tracked = set(
            subprocess.check_output(
                ["git", "-C", str(ROOT), "ls-files"], text=True
            ).splitlines()
        )
        expected = set(package_plugin.PACKAGE_ROOT_FILES)
        for skill in package_plugin.PUBLIC_SKILLS:
            expected.update(
                name for name in tracked if name.startswith(f"skills/{skill}/")
            )
        self.assertEqual(set(package_plugin.package_names()), expected)

    def test_new_tracked_skill_resources_are_included_recursively(self) -> None:
        tracked = set(package_plugin.PACKAGE_ROOT_FILES)
        for skill in package_plugin.PUBLIC_SKILLS:
            tracked.add(f"skills/{skill}/SKILL.md")
        resource = "skills/account-brief/references/field-guide.md"
        tracked.add(resource)
        self.assertIn(resource, package_plugin.package_names_from(tracked))

    def test_git_path_parsing_preserves_unicode_package_names(self) -> None:
        tracked = set(package_plugin.PACKAGE_ROOT_FILES)
        for skill in package_plugin.PUBLIC_SKILLS:
            tracked.add(f"skills/{skill}/SKILL.md")
        resource = "skills/account-brief/references/résumé.md"
        tracked.add(resource)
        encoded = b"\0".join(path.encode("utf-8") for path in sorted(tracked)) + b"\0"

        with mock.patch.object(
            package_plugin.subprocess,
            "check_output",
            side_effect=[encoded, b""],
        ):
            self.assertIn(resource, package_plugin.package_names())

    def test_package_reads_committed_blob_bytes_and_mode(self) -> None:
        tree_record = b"100755 blob abc123\tskills/example/script.sh\0"
        with mock.patch.object(
            package_plugin,
            "git_bytes",
            side_effect=[tree_record, b"#!/bin/sh\n"],
        ):
            entry = package_plugin.git_entry("skills/example/script.sh")
        self.assertEqual(entry.data, b"#!/bin/sh\n")
        self.assertEqual(entry.mode, 0o755)

    def test_archive_matches_git_runtime_payload(self) -> None:
        self.assertEqual(package_plugin.main(), 0)
        version = package_plugin.package_version()
        archive_path = ROOT / "dist" / f"endgame-plugin-{version}.zip"
        with zipfile.ZipFile(archive_path) as archive:
            self.assertEqual(set(archive.namelist()), set(package_plugin.package_names()))

    def test_release_tag_parser_accepts_manifest_version(self) -> None:
        version = package_plugin.package_version()
        self.assertEqual(check_release_tag.expected_version(f"v{version}"), version)

    def test_release_tag_parser_rejects_non_semver(self) -> None:
        with self.assertRaises(ValueError):
            check_release_tag.expected_version("release-latest")

    def test_release_commit_must_match_head_and_origin_main(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repository = Path(directory)
            subprocess.run(["git", "init", "-q", repository], check=True)
            subprocess.run(
                ["git", "-C", repository, "config", "user.email", "test@example.com"],
                check=True,
            )
            subprocess.run(
                ["git", "-C", repository, "config", "user.name", "Test"],
                check=True,
            )
            (repository / "file.txt").write_text("main\n", encoding="utf-8")
            subprocess.run(["git", "-C", repository, "add", "file.txt"], check=True)
            subprocess.run(
                ["git", "-C", repository, "commit", "-q", "-m", "main"], check=True
            )
            main_commit = subprocess.check_output(
                ["git", "-C", repository, "rev-parse", "HEAD"], text=True
            ).strip()
            subprocess.run(
                [
                    "git",
                    "-C",
                    repository,
                    "update-ref",
                    "refs/remotes/origin/main",
                    main_commit,
                ],
                check=True,
            )
            subprocess.run(
                ["git", "-C", repository, "tag", "v0.1.0", main_commit], check=True
            )

            with mock.patch.object(check_release_tag, "ROOT", repository):
                self.assertEqual(
                    check_release_tag.verify_release_commit("v0.1.0"), main_commit
                )

                (repository / "file.txt").write_text("branch\n", encoding="utf-8")
                subprocess.run(["git", "-C", repository, "add", "file.txt"], check=True)
                subprocess.run(
                    ["git", "-C", repository, "commit", "-q", "-m", "branch"],
                    check=True,
                )
                with self.assertRaisesRegex(ValueError, "does not match"):
                    check_release_tag.verify_release_commit("v0.1.0")
                subprocess.run(
                    ["git", "-C", repository, "tag", "v0.1.1", "HEAD"], check=True
                )
                with self.assertRaisesRegex(ValueError, "not contained in origin/main"):
                    check_release_tag.verify_release_commit("v0.1.1")

    def test_runtime_change_detection_is_unicode_and_rename_safe(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repository = Path(directory)
            subprocess.run(["git", "init", "-q", repository], check=True)
            subprocess.run(
                ["git", "-C", repository, "config", "user.email", "test@example.com"],
                check=True,
            )
            subprocess.run(
                ["git", "-C", repository, "config", "user.name", "Test"],
                check=True,
            )
            guide = repository / "skills" / "example" / "references" / "guide.md"
            guide.parent.mkdir(parents=True)
            guide.write_text("guide\n", encoding="utf-8")
            subprocess.run(["git", "-C", repository, "add", "."], check=True)
            subprocess.run(
                ["git", "-C", repository, "commit", "-q", "-m", "base"], check=True
            )
            base = subprocess.check_output(
                ["git", "-C", repository, "rev-parse", "HEAD"], text=True
            ).strip()

            (repository / "docs").mkdir()
            subprocess.run(
                ["git", "-C", repository, "mv", str(guide), "docs/guide.md"],
                check=True,
            )
            unicode_resource = (
                repository / "skills" / "example" / "references" / "résumé.md"
            )
            unicode_resource.write_text("resource\n", encoding="utf-8")
            subprocess.run(["git", "-C", repository, "add", "."], check=True)
            subprocess.run(
                ["git", "-C", repository, "commit", "-q", "-m", "head"], check=True
            )
            head = subprocess.check_output(
                ["git", "-C", repository, "rev-parse", "HEAD"], text=True
            ).strip()

            with mock.patch.object(check_version_bump, "ROOT", repository):
                changes = check_version_bump.runtime_changes(base, head)
            self.assertIn("skills/example/references/guide.md", changes)
            self.assertIn("skills/example/references/résumé.md", changes)

    def test_runtime_version_must_increase_monotonically(self) -> None:
        self.assertGreater(
            check_version_bump.semantic_version("1.0.0"),
            check_version_bump.semantic_version("0.99.99"),
        )
        self.assertLess(
            check_version_bump.semantic_version("0.1.5"),
            check_version_bump.semantic_version("0.1.6"),
        )

    def test_runtime_version_downgrade_fails_check(self) -> None:
        with (
            mock.patch.object(sys, "argv", ["check_version_bump.py", "base", "head"]),
            mock.patch.object(
                check_version_bump, "runtime_changes", return_value=["skills/example/SKILL.md"]
            ),
            mock.patch.object(
                check_version_bump,
                "manifest_version",
                side_effect=["0.1.6", "0.1.5"],
            ),
        ):
            self.assertEqual(check_version_bump.main(), 1)

    def test_release_workflow_uses_exact_tag_and_immutable_assets(self) -> None:
        workflow = (ROOT / ".github" / "workflows" / "release.yml").read_text(
            encoding="utf-8"
        )
        self.assertIn("ref: refs/tags/${{ env.RELEASE_TAG }}", workflow)
        self.assertIn("refs/remotes/origin/main", workflow)
        self.assertNotIn("--clobber", workflow)
        self.assertIn('cmp "$artifact"', workflow)


if __name__ == "__main__":
    unittest.main()
