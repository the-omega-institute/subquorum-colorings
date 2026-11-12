"""Exact small-cost decisions by covering exceptions then solving 2-SAT.

Fixed distinct replacements only. XP in cost bound, not an FPT claim.
The zero-cost test works on any simple graph; positive-cost equivalence
uses bipartite matching/vertex-cover duality. The public solver validates
the current bipartite maximum-degree2 auxiliary domain.
"""
from itertools import combinations
from nonisolated_exchange_frontier import validate, endpoint
from owner_matching_certificate import sat


def _zero_after_cover(data, covered):
    clauses, sources = [], []
    for a, b in data['edges']:
        if a in covered or b in covered:
            continue
        requirements, impossible = [], False
        for v in (a, b):
            if v in data['vertex_op']:
                i, role = data['vertex_op'][v]
                requirements.append((i, role))
            elif v not in data['U']:
                impossible = True
                break
        if impossible:
            continue
        requirements = sorted(set(requirements))
        if any((i, 1-phase) in requirements for i, phase in requirements):
            continue
        clauses.append(requirements)
        sources.append([a, b])
    values, obstruction = sat(len(data['operations']), clauses)
    return dict(values=values, obstruction=obstruction, clauses=clauses,
                clause_edges=sources)


def primary_cost_at_most(n, edges, U, operations, bound):
    """Decide exact unit matching cost<=bound, returning an actual batch.

    Enumerates all subsets Z of the ambient vertices of size<=bound.
    Exponential in bound in the exponent of n (XP), not FPT or a budget
    on selected operations. Any returned cover is intersected with U_S.
    """
    if not isinstance(bound, int) or isinstance(bound, bool) or bound < 0:
        raise ValueError('Nonnegative integer primary-cost bound required')
    data = validate(n, edges, U, operations)
    tested, first_failure = 0, None
    for size in range(min(bound, n)+1):
        for covered in combinations(range(n), size):
            result = _zero_after_cover(data, set(covered))
            tested += 1
            if result['values'] is None:
                if first_failure is None:
                    first_failure = dict(covered=list(covered), **result)
                continue
            selected = [i for i, s in enumerate(result['values']) if s]
            cert = endpoint(n, data['edges'], data['U'], data['operations'], selected)
            final_cover = set(covered) & set(cert['U'])
            assert all(a in final_cover or b in final_cover
                       for a, b in data['edges'] if a in cert['U'] and b in cert['U'])
            assert cert['actual_cost'] <= len(final_cover) <= bound
            return dict(feasible=True, bound=bound, tested_covers=tested,
                        chosen_exception_vertices=list(covered),
                        final_exception_cover=sorted(final_cover),
                        certificate=cert, first_zero_obstruction=first_failure)
    return dict(feasible=False, bound=bound, tested_covers=tested,
                first_zero_obstruction=first_failure)
