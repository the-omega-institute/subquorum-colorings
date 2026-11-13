"""Actual physical all-helper certificates for A=sC4+C16, arbitrary owner cycles."""
from auxiliary_square_forest import blocks
from owner_matching_certificate import prepare,components
from reserved_owner_squares import _connected as inherited_connected,_project
from cyclic_rank_extensions import parity_omission
from mixed_owner_bridges import one_K4_bridge,square_six_bridge,_minimum_omission
from all_helper_optimization import score
from c16_regional_compensation import square_region,contained_exchange,mixed_eight,mixed_ten


def clean(x):
    if isinstance(x,dict):return {k:clean(v) for k,v in x.items()}
    if isinstance(x,set):return sorted(x)
    if isinstance(x,(list,tuple)):return [clean(v) for v in x]
    return x


def root_witness(data,projected,reserved,forest):
    """Rado minimizer from the ORIGINAL common forest's verified dual cut."""
    owners=data['owner_components'];families={i for i,(C,_) in enumerate(owners) if len(C)%6 and i not in reserved}
    J=families-set(forest['dual_reachable_colours'])
    of={v:i for i,(C,_) in enumerate(projected) for v in C};E=[]
    for i in J:
        C=owners[i][0]
        E += [(of[a],of[C[(j+1)%len(C)]]) for j,a in enumerate(C)]
    parts=blocks(range(len(projected)),E)
    rank=len(projected)-len(parts)
    assert len(families)-len(J)+rank==forest['size']
    K=next(set(C) for C in parts if 0 in C)
    root_cycles={i for i in J if of[owners[i][0][0]] in K}
    assert all({of[v] for v in owners[i][0]}<=K for i in root_cycles)
    region={v for j in K for v in projected[j][0]}
    weight=sum(2 if len(owners[i][0])%6==4 else 1 for i in root_cycles)
    return root_cycles,region,dict(Rado_family=sorted(J),root_family=sorted(root_cycles),
                root_nodes=sorted(K),root_rank=len(K)-1,root_deficit_thirds=weight,
                total_subset_rank=rank,full_family_count=len(families),family_indices=sorted(families),
                projected_auxiliary=[C for C,_ in projected],reserved_owner_indices=sorted(reserved),
                forest_size=forest['size'],root_region=sorted(region))


def _connected(data):
    n=2*data['b'];A=data['P']+data['Q'];aux=components(n,A);owners=data['owner_components']
    long=[i for i,(K,_) in enumerate(aux) if len(K)>4]
    if len(long)!=1 or len(aux[long[0]][0])!=16:
        U,rec=inherited_connected(data)
        return U,dict(method='inherited sufficient class',prior=rec)
    if len(aux)<=2:
        rec=one_K4_bridge(**{k:data[k] for k in ('b','P','Q','B','colour')});assert rec['applicable']
        return set(rec['U']),dict(method='at most one auxiliary square',prior=rec)
    if all(len(K)==4 or len(K)%6==0 for K,_ in owners):
        rec=square_six_bridge(**{k:data[k] for k in ('b','P','Q','B','colour')})
        return set(rec['U']),dict(method='owner C4/6k',prior=rec)
    eights=[i for i,(C,_) in enumerate(owners) if len(C)==8]
    if len(eights)==1 and all(len(C) in (4,8) for C,_ in owners):
        reserved={i for i,(C,_) in enumerate(owners) if len(C)==4};k=len(reserved);assert k>=3
        U8=_minimum_omission(owners[eights[0]][0],True)
        U,local=square_region(data,set(range(n)),sorted(reserved),U8)
        assert len(score(n,data['P'],data['Q'],U)[1])<=n//6
        return U,dict(method='closed one C8 plus squares',local=local)
    L=set(aux[long[0]][0]);exceptional={i for i,(C,_) in enumerate(owners) if len(C)%6}
    weight=lambda I:sum(2 if len(owners[i][0])%6==4 else 1 for i in I)
    deficit=weight(exceptional);internal={i for i in exceptional if set(owners[i][0])<=L}
    history=[];region=L;reserved=set(internal);mode='contained';epsilon=0
    if internal:
        lengths=tuple(sorted(len(owners[i][0]) for i in internal))
        eps={(4,):2,(4,4):0,(4,4,4):0,(8,):2,(4,8):0,(10,):1,(4,10):0,(14,):0}
        assert lengths in eps,lengths;epsilon=eps[lengths]
        projected,root,forest,chosen=_project(aux,owners,reserved,region)
        residual=deficit-weight(reserved)
        if 3*len(chosen)<residual-epsilon:
            extra,enlarged,cut=root_witness(data,projected,reserved,forest)
            assert 3*cut['root_rank']<cut['root_deficit_thirds']-epsilon
            assert lengths in ((4,),(4,4)) and all(len(owners[i][0])==4 for i in extra)
            history.append(dict(stage='contained absorption',cut=cut,old_reserved=sorted(reserved)))
            reserved|=extra;region=enlarged;assert len(reserved)==4 and len(region)==20
            mode='pure four boundary';epsilon=0
        elif lengths==(4,4,4):mode='pure four boundary'
    else:
        # Start from a single root L. A deficient common forest supplies its
        # exact Rado minimizer; no search over arbitrary omission assignments.
        projected,root,forest,chosen=_project(aux,owners,set(),region)
        if 3*len(chosen)>=deficit-1:
            U,parity=parity_omission(projected,owners,chosen,root)
            assert len(score(n,data['P'],data['Q'],U)[1])<=n//6
            return U,dict(method='unique C16 ordinary rank',forest=forest,parity=parity,
                          projected_auxiliary=[C for C,_ in projected],reserved_owner_indices=[],rank_epsilon_thirds=1,
                          deficit_thirds=deficit,full_representation=False)
        reserved,region,cut=root_witness(data,projected,set(),forest)
        assert 3*cut['root_rank']<cut['root_deficit_thirds']-1
        history.append(dict(stage='initial serious rank cut',cut=cut))
        lengths=sorted(len(owners[i][0]) for i in reserved)
        free=len(region)-sum(lengths)
        if all(m==4 for m in lengths):
            k=len(lengths)
            assert (free==8 and k in (3,4)) or (free==4 and 4<=k<=7),(lengths,free)
            mode='pure eight boundary' if free==8 else 'pure four boundary'
        elif lengths==[4,4,8] and free==4:mode='mixed C8 four boundary'
        elif lengths in ([4,4,10],[4,4,4,10]) and free==2:mode='mixed C10 two boundary'
        else:raise AssertionError(('Unclassified serious support',lengths,free,cut))
    if mode=='pure eight boundary':
        projected,root,forest,chosen=_project(aux,owners,reserved,region)
        remaining=exceptional-reserved
        if len(chosen)<len(remaining):
            extra,enlarged,cut=root_witness(data,projected,reserved,forest)
            assert len(extra)>cut['root_rank']
            assert all(len(owners[i][0])==4 for i in extra)
            assert len(extra)==cut['root_rank']+1
            history.append(dict(stage='eight-boundary full-representative absorption',cut=cut,old_reserved=sorted(reserved)))
            reserved|=extra;region=enlarged;mode='pure four boundary'
            assert len(region)-4*len(reserved)==4
    # Build the ONE final exterior forest after deciding the full reserved region.
    projected,root,forest,chosen=_project(aux,owners,reserved,region)
    remaining=exceptional-reserved;residual=weight(remaining);r=len(chosen)
    full=mode!='contained'
    if full:assert r==len(remaining),(mode,r,len(remaining))
    if mode=='pure eight boundary' and len(reserved)==4:assert remaining
    else:assert 3*r>=residual-epsilon
    U,parity=parity_omission(projected,owners,chosen,root)
    fixed_exterior=U-region;owned={v for i in reserved for v in owners[i][0]};F=region-owned;F0=U&F
    if mode in ('pure four boundary','pure eight boundary'):
        localU,local=square_region(data,region,sorted(reserved),F0)
    elif mode=='mixed C8 four boundary':
        localU,local=mixed_eight(data,region,sorted(reserved),F0)
    elif mode=='mixed C10 two boundary':
        localU,local=mixed_ten(data,region,sorted(reserved),F0)
    else:localU,local=contained_exchange(data,region,sorted(reserved),U&region)
    assert localU&F==F0
    U=fixed_exterior|localU
    assert U-region==fixed_exterior
    assert len(U)==sum((len(C)+2)//3 for C,_ in owners)
    delta=len(U)-2*len(score(n,data['P'],data['Q'],U)[1])
    assert delta>=r+local['deficiency'] and 3*delta>=deficit-1
    assert len(score(n,data['P'],data['Q'],U)[1])<=n//6
    return U,dict(method='unique C16 '+mode+(' '+','.join(map(str,sorted(len(owners[i][0]) for i in internal))) if mode=='contained' else ''),
                  reserved_owner_indices=sorted(reserved),region=sorted(region),boundary=sorted(F),fixed_boundary=sorted(F0),
                  projected_auxiliary=[C for C,_ in projected],root=root,forest=forest,parity=parity,
                  rank_epsilon_thirds=epsilon if not full else 0,full_representation=full,
                  deficit_thirds=deficit,residual_deficit_thirds=residual,local=local,total_deficiency=delta,history=history)


def certificate(b,P,Q,B,colour):
    data=prepare(b,P,Q,B,colour);n=2*b;A=data['P']+data['Q']
    if len(data['Q'])!=b or any(not cyc for _,cyc in data['owner_components']):
        return dict(applicable=False,reason='Requires perfect Q and owner even cycles')
    U=set();records=[]
    for K in blocks(range(n),A+data['B']):
        idx={v:i for i,v in enumerate(K)};local=dict(b=len(K)//2,colour=[colour[v] for v in K])
        for key in ('P','Q','B'):local[key]=[(idx[a],idx[c]) for a,c in data[key] if a in idx]
        UU,rec=_connected(prepare(**local))
        if UU is None:return dict(applicable=False,reason='outside unique C16 and inherited sufficient classes',component=K)
        U|={K[v] for v in UU};records.append(dict(vertices=K,certificate=rec))
    S=set(range(n))-U;T,M=score(n,data['P'],data['Q'],U)
    assert all(sum(v in e and set(e)<=S for e in data['B'])<=1 for v in S)
    assert len(M)<=n//6
    return clean(dict(applicable=True,U=sorted(U),owners=sorted(S),witnesses=sorted(T),matching=M,
                      cost=len(M),beta_I_lower=3*b-len(M),components=records))
