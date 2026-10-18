"""Run the local general-degree symbolic Lean audit with resource evidence."""

import argparse
import datetime
import json
import os
from pathlib import Path
import re
import resource
import subprocess
import time


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--lean', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    processes = subprocess.check_output(['ps', '-axo', 'pid=,comm=,rss='], text=True)
    active = []
    for line in processes.splitlines():
        process_id, remainder = line.strip().split(None, 1)
        executable, resident = remainder.rsplit(None, 1)
        if Path(executable).name in {'lean', 'lake'}:
            active.append(dict(pid=int(process_id), executable=executable, rss_kib=int(resident)))
    memory = subprocess.check_output(['vm_stat'], text=True)
    print(json.dumps(dict(active_lean_lake=active, memory=memory)), flush=True)
    executable = arguments.lean.resolve()
    version = subprocess.check_output([str(executable), '--version'], text=True).strip()
    if 'version 4.33.0' not in version:
        raise RuntimeError('Use pinned Lean4.33.0: ' + version)
    build = root / 'build/regular-compensation-formal'
    (build / 'StarForming').mkdir(parents=True, exist_ok=True)
    environment = dict(os.environ, LEAN_PATH=str(build))
    checks = []
    for module in ('StarForming/RegularBound.lean', 'StarForming/CubicStability.lean',
                   'StarForming/RegularCompensation.lean', 'StarFormingRegularCompensationAudit.lean'):
        command = [str(executable), module]
        if not module.endswith('Audit.lean'):
            command += ['-o', str((build / module).with_suffix('.olean'))]
        started = time.monotonic()
        result = subprocess.run(command, cwd=root / 'formal', env=environment,
                                capture_output=True, text=True)
        print(result.stdout, end='', flush=True)
        print(result.stderr, end='', flush=True)
        if result.returncode or re.search(r'error:|sorryAx|Lean\.ofReduceBool|Lean\.trustCompiler',
                                         result.stdout + result.stderr):
            raise RuntimeError('Formal check failed: ' + module)
        checks.append(dict(module=module, seconds=round(time.monotonic() - started, 3),
                           stdout=result.stdout, stderr=result.stderr, exit_code=result.returncode))
    declarations = re.findall(r"'([^']+)' (?:depends on axioms: \[([^\]]*)\]|does not depend on any axioms)",
                              checks[-1]['stdout'])
    if len(declarations) != 4:
        raise RuntimeError('Missing audit declarations')
    for declaration, axioms in declarations:
        if set(filter(None, map(str.strip, axioms.split(',')))) - {
                'propext', 'Classical.choice', 'Quot.sound'}:
            raise RuntimeError('Unexpected axioms: ' + declaration)
    receipt = dict(status='ALL_CHECKS_PASSED',
                   checked_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                   lean_version=version, active_lean_lake_before_run=active,
                   memory_before_run=memory, checks=checks,
                   maximum_rss_bytes=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
                   scope='Four symbolic lemmas: unused capacity for arbitrary maximum degree>=3, weighted deficit accounting, regular coefficient conversion and arbitrary-degree integer gap arithmetic. Graph exchange, finite cardinal summation, construction and dissociation cap retain complete written proofs and independent controls; no full Lean graph theorem claimed.')
    arguments.output.write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps(dict(status=receipt['status'], audited_declarations=len(declarations))))


if __name__ == '__main__':
    main()
