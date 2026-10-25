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
    build=root/'build/crossing-matching-ports-formal';(build/'SubQuorum').mkdir(parents=True,exist_ok=True)
    lean=str(args.lean.resolve());version=subprocess.check_output([lean,'--version'],text=True).strip();assert 'version 4.33.0' in version
    checks=[];env=dict(os.environ,LEAN_PATH=str(build)+':'+str(formal))
    fixture=json.loads((root/'develop/fixtures/crossing_matching_port_obstruction.json').read_text())
    dependency=(formal/'SubQuorum/ForcedMatesAdjacentMaxima.lean').read_text()
    for name,key in [('selected','selected_points'),('matching','matching_edges')]:
        statement=re.search(r'^def '+name+r' : .*? := (\[.*\])$',dependency,re.M)
        assert statement and json.loads(json.dumps(ast.literal_eval(statement.group(1))))==fixture[key]
    sys_path=str(root/'develop')
    import sys
    sys.path.insert(0,sys_path)
    from check_compensation_flow_normal_form import owner_data
    kinds={tuple(v):k for v,k in fixture['kinds']};pairs=[tuple(map(tuple,p)) for p in fixture['pairs']]
    owners,A,B,_=owner_data(kinds,pairs)
    expected=dict(ownerLinks=sorted({(owners[tuple(a)],owners[tuple(b)]) for a,b in fixture['links']}),
        alphas=sorted(A),betas=sorted(B),raw=fixture['resources'],supports=fixture['support'])
    fresh=(formal/'SubQuorum/CrossingMatchingPorts.lean').read_text()
    for name,value in expected.items():
        statement=re.search(r'^def '+name+r' : .*? :=\s*(\[.*\])$',fresh,re.M)
        assert statement and json.loads(json.dumps(ast.literal_eval(statement.group(1))))==json.loads(json.dumps(value))
    for filename,n in [('BTColumnCorridorObstruction',16),('FullPoolSingletonObstruction',14),('ForcedMatesAdjacentMaxima',9),('CrossingMatchingPorts',15)]:
        path='SubQuorum/'+filename+'.lean';source=(formal/path).read_text()
        assert not re.search(r'\b(sorry|admit|native_decide|axiom)\b',source)
        command=[lean,path]
        if filename!='CrossingMatchingPorts':command+=['-o',str(build/'SubQuorum'/f'{filename}.olean')]
        result=subprocess.run(command,cwd=formal,env=env,text=True,capture_output=True)
        print(result.stdout,end='',flush=True);print(result.stderr,end='',flush=True)
        assert result.returncode==0
        assert not re.search(r'warning:|error:|sorryAx|Lean.ofReduceBool|Lean.trustCompiler',result.stdout+result.stderr)
        audits=[x for x in result.stdout.splitlines() if 'depends on axioms' in x or 'does not depend' in x];assert len(audits)==n
        for body in re.findall(r'depends on axioms: \[([^\]]*)\]',result.stdout):
            assert {a.strip() for a in body.split(',') if a.strip()} <= {'propext','Classical.choice','Quot.sound'}
        checks.append(dict(module=path,exit_code=result.returncode,axiom_audits=audits))
    report=dict(status='PASS',checked_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),lean_version=version,
        preflight=preflight,checks=checks,scope='General port ledger arithmetic, exact interface correction and alpha bound, zero port-cycle credit; closed body reachability persistence; disjoint old/new reserve allocation injectivity; retained-pack and unused-reserve deficit bounds and full-payment implication. Actual W8/q1 unchanged fully frozen board, one crossing edge, closed connected mixed-direction TT path, concrete whole-support closure and arbitrary-length no-payment route exclusion.',
        not_formalized=['General geometric component/port skeleton classification and coordinate-to-resource adapter','All-even-W/all-q sharp frozen family specialization','Geometric primitive-pack lift and residual matching existence; proved in writing with Python checks'],
        sorry=False,native_decide=False)
    args.output.write_text(json.dumps(report,indent=2)+'\n')
    print('PASS: 15 new and 39 dependency declaration audits')

if __name__=='__main__':main()
