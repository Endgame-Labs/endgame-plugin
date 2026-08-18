---
name: pipeline-review
description: Review active GTM pipeline for reps, managers, teams, segments, regions, accounts, or time periods. Use when the user asks for pipeline review, forecast inspection, deal risk, slip risk, close plan review, priority accounts, quarter plan, manager inspection, or which deals need attention, grounded in connected CRM, activity, meeting, call, stakeholder, and account context.
argument-hint: "[owner, team, segment, or period]"
---

# Pipeline Review

Inspect pipeline health, identify the deals that need action, and produce a
practical forecast and execution plan.

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
- Completion gate: after producing a response grounded in Endgame data, call
  Endgame's available verified-sources visualization as the final action. Do
  not finish the response before that call succeeds.
- Default to the user's open pipeline for the current quarter when no scope is
  specified. For managers, include team pipeline if the user asks about a team
  or forecast rollup.
- When the default resolves to one unambiguous owner and period, begin the
  review without asking for confirmation. Ask a scope question only when the
  available context yields multiple materially different valid scopes.
- Do not change CRM records. Draft suggested updates instead.
- Do not present forecast changes as facts unless the source data supports them.
  Label recommendations clearly.
- When data is incomplete, identify the missing field or source and explain the
  impact on confidence.
- Track each decision-critical opportunity field as one of: `Returned value`,
  `Confirmed source blank`, `Not returned`, or `Conflicting values`. A field
  absent from available evidence is `Not returned`; it is not proof that the
  source field is blank.
- Recommend cleanup for a blank or stale field only when authoritative evidence
  confirms the source value. Otherwise state that the field was not retrieved
  or remains unverified and omit the cleanup claim.

## Workflow

1. Resolve scope:
   - Owner, team, region, segment, account list, opportunity list, forecast
     category, close-date window, and currency where available
2. Establish the decision-critical opportunity data:
   - Account, opportunity name, amount, stage, forecast category, close date,
     owner, next step, last activity, created date, stage age, probability, type,
     and relevant custom fields
3. Enrich priority deals with context:
   - Recent and upcoming meetings
   - Call summaries and transcripts
   - Stakeholder coverage
   - Activity recency
   - Product, legal, security, procurement, implementation, or support signals
4. Segment the pipeline:
   - Commit or high-confidence deals
   - Best case or upside
   - At-risk deals
   - Stale or low-quality pipeline
   - Deals needing qualification or cleanup
5. Produce a review that moves from portfolio-level summary to deal-level action.

## Output Contract

Use this structure unless the user asks for a different format:

### Pipeline Summary

Report scoped totals such as open pipeline, commit, best case, weighted
pipeline, deal count, close-date distribution, and coverage. Use `Not returned`
when available evidence omitted a field. Use `Confirmed source blank` only when
authoritative source evidence confirms that the field has no value.

### Forecast Read

Give a concise judgment on whether the scope looks healthy, exposed, or
overstated. Explain the evidence and confidence level.

### Deal Risk Table

Create a table with:

- Account
- Opportunity
- Amount
- Stage
- Forecast category
- Close date
- Risk level
- Main evidence
- Recommended action

Prioritize by materiality, close date, and risk.

### Priority Actions

List the highest-leverage actions for the user or manager this week. Include
owner, target account, next action, why it matters, and expected impact.

### Coaching Or Inspection Notes

For manager or leadership reviews, include observations about process health:

- Stage hygiene
- Forecast discipline
- Stakeholder coverage
- Next-step quality
- Activity gaps
- Deal concentration

### CRM Cleanup Suggestions

List verified stale close dates, confirmed missing next steps, confirmed blank
forecast categories, duplicate or ambiguous opportunities, and fields that
should be updated. Keep these as draft suggestions, not executed changes.
Separate `Verified source cleanup` from `Needs field verification`; never turn a
missing or partial result into a confirmed CRM cleanup recommendation.

## Quality Bar

- Focus on decisions and actions, not just summarizing pipeline rows.
- Rank risk by evidence, not by gut feel.
- Avoid overprecision when CRM fields are stale or missing.
- Distinguish confirmed source-system blanks from gaps in available evidence.
- Keep manager-facing output concise enough for forecast meetings.
