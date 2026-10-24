# Joint whole-support interval and whole-beta compensation

The later [whole-support stem/fork normal form](WHOLE_SUPPORT_FORK_NORMAL_FORM.md)
allows general mixed continuation and beta-body interval witnesses. Two arms
can consume one beta and use a distinct interval in its support; an exact
fork-packing/residual-flow formula handles this larger interface. This note's
direct one-alpha/one-beta restriction and its exact formula remain as stated.

## Status and purpose

This note proves an exact direct-compensation theorem after an arbitrary fixed
cancellation. It combines the whole-support interval model of
[the full-gap obstruction note](BOUNDARY_SEALED_GAP_OBSTRUCTION.md) with **whole
current virtual beta resources**. The additional beta is chosen before the
interval tree is rooted. Consequently the construction preserves every
previously paid demand and the entire set of used original interval identities.
It also has an exact minimum-change version.

The earlier [grouped beta-reserve route theorem](COMPONENT_ROUTE_CERTIFICATES_AND_GROUPED_BETA_RESERVES.md)
already uses a k-t+mu formula for first-witness alpha/beta **path components**.
Here the components are arbitrary deficient **interval-resource trees** after
C0, and whole current betas supply the exterior units. This extends the
root-after-resource method to that different support incidence; it does not
relabel the earlier cardinality formula as a new general principle. The
minimum-disturbance formula adds a baseline-dependent optimization statement.

The matching and tree-orientation ingredients are standard. The contribution
here is their explicit ownership-preserving adapter to this compensation
problem, including the physical cancellation lift and a quantified rerooting
cost. This is not a claim of a new general matching theorem. It does not yet
establish a universal improvement of the grid's 5/6 bound.

## 1. Hypotheses and units

Subsequent result: [safe beta closing](BETA_CLOSING_AND_SHARP_MIXED_DEFECT.md)
now realizes arbitrarily large positive t-mu in completely frozen physical
grids, stable under blank right padding. Thus a universal direct-beta Hall
saturation theorem under feasibility/freezing alone is false. This exact
joint allocation theorem remains valid; mixed continuation repairs the
constructed family, and general mixed compensation is still open.

Subsequent physical result: [a frozen two-vertex support tree](FROZEN_SUPPORT_TREE_AND_FORCED_REROOT.md)
now realizes positive reroot cost at a specified maximum baseline, with an
all-q disjoint physical stacking proof. It also exhibits a wider mixed repair
and verifies that blank right padding releases its marked exits. The zero
nonsingleton count in Section 6 describes this note's original controls only.

Fix a valid horizontal cancellation matching C0. Its virtual strands have
pairwise disjoint supports. Let A be its k virtual alpha strands and B its b
virtual beta strands. Each **whole current beta** supplies one unit, regardless
of its two free BP tips or the number of original strands inside it. Previously
consumed beta resources are already part of C0 and are unavailable.

Let I be the finite set of available **original unmarked interval units**.
Keep the original identities, including when the same interval is seen from
both sides. An incidence relation E assigns each j in I to at most two eligible
owners in A. In the physical adapter, eligibility means that a P column in the
owner's entire original-strand support bounds the endpoint-free gap containing
j. The proof in the preceding note supplies the two-owner bound. Intervals
with zero owners remain in I as unused resources.

For each a in A and beta in B, retain every permitted **direct free-tip link**
from a TP of a to a BP of beta. Write a ~ beta if at least one such link exists,
and retain a concrete witness. Each permitted link avoids C0. Distinct alpha
owners and distinct beta owners have disjoint supports, so choices for disjoint
owner pairs have no common endpoint. The additional cancellation C1 is
restricted to such owner-disjoint alpha--beta links. Mixed relays, links between
two selected alpha owners, and sequential consumption of multiple resources
inside a beta are outside this theorem.

A joint allocation assigns each paid alpha either one eligible original interval
or one adjacent whole beta. Every resource is used at most once and each alpha
is paid at most once. Beta payments are realized by their retained direct links.
Interval payments are a **counting interface**; no terminal-route realization is
asserted for internal PP support access.

## 2. The deficient-tree graph

Make a multigraph on A: a two-owner interval is one edge, and a single-owner
interval is one private resource attached to its owner. Parallel edges retain
distinct identities. A component is *deficient* precisely when its edge graph
is a tree and it has no private resource; an isolated alpha with no resources is
a deficient singleton tree. Let its deficient components be T1,...,Tt.

Each deficient tree with n vertices has exactly n-1 interval resources. It can
pay every vertex except any prescribed root: give each other vertex the edge
toward that root. This allocation is unique, by deleting leaves other than the
root successively. Each nondeficient component can pay all its vertices: use a
private resource as root anchor, or an edge outside a spanning tree as anchor
and orient the remaining spanning tree away from an endpoint of that edge.
Thus the maximum interval-only payment is k-t. In every maximum interval-only
allocation, each deficient tree omits exactly one vertex, uses all its edges,
and every nondeficient component is fully paid.

Make a bipartite graph H whose left vertices are the deficient trees and whose
right vertices are **whole current betas**. Join T to beta exactly when some
a in T has a witnessed direct free-tip link to beta. Let mu be the maximum
matching size in H.

**Theorem 1 (exact joint compensation).** Under the hypotheses in Section 1,

    maximum paid alpha demands = k-t+mu,
    minimum remaining deficit  = t-mu.

Among allocations attaining this maximum, the smallest number of extra beta
links is exactly mu. Starting from any maximum interval-only allocation, an
optimum exists that keeps every previously paid demand paid and keeps exactly
the same set of original interval resources in use.

**Proof.** Choose a maximum matching in H. For each matched pair (T,beta), choose
a witnessed alpha a in T, link a to beta, and root the interval tree at a. Then
beta pays a and the n-1 tree edges pay every other vertex. Different matched
trees and betas have disjoint owners, so these links are a matching and no beta
is reused. Distinct interval components have disjoint original edge resources.

In unmatched deficient trees retain the baseline allocation, and in every
nondeficient component retain it as well. In a matched tree both allocations use
all n-1 of the same original interval units, and all n demands become paid.
This constructs k-t+mu payments using exactly mu beta links and proves both
preservation statements. The new alpha paid by intervals need not be the alpha
that was previously unpaid: this is why fixing the old root would be invalid.

Conversely, suppose an arbitrary joint allocation fully pays f deficient trees.
Each such tree needs at least one beta: it has only n-1 eligible interval units,
and no interval resource crosses an interval-graph component. Choose a used beta
from each fully paid tree. Chosen betas are distinct and witness a matching in
H, so f <= mu. Every other deficient tree leaves at least one demand unpaid.
Hence at most k-t+mu demands are paid. Moreover, an allocation using l beta
payments uses at most k-t interval payments, so reaching k-t+mu requires l >= mu.
The construction attains equality. QED.

Equivalently, the residual defect is the Hall deficiency

    t-mu = max over X subset {T1,...,Tt} of (|X|-|N_H(X)|).

For completeness, the lower bound follows because at most |N_H(X)| trees in X
can be matched. For the reverse bound, start alternating searches from all
unmatched left vertices of a maximum matching. No unmatched beta is reachable,
or its alternating path augments the matching. If X is the reached left set,
its neighbor set is exactly the reached right set; each reached right vertex is
matched to a reached left vertex, and each reached matched left vertex is
reached through that matched right vertex. Thus |X|-|N_H(X)| equals the number
of unmatched left vertices, t-mu. If all left vertices are matched use X empty.

## 3. Physical lift and unchanged ledger

For a selected alpha--beta pair, gluing their free TP and BP tips leaves one TP
tip and one BP tip: the two owners become one mixed virtual strand. Different
selected pairs cannot interact because their supports are disjoint. All other
alpha supports and all links of C0 remain unchanged. In particular, every
interval assignment constructed above belongs to an unselected alpha, whose
original support witness is retained after C0+C1. Counts become

    alpha_new = k-mu,  beta_new = b-mu.

If U is the number of unused original interval units in the baseline, the
original packet identity gives

    S-Boundary = |I|+b-k = U+b-t
               = U+(b-mu)-(t-mu).

The construction does not turn consumption into new surplus; it removes one
alpha demand and one beta resource simultaneously. If H saturates all deficient
trees, the nonnegative remaining resources certify S >= Boundary. If it does
not, the scalar inequality may still hold because U and unused betas can exceed
the residual defect. This theorem decreases the *certified direct compensation
defect* by exactly mu, not the universal 5/6 constant by a numerical amount.

A simple sufficient condition is useful when geometric incidence is known:
if each deficient tree sees at least r distinct whole betas and each beta sees
at most r deficient trees, r >= 1, then r|X| <= r|N_H(X)| for every X, so mu=t.
For the direct along-band grid interface each beta has two free BP tips, each
with at most two neighboring TP positions; hence it sees at most four deficient
trees. Four distinct beta neighbors per deficient tree therefore suffice.
Freezing alone has not been shown to supply that lower degree condition.

## 4. Exact weighted rerooting

Fix any maximum interval-only baseline. Let r_T be its unique unpaid root in
each deficient tree. For a candidate beta define

    w(T,beta) = min distance_T(r_T,a)

over the alphas a in T with a witnessed link to beta. These are distances in the
tree of **original interval units**, not geometric distances or link counts.

**Theorem 2 (minimum disturbance).** Lexicographically optimize (i) number of
paid demands, (ii) number of beta links, then (iii) number of *previously
interval-paid owners whose interval assignment changes*, including an owner
which switches to beta payment. The first optimum is k-t+mu, the second is mu,
and the third is the minimum total weight of a cardinality-mu matching in H.
The preservation guarantees of Theorem 1 hold at this optimum.

**Proof.** In a tree, moving the omitted root from r to a reverses exactly the
unique r--a path; assignments off the path stay fixed. Write the path as
v0=r,v1,...,vd=a, with distinct original edges e1,...,ed. Initially vi uses ei
for 1<=i<=d. Afterwards vi uses e(i+1) for 0<=i<d, and vd uses beta.
Consequently each of the d previously interval-paid path owners changes its
assignment, every other previously paid owner keeps it, and the original used
edge set is identical. If d=0 no old assignment changes.

Any maximum joint allocation fully pays at least mu deficient trees, by the
upper-bound argument of Theorem 1. If it uses exactly mu betas, exactly mu
deficient trees are fully paid, each gets exactly one beta, and no beta is spent
elsewhere. After the beta-paid vertex a is fixed, the remaining n-1 demands in
its tree must use all n-1 edges, in the unique tree allocation rooted at a.
Thus its change count is exactly distance_T(r_T,a), at least w(T,beta).
The chosen tree--beta pairs form a cardinality-mu matching. Other components
cannot contribute a negative change count. This proves the lower bound; choose
the minimizing roots of a minimum-weight maximum matching and leave all other
components unchanged to attain it. QED.

On an abstract path of n vertices whose only beta adjacency is its endpoint
opposite the old root, the forced disturbance is n-1, even though there is only
one extra beta link. This distinguishes assignment disturbance from link cost.
No arbitrarily long *frozen physical* realization of this example is claimed.

Already with two demands 0,1, one interval adjacent to both, and one beta
adjacent only to 1, fixing the baseline root gives a false obstruction. If the
baseline assigns the interval to 1, its unpaid root 0 sees no beta. Reassign
the same interval to 0 and let beta pay 1; both are paid, with exactly one old
assignment changed. Testing beta access only at the currently unpaid vertex
therefore loses valid compensation.

## 5. Why independent component credits fail

Two deficient trees can each see the same beta. For instance take demand trees
{0,1} and {2,3}, interval units {0,1} and {2,3}, and one beta adjacent to demands
1 and 3. Each tree separately has a beta repair, but both cannot use it: t=2,
mu=1, and exactly one demand remains unpaid. This abstract example refutes
independent reuse of the beta credit, not the scalar inequality or a claimed
frozen grid construction. H retains the whole beta identity precisely to
exclude this mistake.

In the previously archived **actual frozen unported shared-gate fixture**
(unreflected, padded by (2,2)), k=2,b=5,t=2,U=187, and the packet margin is 190.
Its two deficient singleton trees have distinct directly available whole-beta
resources, so mu=2. The construction pays both by two disjoint physical links,
with no change to original interval use. This repairs the interval-only failure
from the preceding note. It does not prove that all frozen deficient trees have
such beta matchings.

## 6. Reproduction and formal scope

Run from the research root:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 develop/check_joint_tree_beta_compensation.py \
  --output output/joint-tree-beta-validation.json
PYTHONDONTWRITEBYTECODE=1 python3 develop/check_joint_tree_beta_formal.py \
  --lean /path/to/lean --output output/joint-tree-beta-lean-validation.json
```

The checker compares the tree construction with a separate flat allocation to
typed interval/beta resources, using successive shortest augmenting paths. For
the three priorities, a beta edge has cost k+1, a retained old interval edge has
cost -1, and every other interval edge has cost zero. Maximum flow is optimized
first. Since at most k old assignments can be retained, the cost then minimizes
beta links before assignment disturbance. Small cases additionally enumerate
all flat allocations and **all maximum interval-only baselines** independently.
Physical checks actually execute C0+C1, recompile the support model, and check
original witness strands and interval eligibility of every retained payment.

The saved run has 5,413 exhaustive flat comparisons over all small maximum
baselines, 7,544 independent flat min-cost comparisons, 751 positive reroot
controls, and path disturbances up to 39. It checks 491 fixed-C0 lifts over
25 frozen geometric packets, with 56 repaired-tree occurrences. These physical
controls contain **no nonsingleton deficient support trees and no positive
reroot cost**; those mechanisms are checked in general abstract models and
proved above, not exhibited as new frozen geometric families.

The Lean module checks the arbitrary-length simple-path reassignment mechanism,
injectivity and preservation of indexed resource identities, and the arithmetic
ledger, with 14 theorem axiom audits and no warnings, sorry or native evaluation.
Its resource-set statement uses the explicit fixed edge-index domain; it does
not infer the ambient tree decomposition. The general tree decomposition,
matching optimality, unique tree-root
allocation, whole-support physical adapter and weighted optimum are written
proofs with computational regression checks, not claimed as fully formalized.

## 7. Remaining research question

The unresolved geometric step is now precise: can freezing force Hall expansion
for the **deficient support-tree / whole-beta graph**, or can a frozen graph
violate it? A violation only obstructs this direct interface; one must separately
check mixed relays and the scalar ledger. The strongest next test is a frozen
nonsingleton deficient support tree with a beta attached away from its omitted
root, or two such trees competing for one whole beta. Neither exists among the
physical controls reported here. Keep this open instead of inferring expansion
from the abstract allocation theorem.
