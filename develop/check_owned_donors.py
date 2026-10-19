"""Physical controls for square-free endpoint structure and owned donors."""

import argparse
import itertools
import json
import re
from pathlib import Path

from check_blank_witness_compensation import witness_record
from check_cooperative_promotion import apply_bundle, neighbors, occupied_degrees
from check_pressured_collar_compensation import region_vertices
from check_promotion_cores import (
    all_oriented_bundles, anchored_diamonds, color_data, frozen_certificate, normalize, peel,
)
from check_residual_corridors import direct_check, transformed
from verify_grid_five_sixths import bits, pairs

if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def endpoint_data(current):
    endpoints = {vertex for edge in current[3] for vertex in edge}
    adjacency = {vertex: set(neighbors(vertex)) & endpoints for vertex in endpoints}
    squares = {vertex for vertex in endpoints
               if {vertex, (vertex[0]+1, vertex[1]), (vertex[0], vertex[1]+1),
                   (vertex[0]+1, vertex[1]+1)} <= endpoints}
    return endpoints, adjacency, squares


def check_structure(current):
    endpoints, adjacency, squares = endpoint_data(current)
    degrees = occupied_degrees(current)
    if any(value < 3 for value in degrees.values()) or squares:
        return None
    assert all(len(adjacent) <= 2 for adjacent in adjacency.values())
    visited = set()
    components = []
    for start in sorted(endpoints):
        if start in visited:
            continue
        component = {start}
        pending = [start]
        visited.add(start)
        while pending:
            vertex = pending.pop()
            for adjacent in adjacency[vertex]-visited:
                component.add(adjacent)
                visited.add(adjacent)
                pending.append(adjacent)
        assert len(component) % 2 == 0
        assert len({vertex[0] for vertex in component}) == 1 or len({vertex[1] for vertex in component}) == 1
        ordered = sorted(component)
        actual_matching = {frozenset(edge) for edge in current[3] if edge[0] in component}
        assert actual_matching == {frozenset(edge) for edge in zip(ordered[::2], ordered[1::2])}
        side_axis = 0 if ordered[0][0] == ordered[-1][0] else 1
        side_signs = []
        for vertex in ordered:
            perpendicular = [adjacent for adjacent in neighbors(vertex)
                             if adjacent in current[2] and adjacent[side_axis] != vertex[side_axis]]
            assert len(perpendicular) == 1
            side_signs.append(perpendicular[0][side_axis]-vertex[side_axis])
        assert all(first == -second for first, second in zip(side_signs, side_signs[1:]))
        supports = {adjacent for vertex in component for adjacent in neighbors(vertex)
                    if adjacent in current[2]}
        assert len(supports) == len(component)+2
        assert all(degrees[vertex] == 3 for vertex in component)
        assert all(sum(adjacent in current[2] for adjacent in neighbors(vertex)) == 3-len(adjacency[vertex])
                   for vertex in component)
        components.append(len(component))
    assert frozen_certificate(current)[0] == endpoints
    assert all(not peel(*color_data(current, color)[1:])[0] for color in (0, 1))
    return components


def local_controls():
    occupied = lambda label: int(label != 0)
    turns = branches = side_failures = 0
    for northwest, southwest, outer, far_north, northeast in itertools.product(range(3), repeat=5):
        north_valid = occupied(northwest)+occupied(far_north)+occupied(northeast)+1 <= 1
        southwest_valid = southwest != 1
        west_terminal = 1+occupied(northwest)+occupied(southwest)+occupied(outer) >= 3
        if north_valid and southwest_valid and west_terminal:
            assert southwest == 2
            turns += 1
    for southwest, southeast, outer in itertools.product(range(3), repeat=3):
        if southwest != 1 and southeast != 1 and 1+occupied(southwest)+occupied(southeast)+occupied(outer) >= 3:
            assert southwest == 2 or southeast == 2
            branches += 1
    for northeast, southeast, outer in itertools.product(range(3), repeat=3):
        if occupied(northeast) == occupied(southeast) == 0:
            assert 1+occupied(northeast)+occupied(southeast)+occupied(outer) < 3
            side_failures += 1
    budgets = 0
    for chosen, endpoints in itertools.product(range(3), repeat=2):
        if chosen+endpoints > 2:
            continue
        for saturated in range(endpoints+1):
            for claims in range(endpoints-saturated+1):
                charge = 2*chosen+endpoints+saturated-4
                assert charge+claims == -2*(2-chosen-endpoints)-(endpoints-saturated-claims) <= 0
                budgets += 1
    return dict(turn_models=turns, branch_models=branches, two_side_exclusions=side_failures,
                donor_budget_models=budgets)


def straight_comb(size):
    endpoints = [(2, 3+index) for index in range(2*size)]
    selected = {(1 if index % 2 == 0 else 3, column) for index, (_, column) in enumerate(endpoints)}
    selected |= {(2, 2), (2, 2*size+3)}
    return 6, 2*size+6, selected, list(zip(endpoints[::2], endpoints[1::2]))


def family_controls():
    records = []
    for size in range(1, 33):
        current = straight_comb(size)
        assert direct_check(*current) == 3*size+2
        assert check_structure(current) == [2*size]
        assert [len(layer) for layer in frozen_certificate(current)[1]] == [2]*size
        if size <= 6:
            assert all_oriented_bundles(current) == (3**size-1, 0)
        for symmetry in itertools.product((False, True), repeat=3):
            shape, selected, matching = transformed(*current, *symmetry)
            assert check_structure((*shape, selected, matching)) == [2*size]
        records.append(dict(matching=size, endpoints=2*size, selected=2*size+2, frozen_rounds=size))
    squares = []
    for offset in (1, 2):
        selected = {(offset-1, offset), (offset, offset+2),
                    (offset+2, offset+1), (offset+1, offset-1)}
        matching = [((offset, offset), (offset, offset+1)),
                    ((offset+1, offset), (offset+1, offset+1))]
        current = 6, 6, selected, matching
        assert direct_check(*current) == 6
        assert set(occupied_degrees(current).values()) == {3}
        assert endpoint_data(current)[2] == {(offset, offset)}
        for color in (0, 1):
            candidates, adjacency, needs = color_data(current, color)
            core = peel(adjacency, needs)[0]
            assert len(core) == 2
            changed = apply_bundle(current, [(endpoint, candidates[endpoint]) for endpoint in core])
            assert direct_check(*changed) == 6 and not changed[3]
        squares.append(dict(origin=[offset, offset], two_edge_core=True))
    return records, squares


def exhaustive_controls():
    records = []
    for rows, columns in ((2, 4), (2, 6), (3, 4)):
        count = original = normalized = nonempty = 0
        for selected_mask, _, indices in pairs(rows, columns):
            current = (rows, columns, {divmod(vertex, columns) for vertex in bits(selected_mask)},
                       [(divmod(first, columns), divmod(second, columns)) for first, second in indices])
            result = check_structure(current)
            original += result is not None
            nonempty += bool(result)
            ending, _ = normalize(current)
            endpoints, adjacency, squares = endpoint_data(ending)
            if max(map(len, adjacency.values()), default=0) <= 2:
                assert not squares
                assert check_structure(ending) is not None
                normalized += 1
            count += 1
        records.append(dict(shape=[rows, columns], feasible_pairs=count, square_free_terminal=original,
                            nonempty_terminal=nonempty, degree_two_normalized=normalized))
    return records


def patch_template(symmetry):
    current, core = anchored_diamonds(1)
    donors = {(1, 0), (2, 3)}
    cells = region_vertices(core | donors)
    patch = (*current[:2], current[2] & cells, current[3])
    shape, selected, matching = transformed(*patch, *symmetry)
    moved_core = transformed(*patch[:2], region_vertices(core), [], *symmetry)[1]
    moved_cells = transformed(*patch[:2], cells, [], *symmetry)[1]
    return selected, matching, moved_core, moved_cells


def packing_controls():
    base = patch_template((False, False, False))
    candidate_count = core_disjoint = overlap_attempts = feasible_pairs = 0
    for symmetry in itertools.product((False, True), repeat=3):
        selected, matching, core, cells = patch_template(symmetry)
        for vertical, horizontal in itertools.product(range(-8, 9, 2), repeat=2):
            shift = lambda vertex: (vertex[0]+vertical, vertex[1]+horizontal)
            chosen = {shift(vertex) for vertex in selected}
            moved_matching = [tuple(shift(vertex) for vertex in edge) for edge in matching]
            moved_core = {shift(vertex) for vertex in core}
            moved_cells = {shift(vertex) for vertex in cells}
            candidate_count += 1
            if base[2] & moved_core:
                continue
            core_disjoint += 1
            overlap = bool(base[3] & moved_cells)
            overlap_attempts += overlap
            first_endpoints = {vertex for edge in base[1] for vertex in edge}
            second_endpoints = {vertex for edge in moved_matching for vertex in edge}
            labels = lambda vertex, chosen, endpoints: 1 if vertex in chosen else 2 if vertex in endpoints else 0
            if any(labels(vertex, base[0], first_endpoints) != labels(vertex, chosen, second_endpoints)
                   for vertex in base[3] & moved_cells):
                continue
            combined = list({frozenset(edge) for edge in base[1]+moved_matching})
            used = [vertex for edge in combined for vertex in edge]
            if len(used) != len(set(used)):
                continue
            merged_selected = base[0] | chosen
            occupied = merged_selected | set(used)
            if any(sum(adjacent in occupied for adjacent in neighbors(vertex)) > 1 for vertex in merged_selected):
                continue
            assert not overlap
            feasible_pairs += 1
    assert overlap_attempts and feasible_pairs
    return dict(pair_placements=candidate_count, disjoint_core_placements=core_disjoint,
                overlapping_patch_attempts=overlap_attempts, feasible_disjoint_core_pairs=feasible_pairs,
                feasible_overlapping_patches=0)


def shared_donor_control():
    current, core = anchored_diamonds(1)
    cells = region_vertices(core | {(1, 0), (2, 3)})
    selected = (current[2] & cells)-{(2, 0)}
    reflect = lambda vertex: (vertex[0], 1-vertex[1])
    selected |= {reflect(vertex) for vertex in selected}
    matching = current[3]+[tuple(reflect(vertex) for vertex in edge) for edge in current[3]]
    shift = lambda vertex: (vertex[0], vertex[1]+6)
    current = (8, 14, {shift(vertex) for vertex in selected},
               [tuple(shift(vertex) for vertex in edge) for edge in matching])
    note = Path(__file__).resolve().parents[1]/'docs/SQUARE_FREE_ENDPOINTS_AND_OWNED_DONORS.md'
    displayed = re.search(r'T=\{(.*?)\},\s+M=\{(.*?)\}\.', note.read_text(), re.DOTALL)
    assert displayed
    coordinates = lambda text: [tuple(map(int, pair)) for pair in re.findall(r'\((\d+),(\d+)\)', text)]
    assert set(coordinates(displayed[1])) == current[2]
    displayed_matching = coordinates(displayed[2])
    assert list(zip(displayed_matching[::2], displayed_matching[1::2])) == current[3]
    cores = [{(row, column+3) for row, column in core},
             {(row, -column+3) for row, column in core}]
    donors = {(1, 3), (2, 0), (2, 6)}
    assert direct_check(*current) == 22
    mate = {endpoint: partner for edge in current[3] for endpoint, partner in (edge, edge[::-1])}
    charges = []
    claims = [0, 0]
    donor_records = []
    for donor in sorted(donors):
        vertices = region_vertices({donor})
        chosen = len(current[2] & vertices)
        endpoints = set(mate) & vertices
        claim_owners = []
        for endpoint in sorted(endpoints):
            owners = [index for index, tiles in enumerate(cores) if mate[endpoint] in region_vertices(tiles)]
            assert len(owners) == 1
            owner = owners[0]
            assert len(current[2] & region_vertices({(mate[endpoint][0]//2, mate[endpoint][1]//2)})) == 1
            claims[owner] += 1
            claim_owners.append(owner)
        charge = witness_record(current, {donor}, [])['regional']['charge_twice']
        assert chosen+len(endpoints) == 2 and charge+len(endpoints) == 0
        charges.append(charge)
        donor_records.append(dict(tile=donor, selected=chosen, endpoints=len(endpoints),
                                  claim_owners=claim_owners, charge_twice=charge))
    assert sorted(charges) == [-2, -1, -1] and claims == [2, 2]
    assert all(witness_record(current, tiles, [])['regional']['charge_twice'] == 2 for tiles in cores)
    patch = set.union(*cores, donors)
    assert len(patch) == 11 and witness_record(current, patch, [])['regional']['charge_twice'] == 0
    for symmetry in itertools.product((False, True), repeat=3):
        shape, selected, matching = transformed(*current, *symmetry)
        moved = transformed(*current[:2], region_vertices(patch), [], *symmetry)[1]
        moved_tiles = {(row//2, column//2) for row, column in moved}
        assert witness_record((*shape, selected, matching), moved_tiles, [])['regional']['charge_twice'] == 0
    return dict(shape=current[:2], selected=sorted(current[2]), matching=current[3],
                cores=[sorted(tiles) for tiles in cores], donors=donor_records,
                core_claims=claims, patch_tiles=11, patch_charge_twice=0, symmetry_images=8,
                bundle_terminality_claimed=False)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    family, squares = family_controls()
    report = dict(status='ALL_CHECKS_PASSED', local=local_controls(), family=family,
                  symmetry_images=8*len(family), removable_squares=squares,
                  exhaustive=exhaustive_controls(), packing=packing_controls(),
                  shared_donor=shared_donor_control(),
                  scope='Finite controls for separate general written proofs; no universal grid inequality, full geometric Lean formalization or external novelty claim.')
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({key: value for key, value in report.items() if key != 'family'}))


if __name__ == '__main__':
    main()
