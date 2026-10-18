"""Validate the standalone Std-only subcubic certificates with local Lean."""

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
    formal = root / 'formal'
    build = root / 'build/subcubic-formal'
    (build / 'StarForming').mkdir(parents=True, exist_ok=True)
    executable = arguments.lean.resolve()
    version = subprocess.check_output([str(executable), '--version'], text=True).strip()
    if 'version 4.33.0' not in version:
        raise RuntimeError('Use the pinned Lean4.33.0 toolchain: ' + version)
    environment = dict(os.environ, LEAN_PATH=str(build))
    checks = []
    for module in ['StarForming/SubcubicCertificate.lean', 'StarFormingSubcubicAudit.lean']:
        command = [str(executable), module]
        if not module.endswith('Audit.lean'):
            command.extend(['-o', str((build / module).with_suffix('.olean'))])
        started = time.monotonic()
        result = subprocess.run(command, cwd=formal, env=environment,
                                text=True, capture_output=True)
        print(result.stdout, end='', flush=True)
        print(result.stderr, end='', flush=True)
        if result.returncode or re.search(
                r'error:|sorryAx|Lean\.ofReduceBool|Lean\.trustCompiler',
                result.stdout + result.stderr):
            raise RuntimeError('Formal check failed: ' + module)
        checks.append(dict(module=module, seconds=round(time.monotonic() - started, 3),
                           exit_code=result.returncode, stdout=result.stdout, stderr=result.stderr))
    declarations = re.findall(r"'([^']+)' (?:depends on axioms: \[([^\]]*)\]|does not depend on any axioms)",
                              checks[-1]['stdout'])
    if len(declarations) != 8:
        raise RuntimeError('Missing audit declarations')
    allowed = {'propext', 'Classical.choice', 'Quot.sound'}
    for declaration, axioms in declarations:
        if set(filter(None, map(str.strip, axioms.split(',')))) - allowed:
            raise RuntimeError('Unexpected axiom: ' + declaration)
    receipt = dict(status='ALL_CHECKS_PASSED',
                   checked_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                   lean_version=version, checks=checks,
                   maximum_rss_bytes=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
                   scope='Std-only: explicit base graph simplicity, local star predicate, deletion minimality, eight-set size, all4096mask dissociation port cap, four isolated-port attaining sets and general arithmetic double-counting bound. Cyclic gluing, exact global attainment, two-connectivity and global SF lower bound have written proofs; they are not asserted to be formalized here.')
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps(dict(status=receipt['status'], audited_declarations=len(declarations))))


if __name__ == '__main__':
    main()
