# Exact compensation for every actual next owner after the second return

22 October 2026. Continue the two-parameter return family in
[the second-return theorem](SECONDARY_TEN_UNBOUNDED_SECOND_RETURN.md).
The parameters h>=12,g>=4 are even. Retain all H3,R,T,W,V original
endpoints, immutable supports and matchings; denote this partial union H.
Its next forced support is q=(23,h+13), with north V and west P_0
endpoint neighbours. All conclusions about complete extensions assume
the stated full even-U/rotor original model, with U breadth at least6
and both leg lengths at least4, all even. No catalogue exhaustion or
existence of a complete extension is asserted.

Explicitly, H3 has a_0=31,s_0=0,widths(h,12),depths(g+24,g+24),
root breadth6, hence a_1=g+49,s_1=-24. The four added originals are
R=U(32,10,g+2),chart(g+38+r,2-c);
T=U(6,4,g),chart(g+41+r,-23-c);
W=U(2g+20,4,40),chart(2g+42-c,r-34);
V=U(6,4,h+8),chart(16+c,h+15-r).

Every actual owner of q is an east-terminal U. Its selected-union
marginal is at least1 in the upward frame and at least2 in the downward
frame. Both statements are exact all-parameter receipt identities below.
This is one new-owner increment relative to H, not a full-family
allocation or repayment of the earlier h/2+1 selected-group deficit.

## Actual-owner classification without a parameter cutoff

In every complete extension containing H, the new owner of q must be
a U whose terminal at q has its own neighbour EAST. A rotor, a south
U terminal and both possible outer-bar-corner orientations are excluded.

The retained north and west endpoints imply that q's internal endpoint
neighbours can only be south or east. For a U, the only eligible roles
are a leg terminal or an outer bar corner: all leg interiors have two
opposite neighbours, while inner bar endpoints have three. The preceding
second-return theorem excludes all four possible rotor roles.

Write C=h+13. The following retained endpoint intervals and point are
enough for the new exclusions:

    P_0 contains (r,C-1), r=23,...,33;
    root K contains (r,C+1), r=25,...,31;
    B_0's fifth original contains (31,C).           (1)

All three claims follow directly from the original source charts. They
hold for every h,g. No new owner or source mass is used to obtain them.

If q is a SOUTH terminal, its incident stem contains every row from23
to23+d in column C, for even d>=4. For d>=8 it hits the retained
point(31,C). For d=4 or6 its bar contains both rows23+d-1,23+d and
extends either left or right from column C. At row23+d-1, its adjacent
bar endpoint is (26,C-1)/(28,C-1), or (26,C+1)/(28,C+1).
Every such point is retained by (1). Thus no south terminal is even
endpoint-disjoint from H.

If q is an outer bar corner with internal SOUTH and EAST neighbours,
the bar extends either down or right. A downward two-column bar has
columns C,C+1 and at least six rows starting at23, so contains the
retained root point(25,C+1). A rightward bar has the canonical form

    Q=U(B,d,f), chart(23+r,C-1+c).                  (2)

The stem at C hits (31,C) if d>=8. The far stem at C+B-1 hits the
root at row25 when B=6. Hence endpoint disjointness requires

    B>=8, d in{4,6}, f>=4, all even.              (3)

Conversely these conditions make Q endpoint-disjoint from H for every
f: the far column is at least h+20, to the right of every retained
endpoint; its near stem stops before row31; the bar is between the
row22 V band and the row25 root bar. That geometric feasibility does
not imply complete extendibility.

## Every feasible rightward corner is impossible in a complete extension

For Q satisfying (3), its missing original axial support is

    p=(24+d,C).

It has the north Q endpoint and the west P_0 and east K endpoints.
It must therefore be consumed by another fresh original.

For d=6, p=(30,C) also has the retained south endpoint(31,C).
All four neighbours belong to retained owners. A new matched endpoint
at p could have no available matching neighbour, a contradiction. This
case is impossible even without restricting the new original's shape.

For d=4, p=(28,C) has exactly those three retained neighbours. A
fresh U/rotor owner can only have its own neighbour south. A U would
be a south terminal with incident leg length at least4, so its
continuous stem includes (31,C), a retained endpoint. A rotor with
only its south terminal neighbour has two possible relative endpoint
patterns; one contains p+(2,-1), the other p+(2,1). These are the
retained P_0 point(30,C-1) and root point(30,C+1). Both rotor roles
therefore collide. The other possible U roles have more than one
internal neighbour and cannot fit the three-neighbour gate.

This proves that the ENTIRE endpoint-disjoint corner family (2)-(3)
has no complete extension in the full U/rotor model, regardless of
B,f,h,g. Finite dimension enumeration is not used in this exclusion.

For comparison, its exact partial-union marginal is B-7>=1. Its
negative source mass is B-1, new mixed full count7+(d-4)/2 and new
directed event count20+d-4. Its positive marginal cannot be assigned
to an actual complete-family occurrence, because that occurrence is
impossible. The companion verifier checks the entire new receipt sets.

## The two remaining east-terminal frames

Exchanging the two U legs when necessary gives exactly the two frames

    A_up=U(L,d,f), chart(24-c,C+d-r),
    A_down=U(L,d,f), chart(22+c,C+d-r),             (4)

with L>=6,d,f>=4 even. The terminal at q is the depth-d terminal.
For A_down, d=4 or6 makes its bar hit the root at row25, so an actual
downward frame requires d>=8. The row-frontier theorem below handles
its arbitrary far return and proves marginal3-delta>=2, delta in{0,1}.

For A_up there is a complete one-owner classification and exact ledger:

    endpoint-disjoint iff L>=8, or L=6 and d-f>=4;
    eta=1 iff L=8 and d-f<=2, otherwise0;
    Phi(H+A_up)-Phi(H)=2-eta>=1.                   (5)

This selected-union theorem does not require a complete extension. It
therefore applies to any actual upward owner. It does not repay the
earlier width-dependent loss by itself, and does not assert monotonicity
under additional owners.

## Proof of the upward-frame theorem

Put b=C+d, an odd column. The aligned two-column bar is {b-1,b},
with rows24-L,...,23. Both bar-end supports are outside its endpoint
tiles. The two axial terminal supports are inside, as are the odd-row
lateral supports of each leg. Direct counts give

    matching=L-1+(d+f)/2,
    endpointTiles=L/2+(d+f)/2,
    originalSupportsInside=(d+f)/2,
    charge(A_up)=-1.                              (6)

All retained endpoints outside V are at rows at least22, and at row23
only P_0 can meet A_up's tiles. P_0 ends at column C-1 and A_up starts
at C; both horizontal directions are excluded by their original bar-end
or axial supports. The A_up bar has minimum column b-1>=h+16,
across the aligned tile boundary from V's rightmost column h+15.
Thus only the near leg at row23 and far leg at row24-L need checking.

The new NEAR mixed full tiles have top-left (22,h+12),(22,h+14).
At the first tile, P_0 supplies its lower-left, V both upper cells,
and A_up its lower-right. The only new directed events are

    A_up:(23,h+13)->V:(22,h+13),
    A_up:(23,h+15)->V:(22,h+15),
    V:(22,h+14)->A_up:(23,h+14).                   (7)

The other vertical directions are excluded by immutable original
supports. The P_0-to-V event already present at column h+12 is not
counted again. The near signed contribution is2*2-3=1; together
with new negative mass1 it gives2 before the far receipt.

If L=6, the far leg is row18. V has endpoints there exactly in
columns h+14,h+15. The continuous far leg can avoid them iff its
odd terminal e=C+d-f is at least h+17, equivalently d-f>=4.
Under that bound the physical tile columns are separated and the
far receipt is zero. If L>=10, the far leg is at row at most14,
strictly above V's first physical endpoint tile row16, so every
far length is legal and its receipt is zero.

If L=8, the far leg is row16, which has no retained endpoints.
The partner row17 has V endpoints exactly at h+11,...,h+15.
Let e=C+d-f, odd. The far receipt is completely described by

    full top-left(16,c), c in{h+12,h+14}, e<=c;
    V:(17,c)->A_up:(16,c), c in{h+12,h+14}, e<=c;
    A_up:(16,c)->V:(17,c), c in{h+11,h+13,h+15}, e<=c.

At odd V columns the upward target is an immutable V support; at even
A_up columns the downward target is an immutable A_up support. There
is no full tile at left column h+10 because V has no endpoint(17,h+10).
The resulting counts are respectively

| Terminal e | New full | New events | Signed far value |
|---|---:|---:|---:|
| e>=h+17 |0|0|0|
| e=h+15 |0|1|-1|
| e=h+13 |1|3|-1|
| e<=h+11 |2|5|-1|

These far receipts lie in row16 tiles, disjoint from the row22 near
tiles. Equations (6)-(7) and this exhaustive table prove (5) without
any dimension cutoff or reused source mass.

## The downward row frontier for arbitrary far returns

For A_down, the two-column bar has columns b-1,b, b=C+d, and rows
23,...,22+L. It has positive charge1, with exact counts

    matching=L-1+(d+f)/2,
    endpointTiles=L/2+1+(d+f)/2,
    originalSupportsInside=4+(d+f)/2.

Both bar-end supports, both axial supports and the even-row lateral
supports lie inside. If d>=8, the bar lies entirely at columns at
least h+20, across an aligned tile boundary from ALL retained endpoints,
whose maximum column is h+19. The near-leg receipt has the same two
full tiles as the upward frame but exactly two new events, both at
column h+14, one in each vertical direction between V and A_down.
At q both vertical directions are excluded by original supports; at
h+15 both are excluded too. Thus the positive source count and the
near receipt together contribute1+4-2=3.

Its far leg lies on the even row y=22+L>=28, ending at the odd column
e=C+d-f. Define A(y),B(y) to be the rightmost retained endpoint columns
of H on rows y,y+1, with an empty symbol when a row has no endpoints.
Direct substitution in the original charts gives this complete table:

| Even y | A(y) | B(y) |
|---|---:|---:|
|28|h+19|h+19|
|30|h+15|h+17|
|32|h+16|h+16|
|34,36|h+14|h+14|
|38|h+5|11|
|40|11|11|
|42<=y<=g+46|2|2|
|g+48|3|5|
|g+50|4|4|
|g+52,g+54|2|2|
|g+56|-7|-13|
|g+58|-13|-13|
|g+60<=y<=2g+66|-22|-22|
|y>=2g+68|empty|empty|

Here are explicit reasons the table is exhaustive. For the first block,
the upper-row maxima through row40 are attained respectively by the
root far leg, east rotor B_0[8], the same rotor, B_0[3]'s far stem,
the same stem, B_0[5], and B_0[0]. Its long B_0[7] stem then has
column2 through row g+49. For the second block, translate the nine-base
row profile by anchor g+49 and offset-24: its east rotor attains the
two maxima3 and4, B_1[3] the next two2's, B_1[5] the -7, B_1[0]
the -13, and its long B_1[7] stem the final -22 through row2g+67.
The partner-row maxima follow by the same substitution. Every other
base endpoint is bounded by the corresponding listed maximum; each
base consists only of its bounded body and this one long stem.

The P/Z/X additions do not increase any maximum: P_0's relevant stem
has column h+12 only through row33; Z_0/X_0 are farther left. P_1's
bar and stem have maximum0 only through row g+51, while Z_1/X_1
are farther left. The root affects row28 and is dominated afterwards.
R's near/bar endpoints have maximum1 only while the first long stem
at2 is present; its far column is-30. T's near leg has column-23,
its far leg-29. W's rightmost column6 occurs only at row22, its
far-return short leg has maximum-30 and ends at row2g+41, and its
bar is at-34,-33. The second long stem at-22 dominates these later
endpoints. V ends at row22. Thus R/T/W/V introduce no unlisted row
maximum. The listed intervals cover every even y>=28 for all even
g>=4, including their shortest boundary cases.

The table has the simple invariant

    A even implies B<=A;
    A odd implies B<=A+2;
    A empty implies B empty.                       (8)

The continuous far leg is endpoint-disjoint iff e>A when A is present;
when A is empty every permitted f is legal. These conditions, together
with d>=8, are also sufficient for the whole A_down original.

If A is even, odd e>A means either e=A+1 or e>=A+3. In the latter
case no old endpoint shares its new physical tiles. In the former,
the only possible far event is the old horizontal direction

    H:(y,A)->A_down:(y,A+1).

Its reverse targets A_down's original axial support and is excluded.
By B<=A there is no old lower cell at column e, hence no new full
tile and no vertical event. The displayed event survives exactly when
its new target is not the source owner's immutable original support.

If A is odd, then e>=A+2. Only e=A+2 can contact anything, and then
the sole possible event is

    H:(y+1,e)->A_down:(y,e), if that old endpoint exists.

Its reverse is excluded by A_down's even-intrinsic-row lateral support.
No new full tile occurs: the other upper cell e-1 is larger than A
and absent. If e>=A+4 there is no contact. This exhausts all cases,
including the empty-row tail.

Let delta be1 exactly when the one possible old-to-new event survives,
and0 otherwise. The far receipt has NO new full tile and exactly delta
new events. It is physically disjoint from the near receipt. Therefore

    Phi(H+A_down)-Phi(H)=3-delta>=2.                (9)

This proves compensation for every arbitrary downward frame with no
far-depth or old-width cutoff. Together with the complete corner
exclusion and (5), every actual q-owner contributes at least1. The
remaining problem is joint allocation relative to the old occupied
band and further forced closure; the global grid targets remain open.

## Reproduction and verification scope

Run `PYTHONDONTWRITEBYTECODE=1 python3 develop/check_secondary_ten_next_support_east_terminal.py`
from the repository root. The deterministic controls cover both original
support phases, full support SETS, all four upward far profiles, both
downward far deductions, row-frontier boundaries and even translations.
The current run passes134 upward and831 downward exact receipt sets,
2110 exact row frontiers,144 corner receipt/nonextension controls, and
the role, collision and sealed-gate controls in the validation JSON.
These finite controls supplement the general chart proof above.

`formal/SubQuorum/SecondaryTenNextSupportEastTerminal.lean` checks
29 conditional/local theorems (31 explicit declarations), including
the blocked-neighbour contradictions, integer parity frontiers and
receipt inequalities. Every declaration was individually axiom-audited
under Lean4.33.0; the final run is clean. It does not formalize the
whole original-model classification or the source-chart event adapter.
The theorem has been submitted for independent Oracle review; no
independent verdict on this new theorem is claimed yet.
