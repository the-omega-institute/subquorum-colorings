"""Physical cyclic completions and exact certificate transfer.

Two complemented copies make Q perfect; four copies can also make the owner
graph 2-regular. These reduce the universal target; they do not prove it.
"""
from owner_matching_certificate import prepare, components
from all_helper_optimization import score


def _edge(a, b):
    return min(a, b), max(a, b)


def cyclic_completion(b, P, Q, B, colour, close_owners=False):
    """Preserve each original copy; return a valid physical comparison template."""
    data = prepare(b, P, Q, B, colour)
    n = 2*b
    copies = 4 if close_owners else 2
    PP = [_edge(a+n*j, c+n*j) for j in range(copies) for a, c in data['P']]
    QQ = [_edge(a+n*j, c+n*j) for j in range(copies) for a, c in data['Q']]
    BB = [_edge(a+n*j, c+n*j) for j in range(copies) for a, c in data['B']]
    col = [c ^ (j % 2) for j in range(copies) for c in colour]
    added_Q = []
    for K, cyclic in components(n, data['P']+data['Q']):
        if cyclic:
            assert len(K) % 4 == 0
            continue
        assert len(K) % 2 == 0 and len(K) >= 2
        a, c = K[0], K[-1]
        if len(K) % 4 == 0:
            added_Q.extend(_edge(a+n*j, c+n*j) for j in range(copies))
        else:
            for j in range(0, copies, 2):
                added_Q.extend((_edge(a+n*j, a+n*(j+1)),
                                _edge(c+n*j, c+n*(j+1))))
    added_B = []
    if close_owners:
        for K, cyclic in data['owner_components']:
            if cyclic:
                continue
            if len(K) == 1:
                v = K[0]
                added_B.extend(_edge(v+n*j, v+n*((j+1) % 4)) for j in range(4))
            else:
                for j in (0, 2):
                    added_B.extend((_edge(K[0]+n*j, K[0]+n*(j+1)),
                                    _edge(K[-1]+n*j, K[-1]+n*(j+1))))
    assert not set(added_Q) & set(QQ) and len(set(added_Q)) == len(added_Q)
    assert not set(added_B) & set(BB) and len(set(added_B)) == len(added_B)
    QQ = sorted(QQ+added_Q)
    BB = sorted(BB+added_B)
    result = dict(b=copies*b, P=sorted(PP), Q=QQ, B=BB, colour=col,
                  copies=copies, original_order=n, added_Q=sorted(added_Q),
                  added_B=sorted(added_B), close_owners=close_owners)
    prepare(result['b'], result['P'], QQ, BB, col)
    assert len(QQ) == copies*b
    assert all(c and len(K) % 4 == 0 for K, c in components(copies*n, PP+QQ))
    if close_owners:
        assert all(c and len(K) % 2 == 0 for K, c in components(copies*n, BB))
    return result


def transfer_certificate(b, P, Q, B, colour, completed_U, close_owners=False,
                         require_target=True):
    """Transfer any permitted completed omission to its cheapest original copy.

    By default require that the completed omission meets its universal target.
    With require_target=False the exact transfer inequality is still certified.
    """
    rec = cyclic_completion(b, P, Q, B, colour, close_owners)
    n = 2*b
    copies = rec['copies']
    Uhat = set(completed_U)
    if any(not isinstance(v, int) or isinstance(v, bool) or v not in range(copies*n) for v in Uhat):
        raise ValueError('Invalid completed omission index')
    Shat = set(range(copies*n))-Uhat
    if any(sum(v in e and set(e) <= Shat for e in rec['B']) > 1 for v in Shat):
        raise ValueError('Completed omission must be owner-permitted')
    _, Mhat = score(copies*n, rec['P'], rec['Q'], Uhat)
    completed_cost = len(Mhat)
    completed_bound = copies*n//6
    if require_target and completed_cost > completed_bound:
        raise ValueError('Completed certificate does not meet its target')
    choices = []
    for j in range(copies):
        U = {v for v in range(n) if v+n*j in Uhat}
        T, M = score(n, P, Q, U)
        S = set(range(n))-U
        assert all(sum(v in e and set(e) <= S for e in B) <= 1 for v in S)
        choices.append(dict(copy=j, U=sorted(U), owners=sorted(S), witnesses=sorted(T),
                            matching=[list(e) for e in M], cost=len(M),
                            beta_I_lower=3*b-len(M)))
    assert sum(x['cost'] for x in choices) <= completed_cost
    best = min(choices, key=lambda x:(x['cost'], x['copy']))
    assert best['cost'] <= completed_cost//copies
    if completed_cost <= completed_bound:
        assert best['cost'] <= n//6
    return dict(**best, all_copies=choices, completed_cost=completed_cost,
                completed_bound=completed_bound, completed_matching=[list(e) for e in Mhat],
                cost_bound=n//6, meets_target=best['cost'] <= n//6,
                sum_original_costs=sum(x['cost'] for x in choices), completion=rec)
