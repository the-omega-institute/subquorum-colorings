"""Standalone coordinate and literal checks for the median-graph obstruction."""
from collections import deque
from itertools import combinations, product
from pathlib import Path
import json


def build(copies=1):
    adj = [set() for _ in range(38*copies)]
    def edge(u, v):
        adj[u].add(v)
        adj[v].add(u)
    for k in range(copies):
        offset = 38*k
        for x, y, z in product(range(4), range(4), range(2)):
            u = offset+8*x+2*y+z
            for dx, dy, dz in ((1,0,0),(0,1,0),(0,0,1)):
                xx, yy, zz = x+dx, y+dy, z+dz
                if xx < 4 and yy < 4 and zz < 2:
                    edge(u, offset+8*xx+2*yy+zz)
        for v, leaves in ((0,(32,33)),(24,(34,35)),(6,(36,37))):
            for leaf in leaves:
                edge(offset+v, offset+leaf)
        if k:
            edge(offset-38+34, offset+32)
    return adj


def masks(adj):
    return [sum(1 << u for u in row) for row in adj]


def formed(g, selected, x):
    neighbours = g[x] & selected
    if neighbours.bit_count() >= 2:
        return True
    if not neighbours:
        return False
    y = neighbours.bit_length()-1
    return bool(g[y] & selected)


def dissociation(g, selected):
    return all(not (selected >> v & 1) or
               (row & selected).bit_count() <= 1 for v, row in enumerate(g))


def certificate(copies):
    lower = {2,4,8,10,12,14,16,18,20,22,26,28,30}
    other = {1,7,25,32,33,34,35,36,37}
    witnesses = {38*k+s:38*k+s+1 for k in range(copies) for s in lower}
    witnesses.update({38*k+s:38*k+s for k in range(copies) for s in other})
    independent_core = {8*x+2*y+z for x,y,z in product(range(4),range(4),range(2))
                        if (x+y+z)%2 == 0} - {0}
    beta_set = {38*k+v for k in range(copies)
                for v in independent_core | set(range(32,38))}
    return witnesses, beta_set


def check_median(adj):
    n = len(adj)
    distances = []
    for s in range(n):
        d = [-1]*n
        d[s] = 0
        queue = deque([s])
        while queue:
            v = queue.popleft()
            for u in adj[v]:
                if d[u] == -1:
                    d[u] = d[v]+1
                    queue.append(u)
        assert min(d) >= 0
        distances.append(d)
    intervals = [[sum(1 << v for v in range(n)
                      if distances[a][v]+distances[v][b] == distances[a][b])
                  for b in range(n)] for a in range(n)]
    count = 0
    for a,b,c in combinations(range(n),3):
        assert (intervals[a][b] & intervals[b][c] & intervals[a][c]).bit_count() == 1
        count += 1
    return count


def main():
    adj = build()
    g = masks(adj)
    assert all(v in adj[u] for u,row in enumerate(adj) for v in row)
    assert len(adj) == 38 and max(map(len,adj)) == 5
    blocks = [[8*(2*i+u)+2*(2*j+v)+w for u,v,w in product(range(2),repeat=3)]
              for i,j in product(range(2),repeat=2)]
    local_cube = [sum(1 << j for j in range(8) if (i^j).bit_count() == 1)
                  for i in range(8)]
    maximum = [s for s in range(256) if dissociation(local_cube,s) and s.bit_count()==4]
    assert max(s.bit_count() for s in range(256) if dissociation(local_cube,s)) == 4
    patterns = {}
    for kind in ('P','X','Y','Z'):
        for phase in (0,1):
            chosen = []
            for u,v,w in product(range(2),repeat=3):
                parity = {'P':u+v+w,'X':v+w,'Y':u+w,'Z':u+v}[kind] % 2
                if parity == phase:
                    chosen.append(4*u+2*v+w)
            patterns[kind,phase] = sum(1 << v for v in chosen)
    assert len(maximum) == 8 and set(maximum) == set(patterns.values())

    # Check all 8^4 possibilities forced by a putative 16-set, using only
    # the physical degree predicate; no type-compatibility table is imported.
    excluded = {0,24,6}
    avoided = compatible = 0
    for choices in product(maximum,repeat=4):
        selected = sum(1 << v for block,choice in zip(blocks,choices)
                       for j,v in enumerate(block) if choice >> j & 1)
        if any(selected >> v & 1 for v in excluded):
            continue
        avoided += 1
        compatible += dissociation(g, selected)
    assert compatible == 0
    lower_f = sum(1 << (8*x+2*y+z)
                  for x,y,z in product(range(4),range(4),range(2))
                  if (x+y+z)%2 == 0 and (x,y,z)!=(0,0,0))
    assert lower_f.bit_count() == 15 and dissociation(g,lower_f)
    assert not any(lower_f >> v & 1 for v in excluded)

    report = {'status':'PASS','cube_subsets':256,'cube_maximum_patterns':8,
              'four_block_pattern_tuples':8**4,'tuples_avoiding_D':avoided,
              'compatible_16_sets':compatible,'punctured_prism_beta':15,
              'median_triples':0,'family_instances':0,'deletion_witnesses':0,
              'exact_SF_claimed':False,'new_Lean':False}
    for r in (1,2,3,4,5,8,16,32,128,256):
        adj_r = build(r)
        gr = masks(adj_r)
        witnesses, beta_set = certificate(r)
        selected = sum(1 << s for s in witnesses)
        beta_mask = sum(1 << v for v in beta_set)
        assert len(adj_r) == 38*r and max(map(len,adj_r)) == 5
        assert len(witnesses) == 22*r and len(beta_set) == 21*r
        assert dissociation(gr,beta_mask)
        assert all(formed(gr,selected,x) for x in range(len(gr)) if not (selected >> x & 1))
        for s,x in witnesses.items():
            after = selected ^ (1 << s)
            assert not (after >> x & 1) and not formed(gr,after,x)
        for k in range(r-1):
            assert adj_r[38*k+34] == {38*k+24,38*(k+1)+32}
            assert adj_r[38*(k+1)+32] == {38*(k+1),38*k+34}
        if r <= 4:
            report['median_triples'] += check_median(adj_r)
        report['family_instances'] += 1
        report['deletion_witnesses'] += len(witnesses)

    witnesses, beta_set = certificate(1)
    certificates = {'adjacency':[sorted(row) for row in adj],
                    'forming':sorted(witnesses),'deletion_witnesses':witnesses,
                    'beta_attaining':sorted(beta_set),'deleted_centres':sorted(excluded),
                    'cube_blocks':blocks,
                    'cube_patterns':{f'{kind}{phase}':[v for v in range(8) if mask >> v & 1]
                                     for (kind,phase),mask in patterns.items()},
                    'family_bridge':'copy i vertex34 -- copy i+1 vertex32'}
    out = Path(__file__).resolve().parents[1]/'output'
    out.mkdir(exist_ok=True)
    (out/'median-obstruction-check.json').write_text(json.dumps(report,indent=2)+'\n')
    (out/'median-obstruction-certificates.json').write_text(json.dumps(certificates,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__ == '__main__':
    main()
