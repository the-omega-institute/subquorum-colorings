# Degree-three fusion, exact square correction and protected donors

20 October 2026. The preceding compensation theorem prescribed port-port
splices and allowed each port only one foreign contact. Neither restriction
is necessary for its two-leg/rotor module class when the final configuration
has occupied degree exactly three. This note proves a fusion theorem from
physical hypotheses alone. It also identifies the precise correction to
charge additivity: each newly formed tile-aligned all-endpoint square
subtracts two. A further exact ledger allows degree-four contacts and pays
their losses with negative module charge and these square corrections,
without charging one endpoint twice. Thus new contacts can create useful
negative charge as well as consume supports. The general grid inequality
remains open.

## 1. Physical hypotheses and inherited local facts

Fix an even-by-even rectangle and its disjoint 2-by-2 tiling. Each module
(T_i,P_i,M_i) is individually feasible, with P_i=V(M_i), and satisfies:

1. Each endpoint has exactly three occupied neighbors in A_i=T_i union P_i.
2. Every selected site has exactly one endpoint neighbor in its own module.
3. The endpoint graph of the module is connected.

The modules' endpoint sets P_i are pairwise disjoint. They need not have
disjoint selected or occupied sets. Form P=union_i P_i, retain the union
matching M=union_i M_i, and set

    T = (union_i T_i) minus P.

Require that this final pair is feasible and that every final endpoint has
occupied degree exactly three. Extra selections may be added only outside
the union of the original receiver tiles and with no endpoint neighbor.
There is no hypothesis about ports, number of foreign contacts, matching
directions, a module graph being a forest, or the final pair being frozen.

The original corrected receiver charge of module i is

    rho_i = |T_i intersect V(R_i)| + |M_i| - 2|R_i|,

where R_i consists of tiles meeting P_i. The final total charge is the
same closed-receiver expression, summed over final endpoint components.
All saturated-mate transfers stay inside these complete receivers.

We use two established local facts, valid in every single-terminal feasible
configuration. In any unit square its endpoints, if present, are connected
inside that square. A selection in an endpoint-bearing square has its own
unique endpoint neighbor inside it. These follow from the same local
blankness/degree argument as the tile-ownership and receiver-locality lemmas;
they do not require that the unit square align with the physical tiling.

## 2. Occupied neighbors cannot change

**Neighbor preservation.** Every module's original occupied set is a subset
of the final occupied set. Consequently each module endpoint has exactly
the same occupied neighbor sites before and after fusion.

Proof. An original selection either remains selected or becomes an endpoint;
an original endpoint remains an endpoint. Thus A_i is contained in the final
A. Both original and final occupied degrees at each p in P_i are three,
so this inclusion of neighbor sets is an equality. QED.

In particular each foreign endpoint edge u--v, with u in P_i and v in P_j,
automatically replaces mutually selected supports: v was in T_i and u in
T_j. This conclusion follows from the degree condition; it is not a
prescribed splice hypothesis. A leaf may replace both its selected neighbors,
while a chamber corner may replace its single selected neighbor. A final
feasible retained support cannot belong to two modules, because it would
touch their two different endpoint sets.

## 3. A new square uses four different modules

**Four-module square lemma.** If all four corners of a unit square are final
endpoints, then either all belong to one original module, or they belong to
four different original modules. In the latter case each corner was a leaf
of its original endpoint graph and both its original selections inside the
square have become foreign endpoints.

Proof. Suppose a module occupies a proper subset of at least two corners.
Opposite corners alone are impossible by original terminal tile ownership.
If three corners belong to it, the fourth final endpoint, adjacent to two
of them, would have been one of its selections by neighbor preservation.
This selection would have two endpoint neighbors, a contradiction. If two
adjacent corners belong to it, the other two final endpoints would both
have been selections of that module. Those selections are adjacent to one
another and each already has its own endpoint neighbor, again contradicting
original feasibility. This exhausts the proper possibilities. Therefore a
mixed-module full square has four different module labels. At each corner
its two neighbors in the square were original selections. Its actual mate
is an original endpoint neighbor, so lies outside the square, and it was
the corner's only original endpoint neighbor. QED.

Let J be the number of PHYSICAL TILE squares having this latter four-module
form. Nonaligned new squares do not contribute to J. This distinction is
essential because receiver charge is defined using the fixed tiling.

## 4. Exact fusion ledger, including repeated support sites

**Fusion ledger theorem.** Under Section 1's physical hypotheses,

    rho_final = sum_i rho_i - 2J.

The equality holds separately in each final endpoint component as well.

Proof. For a final receiver tile Q let m_Q be the number of represented
modules and e_Q the number of endpoint edges inside Q joining different
modules. Each represented original endpoint subset is connected inside Q,
as is the final endpoint subset. If Q is not full, its induced endpoint
graph is a tree. Contracting its connected original subsets gives a tree,
so e_Q=m_Q-1. If Q is full and comes from one module, m_Q=1 and e_Q=0.
If Q is mixed and full, Section 3 gives m_Q=4 and e_Q=4. Hence always

    e_Q = m_Q-1 + indicator(Q is a new mixed full tile).

Put E_in=sum_Q e_Q. Counting receiver tiles with multiplicity gives

    |R_final| = sum_i |R_i| - E_in + J.

We claim that final receiver selections number sum_i t_i-2E_in, where
t_i=|T_i intersect V(R_i)|. Each intratile foreign edge removes two
old selections counted in these old receivers. Conversely, every old
selection counted in its old receiver which becomes a foreign endpoint
has its unique old endpoint neighbor inside that same tile, by locality.
It therefore corresponds to an intratile foreign edge. An intertile
foreign edge removes no selection counted in its old receiver.

These are counts of module-selection INCIDENCES, not of distinct sites
before fusion. A central site in a four-module square was a selection of
two other modules; it is correctly removed twice. Retained selections
cannot coincide, by Section 2, and cannot spill into a foreign-only receiver:
final locality would put their unique old endpoint neighbor in that tile.
Thus there is no missing term for repeated consumed sites or retained spill.
Extra selections are outside all receiver tiles. The matching size is
sum_i |M_i|. Substitution yields

    rho_final = (sum_i t_i-2E_in)+sum_i |M_i|
                  -2(sum_i |R_i|-E_in+J)
              = sum_i rho_i-2J.

Each old module lies in one final endpoint component, and a final tile's
endpoints belong to one component. The same proof therefore applies per
component. QED.

This accounts for every original tile once and keeps all saturated transfers.
Ordinary additivity is valid exactly when J=0. A new full square is a favorable
correction, not an extra compensation resource that may be spent twice.

## 5. Protected supports and a general donor principle

**Straight-anchor protection lemma.** Let x be an original selection of a
module with endpoint neighbor p. Suppose p has two opposite endpoint
neighbors in that module. Then x cannot become a foreign endpoint in a
fusion satisfying Section 1. It remains selected.

Proof. Normalize p=(0,0), its opposite endpoint neighbors to (-1,0),(1,0),
and x to (0,1). The sites (-1,1),(1,1) are originally blank: x is selected
and already sees p, so both its other displayed neighbors must be blank.
They are also neighbors of the original endpoints (-1,0),(1,0). Neighbor
preservation at those endpoints keeps both sites blank after fusion. If x
became an endpoint, only p and (0,2) could be occupied neighbors, giving
degree at most two and contradicting final occupied degree three. QED.

**Protected donor principle.** Suppose an original module has a selected
corner x of an endpoint-free physical tile Q, exterior endpoint anchor p,
and an endpoint q outside Q adjacent to the opposite tile corner z. Require
that p has two opposite original endpoint neighbors and that q has three
original endpoint neighbors. Then Q is still an actual unit donor after
any such fusion. Chosen distinct donors from different modules cannot
coincide, including when their modules merge into the same receiver.

Proof. Straight-anchor protection keeps x selected. The two corners adjacent
to x are blank by final feasibility, as x already sees p. The corner z
remains blank by neighbor preservation at q, whose three original endpoint
neighbors persist. Thus Q has no endpoints and exactly one selection, x.
Its actual deficit is one. Distinct original modules cannot keep the same
x, since each such selection would have two endpoint neighbors. If their
donor tiles coincided, the tiles' sole selected sites would coincide. This
is impossible. Within one module choose distinct physical tiles, rather
than multiple descriptions of one tile. QED.

Consequently, for ANY supported degree-three modules supplied with protected
donor sets of total size N, the numerical condition

    sum_i rho_i <= N+2J

is sufficient for the coefficient-one half-area bound. Indeed N<=D and the
exact ledger gives rho_final<=N<=D. This principle does not assume that
every possible original module has enough protected donors.

## 6. Two-leg/rotor fusion without prescribed ports

Take arbitrary affine copies of two_leg_case(w,a,b), with w even at least
six and a,b even at least four, and of the rotor in
BRANCHED_ROTOR_NETWORKS_AND_UNBOUNDED_RECEIVER_CHARGE.md. Assume only
Section 1's endpoint disjointness, retained-support feasibility and final
occupied-degree-three hypotheses. No declared-port or single-use condition
is imposed.

**Unrestricted-contact fusion corollary.** These configurations satisfy

    rho_final = sum_i rho_i-2J <= N_positive_modules-2J,
    |T|+|M| <= mn/2-2J.

Proof. The all-phase tables show every rotor is nonpositive, and every
positive two-leg module has charge exactly one. For each positive two-leg
module, take x=(3,2), p=(3,1), z=(2,3), q=(1,3) in its positive reference
alignment, transporting them by its tile-preserving isometry. The anchor p
has opposite endpoint neighbors (2,1),(4,1); these exist even at minimum leg
height four. The guard q has three original endpoint neighbors. Section 5
therefore retains one distinct physical unit donor per positive module,
even under non-port contacts and multiple contacts at one leaf. Thus
N_positive_modules<=D. Combine Section 4 with
sum_i rho_i<=N_positive_modules and the original identity

    mn/2-|T|-|M| = D-rho_final

to obtain the bound, including its strict 2J improvement. QED.

The coefficient-one conclusion improves the existing five-sixths bound by
|M|/6; the displayed class gains an additional 2J. This is a wider geometric
class than the prescribed-splice theorem, but is still not an arbitrary
grid decomposition theorem. Final degree four is not allowed, and the
existence of a suitable initial module decomposition is substantive.

## 7. An all-width frozen four-way contact cycle

Fix even w>=8 and let U=two_leg_case(w,4,4). Translate U by (-4,0) to
obtain N, and let L(r,c)=(c,1-r), a tile-preserving quarter turn. Take
N,L(N),L^2(N),L^3(N), with their actual matchings; remove only supports
which become endpoints. The four contacts form the central physical square
{0,1}x{0,1}. Each module contributes one corner, originally a leaf, and
each such leaf now has TWO foreign neighbors. All four modules are positive.

Here is the full adjacent-arm boundary profile, before central selections
are replaced. N has no sites at rows greater than one, while L(N) has none
at rows less than zero. Only the overlap and one-row halos matter:

| Module | Row | Endpoint columns | Selected columns |
|---|---|---|---|
| N | -1 | 1,w | 2,w-1 |
| N | 0 | 1,w | 0,w+1 |
| N | 1 | none | 1,w |
| L(N) | 0 | none | 1,3,5 |
| L(N) | 1 | 1,2,3,4,5 | 0 |
| L(N) | 2 | 4,5 | 2 |

After all four central sites become endpoints, this table leaves exactly
the intended central edge for each adjacent arm pair. The far columns
w-1,w,w+1 are at least 7,8,9, separated from the other arm's columns at
most five. The remaining displayed supports have neither coincident nor
adjacent occupied neighbors other than their original anchors. Opposite
arms have occupied row supports ending at one and starting at zero, but
in these two overlapping rows the north arm has columns 0,1,w,w+1 and
the south arm columns -w,1-w,0,1. Their sole occupied overlaps are central
sites becoming endpoints; the far columns are separated by w>=8. The same
one-row halo check gives no further contact. Quarter-turn symmetry covers
all arm pairs. This proves feasibility and exact degree three uniformly.

There is exactly one new mixed full physical tile, so J=1. The counts are

    P=8w+24, M=4w+12, T=32,
    receiver tiles=2w+17, receiver selections=24,
    sum_i rho_i=4, rho_final=2.

Translate by (w,w) into a (2w+2)-by-(2w+2) rectangle. For w=8 this is an
18-by-18 example with 88 endpoints and 44 matching edges. All endpoints
have occupied degree three, all four positive modules remain, and the
original corrected charge is two, not four. Four chosen donor tiles are
distinct. This disproves naive additivity and positive-module nonadjacency
once the once-used-port restriction is dropped, without refuting compensation.

The construction is fully frozen. Each even-order module has a unique
internal perfect matching and only ONE vertex incident with foreign edges.
If a perfect matching used a foreign edge at that vertex, the module's
remaining endpoint vertices would have odd order and no other exit. That
is impossible. Thus no foreign edge can occur in any perfect matching,
even though the module contact graph is a cycle rather than a tree. The
union matching is unique; the occupied-degree-three matching criterion
excludes every nonempty feasible mixed promotion bundle.

A separate two-module example shows that non-port contacts really occur:
fuse U=two_leg_case(w,4,4) with its image under (r,c)->(-r,1-c), for even
w>=6. Their upper chamber corners (0,1) and (0,0), each initially of
endpoint degree two, replace mutually selected supports. The sole foreign
edge joins these corners, not bottom ports. Feasibility is read off from
their opposite quadrant supports; occupied degrees remain three. Here J=0,
the charges are 1 and 1-w, and total charge is 2-w. The contact is a bridge
between even modules, so this example is also fully frozen.

## 8. Exact degree-four defect and compensation without double charging

We can relax Section 1's FINAL degree-three condition, retaining all other
physical hypotheses and the original modules' exact occupied degree three.
Final endpoints automatically have occupied degree at least three, since
original occupied neighbor sites remain occupied, and at most four in a grid.
The following ledger applies to any supported original modules, not just
the two-leg/rotor examples.

Every new occupied neighbor of p in P_i is a foreign endpoint. It cannot
be a retained foreign selection: such a selection already touches its own
endpoint, so touching p too would violate final feasibility. Extra selections
are assumed to have no endpoint neighbor. Since p originally had degree
three, a final degree-four p has exactly ONE new occupied neighbor v, which
was originally blank in module i. Conversely every oriented foreign edge
p--v with v not in T_i creates exactly this degree-four event at p.

Let K_in count those degree-four endpoints whose unique new neighbor is
INSIDE THE SAME physical tile. Let J count new mixed full physical tiles;
these may now involve two or three modules as well as four. Then

    rho_final = sum_i rho_i - 2J + K_in.                 (1)

Proof. The local tile contraction identity e_Q=m_Q-1+j_Q still holds:
both old and final endpoint subsets are connected inside the tile; a mixed
full square contributes the one cycle of a four-cycle, regardless of how
many connected old subsets are contracted. This argument no longer uses
the degree-three four-module-square restriction. Receiver tiles therefore
still number sum_i |R_i|-E_in+J.

For receiver selections, each intratile foreign edge removes two original
selection incidences, EXCEPT for its oriented ends at which the foreign
neighbor was originally blank. Those missing support incidences number
exactly K_in. The selected receiver count is therefore
sum_i t_i-2E_in+K_in. The earlier locality and retained-support arguments
still hold because single terminality is sufficient for them. Substitution
proves (1). Intertile new-neighbor events contribute no K_in; counting all
degree-four endpoints in its place would be an overestimate, not an identity.

For the two-leg/rotor class, put N_+=number of positive modules and

    S = N_+ - sum_i rho_i >= 0.

This is their available nonpositive-module charge, counted once per module.
For each positive module consider its three canonical protecting endpoints
q=(1,3), a=(2,1), b=(4,1), in its positive reference alignment. Mark that
module if at least one of these endpoints acquires degree four, and let L
be the number of marked positive modules. The straight-anchor/guard proof
uses only degree preservation at a,b,q, so every UNMARKED positive module
still supplies its distinct actual unit donor. Consequently D>=N_+-L.

There is a useful non-reuse fact for the degree-four loss itself. In the
positive reference alignment, each protecting endpoint's unique original
blank neighbor is respectively

    (2,3), (2,2), (4,2).

Each is OUTSIDE the protecting endpoint's own physical tile. Tile-preserving
isometries keep that property. Thus a degree-four event at a protecting
endpoint is intertile and CANNOT already be counted in K_in. Choose one
such endpoint for each marked module. These chosen endpoints are different,
since original endpoint sets are disjoint. If d4 is the total number of
final degree-four endpoints, this proves

    K_in + L <= d4.                                    (2)

In particular the same degree-four endpoint is never charged both for a
missing intratile support incidence and for a possibly lost protected donor.
Combining (1), D>=N_+-L and the original complete-receiver identity yields
the general quantitative bound

    mn/2-|T|-|M| >= S+2J-K_in-L >= S+2J-d4.             (3)

Hence the concrete criterion

    d4 <= S+2J                                         (4)

proves coefficient one even with degree-four contacts. The finer sufficient
criterion is K_in+L<=S+2J. Neither is assumed automatically for all fusions.
Condition (4) is stated in physical counts, with no donor allocation oracle
or unproved Hall hypothesis. Each new square and each module charge occurs
once, and (2) prevents counting the same local loss twice.

The reservation-aware first-q<=5 conclusion also survives under the finer
criterion: (1) then gives rho_final<=N_+-L, paid by those actual unmarked
unit donor tiles. After any B distinct valid reservations, at most B of
these units are lost, leaving at least rho_final-B=q different positive
residual tiles. The established first-failure classification rules out
q<=4, and its three remaining q=5 motifs have only three or four positive
tiles, contradicting five survivors. Here the new full squares are counted
only through the original charge correction; they are not claimed as extra
endpoint-free donor tiles or spent a second time as reservation units.

## 9. Fully frozen occupied adjacent bands with degree-four endpoints

For even w>=6 take U=two_leg_case(w,4,4) and its image under

    H(r,c)=(4-r,c-w).

Keep their actual matchings and retain exactly their supports which are
not endpoints of the other module. The two endpoint bands in columns zero
and one now lie side by side for rows zero through four. Their five foreign
edges are precisely (r,0)--(r,1), 0<=r<=4. Each original module's even-row
outer supports in the other band are consumed; odd-row inner supports at
(3,2) and (1,-1) survive. All other supports are separated, except for the
mutually consumed end supports. This proves feasibility for every w>=6.

There are four degree-four endpoints, at rows one and three in these two
columns. All other endpoints have degree three. Two physical tiles have
new mixed full faces, J=2. Every degree-four event here is intratile, so
K_in=4=2J. The canonical protecting endpoints of U still have degree three,
so L=0. The module charges are 1 and 1-w; thus S=w-1, and (3) proves

    |T|+|M| <= mn/2-(w-1).

The exact fusion charge is 2-w: the two negative square corrections cancel
the four missing-support incidences. Translate by (2,w) into an
8-by-(2w+2) rectangle. Counts give P=4w+12, M=2w+6, T=14,
receiver tiles=3w/2+6, receiver selections=8, and actual slack=6w-12.
This is a direct occupied-adjacent-band compensation example beyond the
occupied-degree-three case, with a complete loss ledger.

For completeness it is fully frozen for every w, despite degree four. Here
is a uniform ordered certificate, in the unshifted coordinates. Let m be
the actual matching involution. Each named witness is either an original
retained selection or m(v) for an earlier frozen v. This directly excludes
mixed bundles without invoking the degree-three matching criterion.

First freeze even rows four and two of U's free right leg, using its outer
and bottom retained supports. In the other module freeze H(4,1) and H(2,1)
on its free left leg in that order. Run the usual two-leg bar wave from U's right
upper corner (0,w) leftwards to column two, and the H-image of the left
bar wave from (4,1-w) rightwards to column minus one. These bar waves have
the same witnesses as the original two-leg theorem, all untouched here.
Next use the following ten seam rows in the order shown:

| Endpoint | First witness | Second witness |
|---|---|---|
| (1,1) | (0,1)=m(0,2) | (1,2)=m(1,3) |
| (3,0) | (4,0)=m(4,-1) | (3,-1)=m(3,-2) |
| (3,1) | (3,2) selected | (2,1)=m(1,1) |
| (1,0) | (1,-1) selected | (2,0)=m(3,0) |
| (4,1) | (5,1) selected | (4,0)=m(4,-1) |
| (0,0) | (-1,0) selected | (0,1)=m(0,2) |
| (2,1) | (2,0)=m(3,0) | (3,1)=m(4,1) |
| (2,0) | (2,1)=m(1,1) | (1,0)=m(0,0) |
| (0,1) | (0,0)=m(1,0) | (1,1)=m(2,1) |
| (4,0) | (4,1)=m(3,1) | (3,0)=m(2,0) |

Both upper bar corners at the seam are now frozen. Run the complementary
bar waves, then freeze the two remaining free lower bar corners and the odd
row-three free-leg endpoints, using their unchanged inner selected supports.
This accounts for all 4w+12 endpoints with two distinct retained witnesses
other than their own mates. The corresponding exact constructor is
occupied_band_certificate(w); its general loops and the displayed seam table
implement this proof. Finite controls also check each ordered witness.

## 10. Scope of verification and next question

Run develop/check_degree_three_fusion.py with --output
output/degree-three-fusion-controls.json. It independently checks the physical
hypotheses, derives rather than assumes mutual support replacement, counts
each module-selection incidence, verifies the local tile correction and
original receiver ledger, and checks actual protected donors without reuse.
It also checks full mixed-bundle freezing for the supplied examples, including
all rows of the separate ordered adjacent-band certificate. The saved run
passes six four-way widths,192symmetry/alignment images, four non-port corner
joins, five preceding branched chains, six occupied-adjacent-band widths,
and192additional symmetry/alignment images with degree-four contacts.
All-length and general fusion conclusions are the separate proofs above.

Eighteen new Lean4.33.0 declarations and individual axiom audits pass locally.
DegreeThreeFusion.lean checks the four-neighbor degree preservation/obstruction,
the fixed four-corner colored-tile contraction identity for all625local
labelings, its degree-three four-module specialization, exact fusion
cancellation with and without degree-four defects, general protected budgets,
the non-doubled degree-four tax interface and the single-boundary matching
parity argument. The arbitrary-configuration label adapter, geometric donor
protection and all-width adjacent-band certificate remain the written proofs.
Finite local kernel reduction is not an extrapolation of global sample grids.
There is no sorryAx or native_decide; only the standard logical axioms occur.
The scope and execution record is output/degree-three-fusion-formal-check.json.

The prior branching review e9e3e3ea remains the original live task; it does
not cover this later general fusion theorem. Its separate review request is
prepared for the same conversation, to submit after that response; no
independent verdict on this new theorem is claimed.

The remaining question is whether general occupied-degree-three frozen
straight-chamber networks admit a useful decomposition with certified protected
donors, or whether genuinely different contacts need new compensation. This
note does not assume such a decomposition. Submitted manuscripts are unchanged.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
