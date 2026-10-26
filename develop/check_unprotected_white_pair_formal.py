"""Run the scoped Lean audit locally after recording memory and real processes."""
import argparse
import json
from pathlib import Path
import re
import subprocess

ROOT=Path(__file__).resolve().parents[1]
NAMES=['common_neighbour_not_selected','three_private_neighbours_not_all_selected','occupied_white_excludes_four_selected','bit_le_one','actual_capacity','top_block_budget','terminal_one_unit_budget']

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
    res=subprocess.run(['lean','SubQuorum/UnprotectedWhitePair.lean'],cwd=ROOT/'formal',text=True,capture_output=True)
    assert res.returncode==0,res.stdout+res.stderr
    assert not res.stderr and not re.search(r'warning:|error:|sorryAx',res.stdout),res.stdout+res.stderr
    found=re.findall(r"'SubQuorum.UnprotectedWhitePair\.(\w+)' (?:depends on axioms: \[([^\]]*)\]|does not depend on any axioms)",res.stdout)
    assert [n for n,_ in found]==NAMES
    audits=[dict(theorem='SubQuorum.UnprotectedWhitePair.'+n,axioms=[x.strip() for x in (axs or '').split(',') if x.strip()]) for n,axs in found]
    assert all(set(x['axioms'])<={'propext','Classical.choice','Quot.sound'} for x in audits)
    out=dict(status='PASS',lean_version=version,execution_location='local',command='cd formal && lean SubQuorum/UnprotectedWhitePair.lean',
        theorems=audits,preflight=checks,
        scope='Actual mate/selected-degree six-site projection proves full two-white capacity allowing either white site selected; four-selector six-hole top-block inequality and disjoint terminal one-unit count.',
        not_formalized='Whole-grid coordinate projection, application of earlier pocket/global count, unchanged frozen rank certificate and all-length local-budget obstruction remain written proofs with solver-free controls.')
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(dict(status=out['status'],lean_version=version,theorems=len(audits))))

if __name__=='__main__':main()
