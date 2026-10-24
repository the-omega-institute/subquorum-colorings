# Every actual root-support owner after a short upward return has nonnegative marginal

22October2026. This continues the
[four-original obstruction and short-return restriction](SECONDARY_TEN_FOUR_ORIGINAL_RETURN_OBSTRUCTION.md).
All original endpoints, supports and matchings remain fixed. Work in
the explicit full-even-U/standard-rotor model, with U breadth at least6
and both even leg depths at least4. This does not assert catalogue
exhaustion for arbitrary grids or existence of a complete extension.

## Hypotheses and theorem

Let h>=12,g>=4 be even. Retain the two-block H3 with a0=31,s0=0,
widths(h,12),depths(g+24,g+24),root breadth6, and the originals

    R=U(32,10,g+2),chart(g+38+r,2-c);
    T=U(6,4,g),chart(g+41+r,-23-c);
    W=U(2g+20,4,40),chart(2g+42-c,r-34).

Let a selected upward east-terminal owner of z=(22,7) be

    A=U(L,D,F),chart(23-c,7+D-r),
    L>=6,4<=D<=h+4,F>=4, all even.               (1)

Write H=H3+R+T+W+A, C=h+13, b=7+D, a=23-L, e=b-F.
Thus C,b,a,e are odd and b<=C-2. The old root support
p=(25,C) is absent from H but has retained west/east endpoint neighbours.

In every complete extension containing H, the owner O of p is a full U.
After exchanging its two legs, its exact original record is one of

    EAST: O=U(B,30-t,f),chart(t+r,C-1+c);
    WEST: O=U(B,30-t,f),chart(t+r,C+1-c),         (2)

where B>=6,f>=4 are even, t is even and t<=22. The west form also
requires t<=20. Its leg through p ends at (30,C), immediately above
the retained B0[4] endpoint(31,C); it cannot end earlier.

Every endpoint-disjoint record in (2), with the precise frontier
restrictions below, has the exact selected-union marginal

    Phi(H+O)-Phi(H)=1-delta>=0,
    delta in{0,1}.                              (3)

No reserve of H3 or A is assigned again. This is an all-parameter
classification and ledger for a SINGLE actual p-owner. It does not
assert monotonicity under arbitrary later originals or settle the whole
family allocation problem.

## Why the near leg must terminate at row30

The retained source records K,P=P0,Q=B0[4] give

    P:(r,C-1),23<=r<=33;
    K:(r,C+1),25<=r<=31;
    Q:(31,C).

There are no old H3/R/T/W endpoints in column C at rows23..30,
and A ends at row22. The same interval is therefore endpoint-empty
before O. The point p is K's original left bar-end support. Its
two horizontal neighbours force occupation by a distinct original.

The four vertical-terminal rotor patterns all collide with P's left
wall, as in the preceding obstruction. A full U at p cannot have a
horizontal internal neighbour, so it must contain p on a vertical leg
outside its bar. Let t be that leg's bar row and u its tip row.
Continuity and the retained endpoint(31,C) prevent crossing row31.
A bar at rows25..30 has both horizontal companions blocked by P,K;
a bar above row30 would force its leg through (31,C). Thus t<=24.
The leg points south, with25<=u<=30.

Suppose u<=29. Its original axial support p'=(u+1,C), at a row
q in26..30, is absent from the baseline and from O. It sees O to
the north and P,K to the west/east, so it must belong to another
original whose only possible internal neighbour is south.

A rotor there contains (q+2,C-1), a P endpoint because28<=q+2<=32.
For a U, a south terminal has a continuous stem of even depth k>=4.
If q>=27, that stem contains (31,C). If q=26 and k>=6 it also
contains (31,C). The only remaining case q=26,k=4 puts its outer
bar at row30, where both horizontal companions are blocked by P,K.
All possible owners are excluded. This proves u=30.

Since u=t+d with even d, t is even. The case t=24 has its inner
bar row25, where both possible inward neighbours are retained.
Consequently t<=22 and d=30-t>=8. The bar can extend either east
or west, giving exactly (2). A west bar at t=22 has inner row23
containing (23,C-1), a P endpoint, so west requires t<=20.
Leg exchange preserves the entire even-U matching/support record.

## Exact endpoint-disjointness frontiers

Put v=t+f, the even far-tip row. The following conditions are necessary
and sufficient for disjointness of O from the ENTIRE H, beyond (2).
They are partial-union conditions; they need not guarantee completion.

### East bar

The far column is C+B-1, even. If B>=8 it lies at least C+7,
across an aligned physical tile boundary from every H endpoint,
whose maximum column is C+6. There is no far restriction.

The bar itself is also disjoint: at both possible bar rows t,t+1<=23,
H has no endpoint in columns C through C+6. This row-local emptiness
follows from the recursive source records, in addition to the global
maximum-column bound. Endpoints in those columns start below these rows.

If B=6, the far column is C+5. Its first old endpoint is K's
bar at row25, so the exact restriction is v<=24. All earlier rows
in this column are empty, and there are no later contacts before this
first collision. A has maximum column b<=C-2 and cannot meet O's
physical endpoint tiles in either east case.

### West bar

Put J=C+1-B, an even far column. The bar spans every column from
J to C. If J>=b+1, the entire O is across an aligned column
boundary from A. Its first old far-column endpoint is P's row23,
so the exact restriction is v<=22.

If J<=b-1, the bar crosses A's bar column b. Disjointness requires
its two rows to lie strictly ABOVE A's top row a: since t is even
and a odd, this is exactly t<=a-3. Below that top, A's vertical
bar reaches row22, so every other t<=20 crossing placement collides.
Once the bar is above A, there are three far-column phases:

| Far column | First old far-column endpoint | Exact terminal restriction |
|---|---|---|
| e+1<=J<=b-1 | A's far leg at odd row a | v<=a-1 |
| J<=e-1 and J>=-34 | contiguous W/A row22 | v<=20 |
| J<=e-1 and J<=-36 | none | none |

The row22 endpoints of W and A together occupy every column from-34
through b. In the last phase J and its partner column J+1 are left
of that entire old union and of A's far terminal e. Before row22,
the only possible A contact for J<=e-1 is J=e-1: the two horizontal
directions at its far terminal both target immutable axial/lateral
supports and are excluded from events. These observations cover every
unbounded width, far depth and old g; no body of a lower old block
can be reached without the displayed first collision.

## Complete new receipts and no double use

Use the single immutable H inventory. The only NEW mixed full tiles,
specified by even top-left coordinates, are

    (24,C-1),(26,C-1),(28,C-1),(30,C-1).         (4)

The first three have P in their left column and O in their right.
The last has O at(30,C), Q at(31,C), and P in both left cells;
it is one three-owner tile, counted once. Before O its upper-right
cell was missing. Every far frontier has a missing other upper cell,
so no far contact creates another mixed full tile.

There are eight NEW near directed events. For both orientations:

    P:(r,C-1)->O:(r,C),r=24,26,28,30.

For the east form, the other four are

    O:(r,C)->P:(r,C-1),r=23,25,27,29.

For the west form, they instead occur at r=24,26,28,30. These
different phases follow from their respective immutable lateral supports.
The other directions are original-support targets and remain excluded.
At the bottom three-owner tile the Q-to-P event at row31 already
existed, and the O/Q vertical directions target their original axial
supports. It supplies no omitted new event.

All possible far receipts consist of the following SINGLE event:

| Form and phase | Event present exactly when |
|---|---|
| East,B=6 | v=24: K:(25,C+5)->O:(24,C+5) |
| West,J>=b+1 | v=22: P:(23,J)->O:(22,J) |
| West,e+1<=J<=b-1 | v=a-1: A:(a,J)->O:(a-1,J) |

In each case the reverse direction targets O's original axial support.
The displayed old-to-new direction is not an original support of its
source. Other legal phases have no far event. In particular J=e-1
has two excluded horizontal directions, and the row22 stopping phase
ends at least two rows above its first collision. Define delta=1 when
one of these three mutually exclusive conditions holds, otherwise0.

The far tile column is different from the near column because B>=6.
Thus the complete receipts are a disjoint union of (4), the eight
near events and at most one far event. All events have their original
source-owner labels. No old event or previously available credit is
recounted, even at the three-owner tile.

For d=30-t the original source counts are

| Form | Matching | Endpoint tiles | Supports inside those tiles | Charge |
|---|---|---|---|---|
| East | B-1+(d+f)/2 | B/2+1+(d+f)/2 | 4+(d+f)/2 | +1 |
| West | B-1+(d+f)/2 | B/2+(d+f)/2 | (d+f)/2 | -1 |

East has both bar-end/axial supports and its even-row lateral supports
inside. West has its axial and odd-row lateral supports inside, and
both bar ends outside. The source contribution is therefore exactly1
in BOTH cases: one new positive indicator, or one new negative-mass unit.
Consequently the single ledger is

    1+2*4-(8+delta)=1-delta>=0,

proving (3) for every actual root owner without bounded enumeration.

## Joint selected-union budget and remaining scope

The earlier R/T/W increment is1 and (1) has increment2-D/2.
Combining each disjoint NEW receipt once gives

    Phi(H+O)-Phi(H3)=4-D/2-delta.                (5)

The known zero-repair H3 ledger is Phi(H3)=h+33 for these two
widths and root breadth6. Count that old inventory ONCE, not once
per consumer. Then

    Phi(H+O)=h+37-D/2-delta>=h/2+34.             (6)

Equation (6) is a joint bound for this explicitly selected union and
does not reassign H3's reserve to any other return. It does not imply
that all later additions have nonnegative marginals. The current
relative increment (5) may still be negative, and complete existence
is not asserted. Further closure, overlapping return groups, other
z-owner directions, arbitrary full-family allocation, the global5/6
improvement and rectangular-grid triple equality remain open.

## Verification scope

Run `PYTHONDONTWRITEBYTECODE=1 python3 develop/check_secondary_ten_short_return_root_compensation.py`.
The final exact-set controls pass 875 endpoint-disjoint U roles, including
772 forbidden early tips and 103 equalities of complete normalized original
records, and exclude 16 rotor placements. They check 1977 complete new
tile/event sets across all six frontier profiles, 1159 collisions and four
large-dimension controls. The existing Q-to-P bottom event is explicitly
checked before and after every legal receipt control; it is never new.
These are finite checks of the general argument, not its proof boundary.

`formal/SubQuorum/SecondaryTenShortReturnRootCompensation.lean` verifies
13 local theorems in 16 explicit declarations: every early-support U/rotor
contradiction from its continuous stem/bar/fork data, terminal row30 from
the complete-owner witness, parity and bar frontiers, and the resulting
marginal and single-baseline absolute budget. Lean4.33.0 and every individual
axiom audit pass without warnings, sorry or native evaluation. The adapter
from complete original U/rotor records to these witnesses, exact far-frontier
geometry and source-labelled receipt sets remain written proofs.

Independent review of this theorem, the short-return dependency and the
full recursive source constructors completed ACCEPT on task
869ec698-79c3-4567-8474-3f33a12fdb32, original stream92280.
Its full response exactly matches the terminal receipt. The row-local bar
emptiness above is made explicit following that review. Terminal row30
uses complete extendibility and is not implied by endpoint disjointness
of a partial owner alone. See the companion validation record.
