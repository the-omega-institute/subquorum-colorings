# Withdrawing the terminal guard: exact half-area frontier

**Subsequent resolution (27 October):**
[Completely frozen attainers and a sharp terminal-port criterion](FROZEN_HALF_AREA_ATTAINERS.md)
settle the frozen maximum left open in this note. It is also half-area;
forbidding the terminal vertical matching edge restores the one-unit margin.
The historical open-question statements below describe the preceding stage.

26 October 2026. Wenlin Zhang and Haobo Ma. Research continuation.

Removing the last retained row-three guard changes the exact unrestricted
matching maximum from half-area minus one to half-area. The whole strip deficit
is still paid, but no additional reserve can be guaranteed. We give a general
upper bound and an explicit sharp family for every length. The family is not
completely frozen; the completely frozen maximum under the new permissions
remains between half-area minus one and half-area.

## 1. Statement and relation to the preceding theorem

Use the board, T0, M0, P0 and R' defined in Section 1 of
[Boundary withdrawals](BOUNDARY_WITHDRAWAL_AND_PROPAGATED_COMPENSATION.md).
For m>=2 the board is {0,...,5} x {0,...,6m+9}. Put

    c=6m+9,  R''=R' minus {(3,c)}.

Equivalently, retain all old selections in rows zero, one and two, retain
(3,1), and allow every other old row-three selection and every old row-four
selection to be withdrawn. An optional withdrawal is permission, not a demand
that a vertex stay absent.

**Theorem.** Suppose M is an actual grid matching with endpoint set P,
T and P are disjoint, each selected vertex has at most one neighbour in T union P,
P0 subset P, and R'' subset T. Then

    J=|T|+|M| <= 18m+30 = area/2.                     (1)

The bound is attained for every m>=2 by the explicit family in Section 4.
Thus the preceding stronger inequality J<=18m+29 does not extend to these
permissions without further hypotheses. These examples do not refute (1),
a completely frozen version of the stronger inequality, or a universal 5/6 bound.

## 2. The new available set and terminal inequality

The new available set is precisely

    U''=U' union {(2,c),(3,c),(4,c)}.

Here U' and its disjoint pocket/pair/block/end partition are those in the
preceding proof. The old guard (3,c) was anchored by old endpoint (3,c-1).
Removing it releases exactly its two formerly blank neighbours (2,c),(4,c)
and the guard itself. Other forced blanks retain their old anchored witnesses.
No site of U'' touches R''; the row-zero unanchored retained selections still
have only forced-blank neighbours. This proves that all new selections and
new endpoints lie in U'' for every length, including arbitrary rematching.
The new fixed contribution is

    |R''|=5m+10, |P0_white|=4m+5,
    J=9m+15+W(U''),                                  (2)

where W counts black new selections and white new occupied vertices.
The available set has 17m+26 sites. Only the right end changes:

    E''=E union {(2,c),(3,c),(4,c)}.

Write a=6m+6 and name its five black selection bits

    x=t_(4,a), y=t_(4,a+2), u=t_(5,a+1),
    w=t_(5,a+3), h=t_(3,a+3),

and five white blank indicators

    A=1-o_(4,a+1), B=1-o_(5,a), C=1-o_(5,a+2),
    L=1-o_(4,a+3), K=1-o_(2,a+3).

Every blank is in [0,1]. The selected-vertex condition implies

    x=1 => A=B=1;          y=1 => A=C=L=1;
    u=1 => A+B+C>=2;       w=1 => C+L>=1;
    h=1 => K=L=1.                                  (3)

The first two upper sites and h each have one old occupied neighbour above
or to the left. The other two have degree three or two within the board.

**Terminal lemma.** Conditions (3) imply

    A+B+C+L+K >= x+y+u+w+h,
    W(E'')=x+y+u+w+h+5-(A+B+C+L+K) <=5.             (4)

Here is an elementary proof, valid even for real blank indicators. First the
old three-variable argument gives A+B+C>=x+y+u: if x=y=1 the three blanks
are one; if exactly one is one, its two forced blanks suffice for it and u;
if both are zero, u's condition suffices. If h=1, K=L=1, so this bound plus
K+L>=h+w proves (4). Suppose h=0. If y=1, A=C=L=1 and B>=x, so the total
is at least 3+x>=y+x+u+w. If y=0,x=1, A=B=1 and C+L>=w, giving at least
2+w>=x+u+w. If x=y=0,u=1, A+B+C>=2>=u+w; if x=y=u=0, C+L>=w suffices.
These cases exhaust the selection bits and prove (4).

The old input state x=0,B=1 no longer improves this bound. In fact equality
with that state uniquely forces

    x=y=h=0, u=w=1,
    A=L=K=0, B=C=1.                                (5)

For a written equality proof: with h=1, B=K=L=1 and u=1 requires A+C>=1,
so the blank sum is strictly greater than y+u+w+h (whether y=0 or1).
Thus h=0. If y=1 then A=C=L=B=1 and the blank sum exceeds y+u+w; hence
y=0. If u=0, B+C+L>=1+w>w. Therefore u=1. Equality now says
A+C+L+K=w, while u requires A+C>=1, forcing w=1, A+C=1, L=K=0.
The w condition gives C=1 and then A=0. This proves (5).
It describes occupation only; a white occupied site may be selected or matched.

## 3. Global bound and an exact no-reuse budget

The preceding pocket certificate still gives W(A')<=10. Its boundary edges
are unchanged. The same 2m anchored pairs each contribute at most one, and
the same m thirteen-site blocks each contribute at most seven. Summing over
these disjoint pieces with (4) gives

    W(U'') <= 10+2m+7m+5=9m+15.

Equation (2) proves (1). This is an all-length proof; no finite optimization
or enumeration is used to justify the bound.

Equality in (1) forces pocket weight ten, every pair saturated, every block
saturated and terminal weight five. The pocket starts the input state and
saturated blocks transmit it, exactly as in the preceding proof. Thus (5)
is a necessary terminal pattern for any equality board, regardless of its
actual matching. The former terminal inequality e+p_m<=4 is replaced by
e<=5. In particular a state arriving at the new terminal can use its full
capacity; treating it as a missing unit of capacity would be incorrect.


There is a useful further restriction for the remaining freezing question:
**every old optional selection must actually be absent at half-area equality**,
that is, T intersect T0=R''. Indeed each old row-four selection is an x or y
site of a saturated block or of the terminal, and all these bits are zero.
Each internal old row-three guard (3,a+3) has its old endpoint neighbour
(3,a+2) and, by block saturation, occupied neighbour (4,a+3). It cannot be
selected. The last guard has h=0 by (5). These lists exhaust T0 minus R''.
Thus a fully frozen half-area witness, if one exists, cannot obtain the
missing freezing support by restoring any of these old guards.

For each original aligned 2x2 tile Q put

    charge(Q)=4-2|T intersect Q|-|P intersect Q|.

The whole sum is area-2J>=0. The unchanged upper strip has sum -m.
Let Cplus be the sum of positive exterior charges and Cminus the absolute
sum of negative exterior charges. Then

    Cplus >= Cminus+m.                              (6)

Allocate distinct positive half-unit tokens first to all Cminus exterior
negative demands and then to the m upper-strip demands. The inequality
supplies one injection for these two demand sets, so no token is reused.
For the sharp family below equality holds in (6): no unspent half-unit token
remains. Consequently neither the former two-half-token reserve nor any
positive uniform reserve survives for unrestricted actual matchings.
This is an aggregate physical-token conclusion, not a directional route theorem.

## 4. Explicit sharp family with no matching edges across seams

Use three finite chunks. Coordinates in the following table are relative to
the first column of each chunk. A vertical bar separates matching edges.

**Left chunk, width six.**

    T_L={(0,1),(0,3),(0,5),(1,2),(1,4),(2,0),(2,3),
         (3,1),(3,3),(4,0),(4,2),(4,4),(5,3),(5,5)}.
    M_L={(1,1)--(2,1) | (1,5)--(2,5) |
         (3,5)--(4,5) | (5,1)--(5,2)}.

**Period chunk, width six.**

    T_B={(0,1),(0,3),(0,5),(1,2),(1,4),(2,3),
         (5,1),(5,3),(5,5)}.
    M_B={(1,0)--(1,1) | (1,5)--(2,5) |
         (2,0)--(3,0) | (2,1)--(3,1) |
         (3,2)--(4,2) | (3,3)--(4,3) |
         (3,4)--(3,5) | (4,0)--(4,1) | (4,4)--(4,5)}.

**Right chunk, width ten.**

    T_R={(0,1),(0,3),(0,5),(0,7),(0,9),
         (1,2),(1,4),(1,8),(2,3),(2,9),
         (5,1),(5,3),(5,5),(5,7),(5,9)}.
    M_R={(1,0)--(1,1) | (1,5)--(2,5) | (1,6)--(1,7) |
         (2,0)--(3,0) | (2,1)--(3,1) | (2,6)--(2,7) |
         (3,2)--(4,2) | (3,3)--(3,4) | (3,5)--(4,5) |
         (3,6)--(4,6) | (3,7)--(3,8) | (3,9)--(4,9) |
         (4,0)--(4,1) | (4,3)--(4,4) | (4,7)--(4,8)}.

Concatenate one left chunk, m-1 period chunks and one right chunk, translating
each to its own column interval. The total width is 6+6(m-1)+10=6m+10.
All matching edges stay inside their chunk; their endpoints are distinct and
disjoint from the tabulated selections. Within each chunk every selected
vertex has at most one occupied neighbour, as direct inspection of the
short tables shows. More explicitly the selected degrees, in sorted T order,
are

    L: 1,0,1,1,1,1,1,1,1,0,1,1,1,1;
    B: 1,0,1,1,1,1,1,1,1;
    R: 1,0,1,1,0,1,1,1,1,1,1,1,1,1,1,1.

At each seam the preceding last column has status (T,P,P,P,P,T) from top
to bottom. The next first column has status (blank,P,P,P,P,blank).
Thus the selected sites on the left touch blanks across the seam and there
are no selected sites on the right first column. Gluing introduces no new
occupied neighbour of a selected vertex. This verifies feasibility for any
number of period chunks, rather than extrapolating a finite-board search.

The retained selections R'' consist of all row-zero odd columns, row-one
columns {2} union {4+6j,8+6j:0<=j<=m}, and (2,0),(3,1). The chunk tables
contain these lists, and (3,c) is absent. Old endpoints are also covered by
their residue. Explicitly, with d=3+6j, 0<=j<=m, they are (1,d+2),(1,d+3),(1,d+4),(2,d+4),(2,d+3),(3,d+3),
(3,d+4),(3,d+5), together with (1,1),(2,1). Comparing these lists with the
left, period and right endpoint tables proves P0 subset P for every m.
For 0<=j<m, the endpoint (1,6j+5) lies in the final column of L (j=0)
or a period chunk (j>0); all seven other endpoints lie in the first three
columns of the next period chunk or R. For j=m the eight endpoints have
right-chunk relative columns 5,6,7,8 and all are explicitly covered there.
The exceptional pair (1,1),(2,1) lies in M_L. Counts give

    |T|=14+9(m-1)+15=9m+20,
    |M|=4+9(m-1)+15=9m+10,
    J=18m+30.

The endpoint (5,1), matched to (5,2), has only its mate as an occupied
neighbour on every board in this family. It can never acquire two kept
neighbours in the freezing induction; equivalently this matching edge admits
a singleton promotion. Hence the family is not completely frozen for any m.
This observation is part of the proof, not a conclusion based on a finite
freezing run.

## 5. Scope and next question

The new result settles the unrestricted actual-matching optimum for this
larger occupied-band permissions class. It proves exactly where the additional
reserve is lost while retaining a correct aggregate compensation inequality.
The previous fully frozen attainers remain in the class and give value
18m+29. Our new family gives 18m+30 but is not fully frozen. Therefore the
fully frozen maximum is one of these two integers. To settle it, either
exclude complete freezing for every equality board using the necessary
saturated-chain and terminal pattern, or construct a completely frozen
equality board. A nonfrozen witness cannot answer that question.

The accompanying standard-library verifier checks local bit models, chunk
seams, actual boards and token injections. Lean verifies the scaled terminal
inequality and its equality pattern, global arithmetic and token accounting;
the graph-coordinate reduction and all-length chunk proof remain written
arguments. Neither finite enumeration nor algebraic Lean checks are presented
as an end-to-end formal graph proof.


## 6. Reproduction

From the repository root:

    python3 develop/check_terminal_guard_half_area.py --output output/terminal-guard-half-area.json
    python3 develop/check_terminal_guard_half_area_formal.py --output output/terminal-guard-half-area-formal.json

The saved exact run checks 182 feasible terminal bit models (76 with input
state, exactly one saturated pattern), three chunks and all four seam types.
There are 93 actual-board controls: 41 sharp lengths through m=100, four
inherited frozen attainers and 48 additional actual rematchings. All 93 token
injections pass; all 41 new sharp controls use the full token budget.
Seven scoped Lean theorems pass locally with Lean 4.33.0 and only standard
logical axioms. The formal runner records memory and enumerates active Lean
and Lake executables by basename of the process comm field before execution.


The [Oracle receipt](../output/terminal-guard-half-area-oracle.json) records two
terminal infrastructure failures, both browser disconnections while typing.
Neither request produced a mathematical response. No independent Oracle
acceptance is claimed for this note; its evidence is the written proof and
the separate exact and Lean checks above.
