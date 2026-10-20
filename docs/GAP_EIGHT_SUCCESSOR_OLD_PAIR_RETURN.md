# A necessary return-length identity for old-pair reuse

21 October 2026. This note isolates an obstruction to crediting a tight-band
positive successor. It proves a necessary condition for reuse by the old P
channel. It does not yet prove a new simultaneous activation injection.

## Statement and proof

Use the complete original U/rotor hypotheses and normalization of
[the occupied-band theorem](TIGHT_GAP_EIGHT_BAND_COMPENSATION.md), with
omega=V-4. The fixed transverse source is

    C=U(V,h,f), C(r,c)=(c+1,h+2-r).

Suppose the actual consumer of y=(V-1,h) is the negative upward-bar
terminal U, and the actual consumer of its forced support z=(V,h) is
the positive upward-bar terminal

    T=U(tau,j,ell), T(r,c)=(V+1-c,r+h-j).

The preceding classification gives j>=g+2>=nu+4. If this very terminal
occurrence is also an old P target, then necessarily **f=j+2**.

To prove this, the accepted old P recipient frame is (c+2,r+2). Equating
its transported whole-source frame to T forces the old positive producer
chart to be F(r,c)=(V+3-r,c+h-j-2). The
[old pair theorem, Section 2](PAIR_GATE_TRANSFERS_AND_PROTECTED_DEFECTS.md)
requires a third original source in that producer's chart, with incident
length hp>=j+2. Transporting it gives

    Cprime=U(Z,hp,fp), Cprime(r,c)=(V+2-c,h+hp-j-r).

Its near leg contains (V+1,h+1): use intrinsic (hp-j-1,1), which is a
bar endpoint if hp=j+2 and otherwise a near-leg endpoint. The same point
is C(1,V). Unique original endpoint ownership therefore forces Cprime
and C to be the SAME original source. A different-owner collision argument
alone would miss this possibility.

On physical row V+1, C's endpoint interval is exactly [h+2-f,h+2].
Cprime's endpoint interval there is exactly [h-j,h+hp-j]; only its
near leg and adjacent bar points can lie on this row, since Z>=6.
Equality of the original endpoint sets equates both ends of these intervals.
The upper ends give hp=j+2; the lower ends then give f=j+2. This uses
original endpoint sets, without any assumption on additional sources.

Consequently **f!=j+2 excludes old P reuse**. In particular f<=nu+4
excludes it, because j+2>=nu+6. This excludes one old channel only;
global reconstruction and joint nonreuse against every other target class
must still be proved before these activations enter the total ledger.

## A checked local matched pattern

The following eight sources have pairwise disjoint original endpoint sets.
Parameters and affine symmetries use the repository convention: reflect the
intrinsic coordinates, then transpose if specified, then translate.

| Role | (width, near, far) | (transpose, flip-row, flip-column) | Offset |
|---|---|---|---|
| A | (22,4,4) | (false,false,false) | (0,0) |
| B | (8,8,4) | (false,true,false) | (11,1) |
| C | (18,18,10) | (true,true,false) | (1,20) |
| X | (6,10,4) | (true,false,false) | (2,3) |
| E | (14,4,4) | (true,true,false) | (2,18) |
| U | (6,6,4) | (true,false,true) | (18,12) |
| T | (8,8,4) | (true,false,true) | (19,10) |
| F | (14,4,4) | (false,true,false) | (21,8) |

Here V=h=18, nu=4, g=6, j=8 and f=10=j+2. The forced old P third
source is exactly C, including its original supports and matching, after
exchanging its legs: Cprime=U(18,10,18), map (20-c,20-r).
The terminal z=(18,18) has both supports (18,19),(19,18) in C. In F's
chart the old P gate pair (3,2),(3,3) maps to T endpoints (18,10),(18,11),
and the required third-source point (2,2) maps to (19,10), also C-owned.
Thus endpoint disjointness and these local stencils do not exclude the
matched identification.

This is a PARTIAL pattern. The remaining original supports have not been
completed or validated as a complete family. It is not a counterexample to
any complete-family compensation rule or to mu>=0. The outstanding question
is whether a complete extension exists or a further general obstruction
excludes it.

## Verification scope and next step

Run `python3 develop/check_gap_eight_successor_return.py`. Independent
endpoint/support/matching construction checks the partial pattern and finite
controls of the interval argument. The universal argument is the written
proof above; finite controls do not replace it. The standalone Lean file
`formal/SubQuorum/GapEightSuccessorReturn.lean` checks the coordinate-level
endpoint implication and return-length identity. It does not formalize the
old-channel geometry or a global injection. No independent written audit has
yet been obtained for this note. No numerical compensation gain is claimed.
