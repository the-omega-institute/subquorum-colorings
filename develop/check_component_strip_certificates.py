"""Independent Hall and non-reuse controls for mixing strip certificates."""

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
from check_two_leg_corner_obstruction import (
    inspect as inspect_two_leg, saturated_endpoint_donors, two_leg_case,
)
from component_strip_certificates import mixed_component_allocation
from owned_corner_witnesses import physical_donors
from sealed_strip_allocation import maximal_strips
from strip_incidence_allocation import maximum_run_allocation


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def verify(records, residual, exhaustive_hall=True):
    result = mixed_component_allocation(records, residual)
    independent_rank = maximum_run_allocation(records, residual)['rank']
    degrees = [sum(residual[tile] for tile in record['tiles']) for record in records]
    weighted = sum(degree//2 for degree in degrees)
    assert result['rank'] == independent_rank and result['weighted'] == weighted
    assert max(independent_rank, weighted) <= result['credits'] <= sum(residual.values())
    used = set()
    counts = Counter()
    requests = set()
    for record in result['assignment']:
        vertex, tile, unit = record['strip'], tuple(record['tile']), record['unit']
        assert tile in records[vertex]['tiles'] and 0 <= unit < residual[tile]
        assert (tile, unit) not in used
        used.add((tile, unit))
        assert (vertex, record['request']) not in requests
        requests.add((vertex, record['request']))
        counts[vertex] += 1
    for component in result['components']:
        vertices = component['vertices']
        if component['rule'] == 'half_capacity':
            assert all(counts[vertex] == degrees[vertex]//2 for vertex in vertices)
        else:
            assert all(counts[vertex] <= 1 for vertex in vertices)
        for mask in range((1 << len(vertices)) if exhaustive_hall else 0):
            chosen = {vertex for index, vertex in enumerate(vertices) if mask >> index & 1}
            tiles = {tile for vertex in chosen for tile in records[vertex]['tiles']}
            assert sum(counts[vertex] for vertex in chosen) <= sum(residual[tile] for tile in tiles)
    capacity = sum(residual.values())
    for charge in range(1, min(4, capacity)+1):
        assert charge <= result['credits']
    first = capacity >= 5 and result['credits'] < 5
    if first:
        assert len(result['components']) == 1
        component = result['components'][0]
        assert len(component['vertices']) == component['rank'] == component['credits'] == 4
        assert capacity in (5, 6)
        if capacity == 6:
            assert component['odd_runs'] == 4
            assert all(degrees[vertex] == 3 for vertex in component['vertices'])
            assert sorted(value for value in residual.values() if value) == [1, 1, 2, 2]
    return result, first


def independent_selected_case(rows, columns, capacities):
    chosen = set()
    for (row, column), capacity in capacities.items():
        candidates = [(2*row, 2*column), (2*row+1, 2*column+1)]
        chosen.update(candidates[:2-capacity])
    return 2*rows, 2*columns, chosen, []


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    tiles, records = array_records(2, 3)
    patterns = first_five = strict_mixtures = 0
    first_capacity_counts = Counter()
    for capacities in itertools.product(range(3), repeat=len(tiles)):
        residual = dict(zip(tiles, capacities))
        result, first = verify(records, residual)
        patterns += 1
        first_five += first
        strict_mixtures += result['credits'] > max(result['rank'], result['weighted'])
        if first:
            first_capacity_counts[sum(capacities)] += 1
    assert first_capacity_counts == {5: 54, 6: 6}
    capacities = {tile: 0 for tile in tiles}
    capacities.update({(0, 0): 2, (0, 1): 2, (1, 2): 1})
    current = independent_selected_case(2, 3, capacities)
    assert verify_terminal(current)['objective'] == 7
    runs, deficits, residual = maximal_strips(current)
    mixed, _ = verify(runs, residual)
    assert mixed['rank'] == mixed['weighted'] == 4 and mixed['credits'] == 5
    reservation_case = 2, 6, set(), []
    runs, _, before = maximal_strips(reservation_case)
    initial, _ = verify(runs, before)
    runs, _, after = maximal_strips(reservation_case, {(0, 0): 1})
    reduced, _ = verify(runs, after)
    assert initial['credits'] == 6 and reduced['credits'] == 4
    frozen, certificate = two_leg_case(6, 4, 6)
    inspect_two_leg(frozen, certificate)
    donor = next(record for record in saturated_endpoint_donors(frozen)
                 if tuple(record['tile']) == (1, 2))
    runs, _, residual = maximal_strips(frozen)
    initial_frozen, _ = verify(runs, residual)
    runs, _, residual = maximal_strips(frozen, {(1, 2): 1})
    reduced_frozen, _ = verify(runs, residual)
    assert initial_frozen['credits'] == 10 and reduced_frozen['credits'] == 8
    frozen_ledger = verify_terminal(frozen)
    assert frozen_ledger['empty_deficit'] == 11
    sources = [fixture()[0], remote_fixture()[0], old_fixture()[0], frozen,
               ring_case(3), ring_case(6)]
    physical_cases = 0
    for source in sources:
        for symmetry in itertools.product((False, True), repeat=3):
            shape, chosen, matching = transformed(*source, *symmetry)
            physical = *shape, chosen, matching
            verify_terminal(physical)
            for use_donors in (False, True):
                reserved = {}
                if use_donors:
                    reserved = {tuple(record['tile']): record['deficit'] for record in
                        physical_donors(physical, include_endpoint_guard=True)
                        + saturated_endpoint_donors(physical)}
                runs, _, residual = maximal_strips(physical, reserved)
                verify(runs, residual, exhaustive_hall=False)
                physical_cases += 1
    mixed_cases = 0
    for amount in (2, 3, 4):
        physical = separated(sources[:amount])
        ledger = verify_terminal(physical)
        assert len(ledger['receivers']) == amount
        for use_donors in (False, True):
            reserved = {}
            if use_donors:
                reserved = {tuple(record['tile']): record['deficit'] for record in
                    physical_donors(physical, include_endpoint_guard=True)
                    + saturated_endpoint_donors(physical)}
            runs, _, residual = maximal_strips(physical, reserved)
            verify(runs, residual, exhaustive_hall=False)
            mixed_cases += 1
    report = dict(status='PASS', capacity_patterns=patterns,
                  first_residual_charge_five_patterns=first_five,
                  first_pattern_capacity_counts=dict(first_capacity_counts),
                  strict_component_mixtures=strict_mixtures,
                  physical_cases=physical_cases, separated_mixed_cases=mixed_cases,
                  physical_mixture=dict(shape=current[:2], rank=4, weighted=4, mixed=5,
                                        selected=sorted(current[2]), receiver_charge=0),
                  reservation_monotonicity_counterexample=dict(shape=[2, 6], all_blank=True,
                      original_credits=6, reserved_tile=[0, 0], reserved_units=1,
                      residual_credits=4, combined_after=5, original_capacity=6,
                      conclusion='B+mixed is NOT reservation-monotone; recompute from residual slots.'),
                  frozen_owned_donor_counterexample=dict(shape=frozen[:2], selected=sorted(frozen[2]),
                      matching=frozen[3], ordered_freezing_certificate=certificate,
                      donor=donor, original_ledger=frozen_ledger,
                      before={key: value for key, value in initial_frozen.items() if key != 'assignment'},
                      after={key: value for key, value in reduced_frozen.items() if key != 'assignment'},
                      reserved_units=1, combined_after=9,
                      conclusion='A valid saturated endpoint donor in a fully frozen receiver '
                                 'reduces B+mixed from10to9. This refutes reservation '
                                 'monotonicity for this score; charge1is paid both before '
                                 'and after, so neither allocation validity nor the target is refuted.'),
                  scope='Every assigned unit is checked physically and against every '
                        'Hall subset within each component for729abstract capacity patterns. '
                        'The low-charge threshold and exact first-failure resource shapes '
                        'are finite controls of written general proofs. Both concrete '
                        'blank/independent physical controls have no endpoints and charge zero; they '
                        'demonstrate a stricter resource certificate and a failed '
                        'monotonicity rule. The separate frozen donor example supplies a '
                        'genuine owned-corner reservation counterexample to monotonicity, '
                        'with the original target intact.96physical and6separated cases '
                        'check distinct assignments and correct branch demands without '
                        'enumerating their potentially large Hall-subset families.')
    arguments.output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report))


if __name__ == '__main__':
    main()
