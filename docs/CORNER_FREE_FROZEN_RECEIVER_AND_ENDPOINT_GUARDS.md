# A frozen degree-three obstruction to corner coverage and a compatible repair

20 October 2026. Universal coverage by the capped-corner and selected-guarded
donors is false, already for a fully frozen occupied-degree-three component
on an 8-by-8 grid. It has corrected charge one and none of either old donor.
The obstruction persists after padding with blank rows and columns, so it
does not result from clipping a witness at the rectangle boundary.

A third local rule, with two same-component endpoint guards, supplies its
missing unit. Its deficit lemma and mixed ownership proof hold for arbitrary
single-terminal configurations, not just this drawing. They extend the
conditional coefficient-one class. Coverage by all three rules for every
positive frozen component remains unproved.

## 1. Complete explicit configuration

Use zero-based coordinates on {0,...,7} x {0,...,7}, nearest-neighbor edges
and the original aligned physical 2-by-2 tiling. Every unspecified site is
blank. In the diagram, P means an actual matching endpoint, T an original
selection, and a dot a blank.

    ..T.T.T.
    ..PPPPPT
    T.PP.T..
    PPPPT...
    PP......
    PP.T....
    PPPPPT..
    T.T.T...

There are 12 selections:

    T={(0,2),(0,4),(0,6),(1,7),(2,0),(2,5),(3,4),(5,3),(6,5),(7,0),(7,2),(7,4)}.

The actual matching consists of:

    (1,2)--(2,2)
    (1,3)--(1,4)
    (1,5)--(1,6)
    (2,3)--(3,3)
    (3,0)--(4,0)
    (3,1)--(3,2)
    (4,1)--(5,1)
    (5,0)--(6,0)
    (6,1)--(6,2)
    (6,3)--(6,4)

These ten edges are disjoint grid edges; their endpoint set P has size 20.
Every selection sees exactly one endpoint and no other selection. Every
endpoint has occupied degree exactly three. The central vertical chambers
{1,2,3} x {2,3} and {3,4,5,6} x {0,1} are connected by the edge
(3,1)--(3,2). The two remaining horizontal tails attach at (1,3) and (6,1).
Thus H=P is a single complete connected component. Its endpoint-induced
degree is at most three as well: it lies in the scope of the general chamber
network reduction, without geometric degree-four junctions.

The complete machine-readable instance is
develop/corner_free_frozen_receiver.json. It was discovered by the optional
solver in output/weighted-coverage-discovery-8x10.json, then simplified by
removing the unused isolated selection (2,8) and two empty columns.
Neither the matching nor a freezing witness changes in that simplification.

## 2. Every mixed promotion bundle is excluded

In this table m is the actual mate. The two witnesses in each row are
distinct neighbors other than the row's mate, and each is either in T or
the mate of an earlier endpoint.

| Step i | Endpoint v_i | First retained witness | Second retained witness |
| --- | --- | --- | --- |
| 1 | (1,6) | (0,6) in T | (1,7) in T |
| 2 | (6,4) | (6,5) in T | (7,4) in T |
| 3 | (1,4) | (0,4) in T | (1,5) = m(v1) |
| 4 | (6,2) | (6,3) = m(v2) | (7,2) in T |
| 5 | (1,2) | (0,2) in T | (1,3) = m(v3) |
| 6 | (6,0) | (6,1) = m(v4) | (7,0) in T |
| 7 | (2,3) | (1,3) = m(v3) | (2,2) = m(v5) |
| 8 | (5,1) | (5,0) = m(v6) | (6,1) = m(v4) |
| 9 | (3,2) | (2,2) = m(v5) | (3,3) = m(v7) |
| 10 | (4,0) | (4,1) = m(v8) | (5,0) = m(v6) |
| 11 | (3,0) | (2,0) in T | (3,1) = m(v9) |
| 12 | (3,1) | (3,0) = m(v10) | (4,1) = m(v8) |
| 13 | (3,3) | (3,2) = m(v12) | (3,4) in T |
| 14 | (4,1) | (3,1) = m(v9) | (4,0) = m(v11) |
| 15 | (2,2) | (2,3) = m(v13) | (3,2) = m(v12) |
| 16 | (5,0) | (4,0) = m(v11) | (5,1) = m(v14) |
| 17 | (1,3) | (1,2) = m(v15) | (2,3) = m(v13) |
| 18 | (6,1) | (5,1) = m(v14) | (6,0) = m(v16) |
| 19 | (1,5) | (1,4) = m(v17) | (2,5) in T |
| 20 | (6,3) | (5,3) in T | (6,2) = m(v18) |

If a nonempty simultaneous bundle existed, take the first promoted endpoint
in this order. Original selections remain occupied. The mate of an earlier
endpoint remains occupied as well: deleting it would require promoting
that earlier endpoint. The first promoted endpoint therefore retains both
listed neighbors, contradicting selected-degree feasibility. This proves
terminality for arbitrary mixed orientations. It is not bundle enumeration.

## 3. Exact charge and absence of both old witness types

The receiver has nine physical tiles. The label inventory is:

| Endpoints | Selections | Blanks | Number of receiver tiles |
| --- | --- | --- | --- |
| 1 | 2 | 1 | 2 |
| 2 | 1 | 1 | 5 |
| 4 | 0 | 0 | 2 |

Thus it has 9 selections and 7 blanks, giving

    rho_H = 9 + 20/2 - 2*9 = (9-7)/2 = 1.

There are two actual saturated-mate transfers. Direct evaluation of the
original corrected graph charge gives one half at tile (0,2), one half at
tile (3,1), and zero at every other receiver tile. In particular the two
saturated tiles themselves have corrected charge zero. Raw and corrected
individual tile values are not being interchanged.

No endpoint-free tile has an old capped-corner witness. This can be checked
without an opaque search: list all runs of at least four P vertices, then
retain only the extended sides of actual physical squares. The only possible
full sides adjoining an endpoint-free physical tile are:

| Tile | Full side of four endpoints | First possible tip/support | Other possible tip/support |
| --- | --- | --- | --- |
| (1,2) | north: (1,3),...,(1,6) | tip (2,3) is P; support (3,3) is P, not T | tip (2,6) is blank |
| (2,1) | west: (3,1),...,(6,1) | tip (3,2) is P; support (3,3) is P, not T | tip (6,2) is P; support (6,3) is P, not T |
| (2,1) | south: (6,1),...,(6,4) | tip (5,1) is P; support (4,1) is P, not T | tip (5,4) is blank |

Every orientation therefore fails the capped witness. Other four-vertex
runs have the wrong physical parity or no endpoint-free adjacent physical
square; the displayed diagram lists all runs.

An old selected-guarded tile must contain exactly one selection. The only
endpoint-free tiles containing selections are (1,2), with two selections,
and (2,1), with its sole selection x=(5,3). In the latter tile the opposite
corner z=(4,2) has exterior neighbors (3,2) and (4,1), both endpoints, and
neither is a selected guard. Every other endpoint-free tile has no selection.
Hence the selected-guarded rule also has no witness, in any orientation.

The sum of actual deficits over distinct tiles of the two old types is
therefore zero, strictly less than rho_H=1. This disproves their universal
weighted coverage, not their conditional compensation theorem.
The whole grid has objective22, half-area32 and deficit10. Its seven
endpoint-free physical tiles have total deficit11, so the exact global
ledger is 32-22=11-1. The grid target and triple equality are not refuted.

Translate the drawing by (2,2) in a 12-by-12 blank rectangle. Physical phase
is preserved. New blank border tiles cannot supply either old witness:
each would require named original selections and endpoints absent from
the enlarged border. Every old feasible witness would already have appeared
in the full local scan of the original support. The computational receipt
checks all eight padded symmetries separately.

## 4. A third general donor rule

Let Q be an original physical square. Let x be a selected corner with an
exterior endpoint neighbor p in a complete component H. Let z be the corner
opposite x. Suppose the two exterior neighbors q_1,q_2 of z are endpoints
of that same component H. Assume feasibility and single terminality for
all endpoints. All named vertices are inside the grid.

**Two-endpoint guard lemma.** Q has no endpoints and contains exactly x as
its occupied site, so its actual deficit is one.

Proof. Since x already sees p, both its neighbors inside Q are blank by
feasibility. If z were an endpoint, these two blanks would leave it with
at most two occupied neighbors, contrary to single terminality. If z were
selected, it would see both distinct endpoints q_1 and q_2, contrary to
feasibility. Thus z is blank. QED.

Assign this tile to H. In the example use

    Q=Q_(2,1)={4,5} x {2,3},
    x=(5,3), p=(6,3), z=(4,2),
    q_1=(3,2), q_2=(4,1).

All three named endpoints belong to H. This supplies exactly the missing
unit, and introduces no extra receiver charge, phase credit or second
copy of an existing deficit.

## 5. Ownership is compatible across all three rules

**Mixed unique-owner lemma.** A physical tile assigned by a capped-corner,
selected-guarded or same-component two-endpoint-guard witness has only one
owner component, including when different rule types describe it.

Proof. The first two types already have compatible unique ownership by
ELBOW_OWNED_DONORS.md and GUARDED_CORNER_AND_STEPPED_ARMS.md. Each new guard
tile has exactly one selection x, whose unique occupied neighbor is p.
Thus two new witnesses have the same x and p, and the same owner. The same
argument applies to a new guard and an old selected guard on one tile.

It remains to compare a new guard with an old capped witness. Normalize the
latter to the north/west coordinates in ELBOW_OWNED_DONORS.md. Its upper-left
and lower-left corners are blank. Since the new witness requires a selection,
the sole selected corner is either upper-right or lower-right.

If x is upper-right, its northern neighbor (-1,1) belongs to the old owner's
extended endpoint run. Feasibility makes this its unique occupied neighbor,
so the new anchor p is in the old owner's component.

If x is lower-right, its opposite corner is upper-left. The two exterior
endpoint guards of that corner are (-1,0) and (0,-1), both in the old owner's
component. The new rule explicitly requires both guards to be in its own
anchor component, so the new and old owners coincide here too. These cases
exhaust all orientations. QED.

The same-component hypothesis is used in the last case. A merely local
two-endpoint guard proves a deficit but does not by itself justify pooling
that resource with old capped ownership.

**Extended weighted compensation theorem.** In a feasible single-terminal
even-by-even grid, suppose each positive complete receiver H admits a set
W_H of distinct witness tiles of any of these three types, assigned to H,
with sum_(Q in W_H) d_Q >= rho_H. Then |T|+|M|<=mn/2.

Proof. Each listed tile is endpoint-free, and mixed unique ownership makes
the W_H pairwise disjoint. Use sets within each W_H to count a physical tile
only once, even if it has several orientations or several rule descriptions.
Then sum_(rho_H>0)rho_H<=sum_H sum_(Q in W_H)d_Q<=D_all. Nonpositive
receiver charges only reduce the total. Substitute into the original exact
ledger mn/2-|T|-|M|=D_all-sum_H rho_H. QED.

The new hypothesis covers the explicit obstruction where both old types
give capacity zero. It is a general sufficient criterion with a proved
ownership rule, not a proof of universal coverage or a numerical improvement
of the unrestricted 5/6 estimate.

## 6. Verification scope

Run the standard-library physical checkers:

    python3 -B develop/check_corner_free_frozen_receiver.py --output output/corner-free-frozen-receiver-controls.json
    python3 -B develop/check_owned_corner_extensions.py --output output/owned-corner-extension-controls.json

The first checks every actual edge, feasibility, occupied degree three,
connectivity, the complete ordered certificate, original corrected charge,
absence of both old donor types, and the new unit. Eight physical images
and eight images after blank padding pass. The second checks56physical
symmetry cases and separated bundles with2,3,7components, with owner and
capacity assertions at each physical tile.

formal/SubQuorum/CornerFreeFrozenReceiver.lean separately formalizes the
32 occupied vertices, their injective embedding into the8-by8grid, selected
neighbor feasibility, actual mate involution, exact occupied degree three,
the20-step frozen proof and exclusion of every feasible bundle. Kernel
decide also checks the complete receiver and its original corrected
twice-charge2, including actual saturated-mate transfers. No native_decide
or sorry is used. The geometric absence of old donors and the new mixed
ownership theorem above are written proofs with their own physical controls,
not asserted to have been formalized in that file.

formal/SubQuorum/EndpointGuardedCorners.lean independently formalizes the
general local deficit lemma in normalized grid coordinates. The two new
modules have35theorem declarations, all locally compiled with Lean4.33.0
and Std-only dependencies. Nine principal statements were audited for axioms:
the only dependencies are standard propext and Quot.sound, with no admitted
or native-decision axiom. The full global geometric ownership adapter remains
the written proof in Section5. The execution receipt is
output/corner-free-frozen-receiver-formal-check.json.

Optional discovery uses develop/search_weighted_owned_coverage.py with
z3-solver5.3.1. Independent physical and symbolic scans agree on24old-rule
controls. The fixed charge-two endpoint/matching template has no choice of
selected labels violating old coverage, a finite UNSAT result only. The
unrestricted8-by10search found the present obstruction; its explicit proof
does not depend on that solver or on its UNSAT result.

Next: derive coverage on arbitrary matching-constrained chamber networks
with this larger set of owned resources, retaining junction, link and hole
costs exactly once. The old two-rule universal claim is now false. Coverage
by three rules and the unrestricted grid inequalities remain open.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
