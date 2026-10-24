# Pairing-choice invariants and local debt-donor cancellation

7 October 2026. Follow-up to [terminal strands](TERMINAL_STRAND_ACCOUNTING.md).
The changes below affect auxiliary strand pairings only. They do not change
the feasible pair T,M, its objective, residual components or tile charges.

## 1. Changing the pairing cannot change the net shortage

Use maximum disjoint adjacent pairs of residual endpoints in each deficient
tile, with endpoint types L,S,P and reserve count c as in the preceding note.
Only two local cases have more than one maximum pairing: capacity two with
three endpoints, or capacity two with four endpoints. In the three-endpoint
case the unused corner has the majority checkerboard color, independent of
the choice; in the four-endpoint case there is no unused endpoint. All other
endpoint sets have a unique maximum pairing. Thus the number of S ends of
each color in every tile, the number of reserves in every tile, and all L
and P ends are independent of the local choices.

Every alternating strand has opposite-color ends: it begins and ends with
a physical matching edge, contains one more matching edge than auxiliary
edges, and therefore has odd physical length. This holds for every strand
type, not just PP. If L_b,L_w,S_b,S_w,P_b,P_w count black/white ends, then

    epsilon=L_b+P_b-S_w-c=L_w+P_w-S_b-c.                 (1)

**Proof.** In the first expression LL, LP and PP strands each contribute
one, SS contributes minus one, and LS and PS contribute zero. This is the
exact shortage identity. Interchange black and white for the second. QED.

On the whole grid P_b=P_w=0 and

    q=L_b-S_w-c=L_w-S_b-c=n_LL-n_SS-c.                 (2)

Consequently choosing pairings to reduce the number of LL strands cannot
improve the sign of q. If LL decreases by one then SS decreases by one too.
Pairing optimization can simplify the geometry of the certificate, but is
not by itself a proof of the missing donor inequality. Black/white counts
give a check on a proposed allocation, not an extra source of budget.

## 2. A local switch cancels a debt strand against an SS donor

Call LL, LP and PP strands debt strands; SS strands are donors. Suppose
a debt strand X and a distinct SS strand Y visit the same tile Q in the
physical strand decomposition. Their physical vertices remain disjoint.
Then Q has capacity two and one of the following forms:

1. d_Q=4: each strand uses one auxiliary pair in Q; they use all four corners.
2. d_Q=3: X uses one auxiliary pair in Q and Y has its S end at the remaining
   residual corner of Q.

These exhaust the possibilities. A debt strand cannot end at a positive-
capacity tile, so it uses two endpoints of Q. A distinct strand needs at
least one more endpoint. Capacity-one tiles have residual degree at most
two; hence r_Q=2 and d_Q is three or four. With d=3 an SS donor can only
use the remaining endpoint as its terminal; with d=4 no residual endpoint
is terminal.

**Theorem 1 (single-use local switch).** In either case choose the other
maximum adjacent pairing in Q and keep every other pairing fixed. Then
X and Y are replaced as follows:

    LL + SS -> LS + LS,
    LP + SS -> LS + PS,
    PP + SS -> PS + PS.                                 (3)

No other strand or cycle changes. Total debt count and SS count each fall
by one. Each tile's S-end count and color and every reserve remain fixed.
T,M, all physical occupancy, objective, boundary matching and tile charges
remain literally unchanged.

**Proof.** In the d=4 case delete the two old auxiliary pairs. Each of the
two distinct paths is cut once into two arms. The other perfect matching
of the tile four-cycle pairs each arm of X with an arm of Y. Each resulting
path therefore has one endpoint from X and one S endpoint from Y, proving
(3). Neither path visits Q twice: a second visit would already consume all
four corners, leaving none for the distinct path.

For d=3 let the old paired corners be A,B and the unused corner C; B is
the minority-color corner adjacent to both A and C. X is cut at A--B;
Y begins at the S end C. Replace A--B by B--C and make A the S end.
The arm of X through A now ends at S in Q; the other arm follows the old
Y to its other S end. This gives (3). A and C have the same color, so the
S-end color is fixed. No physical edge of M changes. QED.

Repeatedly apply this switch whenever a debt and an SS donor share a tile.
The integer number of debt strands strictly decreases at each step, and
SS decreases by the same amount. Hence there are at most
min(initial debt count, initial SS count) steps. Recompute paths after each
step to avoid reusing their old identities. The process terminates in a
decomposition where no debt strand shares a tile with an SS donor. A
straightforward path search and tile-incidence scan gives a polynomial
algorithm. No canonical result or global minimum is asserted.

This proves a local cancellation normal form in arbitrary mixed-direction
configurations, including capacity-two junctions and repeated visits by
other paths. A donor spent in (3) disappears from the SS ledger together
with the debt it paid. It cannot be spent again through its old route name.

## 3. Reserve ownership along a debt strand

If a debt strand visits a tile with c_Q>0, that tile necessarily has
r=2,d=2 with adjacent residual endpoints and c_Q=1. Indeed a debt strand
cannot terminate at S, so it uses an auxiliary pair. The local table leaves
only this row with both an auxiliary pair and a positive reserve. Its two
residual endpoints lie on that one strand, so no distinct debt strand can
visit the same reserve tile. Assign one such tile to each debt strand that
meets a reserve, using a fixed tie rule when it meets several. Every selected
unit is unique and pays that strand's one unit exactly.

Apply this after the SS switches, and remove each assigned debt and reserve
from the unpaid ledger. If D_rem is the remaining debt count, S_rem the
remaining SS count and c_rem the unspent reserve count, then exactly

    epsilon=D_rem-S_rem-c_rem.                          (4)

Every unpaid debt strand now shares no tile with an SS donor and visits no
reserve tile. At each of its capacity-two visits d is three or four: d=2
adjacent would supply a reserve, and d=2 diagonal cannot provide its passage.
This is an explicit all-size reduction of directly overlapping compensation.
It leaves cross-tile and cross-component allocation open. Reserve assignment
changes only the ledger; it asserts no insertion of a feasible matching edge.

## 4. Feasible sharp controls and the remaining obstruction

On a 6-by-6 physical rectangle take T empty and match

    (2,2)--(1,2), (2,3)--(2,4),
    (3,3)--(4,3), (3,2)--(3,1),
    (2,0)--(2,1), (5,2)--(5,3).

Take D as the central tile (tile row 1,column 1), its western neighbor
(1,0) and its southern neighbor (2,1). The central tile has r=2,d=4;
the other two have r=1,d=1. There are two ports, rho(D)=-1 and c=0.
Pairing the central upper and lower sides gives PP+SS. Pairing the two
vertical sides gives PS+PS. The shortage is zero in both decompositions,
and every occupied vertex and matching edge is unchanged.

For the d=3 control delete the edge (3,3)--(4,3) and exclude the southern
tile from D. Its matching edge (5,2)--(5,3) may remain outside D. The
central tile now has r=2,d=3 and its west neighbor has r=1,d=1. Again
p=2,rho=-1,c=0. The upper auxiliary pair yields PP+SS, with the SS end
at the central lower-left corner. Switching to the left pair yields PS+PS,
moving the central S end to the upper-right corner of the same color.

These controls show that minimizing raw debt counts can remove exactly the
same number of donors. It does not generate a new negative budget. On the
full grid this gives the identical LL-minus-SS invariance in (2).

In the prior arbitrary-length normalized equality family the one LL source
and the one reserve lie in different tile regions; there is no SS strand.
This switch has nothing to cancel. The existing transport family also
places its only negative residual component arbitrarily far from the source.
Thus the normal form removes directly shared SS compensation but leaves the
genuinely cross-component source-to-reserve or source-to-SS geometry open.
It does not establish the unrestricted grid inequality or improve the
universal 5/6 bound. The focused manuscript is preserved.

Run `python3 develop/check_strand_switches.py --output output/strand-switch-controls.json`.
Finite controls test all local endpoint types and arm lengths, coordinate
fixtures, colors, count changes and switch termination. They verify the
written local proof rather than replace an all-size allocation argument.
