# Arbitrary rematching in the zero-direct-defect family reduces to one shortest relay

This strengthens Theorem 3 of
[MONOCHROMATIC_COMPLETION_FLOW_AND_UNBOUNDED_ZERO_DEFECT_COST.md](MONOCHROMATIC_COMPLETION_FLOW_AND_UNBOUNDED_ZERO_DEFECT_COST.md).
For the SAME new corner-square family, we can replace the unit-weight lower
bound under rematching by an exact arbitrary-weight formula for EVERY actual
rematching of its endpoint footprint. No full-flow optimization is needed
for this particular family: one shortest alternating path suffices, and
its surrounding direct completion is explicit.

## 1. Fixed data and optimization domain

Let k>=1, G the side-(4k+4) square, S={0,...,4k}^2, h=(2k,2k),
P=S\{h}, Q=V\P, and z=(0,4k+3). Colour odd-coordinate-sum vertices white.
As before, T=Q_white\{z}; H=Q\T. Let M now be ANY perfect grid matching
of this fixed P, not necessarily the earlier vertical/horizontal formula.
Assign arbitrary nonnegative actual-edge weights w_e.

Write L for the old width-one outer L-path of the side-(4k+2) square:

    (0,4k+1),(1,4k+1),...,(4k+1,4k+1),
    (4k+1,4k),...,(4k+1,0).

Its selected white vertices are precisely its even-index vertices. All
other white Q vertices except z are also selected, as in the full family.
The original feasibility condition holds independently of this rematching
because it depends on P and T alone.

Define a directed relay graph with vertices P union {h} union L_white.
For each black vertex b, including h, direct its non-M grid edges toward
adjacent white vertices in this graph, with cost zero. From each white
P vertex direct its unique M edge toward its black mate, with cost w_e.
The vertices of L_white are terminal sinks. These arcs are the reversal
of the physical complete-flow orientation, stopping at the inner boundary.
Let rho(M,w) be the shortest directed h-to-L_white path cost.

**Theorem.** Such a path always exists, and the exact unrestricted full-N
TH optimum is

    min_(N full) f(N) = rho(M,w).                              (1)

Every full N has a=0. An optimal full N can be chosen with exactly ONE
TH component containing actual edges, namely a shortest relay (it may
have total weight zero); all other TH components are direct, the unique
HH component is direct, and all unused actual edges are doubled free.

## 2. Lower bound under an arbitrary rematching

Every T is white, so an alternating terminal path, whose length is odd,
cannot have two T endpoints. The only white H is z. Since z has no P
neighbour, its auxiliary edge goes directly to a black H and forms an
entire HH component. In particular isolated black h cannot be paid by z.

In the tagged decomposition of ANY full N, the path starting at h must
therefore end at a white T. Its internal vertices are all in P, hence
inside S. The first vertex it meets outside S is a white neighbour of
its black boundary vertex in S, and belongs to L_white. A terminal path
stops on meeting Q. Consequently it cannot first end farther out in the
new two-row/two-column annulus. Reversed from h, its steps are precisely
zero-cost non-M grid arcs followed alternately by weighted M arcs in
the relay graph. Its M expense is at least rho(M,w).

All other TH components have nonnegative weights. Thus f(N)>=rho(M,w)
for every full N. Ambient full N exists on the even square, so this same
argument also proves that the relay graph has a path, for EVERY matching
of P. It does not assume that the prescribed old straight relay survives
rematching.

## 3. Every simple relay has a full direct completion

Choose a least-cost relay; remove cycles without increasing cost, so it
can be taken simple. Its only Q vertices are its initial h and final
white t in L. Reverse the path into T-to-h order. Its edge types are
N/M/N/.../M/N. Use all its N edges in the auxiliary matching, and include
every actual M edge not used by the relay as a doubled auxiliary edge.
All its internal P vertices come in their actual M pairs; thus this
covers exactly P union {h,t}, without conflict.

Delete t from the ordered L-path. Since t has even index and L has odd
length 8k+3, the subpaths before and after t both have even length.
Pair consecutive vertices in both. They cover all of L\{t}, using only
direct TH edges. They have no vertex in the relay's interior P.

Put n=4k+2. In each newly added column pair n,n+1, pair horizontally in
rows 0..n-1. In the two added bottom rows n,n+1, pair vertically in all
columns 0..n+1. These pairs cover every remaining vertex and are disjoint
from S and L. All are direct TH except the pair z--(0,n), which is HH.
This produces a full physical N. Its paid actual edges are exactly those
on the chosen relay, once each; all other actual edges are doubled free
components. Hence f(N)=rho(M,w). Together with the lower bound this proves
(1), with no selection of independently incompatible optimal routes. QED.

For unit weights, every target is at distance at least 2k+1 from h,
so rho>=k. The original explicit M has the old straight relay of expense
k. Other actual rematchings are governed by (1); we do not assert that
they all attain k. The result also holds for zero weights, since both
cycle deletion and the lower bound use nonnegativity, not strict positivity.

## 4. Implementation, verification and limits

`develop/corner_relay_shortest_path.py` constructs the relay graph implicitly
and uses standard Dijkstra search with (expense,number-of-arcs) keys. The
secondary key prevents a zero-cost predecessor cycle. It returns the actual
relay and the explicit full N above. The physical state extraction checks
that Paid equals exactly the relay's actual edges. Its arithmetic-operation
bound is O(|V| log |V|) time and O(|V|) memory on this grid family, including
coordinate generation and completion. Integer weights are handled exactly;
the mathematical proof allows all nonnegative real weights.

This is a new application/normal form within the fixed family, not a new
shortest-path algorithm or a solution of the general grid optimization.
The independent verifier compares its expense with the earlier complete
min-cost-flow adapter under actual domino rematchings, transposition, zero
weights and large integer weights. The finite checks are recorded in
`output/corner-relay-shortest-path.json`. The every-rematching equality and
full completion for arbitrary k are established by Sections 2-3, not by
sampling rematchings. No freezing or new Lean verification is claimed.
