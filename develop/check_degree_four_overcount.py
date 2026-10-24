"""Independent physical checks of the coarse-tax obstruction and exact budget."""

import argparse
import itertools
import json
from pathlib import Path

from check_component_receivers import verify_terminal
from check_cooperative_promotion import neighbors, occupied_degrees
from check_degree_three_fusion import inspect, phase_images
from degree_four_overcount import opposed_bands, opposed_band_certificate
from rotor_networks import combine, transform_module


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def check_ordered_certificate(current, certificate):
    mates = {endpoint: partner for edge in current[3]
             for endpoint, partner in (edge, edge[::-1])}
    earlier = set()
    for endpoint, first, second in certificate:
        assert endpoint in mates and endpoint not in earlier
        assert first != second and mates[endpoint] not in (first, second)
        assert {first, second} <= set(neighbors(endpoint))
        assert all(witness in current[2] or witness in mates and mates[witness] in earlier
                   for witness in (first, second))
        earlier.add(endpoint)
    assert earlier == set(mates)
    return len(earlier)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    controls = []
    images = []
    alignments = []
    for width, height in itertools.product((6, 8, 14, 40), (4, 6, 8, 20, 80)):
        current, modules = opposed_bands(width, height)
        report = inspect(current, modules, allow_degree_four=True)
        frozen = check_ordered_certificate(current, opposed_band_certificate(width, height))
        assert [module['charge'] for module in modules] == [1-width, 1]
        assert report['endpoints'] == 4*width+4*height+4 == frozen
        assert report['selected'] == 2*height+4
        assert report['matching_edges'] == 2*width+2*height+2
        assert report['receiver_tiles'] == 3*width//2+2*height+2
        assert report['receiver_selected'] == 2*height+4
        assert report['actual_charge'] == 2-width
        assert report['degree_four_endpoints'] == 2*height+4
        assert report['new_aligned_faces'] == report['intratile_degree_four_defect'] == 0
        assert report['marked_positive_modules'] == 1
        assert report['negative_module_mass'] == width-1
        assert report['certified_slack_lower_bound'] == width-2
        assert report['contact_edges'] == 2*height+4
        expected_degree_four = {(row, column) for row in range(1, height, 2) for column in (1, width)}
        expected_degree_four |= {(row, column) for row in range(0, height+1, 2)
                                for column in (0, width+1)}
        expected_degree_four |= {(height+1, 1), (height+1, width)}
        assert {point for point, degree in occupied_degrees(current).items() if degree == 4} == {
            (row+1, column+1) for row, column in expected_degree_four}
        actual_slack = report['half_area']-report['objective']
        assert actual_slack == height*(width-4)//2+2
        ledger = verify_terminal(current)
        assert ledger['empty_deficit'] == (width-4)*(height-2)//2
        coarse_holds = report['degree_four_endpoints'] <= width-1
        assert coarse_holds == (2*height+5 <= width)
        controls.append(dict(width=width, height=height, coarse_criterion_holds=coarse_holds,
                             exact_slack=actual_slack, empty_deficit=ledger['empty_deficit'], **report))
        for row_phase, column_phase in itertools.product(range(2), repeat=2):
            moved = [transform_module(module, (False, False, False),
                                      (1+row_phase, 1+column_phase)) for module in modules]
            network = combine(moved)
            points = network['endpoints'] | network['selected']
            rows = 2*(max(row for row, column in points)//2+1)
            columns = 2*(max(column for row, column in points)//2+1)
            record = inspect((rows, columns, network['selected'], network['matching']),
                             moved, allow_degree_four=True)
            expected = {
                (0, 0): ([1, -width-1], height+2, 2*height+4, 0, width+1, width+1),
                (0, 1): ([-1, -width-1], 0, 2, 0, width+2, width),
                (1, 0): ([1-width, -1], height, 2*height+2, 0, width, width-2),
                (1, 1): ([1-width, 1], 0, 0, 1, width-1, width-2)
            }[row_phase, column_phase]
            assert [module['charge'] for module in moved] == expected[0]
            assert tuple(record[key] for key in ['new_aligned_faces', 'intratile_degree_four_defect',
                                                'marked_positive_modules', 'negative_module_mass',
                                                'certified_slack_lower_bound']) == expected[1:]
            alignments.append(dict(width=width, height=height, phase=(row_phase, column_phase), **record))
        for symmetry, phase, offset, image, moved in phase_images(modules):
            record = inspect(image, moved, allow_degree_four=True)
            images.append(dict(width=width, height=height, symmetry=symmetry, phase=phase,
                               coarse_criterion_holds=record['degree_four_endpoints'] <=
                               record['negative_module_mass']+2*record['new_aligned_faces'], **record))
    result = dict(status='PASS', scope='Finite coordinate and ordered-witness controls; all-width conclusions have separate written proofs.',
                  physical_controls=controls, phase_symmetry_images=images, alignment_controls=alignments,
                  summary=dict(controls=len(controls), images=len(images), alignments=len(alignments),
                               coarse_failures=sum(not control['coarse_criterion_holds'] for control in controls),
                               image_coarse_failures=sum(not image['coarse_criterion_holds'] for image in images),
                               fine_failures=sum(image['certified_slack_lower_bound'] < 0 for image in images)))
    arguments.output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result['summary']))


if __name__ == '__main__':
    main()
