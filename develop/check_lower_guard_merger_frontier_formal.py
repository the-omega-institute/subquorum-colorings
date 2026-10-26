"""Scoped local Lean audit; preflight precedes each executable invocation."""
import argparse
import datetime
import json
import os
from pathlib import Path
import re
import subprocess

if not __debug__:
    raise RuntimeError('Assertions required; do not use -O.')


def processes():
    lines = subprocess.check_output(['ps','-axo','pid=,comm='],text=True).splitlines()
    return [s.strip() for s in lines if len(s.split(None,1)) == 2 and
            os.path.basename(s.split(None,1)[1]) in ('lean','lake')]


def preflight():
    memory = subprocess.check_output(['memory_pressure'],text=True)
    return dict(active_processes_by_comm_basename=processes(),
        memory_free_percentage=re.search(r'System-wide memory free percentage: (\d+%)',memory).group(1),
        physical_memory_bytes=int(subprocess.check_output(['sysctl','-n','hw.memsize'],text=True)),
        execution='User authorized local machine; one standalone Std-only module; no shared build or CI changes.')


def main():
    p=argparse.ArgumentParser();p.add_argument('--lean',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    args=p.parse_args();root=Path(__file__).resolve().parents[1]
    source=root/'formal/SubQuorum/LowerGuardMergerFrontier.lean'
    assert not re.search(r'\b(sorry|admit|native_decide|axiom)\b',source.read_text())
    before_version=preflight();print(json.dumps(before_version),flush=True)
    version=subprocess.check_output([str(args.lean),'--version'],text=True).strip()
    assert 'version 4.33.0' in version
    before_compile=preflight();print(json.dumps(before_compile),flush=True)
    result=subprocess.run([str(args.lean),str(source)],cwd=root/'formal',text=True,capture_output=True)
    out=result.stdout+result.stderr;print(out,end='',flush=True)
    assert result.returncode==0
    assert not re.search(r'warning:|error:|sorryAx|Lean.ofReduceBool|Lean.trustCompiler',out)
    audits=[' '.join(s.split()) for s in re.findall(
        r"'SubQuorum\.LowerGuardMergerFrontier\.[^']+'\s+(?:does not depend on any axioms|depends on axioms: \[[^\]]*\])",out)]
    assert len(audits)==14
    for body in re.findall(r'depends on axioms: \[([^\]]*)\]',out):
        assert {a.strip() for a in body.split(',') if a.strip()} <= {'propext','Classical.choice','Quot.sound'}
    report=dict(status='PASS',checked_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        lean_version=version,preflight_before_version=before_version,preflight_before_compile=before_compile,
        active_processes_after_by_comm_basename=processes(),declaration_audits=audits,
        scope='Universal13-site weighted identity and capacity16 in doubled occupation; seven-site identity/bound11/equality obstruction under actual mate coverage gives10; all-k two-guard count cancellation and sharp margin; strict witness/mate-plus-one exclusion and selection forced by two alternative traps; lower-only sharp patch counts and signed exterior cut.',
        not_formalized=['All-k free-coordinate classification and boundary adapter, actual guard-implication geometry, full explicit patch freezing schedule and original-tile physical token adapter remain general written proofs with executable checks. Exact sharp frozen attainment inherits the previous all-subset upper-guard construction, which retains lower guards. Not an end-to-end all-k Lean grid theorem; arbitrary other T/P withdrawals and universal5/6 remain open.'],
        sorry=False,native_decide=False,new_axioms=False)
    args.output.write_text(json.dumps(report,indent=2)+'\n')
    print('PASS: 14 lower-guard merger frontier Lean audits')


if __name__=='__main__':
    main()
