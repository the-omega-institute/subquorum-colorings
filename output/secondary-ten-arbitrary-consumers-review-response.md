ACCEPTThe new mathematical statements are correct on their stated scope. In particular:The single-block actual-consumer classification is exhaustive.The collision table is necessary and sufficient for endpoint disjointness.The exact equality cases are
$$T_{\mathrm{right}},\qquad H=w+14,\qquad d=6,\qquad f\in\{4,6,8\}.$$
Replacing  $X$  by any of the permitted tail originals preserves the single-block classification and receipts.Under the explicit nesting and bar-row hypotheses, the additional adjacent-pair debit is exactly
$$-(H_{\mathrm{child}}+2).$$
Each insertion after the first has marginal gain exactly  $-3$ , and the joint gain is
$$H_0-3n+2,$$
with each source mass included and canceled only once.I found two local exposition issues in Section 3, detailed below: the unqualified description of an upper tile as having three endpoints has boundary exceptions, and one event-direction sentence needs an explicit absolute-row parity qualifier. The numerical tables and theorem statements already handle these cases correctly.This review concerns the ordinary geometric proofs. I do not certify any code execution or Lean result.1. Actual-consumer roles and the original chargeThe two U frames exhaust the surviving rolesIn coordinates relative to  $(a,s)$ , the renewed support is
$$t=(-4,0).$$
Its west, east, and south neighbors are retained endpoints. If  $t$  remains unconsumed, its occupied degree is at least three, so completeness forces it to be an endpoint of another actual original.Endpoint disjointness prevents the new owner from using those three neighbors as its own endpoints. Its mandatory matching partner must therefore be north.Every nonterminal endpoint of a canonical U has at least two own endpoint neighbors. Consequently a U owner must use  $t$  as a leg terminal. Full leg exchange and the two horizontal orientations give precisely
$$(r,c)\longmapsto(-4-d+r,1-c)$$
and
$$(r,c)\longmapsto(-4-d+r,-1+c).$$
The rotor exclusion is also correct. Fixing a rotor tip at  $t$  with its matching partner north leaves two placements up to the rotor’s rotational symmetry. One has endpoint offsets from  $t$ 
$$(-3,-1),(-2,-1),(-2,0),(-2,1),
(-1,0),(0,0),(-1,-1),(-1,-2).$$
It contains  $t+(-2,1)=(-6,1)$ . Its horizontal reflection also contains  $(-6,1)$ , because the first placement contains both  $(-2,-1)$  and  $(-2,1)$ . Thus both collide with the retained  $P^0$  endpoint.There is no missed rotor chirality or nonterminal U role.The relative and absolute parities are used correctlySet
$$R=-4-d.$$
As the question emphasizes,  $R$  is even in relative coordinates, while  $a+R$  is odd in absolute coordinates. Thus the two bar rows  $R,R+1$  lie in different physical tile rows.Write  $d=2u$ ,  $f=2v$ . Both frames have
$$H-1+u+v$$
matching edges.For the right frame, the bar occupies  $H$  endpoint tiles across its two physical tile rows. The legs add  $u-1$  and  $v-1$ , giving
$$T_{\mathrm{source}}=H+u+v-2.$$
Only the odd intrinsic lateral rows contribute original supports inside these endpoint tiles:
$$I_{\mathrm{source}}=u+v-2.$$
Hence
$$q(T_{\mathrm{right}})
=(H-1+u+v)+(u+v-2)-2(H+u+v-2)
=1-H.$$
For the left frame, the unaligned bar contributes  $H+2$  endpoint tiles, so
$$T_{\mathrm{source}}=H+u+v.$$
The inside supports are the  $u+v$  even intrinsic lateral supports and the two bar-exterior supports:
$$I_{\mathrm{source}}=u+v+2.$$
This again gives
$$q(T_{\mathrm{left}})=1-H.$$
The axial supports lie in the next physical tile rows beyond the terminals. All these counts use the original supports, including supports already occupied by another original’s endpoints.2. The complete collision frontier is correctLeft frameFor the left frame, the far column is
$$1-H\le-5.$$
Every old endpoint has column at least  $-4$ . At the boundary  $H=6$ , columns  $-5$  and  $-4$  lie in different physical tile columns.The bar has maximum column  $0$  and is above the western rotor. Its near column  $0$  contains no old endpoint at any row at most  $-4$ . Therefore every legal left frame is endpoint-disjoint, including  $d=4$  and arbitrarily large  $f$ .Large  $f$  does not create an exception: the far stem remains in its separated column regardless of how far it extends.Right frameAt  $d=4$ , the row- $-8$  bar contains  $(-8,1)$ , an old  $P^0$  endpoint. This excludes every right frame with  $d=4$ .For  $d\ge6$ , both bar rows are above the old endpoint inventory. The near stem is collision-free. Thus only the far column
$$C=H-1$$
needs classification.The first-old-endpoint table is exhaustive:Odd far column  $C$ First old endpoint rowGoverning source $5\le C\le w+11$  $-8$  $P^0$  bar $C=w+13$  $0$  $E$  far terminal $w+15\le C\le w+h+13$  $-6$ Root  $K$  bar $C\ge w+h+15$ NoneBeyond the old endpoint columnsThe source exclusions used here are correct. In particular,  $P^0,V,T0$  cannot introduce an earlier endpoint in the exceptional or root ranges. The root’s rightmost column is beyond the entire base’s rightmost endpoint because  $h\ge6$ . The unbounded  $V$  stem does not create an exception: it lies in column  $2$ , outside these possible far columns.The far terminal row is
$$R+f=-4-d+f,$$
which is even relative to  $(a,s)$ . Requiring it to stop strictly before the first old endpoint gives respectively
$$f\le d-6,\qquad
f\le d+2,\qquad
f\le d-4,$$
or no restriction.These conditions are sufficient as well as necessary. They reproduce every row of the stated table.Two boundary points are handled correctly:For  $d=6$ , the narrow and root-range bounds are incompatible with  $f\ge4$ , while the special width permits exactly  $f=4,6,8$ .For  $d=8$ , the narrow row is empty because  $f\le2$ . The table expresses this through its stated condition; it does not incorrectly assert existence at that depth.3. The single-block tile and event receipts are correctCommon near-stem contributionThe two common new full tiles have minima
$$(-7,0),\qquad(-5,0).$$
For the left frame, both directions survive exactly at relative rows  $-7,-5$ :
$$T:(j,0)\longrightarrow P^0:(j,1),
\qquad
P^0:(j,1)\longrightarrow T:(j,0).$$
Thus
$$(\Delta F,\Delta E)=(2,4),$$
and the contact contribution is zero.For the right frame, the surviving directions are
$$T\longrightarrow P^0
\quad\text{at relative rows }-8,-6,-4,$$
and
$$P^0\longrightarrow T
\quad\text{at relative rows }-7,-5.$$
Therefore its common contribution is
$$(\Delta F,\Delta E)=(2,5),$$
with signed contact contribution  $-1$ .The exclusions are correct at the boundary  $d=4$  for the left frame. At row  $-8$ , the relevant exclusions are bar-exterior supports; at the lower even relative rows they are lateral supports. The four surviving left-frame events remain exactly the same.The geometric contacts with  $Z$  at  $t$  cross physical tile boundaries. The small  $X$  contributes no additional tile or event, including when the left far column is  $-5$ .Deep right consumersFor  $d\ge8$ , a surviving far stem inside the  $P^0$  breadth ends by relative row  $-10$ . A surviving far stem in the root range ends by  $-8$ . The other column in each corresponding physical tile strip has no old endpoint early enough to create an additional receipt.The exceptional column  $C=w+13$  is different because its partner column  $w+12$  contains the  $P^0$  near stem beginning at row  $-8$ .When
$$m=\frac{f-d+4}{2}\in\{0,1,2,3\},$$
the far terminal is at  $-8+2m$ . The additional full tiles are exactly the  $m$  tiles with minima
$$(-7+2j,w+12),\qquad 0\le j<m.$$
The additional events are exactly
$$T\longrightarrow P^0
\quad\text{at }-8,-6,\ldots,-8+2m,$$
and
$$P^0\longrightarrow T
\quad\text{at }-7,-5,\ldots,-9+2m.$$
They number  $2m+1$ . Hence the extra signed contribution is
$$2m-(2m+1)=-1.$$
The  $m=0$  case is particularly important: it contributes one event and no full tile. Thus the condition defining  $\epsilon$  correctly includes the boundary  $f=d-4$ .This establishes the deep-right receipts
$$(2,5)
\quad\text{or}\quad
(2+m,6+2m),$$
and gains  $H-2$  or  $H-3$ , respectively.Right consumers with  $d=6$ The adjacent bar rows  $-9,-8$  contribute both directions at every column  $1,\ldots,w+12$ , giving
$$2(w+12)$$
events. The original-support tests are correct: the targets are at intrinsic row  $2$  in non-stem columns for  $T$ , and intrinsic row  $-1$  for  $P^0$ .In the wide case, the bar band has  $w/2+6$  new full tiles. Adding the two near-stem tiles and five near events gives
$$\Delta F=w/2+8,\qquad
\Delta E=2w+29.$$
Therefore
$$\Delta=H-w-14.$$
At  $H=w+14$ , the far stem completes the additional top corner tile. For  $f=4+2e$ , it also supplies  $e+1$  lower far-stem tiles and  $3+2e$  horizontal events. Thus
$$\Delta F=w/2+10+e,\qquad
\Delta E=2w+32+2e,$$
and
$$\Delta=1.$$
There is no event duplication at the upper corner: the vertical bar-band event and horizontal stem event may share an endpoint, but their ordered endpoint-target pairs differ.Exact equality classificationThe surviving gains satisfy:CaseGain and lower boundLeft $H-1\ge5$ Deep right without special far contact $H-2\ge4$ Deep right with special far contact $H-3\ge23$ , since  $H=w+14\ge26$ Right  $d=6$ , wide $H-w-14\ge h+2\ge8$ Right  $d=6$ ,  $H=w+14$ ,  $f=4,6,8$  $1$ Consequently the equality classification is exactly as stated. It removes the specified- $Y$  hypothesis in this single-block local union.Two corrections to the Section 3 proseThe “upper partial tile has only three endpoints” sentence needs a case distinction. For
$$\{-9,-8\}\times\{0,1\},$$
the actual endpoint count is:CaseEndpoint countLeft  $d=4$  $2$ Left  $d\ge6$  $3$ Right  $d\ge8$  $3$ Surviving right  $d=6$  $4$ In the last case, the tile is already correctly included in the later bar-band calculation. A suitable replacement is:Above the two lower near-stem tiles, the tile with minimum  $(-9,0)$  is partial for left consumers and deep right consumers. It has two endpoints when left  $d=4$ , and three in the other such cases. For right  $d=6$ , it is full and belongs to the bar band counted below.The special  $d=6$  far-event sentence should specify absolute row parity. “Odd-row  $T$ -to- $P^0$ ” is correct for absolute rows. In the normalized chart, the surviving  $T\to P^0$  directions are at even relative rows, and the reverse directions are at odd relative rows.For maximum precision, the special-case lists can be written as
$$T\to P^0
\quad\text{at }-8,-6,\ldots,-6+2e,$$
and
$$P^0\to T
\quad\text{at }-7,-5,\ldots,-7+2e.$$
These give the stated  $3+2e$  events.Neither correction changes a receipt or theorem.4. The single-block tail replacement is validReplacing  $X$  by any permitted
$$J=U(w,D,D-6),\qquad D\ge z-2,$$
preserves the three neighbors forcing consumption of  $t$ .It also preserves the collision classification. Removing  $X$  admits no previously excluded right consumer: those exclusions come from  $P^0,E,K$ , which remain. Every previously allowed consumer is separated from  $J$  as follows:A left far stem has column at most  $-5$ .Every near stem ends at relative row  $-4$ , while  $J$  starts at  $-2$ , in a different physical tile row.A right far stem inside the  $P^0$  breadth must end by  $-10$ .Every other right far column is at least  $w+13$ , beyond  $J$ ’s maximum column  $w$ .Every consumer bar lies above  $J$ .These are geometric tile separations. They exclude additional full-tile completions as well as directed events.The local inequalities therefore follow:
$$\Phi(H_3\cup\{T\})\ge b+h-1,$$
and, for the tail inventory,
$$\Phi(H_{\mathrm{tail}}\cup\{T\})\ge b+h-5\ge b+1.$$
They remain inequalities for the selected subinventory. The proof supplies no monotonicity under arbitrary additional originals.5. The nested construction is legal and its separation proof is sufficientHere  $R_i$  denotes an absolute row. Each  $R_i$  is odd, and
$$d_i=a_i-4-R_i$$
is even. The hypotheses imply
$$d_0\ge2n+8\ge10,
\qquad
d_{i+1}-d_i=z_i-8\ge16.$$
Thus every displayed original is legal, and its near terminal is exactly
$$(R_i+d_i,s_i)=(a_i-4,s_i)=t_i.$$
With
$$\ell_i=s_i+1-H_i,$$
the nesting condition gives
$$\ell_i\le\ell_{i+1}-2,
\qquad
s_i-s_{i+1}=w_{i+1}+12\ge24.$$
The next bar therefore lies strictly inside the preceding bar interval, with the stated margins.These margins handle the potential stem exceptions:An earlier near stem lies to the right of every later bar.An earlier far stem lies to the left of every later bar.Nonadjacent far-stem columns are separated by at least four columns.Later bar rows begin below earlier bar rows.Hence no consumer endpoints collide. Nonadjacent consumers have no shared endpoint tile or intratile adjacency.The global height estimate is also correct:
$$R_{n-1}+4\le a_0-10.$$
Every old  $H_3$  endpoint has row at least  $a_0-8$ . These bounds lie in different physical tile rows. Therefore no consumer bar or far stem has an old intratile contact.Only each consumer’s near stem can meet the old inventory. Earlier originals lie to its right, later originals begin below its terminal, and its sole local contact is the left-frame  $P_i^0$  strip. Thus, against the whole old chain,
$$\Delta F_i=2,\qquad
\Delta E_i=4,\qquad
\Delta\Phi(T_i\mid H_3)=H_i-1.$$
This isolated receipt does not assume that the blocks are independent after other consumers have been inserted.6. The exact adjacent debit and the  $-3$  insertion marginalLet  $j=i+1$ . The relevant rows are
$$R_i+1,\qquad R_j=R_i+2.$$
Since  $R_i$  is odd absolute, these are an even row followed by an odd row, forming one physical tile row.For every column in
$$[\ell_j,s_j],$$
the two bar endpoints are adjacent. Both directions survive:In  $T_i$ ’s coordinates, the child target has intrinsic row  $2$  and lies strictly inside the parent’s stem columns.In  $T_j$ ’s coordinates, the parent target has intrinsic row  $-1$ .Neither target is an original support of its source owner. Therefore
$$\Delta E_{\mathrm{cross}}=2H_j.$$
The child overlap begins at odd  $\ell_j$  and ends at even  $s_j$ . Its fully contained physical column pairs number
$$\frac{H_j}{2}-1.$$
Each extreme tile has three endpoints.The missing extreme cells cannot be filled by another owner. At the left, the parent far stem is at most  $\ell_j-2$ , whereas the missing child-row cell is at  $\ell_j-1$ . At the right, the parent near stem is at least 24 columns beyond  $s_j$ . Earlier consumers’ far stems lie still farther left; later bars have not reached this tile row; and the entire band is above the old inventory.Thus
$$\Delta F_{\mathrm{cross}}=\frac{H_j}{2}-1,$$
and
$$2\Delta F_{\mathrm{cross}}-\Delta E_{\mathrm{cross}}
=2\left(\frac{H_j}{2}-1\right)-2H_j
=-(H_j+2).$$
The full set partition gives the claimed joint ledgerThe adjacent-pair bands occupy distinct physical tile rows. They are disjoint from the individual near-stem receipts, which occur down in the old blocks. There are no nonadjacent contributions.Accordingly, the total new sets have cardinalities
$$\Delta F
=2n+\sum_{j=1}^{n-1}\left(\frac{H_j}{2}-1\right),$$

$$\Delta E
=4n+\sum_{j=1}^{n-1}2H_j,$$
while
$$\Delta S=\sum_{i=0}^{n-1}(H_i-1),
\qquad
\Delta N=0.$$
Substitution gives
$$\begin{aligned}
\Delta\Phi
&=\sum_{i=0}^{n-1}(H_i-1)
-\sum_{j=1}^{n-1}(H_j+2)\\
&=H_0-3n+2.
\end{aligned}$$
Every child mass occurs once in this equation. Its cancellation against its incoming bar-band debit is not an additional budget available elsewhere.The insertion claim can be checked directly. For  $j\ge1$ , adding  $T_j$  after its predecessors gives
$$\Delta S=H_j-1,$$

$$\Delta F=2+\left(\frac{H_j}{2}-1\right)=\frac{H_j}{2}+1,$$

$$\Delta E=4+2H_j.$$
Therefore
$$\Delta\Phi
=(H_j-1)+2\left(\frac{H_j}{2}+1\right)-(4+2H_j)
=-3.$$
This establishes the negative marginal exactly. For  $n=1$ , the formula reduces correctly to  $H_0-1$ , with no adjacent debit.7. Compensation, tail compatibility, and the remaining scopeTelescoping the breadth assumptions yields
$$H_0\ge6+\sum_{j=1}^{n-1}(w_j+14)
\ge6+26(n-1).$$
Consequently
$$H_0-3n+2\ge23n-18\ge n$$
for every  $n\ge1$ . The nested family therefore compensates the original chain’s relative deficit.For the nested tail version, every consumer endpoint has row at most  $a_{n-1}-4$ , whereas every  $J$  endpoint has row at least  $a_{n-1}-2$ . These endpoint sets share no physical tile row. The accepted  $-4$  tail debit therefore remains a separate term, and
$$\Phi\ge\sum_i(w_i+9)+h-5
\ge\sum_i(w_i+9)+1$$
follows.The remaining incompleteness witness is valid. The last  $E$  axial support
$$u=(a_{n-1}-1,s_{n-1}+w_{n-1}+13)$$
is untouched by the nested consumers: their near stems end above it, and their other endpoints lie above the entire old inventory. Its three retained endpoint neighbors persist.The same obstruction also survives every allowed single-block consumer. A right consumer in column  $w+13$  must terminate by relative row  $-2$ , so it cannot consume  $u$  at row  $-1$ ; the other allowed consumers miss its column or row. Thus the stronger single-block classification does not accidentally produce a completeness assertion.The package keeps the required scope distinctions intact. Completeness forces a  $t$ -consumer, and the single-block theorem classifies its allowable source shape and local receipt. The nested theorem supplies an exact joint calculation only under its explicit breadth and bar-row conditions. Neither result classifies arbitrary multi-block consumers, proves extendibility of the displayed inventories, or establishes monotonicity under further additions.The open step remains control of arbitrary multi-block consumer geometry and its joint signed contact contribution. The new results advance that question without reusing child budgets or claiming the global target.
