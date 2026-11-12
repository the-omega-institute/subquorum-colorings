"""Unbudgeted primary unit matching-cost reduction from Vertex Cover.

A partial batch rounds to whole touched groups without increasing cost.
The exact fixed-list optimum is tau(H), with two-connected physical lifts
from connected bridgeless H. This is not global omission optimization.
"""
from collections import Counter
from nonisolated_exchange_frontier import endpoint
from mixed_isolated_cover_repair import bridgeless_vertex_cover_reduction


def _graph(h, edges, allow_empty=False):
    if not isinstance(h, int) or isinstance(h, bool) or h < (0 if allow_empty else 1):
        raise ValueError('Indexed graph order required')
    edges = [tuple(e) for e in edges]
    if any(len(e) != 2 for e in edges):
        raise ValueError('Two endpoints per source edge required')
    if any(not isinstance(v, int) or isinstance(v, bool) or v not in range(h) for e in edges for v in e):
        raise ValueError('Indexed source endpoints required')
    E = sorted({tuple(sorted(e)) for e in edges})
    if any(a == b for a, b in E):
        raise ValueError('Simple source graph required')
    return E


def _cover(h, edges, vertices):
    vertices = set(vertices)
    if any(not isinstance(v, int) or isinstance(v, bool) or v not in range(h) for v in vertices):
        raise ValueError('Indexed source cover required')
    if any(a not in vertices and b not in vertices for a, b in edges):
        raise ValueError('Source vertex cover required')
    return vertices


def charged_vertex_cover_template(h, edges):
    """Exact primary optimum tau(H), with NO operation-count constraint.

    h>=1, D=Delta(H)+2, q=hD, physical order10(q+h). All owner components
    are squares, initial omission is minimum, all candidates on distinct
    owners are permitted. Ambient auxiliary components are only P2/P4.
    """
    H = _graph(h, edges)
    degree = Counter(v for e in H for v in e)
    D = max(degree.values(), default=0)+2
    incidence, groups, labels, xcolour = {}, [], [], []
    for v in range(h):
        group = []
        for e in H:
            if v in e:
                incidence[v, e] = len(labels)
                group.append(len(labels))
                labels.append([v, list(e)])
                xcolour.append(int(v == e[1]))
        while len(group) < D:
            group.append(len(labels))
            labels.append([v, None])
            xcolour.append(0)
        groups.append(group)
    q = len(labels)
    colour = xcolour + [0]*(3*q)
    P, Q = [], [(incidence[a, e], incidence[b, e]) for e in H for a, b in [e]]
    successor, predecessor = [None]*q, [None]*q
    for group in groups:
        for i, j in zip(group, group[1:]+group[:1]):
            successor[i], predecessor[j] = j, i
            P.append((q+i, j))
            colour[q+i] = colour[j]
        changes = [i for i in group if colour[i] != colour[q+i]]
        assert len(changes) % 2 == 0
        split = {i: int(j >= len(changes)//2) for j, i in enumerate(changes)}
        for i in group:
            if i in split:
                colour[2*q+i], colour[3*q+i] = split[i], 1-split[i]
            else:
                colour[2*q+i] = colour[3*q+i] = 1-colour[i]
        for c in (0, 1):
            Z = sorted(2*q+i for i in group if colour[2*q+i] == c)
            W = sorted(3*q+i for i in group if colour[3*q+i] == c)
            assert len(Z) == len(W)
            P.extend(zip(Z, W))
    squares = []
    for i in range(q):
        block = [i, q+i, 2*q+i, 3*q+i]
        a = sorted(v for v in block if colour[v] == 0)
        b = sorted(v for v in block if colour[v] == 1)
        assert len(a) == len(b) == 2
        squares.append([a[0], b[0], a[1], b[1]])
    U = list(range(q))+list(range(2*q, 3*q))
    representatives = []
    for v, group in enumerate(groups):
        rep = group[-2]
        representatives.append(rep)
        assert labels[rep][1] is None and labels[successor[rep]][1] is None
        assert colour[q+rep] == 0 and colour[3*q+rep] == 1
        u, vv, p, t = range(4*q+4*v, 4*q+4*v+4)
        colour.extend([1, 1, 0, 0])
        P.extend([(u, vv), (p, t)])
        Q.extend([(q+rep, u), (3*q+rep, t)])
        squares.append([u, p, vv, t])
        U.extend([u, p])
    B = [e for K in squares for e in zip(K, K[1:]+K[:1])]
    incidences = [dict(edge=list(e), labels=[incidence[a, e], incidence[b, e]]) for e in H for a, b in [e]]
    return dict(h=h, H=[list(e) for e in H], D=D, q=q, b=2*(q+h),
                P=P, Q=Q, B=B, colour=colour, initial_U=U,
                operations=[[i, i, q+i] for i in range(q)], groups=groups,
                labels=labels, representatives=representatives,
                successor=successor, predecessor=predecessor, incidences=incidences)


def batch_ledger(data, selected):
    """Exact cost and polynomial rounding/cover decoding for ANY batch."""
    S = set(selected)
    q = data['q']
    if any(not isinstance(i, int) or isinstance(i, bool) or i not in range(q) for i in S):
        raise ValueError('Indexed candidate subset required')
    touched, group_charges = [], []
    for v, group in enumerate(data['groups']):
        rep = data['representatives'][v]
        present = bool(S.intersection(group))
        if present:
            touched.append(v)
        boundary = [i for i in group if i != data['successor'][rep]
                    and i not in S and data['predecessor'][i] in S]
        charge = int(rep in S)+len(boundary)
        assert charge >= int(present)
        group_charges.append(dict(vertex=v, representative_selected=rep in S,
                                  boundary_labels=boundary, charge=charge))
    residual = []
    for item in data['incidences']:
        i, j = item['labels']
        positions = {i, j, data['predecessor'][i], data['predecessor'][j]}
        if not S.intersection(positions):
            residual.append(item['edge'])
    Z = set(touched)
    uncovered = [e for e in data['H'] if not Z.intersection(e)]
    rounded_cost = len(Z)+len(uncovered)
    cost = sum(row['charge'] for row in group_charges)+len(residual)
    source_cover = Z | {a for a, b in uncovered}
    assert cost >= rounded_cost >= len(source_cover)
    assert all(a in source_cover or b in source_cover for a, b in data['H'])
    return dict(selected_candidates=sorted(S), cost=cost, touched_groups=touched,
                group_charges=group_charges, residual_edges=residual,
                rounded_candidates=sorted(i for v in Z for i in data['groups'][v]),
                rounded_cost=rounded_cost, source_cover=sorted(source_cover))


def batch_from_source_cover(data, cover):
    C = _cover(data['h'], data['H'], cover)
    return sorted(i for v in C for i in data['groups'][v])


def certificate_for_batch(data, selected):
    ledger = batch_ledger(data, selected)
    pairs = [(x, y) for _, x, y in data['operations']]
    cert = endpoint(2*data['b'], data['P']+data['Q'], data['initial_U'], pairs,
                    ledger['selected_candidates'])
    assert cert['actual_cost'] == ledger['cost']
    U, C = set(cert['U']), set(cert['cover'])
    cert.update(ledger=ledger, owners=sorted(set(range(2*data['b']))-U),
                witnesses=sorted(U-C), beta_I_lower=3*data['b']-cert['actual_cost'])
    return cert


def connected_primary_reduction(h, edges):
    """From arbitrary source F, optimum = tau(F)+normalization offset.

    The resulting physical graph is two-connected, min2/max3, bipartite.
    Zero-order F is allowed; the connected bridgeless source is nonempty.
    """
    H = _graph(h, edges, allow_empty=True)
    normalization = bridgeless_vertex_cover_reduction(h, H)
    template = charged_vertex_cover_template(normalization['k'], normalization['H'])
    return dict(normalization=normalization, template=template,
                additive_offset=normalization['tau_additive_constant'])


def lift_normalized_cover(normalization, source_cover):
    """F cover -> J cover, exactly offset+|cover|, constructively."""
    C = _cover(normalization['original_k'], normalization['original_edges'], source_cover)
    base = C | {normalization['apex']}
    result = set(base)
    for item in normalization['paths']:
        for u, a, b, v in item['paths']:
            assert u in base or v in base
            result.add(b if u in base and v not in base else a)
    _cover(normalization['k'], normalization['H'], result)
    assert len(result) == normalization['tau_additive_constant']+len(C)
    return sorted(result)


def project_normalized_cover(normalization, normalized_cover):
    """J cover -> F cover of size <= |Jcover|-offset, without solving VC."""
    C = _cover(normalization['k'], normalization['H'], normalized_cover)
    base = C.intersection(range(normalization['base_k']))
    for a, b in normalization['base_edges']:
        if a not in base and b not in base:
            base.add(a)
    assert len(base) <= len(C)-2*len(normalization['base_edges'])
    if normalization['apex'] not in base:
        base = set(range(normalization['original_k'])) | {normalization['apex']}
    result = base.intersection(range(normalization['original_k']))
    _cover(normalization['original_k'], normalization['original_edges'], result)
    assert len(result) <= len(C)-normalization['tau_additive_constant']
    return sorted(result)
