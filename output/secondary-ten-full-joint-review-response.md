ACCEPTThe joint-consumer compensation lemma is correct under the stated original-source model. The four U frames exhaust the same-owner possibilities, the leg relabeling preserves the full original matching and support data, both corner receipts are exact for every legal dimension, and the conclusion selects actual originals from the given complete family.There is one nonblocking notation cleanup:  $A$  already contains a fixed original named  $L$ , while the new note also calls the additional consumer at  $p$  “ $L$ .” Rename the latter  $R$ , or  $L_{\mathrm{new}}$ . Its explicit chart and stated distinctness determine the intended original, so this does not obstruct the mathematics. I use  $R$  below.This is a written mathematical audit. I have not executed finite controls or Lean.1. The endpoint-role classification at  $t$  is exhaustiveLet  $J$  be the actual common original owner of
$$e=(a,w+14),\qquad t=(a+1,w+14).$$
The neighboring sites
$$(a+1,w+13)\in E,\qquad (a+2,w+14)\in C$$
retain their foreign endpoint owners. Endpoint disjointness therefore prevents them from being endpoints of  $J$ . Meanwhile the north neighbor  $e$  is an endpoint of  $J$ .Consequently the set of neighboring endpoints belonging to  $J$  at  $t$  must be precisely one of
$$\{N\},\qquad \{N,E\}.$$
This statement concerns own endpoint neighbors, rather than just the original matching partner. That distinction is necessary for the corner cases.For every legal canonical U source, the own-neighbor classification is:Canonical endpoint roleOwn endpoint neighborsEither leg terminalOneLeg interiorTwo opposite neighborsEither outer corner of bar row zeroTwo perpendicular neighborsEvery remaining bar endpointThreeThe lower bounds on breadth and leg lengths exclude degeneracies that could change these degrees. Isometries preserve the classification.A leg interior cannot realize  $\{N,E\}$ , since its neighbors are opposite. A degree-three endpoint cannot fit at all. Thus only a north terminal or an outer bar corner remains.After normalizing the occupied leg or corner, the four frames are exactly those stated:
$$\begin{array}{c|c}
\text{Role}&\text{Placement}\\ \hline
\text{Right north terminal}&(a+1-\ell+r,\ w+13+c)\\
\text{Left north terminal}&(a+1-\ell+r,\ w+15-c)\\
\text{Horizontal bar corner}&(a+1-r,\ w+13+c)\\
\text{Vertical bar corner}&(a+2-c,\ w+14+r).
\end{array}$$
For a normalized terminal, the canonical row direction must point south, leaving two choices for the bar direction. For a normalized outer corner, its two positive canonical coordinate directions must map to north and east, leaving exactly the two displayed assignments.There is no additional U role or orientation under the same-owner hypothesis.A matching distinction that the note correctly allowsIn the two terminal frames,  $e,t$  are the original matching pair at the terminal. They are also an original matching pair in the vertical-corner frame.In the horizontal-corner frame, however,
$$t=J(0,1),\qquad e=J(1,1),$$
and they are not matched to each other:
$$t\text{ is matched to }J(0,2)=(a+1,w+15),$$

$$e\text{ is matched to }J(2,1)=(a-1,w+14).$$
Both partners are present in the original. The hypothesis requires common ownership, so this case is valid and must be included. The proposed classification includes it correctly.2. Leg relabeling preserves the complete originalThe normalization of the opposite leg or opposite outer corner is valid at the level of endpoints, supports, and matching.Let
$$\mathcal R_h(r,c)=(r,h+1-c).$$
For the full canonical original, one has
$$\boxed{
\mathcal R_h\bigl(U(h,\ell,f)\bigr)=U(h,f,\ell),
}$$
where this equality includes the endpoint set, original support set, and unordered matching-edge set.Here is the matching-phase check.A row-zero matching pair has columns
$$(2j-1,2j).$$
After reflection and reordering, its columns become
$$(h+1-2j,\ h+2-2j).$$
Because  $h$  is even, these again begin at an odd column, exactly as required for the row-zero matching.A row-one matching pair has columns
$$(2j,2j+1).$$
Its reflected pair, after reordering, is
$$(h-2j,\ h+1-2j),$$
which again begins at an even column. The two leg matchings exchange without changing their row indices or vertical pairing phases.The supports transform correctly as well:The two bar-corner supports exchange.The two terminal axial supports exchange with the leg lengths.A near even-indexed outward support  $(r,0)$  becomes the far outward support  $(r,h+1)$ .A near odd-indexed inward support  $(r,2)$  becomes the far inward support  $(r,h-1)$ .The corresponding far supports map back to the near supports.The original support anchors are preserved by the same isometry.Thus the normalization introduces no alternative matching phase and no altered support-exclusion rule. It is a re-description of the same actual original, not the substitution of an original having merely the same endpoint silhouette.3. The rotor classification is also complete for full originalsThe standard rotor has four degree-three inner endpoints and four degree-one tips. Its inner endpoints cannot occupy  $t$ , and a tip there must have its own neighbor north.The standard rotor’s endpoints, supports, and matching are all invariant under
$$(r,c)\longmapsto(c,5-r),$$
the quarter-turn about  $(5/2,5/2)$ . For example, the four matching edges cycle into one another. The support set consists of two quarter-turn cycles:
$$(0,2)\to(2,5)\to(5,3)\to(3,0)\to(0,2),$$

$$(1,1)\to(1,4)\to(4,4)\to(4,1)\to(1,1).$$
Therefore fixing a north terminal leaves exactly two reflected full originals, not just two endpoint footprints.One of these contains
$$t+(-1,-1)=(a,w+13),$$
which is already  $E$ ’s far terminal. It is excluded by original endpoint disjointness.The surviving original is precisely
$$Z(r,c)=(a+2-r,w+12+c).$$
It contains
$$t=Z(1,2),\qquad e=Z(2,2),$$
which are one of its original matching pairs.Thus the rotor row of the receipt table is exhaustive under the same-owner hypothesis.4. Both corner frames are disjoint from  $A$  in every legal dimensionIn either corner frame, every endpoint satisfies
$$\text{column}\ge w+14,\qquad \text{row}\le a+1.$$
Every earlier original other than  $C$  has endpoint columns at most  $w+13$ . The only  $C$  endpoints in column  $w+14$  begin at row  $a+2$ .This proves endpoint disjointness for all legal breadths and both leg lengths. Increasing either leg length cannot invalidate the argument.It also proves the asserted shared-tile exhaustiveness. Since  $w+14$  is even, column  $w+13$  belongs to the preceding tile-column pair. Consequently no old endpoint at column  $w+13$  shares a tile with these corner sources.The only shared endpoint tile is
$$T(a+1,w+14).$$
In both corner orientations it contains exactly
$$J:(a+1,w+14),\qquad
J:(a+1,w+15),\qquad
C:(a+2,w+14).$$
The fourth position,  $(a+2,w+15)$ , is empty of endpoints from this inventory. Thus the tile has three endpoints and is not full.There is exactly one foreign adjacent endpoint pair in that tile:
$$t\quad\text{and}\quad C:(a+2,w+14).$$
The two corner orientations differ in whether that latter endpoint belongs to  $J$ ’s original support set. That difference accounts for their different receipts.5. The horizontal-corner charge and receipt are exactFor
$$J(r,c)=(a+1-r,w+13+c),
\qquad H=\frac{\ell+f}{2},$$
the two bar rows are  $a+1$  and  $a$ . They lie in different tile rows, while the even-to-odd bar columns align in complete tile-column pairs.The bar therefore occupies  $h$  endpoint tiles. In each leg, its first endpoint beyond the bar already lies in the tile row occupied by the second bar row. The two stems add
$$\left(\frac{\ell}{2}-1\right)
+
\left(\frac f2-1\right)
=H-2$$
new endpoint tiles. Hence
$$|\mathcal T_J|=h+H-2.$$
The original matching count is
$$|M_J|=h+H-1.$$
Exactly the odd-indexed inward lateral supports lie in these endpoint tiles, giving
$$\left|\Sigma_J\cap
\bigcup_{T\in\mathcal T_J}T\right|=H-2.$$
Both bar-corner supports lie outside the occupied tile columns at the ends of the bar. Both terminal axial supports lie beyond the corresponding endpoint tile rows. No support from one leg gains an additional incidence through the other leg, since  $h\ge6$ .Therefore
$$\begin{aligned}
q(J)
&=(h+H-1)+(H-2)-2(h+H-2)\\
&=\boxed{1-h}.
\end{aligned}$$
At the sole shared tile, the target  $C:(a+2,w+14)$  has intrinsic  $J$ -coordinates
$$(-1,1).$$
It is not an original support of  $J$ . Thus
$$J:t\longrightarrow C:(a+2,w+14)$$
survives.The reverse direction targets  $t$ , which is  $C$ ’s original axial support. It remains excluded after  $J$  consumes that site.Accordingly,
$$\Delta S=h-1,\qquad
\Delta E_v=1,\qquad
\Delta F=\Delta N=0,$$
and
$$\boxed{\Delta\Phi(J\mid A)=h-2\ge4.}$$
There is no additional full-tile receipt or reverse-event debit.6. The vertical-corner charge and receipt are exactFor
$$J(r,c)=(a+2-c,w+14+r),
\qquad H=\frac{\ell+f}{2},$$
the two bar columns are  $w+14,w+15$ , an aligned tile-column pair. The two ends of its  $h$ -row bar split tile rows, so the bar meets
$$\frac h2+1$$
endpoint tiles.The two horizontal stems add  $\ell/2+f/2=H$  tiles. Therefore
$$|\mathcal T_J|=\frac h2+H+1.$$
The matching count remains
$$|M_J|=h+H-1.$$
The counted original supports are precisely:The two bar-corner supports.The two terminal axial supports.The  $H$  even-indexed outward lateral supports.Thus
$$\left|\Sigma_J\cap
\bigcup_{T\in\mathcal T_J}T\right|=H+4,$$
and
$$\begin{aligned}
q(J)
&=(h+H-1)+(H+4)
 -2\left(\frac h2+H+1\right)\\
&=\boxed{1}.
\end{aligned}$$
At the shared tile,  $C$ ’s terminal is now
$$(a+2,w+14)=J(0,0),$$
the image of an original bar-corner support of  $J$ . Therefore  $J\to C$  is excluded. The reverse  $C\to J$  direction again targets  $C$ ’s original axial support  $t$ , so it is excluded too.Consequently,
$$\Delta N=1,\qquad
\Delta S=\Delta F=\Delta E_v=0,$$
giving
$$\boxed{\Delta\Phi(J\mid A)=1.}$$
Any full tiles belonging to this original alone remain excluded from  $F$ , as required. The common three-endpoint tile creates no mixed-full contribution.The two new receipts can therefore be recorded without qualification:Corner orientation $q(J)$  $\Delta N$  $\Delta S$  $\Delta F$  $\Delta E_v$  $\Delta\Phi$ Horizontal $1-h$  $0$  $h-1$  $0$  $1$  $h-2$ Vertical $1$  $1$  $0$  $0$  $0$  $1$ 7. The exceptional continuation invokes the correct accepted theoremThe note correctly invokes the accepted all-north-terminal result, including all widths and both leg lengths. That scope is needed here; the older internal-cap result alone would be insufficient.For an actual left north-terminal consumer
$$J=U(s,\ell,m),\qquad
J(r,c)=(a+1-\ell+r,w+15-c),$$
the only zero increments are:
$$g=w+15-s\text{ inside }V\text{’s bar},
\qquad m=\ell-8,$$
and
$$g=3,\quad\text{first residual family},\qquad m=\ell+8.$$
This includes the second-residual  $g=3$  bar case and the first-residual Q-tip case. Every other endpoint-disjoint left-terminal original has increment  $1$ .On either zero boundary,
$$p=(a+2,w+12)$$
is absent from the endpoint set of  $A\cup\{J\}$ . Its intrinsic  $J$ -coordinates are  $(\ell+1,3)$ , which cannot be on either stem or on the bar.The retained neighbors west, east, and south of  $p$  remain the specified  $V/E$  endpoints. As  $p$  is an original support of  $V$ , completeness forces it to be consumed.Let  $R$  be its actual original owner in the given family. Then necessarily
$$\boxed{R\in\mathscr F\setminus(A\cup\{J\}).}$$
This distinctness follows from the absence of  $p$ , rather than from an assumed fresh-consumer convention.The accepted continuation theorem supplies exactly
$$R=U(h,d,f),\qquad
R(r,c)=(a+2-d+r,w+13-c),$$
with
$$6\le h\le s-4,\qquad
14\le d\le\ell-2,\qquad
4\le f\le d-10,$$
and
$$\Delta\Phi(R\mid A+J)=h-2\ge4.$$
These statements concern the same prescribed prefix  $A+J$ . Arbitrary other originals in the complete family cannot remove a retained endpoint collision or erase the forcing condition at  $p$ .If the displayed parameter region is empty, the assumed complete family with that joint consumer cannot exist. Such a zero row therefore creates no unresolved case in the existential subinventory argument.8. The quantified subinventory conclusion follows exactlyWrite  $\mathscr F$  for the complete original family and set
$$B_0=\Phi(Q,D,W).$$
The accepted baseline is
$$\Phi(A)=B_0-1.$$
Neither  $e$  nor  $t$  is an endpoint of  $A$ . Therefore their actual common original owner satisfies  $J\notin A$ .Nonzero rowsThe exhaustive role classification puts  $J$  in one of the displayed receipt rows. In every nonzero row,
$$\Delta\Phi(J\mid A)\ge1.$$
Take
$$I=A\cup\{J\}.$$
This consists entirely of actual originals of  $\mathscr F$ , and
$$\Phi(I)
=B_0-1+\Delta\Phi(J\mid A)
\ge B_0.$$
For the horizontal corner, the more precise result is
$$\Phi(I)=B_0+h-3\ge B_0+3.$$
For the other immediate-repair rows, the increment is exactly one.Zero rowsIn a zero row, completeness supplies the actual additional original  $R$  described above. Take
$$I=A\cup\{J,R\}.$$
Then
$$\begin{aligned}
\Phi(I)
&=\Phi(A)
 +\Delta\Phi(J\mid A)
 +\Delta\Phi(R\mid A+J)\\
&=B_0-1+0+(h-2)\\
&=\boxed{B_0+h-3\ge B_0+3}.
\end{aligned}$$
Thus in every case,
$$\boxed{
A\cup\{J\}\subseteq I\subseteq\mathscr F,\qquad
|I\setminus(A\cup\{J\})|\le1,\qquad
\Phi(I)\ge\Phi(Q,D,W).
}$$
That is precisely the claimed quantified conclusion.No hypothetical consumer is substituted for an actual one. The source selected at  $p$  is its owner in the already given complete family. Its classification and receipt follow from its retained endpoint disjointness and the accepted continuation theorem.9. The nonreuse and global-scope statements are accurateThe proof keeps one consistent original-owner inventory:Relabeling the legs changes the description of an original, not its identity.Each inserted original contributes to  $N$  or  $S$  exactly once.A source’s original supports continue to govern its event exclusions after consumption.Consuming  $e,t$ , or other outstanding supports, provides no independent per-site credit.In a zero row, the positive-owner unit of  $J$  and its single  $V/Q$  event debit remain in the prefix.The additional source’s three events and one new mixed full tile are counted once in its marginal against that prefix.The selected subinventory need not be complete. Its functional is evaluated using the full original support sets of its retained owners, exactly as in the preceding partial-inventory identities.The result establishes an existential compensating subinventory for one prescribed residual package with a common actual consumer. It does not assign mutually disjoint owner budgets to multiple packages. Nor does inclusion  $I\subseteq\mathscr F$  provide monotonicity of  $\Phi$ : additional originals can change the signed contact contribution.Accordingly, the separate-consumer case, reuse across multiple residual packages, and arbitrary exterior signed contributions remain outside the lemma. The global allocation and rectangular-grid equality targets remain open.Final verdict: ACCEPT. Rename the additional consumer to avoid the existing fixed-owner symbol  $L$ ; the classification, corner calculations, and actual-subinventory compensation theorem require no substantive repair.
