"""Scoped sequential local Lean audit, with explicit executable and preflight."""
import argparse
import datetime
import json
import os
from pathlib import Path
import re
import subprocess
import sys


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--lean', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    formal = root/'formal'
    listing = subprocess.check_output(['ps', '-axo', 'pid=,comm='], text=True)
    active = [line.strip() for line in listing.splitlines()
              if len(line.split(None, 1)) == 2
              and os.path.basename(line.split(None, 1)[1]) in ('lean', 'lake')]
    if active:
        raise RuntimeError('Selected local machine has active Lean/Lake: '+repr(active))
    if sys.platform == 'darwin':
        memory = subprocess.check_output(['memory_pressure'], text=True)
        preflight = dict(active_processes_by_comm_basename=active,
            memory_free_percentage=re.search(r'System-wide memory free percentage: (\d+%)', memory).group(1),
            physical_memory_bytes=int(subprocess.check_output(['sysctl', '-n', 'hw.memsize'], text=True)))
    else:
        preflight = dict(active_processes_by_comm_basename=active,
                         memory=Path('/proc/meminfo').read_text())
    lean = str(args.lean.resolve())
    version = subprocess.check_output([lean, '--version'], cwd=formal, text=True).strip()
    assert 'version 4.33.0' in version
    module = 'SubQuorum/JointTreeBetaCompensation.lean'
    source = (formal/module).read_text()
    assert not re.search(r'\b(sorry|admit|native_decide|axiom)\b', source)
    command = [lean, module]
    run = subprocess.run(command, cwd=formal, text=True, capture_output=True)
    print(run.stdout, end=''); print(run.stderr, end='')
    assert run.returncode == 0
    assert not re.search(r'warning:|error:|sorryAx|Lean.ofReduceBool|Lean.trustCompiler', run.stdout+run.stderr)
    audits = [line for line in run.stdout.splitlines()
              if 'depends on axioms' in line or 'does not depend' in line]
    assert len(audits) == 14
    for body in re.findall(r'depends on axioms: \[([^\]]*)\]', run.stdout):
        assert {a.strip() for a in body.split(',') if a.strip()} <= {'propext', 'Classical.choice', 'Quot.sound'}
    report = dict(status='PASS', checked_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        execution='Explicitly selected local executable; one small core/Omega module.',
        lean_version=version, preflight=preflight, module=module, command=command,
        axiom_audits=audits, sorry=False, native_decide=False,
        scope='Arbitrary-length indexed simple-path reassignment: domains, physical incidence under '
              'endpoint hypotheses, resource identities, no owner reuse, all old path assignments change, '
              'distinct beta root, and joint ledger.',
        not_formalized=['General graph/tree decomposition and unique rooted allocation',
                        'Maximum and minimum-weight matching theorems',
                        'Whole-support physical adapter and universal grid bound'])
    args.output.write_text(json.dumps(report, indent=2)+'\n')
    print('PASS: 14 scoped theorem axiom audits')


if __name__ == '__main__':
    main()
