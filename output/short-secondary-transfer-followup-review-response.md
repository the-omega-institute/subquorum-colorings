ACCEPTThe two additions are mathematically sound under the stated source model and accepted dependencies. The positive transfer, reconstruction, and all-old-target nonreuse extend to every allowed  $j\ge8$  conditioned on the actual secondary consumer having  $\ell=6$ . Both new fence alternatives are valid, including their different-owner collision requirements.I accept every conclusion about  $d$ , including the exclusion of H width  $12$ , only under  $j=8$ , as expressly required in your question and the preceding sentence of Section 3.One wording clarification would make that scope explicit throughout. Replace:“In particular actual H width12 is impossible…”with:“In particular, when  $j=8$ , actual H width12 is impossible, although the three-source-only obstruction above excludes only H widths at most10.”I read the present sentence as inheriting the immediately preceding “ONLY when  $j=8$ ” qualification. An all- $j$  interpretation of that sentence is not established by this argument.1. The positive transfer extends to all  $j\ge8$  with actual  $\ell=6$ The general secondary-escape lemma retains its original scope:
$$6\le\ell\le j-2.$$
It forces  $\ell=6$  at  $j=8$ . For larger  $j$ , the revised theorem correctly adds  $\ell=6$  as an actual-source condition.Once that condition holds,
$$D(r,c)=(b-7+r,c+5)$$
is independent of  $j$ . Every subsequent local forcing step uses this fixed D chart, X, and Q; none requires  $m\le d-2$ .The important checks are:The exclusion of  $m=6$  remains
$$D(3,6)=(b-4,11)=Q(0,6),$$
available because D’s independent far length satisfies  $t\ge4$ .At  $q=(b-5,7)$ , the three fixed endpoint neighbors remain
$$D(1,2),\quad D(2,1),\quad Q(4,6)$$
to the north, west, and south.The claim that q is not H-owned remains valid for every allowed  $j$ . H’s bar rows are
$$b-1-j,\quad b-j,$$
both above  $q$ , since  $j\ge8$ . Its leg columns are  $5$  and  $d+4$ , neither equal to  $7$ .Consequently the consumer of q differs from the blocking owners and can have an own endpoint neighbor only east. The exact U/rotor catalogue therefore gives the same exhaustive alternatives as before: a U east terminal or an east rotor tip. Both rotor chiralities contain
$$q+(-1,2)=(b-6,9)=D(1,4),$$
so both are excluded.For the U terminal, the remaining collisions also remain unchanged:StepFixed obstructionStem cannot reach column  $m+5$  $D(2,m)=(b-5,m+5)$ Upward bar is impossibleD’s lower bar at  $(b-6,g+7)$ Downward bar with  $g=4$  is impossible $Q(1,6)=(b-4,10)$ Thus, throughout the enlarged class,
$$E(r,c)=(b-6+c,g+7-r),\qquad 6\le g\le m-4,$$
and  $m\ge10$ .The positive phase and activation are likewise independent of  $j$ . The E chart preserves the aligned tiles, and its original terminal supports are
$$E(g+1,1)=D(2,1),\qquad E(g,0)=D(1,2).$$
They give one activation at the original E terminal. The full tile still consists of that terminal and three D endpoints; no additional resource follows from enlarging the parameter range.2. Both fence alternatives are correct, including owner exclusionsCase  $\omega=6$ E’s far leg lies on row  $b$ . Its original far-leg endpoints are
$$E(r,6)=(b,g+7-r),\qquad 2\le r\le\nu,$$
so their column interval is
$$[g+7-\nu,\ g+5].$$
The fixed Q endpoint is
$$Q(0,2)=(b,11).$$
It belongs to that far leg exactly when
$$r=g-4\in[2,\nu].$$
Since  $g\ge6$ , the lower requirement is automatic, leaving precisely
$$\nu\ge g-4.$$
This is a genuine different-owner collision: E owns q, whereas q is absent from Q’s original endpoint set. Thus  $E\ne Q$ , even if owners recur elsewhere.Avoidance and evenness give
$$\nu<g-4
\quad\Longrightarrow\quad
\nu\le g-6.$$
Combining this with  $\nu\ge4$  yields
$$\boxed{4\le\nu\le g-6,\qquad g\ge10.}$$
Case  $\omega\ge8$ E contains the original bar endpoint
$$E(0,8)=(b+2,g+7).$$
Using the actual B chart
$$B(r,c)=(b+3-r,c+1),$$
the same point is
$$B(1,g+6)$$
whenever  $g+6\le W$ , equivalently  $g+7\le W+1$ . Its column is within B’s bar interval whenever that inequality holds.Here too, a self-owner check is required, and it succeeds. E cannot be B: the E terminal
$$q=(b-5,7)$$
has B coordinates  $(8,6)$ . This is not a B endpoint: it is outside B’s two bar rows, and  $6$  is neither leg column  $1$  nor  $W$ , because  $W\ge12$ .Therefore the bar intersection is prohibited. Avoidance gives
$$g>W-6,$$
and evenness yields
$$\boxed{g\ge W-4.}$$
These branches are exhaustive because  $\omega$  is even and at least six. They establish the following necessary bounds:Actual B widthBounds for every  $j\ge8$  with actual  $\ell=6$ Additional bound only when  $j=8$  $W=12$  $g\ge8,\ m\ge12$  $d\ge14$  $W\ge14$  $g\ge10,\ m\ge14$  $d\ge16$ Some parameter choices can face further collisions. The displayed bounds are valid necessary conditions and do not assert that their boundary values are realizable.Why the d-scope must remain restrictedAt  $j=8$ , the endpoint supporting  $m\le d-2$  is
$$(b-7,d+4)=H(2,d),$$
which exists under  $z\ge4$ .For general  $j$ , the corresponding point would be
$$(b-7,d+4)=H(j-6,d).$$
Its existence is not guaranteed uniformly by  $z\ge4$ . Thus the all- $j$  transfer and fence arguments cannot simply inherit the parent-width comparison.The revised theorem correctly avoids doing so. In particular, the accepted width- $12$  exclusion concerns actual  $j=8$  chains with B, and the earlier three-source-only  $j=8$  obstruction excludes H widths at most ten.3. Reconstruction is injective across the entire enlarged unionThe reconstruction does not use  $j=8$ . An original E terminal occurrence fixes its ordered axial/lateral supports, hence
$$D(2,1),\qquad D(1,2).$$
These identify D’s physical incident bar end and directed chart. They then recover:Q at the south neighbor  $Q(4,6)=(b-4,7)$ .Q’s other terminal  $(b+1,3)$ .X at its north neighbor  $(b,3)$ .X’s other outer bar corner  $y=(3,3)$ .The actual B gate at  $(3,2)$ .The remaining positive producer anchor  $(3,1)$ , since B also owns  $(4,2)$ .The actual labelled A side through the accepted canonical-gate uniqueness.This recovers the same labelled claim from equal E terminal resources, regardless of which  $j$  initially described the occurrence.Moreover, once the actual claim and its normalized frame are recovered, the point
$$v=(b-1,5)$$
is fixed. Its unique original owner H and the physical incident leg at v are then fixed as well. Thus the same recovered claim cannot acquire a second label merely by being described with a different parent incident length.The  $j=8$  subclass therefore sits inside one injective all- $j$ ,  $\ell=6$  assignment. Equal leg lengths, leg-name exchanges, and recurring owners do not create extra copies.4. The revised S/P exclusions and every other old-target exclusion holdS: the H witness survives for every  $j$ The forced producer map remains
$$F_S(r,c)=(b-3-c,r+4).$$
Its two required endpoints are
$$\begin{aligned}
F_S(0,1)&=(b-4,4)=X(1,b-6),\\
F_S(1,1)&=(b-4,5)=H(j-3,1).
\end{aligned}$$
The second witness exists for every  $j\ge8$ , because  $j-3$  lies within H’s incident leg. The first exists because  $b\ge j+6\ge14$ .Since X and H are distinct original owners, one hypothetical old producer cannot contain both endpoints. This excludes new, self, and recurring producer identifications.P: the new outside-D witness argument is validThe forced producer map remains
$$F_P(r,c)=(b-8+r,g+9-c).$$
The arbitrary-length old-P bound  $w_{\rm old}\ge g+4$  ensures that both required bar endpoints exist.The second witness is
$$F_P(1,g+3)=(b-7,6)=D(0,1).$$
Unique original endpoint ownership therefore identifies the hypothetical old producer with the original D owner.But that same producer would have to contain
$$F_P(0,g+3)=(b-8,6).$$
Every D endpoint has row at least  $b-7$ . Hence this required endpoint lies outside D’s original endpoint set, contradicting the forced owner identification.This argument works without knowing who owns the first witness—or whether it was already occupied. It removes the former dependence on that point being H-owned and closes every self-owner possibility.All remaining named target familiesNone of the remaining exclusions uses  $j=8$  or  $m\le d-2$ :Old target familyContinuing obstructionRAn old support is rotor-owned; both new supports are D-owned U endpoints.All-length E/S companionsTheir two support owners are distinct; the new supports have the same owner.Near-tight  $Q_1$ Its support owners are distinct; the new supports are both D-owned.Entire unsaturated-band D/L unionIts support owners are distinct; the new supports are both D-owned.Tight targetsOrdered support roles identify the transverse physical incident leg with D’s length-six leg, contradicting  $h_{\rm old}\ge8$ .Near-tight  $Q_2$ The same physical identification contradicts  $h_{\rm old}\ge10$ .Nonmatched positive upward successorsTheir axial support has original endpoint degree three;  $D(2,1)$  has original degree two.For tight and near-tight  $Q_2$ , the compared length remains D’s incident length six. D’s independent far length cannot replace it: the ordered  $(2,1),(1,2)$  support pair identifies the physical bar end. E’s incident length  $g$  is also not the length being compared.The original-degree exclusion likewise remains an original-source statement. Additional ambient neighbors cannot change it.Thus the enlarged assignment is jointly disjoint from the complete specified old target union, not merely from a numerical activation lower bound.5. The enlarged residual accounting is correctSection 5 correctly defines  $\kappa$  as the cardinality of one residual union
$$\{\text{eligible actual claims}:j\ge8,\ \ell=6\}.$$
The  $j=8$  subclass belongs to that union once. The two fence branches do not create additional demand classes or additional activation credits.Accordingly,
$$q=q_0+\kappa,\qquad t=t_0-\kappa,
\qquad A_{\rm activation}\ge q+\rho$$
preserve the same total G and the same physical inventory. The unchanged calculation gives
$$\boxed{
\mu\ge n_0+u+p+
\left\lceil
\frac{m_8-s-t_0+\kappa+\rho}{2}
\right\rceil.
}$$
The exact gain and sufficient threshold remain correct:
$$\Delta=
\left\lceil\frac{H_0+\kappa}{2}\right\rceil
-\left\lceil\frac{H_0}{2}\right\rceil,
\qquad H_0=m_8-s-t_0+\rho,$$
and
$$s+t_0\le2n_0+2u+2p+m_8+\rho+\kappa+1.$$
There is one useful baseline distinction when reporting the revision: this displayed gain is relative to the named old certificate before the short-secondary class is added. If a  $j=8$ -only certificate with  $\kappa_8$  claims has already been applied, the newly incremental count is
$$\kappa-\kappa_8,$$
not  $\kappa$  again. The revised union formulation already handles this correctly by including  $j=8$  once.No activation is also added to  $\rho$ , no new pair or cap is credited at E’s tile, and no change is made to  $P,p,G$ , or the other inventory terms.Accepted scopeThere is no blocking mathematical gap in either addition with the H-width restriction made explicit as above. The revised theorem establishes the conditional all- $j$ , actual- $\ell=6$  transfer, the two fence alternatives, joint nonreuse, and the same-ledger consequence.This audit does not certify scoped Lean or finite enumeration, complete realizability, secondary lengths  $\ell\ge8$ , novelty, residual coverage, a global allocation improvement, or unrestricted equality.
