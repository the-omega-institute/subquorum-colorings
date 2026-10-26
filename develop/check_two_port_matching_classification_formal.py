"""Run the scoped Lean audit locally after recording memory and real processes."""
import argparse
import json
from pathlib import Path
import re
import os
import tempfile
import subprocess

ROOT=Path(__file__).resolve().parents[1]
NAMES=['separated_fronts_exclude_freezing','least_root','root_normal_form','odd_column_normal_form','absent_port_excludes_noncanonical']

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
    with tempfile.TemporaryDirectory(prefix='subquorum-classification-lean-') as temporary:
        compiled=Path(temporary)/'SubQuorum';compiled.mkdir()
        env=dict(os.environ,LEAN_PATH=temporary)
        dep=subprocess.run(['lean','-o',str(compiled/'TwoPortUnboundedRematching.olean'),'SubQuorum/TwoPortUnboundedRematching.lean'],cwd=ROOT/'formal',text=True,capture_output=True,env=env)
        assert dep.returncode==0,dep.stdout+dep.stderr
        assert not dep.stderr and not re.search(r'warning:|error:|sorryAx',dep.stdout),dep.stdout+dep.stderr
        checks.append(preflight())
        res=subprocess.run(['lean','SubQuorum/TwoPortMatchingClassification.lean'],cwd=ROOT/'formal',text=True,capture_output=True,env=env)
    assert res.returncode==0,res.stdout+res.stderr
    assert not res.stderr and not re.search(r'warning:|error:|sorryAx',res.stdout),res.stdout+res.stderr
    found=re.findall(r"'SubQuorum.TwoPortMatchingClassification\.(\w+)' (?:depends on axioms: \[([^\]]*)\]|does not depend on any axioms)",res.stdout)
    assert [n for n,_ in found]==NAMES
    audits=[dict(theorem='SubQuorum.TwoPortMatchingClassification.'+n,axioms=[x.strip() for x in (axs or '').split(',') if x.strip()]) for n,axs in found]
    assert all(set(x['axioms'])<={'propext','Classical.choice','Quot.sound'} for x in audits)
    out=dict(status='PASS',lean_version=version,execution_location='local',command='cd formal && lean SubQuorum/TwoPortMatchingClassification.lean',
        theorems=audits,preflight=checks,
        scope='Separated-front interval barrier for arbitrary endpoint types and least freezing closure; all-length singleton/adjacent-pair root normal form; conditional absence-of-input exclusion.',
        not_formalized='Concrete coordinate support localization, EF/L/R reduction, lower-row parity, matching reconstruction, positive wave sequences, exact coordinate counts and physical stack adapters remain written with solver-free checks. Not an end-to-end Lean coordinate classification.')
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(dict(status=out['status'],lean_version=version,theorems=len(audits))))

if __name__=='__main__':main()
