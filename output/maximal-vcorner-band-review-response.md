ACCEPTThe two-source noncompletion proof is valid under the stated complete original U/rotor model. It exhausts every possible consumer at  $q$ , including arbitrary U dimensions, both possible U bar orientations, both east-pointing rotor tips, and owners recurring elsewhere in the family.The proof also covers the boundary case  $k=W-4$ . Consequently, the specified matched eight-source seed has no arbitrary complete U/rotor extension. This conclusion follows from its fixed  $B/X$  pair alone and does not use the finite UNSAT result.I find no substantive defect. The scope remains exactly the maximal-width, long-far-leg subclass stated in the theorem.1. The forced support and the two fixed-owner exclusions are correctWrite  $d=b-2$ . Since  $b\ge8$ , the prescribed  $X$  width satisfies  $d\ge6$ .The point
$$q=X(0,d+1)=X(0,b-1)=(b+1,3)$$
is indeed  $X$ 's original outer-bar support. Its original anchor and the other two fixed neighbors are
$$\begin{aligned}
q+(-1,0)&=(b,3)=X(0,b-2),\\
q+(0,-1)&=(b+1,2)=B(2,1),\\
q+(1,0)&=(b+2,3)=B(1,2).
\end{aligned}$$
All three endpoints exist under the permitted minimum dimensions.Neither fixed source owns  $q$ :The  $X$  bar spans physical rows  $3,\ldots,b$ , and its two legs remain on rows  $3$  and  $b$ . Their independent lengths change columns, not rows. Thus every  $X$  endpoint has row at most  $b$ .The inverse  $B$ -coordinates of  $q$  are  $(2,2)$ . At intrinsic row  $2$ , the only  $B$  endpoint columns are  $1$  and  $W$ . Since  $W\ge6$ ,  $(2,2)$  is not an endpoint.Equivalently,  $B$ 's bar is on rows  $b+2,b+3$ , while its legs lie in columns  $2,W+1$ ;  $q=(b+1,3)$  belongs to none of these.If  $q$  remained selected, it would have its original anchor and two additional occupied neighbors, violating the retained-support condition. It must therefore be consumed by an original endpoint owner different from both  $B$  and  $X$ .That last statement is established geometrically. It is not a fresh-owner assumption.2. Only an east terminal or an east rotor tip can occurLet  $Y$  be the actual original owner consuming  $q$ . The north, west, and south neighbors already belong to  $X,B,B$ , respectively. Since  $Y\ne B,X$ , unique endpoint ownership prevents any of those three points from being an original endpoint of  $Y$ .Thus  $Y$ 's own endpoint neighbors at  $q$  can lie only east.Every original U/rotor endpoint has at least one own endpoint neighbor. Hence  $q$  has exactly one own neighbor, in the east direction.The original-source catalogue now gives an exhaustive reduction:For U sources, the degree-one endpoints are precisely leg terminals.Nonterminal straight-leg points have two opposite own neighbors.Outer bar corners have two perpendicular own neighbors.Internal bar points and bar/stem junctions have three own neighbors.For rotors, only a tip can have one own neighbor; fixing that neighbor east leaves the two displayed tip footprints.No source width or leg-length bound is used in this reduction. In particular, a very wide U, a very long other leg, or a different allowed phase cannot create another endpoint role with only an east own neighbor.3. The U stem bound is exact, including its endpointSuppose  $q$  is an east terminal with incident length  $g$ . After naming the incident leg first, its original endpoint segment contains
$$\{(b+1,c):3\le c\le g+3\}.$$
The rightmost point of this segment is the outer bar corner. Including that point is necessary for the equality case below.The fixed endpoint
$$B(2,W)=(b+1,W+1)$$
exists because  $e\ge4$ . It does not depend on the length of  $B$ 's other leg beyond this stated minimum.If
$$g\ge W-2,$$
then
$$W+1\le g+3,$$
so the terminal segment contains  $B(2,W)$ . Since the consumer is different from  $B$ , that is forbidden. Therefore
$$g<W-2.$$
Both  $g$  and  $W$  are even, giving exactly
$$\boxed{g\le W-4.}$$
For  $W=6$ , this already contradicts the permitted minimum  $g\ge4$ . Otherwise, every remaining U possibility satisfies
$$4\le g\le W-4.$$
There is no off-by-one gap at  $g=W-2$ : the collision then occurs at the terminal’s outer bar corner itself, which is an original endpoint.4. Both U bar orientations are excludedWith the terminal at  $q$  and its own neighbor east, the incident direction fixes the horizontal part of the frame. After incident-leg reindexing, the other bar end can lie only below or above. The stated two frames therefore exhaust the possibilities:
$$F_{\downarrow}(r,c)=(b+c,g+3-r),$$
and
$$F_{\uparrow}(r,c)=(b+2-c,g+3-r).$$
The recipient’s original endpoint  $(0,2)$  exists at every permitted width  $s\ge6$ .Downward barIts image is
$$F_{\downarrow}(0,2)=(b+2,g+3).$$
This is exactly
$$B(1,g+2).$$
The required intrinsic  $B$  column exists: from
$$4\le g\le W-4$$
one gets
$$6\le g+2\le W-2<W.$$
Thus it is an original  $B$  bar endpoint.Because  $q\notin B$ , the hypothetical consumer cannot be  $B$ . The overlap is a genuine different-owner violation.Upward barThe same intrinsic recipient endpoint maps to
$$F_{\uparrow}(0,2)=(b,g+3).$$
This equals
$$X(g,b-2).$$
Here  $b-2$  is  $X$ 's far-leg column, and
$$4\le g\le W-4\le k.$$
Consequently, this is an original endpoint of  $X$ 's far leg.Again, the consumer differs from  $X$ , because  $q\notin X$ , so the overlap is forbidden.The equality boundary is covered: when
$$g=k=W-4,$$
the collision point is  $X$ 's original far terminal, not its beyond-tip support. It remains an endpoint and cannot be removed.The independent recipient far-leg length never enters either argument. Its width is used only through the permitted minimum ensuring intrinsic bar column  $2$ . Nor is any additional restriction placed on  $X$ 's near leg  $a$ .5. Both rotor tips are excludedThe displayed footprints are the two east-facing tip possibilities in the original rotor catalogue. Their chosen blockers are correct.For the first footprint,
$$q+(-1,1)=(b,4)=X(1,b-2).$$
For the second,
$$q+(1,1)=(b+2,4)=B(1,3).$$
Both are fixed original bar endpoints. Their existence requires no extra leg-length assumption.The consumer at  $q$  is neither  $X$  nor  $B$ , so neither overlap can be interpreted as a same-owner identification. Both rotor possibilities are therefore excluded.This is an exhaustion of the fixed rotor catalogue with the own-neighbor direction prescribed. It does not extrapolate from a bounded search over placements.6. Recurring owners and additional sources cannot evade the contradictionThe proof does not require  $Y$  to be absent from other parts of a proposed extension. It may already occur elsewhere, or it may be one of the other sources in the eight-source seed. Its original endpoint role at  $q$  must still be one of the exhausted cases.Every collision is with  $B$  or  $X$ , and the proof has already established
$$Y\ne B,\qquad Y\ne X.$$
Thus recurring ownership creates no escape.Likewise, added sources cannot remove or reassign any of the fixed original endpoints used as blockers. Support consumption is permitted; erasure or reassignment of original endpoints is not. A consumer cannot turn one of these forbidden overlaps into a permissible consumption event.The contradiction is therefore local and independent of the number and dimensions of added sources:
$$\text{completeness requires a consumer at }q,$$
while
$$\text{every permitted original-source consumer at }q\text{ is impossible}.$$
No assumption about the auxiliary  $C$ , the other gap-eight sources, or the phase of added sources is needed.7. The parity corollary is correctIn a complete actual maximal-width Vcorner occurrence,  $d=b-2$  and the minimum width  $d\ge6$  already imply  $b\ge8$ . Thus the two-source theorem applies.Its forbidden condition must fail:
$$k<W-4.$$
Since  $k$  and  $W$  are even,
$$\boxed{k\le W-6.}$$
Combining this with  $k\ge4$  gives
$$\boxed{W\ge10.}$$
These are necessary conditions only. The theorem does not assert that every parameter choice satisfying them has a complete extension.There is also a useful boundary check. Prescribed endpoint disjointness itself already excludes
$$k\ge W-2,$$
because in that case
$$B(3,W)=(b,W+1)=X(W-2,b-2)$$
would be a shared original endpoint. Thus, among endpoint-disjoint pairs satisfying the theorem’s long-far-leg hypothesis, the nontrivial case is precisely
$$k=W-4.$$
The new support-consumer argument excludes that boundary case and strengthens the necessary bound to  $k\le W-6$ . This is consistent with the theorem’s wording and confirms that the proof supplies more than an initial endpoint-overlap check.8. The stated matched seed has no arbitrary complete extensionFor the displayed seed,
$$B=U(8,8,4),\qquad X=U(6,10,4),$$
the relevant parameters are
$$b=W=8,\qquad d=6=b-2,\qquad k=4=W-4.$$
The obstructed support is
$$q=(9,3).$$
Its three fixed neighbors are
$$(8,3)\in X,\qquad (9,2)\in B,\qquad (10,3)\in B.$$
The U stem bound leaves only  $g=4$ . The two possible bars then collide at
$$(10,7)=B(1,6)$$
and
$$(8,7)=X(4,6),$$
respectively. The two rotor blockers are
$$(8,4)=X(1,6),
\qquad
(10,4)=B(1,3).$$
Thus this  $B/X$  pair alone cannot occur in any complete extension. A larger prescribed seed containing that unchanged pair cannot acquire a complete extension either, regardless of how many additional U/rotor sources are allowed or how large they are.This conclusion is stronger than the earlier statement that the seed was merely incomplete: the seed is now proved noncompletable under the model. Its local old-P stencil and exact  $C=C'$  identification remain valid coordinate facts. They never implied complete realizability.The result excludes neither all matched  $f=j+2$  returns nor the surviving maximal-width cases with  $k\le W-6$ . It also creates no activation or compensating reserve: the excluded configurations contribute no actual complete-family claims. The finite UNSAT result and reported code or Lean checks are unnecessary to this written noncompletion proof.