"""A single parity budget for disjoint auxiliary supports of owner exchanges."""
from owner_matching_certificate import prepare, components, sat, materialize
from mixed_owner_bridges import _exchange, _minimum_omission, _permitted, one_K4_bridge
from all_helper_optimization import score


def one_K4_search(b,P,Q,B,colour):
    """Exact <=1 bad-square decision in the specified matching family via 2SAT."""
    data=prepare(b,P,Q,B,colour); failures=[]
    for omit in [-1]+list(range(len(data['clauses']))):
        values,cut=sat(len(data['choices']),[c for j,c in enumerate(data['clauses']) if j!=omit])
        if values is not None:
            assert len(materialize(data,values)['K4'])<=1
            return dict(applicable=True,values=values,omitted_clause=omit,
                        certificate=one_K4_bridge(b,P,Q,B,colour,values))
        failures.append(dict(omitted_clause=omit,contradiction=cut))
    return dict(applicable=False,reason='every specified matching has at least two K4s',
                two_SAT_failures=failures)


def budget_certificate(b,P,Q,B,colour,U=None,chosen_cycles=None):
    """Any permitted U; chosen exceptional cycles must have minimum omissions.

    A chosen cycle may meet several auxiliary components. Those components
    must all have even U counts, and distinct chosen cycles must use disjoint
    sets of components. Default: greedy packing by support size then cycle id.
    The support packing need not be maximum. No independent per-cycle allowance
    is taken for two cycles consuming the same auxiliary component.
    """
    data=prepare(b,P,Q,B,colour);n=2*b;A=data['P']+data['Q'];owners=data['owner_components']
    if U is None:
        U=set().union(*(_minimum_omission(K,c) for K,c in owners)) if owners else set()
    else:U=set(U)
    assert U<=set(range(n)) and _permitted(n,B,U)
    initial=set(U);aux=components(n,A);which={v:j for j,(K,c) in enumerate(aux) for v in K}
    sizes=[len(U&set(K)) for K,c in aux];odd=[j for j,k in enumerate(sizes) if k%2]
    eligible=[]
    for i,(C,cyclic) in enumerate(owners):
        support=sorted({which[v] for v in C})
        if cyclic and len(C)%6 and len(U&set(C))==(len(C)+2)//3 and not any(sizes[j]%2 for j in support):
            eligible.append(dict(cycle=i,support=support))
    if chosen_cycles is None:
        packed=[];used=set()
        for rec in sorted(eligible,key=lambda x:(len(x['support']),x['cycle'])):
            if used.isdisjoint(rec['support']):packed.append(rec);used.update(rec['support'])
    else:
        assert len(set(chosen_cycles))==len(chosen_cycles)
        byid={x['cycle']:x for x in eligible};packed=[];used=set()
        for i in chosen_cycles:
            rec=byid[i];assert used.isdisjoint(rec['support'])
            packed.append(rec);used.update(rec['support'])
    exchanges=[]
    for rec in packed:
        C=owners[rec['cycle']][0];region={v for j in rec['support'] for v in aux[j][0]}
        fixed=(U&region)-set(C);local_size=len(U&region)
        assert local_size%2==0
        found=None
        for start in range(len(C)):
            for UC in _exchange(C,start):
                trial=fixed|UC
                if 2*len(score(n,P,Q,trial)[1])<local_size:
                    found=trial;break
            if found is not None:break
        assert found is not None,'Fixed-outside local count lemma'
        U=(U-region)|found
        exchanges.append(dict(cycle=rec['cycle'],support=rec['support'],U=sorted(found),
                              matching_cost=len(score(n,P,Q,found)[1])))
    assert len(U)==len(initial) and _permitted(n,B,U)
    final_sizes=[len(U&set(K)) for K,c in aux]
    assert all(final_sizes[j]==sizes[j] for j in range(len(aux)) if j not in used)
    bound=(len(initial)-len(odd))//2-len(packed)
    T,M=score(n,P,Q,U)
    assert len(M)<=bound
    return dict(initial_U=sorted(initial),U=sorted(U),auxiliary_component_omissions=sizes,
                final_component_omissions=final_sizes,
                odd_components=odd,eligible_cycles=eligible,packing=packed,exchanges=exchanges,
                cost_upper_bound=bound,actual_cost=len(M),owners=sorted(set(range(n))-U),
                witnesses=sorted(T),matching=M,beta_I_lower=3*b-len(M),
                certified_structural_lower=3*b-bound,
                meets_target=bound<=n//6)


def coupled_family(r):
    """Connected min-degree2/max-degree3 family; all global old tests fail r>=2."""
    assert isinstance(r,int) and r>=1
    baseP=[(0,2),(1,3),(5,7),(6,8),(4,10),(9,11),(12,14),(13,15),(16,18),(17,19)]
    baseQ=[(0,3),(1,2),(5,8),(6,7),(4,13),(15,12),(9,16),(18,17)]
    baseB=[(j,(j+1)%10) for j in range(10)]+[(off+j,off+(j+1)%4) for off in (12,16) for j in range(4)]
    P=[];Q=[];B=[];colour=[];initial=set();zero=set();crossing=[]
    for i in range(r):
        offset=20*i
        P += [(offset+a,offset+c) for a,c in baseP]
        Q += [(offset+a,offset+c) for a,c in baseQ]
        B += [(offset+a,offset+c) for a,c in baseB]
        B.append((offset+10,20*((i+1)%r)+11))
        colour += [j%2 for j in range(20)]
        initial.update(offset+v for v in [0,2,5,7,12,14,16,18])
        zero.update(offset+v for v in [0,1,4,7,14,15,16,17])
    data=prepare(10*r,P,Q,B,colour)
    crossing=[i for i,(C,cyclic) in enumerate(data['owner_components']) if cyclic and len(C)==10]
    return dict(b=10*r,P=P,Q=Q,B=B,colour=colour,initial_U=sorted(initial),
                zero_cost_U=sorted(zero),crossing_cycles=crossing,r=r)
