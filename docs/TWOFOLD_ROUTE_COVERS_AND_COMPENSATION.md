# Low-congestion route covers give simultaneous compensation

23 October 2026. Authors: Haobo Ma and Wenlin Zhang.

The exact strand-flow normal form turns simultaneous compensation into a
unit-capacity routing problem. This note gives a sufficient certificate that
allows several candidate routes per source while charging every shared mixed
owner and every original resource by its actual identity. A low-congestion
certificate gives full compensation, preservation of specified saturated
resource sinks, and an average link-cost bound. An overloaded certificate
still bounds the unpaid demand sharply. The proof uses standard integral
flow and circulation theorems; no new general flow theorem is asserted.

On the earlier real-grid parity-hole family, two independent exits per source
also give an exact compensation formula after arbitrary reservations in the
declared horizontal terminal network. Geometric existence of such certificates
for arbitrary frozen grids remains open.

## 1. Interface and certificate

Use the finite strand system and directed, witnessed network of
[the compensation normal form](COMPENSATION_FLOW_NORMAL_FORM.md), Sections 1--3.
There are k alpha sources. The capacity objects are mixed owners, whole beta
owners, and distinct original interval units. Each has capacity one; a beta's
two BP terminals supply only one resource. Mixed owners supply no payment.
Links are witnessed TP--BP pairs and cost one. Access arcs and split/boundary
arcs cost zero. Normal-form routes are simple source-to-resource paths.
Owner-disjoint routes ending at different resources give legal simultaneous
terminal cancellation and interval allocation. Let nu be the maximum number
of such routes and delta=k-nu.

Fix an integer m>=1. Supply exactly m simple witnessed routes from each
source. These are certificate occurrences, so repeated copies are allowed.
Every occurrence uses each mixed owner at most once and ends at one resource.
For each capacity object u let ell(u) be the number of occurrences using u.
Let L be the sum of their link costs and put

    E_m = sum_u max(ell(u)-m,0).

The sum ranges over actual capacity identities, not route incidences or
terminal presentations of a single resource. Distinct physical cap witnesses
must satisfy the normal-form grid adapter's nonconflict hypothesis as well.
The certificate may be applied after contracting an immutable earlier C0;
then all routes use the current free terminals and unreserved resources.

## 2. Full compensation and cost by integral layers

**Theorem 1.** If ell(u)<=m for every capacity object u, there exist m complete
route packings, each paying all k sources, whose combined use of every
witnessed arc is at most its use by the supplied certificate. In every packing,
each resource sink with ell(u)=m is used. At least one packing has cost
at most floor(L/m), while retaining all those resource sinks.

The packings can switch between certificate prefixes and suffixes at common
vertices. They need not choose an intact supplied route for each source and
need not preserve its source-to-resource assignment. The conclusion concerns
saturated resource sinks, not preservation of saturated internal mixed owners.

**Proof.** Restrict to the union of supplied witnessed arcs and sum their
unit path flows into an integral flow F of value mk. Each source boundary
arc has value m. Each mixed split arc and resource sink arc has value ell(u).
Every link or access arc exits an alpha or mixed owner; its aggregate flow
is therefore at most m. Thus 0<=F_e<=m on every arc. Giving each witnessed
link/access arc unit capacity does not change legitimate route packings:
at most one path can leave its alpha or mixed owner.

For m>1, seek one value-k flow f subject to integral arc bounds

    max(0,F_e-(m-1)) <= f_e <= min(1,F_e).                 (1)

The fractional flow F/m satisfies (1): for F_e=m both bounds force one;
for 0<F_e<m the lower bound is zero and the upper bound one; for F_e=0
both bounds are zero. Add a return arc from super-sink to super-source
with lower and upper bounds k. The standard integral feasible-circulation
theorem supplies an integral f satisfying (1). The residual F-f is a
nonnegative integral flow of value (m-1)k with every arc at most m-1.
Repeat. The m=1 case is F itself. This produces m integral value-k layers
whose sum is F before cycle removal.

Keep all circulation cycles during peeling so that the residual induction
continues to apply. Afterwards remove directed cycles in each layer and
decompose the remaining flow into k source-to-sink paths. Each source arc
has capacity one, so every source occurs. Mixed owners and resource sinks
also have capacity one, giving a legal route packing. Cycle removal only
decreases the combined arc uses and total nonnegative link cost.

If a resource sink arc has aggregate value m, it has value one in every
layer, as no layer can exceed one. Such an arc lies on no directed cycle:
the original super-sink has no outgoing arcs. It therefore survives cycle
removal in every layer. The same statement holds for source boundary arcs.
Internal mixed split arcs may lie on circulation cycles, so no corresponding
preservation conclusion is made for them. The m final costs sum to at most L;
one is at most floor(L/m), and all preserve the saturated resources. QED.

In particular, to preserve a previously used resource set R, it is sufficient
that every resource in R has certificate load m. The old source-resource
pairing is allowed to change. This is distinct from freezing the old matching
or the old assignments, which can obstruct augmentation.

## 3. Sharp deficit from overloaded units

**Theorem 2.** Without a load bound, every m-fold certificate satisfies

    m delta <= E_m, hence delta <= floor(E_m/m).           (2)

For m=2, excess at most one already forces full compensation. The average
cost and saturated-resource conclusions of Theorem 1 are asserted only under
its zero-excess hypothesis.

**Proof.** For a set Z of capacity objects, let U_Z be the sources that cannot
reach any surviving resource after deleting Z. Each of the m supplied routes
from every source in U_Z meets Z. Counting occurrences, with multiple hits
allowed on the right, gives

    m|U_Z| <= sum_(u in Z) ell(u)
            <= m|Z| + sum_(u in Z) max(ell(u)-m,0)
            <= m|Z| + E_m.

The exact separator formula from the normal form is
delta=max_Z(|U_Z|-|Z|). Taking the maximum proves (2). Each capacity object's
excess is included once; counting multiple hits cannot create additional
capacity or improve the left side. QED.

The bound is sharp for every m>=1 and k>=2 in an abstract strand system.
Give k sources links into a single mixed owner, and give that owner's TP
access to mk distinct private interval resources, m assigned to each source's
certificate. The mixed owner has load mk, every resource load one, and
E_m=m(k-1). Only one source can be routed, and at least one can, so
delta=k-1 and equality holds. This example is not asserted to have a frozen
rectangular-grid realization.

## 4. Why one must allow route switching

Consider sources A,B, mixed owners u,v,x,y, and interval resources R_A,R_B.
Supply the four routes

    A: u -> v -> R_A;       x -> y -> R_A;
    B: u -> x -> R_B;       v -> y -> R_B.

Here the source-to-first-owner step and each owner-to-owner step are link
arcs, while the final step is interval access. Each capacity object has load
two. Every supplied A route shares a mixed owner with every supplied B route,
so selecting one intact candidate per source is impossible. Nevertheless
the union of their witnessed arcs admits

    A -> x -> R_B;          B -> v -> R_A.

These routes are disjoint, use each resource once, and cost two links in total.
The four supplied routes cost eight links in total; the theorem's bound is
four. This is a counterexample to the fixed-candidate choice rule, not to
simultaneous compensation or the low-congestion theorem. The checker supplies
an explicit finite terminal/strand realization of this abstract network.

## 5. Exact robustness of the physical parity-hole family

Take the all-parameter real-grid family of
[the parity and interval-repair note](PHYSICAL_PARITY_HOLES_AND_HALF_PROGRESS.md),
with even W>=6, d>=2, q>=1, and L=2d+4. Its k=2q original alpha owners come
from q alpha pair blocks; the q beta pair blocks supply no alpha. Keep exactly
the normal-form physical horizontal TP--BP links, all direct/selected-cap
accesses, and the unmarked original interval units. This is the full declared
horizontal terminal model, not the larger auxiliary candidate graph used for
beta-only endpoint coverage.

Each source has exactly two routes, one in each of its upper/lower bands.
In a block's untranslated coordinates their rows are 5 and W+4. On either
row t, the left source uses

    TP(t,7) -> BP(t,6), TP(t,5) -> BP(t,4),
    free TP(t,3), selected cap (t,2), interval BB1;

the right source uses

    TP(t,L+3) -> BP(t,L+4), TP(t,L+5) -> BP(t,L+6),
    free TP(t,L+7), selected cap (t,L+8), interval BB(L+9).

Thus every branch has two mixed owners, one original interval unit, and cost
two. All 4q branches have pairwise disjoint capacity units; the two branches
of a source share only that source. Upper and lower interval units at a given
column belong to different bands and are distinct original identities.
The exterior singleton intervals are unmarked and away from packet boundary
columns. Every selected mediator lies in the accessed terminal's row.

To see that this lists all routes, trace the horizontal neighbors of the
alpha tips and of the two successive exposed mixed TP terminals in each
band. At each step the only opposite-kind terminal continuation is the one
displayed. Access first becomes available after the second link, at the
exterior cap. The intervening all-BT corridor connects TP to TP in this
placement, hence supplies no horizontal TP--BP link. Different pair packets
are separated by blank rows. No alpha route can enter a beta pair packet or
cross to another source's branch. The frozen template's other mixed owners
are unreachable from these tips in this directed horizontal network.

Let F be an arbitrary set of unavailable mixed owners and interval units.
Unavailability means reserving/removing these routing capacities; it does
not delete physical grid vertices or alter the frozen selected set/matching.
Write B_s^+,B_s^- for the two three-unit branch sets of source s. Then

    delta(F) = #{s: F meets B_s^+ and F meets B_s^-},
    nu(F) = k-delta(F),   minimum cost at value nu(F) = 2nu(F),
    delta(F) <= min(k,floor(|F|/2)).                       (3)

**Proof.** A source can be paid precisely when at least one of its two
branches survives. Since different branches share no capacity units, choose
any surviving branch independently for every such source. Every route costs
exactly two, proving the first two lines. Every blocked source requires two
different excluded units, one in each branch, and different sources require
different units, giving the last line. Excluding the two interval endpoints
of each of s chosen sources attains delta=s with |F|=2s for every 0<=s<=k.
In particular any single unavailable mixed owner or interval unit leaves
full compensation possible at the exact cost 4q. QED.

Theorem 1 with m=2 gives full payment here because all capacity loads are
one. Formula (3) is stronger on this special family because its branches
are entirely independent. It does not claim optimal cost among arbitrary
physical rematchings outside the declared horizontal terminal model.

## 6. Validation, scope and next question

Run from the repository root:

    PYTHONDONTWRITEBYTECODE=1 python3 develop/check_twofold_route_compensation.py --output output/twofold-route-compensation-validation.json

The recorded run passes: 90 independently enumerated abstract networks with
625 complete-or-partial route packings; 3,241 certificate controls, including
1,981 zero-excess covers with full layer decompositions, saturated-resource
and cost checks, and 1,260 overloaded controls; the switching obstruction;
21 sharp overload examples; and 18 complete physical families with 936
reservation controls. Counts across models are summed test occurrences.
The physical controls use W in {6,8,12}, d in {2,3,5}, q in {1,2}; reservations
include the empty set and all singleton relevant units, and all pairs for q=1.
They test the general written proofs, rather than replace them.

[RouteCoverAccounting.lean](../formal/SubQuorum/RouteCoverAccounting.lean)
also checks six local statements: summing twofold load excess, the conditional
separator deficit bound, zero deficit from excess at most one, the integral
layer remainder bound, saturated boundary splitting, and the cheaper of two
layers. Local Lean 4.33.0 execution and all six axiom audits pass using only
propext and Quot.sound. Two unused-premise linter warnings in the remainder
statement are nonblocking. This does not formalize integral circulation
existence, graph-flow decomposition, incidence-to-separator transport, or the
physical grid geometry. The circulation and geometric proofs remain written.

This note does not establish universal geometric route-cover existence,
a universal improvement of the 5/6 bound, or the rectangular-grid triple
equality. Under zero excess, counting resource loads alone already implies
at least k distinct resources. The additional conclusion is simultaneous
realizability with mixed-owner capacities, resource preservation and controlled
link cost. The next geometric task is to construct low-excess route covers
in occupied bands with shared relays, or to exhibit a physical separator
whose deficit requires a separate, nonduplicated exterior budget.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
