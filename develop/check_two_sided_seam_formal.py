"""Scoped local Lean audit with memory/process preflight and physical adapter check."""
import argparse
import ast
import datetime
import json
import os
from pathlib import Path
import re
import subprocess

if not __debug__:raise RuntimeError('Assertions required; do not use -O.')


def main():
    p=argparse.ArgumentParser();p.add_argument('--lean',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    args=p.parse_args();root=Path(__file__).resolve().parents[1]
    def processes():
        lines=subprocess.check_output(['ps','-axo','pid=,comm='],text=True).splitlines()
        return [s.strip() for s in lines if len(s.split(None,1))==2 and os.path.basename(s.split(None,1)[1]) in ('lean','lake')]
    memory=subprocess.check_output(['memory_pressure'],text=True)
    preflight=dict(active_processes_by_comm_basename=processes(),
        memory_free_percentage=re.search(r'System-wide memory free percentage: (\d+%)',memory).group(1),
        physical_memory_bytes=int(subprocess.check_output(['sysctl','-n','hw.memsize'],text=True)),
        execution='Current-session user chose local machine; one small standalone module; preserve unrelated jobs.')
    print(json.dumps(preflight),flush=True)
    fixture=json.loads((root/'develop/fixtures/two_sided_seam_recourse.json').read_text())
    path=root/'formal/SubQuorum/TwoSidedSeamRecourse.lean';source=path.read_text()
    assert not re.search(r'\b(sorry|admit|native_decide|axiom)\b',source)
    def read(name):
        match=re.search(r'^def '+name+r' : .*? := (.+)$',source,re.M);assert match,name
        return json.loads(json.dumps(ast.literal_eval(match.group(1))))
    for name,key in [('selected','selected'),('matching','matching'),('roots','roots'),('reachable','reachable'),('ownerLinks','owner_links'),('originalUnits','resources'),('newUnits','new_units'),('actualSupports','support')]:
        assert read(name)==fixture[key],name
    from check_two_sided_seam_recourse import model
    from check_selection_maximum_singleton import compile_even_width
    from check_compensation_flow_normal_form import owner_data
    cur=model(fixture['W'],fixture['k'],set(fixture['upper_open']),set(fixture['lower_open']))
    data,_=compile_even_width(cur);own,A,B,_=owner_data(*data[:2])
    assert sorted(cur[2])==list(map(tuple,fixture['selected']))
    assert sorted(data[4])==list(map(tuple,fixture['resources']))
    assert set(fixture['roots'])==A and not B
    assert own[(1,5)]==fixture['roots'][0]
    lean=str(args.lean.resolve());version=subprocess.check_output([lean,'--version'],text=True).strip()
    assert 'version 4.33.0' in version
    result=subprocess.run([lean,str(path)],cwd=root,text=True,capture_output=True)
    output=result.stdout+result.stderr;print(output,end='',flush=True)
    assert result.returncode==0
    assert not re.search(r'warning:|error:|sorryAx|Lean.ofReduceBool|Lean.trustCompiler',output)
    audits=[s for s in output.splitlines() if 'depends on axioms' in s or 'does not depend' in s]
    assert len(audits)==15
    for body in re.findall(r'depends on axioms: \[([^\]]*)\]',output):
        assert {a.strip() for a in body.split(',') if a.strip()} <= {'propext','Classical.choice','Quot.sound'}
    report=dict(status='PASS',checked_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),lean_version=version,
        preflight=preflight,active_processes_after_by_comm_basename=processes(),declaration_audits=audits,
        scope='All-length first-double prefix forcing from singleton-edge collisions; forced changed old original-edge identities; injective explicit upper/lower repair units with valid range/incidence/availability; old suffix retained; cyclic cost and global slack arithmetic; unbounded parameter choice; compiler-aligned physical W8/k4/p3 full original-pool closure constants.',
        not_formalized=['General physical coordinate extraction and full-W/k freezing',
            'Finite-cardinality summation for rank, exact cost and p-1 old assignment changes',
            'Physical route/flow equivalence; written proof and independently checked adapter supplied'],
        sorry=False,native_decide=False,new_axioms=False)
    args.output.write_text(json.dumps(report,indent=2)+'\n')
    print('PASS: 15 scoped declaration audits; physical full original-pool constants aligned')

if __name__=='__main__':main()
