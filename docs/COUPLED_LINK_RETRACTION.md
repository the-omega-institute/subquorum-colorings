# Coupled old-link retractions: exact full-repair cost and a serial plateau

25 October 2026. Wenlin Zhang and Haobo Ma. Isolated research branch.

Continuation: [the frozen serial-fork escape theorem](FROZEN_SERIAL_FORK_ESCAPE.md)
proves a forced BB port or exterior-owner exit in any original frozen
realization of this skeleton, and gives a simultaneous common-phase
certificate with original interval identities counted once.

The [frozen gap family](FROZEN_GAP_CAPACITY_AND_LINK_RETRACTION.md) has an exact
one-retraction-per-deficit frontier because its beta bypasses are independent.
That frontier does **not** follow from the abstract strand axioms alone.
Here a connected, all-live, degree-two terminal system has deficit one but
requires arbitrarily many simultaneous old-link revisions before payment
increases. Every original beta remains available. This is an abstract
obstruction; no frozen-grid embedding of the serial system is claimed.

We also give an exact minimum-retraction reduction for full compensation
when each locked alpha has one active TP and no own interval support.
It uses the existing complete stem/fork flow, with one reward per actual
old link. It retains all mixed capacities, both actual beta BP entrances,
whole-beta capacities and original interval identities. It is a weighted
application of the established flow theorem, not a new general flow theorem.
A two-active-tip countercontrol shows why the hypothesis cannot be omitted.

## 1. Exact minimum full-repair revisions under a single-active-tip hypothesis

Use the finite whole-owner-support model and the full network of
[WHOLE_SUPPORT_FORK_FLOW_AND_RESOURCE_CUTS.md](WHOLE_SUPPORT_FORK_FLOW_AND_RESOURCE_CUTS.md).
Let k be the original alpha count and m the original mixed-owner count.
Let C be a set of declared alpha-to-mixed TP--BP links, with distinct
alpha owners and distinct mixed owners. A revision releases an earlier
cancellation constraint; it does not change physical M, points or resources.
A released link remains an available candidate and may be selected again.

Assume, **for every alpha a incident with C**:

1. W(a) is empty: a has no original own-support interval.
2. All outgoing declared links of a use the SAME actual TP as its link in C.
   Its other TP has no declared link. The restrictions concern actual tips,
   not just owner-level reachability.

Other alphas may have two active tips and arbitrary own support. Mixed
owners may form shared chains and cycles, intervals may have shared support,
and beta forks are allowed. No entry/exit separation assumption is made.
Assume unrestricted full compensation k is feasible. Otherwise no finite
release count gives full payment, and the claim below is not applied.

Let rho be the minimum number of links of C that must be released to permit
full payment. In the full network give a declared link e toll

    -1 if e belongs to C, and 0 otherwise;

all structural and resource arcs have toll zero. Let eta be the minimum
toll of a value-k integral flow. Then

    rho = |C| + eta.                                      (1)

For the joint objective, first minimize revisions and then total selected
actual links. Put B=k+m+1 and instead give link e toll

    1-B if e belongs to C, and 1 otherwise.                (2)

Every minimum-toll value-k flow has precisely rho revised links, and its
selected link count is minimum among all full repairs with rho revisions.
The total includes retained old links. Additional link operations exclude
them; this distinction matters when comparing a contraction's reported cost.

**Proof of correspondence, with old-link preservation.** If a full repair
retains K subset C, take its actual terminal matching L containing K. The
existing subset-of-links normalization produces a full stem/fork packing
using a subset L' of L and pays all k sources. Fix c=(u,v) in K. The alpha
of u has no own support, so its route must start with a declared link. The
only active tip is u, already matched to v in L; consequently c is its only
possible first link in L. Since normalization pays this alpha, c must remain
in L'. This holds simultaneously for every c in K. Thus some full packing
retains at least every originally required old link; normalization cannot
increase the required number of releases.

Conversely, a full packing using h distinct members of C retains these h
actual links. Releasing the other |C|-h members makes its selected matching
legal under the earlier constraints. Contracting the retained links first
is equivalent: each joins a different original alpha and mixed owner and
pays no alpha by itself; the packing's remaining links and original resource
assignments lift to this contraction. Hence

    rho = |C| - max_(full packings P) |C intersect L(P)|.    (3)

The existing complete flow-to-packing normalization preserves every selected
link, including beta-sink normalization, which changes only the final
resource. Each rewarded link carries at most one flow unit because its tail
is an original capacity-one alpha source. Thus toll equals minus the number
of different retained C links, proving (1). A single C link is rewarded once
even if both its source and its target gate appear in a conflict description.
Mixed gates, actual BP entries and original sinks retain their capacities.

There is no negative forward cycle: every negative arc leaves an original
alpha, which has no internal incoming arc. Zero-toll cycles in (1) can be
deleted without losing an old link; every forward cycle in (2) has positive
toll. Standard integral minimum-cost flow therefore applies. This assertion
is about forward cycles, not a claim that residual reverse arcs have positive
cost.

Every circulation-free packing has at most k+m selected links: at most one
outgoing link at each original alpha and each original mixed owner; beta
owners have no outgoing TP. Its toll in (2) is |L(P)|-B|C intersect L(P)|.
Since 0<=|L(P)|<=k+m<B, gaining even one retained old link dominates every
possible link-count difference. At a fixed retained count, minimizing toll
minimizes |L(P)|. This proves the lexicographic claim. QED.

**Why two active tips need a separate theorem.** Take alphas A=(a,a'),
D=(d,d'), mixed X=(x_BP,x_TP), beta Z, and one interval j. Declare only
C={a->x_BP} and a'->BP(Z); let W(D)=W(X)={j}, with W(A)=W(Z)=empty.
Retain C as one arm of A, use its OTHER TP a' to Z, and pay D with j.
All two sources pay with zero revisions and two selected links. X is live:
A can instead reach j through X. Nevertheless any full normal-form packing
that uses a->x_BP spends j on A, leaving D unpaid. A signed route reward
would incorrectly require one revision. The subset normalization can drop
that old dangling arm. This is precisely what hypothesis 2 prevents; the
example is checked independently by actual terminal-matching enumeration.
It is an abstract scope countercontrol, not a physical realization.

## 2. A connected serial family with deficit one and an unbounded plateau

Fix n>=2. Take n alphas A_1,...,A_n, n mixed gates X_1,...,X_n and n
betas Z_1,...,Z_n. Each alpha has one active TP a_i and one unused TP;
each beta has one active BP b_i and one unused BP. All owner supports and
the entire original interval set are empty. Declare exactly:

    c_i: a_i -> BP(X_i),                      1<=i<=n;
    a_i -> BP(X_(i+1)),                       1<=i<n;
    a_n -> b_n;
    TP(X_1) -> b_1;
    TP(X_i) -> b_(i-1),                       2<=i<=n.    (4)

The earlier cancellation set is C={c_1,...,c_n}. These n links have different
actual terminals, alpha owners and mixed owners. All n whole betas remain
available; no sink reservation is imposed. In particular X_1 and X_2 use
the SAME actual b_1 entrance and the SAME whole beta Z_1, not copies of it.

The owner graph is connected. Every mixed owner is reached from its A_i
and continues to its specified beta, so safe live-route pruning removes
none. Every actual terminal has candidate-link degree at most two: each
interior X BP has two possible alpha predecessors, and b_1 has two incoming
mixed links. Give active alpha/mixed TP phase 0 and target BP phase 1;
give every owner's partner the opposite phase. Every paired strand and
declared link then joins opposite phases. These necessary degree and phase
conditions do not establish a frozen-grid embedding.

Let Q subset {1,...,n} be the labels of links permitted to be revised; all
other c_i remain immutable and are contracted first. Retain all other links
and beta identities. Then ordinary and full-fork compensation agree, with

    V(Q) = n     if {2,...,n} is contained in Q,
           n-1   otherwise.                              (5)

Consequently, with at most R revisions permitted,

    V_R = n-1   for 0<=R<n-1,
          n     for R>=n-1.                              (6)

Exactly n-1 revisions are needed for full payment, despite initial deficit
one. For n=3 either single revision of c_2 or c_3 gives no improvement;
revising both gives the missing payment. For arbitrary n there is no
strictly improving move of any size smaller than n-1. The resource and
gate capacities are kept throughout this comparison.

**Lower baseline.** Voluntarily retain all C, including links whose revision
is permitted. Pay A_i through X_i into Z_(i-1), for i=2,...,n. These n-1
routes have different gates, BP entrances and whole betas. A_1 stays unpaid.
This proves V(Q)>=n-1 for every Q.

**Full-payment necessity.** With no intervals, a beta fork cannot give a
second payment: it needs a different original interval. Any full packing
therefore assigns all n sources injectively to the n whole betas.
A_1 can reach only Z_1, via X_1 or X_2. For i>=2, A_i can reach only
Z_(i-1) or Z_i, using respectively its old or alternate first link; for
A_n the latter is its direct link to Z_n. Induction forces A_i to Z_i
for all i: Z_1 is already taken by A_1, then Z_2 by A_2, and so on.
Thus every i>=2 must use its alternate first link. It uses the SAME actual
TP as c_i, so c_i must be released. This proves {2,...,n} subset Q.
There is no appeal to enumeration, local surplus or independent reachability.

**Simultaneous construction.** Retain c_1 and route A_1 through X_1 to Z_1.
For i=2,...,n-1 use a_i->BP(X_(i+1))->b_i, and use a_n->b_n.
Release exactly c_2,...,c_n. Each of X_1,X_3,...,X_n is used once, X_2
is unused, and each of Z_1,...,Z_n is used once. No actual terminal is
reused. This pays all n and proves (5)--(6). Every full solution has one
one-link route at A_n and n-1 two-link routes, so its minimum total actual
link count is exactly 2n-1. The retained c_1 is included in that total.
The signed theorem selects this repair, retaining the maximum one old link.
QED.

This rules out a deficit-only uniform bound on revisions, and rules out
requiring each intermediate release to give a strict gain, in the abstract
model. It does not rule out such bounds under additional frozen geometry.
It is also distinct from the older unbounded PP-rematching-cost theorem:
physical M and the original strand pairings remain fixed here; only earlier
TP--BP cancellation decisions change.
The serial construction is an explicit alternating reassignment chain;
its role here is to test the independent-revision strategy, not to claim
a new general result in matching or reconfiguration theory.

## 3. Several bundles: an exact counting inequality without repeated credit

Take disjoint serial systems of lengths n_1,...,n_q>=2. Put N=sum n_i,
ell_i=n_i-1, and sort these positive costs as ell_(1)<=...<=ell_(q).
Each system has one missing baseline payment. With at most R releases,

    V_R = N-q + max{h : 0<=h<=q, sum_(j=1)^h ell_(j)<=R}.   (7)

For a specified collection H of systems to become fully paid, the exact
required release count is sum_(i in H) ell_i. Necessity follows from their
different old-link identities in the serial proof. Sufficiency uses the
simultaneous constructions, with different source/gate/beta identities
between systems. Choosing the cheapest h costs proves (7). For equal length
n this becomes N-q+min(q,floor(R/(n-1))). No capacity is credited for a
partially released bundle, and no release is charged twice. This is an
exact separated-bundle theorem, not a formula for overlapping arbitrary
repair systems. A single serial system is already connected and all-live.

## 4. Frozen-family application and the remaining geometric task

On the earlier actual frozen gap family, delete only the entry arcs into
the proven exterior dead mixed branches. Those branches have empty support
and no link to another owner, so deleting these non-C arcs loses no paying
route or required C link. Keep all original owners and resource identities;
in particular keep the nonproductive C heads when c_i=0. Blanket live
pruning would incorrectly remove those constrained C links in that case.
All remaining outgoing links of each original alpha use its active TP,
and its own support is empty. Thus the full-repair theorem applies for
every original allowed capacity, returning rho=sum max(0,2-c_i) and minimum
total links 2q, in agreement with the geometric proof. The checker uses
c_i in {0,1,2} and separately exhausts all kept subsets in the UNPRUNED
physical model. Its adapter also checks the claimed dead-branch supports
and exits, rather than assuming a general fixed-link pruning theorem.

The new serial family shows exactly which extra independence was used in
the frozen formula. The next geometric question is whether frozen occupied
adjacent bands exclude arbitrarily long serial revision dependencies, or
force accessible original intervals or alternate beta entrances that break
them. Finding a physical embedding would strengthen the obstruction; proving
an exclusion or bounded bundle lemma could support a general compensation
proof. Neither direction is supplied by degree/phase tests alone.

No unrestricted frozen compensation theorem or numerical improvement of
5/6 is claimed. The submitted 11 October manuscript is unchanged.

## 5. Reproducibility and precise formal scope

Run from the repository root:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 develop/check_coupled_link_retraction.py \
  --output output/coupled-link-retraction-validation.json
cd formal
lean SubQuorum/CoupledLinkRetraction.lean
```

The computational receipt records separate counts for serial masks, exact
budget optima, random signed-flow/full-terminal-matching comparisons,
beta-fork repairs, separated bundles, the two-active-tip countercontrol and
the earlier physical family. The tests include all original interval and
beta identities; no external solver is required. Serial systems n=2..8
exhaust every released subset; n=9..12 check specified masks and full repairs.
The proofs above cover every n and every allowed subset.

The final run passes 1,116 serial ordinary/full comparisons, 42 exhaustive
serial budget optima, 1,184 separated-bundle subsets and 34 bundle budget
optima. There are 107 feasible random full targets, independently compared
against actual terminal matchings (five repaired targets use beta forks);
73 generated targets are correctly reported as not fully feasible. Including
the small serial and hypothesis controls, 3,581 actual terminal matchings
are checked. Eighteen previously established physical frozen-family boards
have independent feasibility, freezing and strict-rank checks, plus 504
UNPRUNED fixed-subset comparisons. These counts are not all different frozen
geometries: the serial/random models are abstract and the physical family
was already constructed in the earlier note. There are 254 signed-flow runs.

The Lean file checks the arbitrary-n forced injective resource assignment,
forced tail-link releases, their list-cardinality lower bound, the plateau
arithmetic, route-length count, reward/count identity, lexicographic reward
comparison, and an equal-bundle budget upper bound. It does not formalize
the network-to-assignment adapter, full flow normalization, physical pruning
or a frozen embedding. The full-repair reduction and physical adapter are
written proofs supported by independent computations. The formal receipt
lists all checked statements and their standard axiom dependencies.

Local Lean 4.33.0 was run as one process after measuring 16 GiB memory,
43% system availability and no existing lean/lake executable by wide-comm
basename enumeration. Final process enumeration is recorded separately.
No new Oracle review was requested in this milestone.
