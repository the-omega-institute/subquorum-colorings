"""Selected-degree cubic completion and a fixed gap-loss family."""
from pathlib import Path
import json
from compact_subcubic_selected_stars import core

FIXTURE = Path(__file__).resolve().parent/'fixtures/cubic-completion-gap-loss.json'


def complete(g, selected, colours, edge_count=None, degree=3):
    """Fill selected degree deficits. Old outside vertices must already have the target degree."""
    if type(degree) is not int or degree < 2:raise ValueError('Target degree must be at least two')
    g = [set(q) for q in g]
    selected = set(selected)
    colours = dict(colours)
    assert all(len(q) <= degree for q in g)
    assert all(len(g[v]) == degree for v in range(len(g)) if v not in selected)
    assert all(colours[v] != colours[u] for v in range(len(g)) for u in g[v])
    demand = [sum(degree-len(g[v]) for v in selected if colours[v] == side) for side in (0,1)]
    assert (demand[0]-demand[1]) % degree == 0
    if edge_count is None:
        edge_count = demand[0] % degree
        while any((demand[side]+(degree-1)*edge_count)//degree < max([degree-len(g[v]) for v in selected if colours[v] == side]+([degree-1] if edge_count else [0])) for side in (0,1)):
            edge_count += degree
    if type(edge_count) is not int or edge_count < 0 or any((d+(degree-1)*edge_count)%degree for d in demand):
        raise ValueError('Invalid number of selected edge components')
    original_n = len(g)
    for j in range(edge_count):
        a,b = len(g),len(g)+1
        g.extend(({b},{a}));colours[a]=0;colours[b]=1;selected.update((a,b))
    new_unused = []
    for side in (0,1):
        needs = [(v,degree-len(g[v])) for v in sorted(selected) if colours[v] == side]
        total = sum(r for v,r in needs)
        count = total//degree
        if any(r > count for v,r in needs):
            raise ValueError('Too few new vertices for simple completion')
        start = len(g);g.extend(set() for _ in range(count))
        for v in range(start,start+count):colours[v]=1-side
        new_unused.extend(range(start,start+count))
        index = 0
        for v,r in needs:
            for j in range(r):
                u = start+index%count
                assert u not in g[v]
                g[v].add(u);g[u].add(v);index += 1
    return g,selected,colours,{'selected_edge_count':edge_count,'original_n':original_n,'new_unused':new_unused}


def base():
    data = json.loads(FIXTURE.read_text())
    g,S,D,col = core(4)
    g.extend(({49},{48},{51},{50}));S.update(range(48,52))
    col.update({48:0,49:1,50:0,51:1})
    for name,nb in sorted(data['new_unused_neighbourhoods'].items(),key=lambda x:int(x[0])):
        v = int(name);assert v == len(g)
        g.append(set(nb));col[v] = 1-col[nb[0]]
        for u in nb:g[u].add(v)
    return g,S,set(data['dissociation_witness']),col


def family(k, completed=True):
    if type(k) is not int or k < 1:raise ValueError('k must be a positive integer')
    if completed:g,S,D,col = base()
    else:g,S,D,col = core(4)
    n = len(g)
    h = [{n*j+u for u in g[v]} for j in range(k) for v in range(n)]
    for j in range(k):h[n*j+6].remove(n*j+30);h[n*j+30].remove(n*j+6)
    for j in range(k):
        a,b = n*j+30,n*((j+1)%k)+6
        h[a].add(b);h[b].add(a)
    return h,{n*j+v for j in range(k) for v in S},{n*j+v for j in range(k) for v in D},{n*j+v:col[v] for j in range(k) for v in col}
