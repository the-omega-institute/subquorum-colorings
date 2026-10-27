# Capacity-preserving coarsening loses physical port constraints

The exact 2-by-2 compensation theorem does **not** extend by replacing two
adjacent squares with a single 4-by-2 cell, even if all physical M-edge
capacities and all receiving reserves are respected. There are feasible
rectangular examples for which every coarse regional inequality holds and
all coarse debts are paid, but every cell-confined auxiliary matching leaves
a TT component. The gap is arbitrarily large on connected rectangular boards.

The physical construction and its forced-port obstruction are from
[Sections 8--9 of the general-square note](GENERAL_SQUARE_PORTS_AND_TILE_CUTS.md).
The new deduction here is an exact interpretation of coarse compensation as
a relaxation, an explicit capacity-respecting false certificate, and its
unbounded amplification. It concerns a proposed extension of the method,
not a counterexample to the numerical 5/6 target.

## 1. What a scalar balanced-cell model actually computes

Let M be a partial matching of a finite bipartite grid, with occupied set P,
unoccupied set Q=V\P, selected terminals T in Q, and holes H=Q\T. Partition the board
into cells C, each with a_C black and a_C white vertices. Restrict the auxiliary
full matching N to edges within cells. For U a set of cells let R(U) be its
union, and let M_int(R) include every actual M edge with both endpoints in R,
including edges between different cells of U. Set

    delta_rel = max_U [ |T intersect R(U)| + |M_int(R(U))|
                       - sum_(C in U) a_C ].                 (1)

Every physical cell-confined N has TT >= delta_rel. Moreover delta_rel is
exactly the minimum TT in the **complete-port relaxation**: permit N to pair
any black vertex with any white vertex of the same cell, regardless of grid
adjacency. The relaxation keeps the actual M unchanged.

Proof. Orient N black-to-white and M white-to-black, retaining both tagged
copies when an edge is shared. After removing all N copies, each Q vertex
is a terminal singleton and each M edge a directed fragment with capacity
one. Collapse each cell to one switching node. Add a unit source arc for each
black T and a unit sink arc for each white H. An actual M edge gives one arc
from its white endpoint's cell to its black endpoint's cell; intra-cell edges
are loops. An N routing with x TT components supplies a flow of value B_T-x.

Conversely a maximum integral flow of value F marks incoming and outgoing ports at
each cell in equal numbers. Pair marked black and white ports, and then pair
unmarked ports. Arbitrary bijections are available in the relaxation, so this
is a full relaxed N. Marked source paths reach white H, since a terminal path
cannot enter a directed cycle. Thus minimum TT=B_T-F, by the same two-sided
argument as for the exact square model. This pairing step is precisely what
requires additional justification for physical cells.

Normalize a min-cut by putting black/white T terminals on its source side and
black/white H on its sink side. For cell set U, its deficiency is

    T_black(R) - H_white(R) - M_white-out(R).

The white-vertex identities

    sum a_C = P_white(R)+T_white(R)+H_white(R),
    P_white(R) = |M_int(R)|+M_white-out(R)

give (1). Empty U gives zero. Integral max-flow/min-cut proves exactness in
the relaxation and the necessary physical lower bound. This argument uses
balanced cells, not their shape, and does not assume local feasibility.

For a cell let t_C=|T in C|, p_C=|P in C|, i_C=|M internal to C|, and

    s_C=a_C-t_C-i_C,  d_C=p_C-2i_C,
    k_C=2a_C-2t_C-p_C=2s_C-d_C.

If E(U) counts cross-cell actual M edges inside U once, then

    delta_rel=max_U [E(U)-sum_(C in U) s_C],
    2 delta_rel=max_U [D(U)-K(U)-boundary_M(U)],             (2)

where D(U)=sum max(-k_C,0), K(U)=sum max(k_C,0). In the undirected actual-M
cell multigraph let debt C supply max(-k_C,0), reserve C receive at most
max(k_C,0), and give each physical cross-cell M edge capacity one. If F_D is
the maximum integral debt-to-reserve flow and D the total debt, then

    delta_rel=(D-F_D)/2.                                   (3)

Indeed sum d_C=2E(U)+boundary_M(U) proves (2). The usual undirected flow cut
has capacity D-D(U)+K(U)+boundary_M(U), proving (3). Cancel opposite flows
on the same actual edge before decomposing into paths: each physical edge
is used at most once, and each receiving budget at most its stated value.
Thus a gap below cannot be blamed on duplicate capacity or duplicate credit.

For 2-by-2 cells every bijection of two black and two white ports is a grid
perfect matching, so the relaxation is exact. A 4-by-2 cell has only five
domino matchings, compared with 4! arbitrary black/white bijections; the
missing port constraints can change the global optimum.

## 2. A false certificate on every 4-by-w board, w even and at least six

Write w=2n, n>=3. Use the existing family, with coordinates from zero:

* M has top-row edges (0,c)--(0,c+1) at odd c=1,3,...,w-3;
  row-one edges (1,c)--(1,c+1) at even c=2,4,...,w-4;
  and side edges (1,1)--(2,1), (1,w-2)--(2,w-2).
* T contains (0,0),(0,w-1),(2,0),(2,w-1),(3,1),(3,w-2),
  plus (2,c) at odd 3<=c<w-3 and (3,c) at even 4<=c<w-2.

These disjoint M clauses cover P; |M|=w-1 and |T|=w. Every T sees at most
one neighbour in P union T: the six special vertices see their single P
neighbour, the remaining row-two selections see one P above, and the remaining
row-three selections see neither P nor T. The transition gaps exclude extra
selected neighbours. Thus this is an actual feasible configuration.

Take the n cells C_j={0,1,2,3} x {2j,2j+1}. The cross-cell M graph is the
simple path C_0--C_1--...--C_(n-1), with precisely the top-row actual edges.
Every cell has a_C=4. Both end cells have (t,p,i)=(3,3,1), hence s=0,k=-1.
For interior cells p=4,i=1 and k=4-2t:

* n=3: the sole interior cell has t=0, s=3, k=4;
* n>=4: cells 1 and n-2 have t=1, s=2, k=2;
  all other interior cells have t=2, s=1, k=0.

There are two debts. Send the left debt across the first physical M edge
to C_1, and the right debt across the last physical M edge to C_(n-2).
These edges are distinct even when n=3. For n=3 the common receiving cell
has reserve four and receives two units; otherwise the two receiving cells
are distinct and each has reserve two and receives one. Thus F_D=D=2,
and (3) gives delta_rel=0. ALL regional inequalities in (1) hold, including
disconnected regions. No actual edge or receiving unit has been reused.

Nevertheless the exact physical minimum over all 5^n cell-confined domino
matchings is

    delta_physical=1.                                    (4)

Here is the all-size port proof, not an inference from enumeration. In each
interior strip the two top vertices are either matched horizontally to each
other, or both matched down to the row-one vertices. In the latter case the
internal row-one M edge joins them. Thus the two external top M ports always
continue into each other, independently of the bottom half of the strip.

At the left end the external port is (0,1). If its N edge is horizontal,
it reaches selected (0,0). Otherwise (0,1) goes down to (1,1), then by M to
(2,1). The latter's N edge cannot return to (1,1), already N-matched to
(0,1); its only remaining neighbours in the cell are (2,0),(3,1), both T.
The right end is the mirror statement. Concatenating the forced interior
connections and the two selected ends gives a TT component for EVERY N.
All-horizontal N attains exactly one TT, so (4) is sharp.

For comparison, refine each cell into its two 2-by-2 squares. The original
fine model has two debt ends joined by zero-reserve upper tiles, with no
reachable reserve. Its exact residual is one. Coarsening merged the upper
through-ports with the lower reserve, supplying a connection that no domino
phase of the larger cell can realize. Allowing the fifth 4-by-2 domino state
does not fix this: the forced two-port continuation holds in that state too.

## 3. An unbounded gap on connected rectangles with uniform cells

For arbitrary integers q>=1 and even w>=6 take the 8q-by-w board. In rows
8k,...,8k+3 put a translated copy of the preceding M,T family, for k=0,...,q-1.
Leave rows 8k+4,...,8k+7 entirely in H. Tile the WHOLE board by uniform 4-by-2
cells, aligned at rows 0,4,8,... and even columns.

The four separator rows prevent new selected neighbours across copies, so
the configuration is feasible. Each active four-row band has its own M path
and two debts. Every empty cell has k=8 and no incident actual M edge. The
explicit two-unit flows above combine on edge-disjoint active components;
all debts are paid, so delta_rel=0 and every coarse regional inequality holds.

For cell-confined N no N edge crosses a cell boundary, and no actual M edge
leaves an active band. Each band's forced chain therefore contributes a
different TT component. Empty cells contribute only HH. All-horizontal N
attains the lower bound, proving the exact gap

    delta_physical=q,   delta_rel=0.                       (5)

This is a connected physical board, with a single uniform cell shape. It
does not rely on disconnected ambient grids or overlapping compensation
resources. Its numerical value |M|+|T|=q(2w-1) is below half the area 4qw.
Unrestricted full auxiliary matchings can cover every selected vertex with
zero M cost: apply the prior explicit full completion in each active band
and use horizontal pairs in separator rows. Thus (5) refutes the coarse
certificate, not the target inequality or unrestricted coverage.

There is also an exact distinction between static coarsening and successive
physical changes. Starting from the all-horizontal N_0, the minimum TT over
ALL single independent batches on this stacked board is ONE, whereas exactly
TWO batches suffice to reach zero at zero final M cost. For the one-batch
lower bound, every available square starts in an even column, so all final
N edges remain within the global two-column strips. In the first active
band the top ports still cannot escape upwards (row zero is the board edge),
and the end-port proof still ends at its selected vertices in rows zero,
two or three. It does not rely on any N choices below that first band.
Thus its forced TT survives any one batch.

For the matching upper bound, in every other active band k>=1 flip just the
square with upper-left corner (8k-1,2). It joins that band's old top-row TT
to an N-only HH edge in the separator immediately above. These q-1 squares
are vertex-disjoint and concern different TT and HH components; each replaces
one TT and one HH by two TH. Exactly the first TT remains. Finally, the prior
two-batch construction, applied in every two-row band of the whole rectangle,
covers every T directly. Both batches are independently disjoint, and the
final payment set is empty. The unbounded coarse error q therefore does not
imply unbounded necessary batch depth; the latter is exactly two in this family.

## 4. Exact local Hall criterion for lifting a coarse flow

There is a precise repair of the missing lifting step. This uses classical
finite bipartite Hall, rather than asserting a new Hall theorem. In the
directed complete-port network of Section 1, consider an integral flow of
value B_T with every individual arc capacity one. Allow capacity-one
intra-cell M loops and circulations: discarding them before testing local
realizability need not preserve the local port labels.

Give every vertex its red bit as follows. Black T have bit one; black H and
white T have bit zero. A white H has the bit of its sink arc. Both endpoints
of an actual M edge have the bit of that edge's flow arc. The last convention
also applies to intra-cell M edges. Conservation says that within each cell
the red black and red white sets have the same size; their complements also
have the same size.

**Lifting criterion.** Such a flow is realizable by a physical cell-confined
full N preserving these bits if and only if, in every cell C, for each bit
epsilon in {0,1} and every subset A of the black epsilon vertices,

    |A| <= |N_(G[C])(A) intersect {white epsilon vertices}|.       (6)

Consequently physical full T coverage exists in the cell class if and only
if there exists a value-B_T integral flow satisfying all these local tests.

Proof. A physical bit-preserving N supplies an injection for every A, proving
necessity. Conversely apply bipartite Hall separately to the two induced
same-bit subgraphs in C. The equal side sizes imply perfect matchings of
both, whose union is a full grid matching within C. Taking these unions in
all cells gives a physical N. Along N and M every terminal path preserves
its bit, so no black T (one) can reach a white T (zero); hence TT=0 and all
T are covered. For the existential converse, take any physical covering N
and mark exactly its black-T/white-H paths. Their actual M edges and terminal
arcs give the required integral flow and local matchings. Unused cycles can
remain unmarked. This proves both implications without assuming the scalar
optimum itself has a realizable maximizer.

One must test BOTH bits: matching only the marked ports can leave the
unmarked vertices without a full local completion. Also the criterion is
existential over flows. A failed local test for a particular maximum flow
does not generally rule out another maximum flow; the family in Sections
2--3 excludes every possible lift by its independent forced-port proof.
No polynomial-time claim follows from the coupled integral-flow/Hall model.

## 5. What a valid extension must retain

An exact coarse model must retain the admissible local port pairings, or an
equivalent set of local constraints sufficient to lift every decoded routing.
The five domino states of a 4-by-2 cell are one exact local representation;
their shared interface ports must be reconciled globally. Replacing them by
a node with only conservation and aggregate reserve is a strict relaxation.
Capacity checks alone do not prove this missing lifting statement.

Successive square batches remain a possible physical repair: the prior
two-batch construction covers the single-band family at zero final M cost.
Its intermediate port state changes, whereas a static coarse flow silently
assumes all those connections are simultaneously available. A general
extension must prove both physical realizability and the signed old/new
cycle ledger. Neither follows from (1)--(3).

The companion checker constructs actual edge sets, checks all five local
domino states and all balanced local red-bit profiles, compares directed
complete-port flow with undirected debt flow and regional cuts on small
controls, produces failed local Hall witnesses for the relaxed certificates,
and checks the stacked physical families. The Lean source proves local strip matching constraints from
grid adjacency and mate involution. Global max-flow/min-cut, the coordinate
family and stacking are the written proofs above; they are not end-to-end
Lean formalizations. Finite enumerations validate these proofs and adapters.
