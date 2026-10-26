# Choosing destructive direction exchanges by one exact token flow

26 October 2026. Wenlin Zhang and Haobo Ma. Independent research continuation.

A direction repair can replace a resource already used by a different source.
Thus applying every locally attractive repair is unsafe, even at a completely
frozen true fixed-P maximum. We now give a **positive exact selection theorem**
for a simultaneous class of these destructive replacements. One fixed
fork-capable flow network chooses which actions to perform, pays the maximum
number of sources, and can preserve any specified old feasible paid source
set. Nonnegative integer action costs and physical links can be optimized
lexicographically. The physical old/new resource pools are never unioned.

The optimization uses standard integral max-flow/min-cost-flow theory. The
contribution is the exact old-resource/action encoding, its bidirectional
physical reconstruction including multiunit withdrawal groups and beta forks,
and the distinction between choosing actions and applying all enabled actions.
A second result proves that enabled-action gain need not be submodular:
arbitrarily many coordinated actions may be necessary for a single extra
payment. The abstract family is not claimed to have a frozen-grid embedding.

This does not prove universal availability of suitable geometric actions, or
a universal5/6 improvement. The11 October submitted manuscript is preserved.

The next [P-free pivot analysis](P_FREE_PIVOT_INTERFACE.md) gives a general
five-block support ledger and reserve-based payment stability bound. Its fully
frozen zero-local-capacity example loses payment with every positive forest
cell set unchanged; generic pivots therefore need additional support-change
accounting before they satisfy the physical adapter below.

The later [frozen coordinated-pivot note](FROZEN_COORDINATED_PIVOTS.md) proves
genuine grid coordination by a different geometric mechanism: an arbitrary
number of zero-capacity cuts jointly gate access to two unchanged resources,
and a true fixed-P maximum has a two-pivot repair but no improving single
P-free pivot. This realizes non-submodularity on frozen grids without claiming
a physical embedding of the particular cyclic token family in Section 5.

## 1. Simultaneous replacement hypotheses

Start with the full [whole-support fork model](WHOLE_SUPPORT_FORK_NORMAL_FORM.md):
all global M/PP owners, all physical TP->BP links, mixed capacity-one gates,
both physical BP entries of each beta, its one private whole-beta sink,
and every positive original BB/TT forest unit Q. A source alpha cannot be
used as a transit owner because it has no BP entry.

Let I be a finite collection of optional direction actions. For each i,
specify a target alpha a_i and a nonempty old unit set Q_i. Assume:

1. The Q_i are pairwise disjoint. The union of old owners supporting any
   unit of Q_i has size at most1. Call that owner z_i when it exists.
   Some or all units of Q_i may have no support.
2. For **every chosen subset F** the physical operations are simultaneously
   feasible and preserve all owner bodies, terminal/source types and physical
   links. This includes guards and canonical-band behavior; disjoint physical
   tiles by themselves do not prove simultaneous noninterference.
3. Identifying unchanged forests by actual cells, exactly Q_i for i in F
   are withdrawn. They are replaced by mutually distinct nonempty sets J_i
   of original units, each private to a_i. All other units survive. For a
   direction-only operation |J_i|=|Q_i|, so the numerical raw inventory L
   is unchanged.
4. Every owner that is **not** a target of a chosen action retains precisely
   its old support minus the withdrawn units. Activated targets may lose
   some old supports, but always have the specified private J_i. There are
   no other new resources or support changes.

Repeated targets a_i=a_j are allowed. The hypotheses are an adapter contract,
not a claim that every bent path or occupied adjacent band has such an action.
The [two-tile elbow](LOCAL_ELBOW_RESOURCE_TRANSFER.md) supplies this contract
for the previously stated separated-band geometry. Its delta=1 or2 old
units have at most one old witness. The empty-tile E and elbow F on the
[186-point completely frozen maximum](FIXED_P_MAXIMUM_FROZEN_ELBOW.md) also
satisfy this contract jointly, including their repeated target a.

## 2. Compress a withdrawal group, not its whole old owner

**Single-owner group lemma.** For purposes of payment, paid source identity
and minimum physical links, replace all units in Q_i by one capacity-one
resource token t_i. Give t_i old support from z_i if any unit of Q_i had
support; give it none otherwise. Keep all other units and all owner/link gates.
This preserves the old optimum and every feasible paid source set.

**Proof.** In owner-disjoint primitive normal form, an owner can witness at
most one used interval. In particular a beta fork uses one interval and
one whole-beta sink, not two independent interval credits. Since every
supported unit of Q_i has the same sole possible witness z_i, a normal
pack uses at most one of them. Replace it by t_i without changing any route,
owner or physical link. Conversely an old use of t_i at z_i can be replaced
by any supported actual unit of Q_i. Different groups and all surviving
units are disjoint, so reverse choices cannot collide. Unsupported units
never participate. Beta normalization makes the argument simultaneous for
all groups even if several z_i coincide. ∎

Do **not** merge different groups just because they share z_i. After two
actions their units can become private to two different target sources.
The old owner gate enforces its old one-interval limit, while each disjoint
withdrawal group still has its own token. This retains the distinct units
without counting two old payments through the same witness.

The lemma fails if a group contains two independently usable units at two
different old owners. Two old sources may then be paid at once, whereas a
single token would pay only one. The validator rejects this unsupported
compression rather than using a spurious upper bound.

Tokens are optimization bookkeeping. If |Q_i|=2, compression does not change
the physical fact that two raw original units existed. Never substitute the
number of compressed tokens for L in the numerical inventory identity.

## 3. One proxy network for optional destructive actions

For an enabled action set E subset I, keep the compressed **old** network.
For each enabled i add one direct zero-link access arc

    alpha a_i -> token t_i.

The token still has a single capacity-one edge to the sink, shared by the
old witness access and the action access. Thus a used action consumes the
same token that an old payment would have consumed. Every old mixed gate,
beta BP entry and private whole-beta sink remains in place.

Let V_phys(F) be payment after actually performing F. Let V_proxy(E) be
maximum integral flow in this fixed network with the E action arcs enabled.

**Exact action-choice theorem.** Under Section1,

    V_proxy(E)=max_{F subset E} V_phys(F).                 (1)

An optimum can be chosen with at most one performed action per target alpha.
For any prescribed old feasible paid source set B, there is a maximizer on
the right that retains all source identities in B. Routes and resources
may change. Full compensation within this action class is possible exactly
when this one proxy network sends |A| units; equivalently all its source-sink
cuts have capacity at least |A|.

**Physical pack to proxy.** First normalize every activated target source
to one of its new private units, using the same argument as the exact elbow
formula. A source with an interval route can be replaced by a direct private
payment, freeing its old route. If it is one arm of a beta fork, keep the
other arm at the whole-beta sink; if both arms are replaced, free the fork.
Nothing is lost and physical links do not increase. If an activated source
was unpaid, its private unit would give an additional disjoint payment, so
all activated targets can be paid in a maximum.

If several actions have the same target, keep just one of them and undo the
others. Only that target could use their private units; it keeps the chosen
one. Undoing the other actions restores their old units and cannot hurt the
remaining pack. The all-subsets adapter guarantees this is a valid physical
state. With nonnegative action costs, this pruning cannot increase cost.

Compress surviving groups. Map each remaining activated target's private
payment to its direct a_i->t_i arc. Its withdrawn Q_i was unavailable to all
other physical payments, so t_i is not otherwise spent. All other pack routes
embed identically, retaining their owner capacities and separate beta entries.
This proves a proxy pack of at least the same value, with the same paid
source identities and no greater links or action cost.

**Proxy to physical pack.** Normalize an integral proxy flow into primitives,
retaining beta forks. Each used action arc starts directly at its own alpha:
there is no incoming transit arc to an alpha. Source capacity1 therefore
permits at most one used action for that target. Let F be exactly the actions
whose arcs carry flow. Perform these physical actions. For each such i use
one actual private J_i unit to pay a_i. Token capacity1 ensures that no other
proxy primitive used an old Q_i unit. Every other token was used by an old
access, if at all, and lifts to one actual old supported Q_i unit. All other
resources and nonactivated owner supports survive by the adapter. Gates,
routes and source identities are unchanged. This produces a physical pack
of the same value and physical link cost. The two directions prove(1). ∎

It is essential that(1) optimizes over **subsets**. It does not predict the
value obtained by applying every enabled action. In the186-point example,
applying E and F together pays1, while the proxy with both enabled pays2 by
choosing E alone. The proxy never models a forbidden union of old Q and new J.

**Old-source preservation.** Embed any old B pack in the compressed proxy.
Augment this integral flow to maximum value. A simple residual source-sink
path cannot reverse an already used source arc, because reversing that arc
would re-enter the common source internally. Thus all B source arcs remain
saturated. Reconstruction preserves those source identities. This standard
augmentation argument proves existence at maximum value; it does not assert
that the cheapest unconstrained maximum automatically preserves B.

## 4. Costs and a unified numerical consequence

Assign nonnegative integer action weights c_i. Put c_i on action arcs and
unit cost on physical links, interpreted lexicographically. Old access and
owner/resource gates have cost zero. At fixed maximum value the proxy gives
exactly the minimum total action weight over physical choices, followed by
the minimum physical links. The preceding transformations prove both
inequalities. For unit weights this finds the smallest number of performed
actions. To preserve B as well, require its source arcs saturated using
lower bounds or an equivalent dominant source-priority cost. This can have
a different minimum cost from the unconstrained optimum.

For an integer implementation, normal physical packs have at most n physical
links when there are n owners, since links match distinct free terminals.
Multiplying action costs by n+1 and assigning link cost1 realizes the stated
lexicographic order. A still larger source priority protects B. Neither a
new private beta unit nor a second entry through the same beta BP is invented.

For direction-only exchanges with |J_i|=|Q_i|, let k=alpha and
D*=k-V_proxy(E). Every physical choice still has its original raw L, beta
count and numerical slack. The normal primitive bound V<=L+beta
gives the unified conditional count

    |T|+|M| <= area/2 + D*.                              (2)

When all sources are routed, D*=0 gives the coefficient-one count on the
stated action class. The new point is that D* is computed after jointly
choosing destructive exchanges, with all old-source conflicts in the same
network. No universal bound on D*, or universal availability of a complete
action set, is established here.

## 5. Arbitrarily long coordination; no action-matroid assertion

Resource-addition ranks in the earlier non-destructive switch/deletion
model are matroid ranks. Here actions add **arcs to old tokens**, not fresh
independent sinks. Their enabled-set gain need not be submodular.

For every n>=2 take alpha sources s_0,...,s_(n-1) and resources
r_0,...,r_(n-1). Initially only s_i for i>=1 has support, namely the private
r_i; r_0 is unsupported. There are no links, mixed owners or betas. Action i
withdraws r_(i+1 mod n) and replaces it by a private unit for s_i. All groups
are disjoint singletons, with at most one old witness; all abstract subsets
satisfy the simultaneous adapter. Define the enabled-choice optimum G(E).

**Theorem.** For arbitrary n,

    G(E)=n-1 if E is a proper subset of all n actions,
    G(E)=n   if all n actions are enabled.                (3)

**Proof.** Baseline payment n-1 is always available by choosing no action.
Full payment requires action0, since s_0 has no old support. This withdraws
r_1, so s_1 must have action1; inductively every action through n-1 is
necessary. Conversely all n actions give distinct private units to all n
sources. Therefore every proper enabled subset has optimum exactly n-1,
and the full set has optimum n. ∎

In particular all individual gains are zero, but all n actions together
gain1; the smallest successful action count is n. At n=2,

    g({0})=g({1})=g(empty)=0,  g({0,1})=1,

violating submodularity. A greedy algorithm requiring immediate positive
gain cannot start. In the proxy residual network, one augmenting path follows
s_0->r_1, reverses the old r_1 access to s_1, follows its action to r_2,
and continues until the unused r_0. It preserves all old paid sources while
rerouting their resources. This explains both the exact algorithm and why
its coordinated move cannot be replaced by independent local gain tests.

Some actually applied proper subsets may even lose old payments. Equation(3)
is about the best chosen subset of the enabled set, not the value of applying
that entire set. There is no claimed grid realization of this abstract family.

A beta-fork control has the same two-action synergy: initially two sources
use distinct beta BP entries, one interval group of two units and one private
whole-beta sink, so payment2. One action redirects an old source to an unused
group; another redirects a third source to the beta's old interval group.
Each alone pays2; together they pay3, retaining both old sources. Using the
same beta BP entry for both original arms instead leaves old payment1, as
required by the separate physical entry capacities.

## 6. The fully frozen fixed-P maximum as an exact application

Use the preceding186-point maximum with complete original units R,U,Q.
Let action0 be E: target a, withdraw group{U}, produce private K. Let action1
be F: target a, withdraw group{Q}, produce private J. Q has sole old witness
z; U is unsupported. The remaining unit R and all gates/links stay intact.
All four simultaneous adapter states are checked by physical forest cells.

The proxy has old access z->t_Q, action a->t_U for E and action a->t_Q for F.
The old source route is b->z->t_Q. Maximum payment2 uses

    a->t_U  (perform E),
    b->z->t_Q (retain the old unit; do not perform F).

The optimum has one action and one physical link, retaining b. Two action
arcs cannot both be used by a, so no second private unit is miscounted as a
payment for b. This derives the correct joint choice from the network.

If only F is enabled and action cost is zero, an unconstrained minimum-link
maximum instead switches from b to a: value1 and links0. Requiring old b
retained chooses no action and has value1, links1. Equal values therefore
still do not imply equal paid identities or identity-preserving minimum cost.

## 7. Validation and formal scope

```text
python3 develop/check_destructive_exchange_choice.py \
  --output output/destructive-exchange-choice-validation.json
python3 develop/check_destructive_exchange_allocation_formal.py \
  --lean /path/to/lean-4.33.0 \
  --output output/destructive-exchange-allocation-formal-validation.json
```

The independent primitive-pack DP checks546 applied-action subsets across57
models. For every enabled subset it compares lexicographic min-cost flow
against all physical subsets, with and without prescribed old paid sources:
1092 exact profiles pass. Controls include68 multiunit withdrawal groups,
32 repeated-target models, a genuine beta fork, distinct-versus-shared BP
entries, separate tokens with a common old witness, and rejection of a
multi-owner group. Arbitrary-length family tests exhaust all subsets through
n=6 and check larger flows at n=8,16,32,64; the proof establishes every n.
All four actual186-point direction states satisfy the simultaneous physical
adapter and agree with independently optimized primitive values/costs.

Four general Lean declarations in
[DestructiveExchangeAllocation.lean](../formal/SubQuorum/DestructiveExchangeAllocation.lean)
prove the capacity-one allocation kernel without axioms: chosen actions are
enabled; one target activates at most one allocated token; an injective proxy
allocation reconstructs physical selected-token incidences with the same
paid source identities; and physical allocations project back under explicit
selected-set cases. No enumeration is used in these statements. They do not
formalize the graph-to-grid adapter, single-owner group compression, beta
normalization, maximum-flow/min-cost-flow theorem or numerical corollary.
Those parts have the general written proofs and independent executable checks
above. The concrete186-board freezing remains verified in the preceding
module; no end-to-end formal optimized-grid claim is made.

The remaining research task is geometric coverage and stronger simultaneous
adapters for bent paths, capacity-two tiles and occupied adjacent bands. A
candidate must either satisfy the replacement contract or carry its extra
lost supports, new links and shared-resource conflicts explicitly. This
continuation performs no email operations and changes no submitted manuscript,
public main, PR3, shared CI or C4 primary result.
