# Exact joint compensation with two-unit gate bundles

26 October 2026. Wenlin Zhang and Haobo Ma. Independent research continuation.

We give a positive joint-selection theorem that handles both a whole-corridor
prerequisite and the fact that one operation can pay two different sources.
For independently activatable bundles carrying at most two original units,
one **maximum-weight matching** gives the maximum payment and then the minimum
total activation fee, charged once per used bundle. Old feasible direct-source
payments can be preserved at the same optimal fee. The construction uses the
standard weighted matching problem; the new role here is its precise resource
and geometric adapter, not a new general matching algorithm.

An explicit 16×58 completely frozen grid realizes a shared two-unit bundle
and two competing one-unit bundles. Its shared capacity-two pivot pays two
previously unpaid alpha owners in one operation. Charging that operation
separately to each paid path can choose a strictly more expensive physical
repair. All raw units and baseline mixed routes are accounted for exactly.

The two-unit restriction has a specific algorithmic role: three-unit bundles
already encode Exact Cover by 3-Sets. Sharing one physical gate among many
nominally separate one-unit offers has the same issue. These are standard
abstract allocation reductions, not grid-embedding or grid-hardness claims.
The universal 5/6 improvement remains open; the 11 October manuscript is kept.

## 1. Simultaneous physical adapter

Use the full canonical-band whole-owner model of the preceding notes. Its
owners, TP/BP terminals, physical links and raw positive unit inventory are
fixed under the admitted gate operations. Split its alpha sources into a
residual set A and a baseline part. Assume:

1. Residual sources have no external physical TP→BP exits. Their payments
   are therefore direct interval assignments. The rest of the model has a
   fixed maximum B, independent of residual interval assignments and gate
   choices. Its owners/routes and resources do not compete with the residual
   units specified below. This baseline may contain mixed relays and beta
   forks; it must actually be independent, not separately counted twice.
2. There is a free residual pool R_0, with arbitrary fixed source supports.
   There are also disjoint labelled original resource groups R_j, each of
   size k_j∈{1,2}. They are disjoint from R_0 and all baseline-used resources.
   An inactive group is unsupported by every residual source and unused by
   the baseline; when active its slot r has the declared source set S_{jr}.
   Slots of one group may have different source sets, or may be shared.
3. Bundle j has a nonempty set P_j of primitive gate changes. These P_j are
   pairwise disjoint. For **every** primitive gate subset G, all operations
   are jointly feasible, keep the invariant owner/link/baseline system, and
   give exactly the prescribed residual supports: group j is active iff
   P_j⊆G. Partially opening a bundle adds no residual support and has no
   other effect on the attainable baseline or other residual incidences.
4. Primitive gate fees are nonnegative integers. Thus the bundle fee c_j is
   the sum of its gate fees, and simultaneously opened bundles cost the sum
   of their c_j. An enabled bundle set E restricts which bundles may be used.

Common resource labels may be supplied by the unique positive fine-child
bijection of the [pivot ledger](P_FREE_PIVOT_INTERFACE.md). Physical forest
cells can change under a pivot; group size and original-unit identity must
be transported consistently, not augmented by unioning old and new pools.
Resources outside this residual pool are retained in the physical inventory.

The all-subsets statements are substantive hypotheses. Disjoint gate tiles
alone do not prove them, nor do two separately tested directions. In particular
the [frozen support-loss family](P_FREE_PIVOT_INTERFACE.md) is excluded when
it removes residual/baseline access. The earlier destructive-exchange theorem
handles a different contract and cannot be applied automatically here.

Any primitive choice can now be reduced to whole active bundles: remove every
partial bundle. No useful support or baseline payment is lost and cost does
not rise. Conversely any bundle subset F is realizable by ∪_{j∈F}P_j, and
disjoint nonempty P_j ensure that no other bundle is accidentally activated.

## 2. The two-slot matching gadget

Fix enabled bundles E. Put C=Σ_{j∈E}c_j and K=C+1. Construct an undirected
weighted graph:

- One source vertex for every a∈A.
- One resource vertex for each free unit r∈R_0, with an edge of weight K
  from every source supporting r.
- Two vertices x_j,y_j for every j∈E, with an internal edge x_jy_j of weight
  c_j. Real slots get a source edge of weight K precisely when that source
  belongs to their declared support set. If k_j=1, y_j is a dummy with no
  source edges. For k_j=2 both slots are real.

There are no other edges. In particular every source can be matched only
once, and each original real unit can be matched only once. A two-slot bundle
can pay two sources using its two different units. It is not compressed to
one resource token. Source edges and the internal edge form triangles when
a source supports both slots, so this is general weighted matching, not just
bipartite matching or unweighted maximum-cardinality matching.

**Theorem.** Under Section 1, maximum physical payment is B+p*, where p* is
the number of matched source vertices in a maximum-weight matching of this
graph. The same matching minimizes the activation fee f* among all choices
attaining that payment. It activates exactly bundles whose slots are assigned
to sources. Moreover any specified source set payable using R_0 alone can
be retained without increasing f* or lowering p*.

**Physical allocation to matching.** Choose a maximum-cardinality residual
allocation in a physical state, and delete every activated bundle with no
assigned unit. This preserves every paid source/resource pair and does not
increase its fee. Map assigned free or group units to their source edges.
For each unused bundle add its internal edge. Source and resource uniqueness
make these edges a matching, including the case where two sources use the
two different units of one activated bundle. If p sources are paid and f
is the selected bundle fee, matching weight is

    W = Kp + Σ_{unused j}c_j = C + Kp − f.             (1)

An active bundle pays its fee once whether one or two of its slots are used.

**Matching to physical allocation.** Read every source-slot edge as an
assignment to that actual unit and activate every bundle touched by one.
Matching disjointness prevents duplicate sources or units. Any untouched
bundle has both slot vertices unused unless its internal edge is already
present, so add that edge if absent. This is safe because there are only
two slot vertices; its nonnegative weight does not hurt the objective.
For an optimum matching this completion has the same weight. The resulting
matching satisfies (1) and reconstructs a feasible physical allocation using
exactly the chosen whole bundles. All baseline payments remain independent.

Since 0≤f≤C, increasing p by one improves C+Kp−f even at the worst possible
fee change. At fixed p it strictly prefers the smaller f. Thus maximizing
weight is equivalent to first maximizing payment and then minimizing the
fee. Both directions prove the exact theorem. Standard maximum-weight
matching therefore provides a polynomial algorithm for this adapter class. ∎

The internal edge pays a *saved* fee for an unused bundle. It does not make
the two real slots share capacity one, and it is not another physical unit.
Using an ordinary capacity-two flow edge with fee c_j **per unit** would
instead charge 2c_j for two sources, which is a different objective.

## 3. Preserving old paid source identities

Let D⊆A have an injective direct allocation in the free pool R_0. Take an
optimal activation set F*. Its source-to-actual-unit graph still contains
that old allocation, because this adapter only adds supports. Augment from
that matching to maximum cardinality in this fixed graph. An augmenting
path starts at an unmatched source and ends at an unmatched resource; it
reassigns intermediate matched sources and never leaves one of them unpaid.
It therefore retains D and reaches p*. The state F* has not changed, so its
fee is still f*. Pruning unused activated bundles cannot raise that fee;
optimality implies it cannot reduce it either. This proves the preservation
claim at the **same** minimum activation fee, not only at maximum payment.

To enforce this choice in the weighted graph, add an extra bonus

    H=K|A|+C+1

to every source edge incident to a required source. H exceeds the entire
possible range of the unbonused matching weight. Since all required sources
can already be paid in R_0, the optimum must match every one; the remaining
weight still maximizes p and then minimizes f by (1).

This statement is about activation fees and the direct residual model. It
does not assert that preserving sources is free under a new link-cost or
arbitrary-route objective. Fixed baseline link costs simply add a constant.

**Numerical consequence.** Let alpha be the total source count, beta the
total beta-owner count and L the full physical positive-unit count. If the
matching pays p residual sources, set D=alpha−(B+p). The reconstructed pack
uses each original unit and beta sink at most once, so B+p≤L+beta. With
S=L+beta−alpha this gives

    |T|+|M| ≤ area/2 + D.                             (2)

If the baseline and all residual sources are paid, D=0, yielding the
coefficient-one bound |T|+|M|≤area/2 on this stated class. This is stronger
than a coefficient-5/6 bound there. It gives no universal improvement until
the geometric adapter and full-routing coverage are proved universally.
Optimization slots and unused internal edges must never replace L in (2).

## 4. A completely frozen physical shared-bundle example

Take the existing 16×28 fully frozen T83/M35 module. Put one copy on the
left of a 16×58 board and a horizontal reflection on the right under

    (r,c) ↦ (r,57−c).

Columns 28,29 are empty; all their tiles are H except the upper central
tile (2,28), initially V. Retain both copies' old direction bits, reflecting
tile origins by (r,c)↦(r,56−c). In particular lower tiles (10,16),(10,40)
are V. Keep all T and actual M edges inside their copies.

This board has |T|=166, |M|=70, alpha=4, beta=4, mixed=10, raw L=S=228.
The empty central columns separate occupied sites of the two copies, so
feasibility follows directly from each module. Replay the same 11 strict
freezing waves on both copies in parallel: the reflected witnesses and
matching mates stay internal, and all 140 endpoints freeze. The four
residual alpha tips keep their original occupied degree three.

There are two residual sources a_L (tips (3,12),(10,12)) and a_R (tips
(3,45),(10,45)), with no external exits. The other two sources are always
paid independently through their own b→z one-link routes and private Q
units. Thus the fixed baseline is B=2 and minimum baseline links is two.

Three optional single-tile V→H gates give the following resource groups:

| Gate | Old original units | Activated units | Residual supports |
| --- | --- | --- | --- |
| central (2,28) | two horizontal BB pairs at rows 2,3, cols 28,29 | two vertical BB pairs at cols 28,29, rows 2,3 | each slot supports both a_L,a_R |
| left (10,16) | {(11,16),(11,17)} | {(10,16),(11,16)} | a_L only |
| right (10,40) | {(11,40),(11,41)} | {(10,41),(11,41)} | a_R only |

All four old group units are unsupported. All group units are original
BB/TT forests; no extra numerical resource is created by activation.
The upper central tile is isolated in V by H tiles above/below, so its two
old units have no P boundary. In H its gap joins the two a boundaries through
the copies' BT-only upper corridors, giving both units to both sources.
Those two units can be assigned separately, one to each a. The lower
gates give their own source access as in the existing one-module calculation;
the next occupied V bands stop their horizontal gaps. They cannot affect
the upper corridor or each other's bands. All other owner supports and
physical links are unchanged for every gate subset. This proves the exact
simultaneous adapter, including independence of the two baseline Q payments.

| Chosen gates | Total payment | Minimum links |
| --- | ---: | ---: |
| none | 2 | 2 |
| central only | 4 | 2 |
| left only, or right only | 3 | 2 |
| left and right | 4 | 2 |
| central with either/both others | 4 | 2 |

For unit gate fees the best full repair uses central alone, cost one;
the two private repairs cost two. For fees (central,left,right)=(3,2,2),
the correct minimum full-payment fee is three, still central alone. A
per-paid-path charging rule assigns the central option cost six and chooses
the private pair cost four, which is **strictly worse** than the valid
shared-fee optimum. This is a genuine fully frozen physical counterexample
to that cost rule. Compressing the central group to one capacity-one token
would also lose a real payment: its two units have two independent source
witnesses. The preceding single-old-witness compression theorem was never
applicable to this activated shared group.

Only four of the 228 raw units belong to the optional bundles. The rest
remain in the physical pool, including the two baseline Q units and all
unreachable units. The weighted graph's dummy/internal vertices carry no
physical resource credit. This example is not a fixed-P maximum claim.

## 5. Long prerequisites and the limit of shared-cost compression

The [all-n frozen corridor](FROZEN_COORDINATED_PIVOTS.md) satisfies the same
adapter with one bundle P_j of n zero-capacity gates, two far BB units and
one residual source. Under unit primitive fees c_j=n. Both real slots have
that same sole source neighbour, so its one source vertex can use only one
slot. The theorem finds the exact one-extra-payment cost n without charging
n separate resources or counting two payments for that source. Together
with the new central two-source example, this covers both prerequisite
sharing within one payment and fee sharing across two different payments.

Pairwise disjoint P_j is needed for fee additivity. If two bundles share a
physical gate, adding their fees counts that gate twice. Merging identical
prerequisite sets is safe for costs only if all associated real units and
supports are retained; their **total** capacity, not each offer's individual
capacity, determines whether the two-slot theorem applies.

There is a standard sharp obstruction at capacity three in this abstract
adapter. Given an Exact Cover by 3-Sets instance with universe U of size
3k, make one residual source per element. For each triple X_j create an
independent fee-one bundle with three distinct units, one supporting each
element of X_j and no other source. There are no free units or baseline
routes. Full payment with at most k activated bundles is possible iff the
triples have an exact cover: k triples contain at most 3k distinct elements,
so covering all of U forces k disjoint triples. Conversely an exact cover
provides one distinct unit per source. A chosen bundle list and injective
allocation are a polynomial certificate. Thus this capacity-three abstract
decision problem is NP-complete.

Equivalently, express each triple's three units as three separate one-unit
offers with the **same** fee-one physical gate. Counting the shared gate only
once gives exactly the same reduction, despite nominal offer capacity one.
This explains why arbitrary sharing cannot be hidden by making many small
tokens and giving each a separate linear cost. It does not prove that these
arbitrary incidences/prerequisites embed in a frozen grid. No grid complexity
or new general complexity-priority claim is made here.

## 6. Validation and Lean scope

Run from the repository root:

```sh
python3 develop/check_capacity_two_gate_bundles.py \
  --output output/capacity-two-gate-bundles-validation.json
python3 develop/check_bundle_activation_cost_formal.py \
  --lean /absolute/path/to/lean-4.33.0 \
  --output output/bundle-activation-cost-formal-validation.json
```

The validator checks 120 abstract models and every enabled subset in each,
comparing a vertex-mask weighted-graph DP with independent activation
enumeration plus bipartite matching. Including physical fee profiles and
an empty-residual control gives 947 comparisons. Another 947 comparisons enforce an old free-pool paid
source set and verify exactly the same maximum value and minimum fee.
Models include one-slot dummy padding, arbitrary different slot supports,
shared free units, zero fees and overlapping source neighbourhoods.

All eight physical gate subsets are checked against the full fork flow and
an independent primitive optimizer. The check compares all owner/type/link
identities, complete positive forest replacement groups, every non-residual
support set and disjoint old/new resource groups. It replays 140 strict
freeze events and checks 64 joint states in all eight dihedral images.
Explicit controls reject the once-per-payment fee and one-token compression
rules, and two small exact-cover controls check the reduction's distinction.
The checker uses exhaustive small-graph DP for independence; it is not the
polynomial weighted-matching solver. The polynomial conclusion follows from
the general reduction to standard maximum-weight matching.

[BundleActivationCost.lean](../formal/SubQuorum/BundleActivationCost.lean)
checks four general accounting lemmas: spent and saved fees partition the
total; graph weight plus spent fee equals scaled payment plus total fee;
scale C+1 prioritizes cardinality; and equal cardinality prioritizes lower
fee. The local Lean 4.33.0 audit uses only propext/Quot.sound, with no new
axioms, sorry, native decision or warnings. The full matching reconstruction,
old-source augmentation, geometry and complexity reductions have written
proofs and independent finite checks; they are not end-to-end Lean claims.

Next: extend the residual direct-source adapter to mixed transit while
preserving shared activation fees, or identify geometric conditions allowing
overlapping prerequisites to be merged into genuine groups of capacity at
most two. Any extension must retain original units, baseline competition and
the actual joint physical support states.
