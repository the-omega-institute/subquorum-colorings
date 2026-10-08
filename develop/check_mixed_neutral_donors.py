#!/usr/bin/env python3
"""Finite controls for pressure-free single-tile compensation donors."""
import argparse
import hashlib
import itertools
import json
from pathlib import Path

from check_branching_interval_compensation import band_region, mixed_neutral_obstacle
from check_compensation_transport import flip_internal_squares
from check_cross_component_compensation import band_ledger, encode, witness_record
from check_pressure_bands import branching_band, local_controls
from check_residual_corridors import direct_check, graph_record, transformed
from verify_grid_five_sixths import canonical


def donor_local_controls():
    accepted = []
    for upper in itertools.product('BTP', repeat=2):
        if any(label == 'T' and upper[1-index] != 'B'
               for index, label in enumerate(upper)):
            continue
        selected = upper.count('T')
        endpoints = upper.count('P')
        for attachments in ((), (0,), (1,), (0, 1)):
            if any(upper[index] != 'P' or upper[1-index] != 'B'
                   for index in attachments):
                continue
            charge_twice = 2*selected+endpoints+len(attachments)-4
            assert selected <= 1 and charge_twice <= -2
            accepted.append(dict(labels=''.join(upper)+'/BB',
                                 upward_saturated_attachments=list(attachments),
                                 charge_twice=charge_twice))
    return dict(states=accepted, labelings_examined=9,
                scope='Necessary conditions with arbitrary upper exterior; no matching realizability inferred.')


def compatible(first, second):
    left, right = first['labels'].replace('/', ''), second['labels'].replace('/', '')
    for labels, neighbor, reflected in ((left, right, False), (right, left, True)):
        for row in range(2):
            corner = 2*row+(0 if reflected else 1)
            outside = 2*row+(1 if reflected else 0)
            if labels[corner] != 'T':
                continue
            internal = labels[2*row+1-corner % 2] != 'B'
            vertical = labels[(corner+2) % 4] != 'B'
            pressure = row == 0
            if internal+vertical+pressure+(neighbor[outside] != 'B') > 1:
                return False
    if first['exit_corners'] and second['exit_corners']:
        return False
    return True


def mixed_word_controls(max_width):
    states = local_controls()['neutral_states']
    transitions = [[index for index, second in enumerate(states) if compatible(first, second)]
                   for first in states]
    reports = []
    for width in range(1, max_width+1):
        accepted = narrow = wider_full = wider_mixed = 0
        def extend(word):
            nonlocal accepted, narrow, wider_full, wider_mixed
            if len(word) < width:
                options = transitions[word[-1]] if word else range(len(states))
                for index in options:
                    labels = states[index]['labels'].replace('/', '')
                    if not word and (labels[0] == 'T' or labels[2] != 'B'):
                        continue
                    extend(word+[index])
                return
            labels = states[word[-1]]['labels'].replace('/', '')
            if labels[1] == 'T' or labels[3] != 'B':
                return
            exits = [(position, 'R' if state['exit_corners'] == [3] else 'L')
                     for position, index in enumerate(word)
                     if (state := states[index])['exit_corners']]
            assert exits and exits[0][1] == 'R' and exits[-1][1] == 'L'
            accepted += 1
            intervals = []
            for first, second in zip(exits, exits[1:]):
                if first[1] != 'R' or second[1] != 'L':
                    continue
                interval = set(range(first[0]+1, second[0]))
                assert interval and all(not interval & old for old in intervals)
                intervals.append(interval)
                if len(interval) == 1:
                    narrow += 1
                elif all(states[word[position]]['labels'] == 'PP/PP' for position in interval):
                    wider_full += 1
                else:
                    wider_mixed += 1
            assert intervals
        extend([])
        reports.append(dict(tile_width=width, necessary_feasible_words=accepted,
                            single_tile_donors=narrow, wider_full_intervals=wider_full,
                            wider_mixed_intervals_outside_rule=wider_mixed))
    return dict(neutral_state_count=len(states), widths=reports,
                scope='Necessary label and receiving-cap conditions; general proof and global matching are separate.')


def obstacle_control(configuration):
    rows, columns, selected, matching = configuration
    endpoints = {vertex for edge in matching for vertex in edge}
    assert (3, 4) in selected and (3, 5) not in selected | endpoints
    source = band_region(0, 0, 7)
    parent = band_region(1, 1, 5)
    donor = band_region(2, 2, 1)
    reports = []
    for transpose, flip_rows, flip_columns in itertools.product((False, True), repeat=3):
        dimensions, moved_selected, moved_matching = transformed(
            *configuration, transpose, flip_rows, flip_columns)
        assert direct_check(*dimensions, moved_selected, moved_matching) == 41
        canonical(*dimensions, *encode(*dimensions, moved_selected, moved_matching))
        graph, components = graph_record(*dimensions, moved_selected, moved_matching)
        owned = set()
        charges = []
        for vertices in (source, parent, donor):
            _, moved_vertices, _ = transformed(rows, columns, vertices, [],
                                              transpose, flip_rows, flip_columns)
            ledger = band_ledger(*dimensions, moved_selected, moved_matching, moved_vertices)
            assert not owned & set(ledger['tiles'])
            owned.update(ledger['tiles'])
            charges.append(ledger['charge_twice'])
        remainder = sum(graph['deg'][tile]-2*graph['r'][tile]
                        for tile in range(graph['N'])
                        if tile not in owned and graph['t'][tile] < 2)
        assert charges == [2, 0, -2] and remainder == -2
        assert sum(charges)+remainder == 2*(41-42)
        source_component = next(item for item in components if item['excess'] == 1)
        donor_tile = next(iter(ledger['tiles']))
        donor_component = next(item for item in components if donor_tile in item['tiles'])
        assert donor_component['excess'] == -1
        assert not set(source_component['tiles']) & set(donor_component['tiles'])
        reports.append(dict(dimensions=dimensions, charge_twice=charges,
                            remainder_charge_twice=remainder, max_capacity=max(graph['r'])))
    return reports


def wide_mixed_obstacle():
    from check_residual_corridors import corridor
    _, columns, selected, matching = corridor(8)
    labels = ['PP/BP', 'PB/PT', 'TB/BP', 'TB/BT',
              'BT/TB', 'BT/PB', 'BP/TP', 'PP/PB']
    for tile_column, state in enumerate(labels, start=1):
        for index, label in enumerate(state.replace('/', '')):
            if label == 'T':
                selected.add((2+index//2, 2*tile_column+index % 2))
    matching.extend((((2, 2), (2, 3)), ((2, 4), (3, 4)),
                     ((2, 15), (3, 15)), ((2, 16), (2, 17)),
                     ((3, 3), (4, 3)), ((3, 7), (4, 7)),
                     ((3, 12), (4, 12)), ((3, 16), (4, 16))))
    selected.update({(4, 0), (5, 1), (4, 19), (5, 18),
                     (4, 2), (5, 3), (4, 6), (5, 7),
                     (4, 13), (5, 12), (4, 17), (5, 16),
                     (4, 8), (5, 9), (4, 11), (5, 10),
                     (5, 5), (5, 14)})
    return 6, columns, selected, matching


def wide_obstacle_controls(configuration):
    rows, columns, selected, matching = configuration
    assert len(selected) == 32 and len(matching) == 27
    regions = [band_region(0, 0, 10), band_region(1, 1, 8),
               band_region(2, 4, 2), band_region(2, 2, 1), band_region(2, 7, 1)]
    reports = []
    for transpose, flip_rows, flip_columns in itertools.product((False, True), repeat=3):
        dimensions, moved_selected, moved_matching = transformed(
            *configuration, transpose, flip_rows, flip_columns)
        assert direct_check(*dimensions, moved_selected, moved_matching) == 59
        canonical(*dimensions, *encode(*dimensions, moved_selected, moved_matching))
        claimed = set()
        charges = []
        for region in regions:
            _, moved_region, _ = transformed(rows, columns, region, [],
                                             transpose, flip_rows, flip_columns)
            ledger = band_ledger(*dimensions, moved_selected, moved_matching, moved_region)
            assert not claimed & set(ledger['tiles'])
            claimed.update(ledger['tiles'])
            charges.append(ledger['charge_twice'])
        assert charges == [2, 0, 0, -2, -2]
        graph, components = graph_record(*dimensions, moved_selected, moved_matching)
        remainder = sum(graph['deg'][tile]-2*graph['r'][tile]
                        for tile in range(graph['N']) if tile not in claimed and graph['t'][tile] < 2)
        assert remainder == 0
        assert sorted(component['excess'] for component in components) == [-1, -1]+[0]*6+[1]
        reports.append(dict(dimensions=dimensions, charge_twice=charges,
                            remainder_charge_twice=remainder))
    return reports


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--max-word-width', type=int, default=8)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if not 3 <= args.max_word_width <= 9:
        parser.error('--max-word-width must lie between 3 and 9')
    configuration = mixed_neutral_obstacle()
    obstacle_images = obstacle_control(configuration)
    wide_configuration = wide_mixed_obstacle()
    wide_images = wide_obstacle_controls(wide_configuration)
    flips = []
    for limit in (1, configuration[0]*configuration[1]):
        changed, swaps = flip_internal_squares(configuration, limit)
        assert swaps > 0
        images = obstacle_control(changed)
        assert max(item['max_capacity'] for item in images) == 2
        flips.append(dict(swaps=swaps, symmetry_images=len(images)))
    branching = []
    for branches in range(1, 17):
        config = branching_band(branches)
        direct_check(*config)
        parent = band_ledger(*config, band_region(1, 1, 4*branches-1))
        assert parent['charge_twice'] == 0
        donors = [band_ledger(*config, band_region(2, 4*index+2, 1))
                  for index in range(branches)]
        assert all(donor['charge_twice'] <= -2 for donor in donors)
        tiles = [tile for donor in donors for tile in donor['tiles']]
        assert len(tiles) == len(set(tiles))
        branching.append(dict(branches=branches, terminal_charge_twice=sum(
            donor['charge_twice'] for donor in donors)))
    root = Path(__file__).resolve().parents[1]
    sources = [Path(__file__), root/'docs/MIXED_NEUTRAL_DONORS.md']
    sources.extend(Path(__file__).with_name(filename) for filename in (
        'check_branching_interval_compensation.py', 'check_compensation_transport.py',
        'check_cross_component_compensation.py', 'check_pressure_bands.py',
        'check_residual_corridors.py', 'verify_grid_five_sixths.py',
        'verify_grid_short_path_compensation.py'))
    report = dict(status='ALL_CHECKS_PASSED', local=donor_local_controls(),
                  words=mixed_word_controls(args.max_word_width),
                  obstacle_symmetry_images=obstacle_images, capacity_two_flips=flips,
                  branching_controls=branching,
                  obstacle=witness_record('Mixed-neutral obstacle compensated by capped donor', configuration),
                  wide_obstacle_symmetry_images=wide_images,
                  wide_obstacle=witness_record('Closed wide mixed successor has zero charge', wide_configuration),
                  sha256={str(path.relative_to(root)): hashlib.sha256(path.read_bytes()).hexdigest()
                          for path in sources},
                  scope='Finite controls of the written lemmas and covered-class theorem. Wide mixed intervals and general grid inequality remain open. No Lean run.')
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({key: value for key, value in report.items()
                      if key not in ('obstacle', 'wide_obstacle', 'sha256')}, indent=2))


if __name__ == '__main__':
    main()
