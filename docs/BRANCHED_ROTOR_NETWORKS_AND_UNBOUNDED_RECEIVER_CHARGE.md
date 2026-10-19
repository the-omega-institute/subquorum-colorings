# Branched compensation and unbounded fully frozen receiver charge

20 October 2026. A connected, fully frozen receiver can have arbitrarily
large original corrected charge even when every endpoint has occupied degree
exactly three. The construction below disproves a constant receiver-charge
ceiling in this restricted setting. Nevertheless a coefficient-one compensation
theorem holds for all admissible networks of the two module types used here,
including branching networks and networks with cycles. The proof assigns a
distinct physical unit donor to every positive module, including modules in
the SAME receiver. The unrestricted grid problem remains open.

## 1. Charges and admissible modules

Use one fixed physical tiling by disjoint 2-by-2 tiles. For a feasible pair
(T,M), put P=V(M). Every selected vertex has at most one occupied neighbor.
Single terminality means every endpoint has at least three occupied neighbors.
For the complete receiver R_H of an endpoint component H, define

    rho_H = |T intersect V(R_H)| + |M restricted to H| - 2|R_H|.

This is the original corrected charge, including saturated-tile transfers,
not a resource-allocation score. If D is the sum of 2-|T intersect tile|
over endpoint-free tiles, the established closed-receiver identity is

    mn/2 - |T| - |M| = D - sum_H rho_H.

The two allowed module types, with arbitrary integer translations and grid
isometries, are as follows.

* A two-leg module is two_leg_case(w,a,b), with w even at least six and a,b
  even at least four, with its actual matching and its two bottom leaf ports.
  The all-phase table in LEAF_SPLICED_TWO_LEG_NETWORKS.md gives its charge
  as +1, -1, or 1-w. Every positive module has the guard described below.
* A rotor has the eight selected sites

      (0,2), (1,1), (2,5), (1,4), (5,3), (4,4), (3,0), (4,1)

  and the four matching edges

      (2,2)--(1,2), (2,3)--(2,4),
      (3,3)--(4,3), (3,2)--(3,1).

  Its four outer endpoints (1,2),(2,4),(4,3),(3,1) are its ports. The four
  central endpoints form a square. Every endpoint has occupied degree three,
  and the matching is forced by the four endpoint leaves. Distinct ports
  have Manhattan distance at least three.

The rotor has four receiver selections in every translation phase. At row
and column phase (0,0) it has five receiver tiles and charge -2. At each of
(0,1),(1,0),(1,1) it has four receiver tiles and charge zero. These are exact
counts of the eight displayed endpoint coordinates: take their coordinatewise
floors after division by two and check which of the eight displayed supports
lie in the resulting tiles. Thus every affine rotor has nonpositive charge.
This finite coordinate identity is a local lemma, independent of network size.

Require precisely the physical splice hypotheses of
LEAF_SPLICED_TWO_LEG_NETWORKS.md, Section 1, for these two module types:
disjoint endpoint sets; all foreign endpoint contacts are declared port-port
splices; each port is used at most once; splice sites are mutually selected
supports; no other support becomes an endpoint; retain all other supports;
use the union of actual matchings; and require final selected feasibility.
Extra selections are allowed only outside the union receivers and with no
endpoint neighbor. A module may have four neighbors. Neither a forest nor
the absence of module cycles is required for the compensation theorem.

## 2. Exact additivity survives branching

**Branched splice ledger.** The complete receiver charge of any connected
admissible network equals the sum of its isolated module charges.

Proof. The receiver-locality lemma in LEAF_SPLICED_TWO_LEG_NETWORKS.md,
Section 2, applies to each isolated module and the final configuration.
Every selected site in an endpoint-bearing tile has its own unique endpoint
neighbor inside the tile. It follows both that retained supports cannot spill
into a foreign-only receiver and that retained supports of different modules
cannot coincide: a coincident site would have two distinct endpoint neighbors.

Each module has at most one port in any tile; a tile has diameter two, whereas
port distances are at least three. In a shared receiver tile its endpoint
set is connected, by the established terminal tile-ownership lemma. Contract
the represented modules. Every incident foreign endpoint edge uses the sole
port of that module in that tile, and the port is used at most once. This
connected incidence graph therefore has maximum degree one. Exactly two
modules share the tile, through one intratile splice. Distinct intratile
splices have distinct shared tiles. This argument does not constrain the
global degree of a module, since its ports are in different tiles.

Writing s for the number of intratile splices gives

    |R_union| = sum_i |R_i| - s,
    |T intersect V(R_union)| = sum_i |T_i intersect V(R_i)| - 2s.

An intertile splice removes no support counted in its own old receiver:
otherwise isolated-module locality would put its endpoint neighbor in that
tile, making the splice intratile. Intratile splices remove exactly the two
mutually selected port sites. Matching sizes add. Consequently

    rho_union = sum_i rho_i.

All endpoint occupied degrees remain exactly three: a splice replaces a
selected neighbor by a foreign endpoint at the same site. A surviving foreign
support cannot touch another module's endpoint, since it already has its own
endpoint neighbor. Extra selections have no endpoint neighbors. QED.

## 3. A distinct donor for each positive module

**Branched compensation theorem.** Every admissible network of two-leg and
rotor modules satisfies

    sum_H rho_H <= N_positive_modules <= D,
    |T| + |M| <= mn/2.

In particular this improves the established 5/6 coefficient by |M|/6 on this
explicit class. No bound on the charge of one receiver is assumed.

Proof. Only two-leg modules can be positive, and each has charge exactly one.
In the reference positive alignment use the selected support x=(3,2), its
endpoint anchor p=(3,1), the opposite tile corner z=(2,3), and the endpoint
guard q=(1,3). The guard has three endpoint neighbors within its own module.
For other positive alignments transport these four sites by a tile-preserving
isometry, using the all-phase classification of the two-leg module.

The support x is not a port support: for minimum leg height four it is
distance two from that leg's bottom port, and greater heights only separate
them further; the opposite port is farther away. It therefore survives every
allowed splice. The guard is not a port; its three endpoint neighbors remain,
and its occupied degree stays three. The two corners adjacent to x are blank,
as x already has its unique occupied neighbor p outside the tile. The corner
z is blank because it touches q, which already has three occupied neighbors.
Thus the tile of x is endpoint-free and contains exactly one selection. It
supplies one genuine deficit unit, and is the saturated-endpoint guard donor
of TWO_LEG_DEGREE_THREE_COVERAGE_OBSTRUCTION.md. This argument retains the
donor after joining and does not require exclusion of other donor rules.

The chosen supports x from different positive modules are distinct: each
retained support touches its own endpoint, and coincidence would give two
endpoint neighbors. If two chosen donor tiles coincided, their sole selected
site would coincide, a contradiction. This proves distinctness even for
positive modules in the same final endpoint component. Hence these are
N_positive_modules different actual unit donors. Every other endpoint-free
tile has nonnegative deficit, so N_positive_modules<=D. Additivity and the
nonpositive charges of all other modules give the first inequality. Substitute
in the closed-receiver identity to obtain the half-area bound. QED.

After any B valid unit reservations at most B chosen unit donors disappear.
At least N_positive_modules-B>=sum_H rho_H-B=q distinct positive residual
tiles remain. The earlier first-failure theorem therefore also excludes a
target-preserving local-quota failure for q<=5 in this branched class: q<=4
is already excluded, while the three remaining first-q5 motifs have only
three or four positive tiles. This conclusion uses the same previously proved
first-failure classification as the leaf-spliced path theorem. It is not a
general allocation theorem for larger q or for arbitrary endpoint geometry.

## 4. A fixed charge-two star of occupied degree three

Attach four copies of two_leg_case(w,4,4) to the unshifted rotor, for any even
w>=6, by these affine maps on (row,column), in the order north/east/south/west:

    (r,c) -> (r-4, c+2-w),
    (r,c) -> (c+2-w, 9-r),
    (r,c) -> (9-r, c+2),
    (r,c) -> (c+2, r-4).

Keep the union matching and remove supports occupied by another module's
endpoints. Each attached module has charge +1; the rotor has charge -2.
There are exactly four intratile splices. One splice and its retained support
pattern can be read off at the rotor port (1,2) and the attached port (0,2);
the other three are its quarter-turn images about (2.5,2.5). Away from the
rotor, the four two-row bars lie on four sides of the central gap, and their
legs run toward the rotor along the two ends of their bar. The nonincident
arms have no endpoint contacts or coincident/adjacent surviving supports;
their separation is smallest at w=6, and increasing w extends the bars away
from one another. Equivalently these facts follow by substituting the four
displayed maps into the bar/leg coordinate formulas in two_leg_case.

The star has

    |P|=8w+32, |M|=4w+16, |T|=40,
    |R|=2w+21, |T intersect V(R)|=28, rho=2.

For w=6 it fits a 14-by-14 rectangle after translation by (4,4): 80 endpoints,
40 actual matching edges, 40 selections, 33 receiver tiles and charge two.
Its endpoint graph is a tree of five even-order modules with unique internal
matchings. The bridge argument in Section 5 proves global matching uniqueness
and thus excludes all mixed promotion bundles. This already refutes the
charge-at-most-one assertion within occupied-degree-three frozen geometry.

## 5. All-length family with unbounded charge

Fix S to be the star with w=14. It has 144 endpoints, 72 matching edges,
40 supports, 49 receiver tiles, 28 receiver selections and charge two.
Its free ports are (0,-11),(-11,5),(5,16),(16,0), and its coordinate bounding
box is [-12,17] in both directions. It is invariant under the half-turn
(r,c)->(5-r,5-c).

Let C be two_leg_case(14,4,4) transported by (r,c)->(c-25,r).
Its ports are (-24,4),(-11,4), its row support is [-25,-10], and it has
34 endpoints, 17 matching edges, 10 supports, 11 receiver tiles,
four receiver selections and charge -1. Put F(r,c)=(r-40,5-c).
For any integer k>=1 take

    S_j=F^j(S), 0<=j<k,
    C_j=F^j(C), 0<=j<k-1.

Each C_j joins S_j and S_(j+1). For j=0 the two splice edges are

    (-11,5)--(-11,4), (-24,4)--(-24,5).

Both are intratile. Here is a complete boundary check for the only upper
junction, before supports at the two splice sites are removed:

| Module | Boundary row | Endpoint columns | Selected columns |
|---|---|---|---|
| S | -12 | none | 5,7,9 |
| S | -11 | 5,6,7,8,9 | 4 |
| S | -10 | 8,9 | 6 |
| S | -9 | 8,9 | none |
| C | -13 | 0,1 | none |
| C | -12 | 0,1 | 3 |
| C | -11 | 0,1,2,3,4 | 5 |
| C | -10 | none | 0,2,4 |

The three overlapping rows and their one-row halos are all displayed;
S has no sites at rows less than -12 and C has none at rows greater than -10.
The table shows exactly one foreign endpoint edge, the
upper splice. After removal of S's support (-11,4) and C's support (-11,5),
the retained perpendicular supports (-12,5) and (-10,4) are on opposite sides.
No surviving selection gains a second occupied neighbor. All cross-module
distances relevant to feasibility are visible in this table.

The lower junction is its image under V(r,c)=(-35-r,c): V(C)=C, and the
half-turn symmetry of S gives V(S)=F(S). The same check therefore proves
the second splice. S_j has rows [-12-40j,17-40j] and C_j has rows
[-25-40j,-10-40j]. Nonneighbor stars and connectors are separated by at least
one blank row; the two junctions are disjoint. Applying F^j repeats the same
local check at every j, so it proves feasibility and the absence of other
contacts for every length, independently of finite sample checks.

The primitive module graph is a tree: replace each S_j by its rotor with
four two-leg leaves, and connect consecutive such stars through C_j. Each
primitive module has even endpoint order and unique matching. The rotor's
matching is forced by its four leaves. The uniform two-leg frozen theorem,
together with the degree-three matching uniqueness criterion in
DEGREE_THREE_CHAMBER_NETWORKS.md, Section 3, gives uniqueness for each
two-leg module; isometries preserve it. Every intermodule edge is a bridge
separating even-order vertex sets. A perfect matching cannot use such an edge,
because it would leave odd unmatched order on either side. It follows that
the union of the actual module matchings is the unique global perfect matching.

Every endpoint has occupied degree exactly three. The same criterion now
excludes EVERY nonempty feasible mixed promotion bundle. Explicitly, each
promoted endpoint must lose its mate and at least one other occupied neighbor.
On the selected matching edges these further removed mates give a directed
graph with positive outdegree, hence a cycle; switching along that cycle
would produce a second perfect matching, a contradiction. This does not
assume the promoted endpoints have one color.

The exact splice ledger gives rho=2k-(k-1)=k+1, hence unbounded charge.
Translate the entire family by (12+40(k-1),12), an even vector, into a
(40k-10)-by-30 rectangle. Direct counts give

    |P|=178k-34, |M|=89k-17, |T|=46k-6,
    |R|=58k-9, |T intersect V(R)|=28k,
    rho=k+1, |T|+|M|=135k-23,
    mn/2=600k-150, D=466k-126.

There are 4k positive modules and therefore at least 4k distinct unit donors
by Section 3. At k=4
there is a single fully frozen receiver with rho=5, 678 endpoints, 339
matching edges, 178 selections and 223 receiver tiles. It still has sixteen
chosen distinct donors (thirty-two actual guard donors) and D=1738. Thus it
is not a counterexample to compensation, local-quota coverage or the grid
inequality. It disproves a receiver ceiling and shows why a scalable,
non-reusing compensation argument is necessary even at occupied degree three.

## 6. Verification and remaining scope

The coordinate constructors are develop/rotor_networks.py. Run

    python3 develop/check_branched_rotor_networks.py \
      --output output/branched-rotor-network-controls.json

The checker independently checks physical feasibility, actual matching,
all foreign contacts, mutually consumed supports, the original receiver
ledger, exact occupied degrees, all-endpoint freezing, and distinct chosen
donors inside the same receiver. Controls cover all four rotor phases, six
star widths from six through forty, nineteen chain lengths through sixty-four
(charge sixty-five), and thirty-two tile-preserving symmetry images. The
charge-five witness is supplied as coordinates and actual matching edges.
These controls test the separate arbitrary-length argument above; they do
not prove it by extrapolation.

The local Lean 4.33.0 check passes 104 declarations and individual axiom
audits. RotorStarObstruction.lean checks the ACTUAL 14-by-14 charge-two star:
120 different occupied coordinates, feasible selections, its actual matching,
occupied degree exactly three, all eighty endpoint freezing witnesses,
exclusion of every mixed bundle, and original receiver counts and charge.
BranchedRotorNetworks.lean proves the arbitrary-finite-list positive-module
bound, donor-tile injection interface and arbitrary-length chain arithmetic.
There is no sorryAx or native_decide; axioms are the standard propext,
Classical.choice and Quot.sound. The full affine-chain geometry and the
physical module-to-donor adapter remain the written proofs above. The record
is output/branched-rotor-network-formal-check.json. No Mathlib is rebuilt.

The preceding leaf-spliced path theorem has independently received ACCEPT;
that review does not cover this new branching extension. Further review
is recorded separately. General grid coverage,
the unrestricted coefficient-one bound, and Rafik's proposed triple equality
are still open. Submitted manuscripts are preserved.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
