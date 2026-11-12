"""Two-connected partial templates with exact cost of forcing b witnesses."""


def instance(r):
    if not isinstance(r,int) or isinstance(r,bool) or r<1:
        raise ValueError('r must be a positive integer')
    n=8*r
    P=[(v,v+1) for v in range(0,n,2)]
    Q=[(v,(v+1)%n) for v in range(1,n,2)]
    B=[]
    for i in range(r):
        for parity in (0,1):
            order=[8*i+parity+2*j for j in range(4)]
            B.extend((order[j],order[(j+1)%4]) for j in range(4))
    active=set(range(0,2*(r//2),2))
    owners=[];witnesses=[]
    for i in range(r):
        t,s=({0,2,5,7},{1,3,4,6}) if i in active else ({1,3,6},{0,2,5,7})
        witnesses.extend(8*i+v for v in sorted(t))
        owners.extend(8*i+v for v in sorted(s))
    return {'r':r,'b':4*r,'P':P,'Q':Q,'B':B,
            'colour':[(v//2)%2 for v in range(n)],
            'active_blocks':sorted(active),'owners':owners,'witnesses':witnesses,
            'beta_I':11*r+r//2,'maximum_witness_restricted_optimum':10*r,
            'restricted_loss':r+r//2}
