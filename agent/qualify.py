"""Batch qualification: python -m agent.qualify --input data/sample_leads.jsonl --dry-run."""

import argparse
import json
from pathlib import Path

from .agent import HackathonAgent


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)
    if args.dry_run:
        from .offline import FakeLLM, sample_decider

        agent = HackathonAgent(decider=sample_decider(), llm_factory=FakeLLM)
        print("OFFLINE SIMULATION — fixture probabilities, not model measurements")
    else:
        agent = HackathonAgent()
    leads = [json.loads(line) for line in args.input.read_text().splitlines() if line.strip()]
    dest = Path("results")
    dest.mkdir(exist_ok=True)
    output = dest / ("dry_run.jsonl" if args.dry_run else "qualified.jsonl")
    print(f"{'Name':24} {'Route':10} {'P(outreach)':12} Next step")
    with output.open("w") as stream:
        for lead in leads:
            result = agent.chat(json.dumps(lead))
            p = result["decisions"][0]["p_outreach"]
            score = "review" if p is None else f"{p:.2f}"
            print(f"{lead.get('name', 'Unknown'):24} {result['outcome']:10} {score:12} {result['reply']}")
            stream.write(json.dumps({"lead": lead, **result}) + "\n")
    print(f"Saved {len(leads)} results to {output}")


if __name__ == "__main__":
    main()
