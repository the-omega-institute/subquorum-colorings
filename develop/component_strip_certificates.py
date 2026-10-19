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


def certify_reservation_batch(records, before, after):
    assert set(before) == set(after)
    assert all(isinstance(after[tile], int) and 0 <= after[tile] <= before[tile]
               for tile in before)
    original, slots = incidence_components(records, before)
    initial = mixed_component_allocation(records, before)
    reduced = mixed_component_allocation(records, after)
    removed = [(tile, unit) for tile, capacity in before.items()
               for unit in range(after[tile], capacity)]
    summaries = []
    for component in original:
        vertices = set(component['vertices'])
        old_degrees = Counter()
        new_degrees = Counter()
        consumed = 0
        for slot in component['slots']:
            tile, unit = slot
            old_degrees.update(slots[slot])
            if unit < after[tile]:
                new_degrees.update(slots[slot])
            else:
                consumed += 1
        old_weighted = sum(old_degrees[vertex]//2 for vertex in vertices)
        new_weighted = sum(new_degrees[vertex]//2 for vertex in vertices)
        odd_before = sum(old_degrees[vertex] % 2 for vertex in vertices)
        odd_after = sum(new_degrees[vertex] % 2 for vertex in vertices)
        children = [child for child in reduced['components'] if vertices & set(child['vertices'])]
        assert all(set(child['vertices']) <= vertices for child in children)
        rank_after = sum(child['rank'] for child in children)
        mixed_after = sum(child['credits'] for child in children)
        assert component['rank'] <= consumed+rank_after
        assert new_weighted == sum(child['weighted'] for child in children)
        assert mixed_after >= max(rank_after, new_weighted)
        assert 2*(old_weighted-new_weighted) == 2*consumed+odd_after-odd_before
        sufficient = old_weighted <= component['rank'] or odd_after <= odd_before
        weighted_branch = old_weighted > component['rank']
        signed_gain = 2*(consumed+mixed_after-max(component['rank'], old_weighted))
        parity_credit = odd_before-odd_after if weighted_branch else 0
        assert signed_gain >= parity_credit
        recovery = (mixed_after-new_weighted if weighted_branch
                    else consumed+mixed_after-component['rank'])
        assert recovery >= 0
        assert signed_gain == 2*recovery+parity_credit
        if sufficient:
            assert max(component['rank'], old_weighted) <= consumed+mixed_after
        summaries.append(dict(vertices=sorted(vertices), removed=consumed,
                              rank_before=component['rank'], rank_after=rank_after,
                              weighted_before=old_weighted, weighted_after=new_weighted,
                              weighted_branch=weighted_branch, parity_credit=parity_credit,
                              recovery_surplus=recovery,
                              odd_before=odd_before, odd_after=odd_after,
                              mixed_before=max(component['rank'], old_weighted),
                              mixed_after=mixed_after, sufficient_condition=sufficient))
    componentwise_sufficient = all(component['sufficient_condition'] for component in summaries)
    weighted_odd_before = sum(component['odd_before'] for component in summaries
                              if component['weighted_branch'])
    weighted_odd_after = sum(component['odd_after'] for component in summaries
                             if component['weighted_branch'])
    sufficient = weighted_odd_after <= weighted_odd_before
    score_change = len(removed)+reduced['credits']-initial['credits']
    recovery_surplus = sum(component['recovery_surplus'] for component in summaries)
    assert sum(component['removed'] for component in summaries) == len(removed)
    assert 2*score_change >= weighted_odd_before-weighted_odd_after
    assert 2*score_change == 2*recovery_surplus+weighted_odd_before-weighted_odd_after
    preserves_budget = weighted_odd_after <= weighted_odd_before+2*recovery_surplus
    assert preserves_budget == (score_change >= 0)
    assert not componentwise_sufficient or sufficient
    if sufficient:
        assert initial['credits'] <= len(removed)+reduced['credits']
    return dict(sufficient_condition=sufficient,
                componentwise_sufficient_condition=componentwise_sufficient,
                weighted_odd_before=weighted_odd_before, weighted_odd_after=weighted_odd_after,
                recovery_surplus=recovery_surplus, preserves_budget=preserves_budget,
                removed_units=len(removed), removed_slots=removed,
                before=initial['credits'], residual_after=reduced['credits'],
                combined_after=len(removed)+reduced['credits'],
                score_change=score_change,
                components=summaries)
