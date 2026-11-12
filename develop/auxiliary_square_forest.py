"""All-owner auxiliary-square certificates via a rainbow forest of exchanges."""
from collections import deque
from owner_matching_certificate import components, prepare


def blocks(vertices, edges):
    adj={v:set() for v in vertices}
    for a,b in edges:adj[a].add(b);adj[b].add(a)
    unseen=set(vertices);answer=[]
    while unseen:
        root=min(unseen);part={root};todo=[root]
        while todo:
            for u in adj[todo.pop()]-part:part.add(u);todo.append(u)
        unseen-=part;answer.append(sorted(part))
    return answer


def graphic_rank(vertices, edges):
    parent={v:v for v in vertices}
    def root(v):
        while parent[v]!=v:parent[v]=parent[parent[v]];v=parent[v]
        return v
    rank=0
    for a,b in edges:
        a,b=root(a),root(b)
        if a!=b:parent[a]=b;rank+=1
    return rank


def rainbow_forest(vertices, edges):
    """Shortest augmentations, with an independently checkable rank upper cut.

    Edge records have square endpoints a,b and an owner-cycle label cycle.
    No complexity claim is used in the mathematical theorem.
    """
    vertices=list(vertices);I=set()
    while True:
        adj={v:[] for v in vertices};used={}
        for i in sorted(I):
            e=edges[i];adj[e['a']].append((e['b'],i));adj[e['b']].append((e['a'],i))
            assert e['cycle'] not in used;used[e['cycle']]=i
        exchange={i:[] for i in I};sources=[]
        for j,e in enumerate(edges):
            if j in I:continue
            parents={e['a']:None};todo=deque([e['a']])
            while todo and e['b'] not in parents:
                v=todo.popleft()
                for u,k in adj[v]:
                    if u not in parents:parents[u]=(v,k);todo.append(u)
            if e['b'] not in parents:sources.append(j)
            else:
                v=e['b']
                while parents[v] is not None:
                    v,k=parents[v];exchange[k].append(j)
        parent={j:None for j in sources};todo=deque(sources);sink=None
        while todo:
            j=todo.popleft()
            if j not in I:
                if edges[j]['cycle'] not in used:sink=j;break
                choices=[used[edges[j]['cycle']]]
            else:choices=exchange[j]
            for k in choices:
                if k not in parent:parent[k]=j;todo.append(k)
        if sink is None:
            reachable=set(parent);outside=set(range(len(edges)))-reachable
            rank=graphic_rank(vertices,[(edges[i]['a'],edges[i]['b']) for i in outside])
            colours={edges[i]['cycle'] for i in reachable}
            assert rank+len(colours)==len(I)
            return {'indices':sorted(I),'ground':edges,
                    'dual_unreachable':sorted(outside),'dual_graphic_rank':rank,
                    'dual_reachable_colours':sorted(colours),'size':len(I)}
        while sink is not None:
            if sink in I:I.remove(sink)
            else:I.add(sink)
            sink=parent[sink]
        assert len(I)==graphic_rank(vertices,[(edges[i]['a'],edges[i]['b']) for i in I])
        assert len({edges[i]['cycle'] for i in I})==len(I)


def _maximum_owner(order, cyclic, exchange=None):
    m=len(order)
    if not cyclic:return {v for j,v in enumerate(order) if j%3!=2}
    if exchange is None:
        k=(m+2)//3;gaps=[3]*k;gaps[-1]-=3*k-m;start=0
    else:
        start=next(j for j in range(m) if order[j]==exchange['x'] and order[(j+1)%m]==exchange['y'])
        if m==4:return set(order)-{order[start],order[(start+2)%m]}
        k=(m+2)//3;gaps=[3]*k;gaps[-1]=2
        if m%3==1:gaps[1]=2
        assert sum(gaps)==m
    U=set();j=start
    for gap in gaps:U.add(order[j]);j=(j+gap)%m
    assert j==start and len(U)==k
    return set(order)-U


def _select(square_ids, owner_ids, squares, owners, chosen):
    by_cycle={e['cycle']:e for e in chosen};assert len(by_cycle)==len(chosen)
    D=set()
    for i in owner_ids:
        order,cyclic=owners[i];D|=_maximum_owner(order,cyclic,by_cycle.get(i))
    adj={k:[] for k in square_ids}
    for i,e in enumerate(chosen):
        adj[e['a']].append((e['b'],i));adj[e['b']].append((e['a'],i))
    assert graphic_rank(square_ids,[(e['a'],e['b']) for e in chosen])==len(chosen)
    flips=[];visited=set();parity={k:len(D&set(squares[k]))%2 for k in square_ids}
    for root in square_ids:
        if root in visited:continue
        parent={root:None};order=[root];visited.add(root)
        for v in order:
            for u,i in adj[v]:
                if u not in parent:parent[u]=(v,i);order.append(u);visited.add(u)
        # Isolated squares are unchanged; a tree can choose all ones or one zero.
        if len(order)==1:continue
        target={v:1 for v in order}
        if sum(parity[v] for v in order)%2!=len(order)%2:target[root]=0
        need={v:parity[v]^target[v] for v in order}
        for v in reversed(order[1:]):
            p,i=parent[v]
            if need[v]:flips.append(i);need[p]^=1
        assert need[root]==0
    for i in flips:D^={chosen[i]['x'],chosen[i]['y']}
    S=set()
    for k in square_ids:
        K=squares[k];S|=max((set(K[0::2])&D,set(K[1::2])&D),key=len)
    beta=sum((2*len(owners[i][0]))//3 if owners[i][1] else (2*len(owners[i][0])+2)//3 for i in owner_ids)
    odd=sum(len(D&set(squares[k]))%2 for k in square_ids)
    assert len(D)==beta and odd>=len(chosen) and len(S)>=(beta+len(chosen)+1)//2
    return S,D,{'owner_beta':beta,'forest_edges':chosen,'flipped_edge_indices':sorted(flips),
                'odd_squares':odd,'bound':(beta+len(chosen)+1)//2}


def certificate(b,P,Q,B,colour):
    data=prepare(b,P,Q,B,colour);n=2*b;V=set(range(n));A=sorted(set(data['P']+data['Q']))
    aux=components(n,A)
    if any(not cyclic or len(K)!=4 for K,cyclic in aux):
        return {'applicable':False,'reason':'auxiliary graph is not a union of squares'}
    squares=[K for K,_ in aux];owners=data['owner_components']
    square_of={v:i for i,K in enumerate(squares) for v in K}
    owner_of={v:i for i,(K,_) in enumerate(owners) for v in K}
    small=[];removed_squares=set();removed_owners=set();S=set();D=set()
    for C in blocks(V,A+data['B']):
        sq=sorted({square_of[v] for v in C});ow=sorted({owner_of[v] for v in C})
        if len(sq) not in (1,2) or len(ow)!=len(sq) or not all(owners[i][1] and len(owners[i][0])==4 for i in ow):continue
        removed_squares.update(sq);removed_owners.update(ow)
        if len(sq)==1:
            chosen=set(squares[sq[0]][0::2]);S|=chosen;D|=chosen
            small.append({'vertices':C,'type':'coincident C4','owners':sorted(chosen),'bound':2})
        else:
            i=ow[0];K=owners[i][0]
            j=next(j for j in range(4) if square_of[K[j]]!=square_of[K[(j+1)%4]])
            x,y=K[j],K[(j+1)%4];e=dict(a=square_of[x],b=square_of[y],cycle=i,x=x,y=y)
            selection,maximum,rec=_select(sq,ow,squares,owners,[e]);assert len(selection)>=3
            S|=selection;D|=maximum
            small.append({'vertices':C,'type':'two closed C4s','owners':sorted(selection),'bound':3,'construction':rec})
    sq=[i for i in range(len(squares)) if i not in removed_squares]
    ow=[i for i in range(len(owners)) if i not in removed_owners]
    ground=[];deficit_thirds=0
    for i in ow:
        K,cyclic=owners[i]
        if not cyclic or len(K)%3==0:continue
        deficit_thirds+=2 if len(K)%6==4 else 1
        for j,x in enumerate(K):
            y=K[(j+1)%len(K)];a,c=square_of[x],square_of[y]
            if a!=c:ground.append(dict(a=a,b=c,cycle=i,x=x,y=y))
    forest=rainbow_forest(sq,ground);chosen=[ground[i] for i in forest['indices']]
    assert 3*len(chosen)>=deficit_thirds
    selection,maximum,rec=_select(sq,ow,squares,owners,chosen);S|=selection;D|=maximum
    T=set()
    for K in squares:T|=max((set(K[0::2])-S,set(K[1::2])-S),key=len)
    assert len(T)==b and not S&T and len(S)>=(n+2)//3
    assert all(not ({a,c}<=S or {a,c}<=T) for a,c in A)
    assert all(sum(v in e and set(e)<=S for e in data['B'])<=1 for v in S)
    assert all(sum(v in e and set(e)<=D for e in data['B'])<=1 for v in D)
    return {'applicable':True,'owners':sorted(S),'witnesses':sorted(T),'maximum_owner_set':sorted(D),
            'beta_I_lower':b+len(S)+len(T),'closed_components':small,'residual':rec,
            'residual_deficit_thirds':deficit_thirds,'rainbow_forest':forest}
