# Whole-support forks: one exact flow and a resource-cut criterion

25 October 2026. Haobo Ma and Wenlin Zhang. Research branch only.

Maximum whole-owner-support compensation, including beta-body forks, and the
minimum number of links attaining it are computable by one polynomial-size
integral minimum-cost maximum-flow problem. It is unnecessary to enumerate
compatible forks. The two physical BP tips of every beta have separate
capacity-one entry gates. The beta has one private whole-beta sink and access
to its eligible original intervals. A free normalization makes every used
beta spend that whole-beta unit before spending at most one interval.

The flow and cut theorems are standard. The result is the exact equivalence
for this strand model, including the beta-body normalization and the two
physical entry capacities. It supersedes fork enumeration as an optimization
method, while the previous independent primitive/terminal enumeration remains
useful validation. No new general network-flow theorem or literature-priority
claim is made.

The construction imposes no two-owner hypothesis on interval supports. On
physical grids it uses the established whole-support adapter; its access
arcs are counting witnesses, not assertions of physical free-tip access.
It does not establish that every frozen grid permits full compensation or
improve the universal 5/6 bound.

## 1. Model and network

Use the [whole-support stem/fork model](WHOLE_SUPPORT_FORK_NORMAL_FORM.md).
There are k original alpha owners, beta owners B, mixed owners M, different
available original intervals I, fixed supports W(x) subset I for every owner,
and declared actual TP--BP links. Supports may include beta bodies. Every
resource is used at most once. The objective is

    p(C,F) = |B| - beta_after(C) + |F|,

then the minimum number of selected terminal links at maximum p. Immutable
prepaid C0 is allowed by first contracting it and using the resulting fixed
owner supports, as in the earlier normal form; the present objective is the
additional compensation and links in that contracted system.

The network has a super-source s and super-sink t:

| Part | Arcs and capacity |
|---|---|
| Alpha a | s -> a, capacity 1 |
| Mixed m | m_in -> m_out, capacity 1 |
| Beta b, BP tip q | q_entry -> b_body, capacity 1, separately for its two actual tips |
| Whole beta b | b_body -> t, capacity 1 |
| Original interval j | j -> t, capacity 1 |
| Declared TP--BP link | From its TP owner's exit to the mixed entry or actual beta BP entry, capacity k+1, cost 1 |
| Owner support j in W(x) | From x's exit/body to j, capacity k+1, cost 0 |

Alpha exits are their source nodes, mixed exits are m_out, and beta exits
are b_body. All unlisted costs are zero. Discard mixed self-links; their
positive-cost isolated cycles are unnecessary. Different declared terminal
links can retain separate witness arcs.

The beta's two BP gates bound its total inflow by two. They are entry
capacities, not two whole-beta credits. There is exactly one whole-beta
sink edge. An interval sink is global: supports from multiple owners still
lead to the same one capacity-one original resource.

## 2. Private-beta normalization

**Lemma 1.** Every integral flow without circulation can be changed, with
the same source paths, selected physical links, value and cost, so that each
beta of positive inflow r has exactly one unit using its private whole-beta
sink and r-1 units using intervals. Here r is 1 or 2.

**Proof.** Separate BP gates give r<=2. Every outgoing unit from the body
uses either b's private sink or an interval in W(b). If b's sink already
carries one unit, the claim follows from conservation. If not, take one of
its r outgoing interval paths and redirect its final support/resource
segment to b_body->t. The sink was unused and only b can reach that private
whole-beta edge, so this creates no conflict. It releases the old interval
unit and changes no positive-cost link. Exactly one path now uses b, with
at most one remaining interval path. Perform this independently at every
used beta. The released interval units are never counted as extra payments. ∎

This is the reason an apparent lower-activation condition needs no integer
program: a one-arm beta-body interval path is not itself a valid interval
stem, but it can always be changed to the unused private whole beta.
A beta with two interval outputs can similarly release one interval and
use its whole-beta unit. The normalization preserves payment and links,
not an arbitrary prescribed set of used interval identities. Problems
requiring specified intervals to remain used need separate constraints;
this theorem must not replace the older identity-preserving exchange lemma
without checking that extra requirement.

## 3. Exact equivalence and minimum cost

**Theorem 2.** Let V be the integral maximum-flow value and c its minimum
cost. The full whole-support cancellation/allocation optimum is V, with
minimum additional link count c. Both optima are attained by an explicit
packing of ordinary stems and beta forks obtained from the flow.

**Proof, pack to flow.** An interval stem sends one unit from its original
alpha, along its mixed prefix, through its last owner's support arc to the
assigned interval. A beta stem sends one unit into its actual BP tip and
the private whole-beta sink. A beta fork sends two units, one per alpha arm
through its two different BP entries. Send one out the whole-beta sink and
one through its assigned beta-body interval. Owner-disjointness, distinct
interval assignments and distinct beta units imply all unit capacities.
The two paths of a fork share only its beta body. The value is its payment,
and the cost is its link count.

The prior subset-of-links normalization converts any original cancellation
of value v and link count l into primitives, and hence a flow, of value v
and cost at most l. Thus V is at least the original maximum payment. Once
maximum values are shown equal, the flow's minimum cost is at most the
original minimum link count.

**Proof, flow to pack.** An integral minimum-cost maximum flow has no
positive-cost circulation. Every directed forward cycle must contain a
link arc of cost one, since support arcs end at interval sinks and all
other zero-cost arcs are owner-internal or source/sink arcs. Thus it has
no circulation and decomposes into source--sink paths. Each alpha's unit
source edge gives at most one path, and each mixed gate gives at most one
path through that original owner. Distinct paths therefore have different
alpha sources and do not share mixed owners.

Apply Lemma 1. A path never enters a beta and then another owner: a beta
body only has sink or interval exits. A beta with one path becomes a beta
stem. A beta with two paths has different actual BP entries, different
alpha sources and owner-disjoint pre-beta arms. Together its paths are a
valid fork, spending one whole beta and its one remaining interval. A path
not entering beta ends at an alpha/mixed support witness and is an interval
stem. Different beta groups are disjoint, and interval sink capacities
make all retained original interval assignments different.

At each alpha or mixed TP at most one link is selected, by its source/gate
capacity. At each beta BP at most one link is selected by that specific
entry gate. Therefore the selected links form an actual terminal matching.
The primitives have the flow's value and exactly its positive-cost links.
This proves equality of maximum payments. Applying both directions at
that value proves equality of minimum costs as well. ∎

In particular, if a beta has several supported intervals, it still supplies
at most two total payments, of which exactly one is the whole-beta unit.
Two incoming links at the same BP tip supply at most one payment. Two tips
of the same beta are never counted as two beta units.

The network size is O(owners+intervals) vertices and
O(links+sum_x |W(x)|+owners+intervals) arcs. All capacities are at most k+1.
Successive shortest augmentations take at most k steps; a standard integral
min-cost-flow implementation is polynomial. The previous exact formula
maximizing over disjoint fork choices stays correct, but its exponential
outer enumeration is unnecessary for this unrestricted objective.

## 4. Exact separators including BP entry gates

Let G be the capacity-one gates other than alpha source arcs: mixed gates,
individual beta BP entries, one whole-beta sink per beta, and interval
sinks. For Z subset G delete those gates. Define U_Z to be the original
alpha sources from which no directed path to t survives. Then

    k-V = max_(Z subset G) (|U_Z|-|Z|).                       (1)

**Proof.** Every paid source in U_Z needs a flow path crossing a deleted
unit gate; the paths use any such gate at most once in total. Consequently
at most |Z| of these sources can be paid, giving V<=k-|U_Z|+|Z|.

For the opposite direction, a minimum cut has capacity at most k, so it
crosses none of the k+1-capacity arcs. Let H be the alpha nodes on its
source side and let Z be its crossing non-source unit gates. All paths
from H must cross Z, hence H subset U_Z. The cut capacity is
k-|H|+|Z|=V. Together with the preceding upper bound this forces
|U_Z|=|H| and equality in (1). ∎

In particular all k demands are compensable exactly when |U_Z|<=|Z| for
every such separator. This characterizes compensation in the declared
whole-support model; it is not an equivalent reformulation of every
numerical grid inequality.

**Beta closure in a minimum cut.** If b_body is on the source side, its
private whole-beta sink crosses the cut and every interval j in W(b) is
also on the source side, since a k+1 support arc cannot cross. Thus the
cut includes the one b resource and all those interval sink gates. An
interval shared by several source-side betas occurs only once in Z.
If b_body is on the far side, some of its BP entries may instead be cut;
these are capacity obstructions, not extra resource credits. Ordinary-only
receiver accounting omitting the BP gates cannot certify (1).

This replaces a per-fork residual search with a complete resource-and-entry
separator certificate. Proving a suitable bound on all such separators
from freezing and grid geometry remains a genuine open step.

## 5. Verification and finite mate-surgery control

The new solver agrees in both value and minimum cost with independent
primitive packing enumeration on 11,308 systems, and with 96,843 enumerated
terminal matchings on the explicitly small controls. There are 220 strict
value improvements over ordinary flow and one same-value, lower-cost
example. They are abstract except the already-known physical reserved
interface. No unrestricted strict frozen-grid gain is claimed.

The checks include 1447 positive-deficit separators and 53 returned cuts
containing individual BP entry gates. Every separator is independently
deleted and its blocked source set recomputed. Every returned source-side
beta also passes the support-closure test. Four forced beta-output controls
exercise both normalization changes and already-normalized cases; the
solver's tie order itself returned normalized beta outputs on these models.

Twenty-four actual frozen stack/insertion controls (q=1..8) reproduce
value 3q and cost q+|S|; the physical reserved fork gives value 2/cost 2,
and four physical C0 choices agree with the independent model.

As a finite surgery check, the 66 endpoints of the base fixture support
exactly four actual perfect matchings. All four remain completely frozen.
They are the original and the independent switches of the upper and lower
occupied 2-by-2 squares adjoining the old fork links. Exhaustive vertex
matching recursion verifies no others exist. The original has full and
ordinary optimum (3,1); each other matching has (2,1) in both models.
This rules out a strict gain by changing mates alone on this particular
fixed endpoint/selected footprint. It is not an all-grid surgery exclusion.

Five scoped local Lean 4.33.0 declarations verify the two-BP entry bound for
arbitrary finite path sets, injectivity after replacing one allocation by
an unused private resource, the absence of other new resources, positive
beta occupancy normalization, and the different types of beta/interval
identities. Full flow decomposition, normal-form equivalence, minimum-cost
optimality, separator formula and physical adapters are written proofs,
not claimed full Lean formalizations. No new external review is claimed.

Reproduce:

    python3 develop/check_whole_support_fork_flow.py --output output/whole-support-fork-flow-validation.json
    python3 develop/check_whole_support_fork_flow_formal.py --lean /path/to/lean-4.33.0 --output output/whole-support-fork-flow-formal-validation.json

Next: use the actual BP-aware separator to identify a minimal physical
blocking configuration outside the guarded-pocket class, tracking each
mixed gate, actual beta entry, whole beta and original interval once.
The submitted manuscript and public main remain separate from this research.
