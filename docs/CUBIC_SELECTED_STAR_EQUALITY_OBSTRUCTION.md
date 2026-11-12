# Cubic selected-star gaps cannot attain the numerical n/22 equality

Let G be a nonempty finite simple cubic bipartite graph. Let S be a
specified inclusion-minimal two-star-forming set inducing stars, single
edges and isolates, and put d=|S|-beta_2(G), where beta_2 is unrestricted.
Then

    d <= floor((|V(G)|-2)/22).

In particular, positive equality |V(G)|=22d in the previous numerical
certificate never occurs, at any scale. This is an integer refinement;
it does not prove a smaller asymptotic coefficient than 1/22.

We use the bound and witness ledgers proved in
[Direct witnesses and the cubic bound](DIRECT_WITNESS_EXCHANGE_AND_CUBIC_BOUND.md).
The new step is a structural exclusion of all its positive equality
points. The earlier 22-vertex obstruction is the smallest special case.

## The equality structure

Suppose n=22d with d>0. Retain one witness assignment of the preceding
proof. In its notation,

    n=2J+2R+4T'+5B+2F+2(s+q+b3+mu+z0),
    J,F,s,q,b3,mu,z0>=0, R,T',B>=2d.

Equality therefore forces all the displayed nonnegative terms to
vanish and R=T'=B=2d. Since T'=t-s-q, J=c+s+2q-t-b2-2b3,
and R=c-q+b2+b3-mu, this also gives

    c=t=a=2d, b2=0, m=4d, u=6d.

The last two equalities follow by solving B=c+t+m-u=2d and
F=3u-2c-3t-2m=0. All selected stars are P_3's because s=0.
Every centre has a private leaf witness because q=0. There are 2d
selected isolates, each touching exactly one chosen witness. Of the
4d leaf witnesses, exactly 2d are private, so each star has exactly
one private witness and one helped witness. Label its block as

    a_j - x_j - c_j - y_j - b_j - i_j, j=1,...,2d,

where x_j,c_j,y_j,i_j are selected. The selected edge components
have a total of 4d vertices; call their union P. The remaining 6d
vertices form U and are not selected.

There are no other edges from a chosen witness to S: a private a_j
has selected neighbourhood {x_j}, and b_j has selected
neighbourhood {y_j,i_j}. The exact residual identity for cubic
graphs is

    F=(c+s+2q-sum_i h(i))+2|E(U)|+|E(U,W)|.

Here sum h(i)=2d=c and F=0. Thus E(U)=E(U,W)=empty. Write
A={a_j} and B_w={b_j}, both of order 2d. Within the witness graph
G[A union B_w], every a_j has degree two and every b_j has degree
one. Edges from S to U will play no role because all sets below
omit U. The chosen witnesses meet no selected edge endpoint.

## Either a direct improvement, or four-cycles and a matching

Retain all c_j,y_j,i_j and every vertex of P. This is a dissociation
set of size 6d+4d=10d. Any dissociation set in G[A] can be added:
the only selected neighbour of a_j is the omitted x_j. Therefore

    beta_2(G) >= 10d+beta_2(G[A]).                       (1)

A bipartite graph R of maximum degree two satisfies
beta_2(R)>=|V(R)|/2, with equality only when each component is a C_4.
Indeed its components are paths and even cycles. For a path on l
vertices the exact number is ceil(2l/3), and for a cycle of even
length l>=4 it is floor(2l/3). Partitioning a path into triples
bounds its size by 2 floor(l/3)+(l mod 3); the first l entries of
110110... attain this. On a cycle, summing over all cyclic triples
gives 3|D|<=2l. For lengths 3q, 3q+1, 3q+2, respectively, attaining
cyclic words are (110)^q, (110)^(q-1)1100, (110)^q10.
Every path contributes
strictly more than half its order, and every even cycle except C_4
does so as well. The component values add.

In the putative equality case beta_2(G)=|S|-d=11d. Equation (1)
therefore forces beta_2(G[A])=d. Hence G[A] is a disjoint union
of C_4's. Its vertices already use their two witness-neighbour
slots inside A, so there is no A--B_w edge. Every b_j consequently
uses its single witness-neighbour slot inside B_w, and G[B_w] is
a perfect matching.

## Simultaneous local exchanges

Contract each private C_4 to a vertex. For every edge b_j b_l of
the helped-witness matching put an edge between the C_4's containing
a_j and a_l. This gives a four-regular multigraph: each private
cycle has four distinct blocks, each providing exactly one matching
endpoint. Loops are allowed and count twice towards the degree.

Every finite even-degree multigraph admits a balanced orientation:
follow Euler tours in its components, with loops contributing one
incoming and one outgoing incidence. Thus here every vertex has
indegree two and outdegree two. For each oriented matching edge,
use state A_j={a_j,c_j,y_j,i_j} at its head endpoint and state
B_j={x_j,c_j,b_j,i_j} at its tail endpoint. A loop still has two
distinct original matching endpoints, so one receives each state.

Exactly two of the four blocks at every private C_4 now have state
A_j. The two retained private vertices induce at most an edge.
Exactly one endpoint of each helped-witness matching edge has
state B_j, so that edge never has both ends retained. Locally both
states induce a matching, and these exhaust the witness-interface
edges. Consequently all 2d blocks simultaneously contribute four
vertices to a dissociation set. Add all 4d vertices of P to obtain

    beta_2(G)>=8d+4d=12d,

contradicting beta_2(G)=11d. This excludes n=22d for every d>0.
Since a cubic graph has even order, n>=22d+2. For d<=0 the stated
integer bound is immediate, as a nonempty simple cubic bipartite
graph has at least six vertices. This proves the theorem.

## Scope and checks

Run `python3 -B scripts/check_cubic_equality_obstruction.py`.
The checker independently verifies the maximum-degree-two equality
classification in its stated finite range and constructs the simultaneous
physical exchanges for exhaustive small helped-witness matchings and
larger seeded examples, including quotient loops. These are controls
of the structural proof, not existence assertions about completed
cubic equality graphs. There is no general asymptotic sharpness claim,
unrestricted-SF upper bound, or new Lean verification here.
