---
name: account-brief
description: Produce a source-backed account brief for GTM work. Use when the user asks for an account overview, account brief, account research, account prep, account strategy snapshot, or a concise customer/prospect briefing grounded in connected account, opportunity, contact, activity, meeting, call, document, and public context.
argument-hint: "[account name or domain]"
---

# Account Brief

Create a concise account brief that helps a GTM user understand what matters,
why it matters now, and what to do next.

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
- When relevant, render Endgame MCP results with the available response
  visualization that best fits the answer, such as cards, timelines, grouped
  stakeholders, comparison tables, or evidence strips. Use compact Markdown
  when no suitable visualization is available.
- Finish every response after an Endgame lookup with Endgame's available
  verified-sources visualization as the final action. Apply this completion
  gate to successful, partial, empty, and failed lookups.
- Say exactly which sections are limited when a required source class cannot be
  reached. Do not invent internal account facts.
- Assign stakeholder authority only from direct evidence of decision rights,
  approval behavior, or an explicit opportunity role. For a title-only or
  indirectly mentioned person, state `Authority unconfirmed; outside known
  decision flow` and describe only the observed evidence.
- Mention a title-only or indirectly mentioned person only once, in `People And
  Relationships`. In every other section, refer to the observed need or unknown
  function without naming that person—for example, `CFO-facing adoption story`
  or `Finance approval: approver not identified`.
- Treat `real budget authority`, `actual signer`, `named financial approver`,
  `likely final approver`, `likely economic buyer`, `controls the finance
  decision`, and `renewal needs their sign-off` as unsupported authority
  assignments unless direct evidence establishes that exact role. An
  `Inference`, `Likely`, or `Possible` label does not make an unsupported
  authority assignment acceptable.
- When the evidence establishes a finance step but not its owner, write
  `Finance approval: approver not identified`. Recommend that an evidenced
  stakeholder identify the approval owner instead of assigning the function to
  a title-only or indirectly mentioned person. Target the evidenced stakeholder
  in that action; do not name the unclassified person as a target, candidate, or
  possible approver, including in a question such as `Is [person] the actual
  approver?`.
- Completion gate: before calling verified sources, scan the complete rendered
  answer, including visualization fields, Markdown, and any recap. For every
  title-only or indirectly mentioned person, keep the single canonical entry in
  `People And Relationships` and replace every other name occurrence with the
  observed need or unknown function. Remove every authority assignment from the
  canonical entry.
- Prefer concrete names, dates, opportunity fields, source titles, and observed
  customer language over generic sales advice.
- Ask a clarification question only when the account cannot be resolved from
  the user's request or available context.

## Workflow

1. Resolve the target account and any requested time frame, segment, region, or
   opportunity scope.
2. Establish the account context needed for the brief:
   - CRM account and opportunity fields
   - Contacts, roles, seniority, ownership, and recent engagement
   - Recent and upcoming meetings
   - Call transcripts, summaries, notes, and action items
   - Customer-facing and internal documents
   - Relationship, usage, support, renewal, or implementation signals when
     available
3. Add current external company, market, or regulatory context when it changes
   the GTM approach.
4. Reconcile conflicting facts by comparing recency and support, and make
   unresolved conflicts visible.
5. Produce the brief using the output contract.

## Output Contract

Use this structure unless the user asks for a different format:

### Executive Take

Write 3 to 5 bullets that state the account situation, active motion, most
important risk or opportunity, and recommended next move.

### Account Snapshot

Include account basics such as company description, segment, owner, customer or
prospect status, open opportunity value, renewal or close timing, and relevant
strategic context. Mark unavailable fields as `Not found`.

### Current GTM Motion

Summarize active opportunities, recent meetings, known use cases, customer
priorities, blockers, procurement or legal status, implementation status, and
next steps. Separate confirmed facts from inference.

### People And Relationships

List the known stakeholders, evidence-backed roles, seniority, engagement
level, last meaningful interaction, and observed relevance to the account
motion. Call out coverage gaps. Render unconfirmed authority using the exact
evidence state defined in the operating rules.

### Signals To Watch

Group signals into:

- Positive momentum
- Risks or blockers
- Open questions

Each signal must include evidence or an explicit `Inference` label.

### Recommended Actions

Give 3 to 5 specific next actions. For each action, include owner role, target
stakeholder or account area, suggested message angle, urgency, and evidence.

## Quality Bar

- Keep the brief concise enough to read before a customer interaction.
- Avoid boilerplate industry summaries unless they change the GTM approach.
- Do not bury critical risks. Put them in the Executive Take.
- Do not include sensitive internal claims in externally shareable wording
  unless the user explicitly asks for an internal brief.
