# Exact PP-path accounting and a backward connector obstruction

22 October 2026. Authors: Haobo Ma and Wenlin Zhang.

The actual matching canonically groups arbitrary PP chains into objects with
one exact terminal debit. This removes any dependence on a chain's length or
number of bends from the accounting, including when matching edges leave the
region. It also exposes an obstacle to extending native transverse cancellation:
a fully frozen, uniquely matched family has a terminal connection directed
backwards in column order and changing column parity. The native increasing
interval-path proof therefore does not extend merely by replacing a matching
edge with an arbitrary PP path. This is a rule obstruction, not a counterexample
to the packet inequality or the grid conjecture.

## 1. Actual matching, PP contraction and exterior stubs

Let (T,M) be any feasible configuration, with P the actual matching endpoints.
Selections and endpoints are disjoint and every selection has at most one
neighbor in T union P. Partition a finite region J into disjoint two-cell columns.
For the geometric corollary these are the columns of k aligned adjacent
two-row bands of length n. The contraction identity itself requires neither
alignment, boundary conditions, nor freezing.

Give each column containing P one multigraph vertex. Its type is TP, BP or PP,
according to its other corner. Include each actual matching edge that meets J.
An edge wholly inside J joins the column vertices containing its endpoints;
an edge inside one PP column is a loop. For every edge leaving J introduce
a separate degree-one exterior vertex X. Preserve edge multiplicity, and count
a loop twice toward degree. Distinct exterior edges have distinct X vertices,
even if their exterior endpoints happen to lie in one column outside J.

Each TP/BP vertex has degree one. Each PP vertex has degree two, because its
two endpoints each have exactly one actual mate. Each X vertex has degree one.
Consequently every component is a path between two degree-one terminals or
a cycle consisting entirely of PP vertices. This includes a one-vertex loop
and a two-vertex cycle with parallel edges. To justify the classification,
start at a degree-one vertex and continue along the unique unused incidence.
A repeated vertex before termination would create a cycle with an entering
third incidence, impossible at degree at most two. Thus the walk ends at a
second degree-one vertex and exhausts its component. Components without
degree-one vertices are finite connected degree-two multigraphs, hence cycles.

Equivalently add a temporary vertical pairing of the two endpoints in every
PP column. Components alternate between actual matching edges and these
auxiliary pairs; the latter are for accounting only. A terminal path with p
PP columns has exactly p+1 matching edges. Every original endpoint in J,
every PP auxiliary pair and every actual matching edge meeting J belongs to
one component. Auxiliary pairs are not extra matching or donor resources.

## 2. Exact all-size ledger, including unmatched exterior terminals

Write A,B,C,D,E,F_pp for the numbers of TT, BB, TP, BP, BT and PP columns.
Define the weighted regional surplus and the blank/double balance by

    S_J = |J|/2 - |T intersect J| - |P intersect J|/2,
    L = B-A.

Since the column contributions are respectively -1,+1,-1/2,+1/2,0,0,

    2 S_J = 2L + D-C.                                   (1)

Count the disjoint terminal paths as follows:

    alpha: TP--TP; beta: BP--BP; gamma: TP--BP;
    tau: TP--X; delta: BP--X; epsilon: X--X.

The terminal inventory is exactly

    C = 2alpha + gamma + tau,
    D = 2beta + gamma + delta,
    number of matching cuts = 2epsilon + tau + delta.

Substituting into (1) proves the general identity

    2 S_J = 2(L + beta - alpha) + delta - tau.            (2)

No path length or cycle count occurs in (2). A TP--TP path carries one unit
of debit, a BP--BP path one unit of credit, and a mixed TP--BP path zero.
TP--X and BP--X paths carry a half-unit debit/credit; an X--X path carries
zero, even when both its matching cuts meet PP columns. Thus a rule charging
every boundary cut half a unit can overcharge the same actual path: two cuts
on an X--X path have no terminal debit at all.

For a matching-closed J, all exterior terms vanish and

    S_J = L + beta - alpha.                              (3)

These statements hold for every actual matching separately, whether unique
or not. Different matchings may change the component partition, but D-C and
therefore the signed expression in (2) cannot change for fixed T,P,J.

## 3. Boundary budget and the precise remaining inequality

Now let J be k aligned two-row bands, each with a first BB column and a final
column having a blank corner. In each band join consecutive BB/TT columns
when at least one is TT. Feasibility forces both neighboring columns of each
TT to be BB; the endpoint conditions exclude boundary TT columns. This is a
forest of odd alternating BB,TT,...,BB intervals, with B_i-A_i components.
Thus L is its total number of components. Each band contributes at least one.
If n is even and a band's last column is BB, it contributes at least two:
one alternating interval cannot contain both boundary columns of an even
length band. Let t count such sealed bands when n is even, and put t=0 for
odd n. Therefore L>=k+t.

The desired packet bound S_J>=k+t is, by (2), EQUIVALENT to

    2alpha + tau <= 2(L-k-t+beta) + delta.               (4)

For a matching-closed packet this is exactly

    alpha <= L-k-t+beta.                                (5)

In particular, a matching-closed packet with no TP--TP path satisfies the
bound, without any original two-selected-neighbor condition and regardless
of PP chain length, bends or cycles. This is a sufficient structural class;
it does not prove that every frozen packet belongs to that class.

For the following global corollary, return to the original SINGLE-TERMINAL
setting: every matching endpoint has at least three neighbors in T union P.
Let the packets be disjoint unions of original physical tiles, and require
every original endpoint-component receiver meeting a packet to lie wholly
inside that packet. In this setting the outside component receivers are
pairwise disjoint. Indeed, two distinct endpoint components in one tile
would occupy opposite corners; the other corners would be blank, giving
each endpoint occupied degree at most two. The original ledger is then

    margin = sum_packets S_J + D_out - q + R_out.

Here q is the positive outside component demand, R_out the absolute negative
outside charge and D_out the outside endpoint-free tile deficit. If (4) holds
in every packet and q<=sum(k+t), the half-area, coefficient-one bound follows.
This includes the no-TP--TP class. Packet surplus is counted once. Internal
receivers and paths cannot also be credited as outside resources; packets
must not overlap in physical tiles. This is a conditional improvement of the
5/6 coefficient on the stated class, not a new universal bound.

For arbitrary feasible configurations outside that single-terminal setting,
the exact global ledger has an additional -2N_out term for physical tiles
shared by distinct outside endpoint components. The complete correction and
a separate acyclic boundary-source collision family are proved in
RECEIVER_OVERLAP_AND_PP_BOUNDARY_SOURCE_COLLISION.md. The local identities
and target equivalence in this note are unchanged.

Equation (5) is a reduction, not a proof of its right-hand reserve being
large enough in general. Any future allocation must assign the L-k-t interval
reserve and beta BP--BP paths without reuse. The native transverse theorem
establishes (5) for a special geometry by proving L-alpha>=k+t; it does not
justify the analogous interval graph for arbitrary PP paths.

## 4. All-parameter backward PP path in the original neutral portal

Use the original whole neutral-pair configuration from
NEUTRAL_PAIR_DONOR_SATURATION.md, with even W>=6,H>=4. Its endpoint set and
matching come from the standard elbow shifted by (4,5), plus the actual edge
(7,5)--(8,5). The selections are exactly those in that note. The entire board
has H+8 rows and W+12 columns, so it is matching-closed and has blank first
and last columns in every two-row band. The cited all-parameter proof gives
feasibility, unique matching and complete freezing. No virtual selection is
inserted in the configuration considered here.

Index a column vertex by (band,column), with band=floor(row/2). There is
exactly one terminal path, whose ordered column vertices are

    (4,5), (3,5),
    (2,c) for c=5,6,...,W+4,
    (b,W+4) for b=3,4,...,H/2+2.                        (6)

The two terminals are TP, at actual endpoints (8,5) and (H+4,W+4).
Both have exactly two ORIGINAL selected neighbors. The first has (8,4),
(9,5); the second has (H+4,W+5), (H+5,W+4). All other vertices of (6)
are PP. To check the trace for every W,H, the initial matching edges go
(8,5)--(7,5) and (6,5)--(5,5). At band 2, top-row matching edges join
columns 5--6,7--8,...,W+3--W+4; bottom-row matching edges join
6--7,8--9,...,W+2--W+3. Contracting each PP column therefore traverses
every column 5 through W+4 in order. The right-leg matching in column W+4
then traverses consecutive bands through H/2+2. These are all the edges
of (6), numbering W+H/2+1, on W+H/2+2 column vertices.

Every remaining edge is a vertical matching loop inside a PP column:

    (b,W+3), b=3,...,H/2+1.

There are H/2-1 such loops. They and the path account for all W+H actual
matching edges. Thus alpha=1 and beta=gamma=0 for every W,H. The whole
surplus and forest count are exactly

    |T|=H+7, |M|=W+H,
    S_J=WH/2+3W+4H+41,
    L=S_J+1=WH/2+3W+4H+42.                              (7)

The surplus in (7) is positive; no target inequality fails here.

## 5. The connector rule that fails

In native transverse cancellation, a matching edge joins an interval whose
RIGHT boundary is a BB immediately before its terminal TP column to an
interval whose LEFT boundary is BB immediately after the other terminal TP
column. The direction is from an outgoing right boundary to an incoming
left boundary. Native pinwheel edges strictly increase column number and
preserve the parity of interval endpoint columns. These facts prove the
directed graph is acyclic and give the sealed-boundary argument.

Try exactly the same endpoint-boundary rule for the entire PP path (6).
At its left terminal (band4,column5), the adjacent right BB column is 6,
and it is the LEFT boundary of its forest interval. At its right terminal
(band H/2+2,column W+4), the adjacent left BB column is W+3, and it is the
RIGHT boundary of its forest interval. Both BB intervals are singletons in
the specified configuration. Consequently the proposed directed connector
is necessarily

    (band H/2+2, column W+3) --> (band4, column6).        (8)

For W>=6 this is strictly DECREASING in column. Since W is even, it also
changes column parity. Reversing (8) to restore increasing order would
reverse the outgoing/incoming roles, so it is not the same connector rule.
Reflecting the whole board does not cure the relative role reversal.

This refutes the universal claim that contracting a frozen PP path preserves
the native theorem's increasing, parity-preserving interval connector, even
when both TERMINAL endpoints have two original selected supports. Interior
PP endpoints, including (7,5), may need retained endpoints to freeze. The
native theorem required the stronger support condition at each relevant
actual crossing, which this configuration fails.

We do not assert that the full connector graph has a directed cycle in this
family. A backward edge alone is not a cycle. We also do not disprove a
different geometric allocation satisfying (4). What fails is the stated
monotonicity/parity argument for the naive contracted-path extension.

## 6. The alternate row phase resolves this specified family

For the SAME original neutral configuration, pair rows 1--2,3--4,...,
(H+5)--(H+6) instead of 0--1,2--3,... . This region has H+6 rows and
contains all selections and endpoints; only the two entirely blank outer
rows are omitted. Its matching is closed and both column boundaries remain
blank. Call its surplus S_alt and balance L_alt. The new path inventory is

    alpha_alt=0, beta_alt=W-2, gamma_alt=1,
    number of PP loops=H/2+2,
    S_alt=S_J-(W+12), L_alt=L-(2W+11).                   (9)

Here is a uniform check of that inventory, using row+1 merely as a convenient
coordinate label so these row pairs have ordinary even/odd indices. The upper
bar row is then 5, whose W/2 horizontal matching edges are BP--BP paths. The
lower bar row is 6. Its edge in columns 6--7 is the sole TP--BP path. Its
W/2-3 edges beginning at columns 8,10,...,W are BP--BP paths. The remaining
edge at columns W+2--W+3 initiates the sole long BP--BP path; its column
vertices are (3,W+2), then (b,W+3) for b=3,...,H/2+2. It has H/2 matching
edges and H/2-1 interior PP vertices. Thus beta=W/2+(W/2-3)+1=W-2.
The short elbow tip, neutral pair and H/2 right-leg pairs are PP loops.
These paths and loops exhaust the displayed matching. The balance shift in
(9) follows either directly or by comparing (3) in the two phases.

This gives a checked all-parameter application of the no-TP--TP corollary,
including a bent PP path of arbitrary length in a completely frozen original
configuration. It also shows why the backward connector is an obstacle to a
particular proof, rather than evidence against the target: this family admits
a different row partition with only nonnegative path contributions.

The alternate bands are not aligned to the fixed ORIGINAL physical tiling.
Using them in a global receiver allocation requires an explicit compatible
partition or boundary conversion; one must not use the shifted phase for
surplus while retaining overlapping resources from the original phase. No
general existence theorem for a favorable phase is asserted.

## 7. Verification scope

The general proofs are Sections 1--6. The companion permanent checker is
develop/check_pp_path_terminal_ledger.py; it preserves loops, parallel edges,
exterior terminals and edge ownership. Its short complete label/matching
controls include models outside the native support hypothesis. It also
checks all six terminal types, the native sharp families, neutral portal
parameter families, symmetry images and open crops. Finite enumeration is
used only to test the written identities and coordinate formulas.

Scoped Lean source formal/SubQuorum/PPPathTerminalLedger.lean checks arbitrary
finite path inventories, arbitrary PP-chain size, exact ledger arithmetic,
the target equivalence and structural corollaries, and neutral count/parity
consequences. The actual grid-to-multigraph classification, geometry and
ownership adapter remain written proofs, not claims of full formalization.
Execution and independent review status are recorded separately in output.
The permanent controls pass 7131 models, including 6211 short feasible matching
choices, 266 neutral parameters in both phases, 320 native sharp parameters,
24 symmetry images and 36 open crops. They check ownership of 46194 matching
edges and all six terminal types. Local Lean4.33.0 passes 17 scoped theorems
and individual ordinary-axiom audits, without errors, warnings, sorry or native
evaluation. These execution results are not substitutes for the general proofs.

The initial independent written review returned REVISE: it confirmed the
local results and all-parameter constructions, but identified the missing
single-terminal/additive-receiver scope in the global paragraph. That scope
is now explicit above. The full response is archived in
output/pp-path-terminal-ledger-initial-review.json. That initial verdict remains
REVISE as a historical record. Follow-up aa9e1dd1 completed ACCEPT and explicitly
accepted this corrected note independently of its new companion; see
output/receiver-overlap-and-pp-source-collision-oracle.json for the complete
written review and its exact scope. Neither review certifies code execution.

The remaining research problem is a geometric proof of (4), or a more precise
counterexample to a proposed ownership rule, for arbitrary retained-support
components. General grid compensation and triple equality remain open.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
