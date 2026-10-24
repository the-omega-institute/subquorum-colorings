#!/usr/bin/env python3
"""Controls for terminal-free pruning, one-color injections and remote donors."""
import argparse
import hashlib
import json
from pathlib import Path

from check_compensation_transport import nested_corridor
from check_residual_corridors import direct_check, graph_record
from check_strand_switches import build
from check_terminal_strands import decompose, prune_cycles
from verify_grid_short_path_compensation import pairs


def incidence_components(current, region):
    graph, _ = graph_record(*current)
    pending = set(region)
    result = []
    while pending:
        start = min(pending)
        component = {start}
        queue = [start]
        while queue:
            tile = queue.pop()
            for neighbor, _ in graph['neighbors'][tile]:
                if neighbor in region and neighbor not in component:
                    component.add(neighbor)
                    queue.append(neighbor)
        pending -= component
        result.append(component)
    return result


def color_compensation(current, region):
    applicable = 0
    assignments = 0
    for component in incidence_components(current, region):
        record = build(current, component)
        colors = {color for (kind,color),count in record['colors'].items() if kind in ('L','P') and count}
        if len(colors) > 1:
            continue
        applicable += 1
        assert record['debt'] == 0 and record['terminal']['shortage_twice'] <= 0
        targets = set()
        for strand in record['strands']:
            if strand['kind'] in ('LS','PS'):
                assert not (set(strand['ends']) & targets)
                targets.update(strand['ends'])
                assignments += 1
        assert sum(count for (kind,_),count in record['colors'].items() if kind in ('L','P')) == sum(
            strand['kind'] in ('LS','PS') for strand in record['strands'])
    return applicable, assignments


def prune_and_compare(current, region, record):
    deleted = {frozenset(map(tuple, edge)) for cycle in record['cycles'] for edge in cycle['matching']}
    inserted = [tuple(map(tuple, edge)) for cycle in record['cycles'] for edge in cycle['auxiliary']]
    changed = (*current[:3], [edge for edge in current[3] if frozenset(edge) not in deleted]+inserted)
    prune_cycles(current, region, record)
    after = decompose(changed, region)
    assert after['counts'] == record['counts']
    assert after['reserve'] == record['reserve'] and after['unpaired'] == record['unpaired']
    assert not after['cycles']
    assert {frozenset(map(tuple,path['vertices'])) for path in after['paths']} == {
        frozenset(map(tuple,path['vertices'])) for path in record['paths']}
    if record['terminal']['ports'] == record['terminal']['positive_zero_leaves'] == record['unpaired'] == 0:
        graph, _ = graph_record(*changed)
        assert all(graph['deg'][tile] == 0 for tile in region)
        assert sum(graph['r'][tile] for tile in region) == record['reserve']
    return len(deleted)


def exhaustive():
    reports = []
    for rows,columns in ((2,2),(2,4),(4,2),(2,6),(6,2)):
        feasible = regions = colored = assignments = cycles = removed = terminal_free = 0
        for mask,matching in pairs(rows,columns):
            current = rows,columns,{divmod(vertex,columns) for vertex in range(rows*columns) if mask >> vertex & 1}, [tuple(divmod(vertex,columns) for vertex in edge) for edge in matching]
            graph, _ = graph_record(*current)
            deficient = [tile for tile in range(graph['N']) if graph['t'][tile] < 2]
            for mask in range(1,1 << len(deficient)):
                region = {tile for index,tile in enumerate(deficient) if mask >> index & 1}
                count,injections = color_compensation(current, region)
                colored += count
                assignments += injections
                record = decompose(current,region)
                if record['cycles']:
                    cycles += len(record['cycles'])
                    removed += prune_and_compare(current,region,record)
                terminal_free += record['terminal']['ports'] == record['terminal']['positive_zero_leaves'] == record['unpaired'] == 0
                regions += 1
            feasible += 1
        reports.append(dict(shape=[rows,columns],feasible_pairs=feasible,regions=regions,
                            one_color_incidence_components=colored,injected_terminals=assignments,
                            cycles=cycles,removed_edges=removed,terminal_free_regions=terminal_free))
    return reports


def negative_fixture():
    current = 4,4,set(),[((1,1),(1,2)),((1,3),(2,3)),((2,2),(2,1)),((2,0),(1,0))]
    region = set(range(4))
    direct_check(*current)
    record = decompose(current,region)
    assert record['reserve'] == 4 and not record['paths'] and record['terminal']['charge_twice'] == -8
    assert prune_and_compare(current,region,record) == 4
    return dict(shape=[4,4],selected=[],matching=current[3],reserve=4,charge=-4)


def remote_controls():
    reports = []
    for depth in range(1,41):
        current = nested_corridor(2*depth,depth)
        direct_check(*current)
        graph, _ = graph_record(*current)
        region = {tile for tile in range(graph['N']) if graph['t'][tile] < 2}
        record = decompose(current,region)
        assert record['counts']['LL'] == record['counts']['SS'] == 1
        assert record['reserve'] == 0
        assert all(record['counts'][kind] == 0 for kind in ('LP','LS','PP','PS'))
        source, = [path for path in record['paths'] if path['kind']=='LL']
        donor, = [path for path in record['paths'] if path['kind']=='SS']
        source_tiles = {(row//2,column//2) for row,column in source['vertices']}
        donor_tiles = {(row//2,column//2) for row,column in donor['vertices']}
        distance = min(abs(first[0]-second[0])+abs(first[1]-second[1]) for first in source_tiles for second in donor_tiles)
        assert distance == depth
        assert len(current[2]) == 2+2*depth*(depth+1)
        assert len(current[3]) == 2*(depth+1)*(depth+2)-2
        assert direct_check(*current) == current[0]*current[1]//2
        reports.append(dict(depth=depth,shape=current[:2],selected=len(current[2]),matching=len(current[3]),
                            LL=1,SS=1,reserve=0,donor_distance=distance))
    return reports


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output',type=Path,required=True)
    args = parser.parse_args()
    report = dict(status='ALL_CHECKS_PASSED',exhaustive=exhaustive(),negative_terminal_free_fixture=negative_fixture(),remote_controls=remote_controls())
    root = Path(__file__).resolve().parents[1]
    sources = [Path(__file__),root/'docs/TERMINAL_PRUNING_AND_COLOR_COMPENSATION.md']
    sources.extend(Path(__file__).with_name(name) for name in ('check_compensation_transport.py','check_strand_switches.py','check_terminal_strands.py','check_residual_corridors.py','verify_grid_short_path_compensation.py'))
    report['sha256'] = {str(path.relative_to(root)):hashlib.sha256(path.read_bytes()).hexdigest() for path in sources}
    report['scope'] = 'Independent finite controls of reviewed general color/pruning claims and previously proved all-depth transport; no universal grid proof or new Lean result.'
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({key:report[key] for key in ('status','exhaustive')}))


if __name__ == '__main__':
    if not __debug__:
        raise RuntimeError('Run without -O: verification uses assertions.')
    main()
