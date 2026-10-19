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

FROZEN_CAPACITY_TWO_CROSS.md now treats one concrete square-with-branches
class and proves an exclusive four-half-donor budget and all-size receiving
family. The general P-square/branch case and donor coverage are still open.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
