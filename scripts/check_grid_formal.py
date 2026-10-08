"""Verify the new grid modules with an explicitly selected executable and cache."""
import argparse
import datetime
import hashlib
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
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    formal = root/'formal'
    output = args.output.resolve()
    cache = args.package_cache.resolve()
    executable = args.lean.resolve()
    manifest = json.loads((formal/'lake-manifest.json').read_text())
    version = subprocess.check_output([str(executable), '--version'], text=True).strip()
    assert 'version 4.33.0' in version, version
    dependencies = {}
    paths = []
    for package in manifest['packages']:
        directory = cache/package['name']
        revision = subprocess.check_output(['git', '-C', str(directory), 'rev-parse', 'HEAD'], text=True).strip()
        assert revision == package['rev'], package['name']
        dependencies[package['name']] = revision
        paths.append(str(directory/'.lake/build/lib/lean'))
    build = root/'build/grid-formal'
    (build/'SubQuorum').mkdir(parents=True, exist_ok=True)
    environment = dict(os.environ, LEAN_PATH=':'.join([str(build), str(formal)]+paths))
    modules = ['SubQuorum/BandCompensation.lean', 'SubQuorum/EndpointCompensation.lean']
    checks = []
    for module in modules+['GridAudit.lean']:
        command = [str(executable), module]
        if module in modules:
            command.extend(['-o', str((build/module).with_suffix('.olean'))])
        started = time.monotonic()
        result = subprocess.run(command, cwd=formal, env=environment, text=True, capture_output=True)
        print(result.stdout, end='', flush=True)
        print(result.stderr, end='', flush=True)
        assert result.returncode == 0, module
        assert not re.search(r'error:|sorryAx|Lean\.ofReduceBool|Lean\.trustCompiler', result.stdout+result.stderr), module
        checks.append(dict(module=module, exit_code=result.returncode, seconds=round(time.monotonic()-started, 3),
                           stdout=result.stdout, stderr=result.stderr))
    audit = checks[-1]['stdout']
    expected = ['band_blank_surplus', 'parity_matching_band_compensation', 'parity_charge_compensation',
                'one_export_source_compensation', 'terminal_color_balance',
                'one_color_injective_compensation', 'allocation_component', 'allocation_injective']
    declarations = re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]", audit, re.DOTALL)
    assert len(declarations) == len(expected), declarations
    axioms = {}
    allowed = {'propext', 'Classical.choice', 'Quot.sound'}
    for declaration, body in declarations:
        actual = {item.strip() for item in body.split(',') if item.strip()}
        assert actual <= allowed, (declaration, actual)
        axioms[declaration] = sorted(actual)
    assert all(any(declaration.endswith('.'+name) for declaration in axioms) for name in expected)
    sources = [formal/module for module in modules+['GridAudit.lean']]
    sources.extend([formal/'Audit.lean', formal/'lakefile.toml', formal/'lean-toolchain',
                    formal/'lake-manifest.json', Path(__file__)])
    for source in sources[:3]:
        assert not re.search(r'\b(sorry|admit|native_decide|axiom)\b', source.read_text()), source
    report = dict(status='LEAN_KERNEL_CHECKS_PASSED', checked_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                  lean_version=version, user_selected_execution='local_machine', concurrent_module_builds=1,
                  dependencies=dependencies, checks=checks, audited_axioms=axioms,
                  max_child_rss_bytes=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
                  source_sha256={str(source.relative_to(root)):hashlib.sha256(source.read_bytes()).hexdigest() for source in sources},
                  scope='All-length band labels/counting, boundary parity and conditional regional-charge consequences; endpoint involutions, per-component allocations and global no-reuse injection. Full-grid tiling/geometry adapters and unrestricted conjecture are not formalized.')
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(dict(status=report['status'], audited_theorems=len(axioms),
                         max_child_rss_bytes=report['max_child_rss_bytes'])))


if __name__ == '__main__':
    main()
