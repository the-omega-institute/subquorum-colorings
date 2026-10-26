# Actual new links: an exact bridge repair theorem and a frozen entrance obstruction

26 October 2026. Wenlin Zhang and Haobo Ma. Independent research continuation.

We resolve a specific remaining cross-component question: can one actual new
link repair a deficient old routing component merely because the receiving
component has unused original intervals? **No.** An explicit completely frozen
board has five receiving intervals, only one old receiving payment, and an
actual incoming link, yet that link adds no payment. A different actual link
on the same board, after the same capacity-one direction change and with the
same three-source old packing, does repair the loss.

The distinction is where the incoming link enters an old mixed stem. We give
an exact two-mode theorem retaining this order information, and extend it to
pairwise disjoint pairs of stems. All modes use the same actual resource pool;
one reserve is never credited independently to several added links. This is
a structural extension of [old-link batch repair](OLD_LINK_BATCH_REPAIR.md),
using its established two-owner allocation theorem, not a new abstract
matching theorem. It does not improve the universal 5/6 bound.

## 1. Fixed state, old packing and permitted new links

Fix the final whole-owner compensation model: original alpha/mixed/beta bodies,
actual TP-to-BP links, private whole-beta outputs, and original interval pool Q.
Each unit in Q supports at most two distinct original owners. Units having no
usable incidence remain in Q. The model may result from arbitrary P-free
direction changes, including destructive mixed-target changes. No support
monotonicity assumption is made.

Let P0 be an owner-disjoint old normalized packing with p paid alpha sources
and selected old links E0. Let N be g additional eligible alpha sources outside
that packing. They have no E0 edges and may pay directly. Only sources in
U=paid(P0) union N may be paid. Other original owners/resources stay in the
model, but unavailable links are not silently allowed.

Choose two distinct ordinary interval stems of P0, ordered by their actual
directed links:

    A: a_0 -> ... -> a_r,       B: b_0 -> ... -> b_s.

Here a_0,b_0 are alpha sources and later owners are mixed; neither stem
contains a beta. All other disjoint old beta/fork primitives are permitted.
Take a declared actual link e from a TP of a_i to the BP of b_j, with j>=1,
and e not in E0. In particular the head is an actual capacity-one mixed owner.
The optimization permits precisely E0 union {e}, with arbitrary truncation,
resource reassignment and legal whole-support normalization. It does not
require retaining every old selected link or old resource assignment.

## 2. The two structural modes

Mode 0 is the old skeleton. Mode 1 replaces A and B by

    A_e: a_0 -> ... -> a_i --e--> b_j -> ... -> b_s;
    B_e: b_0 -> ... -> b_(j-1).

The edge into b_j from its old predecessor is omitted. The old A suffix after
a_i is omitted. B_e is nonempty, possibly just b_0. The replacement stems have
disjoint owner sets and the same two alpha sources. Other primitives are
unchanged.

For each mode, make requests and baseline exactly as in old-link repair:
one request per ordinary stem, one per old beta fork, one per N source, and
one guaranteed whole-beta baseline payment per old beta singleton/fork.
Each request sees the union of the **final** supports of its own stem/primitive
owners, deduplicating original unit IDs. Call the two deficient-tree counts
t_0,t_e. Their baseline B and request count D are equal, with B+D=p+g.

Mode 1 is a routing skeleton, not an assertion that its new endpoints already
have old interval witnesses. The allocation proof in the old-link theorem
uses only the disjoint directed stems, actual fork arms, and new supports.
It therefore applies verbatim: a matched request truncates to a supporting
owner, and an unmatched request is omitted (or keeps its fork baseline).
No fictitious endpoint interval enters Q.

**Theorem 1 (exact single-link compensation).** The exact maximum is

    V_(E0+e) = p+g-min(t_0,t_e).

In particular its gain over the old-link optimum p+g-t_0 is either zero or
one, and is one exactly when t_e=t_0-1.

For prescribed R subset U, mark requests mandatory by the old theorem:
an ordinary/new source in R is mandatory; an old fork request is mandatory
only if both its sources lie in R. R is feasible if and only if **at least one
mode** has a nonmandatory request in every deficient tree. Among its feasible
modes, the maximum retained payment is p+g minus the smallest tree count.
If both modes fail, one all-mandatory deficient tree per mode is a complete
two-mode obstruction certificate.

**Proof, coverage.** A normalized packing not using e uses only E0, hence
belongs to Mode 0. If it uses e, its route starts at a_0: no other source
can reach A in E0, whose different primitives have disjoint owners and links.
It follows the A prefix to a_i, crosses e, then follows the B suffix until
its resource witness. The source b_0, if paid, must end strictly before b_j.
Indeed its only E0 route to or beyond b_j would use that same capacity-one
mixed owner, already occupied by a_0's route. No source can use the discarded
A suffix. Thus every route lies in Mode 1 or an unchanged primitive.

Conversely every truncated Mode 1 packing uses actual links in E0 union {e};
the replacement owner sets are disjoint, so it is physically legal whenever
its resource allocation is injective. Mode 0 is legal as well. The exact
allocation theorem gives p+g-t in each mode, proves the formula and transfers
the mandatory-root prescription criterion. Finally, deleting the single
route using e from any improved pack leaves a legal E0 pack, losing only
one payment. Therefore the gain cannot exceed one. ∎

## 3. Several bridges: a joint ledger and exact activation fees

Choose k bridges as above whose **pairs of old stems are pairwise disjoint**.
No old stem may be a donor or receiver in two pairs. Other owner-disjoint old
primitives and N remain allowed. This hypothesis makes the structural switches
independent; their interval resources are explicitly NOT assumed independent.
Give each named bridge a nonnegative integer fee w_i.

For sigma subset {1,...,k}, switch precisely its pairs, keep the other pairs
in Mode 0, and compute the one global resource graph. Let t_sigma be its
deficient-tree count. For prescriptions, consider only modes passing their
mandatory-root test.

**Theorem 2 (joint repair and actual bridge fees).** Without prescriptions,

    V = p+g-min_sigma t_sigma.

With prescriptions the same formula minimizes only over feasible modes; if
none passes, the prescription is infeasible. At this maximum V, minimum
actual fee of added bridges is exactly

    min { sum_(i in sigma) w_i : sigma feasible,
                                  p+g-t_sigma=V }.

For unit fees this gives the minimum number of newly used bridges. The
algorithm uses 2^k resource-graph allocations and polynomial work per mode.
It does not enumerate primitive packings or invoke the full flow optimizer.
No minimum **total old-plus-new link count** is asserted.

**Proof.** Since no pair shares an old primitive with another pair, a route
can traverse at most one named bridge. Apply Theorem 1's mode coverage to
each pair. Every physical packing belongs to the mode determined by its
actually used bridges, and every mode allocation lifts to a legal global
packing. Original requests have disjoint owner sets in every mode, so each
original unit still has at most two request neighbours. The old exact
allocation and prescription theorem therefore applies globally, proving
the value formula.

A packing using sigma pays its actual sum of bridge fees and appears in
that mode. Conversely the constructed packing for a mode uses a subset of
its selected bridges, so its actual fee is at most the mode fee. Comparing
all modes makes the two bounds equal. More explicitly, if a positively
charged selected bridge were unused in the winning packing, that very
packing would belong to a cheaper mode with the same paid sources/value,
contradicting optimality. Zero-fee unused switches have no cost effect. ∎

**Why independent gains cannot be added.** Take four sources A_1,A_2,B_1,B_2,
two mixed owners X_1,X_2, old stems A_1,A_2,B_1->X_1,B_2->X_2, and new
bridges A_i->X_i. Let B_i itself support its private original unit u_i;
both X_1 and X_2 support the SAME original unit r. There are no other units.
The old value is two. Either bridge alone raises it to three. Both together
still give three, since Q={u_1,u_2,r} has only three units. Counting the two
individual gains would falsely give four. For bridge fees 5 and 2, the
minimum fee at value three is 2; requiring A_1 changes that minimum to 5.
Requiring both A_1,A_2 is infeasible. This abstract control has valid two-owner
incidence; we make no frozen-realization claim for this particular control.

## 4. One frozen board, one capacity-one change, two different outcomes

Use the existing explicit board
[frozen_all_mixed_gate_cycle.json](../develop/fixtures/frozen_all_mixed_gate_cycle.json).
It has shape 28 by 24, |T|=49, |M|=154, and all 308 actual endpoints frozen.
Initially every tile is H. Change ONLY the aligned P-free tile (24,22) to V.
It contains the one selection (24,22), so has capacity one. Original owner
bodies/types/links remain unchanged; the original interval count is 131 both
before and after. The tile's former vertical BB unit at column 23 becomes
a horizontal BB unit in row 25 with no supporting P owner; it is not deleted
from the resource inventory.

Use these named original owners (numbers are the fixed compiler's IDs):

| Name | ID | Original tips | Final whole support relevant below |
| --- | ---: | --- | --- |
| A | 12 | TP (5,19), TP (24,19) | empty |
| Y | 24 | BP (24,20), TP (24,21) | empty |
| U | 8 | TP (5,6), TP (5,17) | empty |
| X | 11 | BP (5,18), TP (12,14) | five units F |
| D | 20 | TP (24,6), TP (24,17) | six units G |
| Z | 14 | BP (24,18), TP (18,15) | four units H |

All listed units are singleton BB pairs. Their precise physical coordinates
are below; (r,c) denotes the pair {(r,c),(r+1,c)}:

    F = {(10,10),(10,12),(12,12),(12,15),(12,16)};
    G = {(24,7),(24,12),(24,13),(24,14),(24,15),(24,16)};
    H = {(14,13),(14,15),(18,13),(18,14)}.

These are disjoint original resource sets. The named actual old links are

    A->Y : (24,19)->(24,20);
    U->X : (5,17)->(5,18);
    D->Z : (24,17)->(24,18).

Choose the SAME old packing of three interval stems A->Y, U->X, D->Z for
both comparisons. Initially its respective interval witnesses may be the BB
pairs at (24,23), (10,10), (14,13); all three are original, distinct and valid.
The packing need not minimize old link count, as permitted in Theorems 1--2.

After the change, A->Y has no support, while U->X sees F and D->Z sees
G union H. Thus t_0=1 and the old-link optimum is two.

**Upper bridge fails.** Add e_up=(5,19)->(5,18), from A to X. The receiving
old request U->X has FIVE neighbouring units for one payment, hence four
unused units at every maximum allocation of that request. But U itself
supports none, and both U and A must enter X to reach F. Its one mixed gate
permits at most one of them to be paid. D can still be paid, so the exact
new value is two. The switched mode has U as an isolated unsupported request,
and t_e=1. Both modes forbid retaining all three sources. This is an explicit
failure of the rule “a bridge into a surplus component repairs one deficit.”
All 131 original units and every original whole-beta output remain in the
model; the upper-bound argument uses the complete declared E0+e_up routes.

**Lower bridge succeeds.** Instead add e_down=(24,19)->(24,18), from A to Z.
The old D stem may terminate BEFORE that entry, directly at any unit of G.
A uses e_down and any unit of H through Z. U retains its old path to X and
one unit of F. All three sources are paid, using disjoint owners and distinct
units, with exactly one new bridge (two physical links in total). In this
switched mode t_e=0. The entrance separation has been verified physically,
rather than inferred from the receiver's total reserve count.

The earlier two-source projections are archived in
[the bridge fixture](../develop/fixtures/frozen_single_bridge_compensation.json).
The validation uses the common three-source packing throughout.

## 5. Arbitrary frozen stacks, not a finite extrapolation

For any q>=1, put q translated copies at row offsets 30i, with two blank
separator rows between copies, on a (30q-2)-by-24 rectangle. Change tile
(30i+24,22) in each copy. All other tile directions remain H. Take the three
old paths per copy and either all upper or all lower named bridges.

The old selected sets and endpoints in different copies have distance at
least three across the separator. Feasibility is preserved, all actual M
edges are internal to copies, and the old strict freezing schedule replays
independently: there are exactly 308q frozen endpoints. Auxiliary mates on
P tiles stay horizontal-band mates inside their copies. Declared terminal
links are horizontal within those bands and cannot cross the separator.
No source route changes copies. Each separator supplies 24 distinct unowned
BB units, which remain inventory rather than fake accessible reserve.
All F_i,G_i,H_i are distinct physical sets. Therefore both the upper cut and
the explicit lower repair add over copies, for EVERY q:

    selected old sources                 3q;
    after pivots, old links only          2q;
    old links plus upper bridges         2q;
    old links plus lower bridges         3q;
    minimum lower bridges for 3q          q.

Thus even 4q unused receiving units do not rescue the q upper-entry deficits.
The obstruction is the q actual mixed gates, not a shortage in the global
resource count. The full unrestricted original board pays all 4q alpha sources:
in each copy A uses its original beta exit (5,19)->(5,20), U uses U->X,
D pays directly from G, and the fourth left alpha uses the BB pair
{(14,5),(15,5)} directly. These routes use different owners and resources. The upper
bound is the source count 4q.

Numerically |T|=49q, |M|=154q, L=155q-24, alpha=4q, beta=6q, and

    S=area/2-|T|-|M|=L+beta-alpha=157q-24>0.

This is an all-q frozen obstruction to the named-link surplus rule, together
with an actual alternative repair. It is not a counterexample to the full
compensation target, rectangular-grid inequality or 5/6 bound.

## 6. Verification and remaining scope

`develop/check_single_bridge_compensation.py` constructs the two-mode and batch
algorithms using only the old resource-allocation kernel. It validates every
returned primitive against independently enumerated legal primitives. The
checked run covers 184 single-bridge optima, 4344 source prescriptions, 2230
two-mode prescription obstructions, and 576 batch maximum-value/minimum-fee
prescription cases. Batch fee comparisons independently enumerate permitted
bridge sets and solve the physical primitive model, not the mode graphs.
The abstract two-bridge control explicitly rejects duplicated reserve use.

The complete physical board is rebuilt before and after its pivot; the old
packing is checked as an actual initial packing. The same bridge calculations
are rebuilt at q=1,2,4, including 2156 strict freezing-certificate events and
six full-pool restricted-link comparisons against full flow. The all-q proof
is the geometric separation argument above, not those three tested sizes.
Production controls disable full flow and primitive optimizers. No new
end-to-end Lean verification is claimed; the resource-allocation kernels have
their preceding formal audits, and the new mode-cover/fee/geometric arguments
are written proofs with independent executable checks.

Multiple bridges sharing an old stem, entries into beta forks, and arbitrary
unused external relay networks need a richer mode decomposition or the full
flow. The present theorem does not count such links automatically. The next
geometric task is to locate source-preserving resources BEFORE actual incoming
mixed entries, or to identify real routes that bypass those mixed gates. A
component's unsigned reserve count is insufficient for that step.
