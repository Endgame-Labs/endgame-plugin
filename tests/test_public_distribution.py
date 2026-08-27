from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import unittest
import zipfile
from pathlib import Path


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


if __name__ == "__main__":
    unittest.main()
