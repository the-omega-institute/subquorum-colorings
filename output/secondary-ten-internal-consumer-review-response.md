ACCEPTThe chain construction, the fresh-owner lemma, and the simultaneous zero-gain receipts are valid. I find no blocking ownership, tile-partition, or contact-accounting flaw.One intermediate row bound needs correction. In §2, a preceding body need not end at or above  $a_i-14$ . The uniform bound supplied by  $z_{i-1}\ge24$  is
$$a_{i-1}+10
=a_i-z_{i-1}+16
\le a_i-8.$$
Equality occurs when  $z_{i-1}=24$ . Likewise, a preceding body can reach the first bar row  $a_i-8$  of  $P_i^0$ , so “earlier bodies are above it” should not be used as a strict row-separation argument.This is a nonblocking correction: the weaker row bound already suffices for absence of  $p_i$ , and a stronger, uniform column separation proves disjointness of  $P_i^0$  from every preceding block. No strengthening of the stated parameter hypotheses is needed.1. The recurrences give the required uniform separationFor the legal even parameters, the recurrences preserve  $a_i$  odd and  $s_i$  even. Consequently every
$$x_i=w_i+14+s_i$$
is even.Two particularly useful identities are
$$x_{i+1}=s_i+2,
\qquad
x_i-x_{i+1}=w_i+12\ge24.$$
Also,
$$a_{i+1}-a_i=z_i-6\ge18.$$
After separating the long far stem of  $V_i$ , the remaining body endpoints of  $B_i$  lie in
$$[a_i-6,a_i+10].$$
Every endpoint of the whole  $B_i$ , including its long far stem, has column in
$$[s_i+2,x_i+3].$$
The next body starts at
$$a_{i+1}-6=a_i+z_i-12\ge a_i+12.$$
Thus consecutive bodies have endpoint-row separation at least two, which rules out both adjacency and a shared fixed tile.For  $j\ge i+2$ ,
$$\max\operatorname{col}(B_j)\le s_i-19
< s_i+2\le\min\operatorname{col}(B_i).$$
For example, at  $j=i+2$ ,
$$\max\operatorname{col}(B_{i+2})
=s_{i+1}+5
=s_i-w_{i+1}-7
\le s_i-19,$$
and subsequent maxima decrease further.These estimates are independent of the far-leg lengths. They cover arbitrarily long, nonuniform chains.2. The internal consumer is the same full originalFor  $i\ge1$ , write  $k=w_{i-1}+10$ . Applying the canonical leg exchange
$$(r,c)\longmapsto(r,k+1-c)$$
to the chart of  $V_{i-1}$  gives
$$(r,c)\longmapsto
(a_{i-1}-6+r,\ s_{i-1}+1+c).$$
The recurrences give
$$a_{i-1}-6=a_i-z_{i-1},
\qquad
s_{i-1}+1=w_i+13+s_i.$$
Hence this is exactly
$$(r,c)\longmapsto
(a_i-z_{i-1}+r,\ w_i+13+s_i+c),$$
with dimensions
$$U(w_{i-1}+10,z_{i-1},8).$$
The near terminal in this chart is
$$(a_i,x_i)=e_i.$$
Thus  $V_{i-1}$  is precisely the asserted upper-right U consumer for block  $i$ .This is a full-source relabeling. The even breadth preserves the two bar-matching patterns under reflection, the stem matchings exchange, and the original corner, lateral and axial supports exchange with their prescribed counterparts. Nothing is reconstructed from the surrounding endpoint arrangement.The root  $K$  is the accepted upper-right frame for  $B_0$ , with incident depth  $6$ , far depth  $4$ , and charge  $1-h$ .3. Endpoint disjointness and the chain contact partition are completeThere are three types of interaction to check.Consecutive blocksAll body/body interactions are excluded by the row separation above. The full  $V_i$ , viewed in the next block’s chart, is an upper-right U of arbitrary legal dimensions. The accepted upper-right/north-rotor receipt therefore applies to  $V_i$  against the whole  $B_{i+1}$ , including its own unbounded far stem.It gives endpoint disjointness and exactly one mixed full tile:
$$T_{i+1}=\{a_{i+1}-1,a_{i+1}\}
\times\{x_{i+1},x_{i+1}+1\}.$$
Nonconsecutive blocksTheir column separation excludes endpoint intersections, adjacency and shared fixed tiles. In particular, no tile can involve three distinct blocks: any three block indices contain two nonconsecutive ones.The rootThe root has endpoint columns at least  $x_0$ . Every later block has maximum column at most  $s_0+5$ , whereas
$$x_0=s_0+w_0+14\ge s_0+26.$$
Thus the root has no contact with later blocks. Against  $B_0$ , the accepted upper-right receipt gives exactly  $T_0$ .These facts establish pairwise endpoint disjointness of all  $9n+1$  source occurrences and exhaust the possible cross-block endpoint tiles.The two events in each  $T_i$ Each  $T_i$  contains two upper-U endpoints in column  $x_i$  and two  $R_i$  endpoints in column  $x_i+1$ .At row  $a_i-1$ , both directions are excluded:The rotor endpoint is the upper U’s odd-indexed inward support.The upper-U endpoint is the rotor’s prescribed support.At row  $a_i$ , neither target is an original support of its source. Therefore the surviving events are exactly
$$(a_i,x_i)\longrightarrow(a_i,x_i+1),
\qquad
(a_i,x_i+1)\longrightarrow(a_i,x_i).$$
Each tile contributes
$$2\Delta F-\Delta E=2-2=0.$$
The  $T_i$  are physically distinct, since their row locations differ by at least  $18$ . None was already an internal full tile of a base: its upper-U endpoints belong to the root or to a different base.Thus there are exactly  $n$  new mixed full tiles and  $2n$  new directed events, with no further cross-contact remainder.4. The chain ledger counts each original onceThe accepted local receipts give
$$\Phi(B_i)=b_i-1.$$
The root contributes  $h-1$  once, and the  $n$  cross tiles contribute zero. Hence
$$\boxed{
\Phi(H_0)=\sum_i b_i+h-1-n.
}$$
The internal consumers  $V_0,\ldots,V_{n-2}$  are already included in the base charges. Their use by later blocks does not introduce new original-owner mass.This identifies exactly where the outside-bases hypothesis matters to the packed ledger. Reapplying a local U contribution to  $V_{i-1}$  would count an original already present in  $\Phi(B_{i-1})$ .For  $n>h-1$ , the baseline comparison fails:
$$\Phi(H_0)<\sum_i b_i.$$
At the same time,
$$\Phi(H_0)=\sum_i(w_i+8)+h-1>0.$$
Both conclusions follow uniformly with a fixed root and increasing chain length.5. Completeness forces  $n$  distinct fresh U ownersAbsence of  $p_i$  from the whole chainThe point
$$p_i=(a_i+2,x_i-2)$$
is  $V_i$ ’s original support  $(8,0)$ , and the supplied local charts show that it is absent from  $B_i$ .There is a simple uniform argument for all preceding blocks, avoiding the overstated row bound. For  $j<i$ ,
$$\min\operatorname{col}(B_j)
=s_j+2=x_{j+1}\ge x_i,$$
while  $p_i$  has column  $x_i-2$ . Thus no preceding original contains it.Every later block starts at row at least  $a_i+12$ , well below  $p_i$ . The root has column at least  $x_0$ , while
$$x_i-2<x_0.$$
Therefore  $p_i\notin H_0$ .Its owner must be a north-terminal UThe three asserted foreign endpoint neighbors are correct:DirectionPointOriginal coordinatesWest $(a_i+2,x_i-3)$  $V_i:(8,1)$ East $(a_i+2,x_i-1)$  $E_i:(2,6)$ South $(a_i+3,x_i-2)$  $E_i:(1,5)$ Completeness forces consumption of  $p_i$ . Since its owner is outside  $H_0$ , none of these three endpoints can be an own endpoint neighbor or matching partner. Its unique own-neighbor direction must be north.The two north-tip rotor images both contain
$$p_i+(-2,1)=(a_i,x_i-1),$$
which is  $E_i$ ’s endpoint  $(4,6)$ . Both rotor possibilities are therefore excluded.The two stated north-terminal U frames are exhaustive. They are even translations, by  $(2,-2)$ , of the accepted upper-U frames at  $e_i$ . Consequently their source charge is
$$q(P_i)=1-H_i$$
for every legal breadth and both unbounded leg lengths.Same-color terminals prohibit owner reuseEvery  $p_i$  has odd row and even column, hence the same checkerboard color. The points are distinct because the  $a_i$  increase strictly and the  $x_i$  decrease strictly.A legal U’s terminal coordinate sums differ by
$$(f+H_i)-(d+1)=f-d+H_i-1,$$
which is odd. Its two terminals therefore have opposite checkerboard colors. An integer grid isometry preserves this opposition, even when it exchanges the two color classes globally.If one actual U owned two different  $p_i$ , both points would have to be its leg terminals, because both sites have only their north own-neighbor direction available. That is impossible for two sites of the same checkerboard color.Thus the  $P_i$  are  $n$  distinct originals outside  $H_0$ , and
$$\boxed{M=\sum_i(H_i-1)\ge5n.}$$
The exact extension identity against the full  $H_0$  then follows:
$$\Phi(H_0\cup P)
=\sum_i b_i+h-1-n+M
+2|F_{\rm new}|-|E_{\rm new}|.$$
The new sets must include all  $P/P$  interactions as stated. No sign conclusion follows from the mass bound alone.6. The simultaneous repair sources are endpoint-disjointFor  $P_i^0$ , the endpoint geometry is particularly useful in physical coordinates:Bar rows:  $a_i-8,a_i-7$ .Bar columns:  $s_i+1,\ldots,x_i-2$ .Near stem: column  $x_i-2$ , rows  $a_i-6,\ldots,a_i+2$ .Far stem: column  $s_i+1$ , rows  $a_i-6,\ldots,a_i-4$ .Its terminal  $(10,1)$  is exactly  $p_i$ .Separation from other blocks and repairsFor every preceding block  $B_j$ ,  $j<i$ ,
$$\min\operatorname{col}(B_j)\ge x_i,
\qquad
\max\operatorname{col}(P_i^0)=x_i-2.$$
This excludes both endpoint intersections and shared fixed tiles. It is the appropriate replacement for the claim that all preceding bodies lie strictly above  $P_i^0$ .Every later block starts at row at least  $a_i+12$ , whereas  $P_i^0$  ends at  $a_i+2$ .Also,
$$\min\operatorname{row}(P_{i+1}^0)
=a_i+z_i-14\ge a_i+10,$$
while  $P_i^0$  ends at  $a_i+2$ . Hence different repair originals have no shared endpoint tile or adjacency.The root is separated in columns:
$$\min\operatorname{col}(K)=x_0
\ge x_i,
\qquad
\max\operatorname{col}(P_i^0)=x_i-2.$$
Disjointness within the associated blockThe bar lies above every  $B_i$  endpoint. Its near stem lies in column  $x_i-2$ , while the relevant old endpoint columns are  $x_i-3$  for V and  $x_i-1$  for E. Its far stem is in column  $s_i+1$ , left of every  $B_i$  endpoint.The near stem ends before the E and C bars reach that column. Thus there are no endpoint collisions.The adjacent V columns require the fixed tile phase: $s_i+1$  and  $s_i+2$  belong to different fixed tile columns. $x_i-3$  and  $x_i-2$  likewise belong to different fixed tile columns.These adjacent endpoint bands therefore create no additional intratile event. This distinction is used correctly in the receipt.7. The full-tile and event computation gives exactly zero gainPut
$$k_i=w_i+10.$$
The repair breadth is  $k_i+2$ , so its original charge is
$$q(P_i^0)=1-(k_i+2)=-(k_i+1)=-(w_i+11).$$
The V-bar bandThe shared tile row is
$$\{a_i-7,a_i-6\}.$$
The columns  $s_i+2,\ldots,s_i+w_i+11$  form exactly  $k_i/2$  aligned pairs.Each tile contains two P bar endpoints and two V bar endpoints. All four directed events survive:For a V source endpoint, the P target has intrinsic V row  $-1$ , so it is not a V support.For a P source endpoint, the V target has intrinsic P row  $2$ , in an interior non-stem column. At that row it is not a P support.Thus this band has
$$\Delta F=\frac{k_i}{2},\qquad
\Delta E=2k_i,$$
and signed contribution  $-k_i$ .The E near-stem contactThe tile at rows  $\{a_i-1,a_i\}$ , columns  $\{x_i-2,x_i-1\}$ , has three endpoints. The next tile, at rows  $\{a_i+1,a_i+2\}$ , has the asserted  $2+2$  pattern.The surviving directions can be checked row by row:RowSurviving direction $a_i$  $E_i\to P_i^0$  $a_i+1$  $P_i^0\to E_i$  $a_i+2$  $E_i\to P_i^0$ The opposite directions are excluded by the original lateral supports. In particular, the P near-stem indices are  $8,9,10$ , while the corresponding E far-stem indices are  $4,3,2$ ; their prescribed parity-dependent supports give precisely the three events listed in the note.Therefore this contact contributes
$$(\Delta F,\Delta E)=(1,3),
\qquad
2\Delta F-\Delta E=-1.$$
Exhaustiveness and simultaneous summationWithin  $B_i$ , these are the only new intratile contacts. The P bar can meet old endpoints only in the top V band. In the near-stem tile column, the only old endpoints in the reached rows are E’s far-stem endpoints. The far stem lies in the tile column immediately left of all old endpoints.The separation estimates exclude contacts with other blocks, the root and other repairs. The new tiles for different  $i$  are physically distinct, and none is an old chain tile  $T_j$ .Consequently,
$$\begin{aligned}
\Delta\Phi(P_i^0\mid H_0)
&=(k_i+1)+2\left(\frac{k_i}{2}+1\right)-(2k_i+3)\\
&=0.
\end{aligned}$$
The same receipt remains valid after the other repair originals are inserted, because their contact sets are disjoint. Hence
$$\boxed{\Phi(H_1)=\Phi(H_0).}$$
This is a simultaneous full-source construction. It does not rely on independently computed gains that cease to be valid when combined.8. The remaining incompleteness certificate is validFor
$$q_i=(a_i-3,s_i+1),$$
the P coordinates are
$$(5,w_i+12).$$
This is precisely its far axial support, since the far leg has length  $4$ .The point is absent from its own repair, from  $B_i$ , and from the rest of  $H_1$  by the preceding column and subsequent row separations. It has the two retained endpoint neighbors
$$(a_i-4,s_i+1)\in P_i^0,
\qquad
(a_i-3,s_i+2)\in V_i.$$
Their intrinsic coordinates are respectively
$$P_i^0:(4,w_i+12),
\qquad
V_i:(3,w_i+10).$$
Both are valid endpoints for all the stated parameters.Thus  $q_i$  remains an unconsumed original support with at least two occupied neighbors. This proves  $H_1$  incomplete. It establishes neither complete extendibility nor nonextendibility.9. Scope of the conclusionsThe note establishes three separate facts:Endpoint-only internal borrowing can fail the sum-of-baselines comparison. The dependency graph is a path and the signed cross-contact remainder is zero, yet the excess is  $h-1-n$ .Any complete extension must supply  $n$  distinct fresh negative U owners. This is a conditional complete-family statement, with owner nonreuse proved by terminal color.Fresh negative source mass need not give positive net repair in an endpoint-disjoint partial inventory. The displayed simultaneous repairs spend their entire charge on their exact contact debit.The example shows why the packed theorem’s owner-additivity step cannot be extended merely from endpoint disjointness and acyclicity: a selected  $V_{i-1}$  is already counted in its base. It does not exhibit a complete-family counterexample to an unrestricted compensation statement. The fresh-owner assertion remains conditional on a complete extension existing, and the displayed  $P_i^0$  need not occur in such an extension.The absolute value
$$\Phi(H_1)=\Phi(H_0)=\sum_i(w_i+8)+h-1$$
is positive. Subsequent forced consumers require a new joint contact ledger; neither their effect nor a bound on  $\Phi(G)$  follows from these partial inventories.The reported finite controls and Lean verification are separate from this verdict. I have not certified their execution. With the corrected row estimate and the column-separation justification above, the ordinary mathematical conclusions and exact receipts are accepted.
