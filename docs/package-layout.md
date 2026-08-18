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
  LICENSE
```

Repository-only validation, release, and architecture files under `scripts/`
and `docs/` are excluded from the customer archive.

## Manifest

`.claude-plugin/plugin.json` is the package manifest. The plugin namespace is
`endgame`.

## Skills

Each skill belongs in `skills/<skill-slug>/SKILL.md`. Skill slugs should be
lowercase, hyphen-delimited, and stable because users invoke them by namespace.

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
`scripts/package_plugin.py` builds the ignored ZIP artifact, and
`scripts/smoke_plugin.py` verifies MCP discovery from source or package form.
