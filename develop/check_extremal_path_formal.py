"""One-module local Lean audit, preserving unrelated Lean/Lake jobs."""
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
    args=p.parse_args();root=Path(__file__).resolve().parents[1]
    listing=subprocess.check_output(['ps','-axo','pid=,comm='],text=True)
    active=[x.strip() for x in listing.splitlines() if len(x.split(None,1))==2 and os.path.basename(x.split(None,1)[1]) in ('lean','lake')]
    memory=subprocess.check_output(['memory_pressure'],text=True)
    preflight=dict(active_processes_by_comm_basename=active,
        memory_free_percentage=re.search(r'System-wide memory free percentage: (\d+%)',memory).group(1),
        physical_memory_bytes=int(subprocess.check_output(['sysctl','-n','hw.memsize'],text=True)),
        execution='Local machine selected in current session; one standalone small module; preserve unrelated processes.')
    print(json.dumps(preflight),flush=True)
    fixture=json.loads((root/'develop/fixtures/extremal_full_pool_path.json').read_text())
    path=root/'formal/SubQuorum/ExtremalPathCircuits.lean';source=path.read_text()
    assert not re.search(r'\b(sorry|admit|native_decide|axiom)\b',source)
    def read(name):
        m=re.search(r'^def '+name+r' : .*? := (.+)$',source,re.M)
        assert m,name
        return json.loads(json.dumps(ast.literal_eval(m.group(1))))
    for name,key in [('selected','selected_points'),('matching','matching_edges'),('actualPairs','pairs'),
                     ('ownerLinks','owner_links'),('roots','roots'),('reachable','reachable'),
                     ('originalUnits','resources'),('openedUnits','opened_units'),('actualSupports','support')]:
        assert read(name)==fixture[key],name
    from check_compensation_flow_normal_form import owner_data
    kinds={tuple(v):k for v,k in fixture['kinds']};pairs=[tuple(map(tuple,p)) for p in fixture['pairs']]
    _,alphas,betas,_=owner_data(kinds,pairs)
    assert set(fixture['roots'])==alphas and not betas
    lean=str(args.lean.resolve());version=subprocess.check_output([lean,'--version'],text=True).strip()
    assert 'version 4.33.0' in version
    build=root/'build/extremal-path-circuits-formal';(build/'SubQuorum').mkdir(parents=True,exist_ok=True)
    env=dict(os.environ,LEAN_PATH=str(build)+':'+str(root/'formal'))
    dependency=root/'formal/SubQuorum/EndpointComponentResourceGluing.lean'
    assert not re.search(r'\b(sorry|admit|native_decide|axiom)\b',dependency.read_text())
    checks=[]
    for module,count in [(dependency,11),(path,17)]:
        command=[lean,str(module)]
        if module==dependency:command+=['-o',str(build/'SubQuorum/EndpointComponentResourceGluing.olean')]
        result=subprocess.run(command,cwd=root/'formal',env=env,text=True,capture_output=True)
        output=result.stdout+result.stderr;print(output,end='',flush=True)
        assert result.returncode==0
        assert not re.search(r'warning:|error:|sorryAx|Lean.ofReduceBool|Lean.trustCompiler',output)
        audits=[x for x in output.splitlines() if 'depends on axioms' in x or 'does not depend' in x]
        assert len(audits)==count
        for body in re.findall(r'depends on axioms: \[([^\]]*)\]',output):
            assert {a.strip() for a in body.split(',') if a.strip()} <= {'propext','Classical.choice','Quot.sound'}
        checks.append(dict(module=module.name,declaration_audits=audits))
    after=subprocess.check_output(['ps','-axo','pid=,comm='],text=True)
    after=[x.strip() for x in after.splitlines() if len(x.split(None,1))==2 and os.path.basename(x.split(None,1)[1]) in ('lean','lake')]
    report=dict(status='PASS',checked_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),lean_version=version,
        preflight=preflight,active_processes_after_by_comm_basename=after,checks=checks,
        scope='Physical two-neighbor obstruction behind the open-seam tile loss; one-cover opening-budget and exact slack/deficit arithmetic; general omitted-source edge-range, incidence and injectivity; unbounded left and reverse-right forcing of every maximum source basis and exact cost arithmetic; earlier retained-edge injection reused for full-pool adapter; unique violating withdrawal arithmetic; one-below-maximum mixed specialization; actual W8/k3 full original pool and source/exit/support closure constants.',
        not_formalized=['General physical coordinate extraction and full all-W/k freezing',
            'Finite-cardinality summation of disjoint cover, source and withdrawal injections',
            'Integral flow equivalence and physical minimum link counts from geometric route classification; written proofs and independent code supplied'],
        sorry=False,native_decide=False,new_axioms=False)
    args.output.write_text(json.dumps(report,indent=2)+'\n')
    print('PASS: 17 new and 11 reused dependency audits; full original-pool physical fixture agreement')

if __name__=='__main__':main()
