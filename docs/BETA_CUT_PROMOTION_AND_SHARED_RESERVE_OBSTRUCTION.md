# Beta-body promotion, surplus Hall witnesses and shared reserve

**Continuation:** [actual simultaneous release](SIMULTANEOUS_INTERVAL_RELEASE_AND_PHYSICAL_CIRCUITS.md)
distinguishes individually releasable far-side witnesses from jointly unused
resources, with an exact all-cut criterion and real frozen-board obstructions.

25 October 2026. Haobo Ma and Wenlin Zhang. Research branch only.

We sharpen the BP-aware flow separator with a simultaneous beta-body
promotion inequality. In the largest-source-side minimum cut, double-entry
beta receivers have surplus Hall neighborhoods among the far-side original
intervals: every nonempty set has at least one more neighbor than receiver.
They can be matched to different intervals even after deleting any one
interval. Shared interval identities are counted by their union, never once
per beta.

These witnesses are not necessarily unused reserve. An all-q abstract family
has q double-entry beta receivers, deletion-robust matching witnesses, and
only one globally unused interval. Thus the inference of one new reserve
per receiver is false, even with at most two owners per interval. This
refutes that inference, not the numerical grid target.

We also exhaust a specific finite physical frontier: four matchings on the
base 66 endpoints, extended by at most two added selections or matching
edges. Of 25,004 disjoint edit sets, 6136 yield fully frozen feasible boards.
Every one has full compensation and no value/cost advantage over ordinary
flow. This is finite evidence only; it does not prove a general geometric
cut bound.

## 1. Canonical minimum cut

Use the [complete whole-support fork network](WHOLE_SUPPORT_FORK_FLOW_AND_RESOURCE_CUTS.md).
Let S be the largest source side among minimum s--t cuts. It exists: minimum
cut source sides are closed under union. Equivalently, for any maximum flow,
S is the complement of the vertices that can reach t in its residual network.

For completeness, no residual edge exits this complement, so its cut has
capacity equal to the maximum flow value. For any other minimum cut, no
residual edge exits its source side either. A vertex in that source side
cannot reach t residually; thus the other side is contained in S. This
also proves uniqueness and the residual characterization.

For each beta body b outside S, let r_b count its BP entry gates crossing
from S into b. There are two actual gates, so r_b is 0, 1 or 2. Put

    R = {b outside S : r_b>0},
    D = {b in R : r_b=2},
    I_S = {original intervals with their nodes in S},
    J_b = W(b) minus I_S.

The set J_b consists of available original interval identities on the far
side of this cut. It does not mean unused intervals of the chosen packing.
We count the beta's private sink separately from both BP entry capacities.

## 2. Simultaneous promotion, with shared intervals counted once

**Theorem 1 (strict joint promotion).** For every nonempty Q subset R,

    |union_(b in Q) J_b| >= |Q intersect D|+1.                (1)

No two-owner condition or physical freezing assumption is required.

**Proof.** Add to S all the beta body nodes in Q, and every interval node
in N(Q)=union_(b in Q)J_b. Source/sink membership stays unchanged. The
support arcs of the promoted bodies now end inside the enlarged source
side; no large support arc crosses. Incoming edges from other outside
nodes into these new source-side nodes do not add cut capacity.

The removed cut edges are exactly the r_b old entry gates for each b in Q.
The new edges are one private whole-beta sink per promoted body and one
interval sink per DIFFERENT interval in N(Q). Their cut-capacity change is

    Delta = |Q| + |N(Q)| - sum_(b in Q) r_b
          = |N(Q)| - |Q intersect D|.                        (2)

There are no other outgoing edges from beta bodies or interval nodes.
In particular a unit shared by several beta supports is charged once.
Minimum cut optimality gives Delta>=0. Equality would produce another
minimum cut with a strictly larger source side, since Q is nonempty and
its bodies were outside S. This contradicts maximality of S. The integer
Delta is therefore at least one, proving (1). ∎

For an arbitrary minimum cut, the same argument only gives the nonstrict
bound without +1. Choosing the largest source side is essential for the
stated surplus, rather than a cosmetic tie rule. It changes neither the
maximum payment nor the minimum link cost of the flow.

**Corollary 2 (deletion-robust Hall witnesses).** The double-entry receivers
D have an injective assignment to supporting far-side intervals. Such an
assignment still exists after any one original interval is removed from
the possible targets.

**Proof.** Apply (1) to every nonempty Q subset D: |N(Q)|>=|Q|+1.
Deleting one target reduces every neighborhood by at most one. Hall's
theorem gives a matching saturating D, with or without the deletion. ∎

In particular a beta with two cut BP entries has at least two supported
intervals outside S. If it has at most one, its body cannot be left on
the far side in this canonical minimum cut. A beta with one cut entry
must have at least one supported far-side interval. These statements locate
entry obstructions; neither converts the witnesses into new payment units.

## 3. A two-owner graph characterization

Assume every original interval has at most two current owners, as in the
physical whole-support adapter. Restrict to D and its far-side intervals.
Represent a unit incident to two beta receivers by an edge and a unit
incident to one by a private resource. Here private means relative to D,
not necessarily private in the full physical system.

**Proposition 3.** Surplus Hall, |N(Q)|>=|Q|+1 for all nonempty Q subset D,
is equivalent to both:

(a) every receiver is incident to at least two different resources;

(b) no connected component is a pure cycle with no private resource,
including a two-vertex cycle made of parallel resource edges.

**Proof.** Surplus Hall gives (a) on singletons and rules out a pure cycle
by taking its entire vertex set. Conversely consider a component with n
vertices, e internal edge resources and p private resources. Condition (a)
gives 2e+p>=2n. If p>0, its total e+p is at least n+1. If p=0,
connectedness and minimum degree two give e>=n; equality would make every
degree two and the component a pure cycle, forbidden by (b). Hence again
e+p>=n+1.

For a nonempty proper subset Q of a connected component, let a be its
internal edge count, c its edges to the rest and p_Q its private resources.
There is at least one crossing edge, so c>=1. Summing (a) over Q gives
2a+c+p_Q>=2|Q|, whereas |N(Q)|=a+c+p_Q. Thus
2|N(Q)|-2|Q|>=c+p_Q>=1, forcing |N(Q)|>=|Q|+1.
Whole components have the previously proved surplus; summing over the
components met by Q proves the claim. ∎

Consequently a canonical double-entry cut cannot consist of an isolated
receiver with one witness, a resource tree with only one private anchor,
or an unanchored resource cycle. A path with two private end resources is
allowed. It is a surplus witness component, different from the saturated
ordinary blocking trees in the earlier fixed-route exchange theorem.

## 4. Only one unused interval for arbitrarily many receivers

For q>=1 create alpha pairs A_i,C_i and beta B_i, i=0..q-1. Each alpha has
one direct link to a different BP tip of B_i and has no interval support.
Let the distinct original intervals be J_0,...,J_q, and give

    W(B_i) = {J_i,J_(i+1)}.

There are no other links or supports. Every interval has at most two beta
owners. All q forks can use their own B_i and J_i, giving

    full optimum = (value,minimum links) = (2q,2q),
    ordinary optimum =                         (q,q).        (3)

Every source needs a link, proving the full cost lower bound; there are
2q sources. Ordinary stems can only consume q whole betas, proving their
value upper bound. Thus (3) is exact for every q.

There is one globally unused interval, J_q. The largest-source-side minimum
cut contains all source alpha nodes and their BP entry nodes, but no beta
body or interval. Its cut consists of the 2q BP entry gates. To see maximality,
from any beta body an unused forward support or a reverse used support
followed by the next support leads along the chain to J_q and then t.
All those body/interval nodes can reach t residually; saturated entry gates
prevent the source/entry nodes from doing so. Hence every B_i is in D,
and all q+1 intervals are far-side witnesses.

For any nonempty Q of beta indices with r consecutive runs,
|N(Q)|=|Q|+r. The strict Hall theorem is satisfied. More explicitly, after
deleting any J_h, assign B_i to J_i for i<h and to J_(i+1) for i>=h.
This is injective, uses a supported unit, and avoids the deleted unit.

Despite q separately matched witnesses, only one interval is unassigned
in the full packing. Their other identities already support the fork
payments. Therefore the rule "one double-entry receiver supplies one extra
unused reserve" fails by an arbitrary amount. This is an abstract family;
no frozen physical realization is claimed. Its scalar ledger is
(q+1)+q-2q=1, so it does not refute the target counting inequality.

## 5. Complete finite two-edit frontier

Keep the 16-by-14 base shape, original 21 selections and 66 endpoints, and
standard blank boundary columns 0 and 13. There are exactly four perfect
matchings on those endpoints. From each, add at most two elementary actions:
one new selection, or one actual edge between two previously blank adjacent
vertices. Old selections and the chosen old matching remain unchanged.

There are 52 individually feasible selection actions and 61 individually
feasible matching-edge actions. Every feasible joint extension uses actions
from these lists: deleting other new occupied vertices cannot invalidate
feasibility of an individual action. We do not require each individual
edge addition to be frozen; two actions may jointly supply freezing.
Enumerate all empty/single/pair action sets, reject shared vertices and
infeasibility, then check complete freezing and reconstruct the entire
whole-support model. This exhausts the stated finite class.

There are 25,004 disjoint edit sets, 24,852 feasible boards and 6136 fully
frozen boards. Their edit distribution is 4 unchanged, 208 one-selection,
12 one-edge, 5264 two-selection, 620 selection-plus-edge and 28 two-edge.
Every fully frozen board has full payment of all original alpha demands;
full and ordinary maximum values and minimum costs agree. No negative
scalar margin occurs. The selected full-flow optima contain no forks,
which does not mean there are no feasible forks.

Twenty-four first representatives of the grouped physical cases also agree
with independent primitive packing optimization. A canonical cut with a
single BP entry is already present on the base board, but has zero deficit;
its existence alone is not evidence of failed compensation.

This finite exclusion leaves extensions with more actions, different
endpoint footprints/guards and nonlocal matching surgery open. It does
not imply a universal grid theorem or a general bound on all min-cuts.

## 6. Verification and formal scope

The canonical-cut checker passes 7352 models: 1200 independent random
two-owner systems, 16 shared-reserve chains and 6136 physical boards.
It checks 137,272 strict simultaneous promotion inequalities and 166
single-interval deletion matchings. Twenty canonical cuts contain 140
double-entry receiver occurrences; twenty two-owner surplus components
pass the graph checks. Five small shared chains are independently optimized.
The original full-flow suite is also replayed after adding the optional
largest-cut output: 11,308 packing comparisons and 96,843 terminal matchings
retain their previous results.

Six scoped local Lean 4.33.0 declarations verify the arbitrary-q assignment
after deletion of any one interval, its injectivity/support/avoidance,
the baseline allocation's range and its exactly one unused interval, and
the strict joint-promotion arithmetic. Only propext, Classical.choice and
Quot.sound occur; there are no warnings, incomplete proofs or native_decide.
The min-cut lattice/body-promotion adapter, general Hall/graph theorem,
physical frontier completeness and all-q flow optimality are written proofs,
not claimed complete Lean formalizations. No external review is claimed.

Reproduce:

    python3 develop/check_beta_cut_promotion_and_frozen_frontier.py --output output/beta-cut-promotion-and-frozen-frontier-validation.json
    python3 develop/check_beta_cut_promotion_formal.py --lean /path/to/lean-4.33.0 --output output/beta-cut-promotion-formal-validation.json

The next geometric target is a positive full deficit outside this finite
frontier. Single-entry obstructions remain possible in the abstract model;
double-entry receivers must obey the simultaneous surplus condition above.
Any compensation argument must distinguish far-side witnesses from genuinely
unused, jointly routable reserve. The universal grid bound remains open.
