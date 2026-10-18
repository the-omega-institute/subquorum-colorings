"""Check the general graph-cover theorem in local Lean with resource evidence."""

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
    parser.add_argument('--audit', choices=('cover', 'dissociation', 'heawood', 'cubic-paths', 'padding-rings', 'triple-ports', 'multi-ports', 'long-core', 'long-core-upper'), default='cover')
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
    build = root / {'cover': 'build/cover-pullback-formal',
                    'dissociation': 'build/dissociation-cover-formal',
                    'heawood': 'build/heawood-certificates-formal',
                    'cubic-paths': 'build/cubic-path-accounting-formal',
                    'padding-rings': 'build/cubic-padding-ring-formal',
                    'triple-ports': 'build/cubic-triple-port-formal',
                    'multi-ports': 'build/heawood-multiport-formal',
                    'long-core': 'build/long-core-word-formal',
                    'long-core-upper': 'build/long-core-upper-formal'}[arguments.audit]
    (build / 'StarForming').mkdir(parents=True, exist_ok=True)
    environment = dict(os.environ, LEAN_PATH=str(build))
    checks = []
    modules = ('StarForming/RegularBound.lean', 'StarForming/CoverPullback.lean')
    if arguments.audit == 'cover':
        modules += ('StarForming/CoverStability.lean', 'StarFormingCoverPullbackAudit.lean')
    elif arguments.audit == 'dissociation':
        modules += ('StarForming/DissociationCover.lean', 'StarFormingDissociationCoverAudit.lean')
    elif arguments.audit == 'heawood':
        modules += ('StarForming/DissociationCover.lean', 'StarForming/HeawoodCertificates.lean',
                    'StarFormingHeawoodCertificatesAudit.lean')
    elif arguments.audit == 'cubic-paths':
        modules += ('StarForming/CubicStability.lean', 'StarForming/DissociationCover.lean',
                    'StarForming/CubicPathAccounting.lean',
                    'StarFormingCubicPathAccountingAudit.lean')
    elif arguments.audit == 'padding-rings':
        modules += ('StarForming/CubicPaddingRings.lean', 'StarFormingCubicPaddingRingsAudit.lean')
    elif arguments.audit == 'triple-ports':
        modules += ('StarForming/CubicTriplePorts.lean', 'StarFormingCubicTriplePortsAudit.lean')
    elif arguments.audit == 'multi-ports':
        modules += ('StarForming/DissociationCover.lean', 'StarForming/HeawoodMultiport.lean',
                    'StarFormingHeawoodMultiportAudit.lean')
    elif arguments.audit == 'long-core':
        modules += ('StarForming/DissociationCover.lean', 'StarForming/LongCoreWord.lean',
                    'StarFormingLongCoreWordAudit.lean')
    else:
        modules += ('StarForming/DissociationCover.lean', 'StarForming/LongCoreWord.lean',
                    'StarForming/LongCoreUpper.lean', 'StarFormingLongCoreUpperAudit.lean')
    for module in modules:
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
    expected = {'cover': 22, 'dissociation': 5, 'heawood': 6, 'cubic-paths': 12,
                'padding-rings': 7, 'triple-ports': 8, 'multi-ports': 9, 'long-core': 9,
                'long-core-upper': 10}
    if len(declarations) != expected[arguments.audit]:
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
                   scope='Full graph-level exact cover-stability criterion: safe certificates suffice for every locally bijective map; a missing certificate gives a canonical two-sheeted cover with an explicitly redundant selected lift. Includes local cover construction, deletion formation, nonminimality, exact equivalence for canonical tests, boundary-triangle-free and triangle-free corollaries. No finiteness assumption. Connectedness of the canonical counter-cover and cardinal SF corollaries retain written proofs.')
    if arguments.audit == 'dissociation':
        receipt['scope'] = ('General graph-level dissociation pullback and reflection through '
                            'surjective locally bijective maps; local four-cycle exclusion and '
                            'capacity two. Global fractional four-cycle summation and prism '
                            'parameter/covering formulas retain written proofs.')
    if arguments.audit == 'heawood':
        receipt['scope'] = ('Two explicit 16-vertex dissociation certificates in the scalar/Jordan '
                            'Heawood double covers, their cardinalities, and two conditional '
                            'gap-density arithmetic implications. Matrix classification, '
                            'higher-cover factorization and finite-fiber counting retain written proofs.')
    if arguments.audit == 'cubic-paths':
        receipt['scope'] = ('Two general graph lemmas: exclusion of extra-leaf failure witnesses '
                            'from the chosen high-witness image and simultaneous isolated-pair '
                            'augmentation preserving dissociation. Ten conditional arithmetic lemmas for '
                            'path endpoint counts, quantized bipartition balance, exchange debt '
                            'and equality gap, isolate compensation and positive path slack. '
                            'Full finite normal-form characterization, '
                            'cardinal path decomposition and component summation have written proofs.')
    if arguments.audit == 'padding-rings':
        receipt['scope'] = ('Seven declarations: finite six-periodic weight identities and cut-pair '
                            'weights by kernel decision; a general conditional Int-count theorem '
                            'forcing zero transferred flux from all twenty periodic balance equations; '
                            'four-port deficiency equality, ring parameter identity and conditional '
                            'SF upper arithmetic and the conditional endpoint-padding order threshold. '
                            'The graph deficiency count, all-k aggregation, '
                            'ring construction, exact-beta proof, minimality and connectivity are written proofs.')
    if arguments.audit == 'triple-ports':
        receipt['scope'] = ('Eight conditional count declarations: six-port deficiency, the hard '
                            'one-omitted-pair case from binary high/leaf/Y counts and necessary '
                            'dissociation inequalities, two-pair deficiency equality, all-pairs '
                            'cap, additive omission accounting, two-obstruction module cap and '
                            'ring parameter/SF arithmetic. The fixed graph-to-count implications, '
                            'restoration/symmetry arguments and full all-r graph theorem retain '
                            'written proofs; no whole-graph formalization or finite-subset proof premise.')
    if arguments.audit == 'multi-ports':
        receipt['scope'] = ('Six fixed graph certificates for the explicit34vertex second-cut '
                            'obstruction: dissociation, cardinality, simple subcubic adjacency, '
                            'bipartition, preattachment isolated ports and remaining saturated ports. '
                            'Three conditional count declarations check the two-cut deficiency '
                            'equality, arbitrary-interface exact parameters and architecture density. '
                            'The all-disjoint-cut Fano cap, general block interfaces, minimality, '
                            'connectedness and the architecture cut count retain written proofs.')
    if arguments.audit == 'long-core':
        receipt['scope'] = ('General graph-level dissociation theorem for any successor-indexed '
                            'word in the two local patterns with no adjacent A: every selected edge '
                            'is internal to a block, and local dissociation gives global '
                            'dissociation. Local pattern counts and boundary implication are '
                            'kernel checked. Four conditional count implications check core/full '
                            'word cardinalities, compulsory slack, cubic gap and exclusion of '
                            'the proposed density. Cyclic word cardinal summation, full Heawood '
                            'attachment and all-k upper-bound conjecture are not formalized here.')
    if arguments.audit == 'long-core-upper':
        receipt['scope'] = ('Ten conditional count declarations: two-index cell cap, '
                            'one-hub and two-hub tight-cell classification, exclusion of a '
                            'selected cut after two tight one-hub cells, sharp one-hub and '
                            'two-hub block counts, singleton-normalization score, cyclic '
                            'aggregate bound, exact-beta and SF interval arithmetic. '
                            'Necessary cell/star inequalities are explicit hypotheses. '
                            'Graph-to-count extraction, odd-hub reflection, full exceptional '
                            'pattern identification, cyclic summation and Heawood attachment '
                            'are written proofs, not claimed as fully formalized.')
    arguments.output.write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps(dict(status=receipt['status'], audited_declarations=len(declarations))))


if __name__ == '__main__':
    main()
