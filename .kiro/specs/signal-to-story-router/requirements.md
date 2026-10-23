# Requirements

- WHEN inbound lead evidence arrives THE agent SHALL ask Strands Decider 2B whether it is
  outreach worthy BEFORE generating a draft.
- WHEN P(outreach_worthy) reaches the configured priority threshold THE agent SHALL draft
  at most 120 words through Strands paired with Amazon Bedrock Nova Pro.
- WHEN the probability is between the thresholds THE agent SHALL provide a fixed nurture line.
- WHEN below the warm threshold THE agent SHALL skip generation.
- WHEN Decider is unavailable or returns invalid probabilities THE agent SHALL route to
  WARM/human review and SHALL NOT generate an outreach draft.
- WHEN any branch completes THE agent SHALL expose its decision in the kit chat contract.
- WHEN dry-run is selected THE CLI SHALL use only offline fakes and synthetic fixtures.
- THE agent SHALL never send outreach or store a real key in code.
