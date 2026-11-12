#!/usr/bin/env python3
"""Physical certificates for cubic completion; no cubic beta optimum claimed."""
from pathlib import Path
from itertools import product,combinations
from collections import Counter
import json,sys
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'develop'),str(ROOT/'scripts')]
from cubic_completion_gap_loss import complete,base,family,FIXTURE
from compact_subcubic_selected_stars import core
from check_compact_subcubic_selected_stars import exact
if not __debug__:raise RuntimeError('Assertions must be enabled')


def formed(g,S,v):
    return len(g[v]&S)>=2 or any(g[u]&S for u in g[v]&S)


def minimal(g,S):
    if not all(formed(g,S,v) for v in range(len(g)) if v not in S):return False
    return all(any(not formed(g,S-{v},u) for u in range(len(g)) if u not in S-{v}) for v in S)


def certificate(g,S,D,col):
    assert all(v!=u and v in g[u] and col[v]!=col[u] for v in range(len(g)) for u in g[v])
    assert all(len(g[v]&D)<=1 for v in D)
    assert minimal(g,S)
    unseen=set(S);types=Counter()
    while unseen:
        comp={min(unseen)};todo=list(comp)
        while todo:
            for u in (g[todo.pop()]&S)-comp:comp.add(u);todo.append(u)
        unseen-=comp
        types[len(comp)]+=1
        if len(comp)==3:assert sorted(len(g[v]&comp) for v in comp)==[1,1,2]
        else:assert len(comp) in (1,2)
    return dict(sorted(types.items()))


def connected(g,removed=()):
    remaining=set(range(len(g)))-set(removed)
    if not remaining:return True
    seen={min(remaining)};todo=list(seen)
    while todo:
        for u in (g[todo.pop()]&remaining)-seen:seen.add(u);todo.append(u)
    return seen==remaining


def small_completions():
    counts=Counter();ex=[]
    for left,right in ((1,1),(1,2),(1,3),(2,2),(2,3),(3,3)):
        edges=list(product(range(left),range(left,left+right)));n=left+right
        col={v:int(v>=left) for v in range(n)}
        for mask in range(1<<len(edges)):
            g=[set() for _ in range(n)]
            for j,(v,u) in enumerate(edges):
                if mask>>j&1:g[v].add(u);g[u].add(v)
            counts['labelled_graph_inputs']+=1
            for bits in range(1<<n):
                S={v for v in range(n) if bits>>v&1}
                if any(len(g[v])!=3 for v in range(n) if v not in S) or not minimal(g,S):continue
                counts['eligible_minimal_selections']+=1
                h,T,c,data=complete(g,S,col)
                assert all(len(q)==3 for q in h)
                assert minimal(h,T)
                assert all(c[v]!=c[u] and v in h[u] and v!=u for v in range(len(h)) for u in h[v])
                assert all(h[v]&set(range(n))==g[v] for v in range(n))
                counts['actual_cubic_completions']+=1
                counts['new_selected_edges']+=data['selected_edge_count']
                counts['new_unused_vertices']+=len(data['new_unused'])
    # All-p controls include an imbalanced old bipartition and larger legal p.
    for left,right,edge in [(1,3,[(0,1),(0,2),(0,3)]),(2,2,[(0,2),(1,3)])]:
        n=left+right;g=[set() for _ in range(n)]
        for a,b in edge:g[a].add(b);g[b].add(a)
        # Empty old outside is enough for the degree-completion arithmetic control.
        S=set(range(n));col={v:int(v>=left) for v in range(n)}
        for p in range(10):
            try:h,T,c,data=complete(g,S,col,p)
            except ValueError:counts['invalid_p_rejections']+=1;continue
            assert all(len(q)==3 for q in h)
            assert all(c[v]!=c[u] and v in h[u] for v in range(len(h)) for u in h[v])
            counts['extra_degree_only_controls']+=1
    # Target degree2..6: selected matching components remain minimal in every completion.
    for degree in range(2,7):
        g=[{1},{0}];S={0,1};col={0:0,1:1}
        for p in range(12):
            try:h,T,c,data=complete(g,S,col,p,degree)
            except ValueError:counts['regular_invalid_p_rejections']+=1;continue
            assert all(len(q)==degree for q in h) and minimal(h,T)
            assert all(c[v]!=c[u] and v in h[u] for v in range(len(h)) for u in h[v])
            counts['degree2to6_regular_completions']+=1
    return dict(sorted(counts.items()))


def main():
    q,S,D,col=core(4)
    old_exact=[]
    for remove in (False,True):
        g=[set(x) for x in q]
        if remove:g[6].remove(30);g[30].remove(6)
        ans=exact(g);assert ans['beta']==31
        old_exact.append({'deleted_port':remove,**ans})
    h,T,E,c=base();data=json.loads(FIXTURE.read_text())
    assert sorted(map(sorted,[(v,u)for v in range(len(h))for u in h[v]if v<u]))==sorted(map(sorted,data['edges']))
    assert sorted(T)==data['selected'] and c=={int(k):v for k,v in data['colours'].items()}
    assert len(h)==68 and len(T)==36 and len(E)==38
    assert certificate(h,T,E,c)=={1:8,2:2,3:8}
    assert set(map(len,h))=={3}
    assert all(connected(h,{v}) for v in range(68))
    base_two_cuts=[list(pair) for pair in combinations(range(68),2) if not connected(h,pair)]
    rows=[]
    for k in (1,2,3,4,8,16):
        g,S,D,col=family(k,False)
        h,T,E,c=family(k,True)
        assert len(g)==48*k and len(S)==32*k and len(D)==31*k
        assert certificate(g,S,D,col)=={1:8*k,3:8*k} and connected(g)
        assert len(h)==68*k and len(T)==36*k and len(E)==38*k
        assert certificate(h,T,E,c)=={1:8*k,2:2*k,3:8*k}
        assert set(map(len,h))=={3} and connected(h)
        # Every old edge and selected vertex survives under the copywise embedding.
        embed=lambda v:68*(v//48)+v%48
        assert {embed(v) for v in S}<=T
        assert all(embed(u) in h[embed(v)] for v in range(len(g)) for u in g[v])
        if k<=4:assert all(connected(h,{v}) for v in range(len(h)))
        if k>=2:assert not connected(h,{6,30})
        rows.append({'k':k,'old_n':len(g),'old_selected':len(S),'old_exact_beta_by_theorem':31*k,
                     'new_n':len(h),'new_selected':len(T),'new_dissociation_witness':len(E),
                     'old_edges_preserved':True,'new_gap_upper':-2*k})
    controls=small_completions()
    report={'base_core_exact_controls':old_exact,'base_completed_n':68,'base_selected':36,'base_dissociation_witness':38,
            'base_completed_two_vertex_cuts':base_two_cuts,'family_controls':rows,'generic_completion_controls':controls,
            'scope':'All-k proof uses exact old-core cap and one explicit new38-set; no exact beta for a completed graph, no positive cubic selected-star gap and no universal nonexistence claim. Small controls validate minimality and degree completion only.'}
    out=ROOT/'output/cubic-completion-gap-loss-check.json';out.write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','base_core_exact_controls':old_exact,'generic_completion_controls':controls,
                      'family_models':len(rows),'base_two_vertex_cuts':len(base_two_cuts),'report_bytes':out.stat().st_size}))

if __name__=='__main__':main()
