#!/usr/bin/env python3
"""Finite, literal-star audit of the arbitrary-width disjoint-cap argument.

The general assertion has a geometric proof in GRID_WITNESS_GEOMETRY.md.
This checker enumerates all subsets on the listed small full rectangles and
checks larger genuinely degree-four minimal sets, including protected crosses.
No third-party packages, random search claims, or imported project algorithms.
"""
from collections import Counter
from itertools import combinations
import json
from pathlib import Path
import random

if not __debug__:
    raise RuntimeError("Run with assertions enabled")


class Board:
    def __init__(self, m, n):
        self.m, self.n = m, n
        self.coords = [(r, c) for r in range(m) for c in range(n)]
        self.index = {v: i for i, v in enumerate(self.coords)}
        self.full = (1 << len(self.coords)) - 1
        self.adj = []
        self.pairs = []
        for r, c in self.coords:
            self.adj.append(sum(1 << self.index[v] for v in
                                ((r-1,c),(r+1,c),(r,c-1),(r,c+1))
                                if v in self.index))
        # Literal not-necessarily-induced K1,2 on {x,a,b}; restrict candidates
        # to distance two, then explicitly count the three possible edges.
        for x in range(len(self.coords)):
            near = self.adj[x]
            for a in bits(self.adj[x]):
                near |= self.adj[a]
            near &= ~(1 << x)
            self.pairs.append([
                (1 << a) | (1 << b) for a, b in combinations(bits(near), 2)
                if bool(self.adj[x] >> a & 1) + bool(self.adj[x] >> b & 1)
                + bool(self.adj[a] >> b & 1) >= 2])

    def literal_failures(self, s):
        return [x for x in bits(self.full ^ s)
                if not any(s & p == p for p in self.pairs[x])]

    def fast_forming(self, s):
        for x in bits(self.full ^ s):
            ns = self.adj[x] & s
            if ns.bit_count() >= 2:
                continue
            if not ns:
                return False
            u = ns.bit_length() - 1
            if not self.adj[u] & s:
                return False
        return True

    def minimal(self, s):
        return not self.literal_failures(s) and all(
            self.literal_failures(s ^ (1 << v)) for v in bits(s))

    def greedy(self, s, protected, rng):
        assert self.fast_forming(s)
        order = list(bits(s & ~protected))
        rng.shuffle(order)
        for v in order:
            t = s ^ (1 << v)
            if self.fast_forming(t):
                s = t
        assert self.minimal(s)
        return s

    def audit(self, s, totals):
        assert self.minimal(s)
        totals['minimal_sets'] += 1
        deg = {v: (self.adj[v] & s).bit_count() for v in bits(s)}
        active = sum(1 << v for v in deg if deg[v])
        z = {v for v in deg if deg[v] == 0 or
             (deg[v] == 1 and deg[next(bits(self.adj[v] & s))] == 1)}
        witnesses = {v: self.literal_failures(s ^ (1 << v)) for v in deg}
        direct = {v: [x for x in witnesses[v]
                      if not s >> x & 1 and self.adj[v] >> x & 1] for v in deg}
        e = {v for v in deg if deg[v] in (2, 3) and not direct[v]}
        h = {v for v in deg if deg[v] == 4}
        owners = set(deg) - z - e - h
        allocated = set()
        for v in owners:
            assert direct[v]
            for x in direct[v]:
                assert self.adj[x] & active == 1 << v
                other = self.adj[x] & s & ~(1 << v)
                assert other.bit_count() <= 1
                assert all(deg[u] == 0 for u in bits(other))
            x = direct[v][0]
            assert x not in allocated
            allocated.add(x)
        cap_options = {}
        all_caps = set()
        for v in h:
            vr, vc = self.coords[v]
            clean = [(u, x) for u in bits(self.adj[v] & s) if deg[u] == 1
                     for x in witnesses[v] if not s >> x & 1 and
                     self.adj[x] & s == 1 << u]
            assert clean
            options = []
            for u, x in clean:
                ur, uc = self.coords[u]
                er, ec = ur-vr, uc-vc
                assert self.coords[x] == (vr+2*er, vc+2*ec)
                caps = {self.index[(ur-ec, uc+er)],
                        self.index[(ur+ec, uc-er)]}
                assert len(caps) == 2
                for y in caps:
                    assert not s >> y & 1
                    assert (self.adj[y] & active).bit_count() >= 2
                assert not caps & allocated
                options.append(caps)
            cap_options[v] = options
            # Distinct choices at a single centre need not be disjoint.
            offered = set.union(*options)
            assert not offered & all_caps
            all_caps |= offered
        for v, w in combinations(h, 2):
            vr, vc = self.coords[v]
            wr, wc = self.coords[w]
            assert not ((vr == wr and abs(vc-wc) == 2) or
                        (vc == wc and abs(vr-wr) == 2))
            for a in cap_options[v]:
                for b in cap_options[w]:
                    assert not a & b
        # Extend the resources to exceptional degree-two/three centres.
        # A clean witness can be bent here; a selected perpendicular sibling
        # still provides an omitted cap on that side of the chosen leaf.
        chosen = {}
        exceptional_offers = {}
        exceptional_owners = {}
        for v in e | h:
            vr, vc = self.coords[v]
            options = []
            for u in bits(self.adj[v] & s):
                if deg[u] != 1:
                    continue
                ur, uc = self.coords[u]
                er, ec = ur-vr, uc-vc
                caps = set()
                for fr, fc in [(-ec, er), (ec, -er)]:
                    sibling = (vr+fr, vc+fc)
                    if sibling in self.index and s >> self.index[sibling] & 1:
                        caps.add(self.index[(ur+fr, uc+fc)])
                for x in witnesses[v]:
                    if not s >> x & 1 and self.adj[x] & s == 1 << u:
                        options.append((u, x, caps))
            assert options
            chosen[v] = max(options, key=lambda t: len(t[2]))
            if v in e:
                offers = set.union(*(t[2] for t in options))
                exceptional_offers[v] = offers
                assert not offers & all_caps
                for y in offers:
                    exceptional_owners.setdefault(y, set()).add(v)
                    assert not s >> y & 1
                    assert (self.adj[y] & active).bit_count() >= 2
                expected = 1 if deg[v] == 3 else 0
                if deg[v] == 2:
                    us = [self.coords[u] for u in bits(self.adj[v] & s)]
                    expected = int(us[0][0] != us[1][0] and us[0][1] != us[1][1])
                assert len(chosen[v][2]) >= expected
        assert all(len(owners_at_cap) <= 2 for owners_at_cap in exceptional_owners.values())
        leaves = {t[0] for t in chosen.values()}
        assert len(leaves) == len(e | h) and not leaves & (e | h | z)
        reserved = set()
        for v in set(deg) - z - e - h - leaves:
            assert direct[v]
            x = direct[v][0]
            assert x not in reserved
            reserved.add(x)
        for u, x, caps in chosen.values():
            assert x not in reserved
            reserved.add(x)
        assert len(reserved) == s.bit_count()-len(z)-len(e)-len(h)
        selected_h_caps = set().union(*(chosen[v][2] for v in h))
        selected_e_caps = set().union(*(chosen[v][2] for v in e))
        assert len(selected_h_caps) == 2*len(h)
        assert not selected_h_caps & selected_e_caps
        assert not reserved & (selected_h_caps | selected_e_caps)
        k = sum(len(chosen[v][2]) for v in e)
        assert len(selected_e_caps) >= (k+1)//2
        rhs = s.bit_count() - len(z) - len(e) + len(h)
        assert (self.full ^ s).bit_count() >= rhs
        assert (self.full ^ s).bit_count() >= rhs + len(selected_e_caps)
        totals['exceptional_cap_incidences'] += k
        totals['exceptional_caps_reserved'] += len(selected_e_caps)
        totals['exceptional_caps_with_two_possible_owners'] += sum(
            len(owners_at_cap) == 2 for owners_at_cap in exceptional_owners.values())
        totals['degree_four_centres'] += len(h)
        totals['clean_leaf_choices'] += sum(map(len, cap_options.values()))
        totals['degree_four_pairs'] += len(h) * (len(h)-1) // 2
        totals['exceptional_degree_two_three'] += len(e)
        totals['direct_resource_owners'] += len(owners)
        if not z and not e:
            totals['no_exception_sets'] += 1
            assert 2*s.bit_count() <= len(self.coords)-len(h)
        return {'shape': [self.m, self.n], 'selected_size': s.bit_count(),
                'selected': [self.coords[v] for v in bits(s)],
                'Z': len(z), 'E': len(e), 'H': len(h),
                'omitted': (self.full ^ s).bit_count(),
                'required_omitted': rhs,
                'exceptional_cap_incidences': k,
                'strong_required_omitted': rhs + len(selected_e_caps),
                'all_offered_caps': [self.coords[v] for v in sorted(all_caps)]}


def bits(mask):
    while mask:
        b = mask & -mask
        yield b.bit_length()-1
        mask ^= b


def main():
    totals = Counter()
    shapes = [(m, n) for m in range(1, 5) for n in range(m, 9)
              if m*n <= 16]
    exhaustive = []
    for m, n in shapes:
        board = Board(m, n)
        before = totals['minimal_sets']
        for s in range(board.full+1):
            literal = not board.literal_failures(s)
            assert literal == board.fast_forming(s)
            totals['subset_predicate_comparisons'] += 1
            if literal and all(board.literal_failures(s ^ (1 << v))
                               for v in bits(s)):
                board.audit(s, totals)
        exhaustive.append({'shape': [m, n], 'all_subsets': board.full+1,
                           'minimal_sets': totals['minimal_sets']-before})
    rng = random.Random(20261112)
    seeded = []
    for m, n in [(5,5),(6,6),(7,7),(7,15),(8,9),(9,11)]:
        board = Board(m, n)
        for _ in range(16):
            s = board.greedy(board.full, 0, rng)
            seeded.append(board.audit(s, totals))
    protected = []
    for m, n, centres in [(7,7,[(3,3)]), (7,15,[(3,3),(3,11)]),
                           (15,15,[(3,3),(3,11),(11,3),(11,11)])]:
        board = Board(m, n)
        cross = shell = 0
        for i, (r,c) in enumerate(board.coords):
            ds = [abs(r-a)+abs(c-b) for a,b in centres]
            if any(d <= 1 for d in ds):
                cross |= 1 << i
            if any(d in (2,3) for d in ds):
                shell |= 1 << i
        assert not cross & shell
        for _ in range(4):
            s = board.greedy(board.full & ~shell, cross, rng)
            assert all((board.adj[board.index[c]] & s).bit_count() == 4
                       for c in centres)
            rec = board.audit(s, totals)
            rec['protected_centres'] = centres
            protected.append(rec)
    assert totals['degree_four_centres'] >= 28
    assert totals['degree_four_pairs'] > 0
    assert totals['exceptional_degree_two_three'] > 0
    assert totals['exceptional_cap_incidences'] > 0
    report = {'status': 'PASS', 'totals': dict(sorted(totals.items())),
              'exhaustive_rectangles': exhaustive,
              'seeded_minimal_sets': len(seeded),
              'protected_cross_fixtures': protected,
              'scope': 'Finite audit; all-width assertion uses geometric proof. '
                       'Checks all clean-leaf choices, not a favorable choice.'}
    target = Path(__file__).resolve().parents[1]/'output/grid-disjoint-caps-check.json'
    target.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({'status': 'PASS', 'totals': report['totals'],
                      'protected_fixtures': len(protected)}, sort_keys=True))


if __name__ == '__main__':
    main()
