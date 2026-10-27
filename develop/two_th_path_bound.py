"""Two disjoint non-direct TH paths, with actual-edge capacities retained.

This is a relaxation of full matching completion, not a full TH optimizer.
An optional sink quota requires at least one path to end at a named centre.
"""
from strip_tree_compensation import edge, mates
from check_mixed_terminal_compensation import neighbours
from check_residual_reserve_cost_profile import Network
from exposable_source_completion import solve_exposable_sources


def two_path_relaxation(board, m, t, weights=None, centres=None):
    board=set(board); m={edge(a,b) for a,b in m}; t=set(t)
    mm=mates(board,m); p=set(mm); q=board-p
    if not t<=q or any(sum(v)%2!=1 for v in t):
        raise ValueError('White unoccupied sources required')
    weights={e:1 for e in m} if weights is None else {edge(a,b):c for (a,b),c in weights.items()}
    if weights.keys()!=m or any(type(c) is not int or c<0 for c in weights.values()):
        raise ValueError('Nonnegative integer weights required')
    black_q={v for v in q if sum(v)%2==0}
    if centres is not None:
        centres=set(centres)
        if not centres<=black_q:raise ValueError('Centres must be black Q vertices')
    net=Network(); source=('source',); sink=('sink',); outer=('outer-quota',)
    net.nodes.update(board|{source,sink})
    for v in sorted(t):net.add(source,v,1,tag=('source',v))
    if centres is not None:net.add(outer,sink,1,tag=('outer-quota',))
    for v in sorted(black_q):
        end=sink if centres is None or v in centres else outer
        net.add(v,end,1,tag=('terminal',v))
    for e in sorted(m):
        a,b=e
        if sum(a)%2:a,b=b,a
        net.add(a,b,1,weights[e],('M',e))
    for a in sorted(v for v in board if sum(v)%2):
        for b in sorted(neighbours(a)&board):
            e=edge(a,b)
            # No direct source-to-terminal path: every unit must cross M.
            if e not in m and not (a in t and b in black_q):
                net.add(a,b,1,tag=('N',e))
    value=cost=0
    while value<2:
        extra=net.augment(source,sink)
        if extra is None:break
        value+=1;cost+=extra
    potential=net.potentials()
    residual=[(e['u'],e['v'],e['cap'],e['cost']) for e in net.edges if e['cap']]
    used=[e for e in net.edges[::2] if e['initial']>e['cap']]
    successor={e['u']:e for e in used if e['u'] in board}
    assert len(successor)==sum(e['u'] in board for e in used)
    starts=sorted(e['tag'][1] for e in used if e['tag'][0]=='source')
    paths=[];occupied=set();paid=set()
    for start in starts:
        path=[start];actual=set();v=start
        while v not in black_q:
            assert v not in occupied;occupied.add(v)
            e=successor[v]
            if e['tag'][0]=='M':actual.add(e['tag'][1])
            v=e['v'];path.append(v)
        assert v not in occupied;occupied.add(v)
        assert actual and not actual&paid;paid|=actual
        paths.append(dict(vertices=path,actual=actual,cost=sum(weights[e] for e in actual)))
    assert len(paths)==value
    assert sum(weights[e] for e in paid)==cost  # Any unused circulation has cost zero.
    if centres is not None and value==2:
        assert any(path['vertices'][-1] in centres for path in paths)
    side=net.reachable(source) if value<2 else None
    cut=sum(e['initial'] for e in net.edges[::2] if side is not None and e['u'] in side and e['v'] not in side)
    if side is not None:assert sink not in side and cut==value
    return dict(minimum=cost if value==2 else None,value=value,paths=paths,
                potential=potential,residual_arcs=residual,cut_side=side,cut_capacity=cut if side is not None else None,
                node_count=len(net.nodes),arc_count=len(net.edges)//2,
                requires_centre=centres is not None)


def certify_two_path_bound(board,m,t,parts,centres,weights=None):
    base=solve_exposable_sources(board,m,t,parts,centres,weights)
    if any(neighbours(h)&base['T'] for h in base['centres']):
        raise ValueError('Two-path dichotomy requires no direct selected neighbour at any centre')
    pair=two_path_relaxation(base['board'],base['M'],base['T'],base['weights'],base['centres'])
    upper=base['normal_form_optimum']; f2=pair['minimum']
    # None denotes +infinity, never an arbitrary finite sentinel.
    candidates=[v for v in (upper,f2) if v is not None]
    alternative=min(candidates) if candidates else None
    lower=max(base['source_budget'],alternative) if alternative is not None else None
    exact=upper is not None and lower==upper
    return dict(base=base,two_path=pair,lower_bound=lower,normal_form_upper=upper,
                global_optimum_certified=exact,minimum_TH_fee=upper if exact else None)
