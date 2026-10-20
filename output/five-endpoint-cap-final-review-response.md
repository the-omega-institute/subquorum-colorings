ACCEPTThe final corrected package closes the remaining mathematical obligations identified in the earlier reviews. Under the inherited source model and the exact reserve ledger, the written geometric claims in Sections 1–4 are now valid.This acceptance is limited to the stated scope: it does not certify the complete Lean development, nonvacuous fixture coverage, the unrestricted allocation inequality  $\mu\ge0$ , or the rectangular-grid equality.1. Cap semantics and the five-endpoint theoremThe definition of  $P$  now has the required meaning:
$$P=\bigcup_{\text{all selected source occurrences}} E_{\text{occurrence}},$$
including added U and rotor sources. The prescribed source ownership remains fixed, while an added source may contribute a new endpoint that consumes an original support. The set  $T$  contains supports outside  $P$ , and the at-most-one occupied-neighbor condition applies to retained support points in  $T$ , not to endpoint points in  $P$ .This removes the previous ambiguity.For
$$x=(2,2)$$
and
$$B=\{(1,2),(2,1),(3,2),(2,6),(1,4)\},$$
the points  $(1,2),(2,1),(3,2)$  are three occupied neighbors of  $x$ . If  $x\notin P$ , it remains a mandatory support in  $T$  and violates the support-neighbor condition. Hence  $x\in P$ , and because no prescribed source owns it as an endpoint, an added source must own it.The only available lattice neighbor not already occupied by a prescribed endpoint is
$$y=(2,3).$$
The source-local matching rule therefore forces  $x$  and  $y$  to be endpoints of the same added source.For a U, an endpoint with exactly one same-source endpoint neighbor is a terminal tip. The minimum even leg height gives the endpoint at
$$x+4(y-x)=(2,6),$$
which conflicts with the prescribed endpoint  $(2,6)$ .For a rotor, the two complete normalized role sets compatible with  $x$  and  $y$  both contain  $(1,4)$ , which also conflicts with a prescribed endpoint.The cap is therefore a full source-class argument. It does not depend on a finite translation window, a bounded source count, or pairwise-feasibility assumptions.2. Singleton activation and the  $A$ -injectionThe revised activation definition is the correct one. An original singleton occurrence  $C=(j,Q)$  is activated exactly when
$$(T_j\cap Q)\cap P\ne\varnothing,$$
independently of the identity of the source that owns the endpoint in  $P$ .In the normalized gate configuration, the support
$$p=(2,2)$$
has occupied neighbors  $t=(3,2)$  and  $(2,1)$ . If  $p\notin P$ , it remains a mandatory support with at least two occupied neighbors, which is impossible. Thus  $p\in P$ , and the consumer singleton occurrence is activated.The map from marked sides to activated occurrences is now well-defined:
$$\text{marked side}\longmapsto
(\text{consumer source},\text{physical tile}).$$
The statement that the target occurrence uses the same physical tile  $Q$  as the producer canonical side is sufficient. Since  $t$  is the consumer’s sole relevant endpoint and lies in  $Q$ , the physical tile of the target occurrence is fixed. If two marked sides produced the same target occurrence, their producer canonical physical tiles would coincide. The established distinctness of the original positive donor tiles then identifies the two original sides.Consequently,
$$q_+\le A.$$
The ledger calculation is correct:
$$2R
=q_+ +(A-q_+)+U_0+Z_0+H
\ge q_+,$$
and therefore
$$R\ge \left\lceil\frac{q_+}{2}\right\rceil,
\qquad
\mu
\ge
N-G+\left\lceil\frac{q_+}{2}\right\rceil.$$
The note also correctly avoids double-counting:  $q_+$  is a subset of the existing  $A$ -term, not an additional reserve term. The zero-rotor caveat is consistent with the stated forwarding cancellation.3. Forced transverse negative UThe new all-width consequence is valid.The revised text explicitly assumes that
$$p=(2,2)$$
is not already an endpoint of the prescribed producer or consumer. The three persistent endpoint neighbors are therefore
$$(1,2),\quad (2,1),\quad (3,2),$$
and  $p$  must be covered by a third source.The only possible same-source neighbor for that new endpoint is
$$(2,3).$$
The rotor alternatives are excluded by the two normalized outer-role sets, both of which contain  $(1,4)$ . Thus the third source is a U whose terminal tip is  $p$  and whose stem points right.If  $h$  is the corresponding even leg height, the stem contains
$$(2,2+j),\qquad 0\le j\le h.$$
The producer has endpoint  $(2,w)$ , so endpoint disjointness gives
$$h<w-2.$$
Since  $h$  and  $w$  are even and  $h\ge4$ ,
$$4\le h\le w-4,$$
and therefore
$$w\ge8.$$
The sign conclusion is also valid under the stated positive profile catalogue. The forced source has  $p$  and  $(2,3)$  in the same physical tile, whereas a positive U terminal is a regular singleton. Hence the forced source is negative.The revised wording correctly preserves the original producer and consumer endpoint ownership while identifying the third source that newly consumes  $p$ .4. Width-six positive-U exclusionThe positive profile classification is now complete. $1P2T$ This is excluded by the five-endpoint cap. $2P1T$ If the second endpoint is  $p=(2,2)$ , then the producer owns both outside neighbors  $(1,2)$  and  $(2,1)$ . The point  $p$  has only  $t$  as a same-source endpoint neighbor, so it would have to be a terminal tip. The positive catalogue assigns terminal tips the singleton profile, not  $2P1T$ .If the endpoints are  $\{t,u\}$ , then the only support choices are  $p$  and  $r=(2,3)$ .Support  $p$  gives the five-endpoint cap.Support  $r$  makes  $p$  blank. The displayed normalized continuation table covers all regular pairs: both bar-end orientations and both stem orientations. In every blank-side case, reflection of the paired neighbor through the endpoint yields another original endpoint. Applying this to  $t,u$  produces  $(3,1)$ , the producer anchor, contradicting endpoint disjointness.The continuation ranges include the final regular pair before a terminal singleton, so the arbitrary even-height boundary cases are covered. $4P0T$ The horizontal-bar argument is valid for width six: a length-at-least-six interval containing columns  $2,3$  must contain column  $1$  or  $6$ , and hence meets a producer stem at row  $2$  or  $3$ .The vertical-bar argument is also now valid without any parity restriction. If the long-axis interval is
$$[L,L+v-1],\qquad v\ge6,$$
and contains rows  $2,3$ , then  $L\le2$ .If  $L\le1$ , the bar contains row  $1$ , producing an endpoint collision at  $(1,2)$  or  $(1,3)$ .If  $L=2$ , a U leg is attached at the row-two bar end. By the normalized U geometry, a left-going leg reaches  $(2,1)$ , while a right-going leg is attached at the outward column and reaches  $(2,6)$  with leg height at least four.Thus every positive  $4P0T$  placement is excluded for a width-six producer. This proof is invariant under the allowed translations, reflections, and rotations.Therefore every positive-to-positive gate incidence has producer width at least eight.5. Rotor gate-owner rolesThe rotor role argument is now complete.The producer endpoint subset
$$\{(1,1),(1,2),(1,3),(1,4),(2,1),(3,1),(4,1)\}$$
is sufficient to reject fourteen of the sixteen endpoint roles placed at
$$t=(3,2).$$
The only roles avoiding this set are
$$R_+(2,0)
\quad\text{and}\quad
R_-(1,6).$$
The displayed reference support set is
$$\{(0,2),(1,1),(2,5),(1,4),(5,3),(4,4),(3,0),(4,1)\}.$$
For  $R_+(2,0)$ , the inverse image of  $p=(2,2)$  is
$$(0,2),$$
which is a reference support.For  $R_-(1,6)$ , under
$$(r,c)\mapsto(r+1,-c+6),$$
the inverse image of  $p=(2,2)$  is
$$(1,4),$$
which is also a reference support.Thus both surviving rotor gate-owner roles have original support  $p$ . The forced transverse-U argument then applies, giving
$$w\ge8.$$
Hence no rotor can consume a width-six positive gate.Combining this with the positive-U exclusion gives the claimed conclusion:
$$\boxed{\text{Every actual gate consumer of a width-six positive source is a negative U.}}$$
This is a statement about actual fixed gate consumers. It does not assert a global sign restriction for wider producers, directed acyclicity, or any allocation theorem.Final dispositionThe written geometric package is ACCEPTED under the inherited source model and exact reserve ledger.The accepted results are:the full five-endpoint cap for arbitrary finite U/rotor extensions;the owner-independent occurrence-level singleton activation injection;the forced transverse negative U and the bound  $4\le h\le w-4$ ;the exclusion of all positive  $1P2T$ ,  $2P1T$ , and  $4P0T$  consumers at width six;the complete sixteen-role rotor gate analysis;the conclusion that every actual width-six gate consumer is a negative U.The stated limits remain in force: this does not prove nonvacuous singleton witness coverage, the complete global/isometry/profile adapters, the unrestricted allocation inequality  $\mu\ge0$ , or rectangular-grid equality.
