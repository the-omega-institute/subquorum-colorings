Verdict: REVISEThe local forcing argument, strict length inequalities, physical signs, two activation counts, and integer-ledger calculation check. In particular, the claimed gain of exactly  $\kappa$ , with no parity loss, and the threshold’s  $+1$  are correct once the joint injection is established.There are two substantive issues in the written statement and its supplied dependency boundary:“Three further distinct U owners” overstates the proved distinctness. The displayed frames leave open  $D=B$ , with  $B$ ’s two legs exchanged. The proof establishes three pairwise distinct consumers, including two additional positive owners; it does not establish seven distinct owners  $A,B,C,X,Q_1,D,Q_2$ .The  $Q_1$ -versus-E/S exclusions require exact old recipient frames that are not stated in the supplied accepted dependency. The table is algebraically correct for the frames identified below. Those frames must be explicitly included in the dependency being used; distinct support ownership and prior injectivity alone do not supply them.There are also two small written corrections: state the boundary-role lemma’s owner-exclusion hypothesis explicitly, and correct the P-row collision notation.These are reasons for REVISE, not a demonstrated counterexample to the two-activation conclusion. The  $D=B$  observation below is a frame coincidence that the proof has not excluded; it is not an assertion that a complete near-tight witness exists.1. The unexcluded  $D=B$  identificationThe theorem begins with distinct prescribed owners  $A,B,C,X$ , then claims “three further distinct U owners.” Taken literally, that asserts that  $D$ , as well as  $Q_1,Q_2$ , is distinct from every prescribed owner.The following allowed parameter identification defeats the written distinctness argument:
$$W=h-2,\qquad e=b,\qquad g=b.$$
Recall that
$$B(r,c)=(b+3-r,c+1).$$
Exchanging its two intrinsic leg names gives
$$B(r,W+1-c)
 = (b+3-r,W+2-c)
 = (b+3-r,h-c)
 = D(r,c).$$
In particular, its far terminal is precisely
$$B(e,W)=(3,h-1)=z.$$
Thus the negative south terminal forced at  $z$  could, at the level of the displayed frames, be the already prescribed  $B$ , viewed from its other leg.This is not merely an agreement at one endpoint. With  $e=b$ , the intrinsic reflection
$$(r,c)\longmapsto(r,W+1-c)$$
exchanges the whole U’s legs and its corresponding supports and anchors. For example, near even-row lateral supports at column  $0$  become far even-row supports at column  $W+1$ , and near odd-row supports at column  $2$  become far odd-row supports at column  $W-1$ . There is no support-placement or sign mismatch that automatically rules out this identification.The new inequalities do not rule it out either. They would simply impose
$$\ell+2\le b=g,\qquad b+2\le j\le V-4.$$
No contradiction with the displayed dimension assumptions follows.What distinctness is actually provedThe proof does establish: $Q_1,D,Q_2$  are pairwise distinct. $Q_1,Q_2$  are distinct from  $A,B,C,X$ . $D$  is distinct from  $A,C,X$ . $D\ne B$  remains unproved.For the potentially less immediate assertion  $Q_1,Q_2\ne B$ , inspect row three. Because  $b\ge6$ ,  $B$ ’s bar is below row three, and its row-three endpoints can only have columns  $2$  and  $W+1$ . The latter is odd. The proposed terminals have even columns  $h-2$  and  $h$ , both at least eight. Hence neither can belong to  $B$ .Minimal repairReplace the opening assertion by, for example:Every complete occurrence forces two additional positive U owners  $Q_1,Q_2$  and a negative U owner  $D$ , in the following frames. The owners  $Q_1,D,Q_2$  are pairwise distinct; no assertion that  $D$  differs from  $B$  is needed.Alternatively, retain “three further distinct” only after adding a genuine completeness argument excluding the identification above.The simpler wording repair preserves the proposed allocation result: the reconstruction and support-owner separation need  $C\ne D$ , not  $B\ne D$ .2. Boundary-role lemma: correct in its applications, but sharpen its hypothesisThe first inference in §2 needs the consumer of  $s$  to be different from both owners occupying its north and west neighbors.As a standalone statement, saying that the north neighbor is C-owned and the west neighbor belongs to a different fixed owner does not itself exclude the consumer from being that west owner.A precise formulation is:Suppose  $s$  is consumed by an endpoint owner different from the owners of its north and west neighbors. Then its own endpoint neighbors can only lie east or south.The applications supply this condition:At  $x$ , the west neighbor belongs to  $X$ , and  $x$  is an original support of  $X$ , not an X endpoint. The fixed C endpoint set also does not contain  $x$ .At  $z$ , after classifying the consumer at  $x$ , every surviving role at  $x$  has its sole own endpoint neighbor south. Therefore it cannot also own its east neighbor  $z$ . Also,  $z$  is an original C support, not a C endpoint.The note already makes the second observation. It should be explicitly connected to the boundary lemma’s hypothesis.Subject to that clarification, the role exhaustion is valid:An interior U leg point has opposite own neighbors.An internal bar point or lower bar junction has degree three.The only U degree-two roles compatible with east/south own neighbors are upper outer bar corners.Rotor non-tip points have degree three.Every surviving U role with an east own neighbor continues far enough to include  $(3,h+1)$ : at least four steps for a terminal or an incident leg from an upper corner, and at least five along the bar. The forbidden C endpoint is only two or three steps east. This excludes those roles uniformly in every allowed width and both independent leg lengths.3. Both rotor steps and the third terminal forcing are correctThe rotor argument uses a complete finite catalogue of local tip orientations, followed by explicit collisions. That is a mathematical case exhaustion, independent of any bounded computational search.East-pointing rotorsAt  $s=(3,c)$ , the stated east-pointing forms contain respectively
$$(2,c+1),\qquad (2,c+2).$$
For  $c=h-2,h-1$ , these are the indicated C near-leg endpoints or the C bar corner. Thus both east-pointing forms are excluded.First rotor step: force  $Q_1$  at  $x$ If  $x$  were an  $R_s^+$  tip, a south-terminal consumer of  $z$  would intersect it at
$$(4,h-1).$$
For  $R_s^-$ , the intersection is
$$(5,h-1).$$
Every allowed south-terminal stem at  $z$  contains both row-four and row-five points in its column, since its incident length is at least four.If the consumer of  $z$  were instead a south-pointing rotor, all four chirality pairs are excluded by the stated overlap table. Its four listed intersections are correct:
$$(1,1),\quad(1,0),\quad(2,1),\quad(1,-1).$$
The possible same-owner escape is also correctly closed: a south-pointing tip at  $x$  cannot own the adjacent eastern point  $z$ .Consequently  $x$  must be a U south terminal.Second rotor step: force  $D$  at  $z$ Once  $Q_1$  owns  $x=(3,v)$ , its incident stem contains the points needed to block both remaining rotor tips at  $z$ :
$$R_s^+\text{ at }z\text{ contains }(5,v),\qquad
R_s^-\text{ at }z\text{ contains }(4,v).$$
Both lie on  $Q_1$ ’s stem for every incident length at least four. Thus  $z$  is also a U south terminal.Third terminal: force  $Q_2$  at  $u$ The support  $u=(3,h)$  has fixed endpoint neighbors north, east and west:
$$C(2,1),\qquad C(1,2),\qquad D(g,1).$$
It cannot remain a retained support with its original anchor as its sole occupied neighbor. Its consumer has only the south direction available for an own endpoint neighbor.The two south rotor forms hit
$$(4,h+1),\qquad(5,h+1),$$
respectively, on C’s bar. Both points exist for every  $V\ge6$ . Therefore this consumer is a U south terminal.This argument remains valid if  $D=B$ .4. The three frames and all dimension inequalities checkFor a south terminal at column
$$c\in\{h-2,h-1,h\},$$
the C endpoint at  $(V+1,c)$  has intrinsic coordinates
$$(h+2-c,V),$$
whose first coordinate is respectively  $4,3,2$ . Therefore it exists using only  $f\ge4$ . No equality between C’s two leg lengths is used.If the new incident length is  $t$ , its stem occupies rows  $3,\ldots,t+3$ . Avoiding that far-leg endpoint gives
$$t+3<V+1.$$
Since  $t,V$  are even,
$$t\le V-4.$$
A rightward bar would contain  $(t+2,h+1)$ , an endpoint of C’s lower bar. Hence each bar points left, giving exactly the displayed  $Q_1,D,Q_2$  frames.Strict growthD’s leftward bar contains
$$(g+2,v).$$
If  $g\le\ell$ , that point belongs to  $Q_1$ ’s incident stem. Thus  $g>\ell$ , and evenness gives
$$g\ge\ell+2.$$
Likewise,  $Q_2$ ’s bar contains
$$(j+2,h-1).$$
If  $j\le g$ , that point belongs to D’s incident stem. Hence
$$j\ge g+2.$$
These comparisons do not use any unrelated far-leg length.The strengthened lower bound for  $\ell$ Let  $\omega,\nu$  be  $Q_1$ ’s width and far-leg length.If  $\omega\le v-4$ , its far column is
$$c_{\rm far}=v+1-\omega,
\qquad 5\le c_{\rm far}\le v-5.$$
This lies on X’s row-three near stem. If  $\nu\ge\ell$ ,  $Q_1$ ’s far leg would contain  $(3,c_{\rm far})$ , producing an endpoint collision. Thus
$$\nu\le\ell-2.$$
Because  $\nu\ge4$ , this gives  $\ell\ge6$ .Otherwise, evenness gives  $\omega\ge v-2$ . The bar reaches column four. If  $\ell\le d$ , its endpoint  $(\ell+2,4)$  lies on X’s vertical bar. Hence
$$\ell\ge d+2\ge8.$$
The two branches are exhaustive. Therefore
$$6\le\ell,\qquad
\ell+2\le g,\qquad
g+2\le j,\qquad
j\le V-4,$$
and consequently
$$V\ge\ell+8\ge14.$$
At  $h=10$ ,  $v=8$ , so the first branch would require  $\omega\le4$ , which is impossible. Therefore
$$V\ge\ell+8\ge d+10.$$
These are valid necessary conditions. They make no assertion of complete realizability for the remaining dimensions.5. Physical signs and the two actual activations checkFor  $Q_1$ , both reflection constants
$$\ell+3,\qquad v+1$$
are odd. The same is true of  $j+3,h+1$  for  $Q_2$ .A reflection  $n\mapsto 2a+1-n$  preserves the aligned pairs  $\{2k,2k+1\}$ . Therefore these maps preserve the fixed physical two-by-two tiles and transport the canonical positive U charge unchanged. The conclusion is independent of the two sources’ widths and far-leg lengths.D’s negative sign can also be tied directly to the granted B phase. Start with
$$B_g(r,c)=(g+3-r,c+1)$$
and apply the physical horizontal reflection
$$(R,C)\longmapsto(R,h+1-C).$$
Its reflection constant is odd, so it preserves physical tiles, and the resulting frame is precisely D’s. Thus D has the granted negative charge.The two terminal tiles are:TargetTile endpointsOriginal terminal supports $Q_1$  at  $x$  $C$  at  $(2,v),(2,v+1)$ ;  $Q_1$  at  $(3,v)$ ;  $D$  at  $(3,v+1)$  $(2,v)$  and  $z$  $Q_2$  at  $u$  $C$  at  $(2,h),(2,h+1),(3,h+1)$ ;  $Q_2$  at  $(3,h)$  $(2,h)$  and  $(3,h+1)$ Each target is one activated original positive terminal occurrence. Both tiles are full. The note correctly claims neither a second activation from the second consumed support nor an additional defect or receipt at either tile.6. Reconstruction and global nonreuseReconstruction of  $Q_2$ , jointly with tight targetsThe accepted tight reconstruction applies in exactly its stated scope. The ordered supports remain
$$C(2,1),\qquad C(1,2).$$
They recover C’s incident bar end, directed frame and terminal  $p$ , and therefore  $t$ , its owner  $B$ , and the sole possible external positive anchor. The granted canonical-gate uniqueness then recovers the original labelled A side.Nothing in this reconstruction uses the identity of the endpoint immediately west of  $u$ . The actual X role and its incident length at the recovered  $y$  distinguish
$$a=h-4\quad\text{from}\quad a=h-6.$$
Thus this is indeed one injection on the union of tight and near-tight claims.Reconstruction of  $Q_1$ The target terminal occurrence determines its outward support from its stem direction. Here that is specifically
$$(2,v)=C(4,1).$$
The actual original C source identifies the leg containing this point, its direction toward the bar, and its incident terminal. Since  $h\ge10$ , this is an interior leg role, not a bar or terminal ambiguity. C’s two legs cannot supply the same physical point.This recovers the same C frame and hence the same  $p,t,B$  and labelled A side. Therefore  $Q_1$  targets inject on the near-tight claims.The distinction between target families also holds:A  $Q_1$  target has two different support owners,  $C,D$ .A  $Q_2$  or tight target has the same C owner at both supports.Unique endpoint ownership separates these families. Again,  $D=B$  causes no problem because  $C\ne B$ .The exact E/S dependency that must be statedThe supplied accepted tight theorem explicitly states the old S and P recipient frames. For E/S companions, it states distinct U support ownership, but does not state the recipient frames.That ownership property alone cannot exclude  $Q_1$ , which also has two distinct U support owners.The new table is correct if the old companion frames, in their producer charts with the target incident leg named near, are
$$T_E(r,c)=(c+2,\ell+3-r),
\qquad
T_{S,\mathrm{comp}}(r,c)=(\ell+3-r,c+2).$$
Indeed, with the proposed producer maps
$$F_E(r,c)=(c,v+3-r),
\qquad
F_{S,\mathrm{comp}}(r,c)=(r,v+3-c),$$
one has
$$F_E\circ T_E
=
F_{S,\mathrm{comp}}\circ T_{S,\mathrm{comp}}
=
Q_1.$$
Required repair: explicitly state these exact old frames as the established dependency being invoked, or derive them from the stated old catalogue. If they are already intended as part of the grant, this is a restatement repair. Under a literal restriction to the properties actually stated in the supplied tight dependency, it is a missing premise for the E/S comparisons.All four proposed producer collisions are otherwise correctConditional on those exact companion frames, the table verifies as follows:Old targetCalculated endpoint imageFixed endpoint hitExclusion of self-ownershipS $(0,1)\mapsto(0,v-1)$ A’s barAll producer endpoint columns are  $\ge v-1>1$ , while A owns column-one endpoints.P $(1,\ell+3)\mapsto(2,v+2)=(2,h)$  $C(2,1)$ All producer endpoint columns are  $\le v+3=h+1$ , while C owns endpoints in column  $h+2$ .E companion $(1,1)\mapsto(1,v+2)=(1,h)$ A’s barAll producer endpoint columns are  $\le h+1<w$ , while A owns column- $w$  endpoints.S companion $(0,1)\mapsto(0,v+2)=(0,h)$ A’s barAll producer endpoint columns are  $\le h<w$ , while A owns column- $w$  endpoints.The P endpoint exists because the granted arbitrary-length bound is
$$w_{\rm old}\ge\ell+4.$$
All A collisions lie on A’s original bar because  $h\le w-4$ . The column bounds used to exclude self-ownership remain valid for arbitrarily long independent far legs.The P-row notation in the new note should therefore be corrected from
$$\boxed{C(2,h)}$$
to
$$\boxed{(2,h)=C(2,1)}.$$
With C interpreted as the declared frame map, these are not interchangeable expressions.Finally, the R exclusion is valid: an R target requires a rotor-owned support, whereas both  $Q_1$  support owners are U owners. The  $Q_2$  exclusions inherit the accepted tight argument without changing its premises.7. Demand partition, exact integer gain and the  $+1$ This portion is correct, conditional on the joint injection above.The definition places the  $\kappa$  near-tight claims inside the previous uncertified remainder. Thus
$$q=q_{\rm old}+\kappa,\qquad
t=t_{\rm old}-\kappa$$
reclassifies the same labelled demands and leaves  $G$  unchanged.The original gate class and actual companion role distinguish them from the established old classes. The uniquely normalized actual incident length distinguishes near-tight from tight:
$$a=h-6\ne h-4.$$
The two-target injection gives the correct stronger count,
$$A_{\rm activation}
\ge q_{\rm old}+2\kappa
=q+\kappa.$$
Starting from the granted simultaneous inventory,
$$G\le2(N-n_0),\qquad
2R\ge A_{\rm activation}+m_8+c+2p+2u,$$
we obtain
$$\begin{aligned}
2\mu
&=2N+2R-2G\\
&\ge 2n_0+A_{\rm activation}+m_8+c+2p+2u-G\\
&\ge 2n_0+2u+2p+m_8-s-t+\kappa\\
&=2n_0+2u+2p+m_8-s-t_{\rm old}+2\kappa.
\end{aligned}$$
Therefore
$$\boxed{
\mu\ge n_0+u+p+\kappa
+\left\lceil\frac{m_8-s-t_{\rm old}}2\right\rceil .
}$$
Relative to the same previous displayed ledger certificate, the integer lower bound increases by exactly  $\kappa$ . This follows from
$$\left\lceil\frac{H+2\kappa}{2}\right\rceil
=
\kappa+\left\lceil\frac H2\right\rceil$$
for every integer  $H$ . There is no parity loss.For the threshold, set
$$M=2n_0+2u+2p+m_8-s-t_{\rm old}+2\kappa.$$
The displayed integer certificate is nonnegative exactly when
$$\left\lceil\frac M2\right\rceil\ge0
\quad\Longleftrightarrow\quad
M\ge-1.$$
Consequently the sufficient condition is precisely
$$\boxed{
s+t_{\rm old}
\le
2n_0+2u+2p+m_8+1+2\kappa.
}$$
The  $+1$  is correct:  $M=-1$  still forces the integer  $\mu$  to be nonnegative. This is a sufficient threshold from this certificate, not a necessary condition for allocation.The bookkeeping also correctly leaves the extra activation in  $A_{\rm activation}-q$ , without spending it again as a cap, pair,  $m_8$  receipt or terminal bonus. The conditional coefficient- $1$  consequence uses only the granted existing implication.Required revision before acceptanceThe smallest sufficient revision is:Remove the assertion that D is an additional owner distinct from B, unless a separate proof excludes  $D=B$ .State explicitly that the boundary-lemma consumer differs from the north and west endpoint owners; retain the existing application-specific checks.State the exact E/S companion recipient frames used in the table, with their established scope.Correct the P collision to  $(2,h)=C(2,1)$ .With the stated companion frames supplied, these repairs preserve the forced positive targets, the simultaneous injection, and the exact  $\kappa$  improvement. This audit does not establish complete witnesses, universal residual coverage, or any code/Lean execution claim.
