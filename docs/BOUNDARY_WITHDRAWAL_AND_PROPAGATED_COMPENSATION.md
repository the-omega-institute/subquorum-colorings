# Boundary withdrawals and propagation of one unit of compensation

26 October 2026. Wenlin Zhang and Haobo Ma. Research continuation.

The exact connected-band maximum remains **18m+29** after permitting withdrawal
of every old row-four selection, including all three boundary guards retained
by the preceding theorem. The new proof allows a larger left pocket to gain
one unit. Its equality conditions force a boundary state that either loses a
unit at an intermediate block or reaches a right end whose capacity is smaller
by one. This gives compensation across an arbitrarily long connected band.

## 1. Enlarged permissions and exact statement

Use the grid {0,...,5} x {0,...,6m+9}, m>=2, and set k=m+1. Translate

    Tcore={(0,2),(0,4),(1,1),(1,5),(4,3),(4,5),(3,6)},
    Mcore={(1,2)--(1,3),(1,4)--(2,4),
           (2,3)--(3,3),(3,4)--(3,5)}

by (0,3+6j), 0<=j<k. T0 is the translated selections plus
{(0,3+6j):0<=j<=k} and {(0,1),(1,2),(2,0),(3,1)}. M0 is the translated
matching edges plus (1,1)--(2,1), and P0=V(M0). This time retain only

    R'=T0 minus {g_i=(3,9+6i):0<=i<m}
           minus {v in T0: row(v)=4}.                 (1)

Thus all g/h/f permissions from the preceding theorem remain, and we also
permit withdrawal of (4,6),(4,6m+6),(4,6m+8). No old row-four selection is
required to remain. The terminal old row-three selection (3,6m+9) is retained.

**Theorem.** Let M be any actual grid matching with endpoint set P. Suppose
T and P are disjoint, every selected site has at most one occupied neighbour,
P0 subset P, and R' subset T. Then, for every m>=2,

    |T|+|M| <= 18m+29 = area/2-1.                     (2)

There are completely frozen configurations attaining equality for every m.
The upper bound permits arbitrary actual rematching and requires no freezing.
Any subclass retaining additional permitted selections also satisfies (2).

## 2. Available sites and a disjoint weighted partition

Black means even row+column. For free sites S define W(S) to be the number
of black new selections plus the number of white new occupied sites. Write
nt=T minus R', np=P minus P0. There are |R'|=5m+11 retained selections and
4m+5 white old endpoints. As every matching edge has one white endpoint,

    J=|T|+|M|=9m+16+W(U').                            (3)

The available set U' has 17m+23 sites. It is the disjoint union of:

* the enlarged pocket A'=A union {q=(4,5)}, where

      A={(2,3),(2,5),(3,3),(3,4),(3,5),(4,0),(4,2),(4,3),(4,4),
         (5,0),(5,1),(5,2),(5,3),(5,4),(5,5)};

* 2m pairs {(2,c),(3,c)}, for c=9+6i,11+6i and 0<=i<m;
* m blocks B_a, a=6,12,...,6m, consisting of both lower rows at columns
  a,...,a+5 and the one extra site (3,a+4);
* the seven-site right end

      E={(4,6m+6),(4,6m+7),(4,6m+8)}
         union {(5,6m+6),...,(5,6m+9)}.

For an all-length coordinate check, rows2 and3 of U' are exactly the pocket
sites plus the pair sites and the row3 block extras. Row4 contains every
column 0,...,6m+8 except 1, and row5 contains every column 0,...,6m+9.
All other non-R'/P0 sites are forced blank: row0 even columns; row1 column0
and 3+6j (0<=j<=m+1); row2 columns2,6m+9 and 4+6j,8+6j (0<=j<=m);
row3 columns0,2; row4 columns1,6m+9. There are no row5 forced blanks.
Every listed blank is adjacent to a retained selection already anchored by
P0. The unanchored row0 retained selections have all their neighbours in
that blank list. Hence nt and np lie in U', and no U' site touches R'.
These row lists prove the disjoint partition for every m, without periodic
identification of finite vertices.

Each pair has W<=1 by the old occupied neighbour of its black member.
The ordinary thirteen-site lemma of the
[integer compensation theorem](CONNECTED_BAND_INTEGER_COMPENSATION.md#2-a-local-inequality-with-six-selection-bits)
gives W(B_a)<=7. We need the equality case as well.

## 3. An exact boundary state for a saturated thirteen-site block

In B_a name the black selection bits and the white blank indicators

    x=t_(4,a), y=t_(4,a+2), z=t_(4,a+4),
    u=t_(5,a+1), v=t_(5,a+3), w=t_(5,a+5),
    A=1-o_(4,a+1), B=1-o_(4,a+3), C=1-o_(4,a+5),
    D=1-o_(5,a), E=1-o_(5,a+2), F=1-o_(5,a+4),
    G=1-o_(3,a+4).

Here o is free occupation; all these sites belong to U'. The necessary
conditions are

    x=1 => A=D=1;     y=1 => A=B=E=1;
    z=1 => B+C+F+G>=3;
    u=1 => A+D+E>=2;  v=1 => B+E+F>=2;
    w=1 => C+F>=1.                                   (4)

They imply S=A+B+C+D+E+F+G >= s=x+y+z+u+v+w, so W(B_a)=s+7-S<=7.
Both x and y have an old endpoint above them, including a=6.

**Boundary-state lemma.** Suppose x=0, D=1 and W(B_a)=7. Then necessarily

    y=z=0, u=v=w=1,
    A=B=C=G=0, E=F=1.                               (5)

This holds even for real blank variables in [0,1]. To prove it, equality
means S=s. If y=1, A=B=E=D=1 and C+F+G>=z+w, so S>=4+z+w>s.
Thus y=0. If z=1, D=1 and B+C+F+G>=3 give S>=4+A+E while s<=4.
Equality forces u=v=w=1,A=E=0, contradicting u's condition. Thus z=0.
If u=0,v=1, D+(B+E+F)>=3>s; if u=v=0, D+C+F>=1+w>s. Hence u=1.
If v=0, A+E>=1 and C+F>=w give S>=2+w>s, so v=1.
Adding the u,v conditions and using E<=1 yields A+B+D+E+F>=3.
Equality therefore forces w=1, S=3 and C=G=0. Now w's condition gives
F=1; D=F=1 and S=3 give A+B+E=1. Conditions A+E>=1 and B+E>=1
then force E=1,A=B=0. This proves (5).

Say that a block has input state if x=0 and D=1. By (5), a saturated block
with input state has its last bottom black site selected and its last upper
white site occupied. Consequently the next bottom white site is blank,
and the next upper black site cannot be selected because it has both this
occupied left neighbour and an old endpoint above it. Thus either the block
has weight at most six or it passes the same input state to the next block.
The statement includes the transition from B_(6m) into the right end.
For actual configurations W(B_a) is an integer, so a block that is not
saturated has weight at most six.

## 4. The left pocket can gain at most one unit, and then starts the state

Put r=(5,5), q=(4,5). We prove the two bounds

    W(A')<=9+t_r,           W(A')<=9+o_q.             (6)

For the second bound use the earlier pocket certificate 4W(A)<=39.
Removing the left boundary guard opens four additional edges out of A:

    (3,5)--q, (4,4)--q, r--q, r--(5,6).

Their endpoints inside A are all black. In the old weighted expansion their
coefficients are respectively 0,3,4,4, and they add only nonnegative terms.
The two white upper-port crossings still have coefficient four, and the old
black port has coefficient zero. Thus the old certificate remains valid
as 4W(A) plus nonnegative edge terms <=39. Since W(A) is integral, W(A)<=9,
and W(A')=W(A)+o_q proves the second bound in (6).

Here is a new certificate for the first bound. Let K_v=t_v and O_v=o_v
on A'. Add these valid inequalities with the indicated weights:

| Weight | Left side | Right side |
| ---: | --- | ---: |
| 1 | O_(2,3) | 1 |
| 4 | K_(3,3)+O_(2,3)+O_(3,4) | 2 |
| 1 | 2K_(3,3)+O_(2,3)+O_(3,4)+O_(4,3) | 3 |
| 4 | K_(3,5)+O_(2,5) | 1 |
| 2 | K_(3,5)+O_(2,5)+O_q | 2 |
| 2 | O_(4,2) | 1 |
| 2 | K_(4,2)+O_(4,3)+O_(5,2) | 2 |
| 3 | K_(4,4)+O_q+O_(5,4) | 2 |
| 1 | 3K_(4,4)+O_(3,4)+O_(4,3)+O_q+O_(5,4) | 4 |
| 6 | K_(5,0)+O_(4,0)+O_(5,1) | 2 |
| 2 | K_(5,2)+O_(4,2)+O_(5,3) | 2 |
| 2 | 2K_(5,3)+O_(4,3)+O_(5,2)+O_(5,4) | 3 |

Their weighted right sides total 58. Substitution of occupation as selection
plus actual matching incidence gives the exact identity

    weighted left side + 6t_r = 6W(A') + H,           (7)

where H is the nonnegative matching-edge sum

    4[ (4,2)--(4,3) ] + 2[ (4,2)--(5,2) ]
    +2[ (4,3)--(5,3) ] + 4[ (5,1)--(5,2) ]
    +2[ (5,3)--(5,4) ].

Brackets indicate membership in the single actual matching. Every selection
other than r has coefficient six, r has coefficient zero before adding 6t_r,
and every internal matching edge has coefficient six plus its H coefficient.
Every crossing at a white site of A' has coefficient six, and every crossing
at a black site has coefficient zero. This explicitly includes both old
upper-port mates, q--(4,6), and r--(5,6). Therefore
6(W(A')-t_r)<=58 and integrality gives W(A')<=9+t_r, proving (6).

In particular W(A')<=10. If it equals ten, (6) forces t_r=o_q=1.
The selected r already has occupied neighbour q, so (5,6) is blank. The
site (4,6) has old endpoint neighbour (3,6) as well as occupied neighbour q,
so it is not selected. Thus W(A')=10 starts the input state for B_6.
The local gain is a genuine possibility on every board in the family.
For any m>=2 take

    T=R' union {(2,3),(3,4),(4,0),(4,2),(4,5),(5,0),(5,3),(5,5)}.

From M0 delete (2,6)--(3,6) and (3,7)--(3,8), and add

    (2,5)--(2,6), (3,6)--(3,7), (3,8)--(4,8), (3,3)--(4,3).

These disjoint edges cover every old endpoint. Each of (2,3),(3,4) sees
only occupied (3,3); each of (4,2),(5,3) sees only occupied (4,3);
(4,0),(5,0) form one selected pair, and q,r form another. Retained selections
remain feasible because U' does not touch R'. This proves actual feasibility
for every m, and four black selections plus six white occupied sites give
W(A')=10. The example has J=9m+26 and makes no freezing claim. Thus the
proof genuinely compensates a possible extra unit instead of assuming it away.

## 5. The right end and the all-length compensation argument

In the seven-site right end put

    x=t_(4,6m+6), y=t_(4,6m+8),
    u=t_(5,6m+7), w=t_(5,6m+9),
    A=1-o_(4,6m+7), B=1-o_(5,6m+6), C=1-o_(5,6m+8).

The endpoint above each upper black site gives

    x=1 => A=B=1;    y=1 => A=C=1;
    u=1 => A+B+C>=2.                                 (8)

These imply A+B+C>=x+y+u: if x=y=1 all three blanks are one; if just
one is one its two blanks suffice for that bit and u; if neither is one
u's condition suffices. Hence W(E)<=3+w<=4.
If the incoming state x=0,B=1 holds, then W(E)<=3. Indeed, if y=1 then
A=C=1 and W(E)=1+u+w<=3. If y=0,u=1, then A+C>=1 and
W(E)=1+w+3-(A+1+C)<=3. If y=u=0, W(E)<=w+2<=3.

If W(A')<=9, sum the disjoint capacities directly:

    W(U')<=9+2m+7m+4=9m+13.

If W(A')=10, it starts the input state. If some B_a has weight at most six,
that single missing unit already compensates the extra pocket unit. Otherwise
every B_a is saturated, the state passes through all m blocks, and the right
end has weight at most three. In either case

    W(U')<=10+2m+7m+4-1=9m+13.

There is also a single counting inequality that expresses this propagation.
Let p_i be the 0/1 indicator of the input state at the start of block
B_(6+6i), 0<=i<m, and let p_m be the corresponding input-state indicator
at the right end. Put b_i=W(B_(6+6i)), L=W(A'), e=W(E). The preceding
lemmas give

    L<=9+p_0,
    b_i+p_i<=7+p_(i+1)       (0<=i<m),
    e+p_m<=4.                                       (9)

For the middle inequality, p_i=0 uses b_i<=7. If p_i=1 and p_(i+1)=0,
the equality propagation lemma forces b_i<=6; the remaining case uses
b_i<=7. Summing (9) cancels every state indicator exactly once, leaving

    L+sum_i b_i+e<=7m+13.                            (10)

The 2m pair contributions then give W(U')<=9m+13, and (3) proves (2).
Equivalently, sum_i(7-b_i)+(4-e)>=p_0>=L-9: the extra pocket unit is
paid by actual missing capacity, rather than being counted again as a
separate reserve. Assign it to the first deficient block or, if none,
to the right end. Pieces are disjoint and that unit is used only once.
No assumption of bounded compensation distance is made.

## 6. Sharpness, physical tokens and verification scope

The fully frozen all-g attainer from Section 4 of
[Joint selection withdrawal](SELECTION_WITHDRAWAL_SHARP_STRIPS.md#4-an-all-subset-frozen-attainer-with-no-circular-freezing)
has J=18m+29 and retains all old row-four selections. It belongs to the
larger permissions class (1), so the maximum in (2) is exact. Feasibility and
freezing are inherited from that proved construction, not from its cardinality.

The original aligned tile charge c(Q)=4-2|T intersect Q|-|P intersect Q|
has whole-board sum at least two, while the unchanged top strip has charge
-m. Therefore exterior positive half-unit tokens number at least
Cminus+m+2. Inject the exterior negative demands first and then the m strip
demands into these DISTINCT tokens. At least two tokens remain, with no
allocated token reused as a reserve. The same physical compensation conclusion
now holds with all three boundary guards optional.

The proof above is an all-length argument using explicit local inequalities,
their equality consequences, and induction along the open chain. Local finite
controls and finite-board matching models check the proof and its coordinates.
The accompanying Lean audits cover the boundary-state equality conditions,
right-end bounds, pocket coefficient/rounding identities, and arbitrary-length
state/counting induction. Coordinate-to-graph reductions and the inherited
frozen construction remain written proofs with independent finite controls.
A universal grid improvement of 5/6 still requires other endpoint footprints
and residual configurations; the present theorem enlarges this occupied-band
class and establishes its exact nonlocal compensation mechanism.


The saved [standard-library run](../output/boundary-withdrawal-compensation.json)
passes 549,822 enlarged-pocket models (139 have weight ten), 1,258 thirteen-site
models, 524 input states and 44 terminal models. Actual-board controls include
18 frozen sharp lengths through m=100 and 183 other matching models, including
four full-chain transmissions at m=2,3,4,8 and 18 controls of the explicit
all-m left-gain formula. All 201 boards satisfy the telescoping inequalities
and the original-tile token assignment. Ninety-nine change old matching edges;
159 omit all three former boundary guards.

All thirteen [Lean audits](../output/boundary-withdrawal-compensation-formal.json)
pass with Lean 4.33.0, using standard logical axioms and no custom mathematical
axioms or admitted proofs. The [Oracle review](../output/boundary-withdrawal-compensation-oracle.json)
returns **ACCEPT** for the written enlarged-class theorem and all-length state
argument; it does not execute Python or Lean. Its optional request to state
integrality explicitly has been incorporated. The telescoping reformulation
and extra actual models are recorded as subsequent independently checked
consequences of that argument.


A subsequent [terminal-guard extension](TERMINAL_GUARD_HALF_AREA_FRONTIER.md)
settles the unrestricted maximum when the last row-three guard is optional:
it increases to 18m+30=area/2. Its explicit sharp family is not completely
frozen, so it does not disprove the stronger bound for that subclass.
