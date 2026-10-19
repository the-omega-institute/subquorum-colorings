"""Mix unit-per-run and half-capacity certificates on disjoint incidence components."""

from collections import Counter, defaultdict

from strip_incidence_allocation import incidence_components


def mixed_component_allocation(records, residual):
    components, slots = incidence_components(records, residual)
    adjacent = defaultdict(list)
    for slot, vertices in slots.items():
        for vertex in vertices:
            adjacent[vertex].append(slot)
    assignment = []
    summaries = []
    for component_index, component in enumerate(components):
        vertices = component['vertices']
        degrees = {vertex: len(adjacent[vertex]) for vertex in vertices}
        rank = component['rank']
        weighted = sum(degree//2 for degree in degrees.values())
        if weighted > rank:
            requests = [(vertex, request) for vertex in vertices
                        for request in range(degrees[vertex]//2)]
            rule = 'half_capacity'
        else:
            requested = vertices[1:] if component['tree'] else vertices
            requests = [(vertex, 0) for vertex in requested]
            rule = 'one_per_run'
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

        for request in requests:
            assert augment(request, set())
        assignment.extend(dict(component=component_index, strip=vertex, request=request,
                               tile=tile, unit=unit)
                          for (tile, unit), (vertex, request) in sorted(matched.items()))
        edges = len(component['slots'])
        odd = sum(degree % 2 for degree in degrees.values())
        loss = min(max(0, edges-len(vertices)), odd//2)
        assert odd % 2 == 0
        assert weighted == edges-odd//2
        assert max(rank, weighted) == edges-loss == len(requests)
        summaries.append(dict(vertices=vertices, slots=edges, rank=rank, weighted=weighted,
                              odd_runs=odd, credits=len(requests), unused=loss, rule=rule))
    usage = Counter((tuple(record['tile']), record['unit']) for record in assignment)
    assert all(amount == 1 for amount in usage.values())
    score = sum(component['credits'] for component in summaries)
    assert len(assignment) == score <= sum(residual.values())
    return dict(credits=score, rank=sum(component['rank'] for component in summaries),
                weighted=sum(component['weighted'] for component in summaries),
                unused=sum(component['unused'] for component in summaries),
                components=summaries, assignment=assignment)
