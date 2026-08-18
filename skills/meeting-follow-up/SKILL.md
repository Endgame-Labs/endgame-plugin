---
name: meeting-follow-up
description: Generate source-backed follow-up after customer, prospect, renewal, implementation, partner, or internal account meetings. Use when the user asks for a recap, follow-up email, action items, CRM update, Slack update, mutual action plan, next-step plan, or notes from a meeting, transcript, call recording, or meeting summary.
argument-hint: "[meeting, account, or date]"
---

# Meeting Follow-Up

Turn a meeting into accurate follow-up artifacts that preserve commitments,
customer language, decisions, and next steps.

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
- Finish every response grounded in Endgame data with Endgame's available
  verified-sources visualization as the final action. Treat a no-content result
  established from an Endgame or calendar lookup as grounded data and verify
  the available source before finishing.
- If the user references "that meeting" or a relative time, resolve the actual
  meeting before drafting. Ask only if multiple matches remain.
- Separate what was explicitly said from inferred recommendations.
- Preserve evidence state: distinguish planned, committed, scheduled, and
  completed work. Keep an action pending unless a source explicitly confirms
  completion; a due date or current date is not completion evidence.
- Preserve stakeholder authority in every artifact you produce, including
  optional internal recaps, open follow-ups, and CRM drafts. Describe observed
  roles and explicit actions from the source. A title, indirect mention, or
  possible-role label does not establish decision, approval, budget, or
  signature authority. Never assign an authority-unconfirmed person as an
  actual, likely, ultimate, eventual, or final approver, signer, economic buyer,
  approval gate, or participant in the approval path. A later `unconfirmed`
  label, denial, or caveat does not cure that assignment. It is valid to state
  that a champion needs a finance-facing adoption story, identify a contact's
  title while saying their authority is unknown, ask an evidenced person to
  identify the owner, or describe a generic finance step whose owner remains
  unknown.
- Do not invent commitments, owners, deadlines, product promises, pricing, or
  legal positions.
- Make customer-facing drafts external-safe by default. Include only direct
  customer statements and external-safe commitments. Exclude evidence marked
  internal-only, internal risk framing, and internal deal strategy; put those
  in a clearly labeled internal section.

## Workflow

1. Resolve the meeting or call:
   - Title, account, date, attendees, recording/transcript, linked CRM record,
     and user role
   - Available call content, meeting notes, calendar details, account or
     opportunity context, and prior commitments or mutual action plan
2. Extract:
   - Decisions made
   - Customer priorities and stated pain
   - Objections or risks
   - Questions asked and answered
   - Open questions
   - Commitments, owners, and dates
   - Follow-up materials requested
3. Generate artifacts requested by the user. If the user did not specify a
   format, include the default output contract below.

## Output Contract

Use this structure unless the user asks for only one artifact:

### Customer-Facing Follow-Up Email

Draft a concise email with:

- Thank-you and meeting purpose
- 2 to 4 recap bullets in customer-safe language
- Confirmed next steps with owners and dates
- Open questions or materials to send
- Clear close

Do not include internal risk commentary or unsupported claims.

### Internal Recap

Summarize the meeting for the account team:

- What happened
- Why it matters
- Customer priorities
- Deal, renewal, implementation, or relationship impact
- Risks and blockers
- Recommended next actions

### Action Items

Create a table with owner, action, due date, source evidence, and status. Include
only explicit commitments in the table. Use `Owner needed` or `Date needed` only
when an explicit commitment omitted that field. Put inferred or recommended
follow-ups outside the table under `Open Follow-Ups`; do not turn them into
assigned action items.

### CRM Update

Draft a CRM-ready update with fields or sections the user can paste into the
opportunity or account record:

- Next step
- Stage or forecast implications, if evidence supports them
- Key contacts and roles
- Risks
- Close plan or renewal plan notes

## Quality Bar

- Preserve customer language when it matters, but quote sparingly.
- Keep email drafts short enough to send without heavy editing.
- Make every action item traceable to source evidence or explicitly label it as
  a recommendation.
- If the meeting had no usable source material, say so and ask the user to
  provide notes or a transcript.
