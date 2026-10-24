"""Capacitated strip incidence matching with an attaining internal-edge cut."""

from collections import Counter, defaultdict

from strip_incidence_allocation import incidence_components


def local_quota_allocation(records, residual):
    components, slots = incidence_components(records, residual)
    adjacent = defaultdict(list)
    for slot, vertices in slots.items():
        for vertex in vertices:
            adjacent[vertex].append(slot)
    degrees = {vertex: len(incident) for vertex, incident in adjacent.items()}
    quotas = {vertex: max(1, degree//2) for vertex, degree in degrees.items()}
    matched = {}

    def augment(request, visited):
        vertex, _ = request
        for slot in sorted(adjacent[vertex]):
            if slot in visited:
                continue
            visited.add(slot)
            if slot not in matched or augment(matched[slot], visited):
                matched[slot] = request
                return True
        return False

    for vertex in sorted(quotas):
        for copy in range(quotas[vertex]):
            augment((vertex, copy), set())
    allocation = [dict(strip=vertex, request=copy, tile=tile, unit=unit)
                  for (tile, unit), (vertex, copy) in sorted(matched.items())]
    assigned = Counter(request[0] for request in matched.values())
    slots_by_owner = defaultdict(list)
    for slot, (vertex, _) in matched.items():
        slots_by_owner[vertex].append(slot)
    unmatched = set(slots)-set(matched)
    reached_slots = set(unmatched)
    reached_vertices = set()
    pending = list(unmatched)
    while pending:
        slot = pending.pop()
        for vertex in slots[slot]:
            if vertex in reached_vertices:
                continue
            reached_vertices.add(vertex)
            assert assigned[vertex] == quotas[vertex]
            for other in slots_by_owner[vertex]:
                if other not in reached_slots:
                    reached_slots.add(other)
                    pending.append(other)
    internal = {slot for slot, vertices in slots.items()
                if set(vertices) <= reached_vertices}
    boundary = {slot for slot, vertices in slots.items()
                if len(set(vertices) & reached_vertices) == 1}
    odd_nonleaves = sum(degrees[vertex] >= 3 and degrees[vertex] % 2 == 1
                        for vertex in reached_vertices)
    leaves = sum(degrees[vertex] == 1 for vertex in reached_vertices)
    loss = len(unmatched)
    assert internal == reached_slots
    assert len(internal)-sum(quotas[vertex] for vertex in reached_vertices) == loss
    assert 2*loss == odd_nonleaves-leaves-len(boundary)
    assert len(allocation) == len(slots)-loss
    assert len({(tuple(record['tile']), record['unit']) for record in allocation}) == len(allocation)
    assert len({(record['strip'], record['request']) for record in allocation}) == len(allocation)
    assert all(assigned[vertex] <= quotas[vertex] for vertex in quotas)
    return dict(credits=len(allocation), capacity=len(slots), unused=loss,
                degrees=sorted(degrees.items()), quotas=sorted(quotas.items()),
                assignment=allocation, components=len(components),
                attaining_cut=dict(vertices=sorted(reached_vertices),
                                   internal_slots=sorted(internal), boundary_slots=sorted(boundary),
                                   odd_nonleaves=odd_nonleaves, leaves=leaves,
                                   quota=sum(quotas[vertex] for vertex in reached_vertices),
                                   deficiency=loss))
