"""Scoped local Lean audit; record resources and preserve unrelated processes."""
import argparse
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
    build=root/'build/selection-maximum-singleton-formal';(build/'SubQuorum').mkdir(parents=True,exist_ok=True)
    lean=str(args.lean.resolve());version=subprocess.check_output([lean,'--version'],text=True).strip();assert 'version 4.33.0' in version
    checks=[];env=dict(os.environ,LEAN_PATH=str(build)+':'+str(formal))
    for filename,n in [('BTColumnCorridorObstruction',16),('SelectionMaximumSingleton',17)]:
        path='SubQuorum/'+filename+'.lean';source=(formal/path).read_text()
        assert not re.search(r'\b(sorry|admit|native_decide|axiom)\b',source)
        command=[lean,path]
        if filename=='BTColumnCorridorObstruction':command+=['-o',str(build/'SubQuorum'/f'{filename}.olean')]
        result=subprocess.run(command,cwd=formal,env=env,text=True,capture_output=True)
        print(result.stdout,end='',flush=True);print(result.stderr,end='',flush=True)
        assert result.returncode==0
        assert not re.search(r'warning:|error:|sorryAx|Lean.ofReduceBool|Lean.trustCompiler',result.stdout+result.stderr)
        audits=[x for x in result.stdout.splitlines() if 'depends on axioms' in x or 'does not depend' in x];assert len(audits)==n
        for body in re.findall(r'depends on axioms: \[([^\]]*)\]',result.stdout):
            assert {a.strip() for a in body.split(',') if a.strip()} <= {'propext','Classical.choice','Quot.sound'}
        checks.append(dict(module=path,exit_code=result.returncode,axiom_audits=audits))
    report=dict(status='PASS',checked_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),lean_version=version,
        preflight=preflight,checks=checks,scope='General isolated-selection addability and candidate-hull isolation; maximal-compatible closure; freezing under selected-set extension; all-W scalar tile-bound ledger; concrete W8 feasible72T geometry, all68 frozen endpoints, and empty reachable support certificate.',
        not_formalized=['All-W coordinate candidate hull and tile upper table','No-beta cancellation-to-route adapter','General even-width boundary forest compiler','All-W four-patch cover-to-count specialization and global maximum over changing P'],
        sorry=False,native_decide=False)
    args.output.write_text(json.dumps(report,indent=2)+'\n')
    print('PASS: 17 new and 16 dependency declaration audits')

if __name__=='__main__':main()
