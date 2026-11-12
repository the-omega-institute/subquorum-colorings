"""Two complementary dissociation exchanges from one permitted witness set."""


def construct(g, selected, centres, isolates, witnesses, colours):
    active = selected-isolates
    owner = {w: next(iter(g[w] & active)) for w in witnesses}
    assert all(len(g[w] & active) == 1 and len(g[w] & isolates) <= 1 for w in witnesses)
    at_owner = {v: next(w for w in sorted(witnesses) if owner[w] == v)
                for v in active if any(owner[w] == v for w in witnesses)}
    blocks = []
    for centre in sorted(centres):
        leaves = sorted(g[centre] & selected)
        private = [ell for ell in leaves if g[at_owner[ell]] & selected == {ell}]
        if len(leaves) == 3:
            assert private and centre not in at_owner
            blocks.append(('claw', centre, leaves, None))
        else:
            assert len(leaves) == 2
            if private:
                x = private[0]
                y = next(ell for ell in leaves if ell != x)
                blocks.append(('clean', centre, [x, y], at_owner[x]))
            else:
                assert centre in at_owner
                blocks.append(('direct', centre, leaves, None))
    A = {a for kind, c, leaves, a in blocks if kind == 'clean'}
    exceptional = {a for a in A if len(g[a] & A) <= 1}
    baseline = selected-centres
    for kind, c, leaves, a in blocks:
        if kind == 'clean':
            baseline.add(c)
            baseline.remove(leaves[0])
    raw, repaired, deleted_private, deleted_helpers = [], [], [], []
    for side in (0, 1):
        D = selected-centres-set().union(*(g[c] & selected for c in centres)) if centres else set(selected)
        # D currently contains exactly the original isolates and edge components.
        for kind, c, leaves, a in blocks:
            if kind == 'clean':
                x, y = leaves
                D.update((a, c, y) if colours[c] == side else (x, c, at_owner[y]))
            elif kind == 'direct':
                D.update((*leaves, at_owner[c]) if colours[c] == side
                         else (c, *(at_owner[ell] for ell in leaves)))
            else:
                D.update(leaves if colours[c] == side else (c, *(at_owner[ell] for ell in leaves)))
        raw.append(set(D))
        other_witnesses = (D & witnesses)-A
        bad_private = {a for a in D & A if g[a] & other_witnesses}
        assert bad_private <= exceptional
        D -= bad_private
        bad_helpers = {i for i in D & isolates if len(g[i] & D & witnesses) >= 2}
        D -= bad_helpers
        repaired.append(D)
        deleted_private.append(bad_private)
        deleted_helpers.append(bad_helpers)
    assert not (deleted_private[0] & deleted_private[1])
    assert not (deleted_helpers[0] & deleted_helpers[1])
    return {'blocks': blocks, 'private': A, 'exceptional': exceptional,
            'baseline': baseline, 'baseline_plus_exceptional': baseline | exceptional,
            'raw': raw, 'repaired': repaired, 'deleted_private': deleted_private,
            'deleted_helpers': deleted_helpers}
