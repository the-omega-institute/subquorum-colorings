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
    source=root/'formal/SubQuorum/ConnectedBandMateCoverageBarrier.lean'
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
        r"'SubQuorum\.ConnectedBandMateCoverageBarrier\.[^']+'\s+(?:does not depend on any axioms|depends on axioms: \[[^\]]*\])",out)]
    assert len(audits)==4
    for body in re.findall(r'depends on axioms: \[([^\]]*)\]',out):
        assert {s.strip() for s in body.split(',') if s.strip()}<={'propext','Classical.choice','Quot.sound'}
    report=dict(status='PASS',checked_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        lean_version=version,preflight_before_version=before_version,preflight_before_compile=before_compile,
        active_processes_after_by_comm_basename=processes(),declaration_audits=audits,
        scope='Three axiom-free kernel checks establish all17 scaled92 periodic bounds/anchors/wedges/full-degree/stars/basic mate-coverage and four window cuts, six patched boundary types and period/omission/endpoint sums. All-m positive gap arithmetic is proved over integers.',
        not_formalized=['All-m geometric coordinate reduction to periodic/boundary cases and charge adapter are general written proofs with exact Python controls. Not an actual fractional edge matching, integer or frozen configuration, or a whole-board counterexample. Outside the companion Oracle review input.'],
        sorry=False,native_decide=False,new_axioms=False)
    args.output.write_text(json.dumps(report,indent=2)+'\n')
    print('PASS:4 strengthened mate-coverage barrier Lean audits')


if __name__=='__main__':main()
