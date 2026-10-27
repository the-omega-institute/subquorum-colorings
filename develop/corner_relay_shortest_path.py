"""Exact weighted completion for the new corner-square family under ANY rematching."""
from heapq import heappush, heappop
from zero_defect_long_relay import long_extension_obstacle
from strip_tree_compensation import edge, mates, physical_state_linear
from check_mixed_terminal_compensation import neighbours


def solve_shortest_relay(k, m=None, weights=None):
    f=long_extension_obstacle(k);board=f['board'];p=f['P'];h=f['centre'];line=f['core']['line']
    m=f['M'] if m is None else {edge(a,b) for a,b in m}
    mm=mates(board,m)
    if set(mm)!=p: raise ValueError('Rematching must cover exactly the original endpoint footprint')
    weights={e:1 for e in m} if weights is None else {edge(a,b):c for (a,b),c in weights.items()}
    if weights.keys()!=m or any(type(c) is not int or c<0 for c in weights.values()):
        raise ValueError('One nonnegative integer weight per actual rematching edge required')
    targets={v for v in line if sum(v)%2};allowed=p|targets|{h}
    distance={h:(0,0)};parent={};heap=[(0,0,h)];end=None
    while heap:
        cost,hops,v=heappop(heap)
        if distance[v]!=(cost,hops):continue
        if v in targets: end=v;break
        if sum(v)%2:
            options=[(mm[v],weights[edge(v,mm[v])])]
        else:
            options=[(z,0) for z in neighbours(v)&allowed if mm.get(v)!=z]
        for z,extra in options:
            candidate=(cost+extra,hops+1)
            if z not in distance or candidate<distance[z]:
                distance[z]=candidate;parent[z]=v;heappush(heap,(*candidate,z))
    assert end is not None,'A full board matching implies a relay from h to its boundary'
    # Parent order is already T-to-h, starting/ending with an N edge.
    path=[end]
    while path[-1]!=h:path.append(parent[path[-1]])
    paid={edge(path[i],path[i+1]) for i in range(1,len(path)-1,2)}
    assert paid<=m and len(path)==len(set(path))
    auxiliary=m-paid
    auxiliary.update(edge(path[i],path[i+1]) for i in range(0,len(path)-1,2))
    pos=line.index(end);assert pos%2==0
    for segment in [line[:pos],line[pos+1:]]:
        assert len(segment)%2==0
        auxiliary.update(edge(segment[i],segment[i+1]) for i in range(0,len(segment),2))
    n=f['core']['n']
    auxiliary.update(edge((r,n),(r,n+1)) for r in range(n))
    auxiliary.update(edge((n,c),(n+1,c)) for c in range(f['side']))
    state=physical_state_linear(board,m,auxiliary,f['T'])
    assert state['data']['counts'][0]==0 and state['paid']==paid
    assert sum(weights[e] for e in paid)==distance[end][0]
    return dict(auxiliary=auxiliary,path=path,minimum_TH_fee=distance[end][0],
                paid=paid,state=state,M=m,T=f['T'],weights=weights,
                reached_vertices=len(distance))
