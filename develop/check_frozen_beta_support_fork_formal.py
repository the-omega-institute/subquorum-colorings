"""Reproduce the scoped Lean audit with an explicitly chosen local executable."""
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
    formal, build = root/'formal', root/'build/frozen-beta-support-fork-formal'
    lean = args.lean.resolve()
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
    version = subprocess.check_output([str(lean), '--version'], cwd=formal, text=True).strip()
    assert 'version 4.33.0' in version
    (build/'SubQuorum').mkdir(parents=True, exist_ok=True)
    environment = dict(os.environ, LEAN_PATH=str(build)+':'+str(formal))
    modules = [('SubQuorum/BTColumnCorridorObstruction.lean', 16),
               ('SubQuorum/FrozenBetaSupportFork.lean', 12)]
    checks = []
    for index, (module, expected) in enumerate(modules):
        source = (formal/module).read_text()
        assert not re.search(r'\b(sorry|admit|native_decide|axiom)\b', source)
        command = [str(lean), module]
        if index == 0:
            command += ['-o', str((build/module).with_suffix('.olean'))]
        run = subprocess.run(command, cwd=formal, env=environment, text=True, capture_output=True)
        print(run.stdout, end=''); print(run.stderr, end='')
        assert run.returncode == 0
        assert not re.search(r'warning:|error:|sorryAx|Lean.ofReduceBool|Lean.trustCompiler', run.stdout+run.stderr)
        audits = [line for line in run.stdout.splitlines()
                  if 'depends on axioms' in line or 'does not depend' in line]
        assert len(audits) == expected
        for body in re.findall(r'depends on axioms: \[([^\]]*)\]', run.stdout):
            assert {a.strip() for a in body.split(',') if a.strip()} <= {'propext', 'Classical.choice', 'Quot.sound'}
        checks.append(dict(module=module, exit_code=run.returncode, command=command, axiom_audits=audits))
    report = dict(status='PASS', checked_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        execution='Explicitly selected local executable; sequential dependency and new module.',
        lean_version=version, preflight=preflight, checks=checks,
        scope='Concrete16by14feasible geometry;66endpoint strict-rank complete freezing; '
              'all6original open strands and8PPcycles;two distinct alpha-to-beta links; '
              'interior beta-body gap and pure-cycle opposite boundary; '
              'arbitrary-copy occupied-point separation and distinct copied units; scalar ledgers.',
        not_formalized=['Whole-support original interval construction and exact inventory',
                        'Reserved and unrestricted compensation optimum and min link cost',
                        'All-q physical stacking/padding adapter'],
        sorry=False, native_decide=False)
    args.output.write_text(json.dumps(report, indent=2)+'\n')
    print('PASS:12 new theorem audits and16 dependency audits')


if __name__ == '__main__':
    main()
