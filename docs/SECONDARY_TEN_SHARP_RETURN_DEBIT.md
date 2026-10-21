# A forced-site consumer can return a three-unit debit to the first block

22 October 2026. This follows the
[sharp both-far family](SECONDARY_TEN_BOTH_FAR_SHARPNESS.md).
It gives a general, explicitly verifiable obstruction to inferring a
nonnegative new-owner increment merely from endpoint disjointness and
occupation of a forced support. It does NOT refute the selected-pair
theorem, assert a complete extension, or refute the global target.

## An all-even-parameter family

For any even g>=4 use the sharp construction with m=1,a_0=31,s_0=0:
two old blocks, w_0=w_1=12,z_0=z_1=g+24,root breadth6. Thus

    a_1=g+49, s_1=-24,
    R=U(32,10,g+2), chart(g+38+r,2-c),
    T=U(6,4,g), chart(g+41+r,-23-c).

Let H=H3 union {R,T}. The sharp theorem gives DeltaPhi(H|H3)=4.
Its missing common support is

    x=(2g+41,-30),

with north endpoint in R and east endpoint in T. Consider the FULL U

    W=U(2g+20,4,40), chart(r,c)=(2g+42-c,r-34).       (1)

It contains x as its short-leg terminal, with internal neighbour west.
Its original endpoints are disjoint from ALL of H. Its original charge
is -1. The exact increments are

    DeltaMass=1, DeltaMixedFull=3, DeltaEvents=10,
    DeltaPhi(W|H)=1+2*3-10=-3,
    DeltaPhi(H union {W}|H3)=1.                      (2)

This holds for every even g>=4, with both earlier far legs unbounded.
The new width 2g+20 is essential to the family: a bounded-width search
can miss this return even when it samples large g.

## Endpoint geometry and charge

W's bar is the aligned two-column strip {-34,-33} at rows22,...,2g+41.
Its short leg is row2g+41, columns-34,...,-30, ending at x. Its far
leg is row22, columns-34,...,6. Both legs are contiguous, and the
complete original supports and matching are retained.

All old endpoints have column at least-28, so W's bar and the
nonterminal part of its short leg lie to their left. The selected
R/T far columns are-30,-29; R ends immediately above x and T is
immediately east. Hence W's short leg has no endpoint collision with
H. The far leg lies at row22. The earliest old endpoints are P_0's
bar at row23, while all other old originals begin farther down; the
selected R/T also begin below row22. Thus the entire W is endpoint-
disjoint from H for every g.

The matching count is 2g+41. Its endpoint footprint has g+10 bar
tiles,2short-leg tiles and20far-leg tiles, hence g+32 tiles. Exactly
22original support points lie in that footprint: one per leg tile,
including the terminal axial supports. Its charge is consequently

    (2g+41)+22-2(g+32)=-1.

## Exact new physical sets

At x the new mixed full tile has top-left (2g+40,-30): its upper-left
cell belongs to R, both right cells to T, and lower-left to W.
The ONLY new event in that tile is

    W:x -> R:(2g+40,-30).

W's east target is its original axial support, T's west target is
T's original support, and R's south target is R's original axial
support, so all three of those directions remain excluded. Old R/T
horizontal events at the upper row already existed and are not counted
again. The local site therefore supplies one full tile and one event.

The return far leg lies immediately above P_0's old bar:

    P_0=U(24,10,4), chart(23+r,25-c).

Its bar at row23 occupies columns1,...,24. The new mixed full tiles
have top-left (22,2) and (22,4). The exact surviving directed events are

    P_0:(23,c) -> W:(22,c), c=1,...,6;
    W:(22,c) -> P_0:(23,c), c=2,4,6.

At odd columns W's downward target is an original lateral support.
At physical columns{0,1}, P_0 has no endpoint at column0, so that
tile is not full. At columns{6,7}, W ends at6 and its axial support7
is not an endpoint, so that tile is also not full. There are exactly
two full tiles and nine events in this return region, signed value-5.

W's aligned bar consists of single-owner full tiles and creates no
mixed tile/event. Its remaining short-leg tile has no foreign endpoint.
The displayed local and return regions are physically disjoint, and
all old event/support exclusions are immutable. Adding mass one,
local signed value+1 and return signed value-5 proves (2), without
an enumeration or length cutoff.

## Closure is transferred, not finished

The point z=(22,7) is W's original far axial support. It is absent
from H union W, but has endpoint neighbours W:(22,6) and P_0:(23,7).
It must therefore be consumed by another new original in every complete
extension containing this partial family. The other two endpoint
neighbours are absent. This gives a concrete return to the first block,
not a support-closed negative family.

What fails is the inference

    endpoint-disjoint new original consuming the forced site
    implies a nonnegative Phi increment.

The four-unit selected-pair theorem remains true for its stated selected
union. Whether the family including W admits a complete feasible extension
is OPEN, so this is not a counterexample about actual complete families
or the global inequality. A successful next compensation argument must
include the new z-consumer and its return receipt, not just the number
of forced owners or the local tile at x.

The exact-set verifier retains all original source records, checks all
three new full tiles and all ten owner-labelled events, the charge
counts, both increments, and the next missing support. Finite controls
supplement the all-g proof. No separate Lean or independent review of
this later obstruction is claimed; it lies outside review780b9242's input.
