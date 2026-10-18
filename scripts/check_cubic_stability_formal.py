"""Run local symbolic cubic-compensation Lean audits with a memory preflight."""

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
    active = [line.strip() for line in processes.splitlines()
              if len(line.split()) >= 3 and Path(line.split()[1]).name in {'lean', 'lake'}]
    memory = subprocess.check_output(['vm_stat'], text=True)
    print(json.dumps(dict(active_lean_lake=active, memory=memory)), flush=True)
    executable = arguments.lean.resolve()
    version = subprocess.check_output([str(executable), '--version'], text=True).strip()
    if 'version 4.33.0' not in version:
        raise RuntimeError('Use pinned Lean4.33.0: ' + version)
    build = root / 'build/cubic-compensation-formal'
    (build / 'StarForming').mkdir(parents=True, exist_ok=True)
    environment = dict(os.environ, LEAN_PATH=str(build))
    checks = []
    for module in ('StarForming/RegularBound.lean', 'StarForming/CubicStability.lean',
                   'StarFormingCubicStabilityAudit.lean'):
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
    if len(declarations) != 13:
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
                   scope='Arbitrary-type symbolic leaf adjacent failure, leaf failure other neighbor isolation, triangle-free adjacent high failure other neighbor isolation, shared leaf/high witness has its unique good support as owner; conditional residual accounting and two-exchange cardinal arithmetic, including corrected sharp leaf budget and exchange accounting,7s<=3n+2beta and gap n/14. Prior17s/3n-over34 arithmetic retained. Finite cardinal summation, injection counts and actual graph exchange construction retain full written proofs and independent controls; the graph-level theorem is not claimed fully Lean-formalized.')
    arguments.output.write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps(dict(status=receipt['status'], audited_declarations=len(declarations))))


if __name__ == '__main__':
    main()
