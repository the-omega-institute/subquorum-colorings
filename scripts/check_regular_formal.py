"""Run the symbolic degree-capacity proof audit with pinned local Lean."""

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
        parts = line.strip().split()
        if len(parts) >= 3 and Path(parts[1]).name in {'lean', 'lake'}:
            active.append(line.strip())
    memory = subprocess.check_output(['vm_stat'], text=True)
    print(json.dumps(dict(active_lean_lake=active, memory=memory)), flush=True)
    executable = arguments.lean.resolve()
    version = subprocess.check_output([str(executable), '--version'], text=True).strip()
    if 'version 4.33.0' not in version:
        raise RuntimeError('Use pinned Lean4.33.0: ' + version)
    build = root / 'build/regular-bound-formal'
    (build / 'StarForming').mkdir(parents=True, exist_ok=True)
    environment = dict(os.environ, LEAN_PATH=str(build))
    checks = []
    for module in ('StarForming/RegularBound.lean', 'StarFormingRegularAudit.lean'):
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
    if len(declarations) != 12:
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
                   scope='Symbolic, arbitrary-type proof: a covered deletion in a minimal selection has an outside failure witness; a high vertex is such a deletion; witness sets for different high vertices are disjoint; without selected isolates a selected leaf adjacent to a high vertex has a private outside witness; a high witness has no three selected neighbors and a nonadjacent witness has at most one; degree-capacity arithmetic, conditional cut accounting and all-degree regular/cubic/grid-boundary inequalities. Finite graph cardinal summation, full graph-level order bound, complete regular equality partition, matching exchange and grid corollary have written proofs and independent controls; they are not claimed fully formalized here. No finite graph certificates or compiler-trust axioms used.')
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps(dict(status=receipt['status'], audited_declarations=len(declarations))))


if __name__ == '__main__':
    main()
