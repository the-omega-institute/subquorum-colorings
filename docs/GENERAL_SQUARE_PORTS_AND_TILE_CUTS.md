# General square ports, exact tile compensation, and old-cycle expense

This note removes three restrictions from the physical adapter in
[the contact-flow theorem](CONTACT_FLOW_CUT_AND_EXACT_COST.md): both cuts of a
square may belong to the same original path, a cut may lie on an original
P-only cycle, and actual/auxiliary matching edges may coincide. The exact
coverage flow and joint-cost model survive. For a fixed 2-by-2 tiling the
coverage obstruction becomes an exact geometric regional inequality, or
equivalently an integral debt-to-reserve flow with single-use physical edges.
A separate all-size family shows why absorbing an old cycle must be charged.

These are statements about a fixed actual matching and prescribed independent
square pool. Classical integral flow/min-cut is the optimization ingredient.
The new content is the general physical adapter, its tile specialization and
the old-cycle counterfamily, and a sharp fixed-tiling obstruction deduced from
an existing physical family. The local tile charge classification is already
used in [the absorption notes](GRID_ABSORPTION_PROOF.md); it is not a new
classification. No universal 5/6 improvement follows without a new geometric
bound. The 11 October manuscript and public main are unchanged.

## 1. Physical hypotheses and tagged directed copies

Let G be a finite rectangular grid, with black vertices of even coordinate
sum and white vertices of odd sum. M is an actual partial matching, P its
endpoints, Q=V(G) minus P. Let T be a subset of Q satisfying

    |N_G(t) intersect (P union T)| <= 1  for every t in T.

Write H=Q minus T. T need not be independent: adjacent selected pairs are
allowed. N is any full auxiliary matching. A candidate square has two
opposite edges in N; its two other edges give its alternative phase. Assume
only that the candidate squares have pairwise disjoint vertex supports.
There is no restriction on the original M+N components meeting a square,
or on whether M meets either phase. M and T stay fixed throughout.

Use a directed MULTIGRAPH with tagged copies: each N edge is directed black
to white, and each actual M edge white to black. If an edge belongs to both,
keep the two opposite tagged copies. Its physical component is a two-vertex
directed cycle, rather than a deleted edge or a terminal path. Every P vertex
has indegree=outdegree=1; black Q vertices are sources and white Q vertices
are sinks. Components are terminal paths and P-only directed cycles.
Each terminal path owns its actual M edges. This convention includes retained
M intersect N edges among the free cycles.

Delete only the tagged N copies at all candidate cuts. If there are n terminal
paths and e squares, the starts of the open fragments are the n black Q
vertices and the 2e white cut endpoints. Every fragment ends at a white Q
vertex or a black cut endpoint. The remaining components are untouched
P-only cycles. To justify exhaustiveness, a directed walk from a start cannot
enter an uncut cycle: that would give its first entered vertex two predecessors.
Conversely tracing predecessors from any vertex not in an untouched cycle
reaches exactly one start. This partitions all remaining vertices into
n+2e fragments and the untouched cycles. It also partitions the actual M
edges, since deleting tagged N edges does not delete a tagged M copy.
Fragments may be singletons or have zero actual M edges.

Compress square g to a switch vertex. Its two black cut endpoints are distinct
incoming PORTS and its two white endpoints distinct outgoing PORTS. Index the
ports by the original N edges. Keeping the phase pairs equal indices; flipping
pairs opposite indices. These are exactly the two bijections of two ports.
A fragment is an arc between switches or terminals, with weight equal to its
number of actual M edges. Retain parallel arcs and self-loops as distinct
fragments. An arc can return to the same switch when both cuts belong to
one old component. A cut old cycle likewise produces switch-to-switch arcs.
No original-path identity is used to identify or merge ports.

A choice of local bijections partitions the fragments into terminal paths
and cycles. A terminal path cannot enter a cycle or another path: every
fragment has a unique predecessor and successor wherever these exist.
Since square supports are disjoint, all the chosen bijections simultaneously
realize an actual full auxiliary matching. Thus the compressed routing is
exact, including vertex ownership and actual M ownership, for every subset.

## 2. Coverage, cuts, and payment cost for all general pools

Let B_T be the number of black selected terminals. Give each fragment capacity
one; add a unit source arc to each black T and a unit sink arc from each white
H. Let F be the maximum integral source-sink flow. Then

    minimum residual TT = delta = B_T - F.                 (1)

Here and below TT/HH/TH refer to terminal endpoint types, not internal labels.
For any routing, the black-T/white-H paths form a feasible flow of value
B_T minus its TT count, proving the lower bound. Conversely mark the arcs
of an integral maximum flow. At a switch the two incoming bits and two
outgoing bits have the same sum, counting a self-loop once on EACH side.
Either the straight or crossed bijection preserves both bits. Decode these
local choices. Every marked source path reaches a white H; terminal paths
cannot get trapped in cycles. The decoded TT count is at most B_T-F, and the
lower bound proves equality. Marked cycles have no source and are harmless.
This argument also explains why a zero-cost fragment still has capacity one.
If the original counts were (a,b,t), the optimal counts are

    (delta, b-a+delta, t+2(a-delta)).                       (2)

For an exact terminal-free cut, retain the definitions a_iso, s_T(U), h_H(U)
from the earlier theorem. The word 'touched' still refers to original terminal
paths. Let out(U) count ALL directed fragments from a switch in U to a switch
outside U, including fragments of cut old cycles. Multiplicity is physical;
self-loops contribute zero. Then

    delta = a_iso + max_U [s_T(U)-h_H(U)-out(U)].            (3)

Indeed place black T and white T terminals on the source side and black H
and white H terminals on the sink side. This placement can normalize any
minimum cut without raising its capacity, by exchanging at most its one
fragment with its source/sink arc. For a switch-side set U the resulting
capacity is c0+B_touch-s_T(U)+h_H(U)+out(U), exactly as before. Untouched
terminal paths are counted by c0 and a_iso; cut old cycles only add their
outgoing fragments. Max-flow/min-cut gives (3). We do not assert the earlier
path-only contact-graph cycle-rank formula for this generalized adapter.

The exact joint-cost theorem also extends. Give every fragment R binary red
and blue variables r_R,b_R, with r_R+b_R<=1. Conserve each colour separately
at every switch. At black T set (red,blue)=(1,0); at white T set (0,1);
at black H permit blue only; at white H permit red only. When full coverage
is feasible, the minimum total TH actual-M cost among covering subsets equals

    min sum_R |M in R| (r_R+b_R).                           (4)

Proof: a physical covering routing colours its two types of TH paths and
leaves HH and cycles unused, giving a feasible point of identical cost.
Conversely the red/blue/unused multiplicities match on the two sides of each
switch; the elementary two-port multiset lemma gives a label-preserving
bijection. The decoded terminal paths have the required types. Coloured
cycles can be erased from their colour, leaving all conservation and terminal
constraints valid and never increasing the nonnegative objective. Thus both
optimum inequalities hold. The fragment partition makes all physical vertices
and M resources single-use. This is an exact binary model, not a claim about
its LP relaxation or a polynomial weighted solver.

## 3. The signed ledger must include OLD free cycles

For any auxiliary state i let U_i be the actual M edges on TH paths, B_i
those on TT OR HH paths, and C_i those on all P-only cycles, including
retained doubled components. Within each state these sets partition M:

    U_i disjoint-union B_i disjoint-union C_i = M.

Subtracting their cardinalities between two states gives the exact identity

    |U_1|-|U_0| = |B_0|-|B_1| + |C_0|-|C_1|.               (5)

There is no cross-state disjointness assertion: a resource may change class.
Even full T coverage may leave HH paths containing M, so B_1 cannot in
general be dropped. Retaining any already-free cycle as its M edges changes
its auxiliary representation, without creating another credit.

For a smallest feasible witness use a 2-by-2 board with

    M = { (0,0)--(1,0) },
    N = { (0,0)--(1,0), (0,1)--(1,1) }, T = {(0,1)}.

Initially the left edge is a retained free cycle; the right edge is TH.
There are no bad-path M edges and the payment costs zero. Flip N to the two
horizontal edges. Its unique TH path now owns the one actual M edge. Thus
cost changes 0 to 1, with B_0=B_1=empty, C_0 of size one and C_1 empty.
A bad-path-only increment formula fails even when all T remain covered.

After any general-pool routing all free cycles can be replaced by their
actual M edges. Vertex-disjointness of components gives a full auxiliary
matching with the same terminal paths, same payment set, and M intersect N
exactly equal to the free-cycle M. This is a representation normalization,
not a cost refund for an M edge already free before the operation.

## 4. Fixed 2-by-2 tiling: the exact regional criterion

Now let both board dimensions be even, tile by aligned 2-by-2 squares, and
restrict N to independent local perfect matchings inside these tiles. Include
EVERY tile in the candidate pool. All old N copies are cut. Every P fragment
is consequently just its tagged M edge, from the tile of its white endpoint
to the tile of its black endpoint. It is a self-loop if internal to one tile.
Every Q fragment is a singleton terminal. The resulting compressed directed
network is independent of the initial tile phases.

For a tile set U let R be its union of physical vertices, and let M_int(R)
mean actual M edges whose TWO endpoints are in R, including edges between
different tiles of U. Then

    delta_tile = max_U [ |T intersect R| + |M_int(R)| - 2|U| ].  (6)

The empty set makes this maximum nonnegative. To prove the formula from (1),
the normalized cut gives B_T minus cut capacity equal to

    T_black(R) - H_white(R) - M_white-out(R).

There are exactly 2|U| white vertices in R. Their partition gives
2|U|=P_white(R)+T_white(R)+H_white(R), and actual matching ownership gives
P_white(R)=|M_int(R)|+M_white-out(R). Substitution proves (6), with each
outgoing M edge cancelled exactly once. No selected independence assumption
or original-path hypothesis entered this calculation.

For tile v define t_v=|T in v|, i_v=|M wholly in v| and s_v=2-t_v-i_v.
The local feasibility argument below proves s_v>=0. If E(U) counts actual
M edges joining distinct tiles of U, counting EACH EDGE ONCE, (6) becomes

    delta_tile = max_U [ E(U) - sum_(v in U) s_v ].         (7)

Therefore full product-tile coverage holds exactly when every such regional
inequality E(U)<=sum s_v holds. If a region has positive excess, split its
induced actual-M tile multigraph into connected components. Its excess is
the sum of their excesses; at least one is positive. A residual obstruction
can thus be chosen M-connected. Section 8 gives an actual M-connected positive cut, so these fixed-tiling
inequalities do NOT always hold in feasible grids.

## 5. A uniform compensation flow with no repeated edge capacity

Let p_v=|P in v| and d_v=p_v-2i_v, the number of actual M edges leaving the
tile. Define the signed local reserve

    k_v = 4-2t_v-p_v = 2s_v-d_v.

Local feasibility gives k_v>=-1, and k_v=-1 exactly when t_v=2,p_v=1.
Call these debt tiles; they have diagonal T corners, no internal M, and
exactly one outgoing actual M edge. Let D(U) count debt tiles in U, let
K(U) sum max(k_v,0) there, and let boundary_M(U) count actual M edges with
one tile in U and the other outside. The incidence identity
sum_(v in U)d_v=2E(U)+boundary_M(U) proves

    2 delta_tile = max_U [D(U)-K(U)-boundary_M(U)].         (8)

This gives a single exact compensation problem across arbitrarily many
original components. Make the undirected actual-M tile multigraph, retaining
parallel physical edges and omitting intra-tile loops. Each debt tile supplies
one unit, each nondebt tile can absorb k_v units, and each actual cross-tile
M edge has capacity ONE. Let D be the total debt and F_D the maximum integral
flow from these supplies to these reserves. Then

    delta_tile = (D-F_D)/2.                               (9)

For rigor, model each undirected edge by two opposite unit arcs. Cancel all
oppositely directed flow on the same physical edge and delete circulations;
this preserves flow value and gives paths using each physical edge at most
once, in one direction. Each receiving tile absorbs at most its reserve.
Max-flow/min-cut says D-F_D is the maximum in (8): a cut U pays supplies
outside U, reserves inside U and exactly its physical boundary edges.
This proves (9), including the fact that the uncompensated supply is even.
The algebra in (8) proves this parity for every cut directly.

Thus ALL debts can be compensated if and only if the product-tile pool covers
ALL T. This is a complete counting/flow criterion, not a rule that independently
successful local transfers may be added. There is one supply per debt tile,
one receiving budget per reserve, and one capacity per physical cross-M edge.
It allows shared vertices subject to these budgets; nothing is counted twice.
To construct terminal payments, use (9) to establish the directed coverage
flow value and then decode that flow by Section 2. Debt-flow paths themselves
are not physical terminal paths, so their shared tiles do not grant extra
physical vertex capacity. The debt flow does not itself price the total payment
in (4). In particular cancelling opposite resource-flow directions is justified
in this compensation network, not an instruction to alter the fixed M.

One immediate sufficient subclass has no debt tiles: every regional excess is
nonpositive, hence delta_tile=0. More generally the exact obstruction is a
connected region with more debt than its reserve plus its M boundary capacity.
Section 8 gives an explicit actual positive closed region. Thus this exact
criterion also detects failure of the fixed-tiling strategy; a more flexible
pool must use contacts beyond the fixed tiling in those examples.

Here is the local argument, without finite-board inference. Three selected
corners in a square would give one of them two selected neighbours, so t<=2.
If t=0, p<=4 and i<=2. If t=1, its two adjacent corners contain at most one P,
so p<=2 and i<=1. If t=2 and the corners are adjacent, both remaining corners
are excluded from P; if diagonal, at most one remaining corner is P, and
no internal M is possible. Consequently t+i<=2. These cases also give
2t+p<=4 except for t=2,p=1, which has 2t+p=5. This proves all the claimed
local slack/reserve facts. The argument uses a tile's internal neighbours
only, so global feasibility supplies its hypotheses even at board boundaries.

## 6. Retain every intra-tile actual M edge

**Normalization theorem.** Every product-tile N has another product-tile N*
that retains every intra-tile actual M edge, has exactly the same terminal
endpoint pairings, and has a TH paid-M set contained in the old one.

Proof. A tile has zero, one, or two intra-tile M edges. With none, do nothing.
With one such edge e, if N already contains e do nothing. Otherwise its two
N edges together with e form a three-edge alternating detour joining the two
other tile vertices. Those two other vertices are the only remaining ports
to the exterior (or may themselves be terminals). Replace the local phase
by e and the complementary tile edge. The detour becomes the direct connection
of the SAME two ports, and e becomes an isolated retained doubled component.
This preserves every terminal pairing and removes e from a path payment if
it had belonged to one; a pre-existing free cycle merely loses a free edge.
With two intra-tile M edges all tile vertices are internally matched in M
and N, so there are no terminal/exterior ports. Set N equal to those M edges.
Independent tile operations prove the theorem. Edges already retained remain
retained because all operations are confined to their own tiles.

Since a product-tile N never has cross-tile edges, M intersect N* is exactly
the set of all intra-tile actual M edges. Only tiles with NO intra-tile M
need switching choices for optimal coverage or cost. Other free cycles may
remain. Normalizing every such cycle as in Section 3 may leave the product-
tile class; that additional operation is not needed for this theorem.

## 7. An all-size old-cycle relay barrier

For any even H>=2 take the (H+2)-by-6 board, rows 0,...,H+1 and columns 0,...,5.
The actual matching is

* the two top-row edges (0,1)--(0,2) and (0,3)--(0,4);
* for c in {2,3} and odd r=1,3,...,H-1, the edge (r,c)--(r+1,c).

Thus |M|=H+2. Take T={(0,0),(0,5)}. Define N by

* horizontal column pairs (0,1),(2,3),(4,5) in rows 0 and H+1;
* the horizontal c=2--3 edges in rows 1 and H;
* vertical edges in columns 2,3 at even r=2,4,...,H-2;
* vertical edges in columns 0,1,4,5 at odd r=1,3,...,H-1.

Each listed edge uses adjacent row/column indices. These disjoint clauses
cover every vertex once; the empty middle clause at H=2 is allowed. Both
selected vertices have their top horizontal neighbour in P and their lower
neighbour in H, so feasibility holds. Initially M intersect N is empty.
The top row is one TT path with exactly two actual M edges. The middle
columns form one genuine P-only alternating cycle with exactly H actual
M edges. Every other component is an N-only HH edge, with total counts

    (TT,HH,TH) = (1, 2H+3, 0).

Prescribe two disjoint squares with upper-left corners (0,2) and (H,2).
The first cuts the middle top-row N edge and the TOP cycle N edge; all four
vertices are occupied P. The second cuts the BOTTOM cycle N edge and the
bottom-row middle HH N edge. For H=2 the two supports are still disjoint.
No original alternating square connects TT directly to HH anywhere: all
three old N edges of TT are horizontal in row zero; of the three possible
squares immediately below them, only the central one has a parallel N edge
below, and that edge belongs to the old P-only cycle. A horizontal N edge
cannot be the vertical phase of another candidate square.

Neither singleton switch repairs TT. The upper switch absorbs the whole
cycle into TT, leaving one TT. The lower switch absorbs the whole cycle into
HH, leaving the old TT unchanged. Switching BOTH cuts the old cycle at its
top and bottom and opens its two vertical columns into the two TH paths.
Each contains H/2 cycle M edges plus one original top-row M edge. Therefore
this is the UNIQUE covering subset of the prescribed pool and its cost is

    (TT,HH,TH) = (0,2H+2,2),   payment M = H+2.             (10)

There is no remaining P-only cycle. This also proves the exact binary-model
optimum in (4) for this pool. The original bad M count is fixed at TWO, but
the covering cost H+2 is unbounded. For every natural-number budget multiplier K choose
H=2(K+1); then the payment exceeds K times the old bad M. For real K>=0,
choose H=2(ceil(K)+1), giving the same strict comparison. This refutes every
uniform expense budget based only on original bad-path M for general pools
that can absorb old cycles. Equation (5) correctly charges 2+H.

It is a rule counterexample, not a numerical target counterexample: the two
selected vertices each have their distinct lower H neighbour, giving an
unrestricted zero-M payment outside the prescribed pool. Also
|M|+|T|=H+4, while half the area is 3H+6 and the margin is 2H+2.

## 8. A genuine closed tile-cut obstruction for every even width

The [existing unique-matching family](UNIQUE_MATCHING_HOLE_COMPENSATION_BARRIER.md) gives a
particularly useful NEW consequence: the optimal residual TT count for ALL
product-tile phases is exactly ONE, at every even width w>=6. The physical
M,T construction and its direct-hole certificate are prior results; this
all-phase characterization and its debt-flow explanation are the deduction here.

For completeness set w=2n with n>=3 and take a 4-by-w board. Let P contain
rows 0,1 in columns 1,...,w-2 and the two vertices (2,1),(2,w-2). M consists of

* vertical edges (1,1)--(2,1) and (1,w-2)--(2,w-2);
* top-row edges (0,c)--(0,c+1) for odd c=1,3,...,w-3;
* row-one edges (1,c)--(1,c+1) for even c=2,4,...,w-4.

Take T to be the six vertices (0,0),(0,w-1),(2,0),(2,w-1),(3,1),(3,w-2),
together with (2,c) for odd 3<=c<w-3 and (3,c) for even 4<=c<w-2.
The existing note proves feasibility, unique matching of this P footprint,
and the sharp fixed-P maximum |T|=w. The displayed construction also gives
these facts directly: the four upper/side selected vertices each see one
P neighbour; the two lower special vertices each see their one P neighbour
above; the interior row-two choices each see their one P neighbour above,
and the interior row-three choices see no P. Neither interior class meets
another T. The interval endpoints leave the two transitions to the special
choices blank.
The M clauses are disjoint and cover exactly P, with |M|=w-1.

Use tile coordinates (row-pair,column-pair). The non-isolated actual-M tile
component is the simple path

    (1,0), (0,0), (0,1), ..., (0,n-1), (1,n-1).

The top-row M edges join successive upper tiles, and the two vertical M edges
join the path ends to the two lower tiles. The row-one M edges are intra-tile
loops and do not change connectivity. Each upper endpoint tile has (t,p)=(1,2),
each other upper tile (0,4), and each lower end tile (2,1). Thus all upper
tiles have k=0, the lower ends are the only two debts, and no ordinary reserve
is reachable from either debt. All other tiles have p=0 and k>=0 but are
isolated in the actual-M tile graph. Consequently D=2, F_D=0, so (9) proves

    min residual TT over every product-tile phase = 1.     (11)

The same certificate is visible in (6): let U be all n upper tiles and the
two lower end tiles. It is M-connected, has no outgoing M edge, includes
all w-1 actual M edges and exactly six T, and has n+2 tiles. Its excess is
6+(w-1)-2(n+2)=1. No larger cut can occur by the exact debt-flow calculation.
The optimal full terminal counts are (1,2,w-2), using J=2w-1 and (2).

There are nevertheless disjoint ZERO-M adjacent-hole payments for every T:
map (0,0),(0,w-1) downward; map (2,0),(2,w-1) downward; map (3,1) to (3,2)
and (3,w-2) to (3,w-3); map the remaining lower T vertically to the other
row of its own column. These holes are distinct, outside P and outside T.
These direct payments extend to a FULL auxiliary matching, not merely a
partial collection of terminal edges. Include all the displayed T--H payment
edges, retain all top-row and side-vertical actual M edges, add the two
vertical edges (2,2)--(1,2) and (2,w-3)--(1,w-3), and pair the remaining
row-one vertices by (1,c)--(1,c+1) for odd c=3,5,...,w-5. The payment edges
cover Q except the two holes (2,2),(2,w-3); the retained edges cover P except
the row-one interval c=2,...,w-3; the last clauses match that interval plus
the two holes. These disjoint sets cover every vertex, including at w=6.
This N has counts (0,1,w), with all TH paths single N edges and zero paid M.

Thus (11) refutes universal fixed-product-tiling coverage and every attempted
claim that actual rectangular feasibility automatically makes all regional
cuts pass. It does not refute coverage with unrestricted auxiliary matchings,
or the numerical coefficient-one target: J=area/2-1. It also makes precise
what a next pool must change: a successful pool must go outside these fixed
tile switches, possibly by choosing a different initial N.

## 9. Stronger: every single independent batch from horizontal N fails

The same existing physical family gives a stronger obstruction than (11).
Let N_0 pair every row horizontally in column pairs (0,1),(2,3),...,(w-2,w-1).
For EVERY pool of vertex-disjoint N_0-alternating squares, no subset covers all
T. Its optimal residual TT count is exactly ONE. Thus simply selecting a
more flexible independent pool at this baseline cannot repair the example.

We prove a stronger statement encompassing all such batches: for ANY full
auxiliary N with no edge between distinct four-row, two-column strips

    S_j = {0,1,2,3} x {2j,2j+1},  j=0,...,n-1,

there is a TT component. Each strip may use ANY of its five full domino
matchings, independently; there is no product-tile restriction within a strip.

Proof. The only actual M edges between strips are the top-row edges joining
successive strips. Every interior strip S_j, 1<=j<=n-2, has its two top
vertices in P and the actual M edge joining its two ROW-ONE vertices. Since
N cannot leave the strip and there is no row above zero, the two top vertices
are either N-matched to each other or both N-matched downward. In the former
case a single N edge joins the two top ports; in the latter the sequence
N--M(row one)--N joins the same two ports. Hence in EVERY local domino phase
the two external actual-M ports continue into each other. This argument does
not depend on the bottom-half labels or matching phase.

At the left strip the external actual-M port is the top vertex (0,1). If
its top pair is horizontal in N, it is joined to selected (0,0). Otherwise
both top N edges are vertical. Trace from (0,1) down to occupied (1,1), along
actual M to (2,1), and then along its N edge. It cannot return to (1,1), whose
N mate is already (0,1); it cannot leave the strip. Its only remaining N
neighbours are (2,0) and (3,1), BOTH selected. Thus this end port always
terminates at a T. The right strip is the mirror argument, ending at one of
(0,w-1),(2,w-1),(3,w-2). Concatenating through all the interior strips gives
one actual TT path, with no alternative outgoing branch. Therefore every
such N has at least one TT component. N_0 itself has counts (1,2,w-2): the
top row is TT, its two side detours are TH, the middle row-one actual edges
are retained, and the lower unmatched pairs give exactly two HH. Thus the
minimum over ALL 5^n strip-confined auxiliary matchings is one.

Every N_0-alternating square must have upper-left column 2j: its old edges
are horizontal because N_0 has no vertical edge, and N_0 has no odd-starting
horizontal edge. Its upper-left row is 0,1 or 2. Switching any independent
pool of these squares never creates an N edge between strips. This proves
the asserted obstruction for EVERY possible pool, not just a selected pool.
The empty subset retains N_0, so the best residual for every pool is one.

The complete maximal-pool catalogue also gives a small control: within each
strip either choose both row-zero and row-two squares, or choose the row-one
square. Any other independent pool extends to one of these; strips have
disjoint vertex sets. This validates the all-pool claim without enumerating
all switch subsets in the control, since the accepted coverage flow computes
the optimum for each maximal pool.

The unrestricted full N in Section 8 succeeds and necessarily crosses at
least one of these strip boundaries. This is a fixed-baseline, one-independent-
batch obstruction, not a failure of the general port theorem, which exactly
reports its shortage. To repair it one must change the auxiliary baseline or
allow successive batches with overlapping supports. Section 10 supplies an
explicit optimal two-batch construction for this entire family. A universal pool-selection
argument cannot start from this N_0 and merely search harder among independent
squares. The numerical target remains untouched.

## 10. Exactly TWO batches suffice, with zero final payment cost

For this family the minimum number of successive independent-square batches
needed to cover all T from N_0 is exactly TWO. The lower bound is Section 9;
the following explicit construction proves the upper bound for every even
w>=6, keeping the actual M,T fixed.

1. Flip all squares with upper-left corners (r,c), r in {0,2} and even
   c=0,2,...,w-2. These w squares partition the board. Starting from N_0,
   they produce the full vertical matching N_1 on row pairs (0,1),(2,3).
2. In N_1 flip all squares with r in {0,2} and odd c=1,3,...,w-3. These
   w-2 squares are pairwise vertex-disjoint and now have the required
   vertical old N edges. They produce horizontal pairs (c,c+1) at every
   odd c=1,3,...,w-3 in EVERY row, with vertical edges retained only in
   the two boundary columns 0,w-1. Call this full matching N_2.

The two batches overlap EACH OTHER; each batch separately has disjoint
supports. Applying both at once is not an allowed operation and is not claimed.
Every T is N_2-matched directly to a distinct H: the four selected left/right
vertices in rows zero and two go down; the two special row-three T go inward;
the remaining odd-column row-two T go right; the remaining even-column
row-three T go left. The explicit T ranges in Section 8 show that each target
is a hole. Matching disjointness gives their uniqueness. Therefore all T are
covered with zero actual-M payment, and the counts are (0,1,w).

The intermediate state has not yet repaired the shortage: it still has
(1,2,w-2). The TT endpoints have moved to the two special row-three T, and
that TT now owns ALL actual M edges. This construction is not a monotone
preservation theorem for each previously paid selected vertex. It is a valid
sequence of auxiliary changes at fixed feasible actual M,T, ending in a full
cover. Neither changing the selection nor changing the actual matching is
needed.

The entire actual-resource ledger is explicit. With n=w/2, let M_top be the
n-1 top-row edges, M_mid the n-2 row-one edges, and M_side the two side edges.
These are disjoint actual M sets, so all resource transitions are literal:

| Auxiliary state | TH paid M | TT/HH bad M | P-only free M |
| --- | --- | --- | --- |
| N_0 | M_side (2) | M_top (n-1) | M_mid (n-2) |
| N_1 | empty | all M (2n-1) | empty |
| N_2 | empty | M_mid union M_side (n) | M_top (n-1) |

The signed cost increments in (5) are -2 and 0, for total -2. In particular
the final n-1 free edges do not provide a credit to be added on top of the
old n-2 free edges: the latter were absorbed and end in HH. No credit is
booked per individual flip. The final partition, or the signed telescoping
identity, counts each physical edge once. This supplies both a sharp obstacle
to a one-batch strategy and a complete all-size repair with depth exactly two.
It does not prove that two batches suffice for arbitrary grid configurations.

## 11. Evidence and the remaining scope

The [physical checker](../develop/check_general_square_ports.py) independently
walks actual terminal paths and all P-only cycles, compares their full vertex
and M sets to routed fragments, checks (5), and normalizes all free cycles.
It exhausts actual matchings, feasible T, perfect N, disjoint candidate pools
and their switch subsets on 2-by-2 and 2-by-4. It also checks randomly generated
larger physical models, every regional cut in the product-tile controls, an
independent undirected debt flow, all product-tile phases for intra-tile
retention, the complete local four-corner classification and forty even H
values of (10), fifty widths of (11), and every product phase at widths
6,8,10 for the closed-cut family. These are discovery/verification controls;
Sections 1--10 are the arbitrary-size proofs. Complete products of all five
strip domino states at widths 6,8,10 give 3,875 actual auxiliaries; 504 maximal
independent pools at widths 6,...,16 each have exact residual TT one. Fifty
widths also check both batches, intermediate/final actual component sets and
the complete signed resource ledger, including payment costs 2 -> 0 -> 0. The old network's residual self-loop indices
are corrected; its original checker is rerun as a regression.

The scoped Lean source proves the signed partition arithmetic, regional
white-vertex cancellation, incidence/debt identities, local tile arithmetic
and quantified unbounded old-cycle expense. Physical extraction, global
flow/min-cut, physical tile normalization and coordinate embeddings remain
written; they are not end-to-end Lean theorems. Execution and independent
review receipts give the precise scope and are linked from the README.

The original coefficient ledger is still

    area/2 - [|T|+(1-eta)|M|] = b_opt+eta|M|-delta.

Because b_opt=b-a+delta, delta-b_opt=a-b is invariant at fixed M,T. Better
coverage alone does not improve a numerical coefficient. The present exact
compensation criterion and the actual closed positive cuts isolate the next
issue: choose auxiliary baselines that can reach the otherwise disconnected
reserve, or construct controlled successive overlapping batches, retaining the general
physical ownership/cost ledger. Another possible direction is to characterize
which changed baselines repair this family. Both the fixed-tiling and arbitrary
independent-pool claims at N_0 are disproved, not left open; universal geometric coverage and numerical
coefficient improvement still require additional arguments.
