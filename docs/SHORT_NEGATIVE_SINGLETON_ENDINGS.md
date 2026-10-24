# Short negative-singleton gates: exclusion and nonreusing resolution

21 October 2026. The unrestricted mixed U/rotor allocation mu=N+R-G>=0
and rectangular-grid triple equality remain OPEN. This note excludes an
incident-length-four negative singleton consumer and resolves the
incident-length-six case into an injective activation or a persistent pair.
The positive activation targets are disjoint from ALL established S/P/R
targets. A south-terminal companion also supplies an unmarked-owner count,
with each such owner counted once.

The model, mandatory original supports and fixed physical tiles are those of
[source retention](SOURCE_RETENTION_HORN_CLOSURE.md). Widths are even>=6,
independent legs even>=4; all finite source counts, phases, isometries and
rotors are allowed. Occupied includes unconsumed selected supports. Sources
retain their original endpoints and matchings in every complete extension.

## 1. The negative singleton and its forced transverse owner

Normalize a positive producer A=U(w,L,K), its marked gate t=(3,2), and
Q={2,3}x{2,3}. Suppose t's actual consumer is an ORIGINAL negative-U
singleton. Every own endpoint neighbor of t is outside Q. The west position
is A's endpoint (3,1), leaving only south. The original endpoint graph has
no isolated endpoints, so that south neighbor exists. Thus this particular
gate consumer has own endpoint degree one and is a U terminal. An arbitrary
original tile singleton need not be a terminal: an upper bar corner can
also be a tile singleton, but cannot fit at this gate.
The leftward-bar terminal orientation has the positive regular1P2T profile;
the negative orientation is therefore exactly

    B=U(W,b,e), B(r,c)=(b+3-r,c+1).                    (1)

B's original support p=(2,2) must be consumed: it has B's terminal t and
A's endpoint (2,1) as occupied neighbors. The established all-dimension
transverse-tip theorem forces the owner

    C=U(V,h,f), C(r,c)=(c+1,h+2-r), 4<=h<=w-4.       (2)

C's original support y=(3,3) has its own anchor (2,3) and B's terminal
(3,2) as occupied neighbors. It must be consumed by a fourth owner D.
Neither B nor C nor A has an endpoint at y. The following analysis allows
all additional owners; the displayed partial family need not be feasible
by itself.

## 2. Incident length four has no complete extension

If b=4, B's bar is rows6,7,columns2..W+1. C's bar includes row6, since
V>=6, at columns h+1,h+2. Endpoint disjointness forces h>W, hence h>=W+2.

The entire boundary of [2,6]x[2,W+1] is then endpoints of B or C: top is
C's incident stem, bottom B's upper bar, left B's incident leg, right B's
far leg. The far leg is long enough regardless of e, since e>=4. Neither
owner has an interior endpoint. The forced point y=(3,3) lies strictly
inside, in a three-row interior.

Any foreign source with an interior endpoint must have its entire connected
endpoint graph inside, because a lattice path cannot cross this endpoint
boundary without sharing an original endpoint. No U fits in three rows
in any orientation; its minimum row extent is five. No rotor fits either;
its extent is four. Thus D cannot exist. This is a general exclusion of
b=4, not a bounded placement-search conclusion.

## 3. Incident length six has three necessary U forms

Let b=6. At y, north belongs to C and west to B. Its new owner's own
endpoint neighbors can only be east or south. U endpoints therefore have
only three possible roles: an east terminal, south terminal or upper
corner with both neighbors. The three-neighbor bar/stem junction is
excluded, as is every interior bar point.

All four rotor-tip footprints are excluded directly. In terms of the
canonical rotor P={(1,2),(2,2),(2,3),(2,4),(3,1),(3,2),(3,3),(4,3)}, their
maps and fixed collisions are

| Map | Collision |
|---|---|
| (r,c)->(r,c+2) | C(2,4) |
| (r,c)->(6-r,c+2) | C(2,5) |
| (r,c)->(r+2,c+1) | B(5,2) |
| (r,c)->(r+2,5-c) | B(4,2) |

Rotor central endpoints have three own endpoint neighbors and were already
excluded by the two fixed foreign neighbors. This exhausts the rotor roles.

For U owners the only remaining forms, after naming the incident leg, are

| Case | Original owner and frame | Necessary conditions |
|---|---|---|
| E | U(d,g,k), (r,c)->(c+2,g+3-r) | W<=g<=h-4 |
| S | U(d,4,4), (r,c)->(7-r,c+2) | d<=min(h-2,W-2) |
| H | U(d,4,k), (r,c)->(r+3,c+2) | d<=h-2 |

E and S are positive sources, H negative. The bounds are necessary, not
sufficient for complete realizability.

For E the incident stem occupies row3,columns3..g+3. Avoiding C's bar
gives g<=h-4. An upward bar would meet C's row-two stem, so the bar points
down. Its width is at least six, so it has endpoint (8,g+2). B owns
row8,columns2..W+1. Disjointness gives g+2>W+1 and evenness yields g>=W.
This last bound strengthens the earlier proposed g>=4 classification:

    E requires g>=W>=6 and w>=h+4>=W+8>=14.          (3)

For a south terminal, incident length at least six would reach B's row8
bar at column3; hence its leg is four. A leftward bar would meet B's
near stem, so it points right. Its bar must stop before C's bar, giving
d<=h-2. If its far leg were at least six, it would contain (2,d+2),
already in C's row-two stem. Thus that leg is also four, proving S's
stated exact dimensions.

Its width is also smaller than B's. If d>=W, S's row-six bar would contain
B's far-leg endpoint (6,W+1). Evenness therefore gives d<=W-2, so this
branch requires W>=8. This is an additional dimension restriction beyond
the earlier proposed classification.

A horizontal upper corner also has incident leg four, since a longer
leg would meet B's row8 bar. Avoiding C's bar gives d<=h-2. A vertical
upper corner would have bar columns3,4,rows3..d+2 and would meet B's
row8 bar for every allowed d>=6. This proves the three-form classification
without an upper dimension or source-count bound.

## 4. Positive cases: a new joint activation injection

In E and S, y is an original positive terminal. Its two original intratile
supports are (3,2), owned by B, and (2,3), owned by C. The terminal is
therefore activated, counted ONCE in the existing Aactivation ledger.

These new targets are injective across actual b=6 marked-side claims.
The target terminal and its tile identify its two intratile supports.
Their original endpoint roles distinguish B from C: B's point is an
original terminal, while C's is an internal straight-leg endpoint. These
roles fix the normalized frame and hence the gate t. Of the gate's two
external anchor positions, (4,2) already belongs to negative B; only (3,1)
can belong to the positive producer. Unique original endpoint ownership
and canonical-gate uniqueness determine the original marked side.

The new activation targets are disjoint from S/P targets. If an old target
were the same terminal, the forced old producer frame would be

| New companion | Old channel | Forced old positive-producer frame | Collision |
|---|---|---|---|
| E | S | (r,c)->(5-c,r) | A(0,1) |
| S | S | (r,c)->(r,5-c) | A(0,1) |
| E | P | (r,c)->(r,g+5-c) | A(0,g+4) |
| S | P | (r,c)->(9-c,r) | A(3,1) |

For the first row the colliding original endpoint is (1,5); for the
second it is (0,4); both exist at every allowed width. The third uses
(0,1) and g+4<=h<=w-4, so its image lies on A's original top bar. The
fourth uses original endpoint (1,6), available at every allowed width.

The putative old producer cannot be A itself. The first, second and
fourth frames have original bar endpoints in column zero, whereas A has
no endpoint there. In the third frame the putative bar's maximum column
is g+4<w, whereas A's bar reaches w. Thus the displayed collisions are
genuine different-owner collisions, not merely a change of chart of A.

The new targets are also disjoint from ALL R targets. An R target has
an intratile support owned by the original rotor at its preceding gate.
Both intratile support owners here are U sources B,C, so equality would
violate unique endpoint ownership. This closes the mixed R collision
that was not part of the earlier short-singleton proposal.

Let q0 count the established positive/rotor-consuming marked sides and
q6 the new positive-companion b=6 claims. Then

    q0+q6<=Aactivation.                              (4)

This is an allocation into the existing activation pool; it is not an
additional copy of that pool.

In S there is a further persistent fact. The endpoint boundary of
[2,6]x[3,d+2] consists of C's row-two stem and S's bar and two legs.
Its three-row interior contains BOTH canonical gates of S, at (4,4) and
(4,d+1). The same enclosure argument forbids foreign endpoints at either
gate in every complete extension. Their original selected supports may
remain; it is endpoint consumption that marks a gate. Thus S is permanently
unmarked. Let n0 count DISTINCT positive owners certified this way, not
terminal claims: two terminal claims on one owner give only one owner.

## 5. Negative case: a persistent pair, not a second payment pool

In H the pair (H,B) is precisely the lower enclosure of the
[corridor theorem](PERSISTENT_CORRIDOR_AND_STRIP_CAPACITY.md), with

    H=U(d,4,k)+(3,2), B(r,c)=(9-r,c+1),
    m=min(d+2,W+1).

Hence the tiles {4,5}x{4+2j,5+2j}, 5+2j<=m-1, are permanent original
irregular2P0T pairs. In particular {4,5}x{4,5} is always present and gives
two actual geometric units.

Assign each actual H claim this first pair. Its original owner and first
lower-bar pair fix the bar end and upper corner y. The adjacent B terminal
t, C straight-leg role, and positive anchor then fix the original claim,
as in Section4. Thus the first-pair assignment is injective. Opposite
corners have different first pairs, even at d=6: columns{4,5} and{d,d+1}.

Let s count these resolved negative H claims, and p count the UNION of
distinct physical lower pairs from the corridor enclosure theorem. Then

    s<=p.                                            (5)

These are already part of p. They MUST NOT also be added as a new s-unit
pool in the reserve identity. Lower pairs are disjoint from upper pairs,
caps and m8 receipts by the original-owner/profile proof in that theorem.

## 6. The reduced remaining target

Partition actual marked sides into q=q0+q6 joint activation claims,
c certified full-bar cap claims, s negative H claims and t all remaining
negative-U claims. Their original gate-consumer roles make these classes
disjoint. Then

    G=q+c+s+t<=2(N-n0), q<=Aactivation, s<=p.

The bound on G uses only that the n0 distinct positive owners have both
sides unmarked. The nonreusing reserve floor still reads

    2R>=Aactivation+m8+c+2p+2u.

The established exact reserve R=S+C-K is integral, so mu=N+R-G is integral.
Combining these inequalities in the same family gives

    2mu>=2n0+2u+2p+m8-s-t
        >=2n0+2u+p+m8-t,
    mu>=n0+u+ceil((p+m8-t)/2).                       (6)

Thus the explicit sufficient condition is now

    t<=2n0+2u+p+m8+1.                               (7)

Here t excludes the resolved length-six positive and negative branches;
length-four singleton consumers cannot occur. No activation, lower pair,
unmarked owner or core reserve is duplicated. If (7) holds, the established
sigma>=mu inequality gives coefficient one on the same covered complete
source configurations, improving the previous5/6 coefficient by|M|/6.
This does not prove universal coverage or a grid decomposition theorem.

## 7. A tight return obstruction and a complete realized H branch

There is a further genuine no-extension stencil. Prescribe just

    B=U(6,6,4), B(r,c)=(9-r,c+1),
    C=U(10,8,4), C(r,c)=(c+1,10-r),
    H=U(6,4,4)+(3,2).

Their endpoints are disjoint. H's mandatory support x=(8,8) has three
fixed endpoint neighbors: north(7,8) from H, west(8,7) from B, east(8,9)
from C. It must be consumed. Its new owner's only own endpoint neighbor
is south(9,8), so it is a U terminal or rotor tip. Every allowed U terminal
continues straight for at least three further edges, including (11,8),
already C's far-leg endpoint. The two south rotor-tip footprints are
(r,c)->(r+7,c+6) and (r,c)->(r+7,10-c). They respectively meet C(10,9)
and B(9,7). No owner can consume x, so NO complete extension by arbitrary
allowed U and rotor sources exists. This is a general geometric proof;
a preceding bounded UNSAT search merely suggested where to look.

Increasing C's width to14 removes that particular obstruction and admits
the following complete connected eleven-source witness. Every row specifies
an original U(width,near,far) with its original matching and ALL supports.

| Owner | Dimensions | Original-coordinate map |
|---|---|---|
| A | (12,4,4) | (r,c) |
| B | (6,6,4) | (9-r,c+1) |
| C | (14,8,4) | (c+1,10-r) |
| H | (6,4,4) | (r+3,c+2) |
| E | (6,4,4) | (r+5,c-5) |
| F | (6,4,8) | (r-4,c-6) |
| J | (6,6,6) | (c+15,r+6) |
| K | (8,4,8) | (5-c,17-r) |
| L | (10,4,4) | (6-r,c+10) |
| M | (10,4,6) | (14-r,c-2) |
| Q | (10,6,6) | (21-r,c-5) |

Independent reconstruction gives278disjoint endpoints,139unchanged unit
matching edges and62retained selected supports, each of occupied degree
one. Every endpoint has occupied degree at least three. The endpoint graph
is connected and the least feasible Horn closure of{A,B} WITHIN this
manifest is all eleven sources. No source-count minimality is claimed.

B consumes A's gate with an original negative singleton; C consumes p and
H consumes y. The first lower tile {4,5}x{4,5} is exactly H's original
irregular2P0T pair with no other endpoint or selected point in that tile.
Thus the negative branch is a complete actual occurrence, not merely a
partial role configuration. The exact ledger is

    N=3, G=2, Aactivation=4, U0=2, Z0=0,
    L1=5, L2bar=19, L2mutual=0, L3=3,
    2R=4+2+5+38+3=52, R=26, mu=27.

The example has positive margin and is not an allocation counterexample.
No complete E or S branch is claimed from the partial role controls.

## 8. Verification and limitations

develop/check_short_negative_singleton_endings.py independently reconstructs
the matching/support geometry. Its controls include32endpoint-disjoint
length-four enclosures,72length-six fixed patterns and480distinct anchored
U role candidates.728endpoint-disjoint PARTIAL next-owner patterns split
into461E,42S,225H; all four rotor-tip footprints collide.60old-P frame
controls include the self-owner exclusion, and9312integer count controls
check the rounded residual bound. A separate complete certificate checks
all32phase/isometry images of the eleven-source H witness, eight preserving
the displayed positive/negative branch and its permanent lower pair.

formal/SubQuorum/ShortNegativeSingletonEndings.lean proves unbounded
endpoint-coordinate collision, length-four boundary/interior, the stronger
E width bound, exact S leg lengths and the residual integer implications.
The connected-source enclosure theorem is already formalized in
PairTransferProtectedDefects.lean. Source-role exhaustion, the new joint
injection, its physical/count adapters and first-pair deduplication remain
written proofs with independent finite controls. There is no end-to-end
formalization of source extensions or grid equality.

formal/SubQuorum/ShortNegativeSingletonWitness.lean additionally checks the
concrete eleven-source original matching, mandatory-support feasibility,
actual singleton/transverse/corner chain and irregular lower-pair profile
by ordinary kernel reduction. All eight declarations and their axiom checks
PASS locally in session82522, exit0, with NO axioms. Connectedness, Horn closure and the global
reserve adapters are independently checked Python, not part of that finite
Lean certificate. Execution and axiom results are recorded separately.

The earlier research response b90c01ca proposed the length-four exclusion
and length-six classification with S/P disjointness. This reconstruction
adds E's bound g>=W and w>=14, explicit exclusion of self-producer cases,
joint disjointness with R, and the combined n0/p/m8 residual bound.
The corridor reviewe2d1db08 predates this note. It completed REVISE with one
endpoint/support ownership correction and an explicit reserve-integrality
clarification, now applied to the previous notes. Its response does not
review this new theorem. Follow-up cc4dd625, original stream13551, separately
reviews those repairs and this entire note; its actual verdict is tracked
in output/short-negative-singleton-review.json.

The subsequent [all-length companion theorem](ALL_LENGTH_SINGLETON_COMPANION_INJECTION.md)
extends the E/S activation injection to arbitrary incident lengths. It also
finds a mandatory C support INSIDE the displayed S enclosure, proving that
S with incident leg four has NO complete extension. Thus the unmarked-owner
implication here is valid but vacuous on complete S4 families; the partial
S controls are not actual examples. At b=6 only E or H can occur in a
complete family. This later exclusion is not part of the original review packet.

Longer negative singleton consumers, filled-corridor continuation and
vertical regular exits remain unresolved. Finite completion searches,
if recorded separately, are discovery only and cannot replace those proofs.
Submitted manuscripts are unchanged.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
