# Package Layout

The customer archive uses this minimal Claude plugin package shape:

```text
endgame-plugin/
  .claude-plugin/
    plugin.json
  mcp/
    endgame.json
  skills/
    <skill-name>/
      SKILL.md
      references/  (optional)
      examples/    (optional)
      assets/      (optional)
      scripts/     (optional)
  LICENSE
```

Repository-only validation, release, and architecture files under `scripts/`
and `docs/` are excluded from the customer archive.

## Manifest

`.claude-plugin/plugin.json` is the package manifest. The plugin namespace is
`endgame`.

## Skills

Each skill belongs in `skills/<skill-slug>/`. Skill slugs should be lowercase,
hyphen-delimited, and stable because users invoke them by namespace. Packaging
includes every tracked file below each approved public skill directory, so a
skill's references, examples, assets, and scripts travel with its `SKILL.md`.

The package contains only the seven public skills. Each skill applies the
MCP-backed identity and scope contract documented in `docs/user-context.md`
directly when its request is user-relative.

## Command Surface

Claude Code exposes plugin skills as namespaced slash commands. Claude Chat and
Cowork expose installed skills as short commands. The v1 package uses the seven
`SKILL.md` files as the 1:1 command entrypoints instead of adding legacy flat
files under `commands/`. The command contract and argument hints are documented
in `docs/command-surface.md`.

## MCP

The manifest points `mcpServers` at `mcp/endgame.json`. That file declares the
production Endgame streamable HTTP endpoint and relies on the host's OAuth
flow, so the repository never stores user tokens or organization IDs.

Connector setup and smoke-test instructions live in `mcp/README.md`.

## Scripts

Repository checks live in `scripts/` and must run without vendored dependencies.
`scripts/package_plugin.py` derives the runtime payload from tracked Git files,
builds the ignored ZIP artifact, and verifies that its file list matches the
Git installation. `scripts/smoke_plugin.py` verifies MCP discovery from source
or package form.
