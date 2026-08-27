# Endgame for Claude

Official Claude plugin from Endgame for GTM teams.

Use your Endgame customer and prospect context to prepare for meetings, write
follow-ups, review pipeline and calls, map stakeholders, summarize customer
evidence, and more.

## Supported Claude Surfaces

- Claude Chat on the web
- Claude Desktop Chat
- Claude Cowork
- Claude Code

## Getting Started

You need an Endgame account with access to your organization's customer and
prospect context. The plugin prompts each user to sign in to Endgame when it
first needs the bundled connector.

### Claude Chat And Cowork

Open `Customize -> Plugins`, find **Endgame**, and select **Install**. In
Cowork, open the Cowork tab before opening Customize. Open the installed plugin
to connect Endgame and review its included skills.

### Claude Code Marketplace

```bash
claude plugin marketplace add https://github.com/Endgame-Labs/endgame-plugin.git
claude plugin install endgame@endgame-plugins
```

Endgame also plans to submit this public repository to Anthropic's plugin
directory. Until that listing is approved, the Endgame-hosted marketplace above
is the supported Claude Code installation path.

### Development From Source

```bash
git clone https://github.com/Endgame-Labs/endgame-plugin.git
claude --plugin-dir ./endgame-plugin
```

### Test A Packaged Build

Run `make package`, then load the generated archive directly in Claude Code:

```bash
claude --plugin-dir /path/to/endgame-plugin-0.1.6.zip
```

For Chat and Cowork release-candidate testing, upload that same ZIP through
`Customize -> Plugins` in Claude Desktop or through a Team or Enterprise test
marketplace. The archive retains the production `endgame` identity so the test
exercises the namespace and manifest that will be released.

On first load, connect Endgame when prompted. In Claude Code, open `/mcp` and
select `plugin:endgame:endgame`. On Team or Enterprise plans, an admin may need
to approve the Endgame connector at `https://app.endgame.io/api/v1/mcp`.

See `mcp/README.md` for connector setup and smoke testing, and
`docs/release.md` for packaging.

Claude Code invokes skills through the `endgame` namespace:

```text
/endgame:account-brief
/endgame:meeting-prep
/endgame:meeting-follow-up
/endgame:pipeline-review
/endgame:call-review
/endgame:stakeholder-map
/endgame:customer-evidence
```

In Chat and Cowork, Claude can select the installed skills when they match your
request. Type `/` or select `+` to choose a skill directly. See
`docs/command-surface.md` for the command contract.

## Repo Layout

```text
.claude-plugin/plugin.json  Plugin manifest
skills/                     Claude skill packages
mcp/                        MCP connector assets and docs
scripts/                    Local repository checks
docs/                       Package and release documentation
```

## Development Commands

```bash
make fmt
make format
make lint
make validate
make test
make package
make smoke
make smoke-package
make check
```

- `make fmt` normalizes JSON metadata.
- `make format` is kept as an alias for people coming from package-script repos.
- `make lint` checks text hygiene and placeholder leakage.
- `make validate` validates the manifest, package layout, skills, and MCP config.
- `make test` checks that Git and ZIP installations contain the same runtime
  files and that release metadata is consistent.
- `make package` builds a deterministic installable ZIP under `dist/`.
- `make smoke` asks the local Claude CLI to discover the bundled MCP server.
- `make smoke-package` repeats discovery from the packaged ZIP.
- `make check` runs lint and validation together.

## Included Skills

The plugin includes seven GTM workflows:

- `account-brief`
- `meeting-prep`
- `meeting-follow-up`
- `pipeline-review`
- `call-review`
- `stakeholder-map`
- `customer-evidence`

Each public skill defines the context and evidence it needs without naming MCP
tools or prescribing execution order. The client and model select from the
capabilities available at runtime. See `docs/user-context.md` for the shared
authoring contract.
