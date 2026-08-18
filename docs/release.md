# Packaging And Release

## Build An Installable Archive

Run from the repository root:

```bash
make package
```

Build release candidates from a clean commit and record that commit alongside
the generated checksum.

The target runs the offline repository checks, then writes:

```text
dist/endgame-plugin-<manifest-version>.zip
```

The archive has the plugin manifest at its root and can be loaded directly by
Claude Code 2.1.128 or later:

```bash
claude --plugin-dir ./dist/endgame-plugin-0.1.6.zip
```

The builder uses sorted paths, fixed ZIP timestamps, and preserved Unix file
modes so the same source and manifest version produce the same archive bytes.
It rejects unsafe or incomplete archives and prints the artifact SHA-256 after
every build.

## Verify The Archive

```bash
make smoke-package
```

This rebuilds the ZIP, asks Claude to load it, and verifies discovery of the
scoped Endgame MCP server. The archive contains only the plugin manifest, MCP
configuration, public skills, and license.

## Release State

- `dist/` is ignored and release artifacts are not committed.
- The manifest version controls the archive filename and installed plugin
  version. Version bumps are manual in v1.
- Releases are published through the `endgame-plugins` marketplace. Its plugin
  source uses a full approved commit SHA.
- Version bumps and marketplace source updates are manual.
- Publish only from a clean, reviewed commit that passes the package smoke test.
