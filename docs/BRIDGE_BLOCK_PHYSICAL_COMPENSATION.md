# Exact physical compensation by bridge blocks

The [strip model](STRIP_TREE_PHYSICAL_COMPENSATION.md) gives an exact
three-colour formulation for actual TH expense. Its global feedback algorithm
takes O(3^k |V|) arithmetic operations at total cross-cell cycle rank k.
Here that exponent is localized: many cycles separated by bridges do not
have to be conditioned simultaneously. This yields a linear exact solver
on a physical grid class with arbitrarily large total cycle rank.

Bridge decomposition, conditional tree messages and feedback conditioning
are standard graph methods. The result here is their exact application to
the physical strip constraints and actual-edge fees, with a precise
normalization rule and literal interfaces. It is a theorem about the stated
restricted auxiliary matchings, not a universal numerical 5/6 bound.

## 1. Hypotheses and theorem

Use the hypotheses of the strip note: a rectangular bipartite grid, fixed
actual partial matching M, endpoint footprint P, selected T in Q=V\P,
H=Q\T, nonnegative integer weight per actual M edge, and a partition into
two-column rectangular cells. Auxiliary N is a full domino matching confined
to these cells. The algorithmic theorem does not require the extra
sub-quorum degree condition on T.

Let K be the actual-M cell MULTIGRAPH. Each cross-cell actual edge gives
one distinct multigraph edge. Delete every bridge of K, and let B range
over the resulting connected components, including isolated cell vertices.
Write V_B for the original grid vertices in B's cells and

    k_B = number of nonbridge cross-cell edges inside B
          - number of cells in B + 1.

**Bridge-block theorem.** Feasibility and the exact minimum physical TH fee
are computable, with full N and unique actual-edge payment sets as witnesses,
in

    O( sum_B 3^(k_B) |V_B| ) arithmetic operations,
    O(|V|) storage.

In particular, if r=max_B k_B is bounded, the bound is O(3^r |V|), regardless
of the total rank k=sum_B k_B. All finite costs remain integers, with bit
length bounded by that of 1+sum_e w_e. Impossible conditions are a separate
symbolic value. Coordinate/hash access is taken at unit cost, as in the strip
algorithm; this is an arithmetic-operation bound, not a claim of constant
bit cost for unbounded weights or coordinates.

The partition here is by BRIDGES, not articulation vertices. Two cycles
sharing one cell generally remain in the same B. The cell's internal
physical relation can couple their ports; no independence is inferred merely
because cycles share only one cell. Parallel edges are not bridges and
contribute to k_B.

## 2. Single-colour physical bridge interfaces

Use labels 0,R,B and terminal restrictions from the strip note. Both ends
of every M edge have the same label; local same-colour N matchings must
physically lift. The unrestricted minimum label objective equals physical
TH expense by the exact-cost theorem.

Contract each B to one vertex. The remaining bridge graph is a forest,
including the original connected components independently. Across a parent
bridge e the only link between the two sides is this ONE actual M edge:
N cannot cross cells, hence cannot create another link across the cut.
Its common colour is therefore a sufficient message interface for the
label optimization. It is not an arbitrary exchange of endpoints or a
scalar capacity relaxation.

For a nonroot block B, let e_B be its parent bridge. Define m_B(c) to be
the minimum label cost in its whole block subtree conditional on colour c
on e_B, INCLUDING w_(e_B)[c!=0] exactly once. The endpoint of e_B inside B
remains occupied P, even though the parent block is outside the subproblem.
Deleting a bridge from a message graph never turns its endpoints into Q.

Every child bridge endpoint v in B receives the three-entry unary cost
m_child(c) at v. Distinct bridge endpoints belong to distinct actual edges;
the original matching condition prevents two child bridges sharing one
physical endpoint. The local solver may therefore add all child messages
without sharing one physical resource. Internal actual edges and internal
cross-cell tree edges are charged as in the strip algorithm. The parent
bridge fee is added only after the block's conditional optimum is computed.

## 3. Exact conditional optimization inside one block

Choose a spanning tree of B's cell multigraph. Its complement has k_B
distinct physical feedback edges. For each of the 3^k_B colour assignments:

1. Pin both actual endpoints of every feedback edge to its assigned colour.
   Keep these endpoints occupied and add that edge's fee once outside
   the local tree messages.
2. Pin the parent-bridge endpoint to its message condition, if present.
3. Optimize the remaining cell tree using the at-most-18-state row transfer,
   including child-block unary costs. The transfer retains previous row
   labels even when N has no pending vertical pair, and enumerates all
   physical mono vertical choices as well as mixed pairs.

The parent bridge, feedback edges and child bridges are distinct M edges,
so their pins cannot conflict at one vertex. Infeasibility can still arise
from the physical local matching constraints and is retained symbolically.

Every block-subtree labeling restricts to exactly one local feedback
assignment and one colour per child bridge. Conversely the selected tree
labeling and optimal child messages combine to a valid block-subtree
labeling, with no further edges between them. Conditional optimum equality
follows by induction up the bridge forest. A root has no parent pin. Sum
root optima and backtrack block choices, then cell-tree choices, to obtain
the full global labels and N.

No physical cycle refund is subtracted within a fixed feedback assignment:
the earlier two-parallel-edge red cycle can still have label fee 2 and
physical TH fee 0 in that branch. Messages carry LABEL objectives. At the
complete global minimum, normalize all coloured P-only cycles unused, as
in the strip exact-cost proof. This establishes equality with the true
minimum TH expense, including zero weights, doubled edges and parallel
cross-cell edges.

## 4. Physical cycle confinement and resource accounting

**Cycle confinement lemma.** Every P-only alternating component of M union
N lies within a single bridge block of K. In particular no bridge actual
edge can provide free-cycle credit across a bridge cut.

Proof. If an alternating cycle contained bridge e, project the cycle to
cell vertices. N steps and internal M steps stay in one cell; a cross-cell
M step traverses its actual multigraph edge. A closed walk crosses the cut
of e an even number of times. Since e is the only edge across that cut,
it would have to occur at least twice. A simple physical alternating cycle
uses each actual M edge once, contradiction. Tagged shared M/N edges give
a doubled component inside one cell and do not affect the argument.

Thus a bridge is always on a terminal path, and each actual edge belongs
to exactly one final TH path, bad terminal path or internal free cycle.
Fees are owned in disjoint locations: internal M in its cell, nonbridge
tree M at its child cell, feedback M once per branch, and bridge M at its
child block. A path may pass many blocks; each of its actual edges still
has exactly one owner. Recolouring a complete free cycle cannot alter any
bridge colour. These facts explain precisely why bridge messages can be
combined, while a free-cycle credit cannot be spent again by another block.

## 5. Complexity and implementation

Iterative low-link traversal finds bridges in O(|V|) operations. Skip only
the parent EDGE, not every edge to the parent vertex: the latter mistake
would falsely mark a pair of parallel actual edges as bridges. A second
traversal builds B and its spanning-tree plan. All this preprocessing is
linear since M is a matching.

For B, the three possible parent conditions are a fixed factor. Each
feedback branch processes each cell row and local actual edge a bounded
number of times. The strip row-state count is fixed; child messages are
unary at actual endpoints. Thus B costs O(3^k_B |V_B|), and summing gives
the theorem. Store only three best block reconstructions and messages, not
all feedback branches. Local dynamic-programming storage, saved choices,
input and final reconstruction together occupy O(|V|). The final component
check is one linear traversal, rather than a repeated scan over remaining
components.

The companion implementation supports uniform row-block heights, including
a shorter final block. The proof allows arbitrary two-column rectangular
cells, just as the earlier strip theorem. No complexity claim is inferred
from benchmark timings; the bound follows from these bounded traversals.

## 6. A connected physical family with unbounded total rank

For any q>=1 take a 4-by-4q board and full-height two-column cells. For
j=0,...,q-1 put in M the two edges

    (r,4j+1)--(r,4j+2), r=0,1.

For j=0,...,q-2 additionally put the bridge edge

    (2,4j+3)--(2,4j+4).

All endpoints are distinct, so this is an actual partial matching. Let
T={(3,0),(0,4q-1)}. The first point has no occupied neighbour, and the
second exactly one; they are nonadjacent, so T satisfies the sub-quorum
selected-degree condition. The cell graph is connected. It has q blocks,
each a pair of parallel edges on two cells, joined by q-1 bridges. Thus

    total cycle rank = q,       max block cycle rank = 1.

All-vertical N on row pairs (0,1) and (2,3) is a full physical witness with
zero TH fee under all nonnegative weights: both selected vertices are
directly N-paired to holes, the parallel M pairs lie on P-only four-cycles,
and every bridge lies on an HH path. The old global feedback enumeration
has 3^q branches. The block solver makes exactly

    3 + 9(q-1) = 9q-6

conditional feedback evaluations: three at the root block, nine per other
block. Each block has fixed size. The general theorem therefore gives a
linear exact solver on a connected feasible physical family of unbounded
global rank; this is not a complexity conclusion extrapolated from samples.

## 7. Verification and scope

The checker compares the bridge-block optimum with independently enumerated
full physical N on all small actual weighted models in two geometries,
and with the previous global-rank solver. Additional controls include
random boards, zero and huge integer weights, genuine parallel edges,
short final cells, and the connected q-cycle family. The earlier solver's
large-integer and linear-component repairs have a separate review; that
review does not cover this new theorem or implementation.

This result removes the need for small TOTAL cycle rank when the rank is
distributed across actual bridge blocks. It does not promise that an
arbitrary feasible T has a covering within these cells or improve the
universal 5/6 coefficient. No new Lean formalization is claimed.

## 8. An all-size obstacle to a universal block-rank assumption

The following additional deduction was added AFTER the initial bridge-block
review snapshot. It is not covered by an opinion on that earlier snapshot.

For n>=2 take a 2-by-2n board, two-column full-height cells, and

    M = {(r,2j+1)--(r,2j+2): r=0,1; j=0,...,n-2},
    T = {(0,0),(0,2n-1)}.

The actual edges are disjoint. Each selected point has exactly one P
neighbour and no selected neighbour, so the original feasibility condition
holds. There are 2n-2 actual M edges and two selected points; consequently
J=2n=|V|/2 exactly.

The cell multigraph is a chain on n vertices with TWO parallel actual
edges at each link. Every link pair lies on a two-edge multigraph cycle,
so there is no bridge. The whole graph is one bridge block with

    k_B = 2(n-1)-n+1 = n-1.

Thus feasible T, fixed height, and even exact half-area equality together
do not bound the largest bridge-block rank. This conclusion follows for
all n from the explicit multigraph; it is not inferred from the finite
controls.

Nevertheless N consisting of every vertical rung gives zero TH fee:
the two outer columns are direct TH paths and each pair of parallel M
edges forms a free P-only four-cycle. All actual M edges are free, once
each. Hence this is an obstruction to the proposed universal RANK BOUND,
not to coverage, zero-fee compensation or the numerical target.

Adjacent two-edge cycles share a cell, so splitting at articulation cells
and assigning them independent scalar credit is not licensed by the
bridge theorem. Any extension across such a cell must preserve its joint
physical port relation. The next step is therefore a stronger separator
model with explicit boundary-colour tuples, rather than attempting to
deduce a universal bounded bridge-block rank from feasibility.
