# A forced four-row support staircase and a sharper geometric frontier

22 October 2026. Owner: Wenlin Zhang and Haobo Ma. Status: general written
proof with independent full-original controls; scoped Lean and independent
review are recorded separately. The explicit every-original full-U/rotor
model, H3 construction and specified B,R,A are exactly those of the
[fourth-owner theorem](SECONDARY_TEN_ROOT_FOURTH_CONSUMER.md). This is a
necessary consequence of complete feasibility, not arbitrary-grid exhaustion.

## Forced chain and necessary depth-height tradeoff

Put P=C-1=s+u+12, q=u+v+24 and

    p_i=(a-9-i,P), i=0,1,2,3.

Every complete extension containing the specified B,R,A has FOUR distinct
fresh originals J_i consuming p_i, all west-terminal U's with downward
bars. Their full charts are

    J_i=U(H_i,D_i,G_i),
    (r,c) -> (a-10-i+c,P-D_i+r).

J_0 is the fourth owner previously called J. All H_i,D_i,G_i are even,
H_i>=6,G_i>=4. For i=1,2,3 the following are necessary:

    D_i>=D_(i-1)+2, D_i<=q-2,
    H_i<z+i-4;                                     (1)
    H_i>=H_(i-1)+2 OR D_i>=D_(i-1)+G_i+2.            (2)

In particular D_0<=q-8=u+v+16. The narrower A frontier is

    L<=v OR (L=v+2 AND f<=z-12).                     (3)

Conversely, within the earlier A ranges, (3) is equivalent to the
existence of an endpoint-disjoint four-original staircase avoiding
every retained H3,B,R,A. This converse concerns geometric existence only;
it is not existence of a complete extension.

For the explicit geometrically sufficient choices (4), a single exact
seven-owner ledger relative to H3 gives

    DeltaPhi=v/2+L/2+10-3*epsilon>=19,
    epsilon=[L=v+2 AND f=z-12].                       (5)

This is a compensation theorem for that specified family. An arbitrary
actual staircase need not have the parameters (4), so (5) is not an
allocation theorem for every complete family.

## Proof of forced owners and frame exhaustion

The fourth-owner theorem already gives J_0. Write b_i=P-D_i. Its
original lateral support at the incident terminal is p_1: the canonical
support (D_0,0), since D_0 is even. More generally J_(i-1)'s canonical
support (D_(i-1),0) is exactly p_i. The site p_i is absent from all
previous retained originals. H3 starts at row a-8 or lower; A has
columns at most s; R has columns at least C. At these three rows B has
only its two stems at s1 and C. Earlier J_j have their incident rows
strictly below p_i, their bars strictly left of P, and far rows still
lower, so they also miss p_i.

For i=1,2,3 the east neighbor (a-9-i,C) is a B far-stem endpoint,
and the south neighbor p_(i-1) belongs to J_(i-1). Completeness therefore
forces an actual new owner of p_i. Its own neighboring endpoints must
lie north or west, leaving north terminals, west terminals and the two
degree-two outer-corner orientations as the full-U possibilities.

A north terminal and either north/west corner contain the northward
ray through distance at least4. It meets (a-13,P), B's lower bar, at
distance4-i, which is between1 and3. All four guard-compatible rotor
tips also collide: two contain p_i+(-2,1) or p_i+(-1,1), both B
endpoints; the other two contain p_i+(1,-1) or p_i+(1,-2), endpoints
of the previous incident ray. Non-tip rotor roles hit an immediate
foreign guard. Only a west-terminal full U is possible.

If D_i>=q, its incident ray meets B's near stem at s1. Hence D_i<=q-2
by evenness and b_i>=s1+2. A bar pointing upward then hits B's lower
bar at (a-13,b_i): its northward breadth H_i>=6 reaches that row, and
b_i lies within the B bar interval. Therefore every bar points downward.
These arguments are uniform in all far lengths and component breadths.

At row a-8-i, the new bar endpoints b_i,b_i+1 must avoid the previous
incident ray [b_(i-1),P]. Since b_i+1<P, avoidance forces
b_i+1<b_(i-1). All b_i are even, proving D_i>=D_(i-1)+2. Every
J_i is distinct and fresh because p_i was absent from all preceding
full endpoint sets. This proves the induction through i=3. The next
support p_4=(a-13,P) is already a B endpoint, so this particular forced
vertical chain ends there; other mandatory supports may remain.

## Height constraints and the tradeoff

Every b_i lies between s1+2 and s-L-2, since D_i>=D_0>=u+L+14.
Thus b_i and b_i+1 are within P1's bar interval [s1+1,s]. Its first
row is a+z-14. J_i's bar ends at a-10-i+H_i. It must end strictly
above P1, giving H_i<z+i-4. In particular H_3<=z-2 by evenness.

If H_i<=H_(i-1), the new far row a-10-i+H_i lies within the previous
two-column bar: it is at least four rows below that bar's top, and
at least one row above its bottom. The new far ray [b_i,b_i+G_i]
must stop before b_(i-1). Consequently

    b_i+G_i<b_(i-1),
    D_i-D_(i-1)>=G_i+2

by evenness. Otherwise H_i>=H_(i-1)+2. This proves (2); a short
bar cannot be compensated by reusing an already occupied corridor.

## Sharper frontier, including an explicit converse

Three strict depth steps and D_3<=q-2 give D_0<=q-8. Together with
D_0>=u+L+14 this yields L<=v+2. If L=v+2 then all inequalities are
tight:

    D_i=u+v+16+2i.

The first far-depth cap of J_0 would give G_0<=2 if H_0<=f+2.
Since G_0>=4, H_0>=f+4. At each later step the depth increment2 is
too small for the second alternative of (2), as G_i+2>=6. Therefore
H_i>=H_(i-1)+2 and H_3>=f+10. Combining H_3<=z-2 yields f<=z-12.
Evenness leaves precisely (3).

For the converse choose D_i=u+v+16+2i and G_i=4, and choose

    H_i=6+2i                  if L<=v;
    H_i=f+4+2i               if L=v+2,f<=z-12.       (4)

Every bar column is b_i=s-v-4-2i, hence s1+2<=b_i<=s-v-4. The
four bars are pairwise separated by two columns and lie strictly between
B's near stem and A's far stem. Their near rows lie above H3 and A.
Their far rows are successive rows starting at a-4 in the first case,
or a+f-6 in the second case. Later bars lie left of every earlier
horizontal ray; later far rows lie below the earlier bar endpoints.
This proves pairwise endpoint-disjointness of all four new originals.

In the first case the largest far endpoint column is E_0=s-v<=s-L=F-1,
strictly left of A. All new bar and far columns are also left of every
other first-block endpoint: X0's leftmost column is s-4, and the west
rotor's is s-2. In the second case all far rows lie below A's far
terminal and all far columns are at most s-v<=s-12, left of X0 and
every other first-block original. The last bar row is at most a+1
in the first case, or a+f-3<=a+z-15 in the second. Both precede P1's
first endpoint row a+z-14, and every later block starts still lower.
B's bar is above all new originals, its near stem left of every bar,
and its far stem at C right of every new endpoint. R's columns are
at least C. These checks exhaust all retained originals uniformly in
root breadth, R far length, later dimensions and chain size. They
prove the geometric converse without a bounded enumeration.

## Exact seven-owner compensation for the explicit family

Use precisely (4), write N=u+L+12, D1=u+v+18, D3=u+v+22,
and keep the ORIGINAL support sets when counting directed foreign
intratile events. Charges of J_0,J_1,J_2,J_3 are -1,+1,-1,+1:
translating the incident row by one changes its physical tile phase;
the even terminal column and the rotated canonical supports give the
same two alternating phase calculations as in the fourth-owner theorem.
Their additions to S and N are respectively (1,0),(0,1),(1,0),(0,1).

The complete incremental physical receipt counts are

| New owner | New full mixed tiles | New directed events | Phi marginal |
|---|---|---|---|
| J_0 | N/2 | 3N/2 | 1-N/2 |
| J_1 | 0 | 1 | 0 |
| J_2 | D1/2+2 | D1+4 | 1 |
| J_3 | D3/2+1+2epsilon | 3D3/2+2+7epsilon | 1-D3/2-3epsilon |

J_0 is the already proved fourth-owner receipt, with both three-owner
tiles included. For J_1, all near/far contacts with J_0 cross physical
tile-row boundaries, and their adjacent bar columns cross tile-column
boundaries. The only new event is B:(a-10,C)->J_1:(a-10,P). The
reverse direction targets J_1's original axial support. It gives no
full tile, so N's new unit exactly pays this event.

For J_2 put b1=s-v-6. Its near row a-11 is even and J_1's near row
a-10 is odd. New full tiles have minima(a-11,c), c=b1,b1+2,...,P,
giving D1/2+1 tiles. The last one is completed with B's far stem at C
and is counted once. Each column b1..P contributes exactly one directed
event, J_2->J_1 at even columns and J_1->J_2 at odd columns. There are
D1+1 such events; opposite directions target original lateral supports.

The two far rows are consecutive in one physical tile row, with J_1
above J_2. Write r=a+H_0-9, an even row. Their overlap columns are
b1,b1+1,b1+2. They complete precisely the tile(r,b1) and give three
events: J_2->J_1 at the two even columns and J_1->J_2 at the odd
column. The next tile is partial. Together the near and far receipts
give D1/2+2 full tiles and D1+4 events. All other J_2 contacts cross
physical tile boundaries or target original axial/lateral supports.

For J_3 put b3=s-v-10. Its odd near row a-12 shares a physical tile
row with B's lower bar at even row a-13. Full tile minima are
(a-13,c), c=b3,b3+2,...,P, giving D3/2+1. Events are B->J_3 at
all columns b3..P, J_3->B at the odd columns, and the additional
horizontal event B:(a-12,C)->J_3:(a-12,P). The original axial support
excludes the reverse horizontal direction. These give 3D3/2+2 events.

The only extra receipt occurs when epsilon1. Then J_3's far row is
a+z-15, even, directly above P1's upper bar at a+z-14, odd. Its
five endpoint columns b3..b3+4 complete exactly two tiles with minima
(a+z-15,b3),(a+z-15,b3+2). P1->J_3 contributes all five vertical
directions and J_3->P1 contributes the two odd columns. The three
other reverse directions target J_3's original lateral/bar supports.
Thus this boundary contributes two tiles, seven events, net loss3.
If epsilon0, the far physical tile row is separated from P1 and all
later originals. The bar corridors remain tile-separated from B's near
stem and the earlier bars; far contacts other than J_1/J_2 are separated
by tile rows or columns. These geometric separations exhaust receipts.

All listed tile minima are distinct or belong to distinct insertion
stages where at least one new endpoint was absent. Every new event
contains the new owner's endpoint and targets a foreign endpoint outside
the source's original support set. Old events persist. Hence each
original charge, physical tile and labelled event is used once. Adding
the preceding exact triple ledger gives

    DeltaS=u+v+L+26, DeltaN=3,
    DeltaF=11+(N+D1+D3)/2+2epsilon,
    DeltaE=24+3N/2+D1+3D3/2+7epsilon.

Substitution proves (5). If epsilon0, v>=12,L>=6 give at least19.
If epsilon1, L=v+2 gives v+8>=20. This proves the uniform19 lower
bound for the whole specified family, with no finite cutoff and no
assumption of nonnegative insertion marginals.

## A seven-owner obstacle to positive-marginal closure

For a31,s0,u=v12,z24,L6,f4 and the original h6,R=U(8,8,4), the
four new horizontal dimensions in (4) are

    (6,40,4), (8,42,4), (10,44,4), (12,46,4).

Their immutable charges are -1,+1,-1,+1. Starting from H3+B+R+A,
their successive exact Phi marginals are -14,0,+1,-22. The total
seven-owner increment relative to H3 is19, with one physical union
having DeltaS56,DeltaN3,DeltaF70,DeltaE180:

    56+3+2*70-180=19.

This witness meets the whole top-support staircase and consumes its
last support in B, yet another positive original can debit the union
by22. Closing one forced support chain does not establish a nonnegative
closure rule. This is an explicitly partial inventory; its other forced
supports are unresolved, so it is not a complete-family counterexample
or a counterexample to the target global inequality.

The [full-original verifier](../develop/check_secondary_ten_root_support_staircase.py)
checks explicit geometric witnesses, absent original supports, east/south
guards, all three new steps, rotor collisions, necessary depth-height
constraints and the exact seven-owner example. Finite controls are
separate from the proof above. Scoped Lean supports the coordinate
obstructions and frontier arithmetic; component-role exhaustion and
the geometric converse remain written. This theorem was NOT in the
fourth-owner independent-review request. General complete-family
allocation, global5/6 improvement and rectangular-grid equality remain OPEN.
