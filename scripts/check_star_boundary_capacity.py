#!/usr/bin/env python3
"""Literal non-induced stars versus boundary capacity and ambient witnesses."""
from collections import Counter
from functools import lru_cache
from itertools import combinations
from pathlib import Path
import argparse,hashlib,json,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'develop'))
from star_boundary_capacity import (forms,admissible,signature,safe_internal_deletion,
    saturate_ports,saturate_bipartite_ports,protected_witnesses,loss_obstruction,activity_counterexample,sharp_extension_order)
if not __debug__:raise RuntimeError('assertions required')
counts=Counter();digest=hashlib.sha256()


def sets(n):
    return [{v for v in range(n) if mask>>v&1} for mask in range(1<<n)]


def graphs(n):
    edges=list(combinations(range(n),2))
    for mask in range(1<<len(edges)):
        adj=[set() for _ in range(n)]
        for j,(a,b) in enumerate(edges):
            if mask>>j&1:adj[a].add(b);adj[b].add(a)
        yield adj


def literal_engine(adj,k):
    """Enumerate actual (centre, k distinct leaves) stars, without degree test."""
    n=len(adj);required=[set() for _ in range(n)]
    for centre in range(n):
        for leaves in combinations(sorted(adj[centre]),k):
            star={centre,*leaves}
            for x in star:required[x].add(sum(1<<v for v in star-{x}))
    @lru_cache(None)
    def form_mask(mask):
        return all(mask>>x&1 or any(mask&need==need for need in required[x]) for x in range(n))
    def form(S):return form_mask(sum(1<<v for v in S))
    return form,form_mask


def literal_protected(adj,P,C,v,k):
    Cv=C-{v};out=[]
    # A witness is uncovered even if every selected port has unlimited activity.
    # Test it with stars after adding k shared selected neighbours of all ports,
    # identify the uncovered ORIGINAL nonport vertices individually.
    g,S,_=saturate_ports(adj,P,C,k);S.remove(v)
    for x in set(range(len(adj)))-(Cv|P):
        star_found=False
        for centre in range(len(g)):
            for leaves in combinations(sorted(g[centre]),k):
                Z={centre,*leaves}
                if x in Z and Z-{x}<=S:star_found=True;break
            if star_found:break
        if not star_found:out.append(x)
    return sorted(out)


def bipartition(adj):
    col={}
    for root in range(len(adj)):
        if root in col:continue
        col[root]=0;todo=[root]
        for a in todo:
            for b in adj[a]:
                if b not in col:col[b]=1-col[a];todo.append(b)
                if col[a]==col[b]:return None
    return [col[v] for v in range(len(adj))]


# Complete simple block graphs through4 vertices, every port/selection,
# k=1,...,5. The canonical exterior has at most k shared selected vertices.
for n in range(5):
    subsets=sets(n)
    for adj in graphs(n):
        col=bipartition(adj)
        for k in range(1,6):
            block_literal,_=literal_engine(adj,k)
            for C in subsets:
                assert forms(adj,C,k)==block_literal(C)
                counts['literal_block_formation_comparisons']+=1
            for P in subsets:
                g,external,_=saturate_ports(adj,P,set(),k);sat_literal,_=literal_engine(g,k)
                assert len(g)-n==(k if P else 0)
                if n<=3 and col is not None:
                    bg,be,br=saturate_bipartite_ports(adj,P,set(),k,col);bf,_=literal_engine(bg,k)
                    assert len(bg)-n<=2*k and all(br['colour'][a]!=br['colour'][b] for a in range(len(bg)) for b in bg[a])
                for C in subsets:
                    S=C|external;A=admissible(adj,P,C,k)
                    assert A==sat_literal(S)
                    counts['exact_ambient_admissibility_controls']+=1
                    if n<=3 and col is not None:
                        assert bf(C|be)==A;counts['bipartite_admissibility_controls']+=1
                    if A:
                        for v in C:
                            witness=protected_witnesses(adj,P,C,v,k)
                            assert bool(witness)==(not sat_literal(S-{v}))
                            if n<=3 and col is not None:
                                assert bool(witness)==(not bf((C|be)-{v}))
                                counts['bipartite_essentiality_controls']+=1
                            if n<=3:assert witness==literal_protected(adj,P,C,v,k)
                            counts['exact_universal_essentiality_controls']+=1
                    for D in subsets:
                        if not D or not D<=C-P or not block_literal(C-D):continue
                        unchanged=signature(adj,P,C,k)==signature(adj,P,C-D,k)
                        assert safe_internal_deletion(adj,P,C,D,k)==unchanged
                        counts['internal_deletion_signature_controls']+=1
                        if unchanged:continue
                        bad=loss_obstruction(adj,P,C,D,k);f,_=literal_engine(bad['graph'],k)
                        assert f(bad['selected']) and not f(bad['selected']-D)
                        if col is not None:assert bipartition(bad['graph']) is not None
                        x=bad['failure'];p=bad['port'];assert bad['graph'][x]=={p}
                        counts['literal_capacity_loss_obstructions']+=1
                digest.update(json.dumps([n,[sorted(z) for z in adj],k,sorted(P)],sort_keys=True).encode())

# Arbitrary two-vertex exterior, all boundary edges plus possible exterior
# edge, all global selections: this tests universal implications on actual
# ambient graphs beyond the canonical witnesses.
for n in range(1,4):
    V=set(range(n));subsets=sets(n)
    for adj in graphs(n):
        for P in subsets:
            ee=[(p,x) for p in sorted(P) for x in (n,n+1)]+[(n,n+1)]
            for bits in range(1<<len(ee)):
                g=[set(z) for z in adj]+[set(),set()]
                for j,(a,b) in enumerate(ee):
                    if bits>>j&1:g[a].add(b);g[b].add(a)
                for k in range(1,5):
                    literal,_=literal_engine(g,k)
                    for S in sets(n+2):
                        if not literal(S):continue
                        C=S&V;assert admissible(adj,P,C,k)
                        counts['arbitrary_exterior_forming_selections']+=1
                        for v in C:
                            if protected_witnesses(adj,P,C,v,k):
                                assert not literal(S-{v});counts['arbitrary_exterior_protected_deletions']+=1
                        for D in subsets:
                            if not D or not D<=C-P:continue
                            if safe_internal_deletion(adj,P,C,D,k):
                                assert literal(S-D);counts['arbitrary_exterior_safe_batches']+=1
                    counts['arbitrary_exterior_graph_k_controls']+=1

# One formula gives a physical bipartite tree counterexample for every k>=3.
for k in list(range(3,10))+[16,31,64,257]:
    bad=activity_counterexample(k);g=bad['graph'];C=bad['selected'];D=bad['deleted'];n=len(g)
    assert sum(map(len,g))==2*(n-1) and n==2*k
    col={0:0};todo=[0]
    for a in todo:
        for b in g[a]:
            if b not in col:col[b]=1-col[a];todo.append(b)
            assert col[a]!=col[b]
    assert len(col)==n and len(g[0]&C)==k-1 and len(g[0]&(C-D))==k-2
    if k<=9:
        literal,_=literal_engine(g,k);assert literal(C) and not literal(C-D)
        block=[z-{n-1} for z in g[:-1]];f,_=literal_engine(block,k);assert f(C-D)
        counts['literal_boolean_activity_counterexamples']+=1
    counts['all_parameter_counterexample_controls']+=1

# Sharpness of the universal k-1 NEW-vertex obstruction bound. The block is
# K1,k, with its centre deleted and just one leaf designated as a port.
# Exhaust every smaller allowed exterior for k2..6: all edges among outside
# vertices and to that one port, and every outside selected subset.
for k in range(2,7):
    sharp=sharp_extension_order(k);block=sharp['block'];P=sharp['ports'];C=sharp['selected'];D=sharp['deleted'];n=len(block)
    bad=sharp['obstruction'];f,_=literal_engine(bad['graph'],k)
    assert f(bad['selected']) and not f(bad['selected']-D)
    counts['sharp_extension_attaining_controls']+=1
    for m in range(k-1):
        ee=[(0,n+j) for j in range(m)]+list(combinations(range(n,n+m),2))
        for bits in range(1<<len(ee)):
            g=[set(z) for z in block]+[set() for _ in range(m)]
            for j,(a,b) in enumerate(ee):
                if bits>>j&1:g[a].add(b);g[b].add(a)
            literal,_=literal_engine(g,k)
            for selected in sets(m):
                S=C|{n+j for j in selected}
                assert not literal(S) or literal(S-D)
                counts['complete_smaller_exterior_controls']+=1

# Canonical star blocks: a graph H with t_i>=max(k,2) private leaves at
# each vertex has SF_k=beta_2=sum_i t_i, regardless of edges of H.
# Exhaust H through order3 at one specified heterogeneous leaf vector per k.
for r in range(4):
    for core in graphs(r):
        for k in (1,2,3):
            g=[set(z) for z in core];leaf_count=0
            for p in range(r):
                t=max(k,2)+p%2;leaf_count+=t
                for _ in range(t):u=len(g);g.append({p});g[p].add(u)
            literal,mask_form=literal_engine(g,k);sf=beta=0;n=len(g)
            masks=[sum(1<<u for u in z) for z in g]
            for S in range(1<<n):
                size=S.bit_count()
                if size>beta and all(not(S>>v&1) or (S&masks[v]).bit_count()<=1 for v in range(n)):beta=size
                if not mask_form(S):continue
                if all(not mask_form(S^(1<<v)) for v in range(n) if S>>v&1):sf=max(sf,size)
            assert sf==beta==leaf_count
            counts['exact_corona_parameter_pairs']+=1

# Existing four-port two-star block remains a consequence at k2.
rows=['11001','11010','00011','01111','10111'];g=[set() for _ in range(10)]
for a,row in enumerate(rows):
    for b,bit in enumerate(row,5):
        if bit=='1':g[a].add(b);g[b].add(a)
P={0,1,5,6};C={0,1,2,5,6,7}
for S in sets(10):
    if len(S)>6 and admissible(g,P,S,2):
        assert any(safe_internal_deletion(g,P,S,{v},2) for v in S-P)
        counts['four_port_cap_controls']+=1
for v in C:assert protected_witnesses(g,P,C,v,2);counts['four_port_essential_vertices']+=1

report=dict(status='PASS',counts=dict(sorted(counts.items())),deterministic_sha256=digest.hexdigest(),
    scope='Written all-k finite boundary theorems and all-k>=3 boolean-activity counterfamily. Complete simple blocks through4, all ports/selections, k1..5; arbitrary2vertexexteriors through3, all interfaces/selections, k1..4. Literal stars enumerate centres and k distinct leaves, not the production degree predicate. Corona checks exhaust core graphs through3 for one stated heterogeneous leaf vector per k1,2,3. No bound on arbitrary graph gaps or grid triple equality.')
def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,default=ROOT/'output/star-boundary-capacity-check.json');args=p.parse_args()
    args.output.write_text(json.dumps(report,sort_keys=True,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
