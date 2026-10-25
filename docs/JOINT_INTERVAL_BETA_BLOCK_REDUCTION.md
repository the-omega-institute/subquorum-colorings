# Joint original-interval and exclusive-beta block reduction

25 October 2026. This is an algebraic reduction on the **original** board and
its full exterior allocation network. It does not delete tiles from a frozen
board. It extends the pure-beta tree compression and the closed cyclic-beta
elimination to mixed zero/one-cost resources, with exact payment and minimum
actual-link cost. Universal geometric compensation and improvement of 5/6
remain open. The submitted 11 October manuscript is unchanged.

## Hypotheses and resource identities

Use the existing whole-support ordinary/full-fork normal form. An alpha is a
source, a mixed owner has its original capacity-one gate, a beta has its two
original BP entries and a capacity-one whole-payment sink, and every original
BB interval has capacity one. Each actual TP–BP link costs one. Write V for
maximum paid alphas and c for minimum actual links among maximum payments.
The established normal-form theorem identifies ordinary and fork optima.

Choose disjoint nonempty alpha blocks S. Each block has a connected multigraph
of the following distinct internal resource identities, with one or two
incident alpha owners per resource:

* An original interval j has nonempty whole-support owner set contained in S,
  exactly its declared incidence. No mixed, beta or outside owner supports j.
  Its cost is zero. A one-owner interval is an anchor.
* An internal beta has empty whole-body support and precisely two incoming
  actual links, from the declared one or two S owners, using its distinct BP
  tips. Its cost is one. A one-owner beta is a loop. Recognized guarded short
  betas satisfy these hypotheses by the preceding forced-guard lemma.

No original resource is internal to two blocks. Keep every exterior interval,
actual link, mixed gate, BP-entry gate, beta sink and whole-body support arc,
and every outside alpha source. An internal resource may not be supported by
outside owners. Grouped alphas may have arbitrary **exterior** exits/support.
Internal incidences have size at most two; exterior supports need not.

For each S, form the interval-only components, including isolated alphas.
A component is deficient precisely when its interval multigraph is a tree
without a one-owner anchor: its maximum interval-only payment is its order
minus one. Every other interval component is fully payable at zero links.
Let t be the number of deficient interval components. A connected joint block
is either saturated (all n=card(S) sources payable internally), or an unanchored
joint resource tree (n−1 two-owner units). In the tree case all q interval
components are deficient, so t=q. Loops/parallel resources count with their
original identities throughout.

## Local rooted allocation theorem

Let X be any set of original alphas paid by exterior paths. Put x=card(X).
For a saturated block let z count deficient interval components meeting X.
Then the exact internal optimum on S minus X is

    payment = n−x,                 minimum beta cost = t−z.             (1)

For an unanchored joint tree let z count all interval components meeting X.
Then the exact internal optimum is

    payment = n−max(1,x),          minimum beta cost = q−max(1,z).      (2)

These are graph statements, not claims inferred from enumeration.

**Proof.** An untouched deficient interval tree has one missing payment and
therefore needs a distinct beta to pay all its vertices. A deficient tree
containing r≥1 exterior roots pays its other vertices with distinct interval
edges: orient toward its roots in a multi-root forest, and assign each
nonroot its parent interval. A nondeficient interval component can pay all
its vertices with intervals (orient a spanning tree toward an anchor, or
orient a cycle and its attached trees); restricting that matching after
removing roots still pays all remaining vertices at zero beta cost.

Contract the interval components. Beta units become a connected multigraph,
with loops retained. If some component is nondeficient, it is an available
anchor. For saturated blocks, if no such anchor exists the quotient has a
cycle, since an unanchored tree has only n−1 total units. Touched deficient
components are additional anchors. When anchors exist, choose a multi-root
spanning forest toward them. Each untouched deficient component takes its
parent beta, choosing its incident original alpha as an internal root; its
remaining vertices take interval parent edges. Unneeded edges are ignored.
If there is no anchor, choose a quotient cycle, assign its distinct betas
cyclically, and orient attached trees toward it. This includes a loop or a
two-edge parallel cycle. Each deficient component receives exactly one beta.
Strictly decreasing parent distance prevents two nonroot components from
taking the same parent beta; cycle betas are distinct and disjoint from
forest betas. This attains t−z in (1), and the deficiency lower bound proves
optimality.

For a joint tree, if X is nonempty its quotient is a tree with z roots, so
exactly q−z parent betas suffice and are necessary. If X is empty, choose one
unpaid original root and use all n−1 original tree resources, of which q−1
are betas. With X nonempty each remaining alpha is paid. With X empty a tree
cannot pay n sources from n−1 resources. This proves (2). No original interval,
beta, alpha tip or BP entry is used twice. □

## Simple saturated elimination and its cost condition

Remove saturated blocks algebraically and write (V_res,c_res) for the full
residual exterior problem. If their total order is N and their total number
of deficient interval components is T, then

    V=N+V_res,                     c_res ≤ c ≤ T+c_res.                (3)

If all grouped alpha direct interval support is internal, then exactly
c=T+c_res. Outside paths cannot enter grouped alphas, internal intervals or
internal betas. Dropping grouped-source routes therefore leaves all outside
payments feasible; their minimum cost is c_res. Conversely, internal complete
matchings lift any residual optimum. For the exact cost assertion, at most
N−T grouped sources can be paid at zero links. Any other grouped-source route
has an actual link, distinct from links on the retained outside routes.
Thus every full optimum has at least T+c_res links. This argument also handles
exterior mixed routes and beta body continuations, using the existing
private-beta-first fork normalization.

The cost condition is necessary for this *simple* elimination: on the actual
frozen tight-pocket board, choose one of the two shared original intervals
and the older beta as the internal two-alpha cycle. Its internal cost is one,
but the omitted second interval supplies full cost zero. This refutes the
unconditional equality in (3), not the geometric target or the reduction below.

## Unconditional joint reduction, retaining optional exits

Formulae (1)–(2) give exact cost even when grouped alphas have exterior support.
For a tree retain at most one exterior root per interval component. For a
saturated block retain at most one root per **deficient** interval component;
discard roots in nondeficient components. These pruning operations preserve
all outside paid sources and total maximum payment, and cannot increase cost:
reallocate the removed roots internally using (1) or (2), whose beta cost is
unchanged. They release exterior capacity. Their discarded paths have
nonnegative link cost. If a tree had any exterior roots, retain at least one.

Define baselines over the chosen blocks:

    B = sum_saturated n + sum_tree(n−1),
    C = sum_saturated t + sum_tree(q−1).

In the retained full exterior network make these source interfaces:

* Each outside alpha has one source arc, reward −M.
* Each tree has one first source unit, reward −M, and q−1 further units,
  reward −1 each. All go through capacity one per interval component,
  then choose any original alpha in that component as their exit.
* Each deficient interval component of a saturated block has an optional
  capacity-one source arc, reward −1, then chooses an original alpha exit.
  Nondeficient interval components have no source arc.

Keep the entire exterior network with actual-link cost +1; close sink to
source with a zero-cost return arc. Internal resources are removed from this
network only, while B and C retain their ledger contributions. Set M=L+C+1,
where L is the number of candidate original actual links. Use an integral
minimum-cost circulation and remove any unnecessary path/cycle at a tie.

Let R be outside paid sources plus active tree groups, let e be exterior
actual links, and let

    b = active saturated deficient components
        + sum_tree max(0, active interval components−1).

Then the exact original optimum is recovered as

    V=B+R,                         c=C+e−b.                           (4)

**Proof of exactness.** The retained component gates enforce the pruning
rules. Each active tree group uses its first arc: exchanging an extra arc
for an unused first arc strictly improves objective. Hence network objective
is e−b−MR. We have 0≤b≤C and 0≤e≤L after removing nonnegative cycles and
normalizing exterior routes. The chosen M first maximizes R and then minimizes
e−b. Lifting uses (1)–(2) with precisely the chosen original exits, adding
C−b different internal beta links and distinct internal intervals. Internal
and exterior resources are disjoint. It pays B+R at exact cost C+e−b.

Conversely, decompose an original optimum into source routes in the existing
normal form. No outside route uses internal resources. If a grouped source
has not all possible internal payments, complete its local matching after
retaining its existing exterior roots; this cannot disturb any outside route.
Thus a maximum optimum has the local values in (1)–(2). Prune roots as above,
retaining total payment with no higher cost. It projects to the displayed
network, whose objective cannot exceed the projected optimum. Together with
the lift this proves both equalities. Capacity-one mixed gates and original
beta entries remain present during projection, normalization and lift, so
cross-block contention is never replaced by separate optimistic optima. □

This is an application of integral allocation/min-cost flow and the local
resource-graph theorem. It is not a new general flow theorem.

## Why an alpha-exit discount is false

Take three alphas a,b,c, one internal interval incident to a,b and one internal
beta incident to b,c. Give a and b distinct exterior zero-link intervals.
Both exterior exits meet the **same** interval component {a,b}. Alpha c still
requires the beta: full payment is three and exact minimum link cost is one.
A rule that deducts one beta for every additional alpha exit incorrectly
predicts zero. The verifier records both that invalid prediction and its
actual lifted cost one; the Lean assignment control independently forces c
to use the cost-one resource. This is an abstract eligible-resource example;
no frozen realization is asserted. The failed statement is the exit-based
discount rule, not a counterexample to universal geometric compensation.

## Original-resource deficit ledger and remaining geometry

Let k be all original alpha sources, p the outside ones, g the number of tree
blocks, and E the sum over saturated blocks of internal-resource-count minus
order. Original interval and beta counts are I and b_beta. Then

    I+b_beta−k = E+(I_exterior+b_exterior)−(g+p),
    k−V = (g+p)−R.

This follows by partitioning original resource identities, never by assigning
one scalar surplus to two residual blocks. Unused internal excess remains in
E; it is not turned into fictitious exterior routes. A geometric proof still
has to bound the **joint exterior** cuts with their retained mixed/BP/interval
capacities and the cost term in (4). The present theorem isolates that task;
it does not establish all frozen configurations or improve 5/6.

Interval reservations in the physical controls remove units from the available
allocation pool while preserving the original board. They are not geometric
deletions and do not assert freezing survives a board modification. In
particular the preceding short-beta deletion obstruction is fully respected.

## Reproduction and formal scope

Run:

    python3 develop/check_joint_interval_beta_blocks.py --output output/joint-interval-beta-blocks-validation.json
    cd formal
    lean SubQuorum/JointIntervalBetaBlocks.lean

The checker compares the full old optima with simple and discounted reductions,
lifts actual links and checks endpoint disjointness/payment, checks residual
negative-cycle optimality, and compares small cases with independent primitive
pack optimization. Controls include arbitrary root sets, loops, parallel units,
anchors and cycles; actual frozen tight/loose pocket boards; and all 0/1/2
pocket-interval reservations in up to four independent copies. Abstract random
exterior supports are flow controls, not claimed physical grid realizations.
Exact totals and named controls are in the machine-readable output.

The standalone Lean source checks representative injection, nonreuse of actual
parent beta edges, the mixed-tree count ledger and budget, the saturated count
ledger, and the exact small discount obstruction. Its axiom audit is retained
alongside a formal receipt. The general resource-graph allocation, exterior
network projection/lift, and physical adapter are written mathematical proofs,
not claimed as end-to-end Lean formalization. Finite enumeration checks these
proofs and finds rule errors; it does not replace their general arguments.
