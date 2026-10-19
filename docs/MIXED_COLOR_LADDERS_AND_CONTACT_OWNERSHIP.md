# Mixed-color ladders and exclusive occupied contacts

19 October 2026. Continuation of FOUR_GUARD_LADDER_REDUCTION.md.
General proofs below concern actual matching-endpoint components. The
submitted manuscript is unchanged. Coordinates are zero-based after embedding.

## 1. Compatible bundles compose, and endpoint components factor

Let (T,M) be feasible in a finite graph: P is the endpoint set of M,
A=T union P, and every T has at most one neighbor in A. A promotion bundle
orients distinct matching edges u--v, promotes their u endpoints, deletes
those matching edges and makes their v endpoints blank. For promoted set U
and deleted mate set D, the new occupied set is exactly A minus D.

**Compatible-union lemma.** Any finite family of individually feasible
bundles on pairwise disjoint matching-edge sets has a feasible union.
Their colors may differ. The union preserves |T|+|M| and its increase in
|T| equals the sum of their edge counts.

Proof. Edge disjointness prevents an endpoint from being promoted by one
bundle and deleted by another. In the union, an originally selected vertex
only loses occupied neighbors. A promoted vertex from bundle i sees a
subset of the occupied vertices that remained in its individually feasible
bundle, since the union only deletes more mates. Its occupied degree is
therefore at most one. Counting the disjoint edges proves the final claims.
QED. Identical orientations of a shared edge may instead be deduplicated;
opposite orientations of a shared edge are incompatible and cannot be combined.

**Component factorization.** A global bundle is feasible if and only if
its restriction to each connected component H of the graph induced by P
is feasible. In particular, other components cannot rescue an infeasible
local promotion by deleting additional endpoints.

Proof. Every matching edge stays inside one H. Every endpoint neighbor of a
promoted vertex in H also belongs to H; original T stays occupied and
original blanks stay blank. Thus the promoted vertex has exactly the same
occupied neighbors under the restricted bundle and the global bundle.
Original T is feasible under every restriction because it only loses
neighbors. This proves necessity; the compatible-union lemma proves
sufficiency. QED.

This separates feasibility from the charge ledger: endpoint promotions
factor by endpoint components, whereas two components can still use the same
aligned tile. Tile compensation still requires its own ownership proof.

## 2. Exclusive ownership of occupied contacts

Call g an occupied contact of H if g is occupied and adjacent to some P in H.

**Occupied-contact ownership lemma.** An occupied vertex cannot be a contact
of two distinct endpoint components.

Proof. If g is P, adjacency to an endpoint puts it in that endpoint's
component. If g is T, it has at most one occupied neighbor, so the two
purported endpoint neighbors must be the same vertex. Their components
coincide. These exhaust the occupied labels. QED.

Thus, choose one full-P two-row strip with matching-closed strict interior
and width>=4 in each of L distinct endpoint components. Suppose neither
canonical color bundle of the previous theorem is feasible. Each strip has
at least one occupied guard of each color. Choosing two such guards gives
2L distinct occupied vertices, by the ownership lemma. In particular,

    2L <= | union of the occupied guard sets |.

More precisely each guard color contributes at least L distinct vertices.
An endpoint guard belongs to the component containing its strip; a selected
guard is its exclusive selected contact. This discharges the shared-vertex
ambiguity across distinct endpoint components. It does not apply to two
strips in the same component, and does not assert distinct donor tiles or
negative tile charge. Diagonal T in one saturated tile can be exclusive
contacts of different components while the tile has charge zero. Therefore
this vertex count cannot itself be spent as a compensation budget.

Here is a complete frozen example of this last obstruction. Take matching
edges (-2,0)--(-1,0) and (2,1)--(3,1), with selected vertices

    (-3,0), (-2,-1), (-1,1), (0,0),
    (1,1), (2,2), (3,0), (4,1).

All other sites are blank. Each selected vertex has exactly one endpoint
neighbor. Each matching endpoint has two selected supports and hence freezes
immediately. The two endpoint components are distinct. The contacts (0,0)
and (1,1) belong exclusively to the upper and lower component, respectively,
but occupy the same aligned tile {0,1}x{0,1}. That tile has two T, no P,
and charge zero. Translation by (4,2) embeds this in a10x6rectangle with
T8,M2,objective10. Thus distinct frozen-component contacts do not even
guarantee negative charge in their common tile. The global inequality is
not refuted.

## 3. An all-length family for which mixed colors are essential

Fix integers k,l>=1 and put a=2k, b=2l, W=a+b+1. Let the endpoint
component be the full two-row rectangle

    C={0,1} x {0,...,W-1}.

Take selected supports

    (-1,2j), (2,2j),       0<=j<=k+l,
    (0,-1), (1,W).

All other vertices are blank. Translate into a sufficiently large even
rectangle with blank padding. The same arguments permit any feasible
exterior that retains this complete endpoint component and its supports.

The matching consists of:

1. The horizontal edge (r,2i)--(r,2i+1) for r=0,1 and 0<=i<k.
2. The central vertical edge (0,a)--(1,a).
3. The horizontal edge (r,a+2i+1)--(r,a+2i+2) for r=0,1 and 0<=i<l.

This is a perfect matching of C, with W edges. Every selected support has
exactly its intended endpoint neighbor; selected supports are pairwise
nonadjacent. Each noncorner endpoint has its three core neighbors, and each
corner has at least one selected support. Thus the configuration is feasible
and single-terminal. The selected count is W+3 and the objective is 2W+3.
There are exactly W-1 endpoint squares.

**Mixed-color necessity theorem.** This family has the following exact properties.

- Every endpoint of color0 strictly left of the central column freezes.
- Every endpoint of color1 strictly right of the central column freezes.
- Both endpoints of the central vertical matching edge freeze.
- The remaining W-1 endpoints, color1 on the left and color0 on the right,
  form a feasible promotion bundle U using all noncentral matching edges.
  It removes every endpoint square and leaves precisely the central edge.
- Every feasible bundle restricted to C is oriented on a subset of U. Consequently U is
  the unique largest feasible bundle, of size W-1; the maximum attainable
  increase in selected vertices is W-1.
- Any bundle confined to color0 leaves all 2k left-and-center squares;
  any bundle confined to color1 leaves all 2l right-and-center squares.
  Hence every bundle that removes all squares must use both colors.

Here freezing has its standard universal meaning: a vertex cannot be
promoted by any feasible bundle, even one using other endpoint components.
When a vertex freezes its matching mate must remain occupied. A vertex
with two necessarily retained occupied neighbors freezes.

Proof of freezing. The top-left endpoint has its north and west selected
supports, so freezes. Propagate from left to right along the even top
positions: top position 2i has its north T and the retained top position
2i-1, the mate of the previously frozen top position 2i-2. This reaches
and freezes the top central endpoint.

Symmetrically, the bottom-right endpoint freezes from its south and east
supports. Propagate from right to left along even bottom positions, using
the south T and the retained mate of the previously frozen endpoint, until
the bottom central endpoint freezes. Their common matching edge now makes
both central endpoints necessarily retained.

Freeze the odd bottom positions on the left, proceeding outward from the
center. At position a-1, the vertical top neighbor is retained from the
first top induction, and the right bottom neighbor is the retained central
endpoint. Its freezing retains its left matching mate. At each subsequent
odd bottom position, the vertical top mate is retained and the right bottom
neighbor was retained by the previous step. This freezes the remaining
left color0 endpoints. The symmetric outward top induction on the right
freezes all remaining right color1 endpoints. All premises precede their
use; there is no circular retention argument. QED.

Proof of attainability and exactness. Let

    U={ (r,c) in C: c<a and (r+c)%2=1 }
      union { (r,c) in C: a<c and (r+c)%2=0 }.

Each noncentral matching edge has exactly one endpoint in U and its other
endpoint in the frozen set just proved. The central edge is untouched.
After the move, the occupied set is the original T, U and the two central P.
The set U is independent: each half is one grid color, and the central
column separates the halves. A vertex of U at an even column sees its one
perpendicular T and is not adjacent to the central column. At an odd column
it has no perpendicular T and can see only one central P, if at the boundary
of its half. Neither axial selected support touches U. Thus every promoted
vertex has at most one occupied neighbor. Original T only loses neighbors,
and the bundle is feasible. It deletes W-1 edges and promotes W-1 vertices;
only the central edge remains, so every square disappears.

The frozen set is exactly C minus U: every remaining candidate is in the
attaining bundle and therefore cannot freeze. Any feasible bundle must
promote only U, and neither endpoint of the central edge can be promoted.
It therefore uses at most W-1 edges, with equality only for U. In a color0
bundle, no left matching edge can be deleted because its color0 endpoint
is frozen. The central edge is also retained, leaving all left-and-center
squares intact. The color1 argument on the right is symmetric. QED.

The two restrictions of U to the left and right halves are individually
feasible, since deletions in the other half cannot change the neighbors of
their promoted vertices. They have disjoint matching edges, so the first
lemma also certifies their mixed union. This is a genuine obstruction to
using only one uniform color, not a counterexample to square elimination
or the desired global coloring inequality.

## 4. Exact classification of every feasible bundle in the family

Number left horizontal blocks i=0,...,k-1 from left to right. Write x_i
for promotion of the upper odd endpoint (0,2i+1), and y_i for promotion
of the lower even endpoint (1,2i). These are the only possible orientations,
by the freezing proof. The central endpoints are always retained.

A promoted y_i already sees its south T. Its upper neighbor is deleted
exactly when x_i is chosen, and for i>0 its left neighbor is deleted exactly
when y_(i-1) is chosen. Its matching mate is deleted by its own promotion.
Therefore

    y_i => x_i,               y_i => y_(i-1) when i>0.             (1)

A promoted x_i has no north T. After deleting its mate, its remaining
potential neighbors are the lower odd endpoint and the next upper even
endpoint (the central P when i=k-1). At least one must be deleted. Thus

    x_i => y_i or x_(i+1),    with x_(k) unavailable.               (2)

These conditions are also sufficient, because they check all possible
occupied neighbors of every promoted vertex. If any x_i is chosen, follow
(2) to a chosen y_j with j>=i; finiteness and the unavailable central
promotion guarantee termination. By (1), all y_0,...,y_j and their x mates
are chosen. Applying the same argument to every chosen x shows that the
chosen indices in both rows coincide and form an initial segment. Conversely
any common initial segment satisfies (1)--(2).

Thus the left restriction of every feasible bundle deletes exactly the first
i complete horizontal blocks in both rows, for a unique i in0,...,k.
Reflection across the central column and interchange of the rows gives the
right restriction: exactly the last j complete blocks, for j in0,...,l.
Deletions in either half cannot affect neighbors in the other half, since
the central column stays occupied. The pair (i,j) therefore parametrizes
all feasible bundles, including the empty pair (0,0).

It follows, without enumeration, that there are exactly

    (k+1)(l+1)-1 nonempty feasible bundles.

The bundle (i,j) deletes2(i+j)matching edges and leaves precisely

    2(k-i)+2(l-j)

endpoint squares, in the central remaining rectangle. In particular the
mixed bundle U=(k,l) is the unique square-removing bundle, not only the
unique largest one. The feasible-bundle poset is the product of the two
finite chains, with its empty element removed when requiring a nonempty
bundle. This exact classification explains why the two fixed-color maximal
cores each leave squares, whereas their compatible mixed union succeeds.

## 5. Scope and next question

The ownership, factorization and all-length family proofs are general.
Finite enumeration serves only as a control. The broader statement that
every pure two-row endpoint component admits full square elimination under
an arbitrary matching is now proved separately in
PURE_TWO_ROW_COMPONENT_REDUCTION.md, by reducing to at most one matching
edge. The Oracle input supplying that block argument does not review this
later family classification or its implementation. That general theorem
rests on its own proof, not on the bounded search.

Independent review of the present note was submitted as follow-up
0fa8059e-eff7-45b9-87e4-8d6ce8f2f66b in the same conversation, original
stream91355. The response is pending when this milestone is prepared; no
verdict is inferred. Its scope is this note's proofs, not execution.

The family controls pass144parameter pairs,1152symmetry images and63660
exact nonempty oriented bundles in six small instances. They independently
check the entire frozen set, exact left-prefix/right-suffix classification,
count (k+1)(l+1)-1, unique square-removing bundle, and saturated contact
obstacle. Earlier discovery controls cover1999426single-terminal pure-strip
cases through width10; those counts are discovery evidence, not a proof.
Scoped Lean checks abstract compatible-union feasibility/retention and
contact ownership, arbitrary-length prefix implications, and the general
integer-grid neighbor bound for U. The physical matching/frozen-chain
adapters and exact graph-level classification/count remain written proofs.
The combined local sequential Lean4.33.0audit passes51declarations with
no sorry, new axioms or compiler-reduction axioms.

The new count resolves occupied-vertex reuse between different endpoint
components, but occupied-to-tile payment, same-component guard overlap,
escaping matchings in larger attached components, branching cores and universal compensation
remain open. The general grid/triple equality and universal5/6improvement
are not claimed.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
