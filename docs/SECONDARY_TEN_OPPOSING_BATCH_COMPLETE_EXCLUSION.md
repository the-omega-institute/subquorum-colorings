# The opposing-band shared-consumer obstruction has no complete extension

21 October 2026. The unbounded negative exterior construction in the
[batch terminal-budget note](SECONDARY_TEN_BATCH_TERMINAL_BUDGET.md)
is a correct partial-inventory receipt. This note proves a stronger fact:
its entire prefix is impossible in every complete feasible original U/rotor
family. Thus this particular loss cannot be used against the complete-model
exterior condition. The argument identifies the next actual consumer and
excludes all its unbounded parameter choices.

## 1. Setting and claim

Take odd a, even w>=12, and the first prescribed residual A=A_1 with
k=w+8,z=4. Put

    rho(row,column)=(2a-13-row,column),
    A_2=rho(A_1),
    U=U(16,4,4), (r,c)->(a+2-c,w+18-r).

As shown in the batch note, these17 actual-original endpoint sets are
pairwise disjoint and U is invariant as a full original under rho. Their
exterior term is -(w+8) and their baseline excess is 5-w.

**Theorem.** No complete feasible original U/rotor family G contains
A_1 union A_2 union {U}. The statement holds for every permitted w and a,
and for every tile-preserving isometric image of this whole prefix.

Use the exact original matching and support sets throughout. The already
proved complete exclusions of both north-terminal rotors at
e=(a,w+14) in any extension retaining A_1 are an explicit dependency;
see the [unconditional residual proof](SECONDARY_TEN_UNCONDITIONAL_RESIDUAL_COMPENSATION.md).

## 2. A forced north-terminal U at e

The point e is E_1's ORIGINAL outward support (4,7), since
E_1=U(6,4,4) at (r,c)->(a+4-r,w+7+c). It is absent from all
endpoints of A_1. Every A_2 endpoint lies at row<=a-7, so A_2 does
not contain it. Its coordinates in U are (4,2), also not an endpoint.

The west neighbor E_1:(a,w+13) and the south neighbor
U:(a+1,w+14) are retained endpoints. An unconsumed support would have
at least two occupied neighbors. Completeness therefore forces an actual
original K to contain e. This K is distinct from all17 retained originals.
Its only possible own endpoint neighbors at e are north and east.

If a U original has an own east neighbor but no own west or south neighbor
at e, its role is an east terminal or an outer corner with north/east
neighbors. In either role the eastward arm has at least three further
endpoints: an incident U leg has length>=4 and a bar breadth is>=6.
Thus it must contain (a,w+17). But this is the fixed U endpoint (1,2)
in U's intrinsic chart. Such a U consumer is impossible.

For a rotor, the only role with own neighbors restricted to north/east
and including east is an east tip: rotor core endpoints have three own
neighbors. Both east-tip images contain e+(1,2)=(a+1,w+16), which is
the fixed U endpoint (2,1). Both are therefore excluded as well.

Hence K has only its own north neighbor at e. Its two north-terminal
rotor possibilities are excluded by the accepted A_1 theorem, independently
of the owner of t. Therefore K must be an actual north-terminal U, in
one of the exhaustive frames, with even H>=6,d,f>=4:

    K_R=U(H,d,f), (r,c)->(a-d+r,w+13+c),
    K_L=U(H,d,f), (r,c)->(a-d+r,w+15-c).

Full-source leg relabeling preserves the matching and ORIGINAL supports,
so these frames describe the actual owner, not a replacement component.

## 3. Every north-terminal U has a retained collision

The old sources used here have charts

    V_1=U(w+8,8,4), (r,c)->(a-6+r,w+12-c),
    V_2=rho(V_1),   (r,c)->(a-7-r,w+12-c),
    C_2=rho(C_1),   (r,c)->(a-19+r,w+6+c),
    C_1=U(8,6,4).

**All d>=16, either orientation.** Use x=(a-15,w+14). Its K coordinates
are (d-15,1). At d=16 this is a bar endpoint; at even d>=18 it is a
near-stem endpoint. The same point has C_2 coordinates (4,8), its far
terminal. Both orientations therefore collide with C_2.

**K_R with d=4,6,8,10,12,14.** Use x_R=(a+1-d,w+17).
Its K_R coordinates are (1,4), always a bar endpoint. Its fixed-U
coordinates are (1,d+1), also a bar endpoint, since 5<=d+1<=15<16.
This excludes all remaining right-oriented incident depths.

**K_L with d=4 or6.** Use x_L=(a+1-d,w+11). Its K_L coordinates
are (1,4). Its V_1 coordinates are (7-d,1), equal to (3,1) or (1,1).
They are retained near-stem or bar endpoints.

**K_L with d=8,10,12,14.** Use the same x_L. Its V_2 coordinates are
(d-8,1), respectively (0,1),(2,1),(4,1),(6,1). All are endpoints of
the retained V_2 bar or its near stem of length8.

The incident-depth cases exhaust every legal even d>=4. The collisions
do not depend on K's far-leg length or bar breadth beyond H>=6. Neither
additional originals nor support consumption can remove retained endpoints.
Thus every possible actual owner of e is excluded, contradicting the
forced-consumer conclusion. This proves the theorem.

## 4. Consequences and limits

The original batch receipt remains exactly correct: the17-source PARTIAL
inventory has baseline excess5-w and absolute Phi=w+23. It refutes a rule
based only on endpoint-disjoint partial inventories, even after counting
the shared U mass once. The new theorem proves that this entire family
has NO complete extension, a stronger conclusion than merely observing
that it is currently incomplete.

For the complete-family batch theorem, this removes one explicit source
of an arbitrarily large exterior debit. It does not show that all exterior
contacts are nonnegative, that all negative prefixes are impossible or
that the remaining owner budgets cover every complete-model exterior term.
The packing hypotheses, common-owner routes and global allocation remain
open. The final5/6 improvement and rectangular-grid triple equality are
not consequences of this one exclusion.

The new local Lean certificates verify the fixed-U blockers and all
unbounded upper-U collision alternatives. The forced-consumer implication,
full U/rotor role catalogue, prior north-rotor exclusion and the final
complete-family contradiction are the written argument above. Finite
controls corroborate full source sets and every explicit collision;
they do not replace this parameter-uniform proof.

## 5. A complete classification of this reflected two-route family

The exclusion closes the only contact case in a broader reflection family.
For any legal even h>=6 replace U by

    U_h=U(h,4,4), (r,c)->(a+2-c,w+18-r),
    rho_h(row,column)=(2a+3-h-row,column),
    A_2(h)=rho_h(A_1).

The full U_h is again invariant under rho_h, and the two north-frame
routes use its different leg terminals. The following classification is
parameter-uniform:

| Breadth h | Status of the prescribed prefix |
|---|---|
| 6,8,10,12,14 | V_1 and V_2 already share an endpoint |
| 16 | Endpoint-disjoint, but no complete extension by the theorem above |
| h>=18 | The two base blocks have no shared endpoint tile; exact excess h-3 |

For h<=14 use x_h=(a+8-h,w+11). Its V_1 coordinates are (14-h,1),
namely (8,1),(6,1),(4,1),(2,1),(0,1). Its V_2 coordinates are (1,1).
These retained endpoints coincide, so the two bases cannot both occur.

For h>=18 the A_2(h) endpoint row maximum is a+9-h<=a-9, while the
A_1 row minimum is a-6. Thus every row difference between the two bases
is at least3. They have no shared fixed tile or adjacent endpoint, and
their exterior F and E sets are empty. There is just one selected U_h;
its contacts with each base are exactly the locally accounted north-frame
contacts, which have zero signed contribution. The accepted east-U
disjointness criterion shows U_h is disjoint from A_1 for every such h,
and rho_h-invariance gives the same conclusion for A_2(h).

Consequently, for ANY complete family retaining this reflection-family
prefix with distinct actual base owners, one necessarily has h>=18, and
its selected actual-original subinventory H satisfies the exact identity

    Phi(H)=2(w+9)+(h-1)-2=2(w+9)+h-3,
    Phi(H)>=2(w+9)+15.

This is a two-package compensation conclusion with the shared owner's
mass counted once, rather than an assumption that exterior contact is
harmless. The sole potentially unbounded contact loss occurs at h=16
and was excluded through complete-family geometry. The h>=18 statement
does not assert that every displayed prefix has a complete extension;
it applies to any actual complete extension when one exists, and the
exact partial-inventory identity holds regardless of extendibility.
Further insertions may change Phi, so no bound on Phi(G) is inferred.

The complete exclusion and this all-breadth classification received a
separate ACCEPT written review, task d0d63bb8-2ccd-4ae4-8f1b-fbfd4cccdc5f.
The original stream and terminal API agree exactly. Execution and the
later internal-consumer chain results are outside that audit's scope.
