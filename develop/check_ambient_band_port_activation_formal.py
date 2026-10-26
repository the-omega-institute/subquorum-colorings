"""Run the scoped Lean audit locally after recording memory and real processes."""
import argparse
import json
from pathlib import Path
import re
import subprocess

ROOT=Path(__file__).resolve().parents[1]
NAMES=['stage_rank_forces_closed','stage_certificate_implies_seeded_freezing','three_stage_composition','seeded_trap_exclusion','phase_rank_strict','early_cap_rank_checks','return_cap_rank_checks','flipped_band_rank_checks','cap_rank_max','cap_counts','ambient_counts','zero_charge_is_not_unused_credit','union_token_budget','indexed_payment_bijective','stack_objective','stack_half_area','no_reserve_per_flipped_region']

def preflight():
    ps=subprocess.check_output(['ps','-axo','pid=,comm='],text=True)
    active=[]
    for line in ps.splitlines():
        fields=line.strip().split(maxsplit=1)
        if len(fields)==2 and Path(fields[1]).name in {'lean','lake'}:active.append(line.strip())
    memory=subprocess.check_output(['memory_pressure'],text=True)
    vm=subprocess.check_output(['vm_stat'],text=True)
    if active:raise RuntimeError('Reassess concurrency before Lean: '+str(active))
    return dict(active_lean_lake_by_comm_basename=active,memory_pressure=memory.strip(),vm_stat=vm.strip())

def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);args=p.parse_args()
    checks=[preflight()]
    version=subprocess.check_output(['lean','--version'],cwd=ROOT/'formal',text=True).strip()
    checks.append(preflight())
    res=subprocess.run(['lean','SubQuorum/AmbientBandPortActivation.lean'],cwd=ROOT/'formal',text=True,capture_output=True)
    assert res.returncode==0,res.stdout+res.stderr
    assert not res.stderr and not re.search(r'warning:|error:|sorryAx',res.stdout),res.stdout+res.stderr
    found=re.findall(r"'SubQuorum.AmbientBandPortActivation\.(\w+)' (?:depends on axioms: \[([^\]]*)\]|does not depend on any axioms)",res.stdout)
    assert [n for n,_ in found]==NAMES
    audits=[dict(theorem='SubQuorum.AmbientBandPortActivation.'+n,axioms=[x.strip() for x in (axs or '').split(',') if x.strip()]) for n,axs in found]
    assert all(set(x['axioms'])<={'propext','Classical.choice','Quot.sound'} for x in audits)
    out=dict(status='PASS',lean_version=version,execution_location='local',command='cd formal && lean SubQuorum/AmbientBandPortActivation.lean',
        theorems=audits,preflight=checks,
        scope='Generic strict actual-mate stage induction, seeded closure, three-stage composition, seeded trap exclusion, phase rank lifting, cap and flipped-band rank arithmetic, exact counts, indexed bijective payment nonreuse, arbitrary-stack half-area and impossible flipped-region reserve.',
        not_formalized='Full grid coordinate membership, concrete matching and feasibility, all-length witness adapters, exact interface trap instantiations and geometric tile identities remain written and independently executable. No end-to-end coordinate theorem is claimed.')
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(dict(status=out['status'],lean_version=version,theorems=len(audits))))

if __name__=='__main__':main()
