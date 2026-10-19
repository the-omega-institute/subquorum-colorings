# Exact promotion cores and an obstruction surviving every bundle

19 October 2026. This note answers the next normal-form question posed in
COOPERATIVE_PROMOTION_AND_MIXED_P_CHAINS.md. It proves an exact algorithm
for simultaneous promotions on one bipartition side, including degree-four
endpoints, and gives a physical grid obstruction even to arbitrary oriented
promotion bundles. The submitted manuscript is preserved.

## 1. Exact one-side criterion

Keep a finite feasible pair (T,M), its occupied set A, and objective
|T|+|M|. In a bipartite graph orient every matching edge x_i y_i from
one fixed side to the other. Let D have an arc i to j, i not equal to j,
when x_i is adjacent to y_j. Write d_i=deg_A(x_i) and

    need_i=max(0,d_i-2).

**Core criterion.** A subset S of matching edges can be promoted on this
side precisely when every i in S has at least need_i outgoing neighbors
inside S. The union C of all such subsets is itself feasible, contains
every feasible subset, and is obtained by repeatedly removing vertices
whose current outgoing count is smaller than their fixed need_i.
The resulting C is independent of the removal order.

Proof. When S is promoted, x_i loses its mate and exactly the mates
y_j corresponding to its outgoing neighbors in S. Consequently

    deg_(A minus Y_S)(x_i)=d_i-1-outdeg_(D[S])(i).

The earlier bundle lemma gives the asserted equivalence. If a vertex
is removed because its current outgoing count is too small, no feasible
subset of the remaining vertices can contain it. Induction shows that
every feasible subset survives every removal. At termination the survivors
satisfy all thresholds and so are themselves feasible. They are therefore
exactly the union of all feasible subsets. This proves both maximality
by inclusion and removal-order independence. QED.

Reverse adjacency lists and a queue give a linear-time computation in
the size of D. The verification code additionally sorts small sets for
deterministic transcripts; its ordering overhead is not part of that
linear-time existence claim. All thresholds refer to the original occupied set for this
one computation; they are not recomputed during peeling. Recompute the
whole graph and thresholds after actually performing a promotion.

Repeatedly promoting a nonempty core on either side terminates in at
most the original |M| moves, preserving the objective and retaining T.
The result has no nonempty one-side bundle. It includes all single and
degree-three-cycle normalizations: a degree-at-most-two endpoint is a
feasible singleton, and a degree-three cycle meets threshold one. This
does not assert confluence of the resulting feasible pair, nor absence
of bundles mixing the two sides.

On grids, degree-three endpoints need one outgoing neighbor and
degree-four endpoints need two. The method genuinely treats the latter,
not merely cycles in the degree-three subgraph. The checker gives an
8 by 8 physical example with a twelve-edge core containing degree-four
endpoints. Promoting it leaves one locked matching edge. This is a
valid additional move; it is not claimed to be inaccessible by a
sequence of the earlier moves on that example.

For a strict distinction on general bipartite graphs, K_(4,4) with T empty
and M perfect has every endpoint degree four and no degree-three candidates.
Its full four-edge core is feasible. This abstract example is not a grid
embedding or evidence for a strict grid normal-form separation.

## 2. A sound certificate excluding even mixed-side bundles

**Frozen-endpoint lemma.** For a proposed promotion bundle, every original
T vertex remains occupied. A matching endpoint z also remains occupied if
its mate cannot be promoted. Thus an endpoint x cannot be promoted whenever
two distinct neighbors are already guaranteed to remain occupied.

Starting with T as guaranteed occupied, iteratively freeze such endpoints
x and then mark the mates of frozen endpoints as guaranteed occupied.
Every frozen endpoint is excluded from every promotion bundle, even if
that bundle uses both bipartition sides. If all matching endpoints freeze,
no nonempty promotion bundle exists.

Proof. Initially the guarantee for T is unconditional. Assume all earlier
freezes exclude their endpoints from every feasible bundle. An endpoint z
whose mate is frozen cannot be removed by any bundle: removal of z requires
promotion of that mate on the same matching edge. Therefore all guaranteed
neighbors remain occupied in any feasible bundle. Promoting a vertex with
two distinct such neighbors violates the selected-degree-at-most-one
condition. This proves the next freeze, and induction proves the claim.
QED.

This is a sufficient certificate. No converse or decision algorithm for
arbitrary mixed-side bundles is claimed. It constrains only bundles that
delete original matching edges, promote one of their endpoints and retain
all original T. It does not forbid reassigning matching edges, exchanging
original T vertices, or adding different vertices.

For the abstract Lean statement, a sound physical domain is the original
occupied set A, with the matching involution on P extended by identity on T.
Its universal retained-mate hypothesis must not be applied to original blanks.
This adapter is a written interpretation, not a completed geometric Lean proof.

## 3. An anchored four-endpoint path

Consider four consecutive matching endpoints p0,p1,p2,p3 in an induced
path, with matching edges p0p1 and p2p3. Suppose p0,p3 each have two
neighbors in T and p1,p2 each have one neighbor in T. All those T stay
occupied. First p0,p3 freeze. Their mates p1,p2 are then guaranteed
occupied, so p1 freezes using its own T neighbor and p2; p2 freezes
using its own T neighbor and p1. All four endpoints are frozen.

Equivalently, promoting p1 would require deleting p2, which requires
promoting p3, already impossible; the other direction is symmetric.
This local obstruction is a tree. It does not rely on degree-four
endpoints or on any directed cycle.

## 4. A complete grid diamond with no possible promotion bundle

In the 8 by 8 grid, with zero-based coordinates, set

    T={(1,1),(1,3),(2,0),(2,5),(3,2),(3,4),
       (4,3),(4,5),(5,2),(5,7),(6,4),(6,6)},
    M={ (2,4)--(2,3), (2,2)--(2,1),
        (5,3)--(5,4), (5,5)--(5,6) }.

Every remaining vertex is blank. Every T has exactly one occupied neighbor
and every matching endpoint has occupied degree exactly three. The P
vertices form two disjoint horizontal four-vertex paths, with their two
outer edges matched. Their outer vertices have two T neighbors and their
inner vertices one. Section 3 therefore freezes all eight P endpoints in
two rounds of four. There is no nonempty promotion bundle of any orientation.
In particular, there are no singles, degree-three directed cycles or
nonempty one-side threshold cores.

Let R={(1,1),(1,2),(2,1),(2,2)} be the central four tiles. Its labels are

    P P | P T
    T B | T B
    ----+----
    B T | B T
    T P | P P.

The owners are (1,2) with P at TL and (2,1) with P at BR. The two
deficient tiles have t=b=1, so D=0. Both saturated P mates lie inside
R, giving Q=k=2, sigma=eta=0. Two other matching edges cross the region
boundary, j=2. The exact ledger is

    2rho(R)=-D+k+sigma=2.

No free deficient blank remains after the baseline reservation; the
shared-blank graph has two isolated owners and no payment resource.
This is the same one-unit regional debt as the earlier diamond, but
here every bundle is impossible, including two-edge and larger mixed-side
moves. It also attains the transition bound with v=2 and one state change.
Thus its coefficient two cannot be reduced even by assuming full
bundle terminality.

The objective is 12+4=16, strictly below the full grid's half-size32.
Hence the whole-grid charge is -16 and the exterior's charge is -17.
The example refutes a proposed regional implication, not the global grid
inequality. Its matching is entirely horizontal: local positive charge
can persist even in a direction class whose global target is already
proved. Full bundle terminality does not localize that global proof.

## 5. Arbitrarily large tile-connected receivers

For r>=1, translate r copies of the displayed T,M by (6i,0),
0<=i<r, in an ambient (6r+2) by 8 rectangle. All matching endpoints
lie on rows6i+2 and6i+5. Only selected vertices occur on the nearest
rows of adjacent copies: the preceding row has columns4,6, the next
columns1,3. These sets are disjoint, so no additional occupied adjacency
occurs. All selected degrees remain one and all P degrees remain three.
The same two-round frozen certificate works independently in every block,
and therefore excludes every bundle on the entire graph.

Take the four central tiles of each copy, and, for i=0,...,r-2, add
bridge tile (3i+3,1). The core of one block ends at tile row3i+2,
the bridge follows, and the next block begins at row3i+4, so the receiver
R_r is tile-connected and has5r-1tiles. Each bridge has one T, three
blanks and no P. Its original charge is -1. Therefore

    |T|=12r, |M|=4r, objective=16r,
    Q=k=2r, D=2r-2, sigma=eta=0, j=2r,
    rho(R_r)=r-(r-1)=1.                                (1)

No residual-connectivity assertion is made. For the lexicographically
first adjacent blank reservation used by the checker, each bridge has
two free blanks: one private to a neighboring owner and one unused.
Thus H has2r isolated owners, p=u=r-1 and no shared edges or double
links. The witness identity reproduces2rho=2r-(r-1)-(r-1)=2. Every
actual resource is counted once.

The whole-grid charge is16r-4(6r+2)=-8r-8; the exterior charge is
-8r-9. Unlike the earlier weak-normal-form family, the connected receiver's
positive charge stays one, rather than growing with r. We do not claim
unbounded positive regional charge under this stronger terminality.

In this exact family the extra tile (0,1) has one T, three blanks and
charge -1. It is disjoint from R_r, so adjoining it already pays the
one-unit debt exactly, with combined charge zero. This is an actual
one-tile exterior repair, counted once. The anchor hypotheses alone do
not force that tile's fourth, diagonal corner to be blank, so this
specific donor is not asserted for arbitrary anchored paths.

## 6. Forced adjacent half-donors

The displayed anchored geometry actually forces a small exterior payment
in every feasible completion. This uses the existing half-tile ledger;
the additional conclusion identifies the two physical donors and keeps
their ownership separate.

**Anchored-diamond compensation lemma.** Suppose the central four tiles
have exactly the labels and matching incidences of Section4, including
the two outward mates (2,1),(5,6), and suppose (2,0),(5,7) are in T.
All coordinates may be translated by an even vector and reflected or
transposed. The two exterior tiles U_-=(1,0), U_+=(2,3) each have charge
-1/2. They are disjoint from the central receiver and each other, and
the combined six-tile patch has charge zero in the original configuration.
No hypothesis on the rest of the configuration is required beyond feasibility.

Proof. In U_-, TL=(2,0) is selected and TR=(2,1) is its occupied P
neighbor. Thus BL=(3,0) is blank. The other bottom corner BR=(3,1)
is adjacent to the selected core vertex (3,2), already adjacent to its
own occupied P at (2,2); hence BR is also blank. The tile has t=1,b=2,
one P, and its mate lies in the deficient core tile. It therefore has
no saturated attachment and 2rho(U_-)=t-b=-1. The reflected argument
gives the same result for U_+. All four matching edges are internal to
the six-tile patch; its counts are T8,P8,B8 and M4. Additivity gives
rho(R union U_- union U_+)=1-1/2-1/2=0. QED.

Consequently pairwise tile-disjoint patches of this form, with a remainder
of nonpositive original charge, establish coefficient one on that class.
Each patch must include its two assigned donors, and no donor may be
assigned to another patch. This is a conditional geometric class, not
a universal improvement of5/6. Different outward-mate directions or the
absence of the two stated exterior T vertices remain outside this lemma.

For the r-block construction, these are the2r distinct tiles
(3i+1,0),(3i+2,3). They pay each core once; the r-1 bridge tiles then
give remaining charge -(r-1). Equivalently, adding all these donors to
R_r gives rho=1-r. This is one additive calculation, not extra credit
on top of the earlier one-tile repair.

## 7. A tight full-grid completion

The obstacle is not an artifact of a sparsely occupied exterior. Retain
the same four matching edges and use the following complete8x8labels:

    T B T B T T B T
    B T B T B B T B
    T P P P P T B T
    B B T B T B T B
    T T B T B T B B
    B B T P P P P T
    T T B B T B T B
    B B T T B T B T.

These28selected vertices include the previous12. Direct neighbor checks
give a feasible pair with the same eight degree-three P endpoints and
the same two-round frozen certificate. Its objective is28+4=32, half
the grid. Thus full-grid charge is zero while the central receiver still
has rho1. The two forced adjacent donors of Section6 each have charge
-1/2, and every other tile outside the central receiver has charge zero.
This is exact exterior compensation in a globally tight configuration.

The selected set has maximum possible cardinality at fixed M: the existing5/6theorem
gives6|T|+5*4<=3*64, hence |T|<=28. This argument allows replacing T,
not merely adding a vertex while retaining the original set. The existing
width-eight transfer theorem additionally gives Omega(G_(8,8))=32;
the new completion attains that known optimum. It is still not a
representative maximizing |T| among all objective maximizers: an empty
matching dissociation set has32selected vertices. No stronger optimality
claim is made, and the completion is not asserted for every r.

The exact completion and forced-donor lemma were added after the pending
core/frozen follow-up request, so are outside that request's input.

## 8. Scope and next direction

The fixed-side core criterion and the frozen-certificate lemma are general
proofs. The exact frozen-exclusion logic is formalized in Lean; physical
graph adapters and this all-r embedding remain written proofs. Finite
controls enumerate136,452fixed-side subsets on12,752small feasible pairs,
check the displayed family and its one-tile repair through r32 and all eight symmetries, and
enumerate every nonempty oriented bundle for r1 and r2 independently.
Those literal checks comprise80and6,560bundles, all infeasible. Additional
400seeded4x4grids with19,170fixed-side subsets and a twelve-edge core
containing four degree-four endpoints exercise the code.

The combined local audit passes23declarations. The new
SubQuorum/FrozenPromotion.lean statement proves frozen_exclusion by
induction on the certificate for arbitrary vertex types and adjacency
relations; it depends on no axioms. Its retained/promoted assumptions
are stated explicitly, with the physical matching interpretation proved
in Section2. This is not a Lean formalization of the full core algorithm
or the coordinate family. The general logic is separate from the finite
verification counts.

Run:

    python3 develop/check_promotion_cores.py --output output/promotion-core-controls.json

This settles a concrete obstacle question: neither degree-three acyclicity,
absence of one-side cores nor even absence of every endpoint-promotion
bundle implies nonpositive regional charge, despite sigma=eta=0. The
surviving anchored paths demand an exterior/selected-exchange argument.
No maximal-|T| assertion among all objective-maximizing representatives
is made. Future compensation must follow the actual exterior resources
or use a more general exchange, with all original crossings retained.
Universal grid equality, mixed-core coverage and a universal improvement
of5/6remain open; external novelty is not asserted.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
