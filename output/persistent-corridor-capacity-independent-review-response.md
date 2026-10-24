VERDICT: REVISEThere is one definite ownership error in Section 4 of the corridor note. It has a local repair and does not require changing the compensation inequality or the residual-coverage bound.Under the established inputs you specify, I find the new corridor geometry, lower enclosure, capacity nonreuse, single-family compensation argument, and I/J/K construction mathematically sound. The later residual deduction is also correct in the integral reserve setting. The note should explicitly recall that integrality when applying ceilings and the  $+1$  threshold.I found no complete-source counterexample to the stated, conditional geometric theorem. The supplied  $J\to K$  construction is a valid counterexample to the stronger, expressly disclaimed rule that every lower strip persists.1. Definite repair: the gate in Section 4 has the wrong owner-roleThe sentence“The gate is then B’s original support (3,2).”is false under the coordinates in (2). In fact,
$$B^{-1}(3,2)=(1,1),$$
so  $(3,2)$  is an original lower-bar corner endpoint of  $B$ . It is the positive producer’s original canonical gate support, now consumed by  $B$ .Replace the relevant passage with:The unique two-endpoint owner of the cap identifies  $B$ . Its first internal leg pair fixes the incident leg and the corresponding bar end, hence the consumed canonical gate point  $(3,2)$ . This point is an original endpoint of  $B$ . Of its two possible external original anchor positions,  $(4,2)$  already belongs to  $B$ , so the positive producer must own  $(3,1)$ . Unique endpoint ownership and canonical-gate uniqueness therefore identify the marked positive side.This preserves the intended injection. It also agrees with your later exclusion table, which correctly identifies  $(3,2)$  as a  $B$ -owned endpoint.There is no need to alter the cap definition, the strip count, or any displayed bound because of this correction.2. Corridor geometry: the exhaustion argument worksLeftmost descent applies to arbitrary complete sourcesFix a corridor endpoint  $x=(4,c)$ , and choose it leftmost. The fixed north and south neighbors belong to  $B$  and  $D$ . The point  $x$  itself cannot belong to either of those owners, by their prescribed endpoint sets.If  $c>3$ , its west neighbor is not an endpoint. Thus its only possible neighbor belonging to its own original endpoint graph is east.The required source-role exhaustion is complete:Source roleNumber of adjacent endpoints of the same original ownerU upper outer bar corner2U lower bar corner or internal bar point3U nonterminal leg point2U terminal1Rotor central point3Rotor tip1Consequently, such an  $x$  must be an east-directed U terminal or rotor tip.For the U terminal, the outward endcap support is part of the original source definition. For the rotor, the same outward endcap conclusion is consistent with—and can be checked directly from—the displayed endpoint catalogue. For example, at the canonical west tip  $(3,1)$ , the candidate lateral point  $(2,1)$  already neighbors both  $(3,1)$  and the central endpoint  $(2,2)$ . It cannot be an original selected support of occupied degree one. The outward point  $(3,0)$  is therefore one of the tip’s mandatory supports.In either case, the mandatory west endcap lies in the corridor. Its fixed north and south endpoint neighbors prevent it from remaining selected. It must therefore be consumed by an endpoint, contradicting the leftmost choice.This is a genuine predecessor argument; it does not assume that the foreign source has a particular width, leg length, or orientation.The two rotor placements at  $z_0$  are exhaustiveAt  $z_0=(4,3)$ , the north and west neighbors belong to  $B$ , and the south neighbor belongs to  $D$ . The foreign owner again has only an eastward own-endpoint neighbor.The canonical rotor endpoint set has quarter-turn symmetry. After fixing a tip and its inward direction, its possible endpoint footprints reduce to the two reflection types listed in the note:
$$(r,c)\mapsto(r+1,c+2),\qquad
(r,c)\mapsto(7-r,c+2).$$
They collide with  $B$  at  $(3,4)$  and  $(3,5)$ , respectively. Both points are in  $B$ ’s bar for every allowed width. Thus no rotor case remains.The U bounds and orientation are correctFor a U terminal at  $z_0$ , let  $h$  be its incident leg length. Its incident stem occupies
$$\{(4,c):3\le c\le h+3\}.$$
Avoiding  $B$ ’s far leg at  $(4,d+1)$  gives
$$h+3<d+1.$$
Since  $h,d$  are even,
$$h\le d-4.$$
A north-directed bar would have its two bar columns at  $h+2,h+3$ , crossing  $B$ ’s row-three bar. The preceding bound puts both columns within that bar. Hence the bar must point south.Avoiding  $D$ ’s row-five bar then gives  $h>v$ , and evenness gives
$$h\ge v+2.$$
This yields exactly the stated necessary form
$$F(r,c)=(c+3,h+3-r),\qquad v+2\le h\le d-4.$$
Its incident stem covers the whole corridor. Therefore the dichotomy—entirely unoccupied, or entirely filled by this one original U—is justified.The protected-width conclusion follows immediately. In particular, neither the argument nor its corollary asserts that every parameter choice satisfying these necessary inequalities has a complete realization.3. Permanent profiles and the lower enclosure are validCap and upper stripUnder protected width, corridor points are permanently free of endpoints. They are also free of selected supports, since each already has two fixed occupied neighbors.The cap therefore has the asserted final profile
$$\begin{matrix}
B&\varnothing\\
B&D
\end{matrix},$$
and the upper pair tiles have profile
$$\begin{matrix}
\varnothing&\varnothing\\
D&D
\end{matrix}.$$
The distinction between original and final profiles matters here:The cap’s two  $B$  endpoints originally form a regular  $2P1T$  pair.Their original internal support is  $(5,3)$ , now consumed by  $D$ .The resulting physical tile is a mixed  $3P0T$  tile.The two  $B$  endpoints are local leg positions  $2,3$ , so neither is terminal even when the incident leg has minimum length four. The  $D$  endpoint is an upper bar corner, also not a terminal.The upper strip contains exactly
$$\frac v2-1$$
physical pair tiles. Its endpoints are internal upper-bar endpoints, and its empty row contains no original support of  $D$ .The lower enclosure works at minimum leg length fourFor the rectangle
$$[4,8]\times[3,m],\qquad m=\min(d+2,W+1),$$
all boundary positions are indeed occupied by the stipulated original owners.The potentially delicate right boundary is covered in both cases:If  $m=d+2$ ,  $D_0$ ’s far leg supplies rows  $5,6,7$ , and  $E$ ’s bar supplies row  $8$ .If  $m=W+1$ ,  $E$ ’s far leg supplies rows  $5,6,7$ , and  $D_0$ ’s bar supplies row  $4$ .The minimum far-leg length four suffices in each case. Some longer parameter choices can be excluded by endpoint disjointness, but that does not invalidate the conditional enclosure statement.Neither boundary owner has endpoints in the strict interior. A connected foreign endpoint graph meeting that interior cannot leave it without meeting a boundary lattice vertex, which would share an original endpoint.The strict interior has three rows. An unrotated U occupies at least five rows, a rotated U at least six, and a rotor four. Thus no foreign complete endpoint graph fits.The argument excluding selected supports in the lower tiles is also correct. A selected bottom point adjacent to the  $D_0$  bar would have to have that endpoint as its unique original anchor. But  $D_0$  has no original support at such an internal lower-bar position. A support of another owner would have a distinct anchor and therefore occupied degree at least two.Finally, the tile count is
$$\#\{j\ge0:5+2j\le m-1\}
=
\left\lfloor\frac{m-4}{2}\right\rfloor
=
\min\!\left(\frac d2-1,\frac W2-2\right).$$
The asymmetric  $-1$  and  $-2$  terms in (5) are correct.4. Phase preservation and global nonreuse check outThe phase restriction is substantive and is used correctly.For a signed coordinate permutation to preserve the fixed aligned partition, an output coordinate with positive sign needs an even translation, while one with negative sign needs an odd reflection constant. In particular: $r\mapsto7-r$  preserves the row partition; $r\mapsto r+2$  preserves it;reflection between the two upper corners of  $D$  uses
$$c\mapsto v+5-c,$$
whose reflection constant is odd because  $v$  is even.Thus the opposite-corner strip descriptions refer to the same physical strip under an allowed chart. They do not produce a second resource.Caps and stripsAfter the ownership correction in Section 1 of this review, cap reconstruction gives the claimed injection from selected marked-side claims to cap tiles.Each original  $D$  has only two intrinsic upper corners, so
$$z\le 2|\mathrm{Dset}|.$$
Each counted owner contributes at least two upper pairs:
$$\frac{v_D}{2}-1\ge2.$$
Therefore
$$z\le2|\mathrm{Dset}|\le u.$$
The distinct first pairs at opposite corners remain distinct at minimum width six. Their column sets are  $\{4,5\}$  and  $\{v,v+1\}$ .For different owners, sharing a certified pair tile would force the same two physical endpoints to have two original owners. For the same owner, upper and lower strips use different intrinsic bar rows and, in these certified phases, different physical tiles. Caps and pairs cannot coincide because their permanent endpoint counts are three and two.Positive canonical gate tilesThe gate-exclusion table is correct. The two cases requiring an actual positive-source collision, rather than immediate anchor ownership, are valid:Gate  $(4,2)$  with external anchor  $(4,1)$  forces the allowed positive frame  $r\mapsto7-r$ , which meets  $B$  at  $(6,2)$ .Gate  $(5,2)$  with external anchor  $(5,1)$  forces the allowed positive frame  $r\mapsto r+2$ , which meets  $B$  at  $(2,2)$ .Both collisions exist at the minimum permitted dimensions. The remaining cases follow from permanent emptiness or from the external anchor already belonging to the negative owner.Previous  $m8$  receiptsThe disjointness proof uses the actual original profiles and is sufficient:A new cap is mixed, so it is not a single-owner original U triple.Its unique two-endpoint original owner is  $B$ , whose pair is regular.It therefore cannot be an old mixed receipt whose two-endpoint original pair is irregular.Its singleton is not terminal; indeed, no endpoint in any new cap or pair is an original terminal.New pair tiles have two endpoints and cannot be triple receipts.This is physical nonreuse, not merely a distinction between counter names. It supports adding the new cap and pair capacities to the granted activation/ $m8$  reserve floor.5. The single minimizing family gives the stated compensation inequalityLet
$$B_I
=
p+u+
\left\lceil\frac{A(I)+m8(I)+z}{2}\right\rceil .$$
Once the persistent physical floor is established, every complete intermediate extension satisfies
$$R(F)\ge B_I.$$
For the fixed component partition of  $J\setminus I$ , choose
$$F_{\min}
=
I\cup\bigcup_{\delta_j<0}C_j.$$
The granted component-subunion theorem makes this one family complete feasible, and affinity gives
$$R(F_{\min})
=
R(I)+\sum_{\delta_j<0}\delta_j
=
R(I)-L.$$
Applying the floor once yields
$$L\le
R(I)-p-u-
\left\lceil\frac{A(I)+m8(I)+z}{2}\right\rceil .$$
There is no copying of  $R(I)$ , activations,  $m8$  receipts, caps, or strips across different components.For the canonical demand hull, retaining all positive owners and all marked sides of  $J$  makes  $N$  and  $G$  constant on the component cube. Thus condition (8) gives
$$\mu(F)
=
N+R(F)-G
\ge0$$
for every component subextension, including the hull and the full extension.The sentence “including  $H=J$ ” would read more clearly as “including  $H$  and  $J$ , and also the degenerate case  $H=J$ ,” but this is not a mathematical defect.6. The I/J/K construction and all displayed ledgers are consistentThe support accounting can be checked symbolically for the entire parameter ranges, including the minimum values.Mandatory supportsThe key consumption changes are:Original supportsIn  $I$ In  $J$ In  $K$  $A$ ’s inner supports at rows  $3,5$ Consumed by  $B$ SameSame $A$ ’s inner supports at odd rows  $7,\ldots,g+7$ Consumed by  $E$ SameSame $B$ ’s inner supports  $(5,3),(5,d+2)$ RetainedConsumed by  $D$ Same $E$ ’s inner supports at even rows  $8,\ldots,g+4$ RetainedConsumed by  $D$ Same $D$ ’s inner supports at even rows  $8,\ldots,g+4$ —RetainedConsumed by  $C$  $C$ ’s inner supports at even rows  $10,\ldots,g+4$ ——RetainedThe outer supports and endcaps have the consumers stated in the note. The first two lines of (9), belonging to  $A$ , remain selected throughout.All retained supports have their original anchor as their sole occupied neighbor. The narrowest cases still leave the necessary separation: the two inner-support columns in  $J$  are distance three at  $d=6$ , and those in  $K$  are distance three at  $d=8$ .Endpoint feasibility here means retention of at least the original three occupied neighbors. Some endpoints acquire a fourth neighbor; the text does not impose exact degree three on endpoints, only exact degree one on selected supports.Complete physical tile inventoryA reconstruction of all nonempty physical tiles gives:Final physical profile $I$  $J$  $K$  $4P0T$  $3d/2+3$  $3d/2+g+3$  $2d+g+2$  $2P1T$  $2g+8$  $g+8$  $2g+4$  $1P2T$  $2$  $2$  $2$  $2P0T$  $2$  $d-2$  $d-4$  $3P0T$  $0$  $2$  $4$  $0P1T$  $0$  $g-2$  $0$ The ownership subdivisions agree with the proposed reserve ledger:In  $I$ , the two  $2P0T$  tiles are the mutually consumed  $B/E$  terminal-singleton pairs.In  $J$ , the two triples are the mixed caps, and the  $d-2$  irregular pairs are  $D$ ’s two strips.In  $K$ , the four triples consist of the two persistent caps and the two original unfilled triples of  $C$ . The irregular pairs are  $D$ ’s  $d/2-1$  upper pairs and  $C$ ’s  $d/2-3$  lower pairs.Accordingly, the granted reserve identity yields exactly
$$R(I)=2,\qquad R(J)=d-1,\qquad R(K)=d-2.$$
Endpoint and support totalsFor an original U,
$$|P(U(w,a,b))|=2w+a+b-2.$$
Applying this separately to the disjoint owners gives the stated totals:
$$\begin{aligned}
|P(I)|&=6d+4g+34,\\
|P(J)|&=8d+6g+32,\\
|P(K)|&=10d+8g+22.
\end{aligned}$$
The unchanged original matchings therefore have half these sizes.The retained outer supports of  $A$ , including its endcaps, number  $g+12$ . The additional retained supports number  $g$ ,  $g-2$ , and  $g-4$  in  $I,J,K$ , respectively. Hence
$$|T(I)|=2g+12,\qquad
|T(J)|=2g+10,\qquad
|T(K)|=2g+8.$$
Only  $A$  is positive, both of its canonical gates are consumed by  $B$ , and its two terminal tiles remain  $1P2T$ . Thus
$$N=1,\qquad G=2,\qquad A_{\rm activation}=0,$$
and
$$\mu(I)=1,\qquad \mu(J)=d-2,\qquad \mu(K)=d-3.$$
The hull argument also checks:  $B$ ’s support  $(7,2)$  has its own anchor  $(6,2)$  and the additional occupied neighbor  $A(7,1)$ , so it must be consumed. Within  $J$ , its consumer is  $E$ . Since  $I$  is already feasible, the least feasible closure of the stated seed is exactly  $I$ .Lower persistence is correctly separatedAt  $g=4$ , the lower-enclosure template matches  $D,E$  after an allowed even row translation. It gives
$$p=u=d/2-1,$$
and the reserve floor is exact.For  $g\ge6$ , adding  $C$  fills every former lower-strip pair of  $D$ . The upper strip and both caps persist, while
$$R(K)-R(J)=-1.$$
The extra restrictions  $d\ge8,g\ge6$  are exactly what ensure that  $C$  still has allowed width and leg lengths.Thus this is a legal failure of unconditional lower persistence, without being a failure of either the conditional enclosure theorem or allocation in these examples.7. The later residual corollary is algebraically correctPut  $P=p+u$ . The cleanest rearrangement retains the two nonnegative quantities that the proof discards:
$$\begin{aligned}
2\mu
&\ge
2N+A+m8+c+2P-2(q+c+t)\\
&=
(2N-G)+(A-q)+m8-t+2P\\
&\ge m8-t+2P.
\end{aligned}$$
Here
$$2N-G\ge0,\qquad A-q\ge0$$
are separately justified by the stated inputs.Consequently, for integral  $\mu$ ,
$$\boxed{\mu\ge p+u+\left\lceil\frac{m8-t}{2}\right\rceil.}$$
No additional activation charge or negative-source charge has been inserted.The  $+1$  threshold is correctIf
$$t\le2(p+u)+m8+1,$$
then
$$2\mu\ge-1.$$
Since  $2\mu$  is an even integer, this implies  $\mu\ge0$ .The  $+1$  is therefore justified. A  $+2$  would not follow from this bound: it would permit the integer lower bound  $\mu\ge-1$ .The threshold is exactly the condition that the displayed integer lower bound be nonnegative:
$$p+u+\left\lceil\frac{m8-t}{2}\right\rceil\ge0
\quad\Longleftrightarrow\quad
t\le2(p+u)+m8+1.$$
Explicitly recall integralityAt the first ceiling step, add a sentence citing the established reserve definition or its parity consequence:For every complete original family, the exact reserve identity gives  $R\in\mathbb Z$ ; hence  $\mu=N+R-G\in\mathbb Z$ .This is the exact fact required. Integrality of  $2R$  alone would not suffice. The new packet does not reproduce the full earlier reserve identity, so its scattered half-weight terms should not themselves be presented as a proof of this parity property. If integrality is already part of that established input, this is a citation/clarity repair, not a new geometric obligation.Two useful clarificationsFirst,  $u\ge c$  holds whenever the counted strip owners include every selected cap’s owner. The extra condition that every counted owner itself have a selected cap is unnecessary: additional owners only increase  $u$ .Second,  $K$ ’s two original  $C$ -triples do not contradict the stated weaker specialization
$$\mu(K)\ge d/2-1.$$
If they qualify as additional  $m8$  receipts under the earlier assignment, they strengthen the bound. Their permitted receipt shape alone does not establish that they must be counted by the particular  $m8$  statistic.The  $g=4$  specialization for  $J$  is exact, while the taller-chamber bounds are correctly described as weaker.Scope of the verdictAfter correcting the gate ownership sentence and explicitly identifying the integrality input, I would accept both written deductions within the stated complete-source model.That acceptance covers the conditional compensation theorem and the later residual-coverage criterion. It does not establish universal coverage, arbitrary-grid decomposition, unrestricted allocation, or rectangular-grid equality. It also does not certify execution of the cited Python or Lean files, or any of the reported external review receipts.
