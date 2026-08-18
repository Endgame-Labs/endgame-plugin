---
name: call-review
description: Review customer, prospect, partner, renewal, implementation, support, or sales calls using transcripts, recordings, summaries, CRM, and account context. Use when the user asks for call review, call coaching, transcript analysis, discovery quality, objections, customer pain, next steps, sales methodology inspection, messaging review, or what happened on a call.
argument-hint: "[call, meeting, or account]"
---

# Call Review

Analyze a call for what happened, what the customer revealed, how the team
performed, and what should happen next.

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
  Endgame's available verified-sources visualization as the final action. Treat
  a no-content conclusion established from an Endgame or calendar lookup as
  grounded data. Do not finish the response before the verification call
  succeeds.
- Use the transcript or recording summary available in Endgame as the primary
  call source. If neither is available in Endgame, use an available connected
  transcript, recording summary, or meeting notes. If no reliable call content
  is available, say that a reliable call review needs the transcript or notes.
- Connect the call to available account, opportunity, stakeholder, prior
  meeting, and CRM evidence when it improves the review.
- Distinguish direct customer statements from rep interpretation and your own
  recommendations.
- Quote only short excerpts that are necessary to preserve customer language.
- Do not fabricate attendee names, objections, commitments, or sentiment.

## Workflow

1. Resolve the target call:
   - Account, call title, date, attendees, transcript or summary, linked CRM
     record, and user goal for the review
2. Extract from the reliable call content:
   - Agenda and actual topics covered
   - Customer goals, pain, urgency, decision process, and constraints
   - Objections, competitors, budget, timing, security, legal, or procurement
     issues
   - Commitments, next steps, owners, and dates
   - Product feedback and evidence-worthy quotes
   - Rep questions, talk tracks, and missed opportunities
3. Produce the requested review. If the user does not specify a focus, include
   summary, customer evidence, risks, coaching, and follow-up.

## Output Contract

Use this structure unless the user asks for a different format:

### Call Summary

Start with the call title and date, then summarize the call in 5 to 8
bullets. Include meeting purpose, customer priorities, decisions, and next
steps.

### Customer Signals

Group evidence into:

- Goals and desired outcomes
- Pain or blockers
- Buying process and decision criteria
- Timing and urgency
- Competitive or alternative solution mentions
- Product feedback

Include short source-backed snippets only where useful.

### Deal Or Account Impact

Explain how the call changes the account motion, opportunity health, renewal,
implementation, or support plan. Label recommendations as recommendations.

### Coaching Notes

For each coaching point, include:

- What happened
- Why it matters
- What to do differently next time
- Example language the rep could use

Balance strengths, missed opportunities, and concrete improvements.

### Follow-Up Plan

List customer-facing follow-up, internal actions, CRM updates, stakeholder
engagement, and open questions. Include owners and due dates when stated.

## Quality Bar

- Preserve the customer's actual meaning. Do not overfit one sentence into a
  broad conclusion.
- Avoid generic coaching. Tie every coaching note to call evidence.
- If the user asks for scoring, explain the rubric before assigning scores.
- If the call contains sensitive customer information, keep external drafts
  separate from internal analysis.
