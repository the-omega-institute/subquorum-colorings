# Simultaneous internal compensation with both far legs arbitrary

22 October 2026. This removes BOTH far-leg cutoffs from the
[internal pair theorem](SECONDARY_TEN_INTERNAL_LONG_PAIR.md), retaining
incident ten at E and the full-original H3 chain. The proof uses the
[actual-owner coupling](SECONDARY_TEN_INTERNAL_SHORT_PAIR.md), the
[old T frontier](SECONDARY_TEN_LEFT_CHAIN_EXTERIOR.md), and the
[old E frontier](SECONDARY_TEN_E_FAR_FRONTIER.md). The latter is a
new written dependency, not a previously independently accepted theorem.

## Hypotheses and theorem

Retain every endpoint, original support and matching in H3, with even
w_j>=12,z_j>=24, odd a_0, even s_0, even root breadth at least six,

    a_(j+1)=a_j+z_j-6, s_(j+1)=s_j-w_(j+1)-12.

Let J be any subset of the internal indices. At each i in J, choose

    R_i=U(L_i,10,f_i), chart(a_i-11+r,C_i+1-c),
    T_i=U(M_i,4,g_i), chart(a_i-8+r,s_i+1-c),
    C_i=s_i+w_i+13,
    L_i=w_i+M_i+14+q_i,
    M_i>=6, f_i,g_i>=4, q_i>=0, all even.

Assume that every chosen original is endpoint-disjoint from H3 and from
every other chosen original. Their supports remain immutable in the
event definition. No complete extension is required for this selected-
union theorem. In particular it applies to the actual owners at any
selected incident-ten E blocks in a complete even-U/rotor extension:
the coupling and distinctness theorem supplies these hypotheses.

Write

    F_i=s_i-M_i-q_i, G_i=s_i+1-M_i,
    b_i=a_i-11+f_i, y_i=a_i-8+g_i.

Here F_i,b_i are even and G_i,y_i are odd. Let d_i be the old E
deduction in the E-frontier table, and delta_i the old T deduction.
Thus 0<=d_i<=2, delta_i is zero or one, and delta_i=1 forces M_i>=28.
Define epsilon_i=1 exactly when q_i=0 and b_i<y_i; otherwise zero.
Define chi_i=1 exactly when ALL the following hold:

    q_i=0;
    k>i is the first old E-frontier block;
    F_i=s_k-4, b_i=a_k-3, y_i>=a_k-2.

Set chi_i=0 when no such k exists. Then the selected-union increment is
exactly

    DeltaPhi = sum_(i in J)
      (M_i-d_i-delta_i-2epsilon_i+2chi_i) >=4|J|.      (1)

The FULL endpoint tile footprints of distinct pairs are automatically
disjoint, although each of f_i,g_i can be arbitrarily large. No
disjointness of these tile footprints is assumed. It follows from the
width coupling and actual endpoint disjointness, as proved below.

Only NEW increments relative to the single H3 inventory are counted.
The theorem does not allocate the remaining originals' losses or prove
a global 5/6 improvement, arbitrary-grid catalogue exhaustion or the
rectangular-grid triple equality. Deeper E incident legs remain open.

## Exact one-pair ledger

Suppress i. Separately against H3, the two frontier theorems give

    DeltaPhi(R|H3)=1-d,
    DeltaPhi(T|H3)=M-1-delta.                         (2)

All mixed full tiles and directed events here retain their original
physical coordinates and owner labels. Neither receipt uses another
new owner's negative mass or an old-prefix reserve.

R's bar is an entire row of single-owner physical full tiles: its
first row a-11 is even, and its column interval [F,C] has even/odd
ends. Its short near leg is far to the right of T. T's bar/near leg
cannot meet R's far tile column except at T's far edge. Consequently
the ONLY possible mutual endpoint-tile contact is between their far
stems. If q>=2, G>=F+3 puts those stems in distinct physical tile
columns, so there is no mutual event or joint full tile.

For q=0, G=F+1. R occupies [a-11,b] in the left column F, and T
occupies [a-8,y] in the right column F+1. The entry tile at even row
a-9 has only T's lower-right cell. Its horizontal directions target
original supports, so it has no mutual event or new full tile.

Put

    A={r even: a-7<=r<=min(b,y-1)},
    B={r even: a-7<=r<=min(b-2,y-1)}.

For every r in A there are exactly two mutual directed events:

    R:(r,F)->T:(r,F+1), T:(r,F+1)->R:(r,F).

At odd rows both targets are original supports of the respective
owners. The mutual two-owner full tiles have top-left (r,F) for
r in B. These physical tiles belong to neither separate old receipt.
Because b is even, y is odd, and f,g>=4,

    |A|-|B| = [b<y] = epsilon.

Thus their mutual two-owner signed contribution is -2epsilon for
arbitrary f and g, independently of the number of shared full tiles.

There is one possible additional mixed full tile involving H3,R,T.
R and T must each have an endpoint there, so q=0 and the tile is in
their shared far column. Every interior tile with two R endpoints and
two T endpoints is already in B. The entry tile lacks its upper-right
endpoint in H3 as well: F+1<=s_i-5 separates it from the own and
earlier old blocks, and every later block starts below the entry.
After T's far terminal, its last tile already contains both right
endpoints; no half-terminal in the opposite parity creates another case.

The only remaining possibility is R's terminal tile with upper-left R,
both right cells T, and lower-left old. In the E frontier table:

- At F=s_k-4, the first old left endpoint is X_k at row a_k-2.
  This makes the tile full exactly when b=a_k-3 and y>=a_k-2.
  Its top-left is (a_k-3,F). It is not full in either separate old
  receipt, since that receipt lacks respectively the two T cells or
  the R cell. This is precisely chi=1.
- At F=s_k-2, a lower-left Z endpoint can first occur when b=a_k-3.
  But T's same first frontier has G=s_k-1 and requires y<=a_k-6.
  T cannot occupy the right cells in this terminal tile.
- At F=s_k, R's legal bound b<=a_k-5 stops above the first same-
  column old Z endpoint at a_k-3. There is no lower-left old endpoint.
- At F>=s_k+2, the first old left endpoint is P's bar at a_k-8.
  Its terminal candidate b=a_k-9 again has T bound y<=a_k-10,
  excluding right-cell occupation. Without a frontier there are no
  old endpoints in the shared tile column.

The first frontiers of R and T are the SAME k in these q=0 cases:
F>=s_k-4 iff G>=s_k-3. The additional triple-owner tile contributes
2chi. Events remain pairwise directed endpoint adjacencies; a third
owner cannot create a further event beyond the separate and mutual
event sets. Adding (2), the mutual receipt and this tile proves the
exact one-pair expression in (1).

## Why the two deductions cannot stack

We prove the decisive inequality

    d+2epsilon<=2.                                   (3)

If q>=2 then epsilon=0 and d<=2. If q=0 and d=0 the conclusion is
immediate. For q=0 and d>0, the legal R/T frontiers are coupled:

| F | R deduction active only at | T must satisfy |
|---|---|---|
| s_k-2 | d=1, b=a_k-3 | y<=a_k-6 |
| s_k | d=2, b=a_k-7 or a_k-5 | y<=a_k-10 |
| F>=s_k+2 | d=1, b=a_k-9 | y<=a_k-10 |

In EVERY row y<b, so epsilon=0. The X column has no R deduction.
This proves (3) in all cases without a dimension cutoff.

Since chi>=0, one pair's exact increment is at least M-2-delta.
For delta=0 use M>=6 to obtain at least four. For delta=1 the T
frontier identity gives M=s_i-s_k+4>=28, so the increment is at
least25. The exceptional old T debit is paid once from its OWN M-1
mass; it is neither ignored nor charged to a different pair.

The +2chi term is necessary for the exact identity. For example, use
three uniform blocks a_0=31,s_0=0,w_j=12,z_j=24 and i=1. Choose

    M=28,q=0,f=26,g=24, L=54.

Then F=-52=s_2-4,b=64=a_2-3,y=65=a_2-2. Here
d=0,delta=1,epsilon=1,chi=1, so the exact pair increment is27,
rather than25. The triple-owner full tile has top-left (64,-52).
This is an endpoint-disjoint partial witness, not a complete-extension
existence claim.

## Automatic separation of arbitrary selected pairs

The width relation gives

    F_j=G_j-1-q_j<=G_j-1, s_j+1<C_j.

Thus EVERY endpoint tile column of pair j, including the whole T_j,
is within the tile-column interval of the aligned R_j bar [F_j,C_j].
All its endpoint rows are at least a_j-11. This bar is the crucial
additional guard when both far legs are unbounded.

Take i<j. The R_i bar/near leg and T_i bar/near leg all end at row
at most a_i-1. Since a_j>=a_i+18, their endpoint tiles lie strictly
above the first even R_j bar row a_j-11>=a_i+7. Only either of
pair i's two long far columns can reach pair j's endpoint tiles.

Consider either such continuous far stem, at column x and terminal t.
Its start is above a_j-11. If its physical tile column meets pair j's
footprint, it also meets the R_j bar's tile-column interval. Because
the bar's left end is even and right end odd, this implies

    F_j<=x<=C_j.

If t>=a_j-11, the stem contains the actual R_j bar endpoint
(a_j-11,x), contrary to the assumed endpoint disjointness of these
originals. Therefore t<a_j-11. The first bar row is even, so this
strict bound also separates their PHYSICAL tile rows, whether t is
even (R_i) or odd (T_i). Otherwise their tile columns were separated
already. This argument handles both far stems and all later endpoints,
including T_j, with no imposed far-length bound.

Every two selected pairs therefore have disjoint FULL endpoint tile
footprints. The argument does not require ordering by widths, nesting
of the far columns, support closure, or a separately postulated allocation.

## Exact simultaneous accounting and verification scope

Every newly full mixed tile and every new intratile directed event
contains a new endpoint, so lies in its pair's endpoint tile footprint.
No two pairs can share such a physical tile or event. Each new original's
immutable charge contributes once. New receipts are therefore the
disjoint union of the one-pair receipts, and the exact identity and
lower bound (1) follow. Shared old owners do not re-credit their mass
or duplicate their old events. Only changes relative to H3 are added.

The companion verifier compares the complete predicted physical full-tile
and owner-labelled event SETS, including the triple-owner correction,
then checks automatic pair-footprint separation and exact simultaneous
addition for endpoint-disjoint selected batches. The scoped Lean module
checks parity/column gates, aligned-bar separation, nonstacking and the
conditional scalar/list ledger. General source-chart exhaustion and actual-
owner normalization remain written mathematical arguments.

Validation passed 11,568 exact one-pair full/event SET comparisons,
including 12 activated triple-owner corrections and all frontier phases;
60 endpoint-disjoint batches of four or five pairs; and two/five/eleven-
pair groups with both far legs around 2000 and exact gains 2326,6816,19230.
The explicit triple-owner witness has gain27 and the old-loss sharp
witness gain4. Local standalone Lean passed29declarations/21theorems
with individual ordinary-axiom reports and no warnings/sorry/native axioms
in the final run. See the
[validation record](../output/secondary-ten-both-far-compensation-validation.json).

The previously accepted short-pair audit and active arbitrary-t-far
audit do not cover this new theorem or its new E-frontier dependency.
No independent ACCEPT is claimed without a separate completed review.
The submitted 11 October manuscript and primary star-forming results
are preserved; full-family allocation and the global grid targets remain
open.

A subsequent [sharpness construction](SECONDARY_TEN_BOTH_FAR_SHARPNESS.md)
attains4m for arbitrary pair count and arbitrarily long BOTH far legs
under these selected-union hypotheses. It does not assert complete
extendibility. That corollary was written after this theorem's independent
review input and has its own explicit verification scope.
