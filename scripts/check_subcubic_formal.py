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
    parser.add_argument('--exact', action='store_true')
    parser.add_argument('--cubic', action='store_true')
    arguments = parser.parse_args()
    if arguments.exact and arguments.cubic:
        parser.error('Choose one certificate extension per run.')
    root = Path(__file__).resolve().parents[1]
    formal = root / 'formal'
    build = root / ('build/cubic-formal' if arguments.cubic else
                    'build/subcubic-exact-formal' if arguments.exact else 'build/subcubic-formal')
    (build / 'StarForming').mkdir(parents=True, exist_ok=True)
    executable = arguments.lean.resolve()
    version = subprocess.check_output([str(executable), '--version'], text=True).strip()
    if 'version 4.33.0' not in version:
        raise RuntimeError('Use the pinned Lean4.33.0 toolchain: ' + version)
    environment = dict(os.environ, LEAN_PATH=str(build))
    checks = []
    modules = ['StarForming/SubcubicCertificate.lean', 'StarForming/SubcubicExact.lean',
               'StarFormingSubcubicExactAudit.lean'] if arguments.exact else [
                   'StarForming/SubcubicCertificate.lean', 'StarFormingSubcubicAudit.lean']
    if arguments.cubic:
        modules = ['StarForming/SubcubicCertificate.lean', 'StarForming/CubicCertificate.lean',
                   'StarFormingCubicAudit.lean']
    for module in modules:
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
    if len(declarations) != (9 if arguments.cubic else 5 if arguments.exact else 10):
        raise RuntimeError('Missing audit declarations')
    allowed = {'propext', 'Classical.choice', 'Quot.sound'}
    for declaration, axioms in declarations:
        if set(filter(None, map(str.strip, axioms.split(',')))) - allowed:
            raise RuntimeError('Unexpected axiom: ' + declaration)
    receipt = dict(status='ALL_CHECKS_PASSED',
                   checked_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                   lean_version=version, checks=checks,
                   maximum_rss_bytes=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
                   scope='Std-only: explicit base graph simplicity, local star predicate, deletion minimality, eight-set size, forced adjacent certificates and their failed simultaneous exchange, all4096mask dissociation port cap, four isolated-port attaining sets and general arithmetic double-counting bound. Cyclic gluing, exact global attainment, two-connectivity and global SF lower bound have written proofs; they are not asserted to be formalized here.')
    if arguments.exact:
        receipt['scope'] = 'Std-only: generic supported deletion, fixed ten-vertex dense-core certificate, lifting through an induced embedding, per-core cap for arbitrary outside graphs attached only at labels3,11, and disjoint-core arithmetic accounting. Global J_r embedding, attainment and exact SF equality are written proofs, not asserted to be fully formalized here. The finite certificate supplements the analytic case proof.'
    if arguments.cubic:
        receipt['scope'] = 'Std-only: generic star-formation and inclusion-minimality invariance under arbitrary rewiring of edges outside a fixed selection; explicit Heawood graph simplicity/cubic degree, eight-set formation, deletion failures, minimality and cardinality; conditional dense-block and gap arithmetic. Fano dissociation geometry, saturated-port lemma, cyclic composition, connectivity, girth and global attainment have written proofs, not full new Lean formalizations.'
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps(dict(status=receipt['status'], audited_declarations=len(declarations))))


if __name__ == '__main__':
    main()
