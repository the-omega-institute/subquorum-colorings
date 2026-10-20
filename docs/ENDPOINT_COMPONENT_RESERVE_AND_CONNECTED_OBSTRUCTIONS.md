# Endpoint components localize reserve and the remaining obstruction

20 October 2026. In the complete-source model, every final endpoint
component is itself a complete feasible source fusion. The event reserve,
actual marks and seven defects restrict additively to these components.
Consequently defect parity is available separately on actual endpoint
components. It is not available separately on arbitrary source groups.
This gives a new nonzero-reserve count and confines the first shared
parity obstruction to a single endpoint component.

## 1. Complete-source assumptions and the partition

Use the same finite complete U/rotor source model as
EXACT_GEOMETRIC_EVENT_RESERVE.md. Original endpoint sets P_i are disjoint;
P and M are their original unions. Every original support T_i outside P
is retained. Every final selected vertex has at most one occupied neighbor.
Each source P_i is connected in the lattice graph, every original support
has exactly one original endpoint anchor, and every original endpoint has
original occupied degree three. These are properties of the complete U
and rotor constructors, including all allowed dimensions and isometries.
Original occupied vertices remain occupied after fusion. Optional extra
selections have no endpoint neighbors and lie outside original receivers;
they have no effect on the source counts considered below.

Let C_j be the connected components of the lattice graph induced by
final P. These are ENDPOINT components. They are not arbitrary residual
tile components, subsets of a contact graph, or a proposed partition of
the positive sources. Connectedness assigns every complete original
source to one and only one C_j. Let I_j be its set of source indices.

**Restriction lemma.** The subfamily indexed by I_j, with its original
supports and matching, is a complete feasible fusion whose endpoint set
is C_j. Original events and actual canonical side marks are unchanged.

**Proof.** Original source connectedness puts all of P_i in C_j. For
an original support x of such a source choose its endpoint anchor p in
P_i. If x is consumed into final P, then the edge xp puts x in C_j.
In particular consumption cannot be caused by a source outside I_j.
If x is not consumed, it is retained and already has occupied neighbor
p. Feasibility forbids any second occupied neighbor. Thus x has no
neighbor in another endpoint component, and no retained support from
another component can be adjacent to it. If the same support belonged
to two components, its two distinct endpoint anchors would violate the
same condition, unless it were consumed, which already joins them.

Therefore restriction retains exactly the support-consumption relations
of this subfamily and remains feasible. Every matching edge stays in
its original complete source. An intratile event has two adjacent final
endpoints, so its target stays in the same component. For a canonical
positive side, its endpoint protectors have no occupied neighbor removed
by restriction: any endpoint neighbor is in C_j, and a retained support
neighbor is anchored in C_j. Extra selections have no endpoint neighbor.
Their occupied degrees, and hence actual side marks, are unchanged.
This proves the lemma.

## 2. Tiles and exact additivity

Every nonempty final endpoint tile has a connected endpoint set. The
only disconnected nonempty subset of a square is a diagonal pair. If
a tile contained exactly that pair, either remaining corner, if selected,
would have two endpoint neighbors. Both corners are therefore blank.
Each diagonal endpoint would then have at most its two neighbors outside
the tile occupied. This contradicts its final occupied degree at least
three, inherited from the original complete source. Thus a physical tile
with endpoints belongs to exactly one C_j.

Let R_j=S_j+C_j^credit-Kirregular,j be the reserve computed by the SAME
original ledger on the restricted subfamily. The superscript on the
credit distinguishes it from the endpoint set C_j. Let n0_j,n1_j,n2_j
be its zero-, one- and two-mark positive counts, and L_j its positive
dimension-exception count from the multiple-positive note:

    w!=6 and (w>=12 or max(a,b)>=8).

Original negative mass is additive by sources. Events are additive by
their original endpoint owner and adjacent endpoint target. Every new
full tile belongs to one endpoint component, and the original full-tile
status is unchanged by restriction. Hence regular events and the actual
credit 2J-Kregular are additive. Canonical marks are unchanged by the
restriction lemma. Therefore

    R=sum_j R_j,  G=sum_j G_j,
    n0=sum_j n0_j, n1=sum_j n1_j, n2=sum_j n2_j.     (1)

The exact seven-count theorem applies to each complete restricted fusion:

    D_j=A_j+U0_j+Z0_j+L1_j+2L2bar_j
                          +2L2mutual_j+L3_j=2R_j>=0. (2)

Its source-labelled occurrences and nonfull tile defects restrict to the
same unique endpoint component. Activation consumes a support adjacent
to its original endpoint anchor, so also stays within that component.
Triple filling cannot cross components, since a full tile is connected.
Thus D=sum_j D_j as geometric counts, not merely as a formal difference.
In particular EVERY D_j is even and EVERY R_j is a nonnegative integer.

No ambient slack from separate bounding rectangles is added here. Such
rectangles could overlap and each would include its own half-area. We
sum only the original source-ledger margins from (1), then apply the
one global ambient ledger once:

    sigma >= N+R-G = sum_j(n0_j+R_j-n2_j).          (3)

## 3. One reserve unit per qualifying endpoint component

Let b_j count nonexceptional doubly marked positive sources in C_j, and
let q count endpoint components with b_j>0. This uses their actual source
labels, so it can be stronger than counting only components with n2_j>L_j.
The preceding multiple-positive zero-reserve theorem applies to every
restricted fusion:

    R_j=0 implies b_j=0 and n2_j<=L_j.

Consequently each of the q components has R_j>0 and therefore R_j>=1.
All other reserves are nonnegative. Equations (1)--(3) give the new bound

    R>=q,
    sigma>=n0-n2+q.                                (4)

It follows that

    n2-n0<=q                                       (5)

is sufficient for joint allocation, with arbitrary positive counts,
negative source dimensions and rotor phases. Exceptional positive sources
are allowed in the same components. This condition
uses one reserve unit in each of q DIFFERENT endpoint components. It
does not round an arbitrary defect subtotal, spend a source twice, or
assume each double mark has a separate component.

For example, when L=0, q is exactly the number of endpoint components
containing at least one doubly marked positive source. Thus (5) proves
the allocation at ALL reserve values if each component has at most one
doubly marked positive source. Components can contain arbitrarily many
other positive sources. More generally (5) permits excess demands in one
component to be offset by unmarked sources in other components.

This is a sufficient geometric count, not the unrestricted inequality:
several doubly marked sources in the SAME endpoint component may still
share only one reserve unit. The full target remains
2(n2-n0)<=D, without the component-count restriction (5).
Whenever (5) holds, the resulting coefficient-one inequality
|T|+|M|<=mn/2 strengthens the existing 5/6 matching-coefficient bound by
|M|/6 in its left-hand coefficient. This comparison applies to the
specified complete-source class; no arbitrary-grid decomposition is proved.

## 4. Connected obstruction and the first positive-reserve case

If the global allocation margin is negative, (3) implies that at least
one endpoint component has negative source margin. Its restriction is
a COMPLETE feasible fusion with that same negative margin. Thus any
counterexample to the allocation has an endpoint-connected counterexample
inside it. This does not assert that a counterexample actually exists,
nor that a negative source margin makes ambient sigma negative.

Suppose every positive has nonexceptional dimensions (width6 with
arbitrary even heights, or width8/10 with both heights4/6). A failing
component cannot have R_j=0 by the preceding saturation theorem. Hence

    R_j>=1 and n2_j>=n0_j+R_j+1>=n0_j+2.           (6)

In particular a failing component contains at least two doubly marked
positive sources. The remaining research must address their simultaneous
geometry within one component; splitting them without proof would spend
parity twice.

In the especially focused candidate n0=0,n2=2,R=1 with L=0, (4) gives
q<=1, while the two double marks give q>=1. They MUST lie in the same
endpoint component. Since the nonnegative D_j are even and sum to2,
all geometric defects also lie in that unique component with R_j=1.
All other components have zero reserve and no double marks. Restricting
to that component preserves n2=2,R=1 and a negative allocation margin.
Thus the two isolated one-defect pieces from the arithmetic illustration
cannot be realized as two separate endpoint components in this class.

The remaining D_j=2 possibilities are exactly one weight-two occurrence
(L2bar or L2mutual), or two weight-one occurrences among A,U0,Z0,L1,L3,
with repetitions allowed in the latter list. These alternatives follow
from the exact nonnegative identity. They do not demonstrate physical
realizability or exclude any of the connected alternatives.

## 5. Checks and formal scope

develop/check_endpoint_component_reserve.py reconstructs the actual
endpoint components, assigns each whole source, checks original anchors
and endpoint degree, restricts the complete physical fusions and compares
every source/mark/reserve/defect count with its global counterpart.
Separated copies of marked opposed-band chambers provide controls with
several qualifying components and positive reserves. They do not realize
the connected low-reserve obstruction.

formal/SubQuorum/EndpointComponentReserve.lean checks the finite-list
nonnegative integer reserve count, exact sum of margins, the sufficient
joint criterion, the connected negative-margin reduction and the
single-reserve concentration. Physical source connectedness, retained
support restriction, tile connectivity and ledger adapters are proved
in Sections1--2 and remain written. No arbitrary-grid formal theorem is
claimed. Finite controls do not replace those universal arguments.

Controls PASS on664 physical images and752 complete restricted endpoint
components, including24 images with2,4or8 qualifying components at positive
reserve. All13 scoped Lean declarations compile locally with Lean4.33.0,
and every individual axiom audit passes without sorryAx/native_decide.
See output/endpoint-component-reserve-controls.json and
output/endpoint-component-reserve-formal-check.json. The preceding
multiple-positive review82dc60f9 completed ACCEPT; this new restriction
and nonzero-reserve theorem has its own pending independent review,
original taskc04f8615 in conv_68f343f25e429e97 on stream77960. The
preceding acceptance is not inherited as a verdict for this theorem.

Unrestricted mixed allocation, connected two-demand low-defect geometry,
and arbitrary rectangular-grid triple equality remain open.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
