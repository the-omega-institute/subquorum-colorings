"""Exact unit-per-run allocation in the physical strip incidence multigraph."""

from collections import defaultdict


def incidence_components(records, residual):
    memberships = defaultdict(list)
    for index, record in enumerate(records):
        for tile in record['tiles']:
            memberships[tile].append(index)
    slots = {}
    adjacent = defaultdict(list)
    for tile, capacity in residual.items():
        assert isinstance(capacity, int) and capacity >= 0
        assert len(memberships[tile]) == 2
        first, second = memberships[tile]
        assert records[first]['orientation'] != records[second]['orientation']
        for unit in range(capacity):
            slot = (tile, unit)
            slots[slot] = (first, second)
            adjacent[first].append(slot)
            adjacent[second].append(slot)
    remaining = set(adjacent)
    components = []
    while remaining:
        root = min(remaining)
        vertices = {root}
        edges = set()
        pending = [root]
        while pending:
            vertex = pending.pop()
            for slot in adjacent[vertex]:
                edges.add(slot)
                for other in slots[slot]:
                    if other not in vertices:
                        vertices.add(other)
                        pending.append(other)
        remaining.difference_update(vertices)
        assert len(edges) >= len(vertices)-1
        components.append(dict(vertices=sorted(vertices), slots=sorted(edges),
                               tree=len(edges) == len(vertices)-1,
                               rank=min(len(edges), len(vertices))))
    return components, slots


def allocate_requested(records, residual, requested):
    requested = set(requested)
    assert requested <= set(range(len(records)))
    components, slots = incidence_components(records, residual)
    active = {vertex for component in components for vertex in component['vertices']}
    obstruction = requested-active
    if obstruction:
        return dict(feasible=False, reason='zero_capacity_run', vertices=sorted(obstruction))
    for component in components:
        vertices = set(component['vertices'])
        if component['tree'] and vertices <= requested:
            return dict(feasible=False, reason='entire_tree_requested',
                        vertices=sorted(vertices), slots=component['slots'])
    adjacent = defaultdict(list)
    for slot, vertices in slots.items():
        for vertex in vertices:
            adjacent[vertex].append(slot)
    matched = {}

    def augment(vertex, visited):
        for slot in sorted(adjacent[vertex]):
            if slot in visited:
                continue
            visited.add(slot)
            if slot not in matched or augment(matched[slot], visited):
                matched[slot] = vertex
                return True
        return False

    for vertex in sorted(requested):
        assert augment(vertex, set())
    assignment = [dict(strip=vertex, tile=tile, unit=unit)
                  for (tile, unit), vertex in sorted(matched.items())]
    assert len(assignment) == len(requested)
    return dict(feasible=True, assignment=assignment)


def maximum_run_allocation(records, residual):
    components, _ = incidence_components(records, residual)
    requested = set()
    for component in components:
        vertices = component['vertices']
        requested.update(vertices[1:] if component['tree'] else vertices)
    allocation = allocate_requested(records, residual, requested)
    assert allocation['feasible']
    rank = sum(component['rank'] for component in components)
    assert len(allocation['assignment']) == rank
    return dict(rank=rank, components=components, **allocation)
