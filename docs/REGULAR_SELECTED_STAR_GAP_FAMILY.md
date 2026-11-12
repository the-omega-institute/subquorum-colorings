# Cyclic outside-edge composition and regular selected-star gaps

Let beta_2(G) be the maximum size of a vertex set inducing maximum degree
at most one. Let SF_2(G) be the maximum cardinality of an inclusion-minimal
two-star-forming set. Stars are not required to be induced. All graphs below
are finite and simple; r is a positive integer.

**Result.** There is an explicit two-connected four-regular bipartite graph
H_r, for every r>=1, with

    |V(H_r)|=68r,  beta_2(H_r)=35r,

and a minimal two-star-forming set S_r of size36r inducing exactly4r
copies of P3,4r isolates and10r single edges. Consequently

    |S_r|-beta_2(H_r)=r,   SF_2(H_r)-beta_2(H_r)>=r.       (1)

No exact value of SF_2(H_r) is claimed. The selected-star four-regular
upper coefficient1/34 from FULL_DEGREE_CAPACITY_FOR_SELECTED_STARS.md
therefore has an explicit lower family of coefficient1/68. Determining
the optimal coefficient between these values remains open. The graph is
not a full rectangle, and this does not decide rectangular triple equality.

The all-r conclusion uses the general composition theorem proved next.
The two caps for its fixed68-vertex base are exact integer elimination
certificates, with their general recurrence and reproduction scope below.
They are not inferred from MILP output or from testing finitely many r.
No literature-priority or Lean verification claim is made.

## A general composition theorem

Let H have a minimal two-star-forming set S, and let e=ab be an edge with
both endpoints outside S. Suppose

    beta_2(H-e)=beta_2(H)=b.                              (2)

Take r vertex-disjoint labelled copies H_i. Remove a_i b_i from each,
and insert a_i b_(i+1), with indices modulo r. Denote the resulting graph
by C_r(H,e), and put S_r=union_i S_i. Then

    beta_2(C_r(H,e))=rb,
    S_r is minimal two-star-forming, |S_r|=r|S|.           (3)

For r=1 the original edge is restored. For r>=2 all new edges join
different copies, have distinct endpoints at each port, and are absent
from the original disjoint copies. Thus the resulting graph is simple.

For the upper bound, the restriction of any dissociation set to copy i
is a dissociation set in H_i-e. Equation(2) bounds each restriction by b,
and the vertex classes of the copies are disjoint. Summing gives rb.

For the lower bound, fix any maximum dissociation set D in H and use
the same labelled choice in every copy. If at least one of a,b is omitted
from D, none of the new edges has both endpoints chosen. If both are
chosen, the old edge ab was a matching component of H[D]; hence neither
endpoint had another neighbour in D. The cyclic replacement edges form
a matching on these ports, so their degrees remain one. All other induced
edges are unchanged. Therefore union_i D_i is dissociation of size rb.
This is one simultaneous construction; no vertex capacity is reused.

For any selected subset Q of S_r, the local two-star-forming rule at an
outside vertex uses only its neighbours in Q and adjacency inside Q.
The switched edges have both endpoints outside S_r, so these data are
identical to those in the original disjoint copies, even after a selected
vertex is deleted. Each S_i forms its own copy, and each single deletion
still has its old failing vertex in that copy. Formation is upward closed,
so these single-deletion failures prove inclusion-minimality of S_r.
Its selected components are the disjoint copies of those of H[S].

If H is k-regular bipartite and a,b have opposite colours, the construction
preserves every degree and the common bipartition of the copies. If H-e
is connected, C_r(H,e) is connected: the nonempty copies H_i-e are joined
around a cycle (and the r=1 graph is H).

Finally every connected k-regular bipartite graph, k>=2, is two-connected.
Indeed, suppose deleting v in the A class leaves more than one component.
For a component K, let t_K be its edges to v in the original graph.
Connectivity gives t_K>=1. Summing original degrees over its two colours
and cancelling internal edges gives

    k(|K intersect B|-|K intersect A|)=t_K.

Thus t_K is a positive multiple of k. Two components would need at least
2k edges at v, contradicting deg(v)=k. This proves the assertion without
an enumeration of vertex deletions.

## The labelled base graph

The labels are0,...,67. For j=0,1,2,3 create the six-vertex block

    c_j=6j, l_j=6j+1, m_j=6j+2,
    i_j=6j+3, p_j=6j+4, h_j=6j+5,

with edges c_j l_j,c_j m_j,l_j p_j,m_j h_j,i_j h_j.
Select c_j,l_j,m_j,i_j. Centres c_0,c_1 have colour0 and centres c_2,c_3
have colour1; their leaves and isolates have the opposite colour, and
the two witnesses p_j,h_j have the centre's colour.

On the witness parts

    W_0=(4,10,5,11), W_1=(16,22,17,23),

join W_0[t] to W_1[t+1] and W_1[t+2], indices modulo4, and add
W_0[t] W_1[t] for t=0,1. Private witnesses have degree3 within W;
helped witnesses have degree2.

Select the20 new vertices24,...,43, giving vertex v colour v modulo2.
Join24--25,26--27,...,42--43. Add the unselected classes

    U_0=(44,...,55), U_1=(56,...,67).

For each colour s separately, list the selected vertices of that colour
in increasing order, and start a counter at zero. A selected vertex v
currently of degree a receives4-a neighbours, namely the next4-a entries
of U_(1-s), cyclically modulo12. Advance the counter after each edge.
There are exactly48 assignments in each colour, so every U vertex is
used four times. Each selected vertex needs at most three entries; the
three consecutive residues are distinct. This defines every edge of H.
The full coordinate list is in
`develop/fixtures/regular-selected-star-gap.json`.

There are18 selected vertices in each colour. In each colour, six of
them have initial degree2 and twelve have initial degree1. Their demands
are6*2+12*3=48. Thus every selected vertex has degree4. The witness
vertices have one or two selected neighbours and respectively three or
two witness neighbours, also giving degree4. All U vertices have degree4.
Every listed edge is between opposite colours, and the construction has
no repeated edges. Hence H is simple, four-regular and bipartite.

The selected graph consists of four P3 stars, four isolates and ten edges,
so |S|=36. Each U vertex has four selected neighbours. Each private witness
has its active leaf, and each helped witness has both a leaf and an isolate;
therefore S forms every outside vertex.

Deleting l_j uncovers p_j. Deleting m_j uncovers h_j, whose only remaining
selected neighbour is the inactive isolate i_j. Deleting c_j uncovers p_j
because l_j becomes inactive. Deleting an isolate uncovers that newly
omitted vertex, which has no selected neighbour. Deleting a selected edge
endpoint leaves the newly omitted vertex adjacent only to its now-inactive
mate. These failures prove minimality of S in all cases.

Choose the port edge e=4--16. Both endpoints are private witnesses outside S.
The finite certificate verifies that H-e is connected, and gives

    beta_2(H)=beta_2(H-e)=35.                             (4)

A labelled35-set attaining the first value is included in the fixture and
checked directly by its induced degrees. Equation(4), the construction and
the general composition theorem prove (1) for every r.

The cap hypothesis is substantive. Another outside edge,4--17, has
beta_2(H-(4--17))=36. Thus merely choosing endpoints outside S does not
establish (2). This observation concerns the needed block cap; it is not
claimed to refute additivity for that other cyclic lift.

## Exact integer certificate for the fixed base caps

For any finite graph G of order N, assign a bit x_v to each vertex. Let T
be its distinct triples consisting of a vertex and two different neighbours.
A bit assignment is dissociation exactly when it does not select all three
vertices of any triple. Define M=N+1 and the integer score

    F(x)=sum_v x_v-M*sum_(t in T) product_(v in t)x_v.      (5)

Every infeasible assignment has F<=N-M=-1. The all-zero assignment has
score0. Every feasible assignment has score equal to its cardinality.
Consequently max_x F(x)=beta_2(G), with no floating-point relaxation.

Start with unary factor x_v for each vertex and one triple factor taking
value -M at111 and zero otherwise. To eliminate vertex v, gather exactly
the current factors involving it. Let B_v be the union of their variables,
and replace that bucket by the table on B_v minus v given by

    message(y)=max_(x_v in {0,1}) sum_(f in bucket) f(y,x_v). (6)

Other factors do not depend on x_v, so moving this maximum inside their
sum is an exact identity. Induction over any elimination order proves
that the sum of the final constant factors is max_x F(x). This proves
the certificate algorithm for every finite graph, without assuming a
particular graph class or importing a solver's optimum.

The checker constructs the distinct physical triples from the supplied
coordinates, chooses a deterministic minimum-fill order, and evaluates
(6) with integer arrays. It also checks a bound ensuring every intermediate
sum fits signed32-bit arithmetic. Each original factor belongs to exactly
one bucket at a time and is used once. A bucket message replaces its
entire bucket; no previous contribution is added twice.

The public report records every eliminated vertex, bag and message hash,
as well as the final exact integer. For H it gives35, and for H-e it also
gives35. The original graph's35-set directly attains both caps. The third
calculation gives36 after deleting4--17. These are computer-assisted
certificates for fixed labelled graphs; the general all-r implication
is the written composition proof above. No finite list of lift optima
is used as a substitute for that proof.

## Reproduction and scope

Run `python3 -B scripts/check_regular_selected_star_gap.py` with NumPy
installed and assertions enabled. SciPy and MILP are not required. The
checker compares exact elimination with independent literal subset optima
on all labelled five-vertex simple graphs and all fixed-part(3,3) bipartite
graphs. It reconstructs H independently of the coordinate fixture, checks
literal formation and every deletion, all degrees and colours, connectedness
and the three fixed exact caps. Its finite cyclic-lift controls test actual
lower sets and minimality; their all-size optima are supplied by (3)-(4).

Independent review returned **ACCEPT** without a mathematical correction.
The reviewer reconstructed all four exact manifest files, verified their
hashes, ran the original checker unchanged with assertions to terminal
exit0, and reproduced the entire 36,212-byte report byte-for-byte. The
complete response and actual scope are in
`output/regular-selected-star-gap-review.json`. No Lean, exact SF_2,
arbitrary-width grid or historical-priority claim is made.
