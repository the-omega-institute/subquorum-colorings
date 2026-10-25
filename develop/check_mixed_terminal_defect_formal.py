"""Scoped local Lean audit of mixed-direction terminal and seam defects."""
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
    path=root/'formal/SubQuorum/MixedTerminalDefect.lean';source=path.read_text()
    assert not re.search(r'\b(sorry|admit|native_decide|axiom)\b',source)
    lean=str(args.lean.resolve());version=subprocess.check_output([lean,'--version'],text=True).strip()
    assert 'version 4.33.0' in version
    with tempfile.TemporaryDirectory(prefix='mixed-terminal-lean-') as tmp:
        tmpdir=Path(tmp);(tmpdir/'SubQuorum').mkdir()
        result=subprocess.run([lean,str(path)],cwd=root/'formal',text=True,capture_output=True)
    output=result.stdout+result.stderr;print(output,end='',flush=True)
    assert result.returncode==0
    assert not re.search(r'warning:|error:|sorryAx|Lean.ofReduceBool|Lean.trustCompiler',output)
    audits=[s for s in output.splitlines() if 'depends on axioms' in s or 'does not depend' in s]
    assert len(audits)==16
    for body in re.findall(r'depends on axioms: \[([^\]]*)\]',output):
        assert {a.strip() for a in body.split(',') if a.strip()} <= {'propext','Classical.choice','Quot.sound'}
    report=dict(status='PASS',checked_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),lean_version=version,
        preflight=preflight,active_processes_after_by_comm_basename=processes(),declaration_audits=audits,
        scope='Local degree3/4 and zero-incidence classification for arbitrary Boolean neighbour predicates; selected partner forbids parallel mate partner occupation; injectivity of seam-terminal charges under explicit matching-edge/opposite-normal adapters; joint seam-tax, single-edge full port allocation implication, coefficient-one ledger arithmetic; arbitrary-length private-support list loss and paid/unpaid induction; every maximum has full deficit; Pareto and sharp attainer arithmetic.',
        not_formalized=['Full rectangle parity/coordinate and M/PP-owner adapters, physical forest incidence degree and path/cycle matching theorem, exact grid support/private-unit and common all-size freezing geometry. These have general written proofs and executable checks; not end-to-end Lean.'],
        sorry=False,native_decide=False,new_axioms=False)
    args.output.write_text(json.dumps(report,indent=2)+'\n')
    print('PASS: 16 mixed-terminal-defect audits')

if __name__=='__main__':main()
