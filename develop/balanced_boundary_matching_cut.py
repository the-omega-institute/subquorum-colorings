"""Exact boundary membership with any number of balanced free quartets."""
from fixed_boundary_matching_cut import forced_independent
from all_helper_optimization import score


def certificate(P,Q,reserved,colour,F0):
    """k actual C4s, 4h balanced free vertices; preserve exact prescribed F0.

    Return actual matching and deficiency at least
    max(0,2k-2floor((k+h)/2))+(|F0|mod2).
    """
    V=set(colour);k=len(reserved);P=list(P);Q=list(Q)
    assert sorted(v for e in P for v in e)==sorted(V)
    assert sorted(v for e in Q for v in e)==sorted(V)
    assert {frozenset(e) for e in P}.isdisjoint(frozenset(e) for e in Q)
    occupied=[v for C in reserved for v in C]
    assert len(occupied)==len(set(occupied))==4*k
    assert all(len(C)==4 and all(colour[C[j]]!=colour[C[(j+1)%4]] for j in range(4)) for C in reserved)
    F=V-set(occupied);F0=set(F0)
    assert len(F)%4==0 and F0<=F
    h=len(F)//4
    sides=[[v for v in sorted(F) if colour[v]==c] for c in (0,1)]
    assert list(map(len,sides))==[2*h,2*h]
    R_pairs=[(C[j],C[j+2]) for C in reserved for j in (0,1)]
    free_pairs=[[],[]];mixed=[]
    for c,side in enumerate(sides):
        inside=[v for v in side if v in F0];outside=[v for v in side if v not in F0]
        free_pairs[c] += list(zip(inside[::2],inside[1::2]))
        free_pairs[c] += list(zip(outside[::2],outside[1::2]))
        if len(inside)%2:
            assert len(outside)%2
            edge=(inside[-1],outside[-1]);free_pairs[c].append(edge);mixed.append(edge)
        assert len(free_pairs[c])==h
    artificial=[[a,c,b,d] for (a,b),(c,d) in zip(*free_pairs)]
    R_pairs += free_pairs[0]+free_pairs[1]
    to_dict=lambda E:{v:u for a,b in E for v,u in ((a,b),(b,a))}
    R=to_dict(R_pairs)
    assert set(R)==V
    forced=mixed[0][0] if mixed else None
    Y,cut=forced_independent(to_dict(P),to_dict(Q),R,colour,forced)
    Z=set(Y)
    for a,b in R_pairs:
        assert not {a,b}<=Z
        if not {a,b}&Z:Z.add(min(a,b))
    assert len(Z)==2*(k+h)
    assert all(len(Z&set(C))==2 for C in list(reserved)+artificial)
    a=[sum(v in F0 for v in side) for side in sides]
    intersection_lower=sum(x//2 for x in a)+bool(mixed)
    assert intersection_lower>=(len(F0)+1)//2
    assert len(Z&F0)>=intersection_lower
    U=(Z-F)|F0;additions=F0-Z
    assert len(additions)<=len(F0)//2
    assert U&F==F0 and all(len(U&set(C))==2 for C in reserved)
    T,M=score(len(V),P,Q,U);_,base_M=score(len(V),P,Q,Z)
    assert len(base_M)<=len(Z)-len(Y)<=(k+h)//2
    assert len(M)<=len(base_M)+len(additions)
    delta=len(U)-2*len(M)
    raw=2*k-2*((k+h)//2)+(len(F0)%2)
    guarantee=max(0,2*k-2*((k+h)//2))+(len(F0)%2)
    assert delta>=raw and delta>=len(F0)%2 and delta>=guarantee
    return U,dict(k=k,h=h,boundary=F,fixed_boundary=F0,side_membership_counts=a,
                  free_opposite_pairs=free_pairs,artificial_squares=artificial,
                  forced=forced,cut=cut,independent=Y,base_omissions=Z,
                  intersection_lower=intersection_lower,additions=additions,
                  base_matching=base_M,matching=M,independent_final=T,
                  deficiency=delta,raw_guarantee=raw,guarantee=guarantee)
