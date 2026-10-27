"""Scoped local Lean check, with memory and comm-basename process preflight."""
import json
from pathlib import Path
import re
import subprocess
from check_unprotected_white_pair_formal import preflight

if not __debug__:
    raise RuntimeError('Run this verifier with assertions enabled')
ROOT=Path(__file__).resolve().parents[1]
NAMES=['local_C4_profile','local_C4_charge','debt_diagonal','local_slack',
       'signed_cycle_ledger','regional_white_cancellation','local_reserve_cancellation',
       'regional_cross_excess','debt_boundary_identity','debt_flow_deficit',
       'debt_free_regional_bound','positive_component','cycle_relay_cost',
       'cycle_relay_margin','old_cycle_unbounded_expense']


def main():
    check=preflight()
    run=subprocess.run(['lean','SubQuorum/GeneralSquarePorts.lean'],cwd=ROOT/'formal',text=True,capture_output=True)
    assert run.returncode==0 and not run.stderr,run.stdout+run.stderr
    assert not re.search(r'warning:|error:|sorryAx',run.stdout),run.stdout
    found=re.findall(r"'SubQuorum.GeneralSquarePorts\.(\w+)' (?:depends on axioms: \[([^\]]*)\]|does not depend on any axioms)",run.stdout)
    assert [name for name,_ in found]==NAMES
    audits=[dict(theorem='SubQuorum.GeneralSquarePorts.'+name,axioms=[a.strip() for a in axs.split(',') if a.strip()]) for name,axs in found]
    assert all(set(x['axioms'])<={'propext','Classical.choice','Quot.sound'} for x in audits)
    out=dict(status='PASS',execution_location='local',command='cd formal && lean SubQuorum/GeneralSquarePorts.lean',
        toolchain=(ROOT/'formal/lean-toolchain').read_text().strip(),preflight=check,
        theorems=audits,stdout=run.stdout,stderr=run.stderr,
        scope='Complete local C4 feasible-label profile/charge and diagonal debt; supported-internal-M local slack; signed partition and regional/debt arithmetic; arbitrary finite positive component; all-K even unbounded old-cycle expense.',
        not_formalized='Physical fragment adapter, global max-flow/min-cut and debt-flow equivalence, normalization, all-H coordinate embedding, and numerical target remain written or open as specified. Not end-to-end grid Lean.')
    (ROOT/'output/general-square-formal.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(dict(status='PASS',theorems=len(audits))))


if __name__=='__main__':main()
