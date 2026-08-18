---
name: stakeholder-map
description: Build or update a stakeholder map for an account, opportunity, renewal, implementation, buying committee, executive relationship, or deal team. Use when the user asks who is involved, who to engage, relationship coverage, champion or economic buyer gaps, power map, stakeholder plan, persona map, or threading strategy grounded in connected contacts, CRM roles, meetings, calls, communications, documents, and public context.
argument-hint: "[account or opportunity]"
---

# Stakeholder Map

Map the people who matter in an account motion, explain the evidence behind
their roles, and recommend how to improve relationship coverage.

## Operating Rules

- Determine scope from the explicit request and conversation context. Use
  connected context only when those do not establish it, then apply this skill's
  documented default if scope remains unresolved.
- Use Endgame as the primary source for all customer and prospect context,
  including CRM, account, opportunity, ownership, calendar, meeting, recording,
  transcript, communication, document, and internal GTM facts.
- Use another connected or public source only when the needed evidence is
  unavailable in Endgame. When falling back, preserve source provenance,
  identify any remaining limits, and do not present one source as equivalent to
  another.
- Do not render Endgame MCP results with the available response visualization
  for stakeholder maps. Use compact Markdown so role classification stays in
  one output surface.
- Finish every response grounded in Endgame data with Endgame's available
  verified-sources visualization as the final action.
- Assign authority and influence only from direct evidence of decision rights,
  approval behavior, or an explicit opportunity role. A title or indirect
  mention is insufficient.
- Label every title-only or indirectly mentioned person `Unclassified
  stakeholder — specific authority unconfirmed; outside known decision flow`.
  If the person is named anywhere in the response, repeat this exact label
  verbatim; do not paraphrase or strengthen it.
- Never affirm or imply that a title-only or indirectly mentioned person is the
  `actual approver`, `ultimate approver`, `final approver`, `likely approver`,
  `approval gate`, `signer`, `economic buyer`, `budget holder`, or `decision
  maker`, or that the person owns sign-off. Never claim that the person
  influences, shapes, or controls approval, or needs to be satisfied or won
  over for approval, unless direct evidence establishes that influence. This
  prohibition includes hedged assignments such as `likely economic buyer` or
  `approver, unconfirmed`.
- Never infer from title that the person `sits`, `may sit`, or `appears
  somewhere` in an approval or decision path. A later uncertainty caveat does
  not cure that initial placement. State only the observed title and that the
  person's role and path are unknown.
- Negations, unknown-state statements, and questions or actions to identify or
  confirm the role are valid. For example, `No confirmed economic buyer`,
  `The contact's authority is unknown`, and `Ask an evidenced stakeholder to
  confirm the contact's actual involvement` preserve uncertainty rather than
  assigning authority.
- An observed statement that a champion needs an adoption story for a finance
  audience is valid. Treat it only as the champion's stated content need; it
  does not establish that a title-only contact influences approval, must be
  satisfied, or holds any approval role.
- Refer to a missing finance function as `Finance approval: Unknown — approver
  not identified`.
- Before the final verified-sources action, scan every statement about a
  title-only or indirectly mentioned person. Replace any affirmative or hedged
  authority assignment, known-flow placement, approval-influence claim, or
  claim that the person must be satisfied or won over with the exact canonical
  label.
- Render an unverified approval step as `Finance approval: Unknown — approver
  not identified` and keep every unclassified person outside that flow. Use
  this exact phrase for the unknown function; do not assign it a likely role.
- Keep personal data relevant to the GTM task. Avoid unnecessary biographical
  detail.
- If the user asks for an externally shareable version, remove internal
  relationship commentary and sensitive notes.
- Ask for clarification only when the target account or opportunity cannot be
  resolved.

## Workflow

1. Resolve the account, opportunity, renewal, implementation, or target segment.
2. Gather stakeholder evidence:
   - CRM contacts, contact roles, account team notes, and opportunity roles
   - Meeting attendees and call speakers
   - Email or activity history when available
   - Document mentions and mutual action plans
   - Current public role and company context when useful
3. Classify stakeholders by their observed or likely function:
   - Economic buyer
   - Champion
   - Decision maker
   - Technical evaluator
   - Legal or procurement
   - Executive sponsor
   - User or practitioner
   - Detractor or blocker
   - Unknown or unclassified
4. Assess coverage gaps and relationship risk:
   - Missing roles
   - Single-threaded relationships
   - Stale engagement
   - Unvalidated champion
   - Executive access gaps
   - Procurement, legal, or security not yet engaged
5. Recommend a threading plan.

## Output Contract

Use this structure unless the user asks for a different format:

### Stakeholder Summary

Give a short read on relationship health, known power structure, critical gaps,
and immediate engagement priority. Refer to unverified roles by function only;
do not name unclassified people here.

### Stakeholder Table

Create a table with:

- Name
- Title
- Organization or department
- Role in motion
- Engagement level
- Last meaningful interaction
- Evidence
- Recommended next move

Use `Unknown` or `Not found` rather than guessing.

### Influence And Coverage Map

Describe the buying committee or account network in plain language. Identify
single-threaded areas, executive gaps, technical gaps, and likely decision flow.
Leave unknown steps unnamed and keep unclassified people outside the flow.

### Relationship Risks

List the top risks with evidence:

- Missing economic buyer
- Weak or unvalidated champion
- Key stakeholder inactive
- Procurement or legal not engaged
- Detractor or blocker present
- No recent executive contact

Refer to unverified roles by function only; do not name unclassified people.

### Threading Plan

Recommend 3 to 6 specific outreach or engagement moves. Include target person,
owner role, suggested message angle, purpose, and source-backed rationale.
For an unverified function, target an evidenced stakeholder who can identify
the correct person; do not target an unclassified person.

## Quality Bar

- Make uncertainty visible. A stakeholder map is worse when false confidence
  hides gaps.
- Keep recommendations practical and tied to the user's next account motion.
- Do not use a title alone as proof of buying authority.
- Highlight missing data that Endgame or CRM hygiene should fix.
