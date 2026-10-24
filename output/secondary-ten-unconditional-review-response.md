ACCEPTThe new ordinary proof is correct under the supplied original-source model and the three explicitly accepted dependencies. I find no blocking error in the all-parameter distinct-owner argument, including the arbitrarily long retained  $V$  far leg, the two upper-rotor exclusions, the four directed events per depth-eight  $V$ -tile, or the selection of actual originals.Writing
$$\Phi_0=\Phi(Q,D,W),$$
the proof establishes
$$\forall G\supseteq A\text{ complete and feasible},\quad
\exists I:\quad
A\subseteq I\subseteq G,\qquad
|I\setminus A|\le2,\qquad
\Phi(I)\ge\Phi_0.$$
When the actual owners of  $e$  and  $t$  are distinct, it establishes the stronger conclusion
$$\Phi(I)\ge\Phi_0+1.$$
This acceptance concerns the ordinary mathematical argument and its combination with the stated accepted dependency. It does not certify the finite-control receipts or Lean execution.1. Full-source normalization and original chargesLeg relabeling preserves the actual originalThe required canonical reflection is
$$\sigma_h(r,c)=(r,h+1-c).$$
It carries the complete source data of  $U(h,\ell,f)$  to those of  $U(h,f,\ell)$ .This includes the matching, rather than just the endpoint silhouette:Row-zero pairs with odd left endpoint remain row-zero pairs with odd left endpoint, because  $h$  is even.Row-one pairs with even left endpoint remain row-one pairs with even left endpoint.The two stem matchings are exchanged without changing their row pairings.Bar-corner supports, terminal axial supports, even-indexed outward supports and odd-indexed inward supports are exchanged with their prescribed counterparts.Consequently, normalizing an actual far-leg terminal as a near-leg terminal is a change of intrinsic chart. It does not replace the original, change its matching, or recompute its supports from the surrounding inventory.The rotor normalization is also valid for the full source. The quarter-turn
$$(r,c)\longmapsto(c,5-r)$$
preserves the endpoint set, the four unordered matching pairs and the support set. For example, its support orbits are
$$(0,2)\to(2,5)\to(5,3)\to(3,0)\to(0,2)$$
and
$$(1,1)\to(1,4)\to(4,4)\to(4,1)\to(1,1).$$
Thus fixing a tip and its inward direction leaves the two reflected rotor frames used in the note.The relevant endpoint roles are exhaustiveIn a legal  $U$ :The two leg terminals have one own endpoint neighbor.Nonterminal stem points have two opposite own endpoint neighbors.The two row-zero outer corners have two perpendicular own endpoint neighbors.Every remaining endpoint has three own endpoint neighbors.In the rotor, the four tips have one own endpoint neighbor, and the four other endpoints have three.These facts justify both the east-terminal classification at  $t$  and the later terminal/corner analysis at  $e$ .The charge counts are correctPut  $x=\mathrm{row}-a$ . Since  $a$  is odd, fixed tile rows in these coordinates are
$$\{2j-1,2j\},$$
while fixed column pairs are  $\{2j,2j+1\}$ .For any of the four U frames, let  $H$  be half the sum of its leg lengths. The matching count is
$$|M|=\frac h2+\frac{h-2}{2}+\frac{\text{near}}2+
\frac{\text{far}}2=h+H-1.$$
Direct counting in the fixed phase gives:FrameBar endpoint tilesAll endpoint tilesOriginal supports in those tiles $q$  $J_N$  $h+2$  $h+H$  $H+2$  $1-h$  $J_S$  $h$  $h+H-2$  $H-2$  $1-h$  $K_R$  $h$  $h+H-2$  $H-2$  $1-h$  $K_L$  $h+2$  $h+H$  $H+2$  $1-h$ Each pair of stems adds  $H-2$  tiles beyond the bar tiles. In the  $H+2$  support cases, the counted supports are the two bar-corner supports and the  $H$  even-indexed outward supports. In the  $H-2$  cases, they are exactly the odd-indexed inward supports. The terminal axial supports lie outside the endpoint tiles.Therefore every such U contributes exactly
$$h-1$$
through  $N+S$ . Each of  $R_N,R_S$  has four matching pairs, four endpoint tiles and four original supports in those tiles, so
$$q(R_N)=q(R_S)=0.$$
These are original-owner charges. Consuming an original support does not alter them.2. Distinct owners at  $e,t$ : the east-terminal U branchLet  $J$  be the actual owner of  $t$ , distinct from the actual owner of  $e$ . At  $t$ , the north, west and south neighbors are retained endpoints belonging to other originals:
$$e,\qquad E:(a+1,w+13),\qquad C:(a+2,w+14).$$
The matching partner of  $t$  must therefore lie east. Its own-neighbor set is exactly  $\{\text{east}\}$ .The role classification above consequently gives exactly the two U frames  $J_N,J_S$  and the two rotor frames  $R_N,R_S$ . No corner or nonterminal stem role is omitted.Endpoint-disjointness, including unbounded old  $z$ For either east-terminal U, write its far terminal column as
$$p=w+14+\ell-f.$$
This is even. The far row is a contiguous interval from  $p$  to  $w+14+\ell$ .The relevant retained  $V$  endpoints, in  $x=\mathrm{row}-a$  coordinates, are
$$\begin{aligned}
&x=-6,-5,\qquad B\le c\le w+11,\\
&c=w+11,\qquad -4\le x\le2,\\
&c=B,\qquad -4\le x\le z-6.
\end{aligned}$$
The last interval is the one that must remain unbounded in the second residual.The first possible old endpoint encountered by a far row moving west is:Frame and breadthFar row  $x$ First old endpoint columnRequired even terminal column $J_N,\ h=6,8$  $2-h$  $w+11$  $p\ge w+12$  $J_N,\ h\ge10$  $2-h\le-8$ NoneNo bound $J_S,\ h=6$  $6$  $w+14$ , from  $C$  $p\ge w+16$  $J_S,\ h=8,10$  $8,10$  $11$ , from  $Q$  $p\ge12$  $J_S,\ h\ge12,\ B=2,\ z\ge h+6$  $h$  $2$ , from  $V$  $p\ge4$  $J_S,\ h\ge12$ , otherwise $h$ NoneNo boundThese conditions are exactly the far-leg bounds in the note.They are sufficient as well as necessary. The bars lie farther right than all old endpoints, and the near stems lie in row  $a+1$ , starting at column  $w+14$ , where no old endpoint occurs.The tile boundary for a long old  $V$  also works correctly. Its far terminal row  $z-6$  is even. Thus, when it does not reach the even row  $h$ , it ends at or before  $h-2$ ; it cannot occupy just the preceding row  $h-1$  of the new far-row tile. When it does reach row  $h$ , the bound  $p\ge4$  avoids its entire column- $2$  tile. There is no omitted contact from a long old stem stopping one row short.Exact contacts at the  $t/C$  tileThe tile
$$T_t=\{a+1,a+2\}\times\{w+14,w+15\}$$
contains the two near-stem endpoints of  $J$  and the old  $C$  endpoint  $(a+2,w+14)$ . It has three endpoints.For  $J_N$ , both directions of the vertical  $J_N/C$  contact are excluded by the respective source’s original support set.For  $J_S$ , the  $C\to J_S$  direction is excluded, while
$$J_S:t\longrightarrow C:(a+2,w+14)$$
survives. Thus this tile contributes zero for  $J_N$  and a debit of one for  $J_S$ .The  $h=8$  interaction with  $W$ This is the only additional U/A contact case.At row  $a+7$ , the old  $W$  endpoints are exactly columns  $w+1,\ldots,w+5$ . The new far row is  $a+8$ , with an even left endpoint. Consequently, each reached pair
$$\{w+2,w+3\},\qquad \{w+4,w+5\}$$
produces one mixed full tile and exactly two surviving directed events.More explicitly, in each such pair, both directions at the even column survive, while both directions at the odd column are excluded by original supports. Hence each full tile has net contribution
$$2-2=0.$$
If the interval reaches the additional tile  $\{w,w+1\}$ , that tile has three endpoints. Both directions at column  $w+1$  are excluded by original supports, so it also contributes zero.The disjointness bound  $p\ge12$  places the new row outside every  $Q$  endpoint tile. Thus the contact list is exhaustive, and
$$\Delta\Phi(J_N\mid A)=h-1,\qquad
\Delta\Phi(J_S\mid A)=h-2.$$
Every east-terminal U gives gain at least  $4$ , yielding
$$\Phi(A+J)\ge\Phi_0+3.$$
3. Both upper-rotor exclusions are complete-family argumentsThese exclusions correctly use retained original endpoints and completeness. They do not depend on finite search or on who consumes  $t$ .Exclusion of  $Z_-$ The point
$$p_0=(a,w+12)$$
is the original support  $(6,0)$  of  $V$ . Its west and east neighbors are retained endpoints of  $V$  and  $E$ , and  $Z_-$  supplies its north neighbor.The point  $p_0$  is not an endpoint of those originals. Hence an actual consumer of  $p_0$  cannot use any of these three foreign endpoints as its matching partner. Completeness forces consumption, and the only available own-neighbor direction is south.Every south-terminal U contains  $p_0+(3,0)$ , because the incident leg has length at least four. But
$$p_0+(3,0)=(a+3,w+12)$$
is an endpoint of  $E$ .The two south-terminal rotor frames respectively contain
$$(a+2,w+13),\qquad (a+1,w+13),$$
also endpoints of  $E$ .Thus every possible actual consumer collides with a retained endpoint. Adding further originals cannot repair this obstruction.Exclusion of  $Z_+$ The point
$$q_0=(a-1,w+13)$$
is  $E$ ’s original far axial support. The proposed  $Z_+$  supplies its north and east endpoint neighbors, while  $E$  supplies its south endpoint neighbor.Again, none can be the matching partner of an actual consumer of  $q_0$ . The only possible own-neighbor direction is west.Every west-terminal U contains the second west point, and both west-terminal rotor frames do too:
$$q_0+(0,-2)=(a-1,w+11).$$
This is a retained near-stem endpoint of  $V$ , so every candidate consumer collides with  $V$ .The argument allows the north and east blockers to belong to the same  $Z_+$ . It does not assume fresh or distinct owners for different blocking sites.4. A rotor at  $t$  forces an actual north-terminal U at  $e$ The rotor receipts against  $A$  are correct:
$$\Delta\Phi(R_N\mid A)=0,\qquad
\Delta\Phi(R_S\mid A)=-1.$$
For  $R_N$ , the only A contact is in the three-endpoint  $C$  tile, with no surviving event.For  $R_S$ : $T_t$  becomes mixed full and has two surviving directed events.The next  $C$  tile has three endpoints and one surviving directed event.Together with  $q(R_S)=0$ , this gives
$$2\Delta F-\Delta E_v=2-3=-1.$$
Now let  $K$  be the actual owner of  $e$ . Its west neighbor belongs to  $E$ , and its south neighbor belongs to the rotor at  $t$ . Its possible own-neighbor directions are therefore north and east.For  $R_N$ , the east site itself is already occupied by  $R_N$ , immediately excluding any own east neighbor.For  $R_S$ , the second east site is occupied. Every remaining U role with an own east neighbor contains that second site:An east terminal contains it along its incident leg.A north/east outer corner contains it along either the bar or the incident leg, according to the orientation.A rotor east tip also contains the second east site. Thus these roles are excluded as well.It follows that  $K$  has only its north own neighbor. The two possible north-terminal rotors are exactly  $Z_-,Z_+$ , already excluded. Therefore  $K$  is an actual north-terminal U, with one of the normalized frames  $K_R,K_L$ .Exact disjointness conditions for  $K_L$ Set
$$g=w+15-h.$$
This is odd.Depths  $4$  and  $6$  collide with the retained  $V$ : the left bar includes column  $w+11$ , and at those depths it meets the near stem or bar.For  $g\ge B$ , the far column lies inside the old  $V$  bar’s column interval. Its first possible collision is at row  $a-6$ . Since the far terminal row  $a-d+f$  has the same parity as  $a$ , avoiding this collision requires
$$f-d\le-8.$$
Hence
$$f\le d-8,$$
which, with  $f\ge4$ , forces  $d\ge12$ .For  $g=3,B=4$ , the far column misses  $V$ . Its first old endpoint is  $Q:(a+10,3)$ , giving
$$f-d\le8,\qquad f\le d+8.$$
Depth  $d\ge8$  is sufficient.For  $g\le1$ , the far column lies to the left of every old endpoint, and  $d\ge8$  is sufficient for every legal  $f$ .This proves exactly the stated table. In particular, it remains valid for arbitrarily large old  $z$  and arbitrarily large permitted new  $f$ .The tile assertions also follow from these bounds:In the internal regime, the far stem stops at or above  $a-8$ , before the first old endpoint tile row.At column  $3$ , it stops at or above  $a+8$ , before the  $Q$  tile row containing  $a+10$ ; column  $3$  and  $V$ ’s column  $4$  lie in different fixed tiles.At columns  $g\le1$ , its tiles lie left of every old endpoint tile.For  $K_R$ , the near column ends at  $e$ , its bar lies above the rotor endpoints, and its far column is at least  $w+19$ . Thus its stated unrestricted endpoint-disjointness is correct.5. The depth-eight debit is exactly  $k$ , and width pays all of itThis is the decisive accounting point, and the repaired formula is correct.Suppose  $K=K_L$  and  $d=8$ . Its bar rows are  $a-8,a-7$ , while the old  $V$  bar rows are  $a-6,a-5$ . Their shared tile row is
$$\{a-7,a-6\}.$$
Disjointness forces  $g<B$ . Therefore the  $K_L$  bar covers every aligned pair of columns in
$$B,B+1,\ldots,w+11.$$
There are exactly  $k/2$  such pairs.Four events in each shared  $V$ -tileEach shared tile contains two  $K_L$  endpoints in row  $a-7$  and two  $V$  endpoints in row  $a-6$ . Thus it contributes one new mixed full tile and has two vertical foreign adjacencies.Both directions of both adjacencies survive:The  $K_L$  endpoints are above the intrinsic row-zero bar of  $V$ , and none is an original support of  $V$ .The  $V$  endpoints lie at intrinsic row  $2$  of  $K_L$ , strictly between its stem columns. At this even row, the prescribed lateral supports are outward of the stems, not at these interior points.Consequently,
$$\Delta F=\frac k2,\qquad
\Delta E_v=4\frac k2=2k,$$
and the net contact contribution is
$$2\Delta F-\Delta E_v=k-2k=-k.$$
Counting two events per tile here would be wrong. Unlike the  $J_S/W$  contact, neither direction at either column is removed by an original support.The geometric escape gives the entire required budgetSince
$$g=w+15-h,\qquad B=w+12-k,$$
we have
$$g-B=k+3-h.$$
At depth eight, disjointness requires  $g<B$ . Because  $g$  is odd and  $B$  is even,
$$g\le B-1,$$
so
$$h\ge k+4.$$
Therefore
$$h-1-k\ge3.$$
The charge pays the full debit  $k$ , with at least three remaining. This conclusion is independent of how long the old far leg is.Rotor contacts add no further debitThere is no shared endpoint tile between  $K$  and  $R_S$ .For  $R_N$ , there is exactly one:
$$T_e=\{a-1,a\}\times\{w+14,w+15\}.$$
The two  $K$  near-stem endpoints and the two  $R_N$  endpoints complete this tile. Exactly two directed events survive, so its net contribution is
$$2-2=0.$$
The surviving directions need not be identical for  $K_R$  and  $K_L$ , but their number is exactly two in both cases. Thus no unsupported per-site symmetry is needed.There is also no  $C$  contact: the near stem ends in  $T_e$ , while the first relevant  $C$  endpoint lies in the following tile row. The far-stem boundary checks above exclude the remaining possible A contacts.Combining these facts with the original charge gives the exact formulas
$$\Delta\Phi(K\mid A+R_N)
=
\Delta\Phi(K\mid A+R_S)
=
h-1-k\,\mathbf1_{\{K=K_L,\ d=8\}}.$$
Hence
$$\Delta\Phi(R_N,K\mid A)\ge3,
\qquad
\Delta\Phi(R_S,K\mid A)\ge2.$$
The stated receipt witness is correctFor the first residual, take
$$k=w+8,\qquad z=4,\qquad K_L=U(w+12,8,4).$$
Then  $g=3$ , so the endpoint-disjointness table applies, and
$$\Delta\Phi(K_L\mid A+R_S)
=(w+12)-1-(w+8)=3.$$
Adding the  $R_S$  increment gives
$$\Delta\Phi(R_S,K_L\mid A)=2,
\qquad
\Phi(A+R_S+K_L)=\Phi_0+1.$$
This verifies the partial-inventory receipt and the necessity of the width debit in the exact formula. Complete extendibility is not established by this witness, and the note correctly makes no such claim.6. Actual-original selection and combination with the accepted lemmaThe quantifiers close correctly because the proof selects owners already present in the given complete family.By accepted dependency (i),  $e,t$  are actual endpoints in  $G$ . They are not endpoints of any of the eight prescribed originals. Endpoint disjointness gives each a unique actual owner.Let
$$J=\operatorname{owner}_G(t).$$
If  $J$  also owns  $e$ , accepted dependency (iii) supplies  $I$  consisting of  $A,J$  and at most one additional actual original, with  $\Phi(I)\ge\Phi_0$ .If the owners are distinct and  $J$  is a U, choose  $I=A\cup\{J\}$ .If the owners are distinct and  $J$  is a rotor, let  $K=\operatorname{owner}_G(e)$ . The preceding exclusions prove that this actual  $K$  is one of the allowed north-terminal U originals. Choose  $I=A\cup\{J,K\}$ .There is no step where an arbitrary geometrically admissible frame is substituted for an actual owner. The disjointness conditions are necessary properties of the already selected actual originals.Using accepted dependency (ii),  $\Phi(A)=\Phi_0-1$ , the conclusions are:BranchAdditional actual originalsGain over  $\Phi(A)$ ResultCommon ownerAt most  $2$ At least  $1$ , by the accepted lemma $\Phi(I)\ge\Phi_0$ Distinct, east-terminal U $1$ At least  $4$  $\Phi(I)\ge\Phi_0+3$ Distinct,  $R_N$  and  $K$  $2$ At least  $3$  $\Phi(I)\ge\Phi_0+2$ Distinct,  $R_S$  and  $K$  $2$ At least  $2$  $\Phi(I)\ge\Phi_0+1$ Original supports remain fixed throughout the ledger. Old directed events therefore do not change when a support is consumed, and each new contact is counted against the same prefix. The depth-eight  $V$  tiles and the  $K/R_N$  tile are distinct. No consumed support is introduced as an extra credit.This establishes the claimed nonreuse within one prescribed residual package.7. Lean scope and remaining obligationsThe supplied Lean excerpt contains the fourteen stated theorem declarations. Its mathematical scope is local endpoint/support membership, absence and collision certificates, followed by conditional arithmetic inequalities for the width budget and deficit repair.It does not define the complete-family ownership condition, original matching data,  $q$ ,  $F$ ,  $E_v$ ,  $\Phi$ , or the final subinventory statement. In particular, it does not itself formalize the passage from a forced consumed support to the exhaustive classification of its actual owner. Those steps remain in the ordinary proof, as the note states.I have not executed the source or independently confirmed either receipt’s reported counts or axiom output.No blocking mathematical revision is required. The accepted result is the stated actual-original subinventory theorem. Global package nonreuse, signed exterior control, and any deduction of a global inequality from  $I\subseteq G$  remain outside what this argument proves.
