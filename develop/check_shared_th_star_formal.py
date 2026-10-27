"""Local Lean contact-word classification, after memory/process preflight."""
import json
from pathlib import Path
import re
import subprocess

from check_unprotected_white_pair_formal import preflight

if not __debug__:
    raise RuntimeError('Run this verifier with assertions enabled')

ROOT = Path(__file__).resolve().parents[1]
NAMES = ['edge_partition','no_monochrome_iff','paired_counts','true_run',
         'false_run','blocked_counts','balanced_defects']


def main():
    check = preflight()
    run = subprocess.run(['lean','SubQuorum/SharedTHStar.lean'],
                         cwd=ROOT/'formal',text=True,capture_output=True)
    assert run.returncode==0 and not run.stderr,run.stdout+run.stderr
    assert not re.search(r'warning:|error:|sorryAx',run.stdout),run.stdout
    found = re.findall(
        r"'SubQuorum.SharedTHStar\.(\w+)' "
        r"(?:depends on axioms: \[([^\]]*)\]|does not depend on any axioms)",run.stdout)
    assert [name for name,_ in found]==NAMES
    theorems=[dict(theorem='SubQuorum.SharedTHStar.'+name,
                   axioms=[a.strip() for a in axs.split(',') if a.strip()])
              for name,axs in found]
    assert all(set(x['axioms'])<={'propext','Classical.choice','Quot.sound'} for x in theorems)
    result=dict(status='PASS',execution_location='local',
                command='cd formal && lean SubQuorum/SharedTHStar.lean',
                toolchain=(ROOT/'formal/lean-toolchain').read_text().strip(),
                preflight=check,theorems=theorems,stdout=run.stdout,stderr=run.stderr,
                scope='All finite Bool contact words: edge-count partition, no monochromatic pair iff alternation, all-s alternating and blocked word counts, run counts and conditional balanced endpoint arithmetic.',
                not_formalized='Original grid path/leaf fragment theorem, physical resource ownership adapter, actual all-word feasibility construction and individual-pair Hall projection remain written. Not end-to-end grid Lean.')
    (ROOT/'output/shared-th-star-formal.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(status='PASS',theorems=len(theorems))))


if __name__=='__main__':
    main()
