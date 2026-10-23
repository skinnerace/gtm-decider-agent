# #policy — Inbound lead gate

## Question + options

Should this inbound founder or recruiter be PRIORITY, WARM or SKIP for GTM advisory
outreach? `QUESTIONS` in `agent/decision.py` asks `outreach_worthy` (noul yes/no),
`stage_seniority` (choice: idea_early, growth, established, junior, mid, senior_leader,
unknown), and `gtm_need` (noul yes/no). Each option has an evidence-based description.
All questions share one state and one Decider call. Recruiter GTM hiring focus is represented
by `gtm_need`, adapting the prototype's `gtm_focus`.

## How it's wired

`HackathonAgent.chat` passes the original input to the Strands `qualify_lead` tool;
`LeadGate.qualify` calls `decider_kit.Decider.ask(state, QUESTIONS)`. This pre-agent seam
prevents generated arguments from changing the evidence. `lead_state` is shared with eval
case construction. Every call logs questions/options, probability distributions, thresholds,
outcome/verdict and latency for the kit demo panel.

Code routes only on calibrated P(outreach_worthy): >=0.70 PRIORITY; >=0.50 WARM; otherwise
SKIP. Set `PRIORITY_THRESHOLD` and `WARM_THRESHOLD` in the environment or .env;
0 <= warm < priority <= 1 is enforced. Stage/seniority and GTM need are explanatory context.
If Decider is unavailable or its response is invalid, route to WARM/human review with
no outreach draft. WARM receives a fixed nurture line. SKIP uses no LLM. PRIORITY alone
constructs a Strands Agent with a Bedrock model and drafts at most 120 words; nothing sends.

## Short note

Language signals require judgment: a hiring mandate or sales problem cannot be reliably
inferred by a numeric rule. A calibrated decision model supplies probabilities for an explicit,
auditable policy; an LLM's prose never chooses the branch. Nova Pro handles the story after
the decision. This is one #policy pattern; skipping generation is a consequence of the gate.
Reuse by changing the evidence rubric and tuning thresholds on the tune split. The test
split remains held out. Offline fixtures prove wiring, not real model accuracy or calibration.
