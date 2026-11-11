# Exact dissociation numbers from clean-witness port compositions

A fixed twelve-vertex block gives an exact composition formula for
arbitrary interfaces. The minimal forming selection in every composition
induces only three-vertex stars and isolates, but its size can exceed the
unrestricted dissociation number. Connected examples already occur at
maximum degree four.

## The block and its two ports

Use two six-vertex blocks, labelled

    x_i,l_i,h_i,p_i,u_i,v_i,             i=0,1.

Inside each six-vertex block put exactly the five edges

    x_i l_i, x_i h_i, l_i u_i, h_i v_i, p_i v_i.

Add all four edges between {u_0,v_0} and {u_1,v_1}. Call the resulting
twelve-vertex graph B. It is G_(1,1) of
[SELECTED_STAR_COMPONENT_GAPS.md](SELECTED_STAR_COMPONENT_GAPS.md).
Its bipartition has x_0,u_0,v_0,l_1,h_1,p_1 on the first side and the
other six vertices on the second. Designate u_0,u_1 as the two ports.
Each port has degree three; each helper witness v_i has degree four.

The set

    S_B={x_0,l_0,h_0,p_0,x_1,l_1,h_1,p_1}

is minimal two-star-forming. In each six-vertex block, deletion of
x_i,l_i,h_i,p_i fails at u_i,u_i,v_i,p_i, respectively. For the last
deletion, p_i is the newly omitted unformed vertex. All these failures
depend only on selected neighbourhoods and remain valid when new edges
are added between outside witnesses.

**Block lemma.** Every dissociation set in B has size at most eight.
If it has size eight, it contains both ports, which are adjacent and
already have their full permitted degree in the induced subgraph.
There is also a seven-vertex dissociation set omitting both ports.

**Proof.** If a dissociation set meets witnesses on only one side of
the complete bipartite witness graph, one six-vertex block contributes
at most four and the other at most three. The bound four follows from
the two disjoint paths {x_i,l_i,u_i} and {p_i,v_i,h_i}; the bound three
follows from a P_3 and an isolate after both witnesses are omitted.
If no witness is selected, the bound is six.

If both witness sides are met, exactly one witness is selected on each
side, since all four cross edges are present. They are paired with one
another. A selected u_i forbids l_i and allows at most x_i,h_i,p_i,
giving at most four vertices in its six-vertex block. A selected v_i
forbids h_i,p_i, leaving at most x_i,l_i and itself, giving at most
three. Thus a set of size eight must use u_0 and u_1. The set

    D_8={x_0,h_0,p_0,u_0,x_1,h_1,p_1,u_1}             (1)

attains eight, with induced edges x_0 h_0, x_1 h_1, u_0 u_1.
Finally

    D_7={x_0,l_0,p_0,v_0,l_1,h_1,p_1}                (2)

has seven vertices and induces only x_0 l_0 and p_0 v_0. Both ports
are absent. This proves the lemma.

## Arbitrary interface graphs

Let R be any finite simple graph of order r, including the empty graph.
Orient each edge arbitrarily. For each vertex j of R take a copy B_j.
For every oriented edge j->k add the single edge

    u_(j,0) u_(k,1).                                (3)

There are no further edges. Call the resulting graph F_R. The orientation
is part of the construction but does not change the formula below. All
copies use the same bipartition, so (3) always joins opposite sides;
even a nonbipartite R gives a bipartite F_R.

**Theorem.** With S_R the union of all S_B selections,

    |V(F_R)|=12r,    |E(F_R)|=14r+|E(R)|,
    |S_R|=8r,       beta_2(F_R)=7r+alpha(R).          (4)

Here alpha(R) is the maximum size of an independent vertex set in R.
The set S_R is inclusion-minimal two-star-forming and induces exactly
2r copies of P_3 and 2r isolates. For nonempty R,

    Delta(F_R)=max(4,3+max_j d^+(j),3+max_j d^-(j)).  (5)

The graph F_R is connected exactly when R is connected, for r>=1.

**Proof.** Edges (3) have both ends outside S_R. The formation triples
and all four deletion failures in each six-vertex block are unchanged.
This proves minimality, including the newly omitted p vertices. Counts,
bipartiteness, degree formula and connectivity follow directly from the
construction.

Let D be an arbitrary dissociation set in F_R, and let J be the set of
copies with |D intersect V(B_j)|=8. Each copy contributes at most eight
by the block lemma. In a copy indexed by J, both ports lie in D and are
already adjacent inside that copy. If j,k in J were adjacent in R, edge
(3) would give a second induced neighbour to its two endpoints. Hence
J is independent in R, and

    |D|<=8|J|+7(r-|J|)=7r+|J|<=7r+alpha(R).          (6)

Conversely, choose a maximum independent set J in R. Use D_8 from (1)
in its copies, and D_7 from (2) in every other copy. Both ports of every
D_7 copy are absent. Thus an added edge could have both endpoints in
the resulting set only if its two copies belonged to J, which never
happens. The union is dissociation and has size 7r+alpha(R), proving
(4). Each copy, port and joining edge is counted once.

The exact SF_2 value is not claimed. The actual minimal forming set
does give the parameter lower bound

    SF_2(F_R)-beta_2(F_R)>=r-alpha(R).                (7)

Every selected centre has a private leaf witness, so the sharp clean-leaf
upper bound n/12 applies to |S_R|-beta_2=r-alpha(R). It does not require
that every maximum-cardinality minimal forming set in F_R have that
property.

## Connected degree-four families

Orient a path P_r in its natural direction. Its maximum indegree and
outdegree are at most one, and alpha(P_r)=ceil(r/2). Consequently for
every r>=1,

    n=12r,   |E|=15r-1,   Delta=4,
    |S_R|=8r,   beta_2=7r+ceil(r/2),
    |S_R|-beta_2=floor(r/2).                         (8)

These are connected bipartite graphs with a linearly growing genuine gap
and only P_3 stars and isolates in the minimal selected subgraph. At r=2
the graph has 24 vertices, selected size 16 and beta_2=15. Each joining
edge of a path composition is a bridge; the graphs also have pendant
vertices.

For a cycle C_r, r>=3, use its cyclic orientation. Then

    n=12r,   |E|=15r,   Delta=4,
    |S_R|=8r,   beta_2=7r+floor(r/2),
    |S_R|-beta_2=ceil(r/2).                          (9)

The independence numbers used here follow by pairing consecutive path
vertices, or the disjoint-edge covering of a cycle after choosing a
vertex; alternating positions attain the bounds. In particular, the
three-block cycle has 36 vertices, selected size 24 and beta_2=22.
These formulas concern every length, not a finite observed prefix.

Taking R=K_r gives beta_2=7r+1 for r>=1 and selected deficit r-1.
Thus this port-composition class approaches the sharp clean-leaf
coefficient 1/12 as r grows. The fixed-degree-six construction in the
preceding note attains the coefficient exactly; the port class instead
gives an exact formula for arbitrary interface graphs and degree-four
examples. No claim of full rectangular-grid equality follows from these
constructions.

## Verification

Run `python3 scripts/check_selected_star_ports.py`. The checker
enumerates the whole block to verify the forced ports in every eight-set,
compares literal star formation with the local condition, checks every
deletion including new outside vertices, and compares unrestricted
dissociation optima with the composition formula on small interfaces.
Larger tests check actual edge lists, induced block identity, port
memberships and attaining sets. General proofs are above. Independent
review is pending; no Lean or historical-priority verification is claimed.
