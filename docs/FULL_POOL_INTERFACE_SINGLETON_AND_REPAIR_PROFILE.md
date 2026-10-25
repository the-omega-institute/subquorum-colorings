# Full-pool interface singleton obstruction and exact repair profile

25 October 2026. Wenlin Zhang and Haobo Ma. Research branch only.

A positive closed-local payment and a separately payable interface need not
coexist, even on the **entire original resource pool** of a fully frozen
mixed-direction board. We identify the exact common singleton and prove an
arbitrary-copy repair profile, including the difference between unrestricted
and old-source-preserving minimum link cost.

This uses the sealed board of the existing [full-pool singleton
obstruction](FULL_POOL_SINGLETON_OBSTRUCTION.md), not a new unrelated grid
construction. The new specialization permits actual matching edges to cross
a mixed-direction partition, has positive closed-local payments, identifies
the exact interface loss, and resolves every subset of the isolated repairs
from the [interface reoptimization note](INTERFACE_RESERVE_REOPTIMIZATION.md).
The failure is of automatic full interface compensation, not of the numerical
grid inequality. No new universal 5/6 bound or change to the submitted paper
is claimed.

## 1. Statement with the FULL original pool

Fix any even W>=8, q>=1 and repair set H contained in {0,...,q-1}; put s=|H|.
Take q copies of cropped(W) from the raw-pool sealed family, separated by
TWO entirely blank rows. Copy i starts at row d_i=i(W+4). In copy i remove
the selected point (d_i,1) exactly when i belongs to H. Keep all other T,
all P and the original actual matching M unchanged. The complete board is

    height=q(W+4)-2, width=22.

In each copy use horizontal bands on columns0,...,13 and vertical bands on
columns14,...,21. Give each two-row blank separator its own horizontal
rectangle of width22. These are a valid disjoint even-rectangle partition;
their bands give exactly one auxiliary mate per vertex. Use ALL original
units, including boundary units, separator units and units supported only
by source-free owners. There is no reservation or availability restriction.

**Theorem 1 (full-pool interface profile).** The board is feasible and all
q(6W+20) actual endpoints are frozen. It has

    T=41q-s,       M=q(3W+10),
    S=area/2-T-M=q(8W-7)+s-22>0,
    original units L=q(15W/2-3)+s-22,
    global alpha=2q, global beta=q(W/2-2), global mixed=8q.       (1)

There are 2q crossing actual M edges, q CC relays and q new interface alphas.
The closed local systems have q alpha sources and can pay all q of them,
with minimum link cost 2q-s. The interface alphas, considered by themselves,
can all be paid directly at cost zero: h(Q)=q. Nevertheless the complete
restored model, including all original owners, gates, links and betas, has

    V_global=J(Q)=q+s,   D_global=q-s,   theta=s.                (2)

Thus the exact interface loss in the previous theorem is q-s. At H=empty,
local deficit is zero and h(Q)=q, while the full global deficit is q.

If all q old alpha identities must stay paid, a maximum still has value
q+s, but its minimum link cost is

    protected minimum cost=2q-s.                               (3)

Without that identity requirement the minimum cost at the same maximum
value is s. A minimum-cost unrestricted maximum must omit each unrepaired
old source and instead pay its interface source. The cost difference is
exactly 2(q-s); value preservation alone does not assert cost preservation.

The sole shared live units are j_i, one per copy. The new interface sources
paid in a maximum that retains ALL old sources are exactly those in H.
All statements are proved for arbitrary W,q,H below, not extrapolated from
finite computations.

## 2. Geometric adapter and arbitrary-route closure

It suffices first to analyze one copy in local coordinates. Let

    A: alpha tips (1,5),(W,5),
    I: interface alpha tips (1,13),(W,13).

Exactly (1,13)--(1,14) and (W,13)--(W,14) cross the vertical cut. On the
right they join a CC relay; on the left there are two CT half-paths.
Restoration makes I. No other boundary owner is created.

The complete owner closure reachable from A or I consists of these eight
owners. The indicated arrows are all non-self declared TP-to-BP owner links
out of that closure:

| Owner | Ordinary tips | Non-self exits | Whole support in the FULL pool |
| --- | --- | --- | --- |
| A | (1,5),(W,5), both TP | U0,U1,L0,L1 | empty |
| I | (1,13),(W,13), both TP | none | {j} |
| U0 | (1,3) TP, (1,4) BP | none | {l} if repaired; empty otherwise |
| U1 | (1,6) BP, (1,7) TP | U2 | empty |
| U2 | (1,8) BP, (1,9) TP | none | empty |
| L0 | (W,3) TP, (W,4) BP | none | empty |
| L1 | (W,6) BP, (W,7) TP | L2 | empty |
| L2 | (W,8) BP, (W,9) TP | none | {j} |

Here j=(W/2,11,11) consists of the BB cells (W,11),(W+1,11). If the
isolated T point (0,1) is removed, l=(0,1,1) consists of (0,1),(1,1).
The triples denote original band/first/last identities in the concatenated
partition. In a stack add the cumulative band offset to the first entry.

**Why this table is uniform.** Substitute the two sealed column lists from
the prior construction, subtracting four from their row coordinates as in
cropped(W). The left vertical column5 gives A; its upper and lower neighbors
are the six displayed closed mixed owners. Along each top/bottom two-row
band their only non-self TP-to-BP steps are A to the four adjacent entries,
U1 to U2 and L1 to L2. The outward tips at column3 have no further BP entry.
The selected top cells (0,11),(1,10),(1,12) seal the upper inward gap.
The corresponding lower gap has exactly the one BB unit j, supported by
L2 and I. All other intervals in those bands lie beyond owners not reached
by these exits. The upper outward gap has no unit while (0,1) is selected;
removing precisely that isolated point creates l and changes no TP/BP tip.
The lower outward gap remains sealed by (W+1,1),(W,0),(W,2).

More explicitly, the upper inward gap is columns10,...,12 of band0: it
has length three and exactly three T cells (1,10),(0,11),(1,12), so zero
original units. The bottom gap in the same columns has only (W,10),(W,12)
selected, so its unique BB unit is j. The outward gap columns0,...,2 has
three T cells at either end of the board, except after the upper (0,1)
repair; that deletion opens exactly l. The old A body is column5, and
every middle band has P columns4 and6 immediately beside it, so no
unlisted middle interval enters its whole support.

On the right, the auxiliary pairing is across consecutive columns14/15,
16/17,18/19,20/21. The two cut ports lie on the same CC strand. Its body
is exactly {(r,c):1<=r<=W, c in {14,15}}. Traverse the auxiliary row edge
14--15 at every row; successive actual vertical matching edges alternate
between column15 at odd rows and column14 at even rows. This is one path
from (1,14) to (W,14), for every even W. Its band14/15 has PP at every
row1,...,W and BT at rows0,W+1, so there is no original interval to its
body in that band. It joins the CT tips into I without supplying another
resource. At I's ordinary TP ends, the neighbor at column12 is selected;
column14 lies across the region boundary and is not a declared band link.
Thus I has no declared outgoing link. The extra right beta strands are

    ((r,16),(r+1,16)), r=4,6,...,W-4,
    ((W-2,16),(W-1,18)).

There are W/2-2 of them. The two remaining source-free mixed owners have
tips ((2,16),(3,16)) and ((W-1,7),(W-1,8)). Every other P strand is a
cycle. They lie outside the displayed closed reachable set; none is a
hidden beta sink or alternate exit for A or I. Increasing W adds internal
strands without changing any of the table's exit or support cases.

A directed route starting at A or I therefore stays in this eight-owner
set, for any route length. It never reaches a beta. Its interval payment
can only be j or, in a repaired copy, l. This proves exclusion of all
other original units and all beta sinks for arbitrary routing, not just
for one optimizer's chosen links.

## 3. Exact value and link cost in one copy

In an unrepaired copy both roots can only end at j. An injective original
allocation pays at most one source. I pays j directly, so the unrestricted
maximum is one at cost zero. Paying the old A instead requires the two
links

    (W,5)->(W,6), (W,7)->(W,8),                              (4)

and is possible at cost two. The table shows that no shorter old route
ends at any available resource. If old A remains paid, I cannot be paid.

In a repaired copy the original pool includes l. A reaches it by the
single link (1,5)->(1,4), while I uses j directly. Both sources are paid
at cost one. No zero-link solution pays A, because its own whole support
is empty. Thus the value and minimum cost are two and one. Keeping both
source identities imposes no additional cost in that copy.

Now stack copies with the two blank separator rows. The original feasible
T sets from distinct copies are at distance at least three, and no actual
M crosses the separators. Each old all-W freezing schedule still applies
inside its copy. Removing (d_i,1) is removing one isolated ADDITION, not a
freezing seed, so every endpoint neighborhood and mate in that schedule
is unchanged. This proves feasibility and freezing for every q and H.

No declared owner link crosses copy regions, and separator units have no
supporting owner. The original band identities j_i and l_i belong to
separate regions and are all distinct. The eight-owner route closures
are disjoint. Consequently both the value upper bounds and the explicit
payments above add over copies. This proves (2), (3) and both cost claims.
Each old source individually requires two links if unrepaired and at least
one if repaired; different copies share no links, so the protected lower
bound is also additive.

Counts of T,M,P follow by translation. Each separator adds 22 original BB
units, no owners and no selection. The beta list above gives the beta
count; the table plus the two additional source-free mixed owners gives
eight mixed owners per copy. The exact port ledger then gives
L=S-beta+alpha, yielding (1). For W>=8, q>=1, S>=57q+s-22>=35>0.
These are positive-slack boards, not counterexamples to the target numerical
inequality. The construction is not claimed globally extremal in P or T.

## 4. Exact full-pool withdrawal witness and repair mechanism

Let E={j_i : 0<=i<q}. Every I_i supports just j_i, and each local old
source A_i can avoid j_i exactly when i is repaired. All other reachable
units are the private l_i; units outside these closures are source-free.
For ANY J contained in E, with the remainder of the FULL pool retained,

    sum_R V_R(Q minus J)=q-|{i not in H : j_i in J}|,
    h(Q minus J)=q-|J|.                                      (5)

Thus the joint withdrawal expression is exactly

    |{i not in H : j_i in J}|.                             (6)

By the earlier shared-unit elimination no other withdrawal is needed.
Its maximum is q-s, attained by deleting all unrepaired j_i. The smallest
withdrawal witness is exactly that set. Each repaired j_i may additionally
be deleted without changing the maximum, so there are 2^s minimizing
retained-pool witnesses among the E-restricted choices. If s=q the smallest
withdrawal is empty and full compensation holds.

These are genuine singleton ORIGINAL-owner classes: U(j_i)={I_i,L2_i}
and no other unit has that same owner pair. They survive the exact
[support-class saturation](SUPPORT_CLASS_SATURATION_AND_SINGLETON_CORE.md).
Their old local withdrawal loss is one only in the unrepaired copies.
Opening l_i changes this loss from one to zero, without changing the
interface support or inventing another copy of j_i. This is the exact
cross-component repair mechanism.

If one deliberately chooses the lower old route (4) in EVERY copy, all
j_i are spent and its fixed-pack unused matching number is zero, even in
repaired copies. The optimized theta=s then strictly improves it when
s>0. Those initial packs maximize local value, but are not minimum-cost
where repaired. Starting with locally minimum-cost packs instead leaves
exactly s accessible j_i unused, giving nu=theta=s. At s=0 every local
maximum spends its sole reachable j_i, so no local rerouting repairs the
interface even on the full original pool.

## 5. What fails, and what remains open

The s=0 family refutes the following rule, with an arbitrarily large gap:

> If every closed local system can pay all its old sources and the interface
> alphas have a full direct matching into the complete original pool, all
> old and new sources can be paid together after local rerouting.

The exact joint-cut criterion remains valid and detects the failure. The
upper bound D<=sum D_R+a-theta is attained here with positive old local
payment q; this is different from the earlier sharp crossing-port family,
whose closed local systems were source-free. This theorem also checks the
FULL restored model: omitted interface relays/betas cannot repair it, by
the explicit arbitrary-route closure. The modeled links are the declared
links for this legitimate regional auxiliary partition; the result does
not assert failure for arbitrary extra links, different auxiliary partitions
or a globally extremal choice of P,T. Those geometric freedoms remain
necessary candidates for the universal 5/6 problem.

## 6. Reproducibility and formal scope

    python3 develop/check_full_pool_interface_profile.py \
      --output output/full-pool-interface-profile-validation.json

The verifier rebuilds physical bands, owners and all original units. It
checks complete feasibility/freezing, the translated serial certificate,
all region/crossing ledgers, the exact full reachable table, both value/cost
profiles, protected paid identities and all shared-unit withdrawals at small
q. Independent primitive packing checks the small full original models.
Finite checks corroborate the all-W/q/H proofs above.

[Lean source](../formal/SubQuorum/FullPoolInterfaceProfile.lean) checks the
parametric indexed eight-owner graph: arbitrary route length preserves
copy index, old routes never reach the interface, payments stay in that
copy's shared/private units, and an unrepaired copy cannot pay both roots
injectively. It also checks route-length lower bounds, distinct final
unit identities, exact aggregate arithmetic and the concrete W8 physical
adapter constants. It does not formalize the general geometric extraction,
all-W freezing, max-flow duality or the finite-cardinality summation of the
per-copy bounds; these remain written proofs and separately checked code.

The recorded run passed 92 fully frozen FULL-pool boards, including every
repair subset for q=1,...,4 at W=8,10 and further heights through W=64.
It replayed 37,800 uniform serial freezing events, checked 300 exact
eight-owner closures, 1,176 shared-unit withdrawals and 24 independent
primitive value/cost profiles. All 21 new Lean declarations passed locally
on Lean 4.33.0, with two axiom-free declarations and only standard Lean
axioms in the others; no warnings, placeholders, native decision shortcuts
or new axioms. Memory and real Lean/Lake executable basenames were checked
before each attempt, and unrelated 4.35.0 jobs were preserved.

* [Full-pool computational receipt](../output/full-pool-interface-profile-validation.json)
* [Formal scope and receipt](../output/full-pool-interface-profile-formal-validation.json)
* [Lean declaration audit](../output/full-pool-interface-profile-lean-validation.txt)
* [W8 unrepaired actual board and full original pool](../develop/fixtures/full_pool_interface_singleton.json)
