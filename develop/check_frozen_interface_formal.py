"""Scoped local Lean audit; record resources and preserve unrelated processes."""
import argparse
import ast
import datetime
import json
import os
from pathlib import Path
import re
import subprocess


def main():
    p=argparse.ArgumentParser();p.add_argument('--lean',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    args=p.parse_args();root=Path(__file__).resolve().parents[1];formal=root/'formal'
    listing=subprocess.check_output(['ps','-axo','pid=,comm='],text=True)
    active=[x.strip() for x in listing.splitlines() if len(x.split(None,1))==2 and os.path.basename(x.split(None,1)[1]) in ('lean','lake')]
    memory=subprocess.check_output(['memory_pressure'],text=True)
    preflight=dict(active_processes_by_comm_basename=active,
        memory_free_percentage=re.search(r'System-wide memory free percentage: (\d+%)',memory).group(1),
        physical_memory_bytes=int(subprocess.check_output(['sysctl','-n','hw.memsize'],text=True)),
        concurrency='One small standalone module at a time; preserve every unrelated process.')
    print(json.dumps(preflight),flush=True)
    build=root/'build/frozen-interface-optimality-formal';(build/'SubQuorum').mkdir(parents=True,exist_ok=True)
    lean=str(args.lean.resolve());version=subprocess.check_output([lean,'--version'],text=True).strip();assert 'version 4.33.0' in version
    checks=[];env=dict(os.environ,LEAN_PATH=str(build)+':'+str(formal))
    fixture=json.loads((root/'develop/fixtures/opposed_direction_interface_obstruction.json').read_text())
    concrete=(formal/'SubQuorum/OpposedDirectionInterfaces.lean').read_text()
    for name,key in [('selected','selected_points'),('matching','matching_edges')]:
        statement=re.search(r'^def '+name+r' : .*? := (\[.*\])$',concrete,re.M)
        assert statement and json.loads(json.dumps(ast.literal_eval(statement.group(1))))==fixture[key]
    fresh=(formal/'SubQuorum/FrozenInterfaceOptimality.lean').read_text()
    new_fixture=json.loads((root/'develop/fixtures/frozen_interface_optimality.json').read_text())
    local=re.search(r'def localWitness : List Point :=\s*(\[.*\])',fresh)
    assert local and json.loads(json.dumps(ast.literal_eval(local.group(1))))==new_fixture['local']['attaining_local_selected_points']
    unrestricted=re.search(r'def unrestrictedSelected : List Point := (\[.*\])',fresh)
    assert unrestricted and json.loads(json.dumps(ast.literal_eval(unrestricted.group(1))))==new_fixture['unrestricted_selected_points']
    for filename,n in [('BTColumnCorridorObstruction',16),('FullPoolSingletonObstruction',14),('OpposedDirectionInterfaces',17),('FrozenInterfaceOptimality',13)]:
        path='SubQuorum/'+filename+'.lean';source=(formal/path).read_text()
        assert not re.search(r'\b(sorry|admit|native_decide|axiom)\b',source)
        command=[lean,path]
        if filename!='FrozenInterfaceOptimality':command+=['-o',str(build/'SubQuorum'/f'{filename}.olean')]
        result=subprocess.run(command,cwd=formal,env=env,text=True,capture_output=True)
        print(result.stdout,end='',flush=True);print(result.stderr,end='',flush=True)
        assert result.returncode==0
        assert not re.search(r'warning:|error:|sorryAx|Lean.ofReduceBool|Lean.trustCompiler',result.stdout+result.stderr)
        audits=[x for x in result.stdout.splitlines() if 'depends on axioms' in x or 'does not depend' in x];assert len(audits)==n
        for body in re.findall(r'depends on axioms: \[([^\]]*)\]',result.stdout):
            assert {a.strip() for a in body.split(',') if a.strip()} <= {'propext','Classical.choice','Quot.sound'}
        checks.append(dict(module=path,exit_code=result.returncode,axiom_audits=audits))
    report=dict(status='PASS',checked_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),lean_version=version,
        preflight=preflight,checks=checks,scope='General inductive freezing necessary witnesses and single-witness exclusion; exact integer local packing cut, physical sharp q1 strip and endpoint stencil, actual feasible100T q1 geometry and inductive nonfreezing of its witnessless endpoint; cover-loss substitution and all-q selection count arithmetic.',
        not_formalized=['All-q coordinate specialization of the endpoint stencil and cover membership','Explicit unrestricted all-q attainer coordinate feasibility','Grid-to-indicator/count adapter and end-to-end grid selection optima'],
        sorry=False,native_decide=False)
    args.output.write_text(json.dumps(report,indent=2)+'\n')
    print('PASS: 13 new and 47 dependency declaration audits')

if __name__=='__main__':main()
