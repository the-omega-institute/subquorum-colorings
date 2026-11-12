# A compact two-connected subcubic family

For every positive integer k there is a simple bipartite graph G_k and
a specified inclusion-minimal two-star-forming set S_k satisfying

    |V(G_k)|=64k, |S_k|=40k, beta_2(G_k)=39k,
    delta(G_k)=kappa(G_k)=2, Delta(G_k)=3.

The selected subgraph is the disjoint union of 8k copies of P_3 and
16k isolates. In particular its selected gap is exactly k=|V(G_k)|/64.
This improves the earlier 90-vertex-per-unit construction in
[TWO_CONNECTED_SUBCUBIC_SELECTED_STAR_GAPS.md](TWO_CONNECTED_SUBCUBIC_SELECTED_STAR_GAPS.md).
It leaves open the best coefficient in this degree and selected-component
class. It also gives SF_2(G_k)-beta_2(G_k)>=k; an exact value of the
unrestricted upper star-forming number SF_2(G_k) is not asserted.

Here beta_2(G) is the maximum size of a dissociation set, meaning a set
inducing maximum degree at most one. A set S is two-star-forming if every
vertex outside S lies in a copy of K_(1,2) containing exactly two vertices
of S. The copy need not be induced. Minimality means inclusion minimality.
These definitions follow R. Sahbi, *Upper k-Star-Forming Sets,
k-Independence, and Upper Domination*, arXiv:2610.03785. SF_2 is the
maximum size of such a minimal set.

We prove the more general formula

    n=16Lk, |S|=10Lk, beta_2=(10L-1)k

for every even L>=4 and every k>=1. Taking L=4 gives the stated family.

## The core and its exact dissociation number

Take 2L disjoint paths, indexed by j=0,...,2L-1,

    a_j - x_j - c_j - y_j - b_j - i_j.

For each h in {0,L}, add the chain edges

    a_(h+t) b_(h+t+1),  t=0,...,L-2,

and the two further edges

    a_(h+L-1) a_h,    a_(h+L-1) a_(h+L-2).

Finally add b_0 b_L. Denote this 12L-vertex graph by Q_L. The edge
e=a_1 a_(L+1) is optional for the next lemma. It is absent from Q_L
and present in Q_L+e. Both endpoints have degree two before e is added.
The specified core selection is {x_j,c_j,y_j,i_j:0<=j<2L}.

**Lemma 1.** beta_2(Q_L)=beta_2(Q_L+e)=8L-1.

**Proof.** Each path P_6 contributes at most four vertices. With the
path indexed 0,...,5, its six dissociation sets of size four are

    0134, 0135, 0145, 0235, 0245, 1245.

Normalize a four-set containing a to A={a,c,y,i}=0235. The unique
four-set omitting a is B={x,c,b,i}=1245. The normalization retains
only a subset of the interface vertices {a,b} and never increases
their internal selected degree. Only a and b have neighbours in other
blocks of Q_L or Q_L+e, so simultaneous normalization preserves
dissociation within either core. We do this before adjoining any
attachments at the i vertices.

Suppose that a dissociation set had size 8L. Every block contributes
four vertices, so normalize them all. An edge a_u b_v forbids A at u
and B at v: b_v in state B already has its selected neighbour i_v.
Consequently A at root h forces A in all L blocks of that group.
The vertex a_(h+L-1) would then have the two selected neighbours a_h
and a_(h+L-2), which are distinct since L>=4. This is impossible.
Both roots must therefore have state B. But b_0 b_L joins two
already saturated selected vertices. This is also impossible, and
beta_2<=8L-1 follows even without e.

For attainment take A in the first group and B in the second, and
omit a_(L-1). Call the resulting set D_Q. Its only potential extra
A-A edges in the first group both meet the omitted vertex. Every
chain edge has its b endpoint omitted in that group, and its a
endpoint omitted in the second group. The bridge b_0 b_L has b_0
omitted. Thus D_Q induces only the local matching edges and has
8L-1 vertices. Its endpoint a_1 belongs to D_Q and a_(L+1) does not,
so the optional edge e preserves this attaining set. QED.

## Completing the degrees without losing the gap

Start with Q_L+e. For each j=0,...,L-1 let

    l=L+(j XOR 1),

where XOR 1 exchanges consecutive even and odd indices. Take a fresh
square z_(j,0) z_(j,1) z_(j,2) z_(j,3) z_(j,0), and add

    i_j z_(j,1),    i_l z_(j,3).

Every i occurs in exactly one pair. Select z_(j,0),z_(j,2) in addition
to the core selection. This defines H_L, its 10L-vertex selection S_L,
and its (10L-1)-vertex attaining set D_L obtained from D_Q by adding
the same two vertices of each square. The total number of vertices
is 12L+4L=16L.

**Lemma 2.** H_L is bipartite, has minimum degree two and maximum
degree three, and S_L is inclusion-minimal two-star-forming. Its
selected subgraph consists of 2L copies of P_3 and 4L isolates, and
beta_2(H_L)=10L-1.

**Proof.** Give a_j colour (j mod 2) XOR floor(j/L), and alternate
along each path. Every chain edge has opposite endpoint colours.
Since L is even, the two added a-a edges in each group do also.
The bridge b_0 b_L and e join opposite colours. The i endpoints
of a square have the same colour: exchanging parity with XOR 1
and exchanging groups cancel each other. Give its z_0,z_2 that
common colour and z_1,z_3 the other colour.

The former pendant vertices i gain one neighbour. On each square
z_0,z_2 have degree two and z_1,z_3 degree three. Each root a has
its path edge, first chain edge and closing a-a edge. Each terminal
a has its path edge and two a-a edges. Each penultimate a has its
path edge, outgoing chain edge and terminal chord. The other nonroot,
nonterminal a vertices have their path edge and outgoing chain edge,
with a_1,a_(L+1) gaining e. Since L>=4, the port and penultimate
positions are distinct.
Each b has its two path edges and exactly one chain or bridge edge.
The x,c,y vertices have degree two. Hence all degrees are two or three.

Each outside a is formed by the selected edge x-c; each outside b
by the selected edge y-c. Each outside square vertex has two
selected neighbours z_0,z_2. This proves formation. On deleting x_j,
a_j has no selected neighbour and fails formation. On deleting c_j,
a_j has only its now isolated selected neighbour x_j and again fails.
On deleting y_j, b_j has only its isolated selected neighbour i_j and
fails. Each selected isolate, whether i_j or a square z_0,z_2, fails
at its own vertex when deleted, since it then has no selected neighbour.
These witnesses cover every selected vertex. Formation is upward closed:
every vertex outside a larger selection already has its required star
in any smaller forming selection. Thus failure after every single
deletion implies inclusion minimality. The stated selected components
follow immediately from the edge list.

For an arbitrary dissociation set, its restrictions to the vertex-disjoint
core and L squares have sizes at most 8L-1 and two per square. This
gives beta_2(H_L)<=10L-1. D_L attains the bound: the square attachment
vertices z_1,z_3 are omitted, so no new edge joins two retained vertices.
QED.

## A structural two-connectivity proof

For each group h, the chain and its closing edge form the body cycle

    a_h, b_(h+1), y_(h+1), c_(h+1), x_(h+1), a_(h+1),
    b_(h+2), ..., a_(h+L-1), a_h.

Its length is 5L-4. The two body cycles are disjoint. They are joined by
e and by the path

    a_0-x_0-c_0-y_0-b_0-b_L-y_L-c_L-x_L-a_L.

These connecting paths are internally disjoint and have distinct
endpoints a_1,a_0 on the first cycle and a_(L+1),a_L on the second.
Their union with both cycles is two-connected. Indeed, on deleting an
internal connecting-path vertex, the other connecting path still joins
the two cycles and the remaining path segments attach to them. On
deleting a cycle vertex, that cycle's remainder is a connected path
and at least one connector survives to join it to the other cycle;
the other connector, if severed at its endpoint, has its remaining
segment attached to the other cycle. All surviving vertices are connected.

This backbone covers all core vertices except the i's. For the square
with pair j,l add the two open ears

    b_j-i_j-z_1-z_0-z_3-i_l-b_l,
    z_1-z_2-z_3.

Each ear has distinct old endpoints and new internal vertices. An open
ear preserves two-connectivity: deleting an old vertex leaves a connected
old graph and every surviving ear segment attached to it, while deleting
a new vertex leaves two segments attached to the connected old graph.
The pairs are disjoint, so all these ears can be added successively.
They cover every vertex. Extra unused chord edges preserve the property.
This proves H_L two-connected for all even L>=4. The degree-two vertices
then imply kappa(H_L)=2.

## Cyclic composition and exact additivity

Take k disjoint copies of H_L-e, numbered r modulo k. Add the edge
from a_(L+1) in copy r to a_1 in copy r+1. Call the resulting graph
G_(L,k), and take the unions of the respective S_L and D_L sets.
For k=1 this restores H_L.

The degree and colour constraints survive, since a_1 has colour one
and a_(L+1) has colour zero in every copy. All changed edges have both
endpoints outside S, so every selected neighbourhood and every formation
or deletion witness in Lemma 2 survives. Its selected subgraph is unchanged.
The upper bound partitions the graph into copies of Q_L and individual
squares; none of its edges has been removed. Thus beta_2<=k(10L-1).
The union of D_L attains this bound. Every new edge joins a retained
a_1 to an omitted a_(L+1), so it adds no edge inside that union.

For two-connectivity, the following general fact applies. If H is a
two-connected graph with edge uv, cyclically replacing uv between k
copies of H-uv gives a two-connected graph. First H-uv is connected:
every edge of a two-connected graph lies on a cycle. For k>=2 delete
a vertex z in one copy. If z is u or v, that copy's remainder equals
H-z and is connected through its other port to the remaining copies.
If z is neither port, every component of (H-uv)-z contains u or v;
otherwise it would already be separated in the connected graph H-z.
The other k-1 copies and cyclic links supply an external u-v path,
which joins these components. The other copies remain connected.
For k=1 the claim is the hypothesis on H. Applying this to H_L proves
kappa(G_(L,k))>=2, and its degree-two vertices give equality.

Combining the counts proves, for all the stated parameters,

    |V|=16Lk, |S|=10Lk, beta_2=(10L-1)k,
    delta=kappa=2, Delta=3.

## Verification and the limits of cheaper padding

Run `python3 -B scripts/check_compact_subcubic_selected_stars.py`.
The checker validates the six physical P_6 normalization cases; compares
its exact dissociation recursion against every vertex subset of every
labelled graph on one through five vertices; computes exact core optima
for L=4,6,8 with and without e; and checks all normalized states for
L=4,6. It computes the full 64-vertex graph's beta independently,
validates formula-generated spanning ears for L=4,6,8,12,20, and checks
20 full graphs using all single deletions, all single vertex cuts,
literal three-vertex stars, colours, degrees and attaining sets.
The arbitrary-parameter conclusions follow from the proofs above.

One tempting smaller completion fails in a precisely bounded search.
In Q_4+e, each colour class has four i vertices. Partition each
class into two pairs and add one outside vertex for each pair, adjacent
to its two i vertices. Join the four new vertices by a perfect matching
between the two colours. These are exactly 3*3*2=18 specified recipes,
each with 52 vertices and the original 32-vertex selection. Exact
optimization gives beta_2 in {32,33} for every recipe. They therefore
give no positive selected gap. This finite result rules out those
recipes, not arbitrary 52-vertex graphs. The full list and exact
optimization state counts are in the checker report.
