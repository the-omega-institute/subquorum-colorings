# Four-outward alpha wires are localized by degree defects and direction interfaces

26 October 2026. This is a general geometric counting lemma for original
strands, followed by an exact-degree-three physical boundary example. It
continues the [one-unit slab obstruction](FOUR_OUTWARD_SLAB_AND_ONE_UNIT_OBSTRUCTION.md)
without assuming a unique P-square or a tree of chambers. Submitted
manuscripts are unchanged.

## 1. Hypotheses and quantities

Let (T,M) be feasible on a finite even-by-even grid rectangle. Put P=V(M),
A=T union P. Feasibility means T and P are disjoint, M is a matching of
grid edges, and each t in T has at most one neighbor in A. Suppose every
p in P has occupied degree deg_A(p)>=3 and the fixed pair is
**bundle-terminal**: no nonempty set of distinct actual M edges permits
simultaneously promoting one endpoint of each edge and deleting its mate
while preserving feasibility. Complete freezing is a sufficient certificate;
we do not assume matching uniqueness.

Use the fixed disjoint physical 2-by-2 tiling. Assign each tile either
vertical auxiliary pairs (horizontal bands) or horizontal auxiliary pairs
(vertical bands). An even-rectangle mixed-direction partition is a special
case. Retain each auxiliary pair whose two endpoints are in P as an N edge.
The original owners are components of the multigraph M union N, with the
two copies retained if an M edge equals an N edge. A missing N partner is
a TP terminal when that partner is in T and a BP terminal when it is blank.
An alpha owner is an open TP--TP path. Closed cycles and other open owner
types retain their actual identities.

Let F be ANY collection of full-P physical tiles Q such that all four
actual mates of corners of Q are outside Q. Each has physical capacity two.
Define:

* i_Q: the number of its two N edges belonging to alpha owners;
* a_Q: the number of degree-four occupied endpoints in Q;
* b_Q: the number of degree-four occupied endpoints among its four outside mates;
* c_Q: the number of corners x of Q for which x--m(x) is perpendicular to
  Q's N direction AND the tile containing m(x) has the opposite N direction.

Count **wire incidences**, not distinct owner names: if one alpha visits
both N edges of Q it contributes two. Write I_F=sum i_Q, C_F=sum c_Q,
J4=|{p in P:deg_A(p)=4}|, and E_dir for the number of actual M edges whose
endpoint tiles have different N directions. E_dir counts direction changes,
not every matching edge crossing a region boundary.

## 2. Local and global localization theorem

For every such Q,

    2 i_Q <= 3 a_Q + b_Q + 2 c_Q.                         (1)

Moreover, with J={p in P:deg_A(p)=4}, the identity-preserving aggregate is

    2 I_F <= sum_{p in J} [3 1_{tile(p) in F}
                            + 1_{tile(m(p)) in F}] + 2 C_F,     (2)
    C_F <= E_dir,
    I_F <= 2 J4 + E_dir.                                 (3)

In particular, if EVERY endpoint has occupied degree exactly three and
the auxiliary direction is uniform, **no original alpha passes through
any four-outward full-P tile**. With mixed directions and exact degree
three, I_F<=C_F<=E_dir. The number of distinct alpha owners meeting F is
at most I_F; we do not assert that every alpha meets F.

### 2.1 Frozen alternating squares require two degree defects

Consider any actual alternating unit square: two opposite edges are in M,
the other two are not, and all four vertices are in P. Each checkerboard
color has a degree-four occupied vertex on this square. Otherwise promote
the two vertices of one color, both of degree at most three, deleting
their actual mates. Each promoted vertex loses both its occupied neighbors
on the square, so has at most one occupied neighbor left. The two promoted
vertices are not adjacent. Old selected vertices only lose occupied
neighbors. The remaining M edges are unchanged. This is a feasible
nonempty bundle, contrary to bundle-terminality.

Normalize Q so that N is vertical. Each corner's actual mate is either
vertically outward or horizontally outward. Call a face **double-exit**
when both of its corners' mates leave through that face. The face, its two
actual crossing edges, and the edge between the outside mates make an
actual alternating unit square. If D is the number of double-exit faces,
the preceding argument gives

    2 D <= a_Q + b_Q.                                    (4)

There is no overlap in this use: distinct double-exit faces have disjoint
root corners because each corner has one actual mate, and their outside
mates are distinct because M is a matching. Thus their four-vertex sets
are disjoint. The defects counted in (4) are actual endpoints, including
those whose fourth neighbor is selected; counting only four P neighbors
would be insufficient.

### 2.2 Two-column analysis

Let v be the number of the two N columns for which both actual mates are
vertical. Then v<=D. If v=2 the top and bottom faces are both double-exit.
If v=1, the other column either has two horizontal exits, giving its side
double-exit face, or a vertical exit, completing a top or bottom double-exit
face with the first column. If v=0 there is nothing to prove. This covers
all sixteen outward-direction assignments.

For each remaining column, at least one actual exit is horizontal.
We claim the number h of alpha columns of this kind satisfies

    h <= a_Q + c_Q.                                      (5)

First suppose exactly one exit is horizontal, at corner x with mate y.
Let z be the other corner of the column, and w the exterior companion
adjacent to z on the same side as y. Both y and w belong to the same
neighbor physical tile. If that tile has opposite N direction, x is
counted in c_Q. If its direction agrees, w is the N partner of y.
When w is blank, y is a BP terminal of the very owner containing the
column, which therefore is not alpha. When w is occupied, z has its two
P neighbors in Q, its vertically outward actual mate, and the extra
occupied neighbor w. These are four distinct neighbors. Charge this
possible alpha column to z in a_Q.

If both exits are horizontal, the two outside mates lie in the same
neighbor tile. When its direction agrees, their vertical N edge and the
root N edge form a closed four-edge M/N cycle with the two actual M edges;
that column is not alpha. When the direction differs, both corners are
counted in c_Q and at least one pays for this possible alpha column.

Different root columns use different root defect vertices and different
perpendicular crossing corners. In the opposite-direction case choose
one counted corner of its own column, so no corner is used twice. This
proves (5) by an injection into the disjoint union of root defects and
the counted crossing corners. The discussion allows an owner to revisit
Q and makes no assumption about component shape, number of other squares,
or absence of mixed owners.

At most v alpha columns have no horizontal exit. Therefore

    i_Q <= v+h <= D+a_Q+c_Q.

Combine this with (4) to obtain (1). Rotate the argument to cover horizontal N.

### 2.3 Global sum without reusing an edge

The physical tiles are disjoint. Each p in J is counted in a_Q for at
most its own tile; it is counted in b_Q for at most its mate's tile.
Consequently summing 3a_Q+b_Q gives EXACTLY the endpoint sum in (2),
not a count of separately available donors. Its coefficient at p is at
most 3+1=4, even if both tiles belong to F.

A direction-changing actual M edge is perpendicular to N at exactly
ONE of its endpoints, because the endpoint N directions are opposite.
Thus it contributes to c_Q for at most one root tile, even if both
endpoint tiles are in F. This proves C_F<=E_dir. Summing (1), bounding
the endpoint weights by four, and dividing by two proves (2)--(3).
This also explains why merely counting all cross-tile edges, or counting
the same seam from both sides, would give the wrong bookkeeping. QED.

## 3. Boundary example: a live mixed owner and one direction interface

The permanent [14-by-14 fixture](../develop/fixtures/degree_three_four_outward_live_mixed.json)
has 66 endpoints, 33 actual matching edges and 26 selected vertices.
Every endpoint has occupied degree exactly three. Its fixed 24-wave
strict-rank certificate covers all 66 endpoints and excludes arbitrary
mixed-color simultaneous bundles. The fixture includes every coordinate,
the matching, labels and that independently checked schedule; no search
solver is required for reproduction.

Take the root Q at rows4--5, columns4--5 (zero-based). It is full-P and all
four actual mates are outside. Under uniform vertical N, both root wires
are mixed. Its left wire belongs to the owner with body

    {(3,4),(4,4),(5,4),(5,3)},

TP endpoint (3,4) and BP endpoint (5,3). The original alpha has TP endpoints
(5,2) and (10,2). The legal oriented link (5,2)->(5,3) enters that mixed
owner directly. The blank N pair {(2,5),(3,5)} is an original singleton
resource in its support, outside every direct alpha support. If this
singleton is the ONLY available original unit, that alpha is paid with
one link. Deleting the root mixed owner makes payment zero. Hence absence
of alpha wires at the root does not make all its touching owners safely
prunable. This is a failure of that pruning rule for an available-pool
restriction; the full pool pays its sole alpha at cost zero, and no
full-pool payment decrease is asserted.

Now change only the N direction of the LEFT NEIGHBOR physical tile,
rows4--5, columns2--3, to horizontal. The physical T,P,M and all degrees
and freezing certificates stay fixed. The root's left wire is now alpha,
with TP endpoints (3,4) and (10,2). Exactly two actual matching edges join
tiles with different directions:

    (5,3)--(5,4),    (5,2)--(6,2).

Only the first is perpendicular to root N. Thus J4=0, i_Q=c_Q=1,
E_dir=2: the exact-degree-three local bound i_Q<=c_Q is attained. In
particular one cannot discard the interface term. Owner identities are
recomputed after changing N; there is no claim that old owner bodies are
preserved. Both partitions have one alpha, three beta owners and full-pool
payment one at cost zero.

## 4. What this resolves and what remains open

The [slab](FOUR_OUTWARD_SLAB_AND_ONE_UNIT_OBSTRUCTION.md) has repeated
alpha wires and occupied-degree-four endpoints. The new theorem shows
that removing ALL such degree defects, while keeping uniform direction,
excludes that alpha-through-four-outward mechanism for arbitrarily many
tiles, not just a unique-square component. It also gives an explicit
interface budget when directions are mixed.

This is a localization theorem. Defects and direction-changing M edges
have NOT been proved to supply unused compensating original units.
Neither (1) nor (3) is a new donor allocation theorem. Alpha paths avoiding
these tiles, capacity-one configurations, source-reachable mixed owners,
and resource overlap still require analysis. In particular no universal
improvement of the existing 5/6 bound follows yet. The next counting step
must work on the complete resource cut, retain these reachable owners,
and compare jointly unused credit against actual unpaid demand; it may
not simply pay one fresh unit per defect or per seam.

## 5. Reproduction and formalization scope

Run:

    python3 develop/check_four_outward_alpha_localization.py --output output/four-outward-alpha-localization-validation.json

The checker reconstructs original strands for uniform, checkerboard,
single-tile-flipped and deterministic random direction assignments on
frozen slabs, degree-three chamber networks and crosses. It checks the
local inequalities, alternating-square color defects, injective endpoint
and seam incidences, exact aggregate sum, the explicit live mixed gate,
and independent terminal-matching optima for both witness partitions and
the singleton restriction/pruning test. These finite checks test the
general proof; they do not replace it.

The saved passing receipt covers 20 physical controls, 728 direction
partitions, 4,853 four-outward tile occurrences, all sixteen local direction
patterns, 66 independently checked strict-rank events, and 832 independently
enumerated terminal matchings. The blank pair used by the pruning example is
also verified as the original unit (band1,column5) in an UNCUT whole-board
horizontal-band representation, so the obstruction is not introduced by
tile-region splitting.

The companion [Lean source](../formal/SubQuorum/FourOutwardAlphaLocalization.lean)
checks the sixteen local exit cases, the local counting implication,
finite weighted aggregation and zero-defect corollaries. It also checks
the checkerboard promotion degree arithmetic and direction-change
one-endpoint identity. The coordinate-to-owner injection, frozen-square
geometric adapter, physical rank certificate and general theorem assembly
are written proofs with executable controls, not an end-to-end Lean
formalization of arbitrary grids. See the saved formal-validation receipt
for exact declarations and execution scope.
