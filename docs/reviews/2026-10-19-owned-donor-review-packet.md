# Grid endpoint structure and exclusive compensation: review packet

19 October 2026. This is a written-proof review, not a code-execution or novelty audit. Finite checks and the30-declaration scoped Lean audit passed separately. The general grid equality remains open. A preceding review accepted the original core/frozen package, not the later donor, tight completion, endpoint classification or cross. A follow-up task failed with cdp_disconnected@typing and no mathematical verdict. This fresh request includes all necessary notes and relevant Lean source; review all substantive new claims independently.



---

## Source: docs/SQUARE_FREE_ENDPOINTS_AND_OWNED_DONORS.md

# Square-free endpoint structure and compensation owned by matching edges

19 October 2026. Research continuation; the submitted manuscript is unchanged.
The endpoint graph below is the graph induced by P in the physical grid.
It is not the residual tile graph or its capacity-two strand expansion.

## 1. Conventions

Let (T,M) be a feasible pair in a finite rectangular grid. Write P for all
matching endpoints, A=T union P, and B for the remaining vertices. Every
selected vertex has at most one neighbor in A. A configuration is
single-terminal when every P has at least three neighbors in A: otherwise
promoting that endpoint and removing its mate is feasible.

Extend labels outside the rectangle by B. This permits uniform local
arguments at the boundary without adding occupied vertices. A P-square
means all four vertices of any unit square belong to P. Its lower corner
need not align with the fixed 2-by-2 tiling.

Sections4--6 use an even-by-even rectangle and its aligned2-by2tiling.
The endpoint structure theorems themselves do not require even side lengths.

## 2. Turns and branches force a P-square

**Local turn lemma.** In a single-terminal configuration, if a vertex of
the endpoint graph has exactly two endpoint neighbors and they are
perpendicular, then its endpoint component contains a P-square.

Proof. Translate and rotate so the corner is o=(0,0), with endpoint
neighbors w=(0,-1) and s=(1,0). Its other neighbors are not P. At least
one of them is selected, since o has occupied degree at least three.
By reflection assume n=(-1,0) is selected. Its occupied neighbor o forces
nw=(-1,-1) blank. The vertex sw=(1,-1) cannot be selected, since it is
adjacent to both w and s. Vertex w has occupied degree at least three;
one neighbor nw is blank and another is o. Both its remaining neighbors,
sw and (0,-2), must therefore be occupied. Thus sw is P, completing
the unit square o,w,sw,s. QED.

**Local branch lemma.** Any vertex with at least three endpoint neighbors
in a single-terminal configuration belongs to a P-square.

Proof. Three of its endpoint neighbors can be normalized to w=(0,-1),
s=(1,0), e=(0,1), around o=(0,0). Neither sw=(1,-1) nor se=(1,1)
can be selected: each already has two endpoint neighbors. If both were
blank, s would have at most two occupied neighbors, o and (2,0).
Hence at least one of sw,se is P and completes a P-square. The same
argument applies when all four neighbors of o are P. QED.

These are local general proofs, including boundary cases. They do not
assume an enumeration bound or that the endpoint graph is a forest.

## 3. Complete structure in the absence of P-squares

**Straight-comb theorem.** If a feasible single-terminal configuration
has no P-square, then every nonempty endpoint component has the following
form:

1. It is a straight horizontal or vertical path on an even number 2r of
   vertices, r>=1. Its matching is the unique perfect matching of that path.
2. Every endpoint has occupied degree exactly three. Each path end has
   two selected neighbors: one continuing the path axis outward, the other
   perpendicular. Every inner vertex has one selected perpendicular neighbor.
3. The perpendicular selected supports alternate sides along the path.
   There are exactly 2r+2 distinct selected supports for the component.
4. Every matching endpoint freezes under the general frozen certificate;
   consequently no nonempty endpoint-promotion bundle of any orientation
   exists, even using several components simultaneously.

Proof. The branch lemma bounds endpoint degree by two. Every endpoint has
its mate, so no isolated vertex is possible. The turn lemma excludes
perpendicular degree-two neighbors. A finite component with degree at
most two and no turns is therefore a straight path; a cycle would have
a turn. A matching edge never leaves its endpoint component, so M is a
perfect matching there. A path has a perfect matching precisely when it
has even order, in which case the matching is unique.

No path vertex can have both perpendicular neighbors selected. If it did,
take either adjacent path vertex q. The two perpendicular neighbors of q
would both be forced blank by those selected vertices, each already
adjacent to the original P. Vertex q could then have at most two occupied
neighbors, contradicting terminality. Thus an inner vertex has exactly
one perpendicular T; an end has exactly one perpendicular T and its
outward axial neighbor in T. These give occupied degree exactly three.
Supports at consecutive positions cannot lie on the same side, since
they would be adjacent selected vertices already incident to P.
No selected support can serve two P, by feasibility. This gives the count.

Order the path p_0,...,p_(2r-1), matched in pairs p_(2i),p_(2i+1).
Both ends freeze using their two T neighbors. From the left, freezing
p_(2i) guarantees that its mate p_(2i+1) remains occupied, so the selected
support of p_(2i+2) freezes that next even vertex. The symmetric induction
from the right freezes all odd vertices. All supports stay occupied in
every proposed bundle, so the certificate works across components too.
QED.

For an end-to-end frozen certificate the vertex domain may be the original
occupied set A. The matching involution on P is extended by the identity
on T. The abstract retained-mate hypothesis must not be imposed on original
blank vertices. This is the sound adapter noted by the preceding review;
the geometry and adapter remain written proofs here.

**Constructive reduction.** If the original endpoint graph has no P-square
(in particular, if it is a forest), repeated feasible single promotions
reach the straight-comb class in at most the original |M| moves. Each move
deletes P and preserves the original T and the objective. Deleting P cannot
create a P-square. At termination the straight-comb theorem applies and
excludes every oriented bundle, not merely further singles. No uniqueness
of the final configuration is claimed.

**Maximum-degree-two variant.** Suppose instead that the endpoint graph
has maximum degree two and the configuration has no nonempty fixed-side
promotion bundle. It has exactly the same straight-comb structure.

Proof. It is single-terminal. A P-square, if present, is an entire
four-cycle component. Each corner needs at least one exterior T. The
eight exterior positions form four side-adjacent pairs; each pair contains
at most one T, since each such T is already adjacent to a P. Thus all
four corners have exactly one exterior T and occupied degree three.
Promoting the two corners in either bipartition side deletes both opposite
P and leaves each promoted corner with its one T neighbor. This is a
feasible fixed-side bundle, a contradiction. Now apply the theorem. QED.

This classifies endpoint paths, not residual paths of tiles. Residual paths
can still bend, and all-P squares can straddle the fixed tiling. For the
general problem, the next cases include P-squares in components with
branches or additional attachments; their removability is not proved.

## 4. General compensation by actual matching-edge ownership

All tile charges are original full-configuration charges. For a deficient
tile Q, let t,p,b be its counts of T,P,B, and let s count its endpoints
matched to saturated tiles. Then

    2rho(Q)=t-b+s=2t+p+s-4.

Saturated tiles have charge zero. If t+p<=2 and t=2, necessarily p=s=0,
so the same displayed formula is zero and remains valid.

**Owned-donor lemma.** Let Q have at most two occupied vertices, t+p<=2.
Choose h distinct P in Q whose mates lie in specified deficient tiles
outside Q. Then

    2rho(Q)+h = -2(2-t-p)-(p-s-h) <= 0.                 (1)

Proof. No chosen endpoint contributes to s. Consequently h<=p-s.
Substitute the charge formula and rearrange. Each term on the right
of (1) is nonpositive. QED.

This permits two different half-payments from the same two-endpoint donor
when h=2 and s=0; its charge is then at most -1. A one-endpoint donor
supports at most one claim. Merely being deficient is insufficient:
the occupancy and deficient-mate conditions are substantive hypotheses.

**Cross-component allocation theorem.** Let source regions S_i be
pairwise tile-disjoint, and let D be a set of distinct donor tiles outside
all sources. Each donor has t+p<=2. A claim for S_i is a P in a donor
whose actual matching mate lies in a deficient tile of S_i. Let h_i
be the number of claimed endpoints for S_i and assume

    2rho(S_i)<=h_i.

Then the union of the sources and donors has nonpositive charge. No
assumption about matching directions, residual component membership,
turns, or the shape of a source is required.

Proof. The mate of any particular donor endpoint is unique and cannot
lie in two disjoint sources. Thus claims for distinct sources are disjoint
as physical endpoints. For each donor write h_Q for its total claims;
then sum_i h_i=sum_Q h_Q, with h_Q<=p_Q-s_Q. Apply (1) once per donor
and add the source bounds over the disjoint tile partition. Explicitly,
put delta_i=h_i-2rho(S_i)>=0. The exact identity is

    2rho(union S_i union D)
      = -sum_i delta_i
        -sum_(Q in D) [2(2-t_Q-p_Q)+(p_Q-s_Q-h_Q)] <=0. (2)

There is no extra budget for a second route to the same endpoint.
Distinct endpoints in a two-endpoint tile share its actual charge through
the single h_Q term. If the remainder of the grid also has nonpositive
charge, this proves |T|+|M|<=mn/2, coefficient one on this covered class.
This is not a universal improvement of the existing 5/6 bound. QED.

This supplies an explicit geometric incidence rule in place of an
unverified Hall hypothesis for these donors. It does not establish that
every source has enough such actual matching incidences, or that the
uncovered remainder is nonpositive.

## 5. Automatic non-overlap for anchored diamonds

Take any pairwise tile-disjoint central four-tile cores satisfying the
anchored-diamond lemma in PROMOTION_CORES_AND_ANCHORED_OBSTRUCTIONS.md,
allowing all tile-preserving symmetries and translations in one feasible
configuration. Each has charge1 and its two forced adjacent donors each
have labels with t=p=1,b=2. Their sole P is matched into a deficient tile
of that core.

**Automatic packing corollary.** All these adjacent donors are distinct
and lie outside every central core. Thus all central cores and all their
forced donors together have charge exactly zero; it is enough to assume
disjointness of the central cores, rather than of the six-tile patches.

Proof. Core tiles have (t,p)=(1,2) or (2,1), so a donor with (1,1) cannot
be a tile of any core. If one donor served two different cores, its sole
P would have its matching mate in both, contradicting disjointness.
Within one core the two donor coordinates are distinct. Each core has
two exclusive half-payments; add the exact charges. QED.

This removes an explicit packing hypothesis of the preceding sufficient
class by proving it from the physical matching. It does not permit
overlapping central cores or reuse of the earlier one-tile exterior repair.

## 6. A physical two-source patch with a shared two-endpoint donor

The owned-donor theorem also permits genuine sharing by different endpoints
of one tile. Start with the central diamond and its two adjacent donor tiles,
retaining only the eight T inside that six-tile patch. Remove its upper
donor T at (2,0), reflect this entire configuration by (row,column) ->
(row,1-column), and unite the two copies. The removed T of each copy is
replaced by a P of the other; no selected/P conflict is introduced.
Translate all columns by six into an8-by14board. All unlisted vertices
are blank. The complete data are:

    T={(2,2),(2,11),(3,3),(3,5),(3,8),(3,10),
       (4,2),(4,4),(4,9),(4,11),(5,0),(5,5),(5,8),(5,13)},
    M={ (2,10)--(2,9), (2,8)--(2,7),
        (5,9)--(5,10), (5,11)--(5,12),
        (2,3)--(2,4), (2,5)--(2,6),
        (5,4)--(5,3), (5,2)--(5,1) }.

Feasibility is checked directly, independently of tile charges; the checker
also compares these displayed coordinates with its constructed fixture.
The two cores occupy tile rows1,2 and respectively columns1,2 and4,5.
Each retains charge1. The shared tile (1,3) has PP/BB, with its P at
(2,6),(2,7) matched respectively into the left and right deficient cores.
It has t=0,p=2,s=0 and charge-1. The other two donors, (2,0) and (2,6),
each have t=p=1,b=2,s=0 and charge-1/2. Each source has exactly two
claims. The eleven-tile union has T14,P16,B14 and eight internal matching
edges, hence charge zero. The shared tile's unit is split into two halves
by two distinct matching endpoints; it is not charged twice at unit value.

This patch is feasible, but no bundle terminality or global optimality is
claimed. Its purpose is a physical instance of two sources sharing a donor
through different matching incidences, beyond the preceding exclusive
single-endpoint donor class.

## 7. Verification and next obligations

The general proofs are above. The companion checker tests the local turn
and branch implications, full feasible pairs, straight-comb families,
unit-square removal, finite oriented bundles, and compatible pairs of
physical diamond patches. Lean verifies the stated local label implications,
the general frozen-chain induction and conditional ownership/budget logic;
graph classification, coordinate adapters and the complete allocation
theorem retain written proofs.

The local sequential Lean audit passes30declarations, including seven new
ones in formal/SubQuorum/OwnedDonorCompensation.lean. No sorry, compiler
reduction axioms or new axioms are used. The new ownership uniqueness theorem
is axiom-free; the other new declarations use only standard logical axioms.
The companion finite run passes24,271feasible pairs,32straight-comb sizes,
256family symmetry images, two removable-square alignments,15donor budget
models,648pair placements and the shared two-source patch under8symmetries.
Of576placements with disjoint cores,72attempted overlapping donor patches
are incompatible;392complete feasible pairs have disjoint patches.

    python3 develop/check_owned_donors.py --output output/owned-donor-controls.json
    python3 scripts/check_collar_formal.py --lean /path/to/lean4.33.0/bin/lean --output output/owned-donor-formal-check.json

Next: handle terminal components containing P-squares with branches, and
test whether interacting positive sources admit enough low-occupancy donors
under exclusive endpoint ownership. General rectangular-grid equality,
the unrestricted triple equality and external priority remain open.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.


---

## Source: docs/FROZEN_CAPACITY_TWO_CROSS.md

# A frozen capacity-two center forces four exclusive half-donors

19 October 2026. Continuation of SQUARE_FREE_ENDPOINTS_AND_OWNED_DONORS.md.
This supplies a concrete terminal component with a P-square and branches,
and proves its actual exterior compensation. The submitted manuscript is
unchanged. All coordinates are zero-based; tile coordinates divide by two.

## 1. Complete local hypothesis and frozen certificate

Consider an aligned6-by6patch with the following required selected vertices
and four required matching edges:

    T_0={(0,2),(1,1),(1,4),(2,5),(3,0),(4,1),(4,4),(5,3)},
    M_0={ (2,2)--(1,2), (2,3)--(2,4),
          (3,3)--(4,3), (3,2)--(3,1) }.

Translate by any even vector and apply any tile-preserving reflection or
rotation. The patch may have any feasible exterior, and additional selected
vertices or matching edges are allowed wherever feasibility permits.
These eight T are distinct and each has one of the four outer P as an
occupied neighbor. Their other neighbors are therefore forced blank.
Inside the patch this leaves only its four extreme corners unspecified.

The central unit square is all P. Each of its corners is matched outward
to a different neighboring tile. Each outer P has two specified T neighbors
and freezes immediately. Consequently all four central P remain occupied
in every proposed endpoint-promotion bundle. Each central P has two other
central P neighbors and therefore freezes in the next round. All eight
required P are excluded from every oriented bundle, even with other matching
edges in the exterior. In the exact fixture their occupied degrees are three.

Thus the straight-path classification cannot be extended by simply deleting
its P-square exclusion or its maximum-endpoint-degree-two hypothesis.
The endpoint graph has a square with four pendant matching edges. Matching
directions are mixed: two horizontal and two vertical. This is an obstacle
to that structural extension, not a counterexample to the grid inequality.

## 2. Exact forced compensation

**Capacity-two cross lemma.** Under the local hypotheses above, the central
tile C=(1,1) has residual capacity r=2, residual degree d=4, and charge zero.
Its four side-adjacent tiles each have charge exactly-1/2. Their union with
C, a five-tile cross, has charge exactly-2. Each of the four remaining
corner tiles of the6-by6patch has nonpositive original charge. In particular,
the entire nine-tile patch has charge at most-2, with arbitrary feasible exterior.

Proof. The forced side tile labels, written in TL,TR/BL,BR order, are

    north (0,1): TB/PB,       east (1,2): PT/BB,
    south (2,1): BP/BT,       west (1,0): BB/TP.

Each has t=p=1,b=2. Its sole P is matched to the central all-P tile,
which is deficient, so s=0 and 2rho=t-b+s=-1. The center has t=h=s=0,
r=2 and four residual matching endpoints, giving rho=d/2-r=0.
These five tiles are distinct, so the cross charge is-2.

Each corner tile contains its specified diagonal T, two forced blanks,
and one unspecified outer corner. If that corner is B, the charge is-1.
If it is T, the tile is saturated with charge zero. If it is P, the tile
has t=p=1,b=2 and at most one saturated attachment, so its charge is at
most zero. This last case retains the original boundary term; an outside
saturated mate is not silently discarded. Summing the disjoint nine tiles
proves the bound. QED.

The bound is sharp: add all four outer corners (0,0),(0,5),(5,0),(5,5)
to T_0 and make all other unspecified vertices blank. These additions have
no occupied neighbor in this exact fixture. The complete labels become

    T B T B B T
    B T P B T B
    B B P P P T
    T P P P B B
    B T B P T B
    T B B T B T.

There are T12,P8,B16,M4, objective16 and whole-patch charge-2. This is
not a claim of objective optimality for the6-by6grid, whose known value is18.
At this fixed matching, any single-terminal completion with no additional P
inside the patch must contain T_0: each outer P needs both of its remaining
possible neighbors occupied and these must then be T. The forced blanks
leave at most the four extreme corners available. Therefore T<=12 is exact
under those stated fixed-matching and terminality hypotheses. No unrestricted
fixed-matching maximum or maximal-T normal form is claimed.

The saturated corner boundary case is physically realizable. Translate the
sharp fixture by (2,2) into a10-by10board, replace its upper-left corner T
at (2,2) by a P matched to (1,2), and add T at (0,2),(1,3). The exterior
tile (0,1) is saturated with that P, so the corner's s=1 and its charge is
zero. The original nine-tile patch still has charge-2. This explicitly
checks that the corner boundary correction is retained.

## 3. Several centers cannot spend the same half-donor

**Automatic allocation theorem.** Take c distinct central tiles satisfying
the lemma, with arbitrary allowed orientations, in one feasible configuration.
Their4c side donors are all distinct and none is another center. If K
pairwise tile-disjoint source regions have charge at most one each and
every source tile has (t,p)=(1,2) or (2,1), then source tiles are also
automatically disjoint from these centers and donors. Writing W for all
remaining tiles gives the exact sufficient estimate

    rho(whole grid) <= K-2c+rho(W).                     (1)

In particular K<=2c and rho(W)<=0 establish |T|+|M|<=mn/2 on this class.

Proof. A center has four P; a side donor has exactly one T and one P,
so it cannot be a center. If one donor belonged to two distinct centers,
its unique P would have its actual matching mate in both distinct center
tiles, impossible. Thus each of the4c physical half-donors is counted once.
Source tiles have three occupied vertices, whereas donors have two and
centers four, so these families cannot overlap. Sum the source bounds and
the exact center/donor charges over this tile partition. The corner-tile
inequalities of Section2 may help control W, but their budgets are not
counted again in (1). This proves the estimate without spending an entire
nine-tile collar twice or requiring those collars to be disjoint. QED.

The source charge assumption and the nonpositive remainder are explicit;
neither follows merely from connectivity, terminality, or a long path.
This is a concrete cross-component coefficient-one sufficient class, not
a universal improvement of the5/6bound.

## 4. Arbitrarily large connected receiving regions

For every r>=1, place the sharp complete6-by6fixture at vertical shifts
(6i,0),0<=i<r, in a6r-by6rectangle. Between copies the only common occupied
columns on facing rows are0 and5, belonging to the added outer-corner T.
Each gains just one T neighbor, which is feasible. The required anchors
at facing columns3 and2 do not interact; all required P retain occupied
degree three and the same two-round frozen certificate works globally.

The union of the r five-tile crosses has5r tiles and is tile-connected:
the south donor of one copy is side-adjacent to the north donor of the next.
It has charge-2r. All4r omitted corner tiles are saturated and neutral, so
the whole grid has T12r,M4r,objective16r and charge-2r. Every source budget
in (1) uses these4r distinct side donors once. This gives an all-size
capacity-two/branching receiver, not merely an enumeration range.

## 5. Verification and scope

The written geometry proves all sizes and arbitrary feasible exteriors.
The extended develop/check_owned_donors.py checks exact labels, r,d,
all80nonempty oriented bundles of the base fixture, the two-round certificate,
the only four possible extra selected vertices at fixed M, every corner B/T/P
charge option with its saturated boundary term,32family sizes and256images.
The earlier30-declaration Lean receipt covers its stated local/frozen/owned
interfaces, not this complete coordinate cross or its geometric allocation.

This continuation was added after review52d73dd9 was submitted and is outside
that review's input. No review acceptance or new Lean geometry is inferred.
General coverage, the unrestricted grid/triple equality and external priority
remain open.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.


---

## Source: docs/PROMOTION_CORES_AND_ANCHORED_OBSTRUCTIONS.md

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


---

## Source: formal/SubQuorum/FrozenPromotion.lean

import Std

set_option autoImplicit false

namespace SubQuorum.FrozenPromotion

inductive Frozen {Vertex : Type} (adjacent : Vertex → Vertex → Prop)
    (selected : Vertex → Prop) (mate : Vertex → Vertex) : Vertex → Prop where
  | two_selected (vertex first second : Vertex)
      (hfirstAdjacent : adjacent vertex first) (hsecondAdjacent : adjacent vertex second)
      (hdistinct : first ≠ second) (hfirst : selected first) (hsecond : selected second) :
      Frozen adjacent selected mate vertex
  | selected_frozen (vertex first second : Vertex)
      (hfirstAdjacent : adjacent vertex first) (hsecondAdjacent : adjacent vertex second)
      (hdistinct : first ≠ second) (hfirst : selected first)
      (hsecond : Frozen adjacent selected mate (mate second)) :
      Frozen adjacent selected mate vertex
  | two_frozen (vertex first second : Vertex)
      (hfirstAdjacent : adjacent vertex first) (hsecondAdjacent : adjacent vertex second)
      (hdistinct : first ≠ second)
      (hfirst : Frozen adjacent selected mate (mate first))
      (hsecond : Frozen adjacent selected mate (mate second)) :
      Frozen adjacent selected mate vertex

theorem frozen_exclusion {Vertex : Type}
    (adjacent : Vertex → Vertex → Prop) (selected promoted retained : Vertex → Prop)
    (mate : Vertex → Vertex)
    (hselected : ∀ vertex, selected vertex → retained vertex)
    (hretained : ∀ vertex, ¬ promoted (mate vertex) → retained vertex)
    (hfeasible : ∀ vertex first second, promoted vertex →
      adjacent vertex first → adjacent vertex second →
      retained first → retained second → first = second)
    (vertex : Vertex) (hfrozen : Frozen adjacent selected mate vertex) :
    ¬ promoted vertex := by
  induction hfrozen with
  | two_selected vertex first second hfirstAdjacent hsecondAdjacent hdistinct hfirst hsecond =>
      intro hpromoted
      exact hdistinct (hfeasible vertex first second hpromoted hfirstAdjacent hsecondAdjacent
        (hselected first hfirst) (hselected second hsecond))
  | selected_frozen vertex first second hfirstAdjacent hsecondAdjacent hdistinct hfirst
      hsecond inductionHypothesis =>
      intro hpromoted
      exact hdistinct (hfeasible vertex first second hpromoted hfirstAdjacent hsecondAdjacent
        (hselected first hfirst) (hretained second inductionHypothesis))
  | two_frozen vertex first second hfirstAdjacent hsecondAdjacent hdistinct hfirst hsecond
      firstInductionHypothesis secondInductionHypothesis =>
      intro hpromoted
      exact hdistinct (hfeasible vertex first second hpromoted hfirstAdjacent hsecondAdjacent
        (hretained first firstInductionHypothesis) (hretained second secondInductionHypothesis))

end SubQuorum.FrozenPromotion


---

## Source: formal/SubQuorum/OwnedDonorCompensation.lean

import SubQuorum.FrozenPromotion

set_option autoImplicit false

namespace SubQuorum.OwnedDonorCompensation

inductive Label where
  | blank | selected | endpoint
  deriving DecidableEq

def occupied : Label → Nat
  | .blank => 0
  | _ => 1

def degree (state : Int → Int → Label) (row column : Int) : Nat :=
  occupied (state (row-1) column) + occupied (state (row+1) column) +
  occupied (state row (column-1)) + occupied (state row (column+1))

def feasibleAt (state : Int → Int → Label) (row column : Int) : Prop :=
  state row column = .selected → degree state row column ≤ 1

theorem turn_forces_square (state : Int → Int → Label)
    (hcenter : state 0 0 = .endpoint) (hwest : state 0 (-1) = .endpoint)
    (hsouth : state 1 0 = .endpoint) (hnorth : state (-1) 0 = .selected)
    (hnorthFeasible : feasibleAt state (-1) 0)
    (hsouthwestFeasible : feasibleAt state 1 (-1))
    (hwestTerminal : 3 ≤ degree state 0 (-1)) :
    state 1 (-1) = .endpoint := by
  cases hnorthwest : state (-1) (-1) <;>
    cases hsouthwest : state 1 (-1) <;>
    cases houter : state 0 (-2) <;>
    simp_all [feasibleAt, degree, occupied] <;> omega

theorem branch_forces_square (state : Int → Int → Label)
    (hcenter : state 0 0 = .endpoint) (hwest : state 0 (-1) = .endpoint)
    (hsouth : state 1 0 = .endpoint) (heast : state 0 1 = .endpoint)
    (hsouthwestFeasible : feasibleAt state 1 (-1))
    (hsoutheastFeasible : feasibleAt state 1 1)
    (hsouthTerminal : 3 ≤ degree state 1 0) :
    state 1 (-1) = .endpoint ∨ state 1 1 = .endpoint := by
  cases hsouthwest : state 1 (-1) <;>
    cases hsoutheast : state 1 1 <;>
    cases houter : state 2 0 <;>
    simp_all [feasibleAt, degree, occupied] <;> omega

theorem two_side_supports_impossible (state : Int → Int → Label)
    (hcenter : state 0 0 = .endpoint)
    (hnorth : state (-1) 0 = .selected) (hsouth : state 1 0 = .selected)
    (hnorthFeasible : feasibleAt state (-1) 0)
    (hsouthFeasible : feasibleAt state 1 0)
    (heastTerminal : 3 ≤ degree state 0 1) : False := by
  cases hnortheast : state (-1) 1 <;>
    cases hsoutheast : state 1 1 <;>
    cases houter : state 0 2 <;>
    simp_all [feasibleAt, degree, occupied] <;> omega

theorem frozen_chain {Vertex : Type} (adjacent : Vertex → Vertex → Prop)
    (selected : Vertex → Prop) (mate : Vertex → Vertex)
    (path support : Nat → Vertex) (length : Nat)
    (hbase : FrozenPromotion.Frozen adjacent selected mate (path 0))
    (hsupport : ∀ index, index < length → selected (support index))
    (hselectedAdjacent : ∀ index, index < length →
      adjacent (path (2*(index+1))) (support index))
    (hpreviousAdjacent : ∀ index, index < length →
      adjacent (path (2*(index+1))) (path (2*index+1)))
    (hdistinct : ∀ index, index < length → support index ≠ path (2*index+1))
    (hmate : ∀ index, index < length → mate (path (2*index+1)) = path (2*index)) :
    ∀ index, index ≤ length → FrozenPromotion.Frozen adjacent selected mate (path (2*index)) := by
  intro index
  induction index with
  | zero =>
      intro hbound
      simpa using hbase
  | succ index inductionHypothesis =>
      intro hbound
      have hstep : index < length := by omega
      apply FrozenPromotion.Frozen.selected_frozen _ (support index) (path (2*index+1))
        (hselectedAdjacent index hstep) (hpreviousAdjacent index hstep)
        (hdistinct index hstep) (hsupport index hstep)
      rw [hmate index hstep]
      exact inductionHypothesis (by omega)

theorem single_endpoint_donor_unique {Vertex Owner : Type}
    (endpoint : Vertex → Prop) (inDonor : Vertex → Prop)
    (belongs : Owner → Vertex → Prop) (mate : Vertex → Vertex)
    (hunique : ∀ first second, inDonor first → endpoint first →
      inDonor second → endpoint second → first = second)
    (hdisjoint : ∀ first second vertex, belongs first vertex → belongs second vertex →
      first = second)
    (firstOwner secondOwner : Owner) (firstEndpoint secondEndpoint : Vertex)
    (hfirstDonor : inDonor firstEndpoint) (hfirstEndpoint : endpoint firstEndpoint)
    (hsecondDonor : inDonor secondEndpoint) (hsecondEndpoint : endpoint secondEndpoint)
    (hfirstClaim : belongs firstOwner (mate firstEndpoint))
    (hsecondClaim : belongs secondOwner (mate secondEndpoint)) : firstOwner = secondOwner := by
  have hsame := hunique firstEndpoint secondEndpoint hfirstDonor hfirstEndpoint
    hsecondDonor hsecondEndpoint
  rw [← hsame] at hsecondClaim
  exact hdisjoint firstOwner secondOwner (mate firstEndpoint) hfirstClaim hsecondClaim

theorem owned_donor_budget (selected endpoints saturated claims : Nat) (chargeTwice : Int)
    (hoccupancy : selected+endpoints ≤ 2)
    (hclaims : saturated+claims ≤ endpoints)
    (hledger : chargeTwice = 2*(selected : Int)+endpoints+saturated-4) :
    chargeTwice+claims = -2*(2-(selected : Int)-endpoints)-
      ((endpoints : Int)-saturated-claims) ∧ chargeTwice+claims ≤ 0 := by
  omega

theorem owned_aggregate (source donor : Int) (claims : Nat)
    (hsource : source ≤ claims) (hdonor : donor+claims ≤ 0) : source+donor ≤ 0 := by
  omega

end SubQuorum.OwnedDonorCompensation
