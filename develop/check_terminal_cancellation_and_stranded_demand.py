"""Check signed terminal cancellation and a frozen continuation obstruction."""

import argparse
from collections import Counter, defaultdict
import itertools
import json
from pathlib import Path

from check_even_bridge_support_completion import endpoints_of
from check_frozen_missing_port_bp_injection import inspect as inspect_injection
from check_interval_connector_cycles_and_missing_ports import stack, whole_bands
from check_native_guard_compensation import force_matching
from check_pp_path_terminal_ledger import inspect as inspect_paths
from check_promotion_cores import frozen_certificate
from check_receiver_overlap_and_pp_source_collision import forest_intervals
from check_residual_corridors import direct_check, transformed
from check_neutral_portal_strip_compensation import image_map


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def components(vertices, edges):
    adjacency = defaultdict(list)
    for index, (first, second) in enumerate(edges):
        adjacency[first].append((second, index))
        adjacency[second].append((first, index))
    assert all(len(adjacency[vertex]) <= 2 for vertex in vertices)
    remaining, result = set(vertices), []
    while remaining:
        start = min(remaining)
        reached, pending, used = {start}, [start], set()
        while pending:
            vertex = pending.pop()
            for other, index in adjacency[vertex]:
                used.add(index)
                if other not in reached:
                    reached.add(other)
                    pending.append(other)
        remaining -= reached
        ends = sorted(vertex for vertex in reached if len(adjacency[vertex]) == 1)
        cycle = len(used) == len(reached)
        assert (cycle and not ends) or (len(used)+1 == len(reached)
                                       and len(ends) == (0 if len(reached) == 1 else 2))
        result.append(dict(vertices=reached, edges=used, ends=ends, cycle=cycle))
    return result


def terminal_data(current, bands):
    original = inspect_paths(current, bands, Counter(), True)
    assert original['cuts'] == 0
    labels, intervals, interval_owner = forest_intervals(current, bands)
    endpoints = endpoints_of(current)
    kinds, locations, pairs = {}, {}, []
    for path in original['components']:
        if path['kind'] == ['cycle']:
            continue
        tips = []
        for band, column in (path['nodes'][0], path['nodes'][-1]):
            point = next(point for point in bands[band][column] if point in endpoints)
            kinds[point] = 'TP' if 'T' in labels[band][column] else 'BP'
            locations[point] = band, column
            tips.append(point)
        pairs.append(tuple(tips))
    ports = {point: [(band, adjacent) for adjacent in (column-1, column+1)
                     if 0 <= adjacent < len(bands[band])
                     and labels[band][adjacent] == ('B', 'B')]
             for point, (band, column) in locations.items()}
    return original, labels, intervals, interval_owner, kinds, pairs, ports


def cancel_pairs(kinds, pairs, links, totals):
    assert set(kinds) == {point for pair in pairs for point in pair}
    assert len(kinds) == 2*len(pairs)
    assert len({point for link in links for point in link}) == 2*len(links)
    assert all(kinds[first] != kinds[second] for first, second in links)
    edges = pairs+links
    reduced, records = [], []
    for component in components(kinds, edges):
        used_pairs = [pairs[index] for index in component['edges'] if index < len(pairs)]
        inventory = Counter(tuple(sorted((kinds[first], kinds[second])))
                            for first, second in used_pairs)
        alpha, beta = inventory['TP', 'TP'], inventory['BP', 'BP']
        if component['cycle']:
            assert alpha == beta
            totals['cancellation_cycles'] += 1
        else:
            assert len(component['ends']) == 2
            first, second = component['ends']
            reduced.append((first, second))
            signed_ends = sum(1 if kinds[point] == 'BP' else -1 for point in (first, second))
            assert 2*(beta-alpha) == signed_ends
        records.append(dict(vertices=sorted(component['vertices']),
                            ends=component['ends'], cycle=component['cycle'],
                            alpha=alpha, beta=beta, gamma=inventory['BP', 'TP']))
    original = Counter(tuple(sorted((kinds[first], kinds[second]))) for first, second in pairs)
    final = Counter(tuple(sorted((kinds[first], kinds[second]))) for first, second in reduced)
    assert original['BP', 'BP']-original['TP', 'TP'] == final['BP', 'BP']-final['TP', 'TP']
    consumed = sum(min(record['alpha'], record['beta']) for record in records)
    assert final['TP', 'TP'] == original['TP', 'TP']-consumed
    assert final['BP', 'BP'] == original['BP', 'BP']-consumed
    assert 0 <= consumed <= min(original['TP', 'TP'], original['BP', 'BP'])
    totals['whole_beta_resources_consumed'] += consumed
    path_owner = {point: index for index, pair in enumerate(pairs) for point in pair}
    alpha_owners = {index for index, pair in enumerate(pairs)
                    if all(kinds[point] == 'TP' for point in pair)}
    beta_owners = {index for index, pair in enumerate(pairs)
                   if all(kinds[point] == 'BP' for point in pair)}
    sources = [first if kinds[first] == 'TP' else second for first, second in links]
    if all(path_owner[point] in alpha_owners for point in sources):
        adjacency = defaultdict(set)
        for first, second in links:
            demand, resource = (path_owner[first], path_owner[second]) if kinds[first] == 'TP' else (
                path_owner[second], path_owner[first])
            if resource in beta_owners:
                adjacency[demand].add(resource)
        assignment = {}

        def augment(demand, visited):
            for resource in adjacency[demand]-visited:
                visited.add(resource)
                if resource not in assignment or augment(assignment[resource], visited):
                    assignment[resource] = demand
                    return True
            return False

        for demand in sorted(alpha_owners):
            augment(demand, set())
        assert len(assignment) == consumed
        assert len(set(assignment.values())) == len(assignment)
        totals['source_alpha_unit_allocation_controls'] += 1
        totals['original_beta_path_resources_assigned'] += len(assignment)
        totals['nonempty_source_alpha_unit_allocations'] += bool(assignment)
    assert len(reduced) == len(pairs)-len(links)
    totals['terminal_models'] += 1
    totals['original_path_objects'] += len(pairs)
    totals['cancellation_links'] += len(links)
    return reduced, final, records


def virtual_connectors(original, labels, intervals, owner, kinds, reduced, ports, totals):
    edges, omitted = [], 0
    for first, second in reduced:
        if kinds[first] != 'TP' or kinds[second] != 'TP':
            continue
        if not ports[first] or not ports[second]:
            omitted += 1
            continue
        edges.append((owner[ports[first][0]], owner[ports[second][0]]))
    boundary = {owner[band, 0] for band in range(len(labels))}
    if len(labels[0]) % 2 == 0:
        boundary |= {owner[band, len(row)-1] for band, row in enumerate(labels)
                     if row[-1] == ('B', 'B')}
    assert len(boundary) == original['boundary_budget']
    degrees = Counter(vertex for edge in edges for vertex in edge)
    assert all(degrees[vertex] <= 1 for vertex in boundary)
    classes = Counter()
    for component in components(range(len(intervals)), edges):
        marks = len(component['vertices'] & boundary)
        if component['cycle']:
            assert marks == 0
            classes['cycles'] += 1
        else:
            assert marks <= 2
            classes['h'+str(marks)] += 1
    inventory = Counter(tuple(sorted((kinds[first], kinds[second]))) for first, second in reduced)
    beta = inventory['BP', 'BP']
    margin = classes['h0']+beta-classes['h2']-omitted
    assert original['surplus_twice']-2*original['boundary_budget'] == 2*margin
    assert (margin >= 0) == (classes['h2']+omitted <= classes['h0']+beta)
    totals['virtual_connector_models'] += 1
    totals['residual_unported_paths'] += omitted
    return dict(alpha=inventory['TP', 'TP'], beta=beta, gamma=inventory['BP', 'TP'],
                omitted=omitted, margin_twice=2*margin, **classes)


def extended_ports(current, bands, labels, intervals, owner, kinds, direct_ports, totals):
    locations = {point: (band, column, position) for band, columns in enumerate(bands)
                 for column, cells in enumerate(columns) for position, point in enumerate(cells)
                 if point in kinds}
    result = {point: list(choices) for point, choices in direct_ports.items()}
    side_users = defaultdict(set)
    cap_users = defaultdict(set)
    for point, kind in kinds.items():
        if kind != 'TP':
            continue
        band, column, position = locations[point]
        for direction in (-1, 1):
            middle, target = column+direction, column+2*direction
            if not 0 <= target < len(bands[band]):
                continue
            if labels[band][middle] == ('B', 'T') and labels[band][target] == ('B', 'B'):
                if bands[band][middle][position] in current[2]:
                    result[point].append((band, target))
                    cap_users[bands[band][middle][position]].add(point)
                    totals['selected_cap_access_candidates'] += 1
        for port in result[point]:
            interval = intervals[owner[port]]
            side = 'left' if column < port[1] else 'right'
            assert port[1] == interval['first' if side == 'left' else 'last']
            side_users[owner[port], side].add(point)
    assert all(len(users) == 1 for users in side_users.values())
    assert all(len(users) == 1 for users in cap_users.values())
    totals['extended_access_ownership_models'] += 1
    return result


def inspect_extended(current, bands, links, totals):
    original, labels, intervals, owner, kinds, pairs, ports = terminal_data(current, bands)
    extended = extended_ports(current, bands, labels, intervals, owner, kinds, ports, totals)
    reduced, _, _ = cancel_pairs(kinds, pairs, links, totals)
    return virtual_connectors(original, labels, intervals, owner, kinds, reduced, extended, totals)


def inspect(current, bands, links, totals):
    original, labels, intervals, owner, kinds, pairs, ports = terminal_data(current, bands)
    assert all(abs(first[0]-second[0])+abs(first[1]-second[1]) == 1
               for first, second in links)
    reduced, _, records = cancel_pairs(kinds, pairs, links, totals)
    virtual = virtual_connectors(original, labels, intervals, owner, kinds, reduced, ports, totals)
    return dict(original={key: original[key] for key in ('alpha', 'beta', 'gamma')},
                links=links, virtual=virtual,
                cancellation_components=[record for record in records
                                         if len(record['vertices']) > 2 or record['cycle']],
                free_missing_tp=sorted(point for pair in reduced for point in pair
                                       if all(kinds[tip] == 'TP' for tip in pair)
                                       and not ports[point]))


def direct_family(width, height):
    assert width >= 6 and height >= 4 and width % 2 == height % 2 == 0
    selected = {(4, 3), (4, 5), (4, 7), (5, 2), (5, 8), (6, 6), (7, 5),
                (width+4, 2), (width+4, height+4)}
    selected |= {(width+5, column) for column in range(3, height+4, 2)}
    selected |= {(width+2, column) for column in range(6, height+3, 2)}
    matching = [((row, 3), (row+1, 3)) for row in range(5, width+4, 2)]
    matching += [((row, 4), (row+1, 4)) for row in range(6, width+3, 2)]
    matching += [((5, 4), (5, 5)), ((5, 6), (5, 7))]
    matching += [((width+4, column), (width+4, column+1))
                 for column in range(4, height+3, 2)]
    matching += [((width+3, column), (width+3, column+1))
                 for column in range(5, height+2, 2)]
    return width+12, 2*height+12, selected, matching


def uniform_certificates(current, width, height, totals):
    end_row = width+4
    schedule = []
    schedule += [((5, 3), ((4, 3), (5, 2))), ((5, 7), ((4, 7), (5, 8))),
                 ((end_row, 3), ((end_row, 2), (end_row+1, 3))),
                 ((end_row, height+3), ((end_row, height+4), (end_row+1, height+3))),
                 ((5, 5), ((4, 5), (5, 6)))]
    for column in range(height+1, 4, -2):
        schedule.append(((end_row, column), ((end_row+1, column), (end_row, column+1))))
    for column in range(6, height+3, 2):
        schedule.append(((end_row-1, column), ((end_row-2, column), (end_row, column))))
    schedule.append(((end_row-1, 4), ((end_row-1, 3), (end_row-1, 5))))
    for row in range(6, end_row-1, 2):
        schedule += [((row, 4), ((row-1, 4), (row, 3))),
                     ((row+1, 3), ((row, 3), (row+1, 4)))]
    for row in range(end_row-2, 5, -2):
        schedule += [((row, 3), ((row+1, 3), (row, 4))),
                     ((row-1, 4), ((row-1, 3), (row, 4)))]
    schedule.append(((5, 6), ((6, 6), (5, 5))))
    for column in range(4, height+3, 2):
        schedule.append(((end_row, column), ((end_row, column-1), (end_row-1, column))))
        if column <= height:
            schedule.append(((end_row-1, column+1), ((end_row-1, column), (end_row, column+1))))
    endpoints = endpoints_of(current)
    mates = {first: second for pair in current[3] for first, second in (pair, pair[::-1])}
    frozen = set()
    for point, witnesses in schedule:
        assert point in endpoints-frozen and len(set(witnesses)) == 2
        assert all(abs(point[0]-other[0])+abs(point[1]-other[1]) == 1
                   and other != mates[point] for other in witnesses)
        assert all(other in current[2] or mates[other] in frozen for other in witnesses)
        frozen.add(point)
    assert frozen == endpoints
    totals['uniform_serial_freezing_events'] += len(schedule)
    forced = [((5, 7), (5, 6)), ((5, 5), (5, 4)), ((5, 3), (6, 3))]
    for row in range(6, end_row-1, 2):
        forced += [((row, 4), (row+1, 4)), ((row+1, 3), (row+2, 3))]
    for column in range(4, height+3, 2):
        forced.append(((end_row, column), (end_row, column+1)))
        if column <= height:
            forced.append(((end_row-1, column+1), (end_row-1, column+2)))
    remaining = set(endpoints)
    for first, second in forced:
        assert first in remaining and second in remaining and mates[first] == second
        assert {point for point in remaining
                if abs(first[0]-point[0])+abs(first[1]-point[1]) == 1} == {second}
        remaining -= {first, second}
    assert not remaining
    totals['uniform_forced_template_edges'] += len(forced)


def family_control(width, height, totals):
    current = direct_family(width, height)
    reference = stack(width, height, ['missing'])
    assert current[:3] == reference[:3]
    assert {frozenset(edge) for edge in current[3]} == {frozenset(edge) for edge in reference[3]}
    direct_check(*current)
    force_matching(current, totals)
    uniform_certificates(current, width, height, totals)
    bands = whole_bands(current)
    injection = inspect_injection(current, bands, Counter(), True)
    assert injection['assignment'] == [((5, 3), (5, 4)), ((width+4, 3), (width+4, 4))]
    record = inspect(current, bands, injection['assignment'], totals)
    assert record['original'] == dict(alpha=1, beta=0, gamma=height+1)
    assert record['virtual']['alpha'] == record['virtual']['omitted'] == 1
    assert record['virtual']['beta'] == 0 and record['virtual']['gamma'] == height-1
    assert record['free_missing_tp'] == [(5, 5), (width+4, 5)]
    long_component = next(component for component in record['cancellation_components']
                          if component['alpha'])
    assert (long_component['alpha'], long_component['beta'], long_component['gamma']) == (1, 0, 2)
    _, _, _, _, kinds, pairs, ports = terminal_data(current, bands)
    bottom_tp = [(width+4, column) for column in range(3, height+4, 2)]
    bottom_bp = [(width+4, column) for column in range(4, height+3, 2)]
    assert len(bottom_tp) == len(bottom_bp)+1 == height//2+1
    assert all(kinds[point] == 'TP' and not ports[point] for point in bottom_tp)
    assert all(kinds[point] == 'BP' for point in bottom_bp)
    assert {other for point in bottom_tp for other in kinds
            if kinds[other] == 'BP'
            and point[0] == other[0] and abs(point[1]-other[1]) == 1} == set(bottom_bp)
    extended_links = [((5, 3), (5, 4)), ((5, 5), (5, 6))]
    extended_links += [((width+4, column-1), (width+4, column))
                       for column in range(4, height+3, 2)]
    extended = inspect(current, bands, extended_links, totals)
    assert extended['free_missing_tp'] == [(5, 7), (width+4, height+3)]
    assert extended['virtual']['alpha'] == extended['virtual']['omitted'] == 1
    assert extended['virtual']['beta'] == 0
    used_bp = {second for _, second in extended_links}
    assert all(other in used_bp for point in extended['free_missing_tp'] for other in kinds
               if kinds[other] == 'BP' and point[0] == other[0]
               and abs(point[1]-other[1]) == 1)
    own_mixed_links = [((5, 5), (5, 4)), ((width+4, 5), (width+4, 4))]
    own_cycles = inspect(current, bands, own_mixed_links, totals)
    assert sum(component['cycle'] for component in own_cycles['cancellation_components']) == 2
    cropped_bands = [[((row, column), (row+1, column)) for column in range(height+6)]
                     for row in range(4, width+5, 2)]
    cropped_cells = {point for band in cropped_bands for column in band for point in column}
    endpoints = endpoints_of(current)
    assert current[2] | endpoints <= cropped_cells
    assert all((2*(row//2)+offset_row, 2*(column//2)+offset_column) in cropped_cells
               for row, column in endpoints for offset_row, offset_column in itertools.product((0, 1), repeat=2))
    cropped = inspect(current, cropped_bands, injection['assignment'], totals)
    assert cropped['virtual']['alpha'] == cropped['virtual']['omitted'] == 1
    assert cropped['virtual']['beta'] == 0
    assert cropped['virtual']['margin_twice'] == width*height+2*width-2*height-10 > 0
    totals['physical_receiver_closed_cropped_packets'] += 1
    extended_uncancelled = inspect_extended(current, cropped_bands, [], totals)
    assert extended_uncancelled['omitted'] == extended_uncancelled['beta'] == 0
    assert extended_uncancelled.get('h2', 0) == 0
    assert extended_uncancelled['h0']*2 == cropped['virtual']['margin_twice']
    extended_first_injection = inspect_extended(current, cropped_bands, injection['assignment'], totals)
    assert extended_first_injection['omitted'] == 1
    extended_maximal = inspect_extended(current, cropped_bands, extended_links, totals)
    assert extended_maximal['omitted'] == 0
    assert extended_maximal.get('h2', 0) == (1 if height == 4 else 0)
    totals['selected_cap_family_compensations'] += 1
    totals['selected_cap_boundary_collision_controls'] += height == 4
    totals['fully_frozen_parameter_pairs'] += 1
    totals['hall_deficient_rows'] += 2
    return current, dict(width=width, height=height, injection=record, maximal_continuation=extended,
                         cropped_packet=cropped,
                         selected_cap_compensation=extended_uncancelled,
                         selected_cap_after_first_injection=extended_first_injection,
                         selected_cap_after_maximal_continuation=extended_maximal,
                         bottom_hall_counts=[len(bottom_tp), len(bottom_bp)])


def abstract_controls(totals):
    for count in range(1, 8):
        vertices = list(range(2*count))
        pairs = [(2*index, 2*index+1) for index in range(count)]
        for flags in itertools.product(('BP', 'TP'), repeat=2*count):
            if count > 4 and flags not in (('BP', 'TP')*count, ('TP', 'BP')*count):
                continue
            kinds = dict(zip(vertices, flags))
            links = [(2*index+1, 2*index+2) for index in range(count-1)
                     if flags[2*index+1] != flags[2*index+2]]
            cancel_pairs(kinds, pairs, links, totals)
            if flags[-1] != flags[0]:
                cancel_pairs(kinds, pairs, links+[(2*count-1, 0)], totals)
            totals['abstract_controls'] += 1


def all_link_matchings(choices, index=0, used=frozenset()):
    if index == len(choices):
        yield []
        return
    yield from all_link_matchings(choices, index+1, used)
    pair = choices[index]
    if not used & set(pair):
        for following in all_link_matchings(choices, index+1, used | set(pair)):
            yield [pair]+following


def arbitrary_horizontal_control(width, height, totals):
    current = direct_family(width, height)
    original, _, _, _, kinds, pairs, ports = terminal_data(current, whole_bands(current))
    closed_rows = {point for point in kinds if point[0] in (5, width+4)}
    assert all((first in closed_rows) == (second in closed_rows) for first, second in pairs)
    assert sum(kinds[point] == 'TP' for point in closed_rows) == height//2+4
    assert sum(kinds[point] == 'BP' for point in closed_rows) == height//2+2
    assert all(ports[point] == [] for point in closed_rows if kinds[point] == 'TP')
    choices = [(first, second) for first in sorted(kinds) for second in sorted(kinds)
               if kinds[first] == 'TP' and kinds[second] == 'BP'
               and first[0] == second[0] and abs(first[1]-second[1]) == 1]
    assert all((first in closed_rows) == (second in closed_rows) for first, second in choices)
    seen = set()
    for links in all_link_matchings(choices):
        key = tuple(links)
        assert key not in seen
        seen.add(key)
        reduced, inventory, _ = cancel_pairs(kinds, pairs, links, totals)
        assert inventory['TP', 'TP'] == original['alpha'] == 1
        assert inventory['BP', 'BP'] == original['beta'] == 0
        remaining_alpha = next(pair for pair in reduced if all(kinds[point] == 'TP' for point in pair))
        assert {point[0] for point in remaining_alpha} == {5, width+4}
        assert all(point in closed_rows and not ports[point] for point in remaining_alpha)
        totals['all_horizontal_matching_controls'] += 1
    totals['exhaustive_horizontal_parameter_pairs'] += 1


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    totals, examples = Counter(), []
    abstract_controls(totals)
    for width, height in itertools.product((6, 10), (4, 6, 8)):
        arbitrary_horizontal_control(width, height, totals)
    for width, height in itertools.product(range(6, 31, 2), range(4, 25, 2)):
        current, example = family_control(width, height, totals)
        if (width, height) in ((6, 4), (12, 8), (30, 24)):
            examples.append(example)
        if (width, height) == (6, 4):
            frozen, layers = frozen_certificate(current)
            assert frozen == endpoints_of(current)
            example['shape'] = current[:2]
            example['selected'] = sorted(current[2])
            example['matching'] = current[3]
            example['freezing_certificate'] = layers
            example['full_freezing_count'] = len(frozen)
            for symmetry in itertools.product((False, True), repeat=3):
                shape, selected, matching = transformed(*current, *symmetry)
                move = image_map(*current[:2], symmetry)
                bands = [[tuple(move(point) for point in column) for column in band]
                         for band in whole_bands(current)]
                links = [tuple(move(point) for point in pair)
                         for pair in example['injection']['links']]
                inspect((*shape, selected, matching), bands, links, totals)
                inspect_extended((*shape, selected, matching), bands, links, totals)
                totals['symmetry_controls'] += 1
    for copies in range(1, 33):
        current = stack(6, 4, ['missing']*copies)
        bands = whole_bands(current)
        injection = inspect_injection(current, bands, Counter(), True)
        record = inspect(current, bands, injection['assignment'], totals)
        assert record['virtual']['omitted'] == copies
        assert record['virtual']['alpha'] == copies and record['virtual']['beta'] == 0
        assert len(record['free_missing_tp']) == 2*copies
        extended = inspect_extended(current, bands, [], totals)
        assert extended['omitted'] == extended['beta'] == 0 and extended.get('h2', 0) == 0
        assert 2*extended['h0'] == record['virtual']['margin_twice']
        totals['independent_stack_controls'] += 1
    for kinds in itertools.product(('cycle', 'collision', 'missing'), repeat=3):
        current = stack(6, 4, kinds)
        bands = whole_bands(current)
        injection = inspect_injection(current, bands, Counter(), True)
        inspect(current, bands, injection['assignment'], totals)
        inspect_extended(current, bands, injection['assignment'], totals)
        totals['mixed_stack_controls'] += 1
    report = dict(status='PASS', controls=dict(totals), examples=examples,
                  scope='General written terminal-cancellation conservation and virtual connector ledger; '
                        'fully frozen uniformly stranded continuation and all-missing-TP Hall obstruction. '
                        'This refutes proposed port-exposure/automatic-credit rules, not the grid target.')
    arguments.output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(dict(status='PASS', controls=dict(totals))))


if __name__ == '__main__':
    main()
