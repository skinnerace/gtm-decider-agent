# GTM Decider Agent – Signal to Story Router

Turn inbound founder and recruiter signals into a useful GTM next step. Strands Decider 2B
gates outreach; Amazon Bedrock Nova Pro writes a short personalized draft only for PRIORITY
leads. WARM gets a nurture suggestion, SKIP avoids generation, and nothing is ever sent.

Built with the AWS User Group Madurai Strands Decider hackathon kit

Tags: #strands-decider-2b #policy

## Architecture

The chat wrapper invokes a Strands tool with the original lead evidence before any LLM call.
The tool asks the hosted ugmdu Decider all typed questions together. Python branches on
P(outreach_worthy), never generated text. Decisions are visible in the kit demo panel.

```text
JSON/text lead -> HackathonAgent.chat -> qualify_lead (@tool)
                                           |
                                    decider_kit.Decider
                                    hosted Strands Decider 2B
                                           |
                            Python probability thresholds + log
                             /             |              \
                      PRIORITY           WARM             SKIP
                          |                |                |
                  Strands Agent       fixed nurture      no generation
                  Bedrock Nova Pro    / human review
                          |
                    draft <=120 words (never sent)
```

See [DECISION_PATTERN.md](DECISION_PATTERN.md) and [agent/AGENT.md](agent/AGENT.md).
Memory and Gateway are disabled: independent leads need neither retained personal data
nor an external tool gateway. `HackathonAgent.chat` retains the kit's response contract.

## Setup

Use Python 3.12+ and the supplied environment in this workspace:

```bash
. /workspace/decider-hackathon/.venv/bin/activate
cd /workspace/decider-hackathon/build/gtm-decider-agent
# For a fresh environment only: python -m pip install -r requirements.txt
cp .env.example .env
```

For live use, edit .env locally with a hosted `DECIDER_API_KEY` and configure AWS credentials
through the normal AWS credential chain. Never commit credentials. Environment variables
win over .env. Defaults: `DECIDER_MODE=ugmdu`, hosted `DECIDER_URL` from .env.example,
`BEDROCK_MODEL_ID=us.amazon.nova-pro-v1:0`, `AWS_REGION=us-east-1`,
`PRIORITY_THRESHOLD=0.70`, `WARM_THRESHOLD=0.50`. The agent explicitly selects Bedrock
through `decider_kit.llm.agent_model`; the benchmark also uses `LLM_PROVIDER=bedrock`.

## Run

Offline, with no credentials or network:

```bash
python -m agent.qualify --input data/sample_leads.jsonl --dry-run
```

This is a deterministic simulation using fake Decider probabilities and a fake writer,
shared with the tests. Twelve clearly fictional leads cover all branches. It writes
`results/dry_run.jsonl`. Fixtures are not a benchmark or evidence of live accuracy.

Live, after configuring credentials and Nova Pro access:

```bash
python -m agent.qualify --input data/sample_leads.jsonl
python -m agent.agent '{"name":"Avery Example","title":"Founder","company":"Acme Robotics (fictional)","notes":"Paying customers, needs GTM help"}'
./kit demo
```

The CLI writes ignored `results/qualified.jsonl`; keep real lead files in ignored `leads/`.
The UI accepts the same JSON or free-text evidence. No email or messaging integration exists.

## Verification and benchmark

```bash
python -m pytest -q
ruff check agent tests/fakes.py tests/test_lead_router.py
# Live calls, when ready; not run during this build:
./kit bench --split tune
./kit bench --split test
```

The 24 synthetic labeled cases use the runtime state layout with separate tune/test evidence.
The kit benchmark compares typed question labels; its accuracy is not three-way route accuracy.
No live accuracy, latency, cost or deployment claims are made by this offline build.

## AgentCore deployment

Follow [deploy/AGENTCORE.md](deploy/AGENTCORE.md). The kit's `scripts/deploy.py` packages
`agent/` and `decider_kit/`, passes the hosted endpoint, secret, thresholds, region and model
environment to the runtime, and provisions only enabled features. Use Node 20+ and the
AgentCore CLI, AWS credentials and Bedrock model access. The hosted Decider must be reachable
from AWS. When ready, these commands perform live operations:

```bash
./kit deploy                       # same entrypoint as python scripts/deploy.py deploy
./kit invoke 'Avery Example at Acme Robotics (fictional): paying customers, needs GTM help'
./kit video --target agentcore
./kit destroy                      # clean up after judging
```

Deployment, benchmark, video and publication were deliberately not executed here.
`submission/README.md` lists the remaining author-produced artifacts.

## Licensing

Author's new code in `agent/`, new lead tests, synthetic data, agent specification and project
documentation: MIT, Copyright (c) 2026 Doug Skinner, in [LICENSE](LICENSE).
Kit-derived files, including `decider_kit/`, `demo/`, `deploy/`, `scripts/`, existing tests,
`.kiro/` tooling, and build wrappers retain Apache-2.0 in
[LICENSES/Apache-2.0-kit.txt](LICENSES/Apache-2.0-kit.txt) and [NOTICE](NOTICE).
Rewritten agent files replace the original implementation; shared offline FakeDecider remains
kit-derived Apache-2.0. Both licenses are OSI-approved. AWS User Group Madurai provides the
kit and reusable library; the Signal to Story Router is Doug Skinner's agent.
