# Distinct neutral-contact supports and a joint budget for all original pairs

20 October 2026. This resolves the forced-point repetition question left in
NEUTRAL_U_PORT_TURNING_AND_SHARED_BUDGET.md. Distinct neutral01 contacts force
distinct original endpoint positions, even across different port components.
An additional shared defect budget and a broader cap reservation count retain
this information without treating endpoints or full tiles as fresh reserve.
Unrestricted finite complete-source coefficient one and rectangular-grid triple
equality remain OPEN; full receiver, rotor and open-path exits still need closure.

## 1. Assumptions and the forced point

Use the complete finite U/rotor source model, legal arbitrary even dimensions,
original endpoint disjointness and matching ownership, mandatory support retention,
fixed transported physical tiles and selected occupied degree at most one from
the preceding notes. Optional selections cannot be placed inside an original
receiver or next to an endpoint. No acyclicity, source-count bound or owner
freshness assumption is imposed.

Consider every actual neutral edge between two original phase01 U terminal
singleton ports, whether on a closed component or an open path. Orient it from
its active port p to its passive port q=p+d. Write s for the active source's
terminal predecessor direction. Then s,d are perpendicular cardinal vectors,
the passive source's predecessor direction is d, and its blank direction is -s.

The point z=p+s+d is an original support of both sources. Its two persistent
anchors are p+s and q. Support retention therefore forces z into P, owned by
neither incident original source. This was the preceding continuation lemma.

The following stronger theorem does not require final feasibility beyond the
existence of the two contacts: different neutral01 contacts have different z.
Its geometric input is only complete original U terminal geometry and original
endpoint disjointness. In particular it does not depend on an AA census.

## 2. A direction tag proves global forced-point injection

Both terminals of an original U point toward its bar in the SAME directed
cardinal direction, even when their heights differ. Tag every endpoint of each
original phase01 U by that direction. Endpoint disjointness makes these tags
consistent. If two original endpoint stencils overlap with different direction
tags, their original owners must differ, which contradicts endpoint disjointness.
This allows recurring owners at different contacts; it does not assume freshness.

Suppose two contacts force the same z. Normalize that point to0 and the first
frame to s=N=(-1,0), d=E=(0,1). This normalization concerns lattice geometry;
the physical tile partition is transported and not reset. The first active
owner has the three mandatory endpoints

    p=(1,-1), p+s=(0,-1), p+2s=(-1,-1), all tagged N.

The last point exists because the legal incident height is at least four.
For any second frame (s',d'), its active owner has endpoints

    -s'-d', -d', s'-d', tagged s',

and its passive owner has endpoints -s', -s'+d', tagged d'. These are fixed
minimum terminal stencils, present at arbitrary legal widths/heights.
There are exactly eight perpendicular cardinal frames. The seven different
ones conflict with the first stencil as follows; the remaining frame is (N,E).

| Second frame | Second owner | Shared endpoint | First tag | Second tag |
|---|---|---|---|---|
| (S,E) | active | (0,-1) | N | S |
| (S,W) | passive | (-1,-1) | N | W |
| (E,S) | active | (-1,-1) | N | E |
| (E,N) | active | (1,-1) | N | E |
| (N,W) | passive | (1,-1) | N | W |
| (W,S) | active | (-1,-1) | N | W |
| (W,N) | active | (1,-1) | N | W |

This is an exhaustive proof over orientations, not a bounded search over source
dimensions or placements. Lean checks both the exact eight-frame exhaustion and
the universal implication from endpoint direction tags to equality of frames.

Equal z and equal frames give the same active point p=z-s-d and passive point
q=z-s. Original ownership and the fixed neutral receiver then identify the same
contact. This proves injection for ALL neutral01 contacts simultaneously. Write
Z01 for their forced-point set. Its cardinality equals their contact count.

## 3. The forced endpoints cannot belong to a closed phase01 owner

The physical tile Q containing z also contains the active owner's original
regular pair p+s,p+2s and original support z. Its fourth point is z+s.
It is therefore an exact original2P1T receiver, with at least three final
endpoints. The original neutral contact lies in the neighboring tile.

Let F be the original owner of z. It cannot be the active or passive source.
The west and south neighbors of z in the normalized frame are foreign endpoints.
If F is a U, a nonterminal stem point has two opposite own neighbors and cannot
avoid both foreign directions. Interior/lower bar roles have three own neighbors
and also fail. If F has phase01, its bar receiver is an original full4P0T tile,
so even an upper outer corner would overlap the active owner's pair in Q.
Consequently a phase01 F must have z as an original terminal singleton.

A phase01 owner on ANY closed specified port component has both terminal tiles
actual neutral2P1T with exactly two endpoints. Q has at least three endpoints.
Thus F cannot be such an owner. This exclusion holds without H=0, including
closed port components other than the one producing the contact.

In the AA situation of the preceding turning theorem, the number of neutral01
edges on the ell closed components is M01-M10>=4ell. Hence at least4ell DISTINCT
original endpoints are forced outside all original phase01 owners on those
closed components. They may belong to phase10 owners on those components or to
other original sources. Distinct points do not imply distinct owners or payments.

## 4. Nonfull regular stops use capacity disjoint from the corner stops

If Q is nonfull, its endpoints are exactly the active owner's pair plus z.
Its missing corner neighbors two persistent endpoints and cannot be selected.
Thus Q is an actual mixed3P0T tile and contributes one L3 unit to H. If H=0,
Q is necessarily full and z+s is another original endpoint. Fullness itself
is not a new compensation unit.

Let J01 count these nonfull Q stops over all neutral01 contacts. They are
distinct physical tiles. If two stops had different original active owners,
their two disjoint original pairs would make a shared tile full. If their
active owner were the same, different legs have different receivers; a fixed
pair has only one original support z, and the forced-point injection excludes
two different contacts at that z.

Keep D,C0,C1,E1 from the accepted passive-corner proof, with

    B=D+C0+C1+E1, C1<=A, E1<=A.

A D stop contains an original negative phase10 irregular pair. A C0 stop
contains an original positive regular pair. A J01 stop contains an original
negative phase01 regular pair. These pairs belong to distinct original owners
across the three classes. Any coincident nonfull tiles would contain two
disjoint original pairs and hence be full. Therefore the simultaneous bound is

    D+C0+J01<=H, B+J01<=2A+H.                       (1)

This strengthens the previous B bound using one common H pool. It is not an
additional reserve estimate to add to an old bound. Separation from every older
z/r/Y witness family is not claimed here. Substituting into the turning bound
for the same source collection gives

    4ell+M10+2J01 <= M01+4A+2H.                     (2)

Within the fixed AA full endpoint component c, H_c=0, so D_c=C0_c=J01_c=0.
The remaining forced receivers in c are full and their next points still
require a nonreused continuation.

## 5. Reserve U singleton slots beside ANY exact original pair

Keep the U-only pool Pneg of original phase01 terminal and phase10 outer-corner
singleton endpoints, with |Pneg|=2K01+2K10. Rotor singleton endpoints remain
excluded. Define disjoint endpoint sets, counting each point once:

    E0: points in Pneg whose tile contains a foreign exact2P0T profile;
    E1reg: points in Pneg whose tile contains a foreign exact2P1T profile;
    Eany=E0 union E1reg, eany=|Eany|.

E0 is the preceding sharp Epair set. The complete profile catalogue has no other
original two-endpoint profile. A singleton's three other tile corners cannot
contain two disjoint original pairs, so a point cannot belong to both sets.

A negative U-cap filler cannot belong to Eany. Its tile contains the cap owner's
exact original triple. A foreign pair owner would overlap that triple; the same
cap owner cannot have both an exact pair and an exact triple in one fixed tile.
The original support count of the pair is irrelevant to this exclusion. Hence

    Fneg+|E0|+|E1reg| <= 2K01+2K10.                 (3)

Using Fneg+Fpos+U0=2K11 and Fpos<=A gives the stronger unrestricted cap budget

    2K11+|E0|+|E1reg| <= 2K01+2K10+Fpos+U0.        (4)

Let L=|Pneg\(FnegSet union Eany)|. The exact simultaneous identity is

    2R=2(K11-K01-K10)+eany+(A-Fpos)+Z0+H+L.        (5)

This is an identity derived by partitioning one original singleton pool and
substituting the exact reserve identity. Eany and H may describe the same tile;
no H unit is spent a second time. Dropping L>=0 gives the retained-defect bound.
In the established same-component AA census Fpos=U0=0, so

    |E0|+|E1reg| <= 2Delta, Delta=K01+K10-K11.      (6)

Every forced z from Section3 that belongs to Pneg lies in E1reg: its foreign
active owner supplies the exact regular pair in Q. The forced-point injection
ensures these reservations do not repeat across neutral contacts or components.
Not every forced z belongs to Pneg, and different original owners of the same
type are not automatically new budget resources. Those exits remain to classify.

The later [closed-receiver separation theorem](CLOSED_NEUTRAL_RECEIVER_SEPARATION.md)
proves that the forced physical receivers of closed-component contacts are also
distinct, even when full. A full receiver's other opposite endpoint likewise
avoids every closed phase01 owner, yielding at least eight outside endpoint
positions per AA closed component. That later result has separate validation
and is outside this note's initial independent-review snapshot.

Equation(4) is stronger than the earlier cap inequality by exactly |E1reg| in
the lower bound for2R with the other terms retained. It supplies configuration
constraints, not a new uniform coefficient replacing the accepted complete-source
33/35 or26/27 bounds. No improvement for arbitrary grids is inferred from it.

## 6. Verification boundaries

The Lean companion proves normalized direction-tag uniqueness over all eight
frames, the exact finite orientation catalogue, the conditional support-retention
contradiction, arbitrary-list capacity conditional on cap/pair separation and
pool inclusion, and conditional count/shared budget deductions. The lattice
normalization, source tag construction, global
forced-point injection adapter, source-role exclusion and actual stop separation
are written physical arguments. They are not replaced by arithmetic premises.

The checker independently reconstructs complete original sources, neutral01
contacts, forced points and owners, closed phase01 exclusion, shared H stops,
both endpoint reservation classes and the exact unused-slot identity. Initial
controls PASS641 complete feasible images:116 old irregular-pair slots and170
additional regular-pair slots, with97 strictly stronger images. Eight neutral01
contacts force eight distinct endpoints; all eight are nonfull regular stops
and Pneg reservations. Complete full-stop/AA coverage is ZERO. The original
eight-frame classification is exhaustive because all cardinal orientations
are included; arbitrary dimensions enter through the proven minimum stencil.
Execution and independent-review receipts are recorded separately. Independent
review6b3c685f completed ACCEPT, observed gpt_6/pro, for the injection, whole
closed01 owner exclusion, J01/D/C0 shared stop budget, any-pair cap reservation
and exact unused-slot identity. Its two precision edits to component scope and
conditional list capacity are incorporated above. The original stream92159
completed successfully with DONE and its19206-character answer exactly matches
the same-task terminal response. This is written-proof review, not execution
certification, and excludes the later closed-receiver separation theorem.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
