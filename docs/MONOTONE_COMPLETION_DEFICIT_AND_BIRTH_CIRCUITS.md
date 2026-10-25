# Permanent band links, a joint completion budget and frozen birth circuits

26 October 2026. Wenlin Zhang and Haobo Ma. Independent research continuation.

The [preceding source-birth theorem](DEGREE_CHANGING_BENT_COMPLETIONS.md)
counts new alpha demands when selections are added. Here we incorporate resource
loss and beta loss in ONE budget for the exact full-network deficit. The new
conclusion holds for arbitrary fixed physical mixed-direction partitions and
arbitrary outside stem/fork interactions, not just the occupied-bent family.

Fix P,actual M,the physical auxiliary matching N and old T. In every feasible
monotone selection completion:

1. Every old permitted TP--BP band link remains permitted. A BP that converts
   had NO old TP entry link at all.
2. If p selections are added and s OLD beta bodies become alpha, then the
   exact full deficit D satisfies the sharp bound

       0 <= D_final-D_old <= p-s.                         (A)

   In particular, selection saturation cannot repair a positive fixed-partition
   deficit. Two conversions in one old beta do not consume two independent
   payment budgets.
3. If h is the loss of total original interval capacity and t counts old
   beta-to-mixed transitions, any old paid-source packing loses at most h+t
   of its old source identities. New source births do not themselves force
   an old source to be displaced.

We also give a fully frozen all-width physical realization of joint source
births, private beta withdrawals and shared interval losses. Its exact deficit
is the number of acyclic resource components whose vertices ALL have an active
source and no private beta. One original shared interval is spent once. This
includes arbitrarily large birth sets for which every proper subset is payable
but the whole set is not, with ALL original resources available.

The full-flow and graph-matching tools are existing results. The contribution
is the permanent-link geometry, joint physical completion budget, and the
source/credit activation adapter and its common freezing certificate. The
resource path circuit with all sources already present was proved earlier;
here that circuit is produced by adding new sources to a source-free frozen
baseline. No universal 5/6 improvement or numerical counterexample is claimed.

## 1. Model and comparison of interval pools

Use precisely the model in Section 1 of the preceding note: feasible T has
selected degree at most one in P union T; P is the endpoint set of the fixed
actual grid matching M. N is supplied by disjoint even rectangular regions
with fixed horizontal two-row or vertical two-column bands. Restore every
actual M edge across region boundaries before identifying global bodies.
Permitted links are ALL TP--BP adjacencies along the SAME band, and resources
are all original positive BB/TT forest units plus one credit per whole beta.
The exact stem/fork packing, or equivalently the BP-entry-aware flow, defines
V, the maximum number of paid original alpha sources, and D=a-V.

No endpoint insertion, actual M change, N change, inter-band cancellation,
locked old allocation or deliberate resource reservation is implicit. We
compare the complete original pool separately computed at each T.

**Fixed-gap coupling.** At fixed P,N each maximal no-P gap is fixed, as are
its boundary bodies. Every original interval in a gap has the same whole-owner
support: the different open bodies at its two boundaries. The count of its
units is

    L_gap = gap length - number of selected sites in it.

Thus under additions the count only falls. For comparison replace the actual
forest IDs within each gap by canonical slots (gap,0),...,(gap,L_gap-1).
This replacement is an incidence-preserving bijection and preserves every
stem/fork packing, its value, link cost and source IDs. The final canonical
pool is a subset of the old pool. This is a capacity comparison, NOT a claim
that a changing BB/TT forest retains its old physical interval identity.

Let x be converted BP ends and p added selections. Each added selection whose
N partner is in P converts exactly one BP and lies in no no-P gap. Every
other new selection lies in exactly one no-P gap and lowers its count by one.
Consequently, with h=L_old-L_final,

    p=h+x.                                                (1)

Shared gap boundaries do not multiply this loss; the gap and its slots are
counted once globally, including mixed-direction region boundaries.

## 2. Existing terminal links cannot disappear

**Permanent-link lemma.** If q->p is an old permitted TP--BP link, p cannot
convert in any feasible monotone completion.

The old selection N(q) already sees its P anchor q. Because q,p are consecutive
terminal sites along one band, their physical partners N(q),N(p) are adjacent.
Selecting N(p) would give that new selection the two different occupied
neighbours p and N(q), violating feasibility. Equivalently the old N(q) would
see its anchor and the new adjacent selection. The four sites are distinct
because N(q),N(p) lie outside P. Rotation covers vertical bands.

Old TP ends remain TP and old link targets therefore remain BP. Every old link,
including any harmless self-link, persists. Conversely every newly added link
must originate at a newly converted TP end: if its TP were old, its BP target
and physical adjacency would have supplied the same link before.

In particular an old mixed body which becomes alpha had no old incoming link;
it cannot have been traversed in an old source packing. An old beta with BOTH
ends converting had no old incoming link at either end; it too was unused.
A beta with ONE converting end cannot have been the root of a two-source old
fork: that would require a link into the protected converting tip. This is a
physical exclusion, stronger than merely counting two beta tips as one credit.

## 3. One joint budget, with old source identities tracked

As before let r count old mixed-to-alpha transitions, s old beta-to-alpha,
and t old beta-to-mixed. Bodies are fixed, and old TP ends remain, so

    a_final=a_old+r+s,
    x=r+2s+t,
    p=h+r+2s+t.                                           (2)

**Old-packing retention lemma.** From ANY old normalized packing paying v
specified old sources, one can retain at least v-h-t of those SAME source
identities in the final model. Negative lower bounds mean zero. No new source
needs to replace a retained old source.

Proof. Use canonical gap slots from Section 1. Remove each old allocated
interval slot absent from the final pool; there are at most h. An affected
interval stem is discarded, losing one source. An affected beta fork is
replaced by either one of its arms as a beta stem, losing one source and
releasing its interval. Choose the retained arm's original source. All other
certificates remain disjoint and unchanged.

Now handle old beta bodies that changed type. A beta-to-alpha body was unused
by Section 2; it costs no old payment. A beta-to-mixed body could only have
been used by one beta stem, since its converting BP had no old entry link.
Discard that stem if present, losing at most one old source per such body,
hence at most t. The remaining primitive owners, links and assigned slots are
all retained. New alpha bodies were unused in the old packing, so they do not
conflict with these retained certificates. This construction discards at most
h+t sources in total; an overlap is counted only once, not as two required
losses. It proves the assertion for arbitrary old packing and outside forks.

In particular

    V_final >= V_old-h-t.                                 (3)

**Reverse-packing lemma.** Any final packing of v sources gives an old packing
of at least v-r-s sources.

Proof. Decompose its integral flow into source-to-resource paths, keeping
physical BP entry gates. Discard paths starting at newly born alphas, at most
r+s paths. The remaining paths start at old alpha identities. If such a path
first reaches a body which was beta but is now mixed, truncate it there and
pay its source with that body's OLD whole-beta credit. The final mixed gate
has capacity one, so at most one path uses that body; truncations cannot
spend one old beta twice.

Any new link originates at a converted TP. A surviving path cannot use a new
link from an old mixed-to-alpha or beta-to-alpha body: such a final alpha can
only be a source, whose new path was discarded. A new link out of an old
beta-to-mixed body is removed by the truncation. Hence all retained path
prefixes use old links. Their final interval slots also exist in the old
pool. Any final beta is the same old beta with the same two entry gates;
normalizing its paths spends its private credit once as usual. Original
source, mixed-gate, BP-entry and interval capacities remain respected. These
prefixes therefore form an old feasible flow/normalized packing of at least
v-r-s sources. This includes forks; there is no assumption of one entry per
unchanged beta.

It follows that

    V_final <= V_old+r+s.                                 (4)

Subtracting (3),(4) from the exact source count (2) gives

    0 <= D_final-D_old <= h+t+r+s = p-s.                   (5)

The improved minus-s is essential: an old beta with two converting ends was
unreachable before, so its loss cannot also be charged as an old payment loss.
For one addition s=0 and the deficit increment is either zero or one. Every
ordering of a feasible addition set is feasible, since removing selections
preserves feasibility. The one-step law also telescopes for arbitrary length.
The batch proof gives the stronger paired-beta correction independently of
which order is chosen.

The physical zero-entry conclusion is necessary for the stronger correction.
As an explicitly NONPHYSICAL relabeling control, take two alphas A,B and one
beta C with two incoming links, one from each alpha, and one interval supported
only by C. The old beta fork pays two and D=0. Arbitrarily relabel both C ends
TP and delete their incoming links. Now C is a new alpha and alone can use the
interval: V=1,a=3,D=2. With p=2,s=1 this violates p-s=1. Such a relabeling is
forbidden by Section 2 and is not a feasible physical selection completion.
This control does not refute (5); it prevents extending it to arbitrary
abstract endpoint relabelings without the geometric hypothesis.

Putting H=S+D and S_final=S_old-p yields

    -p <= H_final-H_old <= -s.                             (6)

This is a potential identity/bound, not the desired numerical grid inequality.
It is not legitimate to replace S by S+D in that target. A fixed-partition
positive deficit nevertheless persists in EVERY feasible monotone completion.
If the old endpoints were fully frozen, the old strict witnesses replay in
each completion, so the statement also covers all frozen retaining saturation
extensions. Deleting T reverses the deficit inequality, but can destroy
freezing; no freezing guarantee for arbitrary deletions follows.

**Exchange corollary and necessary repair cost.** For ANY two feasible selected
sets T0,T1 with the same P,M,N, not necessarily nested, let d=|T0 minus T1|
and e=|T1 minus T0|. Apply (5) to their common feasible intersection I and
each endpoint. Since D(I)<=D(T0),D(T1), and D(Ti)-D(I) is at most its number
of additions, we obtain

    -d <= D(T1)-D(T0) <= e.                              (6a)

Thus ANY selection exchange that fully repairs an old deficit D(T0) must
remove at least D(T0) old selections, regardless of how many new selections
it adds. This is a necessary cost, not a promise that such a deletion set
exists or preserves freezing. Nonmonotone exchanges of T remain a possible
repair mechanism and are not excluded by completion monotonicity.

## 4. A common frozen family with three independent kinds of event

Use the existing configuration(W,k), even W>=8, k>=1, on the
(W+2)-by-(10k+2) board, its endpoint set and unique actual M. The base T* is
the previously proved fully frozen fixed-P maximum, with

    a=k,b=0,m=7k,L=3k,S=2k,V=0,D=k.

Use the original horizontal bands. Module a, 0<=a<k, has original alpha tips
(1,10a+5),(W,10a+5). Designate

    x_a=(0,10a+5),       y_a=(W+1,10a+7).

Deleting x_a turns its alpha into mixed (no source). Deleting y_a turns its
lower branch L1 into one beta, with tips (W,10a+6),(W,10a+7). Its whole interval
support is empty, and an active module source can use that private beta through
ONE link from (W,10a+5) to (W,10a+6). This beta is reached only within its own
module; its two tips do not give two credits.

Also retain the existing upper/lower seam-opening sites

    u_i=(0,10i+1),    l_i=(W+1,10i+1), 1<=i<k.

Removing u_i or l_i opens respectively one original shared singleton j_i^+ or
j_i^- in the boundary band, incident to the neighbouring modules i-1 and i.
These sites are occupied-isolated in T* and not adjacent to P. Their deletion
changes no endpoint type or link. These seam adapters were proved in the
[two-sided opening note](TWO_SIDED_SEAM_BUDGET_AND_UNBOUNDED_RECOURSE.md).

For arbitrary X,Y subset {0,...,k-1}, and upper/lower opening sets E+,E-, put

    T(X,Y,E+,E-)=T* minus {x_a:a notin X}
                    minus {y_a:a notin Y}
                    minus {u_i:i in E+}
                    minus {l_i:i in E-}.                  (7)

X activates alpha births; Y removes private beta credits; closing an opening
adds an isolated point and removes a shared resource. All these restoration
operations are additions from the common minimum T(empty,empty,all,all).
They are distinct physical sites. Every set (7) is feasible as a subset of T*.

**Common strict freezing certificate.** The minimum retains a complete ordered
certificate. In each module freeze this prefix, with columns shifted by10a:

    (1,3),(W,3),(1,9),(W,9),(1,7),(W-1,8),(1,5),(W,5),(W,7).

The first four are the old outer seeds. (1,7) uses its retained top T and the
P at (1,8), whose mate (1,9) has frozen. (W-1,8) uses the retained T at
(W-2,8) and P at (W,8), whose mate (W,9) has frozen. (1,5) uses its two
side P neighbours (1,4),(1,6), whose mates (1,3),(1,7) have frozen, so it does
not need the deleted x_a. (W,5) still uses its bottom T and the side P at
(W,4), whose mate (W,3) has frozen. Finally (W,7) uses P at (W-1,7) and
(W,8), whose mates have frozen in the prefix, without the deleted y_a.

Continue with the old uniform module schedule, omitting endpoints already
in this prefix. All other old T witnesses remain: x_a and y_a each neighboured
only the one P endpoint now handled in the prefix, and seam sites neighboured
no P. Moving old endpoints earlier cannot invalidate a strict witness.
This proves full freezing for every W,k and the entire family (7), including
simultaneous deletions. It is not inferred from separate one-deletion tests.

## 5. Exact shared-component deficit with births and beta losses together

For (7), put Z=X intersect Y, and m_open=|E+|+|E-|. Directly tracing the fixed
bodies and gaps gives

    a=|X|, b=k-|Y|, mixed=7k-|X|+|Y|,
    L=3k+m_open,
    S=4k-|X|-|Y|+m_open.                                 (8)

The complete reachable graph is the old seven-owner module table, with two
controlled changes: an inactive source body is mixed with no incoming link,
and L1 may be beta instead of mixed. No link connects different modules;
resources are shared through their fixed gap incidence. When the alpha is
present and the private beta absent (a in Z), its full list of reachable
resources consists exactly of the open seam units incident to module a.
All other original units remain available but unreachable. When the private
beta is present, the one-link private payment is available; it never consumes
a shared seam unit. An inactive module contributes no source demand.

The endpoint change x_a cannot create a new incoming route into an inactive
source: its old upper tip is BP between the two old branch BP sites, while
its lower tip stays TP. Likewise all existing branch routes stay within the
module. A missing y_a makes L1 a sink; it cannot create access to other
modules or resources. For needy a in Z, both controlling sites are retained,
so the old full route/support table applies without change.

It follows that the exact full-network maximum is

    V=|X minus Y| + nu(Z,E),                              (9)

where nu is the maximum injective assignment of vertices in Z to incident
upper/lower open seam units. For the lower bound prepay every X minus Y by
its different private beta, then realize the incident matching for Z. Left
shared units use one link through U0/L0; right ones use two through U1/U2 or
L1/L2. Different modules have disjoint terminal routes; different resource
IDs are assigned once. For the upper bound a needy source has no beta exit
and must take an incident seam unit. Other active sources pay at most one
each, even if they use some shared units instead. Thus they cannot increase
(9) by freeing a nonexistent beta for a needy source.

Form the resource multigraph on ALL k module vertices. Seam i has an upper
edge if i in E+ and a lower edge if i in E-. Components are intervals. A
component is cyclic precisely if some seam is doubled. Then the exact deficit
is

    D = number of ACYCLIC resource components C
               for which every vertex of C belongs to Z. (10)

Proof. A tree component whose r vertices all need resources has only r-1
units; one source must be unpaid and orienting its edges away from any root
pays the others. If a tree component has any vertex outside Z, root there
and assign each needy vertex the first edge toward the root. Each edge is
assigned to its farther endpoint only once, so all needy vertices pay.
In a cyclic component use its doubled seam to pay its two endpoints with
the two distinct parallel units, then assign other vertices edges toward
this two-cycle. Restricting to Z pays all needy vertices. Components have
disjoint physical resources and module routes, so their deficits add.
This proves (10) generally, not by enumerating opening patterns.

## 6. Sharp consequences and genuinely joint failures

**Source/credit AND.** With no shared openings, every component is a singleton,
so D=|X intersect Y|. From the baseline with both x_a,y_a absent, adding x_a
alone creates a source but leaves its private beta available; adding y_a alone
removes an unused beta but creates no source. Both singleton operations have
zero deficit increment. Adding both makes that module's deficit one. Each
step respects the one-unit law; singleton sensitivity is not additive.

**Arbitrarily large joint birth circuit.** Open ALL lower seams and no upper
seams, and retain every y_a (Y=all). The resource graph is one tree path.
Start with X empty: there are no alpha sources and D=0, but the board is fully
frozen. Adding any proper subset of the k source sites x_a leaves a safe root
outside X and D=0. Adding ALL k sites produces D=1. The completed pool has
4k-1 original units, including the inaccessible ones, and all are available.
This is the earlier full-pool resource path circuit activated by source
births, at k different actual M edges. No bounded-order simultaneous-birth
test detects every such obstruction. Every intermediate board remains frozen.
The numerical slack is 3k-1 at the completed circuit, positive.

**Sharp unit coefficient.** With no openings and every y_a retained, adding
k missing x_a creates exactly k unpaid alphas: p=k,s=0,Delta D=k. Conversely,
with every x_a retained, restoring k missing y_a removes k useful private
betas and also gives Delta D=k. These are full-pool, fully frozen controls.

**Sharp paired-beta correction.** In T* delete BOTH alpha partner sites
(0,10a+5),(W+1,10a+5) in every module. Its old source body is beta, with no
incoming links. Restoring all 2k selections produces k unpaid alphas:

    p=2k, s=k, Delta D=k=p-s.

This baseline is also fully frozen. Use the same outer seeds, then (1,7)
and (W,7) with their retained partner selections and already kept side P.
Freeze (1,5) and (W,5) with their two side P neighbours; then continue the old
schedule. Deleting the two source partners affected no other endpoint's old
T witnesses. The double conversion must not be charged both as a lost beta
payment and as a new alpha demand. That old beta could pay nothing.

All these conclusions retain fixed P,M,N. A different direction choice may
pay all sources, as already proved for this endpoint family. They locate
completion and shared-allocation obstructions, not a universal grid failure.

## 7. Reproducibility and formal scope

Run from the repository root:

    python3 develop/check_monotone_completion_deficit.py --output output/monotone-completion-deficit-validation.json
    python3 develop/check_monotone_completion_deficit_formal.py --lean /path/to/lean-4.33.0 --output output/monotone-completion-deficit-formal-validation.json

The physical checker compares actual forest units with the canonical gap-slot
quotient, checks old link inclusion, absence of old entries at converted BP,
exact transition budgets, old-link packing retention and old-source-only
lower bounds. It checks all controlling event subsets at (W,k)=(8,1),(8,2),
(8,3),(10,3), every edge of these event cubes, and larger sizes through W=64,
k=12. All controlled boards replay the SAME common strict certificate.
Independent primitive packing checks full values/costs on selected small
models. General mixed partitions use the physical region compiler and include
all actual M crossings. Abstract zero-entry conversions include outside beta
forks and are checked independently against primitive packing; these controls
are not claimed physical embeddings.

The [permanent three-birth fixture](../develop/fixtures/monotone_birth_circuit_w8_k3.json)
stores the complete source-free board, actual M, common freezing schedule and
three birth sites. Every proper subset has deficit zero, all three give one.
The arbitrary-size proofs are Sections 1--6; the saved
[computational receipt](../output/monotone-completion-deficit-validation.json)
reports the finite scope and counts without promoting it to a general proof.

The saved run passes 2,260 controlled boards,340,560 common-certificate rank
events and10,436 single-event cube edges. There are90 independent controlled
primitive optima;154 additional physical transitions compare both raw and
gap-slot pools, including1,473 preserved old link occurrences and114 converted
BP incidences with no old entry. Another16 transition primitive optima are
checked independently. Nine frozen controls attain the improved p-s bound,
replaying2,112 additional strict events. Six hundred abstract zero-entry
conversions are compared with primitive packing;18 checked optima use forks.
One excluded nonphysical relabeling control violates the p-s formula when
old incoming links are deleted, as predicted by the hypothesis check.

[Lean source](../formal/SubQuorum/MonotoneCompletionDeficit.lean) verifies the
permanent-link exclusion for arbitrary site predicates using selected-neighbour
uniqueness (axiom-free), the joint p-s budget from the stated packing adapters,
the impossibility of an old fork or old beta use at protected converting tips,
beta/mixed single-step laws, arbitrary-length sequence induction, the corrected
potential, persistence of positive deficit, and arbitrary-length endangered-list
logic behind the circuit predicate. The source/beta AND truth table is also
checked. It is NOT an end-to-end formalization of the full-flow transformations,
canonical gap incidence, family geometry, common freezing, or component matching
proof. Those are written proofs and executable adapters. The
[formal receipt](../output/monotone-completion-deficit-formal-validation.json)
records executed scope and individual axiom audits. No external review is
claimed. A NyxID independent-broker review was attempted as task
2e952a46-bebf-498e-b125-2bea532dbf16 and terminated with
model_unavailable@selecting_model, returning no answer. The
[failed-request receipt](../output/monotone-completion-deficit-oracle-review.json)
records that limitation; it is not an acceptance or rejection of the theorem.
Submitted manuscripts and correspondence are unchanged.

The next geometric question is which nonmonotone T exchanges, or allowed
changes of P or auxiliary N, can repair a persistent deficit while charging
each original resource only once and preserving the required freezing.
Adding T alone is now excluded as a repair mechanism in the entire fixed-P,M,N
model, rather than only in previously studied families; a successful T exchange
has the necessary deletion budget just proved.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
