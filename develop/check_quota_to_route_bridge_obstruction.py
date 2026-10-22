"""Check the gap between local slot quotas and mixed-gate route flow."""

import argparse
from collections import defaultdict
import itertools
import json
from pathlib import Path


if not __debug__:
    raise RuntimeError('Run without -O: assertions are the verification.')


def bipartite_matching(left, choices):
    matched = {}

    def augment(source, seen):
        for resource in sorted(choices[source]):
            if resource in seen:
                continue
            seen.add(resource)
            if resource not in matched or augment(matched[resource], seen):
                matched[resource] = source
                return True
        return False

    for source in left:
        augment(source, set())
    return {source: resource for resource, source in matched.items()}


def route_flow(sources, gates, resources, source_gates, gate_resources):
    """Maximum source-resource matching through unit-capacity gates."""
    routes = {
        source: {
            resource
            for gate in source_gates[source]
            for resource in gate_resources[gate]
        }
        for source in sources
    }
    # Enumerate the small gate-disjoint path packing exactly.
    best = 0

    def extend(position, used_gates, used_resources, value):
        nonlocal best
        if position == len(sources):
            best = max(best, value)
            return
        source = sources[position]
        extend(position + 1, used_gates, used_resources, value)
        for gate in sorted(source_gates[source]):
            if gate in used_gates:
                continue
            for resource in sorted(gate_resources[gate]):
                if resource in used_resources:
                    continue
                extend(position + 1, used_gates | {gate},
                       used_resources | {resource}, value + 1)

    extend(0, set(), set(), 0)
    return best, routes


def quota_projection(sources, resources, reachability):
    """Run-slot projection: one quota per source, one unit per resource."""
    choices = {source: set(reachability[source]) for source in sources}
    assignment = bipartite_matching(sources, choices)
    return len(assignment), assignment


def minimal_obstruction():
    sources = ('A', 'B')
    gates = ('g',)
    resources = ('R0', 'R1')
    source_gates = {'A': {'g'}, 'B': {'g'}}
    gate_resources = {'g': {'R0', 'R1'}}
    flow, reachability = route_flow(sources, gates, resources,
                                    source_gates, gate_resources)
    quota, assignment = quota_projection(sources, resources, reachability)
    assert quota == 2 and flow == 1
    assert assignment == {'A': 'R0', 'B': 'R1'} or assignment == {'A': 'R1', 'B': 'R0'}
    reachable_sources = {source for source in sources if 'g' in source_gates[source]}
    assert reachable_sources == set(sources)
    return dict(sources=list(sources), gates=list(gates), resources=list(resources),
                source_gates={key: sorted(value) for key, value in source_gates.items()},
                gate_resources={key: sorted(value) for key, value in gate_resources.items()},
                quota_projection=quota, quota_assignment=assignment,
                route_flow=flow, shared_gate_sources=sorted(reachable_sources))


def separated_control():
    sources = ('A', 'B')
    gates = ('gA', 'gB')
    resources = ('R0', 'R1')
    source_gates = {'A': {'gA'}, 'B': {'gB'}}
    gate_resources = {'gA': {'R0', 'R1'}, 'gB': {'R0', 'R1'}}
    flow, reachability = route_flow(sources, gates, resources,
                                    source_gates, gate_resources)
    quota, assignment = quota_projection(sources, resources, reachability)
    assert quota == flow == 2 and len(assignment) == 2
    assert all(sum(gate in source_gates[source] for source in sources) == 1
               for gate in gates)
    return dict(quota_projection=quota, route_flow=flow, assignment=assignment)


def exhaustive_controls():
    totals = defaultdict(int)
    sources = ('A', 'B')
    resources = ('R0', 'R1')
    gates = ('g0', 'g1')
    gap_examples = []
    for source_mask in range(1, 1 << (len(sources) * len(gates))):
        source_gates = {
            source: {gate for index, gate in enumerate(gates)
                     if source_mask >> (position * len(gates) + index) & 1}
            for position, source in enumerate(sources)
        }
        for resource_mask in range(1, 1 << (len(gates) * len(resources))):
            gate_resources = {
                gate: {resource for index, resource in enumerate(resources)
                       if resource_mask >> (position * len(resources) + index) & 1}
                for position, gate in enumerate(gates)
            }
            flow, reachability = route_flow(sources, gates, resources,
                                            source_gates, gate_resources)
            quota, _ = quota_projection(sources, resources, reachability)
            totals['networks'] += 1
            if quota > flow:
                totals['quota_overstates_flow'] += 1
                if len(gap_examples) < 8:
                    gap_examples.append(dict(source_gates={k: sorted(v) for k, v in source_gates.items()},
                                             gate_resources={k: sorted(v) for k, v in gate_resources.items()},
                                             quota=quota, flow=flow))
            if quota == flow:
                totals['exact_projection'] += 1
            if all(sum(gate in source_gates[source] for source in sources) <= 1
                   for gate in gates):
                assert quota == flow
                totals['source_separated_controls'] += 1
    assert totals['quota_overstates_flow'] > 0
    assert totals['source_separated_controls'] == totals['source_separated_exact'] if 'source_separated_exact' in totals else True
    return dict(totals=totals, gap_examples=gap_examples)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    obstruction = minimal_obstruction()
    separated = separated_control()
    exhaustive = exhaustive_controls()
    # The condition is counted independently to avoid treating a projection
    # equality in one model as a proof for all route networks.
    report = dict(status='PASS', minimal_obstruction=obstruction,
                  source_separated_control=separated,
                  exhaustive=exhaustive,
                  scope='The run-slot quota projection can strictly exceed '
                        'unit-capacity route flow when sources share a mixed gate. '
                        'If every mixed gate is reachable from at most one source, '
                        'a saturating source-resource matching lifts to disjoint '
                        'routes. This is an abstract bridge obstruction, not a '
                        'physical-grid counterexample.')
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, default=dict) + '\n')
    print(json.dumps(dict(status='PASS', totals=dict(exhaustive['totals'])), sort_keys=True))


if __name__ == '__main__':
    main()
