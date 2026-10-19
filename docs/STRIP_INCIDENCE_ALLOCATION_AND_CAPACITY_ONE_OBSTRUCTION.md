# Exact strip incidence allocation and a frozen capacity-one obstruction

20 October 2026. A fully frozen 8-by-10 configuration refutes universal
coverage by the four corner rules together with all maximal endpoint-free
runs of actual capacity at least two. Every such run has capacity at most
one, while the complete receiver charge is one. The original grid target
still holds: objective38is below half-area40.

The appropriate allocation structure is a bipartite multigraph whose edges
are the actual physical capacity units. Its exact one-unit-per-run rank
depends on tree components, rather than excluding every degree-one run.
This removes the threshold-two restriction without permitting reuse.
The graph matching fact is standard; the contribution here is its exact
physical-capacity adapter, reservation rule and explicit frozen obstruction.

## 1. Physical capacity multigraph

Use a feasible pair(T,M)on an even-by-even rectangular nearest-neighbor
grid. Write P=V(M), and let Z be the endpoint-free tiles in the original
fixed disjoint2-by2tiling. Selected means T, not T union P. Each tile Q
has actual capacity d_Q=2-|T intersect Q|>=0.

Each Q in Z belongs to exactly one maximal horizontal Z-run h(Q)and one
maximal vertical Z-run v(Q). Deduplicate intervals and their reversals;
horizontal and vertical singleton runs remain distinct vertices.

Reserve already assigned distinct slots first: integer0<=a_Q<=d_Q,
B=sum a_Q, residual r_Q=d_Q-a_Q. Build a bipartite multigraph G_r:
one vertex for each maximal run, and r_Q parallel edges joining h(Q)to
v(Q). Label each edge by its physical slot(Q,unit). There are no loops,
since the two endpoints have different axes. A capacity-two tile can
produce a genuine two-edge cycle. Include isolated zero-capacity runs;
an implementation may omit them if it separately rejects their requests.

The weighted degree of a run is exactly its residual capacity. The full
edge count is D-B, where D=sum_Q d_Q. Deleting reserved slots changes
edges, not the original endpoint-free maximal runs.

## 2. Exact allocation theorem

**Theorem.** Let X be any set of distinct maximal runs, each requesting one
unit. There is a choice of distinct incident physical slots for all runs
in X if and only if X contains no entire tree component of G_r.
Isolated vertices count as one-vertex trees.

**Necessity.** A tree component has v vertices and v-1 edge slots. Asking
all its vertices for separate slots fails Hall on that component. No slot
outside the component can pay one of its runs.

**Sufficiency by Hall.** Take any subset A of X and examine one connected
component C of G_r. If A intersect C is nonempty and proper, split the
induced graph on A intersect C into connected pieces. A piece with t
vertices has at least t-1 internal edges. Since C is connected and the
piece is a proper subset of C, it also has an edge to its complement.
Different pieces have different boundary edges: an edge between two pieces
would join them in the induced graph. Hence the number of distinct slots
incident with A intersect C is at least |A intersect C|.

If A contains all vertices of C, the hypothesis says C is not a tree.
A connected loopless multigraph that is not a tree has e>=v, including
parallel-edge cycles, so its incident slots again number at least v.
Summing over components proves every Hall inequality. QED.

This is also constructive. In a tree choose an unrequested root and use a
spanning orientation away from it: each other vertex receives its distinct
parent edge. In a cyclic component choose a cycle and extend it to a
connected spanning subgraph with exactly one cycle. Assign cycle edges
cyclically and every remaining parent edge to its child. This pays every
vertex there; discard assignments to vertices outside X. The algorithm
in the repository uses augmenting paths and verifies the same criterion.

## 3. Exact maximum and reservation monotonicity

Let v_C,e_C be the vertex and slot counts of a connected component.
The maximum number K(r)of distinct runs that can each receive one unit is

    K(r) = sum_C min(v_C,e_C)
         = number_of_runs - number_of_tree_components.           (1)

The upper bounds v_C and e_C are immediate. The preceding constructive
proof attains v_C-1=e_C in a tree and v_C in a cyclic component. Isolated
vertices contribute zero. In particular K(r)<=sum_Q r_Q.

The old one-unit-per-capacity-at-least-two collection is always feasible:
a nontrivial tree has a degree-one vertex, and an isolated vertex has
degree zero. Consequently that collection cannot contain any whole tree
component. Thus

    #{runs with residual capacity at least two} <= K(r).          (2)

Unlike the old threshold rule, the exact criterion can select a degree-one
run when some other vertex of its tree is left unrequested.

**Reservation monotonicity.** Removing a single physical slot lowers K by
at most one. Indeed, take a maximum matching before removal. If the slot
was unused, the matching survives; otherwise discard its one paid request.
Deleting edges cannot increase the maximum. Therefore

    K(r)-1 <= K(r-one_slot) <= K(r).                             (3)

For any two valid reservations a<=a' tilewise, with B=sum a,B'=sum a',

    B+K(d-a) <= B'+K(d-a') <= D.                                (4)

The first inequality follows by removing the B'-B additional slots and
applying(3)repeatedly. Hence reserving additional distinct certified corner
credits cannot worsen this exact hybrid score. The simple threshold count
does not itself have this monotonicity guarantee.

Equation(1)is for ONE request per run. The previous weighted rule with
floor(C_s/2)requests per run remains a separate valid certificate and may
pay several requests at a high-capacity run. One may choose the larger of
the two valid residual totals; their totals must not be added on the same
slots. No claim that K dominates that multi-request rule is made.

## 4. Conditional cross-component consequence

Now assume single terminality and complete receivers
R_H={physical tiles meeting endpoints of component H}. Use the established
disjoint ownership and ORIGINAL corrected receiver identity

    mn/2-|T|-|M| = D - sum_H rho_H.

If certified reservations and the physical incidence graph satisfy

    sum_H rho_H <= B+K(d-a),                                    (5)

then(4)gives sum_H rho_H<=D, so |T|+|M|<=mn/2. Replacing the left side
by sum_H max(rho_H,0)is a stronger sufficient condition.

Every credit is a separate edge slot; perpendicular overlaps, parallel
capacity-two edges and different receiver components cannot spend it twice.
No local component owner is needed for this GLOBAL inequality. Additional
routing restrictions would have to be added explicitly if an application
required a particular receiver to be paid only by particular runs.

This is a structural reduction, not a universal coverage theorem. Proving
(5)for all relevant grid representatives remains open. The unrestricted
five-sixths bound and grid triple equality are not improved here.

## 5. A fully frozen32-endpoint obstruction

Coordinates start at zero. P is a matching endpoint, T is selected, and
a dot is blank. Every unmarked grid site is blank.

    .T.T.TT.TT
    TPPP...T..
    .PPPPT..T.
    TPP.T.T.PT
    .PPT...TP.
    TPP.T.T.PT
    .PPPPPPPP.
    TPPPPPPPPT

There are32endpoints,22selections and16actual matching edges:

    (1,1)--(2,1)
    (1,2)--(1,3)
    (2,2)--(3,2)
    (2,3)--(2,4)
    (3,1)--(4,1)
    (3,8)--(4,8)
    (4,2)--(5,2)
    (5,1)--(6,1)
    (5,8)--(6,8)
    (6,2)--(6,3)
    (6,4)--(6,5)
    (6,6)--(6,7)
    (7,1)--(7,2)
    (7,3)--(7,4)
    (7,5)--(7,6)
    (7,7)--(7,8)

Direct neighbor checking gives selected degree at most one and endpoint
occupied degrees24times three and8times four. The endpoint set is
connected: the bottom two-row bar joins the thick left leg and thin right
leg, and the top extension joins the left leg. The receiver has14tiles,
13selections and32endpoints, so its original corrected charge is

    rho = 13+32/2-2*14 = 1.

For completeness the receiver inventory by(endpoint,selection)counts is

    (1,2):3tiles; (2,1):7tiles; (3,0):1tile; (4,0):3tiles.

The actual saturated-mate transfers, each of size1/2, are

    Q_(0,0): (1,1)--(2,1), destination Q_(1,0);
    Q_(1,2): (2,4)--(2,3), destination Q_(1,1);
    Q_(1,4): (3,8)--(4,8), destination Q_(2,4).

All source and destination tiles belong to this same complete receiver;
the correction therefore preserves its total charge. The Lean source also
checks the original corrected tile sum, rather than only the raw total.

The six endpoint-free tile capacities are

| Tile | (0,2) | (0,3) | (0,4) | (1,3) | (2,2) | (2,3) |
|---|---|---|---|---|---|---|
| Capacity | 1 | 0 | 0 | 1 | 1 | 0 |

Their sum is D=3. The global ledger gives40-22-16=3-1=2.
Thus this is a counterexample to a coverage rule, not to the grid target.

## 6. Complete mixed-bundle freezing proof

Here is an ordered certificate. Each row contains its endpoint and two
distinct adjacent retained witnesses, neither its own mate:

    step endpoint witness1 witness2
     1  (1,1)  (0,1)  (1,0)
     2  (2,4)  (2,5)  (3,4)
     3  (3,8)  (2,8)  (3,9)
     4  (1,3)  (0,3)  (2,3)
     5  (2,2)  (2,1)  (2,3)
     6  (3,1)  (2,1)  (3,0)
     7  (5,8)  (4,8)  (5,9)
     8  (4,2)  (3,2)  (4,1)
     9  (5,1)  (4,1)  (5,0)
    10  (7,8)  (6,8)  (7,9)
    11  (6,2)  (5,2)  (6,1)
    12  (6,7)  (6,8)  (7,7)
    13  (7,1)  (6,1)  (7,0)
    14  (6,4)  (5,4)  (6,3)
    15  (7,3)  (6,3)  (7,2)
    16  (7,6)  (6,6)  (7,7)
    17  (6,5)  (6,6)  (7,5)
    18  (6,6)  (5,6)  (6,5)
    19  (7,5)  (6,5)  (7,4)
    20  (7,4)  (6,4)  (7,5)
    21  (7,7)  (6,7)  (7,6)
    22  (6,3)  (6,4)  (7,3)
    23  (6,8)  (6,7)  (7,8)
    24  (4,8)  (4,7)  (5,8)
    25  (7,2)  (6,2)  (7,3)
    26  (6,1)  (6,2)  (7,1)
    27  (5,2)  (5,1)  (6,2)
    28  (4,1)  (4,2)  (5,1)
    29  (3,2)  (3,1)  (4,2)
    30  (2,1)  (2,2)  (3,1)
    31  (1,2)  (1,1)  (2,2)
    32  (2,3)  (1,3)  (2,2)

For every row, a witness is either an original T-vertex or an endpoint
whose actual mate occurs in an earlier row. This property can be checked
directly against the16matching edges above.

If a nonempty simultaneous promotion bundle were feasible, take its earliest
promoted endpoint in this table. Original selections remain occupied.
Removing an endpoint witness requires promoting its actual mate, which
would occur earlier and contradict earliest choice. Thus both witnesses
remain occupied, giving the promoted selection at least two occupied
neighbors. This is impossible. This proves freezing for arbitrary mixed
simultaneous bundles, not merely single moves or one color.

## 7. Exhaustive strip and old-corner exclusions

The complete maximal endpoint-free runs and their actual capacities are:

| Axis | Physical tiles | Capacity |
|---|---|---|
| Horizontal | (0,2),(0,3),(0,4) | 1 |
| Horizontal | (1,3) | 1 |
| Horizontal | (2,2),(2,3) | 1 |
| Vertical | (0,2) | 1 |
| Vertical | (2,2) | 1 |
| Vertical | (0,3),(1,3),(2,3) | 1 |
| Vertical | (0,4) | 0 |

These exhaust the intervals in the six-tile complement of the receiver.
Every proper subinterval also has capacity at most one by nonnegativity.
Hence even allowing nonmaximal subruns cannot produce a capacity-two run.
No sealed run exists, since such a run would have capacity at least two.
The old weighted floor(C_s/2)rule also gives zero.

For capped donors it suffices to examine endpoint-free tiles. The only
aligned extended sides consisting of four endpoints are the south side of
Q_(2,2)and the south/east sides of Q_(2,3). Their six transverse
tip/support pairs are:

| Tile/side | First pair | Second pair |
|---|---|---|
| (2,2),south | (5,3)blank / (4,3)T | (5,6)T / (4,6)blank |
| (2,3),south | (5,5)blank / (4,5)blank | (5,8)P / (4,8)P |
| (2,3),east | (3,7)blank / (3,6)T | (6,7)P / (6,6)P |

None has the required P-tip/T-support combination. The scanner additionally
checks every aligned side in all receiver tiles; those cannot be donors
because the required endpoint-free corner condition fails.

The only selected corners in endpoint-free tiles with an exterior endpoint
anchor are(4,7),(5,6),(5,4). Their opposite corners are respectively
(5,6),(4,7),(4,5). None has an exterior selected guard; their exterior
endpoint guard sets are respectively{(6,6)},{(4,8)},empty. Thus the
selected-guard and two-endpoint-guard rules fail. For the degree-sensitive
fourth rule, q=(6,6)has occupied degree4, and q=(4,8)has only two other
endpoint neighbors. Those are the only candidates, so it also fails.

Consequently B=0for every possible reservation supported by the four old
rules, and the number of residual-capacity-two runs is zero, while rho=1.
This disproves universal coverage by their union. It does not disprove the
valid conditional Hall theorem or the target inequality.

## 8. Exact incidence allocation repairs this obstruction

The positive physical capacities are one unit each at Q_(0,2),Q_(1,3),
Q_(2,2). Each is the sole positive edge of its horizontal and vertical run.
The incidence graph has three disjoint one-edge tree components plus one
isolated zero-capacity run. Its full rank is

    K = 3*min(2,1)+min(1,0) = 3.

Choose one endpoint-run of each tree, rather than requesting both endpoints
of the same single slot. All three units can be allocated distinctly; only
one is needed for rho=1. The previous remote28example instead has two
parallel edges between two runs, a cycle of rank2. These two cases explain
why a global graph criterion treats capacity-one tiles and capacity-two
tiles differently while keeping exactly the same physical ledger.

Boundary endpoints occur in this example. All eight tile-preserving physical
symmetries have the same obstruction. No unchanged blank-padding invariance,
minimality of32endpoints, or all-degree-three restriction is asserted.

## 9. Verification and remaining scope

Run

    python3 -B develop/check_strip_incidence_allocation.py --output output/strip-incidence-allocation-controls.json

The independent abstract controls cover all729capacity-labeled2-by3
bipartite multigraphs with edge multiplicities0,1,2, all23328request subsets,
and2916single-unit reservation transitions. They compare the tree criterion
and actual matching with every Hall-subset condition, and compute the maximum
over all request sets independently of the rank formula.

96physical controls cover six real fixtures, eight symmetries and two
reservation settings; six separated2/3/4-component controls also pass.
An independent interval scan checks maximality, physical capacity sums and
the exact original receiver ledger. The old144-case sealed scanner controls
pass after extending its API to return unsealed maximal runs as well.

The new Lean file formalizes the exact finite32-endpoint configuration:
actual occupied-grid coordinates, selected feasibility, actual matching,
all32freezing steps and arbitrary mixed-bundle exclusion, the ORIGINAL
corrected receiver charge, outside deficit3, and bounds on EVERY horizontal
and vertical maximal-run capacity. It does not formalize absence of the four
old corner types or the general graph-rank theorem; those have the explicit
written proofs and independent checks above. Execution and axioms are
recorded separately in output/strip-incidence-formal-check.json.

The discovery solver is optional. Its SAT output suggests the coordinates;
the displayed finite construction, ordered proof and independent checking
establish the counterexample without trusting solver unsatisfiability.
No finite search replaces either general allocation proof.

The earlier sealed-strip review required definition/dependency clarifications
and corrected a real border-completion error: the completed remote vertical
run extends from length2/capacity2to length3/capacity4. That note is repaired.
Its review does not cover this newer incidence theorem or32-endpoint example.

The next problem is the geometric lower bound(5), or a valid normalization
that guarantees it. One must account for the cost of tree components and
for rank lost when many resource units lie between too few distinct runs.
The present result settles exact one-unit allocation, not universal coverage.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
