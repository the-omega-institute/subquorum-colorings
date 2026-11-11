# A gap with only selected three-vertex stars and isolates

The following assertion is false:

> If G is a finite simple bipartite graph and S is an inclusion-minimal
> two-star-forming set whose selected components are stars, edges or
> isolates, then |S|<=beta_2(G).

Here beta_2 is the maximum size of a dissociation set, a vertex set inducing
maximum degree at most one. We give connected counterexamples with only
three-vertex stars and isolates in the selected subgraph. The smallest
example in the family below has 18 vertices, a minimal forming set of
size 12, and dissociation number 11. This is an unrestricted dissociation
gap, rather than a failure of a prescribed exchange.

## Construction and exact dissociation number

Fix positive integers a,b and put c=a+b. Start with c disjoint blocks
with labelled vertices

    x_i, l_i, h_i, p_i, u_i, v_i,             1<=i<=c.

The five edges in each block are exactly

    x_i l_i, x_i h_i, l_i u_i, h_i v_i, p_i v_i.       (1)

For i<=a, put x_i,u_i,v_i in the first bipartition class and l_i,h_i,p_i
in the second. For i>a reverse these classes. Add every edge from

    W_A={u_i,v_i: i<=a}  to  W_B={u_i,v_i: i>a},       (2)

and no other edges. Denote the resulting graph by G_(a,b). Select

    S={x_i,l_i,h_i,p_i: 1<=i<=c}.                     (3)

Thus G[S] consists of c copies of P_3, with centres x_i, and c isolates
p_i. The construction is simple, bipartite and connected: W induces the
complete bipartite graph K_(2a,2b), and every vertex has a path to W.
It has 6c vertices, 5c+4ab edges and maximum degree 2max(a,b)+2.

**Theorem.** S is inclusion-minimal two-star-forming and

    |S|=4c,
    beta_2(G_(a,b))=3c+max(a,b,2).                    (4)

Consequently every (a,b) other than (1,1) is a strict counterexample to
the displayed assertion. In particular, for a=b=r>=2,

    |V|=12r,   |S|=8r,   beta_2=7r,                  (5)

so SF_2-beta_2>=r=|V|/12. Here SF_2 denotes the largest cardinality of
an inclusion-minimal forming set. An exact value of SF_2 is not needed
or asserted for this construction.

### Minimality

Two-star formation means that every x outside S belongs to a not
necessarily induced two-leaf star together with two vertices of S.
In a bipartite graph an outside vertex is formed exactly when it has
two selected neighbours, or has one selected neighbour that itself has
a selected neighbour.

The only outside vertices in (3) are u_i and v_i. Vertex u_i is formed
by the path u_i-l_i-x_i, and v_i by v_i-h_i-x_i (also v_i has the two
selected neighbours h_i,p_i). The added W-W edges change no selected
neighbourhood. Every single deletion fails as follows:

| Deleted selected vertex | Unformed vertex afterwards | Reason |
| --- | --- | --- |
| x_i | u_i | Its sole selected neighbour l_i has become isolated |
| l_i | u_i | It has no selected neighbour |
| h_i | v_i | Its only selected neighbour is the selected isolate p_i |
| p_i | p_i | The newly omitted vertex has no selected neighbour |

The last row explicitly tests the newly omitted vertex. Formation is
upward closed, so failure of every single deletion proves inclusion
minimality. These witnesses work for all a,b, regardless of the number
of added W-W edges. The leaf witnesses u_i and v_i are unique: deleting
one leaf changes the selected neighbourhood of just its corresponding
outside vertex, while its centre remains active.

### Upper bound on beta_2

Let D be any dissociation set, without restrictions on retained vertices.
There are four exhaustive possibilities for D intersect W.

If it is empty, each block contributes at most three vertices: the
selected P_3 contributes at most two, and p_i contributes at most one.
Thus |D|<=3c.

If D meets W_A and avoids W_B, each first-group block contributes at
most four. Indeed its six vertices are partitioned into the two paths

    {x_i,l_i,u_i},   {p_i,v_i,h_i},                    (6)

and a dissociation set contains at most two vertices of each path. Each
second-group block has no witness in D and contributes at most three.
Therefore |D|<=4a+3b. Reversing the two groups gives |D|<=3a+4b when D
meets W_B and avoids W_A.

Finally suppose D meets both W_A and W_B. Since all cross edges in (2)
are present and degrees in G[D] are at most one, D contains exactly one
vertex from each witness class. These two witnesses are adjacent in D,
so neither can have any selected neighbour in D. If the witness in a
block is u_i, its owner l_i is absent; at most x_i,h_i,p_i remain, giving
at most four vertices in that block including u_i. If it is v_i, both
h_i,p_i are absent; only x_i,l_i remain, giving at most three including
v_i. The two witnesses are in different blocks, and all other blocks
contribute at most three. Thus |D|<=3c+2.

Together these cases prove

    |D|<=max(3c,4a+3b,3a+4b,3c+2)
        =3c+max(a,b,2).                               (7)

### Attaining sets

Each of the three nontrivial case bounds is attained. For 4a+3b, take

    {x_i,p_i,u_i,v_i} in every first-group block,
    {l_i,h_i,p_i}     in every second-group block.     (8)

The only induced edges are p_i v_i in first-group blocks. There are no
second-group witnesses to produce cross edges. The reversed construction
attains 3a+4b.

To attain 3c+2, choose one first-group block and one second-group block.
In each chosen block take {x_i,h_i,p_i,u_i}, and in each other block take
{l_i,h_i,p_i}. The induced edges are x_i h_i in the two chosen blocks
and the single edge between their u_i witnesses. All other selected
vertices are isolated. This gives a dissociation set of size 3c+2.
Equation (4) follows from these constructions and (7).

For (a,b)=(1,2), equations (1)-(3) give an explicit 18-vertex graph with
5(1+2)+4(1)(2)=23 edges; it has maximum degree
six and |S|=12>11=beta_2. For (a,b)=(2,2), the values are 24 vertices,
36 edges, |S|=16 and beta_2=14. These follow directly from (1)-(4).

## Relation to the exact leaf-retaining exchange

For this family the forced leaf-witness graph is

    Q=G[W union {p_i:1<=i<=c}].

It has maximum matching size

    nu(Q)=c+min(a,b).                                 (9)

Match each v_i to its p_i and match all clean witnesses u_i in the
smaller group to distinct clean witnesses in the other group. These
edges give c+min(a,b) disjoint matching edges. Conversely the two
bipartition sizes of Q are 2a+b and 2b+a, whose minimum is exactly
c+min(a,b), proving optimality.

The exact leaf-retaining theorem therefore gives

    leaf-retaining optimum=4c-min(a,b)=3c+max(a,b).    (10)

Whenever max(a,b)>=2, this is already the true beta_2 in (4). Allowing
centres and dropping leaves cannot repair the genuine deficit. In the
exceptional two-block case (1,1), the leaf-retaining optimum is 7 while
the unrestricted optimum is 8. This explains why the earlier sparse
two-block restriction obstruction did not refute the unrestricted
inequality: the denser coupling across at least three blocks changes
the true optimum.

## A sharp n/12 bound with a clean leaf at each centre

There is a matching upper bound for a wider class than this construction.
Let S be a minimal forming selection in a finite simple bipartite graph
of order n, with selected components stars, edges and isolates. Suppose
that each selected star of order at least three has a leaf l and an
outside vertex u with

    N_S(u)={l}.                                      (11)

This is an additional hypothesis: a centre can instead have a direct
deletion witness, so (11) is not inferred from minimality alone.

**Theorem.** Under (11),

    |S|-beta_2(G)<=floor(n/12).                       (12)

The coefficient is sharp, attained by the balanced family (5) for every
r>=2.

**Proof.** Let c be the number of selected star centres and e their
number of leaves, so e>=2c. Choose one witness per leaf, using the
private witness in (11) for one leaf of every centre. These c witnesses
are distinct and meet no selected isolate. Let t be the number of
distinct selected isolates touched by all chosen witnesses. Each other
witness touches at most one isolate, so

    t<=e-c.                                         (13)

The exact matching-exchange theorem, or its two colour-cover constructions,
gives

    beta_2>=|S|-c+ceil((e-t)/2).

If d=|S|-beta_2>0, then

    2d<=2c-e+t<=c.                                  (14)

There are at least e distinct outside witnesses and at least t selected
isolates, all disjoint from the c centres and e leaves. Selected edge
vertices, additional isolates and further outside vertices only add to n.
Consequently

    n>=c+2e+t
      >=c+2e+(2d+e-2c)
      =3e-c+2d
      >=5c+2d
      >=12d.                                        (15)

This proves (12); for d<=0 it is immediate. The graph G_(r,r) satisfies
(11) at u_i for every centre and has n=12r, d=r by (5), proving sharpness.
The witnesses and touched isolates are counted once in (13)-(15), even
when several witnesses have the same helper. This is a bound for the
specified selected set, not an assumption that every maximizing minimal
set in G has property (11).

## Attainment in connected graphs of maximum degree six

The coefficient in (12) remains sharp with a fixed maximum degree.
For every r>=1 take r copies of G_(2,2), reversing their global
bipartitions on alternate copies. In each copy designate its two clean
witnesses u_3,u_4 in the second group as left and right ports, respectively.
Both ports originally have degree five. Add an edge from the right port
of copy j to the left port of copy j+1 for 1<=j<r.

The resulting graph H_r is connected and bipartite, with

    |V(H_r)|=24r,   |E(H_r)|=37r-1,   Delta(H_r)=6.   (16)

No port receives more than one new edge. The union S_r of the selections
(3) is still minimal forming: all new edges have both ends outside S_r,
so every formation triple and every deletion failure in the table is
unchanged. Each centre retains the clean leaf property (11).

Any dissociation set restricts to a dissociation set of size at most 14
in each G_(2,2), giving beta_2(H_r)<=14r. In each copy use the set (8).
It contains no second-group witness, hence neither of the two ports.
The union of these sets is dissociation after all joins and has size
14r. Therefore

    |S_r|=16r,   beta_2(H_r)=14r,
    |S_r|-beta_2(H_r)=2r=|V(H_r)|/12.                (17)

This proves sharpness of (12) in connected bipartite graphs of maximum
degree six, with selected components exclusively P_3's and isolates.
The new connecting edges are bridges. No stronger connectivity property
or exact SF_2 value is asserted.

The displayed examples have pendant vertices and are not full rectangular
grids. General rectangular-grid equality and a unit-weight 5/6 improvement
remain separate questions. The new conclusion is the failure of the
unrestricted selected-star minimal-set inequality for bipartite graphs.

## Reproduction and status

Run `python3 scripts/check_selected_star_gap.py`. The checker uses literal
two-star copies for formation and deletion failures, checks the explicit
attaining sets and path partitions, and independently computes small
unrestricted dissociation optima. Larger controls check the certificates
and the local table underlying every case of the upper bound. All-parameter
claims use the proofs above. Independent review is pending. No Lean or
historical-priority verification is claimed.
