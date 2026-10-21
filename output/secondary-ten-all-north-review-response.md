ACCEPTThe applied  $T_2/Z$  repair closes the previous review issue, and the new all-width, all-leg-length left north-terminal extension is correct on its stated scope. No further mathematical repair is required.In particular:The three regimes in Theorem 1 give an exhaustive and exact endpoint-disjointness classification.The new  $g=3$ , first-residual zero boundary has exactly the stated event
$$Q:(a+10,3)\longrightarrow K:(a+9,3).$$
Both zero boundaries give the same exact  $J$ -disjointness inequalities and the same contribution  $\Delta\Phi=h-2\ge4$ .The complete-family exclusions follow from the mandatory-original-support convention and the full stated endpoint-role catalogue.This verdict concerns the supplied ordinary mathematical arguments. I have not executed the checkers or Lean, and I do not use the reported finite controls or execution results as proof.1. The previous documentation repair is completeThe declarations
$$T_2=U(w+10,10,4),\qquad
T_2(r,c)=(a-8+r,w+13-c),$$
and
$$Z(r,c)=(a+2-r,w+12+c)$$
now determine the originals whose placement was previously missing.The insertion figures are consistent:
$$q(T_2)=-(w+9),\qquad
\Delta F(T_2\mid A)=\frac w2+5,\qquad
\Delta E_v(T_2\mid A)=2w+19,$$
so
$$\Delta\Phi(T_2\mid A)
=(w+9)+2\left(\frac w2+5\right)-(2w+19)=0.$$
The mixed interaction with  $Z$  consists of precisely one jointly completed mixed full tile and one additional directed event:
$$T_2:(a-1,w+12)\longrightarrow Z:(a-1,w+13).$$
The reverse direction is excluded because its target is an original support of  $Z$ . For the surviving direction, the target has  $T_2$ -coordinates  $(7,0)$ ; at this odd near-leg index,  $T_2$ ’s lateral support is at  $(7,2)$ , so the target is not excluded.Thus the mixed second difference is indeed
$$2\cdot1-1=1,$$
and the insertion table remains
$$\begin{array}{c|c}
\text{Insertion}&\Delta\Phi\\ \hline
T_2\mid A&0\\
Z\mid A&1\\
Z\mid A+T_2&2\\
T_2\mid A+Z&1.
\end{array}$$
The new wording supplies both components of this receipt and removes the earlier ambiguity. No additional credit is available from counting the same full tile or cross-event again.2. Theorem 1: the endpoint-disjointness classification is exhaustiveWrite
$$R=a+1-\ell,\qquad
g=w+15-s,\qquad
B=w+12-k\in\{4,2\}.$$
The endpoint geometry of  $K$  is:Bar rows  $R,R+1$ , spanning columns  $g,\ldots,w+14$ .Near stem in column  $w+14$ , ending at row  $a+1$ .Far stem in column  $g$ , ending at
$$u=a+1-\ell+m.$$
Because  $s,w$  are even,  $g$  is odd. Since  $s\ge6$ ,
$$g\le w+9.$$
2.1 The common lower bound  $\ell\ge10$ The note’s single collision witness works for all three smaller legal depths:
$$(a+2-\ell,w+11).$$
Its  $K$ -coordinates are  $(1,4)$ , so it is present for every  $s\ge6$ . Its  $V$ -coordinates are
$$(8-\ell,1).$$
For  $\ell=4,6,8$ , these are respectively
$$(4,1),\quad(2,1),\quad(0,1),$$
all endpoints of  $V$ . Thus every endpoint-disjoint  $K$  has  $\ell\ge10$ .Once  $\ell\ge10$ , the bar’s last row satisfies
$$a+2-\ell\le a-8.$$
Every endpoint of  $A$  has row at least  $a-6$ , so the bar is disjoint from  $A$ .The near stem is also disjoint: it ends at  $(a+1,w+14)$ , immediately before  $C$ ’s far stem begins at  $(a+2,w+14)$ . No other old endpoint in that column creates an obstruction. Therefore only the far column remains to classify.2.2 The far column inside the  $V$  barSuppose  $g\ge B$ . Since  $g\le w+9<w+11$ , this column lies inside  $V$ ’s upper bar interval.The first old endpoint encountered by the descending far stem is
$$(a-6,g).$$
Its intrinsic row in  $K$  is  $\ell-7$ . Therefore the stem reaches it exactly when
$$m\ge\ell-7.$$
Avoidance is exactly
$$m\le\ell-8.$$
Because  $m\ge4$ , this implies  $\ell\ge12$ . Conversely, the bound puts the far terminal at most at row  $a-7$ , strictly before every old endpoint in that column.Hence this regime is exactly
$$\boxed{g\ge B:\quad \ell\ge12,\quad m\le\ell-8.}$$
The stated width equivalence is also correct. Algebraically,
$$g\ge B
\iff s\le k+3,$$
and evenness of  $s,k$  makes this equivalent to  $s\le k+2$ .2.3 The first-residual escape at  $g=3$ Suppose  $B=4$  and  $g=3$ . The  $V$  bar and far stem lie at or to the right of column  $4$ ;  $T_0$ ’s leftmost endpoint column is  $5$ . The other fixed originals, apart from  $Q$ , also miss column  $3$ .The only old endpoint in column  $3$  is  $Q$ ’s near terminal
$$q=(a+10,3).$$
Its intrinsic row in  $K$  is  $\ell+9$ . Thus the exact obstruction is
$$m\ge\ell+9,$$
and the exact avoidance condition is
$$\boxed{B=4,\ g=3:\quad \ell\ge10,\quad m\le\ell+8.}$$
This correctly permits far stems extending below the  $V$  bar. Their endpoint column has escaped that bar.The restriction to the first residual is essential and is correctly stated. When  $B=2$ , the same column  $g=3$  lies inside  $V$ ’s bar and belongs to the preceding regime. It then requires  $m\le\ell-8$ , not  $m\le\ell+8$ .2.4 All farther-left escapesIf  $g\le1$ , every old endpoint column is strictly to its right. Consequently no far-leg length can create an endpoint collision, and
$$\boxed{g\le1:\quad \ell\ge10,\quad m\ge4\text{ arbitrary even}.}$$
There is no hidden height restriction in this argument.These cases exhaust every legal width:Residual familyWidth regimes $B=4,\ k=w+8$  $s\le w+10$ : inside the bar;  $s=w+12$ : Q-tip escape;  $s\ge w+14$ : farther-left escape $B=2,\ k=w+10$  $s\le w+12$ : inside the bar;  $s\ge w+14$ : farther-left escapeThus Theorem 1 is an exact unbounded classification.3. The general  $K$  charge and shared-tile sets are correctLet
$$T(R_0,C_0)=\{R_0,R_0+1\}\times\{C_0,C_0+1\},
\qquad R_0,C_0\in2\mathbb Z,$$
and put  $H=(\ell+m)/2$ .The cap’s bar begins at the even row  $a+1-\ell$ , spans two rows in one tile row, and runs from the odd column  $g$  to the even column  $w+14$ . Therefore:
$$|M_K|=s+H-1,$$

$$|\mathcal T_K|=\frac s2+1+H,$$

$$\left|\Sigma_K\cap
\bigcup_{T\in\mathcal T_K}T\right|=H+4,$$
where  $\Sigma_K$  is the original support set.The last count comprises:Two bar-corner supports.Two terminal axial supports.All  $H$  even-indexed outward lateral supports.The odd-indexed inward lateral supports lie outside the endpoint tiles. The separation between the stems, with  $s\ge6$ , prevents any additional counting through the opposite stem.Hence
$$q(K)
=(s+H-1)+(H+4)-2\left(\frac s2+H+1\right)
=\boxed{1}.$$
This source-charge calculation is independent of how long the far leg is.3.1 The common harmless  $C/K$  tileEvery disjoint  $K$  shares
$$T(a+1,w+14)$$
with  $C$ . The adjacent endpoints are
$$K:(a+1,w+14),\qquad C:(a+2,w+14).$$
Each is an original axial support of the other owner. Both directed contacts are excluded, and the tile does not become full.There are no other near-stem shared tiles. There are no bar shared tiles either: even at the smallest surviving depth  $\ell=10$ , the cap bar’s tile row is  $a-9$ , strictly before the first old endpoint tile row  $a-7$ .3.2 The  $V$ -bar zero boundaryInside the bar regime, the far terminal shares an old endpoint tile exactly at
$$m=\ell-8.$$
Then it is  $(a-7,g)$ , and the shared tile is
$$T(a-7,g-1).$$
Because  $g$  is odd and  $g\ge B$ , both columns  $g-1,g$  lie in  $V$ ’s bar. The tile contains  $K$ ’s upper-right endpoint and  $V$ ’s two lower endpoints, so it is not full.The only foreign adjacent endpoint pair is in column  $g$ . Its surviving direction is
$$V:(a-6,g)\longrightarrow K:(a-7,g).$$
The reverse target is  $K$ ’s original far axial support. The forward target lies north of  $V$ ’s bar and is not a  $V$  original support.For a strictly shorter legal far leg, evenness gives  $m\le\ell-10$ . Its terminal tile ends before  $V$ ’s first endpoint tile, so no far shared tile remains.3.3 The new Q-tip zero boundary and its directionIn the first-residual escape,  $K$ ’s far tile column is the pair  $\{2,3\}$ . The only old endpoint in that tile column is  $Q$ ’s tip  $(a+10,3)$ .At
$$m=\ell+8,$$
the far terminal is  $(a+9,3)$ , giving the shared tile
$$T(a+9,2).$$
It contains only those two endpoints, so  $\Delta F=0$ .The direction check is exact:The target of  $K\to Q$ , namely  $(a+10,3)$ , is  $K$ ’s original far axial support. This direction is excluded.The target of  $Q\to K$ , namely  $(a+9,3)$ , has  $Q$ -coordinates
$$(8,2).$$
At the even near-leg index  $8$ ,  $Q$ ’s original lateral support is  $(8,0)$ , not  $(8,2)$ . Thus this direction survives.Equivalently, at  $Q$ ’s tip the original axial support lies west and the terminal lateral support lies south; the new endpoint lies north.Therefore the sole new event is indeed
$$\boxed{
Q:(a+10,3)\longrightarrow K:(a+9,3).
}$$
A long segment of  $K$ ’s column  $3$  can run alongside old endpoints in column  $4$ , but columns  $3$  and  $4$  belong to different fixed tile pairs. That adjacency creates no intratile event. This is the main point needed to justify the claimed exact event set for the escaped stem.3.4 Arbitrarily long stems with  $g\le1$ The far tile column is  $\{g-1,g\}$ , with lower corner  $g-1\le0$ . Every old endpoint tile column has lower corner at least  $2$ .Thus no far shared tile arises, regardless of  $m$ . This proves the unrestricted far-leg assertion without a finite cutoff.Combining the cases,
$$\Delta N=1,\qquad \Delta S=\Delta F=0,$$
and
$$\Delta E_v=
\begin{cases}
1,&g\ge B,\ m=\ell-8,\\
1,&B=4,\ g=3,\ m=\ell+8,\\
0,&\text{otherwise}.
\end{cases}$$
The two exceptional conditions are mutually exclusive. Consequently every disjoint left north-terminal  $K$  has gain exactly  $0$  or  $1$ , with zeros precisely at the two stated boundaries.4. Completeness forces the claimed consumer role at  $p$ For either zero boundary, consider
$$p=(a+2,w+12).$$
It remains absent from  $K$ , including in the new long-leg case. Its inverse  $K$ -coordinates are
$$(\ell+1,3).$$
This is neither a bar endpoint nor an endpoint on either stem: the stem columns are  $1$  and  $s$ , with  $s\ge6$ . This observation is independent of  $m$ .The point remains  $V$ ’s original support  $(8,0)$ , with its original anchor west. Its three occupied neighbors are still
$$(a+2,w+11)\in V,\qquad
(a+2,w+13)\in E,\qquad
(a+3,w+12)\in E.$$
Under the mandatory-original-support convention, it cannot remain unconsumed in a complete family. Its consumer is an additional original relative to  $A+K$ , and its original matching partner must be north of  $p$ .The catalogue reduction remains exhaustive:Only a leg terminal of a legal  $U$  has just one own endpoint neighbor.The rotor’s inner endpoints have three own neighbors.Its two north-terminal footprints both hit  $E$ ’s retained endpoint  $(a,w+13)$ .Therefore a surviving  $U$  consumer has one of the two north-terminal frames. Every right-pointing frame collides with  $K$ :If  $d<\ell$ , its bar hits  $K$ ’s near stem at
$$(a+3-d,w+14).$$
If  $d\ge\ell$ , its near column hits  $K$ ’s bar at
$$(a+2-\ell,w+12).$$
These witnesses use no restriction on the far length  $m$ . The only remaining form is the displayed left-pointing  $J$ .The argument does not require this consumer to be fresh relative to other outstanding obligations. It only establishes that it is distinct from the retained originals in  $A+K$ .5. Both zero boundaries give the same exact  $J$  inequalitiesLet
$$J=U(h,d,f),\qquad
J(r,c)=(a+2-d+r,w+13-c).$$
The two zero regimes share the crucial properties
$$m\ge\ell-8,\qquad s\le w+12.$$
Those are precisely what is needed to extend the earlier cavity proof.NecessityA depth  $d\ge\ell$  hits  $K$ ’s bar. A depth  $d\le8$  hits  $V$ . With even dimensions, disjointness therefore requires
$$10\le d\le\ell-2.$$
If  $h\ge s-2$ , the lower bar row contains
$$(a+3-d,g).$$
This point has  $K$ -coordinates
$$(\ell+2-d,s).$$
For  $10\le d<\ell$ ,
$$2\le\ell+2-d\le\ell-8\le m,$$
so the point lies on the far stem of  $K$ , including when that stem has length  $\ell+8$ . Avoidance forces
$$h\le s-4.$$
Now  $J$ ’s far column is
$$c=w+13-h.$$
The new width bound gives
$$c\ge w+17-s\ge5,$$
while  $h\ge6$  gives  $c\le w+7$ . Thus  $c$  lies inside  $V$ ’s upper bar in both residual families.Reaching  $(a-6,c)$  would collide with  $V$ . Its intrinsic  $J$ -row is  $d-8$ , so disjointness forces
$$f<d-8.$$
By evenness,
$$f\le d-10.$$
Since  $f\ge4$ , necessarily  $d\ge14$ .This proves all the claimed inequalities:
$$\boxed{
6\le h\le s-4,\qquad
14\le d\le\ell-2,\qquad
4\le f\le d-10.
}$$
SufficiencyUnder these inequalities:
$$\text{last bar row of }J=a+3-d\le a-11,$$

$$\text{far terminal row of }J=a+2-d+f\le a-8.$$
Both the bar and far stem therefore precede every endpoint of  $A$ . Its near column  $w+12$  ends at row  $a+2$ , before  $E$ ’s bar begins in that column at row  $a+3$ .Relative to  $K$ ,
$$c\ge g+2,\qquad w+12<w+14,$$
so both  $J$  columns lie strictly between the cap stems. Its first bar row is at least two rows after  $K$ ’s last bar row:
$$(a+2-d)-(a+2-\ell)=\ell-d\ge2.$$
The length of  $K$ ’s far stem is irrelevant to this separation: that stem stays outside  $J$ ’s column interval.The converse therefore holds for both zero boundaries. In particular, the newly allowed extreme
$$s=w+12,\qquad h=w+8,\qquad c=5$$
causes no failure.6. The common gain  $h-2$  has no extra contacts or double countingPut  $H_J=(d+f)/2$ . The same source counts apply:
$$|M_J|=h+H_J-1,
\qquad
|\mathcal T_J|=h+H_J,
\qquad
|\Sigma_J\cap\cup\mathcal T_J|=H_J+2.$$
Thus
$$q(J)=1-h,\qquad
\Delta S=h-1,\qquad
\Delta N=0.$$
No  $K/J$  endpoint tile is shared:Their bar tile rows are separated. $K$ ’s far tile column is  $\{g-1,g\}$ , while  $J$ ’s begins at  $c-1\ge g+1$ .Their near tile columns are respectively  $\{w+14,w+15\}$  and  $\{w+12,w+13\}$ .Nor is there a  $V/J$  or  $T_0/J$  shared tile. The far stem ends at most at  $a-8$ , before  $V$ ’s first endpoint tile row  $a-7$ .The only shared old endpoint tiles remain
$$T(a-1,w+12),\qquad T(a+1,w+12).$$
Their complete directed accounting is:RowSurviving directionExcluded reverse $a$  $E:(a,w+13)\to J:(a,w+12)$  $J\to E$  targets  $J$ ’s even-indexed outward near support. $a+1$  $J:(a+1,w+12)\to E:(a+1,w+13)$  $E\to J$  targets  $E$ ’s original support  $(3,5)$ . $a+2$  $E:(a+2,w+13)\to J:(a+2,w+12)$  $J\to E$  targets  $J$ ’s original support  $(d,0)$ .The source-relative nature of the exclusion matters in the last row:  $p$  is a support of  $V$ , but it is not a support of  $E$ . Therefore the  $E\to J$  event survives.The upper tile is not full; the lower tile becomes mixed full. Hence
$$\Delta F=1,\qquad \Delta E_v=3,$$
and
$$\boxed{
\Delta\Phi(J\mid A+K)
=(h-1)+2-3=h-2\ge4.
}$$
The pre-existing  $V\to K$  or  $Q\to K$  debit remains in  $A+K$ . It is not an increment when  $J$  is inserted. Likewise, consuming  $p$ ,  $e$ , or  $t$  creates no additional automatic credit.Using the unchanged baseline difference  $-1$ ,
$$\boxed{
\Phi(A+K+J)-\Phi(Q,D,W)=h-3\ge3.
}$$
7. The complete-family exclusions and combined local result followThe  $J$ -parameter region is empty when  $s=6,8$ , or when  $\ell=10,12,14$ , wherever those values occur in the relevant zero regime.Since completeness forces an actual consumer at  $p$ , and every possible consumer must satisfy that region, the claimed noncompletion conclusions follow. Additional originals cannot remove the retained endpoint collisions used in the proof.The local conclusions can therefore be stated exactly as follows:Actual source at  $t$ Established local outcomeRight-pointing north-terminal  $U$ Exact gain  $1$ , repairing the original deficit.Left-pointing north-terminal  $U$ , away from the two boundariesExact gain  $1$ , repairing the original deficit.Left-pointing north-terminal  $U$ , on a zero boundary with no admissible  $J$ No complete feasible extension retaining that prefix.Left-pointing north-terminal  $U$ , on a zero boundary with admissible  $J$ Every complete extension has an actual  $J$  with gain  $h-2\ge4$ ; the prescribed joint inventory is  $h-3\ge3$  above baseline.The specified reflected rotor  $Z$ Exact gain  $1$ , as previously established.The existence of an endpoint-disjoint  $J$  does not establish complete extendibility. Further original-support obligations can remain. The theorem correctly uses these local identities only within the prescribed inventory.8. Formal scope and the remaining global problemThe five added geometric declarations correspond to the claimed written geometry:Sufficiency and necessity of the all-left-cap region.Exclusion of every right-pointing consumer for a general left cap.Sufficiency and necessity of the common left-consumer inequalities on the two zero regimes.Their assumptions match the relevant argument. In particular, the zero-boundary necessity uses the two shared properties
$$s\le w+12,\qquad m\ge\ell-8,$$
rather than silently retaining the earlier restriction  $s\le w+10$ .The catalogue-to-completeness implication and the source/support/tile/event cardinalities remain written arguments. The document accurately states that boundary of formal coverage. The reported execution results are separate from this verdict.The coherent package, including the applied repair and the new extension, is accepted. It completes the stated local north-terminal  $U$  branch. East-terminal and corner roles at  $t$ , consumers outside that branch, and arbitrary signed exterior contributions remain unclassified. The global allocation bound and rectangular-grid equality target remain open.
