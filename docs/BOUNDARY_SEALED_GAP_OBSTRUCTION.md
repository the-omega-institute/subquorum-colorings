# Full-gap route obstruction and compensation from whole strand supports

25 October 2026. Authors: Haobo Ma and Wenlin Zhang.

**Complete freezing does not force full compensation even in the FULL
endpoint-free-gap terminal network.** We prove an all-parameter, uniquely
matched frozen family with one alpha, no beta, no reachable unmarked interval,
and arbitrarily large positive target margin. The obstruction persists on
the entire board, and separated copies give arbitrarily large flow deficit.
In the exact two-phase cut formula, both phase blockers and the shared
resource blocker are EMPTY, but the blocked-source intersection is nonempty.

The target inequality remains true. The failed claim is automatic completeness
of the declared terminal/gap routing interface, not the established exact
normal form, the phase cut formula or the grid conjecture. The recent
[extreme-interval compression](BT_CORRIDOR_PORTS_AND_BOUNDED_ACCESS_OBSTRUCTION.md)
also remains true: its full and sparse networks have the SAME deficit here.

The family points to a concrete missing interface: interval resources beside
an INTERNAL PP column of the alpha. We prove a general whole-support gap
allocation adapter, retaining at most two virtual-alpha owners per original
interval and exact single-use bookkeeping. It repairs every cancellation of
this family. This is a counting allocation with a broader witness relation;
it is not a reinterpretation of such payments as free-terminal routes.

## 1. A completely specified family

Let W>=6 and H>=4 be even, and N>=H+6 be even. Put R=W+4. On the rectangular
board with rows0,...,W+11 and columns0,...,N-1, use the original matching

    (r,3)--(r+1,3), r=5,7,...,W+3;
    (r,4)--(r+1,4), r=6,8,...,W+2;
    (5,4)--(5,5), (5,6)--(5,7);
    (R,c)--(R,c+1), c=4,6,...,H+2;
    (R-1,c)--(R-1,c+1), c=5,7,...,H+1.

The old selections are

    {(4,3),(4,5),(4,7),(5,2),(5,8),(6,6),(7,5),(R,2),(R,H+4)}
    union {(R+1,c): c=3,5,...,H+3}
    union {(R-2,c): c=6,8,...,H+2}.

Add the following selections:

    (4,1), (R+1,1);
    (4,c) for odd c, (5,c) for even c, c=9,...,N-2;
    (R+1,c) for odd c, (R,c) for even c, c=H+5,...,N-2.

All other vertices are blank. There are 2N-H-14 additions, 2N-5 selections
in total, and W+H matching edges. Each addition is isolated from every old
occupied vertex and every other addition. The alternating rows make new
neighbors diagonal rather than adjacent. The first right addition is diagonal
to the old selected cap, and every addition's vertical/outside-band neighbors
are blank. Consequently the pair is feasible.

P and M are identical to direct_family(W,H). The explicit all-parameter
serial freezing schedule and forced-leaf unique-matching proof in
[terminal cancellation](TERMINAL_CANCELLATION_AND_STRANDED_DEMAND.md), Section8,
apply unchanged. Every selected witness from that proof remains selected,
no new endpoint is added, and no matching edge changes. Thus all endpoints
freeze and M is the unique perfect matching of the endpoint-induced graph.
This inheritance proves all parameters, independently of finite controls.

Let J be the aligned packet with rows4,...,R+1 and ALL N columns. It contains
every selected vertex, every endpoint and every original receiver tile: the
old endpoints lie in rows5,...,R and columns3,...,H+3, so their whole original
tiles stay inside J; the new selections also lie inside. Both end columns
are BB in every band, giving B_J=W+2. The exact inventories are

    alpha=1, beta=0, mixed=H+1,
    S_J-B_J=(W/2-1)N+3-2W-H
           >=(W/2-2)H+W-3 >=7.                         (1)

This is not dependent on cropping. Take the entire (W+12)-by-N board K as
the packet instead. It adds five empty two-row bands, each contributing
N-2 to S-B. Therefore

    B_K=W+12,
    S_K-B_K=(W/2+4)N-2W-H-7
           =(S_J-B_J)+5(N-2)>0.                        (2)

The target margins can grow arbitrarily with W or N.

## 2. Full gap access is still unable to pay

The sole original alpha has tips (5,3),(R,3). In upper row5 its reachable
TP tips are columns3,5,7. In lower rowR they are3,5,...,H+3. From a TP at c
one can enter the adjacent mixed strand at BP c+1 and exit at TP c+2.
A link back to the BP of one's own mixed strand is a self-cycle and cannot
create a different exit. These two row chains exhaust source reachability.
No reachable beta exists.

In the upper terminal band the columns are

    BB0, BT1, BT2, TP3, BP4, TP5, BP6, TP7,
    BT8, BT9,...,BT(N-2), BB(N-1).

In the lower terminal band they are

    BB0, BT1, BT2, TP3, BP4, TP5,...,BP(H+2), TP(H+3),
    BT(H+4),...,BT(N-2), BB(N-1).

Thus neither terminal band has ANY unmarked BB--TT interval, whether on J
or on K. Its only BB columns are0,N-1, both marked. An earlier TP in a row
cannot skip a P column to reach another gap. Full endpoint-free gap access
therefore gives no available resource at any reachable TP, however long the
gap access or terminal relay is allowed to be. In fact even access to ANY
unmarked interval in the same band would fail, since there is none.

**Theorem 1.** On both J and K the full-gap terminal network has maximum
compensation0, deficit1, and an empty unit cut. This remains true for EVERY
matching of horizontal opposite-label terminal links, including arbitrary
reassignment and cancellation cycles.

**Proof beyond reachability.** Let V_* be all tips in the two displayed rows.
Every original strand meeting V_* has both tips there: they consist of the
one alpha and its two mixed row chains. Every permitted horizontal link
from V_* also stays there. Hence V_* is closed under original strands and
every C. With no original beta, terminal cancellation preserves alpha'=1
and beta'=0. The unique cancellation component containing the original
alpha is a virtual alpha with both free TP tips in V_*. It cannot be a cycle
or a beta, by its signed endpoint sum. Every other component in V_* has
no alpha and no beta. The remaining free TP tips can reach no unmarked
interval even under full gap access. Thus this unique demand is unpaid
for every C. QED.

The interval supply is nonetheless I_J=S_J-B_J+1 and I_K=S_K-B_K+1. It can
be arbitrarily large. Supplying more inaccessible resources in other bands
does not repair the declared route model.

## 3. The exact two-phase implication that fails

Use the exact cut formula from
[colored owner deficits](COLORED_ROW_OWNER_DEFICIENCY_AND_RESOURCE_CUTS.md),
Section6. A phase is the checkerboard color of a route's TP tips. Let
F_sigma(G_sigma,Q) be the sources blocked in phase sigma after deleting
its mixed-gate set G_sigma and the common original resource set Q. Then

    delta=max (|F_0 intersect F_1|-|G_0|-|G_1|-|Q|).

Take G_0=G_1=Q=empty. Neither phase of the original alpha reaches a resource,
so F_0=F_1={alpha}; the score is1. The formula correctly reports the true
deficit. The candidate geometric implication

    complete freezing => |F_0 intersect F_1| <= |G_0|+|G_1|+|Q|

is therefore FALSE for full-gap terminal access, even with complete receiver
closure and the full board. One cannot prove this implication merely by
improving cut counting inside the same access model.

Stack q copies vertically, translating copy i by i(W+12) rows, and keep all
N columns. Occupied supports, freezing schedules, matchings and the reachable
row chains are separated. Horizontal terminal links cannot move between
copies. The board and packet counts add, so the full-board network has

    alpha=q, deficit=q, G_0=G_1=Q=empty,
    target margin=q*((W/2+4)N-2W-H-7)>0.                 (3)

This is an unbounded failure of the candidate implication, not a grid-bound
counterexample. An expanded proof must expose a resource interface beyond
free TP terminals, or account for the inaccessible exterior reserve separately.

## 4. Whole-support gap incidence has at most two owners

The following adapter applies to ANY feasible matching-closed aligned packet,
not only the family above. Fix any horizontal opposite-label terminal matching
C and form its virtual strands and cycles. The full support of a virtual
strand is the union of the supports of its constituent original PP strands.
Original pure PP cycles remain separate and are not demands.

For a maximal endpoint-free gap G, inspect each of its at most two neighboring
P columns. Assign that side to the virtual component owning that column.
This ownership is unambiguous. A TP or BP column has just one endpoint. A PP
column's two endpoints are joined by the within-band PP edge, so are already
in the SAME original strand or pure cycle. Terminal cancellation joins whole
original strands; it never splits them. Thus the two physical endpoints of
a PP column cannot be counted as two candidate owners.

Declare a virtual alpha eligible for an available original interval in G
when its whole support owns either neighboring P column. The witness can be
an INTERNAL PP column, or a terminal column whose original tip became linked
under C. It need not be a surviving free TP terminal.

**Theorem 2 (whole-support adapter).** Each original interval resource has
at most two eligible virtual-alpha owners. Full-gap payments at free TP tips
are a subset of these permitted whole-support payments. Every interval still
has capacity ONE, even if both sides, two PP endpoints or several constituent
original strands identify the same virtual alpha.

**Proof.** Every interval belongs to one gap. Each of its two boundary columns
has at most one virtual owner by the preceding argument. Remove owners that
are not virtual alphas and merge identical owners. This leaves at most two.
A free TP witness is one of these boundary columns and lies in the support
of its owning virtual alpha, proving the inclusion. Nothing in the relation
creates an additional interval unit. QED.

The extreme-available-interval compression extends to this adapter. Keep
the first available unit for G's left owner and the last for its right owner.
A gap can pay at most two DIFFERENT owners. If it pays two, they must be the
two distinct side owners and its available extremes are distinct. If both
sides have the same owner, it can receive just one payment. The same transport
proof preserves every paid virtual-alpha owner and C, with arbitrary fixed
reservations recomputed first. It preserves an owned boundary-column witness;
it makes no assertion about free-terminal witnesses.

## 5. Exact allocation, scalar ledger and a complete conditional class

Build the standard two-owner resource multigraph on the alpha' virtual
demands. An original unmarked interval with two different eligible owners
is an edge; an interval with one owner is a single-owner unit; units with
no eligible owner stay in the unused pool. Keep different original interval
identities even for parallel edges. Let t be the number of demand-graph
components that are trees without a single-owner unit, including isolated
demands. Let Q_unused be the number of original unmarked units unused by a
maximum whole-support payment. With only the original boundary reservations,

    maximum whole-support interval payment = alpha'-t,
    S_J-B = Q_unused+beta'-t.                            (4)

**Proof.** Theorem2 supplies exactly the at-most-two-owner hypothesis of
the already proved [one-sided allocation theorem](ONE_SIDED_INTERVAL_AND_BETA_ALLOCATION.md).
For completeness, a connected tree with n demands has n-1 edge units and
no single-owner unit, so can pay exactly n-1 demands by orienting its tree
away from an omitted root. A component with a single-owner unit pays its
owner at a root and uses a spanning tree for all others. A component with
a cycle can instead reserve one cycle edge for a root and take a spanning
tree avoiding it, again paying every demand. Parallel edges form a valid
two-edge cycle. These constructions use different units within each component;
different components have disjoint units. This proves the first formula.
Now I=L-B=alpha'-t+Q_unused and the unchanged actual ledger is
S_J=L+beta'-alpha', proving the second. QED.

In particular, every virtual alpha having at least TWO distinct eligible
unmarked interval units suffices for t=0 and S_J>=B. A deficient tree with
n vertices has total demand degree2n-2, so cannot have every demand degree
at least two. More generally t<=Q_unused+beta' is exact for the scalar
packet inequality. Distinct interval assignments, not the number of physical
endpoint sightings, determine payments. Any additional interval reservations
must be accounted for in the corresponding larger ledger; they are not
silently added as free capacity in (4).

This is a counting compensation theorem. It does not change the actual
matching, promote endpoints, or claim that an internal witness is a terminal
route. The old route normalization and phase invariance retain their original
free-terminal access scope. Freezing does NOT force t=0: a carried band phase
of the existing fully frozen unported shared-gate fixture has alpha'=2,
beta'=5 and no support-eligible interval for either alpha. Its support graph
has two isolated demands, t=2, while Q_unused=187 and S-B=190. The full terminal
network can pay both via different beta resources, with deficit0. This is
not a failure of (4); it excludes using interval-only t=0 as a necessary
invariant. Its exact geometry adapter and result are archived as the
support_only_counterexample in the new output. The general scalar inequality
in this broader model remains unproved.

## 6. Exact repair of the obstructed family

In every member of Section1 the original alpha contains the internal PP
column {(6,3),(7,3)}. The column {(6,2),(7,2)} is BB, is unmarked, and is
an original singleton interval. The gap on the left of that PP column also
contains the distinct unmarked BB column1; column0 is the reserved boundary
unit. Thus the virtual alpha has at least two distinct whole-support units.

After ANY C, the whole original alpha still belongs to the unique surviving
virtual alpha. Its two internal units therefore remain eligible. Assign
column2 to it. It is paid with C empty, at zero new links, and the general
support allocation has t=0, Q_unused=S_J-B. The same applies on the full
board and after arbitrary C. In separated copies use the translated column2
unit in each copy, giving q different original resources for q demands.
Neither endpoint markings nor the alpha's two physical PP endpoints produce
an additional credit. This supplies a fully witnessed repair of the whole
parameter family in the broader counting model.

For W=6,H=4,N=10 the complete selected set is

    (4,1),(4,3),(4,5),(4,7),(5,2),(5,8),(6,6),(7,5),
    (8,6),(10,2),(10,8),(11,1),(11,3),(11,5),(11,7).

The crop has8 by10 cells, margin7 and8 unmarked units; the full18 by10
board has margin47 and48 unmarked units. The terminal network pays0 in
either case; support allocation pays1. Both exact ledgers agree.

## 7. Verification, Lean and independent-review status

The deterministic checker reconstructs physical PP components and pure cycles,
the full endpoint-free access relation, phase cuts and maximum flows. For
each C it joins WHOLE original owners, builds support incidence independently
from every gap's P boundary columns, checks the two-owner bound, compares
the constructive allocation with an independent augmenting matching, checks
extreme compression, and verifies (4). Actual matched resource identities
and owned P-column witnesses are retained.

Finite controls include every family triple W=6,8,...,22, H=4,6,...,18 and
N=H+6,H+8,H+14, both cropped and full-board packets; all eight carried-band
isometries of the smallest obstruction; separated stacks of1,...,8 copies;
all horizontal cancellations of the smallest case; and existing bent,
occupied-band, rotor, TT and shared-gate controls with alternative matchings
and band phases. A physical two-alpha/two-unit gap makes the two-owner bound
nonvacuous. The output gives exact totals and complete concrete evidence.
Finite checks corroborate, and do not establish, the universal proofs above.

The final run passes673 fully frozen geometry controls and12470 whole-support
allocation controls, including11796 fixed cancellations and all128 horizontal
cancellations of the smallest obstruction. There are432 parameter/packet
controls,8 isometries,8 separated stacks and224 carried configurations.
The broader support model strictly improves interval payment in11357 controls.
The two-owner gap is explicitly exercised after a two-link transfer; single-link
controls alone would not reach that shared-alpha incidence. The96 deficient
support controls contain128 deficient-tree occurrences and are retained as
negative evidence against automatic interval-only t=0.

Local Lean4.33.0 passes11 new theorem audits using the prior rank/relay module.
It checks the concrete18 by10 geometry and matching, all20 endpoints frozen,
unchanged original tip labels, absence of TT,48 actual unmarked interval units,
arbitrary finite original relay closure with no full-gap exit, the internal
PP support witness and crop/whole-board margins7/47. A general two-side
owner lemma is formalized under explicit boundary ownership hypotheses.
No sorry or native evaluation is used; dependencies are propext and Quot.sound.

General family geometry/unique matching, the flow/cut adapter, whole-support
physical ownership and the allocation/ledger theorem remain written proofs.
Oracle broker preflight finds26 active workers all reporting
model_unavailable@selecting_model. No new review was dispatched, and no new
independent acceptance is claimed. Submitted manuscripts, public main and
the separate star-forming/C4 workstream are unchanged.

Next study joint compensation of deficient support trees by distinct whole
beta owners or an exterior budget, retaining original horizontal-link witnesses
and avoiding a beta used in two components. Neither interval-only t=0 nor
terminal-only full-gap completeness is automatic. The terminal-only
automatic cut implication is now ruled out; the universal grid bound and
5/6 improvement remain open.

Reproduce the finite checks and scoped kernel audit from the research root:

    PYTHONDONTWRITEBYTECODE=1 python3 develop/check_boundary_sealed_gap_obstruction.py --output output/boundary-sealed-gap-validation.json
    PYTHONDONTWRITEBYTECODE=1 python3 develop/check_boundary_sealed_gap_formal.py --lean ~/.elan/bin/lean --output output/boundary-sealed-gap-lean-validation.json

The second command explicitly selects the local Lean executable, measures
memory and real Lean/Lake processes, builds only the one imported core/Omega
dependency and checks the new module sequentially. It adds no CI dependency.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
