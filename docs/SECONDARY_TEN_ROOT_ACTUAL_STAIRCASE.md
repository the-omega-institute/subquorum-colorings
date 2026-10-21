# Compensation for arbitrary actual staircase dimensions

22 October 2026. Owner: Wenlin Zhang and Haobo Ma. Status: general written
proof with exact physical-set controls; scoped Lean and independent review
have separately recorded scopes. Use the explicit every-original full-U/rotor
model, full H3 chain and specified B,R,A from the accepted
[fourth-owner theorem](SECONDARY_TEN_ROOT_FOURTH_CONSUMER.md).

## Theorem

Retain every H3 original, B=U(u+v+26,z+4,4), arbitrary allowed actual R,
and A=U(L,4,f). Let J_i, i0..3, be ANY endpoint-disjoint staircase
originals in the forced charts

    J_i=U(H_i,D_i,G_i),
    (r,c) -> (a-10-i+c,P-D_i+r), P=s+u+12,

with all parameters even, H_i>=6,G_i>=4. Require the necessary bounds
of the support-staircase lemma: D0>=u+L+14, D_i>=D_(i-1)+2,
D3<=u+v+22, H_i<z+i-4, together with disjointness from every full
retained original. In particular these hypotheses hold for the actual
owners of these four supports in any complete extension of the specified
prefix. There is no requirement that their dimensions equal the explicit
witness family used earlier.

For the SINGLE selected union H3+B+R+A+J0+J1+J2+J3,

    DeltaPhi >= L/2-1 >= 2.                         (1)

This supplies compensation for arbitrary actual staircase dimensions.
It does not assert that arbitrary additional originals have nonnegative
marginals or that the selected union admits a complete extension.
The full-grid catalogue and a full-family allocation are still open.

## Fixed upper receipts

Write b_i=P-D_i, nu=u+L+12. The four immutable charges are -1,+1,-1,+1,
independent of H_i,D_i,G_i, because the terminal column is even and
successive incident rows alternate physical tile phase. Each contributes
one to N+S. These are original charges, never recomputed after supports
are occupied. The preceding exact triple gain is u+v+L+24.

The full mixed tile minima in the three upper physical tile rows are

    (a-9,c),  c=s+2-L,s+4-L,...,P;
    (a-11,c), c=b1,b1+2,...,P;
    (a-13,c), c=b3,b3+2,...,P.

Their counts are nu/2,D1/2+1,D3/2+1. The first row's events number
3nu/2 as in the fourth-owner theorem. In the second tile row, the
vertical J2/J1 directions alternate, giving D1+1 events; B->J1 at
(a-10,C)->(a-10,P) gives one further event. In the third tile row,
B->J3 occurs at every column b3..P, J3->B at odd columns, and B's
horizontal direction at (a-12,C)->(a-12,P) gives one further event.
Their total is3D3/2+2. All opposite directions target original lateral
or axial supports. Cooperative three-owner boundary tiles are included
once in these lists.

These rows have no far endpoints: the earliest far row is a-7, below
all three tile rows. Other bar columns in these rows are wholly owned
by their own J and are separated from the displayed receipts. Thus
their total new signed receipt 2F-E is exactly

    -(nu+D3)/2.

Let eta be the remaining signed receipt in all other physical tile rows.
Adding the four new source units gives the exact identity

    DeltaPhi=u/2+v+L/2+22-D3/2+eta.                 (2)

## Interactions between staircase originals: at most four units of loss

All bars are aligned to distinct physical tile columns [b_i,b_i+1],
because b_i is even and strictly decreases by at least2. All far rows
are below every incident row. A foreign intratile contact involving a
bar and a far ray is possible only where that bar ends in the other
row of the same physical tile; it is therefore also a far-ray contact.
If a bar continues through both tile rows, endpoint-disjointness keeps
the far ray outside its entire two-column tile. Horizontal contacts
across different bar columns cross physical tile boundaries.

Consequently, outside the three upper rows, staircase originals can
interact only at far rows sharing one physical tile row. Even-indexed
far rows are odd; odd-indexed far rows are even. Same-parity indices
therefore have no foreign intratile events or mixed full tiles between
them. There are only four possibly interacting index pairs.

For any such pair, the even row must be above the odd row. Their
overlapping horizontal endpoint interval starts at an even column and
ends at an even column, after removing a lower bar's two columns if
necessary. Both lower-bar columns would also be lower-owner endpoints
in the upper row, so upper foreign endpoints cannot occupy them.
For overlap length ell, an odd integer, at least (ell-1)/2 tiles are
full in this two-owner union. Each overlap column gives at most one
directed event: the upper owner's original lateral/bar support excludes
the downward direction at even columns, and the lower owner's original
lateral support excludes the upward direction at odd columns. The
lower-bar exception is already excluded by endpoint-disjointness.
Thus the pair contributes at least

    2*(ell-1)/2-ell=-1.

An empty overlap contributes0. The sum over all four possible pairs
is at least-4. Every tile counted here is wholly covered by that
particular pair; different pairs cannot claim the same physical tile.

## The lower P1 band: one shared width budget

Put t=a+z-15, an even row, immediately above P1's first bar row t+1.
Only J1 and J3 can reach row t; the height bounds keep J0 and J2
at or above t-1. An original reaching t has its far interval [b_i,E_i],
where E_i=b_i+G_i is even. V0's endpoint at column s+2 forces E_i<=s.
These intervals are endpoint-disjoint and start no farther left than b3.

Let m0,1,2 count these intervals and let g be the sum of their G_i.
Each interval completes exactly G_i/2 mixed tiles with P1 and has
G_i+1 directions P1->J plus G_i/2 odd-column directions J->P1.
Its signed contribution is -G_i/2-1. Therefore the entire lower band
contributes exactly -g/2-m.

If m>=1, the disjoint even-ended intervals must leave at least a
two-column difference between an earlier endpoint and the next start.
The common interval [b3,s] has length s-b3=D3-u-12 in endpoint-distance
units. Hence

    g <= D3-u-12-2*(m-1),
    g/2+m <= (D3-u-12)/2+1.                         (3)

The same upper bound is nonnegative when m0, so it also bounds the
zero debit. Thus the entire P1 band contributes at least
-(D3-u-12)/2-1. This is one shared width budget, not a separate copy
for each far interval. It remains valid when both intervals touch P1.

## All other retained originals: at most two units of loss

Bars cannot meet any further old tile: they lie in tile columns strictly
between B's near stem and A's far stem, and stop above P1. Far rays
are also right of B's near column and left of every R endpoint. Later
blocks lie below the last permitted tile row, except the P1 band already
counted. Every first-block original other than A, P0, the west rotor Z0
and X0 has minimum endpoint column at least s+2.

If A's far stem or its lower bar is present on a far row, its odd
column F=s+1-L is the first obstacle. The far endpoint E must satisfy
E<=F-1. Equality can produce a horizontal direction A->J only for
odd-indexed J, whose far row is even. The reverse targets J's original
axial support. For even-indexed J, A's even-indexed lateral support
also excludes A->J. There is at most one debit for each of J1,J3,
at most2 in total. Any further full tile completed there is positive
credit and is not needed in this bound.

After passing A's far terminal, the following complete row check
exhausts the remaining first-block possibilities:

- On rows through a-4, A is still present, so the preceding case applies.
- On the even row a-3, Z0's first endpoint is the odd column s-1.
  X0 has a tip below, at (a-2,s-4). A vertical contact with that tip
  is excluded in both directions by X0's axial support and J's even
  far lateral support. If E=s-2, exactly two Z0->J directions occur,
  from (a-3,s-1) and (a-2,s-2). The tile(a-3,s-2) is full with
  three Z0 endpoints and one J endpoint, giving credit2 and debit2.
  The reverse J directions target axial/lateral supports. This corner
  is neutral, and endpoint-disjointness permits only one such corner.
- On each row a-2 through a+2, X0 has its even far column s-4 or
  its bar beginning there. After A is passed, E<=s-6, and physical
  tile-column separation excludes all X0/Z0 receipts.
- From row a+3 onward, X0/Z0 are above the entire far tile row.
  V0's even stem column s+2 is still present throughout the allowed
  far-row range. It forces E<=s, in a separate physical tile column.

P0's first column s+1 can occur only on the early rows where A is the
earlier obstacle. The other first-block endpoints are still farther
right. A terminal just above an even far row is in the preceding
physical tile row and supplies no additional intratile event. Thus
the old A debits and neutral Z0 corner exhaust all remaining negative
contributions, yielding a total at least-2.

## Nonreuse and the resulting inequality

Directed events have unique source and target owners, so the upper,
staircase-pair, P1 and old-boundary event groups are disjoint. Full
tiles credited to a staircase pair contain only its two owners. P1
tiles contain P1 endpoints. The neutral Z0 tile contains three Z0
endpoints. They are pairwise disjoint physical receipts, and none is
in the three upper rows. Additional cooperative full tiles are left
uncredited; their contribution is nonnegative. Original charges were
added exactly once. Consequently

    eta >= -4 - (D3-u-12)/2 - 1 - 2.

Insert this into (2):

    DeltaPhi >= u+v+L/2+21-D3
             >= L/2-1 >= 2,

using D3<=u+v+22 and L>=6. This proves (1) for every allowed actual
staircase, without a finite-size cutoff or chosen replacement dimensions.

## Evidence and remaining work

The [exact-set verifier](../develop/check_secondary_ten_root_actual_staircase.py)
checks the upper sets, individual far-pair receipts, shared P1 bound,
old A directions and neutral Z0 tile, with no double assignment. It
includes nonuniform dimensions, both simultaneous P1 contacts, an A
boundary contact and a long-chain control. Finite samples test the
proof; they do not replace its row and interval arguments.

For u=v12,z24,L6,f4, dimensions
(16,32,4),(10,38,4),(20,44,12),(22,46,20) give exact joint gain9.
Thus the earlier bound19 for a specified family cannot be imposed on
arbitrary geometrically admissible staircases. This remains a partial
inventory, not a complete-family or target counterexample.

The [scoped Lean source](../formal/SubQuorum/SecondaryTenRootActualStaircase.lean)
verifies the interval-packing arithmetic, overlap debit,
source-phase arithmetic and final inequality in eleven theorems; geometric/event exhaustion
remains the written proof above. Independent review of this new theorem
is separate from the accepted fourth-owner result. Other forced supports,
interactions with additional originals, arbitrary-grid catalogue exhaustion,
global5/6 improvement and rectangular-grid triple equality remain OPEN.
