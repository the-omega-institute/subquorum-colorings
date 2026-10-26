"""Validate explicit scalar capacities and arbitrary-length ownership forcing."""
import argparse
import json
from pathlib import Path
import re
import subprocess

from check_unprotected_white_pair_formal import preflight

if not __debug__:
    raise RuntimeError('Run this verifier with assertions enabled')

ROOT = Path(__file__).resolve().parents[1]
NAMES = ['local_charge_from_owner', 'endpoint_capacity', 'exact_resource_margin', 'half_area_from_resources', 'node_forces_next', 'forced_path', 'every_old_path_owner_changes']


def audit_output(stdout, stderr, returncode):
    assert returncode == 0 and not stderr, stdout + stderr
    assert not re.search(r'warning:|error:|sorryAx', stdout), stdout
    found = re.findall(
        r"'SubQuorum.TurningOwnership\.(\w+)' "
        r"(?:depends on axioms: \[([^\]]*)\]|does not depend on any axioms)", stdout)
    assert [name for name, _ in found] == NAMES
    result = [dict(theorem='SubQuorum.TurningOwnership.' + name,
                   axioms=[a.strip() for a in axioms.split(',') if a.strip()])
              for name, axioms in found]
    assert all(set(r['axioms']) <= {'propext', 'Classical.choice', 'Quot.sound'}
               for r in result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, default=ROOT/'output/turning-ownership-formal.json')
    args = parser.parse_args()
    check = preflight()
    run = subprocess.run(['lean', 'SubQuorum/TurningOwnership.lean'],
                         cwd=ROOT/'formal', text=True, capture_output=True)
    theorems = audit_output(run.stdout, run.stderr, run.returncode)
    result = dict(status='PASS', execution_location='local',
                  command='cd formal && lean SubQuorum/TurningOwnership.lean',
                  toolchain=(ROOT/'formal/lean-toolchain').read_text().strip(),
                  theorems=theorems, stdout=run.stdout, stderr=run.stderr,
                  preflight=check,
                  scope='Scalar actual-edge charge/resource arithmetic and arbitrary-length forced path induction with explicit local hypotheses.',
                  not_formalized='Hall theorem application, tile/endpoint adapter, actual coordinate families and square-exchange assembly remain written proofs.')
    args.output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(dict(status='PASS', theorems=len(theorems))))


if __name__ == '__main__':
    main()
