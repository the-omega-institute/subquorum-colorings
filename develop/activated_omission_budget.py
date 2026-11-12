"""Simultaneous owner exchanges in a consistently chosen activation graph."""
from owner_matching_certificate import prepare
from mixed_owner_bridges import _exchange, _minimum_omission, _permitted
from all_helper_optimization import score


def activated_budget(b,P,Q,B,colour,chosen_cycles,U=None,W=None):
    """Construct a physical certificate; no optimal candidate selection claim.

    W contains U and every vertex of every chosen exceptional owner cycle.
    Its components, all parity counts, and full supports are computed together.
    Supports must be disjoint and all touched initial component counts even.
    """
    d=prepare(b,P,Q,B,colour);n=2*b;V=set(range(n));owners=d['owner_components']
    if U is None:
        U=set().union(*(_minimum_omission(C,c) for C,c in owners)) if owners else set()
    else:U=set(U)
    assert U<=V and _permitted(n,B,U)
    initial=set(U);chosen_cycles=list(chosen_cycles)
    assert len(set(chosen_cycles))==len(chosen_cycles)
    assert all(isinstance(i,int) and 0<=i<len(owners) for i in chosen_cycles)
    Cs=[set(owners[i][0]) for i in chosen_cycles]
    required=U|set().union(*Cs) if Cs else set(U)
    W=required if W is None else set(W)
    assert required<=W<=V
    adj={v:set() for v in W}
    for a,c in d['P']+d['Q']:
        if a in W and c in W:adj[a].add(c);adj[c].add(a)
    blocks=[];unseen=set(W)
    while unseen:
        K={min(unseen)};todo=list(K)
        while todo:
            for v in sorted(adj[todo.pop()]-K):K.add(v);todo.append(v)
        blocks.append(K);unseen-=K
    which={v:j for j,K in enumerate(blocks) for v in K}
    sizes=[len(U&K) for K in blocks];used=set();plans=[]
    for i,C in zip(chosen_cycles,Cs):
        assert owners[i][1] and len(C)%6 and len(C&U)==(len(C)+2)//3
        support=sorted({which[v] for v in C})
        assert used.isdisjoint(support) and all(sizes[j]%2==0 for j in support)
        used.update(support);plans.append(dict(cycle=i,support=support))
    exchanges=[]
    for p in plans:
        C=owners[p['cycle']][0];region=set().union(*(blocks[j] for j in p['support']))
        fixed=(U&region)-set(C);m=len(U&region);found=None
        for start in range(len(C)):
            for UC in _exchange(C,start):
                trial=fixed|UC
                if 2*len(score(n,P,Q,trial)[1])<m:found=trial;break
            if found is not None:break
        assert found is not None,'Fixed-outside local count lemma'
        U=(U-region)|found
        exchanges.append(dict(cycle=p['cycle'],support=p['support'],U=sorted(found),
                              matching_cost=len(score(n,P,Q,found)[1])))
    odd=[j for j,k in enumerate(sizes) if k%2]
    bound=(len(initial)-len(odd))//2-len(plans)
    T,M=score(n,P,Q,U)
    assert len(U)==len(initial) and U<=W and _permitted(n,B,U) and len(M)<=bound
    final_sizes=[len(U&K) for K in blocks]
    assert all(sizes[j]==final_sizes[j] for j in range(len(blocks)) if j not in used)
    return dict(initial_U=sorted(initial),U=sorted(U),activated_vertices=sorted(W),
                activated_components=[sorted(K) for K in blocks],
                initial_component_omissions=sizes,final_component_omissions=final_sizes,
                odd_components=odd,packing=plans,exchanges=exchanges,
                cost_upper_bound=bound,actual_cost=len(M),matching=M,
                owners=sorted(V-U),witnesses=sorted(T),beta_I_lower=3*b-len(M),
                certified_structural_lower=3*b-bound,meets_target=bound<=n//6)


def separated_long_cycle_family(r):
    """Connected60r physical vertices; inactive vertices split one C_(16r)."""
    assert isinstance(r,int) and r>=1
    p0=[(0,2),(1,3),(5,7),(6,8),(4,10),(9,11),
        (12,14),(13,15),(16,18),(17,19),(20,21),(22,23)]
    q0=[(0,3),(1,2),(5,8),(6,7),(4,13),(15,12),
        (9,16),(18,17),(14,20),(21,22),(23,19)]
    b0=[(j,(j+1)%10) for j in range(10)]
    for C in ([12,13,14,15],[16,17,18,19],[20,22,21,23]):
        b0+=list(zip(C,C[1:]+C[:1]))
    P=[];Q=[];B=[];colour=[];U=set();zero=set()
    for i in range(r):
        off=24*i
        P += [(off+a,off+c) for a,c in p0]
        Q += [(off+a,off+c) for a,c in q0]
        Q.append((off+10,24*((i+1)%r)+11))
        B += [(off+a,off+c) for a,c in b0]
        B.append((off+10,24*((i+1)%r)+11))
        colour += [j%2 for j in range(20)]+[1,1,0,0]
        U.update(off+j for j in [0,2,5,7,12,14,16,18,21,22])
        zero.update(off+j for j in [0,1,4,7,14,15,16,17,21,23])
    d=prepare(12*r,P,Q,B,colour)
    chosen=[i for i,(C,c) in enumerate(d['owner_components'])
            if c and min(C)%24 in (12,16)]
    return dict(b=12*r,P=P,Q=Q,B=B,colour=colour,r=r,
                initial_U=sorted(U),chosen_cycles=chosen,zero_cost_U=sorted(zero))
