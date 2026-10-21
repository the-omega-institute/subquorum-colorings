# Arbitrary left consumers against the entire renewed-support chain

21 October 2026. This continues the full-original H3 construction in
[the renewed-support note](SECONDARY_TEN_RENEWED_SUPPORT_ESCAPE.md) and
the [single-block classification](SECONDARY_TEN_ARBITRARY_T_CONSUMERS.md).
It treats one arbitrary left-frame consumer against ALL old blocks, not
just the old block owning its forced support. No nesting of its bar or
bound on either leg length is assumed.

## The exact exterior theorem

Take any H3 chain with n>=1, independent even w_j>=12,z_j>=24, odd a_0,
even s_0 and even root breadth h>=6. Retain every original endpoint,
support and matching set. Thus

    a_(j+1)=a_j+z_j-6,  s_(j+1)=s_j-w_(j+1)-12.

Fix an index0<=i<n and integers H,d,f ALL EVEN, with H>=6 and d,f>=4.
Only this even domain defines legal matched U originals: odd incident or
far leg depths are excluded, since the prescribed matching would not
pair every terminal. Consider the FULL original

    T=U(H,d,f), chart(a_i-4-d+r,s_i+1-c).

Its far column and terminal row are the odd absolute coordinates

    ell=s_i+1-H,  y=a_i-4-d+f.

Define k to be the FIRST index j>i such that ell>=s_j-3, if one exists.
If no such k exists, T is endpoint-disjoint from H3 for every f. If k
exists, the following table is an exact classification:

| Far column | Endpoint-disjoint iff | Extra signed contribution beyond own P_i^0 receipt |
|---|---|---|
| ell=s_k-3 | y<=a_k | -1 if y>=a_k-2, otherwise 0 |
| ell=s_k-1 | y<=a_k-6 | 0 |
| s_k+1<=ell<=s_(k-1)-5 | y<=a_k-10 | 0 |

Only odd ell are considered. The three rows exhaust the interval
[s_k-3,s_(k-1)-5]. For k=i+1 its upper bound still follows from H>=6.
Without a k the extra contribution is 0. Consequently every legal T has

    Phi(H3 union {T})-Phi(H3)=H-1-delta,

where delta=1 precisely in the first row with y in{a_k-2,a_k}, and
delta=0 otherwise. In particular this gain is at least5, with equality
exactly when H=6. In the exceptional case H=s_i-s_k+4>=28, so its
gain is at least26. The isolated-block left-frame gain H-1 can fail by
exactly1 against the full old chain, but its positivity survives.

This theorem neither adds several consumers nor asserts monotonicity under
further extension. Consumer-consumer contact is a separate term. The global
5/6 improvement and rectangular-grid triple equality remain open.

## First-contact classification without a finite cutoff

Each old block, including its P^0,Z,X, has no endpoint to the left of
the even column s_j-4. The root is to the right of every relevant near
column. Earlier old blocks, j<=i, therefore have no contact with T's far
stem: ell<=s_i-5 and the closest old column s_i-4 lies in the NEXT physical
tile column. The near stem has exactly the two-full-tile/four-event receipt
against its own P_i^0 from the single-block proof; earlier blocks lie to
its right and later blocks start below its FIXED NEAR terminal. The bar lies above
all later blocks and to the left of all earlier ones. It has no additional
old contact.

Suppose k exists. Minimality gives ell<s_(k-1)-3 and hence, by parity,
ell<=s_(k-1)-5. All blocks before k have minimum endpoint column at least
s_(k-1)-4, again across a physical tile boundary. This excludes both
events and mixed full tiles, even if those blocks have long stems.

In block k, direct substitution in the full source charts gives:

- At ell=s_k-3, the first endpoint in that column is X_k's bar at row
  a_k+1. Its even partner column s_k-4 has X_k's far stem starting at
  row a_k-2. There are no earlier endpoints in either column.
- At ell=s_k-1, the first endpoint is Z_k at row a_k-4. Its partner
  column s_k-2 has no endpoint above that row.
- At any remaining allowed odd ell, P_k^0's bar gives the first endpoint
  at row a_k-8. Its partner column ell-1 has no endpoint ABOVE that row.
  At ell>=s_k+3 it can have a P^0 endpoint in that SAME row, which is
  irrelevant under the legal bound y<=a_k-10. At ell=s_k+1 the partner
  endpoints start lower. The upper bound
  ell<=s_(k-1)-5=s_k+w_k+7 lies strictly inside this P^0 bar's breadth.

The far stem starts above every one of these rows. It contains every row
up to y, with y odd. Avoiding the displayed first endpoint is equivalent
to the bounds in the table. These are both necessary and sufficient:
first impose the respective legal bound, which always gives y<=a_k.
If k<n-1, every block j>k starts at row at least

    a_(k+1)-8>=a_k+10,

and hence strictly below this legal far terminal. If k=n-1 there is no
later block. Long V_k stems start in other columns and cannot create an
earlier frontier. Without the legal bound one cannot compare arbitrary
far-terminal rows to later blocks, and no such comparison is used.
If no k exists, ell<=s_(n-1)-5 puts ALL old endpoint columns across the
next tile boundary or farther right; column separation alone proves
disjointness and no far contact for any f, however large.

## Exact extra physical sets and original-support exclusions

The only nonzero extra receipt occurs at ell=s_k-3 with y>=a_k-2.
In these activated cases, write

    y=a_k-2+2m,  m in{0,1}.

The new far-contact mixed full tiles have lower-left minima

    (a_k-1,s_k-4), if m=1; none if m=0.

The surviving directed events are exactly

    X_k:(a_k-2+2j,s_k-4) -> T:(a_k-2+2j,s_k-3), j=0,...,m,
    T:(a_k-1,s_k-3) -> X_k:(a_k-1,s_k-4), if m=1.

Thus DeltaF_extra=m and DeltaE_extra=2m+1. Their signed sum is -1.
For X_k the rightward target is excluded on its odd intrinsic stem rows
and survives on its even intrinsic rows. For T the leftward target is
excluded on its even intrinsic far-leg rows and survives on the odd
ones. Since the two bar rows are odd/even in the absolute frame, the
vertical adjacency from y=a_k to X_k's row a_k+1 crosses a tile boundary.
No additional direction survives there. The upper partial tile is not full.

Below this activation threshold there is no contact. In the other two
column cases, the legal far endpoint stops too early for any partner-column
endpoint in its physical tile rows. Hence no extra tile or event
is missed. All these far receipts lie strictly below the own-P_i^0 near
receipt, so their physical tiles and owner-labelled events are disjoint.

T has charge1-H and adds no positive owner. Add its negative mass H-1
ONCE to the four-event/two-full-tile near receipt and the displayed far
receipt. This proves the exact formula. The exceptional width identity
H=s_i-s_k+4 and s_i-s_k>=24 prove the stronger exceptional lower bound.
The general minimum and equality statement follow immediately.

## Validation scope and next question

The argument above is an ordinary proof using the full unbounded source
charts. Its companion verifier checks exact collision decisions, physical
mixed full tile sets and owner-labelled directed event sets; finite controls
do not replace the proof. The standalone
[Lean module](../formal/SubQuorum/SecondaryTenLeftChainExterior.lean)
passed locally:24declarations,18theorems, every declaration audited with
ordinary axioms only and no warnings. It covers explicit frontier endpoints
and collisions, strip and parity bounds, and the conditional gain arithmetic.
The complete geometric partition remains an ordinary proof. The exact-set
validator has passed130302collision decisions and64164legal exact-set
controls through24blocks. The initial independent review returned REVISE
for explicit even-domain and frontier/separation prose; those repairs are
applied above, with no change to the all-even formulas. The full corrected
note received follow-up ACCEPT; optional activation/near-terminal wording
clarifications were applied. See the
[separate status record](../output/secondary-ten-left-chain-validation.json).
This exterior theorem has its own completed written review, separate
from the earlier accepted single-block/nested review.

Next resolve interactions among arbitrary actual left consumers and the
right-frame alternatives. The one-consumer theorem alone does not bound
the additional signed contribution between those new originals. The
submitted11October manuscript and primary star-forming results are unchanged.
