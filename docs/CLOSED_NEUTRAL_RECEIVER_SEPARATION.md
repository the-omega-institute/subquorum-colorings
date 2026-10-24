# Distinct forced receivers around closed neutral U-port components

20 October2026. This strengthens the distinct-support theorem to a count of
disjoint physical receivers. It applies to arbitrary complete finite permitted
sources, with no size bound or source-freshness assumption. Unrestricted
coefficient-one allocation and rectangular-grid triple equality remain OPEN.

## 1. Setting and notation

Use all hypotheses and notation of
[the distinct-support theorem](DISTINCT_NEUTRAL_SUPPORTS_AND_ANY_PAIR_BUDGET.md).
Choose any collection of closed components of the specified neutral U-port
graph. Let C01 be its neutral phase01-to-phase01 contact count, and let Pclosed
be the union of ORIGINAL endpoint sets of every phase01 owner in the chosen
closed components. The stronger established exclusion from all closed phase01
owners, including unchosen closed components, is available too.

At such a contact, orient from active p to passive p+d and let s be the active
predecessor direction. Its forced point is z=p+s+d. Its fixed physical receiver
Q contains the active owner's exact original regular pair p+s,p+2s, the forced
endpoint z, and the fourth point w=z+s. All these coordinates refer to the
transported original tile partition. Write Jc for the number of these receivers
that are nonfull. This is a subset of the earlier J01 stops over ALL contacts.

## 2. The receiving physical tiles are distinct, including full ones

Suppose two contacts in the chosen closed collection have the same Q. If their
active original owners differ, their original regular pairs are disjoint. Both
pairs lie in a four-point tile, so together they fill Q. In particular the first
forced point z, which is outside its own active pair, belongs to the other
active owner's original pair. That owner is a phase01 owner on a closed port
component. This contradicts the established exclusion z outside Pclosed.

If the active owners agree, the contacts either use the same terminal or its
other terminal. A terminal has a unique partner in its actual neutral receiver,
so the first case identifies the same contact. In the second case the two
predecessor regular pairs lie on the two different original stems. They have
distinct physical receivers, since the source's even width is at least six.
Thus contact-to-Q is injective for the chosen closed collection.

The endpoint-owner exclusion is essential here. The preceding proof for J01
alone used nonfullness to separate pairs; that argument does not justify
receiver injection over arbitrary open contacts. No such extension is claimed.

## 3. A full receiver requires two endpoints outside all closed phase01 owners

The forced endpoint z already avoids every closed phase01 owner. Suppose Q is
full, so w is also an original endpoint. If w belonged to a closed phase01
owner F, its original endpoint profile in Q has size one, two or four. These
are the only phase01 U profiles: terminal1P1T, stem2P1T and bar4P0T.

An original full profile overlaps the active pair, impossible for a different
owner. An original pair is connected; avoiding both active endpoints forces
it to be exactly the opposite pair {z,w}. This gives F ownership of z, already
excluded. An original singleton is a terminal of F. But both terminals of a
closed phase01 owner have actual neutral receivers with exactly two endpoints;
they cannot lie in the full Q. These exhaust the catalogue, so w also avoids
every closed phase01 owner.

F cannot be the active owner: its exact original profile in Q has only the two
predecessor endpoints. This also excludes an overlooked same-owner case.

Let X be the union, over these receiving tiles Q, of their final endpoints
outside their own active original pair. Since different aligned physical
tiles are disjoint, all points in this union are distinct. Each nonfull tile
contributes z alone and every full tile contributes z,w. Consequently

    |X| = 2*C01-Jc,    X intersection Pclosed = empty.              (1)

The exclusion holds against the larger union of ALL closed phase01 owners
as well. In particular the number of endpoints outside that union is at least
2*C01-Jc. These positions may belong to recurring phase10, other phase01,
phase11, positive or rotor owners. Equation(1) does not count fresh owners.
Each point of X is adjacent to one of its active predecessor pair's endpoints.
It is therefore in the SAME full endpoint component as that contact. Restricting
the chosen curves to a component c also restricts all these outside endpoints
to c; no endpoints from unrelated full endpoint components supply the count.

## 4. Shared defect and AA consequences

Because Jc is a subset of J01, the established simultaneous stop budget gives

    B+Jc <= 2*A+H.                                                (2)

Combining the EXACT count in(1) with(2) yields

    |X|+2*A+H >= 2*C01+B.                                        (3)

This is one inequality derived from a common H pool. It is not an additional
payment to add to a reserve estimate, and a full receiver creates no H unit.
For any chosen union of closed components of the specified port graph, without
imposing AA, edge-incidence counting gives

    C01-C10 = M01-M10,                                           (4)

where C10 counts neutral edges with two phase10 owners. Both contact types
count edges, including legitimate parallel edges, once. Mixed edges cancel
when subtracting total phase incidences. Equation(4) is valid without AA.
For a general degree-at-most-two port graph that includes open components,
let U01,U10 count unused ports of the two phases. The corresponding identity is

    2*(C01-C10)=2*(M01-M10)-(U01-U10).

It follows by subtracting2*M01=2*C01+Cmix+U01 and its phase10 counterpart.
An isolated phase01 owner already shows why its unused ports cannot be omitted.

In ONE fixed full endpoint component satisfying the established nonexceptional
AA hypotheses, every phase10 owner on a closed port component is double-active.
Hence C10=0, C01=M01-M10>=4*ell, and H=0 implies Jc=0. Therefore

    |X| = 2*(M01-M10) >= 8*ell.                                  (5)

Thus every AA closed neutral component requires at least eight DISTINCT
original endpoint positions outside all closed phase01 owners. This doubles
the earlier four-forced-point conclusion. All counts used with AA are
restricted to that same endpoint component; no unrelated component census
is imported. Distinct receiving tiles and endpoint positions still do not
show these positions supply additional reserve.

## 5. Verification boundary and remaining problem

The proof uses the previous direction-tag injection and owner exclusion,
the original phase01 profile catalogue, elementary packing of a four-point
tile, stem separation, and exact edge incidences. It requires no enumeration
over placements. The finite adjacent-pair catalogue and conditional list/count
deductions have a scoped Lean companion. The physical profile/port adapters
remain written. The independent review of the preceding distinct-support
theorem does not automatically cover this later receiver theorem.

Controls must report actual contact coverage separately: existing complete
closed components have no phase01-to-phase01 edges, so their new collar count
is zero. The four01 partial polygon has four different receiving tiles and
eight geometrically prescribed opposite positions, but its forced supports
are infeasible. It is not a complete feasible AA realization or a counterexample.

The remaining full finite closure must bound these outside endpoint resources
using original owners and the same reserve ledger, allowing owner recurrence,
full2+2 receivers and rotor exits. No arbitrary-grid bound or uniform coefficient
improvement follows solely from the new endpoint count.

Independent reviewff4d49b9 completed ACCEPT at08:29:24.752UTC, observed gpt_6/pro,
for the closed-component receiver theorem and its same-component AA consequence.
The scope correction from arbitrary port graphs to chosen closed unions is
incorporated above, with the exact unused-port formula for open components.
The review independently checks the needed support-injection/whole-owner
dependency; it does not certify executions or later phase10 exit results.
Its original stream15913 transport and same-task response comparison are
recorded in the separate review receipt.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
