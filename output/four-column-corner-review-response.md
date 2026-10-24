ACCEPT for both the four-column barrier and the forced-return conclusion  $e=b-2$ . The arguments hold under the supplied rotor classification and original-support retention rules, for all independent even  $b,e,k$  in the stated ranges. The reported checker and Lean executions remain unverified.One statement-level clarification should be made explicit: “no fixed-owner endpoint on the first interior column” means
$$F\cap\bigl(\{l+1,\ldots,u-1\}\times\{c+1\}\bigr)=\varnothing,
\tag{A}$$
where  $F$  is the fixed owners’ endpoint union. The required top and bottom boundary endpoints also lie on coordinate column  $c+1$ ; condition (A) specifies the strict-interior segment used throughout the proof and application.1. The missing corner permits no escape from the strict interiorLet
$$I=\{l+1,\ldots,u-1\}\times\{c+1,\ldots,c+4\}.$$
Suppose a foreign source has an endpoint in  $I$ . If its connected endpoint graph also has a vertex outside  $I$ , take the first vertex outside  $I$  along an endpoint path starting inside. That vertex lies on the boundary of  $D$ .The possibly missing corner  $(u,c+5)$  has no unit-edge neighbor in  $I$ , so it cannot be this first boundary vertex. The first boundary vertex is therefore occupied by a fixed owner, contradicting endpoint disjointness. Consequently, the foreign source’s entire endpoint graph lies in  $I$ .This proves confinement even if the missing corner belongs to the foreign source under consideration. Fixed-owner endpoints in other interior columns create additional occupancy restrictions and leave this confinement argument valid.A confined U is excluded by its minimum column extent of five. A confined rotor must occupy all four available columns, placing its unique leftmost tip on column  $c+1$ .2. The forced-consumer argument closes for both rotor formsLet the confined rotor have leftmost tip  $x$ . Write its mandatory perpendicular support as
$$y=x+(\delta,0),
\qquad
\delta=
\begin{cases}
1,&R_-,\\
-1,&R_+.
\end{cases}$$
The support is strictly interiorBoth displayed rotor forms contain endpoints at relative positions
$$(-1,2),\qquad (1,2).$$
Because the rotor is confined, both corresponding rows lie strictly between  $l$  and  $u$ . Thus the row of  $y$  lies strictly between those boundaries. Its column is  $c+1$ , so  $y\in I$ .This verifies the support-location assertion directly, including rotors positioned as close as possible to either horizontal boundary.Its consumer must be another confined rotorThe mandatory support  $y$  has two distinct occupied neighbors:its original anchor  $x$ ;the fixed left-boundary endpoint  $(y_{\rm row},c)$ .Therefore retaining  $y$  as a selected point violates its unique-anchor condition. Completeness forces  $y$  to be an endpoint.Condition (A) excludes a fixed owner as its consumer. The first rotor also has no endpoint at  $y$ : its unique endpoint on column  $c+1$  is  $x$ . Hence the consumer is a distinct foreign source.The same confinement argument applies to that consumer. Its extent excludes a U, so it is a rotor. Since it occupies four columns inside the four-column strip and has an endpoint at  $y$ , its unique leftmost tip is exactly  $y$ .The endpoint collision is uniformFor either rotor form,
$$(-1,2),(0,2),(1,2)\in R_\pm.$$
For any producer chirality  $\alpha$ , consumer chirality  $\beta$ , and vertical displacement  $\delta\in\{-1,1\}$ ,
$$x+(0,2)\in x+R_\alpha,$$
and
$$x+(0,2)
=y+(-\delta,2)
\in y+R_\beta.$$
Thus the two owners share the endpoint  $x+(0,2)$ . This single identity covers all eight chirality/sign combinations, including every combination required by the mandatory-support rule.The contradiction proves the barrier. Its only use of the empty first interior column is to force the support consumer to be foreign; fixed-owner endpoints elsewhere inside  $D$  are fully compatible with the argument.3. The H application satisfies every barrier hypothesisThe relevant physical endpoint intervals are
$$\begin{array}{c|c|c}
\text{Owner}&\text{Part}&\text{Physical location}\\ \hline
B&\text{bars}&r=b+2,b+3,\quad c=2,\ldots,7\\
B&\text{near leg}&c=2,\quad r=3,\ldots,b+1\\
B&\text{far leg}&c=7,\quad r=b+3-e,\ldots,b+1\\
H&\text{bars}&r=3,4,\quad c=3,\ldots,8\\
H&\text{near leg}&c=3,\quad r=5,\ldots,b+1\\
H&\text{far leg}&c=8,\quad r=5,\ldots,k+3 .
\end{array}$$
For
$$D=[4,b+2]\times[3,8],$$
these intervals give:the complete top boundary from H;both vertical boundaries through row  $b+1$  from H, using  $k\ge b-2$ ;the bottom boundary at columns  $3,\ldots,7$  from B.Only  $(b+2,8)$  can be missing. When  $k=b-2$ , H’s far leg stops immediately above it. When  $k\ge b$ , H also occupies that corner. Both cases satisfy the barrier.The first strict-interior column is
$$\{5,\ldots,b+1\}\times\{4\},$$
and neither B nor H has an endpoint there. B’s possible interior endpoints at column  $7$  are expressly allowed.4. Every shorter permitted return forces the forbidden foreign endpointIf  $e\ge b$ , B’s far leg contains  $(3,7)$ , which H’s upper bar also contains. Endpoint disjointness and evenness therefore yield
$$e\le b-2.$$
For  $b=6$ , this and  $e\ge4$  already give  $e=4$ . For the remaining wrong-return case, assume
$$e\le b-4,\qquad m=b+2-e.$$
Then
$$6\le m\le b-2,$$
so
$$x=(m,7)$$
is strictly inside  $D$ .Its intrinsic B coordinates are exactly  $(e+1,6)$ . Hence it is B’s mandatory beyond-tip support, with original anchor
$$(m+1,7).$$
B’s far leg starts at row  $m+1$ , so B has no endpoint at  $x$ . H’s column- $7$  endpoints occur only in its bar rows  $3,4$ , so H also has no endpoint there.Meanwhile H supplies the distinct occupied neighbor  $(m,8)$ , because
$$5\le m\le b-2<b+1\le k+3.$$
The support therefore requires endpoint consumption by a foreign owner, contradicting the four-column barrier.This excludes every even  $e\le b-4$ . Combined with the endpoint-disjointness upper bound, it proves
$$\boxed{e=b-2}.$$
The proof uses the independent parameter  $k$  only through  $k\ge b-2$ ; it introduces no equality between  $k$  and  $e$ .5. The realization and accounting scope are correctly statedThe previously accepted families realize
$$e=k=b-2$$
for every even  $b\ge6$ . They establish actual complete examples at every incident length  $b$ . Existence for every independently prescribed larger  $k$  is a separate question, and the addendum makes no such existence claim.For an actual marked claim in the stated subclass, the forced equality supplies the missing hypothesis of the earlier permanent-pair theorem. Its receipt then enters the same physical lower-pair union, with the existing injection and count-once rules.The exclusion proof itself contributes zero additional reserve terms. It removes impossible return-length configurations from the admissible claim analysis. Universal residual coverage, unrestricted allocation, and rectangular-grid triple equality retain their stated OPEN status.Accept the addendum, write the first-column hypothesis explicitly as (A), and retain the existing receipt accounting and stated open scope.
