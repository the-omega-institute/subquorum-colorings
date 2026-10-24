"""Maximal endpoint-free strips, residual physical capacities and unit allocation."""

import itertools

from check_component_receivers import endpoint_components, vertices_of


def maximal_strips(current, reserved=None, sealed_only=False):
    rows, columns, selected, _ = current
    reserved = {} if reserved is None else reserved
    components = endpoint_components(current)
    endpoint_owner = {point: index for index, component in enumerate(components) for point in component}
    endpoints = set(endpoint_owner)
    tile_owner = {}
    for point in endpoints:
        tile = tuple(coordinate//2 for coordinate in point)
        assert tile not in tile_owner or tile_owner[tile] == endpoint_owner[point]
        tile_owner[tile] = endpoint_owner[point]
    tiles = set(itertools.product(range(rows//2), range(columns//2)))
    empty_tiles = tiles-set(tile_owner)
    deficits = {tile: 2-len(vertices_of({tile}) & selected) for tile in empty_tiles}
    assert all(deficit >= 0 for deficit in deficits.values())
    assert set(reserved) <= empty_tiles
    assert all(isinstance(amount, int) and 0 <= amount <= deficits[tile]
               for tile, amount in reserved.items())
    residual = {tile: deficit-reserved.get(tile, 0) for tile, deficit in deficits.items()}
    records = []
    for orientation in ('horizontal', 'vertical'):
        horizontal = orientation == 'horizontal'
        bands, length = (rows//2, columns//2) if horizontal else (columns//2, rows//2)
        for band in range(bands):
            position = 0
            while position < length:
                tile_at = lambda offset: (band, offset) if horizontal else (offset, band)
                if tile_at(position) in tile_owner:
                    position += 1
                    continue
                start = position
                while position < length and tile_at(position) not in tile_owner:
                    position += 1
                stop = position
                strip = [tile_at(offset) for offset in range(start, stop)]
                if horizontal:
                    boundary = {(2*band+local, column) for local in (0, 1)
                                for column in (2*start, 2*stop-1)}
                else:
                    boundary = {(row, 2*band+local) for local in (0, 1)
                                for row in (2*start, 2*stop-1)}
                sealed = not boundary & (selected | endpoints)
                if sealed_only and not sealed:
                    continue
                capacity = sum(deficits[tile] for tile in strip)
                if sealed:
                    assert capacity >= 2
                left_owner = tile_owner.get(tile_at(start-1)) if start > 0 else None
                right_owner = tile_owner.get(tile_at(stop)) if stop < length else None
                owner = left_owner if left_owner is not None and left_owner == right_owner else None
                records.append(dict(orientation=orientation, tiles=strip, length=len(strip),
                                    sealed=sealed, selected_boundary=len(boundary & selected),
                                    capacity=capacity, residual_capacity=sum(residual[tile] for tile in strip),
                                    boundary_owners=[left_owner, right_owner], owner=owner))
    return records, deficits, residual


def sealed_strips(current, reserved=None):
    return maximal_strips(current, reserved, sealed_only=True)


def allocate_units(records, residual):
    eligible = [record for record in records if record['residual_capacity'] >= 2]
    neighbors = [[(tile, unit) for tile in record['tiles'] for unit in range(residual[tile])]
                 for record in eligible]
    matched = {}

    def augment(index, visited):
        for slot in neighbors[index]:
            if slot in visited:
                continue
            visited.add(slot)
            if slot not in matched or augment(matched[slot], visited):
                matched[slot] = index
                return True
        return False

    for index in range(len(eligible)):
        assert augment(index, set())
    assignments = [dict(strip=index, tile=tile, unit=unit)
                   for (tile, unit), index in sorted(matched.items())]
    assert len(assignments) == len(eligible)
    assert {record['strip'] for record in assignments} == set(range(len(eligible)))
    assert all(record['tile'] in eligible[record['strip']]['tiles'] for record in assignments)
    return eligible, assignments
