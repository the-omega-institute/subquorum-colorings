"""Physical fixed-boundary regional constructions used by the unique C16 proof."""
from itertools import combinations,product
from auxiliary_square_forest import blocks
from mixed_owner_bridges import _exchange,_minimum_omission
from all_helper_optimization import score
from balanced_boundary_matching_cut import certificate as square_boundary


def square_region(data,region,reserved,F0):
    V=set(region);C=[data['owner_components'][i][0] for i in reserved]
    assert all(len(K)==4 for K in C)
    U,rec=square_boundary([e for e in data['P'] if set(e)<=V],
                         [e for e in data['Q'] if set(e)<=V],C,
                         {v:data['colour'][v] for v in V},F0)
    return U,dict(method='balanced square boundary',region=sorted(V),reserved=list(reserved),
                   boundary=sorted(rec['boundary']),fixed_boundary=sorted(F0),
                   deficiency=rec['deficiency'],guarantee=rec['guarantee'],
                   construction=rec)


def contained_exchange(data,region,reserved,fixed):
    V=set(region);U=set(fixed);i=min(reserved);C=data['owner_components'][i][0]
    # All other anchors already have their minimum omissions in fixed.
    other=U-set(C);candidates=[]
    for j in range(len(C)):
        for UC in _exchange(C,j):
            UU=(other|UC)&V;cost=len(score(2*data['b'],data['P'],data['Q'],UU)[1])
            candidates.append((len(UU)-2*cost,sorted(UU)))
    delta,UU=max(candidates,key=lambda z:(z[0],[-v for v in z[1]]));U=set(UU)
    assert delta>=(1 if len(U)%2 else 2)
    return U,dict(method='contained exceptional exchange',region=sorted(V),reserved=list(reserved),
                   deficiency=delta,candidate_deficiencies=[x[0] for x in candidates])


def mixed_eight(data,region,reserved,F0):
    V=set(region);cycles=[data['owner_components'][i][0] for i in reserved]
    assert sorted(map(len,cycles))==[4,4,8] and len(V)==20
    A=[e for e in data['P']+data['Q'] if set(e)<=V]
    comps=blocks(V,A);of={v:i for i,K in enumerate(comps) for v in K}
    assert all(len({of[v] for v in K})>=2 for K in cycles)
    adj={v:set() for v in V}
    for a,b in A:adj[a].add(b);adj[b].add(a)
    base={}
    for C in comps:
        root=min(C);base[root]=0;todo=[root]
        for a in todo:
            for b in sorted(adj[a]):
                if b not in base:base[b]=1-base[a];todo.append(b)
                assert base[a]!=base[b]
    orientations=[]
    for phases in product((0,1),repeat=len(comps)):
        col={v:base[v]^phases[of[v]] for v in V}
        nonmono=[j for j,C in enumerate(cycles) if len({col[v] for v in C})==2]
        orientations.append(len(nonmono))
        if len(nonmono)>=2:break
    assert len(nonmono)>=2
    chosen=nonmono[:2];options={}
    for j in chosen:
        C=cycles[j];start=next(k for k,a in enumerate(C) if col[a]!=col[C[(k+1)%len(C)]])
        options[j]=_exchange(C,start)
    candidates=[]
    for phases2 in product((0,1),repeat=2):
        U=set(F0)
        for j,C in enumerate(cycles):U|=options[j][phases2[chosen.index(j)]] if j in chosen else _minimum_omission(C,True)
        cost=len(score(2*data['b'],data['P'],data['Q'],U)[1])
        imbalance=abs(sum(1 if col[v]==0 else -1 for v in U));delta=len(U)-2*cost
        assert delta>=imbalance;candidates.append((delta,sorted(U),imbalance))
    delta,UU,_=max(candidates,key=lambda z:(z[0],[-v for v in z[1]]));U=set(UU)
    assert delta>=2
    return U,dict(method='mixed C8 two-square imbalance',region=sorted(V),reserved=list(reserved),
                   deficiency=delta,guarantee=2,auxiliary_orientation=sorted(col.items()),
                   nonmonochromatic_cycles=nonmono,examined_orientation_counts=orientations,
                   candidate_deficiencies=[z[0] for z in candidates],candidate_imbalances=[z[2] for z in candidates])


def mixed_ten(data,region,reserved,F0):
    """One C10, h C4s, two fixed boundary vertices: actual deficiency>=h."""
    V=set(region);cycles=[data['owner_components'][i][0] for i in reserved]
    tens=[C for C in cycles if len(C)==10];squares=[C for C in cycles if len(C)==4]
    assert len(tens)==1 and len(tens)+len(squares)==len(cycles)
    C10=tens[0];h=len(squares);F=V-{v for C in cycles for v in C};F0=set(F0)
    assert len(V)==4*h+12 and len(F)==2 and F0<=F
    col=data['colour'];assert {col[v] for v in F}=={0,1}
    P=[e for e in data['P'] if set(e)<=V];Q=[e for e in data['Q'] if set(e)<=V]
    assert len(P)==len(Q)==len(V)//2
    M=[(C[j],C[j+2]) for C in squares for j in (0,1)]
    adj={v:set() for v in V}
    for a,b in P+M:adj[a].add(b);adj[b].add(a)
    free=set(C10)|F;contact={};parts=blocks(V,P+M)
    for part in parts:
        endpoints=sorted(set(part)&free)
        if endpoints:
            assert len(endpoints)==2;a,b=endpoints;assert col[a]==col[b]
            contact[a]=b;contact[b]=a
    assert set(contact)==free
    freebits={};tables=[]
    patterns={((0,1),(2,3)):'01011',((0,2),(1,3)):'01101',((0,3),(1,2)):'01010'}
    for c in (0,1):
        f=next(v for v in F if col[v]==c);mate=contact[f]
        five=[v for v in C10 if col[v]==c];pos=five.index(mate);five=five[pos+1:]+five[:pos+1]
        assert five[4]==mate;idx={v:j for j,v in enumerate(five[:4])}
        pairs=tuple(sorted(tuple(sorted((idx[v],idx[contact[v]]))) for v in five[:4] if idx[v]<idx[contact[v]]))
        bits=patterns[pairs];assert sum(bits[j]==bits[(j+1)%5] for j in range(5))==1
        freebits.update({v:int(bits[j]) for j,v in enumerate(five)});freebits[f]=1-freebits[mate]
        tables.append(dict(colour=c,order=five,contact_pairs=pairs,bits=bits,boundary=f))
    bit={}
    for part in parts:
        root=min(set(part)&free) if set(part)&free else min(part)
        bit[root]=freebits.get(root,0);todo=[root]
        for a in todo:
            for b in sorted(adj[a]):
                if b not in bit:bit[b]=1-bit[a];todo.append(b)
                assert bit[a]!=bit[b]
        assert all(bit[v]==freebits[v] for v in set(part)&free)
    assert all(bit[a]!=bit[b] for a,b in P+M)
    candidates=[];budgets=[]
    hitting=lambda U:all({C10[j],C10[(j+1)%10],C10[(j+2)%10]}&U for j in range(10))
    for phases in product((0,1),repeat=2):
        initial={v for v in V if bit[v]==phases[col[v]]}
        assert all(not set(e)<=initial for e in P)
        base_Q=sum(set(e)<=initial for e in Q)
        repairs={C10[(j+1)%10] for j in range(10) if not {C10[j],C10[(j+1)%10],C10[(j+2)%10]}&initial}
        assert len(repairs)<=2 and all(sum(col[v]==c for v in repairs)<=1 for c in (0,1))
        UC=(initial&set(C10))|repairs;assert hitting(UC) and all(sum(col[v]==c for v in UC)<=4 for c in (0,1))
        while True:
            removable=next((v for v in sorted(UC) if hitting(UC-{v})),None)
            if removable is None:break
            UC.remove(removable)
        assert len(UC)==4
        missing=F0-initial;U=(initial-set(C10)-F)|UC|F0
        assert all(len(U&set(C))==2 for C in squares) and U&F==F0
        cost=len(score(2*data['b'],data['P'],data['Q'],U)[1])
        budget=base_Q+len(repairs)+len(missing);assert cost<=budget
        candidates.append((cost,sorted(U),list(phases),sorted(repairs),sorted(UC)));budgets.append(budget)
    assert sum(budgets)<=2*(h+4+len(F0))
    cost,UU,phases,repairs,UC=min(candidates);U=set(UU)
    assert cost<=(h+4+len(F0))//2
    delta=len(U)-2*cost;assert delta>=h
    return U,dict(method='mixed C10 contact-bit repair',region=sorted(V),reserved=list(reserved),
                   boundary=sorted(F),fixed_boundary=sorted(F0),deficiency=delta,guarantee=h,
                   bit=sorted(bit.items()),contact=sorted(contact.items()),tables=tables,
                   candidate_budgets=budgets,candidate_costs=[x[0] for x in candidates],
                   chosen_phases=phases,repairs=repairs,ten_omissions=UC)
