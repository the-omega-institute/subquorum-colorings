"""Run the abstract repeated-surgery resource kernels locally, after preflight."""
import json
from pathlib import Path
import re
import subprocess

from check_unprotected_white_pair_formal import preflight

if not __debug__:
    raise RuntimeError('Run this verifier with assertions enabled')

ROOT = Path(__file__).resolve().parents[1]
NAMES = ['arm_rewire', 'context_rewire', 'surgery_perm', 'surgery_nodup',
         'incremental_cost', 'batch_residuals', 'family_ledger']


def main():
    check = preflight()
    run = subprocess.run(['lean', 'SubQuorum/OrderedTHRelay.lean'],
                         cwd=ROOT/'formal', text=True, capture_output=True)
    assert run.returncode == 0 and not run.stderr, run.stdout+run.stderr
    assert not re.search(r'warning:|error:|sorryAx', run.stdout), run.stdout
    found = re.findall(
        r"'SubQuorum.OrderedTHRelay\.(\w+)' "
        r"(?:depends on axioms: \[([^\]]*)\]|does not depend on any axioms)", run.stdout)
    assert [name for name, _ in found] == NAMES
    theorems = [dict(theorem='SubQuorum.OrderedTHRelay.'+name,
                     axioms=[a.strip() for a in axioms.split(',') if a.strip()])
                for name, axioms in found]
    assert all(set(x['axioms']) <= {'propext', 'Classical.choice', 'Quot.sound'}
               for x in theorems)
    result = dict(status='PASS', execution_location='local',
                  command='cd formal && lean SubQuorum/OrderedTHRelay.lean',
                  toolchain=(ROOT/'formal/lean-toolchain').read_text().strip(),
                  preflight=check, theorems=theorems, stdout=run.stdout, stderr=run.stderr,
                  scope='Four-arm resource-list permutation with context; arbitrary finite ResourceSurgery preserves permutation and Nodup; conditional exact incremental cost, batch residual and family arithmetic.',
                  not_formalized='Actual grid path decomposition, adapter from physical edges to four arm lists, necessity/sufficiency of gate order, component-disjoint chain assembly and coordinate examples remain written. No end-to-end grid theorem.')
    (ROOT/'output/ordered-th-relay-formal.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(dict(status='PASS', theorems=len(theorems))))


if __name__ == '__main__':
    main()
