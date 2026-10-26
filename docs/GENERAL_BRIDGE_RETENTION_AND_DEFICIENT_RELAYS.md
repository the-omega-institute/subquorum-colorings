# General mixed-head repair: retained original units and deficient-tree relays

26 October 2026. Wenlin Zhang and Haobo Ma. Independent research continuation.

We remove the disjoint-stem-pair, deficient-donor and nondeficient-receiver
restrictions of the [shared receiver-slot theorem](SHARED_PREFIX_BRIDGE_FLOW.md).
The new condition is that every beta reachable by the permitted links already
has its whole-beta credit used in the initial normalized packing. **Every
collection of mixed-head additions to an old normalized stem/fork skeleton
satisfies this condition**, including arbitrary shared stems, bent routes,
links between deficient components and new mixed owners outside that skeleton.

The [existing full fork network](WHOLE_SUPPORT_FORK_FLOW_AND_RESOURCE_CUTS.md)
already computes maximum payment. Here reversing its orientation and initializing
it with the old packing proves a stronger retention result: at maximum payment,
globally minimum actual new-link fee, and then minimum new-link count, one can
keep every old paid source, every old used original interval ID, and every old
whole-beta credit. The beta condition makes the resulting flow already normalized;
no old interval is silently replaced by a newly used beta credit.

We also give a precise obstruction to extending the previous contraction by
keeping a single outgoing bridge per deficient tree. A deficient tree can be
a **relay**, with two necessary outgoing bridges and one necessary incoming
bridge. The correct conserved quantity is outgoing minus incoming, not outgoing
alone. This is an abstract two-owner model, not a claimed frozen realization.
A separate fully frozen grid realizes shared-stem synergy: either of two new
bridges alone leaves payment 3, whereas both give 4 and retain all three old units.

## 1. Fixed model, initial packing and the beta guard

Fix the actual original alpha, mixed and beta owners, their physical TP/BP
tips, actual permitted links and whole-owner original supports W(o) in Q.
Every original resource ID remains in Q, including unsupported units. Distinct
interval units and private whole-beta credits are different resource types.
The original two-owner incidence bound is used for request-tree applications;
the reversed-flow argument itself only needs the physical capacity model.

Let E0 be the links of an owner-disjoint normalized reference stem/fork
skeleton, hence a directed forest of stems and beta joins. Let U be the
declared alpha sources, including eligible additional singleton sources.
Let P be a feasible normalized old packing using E0, paying p0 sources,
with original interval set I0 and used whole-beta set B0. In the application
we take P to be the standard lift of **any** maximum old request allocation
in the final resource pool. Thus

    p0 = |I0|+|B0| = |U|-t0,

where t0 is the deficient old request-tree count. This baseline is after
any destructive direction change; we do not assert retention of supports
that disappeared before this final state.

Add any set E+ of actual links, disjoint from E0, with nonnegative integer
fees w(e). All original mixed owners may be used, including outside the
reference skeleton. Candidate links can share stems and can enter deficient
request components. Sources outside U are not payable.

**Beta saturation guard.** Every beta reachable from U along E0 union E+
belongs to B0. Reachability ignores capacities but respects link directions
and stops at beta. It is a polynomial graph test. A failed guard returns an
actual U-to-beta link path. This is a certificate that this theorem's
hypothesis fails, not an infeasibility or counting counterexample.

**Mixed-head corollary.** If every new link has a mixed head, the guard holds
for the standard old request lift. Indeed any link entering beta must be
in E0, so that beta is already the terminus of a reference beta singleton
or fork. The old lift retains its whole-beta baseline irrespective of the
new interval allocation. New links into a beta already in B0 are also allowed.
Newly reachable betas outside B0 remain outside this result's retention claim.

## 2. Resource-first network and exact theorem

Reverse the alpha-to-payment network while retaining actual physical port
capacities. Its new source s supplies payments and its sink t collects sources:

- For every original unit j, add s to unit(j), capacity one. For every beta b,
  add s to body(b), capacity one, representing its private whole-beta credit.
- For j in W(o), add unit(j) to the original owner's output vertex.
- A mixed owner has an output-to-input gate of capacity one.
- A beta body has one capacity-one arc to each of its two actual BP tips.
- Reverse each permitted actual link: its head's mixed input or beta BP tip
  goes to its tail owner's output, with capacity one.
- Each declared alpha has one capacity-one output-to-t arc.

All listed arcs have unit capacity. An alpha has no BP, a mixed owner has
one BP/TP pair, and a beta has no TP; these are the actual owner types.
Original units shared by several supports still have just one source arc.

Let m=|E+|. Charge a new link cost

    c(e) = (m+1) w(e)+1,

and every old link and other arc cost zero. Since at most m actual new links
can be used, minimum encoded cost means first minimum actual fee, then minimum
number of new links. It does not minimize the total number of old plus new links.

**Theorem.** Under the beta saturation guard, one initialized min-cost maximum
flow computes exactly, over all normalized packings using E0 union E+:

1. maximum payment F;
2. minimum actual new-link fee at F;
3. minimum number of new links among those fee-optimal maximum packings.

It can attain all three while preserving every source paid by P, every unit
of I0, and every private beta credit of B0. It adds exactly F-p0 different
previously unused original interval units. Individual assignments and old
links may change. The construction uses no primitive-packing or bridge-mode
enumeration. Shared stems and deficient receivers need no further guard.

## 3. General proof, including normalization without identity loss

**Initialize.** Reverse each actual path of P. A beta fork gives two paths
entering its two distinct BP tips in the original direction: one ends at
its whole-beta credit and the other at its original interval. Its reversed
paths start with these two different resources. Mixed gates, BP ports, resource
arcs and declared alpha sink arcs all satisfy unit capacities. The initial
flow has value p0 and cost zero, so it is globally minimum-cost at that value.

**Augment and retain.** Successive shortest residual s-to-t paths give the
minimum cost at each successive value, until maximum F. A simple such path
cannot return to s or leave t. Therefore it cannot reverse any already saturated
old resource source arc, or any already saturated paid-alpha sink arc. The old
original interval IDs, old private-beta outputs and paid-source labels are
retained throughout. Internal reverse links may change assignments or cancel
previous fee choices. This is the same general boundary-arc principle isolated
in the [earlier Lean kernel](../formal/SubQuorum/SharedPrefixBridgeFlow.lean).

The solver independently verifies a maximum-flow cut and global residual
potentials with nonnegative reduced costs on **every** residual arc, including
arcs entering s or leaving t. Thus both cardinality and encoded-cost optimality
have exact certificates, beyond the augmentation history.

**Extract paths.** Every forward cycle contains a new link, since E0 is a
directed stem/fork forest. Such a cycle has positive encoded cost, even when
its monetary fees are zero, and cannot occur in a minimum-cost flow. The
integral flow therefore decomposes into actual payment-to-alpha paths, with
no residual circulation. A path can contain at most one beta, at its resource
end, since beta has no TP in the original direction.

An unused beta outside B0 cannot occur in a path: reversing such a path would
make it reachable from U, contradicting the guard. Every beta in B0 retains
its saturated private-credit source arc. Its two actual BP port arcs permit
at most two paths, of which exactly one starts with that private credit.
There is consequently at most **one** interval path at that beta. It already
forms a standard beta singleton or beta fork. No interval has to be exchanged
for a beta credit during extraction, including when the interval was old.
Non-beta paths become ordinary interval stems. Mixed capacity and BP ports
give precisely the required owner/entry disjointness.

Thus the extracted packing has value F and encoded cost equal to the flow.
Its whole-beta set is exactly B0. It uses F-|B0| original interval units,
containing I0, so the number of fresh distinct units is

    F-|B0|-|I0| = F-p0.

**Global optimality.** Conversely every permitted normalized packing defines
an integral reversed flow of the same payment, actual fee and new-link count.
Hence no such packing exceeds F or improves on its minimum encoded cost.
The extracted, identity-preserving packing attains that global optimum. The
scaling formula proves the stated fee/count ordering. ∎

The general mathematical mechanism is reversal and initialization of the
established physical fork flow, together with a beta guard that closes its
normalization gap. We do not claim a new general min-cost flow algorithm.
All original inventory and source labels remain identifiable throughout.

## 4. A deficient tree is a relay: an explicit contraction obstruction

The [canonical fixture](../develop/fixtures/deficient_tree_relay_junction.json)
has six alpha owners A,B,C,D,E,F and three mixed owners X,Y,Z. Old stems are

    B->X,   C,   D,   E->Y,   F->Z,

and A is an additional empty singleton request. Original supports are exactly:

| Original unit | Original owner users |
| --- | --- |
| u | B, C |
| v | X, D |
| a | E |
| b | Y |
| c | F |
| d | Z |

Every unit has at most two original owner users. The request tree
T={B->X,C,D} has three requests, two edge units u,v and no private unit.
The singleton {A} is the other deficient tree. E->Y and F->Z each have two
private units and are nondeficient. Old payment is four: C uses u, D uses v,
E uses a and F uses c. Both deficient requests' roots are unpaid.

Declare exactly these three actual canonical TP-to-BP new links:

    A->X,   C->Y,   D->Z.

Their pairs of reference stems are disjoint. All six sources are paid by

    B: u directly,    A->X: v,
    E: a directly,    C->Y: b,
    F: c directly,    D->Z: d.

All old paid sources and old units u,v,a,c are retained; b,d are the two
fresh units. Every new bridge is necessary for payment six. A has no other
exit. If A->X is used, B must stop before X and use u; therefore C must leave
through C->Y. Since A uses v, D must leave through D->Z. Deleting any one
candidate leaves exact maximum five, as seen by omitting the corresponding
source and using the other two distinct payments. Unit fees give exact fee
three and three new links for gain two.

The receiver of A->X lies in a **deficient** tree T, which must simultaneously
use **two outgoing bridges and one incoming bridge**. Any proposed extension
that simply removes the nondeficient-receiver guard but retains at most one
outgoing bridge per old tree cannot attain the actual optimum. The preceding
guarded theorem remains valid on its stated class. This counterexample rejects
that proposed contraction rule, not full routing or the target grid inequality.
The fixture is an abstract canonical owner model; a frozen grid realization
of this particular junction is not asserted.

### Correct component accounting

For a closed old deficient tree with n requests and B_T whole-beta baselines,
there are n-1 original edge units and n+B_T original sources. Assume its original
unit users among all allowed owners stay in this region, its used original
units and beta credits are retained, and every one of its sources is paid.
Ordinary flow conservation gives

    paid sources + incoming physical routes
      = original interval payments + beta payments + outgoing physical routes.

Consequently

    outgoing - incoming = (n+B_T)-(n-1+B_T) = 1.

If one old unpaid source remains, the same difference is zero. The equation
does not bound outgoing itself. In the example it is 2-1=1. The closure
condition matters: an original unit supported by a newly admitted outside
owner can create a crossing access arc, which must also appear in the cut
ledger rather than being counted as a physical bridge alone.

## 5. One gain can require arbitrarily many actual new links

For any r>=1 take sources A0,...,Ar and mixed owners X0,...,X(r-1),Y. Old
reference stem Ai->X(i-1) exists for 1<=i<=r. Unit ui is supported exactly by
Ai and X(i-1). A0 has empty direct support. Y supports one other unit v and
has no old incoming link. The old maximum pays Ai directly with ui for every
i>=1, so p0=r and all r old unit IDs are used.

Add exactly

    Ai->Xi for 0<=i<r,       Ar->Y.

These candidate bridges share old stems along the chain. Full payment is
achieved by Ai->Xi using u(i+1), 0<=i<r, and Ar->Y using v. All r old paid
sources and r old units are kept, with just one fresh original unit.

All r+1 added links are necessary. A0 must take A0->X0 and consume u1.
Inductively Ai cannot use ui, already consumed by A(i-1), and cannot enter
X(i-1), already occupied. It must use Ai->Xi, or Ar->Y at the end. Deleting
any new link makes full payment impossible while the old r payments remain
feasible. Thus the exact gain is one and the minimum actual new-link count
is r+1, with unit fee r+1. Every old assignment changes.

This differs from the earlier
[protected-chain result](PROTECTED_CHAIN_REASSIGNMENT.md), which showed
unbounded reassignment with a bounded repair-link budget on a frozen family.
Here the **minimum new-link budget itself** is unbounded for one gain, on a
different abstract family. No arbitrary-r frozen realization is claimed.
The r=64 production check retains 64 old units, adds one fresh unit, pays
64 to 65 and uses exactly 65 new links without primitive or mode optimization.

## 6. Actual frozen shared-stem synergy

Use the existing all-H 28 by 24 board, with |T|=49, |M|=154 and all 308 actual
endpoints strictly frozen. No pivot is made. The
[reconstruction fixture](../develop/fixtures/frozen_shared_stem_bridge_synergy.json)
declares these reference old stems and old original units:

| Old stem | Actual old link | Used original unit, as two cells |
| --- | --- | --- |
| top alpha 8 to mixed 11 | (5,17) to (5,18) | {(10,10),(11,10)} |
| left alpha 6 to mixed 7 | (5,4) to (5,5) | {(14,6),(15,6)} |
| bottom alpha 20 to mixed 14 | (24,17) to (24,18) | {(14,13),(15,13)} |

The new empty-support source is right alpha 12. Add

    e1=(5,19)->(5,18),  fee 2, from right 12 into mixed 11;
    e2=(5,6)->(5,5),    fee 3, from top 8 into mixed 7.

The old top stem is both receiver of e1 and donor of e2, so the candidate
pairs overlap in that stem. Its old interval request is nondeficient, so it
is also outside the previous deficient-donor hypothesis.

With e1 alone, right 12 and top 8 both need mixed 11, giving at most three
total payments. With e2 alone, right 12 has no permitted route or direct
unit, again at most three. Both together pay all four sources. One actual
certificate is:

- right 12 uses e1, mixed 11, and the old unit {(10,10),(11,10)};
- top 8 uses e2, mixed 7, and the fresh unit {(10,12),(11,12)};
- left 6 stops directly at its old unit {(14,6),(15,6)};
- bottom 20 keeps its old route and old unit {(14,13),(15,13)}.

Each original unit and actual owner is used legally and once, apart from the
explicit beta fork allowance, which is not needed in this instance. All three
old used IDs survive. Thus gain is one, minimum new links is two and minimum
actual fee is five. The new credit is the one identified fresh original unit,
not a second copy of either old mixed-path reserve.

For arbitrary q>=1 translate by (30i,0) and keep two blank separator rows.
No declared owner/link crosses copies, and separator units have no declared
support user. The strict original freezing schedule remains valid. The same
explicit four-payment construction and per-copy single-bridge obstructions
prove, for every q,

    3q -> 4q,  3q old unit IDs retained, q fresh units,
    minimum actual new links 2q, minimum fee 5q.

The board is (30q-2) by 24, with original L=155q-24 and S=157q-24>0. This
positive example is not a grid-inequality counterexample. For q=16 the production
solver gives 48 to 64, 48 retained old units, 16 fresh units, 32 new links and
fee 80, with independent optimizers disabled.

## 7. Counting consequence and remaining boundary

For all original alphas declared, let mu=F-p0. The original ledger and the
constructed packing give

    L+beta >= F = alpha-t0+mu,
    |T|+|M| <= area/2+t0-mu.

The exact remaining declared-link defect is alpha-F, certified by a cut in
the resource-first network. When mu=t0, this proves the coefficient-one
inequality on this class, now allowing arbitrary mixed-head interactions.
What remains is a geometric lower bound on the relevant cut capacities,
including occupied-band/bent-path configurations, and an identity-safe
normalization argument when genuinely new beta credits become reachable.
The current guard's failure is not a counterexample to such an argument.
No universal improvement of the existing 5/6 bound has been proved.

## 8. Verification and formal scope

The [solver and independent checker](../develop/check_general_bridge_retention.py)
and [saved report](../output/general-bridge-retention-validation.json) include:

- 330 independent normalized primitive-DP comparisons of maximum payment,
  minimum actual fee and minimum new-link count, and 330 additional comparisons
  requiring all old paid-source labels and original used interval IDs;
- 108 old whole-beta models, eight old fork reference models, a safe new
  beta-head example, and a residual augmentation reversing an earlier link;
- 43 checks of all maximum old allocations in selected controls;
- 214 newly reachable beta guard rejections, each with an actual link path;
- all three junction bridges individually necessary, and 35 bridge-deletion
  checks across r=1,...,7 transport chains;
- a guarded r=64 production transport run, plus frozen q=1,2,4,16 with 7,084
  strict freezing events, independent restricted full-flow comparisons for
  q=1,2,4, an identity-prescribed primitive check at q=1, and q=16 production
  without primitive enumeration or the existing full optimizer;
- exact max-flow cuts and global residual reduced-cost certificates.

Finite enumeration checks implementations and discovers examples. The general
retention theorem, relay obstruction, unbounded transport and all-q frozen
extension have the preceding proofs for all sizes.

The [Lean source](../formal/SubQuorum/GeneralBridgeRetention.lean) proves three
scoped general facts: saturated private-beta credit leaves at most one interval;
the closed fully repaired tree's outgoing-minus-incoming identity; and integer
fee dominance over actual new-link count. The
[formal report](../output/general-bridge-retention-formal-validation.json)
records Lean 4.33.0, standard propext/Classical.choice/Quot.sound dependencies
only, no sorry/native_decide/added axiom/warnings, and local memory plus actual
comm-basename process checks before each Lean executable invocation. Complete
flow/routing equivalence and physical geometry have written proofs and executable
checks; no end-to-end Lean claim is made.

```sh
PYTHONDONTWRITEBYTECODE=1 python3 develop/check_general_bridge_retention.py \
  --output output/general-bridge-retention-validation.json
PYTHONDONTWRITEBYTECODE=1 python3 develop/check_general_bridge_formal.py \
  --lean /path/to/lean-4.33.0 \
  --output output/general-bridge-retention-formal-validation.json
```
