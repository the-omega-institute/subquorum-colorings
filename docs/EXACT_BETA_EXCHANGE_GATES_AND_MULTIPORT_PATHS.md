# Exact beta exchange gates and simultaneous transfers through a balanced path

25 October 2026. Research continuation; the submitted manuscript is unchanged.

The component route construction in
[COMPONENT_ROUTE_CERTIFICATES_AND_GROUPED_BETA_RESERVES.md](COMPONENT_ROUTE_CERTIFICATES_AND_GROUPED_BETA_RESERVES.md)
was a sufficient lower bound. Here reversible alpha--beta prepayments are
compiled into unit exchange gates, with their original port witnesses retained.
The resulting ordinary route network has an **exact maximum compensation
value**. It also allows several compatible transfers through one balanced
component; one visit per component is unnecessary.

This is a concrete residual-network compilation and lifting theorem for the
existing original-terminal model. Its cardinality argument uses standard
integral-flow augmentation, already applied in
[SUPPORT_PRESERVING_COMPENSATION_AUGMENTATION.md](SUPPORT_PRESERVING_COMPENSATION_AUGMENTATION.md).
It is not a new general flow theorem or a proof of geometric route existence.
The general frozen-grid bound and any unconditional improvement of 5/6 remain
open.

## 1. Input and the gate construction

Use the finite normal form in
[COMPENSATION_FLOW_NORMAL_FORM.md](COMPENSATION_FLOW_NORMAL_FORM.md): original
alpha owners have two TP tips, beta two BP tips, and mixed one BP and one TP.
Owners have disjoint terminals. Links are declared TP--BP links between
different owners, and access witnesses lead from declared TP tips to original
unmarked interval units. Every source, mixed owner, whole beta and distinct
interval has capacity one. Excluded boundary intervals remain excluded.

Let C be **any** set of m allowed alpha--beta links with different alpha
owners and different beta owners. Neither maximality nor the two-tip injection
hypothesis is required. The m payments of C are reversible. If an earlier
cancellation C0 is immutable, first use its already contracted strand system
and declared access witnesses as the input; this theorem never releases C0.
It supplies no new geometric access theorem for virtual tips.

Construct E(C):

1. An alpha not paired by C is a unit source, with both original TP tips.
2. An original mixed owner is its usual unit gate, BP entry and TP exit.
3. For each pair c=(a,b) of C, introduce one **exchange gate**, with every
   original BP tip of b available for entry and every original TP tip of a
   available for exit. Its capacity is one for the entire pair. Traversing
   it means that the old link c will be removed.
4. Each beta not paired by C is a unit sink, with both original BP tips.
   Each original unmarked interval is its own unit sink.
5. Map every original link and access to these ports, retaining its actual
   terminal witness. A link whose two owners are paired together by C maps
   from an exchange gate back into itself and is omitted. Original mixed
   self-links were already excluded.

Parallel arcs may be kept or one actual witness retained per pair of mapped
ports: the source/gate/sink capacities make either choice equivalent in
cardinality, and all original terminals of a used exchange pair are released.

An exchange gate is not a new beta resource. It transfers a payment already
included in m. Only unpaired betas and original intervals are new sinks.

**All original ports are essential.** Literal contraction of c keeps only
the two unused tips as a virtual mixed strand. That operation fixes c and
can lose valid exchanges. E(C) instead reverses c when necessary, releasing
its used tips too. Section 4 gives an explicit example requiring both tips
that literal contraction discards.

## 2. Every compiled packing lifts without repeated credit

**Lemma 1.** Let a simple route packing in E(C) have value mu, use h exchange
gates and c actual TP--BP links. There is a legal original-terminal matching
and a set of different valid interval payments with

    compensation = m+mu,
    unpaid alpha count = k-m-mu,
    selected link count = m-h+c.                              (1)

Every original alpha paid by C remains paid; every beta used by C remains
consumed. Their pairings and routes may change. No original terminal, mixed
owner, beta unit or interval unit is used twice.

**Proof.** Remove precisely those h links of C whose gates are used. Retain
the other m-h links. For every compiled link/access use its retained original
witness. A used exchange gate frees both its original owners from the core:
its entering BP belongs to its beta, and its exiting TP to its alpha. The
two owners are different and were paired only with each other in C.

The retained core therefore uses no exterior owner. Source capacities,
mixed-gate capacities, exchange-gate capacities and sink capacities ensure
that different exterior pieces use different original alpha/beta owners,
mixed owners and interval units. At an original mixed gate, entry and exit
are its distinct BP and TP. Consequently all actual selected links are a
terminal matching, even when an exterior link uses a tip formerly occupied
by C.

Split a compiled route at each exchange gate. A route with h_r exchanges
gives h_r+1 actual original normal-form pieces: the earlier piece ends at
the beta of each split, and the next starts at that split's alpha. Its last
piece ends at an unpaired beta or at its witnessed interval. Thus all mu
routes give mu+h compensated pieces. Each used core beta ends exactly one
piece, and each used core alpha starts exactly one piece. Different interval
payments have different final strands and different original resources.

Adding the m-h retained payments gives m+mu. Each retained pair and each
exterior piece contains precisely one original alpha, so exactly k-m-mu
alphas remain unpaid, and all originally paid source/beta identities persist.
The selected links are exactly the m-h retained links and c exterior links.
This proves (1) and the nonreuse assertions. QED.

Notice why counting the h split beta payments in addition to the full m
would be wrong: these h payments replace h removed core payments. They
provide no net extra credit. The new mu payments use different new sinks.

## 3. Exact cardinality and canonical roots

Let nu be the maximum original compensation, and mu(C) the maximum route
packing in E(C).

**Theorem 2 (exact exchange reduction).**

    nu = m+mu(C).                                            (2)

**Proof.** Lemma 1 gives m+mu(C)<=nu. For the reverse inequality, start the
original normal-form flow network at the m direct routes C. Its source
arcs are saturated precisely at the core alphas, and its resource arcs
precisely at the core betas. Augment along simple residual source--sink
paths until maximum value nu. A simple augmenting path cannot return to
the super-source or depart from the super-sink. Therefore it cannot use
the reverse of an already used source or resource arc. Their identities
remain saturated throughout. This proves that some maximum flow preserves
all of these core boundary supports.

Take its difference from the initial C flow, directed in the initial
residual graph. Each initial core link has flow one. No feasible final
flow can put more than one unit on it, since its original alpha has total
outflow one. Its difference is therefore either zero or its unit reverse
arc b->a. All other original internal arcs start at zero, so their differences
are nonnegative forward arcs. Preserved boundary supports have difference
zero; positive source differences occur only at unpaired alphas, and positive
resource differences only at unpaired betas or intervals.

Delete residual circulations and decompose the remaining difference into
nu-m simple residual source--sink paths. An original paid beta can leave
such a path only along its core reverse arc to its paired alpha, while a
paid alpha can be entered only along that reverse arc. It has capacity one.
Replace every such reverse arc by the corresponding exchange gate; retain
the original forward link/access witnesses and original mixed gates.

A forward alternative link from a paid alpha to its own paired beta cannot
occur in a simple residual path: its alpha was just reached by that beta's
reverse core arc, so it would revisit the beta. This justifies deleting
self-return links in E(C), including parallel terminal witnesses. The
remaining paths give a legal packing of value nu-m in E(C). Hence
nu-m<=mu(C), establishing (2). QED.

This proves equality for the **maximum number paid**, not unrestricted
minimum link cost. Equation (1) gives the actual cost of each lifted packing,
but preserving all previously used beta resources can increase the cost of
an optimal-cardinality certificate; Section 4 gives a strict example.

**Two-tip injection corollary.** Under the previous note's F hypothesis,
choose the internal beta matching C, of size m=k-t. There is one unpaired
alpha in each two-mixed-ended demand path and one unpaired beta in each
reserve path, so E(C) has exactly t sources and s beta sinks. All original
mixed gates remain, and every internally paid alpha--beta pair becomes a
unit exchange gate. Then

    nu = k-t+mu(C),          deficit = t-mu(C).                (3)

Unlike the previous sufficient network Q, E(C) is exact and retains access
through all component interiors. Choose any convenient internal roots and
F-matchings: changing them cannot change mu(C), since both nu and m are
fixed in (2). Even different owner pairings with the same size m give the
same residual value. There is no need to optimize these root choices for
cardinality, provided every reversible exchange gate is retained.

This recasts the remaining geometric problem with t sources rather than k,
without assuming that their downstream reachability sets are separated.
The exact separator formula of the normal-form theorem applies to E(C).
In particular its deficit equals max_D(|Blocked(D)|-|D|), where D consists
of distinct exchange gates, original mixed gates, spare betas and interval
units. Exchange gates in D are capacities, not additional payment resources.
The missing universal ingredient is still a geometric inequality, not flow
integrality or an arbitrary choice of roots.

## 4. Two minimal abstract controls

These are abstract terminal systems, not claimed frozen-grid realizations.

**Port recovery.** Let A=(0,1), B=(2,3) be alpha, and x=(4,5) beta. Allow
exactly links (2,4) and (0,4); let TP2 access one interval J. Start at
C={(2,4)}, paying B with x. Fixing C pays only one; literal contraction
also keeps only unused TP3/BP5 and loses both useful ports. The exchange
gate keeps original BP4 as entry and TP2 as exit. It lifts to link (0,4)
and payment TP2->J, paying A and B with one link and one interval. In (1),
m=1,mu=1,h=1,c=1. Both previously occupied tips are legitimately released.

**Cardinality versus cost.** Let A=(0,1) be alpha, x=(2,3) beta, allow link
(0,2) and access TP1->J, and choose C={(0,2)}. There are no residual sources;
E(C) has value zero, so (2) correctly gives nu=1. Keeping the previously
used beta costs one link; the unrestricted maximum-cardinality solution
pays A directly with J and costs zero. Exact cardinality does not imply
unrestricted minimum-cost equivalence.

## 5. Several simultaneous transfers through one balanced path

Consider the balanced F-path

    m0, a_0, b_0, a_1, b_1, ..., a_(n-1), b_(n-1),

and choose C={a_i--b_i : 0<=i<n}, retaining actual F witnesses. Its exchange
gates are g_0,...,g_(n-1). The other internal F links run from the alpha
of g_i to the beta of g_(i-1). The compiled internal network is the directed
unit-vertex chain

    g_(n-1) -> ... -> g_1 -> g_0.

This describes the internal F arcs. Other declared physical links remain
additional arcs in E(C); the F-completion criterion below does not exclude
repairs using such extra links.

An incoming beta b_j can transfer to an outgoing alpha a_i exactly when
i<=j. The transfer uses every unit gate in the closed index interval [i,j].
Thus distinct transfers can share the same balanced component as long as
their index intervals are disjoint. A single capacity-one gate for the
whole component is unnecessarily restrictive; an unrestricted relay gate
would also permit invalid backwards transfers.

**Theorem 3 (multiport interlacing).** Delete h different alpha roots with
indices i_1<...<i_h and h different beta roots with indices j_1<...<j_h.
All remaining alpha and beta owners admit a perfect alpha--beta F-matching
if and only if

    i_1 <= j_1 < i_2 <= j_2 < ... < i_h <= j_h.                (4)

The empty-root case is included. Under (4), match each surviving alpha a_l
to b_(l-1) if i_r<l<=j_r for some r, and to b_l otherwise. This is a bijection
onto all surviving betas by adjacent F-edges. The transfers are precisely
the disjoint gate intervals [i_r,j_r].

**Proof.** Deleting vertices from a path leaves runs of consecutive surviving
vertices. A run has a perfect adjacent matching exactly when its length is
even: necessity follows from its vertex count; sufficiency pairs consecutive
vertices. The first surviving run has even length only if the first deleted
vertex is alpha. Between successive deletions the run is even only if their
types alternate. The last surviving run is even only if the last deletion
is beta. Since the original sequence is alpha,beta,...,alpha,beta, these
conditions are precisely (4), including adjacent deleted roots and empty
runs. They are also exactly disjointness of the closed index intervals.

Alternatively, under (4) the displayed matching shifts indices left once
inside each interval, omits its alpha left endpoint, and omits its beta
right endpoint. Outside those disjoint intervals it is the original identity
matching. Its images are all surviving beta indices exactly once. QED.

For example [0,1] and [3,4] permit two simultaneous transfers in a single
six-pair balanced component. They use four different exchange gates. With
two additional source alphas and two final original intervals, the checker
reconstructs eight payments with six actual links. This is an abstract
example of why the once-per-balanced-component restriction can be removed.

[BalancedMultiTransfer.lean](../formal/SubQuorum/BalancedMultiTransfer.lean)
proves, for arbitrary finite families of disjoint intervals and arbitrary
n, the matching map's bounds, adjacency, exclusion of deleted beta roots,
injectivity and coverage. The path-deletion necessity and the flow compilation
remain written proofs; the Lean statement does not formalize grid geometry.

## 6. Verification, discovery and practical limits

Reproduce the deterministic checker without optional dependencies:

    PYTHONDONTWRITEBYTECODE=1 python3 develop/check_beta_exchange_gate_reduction.py \
      --output output/beta-exchange-gate-reduction.json
    cd formal
    lean SubQuorum/BalancedMultiTransfer.lean

It lifts every compiled packing, checks actual terminal cancellation, distinct
interval payments, the exact link formula, and preservation of original paid
source/beta identities. Every result is compared with the unrestricted
normal-form solver. Bounded controls are implementation evidence, not the
proof of Theorems 2 or 3.

Recorded controls: 4,096 exhaustive two-alpha/one-beta original systems and
20,480 core choices; 800 larger seeded systems, with 71 strict failures of
protecting every core owner instead of allowing exchange; 32 independent
original-terminal enumerations over 256 terminal matchings; 66,197 multiport
root sets for n<=9 and 345 enlarged route models for n<=5. The main exhaustive
and random controls use 2,980 exchange gates in total. Original identities
of every residual separator and blocked source are also reconstructed.

The physical controls include bent fixtures with both actual matchings,
occupied adjacent bands, the frozen shared-gate and unported fixtures,
capacity-two rotors and branched stars, in all eight isometries and four
band offsets. All are checked feasible and fully frozen. These 480 carried
geometries give 536 partial-core controls. In this existing family, no lifted
packing needs an exchange gate. This is useful negative discovery evidence;
it is not evidence that exchange gates are unnecessary in every frozen grid.

An optional Z3 discovery script attempts a more restrictive two-alpha/one-beta
physical realization with one alpha having no direct/cap access and specified
ports. Two specified placements were UNSAT on their stated finite boards.
They do not exclude other shapes, placements, extra owners, or a frozen-grid
realization of the general exchange obstruction. The script and receipts
record the exact restrictions; they are not used in the general proof.

The next geometric target is a valid cut or route-count inequality in E(C)
for frozen bent paths, capacity-two tiles and occupied adjacent bands. It
must count original intervals and spare whole betas once, retain each
exchange/mixed gate's capacity, and use the ordered-chain structure rather
than treating an entire balanced component as either closed or freely
traversable. No manuscript increment or new general numerical bound follows
from the present compilation alone.
