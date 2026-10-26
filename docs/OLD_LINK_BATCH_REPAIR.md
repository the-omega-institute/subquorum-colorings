# Exact batch compensation without adding physical links

26 October 2026. Wenlin Zhang and Haobo Ma. Independent research continuation.

After any batch of P-free direction changes, including mixed target directions
and changes that lose old support, a fixed old normalized routing pack has an
exact repair formula. It uses the union of the **new** supports along each old
primitive, rather than only the old endpoint witness. Ordinary stems may stop
early. A beta fork may split into an early interval stem and its other old
beta arm. These operations add no physical link.

Each old interval primitive or fork becomes one request; a whole-beta payment
is a separate guaranteed baseline, not an interval credit. Each previously
unpaid alpha that we allow to become paid directly is another request. An
original new interval supports at most two such requests. The resulting
resource multigraph gives the exact maximum payment using subsets of the
old pack's links, and an exact test for preserving specified source identities.

The graph-allocation theorem is the established result in
[one-sided allocation](ONE_SIDED_INTERVAL_AND_BETA_ALLOCATION.md), not a new
abstract matching theorem. The new result is its exact bidirectional adapter
to **arbitrary old mixed/beta primitive packs after destructive support
changes**, including prefix truncation, beta splitting, newly paid direct
sources and prescribed source retention. This extends the single-pivot own-arm
repair in [the pivot ledger](P_FREE_PIVOT_INTERFACE.md). It requires no
lossless-handoff or uniform-target hypothesis.

## 1. Hypotheses and the restricted optimization problem

Use the full original owner/terminal/link model from
[whole-support normal form](WHOLE_SUPPORT_FORK_NORMAL_FORM.md). Owners are
original M/PP paths, with alpha sources A, capacity-one mixed owners, and
beta owners having their two actual BP entries and one private whole-beta
payment. Each original interval is one resource. Its supporting owners are
the distinct open owners at the two boundaries of its maximal no-P gap;
there are at most two, including when the same owner occurs at both boundaries.

Let P0 be any owner-disjoint normalized pack, not necessarily optimal. It has
s ordinary interval stems, b single-source beta stems and f beta forks.
Its paid source set A0 has size

    p = s + b + 2f.

Let E0 be its actual selected physical links. Distinct primitives have
disjoint owners. Inside a fork the two directed source-to-beta arms meet
only at its beta and enter different physical BP tips. Retain the owner
bodies, types and possible physical links, but replace the old interval pool
and support relation by a new pool Q and supports W(o). Assume each j in Q
has at most two distinct supporting owners. Old and new unit IDs need not
be identified or unioned.

Choose N subset A\A0. These are the new alpha sources eligible for direct
zero-link payment. The optimization may pay any subset of U=A0 union N,
using **only links in E0**, the new intervals, and the original private beta
payments. Sources outside U are excluded. Request a prescribed subset
R subset U if desired. Since no source in N occurs in P0 or has an outgoing
link in E0, it can only be paid directly. No old unused physical link may
be added. Retained stems may be shortened and beta forks split.

These hypotheses hold for every simultaneous change of directions on any
collection of aligned P-free tiles, with fixed feasible T and actual M.
At each endpoint its auxiliary mate is unchanged; hence the global owners,
terminal types and physical links remain unchanged. Canonical bands may
split or merge. The new resource pool is compiled afresh, so no common-anchor
or all-subsets monotonicity assumption is needed. Bent owner bodies, occupied
adjacent bands, and local capacity zero, one or two are permitted. This is a
theorem for a specified final direction state, not an optimizer over all states.

## 2. Requests, baseline and actual resource graph

Make a request d for each ordinary interval primitive and each beta fork
of P0. Give d all new units supported by any owner in that primitive:

    J(d) = union_{o in owners(d)} W(o).

Also make one request for every a in N, with J(a)=W(a). A beta singleton
has no request: it retains its one source at its own whole-beta payment.
A beta fork supplies one guaranteed baseline payment and one request for its
second source. Thus the baseline is B=b+f and the number of requests is
D=s+f+|N|, giving B+D=p+|N|.

The unions here deduplicate actual unit IDs. A unit supported by several
owners of the same primitive is still one neighbour of that request.
Distinct requests have disjoint owner sets; their aggregation therefore
preserves the at-most-two-request incidence bound.

Form a multigraph on requests. A unit with two distinct request neighbours
is an ordinary edge. A unit with one neighbour is a private resource at that
vertex. A unit with no request neighbour is unallocated inventory and is
not an edge or a credit for another component. Parallel original units give
different edges: two units from a capacity-two tile must not be collapsed
into a single token.

Call a component deficient if its ordinary-edge graph is a tree and it has
no private resource. An isolated request without neighbours is included.
Let t be the number of deficient components. An unused unit elsewhere
cannot compensate a tree unless an actual incidence connects it to that
tree; a positive global resource count alone is insufficient.

## 3. Exact repair and prescribed-source theorem

**Theorem.** Under Section 1, the maximum number of sources in U payable using
only links in E0 is exactly

    V_E0 = B + D - t = p + |N| - t.                    (1)

There is a constructive pack attaining (1), with each original interval
used at most once and physical link set a subset of E0.

Mark a request mandatory when its ordinary stem's source lies in R, its
new direct source lies in R, or **both** sources of its old fork lie in R.
Then R is feasible if and only if every deficient component has at least
one nonmandatory request. Whenever R is feasible, a maximum pack attaining
(1) can retain it. If it is infeasible, a deficient component all of whose
requests are mandatory supplies a checkable Hall obstruction: n requests
have exactly n-1 actual neighbouring resources.

**Proof, graph allocation.** In each component take a spanning tree, using
its edge resources to pay all nonroot requests with their parent edge.
If a private resource exists, choose its vertex as root and pay it with that
resource. Otherwise, if an extra ordinary edge exists outside the tree,
choose one of its endpoints as root and use that edge to pay the root.
The tree edges and the extra resource are distinct. Thus every nondeficient
component is fully matched. A deficient component has exactly n-1 resource
neighbours, pays n-1 requests and can leave **any chosen** root unmatched.
Different components have disjoint neighbouring unit sets. Therefore the
maximum matching size is D-t. For prescriptions, choose a nonmandatory root
in each deficient component; if none exists, its Hall count forbids the
prescription. This is the earlier finite resource-allocation theorem.

**Proof, constructive routing.** Keep every old beta singleton. For a matched
ordinary request, its assigned j has support at some owner on its old stem.
Keep the prefix to that owner, terminate there using j, and discard the
remaining suffix. For an unmatched ordinary request remove the stem.
A matched new request uses its own alpha's support with zero links.

For a matched fork request, if beta itself supports j, retain the old fork
with j. Otherwise choose a supporting owner on one of its two old arms.
Pay that arm's source by its prefix ending at j, and keep the other full arm
to its old whole-beta payment. The truncated prefix ends before beta, so
these two primitives have disjoint owners. They retain both source identities,
use distinct outputs and use only old links. For an unmatched fork request,
keep one old arm at beta. If precisely one fork source is prescribed, choose
that arm; both sources prescribed would have made the request mandatory.

Each component allocation assigns different new intervals. Original primitive
owner sets were disjoint, and all repairs use subsets of these sets. Betas
are also distinct between primitives. No interval, mixed owner, beta BP entry,
private beta payment or physical link is reused. The pack pays B baseline
sources plus D-t matched requests, giving the lower bound and prescriptions.

**Proof, upper bound.** Consider any pack on U using a subset of E0, allowing
all legal reassignments and truncations. Its source routes stay inside their
original primitive owner sets: E0 contains no edge between different old
primitives. A new source has no E0 edge and must use its own interval.
An old ordinary primitive can retain at most one source, and retaining that
source requires some interval in its union J(d). A beta singleton retains
at most its one source, irrespective of whether it uses beta or an interval.
An old fork can retain at most two sources; to retain two it needs at least
one interval supported somewhere in its owner union, since its one private
beta payment has capacity one. If both sources use intervals, select one
of those units for the fork's request. Select an interval likewise for each
retained ordinary/new source. These selections are different between
requests, since the actual pack does not reuse intervals. They form a
matching in the resource graph. Total payment is consequently at most
B plus its maximum matching size, B+D-t. The same argument makes every
mandatory request matched when R is retained, proving necessity. QED.

No assertion of minimum link count is made. The construction never exceeds
the old link set, but two early interval terminations of a fork may use fewer
links than the particular construction keeping one full beta arm. The checker
contains a strict control for this distinction.

## 4. Exact cross-component compensation ledger

With N empty the exact maximum old-source retention is p-t. This jointly
accounts for every changed support in the final state; summing independent
per-pivot losses is unnecessary. A lost endpoint witness need not cause any
loss if an earlier owner on its stem supports a new unit.

With g=|N| eligible new sources, (1) gives the exact gain in this restricted
optimization:

    V_E0-p = g-t.                                      (2)

Hence g>t guarantees a strict payment increase, and g=t guarantees no
cardinality loss. If preserving all old source identities is required,
apply the mandatory-root test with R=A0. A fork then is mandatory just like
an old ordinary stem, so each deficient tree must contain a new-source
request that may be left unpaid. It is unsafe to infer identity preservation
merely from V_E0>=p. If all eligible new sources must also be paid, every
request is mandatory, so **t=0 is necessary and sufficient**.

Alternatively suppose concrete distinct new resources R0 have already been
assigned injectively to g new direct sources. Delete R0 from the old requests'
neighbour sets first and let t_R0 be their deficient-component count. Keeping
those new assignments fixed and repairing the old pack gives exactly

    p + g - t_R0                                      (3)

within that fixed-assignment scheme, with the same mandatory-root test for
old sources. This is the safe reservation order: the new payment and the
old repair never spend a unit twice. Formula (1) can improve on prematurely
fixing these assignments by choosing them jointly.

For the original complete grid model set N=A\A0. The exact old-link payment
is then |A|-t. Since any normalized pack uses distinct intervals and private
betas, L+beta >= |A|-t. With the original ledger
S=L+beta-|A|=area/2-|T|-|M| this proves

    S >= -t,    |T|+|M| <= area/2 + t.                 (4)

In particular t=0 certifies the coefficient-one inequality
|T|+|M|<=area/2 on this explicitly checkable class, including destructive
mixed-direction batches. The theorem does **not** show t=0 for arbitrary
grids or prove a universal improvement of the existing 5/6 result. When t>0,
unused physical links may repair the obstruction; (1) is an exact obstruction
to repair by E0 alone, not necessarily to full routing or the target inequality.

## 5. Controls, frozen applications and validation

The executable API is `repair(new_data, old_pack, required=..., new_sources=...)`
in [the validator](../develop/check_old_link_batch_repair.py). Its production
path uses support unions and the parent-edge construction, with no primitive
enumeration, flow or blossom call. An API control makes all such calls fail
if invoked. The independent primitive generators and optimizers appear only
in the audit. A fixed old pack need not be optimal.

Nine targeted controls check prefix repair after complete endpoint support
loss; fork splitting at a mixed prefix; two demands competing for one actual
unit despite unrelated spare inventory; distinct and parallel capacity-two
resources; repair possible only with a previously unused link; new direct
payment displacing an old mixed-stem source; a second original unit giving
strict gain; and the failure of minimum-link optimality for this construction.
The competing one-unit pair has total payment one: requiring both identities
is infeasible, even though each alone is feasible. This refutes a shared-reserve
compensation rule, not a new frozen-grid or universal-bound conjecture.

Existing frozen geometries give two useful checks of the new adapter. The
16x28 and 16x34 support-only pivot boards have old value two and exact repaired
value one; unrestricted routing also has value one, as proved in the original
pivot note. The existing coordinated-gate families with two and nine gates
have old payment one and, after all gates open, payment two retaining the old
source with the same one old link. Each has 70 strictly frozen endpoints.
These applications reuse their established geometric proofs; the new claim
is the exact general repair theorem above.

Run:

```sh
python3 develop/check_old_link_batch_repair.py \
  --output output/old-link-batch-repair-validation.json
python3 develop/check_old_link_batch_repair_formal.py \
  --lean /Users/lexa/.elan/toolchains/leanprover--lean4---v4.33.0/bin/lean \
  --output output/old-link-batch-repair-formal-validation.json
```

The independent audit checks 976 old-link optima, 3,862 prescribed source sets
(1,525 infeasible), 160 generic support changes, all 157 compatible old packs
in 24 additional small models, and 244 physical batches. Twenty batches change
tiles toward both final directions. There are 24 old beta-fork occurrences,
350 independently replayed strict freezing events, and one no-enumeration API
control. Finite checks test the adapter and implementation; Sections 1--4 are
the arbitrary-size proof.

The scoped Lean file proves that disjoint owner aggregation preserves the
two-user resource bound, and that a beta-arm prefix excluding the shared beta
is disjoint from the other arm. It does not formalize the complete graph
allocation, path enumeration or the end-to-end grid theorem. The previously
formalized parent-resource injection in `OneSidedResourceAllocation.lean`
remains the graph allocation's separate kernel. No claim of end-to-end Lean
verification is made.

The 11 October manuscript, public main, PR3, shared CI and C4 correspondence
are preserved. This note is a research result, not a manuscript amendment.
