"""Discover local deletion constraints; this is not an all-size proof."""

from collections import defaultdict
from itertools import product
import json

from check_subcubic_starforming import CORE, base


ADJACENCY = base()
SUPPORT = {0: 11, 6: 3}


def local_forms(selected, external, activity):
    def active(vertex):
        return bool(ADJACENCY[vertex] & selected) or (vertex in SUPPORT and external[vertex])
    for outside in set(range(12)) - selected:
        neighbors = ADJACENCY[outside] & selected
        if outside in SUPPORT:
            if len(neighbors) + external[outside] >= 2:
                continue
            if any(active(center) for center in neighbors) or activity[outside]:
                continue
        elif len(neighbors) >= 2 or any(active(center) for center in neighbors):
            continue
        return False
    return True


def records():
    for mask in range(4096):
        selected = {vertex for vertex in range(12) if mask >> vertex & 1}
        for states in product(range(3), repeat=2):
            external = {port: int(state > 0) for port, state in zip([0, 6], states)}
            activity = {port: state == 2 for port, state in zip([0, 6], states)}
            if not local_forms(selected, external, activity):
                continue
            safe = []
            for deleted in selected & set(CORE):
                if any(port in selected and not external[port] and deleted == support
                       for port, support in SUPPORT.items()):
                    continue
                if local_forms(selected - {deleted}, external, activity):
                    safe.append(deleted)
            if not safe:
                yield dict(mask=mask, selected=sorted(selected),
                           ports=[int(port in selected) for port in [0, 6]],
                           external=list(states), core_count=len(selected & set(CORE)))


def main():
    maxima = defaultdict(int)
    dense = []
    for record in records():
        key = tuple(record['ports'] + record['external'])
        maxima[key] = max(maxima[key], record['core_count'])
        if record['core_count'] >= 7:
            dense.append(record)
    print(json.dumps(dict(maxima=[dict(ports=list(key[:2]), external=list(key[2:]),
                                      maximum_core=value) for key, value in sorted(maxima.items())],
                          dense=dense), indent=2))


if __name__ == '__main__':
    main()
