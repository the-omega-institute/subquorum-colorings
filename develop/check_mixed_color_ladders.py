"""Physical controls for compatible unions and the all-length mixed-color family."""

import argparse
import itertools
import json
from pathlib import Path

from check_cooperative_promotion import apply_bundle, neighbors, occupied_degrees
from check_owned_donors import endpoint_data
from check_promotion_cores import color_data, frozen_certificate, peel
from check_residual_corridors import direct_check, graph_record, transformed

if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def mixed_ladder(left, right):
    middle = 2*left
    width = 2*(left+right)+1
    selected = {(row, column) for row in (-1, 2) for column in range(0, width, 2)}
    selected |= {(0, -1), (1, width)}
    matching = [((row, column), (row, column+1))
                for row in (0, 1) for column in range(0, middle, 2)]
    matching += [((0, middle), (1, middle))]
    matching += [((row, column), (row, column+1))
                 for row in (0, 1) for column in range(middle+1, width-1, 2)]
    promoted = {(row, column) for row in (0, 1) for column in range(width)
                if (column < middle and (row+column) % 2 == 1)
                or (column > middle and (row+column) % 2 == 0)}
    move = lambda vertex: (vertex[0]+2, vertex[1]+2)
    current = (6, width+3, {move(vertex) for vertex in selected},
               [(move(first), move(second)) for first, second in matching])
    return current, {move(vertex) for vertex in promoted}, middle+2


def endpoint_components(current):
    endpoints, adjacency, _ = endpoint_data(current)
    unseen = set(endpoints)
    components = []
    while unseen:
        pending = [unseen.pop()]
        component = set(pending)
        while pending:
            vertex = pending.pop()
            newly_seen = adjacency[vertex] & unseen
            unseen -= newly_seen
            component |= newly_seen
            pending.extend(newly_seen)
        components.append(component)
    return components


def verify(current, promoted, middle, left, right):
    width = 2*(left+right)+1
    objective = direct_check(*current)
    assert objective == 2*width+3 and len(current[2]) == width+3
    endpoints, _, squares = endpoint_data(current)
    assert len(endpoint_components(current)) == 1 and len(squares) == width-1
    assert min(occupied_degrees(current).values()) == 3
    frozen, layers = frozen_certificate(current)
    assert frozen == endpoints-promoted and len(frozen) == width+1
    mates = {endpoint: mate for edge in current[3] for endpoint, mate in (edge, edge[::-1])}
    bundle = [(vertex, mates[vertex]) for vertex in sorted(promoted)]
    changed = apply_bundle(current, bundle)
    assert direct_check(*changed) == objective
    assert len(bundle) == width-1 and len(changed[3]) == 1
    assert all(vertex[1] == middle for vertex in changed[3][0])
    assert not endpoint_data(changed)[2]
    for color, count in ((0, 2*right), (1, 2*left)):
        candidates, adjacency, needs = color_data(current, color)
        core, _ = peel(adjacency, needs)
        assert core == {vertex for vertex in promoted if sum(vertex) % 2 == color}
        assert len(core) == count
        single_color = apply_bundle(current, [(vertex, mates[vertex]) for vertex in sorted(core)])
        assert len(endpoint_data(single_color)[2]) == (2*left if color == 0 else 2*right)
    return dict(left=left, right=right, width=width, objective=objective,
                promoted=len(promoted), frozen=len(frozen), frozen_layers=len(layers),
                remaining_matching_edges=len(changed[3]))


def exact_bundles(left, right):
    current, promoted, middle = mixed_ladder(left, right)
    endpoints = {vertex for edge in current[3] for vertex in edge}
    examined = feasible = removing = 0
    maximum = 0
    for states in itertools.product((0, 1, 2), repeat=len(current[3])):
        if not any(states):
            continue
        chosen = set()
        deleted = set()
        for state, edge in zip(states, current[3]):
            if state:
                chosen.add(edge[state-1])
                deleted.add(edge[2-state])
        remaining = (current[2] | endpoints)-deleted
        valid = all(sum(adjacent in remaining for adjacent in neighbors(vertex)) <= 1
                    for vertex in chosen)
        examined += 1
        if not valid:
            continue
        feasible += 1
        assert chosen <= promoted
        left_indices = {index for index in range(left)
                        if (2, 2*index+3) in chosen}
        lower_indices = {index for index in range(left)
                         if (3, 2*index+2) in chosen}
        assert left_indices == lower_indices == set(range(len(left_indices)))
        right_indices = {index for index in range(right)
                         if (2, middle+2*index+2) in chosen}
        lower_right = {index for index in range(right)
                       if (3, middle+2*index+1) in chosen}
        assert right_indices == lower_right == set(range(right-len(right_indices), right))
        maximum = max(maximum, len(chosen))
        after_endpoints = endpoints-chosen-deleted
        squares = sum({(row, column) for row in (2, 3) for column in (start, start+1)}
                      <= after_endpoints for start in range(2, 2+2*(left+right)))
        if not squares:
            removing += 1
            assert {sum(vertex) % 2 for vertex in chosen} == {0, 1}
        assert squares == 2*(left-len(left_indices))+2*(right-len(right_indices))
    assert removing == 1 and maximum == len(promoted)
    assert feasible == (left+1)*(right+1)-1
    return dict(left=left, right=right, examined=examined, feasible=feasible,
                square_removing=removing, maximum_bundle_size=maximum)


def saturated_contact_obstacle():
    selected = {(0, 0), (-3, 0), (-2, -1), (-1, 1),
                (1, 1), (2, 2), (3, 0), (4, 1)}
    matching = [((-2, 0), (-1, 0)), ((2, 1), (3, 1))]
    move = lambda vertex: (vertex[0]+4, vertex[1]+2)
    current = (10, 6, {move(vertex) for vertex in selected},
               [(move(first), move(second)) for first, second in matching])
    objective = direct_check(*current)
    endpoints, _, _ = endpoint_data(current)
    components = endpoint_components(current)
    assert len(components) == 2
    assert frozen_certificate(current)[0] == endpoints
    graph, _ = graph_record(*current)
    tile = 2*3+1
    assert graph['t'][tile] == 2
    contacts = [move((0, 0)), move((1, 1))]
    owners = []
    for contact in contacts:
        adjacent_endpoints = {vertex for vertex in endpoints if vertex in neighbors(contact)}
        assert len(adjacent_endpoints) == 1
        owners.append(next(index for index, component in enumerate(components)
                           if adjacent_endpoints <= set(component)))
    assert owners[0] != owners[1]
    return dict(shape=current[:2], selected=sorted(current[2]), matching=current[3],
                objective=objective, contacts=contacts, owner_components=owners,
                shared_tile=[2, 1], shared_tile_selected=2, shared_tile_charge=0,
                all_endpoints_frozen=True,
                refuted_rule='Distinct occupied contacts of distinct frozen components necessarily provide distinct negative-charge tiles.',
                global_inequality_refuted=False)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--max-arm', type=int, default=12)
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    records = []
    images = 0
    for left, right in itertools.product(range(1, arguments.max_arm+1), repeat=2):
        current, promoted, middle = mixed_ladder(left, right)
        records.append(verify(current, promoted, middle, left, right))
        for symmetry in itertools.product((False, True), repeat=3):
            shape, selected, matching = transformed(*current, *symmetry)
            image = (*shape, selected, matching)
            moved = transformed(*current[:2], promoted, [], *symmetry)[1]
            mates = {endpoint: mate for edge in matching for endpoint, mate in (edge, edge[::-1])}
            assert frozen_certificate(image)[0] == {vertex for edge in matching for vertex in edge}-moved
            changed = apply_bundle(image, [(vertex, mates[vertex]) for vertex in sorted(moved)])
            assert not endpoint_data(changed)[2] and len(changed[3]) == 1
            images += 1
    exact = [exact_bundles(left, right) for left, right in ((1, 1), (1, 2), (2, 1), (2, 2), (1, 3), (3, 1))]
    report = dict(status='ALL_CHECKS_PASSED', family_cases=len(records), symmetry_images=images,
                  family=records, exact_oriented_controls=exact,
                  exact_oriented_bundles=sum(record['examined'] for record in exact),
                  saturated_contact_obstacle=saturated_contact_obstacle(),
                  scope='Finite controls of general all-length freezing, mixed-color necessity, maximum-bundle and compatible-union proofs; not a proof of the unrestricted pure-ladder question.')
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({key:value for key,value in report.items() if key not in ('family', 'saturated_contact_obstacle')}))


if __name__ == '__main__':
    main()
