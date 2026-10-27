"""Local resource-ledger Lean check with measured memory/process preflight."""
import json
from pathlib import Path
import re
import subprocess

from check_unprotected_white_pair_formal import preflight

if not __debug__:
    raise RuntimeError('Run this verifier with assertions enabled')

ROOT = Path(__file__).resolve().parents[1]
NAMES = ['old_partition','new_partition','resource_ledger','signed_cost',
         'full_repair_cost','forest_full_repair_cost','no_increment_iff']


def main():
    check = preflight()
    run = subprocess.run(['lean','SubQuorum/ContactCycleLedger.lean'],
                         cwd=ROOT/'formal',text=True,capture_output=True)
    assert run.returncode == 0 and not run.stderr,run.stdout+run.stderr
    assert not re.search(r'warning:|error:|sorryAx',run.stdout),run.stdout
    found = re.findall(
        r"'SubQuorum.ContactCycleLedger\.(\w+)' "
        r"(?:depends on axioms: \[([^\]]*)\]|does not depend on any axioms)",run.stdout)
    assert [name for name,_ in found] == NAMES
    theorems = [dict(theorem='SubQuorum.ContactCycleLedger.'+name,
                    axioms=[a.strip() for a in axs.split(',') if a.strip()])
                for name,axs in found]
    assert all(set(t['axioms']) <= {'propext','Classical.choice','Quot.sound'} for t in theorems)
    out = dict(status='PASS',execution_location='local',
               command='cd formal && lean SubQuorum/ContactCycleLedger.lean',
               toolchain=(ROOT/'formal/lean-toolchain').read_text().strip(),
               preflight=check,theorems=theorems,stdout=run.stdout,stderr=run.stderr,
               scope='All finite resource-label lists: original/final partition, exact signed cost with bad/cycle exclusions, conditional full-repair/forest cost and no-increment iff cycle credit covers original bad resources.',
               not_formalized='Grid-to-unique-resource-list and permutation routing adapters, cycle-rank bound, normalization matching proof and all-length actual ladder construction remain written. No end-to-end geometric Lean.')
    (ROOT/'output/contact-cycle-formal.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(dict(status='PASS',theorems=len(theorems))))


if __name__ == '__main__': main()
