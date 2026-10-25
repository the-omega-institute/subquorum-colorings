# Exact resource gluing across original endpoint components

**Full-pool continuation:** [sharp opening budgets and full-pool path
circuits](EXTREMAL_SHARED_UNIT_BUDGET_AND_FULL_POOL_PATH_CIRCUITS.md) gives a
different frozen adjacent-module family whose complete physical original
pool has an arbitrarily large path circuit. Each open shared seam costs
exactly one selection relative to its true fixed-P maximum. This strengthens
the restricted-pool diagnostic in Section 3; that section's own full-pool
repair statement remains valid.

**Support-saturation refinement:** [original owner classes and the singleton
core](SUPPORT_CLASS_SATURATION_AND_SINGLETON_CORE.md) preserves every fixed
terminal matching while privatizing any class with at least as many units as
original owners. In physical two-owner systems only singleton owner-pair
classes can couple active P-components; an empty core gives exact value AND
cost additivity. The two original companion units repair every frozen path
in Section 3 without exterior resources.

25 October 2026. Haobo Ma and Wenlin Zhang. Research branch only.

The original endpoint-neighbor components give an exact decomposition of
whole-support compensation. Arbitrary internal mixed layers, separate BP
entries, beta forks, and repeated visits to a tile remain inside the local
networks. The only shared capacities are the ORIGINAL interval units.
Their joint overlap has an exact formula. A fully frozen physical family
shows that every bounded-order withdrawal test can miss that overlap.

This is a specialization of standard integral max-flow/min-cut and cut
uncrossing, not a new general flow theorem. The physical family refutes a
local-to-global inference for restricted original availability; its FULL
original pool pays all sources. No universal grid counterexample or improvement
of the 5/6 bound is claimed. The submitted manuscript is unchanged.

## 1. Fixed model and the decomposition

Use the exact [whole-support fork network](WHOLE_SUPPORT_FORK_FLOW_AND_RESOURCE_CUTS.md),
with its original owner supports and original interval identities. Let P be
the endpoints of the actual matching M; components below mean connected
components of the graph on P with grid-neighbor edges. They are not matching
blocks, tile components, or components of a chosen certificate injection.

Each actual M edge and each original auxiliary PP edge joins adjacent P.
Thus every original open owner is wholly in one P-component. Each declared
actual TP--BP link also joins adjacent P, and stays in that component.
Consequently mixed gates, both physical BP entries of a beta, its body, and
its one whole-beta sink are internal to one component. Only interval nodes
can be shared. Closed PP/M cycles carry no alpha source or terminal sink.

Let i range over alpha-bearing P-components; k_i is its number of original
alphas and k=sum_i k_i. An omitted source-free component cannot carry an
alpha-starting flow. Omit its owners and arcs, retaining ALL original unit
IDs and the supports of retained owners, as in
[source-free pruning](SINGLE_SQUARE_WIRES_AND_SOURCE_FREE_PRUNING.md).
Keep physical negative charges separately; this is a network operation.

Fix any available original interval set Q. For R subset Q define V_i(R)
as the maximum flow in component i, with only R intervals available and
ALL its original internal gates, actual links and private beta sinks.
Write V(Q) for the full network's maximum. No one-stage, private-source,
common-output, or scalar tile-capacity assumption is imposed.

**Theorem 1 (exact gluing).**

    V(Q) = min_{R subset Q} ( |Q \ R| + sum_i V_i(R) ).             (1)
    k - V(Q) = max_{R subset Q} ( sum_i(k_i - V_i(R)) - |Q \ R| ). (2)

In particular full compensation holds exactly when

    sum_i(k_i - V_i(R)) <= |Q \ R|  for EVERY R subset Q.          (3)

**Proof.** Work in the original integral flow network, before beta-output
normalization; all large arcs can have the same capacity k+1. This does
not change local optima because k_i <= k. Every source-to-sink path stays
in its P-component until it terminates at either a private beta sink or
a shared interval sink. For any R, at most |Q\R| paths use intervals
outside R. The remaining paths restrict to feasible local flows with
R available; their total is at most sum_i V_i(R). Removing some paths
preserves the original entry and owner capacities. Thus V(Q) is at most
every displayed expression. Normalization can then be applied if desired;
there is no assumption that it preserves used interval identities.

Conversely take a global minimum cut U (source side), and let J be its
source-side interval nodes in Q. Put R=Q\J. The interval-to-sink arcs
contribute exactly |J|. The other cut arcs partition by P-component:
source arcs, mixed gates, physical beta entry gates, beta-sink arcs,
internal links, and accesses to intervals in R. Accesses to J never
leave U and add no cut cost. Restrict U to component i and the nodes of
R. This is a cut in its R-available local network. Its capacity is at
least V_i(R). Hence V(Q) >= |J|+sum_i V_i(R), which is at least the
minimum in (1). Both bounds give (1); subtracting from k gives (2),
and V(Q)<=k gives (3). The empty active-component case is included. ∎

No shared interval can be spent twice in this proof. The term |Q\R|
counts each ORIGINAL unit once, even when many local networks support it.
The sum of full-pool local maxima alone is only an upper bound on V(Q).

## 2. Fixed-network ranks, private-unit elimination and witnesses

**Lemma 2.** Each V_i is integer, monotone, submodular, and satisfies

    0 <= V_i(R union {j}) - V_i(R) <= 1.

The normalized function V_i(R)-V_i(empty) is a matroid rank function.
This concerns availability in one FIXED network. It makes no submodularity
claim about the earlier signed geometric reserves, whose configurations
and support networks change.

**Proof.** Adding a unit adds one sink arc of capacity one. Feasibility
gives monotonicity. Deleting its at-most-one flow path gives the upper
increment bound. Integrality is integral max-flow. For submodularity put
all interval nodes of Q in a fixed graph, and switch their sink arcs
on/off according to availability. Let C(U) be the directed cut capacity
of all FIXED arcs, excluding these switchable interval sink arcs. Then

    V_i(R)=min_U [ C(U) + sum_{j in R} 1_{j in U} ].

All source sides contain s and exclude t. For minimizers U for R and W
for S, directed cut submodularity gives
C(U)+C(W)>=C(U intersection W)+C(U union W).
For each j, its contributions on the left dominate its contributions
with availability R union S at U intersection W and R intersection S
at U union W: if j is in both R,S there is equality, and if in only
one, intersection membership is at most membership on that side.
Adding and minimizing the latter two cuts gives

    V_i(R)+V_i(S) >= V_i(R union S)+V_i(R intersection S).

Subtract V_i(empty). The resulting normalized integer function is
monotone and submodular, with each singleton increment at most one;
these are the rank axioms (and imply r(R)<=|R|). ∎

Thus F(R)=|Q\R|+sum_i V_i(R) is submodular. Its minimizing sets are
closed under intersection and union: uncrossing two minimizers forces
both resulting inequalities to be equalities. The finite lattice has
unique smallest and largest minimizing witnesses.

Call an interval *shared-live* if retained owner supports meet at least
two alpha-bearing P-components. Every other original unit is effectively
private, including a unit shared with a source-free square component.
Adding a private or zero-owner j to R lowers |Q\R| by one and increases
the local sum by at most one. Therefore some minimizing R contains all
non-shared-live units: (1) need only optimize subsets of shared-live units.
The established physical support multiplicity at most two further makes
these shared-live units edges of a multigraph on active P-components.
The proof of (1) itself needs no multiplicity bound.

Let d_i=k_i-V_i(Q), the isolated full-pool local deficit. Equivalently,

    k - V(Q) = sum_i d_i + max_{J subset Q}
        [ sum_i (V_i(Q)-V_i(Q\J)) - |J| ].                      (4)

The maximum is nonnegative (J=empty), and can be taken over shared-live
J only. Withdrawal losses are supermodular, by Lemma 2 and complements.
Consequently singleton losses do not control simultaneous withdrawal.
Formula (4) gives the exact additional loss due to intercomponent overlap,
with each removed original unit charged once.

## 3. A frozen physical path requiring arbitrarily large joint tests

**Theorem 3.** For every n>=2 there is a feasible fully frozen grid with n
separate one-alpha P-components, and n-1 designated original units whose
support graph on these components is a path. On that restricted pool Q:

* each local V_i(Q)=1, but V(Q)=n-1;
* every proper withdrawal J strictly contained in Q satisfies
  sum_i(V_i(Q)-V_i(Q\J))<=|J|;
* J=Q has total loss n and excess one.

Adding every truly zero-owner original unit preserves these values and
the withdrawal losses indexed by subsets of the designated live edges.
The pool can therefore have at least n units while still paying only n-1.
With those extra units present, a withdrawal of ALL live edges is already
an obstruction even if it is a proper subset of the enlarged pool. The
minimal-witness assertion refers to the designated live edge set. The
full original pool pays n, at zero link cost.

**Construction and geometric proof.** Use zero-based coordinates on an
8 by (4n+6) rectangle. For i=0,...,n-1 put c_i=4+4i and take

    M_i = ((3,c_i),(4,c_i)),
    T_i = {(2,c_i),(5,c_i),(3,c_i+1),(4,c_i-1)}.

The selected sets have no occupied-neighbor conflict: the four T around
each pair are mutually nonadjacent and each meets just its indicated P;
spacing four leaves T belonging to different pairs nonadjacent. Each
P has its mate and two selected neighbors, giving occupied degree three;
the original freezing rule therefore freezes every P immediately.
P-components are exactly these isolated vertical M pairs. In bands
rows2,3 and rows4,5, each end column has one T and one P, so the original
owner is alpha. There are no BP terminals and no terminal links.

In band1 (rows2,3), the gap between c_i and c_{i+1} has three columns:
c_i+1,c_i+2,c_i+3. Only (3,c_i+1) is selected; the other two columns are
unmarked original units. Designate e_i as the unit at column c_i+2=6+4i.
The gap's two original boundary owners are precisely alpha i and i+1;
by whole-support construction they, and only they, support e_i. Let
Q={e_0,...,e_{n-2}}. No private beta sink exists. Each local value is one
as long as at least one incident path edge is available; otherwise zero.
Assign e_i to alpha i for a payment of n-1, and the n-1 available sink
arcs bound the payment from above.

For proper J choose an unwithdrawn edge e_r. A vertex losing all its
incident units is neither endpoint r nor r+1 of e_r. Send each such
vertex toward e_r along the path: map v to e_v when v<r, and to e_(v-1)
when v>r+1. Its image belongs to J, and the map is injective (the two
image ranges are disjoint). Thus the number of losing vertices is at
most |J|. With J=Q all n vertices lose their unit, giving excess one.
This is a proof for every n, not extrapolation from enumeration.

There are at least n zero-owner units in band0 (rows0,1), which has no
P or T and no boundary owner, so adding them can make |Q|>=n without
altering any local or global value. They are effectively private and
can be excluded from optimizing withdrawals as in Section 2. Finally,
in the full original pool use for each alpha the unit in band2 at
column c_i+1. It is unselected, is supported at that alpha's boundary,
and all these n original units are distinct. This pays all n at cost0. ∎

For any prescribed test order b, take n>=b+2. All withdrawals of at most
b units pass the local-loss inequality, while the joint n-1-unit
withdrawal fails. Thus bounded-order checks, even all proper subfamilies
in this path, cannot replace the joint witness in (3)/(4). This is an
obstruction to that checking rule, not a counterexample to the full-pool
grid compensation target or to the 5/6 bound.

## 4. Count and cost must remain distinct

Equation (1) is a VALUE formula. Independently minimum-cost local maxima
need not glue at their summed cost. Here is a small abstract control,
not a claimed physical grid. Two components each have alpha a_i and
mixed m_i, with one actual link a_i->m_i. Both alpha supports are {j};
mixed supports are {x_0} and {x_1}, respectively. All units are distinct
except the shared j. Each local maximum is one at cost0 using j. The
global maximum is two, but its minimum cost is one: at most one source
uses j and the other must traverse its mixed link to x_i. This is also
attainable. The global exact min-cost fork-flow solver remains valid.

## 5. Reproducibility and precise formal scope

Run from the repository root:

    python3 develop/check_endpoint_component_resource_gluing.py \
      --output output/endpoint-component-resource-gluing-validation.json

The verifier compares (1) with the full exact fork network, tests the
whole availability lattice on small partitioned networks (including
layered mixed routing and both beta entries), checks rank uncrossing,
the minimizer lattice, effective private units and (4), and uses
independent terminal matching enumeration on small controls. Frozen
fixtures test the actual P-component adapter. The explicit all-n family
is tested with all proper withdrawals at small n and targeted larger n;
the general proofs above supply the unrestricted claims.

[Lean source](../formal/SubQuorum/EndpointComponentResourceGluing.lean)
checks the arbitrary-length path's parent-edge injection and its
incidence/deletion implications, elementwise cut-output uncrossing,
and the arithmetic needed to uncross optimal witnesses and eliminate a
private unit. It does not formalize max-flow/min-cut, the whole physical
grid adapter, matroid rank recognition, or cardinality from finite-set
injections. Those steps are proved above and tested separately. The
validation artifacts record the exact declarations and execution scope.

The recorded run passed 139 lattice models, 1,916 exact gluing availability
sets, 94,876 rank-submodularity pairs, 8,607 unit-increment checks, 5,764
minimizer-uncrossing pairs and 3,500 independent terminal matchings. Four
existing frozen fixtures, the source-free-square shared-unit control and
12 physical path sizes (n=2,...,10,16,32,64) passed; 1,137 path withdrawals
were checked. The 11 Lean declarations passed locally on Lean 4.33.0:
two are axiom-free and the other nine use only standard Lean axioms, with
no warnings, placeholders or native decision shortcuts. Existing unrelated
Lean/Lake processes were measured and preserved; this file ran alone.

* [Computational receipt](../output/endpoint-component-resource-gluing-validation.json)
* [Formal scope and receipt](../output/endpoint-component-resource-gluing-formal-validation.json)
* [Lean axiom report](../output/endpoint-component-resource-gluing-lean-validation.txt)

The next geometric problem is to bound the joint withdrawal expression
in (4) against the original tile/receiver ledger for actual full pools,
while retaining the exact internal mixed/BP/beta rank of every active
component. Single-square source-free pieces do not consume source flow;
alpha-bearing multi-square components and occupied-band resource
withdrawals remain the difficult cases.
