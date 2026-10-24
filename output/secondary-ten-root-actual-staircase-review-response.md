ACCEPT — under the explicit conditional hypothesesThe stated inequality is correct:
$$\boxed{\Phi(H_3+B+R+A+J_0+J_1+J_2+J_3)-\Phi(H_3)
\ge \frac L2-1\ge2.}$$
The coordinate geometry supports the receipt allocation for all allowed dimensions. In particular, the proof correctly uses a single shared width budget for the  $P_1$  band, and its credited full tiles cannot be reused by another receipt group.There is one presentational subtlety worth making explicit: the first upper row has an event in a nonfull boundary tile. That event is already included in the asserted total  $3\nu/2$ , so it does not invalidate the calculation. The list of full tiles must not be read as a list of every tile carrying an event.Below is a coordinate proof of the new estimate. It uses the accepted triple gain and the assumed charts, rather than finite enumeration or the earlier specified-family bound.1. Endpoint normal form and immutable chargesLet
$$\mathcal O=H_3+B+R+A,\qquad
\mathcal U=\mathcal O+J_0+J_1+J_2+J_3.$$
For each staircase original, put
$$q_i=a-9-i,\qquad
p_i=a-10-i+H_i,\qquad
b_i=P-D_i,\qquad
e_i=b_i+G_i.$$
Its endpoint set is exactly
$$\begin{aligned}
J_i={}&
\bigl([q_i,p_i]\times\{b_i,b_i+1\}\bigr)\\
&\cup\bigl(\{q_i\}\times[b_i,P]\bigr)
\cup\bigl(\{p_i\}\times[b_i,e_i]\bigr),
\end{aligned}$$
where all intervals here are integer intervals. Thus its bar occupies an aligned two-column physical tile column, and its near and far rows carry uninterrupted horizontal intervals.The depth conditions imply
$$s_1+2=s-v-10
\le b_3\le b_i
\le s-L-2-2i.
\tag{3}$$
In particular, all bar tile columns lie strictly between the tile column of  $B$ 's near stem and the tile column of  $A$ 's far stem.All of  $b_i,e_i,P$  are even. The row phases are:Index  $i$ Near row  $q_i$ Far row  $p_i$ EvenEvenOddOddOddEvenSet
$$t=a+z-15,$$
which is even. Using both the strict height bounds and the evenness of  $H_i$ , one obtains
$$p_0,p_2\le t-1,\qquad p_1,p_3\le t.
\tag{4}$$
Also,
$$p_i\ge a-4-i\ge a-7.
\tag{5}$$
Consequently, no far endpoint occurs in the three upper tile rows.For clarity about support exclusions, the transformed original lateral supports have the following form. At a column  $b_i+r$ , with  $r\ge2$ :RayEven  $r$ Odd  $r$ Near $(q_i-1,b_i+r)$  $(q_i+1,b_i+r)$ Far $(p_i+1,b_i+r)$  $(p_i-1,b_i+r)$ The four remaining axial supports are
$$(q_i-1,b_i),\quad
(p_i+1,b_i),\quad
(q_i,P+1),\quad
(p_i,e_i+1).
\tag{6}$$
The restriction  $r\ge2$  matters: a bar endpoint at column  $b_i+1$  must not be treated as though it carried a lateral support. The pair argument below handles this correctly.Charge calculationWrite  $\sigma_i$  for the number of original support locations in  $J_i$ 's endpoint tiles. Direct counting gives
$$M_i=H_i+\frac{D_i+G_i}{2}-1,$$
and:Index phase $T_i$  $\sigma_i$  $M_i+\sigma_i-2T_i$ Even  $i$  $\frac{H_i+D_i+G_i}{2}$  $\frac{D_i+G_i}{2}$  $-1$ Odd  $i$  $\frac{H_i+D_i+G_i}{2}+1$  $\frac{D_i+G_i}{2}+4$  $+1$ These counts use the immutable original supports, including supports consumed by foreign endpoints. Thus the four additions increase  $N+S$  by exactly  $4$ .Endpoint-disjoint additions preserve every old event and every old full mixed tile. Therefore, writing  $\delta F,\delta E$  for the increases relative to  $\mathcal O$ ,
$$\Delta\Phi
=u+v+L+24+4+2\delta F-\delta E.
\tag{7}$$
Every newly added event contains at least one staircase owner.2. The upper receipt calculation is exactPut
$$F_A=s+1-L,\qquad
\nu=P-F_A+1=u+L+12.$$
Here  $F_A$  is odd.The new upper receipts are:Physical tile-row minimumNew full mixed tilesNew eventsSigned receipt $a-9$  $\nu/2$  $3\nu/2$  $-\nu/2$  $a-11$  $D_1/2+1$  $D_1+2$  $0$  $a-13$  $D_3/2+1$  $3D_3/2+2$  $-D_3/2$ Here “new events” is essential: preexisting events between retained owners remain part of the accepted prefix calculation.First upper rowAt row  $a-8$ , the old  $A$  and  $P_0$  endpoints together fill
$$[F_A,P].$$
At row  $a-9$ ,  $J_0$  fills  $[b_0,P]$ , with  $b_0\le F_A-3$ .Every old endpoint in  $[F_A,P]$  has an upward event to  $J_0$ , giving  $\nu$  events. Downward events from  $J_0$  occur exactly at the even columns, giving another  $\nu/2$ .The full mixed tiles have column minima
$$F_A+1,F_A+3,\ldots,P,$$
so there are  $\nu/2$ .The left boundary tile with minimum
$$(a-9,F_A-1)$$
is not full. Nevertheless, it contains the event
$$A:(a-8,F_A)\longrightarrow J_0:(a-9,F_A).$$
This is one of the  $\nu$  old-to- $J_0$  events already counted. No full-tile credit is assigned to it.At the right boundary, both new horizontal  $J_0/R$  directions target original axial supports. The cooperative full boundary tiles are included in the displayed full-tile count.Second upper rowThe upper  $J_2$  interval and lower  $J_1$  interval overlap on
$$[b_1,P].$$
Exactly one vertical direction is an event at each column:upper to lower at even columns;lower to upper at odd columns.This gives  $D_1+1$  events. The additional event is
$$B:(a-10,C)\longrightarrow J_1:(a-10,P).$$
The other relevant horizontal directions target original supports.The full tiles have minima  $(a-11,c)$  for
$$c=b_1,b_1+2,\ldots,P,$$
including the three-owner boundary tile. Hence the signed receipt is zero.Third upper rowUpper  $B$  and lower  $J_3$  meet on  $[b_3,P]$ . There are: $D_3+1$  vertical  $B\to J_3$  events; $D_3/2$  reverse events at odd columns;one horizontal  $B\to J_3$  event at the right boundary.The full-tile count is  $D_3/2+1$ , giving receipt  $-D_3/2$ .All other staircase bar tiles in these rows are wholly owned by their respective originals. By (5), no far ray supplies an omitted upper interaction.Thus the total upper receipt is exactly
$$-\frac{\nu+D_3}{2}.$$
If  $\eta$  denotes the remaining signed receipt, equation (7) becomes
$$\boxed{\Delta\Phi
=\frac u2+v+\frac L2+22-\frac{D_3}{2}+\eta.}
\tag{8}$$
3. Staircase-pair interactions cost at most four unitsThe bar argument is sufficient to exhaust these interactions.A continuing bar occupies both rows and both columns of its physical tile. A foreign endpoint in that tile would overlap one of its endpoints. Horizontal adjacency to an endpoint outside the aligned bar column crosses a physical tile boundary and therefore creates no event.Outside the upper rows, the only way a bar can occupy just one row of a relevant tile is by ending in its even upper row. That row is its far row. Hence every remaining foreign interaction between staircase originals is a far-row interaction.Same-parity indices cannot produce such an interaction:distinct far rows of the same parity belong to different physical tile rows;if their far rows coincide, their disjoint even-ended intervals cannot have neighboring endpoints within one physical tile.A possible interacting pair therefore consists of an odd-indexed owner in the even upper row and an even-indexed owner in the odd lower row. There are at most four such owner pairs.The lower-bar exception is genuinely excludedConsider one possible pair. Let its upper and lower far intervals be  $I_U,I_D$ .The lower owner's bar occupies both rows at its columns  $b_D,b_D+1$ . Endpoint-disjointness therefore prevents the upper interval from occupying either column.Because the upper interval is uninterrupted, it either lies entirely to the left of that bar, producing no overlap, or starts to its right. In the latter case,
$$b_U\ge b_D+2.$$
A nonempty overlap consequently has the form
$$[b_U,\min(e_U,e_D)],$$
with both endpoints even. Its cardinality  $\ell$  is odd.For each overlap column:at an even column, the upper owner's downward direction targets an original far lateral support, or the bar axial support at  $b_U$ ;at an odd column, the lower owner's upward direction targets an original far lateral support.The lower owner's exceptional bar columns are absent from the overlap, so this second statement never incorrectly invokes a nonexistent lateral support.Thus there are at most  $\ell$  events. The overlap supplies at least
$$\frac{\ell-1}{2}$$
full tiles wholly covered by this pair. Its allocated receipt is therefore at least
$$2\frac{\ell-1}{2}-\ell=-1.$$
An empty overlap has no event to debit.Summing over the four possible pairs gives the claimed bound
$$\boxed{\text{staircase-pair receipt}\ge-4.}
\tag{9}$$
This bound needs no restriction on the individual  $G_i$  or on the overlap lengths.4. The  $P_1$  band has one shared width budgetThe first endpoint row of  $P_1$  is
$$a_1-8=a+z-14=t+1,$$
and that row fills
$$[s_1+1,s].
\tag{10}$$
Every other original in block  $1$  starts at row at least  $t+3$ . Subsequent blocks start later still. By (4), only  $J_1,J_3$  can reach row  $t$ .For an interval reaching  $t$ , the endpoint of  $V_0$  at column  $s+2$ , together with endpoint-disjointness and evenness, forces
$$e_i\le s.$$
Equation (3) gives  $b_i\ge b_3\ge s_1+2$ . Hence each such far interval lies inside the first  $P_1$  bar interval.For one interval  $[b_i,e_i]$ :its  $G_i/2$  full mixed tiles have minima
$$(t,b_i),(t,b_i+2),\ldots,(t,e_i-2);$$
every one of its  $G_i+1$  columns gives a  $P_1\to J_i$  event;the reverse direction occurs at exactly its  $G_i/2$  odd columns.Its exact receipt is therefore
$$G_i-\left(G_i+1+\frac{G_i}{2}\right)
=-\frac{G_i}{2}-1.
\tag{11}$$
Now suppose  $m\ge1$  such intervals occur and  $g$  is the sum of their  $G_i$ . When ordered from left to right, disjoint intervals with even endpoints have successive endpoint-distance gaps at least  $2$ . Consequently,
$$g+2(m-1)\le s-b_3=D_3-u-12,$$
and therefore
$$\frac g2+m\le \frac{D_3-u-12}{2}+1.
\tag{12}$$
For  $m=0$ , the same debit bound is valid. Indeed,
$$D_3\ge D_0+6\ge u+L+20$$
implies  $D_3-u-12\ge L+8>0$ .Thus
$$\boxed{\text{\(P_1\)-band receipt}
\ge-\frac{D_3-u-12}{2}-1.}
\tag{13}$$
This proves the shared budget even when both possible far intervals touch  $P_1$ . Assigning that entire width budget separately to each interval would be incorrect; the supplied proof does not do so.5. The remaining old-boundary loss is at most twoThe relevant far intervals start strictly to the left of all the obstacles below, by (3).While  $A$  is presentThe far column of  $A$  is
$$F_A=s+1-L,$$
and it has an endpoint there on every row from  $a-8$  through
$$a+f-8.$$
Its terminal row is odd.If  $A$  is present on a staircase far row, endpoint-disjointness forces
$$e_i\le F_A-1.$$
Only equality permits a same-tile horizontal contact.At equality: $J_i\to A$  targets  $J_i$ 's original far axial support;on an odd far row,  $A\to J_i$  targets  $A$ 's original even-indexed lateral support;on an even far row, one  $A\to J_i$  event may remain.Only  $J_1,J_3$  have even far rows, so these contacts debit at most  $2$ .There is no omitted contact immediately after  $A$  ends. Its terminal row is odd, so the next even row starts a new physical tile row. Once the far row has passed the terminal, the terminal cannot sit in the other row of that far tile.After  $A$  has endedBecause  $f\ge4$ , this case begins no earlier than row  $a-3$ . The remaining possibilities are:Far rowFirst relevant obstacleConsequence $a-3$  $Z_0$  at column  $s-1$ , with the  $X_0$  tip in the next row $e_i\le s-2$ ; only the neutral corner can contribute $a-2,\ldots,a+2$  $X_0$  at even column  $s-4$  $e_i\le s-6$ ; tile-column separation excludes  $X_0/Z_0$  events $a+3,\ldots,t$  $V_0$  at even column  $s+2$  $e_i\le s$ ; all remaining first-block endpoint columns are separatedThe exceptional first row deserves an explicit check.At row  $a-3$ , a vertical contact with the  $X_0$  tip
$$(a-2,s-4)$$
is excluded in both directions: $X_0\to J_i$  targets  $X_0$ 's original axial support; $J_i\to X_0$  targets  $J_i$ 's original even-column far lateral support.If  $e_i=s-2$ , the tile with minimum
$$(a-3,s-2)$$
contains the new endpoint  $(a-3,s-2)$  and precisely these three rotor endpoints:
$$(a-3,s-1),\qquad
(a-2,s-2),\qquad
(a-2,s-1).$$
There are exactly two events to the new endpoint:
$$\begin{aligned}
Z_0:(a-3,s-1)&\longrightarrow J_i:(a-3,s-2),\\
Z_0:(a-2,s-2)&\longrightarrow J_i:(a-3,s-2).
\end{aligned}$$
The reverse directions target  $J_i$ 's original axial and lateral supports. The full-tile credit  $2$  therefore cancels the two events exactly. Endpoint-disjointness allows only one owner to occupy the missing corner.Why this exhausts the retained originalsThe spatial exclusions used here are uniform: $B$ 's near stem is in the tile column beginning at  $s_1$ , whereas every staircase bar and far interval starts at least at  $s_1+2$ . $P_0$ 's exceptional column  $s+1$  occurs only on early rows where  $A$  is already the earlier obstacle.Apart from  $A,P_0,X_0,Z_0$ , every first-block original has minimum endpoint column at least  $s+2$ . $R$  and the root lie farther right. Increasing  $K,g,h$  cannot move their endpoints into the allowed far-ray tile columns.Later blocks have no endpoints in a reachable physical tile row, except for  $P_1$ , already counted.The bar-interior argument from Section 3 also excludes interactions hidden along a continuing staircase bar. Its upper boundary belongs to the upper calculation; its lower partial tile belongs to the far-row calculation.Thus the  $A$  directions and the neutral  $Z_0$  corner exhaust the remaining negative receipts, giving
$$\boxed{\text{remaining-old receipt}\ge-2.}
\tag{14}$$
6. The event partition and credit nonreuse are validThese are two distinct requirements.Every new event is assignedPartition the new events into:events in the three upper physical tile rows;remaining events between two staircase owners;remaining events between a staircase owner and  $P_1$ ;remaining events between a staircase owner and another retained owner.Every new event has at least one staircase owner, so this is exhaustive. The bar and obstacle arguments above exhaust categories 2–4.These are disjoint sets of owner-labelled directed edges. Events from different groups can occupy the same physical tile; that does not duplicate an event.No credited full tile is reusedThe credited tiles have stronger ownership certificates:Each pair-credited tile has all four cells occupied by precisely its two staircase owners.Each  $P_1$ -credited tile contains  $P_1$  endpoints.The neutral corner contains three  $Z_0$  endpoints.The upper credits lie in the three excluded upper rows.A pair-credited tile therefore cannot also contain a  $P_1$  or  $Z_0$  endpoint, or be credited to a different staircase pair. Two  $P_1$  intervals cannot claim the same full tile without sharing staircase endpoints. The  $P_1$  band and the neutral corner also lie in different physical tile rows.Every credited tile is newly full relative to  $\mathcal O$ , because it contains a new staircase endpoint.Additional cooperative full tiles may be left uncredited. Their contribution is nonnegative. In particular, the proof does not need all event-bearing tiles to be disjoint, nor does it need to assign every positive full-tile credit.7. Final estimateCombining (9), (13), and (14),
$$\eta\ge
-4-\frac{D_3-u-12}{2}-1-2.$$
Substitution into (8) gives
$$\begin{aligned}
\Delta\Phi
&\ge
\frac u2+v+\frac L2+22-\frac{D_3}{2}
-4-\frac{D_3-u-12}{2}-1-2\\
&=u+v+\frac L2+21-D_3\\
&\ge\frac L2-1\\
&\ge2.
\end{aligned}$$
The penultimate step uses  $D_3\le u+v+22$ , and the final step uses  $L\ge6$ .The conditional compensation theorem is therefore accepted. The written proof would benefit from explicitly recording the nonfull upper-left boundary event and distinguishing event partition from full-tile credit nonreuse, but neither point requires changing its inequality or hypotheses. This verdict concerns the stated selected-union theorem; it supplies no assertion about complete extendibility or the marginals of arbitrary additional originals.
