# Degree stability, minimum-degree sharpness and the first equality graph

11 November 2026. Throughout, graphs are finite, simple and bipartite;
two-star formation is non-induced and minimality is by inclusion.
Write g=SF_2(G)-beta_2(G), n=|V(G)| and n_2 for the number of vertices
of full graph degree two. Use the accepted general witness decomposition in
[the sharp gap proof](SHARP_BIPARTITE_STAR_FORMING_GAP.md).

## A bound using actual degree-two vertices

**Theorem 1.** If the minimum degree is at least two and the maximum degree
is at most an integer D>=2, then

    (10D+2)g <= D n+n_2.                                      (1)

More generally, if the minimum degree is at least d>=2, then

    (10D+2d-4)g <= D n.                                       (2)

Integer parts may be taken. These are degree-sensitive refinements of the
universal n/10 ceiling, not claims of best possible constants for fixed D.
The earlier regular bound n/(4d+2) is stronger when d=D>=3.

**Proof.** Choose a maximum-cardinality minimal forming set S and use
R,p,u,a,b from the general proof. All p chosen supports and p chosen
leaves have been removed before defining the u residual owners. Let

    m=min(a,p), e=u-a-2b, r=|R|-a-b,
    q=n-|S|-p-u, t=m+b-2g.

All five quantities e,r,q,t,m are nonnegative. The pair/triple disjointness
and the two dissociation exchanges prove this; in particular q counts
outside vertices not chosen as witnesses. The exact count gives

    L:=n-10g = r+[3a+3p-5m]+2e+q+5t >= 2e+q.                 (3)

Here 3a+3p-5m>=0. Thus D L>=Dq+e.

A touched selected isolate has no selected neighbour. No chosen triple
witness meets it. Each chosen pair witness meets at most one selected
isolate, and the q remaining outside vertices supply at most Dq total
incidences to the touched isolates. Consequently

    sum_(i touched) deg_G(i) <= u+Dq.                         (4)

Under minimum degree two, among the b multiply touched isolates at most
n_2 have full degree two. Therefore the left side of (4) is at least
2(a+b)+(b-n_2); if b<n_2 this deliberately weaker expression is still
valid. Substituting u=a+2b+e gives

    a+b-n_2 <= e+Dq,
    2g <= m+b <= n_2+e+Dq <= n_2+D L,

because m<=a. This proves (1).

If minimum degree is d, (4) instead gives

    d(a+b) <= a+2b+e+Dq,
    (d-2)(m+b) <= Dq+e-[(d-1)a-(d-2)m] <= Dq+e.

The bracket is nonnegative because a>=m and d>=2. Hence
2(d-2)g<=Dq+e<=D L, proving (2). Each outside vertex is charged by
its actual degree bound once; no incidence is reused across isolates.

## Minimum degree alone cannot improve the asymptotic coefficient

**Theorem 2.** For every fixed integer d>=3 there is a sequence of
two-connected bipartite graphs with minimum degree at least d for which

    g/n -> 1/10.

Thus 1/10 remains the optimal asymptotic coefficient under any fixed
minimum-degree condition, when the maximum degree is unrestricted.
No positive unrounded equality graph has minimum degree three, as proved
in the general equality ledger. Asymptotic sharpness and exact equality
therefore have different answers.

**Construction and proof.** Let s=d-2 and take r>=d disjoint copies of H.
In copy j distinguish the selected isolates I_j={a3,b3}, the selected
support set C_j={a1,a2,b1,b2}, and W_j={a4,a5,b4,b5}.
The C_j and W_j each induce K_(2,2). Each W vertex meets precisely its
own support and its own isolate in S_j=I_j union C_j.

Add s new vertices on each bipartition side, denoted Q_A,Q_B. Join every
Q_A vertex to every b3, and every Q_B vertex to every a3. Complete the
bipartite graph between all C_A,C_B, and separately between all W_A,W_B.
No edge is added between I and C, or between W and S. The copies of H
remain induced. The resulting graph has

    n=10r+2s, beta_2=5r+s, SF_2>=6r,
    r-s <= g <= floor((10r+2s)/10).                           (5)

Every isolate now has degree d. Each C vertex has degree 2r+1, each W
vertex has degree 2r+2, and each Q vertex has degree r. Minimum degree
is therefore at least d. The two sides have equal size 5r+s.

The union S of the S_j is forming. Old omitted W vertices still have
their same two selected neighbours, and each new Q vertex has r selected
isolate neighbours. The six deletion failures in each block remain:
a deleted support leaves its W witness with only an isolated selected
neighbour, and a deleted isolate itself has no selected neighbour.
All new edges preserve these facts. Thus S is minimal and has size 6r.

To prove the exact dissociation number, each H contributes at most five.
If a dissociation set meets at most one of Q_A,Q_B, the bound 5r+s follows.
If it meets both, it contains at most one selected a3 in total and at
most one selected b3 in total: either is adjacent to every selected Q
vertex on the opposite side, so selecting two such isolates would give
one of those Q vertices degree at least two. Thus at most two copies
contain any selected isolate. Each other copy contributes at most four,
since deleting both isolates leaves two disjoint K_(2,2) subgraphs and
each contributes at most two. The total is at most

    4r+2+2s <= 5r+s,

where r>=s+2=d. A whole bipartition side attains 5r+s.

Each H has the Hamilton cycle displayed in the composition theorem, so
a vertex deletion leaves its block connected. The Q vertices link all
blocks through both isolate classes. Deleting a block vertex removes at
most one of these two kinds of attachment from that block. If a Q vertex
is deleted and s=1, the surviving opposite-side Q vertex still connects
all blocks. If s>1, vertices of both Q classes remain. Every surviving Q
vertex has neighbours in at least r-1 nonempty blocks. Thus the entire
graph stays connected after every vertex deletion and is two-connected.
Dividing (5) by n and using the universal upper bound proves the limit.

## The unique ten-vertex positive equality graph

Bhattacharjee (v1.1.0, final computational remark) previously reports
uniqueness by exhaustive search through order ten. Here it follows by a
structural argument from the universal equality ledger.

**Theorem 3.** Up to graph isomorphism, H is the only bipartite graph of
order ten with SF_2-beta_2=1.

**Proof.** The equality ledger in the general proof forces p=a=0,
b=2, u=4, |R|=2, q=0, |S|=6 and beta_2=5. Both selected isolates
have exactly two outside witness neighbours, and each of the four other
selected vertices has exactly one such witness. Every outside vertex
has exactly its owner and its isolate as selected neighbours.

If b_A,b_B count the isolates on the two bipartition sides, the numbers
of vertices on those sides are 3b_A+2b_B and 2b_A+3b_B. Since each side
is an independent set of size at most beta_2=5, b_A=b_B=1. There are two
supports and two witnesses on each side. Relabel them as in H so all
isolate--witness and owner--witness edges agree with H. Every possible
remaining edge lies within the support graph C or the witness graph W;
each of those is a bipartite graph on two vertices per side. Thus G is a
spanning subgraph of H, differing only by possible deletion of its eight
C/W edges.

The owner pairs are a1--b5, a2--b4, b1--a5 and b2--a4. The two
permutations (a1 a2)(b4 b5) and (b1 b2)(a4 a5), fixing all other
vertices, are automorphisms of H. They act transitively on its four C
edges and, separately, on its four W edges. Deleting a1--b1 from H
admits the dissociation six-set

    {a1,a2,a3,a4,b1,b3},

whose only edges are a2--b1 and a4--b3. Deleting a4--b4 admits

    {a1,a3,a4,b1,b3,b4},

whose only edges are a1--b1, a3--b4, a4--b3.
Further edge deletions preserve these witnesses. Thus any missing C or
W edge forces beta_2>=6, a contradiction. Hence G=H. The established
parameters of H prove the converse.

## Equality beyond four-attachment copies of H

**Theorem 4.** For every r>=2 there is a two-connected bipartite graph
L_r with n=10r, beta_2=5r and SF_2=6r, having no vertex of degree four.
In particular the four-attachment H compositions do not exhaust the
positive equality graphs.

**Construction.** Take a complete bipartite support graph C=K_(2r,2r),
whose sides are {a_(j,0),a_(j,1)} and {b_(j,0),b_(j,1)}, 1<=j<=r.
For each j add a six-cycle in this cyclic order:

    i_j, y_(j,0), x_(j,0), k_j, x_(j,1), y_(j,1), i_j.

Here i_j,x_(j,0),x_(j,1) are on the A side, and k_j,y_(j,0),y_(j,1)
are on the B side. Add the four owner edges a_(j,t)--y_(j,t) and
b_(j,t)--x_(j,t), t=0,1. There are no other edges. The selected set S
consists of C and all i_j,k_j.

**Proof.** Each omitted x or y has its selected owner and selected
isolate as neighbours. Deleting an owner leaves its witness with only
its isolated neighbour; deleting i_j or k_j leaves that newly omitted
vertex with no selected neighbour. Thus S is minimal forming and
SF_2>=6r.

We first prove a local bound. A six-cycle with two pendant vertices
attached to the two y vertices has dissociation number five. Its parts
have sizes five and three. In a hypothetical six-set the part sizes
must be (5,1), (4,2) or (3,3). In (5,1) the selected vertex on the
three-side has degree at least two. In (4,2), at least one of the two
selected vertices on that side is a y vertex, which has degree three;
omitting just one opposite vertex cannot reduce its selected degree
below two. In (3,3), the two x vertices and the i vertex each have two
neighbours on the fully selected three-side, leaving only the two
pendant vertices eligible, a contradiction. A whole five-side attains
five. Also a six-cycle has dissociation number four: each selected
triple of consecutive vertices is forbidden, and summing the six
three-window inequalities gives 3|D|<=12.

Now consider a global dissociation set D. If D meets both sides of C,
it uses at most one vertex of each, since C is complete bipartite.
Each of the r six-cycles contributes at most four, giving

    |D|<=4r+2<=5r.

If D meets only the A side of C, partition the graph vertices that
remain available into r disjoint modules, each comprising one six-cycle
and its two a owner vertices. The local eight-vertex bound gives at
most five per module. The B-only case is symmetric; the case with no
selected support uses at most 4r. Thus beta_2<=5r. A whole bipartition
side has size 5r, so beta_2=5r. The universal upper bound then forces
SF_2<=6r, proving both exact values.

The support graph remains connected after any single vertex deletion.
Each six-cycle remains connected after an internal deletion and retains
at least three of its four owner attachments; after a support deletion
it retains the other three attachments. Thus every surviving module
is connected to the surviving support graph, proving two-connectivity.
The degrees are 2 at i_j,k_j, 3 at x_(j,t),y_(j,t), and 2r+1 at every
support. None is four for r>=2. Every four-attachment H composition
retains the four nonattachment degree-four vertices in each H copy,
so it cannot be isomorphic to L_r.

## Scope

Theorem 1 does not determine sharp constants for every bounded degree
range. Theorem 2 settles the optimal asymptotic coefficient when only
minimum degree and two-connectivity are imposed. Theorem 3 classifies
only the smallest positive unrounded equality order. Theorem 4 refutes
the candidate restriction to the earlier H compositions. The accompanying intrinsic-equality note gives a complete global
neighbourhood recognition criterion and the complete-core classification.
Simpler local criteria for arbitrary incomplete cores and the optimal
connected cubic coefficient remain separate research questions.
