# Every pure two-row endpoint component reduces to at most one matching edge

19 October 2026. This removes the interior-matching-closure, blank-guard and
width>=4 restrictions when the complete endpoint component is a full
two-row rectangle. It does not assume single terminality. The submitted
manuscript remains unchanged.

## 1. Theorem and exact hypotheses

Let (T,M) be feasible in a finite rectangular grid. Write P for matching
endpoints and A=T union P; every T has at most one neighbor in A. Suppose
one entire connected component of the graph induced by P is, after a
translation and rotation,

    H={0,1} x {0,...,w-1},    w>=2.

The actual matching on H may contain horizontal and vertical edges in any
order. Completeness of the component is essential: no other P is adjacent
to H. There is no assumption on alignment with an auxiliary tile partition.
Labels outside the physical rectangle are blank.

**Pure two-row reduction theorem.** There is a nonempty feasible promotion
bundle using only matching edges of H which leaves at most one matching
edge, and hence at most two P, inside H. In particular all w-1 P-squares of
H disappear. It preserves |T|+|M| and promotes either w or w-1 endpoints.
The bound of one remaining edge is sharp.

Original T outside H remains selected, and all other matching edges remain
unchanged. The theorem permits arbitrary feasible exterior configurations.

## 2. Exterior constraints and the easy case

Every occupied neighbor outside H of an endpoint in H is T: an adjacent P
would be in H's endpoint component. Such a T already has its occupied
neighbor in H, so all its other neighbors are blank. Write tau_r(j) for the
indicator of the perpendicular selected support of (r,j), north for r=0
and south for r=1. Adjacent supports on the same exterior row cannot both
be selected:

    tau_r(j)+tau_r(j+1)<=1.                                  (1)

The two lateral sites at either end of H cannot both be selected either.
Only the four corners can have two exterior supports. At most one corner
at each end can have two; when one does, the other corner at that end has
no lateral support. Call a corner with two exterior T doubly supported.

If every doubly supported corner has the same grid color, promote the
other grid color on every matching edge in H. If there is no such corner,
use either color. Each matching edge joins different colors, so every
edge is oriented exactly once. Every promoted vertex has no retained P
neighbor in H and at most one exterior T, proving feasibility. No P remains.

The only remaining case has two doubly supported corners at opposite ends,
with opposite colors. Let C avoid the left doubly supported corner and
let D=1-C, which avoids the right one. The construction uses color C on
the left and D on the right, switching across one actual matching block.

## 3. A blank switch block always exists

Every perfect matching of a two-row rectangle has a unique decomposition
from left to right into V blocks of one vertical matching edge and HH
blocks of two horizontal matching edges across two columns. Indeed, at the
leftmost remaining column either its vertices are matched together, or
both must be matched horizontally to the next column. Removing that block
proves the decomposition inductively. No matching edge crosses block cuts.

For block i occupying columns [a_i,b_i], let v_E(j) be the unique endpoint
of color E in column j. Define

    L_i=0 if a_i=0, otherwise tau(v_C(a_i-1)),
    R_i=0 if b_i=w-1, otherwise tau(v_D(b_i+1)).

These are indicators at the promoted vertices immediately outside the
proposed retained block. If such a vertex is a physical end corner, it is
the corner opposite the doubly supported one, so has no lateral support.
Thus L_i=0 or R_i=0 means the respective existing guard has no occupied
exterior neighbor, including its possible lateral site.

For consecutive blocks, v_D(b_i+1) and v_C(b_i) lie in the same row at
adjacent columns. Their support sites are adjacent. Equation(1) gives

    R_i+L_(i+1)<=1.                                         (2)

The first L and the last R are zero by definition. Choose the first block
whose R is zero. If it is first, its L is zero. Otherwise the previous R
is one, and (2) forces its L to be zero. Thus some block has L=R=0.
This is an unbounded finite-sequence argument, not a search limited to
small widths. The corresponding induction is checked separately in Lean.

## 4. Construct the reduction at that block

Promote color C on every matching edge strictly left of the chosen block,
and color D on every edge strictly right. These choices avoid both doubly
supported corners unless the corner lies inside the chosen block.

If the block is V, retain its single vertical edge. In either outer region
all promoted vertices are one checkerboard color and have no retained P
neighbor there. The only possible retained neighbors inside H are at the
two outside guards. Each guard has just one retained central P and no
exterior occupied neighbor because L=R=0. Other promoted vertices have
at most one exterior T. Hence the bundle is feasible.

If the block is HH at columns a,a+1, let q be the row with color D at a
and C at a+1. Retain the horizontal matching edge in row q. Both outside
promoted guards, when present, also lie in row q. The other row p has
colors C,D across the block. Its perpendicular supports cannot both be
selected by (1); choose an endpoint in row p with blank perpendicular
support, promote it and delete its horizontal mate.

This central promoted vertex retains its vertical P neighbor in row q.
Its mate is blank. Its horizontal neighbor outside the block, if present,
is blank because the outside promoted guards lie in the other row q.
It also has no lateral selected neighbor at a physical end: if the block
touches that end, the row-q endpoint there is the doubly supported corner,
whose lateral support forces the other row's lateral site blank. Thus
the central promoted vertex has exactly one occupied neighbor.

The outside guards each meet one retained endpoint of the row-q edge and
have no exterior support. Every other promoted vertex has no retained P
neighbor in H and at most one exterior support. Feasibility follows.

In both cases exactly w-1 edges are deleted, so the bundle is nonempty
and only the retained edge remains in P. The new occupied set is the old
A minus the deleted mates. Every original T therefore only loses occupied
neighbors. This proves feasibility everywhere and objective preservation.
QED.

## 5. Sharpness and componentwise consequences

For w=3 take three vertical matching edges and selected supports

    (-1,0), (-1,2), (2,0), (2,2), (0,-1), (1,3).

All other vertices outside H are blank; embed with blank padding. Each T
has one P neighbor. The top-left and bottom-right endpoints have occupied
degree4, the other four have degree3, so this is single-terminal.

Suppose a feasible bundle promotes all three matching edges. The two
doubly supported corners cannot be promoted, forcing the bottom-left and
top-right orientations. The bottom-left endpoint already sees its south
T, so the bottom-middle vertex must be deleted. The top-right endpoint
already sees its north T, so the top-middle vertex must also be deleted.
Both endpoints of the middle edge would be blank, impossible when one
must be promoted. Thus complete endpoint removal is impossible.

Retain the left vertical edge, promote the bottom-middle endpoint while
deleting its top mate, and promote the top-right endpoint while deleting
its bottom mate. The first promoted vertex sees only the retained bottom
left P; the second sees only its north T. This feasible two-edge bundle
removes both squares. Therefore the one-edge remainder bound is sharp.

By compatible-bundle composition, all distinct endpoint components of
this type can be reduced simultaneously: their matching edges are disjoint
and their total promoted count is at least sum_H(width(H)-1). Rotation
gives the same conclusion for complete two-column components. No tile
surplus is allocated by this argument, so it spends no compensation twice.

Consequently no configuration terminal under all nonempty promotion
bundles can have such a pure two-row/two-column rectangular endpoint
component of width>=2. Remaining square-bearing components must have a
different complete shape or additional endpoint attachments. The earlier
width3frozen example had four pendant endpoints outside its2x3core and
is therefore outside this theorem. A two-row patch inside a larger
component still needs the previous guard/closure analysis.

If every initial endpoint component is either square-free or a pure
two-row/two-column rectangle, apply this reduction to the rectangular
components, then repeatedly apply feasible single promotions. No move
creates P or a P-square, and at most the original matching-edge count can
be deleted. The resulting endpoint graph is square-free and single-terminal,
so the earlier straight-comb theorem classifies every remaining component
and excludes every further oriented bundle. This gives a general canonical
normalization for that whole initial class, without allocating tile surplus.

## 6. Evidence, attribution and remaining scope

The constructive proof was supplied in Oracle task091b12cf-820d-4073-8660-
5d6a4a961cf1, conversation conv_7bbc210a3b3c3b09, observedgpt_6/pro,
completed19October06:34UTC. Its block, boundary and sharpness arguments
were independently checked against the actual graph definitions before
adoption. The exact response is preserved. This is mathematical input,
not an independent review of later code, Lean execution or the separate
mixed-color family classification.

The companion implementation constructs the indicated bundle from the
actual matching and tests both the original and resulting pair directly.
Full matching decomposition and graph adapters remain written proofs.
Finite controls do not replace the general proof. The blank-block
existence lemma is an arbitrary-length Lean induction.

The completed physical run checks all1211616support-pattern/perfect-matching
pairs of widths2through8, including non-single-terminal cases, with1172456
whole-color constructions,25662vertical switches and13498horizontal
switches. It also checks1792deterministic random cases of widths9through64
and1024symmetry images. All26nonempty oriented bundles of the sharp
three-column fixture are checked separately; none promotes all three edges.
Enumeration only checks the constructed transformation. The proof in
Sections2--4establishes the arbitrary-width statement.

Local Lean separately verifies blank-block existence for arbitrary sequence
length and the numerical contradiction underlying the three-column full-
promotion obstruction. The general physical matching, support and central
horizontal-case adapters are written; a full grid formalization is not claimed.
The combined local sequential Lean4.33.0audit passes51declarations with
only standard logical axioms, no sorry and no compiler-reduction axioms.

The general grid/triple equality, tile source coverage, compensation for
attached/branching components and universal improvement of5/6remain open.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
