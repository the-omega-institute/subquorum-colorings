"""Fixed four-boundary patterns with any number of reserved owner squares."""
from square_core_matching_cut import matching_cut_certificate,bipartition_components
from all_helper_optimization import score


def forced_independent(P,Q,R,colour,forced=None):
    chosen,rec=matching_cut_certificate(P,Q,R,colour)
    if forced is None:return chosen,dict(forced=None,cut=rec)
    assert forced in colour
    side=colour[forced]
    inside={v:{m[v] for m in (P,R) if v in m} for v in colour}
    first=set()
    for a,b in bipartition_components(inside,{v for v in colour if colour[v]==side}):
        assert len(a)==len(b)
        first |= b if forced in b else a
    assert forced in first and 4*len(first)==len(colour)
    forbidden={Q[v] for v in first if v in Q}
    available={v for v in colour if colour[v]!=side}-forbidden
    second=set()
    for a,b in bipartition_components(inside,available):
        second |= max((a,b),key=lambda z:(len(z),sorted(z)))
    chosen=first|second
    J=rec['auxiliary']
    assert forced in chosen and all(not J[v]&chosen for v in chosen)
    assert 8*len(chosen)>=3*len(colour)
    return chosen,dict(forced=forced,first=first,second=second,forbidden=forbidden)


def four_boundary(P,Q,reserved,colour,F0):
    """Return fixed-F0 omissions, exact matching and deficiency>=2floor(k/2)+parity.

    P,Q are disjoint perfect physical matchings on this entire region;
    reserved is a list of disjoint physical C4 cyclic orders. Exactly four
    vertices remain, two in each physical colour. Artificial square conditions
    on those four vertices are discarded before returning.
    """
    V=set(colour);k=len(reserved);assert len(V)==4*(k+1)
    P=list(P);Q=list(Q)
    assert sorted(v for e in P for v in e)==sorted(V)
    assert sorted(v for e in Q for v in e)==sorted(V)
    assert {frozenset(e) for e in P}.isdisjoint(frozenset(e) for e in Q)
    occupied=[v for C in reserved for v in C]
    assert len(occupied)==len(set(occupied))==4*k
    assert all(len(C)==4 and all(colour[C[j]]!=colour[C[(j+1)%4]] for j in range(4)) for C in reserved)
    F=V-set(occupied);F0=set(F0);assert len(F)==4 and F0<=F
    sides=[[v for v in sorted(F) if colour[v]==side] for side in (0,1)]
    assert list(map(len,sides))==[2,2]
    artificial=[sides[0][0],sides[1][0],sides[0][1],sides[1][1]]
    pairs=[(C[j],C[j+2]) for C in list(reserved)+[artificial] for j in (0,1)]
    to_dict=lambda E:{v:u for a,b in E for v,u in ((a,b),(b,a))}
    R=to_dict(pairs)
    if len(F0) in (1,2):forced=min(F0)
    elif len(F0)==3:forced=R[next(iter(F-F0))]
    else:forced=None
    Y,rec=forced_independent(to_dict(P),to_dict(Q),R,colour,forced)
    Z=set(Y)
    for a,b in pairs:
        assert not {a,b}<=Y
        if not {a,b}&Z:Z.add(min(a,b))
    assert len(Z)==2*(k+1) and all(len(Z&set(C))==2 for C in list(reserved)+[artificial])
    additions=F0-Z;U=(Z-F)|F0
    assert len(additions)<=len(F0)//2
    assert U&F==F0 and all(len(U&set(C))==2 for C in reserved)
    T,M=score(len(V),P,Q,U)
    _,base_matching=score(len(V),P,Q,Z)
    assert len(base_matching)<=len(Z)-len(Y)<=(k+1)//2
    assert len(M)<=len(base_matching)+len(additions)
    delta=len(U)-2*len(M);guarantee=2*(k//2)+(len(F0)%2)
    assert delta>=guarantee
    return U,dict(boundary=F,fixed_boundary=F0,base_omissions=Z,independent=Y,
                   forced=forced,cut=rec,additions=additions,matching=M,
                   independent_final=T,deficiency=delta,guarantee=guarantee,
                   base_cost=len(base_matching))
