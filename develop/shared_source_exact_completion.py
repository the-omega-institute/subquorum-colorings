"""Exact TH optimum for both shared-source cores under any actual rematching.

Three standard shortest alternating paths plus one outer matching exchange.
The shared white source goes to exactly one core; all other Q are completed.
"""
from collections import deque
from heapq import heappop, heappush
from shared_hole_chambers import shared_hole_chambers
from strip_tree_compensation import edge, mates, physical_state_linear
from check_mixed_terminal_compensation import neighbours


def _line(origin, n):
    r, c = origin
    return [(r+i, c+n-1) for i in range(n)]+[(r+n-1, c+i) for i in reversed(range(n-1))]


def outer_near_matching(k, short):
    """A matching of R exposing its first right-L white vertex."""
    f = shared_hole_chambers(k, short); first_n=4*k+2; second_n=4*short+2
    l1=_line((0,0),first_n);l2=_line((4*k,first_n),second_n)
    z=f['white_hole'];pos=l1.index(z);assert pos%2==0
    matching=set()
    for segment in (l1[:pos],l1[pos+1:],l2[1:]):
        assert len(segment)%2==0
        matching.update(edge(segment[i],segment[i+1]) for i in range(0,len(segment),2))
    for r in range(f['height']):
        if r<4*k:columns=range(first_n,f['width'],2)
        elif r<first_n:columns=()
        else:columns=range(0,first_n,2)
        matching.update(edge((r,c),(r,c+1)) for c in columns)
    region=f['board']-f['P']-f['centres']-{z};exposed=l2[0]
    assert set(mates(region,matching))==region-{exposed}
    return dict(family=f,region=region,matching=matching,exposed=exposed)


def expose_outer_white(data, target):
    region=data['region'];base=data['matching'];start=data['exposed']
    if target not in region or sum(target)%2!=1:raise ValueError('A white outer-Q target is required')
    mm=mates(region,base);parent={};seen={start};todo=deque([start])
    while todo and target not in seen:
        v=todo.popleft()
        options=(neighbours(v)&region)-({mm[v]} if v in mm else set()) if sum(v)%2 else {mm[v]}
        for z in sorted(options):
            if z not in seen:seen.add(z);parent[z]=v;todo.append(z)
    assert target in seen,'Written outer completion lemma reaches every white R vertex'
    path=[target]
    while path[-1]!=start:path.append(parent[path[-1]])
    flipped={edge(a,b) for a,b in zip(path,path[1:])};matching=base^flipped
    assert set(mates(region,matching))==region-{target}
    return matching,path


def _shortest_relay(centre, p, targets, mm, weights):
    """Reverse orientation: centre to a white terminal, confined to one core."""
    allowed=p|targets|{centre};distance={centre:(0,0)};heap=[(0,0,centre)];parent={};end=None
    while heap:
        cost,hops,v=heappop(heap)
        if distance[v]!=(cost,hops):continue
        if v in targets:end=v;break
        if sum(v)%2:
            options=[(mm[v],weights[edge(v,mm[v])])]
        else:
            options=[(z,0) for z in neighbours(v)&allowed if mm.get(v)!=z]
        for z,extra in options:
            candidate=(cost+extra,hops+1)
            if z not in distance or candidate<distance[z]:
                distance[z]=candidate;parent[z]=v;heappush(heap,(*candidate,z))
    assert end is not None,'Odd-square corner/boundary completion supplies a relay for every M'
    path=[end]
    while path[-1]!=centre:path.append(parent[path[-1]])
    actual={edge(path[i],path[i+1]) for i in range(1,len(path)-1,2)}
    assert len(path)==len(set(path)) and actual<=weights.keys()
    return dict(path=path,actual=actual,cost=distance[end][0])


def solve_shared_source(k, short=None, m=None, weights=None):
    short=k if short is None else short;outer=outer_near_matching(k,short);f=outer['family']
    m=f['M'] if m is None else {edge(a,b) for a,b in m};mm=mates(f['board'],m)
    if set(mm)!=f['P']:raise ValueError('Rematching must cover exactly the two original footprints')
    weights={e:1 for e in m} if weights is None else {edge(a,b):c for (a,b),c in weights.items()}
    if weights.keys()!=m or any(type(c) is not int or c<0 for c in weights.values()):
        raise ValueError('Exactly one nonnegative integer weight per actual edge required')
    first_p={v for v in f['P'] if v[1]<4*k+2};parts=[first_p,f['P']-first_p]
    centres=[f['first_centre'],f['second_centre']]
    assert all((a in parts[0])==(b in parts[0]) for a,b in m)
    th=[_shortest_relay(c,p,{v for v in f['T'] if neighbours(v)&p},mm,weights)
        for c,p in zip(centres,parts)]
    chosen=0 if th[0]['cost']<=th[1]['cost'] else 1;free=1-chosen
    hh=_shortest_relay(centres[free],parts[free],{f['white_hole']},mm,weights)
    paid=th[chosen]['actual'];used=paid|hh['actual'];assert not paid&hh['actual']
    auxiliary=m-used
    for relay in (th[chosen],hh):
        path=relay['path'];auxiliary.update(edge(path[i],path[i+1]) for i in range(0,len(path)-1,2))
    direct,exchange=expose_outer_white(outer,th[chosen]['path'][0]);auxiliary.update(direct)
    state=physical_state_linear(f['board'],m,auxiliary,f['T'])
    assert state['data']['counts'][0]==0 and state['paid']==paid
    assert sum(weights[e] for e in paid)==min(r['cost'] for r in th)
    assert len([p for p in state['data']['paths'] if p['kind']=='HH'])==1
    return dict(M=m,T=f['T'],weights=weights,auxiliary=auxiliary,state=state,
                minimum_TH_fee=min(r['cost'] for r in th),relay_costs=[r['cost'] for r in th],
                TH_relay=th[chosen],HH_relay=hh,chosen_paid_core=chosen,outer_exchange=exchange,
                source_budget_lower=min(r['cost'] for r in th))
