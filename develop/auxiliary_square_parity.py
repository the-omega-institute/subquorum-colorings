"""Constructive sufficient criterion when every auxiliary component is a square."""
from owner_matching_certificate import components, prepare


def certificate(b, P, Q, B, colour):
    data = prepare(b,P,Q,B,colour)
    n = 2*b; V = set(range(n)); A = sorted(set(map(tuple,data['P']+data['Q'])))
    squares = components(n,A)
    if any(not cyclic or len(order)!=4 for order,cyclic in squares):
        return {'applicable':False,'reason':'auxiliary graph is not a union of squares'}
    square_of = {v:i for i,(order,_) in enumerate(squares) for v in order}
    def independent(D):
        result = set()
        for order,_ in squares:
            result |= max((set(order[0::2])&D,set(order[1::2])&D),key=len)
        return result
    D = set(); owner_beta = 0
    for order,cyclic in data['owner_components']:
        m = len(order)
        if not cyclic:
            selected = {v for j,v in enumerate(order) if j%3!=2}
        else:
            k = (m+2)//3; gaps = [3]*k; deficit = 3*k-m
            if deficit: gaps[-1] -= deficit
            U = set(); j = 0
            for gap in gaps: U.add(order[j]); j = (j+gap)%m
            assert j==0 and len(U)==k
            selected = set(order)-U
        assert len(selected)==((2*m)//3 if cyclic else (2*m+2)//3)
        D |= selected; owner_beta += len(selected)
    assert len(D)==owner_beta
    if owner_beta < 2*((n+2)//3)-2:
        return {'applicable':False,'reason':'owner dissociation number below criterion',
                'owner_beta':owner_beta,'required':2*((n+2)//3)-2}
    S = independent(D); target = (n+2)//3
    exchange = None
    if len(S)<target:
        assert owner_beta==2*((n+2)//3)-2 and owner_beta%2==0
        order = next(order for order,cyclic in data['owner_components'] if cyclic and len(order)%3)
        m = len(order); C = set(order)
        cross = next((j for j in range(m) if square_of[order[j]]!=square_of[order[(j+1)%m]]),None)
        if cross is None:
            assert m==4
            square = squares[square_of[order[0]]][0]
            D = (D-C)|set(square[0::2]); S = independent(D)
            exchange = {'type':'coincident square','component':order}
        else:
            if m==4: U0={order[cross],order[(cross+2)%m]}
            else:
                k=(m+2)//3; gaps=[3]*k; gaps[-1]=2
                if m%3==1:gaps[1]=2
                assert sum(gaps)==m and gaps[0]==3 and gaps[-1]==2
                U0=set();j=cross
                for gap in gaps:U0.add(order[j]);j=(j+gap)%m
                assert j==cross and len(U0)==k
            x,y=order[cross],order[(cross+1)%m]
            assert x in U0 and y not in U0
            U1=(U0-{x})|{y}
            candidates=[(D-C)|(C-U) for U in (U0,U1)]
            odd=[sum(len(candidate&set(square))%2 for square,_ in squares) for candidate in candidates]
            assert max(odd)>=2
            D=max(candidates,key=lambda candidate:len(independent(candidate)));S=independent(D)
            exchange={'type':'crossing owner edge','component':order,'edge':[x,y],
                      'deleted_before':sorted(U0),'deleted_after':sorted(U1),'odd_squares':odd}
    T = independent(V-S)
    assert len(D)==owner_beta and len(S)>=target and len(T)==b
    assert not S&T and not any({a,c}<=S or {a,c}<=T for a,c in A)
    assert all(sum(v in e and set(e)<=S for e in data['B'])<=1 for v in S)
    return {'applicable':True,'owner_beta':owner_beta,'required':2*((n+2)//3)-2,
            'maximum_owner_set':sorted(D),'owners':sorted(S),'witnesses':sorted(T),
            'beta_I_lower':b+len(S)+len(T),'exchange':exchange}
