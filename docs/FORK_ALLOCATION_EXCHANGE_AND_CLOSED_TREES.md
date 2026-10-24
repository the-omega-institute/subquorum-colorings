# Fork allocation exchange and closed ordinary blocking trees

25 October 2026. Haobo Ma and Wenlin Zhang. Research branch only.

An arm unit occupied by an ordinary interval stem need not be permanently
blocked: that stem can change its interval, possibly through an alternating
chain of other interval stems. We give an exact joint-matching formula for
this exchange, preserving every old ordinary paid source and every old used
interval identity. We then strengthen the previous thin-gap obstruction.
In a minimum-link maximum packing with two-owner supports, a terminal fork
can be blocked only by closed ordinary allocation trees, each with exactly
one private entrance unit. Different terminal forks have disjoint blocking
trees. Their used units are not additional reserve. More precisely, the joint
matching defect is exactly the number of terminal forks, rather than the
number of original forks or the number of ordinary blocking trees.

The proof uses standard matching augmentation and spanning-tree counting.
The contribution is their application to fixed cancellation routes, beta
consumption, immutable original interval identities and physical two-owner
support. We do not claim a general grid inequality or unrestricted physical
fork gain. The 11 October submitted manuscript is preserved.

## 1. Joint exchange problem

Use the [whole-support stem/fork normal form](WHOLE_SUPPORT_FORK_NORMAL_FORM.md),
possibly after immutable C0 contraction. Every current owner has a fixed
support W(x) in distinct available original intervals I. Compatible
certificates have disjoint owner sets and allocate different intervals.
The interval access of a final strand is the union of its old owner supports.
All costs below count additional terminal links.

Fix a normalized packing P with:

* h beta forks H, each with two different alpha roots and different beta
  entry tips, paying 2 by one whole beta and its assigned interval J_f;
* m ordinary interval stems K_I, each paying 1 by its assigned original unit;
* t ordinary beta stems K_B, each paying 1 by a different whole beta.

Fix the routes and owner sets of these certificates. We may truncate routes
and change interval assignments. We may not introduce another link, use
another owner, undo C0 or alter K_B. Release all old fork interval assignments.
The old interval-stem assignment has used set U, with |U|=m.

Build a bipartite graph with left vertices H union K_I and right vertices I.
A fork f has neighborhood A_f, the union of supports of its two arms
**before** its terminal beta. An interval stem k has neighborhood V_k, the
union of supports of all owners on its existing route. Every witness for a
unit of V_k can be reached by a prefix of that route, so changing to that
unit never increases its number of links. A beta body is not an ordinary
transit access. No use of actual free-tip interval access is asserted.

Let mu be the maximum matching number of this joint graph, and set

    delta_ex = h+m-mu.                                    (1)

The old assignment already matches K_I, so mu≥m and 0≤delta_ex≤h.

## 2. Exact value with preserved old sources and interval identities

**Theorem 1 (joint allocation exchange).** In the ordinary route system
obtained from the fixed P routes, with K_B retained, the maximum payment is

    t+h+mu = (t+m+2h)-delta_ex.                            (2)

There is a realizing ordinary packing that retains every old K_I and K_B
source as paid, uses every old interval in U, uses exactly mu distinct
intervals, and takes a subset of P's links. Its link cost is at most

    links(P)-h.                                          (3)

Thus exactly mu-m different extra original units, relative to U, are added
to the interval allocation. Some can be old fork intervals released at the
start; such units are not new global slack.

**Proof of the matching and preservation claim.** Start with the old matching
saturating K_I. Repeatedly augment from unmatched fork vertices. Each
alternating path ends at a previously unmatched right vertex, reassigns each
internal left vertex, and matches its new fork root. Every old matched left
vertex remains matched; every old matched right vertex remains matched.
When no such augmentation remains, no unmatched left vertex has an augmenting
path, since the only initially unmatched left vertices were forks. The
matching is maximum, has size mu, still covers K_I, and its right set
contains U. It matches g=mu-m forks.

For a matched fork, take one interval prefix witnessing its assigned unit
and its other complete beta arm, paying both original sources. For an
unmatched fork, retain one beta arm, paying one source. For k∈K_I, truncate
to a witness for its new interval. Retain K_B unchanged. These owner sets
are subsets of disjoint old certificates; beta units remain different,
intervals are the matching's different original units, and U remains used.
The payment is t+m+h+g=t+h+mu.

Each matched fork loses at least its interval arm's final beta-entry link;
each unmatched fork discards an entire nonempty arm. Every fork therefore
saves at least one link. No ordinary prefix adds a link. This proves (3).

For the reverse bound, consider any ordinary packing in the restricted
routes, even one that drops some old K_I sources. If m' such sources are
paid, they require m' different interval payments. Let D be the forks whose
two original sources are both paid. Each has at most one beta payment, so
choose one of its pre-beta interval payments. Together these choices give
a matching of size m'+|D| in the joint graph. Total payment is at most

    t+m'+h+|D| <= t+h+mu.

This includes ordinary solutions using two interval stems in a fork instead
of a beta. Hence (2) is exact, while the constructed solution supplies the
stronger old-source and old-used-unit preservation properties. ∎

The source-to-unit assignment need not remain unchanged. Preserving the
identity of every old used interval is consistent with changing which
old source spends it. Treating those old units as fresh credit would give
the wrong count.

**Corollary 2 (sharper whole-network bound).** For any maximum-value packing
P of a full system D,

    0 <= nu(D)-nu0(D) <= delta_ex
       <= delta_fixed,                                  (4)

where delta_fixed is the previous fork-matching defect with K_I assignments
frozen. Indeed a matching of forks avoiding U can be adjoined to the old
K_I matching, so mu≥m+mu_fixed. A full joint matching removes all forks,
preserves value, and saves at least h links. Consequently any nonempty fork
pack in a minimum-link maximum packing must have delta_ex>0.

The ordinary minimum link cost can be smaller than the construction in (3),
because two interval payments can beat retaining a beta. We claim an exact
value and a cost upper bound, not an exact ordinary cost formula.

## 3. Exchange paths and cycles in a lexicographic optimum

Now assume P maximizes payment and then minimizes link count. Give every
interval-paying certificate p∈H union K_I its old assigned unit J_p.
Its access N_p is A_p for forks and V_p for ordinary interval stems.
Draw p->q, p≠q, whenever J_q∈N_p. Also record access to a right unit not
assigned anywhere in P as a free exit. Ordinary self-access to J_p is
ignored; fork self-access would itself remove that fork.

**Lemma 3 (no fork escape or fork cycle).** There is no directed path from
a fork to a free exit, no directed cycle containing a fork, and no fork
self-access.

**Proof.** On a simple path from a fork to a free unit, move each certificate
to the old assigned unit of its successor and move the last one to the free
unit. The units along the path are different. Every ordinary certificate
can take a route prefix to its new witness; every fork can use an interval
prefix and its other beta arm. Release exactly the affected old assignments
before making these changes. All other assignments remain fixed, all sources
on the path remain paid, and each affected fork saves at least one link.
This contradicts minimum link count. A simple directed cycle containing a
fork permits the same cyclic shift, with no free unit needed. A self-access
is a cycle of length 1. Any directed closed walk through a fork contains a
simple directed cycle through that fork after removing repeated interior
segments. ∎

This is stronger than forbidding cycles only among forks. A chain can pass
through many ordinary allocations before reaching another fork or an exit.
It still cannot reuse an original unit, owner or beta.

## 4. Two-owner incidence forces closed ordinary trees

Assume each unit of I belongs to at most two current owners. This is the
physical endpoint-free-gap adapter; contraction unions owner supports and
cannot increase the number of neighboring current owners.

**Lemma 4 (at most one external predecessor).** After ordinary self-arcs
are removed, each interval-paying certificate q has at most one incoming
certificate neighbor.

**Proof.** Its assigned interval J_q has a supporting owner inside q,
including the beta body if q is a fork. An incoming certificate p requires
a supporting owner outside q. There is room for at most one such owner;
owner-disjointness places it in at most one other certificate. ∎

Thus the subgraph reachable from any fork is a directed forest. A cycle
containing a fork is excluded by Lemma3. An ordinary-only directed cycle
cannot be entered from outside: the first entered vertex would have both
its cycle predecessor and a different path predecessor, contradicting
Lemma4. Reachable paths cannot merge from different predecessors either.

A **terminal fork** is a fork from which no different fork is reachable,
allowing intervening ordinary certificates. A nonempty H has a terminal
fork because mutual reachability would make a forbidden fork cycle.
For terminal f let C_f be the ordinary interval certificates reachable
from it. It can be empty if A_f is empty.

**Theorem 5 (closed ordinary blocking trees).** For a terminal fork f:

(a) The union of route supports of C_f is precisely its old assigned set:

    union_{k in C_f} V_k = {J_k : k in C_f}.               (5)

(b) In the interval-incidence graph on C_f, each connected component is a
tree with exactly one private resource. That private resource is its sole
entry interval from A_f. Different entries of f belong to different tree
components.

(c) Different terminal forks have disjoint ordinary closures C_f and
different entrance resources. In particular these blocking trees cannot
be charged independently to two forks.

**Proof.** No reachable certificate sees a free interval by Lemma3. Its
accessible old assigned units cannot belong to another fork by terminality.
They therefore belong to C_f. Conversely each ordinary certificate supports
its own assigned unit. This proves (5).

Represent a resource with two certificate neighbors in C_f by an edge,
and one with a single neighbor by a private resource. Each component has
n certificates and exactly n resources: equation(5) pairs each resource
with its old certificate, which lies in that same incidence component.
Connectedness requires at least n-1 edge resources.

Every component is reached from f. Along a first-entry path there is an
interval j∈A_f assigned inside the component. One of j's original supporting
owners lies in f, so the at-most-two hypothesis leaves at most one supporting
owner inside C_f. Hence j is private within C_f. There is at least one
private resource, so the n-resource inventory and n-1 edge lower bound
force exactly n-1 edges and one private resource. They form a tree. Every
other entry would likewise be private, so it is the same unique interval.
This proves (b).

For (c), directed paths from two different terminal forks cannot merge in
the directed forest; neither fork can be an ancestor of the other. Their
reachable ordinary certificates are disjoint. An entrance interval already
has one witness in its fork and one in its ordinary tree; it cannot have
a third witness in another disjoint fork. ∎

These are saturated ordinary trees, with zero unused interval reserve,
not the deficient substitute trees of the previous note. Their vertices
are ordinary interval certificates, which may themselves contain bent or
long mixed routes. An unused unit anywhere on their route supports would
create a free exit and remove the alleged blocking. Additional legal routes
outside the fixed P links are still a separate question.

**Theorem 6 (exact terminal-fork defect).** Under the hypotheses of this
section, let T be the number of terminal forks in the full certificate
exchange graph, allowing ordinary intermediate vertices. Then

    delta_ex = T,
    nu0(P's fixed routes) = value(P)-T,
    0 <= nu(D)-nu0(D) <= T.                              (6)

The last inequality assumes P is a maximum-value packing of the full system
D, as above. The first two statements concern its fixed routes. In particular
T>0 does not assert a strict whole-network value gap.

**Proof.** For each terminal fork f the left set {f} union C_f has precisely
|C_f| neighbors: its right neighborhood is {J_k : k in C_f}. This follows
from (5) and the fact that every accessible interval of f enters C_f.
For C_f empty this is the singleton left set with empty neighborhood.
These left sets and their right neighborhoods are disjoint for different
terminal forks. Each leaves at least one unmatched left vertex in any
matching. Therefore delta_ex >= T. Several ordinary trees attached to the
same terminal fork collectively give this one-unit deficit; they are not
separate missing fork sources.

For the opposite bound, for every nonterminal fork f choose a directed
path from f to the first different fork g on that path. All intermediate
vertices are ordinary. Paths chosen for different starting forks have
disjoint ordinary interiors and different endpoint forks. Indeed, any
merger forces a common predecessor, by Lemma 4. Following predecessors
backwards would either identify their distinct starting forks or force
one to be an interior fork of the other path, both impossible. Paths may
share a fork only as the endpoint of one and the start of another.

Start with the old matching of all K_I. Along each chosen path match every
vertex except its endpoint to the old assigned unit of its successor.
Leave ordinary vertices outside these interiors unchanged. The distinct
endpoint units J_g were old fork assignments, hence absent from the initial
ordinary matching. Every old intermediate ordinary unit is now used by
its predecessor. Thus all old ordinary sources and all units U stay matched;
the disjointness just proved prevents any repeated left vertex or right
unit. Every nonterminal fork is now matched. Terminal forks are unmatched.
This constructs a matching of size m+h-T, so delta_ex <= T. Apply Theorem 1
and Corollary 2 to conclude (6). ∎

This sharpens the residual search: each terminal fork contributes one local
fixed-route defect, however many saturated ordinary trees it sees. Branching
can leave several terminal forks, so the defect is not generally just the
number of connected components of the directed exchange forest.

## 5. An arbitrarily long obstruction with ordinary intermediates

The following is abstract, not a claimed frozen-grid realization. For q≥1
create forks f_i with alpha roots A_i,C_i, beta B_i and two direct links.
Give B_i interval J_i. Introduce an ordinary alpha K_i with its own unit H_i.
Give A_i access to H_i, and K_i also access to J_(i+1) for i<q-1. No other
support or link exists. Every interval has at most two owners.

Take P to be all q forks, each spending J_i, and all K_i spending H_i.
It pays all 3q sources with 2q links. Full payment forces K_(q-1) to take
H_(q-1), then forces the last fork to use J_(q-1). Inducting backwards
forces every K_i to keep H_i and every fork to use its J_i. Thus the exact
full optimum is (3q,2q).

Frozen old K assignments leave every fork blocked: delta_fixed=q.
Joint exchange instead moves K_i to J_(i+1) for i<q-1, retains the final
K on its H, pays A_i from H_i for i<q-1, and pays every C_i by B_i. Only
A_(q-1) is unpaid. All q old H intervals remain used, all q old K sources
remain paid, and every added J_1,...,J_(q-1) is different. Ordinary payment
is 3q-1 with q links.

This is optimal: only J_1,...,J_(q-1) and the q H units are ordinary-accessible,
so at most 2q-1 interval payments and q beta payments are possible. Attaining
3q-1 requires q beta links. The joint graph has 2q left vertices and maximum
matching 2q-1, giving delta_ex=1. Its dependency path is

    f_0 -> K_0 -> f_1 -> K_1 -> ... -> f_(q-1) -> K_(q-1).

The final ordinary singleton tree blocks its unique entrance. This family
shows why a fixed-assignment defectq can overestimate the residual gap by
q-1, while a real one-unit obstruction remains. Its ledger |I|+beta-alpha
is 2q+q-3q=0; it is not a target-inequality counterexample.

Arbitrary rooted ordinary trees give another family: each ordinary vertex
has its parent-edge unit, the root has one anchor shared with a fork arm,
and the beta has its own interval. All ordinary vertices plus the fork
pay n+2, whereas ordinary-only compensation pays n+1. Add a free interval
at any leaf and the path to that leaf releases the anchor, preserving all
old paid ordinary sources and old used units. The checker includes paths,
stars, binary trees, forests and mixed internal ordinary routes.

## 6. A concrete physical shielding obstruction and safe insertion

The known 16-by-14 frozen fixture has C with TP tips (12,2),(12,5), selected
guards (13,2),(13,5), and a private two-unit gap at columns 3,4 of band 6.
Retain all old T and the actual matching M, and permit arbitrary additional
selected vertices. No feasible such extension can place a selection in any
of the four gap cells:

* (12,3) already has distinct occupied neighbors (12,2),(11,3);
* (12,4) already has distinct occupied neighbors (12,5),(11,4);
* (13,3) would give the old selected guard (13,2) a second occupied neighbor,
  in addition to its old neighbor (12,2);
* (13,4) similarly violates the guard (13,5), already adjacent to(12,5).

Additional selections elsewhere cannot undo any of these occupied-neighbor
violations. The two BB columns therefore persist, remain internal and
unmarked, and still have C as their only open owner. Thus selected-only
shielding of this fixed matching cannot make the designated fork optimal
if its terminal types remain a fork. This is a general monotone-extension
argument for the specified local geometry, not an inference from a bounded
UNSAT search.

Adding instead the actual matching edge((12,3),(12,4)) is feasible and fully
frozen. Old mates and selected vertices remain unchanged, so every old
freezing derivation is preserved. Freeze (12,3) using retained nonmate P
neighbors (12,2),(11,3), whose old mates are frozen; freeze (12,4) using
(12,5),(11,4). Every old selection still has at most one occupied neighbor.
The two new endpoints form an original BP--BP strand, an extra whole beta.
C can enter it by either actual TP--BP link, spending one whole-beta unit.

The resulting board has 68 endpoints, I=41 and beta=3. It still has ordinary
value 3, now with minimum link cost 2, using A's interval, C's new beta and
D's old beta. Both C and D have empty initial support and need separate
links, giving the cost lower bound. Removing a private gap this way has
introduced a real replacement resource; it has not created strict fork
advantage. This concrete 68-endpoint control is independently replayed.

## 7. Verification scope and continuation

The solver-free checker passes 714 pack-exchange controls, with 89 strict
improvements over the frozen-assignment defect bound and 49 partial-replacement
controls. It preserves 1458 occurrences of old used interval identities and
1689 occurrences of old paid outside sources, replaying actual subsets of
links and comparing the exact value to independent ordinary terminal flow.

The controls include 128 ordinary-forest families, 500 random full optima,
10 all-length-chain instances with full independent packing optimization
for q≤5, and 12 actual frozen lifts (six stack sizes, with and without blank
right padding). Under two-owner supports it checks 638 allocation dependency
graphs, 100 closed ordinary trees on 310 certificate occurrences, including 66
nonsingleton trees. Physical lifts have no unrestricted strict fork gain.
All 638 two-owner dependency graphs also pass the exact terminal-fork-defect
identity, with explicit first-next-fork path reassignment. This includes 64
additional branching dependency forests. The new 68-endpoint insertion is a
separate physical control.

Thirteen scoped local Lean 4.33.0 declarations pass after memory/process
preflight. They prove arbitrary-q typed interval/source injectivity for the
alternating-chain exchange, disjoint beta-paid sources, retention of every
old K source and H interval identity, the joint-defect ledgers, unique
outside witnesses, the closed-component single-anchor count, and generic
feasibility exclusions used by the shielding argument. Three declarations
are axiom-free; the others use only propext, Classical.choice and Quot.sound.
There are no warnings, incomplete proofs or native_decide. General matching
augmentation, the route construction, allocation-forest geometry, the exact
terminal-fork defect and exact all-q optima are written proofs, not claimed
full Lean formalizations.
No new Oracle or external-review verdict is claimed.

Reproduce:

    python3 develop/check_fork_allocation_exchange.py --output output/fork-allocation-exchange-validation.json
    python3 develop/check_fork_allocation_exchange_formal.py --lean /path/to/lean-4.33.0 --output output/fork-allocation-exchange-formal-validation.json

The next physical target is a thin fork whose external allocation blocking
survives **all** ordinary interval exchanges: its terminal ordinary closures
must be saturated trees with one entrance each. A valid candidate still
requires checking full-network rerouting beyond the selected routes.
Selected-only shielding of the current C gap is now excluded, and merely
inserting endpoints can add ordinary beta credit. The general compensation
inequality and universal 5/6 improvement remain open.
