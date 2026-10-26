# New beta admission without losing old interval identities

26 October 2026. Wenlin Zhang and Haobo Ma. Independent research continuation.

We remove the beta saturation guard from the
[general mixed-head retention theorem](GENERAL_BRIDGE_RETENTION_AND_DEFICIENT_RELAYS.md).
New links may enter previously unused beta owners. At maximum payment, minimum
actual new-link fee, and then minimum actual new-link count, an optimum still
retains every old paid alpha, every old used original interval ID, and every old
whole-beta credit. The important change is to maintain beta normalization after
**each augmentation**, by choosing a shortest residual path with the fewest
residual arcs among cost ties. There is no identity-changing post-processing.

The exact full physical fork flow and successive shortest augmentations are
established tools. The contribution here is the normalization-preserving
shortcut argument in this resource-first network, and its consequence for
simultaneous source/resource retention. This is not a new general flow algorithm.
Finite optimization checks below test the construction; the proof is for all
finite instances satisfying the stated hypotheses.

## 1. Model and theorem

Fix the final original owner types, actual TP/BP tips and permitted links,
original interval pool Q, whole-owner supports W(o), and declared payable alpha
set U. An alpha has no BP, a mixed owner has one BP/TP pair, and a beta has two
BP tips and no TP. Each beta supplies one private whole-beta resource, separate
from all original intervals. Each interval has a single global identity even
when several owners support it. No two-owner incidence hypothesis is needed
for the network theorem; the old request-tree adapter still uses that hypothesis.

Let E0 be a set of free old links whose owner graph is directed acyclic; an
owner-disjoint old normalized stem/fork skeleton is a sufficient special case.
Let P be **any feasible normalized packing using E0**, with paid alpha set A0,
original interval set I0, whole-beta set B0, and

    p0 = |A0| = |I0| + |B0|.

A maximum old request allocation's standard lift is an important application,
but initial maximality is unnecessary here. In particular, zero-cost augmentations
using only E0 are permitted. All supports and resources are those of the fixed
final model, after any destructive direction change. We do not promise retention
of resources which disappeared before P was formed.

Add any set E+ of actual links disjoint from E0, with nonnegative integer fees
w(e). Candidate pairs may share stems, enter deficient components, and enter
previously unused beta bodies through either actual BP tip. Eligible mixed
owners outside the old skeleton are also allowed. Mixed self-links are discarded.
Let m=|E+| and encode each new link's cost as

    c(e) = (m+1)w(e) + 1.

All other arcs and old links have cost zero.

**Theorem.** There is a normalized packing using only E0 union E+ that
simultaneously:

1. attains the globally maximum payment F;
2. minimizes actual new-link fee at payment F;
3. minimizes the number of actual new links at that minimum fee;
4. retains A0, I0 and B0 as subsets of its paid-source and used-resource sets.

It is found by one resource-first integral minimum-cost maximum-flow computation
initialized with P, choosing every augmentation by minimum encoded residual cost,
then minimum number of residual arcs among those cost ties. If I and B are its
final original interval and whole-beta sets, then

    F-p0 = |I minus I0| + |B minus B0|.                 (1)

Thus new whole-beta credits are part of the net gain; they must not also be
counted as fresh interval gains. There is no new-beta reachability guard. This
is an existence/construction statement, not a claim that every cost-optimal
flow or every cost-only tie rule preserves normalization.

The local residual-arc-count tie rule is **not a fourth global objective**. We
claim no minimum of total old plus new link count, nor of final internal arcs.

## 2. Resource-first network

Reverse the established alpha-to-payment physical fork network:

- s -> unit(j), capacity one, for every original j in Q;
- s -> body(b), capacity one, for every private whole-beta credit;
- unit(j) -> output(o), capacity one, for j in W(o), with beta output its body;
- mixed output -> input, capacity one;
- beta body -> each of its two separate actual BP tips, capacity one per tip;
- reverse each actual link, from its head mixed input or beta BP tip to its
  tail owner output, capacity one, with the encoded cost for a new link;
- output(a) -> t, capacity one, for every a in U.

All listed capacities are one. An interval source arc is shared globally by
all its possible support access arcs. Whole-beta and interval source arcs
represent different resource types. A beta body's total outgoing flow through
its BP tips is at most two.

Reverse the paths of P to initialize the flow. Each old beta singleton/fork
already uses exactly one private beta credit and at most one interval. The
initial value is p0 and cost is zero, hence it is globally minimum-cost at that
value because every forward cost is nonnegative.

## 3. The private-beta shortcut lemma

Call a feasible flow **beta-normal** if every beta of positive BP-port flow
has its private source arc saturated. Conservation and the two BP ports then
leave at most one interval path at that beta. The initial flow is beta-normal.

**Lemma.** Suppose f is an integral beta-normal flow, minimum-cost among flows
of its current value. A simple residual s-to-t path of minimum cost, with the
fewest residual arcs among cost ties, cannot first enter an unused beta body
through an interval access arc. If it uses such a body, its first arc is the
private source arc s -> body(b).

**Proof.** An unused beta has no positive body/port flow by beta-normality.
There are therefore no reverse used-port arcs entering its body. Its only
possible incoming residual arcs are its unused private source arc and original
interval access arcs. Suppose the selected path enters through

    unit(j) -> body(b).

Write R for its prefix from s to unit(j). The access arc has zero cost.

If the source arc s -> unit(j) is unused, resource-node conservation says that
all access arcs out of unit(j) are unused. No reverse access arc can enter it.
Its only incoming residual arc is s -> unit(j), so R is that zero-cost arc.

If the source arc is used, the zero-cost reverse arc unit(j) -> s is residual.
A negative-cost R followed by that return arc would be a negative residual
cycle, contradicting minimum-cost optimality of f at its value. Thus R again
has nonnegative cost. This reasoning includes residual reverse links with
negative individual cost; it does not assume all residual arcs are nonnegative.

In both cases the entire prefix to body(b) has nonnegative cost and at least
two arcs. Replace it by the unused zero-cost private arc s -> body(b), keeping
the same suffix to t. The result is a residual simple path: its suffix never
returns to s or revisits body(b). If the removed prefix had positive cost,
this contradicts minimum cost of the original path. If it had zero cost, the
replacement has equal cost and strictly fewer arcs, contradicting the tie rule.
Therefore the proposed interval entrance cannot occur. ∎

Equivalently, nonnegative reduced-cost potentials telescope along R; the
residual zero-cost return arc supplies its final lower bound. The
[Lean kernel](../formal/SubQuorum/NewBetaRetention.lean) formalizes this general
finite-walk argument, including possibly negative residual edge costs, and the
strict lexicographic shortcut comparison. The network-specific incoming-arc
case split above remains part of the written proof.

## 4. Induction, extraction and optimality

**Normalization and retention.** Perform successive shortest residual
augmentations, using the lemma's tie rule. Every used resource source arc and
paid-alpha sink arc stays saturated: a simple path cannot return to s or depart
from t, so it cannot reverse one of those boundary arcs. This retains the initial
identities, and also retains every newly activated resource at subsequent steps.

If a previously unused beta is touched, the lemma forces its private source
arc to be the first arc of the augmentation. It becomes a used beta with its
private credit present. Every previously used beta retains its private source
arc, and still has total flow at most two through its BP ports. Hence all betas
remain normal after the augmentation. In particular, at most one new beta is
activated in a single augmentation. No interval is substituted or discarded.

A shortest residual augmentation takes a minimum-cost flow at value v to a
minimum-cost flow at v+1. The extra tie rule chooses one of those shortest
paths, so it preserves this standard optimality theorem. Minimum-cost flows
have no negative residual cycles at every step, supplying the lemma's induction
hypothesis, not just a final check. At termination the flow is maximum, with
exact max-flow cut and min-cost residual-potential certificates.

**Extract a packing.** Every forward circulation would contain a new link:
zero-cost E0 is directed acyclic, and support/resource/sink arcs cannot form
an owner cycle. Every new link has strictly positive encoded cost, even if its
actual monetary fee is zero. A minimum-cost flow therefore has no circulation.
Decompose it into resource-to-alpha paths. Mixed gates and alpha sink arcs
prevent owner/source reuse. Beta-normality makes every used beta group exactly
one beta singleton or one beta fork with two different BP ports and at most
one interval. No normalization substitution is needed. Each original interval
has one source arc, so its identity occurs at most once globally.

**Exact objectives.** Every normalized packing on the permitted links defines
a feasible reversed flow with the same payment and encoded cost. The constructed
flow extracts to a normalized packing with exactly its resources and links.
It therefore attains the global normalized optimum, while preserving all old
boundary identities. As at most m distinct new links can be used, the scale
m+1 makes actual integer fee dominate new-link count. This proves the theorem.

**Exact ledger.** The extracted packing has F=|I|+|B| and the old packing has
p0=|I0|+|B0|. Since I0 subset I and B0 subset B, subtraction gives (1). Both types
are injectively used, and the two types are disjoint. In particular there exists
an optimum with at most F-p0 newly activated betas. Under the former guard
B=B0, so this reduces to the earlier statement that all gains are fresh intervals.

## 5. Why arbitrary cost ties followed by normalization are insufficient

The [explicit fixture](../develop/fixtures/new_beta_shortest_path_tie.json)
has alphas A,C, beta B, old unit u supported by A and B, and fresh unit v
supported only by A. The old packing is A:u; C has empty support. The only
new link is C -> B, with fee one. The maximum payment is two and needs this link.

One minimum-cost residual augmentation is

    s -> v -> A -> u -> B_body -> B_tip -> C -> t.

Here A -> u reverses the old access arc. The resulting raw flow pays A with v
and C with u at beta B, whose private credit is unused. Replacing C:u by C:B
in post-hoc normalization drops the old identity u. Payment and actual fee stay
optimal, but original-unit retention has been lost.

The shortcut

    s -> B_body -> B_tip -> C -> t

has the same cost and four rather than seven residual arcs. It retains A:u
and pays C with the new whole-beta credit. The fixture rejects the arbitrary
cost-tie-plus-post-processing **rule**, not the retention theorem and not any
original grid inequality. It is an abstract canonical owner system.

A separate control has A supporting u,v, a new beta supporting u, and two
empty sources entering its different BP ports. Full payment three retains old
u by moving it into the new beta fork, moves A to v, and uses the beta credit
once. Thus the theorem permits an old interval to enter a newly used beta
**after its private credit is activated**; it does not ban such reallocations.
Sending both sources to the same BP tip gives only two payments.

## 6. All-length transport with one new beta and no fresh intervals

For r>=1 take alphas A0,...,Ar, mixed X0,...,X(r-1), and a beta B. The old
stems are Ai -> X(i-1), 1<=i<=r. Unit ui is supported exactly by Ai and X(i-1).
A0 has empty support and beta B has no interval support. The old packing
pays Ai directly using ui, for payment r, retaining all r distinct units.

Add Ai -> Xi for 0<=i<r and Ar -> one fixed BP tip of B. Payment r+1 uses
Ai -> Xi with u(i+1), 0<=i<r, and Ar -> B with B's private credit. It retains
all r old paid sources and all old units, adds no fresh interval, and activates
exactly one new beta.

All r+1 added links are necessary. A0 must enter X0 and take u1. Inductively
Ai cannot reuse ui or the occupied X(i-1), so it must take the next new link,
ending in Ar -> B. Deleting any new link leaves maximum r; the old packing
still attains r. With unit fees the exact new-link count and fee are r+1.
Thus a single new-beta gain may require arbitrarily many new links; beta
activation count does not replace actual bridge costs. This family is abstract,
with an all-r proof, not a claimed all-r frozen realization.

## 7. Frozen-grid instantiation and counting consequence

The existing all-H 28 by 24 board has 49 selected cells, 154 matching edges,
and 308 strictly frozen endpoints. Keep the same three old stems and specified
old interval IDs from the [shared-stem fixture](../develop/fixtures/frozen_shared_stem_bridge_synergy.json).
Its empty-support right alpha12 has the actual adjacent link

    (5,19) -> (5,20), from alpha12 into previously unused beta4.

Declare only this new link in addition to the old skeleton. Keep all three old
payments and interval IDs, and pay alpha12 by beta4. Payment rises 3 to 4, with
one new beta, no fresh intervals, and one new link. One link is also necessary
because alpha12 has neither direct interval support nor another permitted exit.
The former beta guard rejects precisely this newly reachable beta; the new
algorithm handles it without substitution. This instantiates the new retention
theorem on an already known board; it is not a new unrestricted geometric
compensation improvement.

For any q>=1, translate copies by (30i,0), separated by two blank rows, exactly
as in the existing frozen-family proof. Original supports, actual links and
freezing certificates separate. Declare the translated right-to-beta link in
each copy. With unit fees, for all q:

    3q -> 4q, retain 3q old intervals,
    fresh intervals 0, fresh whole-betas q, minimum new links q, minimum fee q.

All old beta credits are absent in this example. The board is (30q-2) by 24,
with L=155q-24 and the previously computed positive slack; no target inequality
is contradicted. The q=16 production check gives 48 to 64, retaining 48 old
intervals and activating 16 different beta credits with 16 new links.

For all original alphas declared and an old maximum request lift
p0=alpha-t0, put mu=F-p0. As before,

    L+beta >= F = alpha-t0+mu,
    |T|+|M| <= area/2+t0-mu.

The formula now covers arbitrary mixed-head **and beta-head** additions, with
mu split exactly between fresh intervals and new betas. The remaining declared
routing defect alpha-F has its usual exact network cut. To improve the universal
5/6 bound one must still prove the necessary geometric cut lower bound for
actual bent paths, capacity-two tiles and occupied bands. This result closes
the identity-safe beta-admission gap; it does not supply that geometric bound.

## 8. Verification and formal scope

The [production solver and independent controls](../develop/check_new_beta_retention.py)
check beta normality, old boundary saturation and absence of negative residual
cycles at initialization and every augmentation. Extraction is checked against
independent normalized primitive certificates on small systems. Global min-cost
potentials cover all residual arcs, including those entering s or leaving t;
max-flow cuts are also checked. Production uses no primitive/mode enumeration.

The [saved computation report](../output/new-beta-retention-validation.json)
records 1,210 independent unrestricted and 1,210 identity-prescribed
lexicographic optima (including 437 new-beta models, 27 new-beta forks and
63 augmentations with reverse links),
new-beta forks, reverse-link augmentations, all old baselines on selected cases,
two additional arbitrary-support/nonmaximum-or-empty-baseline controls,
the cost-tie negative control, 35 transport bridge-deletion checks and the r=64
production chain. It also records four actual frozen q=1,2,4,16 boards, both
previous mixed-head regression and new-beta admission. Their freezing schedules
supply 7,084 checked endpoint events; small physical cases have independent
restricted full-flow checks and q=1 has an identity-prescribed primitive check.
The q=16 production solver has independent optimizers disabled.

The [Lean source](../formal/SubQuorum/NewBetaRetention.lean) and
[formal report](../output/new-beta-retention-formal-validation.json) cover four
scoped general kernels: finite residual-walk reduced-cost telescoping,
nonnegative prefixes with a resource return arc, strict shortcut improvement
in the local cost/arc-count order, and the fresh interval/beta gain ledger.
The whole graph-specific induction, flow equivalence, min-cost theorem, frozen
geometry and all-size constructions are written proofs with executable checks,
**not end-to-end Lean formalizations**. Standard logical axiom dependencies
are reported explicitly. The local runner measures memory and actual
comm-basename lean/lake processes before every Lean executable invocation.

Reproduce from the repository root:

    PYTHONDONTWRITEBYTECODE=1 python3 develop/check_new_beta_retention.py --output output/new-beta-retention-validation.json
    PYTHONDONTWRITEBYTECODE=1 python3 develop/check_new_beta_formal.py --lean /path/to/lean-4.33.0 --output output/new-beta-retention-formal-validation.json

The submitted manuscript, public main, PR #3, shared CI and correspondence are
separate from this research continuation.
