# Interface compensation with local rerouting and protected payments

**Full-pool continuation:** the [exact interface singleton/repair profile](FULL_POOL_INTERFACE_SINGLETON_AND_REPAIR_PROFILE.md)
proves the complete original-pool behavior for every even height and every
subset of repairs in a stack. Local full payment and an independently full
interface matching can have deficit q-s after restoration. For the chosen
non-minimum-cost lower-route packs, theta=s>nu=0 when s>0 even on the full
pool; locally minimum-cost packs instead have nu=theta=s. It also determines
the exact cost of retaining old source identities.

25 October 2026. Wenlin Zhang and Haobo Ma. Research branch.

The previous [crossing-port lemma](CROSSING_MATCHING_PORT_LEDGER.md) fixed
local packs and matched interface alphas to the original units left unused.
Here the routes may change while **every previously paid source identity
survives**. We obtain the exact extra payment and a single joint withdrawal
criterion. Its proof specializes integral flow augmentation and the existing
[resource-gluing theorem](ENDPOINT_COMPONENT_RESOURCE_GLUING.md); it is not a
new general max-flow theorem. A completely frozen mixed-direction board
shows a strict improvement over a fixed pack on a restricted two-unit pool.
The universal 5/6 improvement remains open; the submitted manuscript is unchanged.

## 1. Hypotheses: one partition, one original pool

Use a disjoint even-by-even rectangle partition and the auxiliary matching
of the crossing-port lemma. Actual matching edges may cross the partition.
Keep every actual endpoint, with missing mates recorded as C ports. Let
I be the newly closed interface alpha owners, a=|I|. In each region R keep
only owners whose alternating paths were already closed before restoring
crossing edges. Write A_R for their number of alpha sources. Use the complete
local whole-support network: mixed gates, actual BP entry gates, private
whole-beta sinks, and both-arm beta forks are retained.

Fix an available set Q of **original resource identities**. It may be the
full pool or an explicitly restricted pool. The regions' original pools
Q_R partition Q. Local owners and private gates are disjoint; all local
arcs stay in their region. For F contained in Q let V_R(F) be the local
maximum with F intersect Q_R available. Put v_R=V_R(Q), p=sum_R v_R,
and D_R=A_R-v_R. Choose ANY maximum pack in each local system, and let
P_R be its paid source set. The union P has size p and is feasible, because
the local original pools and private gates are disjoint.

Form a conservative joint network by adjoining I as direct interval-only
sources with their actual whole-owner supports in Q. Each interface source
has capacity one; it can use one supported original unit. Delete its outgoing
terminal links. Omit all other interface owners and their gates/links. Thus
this theorem does not silently assume that a C half-path is a beta or a
new resource. Write h(F) for the bipartite matching rank from I to F, and
J(Q) for the joint maximum. All original interval sinks have capacity one
across the entire network.

## 2. Exact compensation theorem

**Theorem 1.** Under these hypotheses,

    J(Q) = min_{F subset Q} [ |Q minus F| + sum_R V_R(F) + h(F) ].  (1)

There is a joint pack of value J(Q) paying EVERY source of the initially
chosen P. It pays exactly p old sources and

    theta = J(Q)-p                                                 (2)

interface sources. Consequently theta is the exact largest additional
interface payment compatible with retaining P, and is independent of the
choice of the initial maximum paid sets P_R. Routes, used intervals and
link costs need not be preserved.

**Proof of (1).** Apply the resource-gluing argument to the disjoint local
networks and one direct-interface network of value h(F). For completeness,
any joint integral flow has at most |Q minus F| paths ending at original
units outside F. Removing those paths leaves at most sum_R V_R(F)+h(F)
payments. This gives the upper bound for every F, including private beta
payments in the local terms.

Conversely, choose a minimum cut U and let H be its source-side original
interval nodes; put F=Q minus H. Their sink arcs contribute |H|. Every
other crossing arc belongs to a unique local network or to the direct
interface network. Restricting U to each of these networks with only F
available gives cuts of capacities at least V_R(F) and h(F), respectively.
Accesses to H never leave U. Summing gives the reverse bound. Large
access/link capacities can all be p+a+1; a minimum cut has capacity at most
p+a, so none of those arcs is cut. Integrality gives (1).

**Proof that no old payment is sacrificed.** Start with the union of the
chosen local packs, represented as an integral flow. Initially disable the
interface source arcs, then restore them and augment to a joint maximum.
Choose each residual augmenting path simple, stopping at its first visit
to the sink. It never revisits the super-source. In particular it cannot
use the reverse of any source arc, since that reverse arc enters the
super-source. Every saturated source arc therefore stays saturated. All
p source identities of P remain paid after every augmentation.

In any joint flow, paths starting at old sources stay in their old local
network until they end at an interval or private beta sink. Restricting
to the old-source paths in region R gives a feasible local flow of value
at most v_R. Hence no joint flow can pay more than p old sources. Since
all p chosen sources survive, every extra payment is an interface source.
At the joint maximum it is exactly theta. Whole-beta output normalization
can change a terminal unit to that beta's private sink, but does not change
the starting source of any path. It retains P and uses no new interval.
This proves (2), including the case of initially unpaid old sources. ∎

The value J(Q) embeds into the full restored compensation model: every
retained closed owner has the same body, and every new interface alpha
has its real whole support. The full model may do better by using omitted
interface relays or betas. Its deficit therefore satisfies

    D_global <= sum_R D_R + a - theta.                            (3)

For any fixed initial local packs let nu be their unused-original matching
number from the earlier lemma. Their union with that matching is a feasible
joint pack retaining P. Thus theta>=nu. Formula (3) strengthens the previous
bound by exactly theta-nu for that choice of packs; it need not be strict.

## 3. A joint withdrawal witness, with each unit charged once

Subtract (1) from p+a. The exact unpaid interface count in this conservative
joint model is

    a-theta = max_{F subset Q}
      [ sum_R(v_R-V_R(F)) + (a-h(F)) - |Q minus F| ].              (4)

The maximum is nonnegative: J(Q)<=p+a. Full interface compensation while
retaining P is possible if and only if, for EVERY F contained in Q,

    sum_R(v_R-V_R(F)) + (a-h(F)) <= |Q minus F|.                   (5)

Here v_R-V_R(F) is a local withdrawal loss, a-h(F) is the interface
matching deficit on the retained pool, and |Q minus F| counts the removed
ORIGINAL units once. There is one joint witness F, not a sum of separately
optimized witnesses. Testing singleton withdrawals cannot replace (5).
At F=Q the expression is a-h(Q); at F=empty it can involve surviving
private beta payments through V_R(empty). Those cannot be erased from
the ledger. The criterion also handles a=0 and Q=empty.

This is a value criterion. The existing [exact reserve-cost
analysis](RESIDUAL_EXCHANGE_AND_EXACT_RESERVE_COST.md) is needed if link
cost must be retained. Failure of (5) is an obstruction to THIS conservative
joint network; it is not necessarily a failure of the full restored model,
a different auxiliary partition, or the numerical grid inequality.

**Corollary 2 (only shared interface units need be withdrawn).** Let K be
the original units supported both by a retained local owner and by an
interface alpha. The maximum in (4) has a witness with Q minus F contained
in K. In particular, if K is empty, theta=h(Q): the old maxima and the
best direct-interface matching can be attained together while retaining P.

**Proof.** If j is outside K, it is supported in at most one of the
disjoint local networks and the single interface network. Adding j to F
increases that network's maximum by at most one and changes no other
term. It lowers |Q minus F| by one. Thus the cut expression in (1) cannot
increase. Starting from a minimizer, add all such j; it remains a minimizer.
This proves the witness restriction. If K is empty, the only required
cut is F=Q, giving J=p+h(Q), as claimed. ∎

The increment bound follows by deleting the at-most-one path using j.
The rank submodularity proved in the earlier resource-gluing note also
shows that the cut expression is submodular. Its minimizing witnesses
are closed under union and intersection, so there is a largest retained
pool and a smallest withdrawal witness. This does not imply that testing
individual shared units is sufficient: their local withdrawal losses
may accumulate non-additively through mixed gates and beta entries.

## 4. Fully frozen mixed-direction physical exchange, every even W>=8

Take cropped(W) from [the raw-pool construction](FULL_POOL_SINGLETON_OBSTRUCTION.md)
and remove the isolated added selection (0,1). Coordinates here are those
of the cropped board, of shape (W+2) by 22. This point was not an original
freezing seed. The old matching and all its endpoint neighborhoods are
unchanged, so the all-W feasibility and freezing certificate from that
construction still applies. There are 40 selected vertices, 3W+10 actual
matching edges, and 6W+20 fully frozen endpoints. The numerical slack is

    11(W+2)-40-(3W+10)=8W-28 > 0.                               (6)

Use horizontal (two-row) bands in columns 0,...,13 and vertical (two-column)
bands in columns 14,...,21. Exactly two actual matching edges cross the
partition: (1,13)--(1,14) and (W,13)--(W,14). Restoring them creates one
interface alpha I, with ordinary tips (1,13),(W,13); the right-hand CC
relay is not an extra resource. There is one closed local alpha A with
tips (1,5),(W,5).

For the exchange control make ONLY these two original units available:

    j = (W/2,11,11),   physical cells (W,11),(W+1,11);
    l = (0,1,1),      physical cells (0,1),(1,1).                 (7)

The triple is the original (band,first,last) identity in the concatenated
partition bands. Other actual original units remain on the physical board
and in its numerical ledger, but are unavailable in this stated control.

The alpha A has no own support. Its bottom tip reaches j along

    (W,5)->(W,6),  (W,7)->(W,8),                              (8)

using two actual links through distinct closed mixed owners. Its upper
tip reaches l along the single outward link

    (1,5)->(1,4),                                             (9)

whose mixed owner has TP tip (1,3) and whole support containing l.
These endpoint coordinates follow directly from the two sealed column
lists; extra middle PP/M cycles at larger W alter none of them. Removing
(0,1) opens exactly the BB unit l in the top band. In the bottom band j
lies between the left and right owner columns; I supports j directly,
whereas its whole support does not contain l. All three indicated links
are internal to the left region. Their distinct-owner routes are disjoint
from I; no beta is used.

Choose the old local maximum by (8), paying A with j at cost two. It is
a maximum in VALUE, because there is only one old source. It is NOT a
minimum-cost local maximum: (9) pays A with l at cost one. Keeping the
chosen pack fixed leaves l, which I cannot use, so nu=0. Reroute A by (9)
and pay I directly with j. This gives J=2, theta=1>nu, at one link; there
are only two sources, so the value is exact. At least one link is necessary
because A has no own support, making the joint minimum cost exactly one.
Every old paid source survives, and the two final resource identities
are distinct. Equation (4) is zero for all maximizing witnesses, as full
payment is achieved. On all four subsets F of {j,l}, the right side of
(1) has minimum two.

This proves a strict fixed-pack improvement for every even W>=8 on the
stated restricted pool. It does not establish a strict gain against a
minimum-cost initial pack or against the full original pool. The W=8
fixture is 10 by 22, with 40 selections and 34 edges, all 68 endpoints
frozen, and positive numerical slack 36. Finite instances only check the
coordinate adapter; the argument above supplies the arbitrary-W claim.

## 5. Preserving minimum link cost can itself fail

An independent abstract control has old alpha A supporting {j}, a private
beta B, and a single A-to-B actual link; the new direct interface alpha I
also supports {j}. The local maximum is one at cost zero via j, leaving
nu=0. Reroute A to B and pay I with j: J=2 and theta=1, but now one link
is necessary. This is a model control, not a newly claimed frozen grid.
It proves that retaining the initially minimum link cost cannot be added
to Theorem 1 without further hypotheses.

A second abstract control exposes the capacity-two accounting issue. Two
old alphas enter the two DIFFERENT actual BP entries of one beta, whose
whole support is {j}; a new interface alpha also supports {j} directly.
The old maximum is p=2: one beta sink plus j, realized as a beta fork.
Although h({j})=1, the joint value stays two and theta=0. At F=empty,
V_R(empty)=1 and h(empty)=0, so (4) is (2-1)+(1-0)-1=1.
The second old arm and the interface source cannot both claim j. This
refutes the rule that the interface full-pool matching rank is always
additional to the old local maxima. It does not refute the exact cut
criterion, and it is not a new frozen physical or numerical grid example.

## 6. Reproducibility and formal scope

Run the dedicated verifier:

    python3 develop/check_interface_reserve_reoptimization.py \
      --output output/interface-reserve-reoptimization-validation.json

It constructs the actual whole-support network with separate BP entries,
first maximizes old-only flow, restores the interface source arcs, and
augments while checking saturated source identities after EVERY step.
It normalizes beta outputs and checks the resulting terminal matching.
Independent primitive enumeration checks all possible maximum old paid
sets on small controls; the entire availability lattice checks (1), (4)
and (5), the shared-unit restriction, and minimizer uncrossing. Physical
controls independently check feasibility, freezing,
partition compilation, the two prescribed routes, and all four pool cuts.

[Lean source](../formal/SubQuorum/InterfaceReserveReoptimization.lean)
formalizes the crucial simple-path source-arc protection implication,
its iteration, finite protected-source saturation, the cut/deficit
equivalence, and the compiled exchange's resource and route certificates.
It does not formalize integral max-flow/min-cut, the general physical
coordinate adapter, or the full all-W freezing theorem. These remain
written proofs with computational checks, not an end-to-end Lean grid theorem.

The recorded run passed 293 models, 1,084 joint withdrawal cuts, 1,134
minimizer-uncrossing pairs, 166 disjoint-interface additivity controls,
and 529 simple augmentations. It retained 403 protected old sources across
the separate controls and checked 72 possible maximum old paid sets by
independent primitive packing on 63 models. Eight fully frozen physical
heights W=8,10,12,16,20,40,64,128 passed, including the uniform serial
freezing certificate and both explicit routes. One forced two-entry beta
fork checks the double-spending obstruction. All 14 new Lean declarations
passed locally on Lean 4.33.0, with no warnings, placeholders, native
decision shortcuts or new axioms; two declarations are axiom-free and the
others use only standard Lean axioms. The preflight measured memory and
real Lean/Lake executable basenames, and preserved unrelated 4.35.0 jobs.

* [Computational receipt](../output/interface-reserve-reoptimization-validation.json)
* [Formal scope and receipt](../output/interface-reserve-reoptimization-formal-validation.json)
* [Lean audit](../output/interface-reserve-reoptimization-lean-validation.txt)
* [Actual W=8 restricted-pool fixture](../develop/fixtures/interface_reserve_exchange.json)

The next geometric task is to bound (4) for full original pools using
freezing and extremality, or to find a valid partition making (5) hold.
The exact criterion prevents an apparent surplus at one interface from
being spent again at another; it does not by itself supply that geometric
bound or improve 5/6.
