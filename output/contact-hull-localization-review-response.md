Verdict: ACCEPT, with one boundary case that should be stated explicitlyUnder the inherited exact Horn-closure and feasible-core separator theorems, the package is mathematically sound. The contact hull construction, physical feasibility of  $C(T)\cup B(T)$ , exact localization of  $R,N,G,\mu$ , the one-use loss bound, the J24 obstruction, and the source-minimal inequalities all follow.There is one literal edge case to make explicit:  $T\neq\varnothing$  but  $D(T)=C(T)=\varnothing$ . The written argument invokes the separator theorem with an empty shared core without saying that the theorem permits this. If the inherited theorem quantifies over the empty complete feasible family, there is no defect. If it was stated only for a nonempty core, add a direct no-contact argument for this case. This is the only proof-completeness issue I find.The integer-valued convention used by the ceiling bound and the  $+1$  in (7) must also remain part of the inherited reserve model:  $R$ , the component increments  $d_j$ , and  $\mu$  need to have the integrality asserted in the note. Under that convention, the arithmetic is correct.1. Endpoint components and the ambient closureThe partition into new endpoint-connected owner groups is valid.Each original U or rotor endpoint graph is connected. Since all original endpoint sets in  $J$  are pairwise disjoint, every source occurrence in  $J\setminus I$  lies entirely inside one connected component of the lattice graph on
$$P(J)\setminus P(I).$$
Thus the components partition the added source occurrences, and there is no endpoint edge between distinct  $B_j$ .For a selected collection  $T$ ,  $D(T)$  contains every old owner with an endpoint adjacent to a  $B(T)$ -endpoint. Since  $I$  is already a complete feasible family and  $D(T)\subseteq I$ , the least complete-feasible closure in the ambient source family  $J$  satisfies
$$C(T)=\operatorname{cl}_J(D(T))\subseteq I.$$
This is the correct reason that closure in  $J$  does not unexpectedly pull in a new owner outside  $I$ . The family  $I$  itself is a feasible carrier for  $D(T)$ , so leastness places the ambient closure inside  $I$ . Consequently, closing inside  $I$  gives the same result.The closure also correctly incorporates support/support-conflict implications. The raw contact set need not contain every old owner needed to restore feasibility; the closure adds precisely those owners required by the Horn implications. This is exactly what the J24 example demonstrates.Because every old owner directly adjacent to  $B(T)$  is in  $D(T)\subseteq C(T)$ , there is no endpoint edge between
$$B(T)\quad\text{and}\quad I\setminus C(T).$$
That is the required separation condition.Now apply the inherited separator theorem to
$$X(T)=(I\setminus C(T))\cup C(T)\cup B(T),$$
with shared core  $C(T)$ , old exclusive part  $I\setminus C(T)$ , and new exclusive part  $B(T)$ . The full family  $X(T)=I\cup B(T)$  is feasible by the earlier component theorem. The separator theorem then gives feasibility of both restrictions, including
$$Y(T)=C(T)\cup B(T).$$
This is the correct place to use the restored-support clause. When  $I\setminus C(T)$  is removed, supports previously consumed by that part become mandatory again. The inherited theorem is specifically needed to show that those restored supports do not create a support/support conflict with  $C(T)\cup B(T)$ . Endpoint separation by itself would not be sufficient for that conclusion.The empty cases are as follows. $T=\varnothing$ :  $B(T)=D(T)=C(T)=Y(T)=\varnothing$ , and  $X(T)=I$ . $C(T)=I$ : the old exclusive part is empty and  $Y(T)=X(T)$ . $m=0$ , or there are no losing components: the only relevant selection is empty and the loss is zero. $T\neq\varnothing$  with  $D(T)=C(T)=\varnothing$ : this is the one case whose theorem convention should be made explicit. If the separator theorem permits an empty shared core, the argument is complete. Otherwise, add a direct lemma that a no-contact  $B(T)$  is feasible.The direct lemma is available if needed:  $X(T)=I\cup B(T)$  is feasible and there is no endpoint edge between  $I$  and  $B(T)$ . Removing  $I$ -endpoints cannot create a new occupied neighbor for a support that was already selected in  $X(T)$ . If a support was consumed by an  $I$ -endpoint and becomes restored, any  $B(T)$ -endpoint neighbor at that location would have created an  $I$ -to- $B(T)$  endpoint edge. Hence no restored support can acquire two  $B(T)$ -neighbors. That establishes feasibility of  $B(T)$  directly.2. Exact localization of  $R,N,G,\mu$ The localization identity
$$Q(X(T))-Q(I)=Q(Y(T))-Q(C(T))$$
is valid for  $Q\in\{R,N,G,\mu\}$ , provided it is read as an application of the inherited feasible-core valuation theorem.For  $R$ , the endpoint graph alone would not be enough to prove additivity, because  $R$  includes source mass together with event and mixed-full-tile terms. The inherited theorem supplies the needed inclusion-exclusion:
$$R(X(T))=R(I)+R(Y(T))-R(C(T)).$$
The event/full-tile accounting works in the usual three-way manner:terms supported entirely in the common core are counted in both restrictions and subtracted once;terms involving the core and  $B(T)$  occur in  $Y(T)$  and  $X(T)$ ;terms involving the core and  $I\setminus C(T)$  occur in  $I$  and  $X(T)$ ;terms requiring both exclusive parts are excluded by the separator theorem.Thus the equation is not being inferred from a raw endpoint-separation heuristic; it is an invocation of the previously established exact valuation theorem with the newly constructed core  $C(T)$ .For  $N$ , additivity is immediate at the level of source occurrences. The demand-hull argument requires the note’s stated convention that  $N$  counts positive source occurrences, not all source occurrences. Since  $H$  contains every positive owner of  $J$ , adding components outside  $H$  does not change  $N$ :
$$N(X(T))=N(H)=N(J).$$
If  $N$  were instead total source count, the claim in Section 3 that  $N(X(T))=N(J)$  would be false. The current note explicitly fixes the positive-occurrence meaning, so there is no defect under the inherited definitions.For  $G$ , the canonical gate theorem gives the needed incidence control. A marked producer/consumer incidence always uses adjacent endpoint roles. Therefore:an incidence cannot run from one new component  $B_i$  to another  $B_j$ , because that would connect the two components;an incidence cannot run from  $B(T)$  to  $I\setminus C(T)$ , because the old endpoint owner would then be in  $D(T)\subseteq C(T)$ ;a core-to-new incidence appears in both  $X(T)$  and  $Y(T)$ ;an old-core-to-old-exclusive incidence appears in both  $X(T)$  and  $I$ , so it cancels in the difference;uniqueness of the canonical gate consumer prevents duplicate-new-core marks.The demand hull hypothesis must be read in the inherited sense: it contains every producer relevant to a full-family marked side and its unique consumer. Under that convention,
$$G(X(T))=G(H)=G(J).$$
Then  $\mu=N+R-G$  gives the corresponding localization for  $\mu$ .3. The one-use aggregate loss boundLet
$$d_j=R(I\cup B_j)-R(I),$$
and let  $T$  contain only components with  $d_j<0$ . From the earlier component-affine valuation and the exact localization identity,
$$\begin{aligned}
\ell(T)
&=\sum_{j\in T}(-d_j)\\
&=R(I)-R(X(T))\\
&=R(C(T))-R(Y(T)).
\end{aligned}$$
This is the important localization step. Although the contact cores for different individual groups may overlap, the proof never assigns their reserves independently. It takes the entire selected collection  $T$ , constructs the single feasible core  $C(T)$ , and applies the ledger once to the single feasible family  $Y(T)$ .Activation is monotone under endpoint addition. Every positive singleton occurrence active in  $C(T)$  remains active in  $Y(T)$ , so
$$A(Y(T))\ge A(C(T)).$$
The exact ledger on  $Y(T)$  gives
$$2R(Y(T))
=A(Y(T))+U_0(Y(T))+Z_0(Y(T))+H(Y(T))
\ge A(C(T)).$$
Therefore
$$\begin{aligned}
2\ell(T)
&=2R(C(T))-2R(Y(T))\\
&\le 2R(C(T))-A(C(T)),
\end{aligned}$$
and hence
$$\ell(T)
\le R(C(T))-\left\lceil\frac{A(C(T))}{2}\right\rceil.$$
The ceiling form uses the inherited integrality of the reserve/loss quantities. Without that convention, the raw inequality with  $A(C(T))/2$  is the directly justified one; with the stated integer-valued loss model, the displayed ceiling strengthening is correct.This is a genuine simultaneous bound. It does not add
$$R(C(\{j\}))-\left\lceil A(C(\{j\}))/2\right\rceil$$
over individual groups, so no overlapping core is spent more than once. If  $C(T)=\varnothing$ , the ledger forces  $\ell(T)=0$ , exactly as it should for an independent feasible new group.The closure identity
$$C(T\cup U)
=\operatorname{cl}_J\bigl(C(T)\cup C(U)\bigr)$$
is also valid. It follows from
$$D(T\cup U)=D(T)\cup D(U)$$
and extensivity, monotonicity, and idempotence of the exact Horn closure. The note correctly avoids drawing any submodularity or reserve-monotonicity conclusion from this identity.4. The J24 raw-contact obstructionThe J24 witness is coherent and checks the claimed distinction between raw contact and feasible contact closure.For
$$I=\{V6,V8,V9\},\qquad B=J24\setminus I,$$
the new owners  $B$  form one connected endpoint group. The only old owners directly adjacent to  $B$  are  $V6$  and  $V8$ , so
$$D=\{V6,V8\}.$$
The point  $x=(-36,4)$  is an original V6 support. In the raw family  $D$ , it is not an endpoint of V6 or V8, so it remains mandatory. Its V6 anchor
$$a=(-35,4)$$
is occupied, and the V8 endpoint
$$b=(-36,3)$$
is also occupied. Thus  $x$  has two occupied neighbors and violates the complete-feasibility condition.In the full family, V9 has an original endpoint at  $x$ , so V9 consumes the V6 support and removes the conflict. Therefore the raw contact family is infeasible, while the closure must add V9:
$$\operatorname{cl}_{J24}(\{V6,V8\})
=\{V6,V8,V9\}=I.$$
The coordinate-shift certificate is internally consistent. With  $\rho=\text{physical row}+24$ , the support  $x=(-36,4)$  is  $(\rho,c)=(-12,4)$ , its own anchor is  $(-11,4)$ , and the V8 endpoint is  $(-12,3)$ . The table contains
$$6+12+8=26$$
selected support points for V6, V8, and V9, respectively. The stated 60 distinct endpoints and 30 disjoint original matching edges, together with the listed sole occupied neighbors, provide the finite feasibility certificate for  $I$ . This is a concrete physical obstruction to raw-contact budgeting, not a bounded enumeration standing in for the general proof.5. The H70 comparisonThe numerical comparison is correct:
$$R(H70)-R(J70)=48-24=24,$$
while the localized extension satisfies
$$R(C)-R(Y)=77-53=24.$$
Thus the smaller contact core can have a larger standalone reserve than the larger demand hull, while producing exactly the same signed extension loss after the relevant new group is attached. This correctly demonstrates that the localized inequality should not be rewritten as a monotonicity statement such as  $R(C)\le R(H)$ , nor as a direct proof of the remaining demand inequality.The note also correctly preserves the distinction between:the exact loss identity  $L=R(C)-R(Y)$ ;the local ledger bound  $L\le R(C)-\lceil A(C)/2\rceil$ ;the still-open target  $L\le\mu(H)$ .The local bound does not by itself pay the marked demand  $G(J)-N(J)$ .6. Source-minimal counterexamplesThe minimal-counterexample deductions are valid, with “source count” understood as total source-occurrence count rather than the positive-source quantity  $N$ .If  $H\subsetneq J$  is the canonical demand hull and  $\mu(J)<0$  is a counterexample of minimum total source count, then  $H$  is a smaller demand-preserving feasible family. Hence
$$\mu(H)\ge0.$$
Every added component must have  $d_j<0$ . If some  $d_j\ge0$ , removing  $B_j$  gives a proper complete feasible demand-preserving family with
$$\mu(J\setminus B_j)=\mu(J)-d_j<0,$$
contradicting minimality.Writing  $\ell_j=-d_j\ge1$ , the full family has
$$\mu(J)=\mu(H)-\sum_j\ell_j<0.$$
Under the inherited integer-valued margin convention,
$$\sum_j\ell_j\ge\mu(H)+1.$$
For any proper  $T$ ,  $X(T)$  has fewer source occurrences than  $J$ , remains demand preserving, and therefore must satisfy  $\mu(X(T))\ge0$ . Consequently,
$$\sum_{j\in T}\ell_j\le\mu(H).$$
This is exactly the “single actual core reserve competing across branches” structure described in the note. If  $H=J$ , there are no added components and this decomposition gives no further information, as correctly stated.Final assessmentThe package is acceptable as a written mathematical step under the inherited assumptions:the ambient closure is correctly shown to remain inside  $I$ ;support restoration is handled by the cited feasible-core separator theorem;the local family  $C(T)\cup B(T)$  is physically feasible;event, mixed-full-tile, and mark overlaps are localized by the inherited inclusion-exclusion theorem;all losses are charged once to the single aggregate contact core;the J24 obstruction is a valid witness that raw contact need not be feasible;the source-minimal inequalities are correct;no unclaimed reserve monotonicity, Hall assignment, full allocation, or grid-equality conclusion is being smuggled in.The only edit I recommend is to state explicitly that the separator theorem includes the empty shared core, or to add the direct no-contact proof for  $D(T)=C(T)=\varnothing$ . If that convention is already part of the inherited theorem, the verdict is ACCEPT with no substantive remaining mathematical defect.
