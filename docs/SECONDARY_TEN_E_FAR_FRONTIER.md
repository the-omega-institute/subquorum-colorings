# Exact old-chain frontier for arbitrary internal E far legs

22 October 2026. Retain every original endpoint, support and matching of
the full H3 chain defined in
[the left-chain exterior theorem](SECONDARY_TEN_LEFT_CHAIN_EXTERIOR.md).
The even dimensions satisfy w_j>=12,z_j>=24, the anchors a_j are odd,
the offsets s_j are even, and

    a_(j+1)=a_j+z_j-6, s_(j+1)=s_j-w_(j+1)-12.

This note removes the E far-leg cutoff for ONE original against H3.
It does not add arbitrary other new owners. The subsequent
[both-far compensation theorem](SECONDARY_TEN_BOTH_FAR_COMPENSATION.md)
uses this frontier and the paired width coupling to prove simultaneous
compensation for arbitrary selected incident-ten pairs.

## Statement

Fix an internal index i>=1 and a full original

    R=U(L,10,f), chart(r,c)=(a_i-11+r,C_i+1-c),
    C_i=s_i+w_i+13, L>=w_i+20, f>=4, L,f even.

The width condition is necessary whenever R is an actual E owner with
incident ten: the actual-owner coupling gives L>=w_i+M+14 with M>=6.
For the present theorem, completeness is unnecessary; R need only be
endpoint-disjoint from H3. Its even far column and terminal row are

    F=C_i+1-L<=s_i-6, b=a_i-11+f.

Let k>i be the first index with F>=s_k-4, if it exists. The following
table is exact. The deduction d is defined only on the legal rows.

| Far column | Endpoint-disjoint iff | Deduction d |
|---|---|---|
| No k | Every even f>=4 | 0 |
| F=s_k-4 | b<=a_k-3 | 0 |
| F=s_k-2 | b<=a_k-3 | 1 if b=a_k-3, otherwise 0 |
| F=s_k | b<=a_k-5 | 2 if b is a_k-7 or a_k-5, otherwise 0 |
| s_k+2<=F<=s_(k-1)-6 | b<=a_k-9 | 1 if b=a_k-9, otherwise 0 |

For every legal R,

    Phi(H3 union {R})-Phi(H3)=1-d>=-1.                 (1)

The minimum -1 occurs exactly in the third finite-contact row with
b in {a_k-7,a_k-5}. It is attained by endpoint-disjoint originals.
These witnesses need not admit a complete extension. A negative R
marginal neither refutes a joint-pair compensation rule nor the global
target inequality.

## First-contact proof

Every old block, including its P,Z,X originals, has minimum endpoint
column s_j-4. The far strip of R uses the physical tile column {F,F+1}.
For j<=i, F<=s_i-6 puts that tile strictly to the left of every old
endpoint. If k exists, minimality and even parity give

    s_k-4<=F<=s_(k-1)-6.

Every block before k is separated by the same tile-column argument.
The R bar is above its own P bar and above all later blocks; earlier
blocks are to its right. Its fixed near leg has the same four-full-
tile/eight-event receipt as in the short-pair theorem. Extending its
far leg therefore changes only the strip at {F,F+1}.

Substitution in the full original charts of block k gives the first
same-column endpoint and the relevant partner-column profile:

| F | First old endpoint in column F | Relevant endpoints at F+1 |
|---|---|---|
| s_k-4 | X_k at row a_k-2 | None before the legal terminal tile |
| s_k-2 | Z_k at row a_k-2 | Z_k starts at row a_k-4 |
| s_k | Z_k at row a_k-3 | P_k far stem at rows a_k-8,...,a_k-4 |
| F>=s_k+2 | P_k bar at row a_k-8 | None above that bar |

R occupies every far-column row from a_i-11 through b. Its start is
above each displayed first endpoint. Avoiding that endpoint, with b
even, gives exactly the legal bounds in the statement. In particular
the last case is blocked by the P BAR, even when another old stem
continues farther down. Treating that stem as the first obstacle would
give an incorrect legal depth.

These bounds are sufficient as well. R's bar and near leg have already
been separated; earlier blocks cannot meet the far tile column. All
legal terminals satisfy b<=a_k-3. Every block after k starts at row at
least a_(k+1)-8>=a_k+10, below this terminal and its physical tile.
There is no later block when k is last. If k does not exist, column
separation excludes every old endpoint and intratile receipt for any f.
This proves the exact collision table without a depth or chain cutoff.

## Exact physical receipts

All coordinates below are absolute. A physical tile is specified by
its even top-left coordinate; rows increase downward. Old supports stay
excluded from directed events even if another owner consumes them.

The near receipt has four new mixed full tiles and eight new directed
events, hence signed value zero. R has charge -1 and adds negative
mass one. The far receipt is disjoint from these near tiles.

At F=s_k-4, even the last legal terminal b=a_k-3 creates no event:
R's downward target is its original axial support, and X_k's upward
target is X_k's original axial support. There is no mixed full tile.

At F=s_k-2, only b=a_k-3 activates a receipt. The tile with top-left
(a_k-3,F) has R at its upper-left cell and Z_k at the other three.
The two horizontal directions at row b and the upward Z_k direction
from (b+1,F) survive. R's downward direction is excluded by its axial
support. Thus there is one new mixed full tile and three new events,
with signed value -1. Earlier even terminals create no receipt.

At F=s_k, activation occurs at b=a_k-7 or a_k-5. Write

    b=a_k-7+2h, h in {0,1}.

The new mixed full tiles have top-left (a_k-7,F) when h=1 and none
when h=0. For each t=0,...,h the events are exactly

    R:(a_k-7+2t,F) -> P_k:(a_k-7+2t,F+1),
    P_k:(a_k-7+2t,F+1) -> R:(a_k-7+2t,F).

At odd rows the horizontal directions target original supports of the
respective originals. The entry tile, where P_k first occupies its
lower-right cell, has no event or full tile. The terminal tile has the
two displayed events and lacks R's lower-left cell. Therefore the far
receipt has h new mixed full tiles and 2h+2 events, signed value -2.
All earlier terminals have zero far receipt. Z_k in the same column
prevents any continuation to X_k or another later profile.

In the remaining column range only b=a_k-9 activates a receipt. There
is a single upward event P_k:(b+1,F)->R:(b,F); R's reverse direction
targets its original axial support. The partner cells are absent, so
there is no new full tile. The signed value is -1.

These profiles exhaust the legal far strip. Adding its signed value
to the near value zero and mass one proves (1). Every mixed full tile
and owner-labelled event is counted as a physical set element once.
No old-prefix reserve or other new owner's negative mass is used.

## A sharp local witness and the remaining simultaneous problem

Take a_0=31,s_0=0, three blocks with all w_j=12,z_j=24 and root
breadth six. At i=1, a_i=49,s_i=-24,C_i=1. Let

    R=U(50,10,22), chart(r,c)=(38+r,2-c).

Then F=-48=s_2 and b=60=a_2-7. R is endpoint-disjoint from H3 and
has exact increment -1. Its actual forced t partner, if it exists,
has left incident four and width at most 24 by the coupling inequality.
The witness alone is not a complete configuration or a counterexample
to simultaneous pair gain >=4m.

The frontier theorem proves that a long R can lose at most two units
to the OLD chain. A discovery run checked 18,111 marginals against
H3 plus selected new T owners with minimum -1; this finite observation
is not a proof of joint compensation. The subsequent both-far theorem
proves the necessary nonstacking using the coupled frontiers and gives
an aligned-bar argument separating entire pairs. Its general proof and
separate validation, rather than this discovery run, establish that
selected-union strengthening.

The companion verifier checks exact collision decisions and complete
mixed-full-tile and owner-labelled-event SETS at every frontier phase,
translated and nonuniform chains, and large far depths. The standalone
Lean module checks the frontier parity arithmetic, conditional receipt
identity and sharp lower bound. Full original geometric exhaustion is
the written proof above; it is not claimed to be fully formalized.

Validation passed 19,712 collision decisions and 10,482 exact full/event
set comparisons, with all four frontier phases and far depths up to 2000.
Local standalone Lean passed 18 declarations, including 17 theorems;
individual axiom reports contain only ordinary axioms, with no warnings,
sorry or native axioms. No independent review of this new frontier theorem
has been submitted or accepted. The earlier arbitrary-t-far audit continues
under its own original task; it does not review this new note.
See the [validation record](../output/secondary-ten-e-far-frontier-validation.json).

The global 5/6 improvement, full-family allocation and rectangular-grid
triple equality remain open. The submitted 11 October manuscript stays
unchanged.
