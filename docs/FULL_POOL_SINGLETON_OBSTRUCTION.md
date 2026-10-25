# A fully frozen singleton obstruction with the complete original resource pool

25 October 2026. Haobo Ma and Wenlin Zhang. Independent research branch.

There are feasible, fully frozen configurations with two alpha strands in
**different actual P-neighbour components** such that each component can pay
its alpha using the complete original interval pool, but together they can pay
only one. All terminal links may be chosen afresh. No previously selected
links are locked, and no extra resource is reserved. The obstruction already
holds with the existing BB-boundary packet convention. A second version
continues to fail even when every raw interval, including boundary intervals,
is available.

This supplies a genuinely essential singleton in the
[support-class reduction](SUPPORT_CLASS_SATURATION_AND_SINGLETON_CORE.md).
It strengthens the earlier [donor-collision construction](WHOLE_SUPPORT_DONOR_COLLISION_AND_FROZEN_PP_SEALS.md),
whose alternative lower exit still repaired the complete network. Here all
alternative routes have been checked in the written proof; the old fixed-C
collision is not being presented as a complete-network obstruction.

The failed implication is **local full compensation implies global full
compensation under feasibility and freezing alone**. This is not a
counterexample to the numerical grid inequality, to Proposition B.13, or to a
statement with additional global extremality hypotheses. We do not assert
that the selected set is globally maximal or optimal. The matching, band phase
and whole-owner-support interface are fixed; arbitrary mate surgery or a change
of band phase has not been excluded. The universal 5/6 improvement remains open.

## 1. Explicit family and hypotheses

Fix even W>=8, put R=W+4, and use the board of height W+12 and width22, with
aligned two-row bands starting at rows0,2,...,W+10. Coordinates are (row,column),
starting at zero. The original sealed construction has selections consisting
of the following left list and its translate ten columns right:

    (4,c), c in {3,5,7,9}; (5,c), c in {2,10}; (6,8);
    (7,c), c in {3,7}; (W+2,c), c in {3,8};
    (R,c), c in {2,10}; (R+1,c), c in {3,5,7,9}.

Its matching is the following left list and its translate ten columns right,
followed by the seal edges:

    (5+2i,5)--(6+2i,5),             0<=i<W/2;
    (6+2i,6)--(7+2i,6),             0<=i<W/2-1;
    (r,6)--(r,7), (r,8)--(r,9),     r in {5,R};
    (R-1,7)--(R-1,8);
    (r,3)--(r,4),                  r in {5,R};
    (6,4)--(7,4); (W+2,4)--(W+3,4);

    seal edges: (r,c)--(r+1,c), r=8,10,...,W, c in {4,14}.

These are exactly `sealed(W)` from the previous note; cropping the enclosing
board to width22 removes only blank columns. Keep this matching unchanged.
For the **raw-pool version**, add the seven selections

    (4,1), (5,0), (R+1,1), (R,0), (4,21), (R+1,21), (4,11).     (1)

Every added point is isolated from the old occupied set and from every other
added point. This is verified directly from the two coordinate lists, for
all W>=8: the new left and right points lie two or more Manhattan steps from
the nearest old occupancy, and the middle point (4,11) is two steps from
(5,10),(5,12). The top and bottom additions are separated by R-4>=8 rows.
Thus every old selected degree and every old endpoint neighbourhood and mate
is unchanged. Feasibility follows, and the old complete freezing certificate
replays unchanged. The arbitrary-length seal induction and relay freezing
proof are in the preceding note; no finite-height extrapolation is used.

The terminal strand inventory remains

    |T|=41, |M|=3W+10, |P|=6W+20;
    alpha=2, beta=0, mixed=14, pure PP/M cycles=2W-4.             (2)

The alpha strands have tips (5,5),(R,5) and (5,15),(R,15).
Every P point lies in columns3..9 or13..19, so there is no P adjacency between
these two slabs. Within each slab the column5/15 alpha, its adjacent seal and
return columns, and the horizontal cap edges connect the relevant endpoints.
The two alphas are therefore in distinct actual P-neighbour components.

The resource and link conventions are exactly those of the whole-support
normal form: one unit per original BB--TT interval; an open owner supports
all units in any maximal no-P gap incident to one of its P columns; pure
cycles give no open-owner support or beta credit. Terminal links join actual
horizontally adjacent TP and BP tips in the same band. They may be selected
subject to disjoint terminals. Whole virtual-owner support is the union of
its original owners' supports. Each original unit can pay at most one alpha.

## 2. Complete raw inventory and all support bypasses

There are no TT columns. Consequently each BB column is a separate original
interval unit, even if it is next to another BB. Denote its identity by
(original band index,original column); do not merge neighbouring units or
units in different bands.

The unmodified packet, rows4..R+1 and columns0..21, has four band classes:

    top/bottom:
    BB BB BT PT BP PT BP PT BP PT BT BB BT PT BP PT BP PT BP PT BT BB
    rows6,7:
    BB BB BB BT PP PP PP BT BT BB BB BB BB BT PP PP PP BT BT BB BB BB
    rowsW+2,W+3:
    BB BB BB BT PP PP PP BP PT BB BB BB BB BT PP PP PP BP PT BB BB BB
    remaining interior bands:
    BB BB BB BB PP PP PP BB BB BB BB BB BB BB PP PP PP BB BB BB BB BB.

There are W/2-3 bands of the last type; the total raw packet count is8W-20.
There are also five completely blank whole-board bands, giving110 units.
Each of the seven isolated additions replaces one BB by BT, so the complete
raw pool Q has

    L=|Q|=8W+83,
    S=area/2-|T|-|M|=8W+81=L-2.                              (3)

For the raw obstruction no unit is excluded, including every boundary unit.
For reference, the number of extreme-column BBs is W+8; the four terminal-band
boundary BBs have been replaced by BT. We do not apply the old first-BB packet
adapter to these new BT boundaries.

The added selections make the left outer gap columns0..2 in both terminal
bands entirely alternating BT, hence its raw capacity is zero. The right
outer gap columns20..21 likewise has zero capacity. The top middle gap
columns10..12 now consists of BT,TB,BT, again with zero capacity. The bottom
middle gap retains exactly one BB at column11:

    j=(R/2,11), physical pair {(R,11),(R+1,11)}.                (4)

The original alphas themselves have empty whole support in every band:
columns4,6 and14,16 are P columns throughout the alpha bodies, including
the pure-cycle seals. This rules out internal PP access, not just tip access.

For completeness, the entire nonempty open-owner support list is below.
All other open strands have empty support. The list is independent of W
except for the displayed row/band translations.

| Original strand tips | Complete raw whole-owner support |
| --- | --- |
| (R-1,7), (R-1,8) | (R/2-1,c), c=9,10,11,12 |
| (R-1,17), (R-1,18) | (R/2-1,c), c=19,20,21 |
| (R,8), (R,9) | {j} |
| (R,13), (R,14) | {j} |

To verify completeness, inspect the four band classes above. Every interior
P column is PP. The only interior open-owner P columns are the two horizontal
strands in the penultimate band, yielding the first two rows of the table.
The top and bottom open P columns face exactly the three outer/middle gaps
just analysed, or a neighbouring P column. Thus only the two lower middle
exits support a nonzero-capacity gap. Blank exterior bands have no P-column
boundary and hence no owner support.

The first two rows are real spare units, but their mixed strands cannot be
reached from either alpha by directed terminal links. They must remain in the
raw ledger; their existence does not create an admissible route.

## 3. Closed reachability and a proof for every legal terminal matching

Write A_L,A_R for the left and right original alpha owners. For either row
r in {5,R}, the only non-self transitions from A_L and A_R are the following.
An arrow stands for the specified actual TP--BP link and inclusion of the
unique next mixed strand; labels give that strand's two tip columns.

    A_L -> (3,4),         terminal TP3 supports no unit;
    A_L -> (6,7) -> (8,9), terminal TP9 sees only middle gap;
    A_R -> (13,14),       terminal TP13 sees only middle gap;
    A_R -> (16,17) -> (18,19), terminal TP19 supports no unit.   (5)

The actual links on the inward lower routes are

    left:  (R,5)--(R,6), (R,7)--(R,8);
    right: (R,15)--(R,14).                                   (6)

Every mixed strand in(5) has a horizontal original matching edge. Its BP has
only the previous TP and its own TP as possible horizontal terminal-link
neighbours. Its TP has only its own BP and, on the inward two-step chains,
the next BP as such neighbours. Self-links merely close that one original
mixed strand and cannot advance an alpha. The two strands at rowR-1 have
only their self-links: their other horizontally adjacent P neighbours are
in PP columns, hence are not tips. No vertical or interband terminal link
is part of this interface.

Therefore(5) is the complete non-self directed graph reachable from either
alpha. On its union, the support union is exactly {j}; each alpha separately
can reach j. All original supports, including internal ones, were used in
this conclusion. There is no beta to consume and no possible beta fork.

Now take **any** legal terminal matching C, without fixing earlier links.
Contract every original open strand to one owner and orient each selected
link from its TP owner toward its BP owner. An alpha has no incoming BP
ports and at most two outgoing links. A mixed owner has at most one incoming
and one outgoing link, because its two terminals can each be used only once.
There is no owner of indegree two, since there is no beta. An original alpha
cannot belong to a cycle or share a connected cancellation component with a
second alpha: along any attempted meeting the first meeting vertex would
require two incoming links. Its component consists of zero, one or two
outward directed mixed arms. Every owner in it is thus reachable from that
alpha in(5). There remain exactly two virtual alpha demands, and every unit
in either virtual alpha's whole support belongs to {j}.

Paying both would require two distinct original units in this singleton.
This is impossible. Equivalently, the two-demand set is a Hall obstruction
of size2 with neighbourhood size1, for **every C**, not just the optimum of
one earlier chosen C. The right link in(6) pays one demand with j, proving

    V(Q)=1, deficit=1, minimum links at maximum payment=1.     (7)

Both alphas initially have empty support, so cost0 cannot pay anything.
The right component's separate optimum is(value,cost)=(1,1); the left's is
(1,2), since its only useful exit needs the two distinct links in(6). Removing
j from Q makes both local optima0. Their P components are different, so this
is a jointly essential cross-component singleton, rather than a shared
mixed-gate bottleneck inside a single component.

In the exact gluing formula the local sum is2, while deleting J={j} gives
|J|+sum_i V_i(Q minus J)=1. In the singleton-core description E={j}; it cannot
be privatized to both owners by the preceding saturation lemma because its
support class has two owners and only one unit.

## 4. The existing boundary convention already has the same obstruction

For an example satisfying the original first-column-BB convention, use the
same base and add only

    (4,1), (R+1,1), (4,11).                                (8)

Now |T|=37. The extreme columns0 and21 remain BB in every band. Remove only
the usual two extreme-column marks per band, and no extra units. This gives

    raw L=8W+87, boundary B=W+12, available I=7W+75;
    S=8W+85, S-B=7W+73=I-2>0.                            (9)

The two outer terminal-band gaps have only their extreme boundary unit,
which is one of the standard marks. All other reachable supports are the
same as in(5), so the complete original **unmarked** pool still has V=1,
deficit1, and minimum cost1. The old packet compiler and the independent
compiler agree exactly after matching owners by actual original tips and
units by physical band/column identity. Thus the counterexample is not
based on silently broadening the original packet's boundary assumptions.

Version(1) fills those four boundary BBs physically, making the same result
hold even in the larger raw pool. Its custom no-TT compiler has deliberately
separate scope: whole-board matching closure, no TT, BB or BT boundary
columns. Published packet assertions were not disabled or modified.

## 5. Arbitrarily large deficit and a sharp two-unit repair control

Stack q copies of the raw board vertically at stride W+12, keeping width22.
Every stride is even, so the original band phase is preserved. Successive
occupied blocks have six blank rows between them. There is no intercopy
occupied adjacency or terminal link; every supported gap remains in its
original band's copy. The q distinct shared units j_i therefore give

    alpha=2q, beta=0, V=q, deficit=q, minimum links=q;
    local optima sum=2q, |Q|=q*(8W+83), S=q*(8W+81).         (10)

The upper bound is the q disjoint singleton neighbourhoods and injective
allocation; the q right lower links attain it. Every old freezing proof
replays within its copy. Counts add because the copies partition complete
bands; no shared separator band is counted twice.

As a sharp control, delete just the addition(4,11) from the raw version.
The upper middle singleton j_top=(2,11) returns. Both sources can now reach
two distinct resources. Give the left source the upper unit through its two
upper inward links, and the right source the lower unit through its one
lower inward link. This pays both with three links. Each source initially
has empty support and the left needs at least two links while the right
needs at least one, so three is exact. No P point, mate, or original terminal
link changes. This also explains why the older donor-collision family was
repairable: its unsealed alternative resources mattered.

## 6. What this changes in the proof strategy

The family disproves the hope that freezing alone forces saturation of the
complete whole-support compensation flow. Enlarging tip access to arbitrary
whole-owner support, allowing all links to be reselected, and opening every
raw interval still does not force full payment. The preceding saturation
and gluing theorems remain valid and detect the deficit exactly.

The numerical ledger is positive. In the raw family, after optimal payment,
U=L-1 units remain unused and t=1 demand remains unpaid. Thus

    U+beta-t=(L-1)-1=S=8W+81>0.                            (11)

For the original marked family it is I-2=7W+73>0. Consequently the obstruction
attacks the proposed route-to-full-compensation rule, **not the target
inequality or the existing 5/6 theorem**. It also is not a counterexample
inside an asserted globally extremal selected configuration: no such
hypothesis was proved for this family.

The next general target should allow real unpaid demand: bound its count by
unused original interval or receiver slack, counting each physical unit
once across components. Alternatively, if full flow is required in a proof
using a genuinely stronger extremal hypothesis, prove precisely how that
hypothesis excludes this sealed singleton family. A different band phase or
mate surgery is another possible mechanism, but requires its own proof.
Merely adding another local reachability criterion will not remove(7).

For a later paper supplement, the useful order is the fixed-C saturation
lemma, the exact singleton-core formula, this all-height obstruction, then
any new slack-versus-deficit bound. This note is the reviewable research
increment; the 11 October submitted manuscript is preserved.

## 7. Reproduction and formalization scope

    python3 develop/check_full_pool_singleton_obstruction.py --output output/full-pool-singleton-obstruction-validation.json
    python3 develop/check_full_pool_singleton_formal.py --lean /path/to/lean-4.33.0 --output output/full-pool-singleton-formal-validation.json

The independent no-TT compiler reconstructs the endpoint multigraph with
separate matching and PP edges, every original BB unit and maximal no-P gap,
all open-owner supports, and every legal terminal link. It does not call the
old first-BB packet adapter. Old-adapter comparisons are explicit separate
controls. The permanent [W8 fixture](../develop/fixtures/full_pool_singleton_obstruction.json)
contains actual selections, all34 matching edges, strict-rank witnesses for
all68 endpoints, every strand's support, and all26 candidate terminal links.

The base independent union/find and resource-allocation DFS enumerates all
777,924 legal terminal matchings:536,256 pay0 and241,668 pay1; none pays2.
It does not call the published cancellation/evaluation or flow functions.
This corroborates the all-C written argument; enumeration is not its proof.

Other controls cover19 height parameters W=8,10,...,40,64,128, each with the
raw obstruction, original marked obstruction, and two-unit full repair;
8 carried-band isometries;12 stacked boards at q=2,3,5,8 and W=8,12,20.
There are39 frozen raw-board checks and22 exact legacy-adapter comparisons.
All exact flows and independently checked strict-rank freezing certificates
pass. A carried rotation moves the original bands; re-pairing rows after
rotation would be a different interface and is not claimed.

[Lean source](../formal/SubQuorum/FullPoolSingletonObstruction.lean) checks14
new declarations and16 dependency declarations on local Lean4.33.0, without
warnings, sorry, native_decide, or extra axioms beyond standard Lean axioms.
It proves the arbitrary-route closed-set invariant, the singleton payment
injection obstruction, all-W raw/marked/stack arithmetic, concrete W8 feasible
geometry and full freezing, and the W8 owner-link closure and singleton
reachable-support certificate. The all-height coordinate compiler, the
no-beta cancellation-to-route adapter, actual P-component specialization,
exact min-cost optimality and the geometric all-copy adapter remain written
proofs with Python checks; this is not an end-to-end formalization.

No new Oracle review was requested. No email was read, drafted, edited or
sent in this increment. Public main, PR3, the submitted manuscript and shared
CI are untouched.
