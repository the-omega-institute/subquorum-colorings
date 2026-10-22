# A nonreusing whole-family budget for transverse U sources in six rows

22 October 2026. Authors: Haobo Ma and Wenlin Zhang.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.

## Statement and its relation to the open pocket problem

Use the immutable full-even-U endpoint/support/matching records and physical
tiles of `TEN_ROW_COMPLETE_CHAMBER_CLASSIFICATION.md`. Consider ANY finite
endpoint-disjoint family Y in rows0 through5, every member a transverse
U(6,d,f), where d,f are arbitrary even integers at least4. Its vertical bar
occupies all six rows in columns b,b+1. Its two stems run horizontally,
both right or both left, in rows0 and5. Arbitrary integer b, either
direction and independently unequal depths are allowed. Completeness is
NOT required for the first theorem. Write a for the number of even-b bars,
b_odd for the number of odd-b bars, and n=a+b_odd.

Then the exact inventory Phi obeys

    Phi(Y) >= a+2 b_odd >= n.                              (1)

In the aligned six-row pocket left by a spanning upward U_W, if ALL further
sources are transverse U sources of this kind, their physical tiles do
not touch the old core. Therefore the whole-chamber increment is at least

    Delta_chamber >= 5+n.

If the chamber is complete and Y is nonempty, in fact n>=2. Thus

    Delta_chamber >=7 for a nonempty transverse-only pocket, (2)

whereas the empty pocket has exact increment5. The bound7 is attained by
locally complete pocket states for EVERY even W>=12. This does not assert
global extendibility of those states. Horizontal-bar U sources and rotors
are not covered; their exclusion or joint budget remains an open part of
the arbitrary-width complete-pocket problem.

## Canonical coordinates and original charge

For a right-facing original take the complete canonical record U(6,d,f)
under the chart

    (r,c) -> (6-c,b+r).

For a left-facing original use (r,c)->(6-c,b+1-r). The bar columns in either
case are b,b+1; d is the row5 stem depth and f the row0 stem depth. Swapping
these independent parameters includes reflection in the horizontal axis.
Put t=(d+f)/2. The complete record has the following counts, in either
direction:

| Bar start | Matching edges | Endpoint tiles | Original supports inside those tiles | Charge |
|---|---:|---:|---:|---:|
| b even | 5+t | 3+t | t | -1 |
| b odd | 5+t | 4+t | t-2 | -5 |

For even b the bar occupies three whole tiles and each stem adds its
depth/2 tiles beyond the bar. For odd b the bar occupies six partial tiles,
and each stem adds depth/2-1 more. The alternating inner lateral supports
give respectively t or t-2 supports inside the footprint; beyond-tip and
above/below supports account for the excluded ones. These disjoint interval
counts prove the table at every depth, rather than fitting sample values.
All charges are negative, so their total source mass in Phi is a+5b_odd.

## All possible mixed tiles and events

Order the distinct bars from left to right. Their two-column intervals are
disjoint: overlapping bar columns would overlap endpoints in every row.
Every point in rows1 through4 belongs to a bar. Vertical foreign endpoint
adjacency is impossible. Indeed, if one of two vertically adjacent points
is on a bar, that same bar owns the other point; an adjacent pair in the
strip must have at least one row among1 through4.

If bars start at x and x+2, the left source must face left and the right
source right. Otherwise its stem, of depth at least4, hits the other bar.
Consequently no source can belong to two such adjacent-bar pairs: a middle
bar would have to face both directions. This conclusion uses the complete
original endpoint records and holds even in incomplete families.

If x is even, the adjacent bars lie in different physical tile columns.
If x is odd, their touching columns x+1,x+2 share one tile column. The three
tiles in that column are full and mixed. Each of their twelve endpoint
tails emits a source-labelled event across the interface: the foreign
bar endpoint is not an original support of the emitting source. Thus one
such pair contributes exactly3 mixed tiles and12 events, net -6.
Let p be the number of these ODD adjacent-bar pairs. They form a matching
on the odd-bar sources, so 2p<=b_odd.

There are no other mixed full tiles. Such a tile needs endpoints in row1
or4 (or both interior rows2,3), hence has a bar column. If both columns
belong to one bar it was full in that original; if they belong to different
bars this is precisely the odd adjacent-bar case. A remaining column
containing a stem has endpoints in row0 or5 only and cannot complete it.

It remains to classify events outside those pairs. All are horizontal.
Along a stem, every nonterminal point has its horizontal neighbours in its
own endpoint set; the point just beyond a terminal is its own original
support, so that terminal emits no event to a foreign neighbour. Hence an
event not already counted must emit from a bar endpoint into a foreign
stem terminal. It is on row0 or5, on the BACK side of that bar: the front
side next to the bar is already its own stem. An even-b bar has no intratile
backside neighbour. An odd-b bar can emit at most one such event on each
of rows0 and5. Its foreign terminal emits no reverse event, since the bar
point consumes that terminal's original beyond-tip support.

An odd bar in an adjacent-bar pair has its whole backside occupied by
that partner, so it has NONE of these remaining events. Thus, writing e
for the remaining events, their (emitting owner,row) labels are injective
and

    0<=e<=2(b_odd-2p).                                    (3)

This exhausts original source-labelled events, not just unlabelled edges.
In particular the twelve events of a bar pair are not mistaken for six.

## Exact ledger and no reuse

The preceding geometric classification gives the EXACT identity

    Phi(Y)=a+5b_odd-6p-e.

Using (3) and 2p<=b_odd yields

    Phi(Y)>=a+3b_odd-2p>=a+2b_odd.

Each odd pair spends6 once from the mass10 of its two distinct sources,
leaving4. Every unpaired odd bar spends at most2 from its own mass5,
leaving at least3. Each even bar retains its mass1. The pair matching and
the injective event labels prove that these payments cannot share a source
or event; all full mixed tiles have already been assigned exactly once.
This is a whole-family inequality, with no selected-source surplus being
silently reserved again for another contact.

## The same theorem at arbitrary even common height

The proof above is not intrinsically restricted to six rows. For ANY common
even height h>=6, use full transverse U(h,d,f) originals in rows0 through
h-1, with the same bar normalization and aligned top row0. The matching
count is h-1+t. For even bars the endpoint-tile/inside-support counts are
h/2+t and t; for odd bars they are h-2+t and t-2. Thus their charges are
-1 and1-h respectively. The adjacent odd-bar pairs are still a matching;
each pair now has h/2 mixed tiles and2h events, net -h. All other events
are still at the two outside rows, at most2 per unpaired odd bar.

Consequently the exact identity and bound become

    Phi(Y)=a+(h-1)b_odd-hp-e,
    Phi(Y)>=a+(h/2-1)b_odd>=a+2b_odd.

Indeed twice the difference between Phi and the first lower bound is
h(b_odd-2p)-2e, which is at least(h-4)(b_odd-2p)>=0. Two adjacent odd bars
facing away attain Phi=h-2, so the per-odd-source coefficient h/2-1 is
sharp. An isolated even bar attains1, making its coefficient sharp too.
No completeness premise is used. This controls an entire arbitrary-size
parallel-source family with unequal legs, not just a fixed six-row example.
The singleton-completeness argument below additionally uses the particular
old supports of the six-row pocket and is stated only for that pocket.

## A complete pocket cannot contain exactly one transverse original

Normalize the aligned pocket to [0,5] x [0,N-1], where N=W-2 is even.
The one-step boundary is occupied by old endpoints. The old core also has
original supports at (1,0),(4,0),(1,N-1),(4,N-1). These remain subject to
the full retained-support condition, as established in the previous note.

Suppose exactly one transverse original occurs. Its beyond-tip support
on row0 has both its own terminal neighbour and an occupied boundary
neighbour on row-1. If inside the pocket, this support is neither its own
endpoint nor an old endpoint and cannot be consumed, contradicting
completeness. It must therefore be on the vertical boundary. Consequently
the row0 terminal lies at column0 orN-1. At that same column, the old
support on row1 has its old vertical-wall neighbour and the new terminal
neighbour. It too must be consumed. But the single source has no endpoint
there: its bar is at least three columns away, and only its row0/5 stems
reach the tip column. This is a contradiction. Thus a nonempty complete
transverse-only pocket has at least two originals, proving (2).

## Arbitrary-width sharp complete pocket states

For every even N>=10 choose even d,f with 4<=d,f<=N-6. Use a right-facing
U(6,d,f) at bar0 and a left-facing U(6,N-2-d,N-2-f) at barN-2. Their row5
tips are at d and d+1; their row0 tips at f and f+1. The two rows are
filled end to end; all other endpoints are on the two extreme bars. The
tips cross-consume their original beyond-tip supports.

All old interior supports at columns0,N-1 are consumed by the bars. The
new supports outside the pocket are consumed by its occupied boundary.
The only remaining supports are on row1 or4. On row1 the left supports
are odd columns3 through f-1; the right supports are even columns f+2
through N-4. They are separated across the seam by3 and internally by2.
Each has exactly one occupied neighbour, its endpoint on row0. The row4
statement is identical with d in place of f and row5 in place of row0.
No other support is retained inside the pocket. This proves full local
retained-support feasibility for every parameter, including d!=f.

Both bars are even, giving source mass2. There are no mixed full tiles
or events, so the pocket contribution is EXACTLY2 and the whole chamber
increment exactly7. Disjoint even-width blocks of these pairs may also
be juxtaposed: their bar tiles do not cross a block boundary. The exact
pocket contribution is2k for k blocks, with independently chosen depths
and widths and no reuse. These explicit complete local states rule out
any proposed universal nonempty-pocket lower bound greater than2.

## Verification scope and remaining frontier

`develop/check_six_row_transverse_budget.py` reconstructs full canonical
T/H/M records and compares exact charge, mixed-tile and labelled-event
sets with the classification above, including both directions, both bar
parities, unequal depths, large parameters and simultaneous families.
Separate written arguments establish every unrestricted-parameter step.
`formal/SubQuorum/SixRowTransverseBudget.lean` supplies the scoped six-row
geometric and arithmetic formalization: bar clearance, forced facing-away
directions and no touching-bar chain; no vertical foreign adjacency;
terminal/support and inherited-singleton obstruction; budget arithmetic
and sharp-pair arithmetic. All24 explicit declarations, including17 local
theorems, are individually axiom-audited. Final local Lean4.33.0 invocation
595c3b exited0, no warnings/sorry/native, only ordinary axioms or none;
preflight65% memory free and no real lean/lake by comm-basename inspection.
It is not an end-to-end formalization of the full original-source inventory,
event classification, general-height extension or completeness assembly.
Those parts have separate written proofs. The first Lean attempt exposed
two already simplified True goals and was corrected before the passing run.

Final exact-record verifier8b6ce5 exited0:27782 disjoint pairs,100 greedy
simultaneous families,46 opposed-pair/local complete controls,135 arbitrary
common-height controls through height2000, and1116 actual old-core singleton
obstructions. All three ordinary-event cardinalities0/1/2 and the full
odd-bar adjacent-pair event sets are exercised. An independent self-contained
audit is running on originalstream84340, with no verdict yet. Its attachment
contains every theorem/proof and final Lean, canonical definitions and the
verifier before the extra1116 singleton controls; those extra controls are
not claimed independently reviewed. Pool preflight17ready/8busy/1attention/
0queued. No service-worker settings were changed or live request duplicated.

Finite six-row discovery has additionally found no rotor-containing
complete state at W8,10,12,14,16,20; W24 andW30 timed out at their specified
solver budgets and are UNKNOWN. A separate search found no nonempty
complete pocket contribution<=1 at W8,10,12,14,16,20,24. Neither finite
statement proves rotor exclusion or a general complete-pocket inequality.
The new theorem controls the entire transverse-U subfamily at arbitrary
width, not the horizontal-U/rotor interactions with that family. The
exterior sign, universal decomposition and global5/6/grid targets remain
open. The submitted manuscript and shared infrastructure are unchanged.
