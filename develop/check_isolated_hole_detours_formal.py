"""Run nine scoped Lean kernels locally, with process/memory preflight."""
import json
from pathlib import Path
import re
import subprocess

from check_unprotected_white_pair_formal import preflight

if not __debug__:
    raise RuntimeError('Run this verifier with assertions enabled')

ROOT = Path(__file__).resolve().parents[1]
NAMES = ['centre_neighbour_in_P', 'square_capacity',
         'unrestricted_disjoint_capacity', 'singleton_colour_obstruction',
         'exact_mixed_margin', 'padded_footprint_bound', 'exact_adjacent_defect',
         'outer_L_distance', 'unbounded_relay_cost']


def main():
    check = preflight()
    run = subprocess.run(['lean', 'SubQuorum/IsolatedHoleDetours.lean'],
                         cwd=ROOT/'formal', text=True, capture_output=True)
    assert run.returncode == 0 and not run.stderr, run.stdout+run.stderr
    assert not re.search(r'warning:|error:|sorryAx', run.stdout), run.stdout
    found = re.findall(
        r"'SubQuorum.IsolatedHoleDetours\.(\w+)' "
        r"(?:depends on axioms: \[([^\]]*)\]|does not depend on any axioms)", run.stdout)
    assert [name for name, _ in found] == NAMES
    theorems = [dict(theorem='SubQuorum.IsolatedHoleDetours.'+name,
                     axioms=[a.strip() for a in axioms.split(',') if a.strip()])
                for name, axioms in found]
    assert all(set(x['axioms']) <= {'propext', 'Classical.choice', 'Quot.sound'}
               for x in theorems)
    result = dict(status='PASS', execution_location='local',
                  command='cd formal && lean SubQuorum/IsolatedHoleDetours.lean',
                  toolchain=(ROOT/'formal/lean-toolchain').read_text().strip(),
                  preflight=check, theorems=theorems, stdout=run.stdout, stderr=run.stderr,
                  scope='Actual centre-neighbour coordinates; local square capacity; arbitrary-list disjoint capacities; integer colour obstruction and exact margin/footprint/defect arithmetic; arbitrary-k outer-L distance and alternating-path actual-edge cost, with explicit hypotheses.',
                  not_formalized='Periodic disjoint coordinate cover, all forced-hole classification, fractional conservation, feasible sharp selections, square/path assembly, arbitrary-selection DP and geometric minimum-relay-edge proof remain written mathematics with computational controls.')
    (ROOT/'output/isolated-hole-detours-formal.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(dict(status='PASS', theorems=len(theorems))))


if __name__ == '__main__':
    main()
