# Safe beta closing: sharp frozen Hall deficiencies repaired through mixed paths

25 October 2026. Haobo Ma and Wenlin Zhang. Research branch only.

Completely frozen grids do **not** always admit a direct whole-beta matching
saturating their deficient whole-support interval trees. This note gives an
explicit all-parameter physical counterexample to that proposed saturation
rule. Its Hall defect is arbitrary, survives blank right padding, and attains
the preceding two-external-witness bound. The full network nevertheless pays
all demands through distinct mixed paths and distinct original intervals.
The target scalar grid inequality remains strictly true.

The construction uses one extra selection in the
[interior capped family](INTERIOR_SUPPORT_TREE_CAPS_AND_EXTERNAL_WITNESSES.md).
No new solver search is needed. The point is the distinction between a
false direct-beta completion rule and the still-open general compensation
problem, not a new abstract matching theorem.

## 1. A safe selection insertion at a BP tip

Let (T,M) be a feasible grid configuration, with actual endpoint set P, and
all P endpoints completely frozen for that actual M. Let v be a BP terminal
of an original beta strand. Let w be its blank within-band vertical partner.
Suppose the original occupied neighbors of w are **exactly {v}**. Insert w
into T, leaving P and M unchanged.

**Lemma 1 (safe beta closing).** The new configuration remains feasible and
completely frozen. The entire BB--TT interval forest, all its original
identities and all its boundary marks are unchanged. The beta containing v
becomes mixed. Every old alpha and its entire support stay unchanged, as
does its interval incidence. Thus t stays fixed, b decreases by1, and the
whole-support tree--beta graph loses precisely that beta vertex. Its maximum
matching size falls by either0 or1. The signed boundary margin falls by1.

**Proof.** The new selected vertex w sees only v among old occupied vertices;
there is no self adjacency. No old selected vertex is adjacent to w, since
v is the only old occupied neighbor and is an endpoint, disjoint from T.
Thus every selected site still sees at most one occupied neighbor. The old
freezing derivations still apply: actual endpoints, mates and nonmate
adjacencies do not change, and every old selected witness remains selected.
More generally induction on a freezing derivation proves monotonicity under
enlarging T with P,M fixed. There is no new matching endpoint to freeze.

Only the within-band column {w,v} changes type, from BP to TP. It contains P
both before and after, and is neither BB nor TT in either configuration.
All BB/TT sites and their connecting edges are therefore identical. The
PP strand graph depends only on actual matching edges and within-band P--P
edges, so it too is unchanged as an untyped graph. Exactly the terminal v
changes label, BP to TP. Its old BP--BP strand becomes TP--BP; no other
strand changes type. In particular all original alpha supports and their
P-free neighboring gaps are identical. All other beta tips and direct
alpha--beta adjacencies are identical. Deleting one right vertex from a
finite matching graph changes its optimum by at most one. Finally |T|
increases by1 with board, M and boundary marks fixed, so the margin decreases
by1. QED.

This statement uses feasibility and complete freezing. It makes no extra
claim that T is a globally maximum selected set or that M is unique.

## 2. Applying the lemma in the explicit capped family

Take any d>=1 and c=17+2d in the preceding 12-by-(20+2d) family. Insert

    w=(2,12),   whose sole old occupied neighbor is v=(3,12).

This is checked from the permanent original coordinates: (1,12),(2,11),
(2,13) are blank and (3,12) is P. The cap and tail lie in rows5..10 and
columns>=17, so they never change this neighborhood, for any d or padding.
Originally v was one end of the sole beta, with other tip (5,11). That
strand now has TP (3,12) and BP (5,11), hence is mixed. There is no beta left.

The original alphas are still

    A: (5,8),(8,8);   B: (5,10),(8,14).

Their complete support incidence is still exactly A--J--B, with J the
singleton original BB interval at band2/column9. It is a deficient two-owner
tree. Therefore

    t=1, mu=0, direct joint defect=1.             (1)

The two selected external tokens from the preceding lemma are unchanged:

    A:(8,8) -> BP(8,7), on mixed TP(8,6)--BP(8,7);
    B:(8,14)-> BP(8,13), on mixed TP(8,12)--BP(8,13).

They are two different original mixed identities. The top tips of A,B both
choose J. Thus q_mixed=2 and h_marked=0, and the bound

    t-mu <= floor((q_mixed+h_marked)/2)

is attained **by an actual completely frozen grid**, not just an abstract
token network. The explicit Hall set is the single deficient tree with an
empty whole-beta neighborhood.

The exact inventory is

    |T|=34+4d, |M|=25, |P|=50,
    alpha=2, beta=0, mixed=9, pure PP cycles=5,
    available original intervals I=51+8d,
    interval-only payment1, U=50+8d,
    margin=U+beta-t=49+8d>0.                    (2)

All interval identities, including the sole original TT merger, are exactly
those of the pre-insertion board. Adding2r blank right columns preserves(1),
adds12r to I,U and margin, and does not release source access across the
interior PP cap.

## 3. Two explicit one-link mixed repairs

Direct-beta completion fails, but mixed continuation pays the missing unit.
Here are two witnessed repairs with different old-assignment behavior.

**Repair A, preserving the specified old B->J assignment.** Link

    (8,8)->(8,9).

The destination is the original mixed strand BP(8,9)--TP(8,10). The resulting
alpha A' has free TP tips (5,8),(8,10). Its latter tip sees the unmarked
original singleton K at band4/column11, physical cells {(8,11),(9,11)}.
Pay A' with K and keep B paid by J. K and J are distinct original resources,
and K was unused by every original alpha in the interval baseline. This
uses one link and changes zero old interval assignments.

**Repair B, using the former beta as a zero-credit gate.** Link

    (5,10)->(5,11).

The former beta is now mixed, with exit TP(3,12). Following the BT column11
leftward reaches the original singleton R at band1/column10, physical cells
{(2,10),(3,10)}. Explicitly the cap selection is (3,11) and its within-band
partner (2,11) is blank. Thus this is a justified existing selected-cap / BT
access, not a newly invented interval. The new B' has TP tips (3,12),(8,14).
Assign B' to R and A to J. Relative to B->J this changes B's old payment
once; relative to the opposite baseline A->J it changes no old payment.

Both repairs leave alpha=2,beta=0, pay two different alpha strands using two
different original intervals, and leave U'=49+8d,t'=0. The exact margin is
still(2). In particular **the old beta link is no longer beta consumption**;
its usefulness now comes from the mixed exit's interval access.

Zero links cannot pay both alphas: their complete original supports see only
J. Either construction pays both with one link. Hence full compensation has
maximum value2 and exact minimum link count1. This is a proof by explicit
upper and lower bounds, independent of the verifier's flow optimization.

The chosen external-token destinations in Section2 need not be the gates
used by an optimal repair. Restricting future continuation to those chosen
tokens without proof could discard legitimate routes.

## 4. Arbitrary physical deficiency and simultaneous nonreuse

For every q>=1 stack q copies with translations (12i,0). As in the preceding
all-q stacking proof, occupied rows in consecutive copies are separated, no
new occupied adjacency is introduced, all actual matching witnesses remain
valid, and interval identities lie in different bands. There are no
horizontal terminal links across copies. Therefore

    alpha=2q, beta=0, mixed=9q, t=q, mu=0,
    I=(51+8d)q, U=(50+8d)q, margin=(49+8d)q,
    q_mixed=2q, h_marked=0, defect=q.             (3)

The physical bound is sharp for every q, not just q=1. Right padding remains
stable. Applying Repair A in every copy uses q distinct mixed gates, q links,
and the q original unused K_i. The old q B_i->J_i payments remain unchanged.
Applying Repair B instead uses the q distinct former beta/mixed gates and
q distinct original R_i, with A_i->J_i. All terminal endpoints are distinct,
so these links are simultaneously legal. Every original interval is used
once. Each separated copy needs at least one link and permits one, proving
the full exact minimum link countq.

One may additionally include s>=1 **unclosed** capped copies, so the total
board has betas without curing the closed components. The direct graph has

    t=q+s, beta=s, mu=s, defect=q.               (4)

Each such beta is confined to its own unclosed component and is spent there;
it is not a spare resource available again to a closed tree. Repair A on
closed copies plus the original direct-beta repair on unclosed copies pays
everything with q+s links. The positive margin is
(49+8d)q+(50+8d)s. Equation(4) is not an example of two trees competing for
the same beta; that stronger geometric realization remains a separate task.

## 5. Verification, formalization and changed research status

The all-d safe insertion, unchanged interval identities, arbitrary stacking,
padding stability, sharp Hall defect and exact mixed repair arguments above
are written proofs. The deterministic checker verifies72 boards (d=1..16,
three nonzero padding widths and eight carried isometries) and33 stacks,
including9 positive-beta controls. Across these105 physical models it checks
267 nonsingleton deficient trees and105 positive beta Hall deficiencies;
all are real frozen models. Original-alpha token capacities and4,649 subset
inequalities are rechecked. Every route is replayed against actual supports
and original resource identities. No solver is needed.

`formal/SubQuorum/BetaClosingAndMixedRepair.lean` supplies eight scoped
declarations: arbitrary freezing monotonicity under selected-set inclusion;
a general insertion feasibility lemma; the concrete safe site; preservation
of the46 original endpoints' freezing; local terminal-type data; the cap exit;
the parametric ledger; and sharpness arithmetic. The earlier all-column cap
freezing proof supplies the four new endpoints. The full-board interval
inventory, matching/Hall adapter and full mixed-route optimality remain written
proofs and solver-free checks, not a claimed complete Lean formalization.

The proposed universal direct-beta saturation rule is now **refuted under
the stated feasibility/freezing hypotheses**. It should no longer be listed
as an open lemma to prove. The target inequality is not refuted: every board
here has a positive margin and explicit full mixed compensation. The next
question is a general capacity-preserving mixed continuation mechanism or an
actual obstruction to that broader mechanism. Two trees sharing a beta is
also still open as a specific physical configuration. No change to submitted
manuscripts or claim of a new universal5/6 bound is made.
