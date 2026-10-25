# Exact frozen repair frontier under arbitrary selection exchange

26 October 2026. Haobo Ma and Wenlin Zhang. Independent research branch.

For the adjacent-module endpoint family of
[unique mates and exact maxima](FORCED_MATES_AND_ADJACENT_MAXIMA.md), we prove
an exact tradeoff over **all feasible final selected sets T**, allowing arbitrary
removal, addition and replacement of the original selections. The actual
matching is fixed (and unique), and the band matching is uniform horizontal.
This removes the retained-T restriction of the
[monotone completion theorem](MONOTONE_COMPLETION_DEFICIT_AND_BIRTH_CIRCUITS.md).

For even W>=8 and k>=1, write

    tau = (7k+2)(W/2)+3k+2,
    ell = tau-|T|,
    D = alpha-V,

where V is the optimal number of paid alpha sources in the complete original
whole-support network, including distinct physical BP entry capacities,
whole-beta credits and two-entry beta forks. If the two column3 leaves of
each module freeze, then

    ell + D >= k + b_A,                                  (1)

where b_A is the number of central column5 bodies that are beta. In particular,
for every integer 0<=d<=k,

    max {|T| : T feasible, all P frozen, D<=d} = tau-k+d.  (2)

Every fully frozen true fixed-P maximum has exactly k alphas and D=k.
Complete repair requires a **net loss of at least k selections**, even if all
of T may be reselected. This is stronger than a necessary deletion count:
adding replacement points cannot recover that cost while the stated leaves
remain frozen and this horizontal decomposition is retained. Starting from
T*, if p original selections are removed and q new selections are added,
(1) reads D_final>=k-p+q+b_A. This explicitly charges replacement additions,
which the earlier general deletion-only necessary condition did not do.

The proof is a coupling of two injections: missing central tips and available
payment sinks charge distinct members of a disjoint geometric cover; paid
sources inject into those sinks. A shared interval or whole-beta credit is
counted once. The strengthened term b_A pays for both missing central tips
when the central body itself ceases to be a source.

## 1. Fixed geometry and precise scope

Use rows0..W+1 and columns0..10k+1. For module i set c=10i. Its P vertices are

    columns c+4,c+5,c+6: rows1..W;
    columns c+3,c+9: rows1,W;
    columns c+7,c+8: rows1,W-1,W.

Take exactly the matching M in Section1 of the unique-mates note. Its successive
leaf elimination proves it is the unique actual perfect matching on P,
independently of T. The standard horizontal bands have rows(0,1),(2,3),...,
(W,W+1); N pairs the two sites in each column of each band.

Feasibility means T avoids P and each selected site has at most one neighbour
in P union T. No old selections must be retained. All original interval units
are present; there are no reservations, restricted ports or prescribed payments.
D refers to this fixed physical N, with every actual M edge included.

The minimal extra hypothesis we use is the following four-site seal, for
every i:

    (0,c+3), (1,c+2), (W,c+2), (W+1,c+3) belong to T.      (3)

It follows if the two leaves (1,c+3),(W,c+3) freeze in the strict peeling
process. To see this at the first freezing time of (1,c+3), its only P
neighbour is its actual mate (1,c+4). That mate cannot yet count as a kept
witness: its own mate is precisely the not-yet-frozen leaf. The three nonmate
neighbours are (0,c+3),(1,c+2),(2,c+3). The last has two P neighbours,
(1,c+3),(2,c+4), and so cannot be selected. Two distinct kept witnesses
therefore force the first two sites into T. The bottom argument reflects
rows, using (W-1,c+3), whose P neighbours are (W,c+3),(W-1,c+4).
Conversely (3) freezes these leaves in the first round. Thus only these 2k
leaves, rather than all endpoints, are needed for (1). In particular, no
assumption about (0,c+7) being selected is used.

## 2. All possible bodies and payment sinks

The M/PP body decomposition is independent of T. In each module its open
bodies are exactly:

- A_i, the entire column c+5 at rows1..W, with tips (1,c+5),(W,c+5);
- the six single-M-edge bodies at rows1,W and column pairs(3,4),(6,7),(8,9), translated by c;
- the single-M-edge body at rowW-1 and columns(c+7,c+8).

The remaining bodies are cycles. This follows by tracing the matching pairs
in the unique-mates note: N joins successive central pairs into A_i; the
column4/6 M edges not in terminal bodies coincide with PP edges and form
double-edge cycles. The listed seven single-edge bodies have N partners
outside P at both ends.

No single-edge body can be alpha. Its two N partners are adjacent; if both
were selected, either selected site would see its own P anchor and the
other selected site. Thus only the k central bodies can be alpha. Let their
alpha, mixed and beta counts be a,m_A,b_A, with a+m_A+b_A=k. The total number
of missing selected N partners of central tips is

    m_A+2b_A = k-a+b_A.                                  (4)

Every central body's original interval support is empty: in every band its
column5 is flanked by P columns4 and6, including the contiguous terminal
P block in columns3..9.

All inter-owner standard TP-to-BP band links lie in rows1 or W, inside one
module, along the terminal P block. Indeed only those rows have adjacent
tips of different bodies; the penultimate body's column6 neighbour is PP,
not a tip. The no-P gaps between slabs have length three and contain no
P tip through which a link could cross. Consequently every source route
stays in the union of central and terminal bodies. A central body can connect
its own top and bottom rows, but this introduces no new interior support.
The penultimate body is unreachable from any source. Each module has at
most one alpha, its central body. Since links never change the module, a
reachable central body must be that module's alpha itself; no central beta
can be a payment sink for a source in another module.

Let B_term count all beta bodies among the six terminal bodies per module,
including any not reachable, and let L_term count all original interval units
in the top and bottom bands. Every possible paid source ends at a terminal
whole-beta credit or a terminal-band interval unit. Each sink has capacity
one. In a two-entry beta fork, the two payments use its one beta credit AND
a distinct interval; the beta does not provide two credits. Thus

    V <= B_term+L_term.                                  (5)

Overcounting unreachable terminal sinks only weakens this upper bound.
The units in L_term are actual original forest units, counted globally;
a gap shared by two modules is not counted once per owner.

## 3. One disjoint cover, with three disjoint charges

Use the existing ALL-T upper cover from Section3 of the unique-mates note.
Start with the aligned2-by2 tiles. In each module replace the two vertically
adjacent tiles at upper-left coordinates(0,c+2),(2,c+2) by their4-by2 union,
and similarly replace(W-2,c+2),(W,c+2) by their union. Each replacement has
cap3 instead of the old total cap4. These patches and all remaining tiles
partition the entire board. Their valid caps sum to tau.

For completeness, the tile cap rows before replacement are

    terminal:    [2,2,1,1,1] repeated k times, then2;
    interior:    [2,2,0,1,2] repeated k times, then2;
    penultimate: [2,2,0,0,1] repeated k times, then2.

Interior occurs W/2-2 times. Cap2 is the general square bound; cap0/1 follows
by excluding P and sites with two P neighbours. Each4-by2 patch has just six
permissible sites, partitioned into three pairs that cannot both be selected
(the outside horizontal pairs and the middle vertical pair, each facing a P
anchor); hence cap3. The initial sum is (7k+2)(W/2)+5k+2 and the 2k patches
save one each. This proves the upper bound for every feasible T.

For each cover member C define its loss as cap(C)-|T intersect C|>=0.
All member losses sum to ell. We charge the following **different** members.

### Central-tip losses

For each module take the top and bottom tiles at columns(c+4,c+5). Their
terminal row consists of P; their cap is1. The outer site at column c+4
cannot be selected, because the adjacent seal at column c+3 is selected
and already sees its own P anchor. Hence the tile loss is exactly1 when
the central N partner at column c+5 is absent and0 otherwise. By (4) these
2k tiles have total loss k-a+b_A.

### Terminal-beta losses

A terminal body(3,4) cannot be beta, since its outer column3 partner is a
seal in T. For any beta terminal body(6,7) or(8,9), both outer N partners
are blank. Its aligned tile, with terminal row in P, has cap1 and occupancy0.
Charge that tile's unit loss. Distinct terminal betas use distinct tiles,
so the total charge is B_term. These tiles are neither central-tip tiles
nor any of the replacement patches.

### Terminal interval losses

In each terminal band, all no-P gaps are

    [10i,10i+3) for i=0..k-1, and [10k,10k+2).

For a length-three gap with c=10i, its terminal column c+2 site is a seal
in T and its outer column c+2 site must be blank: it is adjacent to the
outer seal at c+3, which already sees P. The gap has exactly1 plus the
number of selections in the aligned tile at columns(c,c+1). Its original
unit capacity is gap length minus its selected count, so it equals

    3-(1+|T in that tile|) = 2-|T in that tile|.

This is precisely the loss of that cap2 tile. The final length-two outside
gap has capacity2-|T in its cap2 tile| as well. The equality between gap
capacity and the number of original forest units is the standard BB-minus-TT
identity, also checked by the band compiler. Summing these particular tiles
in both terminal bands gives exactly L_term. Each shared length-three gap
uses one tile globally, regardless of which neighbouring owner reaches it.

The three sets of charged members have left columns congruent to4,
6-or8, and0 modulo10, respectively (plus the final outside gap tile).
None is replaced by a patch, whose left column is2 modulo10. They are
pairwise disjoint across modules and across terminal bands. Therefore

    ell >= (k-a+b_A)+B_term+L_term.                       (6)

Combining (5),(6) and D=a-V proves (1). In terms of numerical slack
S=|grid|/2-|M|-|T|=2k+ell, it also says

    S+D >= 3k+b_A.                                      (7)

This counts one physical loss for each missing tip or candidate payment
sink. It does not allocate one source's reserve twice or count a shared
gap twice.

## 4. Exact frontier and uniform frozen attainers

For D<=d, (1) and b_A>=0 give |T|<=tau-k+d. Start from the explicit frozen
maximum T* in `configuration(W,k)`. It contains all central tip partners,
all four seals per module, has a=k, B=0, V=0 and D=k. In any chosen k-d
modules delete only

    y_i=(W+1,10i+7).

Their lower terminal(6,7) bodies change from mixed to beta, because their
outer column6 sites were already blank. All k central alpha bodies remain.
Each chosen module now pays its own source through the one link

    (W,10i+5) -> (W,10i+6).

These beta owners and physical tips are distinct across modules. No gap
changes: y_i had a P anchor and was outside every no-P gap. There are no
other new sinks reachable by a source, so V=k-d, D=d and the minimum number
of links is k-d. In particular the attained size is tau-k+d.

All deletion subsets stay fully frozen. Here is an explicit common strict
schedule, rather than an appeal to finite enumeration. In each module put
first the translated singleton endpoints

    (1,3),(W,3),(1,9),(W,9),(1,7),(W-1,8),(1,5),(W,5),(W,7).

The first four see their two retained outer/side T neighbours. Next (1,7)
sees its outer T and the kept P at(1,8), whose mate(1,9) froze earlier.
The endpoint(W-1,8) sees its retained outer T at(W-2,8) and the kept P at
(W,8), whose mate(W,9) froze earlier. The two central terminal endpoints
see their retained outer T and a kept terminal P neighbour. Finally(W,7)
sees kept P neighbours(W,8) and(W-1,7), whose mates(W,9) and(W-1,8) have
already frozen. None of these steps needs any y_i. Then append the original
uniform strict freezing schedule, omitting the endpoints already listed.
In that original schedule y_i could supply a selected witness only to
(W,10i+7), which is already frozen; every other old dependency is retained
or moved earlier. This proves a valid strict schedule for every subset,
all even W>=8 and all k. It also explains why keeping the lower(6,7) body
frozen does not require its deleted outer column7 selection.

This proves (2). For d>=k the maximum is tau. At ell=0, (6) forces all three
nonnegative charges to vanish. Equation(4) forces a=k,b_A=0, and (5) forces
V=0. Thus **every** sealed size-tau selection, including every fully frozen
one, has D=k; changing which maximum is selected cannot repair this N.

### Full central-inventory refinement

The beta correction in (1) is sharp, including when some central bodies are
mixed. Fix nonnegative integers a,b with a+b<=k and a threshold d>=0. Among
fully frozen feasible selections with exactly a central alpha bodies and b
central beta bodies, the exact optimum is

    max |T| = tau-k-b+min(a,d), subject to D<=d.           (8)

Indeed the missing central partner count is k-a+b. Equations(5),(6) give both
ell>=k-a+b (all losses are nonnegative) and ell>=k+b-D>=k+b-d.
Their maximum is k+b-min(a,d), proving the upper bound.

For attainment choose a modules as alpha, b others as beta and the rest as
mixed. From T* delete the top central partner(0,c+5) in every nonalpha
module; also delete the bottom central partner(W+1,c+5) in each chosen
central beta module. This costs k-a+b selections. In exactly max(0,a-d)
alpha modules also delete y_i to open its private lower beta, and pay that
source by the same one-link route. No terminal gap changes. There is no
inter-module route, so the central beta bodies in other modules cannot pay
an alpha. Thus V=max(0,a-d), D=min(a,d), and |T| attains (8).

These selections are fully frozen even with both central partners absent.
Use the preceding prefix with (W,7) moved **before** (W,5). The former still
has the earlier witnesses(W,8),(W-1,7). The top central endpoint then has
kept P witnesses(1,4),(1,6), and the bottom central endpoint has kept P
witnesses(W,4),(W,6); neither needs its own outer selected partner. Append
the original uniform schedule as before. Every newly deleted selected
central partner is adjacent to exactly its central terminal endpoint in P,
which the prefix already freezes. Thus this single schedule works for all
inventories and all threshold choices, with no retained-central-partner
assumption. Maximizing (8) over a,b recovers (2).

## 5. Removing freezing: an exact boundary defect term

The same cover gives a useful inequality for **every feasible T**, with no
freezing hypothesis. For each module and each of its terminal bands, call the
row in P the terminal row and the other row the outer row. Let

    O3 = number of absent outer selections at column c+3;
    Z2 = number of terminal-band column c+2 pairs containing no selection;
    E = O3+Z2.

Then for arbitrary final T on this fixed P,M,N,

    ell+D+E >= k+b_A.                                   (9)

This is an explicit correction to the frozen inequality, using actual
physical occupations. To prove it let O4 count selected outer sites at
column c+4 and split the terminal beta count into B_left (the terminal
column pair3,4) and B_right (pairs6,7 and8,9). The source tiles have exact
loss (k-a+b_A)-O4: the former seal-forbidden column4 site may now be selected.
Feasibility prevents the adjacent outer column3 and4 sites from both being
selected. Thus on each terminal side, an absent outer column3 site is
accounted for exactly once by either an occupied outer column4 site or the
left terminal body being beta. Therefore

    O4+B_left = O3.

The two sites at column c+2 cannot both be selected, since the terminal one
already has its P anchor at column c+3. A terminal length-three gap consequently
has capacity equal to its cap2 gap-tile loss plus1 exactly when this column2
pair is empty, and plus0 otherwise. The final outside gap remains unchanged.
Hence the total charged gap-tile loss is L_term-Z2. The same disjoint member
sets from Section3 now give

    ell >= (k-a+b_A)-O4+B_right+L_term-Z2,
    V <= B_left+B_right+L_term.

Adding them proves (9). No left-beta tile inside a replacement patch is
charged as if it were a separate cover member; its contribution is precisely
part of the explicit boundary correction O3.

Let U be the number of the 2k designated column3 leaves that do not freeze.
The first-freezing argument in Section1 still proves that each such leaf
freezes iff its two seals are selected. Per terminal side, its contribution
to E is0 exactly when both seals are present, and otherwise1 or2. Indeed
if the outer column3 seal is absent it already contributes1 to O3; if it is
present but the terminal column2 seal is absent, the outer column2 site is
forced blank, giving1 to Z2. Conversely both seals present give no defect.
Thus

    U <= E <= 2U,
    ell+D+2U >= k+b_A.                                  (10)

In particular a size-tau completely paid selection must leave at least
ceil((k+b_A)/2) of these designated endpoints unfrozen. For fully frozen T,
E=U=0, recovering (1). We do not claim the coefficient2 or the unfrozen-leaf
count lower bound is sharp for arbitrary inventories; the frozen and fixed-
inventory optima in Sections1–4 are sharp.

## 6. Why the hypotheses matter

The permanent fixture
[`nonfrozen_zero_loss_selection_repair.json`](../develop/fixtures/nonfrozen_zero_loss_selection_repair.json)
has W=8,k=1, |T|=tau=41 and D=0, with only1 of34 endpoints frozen. It is
feasible on exactly the same P and M, but fails the leaf seals. The checker
reconstructs it and verifies feasibility and the full optimal flow after
serialization. It is an excluded control, not a counterexample to (1).
Its T was discovered by an exact row-mask dynamic program; the recorded
witness needs no solver or search to check, and the proof of (1) does not
use that search.

The [perpendicular-reserve theorem](PERPENDICULAR_GUARDED_RESERVES_AND_JOINT_MAXIMALITY.md)
proves full compensation for every feasible T on this P after changing to
uniform vertical bands. Thus the same frozen maximum can be repaired at
zero selection loss by changing N. Our exact net-cost theorem is for the
fixed horizontal decomposition. It is not a lower bound after optimizing
N, or over other P. The universal5/6 improvement remains open. The new result
settles the arbitrary frozen-T exchange option for this family and identifies
direction or endpoint structure as the necessary next change.

## 7. Verification and formalization boundaries

Run `python3 develop/check_frozen_selection_frontier.py --output
output/frozen-selection-frontier-validation.json`. It reconstructs the cover,
all body types, permitted link closure and actual original terminal units;
checks each charge's equality and pairwise disjointness; and compares full
fork-capable optimal payments. It tests T rebuilt from only seals, arbitrary
sparse subsets, greedy completions, and exchanges independently checked to
stay fully frozen. It also checks all sharp deletion subsets for small k,
representatives at larger k, a common strict rank schedule, independent
primitive optima, and the two saved fixtures. These are checks of the written
all-size proof, not a finite proof of its universal quantifiers.

[`FrozenSelectionFrontier.lean`](../formal/SubQuorum/FrozenSelectionFrontier.lean)
formalizes the leaf witness implication, central-tip identity with arbitrary
list induction, disjoint-loss arithmetic, coupled frontier, slack form,
necessary net loss, Pareto upper bound, maximum rigidity and sharpness
arithmetic, including the fixed-alpha/beta inventory upper bound and its sharp min/max construction, and the unsealed boundary-defect coupling and unfrozen-leaf necessary bound. It also proves module invariance of arbitrarily long owner walks, that a reached central body is the source itself, and central beta unreachability. The coordinate edge/unique-central conditions and its cover and payment bounds are explicit hypotheses. It does
not formalize the grid-coordinate cover adapter, route-closure injection or
geometric freezing schedule end to end. The runner records local memory and
real Lean/lake processes before compiling this one small module and audits
each declaration for unapproved axioms. See the permanent JSON receipts in
`output/frozen-selection-frontier-{validation,formal-validation}.json`.

The refinement checker `develop/check_frozen_inventory_frontier.py` replays
the strengthened common schedule with arbitrary central alpha, beta and
mixed inventories. Its permanent receipt is
`output/frozen-inventory-frontier-validation.json`.

The unsealed checker `develop/check_unsealed_selection_frontier.py` rebuilds
arbitrary selections without any retained seals, checks all correction
identities and their relation to the actual peeling process, and records
`output/unsealed-selection-frontier-validation.json`.

Final receipts: the main checker passes1,131 models (600 rebuilt from seals,
300 fully frozen arbitrary exchanges,230 sharp frozen attainers and one
serialized attainer replay), with76 independent primitive optima and118,916
strict freezing events on the sharp attainers. The inventory refinement
passes166 attainers,23 independent optima and66,392 strict events. The
unsealed refinement passes361 arbitrary selections with19 independent optima.
All19 Lean declaration audits pass without warnings or unapproved axioms.
