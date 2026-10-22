# Horizontal boundary bands: an all-phase simultaneous budget

22 October 2026. Authors: Haobo Ma and Wenlin Zhang.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.

## Hypotheses and conclusions

Use the six-row pocket P=[0,5] x [0,N-1], N even, of
`SIX_ROW_CEILING_DESCENT.md`. The one-step old boundary is occupied by old
endpoints, with no old endpoint inside P. Every new original is an immutable
full canonical even U or standard rotor, wholly confined to P, with pairwise
disjoint endpoint sets. Retain every original support not consumed by an
actual endpoint; every retained support in P has exactly one occupied
neighbour. The full-U/rotor source decomposition is an explicit hypothesis.
It is not established for arbitrary grid configurations.

The ceiling-descent theorem excludes boundary horizontal U and proves that
the projection of every remaining horizontal H contains no foreign endpoint.
Thus the only full U types are:

* H1: width B>=6 even, bar rows1,2, sides rows1..5;
* H4: width B>=6 even, bar rows4,3, sides rows0..4;
* V: transverse U(6,d,f), even independent d,f>=4, full-height bar in
  columns b,b+1 and horizontal stems on rows0,5.

The horizontal projection is [L,R], R=L+B-1. Here L is ANY integer:
the earlier even-L restriction is removed. Rotors remain allowed unless
explicitly excluded below. Use physical tiles
tau(r,c)=(floor(r/2),floor(c/2)). Let M_i be original matching size, T_i
the number of its endpoint tiles, and S_i the number of its immutable
original supports lying in those tiles. Set

    q_i=M_i-2T_i+S_i,
    Phi(Y)=number(q_i>0)+sum_i max(0,-q_i)+2J(Y)-K(Y).

J counts tiles filled by the endpoint union but not filled by any single
original. K counts directed, emitting-source-labelled events (i,p,z):
p is an endpoint of i, z is a foreign endpoint, p and z are adjacent in
one physical tile, and z is NOT an original support of i. A consumed
original support is still an original support in this predicate.

Call an odd H/V contact band a shared physical tile column at a boundary
of an odd-L H, whose outside column belongs to a V BAR. Let c be their
number. Then, including rotors in the residual family,

    Phi(all)=Phi(V union rotors)+sum_H(B_H-1)-3c.          (1)

In particular no rotor touches an H exterior column, and adjacent H
projections have the same orientation. These facts and (1) use completeness.

If there are NO rotors, let a,b count even/odd V bar starts, p count odd
adjacent-V-bar pairs, and e count the other V-only events. The c contact
bands have distinct odd V owners, none in those p pairs and none emitting
an e event. Put u=b-2p-c. Then

    u>=0,  e<=2u,
    Phi(all)=a+5b-6p-e+sum_H(B_H-1)-3c,
    Phi(all)>=a+2b+sum_H(B_H-1)+u.                       (2)

Every H is now credited its whole negative mass B-1, even when odd-L,
because its boundary losses are paid from distinct V budgets. In particular
any such pocket containing an H has Phi>=5, so its established chamber
increment is at least10. The transverse-only nonempty sharp pocket/chamber
bounds2/7 remain unchanged. This is an extension to all horizontal column
phases of the previous rotor-free aligned-H result. It does not establish
a sign for the V/rotor residual, an exterior budget, a universal source
decomposition, or an unrestricted improvement of the global5/6 bound.

There is also a sharp obstruction to a stronger intermediate claim:
locally complete pockets can have an H marginal of -1, and batches can
have marginal -k. Thus nonnegative H marginal monotonicity is false;
the simultaneous budget (2) survives.

## No rotor on a horizontal exterior column

The accepted ceiling-descent proof gives absence of every foreign endpoint
over [L,R], without a column-parity restriction. Suppose a rotor has an
endpoint on the exterior column t=L-1. Connectedness of its endpoint
graph puts the entire rotor to the left, with maximum column t. Normalize
its left column as t-3. Its two possible endpoint shapes are

    A={(0,1),(1,1),(1,2),(1,3),(2,0),(2,1),(2,2),(3,2)},
    B={(0,2),(1,0),(1,1),(1,2),(2,1),(2,2),(2,3),(3,1)}.

With top row h in {0,1,2}, A has its unique right tip at row r=h+1,
and column t-1 has endpoints in rows r,r+1,r+2. B has its unique right
tip at row r=h+2, and column t-1 has endpoints in rows r-2,r-1,r.
In particular 1<=r<=4. These two shapes exhaust the normalized dihedral
images, independently of translation.

The H4 exterior supports on column t are rows0,2,4; the H1 supports are
rows1,3,5. Choose in the rotor's listed three-row bulk an s of the
appropriate parity, different from r: for A take s=r+2 if r already has
that parity, otherwise r+1; for B use r-2 or r-1 respectively. Then

    (s,t) is an H original support, not an endpoint of H or this rotor;
    (s,t-1) is a rotor endpoint;
    (s,t+1) is an H endpoint.

Both occupied neighbours are distinct, so retained-support completeness
forces a further actual original C to own (s,t). If t is the old boundary
instead, the presumed rotor would already violate confinement, so the
forced point is indeed inside P.

Connectedness and absence of foreign endpoints over [L,R] confine C to
columns<=t. Its rightmost endpoint column is t. Classify its type:

* An H ending at t owns every (r,t) with 1<=r<=4, including the first
  rotor's unique tip.
* A V bar containing column t also owns the first rotor's tip.
* A V stem can own (s,t) only at row0 or5. It must approach from the
  left and terminate at t, since the next column is in the forbidden H
  projection. It owns (s,t-1), already owned by the first rotor.
* A second rotor with maximum column t has a west endpoint neighbour at
  its right tip, by either normalized shape. It too owns (s,t-1).

Every possibility collides. This contradiction excludes the entire rotor,
not just its possible event direction. Horizontal reflection gives the
right exterior-column exclusion. The argument uses neither even L nor
even rotor placement.

## Adjacent horizontal projections

Disjointness of H projections is already proved in the ceiling theorem.
If an H1 on the left is immediately followed by an H4 on the right,
the right H4's support (0,R_left) lies over the left projection and is
not an endpoint of either H. It has the old boundary endpoint above it
and the right H4 endpoint beside it. Completeness forces a foreign
endpoint in the left H1 projection, contradicting the ceiling theorem.
For H4-left/H1-right the same contradiction occurs at row5 using the old
boundary below. Hence adjacent H projections have the same orientation.

## Exact source mass and boundary ledger

For either interior H orientation the matching size is B+3. When L is
even, its bar meets B/2 tile columns, both complete side legs each add
one tile, so T=B+2 and S=2. When L is odd, the bar and side footprints
give T=B+4 and S=6. Directly in both cases

    q_H=(B+3)-2T+S=1-B.

These counts are finite interval counts for every even B, with original
supports retained in S even when consumed. The positive-source term in
Phi is unchanged by adding H.

No foreign endpoint lies inside an H projection. A cross-source event
involving H must therefore cross one of its two exterior columns. Such
an edge is intratile precisely when L is odd: its left interface is
between L-1,L, and its right interface between R,R+1. For even L neither
is intratile. Nor can a mixed full tile arise wholly inside its projection.

Assume L odd. Normalize an interface as columns t,t+1 with t even.
The possibilities at the outside column exhaust the boundary ledger:

| Neighbour of H | New mixed full tiles | Directed events | 2J-K |
|---|---:|---:|---:|
| Adjacent H of the same orientation | 2 | 4 | 0 |
| Adjacent full-height V bar | 2 | 7 | -3 |
| V stem terminal | 0 | 0 | 0 |
| Rotor | impossible | impossible | -- |

Here are the actual event counts, including source labels. For H4 the
full tile rows are0,1. Each H side emits exactly on rows1,3: its foreign
neighbours on rows0,2,4 are its own original supports. Thus H/H gives
two events in each direction. H1 is the reflected case: full tile rows
1,2 and H emission rows2,4. For an H4/V interface, the V bar emits on
all five H side rows0..4, while H emits only on rows1,3. These are seven
events, not seven undirected edges; H1 reflects them to rows1..5 and2,4.
The V must face away from H, since any front stem would collide with H.

A V stem not belonging to such an adjacent bar can reach an exterior
column only as its terminal: continuing one more step would enter the
forbidden projection. Where H has an extreme-row endpoint, the two
neighbours are each other's immutable original supports, so neither
direction emits. Where H lacks that extreme row there is no adjacent
H endpoint and no new full tile.

There is no hidden three-owner full tile. An outside-column interior
endpoint must belong to an H side or a V bar: V stems occur only on
rows0,5 and rotors have been excluded. An H or V fills that entire
interior side, preventing any other owner there. In the remaining
extreme-row tile, the missing point inside the H projection cannot be
filled by a foreign endpoint. If the neighbour is an H, opposite
orientation has already been excluded. These facts rule out every
additional completion and vertical cross-owner event.

All remaining events and full mixed tiles lie entirely in the residual
V/rotor family and are unchanged on deleting H: no tile intersecting an
H endpoint was previously a residual full tile, since there were no
residual endpoints inside its projection. Enumerate each interface only
once. A tile or directed event cannot belong to two interfaces, since
each H has width>=6 and disjoint projections, and an H/H interface is
recorded once for the unordered pair. The boundary table now proves (1)
simultaneously for the entire family. Completeness after deleting H is
neither assumed nor needed for the residual inventory identity.

## Distinct V budgets pay the odd bands without reuse

Assume no rotors. The transverse-family proof gives exactly

    Phi(V)=a+5b-6p-e,

where odd adjacent-bar pairs form a matching, and every other event is
labelled injectively by an unpaired odd emitting V and row in {0,5}.
The emitting edge is on that bar's backside and targets a foreign stem
terminal. Even bars emit none of these events.

An odd-L H contact bar has odd start: on the left its start is L-2;
on the right its start is R+1. Each such V faces away from H. A V cannot
contact H on both sides, because it would have to face both ways. Hence
the c bands have c distinct odd V owners.

Such a bar cannot also be in an adjacent-V-bar pair. Its backside next
column is in the H projection, containing no V endpoint. Its front
stems would collide with an adjacent front bar. The contact bar also
emits no remaining V-only event: those events all target its backside
neighbour, which is in the H projection even at the extreme row absent
from H itself; there is no V endpoint there at all. Thus its budget is
disjoint from every paired-bar and e-event budget.

After removing these c bars and the 2p paired bars, exactly u=b-2p-c
odd bars remain, and e<=2u. Consequently

    Phi(all)>=a+5b-6p-2u+sum_H(B_H-1)-3c
             =a+2b+sum_H(B_H-1)+u.

This is an explicit simultaneous payment, not a marginal inference:
each contacted odd bar spends3 from its own mass5 and keeps2; each odd
V pair spends6 from the combined mass10 and keeps4; each other odd bar
spends at most2 and keeps at least3; each even bar keeps1. Every H keeps
its mass B-1. These four V classes are disjoint, and every tile/event
has already been assigned once. No copy of H or V surplus is reused.

## Sharp locally complete family and negative H marginals

For every even B>=6 put N=B+34 and add H1 with L=17 and width B. The
six V specifications (bar start,direction,row5 depth,row0 depth) are

    (0,+1,4,4), (5,+1,4,4), (15,-1,6,6),
    (B+17,+1,4,4), (B+22,+1,4,4), (B+32,-1,6,6).

They are pairwise endpoint-disjoint and have no endpoint over the H
projection. Here a=3,b=3,p=0,e=2,c=2,u=1. The exact inventories are

    Phi(V)=16,
    Phi(V union H)=B+9,
    Phi(V union H)-Phi(V)=B-7.

This attains (2): its right-hand side is 3+6+(B-1)+1=B+9. At B=6 the
H marginal is -1, decreasing Phi from16 to15. Each of the two H/V
bands spends3, exceeding H's mass5.

Here is a general retained-support check, not just a sample enumeration.
The terminal supports of the six V are consumed by the next bar at
depth4 or by the facing tips at columns9/10, with the translated pair
on the right behaving the same way. Supports outside the six-row strip
are consumed by the old boundary. The unconsumed V supports inside P
are exactly both rows1,4 at columns

    {3,8,11,13,B+20,B+25,B+28,B+30}.

The H has exactly two further retained supports (4,18),(4,B+15).
Its exterior supports are consumed by the adjacent V bars15/16 and
B+17/B+18; its beyond-leg supports lie on the occupied row6 boundary.
Every same-row support gap is at least2. Each listed V support has
exactly its own endpoint neighbour toward row0 or5, and each H support
has exactly its own side-leg neighbour. There is no second occupied
neighbour from a different row or the boundary. The old pocket-side
supports at rows1,4 and columns0,N-1 are consumed by the extreme V bars.
Thus the entire pocket satisfies the stated retained-support condition.
Reflection in rows gives the H4 family too. This argument works for
every even B>=6.

Juxtapose k such blocks. Their widths B+34 are even. Across a block
interface the extreme V bars have even starts, so the touching endpoint
columns belong to different physical tile columns. No new intratile
event or mixed full tile occurs; the listed retained supports and their
degrees are unchanged. With B=6 the batch inventories are16k and15k,
with H marginal -k. There is no universal lower bound on that marginal.

These are locally complete states of the actual old chamber pocket;
the executable also reconstructs the old core and checks its chamber
increment5+Phi. No whole-grid complete extension is asserted. Moreover,
deleting H need not preserve completeness. The obstruction refutes a
nonnegative-H-marginal rule even when the AFTER state is locally complete;
it refutes neither (2) nor the target global inequality.

## Verification and remaining scope

`develop/check_six_row_all_phase_horizontal.py` reconstructs immutable
endpoint/support/matching records and compares the entire labelled-event
and mixed-tile sets, not only totals. It verifies the H parity counts,
boundary ledger, distinct V owners, exclusion from other V debits, (1)
without rotors, (2), actual old-core local completeness, and exact negative
marginals. It also checks the two rotor edge shapes and all forced owner
roles in selected full-record libraries. These finite controls test the
separate general arguments above and do not replace them.

`formal/SubQuorum/SixRowHorizontalBands.lean` contains ten local theorems
and fourteen individually axiom-audited declarations. Lean checks the two
rotor shapes, unique right tip, west neighbour, parity-selected forced
support and second-rotor collision, as well as the simultaneous budget
arithmetic and sharp block/batch arithmetic. Canonical source adapters,
all-owner geometry, band/event classification, completeness and the V
owner injection remain written proofs. No full source-to-global-inequality
formalization is claimed. The final local Lean run has no warnings,
errors, sorry axioms or native evaluation.

The validation record is `output/six-row-all-phase-horizontal-validation.json`.
Independent review is recorded there when returned. Next: the genuinely
mixed V/rotor residual budget, followed by exterior contributions and a
general source decomposition. The submitted manuscript is unchanged.
