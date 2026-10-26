"""Scoped Lean audit with a fresh memory/process preflight per invocation."""
import argparse
import datetime
import json
from pathlib import Path
import re
import subprocess

from check_lower_guard_merger_frontier_formal import preflight,processes

if not __debug__:
    raise RuntimeError('Assertions required; do not use -O.')


def main():
    p=argparse.ArgumentParser();p.add_argument('--lean',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True);args=p.parse_args()
    root=Path(__file__).resolve().parents[1]
    source=root/'formal/SubQuorum/SuccessorGuardCompensation.lean'
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
        r"'SubQuorum\.SuccessorGuardCompensation\.[^']+'\s+(?:does not depend on any axioms|depends on axioms: \[[^\]]*\])",out)]
    assert len(audits)==19
    for body in re.findall(r'depends on axioms: \[([^\]]*)\]',out):
        assert {s.strip() for s in body.split(',') if s.strip()}<={'propext','Classical.choice','Quot.sound'}
    report=dict(status='PASS',checked_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        lean_version=version,preflight_before_version=before_version,preflight_before_compile=before_compile,
        active_processes_after_by_comm_basename=processes(),declaration_audits=audits,
        scope='Universal G/F13-site weighted identity and capacity16; f-only10-site identity, occupation13 equality data and actual-mate-coverage capacity12; successor-isolate injectivity, all-k component counts and permission cancellation; sharp patch counts. Kernel decides all17 integer-scaled periodic local constraints, four window cuts, five boundary types and period/omission sums; all-m positive fractional gap arithmetic. Three additional kernel checks verify the explicit6x22 counterexample grid feasibility/matching, supplied retainedR/P0 inclusion and component35/whole55 charges.',
        not_formalized=['All-k grid/free-graph coordinate classification, actual-matching boundary adapter, successor slot cover, original-tile token allocation, explicit patch freezing geometry and finite-chain/periodic adapter remain written general proofs with executable checks. No end-to-end all-k grid theorem. The explicit6x22 retainedR/P0 lists are supplied as concrete constants; their original-family/connected-component adapter and non-complete freezing remain Python/written. Fractional witness and actual integer counterexample have separate scopes; the latter refutes only the non-frozen permissions component cut.'],
        sorry=False,native_decide=False,new_axioms=False)
    args.output.write_text(json.dumps(report,indent=2)+'\n')
    print('PASS:19 successor compensation and periodic barrier Lean audits')


if __name__=='__main__':main()
