"""Adjacent module maxima, unique actual mates, and exact unpaid/slack counts.

Solver-free. All-size proofs are in FORCED_MATES_AND_ADJACENT_MAXIMA.md.
"""
import argparse
from collections import Counter
import itertools
import json
from pathlib import Path

from check_selection_maximum_singleton import (
    cropped, fixed_p_maximum, candidates, tile_bounds, feasible,
    compile_even_width, closure, reduced_serial_certificate,
)
from check_frozen_shared_mixed_gate import check_rank_certificate
from check_promotion_cores import frozen_certificate
from check_residual_corridors import direct_check
from check_compensation_flow_normal_form import owner_data
from check_whole_support_fork_flow import fork_flow

if not __debug__:
    raise RuntimeError('Run without -O; assertions required.')


def configuration(w,q):
    assert w>=8 and w%2==0 and q>=1
    base=cropped(w)
    module=[e for e in base[3] if max(v[1] for v in e)<10]
    matching=[tuple((r,c+10*i) for r,c in e) for i in range(q) for e in module]
    T={(0,c) for c in range(1,10*q+2,2)}|{(w+1,c) for c in range(1,10*q+2,2)}
    for r in (1,w):T|={(r,10*i+c) for i in range(q) for c in (0,2)}|{(r,10*q)}
    T|={(2,0)}|{(2,10*i+c) for i in range(q) for c in (8,11)}
    T|={(3,10*i+c) for i in range(q) for c in (1,3,7,9)}|{(3,10*q+1)}
    upper={10*i+c for i in range(q) for c in (0,2,8)}|{10*q}
    lower={10*i+c for i in range(q) for c in (1,3,7,9)}|{10*q+1}
    for r in range(4,w-2,2):
        T|={(r,c) for c in upper}
        row=lower if r!=w-4 else (lower-{1,3})|{0,2}
        T|={(r+1,c) for c in row}
    T|={(w-2,c) for c in (upper-{0,2})|{1,3}}
    T|={(w-1,0)}|{(w-1,10*i+11) for i in range(q)}
    return w+2,10*q+2,T,matching


def forced_order(w,q):
    """Leaf endpoint, mate; after earlier pairs are removed, leaf has only mate.
    Independent of T. Formula works on the entire P-neighbour graph.
    """
    order=[]
    for i in range(q):
        def add(a,b):order.append(((a[0],a[1]+10*i),(b[0],b[1]+10*i)))
        for r in (1,w):
            add((r,3),(r,4));add((r,9),(r,8))
        add((1,7),(1,6))
        for r in range(1,w,2):
            add((r,5),(r+1,5))
            if r+1<w:
                add((r+1,4),(r+2,4));add((r+1,6),(r+2,6))
        add((w,6),(w,7));add((w-1,7),(w-1,8))
    return order


def verify_forced_mates(cur,order):
    P={v for e in cur[3] for v in e}
    canonical={frozenset(e) for e in cur[3]}
    remaining=set(P);certificate=[]
    for rank,(a,b) in enumerate(order):
        assert a in remaining and b in remaining and frozenset((a,b)) in canonical
        neighbours={u for u in remaining if sum(abs(x-y) for x,y in zip(a,u))==1}
        assert neighbours=={b}
        remaining-={a,b};certificate.append(dict(leaf=a,mate=b,rank=rank))
    assert not remaining
    rank={v:k for k,e in enumerate(order) for v in e}
    for a,b in order:
        assert all(rank[u]<rank[a] for u in P-{b} if sum(abs(x-y) for x,y in zip(a,u))==1)
    return certificate


def uniform_freezing(w,q,cur):
    # The prior right module's reduced-selection certificate is internally
    # closed in its own P slab. Translate that same proof to EVERY module.
    base=cropped(w);reduced=(*base[:2],base[2]-{(w-2,13)},base[3])
    old=reduced_serial_certificate(w,reduced)
    right=[[v for v in layer if v[1]>=10] for layer in old]
    right=[layer for layer in right if layer]
    layers=[[(r,c-10+10*i) for r,c in layer] for i in range(q) for layer in right]
    return check_rank_certificate(cur,layers),layers


def upper_certificate(w,q,cur):
    empty=(*cur[:2],set(),cur[3]);C=candidates(empty);caps=tile_bounds(empty,C)
    terminal=[2,2,1,1,1]*q+[2]
    interior=[2,2,0,1,2]*q+[2]
    penultimate=[2,2,0,0,1]*q+[2]
    assert caps==[terminal]+[interior]*(w//2-2)+[penultimate,terminal]
    assert list(map(sum,caps))==[7*q+2]*(w//2-1)+[5*q+2,7*q+2]
    assert sum(map(sum,caps))==(7*q+2)*(w//2)+5*q+2
    cover=set();patches=[]
    for r,i in itertools.product((0,w-2),range(q)):
        c=2+10*i;cells={(r+j,c+k) for j in range(4) for k in (0,1)}
        assert not cover&cells;cover|=cells
        allowed={(r,c),(r,c+1),(r+1,c),(r+2,c),(r+3,c),(r+3,c+1)}
        assert C&cells==allowed
        pairs=[((r,c),(r,c+1)),((r+1,c),(r+2,c)),((r+3,c),(r+3,c+1))]
        assert all(not feasible(empty,pair) for pair in pairs)
        assert sum(caps[j//2][c//2] for j in (r,r+2))==4
        patches.append(dict(first_row=r,first_column=c,old_cap=4,new_cap=3))
    assert len(patches)==2*q
    return dict(tile_bound=sum(map(sum,caps)),patches=patches,upper_bound=(7*q+2)*(w//2)+3*q+2)


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',required=True,type=Path);args=p.parse_args()
    totals=Counter();records=[];fixture=None
    for w,q in itertools.product((8,10,12,20,40,64),(1,2,3,4,7,12)):
        cur=configuration(w,q);direct_check(*cur)
        explicitP={(r,c+10*i) for i in range(q) for c,rows in
            [(3,(1,w)),(4,range(1,w+1)),(5,range(1,w+1)),(6,range(1,w+1)),
             (7,(1,w-1,w)),(8,(1,w-1,w)),(9,(1,w))] for r in rows}
        assert explicitP=={v for e in cur[3] for v in e}
        expectedPairs={((1,0),(2,0)),((w-4,0),(w-3,0)),
            ((w-4,2),(w-3,2)),((w-1,0),(w,0))}
        expectedPairs|={((2,10*i+11),(3,10*i+11)) for i in range(q)}
        actualPairs={(a,b) for a in cur[2] for b in ((a[0]+1,a[1]),(a[0],a[1]+1)) if b in cur[2]}
        assert actualPairs==expectedPairs
        if q==2:
            old=fixed_p_maximum(w)
            assert cur[:3]==old[:3] and {frozenset(e) for e in cur[3]}=={frozenset(e) for e in old[3]}
            totals['previous_two_module_exact_comparisons']+=1
        cert=verify_forced_mates(cur,forced_order(w,q));upper=upper_certificate(w,q,cur)
        assert len(cur[2])==upper['upper_bound'] and len(cur[3])==q*(3*w//2+5)
        ranks,layers=uniform_freezing(w,q,cur)
        assert frozen_certificate(cur)[0]=={v for e in cur[3] for v in e}
        data,meta=compile_even_width(cur);own,A,B,M=owner_data(*data[:2]);flow=fork_flow(*data)
        assert (len(A),len(B),len(M))==(q,0,7*q)
        assert meta['raw']==3*q and meta['slack']==2*q
        assert not closure(data)[1] and (flow['value'],flow['cost'],flow['deficit'])==(0,0,q)
        totals['adjacent_frozen_exact_maximum_boards']+=1
        totals['forced_unique_matching_pairs']+=len(cert)
        totals['disjoint_replacement_patches']+=len(upper['patches'])
        record=dict(w=w,modules=q,shape=cur[:2],selected=len(cur[2]),matching=len(cur[3]),
            exact_fixed_P_maximum=upper['upper_bound'],alpha=len(A),beta=len(B),mixed=len(M),
            raw_intervals=meta['raw'],value=0,deficit=q,slack=2*q)
        records.append(record)
        if (w,q)==(8,1):
            fixture=dict(**record,selected_points=sorted(cur[2]),matching_edges=cur[3],
                unique_matching_leaf_certificate=cert,freezing_layers=layers,
                strict_rank_witnesses=ranks,upper_certificate=upper,
                source_support=[dict(tips=pair,support=sorted(data[3][o])) for o,pair in enumerate(data[1])])
    (Path(__file__).parent/'fixtures'/'adjacent_maximum_unique_mate_module.json').write_text(json.dumps(fixture,indent=2)+'\n')
    args.output.write_text(json.dumps(dict(status='PASS',totals=dict(totals),records=records,
        scope='Written all-even-height/all-module-count exact ALL-T fixed-P optimum; uniform leaf elimination proves '
              'uniqueness of M, uniform freezing, all raw resources and exact zero payment.',
        limits=['Does not optimize over different endpoint sets P.',
                'Aligned horizontal bands retained; another direction/phase may pay all.',
                'No universal5over6 improvement or global Omega counterexample.']),indent=2)+'\n')
    print(json.dumps(dict(status='PASS',totals=dict(totals)),indent=2))

if __name__=='__main__':main()
