# Exact TH optimization and a zero-expense theorem for ladders

We give an exact formulation of the source-dependent TH expense by two
vertex labels. On a grid of bounded width, this yields an exact frontier
algorithm that chooses the routes and completes the board together. We also
prove that every feasible selection on a full two-row rectangular grid has
a zero-expense completion, with a linear construction.

## 1. The expense and its exact binary formulation

Let G=(V,E) be a finite bipartite graph with equally many white and black
vertices. Fix a matching M, let P be its endpoints, and put Q=V\\P. Fix a
set T of white vertices of Q; let W be the other white vertices of Q. Each
actual edge e in M has a nonnegative weight w_e. A full auxiliary matching
N is a perfect matching of G. Use separate copies of M and N when an edge
belongs to both matchings.

In the tagged union M+N, vertices in P have degree two and vertices in Q
have degree one. Each component is therefore a cycle contained in P or
an alternating path with both endpoints in Q. The first and last edges of
such a path belong to N, so its length is odd and its endpoints have
opposite colours. Orient it from its white endpoint. A TH component starts
in T; an HH component starts in W. Define f(N) as the sum of actual-edge
weights on all TH components. Cycles and HH components are free.

For a pair (N,x), impose the following local constraints:

* N is a perfect matching;
* each vertex v has a label x_v in {0,1};
* x_t=1 for t in T, and x_w=0 for w in W;
* the endpoints of every actual edge, and every chosen auxiliary edge,
  have the same label.

Set L(N,x)=sum_{e=uv in M} w_e x_u; the actual-edge constraint makes this
independent of the endpoint chosen.

**Theorem 1.** With minimum over the empty feasible set interpreted as
infinity,

    min_{N perfect} f(N) = min_{(N,x) feasible} L(N,x).

Every optimal labelled pair yields a genuinely optimal full N.

**Proof.** The constraints make x constant on each component of M+N. A TH
component must have label one, and an HH component must have label zero.
Only cycles are free to take either label. Thus for every feasible pair,

    L(N,x) = f(N) + sum_{label-one cycles C} sum_{e in M cap C} w_e >= f(N).

Conversely, for any perfect N, assign label one to its TH components and
zero to every other component. This satisfies every constraint and has
L(N,x)=f(N). Taking minima gives the identity and also proves simultaneous
feasibility. If (N,x) is optimal, then

    min f <= f(N) <= L(N,x) = min f,

so its N attains the true optimum. This proof covers zero weights and common
M/N edges, which form two-edge cycles in the tagged union. Nonnegativity
is needed: a negative label-one cycle could lower L below f. Pointwise
equality L=f is not asserted for arbitrary feasible labels. QED.

The formulation accounts for source ownership by labels and physical
capacity by the perfect matching constraint. Every actual edge is charged
once. It permits arbitrarily long free HH paths and chooses between tied
route optimizers through the full-board constraint.

### Retained terminal paths

Suppose R is a collection of vertex-disjoint complete alternating paths,
each oriented from white Q to black Q, with all interior vertices in P and
with actual edges on the alternating interior steps. Retain their auxiliary
steps. Every internal actual pair is removed whole, so no actual edge
crosses the deletion of V(R). The remaining board is balanced. Let b_R be
the fixed expense of TH paths in R.

**Corollary 2.** The minimum expense among full matchings retaining R is
b_R plus the binary-label optimum of the residual board. A residual optimum
and the auxiliary steps in R give an attaining original full matching.

**Proof.** At every retained-path vertex its required auxiliary edge is
already fixed. Thus restriction and extension are inverse bijections between
retaining perfect matchings and perfect matchings of the residual graph.
The overlay components on retained vertices are precisely those paths;
all other components lie in the residual graph. Expenses add. Apply
Theorem 1 to the residual instance. QED.

## 2. Frontier algorithm on a grid

Use the induced four-neighbour graph on any finite balanced set of integer
grid vertices. Let h be the shorter side of its bounding rectangle and n
its number of vertices. Scan columns when the height is h, or transpose.
Order vertices within each column by row. Introduce each vertex, process
all its edges to earlier introduced neighbours, and then forget every
vertex whose last neighbour has now been introduced. Isolated vertices
are introduced and immediately tested for forgetting.

For each active vertex keep two bits: its label and whether a chosen
auxiliary edge has already matched it. Store the minimum accumulated L
for each state. The transitions are:

1. Introduce v with matched bit zero and every permitted label. A white Q
   vertex has its fixed source label; a vertex in P or a black Q vertex
   may take either label.
2. On an edge e=uv, one may omit it from N. One may choose it in N exactly
   when both matched bits are zero and the labels agree, setting both
   matched bits to one. If e belongs to M, discard unequal-label states
   and add w_e x_u exactly once to either alternative.
3. Forget v only if its matched bit is one; remove its two bits.

Start with the empty state of value zero. A final empty state gives the
optimum; no final state means there is no perfect matching. Store a
predecessor and chosen-edge/label action for each minimizing state to
recover the full N and labels. Value-only mode keeps just two tables.

**Theorem 3.** These transitions exactly compute the minimum in Theorem 1.
There are at most 4^(h+1) states at any event, O(n) events, and a constant
number of transitions per state per event. Thus the algorithm uses
O(n 4^(h+1)) state transitions and O(4^(h+1)) rolling state records, or
O(n 4^(h+1)) records with full witness history.

**Proof.** By induction on events, a table entry is the least expense of
all choices on introduced vertices and processed edges satisfying the
source labels, every processed actual-edge constraint, and all selected
auxiliary-edge constraints, with auxiliary degree at most one everywhere
and exactly one at each forgotten vertex. The state specifies exactly the
remaining information needed by future edges. Each transition enumerates
all allowed extensions and charges an actual edge only at its edge event.
Forgetting is valid because that vertex has no future neighbour. At the
end the constraints are exactly those of Theorem 1. Keeping the least
expense per state is valid because all continuations depend only on its
bits. Reversing stored predecessors reconstructs an attaining pair.

For the bag bound, consider introducing row r of a column. An active vertex
in the preceding column can occur only at an unprocessed row, or at row r
until its edge is processed. Current-column vertices can occur only in
processed rows. Before forgetting, the two counts sum to at most h+1.
No earlier column can remain active. Missing vertices can only reduce
these counts. The grid has at most 2n edges, and there are n introduce and
n forget events. Each vertex has four possible bit states and each edge
at most two alternatives. This proves the bounds. QED.

These are counts of state records and transitions, rather than bit-operation
bounds. The Python implementation uses tuples of length at most h+1, so
tuple construction/hashing and witness storage introduce a factor O(h).
Sorting arbitrary integer coordinates costs O(n log n) comparisons; adjacency
uses four set probes per vertex. Integer comparisons/additions also have
their ordinary cost in the accumulated-weight bit length. For fixed h this
is an exact algorithm polynomial in input length. The algorithm is
exponential in h, and is not a polynomial-time algorithm for arbitrary-width
rectangles. The two-bit frontier recurrence is an application of standard
dynamic programming on a path decomposition; the result here is the exact
source-expense representation and its use for this completion problem.

## 3. Every feasible two-row ladder has zero expense

Now let G be the full 2-by-n rectangular grid, for any integer n>=1, with
arbitrary actual matching M. Let T be any set of white Q vertices such that
each t in T has at most one neighbour in P. No paths are prescribed.

Write w_j and b_j for the white and black vertices in column j. Each white
w_j is adjacent to b_j and, when present, b_(j-1), b_(j+1). Its rung is
w_j b_j. Call a column j bad if w_j belongs to T and b_j belongs to P.

**Theorem 4.** There is a full auxiliary matching in which every selected
vertex is paired directly with a black vertex of Q. Consequently f*=0
for every assignment of nonnegative weights to M. It can be constructed
by disjoint adjacent-column swaps in linear time.

**Proof.** For each bad j, the actual mate of b_j is w_i for an adjacent
column i: it cannot be w_j because w_j belongs to Q. Thus |i-j|=1 and
w_i belongs to P. Since w_j already has the occupied neighbour b_j, the
feasibility condition forces b_i to be in Q.

Swap the rungs in columns i,j: choose w_i b_j (the actual edge) and w_j b_i
(the other horizontal edge). These swaps for different bad columns are
disjoint. Indeed a bad-column index always has its white vertex in Q,
whereas a mate-column index has its white vertex in P, so the two kinds
cannot coincide. Two bad indices cannot share a mate index because M is a
matching. Distinct bad indices are distinct by definition. Therefore every
column is in at most one swap.

Use the rung w_j b_j in all unused columns. This is a perfect matching.
Every selected white vertex in a bad column is paired to the black Q
vertex b_i. A selected vertex in any other column is not in a swap (mate
columns are occupied whites), and its rung endpoint is in Q by the
definition of bad. Thus all TH paths are single auxiliary edges, their
expense is zero, and nonnegative expenses prove optimality. The scan,
mate lookup and swaps take linear time. The construction also applies to
translated and transposed ladders. QED.

The selected-neighbour condition matters. In the full 2-by-3 grid take
M={w_1 b_2,w_2 b_3}, T={w_3}, and unit actual weights. Both neighbours of
w_3 are occupied, so its TH component must cost at least one. The perfect
matching {w_1 b_1,w_2 b_3,w_3 b_2} has exactly one paid actual edge,
w_1 b_2, and hence f*=1. This example violates the hypothesis at w_3.

### Why a retained ladder may still cost arbitrarily much

For r>=1 take the full 2-by-4r grid. In top-row block i=0,...,r-1 put the
actual edge (0,4i+1)(0,4i+2), of weight mu>0, and select (0,4i+3). Each
selected vertex has exactly one occupied neighbour, so Theorem 4 applies.
In particular the all-vertical auxiliary matching has expense zero: every
actual edge lies on an HH component, and every selected top vertex is
paired directly to a bottom black Q vertex.

If all bottom-row horizontal HH pairs (1,2j)(1,2j+1) are retained, however,
the residual board is the single top-row path. Its unique perfect matching
uses consecutive pairs (0,2j)(0,2j+1), by induction from its degree-one end.
Every top block contributes its one actual edge to a TH component, so

    unrestricted f* = 0,      retaining f_R* = r mu.

This is an all-size example of Corollary 2 and of why a conditional routing
choice cannot certify an unrestricted optimum. The exact optimizer handles
both questions by including or omitting the retained paths.

## 4. Implementation, checks and remaining scope

`scripts/source_label_dp.py` supplies the integer-weight optimizer and the
linear ladder constructor. `scripts/check_source_label_dp.py` compares it
with literal full-matching enumeration and independent overlay scoring;
it also checks source labels, actual/auxiliary degree and adjacency,
retention, alternative scans, value-only mode, infeasibility, zero weights,
401-bit weights, and the long cascade. Separate colour enumeration checks
the reduction without using the frontier recurrence. Reports and small
full witnesses are in `output/source-label-dp-*.json`.

The ladder proof is structural and holds for every n. Finite exhaustive
controls enumerate all actual matchings on 2-by-n for 1<=n<=8, construct
for the maximal feasible T and thereby cover every subset of it, and
cross-check selected cases with the exact optimizer. The tests are not
premises of the general proofs.

This resolves the unrestricted exact TH-optimization subproblem by width
and gives a zero-expense geometric class. The wider rectangular-grid
triple equality and a universal improvement of the 5/6 colouring coefficient
remain open. In particular, a zero-expense auxiliary completion alone is
not asserted to prove the three graph parameters equal, even on ladders.
