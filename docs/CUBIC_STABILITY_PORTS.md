# Port deficiency and connected cubic stability examples

19 October 2026. This note proves an exact connected family at the proposed
cubic stability boundary. It also excludes an order-only strengthening
obtained by merely assuming a positive SF-dissociation gap. No general
stability theorem or historical priority is claimed.

Use the non-induced two-star definition and inclusion-minimality from
[the regular-bound note](REGULAR_STAR_FORMING_BOUND.md). Write beta for
the dissociation number and SF for the upper two-star-forming number.

## A general deficiency budget

**Lemma 1.** Let F be a finite simple graph on N vertices with maximum
degree at most d, where d>=1. Put epsilon(v)=d-deg_F(v),
R=sum_v epsilon(v), and R_D=sum_(v in D) epsilon(v). Every dissociation
set D satisfies

    (2d-1)|D| <= dN-R+2R_D.                                  (1)

**Proof.** Each vertex of D has at most one neighbor in D, so the number
of cut edges is at least (d-1)|D|-R_D. Counting from the complement gives
at most d(N-|D|)-(R-R_D). Combine the two estimates. Each deficiency
belongs to its actual vertex and occurs in exactly one of R_D and
R-R_D; no port capacity is assigned to two different pieces. QED.

In particular, if F is cubic except for two degree-two ports, and D
selects p of those ports, then

    5|D| <= 3N-2+2p.                                        (2)

For N=20k this implies |D|<=12k, and an attaining set must select at
least one port. If both ports are omitted then |D|<=12k-1. This is an
all-orders counting proof; no optimization or enumeration is used.

## A cubic bipartite equality core

For k>=1 put m=6k. Define C_k using disjoint classes

    H={h_i:0<=i<m}, U={u_i:0<=i<m}, X={x_i:0<=i<m},
    Y={y_j:0<=j<2k}.

Indices on H and X are read modulo m. Put a cycle on H, a cycle on X,
and add h_i--u_i--x_i for every i. For 0<=b<k add edges

    y_(2b)--u_(6b), u_(6b+2), u_(6b+4),
    y_(2b+1)--u_(6b+1), u_(6b+3), u_(6b+5).

Thus C_k is cubic on 20k vertices. A bipartition has h_i,x_i in L
when i is even and in R when i is odd; u_i has the opposite color,
and y_j is in L exactly when j is even.

The set S_C=H union U, of size 12k, is minimal star-forming. Every y
has three selected neighbors, and every x_i is covered by x_i--u_i--h_i.
Deleting u_i uncovers x_i. Deleting h_i also uncovers x_i, since u_i
then has no selected neighbor. These are witnesses for every selected
vertex. Formation is upward closed, so single-deletion failure proves
inclusion-minimality. The regular bound gives SF(C_k)=12k.

The set U union H_odd union X_even induces a matching and has size 12k.
The dissociation cut bound, or Lemma 1 with R=0, gives beta(C_k)=12k.

C_k is two-connected. After deleting an H vertex, the X cycle remains
intact and every surviving H vertex attaches to it through its own U;
the same argument with H,X exchanged handles deletion from X. After
deleting a U vertex, both cycles remain and another U connects them.
After deleting a Y vertex, the two cycles and all U remain connected.
Every surviving Y retains at least two U neighbors in all these cases.

Let C'_k=C_k-x_0x_1. Its two ports x_0,x_1 have degree two. Lemma 1
shows that every dissociation set has size at most 12k and that selecting
12k vertices requires at least one port.

## Joining an obstruction to an equality core

Let B be the Heawood graph with the edge 0--8 deleted, in the labeling
of [the Fano-plane proof](CUBIC_STAR_FORMING_GAPS.md). Its ports are the
point 0 and line 8. That note proves the saturated-port lemma:

    beta(B)=8; every dissociation eight-set selects both ports,
    and each port already has one selected neighbor in B.

Take disjoint B and C'_k and add precisely the two edges

    0--x_1, 8--x_0.

Call the result G_k. It is cubic and bipartite, with the Heawood points
in L and lines in R, and the coloring of C_k specified above.

**Theorem 2.** For every k>=1, G_k is two-connected, cubic and bipartite,
and has exact parameters

    |V(G_k)|=14+20k,
    SF(G_k)=8+12k,
    beta(G_k)=7+12k,
    Gamma(G_k)=alpha(G_k)=7+10k.                             (3)

**Proof of the SF value.** In the Heawood block use
S_H={1,2,3,5,7,9,10,11}. The Fano-plane proof supplies all eight
single-deletion witnesses. The selection S=S_H union H union U has
size 8+12k and remains minimal: all removed and added edges have both
endpoints outside S. Indeed, a star covering a vertex outside any
subset of S uses at most one vertex outside that subset. An edge whose
two endpoints lie outside S therefore cannot occur in that star. This
also proves minimality preservation for every proper subset, rather
than just preserving the displayed deletion witnesses. The cubic bound
SF<=floor(3|V|/5)=8+12k proves equality.

**Proof of the beta value.** Let D be any dissociation set in G_k.
Its restrictions to the two vertex-disjoint blocks remain dissociation
sets. The bounds above give |D intersect B|<=8 and
|D intersect C'_k|<=12k. If the first contribution is at most seven,
their sum is at most 7+12k. If it is eight, both Heawood ports are
selected and each already has an internal selected neighbor. Thus both
cross edges force their C'_k endpoints x_0,x_1 to be omitted. The port
budget then gives |D intersect C'_k|<=12k-1, with the same total bound.
The loss is charged to this single complement-port condition, once.

For attainment, select all seven Heawood points, together with
U union H_odd union X_even in C'_k. The latter set induces a matching.
On 0--x_1 the second endpoint is omitted; on 8--x_0 the first is
omitted. Thus no cross edge has two selected endpoints, and the union
is a dissociation (7+12k)-set. This proves the exact value.

**Proof of connectivity.** The Heawood graph is two-connected: its
Hamilton cycle is
0,7,4,11,1,8,5,12,2,9,6,13,3,10,0.
We proved the same property for C_k. In general, take two disjoint
two-connected graphs, remove an edge ab from the first and cd from the
second, and add ad,bc. Both edge-deleted blocks are connected. After
deleting a non-port vertex from one block, that block before edge removal
was connected. Removing its edge either leaves it connected or splits it
into two components containing the two ports separately. The other
edge-deleted block and both interfaces reconnect those components. After
deleting a port, its own block minus that vertex is connected, and the
one remaining interface joins it to the other connected block. The same
arguments apply in either block. Hence the joined graph is two-connected.

Finally, the classical upper-domination equality Gamma=alpha for
bipartite graphs and a perfect matching in every positive regular
bipartite graph give Gamma=alpha=|V|/2. The regular-bound note includes
the private-neighbor proof of the first fact. This completes (3). QED.

## Consequences for the stability programme

The still-open proposed inequality for all cubic bipartite graphs is

    2(SF-beta)<=3n-5SF, equivalently 7SF<=3n+2beta.            (4)

For G_k both sides of its first form are exactly two. Thus (3) gives
arbitrarily large two-connected examples attaining this candidate.
This does not prove (4) for other graphs.

It does refute the stronger rule

    SF>beta implies SF<=4n/7,

since SF(G_k)-4|V(G_k)|/7=4k/7>0. More generally, SF(G_k)/|V(G_k)|
tends to 3/5 while the gap stays one. Therefore no uniform coefficient
c<3/5 can bound SF<=cn throughout the positive-gap two-connected cubic
bipartite class. The regular endpoint excludes positive gap at exact
equality, but gives no fixed positive separation in this ratio. The
failed rule and the unrefuted target (4) are distinct statements.

## Reproduction and formalization scope

Run `python3 scripts/check_cubic_stability_ports.py --output
output/cubic-stability-ports-controls.json`. It checks literal non-induced
stars, every single-deletion failure, the explicit dissociation witness,
bipartition, degrees and connectivity after every vertex deletion for
k=1,...,8. It independently enumerates all Heawood-block subsets to
check the saturated-port property. Optional `--milp` also checks beta
on k=1,2,3 using SciPy's integer solver and independently checks its
returned vertex sets. Those solver optima are finite controls only;
the all-k parameter proofs are the arguments above.

The recorded run passes all eight constructions, including 496 selected
single-deletion witnesses and 832 vertex-deletion connectivity tests.
It checks all16,384subsets of the broken Heawood graph. The independent
integer optimizations return beta19,31,43 on orders34,54,74, respectively,
with optimal status and zero reported solver gap. The smallest graph's
complete edge list and all displayed vertex witnesses are in the receipt.

The earlier regular order bound and general outside-selection rewiring
lemmas have the formal verification scope documented in their respective
notes. Lemma 1, the new construction, its connectivity proof and exact
parameter combination here have written proofs and the listed controls;
they are not newly claimed as fully Lean-formalized or Oracle-reviewed.
