# Independent cavity review

Verdict: ACCEPT, with two necessary literal clarificationsUnder the intended prior-coordinate hypotheses and the stated root-triple ledger, the all-parameter cavity theorem and the conditional  $54$  corollary are correct. The geometric exclusion is genuinely parameter-uniform: it uses only  $H\ge 6$ , leg depths at least  $4$ , and the retained guard geometry.Two details should be made explicit for a completely self-contained statement:The four rotor rows are the four guard-compatible survivors. Before imposing the north/west guards, there are eight normalized tip placements whose matching direction is east or south; four of those already collide with an immediate north/west guard.The root application requires the B-coordinate notation to mean that the near B stem is at a column  $s_1\neq s+1$ , while the interval from  $s+1$  to  $C$  is a retained subinterval of B’s row-one bar. If  $s_1$  were intended to equal  $s+1$ , then  $x$  would itself be a B stem endpoint and the claimed absence of  $x$  would fail.With those readings, the proof is sound.1. Full- $U$  classificationTranslate the proposed consumer site to  $x=(0,0)$ . The retained north and west neighbors are
$$(-1,0),\qquad (0,-1).$$
Any candidate original  $J$  must avoid all guards in  $G$ . Hence every endpoint neighbor of  $x$  belonging to  $J$  must lie in the east or south direction. In particular, the matching neighbor of  $x$  must be east or south.The endpoint graph of a full  $U(H,d,f)$ , up to lattice isometry, has the following classes.A leg terminal has degree one.A row-zero outer bar corner has degree two, with perpendicular neighbors.A nonterminal stem site has degree two, with opposite collinear neighbors.Every remaining bar site has at least three endpoint neighbors.The last two categories cannot occur at  $x$ . A nonterminal stem site has one neighbor in a forbidden direction after any orientation, because its two neighbors are opposite. A bar site of degree at least three cannot have all its neighbors among only east and south.Thus only three full- $U$  roles remain.Role 1: terminal with matching ray southThe incident leg contains
$$(0,0),(1,0),\ldots,(d,0),
\qquad d\ge 4.$$
Therefore  $(4,0)$  is occupied, and it is in the south guard strip.Role 2: outer bar corner with own neighbors east and southThe two perpendicular rays from the corner are mapped to east and south.The south ray is either:a stem ray of depth at least  $4$ , ora bar ray of length  $H-1\ge 5$ , since  $H\ge 6$ .In either case  $(4,0)$  is occupied. Hence this role also meets the south guard.Role 3: terminal with matching ray eastAfter exchanging the near and far legs if necessary, the incident leg is
$$(0,0),(0,1),\ldots,(0,d),
\qquad d\ge 4,$$
and the perpendicular bar occupies the two columns  $d-1,d$ , with breadth at least  $6$ .If  $d\ge q$ , then  $(0,q)$  is on the incident ray and meets the east guard.If  $d<q$ , then  $d\le q-1$ . If the bar points north, its endpoint  $(-1,d)$  lies in the north strip. If it points south, its breadth at least  $6$  reaches  $(4,d)$ , which lies in the south strip.Thus every possible full- $U$  role hits  $G$ .The argument does not use a component-size cutoff, a search bound, or a restriction on the unused leg length. It covers every legal even  $H\ge 6$  and every  $d,f\ge4$ .2. Rotor classificationFor the standard rotor, the four degree-one tips are the only possible locations for  $x$ . Every non-tip endpoint has at least three endpoint neighbors, so after placing it at  $x$ , at least one neighbor lies north or west and immediately collides with a retained guard.There are eight normalized tip placements whose matching direction is east or south. Four are already impossible because they contain an immediate north or west neighbor. For example, the four discarded normal forms include endpoint sets of the following types:
$$\begin{aligned}
&\{(-1,-1),(0,-1),(0,0),(0,1),(1,-2),(1,-1),(1,0),(2,0)\},\\
&\{(-2,-1),(-1,-1),(-1,0),(-1,1),(0,-2),(0,-1),(0,0),(1,0)\},\\
&\{(-2,1),(-1,-1),(-1,0),(-1,1),(0,0),(0,1),(0,2),(1,0)\},\\
&\{(-2,0),(-1,-2),(-1,-1),(-1,0),(0,-1),(0,0),(0,1),(1,-1)\}.
\end{aligned}$$
Each contains  $(-1,0)$  or  $(0,-1)$ , so each is excluded before the farther parts of  $G$  are used.The four surviving guard-compatible forms are exactly the table in the note:
$$\begin{array}{c|c|c}
\text{matching direction}
& \text{endpoint set relative to }x
& \text{forced guard collision}\\
\hline
\text{south}
&
\{(0,0),(1,0),(1,1),(1,2),(2,-1),(2,0),(2,1),(3,1)\}
&
(2,-1)
\\
\text{east}
&
\{(-2,1),(-1,1),(-1,2),(-1,3),(0,0),(0,1),(0,2),(1,2)\}
&
(-1,1)
\\
\text{south}
&
\{(0,0),(1,-2),(1,-1),(1,0),(2,-1),(2,0),(2,1),(3,-1)\}
&
(1,-1)
\\
\text{east}
&
\{(-1,2),(0,0),(0,1),(0,2),(1,1),(1,2),(1,3),(2,1)\}
&
(-1,2).
\end{array}$$
The first and third collisions are west guards with row coordinates  $2$  and  $1$ . The second and fourth are north guards with column coordinates  $1$  and  $2$ . Therefore all four are excluded for  $q\ge2$ , and in particular for the lemma’s  $q\ge3$ .So no rotor can contain  $x$  while avoiding  $G$ .The precise wording should therefore be that the table is the complete list of surviving east/south tip placements after the immediate north/west collisions have been discarded. With that interpretation, the rotor part is exhaustive.3. Transfer to the depth-eight root prefixSet
$$x=(a-12,s+1),\qquad q=u+12,\qquad C=s+u+13.$$
The translated guard set is
$$\begin{aligned}
G_x^{N}
 &=\{(a-13,s+1+c):0\le c\le u+12\},\\
G_x^{E}
 &=\{(a-12,C)\},\\
G_x^{S}
 &=\{(a-8,s+1+c):0\le c\le u+11\},\\
G_x^{W}
 &=\{(a-12,s),(a-11,s),(a-10,s)\}.
\end{aligned}$$
Each part is supplied by a retained original.North stripThe points
$$(a-13,s+1),\ldots,(a-13,C)$$
are on B’s row-one bar.East guardThe point
$$(a-12,C)$$
is B’s far stem endpoint.South stripThe points
$$(a-8,s+1),\ldots,(a-8,C-1)$$
are on P0’s row-zero bar.West guardsFor
$$A=U(L,8,f)$$
with chart
$$(a-12+r,s+1-c),$$
the near column is  $c=1$ , hence the points
$$(a-12,s),\quad (a-11,s),\quad (a-10,s)$$
are A endpoints.The proposed support  $x$  is A’s local bar-exterior point  $(0,0)$ . Since A’s row-zero and row-one bars begin at local  $c=1$ , and its legs are also at  $c=1$  or  $c=L$ ,  $x$  is not an A endpoint.It is also absent from the other retained endpoint sets under the stated root coordinates:H3 endpoints begin at row  $a-8$  or below.R has endpoint columns at least  $C$ .B’s row  $a-12$  contains only its two stem endpoints, at the previously defined stem columns  $s_1$  and  $C$ ; the application requires  $s_1\neq s+1$ .The last point is the coordinate detail that must be explicit. If  $s_1=s+1$ , then  $x=(a-12,s+1)$  is B’s near stem endpoint and the absence claim is false. The proof is valid when  $s_1$  is the distinct prior root coordinate and  $s+1$  is merely the left endpoint of the retained bar subinterval.4. Why a complete extension would require a new owner of  $x$ The retained originals occupy the north and west neighbors of  $x$ . The west neighbor belongs to A itself, but it is still a retained endpoint and is foreign to any additional consumer  $J$ .Because  $x$  is an original support absent from the retained full endpoint union, the complete-feasibility rule cannot leave it absent with the retained occupancy pattern. Therefore any complete extension must introduce a distinct original  $J$  having  $x$  as an endpoint.Endpoint-disjointness implies that  $J$  avoids every retained endpoint, hence in particular every point of  $G_x$ . But the translated geometric lemma says that no full permitted  $U$  and no standard rotor can contain  $x$  while avoiding  $G_x$ .Therefore:
$$\boxed{\text{No complete full-}U/\text{rotor extension can contain the depth-eight }A\text{ prefix}.}$$
This is a conditional nonexistence result for extensions containing that fixed prefix. It does not assert that any complete extension of the surrounding root data exists.5. Conditional arithmetic- $54$  corollaryNow assume the prior root-triple classification and exact ledger, including the inherited parameter bounds
$$u\ge12,\qquad v\ge12,$$
and the ledger identity
$$\Delta\Phi(\{B,R,A\}\mid H_3)
=(u+v+25)+(L-1-\varepsilon),
\qquad
\varepsilon=[L=v+12].$$
Equivalently,
$$\Delta\Phi
=u+v+L+24-\varepsilon.$$
The cavity theorem removes the depth-eight actual owner from every complete extension containing B. Thus only the previously classified d4 and d6 cases remain.Case  $\varepsilon=0$ Since  $L\ge6$ ,
$$L-1-\varepsilon=L-1\ge5,$$
and therefore
$$\Delta\Phi
\ge u+v+25+5
=u+v+30
\ge 12+12+30
=54.$$
Case  $\varepsilon=1$ Here
$$L=v+12,$$
so
$$L-1-\varepsilon
=(v+12)-2
=v+10.$$
With  $v\ge12$ , the marginal is at least  $22$ . In fact,
$$\Delta\Phi
=u+v+(v+12)+24-1
=u+2v+35
\ge 12+24+35
=71.$$
Thus the note’s weaker uniform statement is valid:
$$\boxed{
\Delta\Phi(\{B,R,A\}\mid H_3)\ge u+v+30\ge54.
}$$
The  $54$  bound is therefore correct conditionally on the prior root-triple ledger and its  $u,v\ge12$  parameter bounds.If  $v\ge12$  is not part of those inherited hypotheses, then the arithmetic- $54$  conclusion would need revision: the displayed local cavity constraints alone only give  $u\ge12$  and  $6\le L\le v+12$ . For example, the formal local values  $u=12,v=0,L=6,\varepsilon=0$  give  $42$ , not  $54$ . That is not a counterexample to the conditional corollary when the prior ledger includes  $v\ge12$ ; it only identifies the required inherited premise.The result does not establish sharpness, extension existence, a global monotonicity theorem, an arbitrary-grid catalogue exhaustion, or any global improvement beyond this conditional root-triple statement.
