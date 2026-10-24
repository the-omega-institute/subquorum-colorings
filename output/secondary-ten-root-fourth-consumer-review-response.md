Verdict: ACCEPT, with the stated coordinate and event conventionsThe reflected exclusions and the fourth-owner classification are correct under the explicit full- $U$ /rotor model, the supplied coordinates, and the prior accepted root-triple ledger.The two points that must remain explicit are:For the d6 reflected application, the A chart is the depth-dependent chart
$$A=U(L,6,f),\qquad (r,c)\mapsto(a-10+r,s+1-c).$$
Using the d4 offset  $a-8$  for a d6 A would make the displayed east wall incorrect.In the ledger,  $N=u+L+12$  is a tile/event-count parameter. It must not be confused with the global  $\Phi$ -quantity  $N$ , which counts positive-charge originals. The latter changes by  $\Delta N=1$  because of  $R$ ;  $J$  has charge  $-1$  and does not increase that count.Subject to those readings, the result is accepted.1. The reflected cavity is exactly the  $180^\circ$  image of the generic cavityThe relevant missing support in both reflected applications is
$$p=(a-9,C-1),
\qquad C=s+u+13.$$
This is R’s bar-exterior support  $(0,0)$ . Its east neighbor is
$$p+(0,1)=(a-9,C),$$
an R endpoint, and its south neighbor is
$$p+(1,0)=(a-8,C-1),$$
a P0 endpoint. Thus  $p$  has two retained occupied neighbors. By the support rule, a complete family cannot leave  $p$  absent, so a fresh original must contain  $p$  as an endpoint.Any such fresh owner is endpoint-disjoint from all retained originals and must avoid the translated guard set.The original cavity guard set is
$$\begin{aligned}
G_N&=\{(-1,c):0\le c\le q\},\\
G_E&=\{(0,q)\},\\
G_S&=\{(4,c):0\le c\le q-1\},\\
G_W&=\{(r,-1):0\le r\le2\}.
\end{aligned}$$
Under the  $180^\circ$  map  $(r,c)\mapsto(-r,-c)$ , this becomes
$$\begin{aligned}
G'_N&=\{(1,-c):0\le c\le q\},\\
G'_E&=\{(0,-q)\},\\
G'_S&=\{(-4,-c):0\le c\le q-1\},\\
G'_W&=\{(-r,1):0\le r\le2\}.
\end{aligned}$$
The reflected applications realize exactly this pattern around  $p$ .2. Reflected d6 applicationFor  $A=U(L,6,f)$ , use the correct chart
$$(r,c)\longmapsto(a-10+r,s+1-c).$$
Take
$$q=u+12.$$
The translated reflected guard set is:
$$\begin{array}{c|c|c}
\text{relative role} & \text{absolute sites} & \text{retained source}\\
\hline
\text{row at }p+(1,\cdot)
&
(a-8,s),\ldots,(a-8,C-1)
&
A\text{ near stem at }s,\quad P_0\text{ row-zero bar}
\\
\text{single wall}
&
(a-9,s)
&
A\text{ lower bar}
\\
\text{row at }p+(-4,\cdot)
&
(a-13,s+1),\ldots,(a-13,C-1)
&
B\text{ lower bar}
\\
\text{column at }p+(\cdot,1)
&
(a-9,C),(a-10,C),(a-11,C)
&
R\text{ at }a-9,\ B\text{ far stem at }a-10,a-11.
\end{array}$$
The first row has  $q+1=u+13$  sites, and the third has  $q=u+12$  sites, as required by the reflected generic lemma.The relevant endpoint facts are direct from the charts:A’s d6 near stem is column  $s$ , starting at row  $a-8$ .P0’s row-zero bar covers columns  $s+1$  through  $C-1$ .A’s lower bar contains  $(a-9,s)$ .B’s row-one bar contains columns  $s+1$  through  $C-1$  at row  $a-13$ .R contributes  $(a-9,C)$ .B’s far stem contributes  $(a-10,C)$  and  $(a-11,C)$ .The reflected guard system is therefore an exact lattice isometric image of the generic cavity with  $q=u+12\ge24$ . Since the generic theorem excludes every full  $U$  and every rotor, no fresh owner can consume  $p$ . Consequently no complete extension can contain any d6 A branch, regardless of  $L,f$ , or R’s parameters.No existence claim is being made: this says that every complete extension containing the retained prefix would lead to a contradiction.3. Reflected tight d4 applicationNow let
$$A=U(L,4,f),
\qquad
A:(r,c)\mapsto(a-8+r,s+1-c),$$
with the tight breadth
$$L=v+12.$$
Since
$$s_1=s-v-12,$$
the left endpoint of A’s row-zero bar is
$$s+1-L
=s+1-(v+12)
=s-v-11
=s_1+1.$$
Take
$$q=C-1-s_1
=(s+u+12)-(s-v-12)
=u+v+24.$$
The reflected guard sites are:
$$\begin{array}{c|c|c}
\text{relative role} & \text{absolute sites} & \text{retained source}\\
\hline
\text{row at }p+(1,\cdot)
&
(a-8,s_1),\ldots,(a-8,C-1)
&
B\text{ near stem},\ A\text{ row-zero bar},\ P_0\text{ row-zero bar}
\\
\text{single wall}
&
(a-9,s_1)
&
B\text{ near stem}
\\
\text{row at }p+(-4,\cdot)
&
(a-13,s_1+1),\ldots,(a-13,C-1)
&
B\text{ lower bar}
\\
\text{column at }p+(\cdot,1)
&
(a-9,C),(a-10,C),(a-11,C)
&
R\text{ and B}.
\end{array}$$
The first row is continuous because:B supplies  $s_1$ ,A supplies  $s_1+1,\ldots,s$ ,P0 supplies  $s+1,\ldots,C-1$ .The third row is a B lower-bar segment. The single wall is B’s near stem. Hence this is again exactly the  $180^\circ$  image of the generic cavity, now with  $q=u+v+24\ge48$ .Therefore every tight d4 branch  $L=v+12$ , at every allowed far length  $f$ , is excluded from complete extension.The prior d4 range is
$$6\le L\le v+12,\qquad 4\le f\le z-8.$$
Because  $L,v$  are even, removing  $L=v+12$  leaves
$$\boxed{
d=4,\qquad 6\le L\le v+10,\qquad 4\le f\le z-8.
}$$
For these remaining d4 branches,
$$\varepsilon=[L=v+12]=0,$$
so the prior accepted marginal is  $L-1$ , and
$$\Delta\Phi
=u+v+L+24
\ge u+v+30
\ge54.$$
Thus the reflected exclusions narrow the necessary actual-owner classification without changing the previously established lower bound.4. Fourth-owner classificationAgain set
$$p=(a-9,C-1).$$
The east and south neighbors of  $p$  are retained endpoints of R and P0. Hence any new owner containing  $p$  can have own endpoint neighbors only north and west.The full- $U$  classification is the reflected version of the earlier cavity classification:a north terminal;a west terminal;a degree-two outer bar corner whose two neighbors are north and west.All other U positions have either an east/south neighbor or too many endpoint neighbors.North terminal and north/west outer cornerA north terminal has a north ray of length at least  $4$ , and a north/west outer corner has either a stem ray of depth at least  $4$  or a bar ray of length at least  $5$ . Each therefore contains
$$p+(-4,0)=(a-13,C-1),$$
which is a B lower-bar endpoint.These roles are impossible.RotorThe four relevant rotor tips are the  $180^\circ$  images of the four east/south guard-compatible tip shapes from the original cavity table. Their forced collisions relative to  $p$  are:
$$p+(-2,1),\qquad
p+(-1,1),\qquad
p+(1,-1),\qquad
p+(1,-2).$$
The first two are B endpoints on its far stem; the last two are P0 endpoints. Rotor non-tips already have an immediate retained neighbor in a forbidden direction.Thus no rotor can consume  $p$ .Only a west-terminal full  $U$  remains.5. West-terminal U and chart classificationWrite
$$b=C-1-D.$$
The incident west-oriented row of the remaining U runs from  $b$  through  $C-1$ .If
$$D\ge u+v+24,$$
then
$$b=C-1-D\le s_1,$$
so the incident row reaches B’s near stem at column  $s_1$ . This is impossible.If instead
$$D<u+v+24,$$
then  $D$  and  $u+v+24$  are even, so
$$D\le u+v+22,$$
and consequently
$$b\ge s_1+2.$$
If the U bar points upward, its breadth at least  $6$  reaches
$$(a-13,b),$$
which is on B’s lower bar because  $b\in[s_1+2,C-1]$ . Hence the bar must point downward.This gives exactly the chart
$$J=U(H,D,G),\qquad
(r,c)\mapsto(a-10+c,\ s+u+12-D+r),$$
with
$$u+L+14\le D\le u+v+22.$$
The dimensions  $H,D,G$  are even and satisfy  $H,D,G\ge4$ , with  $H\ge6$ .6. Derivation of the parameter boundsLower bound on  $D$ At row  $a-8$ , A and P0 occupy the continuous interval
$$[F,C-1],
\qquad
F=s+1-L.$$
J’s two-column bar has columns  $b,b+1$ . Since  $b<C-1$ , it cannot lie to the right of the occupied interval. Therefore it must satisfy
$$b+1<F.$$
Substituting  $b=C-1-D=s+u+12-D$ ,
$$s+u+13-D<s+1-L,$$
so
$$D>u+L+12.$$
Since  $D,u,L$  are even,
$$\boxed{D\ge u+L+14.}$$
Bound on  $H$ P1’s row-zero bar begins at row  $a+z-14$ . J’s far bar row is  $a+H-10$ . If  $H\ge z-4$ , these rows meet or overlap. Thus
$$H<z-4.$$
With even  $H,z$ ,
$$\boxed{H\le z-6.}$$
Far-row bounds on  $G$ Let
$$r_F=a+H-10,
\qquad
E=b+G$$
be J’s far row and its rightmost endpoint.Regime 1:  $H\le f+2$ The far row lies within A’s far stem, whose column is
$$F=s+1-L.$$
Since  $F$  is odd and  $E$  is even, disjointness requires
$$E\le F-1=s-L.$$
Using  $E=s+u+12-D+G$ ,
$$\boxed{G\le D-u-L-12.}$$
Regime 2:  $H\ge f+4$  and  $H\le12$ A is already above the far row. The first retained obstacle to the right is X0 at column  $s-4$ . Parity gives
$$E\le s-6,$$
hence
$$\boxed{G\le D-u-18.}$$
Regime 3:  $H\ge f+4$  and  $H\ge14$ X0 and the west rotor are above the far row. V0 supplies the first retained endpoint to the right, at column  $s+2$ . Therefore
$$E\le s,$$
and
$$\boxed{G\le D-u-12.}$$
The three regimes exhaust all even  $H$ , since  $H\le f+2$  and  $H\ge f+4$  are the two possible cases for even  $H,f$ .These bounds give exactly
$$\boxed{
\begin{aligned}
&u+L+14\le D\le u+v+22,\\
&6\le H\le z-6,\\
&G\le D-u-L-12 &&(H\le f+2),\\
&G\le D-u-18 &&(H\ge f+4,\ H\le12),\\
&G\le D-u-12 &&(H\ge f+4,\ H\ge14).
\end{aligned}}$$
The chart and these inequalities are sufficient for endpoint-disjointness from the retained H3 originals, B, R, and A: the incident row lies in the B/A/R corridor, the two-column bar avoids the continuous A/P0 interval, the P1 bound keeps the bar above the next block, and the far-row caps stop J before the first retained endpoint in each possible height regime. The last endpoint row of J is at most  $a+z-16$ , while later blocks begin at row  $a+z-14$ .This is geometric sufficiency only. It does not assert a complete extension.7. Frontier for geometric admissibilityThe necessary and sufficient condition
$$\boxed{
L\le v+6
\quad\text{or}\quad
(L=v+8\ \text{and}\ f\le z-10)
}$$
is correct.NecessityIf  $H\le f+2$ , then  $G\ge4$  and the first cap give
$$4\le D-u-L-12,$$
so
$$D\ge u+L+16.$$
Combining with  $D\le u+v+22$ ,
$$L\le v+6.$$
If  $H\ge f+4$ , then  $H\le z-6$  requires
$$f+4\le z-6,$$
hence
$$f\le z-10.$$
The general D bounds imply  $L\le v+8$ . Since  $L,v$  are even, the case not covered by  $L\le v+6$  is exactly  $L=v+8$ .SufficiencyIf  $L\le v+6$ , choose
$$H=6,\qquad D=u+v+22,\qquad G=4.$$
Then  $H\le f+2$  because  $f\ge4$ , and
$$D-u-L-12=v+10-L\ge4.$$
All other caps hold.If  $L=v+8$  and  $f\le z-10$ , choose
$$H=f+4,\qquad D=u+v+22,\qquad G=4.$$
Then  $H\le z-6$ . If  $H\le12$ , the second cap is
$$D-u-18=v+4\ge4.$$
If  $H\ge14$ , the third cap is
$$D-u-12=v+10\ge4.$$
Thus the stated frontier is exact for geometric endpoint-disjointness.8. Exact four-owner ledgerUse a distinct symbol
$$\nu=u+L+12$$
for the number appearing in the new J corridor. This avoids confusion with the global  $\Phi$ -quantity  $N$ , which counts positive-charge originals.For the retained B,R,A triple in the residual d4 branch, the accepted prior ledger gives
$$(\Delta S,\Delta N,\Delta F,\Delta E)_{\mathrm{B,R,A}}
=
(u+v+L+24,\ 1,\ 8,\ 17).$$
The fourth owner J has charge  $-1$ .Let
$$t=\frac{D+G}{2}.$$
For J,
$$M=H-1+t$$
because the two bar rows contribute  $H/2+(H/2-1)=H-1$ , and the two stems contribute  $D/2+G/2=t$ .Its full endpoint tiles number
$$T=\frac H2+t.$$
The original supports lying in those endpoint tiles are the two axial supports plus  $t-2$  lateral supports, hence exactly  $t$ . The two bar-exterior supports lie outside the endpoint tiles. Therefore
$$\operatorname{charge}(J)
=(H-1+t)+t-2\left(\frac H2+t\right)
=-1.$$
Thus J contributes
$$\Delta S_J=1,\qquad \Delta N_J=0.$$
New full mixed tilesThe new mixed full tile minima are
$$(a-9,c),
\qquad
c=s+2-L,\ s+4-L,\ldots,s+u+12.$$
The count is
$$\frac{(s+u+12)-(s+2-L)}2+1
=\frac{u+L+12}{2}
=\frac{\nu}{2}.$$
The tile at  $s-L$  is only partial at the left boundary. The tile at  $C-1$  is full and has three owners:J/P0 on the left physical column,R on the right physical column.The tile at  $s$  is the other three-owner tile:J on the upper pair,A and P0 on the lower pair.Those two tiles are each counted once in  $F$ . The J bar’s own two-column tiles are wholly J-owned and therefore do not belong to  $F$ . The far-row boundary tiles are partial, and later blocks start below J’s last tile row.Therefore
$$\Delta F_J=\frac{\nu}{2}.$$
Together with the prior triple,
$$\boxed{\Delta F=8+\frac{\nu}{2}.}$$
New directed eventsThe new event sets are:J to an old endpoint:
$$J:(a-9,c)\to \mathrm{old}:(a-8,c),$$
for the  $\nu/2$  even tile minima listed above.A to J:
$$A:(a-8,c)\to J:(a-9,c),
\qquad c=s+1-L,\ldots,s,$$
giving  $L$  events.P0 to J:
$$P_0:(a-8,c)\to J:(a-9,c),
\qquad c=s+1,\ldots,s+u+12,$$
giving  $u+12$  events.The apparent second J-to-old vertical edge in each incident-row tile is excluded by the explicit support rule: its target is one of J’s original lateral supports. The reverse A/P0-to-J edges are not excluded because the J endpoint is not an original support of A or P0.Consequently,
$$\Delta E_J
=
\frac{\nu}{2}+L+(u+12)
=
\frac{3\nu}{2}.$$
The horizontal J/R boundary directions are excluded because the relevant targets are J axial/bar-exterior supports or R’s bar-exterior support. The left boundary is partial, and the far-row boundary is partial or support-excluded in the three height regimes. No later block can create a new receipt because its first endpoints begin below J’s last tile row.Thus
$$\boxed{\Delta E=17+\frac{3\nu}{2}.}$$
Adding the fourth owner gives
$$\boxed{
\Delta S=u+v+L+25,\qquad
\Delta N=1,\qquad
\Delta F=8+\frac{\nu}{2},\qquad
\Delta E=17+\frac{3\nu}{2}.
}$$
Therefore
$$\begin{aligned}
\Delta\Phi
&=\Delta S+\Delta N+2\Delta F-\Delta E\\
&=(u+v+L+25)+1
 +2\left(8+\frac{\nu}{2}\right)
 -\left(17+\frac{3\nu}{2}\right)\\
&=u+v+L+25-\frac{\nu}{2}\\
&=\frac u2+v+\frac L2+19,
\end{aligned}$$
because  $\nu=u+L+12$ .9. Explicit witnessFor
$$a=31,\quad s=0,\quad u=v=12,\quad z_0=z_1=24,\quad h=6,$$
take
$$B=U(50,28,4),\qquad
R=U(8,8,4),\qquad
A=U(6,4,4),\qquad
J=U(8,34,4)$$
in the stated charts.Here
$$L=6,\qquad \nu=u+L+12=30.$$
The frontier condition holds through  $L\le v+6$ . The four-owner ledger is
$$\Delta S=55,\qquad
\Delta N=1,\qquad
\Delta F=23,\qquad
\Delta E=62,$$
and hence
$$\Delta\Phi
=55+1+2(23)-62
=40.$$
The prior triple gain is
$$u+v+L+24=54,$$
while J’s marginal is
$$1-\frac{\nu}{2}=1-15=-14.$$
Thus
$$54-14=40,$$
exactly as stated.This witness demonstrates a negative fourth-owner marginal in the specified partial inventory. It does not establish complete extendibility, a global monotonicity failure, arbitrary-grid catalogue exhaustion, or any global bound.
