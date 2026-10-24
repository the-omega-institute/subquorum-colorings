"""Exhaustive Hall controls, physical strip accounting and a frozen coverage obstruction."""

import argparse
from collections import Counter
import itertools
import json
from pathlib import Path

from check_component_receivers import verify_terminal, vertices_of
from check_cooperative_promotion import neighbors, occupied_degrees
from check_owned_corner_extensions import separated
from check_promotion_cores import frozen_certificate
from check_remote_deficit_obstruction import fixture as remote_fixture
from check_residual_corridors import transformed
from check_sealed_strip_allocation import ring_case
from check_three_rule_obstruction import fixture as old_fixture
from check_two_leg_corner_obstruction import saturated_endpoint_donors, two_leg_case
from owned_corner_witnesses import physical_donors
from search_corner_coverage import corner_patterns
from sealed_strip_allocation import maximal_strips
from strip_incidence_allocation import allocate_requested, maximum_run_allocation


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def fixture():
    source = json.loads(Path(__file__).with_name('capacity_one_strip_obstruction.json').read_text())
    current = (*source['shape'], {tuple(point) for point in source['selected']},
               [tuple(tuple(point) for point in edge) for edge in source['matching']])
    certificate = [tuple(tuple(point) for point in row) for row in source['freezing_certificate']]
    return current, certificate


def check_assignment(records, residual, allocation):
    assert allocation['feasible']
    slots = [(tuple(record['tile']), record['unit']) for record in allocation['assignment']]
    assert len(slots) == len(set(slots))
    assert len({record['strip'] for record in allocation['assignment']}) == len(slots)
    for record in allocation['assignment']:
        tile = tuple(record['tile'])
        assert tile in records[record['strip']]['tiles']
        assert 0 <= record['unit'] < residual[tile]


def abstract_controls():
    tiles = list(itertools.product(range(2), range(3)))
    records = [dict(orientation='horizontal', tiles=[tile for tile in tiles if tile[0] == row])
               for row in range(2)]
    records += [dict(orientation='vertical', tiles=[tile for tile in tiles if tile[1] == column])
                for column in range(3)]
    configurations = requests_checked = reservation_transitions = 0
    for capacities in itertools.product(range(3), repeat=len(tiles)):
        residual = dict(zip(tiles, capacities))
        slots = [(tile, unit) for tile, capacity in residual.items() for unit in range(capacity)]
        neighbors_by_mask = []
        for mask in range(1 << len(records)):
            chosen = [record for index, record in enumerate(records) if mask >> index & 1]
            neighbors_by_mask.append(sum(any(tile in record['tiles'] for record in chosen)
                                         for tile, _ in slots))
        feasible_masks = []
        for mask in range(1 << len(records)):
            subset = mask
            hall = True
            while subset:
                if subset.bit_count() > neighbors_by_mask[subset]:
                    hall = False
                    break
                subset = (subset-1) & mask
            requested = {index for index in range(len(records)) if mask >> index & 1}
            allocation = allocate_requested(records, residual, requested)
            assert allocation['feasible'] == hall
            if hall:
                check_assignment(records, residual, allocation)
                assert {record['strip'] for record in allocation['assignment']} == requested
                feasible_masks.append(mask)
            requests_checked += 1
        maximum = maximum_run_allocation(records, residual)
        assert maximum['rank'] == max(mask.bit_count() for mask in feasible_masks)
        check_assignment(records, residual, maximum)
        for tile, capacity in residual.items():
            if capacity:
                after = dict(residual)
                after[tile] -= 1
                reduced = maximum_run_allocation(records, after)
                assert maximum['rank']-1 <= reduced['rank'] <= maximum['rank']
                reservation_transitions += 1
        configurations += 1
    return dict(capacity_multigraphs=configurations, requested_subsets=requests_checked,
                one_unit_reservation_transitions=reservation_transitions)


def physical_control(current, reserve=False):
    checked = verify_terminal(current)
    reserved = {}
    if reserve:
        for record in physical_donors(current, include_endpoint_guard=True)+saturated_endpoint_donors(current):
            reserved[tuple(record['tile'])] = record['deficit']
    records, deficits, residual = maximal_strips(current, reserved)
    endpoints = {point for edge in current[3] for point in edge}
    receiver = {(row//2, column//2) for row, column in endpoints}
    independent_runs = set()
    for horizontal in (True, False):
        bands, length = (current[0]//2, current[1]//2) if horizontal else (current[1]//2, current[0]//2)
        for band in range(bands):
            tile = lambda index: (band, index) if horizontal else (index, band)
            for start in range(length):
                for stop in range(start+1, length+1):
                    run = tuple(tile(index) for index in range(start, stop))
                    if set(run) & receiver:
                        continue
                    if start and tile(start-1) not in receiver:
                        continue
                    if stop < length and tile(stop) not in receiver:
                        continue
                    independent_runs.add(('horizontal' if horizontal else 'vertical', run))
    assert independent_runs == {(record['orientation'], tuple(record['tiles'])) for record in records}
    for record in records:
        assert record['capacity'] == 2*len(record['tiles'])-len(vertices_of(record['tiles']) & current[2])
    allocation = maximum_run_allocation(records, residual)
    check_assignment(records, residual, allocation)
    initial = maximum_run_allocation(records, deficits)
    assert initial['rank'] <= sum(reserved.values())+allocation['rank'] <= checked['empty_deficit']
    old_requested = {index for index, record in enumerate(records) if record['residual_capacity'] >= 2}
    assert allocate_requested(records, residual, old_requested)['feasible']
    assert len(old_requested) <= allocation['rank']
    return dict(components=len(checked['receivers']), runs=len(records),
                certified_high_capacity_runs=len(old_requested), reserved=sum(reserved.values()),
                rank=allocation['rank'], total_capacity=checked['empty_deficit'],
                incidence_tree_components=sum(record['tree'] for record in allocation['components']))


def obstruction():
    current, certificate = fixture()
    endpoints = {point for edge in current[3] for point in edge}
    mates = {point: partner for edge in current[3] for point, partner in (edge, edge[::-1])}
    earlier = set()
    for vertex, first, second in certificate:
        assert vertex in endpoints-earlier and first != second
        assert {first, second} <= set(neighbors(vertex))
        assert mates[vertex] not in {first, second}
        assert all(point in current[2] or point in mates and mates[point] in earlier
                   for point in (first, second))
        earlier.add(vertex)
    assert earlier == endpoints and len(certificate) == 32
    assert frozen_certificate(current)[0] == endpoints
    ledger = verify_terminal(current)
    assert (len(endpoints), len(current[2]), len(current[3])) == (32, 22, 16)
    assert len(ledger['receivers']) == 1
    receiver = ledger['receivers'][0]
    assert (receiver['tiles'], receiver['selected'], receiver['charge_twice']) == (14, 13, 2)
    assert not physical_donors(current, include_endpoint_guard=True)
    assert not saturated_endpoint_donors(current)
    records, deficits, residual = maximal_strips(current)
    assert sorted(record['capacity'] for record in records) == [0, 1, 1, 1, 1, 1, 1]
    assert sum(deficits.values()) == 3 and max(deficits.values()) == 1
    assert all(not record['sealed'] for record in records)
    allocation = maximum_run_allocation(records, residual)
    assert allocation['rank'] == 3
    assert all(component['tree'] and len(component['vertices']) == 2 and len(component['slots']) == 1
               for component in allocation['components'])
    candidates = []
    for top, left in itertools.product(range(0, current[0], 2), range(0, current[1], 2)):
        for orientation, (required, support, excluded) in enumerate(corner_patterns(top, left)):
            if set(required[:4]) <= endpoints:
                assert required[4] not in endpoints or support not in current[2] or set(excluded) & endpoints
                candidates.append(dict(tile=(top//2, left//2), orientation=orientation,
                                       tip=required[4], support=support,
                                       tip_is_endpoint=required[4] in endpoints,
                                       support_is_selected=support in current[2],
                                       excluded_endpoints=sorted(set(excluded) & endpoints)))
    corners = []
    for tile in deficits:
        cells = vertices_of({tile})
        for chosen in sorted(cells & current[2]):
            anchors = (set(neighbors(chosen))-cells) & endpoints
            if anchors:
                opposite = tuple(4*coordinate+1-value for coordinate, value in zip(tile, chosen))
                corners.append(dict(selected=chosen, opposite=opposite,
                                    exterior_endpoints=sorted((set(neighbors(opposite))-cells) & endpoints),
                                    exterior_selections=sorted((set(neighbors(opposite))-cells) & current[2])))
    return dict(shape=current[:2], endpoints=32, selected=22, matching_edges=16,
                receiver=receiver, objective=ledger['objective'], half_area=40,
                total_capacity=3, capacity_two_run_credits=0, all_four_corner_credits=0,
                exact_incidence_rank=3, positive_tiles=[tile for tile, value in deficits.items() if value],
                degree_histogram=dict(sorted(Counter(occupied_degrees(current).values()).items())),
                runs=records, capped_candidates=candidates, anchored_selected_corners=corners,
                ordered_freezing_steps=32)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    abstract = abstract_controls()
    fixture_cases = [('new32', fixture()[0]), ('remote28', remote_fixture()[0]),
                     ('old22', old_fixture()[0]), ('two_leg', two_leg_case(6, 4, 6)[0]),
                     ('ring3', ring_case(3)), ('ring6', ring_case(6))]
    physical = []
    for name, current in fixture_cases:
        for symmetry in itertools.product((False, True), repeat=3):
            shape, selected, matching = transformed(*current, *symmetry)
            for reserve in (False, True):
                physical.append(dict(name=name, symmetry=symmetry, reserve=reserve,
                                     **physical_control((*shape, selected, matching), reserve)))
    mixed = []
    for amount in (2, 3, 4):
        current = separated([case for _, case in fixture_cases[:amount]])
        for reserve in (False, True):
            record = physical_control(current, reserve)
            assert record['components'] == amount
            mixed.append(dict(reserve=reserve, **record))
    report = dict(status='PASS', abstract_controls=abstract, physical_cases=len(physical),
                  mixed_controls=mixed, obstruction=obstruction(), physical=physical,
                  scope='Exhaustive finite checks of the separately written exact incidence '
                        'allocation theorem and reservation monotonicity; explicit fully frozen '
                        '32-endpoint counterexample to four-corner-plus-capacity-two-run coverage. '
                        'No universal grid conclusion or Lean execution is inferred.')
    arguments.output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({key: value for key, value in report.items()
                      if key not in ('physical', 'obstruction')}, default=list))


if __name__ == '__main__':
    main()
