# Partial PP connectors: exact boundary compensation, actual cycles and missing ports

22 October 2026. Authors: Haobo Ma and Wenlin Zhang.

We give an exact compensation criterion that allows connector cycles, merged
boundary sources, and TP--TP paths without an adjacent blank-column port.
Two uniform fully frozen constructions show that cycles and missing ports
actually occur. Neither construction violates the target inequality. In
particular a cycle is not an additional debit when interior reserves count
only path components. Counting all interior components instead requires one
cycle correction, exactly once.

## 1. Setup and a connector construction with no coverage assumption

Use the feasible pair (T,M), actual endpoint set P and PP-column multigraph
of PP_PATH_TERMINAL_LEDGER_AND_BACKWARD_CONNECTOR.md. Let J be k adjacent
aligned two-row bands of the same width n>=2. Its first column in every band
is BB and its final column has a blank corner. Assume the actual matching is
closed in J. Define

    S=|J|/2-|T intersect J|-|P intersect J|/2,
    alpha=#TP--TP paths, beta=#BP--BP paths,
    L=#BB columns-#TT columns.

The established exact ledger is S=L+beta-alpha. TP--BP paths and pure PP
cycles have zero net terminal charge. The PP multigraph and the connector
multigraph defined below are different graphs; their cycles must not be
identified.

In each band join consecutive BB/TT columns when at least one is TT.
Feasibility forces both neighbors of a TT column to be BB. Since neither
end column is TT, the resulting components are odd alternating intervals
BB,TT,...,BB, including isolated BB columns. There are exactly L intervals.

At a TP terminal a port means an immediately adjacent BB column in its own
band. Select ANY SUBSET of the alpha paths for which both terminals have
ports, and choose ONE port at each of their two terminals. Add an undirected
edge joining the two chosen interval vertices for every selected path.
Keep edge multiplicity and loops. Let a be the number of added edges and

    u=alpha-a.

Thus u counts every omitted TP--TP path, whether omission was forced by a
missing port or was a choice. A TP terminal need not have any port. No
orientation, monotonicity, acyclicity or complete coverage is assumed.

There is an exact local description of missing ports. At a TP--TP terminal,
the endpoint's actual mate MUST cross to the next band in the same column.
Indeed the selected corner in its own column forces its horizontal neighbors
to be blank. A horizontal mate of the endpoint would therefore lie in a BP
column, terminating a TP--BP path immediately, contrary to the path type.
The vertical neighbor within its own band is selected and cannot be its mate.
Matching closure puts its actual mate in the neighboring band.

The two horizontal neighbors of the selected corner are blank. Hence a
lateral column is BB precisely when the endpoint's horizontal neighbor
on that side is blank. The endpoint has two fixed occupied vertical
neighbors, its selected corner and actual mate. It follows exactly that

    #BB ports at this terminal = 4-occupiedDegree(endpoint).     (0)

Boundary columns cannot be TP under the hypotheses, so both lateral columns
exist. In particular a terminal has no port if and only if its occupied
degree is four. If m paths have at least one missing terminal and q_4 counts
their degree-four terminals, distinct paths have distinct terminals and

    m<=q_4<=2m.

Connecting every attachable path gives u=m. Thus the residual is a precise
degree-four obstruction, not an unspecified exceptional path type. When
all alpha terminals have occupied degree at most three, complete connector
coverage is automatic. No freezing assumption is used in this local lemma.

There is a further constraint in the single-terminal setting where every
endpoint has occupied degree at least three (in particular in a completely
frozen pair). A missing-port terminal must have a horizontal ENDPOINT
neighbor, lying in a BP column. Otherwise both its occupied horizontal
neighbors would be selections. Feasibility at these selections would force
both horizontal neighbors of its vertical actual mate to be blank. That
mate would have occupied degree at most two, a contradiction. This locates
a real adjacent BP terminal for each missing port, but it does not assign
distinct BP--BP paths: two demands might reach the same path, or reach a
TP--BP path. It is not a compensation proof by itself.

## 2. Why the connector graph has degree at most two

A port next to a TP column must be an END of its BB--TT interval: the
intervening TP column is not part of the interval. A fixed interval's left
end can be chosen only by the TP column immediately to its left in that
same band. That column contains exactly one endpoint, which belongs to
exactly one actual matching path. It can be used only once. The same proof
applies at the right end. Therefore each interval has at most two connector
incidences, with a loop using both incidences. This argument uses neither
freezing nor a native selected-neighbor assumption.

Mark the interval containing the first BB column of each band. If n is even,
also mark every interval containing a final BB column; write t for the
number of such sealed bands. If n is odd put t=0. All

    B=k+t

marked vertices are distinct. In one even-width band an alternating
interval has odd length and cannot contain both end columns. Different
bands have different interval vertices. Every marked interval has degree
at most one, since one of its ends lies on the boundary of J and has no
neighboring TP column. In particular a marked vertex cannot lie on a cycle.

Every finite connected multigraph of maximum degree two is a path, an
isolated vertex, or a cycle. Here a loop is a one-vertex cycle and two
parallel edges form a two-vertex cycle. To verify the classification,
start at a degree-at-most-one vertex when one exists and follow the sole
unused continuation. It cannot branch; closing before exhausting the
component would leave no unused incidence for any remaining vertex.
Otherwise all degrees are two, and following unused edges returns to the
start and exhausts the component. A path has one more vertex than edges;
a cycle has equal numbers of vertices and edges. A path contains at most
two marked vertices, at its endpoints; an isolated vertex contains at most
one.

Let h_j count path components with exactly j marked vertices, j=0,1,2,
including isolated vertices, and let c count cycle components. Then

    L-a=h_0+h_1+h_2,       B=h_1+2h_2.                (1)

In particular L-a counts PATH components, not all components. Subtracting
c again from this expression would charge every cycle twice.

## 3. Exact compensation theorem and unique ownership

Substitute alpha=a+u into the PP ledger and then use (1). This proves

    S=h_0+h_1+h_2+beta-u,
    S-B=h_0+beta-h_2-u.                               (2)

Consequently, for EVERY permitted selection of paths and ports,

    S>=k+t  iff  h_2+u<=h_0+beta.                     (3)

This is a necessary and sufficient local compensation criterion, not a
claim that its right-hand inequality holds for every frozen configuration.
It strictly extends the native proof's counting mechanism: cycles are
allowed, boundary sources may merge, and omitted paths retain their unit
debit. The no-TP--TP case is recovered with a=u=0.

There is an explicit allocation interpretation. Regard each unmarked
connector PATH component and each actual BP--BP matching path as one
distinct resource. Regard every twice-marked connector path and every
omitted TP--TP matching path as one demand. These are finite sets with
sizes h_0+beta and h_2+u. An injection from demands into resources proves
the bound; conversely (3) implies such an abstract injection. A geometric
or local injection remains a separate problem. The resource count never
counts individual intervals again after placing them in a connector
component. The beta matching paths are distinct actual edge-disjoint
paths, and their credit was not used to form connector edges. Omitted
TP--TP paths are not used as edges or resources.

If i_0 counts ALL unmarked connector components, including cycles, then
i_0=h_0+c and the SAME identity is

    S-B=i_0+beta-h_2-u-c.                             (4)

One may use h_0 without a cycle debit or i_0 with one debit c, but not h_0-c.
For example, two interval vertices joined by two parallel connectors have
L=a=2, h_0=0, c=1 and contribute zero to L-a. They do not contribute -1.

For disjoint physical-tile packets with complete original receiver closure,
the established arbitrary-feasible outside ledger gives

    global margin = sum_J [B_J+h_0,J+beta_J-h_2,J-u_J]
                    +D_out-q+R_out-2N_out.           (5)

Thus injections as above in each packet, together with
q+2N_out<=sum_J B_J (or the version also using unused D_out+R_out),
give the coefficient-one half-area bound on that stated class. These are
conditional sufficient hypotheses improving the former 5/6 coefficient;
there is no universal improvement asserted here. Every interval and matching
path belongs to one packet, and inside receiver overlaps are already in S.
No credit from (2) is added to S again in (5).

## 4. Actual two-edge connector cycles in completely frozen configurations

Let W>=6,H>=4 be even. Let C(W,H) be the single block collision_family(W,H,1)
from RECEIVER_OVERLAP_AND_PP_BOUNDARY_SOURCE_COLLISION.md. Its shape is
(W+12) by (H+10). It is feasible, has a unique actual matching and completely
freezes. Apart from the four added selections

    (4,3),(5,3),(W+4,3),(W+5,3),

all occupied vertices have column at least 5. Its unique TP--TP path lies
in column 5, with terminal bands 2 and W/2+2. Its unique ports are column 4
in those bands, belonging to BB2--TT3--BB4. The other adjacent column 6 is BP.

Take two images of this ENTIRE block under

    right: (row,col) -> (row,col+H+2),
    left:  (row,col) -> (row,H+8-col).

Use the union of the selected sets and the union of the matchings, on the
board (W+12) by (2H+12). The four added selections coincide at column H+5
and are included ONCE. All other occupied vertices of the right image
have column at least H+7 and those of the left image at most H+3. The
shared selections see only their paired selection and are separated from
both occupied cores by blank columns. Consequently there are no new
occupied adjacencies; both endpoint cores, unique matchings and full
freezing certificates persist. The smallest occupied column is 1 and
the largest is at most 2H+9, so the whole board has blank end columns and
is an aligned, matching-closed physical packet containing every receiver.

The two TP--TP paths are at columns H+7 and H+3. In each of their two
terminal bands the chosen ports lie in the SAME interval

    BB(H+4)--TT(H+5)--BB(H+6).

The two paths therefore create two parallel connector edges between the
same two distinct interval vertices. This is an actual connector cycle,
with no choice of alternative ports. The PP graph separately has W-2
single-edge loops; those are not this connector cycle.

All other intervals are isolated. The cycle's two vertices are interior,
and all B=W+12 marked boundary intervals are isolated. Exact counts are

    |T|=2H+18, |M|=2(W+H),
    alpha=2, beta=0, gamma=2(H+1), PP loops=W-2,
    S=WH+4W+8H+54, L=S+2,
    c=1, u=h_2=0, h_1=B, h_0=S-B.

The selected count subtracts the four shared selections once. The matching
and PP counts add the two disjoint cores. The area formula gives S; the
PP ledger gives L. After removing the two cycle vertices the remaining
L-2=S intervals are isolated, which proves the displayed h counts.

Stack r>=1 blocks with row offsets j(W+12). Occupied rows within each block
lie in 4,...,W+5; successive blocks have no occupied adjacency. Physical
alignment, receiver closure, unique matching and full freezing persist.
All displayed inventories multiply by r, so c=r, while

    S-B=r(WH+3W+8H+42)>0.                             (6)

This disproves universal connector acyclicity for the actual frozen
configurations. It does not disprove the target, and cycles have zero
net contribution to L-a.

## 5. Actual fully frozen paths whose terminals have no BB port

Start instead with the original neutral_pair(W,H), before adding the four
TT selections. Add original selections (3,5) and (3,W+4), and apply
(oldrow,oldcol)->(oldcol,oldrow+1). Equivalently remove the four TT additions
from C(W,H), and add (5,4),(W+4,4).

In original coordinates occupied rows start at 4. Each new selection in
row 3 sees precisely its endpoint immediately below, respectively (4,5)
and (4,W+4); its other three neighbors are blank. The selections are
distinct and nonadjacent for W>=6. No old selection gains an occupied
neighbor. Feasibility therefore persists. The endpoint set and matching
are unchanged, so uniqueness persists. Adding feasible selections deletes
no original or retained witness in the existing full freezing certificate;
that certificate remains valid. This proves the construction for all W,H.

After the transform the sole TP--TP path still lies in column 5, with
terminal endpoint rows 5 and W+4. At BOTH terminals the left column 4 is
now BT and the right column 6 is BP. Neither terminal has a BB port. The
fact that each has two original selected neighbors does not create a
port by itself. In particular complete freezing does not imply port
coverage for TP--TP paths.

For a common board and for stacking with the preceding constructions,
shift this configuration two columns left and embed it in
(W+12) by (2H+12), leaving extra columns blank. It has

    |T|=H+9, |M|=W+H,
    alpha=u=1, beta=0, gamma=H+1, PP loops=W/2-1,
    S=WH+5W+10H+63, L=S+1,
    B=W+12, c=h_2=0, h_1=B, h_0=L-B.

Here a=0 and every interval is isolated. Formula (2) gives S-B=h_0-1.
Omitting the residual debit u would overestimate the actual reserve by
one. The target still holds, with excess WH+4W+10H+51>0. Stacking r
separated blocks makes the missing-port debit r, not a bounded exception.
Although the missing terminals have adjacent BP endpoints, beta=0 throughout
this family: all the adjacent BP terminals belong to mixed TP--BP paths,
which supply zero credit in the PP ledger. Thus finding such a BP terminal
does not by itself supply the missing unit of compensation.

## 6. Coexistence and the remaining theorem

The earlier collision block can also be shifted two columns left onto the
common board. Its source interval becomes BB0--TT1--BB2, so its one
connector joins two first-boundary marked intervals. It has

    S=WH+5W+10H+61, h_2=1, c=u=0.

Arbitrarily stack r_C cycle blocks, r_B collision blocks and r_U missing-port
blocks, not all zero, using their common row height W+12. Feasibility,
unique matching, full freezing and physical closure follow from the same
separation. With all attachable paths connected,

    c=r_C, h_2=r_B, u=r_U, beta=0,
    B=(r_C+r_B+r_U)(W+12),
    S=r_C(WH+4W+8H+54)
      +r_B(WH+5W+10H+61)+r_U(WH+5W+10H+63),
    h_0=S-B+r_B+r_U.

Thus these three effects coexist independently on actual frozen boards.
An argument must neither assume missing ports away nor spend cyclic
components as unit reserves. The examples all have ample interior reserves;
the general geometric inequality h_2+u<=h_0+beta remains open. In particular
this note supplies an exact reduction and two uniform rule obstructions,
not the missing universal allocation theorem or rectangular-grid triple equality.

## 7. Reproducibility and formal scope

The companion checker is
develop/check_interval_connector_cycles_and_missing_ports.py. It checks
the actual matching, feasibility, unique matching and complete freezing,
preserving connector multiplicity, marked interval ownership and residual
paths. It also checks independent short configurations, partial connector
choices, reflected/transposed images and mixed block inventories. Run it with

    PYTHONDONTWRITEBYTECODE=1 python3 develop/check_interval_connector_cycles_and_missing_ports.py --output output/interval-connector-cycles-and-missing-ports-validation.json

The companion formal/SubQuorum/IntervalConnectorCyclesAndMissingPorts.lean
proves arbitrary finite component inventory identities and their arithmetic
compensation and global corollaries. The coordinate, freezing and actual
grid-to-multigraph adapters in Sections1--6 are written proofs, not a full
Lean formalization. Finite computations test the written arguments and are
not substitutes for the uniform proofs above. Execution and independent
review outcomes are archived separately and must be read at their actual scope.

The permanent checker passes 6748 connector models: 6211 independent short
matching configurations, 383 fully frozen unique-matching family packets,
24 symmetry images, and partial/alternative connector choices. The family
packets include 240 parameter triples, 80 multiplicities through r=40 and
63 mixed inventories. There are 1004 actual connector cycles, 1203 missing-port
paths and 288 twice-marked path components across all controls, with exact
edge/port ownership checked. The results are in
output/interval-connector-cycles-and-missing-ports-validation.json.

Local Lean4.33.0 passes 19 scoped theorems and 19 individual axiom audits,
without errors, warnings, sorry or native evaluation. The two Boolean
port-degree lemmas and the two-edge-cycle example have no axioms. Other
inventory/corollary proofs use the ordinary axioms listed in
output/interval-connector-cycles-and-missing-ports-lean.json. The actual grid
and coordinate adapters remain written, including the adjacent-BP lemma.

Independent review 37c00120-f31d-4521-8718-2046d884cfc8 is dispatched in
conversation conv_9a8ee0adac356fe3. Its initial input predates the local
port-degree and adjacent-BP additions above. No acceptance of either the
initial note or those additions is inferred while the task is live.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
