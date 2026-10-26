# Shared prefix/suffix reserves: exact donor-tree contraction and retained-unit flow

26 October 2026. Wenlin Zhang and Haobo Ma. Independent research continuation.

Continuation: [general mixed-head retention and deficient-tree relays](GENERAL_BRIDGE_RETENTION_AND_DEFICIENT_RELAYS.md)
remove the disjoint-pair/donor/receiver guards under beta saturation, and give
an explicit obstruction to extending the one-outlet contraction unchanged.

The [private prefix/suffix theorem](PRIVATE_PREFIX_BRIDGE_COMPENSATION.md)
gave a sufficient geometric certificate for bridge compensation. We now remove
its private-unit hypothesis entirely, retaining the ordered entrance and the
restriction that candidate bridges connect disjoint pairs of reference stems.
Donors must lie in deficient reference request trees; receivers must lie in
nondeficient reference request components. Shared reserves are allocated once
in a single receiver-slot min-cost flow.

The established [whole-support fork flow](WHOLE_SUPPORT_FORK_FLOW_AND_RESOURCE_CUTS.md)
already solves general maximum routing. The contribution here is an exact
contraction of donor trees, a proof that one bridge per repaired tree suffices
even when competing physical packings use more, and retention of **all old
used original interval IDs at the same globally minimum actual bridge fee**.
This is a structural compensation theorem, not a new general flow algorithm.

A fully frozen mixed-direction board demonstrates the strict extension:
the receiver's entire suffix support is shared with another old request, so
the preceding private-witness rule rejects it. A single capacity-one P-free
pivot gives payment 2 to 3 while preserving two shared units that were both
already used in the supplied maximum baseline. No suffix unit is credited
as fresh; the one fresh unit is identified on the receiver prefix.

## 1. Model, requests and hypotheses

Use the fixed final actual-owner model and original unit pool Q from
[old-link batch repair](OLD_LINK_BATCH_REPAIR.md). Each original unit has
at most two original owner users. Unsupported original units remain in Q.
Supports can have undergone arbitrary destructive mixed-direction pivots.

Let P0 be an owner-disjoint normalized reference skeleton with p source labels,
old links E0, and g additional eligible alpha sources N outside its owner set.
Append each a in N as a singleton ordinary routing skeleton, not an asserted
old payment. A singleton with empty support can donate a bridge.

There is one request per ordinary interval stem, beta fork and appended source.
Each request sees its owners' union of final original supports. Beta singletons
have no request. Every beta singleton/fork supplies one whole-beta baseline;
let B be their number and D the number of requests, so B+D=p+g.
Original units induce full edges between two request users or private half-edges
at one. A deficient component is a tree with no private unit, including an
empty isolated request. Let these trees be T, with n_T requests each, and let
t0 be their number. All other request vertices form R, with r=|R|. The exact
old-link optimum is

    V0 = B+D-t0 = C+r,
    C = B + sum_T (n_T-1).

Candidate e is an actual new TP-to-BP link from an owner of an ordinary donor
stem A_e to a mixed owner of an ordinary receiver stem C_e. The stems are
distinct and neither contains beta. Candidate pairs are disjoint: no reference
stem is a donor or receiver of two candidates. Other old beta/fork primitives
are allowed. Require:

1. A_e's request lies in some deficient tree T(e).
2. C_e's request lies in R, a nondeficient reference component.

There is **no privacy, positive-surplus-per-receiver, or individual-bridge-gain
hypothesis**. Receivers may share any original units and belong to the same
nondeficient component; many different donor requests may belong to one T.
At each receiver preserve the actual owner order. Let P_e be the union of
supports on its strict prefix before the mixed entrance, and S_e the union
at/after the entrance. Either can be empty. They may overlap, with the overlap
still consisting of the same original unit IDs.

Only the p+g declared sources, E0, and the candidates are permitted. Assign
each candidate a nonnegative integer actual fee w_e. No minimum total old
plus new link count is asserted.

## 2. One receiver-slot network

Construct the following unit-capacity network. There is one vertex q_j for
each original unit incident with R; other original units remain in the pool
and are handled in their donor tree or remain unsupported.

- Source s has an arc of capacity one to each q_j.
- Each candidate receiver C_e has two slots, pre_e and post_e. Add q_j to
  pre_e for j in P_e, q_j to post_e for j in S_e, and a capacity-one arc
  from each slot to the receiver's aggregation vertex c_e.
- Every other request in R has one whole-support slot, with analogous access
  and aggregation arcs.
- Every request aggregation vertex has one baseline arc to sink t.
- Receiver c_e additionally has an arc to a vertex z_T(e), of capacity one
  and cost w_e. Each distinct donor-tree vertex z_T has one arc to t.
- All other costs are zero. Every listed arc has capacity one.

Thus a receiver can take at most one unit from each side. Its second unit
uses the actual bridge-fee arc. All candidate receivers for one donor tree
share a single extra-payment outlet. Every original unit enters through one
source arc even if supported by several slots.

Let F be maximum flow value and W its minimum cost. Since R is nondeficient,
its old maximum request allocation supplies a zero-cost r-unit baseline flow.
Write mu=F-r>=0.

**Theorem.** Over all legal normalized physical packings using E0 and the
candidates, including those using several bridges from one donor tree, the
exact maximum payment and minimum actual bridge fee at that value are

    V = C+F = p+g-t0+mu,      minimum fee = W.

There is a packing attaining both with exactly mu actual new bridges, which
is also the minimum possible number of new bridges. For **any** maximum old
request allocation M0 in the final pool and its standard old stem/fork lift,
such a minimum-fee packing can preserve every old paid source and every old
used original unit, adding exactly mu distinct previously unused units.
It need not preserve assignments or individual old links. Retention is scoped
to this final-pool baseline, as in the private theorem, not arbitrary earlier
supports or an unnormalized two-interval beta packing.

## 3. Lower bound, exact fees and original-unit retention

Initialize the network with M0's assignments on R. For a candidate receiver,
choose a side supporting its old assigned unit; send that unit through the
side slot and baseline arc. Other R requests use their whole slots. Every
baseline arc is saturated, every used original unit's source arc is saturated,
and the cost is zero. This flow is minimum-cost at value r because all
original costs are nonnegative.

Run successive shortest augmenting source-to-sink paths in this **one fixed
residual graph**, with reverse arcs and costs. No simple augmenting path can
return to s or depart from t. It therefore cannot reverse an old saturated
source-to-unit arc or an old saturated baseline-to-t arc. Every old used R
unit and every R baseline remains present throughout, even when an augmentation
reverses an earlier bridge choice and its fee. Standard min-cost flow
optimality gives maximum value F and minimum cost W. The checker additionally
verifies a maximum-flow cut and global residual potentials with nonnegative
reduced costs on every residual arc, including source/sink incident arcs.

At the end each receiver has its baseline plus either zero or one extra.
A receiver with an extra has both side slots matched to different original
units. The z_T outlet ensures at most one such receiver per donor tree.
For its actual candidate e, reroot T at A_e: every other request uses its
parent-edge unit and A_e gets no tree unit. A deficient n_T-vertex tree has
exactly n_T-1 original units, all used in every maximum old allocation, so
rerooting keeps that entire old unit set.

Give the old receiver source the pre unit, truncating strictly before the
entrance. Give the donor source its own prefix, e, and the receiver suffix,
ending at a supporter of the post unit. Other receivers use their one slot
anywhere along their old stem; other requests retain their standard lift.
The donor prefix cannot itself support the assigned post unit: its units
belong to a deficient component, disjoint from all units incident with R.
Consequently the assigned post route actually traverses e.

The disjoint candidate pairs keep physical owners disjoint. The network keeps
resource IDs disjoint. Rerooted tree units are disjoint from all R units.
Each selected tree pays all its requests and each unselected tree keeps M0,
so every previously paid source is retained, including fork baseline choices.
The construction pays C+F with actual fee W and F-r=mu actual bridges. It
uses every old unit, plus exactly F-r new R units. This proves the lower bound,
identity retention and the claimed actual fee for the constructed packing.

## 4. Upper bound against arbitrary multi-bridge packings

It remains to prove that the tree-outlet capacity one does not exclude a
better physical packing. Take any legal packing on E0 plus the candidates.
Normalize its beta singleton/fork parts to one whole-beta baseline and at
most one interval per fork, preserving value and deleting links only. This
step is used for the upper bound; it is not an identity-retention operation.

For a deficient tree T let k_T be its actually used outgoing bridges and
i_T its internally paid request count, counting a fork's second payment
above its whole-beta baseline as one request. Candidate donors are ordinary
and distinct. Their routes that actually use a bridge terminate in a receiver
suffix, so they cannot also use a unit inside T. Thus

    i_T <= n_T-1,       i_T+k_T <= n_T.                 (1)

All paths terminating in R can be represented by receiver slots. If a receiver
pays both its own source and the incoming donor, its own path must stop in
the strict prefix: otherwise both paths occupy the same mixed entrance.
Such a receiver fills pre and post. If only one source is paid, put its
actual resource in the appropriate side slot and send it through the baseline
outlet; this applies also when only the donor was paid. Noncandidate R
requests fill at most their one slot. The packing's distinct original units
give a legal resource-to-slot assignment.

Let H be the total occupied R slots, including paths of outgoing donor sources.
Let h_T count doubly occupied candidate receivers associated with T, so h_T<=k_T.
Route one occupied slot at every occupied request through its baseline. For
each T retain at most one of its h_T extras; delete h_T-1 extras when h_T>0,
with their slot paths. This gives a feasible network flow of value

    f = H - sum_T max(h_T-1,0),

whose fee is at most the original actual fee: the remaining charged bridges
are a subset of actually used bridges, and their fees are nonnegative. By (1),
for every T,

    i_T + max(h_T-1,0) <= n_T-1.                       (2)

For k_T=0 this is the first inequality in (1). For k_T>=1 it follows from
h_T<=k_T and i_T+k_T<=n_T. Therefore the original physical payment P obeys

    P <= B + sum_T i_T + H
      <= B + sum_T(n_T-1) + f
       = C+f <= C+F.

If P=C+F is maximum, all these inequalities force f=F. The projection then
provides a maximum network flow of cost no greater than that physical packing.
Consequently W is a lower bound for every maximum packing's actual bridge fee.
The lower construction attains W, proving exactness against **all** permitted
packings, rather than only a rooted repair convention.

Finally f<=r+number_of_actual_bridges, so a gain mu requires at least mu new
bridges. The construction attains that bound at the optimum fee. ∎

The inequality (2) is where multiple bridges from one donor tree are accounted
for. Their extra receiving demands can use multiple units, but each bridge
beyond the first displaces another internally payable donor request. The
network contracts this exchange without inventing a second tree deficit.

## 5. Joint Hall condition, cut ledger and relation to private witnesses

For a fixed chosen set S with at most one candidate per donor tree, split
each selected receiver into pre and post requests and keep every other R
request whole. Joint completion is feasible exactly when this slot-resource
bipartite graph has a matching covering all its requests, equivalently

    |union_(slot in X) support(slot)| >= |X| for every slot subset X.

This is a **global original-resource union**, never a sum of individual reserve
counts. Candidate-side selection and the donor-tree restriction are optimized
by the single network above, rather than enumeration of S. The maximum-flow
minimum-cut condition for repairing all old deficient trees is that every
s-to-t cut have capacity at least r+t0. An unrepresented tree has no outlet,
so the condition automatically fails when such a tree remains.

In general the exact residual payment defect is

    t0-mu = t0+r-mincut_capacity.

This is an obstruction for the declared old-plus-candidate link set. Other
physical links can repair it; it need not be an obstruction to the full
original routing network or the target grid inequality.

Two request-private pre/post witnesses at each receiver ensure that one
candidate per distinct donor tree can always be used. Hence mu equals the
number d of represented trees, and the previous independent per-tree cheapest
fee formula follows. Without privacy, mu can be smaller and the optimal fee
can require reversing a cheaper earlier bridge. Independent per-tree greedy
choices are no longer justified.

## 6. Frozen mixed-direction instance beyond the private rule

The [reconstructible fixture](../develop/fixtures/frozen_shared_prefix_bridge.json)
uses the existing 28 by 24 board with |T|=49, |M|=154 and 308 frozen endpoints.
Start with all tiles H and change only the P-free tile with corner (14,14)
to V. It contains selected cell (15,14), so its capacity is **one**. The
selection and actual matching are unchanged. Coordinates below refer to
the final whole-owner model.

The reference stems and the new candidate are:

| Role | Actual original source and mixed owner | Actual link |
| --- | --- | --- |
| Receiver | bottom alpha 20 to mixed 14 | (24,17) to (24,18) |
| Other old request | left alpha 6 to mixed 17 | (24,4) to (24,5) |
| New donor | right alpha 12, empty direct support | (24,19) to (24,18) |

The receiver suffix consists of mixed 14. Its **entire** support is

    u = {(18,13),(19,13)},   v = {(18,14),(19,14)}.

Both units' complete original-owner user sets are {14,17}. Thus their request
users are the receiver and the other left request: neither is private to the
receiver, and no private suffix witness exists. A third original unit

    w = {(24,7),(25,7)}

has owner users {20,22}; owner 22 is outside the declared skeleton, so w is
available to the receiver prefix.

Supply a maximum baseline that already uses **both** shared units: bottom's
old receiver stem uses u and left's old stem uses v. The donor is unpaid.
After repair, bottom alpha 20 stops directly at w, left keeps its actual
old link to mixed 17 and unit v, and right alpha 12 traverses the new bridge
to mixed 14 and uses u. Payment rises from 2 to 3; both old used units and
both old paid sources remain. The fresh credit is w, not either shared suffix
unit. Only one new bridge is charged.

Translate the construction by (30i,0), 0<=i<q, with two blank separator rows.
For every q>=1, the original freezing schedule remains valid in each copy;
no declared owner/link connects copies, and separator units have no declared
request users. The explicit construction and source-count upper bound prove

    old payment 2q, new payment 3q,
    2q old shared unit IDs retained, q fresh units, q new bridges.

The board is (30q-2) by 24, L=155q-24 and S=157q-24>0. This is a positive
compensation example on three declared sources per copy, not a counterexample
to the numerical grid inequality or a statement that all original sources
are covered by these particular links. The q=16 production check gives
32 to 48, 32 retained shared units and minimum bridge fee 31 for
w_i=1+(i mod 3), while mode enumeration and full optimizers are disabled.

## 7. Counting consequence, validation and formal scope

If all original alphas are declared, the resulting packing proves

    L+beta >= alpha-t0+mu,
    |T|+|M| <= area/2+t0-mu.

Thus full donor-tree repair certifies the coefficient-one bound on this
class, now without a private-reserve hypothesis. Existence of sufficient
geometric slots for arbitrary residual mixed-direction configurations remains
unproved. Shared-stem candidates and deficient receiving components are not
covered. The universal 5/6 bound has not been improved.

The [solver and independent checker](../develop/check_shared_prefix_bridge_flow.py)
and its [saved report](../output/shared-prefix-bridge-flow-validation.json) record:

- 300 exact value/actual-fee comparisons with independent 2^k mode enumeration,
  including 295 accepted seeded shared-support models;
- 50 independent primitive-packing and full-routing value comparisons;
- 454 checks over all maximum baseline allocations in selected controls;
- a shared-one-suffix example in which two separately successful bridges give
  only one joint gain, with fee 2 rather than 5;
- a case where the first free bridge is reversed to attain two gains: final
  selected fees 2 and 1, total 3;
- a discarded donor suffix whose old unit is retained by rerooting, and a
  beta fork in the deficient donor tree;
- maximum-flow cuts and global residual min-cost potential certificates;
- frozen q=1,2,4,16 with 7,084 strict freezing events; independent restricted
  routing comparisons for q=1,2,4, and a production q=16 guard against mode,
  primitive and full-flow optimization.

Finite enumeration is used to audit these examples and implementations. The
general contraction, identity retention, fee theorem and all-q construction
are established by the preceding proofs.

The [Lean source](../formal/SubQuorum/SharedPrefixBridgeFlow.lean) proves two
scoped general facts: inequality (2), and exclusion of reverse boundary arcs
on a path that never returns to source or departs sink. The arithmetic theorem
depends only on Lean's standard propext and Quot.sound; the boundary theorem
has no axiom dependencies. The [formal report](../output/shared-prefix-bridge-formal-validation.json)
records Lean 4.33.0, no sorry, native_decide, added axioms or warnings, and local
memory/process preflight before each executable invocation. Flow construction,
general min-cost optimality, geometry and complete routing equivalence remain
written proofs with executable checks, not end-to-end Lean.

```sh
PYTHONDONTWRITEBYTECODE=1 python3 develop/check_shared_prefix_bridge_flow.py \
  --output output/shared-prefix-bridge-flow-validation.json
PYTHONDONTWRITEBYTECODE=1 python3 develop/check_shared_prefix_bridge_formal.py \
  --lean /path/to/lean-4.33.0 \
  --output output/shared-prefix-bridge-formal-validation.json
```
