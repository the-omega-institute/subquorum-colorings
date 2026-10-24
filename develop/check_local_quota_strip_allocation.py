"""Independent exhaustive cut controls and physical local-quota regressions."""

import argparse
from collections import Counter
import itertools
import json
from pathlib import Path

from check_component_receivers import verify_terminal
from check_low_charge_rank_barrier import array_records
from check_owned_corner_extensions import separated
from check_remote_deficit_obstruction import fixture as remote_fixture
from check_residual_corridors import transformed
from check_sealed_strip_allocation import ring_case
from check_strip_incidence_allocation import fixture
from check_three_rule_obstruction import fixture as old_fixture
from check_two_leg_corner_obstruction import inspect, saturated_endpoint_donors, two_leg_case
from component_strip_certificates import mixed_component_allocation
from local_quota_strip_allocation import local_quota_allocation
from sealed_strip_allocation import maximal_strips


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def verify(records, residual, all_cuts=False):
    report = local_quota_allocation(records, residual)
    degrees = {vertex: sum(residual[tile] for tile in record['tiles'])
               for vertex, record in enumerate(records)}
    quotas = {vertex: max(1, degree//2) if degree else 0
              for vertex, degree in degrees.items()}
    used = set()
    counts = Counter()
    for entry in report['assignment']:
        tile, unit = tuple(entry['tile']), entry['unit']
        vertex = entry['strip']
        assert tile in records[vertex]['tiles'] and 0 <= unit < residual[tile]
        assert (tile, unit) not in used
        used.add((tile, unit))
        counts[vertex] += 1
    assert all(counts[vertex] <= quotas[vertex] for vertex in quotas)
    previous = mixed_component_allocation(records, residual)
    assert previous['credits'] <= report['credits'] <= sum(residual.values())
    if all_cuts:
        cut_maximum = 0
        for mask in range(1 << len(records)):
            subset = {vertex for vertex in range(len(records)) if mask >> vertex & 1}
            incident = Counter(tile for vertex in subset for tile in records[vertex]['tiles'])
            internal = sum(residual[tile] for tile, amount in incident.items() if amount == 2)
            boundary = sum(residual[tile] for tile, amount in incident.items() if amount == 1)
            deficiency = internal-sum(quotas[vertex] for vertex in subset)
            odd_nonleaves = sum(degrees[vertex] >= 3 and degrees[vertex] % 2
                                for vertex in subset)
            leaves = sum(degrees[vertex] == 1 for vertex in subset)
            assert 2*deficiency == odd_nonleaves-leaves-boundary
            cut_maximum = max(cut_maximum, deficiency)
        assert report['unused'] == cut_maximum
    return report, previous


def abstract_controls():
    tiles, records = array_records(2, 3)
    counts = Counter()
    for capacities in itertools.product(range(3), repeat=len(tiles)):
        residual = dict(zip(tiles, capacities))
        report, previous = verify(records, residual, all_cuts=True)
        counts['patterns'] += 1
        counts['cut_subsets'] += 1 << len(records)
        counts['strict_improvements'] += report['credits'] > previous['credits']
        if sum(capacities) >= 5 and previous['credits'] < 5:
            counts['old_first_five_patterns'] += 1
            counts['first_five_repaired'] += report['credits'] >= 5
            if report['credits'] < 5:
                assert report['credits'] == 4 and report['capacity'] in (5, 6)
                active = [degree for _, degree in report['degrees']]
                assert sorted(active) == ([2, 2, 3, 3] if report['capacity'] == 5
                                          else [3, 3, 3, 3])
                counts['remaining_first_five'] += 1
                counts['remaining_capacity_'+str(report['capacity'])] += 1
    assert counts['patterns'] == 729 and counts['cut_subsets'] == 23328
    assert counts['old_first_five_patterns'] == 60
    assert counts['first_five_repaired'] == counts['remaining_first_five'] == 30
    assert counts['remaining_capacity_5'] == 24 and counts['remaining_capacity_6'] == 6
    return dict(counts)


def physical_controls():
    frozen, certificate = two_leg_case(6, 4, 6)
    inspect(frozen, certificate)
    sources = [fixture()[0], remote_fixture()[0], old_fixture()[0], frozen,
               ring_case(3), ring_case(6)]
    counts = Counter()
    for source in sources:
        for symmetry in itertools.product((False, True), repeat=3):
            shape, selected, matching = transformed(*source, *symmetry)
            physical = *shape, selected, matching
            verify_terminal(physical)
            for use_donors in (False, True):
                reserved = {tuple(donor['tile']): donor['deficit']
                            for donor in saturated_endpoint_donors(physical)} if use_donors else {}
                records, _, residual = maximal_strips(physical, reserved)
                verify(records, residual)
                counts['fixture_symmetry_reservations'] += 1
    for amount in (2, 3, 4):
        physical = separated(sources[:amount])
        assert len(verify_terminal(physical)['receivers']) == amount
        records, _, residual = maximal_strips(physical)
        verify(records, residual)
        counts['separated_components'] += 1
    records, _, before = maximal_strips(frozen)
    _, _, after = maximal_strips(frozen, {(1, 2): 1})
    initial, _ = verify(records, before)
    reduced, _ = verify(records, after)
    assert initial['credits'] == 10 and reduced['credits'] == 9
    counts['frozen_right_donor_now_safe'] += 1
    all_blank = 4, 4, set(), []
    records, _, before = maximal_strips(all_blank)
    _, _, after = maximal_strips(all_blank, {(0, 0): 1})
    initial, _ = verify(records, before, all_cuts=True)
    reduced, _ = verify(records, after, all_cuts=True)
    assert initial['credits'] == 8 and reduced['credits'] == 6
    counterexample = dict(shape=[4, 4], selected=[], matching=[],
                          reserved_tile=[0, 0], reserved_units=1,
                          before=initial, after=reduced, combined_after=7,
                          scope='Resource-only counterexample to reservation monotonicity '
                                'for local-quota score. Zero receiver charge, no owned donor.')
    return dict(counts=counts, repaired_frozen_donor=dict(before=10, reserved=1, after=9),
                reservation_monotonicity_counterexample=counterexample)


def frozen_batch_controls():
    cases = []
    base = None
    symmetry_batches = 0
    for width in list(range(8, 34, 2))+[64]:
        current, certificate = two_leg_case(width, 6, 6)
        ledger = inspect(current, certificate)
        assert ledger['endpoints'] == 2*width+10
        assert ledger['no_endpoint_deficit'] == 3*width-10
        capacity = 3*width-10
        for symmetry in itertools.product((False, True), repeat=3):
            shape, selected, matching = transformed(*current, *symmetry)
            physical = *shape, selected, matching
            inspect(physical)
            donors = saturated_endpoint_donors(physical)
            assert len(donors) == 2
            summaries = []
            for mask in range(4):
                reserved = {tuple(donor['tile']): 1 for index, donor in enumerate(donors)
                            if mask >> index & 1}
                records, _, residual = maximal_strips(physical, reserved)
                allocated, previous = verify(records, residual)
                amount = len(reserved)
                expected = capacity if amount == 0 else capacity-amount-1
                assert allocated['credits'] == previous['credits'] == expected
                assert allocated['unused'] == (0 if amount == 0 else 1)
                assert all(degree >= 2 for _, degree in allocated['degrees'])
                summaries.append(dict(reserved_tiles=sorted(reserved), reserved=amount,
                                      local_quota=allocated, previous_mixed=previous['credits'],
                                      combined=amount+allocated['credits']))
                symmetry_batches += 1
            assert all(record['combined'] == capacity-1 for record in summaries[1:])
            if width == 8 and symmetry == (False, False, False):
                base = dict(shape=current[:2], selected=sorted(current[2]), matching=current[3],
                            ordered_freezing_certificate=certificate, original_ledger=ledger,
                            donors=donors, reservations=summaries)
        cases.append(dict(width=width, endpoints=ledger['endpoints'], original_capacity=capacity,
                          before=capacity, any_nonempty_donor_batch=capacity-1))
    assert base is not None
    return dict(parameter_cases=len(cases), symmetry_batch_cases=symmetry_batches,
                cases=cases, base=base,
                conclusion='For every even width at least8, the height-six two-leg family '
                           'is fully frozen and has exactly two donors from the four rules. '
                           'Every nonempty subset lowers both mixed and local-quota budgets '
                           'by one, including the complete batch. Neither single-donor order '
                           'starts safely. Corrected charge is1 and the grid target survives. '
                           'The all-width result has a separate written proof.')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    report = dict(status='PASS', abstract=abstract_controls(), physical=physical_controls(),
                  frozen_batches=frozen_batch_controls(),
                  scope='General capacitated incidence matching is proved by an attaining '
                        'internal-edge cut. All729abstract patterns and23328cut subsets '
                        'verify the odd-nonleaf/leaf/boundary formula, non-reuse and exact '
                        'maximum.30of60first-q5resource patterns are repaired; remaining '
                        'shapes have no leaves. Actual frozen right-donor loss is repaired. '
                        'An all-even-width actual frozen two-donor family refutes existence '
                        'of a safe nonempty subset, including reserving all donors at once. '
                        'The additional4x4blank example has no donor and charge zero. Universal initial '
                        'geometric coverage and the grid target remain open.')
    arguments.output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(dict(status=report['status'], abstract=report['abstract'],
                         physical=report['physical']['counts'])))


if __name__ == '__main__':
    main()
