# Boundary stops and the joint four-stem core obstruction

20 October 2026. This note proves necessary terminal roles for the boundary
route of an unpaid width-six double and excludes mutual closure using only
the two existing four-stem cores. It does not assign a new compensation unit
to an additional owner. Negative-source finite closure, unrestricted
coefficient one, and rectangular-grid triple equality remain OPEN.

## 1. Model and hypotheses

Use the finite complete U/rotor source model, original endpoint ownership,
retained original supports and fixed physical aligned 2x2 partition of
WIDTH_SIX_FOUR_STEM_COMPENSATION.md and
POSITIVE_BOTTOM_OWNER_RESERVE_OBSTRUCTION.md. In particular original
endpoint sets are disjoint, their union is P, every original support outside
P remains selected, and every final selected vertex has occupied degree at
most one. Every U has even width at least six and independent even incident
heights at least four. All lattice isometries and translations are allowed.
Final selections are the retained original supports together with any
permitted optional selections outside every original receiver and without
an endpoint neighbor. In particular no arbitrary unanchored selection
may be added inside a source receiver. Positive-source normalizations
transport the FIXED physical partition; they do not reset it after a
translation or reflection. The later affine origin for vector arithmetic
is chosen only after the physical parity comparisons.

Consider the actual nonexceptional R=1 AA residual: exactly two double-marked
positive sources, both width six, each with one activated terminal. Its exact
ledger has A=2 and U0=Z0=H=0. The accepted common pool then also gives
r=J=X=0. Arbitrarily many one-mark positive and negative sources remain
allowed. An original owner may belong to both four-stem cores through
different tips; this possibility is explicitly allowed throughout.

Normalize either double as O=U(6,a,b), with its long left terminal unactivated.
Its four distinct incoming owners have the established forms

    L(r,c)=(h+2-r,c+1),   R(r,c)=(k+2-r,c+4),
    V(r,c)=(d+2-r,c+2),   W(r,c)=(j+2-r,c+3),
    b<=k, k+2<=j, j+2<=d, d+2<=h<=a-4.

L,W have two original triple caps; V,R have none. All four bars have
thickness in the long-leg direction and straddle the aligned row-pairs:
their two bar rows have odd/even parity in this normalization. The
original tip predecessor of either leg of each core owner points SOUTH,
along O's long-leg direction. Here and below the predecessor direction
means the vector from a terminal to its adjacent endpoint of that owner.

The forced point p=(h+3,2) belongs to P. The point q=(a+1,2) is absent from
every original endpoint AND support set. These are the previously proved
two-neighbor bottom-point and retained beyond-tip-support conclusions.

Zero H forces each original 2P0T pair receiver to be full: otherwise its
tile is an L2bar defect or a mixed L3 defect. Zero U0,H forces each
original endpoint-containing phase11 U receiver to be full. These are
the existing physical saturation results, not new independent payments.
For the first implication, each unfilled corner neighbors an original
endpoint of the pair owner. A foreign retained support there would have
its own different persistent original anchor, hence two occupied neighbors.
The pair owner contributes no support in this tile and optional selections
are excluded there. Thus no vacant corner is selected; a nonfull tile
has the original adjacent pair (L2bar) or a mixed triple (L3).

## 2. A finite last point gives three possible stop roles

Define

    rho=max{r:h+3<=r<=a and (r,2) belongs to P},
    x=(rho,2), y=(rho+1,2).

The set is nonempty because it contains h+3 and finite because r<=a;
no bound on the number or dimensions of the other sources is needed.
If rho<a, maximality excludes y from P. If y were an original support,
retention would leave it selected with distinct persistent endpoint
neighbors x and O(rho+1,1), impossible. If rho=a, y=q is already forbidden
as both endpoint and support. Thus in all cases y is neither an original
endpoint nor an original support of ANY source.

Let B be the unique original endpoint owner of x. It differs from O;
the west neighbor (rho,1) is an original endpoint of O and hence not of B.
The south neighbor y is neither an endpoint nor a support of B. The exact
U endpoint/support predicates now leave just two U roles, after renaming
the incident leg as the left leg:

    corner:   B(r,c)=(rho-r,c+1),
    terminal: B(r,c)=(rho+c-1,D+2-r),

where D is the terminal's even incident height. In the corner role the
bar goes east and the incident stem north. In the terminal role the
predecessor is east and the bar goes south. The unrestricted endpoint-only
classification also allows a corner whose bar goes north and stem east,
but its exterior bar-end support is y. It also allows a terminal whose
predecessor is north; its
original beyond-tip support is y, so support exclusion eliminates it.
For the east-predecessor terminal, the opposite bar direction makes y
the original even-height exterior support and is likewise eliminated.

For a rotor, putting each of its eight endpoints at x in each chirality
is an exact 16-role exhaustion over every translation. Only one role
survives the same west-endpoint and south-endpoint/support exclusions.
Relative to x, it has endpoints

    {(-1,2),(0,0),(0,1),(0,2),(1,1),(1,2),(1,3),(2,1)}

and an original support (2,0) anchored at (2,1). This is
source_at((true,-2,4)) translated by x, or the supplied rotor under
(u,v)->(rho+3-u,v+1).

## 3. Even U stops are impossible; a rotor stop reaches the terminal

Suppose rho is even. The aligned tile
Q={rho,rho+1} x {2,3} has the original B endpoint pair in its top row.
For the corner role it has no original B support. Zero H makes this
2P0T receiver full, which would put y in P, a contradiction.

For the terminal role, Q has exactly that endpoint pair and original
support (rho+1,3), with y its original blank. This physical U image has
phase11 (two triple caps); zero U0,H saturates Q, again filling y.
Thus a U stop must have rho odd. The corner role then has original
charge -1, and the terminal role has phase10 and no triple caps. These
phase conclusions use legal even dimensions and the physical aligned
partition, in addition to the endpoint-role classification.

For the rotor role, if rho<=a-2 its original support z=(rho+2,2) is outside
P by maximality. Retention leaves it selected, but it sees the distinct
persistent endpoints (rho+2,3) of B and (rho+2,1) of O, impossible.
If rho=a-1 the same support is q, already forbidden. Consequently rho=a.
The rotor's tile Q has three original endpoints, with missing point q.

An unfilled rotor triple is NOT automatically a Z0 defect. That count
requires the specific activated paired-zero-rotor singleton relation in
the existing ledger. No such pairing has been established here. Therefore
the rotor-at-a alternative remains a legitimate necessary stop role.

The complete necessary list is therefore:

1. An odd-row negative corner, bar east and legs north.
2. An odd-row negative phase10 terminal, predecessor east and bar south.
3. The unique rotor role at rho=a.

In the odd-corner role, disjointness from L's column-two wall also forces
its incident height D to satisfy rho-D>=h+3, hence D<=a-h-4. This bounds
one incident height relative to the available gap; it does not exclude
arbitrarily large gaps or give a descent invariant.

## 4. Two existing cores cannot supply both boundary stops

For the two positive doubles let C_i={L_i,V_i,W_i,R_i}. These sets may
overlap. Choose the boundary stop B_i as above for each double.

First B_i lies outside its OWN C_i. Every original endpoint of a core
owner lies at long-leg coordinate at most m+2<=h_i+2, from its displayed
map and nonnegative original source row. But the stop coordinate is
rho_i>=h_i+3. This includes both original tips, however long the far leg.

Assume for contradiction that both B_i belong to C_1 union C_2. Each
must then be in the OTHER core. Rotor and odd-corner roles are impossible
there: a rotor is not a U, while an odd corner's physical bar thickness
is aligned and every core owner's thickness straddles aligned pairs.
That comparison uses the same fixed physical partition in both frames.
Thus both identifications must be terminal roles. We allow ALL four
core offsets below; no cap-count reduction to V/R is necessary.

Let A_i be the outer top bar endpoint of O_i adjoining its long leg.
Let d_i point along that leg and e_i inward toward the opposite leg.
Then the boundary stop and all possible near core tips are

    S_i=A_i+rho_i*d_i+e_i,             rho_i>=h_i+3>=13,
    near core tip=A_i+2*d_i+t_i*e_i,  t_i in {1,2,3,4}.

Both near and far tips of a core owner have predecessor +d_i. Both
boundary stops have predecessor +e_i. Mutual identification therefore
forces d_2=e_1 and d_1=e_2. The boundary terminal's bar direction is
+d_i. A near core tip has bar direction +e_i, while a far core tip has
bar direction -e_i. Thus each mutual identification must use the NEAR
tip. In particular the possibility of a shared owner being used at its
other, far tip has been checked, not silently excluded.

Normalize A_1=(0,0), d_1=(1,0), e_1=(0,1). Then d_2=e_1, e_2=d_1.
Write A_2=(u,v). Identifying both stops with the other core's near tips
gives exactly

    rho_1=u+t_2,   1=v+2,
    u+1=2,         v+rho_2=t_1.

Hence u=1, v=-1, rho_1=t_2+1 and rho_2=t_1+1. Both stop rows would lie
between two and five, contradicting rho_i>=13. Therefore at least one boundary
stop has an original owner outside C_1 union C_2.

This is an owner requirement, not a fresh defect or activation. The same
additional owner might serve both stops. Nothing here permits counting
that owner, its charge or its matching twice, or concludes that continued
negative-source routes cannot cycle.

## 5. Verification and scope

The boundary last-point argument and stop classification in Sections 2-3
are written general proofs. The universal U classification and exact
16-role rotor check have scoped Lean counterparts; the maximum,
physical saturation, phase and coordinate adapters remain written.
The Python controls reconstruct representative original U images and
even receiver profiles, the exact rotor table, and a conditional
near-tip coordinate calculation. The physical predecessor and bar signs
justify that near-tip reduction in the written proof above. There is no
new complete feasible physical fixture or new
independently spendable defect payment.

The boundary route was proposed in Oracle research follow-up54d0581e;
the local reconstruction supplies the last-point and retention proof.
Independent audit2e5c473e accepts the written boundary and joint theorem,
under the explicit complete-source support and physical-partition rules.
The unrestricted negative-source cycle problem remains the next target.

All fourteen declarations in formal/SubQuorum/BoundaryStopAndJointCore.lean
compile, build and pass individual axiom audits on the user-selected local
Mac with Lean4.33.0. The exact rotor tables and retention/logical lemmas
use no axioms; other declarations use only propext, Classical.choice and
Quot.sound as applicable. No sorry or native_decide is used. The universal U role proof
first classifies endpoint-only roles and then excludes the exterior-support
roles; this avoids the original monolithic simplification timeout.

Finite controls pass29 dimension triples/15904 U roles,116 exact even-stop
receiver profiles, all16 rotor roles, all8 orthogonal physical frames and
128 conditional mutual-tip coordinate solutions, all with stop rows at
most five. These controls do not enumerate complete AA configurations.
See output/boundary-stop-joint-core-controls.json and
output/boundary-stop-joint-core-formal-check.json. Independent audit
2e5c473e completed ACCEPT at2026-10-20T06:27:48.824UTC, observed gpt_6/pro,
21233characters. Original83291 exits0/DONE and exactly matches terminal
response. Its support/partition clarifications and the unnecessary-Y
removal are incorporated; its simplification allows all four offsets,
with the coordinate hypothesis weakened to t_i<=4. The audit is a written
proof review, not certification of Lean/Python execution. See
output/boundary-stop-joint-core-review.json.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
