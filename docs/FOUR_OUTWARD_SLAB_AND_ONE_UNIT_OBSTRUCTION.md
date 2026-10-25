# Arbitrarily many four-outward capacity-two tiles with one unit of charge

26 October 2026. Wenlin Zhang and Haobo Ma. Isolated research branch.

This resolves the specific open extension in Section 5 of
[single-square parity and alignment](SINGLE_SQUARE_PARITY_AND_ALIGNMENT.md):
keeping alignment, four outward actual mates, single terminality and even
complete freezing does **not** preserve the two-unit compensation theorem
when uniqueness of the endpoint square is removed. The obstruction has a
general construction and proof. It is not a counterexample to the numerical
grid target; its objective is exactly one below half the area.

## 1. Statement and conventions

Use a feasible pair (T,M): M is a grid matching, P=V(M), T is disjoint
from P, and every T vertex has at most one neighbor in T union P.
Tiles are the original disjoint squares with even first row and column.
On a deficient tile the corrected physical charge is

    2 rho = t-b+s,

where s counts actual matching attachments to saturated tiles. Saturated
tiles have charge zero. Residual capacity is r=2-t-h_internal-s.
The negative capacity of a tile is max(0,-rho); these capacities refer to
physical tile identities and are not cloned when several squares use them.

**Theorem.** For every integer h>=1 there is a feasible pair on the
(2h+4)-by-8 rectangle such that:

1. P is one connected component; every endpoint has occupied degree at
   least three, and every endpoint is excluded from every feasible
   simultaneous oriented promotion bundle.
2. There are exactly 2h aligned all-P tiles with all four actual mates
   outside their respective tiles. Each has t=h_internal=s=0,r=2,d=4
   and corrected charge zero.
3. Exactly two tiles have negative charge, each -1/2. Every other tile
   has charge zero. Thus the **entire board** supplies just one unit of
   negative physical charge, and the whole endpoint receiver has charge -1.
4. In the original horizontal two-row PP/M decomposition there is exactly
   one alpha path and one alternating cycle, no beta and no mixed owner.
   Each of the 2h capacity-two tiles has one PP column on that same alpha
   and one on that same cycle. The full original resource pool has two
   distinct units, both supported by the alpha; maximum payment is one at
   zero links.

Consequently even ONE such four-outward tile need not admit two units of
negative physical charge anywhere in its board. Counting two units for
every such tile would request 4h units from an actual one-unit budget.

## 2. Explicit construction

Rows and columns are zero-based. Put R=2h+4. Select, in every row r,

    columns 1,6 if r is even; columns 0,7 if r is odd,

and also select the two points (2h+3,2),(2h+3,5). Define the actual
matching by these disjoint groups:

    (0,2)--(0,3), (0,4)--(0,5);
    (1,3)--(1,4), (2,3)--(2,4);
    (1,c)--(2,c)                         for c=2,5;
    (r,c)--(r+1,c)                       for odd r=3,5,...,2h-1,
                                            c=2,3,4,5;
    (2h+1,3)--(2h+1,4);
    (2h+1,c)--(2h+2,c)                   for c=2,5.

The odd-r range is empty for h=1. The endpoint set is exactly

    P=({0,...,2h+1} x {2,3,4,5}) union {(2h+2,2),(2h+2,5)}.

Every listed endpoint occurs in precisely one matching edge. The full
rectangle is completely specified; all unlisted sites are blank. The
smallest member, h=1, has these labels (dot means blank):

```text
.TPPPPT.
T.PPPP.T
.TPPPPT.
T.PPPP.T
.TP..PT.
T.T..T.T
```

The smallest member has T14, P18, M9, area48 and objective23. It is a
convenient independently checkable witness, not a claim of minimality
among all rectangles.

## 3. General feasibility and complete freezing proof

Even-row side selections at columns1,6 see precisely their adjacent
side endpoint, including the final even row. Odd-row side selections at
columns0,7 are isolated: their horizontal neighbor is blank and the
same-column sites in adjacent even rows are blank. The two extra selections
in the final row see precisely their matching-path tips immediately above.
They have no selected neighbor. This exhausts T and proves feasibility.
The full rectangle of endpoints is connected; both last tips attach to it.
Endpoints on its vertical sides have their two vertical P neighbors and
their inner P neighbor, except the upper corners, which have two P neighbors
and one side selection. The last full row has the same three-neighbor
count. The tips have their matching mate and two selected neighbors.
Interior vertices have degree four. Thus all endpoint degrees are >=3.

For freezing, fix any proposed simultaneous bundle. A selected vertex is
retained. If an endpoint z cannot be promoted, its actual mate is retained:
that mate could be removed only by promoting z on their matching edge.
Any endpoint with two distinct retained neighbors cannot be promoted.
Use this implication in the following ordered waves. Each two-column wave
uses both columns at the indicated row; it does not depend on the order
inside that wave.

1. Freeze side columns2,5 at even rows 2h+2,2h,...,2. The last tips
   have two T neighbors. Each preceding even side vertex uses its own
   selected side support and the next odd side vertex, retained as the
   mate of the already frozen even side vertex two rows below.
2. Freeze (0,2),(0,5), using their side selections and the retained
   row1 side vertices (mates of frozen row2 side vertices).
3. Freeze (1,3),(1,4), using the retained row0 middle vertices (mates
   of the preceding frozen corners) and the retained row1 side vertices.
4. Freeze (0,3),(0,4). Each sees the other retained row0 middle vertex
   and the retained vertex below (mate of the other frozen row1 middle).
5. Freeze (1,2),(1,5), using the retained row0 corners and row1 middles.
6. Freeze (2,3),(2,4), using the retained vertex immediately above and
   the retained side vertex in row2.
7. Freeze middle columns3,4 at odd rows3,5,...,2h-1, in increasing
   order. Each sees the retained middle vertex immediately above and
   its retained same-row side neighbor. For the first step, the above
   row2 middles retain one another; thereafter they are mates of the
   previously frozen odd middle row. Side vertices are retained from
   wave1. Then freeze the bottom middle row2h+1 by the same test.
8. Freeze middle columns3,4 at even rows2h,2h-2,...,4, in decreasing
   order. The opposite middle column is retained from wave7. The middle
   vertex below is retained from the previously frozen even row, or from
   the horizontally matched bottom middle pair for the first step.
9. Freeze side columns2,5 at odd rows3,5,...,2h+1, in increasing
   order. Each sees its retained middle neighbor and the retained side
   vertex immediately above. Wave5 supplies the first above vertex;
   each later above vertex is the mate of the preceding frozen odd side.

Empty ranges cause no problem when h=1. These waves cover every P vertex
exactly once. Every retained-mate dependency is strictly earlier; the
argument therefore excludes mixed-direction bundles too. It remains valid
in every feasible extension retaining these selections and actual edges.
This is a finite induction for arbitrary h, not an inference from tests.

## 4. Physical charge, counts and the repeated-owner obstruction

In tile bands b=0,...,h, the two central tiles (b,1),(b,2) are full P.
The side tiles (b,0),(b,3), including the final band b=h+1, have two
diagonal selections and no P. In the last band, tiles (h+1,1),(h+1,2)
each have one P, one T and two blanks. No endpoint lies in a saturated
tile, so s=0 everywhere and no boundary matching credit is being omitted.

For b=0 each full-P tile contains one actual horizontal matching edge;
its (h_internal,r,d) is (1,1,2). For b=1,...,h, no actual matching edge
is internal to either central tile: the even-row side edges go upward,
the middle horizontal edges in rows2 and2h+1 cross the central tile
boundary, and all other actual edges cross a horizontal tile boundary.
Hence these exactly 2h tiles have (h_internal,r,d)=(0,2,4).
All full-P tiles have charge d/2-r=0. Each last singleton tile has
(t,p,b,s)=(1,1,2,0), hence charge -1/2. Saturated side tiles are neutral.
This proves the asserted *gross* negative capacity, not just a net bound
after cancelling unidentified positive charges.

Direct counts are

    |P|=8h+10, |M|=4h+5, |T|=4h+10,
    |T|+|M|=8h+15, area/2=8h+16.

The receiver consists of the 2(h+1) full-P tiles and the two singleton
tiles. Its charge is -1, all other tiles are saturated, and the global
margin is exactly1. Thus any subset of physical tiles also has negative
capacity at most1. There is no possible choice of a more distant physical
donor that restores the missing second unit in this board.

The PP/M trace explains the repeated count. The alpha runs from the left
tip up column2, traverses the four middle vertices in rows0,1 through the
specified top matching, then descends column5 to the right tip. Its body
has 4h+10 vertices. The remaining vertices, columns3,4 in rows2,...,2h+1,
form ONE alternating cycle of length4h, joined horizontally at its top and
bottom and vertically elsewhere. These descriptions exhaust P and both
strand matchings. Each capacity-two tile contains one fixed column wire
from the alpha and one from the cycle. The many tiles do not provide new
owners, sources, or negative-charge budgets.

The original resource ledger is equally explicit. The side columns in
each horizontal band are BT/TB, with no BB/TT resource. All central columns
above the last band are PP. The last band has TP,BB,BB,TP at columns2..5:
its two separate BB singleton units are the complete pool and both are
adjacent through the same gap to the alpha. There are no BP terminals or
links. Thus alpha=1,beta=mixed=0, raw=2, maximum payment=1, link cost0.
One original unit pays the single alpha and one remains. This is consistent
with the exact one-unit global margin. Those two original units are not two
additional unused compensation units per full-P tile.

## 5. Consequence and remaining question

The unique-square odd-arm theorem remains valid. This family specifically
retains its four-outward condition while dropping square uniqueness,
settling the extension which the earlier two-overlapping-square example
did not settle. In fact the ratio of total negative capacity to the number
of capacity-two tiles is 1/(2h), tending to zero. No positive uniform
charge credit per such tile can hold without further geometric hypotheses.

The family does not violate coefficient one, the existing 5/6 bound, or the
flow theorem: its one source is completely paid and its margin is positive.
It also does not refute a theorem that separately requires occupied degree
exactly three; some interior vertices here have degree four. It supplies
the obstruction under the stated single-terminal degree-at-least-three
and complete-freezing hypotheses.

A usable next compensation statement must control *distinct global owners*
and source-bearing geometry, or charge the boundary of the whole repeated
strand region. A full tile's residual capacity and its four outward mates
alone cannot justify either a two-unit local donor or independent copies
of the shared negative reserve. Arbitrary bent paths and occupied bands
still need such a geometric adapter. No universal improvement of 5/6 is
claimed; the submitted 11 October manuscript, main and PR3 are unchanged.

## 6. Reproduction and formal scope

```sh
PYTHONDONTWRITEBYTECODE=1 python3 develop/check_four_outward_slab.py \
  --output output/four-outward-slab-validation.json
```

The verifier passes 75 physical models, including 40 symmetry images, with
2,272 four-outward tile occurrences,9,838 peeling-certificate events and
6,494 separately checked written-schedule events. It compares 35 full-pool
physical flow instances against independent terminal enumeration, and checks
all 19,682 nonempty oriented bundles of the smallest nine-edge witness.
These include h=1,...,32,48,64,128. The verifier uses no search solver.
It checks exact original corrected
charges, the full physical flow, an independent strict certificate for the
written freezing schedule, symmetry images, and every nonempty oriented
bundle on the smallest witness. The discovery search was used only to
find the initial h=2 example; neither the general proof nor reproduction
depends on satisfiability search or its negative results.

The Lean source `formal/SubQuorum/FourOutwardSlab.lean` checks the actual
h=1 matching, selected feasibility, terminality, all endpoint freezing,
the two four-outward tiles, the complete tile table and exact one-unit
negative capacity. Its frozen certificate uses the existing `FrozenPromotion`
inductive rules. A separate physical bundle-exclusion theorem checks the same
strict dependencies with mate retention restricted to actual endpoints;
it does not require blank vertices to remain occupied. All 13 declaration
audits pass locally with Lean 4.33.0, without warnings, sorry, native evaluation
or new axioms. Scalar all-h count consequences are also checked.
The arbitrary-h coordinate construction, freezing waves,
strand classification and resource adapter retain the written proofs above;
they are not claimed to be an end-to-end Lean formalization.

No mail was read, drafted or sent. AI tools were used for proof development
and verification. No new Oracle review or external priority claim is made.
