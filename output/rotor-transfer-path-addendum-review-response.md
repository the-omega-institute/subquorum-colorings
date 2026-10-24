ACCEPT. Both new exclusions follow from the unchanged source model and the accepted rotor theorem. The wall/bar dichotomies cover all permitted lengths, including equality and the minimum dimensions. The second application of the rotor theorem in Theorem 4 is valid for the same actual rotor, with its original matching and supports.Throughout, “P followed by S/R” has its existing meaning in the side-occurrence graph: the second edge uses the incident side identified by the first P transfer’s target. No switch to the recipient’s opposite leg is made.I did not use the earlier verdict, the reported coordinate controls, or the Lean status as evidence for these new conclusions.1. The earlier P transverse source supplies both complete endpoint intervalsLet  $B$  be the recipient of the P transfer. Write the earlier transverse source as  $C_P=U(V,h,f)$ , to distinguish it from any transverse sources subsequently forced by R transfers.The change to  $B$ ’s coordinates is correct. From
$$T(r,c)=(c+2,r+2),\qquad
T^{-1}(x,y)=(y-2,x-2),$$
and the transverse frame in the preceding producer’s coordinates,
$$(r,c)\longmapsto(c+1,h+2-r),$$
one obtains
$$\Phi_h(r,c)=(h-r,c-1).$$
The original near column of  $U(V,h,f)$  contains every point
$$(r,1),\qquad 0\le r\le h.$$
Here  $r=0,1$  are bar corners, and  $2\le r\le h$  is the leg. Its image is therefore the uninterrupted endpoint interval
$$\boxed{\{(s,0):0\le s\le h\}.}$$
In particular, there is no missing point at the leg/bar junction.The original row-one bar similarly gives
$$\boxed{\{(h-1,c):0\le c\le V-1\}.}$$
The first P transfer supplies
$$h\ge a+2\ge6,\qquad V\ge6.$$
These lower bounds suffice for every witness used below. The far-leg length  $f$  does not affect either interval.2. Theorem 3: universal P→S impossibilityThe hypothetical S consumer’s incident frame is
$$S_b(r,c)=(b+3-r,3-c).$$
Its original endpoint  $(1,3)$  exists at every allowed width and maps to
$$S_b(1,3)=(b+2,0).$$
Its original near column, including both bar corners, maps to
$$\boxed{\{(s,2):3\le s\le b+3\}.}$$
There are exactly two alternatives.Case 1:  $b+2\le h$ Since  $b\ge4$ ,
$$0\le b+2\le h.$$
Thus the S bar endpoint
$$(b+2,0)$$
lies on  $C_P$ ’s column-zero endpoint interval.Equality  $b+2=h$  is included. The collision then occurs at  $C_P$ ’s bar corner, which is an original endpoint.Case 2:  $b+2>h$ The first P transfer gives  $h\ge6$ , hence
$$h-1\ge5\ge3.$$
The case assumption also gives
$$h-1<b+1<b+3.$$
Consequently the S consumer’s column-two interval contains
$$(h-1,2).$$
The transverse source’s bar contains the same point because
$$0\le2\le V-1.$$
Thus this case also produces an endpoint collision.Owner identity and quantifiersThe S consumer is a positive U, whereas  $C_P$  is the actual negative U supplied by the P transfer. They cannot be the same source occurrence. Identifying the hypothetical S consumer with some earlier positive producer does not help: it would still have the displayed collision with  $C_P$ .The two cases exhaust every allowed  $b,h$ . No parity argument is needed for this dichotomy, and additional sources cannot remove either owner’s original endpoints.Therefore
$$\boxed{\text{No P edge can be followed by an S edge.}}$$
The retained necessary gap is consistent with this stronger result. Indeed, its bound  $b\le h-6$  already puts  $(b+2,0)$  strictly inside the newly identified wall. The two-case proof establishes the contradiction directly without relying on that earlier gap.The proof uses the source model’s fixed minimum dimensions; it requires no upper dimensional cutoff.3. Theorem 4: a length-four companion really forces a second R stepSuppose a P transfer is followed by an R transfer from  $B$ , and suppose that R transfer’s positive companion  $D$  has incident length  $g=4$ .In  $B$ ’s coordinates,
$$V_4(r,c)=(c+2,7-r).$$
The canonical gate of the relevant side of  $D$  is
$$V_4(3,2)=(4,4),$$
which is an endpoint of the existing rotor  $B_0$ .This is genuinely a gate of  $D$ : its inverse image  $(3,2)$  is  $D$ ’s original canonical support position, not one of  $D$ ’s original endpoints. The established canonical-gate equivalence therefore makes that side marked, and unique endpoint ownership identifies the existing rotor as its consumer.Unique consumption identifies an owner separately at each gate. These two distinct gates can have the same rotor owner.The full rotor constructor is preserved in  $D$ ’s frameThere is no hidden orientation or chirality change. The inverse frame is
$$V_4^{-1}(x,y)=(7-y,x-2),$$
and
$$V_4^{-1}(B_0)=B_0.$$
More explicitly,  $V_4$  is the quarter-turn about the rotor’s center. It cycles its four tips as
$$(3,2)\longmapsto(4,4)\longmapsto(6,3)
\longmapsto(5,1)\longmapsto(3,2),$$
and its corresponding central endpoints as
$$(4,2)\longmapsto(4,3)\longmapsto(5,3)
\longmapsto(5,2)\longmapsto(4,2).$$
Thus it preserves the four original central-to-tip matching edges.It also preserves the original support set. Its two support cycles are
$$(2,2)\longmapsto(4,5)\longmapsto(7,3)
\longmapsto(5,0)\longmapsto(2,2)$$
and
$$(3,1)\longmapsto(3,4)\longmapsto(6,4)
\longmapsto(6,1)\longmapsto(3,1).$$
The map preserves the aligned physical tiles. Accordingly, the complete family in  $D$ ’s coordinates satisfies the same hypotheses, with the same rotor constructor and its unchanged support and matching roles.The accepted rotor theorem can therefore be applied again.No additional lower bound on  $D$ ’s width needs to be assumed before this application. The rotor producer’s width bound is a conclusion of that theorem. If the hypothesized  $D$  had insufficient width, the second application would already give a contradiction.4. The second companion frame and endpoint memberships are correctThe second application forces a positive companion  $E$ , with even incident length  $k\ge4$ , whose frame in  $D$ ’s coordinates is  $V_k$ . In  $B$ ’s coordinates,
$$\begin{aligned}
(V_4\circ V_k)(r,c)
&=V_4(c+2,k+3-r)\\
&=(k+5-r,5-c).
\end{aligned}$$
This is exactly equation (11).Write  $E=U(s,k,e)$ , with  $s\ge6$ .Its original bar endpoint  $(1,5)$  maps to
$$\boxed{(k+4,0).}$$
This is the relevant original endpoint behind the asserted bar witness. Column five exists at the minimum allowed width six.Its entire original near column, including the two bar corners, maps to
$$\boxed{\{(u,4):5\le u\le k+5\}.}$$
The lower endpoint  $u=5$  is  $E$ ’s terminal. It is included, not an open endpoint of a stem interval.These memberships require no restriction on  $E$ ’s far-leg length.5. The second wall/bar dichotomy covers every length and boundary caseUse the earlier P source  $C_P$ , whose two endpoint intervals were established in §1 above.Case 1:  $k+4\le h$ Because  $k\ge4$ ,
$$0\le k+4\le h.$$
The E bar endpoint
$$(k+4,0)$$
therefore belongs to  $C_P$ ’s column-zero wall.Equality  $k+4=h$  is covered: the witness lies at  $C_P$ ’s bar corner.Case 2:  $k+4>h$ Since  $h\ge6$ ,
$$h-1\ge5.$$
The case assumption gives
$$h-1<k+3<k+5.$$
Hence
$$(h-1,4)$$
belongs to  $E$ ’s column-four endpoint interval.It also belongs to  $C_P$ ’s bar, since
$$0\le4\le V-1$$
follows from  $V\ge6$ .At the minimum height  $h=6$ , this witness is
$$(5,4),$$
exactly the included terminal endpoint of  $E$ . There is no lower-endpoint escape. At  $V=6$ , column four is also within the transverse bar.The two alternatives are exhaustive and use no rounding.The contradiction does not require E to be a previously unseen positive ownerThe earlier P transverse source  $C_P$  is negative, while the forced companion  $E$  is positive. They are necessarily distinct actual owners.That is the only owner distinction needed for either collision. If an earlier positive source were proposed as the source realizing  $E$ , it would still have to own the displayed E endpoints and would still collide with  $C_P$ . Nor does the proof need to assume that all negative transverse roles are realized by different owners.Thus every possible realization of the forced companion contradicts endpoint disjointness, and
$$\boxed{g=4\text{ is impossible after P}\to\text{R}.}$$
6. The stated lower bounds follow, with the two heights kept distinctAllowed incident lengths are even and at least four. Excluding four gives
$$\boxed{g\ge6.}$$
Now let  $h_R$  denote the transverse height of the first R step, and let  $W$  be the width of the intermediate producer  $B$ . The accepted rotor theorem gives
$$g\le h_R-4,\qquad h_R\le W-4.$$
Therefore
$$g\le W-8$$
and
$$\boxed{W\ge g+8\ge14.}$$
The height  $h$  used in the collision proof belongs to the earlier P transverse source. The height  $h_R$  used in this final width deduction belongs to the R transfer. The argument does not conflate them.The width-at-least-fourteen conclusion applies to the intermediate positive producer  $B$ , as stated.Verdict scopeTheorems 3 and 4 are accepted as written mathematical exclusions. The new argument rules out every complete P→S configuration and every P→R configuration whose first R companion has incident length four.The second proof depends on the preceding P source’s occupied wall and bar. It therefore supplies no exclusion of R→R paths lacking that preceding P configuration. It also supplies no complete realization of the remaining PR/R cases, no execution certification, and no full reserve or grid theorem.
