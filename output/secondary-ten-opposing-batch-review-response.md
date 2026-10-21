ACCEPTThe new complete-family exclusion is correct, and the all-breadth classification yields the stated exact excess  $h-3$  for  $h\ge18$ . I find no blocking flaw in the forced-consumer argument, the U/rotor role classification, the unbounded collision certificates, or the final ledger.This is a separate acceptance of the new theorem. The earlier negative partial-inventory receipt remains correct; the new argument proves that its  $h=16$  prefix has no complete extension.1. Completeness forces an additional actual owner at  $e$ The support and endpoint assertions at
$$e=(a,w+14)$$
are correct.For  $E_1$ , the inverse chart sends  $e$  to  $(4,7)$ . Since  $E_1=U(6,4,4)$ , this is the even-indexed outward support at the far terminal.The point is absent from the retained endpoint sets:It is absent from  $A_1$ , as in the accepted residual geometry.Every  $A_2$  endpoint lies at row at most  $a-7$ .Its fixed- $U$  coordinates are  $(4,2)$ , which satisfy neither the bar nor either stem endpoint condition.Its west and south neighbors are retained endpoints:
$$(a,w+13)\in E_1,\qquad
(a+1,w+14)\in U.$$
Their respective intrinsic coordinates are  $(4,6)$  in  $E_1$  and  $(4,1)$  in  $U$ .Thus an unconsumed  $e$  would have at least two neighbors in  $O$ , contradicting completeness. An actual original  $K$  must contain  $e$ , and  $K$  is distinct from all seventeen retained originals.Because the west and south endpoint neighbors belong to other actual owners, neither can be an own endpoint neighbor of  $K$ . The only possible own-neighbor directions are north and east. At least one must occur because  $e$  has an original matching partner.2. Every role involving an own east neighbor is excludedU rolesThe stated catalogue is exhaustive. With own neighbors restricted to north/east and including east, a U endpoint can only be:an east-directed leg terminal; oran outer corner with north/east own neighbors.A nonterminal stem point has two opposite own neighbors, and the remaining bar or junction roles have three own neighbors, so those roles cannot occur here.Every eligible U role contains the third east site
$$e+(0,3)=(a,w+17).$$
For a terminal, moving three steps inward leaves intrinsic row  $d-3\ge1$ , which is still on the incident leg or its row-one bar endpoint. For an outer corner, the eastward arm is either a bar of breadth at least  $6$  or a leg of length at least  $4$ ; either contains its first three further endpoints.The fixed U contains this blocking point at intrinsic coordinates
$$(1,2).$$
Since  $K\ne U$ , this is a genuine original-endpoint collision.Rotor rolesRotor core endpoints have three own endpoint neighbors. Therefore an east-including rotor role under the north/east restriction must be an east tip.The two full-source east-tip images at  $e$  can be represented by
$$R^e_N(r,c)=(a-3+r,w+13+c),$$

$$R^e_S(r,c)=(a+3-r,w+13+c).$$
Both place the standard tip  $(3,1)$  at  $e$ , with its own neighbor east.Both contain
$$e+(1,2)=(a+1,w+16):$$
its standard rotor coordinates are  $(4,3)$  in the first image and  $(2,3)$  in the second. Both are rotor endpoints.The same point has fixed- $U$  coordinates
$$(2,1),$$
so both rotor possibilities collide with the retained U.Consequently,  $K$  has exactly its north own neighbor.The two north-terminal rotor possibilities are then excluded by the explicitly accepted complete-family lemma for  $A_1$ . That dependency applies here regardless of the identity of the owner of  $t$ .Thus  $K$  must be an actual north-terminal U, in one of the stated frames:
$$K_R(r,c)=(a-d+r,w+13+c),
\qquad
K_L(r,c)=(a-d+r,w+15-c).$$
The accepted full-source leg reflection justifies normalizing the incident leg this way without changing the actual matching or original supports.3. All north-terminal U collision certificates checkThe reflected source charts are correct:
$$V_2(r,c)=(a-7-r,w+12-c),$$

$$C_2(r,c)=(a-19+r,w+6+c).$$
Here is the complete collision ledger:Candidate and depthPhysical collision pointCandidate coordinatesRetained blocker and coordinatesEither orientation,  $d\ge16$  $(a-15,w+14)$  $(d-15,1)$  $C_2:(4,8)$  $K_R$ ,  $d=4,6,8,10,12,14$  $(a+1-d,w+17)$  $(1,4)$  $U:(1,d+1)$  $K_L$ ,  $d=4,6$  $(a+1-d,w+11)$  $(1,4)$  $V_1:(7-d,1)$  $K_L$ ,  $d=8,10,12,14$  $(a+1-d,w+11)$  $(1,4)$  $V_2:(d-8,1)$ Every listed coordinate is an endpoint throughout its stated parameter range.The unbounded depth rangeFor  $d=16$ , the candidate coordinate  $(d-15,1)$  is  $(1,1)$ , a bar endpoint. For every legal even  $d\ge18$ ,
$$3\le d-15\le d,$$
so it is a near-stem endpoint.The blocking coordinate  $(4,8)$  is  $C_2$ ’s far terminal. This proves the collision for both orientations and for arbitrarily large  $d$ . It does not use any bound on the candidate’s far-leg length or breadth.The remaining right-oriented depthsFor  $4\le d\le14$ , with  $d$  even, the candidate coordinate  $(1,4)$  is a bar endpoint because  $H\ge6$ .The fixed-U coordinate is
$$(1,d+1),\qquad 5\le d+1\le15.$$
It lies in the row-one bar of  $U(16,4,4)$ .The remaining left-oriented depthsAt  $d=4,6$ , the  $V_1$  coordinates are
$$(3,1),\quad(1,1),$$
respectively a near-stem and a bar endpoint.At  $d=8,10,12,14$ , the  $V_2$  coordinates are
$$(0,1),\quad(2,1),\quad(4,1),\quad(6,1),$$
respectively a bar endpoint and three endpoints of its retained near stem of length  $8$ .These cases exhaust every legal even  $d\ge4$ . The candidate breadth enters only through  $H\ge6$ , ensuring that bar column  $4$  exists; its far-leg length never enters the collision argument.Each blocker belongs to an original distinct from  $K$ , because  $e$  is absent from every retained original. Thus none of these intersections can be resolved by identifying the candidate with the blocker’s owner.The conclusion follows: completeness forces an actual owner of  $e$ , but every possible owner is excluded. Additional originals and support consumption cannot remove these retained endpoint collisions.The same contradiction transports under any permitted tile-preserving isometry of the whole prefix, since endpoint ownership, original matching/support data, adjacency and completeness are preserved.4. The reflection family is correctly normalized for every legal breadthWrite
$$f_h(r,c)=(a+2-c,w+18-r).$$
Then
$$\rho_h(f_h(r,c))
=f_h(r,h+1-c).$$
Thus  $\rho_h$  acts on the canonical U by its leg-exchanging reflection.Because  $h$  is even and the two legs both have length  $4$ , this preserves the full original: endpoints, matching and supports. The reflection constant
$$2a+3-h$$
is odd, so  $\rho_h$  also preserves the fixed tile partition.The two physical terminals are
$$t_1=(a+1,w+14),
\qquad
t_2=(a+2-h,w+14).$$
They are distinct for every legal  $h\ge6$ , and each is the terminal of a north-frame east-U route in its own package chart. Hence each route has cost  $1$ .For any complete extension in the admissible range, these are indeed distinct-owner routes. The point  $e_1$  has U coordinates  $(4,2)$ , so  $U_h$  does not own it; invariance gives the same conclusion for  $e_2=\rho_h(e_1)$ . The accepted forced-support result supplies their actual owners in a complete extension.5. The small-breadth collisions and the  $h=16$  exception are exhaustiveThe reflected V chart in this family is
$$V_2(h)(r,c)=(a+9-h-r,w+12-c).$$
For
$$x_h=(a+8-h,w+11),$$
the inverse coordinates are
$$V_1^{-1}(x_h)=(14-h,1),
\qquad
V_2(h)^{-1}(x_h)=(1,1).$$
For  $h=6,8,10,12,14$ , the first coordinates in  $V_1$  are
$$8,\ 6,\ 4,\ 2,\ 0.$$
Each gives an endpoint of its near stem or bar;  $(1,1)$  is always a bar endpoint of  $V_2(h)$ . Thus the displayed physical endpoint collision is valid in every small-breadth case.This is not a harmless alternative labeling of one physical V. The row ranges of the two V originals are
$$[a-6,a+2]
\quad\text{and}\quad
[a+1-h,a+9-h].$$
Equality would require  $h=7$ , outside the legal even breadths. In particular, the colliding V originals are distinct physical sources.At  $h=16$ ,
$$\rho_h(\mathrm{row},\mathrm{column})
=(2a-13-\mathrm{row},\mathrm{column}),$$
so this is exactly the endpoint-disjoint seventeen-source prefix excluded by the new complete-family theorem.There is therefore no missing legal breadth between the small-overlap range, the excluded  $h=16$  case and  $h\ge18$ .6. For  $h\ge18$ , the exterior remainder is exactly emptyThe endpoint row range of  $A_1$  is
$$[a-6,a+10].$$
Reflection gives the range
$$[a-7-h,a+9-h]$$
for  $A_2(h)$ .For  $h\ge18$ ,
$$\max\operatorname{row}(A_2(h))
=a+9-h\le a-9.$$
Thus any endpoint of  $A_1$  and any endpoint of  $A_2(h)$  differ in row by at least  $3$ . They cannot:coincide;be adjacent endpoints;lie in the same fixed  $2\times2$  tile.This proves the needed physical separation uniformly in  $w$ . It uses the prescribed first residual with  $z=4$ , whose endpoint row range is fixed as stated.The accepted  $J_N$  disjointness criterion applies to  $U_h$  and  $A_1$  for every  $h\ge18$ . Full-source  $\rho_h$ -invariance then gives disjointness from  $A_2(h)$ .The exterior-set conclusion also follows physically, rather than only from a signed calculation:There are no inter-base events or shared full tiles.There is only one selected U owner, so there are no foreign contacts between distinct selected U owners.Every U/base interaction is already one of the two local interactions.A full tile involving both bases and the U is impossible, because the two bases have no shared endpoint tile.Consequently,
$$F_{\mathrm{extra}}=E_{\mathrm{extra}}=\varnothing.$$
For these north-frame routes, the accepted local receipt is in fact stronger than merely zero signed contribution: there are no locally claimed new full tiles and no surviving local directed events. The possible three-endpoint  $t/C$  contact is excluded in both directions by original supports.7. The exact  $h-3$  excess counts the shared owner onceTile preservation gives
$$b_1=b_2=w+9,
\qquad
\Phi(A_1)=\Phi(A_2(h))=w+8.$$
The single selected owner  $U_h$  has
$$q(U_h)=1-h,$$
and therefore contributes  $h-1$  once to  $S$ .With zero local signed contact terms and empty exterior sets,
$$\begin{aligned}
\Phi(H)
&=2(w+8)+(h-1)\\
&=2(w+9)+h-3.
\end{aligned}$$
Equivalently, its exact remaining terminal budget is
$$r_{U_h}=(h-1)-1-1=h-3.$$
Since every complete extension of this prescribed family must have  $h\ge18$ ,
$$\boxed{\Phi(H)\ge2(w+9)+15.}$$
There is no duplicate mass: the reflected U is the same full original, and  $H$  includes it once. The two bases are disjoint owner inventories in this range, and the two terminal claims charge only their respective costs of  $1$ .The identity also holds for the endpoint-disjoint partial prefix at every  $h\ge18$ , independently of whether it admits a complete extension.8. The scope distinctions remain correctThe  $h=16$  receipt remains
$$\Phi=w+23,\qquad
\Phi-2(w+9)=5-w.$$
The new theorem changes its extendibility status, not its accounting: it has no complete extension, a stronger conclusion than its previously exhibited incompleteness.Within this specific reflected family,  $h=16$  is the only endpoint-disjoint breadth producing the opposing-bar exterior loss. Smaller legal breadths already have endpoint collisions; larger legal breadths have no inter-base endpoint tile.The proof does not establish complete realizability for any  $h\ge18$ , nor does it transfer the bound on  $\Phi(H)$  to  $\Phi(G)$  after further originals are inserted. Those qualifications are necessary and are correctly stated.The reported Lean execution and finite exact-set controls are separate from this verdict. I have not certified those runs. The acceptance follows from the exhaustive role argument, the parameter-uniform collision certificates, and the physical tile and owner accounting above.
