# Physical strip compensation: exact costs, tree messages and feedback rank

The [macrocell obstruction](CAPACITY_PRESERVING_MACROCELL_OBSTRUCTION.md)
shows that scalar compensation can pass every capacity check and still fail
to lift. Here the local lift is made constructive for arbitrary two-column
rectangular cells. It yields an exact weighted physical model, a linear-time
forest algorithm, and an O(3^k |V|) algorithm at cross-cell cycle rank k.
A separate all-width deduction gives a sharp cost/depth tradeoff: moving
one old selected vertex makes one-batch coverage possible, but its minimum
M cost is w/2, while two batches still cost zero.

Tree dynamic programming, feedback conditioning, and finite-state strip
transfer are classical methods. The content here is their exact physical
adapter with the actual matching fixed, the cycle-cost normalization needed
for equality, and their application to the specified grid families. No
universal numerical 5/6 improvement or universal constant batch depth is proved.

## 1. Physical hypotheses and allowed cells

Let G be a finite rectangular grid, black at even coordinate sum. M is a
fixed actual partial matching, P its endpoints, Q=V\P, T a subset of Q,
and H=Q\T. In the sub-quorum application every t in T has at most one
neighbour in P union T; the algorithmic equivalences below do not need this
extra feasibility hypothesis. Each actual edge e has nonnegative weight w_e;
unit weights give the number of actual M edges paid on TH paths.

Partition the board into axis-aligned rectangles of width TWO and arbitrary
positive height. Each has equally many black and white vertices. N must be
a full physical auxiliary matching with every edge inside its cell. This
is a restriction on N, not on M, which may cross cell boundaries and have
internal edges of either orientation. M,N shared edges retain two tagged
copies and are free P-only doubled cycles. TT/HH/TH always refer to terminal
types; the objective is the sum of actual-edge weights on ALL TH paths.

Make the actual-M cell MULTIGRAPH: one vertex per cell, one edge per
cross-cell actual M edge. Internal M edges stay inside the local problem.
Parallel physical edges are distinct and contribute to cycle rank. Let

    k = E_cross - number_of_cells + number_of_components.

This is nonnegative. A forest has k=0, so in particular no parallel edges.
The implementation uses a uniform row-block height, with a possible shorter
last block; the proof applies to any partition into the stated cells.

## 2. An exact strip language, for any finite number of colours

Colour every vertex of an h-by-2 cell with one of q colours. Write its row
word as (a_0,b_0),...,(a_(h-1),b_(h-1)). A row is monochromatic if a=b and
mixed otherwise. A mixed run is a maximal consecutive sequence of one
fixed ordered unequal pair (a,b).

**Strip lifting theorem.** A same-colour physical perfect matching exists
if and only if every mixed run has EVEN length. Equivalently the word can
be parsed into single monochromatic rows and pairs of identical mixed rows.

Proof by removing the first row. If it is mixed it cannot use the horizontal
rung, so both vertices must match downward. The next row must have exactly
the same ordered colours; delete these two rows and repeat. If the first row
is monochromatic, an existing matching either uses its rung or uses two
vertical edges to an identical monochromatic second row. In the latter case
replace these by the two horizontal rungs and delete just the first row.
This preserves colour legality and full matchingness, though no invariance
of actual-M payment under this local replacement is asserted. Induction
proves necessity and constructs a matching for every valid parsing.

The parsing into mono singletons and mixed pairs is unique. Therefore if
A_h(q) counts liftable colour assignments, then

    A_0(q)=1, A_1(q)=q,
    A_h(q)=q A_(h-1)(q)+q(q-1) A_(h-2)(q).               (1)

At q=2,h=4 this gives 44, explaining the earlier 44 liftable patterns among
70 colour-balanced assignments. At q=3,h=4 it gives 279 out of 3^8 total
assignments. Equation (1) counts assignments, not physical matchings: several
physical matchings may share one colour word.

A recognizer has one empty state and q(q-1) pending mixed-pair states.
From empty, a monochromatic row stays empty; a mixed row enters its pending
state. A pending state accepts only its identical row and returns to empty.
Start and finish empty. This is a finite-state replacement for the two-colour
local Hall test on these cells, and also handles red/blue/unused labels.

## 3. Exact weighted three-colour model, including free cycles

Use labels 0 (unused), R (red), B (blue). Impose:

| Vertex type | Allowed labels |
| --- | --- |
| black T | R |
| white T | B |
| black H | 0 or B |
| white H | 0 or R |
| P | 0, R or B |

Both endpoints of each actual M edge must have the same label. In every
cell the row word must satisfy the strip lifting theorem. Minimize

    L = sum_(e in M) w_e * [label(e) is R or B].          (2)

**Exact-cost theorem.** A feasible labeling exists exactly when some allowed
physical N covers all T. If so, min L equals the minimum actual TH cost in
this cell class, not merely a relaxation or an upper estimate.

Proof. Given a physical covering N, label its black-T/white-H paths R, its
black-H/white-T paths B, and all HH paths and P-only cycles 0. Every M and N
edge preserves its label. The cell words are liftable and (2) is exactly the
actual TH cost, giving min L <= optimum physical cost.

Conversely decode a feasible word in each cell to a physical N. Each terminal
path preserves its label on both M and N. Red paths can only have black T
and white H endpoints; blue paths only black H and white T. Every selected
vertex therefore belongs to a TH path. Zero paths are HH. Equation (2)
charges every TH edge and possibly some coloured P-only cycles, so physical
cost <= L. Recolour each complete coloured cycle 0, keeping its N and M;
this remains feasible and never increases L. Thus a minimizing labeling has
no positive-weight coloured cycle and both optimum inequalities give equality.
Zero-weight coloured cycles may remain and can also be recoloured 0.

All resources are actual M edges; there is no credit per row or per cell.
The complete old/new signed partition ledger from the earlier note applies
to comparisons between resulting N states. Nonnegativity is essential for
the cycle argument. The canonical strip parsing need not preserve a previous
terminal pairing or a previously chosen payment set, and no such claim is made.

## 4. Linear exact solution on the actual-M cell forest

Root every component of the cell multigraph, assuming k=0. For a nonroot
cell C let e be its unique parent edge. Send a message m_C(c), c in {0,R,B}:
the minimum (2) in C's subtree conditional on e's label being c, with the
weight w_e[c!=0] included ONCE in this child message. An impossible conditional
problem has value infinity. Internal edges are charged once at one endpoint
inside their own cell; child messages are unary costs at the respective
actual-M endpoints in the parent cell.

Given these unary costs, solve a cell exactly by a row transfer. Choose each
row's ordered label pair, at most nine choices. Retain the previous row's
labels and whether both N vertical edges are pending from that previous row.
There are at most 18 states after a row:

* If N is pending, the new row must repeat the previous labels; insert its
  two vertical N edges and clear pending.
* Otherwise use a horizontal N rung if its two labels agree, or start two
  vertical N edges to the next row. End with pending clear.

Independently require equal labels on any internal horizontal M edge, and
on each internal vertical M edge between the previous and current rows.
This explains why the previous pair must remain in state even when N has
no pending edge: the strip recognizer alone would forget an M constraint.
Apply terminal restrictions and a possible parent-endpoint label pin. Add
the two vertex unary costs and the weight of each internally owned M edge.
The transfer enumerates exactly the same-colour physical domino matchings
and all labelings, including monochromatic vertical choices; it is not a
projection to scalar reserves. Store predecessors to reconstruct labels/N.

Inductively child subtrees interact only through their respective ONE
physical parent-edge colour, since the remaining graph is a forest and N
does not cross cells. Conditional optima therefore add exactly. Minimizing
the root local values and summing disconnected components proves optimality.
Backtracking returns an actual full N. Section 3 removes coloured cycles at
the global optimum, proving that the returned minimum is actual TH expense.

The number of colours and transfer states is fixed. Precompute each endpoint's
three unary costs, process each cell at most three times (one per parent colour),
and traverse each actual edge once. This is O(|V|) arithmetic operations and
O(|V|) storage, not an enumeration of the Fibonacci-many local tilings.
All finite costs remain arbitrary-size integers. Impossible unary/message values
use a separate symbolic value (None), never floating-point infinity; an option
with an impossible chosen unary is rejected before finite costs are added.
Integer arithmetic has the bit length of the total weights. The final component
extraction scans Q once for terminal starts and V once for cycle starts,
marking each vertex on entry. Each N edge and actual M edge is traversed
once, including shared edges as tagged doubled cycles. Thus the diagnostic
wrapper and backtracking also obey the linear operation bound; they do not
repeatedly choose a minimum unseen vertex or rebuild a growing path set. This is a
weighted algorithm for the stated forest class, not a claim that arbitrary
cell graphs or unrestricted grids have a polynomial weighted solver.

## 5. Exact cycle-rank extension; defer cycle normalization

Choose a spanning forest of the physical cell MULTIGRAPH, leaving precisely
k feedback edges. Enumerate the 3^k assignments of 0,R,B to these edges.
For each assignment remove feedback edges ONLY from the message graph:
their actual endpoints remain P, both endpoints are pinned to the assigned
colour, and each edge incurs w_e[c!=0] once outside the tree messages.
Solve the resulting constrained forest problem as above. Take the least
labeling objective over all assignments.

Every global feasible labeling restricts to exactly one feedback assignment,
and every solved branch is a global feasible labeling. This partitions the
labeling problem without losing any physical edge or multiplying its fee.
It proves exactness and O(3^k |V|) arithmetic complexity. Parallel actual
edges contribute to k, rather than being silently merged. Each branch is
a physical matching problem; it is not the coarse complete-port relaxation.

**Cycle normalization must wait until the global minimum.** A fixed feedback
colour can force a red P-only cycle. Recolouring that cycle 0 changes the
feedback assignment, so its branch's minimum L can exceed its actual TH
expense. One must compare the branch LABEL objectives, and then invoke
Section 3 at the unrestricted global minimum. A concrete two-cell control
has two parallel actual M edges and a forced red 4-cycle: that branch has
L=2 and actual TH cost zero, while the global all-unused branch has L=0.
Treating the branch's coloured cycle as a local refund would not preserve
the constraints under which the message was computed.

## 6. A sharp all-width tradeoff after one selected-vertex relocation

Take the earlier unique-matching 4-by-w family, w=2n>=6, with the same M.
Replace selected (3,w-2) by (3,w-3), leaving all other T unchanged. The
feasibility of this single relocation is an earlier result. Directly, the
new T has no occupied neighbour, and only possibly selected (3,w-4) next to
it; that neighbour has no occupied neighbour and no other selected neighbour.
At w=6 it is a singleton. Thus the selected-degree condition still holds.

The old selection had no covering N confined to the 4-by-2 column cells.
For the relocated selection the exact minimum is instead

    minimum cell-confined TH cost = n = w/2.             (3)

Lower bound. Every interior cell still joins its two top M ports, either
directly by N or through its internal row-one M edge. The left end port
still terminates at a T by the earlier forced-end argument. A covering N
must make the right end terminate at H. The right port cannot use its top
horizontal N edge, since (0,w-1) remains selected. It must go down through
(1,w-2), use the actual side edge to (2,w-2), and then reach H=(3,w-2).
The other available terminal neighbour (2,w-1) is still selected. Hence
this TH path contains all n-1 distinct top-row actual edges and the right
side actual edge, giving the lower bound n. Internal detours can only add
nonnegative edges. This is a physical all-N lower bound, not inferred from
the tree solver or from enumeration.

For equality choose the following local phases:

* Left cell: horizontal rungs in rows 0 and 3, and both vertical edges
  between rows 1 and 2. This is the fifth 4-by-2 domino phase and RETAINS
  the left side actual M edge as a free doubled component.
* Every interior cell: horizontal rungs in rows 0 and 1, and both vertical
  edges between rows 2 and 3. Its row-one M is retained free.
* Right cell: vertical edges on row pairs (0,1) and (2,3).

The forced top chain runs from left selected (0,0) to new hole (3,w-2).
Its actual paid set is exactly top M union {right side M}, of size n.
Every other T is directly N-matched to H: the left lower selections use
the retained-edge phase's other middle vertical edge and bottom rung;
interior selections use vertical lower pairs; the two right selections use
the rightmost column's vertical pairs. These clauses remain valid at w=6.
All other actual edges are retained free, and no bad-path M remains. This
proves (3) with literal resource sets.
More generally, for any nonnegative actual-edge weights, the exact minimum
is the sum of the weights of the top-row M edges and the right side M edge:
the lower bound forces that whole set onto one TH path, and the displayed
matching pays exactly that set and nothing else.

Every physical domino matching in a 4-by-2 cell can be reached from its
all-horizontal baseline in one independent batch: flip neither square,
just the top square, just the bottom, top and bottom, or just the middle.
These are all five ladder tilings (three possible first vertical-pair positions,
the disjoint top/bottom pair, or no vertical pair). Different cells have
disjoint supports. Conversely every one-batch square from horizontal N
stays inside one such cell. Therefore (3) is also the exact minimum cost
among all successful SINGLE independent batches from horizontal N_0.

The same two-batch final matching N_2 as in the earlier note still costs
ZERO: the moved T merely swaps T and H on one of N_2's direct TH edges.
All other selected pairings persist. Thus

    one batch: feasible, exact minimum M fee w/2;
    two batches: feasible, exact minimum M fee 0.          (4)

For this relocated selection the minimum coverage depth is one, while the
minimum zero-fee depth is two, under UNIT fees. With arbitrary nonnegative
weights, the minimum zero-weight-fee depth is one exactly when the forced
set has total weight zero, and two otherwise. The gap in expense is unbounded, without any
change to actual M. In particular the left middle vertical phase matters:
ignoring that fifth phase would incorrectly charge the left side edge too.

## 7. A second positive family with arbitrarily long optimal relay cost

The earlier [isolated-hole family](UNBOUNDED_ISOLATED_HOLE_RELAY_COST.md) has
side length 4k+2, one central hole h=(2k,2k), actual M as specified there,
and every odd Q vertex selected. Its general distance argument already
proves cost at least k under every rematching, and a vertical payment attains
k. A new completion attaining k lies in the full-height two-column cell class:

Use horizontal N pairs in every row except the LAST two-column cell. In that
last cell use vertical N at the same row pairs as its actual occupied column,
and horizontal N rungs in rows 2k and 4k+1. The two special rungs join its
remaining middle and bottom vertices, so this is a full cell-confined N.

The central row gives the path from h to selected (2k,4k+1), alternating N
even-starting pairs with the k odd-starting actual M edges in columns
2k+1,...,4k. Every other T uses a direct N edge on the outer L. Thus its
paid set is exactly those k central-row actual edges. The cell multigraph
consists of a path of these edges and isolated cells; the forest algorithm
therefore applies and its exact answer is k. The base family and distance
lower bound are credited; the horizontal full completion and its placement
in the tractable physical class are the deduction here.

## 8. Evidence and remaining scope

The companion implementation reconstructs a full physical N, checks actual
terminal/cycle components, and prices unique actual M sets. Independent
enumerations compare all cell-confined N on small actual matching/feasible-T
models, including nonunit and zero weights, parallel edges and cyclic cell
graphs. Colour-word enumeration checks the local language against actual
domino matchings. The current checker passes 2,192 weighted actual models
with 9,864 full-auxiliary evaluations, 100 further models (cycle rank up to
two in those random controls), 12,842 colour profiles, 50 relocated widths
and 16 isolated-hole parameters. The fixed-red-cycle branch is checked
separately. Five scoped Lean declarations pass locally for arbitrary alphabet
and word length; two are axiom-free and the others use only standard Lean
axioms. The geometric extraction of the rung/vertical grammar is written.
All-width proofs of (1)--(4), the message induction and
feedback partition above provide generality; finite controls do not replace
them. Scoped Lean statements concern the word grammar, its normalization, and
its recognizer, not resource arithmetic or global coordinate/flow/algorithm
adapters.

The next open issue is a geometric guarantee or resource estimate for the
full mixed/occupied-band problem. These exact models can certify or exclude
proposed physical compensations and price them without repeated credit;
they do not prove every feasible board has a covering N in a chosen strip
class. In particular the old closed-chain selection remains infeasible even
though its scalar coarse flow passes, and fixed-M coverage improvements do
not change the numerical invariant delta-b_opt=a-b.

The [initial independent review](reviews/2026-10-27-strip-tree-initial-review.txt)
accepted the written arguments and reproduced the submitted checker JSON
byte for byte, but returned REVISE for large-integer arithmetic and quadratic
component-checking overhead in the implementation. Both issues are corrected
in this revision and covered by large-integer and exact traversal-count
controls, in addition to differential checks against the older decomposition.
A follow-up verdict is recorded separately; initial mathematical acceptance
does not count as acceptance of the corrected implementation.
