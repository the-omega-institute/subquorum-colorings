# Cyclic mixed entrances: when distinct peripheral betas repair together

25 October 2026. Haobo Ma and Wenlin Zhang. Isolated research branch.

The [actual frozen mixed cycle](FROZEN_MIXED_GATE_CYCLES_AND_OCCUPIED_CHAMBERS.md)
does not justify counting different peripheral beta exits as independent
repairs. We give an exact criterion for a cyclic source/gate interface. It
depends on the positions of the sources diverted to beta, as well as on
the different original beta and interval identities. On the actual frozen
board, a declared original subinterface has two interval-tree deficits and
two different available beta exits, but still misses one payment. Allowing
another beta exit permits a different, successful pair. The complete original board retains other exits and
still pays all four; this is an obstruction to a compensation rule, not to
the unrestricted grid inequality or the 5/6 bound.

This is a specialization of matching to a cyclic interface, not a new
general matching theorem. The geometric task is to establish its Hall
conditions, or a more general full-network cut, from the original board.

## 1. Interface and resource identities

Let n>=3. The designated sources s_i and capacity-one mixed gates g_i are
indexed cyclically. Source s_i has exactly the two gate options g_i and
g_(i+1). Every paying route in this declared interface is either

* s_i -> one of its two gates -> one available original interval; or
* s_i -> an allowed peripheral whole beta.

The interval's gate support has size one or two. Form the resource
multigraph R on ALL n gates, including isolated gates: an interval with
two supporting gates is an edge, and one with a single supporting gate
is a loop. Parallel original intervals stay different edges. Let T be
the family of tree components, including isolated vertices; write t=|T|.
Non-tree components include components with loops or parallel-edge cycles.
With no beta use, the interval optimum is n-t, by the fixed bijection
s_i->g_i and the resource-graph rank lemma.

An allowed source/beta incidence must have a real route. Different chosen
source/gate/interval routes and source/beta routes must lift simultaneously:
no shared intermediate owner, BP entrance or interval, except a gate or
beta which the assignment uses at most once. Beta routes avoid the mixed
gates and interval branches. Betas have no allowed body-interval exits in
this interface, so two BP tips are never two whole-beta credits. All
allowed routes project back to these choices. These are hypotheses; a
complete frozen grid need not have this form. Costs are not eliminated by
prepaying beta options.

In a physical cycle using the two different original TP ports at every
source, n is even by terminal color parity. The combinatorial statements
also hold for odd abstract cycles.

## 2. Exact cut criterion for a fixed choice of escaped sources

Choose a nonempty source set E. Delete its source edges from the cycle
on gates: edge i joins g_i to g_(i+1). The remaining graph is a disjoint
union of |E| paths, including isolated gate vertices. Call these the
**gap components** K(E). Each gap with v gates has v-1 remaining sources.

Make a bipartite graph between the resource tree components T and gaps
K(E): a tree and a gap are adjacent exactly when they share a gate vertex.
Let mu(E) be its maximum matching size. Both the resource components and
the gaps partition gates, but these are different partitions.

**Theorem 1 (fixed escaped-source criterion).** Suppose the sources in E
are assigned injectively to allowed original peripheral betas. All other
sources can be paid by different gates and intervals if and only if

    mu(E)=t,

equivalently, for every subfamily X of resource trees,

    |X| <= |{K in K(E): K meets some tree in X}|.             (1)

The beta assignment and this tree/gap matching are BOTH required.
For E empty, full payment is possible exactly when t=0.

**Necessity.** In a gap with v gates, its v-1 sources must use v-1
different gates inside that gap. Thus exactly one gate in each gap is
unused by interval routes. A resource tree with w gates has only w-1
original intervals, so at least one of its gates must be unused. Choose
one such gate for each tree. Different trees are disjoint. Their chosen
gates cannot lie in the same gap, since that gap has only one unused
gate. Sending each tree to the gap of its chosen gate is an injective
matching, proving (1). An empty E would leave no unused gate, so no tree
is then possible.

**Sufficiency.** Match all resource trees to different intersecting gaps.
In each matched gap choose one gate in its matched resource tree. In each
unmatched gap choose any gate. Declare precisely these |E| gates unused.
Every resource tree contains an unused gate. Root it at one such gate and
assign its parent interval to each other gate; if there are additional
unused gates, discard their assignments. Every non-tree resource component
has a matching covering all its gates: take a spanning unicyclic subgraph,
orient its cycle cyclically and orient attached trees away from the cycle.
Discard the assignments of unused gates. Hence all remaining gates get
different original intervals, with no identity spent twice.

In each source gap, order the gates 0,...,v-1 and let its unused gate be j.
Send source edge i to gate i for i<j, and to gate i+1 for i>=j. This is a
bijection from its v-1 sources to the gates except j, and uses actual
incidences. Different gaps are disjoint. Combine it with the interval
assignment and the assumed injective beta assignment. The interface lift
hypotheses give simultaneous legal paths. This proves sufficiency for all
n, not by enumeration. For empty E and t=0 use the original cycle
bijection and the non-tree assignments. QED.

**Corollaries.** A single connected interval tree is repaired by ANY one
allowed beta escape: deleting one source leaves one gap containing every
gate. For several resource trees, merely having t different beta options
is insufficient; their escaped-source positions must satisfy (1). At
least t beta payments are necessary for full payment. Whenever full
payment is possible, exactly t suffice, by the following pruning lemma.

**Lemma (pruning surplus beta uses).** Suppose Theorem 1 succeeds for
escaped sources E and their beta assignment. If t=0, all sources can
instead use intervals. If t>0, choose one root gate for each resource tree
in its matched gap. These t roots are distinct and in different gaps.
Between each two consecutive roots around the source/gate cycle lies at
least one deleted source edge from E; otherwise those roots would be in
the same gap. Keep one such deleted edge in each of the t disjoint cyclic
arcs, and restore all other edges of E. The retained escape set E' is a
subset of E of size t. Its t gaps each contain exactly one chosen root,
so the tree/gap matching still saturates all trees. Restrict the original
beta assignment to E' and apply Theorem 1. This pays everyone using
exactly t original whole betas. For t=1 the sole cyclic arc runs from the
root back to itself through the entire cycle; it contains a deleted edge
because E is nonempty. QED.

Thus the issue is WHICH t beta uses work, not a need to spend more than t
once a full repair exists. This also gives a criterion using only escaped
sets of size t. Pruning preserves the chosen beta identities as a subset;
it can change interval assignments and does not promise to preserve cost.

## 3. Exact deficit, and cost when the number of beta uses is minimal

The criterion also determines the whole ordinary interface value. Let U
be the sources deliberately left unpaid and E the sources paid by beta,
with U and E disjoint. Define K(U union E) by deleting both sets of source
edges. Then

    D = min |U|,                                             (2)

where the minimum is over pairs U,E for which E has an injective allowed
beta assignment and every resource tree matches a different intersecting
gap of K(U union E). For U union E empty the condition is t=0.
Indeed project any packing to its unpaid and beta source sets, and repeat
Theorem 1's necessity on its interval-paid sources. Conversely the same
construction pays every source outside U. Thus V=n-D. This formula retains
both kinds of capacity, rather than separately adding maximum repair counts.

There is a useful cost formula when exactly t>0 beta routes are used. Fix
their source/beta matching F, with escaped source set E. Assume entry and
exit costs separate: a_(i,g) is the gate-entry toll, w_(g,h) is the toll
from gate g to supported interval h, and d_(i,b) is the beta-route toll.
All are costs of actual paths satisfying the lift hypotheses.

There are exactly t gaps and t resource trees. A full packing must leave
exactly one gate unused in each tree, and none in a non-tree component.
Every tree therefore uses ALL its original intervals. Write

* A_K(v): the sum of entry costs for the gap's unique matching when v is
  its unused gate (the explicit two-sided assignment in Theorem 1).
* B_T(v): the sum of exit costs for the tree matching rooted at v.
* B_non: the sum of minimum full gate/interval matching costs over the
  non-tree resource components.

**Theorem 2 (fixed-F cost).** The minimum full-payment cost using exactly F
as its beta routes is

    sum_((i,b) in F) d_(i,b) + B_non
      + min_(perfect tree/gap matching)
          sum_(T,K matched) min_(v in T intersect K) [A_K(v)+B_T(v)]. (3)

An empty intersection has infinite weight. Both path and rooted-tree
matchings are unique: peel from the endpoints/leaves toward the omitted
root. Thus any full packing gives a perfect tree/gap matching and pays at
least (3). Choose the minimizing shared root for each matched pair and
combine the unique assignments and optimal non-tree matchings to attain
it. This proves the cost identity. When t=0 and E is empty, instead
minimize over the cycle's two perfect entry matchings. Formula (3) does
not assert that an optimum for link cost over ALL beta choices uses exactly
t betas: restoring a cheap beta route to an expensive interval route can
increase cost, even though it reduces beta use.

## 4. Actual frozen interface: two distinct beta repairs still overlap

Use the unchanged 28x24, 308-endpoint completely frozen fixture from the
preceding note. The original source/gate cycle, in cyclic order, is

    A: g0,g1; B: g1,g2; C: g2,g3; D: g3,g0.

Use precisely two available original interval identities:

    p=(band6,column15), supported by g1;
    z=(band9,column13), supported by g2,g3.

Within these four gates, resource components are

    non-tree: {g1}, with loop p;
    tree T0: {g0}, isolated;
    tree T1: {g2,g3}, with original edge z.

There are t=2 tree deficits and interval value2. The following THREE
whole betas and their one-link source entries are original and distinct:

    beta_A: (5,17)->(5,16),
    beta_B: (5,19)->(5,20),
    beta_D: (5,4)->(5,3).

Declare the local owners to be A,B,C,D,g0,...,g3 and any chosen subset of
these three whole betas. Keep ALL original links among the declared owners
and precisely the original intervals p,z. Their beta bodies have empty
support in this pool, no source has direct support, and no designated
gate reaches one of these betas. Thus this is an actual original induced
owner interface satisfying Section 1, not an invented incidence table.
It omits other original owners; it is explicitly NOT the complete board.

Allowing beta_A and beta_B gives E={A,B}. Its gaps are {g1} and
{g0,g2,g3}. Both resource trees meet only the second gap. For X={T0,T1},

    |X|=2 > 1=|N_K(X)|.

Both beta identities are different, but full payment is impossible. More
directly, C and D cannot reach p through an allowed gate, so they compete
for the single original z. Their combined payment is at most one. The
packing A->beta_A, B->g1->p, C->g2->z attains value3.

Each beta alone raises interval value2 to3. Together they STILL give3:
adding their separate gains would double-count a gain at the coupled
source/gate interface, despite using different beta and interval identities.

If beta_D is also allowed, choose E={A,D} instead. The two gaps are {g0}
and {g1,g2,g3}; match T0 to the first and T1 to the second. Pay A,D by
their different beta stems, B->g1->p and C->g2->z. Full value4 is attained
with two beta payments. The pair B,D works too. Thus the successful pair
uses the newly available beta and reassigns an earlier beta-paid source
back to a gate. Every payment uses one link,
so the minimum link cost equals value in all eight beta-availability cases:

| Available whole betas in declared interface | V / minimum links |
| --- | --- |
| none | 2 / 2 |
| any one of A,B,D | 3 / 3 |
| A,B | 3 / 3 |
| A,D or B,D | 4 / 4 |
| all three | 4 / 4 |

The full original network with p,z available still has V4/c4, as proved
in the preceding note; none of its six original betas is discarded in
that comparison. The two-beta witness above is also legal there. This
does NOT refute a theorem that all original peripheral exits collectively
suffice. It refutes counting each distinct available beta as one freely
placeable repair of an interval-tree deficit.

**Arbitrary separated copies, with exact nonreuse.** Place copy i at row
offset 32i+2 in a32q-by24 board, as in the preceding note. Even blank
buffers separate original strands, support and links and retain band
phase. Replay each copy's strict freezing certificate. Keep its p,z and
the same declared cycle owners. Let E_A,E_B,E_D be the copy sets in which
the corresponding whole beta is allowed. The eight-case classification
above, and disjoint actual owner/unit identities between copies, give

    V_local = 2q + |E_A union E_B union E_D|
                   + |E_D intersect (E_A union E_B)|,
    c_local = V_local.                                      (4)

In particular with no D exits, 2q DIFFERENT beta resources (A and B in
every copy) add only q payments. With D available, it is the displayed
intersection that permits a second payment in the same copy. This is a
general proof by the local upper bound and simultaneous separated lift,
not by finitely many q. The COMPLETE original copies with these same p,z
still have V4q/c4q, retaining every original beta.

## 5. Verification and formal scope

The checker `develop/check_cyclic_beta_escape_cuts.py` reconstructs the
unchanged actual freezing certificate and the exact induced owner interface.
Abstract controls compare (1)--(2) with independent primitive packing,
including shared betas, isolated gates, loops and parallel intervals.
Weighted controls check (3) against direct route enumeration for a fixed
beta matching. Finite controls corroborate the proofs; they do not replace
them. The receipt records the exact tested counts.

`formal/SubQuorum/CyclicBetaEscapeCuts.lean` proves the arbitrary-length
gap matching construction (legality, root exclusion, injectivity and full
coverage), the no-reuse composition with interval/beta assignments, the
tree-to-gap injection extracted from unused roots, and the four-source
shared-z obstruction. The graph component decomposition, tree rank,
Hall theorem, cost minimization, physical adapter and complete original
flow remain written/Python. The previous actual308-endpoint Lean
certificate is reused unchanged; it is not newly rerun or relabeled.
Pruning the cyclic cut set and the cost identities have written proofs
and Python checks; they are not yet Lean theorems.

The remaining geometric question is now sharper: for the complete original
network, what supplies the required joint tree/gap Hall expansion after
beta choices? Distinct whole-beta counts and individual repairs do not
establish it. Shared entry chains, gate-to-gate continuations and beta-body
forks outside this interface still require the full original flow model.
The submitted manuscript, public main and unrestricted5/6 bound are unchanged.
