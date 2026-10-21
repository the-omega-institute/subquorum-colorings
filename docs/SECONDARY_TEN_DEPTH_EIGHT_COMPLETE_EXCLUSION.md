# Depth-eight exclusion and a stronger distinct-owner compensation bound

21 October 2026. This strengthens the distinct-owner branch of
[the unconditional residual theorem](SECONDARY_TEN_UNCONDITIONAL_RESIDUAL_COMPENSATION.md).
It uses the same complete feasible original U/rotor model, fixed tile phase,
matching and ORIGINAL support sets. No new statement about arbitrary graphs,
global package allocation or the global 5/6 bound is made.

## Statement

Retain either eight-original residual A=Q,D,L,C,E,W,T0,V of the cited note.
In particular a is odd, w>=12 even, and

    V=U(k,8,z), (r,c)->(a-6+r,w+12-c),
    (k,z)=(w+8,even 4..14) or (w+10,even z>=16),
    E=U(6,4,4), (r,c)->(a+4-r,w+7+c).

**Exclusion lemma.** No complete feasible original family retaining A can
contain an additional original

    K=U(h,8,f), (r,c)->(a-8+r,w+15-c),

for any legal even h>=6 and f>=4. This holds without any assumption about
the actual consumer at t=(a+1,w+14).

**Compensation corollary.** If e=(a,w+14) and t have distinct actual
owners, the subinventory I in the unconditional theorem can be chosen with

    A subset I subset G, |I minus A|<=2,
    Phi(I)>=Phi(Q,D,W)+3.

For the common-owner branch the previously proved baseline bound remains.

## The missing support and its forced direction

Suppose first that K is endpoint-disjoint from A; otherwise it is already
excluded. The point p=(a+2,w+12) is the ORIGINAL support (8,0) of V.
It is absent from all eight retained endpoint sets. Its K coordinates
are (10,3), which are neither bar nor stem endpoints for h>=6, so K also
does not consume p. The three retained endpoint neighbors of p are

    west  (a+2,w+11) in V,
    east  (a+2,w+13) in E,
    south (a+3,w+12) in E.

An unconsumed original support in a complete feasible family has exactly
one occupied neighbor. Thus p must be consumed by an additional actual
original J. Its matching partner cannot be any of these three foreign
endpoints. The only possible own neighbor is north. Consequently J has
exactly one own neighbor at p. In the U/rotor catalogue this is either a
U leg terminal or one of the two north-terminal rotor tips. Full-source
leg relabeling preserves matching and original supports, so a U at p has
one of the following exhaustive charts, with legal even H>=6,d,f'>=4:

    J_R=U(H,d,f'), (r,c)->(a+2-d+r,w+11+c),
    J_L=U(H,d,f'), (r,c)->(a+2-d+r,w+13-c).

The consumer is neither K nor an original of A, since p is absent from
those endpoint sets. Therefore any shared endpoint below violates actual
original endpoint disjointness.

## Explicit collisions for every possible consumer

For d>=10, both J_R and J_L contain x=(a-7,w+12): its J coordinates
are (d-9,1). At d=10 this is a bar endpoint; at d>=12 it is a near-stem
endpoint. The same point has K coordinates (1,3), so it belongs to K.

For d in {4,6,8} and J_R, use x_R=(a+3-d,w+14). Its J_R coordinates
are (1,3), and its K coordinates are (11-d,1). The latter row is 7,5,3,
respectively, hence lies in K's retained near stem of length 8.

For d in {4,6,8} and J_L, use x_L=(a+3-d,w+11). Its J_L coordinates
are (1,2). Its V coordinates are (9-d,1), namely (5,1),(3,1),(1,1).
All three are endpoints in the retained near stem or bar of V.

These cases exhaust every legal even incident depth. Neither the U
consumer's far-leg length nor the breadth or far-leg length of V can
remove these explicit endpoints.

Finally, each north-terminal rotor at p contains p+(-2,1)=(a,w+13).
That is E's endpoint with intrinsic coordinates (4,6). Both rotor
choices therefore collide with E. No actual consumer of p is possible.
This contradicts completeness and proves the exclusion lemma. Adding
more originals cannot remove any of these retained collisions.

## Improved compensation and the old receipt witness

The exact accounting in the unconditional theorem remains valid for
endpoint-disjoint partial inventories. A distinct t-owner which is a U
already gives gain at least4 over Phi(A). For an east-terminal rotor
R_N or R_S at t, its increment is 0 or -1 and the actual e-owner is a
north-terminal U, with exact increment

    h-1-k*[left orientation and incident depth 8].

The exclusion lemma eliminates the exceptional indicator in every
complete extension. Thus the actual upper U contributes h-1>=5. The
two-original increment is at least5 for R_N or at least4 for R_S.
Since Phi(A)=Phi(Q,D,W)-1, all distinct-owner routes give baseline
excess at least3. The same original charge is used only once in this
single-package accounting; a consumed support receives no separate credit.

The former endpoint-disjoint witness with k=w+8,z=4, R_S and
K=U(w+12,8,4) still has exactly the previously computed increment2
over A. Its width debit and four directed events per shared V tile are
correct. The new lemma proves that its entire prefix has NO complete
extension in this model. It is therefore a valid partial-inventory
receipt test and cannot witness sharpness of the complete-family bound.

## Verification scope and next obligation

The ten new declarations in
[SecondaryTenDistinctConsumers.lean](../formal/SubQuorum/SecondaryTenDistinctConsumers.lean)
verify the original support, absence, three foreign neighbors, unbounded
U collision alternatives, both rotor collisions and the strengthened
conditional arithmetic. The module now has 24 theorem declarations.
The role catalogue, complete-family implication and exact Phi receipts
are ordinary written proofs, rather than an end-to-end Lean theorem.

[The control program](../develop/check_secondary_ten_depth_eight_exclusion.py)
checks full original source sets, the forced support, explicit collision
points and the unchanged partial-inventory accounting across both
residual families, signed translations and long far legs. Enumeration
is a control of the written all-parameter proof.

Different residual packages may still select the same actual compensator.
The next question is whether their terminal claims can be assigned once
per physical terminal and whether all remaining inter-package directed
events fit the unused owner budgets. The larger single-package margin
does not itself prove either fact or any global inequality.
