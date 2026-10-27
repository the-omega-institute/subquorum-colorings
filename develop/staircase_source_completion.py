"""Exact weighted HH-budget attainment for an arbitrary staircase of odd cores."""
from collections import deque
from check_unbounded_hole_relay import family as isolated_core
from shared_source_exact_completion import _shortest_relay
from strip_tree_compensation import edge,grid,mates,physical_state_linear
from check_mixed_terminal_compensation import neighbours


def staircase_family(scales):
    scales=tuple(scales)
    if not scales or any(type(k) is not int or k<1 for k in scales):
        raise ValueError('A nonempty sequence of positive integer core scales is required')
    height=4*sum(scales)+2;width=4*sum(scales)+2*len(scales)
    board=grid(height,width);parts=[];centres=[];lines=[];origins=[];m=set();canonical_n=set()
    row=col=0
    for k in scales:
        f=isolated_core(k);origins.append((row,col));move=lambda v:(v[0]+row,v[1]+col)
        parts.append({move(v) for v in f['P']});centres.append(move(f['h']))
        lines.append([move(v) for v in f['line']]);actual={edge(move(a),move(b)) for a,b in f['M']};m|=actual
        relay_actual={edge(move(f['long_path'][i]),move(f['long_path'][i+1])) for i in range(1,len(f['long_path'])-1,2)}
        canonical_n|=actual-relay_actual
        for path in f['paths']:
            canonical_n.update(edge(move(path[i]),move(path[i+1])) for i in range(0,len(path)-1,2))
        row+=4*k;col+=4*k+2
    p=set().union(*parts);white_holes={lines[i][4*scales[i]] for i in range(len(scales)-1)}
    t={v for v in board-p if sum(v)%2}-white_holes
    outside=set()
    for i,(r,c) in enumerate(origins):
        n=4*scales[i]+2
        for rr in list(range(r))+list(range(r+n,height)):
            outside.update(edge((rr,cc),(rr,cc+1)) for cc in range(c,c+n,2))
    canonical_n|=outside
    return dict(scales=scales,height=height,width=width,board=board,P=p,M=m,T=t,H=board-p-t,
                parts=parts,centres=centres,lines=lines,origins=origins,white_holes=white_holes,
                ordered_white_holes=[lines[i][4*scales[i]] for i in range(len(scales)-1)],
                outside_matching=outside,canonical_C_auxiliary=canonical_n)


def staircase_outer_matching(f):
    r=len(f['scales']);matching=set(f['outside_matching'])
    for i,line in enumerate(f['lines']):
        if i==r-1:segments=[line[1:]]
        else:
            j=4*f['scales'][i];segments=[line[:j],line[j+1:]]
        for segment in segments:
            assert len(segment)%2==0
            matching.update(edge(segment[j],segment[j+1]) for j in range(0,len(segment),2))
    region=f['board']-f['P']-set(f['centres'])-f['white_holes'];start=f['lines'][-1][0]
    assert set(mates(region,matching))==region-{start}
    return region,matching,start


def expose_staircase_white(f,target):
    region,base,start=staircase_outer_matching(f)
    if target not in region or sum(target)%2!=1:raise ValueError('An outer white T vertex is required')
    mm=mates(region,base);parent={};seen={start};todo=deque([start])
    while todo and target not in seen:
        v=todo.popleft()
        choices=(neighbours(v)&region)-({mm[v]} if v in mm else set()) if sum(v)%2 else {mm[v]}
        for z in sorted(choices):
            if z not in seen:seen.add(z);parent[z]=v;todo.append(z)
    assert target in seen,'The all-size outer alternating reachability lemma reaches every white vertex'
    path=[target]
    while path[-1]!=start:path.append(parent[path[-1]])
    matching=base^{edge(a,b) for a,b in zip(path,path[1:])}
    assert set(mates(region,matching))==region-{target}
    return matching,path


def solve_staircase(scales,m=None,weights=None):
    f=staircase_family(scales);m=f['M'] if m is None else {edge(a,b) for a,b in m}
    mm=mates(f['board'],m)
    if set(mm)!=f['P']:raise ValueError('M must cover exactly the staircase endpoint footprint')
    weights={e:1 for e in m} if weights is None else {edge(a,b):c for (a,b),c in weights.items()}
    if weights.keys()!=m or any(type(c) is not int or c<0 for c in weights.values()):
        raise ValueError('Exactly one nonnegative integer weight per actual edge required')
    core={v:i for i,p in enumerate(f['parts']) for v in p}
    assert all(core[a]==core[b] for a,b in m)
    th=[_shortest_relay(centre,p,{v for u in p for v in neighbours(u)&f['T']},mm,weights)
        for p,centre in zip(f['parts'],f['centres'])]
    chosen=min(range(len(th)),key=lambda i:(th[i]['cost'],i));hh=[];assignment=[]
    for i,(p,centre) in enumerate(zip(f['parts'],f['centres'])):
        if i==chosen:continue
        hole=i if i<chosen else i-1;z=f['ordered_white_holes'][hole]
        relay=_shortest_relay(centre,p,{z},mm,weights);hh.append(relay);assignment.append((hole,i))
    assert len({h for h,i in assignment})==len(assignment)==len(f['white_holes'])
    relays=[th[chosen]]+hh;used=set()
    auxiliary=set()
    for relay in relays:
        assert not used&relay['actual'];used|=relay['actual'];path=relay['path']
        auxiliary.update(edge(path[i],path[i+1]) for i in range(0,len(path)-1,2))
    auxiliary|=m-used
    direct,exchange=expose_staircase_white(f,th[chosen]['path'][0]);auxiliary|=direct
    state=physical_state_linear(f['board'],m,auxiliary,f['T']);paid=th[chosen]['actual']
    assert state['data']['counts'][0]==0 and state['data']['counts'][1]==len(f['white_holes'])
    assert state['paid']==paid and sum(weights[e] for e in paid)==th[chosen]['cost']
    return dict(family=f,M=m,T=f['T'],weights=weights,auxiliary=auxiliary,state=state,
                rho=[p['cost'] for p in th],minimum_TH_fee=th[chosen]['cost'],paid_core=chosen,
                TH_relay=th[chosen],HH_relays=hh,HH_assignment=assignment,outer_exchange=exchange,
                source_budget_lower=th[chosen]['cost'])
