# Degree-changing bent completions, source births and sharp full-network cuts

26 October 2026. Wenlin Zhang and Haobo Ma. Independent research continuation.

General continuation: [permanent links and a joint completion
budget](MONOTONE_COMPLETION_DEFICIT_AND_BIRTH_CIRCUITS.md) proves that existing
band links persist, full deficit cannot fall under feasible additions, and
its growth is at most added selections minus old beta-to-alpha births.
It also treats shared resource loss, private beta removal and new source
demands in one frozen physical family, including arbitrarily large joint
birth obstructions with every proper birth subset payable.

The [preceding reserve theorem](BENT_GAP_PRIVATE_RESERVES.md) kept the occupied
degree of every P endpoint fixed. Here we allow arbitrary feasible additions to
T, retaining only P, the actual matching M and all old selections. We prove:

* In any fixed physical band decomposition, every newly born alpha owns a
  distinct actual M edge whose two physical N partners are not adjacent.
  This includes restored matching edges across mixed-direction seams.
* For every even width w>=6, EVERY such completion of the frozen occupied-bent
  family still has exactly its original q alphas, all payable at zero links.
  The sharp private reserve per alpha is g(6)=3 and g(w)=2 for even w>=8.
* The full-network withdrawal deficit is at most floor(|R|/g(w)). This is
  sharp: a feasible degree-changing completion converts the former beta
  escape route into a mixed chain with no exit, so withdrawing exactly g(w)
  private units per source really leaves it unpaid in the complete network.

The full ORIGINAL pool still pays all q sources. The obstruction concerns
explicit interval withdrawals and extending the old beta-fallback rule beyond
its hypotheses. It is not a counterexample to the numerical inequality. The
universal 5/6 improvement remains open. The underlying occupied-bent family and
the elementary two-BB-ends bound are existing results; the contribution here is
the coverage of all degree-changing completions, sharp reserve and stable
whole-network cut, together with source-birth localization at physical edges.

## 1. Physical model and fixed bodies

Let G be an even rectangle with its grid adjacency. M is an actual matching of
adjacent sites, P is its endpoint set, and T is disjoint from P. Feasibility
means every selected site has at most one neighbour in P union T. Fix a
partition into even-by-even rectangles, each tiled by uniform horizontal
two-row bands or uniform vertical two-column bands. N is the resulting PHYSICAL
perfect matching of adjacent sites; it does not change during a completion.
All actual M edges, including those crossing region boundaries, are restored
before components are formed.

The multigraph on P with actual M edges and those N edges having both ends in P
has degree at most two. Its path/cycle bodies depend only on P,M,N. An open
end p has N(p) outside P and is TP or BP according as N(p) is selected or blank.
Bodies with two TP ends are alpha, two BP ends beta, one of each mixed.
Parallel M,N edges are retained, so a coincident pair is a cycle, not a path.

A monotone completion replaces T0 by feasible T>=T0, keeping P,M,N fixed.
Bodies do not change; TP ends cannot revert, while a BP end converts precisely
when its N partner is added to T. Thus alpha stays alpha, mixed can become
alpha, and beta can become mixed or alpha. Cycles do not change.

We use the original interval/whole-beta/fork model of the preceding notes.
Its permitted cancellation links are TP--BP adjacencies ALONG a physical band:
horizontal between successive columns in a two-row band, or vertical between
successive rows in a two-column band. All such links are included. Arbitrary
adjacencies between different bands are not added to this declared link model.
Throughout, "complete/full network" means this complete standard band-link
network with all original interval and whole-beta resources, not a model with
an enlarged set of cancellation operations.
L is the total number of positive original BB/TT forest units, a,b,m are the
global open-owner counts, and

    S=|G|/2-|T|-|M|=L+b-a.                            (1)

An interval has one identity, even if supported from both gap boundaries.
One whole beta supplies one credit. No virtual corridor rematching is used.

## 2. Square barrier and a source-birth tax with no duplicate edges

Call an actual edge p--M(p) square-compatible if N(p) and N(M(p)) are
grid-adjacent. This term is only used for physical N. If p is BP, the four sites
are distinct: N(p) is outside P, and N is an involutive perfect matching.

**Square barrier.** Suppose BP p converts in a monotone feasible completion
and its M edge is square-compatible. Then the old body containing p is the
single-edge beta {p,M(p)}, and it becomes mixed, never alpha.

Indeed the new selection N(p) sees its P anchor p. It also sees N(M(p)). If the
latter were old P or old T, it would have two different occupied neighbours.
It was therefore blank: M(p) was also BP, neither endpoint has an N edge inside
P, and the whole body is the single actual M edge. The two N partners cannot
both be selected in the completion: either would see its P anchor and its
adjacent selected partner. Only one BP can convert. This proof does not assume
degree three, freezing or uniform band direction.

Let r count mixed-to-alpha transitions, s beta-to-alpha transitions, t
beta-to-mixed transitions, x converted old BP ends and p_add new selections.
With primes denoting final counts, the exact inventory is

    a'=a+r+s,       b'=b-t-s,        m'=m+t-r,
    x=t+2s+r,       b'-a'=b-a-x,
    L'=L-p_add+x.                                     (2)

The first four equations classify fixed bodies. The fifth is their difference;
the sixth follows by applying (1) before and after completion. It is a count
identity, not a claim that each old interval retains its identity. In fact
x<=p_add: distinct converted BP ends have distinct newly selected N partners.

Let c_bad count converted BP incidences whose actual edge is NOT
square-compatible. The square barrier implies

    r+2s<=c_bad.                                       (3)

There is a sharper statement counting actual edges only ONCE. For each new
alpha choose one converted BP end and its non-square-compatible actual edge.
Different new alphas lie in disjoint fixed bodies, so they cannot choose the
same M edge. Consequently

    a'-a <= number of distinct actual M edges incident
            to converted BP ends and not square-compatible.  (4)

A beta birth may use two BP incidences of ONE edge; it is still just one
edge in (4). Equations (3),(4) are different valid budgets. An edge shared by
two regional descriptions is not charged twice. In horizontal bands, where N
is vertical, horizontal actual edges are square-compatible. Actual vertical
edges crossing N bands, and direction interfaces, must be checked physically.
No claim is made that all non-square edges are direction interfaces.

Both birth types occur. On a 4-by-2 board take the single actual edge
(1,0)--(2,0) and vertical N pairing rows0/1 and2/3. With T0 empty, adding
(0,0),(3,0) makes a beta into an alpha: two bad incidences on one edge.
Starting instead with T0={(0,0)} and adding (3,0) gives a mixed birth.
These small controls are feasible but are not claimed frozen. Section 7 gives
fully frozen, mixed-direction examples attaining (4) for every q.

## 3. All completions of the occupied-bent family

Use exactly occupied_bands(w) from
[degree_three_fusion.py](../develop/degree_three_fusion.py), even w>=6, and
the existing uniform certificate occupied_band_certificate(w). Its construction
and all-width freezing proof are in
[degree-three fusion, Section 9](DEGREE_THREE_FUSION_AND_PROTECTED_DONORS.md).
The board is 8-by-(2w+2), with

    |P|=4w+12, |M|=2w+6, |T0|=14,
    a=1, b=w-1, m=0.

Use horizontal bands, N pairing rows0/1,2/3,4/5,6/7. Its alpha body is

    {2,3} x {w+1,...,2w}
    union {4,5,6} x {w+1,2w},                           (5)

with TP tips (6,w+1),(6,2w). Every old beta is a single horizontal M edge, hence
square-compatible. There are no old mixed owners. By the square barrier no
beta can become alpha, so EVERY feasible monotone completion has exactly the
same one alpha, although beta owners can become mixed and P degrees can rise.

For q copies translate by row offsets10i, 0<=i<q, on a
(10q-2)-by-(2w+2) rectangle. The intervening two rows are initially blank and
are also allowed to receive selections. They introduce no P bodies. Thus the
final alpha count is exactly q for all completions, not just those restricted
to the two gap rectangles below.

Strict freezing also persists. Replay the old ordered endpoint certificate:
each endpoint has two distinct retained occupied witnesses, consisting of old
T or endpoints earlier in the schedule. Adding selections cannot remove those
witnesses. The argument neither requires nor asserts preservation of endpoint
occupied degrees. The same certificates replay in all separated copies.

**Sharp private reserve theorem.** In every such completion each alpha has at
least g(w) private original interval units, where

    g(6)=3;    g(w)=2 for even w>=8.                    (6)

Proof. Put n=w-2 and look at columns w+2,...,2w-1. There are two internal no-P
gaps, in rows4/5 and rows6/7. Both P boundaries of either gap belong to (5),
so every unit there is private to that alpha. Different gaps/copies have
different resource identities.

In the lower gap, the row6 site at each end has TWO retained occupied
neighbours: its side P and the row5 end selection. It cannot be newly selected.
The row7 end site neighbours a retained axial selection, (7,w+1) on the left
or (7,2w) on the right, already saturated by its row6 P anchor. It too cannot
be selected. Both end columns therefore remain BB without any degree-profile
hypothesis. In an internal gap each BB/TT forest starts and ends in BB and
has one unit. If both end BB columns belonged to the same forest, that forest
would span the entire gap and have odd length. But n is even. The two ends
give two distinct units.

For w=6 the upper gap has n=4 and has at least one further unit. A zero-unit
internal gap contains neither BB nor TT, hence has exactly one selection in
each column. The retained bottom selections at j=0,3 already see their side
P anchors; bottom sites j=1,2 must be blank. Thus zero capacity would force
both top sites j=1,2 selected. They are adjacent and each sees the retained
row3 P bar, violating feasibility. For w>=8 no positive upper-gap lower bound
is asserted. This proves (6). Notice that a BT/TB word need not alternate:
horizontal selected pairs are permitted. The lower-gap parity argument is
the existing two-BB-ends lemma, now with protection valid under degree changes.

The original alpha's other incident gaps have zero capacity in T0. With P
fixed, a gap's capacity is its length minus its selected-site count; it cannot
increase under T additions. They remain zero. In particular all of the alpha's
current support is confined to these private gaps; this fact will also give
the exact withdrawal formula below. The private inventory gives L>=g(w)q and

    S>=b+(g(w)-1)q.                                    (7)

Here b is the FINAL beta count, not the old (w-1)q. This is a coefficient-one
statement on this already compensated family, not an improvement of universal
5/6.

## 4. Explicit completions attaining the private minimum

Write j=c-(w+2), 0<=j<n=w-2. Define two index sets A,B:

    w=6:  A={1}, B={0,n-1};
    w>=8: A={1} union {4,6,8,...,n-2},
           B={0,...,n-1} minus A.

Retain T0. Select row4 at indices A and row5 at indices B; some row5 sites are
already selected. For every interior index 1<=j<=n-2 select row7 if j is in B,
and row6 otherwise. Translate this prescription in every copy.

Feasibility can be checked for all widths directly. For w>=8, A has the
isolated index1 and then separated even indices; every row4 selection is
isolated in its row and sees just its row3 P anchor. In B the only interior
horizontal pair is j=2,3; j=0 is separated by1, and the final end j=n-1 is
separated by n-2. The interior pair sees just its partner; row5 end selections
see their side P anchors. At w=6 the unselected j=2 separates the retained
bottom end j=3 from the others. In the lower gap row7 is used exactly below
selected row5, leaving one blank row between them. Its only possible interior
horizontal pair is again2,3. At w>=8 the remaining row6 selections are
isolated; at w=6 its two interior selections form one horizontal pair.
All have blank row5 neighbours. Lower end columns stay BB and isolate these
additions from the retained axial selections. No other old T acquires a
second occupied neighbour. The original freezing certificate persists.

For w>=8 every upper-gap column has one selected site, so it has zero units.
For w=6 the upper-gap word has a single BB at j=2 and no TT, so has one unit.
In the lower gap only the two end columns are BB, and all interior columns
are BT/TB. It has exactly two units. All other incident gaps remain zero.
This attains (6), with per-copy

    |T|=2w+6-delta,    S=4w-4+delta,
    delta=1 if w=6 and 0 otherwise.                    (8)

This construction changes endpoint degrees; it is not in the extension class
of the preceding floor(w/3)+2 theorem. At w=8 the gap rows are:

| Physical row | Gap columns10,...,15 |
| --- | --- |
| 4 | BTBBTB |
| 5 | TBTTBT |
| 6 | BTBBTB |
| 7 | BBTTBB |

The upper gap has no units, and the lower has exactly two. The sharp old
degree-preserving reserve was four at this width.

## 5. Arbitrary joint withdrawals and the full-network upper bound

Fix any completed configuration in Section 3. Let U_i be ALL current original
intervals supported by its ith alpha. These are private among all global open
owners, disjoint over i, and |U_i|>=g(w). Withdraw any set R of distinct current
ORIGINAL INTERVALS, without changing T,M,N or removing beta credits. Set

    t(R)=number of i with U_i subset R.

Each source with a surviving unit can take its own private unit, and a source
with none has no direct payment. Thus the exact direct deficit is t(R), and

    g(w)t(R)<=|R|.                                     (9)

The complete whole-fork model includes this zero-link allocation. Writing V
for its maximum paid-source count gives

    0<=q-V<=t(R)<=floor(|R|/g(w)).                      (10)

This proves a joint bound without counting a private interval twice. It does
not say that every direct loss is a full loss: in the degree-preserving class,
the dedicated beta fallback of the preceding note always repairs it. The next
section shows that conclusion cannot be extended to all completions here.

## 6. Sealed mixed chains: sharp FULL withdrawal deficit

Starting with the sharp completion of Section 4, also select

    (7+10i,c),  c=1,3,...,w-1,  for every copy i.        (11)

These selections are separated by blanks, each sees only its row6 P anchor,
and column w separates them from the retained axial selection at w+1. Thus
the board remains feasible and fully frozen. Its per-copy inventory is

    a=1, b=w/2-1, m=w/2,
    |T|=2w+6-delta+w/2.                                (12)

The row6 single-edge betas at columns (1,2),(3,4),...,(w-1,w) are now mixed:
the odd endpoint is TP, the even endpoint BP. The alpha's left TP at w+1
links to the BP at w, then successive mixed owners give the directed chain

    alpha -> (w-1,w) -> (w-3,w-2) -> ... -> (1,2).       (13)

This is the COMPLETE source-reachable owner graph in the standard band-link
model, not a proposed subgraph. All reachable TP ends are in row6; their
permitted links run horizontally in band rows6/7. An internal odd TP can
link left only to the preceding even BP, besides its own mate which gives
no inter-owner link. The last TP at column1 faces the old selected site at
column0 and has no further link. The alpha's right TP at column2w faces an
old selected site at2w+1 and likewise has no exit. Inter-band vertical
adjacencies are outside the cancellation operations fixed in Section 1;
they must not be silently included or used to claim a stronger obstruction.

Each chain owner has empty WHOLE interval support. In rows6/7 the contiguous
P block at columns1,...,w has no interior no-P gap. Its outer column0 gap
is BT and has zero capacity; on the right column w+1 is P of the alpha.
No chain owner meets any other band. There is no reachable beta, no interval
sink on the chain, and no cross-copy route. Other original resources and
the remaining upper betas are present but unreachable from these sources.

Closure is stable under every further feasible monotone completion retaining
(11). Each row7 site at an even chain column neighbours a retained selected
odd site already saturated by its P anchor, so it cannot be selected. The
chain's BP ends therefore cannot convert. Its TP ends, endpoint bodies and
all candidate link adjacencies are fixed. Its gaps had zero capacity, which
cannot rise under additions. Fixed physical adjacency and fixed P forbid
new inter-copy links, even if the separating blank rows receive selections.
Alpha-private supports can change identities and sizes, so recompute U_i in
the final configuration when making withdrawals.

It follows for EVERY such sealed extension and every R that

    V_full(R)=q-t(R),    minimum links at this value=0. (14)

The surviving direct assignments attain this value. A blocked source can
only enter (13), which has neither a surviving interval nor a beta credit;
following, merging or truncating this dead chain cannot pay it. This proves
the upper bound in the full model with all undeleted original resources and
all beta owners available. No locked old allocation is assumed.

For the explicit sharp sealed completion, withdraw precisely union_i U_i.
Then |R|=g(w)q, t(R)=q and V_full=0. This attains (9),(10) for all w,q.
Withdrawing the support of any chosen subset similarly makes exactly those
sources unpaid. In contrast R empty gives V_full=q at zero links.

The [stored w8 fixture](../develop/fixtures/degree_changing_bent_w8.json)
has 44 P endpoints,22 actual matching edges,26 selections, one alpha,three
betas,four mixed owners and exactly two alpha-private original units. It
includes all 44 retained strict freezing events. Removing both units gives
full value zero; without withdrawal the value is one. Its numerical slack
is24. The failed candidate rule is “the old dedicated beta always remains
an available fallback after arbitrary degree-changing additions”, not the
target numerical bound or original-full-pool compensability of this family.

## 7. Sharp frozen births at actual mixed-direction seams

The edge tax (4) is also attained in fully frozen models. Keep the SAME P,M,T0
of Section 3, but choose N vertically in the region consisting of columns0,1
and horizontally in the region of columns2,...,2w+1. These are valid even
rectangles. In particular restore the actual M edge (6,1)--(6,2) crossing
their boundary. Direct tracing gives initially a=b=0,m=3 per copy. Add only
(7+10i,1) in each copy. These selections each see just their P anchor and
preserve the old strict freezing certificate.

Now the BP at p=(6+10i,1) converts; its actual mate is (6+10i,2). The physical
N partners are (7+10i,1) and (6+10i,3), at grid distance three. Their edge is
not square-compatible. The newly born alpha body in a single copy is

    {2} x {w,...,2w}
    union {3,4,5} x {w,w+1}
    union {6} x {1,...,w+1},                            (15)

with TP tips (2,2w) and (6,1). The remaining bodies are two mixed paths; there
are no betas. One can trace (15) by alternating actual M and PP_N edges:
the row2 run goes left from2w to w, turns down the two-column leg at w,w+1,
then follows row6 left to1. Every other P endpoint continues along the two
remaining mixed paths. Hence the inventory changes (0,0,3)->(1,0,2).
Copies are separate; exactly q new alphas use q distinct crossing M edges.
There are no other BP conversions in this construction. Equality holds in
(3) and (4). This is a general family, not just a small numerical search.

These born alphas have original interval support and can be paid at zero
links. They are a warning to count new source demands at mixed seams, not
counterexamples to compensation. Existing degree-four/seam localization
results concern other tile incidences; they do not replace this fixed-body
monotone transition account.

## 8. Reproducibility and exact formal scope

From the repository root run:

    python3 develop/check_degree_changing_bent_completions.py --output output/degree-changing-bent-completions-validation.json
    python3 develop/check_degree_changing_bent_completions_formal.py --lean /path/to/lean-4.33.0 --output output/degree-changing-bent-completions-formal-validation.json

The [physical receipt](../output/degree-changing-bent-completions-validation.json)
records PASS for 196 family models, including168 genuinely degree-changing
models and56 sealed models, at widths6,8,10,14,20,32,64 and copy counts1,2,3,7.
There are63,700 strict family rank events,1,813 joint interval withdrawals,
756 full-network value/cost comparisons and28 sharp full-deficit controls.
All feasible completions inside the two gap rectangles are checked at w6
(33) and w8 (1,956), agreeing with the written minima3 and2. These enumerations
test the proof; they do not establish arbitrary-width or all-board coverage.

Across374 monotone transition models,7,705 converted BP incidences satisfy
the exact ledger;107 mixed births and one beta birth have108 distinct owned
edge witnesses. There are24 sharp frozen seam models,5,616 strict seam rank
events and24 comparisons with the independently compiled crossing-edge
ledger. Another152 mixed-direction transition models test the general count
identities without claiming a fresh freezing audit for every such model.
The stored fixture independently replays44 freezing events.

Local Lean4.33.0 checks12 declarations and their individual axiom dependencies:
the two square exclusions; fixed-body and resource transition arithmetic;
birth budgets and the zero-birth corollary; actual-edge witness injection;
two-neighbour protection; the width-six zero-gap-to-infeasibility interface;
private withdrawal division; and two/three-unit ledger consequences. There
are no warnings, sorry placeholders, native evaluation or new axioms. The
width-six declaration assumes the geometric zero-gap adapter, and the
injection declaration assumes the owned-edge witness adapter. They must not
be described as end-to-end graph formalizations.

The general M/PP decomposition and square adapters, coordinate family and
seam tracing, all-width feasibility, inherited freezing, private allocation
and sealed complete-network closure are WRITTEN proofs above, supported by
executable checks, not end-to-end Lean certification. Permanent artifacts:

* [Physical checker](../develop/check_degree_changing_bent_completions.py).
* [Lean source](../formal/SubQuorum/DegreeChangingBentCompletions.lean).
* [Formal runner](../develop/check_degree_changing_bent_completions_formal.py)
  and [receipt](../output/degree-changing-bent-completions-formal-validation.json).
* [Sharp sealed physical fixture](../develop/fixtures/degree_changing_bent_w8.json).

The next general obstruction is not absence of resources in this occupied
family: its full pool is always sufficient. It is whether source births and
resource loss in genuinely shared mixed-seam networks admit a single geometric
budget, with each physical edge, interval and whole beta charged once. Short
bends lacking these protected BB ends and source-changing N rematchings also
remain outside the theorem. Submitted manuscripts and correspondence are
unchanged.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
