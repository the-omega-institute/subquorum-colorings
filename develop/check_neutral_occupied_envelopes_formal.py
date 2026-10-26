"""Run the scoped Lean audit locally after recording memory and real processes."""
import argparse
import json
from pathlib import Path
import re
import os
import tempfile
import subprocess

ROOT=Path(__file__).resolve().parents[1]
NAMES=['shield_coordinate_injective','exact_shared_guard_count','restricted_conversion_shortage','singleton_shield_excludes_freezing','no_fully_frozen_restricted_conversion','local_full_envelope_budget','all_length_full_envelope_budget','zero_deficit_iff_complete_cells','neutral_objective_forces_complete_cells']

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
    with tempfile.TemporaryDirectory(prefix='subquorum-envelope-lean-') as temporary:
        compiled=Path(temporary)/'SubQuorum';compiled.mkdir()
        env=dict(os.environ,LEAN_PATH=temporary)
        dep=subprocess.run(['lean','-o',str(compiled/'FrozenHalfAreaAttainers.olean'),'SubQuorum/FrozenHalfAreaAttainers.lean'],cwd=ROOT/'formal',text=True,capture_output=True,env=env)
        assert dep.returncode==0,dep.stdout+dep.stderr
        assert not dep.stderr and not re.search(r'warning:|error:|sorryAx',dep.stdout),dep.stdout+dep.stderr
        checks.append(preflight())
        res=subprocess.run(['lean','SubQuorum/NeutralOccupiedEnvelopes.lean'],cwd=ROOT/'formal',text=True,capture_output=True,env=env)
    assert res.returncode==0,res.stdout+res.stderr
    assert not res.stderr and not re.search(r'warning:|error:|sorryAx',res.stdout),res.stdout+res.stderr
    found=re.findall(r"'SubQuorum.NeutralOccupiedEnvelopes\.(\w+)' (?:depends on axioms: \[([^\]]*)\]|does not depend on any axioms)",res.stdout)
    assert [n for n,_ in found]==NAMES
    audits=[dict(theorem='SubQuorum.NeutralOccupiedEnvelopes.'+n,axioms=[x.strip() for x in (axs or '').split(',') if x.strip()]) for n,axs in found]
    assert all(set(x['axioms'])<={'propext','Classical.choice','Quot.sound'} for x in audits)
    out=dict(status='PASS',lean_version=version,execution_location='local',command='cd formal && lean SubQuorum/NeutralOccupiedEnvelopes.lean',
        theorems=audits,preflight=checks,
        scope='Injective physical shield coordinates; exact shared-guard count and strict conversion shortage on arbitrary finite entry words; actual-mate singleton trap; conditional restricted no-freezing contradiction; all eight envelope masks, arbitrary-length pooled budget, and neutral equality footprint classification.',
        not_formalized='The envelope matching, complete coordinate rank tables, feasibility and physical token cancellation remain written all-length proofs with solver-free adapter checks. Rank induction is reused from FrozenHalfAreaAttainers. Not an end-to-end Lean coordinate theorem.')
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(dict(status=out['status'],lean_version=version,theorems=len(audits))))

if __name__=='__main__':main()
