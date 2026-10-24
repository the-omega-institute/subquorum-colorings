"""Check exact receiver overlap and fully frozen PP boundary-source collisions."""

import argparse
from collections import Counter, defaultdict
import itertools
import json
from pathlib import Path

from check_component_receivers import endpoint_components, vertices_of
from check_cooperative_promotion import neighbors, occupied_degrees
from check_even_bridge_support_completion import endpoints_of, tiles_of
from check_native_guard_compensation import force_matching
from check_neutral_pair_donor_saturation import neutral_pair
from check_neutral_portal_strip_compensation import image_map
from check_occupied_strip_matching_flux import matchings
from check_pp_path_terminal_ledger import inspect as inspect_paths
from check_residual_corridors import direct_check, transformed


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def receiver_ledger(current, packets, totals):
    direct_check(*current)
    assert current[0] % 2 == current[1] % 2 == 0
    selected, endpoints = current[2], endpoints_of(current)
    components = endpoint_components(current)
    receivers = [tiles_of(component) for component in components]
    all_tiles = set(itertools.product(range(current[0]//2), range(current[1]//2)))
    packet_union = set()
    for packet in packets:
        assert packet <= all_tiles and not packet & packet_union
        packet_union |= packet
    outside_components = []
    multiplicity = defaultdict(list)
    for index, (component, receiver) in enumerate(zip(components, receivers)):
        assert len(component) % 2 == 0
        touched = [packet for packet in packets if packet & receiver]
        if touched:
            assert len(touched) == 1 and receiver <= touched[0]
        else:
            outside_components.append(index)
        for tile in receiver:
            multiplicity[tile].append(index)
    shared, correction = [], 0
    for tile, owners in multiplicity.items():
        local = endpoints & vertices_of({tile})
        if len(local) == 2:
            first, second = sorted(local)
            if abs(first[0]-second[0]) == abs(first[1]-second[1]) == 1 and len(owners) == 1:
                totals['local_diagonal_same_global_component_tiles'] += 1
        if len(owners) > 1:
            cells = vertices_of({tile})
            local = endpoints & cells
            assert len(owners) == len(local) == 2 and not selected & cells
            first, second = sorted(local)
            assert abs(first[0]-second[0]) == abs(first[1]-second[1]) == 1
            assert all(occupied_degrees(current)[point] <= 2 for point in local)
            shared.append(tile)
        if tile not in packet_union:
            correction += (len(owners)-1)*(2-len(selected & vertices_of({tile})))
    outside_shared = set(shared)-packet_union
    assert correction == 2*len(outside_shared)
    charges = [len(component)//2+sum(len(selected & vertices_of({tile}))-2
                                   for tile in receiver)
               for component, receiver in zip(components, receivers)]
    positive = sum(max(0, charges[index]) for index in outside_components)
    negative = sum(max(0, -charges[index]) for index in outside_components)
    blank_tiles = all_tiles-packet_union-set(multiplicity)
    deficit = sum(2-len(selected & vertices_of({tile})) for tile in blank_tiles)
    assert all(len(selected & vertices_of({tile})) <= 2 for tile in blank_tiles)
    surplus_twice = sum(4*len(packet)-2*len(selected & vertices_of(packet))
                        -len(endpoints & vertices_of(packet)) for packet in packets)
    margin_twice = current[0]*current[1]-2*len(selected)-2*len(current[3])
    uncorrected = surplus_twice+2*deficit-2*positive+2*negative
    assert margin_twice == uncorrected-4*len(outside_shared)
    if all(degree >= 3 for degree in occupied_degrees(current).values()):
        assert not shared
        totals['single_terminal_disjoint_receiver_models'] += 1
    totals['receiver_models'] += 1
    totals['receiver_overlap_models'] += bool(shared)
    totals['outside_shared_tiles'] += len(outside_shared)
    totals['inside_shared_tiles'] += len(set(shared) & packet_union)
    return dict(margin_twice=margin_twice, packet_surplus_twice=surplus_twice,
                outside_deficit=deficit, outside_positive=positive, outside_negative=negative,
                outside_shared_tiles=sorted(outside_shared),
                uncorrected_margin_twice=uncorrected, charges=charges)


def collision_family(width, height, copies):
    assert copies >= 1
    base, _, _ = neutral_pair(width, height)
    additions = {(2, 4), (2, 5), (2, width+4), (2, width+5)}
    selected, matching = set(), []
    for index in range(copies):
        move = lambda point: (point[1]+index*(width+12), point[0]+1)
        selected |= {move(point) for point in base[2] | additions}
        matching += [tuple(move(point) for point in edge) for edge in base[3]]
    return copies*(width+12), height+10, selected, matching


def forest_intervals(current, bands):
    selected, endpoints = current[2], endpoints_of(current)
    labels = [[tuple(sorted('T' if point in selected else 'P' if point in endpoints
                            else 'B' for point in column)) for column in columns]
              for columns in bands]
    nodes, owner = [], {}
    for band, row in enumerate(labels):
        remaining = {column for column, label in enumerate(row)
                     if label in (('B', 'B'), ('T', 'T'))}
        while remaining:
            start = min(remaining)
            reached, pending = {start}, [start]
            remaining.remove(start)
            while pending:
                column = pending.pop()
                added = {other for other in (column-1, column+1) if other in remaining
                         and (row[column] == ('T', 'T') or row[other] == ('T', 'T'))}
                remaining -= added
                reached |= added
                pending.extend(added)
            assert reached == set(range(min(reached), max(reached)+1))
            assert len(reached) % 2 == 1
            index = len(nodes)
            nodes.append(dict(band=band, first=min(reached), last=max(reached)))
            owner.update({(band, column): index for column in reached})
    return labels, nodes, owner


def inspect_collision(current, width, height, copies, totals, bands=None):
    if bands is None:
        bands = [[((2*band, column), (2*band+1, column))
                  for column in range(2, height+8)] for band in range(current[0]//2)]
    record = inspect_paths(current, bands, totals, True)
    assert len(current[2]) == copies*(height+11) and len(current[3]) == copies*(width+height)
    assert (record['alpha'], record['beta'], record['gamma'], record['cuts']) == (
        copies, 0, copies*(height+1), 0)
    paths = [component for component in record['components'] if component['kind'] == ['TP', 'TP']]
    cycles = [component for component in record['components'] if component['kind'] == ['cycle']]
    assert len(cycles) == copies*(width//2-1)
    assert all(len(component['nodes']) == len(component['edges']) == 1 for component in cycles)
    labels, nodes, owner = forest_intervals(current, bands)
    assert len(nodes) == record['balance']
    adjacency, edges = defaultdict(set), []
    for path in paths:
        assert len(path['edges']) == width//2 and len(path['nodes']) == width//2+1
        terminals = path['nodes'][0], path['nodes'][-1]
        ports = []
        for band, column in terminals:
            assert column == 3 and labels[band][column-1] == ('B', 'B')
            assert labels[band][column+1] == ('B', 'P')
            endpoint = next(point for point in bands[band][column] if point in endpoints_of(current))
            assert len(set(neighbors(endpoint)) & current[2]) == 1
            index = owner[band, column-1]
            assert nodes[index] == dict(band=band, first=0, last=2)
            ports.append(index)
        first, second = ports
        assert first != second and first not in adjacency and second not in adjacency
        adjacency[first].add(second)
        adjacency[second].add(first)
        edges.append((first, second))
    assert len(edges) == copies
    component_at, component_count = {}, 0
    for node in range(len(nodes)):
        if node in component_at:
            continue
        reached = {node} | adjacency[node]
        assert len(reached) <= 2
        for other in reached:
            assert other not in component_at
            component_at[other] = component_count
        component_count += 1
    first_sources = {component_at[owner[band, 0]] for band in range(len(bands))}
    final_sinks = {component_at[owner[band, len(columns)-1]] for band, columns in enumerate(bands)}
    band_count = copies*(width//2+6)
    assert len(bands) == band_count
    assert len(first_sources) == band_count-copies
    assert len(final_sinks) == band_count and not first_sources & final_sinks
    assert len(first_sources | final_sinks) == 2*band_count-copies
    surplus = copies*(width*height//2+2*width+4*height+25)
    assert record['surplus_twice'] == 2*surplus
    assert record['balance'] == surplus+copies
    assert component_count == len(nodes)-copies == surplus
    interior_components = component_count-len(first_sources | final_sinks)
    assert interior_components == copies*(width*height//2+width+4*height+14)
    assert surplus-record['boundary_budget'] == copies*(width*height//2+width+4*height+13) > 0
    force_matching(current, totals)
    totals['source_collision_packets'] += 1
    totals['source_collisions'] += copies
    return dict(width=width, height=height, copies=copies, bands=band_count,
                alpha=record['alpha'], beta=record['beta'], gamma=record['gamma'],
                forest_intervals=len(nodes), joint_components=component_count,
                first_boundary_components=len(first_sources), final_boundary_components=len(final_sinks),
                boundary_components=len(first_sources | final_sinks), interior_components=interior_components,
                surplus=surplus, target=record['boundary_budget'], connector_cycle_count=0)


def exhaustive_receiver_controls(totals):
    census = []
    for length in range(2, 5):
        checked = 0
        points = [(row, column) for column in range(1, length) for row in range(4)]
        for labels in itertools.product(range(3), repeat=len(points)):
            if all(labels[-4+row] for row in (0, 1)) or all(labels[-4+row] for row in (2, 3)):
                continue
            selected = {point for point, label in zip(points, labels) if label == 1}
            endpoints = {point for point, label in zip(points, labels) if label == 2}
            if any(len(set(neighbors(point)) & (selected | endpoints)) > 1 for point in selected):
                continue
            for matching, exported in matchings(endpoints, False):
                assert not exported
                current = 4, length+length % 2, selected, matching
                receiver_ledger(current, [], totals)
                checked += 1
        census.append(dict(columns=length, actual_matchings=checked))
    return census


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    totals = Counter()
    reviewer = 8, 4, set(), [((1, 0), (2, 0)), ((3, 1), (4, 1)), ((6, 1), (6, 2))]
    example = receiver_ledger(reviewer, [{(3, 0), (3, 1)}], totals)
    assert example['margin_twice'] == 26 and example['uncorrected_margin_twice'] == 30
    assert example['outside_shared_tiles'] == [(1, 0)]
    receiver_ledger(reviewer, [set(itertools.product(range(4), range(2)))], totals)
    globally_connected_diagonal = 6, 6, set(), [((2, 2), (1, 2)), ((1, 3), (1, 4)),
                                              ((2, 4), (3, 4)), ((3, 3), (4, 3))]
    control = receiver_ledger(globally_connected_diagonal, [], totals)
    assert not control['outside_shared_tiles']
    assert totals['local_diagonal_same_global_component_tiles'] > 0
    samples = []
    for width, height, copies in itertools.product(range(6, 31, 2), range(4, 21, 2), (1, 2, 4)):
        current = collision_family(width, height, copies)
        result = inspect_collision(current, width, height, copies, totals)
        tiles = set(itertools.product(range(current[0]//2), range(1, height//2+4)))
        receiver = receiver_ledger(current, [tiles], totals)
        assert receiver['packet_surplus_twice'] == 2*result['surplus']
        assert not receiver['outside_shared_tiles'] and receiver['outside_positive'] == 0
        totals['physical_receiver_closed_collision_packets'] += 1
        if (width, height, copies) in ((6, 4, 1), (12, 8, 2), (30, 20, 4)):
            samples.append(result)
            bands = [[((2*band, column), (2*band+1, column))
                      for column in range(2, height+8)] for band in range(current[0]//2)]
            for symmetry in itertools.product((False, True), repeat=3):
                shape, selected, matching = transformed(*current, *symmetry)
                move = image_map(*current[:2], symmetry)
                image_bands = [[tuple(move(point) for point in column) for column in columns]
                               for columns in bands]
                image = *shape, selected, matching
                assert inspect_collision(image, width, height, copies, totals, image_bands) == result
                image_tiles = tiles_of({move(point) for point in vertices_of(tiles)})
                receiver_ledger(image, [image_tiles], totals)
                totals['collision_symmetry_images'] += 1
    for copies in range(1, 51):
        inspect_collision(collision_family(6, 4, copies), 6, 4, copies, totals)
        totals['unbounded_collision_parameters'] += 1
    census = exhaustive_receiver_controls(totals)
    assert totals['receiver_overlap_models'] > 0 and totals['inside_shared_tiles'] > 0
    result = dict(status='PASS', controls=dict(totals), reviewer_counterexample=example,
                  collision_samples=samples, short_census=census,
                  scope='Finite checks of written general diagonal-overlap correction, global physical-packet ledger, and arbitrary-parameter frozen/unique-matching boundary-source collision family. Acyclic connector source injection fails; target inequalities do not fail. General compensation open.')
    arguments.output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(dict(status=result['status'], controls=result['controls'], samples=samples)))


if __name__ == '__main__':
    main()
