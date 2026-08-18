# Contributing

This repository contains the official Endgame plugin package.

## Development Rules

- Keep the plugin namespace `endgame`.
- Put Claude skills in `skills/<skill-slug>/SKILL.md`.
- Keep MCP connector assets under `mcp/` and never commit connector credentials.
- Keep scripts dependency-light and runnable with the system Python.
- Do not add generated files, local credentials, or exported customer data.

## Local Checks

Run the full check suite before opening a PR:

```bash
make check
```

The individual commands are:

```bash
make fmt
make lint
make validate
make package
make smoke
make smoke-package
```

`make fmt` normalizes JSON metadata. `make lint` checks text hygiene.
`make validate` checks the plugin manifest and expected package layout.
`make package` builds the ignored ZIP artifact. `make smoke` and
`make smoke-package` require Claude Code and confirm MCP discovery from source
and packaged forms.
