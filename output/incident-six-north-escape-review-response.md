ACCEPTI find no blocking mathematical issue under the stated complete-source conventions and the supplied accepted chain, reconstruction, and ledger results. The three-source obstruction covers arbitrary legal dimensions, including every straight-leg interior position and all four relevant rotor-tip forms. Its  $b=12$  pair corollary is valid with the actual-chain hypotheses retained. The separate two-source construction has the stated surviving supports and counts for every legal even  $b\ge10$  and independently chosen even  $a\ge4$ .The scope distinctions are also correct: the obstruction excludes an occurrence without creating a reserve; the pair certificate is conditional on an actual marked chain; and the two-source construction supplies neither the A/B/C gates nor an actual  $V_{\mathrm{corner}}$  realization.1. The three-source obstructionAll intervals below are integer intervals. Applying the prescribed frames gives
$$\begin{aligned}
E_X={}&([3,b]\times\{3,4\})
 \cup(\{3\}\times[5,a+3])
 \cup(\{b\}\times[5,k+3]),\\
E_Q={}&([b-4,b+1]\times\{10,11\})
 \cup(\{b+1\}\times[3,9])
 \cup(\{b-4\}\times[7,9]),\\
E_H={}&(\{b-7,b-6\}\times[5,d+4])
 \cup([b-5,b-1]\times\{5\})
 \cup([b-5,b+z-7]\times\{d+4\}).
\end{aligned}$$
These formulas establish the required blockers without restricting  $a,d,z$ .The forced support and its ownerFor
$$p=(b-4,6),$$
the inverse coordinates are:SourceIntrinsic coordinate of  $p$ Original anchor $H$  $(3,2)$  $(b-4,5)$  $Q$  $(5,6)$  $(b-4,7)$ Thus  $p$  is simultaneously H’s near inner support and Q’s far beyond-terminal support, with two distinct immutable occupied anchors.It is not an endpoint of any of the three named sources:For  $X$ , column  $6$  occurs only on its near and far horizontal legs, at rows  $3$  and  $b$ ;  $b-4$  is neither.For  $Q$ , its far leg on row  $b-4$  begins at column  $7$ .For  $H$ , intrinsic  $(3,2)$  is neither a bar point nor a leg endpoint.Consequently, retaining  $p$  as a nonendpoint would violate the sole-occupied-anchor condition. It must be consumed by an endpoint whose original owner  $R$  differs from  $X,Q,H$ .There is no repeated-owner shortcut hidden here. The prescribed sources themselves cannot merely be different presentations of one owner:  $X$  contains  $(3,3)$ , which is outside  $Q$ ;  $H$  contains  $(b-6,6)$ , which is outside  $X$ , and  $(b-6,5)$ , which is outside  $Q$ . If their endpoint sets intersect, the distinct prescribed owners already violate ownership.Once  $R\ne H,Q$  is established, the west and east neighbors of  $p$  cannot be R-owned endpoints. Hence R’s own endpoint neighbors at  $p$  must be contained in the north/south directions. This is exactly the restriction needed for the catalogue argument.Every U position is coveredThe U endpoint types have the following own endpoint-neighbor profiles:Intrinsic positionOwn endpoint neighborsCompatible at  $p$ ?Noncorner bar point, including a leg–bar junctionThreeNoOuter bar cornerTwo perpendicular directionsNoStrict leg interiorTwo opposite directionsYes, only on a vertical legLeg terminalOne directionYes, only on a vertical legThus  $p$  must lie on a vertical leg at some intrinsic depth  $t\ge2$ . Nothing restricts  $t$  to the terminal depth. This explicitly includes all straight-leg interior anchors.If the horizontal bar is above  $p$ , its outer row is
$$S=(b-4)-t\le b-6.$$
The column- $6$  endpoint interval from that bar to  $p$  therefore contains
$$(b-6,6)\in E_H.$$
This is a collision regardless of the direction in which the bar extends, either leg length, or whether  $p$  is interior or terminal.If the bar is below  $p$ , its outer row is
$$T=(b-4)+t\ge b-2.$$
If  $T\ge b$ , the column- $6$  leg contains  $(b,6)\in E_X$ . That endpoint exists for both  $k=4$  and  $k=6$ .Otherwise  $T\in\{b-2,b-1\}$ .A bar extending left contains  $(T,5)$ , an endpoint of H’s incident leg.A bar extending right, of width at least  $6$ , contains  $(T,10)$ , an endpoint of Q’s bar.This exhausts the possible bar locations. In particular, the proof permits both parities of  $t$ , as required for arbitrary interior positions.All four north/south rotor-tip forms are coveredFor the supplied canonical rotor, the four central endpoints each have three own endpoint neighbors, while the other four are tips. Only tips whose sole own endpoint neighbor lies north or south can occur at  $p$ .For a tip with its own neighbor north, translate the canonical tip  $(4,3)$  to the origin. One relative footprint is
$$\begin{split}
\{&(0,0),(-1,0),(-1,-1),(-1,-2),\\
  &(-2,-1),(-2,0),(-2,1),(-3,-1)\}.
\end{split}$$
The other chirality reflects the second coordinate. Both contain the entire three-point row
$$\{-2\}\times\{-1,0,1\},$$
and hence both contain
$$p+(-2,-1)=(b-6,5)\in E_H.$$
For a tip with its own neighbor south, translate the canonical tip  $(1,2)$  to the origin. One footprint is
$$\begin{split}
\{&(0,0),(1,0),(1,1),(1,2),\\
  &(2,-1),(2,0),(2,1),(3,1)\}.
\end{split}$$
Its reflected form again contains the same three-point transverse row. Both therefore contain
$$p+(2,-1)=(b-2,5)\in E_H.$$
The two chiralities for each of the two allowed neighbor directions account for all four forms. Every one collides with H.Conclusion for §§1–2: the forced endpoint at  $p$  has no possible U or rotor owner. The theorem is valid at arbitrary legal dimensions and with unrestricted additional sources. It neither assumes fresh owners for unrelated forced supports nor assigns two consumers to  $p$ .2. The strengthened escape bound and permanent  $b=12$  pairThe substitution  $j=6$  is exactThe accepted actual-chain escape theorem supplies
$$H(r,c)=(b-1-j+r,c+4),
\qquad 6\le j\le b-6,$$
with even  $j$ .At  $j=6$ , this is precisely
$$H(r,c)=(b-7+r,c+4),$$
the new three-source theorem’s frame. No additional hypothesis is needed to apply that theorem.It follows that
$$8\le j\le b-6,
\qquad b\ge14.$$
These are necessary conditions for an actual lower-corner intrusion; no sufficiency or realizability is asserted.For  $b=12$ , the previous interval allowed only  $j=6$ , so it now allows nothing. Therefore  $v=(b-1,5)$  is not an endpoint. The accepted implication
$$u\text{ is an endpoint}\Longrightarrow v\text{ is an endpoint}$$
then excludes  $u=(b-2,5)$ .Endpoint absence is correctly strengthened to occupied-site absenceThe note supplies the necessary additional argument; it does not simply identify “not an endpoint” with “empty.”Each of  $u,v$  has a west neighbor belonging to X’s inner bar. Therefore:Neither site can be an optional selection.If either were a retained original support, its sole occupied neighbor would have to be that western X endpoint.Its support owner would consequently own that anchor.Unique original endpoint ownership would identify the support owner with  $X$ .But the inverse X coordinates are
$$X^{-1}(u)=(2,b-4),\qquad
X^{-1}(v)=(2,b-3).$$
Neither belongs to X’s original support list. In particular, at intrinsic depth  $2$ , the alternating leg supports are exterior supports, not these interior bar-adjacent positions.Thus both sites are absent from the occupied set.The two western endpoints have intrinsic coordinates
$$(1,b-4),\qquad(1,b-3).$$
Because  $b$  is even, these are a consecutive pair beginning at an even column, exactly as required by the original matching on intrinsic row  $1$ . Hence
$$J=\{b-2,b-1\}\times\{4,5\}$$
is the claimed permanent original irregular  $2P0T$  pair.This validates the  $b=12,k=6$  extension of the previously accepted  $b=8,10$  certificate.3. Repeated owners, joint nonreuse, and the ledgerLabelled-demand reconstruction retains its required gateThe extension uses the same physical X pair and the same actual B gate as the accepted reconstruction. Changing the allowed value of  $b$  to include  $12$  does not change the reconstruction mechanism.The stated competing producer-frame anchor is indeed B-owned:
$$B(b-1,1)=(4,2).$$
Thus the actual B premise excludes that alternative. Equality of numerical leg lengths cannot exchange the physical bar end selected by  $J$ , the original endpoint owner, or the labelled producer side.The application therefore preserves the accepted uniqueness argument rather than introducing a symmetry-based identification of distinct demands.The old-H exclusion handles the repeated-owner case correctlyThe supplied change of frame satisfies
$$\Phi(2,2)=(b+1,2).$$
This point is B’s intrinsic  $(2,1)$ , so it is a B endpoint.An old-H transverse source requiring that endpoint must therefore be B itself. This is the correct treatment of a potentially repeated owner; declaring the point a collision with a presumed new source would not suffice.The same transverse source also requires
$$(b+1-h_{\mathrm{old}},3),
\qquad h_{\mathrm{old}}\ge4.$$
In B’s frame, physical column  $3$  corresponds to intrinsic column  $2$ . Since  $W\ge12$ , that column is not either leg. Its B endpoints occur only on the two bar rows:
$$b+2,\qquad b+3.$$
But
$$b+1-h_{\mathrm{old}}\le b-3.$$
The required second endpoint is therefore not a B endpoint, giving the contradiction.This argument excludes old-H reuse even when the first endpoint forces identification with B.The remaining separation from upper pairs and other inventory types is an application of the supplied accepted physical-pair reconstruction result. Its dependencies are unchanged by the  $b=12$  extension.One physical-pair union gives the stated algebraThe accounting correctly uses one union  $\mathcal P$  of physical pairs:
$$p=|\mathcal P|,\qquad s\le p.$$
Repeated certificates do not create additional elements of  $\mathcal P$ , and repeated labels for an already identified demand do not create additional demands.The ledger remains
$$\mu\ge n_0+u_{\mathrm{upper}}+p+
\left\lceil\frac{m_8-s-t_{\mathrm{residual}}+\rho}{2}\right\rceil.$$
When  $t_{\mathrm{residual}}=0$ , the displayed rearrangement is exact:
$$p+\left\lceil\frac{m_8-s+\rho}{2}\right\rceil
=
(p-s)+\left\lceil\frac{m_8+s+\rho}{2}\right\rceil.$$
It follows by moving the integer  $s$  through the ceiling. The concluding nonnegativity uses  $p-s\ge0$  and the nonnegative inventory quantities of the accepted ledger.The “exact gain” sentence is valid with its qualification that the other quantities are fixed. More operationally, if a newly certified existing demand moves from residual to covered status, then
$$\Delta s=1,\qquad \Delta t_{\mathrm{residual}}=-1,$$
so the ceiling term is unchanged. The gain is then exactly  $\Delta p$ : one for a newly added physical pair, zero for a pair already in  $\mathcal P_{\mathrm{old}}$ . This does not assert an exact gain under arbitrary simultaneous changes to all inventory quantities.The cross-component floor is also correctly applied once in the intermediate family retaining the supporting owners. Keeping the actual A/B/C/X/Q premises, particularly C’s endpoint  $(2,5)$ , is essential and is explicitly required.Empty classes contribute no resourceThe note correctly distinguishes exclusion from compensation:The  $j=6$  theorem rules out an occurrence. It awards no activation or reserve.The accepted rotor-cavity theorem makes the actual  $k=4$  class empty. Such an occurrence contributes neither a realized demand nor a physical pair to the inventory.The  $b=12,k=6$  statement certifies a pair if an actual marked-chain demand occurs. It does not establish that any such demand is realized, or that  $p\ge1$  merely because the conditional certificate exists.There is no impossible occurrence being counted as reserve.4. The arbitrary-size two-source constructionSet  $k=6$ . Then
$$\begin{aligned}
E_X={}&([3,b]\times\{3,4\})
 \cup(\{3\}\times[5,a+3])
 \cup(\{b\}\times[5,9]),\\
E_Q={}&([b-4,b+1]\times\{10,11\})
 \cup(\{b+1\}\times[3,9])
 \cup(\{b-4\}\times[7,9]).
\end{aligned}$$
Endpoint disjointness genuinely permits independent  $a$ For every even  $b\ge10$ :X’s arbitrarily long near leg lies on row  $3$ , while Q’s first endpoint row is  $b-4\ge6$ .X’s vertical bar occupies columns  $3,4$ , whereas Q’s vertical bar occupies columns  $10,11$ .On row  $b$ , X ends at column  $9$ , before Q’s bar.Q’s long near leg is on row  $b+1$ , below all X endpoints.Q’s far leg is on row  $b-4$ , in columns  $7,\ldots,11$ , away from X’s bar.Thus no upper bound or coupling condition on  $a$  is hidden in endpoint disjointness.The consumed supports are exactly those statedTransforming the original support formulas and intersecting with the opposite endpoint set gives:Original ownerSupports consumed by the other source $X$  $(b+1,3),(b+1,5),(b+1,7),(b+1,9),(b,10)$  $Q$  $(b,4),(b,6),(b,8)$ The remaining supports are exactly the following. The table also records their original anchors and cardinalities.OwnerSurviving supportsSole occupied neighborCount $X$  $(2,c)$ ,  $c=3,5,\ldots,a+3$  $(3,c)$  $a/2+1$  $X$  $(3,a+4)$  $(3,a+3)$  $1$  $X$  $(4,c)$ ,  $c=6,8,\ldots,a+2$  $(3,c)$  $a/2-1$  $X$  $(b-1,6),(b-1,8)$  $(b,6),(b,8)$ , respectively $2$  $Q$  $(b+2,c)$ ,  $c=3,5,7,9,11$  $(b+1,c)$  $5$  $Q$  $(b-5,c)$ ,  $c=7,9,11$  $(b-4,c)$  $3$  $Q$  $(b+1,2)$  $(b+1,3)$  $1$  $Q$  $(b-4,6)$  $(b-4,7)$  $1$  $Q$  $(b-3,8)$  $(b-4,8)$  $1$ There are no further endpoint consumptions or coincident surviving supports.The sole-neighbor checks include the delicate boundaryThe listed anchors are indeed the only occupied neighbors.Upper region. Increasing  $a$  extends X’s occupied set only on rows  $2,3,4$ . Q’s first endpoint row is at least  $6$ . The only potentially adjacent support rows occur at  $b=10$ : X’s row- $4$  supports have even columns, and Q’s row- $5$  supports have odd columns  $7,9,11$ . Hence they have no vertical adjacency. Their diagonal proximity does not create a lattice edge.For larger legal  $b$ , the separation increases. The smallest  $a=4$  is also included: the row- $4$  support list consists of the single point  $(4,6)$ , and the same parity check applies.Lower X supports. The points  $(b-1,6),(b-1,8)$  have their anchors immediately below. Q’s bar is in columns  $10,11$ , and Q’s exceptional support  $(b-3,8)$  is two rows away. Neither point acquires another neighbor.Exceptional Q supports.At  $(b+1,2)$ , the other possible neighbors  $(b,2),(b+2,2),(b+1,1)$  are empty.At  $(b-4,6)$ , the west neighbor is empty; the north neighbor lies in even column  $6$  on Q’s odd-column upper-support row; and the south neighbor is empty.At  $(b-3,8)$ , only the endpoint immediately above is occupied.Within each remaining horizontal support list, consecutive supports are two columns apart. The endpoint intervals and these parity checks exclude all other support–support and support–endpoint adjacencies.This establishes the full sole-occupied-anchor condition, rather than merely checking that each support still touches its intended anchor.Completeness, connectivity, matching, and countsEvery originally occupied point remains occupied: consuming a support changes its status but does not remove it. Therefore every endpoint retains the stipulated at-least-three occupied neighbors from its original source.Endpoint disjointness preserves the disjoint original matching edges. Both sources are connected, and they are adjacent between X’s row  $b$  and Q’s row  $b+1$ , including at columns  $3,\ldots,9$ .The counts are exact:
$$|E_X|=2(b-2)+(a-1)+(6-1)=2b+a,$$

$$|E_Q|=2\cdot6+(8-1)+(4-1)=22.$$
Thus
$$\boxed{|E|=2b+a+22},
\qquad
\boxed{|M|=b+\frac a2+11}.$$
The surviving X support count is
$$\left(\frac a2+1\right)+1+
\left(\frac a2-1\right)+2=a+3,$$
and Q contributes  $5+3+1+1+1=11$ . Therefore
$$\boxed{|S|=a+14}.$$
All occupied coordinates lie between rows  $2$  and  $b+2$ , with maximum column  $\max(a+4,11)$ . The claimed even rectangle
$$(b+4)\times\max(a+6,12)$$
therefore contains the construction for every allowed parameter choice.5. Scope controlThe two-source construction uses only X and Q, their original endpoints, their original matchings, and their unconsumed original supports. No A/B/C gate, positive producer, or actual marked  $V_{\mathrm{corner}}$  condition enters its proof.The relation between the two main results is particularly clear at
$$p=(b-4,6).$$
In the two-source family, its west neighbor  $(b-4,5)$  is empty, so  $p$  is a valid retained Q support with its sole anchor to the east. Adding the specified  $j=6$  source H occupies that west neighbor, forces consumption of  $p$ , and triggers the impossible-consumer argument. Thus the two-source realization and three-source noncompletion are fully compatible.The construction rules out an exclusion based on the X/Q frames alone. It does not realize the actual chain, refute compensation, settle allocation, or improve the universal  $5/6$  bound.One nonblocking wording clarification would help: replace “The  $j\ge8$  north escape … still require[s] work” with “The realizability of  $j\ge8$  north escapes … remains open.” The necessary bound is proved; completion of those longer escapes remains unresolved.Final verdict: ACCEPT. No blocking issue found in the new advance or its stated conditional corollary.
