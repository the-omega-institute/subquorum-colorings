# Exact reserve cost by residual terminal exchange

25 October 2026. Wenlin Zhang and Haobo Ma. Research branch only.

The [simultaneous-release theorem](SIMULTANEOUS_INTERVAL_RELEASE_AND_PHYSICAL_CIRCUITS.md)
counts releasable original intervals but permits additional links. We now
give the complete additional-link cost of every reserve target, retaining
the same prescribed paid sources and including mixed relays, both actual
beta BP entry gates, whole-beta units and beta-body forks. A zero reduced
cost cut gives the exact capacity at unchanged link cost. This applies
standard residual min-cost-flow theory to the complete compensation model;
it is not a new general flow theorem or a universal geometric inequality.

## 1. Start from a minimum-link payment of a fixed source set

Fix original alpha sources P that can all be paid, p=|P|, and retain only
their source arcs in the full whole-support flow. Every value-p flow then
pays exactly P. All terminal sink edges have capacity one and cost zero.
Their distinct identities form E: one private whole-beta unit per beta and
one original identity per unreserved interval. The original sink t has no
outgoing edge. Internal declared link arcs cost one; other internal arcs
cost zero. Actual beta tips and mixed gates retain their original capacities.

Let f be an integral value-p flow with MINIMUM original link cost c*. It
may be normalized to use a private whole-beta unit before a beta-supported
interval. Let U subset E be its used terminal identities. For candidate
original intervals F, put

    U_F=U intersect F,      z=|F minus U|.

We identify F with its interval-tagged terminal identities, so an interval
and a whole-beta unit never collide. The number z is the initially unused
candidate count. We seek the minimum link cost with AT LEAST r members of
F unused, permitting arbitrary internal rerouting but keeping all of P.

## 2. One terminal-exchange network

Take the residual network of f, with every original residual capacity and
cost. In particular a reverse used link costs -1. Remove t and all its
incident residual arcs; keep every other residual arc. Add new source a
and sink b. For each USED candidate terminal j in U_F add

    a -> node(j), capacity 1, cost 0.

For each UNUSED terminal h in E minus (U union F) add

    node(h) -> b, capacity 1, cost 0.

The second set includes unused whole-beta units as well as unused original
intervals, but excludes F. These auxiliary boundary arcs represent the
original residual edges t->j and h->t. All sharing inside the auxiliary
network uses the actual residual gate capacities. Write kappa_F(h) for the
minimum auxiliary cost of an integral h-unit a-b flow; kappa_F(0)=0, with
infinity when that value is infeasible.

**Theorem 1 (exact cost of simultaneous reserve).** For 0<=r<=|F|, the
minimum original link cost while retaining every payment in P and leaving
at least r members of F unused is

    c* + kappa_F(max(0,r-z)).                              (1)

The formula remains exact for normalized whole-support stem/fork packings.
In particular, an optimal reserve solution can keep every initially unused
member of F unused. Initial source identities survive, but initial internal
routes and all other used resource identities are not promised to survive.

**Proof, auxiliary flow to compensation.** Decompose an integral h-unit
auxiliary flow into a-b paths and cycles. The residual network of f has no
negative-cost cycle, since f is minimum cost at its fixed value. Every
auxiliary cycle is an original residual cycle, so a minimum-cost auxiliary
flow may be chosen without cycles. Close each a-b path by its represented
edges t->j and h->t. Distinct auxiliary boundary gates use different old
candidate units j and different formerly unused outside terminals h. The
closed paths form a feasible original residual circulation, with the same
cost. Adding it to f preserves flow value p and frees exactly h formerly
used F identities, activating none of the initially unused F identities.
Its original cost is c*+kappa_F(h). Normalization can only release further
intervals and keeps the link cost and payments, proving the upper bound
for the stated at-least target.

**Proof, compensation to auxiliary flow.** Let g be ANY competing integral
value-p flow meeting the target. Orient g-f in the residual directions of
f and decompose it into unit directed simple cycles. Each cycle costs at
least zero, again by optimality of f. A cycle avoiding t changes no terminal
identity. A simple cycle meeting t uses one reverse OLD used sink edge
t->j and one forward OLD unused sink edge h->t. Its gain in unused F
identities is +1, 0 or -1. A +1 cycle has j in U_F and
h in E minus (U union F); deleting its two terminal edges gives exactly an
auxiliary a-b path. If g frees h0>=r-z net additional candidates, its cycle
decomposition has at least h0 positive-gain cycles. Select any
max(0,r-z) of them and discard every other cycle. Residual capacities remain
valid for this subcollection, and its cost is at most cost(g)-c*, because
ALL discarded cycles have nonnegative cost. It gives an auxiliary flow of
the required value. Thus kappa_F(max(0,r-z))<=cost(g)-c*, proving the reverse
bound. This also proves the initially-unused-identity statement. QED.

Baseline cost optimality is essential to this pruning: a negative-cost
zero-gain cycle from a nonoptimal baseline could subsidize a reserve move.
The target is at least r unused intervals; normalization need not preserve
an arbitrarily prescribed number of used interval identities exactly.

The auxiliary minimum costs are nonnegative. Their successive marginal
costs are nonnegative and nondecreasing, by the usual integral min-cost-flow
value function. One successive-shortest-path run supplies the full finite
profile, not separate optimization over all subsets of F. For an additional
link budget B>=0, exact reserve capacity is

    z + max{h : kappa_F(h)<=B}.                            (2)

In particular the unlimited-budget endpoint agrees with the previous
formula |F|-p+nu_F. A disjoint matching of individually possible exchanges
does not suffice unless their internal gate capacities are also respected.

## 3. An exact cut at unchanged link cost

Choose any feasible residual potential pi with

    reduced(u,v)=cost(u,v)+pi(u)-pi(v)>=0

on EVERY residual arc, including the sink edges. Such a potential exists
because there is no negative residual cycle; distances from a virtual
zero-cost source to every node provide one. Give the auxiliary source and
sink the original potential pi(t). Then the boundary reduced costs are

    a->j: pi(t)-pi(j),       h->b: pi(h)-pi(t).             (3)

They are nonnegative, since they represent actual residual sink arcs.
Retain ONLY auxiliary arcs with reduced cost zero, INCLUDING this boundary
test. Call the resulting network A_0, and let mu_0 be its maximum flow.

**Corollary 2 (zero-additional-link capacity).** The maximum number of
members of F simultaneously unused at original cost c* is

    R_at_c*(F)=z+mu_0
             =z+min_(a-b cuts Q in A_0) capacity(Q).       (4)

**Proof.** The original and reduced costs of an auxiliary a-b flow agree,
because its endpoint potentials are equal. All reduced costs are
nonnegative. Thus cost zero is equivalent to using only zero reduced-cost
arcs. Apply Theorem 1 and max-flow/min-cut in A_0. QED.

This is invariant under the choice of optimal f and feasible pi after the
initial offset z is included. A bare unweighted reachability test in the
whole residual graph measures value-only reserve. Also, checking reduced
cost only on INTERNAL arcs is insufficient: omitting (3) can turn a
positive-cost exchange into a falsely free one.

## 4. Small controls that expose the two mistakes

**Reverse links are necessary.** Take alpha sources A,C, beta sinks B,E,
links A->B, C->B, C->E, and one candidate interval j supported only by A.
A minimum-cost baseline pays A by j and C by B: c*=1. Releasing j requires
paying A by B and C by E, at cost 2. The auxiliary path goes from j back
to A, into B, BACK along C's used link, then to E. Its link cost is
1-1+1=1. Suppressing negative reverse links leaves no auxiliary route at
all, although the release is feasible. This is an abstract exchange-rule
control, not a claim of a new frozen-grid realization.

**Terminal potential gates matter.** Take one alpha A, one beta B, link
A->B, and candidate j supported by A. Baseline A->j has c*=0; releasing j
costs one link. Choose a valid potential with pi(s)=pi(A)=pi(j)=-1 and
pi(t)=pi(B)=pi(B's tip nodes)=0. The internal residual path j->A->B has
zero reduced cost, as does the unused B output. But the represented reverse
sink edge t->j has reduced cost 1. Ignoring that boundary gate would
incorrectly declare a free release. The full zero-reduced-cost test gives
capacity zero, independently of this valid potential choice.

## 5. Physical consequences and exact profiles

On the original fully frozen board from the previous note, c*=1. Write
A5,C2,B4 for the disjoint support classes of its eleven-unit sector. The
new method gives these complete profiles:

| Candidate set | Initially unused z | Additional costs kappa(0),kappa(1),... |
| --- | ---: | --- |
| C's two adjacent units | 1 | 0,1 |
| All seven A/C units | 5 | 0,1,2 |
| All eleven A/C/B units | 9 | 0,1 |

Thus freeing both C units costs one extra link. Freeing all A/C-supported
units costs two extra links and forces payment through a beta-body fork.
The eleven-unit sector can never be entirely freed, even with an unlimited
link budget. These are exact profiles of the COMPLETE physical network,
with all other resources retained.

For q separated physical copies, all-q profiles follow from the previous
local lower bounds and geometric separation:

    F=C pockets:       z=q,  kappa(h)=h for 0<=h<=q;
    F=A/C supports:    z=5q, kappa(h)=h for 0<=h<=2q;
    F=eleven sectors:  z=9q, kappa(h)=h for 0<=h<=q.

Beyond the displayed ranges the auxiliary value is infeasible. For example,
at additional budget B the C pockets release exactly q+min(q,B) units.
This quantifies the cost of joint reserve; a merely positive local witness
does not bound that cost. It remains necessary to prove from general frozen
geometry that the relevant deficit neighborhoods have enough reserve AND
usable access from their unpaid sources. Reserve release alone is not an
additional payment theorem.

## 6. Verification and scope

`develop/check_residual_reserve_cost_profile.py` builds an independent
explicit flow/residual representation while leaving the existing full-flow
solver unchanged. Each auxiliary stage is lifted back to original edges
and checked for every capacity, vertex balance, original link cost, fixed
payment count, candidate identity avoidance and exact newly freed count.
All zero-reduced-cost maxima have checked cut capacities. Direct resource
reservation optimizations and independent primitive packings check the
entire cost profile, including the base board's every candidate subset.

Results: 6057 cost-profile models and zero-reduced-cost cut certificates;
25,370 comparisons at requested reserve targets; 5716 direct reservation
models and 2556 independent primitive comparisons. There are 360 seeded
fixed-paid-source systems, all 2048 candidate subsets of the physical
eleven-unit sector, and 48 physical stack profiles (q=1..16, three families).
The 3888 lifted auxiliary stages pass capacity, balance, cost and resource
identity checks. Fifty-eight profiles use reverse old links; the two small
explicit rule obstructions above pass independently. A further 292 candidate
checks change the optimal baseline by a zero-cost exchange and still agree
with the same direct optimum, including the candidate offset z.

The general cycle pruning, residual representation and min-cost reduction
are written proofs. The standalone Lean module formalizes the cycle
selection step and scoped counting/cost consequences; it does not
formalize a full flow decomposition, the physical adapter or max-flow/min-cut.
Finite profile checks support these proofs and do not replace them.

All six scoped Lean statements pass on the explicitly selected local
Lean 4.33.0, using only propext and Quot.sound. The local preflight reports
16 GiB physical memory, 40% free, and no active Lean/Lake process by comm
basename. Reproduce with:

```sh
python3 develop/check_residual_reserve_cost_profile.py --output output/residual-reserve-cost-profile-validation.json
python3 develop/check_residual_reserve_cost_formal.py --lean /path/to/lean-4.33.0 --output output/residual-reserve-cost-formal-validation.json
```

No new universal 5/6 improvement, no new unrestricted physical full-deficit
board and no external review are claimed. The 11 October submitted paper,
public main, star-forming/C4 sources and unmerged PR #3 remain untouched.
