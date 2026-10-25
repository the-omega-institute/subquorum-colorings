"""Nonvacuous actual beta-fork embeddings and the same-N sharp tax controls."""
import argparse
from collections import Counter
import json
from pathlib import Path

from check_canonical_band_coarsening import check_coarsening, canonical_bands, vertical_segments
from check_crossing_matching_ports import rectangle
from check_degree_changing_bent_completions import compile_model
from check_forced_mates_and_adjacent_maxima import configuration
from check_frozen_beta_support_fork import fixture
from check_mixed_terminal_defect import port_graph, mixed_regions
from check_whole_support_fork_normal_form import primitive_certificates

if not __debug__:
    raise RuntimeError('Assertions required; no -O.')


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--output', type=Path, required=True)
    args = p.parse_args()
    totals, records = Counter(), []
    cur, _ = fixture()
    R, C = cur[:2]
    for cut in (8, 10, 12):
        fine = [rectangle(0, R, 0, cut), rectangle(0, R, cut, C)]
        data, _, _ = compile_model(cur, fine)
        primitives = primitive_certificates(*data)
        forks = [x for x in primitives if x['kind'] == 'fork']
        assert forks and all(len(set(x['entries'])) == 2 for x in forks)
        totals['actual_two_entry_beta_fork_embeddings'] += len(forks)
        check_coarsening(cur, fine, totals, independent=True, withdrawal=True, port=True)
        records.append(dict(cut=cut, old_forks=len(forks)))
    for w, k in ((8, 1), (8, 2), (14, 3), (32, 7)):
        cur = configuration(w, k)
        fine = vertical_segments(*cur[:2], set())
        coarse = canonical_bands(*cur[:2], fine)
        old, oc = port_graph(cur, fine)
        new, nc = port_graph(cur, coarse)
        for rec in (old, new):
            assert (rec['alpha'], rec['beta'], rec['mixed'], rec['raw'], rec['slack']) == (k, k, k*(w//2-2), 2*k, 2*k)
            assert rec['d4'] == rec['seam'] == rec['cross_direction_M'] == 0
        assert (old['value'], old['deficit'], old['boundary']) == (0, k, 2*k)
        assert (new['value'], new['deficit'], new['boundary'], new['cost']) == (k, 0, 0, 0)
        assert oc['partner'] == nc['partner']
        # In this family the positive singleton physical cell sets themselves
        # survive unchanged, an additional property beyond the general bijection.
        def cells(cert):
            bands = [b for r in cert for b in r['bands']]
            return {frozenset(v for q in range(j[1], j[2]+1) for v in bands[j[0]][q])
                    for j in compile_model(cur, cert)[0][4]}
        assert cells(fine) == cells(coarse)
        totals['sharp_same_N_no_seam_tax_controls'] += 1
        records.append(dict(w=w, k=k, fine=old, canonical=new))
        # A genuine direction interface remains after canonicalization.
        original_mixed = mixed_regions(w, k)
        mixed, _ = port_graph(cur, original_mixed)
        normalized, _ = port_graph(cur, canonical_bands(*cur[:2], original_mixed))
        assert mixed == normalized
        assert (mixed['boundary'], mixed['seam'], mixed['cross_direction_M'], mixed['deficit']) == (0, 2*k, 2*k, k)
        totals['genuine_mixed_seam_deficit_retained_controls'] += 1
    args.output.write_text(json.dumps(dict(status='PASS', counts=dict(totals), records=records,
        purpose='Nonvacuity: actual two-source beta forks with distinct BP entries embed, and fully frozen T* has unchanged physical original units and N while the full deficit drops k to0 without seams.'), indent=2)+'\n')
    print(json.dumps(dict(status='PASS', counts=dict(totals)), indent=2))


if __name__ == '__main__':
    main()
