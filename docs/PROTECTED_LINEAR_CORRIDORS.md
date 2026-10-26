# Protected linear corridors: extreme resources and polynomial joint repair

**Physical recognition continuation:** [uniform zero-capacity openings](UNIFORM_ZERO_CAPACITY_OPENINGS.md)
prove a two-state support audit for arbitrary feasible grids. A passing input
automatically satisfies the complete corridor contract below, including all
gate subsets. Balanced zero-capacity gates may change coarse forest cells;
common positive fine anchors preserve original resource identities.

26 October 2026. Wenlin Zhang and Haobo Ma. Independent research continuation.

The [mixed-resource dual parity theorem](MIXED_RESOURCE_DUAL_PARITY.md) handles
independent one/two-unit resource bundles in an arbitrary fixed mixed/beta
network. Here we give a geometric path class with arbitrarily many gate cuts
and original units whose joint operation choices reduce further to **one
minimum-cost maximum fork flow**, without a matroid-parity algorithm.

The key is simultaneous extreme-resource privatization. In a protected
two-ended linear corridor with at least two original units, only the leftmost
and rightmost units are needed. Each can be assigned exclusively to its own
boundary owner. Their required open-gate prefixes are disjoint. With exactly
one unit, retain one shared capacity-one output, not two private credits.
This works with arbitrary competing mixed relays and beta forks outside the
corridors, and preserves the physical links of every normalized packing.

This is a model-specific compression and geometric adapter, using standard
integral min-cost flow. It does not improve the universal 5/6 bound or cover
arbitrary branching, shared gates between different corridors, or pivots that
remove old supports. The original numerical inventory is retained throughout.

## 1. Protected-corridor contract

Fix the full original-owner/type/link network from the
[whole-support fork-flow theorem](WHOLE_SUPPORT_FORK_FLOW_AND_RESOURCE_CUTS.md).
All mixed capacity-one gates, the two actual BP entries of each beta, and its
one whole-beta output stay fixed. The external network can have arbitrary
competing routes and fixed interval support; it need not be an independent
baseline. Every physical state considered has the same original owners,
actual links, raw interval inventory, and fixed numerical ledger.

Each declared corridor has:

1. An ordered list of distinct original interval units u_0,...,u_(m-1).
   Different corridors have disjoint lists. Their other physical forest cells
   may be tracked by a simultaneous anchor bijection, but the original IDs
   and their count must be preserved.
2. A left boundary owner L and right boundary owner R, either of which can
   be absent. Owners may be alpha, mixed or beta; L and R may coincide, and
   different corridors may share boundary owners.
3. A linearly ordered list of primitive gates between the two boundaries.
   A gate lies before, between, or after units, never inside an individual
   retained unit. Each gate has a nonnegative integer opening fee. Different
   corridors have disjoint gate sets, although routes inside one corridor
   may share many prerequisites.
4. For every opened subset F, the complete corridor support is exactly

       L supports u_i iff all gates before u_i belong to F;
       R supports u_i iff all gates after  u_i belong to F.

   Remove absent boundaries and deduplicate coincident owner identities.
   No other owner supports a corridor unit. Every incidence on every
   noncorridor unit is fixed. No routing capacity changes.
5. Every gate subset is physically feasible and has precisely this support
   effect, with no other change to the compensation model. Actual physical
   opening cost is the sum over different opened gates.

This is a simultaneous support-only contract. BT-only tiles or unchanged
forest cell sets alone do not prove it: a direction change can remove support
from distant units. The [four-arm pivot ledger](P_FREE_PIVOT_INTERFACE.md)
must also rule out those effects. Section 5 provides an all-length completely
frozen realization, including both one-unit and two-unit shared corridors.

Every normalized whole-support pack uses at most one interval witnessed by
any particular owner: an ordinary owner is in one primitive, and a beta fork
uses one interval plus its one whole-beta output. This remains true when a
beta supports many intervals or is a boundary of several corridors.

## 2. Extreme-resource privatization in every state

For m=0 remove all corridor access. For m=1 keep the one original unit, with
its two possible boundary supports. For m>=2 keep only the following supports:

    L -> u_0          when the left prefix G_L is open;
    R -> u_(m-1)      when the right suffix G_R is open.

Here G_L is the set of gates before the first unit and G_R those after the
last. Omit absent boundaries. Keep all omitted units in the original raw
inventory, but suppress their corridor support for optimization. Their
numerical resources are not reclassified or erased.

**Lemma 1 (simultaneous extreme reassignment).** For every fixed gate state,
this support privatization preserves maximum payment and its minimum link
count. More strongly, every normalized physical packing can be transferred
to the privatized supports with the same paid sources, owner primitives,
selected physical links, and value.

**Proof.** A unit used from a corridor has witness L or R, by the contract.
If L and R are distinct, at most one used interval has witness L, and at
most one has witness R. If L can reach any u_i in the chosen state, all
gates before u_i are open. They include every gate before u_0, so L can
reach u_0. Similarly, if R can reach any corridor unit, it can reach u_(m-1).

When m>=2, reassign all L-witnessed corridor uses to u_0 and all R-witnessed
uses to u_(m-1) simultaneously. These are different original IDs. No other
owner can use them, and a retained use by the opposite boundary is included
in the same reassignment. No use from another corridor or noncorridor pool
can occupy them. Thus the reassignment is injective and creates no conflict.

When L=R there is at most one interval use from that owner in the entire
normalized pack. Its support is witnessed by at least one of the two ends;
reassign it to that end's extreme. The same disjointness argument applies.
For m=1 the original shared output is unchanged, so it can be used at most
once. For m=0 no use exists. Repeat independently over disjoint corridors.

No owner or link changes; beta forks keep their one interval and whole-beta
output. Thus every original pack transfers with unchanged link count. The
privatized supports are a subset of the original supports, giving the reverse
inclusion of feasible packs. Maximum value and minimum links therefore agree.
The construction also preserves any prescribed paid-source set. ∎

**Lemma 2 (disjoint payment prerequisites).** G_L and G_R are disjoint for
every nonempty corridor. All retained offer prerequisite sets are pairwise
disjoint across the family. Any opened gate strictly between the first and
last units can be omitted after Lemma 1 without changing the transferred pack.

**Proof.** A gate before the first unit cannot also be after the last unit.
This holds also for m=1, where the left prefix and right suffix partition the
line's gates. Different corridors have disjoint gates by assumption. The
transferred uses need only their respective extreme offers. Deleting other
open gates leaves every such offer's prerequisites open and changes no other
support. It cannot increase opening fees. ∎

The lemma resolves sharing among the many original prefix/suffix routes by
changing their resource assignments first. It does not justify charging an
arbitrary original route per gate independently. Every omitted interior unit
still contributes to the original raw count.

## 3. One polynomial flow for payment, activation fee and links

Replace every corridor by the supports above, and make each retained access
arc optional with a cost equal to its complete prerequisite fee:

    fee(L,u_0)     = sum_(g in G_L) fee(g);
    fee(R,u_last)  = sum_(g in G_R) fee(g).

For m=1 these are two possible incoming arcs to the SAME capacity-one
interval output. For m>=2 their outputs are distinct and each offer has its
own boundary owner. Empty prerequisites give an always-free offer. Keep all
ordinary external support arcs at fee zero and all beta output gates.

Let H=number of alpha owners + number of mixed owners, and K=H+1. In the
standard full fork network, give terminal-link arcs cost one and a corridor
offer arc cost K times its prerequisite fee. All other arcs have cost zero.
Compute an integral minimum-cost maximum flow.

**Theorem 3 (exact protected-corridor repair).** This one flow first maximizes
physical payment over all gate subsets, then minimizes the total actual
opening fee, then minimizes the number of physical links among all states
and packings attaining those first two optima. Its solution reconstructs an
optimal physical gate set and normalized pack. The construction is polynomial
in the explicit fixed network, corridor lists, gates and fee bit lengths.

**Pack to costed flow.** For any physical state and normalized pack, apply
Lemma 1. Retain just the prerequisites of the used extreme offers. This
does not lose a payment, increase fee, or change a physical link. By Lemma 2,
used offers charge disjoint actual gates. Each offer can be used at most once:
its output has capacity one; in the one-unit case the two offers compete
for that same one output. Thus their total fee equals the fee of their gate
union, even when different corridors share boundary owners. Map the pack
to the standard fork flow. Its cost is exactly Kf+ell, for the retained
activation fee f and the unchanged physical link count ell.

**Costed flow to pack.** Remove circulations from a min-cost maximum flow.
Every forward directed cycle contains a positive-cost physical link, so
none is needed. Normalize beta outputs by using each used beta's private
whole-beta output first. This releases at most one supported interval,
does not introduce an interval or physical link, and cannot increase fee
because every access cost is nonnegative. At a minimum-cost optimum it cannot
strictly decrease the scalar cost either. The usual fork-flow reconstruction
therefore gives an equally optimal normalized pack. Open exactly the union
of prerequisite gates of its used offers. Lemma 2 and the capacity-one
outputs make actual fee equal to the sum of retained offer fees. The protected
support contract makes the pack physically feasible in that state.

These two directions prove equality of maximum values and scalar cost
optima. In a normalized pack a selected link leaves an alpha or mixed TP
owner, and at most one selected link leaves any such owner. Hence
0<=ell<=H. Since fees are integers, K=H+1 makes every one-unit reduction of
fee dominate every possible link-count change. Minimizing Kf+ell thus gives
the stated second and third objectives exactly. The full network and retained
offer list are polynomial in the input; integral min-cost max-flow is a
standard polynomial algorithm. The checker uses finite gate enumeration as
an independent oracle, not as the algorithm proving this claim. ∎

**Old source retention.** Every original activation state contains the
zero-activation network. Starting from any old feasible paid-source set P,
augment in a minimum-fee maximum-payment state; simple augmentation preserves
old saturated source arcs. Normalization and Lemma 1 preserve P. Thus P can
be retained at the same maximum value and minimum fee. To minimize links
*subject to retaining P*, impose lower bounds one on those source arcs, or
an additional sufficiently large source priority in the fixed-value min-cost
flow. This need not preserve the unrestricted third-objective link optimum.
The validator independently compares the constrained three-objective optima.

This is a polynomial special case of geometric operation selection, not
a polynomial implementation of arbitrary resource matroid parity.

## 4. Why the hypotheses and single-unit distinction matter

**One original unit is not two endpoint credits.** Two direct alpha endpoints
of a one-unit corridor can each individually reach its sole unit. With all
gates open the maximum payment is still one, not two. With left/right prefix
fees 1 and 3, maximum payment costs one by opening only the left prefix.
Two private output tokens would falsely claim two payments. The shared sink
in Theorem 3 forbids exactly that error.

**Interior cuts need not be opened.** Let a four-unit corridor have a left
prefix of fee 2, an interior gate of fee 100, and a right suffix of fee 3.
Two direct alpha endpoints are both payable for total fee 5. Opening the
interior gate is unnecessary; original routes reaching deeper units have
overlapping prerequisites, while their extreme reassignments do not.

**An unprotected outside owner breaks privatization.** Take three units
u_0,u_1,u_2 with no gates, endpoints a,b each supporting every unit, and a
third alpha c supporting u_0. Original payment is three: c uses u_0, a uses
u_1 and b uses u_2. Privatizing a to u_0 and b to u_2 leaves only two payable
sources, even if c's old support is retained. Thus a corridor's exclusive
boundary support is essential. This is an abstract counterexample to the
unguarded extension, not a frozen-grid or numerical-bound counterexample.

Arbitrary branching or gates shared between corridors also lack the disjoint
prerequisite conclusion. The previous abstract shared-gate complexity
obstructions remain applicable; we claim no grid embedding of those arbitrary
incidences. A geometric adapter must establish the contract, rather than
declare every no-P region to be a protected line.

## 5. All-length completely frozen two-ended corridors

Use the existing [all-n frozen upper corridor](FROZEN_COORDINATED_PIVOTS.md),
whose explicit base (T83,M35), direction bits and eleven strict freeze waves
are serialized by the previous validators. Choose positive n_L,n_R and
q=max(n_L,n_R,6). Its left module has width 18+2q, selections 71+2q and
35 actual matching edges. Reflect it across the full width

    W=34+4q,

identifying the two empty far-right columns with their reflected pair.
The modules' selected and matching cells do not meet. Keep their lower
private cuts at V. The two original central BB interval units are

    J_0={(2,16+2q),(3,16+2q)},
    J_1={(2,17+2q),(3,17+2q)}.

Set the following gates initially to V, all other upper corridor tiles to H:

    left:  (2,16+2i),                  0<=i<n_L;
    right: (2,W-2-(16+2i)),            0<=i<n_R.

Opening a gate means V→H. Every gate is P-free, contains two diagonal T
sites, and has zero positive resource capacity in both orientations.

**Theorem 4 (all lengths, all subsets).** Every opened subset F is feasible;
all 140 actual endpoints remain strictly frozen in the same eleven waves.
Owners, types, physical links and all positive forest cell sets are fixed.
There are alpha=4, beta=4, mixed=10, and

    |T|=142+4q,  |M|=70,  raw L = slack S = 60+28q.

Only the supports of the two upper alpha endpoints a_L,a_R vary. Each
supports precisely {J_0,J_1} if all its side's gates are open, and nothing
otherwise. The central units have no other supporting owners. All other
unit supports stay fixed. Thus this is a protected two-ended corridor.

Writing l and r for the two side-completeness indicators,

    V(F)=2+l+r,          minimum links=2.                      (1)

With nonnegative gate fees and complete-side fees c_L,c_R, maximum payment
four has minimum activation fee c_L+c_R, and minimum links two.

**Proof.** The left corridor is the previously proved arbitrary-length
diagonal BT chain, and the right is its reflection. Identifying only their
empty final columns creates the two central original BB units without
identifying any P or T site. Consequently feasibility and each module's
strict rank witness remain unchanged. No later opening changes T or M.

Every varied tile is BT-only and P-free. It cannot contain a positive forest,
and a positive forest cannot traverse one of its BT pairs. Splitting/merging
bands at those gates therefore leaves all positive forest cell sets fixed.
Each gate's old vertical lower arm retains its boundary support and has no
new upper P boundary, by the old sealed-arm construction and its reflection.
There is no new central P boundary. Thus every noncentral support remains
as in the two old modules. Horizontally, only a_L and a_R can bound the
central no-P gap, and either boundary reaches J_0,J_1 exactly when every
gate between it and the center is H. This proves the exact support contract
for every subset, including a central segment with no or one P boundary.

The complete source kernel is also fixed: each a has no external exit;
the other two alphas b_L,b_R each pay through its own mixed z at one link
and a fixed private original interval. There are no further reachable exits
or beta fallbacks for these sources. Two central units can pay both distinct
a sources; one side's completion cannot pay its alpha twice. This proves
(1) and the exact link count. Each completed side is necessary to pay its
own a, so its entire prefix fee is necessary and sufficient. Finally the
modules have disjoint selected/matching cells; the inventory is

    16W/2 - (142+4q) - 70 = 60+28q.

Alpha equals beta, so the slack equals this raw inventory. ∎

**One-unit frozen variant.** Add the isolated selected site (3,16+2q).
Its adjacent sites are unselected and it is outside P. It creates no new
matching owner, and additional occupied neighbours cannot weaken the strict
freeze witnesses. It makes J_0 a zero BT pair, retaining only J_1. All
gate/support/source arguments stay the same. Now

    |T|=143+4q,  raw L=S=59+28q,
    V(F)=2+1[l or r],    minimum links=2.                     (2)

The maximum payment is three, for exact minimum opening fee min(c_L,c_R).
Even with both sides complete it is three, not four. Thus the distinction
between one shared output and two distinct extreme outputs has a genuine
all-length completely frozen realization. The fourth alpha remains unpaid;
this is not a counterexample to the numerical 5/6 inequality.

## 6. Reproducibility and formal boundary

Run from the repository root:

```sh
python3 develop/check_protected_linear_corridors.py \
  --output output/protected-linear-corridors-validation.json
python3 develop/check_protected_corridor_extremes_formal.py \
  --lean /absolute/path/to/lean-4.33.0 \
  --output output/protected-corridor-extremes-formal-validation.json
```

The [independent checker](../develop/check_protected_linear_corridors.py)
compares original and privatized primitive optima in every small gate state,
then compares the one costed full fork flow against exhaustive gate choice
with primitive packing. It separately checks conditional source-retention
optima, zero fees, coincident/absent/beta/mixed endpoints, empty corridors,
multiple corridors sharing owners, and the explicit failed unprotected rule.
The frozen family is checked for both variants and nine length pairs,
including (16,17) and (32,19). All states are checked up to eight gates;
larger cases check empty/full/each side/every singleton/every one-gate omission.
Full original resources, nonboundary supports, owner bodies, terminal links
and strict ranks are verified, not only the local target units.

The [Lean source](../formal/SubQuorum/ProtectedCorridorExtremes.lean) checks
general ordered-prefix/suffix inheritance, disjoint extreme prerequisites,
and distinct in-range extreme indices when at least two units exist. These
are non-enumerative kernels of the geometric argument. The full physical
adapter, normalized-pack reassignment, costed fork flow and grid embedding
are written proofs with independent executable checks, not end-to-end Lean.
The exact counts and audit scope are in the [execution record](../output/protected-linear-corridors-validation.json)
and [formal record](../output/protected-corridor-extremes-formal-validation.json).

The next issue is whether a residual geometric region can be decomposed
into protected line corridors with disjoint actual resources and gates, or
whether unavoidable outside support/branching defeats that decomposition.
This theorem resolves the linear protected class, while leaving that general
coverage question and universal 5/6 open. The submitted 11 October manuscript,
public main, PR #3 and shared CI are preserved; no mail operation is included.
