# Sealed-chamber localization and an actual repair of a negative marginal

22 October 2026. Authors: Haobo Ma and Wenlin Zhang.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.

## Model and the issue after axial compensation

Use the explicit full-even-U/standard-rotor model and immutable T,H,M
inventory Phi from `ALL_EVEN_GAP_AXIAL_COMPENSATION.md`. The existence of
this source decomposition is an assumption. A support not consumed by the
endpoint union has exactly one occupied endpoint neighbour in a complete
extension. New sources have connected nearest-neighbour endpoint graphs
and disjoint endpoint sets, also disjoint from all retained endpoints.

Retain the same old family O: one outer A=U(W+2,D,F), chart(r,c-1), and
inner B_i=U(W,4,4) at increasing even bar rows a_i, every gap>=10, even
W>=6, a_0>=2, D,F>=a_(n-1)+4. Put g=n-1. The preceding theorem gives a
positive selected inventory, but says nothing about the signed marginal
of the other actual originals. Here we establish two further facts:

1. ALL new originals, including unselected ones, localize into disjoint
   sealed gap chambers or an exterior class. Their entire physical-tile
   and source-labelled-event budgets separate exactly by chamber.
2. A specified extra original can have exact marginal-1, but at a twelve-
   row gap it forces a further actual owner with exact marginal+2. This
   repairs that negative branch by+1 relative to the selected core. At
   W=8 the retained branch cannot completely extend at all.

Neither result asserts nonnegativity for arbitrary unselected originals
or proves the global5/6/grid target. The finite checks below supplement
separate general proofs.

## A connected original cannot leave its chamber

For each gap define the finite open lattice rectangle

    C_i={a_i+2,...,a_(i+1)-1} x {1,...,W}.                 (1)

Its four boundary sides are rows a_i+1 and a_(i+1), and columns0,W+1.
The upper row is the FULL inner row of B_i, including its two stem
endpoints. The lower row is B_(i+1)'s full outer row. The sides belong
to A's continuous walls. The stated depth bound supplies every boundary
point, including the four corners. Thus every boundary point is an old
endpoint. B_i's own short stems may also occupy points inside C_i;
those remain retained blockers and do not weaken the boundary argument.

If a new connected endpoint set T meets C_i, choose an endpoint inside.
Every endpoint of T is joined to it by a nearest-neighbour path in T.
If that path leaves C_i, its first step out lands on a boundary side:
a unit lattice step cannot jump over a row or column boundary. But that
point is already in T(O), contradicting endpoint disjointness. Therefore

    T intersects C_i  ==>  T is contained in C_i.           (2)

For a full U, the outer bar joins both continuous stems and the inner
bar; the entire endpoint graph is connected. The standard rotor's four
central degree-three endpoints and their terminals are connected as well.
Hence (2) applies to every permitted source at every dimension/orientation.
It is a graph-path proof, not a bounded source enumeration.

There is a stronger TILE separation. Because the a_i and W are even,
the physical tiles meeting C_i have row indices

    a_i/2+1,...,a_(i+1)/2-1

and column indices0,...,W/2. Every cell of these tiles is either inside
C_i or on one of A's two walls. None lies beyond a top/bottom boundary:
the first interior row a_i+2 is even and the last a_(i+1)-1 is odd.
An endpoint of a different NEW source in such a tile is therefore inside
C_i, because wall cells are already occupied by O. By (2) that entire
source belongs to the same chamber. Consequently new sources in two
different chambers, and chamber/exterior new sources, have disjoint
physical tile footprints. This applies to every actual original, not
just an axial owner with a previously known shape.

## Exact whole-family reduction

Let Y be ANY finite collection of additional endpoint-disjoint connected
originals. Let Y_i consist of those meeting C_i; each lies wholly inside
it. Let Y_out be the remaining originals. Define, always against the
same old inventory O,

    Delta_i=Phi(O union Y_i)-Phi(O),
    Delta_out=Phi(O union Y_out)-Phi(O).

Then the exact identity is

    Phi(O union Y)=-g+Delta_out+sum_i Delta_i.              (3)

To prove it, charges are additive per immutable original. Existing mixed
tiles and events persist. Every newly full mixed tile touching a new
source, and every new source-labelled event, has a unique physical tile.
By tile separation it touches new sources from only one Y_i or Y_out.
Its old endpoints may come from A or B_i, but this does not create another
copy of the tile or event. Partition these differences by that unique
class and sum the marginals. The even-bar ledger supplies Phi(O)=-g.
There is no uncounted old/new/new tile involving two different classes.

If the whole family is complete, its support condition at any point of
C_i is local: an adjacent new endpoint outside C_i would have to lie on
the already occupied boundary, which is impossible. Moreover original
supports of a source in Y_i are adjacent to its endpoints, so supports
outside C_i lie on the old boundary and are already consumed. Thus the
actual chamber state satisfies the inherited support conditions inside
C_i without reference to an exterior new source. We do not claim a
converse construction or that arbitrary local states extend globally.

This reduces the unselected-source question to complete chamber budgets
and the exterior budget. For example, proving Delta_i>=1 for every
complete chamber and Delta_out>=0 would suffice for nonnegative Phi in
this particular nested old family. Those inequalities are NOT proved
by (3). Nor may Delta_i be replaced by its selected-core marginal:
the next example gives a precise loss after that core was compensated.

## A genuine negative additional marginal

Fix a twelve-row gap with upper bar at even a>=2, lower at a+12,
even W>=8 and outer depths covering a+16. Normalize a=0. In addition to
the three old originals, retain

    R=U(6,4,4), chart(r,c)=(4+c,1+r),
    Z=U(6,4,4), chart(r,c)=(3+c,7-r).                     (4)

R is the rotated-corner actual-left candidate from the preceding theorem.
Their full endpoint records are

    R: rows5,10 columns1..5; rows6..9 columns1,2;
    Z: rows4,9 columns3..7; rows5..8 columns6,7.

All these endpoints and the old endpoints are pairwise disjoint. The
source charges are q_R=-5 and q_Z=-1. For Z, use the wall-aligned U
charge-1 calculation from the preceding note and the tile-preserving map
(x,y)->(4+y,7-x). Adding R to O gives marginal+2,
so Phi(O+R)=1. Adding Z creates just the mixed tile(2,2), with rows4,5
and columns4,5. The four new source-labelled events are

    R:(5,4)->Z:(4,4),       R:(9,2)->Z:(9,3),
    Z:(4,3)->R:(5,3),       Z:(4,5)->R:(5,5).

All other cross directions are in the relevant immutable H, in different
tiles, or absent. Z meets no old endpoints in a tile. Therefore

    DeltaPhi(Z | O+R)=1+2*1-4=-1,
    Phi(O+R+Z)=0.                                         (5)

This disproves monotonicity under arbitrary endpoint-disjoint additions
even AFTER an axial owner has been selected in every gap. It is a
partial-inventory counterexample to that inference, not to the complete-
family target. Whether Z can actually occur must be checked by completeness.

## Its next owner is forced and fully classified

R's immutable support z=(11,1) is absent from the retained endpoints.
Its neighbours (10,1), (11,0), (12,1) belong to R, A, and the lower B.
Hence any complete extension has an actual owner N of z with EAST the
only available internal direction. N cannot be another copy of R or Z.
A U must realize z as an east terminal, and the two standard east-terminal
rotors both hit the lower B at row12. No rotor owner is possible.

Write the U's even near horizontal depth as k>=4, even breadth as b>=6,
and far depth as f>=4. Its bar must go north; a south-going bar crosses
the lower B immediately. A near stem crossing the right wall is forbidden,
so k<=W-2. The complete candidate is

    N_b(k,f)=U(b,k,f), chart(r,c)=(12-c,1+k-r).              (6)

Its outer bar is column1+k, rows12-b..11, and inner bar is column k,
rows13-b..10. Its horizontal near stem is row11, columns1..1+k;
the far stem is row12-b, columns1+k-f..1+k. These whole-record coordinates
also carry its original supports and matching; neither is reassigned.

The exhaustive surviving parameter range is

    b=10:  even 8<=k<=W-2, even 4<=f<=k-2;
    b=6,8: even 12<=k<=W-2, even 4<=f<=k-8.               (7)

Indeed, breadth b>=12 crosses row0 inside the upper B, so only6,8,10
remain. At k=4 or6 the outer bar meets Z's full row9 at column5 or7;
thus k>=8. When b=10 its far stem is row2 and must avoid the upper B's
stem(2,1); the odd first column is therefore at least3, giving f<=k-2.
For b=6 or8 the far row is6 or4, where Z occupies column7 and intervening
points on that far stem; its odd first column must be at least9, so
f<=k-8 and k>=12. Conversely every record in (7) avoids every fixed
endpoint: the bars have columns at least9/8, the near row11 is free,
and the far row/column bounds are exactly the blockers just listed.
This proves (7) for arbitrary dimensions and all orientations.

In particular W=8 admits no N, so the FIVE retained originals O,R,Z
have no complete extension. At W=10,12 only the breadth10 family can
remain. These are necessary conditions; no complete-extension witness
is inferred from the surviving parameter list.

## Exact repair and simultaneous nonreuse

Every N in (7) has original charge-1: its chart is the tile-preserving
map (x,y)->(11-y,1+k-x) of the wall-aligned canonical U, which has charge-1
at all dimensions. Against O+R+Z it creates exactly
the three mixed tiles(5,0),(5,1),(5,2), using R's row10 and N's row11.
Its five new source-labelled events are

    R:(10,2)->N:(11,2),     R:(10,4)->N:(11,4),
    N:(11,1)->R:(10,1),     N:(11,3)->R:(10,3),
    N:(11,5)->R:(10,5).

At odd columns only N-to-R counts; at even columns only R-to-N counts,
by the alternating original lateral supports. At column1 the same mixed
tile also contains A's two wall endpoints, but is counted only once.
Neither N nor Z nor another old source creates an additional contact:
N's far stem starts at column3 or9 according to (7), and its right bar
lies strictly inside the old right wall band. Hence

    DeltaPhi(N | O+R+Z)=1+2*3-5=2,
    DeltaPhi(Z+N | O+R)=-1+2=1,
    Phi(O+R+Z+N)=2.                                       (8)

This is compensation by a new actual source forced by retained data,
not spending R's already counted surplus again. R's old events remain;
the two old-to-N events are new labelled events with a different target.
The original negative tile(2,2) and the three repair tiles are disjoint.

In several twelve-row chambers with this retained R/Z branch, each
actual N is confined by the sealed-chamber lemma. The owners, new tiles
and events used in (8) are distinct across chambers. If all g chambers
have this branch, the exact selected sequence of inventories is

    Phi(O+all R)=g,
    Phi(O+all R+all Z)=0,
    Phi(O+all R+all Z+actual N)=2g.                        (9)

Unselected remaining originals are still outside (9). Equations(3) and
(8) identify a general localization tool and a repaired negative branch;
they do not establish every chamber's complete budget or the exterior
budget. The submitted manuscript, main results and global open targets
are unchanged.

## Verification scope

The companion Python source reconstructs the full original T/H/M, checks
the exact negative/repair tile and event SETS, tests all sampled source
orientations/roles against (7), the W=8 obstruction, simultaneous batches,
and confinement/tile separation of sampled connected new sources. These
are controls of the written graph-path and exhaustive-role proofs above.
The companion Lean source proves unbounded connected-path confinement,
tile-mate localization and chamber separation, plus local parameter and
receipt/repair arithmetic. Whole-source role and complete-support adapters
remain written mathematics. No earlier independent ACCEPT covers these
new localization/repair results; the preceding general-gap review11740
completed ACCEPT with20944-character exact stream/terminal agreement,
but was submitted before this note and is separately scoped.

Final Python79185 exited0:48 transformed branch patterns,24000 U/384 rotor
roles,296 surviving normalized owners,7068 exact repair receipts,64
simultaneous batches and8 tile-preserving isometries. Localization controls
check83790 endpoint-disjoint sources in9 chambers:3624 confined sources
and80166 exterior sources with no shared chamber tile. A separate128
heterogeneous whole-inventory controls, containing5306 new sources
(4674 exterior), check the exact common-baseline full-tile/event partitions
and identity(3). Four additional width/top/depth2000 controls agree.

Final local Lean4.33.0 process19777 exited0:32 explicit abbreviations,
definitions and theorems, including23 local theorems, plus SourceWalk
individually audited. Only ordinary propext/Classical.choice/Quot.sound
or none; no warnings/sorry/native. Preflight36% memory free and no real
lean/lake by comm-basename inspection. The initial invocation20828 found
constructor-case binder mismatches; these were corrected before this
clean final run. Full source-role/charge/receipt and completeness assembly
remain written, whereas the arbitrary connected-walk and physical-tile
confinement lemmas themselves are formalized.

A distinct follow-up containing this complete note, full-record verifier
and Lean source completed ACCEPT as taskf5f62488-ec57-4023-826f-0a1a3e1bbfe5,
conversation conv_e18bcaa504addda4. Original73515 exited0/DONE with19028
response characters exactly matching the terminal API, observed gpt_6/pro.
The fresh audit confirms all-source confinement, tile/exterior separation,
inherited support locality, exact common-baseline set partitions, complete
R/Z receipts, actual N catalogue, W8 nonextension and simultaneous repair.
It requests no mathematical correction and reports fresh canonical-record
set computations plus a heterogeneous partition control. It did not rerun
Lean. See `output/sealed-chamber-negative-repair-review-terminal.json`.
The later `TEN_ROW_COMPLETE_CHAMBER_CLASSIFICATION.md` is outside this
review's scope, and no arbitrary chamber or exterior sign is inferred.
