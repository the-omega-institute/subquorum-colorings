# Exact charge and compensation for leaf-spliced two-leg networks

20 October 2026. This treats a geometric class with arbitrarily many chambers,
mixed matching directions, bends, and connections between formerly separate
modules. The argument uses actual endpoint receivers and their original corrected
charges. It does not replace the open general coverage problem by an allocation
score. In this class each connected path network has charge at most one, and
each cycle network has nonpositive charge. Positive networks have genuine,
distinct unit donors. Thus the coefficient one half-area bound holds on the
stated class, improving the established coefficient five-sixths by |M|/6 there.
Neither the unrestricted grid bound nor all degree-three networks are settled.

## 1. Modules and precise splice assumptions

A module is an integer translate and grid isometry of two_leg_case(w,a,b),
where w is even and at least six, and a,b are even and at least four. It retains
the selected supports and actual matching in
TWO_LEG_DEGREE_THREE_COVERAGE_OBSTRUCTION.md. Its two ports are the bottom
endpoints of its two legs, not arbitrary endpoints of the matching. Each port
is a leaf of its module's induced endpoint graph, with one endpoint mate and
two selected supports. The two ports have Manhattan distance at least five.

Take finitely many modules (T_i,P_i,M_i) in one fixed physical 2-by-2 tiling.
Require the following physical conditions, before drawing conclusions:

1. The P_i are disjoint. Every endpoint edge between different modules is a
   declared splice u--v between their ports; each port is used at most once.
2. For each splice, v is one of u's original selected supports and u is one
   of v's original selected supports. These two sites become endpoints of
   the other module. No other original selected support is an endpoint.
3. Keep all remaining selected supports, and use exactly the union of the
   actual M_i. The resulting selected set is feasible. Extra selected vertices
   may be added only outside the union of the endpoint-bearing receiver tiles
   and must have no endpoint neighbor. All endpoints belong to the modules.

These are checkable geometric hypotheses, not assumed charge inequalities.
The finite graph on modules has degree at most two. Each of its connected
components is a path, an isolated vertex, or a cycle (two parallel splice
edges give the possible two-module cycle).

Each remaining support still touches its original endpoint. Two retained
supports from different modules cannot coincide or be adjacent: either event
would violate feasibility, because each already has its own endpoint neighbor.
Nor can a retained foreign support touch a module endpoint, for it would then
see two endpoints. At a used port a selected neighbor is simply replaced by
an endpoint at the same site. All endpoint occupied degrees therefore remain
exactly three. In particular the complete-receiver partition is valid. The
bound below does not require that the spliced configuration stay fully frozen.

## 2. A local receiver fact

**Receiver-locality lemma.** In every feasible single-terminal configuration,
a selected vertex in an endpoint-bearing physical tile is adjacent to an
endpoint inside that tile. Consequently that endpoint is its unique occupied
neighbor.

**Proof.** Otherwise the tile's endpoint must be the corner opposite the
selection. Neither intervening corner can be an endpoint, by the supposed
nonadjacency. Neither can be selected, since it would touch both the original
selection and the opposite endpoint. Thus both are blank. The endpoint has
two blank internal neighbors and at most two exterior occupied neighbors,
contradicting single terminality. QED.

This also forbids receiver spill: a retained support of module i cannot sit
in another module's receiver without also sitting in its own receiver. Its
unique occupied neighbor belongs to P_i, so the lemma puts that P_i inside
the tile. Extra selections outside all module receivers do not alter this.

## 3. All alignment phases of one module

Set h=(a+b)/2. For the unrotated constructor, translate by (epsilon,delta)
with epsilon,delta in {0,1}, in addition to any even translation. Its exact
receiver counts are:

| Row phase | Column phase | Receiver tiles | Selected vertices in receiver | Original corrected charge |
|---|---|---|---|---|
| 0 | 0 | w/2+h+1 | h+4 | 1 |
| 0 | 1 | w/2+h | h | -1 |
| 1 | 0 | w+h | h+2 | 1-w |
| 1 | 1 | w+h-2 | h-2 | 1-w |

Here |M_i|=w+h-1 in every phase, and the charge is
t_i+|M_i|-2r_i. To count the tiles, separate those meeting the two-row bar
from the tiles meeting the two descending legs, counting their intersections
once. In row phase zero the bar occupies one tile row and contributes w/2+1
or w/2 tiles according to column phase; its remaining leg tiles contribute h.
In row phase one the bar occupies two tile rows, contributing w+2 or w;
the remaining leg tiles contribute h-2. The supports counted in the table
are the two upper supports, alternating outer/inner leg supports, and the two
bottom supports; inspecting their tile with respect to their unique endpoint
gives h+4,h,h+2,h-2 respectively. Substitution gives the final column.
An arbitrary grid isometry is a tile-preserving isometry followed by one of
these four phase changes, so these are all possibilities.

In particular every isolated module charge is either +1 or at most -1.
In its +1 phase each of its two port tiles contains that port and BOTH of
its selected supports; its actual mate is outside that tile. This statement
is preserved by tile-preserving rotations and reflections.

## 4. Exact charge additivity under splicing

**Splice ledger lemma.** The complete receiver charge of a connected network
is exactly the sum of its isolated module receiver charges.

**Proof.** If a physical tile meets multiple modules, the single-terminal
tile-ownership lemma makes its endpoint set connected within the tile.
Every edge joining modules in it is a splice. A module has at most one port
in that tile, since its two ports have distance at least five. That port has
at most one foreign endpoint neighbor. The connected graph on the represented
modules therefore has maximum degree one: precisely two modules meet, and
their unique intratile splice accounts for the overlap. Distinct intratile
splices have distinct physical tiles. Write s for their number.

The union receiver has sum_i r_i-s tiles. Each intratile splice removes two
original selected supports counted in the isolated receiver counts. A support
removed by an intertile splice was not counted in its own module receiver:
otherwise receiver locality in that original module would put its unique
endpoint neighbor inside the tile, contrary to the splice crossing tiles.
Receiver locality also rules out retained support spill between receivers.
Thus the union has sum_i t_i-2s selected vertices, and its matching has
sum_i |M_i| edges. Consequently its ORIGINAL corrected charge is

    (sum_i t_i-2s)+sum_i |M_i|-2(sum_i r_i-s)
      = sum_i (t_i+|M_i|-2r_i).

This uses closed receivers, so all saturated-to-deficient transfers are
included. It does not add raw charges of overlapping tiles. QED.

## 5. Positive modules cannot be neighbors

Suppose two +1 modules were joined at ports u,v. In the first module v is
a selected support of u and is in u's physical tile; the same is true in
the second module. The splice endpoints therefore share one physical tile.
Its other two corners are the two selected supports not consumed by this
splice. They remain selected, are adjacent to each other, and each is adjacent
to one of u,v. Each has at least two occupied neighbors, violating feasibility.
Thus no two positive modules are adjacent in the module graph. This is a
local geometric obstruction, not an inference from a finite search.

Let c_i be consecutive module charges on a path. Each c_i<=1 and every
adjacent pair satisfies c_i+c_(i+1)<=0: either both are negative, or one is
at most -1 and the other at most +1. Pair consecutive modules. Even paths
have total charge at most zero, and odd paths at most one. For a cycle, sum
all adjacent-pair inequalities to obtain 2 sum_i c_i<=0, including the
two-module case. The splice ledger proves the asserted receiver bounds.

A positive path necessarily contains a +1 module, and in fact for positive
integer total it must be odd, alternate +1,-1, and have +1 modules at both
ends. To see the stronger assertion, let p,n count positive and negative
modules. Nonadjacency gives p<=n+1, while sum c_i<=p-n. Positivity forces
p=n+1, no charge below -1, and the alternating arrangement.

## 6. Genuine unit compensation and the coefficient-one theorem

Every +1 module retains the degree-three endpoint guard at its original
Q_(1,1), or its transformed copy: selected x=(3,2), endpoint anchor p=(3,1),
opposite corner z=(2,3), guard q=(1,3), and q's three other endpoint neighbors.
The selected x is not a port support consumed by a splice, even at leg
height four. All these occupied vertices remain. The guard is not a port,
so its occupied degree stays three. Anchor and guard belong to the same
complete network component. The degree-three guard lemma therefore makes
this tile endpoint-free with exactly one selected vertex and actual capacity
one, regardless of other modules nearby.

Choose one such tile for each positive connected network. Two different
networks cannot choose the same tile: it has a sole selection with a unique
occupied endpoint anchor, which identifies its endpoint component. Thus the
chosen donors are physical distinct unit resources. Negative networks supply
only their own original negative charges; they are not also spent as donors.
With D the total actual deficit on all endpoint-free tiles, the receiver
bound and these donors give

    sum_H rho_H <= number of positive networks <= D,
    |T|+|M| <= mn/2.

This handles a union of differently oriented networks and additional feasible
selections outside their receivers with no endpoint neighbor. Relative to
|T|+(5/6)|M|<=mn/2 it recovers the whole |M|/6 on this class. It does not
assert that an arbitrary initial configuration reduces to this modular class.
In particular a single charge-five frozen receiver cannot be such a network;
five separate positive networks can occur, but have five distinct real donors.
There is a reservation-aware consequence for the three first-charge-five
resource motifs. Choose one distinct unit donor per positive network, and
write N_+ for their number. The proof gives rho<=N_+. After ANY B distinct
valid slot reservations, at most B of these chosen unit donors disappear.
There remain at least N_+-B>=rho-B=q positive residual tiles, all distinct.
But a target-preserving local-quota failure at q=5 has one of the three
classified shapes, supported on only three or four positive residual tiles.
That is impossible. For q<=4 the earlier threshold already excludes a
target-preserving failure. Therefore this geometric class satisfies q<=A
whenever q<=5, including prior reservations, not only the restricted B=0
donor-free search. At higher residual charges the first-shape argument does
not apply. The three motifs remain open for general endpoint geometry.

## 7. All-length sharp charge example and validation scope

For any N>=1 take N copies of two_leg_case(6,4,4). Translate copy i by
(0,5i) when i is even; for odd i use (r,c)->(9-r,c+5i). Consecutive ports
at column 6+5i lie at rows four and five and are spliced. Keep all actual
matching edges and delete from the supports precisely the sites occupied by
the other modules. No other module contacts occur. The supports between
opposing bars are separated; at a splice their retained perpendicular
supports lie on opposite sides. Hence the resulting configuration is feasible
with occupied endpoint degrees exactly three.

Every module matching is unique: the uniform two-leg frozen theorem and
the occupied-degree-three uniqueness criterion in
DEGREE_THREE_CHAMBER_NETWORKS.md, Section 3, imply this for every base
module, and grid isometries preserve it. Each intermodule edge is a bridge of the
endpoint graph, connecting modules of even order, so no perfect matching can
use that bridge: either side contains an even number of vertices. Inductively
the union matching is the unique perfect matching. The degree-three matching
criterion excludes every mixed promotion bundle, not only one-color bundles.
The module charges alternate +1,-1. Therefore the complete receiver charge
is exactly one for odd N and zero for even N. The counts are 18N endpoints,
9N matching edges, and 8N+2 selected supports. This realizes arbitrarily
large, fully frozen, multichamber positive receivers, while keeping their
charge bounded by one.

The accompanying checker verifies the four phase counts, actual splice and
tile-overlap ledger, the all-length construction at recorded sample lengths,
and donor non-reuse across separated networks. A scoped Lean file separately
checks the all-length integer path argument and the charge cancellation
interface. The geometric proofs and all-length coordinate construction are
the written arguments above; finite experiments do not replace them. No
submitted manuscript is changed. The physical controls cover96phase cases,
all6561local label/exterior-count cases (625feasible terminal),19sample path
lengths through64modules,152symmetry images,76phase/splice cases including
intertile joins, and four separated networks with distinct compensation.
All128subsets of seven chosen donor units check surviving distinct capacity;
120have residual charge at most five. One nonzero-reservation q5case is also
checked by exact local-quota matching, alongside the general counting proof.
Seventeen scoped Lean4.33.0 declarations compile locally and pass individual
axiom audits. The path estimate is an induction over arbitrary finite lists,
not a list of tested path lengths. No sorryAx or native_decide is used;
the axioms are standard propext/Quot.sound, with Classical.choice additionally
in the adjacent-module case split. The full geometric adapter and cycle
summation retain written proofs. The original local-quota/batch review
f96f7cd4 completed ACCEPT; it does not cover this later theorem. Its own
review f8082c0a-3c2d-4ea7-97f6-5ec40678db16 completed ACCEPT. The original
streaming execution81548lost its connection before receiving the answer;
the authoritative response was recovered from that same task. The assessment
in docs/reviews/2026-10-20-leaf-spliced-network-assessment.md records its
scope and dependencies. Exclusion of other donor rules after splicing is
not needed: the proof requires one surviving actual donor, not completeness
of the donor list.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
