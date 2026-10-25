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
    fixture=json.loads((root/'develop/fixtures/interface_reserve_exchange.json').read_text())
    path=root/'formal/SubQuorum/InterfaceReserveReoptimization.lean';source=path.read_text()
    assert not re.search(r'\b(sorry|admit|native_decide|axiom)\b',source)
    def read(name):
        m=re.search(r'^def '+name+r' : .*? := (.+)$',source,re.M)
        assert m,name
        return json.loads(json.dumps(ast.literal_eval(m.group(1))))
    for name,key in [('shared','shared'),('privateUnit','private'),('lowerLinks','old_baseline_links'),
                     ('upperLinks','rerouted_old_links'),('actualPairs','pairs'),('actualLinks','links')]:
        assert read(name)==fixture[key],name
    assert read('actualAlphaOwners')==[fixture['old_owner'],fixture['interface_owner']]
    Q={tuple(x) for x in fixture['available_original_units']}
    actual={o:{tuple(j) for j in js}&Q for o,js in fixture['support']}
    expected={1:set(),4:{tuple(fixture['shared'])},0:{tuple(fixture['private'])},11:{tuple(fixture['shared'])}}
    assert all(actual[o]==expected.get(o,set()) for o in actual)
    for owner,definition in [(1,'[]'),(4,'[shared]'),(0,'[privateUnit]'),(11,'[shared]')]:
        assert f'| {owner} => {definition}' in source
    lean=str(args.lean.resolve());version=subprocess.check_output([lean,'--version'],text=True).strip()
    assert 'version 4.33.0' in version
    result=subprocess.run([lean,str(path)],cwd=root/'formal',text=True,capture_output=True)
    output=result.stdout+result.stderr;print(output,end='',flush=True)
    assert result.returncode==0
    assert not re.search(r'warning:|error:|sorryAx|Lean.ofReduceBool|Lean.trustCompiler',output)
    audits=[x for x in output.splitlines() if 'depends on axioms' in x or 'does not depend' in x]
    assert len(audits)==14
    for body in re.findall(r'depends on axioms: \[([^\]]*)\]',output):
        assert {a.strip() for a in body.split(',') if a.strip()} <= {'propext','Classical.choice','Quot.sound'}
    after=subprocess.check_output(['ps','-axo','pid=,comm='],text=True)
    after=[x.strip() for x in after.splitlines() if len(x.split(None,1))==2 and os.path.basename(x.split(None,1)[1]) in ('lean','lake')]
    report=dict(status='PASS',checked_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),lean_version=version,
        preflight=preflight,active_processes_after_by_comm_basename=after,declaration_audits=audits,
        scope='Simple injective finite path cannot reenter super-source or reverse any source arc; saturated-source and iteration invariants; exact interface gain; attained cut/deficit and full-payment equivalences; comparison to fixed pack; global deficit; positive physical slack; fixture-aligned original resources, owner pairs and declared route links with distinct final payments.',
        not_formalized=['Integral max-flow/min-cut and existence of a finite terminating augmentation sequence',
            'Whole-beta normalization and geometric embedding into the full restored network',
            'General coordinate-to-owner/resource adapter and all-W freezing/construction'],
        sorry=False,native_decide=False,new_axioms=False)
    args.output.write_text(json.dumps(report,indent=2)+'\n')
    print('PASS: 14 declaration audits and actual compiled route/resource agreement')

if __name__=='__main__':main()
