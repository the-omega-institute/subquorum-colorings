"""Local quantified ratio Lean check, with the required process/memory preflight."""
import json
from pathlib import Path
import re
import subprocess

from check_unprotected_white_pair_formal import preflight

if not __debug__:
    raise RuntimeError('Run this verifier with assertions enabled')

ROOT=Path(__file__).resolve().parents[1]
NAMES=['symbolic_ledger','quadratic_cost','positive_gap','linear_bound','ratio_bound','unbounded_ratio']


def main():
    check=preflight()
    run=subprocess.run(['lean','SubQuorum/FiveContactBarrier.lean'],
        cwd=ROOT/'formal',text=True,capture_output=True)
    assert run.returncode==0 and not run.stderr,run.stdout+run.stderr
    assert not re.search(r'warning:|error:|sorryAx',run.stdout),run.stdout
    found=re.findall(r"'SubQuorum.FiveContactBarrier\.(\w+)' "
        r"(?:depends on axioms: \[([^\]]*)\]|does not depend on any axioms)",run.stdout)
    assert [name for name,_ in found]==NAMES
    audits=[dict(theorem='SubQuorum.FiveContactBarrier.'+n,
        axioms=[a.strip() for a in axs.split(',') if a.strip()]) for n,axs in found]
    assert all(set(x['axioms'])<={'propext','Classical.choice','Quot.sound'} for x in audits)
    out=dict(status='PASS',execution_location='local',
        command='cd formal && lean SubQuorum/FiveContactBarrier.lean',
        toolchain=(ROOT/'formal/lean-toolchain').read_text().strip(),preflight=check,
        theorems=audits,stdout=run.stdout,stderr=run.stderr,
        scope='Exact symbolic two-cycle accounting; square-family cost expression; positivity and FOR EVERY integer K an explicit even L with C2>K*C5.',
        not_formalized='Domino embedding, simplicity/disjointness/feasibility, five-contact routing and structural all-proper-subset comparison remain written with actual physical controls. Not end-to-end grid Lean.')
    (ROOT/'output/five-contact-formal.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(dict(status='PASS',theorems=len(audits))))


if __name__=='__main__':main()
