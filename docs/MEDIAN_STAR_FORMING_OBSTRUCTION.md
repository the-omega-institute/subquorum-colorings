# A star-forming gap in median graphs of maximum degree five

For every integer r>=1 there is a connected median graph G_r with

    |V(G_r)|=38r,  Delta(G_r)=5,
    beta_2(G_r)=21r,  SF_2(G_r)>=22r.                    (1)

Thus the assertion that SF_2=beta_2 on all finite median graphs is false,
even with a fixed maximum degree. The proof gives every deletion witness
and an elementary exact dissociation bound. The graphs have pendant
vertices and are not rectangular grids; the rectangular-grid equality
remains a separate question. No exact value of SF_2(G_r) is asserted.

## 1. Definitions and the 38-vertex graph

A dissociation set A induces maximum degree at most one; beta_2 is its
maximum size. A set S is forming when each x outside S has at least two
neighbours in S, or a neighbour y in S having a neighbour in S. This is
formation by a non-induced K_(1,2). The upper star-forming number SF_2 is
the maximum size of an inclusion-minimal forming set. Formation is upward
closed, so a forming set is minimal exactly when every single deletion
fails. The deleted vertex is among the outside vertices to be checked.

A connected graph is median if every triple has a unique vertex in the
intersection of its three pairwise shortest-path intervals.

Start with B=P_4 square P_4 square K_2, with vertices (x,y,z), where
0<=x,y<=3 and z is zero or one, and Manhattan adjacency. Put

    C={(0,0),(3,0),(0,3)},
    D={(x,y,0):(x,y) in C}.

At each vertex of D add two pendant leaves. Their union L has size six.
Call the resulting graph G. It has 38 vertices and maximum degree five.
The three points of C have pairwise distances 3,3,6. They are independent,
and every base-grid vertex has at most one neighbour in C.

The certificate uses labels ell(x,y,z)=8x+2y+z. The new leaves 32,33
attach at 0; leaves 34,35 attach at 24; leaves 36,37 attach at 6.
These rules specify the entire graph without an implicit edge choice.

## 2. Medianity and minimal formation

Distances in B are coordinatewise Manhattan distances. Its intervals are
coordinate boxes, so coordinatewise median is the unique median of any
triple. Adding a pendant vertex preserves medianity. To see this directly,
project each leaf to its attachment vertex and fix B. For two distinct
vertices a,b, the B part of their interval is the interval of their
projections in B. No leaf can lie on a shortest path between two other
vertices. For three distinct vertices the median therefore lies in B
and is the coordinatewise median of their projections. A repeated vertex
is itself the unique median. This also covers two leaves at one attachment.

Select

    S_L={(x,y,0):(x,y) not in C},
    S_U={(x,y,1):(x,y) in C},
    S=S_L union S_U union L.

Its size is 13+3+6=22. Every base-grid vertex has degree at least two and
at most one neighbour in C. Hence every vertex of S_L has a neighbour
in S_L. Vertices of S_U and L are isolated in G[S]. An outside lower
vertex is in D and has two selected leaves. An outside upper vertex has
its active lower rung neighbour. Thus S is forming.

For s=(x,y,0) in S_L, deletion leaves its upper mate x_s=(x,y,1)
unformed: the only possible remaining selected neighbours of x_s are
upper copies of neighbours in C. There is at most one, and it is isolated
in the remaining selected graph. For s in S_U or L, the deleted vertex
itself has no remaining selected neighbour. These are witnesses for all
22 deletions, proving inclusion-minimality and SF_2(G)>=22.

Numerically the thirteen lower selected vertices are

    2,4,8,10,12,14,16,18,20,22,26,28,30;

their witnesses are s+1. The other selected vertices are

    1,7,25,32,33,34,35,36,37;

each is its own witness.

## 3. Exact dissociation bound for the punctured prism

Let F=B-D. We prove beta_2(F)=15.

First classify the four-vertex dissociation sets in a cube Q_3, with local
coordinates (u,v,w) in {0,1}^3. Each square face has at most two selected
vertices. Each vertex belongs to three of the six faces, so
3|A|<=6*2=12 and |A|<=4. If a four-set
contains an edge, its endpoints exclude their other four neighbours;
the remaining two vertices form the opposite parallel edge. Otherwise
the set is independent. Its twelve incident edges account for every
cube edge, so its complement is also independent; connectedness forces
one of the two bipartition classes. The complete list is therefore

| Type | Selected condition, modulo two | Induced edges |
| --- | --- | --- |
| P | u+v+w=epsilon | None |
| X | v+w=epsilon | Two parallel u-edges |
| Y | u+w=epsilon | Two parallel v-edges |
| Z | u+v=epsilon | Two parallel w-edges |

Each epsilon is zero or one. In a type X,Y,Z set every selected vertex
already has its one allowed selected neighbour inside its cube.

Partition B into four disjoint cubes

    B_ij={(2i+u,2j+v,w):u,v,w in {0,1}}, i,j in {0,1}.

A dissociation set in F has size at most sixteen. If it has size sixteen,
it uses a four-set from the table in every cube. We now exclude this.

Across an x boundary, the selected halves of the left face u=1 and right
face u=0 have respective equations

| Type | Left | Right |
| --- | --- | --- |
| P | v+w=epsilon_L+1 | v+w=epsilon_R |
| X | v+w=epsilon_L | v+w=epsilon_R |
| Y | w=epsilon_L+1 | w=epsilon_R |
| Z | v=epsilon_L+1 | v=epsilon_R |

When at least one side is X,Y,Z these halves must be disjoint, since
otherwise an already saturated selected vertex gains another neighbour.
Different functions among v+w,w,v give halves intersecting in one point.
Equal functions give disjoint halves exactly when their values differ.
Consequently the only possible ordered pairs and necessary phases are

| Left/right type | Phase condition |
| --- | --- |
| P/P | Any |
| P/X | epsilon_R=epsilon_L |
| X/P | epsilon_R=epsilon_L+1 |
| X/X | epsilon_R=epsilon_L+1 |
| Y/Y | epsilon_R=epsilon_L |
| Z/Z | epsilon_R=epsilon_L |

For a y boundary interchange X and Y. These are necessary conditions;
the P/P entry still requires the full degree condition at vertices
meeting both boundaries.

If some cube has type Z, both its neighbours are Z with the same phase,
so all four cubes are Z with one phase. Avoiding (0,0,0) requires phase
one, while avoiding (3,0,0) requires phase zero, a contradiction.

If a cube has type X, its y neighbour must be X with the same phase.
The other column consists of P or X cubes. Its two types must agree,
because a P/X pair is forbidden across a y boundary. Their phases agree
as well, directly for X/X or by the identical horizontal relations to
the first column for P/P. Hence the left column, containing the two
deleted vertices with x=0, has one type P or X and one phase. Avoiding (0,0,0) requires phase one; avoiding (0,3,0)
requires phase zero. This is impossible. The case with a Y cube follows
by interchanging x,y and uses (0,0,0),(3,0,0).

The remaining case has four P cubes. Avoiding the deleted vertices forces

    epsilon_00=1, epsilon_10=0, epsilon_01=0.

Then (1,1,1), (2,1,1), (1,2,1) are all selected. The first has the other
two as neighbours, a final contradiction. Thus beta_2(F)<=15.

The even-parity vertices of B other than (0,0,0) form an independent
15-set in F; the other two deleted vertices have odd parity. This proves
beta_2(F)=15.

## 4. Exact beta_2 and connected amplification

For any dissociation set A in G, its intersection with the attachment
vertex and its two leaves has size at most two. Remove the three
attachment vertices and all chosen leaves, then insert all six leaves.
The result is a dissociation set of size at least |A|: its other vertices
form a dissociation set of F and the leaves are isolated. Therefore

    beta_2(G)=6+beta_2(F)=21.

Now take r disjoint copies G^(1),...,G^(r) and add the r-1 edges

    34 in copy i -- 32 in copy i+1, 1<=i<r.             (2)

Call the result G_r. Each leaf is used in at most one new edge. Each new
edge is a bridge between successive copies. Gluing median graphs by a
bridge preserves medianity: for a triple all in one component the median
is unchanged; for two in one component and the third in the other, its
median is the median of the two vertices and that component's bridge
endpoint. Every shortest path crossing the cut uses the bridge, which
proves both interval membership and uniqueness. Apply this inductively.
The old degree-five attachment vertices keep their degree; bridge leaves
have degree two. Thus G_r is connected median with maximum degree five.

The union S_r of the r displayed forming sets has size 22r and is forming
by the old certificates. The old upper-mate witnesses for lower selected
vertices remain valid; no added edge touches them or the upper selected
isolates. An unbridged selected leaf still witnesses its own deletion.
A bridged selected leaf, when deleted, has just its selected bridge mate
as a selected neighbour; that mate is then isolated, because its attachment
vertex is unselected and it has no second bridge. It too witnesses its
own deletion. Upper selected vertices retain their self witnesses.
This proves minimality of S_r for every r.

For beta_2, simultaneously remove every attachment vertex and replace the
selected leaves by all 6r leaves. Every attachment cluster contained at
most two selected vertices, so cardinality cannot decrease. The inserted
leaves induce exactly the matching (2), with no edges to the remaining
core vertices. The remaining graph is a disjoint union of r copies of F.
The resulting set has size at most 6r+15r=21r. Conversely take the
independent 15-set of F in each copy and all leaves: their only selected
edges are the bridges, so they form a dissociation set of size 21r.
This proves (1). The normalization is simultaneous; it does not assume
that individual insertions preserve dissociation before all centres
have been removed.

## 5. Verification and scope

Run `python3 scripts/check_median_obstruction.py`. This standalone checker
uses no other project modules. It checks physical adjacency, all triples
in four family members (r=1,...,4), the exact eight
four-vertex cube patterns, every combination of those patterns in the
punctured prism, all displayed formation/deletion witnesses, and larger
members of the connected family. Machine-readable coordinates and full
witnesses are in `output/median-obstruction-certificates.json`.

The proof establishes a separation SF_2>=22r>21r=beta_2, not an exact
SF_2 value or an optimal median-graph gap coefficient. The fixed graph
was obtained in an Oracle research response and reconstructed here; the
bounded-degree connected amplification is proved above. An independent
review accepted the complete all-r proof and inspected the checker source.
That reviewer did not execute the checker; the reported finite execution
is local. The note incorporates the recommended explicit face-incidence
count and column orientation. The complete response, reviewed source hashes
and execution scope are recorded in `output/median-obstruction-review.json`.
There is no new Lean verification or historical priority claim.
