ACCEPT — the sharper bound and the advertised equality family are correctUnder the same explicit full- $U$ /rotor model, assumed forced charts, immutable supports, and endpoint-disjointness hypotheses,
$$\boxed{\Delta\Phi\ge \frac L2+3\ge6.}$$
The proposed family attains
$$\boxed{\Delta\Phi=\frac L2+3}$$
for every advertised even parameter choice
$$u,v\ge12,\qquad z\ge24,\qquad 6\le L\le v,$$
uniformly in the chain length and the allowed root and  $R$  dimensions.The two new improvements are valid for all parameters. The equality claim also survives the stronger check it requires: there are no additional cooperative full tiles outside the stated receipt groups. Below is a symbolic audit of both conclusions.1. The far-pair exclusion is valid for arbitrary dimensionsRetain the notation
$$q_i=a-9-i,\qquad
y_i=a-10-i+H_i,\qquad
b_i=P-D_i,\qquad
e_i=b_i+G_i.$$
The endpoint set of  $J_i$  consists of:its bar in columns  $b_i,b_i+1$ , on rows  $q_i,\ldots,y_i$ ;its near interval  $[b_i,P]$  on row  $q_i$ ;its far interval  $[b_i,e_i]$  on row  $y_i$ .The depth conditions give
$$b_0>b_1>b_2>b_3,
\qquad b_i-b_{i+1}\ge2.
\tag{5}$$
The previously established bar argument applies unchanged. Outside the three upper tile rows, a continuing bar fills its entire aligned two-column tile. A foreign endpoint cannot occupy that tile without an endpoint collision. Horizontal adjacency across the boundary of that bar column lies across a physical tile boundary.Thus a remaining staircase interaction must occur between far rows in one physical tile row. The upper far row is even and the lower far row is odd, so an interacting ordered pair must satisfy
$$i\ \text{odd},\qquad j\ \text{even},\qquad y_j=y_i+1.
\tag{6}$$
Suppose its far intervals overlap and  $b_i\le b_j$ . Since  $b_j$  is the lower interval’s first column, overlap implies
$$b_j\le e_i.$$
Hence
$$(y_i,b_j)$$
is an upper-owner endpoint. But
$$(y_i,b_j)=(y_j-1,b_j)$$
is also a lower-owner bar endpoint. This contradicts endpoint-disjointness.Therefore
$$b_i>b_j,$$
and evenness strengthens this to
$$b_i\ge b_j+2.
\tag{7}$$
By (5), this requires  $i<j$ . Among the indices  $0,1,2,3$ , the only odd  $i$  and even  $j$  satisfying  $i<j$  are
$$\boxed{(i,j)=(1,2).}$$
This proves the exclusion independently of every  $H_i$  and  $G_i$ .There is no overlooked lower-bar corner contactIf the upper interval lies to the left of the lower bar, it ends at an even column at most  $b_j-2$ . It therefore cannot have a horizontal neighboring endpoint at the lower bar’s even starting column within the same physical tile.If it lies to the right, (7) excludes both lower-bar columns from the overlap. This is exactly the condition needed in the inherited lateral-support calculation.For a nonempty overlap of cardinality  $\ell$ , its endpoints are even, so  $\ell$  is odd. There are at least
$$\frac{\ell-1}{2}$$
full tiles covered by the pair, and at most one permitted directed event per overlap column. Consequently,
$$2F_{\mathrm{pair}}-E_{\mathrm{pair}}
\ge (\ell-1)-\ell=-1.$$
An empty overlap supplies no debit. Therefore
$$\boxed{\text{total staircase-pair receipt}\ge-1.}
\tag{8}$$
The reduction from four possible parity pairs to the single pair  $J_1/J_2$  is justified.2. The  $A$  and  $P_1$  debits are exclusive for each ownerLet
$$t=a+z-15.$$
The height bounds and parity imply
$$y_0,y_2\le t-1,\qquad y_1,y_3\le t.
\tag{9}$$
A  $P_1$  contact requires the far row to be exactly  $t$ . Thus only  $J_1,J_3$  can supply one.An  $A$ -boundary debit likewise requires an odd-indexed staircase owner, but it requires  $A$  to be present on that owner’s far row. The last row occupied by  $A$ 's far stem is
$$a-8+f\le a+z-16=t-1.
\tag{10}$$
Each staircase original has only one far row. Consequently, an owner touching  $P_1$  cannot also incur an  $A$ -boundary debit.The terminal-row phase is important here. The terminal row of  $A$  is odd. Once an even far row has passed it, that terminal endpoint is in the preceding physical tile row; it cannot generate an additional vertical intratile event.The inherited boundary calculation also shows that each eligible owner incurs at most one  $A$ -boundary debit. Therefore, if  $m$  counts  $P_1$ -contact owners and  $q$  counts  $A$ -boundary debits,
$$\boxed{m+q\le2.}
\tag{11}$$
This remains valid at the maximal allowed value  $f=z-8$ .3. The shared width estimate and refined ledger are soundPut
$$W=s-b_3=D_3-u-12.$$
Every far interval meeting  $P_1$  lies in  $[b_3,s]$ .If  $g$  is the sum of their endpoint distances  $G_i$ , then:for  $m=0$ ,  $g=0$ ;for  $m=1$ , containment gives  $g\le W$ ;for  $m=2$ , disjoint even-ended intervals require an intervening endpoint-distance gap of at least  $2$ , giving  $g\le W-2$ .Moreover,
$$D_3\ge D_0+6\ge u+L+20$$
implies  $W\ge L+8>0$ . Thus, uniformly,
$$\boxed{0\le g\le W.}
\tag{12}$$
The exact  $P_1$  receipt remains
$$-\frac g2-m.$$
The other old-boundary receipt is bounded below by  $-q$ : the exceptional rotor corner has its own cancelling full-tile credit.Combining these facts with (8),
$$\begin{aligned}
\eta
&\ge -1-\frac g2-m-q\\
&\ge-\frac g2-3\\
&\ge-\frac{D_3-u-12}{2}-3.
\end{aligned}
\tag{13}$$
The inherited exact identity is
$$\Delta\Phi
=\frac u2+v+\frac L2+22-\frac{D_3}{2}+\eta.$$
Substitution yields
$$\begin{aligned}
\Delta\Phi
&\ge
\frac u2+v+\frac L2+22-\frac{D_3}{2}
-\frac{D_3-u-12}{2}-3\\
&=u+v+\frac L2+25-D_3\\
&\ge\frac L2+3\\
&\ge6.
\end{aligned}$$
Nonreuse is preservedThe strengthening changes debit estimates without introducing a new credit assignment.The credited full tiles still have incompatible ownership descriptions:a staircase-pair tile has all four cells occupied by  $J_1/J_2$ ;a  $P_1$  tile contains  $P_1$  endpoints;the neutral rotor tile contains three old rotor endpoints;the upper credits lie in the three upper tile rows.Endpoint-disjointness prevents a full tile from satisfying two of these descriptions. The event groups are disjoint as sets of owner-labelled directed edges, using the owner classes and row partition.As before, different event groups may occupy the same physical tile. That causes no double counting: what must be disjoint are the directed events themselves and the full tiles receiving credit.4. The proposed equality parameters satisfy all hypothesesFor the family, write
$$x=s-L,\qquad F_A=x+1,\qquad t=a+z-15.$$
Its relevant coordinates are:OwnerNear rowFar rowBar startFar interval $J_0$  $a-9$  $a-4$  $x-4$  $[x-4,x]$  $J_1$  $a-10$  $a-3$  $x-6$  $[x-6,x]$  $J_2$  $a-11$  $a-2$  $x-8$  $[x-8,x-4]$  $J_3$  $a-12$  $t$  $s-v-10$  $[s-v-10,s]$ The depth conditions hold because
$$D_0=u+L+16\ge u+L+14,$$

$$D_1-D_0=D_2-D_1=2,$$
and
$$D_3-D_2=v-L+2\ge2.$$
Also,
$$D_3=u+v+22.$$
The height conditions follow from  $z\ge24$ :
$$6<z-4,\quad
8<z-3,\quad
10<z-2,\quad
z-2<z-1.$$
All far depths are even and at least  $4$ , and  $f=6$  satisfies
$$4\le6\le z-8.$$
In particular,
$$b_3\le b_2-2,$$
including the boundary case  $L=v$ .5. The complete staircase endpoint sets are disjointChecking only the far rays would be insufficient. The near intervals and full bars also need to be controlled.Near intervalsTheir rows are ordered
$$q_3<q_2<q_1<q_0.$$
At row  $q_i$ , every already-started staircase owner has index  $j>i$ , and its bar lies strictly to the left:
$$b_j+1<b_i.$$
None of those owners has yet reached its far row. Thus the near interval  $[b_i,P]$  avoids every foreign staircase endpoint.These near rows precede the first  $H_3$  and  $A$  endpoint row  $a-8$ . At the relevant rows,  $B$ 's stems are at
$$s_1=s-v-12,\qquad C=P+1,$$
strictly outside every near interval. At row  $a-9$ ,  $R$  begins at column  $C=P+1$ , again outside the interval.BarsThe bar columns are disjoint because their starts have gaps at least  $2$ .All bars lie between columns
$$s_1+2
\quad\text{and}\quad
s-L-3=x-3.$$
They are therefore right of  $B$ 's near stem and left of  $A$ , whose minimum column is  $F_A=x+1$ .They also lie left of all first-block  $H_3$  endpoints. The exceptional leftmost columns are  $s-4$  for  $X_0$ ,  $s-2$  for the west rotor, and  $s+1$  for  $P_0$ ; each is strictly to the right of these bar columns.Every bar ends by row  $t$ , while the first later-block endpoint occurs at  $P_1$ 's row  $t+1$ .Far intervalsAt the successive far rows:when  $J_0$  ends, all continuing foreign bars lie to its left;when  $J_1$  ends,  $J_0$  has ended and the other continuing bars lie to its left;when  $J_2$  ends,  $J_0,J_1$  have ended and the  $J_3$  bar lies to its left;when  $J_3$  ends, the first three staircase originals have all ended.Their far rows are distinct. Hence the four full staircase originals are mutually endpoint-disjoint.For  $f=6$ ,  $A$ 's far stem remains at  $F_A=x+1$  through row  $a-2$ . The first three far intervals end at  $x,x,x-4$ , so they avoid it. Since  $L\ge6$ , they also remain strictly left of  $X_0$ , the west rotor,  $P_0$ , and the other first-block endpoints.On row  $t$ , the exceptional originals  $A,P_0,X_0,Z_0$  have ended. Every other first-block original has minimum endpoint column at least  $s+2$ , whereas  $J_3$  ends at  $s$ . Later blocks have not started;  $P_1$  begins in the next row.These arguments are independent of  $n,h,K,g_R$ .One useful wording clarification: when  $z=24$ ,  $Q_0$  can still have endpoints in the last relevant physical tile row. It is excluded by its column bound, not by being entirely above that row. Your argument remains valid because its minimum endpoint column is  $s+3$ .6. The equality receipt calculation is exhaustiveThis is the decisive additional check. To prove equality, one must exclude surplus positive full-tile credits, not merely enumerate the negative events.Outside the three upper tile rows, the only physical tile rows containing staircase far endpoints have minima
$$a-5,\qquad a-3,\qquad t.
\tag{14}$$
In every other row, any staircase endpoints belong to continuing aligned bars, whose tiles are wholly owned by those originals.It therefore suffices to inspect these three tile rows.6.1. Tile row  $a-5$ :  $J_0$  contributes zeroThe rows are  $a-5,a-4$ . The  $J_0$  bar tile at column  $x-4$  is wholly  $J_0$ -owned. The next tile, beginning at  $x-2$ , has only lower-row  $J_0$  endpoints.The terminal tile, beginning at column  $x$ , contains exactly
$$J_0:(a-4,x),\qquad
A:(a-5,x+1),\qquad
A:(a-4,x+1).$$
Its upper-left cell  $(a-5,x)$  is empty, so it is not full.No other owner fills that cell: the other staircase bars are to the left, their far rows occur elsewhere, and the other retained originals are farther right.The horizontal  $J_0\to A$  direction targets  $J_0$ 's axial support. Its reverse targets  $A$ 's even-indexed far lateral support, because  $A$ 's canonical row here is  $4$ .Thus this tile row has no residual event or new mixed full tile.6.2. Tile row  $a-3$ : one pair tile and one  $A$  debitThe rows are  $a-3,a-2$ . The upper  $J_1$  interval is
$$[x-6,x],$$
and the lower  $J_2$  interval is
$$[x-8,x-4].$$
The relevant occupancy is:Column minimumUpper two cellsLower two cellsStatus $x-8$  $J_2,J_2$  $J_2,J_2$ Wholly  $J_2$ -owned $x-6$  $J_1,J_1$  $J_2,J_2$ One new mixed full tile $x-4$  $J_1,J_1$  $J_2,\varnothing$ Not full $x-2$  $J_1,J_1$  $\varnothing,\varnothing$ Not full $x$  $J_1,A$  $\varnothing,A$ Not fullThe  $J_1/J_2$  overlap is exactly the three-column interval
$$[x-6,x-4].$$
Its events are: $J_2\to J_1$  at the even columns  $x-6,x-4$ ; $J_1\to J_2$  at the odd column  $x-5$ .The opposite directions target original supports. Hence the pair supplies one full tile and three events:
$$2-3=-1.$$
The only  $A$ -boundary event is
$$A:(a-3,x+1)\longrightarrow J_1:(a-3,x).$$
Here  $A$ 's canonical far-stem row is  $5$ , so its lateral support is on the other side. The reverse direction targets  $J_1$ 's axial support.Crucially, the lower-left cell of this  $A$ -adjacent tile remains empty:  $J_2$  stops at  $x-4$ , not at  $x$ . Thus there is no cooperative full-tile credit cancelling that debit.Because
$$x+2=s-L+2\le s-4,$$
the  $X_0$  tip and the rotor endpoints are outside all the listed tiles. In particular, there is no neutral rotor corner.This tile row therefore contributes exactly
$$-1-1=-2.$$
6.3. Tile row  $t$ : exactly the  $J_3/P_1$  receiptHere
$$b_3=s-v-10,\qquad G_3=v+10,$$
and  $J_3$  fills the upper interval
$$[b_3,s].$$
The first  $P_1$  bar row fills the lower interval
$$[b_3-1,s].$$
The newly full mixed tiles are exactly
$$\boxed{(t,b_3+2k),\qquad
0\le k<\frac{v+10}{2}.}
\tag{15}$$
The terminal tile beginning at  $s$  contains only the two vertical endpoints at column  $s$ ; its column  $s+1$  is empty.Immediately to the left,  $B$ 's near stem lies at  $b_3-2$ . The old partial  $B/P_1$  tile receives no new endpoint because  $J_3$  starts at  $b_3$ . Immediately to the right,  $V_0$  lies at  $s+2$ , in a different physical tile column.There are
$$G_3+1$$
events  $P_1\to J_3$ , and
$$G_3/2$$
reverse events at odd columns. The exact receipt is
$$-\frac{G_3}{2}-1
=-\frac{v+10}{2}-1.$$
Exact residual sets and totalConsequently, the entire new full mixed-tile set outside the upper rows is
$$\left\{(a-3,x-6)\right\}
\;\cup\;
\left\{(t,b_3+2k):
0\le k<\frac{v+10}{2}\right\}.$$
The corresponding new events consist exactly of:three  $J_1/J_2$  directions;one  $A\to J_1$  direction; $G_3+1+G_3/2$  directions between  $J_3$  and  $P_1$ .Thus
$$\begin{aligned}
\eta
&=2\left(1+\frac{G_3}{2}\right)
-\left(3+1+G_3+1+\frac{G_3}{2}\right)\\
&=-\frac{G_3}{2}-3\\
&=\boxed{-\frac v2-8}.
\end{aligned}
\tag{16}$$
This also proves directly that no extra cooperative full tile destroys equality.7. Equality and sharpnessFor the family,
$$D_3=u+v+22,$$
so the inherited exact ledger becomes
$$\Delta\Phi
=\frac v2+\frac L2+11+\eta.$$
Using (16),
$$\boxed{\Delta\Phi
=\frac v2+\frac L2+11-\frac v2-8
=\frac L2+3.}$$
The family saturates all the relevant inequalities:
$$D_3=u+v+22,\qquad
g=W=v+10,\qquad
m=q=1,$$
with the unique possible pair receipt equal to  $-1$  and no surplus full-tile credit.For the displayed specialization  $u=v=12,z=24,L=6$ , the formula gives  $\Delta\Phi=6$  directly.The universal strengthening and the unbounded equality family are both accepted. Sharpness is established on the advertised family range  $6\le L\le v$ , as a selected inventory of endpoint-disjoint full originals. The argument makes no complete-extension or global-allocation claim.
