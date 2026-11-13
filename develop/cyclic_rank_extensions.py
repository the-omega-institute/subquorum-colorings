"""Actual matching certificates for one-C8 and square-incidence cyclic classes.

These are sufficient classes, not a solver for arbitrary mixed cyclic inputs.
Whole-auxiliary parity and internal matching deficiency are distinguished.
"""
from itertools import combinations
from owner_matching_certificate import prepare,components,certificate as owner_certificate
from auxiliary_square_forest import blocks,rainbow_forest,certificate as square_certificate
from mixed_owner_bridges import _minimum_omission,_exchange,square_six_bridge
from all_helper_optimization import score


def parity_omission(aux,owners,chosen,root=None):
    """One independent owner-edge exchange per family, one common forest."""
    bycycle={e['cycle']:e for e in chosen};assert len(bycycle)==len(chosen)
    U=set()
    for i,(K,cyclic) in enumerate(owners):
        assert cyclic
        e=bycycle.get(i)
        U|=(_minimum_omission(K,True) if e is None else _exchange(K,K.index(e['x']))[0])
    adj={k:[] for k in range(len(aux))}
    for i,e in enumerate(chosen):
        adj[e['a']].append((e['b'],i));adj[e['b']].append((e['a'],i))
    parity={k:len(U&set(K))%2 for k,(K,_) in enumerate(aux)}
    visited=set();flips=[]
    roots=list(range(len(aux)))
    if root is not None:roots.remove(root);roots.insert(0,root)
    for start in roots:
        if start in visited:continue
        parent={start:None};order=[start];visited.add(start)
        for v in order:
            for w,i in adj[v]:
                if w not in parent:parent[w]=(v,i);order.append(w);visited.add(w)
        target={v:1 for v in order}
        target[start]=(sum(parity[v] for v in order)-(len(order)-1))%2
        need={v:parity[v]^target[v] for v in order}
        for v in reversed(order[1:]):
            p,i=parent[v]
            if need[v]:flips.append(i);need[p]^=1
        assert need[start]==0
    for i in flips:U^={chosen[i]['x'],chosen[i]['y']}
    odd=[k for k,(K,_) in enumerate(aux) if len(U&set(K))%2]
    assert len(odd)>=len(chosen)
    if root is not None:assert len(set(odd)-{root})>=len(chosen)
    return U,dict(flipped=sorted(flips),odd_auxiliary_components=odd)


def _connected(data):
    n=2*data['b'];A=sorted(set(data['P']+data['Q']));aux=components(n,A);owners=data['owner_components']
    square=[i for i,(K,_) in enumerate(aux) if len(K)==4];long=[i for i,(K,_) in enumerate(aux) if len(K)>4]
    if not long:
        rec=square_certificate(**{k:data[k] for k in ('b','P','Q','B','colour')})
        return set(range(n))-set(rec['owners']),dict(method='all auxiliary squares')
    if not square:
        rec=owner_certificate(data);assert rec['feasible']
        return set(range(n))-set(rec['owners']),dict(method='no auxiliary square')
    if all(len(K)==4 or len(K)%6==0 for K,_ in owners):
        rec=square_six_bridge(**{k:data[k] for k in ('b','P','Q','B','colour')});assert rec['applicable']
        return set(rec['U']),dict(method='owner C4/6k')
    of={v:i for i,(K,_) in enumerate(aux) for v in K};S={v for i in square for v in aux[i][0]}
    exceptional=[i for i,(K,_) in enumerate(owners) if len(K)%6]
    deficit=sum(2 if len(owners[i][0])%6==4 else 1 for i in exceptional)
    incidence=all(len(set(owners[i][0])&S)>=(3 if len(owners[i][0])%6==4 else 2) for i in exceptional)
    oneeight=len(long)==1 and len(aux[long[0]][0])==8
    if not incidence and not oneeight:
        return None,dict(method='outside the new sufficient cyclic classes')
    reserved=None;root=None
    if not incidence:
        root=long[0]
        reserved=next((i for i in exceptional if len(owners[i][0])==4 and all(of[v]==root for v in owners[i][0])),None)
    ground=[]
    for i in exceptional:
        if i==reserved:continue
        K=owners[i][0]
        for j,x in enumerate(K):
            y=K[(j+1)%len(K)]
            if of[x]!=of[y]:ground.append(dict(a=of[x],b=of[y],cycle=i,x=x,y=y))
    forest=rainbow_forest(range(len(aux)),ground);chosen=[ground[i] for i in forest['indices']];r=len(chosen)
    assert 3*r>=deficit-(0 if incidence else 1 if reserved is None else 2)
    U,parity=parity_omission(aux,owners,chosen,root if reserved is not None else None)
    candidates=[]
    if reserved is not None:
        C=set(owners[reserved][0]);fixed=U-C
        for pair in combinations(sorted(C),2):
            UU=fixed|set(pair);M=score(n,data['P'],data['Q'],UU)[1];candidates.append((len(M),sorted(UU)))
        _,UU=min(candidates);U=set(UU)
        local=set(aux[root][0])&U;localM=score(n,data['P'],data['Q'],local)[1]
        assert len(local)-2*len(localM)>=(1 if len(local)%2 else 2)
        assert len(U)-2*len(score(n,data['P'],data['Q'],U)[1])>=r+1
    assert len(U)==sum((len(K)+2)//3 for K,_ in owners)
    assert len(score(n,data['P'],data['Q'],U)[1])<=n//6
    return U,dict(method='square incidence' if incidence else 'one C8 reserved owner square' if reserved is not None else 'one C8 rank deficit',
                  forest=forest,parity=parity,deficit_thirds=deficit,reserved_owner=reserved,root=root,reserved_candidate_costs=candidates)


def certificate(b,P,Q,B,colour):
    data=prepare(b,P,Q,B,colour);n=2*b;A=sorted(set(data['P']+data['Q']))
    if len(data['Q'])!=b or any(not cyc for _,cyc in data['owner_components']):
        return dict(applicable=False,reason='Requires perfect Q and owner even cycles')
    U=set();records=[]
    for K in blocks(range(n),A+data['B']):
        idx={v:j for j,v in enumerate(K)}
        local=dict(b=len(K)//2,colour=[colour[v] for v in K])
        for key in ('P','Q','B'):local[key]=[(idx[a],idx[c]) for a,c in data[key] if a in idx]
        UU,rec=_connected(prepare(**local))
        if UU is None:return dict(applicable=False,reason=rec['method'],component=K)
        U|={K[v] for v in UU};records.append(dict(vertices=K,certificate=rec))
    S=set(range(n))-U;T,M=score(n,data['P'],data['Q'],U)
    assert all(sum(v in e and set(e)<=S for e in data['B'])<=1 for v in S)
    assert len(M)<=n//6
    return dict(applicable=True,U=sorted(U),owners=sorted(S),witnesses=sorted(T),matching=M,cost=len(M),
                beta_I_lower=3*b-len(M),components=records)


def coarse_parity_obstruction(t):
    """Exact all-scale obstruction to optimized whole-component parity only."""
    if type(t) is not int or t<1:raise ValueError('Positive integer required')
    r=6*t;L=8*r+8;n=L+8;Aorders=[list(range(L)),list(range(L,L+4)),list(range(L+4,n))];P=[];Q=[];B=[]
    for K in Aorders:
        P.extend(zip(K[::2],K[1::2]));Q.extend((K[j],K[(j+1)%len(K)]) for j in range(1,len(K),2))
    for i in range(r):
        K=[8*i+j for j in (0,2,1,3,4,6,5,7)];B.extend(zip(K,K[1:]+K[:1]))
    a=8*r;K=[a+4*j+k for j in range(4) for k in (0,2,1,3)];B.extend(zip(K,K[1:]+K[:1]))
    U={8*i+j for i in range(r) for j in (0,3,6)}|{a+j for j in (0,3,5,10,12,14)}
    return dict(b=n//2,P=P,Q=Q,B=B,colour=[(v//2)%2 for v in range(n)]),dict(U=sorted(U),minimum_omissions=18*t+6,
        exact_matching_cost=0,exact_beta_I=3*n//2,exact_min_coarse_cost=9*t+2,target_cost=8*t+2,coarse_shortfall=t,
        omission_intersections=[18*t+3,1,2],maximum_rainbow_forest=1)
