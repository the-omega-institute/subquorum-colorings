# Connected frozen extensions: interval-only repair fails, while different beta stems pay everything

25 October 2026. Haobo Ma and Wenlin Zhang. Independent research branch.

The [joint-extension theorem](SELECTED_EXTENSIONS_AND_NEW_TP_DEFECT_BUDGET.md)
leaves exactly k post-cancellation alpha paths with two new TP ends. Its
disjoint-new-interval repair lemma is sufficient. We now refute the proposed
automatic applicability of that lemma under complete freezing, even with a
CONNECTED occupied graph. The sufficient lemma itself remains valid.

For every q>=1 there is an explicit connected, completely frozen extension
of the actual 49T/308P board. It adds q translated copies and four endpoints
per seam. After the old 18-link certificate C, there are 4q new-new alpha
paths. Their direct free-end interval graph has rank q. Even allowing the
WHOLE support of each free end's original owner, interval rank is only 2q:
two source classes per new copy have NO interval support at all.

Nevertheless all 4(q+1) original alpha sources have ordinary and full
beta-only compensation with EXACT minimum link cost 5(q+1). The beta target
owners are different. Alternatively, retain the old partial certificate
and extend it by 5q new-copy beta assignments; this fully compensates the
extension with at most one old interval payment and at most 18+5q links.

The failed rule is "freezing/occupied connectivity forces every residual
new-new alpha to have a simultaneous new-interval payment." Neither the
old sufficient repair lemma nor the all-resource compensation target is
false here. This family is fully compensated even with NO available intervals.

## 1. A neutral PP splice joins the actual boards

Let B be the fixed 28-by-24 board with 49 selections T0 and 308 endpoints
P0. Form q+1 copies indexed i=0,...,q, translating copy i by (0,24i).
The final rectangle is 28-by-24(q+1). Retain every old selection and endpoint.

For each seam i=0,...,q-1 put c=22+24i. The two existing vertical actual
matching edges are

    (2,c)--(3,c),       (2,c+3)--(3,c+3).

Add the four endpoints (2,c+1),(3,c+1),(2,c+2),(3,c+2). Replace the two
vertical edges by the four horizontal edges

    (r,c)--(r,c+1),     (r,c+2)--(r,c+3),       r=2,3.      (1)

Only two old actual matching edges per seam change. No claim that the old
matching is entirely retained is made. The first original board loses its
single old vertical PP matching edge at column22; all its other matching
edges are retained. The construction is an arbitrary-M extension of the
previous theorem, not an instance of an old-M-retaining theorem.

All eight patch endpoints have an occupied band partner: they are PP,
not TP or BP. Their old/new actual edges and band edges stay entirely inside
the patch. Thus the modification affects only closed PP cycles. It creates
no terminal, changes no noncycle strand, and changes no terminal TP--BP link.

The added sites have no selected neighbour. Selections in adjacent copies
are separated by at least two columns. Therefore all selection-degree and
global boundary conditions hold. The final first/last columns stay blank.
The occupied graph of B is connected (a fixed finite coordinate audit).
The horizontal occupied chain across each seam joins the two copies, so
the full induced graph on T union P is connected for EVERY q.

Counts are

    selections = 49(q+1),
    endpoints = 308(q+1)+4q = 308+312q,
    alpha = 4(q+1),   beta = 6(q+1),   mixed = 15(q+1).      (2)

The last three counts follow from the unchanged noncycle strands. Full
original interval identities are recomputed in the large rectangle; they
are NOT assigned private copies by fiat. Some boundary/gap resources can
change or be shared across seams. The proofs below use only permanent
occupied-side exclusions and explicitly different interior units.

## 2. Complete freezing for arbitrary q by an explicit rank replay

Define the four boundary endpoints of one original copy by

    X={(2,1),(3,1),(2,22),(3,22)}.

These include all old endpoints whose actual mates might change. Run the
old freezing rule while forbidding X from being declared frozen. Its fixed
coordinate certificate has 112 endpoints in 27 layers. Call this prelude F.
Every kept endpoint used by its witnesses has its old mate in F, and hence
is outside X; these mate identities are unchanged by the splice. Thus this
same prelude translates to every copy simultaneously for arbitrary q.

After the prelude, all four sites of X have two kept neighbours:

| Endpoint in X | Two kept neighbours |
| --- | --- |
| (2,1) | selected (1,1), endpoint (2,2) |
| (2,22) | selected (1,22), endpoint (2,21) |
| (3,1) | endpoints (3,2), (4,1) |
| (3,22) | endpoints (3,21), (4,22) |

For each listed endpoint neighbour, its unchanged old mate is in F. These
are fixed finite witnesses, saved with the prelude; they are independent
of the changed matching inside the seam. Freeze X in every copy next.

Every NEW seam endpoint now has two neighbours whose NEW actual mates lie
in X. For example, (2,c+1) sees (2,c+2), mated to (2,c+3), and (3,c+1),
mated to (3,c). Both mates have just frozen. The other three new endpoints
have the corresponding horizontal/vertical witnesses. Freeze all four.

Now replay the original complete rank in every copy, skipping endpoints
already frozen. An old kept witness outside X has the unchanged actual
mate, which precedes it by the old rank. A witness in X instead has its
new mate among the already frozen seam endpoints (or has its unchanged
mate in X at an outer boundary). Every old rank dependency is therefore
satisfied. Induction on the old natural-number rank freezes ALL endpoints.

This is a general freezing proof. It is not an assertion that a finite
collection of q values was frozen. The generated certificate for any q is:
translate the 27 prelude layers; freeze X; freeze new seam endpoints;
replay the old rank. The independent coordinate checker validates its
strict dependencies in the finite controls.

## 3. The new-new interval Hall graph has an unbounded deficiency

Keep C equal to the old 18 TP--BP assignments in copy0, together with the
old five different singleton interval assignments. No seam endpoint
occupies one of those five candidates: h=0. The old 23 TP certificate
persists. Every added copy contributes 23 genuinely new TP ends, so

    d=23q,   s=49q.

The splice changes only PP cycles, so all four alpha strands in each new
copy remain untouched by C. Hence k=4q. The old part has one post-C alpha,
which has its old interval assignment; the new-new residual demands are
exactly the four new-copy alpha classes:

| Class | Original TP ends, before translation | Free-end BT interval access | Whole-owner interval support |
| --- | --- | --- | --- |
| top | (5,17), (5,6) | none | none |
| right | (24,19), (5,19) | none | none |
| bottom | (24,17), (24,6) | present | present |
| left | (24,4), (5,4) | none | present |

For top and right, EVERY horizontal neighbour column of EVERY node on the
original strand contains a retained endpoint. The fixed certificate gives
50 endpoint blockers for the 25 nodes (14 top, 11 right). No endpoint-free
gap can start there, irrespective of a new global boundary or interval
renumbering. The seam modifies only band1, whereas these strands lie in
bands2,...,12. Thus their whole supports remain empty. The two left free
ends also have no endpoint-free port. These are occupied-geometry facts,
not consequences inferred from a reserved or empty Q.

Consider the bipartite matching graph from the 4q new-new alphas to FINAL
original interval identities, excluding the old five if desired.

* With direct free-end BT-corridor access, only the q bottom alphas have
  neighbours. Each can use the different interior unit (band12,col24i+7),
  i=1,...,q. Thus the rank is EXACTLY q and deficiency is 3q.
* Even if a free end is allowed every whole-support unit of its original
  owner, the 2q top/right demands are isolated. The remaining left/bottom
  demands can use the different interior units

      left:   (band7,col24i+5),
      bottom: (band12,col24i+7),          i=1,...,q.

  All are final internal singleton units, mutually different and outside
  the old five. Thus this more generous rank is EXACTLY 2q and its
  deficiency is 2q.

Allowing all final interval identities, even those used by old assignments,
cannot help the isolated top/right demands. Consequently neither complete
freezing nor occupied connectivity implies the proposed interval Hall
condition. This disproves its automatic applicability, not its sufficiency.

## 4. Different beta stems pay every source, with exact link cost

In each copy the following translated routes exist:

| Alpha class | Actual TP--BP route | Payment |
| --- | --- | --- |
| top | (5,17)->(5,16) | one original beta |
| right | (5,19)->(5,20) | a different original beta |
| left | (5,4)->(5,3) | a different original beta |
| bottom | (24,17)->(24,18), then (18,15)->(18,16) | a different original beta, through one mixed owner |

The source owners, the intermediate mixed owner and all four beta targets
are different within each copy. Translation separates all these owners
between copies. In particular the beta at the end of the two-link route
is not reused by another source, and a BP entrance is not counted as a new
beta unit. This is an owner-disjoint ORDINARY packing of four payments
using five actual terminal links per copy, without intervals or forks.

For the matching lower bound with Q empty, every alpha must use an outgoing
terminal link. The bottom class has only mixed owners as first targets,
so it additionally needs a link out of a mixed owner before any beta can
be paid. No beta-only route can stop at that mixed entrance. Thus every
copy needs at least four source links and one further mixed link. Forks
do not remove either requirement. There are no terminal links across
copies: the geometric connectors are PP, and all old terminal strands and
TP--BP links stay inside their own copy. Therefore

    V_ord(empty)=V_full(empty)=4(q+1),
    c_ord(empty)=c_full(empty)=5(q+1).                         (3)

This separation is a statement about the BETA-ONLY owner/link graph. We do
NOT claim the whole interval-resource graph separates, or that occupied
connectivity is the same as interaction of compensation owners.

There is a compatible repair that keeps the old partial assignments. Add
the five beta-route assignments for each NEW copy to C. They have different
new TP sources and BP targets, so they do not conflict with old assignments
or with one another. They eliminate the 4q new-new alphas without a new
interval. The final counts are

    aC=1,    bC=3+2q,
    beta payments=(6+6q)-(3+2q)=3+4q,
    one old interval payment,    total=4+4q.                 (4)

There are 18+5q selected links in this extended certificate. The ordinary
normal-form lift may use a subset, so it gives an upper bound on links;
it is not a claim that normalization retains every old C edge. This does
not preserve every old actual M edge either: the PP splice was stated
explicitly in Section1. None of the interval or beta resources is duplicated.

## 5. What this changes in the research direction

The earlier sufficient new-interval matching lemma is correct, but proving
its hypotheses from freezing is an unavailable route to universal coverage.
Even its whole-owner relaxation fails with unbounded deficiency here.
The failure cannot be dismissed by asking for a connected occupied graph.

The remaining general geometric problem must allow beta paths through mixed
owners, respect individual BP-entry capacity and original beta identities,
and allocate original intervals jointly. Merely counting a supply of new
intervals or treating visible beta entrances as independent credits cannot
prove it. The existing ordinary/full flow models already express these
requirements; what remains is a general geometric coverage/min-cut argument
or an actual all-resource frozen counterexample. Neither the universal
compensation conjecture nor the 5/6 improvement is settled by this family.

## 6. Verification and the external-review attempt

The fixed prelude, boundary witnesses, occupied-side blockers and arbitrary-q
rank replay are explicit. Twelve connected frozen models q=1,...,12 pass
independent complete coordinate/rank checks, both beta-only optimizers and
all interval-rank and resource-identity checks. There are 24 ordinary/full
beta-only comparisons and two independent primitive-pack checks on the
actual 620-endpoint case. The largest control has 4052 endpoints. These
controls corroborate the written arbitrary-q proof.

All five perfect matchings of the closed 2x4 PP patch are also checked:
three give 620 frozen endpoints and two only616. Every one preserves the
terminal pairs/links and beta-only value8/cost10. Feasible nonfrozen control
matchings are explicitly distinguished from the completely frozen construction.

Ten local Lean4.33.0 declarations pass with exit0. They cover arbitrary-rank
replay after mate changes, closure of the PP patch, freezing its four new
sites once the boundary has frozen, disjoint translated identities, interval
Hall arithmetic, beta ledger/link budget and actual occupied-side witnesses.
The axiom union is propext, Classical.choice and Quot.sound; no sorry/native
evaluation is used. Concrete112-prelude verification, the complete620 rank,
physical support adaptation and ordinary-flow/normal-form identification
remain written/Python. This is NOT an end-to-end Lean theorem for the family.

An Oracle broker review of the PRECEDING extension results at public revision
08810f45a9d9b05df741f465a04472236073631f was attempted through the streamed
NyxID service. The only available pool reported26 online workers, but the
task ended with model_unavailable@selecting_model. It produced NO review.
The failed attempt is archived and is not described as external acceptance.

Permanent evidence:

* [Verifier](../develop/check_connected_frozen_interval_repair_obstacle.py)
* [Actual connected620P frozen fixture](../develop/fixtures/connected_frozen_new_end_obstacle.json)
* [Prelude and occupied-side witnesses](../develop/fixtures/connected_frozen_splice_local_certificate.json)
* [Computational receipt](../output/connected-frozen-interval-repair-validation.json)
* [Direct Lean source](../formal/SubQuorum/ConnectedFrozenIntervalRepair.lean)
* [Formal scope](../output/connected-frozen-interval-repair-formal-check.json)
* [Failed Oracle receipt](../output/extension-theorems-oracle-review.json)

The submitted manuscript, public main, PR3, shared CI and independent
star-forming/C4 project identity are unchanged. No Mail was read, drafted
or sent in this round.
