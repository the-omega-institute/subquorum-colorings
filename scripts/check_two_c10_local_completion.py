#!/usr/bin/env python3
"""Run finite checks supporting the two-C10 local completion note."""

from __future__ import annotations

import json
import random
from collections import Counter
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from develop.two_c10_local_completion import (  # noqa: E402
    classify_contact,
    four_phase_repair_certificate,
    perfect_matchings,
    physical_sample,
)


def main():
    contacts = list(perfect_matchings(range(10)))
    classes = [classify_contact(contact) for contact in contacts]
    cross_histogram = Counter(item.cross_edges for item in classes)
    exceptional = [item for item in classes if not item.both_cycles_good]
    assert cross_histogram == Counter({1: 225, 3: 600, 5: 120})
    assert len(exceptional) == 10
    assert all(item.owner0_bad_solution for item in exceptional)
    assert all(item.owner1_bad_solution for item in exceptional)
    assert all(
        item.both_cycles_good or item.cross_edges == 5 for item in classes
    )

    rng = random.Random(20261113)
    phase_samples = []
    for _ in range(2500):
        left = contacts[rng.randrange(len(contacts))]
        right = contacts[rng.randrange(len(contacts))]
        certificate = four_phase_repair_certificate(left, right)
        assert certificate is not None
        phase_samples.append(certificate["average"])

    physical = [
        physical_sample(k, 20261113 + k, models)
        for k, models in ((0, 25), (1, 25), (2, 15), (3, 8))
    ]
    report = {
        "status": "PASS",
        "scope": {
            "contact_matchings": len(contacts),
            "cross_edge_histogram": dict(sorted(cross_histogram.items())),
            "exceptional_contact_matchings": len(exceptional),
            "phase_pair_samples": len(phase_samples),
            "maximum_sampled_four_state_average": max(phase_samples),
            "physical_controls": physical,
        },
        "theorem_scope": "The written local lemma is general; physical controls are finite checks and do not audit the C20 global absorption argument.",
    }
    output = ROOT / "output/two-c10-local-completion-check.json"
    output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
