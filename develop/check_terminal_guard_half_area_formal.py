"""Run the scoped Lean audit locally after recording memory and real processes."""
import argparse
import json
from pathlib import Path
import re
import subprocess

ROOT=Path(__file__).resolve().parents[1]
NAMES=['terminal_bound','saturated_input_state','whole_board_bound',
       'equality_capacities','chunk_counts','physical_token_budget','no_reserve_at_equality']

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
    res=subprocess.run(['lean','SubQuorum/TerminalGuardHalfArea.lean'],cwd=ROOT/'formal',text=True,capture_output=True)
    assert res.returncode==0,res.stdout+res.stderr
    assert not res.stderr and not re.search(r'warning:|error:|sorryAx',res.stdout)
    found=re.findall(r"'SubQuorum.TerminalGuardHalfArea\.(\w+)' depends on axioms: \[([^\]]*)\]",res.stdout)
    assert [n for n,_ in found]==NAMES
    audits=[dict(theorem='SubQuorum.TerminalGuardHalfArea.'+n,axioms=[x.strip() for x in axs.split(',') if x.strip()]) for n,axs in found]
    assert all(set(x['axioms'])<={'propext','Classical.choice','Quot.sound'} for x in audits)
    out=dict(status='PASS',lean_version=version,execution_location='local',command='cd formal && lean SubQuorum/TerminalGuardHalfArea.lean',
        theorems=audits,preflight=checks,
        scope='Scaled terminal inequality/equality pattern, global upper bound/equality capacities, arbitrary-length chunk counts and physical token arithmetic.',
        not_formalized='Graph-coordinate reduction, old endpoint coverage, chunk gluing, inherited pocket/pair/block lemmas and nonfreezing argument are written proofs with independent Python controls; no end-to-end graph theorem claimed.')
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(dict(status=out['status'],lean_version=version,theorems=len(audits))))

if __name__=='__main__':main()
