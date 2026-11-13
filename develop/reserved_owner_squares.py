"""Physical all-helper certificates for one C12 plus auxiliary squares.

Uses one common exchange forest, then chooses reserved owner cycles while
preserving every exterior membership. All returned costs are actual matchings.
The prior sufficient classes remain supported. No general mixed-cycle claim.
"""
from itertools import combinations
from owner_matching_certificate import prepare, components
from auxiliary_square_forest import blocks, rainbow_forest, graphic_rank
from cyclic_rank_extensions import _connected as prior_connected, parity_omission
from mixed_owner_bridges import one_K4_bridge, _exchange
from all_helper_optimization import score


def four_boundary(data, region, reserved, boundary_omissions):
    """Lemma: k=3/4 owner squares in 4(k+1) auxiliary vertices, fixed F0."""
    n=2*data['b'];R=set(region);owners=data['owner_components'];k=len(reserved)
    assert k in (3,4) and len(R)==4*(k+1)
    C=[owners[i][0] for i in reserved]
    assert all(len(K)==4 and set(K)<=R for K in C)
    F=R-set().union(*(set(K) for K in C));F0=set(boundary_omissions)
    assert len(F)==4 and F0<=F
    A=[e for e in data['P']+data['Q'] if set(e)<=R]
    assert len(A)==len(R) and all(not (set(e)&R) or set(e)<=R for e in data['P']+data['Q'])
    record=dict(region=sorted(R),reserved=list(reserved),boundary=sorted(F),fixed_boundary=sorted(F0))
    if len(F0)%2==0:
        fixed=F0|set().union(*(set(K[:2]) for K in C[1:]));candidates=[]
        for pair in combinations(sorted(C[0]),2):
            U=fixed|set(pair);d=len(U)-2*len(score(n,data['P'],data['Q'],U)[1])
            candidates.append((d,sorted(U)))
        d,UU=max(candidates,key=lambda z:(z[0],[-v for v in z[1]]));U=set(UU)
        record.update(method='even boundary fixed-outside square',candidate_deficiencies=[z[0] for z in candidates])
    else:
        sides=[[v for v in sorted(F) if data['colour'][v]==c] for c in (0,1)]
        assert list(map(len,sides))==[2,2]
        artificial=[sides[0][0],sides[1][0],sides[0][1],sides[1][1]]
        D=[(K[0],K[2]) for K in C+[artificial]]+[(K[1],K[3]) for K in C+[artificial]]
        adj={v:set() for v in R}
        for a,b in [e for e in data['P'] if set(e)<=R]+D:adj[a].add(b);adj[b].add(a)
        bit={}
        for v in sorted(R):
            if v in bit:continue
            bit[v]=0;todo=[v]
            for a in todo:
                for b in sorted(adj[a]):
                    if b not in bit:bit[b]=1-bit[a];todo.append(b)
                    assert bit[b]!=bit[a]
        label={v:2*data['colour'][v]+bit[v] for v in R}
        assert all(len({label[v] for v in K})==4 for K in C+[artificial])
        assert all(label[a]!=label[b] for a,b in A)
        lone=next(iter(F0 if len(F0)==1 else F-F0));lam=label[lone]
        pairs=[p for p in combinations(range(4),2) if (lam in p)==(len(F0)==1)]
        candidates=[]
        for p in pairs:
            U0={v for v in R if label[v] in p};edges=sum(set(e)<=U0 for e in A)
            U=(U0-F)|F0;candidates.append((edges,list(p),sorted(U)))
        assert sum(z[0] for z in candidates)==2*(k+1)
        edges,p,UU=min(candidates);U=set(UU);assert edges<=2*(k+1)//3
        record.update(method='odd boundary four labels',labels=sorted(label.items()),label_pair=p,
                      candidate_edge_counts=[z[0] for z in candidates],base_edges=edges)
    delta=len(U)-2*len(score(n,data['P'],data['Q'],U)[1])
    assert U&F==F0 and all(len(U&set(K))==2 for K in C)
    assert delta>=(3 if len(F0)%2 else 2)
    record.update(U=sorted(U),deficiency=delta)
    return U,record


def _project(aux,owners,reserved,region=None):
    if region is None:projected=aux;root=None
    else:
        R=set(region);projected=[(sorted(R),True)]+[(K,c) for K,c in aux if not set(K)&R];root=0
        assert sum(map(lambda z:len(z[0]),projected))==sum(map(lambda z:len(z[0]),aux))
    of={v:i for i,(K,_) in enumerate(projected) for v in K};ground=[]
    for i,(K,_) in enumerate(owners):
        if i in reserved or len(K)%6==0:continue
        for j,x in enumerate(K):
            y=K[(j+1)%len(K)]
            if of[x]!=of[y]:ground.append(dict(a=of[x],b=of[y],cycle=i,x=x,y=y))
    forest=rainbow_forest(range(len(projected)),ground)
    return projected,root,forest,[ground[i] for i in forest['indices']]


def _connected(data):
    U,previous=prior_connected(data)
    if U is not None:return U,dict(method='prior cyclic class',prior=previous)
    n=2*data['b'];A=sorted(set(data['P']+data['Q']));aux=components(n,A);owners=data['owner_components']
    long=[i for i,(K,_) in enumerate(aux) if len(K)>4]
    if len(long)!=1 or len(aux[long[0]][0])!=12:
        return None,dict(method='outside unique C12 and prior sufficient classes')
    if sum(len(K)==4 for K,_ in aux)<=1:
        rec=one_K4_bridge(**{k:data[k] for k in ('b','P','Q','B','colour')});assert rec['applicable']
        return set(rec['U']),dict(method='at most one auxiliary square',prior=rec)
    L=set(aux[long[0]][0]);exceptional=[i for i,(K,_) in enumerate(owners) if len(K)%6]
    weight=lambda I:sum(2 if len(owners[i][0])%6==4 else 1 for i in I)
    deficit=weight(exceptional);internal=[i for i in exceptional if set(owners[i][0])<=L]
    local=None;reserved=set();R=None;epsilon=1;strict=False
    if internal:
        reserved=set(internal);R=L
        lengths=sorted(len(owners[i][0]) for i in reserved)
        assert lengths in ([4],[4,4],[8],[10]),lengths
        method='contained '+','.join(map(str,lengths));epsilon=1 if lengths==[4] else 0
    else:
        projected,root,forest,chosen=_project(aux,owners,reserved)
        squares=[i for i,(K,_) in enumerate(aux) if len(K)==4]
        found=None
        for k in (3,4):
            for sq in combinations(squares,k-2):
                region=L|set().union(*(set(aux[j][0]) for j in sq))
                contained=[i for i,(K,_) in enumerate(owners) if len(K)==4 and set(K)<=region]
                for indices in combinations(contained,k):
                    of={v:j for j,(K,_) in enumerate(aux) for v in K}
                    E=[(of[x],of[y]) for i in indices for x,y in zip(owners[i][0],owners[i][0][1:]+owners[i][0][:1]) if of[x]!=of[y]]
                    if graphic_rank(range(len(aux)),E)==k-2:found=(set(indices),region);break
                if found:break
            if found:break
        if found is None:
            assert 3*len(chosen)>=deficit-1,'Serious rank loss must contain T3 or T4'
            U,parity=parity_omission(projected,owners,chosen)
            M=score(n,data['P'],data['Q'],U)[1];assert len(M)<=n//6
            return U,dict(method='unique C12 ordinary rank',forest=forest,parity=parity,deficit_thirds=deficit,
                          projected_auxiliary=[K for K,_ in projected],reserved_owner_indices=[],rank_epsilon_thirds=1)
        reserved,R=found;strict=len(reserved)==4;epsilon=-1 if strict else 0
        method='T4 strict rank' if strict else 'T3 four boundary'
    projected,root,forest,chosen=_project(aux,owners,reserved,R);r=len(chosen)
    residual=deficit-weight(reserved)
    assert 3*r>=residual-epsilon
    if strict:assert residual>0 and 3*r>residual
    U,parity=parity_omission(projected,owners,chosen,root)
    assert len(set(parity['odd_auxiliary_components'])-{root})>=r
    fixed_exterior=U-R
    if internal:
        i=min(reserved);C=owners[i][0];fixed=U-set(C);candidates=[]
        for j in range(len(C)):
            for UC in _exchange(C,j):
                UU=fixed|UC;UR=UU&R;d=len(UR)-2*len(score(n,data['P'],data['Q'],UR)[1])
                candidates.append((d,sorted(UU)))
        d,UU=max(candidates,key=lambda z:(z[0],[-v for v in z[1]]));U=set(UU)
        assert d>=(1 if len(U&R)%2 else 2)
        local=dict(method='contained exceptional fixed-outside exchange',region=sorted(R),reserved=sorted(reserved),
                   candidate_deficiencies=[z[0] for z in candidates],deficiency=d)
    else:
        F=R-set().union(*(set(owners[i][0]) for i in reserved));F0=U&F
        UR,local=four_boundary(data,R,sorted(reserved),F0);U=(U-R)|UR
        assert U&F==F0
    assert U-R==fixed_exterior
    delta=len(U)-2*len(score(n,data['P'],data['Q'],U)[1])
    assert delta>=r+local['deficiency'] and 3*delta>=deficit-1
    assert len(U)==sum((len(K)+2)//3 for K,_ in owners)
    assert len(score(n,data['P'],data['Q'],U)[1])<=n//6
    return U,dict(method='unique C12 '+method,reserved_owner_indices=sorted(reserved),root=root,
                  projected_auxiliary=[K for K,_ in projected],forest=forest,parity=parity,local=local,
                  deficit_thirds=deficit,residual_deficit_thirds=residual,rank_epsilon_thirds=epsilon,total_deficiency=delta)


def certificate(b,P,Q,B,colour):
    data=prepare(b,P,Q,B,colour);n=2*b;A=sorted(set(data['P']+data['Q']))
    if len(data['Q'])!=b or any(not cyclic for _,cyclic in data['owner_components']):
        return dict(applicable=False,reason='Requires perfect Q and owner even cycles')
    U=set();records=[]
    for K in blocks(range(n),A+data['B']):
        idx={v:j for j,v in enumerate(K)};local=dict(b=len(K)//2,colour=[colour[v] for v in K])
        for key in ('P','Q','B'):local[key]=[(idx[a],idx[c]) for a,c in data[key] if a in idx]
        UU,rec=_connected(prepare(**local))
        if UU is None:return dict(applicable=False,reason=rec['method'],component=K)
        U|={K[v] for v in UU};records.append(dict(vertices=K,certificate=rec))
    S=set(range(n))-U;T,M=score(n,data['P'],data['Q'],U)
    assert all(sum(v in e and set(e)<=S for e in data['B'])<=1 for v in S)
    assert len(M)<=n//6
    return dict(applicable=True,U=sorted(U),owners=sorted(S),witnesses=sorted(T),matching=M,
                cost=len(M),beta_I_lower=3*b-len(M),components=records)
