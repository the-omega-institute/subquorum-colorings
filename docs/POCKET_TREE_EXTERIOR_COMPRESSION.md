# Filled pocket trees: exact exterior compression, cuts and link costs

25 October 2026. Haobo Ma and Wenlin Zhang. Research branch only.

The preceding [shared-pocket theorem](SHARED_POCKET_COMPLETION_AND_JOINT_DEFICIT.md)
counts one deficiency per all-filled tree in the pocket-only interface. We
now retain the **entire exterior** whole-support system, including shared
mixed gates, both physical beta entry gates and beta-body interval support.
Every such tree reduces to one residual source with a choice of its original
alpha exits. This preserves maximum payment exactly. It also preserves
minimum link cost, after adding the internal baseline, if all tree alphas
have empty direct interval support. Without that assumption the same
cardinality reduction can overestimate cost even on a completely frozen
board; a discounted circulation gives the exact general cost instead.

This is a structural application of tree allocation and standard integral
flow/circulation theory. It proves no new general network theorem and does
not establish universal geometric saturation or improve 5/6. Its purpose
is to replace many individual path deficits by the correct jointly
capacitated exterior problem, without presuming different exits are free.

## 1. Hypotheses and original identities

Use the complete finite whole-support model and network of
[WHOLE_SUPPORT_FORK_FLOW_AND_RESOURCE_CUTS.md](WHOLE_SUPPORT_FORK_FLOW_AND_RESOURCE_CUTS.md).
An alpha is a unit source with two TP tips, a mixed owner has one capacity-one
gate, each beta has two separate actual BP entry gates and one whole-beta
sink, and every available original interval has one global sink capacity.
The declared TP--BP links have unit link cost. Interval support arcs cost zero.

Select pairwise disjoint nonempty sets D_i of original alpha owners.
For each i, specify a tree H_i on D_i and a different original beta E_e
for every tree edge e=ab. Require:

1. W(E_e) is empty: the internal beta has no original interval support.
2. The only declared links entering E_e are one direct link from a and
   one from b, using its two different actual BP tips.
3. All internal betas are different across all trees. No alpha belongs
   to two D_i.

Singleton trees, having no internal beta, are permitted. A family of
vertex-disjoint filled guarded pockets on different alpha owners supplies
these hypotheses by the preceding geometric dichotomy. Once established,
the reduction uses the strand model and does not need a new freezing
assumption. We make no frozen realization claim for arbitrary H_i.

Call all remaining betas, mixed owners, intervals, links and alpha owners
**exterior**. This includes the direct interval supports W(a) of a in D_i
and all its links to noninternal owners. Different trees may share these
exterior targets and relays. We do not remove these conflicts.

Write n_i=|D_i|, g=number of trees, p=number of outside alpha sources, and

    B=sum_i(n_i-1),       total original alpha count=B+g+p.

The internal resources are actual whole beta identities, not their two
BP ports counted separately. All exterior intervals keep their original
identities and all exterior owner supports remain unchanged.

## 2. A tree with a prescribed set of exterior representatives

**Lemma 1 (multiple exterior roots).** Let X subset D_i be the distinct
alpha owners paid by exterior routes, x=|X|. The remaining internal tree
can pay exactly

    n_i-max(1,x)

additional alpha sources by that many direct one-link internal beta stems.
If X is nonempty, all n_i sources are paid. If X is empty, exactly one
chosen root remains unpaid.

**Proof.** If X is nonempty, run multi-source BFS in H_i from all vertices
of X. Give every other vertex its parent-edge beta through its declared
incoming link. Distances decrease toward a root, so two vertices cannot
spend the same parent edge. Every selected stem has one different alpha
source and one different whole beta. The exterior sources are not used
again. This gives n_i-x internal payments, the maximum allowed by the
number of unspent sources. If X is empty, root the tree at any vertex and
give every nonroot its parent-edge beta. There are n_i-1 betas in total,
so n_i-1 is both achievable and optimal. QED.

These internal stems are compatible with every exterior certificate:
outside routes cannot enter an internal beta by hypothesis 2, and cannot
enter an alpha owner, which has no BP tip. Internal betas have no fork
resource because W(E_e) is empty. This is an availability proof, not an
assumption that a formerly used beta is free.

## 3. One grouped residual source per tree

Delete the internal beta nodes and their incoming links. For every tree,
replace its n_i source arcs by one source arc s->G_i of capacity one.
Join G_i to every original alpha exit a in D_i by a zero-cost choice arc.
Retain the alpha exits themselves and every exterior link/support arc.
Keep the p outside source arcs and every exterior mixed gate, actual BP
entry, whole-beta sink and original interval sink exactly as before.
Choice arcs may have unit capacity; the group source already limits total
flow to one. This is a network reduction, not a claim that G_i is a new
physical TP--TP path.

Let R be the maximum flow value in this exterior grouped network and d
its minimum link cost at value R. The maximum original payment is V.

**Theorem 2 (exact cardinality compression).**

    V=B+R,       original deficit=(g+p)-R.                (1)

The statement permits arbitrary direct supports W(a), arbitrary exterior
mixed sharing and arbitrary exterior beta forks.

**Proof, lift.** A grouped unit selects one original alpha exit in its
tree and follows an exterior route. Normalize exterior beta outputs to
spend the whole-beta unit first. Then lift the flow to ordinary stems and
beta forks using the established full-network equivalence. Apply Lemma 1
inside each tree, using its representative as root when paid and any
unpaid root otherwise. The trees contribute their B baseline payments
plus one per active group; outside paths contribute one per paid outside
source. All owners and resources are disjoint where required. This gives
B+R original payments, at cost B+d.

**Proof, project.** In any original primitive packing, distinguish direct
stems ending at internal betas from exterior source paths. There are no
other uses of internal betas, by hypotheses 1--2. Let X_i be its exterior
source set in D_i. The tree's total paid-source count is at most
n_i-1+1_(X_i nonempty): with no exterior path it has only n_i-1 internal
resources; with one or more it still has only n_i sources.

Keep one exterior path per nonempty X_i, delete the others, and keep all
paid outside-source paths. This only releases mixed gates, BP entries and
interval capacities. If deletion removes one fork arm, redirect the
remaining arm to that beta's whole unit; the established normalization
preserves that remaining source and its links, releasing an interval.
The retained paths are a feasible grouped flow. If h is their count, the
original payment is at most B+h<=B+R. This proves (1). QED.

The projection retains every paid **outside** source identity. It can
change which tree alpha uses the exterior route. If particular outside
sources must remain paid, retain that constraint as lower bounds on their
source arcs; the same projection/lift argument applies to that constrained
problem. Unconstrained maximization alone does not promise to keep a
previously selected outside-source set.

For a set Z of exterior capacity-one mixed/BP/beta/interval gates, let U_Z
be the grouped and outside sources with no surviving sink route after
deleting Z. Standard min-cut duality in the reduced network gives

    original deficit = max_Z (|U_Z|-|Z|).                 (2)

Choose the choice/link/support capacities larger than g+p for this cut
description; they can never cross a minimum cut. The unit source groups
still choose one alpha representative. Formula (2) counts every shared
gate and resource once. Thus proving all residual groups individually
reach some exterior resource is insufficient; the remaining geometric
task is the joint cut inequality |U_Z|<=|Z| for every Z.

## 4. Exact cost when tree alphas are unsupported

**Theorem 3.** In addition to hypotheses 1--3, suppose

    W(a)=empty for every a in every D_i.

Then the original minimum link cost c at value V satisfies

    c=B+d.                                                (3)

There is an optimum in which at most one source per tree is paid by an
exterior route. This does not assert that every optimum has that form.

**Proof.** The lift in Theorem 2 proves c<=B+d. Take a minimum-cost
original maximum packing and write x_i=|X_i| for its exterior source
counts. Each tree's internal payments must attain Lemma 1's maximum:
otherwise internal rerouting would increase payment without altering any
exterior route, contradicting maximality. When x_i>0 it therefore uses
exactly n_i-x_i one-link internal stems.

Every exterior path starting at one of these unsupported alpha sources
contains at least one actual link. Keep any one of its x_i exterior paths
and delete the other x_i-1. Reroot the tree at the retained representative
and replace its old n_i-x_i internal stems by n_i-1 internal stems.
This adds x_i-1 internal links and deletes at least x_i-1 exterior links.
All tree sources stay paid, every outside source stays paid, and cost
does not increase. Fork normalization after deleted arms is free as in
Theorem 2. Do this in every tree. The new exterior flow has value R,
and internal cost B, so d<=c-B. Combining both bounds proves (3). QED.

This is the point at which empty direct support is used. Individual
external routes may be arbitrarily long, and may share candidate mixed
owners or resources; only the selected compatible paths are pruned.

## 5. General exact cost with direct supports retained

Without Theorem 3's support assumption, Theorem 2 still gives V=B+R and
the upper bound c<=B+d, but its cost equality can fail. Several direct
zero-link exterior payments can beat replacing all but one with local
one-link stems.

There is nevertheless an exact, finite-size cost reduction. Let L be the
number of distinct declared links, including internal links, and put
M=L+B+1. Use the exterior network from Section 3, but for each tree use
two parallel s->G_i arcs:

* first arc: capacity one, cost -M;
* extra arc: capacity n_i-1, cost -1.

The arcs G_i->a have capacity one for every a in D_i. Give every outside
source arc capacity one and cost -M. Exterior links retain cost one and
all other exterior arcs cost zero. Add t->s of capacity equal to the
total original source count and cost zero, and minimize integral
circulation cost. This optional-flow circulation can be computed by
successive minimum-cost s-t augmentations while their cost is negative.

For a circulation let x_i be its number of exterior paths from tree i,
h the number of active groups plus paid outside sources, and ell its
exterior link count. At an optimum the first group arc is used before
the extra arc. Lemma 1 and the retained actual capacities give the exact
lifted payment and cost

    payment=B+h,
    cost=B+ell-sum_i(max(0,x_i-1)).                        (4)

The variable part Delta=ell-sum_i(max(0,x_i-1)) lies in [-B,L]: no link
can be selected twice, and the total extra-exit count is at most B. The
circulation objective is exactly

    -M*h + Delta.                                        (5)

Since M>L+B, improving h by one strictly beats every possible change in
Delta. It therefore maximizes original payment first and minimizes the
actual original link cost second. If Q* is its optimum objective and
h*=R its optimal coverage, the exact cost is

    c=B+Q*+M*R.                                          (6)

**Proof of exactness.** Every exterior flow lifts by Lemma 1 with exactly
(4), preserving all capacities. Conversely any maximum original packing
must pay the maximum possible internal sources for its exterior sets X_i,
or could be augmented internally. Its internal stems therefore number
n_i-max(1,x_i), and its exterior flow has exactly the payment/cost (4).
Exterior beta normalization leaves links unchanged, so forks do not change
this accounting. The two directions give equality of feasible maximum
payment/minimum-cost optima. The bound on Delta proves the lexicographic
claim and (6). QED.

The discount -1 accounts for a specific internal link no longer needed;
it is not an additional beta credit or a negative physical link length.
No new original interval or resource is created. The existing full-flow
solver is not modified by this auxiliary optimization.

## 6. Frozen controls and a joint exterior obstruction

Apply the reduction to the **filled** pockets in each of the two actual
frozen families from the preceding note. An unfilled copy's two original
alpha sources remain ordinary outside sources. Write f=|S| for the number
of filled copies, so B=f.

| Frozen family, q copies | Original V,c | Grouped R,d | B+d | Exact discounted c |
|---|---|---|---|---|
| Tight unsupported alphas | 2q, 2f | 2q-f, f | 2f | 2f |
| Alphas with outside intervals | 2q, 0 | 2q-f, 0 | f | 0 |

These are all-q formulas, by the earlier explicit exterior interval/beta
witnesses, the unsupported-source lower bound and separated copies.
In the second row, each filled tree optimally uses **two** zero-link
exterior representatives, saving its internal baseline link. Thus a
completely frozen board refutes dropping Theorem 3's support hypothesis.
The discounted circulation records exactly f extra exits and cost zero.

For a simple abstract joint obstruction, take two two-source trees, each
with its own one internal beta. Give one source from each tree a link
to a different BP tip of the **same** exterior beta, with empty beta-body
support. Each residual tree individually has an exit, but there is only
one exterior whole-beta unit: R=1, B=2, V=3 rather than four. Adding one
different original interval supported by the exterior beta repairs the
deficit through a genuine two-entry fork: R=2, V=4, c=4. The reduction
retains this fork and never turns the two BP gates into two beta units.
This control is abstract, not a new frozen counterexample to the target.

## 7. Verification and remaining geometric obligation

`develop/check_pocket_tree_exterior_compression.py` leaves prior solvers
unchanged. It checks the three tree-interface hypotheses, computes both
reductions, verifies original edge capacities and vertex balances, constructs
the internal parent-beta payments, checks physical terminal uniqueness,
and evaluates the lifted actual links in the original model. Its ordinary
grouped exterior flow has a checked cut capacity. The discounted computation
checks the exact cost identity and absence of negative residual cycles.

There are 866 controls: 600 seeded general systems, two named joint-beta
controls, and 264 completely frozen physical boards. All 866 compare the
full original optimum to both reductions, giving 1,732 checked flow lifts;
285 also compare an independent primitive packing optimizer. The simple
cost formula passes 530 unsupported controls, and 164 models have a strict
simple-cost overestimate corrected by multiple exterior exits. The physical
checks include all fill subsets through five copies and further controls
through twelve. Finite checks validate the implementation; Sections 2--5
give the general proofs.

`formal/SubQuorum/PocketTreeExteriorCompression.lean`, Lean 4.33.0, checks
four scoped declarations: sum of positive route lengths, cost-safe pruning
to one exterior representative, the exact local payment/savings ledger,
and the reward bound that enforces the lexicographic objective. Earlier
`SharedPocketJointDeficit.lean` checks the parent-edge nonreuse mechanism.
The tree allocation geometry, full-network projection/lift, and min-cost
circulation theorem remain written arguments; no full formalization is
claimed. The Lean source uses no sorry or native evaluation. No new
independent external review is claimed.

The remaining research target is now precise: after private-source
elimination and tree compression, prove from complete frozen geometry that
every exterior separator Z blocks at most |Z| grouped/outside sources, or
exhibit a genuine geometric obstruction to a proposed stronger rule.
Individual reachability, distinct BP tips, or a positive scalar reserve
count cannot replace that joint gate/resource inequality. Universal
compensation and improvement of the 5/6 bound remain open.

Continuation: [forced pocket guards and cyclic-block elimination](FORCED_POCKET_GUARDS_AND_CYCLE_ELIMINATION.md)
proves that every short beta between alpha TP tips already has the required
PP guards in a completely frozen board. Construct the complete recognized
resource multigraph and eliminate its non-tree components before compressing
the remaining trees. In particular, the tight completed fixture has an older
second beta joining the same two alphas; considering both edges eliminates
the closed two-source component. The tree compression theorem above remains
valid when only one of those edges is selected for compression.

The subsequent [short-beta deletion obstruction](SHORT_BETA_DELETION_AND_FREEZING_OBSTRUCTION.md)
also shows that geometric deletion need not preserve complete freezing.
The reduced network above is an algebraic system retaining original resource
identities; further geometric estimates must use the original frozen board,
unless a separate preservation or repair theorem is supplied.

Continuation: [joint interval/beta block reduction](JOINT_INTERVAL_BETA_BLOCK_REDUCTION.md)
combines original source-only intervals and exclusive betas. Exact discounts
count distinct interval components (only deficient ones in saturated blocks),
retaining the full exterior and both value and minimum-link cost. It is an
algebraic reduction on the original board; universal compensation remains open.
