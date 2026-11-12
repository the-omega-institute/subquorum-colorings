"""Sharp all-helper8b/3 for arbitrary owner paths/even cycles, auxiliaryP2/P4/C4.

Close P4s and pair P2s into squares. One ghost P2 is paid for by its two
isolated owner vertices' surplus in the rainbow-forest theorem. Artificial
edges need not respect physical colours; the square theorem is colour-free.
Actual original certificates and original matching costs are returned.
"""
from auxiliary_square_forest import abstract_certificate
from owner_matching_certificate import prepare,components
from all_helper_optimization import score


def complete_short_auxiliary(n,A,B):
    """Abstract even short components, owner paths/even cycles; all-size bound.

    R=sum(|path| mod3) over owner PATH components, isolates included.
    Returns permitted original U with nu(A[U])<=floor((n-R)/6).
    """
    if not isinstance(n,int) or isinstance(n,bool) or n<0 or n%2:
        raise ValueError('Nonnegative even indexed order required')
    graphs=[]
    for edges in (A,B):
        E=sorted({tuple(sorted(e)) for e in edges})
        if any(len(e)!=2 or e[0]==e[1] or any(not isinstance(v,int) or isinstance(v,bool) or v not in range(n) for v in e) for e in E):
            raise ValueError('Simple indexed graph required')
        if any(sum(v in e for e in E)>2 for v in range(n)):
            raise ValueError('Maximum degree two required')
        graphs.append(E)
    A,B=graphs;aux=components(n,A);owners=components(n,B)
    if any((cyclic and len(K)!=4) or (not cyclic and len(K) not in (2,4)) for K,cyclic in aux):
        raise ValueError('Auxiliary components must be P2/P4/C4')
    if any(cyclic and len(K)%2 for K,cyclic in owners):
        raise ValueError('Owner paths/even cycles required')
    remainder=sum(len(K)%3 for K,cyclic in owners if not cyclic)
    pairs=[];added=[]
    for K,cyclic in aux:
        if len(K)==2:pairs.append(K)
        elif not cyclic:added.append((K[0],K[-1]))
    ghost=[];completed_n=n
    if len(pairs)%2:
        ghost=[n,n+1];completed_n+=2;pairs.append(ghost)
        added.append((n,n+1))
    for first,second in zip(pairs[::2],pairs[1::2]):
        added.extend([(first[1],second[0]),(second[1],first[0])])
    augmented=sorted(set(A+[(min(a,b),max(a,b)) for a,b in added]))
    square=abstract_certificate(completed_n,augmented,B)
    original_S=set(square['owners'])&set(range(n));U=set(range(n))-original_S
    T,M=score(n,[],A,U)
    expanded_U=set(range(completed_n))-set(square['owners'])
    _,expanded_M=score(completed_n,[],augmented,expanded_U)
    cost=len(M);bound=(n-remainder)//6
    assert len(expanded_M)==completed_n//2-len(square['owners'])
    assert len(expanded_M)<=(completed_n-remainder-2*bool(ghost))//6==bound
    assert cost<=len(expanded_M)<=bound
    assert all(sum(v in e and set(e)<=original_S for e in B)<=1 for v in original_S)
    assert not original_S&T and all(not set(e)<=T for e in A)
    return dict(n=n,owners=sorted(original_S),witnesses=sorted(T),U=sorted(U),matching=[list(e) for e in M],
                cost=cost,cost_bound=bound,path_remainder=remainder,ghost_vertices=ghost,
                added_auxiliary_edges=[list(e) for e in added],completed_order=completed_n,
                completed_cost=len(expanded_M),square_certificate=square)


def certificate(b,P,Q,B,colour):
    """Actual physical template; original graph certificate, no added physical edges."""
    data=prepare(b,P,Q,B,colour);A=sorted(set(data['P']+data['Q']))
    aux=components(2*b,A)
    if any((cyclic and len(K)!=4) or (not cyclic and len(K) not in (2,4)) for K,cyclic in aux):
        return dict(applicable=False,reason='auxiliary graph is outside P2/P4/C4')
    result=complete_short_auxiliary(2*b,A,data['B'])
    result.update(applicable=True,beta_I_lower=3*b-result['cost'])
    assert result['beta_I_lower']>=(16*b+result['path_remainder']+5)//6
    return result
