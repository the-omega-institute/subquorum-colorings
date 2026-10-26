"""Validate guarded-hole exclusions, partner injection and arbitrary-length slots."""
import argparse
import json
from pathlib import Path
import re
import subprocess

from check_unprotected_white_pair_formal import preflight

if not __debug__:
    raise RuntimeError('Run this verifier with assertions enabled')

ROOT = Path(__file__).resolve().parents[1]
NAMES = ['two_endpoints_exclude_selection', 'guarded_pair_exclusion', 'partner_injective', 'selected_partner_is_hole', 'all_length_slot_bound', 'exact_hole_margin', 'fixed_footprint_bound']


def audit_output(stdout, stderr, returncode):
    assert returncode == 0 and not stderr, stdout + stderr
    assert not re.search(r'warning:|error:|sorryAx', stdout), stdout
    found = re.findall(
        r"'SubQuorum.GuardedHoleCover\.(\w+)' "
        r"(?:depends on axioms: \[([^\]]*)\]|does not depend on any axioms)", stdout)
    assert [name for name, _ in found] == NAMES
    result = [dict(theorem='SubQuorum.GuardedHoleCover.' + name,
                   axioms=[a.strip() for a in axioms.split(',') if a.strip()])
              for name, axioms in found]
    assert all(set(r['axioms']) <= {'propext', 'Classical.choice', 'Quot.sound'}
               for r in result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, default=ROOT/'output/guarded-hole-cover-formal.json')
    args = parser.parse_args()
    check = preflight()
    run = subprocess.run(['lean', 'SubQuorum/GuardedHoleCover.lean'],
                         cwd=ROOT/'formal', text=True, capture_output=True)
    theorems = audit_output(run.stdout, run.stderr, run.returncode)
    result = dict(status='PASS', execution_location='local',
                  command='cd formal && lean SubQuorum/GuardedHoleCover.lean',
                  toolchain=(ROOT/'formal/lean-toolchain').read_text().strip(),
                  theorems=theorems, stdout=run.stdout, stderr=run.stderr,
                  preflight=check,
                  scope='Occupied-neighbour exclusions, guarded-pair partner injection, all-length slot bound and exact hole-margin arithmetic; hypotheses explicit.',
                  not_formalized='Actual grid-coordinate cover, disjoint partner construction, arbitrary-width matching uniqueness, no-endpoint-certificate cut and selection-relocation assembly remain written proofs.')
    args.output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(dict(status='PASS', theorems=len(theorems))))


if __name__ == '__main__':
    main()
