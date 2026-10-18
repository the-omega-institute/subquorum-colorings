# Exact structure when all regular slack comes from selected isolates

19 October 2026. The [compensation theorem](CUBIC_STABILITY_COMPENSATION.md)
reduces the gap problem to interactions involving selected isolates. This
note characterizes the entire zero-residual-capacity stratum, rather than
only the separated-block examples. No general sharp stability theorem is
claimed.

## Characterization

Let G be finite, simple, cubic and bipartite, and let S be a minimal
two-star-forming set. Put z equal to the number of selected isolates and
delta=3|V(G)|-5|S|. Then delta=z if and only if G and S have the following
partition and neighborhoods. Empty classes are allowed.

- S is the disjoint union I,P,H2,H3,U. I consists of selected isolates,
  P induces a matching, and U consists of selected leaves attached to H3.
- H=H2 union H3 induces a two-regular graph, hence a disjoint union of
  even cycles. Vertices of H2 have selected degree two, and vertices of
  H3 each have one additional selected leaf in U.
- T=V minus S is partitioned into X1,X2,Y according to selected degree
  one, two and three.
- The paths h--u--x give bijections H3<->U<->X1. Each u has its third
  neighbor in Y. Each x in X1 has no other selected neighbor.
- H2<->X2 is a bijection through edges. Each x in X2 has one selected
  neighbor in H2 and one in I. A vertex of I may serve several different
  X2 vertices, but has only three incident edges in total.
- Every remaining edge from I goes to Y. Every P vertex has its mate
  and two Y neighbors. Each Y vertex has all three neighbors in
  I union P union U.
- The outside graph on X1 union X2 has degree two at X1 and degree
  one at X2. Thus it is a disjoint union of even cycles entirely in X1
  and paths whose distinct endpoints lie in X2 and whose internal
  vertices lie in X1. Direct X2--X2 edges are allowed. Y is independent
  and has no edges to X1 union X2.

## Necessity

Use an injective high failure map and the notation A,B,C,r1,r2,E,g2
of the compensation proof. Its exact slack identity gives

    delta=z+A+C+2r1+r2.

If delta=z, every term A,C,r1,r2 is zero. Therefore every selected
degree-two high vertex has an adjacent degree-two witness, whose other
selected neighbor is an isolate. Every selected degree-three vertex
has a nonadjacent degree-one witness supported through a selected leaf.
There are no other outside vertices of selected degree one or two:
all are used by the chosen high map. Thus X1=f(H3) and X2=f(H2).

Every selected leaf has its own adjacent failure witness. Degree-two
leaf witnesses cannot be chosen high witnesses, so r2=0 excludes them.
The remaining private degree-one witnesses belong to X1=f(H3), and
each such vertex has just one selected neighbor. This gives an injection
U->X1. In the other direction, each H3 witness requires a leaf supported
by that H3 vertex; distinct supports have distinct leaves. Hence

    |H3|<=|U|<=|X1|=|H3|.

Equality forces the claimed H3<->U<->X1 bijections, exactly one leaf
at each H3 vertex, and no selected leaf supported by H2. The remaining
selected degree-one vertices form the matching P. Removing those unique
leaves from H3 leaves degree two at every vertex of H2 union H3.

Each H2 vertex has only one outside neighbor, its chosen X2 witness.
Each X2 vertex has exactly that high neighbor and one isolate. By the
bijections every U vertex uses precisely one X1 neighbor; its remaining
outside edge can reach neither X1 nor X2 and therefore reaches Y.
The same selected-neighbor descriptions force all remaining P and I
edges to Y and exclude any H neighbor at Y. Cubicity gives the stated
outside degrees. A finite simple graph with degrees one and two has
exactly the stated cycle and path components. Bipartiteness makes the
cycles even. This proves every structural assertion.

## Sufficiency and exact accounting

Conversely, suppose a cubic bipartite graph has this partition. The
selection S=I union P union H2 union H3 union U is star-forming:
X1 vertices are leaves supported by U--H3, X2 vertices have their H2
and I neighbors, and Y vertices have three selected neighbors.

Deleting an I vertex uncovers itself. Deleting a P vertex uncovers
itself, because its mate then has no selected neighbor. Deleting an
H2 vertex uncovers its associated X2 vertex, which is left with an
isolated selected neighbor. Deleting either h in H3 or its leaf u
uncovers the associated X1 vertex. These witnesses prove minimality.

Write b=|H2|, h=|H3|=|U|=|X1|, p=|P|, y=|Y|. The bijection gives
|X2|=b. Counting Y incidences from the selected side yields

    3y=h+2p+3z-b,
    |S|=z+p+b+2h,
    n=z+p+2b+3h+y.

Substitution gives3n-5|S|=z, proving the converse. In particular b<=3z,
and the fully general structure specializes to the earlier regular
equality partition when z=0: then b=0 and all high vertices have degree
three in the selected graph.

There is also a forced balance not apparent from the selected cycles
alone. Let b_L,b_R and h_L,h_R count H2 and H3 on the two sides.
The selected two-regular graph gives b_L+h_L=b_R+h_R. The outside
degree sums give2h_L+b_R=2h_R+b_L, since X1 has the color of its
associated H3 vertex and X2 the opposite color to its H2 vertex.
Combining the two equations yields

    b_L=b_R, h_L=h_R, b<=6 min(|I intersect L|,|I intersect R|).

The last bound follows from the X2-to-I incidences, with at most three
per isolate. In particular, a single selected isolate forces b=0 and
the two exchanges already attain |S|; having |S|>beta_2 in this stratum
requires isolates in both parts. This is a general balance argument,
not an inference from the 300 sampled instances.

## Why this is the next sharp case

On this entire stratum the desired sharp exchange would construct a
dissociation set of size at least |S|-z/2. The present two exchanges
guarantee only |S|-b/2, with b<=3z. The selected high cycles can mix
H2 and H3 arbitrarily subject to the displayed neighborhoods; the
outside components can independently be paths or cycles. Treating the
Heawood and regular equality cores as disjoint selected components
therefore omits genuine residual configurations.

The 300 mixed-cycle discovery controls instantiate the case z=2,b=6,
p=0,h=6k,y=2k with one mixed high cycle. Their recorded integer
optima do not supply a proof for all path/cycle systems. The general
classification above follows from the exact slack and injective witness
arguments, independently of those computations.

The independent compensation checker tests this structure whenever a
controlled minimal selection has delta=z, including z=0 and the explicit
large families. This classification is a written theorem, not newly
Lean-formalized. It was derived after the original compensation-review
input and is outside that review's scope unless separately stated.
