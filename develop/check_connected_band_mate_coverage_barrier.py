"""A second all-length rational point, also satisfying local mate coverage.

Periodic substitution and the endpoint boundary patch are the general proof;
the finite length controls check its grid adapters. No optimization dependency.
"""
import argparse
from collections import Counter
from fractions import Fraction as Q
import itertools
import json
from pathlib import Path

from check_connected_band_local_relaxation import connected_cells,old_count,reduced,WINDOWS
from check_cooperative_promotion import neighbors

if not __debug__:
    raise RuntimeError('Assertions required; do not use -O.')

# Columns are t*92,o*92; do not confuse this with the preceding36-scaled point.
DATA=[((2,3),92,92),((2,5),0,92),((3,3),0,67),((3,4),56,92),((3,5),0,61),
      ((4,0),36,54),((4,1),38,56),((4,2),36,54),((4,3),47,56),((4,4),36,36),((4,5),53,56),
      ((5,0),55,56),((5,1),54,54),((5,2),49,56),((5,3),54,70),((5,4),56,56),((5,5),54,58)]
POINT={v:(Q(t,92),Q(o,92)) for v,t,o in DATA}


def check_vertex(v,ns,t,o,counts):
    c=old_count(v);d=len(ns);p=lambda u:o(u)-t(u)
    assert 0<=t(v)<=o(v)<=1
    if c>=2:assert t(v)==0
    if c>=1:assert all(t(v)+o(u)<=1 for u in ns)
    assert all(t(v)+o(a)+o(b)<=2 for a,b in itertools.combinations(ns,2))
    assert (d+c-1)*t(v)+sum(o(u) for u in ns)<=d
    assert p(v)<=c+sum(p(u) for u in ns)
    if v[0]==5:assert sum(t(u)+o(u) for u in ns|{v})<=6
    counts['exact_vertex_and_mate_coverage_checks']+=1


def period_and_boundary(counts):
    t=lambda v:POINT[reduced(v)][0];o=lambda v:POINT[reduced(v)][1]
    for v in POINT:
        check_vertex(v,{reduced(u) for u in neighbors(v)}&set(POINT),t,o,counts)
    for name,pat,b in WINDOWS:
        assert sum(t((r,c+9))+o((r,c+9)) for r,c in pat)<=b
        counts['exact_period_window_checks']+=1
    assert sum(sum(pair) for pair in POINT.values())==Q(891,46)
    assert sum(sum(POINT[v]) for v in [(4,0),(4,1),(4,5),(5,0)])==Q(101,23)
    assert POINT[5,5][1]-POINT[5,5][0]==Q(1,23)
    # Five truncated vertex types, plus the one surviving neighbour of the
    # patched bottom-right endpoint. Translation by6 gives every length.
    C=connected_cells(2);o_patched=lambda v:t(v) if v==(5,17) else o(v)
    for v in [(3,17),(4,8),(4,16),(5,7),(5,16),(5,17)]:
        check_vertex(v,set(neighbors(v))&C,t,o_patched,counts)


def finite_control(m,counts):
    C=connected_cells(m);t=lambda v:POINT[reduced(v)][0]
    o=lambda v:t(v) if v==(5,6*m+5) else POINT[reduced(v)][1]
    for v in C:check_vertex(v,set(neighbors(v))&C,t,o,counts)
    for name,pat,b in WINDOWS:
        for i in range(m):
            S={(r,c+9+6*i) for r,c in pat}
            if S<=C:assert sum(t(u)+o(u) for u in S)<=b
    value=sum(t(v)+o(v) for v in C)
    assert value==Q(891*m-204,46)
    assert value-(18*m-2)==Q(63*m-112,46)>0
    counts['finite_connected_chain_controls']+=1
    return dict(m=m,charge=str(value),gap_above_18m_minus2=str(Q(63*m-112,46)))


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True)
    args=p.parse_args();counts=Counter();period_and_boundary(counts)
    samples=[finite_control(m,counts) for m in [*range(2,17),32,64,128]]
    out=dict(status='PASS',counts=dict(counts),period_scaled_by92=[dict(site=v,t=t,o=o) for v,t,o in DATA],
        bulk_charge='891/46',omission_charge='101/23',boundary_endpoint_reduction='1/23',
        all_m_charge='(891m-204)/46',gap_above_18m_minus2='(63m-112)/46>0 for m>=2',samples=samples,
        scope='General written all-m rational witness for the previously stated local occupation/degree/star/four-window system PLUS every basic mate-coverage inequality (o_v-t_v)<=oldPCount_v+sum_neighbour(o_u-t_u). At bottom-right site seto=t; all other values periodic. Still has bulk slope891/46>18, so these local mate constraints do not suffice for any bound18m+B with fixedB. Not an actual fractional edge matching, not integer or completely frozen, and not a whole-board counterexample; joint edge capacities, integrality and boundary/freezing structure remain open. This strengthening is separate from the earlier Oracle review scope.')
    args.output.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(dict(status='PASS',counts=dict(counts),samples=samples[:2]),indent=2))


if __name__=='__main__':main()
