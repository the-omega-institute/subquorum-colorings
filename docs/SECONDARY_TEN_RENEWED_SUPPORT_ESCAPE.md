# Renewed-support closure and the long positive tail escape

21 October 2026. This continues the [internal-consumer chain theorem](SECONDARY_TEN_INTERNAL_CONSUMER_CHAINS.md).
All originals retain their full matching, endpoint and original-support sets.
The functional is Phi=N+S+2F-E, with N the number of positive originals,
S their total negative mass, F the mixed full physical tiles and E the
owner-labelled intratile directed foreign events excluding original supports.
No charge or event resource is copied when a support is consumed.

## 1. Setting and statements

Use all hypotheses, coordinates and original owners of that theorem:
n>=1, independent even w_i>=12 and z_i>=24, odd a_0, even s_0,
even root breadth h>=6, and

    a_(i+1)=a_i+z_i-6,   s_(i+1)=s_i-w_(i+1)-12.

Its H1 contains the9n+1 base/root originals and the n zero-gain repairs
P_i^0=U(w_i+12,10,4), chart(a_i-8+r,w_i+13+s_i-c). Put

    q_i=(a_i-3,s_i+1),   r_i=(a_i-2,s_i+1).

Let R be the standard eight-endpoint rotor of the source catalogue. Adjoin
the following FULL originals, not just their local endpoints:

    Z_i=R,            chart(a_i-5+r,s_i-3+c),
    X_i=U(6,4,4),     chart(a_i+2-r,s_i+2-c),
    H2=H1 union {Z_i:0<=i<n},
    H3=H2 union {X_i:0<=i<n}.

**Zero-gain closure theorem.** These originals are pairwise endpoint-disjoint.
Every Z_i consumes q_i and has charge0, no new mixed full tile and no new
directed event. Every X_i consumes r_i, has charge-1 and adds exactly one
mixed full tile and three directed events. The increments hold simultaneously:

    Phi(H3)=Phi(H2)=Phi(H1)=sum_i(w_i+9)+h-1-n.       (1)

H2 has11n+1 originals and H3 has12n+1 originals. For every i, both H2 and
H3 are incomplete at the retained original support

    t_i=(a_i-4,s_i).

**Actual-consumer alternatives.** In any complete feasible original U/rotor
family containing H2, the actual owner of r_i is a fresh south-terminal U.
Writing its breadth H and its incident/other depths d,f, all even with
H>=6 and d,f>=4, leg exchange gives exactly two possible endpoint/support/
matching frames:

    left:  U(H,d,f), chart(a_i+d-2-r,s_i+2-c), charge-1;
    right: U(H,d,f), chart(a_i+d-2-r,s_i+c),   charge+1.     (2)

The right frame requires d>=z_i-2. If i<n-1, that same frame collides
with E_(i+1), so every interior r_i must have a left-frame owner.
All n actual owners are distinct: the r_i have the same checkerboard color
and the two terminals of one legal U have opposite colors. Consequently
at least n-1 distinct fresh charge-1 originals are forced by H2. This is
an ownership statement, not a net-compensation estimate for arbitrary owners.

**Long positive tail obstruction.** Put a=a_(n-1), s=s_(n-1), w=w_(n-1),
z=z_(n-1). For ANY even d>=z-2, the FULL original

    J=U(w,d,d-6), chart(a+d-2-r,s+c)                    (3)

is endpoint-disjoint from H2 and from all X_i with i<n-1. It consumes the
last r, has charge+1, and its EXACT increment relative to their union is

    DeltaN=1, DeltaS=0, DeltaF=2, DeltaE=9, DeltaPhi=-4. (4)

Thus the union with J in place of the last L has

    Phi=sum_i(w_i+9)+h-1-n-4.                         (5)

It is still incomplete at every t_i. This refutes the proposed endpoint-only
rule that a renewed-support consumer necessarily has nonnegative marginal
Phi. It neither refutes a rule with complete-extension hypotheses nor the
complete-model inequality or global5/6 target. Extendibility is not asserted.

## 2. Proof of simultaneous closure and retained incompleteness

Relative to (a_i,s_i), the endpoints of Z_i are

    (-4,-1),(-3,-1),(-3,0),(-3,1),
    (-2,-2),(-2,-1),(-2,0),(-1,0).

Its original supports are

    (-5,-1),(-4,-2),(-4,1),(-3,2),
    (-2,-3),(-1,-2),(-1,1),(0,0).

The single-source charge is0 by its four original matching edges and
its original-support/tile count. The endpoints do not meet H1: its eastern
tip q lies just below the P^0 far terminal; all other Z endpoints have
columns at most s_i. Its only possible old endpoint adjacencies are with
that P^0 terminal and with V_i's column s_i+2. The first crosses a physical
tile-row boundary; the second crosses a tile-column boundary. There is no
new intratile adjacency and no new mixed full tile. In particular no new
directed event is being discarded merely because its target became occupied.

The endpoints of X_i have near stem column s_i+1 and far stem column
s_i-4, between rows a_i-2 and a_i+2, and the two bar rows a_i+1,a_i+2.
The stems stop above at row a_i-2. They avoid Z and H1. The only new
mixed full tile is

    {a_i-3,a_i-2} x {s_i,s_i+1}.

Its three old cells are in Z_i, and its fourth is r_i in X_i. The exact
three new directed events are

    Z_i:(a_i-3,s_i+1) -> X_i:(a_i-2,s_i+1),
    Z_i:(a_i-2,s_i)   -> X_i:(a_i-2,s_i+1),
    X_i:(a_i-2,s_i+1) -> Z_i:(a_i-2,s_i).

The reverse event from r_i to q_i is excluded because q_i is X_i's
original axial support. At (a_i-1,s_i+1), the west Z endpoint is an
original X support, so it supplies no extra event. The far X stem has
column s_i-4, at least two columns left of every Z endpoint. Contacts
with V_i's column s_i+2 cross tile columns. Thus the lists are exhaustive.
The phase of X gives charge-1; its increment is1+2-3=0.

These local partitions persist in the full chain. All preceding B_j
have minimum column at least x_i=s_i+w_i+14. Preceding P_j^0 have
minimum column at least s_i+w_i+13. They are separated from Z_i and X_i
by columns. The root lies still farther right. For j>i, P_j^0 starts at row a_j-8>=a_i+10, and the body of B_j
starts at row at least a_i+12; its long stem starts no earlier than that
body's lower row bound. The new endpoints have maximum row a_i+2.
For new originals at adjacent indices, their row ranges are separated
by at least12: a_(i+1)-4>=a_i+14, whereas the current maximum is a_i+2.
No additional full tile or event is possible. This proves(1).

The point t_i is P_i^0's original far side support with intrinsic
coordinates(4,w_i+13). It is absent from both enlarged endpoint sets.
Its retained endpoint neighbors are

    west Z_i:(a_i-4,s_i-1),
    east P_i^0:(a_i-4,s_i+1),
    south Z_i:(a_i-3,s_i).

An unconsumed support with these three occupied neighbors contradicts
the required degree1. This proves incompleteness without counting other
unresolved support obligations.

## 3. Proof of the actual-owner alternatives

The absent r_i is V_i's original side support with intrinsic(4,w_i+11).
In H2 it has the three foreign endpoint neighbors

    north Z_i:q_i, west Z_i:(a_i-2,s_i),
    east V_i:(a_i-2,s_i+2).

Completeness therefore forces r_i to be consumed. The consuming original
can only have its own matching neighbor south. A U endpoint with exactly
one own endpoint neighbor is a leg terminal. Exchanging the full original
legs gives the two frames(2), with no depth restriction imported from an
enumeration. There are two full south-tip rotor possibilities. The first
contains V_i:(a_i-1,s_i+2), and the second contains Z_i:(a_i-1,s_i).
Both are excluded by endpoint disjointness. This exhausts the catalogue.

For clarity, the charge phases in(2) can be counted directly. Set
H=2b,d=2u,f=2v and R=a_i+d-2, which is odd. Both frames have
2b-1+u+v matching edges. For the right frame the endpoint-tile count is
b+1+u+v and the original-support-inside count is u+v+4, giving charge+1.
For the left frame those counts are b+u+v and u+v, giving charge-1.
Every count uses original supports, including ones subsequently consumed.

For the right frame, a bar endpoint lies in column s_i+2 at row
R-1=a_i+d-3. If d<z_i-2, evenness gives d<=z_i-4. This row is then
between a_i-4 and a_i+z_i-6, on V_i's retained far stem: a collision.
Thus d>=z_i-2. If i<n-1, the right frame's near stem, including its
top bar cell, covers column s_i+1 from row a_i-2 through
R>=a_i+z_i-4. The next block has

    E_(i+1):(a_(i+1),w_(i+1)+13+s_(i+1))
           =(a_i+z_i-6,s_i+1).

That retained endpoint belongs to the near stem, a contradiction. Right
escape is therefore a genuine tail alternative only. It is not missing
from the catalogue simply because short-depth controls cannot reach it.

All r_i have odd row and odd column, hence the same checkerboard color.
The full-original terminal-color lemma of the chain theorem proves their
owners distinct. They are outside H2 because every r_i is absent there.
This proves the stated fresh-owner consequence.

## 4. Exact tail debit and separation proof

For J in(3), the near stem has column s+1, starting at row a-2, and the
far stem has column s+w, starting at row a+4. Its bar rows are
R-1,R with R=a+d-2>=a+z-4. They lie below every local body, whose
last row is at most a+10. At the smallest d, the lower V terminal is
at row a+z-6, odd, while the upper J bar row a+z-5 is even: they lie
in different tile rows. For larger d they are farther separated.

The near stem avoids P^0, whose far terminal is at a-4; its other
old endpoints in the same tile column belong to Z. The far stem starts
below the D/L/T0/V bars. Q has columns at most s+11<s+w; at w=12,
its last tile column ends at s+11, before the J far column s+12. All C/E
stems have columns greater than s+w. W has its left bar column at
s+w+1, so it is adjacent to, and disjoint from, the J far stem.
All other potential old contacts cross tile boundaries or are separated.

For j<n-1, every B_j has minimum column at least s+w+14;
P_j^0 has minimum column at least s+w+13; Z_j has minimum column
at least s+w+10, and X_j at least s+w+8. J's maximum column is s+w.
These bounds give at least two columns of separation, even when J's long
legs overlap preceding row ranges. Thus no preceding owner contributes
to the new full-tile/event sets. There is no following block at the tail.

The three near-stem events are

    Z:(a-3,s+1) -> J:(a-2,s+1),
    Z:(a-2,s)   -> J:(a-2,s+1),
    J:(a-1,s+1) -> Z:(a-1,s).

The same three-old/one-new tile as in Section2 becomes full. Unlike X,
J's original side support at r is the west point, so its outgoing
event there is excluded; the third event is at the next stem endpoint.

The far-stem contacts with W give exactly the events

    W:(a+j,s+w+1) -> J:(a+j,s+w),  j=4,5,6,7,
    J:(a+j,s+w)   -> W:(a+j,s+w+1), j=5,7.

The two reverse events at j=4,6 are excluded by J's ORIGINAL side
supports. Each J target in this band has intrinsic W-row -1, so none belongs
to W's original-support set. This also holds at row a+2; there is no
exceptional west original support there. The only new full tile in this band is

    {a+5,a+6} x {s+w,s+w+1}.

The neighboring partial overlaps do not form additional full tiles.
The two tile lists and nine-event list are disjoint and exhaustive.
The direct charge count in Section3 gives N increment1 and mass
increment0. Thus1+2*2-9=-4, proving(4) and(5). The t_i blockers from
Section2 persist, so neither tail family is complete.

## 5. A simultaneous specified-owner compensation lemma

There is a full-original choice for all t_i-consumers that compensates the
original chain deficit, even with the negative tail. Set

    Y_i=U(w_i+14,6,4), chart(a_i-10+r,s_i-1+c).

**Specified-owner compensation lemma.** All Y_i are endpoint-disjoint from
one another and from H3. Each consumes t_i, has charge-(w_i+13), and its
increment relative to the whole simultaneous union is

    DeltaS=w_i+13, DeltaF=w_i/2+10,
    DeltaE=2*w_i+32, DeltaPhi=1.                     (6)

Consequently the exact two joint ledgers are

    Phi(H3 union all Y_i)=sum_i(w_i+9)+h-1,
    Phi(H2 union {X_i:i<n-1} union {J} union all Y_i)
                         =sum_i(w_i+9)+h-5.         (7)

The second has at least one unit beyond the sum of baselines because h>=6.
This is a conditional local compensation lemma when the specified Y_i
actually occur in the inventory. No existence or completeness assertion is
needed to calculate these full-original unions. It gives no monotonicity
claim for arbitrary further originals.

**Proof.** Work relative to (a_i,s_i), writing w=w_i. The Y bar occupies
rows-10,-9 and columns0..w+13. Its near stem is in column0 through row-4;
its far stem is in column w+13 through row-6. The only foreign original
with an intratile contact is P_i^0, whose bar occupies rows-8,-7 and
columns1..w+12, far stem is column1 through row-4 and near stem is
column w+12 through row2. The Y charge is1-(w+14)=-(w+13), by the
same north-terminal phase count as the accepted chain theorem.

The new full tiles have exactly the following lower-left coordinates in
this relative chart (tile row and column minima):

    (-9,2j),  j=0,...,(w+12)/2,
    (-7,0), (-5,0), (-7,w+12).

There are w/2+7 top-band tiles and three stem tiles. The new directed
events comprise the following disjoint lists:

    Y:(-9,c) -> P^0:(-8,c), and reverse, c=1,...,w+12;
    Y:(j,0) -> P^0:(j,1), j=-8,-6,-4;
    P^0:(j,1) -> Y:(j,0), j=-7,-5;
    Y:(j,w+13) -> P^0:(j,w+12), j=-8,-6;
    P^0:(-7,w+12) -> Y:(-7,w+13).

The first list has2(w+12) events, the others5+3. In the band the targets
have intrinsic non-stem row2 for Y, or row-1 for P^0, and are not original
supports. In the stem lists the omitted reverse directions are exactly
the original axial/bar-exterior or parity-dependent lateral supports.
These support tests use the original sets even though several supports
are already consumed. This proves the exact counts in(6).

To exhaust the exterior, local B_i endpoints have columns at least s_i+2
and rows at least a_i-6. Y's bar is above them and its near stem is to
their left. Its far stem ends at row a_i-6. The east rotor starts at
row a_i-1, and L/C/E/W start at row a_i or later, so none can reach that
stem. V and T0 have maximum
columns s_i+w_i+11 and s_i+w_i+10, respectively, to its left. D and Q
also lie to its left. Thus no local B endpoint shares an intratile edge
with Y. Z has no intratile adjacency to its tip t: Z's west neighbor
crosses a tile-column boundary and its south neighbor crosses a tile-row
boundary. X begins two rows below Y's last endpoint.

Preceding B_j have columns at least x_i=s_i+w_i+14, which is even;
Y's maximum column x_i-1 is in the preceding tile column. The root
also lies beyond that boundary. Preceding P^0/Z/X originals have maximum
row at most a_i-16, whereas Y starts at a_i-10. Subsequent originals
start below Y's last row a_i-4. Adjacent Y bar starts differ by at
least18, with a gap of at least12 between the previous Y's last endpoint
and the next Y's first endpoint. These bounds rule out any additional
event or shared full tile. They also prove all stated endpoint disjointness.

For the tail version, J starts at row a-2, two rows below the tail Y's
last endpoint; preceding Y's end still earlier. Thus J and all Y have
no intratile contact. The two tail full tiles from Section4 are also
disjoint from the Y lists. The exact increments sum, proving(7).

Both unions remain incomplete. For example the last block's retained
E original axial support u=(a-1,s+w+13), intrinsic(5,6), is still absent.
Its west P^0 endpoint(a-1,s+w+12), south E endpoint(a,s+w+13) and east
upper-consumer endpoint(a-1,s+w+14) persist. The upper consumer is the
root if n=1 and V_(n-2) otherwise. No Y or J reaches u. Thus at least
three occupied neighbors still force a later consumer; even the compensated
inventory has not been promoted to a complete-family theorem.

This identifies a genuine compensation mechanism for an entire specified
chain: a later forced owner can repay a deficit that earlier forced owners
left unchanged or worsened. It does not assert that an arbitrary actual
t_i-consumer has the receipt(6). That is the next all-parameter question.

## 6. Meaning and verification scope

This proves an arbitrary-length simultaneous closure result beyond the
previous one-stage repair. It also isolates why a depth18 catalogue was
insufficient: the right frame first clears V at d=z-2>=22, changes charge
phase, and can lose four units through the already occupied W band.
The interior-chain exclusion is a new necessary condition, not a claim
that arbitrary left consumers have zero marginal contribution. Only the
explicit L family has that conclusion.

The global question still needs a common allocation and control of all
remaining mandatory support consumers. Before the specified Y_i are adjoined,
t_i supplies a specific next obligation for both families; after compensation
the displayed remaining obligation is u. No finite catalogue substitutes
for the general arguments above. The submitted11October DMGT manuscript,
the primary star-forming results and the global5/6 target are unchanged.

The companion checker independently reconstructs full originals and compares
exact mixed-tile and owner-labelled event sets, including nonuniform chains,
long legs, both terminal frames and the excluded rotor roles. The standalone
Lean source certifies local blocker coordinates, unbounded collision bounds,
terminal parity and receipt arithmetic. General role completeness, charge
counts and exhaustive event partitions remain ordinary proofs, not end-to-end
Lean formalization.

Validation:144 single-block parameter controls,72 source parameter triples
giving280 full-original south-terminal roles and144 charge-phase controls,
36 below-threshold collisions, both full south-tip rotor exclusions and
eight tile-preserving isometries PASS. Three simultaneous chains of8,7,24
blocks check exact full-tile/event SETS for zero closure, negative tail and
both compensation ledgers, with648 interior-collision and432 preceding-column
separation controls. The8-block example has baseline168, zero-closure Phi165,
negative-tail Phi161, and compensated values173 and169 respectively.

All36 declarations, including30 theorems, in the
[standalone Lean source](../formal/SubQuorum/SecondaryTenRenewedSupportEscape.lean)
pass locally with every individual axiom list inspected, no warnings and no
sorry/native axioms. The [exact-set receipt](../output/secondary-ten-renewed-support-controls.json)
and [Lean receipt](../output/secondary-ten-renewed-support-lean-validation.json)
record their execution scopes. The first written-review task failed during
typing with infrastructure_retry_exhausted and no mathematical review. The
fresh self-contained written review, INCLUDING Section5, completed ACCEPT.
Two geometric descriptions are corrected: Q is excluded by tile columns
and every W target has intrinsic row -1. No hypothesis, formula or event
list changes. Focused controls check24 Q/J disjoint tile sets, including
eight width12 boundaries, and120 W targets at intrinsic row -1; the
[review receipt](../output/secondary-ten-renewed-support-review.json) records
the accepted ordinary-proof scope separately from execution.
