A — ACCEPTThe repaired gate argument is now correct. It establishes own-endpoint degree one at the specified gate, without making the false general assertion that every original tile singleton is a terminal. Explicitly allowing upper-corner singletons elsewhere resolves that issue completely.I accept the repaired short note’s substantive results under the established inputs. The new obstruction in the all-length note further sharpens those results: the old S4 branch was listed as a necessary possibility, without a converse or a complete realization claim. Proving that this branch never occurs in a complete family is therefore consistent with the earlier theorem. Its conditional unmarked-owner statement remains true, but its contribution to an actual complete-family count is zero.B — ACCEPTI find the all-length continuation correct within the stated complete-source model. In particular:The four U roles exhaust the possibilities at the forced point, and the rotor exclusions remain valid for arbitrary  $b\ge6$ .The dimension restrictions are necessary conditions, with the disjunctions used correctly.The all-length activation assignment is injective and disjoint from the established S/P/R assignments, including the large- $g$  S/P case.The new two-source S4 obstruction uses an actual mandatory original support and proves nonextendability by arbitrary allowed U/rotor additions.The residual inequality retaining the actual  $s$  is correct and uses each lower pair once.No mathematical repair is required. There is one optional precision concerning how much the rounded bound improves when  $p>s$ , discussed below.1. The four-role classification is exhaustiveThe existing terminal/transverse argument supplies the stated distinct owners  $B,C$ , and forces an endpoint at  $y=(3,3)$ . At that point, north belongs to  $C$  and west belongs to  $B$ . Thus the new owner’s own-endpoint neighbors can only be east and south.The U possibilities are exactly:Own-endpoint role at  $y$ Remaining possibilityDegree oneEast terminal or south terminalStraight internal leg pointExcluded: requires opposite neighborsInternal bar point or lower bar junctionExcluded: requires three neighborsUpper outer bar cornerTwo orientations: H and VcornerThe distinction between the two corner orientations is necessary. The short proof excluded Vcorner using  $b=6$ ; that exclusion does not survive at arbitrary  $b$ .For a rotor, central points have three own-endpoint neighbors. A tip with its own neighbor east or south has the four reflection types already identified. Their blockers
$$C(2,4),\quad C(2,5),\quad B(5,2),\quad B(4,2)$$
exist for every permitted  $h\ge4$  and  $b\ge6$ . Consequently no rotor role reappears when  $b$  increases.The phase labels also check. E and S have the even translations and odd reflection constants needed to preserve the canonical positive phase. H and Vcorner have the stated negative phases. No arbitrary translation that changes the fixed tile partition is being used to identify positive and negative roles.2. The necessary bounds and disjunctions are correctThe physical locations of the four candidates make the relevant collisions explicit:RoleIncident path or bar relevant to the boundsERow-three path through columns  $3,\ldots,g+3$ ; bar columns  $g+2,g+3$ , rows  $3,\ldots,d+2$ SColumn-three path through rows  $3,\ldots,g+3$ ; bar rows  $g+2,g+3$ , columns  $3,\ldots,d+2$ HBar rows  $3,4$ , columns  $3,\ldots,d+2$ ; incident leg at column  $3$  through row  $a+3$ VcornerBar columns  $3,4$ , rows  $3,\ldots,d+2$ ; incident path in row  $3$  through column  $a+3$ EAvoiding  $C$ ’s bar at column  $h+1$  requires
$$g+3<h+1,$$
hence
$$g\le h-4$$
by evenness.An upward bar would intersect  $C$ ’s row-two stem, so the downward E frame is forced.If  $d\ge b$  and  $g<W$ , then
$$(b+2,g+2)$$
belongs to both E’s bar and  $B$ ’s row- $b+2$  bar. Therefore
$$d\le b-2\quad\text{or}\quad g\ge W.$$
The distinction from the short theorem is correct. At  $b=6$ , the first alternative is impossible because  $d\ge6$ , so  $g\ge W$  follows. For larger  $b$ , that conclusion cannot be extracted from this collision alone.SIf  $g\ge b$ , the incident path meets  $B$ ’s bar at  $(b+2,3)$ . Thus
$$g\le b-2.$$
A left-directed bar intersects  $B$ ’s near leg, so the bar points right.If  $d\ge h$  and  $g<V$ , then
$$(g+2,h+1)$$
belongs to both bars. Indeed, evenness gives  $g\le V-2$ , putting row  $g+2$  within  $C$ ’s bar. Hence
$$d\le h-2\quad\text{or}\quad g\ge V.$$
On the first branch,  $d\le h-2$ , the far-leg restriction is also correct. If  $k>g$ , then evenness gives  $k\ge g+2$ , and the far leg contains
$$(2,d+2).$$
That point belongs to  $C$ ’s row-two stem, a contradiction. Therefore
$$k\le g$$
on that branch.The note correctly avoids using either  $d\le h-2$  or  $k\le g$  throughout the alternative  $g\ge V$ . The activation proof below does not depend on making that invalid extension.H and VcornerFor H: $a\ge b$  produces the collision  $(b+2,3)$  with  $B$ . $d\ge h$  produces the collision  $(3,h+1)$  with  $C$ .Thus
$$a\le b-2,\qquad d\le h-2.$$
For Vcorner: $d\ge b$  produces the collision  $(b+2,3)$  with  $B$ . $a\ge h-2$  produces the collision  $(3,h+1)$  with  $C$ .Thus
$$d\le b-2,\qquad a\le h-4.$$
In particular, Vcorner requires  $b\ge8$ . The note correctly restores this role in the all-length classification.These are all necessary restrictions on actual owners. The argument does not assert that satisfying the table produces a complete family, nor that arbitrary remaining far-leg choices are feasible.3. The new activation assignment remains injective at every lengthFor both E and S,  $y=(3,3)$  is an original positive terminal. Its two original intratile supports are exactly
$$(3,2),\qquad(2,3),$$
occupied by  $B$  and  $C$ , respectively. This is one activated terminal occurrence in the existing ledger.The reconstruction does not use a short-leg assumption: $B$ ’s point  $(3,2)$  is its original terminal. $C$ ’s point  $(2,3)$  is local leg position  $h-1$ . Since  $h\ge4$ , this is an internal straight-leg endpoint, not a terminal or junction.Thus the original roles distinguish the two support positions. The target terminal, its fixed physical tile, and those roles determine the normalized frame and identify  $t$ .At  $t$ , one external producer-anchor candidate,  $(4,2)$ , belongs to  $B$ . The positive producer must therefore own  $(3,1)$ . Unique endpoint ownership and canonical-gate uniqueness determine the original marked side.This proves injectivity across arbitrary lengths and also prevents an E claim and an S claim from sharing one target: a shared target would reconstruct the same original claim.4. The joint S/P/R exclusion works, including large  $g$ The two old S-channel frames remain independent of the new incident length. For an old singleton target, the target terminal is the old gate; its own endpoint neighbor occupies one external position, forcing the old producer’s anchor into the other. Partition preservation gives the two frames in the table.For the old P channel, normalize the positive recipient as  $U(d,g,k)$ , with the target terminal at  $(g,1)$ . The relevant old producer frame in recipient coordinates is
$$F(r,c)=(c-2,r-2).$$
Composing it with the actual E and S frames gives
$$(r,c)\mapsto(r,g+5-c)$$
and
$$(r,c)\mapsto(g+5-c,r),$$
respectively.The four collision images are therefore:New role / old channelOld original endpointImage in the new chartE / S $(1,5)$  $(0,1)$ S / S $(0,4)$  $(0,1)$ E / P $(0,1)$  $(0,g+4)$ S / P $(1,g+2)$  $(3,1)$ The first two old endpoints exist at every permitted width. For E/P,
$$g+4\le h\le w-4,$$
so the collision is on  $A$ ’s original top bar.The large- $g$  S/P endpoint existsThis is the most important new dimension check, and it is valid.Let  $w_{\rm old}$  be the hypothetical old P producer’s width. Its original endpoint
$$(3,w_{\rm old})$$
exists because its far leg has length at least four. Under  $F$ , this endpoint becomes
$$F(3,w_{\rm old})=(w_{\rm old}-2,1).$$
If  $g\ge w_{\rm old}-2$ , that image lies on the recipient’s original incident leg. This would be a different-owner endpoint collision. The producer and recipient are necessarily distinct: their gate is an original support of the former and an endpoint of the latter.Therefore
$$g<w_{\rm old}-2.$$
Since both quantities are even,
$$\boxed{g\le w_{\rm old}-4.}$$
It follows that  $(1,g+2)$  is indeed an old producer bar endpoint, even for arbitrarily large  $g$ . Its image  $(3,1)$  is an endpoint of  $A$ .This proof uses neither  $d\le h-2$  nor  $k\le g$  from the new S classification. Thus it remains valid in the alternative  $g\ge V$  branch.Self-producer cases are excluded without circularityThe first, second, and fourth hypothetical producer frames have original bar endpoints in column zero, while  $A$  has no endpoint there.In the E/P case, every hypothetical producer endpoint has column at most  $g+4<w$ , whereas  $A$  contains  $(0,w)$ .Hence the hypothetical old producer cannot be  $A$ . All four overlaps are genuine different-owner contradictions.The bound  $g\le w_{\rm old}-4$  above did not assume this conclusion: it used distinctness of the old producer and its recipient. There is therefore no circular self-owner exclusion.R targetsUnder the established R assignment, an intratile support of the target is occupied by the preceding original rotor. Both intratile supports of every new target are occupied by the original U owners  $B,C$ .Because the terminal’s original support set and its physical tile are fixed, equality with an R target would assign a second original owner to one of those points. This excludes all R overlaps, independently of dimensions or terminal direction.Consequently,
$$\boxed{q_0+q_T\le A_{\rm activation}}$$
is a valid joint injection into the existing activation pool.5. The new two-source S4 obstruction is correctThis is a genuine strengthening of the earlier enclosure argument. It uses a mandatory original support, not merely the absence of room for another endpoint.Reduction to the two prescribed ownersIf the south companion has  $g=4$ , the alternative  $g\ge V$  is impossible because  $V\ge6$ . Hence
$$d\le h-2,\qquad 4\le k\le g=4.$$
The companion is therefore exactly
$$D=U(d,4,4),\qquad D(r,c)=(7-r,c+2).$$
Consider
$$\mathcal R=[2,6]\times[3,d+2].$$
Its boundary is occupied by the two original owners:The top lies in  $C$ ’s row-two incident stem.The bottom is D’s row-six bar.The side boundaries at columns  $3,d+2$  are D’s legs.Neither owner has an interior endpoint: $C$ ’s incident stem lies on row  $2$ .Its bar columns  $h+1,h+2$  lie beyond the right boundary because  $d\le h-2$ .Its far leg lies on row  $V+1\ge7$ .D’s bars are on rows  $6,7$ , and its legs are the side boundaries.The three-row interior consequently admits no foreign complete endpoint graph, by the connected-source enclosure argument.The original support  $x$  is present for every permitted parameter choiceSet
$$x=(3,d+1).$$
Its inverse coordinates in  $C$  are
$$(r,c)=(h-d+1,2).$$
The local row is odd, and
$$d\le h-2\Longrightarrow h-d+1\ge3,$$
while
$$d\ge6\Longrightarrow h-d+1\le h-5.$$
Thus  $x$  is exactly one of  $C$ ’s original inner supports along its incident leg. There is no boundary or minimum-length exception.Its original anchor is
$$C(h-d+1,1)=(2,d+1).$$
D’s far terminal is
$$(3,d+2).$$
These are two distinct fixed occupied neighbors of  $x$ . The mandatory support therefore cannot remain selected and must be consumed by an endpoint.But  $x$  is strictly inside  $\mathcal R$ , since
$$2<3<6,\qquad 3<d+1<d+2.$$
It is not an endpoint of either prescribed owner, and no foreign complete owner can fit inside the enclosure. This is the contradiction.There is no same-owner escape:  $C$  and D have different original endpoint data, and in particular D’s endpoint  $(3,3)$  is an original support position of  $C$ , not one of its endpoints.The proof uses only  $C$  and D. Neither  $A$  nor  $B$  is needed.ConsequencesThe resulting conclusions are valid:
$$\text{Actual S companion}\Longrightarrow g\ge6,$$
and, since  $g\le b-2$ ,
$$\text{Actual S companion}\Longrightarrow b\ge8.$$
At  $b=6$ , S is therefore impossible. Vcorner is already impossible from  $d\le b-2$  and  $d\ge6$ . The complete-family companion possibilities at that length sharpen to E or H.The old S4 unmarked-owner implication is now vacuous on complete families. It cannot provide a realized positive  $n_0$  contribution. The note correctly says so, while leaving larger- $g$  south companions unresolved as existence questions.6. The retained- $s$  residual bound is correctThe refined classes remain disjoint: $q_0$  covers positive/rotor gate consumers. $q_T$  covers negative-singleton consumers with positive terminal companions, now at every length. $c$  covers selected full-bar cap claims. $s$  covers the earlier  $b=6$  negative H claims assigned to protected lower pairs. $t$  is the remaining class.In particular, old short positive-companion claims are included in  $q_T$ ; they are not added again. Longer H and Vcorner claims do not receive the old short enclosure payment merely because they appear in the new classification.The general  $n_0$  may count independently certified distinct unmarked positive owners. The impossible S4 role contributes none.Using
$$G=q+c+s+t,$$
the reserve inequality gives
$$\begin{aligned}
2\mu
&\ge 2N+A_{\rm activation}+m8+c+2p+2u-2G\\
&=(2N-G)+(A_{\rm activation}-q)
  +m8+2p+2u-s-t\\
&\ge 2n_0+2u+2p+m8-s-t.
\end{aligned}$$
The two discarded quantities are controlled separately:
$$2N-G\ge2n_0,\qquad A_{\rm activation}-q\ge0.$$
This is all within one complete family and does not reuse reserve from another component or configuration.Integrality then gives
$$\boxed{\mu\ge n_0+u+p+
\left\lceil\frac{m8-s-t}{2}\right\rceil.}$$
The direct threshold, including  $+1$ The displayed integer lower bound is nonnegative exactly when
$$\boxed{s+t\le2n_0+2u+2p+m8+1.}$$
At equality, the lower bound on  $2\mu$  is  $-1$ . Since  $2\mu$  is even, it must be at least zero. The  $+1$  is justified; a  $+2$  would not follow from this inequality.Eliminating  $s$  recovers the weaker boundFrom  $s\le p$ ,
$$\begin{aligned}
\mu
&\ge n_0+u+p+
\left\lceil\frac{m8-p-t}{2}\right\rceil\\
&=n_0+u+
\left\lceil\frac{p+m8-t}{2}\right\rceil.
\end{aligned}$$
This gives exactly the earlier convenient threshold
$$t\le2n_0+2u+p+m8+1.$$
The accounting is sound: the actual  $2p$  capacity enters once, and the actual  $s$  claims are charged once. No additional  $s$ -pool is introduced.Optional precision about “sharper”Let
$$\delta=p-s\ge0.$$
Retaining  $s$  improves the lower bound on  $2\mu$  by exactly  $\delta$ , and improves the permitted threshold for  $t$  by exactly  $\delta$ .For a fixed set of counts, the rounded lower bounds on  $\mu$  need not differ strictly whenever  $\delta>0$ . In fact, the stronger bound can be written as
$$n_0+u+
\left\lceil\frac{p+m8-t+\delta}{2}\right\rceil.$$
When  $\delta=1$ , it can tie the weaker rounded bound, depending on parity.The note’s claim that it retains unused capacity is correct. It should simply not be strengthened to a claim of a strictly larger rounded value for every  $p>s$ .Scope of acceptanceThe new note proves an all-length transfer for positive terminal companions and a genuine two-source exclusion of S4. It also gives the stated stronger conditional residual criterion.It does not prove that any particular remaining E/S parameter pattern has a complete realization, pay all long H or Vcorner endings, establish a terminating allocation procedure, or prove universal coverage. The note keeps those limits explicit.This acceptance concerns the written mathematics. It does not certify the reported finite searches, checker counts, Lean declarations, compilation results, or axiom reports.
