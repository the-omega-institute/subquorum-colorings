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
That task subsequently failed with cdp_disconnected@typing. A fresh complete
file review d3705dc5 includes this note and is dispatched/sent; its exact
attachment and handle are in output/owned-donor-file-review.json. No mathematical
verdict from that task is available at this milestone.
Subsequently that file review ended with no_assistant_output and no
mathematical verdict; see output/owned-donor-file-review-failed-response.json.
ODD_ARM_COMPENSATION.md now replaces the eight fixed selected anchors by
single terminality, uniqueness/alignment of the square and four outward mates.
It proves arbitrary odd-arm transport and explains when adjacent donors disappear.
General coverage, the unrestricted grid/triple equality and external priority
remain open.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
