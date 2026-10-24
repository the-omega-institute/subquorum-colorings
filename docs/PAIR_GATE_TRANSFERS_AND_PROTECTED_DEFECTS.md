# Positive pair transfers protect actual reserve occurrences

21 October 2026. Complete positive gate consumers have an injective transfer
to activated positive terminals, including the previously unpaid regular-pair
channel. A minimal pair attachment has a permanently unmarked receiving side.
For the next attachment size, a marked receiving side has a distinct permanent
U0 or mixed-three defect. These are existing reserve occurrences, not new
credits. The full unrestricted allocation and rectangular-grid equality remain
open. Validation and independent-review status are recorded below.

## 1. Exact model and notation

Keep every complete-source hypothesis of
[the Horn retention theorem](SOURCE_RETENTION_HORN_CLOSURE.md): a finite family
of complete U and rotor sources, arbitrary permitted even dimensions, phases,
isometries and contacts, disjoint original endpoints and unchanged original
matchings. Every original support outside the endpoint union remains selected;
a selected point has its unique occupied anchor. Original endpoint graphs are
connected. Optional selections have no endpoint neighbor and do not affect
any argument below. All physical tiles remain the fixed aligned 2 by 2 tiles.

N counts positive source occurrences, G actual marked positive sides, and

    mu=N+R-G,       2R=A+U0+Z0+H,
    H=L1+2L2bar+2L2mutual+L3.

The counts are those of [the exact geometric ledger](EXACT_GEOMETRIC_EVENT_RESERVE.md).
In particular A counts activated ORIGINAL positive terminal singleton
occurrences, not consumed supports separately. All integer rounding is global.
An actual marked side has one fixed gate and unique endpoint consumer by
[canonical gate consumption](MARKED_SIDE_GATE_CONSUMPTION.md).

Normalize its producer to U(w,l,l'), with left gate t=(3,2), canonical tile
Q={2,3} squared, p=(2,2), y=(3,3). Exchange legs and transport by the
physical tile isometry for any other side. All dimensions below are even,
widths at least six and leg lengths at least four.

## 2. Every positive gate consumer transfers to an activation

**Theorem 1.** Every marked side whose gate consumer is positive has one
specified activated terminal of that consumer. These assignments are
injective over ALL such marked sides, including singleton and pair consumers.
If qpos counts these sides, then qpos<=A.

Here is the complete original-profile classification. A positive consumer
has a singleton, regular pair, or full bar tile at Q. A full bar tile is
strictly interior along its bar axis: its original bar continues beyond
BOTH ends of the tile. A horizontal bar therefore meets the producer at
(2,1) or (3,1); a vertical bar meets it at (1,2) or (1,3). Full consumers
are impossible, for ALL producer widths.

A pair {p,t} makes p have only one own endpoint neighbor, because (1,2)
and (2,1) are producer endpoints. It would be a positive terminal, whose
original profile is a singleton, a contradiction. The other pair is {t,y}.
If its support is (2,3), the established positive-pair continuation puts
its reflected endpoint at the producer anchor (3,1). Thus its support is p.
If this were an interior stem pair, its predecessor beyond t would again
be (3,1). It is a BAR-END pair. The bar cannot extend upward, since it
would meet the producer's row-one bar. Up to exchanging its own leg names,
the consumer has precisely the frame

    B=U(W,a,b),       T(r,c)=(c+2,r+2).                 (1)

Its near stem is row3 through column a+2. Disjointness at the producer's
opposite stem gives a<=w-4.

The singleton case transfers to the consuming terminal itself. Its original
support p has additional producer neighbors and must be consumed, so this
terminal is activated, as proved in FIVE_ENDPOINT_CAP_AND_POSITIVE_GATE_CONSUMERS.md.

For the pair case, the same support p forces a third source. The all-width
transverse-tip theorem says it is a negative U terminal pointing right,
with incident height h satisfying 4<=h<=w-4. There are two bar directions.
An upward bar includes (1,h+2), a producer endpoint. Therefore the only
possible frame, after naming the incident leg first, is

    C=U(V,h,f),       C(r,c)=(c+1,h+2-r).              (2)

If h<=a, its bar endpoint (3,h+2) collides with B's near stem. Evenness gives

    4<=a,       a+2<=h<=w-4.                          (3)

Consequently pair consumption requires w>=10. More significantly, C's
near stem contains (2,a+2), an ORIGINAL intratile support of B's terminal
z=(3,a+2). The pair case transfers to that terminal, which is activated.
The third source's original negative mass is not spent by this transfer.

The injection needs a mixed-collision argument. Two singleton transfers to
one terminal have the same gate point and canonical tile; canonical positive
tiles are distinct. Two pair transfers to one terminal determine the same
incident outer bar corner, again the same gate and canonical tile. These
cannot be different sides.

Suppose a pair target z were also a singleton gate consumer. The two neighbors
of z outside its tile are (3,a+1), already owned by B, and (4,a+2). Only the
latter can be another positive producer's anchor. Its canonical-side stencil
then includes endpoint (2,a+4). But (3) makes this a C endpoint (a bar
corner when h=a+2, and a near-stem endpoint otherwise).
The hypothetical positive producer and negative C have different owners,
contradicting endpoint disjointness. Thus pair and singleton targets cannot
coincide. This proves Theorem1 without repeated activation units.

In particular all positive gate consumers at producer width eight are
singleton consumers. The endpoint-disjoint pair U(8,4,4) and the image
T(U(6,4,4)) has NO complete extension by any sources: (3) would require
6<=h<=4. This is an explicit two-source noncompletion obstruction, not a
negative-margin fusion or a grid counterexample.

## 3. A thin enclosure excludes every further endpoint owner

**Enclosure lemma.** Suppose the complete boundary of the integer rectangle
[r,r+4] by [c,d] consists of endpoints of specified owners. A lattice point
strictly inside it, absent from those owners, cannot become an endpoint of
any other complete source.

Indeed another owner's endpoint graph is connected, consists of unit lattice
edges, and is disjoint from the occupied boundary. If it contains an interior
point, every one of its endpoints stays strictly inside: a unit path cannot
leave a lattice rectangle without meeting its boundary. There are only three
interior rows. Every U has bounding-box size at least5 by6, up to exchange
of axes, because both leg lengths are at least4 and width at least6. Every
rotor has bounding-box size4 by4. Neither can fit in three rows. This is a
general connectedness/extent proof, with no translation or source-count cutoff.

Return to a pair transfer and use the recipient B's OWN frame. Then

    B=U(W,a,b),       C(r,c)=(h-r,c-1).               (4)

If h=6, (3) forces a=4. Put m=min(W,V-1), with V C's width. B and C supply
the entire endpoint boundary of [1,5] by [1,m]: B supplies the top and near
leg, C the bottom bar, and the nearer far leg supplies the right side.
Their minimum far heights4 suffice, including the joining corner at row5.
Neither owns B's canonical support (3,2), strictly inside the rectangle.
The enclosure lemma excludes every endpoint owner of that support.

**Theorem 2.** This receiving side is permanently UNMARKED in every complete
extension. In particular every pair transfer from a width-ten producer ends
at an unmarked receiving side, since (3) then forces (a,h)=(4,6).

## 4. A permanent defect when the receiving leg is six

Suppose the pair recipient, in its own frame, has

    B=U(W,6,b),       C=U(V,8,f), C(r,c)=(8-r,c-1).  (5)

If B's near side is marked, let D be its actual gate consumer at (3,2).
The original endpoint blockers (1,2),(3,1),(7,2) give exactly these U forms:

| Type | D's dimensions and frame | Necessary clearance |
|---|---|---|
| I | U(d,4,e), (r,c)->(r+2,c+1) | d+1<W |
| II | U(d,4,e), (r,c)->(6-r,c+1) | Other dimensions subject to feasibility |
| III | U(d,g,e), (r,c)->(c+2,g+2-r) | V<=g<=W-4 and f=4 |

For I, d+1<V-1 forces e=4; d+1>V-1 forces f=4; equality is impossible.

Here is a catalogue proof, rather than bounded owner enumeration. A vertical
bar through t would occupy at least six consecutive points in column2; the
blockers at rows1 and7 leave only five. If t is on a horizontal bar or a
vertical leg, its column2 segment has at least five consecutive points.
It is therefore exactly rows2 through6, forcing incident height4 and forms
I or II. The blocked west neighbor makes its bar end the left end. Otherwise
t is on a horizontal leg. Its west neighbor is foreign, so it is an
east-pointing terminal. A north-extending bar cannot avoid both B's top
bar and far leg. Its south-extending bar gives III. Crossing C's bar at
row7 forces g>=V; its near stem avoids B(3,W) only if g<=W-4. Crossing
C's far column forces f=4. In I the far-leg comparison gives the stated
three alternatives, using e,f>=4 and evenness. Their phases are respectively
01,11,10, so ALL three consumers are negative U sources.

Rotors are excluded without a size cutoff. Of their sixteen gate endpoint
roles only the two footprints of the earlier cap theorem avoid B's fixed
producer stencil. One contains (5,1), already in B's height-six leg. The
other contains (2,4), but its original support (2,2) forces a transverse U
tip owning (2,4). Positive U consumers are also excluded by the same three
U forms (or by their singleton/pair classification and blocker (7,2)).

In each possible case a three-row enclosure protects one ACTUAL defect:

| Consumer | Endpoint rectangle | Missing point | Receipt |
|---|---|---|---|
| II | [1,5] by [2,min(W,d+1)] | (4,3) | D's original near unfilled U11 triple |
| III, or I with d+1>V-1 | [3,7] by [1,V-1] | (6,V-2) | C's original far unfilled U11 triple |
| I with d+1<V-1 | [3,7] by [1,d+1] | (6,d) | Actual mixed nonfull three-endpoint tile |

For II the receipt tile {4,5} by {2,3} has D endpoints (4,2),(5,2),(5,3).
The top boundary is B's bar, the left/bottom D's near leg/bar, and the
right the nearer far leg. If the right side is W and b=4, D's row-five bar
supplies the last joining corner; B supplies rows1 through4.

For III or crossing I, D owns row3 through V-1. Together with B's near leg
and C's row-seven bar and far leg this supplies the second rectangle.
Its receipt tile {6,7} by {V-2,V-1} has C endpoints (6,V-1),(7,V-2),(7,V-1).

For short I, e=4. B's near leg, D's row-three bar/far leg, and C's row-seven
bar supply the third rectangle. Its receipt tile {6,7} by {d,d+1} has
D endpoint (6,d+1) and C endpoints (7,d),(7,d+1).

Each displayed missing point is absent from B,C,D by their explicit intervals.
The enclosure lemma forbids every other endpoint owner, in every extension.
It also has two persistent endpoint neighbors and cannot remain a selected
support. Thus each tile stays an exact unfilled original triple or exact
mixed nonfull triple, respectively. No full-tile credit is reused.

## 5. The receipts are globally injective

Let m8 count the MARKED receiving side occurrences in (5) arising from
actual positive pair transfers. Each count retains its preceding positive
producer; it is not an arbitrary match between B and a nearby negative C.

Two type-II receipts with the same original cap identify D, its incident
terminal, and hence B's canonical physical tile. Canonical-tile separation
identifies the same receiving side. Two far-C receipts at the same cap
identify C's opposite terminal (the transverse tip). Its physical tile is
the PRECEDING positive producer's canonical tile. That identifies the same
pair transfer and recipient B. Original U caps here have two distinct
incident/opposite legs, so these recoveries are unambiguous.

An original cap might still have been type II in one configuration and
far-C in another; differing category names do not prevent reuse. Normalize
the first cap owner to F=U(d,4,e) with map (r,c)->(6-r,c+1). To be the other
kind its opposite leg must be8. The other recipient's coordinates map to
the first by Psi(r,c)=(r-2,d+1-c), because

    Psi(8-r,c-1)=(6-r,d+2-c),

which represents F with its legs exchanged. Every far-C receipt has its
negative gate consumer owning second-frame row3, columns2 through d-1.
Their images contain first-frame (1,3), already owned by the first positive
B. Those owners are distinct in sign, so endpoint disjointness excludes
the cross-type collision.

A mixed receipt has a unique actual 2+1 owner split. Its singleton is D's
specified far terminal, which determines D's opposite lower bar corner:
B's canonical support. Two coincident mixed receipts therefore identify
the same marked side. An original cap has three endpoints from one owner,
so it cannot coincide with a mixed receipt.

**Theorem 3.** These assignments are injective and extension-stable. Hence

    m8 <= U0+L3.                                     (6)

Receipts are actual source/tile occurrences already counted by the exact
ledger. They are also separate from positive activation occurrences: every
endpoint in a receipt belongs to its negative owner(s). A positive terminal
in that same tile would fill it, contrary to its permanent missing corner.

## 6. A stronger simultaneous loss bound

Let H subset J be the canonical least demand-preserving feasible hull.
It contains every positive source and preserves the entire labelled set of
marked positive sides. Equivalently, once all positive sources are retained,
marks are monotone under feasible inclusion, so equality of G preserves
every marked-side label, not just its cardinality.
Use the actual endpoint components of J minus H and aggregate loss L from
[the component theorem](COMPONENT_LOSS_AND_THE_MARKED_DEMAND_GAP.md).
All positive pair producers and recipients lie in H; their forced transverse
C also lies in H by the support Horn implication. Preservation of a marked
receiving side retains its unique consumer D in H; feasibility alone would
not imply that retention. Thus every m8 certificate of J is
already present in H and its protected receipt persists in every complete
extension of H. Conversely a pair/m8 pattern present in H persists in J.

Choose ALL reserve-losing new components together. Their feasible union X
has R(X)=R(H)-L. Positive activations in H persist. Theorem3 supplies m8(H)
distinct persistent U0/L3 units, so ONE application of the exact ledger gives

    2R(X) >= A(H)+m8(H),
    2L <= 2R(H)-A(H)-m8(H),                           (7)
    L <= R(H)-ceil((A(H)+m8(H))/2).                    (8)

This strengthens the previous A-only bound by actual protected non-A units.
The integer improvement is exactly
ceil((A+m8)/2)-ceil(A/2); an odd subtotal is never rounded separately.
In particular

    A(H)+m8(H) >= 2(G-N)  ==>  L<=mu(H).              (9)

The H=J case is retained: there are no added groups, but the persistent
floor also proves mu(H)>=0 whenever the stated sufficient condition holds.
For arbitrary H,J we have not proved that this condition always holds.

Theorem1 separately gives mu>=N-G+ceil(qpos/2). If qother=G-qpos counts
gate consumers that are not positive, then G<=2N implies
mu>=-floor(qother/2). Thus coefficient one holds when qother<=1. These
conditional complete-source classes improve the coefficient5/6 by |M|/6
on the SAME configurations, using sigma>=mu. They do not assert a new
universal grid coefficient or the missing arbitrary-grid/source bridge.

The remaining work is to protect/payment-count all other negative-U endings,
including full-bar consumers at arbitrary attachments. No bounded enumeration
or scalar budget proves their general compensation.

## 7. Two complete physical examples

Here are two actual five-source configurations, with all frames expressed
in B's coordinates. Retain each source's original matching, and select
every original support not consumed by the endpoint union.

| Owner | Original source | Physical frame |
|---|---|---|
| A | U(14,12,4) | (r,c)->(c-2,r-2) |
| B | U(8,6,6) | (r,c)->(r,c) |
| C | U(10,8,8) | (r,c)->(8-r,c-1) |
| D, first example | U(6,4,4) | (r,c)->(r+2,c+1) |
| D, second example | U(6,4,4) | (r,c)->(6-r,c+1) |
| E | U(6,4,4) | (r,c)->(4-r,c+9) |

Use exactly one of the two D rows. The checker independently reconstructs
138 distinct endpoints, 69 original matching edges and 23 mandatory selected
points in each case, verifies each selection's unique occupied anchor, and
finds connected endpoint graphs. Both have N=2, G=3, R=13, A=2, mu=12 and
m8=1. The first has the short-I mixed receipt; the second has the type-II
original cap receipt. Thus the persistent integer floor increases from
ceil(A/2)=1 to ceil((A+m8)/2)=2. These are complete realizations of a strict
improvement, not sharp-margin examples or allocation counterexamples.

The controls also include their separated union and a separated union of
the first example with the existing J70 loss family. The latter checks a
proper losing canonical extension with a protected receipt; it does not
assert connectedness of that combined benchmark.

## 8. Validation status and provenance

This note independently reconstructs the positive-consumer pair clearance,
mixed activation nonreuse, enclosure and protected-cap geometry. Oracle task
1adc9732 completed with a broader proposal containing these results and
additional rotor/path transfers. Its original stream64276 exited0/DONE;
all23723 response characters match the task API, observed gpt_6/pro.
The raw proposal is archived separately and is not itself an acceptance or
execution receipt. Its additional rotor/path theorem is not adopted here.

[Physical controls](../output/pair-transfer-protected-defect-controls.json)
PASS: 832 phase/isometry images, 33,728 complete legal restrictions, 848
actual pair transfers and 2,024 canonical component subextensions. These
include 40 subextensions with protected receipts, eight losing canonical
hulls with protected receipts and 24 hulls with a stronger integer floor.
The local controls check 48 thin enclosures, 564 endpoint-disjoint receipt
geometries, 572 anchored U-role cases and four cross-cap collision controls.
The complete physical fixtures exercise short-I and II receipts. Their
singleton, permanently unmarked h=6, crossing-I and III counts are zero;
these channels rely on the written general proofs and scoped local controls,
not complete physical realizations in this finite library.

[Twelve Lean declarations](../formal/SubQuorum/PairTransferProtectedDefects.lean)
compile locally and pass the recorded axiom audit, with no sorryAx or native
decision axiom. They cover coordinate/support separation, arbitrary connected
unit-walk enclosure, cross-cap collision and conditional ledger arithmetic.
Catalogue normalization, boundary/count adapters and the global physical
receipt injection remain written; this is not an end-to-end formalization.
The [execution receipt](../output/pair-transfer-protected-defect-formal-check.json)
records this scope and the corrected initial parameter-name syntax failure.

Independent written review cc5ab6b7 ACCEPTS the activation injection,
extension-stable receipt injection and stronger loss bound, under the cited
complete-source/Horn/ledger/component hypotheses. It found no must-fix
mathematical issue. Its endpoint wording correction and explicit marked-label
retention clarification are incorporated above. This was a written review,
not execution of the checker or Lean and not a novelty or full-target
certificate. See the [review receipt](../output/pair-transfer-protected-defect-review.json)
and [full response](../output/pair-transfer-protected-defect-review-response.md).
The full unrestricted allocation and rectangular-grid equality remain OPEN.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
