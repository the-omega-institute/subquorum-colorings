# A sharp six-unit bound for arbitrary actual staircases

22 October 2026. Owner: Wenlin Zhang and Haobo Ma. Status: general written
proof; exact physical-set controls and scoped Lean are recorded separately.
Use precisely the model, retained originals and all-parameter hypotheses of
[the arbitrary-actual-staircase theorem](SECONDARY_TEN_ROOT_ACTUAL_STAIRCASE.md).
In particular, every original is a full even U or standard rotor by explicit
model assumption; arbitrary-grid exhaustion is not asserted. Keep the whole
H3 chain and the specified B,R,A. All endpoints of different originals are
disjoint. Four staircase originals J_i have charts

    J_i=U(H_i,D_i,G_i),
    (r,c) -> (a-10-i+c,P-D_i+r), P=s+u+12,

with all dimensions even, H_i>=6,G_i>=4,
D0>=u+L+14, D_i>=D_(i-1)+2, D3<=u+v+22 and H_i<z+i-4.
The retained consumer is A=U(L,4,f) at(a-8+r,s+1-c),
6<=L<=v+10 and4<=f<=z-8. The earlier forced staircase narrows the
necessary A frontier further, but no additional restriction is needed here.

## Theorem

For this single selected union, relative to H3,

    DeltaPhi >= L/2+3 >= 6.                         (1)

The parameter-dependent lower bound L/2+3 is sharp among geometrically
admissible selected unions: an explicit family attains it for every even
u,v>=12, z>=24 and6<=L<=v. The family is not claimed to extend to a
complete configuration. Thus sharpness here is not a global obstruction.

## Only J1 and J2 can have a far-pair receipt

Write b_i=P-D_i and y_i=a-10-i+H_i. The far endpoints of J_i form
the full interval [b_i,b_i+G_i] on row y_i. Its two-column bar lies at
[b_i,b_i+1] and includes both columns on row y_i-1.
The starts satisfy b0>b1>b2>b3, with gaps at least2.

The preceding proof shows that, outside the three fixed upper tile rows,
any intratile interaction between staircase owners must be between far
rows in one physical tile row. Equal-phase rows cannot interact. If J_i
is the upper owner and J_j the lower owner, then

    i is odd, j is even, y_j=y_i+1.

Suppose their far intervals overlap and b_i<=b_j. Overlap implies
b_j<=b_i+G_i, so (y_i,b_j) is an upper far endpoint. It is also a
lower-owner bar endpoint because y_i=y_j-1. This contradicts endpoint
disjointness. Therefore b_i>b_j, equivalently i<j. With indices0..3,
the only odd i and even j satisfying i<j are i1,j2.

This argument excludes the other three opposite-phase pairs for all
heights and far lengths. It also excludes a contact with the lower bar's
corner: the first two lower columns cannot belong to the upper interval.
The earlier per-pair interval calculation gives signed receipt at least-1
for the remaining pair J1/J2. Thus the entire staircase-pair receipt is
at least-1, improving the earlier conservative bound-4.

## A boundary debit and a P1 contact cannot use the same odd owner

Let t=a+z-15. A lower P1 contact requires the far row to be exactly t.
An A->J boundary debit can occur only while the A far stem or its lower
bar is present at that far row. Its latest row is

    a-8+f <= a+z-16 = t-1.

Only J1 and J3 can have either kind of receipt. If m counts the owners
touching the P1 band and q counts the A boundary debits, their owner sets
are disjoint, and each owner contributes at most one such debit. Hence

    m+q <= 2.                                      (2)

Let g be the sum of G_i over the m lower contacts. The exact P1 signed
receipt remains -g/2-m. All these intervals lie in the single common
column interval [b3,s], so

    0 <= g <= s-b3=D3-u-12.                        (3)

For m0 this follows from g0 and D3>=u+L+20. For m1 it follows by
containment. For m2, disjointness gives the stronger bound
g<=D3-u-14, although that strengthening is not needed for (1).
The same common interval is never assigned separately to the two owners.

## Combined receipt partition

The upper ledger and remaining-boundary classification are unchanged:

    DeltaPhi=u/2+v+L/2+22-D3/2+eta.

The neutral old rotor corner has two events paid by its one distinct
full tile. Every other unassigned mixed full tile contributes nonnegative
credit. The staircase-pair tiles contain only J1/J2 endpoints, P1 tiles
contain P1 endpoints, and the neutral corner contains three old rotor
endpoints. These are distinct physical tiles outside the upper rows.
Events have distinct owner pairs or disjoint row groups. Source charges
were added exactly once in the inherited upper ledger.

Consequently, using (2) and (3),

    eta >= -1-g/2-m-q
        >= -g/2-3
        >= -(D3-u-12)/2-3.

Substituting gives

    DeltaPhi >= u+v+L/2+25-D3
             >= L/2+3 >= 6,

as D3<=u+v+22 and L>=6. This proves the theorem without a finite
dimension cutoff or replacement of the actual staircase dimensions.

## An unbounded equality family

Take f6, any even6<=L<=v, and choose

    J0: (H,D,G)=(6,u+L+16,4),
    J1: (H,D,G)=(8,u+L+18,6),
    J2: (H,D,G)=(10,u+L+20,4),
    J3: (H,D,G)=(z-2,u+v+22,v+10).                (4)

These choices work for every even u,v>=12,z>=24, any H3 length n>=2,
any allowed root h>=6 and retained R breadth K>=h+2,far g_R>=4.
The starting columns are respectively

    s-L-4, s-L-6, s-L-8, s-v-10.

They are distinct even columns with gaps at least2; the last gap is
v-L+2>=2. Every bar is strictly between B's near stem at s-v-12 and
A's far stem at F=s+1-L. The far rows and terminal columns are

| Owner | Far row | Last column |
|---|---|---|
| J0 | a-4 | s-L |
| J1 | a-3 | s-L |
| J2 | a-2 | s-L-4 |
| J3 | a+z-15 | s |

The first three rays stay strictly left of A while its far stem is present.
They avoid all staircase bars continuing at their row: a continuing bar
to their left stays outside the ray, and a bar to their right has already
ended. The J3 bar lies strictly to the left of all three, and its far ray
is below their endpoints. All bars start below B's lower bar. R lies
strictly to the right. H3's early P0 endpoints are to the right of A;
at the remaining early rows its west rotor and X0 also lie strictly
right of the first three ray endpoints (L>=6). On J3's far row,
those short originals are above it, while V0 starts at column s+2.
At z24, Q0 can still occupy the last physical tile row, but its minimum
column s+3 excludes it by column separation; it is not assumed to be above.
Every later old original starts below that row; P1 is the next row.
These column and row separations prove disjointness from every full old
original and from each other, independent of n,h,K,g_R.

The only far-pair overlap is J1/J2 on rows a-3,a-2, over columns
s-L-6 through s-L-4. Its one full tile and three events give-1.
Only J1 has an A boundary event, giving-1. Only J3 meets P1, with
G3=v+10, signed receipt -(v+10)/2-1. There is no neutral rotor
corner or additional cooperative tile.

For completeness, outside the upper rows the exact new mixed full-tile
minima are

    {(a-3,s-L-6)} union
    {(t,s-v-10+2k): 0<=k<(v+10)/2}.

Only the physical rows with minima a-5,a-3,t contain far endpoints;
other staircase endpoints lie in wholly owned continuing bar tiles.
In row a-5, J0's A-adjacent tile has only three endpoints. In row a-3,
the pair gives the listed single full tile, while J1's A-adjacent tile
also has only three endpoints. In row t, the last tile at column s
has only its two column-s endpoints. These facts exclude omitted
cooperative full tiles and justify equality, not just a lower bound.
The residual event count is3+1+(v+10)+1+(v+10)/2. Thus

    eta = -1-1-(v+10)/2-1 = -v/2-8,
    DeltaPhi=v/2+L/2+11+eta=L/2+3.

For u=v12,z24,L6, the dimensions are
(6,34,4),(8,36,6),(10,38,4),(22,46,22), with exact joint gain6.
This proves sharpness for the selected geometric family, while leaving
all complete-extension and global-family questions open.

## Validation scope and next question

The [exact-set checker](../develop/check_secondary_ten_root_sharp_staircase.py)
reconstructs full original supports, verifies the inherited exact upper
sets and residual classification, excludes all far-pair receipts other
than J1/J2, checks the owner exclusivity in (2), and tests the equality
family under translations, different roots/R and long chains. Its finite
checks supplement the general proof above.

The [scoped Lean source](../formal/SubQuorum/SecondaryTenRootSharpStaircase.lean)
checks the lower-bar collision, phase/index arithmetic, A/P1 row separation,
exclusive debit arithmetic and final sharp ledger. Full event exhaustion,
global component exhaustion and the equality-family geometric adapter remain
written. Independent review of the earlier weaker theorem completed ACCEPT
in task523658e0-2938-4254-b39d-edcc533e5c3c. That verdict does not review
this strengthening. Follow-up30eabe1f-f849-41fd-9df6-276c1603764c also
completed ACCEPT for the sharp theorem and unbounded equality family.
Its complete streamed response equals the terminal API response, observed
gpt_6/pro. The exact residual full-tile list and the Q0 column-separation
clarification above incorporate the review's symbolic checks. The raw
response and terminal record are archived separately.

The next issue is whether additional actual originals can consume these
receipts or source units when overlapping selected groups are combined.
No full-family allocation, global5/6 improvement or rectangular-grid triple
equality follows yet.
