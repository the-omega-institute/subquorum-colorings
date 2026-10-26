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
    source=root/'formal/SubQuorum/ConnectedBandRetainedPhases.lean'
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
        r"'SubQuorum\.ConnectedBandRetainedPhases\.[^']+'\s+(?:does not depend on any axioms|depends on axioms: \[[^\]]*\])",out)]
    assert len(audits)==2
    for body in re.findall(r'depends on axioms: \[([^\]]*)\]',out):
        assert {s.strip() for s in body.split(',') if s.strip()}<={'propext','Classical.choice','Quot.sound'}
    report=dict(status='PASS',checked_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        lean_version=version,preflight_before_version=before_version,preflight_before_compile=before_compile,
        active_processes_after_by_comm_basename=processes(),declaration_audits=audits,
        scope='Two axiom-free kernel computations verify the corrected retained phases (row0 residues1,3,5; row1 residues2,4), the entire periodic whole-board occupation/wedge/full-degree system and old endpoint matching saturation. Explicitly excludes incorrect row0 residue0.',
        not_formalized=['All-length finite old-family to periodic coordinate adapter remains a written proof and exact Python check. No integer/frozen or end-to-end grid theorem.'],
        sorry=False,native_decide=False,new_axioms=False)
    args.output.write_text(json.dumps(report,indent=2)+'\n')
    print('PASS:2 corrected periodic whole-board Lean audits')


if __name__=='__main__':main()
