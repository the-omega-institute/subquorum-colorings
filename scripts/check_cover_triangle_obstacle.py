"""Check the explicit obstruction to unrestricted minimal-set pullback."""

import argparse
import json
from pathlib import Path

from check_regular_starforming import covered, graph_from_edges, star_lists
from explore_heawood_two_lifts import lift


def formation_witnesses(adjacency, selected):
    stars = star_lists(adjacency)
    selection = sum(1 << vertex for vertex in selected)
    witnesses = {}
    for outside in set(range(len(adjacency))) - selected:
        assert covered(stars, selection, outside)
        available = selection | (1 << outside)
        star = min(star for star in stars[outside] if star & available == star)
        witnesses[outside] = [vertex for vertex in range(len(adjacency)) if star >> vertex & 1]
    return witnesses


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    edges = [(0, 1), (0, 2), (0, 4), (1, 4), (1, 5), (3, 5), (2, 6), (3, 6)]
    adjacency = graph_from_edges(7, edges)
    selected = {0, 1, 2, 3}
    base_witnesses = formation_witnesses(adjacency, selected)
    stars = star_lists(adjacency)
    for selection in range(15):
        assert any(not covered(stars, selection, vertex)
                   for vertex in range(7) if not selection >> vertex & 1)
    failures = {0: 4, 1: 5, 2: 6, 3: 3}
    for deleted, outside in failures.items():
        assert not covered(stars, 15 ^ (1 << deleted), outside)
    cover = lift(adjacency, {(0, 4)})
    for vertex, neighbors in enumerate(cover):
        projected = [neighbor % 7 for neighbor in neighbors]
        assert len(projected) == len(set(projected))
        assert set(projected) == adjacency[vertex % 7]
    pulled = selected | {7 + vertex for vertex in selected}
    formation_witnesses(cover, pulled)
    deletion_witnesses = formation_witnesses(cover, pulled - {0})
    report = dict(scope='Explicit counterexample to unrestricted minimal-set pullback; not a counterexample to the triangle-free theorem or a numerical SF inequality.',
                  base_edges=edges, base_selection=sorted(selected),
                  proper_base_subsets_checked=15, base_star_witnesses=base_witnesses,
                  base_deletion_failures=failures, crossed_edges=[[0, 4]],
                  cover_order=14, locally_bijective=True, pullback=sorted(pulled),
                  redundant_lift=0, after_deletion_star_witnesses=deletion_witnesses)
    arguments.output.write_text(json.dumps(report, indent=2) + '\n')
    print('PASS: explicit triangular base has minimal S but nonminimal full pullback')


if __name__ == '__main__':
    main()
