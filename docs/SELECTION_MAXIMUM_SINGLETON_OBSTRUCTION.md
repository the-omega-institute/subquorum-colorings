# Selection saturation preserves the frozen obstruction and destroys its last payment

25 October 2026. Haobo Ma and Wenlin Zhang. Independent research branch.

Follow-up: [unique actual matching and arbitrary adjacent modules](FORCED_MATES_AND_ADJACENT_MAXIMA.md) removes matching freedom on this P family and proves an exact additive all-module maximum.

The [complete-pool singleton obstruction](FULL_POOL_SINGLETON_OBSTRUCTION.md)
is not explained merely by a failure to make the selected set inclusion
maximal. On a cropped board, **every** feasible selected-only extension has
the same two alpha strands, no beta, and at most one possible payment.
Every inclusion-maximal extension, and hence every maximum-cardinality
extension containing the original selections with the endpoint set fixed,
has **zero** possible payments. Complete freezing persists.

There is also a positive result on this entire extension class: its numerical
margin is at least four. More strongly, allowing ALL choices of T with the same fixed P, we prove
max|T|=8W+8 and give an attaining, fully frozen zero-payment construction
for every even W>=8. It has numerical margin exactly four. The W8 maximum
is72, while the narrower extension maximum retaining all original T0 is71.
Both upper bounds have elementary disjoint-cover proofs; optimization was
used only for discovery.

There are two distinct optimization domains: Sections1–7 retain T0 and P;
Section8 permits arbitrary T with P fixed. Neither domain changes P, so
neither is the global Omega problem over all choices of T and P. The band
phase and actual matching remain fixed.
No universal5/6 improvement or target counterexample is claimed.

## 1. Board and selection-extension class

Fix even W>=8. Take the seven-addition raw-pool family of the preceding note,
remove its four empty top rows and six empty bottom rows, and subtract four
from all occupied row coordinates. The resulting board has

    height W+2, width22, |T0|=41, |M|=3W+10, |P|=6W+20.       (1)

All old selections and endpoints were in the retained rows. Thus feasibility
and the full freezing certificate remain valid at the new board boundary.
The bands are rows(0,1),(2,3),...,(W,W+1). The alpha tips are now
(1,5),(W,5) and (1,15),(W,15). There are14 mixed owners, no beta owners and
2W-4 pure cycles.

Consider every U such that T0 is a subset of U, U avoids P, and(U,M) is
feasible: each selected vertex has at most one occupied neighbour in U union P.
Neither the matching nor endpoints change. This is an arbitrary simultaneous
selected-only extension, with no bound on the number of additions.

Write C for the individually selectable baseline sites:

    C={v outside(T0 union P): (T0 union{v},M) is feasible}.

If U is feasible, then U minus T0 is a subset of C. Indeed removing the other
new selections only removes occupied neighbours; the feasibility of every
remaining selected vertex persists. It is not asserted that arbitrary subsets
of C are jointly feasible. C is a necessary candidate hull, not a selection
rule.

## 2. Original terminal types, links and freezing never change

The only original BP tips are in columns4,6,8,14,16,18 of the two terminal
bands, and at(W-1,7),(W-1,17) in the penultimate band. To promote a BP into TP
one would have to select its blank band partner. None of these partners is
in C:

* In rows0 and W+1, a terminal BP partner in any listed even column has two
  already selected horizontal neighbours, in the adjacent odd columns.
* The partner(W-2,7) has occupied neighbours(W-1,7),(W-2,6),(W-2,8), the last
  being an original selection; the column17 version is its translate by10.

The two-neighbour obstruction already suffices. Existing TP partners remain
selected and every PP column remains PP. Therefore **all** original terminal
types, original open-strand pairs, pure cycles, and candidate TP--BP links
are identical for every feasible U. In particular alpha=2,beta=0,mixed=14.
An added selection can shrink resources but cannot create a new BP/TP route.

Freezing is monotone under increasing selections while preserving P and its
mates. Replay each old strict-rank witness: an old selected witness remains
selected, and every endpoint witness's mate retains its earlier rank. This
proves complete freezing for every feasible U; no search over extensions is
needed. `frozen_extend_selection` formalizes this induction.

## 3. The one universally addable site

Let

    x=(W+1,11),    j=(W/2,11,11).                          (2)

The identity j records(band,first column,last column). Before adding x, it
is the lower shared BB singleton, with physical cells(W,11),(W+1,11).

The top band is fully blocked against new selections. In the bottom band,
the only individually selectable site is x. This follows directly from
the terminal rows:

    row0:   T at every odd column1,3,...,21;
    row1:   T at0,2,10,12,20, plus original endpoint columns;
    rowW:   T at0,2,10,12,20, plus original endpoint columns;
    rowW+1: T at odd columns1,3,5,7,9,13,15,17,19,21.

Every other blank there either has two occupied neighbours, or touches an
old selected vertex whose occupied-neighbour allowance is already used.
This also verifies the claimed terminal-band part of the candidate hull
without assuming anything about choices made in the middle of the board.

The site x has no old occupied neighbour. It has just three board neighbours:
(W,11),(W+1,10),(W+1,12). None is in C. The first lies between the already
saturated selections(W,10),(W,12); the latter two each see both an upper
selection and a neighbouring lower odd-column selection. Thus no feasible
U contains any neighbour of x. Adding x to **any** such U remains feasible:
x is isolated, and no previous selected vertex acquires a neighbour.

Consequently every inclusion-maximal U contains x. A maximum-cardinality U
exists because the board is finite, and is inclusion maximal, so it also
contains x. This conclusion concerns the entire feasible extension class,
not only greedy examples or one optimizer's output.

The crop is essential to this statement. On the previous enclosing board,
a new selection below x could interact with it. Here x is on the board's
bottom boundary; no outside neighbour is silently discarded in an ambient
extension claim.

## 4. Complete resource accounting, including TT boundary chains

Selected-only extensions can create TT columns, including physical boundary
TT columns. The old no-TT compiler cannot be reused without modification.
We use a separate whole-board even-width adapter and retain the old assertions.

In any feasible two-row band, a TT column has BB columns on both horizontal
sides that exist. Each T already sees its vertical T companion; another
horizontal occupied neighbour would violate feasibility. Build the BB/TT
forest by joining consecutive BB/TT columns whenever one is TT. Consecutive
BBs alone are not joined. Each connected component is an alternating path:

* BB at both ends gives one more BB than TT, hence **one** original unit.
* TT at one physical board end and BB at the other gives equal counts,
  hence **zero** units. This is a balanced boundary chain.
* TT at both ends would have to reach both physical band boundaries and
  have odd length. The band width is22, so this case cannot occur.

The statement holds for every even width, not for arbitrary odd widths.
There are no negative components in the stated adapter. Do not count a
balanced boundary chain as a positive resource or treat each of its BBs as
an independent unit. Each positive path retains its original coordinate
identity(band,first,last); all such units are available, without reservations.

Every forest component lies within one maximal no-P gap. A gap's number of
positive units equals its number of columns minus its number of selected
vertices. Balanced paths contribute zero, so they neither add fake credit
nor create a missing debt. The original endpoint/strand ledger therefore
continues to give

    S=area/2-|U|-|M|=L+beta-alpha=L-2,                      (3)

where L is the total number of positive original interval components for U.
All remote units remain in this ledger even when unreachable.

## 5. Exact compensation for every selected-only extension

The complete directed mixed closure from the two alphas is the same as in
the previous note. In each terminal row r in{1,W}, it has precisely the
non-self chains

    A_L -> mixed(3,4);
    A_L -> mixed(6,7) -> mixed(8,9);
    A_R -> mixed(13,14);
    A_R -> mixed(16,17) -> mixed(18,19).                   (4)

The internal PP body columns are shielded by P columns. The other two mixed
owners in the penultimate band are unreachable and have only self-links.
All no-P gaps incident to a reachable original owner are in the two terminal
bands. Their intersection with C is exactly{x}, as Section3 proves.

Thus none of these gaps changes except j: it remains BB if x is absent,
and becomes BT, with zero capacity, if x is present. No TT complication
occurs in a reachable gap. All resource changes elsewhere are behind the
same unchanged directed closure. Taking the union of the complete supports
of every reachable owner gives exactly{j} or the empty set, respectively.

For any terminal matching, the no-beta cancellation argument in the preceding
note applies: each alpha component consists of two outward mixed arms, and
cannot merge with another alpha. Every interval payment needs a resource
from the displayed reachable support. Therefore, for the complete raw pool,

    V(U)=1 if x is absent, and0 if x is present;
    deficit(U)=1 if x is absent, and2 if x is present.       (5)

The first case is attained by the right lower one-link route; it has minimum
cost1. The second needs no links to attain value0. In particular **every
inclusion-maximal and every maximum-cardinality U in this fixed-P extension
class has two unpaid demands and zero compensation value**. Neither the
availability of all raw resources nor selection saturation repairs the flow.

This does not strengthen the previous local-full/global-deficient assertion
by retaining local fullness: after x is added, each local value is itself0.
The two results exclude different candidate fixes.

## 6. A positive bound for the entire extension class

We can bound the numerical margin uniformly without requiring full flow.
Partition the board into aligned2-by2 tiles. Any feasible selected set has
at most two vertices in a2-by2 square: any three contain a vertex adjacent
to the other two. For additions in a tile, use this bound and the necessary
candidate hull C. A tile with only one possible candidate has cap1. In the
interior at columns6,7 or16,17, the two possible blank-column candidates
both face P; selecting both would give each two occupied neighbours, so
these tiles also have cap1.

The complete upper table for the number of **new** selections, indexed by
tile column0..10, is:

    top band:
    0 0 0 0 0 0 0 0 0 0 0
    second band(rows2,3):
    2 0 0 0 1 2 0 0 0 1 2
    each remaining interior band(rows4,5 through W-4,W-3):
    2 2 0 1 2 2 2 0 1 2 2
    penultimate band(rowsW-2,W-1):
    2 0 0 0 0 2 0 0 0 0 2
    bottom band:
    0 0 0 0 0 1 0 0 0 0 0.

There are W/2-3 interior bands. Zero entries are excluded by P or the fixed
selection neighbourhoods; the only cap1 entries were explained above.
Every cap2 follows from the2-by2 bound, so no finite enumeration is needed
to establish the table or its applicability to simultaneous additions.
The tiles are disjoint and cover the board, hence

    |U minus T0| <=8+16*(W/2-3)+6+1=8W-33;
    |U| <=8W+8;
    S=11(W+2)-|U|-(3W+10) >=4.                           (6)

Combining(3),(5),(6), every selection-maximal extension has L>=6 unused
original units and exactly two unpaid demands. Their difference L-2 is at
least four. This is a genuine slack-versus-deficit conclusion on an entire
unbounded family, proved using disjoint physical regions. It does not
assign the same spare unit to two demands, and does not insist that those
spare units be reachable by the failed compensation flow.

## 7. Explicit W8 maximum:71 selections, zero payment, margin five

For W8 the table's upper bound on additions is31. Improve it by one using
a shifted cover of rows4,5 and columns8..13. In this region the only
individually selectable points are

    (4,8), and rows4,5 at columns9,10,11,12.

Thus these three original tiles, with caps2+2+2=6, can instead be covered by
one singleton and two disjoint2-by2 squares on columns9,10 and11,12. Their
total cap is1+2+2=5. The other three cells are individually forbidden. This
replaces, rather than adds to, the old tile cover, so nothing is counted twice.
Every feasible extension therefore has at most30 additions, hence at most71
selections.

An attaining set of30 additions, listed by row, is

    row2: 0,11,21
    row3: 1,9,10,19,20
    row4: 0,2,8,11,12,18,21
    row5: 0,2,7,9,10,17,19,20
    row6: 1,11,21
    row7: 0,11,21
    row9: 11.

It is feasible by direct coordinate checks. Along each listed row, any
adjacent selected pair has no other occupied neighbour; isolated additions
have at most one old or new occupied neighbour. The old selected vertices
retain the required allowance. The permanent fixture and Lean geometry
statement independently check all these contacts and every original matching
edge. It contains x=(9,11). Therefore

    max_fixed_P |U|=71, |M|=34, |P|=68;
    L=7, V=0, deficit=2, S=110-71-34=5.                  (7)

The written cover gives the upper bound, and the displayed feasible set gives
the lower bound. Finite branch search over candidate components is not the
proof of maximum. The original T0 remains included. No claim is made that71
is maximum if the original selections can be removed or the endpoints changed.

## 8. Exact maximum over all selections with fixed P

We can remove the retention requirement from the optimization itself. Let
T be ANY feasible selected set with the original P, without requiring T0
as a subset. Then

    |T|<=8W+8.                                              (8)

This is sharp for every even W>=8, with a completely frozen attaining
configuration of zero compensation value and numerical margin exactly four.

First discard every possible selection site with two or more P neighbours.
Use the aligned2-by2 cover as before. The complete P-only cap table is

    top and bottom bands:
    2 2 1 1 1 2 2 1 1 1 2
    each band rows2,3 through W-4,W-3:
    2 2 0 1 2 2 2 0 1 2 2
    penultimate band:
    2 2 0 0 1 2 2 0 0 1 2.

The first two row types total16, and the last totals12, giving8W+12.
Cap2 is the ordinary square bound; cap1 is a single remaining candidate or
two adjacent possible selections already facing P, which cannot both be
selected; cap0 has no allowable vertex. These arguments use P alone.

Now replace the cover of four disjoint4-by2 patches, with top-left
coordinates

    (0,2), (0,12), (W-2,2), (W-2,12).

Each patch previously used two tiles of total cap4. In a patch starting at
(r,c), the only P-allowable sites are

    (r,c),(r,c+1), (r+1,c), (r+2,c), (r+3,c),(r+3,c+1).

Partition them into the three adjacent pairs

    {(r,c),(r,c+1)}, {(r+1,c),(r+2,c)},
    {(r+3,c),(r+3,c+1)}.

In each pair at least one endpoint already has a neighbouring P, so selecting
both would violate the one-neighbour condition. Each pair contributes at
most one, giving cap3. The four patches are disjoint for W>=8 and replace
eight distinct old tiles. Hence the bound improves by four to8W+8, proving(8)
without transfer-matrix optimality or finite enumeration.

An attaining T* is the following explicit row pattern:

    row0:   odd columns1,3,...,21                         (11)
    row1:   0,2,10,12,20                                  (5)
    row2:   0,8,11,18,21                                  (5)
    row3:   1,3,7,9,11,13,17,19,21                        (9)
    each interior upper row r=4,6,...,W-4:
            0,2,8,10,12,18,20                             (7)
    its lower row r+1, except the last interior band:
            1,3,7,9,11,13,17,19,21                        (9)
    last interior lower row W-3:
            0,2,7,9,11,13,17,19,21                        (9)
    rowW-2: 1,3,8,10,12,18,20                             (7)
    rowW-1: 0,11,21                                       (3)
    rowW:   0,2,10,12,20                                  (5)
    rowW+1: odd columns1,3,...,21                         (11).

The top, bottom and penultimate interfaces have fixed size and are checked
directly. In each repeated interior strip, the selected pattern is a
checkerboard on the free columns; no new vertical or horizontal T adjacency
occurs. In its last band the two pairs in columns0 and2 are vertical pairs,
with no selected neighbour above or below; the adjacent penultimate row uses
columns1 and3. Every remaining selected vertex has at most one P neighbour.
These observations check arbitrary repetition and both interfaces, proving
feasibility for all W. The count is

    |T*|=56+16*(W/2-3)=8W+8.

This differs from the original T0 by added selections and removal of just
one old selection y=(W-2,13). Even T0 minus{y} is fully frozen. Here is a
uniform modification of the earlier relay/seal freezing certificate, using
the preceding note's uncropped coordinates temporarily. The removed point
is y=(W+2,13). Freeze the four outer relay TP tips first and replay both old
direct-core certificates. Their replaced caps are retained because the outer
TP mates have already frozen. All upper relay pairs and the lower left pair
freeze as before. On the lower right freeze q=(W+3,14), using its side alpha
neighbour and the retained BP below. Postpone p=(W+2,14) and BP(R,14).

Now freeze both PP seals by the previous upper even-row and reversed lower
odd-row inductions. The upper boundary is unchanged; the lower right boundary
p is retained because its mate q has already frozen, although p itself is
not yet frozen. Finally freeze p using the side alpha and(W+1,14), whose
mate(W,14) is now frozen; then freeze BP(R,14) using its original alpha
neighbour and q, whose mate p has just frozen. This covers every endpoint.
The solver-free `reduced_serial_certificate` implements exactly this uniform
schedule and checks the strict witnesses, independently of peeling output.
Adding the remaining selections to reach T* preserves freezing.

The removed y is not a band partner of a P tip, and none of the new T* points
promotes an original BP. Thus the original2 alpha/0 beta/14 mixed inventory
and all links are unchanged. Its terminal bands have the same zero-capacity
outer and upper middle gaps, while x is now selected and kills the lower
middle singleton. The same closed-reachability argument gives

    L=6, V(T*)=0, deficit=2;
    S=11(W+2)-(8W+8)-(3W+10)=4.                          (9)

This is a true maximum over all T with the fixed P, rather than only an
inclusion-maximal set or an optimizer retaining the original selections.
It still does not maximize over changes in P. The [W8 permanent fixture](../develop/fixtures/fixed_P_selection_maximum_zero_payment.json)
has72 selections,34 matching edges and all68 endpoints frozen; all six raw
interval units are unreachable from the two sources.

## 9. Consequences and remaining scope

The previous complete-pool obstruction had a sparse selected set. The new
argument shows that making it inclusion maximal, or optimizing cardinality
within the fixed-P extension class, does not force full compensation; it
can destroy the final payment. Consequently a proof that relies on an
extremal configuration must specify its exact optimization domain. Merely
adding a fixed-P selection-maximality hypothesis will not suffice.

The family nevertheless satisfies the desired coefficient-one numerical
inequality throughout the extension class, with a strict constant margin.
This supports a route allowing unpaid demand and paying it from a disjoint
physical slack budget. It does not prove the general geometric budget.
The all-T fixed-P optimum in Section8 also has zero compensation, so simply
removing the retention condition does not force the optimum to be fully
payable. Changes in P/M or another band phase remain possible mechanisms
outside this theorem. An exploratory check of
the earlier enclosing family in the other horizontal row phase has no alpha
strands; that observation is not promoted here to a universal phase theorem.
The submitted11 October manuscript remains unchanged.

## 10. Reproduction and formal scope

    python3 develop/check_selection_maximum_singleton.py --output output/selection-maximum-singleton-validation.json
    python3 develop/check_selection_maximum_formal.py --lean /path/to/lean-4.33.0 --output output/selection-maximum-singleton-formal-validation.json

The solver-free checker verifies696 feasible extension boards, including429
single-site controls and152 inclusion-maximal extensions, over19 heights
W=8,10,...,40,64,128. Small heights W<=12 check every individually selectable
site; larger heights check12 seeded sites each. It checks the complete
candidate hull's BP exclusion, universal addability of x, reachable-gap
intersection, full upper table, strand/link invariance, strict freezing ranks,
exact raw ledger, and full flow. It also checks19 all-T fixed-P exact maxima against the
P-only table and four forbidden-pair patch certificates, and19 uniform
reduced-selection serial freezing certificates. It independently reconstructs balanced
boundary TT chains on219 boards. A207-case complete small even-board census with P empty
checks the forest adapter;19 no-TT comparisons agree with the prior compiler.

The [permanent W8 fixture](../develop/fixtures/selection_maximum_singleton_obstruction.json)
contains71 actual selections,34 matching edges, all30 additions and a strict
freezing certificate. The W8 cover is separately checked using the actual
necessary candidate set and displaced tiles.

The [Lean source](../formal/SubQuorum/SelectionMaximumSingleton.lean) has17
new audited declarations, six axiom-free, the rest standard-only, plus16
dependency audits. It proves isolated-selection addability, candidate-hull
isolation, maximality under universally compatible additions, monotone
freezing under selection extension, scalar all-W and W8 bounds, concrete
W8 feasible72T geometry and all68 frozen endpoints, and the empty
reachable-support certificate. The full coordinate hull/table proof,
four-patch cover-to-count specialization, BB/TT boundary adapter and no-beta
cancellation adapter remain written proofs with independent checks. This is
not an end-to-end formalization of the selection optimum or the general
Omega inequality. Local memory and actual comm-basename Lean/Lake processes
were checked before sequential compilation; unrelated jobs were preserved.

No new Oracle review, email read, draft edit or email transmission is part
of this increment. Public main, PR3 and shared CI are preserved.
