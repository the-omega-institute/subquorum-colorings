"""Two distinct protected donor tiles for each positive two-leg module."""

from check_component_receivers import vertices_of
from check_cooperative_promotion import neighbors, occupied_degrees
from check_degree_three_fusion import inspect as inspect_single_guard


def paired_guards(module):
    chosen, anchor, opposite, guard = module['guard']
    inward = tuple(first-second for first, second in zip(chosen, anchor))
    assert sum(abs(coordinate) for coordinate in inward) == 1
    projection = lambda point: sum(coordinate*direction for coordinate, direction in zip(point, inward))
    center_sum = min(map(projection, module['endpoints']))+max(map(projection, module['endpoints']))
    reflect = lambda point: tuple(coordinate+(center_sum-2*projection(point))*direction
                                  for coordinate, direction in zip(point, inward))
    return (chosen, anchor, opposite, guard), tuple(reflect(point) for point in module['guard'])


def inspect(current, modules, require_frozen=True):
    original = inspect_single_guard(current, modules, require_frozen=require_frozen, allow_degree_four=True)
    degrees = occupied_degrees(current)
    chosen_tiles = []
    marked_witnesses = []
    positive = 0
    marked_sides = 0
    for module in modules:
        if module['charge'] <= 0:
            continue
        positive += 1
        all_protectors = set()
        module_tiles = set()
        for chosen, anchor, opposite, guard in paired_guards(module):
            protectors = (set(neighbors(anchor)) & module['endpoints']) | {guard}
            assert len(protectors) == 3 and not all_protectors & protectors
            all_protectors |= protectors
            tile = tuple(coordinate//2 for coordinate in chosen)
            assert tile not in module_tiles
            module_tiles.add(tile)
            cells = vertices_of({tile})
            assert not cells & module['endpoints'] and cells & module['selected'] == {chosen}
            old_occupied = module['endpoints'] | module['selected']
            for endpoint in protectors:
                missing = set(neighbors(endpoint))-old_occupied
                assert len(missing) == 1
                assert tuple(coordinate//2 for coordinate in endpoint) != tuple(
                    coordinate//2 for coordinate in next(iter(missing)))
            affected = sorted(endpoint for endpoint in protectors if degrees[endpoint] == 4)
            if affected:
                marked_sides += 1
                marked_witnesses.append(affected[0])
                continue
            assert chosen in current[2]
            assert not cells & {point for original_module in modules for point in original_module['endpoints']}
            assert cells & current[2] == {chosen}
            chosen_tiles.append(tile)
    assert positive == sum(module['charge'] > 0 for module in modules)
    assert len(chosen_tiles) == 2*positive-marked_sides
    assert len(set(chosen_tiles)) == len(chosen_tiles)
    assert len(set(marked_witnesses)) == marked_sides
    internal_events = set()
    all_endpoints = {point for module in modules for point in module['endpoints']}
    for module in modules:
        for endpoint in module['endpoints']:
            for other in (set(neighbors(endpoint)) & all_endpoints)-module['endpoints']-module['selected']:
                if tuple(coordinate//2 for coordinate in endpoint) == tuple(coordinate//2 for coordinate in other):
                    internal_events.add(endpoint)
    assert len(internal_events) == original['intratile_degree_four_defect']
    assert not internal_events & set(marked_witnesses)
    assert original['intratile_degree_four_defect']+marked_sides <= original['degree_four_endpoints']
    assert marked_sides <= positive+original['marked_positive_modules']
    credit = (positive+original['negative_module_mass']+2*original['new_aligned_faces']-
              original['intratile_degree_four_defect']-marked_sides)
    coarse_credit = (positive+original['negative_module_mass']+2*original['new_aligned_faces']-
                     original['degree_four_endpoints'])
    assert credit >= original['certified_slack_lower_bound']
    assert original['half_area']-original['objective'] >= credit >= coarse_credit
    return dict(**original, positive_modules=positive, marked_sides=marked_sides,
                two_guard_unit_donors=len(chosen_tiles), two_guard_credit=credit,
                two_guard_coarse_credit=coarse_credit,
                improvement=credit-original['certified_slack_lower_bound'])
