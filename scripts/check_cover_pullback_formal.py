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
    parser.add_argument('--audit', choices=('cover', 'dissociation', 'heawood', 'cubic-paths', 'padding-rings', 'triple-ports', 'multi-ports', 'long-core', 'long-core-upper', 'private-clauses', 'bare-ports', 'boundary-loss', 'port-ownership', 'port-return', 'block-ledger', 'closed-high-cycle'), default='cover')
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
                    'long-core-upper': 'build/long-core-upper-formal',
                    'private-clauses': 'build/private-clauses-formal',
                    'bare-ports': 'build/bare-ports-formal',
                    'boundary-loss': 'build/boundary-loss-formal',
                    'port-ownership': 'build/port-clause-ownership-formal',
                    'port-return': 'build/port-return-formal',
                    'block-ledger': 'build/heawood-block-ledger-formal',
                    'closed-high-cycle': 'build/closed-high-cycle-formal'}[arguments.audit]
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
    elif arguments.audit == 'long-core-upper':
        modules += ('StarForming/DissociationCover.lean', 'StarForming/LongCoreWord.lean',
                    'StarForming/LongCoreUpper.lean', 'StarFormingLongCoreUpperAudit.lean')
    elif arguments.audit == 'bare-ports':
        modules += ('StarForming/BareHeawoodPorts.lean', 'StarFormingBareHeawoodPortsAudit.lean')
    elif arguments.audit == 'boundary-loss':
        modules += ('StarForming/PrivateClauses.lean', 'StarForming/BoundaryLoss.lean',
                    'StarFormingBoundaryLossAudit.lean')
    elif arguments.audit == 'port-ownership':
        modules += ('StarForming/PrivateClauses.lean', 'StarForming/PortClauseOwnership.lean',
                    'StarFormingPortClauseOwnershipAudit.lean')
    elif arguments.audit == 'port-return':
        modules += ('StarForming/PortReturn.lean', 'StarFormingPortReturnAudit.lean')
    elif arguments.audit == 'block-ledger':
        modules += ('StarForming/HeawoodBlockLedger.lean', 'StarFormingHeawoodBlockLedgerAudit.lean')
    elif arguments.audit == 'closed-high-cycle':
        modules += ('StarForming/DissociationCover.lean', 'StarForming/LongCoreWord.lean',
                    'StarForming/LongCoreUpper.lean', 'StarForming/ClosedHighCycle.lean',
                    'StarFormingClosedHighCycleAudit.lean')
    else:
        modules += ('StarForming/PrivateClauses.lean', 'StarFormingPrivateClausesAudit.lean')
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
                'long-core-upper': 10, 'private-clauses': 5, 'bare-ports': 4, 'boundary-loss': 2,
                'port-ownership': 2, 'port-return': 5, 'block-ledger': 4, 'closed-high-cycle': 6}
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
    if arguments.audit == 'private-clauses':
        receipt['scope'] = ('Five general graph-level theorems, without finiteness or '
                            'degree assumptions: star formation is equivalent to hitting '
                            'closed-neighborhood and oriented-edge clauses; inclusion-minimal '
                            'formation is equivalent to each selected vertex owning a private '
                            'clause; one clause cannot have two selected private owners; '
                            'clause support is monotone under edge addition; and every '
                            'selected non-port in an attached core has an internal private '
                            'clause or is the sole selected core neighbor of a selected port. '
                            'The finite binary optimization model and bounded-size clause '
                            'count follow by the written cardinal/count argument.')
    if arguments.audit == 'bare-ports':
        receipt['scope'] = ('Two general graph-level statements: if deleting a selected vertex '
                            'covers the newly omitted vertex and every old omitted vertex except '
                            'one port, minimality forces that port to be omitted and its only '
                            'selected neighbor to be its retained external support; therefore '
                            'all internal neighbors are omitted. Two conditional list/count '
                            'theorems sum additive per-port losses without reusing a block '
                            'deficit and yield the periodic-phase upper bound. The Fano '
                            'local loss proof, periodic certificate table and graph-to-count '
                            'instantiation retain written proofs; the full Heawood inequality '
                            'and all-k SF conjecture are not formalized or settled here.')
    if arguments.audit == 'boundary-loss':
        receipt['scope'] = ('Two general graph-level theorems. Every selected core non-port '
                            'without a private internal star clause in an ambient minimal '
                            'forming set exports through a selected core port with that '
                            'candidate as its sole selected internal neighbor; across a new '
                            'edge the other endpoint is omitted and has that port as its '
                            'only selected ambient neighbor. Distinct candidates cannot use '
                            'the same such endpoint. No finite, degree or core-formation '
                            'hypothesis. Finite cardinal injection, Heawood block accounting '
                            'and any long-core partial private-owner cap are written '
                            'deductions or separate open questions, not proved here.')
    if arguments.audit == 'port-ownership':
        receipt['scope'] = ('Two general graph-level statements. Every external neighbor of a '
                            'port belongs to any closed port clause or oriented clause on an '
                            'edge from that port to an internal vertex. If such a clause is '
                            'private, all selected external neighbors of the port equal its '
                            'owner, preventing different outside owners from sharing that '
                            'port. Fano geometry, the eight-selection directional classification, '
                            'the two-owner six-vertex cap and joint loss accounting retain '
                            'written proofs and are not claimed fully formalized.')
    if arguments.audit == 'port-return':
        receipt['scope'] = ('Four general graph-level statements: exact three-case characterization '
                            'of failure after a selected deletion; localization of a high protected '
                            'port failure to a core across its unique exit, directly or through a '
                            'selected leaf; uniqueness of a failed witness for different high '
                            'ports; exclusion of an edge from a failed witness to any other '
                            'selected high vertex. No finiteness or degree bound is imposed. '
                            'One conditional arithmetic statement combines the refined cubic '
                            'capacity premise with isolate compensation. Fano instantiation, '
                            'the direct-return capacity margin and infinite all-saturated '
                            'long-core obstruction retain written proofs.')
    if arguments.audit == 'block-ledger':
        receipt['scope'] = ('Four conditional counting statements: the per-block capacity/flux '
                            'identity implies two units of credit; those credits sum over any '
                            'finite list; global no-reuse implies the cubic block cap; the '
                            '62k-order application gives size<=36k. Fano geometry, restoration '
                            'to a closed Heawood block, graph-to-ledger extraction, unique '
                            'core-isolate ownership and attainment have complete written '
                            'proofs, not a claimed full formalization of SF(L_k)=36k.')
    if arguments.audit == 'closed-high-cycle':
        receipt['scope'] = ('Six conditional count declarations, including the existing one-hub '
                            'lemma: zero-hub bound, closed-high-seam exclusion of the two-hub '
                            'exception, disjoint three-block module cap, arbitrary finite-list '
                            'sum and exact beta/SF/gap arithmetic. Binary cell and star '
                            'inequalities are explicit premises. Normalization, graph-to-count '
                            'extraction, odd-hub reflection, Heawood saturation, arbitrary-r '
                            'construction, attainment and connectivity retain written proofs; '
                            'the full graph theorem is not claimed Lean-formalized.')
    arguments.output.write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps(dict(status=receipt['status'], audited_declarations=len(declarations))))


if __name__ == '__main__':
    main()
