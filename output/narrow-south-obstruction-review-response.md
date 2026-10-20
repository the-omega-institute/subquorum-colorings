# Independent review: three-column south obstruction

ACCEPT. The stated two-source no-extension theorem is correct under the supplied complete-source assumptions. No mathematical repair is needed. In particular, the argument does not require a relation between  $k$  and  $g$ : it uses an original support of  $S$ ’s incident leg, while  $S$ ’s far leg stays outside the enclosure horizontally for every permitted  $k$ .This verdict covers the newly supplied obstruction separately from the previously accepted all-length packet.1. The whole boundary is occupied by prescribed endpointsWrite the two maps as
$$\Phi_C(r,c)=(c+1,8-r),\qquad
\Phi_S(r,c)=(g+3-r,c+2).$$
Their original endpoint sets have the following physical coordinates. All intervals here are integer intervals.Original portionPhysical endpoints $C$ ’s two-row barRows  $2,\ldots,V+1$ , columns  $7,8$  $C$ ’s incident leg beyond its barRow  $2$ , columns  $2,\ldots,6$  $C$ ’s far leg beyond its barRow  $V+1$ , columns  $4,5,6$  $S$ ’s two-row barRows  $g+2,g+3$ , columns  $3,\ldots,d+2$  $S$ ’s incident leg beyond its barColumn  $3$ , rows  $3,\ldots,g+1$  $S$ ’s far leg beyond its barColumn  $d+2$ , rows  $g+3-k,\ldots,g+1$ Consider
$$\mathcal R=[2,V+1]\times[3,7].$$
Every boundary point is therefore an original endpoint:Top:  $C$  occupies  $(2,c)$  for every  $3\le c\le7$ .Right:  $C$ ’s bar occupies  $(r,7)$  for every  $2\le r\le V+1$ .Bottom:  $C$  occupies  $(V+1,c)$  for  $4\le c\le7$ . Its far leg supplies columns  $4,5,6$ , and its bar supplies column  $7$ . The remaining bottom-left point  $(V+1,3)$  belongs to  $S$ .Left: The top-left point  $(2,3)$  belongs to  $C$ . Every point  $(r,3)$ ,  $3\le r\le V+1$ , belongs to  $S$ , because
$$V+1\le g+1.$$
The limiting case  $g=V$  still supplies the entire required left boundary, including its bottom endpoint. The far-leg length  $4$  of  $C$  supplies exactly the crucial endpoint at column  $4$ ; no longer far leg is being assumed.2. Neither prescribed owner has an interior endpointThe strict lattice interior is
$$\mathcal R^\circ_{\mathbb Z}
=\{3,\ldots,V\}\times\{4,5,6\}.$$
For  $C$ , its endpoints are confined to row  $2$ , row  $V+1$ , or columns  $7,8$ . Consequently none lies in this strict interior.For  $S$ :Its incident leg lies in boundary column  $3$ .Its bar lies below the rectangle, since
$$g+2\ge V+2>V+1.$$
Its far leg lies in column
$$d+2\ge8>7.$$
The last fact handles the independence of  $k$ . Even if the far leg extends far upward, it remains outside the rectangle’s horizontal range. No inequality such as  $k\le g$  is needed.3. The claimed point is an original mandatory supportTake
$$x=(V,4).$$
Its original coordinates in  $S$  are
$$\Phi_S^{-1}(x)=(g+3-V,2).$$
Put
$$r_*=g+3-V.$$
Because  $g,V$  are even,  $r_*$  is odd. Moreover,
$$g\ge V\quad\Longrightarrow\quad r_*\ge3,$$
and
$$V\ge6\quad\Longrightarrow\quad r_*\le g-3.$$
Thus
$$r_*\in\{3,5,\ldots,g-3\}.$$
According to the established original support rule,  $(r_*,2)$  is an inner support of  $S$ ’s incident leg. It is therefore a mandatory original support, with original anchor  $(r_*,1)$ . Under the physical map, that anchor is
$$\Phi_S(r_*,1)=(V,3).$$
The second fixed endpoint is
$$\Phi_C(4,V)=(V+1,4).$$
Here  $(4,V)$  is precisely  $C$ ’s original far terminal, since its far-leg length is  $4$ .Hence  $x$  has two distinct permanent occupied neighbors:
$$(V,3)\in E(S),\qquad (V+1,4)\in E(C).$$
If  $x$  were unconsumed, support retention would require it to remain selected, with occupied degree at least two. That contradicts the required degree one. Therefore an endpoint must consume  $x$ .Also,  $x$  is strictly interior:
$$2<V<V+1,\qquad 3<4<7.$$
This remains true at the minimum width  $V=6$ .4. Connectedness excludes every possible consuming ownerNeither  $C$  nor  $S$  has an interior endpoint, so any owner consuming  $x$  would be a foreign source  $D$ .Suppose  $D$ ’s connected original endpoint graph had an endpoint outside the strict interior. A lattice-edge path within that graph from  $x$  to that endpoint would have to visit the boundary of  $\mathcal R$ . Every boundary vertex is already an original endpoint of  $C$  or  $S$ . Such a visit would violate original endpoint disjointness.Therefore all original endpoints of  $D$  would have to lie inside
$$\{3,\ldots,V\}\times\{4,5,6\},$$
which has only three available columns.No permitted source fits:A canonical U occupies at least six lattice columns and at least five lattice rows. After any permitted orientation, it still requires at least five lattice columns.A rotor requires four lattice columns in every permitted orientation.Thus no foreign U or rotor can consume  $x$ . This contradicts the consumption forced by its two fixed endpoint neighbors.Scope of acceptanceThe proof establishes
$$\boxed{
C=U(V,6,4),\quad
S=U(d,g,k),\quad g\ge V,
\quad E(C)\cap E(S)=\varnothing
\ \Longrightarrow\
\text{no complete permitted U/rotor extension}.
}$$
It applies to arbitrary numbers and dimensions of added sources. It establishes the stated transverse-height-six, far-length-four subclass exclusion; it does not establish a general exclusion of longer south companions.This acceptance concerns the written mathematical argument. It does not certify any search, program execution, or formal verification, and it does not retroactively enlarge the scope of the earlier review.

