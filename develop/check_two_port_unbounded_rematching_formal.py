"""Run the scoped Lean audit locally after recording memory and real processes."""
import argparse
import json
from pathlib import Path
import re
import subprocess

ROOT=Path(__file__).resolve().parents[1]
NAMES=['actual_mate_preserves_dependency_colour', 'colour_freezing_invariant', 'exact_two_input_response', 'two_inputs_necessary_sufficient', 'zipper_matching_counts', 'exact_interface_counts', 'early_black_checks', 'lower_black_step', 'terminal_G_check', 'lower_white_step', 'white_core_steps', 'white_core_successors', 'changed_cap_seam_checks', 'rank_max_checks', 'no_uniform_defect_per_port', 'no_uniform_rematching_radius', 'fixed_port_affine_defect_bound_fails']

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
    res=subprocess.run(['lean','SubQuorum/TwoPortUnboundedRematching.lean'],cwd=ROOT/'formal',text=True,capture_output=True)
    assert res.returncode==0,res.stdout+res.stderr
    assert not res.stderr and not re.search(r'warning:|error:|sorryAx',res.stdout),res.stdout+res.stderr
    found=re.findall(r"'SubQuorum.TwoPortUnboundedRematching\.(\w+)' (?:depends on axioms: \[([^\]]*)\]|does not depend on any axioms)",res.stdout)
    assert [n for n,_ in found]==NAMES
    audits=[dict(theorem='SubQuorum.TwoPortUnboundedRematching.'+n,axioms=[x.strip() for x in (axs or '').split(',') if x.strip()]) for n,axs in found]
    assert all(set(x['axioms'])<={'propext','Classical.choice','Quot.sound'} for x in audits)
    out=dict(status='PASS',lean_version=version,execution_location='local',command='cd formal && lean SubQuorum/TwoPortUnboundedRematching.lean',
        theorems=audits,preflight=checks,
        scope='Arbitrary-type actual-mate colour dependence and least-closure invariance, conditional exact two-input response and necessity/sufficiency, matching and interface counts, all-length rank arithmetic, and unbounded changed-edge count/radius at fixed two ports.',
        not_formalized='The concrete all-length matching, coordinate-to-bipartition adapter, explicit rank membership, exact geometric trap support tables, physical token payment and stack adapters remain written with solver-free checks. This is not an end-to-end Lean coordinate theorem or a classification of all matchings.')
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(dict(status=out['status'],lean_version=version,theorems=len(audits))))

if __name__=='__main__':main()
