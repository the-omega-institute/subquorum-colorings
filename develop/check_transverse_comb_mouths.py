"""Physical and exact strip-optimization controls for transverse comb payment."""

import argparse
import itertools
import json
from pathlib import Path

from check_bent_cap_compensation import charge_twice
from check_component_receivers import endpoint_components, verify_terminal, vertices_of
from check_long_bent_terminal_strips import terminal_strip
from check_owned_donors import endpoint_data
from check_promotion_cores import frozen_certificate
from check_residual_corridors import direct_check, graph_record, transformed
from check_saturated_bent_bands import long_bent


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def adjacent(vertex):
    row, column = vertex
    return {(row+vertical, column+horizontal)
            for vertical, horizontal in ((1, 0), (-1, 0), (0, 1), (0, -1))}


def crossing_family(width, depth, centers, phases, upper=1, lower=2):
    baseline, _ = long_bent(width, depth, saturate=False)
    tip = 2*depth+2
    selected, matching = set(baseline[2]), list(baseline[3])
    move = lambda vertex: (vertex[0]+2, vertex[1]+3)
    for center, phase in zip(centers, phases):
        points = [(row, center) for row in range(tip-upper, tip+lower+1)]
        assert len(points) % 2 == 0
        matching.extend((move(first), move(second)) for first, second in zip(points[::2], points[1::2]))
        supports = {(tip-upper-1, center), (tip+lower+1, center)}
        supports.update((row, center+phase*(1 if (row-tip) % 2 else -1))
                        for row in range(tip-upper, tip+lower+1))
        selected.update(move(point) for point in supports)
    required_rows = max(row for row, column in selected)+1
    rows = max(baseline[0], required_rows+required_rows % 2)
    current = rows, baseline[1], selected, matching
    direct_check(*current)
    return current, terminal_strip(width, depth)


def optimize_strip(current, strip):
    selected, endpoints = current[2], endpoint_data(current)[0]
    occupied = selected | endpoints
    rows = sorted({row for row, column in strip})
    columns = sorted({column for row, column in strip})
    forbidden = set().union(*(adjacent(point) for point in selected-strip))
    forced_masks, endpoint_masks, choices = [], [], []
    for column in columns:
        fixed = sum(1 << index for index, row in enumerate(rows) if (row, column) in selected)
        paired = sum(1 << index for index, row in enumerate(rows) if (row, column) in endpoints)
        banned = sum(1 << index for index, row in enumerate(rows) if (row, column) in forbidden)
        forced_masks.append(fixed)
        endpoint_masks.append(paired)
        choices.append([mask for mask in range(4) if mask & fixed == fixed and not mask & (paired | banned)])

    def feasible_column(index, previous, present, following):
        for row_index, row in enumerate(rows):
            if not present >> row_index & 1:
                continue
            vertical = (present | endpoint_masks[index]) >> (1-row_index) & 1
            before = ((previous | endpoint_masks[index-1]) >> row_index & 1
                      if index else int((row, columns[0]-1) in occupied))
            after = ((following | endpoint_masks[index+1]) >> row_index & 1
                     if index+1 < len(columns) else int((row, columns[-1]+1) in occupied))
            outside = int((row+(-1 if row_index == 0 else 1), columns[index]) in occupied)
            if vertical+before+after+outside > 1:
                return False
        return True

    states = {(0, 0): (0, [])}
    for index, options in enumerate(choices):
        following_states = {}
        for (previous, present), (value, path) in states.items():
            for following in options:
                if index and not feasible_column(index-1, previous, present, following):
                    continue
                key, candidate = (present, following), (value+following.bit_count(), path+[following])
                if key not in following_states or candidate[0] > following_states[key][0]:
                    following_states[key] = candidate
        states = following_states
    value, path = max((value, path) for (previous, present), (value, path) in states.items()
                      if feasible_column(len(columns)-1, previous, present, 0))
    extended = selected | {(row, column) for column, mask in zip(columns, path)
                           for row_index, row in enumerate(rows) if mask >> row_index & 1}
    assert len(extended & strip) == value
    result = (*current[:2], extended, current[3])
    direct_check(*result)
    return result


def inspect(current, strip):
    checked = verify_terminal(current)
    endpoints = endpoint_data(current)[0]
    assert frozen_certificate(current)[0] == endpoints
    tiles = {(row//2, column//2) for row, column in strip}
    paired_tiles = {(row//2, column//2) for row, column in endpoints & strip}
    empty_tiles = tiles-paired_tiles
    for tile in paired_tiles:
        cells = vertices_of({tile})
        assert len(cells & endpoints) == 2 and len(cells & current[2]) == 1
    for upper in range(min(row for row, column in strip), max(row for row, column in strip)):
        for column in range(min(column for row, column in strip), max(column for row, column in strip)):
            square = {(row, current_column) for row in (upper, upper+1)
                      for current_column in (column, column+1)}
            assert 2*len(square & current[2])+len(square & endpoints) <= 4
    deficit = sum(2-len(vertices_of({tile}) & current[2]) for tile in empty_tiles)
    assert deficit >= 2
    assert 2*len(current[2] & strip)+len(endpoints & strip) <= 2*len(tiles)*2-4
    assert sum(receiver['charge_twice'] for receiver in checked['receivers']) == 2
    assert len(endpoint_components(current)) == len(checked['receivers'])
    graph, _ = graph_record(*current)
    corrected_strip_twice = sum(charge_twice(graph, current[1], tile) for tile in tiles)
    return dict(crossing_components=len(checked['receivers'])-1,
                no_endpoint_payment_tiles=len(empty_tiles), payment_deficit=deficit,
                source_charge=1, compensated_charge=1-deficit,
                corrected_full_strip_charge_twice=corrected_strip_twice)


def controls():
    cases, images = [], 0
    for count in range(1, 9):
        patterns = list(itertools.product((-1, 1), repeat=count)) if count <= 4 else [
            tuple(1 for index in range(count)), tuple(-1 for index in range(count)),
            tuple((-1)**index for index in range(count)), tuple(-(-1)**index for index in range(count))]
        width = 4*count+10
        for depth, phases in itertools.product((2, 4, 9), patterns):
            current, strip = crossing_family(width, depth, [5+4*index for index in range(count)], phases)
            sharp = optimize_strip(current, strip)
            record = inspect(sharp, strip)
            cases.append(dict(width=width, depth=depth, phases=phases, **record))
            if depth == 4 and phases == patterns[0] and count in (1, 4, 8):
                for symmetry in itertools.product((False, True), repeat=3):
                    shape, selected, matching = transformed(*sharp, *symmetry)
                    _, moved_strip, _ = transformed(*sharp[:2], strip, [], *symmetry)
                    image = (*shape, selected, matching)
                    assert inspect(image, moved_strip)['payment_deficit'] == record['payment_deficit']
                    images += 1
    for upper, lower in itertools.product((1, 3, 5), (2, 4, 6)):
        current, strip = crossing_family(18, 5, [5, 9], [1, -1], upper, lower)
        record = inspect(optimize_strip(current, strip), strip)
        cases.append(dict(width=18, depth=5, upper=upper, lower=lower, **record))
    baseline, strip = crossing_family(10, 2, [3], [1])
    optimized = optimize_strip(baseline, strip)
    exact_record = inspect(optimized, strip)
    free = sorted(strip-baseline[2]-endpoint_data(baseline)[0])
    feasible, maximum = 0, -1
    for mask in range(1 << len(free)):
        selected = baseline[2] | {point for index, point in enumerate(free) if mask >> index & 1}
        occupied = selected | endpoint_data(baseline)[0]
        if any(len(adjacent(point) & occupied) > 1 for point in selected):
            continue
        feasible += 1
        maximum = max(maximum, len(selected & strip))
    assert maximum == len(optimized[2] & strip) and feasible == 20
    assert exact_record['payment_deficit'] == 2
    assert exact_record['corrected_full_strip_charge_twice'] == -3
    ending_base, _ = long_bent(12, 3, saturate=False)
    above, ending_strip = crossing_family(12, 3, [4], [-1], upper=3, lower=0)
    below, _ = crossing_family(12, 3, [7], [-1], upper=-1, lower=4)
    extra_selected = {(row+2, column+3) for row in (8, 9) for column in (2, 9)}
    ending = (max(above[0], below[0]), ending_base[1],
              above[2] | below[2] | extra_selected,
              above[3]+below[3][len(ending_base[3]):])
    ending_objective = direct_check(*ending)
    ending_endpoints = endpoint_data(ending)[0]
    assert all(len(adjacent(point) & (ending[2] | ending_endpoints)) == 1 for point in ending[2])
    assert frozen_certificate(ending)[0] == ending_endpoints
    ending_checked = verify_terminal(ending)
    assert sorted(record['charge_twice'] for record in ending_checked['receivers']) == [0, 0, 2]
    ending_tiles = {(row//2, column//2) for row, column in ending_strip}
    endpoint_tiles = {(row//2, column//2) for row, column in ending_endpoints & ending_strip}
    ending_deficit = sum(2-len(vertices_of({tile}) & ending[2])
                        for tile in ending_tiles-endpoint_tiles)
    assert ending_deficit == 0
    assert len(ending_tiles-endpoint_tiles) == 3
    ending_graph, _ = graph_record(*ending)
    ending_strip_charge = sum(charge_twice(ending_graph, ending[1], tile) for tile in ending_tiles)
    assert ending_strip_charge == -2
    comb_tiles = {(row//2, column//2) for row, column in
                  ending_endpoints-endpoint_data(ending_base)[0]}
    outside_comb_charge = sum(charge_twice(ending_graph, ending[1], tile)
                              for tile in comb_tiles-ending_tiles)
    assert outside_comb_charge == 2
    assert sorted(charge_twice(ending_graph, ending[1], tile)
                  for tile in endpoint_tiles) == [-1, -1]
    first_source, _ = long_bent(14, 2, saturate=False)
    _, reflected_selected, reflected_matching = transformed(*first_source, False, True, True)
    reflected = lambda vertex: (vertex[0]+12, vertex[1]-2)
    shared_selected = first_source[2] | {reflected(point) for point in reflected_selected}
    shared_matching = first_source[3]+[tuple(reflected(point) for point in edge)
                                       for edge in reflected_matching]
    shared_selected |= {(6, 8), (17, 8)} | {(row, 9 if row % 2 else 7) for row in range(7, 17)}
    shared_matching += [((row, 8), (row+1, 8)) for row in range(7, 17, 2)]
    shared = 32, 22, shared_selected, shared_matching
    first_strip = terminal_strip(14, 2)
    _, reflected_strip, _ = transformed(*first_source[:2], first_strip, [], False, True, True)
    second_strip = {reflected(point) for point in reflected_strip}
    for strip in (first_strip, second_strip):
        shared = optimize_strip(shared, strip)
    shared_checked = verify_terminal(shared)
    shared_endpoints = endpoint_data(shared)[0]
    assert frozen_certificate(shared)[0] == shared_endpoints
    assert sorted(record['charge_twice'] for record in shared_checked['receivers']) == [0, 2, 2]
    assert not first_strip & second_strip
    shared_payments = []
    for strip in (first_strip, second_strip):
        tiles = {(row//2, column//2) for row, column in strip}
        endpoint_tiles = {(row//2, column//2) for row, column in shared_endpoints & strip}
        payment = sum(2-len(vertices_of({tile}) & shared[2]) for tile in tiles-endpoint_tiles)
        assert payment == 2
        shared_payments.append(payment)
    return dict(status='ALL_CHECKS_PASSED', optimized_family_cases=len(cases), symmetry_images=images,
                exhaustive_fixture=dict(feasible_completions=feasible, masks=1 << len(free),
                    shape=optimized[:2], selected=sorted(optimized[2]), matching=optimized[3],
                    **exact_record), family=cases,
                two_ending_comb_obstacle=dict(shape=ending[:2], selected=sorted(ending[2]),
                    matching=ending[3], objective=ending_objective,
                    no_endpoint_payment_deficit=ending_deficit,
                    original_strip_charge_twice=ending_strip_charge,
                    whole_comb_receiver_charge_twice=0,
                    outside_strip_comb_charge_twice=outside_comb_charge,
                    global_coefficient_one_refuted=False),
                shared_crossing_receiver_fixture=dict(sources=2, crossing_components=1,
                    distinct_strip_payments=shared_payments, whole_crossing_receiver_charge=0,
                    compensated_charge=-2, objective=shared_checked['objective']),
                scope='Controls for independent all-length weighted shifted-square and disjoint no-P payment proofs. '
                      'Dynamic programming optimizes all additional selected sites in each fixed physical mouth. '
                      'No general endpoint-contact or universal grid theorem is inferred from these cases.')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    report = controls()
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({key: value for key, value in report.items()
                      if key not in ('family', 'exhaustive_fixture', 'two_ending_comb_obstacle')}))


if __name__ == '__main__':
    main()
