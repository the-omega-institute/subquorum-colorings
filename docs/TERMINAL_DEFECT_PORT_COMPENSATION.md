# Terminal defects, full-pool compensation and exact interval withdrawals

26 October 2026. Wenlin Zhang and Haobo Ma. Independent research continuation.

The full-pool question following the [beta-core switch theorem](PINWHEEL_BETA_CORE_SWITCHES.md)
has an automatic positive answer under the standard packet boundary conditions:
if every alpha terminal has occupied degree three, all original alphas have
simultaneous zero-link payments by different original intervals. Neither root
flips nor beta credits are needed. Other endpoints may have degree four; paths
may bend, chambers may branch, and different endpoint components may share
intervals. Freezing is stronger than the single-terminal hypothesis used here.

We also give an exact formula for the loss of this **port-only certificate**
after arbitrary original intervals are withdrawn. On a general rectangle the
only additional exceptions in this reduction are explicit lateral-boundary
defects. We do not discard them or claim to have settled their geometric
coverage. The universal grid inequality and universal improvement of 5/6
remain open.

This is a new geometric consequence and quantitative completion of the earlier
[port-degree and connector lemmas](INTERVAL_CONNECTOR_CYCLES_AND_MISSING_PORTS.md),
using the elementary allocation mechanism in
[one-sided allocation](ONE_SIDED_INTERVAL_AND_BETA_ALLOCATION.md).
The underlying path/cycle matching argument is standard, not a new abstract
matching theorem. Unlike the earlier partial connector construction, every
alpha is retained as an edge, with a separate zero-capacity endpoint for every
missing port. Boundary-marked positive units are available in the full pool;
they must not silently be removed in the corollaries below.

## 1. Physical hypotheses and the complete port graph

Fix a feasible pair (T,M) on an even-by-even rectangular grid, with P=V(M).
Every selected vertex has at most one occupied neighbour in T union P.
Assume every endpoint has occupied degree at least three. Use the original
horizontal two-row bands and vertical N-pairs. Matching M is the actual
matching, closed in the rectangle. An alpha is a TP--TP component of M union
the PP N-edges. All resource identities refer to this original configuration.

A BB--TT forest component joins neighbouring BB/TT columns whenever at least
one is TT. Feasibility makes each TT neighbour BB. Each such component is an
alternating interval. It has BB-TT difference one or zero: a difference-one
component is one original unit; a difference-zero component touches a lateral
boundary and ends there with TT. There are no negative components on an even
width: an interval starting and ending TT would have odd length and would
have to span the whole even-width band. A balanced component has one BB end
facing the interior, and hence at most one possible alpha-port incidence.

At an alpha terminal v the actual mate is vertical in the neighbouring band.
Indeed the selected N-partner forces its horizontal neighbours blank; a
horizontal mate of v would consequently be BP and end a mixed path immediately.
The other vertical neighbour is the selected N-partner. At an interior column,

    number of immediately adjacent BB ports = 4 - deg_occupied(v).

Thus a degree-three terminal has exactly one port, while a degree-four terminal
has none. At a lateral board edge a degree-three terminal can have no physical
port: the missing outside column is not a resource. No terminal has two ports
under the stated degree assumption.

Construct a finite multigraph H as follows. Every alpha contributes one edge
with its two terminal incidences. A terminal with a port attaches to that
port's BB--TT component, retaining a balanced component as a **zero-capacity**
vertex. A terminal without a port attaches to a new private zero-capacity
dummy vertex; different missing terminals receive different dummies. All
positive original interval vertices are retained, including isolated ones.
Loops and parallel edges retain multiplicity.

Every physical interval has at most two incidences. A port is a BB end of its
interval and can be used only by the unique immediately exterior TP column
on that side. A loop consumes both incidences, not two resources. Balanced
intervals and dummies have degree at most one. Therefore H has maximum degree
two, and all zero vertices are ends of path components. Each component is
a path (possibly isolated) or a cycle. Cycles have no zero vertices.

Write z_C for the number of zero vertices in a path component C, so
z_C in {0,1,2}. Let h be the total number of zero **incidences**; an unused
balanced boundary interval contributes no incidence and may be omitted.
Let d4 count occupied-degree-four original alpha terminals, and let b count
the other zero incidences: missing physical ports at lateral boundary terminals
and ports entering balanced boundary intervals. Then exactly

    h = d4 + b.

These counts concern alpha terminals, not all degree-four endpoints in P.

## 2. Exact port allocation, including every missing terminal

A port allocation assigns an alpha edge to one of its positive endpoint
vertices, injectively. It is a legal zero-link payment using the original
interval at that terminal. Let k be the alpha count and D0 the number of path
components having two zero ends. Then

    V_port = k - D0,                 2 D0 <= d4 + b.       (1)

Proof. List a path's vertices v0,...,vm and edges e1,...,em, with ei between
v(i-1),vi. With no zero vertex, assign ei to vi. With only v0 zero use the
same assignment; with only vm zero assign ei to v(i-1). With both ends zero,
leave e1 unpaid and assign ei to v(i-1) for i=2,...,m. This pays exactly m-1;
only m-1 positive vertices exist, so no port allocation can pay more. An
isolated vertex contributes no edge or deficit. For a cycle, orient it
cyclically and assign each edge its head. This also covers a loop and two
parallel edges. Different components have different physical resource
vertices. These assignments prove (1) without spending any interval twice.
Each deficient path contains two different zero incidences, proving the bound.

This is the exact optimum of the stated port relation. Whole-body support,
cap access, mixed relays or betas can improve it. An unpaid port edge alone
is not a full-network or numerical counterexample.

**Automatic full-pool corollary.** Suppose b=0 and d4<=1. Then every alpha is
paid by a different original interval, at zero links. In particular this
holds when all alpha terminals have degree three and b=0. It requires neither
unique matching nor freezing, and permits arbitrary interior degree-four
vertices that are not alpha terminals.

The established standard packet boundaries (first column BB, last column
containing a blank in each band) imply b=0: no alpha terminal is a lateral
boundary column, and neither end is TT, so all forests are positive units.
Blank lateral boundary columns are a sufficient special case. More generally
one may check b=0 directly. Positive boundary-marked units must remain available.

For the exact-degree-three beta-core switch problem this settles the complete
pool on all such packets before any switch is made: V=k and minimum link
count is zero. Root directions cannot increase a value already equal to k.
For arbitrary rectangles the reduction leaves explicit zero-to-zero boundary
paths; it does not prove that freezing excludes or repairs them.

## 3. Exact simultaneous withdrawal profile

Keep the original graph and remove an arbitrary set R of distinct positive
interval identities. Let r_C be its number in component C. The exact new
port deficit is

    D(R) = sum_(cycles C) r_C
           + sum_(paths C) max(0, z_C + r_C - 1).       (2)

In particular

    D(R) <= D0 + |R| <= floor((d4+b)/2) + |R|.         (3)

For a defect-free packet (d4=b=0), a path tolerates its first withdrawn unit
for free, while a cycle loses one payment per withdrawn unit. Even if two
ports of one alpha meet the same original interval, withdrawing that one
unit is counted once. Equation (2) treats simultaneous withdrawals in one
component jointly, rather than summing independent local losses.

Proof. In a cycle with m vertices/edges, its m-r_C remaining positive vertices
can each be assigned a distinct incident edge by the original cyclic
orientation; reverse this injection to pay that many edges. Resource count
is an upper bound. In a path let w=z_C+r_C be its final number of zero
vertices, including internal withdrawn vertices. If w=0 use the full path
assignment. If w>=1 root the underlying path at any zero vertex, orient edges
away from it, and assign each remaining positive vertex its unique parent
edge. The assigned edges are different. There are m+1-w such vertices, at
most m, and resource count again gives optimality. This proves (2), including
an isolated interval. Per path, max(0,z+r-1)<=max(0,z-1)+r; cycles have initial
deficit zero. Sum to obtain (3). All allocations use actual incident units;
no beta credit has been spent. QED.

## 4. A coefficient-one criterion and its exact scope

Let L be the complete original positive interval count and beta the original
BP--BP path count. The original terminal ledger on the rectangle is

    S = area/2 - |T| - |M| = L + beta - k.

Balanced boundary forests contribute zero to L and to BB-TT. A port allocation
of k-D0 different intervals proves L>=k-D0. Hence

    S >= beta-D0 >= beta-floor((d4+b)/2).                (4)

Consequently d4+b<=2 beta+1 suffices for

    |T| + |M| <= area/2.                                (5)

Under standard packet boundaries, all alpha terminals of degree three imply
the stronger S>=beta. This is a concrete coefficient-one subclass, replacing
the 5/6 matching coefficient there; it does not improve 5/6 universally.
No geometric component decomposition, unique-square assumption or bounded
number of bends is imposed. The beta in (4) is the unused original ledger
credit; it has not also been allocated as a payment resource. For a subpacket,
one must still close the actual matching and use the existing outside ledger;
this note does not remove receiver-overlap or packet-boundary terms.

## 5. Validation and relationship to the previous obstructions

The checker independently extracts positive and balanced forests, counts
physical port incidences, constructs H with actual alpha identities, and
compares (1)--(2) to bipartite augmentation and, on small controls, exhaustive
assignments. It checks the exact original ledger (4) and compares the port
lower bound to the whole-support fork optimum. Raw boundary defects are
retained, and withdrawn physical identities are shared globally.

The earlier full-pool singleton obstruction has degree-four alpha terminals;
it is outside the defect-free corollary. The frozen missing-port family has
one alpha and two degree-four terminals per copy. It attains D0=d4/2 in the
port relation, proving the factor one-half sharp for that certificate. This
does not assert sharpness of the whole-support deficit on that family.
The frozen two-edge connector cycle has degree-three alpha terminals and
two different shared units. Both sources pay simultaneously; reserving one
of those units produces exactly one unpaid port edge. Its interior degree-four
vertices do not invalidate the new terminal-only corollary.

The permanent run passes 1180 physical models (including 76 degree-three
selection extensions), 4720 simultaneous withdrawal profiles, 4624 independent
exhaustive physical port optima and 4576 whole-fork lower-bound comparisons.
There are 250 nonvacuous automatic full-pool controls, four sharp frozen
half-tax controls and two shared-cycle single-withdrawal controls. The raw
boundary adapter retains two actual zero incidences in selection extensions;
neither causes a deficit alone. Separately, 735 abstract port multigraphs
with loops/parallel edges give 5227 exhaustive withdrawal optima. The 448
independent rank events check selected inherited frozen controls, not every
model in the census. Local Lean4.33.0 passes 16 declarations/axiom audits,
without warnings, sorry, native evaluation or new axioms.

Reproduce with:

    python3 develop/check_terminal_defect_port_compensation.py --output output/terminal-defect-port-compensation-validation.json
    python3 develop/check_terminal_defect_port_compensation_formal.py --lean /path/to/lean-4.33.0 --output output/terminal-defect-port-compensation-formal-validation.json

Permanent evidence: [physical and abstract checker](../develop/check_terminal_defect_port_compensation.py),
[Lean source](../formal/SubQuorum/TerminalDefectPortCompensation.lean),
[physical receipt](../output/terminal-defect-port-compensation-validation.json),
[formal receipt](../output/terminal-defect-port-compensation-formal-validation.json).

Finite searches and existing-family censuses motivated the result; the proofs
above are independent of their bounds. Lean verifies the explicit path/cycle
allocation indices and finite inventory/withdrawal arithmetic. The arbitrary
grid-to-graph adapter, graph classification and full physical conclusion are
written proofs, not an end-to-end Lean theorem. See the accompanying saved
validation receipts for executed scope. Manuscripts and correspondence are
unchanged.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
