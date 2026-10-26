"""Run the scoped Lean audit locally after recording memory and real processes."""
import argparse
import json
from pathlib import Path
import re
import subprocess

ROOT=Path(__file__).resolve().parents[1]
NAMES=['rank_forces_closed', 'certificate_implies_frozen', 'trap_excludes_frozen', 'early_ranks', 'lower_white_step', 'lower_white_terminal', 'lower_black_early', 'lower_black_step', 'lower_black_terminal', 'left_port_step', 'right_return_start', 'bridge_precedes_H', 'lower_whites_precede_H', 'return_core_steps', 'return_bridge_step', 'old_core_white_max', 'last_white_rank', 'lower_and_port_rank_max', 'bridge_rank_max', 'construction_counts', 'exact_token_budget', 'full_tile_budget', 'terminal_port_frontier', 'terminal_port_token_budget']

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
    res=subprocess.run(['lean','SubQuorum/FrozenHalfAreaAttainers.lean'],cwd=ROOT/'formal',text=True,capture_output=True)
    assert res.returncode==0,res.stdout+res.stderr
    assert not res.stderr and not re.search(r'warning:|error:|sorryAx',res.stdout)
    found=re.findall(r"'SubQuorum.FrozenHalfAreaAttainers\.(\w+)' (?:depends on axioms: \[([^\]]*)\]|does not depend on any axioms)",res.stdout)
    assert [n for n,_ in found]==NAMES
    audits=[dict(theorem='SubQuorum.FrozenHalfAreaAttainers.'+n,axioms=[x.strip() for x in (axs or '').split(',') if x.strip()]) for n,axs in found]
    assert all(set(x['axioms'])<={'propext','Classical.choice','Quot.sound'} for x in audits)
    out=dict(status='PASS',lean_version=version,execution_location='local',command='cd formal && lean SubQuorum/FrozenHalfAreaAttainers.lean',
        theorems=audits,preflight=checks,
        scope='Generic well-founded strict-rank implication into least freezing closure and exclusion by a freezing trap; all-length early/lower/return-wave rank comparisons, maximum certificate rank, construction counts and sharp terminal-port bound/token arithmetic.',
        not_formalized='Actual coordinate/matching adapter, endpoint partition, selected feasibility, witness adjacency/selection exact physical tile-charge table and the coordinate instantiation of terminal traps are written proofs with independent Python checks. The generic rank theorem is not an end-to-end Lean graph instantiation.')
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(dict(status=out['status'],lean_version=version,theorems=len(audits))))

if __name__=='__main__':main()
