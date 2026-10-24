# Independent review — negative cavity and all-width six-source family

Task 26cbc972-3663-4e3d-bccc-a6fa5eb56149. Verdict ACCEPT. It additionally derives the complete-family exclusion of even B, now incorporated. The subsequent third-right repair theorem is outside this input. This review does not certify executions, full formalization, realizability, novelty or the unrestricted target.

ACCEPTThe bar-window theorem, strict  $h\ge t+2$  consequence, tight-width exclusion, and all-width six-source obstruction are correct as the necessary statements expressly claimed. The accounting after adding  $E$  is also correct, including the exclusions for consumed original supports and original full tiles.There is one useful strengthening concerning the word actual: the even- $B$  phase cannot occur in a complete family. Its charge formula  $1-J$  is correct for the endpoint-disjoint coordinate configuration, but completeness at its next axial support excludes that configuration. Thus an actual cavity consumer in a complete family necessarily has odd  $B$ , charge  $-1$ , and its terminal at  $(a,w+8)$ ; the cavity point  $s$  is then a straight leg interior.This strengthens the note rather than contradicting its stated necessary theorem: the note expressly does not claim realizability of both phases. I would make this distinction explicit.1. The shared original support and its forced ownerWrite  $V_X$  for the original endpoint set of owner  $X$ . The constructor gives
$$V_{U(J,g,z)}
=
\bigl(\{0,1\}\times\{1,\ldots,J\}\bigr)
\cup
\bigl(\{2,\ldots,g\}\times\{1\}\bigr)
\cup
\bigl(\{2,\ldots,z\}\times\{J\}\bigr).$$
In particular, every original endpoint has at least one adjacent endpoint belonging to its own original owner.The claimed shared support is
$$s=(a+1,w+8).$$
For  $D$ , it is the original support with intrinsic coordinates
$$(3,w+3),$$
whose anchor is
$$D(3,w+4)=(a+1,w+9).$$
For  $C$ , it is the original support with intrinsic coordinates
$$(h-1,2),$$
whose anchor is
$$C(h-1,1)=(a+1,w+7).$$
These support incidences are valid because  $t,h\ge4$  are even: intrinsic rows  $3$  and  $h-1$  are odd leg rows in the support catalogue.The two anchors are distinct occupied endpoints. The support  $s$  cannot remain unconsumed in a complete family.It is absent from all four prescribed endpoint sets:Q’s endpoint columns are at most  $11$ .At row  $a+1$ , D has only its stem columns  $6,w+9$ .L’s endpoint columns are at most  $w+6$ .At row  $a+1$ , C has its near stem at  $w+7$ , and possibly its far stem at  $w+K+6$ ; its bar begins no earlier than row  $a+3$ .Therefore its actual consumer  $E$  is distinct from  $Q,D,L,C$ . It may already be an owner elsewhere in the complete family; the argument supplies no separate “fresh activation” credit.2. Exhaustion of U and rotor roles at  $s$ The west and east neighbors of  $s$  already belong to  $C$  and  $D$ . Thus E’s own endpoint neighbors at  $s$  can only be north and south.U roles, including straight interiorsThe original U graph has:RoleOwn endpoint neighborsLeg terminalOneStrict leg interiorTwo oppositeOuter bar cornerTwo perpendicularOther bar or junction roleThreeConsequently, the surviving U possibilities are exactly vertical terminals and strict vertical leg interiors.A corner cannot fit because its neighbors are perpendicular. A degree-three role cannot fit because only two directions remain available. A transposed bar interior does not provide an omitted degree-two role: its original degree is still three.Retaining the straight-interior possibility is essential. It becomes the actual surviving role in the complete-family conclusion below.Rotor rolesRotor nontips have degree three and cannot fit. The four vertical-tip possibilities are blocked uniformly:Each north-tip form has a mandatory endpoint at relative position  $(-2,1)$  or  $(-2,-1)$ , on D’s lower bar at row  $a-1$ . In fact, both forms also contain  $(-2,0)$ , which gives the same exclusion.The south-tip forms have the stated mandatory endpoints  $(2,-1)$  and  $(1,-1)$ , giving
$$(a+3,w+7),\qquad (a+2,w+7).$$
Both belong to C’s original near stem or its bar junction.The last assertion remains valid at  $h=4$ : row  $a+3$  is then C’s first bar row, and its near-column endpoint still exists.Thus every rotor possibility is excluded by mandatory original endpoints, independently of any upper dimension bound.3. The physical frame and the exact windowLet the incident leg of E be the one containing  $s$ . Its physical column is necessarily  $w+8$ .Because  $s$  is a terminal or strict leg interior, its intrinsic leg index is at least  $2$ . This excludes both the outer corner at intrinsic row  $0$  and the junction at row  $1$ .The bar cannot be above  $s$ If the bar were above  $s$ , its outer row would be at or above  $a-1$ . The incident leg is a continuous endpoint segment from the bar to  $s$ , so it would contain
$$(a-1,w+8)\in V_D.$$
That contradicts endpoint disjointness.Hence the bar lies below  $s$ . Write its outer row as  $B$ , so its two rows are  $B-1,B$ . Initially this gives  $B\ge a+3$ .The bar cannot pass C’s first bar rowC contains the endpoint
$$(a+h-1,w+8).$$
The incident leg of E connects  $s$  to its bar along this same column. Therefore it cannot reach that row:
$$B\le a+h-2.$$
The bar cannot point leftA left-pointing bar would contain column  $w+7$ , for example at row  $B-1$ . The bounds already obtained place that row inside C’s near-stem interval:
$$a+2\le B-1\le a+h-3.$$
C owns every point in column  $w+7$  from row  $a$  through row  $a+h$ . This gives another collision.Therefore the bar points right, and after naming the incident leg as the first leg, the unique canonical frame is
$$E=U(J,g,z),\qquad
E(r,c)=(B-r,w+7+c).$$
Here “unique” correctly means the orientation and coordinate presentation of the fixed actual owner. It does not mean that all hypothetical completions must choose the same  $B,J,g,z$ .The lower bound on  $B$ Both bar rows cross D’s far-stem column  $w+9$ . D occupies that column through row  $a+t-2$ .Since the bar is below  $s$ , avoiding that stem requires
$$B-1>a+t-2,$$
and hence
$$B\ge a+t.$$
Combining the bounds gives exactly
$$\boxed{a+t\le B\le a+h-2.}$$
The incident-leg windowThe near terminal is at row  $B-g$ .It cannot be at or above row  $a-1$ , because the continuous incident leg would then contain D’s endpoint  $(a-1,w+8)$ . Thus
$$B-g\ge a.$$
Since the leg contains  $s$ ,
$$B-g\le a+1.$$
Equivalently,
$$\boxed{B-a-1\le g\le B-a.}$$
The bar window immediately implies
$$\boxed{h\ge t+2.}$$
Thus the nominal case  $h=t$  admits no complete extension retaining these prescribed original owners. The endpoint-disjoint algebraic package identity at  $h=t$  remains valid; completeness is what fails.No equality between the independent far legs  $f,z$  has been used.4. Legal parity and both charge formulasBecause  $a$  is odd and  $g$  is even, the two adjacent integers in the  $g$ -window give precisely:Parity of  $B$ Incident length  $g$ Near terminalRole of  $s$ Odd $B-a$  $(a,w+8)$ Strict interior, intrinsic row  $g-1$ Even $B-a-1$  $s$ Terminal, intrinsic row  $g$ The legal lower bound  $g\ge4$  is respected. In the odd case,  $g\ge t$ . In the even case,  $a+t$  is odd, so  $B\ge a+t+1$ , again giving  $g\ge t$ .For an independent charge reconstruction, put
$$\lambda=\frac{g+z}{2}.$$
The original matching-edge count is
$$M_E=J-1+\lambda.$$
Let  $T_E$  count endpoint-touched tiles, and  $A_E$  count original supports in those tiles. Directly from the constructor:Phase $T_E$  $A_E$ Original full tilesOriginal charge $B$  odd $J/2+\lambda$  $\lambda$  $J/2$  $-1$  $B$  even $J+\lambda-2$  $\lambda-2$  $0$  $1-J$ For odd  $B$ , the bar occupies one aligned tile row. The support count comprises two axial terminal supports and
$$(g/2-1)+(z/2-1)=\lambda-2$$
odd-row inward lateral supports.For even  $B$ , the two bar rows occupy different tile rows. Intrinsic row  $2$  already shares a tile row with bar row  $1$ , accounting for the subtraction of two in the tile count. Neither axial terminal support belongs to an endpoint-touched tile; only the  $\lambda-2$  inward lateral supports contribute.Therefore
$$q_E=(J-1+\lambda)+\lambda-2(J/2+\lambda)=-1$$
in the odd case, and
$$q_E=(J-1+\lambda)+(\lambda-2)-2(J+\lambda-2)=1-J$$
in the even case.The independent far-leg length  $z$  cancels exactly. Consuming any original support does not change these original-charge formulas.Further completeness excludes even  $B$ This is a stronger consequence of the same assumptions.Suppose  $B$  were even. Then  $s$  is E’s terminal, and its original axial support is
$$p=E(g+1,1)=(a,w+8).$$
This point is absent from  $Q,D,L,C,E$ , but all four of its neighboring positions are occupied:Direction from  $p$ PointOriginal ownerNorth $(a-1,w+8)$  $D$ East $(a,w+9)$  $D$ West $(a,w+7)$  $C$ South $(a+1,w+8)$  $E$ Completeness requires an endpoint consumer at  $p$ , since it cannot remain an original support with four occupied neighbors.That consumer would be distinct from the prescribed owners. But every legal U/rotor endpoint has an adjacent endpoint of its own original owner, and all four adjacent positions are already fixed foreign endpoints. Such a consumer is impossible.Hence the actual complete-family conclusion sharpens to
$$\boxed{
B\text{ odd},\qquad
g=B-a,\qquad
t\le g\le h-2,\qquad
q_E=-1.
}$$
The even- $B$  formula remains a correct algebraic phase calculation. It should not be described as a realizable complete-family alternative.5. The tight-width exclusion is correctWhen  $h=t+2$ , the bar window is a singleton:
$$B=a+t=a+h-2.$$
This is odd, so
$$g=t.$$
The endpoint
$$C(2,K)=(a+h-2,w+K+6)=(B,w+K+6)$$
exists for every allowed independent far leg  $f\ge4$ .At row  $B$ , E’s outer bar contains columns
$$w+8,\ldots,w+J+7.$$
Thus  $J\ge K-1$  would place that C endpoint on E’s bar, with intrinsic coordinates  $(0,K-1)$ . Since  $J,K$  are even, endpoint disjointness forces
$$\boxed{J\le K-2.}$$
Together with  $J\ge6$ , this yields
$$\boxed{K\ge8.}$$
The terminal supports also evaluate exactly as claimed:
$$E(g+1,1)=(a-1,w+8)\in V_D,$$

$$E(g,0)=(a,w+7)\in V_C.$$
This argument uses C’s actual original far-leg endpoint; it does not presume  $f=h$ ,  $z=g$ , or any relation between the independent far legs.The width restriction is specifically justified in the tight case. For a larger window, an E bar farther above C’s bar may avoid a short C far leg. The displayed window is a necessary condition, not a complete sufficiency criterion for arbitrary widths.6. Geometry of the six-source family for every even  $w\ge12$ The relevant endpoint geometry is:OwnerBar rows and columnsNear stemFar stem $D$ Rows  $a-2,a-1$ , columns  $6,\ldots,w+9$ Column  $6$ , rows  $a-2,\ldots,a+8$ Column  $w+9$ , rows  $a-2,\ldots,a+2$  $L$ Rows  $a,a+1$ , columns  $7,\ldots,w+6$ Column  $7$ , rows  $a,\ldots,a+4$ Column  $w+6$ , rows  $a,\ldots,a+6$  $C$ Rows  $a+5,a+6$ , columns  $w+7,\ldots,w+14$ Column  $w+7$ , rows  $a,\ldots,a+6$ Column  $w+14$ , rows  $a+2,\ldots,a+6$  $E$ Rows  $a+3,a+4$ , columns  $w+8,\ldots,w+13$ Column  $w+8$ , rows  $a,\ldots,a+4$ Column  $w+13$ , rows  $a,\ldots,a+4$ W’s transposed bar occupies columns  $w+1,w+2$ , on rows  $a+2,\ldots,a+7$ . Its two horizontal legs lie on rows  $a+2,a+7$ , reaching column  $w+5$ .Q has endpoint columns at most  $11$  and endpoint rows at least  $a+5$ .These descriptions prove pairwise endpoint disjointness uniformly:E’s bar is below D’s last far-stem endpoint and above C’s bar.E’s stem columns are strictly between C’s stem columns.W starts below L’s bar and lies between L’s stem columns.For  $w\ge12$ , W and the new right-hand owners are separated from Q in tile columns.Q’s possible interaction with L’s near portion is excluded by the adjacent but distinct tile-row ranges already used in the accepted package.The initial forced point  $(a,w+7)$  belongs to C. The cavity point  $s$  belongs to E at intrinsic coordinates  $(3,1)$ . Thus both stated forced sites are indeed consumed.7. Adding  $E$ : exactly two mixed full tiles and five eventsTo distinguish the owner  $E$  from the event count, write  $e$  for the latter, so
$$\Phi=N+S+2F-e.$$
E’s only shared endpoint tiles with  $Q,D,L,C$  are
$$T_0=\{a-1,a\}\times\{w+8,w+9\},$$

$$T_1=\{a+1,a+2\}\times\{w+8,w+9\}.$$
The  $3D+1E$  tile  $T_0$ It adds one mixed full tile. Its three new events are
$$D:(a-1,w+8)\longrightarrow E:(a,w+8),$$

$$D:(a,w+9)\longrightarrow E:(a,w+8),$$

$$E:(a,w+8)\longrightarrow D:(a,w+9).$$
The remaining possible direction,
$$E:(a,w+8)\longrightarrow D:(a-1,w+8),$$
hits E’s original axial terminal support. It is excluded even though D consumes that support.The  $2D+2E$  tile  $T_1$ It also adds one mixed full tile.On row  $a+1$ , both directions are excluded:D’s target  $(a+1,w+8)$  is its original inward far-leg support.E’s target  $(a+1,w+9)$  is its original inward near-leg support.Both supports are consumed, but the original-support exclusions persist.On row  $a+2$ , neither cross direction meets that owner’s original support. Both directions are events.Thus
$$\boxed{\Delta F=2,\qquad \Delta e=3+2=5.}$$
Why there are no additional contactsC/E separation requires the aligned tile structure:C’s near stem uses column pair  $(w+6,w+7)$ .E’s endpoint columns use pairs from  $(w+8,w+9)$  through  $(w+12,w+13)$ .C’s far stem uses pair  $(w+14,w+15)$ .E’s bar uses row pair  $(a+3,a+4)$ .C’s bar uses the next row pair  $(a+5,a+6)$ .Physical adjacencies across these boundaries create no intratile events.L and Q share no endpoint tile with E. D’s far stem ends in row  $a+2$ , which is odd, while E’s bar starts at row  $a+3$ , which is even. Those also belong to different tile rows.Original full E tilesE has three full original bar tiles:
$$(a+3,w+8),\qquad
(a+3,w+10),\qquad
(a+3,w+12).$$
They are excluded from mixed  $F$ . C’s three original full bar tiles, at the corresponding columns in row pair beginning  $a+5$ , are likewise excluded.For this E,
$$M_E=9,\qquad T_E=7,\qquad A_E=4,$$
so its original charge is  $-1$ . Therefore
$$\Delta S=1,\qquad \Delta N=0,$$
and
$$\boxed{\Delta R_{\rm raw}=1+2(2)-5=0,\qquad \Delta\Phi=0.}$$
This is the claimed particular insertion identity. It does not assert that every consumer satisfying the general window has a neutral insertion ledger.8. The external term remains exactly  $-3$ W has no endpoint tile in common with  $Q,D,C,E$ . In particular, its last column pair is  $(w+4,w+5)$ , before C’s first pair  $(w+6,w+7)$  and E’s first pair  $(w+8,w+9)$ .Its shared L tiles are exactly:Lower tile coordinatePartitionExtra mixed full tilesDirected events $(a+1,w)$  $2L+1W$ 01 $(a+1,w+2)$  $2L+2W$ 13 $(a+1,w+4)$  $2L+2W$ 13The seven events are
$$L:(a+1,c)\longrightarrow W:(a+2,c),
\qquad c=w+1,\ldots,w+5,$$
and
$$W:(a+2,c)\longrightarrow L:(a+1,c),
\qquad c=w+2,w+4.$$
The reverse directions at columns  $w+1,w+3,w+5$  meet W’s original supports. Their consumption by L does not turn those directions into events.Consequently,
$$F_{\rm extra}=2,\qquad e(P,W)=7,$$
and
$$\boxed{2F_{\rm extra}-e(P,W)=-3.}$$
The same source-labelled partition used for the accepted package applies to  $P=\{L,C,E\}$ : internally full tiles are necessarily new, original-full tiles remain excluded, and added events partition by the original owner of the foreign endpoint. There is no additional sign assumption.Symbolic total ledgerThe isolated original charges are:OwnerMatching edgesEndpoint-touched tilesOriginal supports in those tilesCharge $Q$ 1196 $-1$  $D$  $w+10$  $w+9$ 5 $-w-3$  $L$  $w+4$  $w+5$ 7 $1-w$  $C$ 12109 $+1$  $E$ 974 $-1$  $W$ 9106 $-5$ Writing  $k=w/2$ , the family totals are:Family $N$  $S$  $F$  $e$  $R_{\rm raw}$  $\Phi$  $Q,D$ 0 $w+4$ 00 $w+4$  $w+4$  $Q,D,L,C$ 1 $2w+3$  $k+6$  $2w+12$  $w+3$  $w+4$  $Q,D,L,C,E$ 1 $2w+4$  $k+8$  $2w+17$  $w+3$  $w+4$  $Q,D,W$ 0 $w+9$ 00 $w+9$  $w+9$ All six1 $2w+9$  $k+10$  $2w+24$  $w+5$  $w+6$ Thus
$$\Phi(Q,D,L,C,E)=\Phi(Q,D),$$
while
$$\boxed{
\Phi(Q,D,W,L,C,E)-\Phi(Q,D,W)=-3.
}$$
Only C is a positive original owner. E contributes no increment to  $N$ .9. The claimed next missing support is correct at every widthLet
$$q=(a+2,w+10).$$
It is D’s original outward far-leg support with intrinsic coordinates
$$(4,w+5),$$
and its original anchor is
$$D(4,w+4)=(a+2,w+9).$$
It is absent from all six endpoint sets:Q, L and W are excluded by their column ranges.D has no endpoint there because row  $4$  has endpoints only on its two stems.In C’s coordinates,  $q=(4,4)$ , which is not an endpoint.In E’s coordinates,  $q=(2,3)$ , which is not an endpoint.But its south neighbor is the E bar endpoint
$$E(1,3)=(a+3,w+10).$$
Thus the unconsumed support  $q$  has its west original anchor and a distinct occupied south neighbor. It violates the sole-occupied-neighbor requirement.This proves incompleteness for every even  $w\ge12$ , independently of  $b$ ’s even translation. Any complete extension would have to consume this point and include the entire actual consumer and its signed contribution.The six-source family therefore refutes precisely the endpoint-only external nonnegativity rule after the two identified consumers have been supplied. It does not furnish a complete-family compensation counterexample or a target allocation counterexample.Recommended precision in the statementI would retain the theorem and obstruction, while sharpening the parity paragraph to distinguish the two levels:The endpoint-disjoint coordinate classification has the two stated parity charge formulas. Completeness at the next axial support excludes even  $B$ . Hence an actual cavity consumer in a complete family has odd  $B$ ,  $g=B-a$ , and original charge  $-1$ .Also retain the explicit qualification that the window gives necessary forms, and that uniqueness concerns the frame of the fixed actual owner rather than a unique choice of dimensions across completions.The audit above uses the original catalogue, coordinate intervals, parity and tile/event partitions. It does not certify the reported checker or Lean executions, complete realizability, full allocation, grid equality, or novelty.
