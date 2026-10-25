# Isolated-candidate coverage fails; exact zero-loss strip-direction repair

25 October 2026. Haobo Ma and Wenlin Zhang. Independent research branch.

The [isolated-deletion repair theorem](ISOLATED_SELECTION_REPAIR_MATROID.md)
optimizes deletion choices provided their full candidate pool covers the
unpaid sources. Here we disprove automatic coverage for a fixed conservative
mixed-direction partition, even when every endpoint is frozen, the actual
matching is unique, all original units are available, and ALL occupied-isolated
selections have been deleted. The example has actual matching edges crossing
region boundaries. We also prove an exact repair by changing auxiliary band
directions, with no deletion required. Neither conclusion is a counterexample
to the numerical grid inequality or to coverage after an arbitrary repartition.

## 1. Precise model and theorem

Use the whole-owner-support model and original BB/TT interval units of the
[crossing-matching port ledger](CROSSING_MATCHING_PORT_LEDGER.md). Rectangles
are disjoint, even by even, and cover the board. Each chooses horizontal or
vertical bands. Restore every actual matching edge across rectangles before
identifying global owners. Supports are local-band no-P gaps incident to a
physical owner body; declared TP--BP links stay within the chosen local band.
Use the full resource pool and the full mixed/beta stem-and-fork model. In
particular no resource is artificially locked or withheld. Additional cross-
region terminal links are NOT part of this specific network.

Fix even W>=8, k>=1, and the board, P, unique matching M and attaining T*
from [the adjacent-module theorem](FORCED_MATES_AND_ADJACENT_MAXIMA.md),
namely `configuration(W,k)`. Its shape is (W+2) by (10k+2), and

    t=|T*|=(7k+2)W/2+3k+2,
    |M|=k(3W/2+5),    |P|=k(3W+10),    S*=2k.

Let X be ALL vertices of T* with no occupied neighbor in T* union P. For
ANY Y subset X put T_Y=T* minus Y. For ANY F subset {0,...,k-1}, use these
full-height column rectangles, with c=10a in module a:

| Columns, half-open | Band direction |
| --- | --- |
| [c,c+2) | vertical |
| [c+2,c+4) | vertical if a belongs to F, horizontal otherwise |
| [c+4,c+10) | vertical |
| final [10k,10k+2) | vertical |

This is a valid partition into 3k+1 even rectangles. Write V for maximum
whole-support compensation, D for unpaid alpha count, and L_min for minimum
link count at value V. Then, for EVERY such W,k,Y,F,

    alpha=k, beta=k, mixed=k(W/2-2),
    |Q|=S_Y=2k+|Y|,
    V=|F|,    D=k-|F|,    L_min=0.                       (1)

P, M, complete freezing and every physical global owner body, source identity
and ordinary tip type are unchanged throughout. There are always exactly 2k
actual crossing matching edges. Directions change support and resource IDs:
resources from two different partitions must never be pooled together.

For F empty, every deletion candidate has zero marginal and zero joint
payment gain. Taking Y=X gives a completely frozen board with NO occupied-
isolated selection, still with D=k. Thus freezing plus deletion of all such
selections does not imply fixed-partition candidate coverage V(E)=k.
For F all modules, full compensation already holds at Y empty, with zero
selection loss. Within this prescribed family of direction changes, all k
narrow strips must be flipped and doing so suffices.

## 2. Deletions, exact counts and unchanged freezing

The prior isolated-deletion adapter applies to each Y: P neighborhoods,
terminal types, all freezing witnesses and the old resource identities of a
FIXED partition persist. Each deleted point adds one distinct original
singleton sink and S increases by one. Because a deleted point had no
occupied neighbor, each remaining selected point has exactly its old
occupied degree. Thus the isolated points of T_Y are exactly X minus Y.

Here are explicit all-X counts, rather than an inference from finite scans:

    |X|=k(5W/2-9)+W-6,
    |T_X|=k(W+12)+8,
    S_X=k(5W/2-7)+W-6.                                  (2)

To check them, use the row formula for T* in the adjacent-module theorem.
All selected-selected adjacencies are precisely

    (1,0)--(2,0),
    (W-4,0)--(W-3,0),   (W-4,2)--(W-3,2),
    (W-1,0)--(W,0),
    (2,10a+11)--(3,10a+11),  a=0,...,k-1.

They cover 2k+8 selected points. Selected points adjacent to P are counted
by the following disjoint row groups:

| Rows | Number adjacent to P |
| --- | ---: |
| 0 and W+1 | 8k |
| 1 and W | 4k |
| 2 | k |
| 3 | 2k |
| odd 5,...,W-3 | k(W-6)-1 |
| W-2 | k+1 |
| all remaining rows | 0 |

These sum to k(W+10). Feasibility makes the P-adjacent and T-adjacent
categories disjoint. Their union is all nonisolated selections, proving
|T* minus X|=k(W+12)+8 and then (2). After deleting X every remaining
selection has degree exactly one in T_X union P. Complete freezing is
preserved by the P-neighborhood argument, not by maximality of T_X;
T_X is no longer asserted to be a selection maximum.

## 3. Global strands and actual interface crossings

Suppress translation c. The vertical classification in the
[guarded-reserve theorem](PERPENDICULAR_GUARDED_RESERVES_AND_JOINT_MAXIMALITY.md)
has one strand L with tips (1,3),(W,3), short strands R_r with tips
(r,6),(r+1,6), r=2,4,...,W-4, and R_end with tips
(W-2,6),(W-1,8). There are also four alternating pure cycles per module.
L traverses both column3 tips and every P vertex in columns4,5, rows1..W.

Changing the width-two strip [c+2,c+4) between horizontal and vertical
auxiliary pairing alters NO auxiliary edge having both endpoints in P:
its only P vertices are (1,c+3),(W,c+3), and in either pairing their partners
are selected points outside P. The entire graph M union N[P] is therefore
identical to the vertical one, so its physical owner bodies are identical.
The ordinary tips remain TP in either direction: their horizontal partners
are (0,c+3),(W+1,c+3); their vertical partners are (1,c+2),(W,c+2).
All four partners face P and hence survive every Y. Other tips and auxiliary
edges are unaffected.

The L strands are alphas. Each R_r is mixed: its even-row band partner
(r,c+7) is blank and its odd-row partner (r+1,c+7) is selected. Both R_end
partners, (W-2,c+7) and (W-1,c+9), are blank, so R_end is beta. This proves
the inventory in (1), unchanged by Y.

The only crossing actual edges are

    ((1,c+3),(1,c+4)),    ((W,c+3),(W,c+4)).              (3)

Cutting them produces two CT half paths in the narrow strip, and one CC
relay in the right vertical strip, in EACH module. Restoring (3) gives L.
All other ordinary-ended owners are closed local mixed/beta owners; there
is no closed local alpha. Thus there are 2k CT half paths, k CC relays and
exactly k interface alphas, regardless of F. In particular this is not an
artifact of omitting genuine matching crossings. The exact global ledger
S=|Q|+beta-alpha now gives |Q|=2k+|Y|.

## 4. The all-route obstruction in each unflipped strip

Fix a not in F. L_a's only ordinary tips are (1,c+3),(W,c+3).
In their horizontal local bands their sole possible axis neighbor inside
the rectangle is column c+2, which is selected, not in P. Column c+4 is
in another rectangle, so supplies no declared local-band terminal link.
Interior PP body vertices are not additional ordinary tips. Hence L_a
has NO outgoing owner link, and its reachable closure consists of itself.

Its own support is empty. In each top/bottom narrow horizontal band the
only adjacent no-P column is c+2; this column is BT, since (1,c+2) or
(W,c+2) is selected. There is no BB/TT resource in this one-column gap.
In the vertical band (c+4,c+5), its body occupies every row1..W; its only
no-P gaps are the single-row caps 0,W+1. These are BT because (0,c+5)
and (W+1,c+5) are selected. All four gap-sealing selections face P and
are outside X, so the gaps stay sealed for every Y. No other band meets L_a.

An arbitrary-length directed route starting at L_a thus stays at L_a,
where no original unit is supported. No beta is reachable either. In the
full stem/fork model a source needs an interval-ending route or a route
to an actual beta BP gate; neither is possible. This excludes all routes,
not just the routes of one chosen optimum. It applies simultaneously and
independently to all k-|F| unflipped sources. Therefore V<=|F|, even with
all original resources and arbitrary rerouting of other owners.

## 5. Exact private-reserve repair and no repeated credit

For a in F, L_a's two ordinary tips lie in vertical band (c+2,c+3).
The selected partner (1,c+2) sees P at (1,c+3), so (2,c+2) cannot be
selected. The other cell (2,c+3) has two P neighbors, (1,c+3),(2,c+4),
so it also cannot be selected. Neither is in P. The corresponding two-cell
column at original row2 is BB. The bottom symmetric argument gives a BB
column at original row W-1.

These are genuine DISTINCT singleton original units, not two vertices
counted from one interval. At every interior row, column c+3 has its P
neighbor in c+4; a TT pair in columns c+2,c+3 would give it a second
occupied neighbor. Thus the no-P gap between original rows1,W contains
no TT columns, so each BB is its own forest component. Both are incident
to L_a. This band has no other P owner, and bands for distinct modules
are disjoint: the two units are private even relative to all other owners.

If b_a is the global band index of this strip, their compiler IDs are
(b_a,2,2) and (b_a,W-1,W-1). Choose ONLY the first for each a in F.
Distinct modules have distinct b_a, so this assignment is injective.
Each payment uses its own alpha and original unit, no links, and no beta
or mixed gate. It gives V>=|F| at cost zero. The previous upper bound proves
all three exact optimization formulas in (1). The second private unit is
unused and is never credited to another source.

The flip creates no extra numerical slack: T_Y,P,M and S_Y are fixed.
It changes the auxiliary decomposition and hence which original intervals
and supports represent that same slack. It is invalid to add the old and
new pools. This distinction is essential: deleting isolated points and
choosing directions are two mathematically different operations.

## 6. Concrete witness, validation and formal scope

The permanent fixture has W=8,k=2,Y=X,F empty. Its 10-by-22 board has
48 selections, 34 actual matching edges, 68 fully frozen endpoints, 24
removed isolated candidates, no remaining isolated selection, 2 alpha,
2 beta, 4 mixed, 28 original units, slack28, four matching crossings,
V=0 and D=2. Flipping both narrow strips pays both sources without changing
this board. Alternatively at Y empty, the original maximum has 72
selections, slack4, and the same zero-loss direction repair.

Run:

    python3 develop/check_isolated_coverage_obstruction.py --output output/isolated-coverage-obstruction-validation.json
    python3 develop/check_isolated_coverage_formal.py --lean /path/to/lean-4.33.0 --output output/isolated-coverage-obstruction-formal-validation.json

The solver-free physical checker passed 568 partition/deletion models,
171004 strict freezing events, 2608 exact one-owner source closures,
244 independent primitive value/cost comparisons, 168 fully frozen boards
with no isolated selection, and all 64 subsets of six chosen candidates.
The controls cover W through64, k through16, arbitrary flip subsets on
small cases, and deletion subsets including the entire X. These corroborate
the preceding all-parameter proof; they do not replace it.

Local Lean4.33.0 passed 13 declaration audits with no warnings, sorry,
native evaluation or new axioms. Preflight checked memory and actual
lean/lake comm basenames, preserving unrelated jobs. The standalone Lean
module checks arbitrary-length reachability at a root
with no outgoing links, the resulting no-payment obstruction, retention
of P-adjacent seals under isolated deletions, preservation of the PP graph
when changed pairs never join two endpoints, injectivity of private reserve
IDs, and the scalar counts and exact flip/deficit arithmetic. The general
coordinate classification, BB/TT extraction, freezing adapter and full
stem/fork correspondence remain written proofs with executable checks.
This is scoped formal validation, not an end-to-end formal grid theorem.

## 7. What has failed and what remains

The failed rule is: complete freezing plus deleting all occupied-isolated
selections guarantees full compensation in the fixed conservative mixed
partition. The candidate coverage assumption in the repair-matroid theorem
is genuinely necessary. Even 'no isolated selection remains' cannot replace
it. An unbounded supply of original units elsewhere cannot pay a source
with empty reachable support; no original surplus is counted twice here.

The target numerical inequality and any universal improvement of 5/6 remain
open. This family actually admits full compensation by the explicit strip
repair, and also by globally vertical bands. It leaves open coverage under
an appropriately chosen partition, coverage with additional justified
cross-region links, and the uniform whole-board H/V no-isolated question.
A useful next geometric task is to characterize when local direction
changes preserve needed old certificates while opening private support;
one cannot assume the source identities survive for an arbitrary P.
