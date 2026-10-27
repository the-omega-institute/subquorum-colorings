"""Fixed 18x18 feasible five-core source tree and exact Hall obstruction.

All edge lists below are explicit witnesses. Enumeration was used to discover
the unit example, not to define the fixture or prove its optimality.
"""
from check_unbounded_hole_relay import family as isolated_core
from check_mixed_terminal_compensation import edge,grid,neighbours

UNIT_CENTRAL=[((0,0),(0,1)),((0,2),(1,2)),((0,3),(0,4)),((1,0),(1,1)),
              ((1,3),(2,3)),((1,4),(2,4)),((2,0),(3,0)),((2,1),(3,1)),
              ((3,2),(3,3)),((3,4),(4,4)),((4,0),(4,1)),((4,2),(4,3))]
UNIT_NW=[((0,0),(0,1)),((0,2),(0,3)),((0,4),(1,4)),((1,0),(1,1)),
         ((1,2),(1,3)),((2,0),(2,1)),((2,3),(3,3)),((2,4),(3,4)),
         ((3,0),(4,0)),((3,1),(3,2)),((4,1),(4,2)),((4,3),(4,4))]
UNIT_ARM=[((0,0),(0,1)),((0,2),(0,3)),((0,4),(1,4)),((1,0),(2,0)),
          ((1,1),(1,2)),((1,3),(2,3)),((2,1),(3,1)),((2,4),(3,4)),
          ((3,0),(4,0)),((3,2),(3,3)),((4,1),(4,2)),((4,3),(4,4))]


def branched_family(unit_rematching=False):
    origins=[(6,6),(2,0),(0,10),(10,12),(12,2)];board=grid(18,18)
    parts=[];centres=[];m=set();f=isolated_core(1)
    local=[UNIT_CENTRAL,UNIT_NW,UNIT_ARM,UNIT_ARM,UNIT_ARM] if unit_rematching else [f['M']]*5
    for (r,c),actual in zip(origins,local):
        move=lambda v:(v[0]+r,v[1]+c)
        parts.append({move(v) for v in f['P']});centres.append(move(f['h']))
        m|={edge(move(a),move(b)) for a,b in actual}
    p=set().union(*parts);q=board-p
    holes={(5,10),(6,5),(10,11),(11,6)};t={v for v in q if sum(v)%2}-holes
    chamber={(r,c) for r in range(2) for c in range(10)}|{(r,c) for r in range(2,6) for c in range(5,10)}
    black_chamber={v for v in chamber if sum(v)%2==0};white_chamber=chamber-black_chamber
    assert chamber<=q-holes-set(centres) and len(black_chamber)==len(white_chamber)==20
    assert set().union(*(neighbours(v)&t for v in black_chamber))==white_chamber
    return dict(board=board,height=18,width=18,origins=origins,parts=parts,centres=centres,P=p,M=m,T=t,
                white_holes=holes,chamber=chamber,black_chamber=black_chamber,white_chamber=white_chamber,
                cheap_edge=edge((6,8),(7,8)),cheap_source=(5,8))


def weighted_obstruction(k):
    if type(k) is not int or k<2:raise ValueError('K must be an integer at least two')
    f=branched_family();f['weights']={e:1 if e==f['cheap_edge'] else k for e in f['M']}
    return f
