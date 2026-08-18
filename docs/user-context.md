# Runtime User Context

The plugin resolves user-relative scope through Endgame MCP at runtime. It does
not create or read a local preferences file in v1.

## MCP Authoring Contract

Skills define the context required to accomplish a workflow. Endgame MCP exposes
its current capability catalog, and the MCP client and model select the
operations appropriate to the request.

This separation prevents packaged skills from coupling to a changing server
catalog or bypassing normal MCP discovery and selection behavior.

## Minimum Context Contract

| Context | Requirement | Use |
|---------|-------------|-----|
| Identity | Resolve the current user when the request depends on `me` or `my` | Establish role and user-relative scope |
| Organization | Use available Endgame organization context without inference | Establish vendor organization |
| Reporting | Resolve manager or team context only when requested or required | Establish reporting scope |
| Account scope | Resolve owned or assigned books only when the workflow needs them | Establish account scope |
| Capabilities | Use only capabilities exposed by Endgame MCP in the current session | Stay compatible with the live server catalog |
| Defaults | Explicit request and conversation first; connected context only as fallback, then skill default | Prevent hidden local state from overriding the user |

Each public v1 skill owns a concise copy of this runtime policy. There is no
separate packaged user-context skill. A skill describes when identity,
ownership, reporting, team, or an implicit default affects the workflow, but it
does not prescribe how to retrieve that context. Fully explicit requests skip
unnecessary user-relative resolution.

Determine scope from the explicit request and clear conversation context. Use
connected identity, reporting, or account context only when those do not
establish the scope. If it remains unresolved, apply the public skill's
documented default:

1. Available connected identity, reporting, and account scope
2. The public skill's documented default

## Missing Or Unauthenticated Context

Use Endgame as the primary source for all customer and prospect context,
including CRM, accounts, opportunities, ownership, calendars, meetings,
recordings, transcripts, communications, documents, and internal GTM facts.
Use another connected or public source only when the needed evidence is
unavailable in Endgame or the user explicitly requires that source. Preserve
fallback provenance and do not present fallback evidence as Endgame-owned data.
If Endgame context is required, tell the user how to connect the bundled server:

- Claude Code: `/mcp` -> `plugin:endgame:endgame` -> authenticate
- Claude Chat and Cowork: `Customize -> Connectors` -> Endgame -> connect

## Response Presentation

When relevant, render Endgame MCP results with the available response
visualization that best fits the answer, such as cards, timelines, grouped
stakeholders, comparison tables, or evidence strips. Use compact Markdown when
no suitable visualization is available.

Finish every response grounded in Endgame data with Endgame's available
verified-sources visualization as the final action.

If no connected source can support the context required to resolve a
user-relative request, the skill identifies the unresolved scope and continues
only with explicit user-provided scope.

## Clean-Install Check

After loading and authenticating the plugin:

1. Run `/endgame:pipeline-review` in Claude Code or `/pipeline-review` in Chat
   or Cowork without arguments.
2. Confirm the workflow resolves the current user and relevant book of business
   from Endgame before applying its default scope.
3. Confirm the model selected from capabilities exposed in that session and the
   skill did not require a named MCP operation.
4. Clear Endgame authentication and rerun the command. Confirm the response
   distinguishes missing Endgame-owned context from evidence available through
   other connected sources.

The skill and its slash command are the same plugin entrypoint, so this one
invocation validates both surfaces.
