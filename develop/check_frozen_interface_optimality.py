"""Solver-free checks of the written all-q frozen-interface optimum proof."""
import argparse
from collections import Counter
import itertools
import json
from pathlib import Path

from check_opposed_direction_interfaces import family, reflected_right, fast_rank_certificate, freezing_schedule
from check_perpendicular_guarded_reserves import neighbourhoods
from check_residual_corridors import direct_check
from check_promotion_cores import frozen_certificate

if not __debug__:raise RuntimeError('Run without -O; assertions required.')


def unrestricted_maximum(q):
    cur,*_=family(q);L=10*q+2
    E={10*i+c for i in range(q) for c in (2,10)}
    I={10*i+1 for i in range(1,q)};J={10*i+11 for i in range(q)}
    removed={(0,c) for c in range(3,L,2)}|{(1,c) for c in E}|{(2,c) for c in I}
    added={(0,c) for c in range(2,L,2)}|{(2,c) for c in E}|{(1,c) for c in J}
    assert removed<=cur[2] and not added&cur[2]
    assert len(removed)==8*q-1 and len(added)==8*q
    return (*cur[:2],cur[2]-removed|added,cur[3]),removed,added


def feasible_local(S,P,N):
    return not S&P and all(len(N[v]&(S|P))<=1 for v in S)


def physical_cover(q,P,N):
    """Reconstruct disjoint cover and compute local caps from actual geometry."""
    L=10*q+2;w=L-2
    patches=[{(r+j,10*i+2+k) for j in range(4) for k in (0,1)}
             for r in (0,w-2) for i in range(q)]
    replaced=set.union(set(),*patches);left=[(G,3) for G in patches]
    for r,c in itertools.product(range(0,L,2),repeat=2):
        G={(r+i,c+j) for i,j in itertools.product((0,1),repeat=2)}
        if G&replaced:assert G<=replaced;continue
        candidates=sorted(v for v in G if v not in P and len(N[v]&P)<=1)
        cap=max(len(S) for k in range(len(candidates)+1)
                for S in map(set,itertools.combinations(candidates,k)) if feasible_local(S,P,N))
        left.append((G,cap))
    for G,cap in left[:len(patches)]:
        candidates=sorted(v for v in G if v not in P and len(N[v]&P)<=1)
        actual=max(len(S) for k in range(len(candidates)+1)
                   for S in map(set,itertools.combinations(candidates,k)) if feasible_local(S,P,N))
        assert actual==cap==3
    right=[({reflected_right(v,L) for v in G},cap) for G,cap in left]
    cover=left+right;seen=set()
    for G,cap in cover:
        assert not seen&G;seen|=G
    assert seen==set(N)
    t=35*q*q+13*q+2
    assert sum(cap for _,cap in left)==t and sum(cap for _,cap in cover)==2*t
    D={(r,c) for r in (2,3) for c in range(L-6,L+2)}
    touched=[(G,cap) for G,cap in cover if G&D]
    assert len(touched)==4 and set.union(set(),*(G for G,_ in touched))==D
    touched.sort(key=lambda item:min(v[1] for v in item[0]))
    assert [cap for _,cap in touched]==[1,2,2,1]
    return cover,D


def local_stencil(q,P,N,M):
    L=10*q+2;p=(1,L-3);z=(4,L+1);mate={a:b for e in M for a,b in (e,e[::-1])}
    assert mate[p]==(1,L-4) and mate[z]==(5,L+1)
    assert N[p]-{mate[p]}=={(0,L-3),(1,L-2),(2,L-3)}
    assert not (N[p]-{mate[p]})&P
    assert N[z]-{mate[z]}=={(3,L+1),(4,L),(4,L+2)}
    assert (N[z]-{mate[z]})&P=={(3,L+1)}
    assert len(N[(4,L+2)]&P)==2
    D={(r,c) for r in (2,3) for c in range(L-6,L+2)}
    candidates={v for v in D if v not in P and len(N[v]&P)<=1}
    rel={(r,c-L) for r,c in candidates}
    assert rel=={(2,c) for c in (-4,-3,-2,-1,0)}|{(3,c) for c in (-5,-4,-3,-2,-1,0)}
    return p,z,candidates,D


def exhaustive_local_check(P,N,candidates,D,L):
    extra={(0,L-3),(1,L-2),(4,L)};xs=sorted(candidates|extra)
    assert len(xs)==14
    accepted=0;best=-1;witness=None
    for mask in range(1<<len(xs)):
        S={v for i,v in enumerate(xs) if mask>>i&1}
        if (4,L) not in S or len(S&{(0,L-3),(1,L-2),(2,L-3)})<2:continue
        if not feasible_local(S,P,N):continue
        accepted+=1;value=len(S&D)
        assert value<=5
        if value>best:best=value;witness=sorted(S)
    assert best==5
    return dict(assignments=1<<len(xs),accepted_necessary_freezing_feasible=accepted,
                exact_local_maximum=best,attaining_local_selected_points=witness)


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);args=p.parse_args()
    totals=Counter();records=[];fixture=None
    for q in (*range(1,9),10,12):
        cur,*_=family(q);R,C,T,M=cur;L=10*q+2;N=neighbourhoods(R,C);P={v for e in M for v in e}
        direct_check(*cur);p,z,candidates,D=local_stencil(q,P,N,M)
        cover,D2=physical_cover(q,P,N);assert D==D2
        witnesses=fast_rank_certificate(cur,freezing_schedule(q));assert frozen_certificate(cur)[0]==P
        assert p in P and z in P and len(T&D)==5
        for G,cap in cover:assert len(T&G)<=cap
        assert len(T)==70*q*q+26*q+3
        unrestricted,removed,added=unrestricted_maximum(q);direct_check(*unrestricted)
        assert len(unrestricted[2])==70*q*q+26*q+4
        assert all(len(unrestricted[2]&G)==cap for G,cap in cover)
        assert not (N[p]-{next(b if a==p else a for a,b in M if p in (a,b))})&(unrestricted[2]|P)
        assert p not in frozen_certificate(unrestricted)[0]
        totals['all_parameter_boards']+=1;totals['strict_frozen_endpoint_witnesses']+=len(witnesses)
        totals['disjoint_cover_members']+=len(cover);totals['physical_local_stencil_checks']+=1
        rec=dict(q=q,shape=(R,C),unrestricted_exact_maximum=len(unrestricted[2]),
                 fully_frozen_exact_maximum=len(T),frozen_slack=4*q+1,unrestricted_slack=4*q,
                 local_old_cap=6,local_frozen_cap=5,two_required_frozen_endpoints=(p,z))
        records.append(rec)
        if q==1:
            local=exhaustive_local_check(P,N,candidates,D,L);totals['local_physical_assignments']+=local['assignments']
            fixture=dict(**rec,local=local,endpoint_set=sorted(P),matching_edges=M,
                         frozen_selected_points=sorted(T),unrestricted_selected_points=sorted(unrestricted[2]),
                         removed=sorted(removed),added=sorted(added),
                         local_strip=sorted(D),cover=[dict(cells=sorted(G),cap=cap) for G,cap in cover])
    (Path(__file__).parent/'fixtures/frozen_interface_optimality.json').write_text(json.dumps(fixture,indent=2)+'\n')
    report=dict(status='PASS',totals=dict(totals),records=records,
        scope='Written all-q exact unrestricted and fully-frozen fixed-P selection optima; two frozen endpoints force one local loss; disjoint cover prevents repeated charges; explicit uniform unrestricted attainer.',
        limits=['Does not assert all frozen maximizers share the same compensation network.',
                'No optimization over replacement endpoint sets or other band phases.',
                'No universal5over6 improvement; all slacks positive.'])
    args.output.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(dict(status='PASS',totals=dict(totals)),indent=2))

if __name__=='__main__':main()
