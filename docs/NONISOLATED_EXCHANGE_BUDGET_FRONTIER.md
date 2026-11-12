# Exact budget frontiers with nonisolated additions

For a fixed candidate list on a degree-two bipartite auxiliary graph, this
note allows arbitrary mixed removals and additions. New points may be adjacent
to surviving old points or to one another. It computes the exact minimum
matching cost at **every exact operation count**, with explicit operation
witnesses, then constructs final matching and cover certificates.

The algorithm is a standard finite-state frontier dynamic program adapted
to this exchange problem. Its exponential parameter is the number of
candidate pairs crossing a supplied traversal cut, not the size of a
matching or a universal constant. Path matching identities and frontier-DP
ideas are not claimed independently novel; no priority audit is claimed.

## 1. Full endpoint formula and sharp budget variation

Let A be a finite simple bipartite graph of maximum degree at most two.
Here the restriction is on the **ambient** A, not merely the initial A[U].
For initial U, each candidate i replaces a different x_i in U by a different
y_i outside U. For S write U_S=(U-{x_i:i in S}) union {y_i:i in S}. All
candidate subsets are allowed in the generic problem. No final-isolation
constraints, dependencies or addition conflicts are imposed.

For V subset V(A), let o(V) count odd-order components of A[V], including
isolated vertices. Every cycle of A[V] is even. Since |U_S|=|U|,

**Theorem 1 (arbitrary endpoint cost).**

    nu(A[U_S])=(|U|-o(U_S))/2,
    nu(A[U])-nu(A[U_S])=(o(U_S)-o(U))/2.

All final isolates, including new ones, count in o(U_S). A final minimum
cover and maximum matching are constructed by selecting a smaller side in
each path or even cycle and pairing consecutive vertices. The formula does
not require additions to be isolated and does not require retaining the
initial cover.

**Proof.** On each path the common matching/cover size is half its order
rounded down; on an even cycle it is half the order. Sum the component
identities. Smaller sides and consecutive pairing give equality certificates.
The equal-cardinality replacement gives the second identity. QED.

Define the complete budget frontier

    F(t)=min{nu(A[U_S]): |S|=t},       0<=t<=q,

where q is the candidate count. The best cost with at most B operations is
min_{0<=t<=min(B,q)} F(t); the first t attaining it gives its fewest-operation
tie-break. There is no assertion that F itself is nonincreasing.

**Proposition 2 (sharp variation bound).** For all t<q,

    |F(t+1)-F(t)|<=1,
    |nu(A[U_S])-nu(A[U])|<=|S|.

**Proof.** One replacement deletes one vertex and adds one vertex. Deletion
changes matching number by0 or-1; addition changes it by0 or1. Thus a full
replacement changes it by at most one in absolute value. Extend an optimal
t-subset by any unused label to obtain F(t+1)<=F(t)+1; remove one label
from an optimal (t+1)-subset to obtain F(t)<=F(t+1)+1. Iterating the
single-replacement bound proves the second inequality. QED.

## 2. A two-state cost automaton

Choose a complete traversal of each ambient path or even cycle, and
concatenate these component orders. It may permute components, reverse
paths, and rotate or reverse cycles. Each candidate variable s_i appears
exactly twice: x_i is present iff s_i=0, y_i iff s_i=1. Fixed vertices have
their initial membership. This equal-variable constraint is the part that
can link distant positions or different auxiliary components.

While scanning a component, let p be the parity of the current consecutive
run of present vertices. The transition on a membership bit a is:

| Membership a | Incoming p | Outgoing p | Cost increment |
| --- | --- | --- | --- |
| 0 | either | 0 | 0 |
| 1 | 0 | 1 | 0 |
| 1 | 1 | 0 | 1 |

For a path start at p=0 and accept either terminal parity. This counts
floor(length/2) on every run.

For a cycle, branch over starting parity h in {0,1} and require terminal
p=h. If at least one vertex is absent, that zero resets parity; the closed
trace then counts each circular present run exactly once. If all vertices
are present, the ambient cycle has even order and both closed traces cost
exactly half that order. Thus the cycle case needs no guessed absent vertex
and also handles a fully selected cycle. At component boundaries reset
parity appropriately while retaining all live candidate assignments.

## 3. Pair width and exact dynamic program

A candidate is live after a cut when exactly one of its two vertices has
been scanned. Let w be the largest live count for the chosen concatenated
component traversal. Cross-component candidates remain live across the
boundary. This is a property of the supplied order; no efficient algorithm
for finding the best order is asserted.

**Theorem 3 (exact full frontier).** All F(t), t=0..q, and witnessing candidate
subsets can be computed in 2^w times polynomial time. At most
4(q+1)2^w states occur during a component, with O(N(q+1)2^w) transitions
up to constant factors, where N=|V(A)|. Bitset operations and witness output
have polynomial bit cost.

**Proof.** A state stores the decisions of all live variables, the count t
of selected operations introduced so far, current parity p, and a cycle
starting parity h when necessary. The state value is the lowest accumulated
matching cost and an explicit full selected-variable bitmask witnessing it.
Ties may use the numerically least mask; no unique mathematical optimum is
claimed.

At the first occurrence of candidate i, branch on s_i=0,1. Record its decision
until its second occurrence and add s_i to t **once**. At the second
occurrence use the stored decision, apply the appropriate x/y membership,
and forget i. In particular, y_i may occur before x_i. Fixed vertices simply
use their membership bit. Apply the automaton transition and keep only the
lowest value for identical states. At a cycle end discard nonclosed traces;
at any component end merge states after dropping parity but retaining live
assignments and t. At the end every candidate has appeared twice, so no
live assignments remain. The minimum value for each t is F(t).

For rigor, every partial assignment to introduced variables and every valid
automaton prefix gives a state. Conversely every state transition chooses
exactly such an assignment and prefix. Two histories with the same state
have identical possibilities for future variables and membership bits; all
past costs are additive. Keeping the smaller accumulated cost cannot remove
a better completion. Induction through all vertices and component-boundary
closures proves exactness. For cycles the trace argument above proves that
minimizing over accepted automaton paths gives the actual matching number,
including the all-present case.

There are at most2^w live assignments, q+1 counts, two p-values and two
h-values. Each state has at most two next choices. The number of transitions
has the stated bound. Storing a full witness mask uses q bits per value;
the q+1 final masks use O(q^2) output bits. Decoding them and constructing
matching/cover certificates with Theorem1 incurs only polynomial cost. QED.

For w bounded independently of q the algorithm is polynomial even with
arbitrarily many operations. In general w can grow with q; no unrestricted
polynomial-time optimizer follows. The auxiliary graph's degree-two form
alone does not remove the candidate equalities linking different positions.
The method does not rely on monotonicity or on an inherited cover.

For the physical helper/owner setting A=P union Q is automatically bipartite
and degree two, since P is a perfect matching and Q another matching. Fix a
permitted initial omission, and at most one individually permitted within-owner
replacement per owner component. Then every subset and every prefix remains
permitted: the changes lie in distinct owner components. Consequently the
frontier is exact over **all subsets of that list**, including nonisolated
additions. The physical wrapper checks these restrictions, returns an
optimal batch, and supplies owners/witnesses and a dissociation certificate
of size3b-F(t). It does not optimize over unrestricted omission sets or
multiple incompatible operations in the same owner.

## 4. Two physical all-scale boundary families

Both families below have unit matching costs, minimum-cardinality initial
omissions and square owner components. All subsets are permitted. Their
opposite slopes show that Proposition2 is sharp in both directions.

### 4.1 Every operation increases cost

**Theorem 4.** For every r>=1 there is a two-connected bipartite physical
graph of order10r, minimum degree2 and maximum degree3, with r candidates,
auxiliary graph r disjoint P4s and

    F(t)=t,       0<=t<=r,       initial cost0.

The displayed traversal has pair width at most2 (at most1 when r=1).

**Construction and proof.** For each i modulo r introduce witnesses
x_i,y_i,z_i,w_i with physical colours0,1,1,0. Put

    P={(x_i,w_i),(y_i,z_i)},     Q={(x_i,y_(i+1))},
    owner square=(x_i,y_i,w_i,z_i),
    U={all x_i, all z_i},       candidate i:x_i->y_i.

Every owner has exactly two omissions, a minimum for a square. A[U] is
edgeless. The auxiliary components are

    w_i -- x_i -- y_(i+1) -- z_(i+1).

In a selected batch S, w_i is always absent and z_(i+1) always present;
y_(i+1) is present precisely when i+1 is selected. If selected, the surviving
component has its edge y_(i+1)z_(i+1), possibly with x_i attached, hence
matching cost1. If unselected it has cost0. Summing gives cost=|S| for every
subset, proving the entire frontier.

Physical colours satisfy the P/Q/B conditions. Each owner square together
with its two P-helper paths is a two-connected module: both paths are ears
between distinct owner vertices. Q joins these modules cyclically, with
at most one intermodule Q-edge incident with any physical vertex. Removing
one vertex preserves each module's connectivity and removes at most one
cyclic joining edge. For r>=3 the quotient cycle stays connected. For r=2
the quotient has two distinct joining edges and one remains; for r=1 the
single Q-edge is internal and adding it preserves the module's connectivity.
This proves two-connectivity at every scale. Centres and non-Q witnesses
have degree2, Q witnesses and owners degree3.

Ordering the P4 components as0,r-1,1,2,...,r-2 for r>=3, orient component0
forward as displayed, componentr-1 backward, and the remaining components
forward. This closes candidate0 before introducing candidater-1 and keeps
at most two pairs live: the wrap candidate and the current local candidate. The r1/r2 cases satisfy the displayed
bounds directly. The implementation's canonical component traversal gives
the same bound. QED.

Thus extending a greatest-batch monotonicity rule after dropping final
isolation can be wrong by an arbitrarily large additive amount. The actual
unrestricted-list optimum here is the empty batch; the example is not a
counterexample to an earlier theorem that required final isolation.

### 4.2 Nonisolated additions can be useful

**Theorem 5.** For every r>=1 there is a two-connected bipartite physical
graph of order20r, minimum degree2 and maximum degree3, r candidates and
pair width1, with

    F(t)=2r-t,       0<=t<=r.

Requiring final isolation allows only the empty batch, of cost2r; allowing
the additions gives costr and an actual certificate of size11r. Earlier
mixed inherited-cover certificates already attain costr on this family;
this comparison is specifically with the final-isolation domain.

**Construction and proof.** Set N=8r,b=4r and A=C_N, with consecutive
even-odd P-pairs, complementary Q-pairs and physical colour floor(v/2) mod2.
For tile i write a=8i and use owner squares

    (a+2,a+5,a+6,a+1),       (a,a+3,a+4,a+7),
    U cap tile={a+1,a+2,a+3,a+4},
    candidate i:a+2 -> a+5.

The squares alternate physical colours and each has two initial omissions;
the operation stays in the first square and every subset is permitted.
An unselected tile has a P4 on1,2,3,4, with cost2. A selected tile has an
isolate1 and P3 on3,4,5, with cost1. Tile boundaries remain absent, so all
costs add. The new5 is adjacent to surviving4, hence every selected
operation violates final isolation. This proves the cost comparison and
shows the new point can extend a balanced path at no extra matching cost.
The physical centres/witnesses form the auxiliary cycle with P-edges
subdivided. Each owner square has four distinct attachments to that cycle.
After any one deletion the remaining cycle is intact or a path, and every
owner square or its remaining path retains at least three attachments.
All remaining vertices stay connected. The colour and degree bounds follow
directly from the P/Q/B construction.

In the natural order0,1,...,8r-1 every pair(a+2,a+5) is confined to its
own tile, and at most one pair is live. An earlier mixed certificate uses
initial cover{a+2,a+4}, matching{(a+1,a+2),(a+3,a+4)} per tile, retires a+2
when selected, and retains a+4 to cover the final P3. Thus no gain over that
broader earlier rule is claimed. QED.

The all-square owner class already has unrestricted positive results in
the prior research. Neither family settles a new universal numerical class,
proves an unrestricted all-helper optimum or embeds into rectangular grids.

## 5. Why the width parameter is substantive

The preceding [physical Vertex Cover encoding](MIXED_ISOLATED_REPAIR_AND_OPERATION_HARDNESS.md)
proves NP-completeness of reaching cost0 within a given operation budget,
even for two-connected bipartite physical min2/max3 graphs with square owners,
minimum omissions and auxiliary P4/P2 components. That theorem required
final isolation, but cost0 itself makes the final auxiliary graph edgeless.
Final isolation is therefore automatic for every cost-zero batch. The same
zero-cost decision equivalence and threshold hold without imposing that
restriction explicitly.

Consequently a uniform polynomial algorithm for the entire budget frontier
in this restricted physical class would solve that NP-complete problem.
Theorem3 does not make that claim: pair width can grow. This argument does
not prove hardness of minimizing cost with **no operation budget and no
tie-break**; the reduction's zero cost is reached simply by selecting all
groups. No hardness of unrestricted graph parameters or rectangular grids
is asserted.

## 6. Reproduction and remaining scope

Implementation: [nonisolated_exchange_frontier.py](../develop/nonisolated_exchange_frontier.py).
Run the complete assertion-enabled checker:

```sh
python3 -B scripts/check_nonisolated_exchange_frontier.py
```

The checker compares every exact-count cost and at-most-budget optimum with
independent literal candidate and matching enumeration on its small inputs.
The [saved report](../output/nonisolated-exchange-frontier-check.json) contains
aggregate counts, a reproducibility digest and two r=2 family examples; it
does not contain every comparison row. Checks include fully selected even
cycles, all cycle subsets through12 vertices, different component traversals,
arbitrary candidate crossings and y-before-x orders, random physical lists,
both all-scale families and earlier hardness budget controls. Connectivity
checks delete every vertex through r=6 and four sampled vertices at each
larger tested scale; all-size connectivity relies on the proofs. Regression
controls also pass one-shot iterators for generic edges, U, operations,
selected labels and supplied component orders. The
[independent audit receipt](../output/nonisolated-exchange-frontier-review.json)
records the original finding, correction and exact-source execution scope.
General conclusions rely on the
proofs above, not extrapolation from finite enumeration.

The fixed-list exchange problem now has an exact parameterized solution
without final isolation. A universally small traversal width or a structural
cost guarantee remains unproved. Universal8b/3, sharp remaining degree/gap
parameters, compatible physical multi-Hall routing, a universal unit5/6 gain
and arbitrary-width rectangular-grid triple equality remain in the full
ACTIVE goal. The October submitted manuscript is preserved; no weighted TH
or formal-kernel verification is claimed here.
