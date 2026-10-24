# Original-board compensation through a neutral portal

22 October 2026. Authors: Haobo Ma and Wenlin Zhang.

The neutral-pair saturation example leaves a blank donor one tile farther
out. That particular tile need not remain a donor after feasible exterior
selections are added. This note proves a replacement: an endpoint-free
two-row corridor must retain original capacity somewhere along it, even
under arbitrary feasible exterior labels. It then controls simultaneous
routes, including perpendicular collisions. The resulting bounds concern
the precise corridor-covered class below, not all terminal grids.

The complete written theorem received an independent ACCEPT; the full
answer and exact task/session/stream checks are archived in
output/neutral-portal-strip-compensation-oracle.json. Finite computation
and Lean execution are separate evidence, not part of that written review.

## 1. A one-corner extension of the sealed-strip lemma

Let I be k>=1 consecutive physical tiles in one horizontal row band of a
feasible grid pair. Assume I is endpoint-free, its leftmost vertex column
is blank in both rows, and at least one vertex in its rightmost column
is blank. Then its ORIGINAL deficit satisfies

    D_I=2k-|T intersect I| >= 1.                         (1)

If both vertices in the rightmost column are blank, D_I>=2, recovering
the existing sealed-strip lemma. All statements permit arbitrary feasible
data outside I. Transposition and reflection give all directions.

Proof. The internal 2k-2 columns partition into k-1 disjoint shifted unit
squares. Each contains at most two selections, since three selected
corners would give one selected corner two occupied neighbors. At most
one additional selection lies in the final column. Thus |T intersect I|
is at most2k-1, or2k-2 when that entire column is blank. Shifted squares
bound this cardinality only; none is a new physical donor. QED.

There is a useful directed witness. Scan I from its blank boundary and
stop at the FIRST physical tile Q with positive original deficit. Such
a tile exists by(1). Its entry side is blank in both corners: a preceding
tile of deficit zero, whose own entry side is blank, must have both
opposite corners selected. They are adjacent and each already sees the
other, so feasibility forces both next-entry corners blank. Induction
proves the assertion. The same argument works at arbitrary corridor length.

## 2. The neutral elbow portal supplies the boundary conditions

Use the elbow, neutral pair and coordinates of
NEUTRAL_PAIR_DONOR_SATURATION.md. Retain the canonical elbow selections
other than q as ORIGINAL selections, and retain c,u,v as original
selections. Additional feasible exterior endpoints and selections are
allowed subject to the conditions explicitly stated below. In particular
this is not an invariance claim under an arbitrary exterior.

Consider the physical row band {8,9}. Set its corridor to

    columns6,...,W+3, if H=4;
    columns6,...,W+1, if H>=6.

ASSUME every physical tile of this corridor is endpoint-free in the
original configuration. This is the essential uncovered obstruction if
foreign components occupy the corridor. The corridor lengths are W/2-1
and W/2-2 respectively, hence are positive for W>=6.

Its left boundary vertices(8,6),(9,6) are blank: native c=(7,6) already
sees endpoint q, and native v=(9,5) already sees endpoint s. At H>=6,
the native inner-leg selection(9,W+2) sees endpoint(9,W+3), forcing
(9,W+1) blank. Thus(1) gives D_I>=1. At H=4, native(9,W+4) sees the
bottom-tip endpoint(8,W+4), forcing(9,W+3) blank. The vertex(8,W+3)
sees endpoints(7,W+3),(8,W+4), so cannot be selected; endpoint-freeness
makes it blank. The corridor is sealed and D_I>=2.

These are general exterior statements: they use the retained ORIGINAL
supports and endpoint-freeness, not the blank-exterior construction. They
do not require every tile individually to be a donor. The marker tile
immediately before the corridor contains s=(8,5) as an endpoint and
v=(9,5) as a native selection on its facing side. A vertical reflection
reverses this P/T order. The endpoint s identifies the neutral matching
pair that belongs to this portal.

Both lower bounds are sharp for the explicit family. Fill each corridor
tile except the last by the two selections in its right column. For
H>=6 also select the upper-right corner of the last tile. Its other
corners are blank and this selection is isolated: its north neighbor is
excluded by the native support(7,W+2), its east neighbor by(9,W+2),
and its west/south neighbors are blank. Then D_I=1. At H=4 leave the
last tile blank, giving D_I=2. All added selected pairs have only their
partner as an occupied neighbor. No endpoint or canonical support changes;
unique matching, freezing and the two completed charges1,0 persist.

Consequently a prescribed first-step donor can fail for arbitrarily long
feasible saturated prefixes. This does not assert that all other nearby
donor choices fail, or that the nearest donor has unbounded distance.

## 3. Markers prevent repeated claims from one direction

Consider any finite collection of directed corridors as above, or any
endpoint-free corridors satisfying Section1 and the following marker
conditions. Every corridor has an endpoint marker in the immediately
preceding physical tile. On that tile's facing side the two labels are
one endpoint and one original selection. Marker endpoints are distinct
between claims. Each claim requests at most one unit and scans to its
first positive-deficit tile.

**Directional injection.** At any physical donor tile Q, at most one
claim arrives from each of west,east,north,south.

Proof for eastward scans. Two claims in different row bands cannot stop
at Q. If their entry tiles coincide, opposite P/T marker orders conflict;
equal orders share the marker endpoint, contrary to distinctness. If the
entries differ, the later entry's marker tile is in the earlier claim's
endpoint-free prefix up to Q. Its endpoint contradicts endpoint-freeness.
The other three directions follow by isometry. QED.

Different portals associated to distinct completed positive elbows have
distinct marker matching pairs. Indeed a portal pair's only endpoint edge
to another piece is p--q: q's other outside neighbors are native c or
blank, and s's two other neighbors u,v are native selections. Hence one
such pair can be attached to only one positive piece. Distinct positive
pieces cannot share that pair or its marker s. This verifies the marker
injectivity for the stated source application, rather than assuming a
separate physical budget for every description of a route.

## 4. Mixed-direction allocation and the transverse obstruction

Let k_Q be the number of claims stopping at Q, and d_Q its original
deficit. Each arriving direction forces the corresponding entry side
of Q blank. Directional injection gives k_Q<=4. The complete local
capacity table is

| Arrivals | Forced blank corners | Guaranteed d_Q |
| --- | --- | --- |
| one | at least two, and Q is deficient | 1 |
| two opposite | four | 2 |
| two adjacent | at least three | 1 |
| three or four | four | 2 |

Thus always k_Q<=2d_Q. Give each claim half a unit of capacity at its
stop. At any Q the total use is k_Q/2<=d_Q, so

    number of claims N <= 2D.                            (2)

This is a fractional certificate with physically bounded usage, not an
assertion that every claim receives one integral unit. If all claims are
parallel, the only possible double arrival is opposite, and the stronger
inequality k_Q<=d_Q gives N<=D with an actual distinct-slot assignment.

For arbitrary mixed directions define the exact FIRST-STOP shortage

    C=sum_Q max(0,k_Q-d_Q).

Assign min(k_Q,d_Q) claims to distinct unit slots at each Q. Exactly N-C
claims are paid, and C<=N/2 by the same local table. Thus if the signed
nonpositive-piece surplus R is at least C, the full demand is compensated.
This uses R once; it does not also introduce lost local donors as supply.
C is the shortage of this prescribed first-stop assignment, not the
optimal shortage after rerouting to other original donors.

The factor two cannot be improved from these local stop data alone. Take
Q={2,3}x{2,3}. Put adjacent selected pairs on its west exterior side
{(2,1),(3,1)} and north exterior side{(1,2),(1,3)}, and select(3,3).
All unlisted vertices are blank and there are no endpoints. This is
feasible, the west/north sides of Q are blank, and d_Q=1 for two arrivals.
Alternatively put selected pairs on all four exterior sides and leave
Q blank: d_Q=2 for four arrivals. These are local allocation obstacles,
not positive-elbow configurations or counterexamples to the grid target.
No claim that this local sharpness is attained by the full source class
is made. Resolving these collisions using source geometry remains useful.

## 5. Concrete consequences for completed positive elbows

Assume a feasible single-terminal original pair has the accepted completed
piece decomposition and original ledger

    mn/2-|T|-|M|=D-N+R, R>=0.

Require EVERY positive piece to be a standard even W>=6,H>=4 elbow of
charge1 (additional feasible selections must be outside its receiver),
with an attached neutral pair and native supports as in Section2, in any
tile-preserving orientation. Require its displayed corridor endpoint-free.
All other pieces have nonpositive charge, whose absolute sum is R.
All canonical supports used for the corridor boundary remain original
selections. No occupied-band coverage is inferred from terminality.

Then the marker argument and Section4 prove the following bounds.

* If all corridors are parallel, |T|+|M|<=mn/2.
* In mixed directions, R>=C also suffices for that same coefficient-one
  conclusion, using the exact first-stop shortage above.
* Without that additional payment, a definite coefficient19/20 holds:

      |T|+(19/20)|M|<=mn/2.                              (3)

For(3), each positive elbow contains W+H-1>=9 matching edges. Its attached
neutral piece contains one more. These pieces are pairwise distinct, so
|M|>=10N. Combining(2)with the original ledger gives

    mn/2-|T|-|M| >= -N/2+R >= -|M|/20+R.

This proves(3), in fact with additional margin R. On this explicit
corridor-covered class,19/20 improves5/6 by7/60 in the matching
coefficient; the parallel case removes the matching loss altogether.
This is neither a universal improvement nor a claim that19/20 is optimal
for these elbows. The earlier39/41 prescribed-source bound has different
source hypotheses; the two bounds are not ordered globally.

The new geometric input is the neutral-portal adapter, its one-corner
boundary, first-stop directional injection and original-capacity collision
accounting. The shifted-square counting argument extends the existing
sealed-strip lemma; it is not claimed as a new general counting technique.

The remaining cases include foreign endpoints inside these corridors,
other positive irreducible shapes, lost native boundary supports, and
source-geometric control of transverse first-stop collisions. General
grid compensation and triple equality remain open. Finite controls and
scoped Lean lemmas supplement the general proofs above.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
