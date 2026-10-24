"""Independent matching-exchange, receiver-flux and forcing controls."""

import argparse
from collections import Counter
import itertools
import json
from pathlib import Path

from check_charge_two_frozen_receiver import fixture
from check_component_receivers import endpoint_components, verify_terminal, vertices_of
from check_cooperative_promotion import apply_bundle, neighbors
from check_elbow_sources import elbow
from check_owned_donors import endpoint_data
from check_promotion_cores import frozen_certificate, normalize
from check_residual_corridors import direct_check, transformed
from rotor_networks import affine


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def canonical(matching):
    return {tuple(sorted(edge)) for edge in matching}


def perfect_matchings(endpoints):
    if not endpoints:
        yield ()
        return
    vertex = min(endpoints, key=lambda point: (len(set(neighbors(point)) & endpoints), point))
    for mate in sorted(set(neighbors(vertex)) & endpoints):
        for remainder in perfect_matchings(endpoints-{vertex, mate}):
            yield ((vertex, mate),)+remainder


def square_exchange(current):
    removed = canonical([((7, 3), (8, 3)), ((7, 4), (8, 4))])
    required = removed | canonical([((5, 5), (5, 6)), ((6, 2), (7, 2)),
                                    ((6, 4), (6, 3)), ((7, 5), (6, 5))])
    assert required <= canonical(current[3])
    occupied = current[2] | endpoint_data(current)[0]
    assert not {(4, 5), (6, 1), (7, 6)} & occupied
    matching = [edge for edge in current[3] if tuple(sorted(edge)) not in removed]
    matching += [((7, 3), (7, 4)), ((8, 3), (8, 4))]
    exchanged = *current[:3], matching
    assert direct_check(*current) == direct_check(*exchanged)
    assert endpoint_data(current)[0] == endpoint_data(exchanged)[0]
    mate = {vertex: partner for edge in matching for vertex, partner in (edge, edge[::-1])}
    promoted = [(5, 5), (6, 2), (6, 4), (7, 3), (7, 5)]
    bundle = [(point, mate[point]) for point in promoted]
    deleted = {partner for _, partner in bundle}
    retained_neighbors = {str(point): sorted(set(neighbors(point)) & (occupied-deleted))
                          for point in promoted}
    assert all(len(adjacent) <= 1 for adjacent in retained_neighbors.values())
    result = apply_bundle(exchanged, bundle)
    assert len(result[3]) == len(current[3])-5
    assert direct_check(*result) == direct_check(*current)
    return exchanged, result, retained_neighbors


def perfect_completion(endpoints, required):
    fixed = {point for edge in required for point in edge}
    assert len(fixed) == 2*len(required) and fixed <= endpoints
    assert all(second in set(neighbors(first)) for first, second in required)
    remaining = endpoints-fixed
    left = sorted(point for point in remaining if sum(point) % 2 == 0)
    if 2*len(left) != len(remaining):
        return None
    owners = {}

    def augment(vertex, seen):
        for candidate in sorted(set(neighbors(vertex)) & remaining):
            if candidate in seen:
                continue
            seen.add(candidate)
            if candidate not in owners or augment(owners[candidate], seen):
                owners[candidate] = vertex
                return True
        return False

    for vertex in left:
        if not augment(vertex, set()):
            return None
    completion = list(required)+[(owner, candidate) for candidate, owner in sorted(owners.items())]
    assert {point for edge in completion for point in edge} == endpoints
    assert len(completion)*2 == len(endpoints)
    return completion


def find_motif_move(current):
    endpoints = endpoint_data(current)[0]
    occupied = current[2] | endpoints
    required = [((5, 5), (5, 6)), ((6, 2), (7, 2)), ((6, 4), (6, 3)),
                ((7, 5), (6, 5)), ((7, 3), (8, 3)), ((7, 4), (8, 4))]
    promoted = [(5, 5), (6, 2), (6, 4), (7, 3), (7, 5)]
    blanks = {(4, 5), (6, 1), (7, 6)}
    for symmetry in itertools.product((False, True), repeat=3):
        anchor = affine((5, 5), symmetry)
        for target in sorted(endpoints):
            offset = tuple(target[index]-anchor[index] for index in range(2))
            move = lambda point: affine(point, symmetry, offset)
            translated = [tuple(move(point) for point in edge) for edge in required]
            footprint = {point for edge in translated for point in edge}
            if not footprint <= endpoints or {move(point) for point in blanks} & occupied:
                continue
            completed = perfect_completion(endpoints, translated)
            if completed is None:
                continue
            removed = canonical(translated[-2:])
            exchanged = [edge for edge in completed if tuple(sorted(edge)) not in removed]
            exchanged += [(move((7, 3)), move((7, 4))), (move((8, 3)), move((8, 4)))]
            mate = {vertex: partner for edge in exchanged
                    for vertex, partner in (edge, edge[::-1])}
            bundle = [(move(point), mate[move(point)]) for point in promoted]
            result = apply_bundle((*current[:3], exchanged), bundle)
            assert direct_check(*result) == direct_check(*current)
            assert len(result[3]) == len(current[3])-5
            return result, dict(symmetry=symmetry, offset=offset,
                                promoted=[vertex for vertex, _ in bundle],
                                deleted=[partner for _, partner in bundle])
    return None


def normalize_motif(current):
    moves = []
    while True:
        found = find_motif_move(current)
        if found is None:
            return current, moves
        current, move = found
        moves.append(move)


def region_data(current, component):
    tiles = {(row//2, column//2) for row, column in component}
    selected = len(current[2] & vertices_of(tiles))
    return tiles, selected+len(component)//2-2*len(tiles)


def check_flux(before, after):
    old_ledger, new_ledger = verify_terminal(before), verify_terminal(after)
    assert before[:2] == after[:2]
    assert before[2] <= after[2]
    assert endpoint_data(after)[0] <= endpoint_data(before)[0]
    assert old_ledger['objective'] == new_ledger['objective']
    old_components, new_components = endpoint_components(before), endpoint_components(after)
    accounted_freed = set()
    accounted_children = set()
    records = []
    for component in old_components:
        old_tiles, old_charge = region_data(before, component)
        descendants = [index for index, child in enumerate(new_components) if child <= component]
        assert not accounted_children & set(descendants)
        accounted_children.update(descendants)
        surviving_tiles = set()
        descendant_charge = 0
        for index in descendants:
            tiles, charge = region_data(after, new_components[index])
            assert not surviving_tiles & tiles
            surviving_tiles |= tiles
            descendant_charge += charge
        assert surviving_tiles <= old_tiles
        freed = old_tiles-surviving_tiles
        assert not freed & accounted_freed
        accounted_freed |= freed
        freed_deficit = sum(2-len(after[2] & vertices_of({tile})) for tile in freed)
        assert freed_deficit >= 0
        assert descendant_charge == old_charge+freed_deficit
        records.append(dict(old_charge=old_charge, descendant_charge=descendant_charge,
                            freed_deficit=freed_deficit, freed_tiles=sorted(freed)))
    assert accounted_children == set(range(len(new_components)))
    total_flux = sum(record['freed_deficit'] for record in records)
    assert new_ledger['empty_deficit'] == old_ledger['empty_deficit']+total_flux
    return dict(before=old_ledger, after=new_ledger, components=records, flux=total_flux)


def pinwheel():
    selected = {(2, 3), (3, 5), (5, 4), (4, 2)}
    matching = [((3, 3), (4, 3)), ((3, 4), (4, 4))]
    current = 8, 8, selected, matching
    result = apply_bundle(current, [((3, 3), (4, 3)), ((4, 4), (3, 4))])
    return current, result


def union(first, second):
    move = lambda point: (point[0]+22, point[1]+2)
    selected = first[2] | {move(point) for point in second[2]}
    matching = first[3]+[tuple(move(point) for point in edge) for edge in second[3]]
    return 40, 20, selected, matching


def elbow_forcing(width, height):
    forced = [((2, 0), (1, 0))]
    for column in range(0, width, 2):
        forced.append(((0, column), (0, column+1)))
        if column < width-2:
            forced.append(((1, column+1), (1, column+2)))
    for row in range(1, height, 2):
        forced.append(((row, width-1), (row+1, width-1)))
        if row < height-1:
            forced.append(((row+1, width-2), (row+2, width-2)))
    current = elbow(width, height)
    endpoints = {(row-4, column-5) for row, column in endpoint_data(current)[0]}
    remaining = set(endpoints)
    for leaf, mate in forced:
        assert leaf in remaining and set(neighbors(leaf)) & remaining == {mate}
        remaining.difference_update((leaf, mate))
    assert not remaining
    original = [tuple((row-4, column-5) for row, column in edge) for edge in current[3]]
    assert canonical(forced) == canonical(original)
    assert frozen_certificate(current)[0] == endpoint_data(current)[0]
    return len(forced)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    initial = fixture()[0]
    assert frozen_certificate(initial)[0] == endpoint_data(initial)[0]
    exchanged, final, retained_neighbors = square_exchange(initial)
    assert all(len(adjacent) == 1 for adjacent in retained_neighbors.values())
    sparse_matching = [((5, 5), (5, 6)), ((6, 2), (7, 2)), ((6, 4), (6, 3)),
                       ((7, 5), (6, 5)), ((7, 3), (8, 3)), ((7, 4), (8, 4))]
    _, sparse_result, sparse_neighbors = square_exchange((14, 10, set(), sparse_matching))
    assert len(sparse_neighbors[str((6, 4))]) == 0 and len(sparse_result[3]) == 1
    assert frozen_certificate(final)[0] == endpoint_data(final)[0]
    main_record = check_flux(initial, final)
    matching_histogram = Counter()
    completion_controls = 0
    required = [((5, 5), (5, 6)), ((6, 2), (7, 2)), ((6, 4), (6, 3)),
                ((7, 5), (6, 5)), ((7, 3), (8, 3)), ((7, 4), (8, 4))]
    for matching in perfect_matchings(endpoint_data(initial)[0]):
        current = *initial[:3], list(matching)
        frozen, _ = frozen_certificate(current)
        matching_histogram[len(frozen)] += 1
        normalized, _ = normalize(current)
        check_flux(current, normalized)
        completed = perfect_completion(endpoint_data(current)[0], required)
        assert completed is not None
        _, unlocked, _ = square_exchange((*current[:3], completed))
        check_flux(current, unlocked)
        completion_controls += 1
    assert matching_histogram == {27: 5, 38: 3}
    final_matchings = list(perfect_matchings(endpoint_data(final)[0]))
    assert len(final_matchings) == 1
    forcing_certificate = [((1, 4), (2, 4)), ((3, 1), (4, 1)), ((3, 4), (4, 4)),
                           ((5, 1), (5, 2)), ((4, 2), (4, 3)), ((5, 3), (5, 4)),
                           ((8, 8), (8, 7)), ((8, 6), (8, 5)), ((10, 4), (9, 4)),
                           ((8, 4), (8, 3)), ((9, 3), (9, 2)), ((8, 2), (8, 1)),
                           ((9, 1), (10, 1)), ((11, 1), (12, 1))]
    remaining = set(endpoint_data(final)[0])
    for leaf, partner in forcing_certificate:
        assert leaf in remaining and set(neighbors(leaf)) & remaining == {partner}
        remaining.difference_update((leaf, partner))
    assert not remaining and canonical(forcing_certificate) == canonical(final[3])
    assert len(list(perfect_matchings({(0, 0), (0, 1), (1, 0), (1, 1)}))) == 2
    assert perfect_completion({(0, column) for column in range(4)},
                              [((0, 1), (0, 2))]) is None
    assert perfect_completion({(0, column) for column in range(4)}, []) is not None
    wheel_before, wheel_after = pinwheel()
    assert check_flux(wheel_before, wheel_after)['flux'] == 2
    mixed_before, mixed_after = union(initial, wheel_before), union(final, wheel_after)
    assert check_flux(mixed_before, mixed_after)['flux'] == 2
    images = positive_flux = algorithm_controls = 0
    for before, after in ((initial, final), (wheel_before, wheel_after), (mixed_before, mixed_after)):
        for symmetry in itertools.product((False, True), repeat=3):
            shape_before, selected_before, matching_before = transformed(*before, *symmetry)
            shape_after, selected_after, matching_after = transformed(*after, *symmetry)
            record = check_flux((*shape_before, selected_before, matching_before),
                                (*shape_after, selected_after, matching_after))
            positive_flux += record['flux'] > 0
            images += 1
            if before is initial:
                image = *shape_before, selected_before, matching_before
                reduced, moves = normalize_motif(image)
                assert moves and len(reduced[3]) == 14
                terminal, _ = normalize(reduced)
                check_flux(image, terminal)
                algorithm_controls += 1
    forcing_edges = forcing_cases = 0
    for width in range(6, 41, 2):
        for height in range(4, 41, 2):
            forcing_edges += elbow_forcing(width, height)
            forcing_cases += 1
    for width, height in ((6, 4), (8, 6), (12, 10)):
        assert find_motif_move(elbow(width, height)) is None
    result = dict(status='PASS', initial_perfect_matchings=sum(matching_histogram.values()),
                  initial_freezing_histogram=dict(matching_histogram),
                  final_perfect_matchings=len(final_matchings), final_all_frozen=True,
                  matching_independent_completion_controls=completion_controls,
                  nonextendible_partial_matching_control=True,
                  sparse_degree_three_motif_control=True,
                  final_matching_forcing_certificate=forcing_certificate,
                  transformed_flux_controls=images, strictly_positive_flux_controls=positive_flux,
                  generic_motif_normalizer_controls=algorithm_controls,
                  irreducible_elbow_normalizer_controls=3,
                  elbow_forcing_cases=forcing_cases, forced_edges=forcing_edges,
                  square_positive_control_perfect_matchings=2,
                  retained_neighbors=retained_neighbors, charge_two_exchange=main_record,
                  scope='Exact local move and finite flux/forcing controls; general normalization, physical flux partition and all-length forcing are written proofs.')
    args.output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({key: value for key, value in result.items()
                      if key not in ('retained_neighbors', 'charge_two_exchange',
                                     'final_matching_forcing_certificate')}, indent=2))


if __name__ == '__main__':
    main()
