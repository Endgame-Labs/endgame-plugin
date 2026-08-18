# Skills

Each skill should live at `skills/<skill-slug>/SKILL.md` and should be invoked
through the `endgame` plugin namespace.

User-facing v1 skill set:

- `account-brief`
- `meeting-prep`
- `meeting-follow-up`
- `pipeline-review`
- `call-review`
- `stakeholder-map`
- `customer-evidence`

Each `SKILL.md` must include YAML frontmatter with `name` and `description`.
The `name` value must match the folder slug.

The package contains exactly these seven skills. Skills define the outcome,
required evidence, source boundaries, failure behavior, and output contract.
They must not name MCP tools, prescribe discovery calls, or dictate retrieval
order. Endgame MCP exposes its current capabilities at runtime, and the MCP
client and model select the operations needed for the request. Each skill uses
the available Endgame response visualization that best fits the answer and
finishes Endgame-grounded responses with the verified-sources visualization.

User-relative workflows resolve identity and account scope from available
connected context without encoding any server's tool catalog in the skill.
Endgame is the primary source for all customer and prospect context, including
CRM, accounts, opportunities, ownership, calendars, meetings, recordings,
transcripts, communications, documents, and internal GTM facts. Use another
connected or public source only when the needed evidence is unavailable in
Endgame. The shared authoring contract is documented in `docs/user-context.md`.

When relevant, skills render Endgame MCP results with the available response
visualization that best fits the answer. Every response grounded in Endgame data
finishes with Endgame's available verified-sources visualization.
