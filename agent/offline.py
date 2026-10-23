"""Offline fixtures. FakeDecider derives from the Apache-2.0 kit tests/fakes.py.

See LICENSES/Apache-2.0-kit.txt and NOTICE; new writer/fixtures are MIT.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from decider_kit.client import Decision


class FakeDecider:
    def __init__(self, rule: Callable[[str, str, dict[str, Any]], Any] | None = None):
        """rule(state, name, question) -> P(yes) for noul, an option name for choice/score."""
        self.rule = rule or (lambda s, n, q: 0.9 if q["type"] == "noul" else next(iter(q["criteria"])))
        self.calls: list[tuple[str, dict]] = []
        self.last_latency_ms = 12.0
        self.last_server_ms = 10.0
        self.url = "fake://decider"

    def ask(self, state: Any, questions: dict[str, dict[str, Any]], images: Any = None) -> dict[str, Decision]:
        self.calls.append((state, questions))
        out = {}
        for name, q in questions.items():
            v = self.rule(state, name, q)
            if q["type"] == "noul":
                out[name] = Decision.parse({"type": "noul", "noul": float(v)})
            elif q["type"] == "choice":
                opts = list(q["criteria"])
                probs = {o: (0.85 if o == v else 0.15 / max(1, len(opts) - 1)) for o in opts}
                out[name] = Decision.parse({"type": "choice", "choice": v, "probabilities": probs, "confidence": 0.85})
            else:
                levels = q["criteria"]
                i = levels.index(v)
                probs = {str(k): (0.8 if k == i else 0.2 / max(1, len(levels) - 1)) for k in range(len(levels))}
                out[name] = Decision.parse({"type": "score", "score": float(i), "probabilities": probs,
                                            "legend": {str(k): l for k, l in enumerate(levels)}})
        return out

    def health(self) -> dict[str, Any]:
        return {"checkpoint": "fake"}


class FakeLLM:
    """Deterministic draft-only writer; no model or network initialized."""

    def __call__(self, message):
        import json

        lead = json.loads(message)
        return (f"Hi {lead.get('name', 'there')}, your signal at {lead.get('company', 'your company')} "
                f"stood out: {lead.get('notes', '')} Could we compare GTM priorities in a short conversation?")


def sample_decider():
    """Explicit synthetic fixture lookup, never a substitute for live qualification."""
    import json
    from pathlib import Path

    fixtures = json.loads((Path(__file__).parents[1] / "data/offline_fixtures.json").read_text())

    def rule(state, name, question):
        match = next((v for key, v in fixtures.items() if f"name: {key}\n" in state), None)
        if match is None:
            raise ValueError("No offline fixture for this lead")
        return match["stage"] if name == "stage_seniority" else match["p"]

    return FakeDecider(rule)
