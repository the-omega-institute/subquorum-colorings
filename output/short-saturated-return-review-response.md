ACCEPTUnder the stated complete original-source model and the supplied inherited results, I find no blocking error in the general proof, endpoint ownership, joint nonreuse, or exact accounting. The four-row argument works at arbitrary horizontal width because it excludes foreign endpoints on the first interior column; it does not require the entire chamber to be empty.This is a written mathematical acceptance of the conditional theorem. It uses the supplied canonical-gate reconstruction, H transverse-source theorem, defect identity, and intermediate-family loss argument as inherited results. It does not certify the reported finite controls, Lean executions, previous review receipts, complete Vcorner realizability, or unrestricted compensation.1. The chamber boundary and confinement argument are correctThe frames in the new note give the following physical endpoint locations:FeaturePhysical locationX’s two barsColumns  $3,4$ , rows  $3,\ldots,b$ X’s near stemRow  $3$ , columns  $3,\ldots,a+3$ X’s far stemRow  $b$ , columns  $3,\ldots,k+3$ Q’s two barsColumns  $g+2,g+3$ , rows  $b-4,\ldots,b+1$ Q’s near stemRow  $b+1$ , columns  $3,\ldots,g+3$ Q’s far stemRow  $b-4$ , columns  $5,\ldots,g+3$ Thus every lattice point of the boundary of
$$D=[b-4,b+1]\times[4,g+2]$$
is an original X or Q endpoint, including all four corners:The top is X at column  $4$ , followed by Q at columns  $5,\ldots,g+2$ .The bottom and right side are Q-owned.The left side is X-owned through row  $b$ , followed by Q at row  $b+1$ .The strict interior is
$$D^\circ_{\mathbb Z}
=\{b-3,b-2,b-1,b\}\times\{5,\ldots,g+1\}.$$
It has exactly four rows and potentially arbitrarily many columns. Since  $b\ge8$ , X’s near stem at row  $3$  is outside it. Since  $g\ge k+2$ , X’s far-stem columns through  $k+3$  lie strictly before the right boundary  $g+2$ . Consequently the asserted interior endpoint description is correct: X contributes only its far-stem endpoints at row  $b$ , and Q contributes none. [New note, §§1–2.]For any original owner other than X or Q, an endpoint path from the strict interior to its complement must visit the lattice boundary. Unit-edge connectivity and unique original endpoint ownership therefore confine that owner’s entire endpoint set to the strict interior.This argument works owner by owner. It does not assume that another role label denotes a fresh source, nor does it depend on the number or dimensions of the remaining sources.2. The four-row rotor exclusion is valid at arbitrary widthA confined U is impossible: in every permitted orientation it has at least five rows of endpoints. A confined rotor has exactly four rows, so its row range must be precisely
$$b-3,\ b-2,\ b-1,\ b.$$
If such a rotor has an endpoint in column  $5$ , that column must be its leftmost endpoint column. For the two supplied footprints, the leftmost endpoint is the unique tip  $x$ . The resulting calculation is:FootprintRow range relative to  $x$ Forced row of  $x$ Forced bottom endpoint $R_-$  $[-2,1]$  $b-1$  $(b,7)$  $R_+$  $[-1,2]$  $b-2$  $(b,6)$ Both bottom points are original X endpoints, because
$$\{6,7\}\subseteq\{3,\ldots,k+3\}
\qquad(k\ge4).$$
Either rotor would therefore violate unique original endpoint ownership.There is also no omitted quarter-turn orientation of the displayed rotor. The map
$$(r,c)\longmapsto(c-2,1-r)$$
permutes  $R_-$ , and reflection  $(r,c)\mapsto(-r,c)$  takes  $R_-$  to  $R_+$ . Hence the dihedral images of the supplied rotor shape, up to translation, are covered by these two footprints. Restricting charts to those preserving the aligned tiles introduces no additional footprint.The conclusion is exactly:
$$\boxed{\text{No foreign original endpoint lies on the first interior column }5.}$$
It is not a claim that no rotor can occur farther right. The proof needs no such stronger conclusion. Increasing  $g$  does not alter either forced bottom collision. [New note, §2.]3. The transition from “not an endpoint” to “unoccupied” correctly uses ownershipSet
$$v_1=(b-2,5),\qquad v_2=(b-1,5).$$
Neither point is an X or Q endpoint. The preceding argument excludes every other original endpoint owner.If either point were a retained selected support, its occupied west neighbor—an X endpoint—would have to be its sole original anchor. Unique ownership of that anchor forces the support producer to be X itself. This is the required ownership argument; it does not assume that an alternative producer would be a fresh source.The inverse X coordinates are
$$X^{-1}(v_1)=(2,b-4),\qquad
X^{-1}(v_2)=(2,b-3).$$
X has width  $b-2$ , so its original row-two supports occur only in columns
$$0,\qquad (b-2)+1=b-1.$$
Neither displayed point is an X support. Optional selected vertices are excluded by their prohibition on endpoint neighbors.Thus both points remain unoccupied in every complete extension retaining X and Q. Together with the unchanged original endpoints and matching, this gives exactly the inherited irregular  $2P0T$  profile in
$$J=\{b-2,b-1\}\times\{4,5\}.$$
Its contribution is therefore two units to  $2R$ , equivalently one unit to  $R$ , under the supplied defect identity. [New note, §§1–2.]4. Actual-demand reconstruction and joint nonreuse are soundVcorner reconstruction and compatibility with width tenThe physical pair identifies its unique original endpoint owner X. Its location on X’s intrinsic lower bar identifies the adjacent bar end, hence the adjacent upper corner and the opposite Vcorner used by the actual demand.In the displayed chart these are respectively
$$(b,3),\qquad y=(3,3).$$
At the reconstructed  $y$ , the west gate endpoint  $t=(3,2)$  identifies B. Of the two possible positive-producer anchors,
$$(3,1),\qquad(4,2),$$
the second is B-owned. Unique ownership at the remaining anchor, followed by the inherited canonical-gate uniqueness theorem, determines the original positive marked side.This reconstruction does not use  $k=4$ ,  $W=10$ , or any upper bound on the return dimensions. It therefore establishes injectivity for the new demands and compatibility with the previous width-ten assignment. At the minimum X width six, the first lower pairs at opposite bar ends are still distinct: in this chart they occupy rows  $\{4,5\}$  and  $\{6,7\}$ .Taking the Vcorner classes by set union is essential and correct. A demand satisfying both theorems is one demand, and a physical pair carrying multiple certificates is one receipt. [New note, §3; accepted width-ten note, §4.]The H/V exclusion explicitly handles recurring ownersSuppose an established H demand targeted the same physical pair. The inherited H reconstruction makes it use X’s adjacent corner. With
$$\Phi(r,c)=(b+3-c,r),$$
its transverse point satisfies
$$\Phi(p_{\rm old})=\Phi(2,2)=(b+1,2),$$
which is B-owned.The inherited H transverse-source theorem requires
$$C_{\rm old}(r,c)=(c+1,h_{\rm old}+2-r),
\qquad h_{\rm old}\ge4.$$
After transport,
$$\Phi(C_{\rm old}(r,c))
=(b+1-h_{\rm old}+r,c+1).$$
Its intrinsic endpoint  $(h_{\rm old},1)$  maps to  $(b+1,2)$ . Therefore unique original endpoint ownership forces this entire source to be B.That identification is impossible: the same source’s intrinsic bar endpoint  $(0,2)$  would map to
$$(b+1-h_{\rm old},3).$$
But B’s only endpoints in column  $3$  lie on rows  $b+2,b+3$ , while
$$b+1-h_{\rm old}\le b-3.$$
This is a valid whole-source contradiction. It does not assume  $C_{\rm old}\ne B$ ; it first forces equality by ownership and then disproves it geometrically. No bound on  $W,k,g,a$  enters. [New note, §3; accepted width-ten note, §4.]Separation from other receiptsThe remaining nonreuse claims are consistent with the inherited receipt classes:For the same owner, this pair uses the other intrinsic bar row from an upper-bar pair.A different owner cannot supply these endpoints, and the other two tile positions are permanently empty.The exact two-endpoint profile excludes the cited cap and  $m_8$ -triple receipts.The tile contains no original terminal.Every occupied endpoint neighbor that could anchor an external producer at either pair endpoint is X-owned, excluding an external positive canonical-gate receipt there.Thus adding this certificate to the existing physical lower-pair union does not create a second defect contribution.5. The ledger and the claimed exact gain check algebraicallyUsing the supplied inequalities,
$$G=q+c+s+t,\qquad
2N\ge2n_0+G,$$
and
$$2R\ge q+\rho+m_8+c+2p+2u,$$
one obtains
$$\begin{aligned}
2\mu
&=2N+2R-2G\\
&\ge
2n_0+G+q+\rho+m_8+c+2p+2u-2G\\
&=
2(n_0+u+p)+m_8+\rho-s-t.
\end{aligned}$$
The inherited integrality therefore gives precisely the displayed bound
$$\boxed{
\mu\ge n_0+u+p+
\left\lceil\frac{m_8-s-t+\rho}{2}\right\rceil.
}$$
For  $t=0$ , the rearrangement is exact:
$$p+\left\lceil\frac{m_8-s+\rho}{2}\right\rceil
=
(p-s)+\left\lceil\frac{m_8+s+\rho}{2}\right\rceil.$$
Since the joint injection gives  $s\le p$ , all terms in
$$n_0+u+(p-s)+
\left\lceil\frac{m_8+s+\rho}{2}\right\rceil$$
are nonnegative. The automatic covered-class conclusion follows through the inherited  $\sigma\ge\mu$  reduction. No conclusion for unrestricted residual demands follows from this calculation. [New note, §4.]The “EXACTLY” statement about the certificate gain is also correct for the same family, same remaining counts, and same displayed lower bound. Reclassifying eligible demands preserves
$$s_{\rm new}+t_{\rm new}=s_{\rm old}+t_{\rm old},$$
while enlarging the physical union gives
$$p_{\rm new}-p_{\rm old}
=|J_{\rm new}\setminus P_{\rm old}|.$$
Consequently the displayed certified floor increases by exactly that number. A previously counted pair adds zero capacity, regardless of how many new geometric descriptions or certificates it receives. This is an increase in the certified lower bound for a fixed configuration; it does not assert a change in that configuration’s actual  $\mu$ .6. The component-loss application does not duplicate reserveLet  $F_-$  denote the inherited complete intermediate family containing I and exactly the losing added endpoint components. The inherited component argument supplies
$$R(F_-)=R(I)-L.$$
Every new pair counted here already has its certificate in I, with X and Q retained. The permanence theorem therefore applies in  $F_-$ . Applying the protected floor once gives
$$R(F_-)\ge
p+u+\left\lceil\frac{A(I)+m_8(I)+z}{2}\right\rceil,$$
and hence
$$\boxed{
L\le R(I)-p-u-
\left\lceil\frac{A(I)+m_8(I)+z}{2}\right\rceil.
}$$
The new proof supplies the permanence needed for this inherited application. It neither allocates a separate copy of  $R(I)$  or  $p$  to each component nor borrows a certificate first established using an added owner. [New note, §4; accepted width-ten note, §5.]7. The opening intruder is correctly distinguished from a complete-family counterexampleFor the unsaturated return  $Q=U(6,8,4)$ , its far stem begins at column  $7$ . The prospective top boundary therefore has the two missing points in columns  $5,6$ .The displayed D has bars in columns  $5,6$ , on rows
$$b-6,\ldots,b-1,$$
and stems at rows  $b-6,b-1$ , extending through column  $9$ . For even  $b\ge10$ , these endpoints are disjoint from the displayed X and unsaturated Q and include both missing column- $5$  points of J.D extends above the prospective chamber and passes through its missing top boundary. It is therefore not subject to the closed-boundary confinement argument. Moreover, replacing Q by the saturated  $U(6,8,6)$  would make D collide with Q at
$$(b-4,5),\qquad(b-4,6).$$
So this partial intruder does not satisfy—and does not contradict—the new theorem’s hypotheses.The shared-consumer example also checks. For
$$P(r,c)=(b-4-c,11-r),$$
the three intrinsic near-stem endpoints
$$(4,1),\qquad(3,1),\qquad(2,1)$$
map respectively to
$$(b-5,7),\qquad(b-5,8),\qquad(b-5,9).$$
For  $b\ge14$ , its endpoint footprint is disjoint from the displayed X/Q/D stencil. Thus one original owner can consume all three forced points. Distinct forced support positions do not imply distinct consuming owners.Neither D nor this P continuation establishes that every original support can be retained or consumed lawfully in a finite complete family. The note correctly leaves that obligation open. Its partial construction defeats endpoint-only protection in the unsaturated case and defeats the proposed distinct-consumer inference; it does not provide a complete-family counterexample to compensation or to  $\mu\ge0$ . [New note, §5.]No mathematical revision is required for the conditional theorem as stated. The arbitrary-width rotor argument, recurring-owner identifications, joint injection, and single-use accounting all withstand this audit; execution and complete-family realizability remain outside this acceptance.
