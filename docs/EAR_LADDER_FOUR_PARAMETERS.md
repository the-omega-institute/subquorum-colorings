# Exact four-parameter separation in outerplanar median graphs

For every r>=1 we construct a two-connected outerplanar median graph H_r
of maximum degree four and order16r with

    beta_2(H_r)=sf_2(H_r)=SF_2(H_r)=8r,
    psi_sq(H_r)=Omega(H_r)=9r.                              (1)

Thus the equality of upper star-forming and dissociation numbers does
not force equality with the sub-quorum number, even under these simultaneous
structural restrictions. The gap psi_sq-SF_2 is exactly |V(H_r)|/16.

## 1. Definitions and construction

A dissociation set induces maximum degree at most one; beta_2 is its
maximum size. A selected set S is forming if each outside vertex has
two neighbours in S, or a selected neighbour which itself has a selected
neighbour. The largest and smallest sizes of inclusion-minimal forming
sets are SF_2 and sf_2. The deleted vertex is tested in minimality.

In a partial sub-quorum colouring, each coloured vertex has at least half
of its coloured closed neighbourhood in its own colour. The maximum
number of nonempty colours is psi_sq. A feasible representative pair
(M,T) has a matching M, its endpoint set P, and T disjoint from P, with
each t in T having at most one neighbour in T union P. Write

    Omega=max (|T|+|M|).

Always beta_2<=psi_sq<=Omega. For the first inequality colour each
vertex of a dissociation set separately. For the second, retain one
edge from every colour class containing an edge and one vertex from
every edge-free class. A retained singleton originally had no same-colour
neighbour, so sub-quorum forces at most one other coloured neighbour.
It therefore has at most one neighbour in the retained support.
The retained vertices and edges give a feasible pair with one unit per
colour. The upper bound below applies even when the retained edge
endpoints do not themselves form a sub-quorum colouring.

Put n=4r. Start with the two-row ladder with old vertices (i,j),
i in {0,1}, 0<=j<n. Its edges are row edges (i,j)(i,j+1) and rungs
(0,j)(1,j). For each i and 0<=s<n/2, add distinct a_(i,s),b_(i,s) and
the path

    (i,2s)-a_(i,s)-b_(i,s)-(i,2s+1),

retaining the old row edge. Call the resulting square Q_(i,s). These
n squares partition all4n=16r vertices. No new vertex has an outside
neighbour. This fully specifies H_r.

Equivalently, H_r is the full4-by-4r grid with exactly the following
boundary edges removed: on each of its first and last rows remove the
edge between columns 2s+1 and 2s+2 for 0<=s<2r-1. To see the isomorphism,
send old (i,j) to row i+1, column j; send a_(0,s),b_(0,s) to row0,
columns2s,2s+1, and a_(1,s),b_(1,s) to row3 at those columns. All vertical
edges and both middle-row paths are retained, and the outer-row edges
are precisely the disjoint pairs. In particular H_1 is a4-by-4 grid
with just its top and bottom middle horizontal edges deleted.

## 2. Star-forming and dissociation values

Every dissociation set meets each square in at most two vertices,
since every three vertices of C_4 contain an induced degree-two vertex.
Selecting all new pairs gives n isolated selected edges. Hence
beta_2=2n.

Every minimal forming set selects exactly two vertices per square.
At least two are needed: a sole selected root leaves the opposite new
vertex without a selected neighbour, and a sole selected new vertex is
inactive and leaves the other new vertex unformed.

For at most two, write one square d-e-b-a-d. With d,e,a selected,
delete a; the active old edge d-e forms both omitted new vertices.
With d,a,b selected, delete b; the active edge d-a forms both b and e.
The cases with the other three-set are symmetric. With all four
selected, delete a; it sees d,b, and both selected roots stay active
through d-e. These deletions remove only a new vertex, and all selected
roots retain activity. Every outside star using that new vertex as a
leaf can therefore use a retained neighbour of its root instead.
No outside vertex loses formation. Thus three or four selections
contradict minimality.

Any two vertices of a square form its omitted vertices locally. Each
selected vertex also has a deletion witness among the two new vertices:
for pair {d,e} the witnesses are a,b; for {a,b} each deleted vertex
witnesses itself; for {d,a} the witness b works for either deletion,
and {e,b} is symmetric; for {d,b}, deleting d leaves a with the isolated
selected b, and deleting b leaves b without a selected neighbour;
{e,a} is symmetric. Outside edges cannot alter these failures.
Consequently all6^n choices of a pair per square are minimal forming,
each of size2n. This proves sf_2=SF_2=beta_2=2n=8r.

## 3. An upper bound for every representative pair

Let (M,T) be arbitrary feasible, and P=V(M). In each square Q write

    t_Q=|T intersect Q|, p_Q=|P intersect Q|,
    w_Q=t_Q+p_Q/2.

Since the squares partition the graph,

    |T|+|M|=sum_Q w_Q.                                    (2)

We classify the only way to have w_Q>2. Three T vertices in a square
would leave its middle T vertex with two T neighbours, impossible.
If t_Q=0, then w_Q<=2. If t_Q=1, at least one of the two neighbours
of that T vertex must be unoccupied, so p_Q<=2 and w_Q<=2.
If t_Q=2 and the two vertices are adjacent, their other neighbours
must be unoccupied; hence p_Q=0 and w_Q=2.

The only remaining case has two opposite T vertices. Each omitted
vertex is adjacent to both of them, so at most one omitted vertex is
in P. The case w_Q>2 is therefore exactly t_Q=2,p_Q=1,w_Q=5/2.
Its unique P vertex cannot be new: a new vertex has only the two T
neighbours, and could not belong to an M edge disjoint from T. Thus
the two old roots of such a square are occupied, one in T and one in P.
Call a square of this type exceptional, and let h be their number.

For each interval of columns {2s,2s+1}, the top and bottom ear-squares
cannot both be exceptional. If they were, the old T root in the top
square would have its old P root as one occupied neighbour and its
bottom rung neighbour, also occupied, as another. This violates
feasibility at that T vertex. There are n/2 such intervals, so h<=n/2.
Summing the local estimates in (2) gives

    |T|+|M|<=2n+h/2<=2n+n/4=9r.                          (3)

This charges every matching endpoint by one half, including endpoints
of edges joining different squares. It does not count one such edge
twice. Therefore Omega<=9r and psi_sq<=9r.

## 4. A colouring attaining the bound

Partition the old columns into r blocks {4j,4j+1,4j+2,4j+3}.
In block j choose row i=j mod2. Its two ear-squares are exceptional.
Select for T the old roots (i,4j),(i,4j+3), and the new vertices
b_(i,2j),a_(i,2j+1) adjacent to the two middle old roots.
In the other row select both new vertices of each ear-square for T.
Finally put the row edge

    (i,4j+1)(i,4j+2)

into M. Do this for every j. These r edges are disjoint and |T|=2n=8r.
All old roots in each block's other row are unoccupied, and the choice
of row alternates between consecutive blocks.

Each selected old T root sees only its own P root in the occupied
support: its rung neighbour is unoccupied, and at a block boundary
its row neighbour belongs to the adjacent block's unoccupied row, when
that adjacent block exists. Each
selected new T vertex in an exceptional square sees only its P root.
Every new T vertex in the other row sees only its selected new partner.
Thus (M,T) is feasible and has value8r+r=9r.

More strongly, give every vertex of T a different colour, and give
the two endpoints of each M edge one further colour unique to that
edge. A T vertex has a coloured closed neighbourhood of size two,
with one vertex of its own colour. Each P vertex has exactly three
coloured neighbours: its M partner, its own old T root and its selected
new T neighbour. Its coloured closed neighbourhood has four vertices,
two of its own colour. Hence every coloured vertex satisfies sub-quorum.
There are9r colours. Together with (3), this proves (1).

## 5. Structural restrictions

Adding a square along an old edge of a median graph preserves medianity.
It is the induced isometric subgraph of B square K_2 on

    (V(B) times {0}) union ({d,e} times {1}).

It is closed under the coordinatewise median: a median in layer one
requires two layer-one inputs, whose first coordinates are equal or
lie on the edge {d,e}; their interval median again belongs to {d,e}.
Thus successive attachments to the median ladder remain median.

Draw the ladder horizontally, with the new paths above its top row
and below its bottom row on disjoint intervals. This is an outerplanar
drawing with every vertex on the outer face. Adding a path between the
ends of an existing edge preserves two-connectivity: after deleting
either end, the surviving path still attaches at the other; after
deleting a new vertex, the old graph remains connected and the surviving
path pieces attach to it. This also covers all successive attachments.
Old ladder corners gain one neighbour and have degree three; all other
old vertices have degree four, and the new vertices have degree two.

For r>=1 the graph also has no automorphism sending each vertex to a
neighbour. In a corner ear the two new degree-two vertices would have
to be swapped, forcing their old neighbours of degrees three and four
to be swapped, impossible.

These graphs contain added square paths and are not full rectangular
grids. Formula (1) refutes a triple-equality extension to two-connected
outerplanar median graphs, while retaining SF_2=beta_2 on the entire
family. The rectangular-grid triple equality remains a separate question.
