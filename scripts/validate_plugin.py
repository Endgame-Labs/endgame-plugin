#!/usr/bin/env python3
"""Validate the baseline Claude plugin package."""

from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / ".claude-plugin" / "plugin.json"
MARKETPLACE = ROOT / ".claude-plugin" / "marketplace.json"
MCP_CONFIG = ROOT / "mcp" / "endgame.json"
REQUIRED_DIRS = [".claude-plugin", "skills", "mcp", "scripts", "docs"]
REQUIRED_FILES = [
    "README.md",
    "Makefile",
    ".claude-plugin/plugin.json",
    ".claude-plugin/marketplace.json",
    "docs/release.md",
    "docs/user-context.md",
    "mcp/endgame.json",
    "scripts/package_plugin.py",
    "scripts/smoke_plugin.py",
]
ENDGAME_MCP_URL = "https://app.endgame.io/api/v1/mcp"
MARKETPLACE_NAME = "endgame-plugins"
MARKETPLACE_SOURCE = "./"
MARKETPLACE_DESCRIPTION = "Official Claude plugin from Endgame for GTM teams."
PLUGIN_DESCRIPTION = (
    "Use your Endgame customer and prospect context to prepare for meetings, "
    "write follow-ups, review pipeline and calls, map stakeholders, summarize "
    "customer evidence, and more."
)
MARKETPLACE_TAGS = {
    "endgame",
    "gtm",
    "sales",
    "revenue",
    "pipeline",
    "meeting-prep",
    "customer-intelligence",
}
REQUIRED_SKILLS = [
    "account-brief",
    "meeting-prep",
    "meeting-follow-up",
    "pipeline-review",
    "call-review",
    "stakeholder-map",
    "customer-evidence",
]
REQUIRED_SKILL_ARGUMENT_HINTS = {
    "account-brief": "[account name or domain]",
    "meeting-prep": "[meeting, account, or time]",
    "meeting-follow-up": "[meeting, account, or date]",
    "pipeline-review": "[owner, team, segment, or period]",
    "call-review": "[call, meeting, or account]",
    "stakeholder-map": "[account or opportunity]",
    "customer-evidence": "[topic and optional timeframe]",
}
RUNTIME_CONTEXT_MARKERS = [
    "Use connected context only when those do not establish it",
    "Use Endgame as the primary source for all customer and prospect context",
    "Use another connected or public source only when",
    "unavailable in Endgame",
    "render Endgame MCP results with the available response visualization",
    "verified-sources visualization as the final action",
    "one source as equivalent to another",
]
PIPELINE_COMPLETENESS_MARKERS = [
    "begin the review without asking for confirmation",
    "Confirmed source blank",
    "Not returned",
    "Conflicting values",
    "authoritative evidence",
    "missing or partial result",
]
NAME_RE = re.compile(r"^[a-z0-9][a-z0-9-]{0,63}$")
MCP_TOOL_NAME_RE = re.compile(
    r"\b(?:create|delete|download|fetch|get|list|persist|read|render|search|submit|update)_[a-z0-9_]+\b"
)


def load_manifest() -> dict[str, Any]:
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def load_mcp_config() -> dict[str, Any]:
    return json.loads(MCP_CONFIG.read_text(encoding="utf-8"))


def load_marketplace() -> dict[str, Any]:
    return json.loads(MARKETPLACE.read_text(encoding="utf-8"))


def git_output(args: list[str]) -> str:
    return subprocess.check_output(
        ["git", "-C", str(ROOT), *args],
        stderr=subprocess.DEVNULL,
        text=True,
    ).strip()


def parse_frontmatter(path: Path, errors: list[str]) -> tuple[dict[str, str], str]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()

    if len(lines) < 3 or lines[0] != "---":
        errors.append(f"skill missing YAML frontmatter: {path.relative_to(ROOT)}")
        return {}, ""

    metadata: dict[str, str] = {}
    end_index = None
    for index, line in enumerate(lines[1:], start=1):
        if line == "---":
            end_index = index
            break
        if ":" not in line:
            errors.append(
                f"skill frontmatter line is not key/value: {path.relative_to(ROOT)}:{index + 1}"
            )
            continue
        key, value = line.split(":", 1)
        metadata[key.strip()] = value.strip().strip('"').strip("'")

    if end_index is None:
        errors.append(f"skill frontmatter is not closed: {path.relative_to(ROOT)}")
        return metadata, ""

    body = "\n".join(lines[end_index + 1 :]).strip()
    if not body:
        errors.append(f"skill body is empty: {path.relative_to(ROOT)}")

    return metadata, body


def validate_skills(errors: list[str]) -> None:
    skills_root = ROOT / "skills"
    if not skills_root.exists():
        return

    for slug in REQUIRED_SKILLS:
        skill_file = skills_root / slug / "SKILL.md"
        if not skill_file.is_file():
            errors.append(f"missing required skill: skills/{slug}/SKILL.md")

    for skill_dir in sorted(skills_root.iterdir()):
        if not skill_dir.is_dir():
            continue
        rel = skill_dir.relative_to(ROOT)
        if not NAME_RE.fullmatch(skill_dir.name):
            errors.append(f"skill directory must be lowercase hyphen-case: {rel}")
            continue

        skill_file = skill_dir / "SKILL.md"
        if not skill_file.is_file():
            errors.append(f"skill directory missing SKILL.md: {rel}")
            continue

        metadata, body = parse_frontmatter(skill_file, errors)
        skill_text = skill_file.read_text(encoding="utf-8")
        if metadata.get("name") != skill_dir.name:
            errors.append(f"skill name must match directory: {skill_file.relative_to(ROOT)}")
        if not metadata.get("description"):
            errors.append(f"skill missing description: {skill_file.relative_to(ROOT)}")

        expected_hint = REQUIRED_SKILL_ARGUMENT_HINTS.get(skill_dir.name)
        if expected_hint and metadata.get("argument-hint") != expected_hint:
            errors.append(
                "skill argument-hint must match v1 command contract: "
                f"{skill_file.relative_to(ROOT)}"
            )
        if expected_hint and metadata.get("user-invocable") == "false":
            errors.append(
                f"v1 skill must remain user-invocable: {skill_file.relative_to(ROOT)}"
            )
        if skill_dir.name == "user-context":
            errors.append("user-context must not be packaged as a separate skill")

        named_operations = sorted(set(MCP_TOOL_NAME_RE.findall(skill_text)))
        if named_operations:
            errors.append(
                "skill must not prescribe MCP tool names "
                f"{', '.join(named_operations)}: {skill_file.relative_to(ROOT)}"
            )

        normalized_body = " ".join(body.split())

        if expected_hint:
            for marker in RUNTIME_CONTEXT_MARKERS:
                if marker not in normalized_body:
                    errors.append(
                        "v1 skill missing runtime-context policy marker "
                        f"{marker}: {skill_file.relative_to(ROOT)}"
                    )
            if "### Source Trail" in body:
                errors.append(
                    "v1 skill must use the Endgame verified-sources visualization instead of "
                    f"a prose Source Trail: {skill_file.relative_to(ROOT)}"
                )

        if skill_dir.name == "pipeline-review":
            for marker in PIPELINE_COMPLETENESS_MARKERS:
                if marker not in normalized_body:
                    errors.append(
                        "pipeline-review missing completeness policy marker "
                        f"{marker}: {skill_file.relative_to(ROOT)}"
                    )


def validate_git(errors: list[str]) -> None:
    if not (ROOT / ".git").exists():
        errors.append("repository is not initialized with git")
        return

    try:
        is_work_tree = git_output(["rev-parse", "--is-inside-work-tree"])
    except (subprocess.CalledProcessError, FileNotFoundError):
        errors.append("git repository metadata is not readable")
        return

    if is_work_tree != "true":
        errors.append("git does not recognize this directory as a work tree")

def validate_mcp(manifest: dict[str, Any], errors: list[str]) -> None:
    if manifest.get("mcpServers") != "./mcp/endgame.json":
        errors.append("manifest mcpServers must reference ./mcp/endgame.json")

    try:
        config = load_mcp_config()
    except Exception as exc:
        errors.append(f"MCP config is not valid JSON: {exc}")
        return

    servers = config.get("mcpServers")
    if not isinstance(servers, dict):
        errors.append("MCP config must contain an mcpServers object")
        return

    if set(config) != {"mcpServers"} or set(servers) != {"endgame"}:
        errors.append("MCP config must contain only the bundled endgame server")

    server = servers.get("endgame")
    if not isinstance(server, dict):
        errors.append("MCP config must declare the endgame server")
        return

    if server.get("type") != "http":
        errors.append("Endgame MCP transport must be http")
    if server.get("url") != ENDGAME_MCP_URL:
        errors.append(f"Endgame MCP URL must be {ENDGAME_MCP_URL}")

    unsupported_keys = set(server) - {"type", "url"}
    if unsupported_keys:
        errors.append(
            "Endgame MCP config must use OAuth without embedded credentials; "
            f"remove: {', '.join(sorted(unsupported_keys))}"
        )


def validate_marketplace(manifest: dict[str, Any], errors: list[str]) -> None:
    try:
        marketplace = load_marketplace()
    except Exception as exc:
        errors.append(f"marketplace manifest is not valid JSON: {exc}")
        return

    if marketplace.get("name") != MARKETPLACE_NAME:
        errors.append(f"marketplace name must be {MARKETPLACE_NAME}")
    if marketplace.get("description") != MARKETPLACE_DESCRIPTION:
        errors.append("marketplace description must use approved customer-facing copy")

    owner = marketplace.get("owner")
    expected_owner = {
        "name": "Endgame",
        "email": "support@endgame.io",
        "url": "https://endgame.io",
    }
    if owner != expected_owner:
        errors.append("marketplace owner must use customer-facing Endgame details")

    plugins = marketplace.get("plugins")
    if not isinstance(plugins, list) or len(plugins) != 1:
        errors.append("marketplace must publish exactly one plugin")
        return

    plugin = plugins[0]
    if not isinstance(plugin, dict) or plugin.get("name") != manifest.get("name"):
        errors.append("marketplace plugin name must match the plugin manifest")
        return
    if plugin.get("displayName") != "Endgame":
        errors.append("marketplace plugin displayName must be Endgame")
    if plugin.get("description") != PLUGIN_DESCRIPTION:
        errors.append("marketplace plugin description must use approved customer-facing copy")
    if plugin.get("category") != "sales":
        errors.append("marketplace plugin category must be sales")
    if set(plugin.get("tags", [])) != MARKETPLACE_TAGS:
        errors.append("marketplace plugin tags must match the external discovery set")

    if plugin.get("source") != MARKETPLACE_SOURCE:
        errors.append(f"marketplace plugin source must be {MARKETPLACE_SOURCE}")


def main() -> int:
    errors: list[str] = []

    for dirname in REQUIRED_DIRS:
        if not (ROOT / dirname).is_dir():
            errors.append(f"missing directory: {dirname}")

    for filename in REQUIRED_FILES:
        if not (ROOT / filename).is_file():
            errors.append(f"missing file: {filename}")

    try:
        manifest = load_manifest()
    except Exception as exc:
        errors.append(f"manifest is not valid JSON: {exc}")
        manifest = {}

    name = manifest.get("name")
    if not isinstance(name, str) or not NAME_RE.fullmatch(name):
        errors.append("manifest name must be lowercase hyphen-case and <= 64 chars")

    if manifest.get("displayName") != "Endgame":
        errors.append("manifest displayName must be Endgame")
    if manifest.get("description") != PLUGIN_DESCRIPTION:
        errors.append("manifest description must use approved customer-facing copy")

    for field in ["version", "description", "homepage", "repository", "license"]:
        if not isinstance(manifest.get(field), str) or not manifest.get(field):
            errors.append(f"manifest missing string field: {field}")

    author = manifest.get("author")
    expected_author = {
        "name": "Endgame",
        "email": "support@endgame.io",
        "url": "https://endgame.io",
    }
    if author != expected_author:
        errors.append("manifest author must use customer-facing Endgame details")

    keywords = manifest.get("keywords")
    if not isinstance(keywords, list) or not all(isinstance(item, str) for item in keywords):
        errors.append("manifest keywords must be a list of strings")

    validate_skills(errors)
    validate_marketplace(manifest, errors)

    validate_mcp(manifest, errors)

    validate_git(errors)

    if errors:
        for error in errors:
            print(error)
        return 1

    print("plugin validation ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
