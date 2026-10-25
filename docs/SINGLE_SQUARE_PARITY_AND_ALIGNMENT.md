# Complete single-square classification and a neutral misalignment obstacle

**26 October continuation:** the [four-outward slab obstruction](FOUR_OUTWARD_SLAB_AND_ONE_UNIT_OBSTRUCTION.md)
resolves the specific extension left open in Section5: without square
uniqueness, even retaining four outward actual mates and complete freezing
does not guarantee two negative units. Arbitrarily many aligned capacity-two
tiles share a total one-unit negative budget. The original theorem is unchanged.

19 October 2026. This extends ODD_ARM_COMPENSATION.md by removing its
four-outward-mates hypothesis and identifies why tile alignment is necessary
for a strict negative budget. The submitted manuscript is unchanged.
All vertex coordinates and tile indices are zero-based.

## 1. Classification without a matching-direction assumption

Let (T,M) be a feasible pair in a finite rectangular grid, P=V(M), and
A=T union P. Every T has at most one neighbor in A. Assume single
terminality: every P has at least three neighbors in A. Let H be an
endpoint component containing exactly one all-P unit square Q, counting
all unit squares regardless of their alignment with a tiling.

Throughout, use the full original tile ledger: for a deficient tile,
r=2-t-h-s, where h is the number of internal matching edges and s counts
endpoints matched to saturated tiles. Then rho=d/2-r=(t-b+s)/2. Saturated
tiles have charge zero. The single-square receivers below have s=0;
the two-square example in Section5requires the s term.

**Single-square parity theorem.** The occupied external incidences of Q
have one of the two pinwheel orientations. H consists of Q and four straight
outward rays, of lengths l_N,l_E,l_S,l_W>=0. A zero length means the
corresponding external neighbor is T. Every vertex of H has occupied degree
three. Selected perpendicular supports alternate along each nonempty arm,
starting on the side facing away from Q, and each tip has an axial T.

A central corner is matched outward if and only if its arm length is odd.
Let o be the number of odd arms and k the number of matching edges inside
Q. Then

    o+2k=4,       o in {0,2,4}.

When o=2, the two odd-arm corners are adjacent. For o=0 there are two
possible internal perfect matchings of Q; for o=2 its remaining adjacent
corners have their unique internal edge; for o=4 there is no internal edge.
These seven central matching patterns exhaust the possibilities.

Proof. The face-pair and corner-incidence argument of the preceding note
never used the matching-direction hypothesis. It gives exactly one occupied
external neighbor at each corner and on each face. Each is either T or P.
If it is P, the local branch and turn lemmas exclude every branch or turn
outside Q, because they produce a square containing that outside vertex.
Thus each nonempty arm is a finite straight path. The distinct outward rays
do not meet and no other endpoint can join H. The selected support argument
is unchanged: one perpendicular T per arm vertex, alternating sides, and an
axial T beyond its tip. If the arm is absent, its corner's unique external
occupied neighbor is T. Every endpoint has occupied degree three.

If its corner v is matched to p_1, the remaining arm p_2,...,p_l has a
perfect matching, forcing l odd, with pairs p_2--p_3,p_4--p_5,... . If v
is matched within Q, the entire arm p_1,...,p_l must match internally,
forcing l even, with pairs p_1--p_2,p_3--p_4,... . These implications are
also sufficient for the arm matching. A zero-length corner must match
inside Q. Hence the corners not incident to internal central matching edges
are exactly the odd-arm corners. Internal edges are disjoint edges of a
four-cycle, giving o+2k=4 and the stated seven patterns. QED.

This structural theorem does not require even dimensions or an aligned Q.
The next budget statement does.

## 2. Exact aligned charge and the removable/frozen dichotomy

Assume now an even-by-even rectangle and the fixed2-by2tiling, with Q
aligned. Write a_i=floor(l_i/2), N=sum a_i. Let R be exactly the tiles
containing P from H.

**Parity-budget theorem.** R consists of its center, N neutral arm tiles
with (t,p,b,s)=(1,2,1,0), and o terminal half-donors with
(t,p,b,s)=(1,1,2,0). Every P in R belongs to H, all its matching edges
are internal to R, and

    |R|=1+N+o,    P=4+2N+o,    T=N+o,    B=N+2o,
    |M in R|=2+N+o/2,          rho(R)=-o/2.

There are2N+o+4distinct selected supports for H in the entire grid.
The center has h=k, residual capacity r=2-k=o/2 and residual degree d=o.
In particular its charge is zero for all seven matching patterns.

Proof. A north arm still has endpoints (-j,0) and perpendicular supports
(-j,-1) for odd j, (-j,1) for even j, after normalization of Q. Each
paired tile on the ray has PT/PB labels. For an odd arm, the last unpaired
endpoint and the axial T form the terminal TB/PB half-donor. For an even
arm, the last pair already fills its last P tile; its axial T lies in the
next tile, outside R. With l=0 there is no arm tile. Rotation gives all
four directions. The selected supports and unused external face incidences
force the remaining tile vertices blank. In particular, the blank beside
p_1 on a length-one arm is its unused central face incidence; on a longer
odd arm the preceding selected support forces it blank. Thus no exterior
attachment changes their full labels.
All matching mates are in H and all receiver tiles are deficient, hence s=0.
An even arm's neutral tiles contain their internal matching edges; an odd
arm's neutral tiles carry crossing pairs. Either way their original charge
is zero. At the center r=2-k and d=o=4-2k, also giving zero charge.
The remaining o terminal donors each have charge-1/2. Summing gives all
counts and the budget. The support count is sum_i(l_i+1)=2N+o+4,
including one external T at each zero-length arm. Feasibility prevents any
selected support from serving two endpoints. QED.

**Dichotomy.** If o=0, either bipartition side of the central square is a
feasible two-endpoint promotion bundle. If o>=2, every endpoint of H freezes
and no oriented bundle, including one meeting other components, can promote
any endpoint of H.

For o=0 both central matching edges are internal. Promote the two opposite
corners in either grid bipartition side and remove their mates, the other
two corners. Each promoted vertex loses its two central occupied neighbors
and keeps exactly its one external occupied neighbor. The promoted vertices
are nonadjacent. Existing selected vertices only lose occupied neighbors,
so the bundle is feasible and preserves |T|+|M|. It removes Q; deleting P
cannot create a new square. Its original endpoint component is now square-free.

For o>=2, on every odd arm the tip freezes and the two-step inward induction
freezes p_1, retaining its central mate. On every nonempty even arm the same
induction freezes p_2, retaining p_1. A corner with an even arm therefore
has a retained external neighbor: T for length zero, or p_1 otherwise.
The odd arms instead retain their central corners. In the
o=2 case specifically the two internally matched corners have even arms,
so their external neighbors are already retained. Each is adjacent to one
of the two already retained outward-matched central corners. These two
retained neighbors freeze both internally matched corners. Their mates
therefore become retained as well. All four central corners are retained;
each has two retained central neighbors and freezes. For o=4 all central
corners were already retained, so the same final step applies immediately.
Once the center freezes, odd arms propagate outward to their even positions,
and even arms propagate outward to their odd positions. Each step uses its
selected perpendicular support and the retained preceding endpoint. This
freezes every endpoint. The certificate excludes all bundles globally. QED.

Consequently every component with exactly one aligned P-square in a
fixed-side-bundle-terminal configuration has o=2 or4 and pays respectively
one or two units. Square-free terminal components remain straight combs.
This is a complete one-square classification, not a bound on how many
positive sources may require those units.

Receivers from distinct such endpoint components are automatically tile
disjoint: each receiver tile's complete nonempty P set belongs to its
component. For any tile-disjoint source regions S_j outside the receivers,
with rho(S_j)<=1, the remainder W satisfies

    rho(whole grid) <= K - sum_components(o/2) + rho(W).

Source/receiver disjointness is automatic for source tiles with (t,p)=(2,1),
or (1,2) with s>=1, as in the preceding theorem. Without that condition,
it remains an explicit hypothesis. Physical terminal donors and neutral
tiles are each charged once. No uniform source coverage or remainder sign
is asserted, and no unrestricted improvement of5/6follows yet.

## 3. An all-length neutral misalignment family

There is a general neutral counterpart to the aligned four-odd-arm theorem.
Suppose both coordinates of Q's upper-left vertex are odd, and all four arms
are odd, l_i=2a_i+1. Every matching edge of H is then wholly inside one
aligned tile. The tiles containing H have exactly the labels t=1,p=2,b=1
and h=1,s=0, and therefore r=d=rho=0. Writing N=sum a_i, their union R has

    |R|=N+4,    T=N+4,    P=2N+8,    B=N+4,
    |M|=N+4,    rho(R)=0.

Proof. Normalize Q's upper-left corner to (1,1). Its north ray has vertices
(1-j,1), starting with the central corner at j=0. Its matching pairs are
(j=0,1),(j=2,3),... . Each pair occupies the right column of exactly one
aligned tile. At its odd-indexed vertex, the forced perpendicular support
is the other vertex in that row of the tile. The remaining tile vertex is
blank, forced by that T. Thus every matching
pair occupies a tile with exactly one T and no additional P. Rotation about
Q's center (a tile-preserving rotation in this phase) proves the same for
the other rays. These tiles are distinct. Counting matching pairs gives
the displayed ledger, with no saturated attachment or exterior dependence.
The earlier odd-arm frozen proof is independent of tile alignment. QED.

Thus neutral frozen receivers exist at all arm lengths, not just at one
small example. They do not provide a strictly negative budget for positive
sources. The following exact completion shows that an arbitrary feasible
exterior need not restore such a budget either.

## 4. A fully neutral8-by8misalignment obstacle

Alignment cannot simply be deleted from the strict-budget conclusion.
Here is an explicit feasible8-by8configuration with one endpoint component,
one P-square at rows3,4/columns3,4, all four central corners matched outward,
and every endpoint frozen, yet every aligned tile has original charge zero.
In row order the complete labels are

    T B T B T T B T
    B T B T B B T B
    T B T P B T B T
    T B B P P P T B
    B T P P P B B T
    T B T B P T B T
    B T B B T B T B
    T B T T B T B T.

The four matching edges are

    (3,3)--(2,3),  (3,4)--(3,5),
    (4,4)--(5,4),  (4,3)--(4,2).

The displayed T and these edges specify the entire pair; all B are blank.
The eight required supports around the P are
(1,3),(2,2),(2,5),(3,6),(4,1),(5,2),(5,5),(6,4).
The four outer P each have two of these T as neighbors and freeze first;
their mates retain all four central P, which freeze in the second round.
Each P has occupied degree three. Direct inspection of the displayed rows
shows every T has at most one occupied neighbor. The endpoint graph is the
central square with four pendant matching edges, so it has exactly one
P-square. The square is not aligned with the fixed tiling.

The four tiles containing P have respective labels

    (1,1): TP/BP,   (1,2): BT/PP,
    (2,1): PP/TB,   (2,2): PB/PT.

Each has t=1,p=2,b=1,s=0 and contains one whole matching edge. Thus
h=1,r=0,d=0 and rho=0. Each of the other twelve tiles contains exactly
two T, so is saturated and has charge zero. There are T28,P8,B28,M4,
giving objective32=8*8/2 and total charge zero. No independent optimality
claim is needed for this obstacle: feasibility and exact equality suffice.

In particular there is no positive budget of negative tile charge available
anywhere in this configuration. None of its P tiles has at most two occupied
vertices, so the earlier low-occupancy owned-donor rule has no endpoint
incidence to claim. This disproves a proposed uniform negative payment per
single-square frozen component without alignment, even if arbitrary exterior
tiles may be used. It does not disprove the desired global nonpositive-charge
inequality, which holds with equality here. A general proof must allow these
neutral frozen components or use a different normalization/resource.

## 5. Two overlapping squares do not supply two independent budgets

A frozen component containing an aligned P-square can have exactly one unit
of available negative tile charge. The following two-square fixture rules
out a universal two-unit payment based solely on freezing and the presence
of an aligned square. Consider the following complete6-by6configuration:

    T B T B T B
    B T P B P T
    T B P P P B
    T B P P P B
    B T P B P T
    T B T B T B.

Its five matching edges are

    (2,2)--(1,2),  (2,4)--(1,4),
    (3,2)--(4,2),  (3,4)--(4,4),  (2,3)--(3,3).

The endpoint component consists of a2-by3rectangle and four pendant mates.
Its only P-squares have upper-left corners (2,2),(2,3), sharing the central
vertical edge. Every P has occupied degree three. The four pendant P have
two selected neighbors each and freeze first, retaining all four corner P.
The two middle-column P now have two retained horizontal neighbors and freeze
next, retaining each other. The four corners then each have two retained core
neighbors and freeze. These4,2,4layers exclude every oriented bundle, also
in the presence of other components. Direct inspection verifies feasibility.

The north/south left donors (0,1),(2,1) each have t=p=1,s=0 and charge-1/2.
The north/south right tiles (0,2),(2,2) have t=2,p=1 and are saturated.
The all-P core tile (1,1) has h=1,s=0,r=1,d=2 and is neutral. The other
core tile (1,2) has t=0,p=2,h=0,s=2,r=0,d=0 and is also neutral: both
of its matching mates lie in the two saturated right tiles. The remaining
three left tiles all have t=2 and charge zero. Thus the only negative charge
in the entire configuration is the two left half-donors, giving

    T=12, P=10, B=14, |M|=5, objective17=6*6/2-1,
    rho(whole grid)=-1.

The raw occupancy term of the two-P core tile is (t-b)/2=-1; its
saturated-endpoint contribution s/2=1 gives the actual charge zero. The full fixture
therefore refutes a two-unit negative budget for every frozen component
containing an aligned square once additional squares are allowed, even if
the entire exterior may be charged. It also precludes assigning one physical
unit independently to each of these two overlapping P-squares under this
ledger. Exactly one of these squares is aligned, and each has two outward
matching edges and one internal matching edge: o=2, not o=4. Consequently this
example does not settle whether the original four-outward-matched two-unit
theorem extends when uniqueness alone is removed; the later
[all-length slab](FOUR_OUTWARD_SLAB_AND_ONE_UNIT_OBSTRUCTION.md) now refutes
that extension while retaining the four outward mates. Distinct aligned unit
squares are disjoint tiles. The global target remains
valid, strictly, here. The general geometry of several-square components is
still unclassified; this is an exact obstacle to that proposed extension.

## Verification and scope

The first two sections are general proofs. The companion checker enumerates
the seven central matching patterns and independent arm lengths, checks
geometric labels, actual matching parity, frozen certificates or the explicit
two-corner bundle, and the complete physical obstacle under all tile-preserving
symmetries. Finite enumeration is auxiliary, not the classification proof.
The checker passes1806parameter/pattern pairs and14448symmetry images:
516removable,1032two-odd-arm and258four-odd-arm cases. It checks2432bundles
for small frozen family members and all80nonempty bundles of the explicit
8-by8obstacle, with eight symmetry images of that obstacle. The long controls
include arm lengths16/17and asymmetric lengths through31.
All258four-odd-arm cases also pass after an odd/odd tile-phase shift, checking
that every matching edge becomes internal and every P tile has zero charge.
The two-square fixture is checked under eight symmetries, including the full
saturated-attachment ledger and all242nonempty oriented bundles, none feasible.

All41local/general Lean declarations pass sequentially on the authorized
local machine. Two new statements verify the seven central matching
alternatives and the center's parity ledger. Seven further statements in
formal/SubQuorum/SingleSquareObstacle.lean verify the actual finite matching,
selected feasibility, endpoint degrees, unique P-square, exact neutral tile
counts, objective32and a complete frozen certificate. They use kernel
reduction and ordinary logical axioms, with no sorry or compiler-reduction
axioms. The geometric charge adapter, infinite structural classification and
general parity dichotomy remain written proofs.

Oracle review122da19b-19c8-48d8-bbd2-29fcfcf1d961 completed REVISE with
observedgpt_6/pro. It confirms all supplied mathematical results after
correcting the original request's background omission of-s from r. Every
supplied receiver has s=0, so its claims are unchanged; the source verifier
always used r=2-t-h-s. The turning-vertex statement, length-one face blank
and zero-based indices are now explicit as requested. The review's4x4
saturated-attachment example is also independently checked with actual r0,
rho0, rather than unadjusted r1and incorrect rho-1.

Follow-upfc9e74ce-9a65-4ad8-a9d1-e3aec3bf50df in the same conversation
conv_e03faff81c763d9b, original stream62212, supplies the actual adjusted
capacity, clarifications, all-length neutral family and6x6two-square fixture.
It completed REVISE at06:09:07UTC with observedgpt_6/pro. The reviewer accepts
the corrected original theorem, all-length neutral family and complete6x6
certificate, but points out that the fixture changes both uniqueness and
the four-outward condition. Section5now states exactly the broader payment
rule it refutes; the extension retaining four outward mates stays open.
The saturated-endpoint term is also displayed explicitly. No overall ACCEPT
is inferred. Finite Lean execution and the subsequent colorwise ladder
criterion are outside the review input. Both full responses and assessments
are archived.
Multi-square components and full source coverage remain open.

    python3 develop/check_single_square_parity.py --output output/single-square-parity-controls.json

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
