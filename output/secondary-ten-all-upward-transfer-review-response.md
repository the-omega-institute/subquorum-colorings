ACCEPTThe all-upward rigidity and compensation extension is mathematically sound under the supplied accepted dependencies and the retained full actual-chain hypotheses. The current right-boundary correction and the  $T=8$  D-only blocker both work. Local rigidity requires no  $H$  premise.I found no missing case requiring a stronger mathematical hypothesis. In particular, the extension does not need  $h=m$ ,  $\omega\ge8$ ,  $w\ge10$ , or the tight-gap parent exclusions. The global compensation argument still uses the stated full actual chain, including  $H$ , canonical-gate reconstruction, the old recipient catalogues, and the identified simultaneous inventory.Two wording corrections should make the opening and closing statements match the proof precisely:The all-upward map extends the old gap2 assignment. Its entire image therefore should not be described as disjoint from a previous union that already contains that gap2 image. The larger-gap restriction avoids that old image. Sections 4–5 already prove and use the correct formulation.The last sentence of Section 3 should remove the stale phrase “satisfying the H premise.” The argument proves the stronger local statement announced in Section 1.Neither correction changes the mathematical argument or accounting.1. The top obstruction covers every U role and both boundariesFrom the supplied U constructor, the original endpoint set is exactly the two-row bar together with its two separated legs. Its possible original endpoint-neighbor roles are:A terminal, with one original endpoint neighbor.A straight leg interior, with two opposite original endpoint neighbors.An outer bar corner, with two perpendicular original endpoint neighbors.A bar interior or leg/bar junction, with three original endpoint neighbors.This classification uses the entire original endpoint set. It does not depend on which neighboring endpoints are matched.At
$$s=(b-9,c),\qquad 7\le c\le m+4,$$
the north D endpoint and the specified south endpoint exclude those directions from the consumer’s own endpoint neighbors. The consumer cannot be D, because D does not contain  $s$ , and cannot be the south owner by hypothesis.Consequently, a U consumer can only place  $s$  at a horizontal terminal or a horizontal straight leg interior. All straight interiors are included.The entire incident horizontal segment, including its two bar columns, must avoid the D wall endpoints
$$(b-9,6)=D(2,1),\qquad
(b-9,m+5)=D(2,m).$$
Since the segment contains  $s$ , it must lie strictly between those walls. This remains true at  $c=7$  and  $c=m+4$ .An upward bar then meets D’s lower bar at row  $b-10$ . A downward bar extends at least five lattice steps from its incident end, since its width is at least six, and therefore reaches E’s incident row  $b-5$ . Its columns lie in  $[7,m+4]$ , which E covers because  $g\ge m$ . Thus every U possibility is excluded at arbitrary legal incident and far-leg lengths.The rotor table also checks directly against the supplied endpoint footprint:Tip formRelative endpointActual D endpointEast A $(-2,1)$  $D(0,c-4)$ East B,  $c\le m+3$  $(-1,2)$  $D(1,c-3)$ East B,  $c=m+4$  $(0,1)$  $D(2,m)$ West B $(-2,-1)$  $D(0,c-6)$ West A,  $c\ge8$  $(-1,-2)$  $D(1,c-7)$ West A,  $c=7$  $(0,-1)$  $D(2,1)$ Every index is legal, including at the minimum  $m=6$ . In particular:The added right-boundary blocker  $D(2,m)$  is an actual far-leg endpoint.The left-boundary blocker  $D(2,1)$  is an actual near-leg endpoint.Neither boundary argument substitutes a support for an endpoint.Every rotor nontip has three original endpoint neighbors, so none can fit the two available horizontal directions.This establishes the enlarged top obstruction on the full interval  $[7,m+4]$ , with no bounded-enumeration premise.2. Original-support closure excludes every  $T\ge8$ Set
$$T=B-h.$$
The accepted bar window gives
$$7\le T\le m+5.$$
Suppose  $T\ge8$ . The point
$$a=(b-6,T-1)$$
is C’s original beyond-terminal support: its C coordinates are  $(h+1,1)$ , and its original anchor is the east endpoint  $(b-6,T)$ .The claimed absences are correct:Q has no endpoint this far north.On row  $b-6$ , D has only its near-stem endpoint at column  $6$ , whereas  $7\le T-1\le m+4$ .At this row, E has only its bar columns  $g+6,g+7$ , strictly to the right of  $a$ .The C coordinates  $(h+1,1)$  are outside C’s endpoint set.Meanwhile,
$$(b-5,T-1)$$
is an E endpoint, because
$$7\le T-1\le m+4\le g+7.$$
Thus the original support has its C anchor and a distinct occupied E neighbor. Retention forces consumption. Optional selections cannot supply an alternative, because they have no endpoint neighbor. Any actual consumer has own endpoint neighbors only north and west.All U possibilities are excludedStraight interiors require opposite directions, and degree-three roles require three directions, so neither can occur.A north terminal contains the point four steps north because its incident leg has length at least four. A north/west outer corner also contains that point:If its bar runs north, its width supplies at least five steps.If its incident leg runs north, its leg supplies at least four steps.In every case, that point is
$$a+(-4,0)=(b-10,T-1)=D(1,T-6).$$
The intrinsic column satisfies  $2\le T-6\le m-1$ , so this is a legal lower-bar D endpoint throughout the range.For a west terminal, its whole incident segment either reaches column  $6$ , meeting D’s near stem, or keeps both bar columns between  $7$  and  $T-1$ . In the latter case, an upward bar meets D’s lower bar and a downward bar meets E’s incident row.This exhausts all U roles. No restriction on an unrelated far leg is used.The current west-rotor boundary table is correctThe five cases are valid:Form and rangeMandatory endpointActual ownerWest A,  $T=8$  $(b-5,6)$  $D(6,1)$ West A,  $T\ge9$  $(b-5,T-2)$ EWest B,  $T=8$  $(b-8,6)$  $D(3,1)$ West B,  $T=9$  $(b-5,6)$  $D(6,1)$ West B,  $T\ge10$  $(b-5,T-3)$ EThe critical correction is
$$T=8,\quad\text{West B}:\qquad
a+(-2,-1)=(b-8,6)=D(3,1).$$
The relative endpoint  $(-2,-1)$  genuinely belongs to that west-B footprint. This is a D near-leg endpoint for every legal  $m$ . H is unnecessary for this exclusion.The north-rotor forcing sites are genuine original supportsFor the exact original rotor, the support  $(1,4)$  has sole original endpoint anchor  $(2,4)$ . The two maps
$$(r,c)\longmapsto(r-4,c-3),\qquad
(r,c)\longmapsto(r-4,3-c)$$
produce precisely the stated RA and RB footprints.They transport that original support/anchor pair to
$$(-3,1)/(-2,1),\qquad
(-3,-1)/(-2,-1),$$
respectively. Therefore the second-stage forcing uses original supports, rather than merely empty sites in endpoint footprints.For RA:If  $T=m+5$ , its endpoint
$$a+(-2,1)=(b-8,m+5)=D(3,m)$$
already gives a collision.Otherwise,
$$s_A=(b-9,T),\qquad 8\le T\le m+4,$$
lies in the enlarged top interval. Its south neighbor is its original rotor anchor, and its north neighbor is a D lower-bar endpoint.For RB:If  $T=8$ , its endpoint  $a+(-2,-1)=D(3,1)$  already gives a collision.Otherwise,
$$s_B=(b-9,T-2),\qquad 7\le T-2\le m+3,$$
lies in the top interval and has the same required north-D/south-anchor structure.The supplying rotor does not contain its own support. D and E are absent at the relevant top site. Hence any consumer has only horizontal available own-neighbor directions and is excluded by Section 2.This also handles an additional original owner that already contains the support: that owner is itself the forbidden consumer. No freshness assumption, and no assumption that all additional sources avoid the support, is needed.The proof covers every integer  $T\ge8$  in the window, including even  $T$ . Therefore
$$T=7,\qquad B=h+7.$$
Since  $h$  is even,  $B$  is odd. Substitution into the bar-window inequalities gives
$$m\le h\le g-2.$$
The accepted phase table then supplies positivity, and the terminal and ordered supports are exactly
$$z=(b-6,7),\qquad
D(5,1)=(b-6,6),\qquad
E(g,1)=(b-5,7).$$
This proves the stated H-free local rigidity. In particular, every even- $B$  candidate is excluded under the local hypotheses.3. Recovery gives one injection across all upward gapsThe recovery argument uses the whole original terminal occurrence, so its axial and lateral directions are fixed.The axial support identifies the actual original D owner at the physical point corresponding to  $D(5,1)$ . That point has:
$$\deg_D=2,\quad\text{opposite own neighbors},\quad
d_\infty(\,\cdot\,,\operatorname{bar}(D))=4.$$
The whole original endpoint set intrinsically identifies D’s bar, by the endpoint-square characterization in the supplied tight-transfer note. The point lies on the physical length- $10$  leg; the length- $4$  leg cannot contain an intrinsic row- $5$  endpoint. Thus the physical incident leg, its bar end and its terminal
$$s=(b-1,6)$$
are fixed.The retained actual-chain reconstruction then fixes X through the endpoint  $(b,6)$ , its opposite actual Vcorner, the actual B gate and the canonical A labelled side. The retained  $C_0$ , B-gate and  $B(4,2)$  hypotheses are the same hypotheses used by the accepted reconstruction. Nothing in this step requires  $h=m$  or  $g=m+2$ .The common lateral support also fixes the actual E owner and its physical terminal. Its physical incident length  $g$  is consequently fixed. D’s whole source fixes  $m$ . Therefore equality of targets fixes the same gap  $g-m$ , as well as the same actual labelled claim.It follows that:The map is injective on the union of all upward gaps.A larger-gap claim cannot share a target with a gap2 claim.The old gap2 assignment is the restriction of this same map.Selecting new claims from the residual after gap2 prevents a second claim credit, while union injectivity independently prevents a second target credit.This is an injection into original terminal occurrences. It does not require an injection into positive owners.4. All four old producer transports remain valid with  $h$ A common recipient terminal occurrence fixes its physical incident leg and its length. Thus the old chart parameter is
$$\ell=h.$$
It is not necessary to retain  $\ell=m$ .For
$$C(r,c)=(b-5-c,h+7-r),$$
the four proposed producer maps compose with the supplied old recipient charts exactly as claimed:Old channelForced producer map  $F(r,c)$ Actual witness identitiesS $(b-8+c,r+4)$  $F(0,1)=X(1,b-9)$ ;  $F(1,1)=H(j-6,1)$ P $(b-3-r,h+9-c)$  $F(0,h+3)=D(8,1)$ ;  $F(1,h+2)=Q(4,6)$ E companion $(b-3-r,c+4)$  $F(0,1)=H(j-2,1)$ ;  $F(0,2)=D(8,1)$ S companion $(b-3-c,r+4)$  $F(0,1)=X(1,b-6)$ ;  $F(1,1)=H(j-3,1)$ For example, in the P case,
$$F_P(c+2,r+2)
=(b-5-c,h+7-r),$$
so the dependence on  $h$  is exactly correct.All mandatory endpoints remain legal:The retained chain supplies  $12\le j\le b-6$ , hence  $b\ge18$ .Consequently  $j-6,j-2,j-3$  are valid H near-leg indices.The X bar columns  $b-9,b-6$  are valid for its width  $b-2$ . $D(8,1)$  belongs to the length- $10$  leg. $Q(4,6)$  is a valid far terminal.The accepted old P bound becomes
$$\operatorname{width}_{\rm old}\ge h+4,$$
which supplies both  $(0,h+3)$  and  $(1,h+2)$ .The physical witness locations do not acquire any dependence on  $h$ .The owner inequalities are also sufficient: $X\ne H$ , because H’s actual intrusion  $(b-1,5)$  is absent from X. $H\ne D$ , because D’s terminal  $s=(b-1,6)$  is absent from H. $D\ne Q$ , by the prescribed distinct original sources.Each hypothetical old producer would therefore have to own two endpoints whose actual original owners differ. Unique original ownership rules this out, including possible identifications of that producer with one of the named owners.These comparisons use H globally, as stated. They introduce no new dimension bound and no fresh-owner assumption.5. The entire supplied current target union is excludedThe new target’s distinguishing ordered profile is:
$$\begin{aligned}
&\text{axial: a U-owned straight degree-two point at bar distance }4,\\
&\text{lateral: a U-owned terminal},\\
&\text{the two support owners are distinct.}
\end{aligned}$$
After the four producer comparisons, the remaining exclusions are valid:Current target familyObstruction to coincidenceRAt least one support is rotor-owned.Tight Vcorner, near-Q2, secondary6, secondary8 TBoth supports have one original owner.Nonmatched upwardIts axial original point has degree three.Unsaturated D/LIts axial point has degree three, or degree two with perpendicular neighbors.Near-Q1, secondary8 ETheir axial original point has bar distance three.CornerIts axial point has degree three; its two supports also have one owner.Downward FIRST, including far4Its axial original point has bar distance five.Downward LASTBoth supports have one original owner.The two emphasized recent profiles are used correctly.For the accepted corner target, the ordered points are
$$D(1,2),\qquad D(2,1).$$
The first has the three original neighbors
$$D(0,2),\ D(1,1),\ D(1,3).$$
The second has two opposite original neighbors,
$$D(1,1),\ D(3,1).$$
Thus the axial degree-three exclusion is correct; it does not require both corner support points to have degree three.For downward FIRST, the axial point is  $D(6,1)$ , whose intrinsic bar distance is
$$6-1=5.$$
Its support owners are distinct, so distinct ownership alone would not separate it from the new target. The document correctly uses the distance- $5$  versus distance- $4$  distinction, including for far4.These distances are invariant under all allowed whole-source lattice isometries and leg-label exchanges. The bar is recovered from the whole original endpoint set as the union of endpoint unit squares. Equality of terminal occurrences would force equality of the physical axial support and its unique original owner; that same point in that same owner cannot have two different intrinsic bar distances.The terminal tile is indeed
$$\{z,D(5,1),D(6,1),E(g,1)\},$$
so the proof identifies the same full tile throughout the extension. It adds no separate cap, pair,  $m_8$ , or additional tile credit.6. The unchanged-inventory arithmetic is correctUse the first document’s incremental baseline:  $t_0$  is the actual residual after the existing gap2, corner and downward assignments, and  $q_0+\rho$  has its identified simultaneous activation witness.For  $0\le\kappa\le t_0$  selected larger-gap claims, put
$$q=q_0+\kappa,\qquad t=t_0-\kappa.$$
Then
$$G=q+c+s+t=q_0+c+s+t_0$$
is unchanged, while the enlarged witness gives
$$A_{\rm activation}\ge q_0+\rho+\kappa.$$
Using the accepted inventories,
$$2N\ge G+2n_0$$
and
$$2R\ge q_0+\rho+\kappa+m_8+c+2p+2u.$$
Therefore
$$\begin{aligned}
2\mu
&=2N+2R-2G\\
&\ge 2(n_0+u+p)+m_8-s-t_0+\rho+\kappa.
\end{aligned}$$
Integrality gives exactly
$$\boxed{
\mu\ge n_0+u+p+
\left\lceil\frac{m_8-s-t_0+\rho+\kappa}{2}\right\rceil.
}$$
Writing  $J=m_8-s-t_0+\rho$ , the certificate increment is
$$\left\lceil\frac{J+\kappa}{2}\right\rceil-
\left\lceil\frac J2\right\rceil.$$
Every two added claims give exactly one unit. A single added claim gives one when  $J$  is even and zero when  $J$  is odd, including for negative  $J$ .The sufficient coefficient-one threshold is consequently
$$\boxed{
s+t_0\le
2n_0+2u+2p+m_8+\rho+\kappa+1.
}$$
The  $+1$  is correct.The equivalent unified certificate is also valid with the different baseline explicitly supplied in the far-four note, Section 5: the residual there is taken before any secondary10 assignments. On that baseline,
$$K_{\rm single}
=k_{\rm up,\ all\ gaps}+k_{\rm corner}+k_{\rm far4}$$
replaces the former tight-only upward contribution, and
$$K_{\rm double}=k_{\rm down}.$$
All single claims share one ceiling. Old gap2 claims are included once, either in the incremental old witness or in the unified  $K_{\rm single}$ , according to the chosen baseline. The proof does not require adding them to both.7. Exact wording corrections and scopeFor Section 1, replace the unqualified sentence about avoiding the entire previous union with:The all-upward map extends the old gap2 assignment and avoids every other previously established target family. Its restriction to residual claims of gap at least4 also avoids the old gap2 image, because both restrictions belong to one injective map.For the end of Section 3, use:This proves the local result for every upward gap. Every even- $B$  candidate is impossible under the stated local hypotheses; H is not needed.These changes express what the current proof already establishes.The acceptance is for the written arbitrary-dimension extension, its actual-labelled union injection, its nonreuse against the specifically supplied current target union, and its same-inventory arithmetic. The finite controls and reported Lean runs play no role in this verdict. Complete realizability, the remaining north and higher-secondary branches, unrestricted allocation and rectangular-grid equality remain open as stated. The historical failed review attempt supplies no mathematical verdict.
