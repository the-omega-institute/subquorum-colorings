"""Local scoped Lean validation after memory and process preflight."""
import json
from pathlib import Path
import re
import subprocess

from check_unprotected_white_pair_formal import preflight

if not __debug__:
    raise RuntimeError('Run this verifier with assertions enabled')

ROOT=Path(__file__).resolve().parents[1]
NAMES=['strict_prefix_credit','prefix_credit_identity','inner_credit_bound',
       'local_cost_exact','sum_batch_balance','zero_cost_iff','batch_saving']


def main():
    check=preflight()
    run=subprocess.run(['lean','SubQuorum/DoubleContactCover.lean'],
        cwd=ROOT/'formal',text=True,capture_output=True)
    assert run.returncode==0 and not run.stderr,run.stdout+run.stderr
    assert not re.search(r'warning:|error:|sorryAx',run.stdout),run.stdout
    found=re.findall(r"'SubQuorum.DoubleContactCover\.(\w+)' "
        r"(?:depends on axioms: \[([^\]]*)\]|does not depend on any axioms)",run.stdout)
    assert [name for name,_ in found]==NAMES
    audits=[dict(theorem='SubQuorum.DoubleContactCover.'+name,
        axioms=[a.strip() for a in axs.split(',') if a.strip()]) for name,axs in found]
    assert all(set(x['axioms'])<={'propext','Classical.choice','Quot.sound'} for x in audits)
    out=dict(status='PASS',execution_location='local',
        command='cd formal && lean SubQuorum/DoubleContactCover.lean',
        toolchain=(ROOT/'formal/lean-toolchain').read_text().strip(),preflight=check,
        theorems=audits,stdout=run.stdout,stderr=run.stderr,
        scope='Ordered natural prefix-credit identity/minimum2/bound; arbitrary finite account lists with credit<=total give exact cost+credit sum and integer saving.',
        not_formalized='Actual grid prefixes/unique fragment ownership, range-minimum optimum, Hall and min-cost matching, all-size physical family and broader optimality remain written or open as explicitly stated.')
    (ROOT/'output/double-contact-formal.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(dict(status='PASS',theorems=len(audits))))


if __name__=='__main__':main()
