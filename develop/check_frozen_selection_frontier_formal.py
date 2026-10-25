"""Scoped local Lean audit of the frozen arbitrary-selection repair frontier."""
import argparse
import datetime
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

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
    path=root/'formal/SubQuorum/FrozenSelectionFrontier.lean';source=path.read_text()
    assert not re.search(r'\b(sorry|admit|native_decide|axiom)\b',source)
    lean=str(args.lean.resolve());version=subprocess.check_output([lean,'--version'],text=True).strip()
    assert 'version 4.33.0' in version
    with tempfile.TemporaryDirectory(prefix='selection-frontier-lean-') as tmp:
        tmpdir=Path(tmp);(tmpdir/'SubQuorum').mkdir()
        result=subprocess.run([lean,str(path)],cwd=root/'formal',text=True,capture_output=True)
    output=result.stdout+result.stderr;print(output,end='',flush=True)
    assert result.returncode==0
    assert not re.search(r'warning:|error:|sorryAx|Lean.ofReduceBool|Lean.trustCompiler',output)
    audits=[s for s in output.splitlines() if 'depends on axioms' in s or 'does not depend' in s]
    assert len(audits)==19
    for body in re.findall(r'depends on axioms: \[([^\]]*)\]',output):
        assert {a.strip() for a in body.split(',') if a.strip()} <= {'propext','Classical.choice','Quot.sound'}
    report=dict(status='PASS',checked_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),lean_version=version,
        preflight=preflight,active_processes_after_by_comm_basename=processes(),declaration_audits=audits,
        scope='Leaf witnesses force the two permissible seals; exact central-tip identity and unbounded list induction; disjoint nonnegative loss arithmetic; cover/payment coupled frontier; slack form; arbitrary-exchange net-loss lower bound; Pareto upper bound; every sealed maximum has k alphas and deficit k; sharp attainer arithmetic and conditional maximum packaging; complete fixed-central-alpha/beta inventory upper bound and max/min attainer arithmetic; arbitrary unsealed-T boundary-defect coupling and necessary count of unfrozen designated leaves; arbitrary-length owner-walk module invariance, uniqueness of reached central body, and central beta unreachability.',
        not_formalized=['Coordinate classification of bodies and leaf witness exclusion, validity and disjointness of the geometric cover charges, full-network source-route closure and resource injection, and uniform geometric freezing of all attainers; these have written proofs and executable checks.'],
        sorry=False,native_decide=False,new_axioms=False)
    args.output.write_text(json.dumps(report,indent=2)+'\n')
    print('PASS: 19 frozen-selection-frontier audits')

if __name__=='__main__':main()
