# Exact integer compensation for the connected occupied band

26 October 2026. Wenlin Zhang and Haobo Ma. Research note.

We prove the exact maximum **18m+29** for the simultaneous G/H/F withdrawal
permissions of the connected-band problem, with every old endpoint retained
and with arbitrary actual rematching. A chessboard count replaces separate
component charges. A disjoint cover bounds the long component, and a new
weighted certificate bounds the fixed pocket. The earlier fractional matching
obstruction survives: integrality of selections supplies the missing step.

## 1. The finite board and theorem

Let m>=2 and work on the grid {0,...,5} x {0,...,6m+9}, with edges between
sites at Manhattan distance one. Set k=m+1. Translate each of

    Tcore={(0,2),(0,4),(1,1),(1,5),(4,3),(4,5),(3,6)},
    Mcore={(1,2)--(1,3),(1,4)--(2,4),
           (2,3)--(3,3),(3,4)--(3,5)}

by (0,3+6j), 0<=j<k. T0 is the union of the translated selections, together
with {(0,3+6j):0<=j<=k} and {(0,1),(1,2),(2,0),(3,1)}. M0 is the union of
the translated matching edges and {(1,1)--(2,1)}. Put P0=V(M0), and

    g_i=(3,9+6i), h_i=(4,8+6i)                 (0<=i<m),
    f_i=(4,12+6i)                             (0<=i<m-1),
    R=T0 minus {g_i,h_i:0<=i<m} minus {f_i:0<=i<m-1}.

These are permissions, so permitted selections may be restored.

**Theorem.** Suppose M is an actual grid matching with endpoint set P,
T and P are disjoint, every selected site has at most one neighbour in
T union P, and R subset T and P0 subset P. Then

    J=|T|+|M| <= 18m+29 = area/2-1.                    (1)

For every m>=2 equality is attained by a completely frozen configuration.
The upper bound does not assume freezing or retention of old matching edges.
In particular all subclasses obtained by retaining more of g,h,f satisfy (1).
The exact maximum assertion concerns the displayed full permissions class.

### 1.1 Available sites and the matching colour identity

A retained selection adjacent to P0 already has its one occupied neighbour,
so all its other neighbours are forced blank. Inspection of the displayed
rows gives |R|=5m+14, |P0|=8m+10 and the available set U, disjoint from R,P0:

    C_m row2: 9+6i,11+6i                       (0<=i<m)
        row3: 9+6i,10+6i,11+6i                (0<=i<m)
        row4: 8,...,6m+4
        row5: 7,...,6m+5;
    A={(2,3),(2,5),(3,3),(3,4),(3,5),(4,0),(4,2),(4,3),(4,4),
       (5,0),(5,1),(5,2),(5,3),(5,4),(5,5)};
    I={(5,6m+7),(5,6m+9)}.

Thus U=C_m disjoint-union A disjoint-union I; |C_m|=17m-4. No U site
is adjacent to R. Conversely all new selections and new endpoints lie in U.
To check the boundary for all m, rows0,1 have no available sites; the two
isolated row2 sites above each slot join the three row3 sites, and rows4,5
are exactly the two stated intervals. The retained terminal lower guard
forces (4,6m+5) blank. The leftmost retained lower guard is (4,6).
These also separate A and I from C_m. The only A sites adjacent to P0
are (2,5), with two such neighbours, and (3,5), with one.

Call a site black when r+c is even, and white otherwise. For S subset U put

    W(S)=| (T minus R) intersect S intersect black |
           +| ((T minus R) union (P minus P0)) intersect S intersect white |.

Every actual grid edge has one endpoint of each colour. Therefore
|P intersect white|=|M|, and since |P0 intersect white|=4m+5,

    J=|R|+|P0 intersect white|+W(U)=9m+19+W(U).         (2)

This uses the actual global matching once, even when it crosses from U into
P0. It requires no independent matching capacities for individual components.
It remains to show W(C_m)<=9m-1, W(A)<=9 and W(I)<=2.

## 2. A local inequality with six selection bits

Let x,y,z,u,v,w be binary, and let A,B,C,D,E,F,G be real numbers in [0,1].
Assume

    x=1 => A=D=1;
    y=1 => A=B=E=1;
    z=1 => B+C+F+G>=3;
    u=1 => A+D+E>=2;
    v=1 => B+E+F>=2;
    w=1 => C+F>=1.                                  (3)

Then

    A+B+C+D+E+F+G >= x+y+z+u+v+w.                    (4)

Here is a proof valid for real blanks, with no enumeration assumption.
If y=1, A=B=E=1 and D>=x. The z and w implications give
C+F+G>=z+w: if z=1 this sum is at least 2, since B<=1; if z=0 the w
condition suffices. Thus the total is at least 3+x+z+w, which covers the
selection sum since u+v<=2.
If y=0,z=1, the disjoint group B+C+F+G contributes at least 3. If either
x or u is one, A+D+E contributes at least 2, covering all five possible
bits; otherwise the first three units cover z+v+w.
If y=z=0,x=1, A=D=1. When v=1 the disjoint group B+E+F contributes
at least 2, covering x+u+v+w. When v=0, C+F>=w supplies what remains.
Finally take x=y=z=0. If u=v=1, adding their conditions and subtracting
the shared E<=1 gives A+B+D+E+F>=3, enough even for w=1. If exactly
one of u,v is one, its two units cover that bit and w. If neither is one,
the w condition proves (4).

There is also a strengthened left-boundary form: if x=0 and A=D=1,
then the total in (4) is at least x+y+z+u+v+w+1. For y=1 there are
four fixed blank units A,B,D,E, plus z+w from C,F,G. For y=0,z=1,
A+D=2 and B+C+F+G>=3 give five, covering 1+z+u+v+w. For y=z=0,
if v=1 use its two units disjoint from A,D; otherwise use C+F>=w and
u<=1. These cases prove the strengthened inequality.

### 2.1 Embedding and disjoint cover of the open band

For even a write t for selection and o for occupation. Instantiate (3) by

    x=t_(4,a), y=t_(4,a+2), z=t_(4,a+4),
    u=t_(5,a+1), v=t_(5,a+3), w=t_(5,a+5),
    A=1-o_(4,a+1), B=1-o_(4,a+3), C=1-o_(4,a+5),
    D=1-o_(5,a), E=1-o_(5,a+2), F=1-o_(5,a+4),
    G=1-o_(3,a+4).

For a=12,18,...,6m the sites x,y each have an occupied old endpoint above
them; z has four neighbours, u,v have three, and w has at most one
occupied neighbour. Ignoring the left outside neighbour of x and the right
outside neighbour of w only weakens the necessary conditions (3). Thus (4)
bounds the coloured weight of these thirteen sites by 7. At a=6m, the
site (4,a+5) is a forced blank; adding its zero occupation does not change
W. In particular no periodic identification of finite sites is used.

The remaining lower-left ten sites are

    L={(3,10)} union {(4,c):8<=c<=11} union {(5,c):7<=c<=11}.

Use the strengthened inequality at a=6, with x=0 as a selection increment
(the physical site (4,6) belongs to R), and A=D=1 because (4,7),(5,6)
are forced blank. The y anchor is still present. Conditions for z,u,v,w
remain valid after ignoring any outside occupied neighbour. The thirteen
formal terms consist exactly of the ten L terms and three zero terms.
Hence W(L)<=6.

For each i, d_i=(2,9+6i) is white and g_i=(3,9+6i) is black with an old
endpoint neighbour. Thus o_(d_i)+t_(g_i)<=1. The same argument gives
 o_(2,11+6i)+t_(3,11+6i)<=1. These 2m pairs, L, and the m-1 thirteen-site
blocks cover every weighted site of C_m exactly once. Different blocks
use distinct row3 extras, and their six-column lower intervals are disjoint.
Consequently

    W(C_m)<=2m+6+7(m-1)=9m-1.                        (5)

## 3. A pocket certificate that includes both matching ports

Write U0=(2,5) and V0=(3,5). The only possible matching crossings of A
are at U0,V0 and go into P0. Let e be the number of internal matching
edges and x_U the 0/1 indicator of a crossing at U0. Each internal edge
has one white endpoint; V0 is black, U0 white. Hence

    W(A)=|T intersect A|+e+x_U.                       (6)

All indicators here count selections in A, which is disjoint from R.
Let K_v denote t_v and O_v denote o_v. Add the following valid inequalities,
with the indicated weights. A wedge has the form K_v+O_a+O_b<=2.

| Weight | Left side | Right side |
| ---: | --- | ---: |
| 1 | O_(2,3) | 1 |
| 2 | K_(3,3)+O_(2,3)+O_(3,4) | 2 |
| 1 | 2K_(3,3)+O_(2,3)+O_(3,4)+O_(4,3) | 3 |
| 4 | K_(3,5)+O_(2,5) | 1 |
| 1 | K_(4,2)+O_(4,3)+O_(5,2) | 2 |
| 1 | K_(4,4)+O_(3,4)+O_(4,3) | 2 |
| 4 | K_(5,0)+O_(4,0)+O_(5,1) | 2 |
| 3 | K_(5,2)+O_(4,2)+O_(5,3) | 2 |
| 1 | K_(5,3)+O_(4,3)+O_(5,4) | 2 |
| 3 | K_(5,4)+O_(4,4)+O_(5,5) | 2 |
| 1 | O_(5,5) | 1 |

The third row is the three-neighbour selected-degree inequality; the fourth
uses the old occupied neighbour of V0. The weighted right sides total 39.
Substitute O_v=K_v+sum of actual incident matching indicators. Every K_v
has coefficient 4, and every internal edge has coefficient at least 4.
The exact expansion is

    weighted left side = 4W(A)+3H+E0,                 (7)

where H counts internal matching edges in

    {(3,4)--(4,4), (4,2)--(4,3),
     (4,3)--(4,4), (4,3)--(5,3)},

and E0 counts edges {(5,1)--(5,2),(5,4)--(5,5)}. Each crossing at U0
has coefficient 4, whether its outside mate is (1,5) or (2,6); a crossing
at V0 has coefficient 0. All edges are counted from the single actual
matching. Since H,E0>=0, (7) proves 4W(A)<=39; W(A) is integral, so

    W(A)<=9.                                         (8)

This proves the formerly delicate U0-only case as well. It replaces the
previous pocket half-unit slack by a bound suited to the global colour count.

## 4. Sharpness and physical compensation without duplicate credit

Both isolates are black and contribute at most one each. Equations (5),(8)
give W(U)<=9m+10, and (2) proves (1).

For equality take the established fully frozen g-withdrawal attainer with
k=m+1 and every g permission used. It retains all h_i and f_i, so belongs
to the present larger class. Explicitly begin with the sharp completion
(T*,M0) in the [completion note](FROZEN_STRIP_SHARP_COMPLETION_AND_RESERVES.md).
Writing b=6k+4 for the width, its selections are explicitly:

| Row | Selected columns |
| --- | --- |
| 0 | odd columns 1,...,b-1 |
| 1 | 2 and 4+6j,8+6j, for 0<=j<k |
| 2 | 0,3 |
| 3 | 1,3 and 5+6j,9+6j, for 0<=j<k |
| 4 | even columns 0,...,b-2 |
| 5 | 0 and odd columns 3,...,b-1 |

The completion has |T*|=13k+11 and retains T0.
For c_i=9+6i remove selections (3,c_i),(3,c_i+2), add selection (2,c_i),
and add edges (3,c_i)--(3,c_i+1) and (2,c_i+2)--(3,c_i+2), for every i<m.
The slots are disjoint. Each step decreases |T| by one and increases |M|
by two, so J=17k+12+m=18m+29. The earlier frozen certificate applies;
the verifier checks it independently on the actual boards.

For each original aligned 2-by-2 tile Q define the integer half-unit charge

    c(Q)=4-2|T intersect Q|-|P intersect Q|.

The top two-row strip is unchanged and has total charge -m. The whole-board
charge is area-2J>=2 by (1). Thus the exterior tiles have total charge at
least m+2. If Cplus and Cminus are the sums of positive charges and of
absolute negative charges on DISTINCT exterior tiles, then

    Cplus >= Cminus+m+2.                              (9)

Create c(Q) separate tokens (Q,j) on each positive tile. Pay each negative
exterior half-unit first, then the m half-units of net strip deficit, by
injecting this ordered demand list into the ordered positive token list.
At least two tokens remain. The injection uses each physical token once;
no credit allocated to an exterior debt is reused for the strip or reserve.
This is a global compensation statement, with no directional routing claim.

## 5. Verification and scope

The proof above holds for every m>=2. Enumeration is used to check local
identities and finite actual-board controls, not to extrapolate (1).
The standard-library checker verifies the pocket identity coefficient by
coefficient, the local implications, the disjoint coordinate cover, matching
colour accounting, frozen sharp attainers, randomized actual rematchings,
and the original-tile token assignment. The saved run checks 147,297
pocket partial-matching models, 3,139 local implication models, 496 left
boundary controls, 20 frozen sharp attainers at lengths through m=100,
and 144 actual rematching models (62 change old matching edges). All pass.

The accompanying Lean file formalizes the local inequalities at every natural
scaling, the pocket coefficient identity and rounding, and the all-m arithmetic
and compensation accounting. The coordinate decomposition, graph feasibility,
and universal frozen construction are proved in the written argument and
checked on finite boards by Python; they are not claimed as fully formalized
graph theorems in Lean. All ten Lean theorems pass with Lean 4.33.0;
they use standard Lean logical axioms, with no custom mathematical axioms
or admitted proofs. See the [formal receipt](../output/connected-band-integer-compensation-formal.json)
and [finite validation receipt](../output/connected-band-integer-compensation.json).

The [preceding fractional construction](CONNECTED_BAND_SIMULTANEOUS_MATCHING_BARRIER.md)
exceeds (1) for m>=18 while satisfying all simultaneous matching capacities.
There is no conflict: (3)--(4) uses integral selection bits, and (8) uses an
integer pocket count. The new theorem closes the displayed mixed-direction
connected-band class and supplies a full unit of surplus there. A universal
improvement of the manuscript's 5/6 bound still requires a reduction covering
other residual configurations; that further statement is not inferred here.
