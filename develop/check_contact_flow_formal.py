"""Compile scoped ContactFlowCut Lean after local memory/process preflight."""
import json
from pathlib import Path
import re
import subprocess
from check_unprotected_white_pair_formal import preflight

if not __debug__:
    raise RuntimeError('Run this verifier with assertions enabled')
ROOT=Path(__file__).resolve().parents[1]
NAMES=['two_port_completion','binary_completion','three_colour_partition',
       'two_colour_completion','optimal_TT_from_flow','cut_deficit_identity','star_cut_shortage',
       'greedy_cost_gap','greedy_linear_bound','greedy_ratio_bound','greedy_unbounded_ratio']


def main():
    check=preflight()
    run=subprocess.run(['lean','SubQuorum/ContactFlowCut.lean'],cwd=ROOT/'formal',text=True,capture_output=True)
    assert run.returncode==0 and not run.stderr,run.stdout+run.stderr
    assert not re.search(r'warning:|error:|sorryAx',run.stdout),run.stdout
    found=re.findall(r"'SubQuorum.ContactFlowCut\.(\w+)' (?:depends on axioms: \[([^\]]*)\]|does not depend on any axioms)",run.stdout)
    assert [name for name,_ in found]==NAMES
    audits=[dict(theorem='SubQuorum.ContactFlowCut.'+name,axioms=[a.strip() for a in axs.split(',') if a.strip()]) for name,axs in found]
    assert all(set(x['axioms'])<={'propext','Classical.choice','Quot.sound'} for x in audits)
    out=dict(status='PASS',execution_location='local',command='cd formal && lean SubQuorum/ContactFlowCut.lean',
        toolchain=(ROOT/'formal/lean-toolchain').read_text().strip(),preflight=check,
        theorems=audits,stdout=run.stdout,stderr=run.stderr,
        scope='Arbitrary-label two-port completion, binary completion, two-colour+unused completion; conditional optimal-TT, cut and star arithmetic; FOR EVERY K an explicit even greedy-barrier ratio witness.',
        not_formalized='Physical extraction/unique ownership, global max-flow decoding and min-cut optimality, all-s star embedding and two-colour weighted equivalence remain written. Not end-to-end grid Lean.')
    (ROOT/'output/contact-flow-formal.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(dict(status='PASS',theorems=len(audits))))


if __name__=='__main__':main()
