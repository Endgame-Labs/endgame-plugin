# Endgame MCP Connector

The plugin manifest loads `mcp/endgame.json`, which declares Endgame's
production streamable HTTP endpoint:

```text
https://app.endgame.io/api/v1/mcp
```

The config intentionally contains no API key, bearer token, organization ID,
or custom authorization header. The Endgame server and Claude host negotiate
OAuth, and the host stores each user's credentials outside this repository.

## Claude Code

For local development, start Claude Code from the parent directory:

```bash
claude --plugin-dir ./endgame-plugin
```

On first load, open `/mcp`, select `plugin:endgame:endgame`, and complete the
Endgame sign-in flow. Claude Code stores and refreshes the OAuth credentials.
Use the same `/mcp` menu to re-authenticate or clear authentication later.

To authenticate directly from a terminal instead, run from the repository root:

```bash
claude --plugin-dir . mcp login plugin:endgame:endgame
```

## Claude Chat And Cowork

Claude Chat and Cowork do not consume Claude Code's `--plugin-dir` flag. Add the
packaged ZIP under `Customize -> Plugins` in Claude Desktop, or install the
plugin from a marketplace. The package declares the Endgame connector, but
organization policy may still require an admin to approve it or add Endgame
under `Customize -> Connectors` using the same production URL. Each user then
completes OAuth. No API key or legacy `mcp-remote` bridge is required.

Before testing an uploaded plugin, disconnect any standalone custom Endgame
connector that uses the same URL. Claude Desktop can keep both registrations
active and silently use the standalone connector while the plugin connector is
disconnected or reconnecting. Connect Endgame from the plugin details page,
then start a fresh chat before verifying its deferred tool registry and health.

## Smoke Test

From the repository root, run:

```bash
make smoke
```

The test asks the local Claude CLI to load the plugin and list MCP servers. A
fresh install should discover this line before authentication:

```text
plugin:endgame:endgame: https://app.endgame.io/api/v1/mcp (HTTP) - ! Needs authentication
```

After sign-in, the status should become `Connected`. The smoke test checks
discovery and endpoint wiring; it does not require or inspect user credentials.

## Runtime User Context

User-relative workflows resolve identity and account scope from the context and
capabilities Endgame MCP makes available at runtime. Fully explicit requests do
not need user-relative resolution. Skills define the required context but do not
name MCP tools or prescribe execution order. Skills may use other connected
sources when relevant, while preserving source authority and provenance. See
`docs/user-context.md` for the shared contract and clean-install check.

References:

- [Endgame MCP Server](https://docs.endgame.io/features/mcp-server)
- [Claude Code MCP reference](https://code.claude.com/docs/en/mcp)
- [Claude Code plugin reference](https://code.claude.com/docs/en/plugins-reference)
