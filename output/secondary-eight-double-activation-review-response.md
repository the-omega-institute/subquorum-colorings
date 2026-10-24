REVISE — one exact charge formula needs correctionThe two-activation forcing, both injections, all named old-target exclusions, and the same-ledger gain check out. I found one definite error in the note as written:
$$\boxed{\operatorname{charge}(F)=-1,\quad\text{not }1-\tau.}$$
This is an error in the numerical classification of the intermediate negative source. It does not invalidate the two positive activations or their compensation theorem: F remains negative, and the proof assigns no resource using its charge magnitude.Replacing that formula is sufficient for the result audited below. I found no further blocking gap or missing hypothesis.1. The required charge correctionYour supplied accepted occupied-band dependency, Section 1, assigns isolated charge  $-1$  to the negative chart
$$U_{\mathrm{old}}(r,c)=(V_0-c,\ r+H_0-h),$$
where  $V_0,H_0,h$  are even. Take the same intrinsic source  $U(\tau,h,\xi)$  as the new F.Define the physical isometry
$$J(x,y)=\bigl(b-7+V_0-x,\ H_0+7-y\bigr).$$
Then
$$\begin{aligned}
J(U_{\mathrm{old}}(r,c))
&=\bigl(b-7+V_0-(V_0-c),\ H_0+7-(r+H_0-h)\bigr)\\
&=(b-7+c,\ h+7-r)\\
&=F(r,c).
\end{aligned}$$
Both reflection constants are odd. Therefore J preserves the fixed aligned  $2\times2$  tiles. It transports the whole original source, supports, and matching, so the isolated charge is unchanged. Consequently
$$\operatorname{charge}(F)=-1.$$
This disagrees with  $1-\tau$  for every permitted  $\tau\ge6$ ; for example, at  $\tau=6$ , the stated value would be  $-5$ .The minimal repair in Section 3 is:“F has first offset  $b-7$  odd and isolated charge  $-1$ . No resource follows just from introducing F.”This is a correction to an isolated-source assertion, not a complete-extension counterexample and not a counterexample to the claimed double activation.2. The local forcing is exhaustive and uses only Q and DOwner exclusions and available directionsThe forcing points and their initial blockers are:PointOriginal support and fixed neighborsPossible own-neighbor directions $q=(b-5,7)$ Q support; south  $Q(4,6)$ , west  $D(4,1)$ North/east $n=(b-6,7)$ D support  $(3,2)$ , also E’s lateral support; west  $D(3,1)$ , south E terminal qNorth/east $p=(b-7,7)$ F’s lateral support; south F terminal n, west  $D(2,1)$ , north  $D(1,2)$ East onlyThe required absence statements hold:q is absent from Q and D.n is absent from Q, D, and E.p is absent from Q, D, E, and F.In particular, Q’s minimum endpoint row is  $b-4$ , E’s is  $b-5$ , and F’s is  $b-6$ . D has its bar at rows  $b-9,b-8$ , with legs on columns  $6,m+5$ .Thus the consumers are distinct from the relevant blocker owners before their endpoints are used in collision arguments. This establishes the needed distinctions without assuming that every newly named role has a previously unused owner.All U roles and rotor orientationsFor the exact original U endpoint set, degree-three points are impossible when only north/east own neighbors are available. Straight degree-two points have opposite neighbors and are also impossible. The remaining possibilities are terminals and upper outer-bar corners.At q and n, every eligible north-bearing U role reaches D’s lower bar:At q, the collision is three steps north, at  $D(1,2)=(b-8,7)$ .At n, it is two steps north, at the same point.A north terminal or a corner’s north incident leg continues at least four steps; a northward bar continues at least five. Thus these exclusions cover both outer-corner orientations as well as north terminals.All rotor nontips have original degree three. The remaining tip footprints are exhausted by the north/east chiralities in your text:Consumer pointNorth-tip obstructionReA obstructionReB obstructionq $q+(-2,-1)=D(2,1)$  $q+(1,2)=Q(2,6)$  $q+(1,3)=Q(1,6)$ n $n+(-2,-1)=D(1,1)$  $n+(1,2)$ , on E’s stem $n+(1,1)$ , on E’s stempNorth is already a foreign-owned neighbor $p+(1,2)$ , on F’s stem $p+(1,1)$ , on F’s stemThe E-stem points exist because  $g\ge6$ , and the F-stem points exist because  $h\ge g+2$ . Hence no rotor direction or chirality survives.The remaining consumers are east U terminals.Bar directions, far-leg blockers, and incident lengthsThe far-leg blockers used successively are
$$D(4,m),\qquad D(3,m),\qquad D(2,m).$$
All exist under the stated  $t\ge4$ . There is no hidden requirement that D’s far leg have length eight.For each incident length  $a\in\{g,h,k\}$ , the corresponding horizontal stem must end before column  $m+5$ . This gives
$$a\le m-4.$$
An upward bar crosses D’s lower bar at column  $a+7$ . The crossing occurs at its fourth, third, or second bar position for E, F, or T, respectively. Each position exists at every legal width, and the column lies inside D’s bar by the incident-length bound. Thus all three bars point down.For E,  $g=4$  produces
$$E(1,2)=(b-4,10)=Q(1,6),$$
so  $g\ge6$ .For F, if  $h\le g$ , then
$$F(0,2)=(b-5,h+7)$$
lies on E’s incident row, whose endpoint columns are  $7,\ldots,g+7$ . Since E and F are distinct owners, this is impossible. Therefore
$$h\ge g+2.$$
Likewise,  $k\le h$  would put
$$T(0,2)=(b-6,k+7)$$
on F’s incident row. Hence
$$k\ge h+2.$$
The resulting chain is exactly
$$\boxed{6\le g,\qquad g+2\le h,\qquad h+2\le k,\qquad k\le m-4,}$$
and therefore  $m\ge14$ .None of these arguments uses X, H, B, or an actual positive producer.3. There are two actual positive terminal activationsThe E and T charts preserve the fixed tiling: their intrinsic-column offsets are even and their intrinsic-row reflection constants are odd. Both therefore have isolated charge  $+1$ .Their original terminal supports are:TargetAxial supportLateral supportSupport-owner patternE at q $E(g+1,1)=D(4,1)$  $E(g,0)=n$ , F’s terminalTwo distinct owners D, FT at p $T(k+1,1)=D(2,1)$  $T(k,0)=D(1,2)$ The same owner DBoth supports of each terminal are consumed.The full E tile contains
$$D(3,1),\ D(4,1),\ F(h,1),\ E(g,1),$$
and the full T tile contains
$$D(1,1),\ D(1,2),\ D(2,1),\ T(k,1).$$
These are two positive original terminal occurrences, each counted once. No second credit follows from consuming both supports of one terminal. Neither the corrected negative charge of F nor either full tile supplies an additional pair, cap, or  $m_8$  receipt.4. Both labelled reconstructions are sufficientThe distinction between the local theorem and compensation theorem is maintained correctly.For T, the ordered pair
$$D(2,1),\quad D(1,2)$$
identifies D’s physical incident bar end and directed chart.For E, the use of the whole original D source is essential and sufficient. The axial support is  $D(4,1)$ . Within D’s original graph, the path in one direction reaches the incident lower-bar junction; the other reaches the terminal of that physical leg. Thus the whole source identifies its bar end and actual incident length eight. A degree-two profile alone would not establish this.Either route recovers
$$s=D(8,1)=(b-1,6).$$
Its south neighbor has unique original owner X and actual role
$$X(3,b-2)=(b,6).$$
The whole X source and that physical leg identify its bar end and the opposite actual Vcorner  $(3,3)$ . The inherited B-gate argument then recovers the labelled A side: B owns  $(3,2)$  and  $(4,2)$ , leaving  $(3,1)$  as the positive producer anchor.Therefore each assignment is injective on actual labelled claims.Moreover, an E target from any claim cannot equal a T target from any claim: their ordered terminal supports have two distinct owners versus one owner. This is a comparison of actual terminal resources, not merely of local channel names.Recovering the actual claim also fixes H at  $v=(b-1,5)$ , so different descriptions of j cannot duplicate a claim.5. Every stated old-target exclusion checksThe producer-frame comparisons and self-owner casesAll six supplied producer-frame compositions are correct. Their required witnesses are:New target / old channelFirst witnessSecond witnessE / S $(b-4,4)=X(1,b-6)$  $(b-4,5)=H(j-3,1)$ E / P $(b-8,6)=D(1,1)$  $(b-7,7)$ , T’s terminalE / E companion $(b-8,5)=H(j-7,1)$  $(b-8,6)=D(1,1)$ E / S companion $(b-7,4)=X(1,b-9)$  $(b-7,5)=H(j-6,1)$ T / S $(b-6,4)=X(1,b-8)$  $(b-6,5)=H(j-5,1)$ T / P $(b-10,6)$ , outside D $(b-9,6)=D(0,1)$ Every witness exists under  $j\ge10$ ,  $b\ge j+6\ge16$ , and the supplied old-P width bound  $w_{\rm old}\ge l+4$ .The first five rows force one hypothetical producer to contain endpoints of two distinct actual owners. This excludes every self or recurring-owner identification as well as a new producer.In the final row, the second witness forces the producer to be D. The first witness lies one row above D’s minimum endpoint row  $b-9$ , contradicting that identification. No freshness premise is needed.E versus near-tight  $Q_1$ This exclusion is valid, and it correctly uses more than an original-degree comparison.An explicit chart calculation confirms the physical-leg identification. Let  $h_o$  be the old transverse incident length. The old  $Q_1$  recipient has chart
$$(g+3-r,\ h_o-1-c).$$
Equality with the new E chart forces the producer transport
$$\Gamma(r,c)=(b+h_o-7-c,\ r+4).$$
For the old transverse source
$$C_o(r,c)=(c+1,h_o+2-r),$$
one obtains
$$\Gamma(C_o(r,c))=(b-9+r,c+5)=D(r,c).$$
Thus equality identifies the same original source and the same physical incident leg, forcing
$$h_o=8.$$
Near-tight  $Q_1$  requires  $h_o\ge10$ , so equality is impossible.The independent far leg cannot replace the designated leg while preserving the fixed axial support and whole-source chart.E versus the entire unsaturated D/L unionThe newly supplied complete dependency establishes the needed profiles uniformly over
$$6\le\omega\le V-4.$$
For an old D target, the axial support is
$$C_o(1,\omega+2).$$
Since
$$8\le\omega+2\le V-2,$$
this is an internal lower-bar point of original degree three.For an old L target, the axial support is
$$E_o(0,\omega),$$
whose two original neighbors are perpendicular:
$$E_o(0,\omega-1),\qquad E_o(1,\omega).$$
The new E axial support  $D(4,1)$  has precisely the opposite neighbors
$$D(3,1),\qquad D(5,1).$$
Therefore E cannot equal either old D or old L. This covers all unsaturated widths, including the boundary cases, rather than only the tight-band D subfamily. The comparison uses the original owner’s endpoint graph, so ambient contacts cannot change it.T versus tight targets when  $h_o=8$ The additional argument is necessary and correct. Length mismatch alone would not exclude this case.Ordered support equality identifies the old transverse source with D and forces  $h_o=8$ . The old producer transport is
$$\Gamma(r,c)=(b+h_o-7-c,r+4).$$
The old tight X has incident length  $h_o-4=4$ , and
$$X_o(r,c)=(c+2,r+3).$$
Consequently
$$\Gamma(X_o(r,c))=(b-2-r,c+6).$$
Its two required original endpoints give
$$\Gamma(X_o(3,1))=q,\qquad
\Gamma(X_o(4,1))=n.$$
Those points have distinct actual owners E and F. A single old X owner cannot contain both. This excludes tight reuse even if that old owner coincides with another named source elsewhere.Exhaustiveness of the remaining exclusionsThe remaining comparisons are also valid:Old familyExclusion for new EExclusion for new TRRotor-owned support versus two U-owned supportsSameAll-length E/S companionsProducer collisions aboveDistinct support owners versus the same ownerTightSame support owner versus distinct ownersThe two-owner old-X contradiction aboveNear-tight  $Q_1$ Incident-leg identification  $8\ne h_o\ge10$ Distinct support owners versus the same ownerNear-tight  $Q_2$ Same support owner versus distinct ownersIncident-leg identification  $8\ne h_o\ge10$ Entire unsaturated D/L unionDegree-three/perpendicular versus straight axial profileDistinct support owners versus the same ownerNonmatched upward successorsSame support owner versus distinct ownersAxial original degree three versus twoAll-j secondary-length-six targetsSame support owner versus distinct ownersPhysical incident length eight versus sixThus the proof excludes the entire identified old union, including the already accepted all-j short-secondary targets.6. The exact same-ledger gain is correctWith the old baseline already including the secondary-length-six class, the new residual count  $\kappa$  consists only of eligible actual secondary-length-eight claims.The two-target injection gives
$$A_{\rm activation}\ge q_0+\rho+2\kappa
=q+\rho+\kappa,$$
where
$$q=q_0+\kappa,\qquad t=t_0-\kappa.$$
Using the unchanged inventory,
$$\begin{aligned}
2\mu
&\ge (2N-G)+m_8-s-t+\rho+\kappa+2p+2u\\
&\ge 2n_0+2u+2p+m_8-s-t_0+\rho+2\kappa.
\end{aligned}$$
Therefore
$$\boxed{
\mu\ge n_0+u+p+\kappa+
\left\lceil\frac{m_8-s-t_0+\rho}{2}\right\rceil.
}$$
The integer certificate improves by exactly  $\kappa$  relative to that specified old certificate, without a parity loss. The sufficient threshold is exactly
$$\boxed{
s+t_0\le2n_0+2u+2p+m_8+\rho+2\kappa+1.
}$$
Each demand leaves  $t_0$  once. Its two distinct activation resources account for the two appearances of  $\kappa$  before taking the ceiling. There is no additional  $\kappa$  placed in  $\rho$ , and no change to the physical pair union, total G, or other inventory terms.Correcting F’s charge changes none of this algebra: no numerical contribution from F was used.7. Parent-length-ten coverage and width scopeAt  $j=10$ , the general secondary-escape bound gives
$$6\le\ell\le8,$$
so the actual even secondary length is six or eight. The two accepted branches therefore cover the eligible parent class:Secondary length six has the prior one-activation transfer.Secondary length eight has the new two-activation transfer.This does not give a uniform two-activation or unit-integer-gain statement for all  $j=10$  claims. Nor does parent- $j=10$  coverage create another demand class to count.For the  $j=10,\ell=8$  branch, the parent-width comparison is correct:
$$H(2,d)=(b-9,d+4)$$
lies on D’s upper-bar row. If  $m\ge d$ , it belongs to D’s bar, contradicting the distinct original ownership. Hence
$$m\le d-2,$$
and the local  $m\ge14$  gives  $d\ge16$ .The actual B fence applies to the unchanged E chart. Its owner exclusions remain valid: E is not Q because q is Q’s original support, and E is not B because q has B coordinates  $(8,6)$ , a nonendpoint when  $W\ge12$ . Thus:
$$W\ge12
\Longrightarrow
g\ge8,\quad k\ge12,\quad m\ge16,$$
and, additionally for  $j=10,\ell=8$ ,
$$d\ge18.$$
For  $W\ge14$ ,
$$g\ge10,\quad k\ge14,\quad m\ge18,$$
and, additionally for  $j=10,\ell=8$ ,
$$d\ge20.$$
These d-bounds belong to the length-eight branch and are not asserted for arbitrary parent j or for the entire  $j=10$  union.Exact dispositionRequired revision: replace F’s claimed isolated charge  $1-\tau$  by  $-1$ , or retain only the correctly proved statement that F is negative.With that correction, the local two-source theorem, the two globally unused activation assignments under the full actual-chain hypotheses, and the exact same-ledger consequence are accepted within the stated scope. I found no other blocking gap.This is a written mathematical audit. It does not certify execution, complete realizability, novelty, full Lean formalization, residual coverage beyond the stated classes, full allocation, or unrestricted grid equality.
