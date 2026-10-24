Verdict: REVISE — one narrow quantifier correctionThe new canonical-gate equivalence, unique-consumer description, least demand-preserving hull, demand supermodularity, elimination of duplicate-new-core marks, and binary feasible-core valuation all pass under the supplied complete-source hypotheses.The correction concerns the multibranch minimum-counterexample conclusion: it requires every counted branch  $I_t=C\cup A_t$  to be a proper subfamily of  $F$ . In the displayed multibranch hypotheses, disjointness is stated, but nonemptiness or properness is not. The valuation identities themselves remain valid with empty parts.I found no geometric counterexample to the new gate or feasible-core theorems. I have not certified execution or assumed that gate consumers are negative.1. Required correction: make the proper-branch condition explicitIn FEASIBLE_CORE_SEPARATOR_TRANSFER.md, §5, the inference
$$(r-1)\mu(C)\ge D_r+1$$
uses
$$\mu(I_t)\ge0\qquad\text{for every }t.$$
Source minimality supplies this only when every  $I_t$  is proper.A sufficient—and here equivalent—condition is:At least two of the exclusive owner sets  $A_t$  are nonempty. Consequently every  $I_t=C\cup A_t$  is a proper subfamily of  $F$ .Without that condition, the stated set hypotheses allow
$$r=2,\qquad C=\varnothing,\qquad A_1=F,\qquad A_2=\varnothing.$$
The no-cross-edge condition is vacuous, the core is feasible, and the valuation is simply
$$\mu(F)=\mu(F)+0.$$
One cannot apply minimality to its first branch, because that branch is  $F$  itself.This demonstrates a missing hypothesis in the inference; it is not a constructed negative-margin physical fusion.Once properness is stated, the calculation is exact:
$$\begin{aligned}
\mu(F)
&=\sum_t\mu(I_t)-(r-1)\mu(C)+D_r,\\
(r-1)\mu(C)
&=\sum_t\mu(I_t)+D_r-\mu(F)
\ge D_r+1,
\end{aligned}$$
using integrality and  $\mu(F)<0$ . After the gate theorem gives  $D_r=0$ ,
$$\boxed{(r-1)\mu(C)\ge1.}$$
The same properness qualification belongs to the corresponding minimum-counterexample paragraph in the canonical-gate note. If “branch” is already defined elsewhere to mean a nonempty exclusive part, this is a clarification of that convention rather than a new geometric assumption. In the supplied §5, it should be explicit.2. The supplied coordinates establish the local gate stencilUse  $a_0=(3,1)$  for the gate’s anchor, to distinguish it from the leg-height parameter  $a$ . Put
$$t=(3,2),\quad p=(2,2),\quad q=(4,2),\quad
r=(2,3),\quad u=(3,3).$$
Because  $a\ge4$ , the odd row  $3$  belongs to the left leg. The supplied support formula therefore gives
$$t\in T_i,\qquad a_0\in P_i.$$
The three protectors have exactly the claimed original neighborhoods:ProtectorThree original occupied neighborsMissing neighbor $(2,1)$  $(1,1),(3,1),(2,0)$  $p=(2,2)$  $(4,1)$  $(3,1),(5,1),(4,0)$  $q=(4,2)$  $(1,3)$  $(0,3),(1,2),(1,4)$  $r=(2,3)$ The boundary  $a=4$  is covered: then  $(5,1)$  is the terminal support  $(a+1,1)$ , so it remains occupied and still supplies the third original neighbor of  $(4,1)$ .For  $w\ge6$ , the right leg and its supports do not enter  $p,q,r,u$ . In particular,  $p,q,r$  are original blanks, and  $t$  originally has only its anchor  $a_0$  as an occupied neighbor.Reflection
$$(x,y)\longmapsto(x,w+1-y)$$
gives the other side, with the corresponding leg height. Lattice isometries and translations preserve every adjacency and occupancy statement used here. The argument does not depend on alignment with the fixed physical tile partition.Thus, for the stipulated canonical side, the actual degree-four condition is precisely
$$p\in O\ \lor\ q\in O\ \lor\ r\in O.$$
Occupied triggers are endpointsLet  $z\in\{p,q,r\}$  be occupied, and let  $v\in P_i$  be its corresponding positive protector. If  $z$  were not an endpoint, it would be a selected support of a retained owner  $k$ .Its original anchor  $a_k(z)$  is distinct from  $v$ . Otherwise endpoint ownership uniqueness would imply  $k=i$ , contrary to  $z$  being an original blank of  $i$ . Hence  $z$  would have two distinct occupied neighbors,
$$a_k(z),\qquad v,$$
contradicting selected-support feasibility.Therefore every occupied trigger is an endpoint.Marking forces gate consumptionIf  $p$  or  $q$  is occupied, the retained original support  $t$  has its anchor and an additional occupied neighbor. It cannot remain selected, so it must be an endpoint.For a guard witness  $r$ , suppose that  $t$  remained selected. Its unique occupied neighbor would be  $a_0$ , forcing both  $p$  and  $u$  to be blank. But  $r$  is an endpoint, and its four neighbors are
$$(1,3),\quad p,\quad u,\quad (2,4).$$
With  $p,u$  blank, it has occupied degree at most two, contradicting the endpoint degree bound.Thus every mark consumes  $t$ .Gate consumption forces markingConversely, if  $t$  is an endpoint, its possible neighbors are
$$a_0,\quad p,\quad q,\quad u.$$
If both  $p,q$  were blank, its occupied degree would be at most two. Therefore one of  $p,q$  is occupied, marking a leg protector.This proves
$$\boxed{\text{canonical side marked}\iff t\in P}$$
and the stronger observation that every mark has a leg-protector witness, even when it also has a guard witness.The proof requires the degree-at-least-three property for all retained endpoints, including foreign trigger endpoints and the gate’s consumer endpoint. Complete-source retention supplies that property.3. The gate consumer is unique, but need not be negativeFor a marked side  $s$  of positive owner  $i$ , its gate  $t(s)$  lies in  $T_i$  and becomes an endpoint. Disjoint endpoint ownership gives one consumer  $j(s)$ , and
$$j(s)\ne i$$
because  $T_i\cap P_i=\varnothing$ .That is the owner restriction established by the argument. No sign restriction on  $j(s)$  follows or is needed.The two roles must remain distinct:
$$j(s)=\operatorname{owner}(t(s))$$
is the gate consumer, whereas a chosen mark-witness owner owns one of the trigger vertices  $p,q,r$ , or another endpoint specified by an earlier assignment convention. Those owners need not coincide. A negative-owner theorem for a previously assigned mark endpoint cannot be transferred to  $j(s)$ .For every feasible retained  $I\subseteq F$  containing  $i$ ,
$$\begin{aligned}
s\text{ marked in }I
&\iff t(s)\in P_I\\
&\iff j(s)\in I.
\end{aligned}$$
The first equivalence applies the local theorem inside the actual restriction; the second uses fixed endpoint ownership.An unmarked full-family side cannot become marked under restriction, because its original protectors persist while occupancy only decreases.4. The canonical least demand-preserving hull is genuinely leastLet  $\mathcal E$  be the fixed set of labelled full-family mark incidences
$$(i,s,j(s)).$$
For every feasible retained family  $I$ ,
$$\boxed{
G(I)=\sum_{(i,s,j)\in\mathcal E}
       \mathbf 1_{\{i,j\}\subseteq I}.
}$$
Distinct sides remain distinct labels, including when they have the same consumer.Define the seed
$$S=\{\text{all positive owners of }F\}
  \cup\{j(s):s\text{ is marked in }F\},
\qquad H=\operatorname{Cl}(S).$$
The supplied Horn theorem gives a feasible  $H$  containing  $S$ . The consumer equivalence then proves that  $H$  preserves all original positives and all their full-family marks.Conversely, any feasible retained family  $I$  preserving those data must retain every relevant positive owner and every corresponding gate consumer. Thus  $S\subseteq I$ , and Horn leastness gives
$$H\subseteq I.$$
Therefore  $H$  is the unique least such family within the fixed ambient family  $F$ .The witness-hull assertion also follows. Since  $H$  retains each mark, choose one actual endpoint witness for each mark inside  $H$ , and let  $W$  consist of their owners together with all positive owners. Then
$$\operatorname{Cl}(W)\subseteq H,$$
because  $H$  is a feasible completion of  $W$ . On the other hand, retaining those witnesses preserves all marks, so the leastness just proved gives
$$H\subseteq\operatorname{Cl}(W).$$
Hence
$$\operatorname{Cl}(W)=H.$$
This establishes the existence of a witness choice realizing the canonical hull. It does not assert equality for arbitrary witness choices, and the note correctly avoids that stronger claim.5. Demand is supermodular on the legal Horn latticeThe proof works even when the ordinary union of two legal families is infeasible. The clean way to express it is to define, on all owner subsets,
$$\widetilde G(X)
=\sum_{(i,s,j)\in\mathcal E}
   \mathbf 1_{\{i,j\}\subseteq X}.$$
This agrees with physical  $G$  on feasible families.For a fixed incidence,
$$\mathbf 1_{\{i,j\}\subseteq L}
+\mathbf 1_{\{i,j\}\subseteq K}
\le
\mathbf 1_{\{i,j\}\subseteq L\cap K}
+\mathbf 1_{\{i,j\}\subseteq L\cup K}.$$
Summing gives ordinary set supermodularity of  $\widetilde G$ . Since
$$L\cup K\subseteq\operatorname{Cl}(L\cup K)$$
and incidence counts increase under owner inclusion,
$$\begin{aligned}
G(L)+G(K)
&\le \widetilde G(L\cap K)+\widetilde G(L\cup K)\\
&\le G(L\cap K)+G(\operatorname{Cl}(L\cup K)).
\end{aligned}$$
Both the meet and the Horn join are feasible, so the final quantities are physical demand counts.Thus the stated supermodularity is valid. It does not require treating an infeasible ordinary union as a legal physical fusion, and it supplies no corresponding property of  $R$  or  $\mu$ .6. Duplicate-new-core marks vanish without minimalityFor any two feasible retained families  $L,K$ , their intersection  $C$  is feasible.For a positive owner  $i\in C$ , if a side is marked in both  $L$  and  $K$ , its same fixed consumer lies in both. Hence  $j(s)\in C$ , and the side is marked in  $C$ . Conversely, a mark in  $C$  persists in both restrictions. Pointwise,
$$\boxed{b_C=b_Lb_K.}$$
It follows that
$$b_Lb_K(1-b_C)=0,
\qquad D=0.$$
This conclusion requires neither minimality nor the no-exclusive-cross-edge condition.For branches  $I_t=C\cup A_t$ , a core side unmarked in  $C$  has its consumer outside  $C$ . Disjoint exclusive owner sets place that consumer in at most one branch. Such a side is therefore marked in at most one branch, proving
$$D_r=0.$$
For a singleton positive core  $C=\{i\}$ , a side marked in both restrictions would force its consumer to be  $i$ , contradicting  $j(s)\ne i$ . Thus the earlier duplicate separator-side correction is indeed always zero in this physical model. The earlier OR formula remains valid; the new theorem restricts its physically possible overlap cases.This does not make  $G$  a valuation on arbitrary legal pairs. The separate no-cross condition is what guarantees that every full-family incidence is covered by one branch.7. The arbitrary feasible-core restriction proof is validThe new proof correctly replaces intrinsic feasibility of a shared single source by actual feasibility of the entire shared core.Take a selected  $x$  in  $L=A\cup C$ , produced by  $i$ , and a second occupied neighbor
$$y\ne a_i(x).$$
Full feasibility forces  $x$  to be an endpoint of a removed  $B$ -owner  $j$ . If  $i\in A$ , the endpoint edge  $a_i(x)x$  is forbidden. Hence  $i\in C$ , and  $x$ , being no endpoint of  $L$ , is selected in  $C$ .Core feasibility then implies  $y\notin O_C$ . Any retained owner supplying  $y$ 's occupancy lies in  $A$ ; call it  $k$ .If  $y\in P_k$ , the edge  $yx$  violates the no-cross hypothesis. Otherwise  $y\in T_k$ , with anchor  $a_k(y)\ne x$  by endpoint ownership uniqueness. Full feasibility forces  $y$  to be an endpoint of some owner  $\ell$ .If  $\ell\in A$ ,  $yx$  is forbidden.If  $\ell\in B$ ,  $a_k(y)y$  is forbidden.Therefore  $\ell\in C$ , contradicting  $y\notin O_C$ .This handles the restored support/support case. Original endpoint degrees and unchanged matching edges persist because whole original occupied sets are retained.Actual core feasibility is essential at the indicated step. An arbitrary set of desired boundary owners cannot replace that hypothesis.8. The aggregate core-profile and reserve valuation proofs passThe core-profile argument is stronger than the original single-source profile assumption: it establishes the needed property for the fused endpoint set of the feasible core.Suppose a fixed square contained precisely two diagonal core endpoints. Each missing corner has those two endpoints as neighbors. It cannot be selected, and it is not an endpoint, so it is unoccupied. Each diagonal endpoint then has no occupied intratile neighbor and at most its two outside-tile neighbors, contradicting occupied degree at least three.Therefore every nonempty core endpoint profile is connected. No global connectivity of  $C$  is needed.In a full tile of  $F$ , the complement of this core profile is connected whenever nonempty. If its endpoints had both exclusive  $A$ - and  $B$ -owners, a path in that complement would contain a forbidden cross edge. The tile is consequently full in one restriction. It is full in both exactly when it is full in  $C$ .Fixed disjoint endpoint ownership also preserves the originally-full versus mixed-full distinction. Together with the analogous event argument, this proves
$$\begin{aligned}
E(F)&=E(L)\cup E(K),&
E(L)\cap E(K)&=E(C),\\
F_{\mathrm{mix}}(F)&=F_{\mathrm{mix}}(L)\cup F_{\mathrm{mix}}(K),&
F_{\mathrm{mix}}(L)\cap F_{\mathrm{mix}}(K)&=F_{\mathrm{mix}}(C).
\end{aligned}$$
Sourcewise modularity of  $S$  then gives
$$\boxed{R(F)=R(L)+R(K)-R(C).}$$
The correction really is  $R(C)$ . Its internal event debit and mixed-full-tile credit retain their original signs; replacing it by  $S(C)$  would omit those contributions.For demand, every incidence connects adjacent endpoints:
$$a_i(t(s))\in P_i,\qquad t(s)\in P_{j(s)}.$$
Its owners cannot lie in opposite exclusive parts. Thus every incidence is covered by  $L$  or  $K$ , and the common incidences are exactly those in  $C$ . Hence
$$G(F)=G(L)+G(K)-G(C).$$
Together with modularity of  $N$ ,
$$\boxed{\mu(F)=\mu(L)+\mu(K)-\mu(C).}$$
The multibranch valuations follow by the same multiplicities. Core occurrences are counted  $r$  times in the branch sum and corrected  $r-1$  times.Keep the feasible-union scope explicitFor these valuations,  $F=L\cup K$  must itself be the complete feasible family required by the core theorem. I read the canonical note’s use of the already fixed  $F$  in exactly that way.Arbitrary legal  $L,K$  inside a larger ambient family need not have a legal ordinary union: Horn closure may require an additional consumer. The assertions  $D=0$  and demand supermodularity remain valid for such pairs, but the shared-core valuation should not silently be extended to their Horn join.9. Examples and formalization remain separate from the general proofThe displayed five-source-overlap arithmetic is consistent:
$$R(C)=(k+19)+2\cdot2-6=k+17,$$
and at  $k=24$ ,
$$35+30-41=24,\qquad 34+30-41=23.$$
The stated extension increment also simplifies correctly:
$$5+2\left(\frac k2+3\right)
-\left((k+7)+\left(\frac k2+3\right)\right)
=1-\frac k2.$$
However, the full coordinate data for the referenced upper-source table and nine-source canonical-hull construction are not supplied here. I therefore do not independently certify that entire fixture, its canonical seed/hull identification, or its all- $k$  physical feasibility from the displayed arithmetic and partial support list. The general proofs above do not depend on those reconstructions.Likewise, the new Lean declaration bodies were not included. The stated scope—local equivalence and consumer retention in one file, restriction feasibility and event identities in the other—is consistent with the written division of work. It does not cover the catalogue adapters, square valuation, labelled counts, canonical-hull consequences, or supermodularity proof end to end. No compilation, axiom audit, or finite control is certified by this review.With the proper-branch hypothesis made explicit, the substantive new general conclusions are valid at the stated complete-source scope. They determine demand retention and exact overlap compensation. They do not provide the remaining global bound
$$N+R-G\ge0$$
for unrestricted finite mixed U/rotor fusions, and they do not establish grid equality.
