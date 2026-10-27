"""Two ordinary matching exposures couple HH sources and exterior ports.

This solves the specified one-paid-centre/direct-exterior normal form.
It certifies the true TH optimum when its upper bound meets the source budget;
strictly positive costs also give an exact budget-attainment criterion.
"""
from collections import deque
from shared_source_exact_completion import _shortest_relay
from strip_tree_compensation import edge,mates,physical_state_linear
from check_mixed_terminal_compensation import neighbours,selected_feasible


def surplus_exposure(left,right,adjacency):
    """Standard augmenting matching and all exposable vertices on surplus side.

    Right has exactly one more vertex. No recursive search or sentinel weights.
    Return None if the left side cannot be saturated.
    """
    left=set(left);right=set(right)
    if len(right)!=len(left)+1:raise ValueError('Right side must have surplus one')
    adj={a:set(adjacency.get(a,())) for a in left}
    if any(not ns<=right for ns in adj.values()):raise ValueError('Invalid bipartite adjacency')
    lm={};rm={}
    for start in sorted(left):
        todo=deque([start]);seen={start};parent={};end=None
        while todo and end is None:
            a=todo.popleft()
            for b in sorted(adj[a]):
                if b in parent:continue
                parent[b]=a
                if b not in rm:end=b;break
                c=rm[b]
                if c not in seen:seen.add(c);todo.append(c)
        if end is None:continue
        b=end
        while True:
            a=parent[b];old=lm.get(a);lm[a]=b;rm[b]=a
            if old is None:break
            b=old
    if len(lm)!=len(left):return None
    exposed=next(iter(right-rm.keys()));reverse={b:set() for b in right}
    for a in left:
        for b in adj[a]:reverse[b].add(a)
    reached={exposed};todo=deque([exposed]);parent_left={};parent_right={}
    while todo:
        b=todo.popleft()
        for a in sorted(reverse[b]):
            if lm[a]==b or a in parent_left:continue
            parent_left[a]=b;c=lm[a]
            if c not in reached:
                reached.add(c);parent_right[c]=a;todo.append(c)
    return dict(left=left,right=right,adjacency=adj,matching=lm,exposed=exposed,
                exposable=reached,parent_left=parent_left,parent_right=parent_right)


def expose_matching(data,target):
    if target not in data['exposable']:raise ValueError('Target is not exposable')
    result=data['matching'].copy();b=target
    while b!=data['exposed']:
        a=data['parent_right'][b];new=data['parent_left'][a];result[a]=new;b=new
    assert result.keys()==data['left'] and set(result.values())==data['right']-{target}
    assert all(b in data['adjacency'][a] for a,b in result.items())
    return result


def _reachable_pads(centre,p,mm,pads):
    allowed=p|{centre}|pads;seen={centre};todo=[centre]
    while todo:
        v=todo.pop()
        if v in pads:continue
        options={mm[v]} if sum(v)%2 else (neighbours(v)&allowed)-({mm[v]} if v in mm else set())
        for z in options:
            if z not in seen:seen.add(z);todo.append(z)
    return seen&pads


def solve_exposable_sources(board,m,t,parts,centres,weights=None):
    board=set(board);m={edge(a,b) for a,b in m};t=set(t);parts=[set(p) for p in parts];centres=list(centres)
    mm=mates(board,m);p=set(mm);q=board-p;r=len(parts)
    if not r or len(centres)!=r or len(set(centres))!=r:raise ValueError('One distinct centre per core required')
    owner={v:i for i,part in enumerate(parts) for v in part}
    if set(owner)!=p or sum(map(len,parts))!=len(p):raise ValueError('Core parts must partition P')
    if any(owner[a]!=owner[b] for a,b in m):raise ValueError('An actual edge crosses cores')
    if any(owner[v]!=owner[z] for v in p for z in neighbours(v)&p):raise ValueError('P cores must be nonadjacent')
    if any(h not in q or sum(h)%2 for h in centres):raise ValueError('Centres must be black Q vertices')
    if any(not (neighbours(h)&p)<=part for part,h in zip(parts,centres)):raise ValueError('A centre touches another core')
    if not t<=q or any(sum(v)%2!=1 for v in t) or not selected_feasible(p,t):raise ValueError('Feasible white T required')
    white_q={v for v in q if sum(v)%2};holes=white_q-t
    if len(holes)!=r-1:raise ValueError('Exactly r-1 white HH sources required')
    if len(white_q)*2!=len(q):raise ValueError('Equal Q colour populations required')
    weights={e:1 for e in m} if weights is None else {edge(a,b):c for (a,b),c in weights.items()}
    if weights.keys()!=m or any(type(c) is not int or c<0 for c in weights.values()):raise ValueError('Nonnegative integer weights required')
    outside=q-set(centres)-holes;black_out={v for v in outside if sum(v)%2==0}
    outer=surplus_exposure(black_out,t,{v:neighbours(v)&t for v in black_out})
    if outer is None:raise ValueError('The direct outer graph must saturate its black side')
    rho=[];sigma=[];paid_relays=[];gamma={z:set() for z in holes}
    for i,(part,h) in enumerate(zip(parts,centres)):
        pads={z for v in part|{h} for z in neighbours(v)&white_q}
        reach=_reachable_pads(h,part,mm,pads)
        if not reach&t:raise ValueError('Every centre needs a finite TH relay')
        rho.append(_shortest_relay(h,part,reach&t,mm,weights)['cost'])
        good=reach&t&outer['exposable']
        relay=_shortest_relay(h,part,good,mm,weights) if good else None
        paid_relays.append(relay);sigma.append(relay['cost'] if relay else None)
        for z in reach&holes:gamma[z].add(i)
    source=surplus_exposure(holes,set(range(r)),gamma)
    if source is None:raise ValueError('HH source graph must saturate all r-1 sources')
    roots=source['exposable'];lower=min(rho[i] for i in roots)
    possible={i for i in roots if sigma[i] is not None}
    chosen=min(possible,key=lambda i:(sigma[i],i)) if possible else None
    upper=sigma[chosen] if chosen is not None else None
    strict=all(c>0 for c in weights.values()) and all(c>0 for c in rho)
    result=dict(board=board,M=m,T=t,parts=parts,centres=centres,white_holes=holes,weights=weights,
                outer=outer,source=source,source_adjacency=gamma,eligible_roots=roots,
                rho=rho,sigma=sigma,source_budget=lower,normal_form_optimum=upper,paid_core=chosen,
                budget_attained=upper==lower,strict_positive_hypotheses=strict,
                budget_attainment_decided=(upper==lower or strict),auxiliary=None,state=None)
    if chosen is None:return result
    assignment=expose_matching(source,chosen);th=paid_relays[chosen];relays=[th]
    for z,i in sorted(assignment.items()):relays.append(_shortest_relay(centres[i],parts[i],{z},mm,weights))
    used=set();n=set()
    for relay in relays:
        assert not used&relay['actual'];used|=relay['actual'];path=relay['path']
        n.update(edge(path[j],path[j+1]) for j in range(0,len(path)-1,2))
    n|=m-used
    direct=expose_matching(outer,th['path'][0]);n|={edge(a,b) for a,b in direct.items()}
    state=physical_state_linear(board,m,n,t)
    assert state['paid']==th['actual'] and sum(weights[e] for e in state['paid'])==upper
    assert state['data']['counts'][0]==0 and state['data']['counts'][1]==r-1
    result.update(auxiliary=n,state=state,HH_assignment=assignment,TH_relay=th,relays=relays)
    return result
