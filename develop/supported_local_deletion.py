"""Select a deletion whose support is internal to a finite interface block."""


def supported(g, C, ports, v):
    """Sufficient conditions; g is the block, C its selected vertices."""
    if v not in C or v in ports or not g[v]&C:
        return False
    if any(not(g[u]&(C-{v})) for u in g[v]&C):
        return False
    for x in g[v]-C:
        ns=g[x]&C
        if len(ns)>=3:
            continue
        if len(ns)!=2 or not g[next(iter(ns-{v}))]&C:
            return False
    return True


def choose(g, C, ports):
    return next((v for v in sorted(C-ports) if supported(g,C,ports,v)),None)
