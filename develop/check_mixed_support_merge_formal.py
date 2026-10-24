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
    formal, build = root/'formal', root/'build/mixed-support-merge-formal'
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
    modules = [('SubQuorum/MixedSupportComponentMerges.lean', 11)]
    checks = []
    for index, (module, expected) in enumerate(modules):
        source = (formal/module).read_text()
        assert not re.search(r'\b(sorry|admit|native_decide|axiom)\b', source)
        command = [str(lean), module]
        if index < len(modules)-1:
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
        scope='Arbitrary-length indexed alternating augmentation preserves old paid owners '
              'and used resource identities, pays the new root with one new unit and has no '
              'owner or unit reuse; signed component deficit and min(d,s) gain arithmetic; constant ledger.',
        not_formalized=['General finite component partition and reserve cardinalities',
                        'Existence of augmenting paths and full allocation optimum',
                        'Whole-support mixed extension adapter and physical controls'],
        sorry=False, native_decide=False)
    args.output.write_text(json.dumps(report, indent=2)+'\n')
    print('PASS:11 standalone theorem audits')


if __name__ == '__main__':
    main()
