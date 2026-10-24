ACCEPTThe exclusion lemma is correct, and it strengthens the distinct-owner conclusion to
$$\Phi(I)\ge \Phi(Q,D,W)+3,
\qquad
A\subseteq I\subseteq G,\qquad |I\setminus A|\le2.$$
Every collision coordinate checks. The north-terminal catalogue is exhaustive under the full-source model, and the exclusion applies independently of the consumer at  $t$ . The argument covers all legal breadths and far-leg lengths without using finite enumeration as a proof.1. The support  $p$  must have an additional actual consumerThe point
$$p=(a+2,w+12)$$
has intrinsic  $V$ -coordinates  $(8,0)$ . Since  $8$  is even and the near leg of  $V$  has length  $8$ , this is exactly a prescribed outward original support.The assertion that  $p$  is absent from every retained endpoint set is correct. Its intrinsic coordinates are:OriginalIntrinsic coordinates of  $p$  $Q$  $(-w-1,9)$  $D$  $(4,w+7)$  $L$  $(2,w+6)$  $C$  $(4,6)$  $E$  $(2,5)$  $W$  $(11,1)$  $T_0$  $(6,-1)$  $V$  $(8,0)$ Proposed  $K$  $(10,3)$ None satisfies the corresponding endpoint definition. In particular, for  $K$ , row  $10$  is outside the bar and the near stem, while column  $3$  cannot be its far-stem column because  $h\ge6$ . This remains true however large  $f$  is.The three asserted foreign endpoint neighbors are also correct:Neighbor of  $p$ Retained originalIntrinsic coordinates $(a+2,w+11)$ , west $V$  $(8,1)$  $(a+2,w+13)$ , east $E$  $(2,6)$  $(a+3,w+12)$ , south $E$  $(1,5)$ These are retained endpoints, so all three remain in  $O$ . If  $p$  were unconsumed, the requirement of exactly one  $O$ -neighbor would fail. Completeness therefore forces an actual original  $J$  to contain  $p$ .Because  $p$  belongs to none of the endpoint sets of  $A$  or  $K$ , this consumer is distinct from all those originals. Its matching partner cannot be any of the three listed endpoints. Endpoint disjointness also prevents any of those sites from being an own endpoint neighbor of  $J$ .Thus the own-neighbor set of  $J$  at  $p$  is exactly
$$\{\text{north}\}.$$
The fact that two blockers belong to the same original  $E$  causes no difficulty: both are foreign to the actual consumer  $J$ .2. The north-terminal charts are exhaustiveIn the prescribed U endpoint graph, the only endpoints having one own endpoint neighbor are the two leg terminals. In the rotor, they are precisely the four tips.For a U consumer, full-source leg relabeling permits the incident leg to be designated the near leg. As established in the accepted proof, the reflection
$$(r,c)\longmapsto(r,H+1-c)$$
exchanges the legs while preserving the complete matching and support data under the corresponding parameter exchange.Once  $p$  is the near terminal and its inward direction is north, the intrinsic row direction is fixed. The intrinsic column direction can point east or west, giving exactly
$$J_R(r,c)=(a+2-d+r,\;w+11+c)$$
and
$$J_L(r,c)=(a+2-d+r,\;w+13-c).$$
In each case, the terminal  $(d,1)$  maps to  $p$ . These charts cover a terminal originally designated either near or far; they do not replace or modify the actual original.For completeness, the two north-terminal rotor images at  $p$  can be written as
$$\mathcal R_-(r,c)=(a-2+r,\;w+9+c),$$

$$\mathcal R_+(r,c)=(a-2+r,\;w+15-c).$$
Both place the standard tip  $(4,3)$  at  $p$ , with its own neighbor north. Full-source quarter-turn invariance reduces all four possible canonical tips to these two reflected images.There is no additional corner or nonterminal-stem case: those roles have more than one own endpoint neighbor.3. Every proposed consumer has the claimed collisionU consumers with  $d\ge10$ For either  $J_R$  or  $J_L$ , take
$$x=(a-7,w+12).$$
Its consumer coordinates are
$$(r,c)=(d-9,1).$$
At  $d=10$ , these are  $(1,1)$ , a bar endpoint.For legal even  $d\ge12$ ,
$$3\le d-9\le d,$$
so this is a near-stem endpoint.The same point has  $K$ -coordinates
$$(1,3),$$
which is a bar endpoint for every legal  $h\ge6$ .Thus both orientations collide with  $K$  for every legal  $d\ge10$ . Neither breadth nor far-leg length can remove this collision.Right-oriented U consumers with  $d\in\{4,6,8\}$ Take
$$x_R=(a+3-d,w+14).$$
Its  $J_R$ -coordinates are
$$(1,3),$$
so it is always a bar endpoint.Its  $K$ -coordinates are
$$(11-d,1),$$
namely
$$(7,1),\quad(5,1),\quad(3,1)$$
for  $d=4,6,8$ , respectively. All lie in the retained near stem of  $K$ , whose length is  $8$ .This gives the required collision for every remaining legal incident depth in the right orientation.Left-oriented U consumers with  $d\in\{4,6,8\}$ Take
$$x_L=(a+3-d,w+11).$$
Its  $J_L$ -coordinates are
$$(1,2),$$
again a bar endpoint for every legal  $H\ge6$ .Its  $V$ -coordinates are
$$(9-d,1),$$
namely
$$(5,1),\quad(3,1),\quad(1,1).$$
The first two are near-stem endpoints of  $V$ , and the last is a bar endpoint.The collision therefore holds in both residual families, independently of  $z$ . In particular, allowing the old far leg to be arbitrarily long introduces no missing case: this argument uses only  $V$ ’s fixed bar and near stem.Both north-terminal rotorsThe common collision point is
$$p+(-2,1)=(a,w+13).$$
Using the explicit rotor charts above, its standard rotor coordinates are:Rotor imageCoordinates of  $(a,w+13)$  $\mathcal R_-$  $(2,4)$  $\mathcal R_+$  $(2,2)$ Both are standard rotor endpoints. Its  $E$ -coordinates are
$$(4,6),$$
the retained far-leg terminal of  $E$ .Thus both rotor choices collide with  $E$ .Exhaustion and the complete-family contradictionThe legal incident depths are the even integers  $d\ge4$ , partitioned by
$$d\in\{4,6,8\}\quad\text{or}\quad d\ge10.$$
Both U orientations are covered in every case, and both rotor choices are covered.Consequently, completeness requires an actual consumer of  $p$ , while every possible consumer shares an endpoint with  $K$ ,  $V$ , or  $E$ . Since  $p$  is absent from those originals, the consumer cannot be identified with the blocking original. Each shared endpoint is therefore a genuine violation of original endpoint disjointness.This proves the exclusion lemma. The proof never uses the owner of  $t$ , and further originals cannot remove any of the retained blocking endpoints.4. The revised baseline excess is at least  $3$ Let
$$\Phi_0=\Phi(Q,D,W).$$
The accepted baseline identity remains
$$\Phi(A)=\Phi_0-1.$$
On the distinct-owner branch, the accepted proof gives the following alternatives.A U owns  $t$ The existing exact receipts give
$$\Delta\Phi(J_N\mid A)=h-1,\qquad
\Delta\Phi(J_S\mid A)=h-2.$$
Since  $h\ge6$ , either orientation contributes at least  $4$ . Hence
$$\Phi(A+J)\ge \Phi_0+3.$$
A rotor owns  $t$ The accepted classification forces the distinct actual owner of  $e$  to be a north-terminal U, with exact increment
$$h-1-k\,\mathbf 1_{\{\text{left orientation and incident depth }8\}}.$$
The newly excluded family is exactly the exceptional family in this formula:
$$K_L\text{ with }d=8
\quad\Longleftrightarrow\quad
U(h,8,f),\qquad
(r,c)\mapsto(a-8+r,w+15-c).$$
Thus the indicator vanishes in every complete family retaining  $A$ , and the actual upper U contributes
$$h-1\ge5.$$
The resulting bounds are:Actual owner of  $t$ Its incrementUpper-U incrementTotal gain over  $\Phi(A)$ Excess over  $\Phi_0$ East-terminal UAt least  $4$ —At least  $4$ At least  $3$  $R_N$  $0$ At least  $5$ At least  $5$ At least  $4$  $R_S$  $-1$ At least  $5$ At least  $4$ At least  $3$ Therefore the uniform distinct-owner conclusion is precisely
$$\boxed{\Phi(I)\ge\Phi(Q,D,W)+3.}$$
The same actual-original selection from the accepted theorem applies:In the U branch, select  $A$  and the actual owner of  $t$ .In the rotor branch, select  $A$  and the distinct actual owners of  $t$  and  $e$ .Thus  $I\subseteq G$  and  $|I\setminus A|\le2$ . The consumer of  $p$  is used only in the contradiction excluding the exceptional  $K$ ; it is not an additional compensator that must be inserted into  $I$ .The common-owner branch continues to use the previously accepted baseline bound.5. The old partial receipt and the verification scope remain consistentThe former partial inventory
$$k=w+8,\qquad z=4,\qquad
R_S,\qquad K=U(w+12,8,4)$$
still has the accepted exact gain
$$\Delta\Phi(R_S,K\mid A)=2.$$
Its four directed events per shared  $V$ -tile and its total width debit are unchanged.The exclusion lemma now proves that no complete family can retain  $A$  and this  $K$ . Hence no complete family can retain the larger prefix  $A+R_S+K$ . This is fully consistent with the previous acceptance, which established its partial-inventory accounting without asserting complete extendibility. It cannot demonstrate sharpness of the complete-family bound.The general proof is the forced-consumer argument, exhaustive chart classification and parameter-uniform collision certificates above. The reported finite controls can corroborate those statements, and local Lean declarations can establish their encoded coordinate and arithmetic facts. I am not certifying their execution or independently checking the newly reported declaration count.There is no blocking flaw in the strengthening. The larger single-package margin does not itself assign compensators across different packages or control the remaining inter-package directed events; those remain the separate obligations stated in the note.
