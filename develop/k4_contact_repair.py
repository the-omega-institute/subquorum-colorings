"""Simultaneous K4 repair by independent choices of owner matching pairs.

The contact 2-SAT criterion is sufficient for the actual all-helper8b/3 bound.
Failure rejects this criterion only. Exterior three-colouring is a feasibility
search; no polynomial bound for that supplied implementation is claimed.
"""
from collections import deque
from owner_matching_certificate import prepare, components, sat, three_colour
from all_helper_optimization import score


def _components(n, edges):
    adj=[set() for _ in range(n)]
    for a,b in edges:adj[a].add(b);adj[b].add(a)
    unseen=set(range(n));out=[]
    while unseen:
        K={min(unseen)};todo=list(K)
        while todo:
            for w in adj[todo.pop()]-K:K.add(w);todo.append(w)
        out.append(sorted(K));unseen-=K
    return out


def pair_choices(pairs, contacts):
    """Choose one member of each pair, with no forbidden contact; exact 2-SAT."""
    pairs=[tuple(p) for p in pairs]
    if any(len(p)!=2 or p[0]==p[1] for p in pairs) or len({v for p in pairs for v in p})!=2*len(pairs):
        raise ValueError('Disjoint two-element parts required')
    loc={v:(j,k) for j,p in enumerate(pairs) for k,v in enumerate(p)}
    contacts=sorted({tuple(sorted(e)) for e in contacts})
    if any(len(e)!=2 or e[0] not in loc or e[1] not in loc or e[0]==e[1] for e in contacts):
        raise ValueError('Contacts need two distinct candidate members')
    contacts=[e for e in contacts if loc[e[0]][0]!=loc[e[1]][0]]
    clauses=[[loc[a],loc[b]] for a,b in contacts]
    values,obstruction=sat(len(pairs),clauses)
    if values is None:return dict(feasible=False,obstruction=obstruction,clauses=clauses,contacts=contacts)
    chosen=[p[phase] for p,phase in zip(pairs,values)];S=set(chosen)
    assert not any(a in S and b in S for a,b in contacts)
    return dict(feasible=True,values=values,chosen=chosen,clauses=clauses,contacts=contacts)


def pseudoforest_choices(pairs, contacts):
    """Edge-to-endpoint matching proves every contact pseudoforest is feasible.

    Different member contacts between the same two parts remain parallel edges.
    Return None outside this sufficient graph class, never a negative SAT claim.
    """
    pairs=[tuple(p) for p in pairs];loc={v:j for j,p in enumerate(pairs) for v in p}
    contacts=sorted({tuple(sorted(e)) for e in contacts if loc[e[0]]!=loc[e[1]]})
    ends=[(loc[a],loc[b]) for a,b in contacts]
    for K in _components(len(pairs),ends):
        if sum(a in K and b in K for a,b in ends)>len(K):return None
    # Match each edge to an endpoint, giving each part at most one outgoing edge.
    assigned={}
    for i,(a,b) in enumerate(ends):
        parent={i:None};todo=deque([i]);last=None
        while todo and last is None:
            e=todo.popleft()
            for v in ends[e]:
                if v not in assigned:last=(e,v);break
                old=assigned[v]
                if old not in parent:parent[old]=(e,v);todo.append(old)
        assert last is not None
        e,v=last
        while True:
            assigned[v]=e
            if parent[e] is None:break
            e,v=parent[e]
    assert len(assigned)==len(contacts) and len(set(assigned.values()))==len(contacts)
    chosen=[]
    for j,p in enumerate(pairs):
        if j not in assigned:chosen.append(p[0]);continue
        edge=contacts[assigned[j]];chosen.append(next(v for v in p if v not in edge))
    assert not any(a in chosen and b in chosen for a,b in contacts)
    return dict(chosen=chosen,edge_owner=sorted((e,v) for v,e in assigned.items()),contacts=contacts)


def contact_instance(n,A,B,R):
    """Extract K4 components, owner-pair graph and distance-one/two contacts."""
    R=sorted({tuple(sorted(e)) for e in R});special=set();virtual=set()
    for K,cyclic in components(n,B):
        if cyclic and len(K)==4:
            special.update(K);virtual.update((tuple(sorted((K[0],K[2]))),tuple(sorted((K[1],K[3])))))
    if sorted(v for e in R for v in e)!=list(range(n)) or not set(R)<=set(B)|virtual or not virtual<=set(R):
        raise ValueError('Use a perfect actual owner matching, with virtual diagonals on every owner C4')
    F=sorted(e for e in set(B)-set(R) if not set(e)&special)
    if len({v for e in F for v in e})!=2*len(F):
        raise ValueError('Remaining owner edges must be a matching')
    J=sorted(set(A)|set(R));bad=[K for K in _components(n,J) if len(K)==4 and sum(set(e)<=set(K) for e in J)==6]
    if any(set(K)&special for K in bad):
        raise ValueError('Physical domain excludes a K4 using virtual owner-square diagonals')
    rid={v:i for i,e in enumerate(R) for v in e};pairs=[]
    for K in bad:
        part=sorted({rid[v] for v in K});assert len(part)==2
        pairs.append(part)
    candidate={v for p in pairs for v in p};H={j:set() for j in range(len(R))}
    for a,b in F:
        x,y=rid[a],rid[b];assert x!=y;H[x].add(y);H[y].add(x)
    assert max(map(len,H.values()),default=0)<=2
    contacts=set();witnesses={}
    for a in sorted(candidate):
        for middle in sorted(H[a]):
            if middle in candidate:
                e=tuple(sorted((a,middle)));contacts.add(e);witnesses.setdefault(e,[a,middle])
            for b in sorted(H[middle]-{a}):
                if b in candidate:
                    e=tuple(sorted((a,b)));contacts.add(e);witnesses.setdefault(e,[a,middle,b])
    partof={v:j for j,p in enumerate(pairs) for v in p}
    contacts=sorted(e for e in contacts if partof[e[0]]!=partof[e[1]])
    return dict(R=R,F=F,owner_square_vertices=sorted(special),J=J,bad=bad,pairs=pairs,H={j:sorted(z) for j,z in H.items()},
                contacts=contacts,contact_paths=[dict(contact=list(e),path=witnesses[e]) for e in contacts])


def certificate(b,P,Q,B,colour,R=None,exterior_colouring=None):
    """Actual three-set all-helper proof under the contact 2-SAT criterion."""
    data=prepare(b,P,Q,B,colour);n=2*b;A=sorted(set(data['P']+data['Q']));B=data['B']
    if R is None:
        if any(not cyclic and len(K)%2 for K,cyclic in data['owner_components']):
            return dict(applicable=False,reason='Owner graph has an odd-order path; no permitted perfect R supplied')
        R=[]
        for K,cyclic in data['owner_components']:
            if cyclic and len(K)==4:R.extend(((K[0],K[2]),(K[1],K[3])))
            else:R.extend((K[j],K[j+1]) for j in range(0,len(K),2))
    model=contact_instance(n,A,B,sorted(tuple(sorted(e)) for e in R));R=model['R'];F=model['F']
    choice=pair_choices(model['pairs'],model['contacts']);pseudo=pseudoforest_choices(model['pairs'],model['contacts'])
    if not choice['feasible']:
        return dict(applicable=False,reason='Independent owner-pair contact criterion is unsatisfiable',contact=model,choice=choice,pseudoforest=False)
    active=set(choice['chosen']);badvertices={v for K in model['bad'] for v in K};outside=set(range(n))-badvertices
    labels=(three_colour(outside,[e for e in model['J'] if set(e)<=outside]) if exterior_colouring is None else dict(exterior_colouring))
    if set(labels)!=outside or any(c not in range(3) for c in labels.values()) or any(labels[a]==labels[z] for a,z in model['J'] if a in outside and z in outside):
        raise ValueError('Exterior colouring must properly colour the whole K4-free exterior')
    rid={v:j for j,e in enumerate(R) for v in e};rmate={v:w for a,c in R for v,w in ((a,c),(c,a))}
    fmate={v:w for a,c in F for v,w in ((a,c),(c,a))};bonus={};lists={}
    for j in sorted(active):
        forbidden={labels[rmate[fmate[v]]] for v in R[j] if v in fmate and fmate[v] in outside}
        lists[j]=sorted(set(range(3))-forbidden);assert lists[j]
        bonus[j]=lists[j][0]
    direct=[]
    for c in range(3):
        T={v for v in outside if labels[v]==c}
        for part in model['pairs']:
            inactive=next(j for j in part if j not in active);T.update(R[inactive])
        doubled={v for j in active if bonus[j]==c for v in R[j]}
        S=set(doubled)
        forbidden={fmate[v] for v in doubled if v in fmate}
        for j,e in enumerate(R):
            if j in active:
                if bonus[j]!=c:S.add(e[0])
            elif set(e)<=outside:
                available=set(e)-T-forbidden;assert available
                S.add(min(available))
        assert not S&T and all(not set(e)<=T for e in A)
        assert all(sum(v in e and set(e)<=S for e in B)<=1 for v in S)
        direct.append(dict(owners=sorted(S),witnesses=sorted(T),size=b+len(S)+len(T),colour=c))
    assert sum(x['size'] for x in direct)==8*b
    best=max(direct,key=lambda x:x['size']);S=set(best['owners']);U=set(range(n))-S;T,M=score(n,data['P'],data['Q'],U)
    value=3*b-len(M);assert value>=best['size']>=(8*b+2)//3
    return dict(applicable=True,beta_I_lower=value,owners=sorted(S),witnesses=sorted(T),U=sorted(U),matching=[list(e) for e in M],cost=len(M),
                direct_sets=direct,direct_size_sum=8*b,contact=model,choice=choice,active_pairs=sorted(active),bonus=bonus,bonus_lists=lists,
                exterior_colouring=sorted(labels.items()),pseudoforest=pseudo is not None,pseudoforest_certificate=pseudo)


def cyclic_family(r):
    """Connected pure-cycle physical family with r unavoidable K4s, r>=2.

    r copies of the inherited16-index two-C8 fixture. Merge their unused
    auxiliary square by a cyclic splice of one Q edge per copy.
    """
    import json
    from pathlib import Path
    if type(r) is not int or r<2:raise ValueError('Integer r>=2 required')
    base=json.loads((Path(__file__).resolve().parent/'fixtures/k4-contact-base.json').read_text())
    a,c=base['free_Q_edge'];removed=tuple(sorted((a,c)))
    x=dict(b=8*r,P=[],Q=[],B=[],colour=base['colour']*r)
    for j in range(r):
        for key in ('P','Q','B'):
            x[key].extend((v+16*j,w+16*j) for v,w in base[key] if key!='Q' or tuple(sorted((v,w)))!=removed)
        x['Q'].append((a+16*j,c+16*((j+1)%r)))
    return x
