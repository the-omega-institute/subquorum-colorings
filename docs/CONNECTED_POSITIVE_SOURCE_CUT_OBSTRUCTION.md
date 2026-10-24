# A connected positive-demand obstruction to pointwise boundary payment

20 October 2026. The source-cut rule that pays one reserve unit per necessary
restored-support omission fails even when the full endpoint graph and the
retained endpoint graph are connected, all positive sources and actual marked
sides survive, and only ONE negative original source is deleted. There is an
all-parameter family with fixed resource vector

    (A,U0,Z0,H)=(1,5,0,30), N=1, G=2, R=18,

but exact minimum relaxed omission count kappa=k/2+2 for every even k>=4.
At k=70 this gives37>36=A+U0+Z0+H. The full allocation margin is17 and the
ambient slack is623, both positive. This is an obstruction to the proposed
pointwise bridge, not to allocation or rectangular-grid equality.

## 1. Complete sources and fixed physical tiles

Use the unchanged tiles {2i,2i+1} x {2j,2j+1}. The complete canonical source
U(w,L,H) is the constructor in
[two_leg_case](../develop/check_two_leg_corner_obstruction.py): its matching
contains horizontal edges (0,c)--(0,c+1) for odd1<=c<w and
(1,c)--(1,c+1) for even2<=c<w-1, plus vertical leg edges
(r,1)--(r+1,1) and (r,w)--(r+1,w) for odd r below the respective even heights.
Its supports are (0,0),(0,w+1), the beyond-tip points (L+1,1),(H+1,w),
and the alternating exterior/even-row or interior/odd-row leg supports for
rows2 through the respective heights. No original endpoint, matching edge or
support is discarded before fusion. Supports lying in another retained
source's endpoint set are consumed; all other supports remain mandatory.

For any even k>=4 take the following eight original sources:

| Owner | Canonical source | Physical map of (r,c) | Original phase |
|---|---|---|---|
| V1 | U(8,k+4,k+2) | (r-k-2,c-1) | 01 |
| V2 | U(6,6,4) | (c+1,7-r) | 01 |
| V3 | U(k+8,8,4) | (2-c,9-r) | 01 |
| V4 | U(6,k,k) | (-r,c) | 10 |
| V5 | U(8,8,6) | (r+12,17-c) | 00, positive |
| V6 | U(6,6,4) | (c+19,r+9) | 11 |
| V7 | U(12,8,4) | (20-c,r+7) | 11 |
| V8 | U(6,4,4) | (18-r,16-c) | 11 |

The first four sources are the family F(k,8). The last four are F(4,8)
under the isometry Psi(r,c)=(r+18,16-c). The original negative charge
magnitudes are1,1,1,5,5,11,5, whose sum is29, independent of k.
V5 is the sole positive source. These source counts are not marked demand.

## 2. General feasibility and connectivity

All intervals below contain integer coordinates. The exact endpoint sets of
the first block are:

    P1={-k-2,-k-1} x [0,7]
       union [-k,2] x {0} union [-k,0] x {7};
    P2=[2,7] x {6,7} union {2} x [1,5] union {7} x [3,5];
    P3=[-k-6,1] x {8,9} union {1} x [1,7]
       union {-k-6} x [5,7];
    P4={-1,0} x [1,6] union [-k,-2] x {1,6}.

These four sets are pairwise disjoint. For example V1's stems lie outside
V4's legs; V3's long bar is in columns8,9, outside V1,V2,V4, and its near
stem in row1 lies between the bars of V4 and V2. This also separates the two
short far stems. Each original source is endpoint-connected. Contacts between
V1,V4 at (0,0)--(0,1), V4,V3 at (0,1)--(1,1), and V3,V2 at
(1,1)--(2,1) prove first-block connectivity.

Substitution in the support formula gives the ENTIRE selected set of this
block as the following disjoint families. The right column is the unique
neighbor in its full occupied set:

| Selected point or family | Unique occupied neighbor |
|---|---|
| (r,-1), even -k-2<=r<=2 | (r,0) |
| (3,0) | (2,0) |
| (3,2),(3,4) | (2,2),(2,4), respectively |
| (8,c), c=3,5,7 | (7,c) |
| (7,2) | (7,3) |
| (6,4) | (7,4) |
| (2,9) | (1,9) |
| (-k-7,c), c=5,7,9 | (-k-6,c) |
| (-k-6,4) | (-k-6,5) |
| (-k-5,6) | (-k-6,6) |
| (r,2), odd -k+1<=r<=-3 | (r,1) |
| (r,5), same odd r | (r,6) |

For the first column, the ranges above exclude every other endpoint neighbor;
successive selected points in a column differ by two, and the separated
columns and endpoint rows exclude selected-selected edges. The short end
exceptions are displayed separately, including the boundary case k=4.
This proves occupied-degree-one feasibility of every selection. Each endpoint
already has at least three neighbors in its own original occupied source;
that occupancy persists under fusion, so endpoint degrees stay at least three.
Original endpoint disjointness preserves the original matching.

The second block inherits feasibility and connectivity under Psi. The first
block's endpoints end at row7; the second block's endpoints start at row8.
Every possible cross-block adjacency is determined by this fixed seam:

| Block | Row | Endpoint columns | Selected columns before joining |
|---|---:|---|---|
| First | 6 | 6,7 | 4 |
| First | 7 | 3,4,5,6,7 | 2 |
| First | 8 | none | 3,5,7 |
| Second | 7 | none | 7,9,11 |
| Second | 8 | 7,8,9,10,11 | 12 |
| Second | 9 | 7,8 | 10 |

All other occupied points of the blocks lie at rows<=5 or rows>=10,
respectively. Exactly two seam supports are consumed: (8,7) from the first
block and (7,7) from the second. After those consumptions the table leaves
every remaining selection with its original unique occupied neighbor.
The only cross-block endpoint edge is (7,7) in V2 adjacent to (8,7) in V7.
The full family is therefore complete feasible and endpoint-connected for
EVERY even k>=4. In particular, this argument uses finite interval formulas
and a fixed seam, not extrapolation from the checker.

The exact sizes are

    |P|=6k+176, |M|=3k+88, |T|=3k/2+34.

## 3. Actual demand and one resource census

V5's canonical left marked side has witnesses (2,2),(4,2), mapping to
(14,15),(16,15); its right side has (2,7),(4,7), mapping to
(14,10),(16,10). All four points are original endpoints of V8. Each actual
side counts once, giving N=n2=1, n0=0 and G=2. Thus the demand is retained
by preserving the original positive owner V5 and the actual gate owner V8.

The positive terminal (20,16) keeps both supports (20,17),(21,16).
The other terminal (18,9) has both supports (18,8),(19,9) consumed by V7.
It contributes the single activation A=1.

Here is the full tile census. The seam is along an aligned tile boundary;
both consumed seam supports are outside their original blocks' endpoint-bearing
tiles, so the blocks' censuses add without changing profiles:

| Actual profile | F(k,8) | Psi(F(4,8)) | Total |
|---|---:|---:|---:|
| 4P0T | 3k/2+15 | 10 | 3k/2+25 |
| 2P1T | 5 | 10 | 15 |
| 2P0T | 2 | 12 | 14 |
| 3P0T | 0 | 5 | 5 |
| 1P1T | 2 | 0 | 2 |
| 1P2T | 0 | 1 | 1 |

For completeness, all nonfull endpoint tiles of F(k,8), specified by their
even origins, are: (2,0),(2,2),(2,4),(6,4),(-k-6,6) of profile2P1T;
(-2,2),(-2,4) of profile2P0T; and (6,2),(-k-6,4) of profile1P1T.
Every other endpoint tile in the endpoint intervals is full. The second
block is fixed, and direct substitution in its four displayed original
sources gives the second column.

All fourteen 2P0T tiles contain exactly one original irregular pair: two
from V4, four from V6, seven from V7 and one from V8. The five triples are
unfilled ORIGINAL U11 caps with even origins

    (20,10),(24,10),(8,8),(16,10),(16,14).

The sixth original cap, at (18,8), is filled by the activated positive
terminal (18,9). The two 1P1T tiles are original far terminal receivers of
V2,V3. There are no mixed triples or mutual non-event pairs. Therefore

    U0=5, Z0=0, L1=2, L2bar=14, L2mutual=L3=0,
    H=L1+2L2bar+2L2mutual+L3=30,
    2R=A+U0+Z0+H=36, R=18, mu=N+R-G=17.

This is ONE reserve ledger. The activation and filled cap do not create a
second independent payment.

## 4. Delete one negative owner; compute the exact repair obstruction

Retain I={V2,V3,V4,V5,V6,V7,V8}, deleting only V1. The retained endpoint
graph is connected: V2,V3,V4 keep the contacts displayed in Section2, V2
keeps the seam edge to V7, and the entire second block remains. V5,V8 and
all four actual marked witnesses survive.

Let W be the supports of retained producers restored by deletion of V1.
Direct substitution gives exactly

    W={(-2j,0),(-2j,7):0<=j<=k/2}
      union {(-k-1,1),(-k-1,6),(1,0),(2,0)}.

Thus |W|=k+6. Its multiple-anchor set is exactly

    W2={(-2j,7):0<=j<=k/2}.

For j>=1 each such point has persistent endpoint neighbors (-2j,6) in V4
and (-2j,8) in V3. At j=0 the additional neighbor (1,7) in V3 also persists.
Every point in W2 must therefore be omitted in ANY relaxed repair that keeps
the retained endpoint set fixed and permits deletion of restored supports.
No deletion of another selected point removes these endpoint conflicts.

Among W minus W2 the only edges are the path

    (0,0)--(1,0)--(2,0),

whose persistent endpoint anchors are respectively (0,1) in V4, (1,1) in
V3, and (2,1) in V2. Each selected-selected edge forces deletion of an end,
so at least one further omission is necessary. All other restored points
have only their single retained anchor and no restored-support adjacency;
the surviving previously visible selections have no neighbor in W. Omitting
W2 together with (1,0) attains feasibility of ALL remaining selections.
Consequently the exact relaxed optimum is

    kappa(I)=|W2|+1=k/2+2.

The actual complete-source rule forbids those omissions. The conclusion is a
lower bound even for a RELAXED repair; no feasible source subfamily is being
claimed for the cut. The distinct-point omission count is also different
from total degree excess, which is k/2+6 here.

The recurring occupied band has one owner-level rule

    {V3,V4} -> V1.

Its many physical conflict witnesses do not supply many reserve occurrences.
Since I contains both antecedents and every other owner, its least feasible
Horn closure is the entire eight-source family. Closure restores legality,
but this particular attempted cut gives no strictly smaller source instance.

## 5. Concrete witness and the remaining research question

At k=70 the complete family has596 endpoints,298 matching edges and139
selections. The retained endpoint graph has436 vertices. There are76 restored
supports,36 forced multiple-anchor omissions, and the independent path needs
one further omission. Hence kappa=37 exceeds the ENTIRE actual pool36.

All original occupied points fit in the aligned rectangle
[-k-8,27] x [-2,17] of dimensions(k+36) x20. Its ambient slack is

    sigma=10(k+36)-(3k+88)-(3k/2+34)=11k/2+238.

At k=70 this is623. Both sigma and mu are positive; neither target inequality
is refuted. The vector(A,U0,Z0,H), source counts, N,G and negative mass all
stay fixed as kappa grows without bound. Therefore no bound on these pointwise
omissions can depend only on those counts, even with the stated connectivity.

The second block alone is a legal closed family containing the positive
source and gate witnesses. Cross-block nontrivial Horn dependencies are absent;
the seam's consumer implications are tautological. Thus this does NOT rule out
a comparison specifically for a least hull generated by positive demand and
its actual witnesses. The remaining task is a demand-related SIGNED transfer
bound on such legal hulls or another general argument for mu>=0. A generic
connectedness assumption and pointwise repair payment cannot supply it.

## Verification and provenance

Run `python3 develop/check_connected_source_cut_obstruction.py`. Complete
reconstruction checks all mandatory supports, all selected occupied degrees,
original matching and endpoint disjointness, full and retained connectivity,
actual marked sides, the exact geometric reserve ledger, restored-support
formulas, the attaining omission certificate, and the Horn completion.
Ten finite controls include k=4,68,70,200; the general proof is Sections1--4.
The original Oracle research task573e88ad proposed this connected extension;
its stream failed, and its completed SAME task response was recovered through
the task API. The independent local checker reproduces the proposal. The
earlier ACCEPT concerns the source-retention theorem, not an independent review
of this new note. No new Lean verification is claimed for this note.
