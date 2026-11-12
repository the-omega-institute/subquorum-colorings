"""Exact dissociation optimization on the stated two-wing construction.

The proof and scope are in docs/SHARP_MINIMUM_TWO_DEGREE_BOUND.md.
Standard library only. No floating point or external optimizer.
"""
from functools import lru_cache


def validate(p_left,p_right,adj):
    if any(type(p)is not int or p<1 for p in(p_left,p_right)):
        raise ValueError('Positive integer wing sizes are required.')
    if len(adj)!=2*p_left or any(type(m)is not int or not 0<=m<1<<(2*p_right)for m in adj):
        raise ValueError('Witness adjacency has an invalid row or bit domain.')


def graph(p_left,p_right,adj):
    validate(p_left,p_right,adj)
    total=p_left+p_right;n=6*total+2;g=[set()for _ in range(n)]
    def edge(a,b):g[a].add(b);g[b].add(a)
    for j in range(total):
        for a,b in((0,1),(0,2),(1,4),(2,5),(3,5)):edge(6*j+a,6*j+b)
    for a,mask in enumerate(adj):
        for b in range(2*p_right):
            if mask>>b&1:edge(6*(a//2)+4+a%2,6*(p_left+b//2)+4+b%2)
    for first,p,u in((0,p_left,6*total),(p_left,p_right,6*total+1)):
        for j in range(first,first+p):edge(u,6*j+3)
        edge(u,6*first+2)
    return g,{6*j+a for j in range(total)for a in range(4)}


@lru_cache(None)
def local_options(w,sat,u,distinguished):
    """Best four-variable score at each consumed degree0/1 of the wing u."""
    result={}
    for mask in range(16):
        c,x,y,i=((mask>>j)&1 for j in range(4))
        a,b=w&1,(w>>1)&1
        if c and x+y>1:continue
        if x and c+a>1:continue
        if y and c+b+u*distinguished>1:continue
        if i and b+u>1:continue
        if a and x+(sat&1)>1:continue
        if b and y+i+((sat>>1)&1)>1:continue
        used=u*(i+distinguished*y)
        if used>1:continue
        if used not in result or mask.bit_count()>result[used][0]:
            result[used]=(mask.bit_count(),mask)
    return result


@lru_cache(None)
def wing(p,w,sat):
    if not(0<=sat<1<<(2*p)and 0<=w<1<<(2*p)and sat&w==sat):
        raise ValueError('Invalid selected/saturated witness state.')
    best=(-1,None)
    for u in(0,1):
        states={0:(0,())}
        for j in range(p):
            options=local_options((w>>(2*j))&3,(sat>>(2*j))&3,u,j==0)
            nxt={}
            for used,(value,masks)in states.items():
                for extra,(score,mask)in options.items():
                    if used+extra<=1 and(used+extra not in nxt or value+score>nxt[used+extra][0]):
                        nxt[used+extra]=(value+score,masks+(mask,))
            states=nxt
        for value,masks in states.values():
            score=value+w.bit_count()+u
            if score>best[0]:best=(score,(u,masks))
    return best


def selected_set(p_left,p_right,left,right,L,R):
    Q=set();total=p_left+p_right
    for first,w,(u,masks)in((0,left,L),(p_left,right,R)):
        for j,mask in enumerate(masks):
            Q.update(6*(first+j)+a for a in range(4)if mask>>a&1)
        Q.update(6*(first+a//2)+4+a%2 for a in range(2*len(masks))if w>>a&1)
        if u:Q.add(6*total+(first!=0))
    return Q


def exact(p_left,p_right,adj):
    validate(p_left,p_right,adj)
    reverse=[sum(1<<a for a in range(2*p_left)if adj[a]>>b&1)for b in range(2*p_right)]
    best=-1;witness=None;rows=[]
    for left in range(1<<(2*p_left)):
        allowed=0;satR=0
        for b,mask in enumerate(reverse):
            hits=(mask&left).bit_count()
            if hits<=1:allowed|=1<<b
            if hits==1:satR|=1<<b
        right=allowed;row_best=-1;row_right=0;pairs=0
        while True:
            satL=0;valid=True
            for a,mask in enumerate(adj):
                if left>>a&1:
                    hits=(mask&right).bit_count()
                    if hits>1:valid=False;break
                    if hits:satL|=1<<a
            if valid:
                L=wing(p_left,left,satL);R=wing(p_right,right,satR&right)
                value=L[0]+R[0];pairs+=1
                if value>row_best:row_best=value;row_right=right
                if value>best:
                    best=value;witness=selected_set(p_left,p_right,left,right,L[1],R[1])
            if right==0:break
            right=(right-1)&allowed
        rows.append({'left':left,'allowed_right':allowed,'feasible_pairs':pairs,'cap':row_best,'argmax_right':row_right})
    assert witness is not None
    return {'beta':best,'attaining_set':sorted(witness),'rows':rows}


def basis_adjacency(q):
    if q not in(5,6):raise ValueError('Only the two certified basis sizes are used.')
    n=2*q;offset=q-1 if q%2 else q
    return [sum(1<<((a+d)%n)for d in range(q-1)) | ((1<<((a+offset)%n))if a%2==0 else 0)for a in range(n)]


def degree_adjacency(p):
    if type(p)is not int or p<5:raise ValueError('Degree parameter p>=5 required.')
    n=2*p;offset=p-1 if p%2 else p
    return [sum(1<<((a+d)%n)for d in range(p-1)) | ((1<<((a+offset)%n))if a%2==0 else 0)for a in range(n)]


def degree_fixture(p):
    adj=degree_adjacency(p);g,S=graph(p,p,adj);n=12*p+2
    Q={6*j+a for j in range(2*p)for a in((0,1,3)if j<p else(1,2,4,5))}
    return {'order':n,'p_left':p,'p_right':p,'adjacency_masks':adj,
            'edges':[[a,b]for a in range(n)for b in sorted(g[a])if a<b],
            'selected':sorted(S),'attaining_set':sorted(Q),'safe_port_edge':[5,6*p+5],
            'beta':7*p,'selected_gap':p,'minimum_degree':2,'maximum_degree':p+1}


def cyclic_lift(p,k):
    if type(k)is not int or k<1:raise ValueError('Positive integer lift size required.')
    fixture=degree_fixture(p);n=fixture['order'];a0,b0=fixture['safe_port_edge']
    g=[set()for _ in range(n*k)]
    edges={tuple(e)for e in fixture['edges']}-{(a0,b0)}
    for j in range(k):
        for a,b in edges:g[n*j+a].add(n*j+b);g[n*j+b].add(n*j+a)
        a=n*j+a0;b=n*((j+1)%k)+b0
        g[a].add(b);g[b].add(a)
    S={n*j+v for j in range(k)for v in fixture['selected']}
    Q={n*j+v for j in range(k)for v in fixture['attaining_set']}
    return g,S,Q
