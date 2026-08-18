---
name: meeting-prep
description: Prepare a GTM user for a customer, prospect, partner, renewal, implementation, or internal account meeting. Use when the user asks to prep for a meeting, get a pre-read, identify attendees, draft an agenda, generate discovery questions, or produce talking points grounded in calendar, CRM, call, meeting, document, stakeholder, and account context.
argument-hint: "[meeting, account, or time]"
---

# Meeting Prep

Prepare the user for a specific meeting with a short, source-backed brief and a
clear plan for how to use the time.

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
  stakeholders, comparison tables, or evidence strips. Make the visualization
  preserve the requested fields and this skill's Output Contract. Use compact
  Markdown when no suitable visualization is available.
- Finish every response grounded in Endgame data with Endgame's available
  verified-sources visualization as the final action.
- Resolve the actual meeting before preparing the brief. When exactly one
  upcoming meeting matches the account and requested timeframe, select it and
  prepare the brief without asking for confirmation.
- When multiple meetings match, present the distinct sourced candidates and ask
  the user to choose before drafting the brief. Treat that candidate list as an
  Endgame-grounded response and apply the verified-sources rule above.
- If the meeting cannot be found, ask for the meeting title, account, attendees,
  or time. Do not fabricate attendee or agenda details.
- Make the prep useful in the first 60 seconds: lead with what the user should
  know and say.

## Workflow

1. Identify the meeting:
   - Title, date, time, account, meeting type, attendees, organizer, and linked
     CRM record when available
   - Whether the meeting is upcoming, in progress, or a prep request for a
     future event not yet on the calendar
2. Determine the likely meeting objective from invite text, prior threads, CRM
   stage, recent commitments, and attendee roles.
3. Establish account and relationship context:
   - Active opportunity, renewal, expansion, implementation, or support motion
   - Recent meetings and calls
   - Open action items and unresolved questions
   - Stakeholder roles, influence, sentiment, and engagement gaps
4. Build the prep around decisions the user can make before the meeting:
   - What to confirm
   - What to ask
   - What to avoid
   - Who to engage
   - What outcome to drive

## Output Contract

Include every section or field the user explicitly requests. A response
visualization must carry that content; it must not replace the requested brief
with a generic timeline or summary. Use this structure unless the user asks for
a different format:

### Opening Line

Give one direct sentence the user can use to open the meeting or frame the call.

### Meeting Snapshot

Include title, time, account, attendees, likely objective, and linked opportunity
or customer motion. Mark unavailable fields as `Not found`.

### What Matters

List 3 to 6 bullets covering the highest-signal context from CRM, prior
meetings, customer commitments, risks, account changes, and stakeholder dynamics.

### Attendee Map

For each known attendee, include name, title, organization, likely role in the
conversation, relationship context, and what the user should learn or confirm.

### Recommended Agenda

Provide a practical agenda with time allocation when useful. Tie agenda items to
known objectives and open questions.

### Questions To Ask

Group questions by topic. Favor specific questions that test assumptions,
advance a deal, uncover buying process, or clarify next steps.

### Talk Tracks

Give concise talking points tailored to the account and attendee roles. Include
customer evidence or prior language only when source-backed.

### Risks And Watchouts

Call out sensitive topics, stale commitments, stakeholder gaps, competitive
pressure, timing risks, or areas where the user lacks context.

### Desired Exit

Define the ideal outcome, minimum acceptable outcome, next step to secure, and
who should own it.

## Quality Bar

- Keep the brief meeting-specific. Avoid generic account research that does not
  affect the conversation.
- Distinguish customer-stated goals from seller interpretation.
- Prefer fewer, sharper questions over a long discovery script.
- If the meeting is executive-facing, compress detail and emphasize business
  outcomes, risk, and decision process.
