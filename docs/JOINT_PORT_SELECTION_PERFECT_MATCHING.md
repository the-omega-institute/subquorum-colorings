# Joint port and resource selection as a perfect-matching problem

23 October 2026. Authors: Haobo Ma and Wenlin Zhang.

The full-domain compensation interface need not fix source endpoints before
searching. An exact finite graph encoding jointly chooses sources, their
ends, different beta resources, and optional whole mixed relays, while
retaining every PP coverage. It also preserves arbitrary additive costs
of the auxiliary matching. The encoding solves coverage and resource
capacity; coherence remains a separate required certificate.

## 1. Exact coverage problem

Let W be the set of old A-covered PP vertices. Its old matching A is fixed
for cost comparisons, but its edges may all be replaced. Let the following
two-port groups be pairwise disjoint and disjoint from W:

- source groups: the two free ends of each eligible unpaid original alpha;
- resource groups: the two free ends of each original beta;
- relay groups: the TP and BP free ends of each original mixed path.

Other original free ends, including old paid-alpha witnesses, are excluded
from the auxiliary candidate graph. All such ends remain free. Let E be any
declared permitted edge relation on W and the listed ports. Choose a number r.

An admissible auxiliary matching N must cover every vertex of W, exactly one
port in each of r different source groups and r different resource groups,
and either both or neither port of every relay group. It covers no other
port. In particular one beta cannot be used twice through its two ends.
No path-owner capacity or protected-tail condition is imposed internally.
An N component is not required to pair a preassigned source with a resource.

## 2. Selector graph and exact reduction

Start with all vertices of W and all ports, and insert every edge of E.
Add r source-slot vertices and r resource-slot vertices.

For each source or resource group with ports p_0,p_1, add two selector
vertices o,h. Insert the four edges from {o,h} to {p_0,p_1}. Connect o to
every slot of its own category; h has no slot neighbour.

For each mixed relay with ports q_0,q_1, add vertices x,y and the three
edges q_0--x, x--y, y--q_1. All selectors, slots and relay vertices are
new, distinct accounting vertices. Call the resulting graph G_r.

**Exact selection theorem.** G_r has a perfect matching if and only if an
admissible N exists. Projecting a perfect matching onto its E edges gives
an admissible N; every admissible N has a perfect-matching lift. If the
E edges carry arbitrary nonnegative weights and all other edges have weight
zero, the projection preserves cost and the minimum costs agree.

### Proof

The holding selector h must match one group port. If o matches a slot,
the other port cannot match locally and must be covered by one E edge.
Thus exactly one port is active. If o does not match a slot, it must match
the other port, so neither port is active. Both ports can never be active:
h would have no available neighbour. Every slot is matched to one distinct
o, so exactly r groups of each category are active.

In a relay gadget, matching x to y forces both relay ports to use E edges.
If x is not matched to y, it must match q_0, and y must match q_1; then
neither relay port uses E. A one-active-port state is impossible. Every
PP vertex has only E neighbours and is therefore covered by the projection.
The E edges of a perfect matching are themselves a matching, proving the
forward direction.

Conversely, start with an admissible N. Match the open selectors of the
r active source groups bijectively to the source slots, and do the same
for active resources. In every active group match h to its inactive port.
In an inactive group match o to p_0 and h to p_1. For an active relay use
x--y; for an inactive relay use q_0--x and y--q_1. Along with N, these
edges cover every vertex once. They belong to G_r and give the desired
perfect matching. Its only weighted edges are the edges of N. QED.

For the repair cost set w(e)=0 for e in A and w(e)=1 otherwise. Then the
minimum-weight perfect matching minimizes |N setminus A| jointly over
source ends, different resources, optional mixed states and internal PP
reconnections. The proof is a reduction to the standard general-graph
perfect-matching problem; the finite checker uses exhaustive matching
enumeration only on small controls and is not a scalable blossom solver.

The standard Tutte criterion supplies an exact coverage obstruction:
G_r has no perfect matching precisely when some vertex set Z leaves more
odd components in G_r minus Z than |Z|. This is a criterion for the defined
coverage problem. It is not a geometric proof that the criterion always
holds on grid-derived inputs.

## 3. Relation to the compensation proof

After projection, the selected source and resource ports and the active
relay states determine the full-domain open-path signs. Original cycles
retain their flip freedom. Apply the balanced mixed-port transfer theorem:

    delta_N <= delta_old-r+h,

where h counts negative same-sign N edges in an allowed signing. Old backed
payments transfer at their surviving endpoints, with distinct original
units. If a coherent signing exists, h=0. Slots and selectors do not supply
payments and are removed before this signed-graph argument.

**Perfect-matching feasibility alone does not imply coherence or compensation.**
The eight-endpoint open-relay obstruction illustrates this exactly. Its actual
edges are t--t', p--p', q_T--x, y--q_B and A={x--y}. The source group is
{t,t'}, resource group {p,p'}, mixed group {q_T,q_B}. With
E={x--y,t--x,y--p}, G_1 has a perfect matching projecting to
N={t--x,y--p}, with the mixed relay inactive. Nevertheless the final actual/N
graph has an alpha and a beta. Its two inserted edges are same-sign, h=1,
and the deficit bound is 1<=1-1+1. There is no cycle flip to fix them.

Thus the reduction removes arbitrary port choices and resource double use
from coverage search, but the sign obstruction is retained explicitly.
One may search different perfect matchings or open-path states and then
audit their grounded cycle constraints. No polynomial-time optimization
over all coherent states is claimed here.

## 4. Original interval units can be represented once

Let J be a subset of original unmarked interval units, disjoint from all
old backed payments that are being retained. For each unit j in J, add a
formal two-vertex beta edge to the accounting actual matching, give its
ends BP labels, and make those two ends one resource group. Permit an
access edge to such a port only when its original physical endpoint has
the stated access certificate to that specific interval identity.

In the extended accounting graph use b'=b+|J| and I'=I setminus J. Then

    |I'|+b'-k=|I|+b-k.

The physical actual matching and selections remain unchanged; the new edge
is a formal representative of an already existing interval unit. Its
resource gadget allows at most one of its ends to become auxiliary-covered.
The same interval cannot also remain in I', be used as another formal beta,
or back an old payment. Hence its credit is represented once.

This adapter requires the interval identities and access certificates as
input. It does not assert a new universal grid access relation. Once those
inputs are supplied, the perfect-matching reduction and balanced incidence
proof apply to the extended finite accounting graph without alteration.
This is different from labelling an opened PP cycle a donor: no new credit
is created, and the exact physical scalar ledger is preserved.

## 5. Scope and validation

The checker compares the complete set of projected selector-graph perfect
matchings with an independent direct enumeration of the coverage definition
on 1,368 finite candidate models. The per-model projected sets agree in every
case, totaling 3,456 modeled replacement occurrences and 9,723 selector
perfect matchings; 208 models are infeasible on both sides. These totals
sum occurrences across models, not globally distinct graphs or resources.
It checks reverse lifts, cost preservation,
one-port source/resource capacities, and both-or-neither relay states.
It includes a shared-beta collision despite individually feasible sources,
a successful joint choice that avoids a greedy endpoint conflict, the
noncoherent open-relay example, three lifts of real seven-edge grid repairs,
and an interval-virtualization example retaining a separate backed payment.

The general equivalence is proved above; enumeration does not replace it.
No global grid bound, universal coherent existence, scalable solver
implementation or full Lean matching formalization is claimed. The record is
`output/joint-port-selection-matching-validation.json`.

    PYTHONDONTWRITEBYTECODE=1 python3 develop/check_joint_port_selection_matching.py --output output/joint-port-selection-matching-validation.json

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
