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
    fixture=json.loads((root/'develop/fixtures/full_pool_interface_singleton.json').read_text())
    path=root/'formal/SubQuorum/FullPoolInterfaceProfile.lean';source=path.read_text()
    assert not re.search(r'\b(sorry|admit|native_decide|axiom)\b',source)
    def read(name):
        m=re.search(r'^def '+name+r' : .*? := (.+)$',source,re.M)
        assert m,name
        return json.loads(json.dumps(ast.literal_eval(m.group(1))))
    for name,key in [('selected','selected_points'),('matching','matching_edges'),('actualPairs','pairs'),
                     ('ownerLinks','owner_links'),('closedOwners','closure'),('oldOwners','old'),
                     ('interfaceOwners','interface'),('originalUnits','resources')]:
        assert read(name)==fixture[key],name
    assert read('actualShared')==fixture['tables'][0]['shared']
    from check_compensation_flow_normal_form import owner_data
    kinds={tuple(v):k for v,k in fixture['kinds']};pairs=[tuple(map(tuple,p)) for p in fixture['pairs']]
    _,alphas,betas,_=owner_data(kinds,pairs)
    assert read('betaOwners')==sorted(betas) and set(fixture['old'])|set(fixture['interface'])==alphas
    support={o:js for o,js in fixture['support']}
    assert all(support[o]==([read('actualShared')] if o in [4,11] else []) for o in fixture['closure'])
    lean=str(args.lean.resolve());version=subprocess.check_output([lean,'--version'],text=True).strip()
    assert 'version 4.33.0' in version
    result=subprocess.run([lean,str(path)],cwd=root/'formal',text=True,capture_output=True)
    output=result.stdout+result.stderr;print(output,end='',flush=True)
    assert result.returncode==0
    assert not re.search(r'warning:|error:|sorryAx|Lean.ofReduceBool|Lean.trustCompiler',output)
    audits=[x for x in output.splitlines() if 'depends on axioms' in x or 'does not depend' in x]
    assert len(audits)==21
    for body in re.findall(r'depends on axioms: \[([^\]]*)\]',output):
        assert {a.strip() for a in body.split(',') if a.strip()} <= {'propext','Classical.choice','Quot.sound'}
    after=subprocess.check_output(['ps','-axo','pid=,comm='],text=True)
    after=[x.strip() for x in after.splitlines() if len(x.split(None,1))==2 and os.path.basename(x.split(None,1)[1]) in ('lean','lake')]
    report=dict(status='PASS',checked_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),lean_version=version,
        preflight=preflight,active_processes_after_by_comm_basename=after,declaration_audits=audits,
        scope='Indexed eight-owner arbitrary routes preserve copy index; no route from old source reaches interface; all payments stay in original copy; unrepaired old/interface payments collide; exact lower bounds two links to shared unit and one to private unit; explicit repair routes and distinct units; aggregate exact value/deficit/cost arithmetic and positive numerical slack; actual W8 source table and full original pool compiled constants.',
        not_formalized=['General physical coordinate-to-owner/resource adapter and all-W/q freezing',
            'Finite-cardinality summation of per-copy route/payment bounds and construction of full physical certificates',
            'Max-flow duality; complete written arguments and independent Python checks supplied'],
        sorry=False,native_decide=False,new_axioms=False)
    args.output.write_text(json.dumps(report,indent=2)+'\n')
    print('PASS: 21 declaration audits and full-pool physical fixture agreement')

if __name__=='__main__':main()
