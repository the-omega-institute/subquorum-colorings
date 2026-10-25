# Boundary zero paths and compensation from adjacent exposed bands

26 October 2026. Wenlin Zhang and Haobo Ma. Independent research continuation.

Continuation: [pressured bent gaps and exact beta repair](BENT_GAP_PRIVATE_RESERVES.md)
handles an occupied family with zero immediate-exposure pair count, proves a
sharp private reserve over all retaining completions, and removes the column
alignment requirement from the same-side boundary exclusion.

Freezing does **not** exclude the double-zero-ended boundary paths left by
[terminal-defect compensation](TERMINAL_DEFECT_PORT_COMPENSATION.md), even
when every occupied endpoint has degree exactly three. We give an explicit
fully frozen 144-endpoint counterexample, and arbitrary separated copies
in which every alpha has two zero-capacity boundary ports. Nevertheless all
alphas have zero-link payments through their whole original bodies.

The positive result is a general adjacent-band lemma: two aligned exposed BB
columns next to the same owner's P column in consecutive bands cannot both
belong to balanced boundary forests. One therefore supplies a genuine original
interval. Disjoint pairs of band indices produce different units. A global
incidence count and allocation theorem handle sharing between owners without
counting any interval more than twice as an incidence or more than once as a
payment. The result applies to bent bodies with the stated local witnesses,
not just the example. The universal coefficient-one bound remains open.

The arguments use the existing original whole-support model and elementary
resource matching. They do not assert a new abstract matching theorem, nor
that all residual alpha paths have the exposed-band witnesses below.

## 1. Geometry and the adjacent-band reserve

Use a feasible pair (T,M) on an even-by-even rectangle with its uniform
horizontal two-row bands and actual matching. Original intervals are the
BB--TT forest components of positive difference one. A balanced component
has difference zero and reaches a lateral TT boundary. Whole support of an
original open M/PP path includes every original interval in a maximal no-P
gap incident to any of its P columns. Identities are the actual physical
forest cells, not separately numbered resources for different owners.

Fix an even row r, a P-column index c, and a side epsilon in {-1,+1}; put
x=c+epsilon. Suppose in both bands {r,r+1} and {r+2,r+3}:

* column x is BB;
* column c contains a P vertex of the same original open owner A.

The owner need not have both P vertices of either column. No degree or freezing
hypothesis is required for this local statement. All four rows and column x
are inside the board.

**Adjacent-band lemma.** At least one of the two BB columns belongs to a
positive original interval supported by A.

Proof. Because column c contains P, the BB at x is an end of its BB--TT
forest on the side facing c. If its forest is balanced, it extends away from
c to a TT at the lateral board boundary. In particular the immediately
outward column x+epsilon exists and is TT in that band. If both forests were
balanced, column x+epsilon would have selected vertices at all four rows
r,...,r+3. The selected vertex at row r+1 would then see its selected partner
at r and another selected neighbour at r+2, contradicting feasibility.
Thus at least one forest is positive. Its gap faces the owner's P column c,
so the positive interval is in A's original whole support. QED.

If x itself is a board boundary, the forest cannot extend outward and is
already positive; no fictitious outside column is used. If outward P or BT
blocks a forest before the boundary, it also cannot be balanced. The proof
therefore allows occupied neighbouring bands and arbitrary other components.

**Run corollary.** If an owner has this exposed BB/P boundary on ell consecutive
bands at fixed c,epsilon, it supports at least floor(ell/2) different positive
original units. Pair bands 0/1,2/3,... and apply the lemma. The pairs use
disjoint band indices, and an original interval lies in exactly one band.

More generally choose any collection of such pairs along an owner's possibly
bent body, allowing c and epsilon to vary, provided their band-index sets are
pairwise disjoint within that owner. If there are g_A pairs they certify
g_A different original units. Arbitrary overlapping pair collections must
not be summed: the same unit could otherwise be counted twice for one owner.

This is an existence statement in the actual final configuration. If T changes,
forests can merge or split; the conclusion does not preserve a designated
interval identity from before that change. Withdrawals below keep T fixed.

## 2. Unified counting and allocation without duplicated slack

Let the original alpha set have size k, original beta count be beta, and the
complete original interval pool have size L. For each alpha A choose g_A
band-disjoint adjacent-band witnesses as above; zero witnesses are allowed.
Then

    sum_A g_A <= 2L,
    S = area/2-|T|-|M| >= beta + ceil((sum_A g_A-2k)/2).   (1)

Proof. Choose one positive unit from each witness pair. Within one owner the
chosen units are different. A physical interval can belong to at most two
different original open owners: its maximal no-P gap has at most one owner
at each of its two P-column boundaries. Therefore every chosen original unit
has at most two different alpha incidences, giving the first inequality.
The original exact ledger is S=L+beta-k. Substitute L>=ceil(sum g_A/2)
to obtain the second inequality. No selected mediator or TT pair is itself
an additional credit. QED.

In particular

    sum_A g_A + 2 beta >= 2k-1                           (2)

suffices for |T|+|M|<=area/2. The one parity rounding is global. This numerical
criterion permits some alphas to have no witness and does not claim that
those particular alphas can reach other owners' spare units.

**Full-payment corollary.** If every alpha has g_A>=2, all k alphas have
simultaneous zero-link payments by different original units, with no boundary
condition and no beta spent. For any source subset U there are at least
2|U| distinct source/unit incidences and at most two incidences per unit,
so its resource neighbourhood has at least |U| vertices. The ordinary finite
matching theorem gives the injection. Equivalently, use the constructive
cycle-or-singleton allocation of ONE_SIDED_INTERVAL_AND_BETA_ALLOCATION.md;
a deficient tree cannot have every demand degree at least two. Either proof
uses one capacity for each actual original interval. This corollary improves
the 5/6 coefficient to one on the stated geometric class, not universally.

For a uniform g>=2, the unused interval ledger is stronger:

    S >= beta + ceil((g-2)k/2).                          (3)

In particular g=4 gives S>=beta+k. These credits are counted in L, not added
to the terminal ledger a second time.

## 3. Joint withdrawals and private reserves

Fix T,M and its interval identities. Reserve an arbitrary set R of r different
original units. If every alpha has at least g>=2 certified distinct units,
the maximum direct whole-support allocation leaves D alphas unpaid with

    gD <= 2r.                                           (4)

Also D=0 whenever r<=g-2, since each alpha retains at least two units. These
are upper bounds for the deficit of the full stem/fork network; relays and
beta paths can only improve the direct certificate.

Proof of (4). Take a maximum bipartite allocation and follow alternating
paths from its D unmatched sources. If D>0, the reached source set U has
only matched resource neighbours, and exactly |U|-D available neighbours;
otherwise the matching augments. Before withdrawal, its certified incidences
number at least g|U|. Available neighbours contribute at most 2(|U|-D)
incidences, and withdrawn units at most 2r. Hence

    g|U| <= 2(|U|-D+r).

As |U|>=D and g>=2 this implies gD<=2r. The same physical withdrawn unit is
counted at most twice as an incidence, never once per route or terminal. QED.

If instead each alpha has g private certified units supported by **no other
open owner**, the private unit sets of different alphas are disjoint. A
source remains payable unless all its g chosen units are reserved, giving

    D <= floor(r/g).                                    (5)

This last statement is a guaranteed certificate, not an exact full-network
deficit formula. The general exact arbitrary-withdrawal formula for the
smaller terminal-port graph remains in the preceding note.

## 4. A fully frozen boundary obstruction with every terminal port zero

Start with chain(1) from rotor_networks.py, transpose its 30-by-30 board, and
retain its 144 endpoints, 72 actual matching edges and 40 selections. This is
the existing width-14 four-arm rotor star, with occupied degree three and a
unique matching; its complete freezing proof is in
BRANCHED_ROTOR_NETWORKS_AND_UNBOUNDED_RECEIVER_CHARGE.md. Add exactly

    {0,1,14,15} x {0,2,4,6},
    {14,15,28,29} x {23,25,27,29}.                       (6)

The two products are disjoint and contain 32 new selections, arranged in
vertical TT pairs. In rows 0,...,15 the old left exterior columns 0,...,7
are blank. The only old occupied left-exterior site on the lower halo row 16
is (16,1); its column is odd, whereas all new left selections use even
columns, so it is adjacent to none. In rows 14,...,29 the old right exterior
columns 22,...,29 are blank. Its upper halo row 13 has only (13,28) there;
that even column is different from every new odd selection column. The
other exterior halos are outside the board or inside these blank rectangles.
Thus every new selection sees only its TT partner. No old selection or
endpoint gains a neighbour, so all old occupied degrees and freezing witnesses
remain unchanged. These are fixed coordinate facts, also checked by the
independent fixture verifier. This proves feasibility and full freezing,
without inferring them from a sample-size trend.

The original alpha bodies are the straight P columns

    A: {(r,8):1<=r<=14},       tips (1,8),(14,8);
    B: {(r,21):15<=r<=28},     tips (15,21),(28,21).       (7)

For A, both ports now enter the balanced word
TT0,BB1,TT2,BB3,TT4,BB5,TT6,BB7, at bands 0 and 7. For B, at bands 7 and 14,
the balanced word is BB22,TT23,BB24,TT25,BB26,TT27,BB28,TT29. Thus the port graph
has two isolated alpha edges, each with two zero ends:

    k=2, beta=0, d4=0, b=4, V_port=0, D_port=2;
    |T|=72, |M|=72, L=308, S=306;
    full whole-support value=2, minimum links=0.          (8)

All endpoint occupied degrees are three. The fixture's 36 strict freezing
layers are independently checked against physical retained neighbours.
This refutes “freezing excludes boundary double-zero paths”, not full-pool
compensation or the numerical inequality.

For arbitrary q>=1 put copies at row offsets 32i,0<=i<q, on the
(32q-2)-by-30 board. Two blank rows separate successive copies, so no old or
new occupied sites interact. M and N never join copies. The inventories are

    P=144q, M=72q, T=72q, k=2q, beta=0,
    b=4q, D_port=2q, V_port=0,
    L=338q-30, S=336q-30;
    full value=2q, minimum links=0.                      (9)

Each copy contributes its 308 old units and each separating blank band adds
30. Counts and freezing therefore follow by an arbitrary-q disjoint union,
not enumeration extrapolation. A single auxiliary global direction change
or an assertion that boundary defects are bounded is unnecessary here.

## 5. Repair survives every degree-three selection extension of this family

Retain P,M and every selection of the transposed unfilled star copies; permit
any further selections for which feasibility holds and all endpoint occupied
degrees remain three. This includes (6), but does not prescribe those TT
pairs or impose a new boundary convention. No new P is allowed in this
corollary. New selections cannot touch P, since those degrees were already
three. Thus all original alpha/beta/mixed types and bodies remain unchanged.
The old freezing certificate replays.

For each upper alpha A, column 7 stays blank on rows 0,...,15. Its endpoints'
selected N-partners force the two outer blanks; all other blanks either
neighbour degree-three P or a retained selection already seeing P. The
adjacent alpha column 8 touches the eight bands r=0,2,...,14. For B, column
22 stays blank on rows 14,...,29, and its P column 21 touches r=14,16,...,28.
These statements follow immediately from (7) and the displayed retained
supports of the two-leg arms. Transport them by the copy offsets.

Pair these eight bands consecutively. The adjacent-band lemma gives FOUR
different original intervals in every alpha's whole support in every such
extension. With fixed P, its exterior no-P gap reaches the board edge and
has only that alpha as a boundary open owner. These four units are therefore
private among all open owners. Gaps on the left/right or in separate copies
give different private identities, even at the one band shared by A and B.

Consequently every selection extension in this entire class has all 2q
alphas paid at zero links in its complete original pool. After any r original
units of that final configuration are reserved, full-network deficit is at
most floor(r/4) by (5). Forest identities may depend on the added selections;
this is not a claim that four particular old singletons remain unchanged.
The private sets also give L>=4k, so the actual numerical margin satisfies
S>=beta+3k=6q throughout this completion class, rather than merely S>=0.
No claim about arbitrary P additions, arbitrary reselection of the old
supports, or all frozen geometries is implicit in this completion theorem.

## 6. Mixed directions, including actual matching edges crossing regions

The reserve lemma and all bounds (1)--(5) also hold for any partition of the
board into disjoint even-by-even rectangles, each using its own horizontal or
vertical bands. The auxiliary matchings combine into one perfect matching N.
Restore **every actual M edge**, including edges crossing region boundaries,
before identifying the original global alpha, beta and other open owners.
Use precisely the complete regional BB/TT unit convention of
[the crossing-matching ledger](CROSSING_MATCHING_PORT_LEDGER.md). A unit's
identity includes its region and band; its physical cells lie in that region.

Each witness pair lies in one region, in two consecutive parallel local bands,
at the same local P-column and side. Both P columns must meet the same GLOBAL
alpha body. Different pairs for that owner may lie in different regions and
have different directions. Their (region,band) sets must be disjoint within
that owner. Both pairs are wholly inside their own region. At an artificial
lateral region boundary a balanced forest still has an immediately outward
TT inside that region; physical feasibility rules out two such TT columns in
adjacent local bands by the same argument as Section 1, rotated if necessary.
Neighbours outside the region cannot remove this contradiction.

These hypotheses imply distinct chosen units within each owner. Every unit
still lies in one no-P gap with at most two P-column boundary owners; a PP
column belongs to a single global owner because N joins its P vertices.
Consequently its incidence with different global alpha owners is at most two.
The proof of the full-payment corollary therefore applies to all global
alphas simultaneously, including newly restored interface alphas. The direct
payments use no terminal links or beta gates. Bounds (4)--(5) likewise hold
for withdrawals of distinct actual regional units from this fixed model.

For completeness, retain the seam correction explicitly. In the notation of
the crossing-matching note let A0,B0 be closed local alpha/beta counts,
b,c the BC/CC half-path counts, e the number of crossing actual M edges,
and aI,bI the alpha/beta counts created on restoring the ports. Then

    S=L+B0-A0+b+c-e,
    b+c-e=bI-aI,
    alpha_global=A0+aI, beta_global=B0+bI.

Thus S=L+beta_global-alpha_global exactly, and (1)--(3) use these GLOBAL
counts and the global witness total G. In particular

    G+2(B0+bI) >= 2(A0+aI)-1

implies S>=0. Half-paths are not spare units, the e matching debit is retained,
and no local beta or interface path is credited a second time. We choose a
joint direct allocation freely; the theorem does not also preserve an arbitrary
previously locked local pack. If such a pack is retained, remove its actual
spent units first and apply the withdrawal bound to the still-unpaid alpha
subset with that explicit set R and its certified reserves.
This proves the mixed-direction extension without assuming matching-closed
regions or summing local optima.

## 7. Validation and remaining problem

The permanent fixture is
develop/fixtures/degree_three_double_boundary_zero_paths.json. The checker
develop/check_adjacent_band_boundary_repair.py independently verifies physical
feasibility, all degrees, stored strict ranks, original resource identities,
zero-port deficits and whole-support payments. It also extracts witnesses
from bent/branched families, checks global incidence counts and tests joint
withdrawals against independent resource matching and whole-fork bounds.
The arbitrary-size proofs are Sections 1--6; finite controls test them.

The saved Python receipt passes 215 physical models, 737 alpha occurrences,
2,643 selected band-disjoint witness pairs, 1,350 geometric joint-withdrawal
bounds, 324 private-reserve withdrawal bounds and 36,476 abstract withdrawals.
There are 30 degree-three selection-extension controls, 36 private-four-reserve
models, 150 nonempty full-payment controls and 28 positive port-deficit models.
Stored and copied strict-rank certificates check 144 and 4,176 endpoint events,
respectively; this does not label all 215 models frozen. Three explicit
degree-two controls test that the local theorem needs no degree-three premise.

Of the physical models, 48 have genuinely mixed regional directions. They
contain 136 crossing actual matching-edge occurrences and 52 global interface
alpha occurrences; 32 of those alphas have at least two certified pairs.
In 24 partitions with interface alphas, EVERY global alpha has at least two
pairs and is paid at zero links. The 20 two-region models independently agree
with the existing crossing-port compiler on global owner counts and the exact
ledger. Resource matching is compared with 1,567 exhaustive small guard
allocations and 770 whole-fork lower bounds across the test suite.

Local Lean 4.33.0 passes 17 declaration/public-axiom audits with no warnings,
placeholders, native evaluation or new axioms. It checks the local TT-neighbour
exclusion, disjoint band choices, arbitrary
finite incidence and ledger arithmetic, alternating-set withdrawal inequality
and private-reserve tax, including the restored-interface ledger arithmetic.
The arbitrary grid adapter, general matching theorem,
coordinate construction and completion coverage remain written proofs, not an
end-to-end Lean certification. Executed scope is recorded in the saved receipts.

Reproduce from the repository root:

    python3 develop/check_adjacent_band_boundary_repair.py --output output/adjacent-band-boundary-repair-validation.json
    python3 develop/check_adjacent_band_boundary_repair_formal.py --lean /path/to/lean-4.33.0 --output output/adjacent-band-boundary-repair-formal-validation.json

Permanent sources and receipts:
[physical checker](../develop/check_adjacent_band_boundary_repair.py),
[explicit frozen fixture](../develop/fixtures/degree_three_double_boundary_zero_paths.json),
[Lean source](../formal/SubQuorum/AdjacentBandBoundaryRepair.lean),
[physical receipt](../output/adjacent-band-boundary-repair-validation.json),
[Lean scope and receipt](../output/adjacent-band-boundary-repair-formal-validation.json).

The next unresolved cases are alpha owners without enough exposed-band pairs,
especially short bent paths and occupied neighbours which obstruct the BB
column itself. Degree-four terminal obstructions also remain. The old
pinwheel joint flow still handles arbitrary restricted pools; no beta credit
or root crossing has been charged in the present direct-resource proofs.
Submitted manuscripts, public main, PR3 and correspondence are unchanged.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
