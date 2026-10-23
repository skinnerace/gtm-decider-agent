# GTM Decider Agent – Signal to Story Router

Pitch: Turn inbound founder and recruiter signals into prioritized, draft-only GTM next steps.

Features: calibrated lead gate; original evidence in each decision log; personalized notes
only for PRIORITY; fixed nurture suggestions for WARM; no generation for SKIP; offline CLI.

For Doug Skinner and GTM advisors reviewing inbound prospects. Inputs are name, title,
company and notes, with optional founder/recruiter type. JSON is preferred; chat also accepts
plain evidence text. Data shipped here is synthetic; nothing is sent.

Decision: #policy — Inbound lead gate. Strands Decider 2B estimates outreach worthiness,
stage/seniority and GTM need together. Code routes on P(outreach_worthy), preserving the
prototype's 0.70 and 0.50 defaults. Failure means WARM/human review. The other answers
provide context rather than additional gates. Amazon Bedrock Nova Pro, through a real
Strands Agent and decider_kit.llm, drafts only PRIORITY notes, capped at 120 words.
Memory is off because leads are independent; Gateway is off because one local tool suffices.
