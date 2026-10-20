# C second corners cannot consume phase01 terminals

20 October 2026. Under the complete original-source hypotheses of the
[C two-corner theorem](BACKFILL_TWO_CORNER_COMPENSATION.md), every negative
second corner of a C backfill has phase10, never phase01. This is a general
route-C statement, without the saturated AA restriction. It gives two exact
phase-specific partitions of the existing negative pool. It neither creates
additional reserve nor proves unrestricted coefficient-one allocation or the
rectangular-grid triple equality.

## Complete-source hypotheses and the two possible terminal shapes

Retain complete finite original U/rotor sources, all independent legal even
widths at least6 and heights at least4, disjoint original endpoint sets,
unchanged original matching, mandatory retention of original supports outside
P, selected occupied degree at most one, and one transported physical tile
partition. Repeated owners and components are allowed.

Normalize the C backfill tile to {0,1}x{-2,-1}, with q=(1,-1) and r=(1,-2).
Its U11 companion is

    F(s,t)=(t-1,s-h-1), from U(v,h,f).

The C owner of q, called H, has the form

    H(s,t)=(a+1-s,t-w-1), from U(w,b,a).

Here a is the RIGHT incident height, whereas b is the independent left
height. In particular H owns column-1 from row1 through rowa+1 and its
bar contains (a,-2). F owns row0 through columns-h-1,...,-1 and its
bar contains (1,-h). These facts use full sources, not a truncated stencil.

The earlier theorem proves that r has an exact singleton owner J, different
from F and H; J is not a rotor or a phase11 U. Suppose J has phase01.
The original singleton catalogue makes r an actual terminal. Its foreign
north and east neighbours forbid an upward or rightward incident stem.
The fixed physical phase and singleton tile leave the following two forms,
after interchanging the two independent heights when needed:

    J_N(s,t)=(j+1-s,t-3),   from U(z,j,k),
    J_E(s,t)=(2-t,s-j-2),   from U(z,j,k).

The first has its incident stem down from r and its bar extending east;
the second has its incident stem west from r and its bar extending north.
Both descriptions include a terminal from either canonical arm: reflect the
source across its vertical axis and exchange its left/right heights. They
do not assume equal heights or fix the far height k. This orientation/phase
adapter uses the previously established complete U singleton catalogue; its
sampled independent physical controls are separate from the general proof.

## Two unbounded crossing arguments

For J_N compare j+1 and a.

- If j+1>=a, H's bar endpoint (a,-2) is on J_N's incident stem or bar.
  Its J_N inverse coordinate is (j+1-a,1), between rows0 andj.
- If j+1<a, J_N's bar endpoint (j+1,-1) is on H's incident stem.
  Its H inverse coordinate is (a-j,w), between rows2 anda.

Thus J_N and H have a common original endpoint for every independent pair
of heights. The case of equality is included in the first alternative.

For J_E compare j+2 and h.

- If j+2>=h, F's bar endpoint (1,-h) lies on J_E. Its J_E inverse
  coordinate is (j+2-h,1), between rows0 andj.
- If j+2<h, J_E's bar endpoint (0,-j-2) is on F's incident stem.
  Its F inverse coordinate is (h-j-1,1), between rows2 andh.

Again equality is included. Neither argument bounds the dimensions or
assumes a fresh owner: J differs from H and F because their exact profiles
in the physical backfill tile are respectively {q} and {(0,-2),(0,-1)},
whereas J's exact profile is {r}. Disjoint original endpoint ownership
therefore contradicts either crossing. Phase01 is excluded.

Consequently a C second corner is either a negative phase10 bar-corner
singleton, counted by Cminus, or an actual positive phase00 terminal
activation, counted by Cplus. The already proved identity remains

    Cminus+Cplus=KC.

## One pool refined by original source phase

Use the jointly disjoint occurrence families and the ONE complement Lnew
of the [D enhancement](BACKFILL_D_INTERIOR_TWO_CORNER_COMPENSATION.md).
Split negative cap fillers, old selections e=|E0|+|E1old|, negative D second
corners, and Lnew according to their fixed original phase:

    Fneg=Fneg01+Fneg10,  e=e01+e10,
    Dminus=D01+D10,     Lnew=L01+L10.

All these are counts of actual selected occurrences or their complement,
not new allocations. The two phase-specific original singleton pools have
exact sizes2K01 and2K10. A C first corner q has phase01; the present theorem
makes its negative second corner phase10. A D first corner x has phase10.
Thus the previously established joint disjointness gives exactly

    2K01=Fneg01+e01+KC+D01+L01,
    2K10=Fneg10+e10+Cminus+d+D10+L10.                 (1)

Summing (1) recovers the previous negative-pool identity, with
Dminus=D01+D10, without spending any occurrence twice. In particular

    Fneg10+e10+Cminus+d+D10<=2K10.                  (2)

In the specified AA component, the accepted C/D positive-exit exclusion
gives Cminus=KC and D01+D10=d. Hence

    Fneg10+e10+KC+d+D10<=2K10.                     (3)

Counts and pools in (3) must all be restricted to that SAME component.
This refinement forbids replacing a demanded phase10 corner by spare
phase01 terminals. For example the purely scalar tuple K01=1,K10=0,
KC=Cminus=1 with all other negative-pool counts zero satisfies the old
combined census2(K01+K10)=KC+Cminus, but violates (2). This is an excluded
arithmetic candidate, not a physical fusion or a counterexample to the goal.

Equations (1)--(3) refine resource type. They do not increase R or change
the previously established all-route retained term. In particular they do
not alone prove a strict source/mark surplus, exclude all AA components,
improve the unrestricted5/6 bound, or settle the full target. The remaining
problem is to control the phase10 claims and surviving A/C/D and neutral
continuations globally.

## Verification scope

The source [CSecondCornerPhase.lean](../formal/SubQuorum/CSecondCornerPhase.lean)
contains six declarations: both all-parameter endpoint crossing witnesses,
their disjointness contradiction, and three conditional typed-pool
identities/inequalities. The physical singleton/phase classification and
global occurrence partition adapters remain written. No end-to-end Lean
source-fusion or full allocation theorem is claimed.

Run `python3 develop/check_c_second_corner_phase.py` for physical controls.
They cover27 independent dimension catalogues and108 anchored surviving
phase01 roles;256 crossings in each orientation, including48 equality
boundary cases for the second;4860 conditional typed budgets, of which2430
have the AA Cminus=KC specialization. They verify coordinates and catch
left/right-height mistakes; the unbounded crossing arguments above prove
the exclusion. Complete criticalU10 realizations supplied here: ZERO.
