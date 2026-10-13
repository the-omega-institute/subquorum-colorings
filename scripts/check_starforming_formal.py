"""Check the all-index witness-preservation theorem with a selected local cache."""
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
    parser.add_argument('--package-cache', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    formal = root / 'formal'
    cache = arguments.package_cache.resolve()
    executable = arguments.lean.resolve()
    version = subprocess.check_output([str(executable), '--version'], text=True).strip()
    if 'version 4.33.0' not in version:
        raise RuntimeError(version)
    manifest = json.loads((formal / 'lake-manifest.json').read_text())
    paths = []
    for package in manifest['packages']:
        directory = cache / package['name']
        revision = subprocess.check_output(
            ['git', '-C', str(directory), 'rev-parse', 'HEAD'], text=True).strip()
        if revision != package['rev']:
            raise RuntimeError('Cache revision mismatch: ' + package['name'])
        paths.append(str(directory / '.lake/build/lib/lean'))
    build = root / 'build/starforming-formal'
    (build / 'StarForming').mkdir(parents=True, exist_ok=True)
    environment = dict(os.environ, LEAN_PATH=':'.join([str(build), str(formal)] + paths))
    checks = []
    for module in ['StarForming/Amplification.lean', 'StarFormingAudit.lean']:
        command = [str(executable), module]
        if module != 'StarFormingAudit.lean':
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
                           exit_code=result.returncode, stdout=result.stdout,
                           stderr=result.stderr))
    declarations = re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]",
                              checks[-1]['stdout'])
    if len(declarations) != 7:
        raise RuntimeError('Missing declarations in axiom audit')
    allowed = {'propext', 'Classical.choice', 'Quot.sound'}
    for declaration, axioms in declarations:
        if set(filter(None, map(str.strip, axioms.split(',')))) - allowed:
            raise RuntimeError('Unexpected axiom: ' + declaration)
    receipt = dict(status='ALL_CHECKS_PASSED',
                   checked_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                   lean_version=version, checks=checks,
                   maximum_rss_bytes=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
                   scope='Literal/local equivalence, arbitrary-interface bipartiteness, '
                         'minimal star formation, deletion witnesses and 6 times index count. '
                         'Dissociation optimum and two-connectivity have written proofs only.')
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps(dict(status=receipt['status'], audited_declarations=len(declarations))))


if __name__ == '__main__':
    main()
