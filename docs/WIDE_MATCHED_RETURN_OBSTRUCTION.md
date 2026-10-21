# A six-source obstruction beyond the first maximal-band length test

21 October 2026. The W10,k4 matched partial seed passed the necessary
k<=W-6 test, but the following six sources already have NO complete
extension by original U/rotor sources of arbitrary dimensions and number.
This is an explicit general noncompletion proof for a prescribed motif,
not an extrapolation of bounded UNSAT. Other matched configurations and
the unrestricted allocation/grid objectives remain open.

## 1. Fixed original sources and support model

Use the established finite complete original U/rotor model: unique original
endpoint ownership, unchanged original matching, and every original support
retained unless consumed by an endpoint. A retained support has its original
anchor as its sole occupied neighbor. All widths are even>=6 and both
independent legs even>=4. Source endpoint graphs are connected and have
no isolated endpoints. The fixed sources are

    B=U(10,8,4),   B(r,c)=(11-r,c+1),
    C=U(18,20,10), C(r,c)=(c+1,22-r),
    X=U(6,12,4),   X(r,c)=(c+2,r+3),
    E=U(14,4,4),   E(r,c)=(c+2,20-r),
    U=U(6,6,4),    U(r,c)=(18-c,r+14),
    T=U(8,8,4),    T(r,c)=(19-c,r+12).

Their original endpoint sets are pairwise disjoint. The prescribed positive
producer A and old-P producer F of the earlier eight-source seed are NOT
needed for this obstruction. We impose no bounds on additional sources.

Useful fixed endpoint segments include

    B: column11, rows7..11; rows10,11, columns2..11;
    C: row2, columns2..22;
    X: row3, columns3..15; columns3,4, rows3..8;
    E: columns19,20, rows3..16;
    U: row12, columns14..18;
    T: row11, columns12..16; columns12,13, rows11..18.

When we exclude a new consumer by these endpoints, its point of consumption
is absent from all already fixed source endpoint sets, including any earlier
forced consumers. Thus its owner differs from the blocking owners. Recurring
ownership elsewhere is allowed, but does not evade these specific exclusions.

## 2. The first consumer is rigid and negative

X's outer-bar support q=(9,3) has endpoint neighbors north X, west B and
south B. As in the maximal-band theorem, its actual consumer must be an
east U terminal; both east rotor forms collide with B/X. The stem bound
g<=W-4=6 and exclusion of the downward bar hold independently of k.
An upward bar with g<=k=4 hits X's far leg, so evenness forces g=6.

Write its width s and other leg t. The upward frame is

    Q=U(s,6,t), Q(r,c)=(10-c,9-r).

If s>=8 its bar includes (3,9), on X's near stem. Hence s=6. If t>=6,
its far stem contains (4,4), on X's bar. Hence t=4. Therefore the actual
consumer is the precise original source

    Q=U(6,6,4), Q(r,c)=(10-c,9-r).

Its supports at q are (9,2),(10,3), both B-owned. Its fixed tile phase
is negative charge -1; it is not a positive activation receipt. We only
use its occupied endpoints below. Q's bar is rows4..9, columns8,9; its
far stem is row4,columns5..9 and near stem row9,columns3..9.

## 3. A forced consumer at v=(4,10)

v is X's original inner support at intrinsic (7,2). Besides its X anchor
(3,10), it has Q endpoint (4,9) as a neighbor. Hence v must be consumed.
It lies in none of the fixed endpoint sets or Q. Its own neighbors can
only be east/south. The original catalogue leaves east/south U terminals,
the two outer-corner orientations, or four rotor tips.

All four rotors are excluded. The two east footprints contain respectively
offsets (-1,1),(-1,2), hitting X at (3,11),(3,12). The two south footprints
contain respectively (2,-1),(1,-1), hitting Q at (6,9),(5,9).

A south terminal has incident length j=4: j>=6 hits B at (10,10).
Its bar lies in rows7,8. A left bar hits Q at (8,9), and a right bar
hits B at (8,11). Thus no south terminal is possible.

A vertical-bar outer corner with neighbors east/south has bar columns10,11
and extends at least to row9; it hits B at (7,11). For a horizontal-bar
outer corner, its incident south leg is exactly4, since length>=6 hits
B at (10,10). Its original beyond-tip support is then (9,10). That point
has FOUR occupied endpoint neighbors: (8,10) from the corner, (9,9) from
Q, and (9,11),(10,10) from B. None of those owners owns (9,10), and
no other prescribed source does either. A consumer would have no possible
own endpoint neighbor, contradicting the catalogue. Thus no corner survives.

The remaining possibility is an east terminal with incident j and bar width
s. Its stem is row4,columns10..j+10. E at (4,19) gives j<=8. An upward
bar contains a C endpoint on row2; hence the bar points down:

    P=U(s,j,t), P(r,c)=(c+3,j+10-r).

If s>=10 its bar reaches U's row12 segment, at column14,16 or18 for
j=4,6 or8. Thus s<=8. If s=8, its far stem is row11; for j=4,6 the
bar itself hits T there, and for j=8 the far stem reaches T's (11,16)
because t>=4. Hence s=6. Its far stem lies on row9 and must avoid B's
(9,11), giving t<=j-2. The three surviving forms are exactly

    P6=U(6,6,4), P8a=U(6,8,4), P8b=U(6,8,6),

all with the displayed downward frame. This is an all-dimension reduction:
the bounds derive from fixed endpoints, not a search cutoff.

## 4. P6 and P8b leave the next support without a consumer

w=(10,12) is T's original outer-bar support. It has anchor (11,12) and
B neighbor (10,11), so it must be consumed. It is in none of the fixed
or newly forced endpoint sets. For P6 and P8b its north neighbor (9,12)
is a P endpoint. Thus its only possible own neighbor is east.

The two east rotor forms hit P at (9,13) or T at (11,13). For an east
U terminal with incident j', E's (10,19) gives j'<=6. A downward bar
with j'=4 hits T at (11,16); with j'=6 it hits U at (12,18).
An upward bar with j'=4 hits P at (9,16). With j'=6 it also hits P8b
at (9,18), excluding that entire P8b case.

Only P6 with an upward bar and j'=6 remains. Its bar columns are17,18.
If its width s'>=10, it hits C at (2,18), hence s'<=8. For s'=6 its
far stem on row5 reaches P6 at (5,16), because its other leg is>=4.
For s'=8 its far stem on row3 reaches X at (3,15). Thus P6 is impossible
as well, at arbitrary additional widths and far-leg lengths.

## 5. P8a forces a final corner and a sealed two-by-two interior

For P8a, w still has fixed west B and south T neighbors, but north is
not P-owned. Its only possible own neighbors are north/east.

All four rotor tips collide: the two north forms contain (-1,-1) or
(-2,-1), hitting B at (9,11),(8,11); both east forms contain (-1,2),
hitting P8a at (9,14).

For an east U terminal, E gives incident j'<=6. Either upward bar hits
P8a's row9 stem at column16 or18; downward bars hit T at (11,16) or
U at (12,18). For a north terminal, the stem must stop before X's row3,
so its incident length is4 or6. A rightward bar reaches P8a column17;
a leftward bar hits B at (7,11) for length4 or Q at (5,9) for length6.
No terminal remains.

There are two outer corners with north/east own neighbors. A horizontal
bar to the east contains (9,17), a P8a endpoint. The vertical-bar corner
has its bar going north, and must have width6: width>=8 hits X at (3,12).
Its row5 leg has length4, since length>=6 hits P8a at (5,17). Its row10
leg has length4 or6, since length>=8 hits E at (10,19). Consequently
its only possible original endpoint frames are

    N=U(6,4,t), N(r,c)=(c+4,r+12), t in {4,6}.

Both contain (10,16), and neither contains (11,17).

Now the ENTIRE boundary of D=[9,12]x[16,19] consists of endpoints:

    top: P8a at columns16..18, E at column19;
    bottom: U at columns16..18, E at column19;
    left: P8a at row9, N at row10, T at row11, U at row12;
    right: E at every row9..12.

The strict interior is {10,11}x{17,18}, a two-by-two square. T's original
beyond-tip support z=(11,17) lies there; it has T anchor (11,16) and
U neighbor (12,17). It must be consumed and is not an endpoint of any
fixed owner, P8a, Q or either N.

Any OTHER original source with an endpoint at z is confined to the strict
interior: a path in its connected endpoint graph cannot cross the fixed
endpoint boundary without sharing a different owner's original endpoint.
No permitted U fits in two rows/columns (minimum span5 in each axis),
and no rotor fits either (span4 in each axis). Fixed N may occupy part
of the interior when t=6; this does not allow it to own z or allow any
foreign source to cross the boundary. Thus z has no consumer. This
excludes both final corners and finishes the six-source noncompletion proof.

## 6. Scope and verification

Every step permits arbitrarily many additional sources of arbitrary dimensions.
Forbidden overlaps are with persistent original endpoints, and each consumer's
distinction from blocker owners is checked at its forced support point.
The proof asserts no source-count minimality and excludes neither all matched
f=j+2 returns nor all maximal-width Vcorner configurations. It supplies no
extra activation or reserve; impossible claims contribute zero.

Finite role controls PASS: the six fixed sources have 200 distinct endpoints;
the successive U role catalogues have 1, 7 and then 0/2/0 shapes, with no
rotor consumers. Both final enclosure cases pass. Widths 6..26 and independent
legs 4..26 are controls of the written reductions, not general exhaustion.
The three P alternatives have charge -5 and supply no positive receipt.

All 11 scoped declarations pass standalone Lean 4.33.0, final session82611
exit0, with individual axiom inspection: only propext, Classical.choice and
Quot.sound, no sorry/native axioms. Before execution the authorized local Mac
had 49% free memory and no real lean/lake processes by comm basename. Earlier
heartbeat and Decidable-synthesis failures were repaired and are not passes.
These declarations certify the stated local support/endpoint, dimension,
boundary and span facts; the catalogue, complete role reductions and connected
confinement argument remain written.

Independent written audit268280ee ACCEPTS the arbitrary-dimension proof,
including owner exclusions and the interior endpoints in the t=6 case.
Its 15991-character response exactly matches original stream74482 exit0 and
the completed task API, with [DONE], observed gpt_6/pro. It does not certify
execution, source minimality, all matched returns or the full research target.
See [review](../output/wide-matched-return-review-response.md),
[review receipt](../output/wide-matched-return-review.json),
[formal receipt](../output/wide-matched-return-formal-check.json), and
[finite controls](../output/wide-matched-return-controls.json).

The earlier51096-candidate UNSAT only motivated the analysis; the proof above
does not use it. A separate four-source seed search is also bounded only and
does not prove a four-source obstruction.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
