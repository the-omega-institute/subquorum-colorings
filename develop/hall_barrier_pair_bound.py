"""Canonical exterior Hall barrier and physical source/sink pair quotas.

All flow costs are relaxations of complete TH expense. A separate matching
test certifies, or gives a Hall obstruction to, a fixed-path completion with
every remaining TH path direct. No actual M capacity is copied.
"""
from collections import deque
from check_mixed_terminal_compensation import edge,mates,neighbours
from check_residual_reserve_cost_profile import Network
from strip_tree_compensation import physical_state_linear
from two_th_path_bound import certify_two_path_bound,two_path_relaxation


def quota_pair_relaxation(board,m,t,weights,source_groups,sink_groups):
    board=set(board);m={edge(a,b) for a,b in m};t=set(t)
    p=set(mates(board,m));q=board-p;black={v for v in q if sum(v)%2==0}
    sg=list(map(set,source_groups));eg=list(map(set,sink_groups))
    if len(sg)!=2 or len(eg)!=2 or sg[0]&sg[1] or eg[0]&eg[1]:
        raise ValueError('Two disjoint source groups and two disjoint sink groups required')
    if sg[0]|sg[1]!=t or not t<=q or any(sum(v)%2!=1 for v in t):
        raise ValueError('Source groups must partition white unoccupied T')
    if not (eg[0]|eg[1])<=black:raise ValueError('Sink groups must be black Q subsets')
    weights={edge(a,b):c for (a,b),c in weights.items()}
    if weights.keys()!=m or any(type(c) is not int or c<0 for c in weights.values()):
        raise ValueError('Nonnegative integer actual weights required')
    net=Network();s=('source',);z=('sink',);net.nodes|={s,z}
    for i,group in enumerate(sg):
        collect=('source-group',i);net.add(s,collect,1,tag=('source-quota',i))
        for v in sorted(group):net.add(collect,v,1,tag=('source',v))
    for i,group in enumerate(eg):
        collect=('sink-group',i);net.add(collect,z,1,tag=('sink-quota',i))
        for v in sorted(group):net.add(v,collect,1,tag=('terminal',v))
    for e in sorted(m):
        a,b=e
        if sum(a)%2:a,b=b,a
        net.add(a,b,1,weights[e],('M',e))
    for a in sorted(v for v in board if sum(v)%2):
        for b in sorted(neighbours(a)&board):
            e=edge(a,b)
            if e not in m and not(a in t and b in black):net.add(a,b,1,tag=('N',e))
    value=cost=0
    while value<2:
        extra=net.augment(s,z)
        if extra is None:break
        value+=1;cost+=extra
    phi=net.potentials();used=[e for e in net.edges[::2] if e['initial']>e['cap']]
    successor={e['u']:e for e in used if e['u'] in board}
    assert len(successor)==sum(e['u'] in board for e in used)
    starts=sorted(e['tag'][1] for e in used if e['tag'][0]=='source')
    paths=[];owned=set();paid=set()
    for start in starts:
        path=[start];actual=set();v=start
        while v not in black:
            assert v not in owned;owned.add(v);e=successor[v]
            if e['tag'][0]=='M':actual.add(e['tag'][1])
            v=e['v'];path.append(v)
        assert v not in owned;owned.add(v)
        assert actual and not actual&paid;paid|=actual
        paths.append(dict(vertices=path,actual=actual,cost=sum(weights[e] for e in actual)))
    assert len(paths)==value and sum(weights[e] for e in paid)==cost
    if value==2:
        assert all(sum(path['vertices'][0] in group for path in paths)==1 for group in sg)
        assert all(sum(path['vertices'][-1] in group for path in paths)==1 for group in eg)
    side=net.reachable(s) if value<2 else None
    cut=sum(e['initial'] for e in net.edges[::2] if side is not None and e['u'] in side and e['v'] not in side)
    if side is not None:assert z not in side and cut==value
    return dict(minimum=cost if value==2 else None,value=value,paths=paths,potential=phi,
                residual_arcs=[(e['u'],e['v'],e['cap'],e['cost']) for e in net.edges if e['cap']],
                cut_side=side,cut_capacity=cut if side is not None else None,
                source_groups=sg,sink_groups=eg,node_count=len(net.nodes),arc_count=len(net.edges)//2)


def canonical_barrier(outer):
    """D is independent of the supplied black-saturating matching."""
    exposed=set(outer['exposable']);forbidden=outer['right']-exposed
    dark={b for b,t in outer['matching'].items() if t in forbidden}
    assert len(dark)==len(forbidden)
    neighbours_of_dark=set().union(set(),*(outer['adjacency'][b] for b in dark))
    assert neighbours_of_dark==forbidden
    assert dark=={b for b in outer['left'] if not outer['adjacency'][b]&exposed}
    return dict(exposable=exposed,forbidden=forbidden,dark=dark)


def certify_hall_barrier_bound(board,m,t,parts,centres,weights=None):
    previous=certify_two_path_bound(board,m,t,parts,centres,weights);base=previous['base']
    barrier=canonical_barrier(base['outer']);centres=set(base['centres'])
    eligible={base['centres'][i] for i in base['eligible_roots']}
    cc=two_path_relaxation(base['board']-base['outer']['left'],base['M'],base['T'],base['weights'])
    hall=quota_pair_relaxation(base['board'],base['M'],base['T'],base['weights'],
                               [barrier['forbidden'],barrier['exposable']],[eligible,barrier['dark']])
    candidates=[v for v in (base['normal_form_optimum'],cc['minimum'],hall['minimum']) if v is not None]
    lower=max(base['source_budget'],min(candidates)) if candidates else None
    assert lower is None or previous['lower_bound'] is None or lower>=previous['lower_bound']
    upper=base['normal_form_optimum'];exact=upper is not None and lower==upper
    return dict(previous=previous,base=base,barrier=barrier,two_centres=cc,Hall_pair=hall,
                lower_bound=lower,normal_form_upper=upper,global_optimum_certified=exact,
                minimum_TH_fee=upper if exact else None)


def complete_fixed_th_paths(board,m,t,paths):
    """Exact extension test: keep these TH paths, all other TH paths direct.

    Failure is a Hall obstruction for this specified extension problem only.
    It does not rule out other path pairs or extra nontrivial TH paths.
    """
    board=set(board);m={edge(a,b) for a,b in m};t=set(t);p=set(mates(board,m));q=board-p
    if not t<=q or any(sum(v)%2!=1 for v in t):raise ValueError('White unoccupied T required')
    removed=set();fixed_n=set();fixed_m=set()
    for raw in paths:
        path=list(raw)
        if len(path)<4 or len(path)%2 or len(set(path))!=len(path) or removed&set(path):
            raise ValueError('Disjoint simple nontrivial TH paths required')
        if not set(path)<=board or path[0] not in t or path[-1] not in q or sum(path[-1])%2:
            raise ValueError('Paths must run from selected white to black Q')
        if not set(path[1:-1])<=p:raise ValueError('Path interiors must lie in P')
        for i,(a,b) in enumerate(zip(path,path[1:])):
            e=edge(a,b)
            if b not in neighbours(a) or ((e in m)!=(i%2==1)):
                raise ValueError('Paths must alternate non-M and M edges')
            (fixed_m if i%2 else fixed_n).add(e)
        removed|=set(path)
    remaining=board-removed;white={v for v in remaining if sum(v)%2};black=remaining-white
    if len(white)!=len(black):raise ValueError('Balanced remaining board required')
    adj={b:{w for w in neighbours(b)&white if not(w in t and b in p)} for b in black}
    left_match={};right_match={}
    for start in sorted(black):
        todo=deque([start]);seen={start};parent={};end=None
        while todo and end is None:
            b=todo.popleft()
            for w in sorted(adj[b]):
                if w in parent:continue
                parent[w]=b
                if w not in right_match:end=w;break
                b1=right_match[w]
                if b1 not in seen:seen.add(b1);todo.append(b1)
        if end is None:
            assert set().union(set(),*(adj[b] for b in seen))==set(parent)
            assert len(parent)<len(seen)
            return dict(feasible=False,Hall_black=seen,Hall_white=set(parent),remaining=remaining,
                        fixed_actual=fixed_m,auxiliary=None,state=None)
        w=end
        while True:
            b=parent[w];old=left_match.get(b);left_match[b]=w;right_match[w]=b
            if old is None:break
            w=old
    n=fixed_n|{edge(a,b) for a,b in left_match.items()}
    state=physical_state_linear(board,m,n,t)
    assert state['paid']==fixed_m
    return dict(feasible=True,auxiliary=n,state=state,fixed_actual=fixed_m,remaining=remaining,
                Hall_black=None,Hall_white=None)


def solve_hall_barrier_completion(board,m,t,parts,centres,weights=None):
    """Certify an optimum if either the normal form or a minimum pair extends.

    A failed extension of the particular minimum pairs returned by the flow
    does not exclude other minimizing pairs. No such necessity is claimed.
    """
    result=certify_hall_barrier_bound(board,m,t,parts,centres,weights);base=result['base']
    result.update(auxiliary=base['auxiliary'],state=base['state'],completion_kind='normal_form_upper',
                  extension_attempts=[],normal_form_globally_optimal=result['global_optimum_certified'])
    if result['global_optimum_certified']:
        result['completion_kind']='normal_form_optimum';return result
    for key in ['two_centres','Hall_pair']:
        candidate=result[key]
        if candidate['minimum'] is None or candidate['minimum']!=result['lower_bound']:continue
        extension=complete_fixed_th_paths(base['board'],base['M'],base['T'],[p['vertices'] for p in candidate['paths']])
        result['extension_attempts'].append(dict(kind=key,**extension))
        if not extension['feasible']:continue
        fee=sum(base['weights'][e] for e in extension['fixed_actual'])
        assert fee==result['lower_bound']
        result.update(auxiliary=extension['auxiliary'],state=extension['state'],completion_kind=key+'_optimum',
                      global_optimum_certified=True,minimum_TH_fee=fee)
        return result
    return result
