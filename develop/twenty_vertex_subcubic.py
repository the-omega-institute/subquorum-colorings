"""Explicit robust block and all-order two-connected subcubic gap certificates."""
from pathlib import Path
import json

FIXTURE = Path(__file__).resolve().parent/'fixtures/twenty-vertex-subcubic-core.json'


def block():
    """Return F=H-4--12, its canonical selection, colours and optimum witness."""
    f=json.loads(FIXTURE.read_text())
    g=[set() for _ in range(20)]
    for a,b in f['edges']:
        if {a,b}=={4,12}:continue
        g[a].add(b);g[b].add(a)
    return g,set(f['selected']),[f['graph_colour'][str(v)] for v in range(20)],set(f['port_avoiding_dissociation_set'])


def cyclic_family(r):
    """G_r has r copies of F and edges4_i--12_(i+1), indices modulo r."""
    if not isinstance(r,int) or isinstance(r,bool) or r<1:
        raise ValueError('r must be a positive integer')
    base,S,col,D=block()
    g=[{20*i+u for u in base[v]} for i in range(r) for v in range(20)]
    for i in range(r):
        a,b=20*i+4,20*((i+1)%r)+12
        g[a].add(b);g[b].add(a)
    return {'g':g,'selected':{20*i+v for i in range(r) for v in S},
            'dissociation':{20*i+v for i in range(r) for v in D},
            'colour':col*r,'order':20*r,'proved_beta':11*r,
            'proved_SF_lower':12*r,'proved_gap_lower':r}
