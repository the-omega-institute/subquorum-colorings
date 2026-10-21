# Independent sealed-cavity and complete-prefix review

VerdictACCEPT the sealed-cavity lemma and the complete-prefix bound
$$\boxed{\Delta\Phi\ge \frac L2+7\ge10.}$$
The full-wall argument, forced-support step, connected-owner trapping, orientation obstruction, and three-case receipt analysis are valid under the stated model.One correction is needed in the boundary-control paragraph: the width- $3$  modification requires
$$\boxed{6\le L\le v-2.}$$
It cannot inherit the entire former range  $6\le L\le v$ . At  $L=v$ , its modified  $J_3$  bar coincides with the  $J_2$  bar, violating endpoint-disjointness. This does not affect either principal theorem or the width- $3$  obstruction for admissible prefixes.Here is the coordinate audit.1. The cavity has four complete retained endpoint wallsAssume  $J_3$ 's height is  $H_3=z-2$ . Its near and far rows are then
$$q_3=a-12,\qquad
y_3=a-13+(z-2)=a+z-15=t.$$
Set
$$b_3=P-D_3,\qquad
C=[a-12,t]\times[s_1+1,b_3-1].$$
The number of columns in  $C$  is exactly
$$W=(b_3-1)-(s_1+1)+1
=b_3-s_1-1
=u+v+23-D_3.
\tag{4}$$
The number of rows is  $z-2$ . The upper depth bound gives  $W\ge1$ , so the rectangle is nonempty.The lower depth bounds give
$$D_3\ge D_0+6\ge u+L+20,$$
hence
$$b_3\le s-L-8<s.
\tag{5}$$
Every nearest-neighbor site immediately outside  $C$  belongs to one of the stated walls:WallCoordinate verificationLeft:  $(r,s_1)$ ,  $a-12\le r\le t$ Under  $B$ 's chart, these are near-stem endpoints with canonical rows  $2,\ldots,z-1$ , all within its depth  $z+4$ .Right:  $(r,b_3)$ ,  $a-12\le r\le t$ These form one entire column of the  $J_3$  bar.Top:  $(a-13,c)$ ,  $s_1+1\le c\le b_3-1$ These lie in  $B$ 's canonical bar row  $1$ , whose full endpoint interval covers them.Bottom:  $(t+1,c)$ ,  $s_1+1\le c\le b_3-1$  $P_1$ 's first bar row covers  $[s_1+1,s]$ , which contains this entire interval by (5).Thus these are genuinely complete walls. The proof is not relying on a few corner guards.No diagonal corner site is needed. A path in the nearest-neighbor grid graph can first leave an integer rectangle only through one of these four walls.2. The forced site is an original support and is absent from the prefixTake
$$q=(t,s_1+1).$$
In  $B$ 's canonical coordinates,
$$r=t-(a-14)=z-1,\qquad
c=(s_1+1)-(s_1-1)=2.$$
Because  $z$  is even,  $z-1$  is odd. Therefore
$$\boxed{q\text{ is precisely the original near-lateral support }(z-1,2)\text{ of }B.}$$
This membership does not depend on whether another original eventually consumes the support.The site is absent from the selected endpoint union: $B$  has no endpoint at canonical column  $2$  on row  $z-1$ .Every staircase endpoint has column at least its bar start, and
$$b_i\ge b_3\ge s_1+2>s_1+1.$$
 $A$ 's terminal row is at most  $t-1$ , so  $A$  has ended before  $q$ 's row.The first-block  $H_3$  endpoints are farther right. Even the exceptional leftmost column of  $X_0$ , namely  $s-4$ , is strictly right of
$$s_1+1=s-v-11.$$
Later blocks have no endpoint before  $P_1$ 's first row  $t+1$ .The root and  $R$  lie farther right.Two distinct neighbors of  $q$  are already retained endpoints:
$$(t,s_1)\in B,
\qquad
(t+1,s_1+1)\in P_1.
\tag{6}$$
Now apply the support rule in a hypothetical complete extension. If  $q$  remained absent from the full endpoint union, its immutable original-support status would require exactly one occupied neighbor. Equation (6) supplies at least two, and additional originals cannot remove either one.Therefore a complete extension must contain an original having  $q$  as an endpoint.That original must be fresh: no retained original contains  $q$ , and retained originals cannot be enlarged or altered.3. Endpoint connectivity traps the entire consumerThe relevant graph is the endpoint-induced nearest-neighbor graph, not the graph consisting only of matching edges.For a full  $U(H,d,f)$ , this endpoint graph is connected:its two bar rows form a connected  $2\times H$  rectangle;each stem is a contiguous path attached to the bar.The rotor is also connected. For example, the following seven edges form a spanning tree of its eight endpoints:
$$\begin{aligned}
&(1,2)-(2,2),\qquad (2,2)-(2,3),\qquad (2,3)-(2,4),\\
&(2,2)-(3,2),\qquad (3,2)-(3,1),\\
&(2,3)-(3,3),\qquad (3,3)-(4,3).
\end{aligned}$$
Every permitted lattice isometry preserves this connectivity.Suppose the fresh original containing  $q\in C$  had an endpoint outside  $C$ . By connectivity, an endpoint path within that original joins  $q$  to the outside endpoint. Its first vertex outside  $C$  is one of the retained wall endpoints established in Section 1.That vertex would belong both to the fresh original and to a retained original, contradicting endpoint-disjointness. Hence
$$\boxed{\text{every endpoint of the fresh original must lie in }C.}
\tag{7}$$
This is an obstruction to every possible consumer, including consumers with arbitrarily large dimensions. It does not depend on a proposed orientation or a chosen local replacement.4. The width obstruction covers every permitted orientationIt is helpful to express the projection argument using numbers of occupied coordinate levels, avoiding any ambiguity between span and width.For a canonical full  $U(H,d,f)$ :the column projection has  $H\ge6$  distinct values;the row projection has  $\max(d,f)+1\ge5$  distinct values.A square-lattice rotation or reflection preserves or exchanges these projections, up to translation and reversal. Consequently,
$$\boxed{\text{every permitted orientation of a full }U\text{ needs at least five columns}.}$$
The rotor has exactly four distinct row coordinates and four distinct column coordinates. Thus every permitted orientation needs exactly four columns.Neither type fits in a rectangle with at most three columns, regardless of its height.If
$$D_3\ge u+v+20,$$
then, together with  $D_3\le u+v+22$ , equation (4) gives
$$1\le W\le3.$$
The forced original from Section 2 would have to fit inside this rectangle by (7), which is impossible.Since  $D_3$  is even, excluding  $D_3\ge u+v+20$  proves
$$\boxed{H_3=z-2\ \Longrightarrow\ D_3\le u+v+18}$$
whenever the selected prefix has a complete extension.The occupied walls and the two occupied neighbors of  $q$  persist under additions. Therefore later originals cannot defeat this argument by opening the cavity, removing the forcing condition, or changing a retained original.5. The three compensation cases are exhaustiveUse the accepted normal form
$$y_i=a-10-i+H_i,\qquad
b_i=P-D_i,\qquad
e_i=b_i+G_i,$$
and
$$t=a+z-15.$$
The accepted height and parity calculation gives
$$y_0,y_2\le t-1,\qquad y_1,y_3\le t.$$
Only the odd-indexed owners  $J_1,J_3$  can meet  $P_1$ . Thus the proposed cases exhaust all possibilities: $J_3$  meets  $P_1$ , whether or not  $J_1$  also does. $J_3$  does not, but  $J_1$  does.Neither does.The exact selected-prefix identity remains
$$\Delta\Phi
=\frac u2+v+\frac L2+22-\frac{D_3}{2}+\eta.
\tag{8}$$
Case 1:  $J_3$  meets  $P_1$ This means
$$y_3=t,$$
hence
$$a-13+H_3=a+z-15
\quad\Longrightarrow\quad
H_3=z-2.$$
The cavity lemma therefore gives
$$D_3\le u+v+18.$$
Apply the previously accepted intermediate bound
$$\Delta\Phi\ge u+v+\frac L2+25-D_3.$$
It follows immediately that
$$\boxed{\Delta\Phi\ge \frac L2+7.}
\tag{9}$$
This branch does not assume that  $J_3$  is the only  $P_1$ -contact owner.Case 2:  $J_1$  meets  $P_1$ , but  $J_3$  does notHere
$$y_1=t,\qquad y_2\le t-1,\qquad y_3\le t-2.$$
No far-pair receipt remainsThe only possible staircase pair is upper  $J_1$ , lower  $J_2$ . It would require
$$y_2=y_1+1=t+1,$$
contradicting  $y_2\le t-1$ . $J_1$  has no  $A$ -boundary debitThe last row of  $A$ 's far stem is at most  $t-1$ . Its terminal row is odd, so it is in the preceding physical tile row. It cannot interact intratile with the even far row  $y_1=t$ . $J_3$  also has no  $A$ -boundary debitThe minimum height and the assumption that  $J_3$  does not meet  $P_1$  give
$$a-7\le y_3\le t-2.$$
This entire range lies inside  $J_1$ 's bar row interval
$$[a-10,t].$$
Since  $b_3<b_1$ , the  $J_3$  far interval starts to the left of that bar. If it reached  $b_1$ , it would contain the occupied endpoint
$$(y_3,b_1)\in J_1.$$
Endpoint-disjointness therefore forces
$$e_3\le b_1-2,
\tag{10}$$
using evenness.Also,
$$D_1\ge D_0+2\ge u+L+16$$
implies
$$b_1=P-D_1\le s-L-4.$$
Combining this with (10),
$$e_3\le s-L-6.$$
In particular,  $J_3$  cannot reach the  $A$ -adjacent column  $s-L$ .This proves the proposed “ $J_1$  at the bottom excludes a  $J_3/A$  debit” claim for all allowed dimensions.Basic branch boundThe only remaining negative receipt group is  $J_1/P_1$ , with receipt
$$-\frac{G_1}{2}-1.$$
Its far endpoint satisfies  $e_1\le s$ , so
$$G_1\le s-b_1=D_1-u-12.$$
The ordinary depth steps give  $D_1\le D_3-4$ . Hence
$$\eta\ge-\frac{D_3-u-16}{2}-1.$$
Substitution in (8) gives
$$\begin{aligned}
\Delta\Phi
&\ge
\frac u2+v+\frac L2+22-\frac{D_3}{2}
-\frac{D_3-u-16}{2}-1\\
&=u+v+\frac L2+29-D_3\\
&\ge \frac L2+7.
\end{aligned}
\tag{11}$$
The optional stronger branch bound is also validThe  $J_2$  far row satisfies
$$a-6\le y_2\le t-1,$$
so it too lies within the continuing  $J_1$  bar.Because  $b_2<b_1$ , disjointness forces
$$b_2+G_2\le b_1-2.$$
Equivalently,
$$D_2\ge D_1+G_2+2\ge D_1+6.$$
Together with  $D_3\ge D_2+2$ , this yields
$$D_3\ge D_1+8.$$
Thus
$$G_1\le D_3-u-20,$$
and the same ledger gives
$$\boxed{\Delta\Phi
\ge u+v+\frac L2+31-D_3
\ge\frac L2+9\ge12.}
\tag{12}$$
Case 3: neither odd owner meets  $P_1$ There is no  $P_1$  debit. The single possible staircase pair costs at most  $1$ , and the two possible  $A$  debits cost at most  $2$ . Therefore
$$\eta\ge-3.$$
Equation (8) gives
$$\begin{aligned}
\Delta\Phi
&\ge \frac u2+v+\frac L2+19-\frac{D_3}{2}\\
&\ge \frac v2+\frac L2+8\\
&\ge \frac L2+14,
\end{aligned}
\tag{13}$$
since  $D_3\le u+v+22$  and  $v\ge12$ .Equations (9), (11), and (13) prove the uniform complete-prefix conclusion
$$\boxed{\Delta\Phi\ge\frac L2+7\ge10.}$$
6. No receipt or source unit is reusedThe new proof introduces no new full-tile credit.Case 1 uses the accepted receipt bound with a newly restricted  $D_3$ .Case 2 removes impossible pair and  $A$  debits and bounds the one surviving  $P_1$  interval.Case 3 removes the  $P_1$  debit group.The existing ownership descriptions remain sufficient:credited staircase-pair tiles are wholly covered by  $J_1/J_2$ ;credited  $P_1$  tiles contain  $P_1$  endpoints;the neutral rotor tile contains three rotor endpoints;upper credits lie in the separately counted upper rows.Endpoint-disjointness prevents reuse of these credited full tiles. The directed events remain assigned by the accepted owner and row partition, and the four staircase source contributions remain included exactly once in (8).The hypothetical complete extension is used to constrain the selected geometry through the cavity lemma. Its other originals are not added to the selected-prefix ledger, and no claim about their marginal contributions is used.7. The boundary controls need one parameter-range correctionThere is a convenient uniform statement of all three families. Keep  $J_0,J_1,J_2$  from the preceding equality family, keep  $f=6$ , and for  $k=0,1,2$  set
$$J_3^{(k)}
=
\bigl(z-2,\ u+v+22-2k,\ v+10-2k\bigr).$$
Then
$$b_3^{(k)}=s-v-10+2k,\qquad
e_3^{(k)}=s,$$
and the cavity width is
$$W_k=1+2k.$$
But the unchanged  $J_2$  has
$$D_2=u+L+20,$$
so the required final depth step is
$$D_3^{(k)}-D_2
=v-L+2-2k\ge2.$$
Therefore the family is admissible only when
$$\boxed{L\le v-2k.}
\tag{14}$$
Under (14), the shifted  $J_3$  bar remains at least two columns left of the  $J_2$  bar. The earlier endpoint-disjointness and receipt-exhaustion arguments persist. The far-pair and  $A$  receipts stay  $-1$  each; the sole  $P_1$  interval now has  $G_3=v+10-2k$ . Hence
$$\eta_k=-\frac v2-8+k,$$
while the upper expression increases by  $k$ . Consequently,
$$\Delta\Phi_k=\frac L2+3+2k.$$
The correct control statement is:Cavity widthAdmissible family rangeExact selected gainComplete-extension conclusion $1$  $6\le L\le v$  $L/2+3$ Excluded by the cavity lemma $3$  $6\le L\le v-2$  $L/2+5$ Excluded by the cavity lemma $5$  $6\le L\le v-4$  $L/2+7$ Not decided by this lemmaThe width- $5$  range is already correctly stated in the note. The width- $3$  range should be added explicitly.Concrete failure of the unrestricted width- $3$  constructionAt  $L=v$ , reducing the old  $D_3$  by  $2$  gives
$$D_3'=u+v+20=D_2,$$
so
$$b_3'=b_2=s-v-8.$$
Both bars contain
$$(a-11,s-v-8).$$
Indeed,  $J_2$ 's bar starts on that row, while  $J_3$ 's bar starts one row earlier and continues well below it.For example, with
$$u=v=12,\quad z=24,\quad L=12,$$
both depths become  $44$ , and the bar columns coincide. This is a precise defect in the unqualified family statement, not a counterexample to the cavity or compensation theorem.8. The first- $P_1$ -contact control is consistentFor the displayed parameters
$$u=12,\quad v=20,\quad z=24,\quad L=6,\quad f=4,$$
the starts and far intervals, relative to  $s$ , are:OwnerBar startFar rowFar interval $J_0$  $s-20$  $a-4$  $[s-20,s-16]$  $J_1$  $s-22$  $t=a+9$  $[s-22,s]$  $J_2$  $s-28$  $a-6$  $[s-28,s-24]$  $J_3$  $s-30$  $a-5$  $[s-30,s-26]$ The short rays avoid the continuing  $J_1$  bar. There is no  $J_1/J_2$  far-pair contact, no  $A$  debit, and no additional mixed full tile from those short rays. The sole residual group is  $J_1/P_1$ , with  $G_1=22$ :
$$\eta=-\frac{22}{2}-1=-12.$$
The upper expression equals
$$\frac{12}{2}+20+\frac62+22-\frac{54}{2}=24.$$
Thus its exact gain is
$$\boxed{\Delta\Phi=24-12=12,}$$
as claimed. This attains the stronger second-branch bound geometrically, without establishing complete extendibility.With the width- $3$  family range corrected, the new mathematical claims are sound at their stated conditional scope. The width- $1$  and admissible width- $3$  controls cannot occur as prefixes of any complete extension in the explicit model. The width- $5$  controls pass this particular obstruction, while their complete extendibility and all global-allocation questions remain unresolved.

