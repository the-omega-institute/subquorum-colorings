"""Fast direct check of the literal 40P/51T intrinsic-gap fixture.

Does not call the paired-board or gap-suppression constructor.
"""
import argparse
import json
from pathlib import Path

from check_compensation_flow_normal_form import owner_data
from check_frozen_shared_mixed_gate import check_rank_certificate
from check_frozen_tip_slot_obstruction import independent_strands
from check_interval_connector_cycles_and_missing_ports import whole_bands
from check_merger_completion_reserves import feasible, frozen
from check_whole_support_fork_normal_form import whole_support_data, ordinary_flow, contract, optimize
from check_whole_support_fork_flow import fork_flow

if not __debug__:raise RuntimeError('Run without -O.')


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
    raw=json.loads(Path('develop/fixtures/frozen_intrinsic_one_unit_gap.json').read_text())
    cur=(*raw['shape'],set(map(tuple,raw['selected'])),[tuple(map(tuple,e)) for e in raw['matching']])
    layers=[[tuple(v) for v in layer] for layer in raw['strict_rank_layers']]
    assert feasible(cur) and frozen(cur);check_rank_certificate(cur,layers)
    bands=whole_bands(cur);data,meta,_=whole_support_data(cur,bands)
    kinds,parts=independent_strands(cur,bands)
    assert kinds==data[0] and {frozenset(p) for p in data[1]}=={tips for tips,_ in parts if tips}
    assert len(cur[2])==51 and len(cur[3])==20 and len(data[4])==125
    assert 2*len(cur[3])==40 and len({v for e in cur[3] for v in e})==40
    C=[tuple(map(tuple,e)) for e in raw['initial_locked_links']]
    records=[];comparisons=0
    for mask in range(4):
        kept=[e for i,e in enumerate(C) if mask>>i&1];model=contract(data,kept)
        expected=(2-max(0,len(kept)-1),2-len(kept))
        for forks in (False,True):
            flow=fork_flow(*model) if forks else ordinary_flow(*model)
            primitive=optimize(*model,allow_forks=forks)
            assert (flow['value'],flow['cost'])==(primitive['value'],primitive['cost'])==expected
            comparisons+=1
        records.append(dict(kept_links=len(kept),payment=expected[0],additional_links=expected[1]))
        if mask==3:
            owner,aa,_,_=owner_data(*model[:2])
            assert len(aa)==2
            pool=set().union(*(model[3][a] for a in aa))
            assert len(pool)==1 and next(iter(pool)) in data[4]
            assert meta['intervals'][next(iter(pool))]==raw['shared_original_interval']
            assert all(model[3][a]==pool for a in aa)
    report=dict(status='PASS',literal_shape=cur[:2],endpoints=40,selected=51,
        all_available_original_units=125,shared_units_reachable_by_locked_alphas=1,
        strict_rank_layers=len(layers),kept_subset_optima=records,
        independent_primitive_comparisons=comparisons,
        scope='One literal configuration, reconstructed without the family constructor; full-pool ordinary/full and independent primitive comparisons. General parameter theorem is written separately.')
    args.output.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))


if __name__=='__main__':main()
