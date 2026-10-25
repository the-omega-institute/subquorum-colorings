# Saturated original support classes and the irreducible singleton core

25 October 2026. Haobo Ma and Wenlin Zhang. Research branch only.

Subsequent full-pool obstruction. The [fully frozen singleton family](FULL_POOL_SINGLETON_OBSTRUCTION.md)
realizes an essential cross-component core even in the complete original
pool: two locally payable sources have joint value one, with all links
reselected and no extra reservations. A raw-pool version also includes every
boundary unit. This does not contradict saturation or exact gluing; it
refutes automatic full compensation under feasibility and freezing alone.

Two available intervals with the SAME two original whole owners can be
assigned one to each owner without losing any cancellation/allocation value
or link cost. Their coordinates may be in different bands and gaps. This
extends the two persistent shared units used for the special
[protected-column family](PROTECTED_SHARED_COLUMNS_AND_FRESH_ENDS.md)
to arbitrary internal mixed routing, beta forks and fixed terminal matchings.

Consequently, after exact source-free pruning, the only resources which need
couple distinct active original P-components are singleton support classes:
exactly one available original unit supported by exactly two retained owners
in different active components. This strengthens the
[component-gluing interface](ENDPOINT_COMPONENT_RESOURCE_GLUING.md), including
an exact cost-additivity theorem when this singleton core is empty.

The allocation exchange is elementary, not a new general matching theorem.
The geometric statement uses the existing at-most-two-whole-owner adapter.
The unrestricted geometric inequality and universal 5/6 improvement remain
open. The submitted manuscript, public main and shared CI are unchanged.

## 1. Original resource classes and a fixed cancellation

Fix the original terminal model: disjoint two-terminal owners O; a declared
TP/BP type at each tip; admissible terminal links; and a fixed set Q of
available ORIGINAL intervals. For every owner o, W(o) subset Q is its whole
support. For each unit j set

    U(j)={o : j in W(o)},        J_U={j in Q : U(j)=U}.

All support sets here are ORIGINAL owner sets, not P-component labels,
reachability sets, free terminals, or virtual owners after cancellation.
Classes J_U are disjoint, and every owner in U supports every j in J_U.
For the physical adapter |U|<=2; the first theorem permits arbitrary finite U.

Choose ANY fixed admissible terminal matching C. Its cancellation graph has
the original strand edge of each owner and the links C. Every original owner
belongs to precisely one cancellation component; a resulting virtual alpha
is one component, with one interval payment available. Its legal support is
the union of W(o) over the original owners in that component. Different
virtual alphas have disjoint original-owner sets. The number of consumed
whole betas is determined by C and does not depend on interval allocation.

A nonempty class J_U is *saturated* when |J_U|>=|U|. Choose any injection

    e_U : U -> J_U.

For each saturated class retain only the support incidences
(o,e_U(o)) for o in U. All its other incidences can be removed. Classes
below saturation are unchanged. Zero-owner resources can have all incidences
empty throughout. Keep ALL original resource IDs in Q and the physical
ledger; this is a restriction of counting witnesses, not physical deletion.
Call the new supports W^sharp.

**Theorem 1 (fixed-matching saturation).** For every C and every subset D of
its virtual alpha components, D has an injective interval payment under W
if and only if it does under W^sharp. The very same terminal matching C
is retained. Hence its maximum interval payment, total compensation and
link cost are preserved. No beta normalization is needed for this claim.

**Proof.** Start with an injective original allocation j_d for d in D.
Choose an original witness o_d in component d supporting j_d. Distinct d
have distinct witnesses, since their original-owner sets are disjoint.
If J_(U(j_d)) is unsaturated, keep j_d. Otherwise replace it by
e_(U(j_d))(o_d), which is still supported by o_d, hence by component d.

Two new assignments in different support classes are different because
the classes are disjoint. Inside a saturated class they are different
because e_U and the witness map d->o_d are injective. Inside an unsaturated
class the old injectivity is unchanged. These cases also exclude a
collision between a changed and an unchanged assignment: their classes
would have to coincide but cannot be both saturated and unsaturated.
Thus all new payments are compatible and pay precisely D. The reverse
implication follows from W^sharp(o) subset W(o). C, all its terminal
conflicts, and beta consumption were unchanged. ∎

**Corollary 2 (exact optimization).** The maximum total compensation and
minimum link cost at that value are unchanged. More generally the whole
set of feasible pairs (C,D) is unchanged. This includes any immutable
prefix C0, restrictions on allowed links, and any cost depending only on
C. It does not preserve arbitrary used interval identities.

**Proof.** Apply Theorem 1 pointwise for every permitted C, then optimize.
An alpha, mixed or beta owner is not itself a freely reusable payment:
it is the disjointness of original-owner witnesses across virtual alpha
components that proves the exchange. In a beta fork there is one virtual
alpha after cancellation and one interval, in addition to the whole beta.
Both incoming BP links and the original beta credit remain unchanged. ∎

This statement is stronger than preserving only the unrestricted flow value.
In particular support reallocation never requires changing a previously
selected physical link or increasing its cost.

## 2. Physical specialization: only singleton pairs remain shared

Use fixed original aligned bands and the established whole-support adapter.
Every original interval has at most two supporting whole open owners,
since its endpoint-free gap has only two boundary P columns. All units
in the same gap have the same owner set (possibly empty or one owner).
Different gaps can have the same set; their units belong to one class J_U.

Theorem 1 gives the following exact reduction:

| Retained owner set U | Available class size | Required shared capacity |
| --- | --- | --- |
| empty | any | none |
| one owner | at least one | one designated private original unit |
| two owners | at least two | one different designated unit per owner |
| two owners | exactly one | retain this one shared original unit |

Additional original units and their physical slack still exist. They simply
need no additional support arcs to represent attainable compensation.
Two units of the same class count as TWO different actual resources, never
as two permissions to reuse one unit. A scalar capacity-two TILE alone
does not satisfy these hypotheses: the
[same-owner square-wire obstruction](SINGLE_SQUARE_WIRES_AND_SOURCE_FREE_PRUNING.md)
continues to apply, and its mixed/BP gates must still be retained.

For intercomponent analysis first use exact source-free pruning. Recompute
U from retained owners; this can merge former classes or turn a shared unit
into a one-owner resource. A unit shared with a source-free square must
stay available to its retained owner. Now define E to be the ORIGINAL
units j for which

1. U(j)={u,v}, with u and v in different alpha-bearing P-components;
2. |J_{ {u,v} }|=1.

All other cross-component classes can be privatized. Internal classes can
also be privatized when saturated; retaining them instead is harmless.
Every unit of E remains a distinct edge between active P-components.
Several different owner pairs can still give parallel edges between
the same two P-components; those are not one support class.

## 3. Exact singleton-core formula in ORIGINAL local ranks

Let V_i(R), V(Q), k_i and d_i=k_i-V_i(Q) be as in the original
component-gluing theorem, after source-free pruning. Then

**Theorem 3 (only singleton pairs need be withdrawn).**

    V(Q)=min_{J subset E} ( |J| + sum_i V_i(Q minus J) ),       (1)
    k-V(Q)=sum_i d_i + max_{J subset E}
        [sum_i(V_i(Q)-V_i(Q minus J))-|J|].                   (2)

Here the local functions on the right are the ORIGINAL local network
values, not an assertion that saturation preserves every availability rank.

**Proof.** Privatize only saturated classes with owners in distinct active
P-components; leave all other classes alone. Call this fixed subnetwork N^sharp.
Its exact global value and minimum cost are preserved by Theorem 1.
Its only intervals supported in multiple active components are E. The
private-unit elimination in the gluing theorem therefore reduces its
minimization to withdrawals J subset E.

For such a J every privatized class is still entirely available, so its
original injections e_U are still valid. Apply the same fixed-matching
proof within each single component. If U meets that component only in
one owner, that owner has its own designated unit; if U does not meet it,
no local allocation uses the class. Thus

    V_i^sharp(Q minus J)=V_i(Q minus J)

for every i and J subset E. Substitute in the reduced gluing expression.
Subtract from k to get (2). ∎

In particular a gap with two or more available units can never be needed
in a minimum intercomponent withdrawal witness. Even a singleton gap is
removable from this witness if another available original interval, in
another band or gap, has the SAME original owner pair.

**Corollary 4 (exact value AND cost additivity).** If E is empty, write c_i
for each original component's minimum link cost at its local maximum.
Then

    V(Q)=sum_i V_i(Q),             c(Q)=sum_i c_i.

Consequently, if each original component is locally fully compensable,
so is their union, at the sum of their minimum costs, with no original
interval, mixed owner, BP entrance or beta credit used twice.

**Proof.** After cross-class privatization the local networks share no
usable resource. Their independent optima combine. Theorem 1 preserves
the global and each local optimum, including cost. ∎

For a matching-closed rectangular packet satisfying the established
boundary adapter, S=area/2-|T|-|M|=L+b-k and I=L-B. Full compensation
implies k<=I+b, so S>=B>=0. Under those explicit adapter hypotheses,
Corollary 4 plus local full compensation proves coefficient one:

    |T|+|M| <= area/2,

removing the entire |M|/6 loss from the existing 5/6 matching-coefficient
bound ON THIS CLASS. No coverage of arbitrary actual components or
unrestricted boundary positions is established.

**Theorem 5 (exact cost by singleton assignment).** For each edge of E,
choose ONE of its two active P-components as recipient; let sigma denote
all these choices and E_i(sigma) the units assigned to i. Put

    R_i(sigma)=(Q minus E) union E_i(sigma),
    v_i(sigma)=V_i(R_i(sigma)),
    c_i(sigma)=minimum local link cost at v_i(sigma).

Then

    V(Q)=max_sigma sum_i v_i(sigma),
    c(Q)=min_{sigma: sum_i v_i(sigma)=V(Q)} sum_i c_i(sigma).

**Proof.** Use the fixed cross-class privatization from Theorem 3.
For each sigma, the resulting local networks have disjoint usable resources,
so local maxima combine and their link costs add. All saturated classes
remain fully available, and their local value/cost optima are the original
ones by Theorem 1, even with these singleton assignments. Thus every
displayed sum is attainable globally.

Conversely take a global minimum-cost maximum flow. Assign every used
singleton-core interval to the component of its source path, and every
unused one arbitrarily to an endpoint component. Its paths restrict to
local feasible flows. Replacing them by the local maxima for this sigma
would be globally feasible after privatization. Their value sum is at
least V(Q), and hence exactly V(Q) by global maximality; no component
can have a strict local improvement. The sum of local minimum costs is
therefore at most the global cost. The first direction supplies the
reverse bound at maximum value. ∎

Only these singleton decisions can obstruct independent cost additivity;
there is no claim that their costs vanish. For example, the earlier two-AM
abstract control has one shared alpha-supported singleton j, with different
private mixed-supported x_i behind one link in each component. Locally
each optimum is 1/0; assigning j to either side forces the other side to
use its private mixed route, giving the exact global optimum 2/1.

The orientation formula describes certificates and costs for any finite E.
It is not a recommendation to enumerate exponentially many assignments:
the existing full min-cost fork-flow network computes the same optimum
in polynomial time. Enumeration below is only an independent small check.

## 4. Verified physical consequences and necessary limitations

The all-n frozen path of the preceding gluing note has two original units
per internal top-band gap, supported by the same neighboring alphas.
Their classes are saturated. The old restricted one-unit-per-gap pool has
n-1 singleton-core edges and pays n-1. Keeping both units per gap makes
E empty and pays all n at zero links for n>=2, even if all exterior
resources are reserved. Thus the companion units themselves repair the
entire family; the earlier separate exterior assignment is not needed.
On a path choose e_(i-1) for each nonleftmost alpha from one copy of its
gap and use the other copy of the first gap for the leftmost alpha.
These are n different original units.

The frozen protected-shared-columns fixture has four active P-components,
four cross-component units in two saturated two-owner classes, and no
singleton-core edge. Its exact full value/cost is therefore the sum of
the local values/costs, 4/0. In contrast the frozen intrinsic one-unit-gap
fixture retains one singleton-core edge, and whole-support donor collision
retains two distinct owner-pair singleton edges between the same two active
P-components. These are genuine remaining interfaces, not deleted by the
theorem; neither fixture is a full-pool counterexample.

Three limitations are essential:

* **Group by original OWNER pair, not P-component pair.** An abstract control
  has components {a_0,m_0} and {a_1,m_1}, no links, with unit x supported by
  {a_0,m_1} and y by {m_0,a_1}. The original value is 2 using x at a_0 and
  y at a_1. Mistakenly grouping by component pair and assigning x only to
  m_1, y only to m_0 leaves value0. Each true owner class was singleton.
  This is an abstract identity countercontrol, not a physical realization.
* **Reserve first, then recompute.** For an abstract alpha a and unreachable
  mixed m, let x,y both have support {a,m}. Privatize x to a, y to m.
  Afterwards reserving x leaves original value1 via y but reduced value0.
  The theorem fixes Q; it is not one static replacement valid for every
  later reservation. Theorem 3 only withdraws E and keeps saturated classes
  fully available, which is why that formula remains exact.
* **Beta sinks and physical ledger remain.** Privatizing interval accesses
  does not create two whole-beta units, remove BP entry conflicts, or erase
  the physical slack of redundant intervals. One cannot replace I by the
  number of retained support arcs in a geometric accounting identity.

## 5. Verification and next geometric target

Run:

    python3 develop/check_support_class_saturation.py \
      --output output/support-class-saturation-validation.json

The verifier checks the stronger fixed-C statement on independent terminal
matchings, compares full fork-flow value and minimum cost, varies prescribed
paid virtual-alpha subsets, and tests singleton-core gluing against all
small withdrawals. It includes beta-fork controls, arbitrary support sizes
in abstract models, the existing frozen fixtures, all-n path controls with
both companion units, and the two deliberately incorrect reductions above.

[Lean source](../formal/SubQuorum/SupportClassSaturation.lean) checks the
arbitrary-size injection exchange given original-owner witnesses, class
membership and injective class selectors, together with the two-owner
selector and accounting implications. It does not formalize the physical
support adapter, cancellation graph decomposition, max-flow/min-cut, or
the complete geometric coefficient-one corollary. The exact declaration
scope is recorded in the validation receipt.

The recorded run passed 267 original/restricted models, 2,898 independent
terminal matchings and 17,653 prescribed virtual-alpha payment subsets;
2,890 matchings checked all such subsets and eight large path cases used
specified and seeded subsets. It removed 3,297 redundant support incidences
across 911 saturated classes without changing the measured optima. The
singleton formulas passed 603 withdrawals and 603 recipient assignments
over 215 models; 86 tests had multiple active components and an empty core,
with exact value/cost additivity. Seven existing frozen fixtures and 14
frozen companion-path sizes (n=2,...,12,24,48,96) passed. Eight Lean
declarations passed on local Lean 4.33.0, four axiom-free and the other four
standard-only, without warnings or placeholders.

* [Computational receipt](../output/support-class-saturation-validation.json)
* [Formal scope and receipt](../output/support-class-saturation-formal-validation.json)
* [Lean axiom report](../output/support-class-saturation-lean-validation.txt)

The unresolved intercomponent geometry is now confined to singleton
ORIGINAL-owner-pair classes. The next question is whether their joint
withdrawal loss can be paid by other original intervals, whole-beta units
and tile/receiver slack, while keeping the internal local ranks exact.
Saturation alone gives no such bound for arbitrary alpha-bearing
multi-square components or occupied adjacent bands.
