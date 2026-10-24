"""Physical capped, selected-guarded and same-component endpoint-guarded donors."""

import itertools

from check_component_receivers import endpoint_components, vertices_of
from check_cooperative_promotion import neighbors
from search_corner_coverage import corner_patterns, witnesses


def physical_donors(current, include_endpoint_guard=False):
    rows, columns, selected, _ = current
    components = endpoint_components(current)
    owner = {point: index for index, component in enumerate(components) for point in component}
    endpoints = set(owner)
    assigned = {}
    for witness in witnesses(rows, columns, selected, endpoints):
        tile = tuple(coordinate//2 for coordinate in witness['square'])
        required, _, _ = list(corner_patterns(*witness['square']))[witness['orientation']]
        required_owners = {owner[point] for point in required}
        assert len(required_owners) == 1
        assigned.setdefault(tile, {}).setdefault('capped', set()).update(required_owners)
    for tile in itertools.product(range(rows//2), range(columns//2)):
        cells = vertices_of({tile})
        for chosen in cells & selected:
            anchors = (set(neighbors(chosen))-cells) & endpoints
            if not anchors:
                continue
            assert len(anchors) == 1
            chosen_owner = owner[next(iter(anchors))]
            opposite = tuple(4*coordinate+1-value for coordinate, value in zip(tile, chosen))
            exterior = set(neighbors(opposite))-cells
            for guard in exterior & selected:
                if (set(neighbors(guard))-{opposite}) & endpoints:
                    assigned.setdefault(tile, {}).setdefault('guarded', set()).add(chosen_owner)
            guards = exterior & endpoints
            if include_endpoint_guard and len(guards) == 2 and all(
                    owner[point] == chosen_owner for point in guards):
                assigned.setdefault(tile, {}).setdefault('endpoint_guarded', set()).add(chosen_owner)
    records = []
    for tile, kinds in sorted(assigned.items()):
        cells = vertices_of({tile})
        assert not cells & endpoints
        deficit = 2-len(cells & selected)
        assert deficit >= 1
        if 'guarded' in kinds or 'endpoint_guarded' in kinds:
            assert deficit == 1
        owners = set.union(*kinds.values())
        assert len(owners) == 1
        records.append(dict(tile=tile, deficit=deficit, owner=next(iter(owners)),
                            capped='capped' in kinds, guarded='guarded' in kinds,
                            endpoint_guarded='endpoint_guarded' in kinds))
    return records
