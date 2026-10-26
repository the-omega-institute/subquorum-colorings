# Mixed target directions: exact zero-capacity optimization and a positive-capacity parameter

26 October 2026. Wenlin Zhang and Haobo Ma. Independent research continuation;
the submitted 11 October manuscript is unchanged.

## Result and relation to previous work

We extend the physical protected-corridor optimizer from a uniform target
direction to **arbitrary mixed target directions**, under the precise hypothesis
that every original owner/resource incidence is increasing in the set of changed
gates. If every variable tile has capacity zero, one minimum-cost maximum fork
flow exactly optimizes payment, actual gate activation fee, and physical link
count, in that order. Gates in both directions can contribute real payments.

If there are p positive-capacity variable tiles, the same general problem is
solvable using 2^p such flows. The remaining number of zero-capacity variables
appears only polynomially. No parameterized enumeration of their subsets is
needed. This extends the available class of exact mixed-direction compensation
algorithms; it does not assert a polynomial algorithm for unbounded p.

The general geometric argument is below. Finite enumeration only audits its
implementation. We reuse, and do not claim as new, the whole-support fork-flow
normal form, protected-corridor extreme reassignment, and standard integral
min-cost flow from the preceding notes:

- [Signed mixed support](SIGNED_MIXED_SUPPORT_COMPILER.md): exact three-snapshot
  support compilation and polynomial all-subset monotonicity recognition.
- [Protected corridors](PROTECTED_LINEAR_CORRIDORS.md): extreme reassignment
  and costed full fork flow for an abstract protected-corridor contract.
- [Whole-support fork flow](WHOLE_SUPPORT_FORK_FLOW_AND_RESOURCE_CUTS.md): actual
  beta entries, private whole-beta outputs, and competing mixed owner capacities.
- [Uniform positive-capacity matching](FULL_ROUTING_WEIGHTED_MATCHING.md): the
  stronger polynomial algorithm for the previously recognized uniform class.
  Our general mixed-target parameterization does not replace that result.

## 1. Hypotheses and objective

Fix a feasible even rectangular board (T,M), with its actual matching M. Tiles
are the aligned 2-by-2 tiles; each has a prescribed initial H/V direction.
Choose distinct P-free variable tiles g_0,...,g_(h-1), where P is the vertex
set of M. Changing a tile reverses its initial direction; hence its target
direction is fixed and the targets may be mixed. Fixed tiles never change.

Use the restored whole-owner model: owner bodies, original terminal types,
actual directed TP-to-BP links, capacity-one mixed owners, the two individual
entries of each beta, and one private whole-beta output. These are invariant
under the P-free changes. For each state F subset {0,...,h-1}, let W_F(o)
denote the supported original interval units of owner o. All states are
feasible. Units use the common fine-anchor identification; local positive
children are paired between directions as in the signed compiler, and are
never pooled as separate phase resources.

The required support hypothesis is the **whole all-state condition**

    F subset F' implies W_F(o) subset W_F'(o), for every original owner o.

Endpoint monotonicity alone is insufficient. The signed recognizer certifies
this condition in polynomial time, or returns an actual adjacent-state
owner/unit loss. Rejected inputs are outside the theorem; rejection says
nothing by itself about the truth of a desired compensation inequality.

Let kappa(g)=2-|T intersect g|, in {0,1,2}, and let w_g be a nonnegative
integer activation fee, paid once if g changes. The objective is lexicographic:

    maximize paid alpha sources;
    minimize sum_(g in F) w_g;
    minimize selected actual physical links.

We also allow a prescribed paid-source set R that is feasible initially.
The support hypothesis preserves its feasibility in every state. The APIs
take this feasibility as a precondition; they do not use exponential primitive
enumeration to establish it. R may in particular be the paid sources of an
existing checked packing.

## 2. Final-gap projection when all variable capacities are zero

Assume kappa(g)=0 for every variable tile. Such a tile has no positive fine
anchor in either direction. Thus every original positive anchor is outside
the variable tiles, and its own direction is fixed throughout the family.

Let the **final configuration** change every variable tile. In every final
canonical H and V band, split at P columns into maximal no-P gaps. Each gap
has its ordered original positive anchors, nearest left/right P-column
owners (if present), and its variable tiles in axial order. All gates in
such a final gap target that gap's direction. Each variable gate belongs
to exactly one such gap, and each original unit belongs to exactly one gap.
There is no gate inside a positive anchor. Gaps with no units are retained
geometrically but offer no payment.

For a unit u in one such gap, define G_L(u) and G_R(u) as the gates strictly
between it and the left/right boundary, respectively. These are actual gate
IDs, not copies for different owners. If a boundary is absent, omit that
offer; if both boundaries belong to the same global owner, their accesses
are alternatives for the same owner/unit incidence.

**Theorem 1 (exact mixed-direction final corridors).** At every state F,

    u in W_F(o) iff
       (o=L and G_L(u) subset F) or (o=R and G_R(u) subset F).

No other owner supports u. This includes all initial support: no separate
legacy pool or assumed final-phase-only support rule is added.

**Proof, soundness.** A completed left or right prerequisite set makes every
intervening tile have the unit's fixed direction D. The nonvariable tiles
already have D in the final gap, and the path to the appropriate P boundary
has no intervening P column. Consequently that whole boundary owner actually
supports the unit in F. Changes outside this corridor cannot cut its internal
direction path. An empty prerequisite set gives genuine unconditional support.

**Proof, completeness.** Suppose o supports u in F, and let D be u's fixed
direction. Let C_D be *all* gates whose target is opposite D, and set

    F' = F union C_D.

Support monotonicity preserves o's support of the same original unit u in F'.
Every variable tile that is opposite D in the final configuration is now
opposite D in F', and all fixed tiles keep their final direction. Hence the
actual D band containing u in F' is contained in u's final D band. An
actual no-P route from u to a P-column owner can only reach the corresponding
nearest P boundary of its final gap: a shorter band may remove a boundary,
but cannot insert a different P boundary, since all variables are P-free.
Choose a side actually witnessing o in F'. This also covers the case where
the two final boundaries have the same owner.

Every gate on this final-gap boundary route targets D. It must be changed
in F' to permit the actual D route. But we added only gates in C_D, none of
which target D. Therefore every required gate was already in F. This is
exactly the appropriate G_L(u) subset F or G_R(u) subset F. The identification
of u is unchanged because no variable tile contains a positive anchor. ∎

This proof uses the entire support-monotonicity hypothesis, not merely initial
support preservation. It also explains why the zero-capacity assumption is
substantive: a positive local resource has no fixed direction D to which the
argument can be applied across all states.

The compiler needs the signed recognizer's at most three snapshots and one
final mixed snapshot, hence at most four physical snapshot calls (possibly
duplicates). It traverses both final axes and all gaps. It enumerates neither
gate states nor packings.

## 3. Exact fees without repeated credits

Theorem 1 supplies the full protected-corridor contract simultaneously, rather
than testing corridors separately. Distinct corridors have disjoint original
unit lists and disjoint actual gate sets; no outside owner supports their
units. Owners themselves may occur at many boundaries and may be mixed or beta.

In a normalized packing an owner witnesses at most one interval unit. In
every nonempty gap, reassign a left-witnessed use to its first original unit
and a right-witnessed use to its last original unit. With at least two units
these IDs are distinct. With one unit retain a single shared capacity-one
output. If L=R, retain at most one interval use by that owner, using a side
that witnesses its access. This reassignment preserves paid sources, owner
primitives and actual links; it is simultaneous and injective across all gaps.

The gates before the first unit and those after the last unit are disjoint,
even in the singleton case: a zero-capacity gate contains no unit. Gate sets
in different gaps are disjoint as well, including between H and V gaps.
Consequently **all retained extreme offer prerequisite sets are pairwise
disjoint**. Every used gate fee is charged exactly once. Neither two ends of
one original unit nor two directions of one operation create two resources.

Interior gates and gates of unused offers can be removed after reassignment
without losing a retained use. Their fees are nonnegative, so this cannot
make the objective worse. The raw resource inventory is unchanged; suppressed
interior offers do not delete original units from the numerical ledger.

**Theorem 2 (one exact full flow).** Under Section 1 and zero variable
capacity, one costed full fork flow solves the stated lexicographic objective,
including initially feasible prescribed sources.

**Proof.** Give each retained extreme support arc fee equal to the sum of its
actual prerequisite gate fees. Retain the full owner/link network, mixed
capacity gates, separate beta entry gates, private beta outputs, and original
capacity-one interval outputs. With H=|alpha|+|mixed|, assign support arc cost
(H+1) times its fee and each physical link cost one. Compute a min-cost maximum
integral flow. This is the existing protected-corridor construction.

Any normalized physical pack transfers to extreme supports with the same
payments and links. Open only its used prerequisite sets. Their disjointness
makes flow cost exactly (H+1) times actual activation fee plus link count;
the opening fee cannot exceed the original state's fee. Conversely, a costed
flow normalizes through the existing whole-beta output construction, without
increasing fees or links, and becomes a physical pack after opening the union
of its used prerequisites. Theorem 1 supplies every used support in that
single actual state. Each original unit still has just one output capacity.

Normalized packs use at most H physical links. Thus the integer cost first
minimizes actual fees and then links, while maximum flow first maximizes
payments. Initially feasible prescribed source arcs can be retained at
maximum cardinality by the standard source-preserving flow augmentation
property; alternatively apply the preceding source-preservation theorem.
The implementation uses a dominating source reward to select those arcs.
The extreme reassignment preserves their individual source identities. ∎

## 4. Arbitrary positive capacities: parameterize only positive gates

Let J={i:kappa(g_i)>0}, p=|J|, and Z be the other gate indices. The entire
mixed-target input still has to pass the signed all-state recognizer.

**Theorem 3 (2^p polynomial exact optimization).** The general capacity
0/1/2 input under Section 1 can be solved with 2^p full costed fork flows
and polynomial work per branch. The algorithm does not enumerate subsets
of Z, even when |Z| is arbitrarily large.

**Algorithm.** For every A subset J, fix the positive gates in A at their
target directions, and the other positive gates at their initial directions.
Treat these gates as fixed tiles. The only remaining variables are Z, with
their original initial directions and mixed targets. Run Theorem 2, and add
the fixed branch fee sum_(i in A) w_i. Compare branch answers lexicographically.
Return the winning branch's actual positive changes plus its used zero-gate
prerequisites, with global gate IDs.

**Proof.** The original all-state monotonicity restricts to every fixed-A
subcube: A union F subset A union F' whenever F subset F' are zero-gate
sets. The unit correspondence in a branch agrees with the global original
correspondence up to a fixed bijection. Positive gates now have fixed physical
anchors, so Theorems 1 and 2 apply to every branch. Prescribed initial sources
remain feasible at A and throughout that branch.

Every global state has one unique decomposition A union F with A subset J,
F subset Z, so it occurs in a branch. That branch's optimizer attains at
least its payment, and, at equal payment, no greater total fee or link count.
Every branch solution conversely reconstructs an actual global state and
valid packing. Comparing all branches is therefore exact. Fees of positive
gates are charged once as fixed branch costs, including when two children
are used; zero-gate fees are charged once by Theorem 2. A positive gate unused
by a returned pack still costs its branch fee; the algorithm never silently
refunds it. If avoiding it is beneficial, that state appears in another
branch. Unit sets of different branches are never unioned. ∎

The result is fixed-parameter tractable in p, not in the total number of
variables. For p=0 it uses one flow. For a uniform target family, prefer the
existing polynomial matching algorithm when applicable; an exponential
parameterization there is unnecessary.

## 5. Checks and formal scope

Run `python3 develop/check_mixed_zero_corridor_optimization.py --output
output/mixed-zero-corridor-validation.json` from the repository root. The
production APIs are `compile_zero`, `solve_zero`, and `solve_parameterized`.
The internal `certified_monotone` premise is used only after a global signed
certificate; ordinary callers leave it false. It is not an endpoint shortcut.

The checked run has 112 accepted and two rejected models; 144 zero-capacity
states agree exactly between the final-corridor compiler and physical rebuilds.
334 physical state optima agree with independent primitive optimization;
318 single-flow and 360 parameterized lexicographic optima agree with an
independent all-state primitive DP. These include 24 nonempty prescribed-source
optimization checks. Positive-capacity inputs are explicitly refused by the
zero-only adapter. The earlier old-phase-birth family is handled by branching
its one positive gate, rather than falsely applying Theorem 1 to it.

A board and its separated transpose provide completely frozen fixtures with
both H-target and V-target payment chains. For four/eight zero gates, all
16/256 states are physically rebuilt and the exact support identities and
payment formula checked. Payment rises from 4 to 8, with four links; weighted
activation minima are 7 and 15 in the recorded profiles. Two additional
frozen mixed-target fixtures have two positive gates (capacity two or one),
four branch flows, genuine paid alpha sources and shared resource competition.
The capacity-two result pays 8 for fee 12; capacity-one pays 6 for fee 7.
Four freezing-certificate replays check 1120 strict events in total.

A 36-zero-gate mixed-target fixture represents 2^36=68,719,476,736 states.
It is solved by one flow with optimum payment 8, fee 36, links 4. Production
is run with audit subset enumeration and primitive optimizers disabled;
the large state space is not enumerated. This is an implementation audit,
not the proof of polynomiality or all-state correctness.

[Lean source](../formal/SubQuorum/MixedZeroCorridors.lean) verifies two arbitrary-
size logical kernels without axioms: final-corridor projection from monotone
support, saturated-cut completeness, soundness and cut-avoiding prerequisites;
and inheritance of monotonicity under a fixed-coordinate embedding. These
are logical parts of Theorems 1 and 3. The physical gap/anchor geometry,
extreme reassignment, costed-flow equivalence and optimization algorithm have
written proofs and executable checks, and are **not end-to-end Lean verified**.
The local runner measures memory and actual lean/lake process basenames
before each executable invocation, and audits the declarations for axioms.

## 6. Consequences and remaining geometric question

This closes a genuine gap between arbitrary mixed-direction support compilation
and actual joint fee optimization: all zero-capacity gates are now eliminated
polynomially, and positive gates alone control the general branching cost.
It provides an exact way to search for the cheapest actual compensation of
a checked old source set while retaining all competing mixed and beta routes.

It does not yet force a particular geometric input to have enough payment.
The general obstruction-removal question remains: which physical bent paths,
occupied bands and capacity-two arrangements guarantee the disappearance of
deficient resource trees, or imply a uniform cross-component lower bound?
Nor does the signed recognizer cover families that actually lose support;
those still require destructive-support repair and its explicit old-resource
ledger. No universal improvement to the existing 5/6 bound is claimed here.
The submitted manuscript, public main, PR #3, shared CI, C4 results and
correspondence are unchanged by this continuation.
