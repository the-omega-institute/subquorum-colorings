# Joint selection withdrawal: an exact frontier, successor compensation, and a normalization obstruction

26 October 2026. Wenlin Zhang and Haobo Ma. Research continuation.

The subsequent [joint withdrawal/rematching theorem](WITHDRAWAL_REMATCHING_JOINT_BOUND.md)
removes the retained-M0 assumption while keeping P0 and the specified retained
selections. It proves the same sharp frontier by occupation weights and a
single global rounding, and gives actual original-tile net compensation for
every rematching, including the normalization obstruction below.

Withdrawing one retained guard CAN increase the objective by one, even with
complete freezing and all old matching edges retained. For any subset of q
interior guards we prove the exact maximum 17k+12+q and give a completely
frozen attainer. Its compensation moves each lost rebate to the next core's
original reserve, spends that reserve once, and leaves exactly k-q full units.
When every interior guard is withdrawn, the negative strip is arbitrarily
deficient but the whole board has only ONE remaining full unit.

A separate completely frozen all-k construction shows that one withdrawal
also defeats old-edge-preserving normalization on the same occupation. This
refutes an extension of the earlier repair rule, not the half-area target.

## 1. Exact theorem and hypotheses

Use the original b=1 family (T0,M0) on the 6-by-(6k+4) board, k>=2, defined in
[the sharp-completion note](FROZEN_STRIP_SHARP_COMPLETION_AND_RESERVES.md).
Let J be ANY subset of {0,...,k-2}, q=|J|, and let

    g_i=(3,9+6i),     G_J={g_i:i in J}.

Each g_i is an old selection beside the right end of core i. Consider EVERY
feasible pair (T,M) satisfying

    T0 minus G_J is a subset of T,    M0 is a subset of the actual M.

M is a grid matching; T is disjoint from P=V(M); and every selected site has
at most one occupied neighbour. Additional selections and actual matching
edges are unrestricted. The sites in G_J may even be selected again; their
withdrawal is permitted, not forced by the upper-bound hypothesis. Then

    |T|+|M| <= 17k+12+q = area/2-(k-q).               (1)

For every J there is a completely frozen configuration attaining equality,
with exactly G_J removed from T0. Thus (1) is the true maximum over all these
additional choices, and remains the true maximum with complete freezing.
The top two-row strip is unchanged, with surplus (1-k)/2.

This theorem retains M0 and treats the specified interior guards. It does
not claim the same upper bound when old edges are simultaneously rematched,
when other old selections may be removed, or when old endpoint sites are
withdrawn. The separate obstruction in Section 6 explains why the previous
rematching normalization cannot simply supply that missing generalization.

## 2. One guard merges a gate and star into a nine-vertex tree

Anchor old selections using their fixed P0 neighbours, as in the preceding
[retained endpoint theorem](ENDPOINT_INVASION_SHARP_STRIPS.md). An anchored
old T forces every other neighbour blank, including attempted new endpoints.
After removing g_i with c=9+6i, exactly THREE new sites become available for
occupancy: (3,c) itself, (2,c), and (3,c+1). The other former neighbour (4,c)
is still forced blank by retained T0(4,c-1). These three sites join the old
gate and star belonging to core i+1. Name their union

    d=(2,c),   g=(3,c),   b=(3,c+1),
    u=(2,c+2), v=(3,c+2), a=(4,c+1),
    s=(5,c+1), l=(5,c),   r=(5,c+2).

Its exact edges are

    dg, gb, bv, ba, uv, as, sl, sr.

It is a tree. Vertex g has one old P neighbour, u has two, v has one,
and the others have none. In particular u can never be selected.
Different activated trees have disjoint vertices and no free-grid edges
between them, even when the withdrawn guards are consecutive. Every
unactivated core j>=1 retains its old separate two-site gate and three-leaf
star. The first 15-site pocket and all k+1 isolated free sites are unchanged.

These statements follow by deleting the guards from the exact free-row table
in the preceding note. There are no other newly allowed sites: the remaining
old selections are unchanged, and (4,c) has the second independent guard
just identified. Thus the total free set has 7k+10+3q sites. Retaining M0
ensures that every new actual edge lies within one of these free components.

## 3. A universal tree capacity six, with equality rigidity

Write t_x for new-selection indicators, m_e for new actual tree-edge
indicators, and o_x=t_x+sum_(e incident with x) m_e for actual new occupancy.
Feasibility and the old P neighbours give

    t_g+o_d<=1,   t_u=0.

Use four ordinary wedge inequalities:

    t_b+o_g+o_v<=2,    t_b+o_v+o_a<=2,
    t_a+o_b+o_s<=2,    t_s+o_l+o_r<=2.

A selected centre cannot have two distinct occupied neighbours, so these
hold for every feasible choice. Add these four inequalities, the anchored
pair inequality, t_d<=1,t_l<=1,t_r<=1, and 2t_u<=0. The exact left side is

    2*(number of new T + number of new M) + t_b + m_bv,

and the right side is 12. Every selected-site coefficient is two except
t_b's three; every actual-edge coefficient is two except m_bv's three.
Hence each tree contributes at most SIX. This is an explicit universal
linear certificate; no enumeration of configurations proves the bound.

At capacity six, all contributing inequalities must be tight. In particular
d,l,r are selected, b is not selected, and bv is not a matching edge.
The first wedge forces g and v occupied. As d is selected, g is not selected,
and its only available matching partner is b. Thus gb is a matching edge.
Vertex v now has occupied neighbours b and its old P, so cannot be selected;
with b already matched it must pair with u. The second wedge forces a
occupied. There are exactly two possible equality patterns:

| Pattern | New selections | New matching edges |
| --- | --- | --- |
| A | d,a,l,r | gb,uv |
| B | d,l,r | gb,uv,as |

In B the matched endpoint a has only its mate s and the one other occupied
neighbour b. Its other two grid neighbours are still forced blank. Such an
endpoint cannot freeze: its mate cannot be a strict witness for itself,
leaving only one distinct possible witness. Thus every completely frozen
capacity-six tree has the UNIQUE occupation and new matching of pattern A.

The first pocket has capacity nine by the preceding weighted certificate;
each inactive gate/star pair has capacity 1+3=4; each isolated site has one.
Adding the DISTINCT components bounds the new contribution by

    9+6q+4(k-1-q)+(k+1)=5k+6+2q.

The retained old objective is |T0 minus G_J|+|M0|=12k+6-q. Their sum proves
(1). The equality classification also applies locally to every completely
frozen global maximum, since all disjoint component capacities must then
be attained. It does not assume anything about the first pocket's maximizer.

## 4. An all-subset frozen attainer, with no circular freezing

Begin with the periodic attaining T* of the sharp-completion note and M0.
For every i in J, with c=9+6i, make these disjoint changes:

    delete selections (3,c),(3,c+2);
    add selection     (2,c);
    add actual edges  (3,c)--(3,c+1), (2,c+2)--(3,c+2).

Only (3,c) was in T0. Each active tree now has exactly pattern A. The other
free components keep their old attaining choices. Each new d is selected
beside only g; a is selected beside only b; l,r remain selected with their
centre s blank. All unchanged selected sites keep their original permissible
occupied neighbours. The free-row table and the displayed tree exhaust all
potential interactions, so this proves feasibility for every J and k.

There is an important freezing dependency because changing the old guard g
to an endpoint removes the old right leaf's two-selection seed. Here is a
direct valid induction. Use the preceding core names A,B,C,D,E,F,G,H, with
old edges AB,CD,EF,GH. In EVERY core, A and C still freeze from their two
retained T witnesses; then E freezes using neighbours B,D whose mates A,C
have frozen; then G freezes using F,D whose mates E,C have frozen. These
four frozen endpoints do not depend on H or any withdrawn guard.

The last core has its right guard retained, so H freezes and its whole old
core completes. Work from right to left. If a core's guard was retained,
the usual old certificate completes it. If guard i was withdrawn and core
i+1 has completed, U_(i+1) freezes from its two old P neighbours whose
mates B_(i+1),F_(i+1) are frozen. The new endpoint g_i freezes using selected
d_i and old H_i, whose mate G_i is already frozen. The new V_(i+1) freezes
using old F_(i+1) (mate E_(i+1) already frozen) and new b_i (mate g_i now
frozen). Then b_i freezes using selected a_i and V_(i+1), whose mate
U_(i+1) is frozen. Old H_i can now use its retained lower T and g_i, whose
mate b_i has frozen. This completes F_i,D_i,B_i as in the old certificate.
All dependencies point to an earlier proved stage. This handles arbitrarily
long consecutive runs of active guards, without assuming independent cores.

The construction has

    |T|=13k+11-q, |M|=4k+1+2q, |P|=8k+2+4q.

It attains (1) and has whole surplus k-q. At q=k-1 the whole surplus is
exactly one, whereas the strip surplus (1-k)/2 tends to minus infinity.

## 5. Successor-resource compensation, with original identities

Use ORIGINAL aligned tiles Q_(a,b)={2a,2a+1} x {2b,2b+1}, with doubled
surplus c(Q)=4-2|T intersect Q|-|P intersect Q|. Let

    reserve Q_j=Q_(1,2+3j),  rebate R_i=Q_(1,4+3i).

In the explicit attainer, withdrawing guard i changes its old rebate R_i
from c=1 to c=0: it now contains two endpoints and the new selection d_i.
The successor reserve Q_(i+1) changes from c=2 to c=1: it now has three
endpoints and no selections. Its original whole unit is no longer unspent.
All other reserves retain c=2; all other rebates retain c=1. The boundary
tile Q_(1,0) has c=-1 and every remaining exterior tile has c=0.

All original top-strip labels and actual M0 edges are retained, so its exact
inventory remains B=1,D4=k, no BP refund, and 2S_strip=1-k. Pay its D4 in
core i by

    R_i             if i is not in J;
    Q_(i+1)         if i is in J.

Every allocated tile has exactly one half unit. Different inactive i use
different R_i; different active i use different Q_(i+1); the two original
tile families have different column residues and are disjoint. This proves
one payment per demand with no resource reused, including along consecutive
active chains. Internal B=1 pays the exterior boundary half demand once.

The remaining unspent full units are precisely the ORIGINAL Q_j with
j NOT in {i+1:i in J}. Their number is k-q. None is in the payment map.
In particular one cannot keep counting a successor Q_(i+1) as a whole-unit
reserve after it has been converted into the half unit paying core i.
The complete doubled ledger is

    (1-k)+(k-1)+2(k-q)=2(k-q).

This supplies a simultaneous cross-component compensation lemma for every
subset of guards, not just isolated edits. The payment map is asserted for
the displayed attainers; (1) covers all feasible retained-M0 extensions.

## 6. One withdrawal can also make old-edge normalization impossible

There is a different all-k construction, k>=2, with old P0 retained and
only the same old guard (3,9) removed, but actual M0 rematched. Start again
with T*,M0 and make this fixed patch:

    remove T: (2,3),(3,5),(3,9),(3,11),(4,10);
    add T:    (2,9),(3,10);
    remove M: (1,5)--(1,6), (1,7)--(2,7), (3,7)--(3,8);
    add M:    (1,5)--(2,5), (1,6)--(1,7), (2,7)--(3,7),
              (3,4)--(3,5), (3,8)--(3,9).

The only new endpoint sites are

    P minus P0={(2,5),(3,4),(3,5),(3,9)}.

They contain the isolated site (3,9) in their induced grid graph. ANY matching
on this SAME P containing all M0 would have to match new endpoints among
themselves, since every old endpoint is already used. That is impossible at
(3,9). Hence no occupation-preserving old-edge normalization exists here.
The first old core now uses two nonadjacent ports U and the newly opened
guard, which is precisely what the earlier two-adjacent-port proof excluded.

This is feasible and completely frozen. To make freezing independently
reviewable, the changed first component has the following strict certificate;
all other old cores retain their original certificates. Each listed P witness
is retained because its ACTUAL mate has smaller rank:

| Endpoint | Rank | Two neighbour witnesses |
| --- | --- | --- |
| (1,5) | 0 | T(0,5), T(1,4) |
| (1,7) | 0 | T(0,7), T(1,8) |
| (3,4) | 0 | T(3,3), T(4,4) |
| (3,9) | 0 | T(2,9), T(3,10) |
| (2,6) | 1 | P(1,6), P(2,5) |
| (3,6) | 1 | T(4,6), P(3,5) |
| (3,5) | 2 | P(2,5), P(3,6) |
| (3,7) | 2 | P(3,6), P(3,8) |
| (2,5) | 2 | P(2,6), P(3,5) |
| (1,6) | 3 | P(1,5), P(2,6) |
| (2,7) | 4 | P(1,7), P(2,6) |
| (3,8) | 5 | T(4,8), P(3,7) |

The selected-selected pair (2,3)--(3,3) was broken by removing (2,3), so
(3,3) can now support P(3,4). The new T(3,10) sees only P(3,9), because
(3,11),(4,10) were removed. All other affected selections have at most
their one prescribed endpoint neighbour. The rest of the periodic pattern
is unchanged, proving feasibility and the certificate for every k>=2.

Its objective is 17k+11, and whole surplus k+1. Thus it refutes the proposed
extension of old-edge normalization AND frozen rigidity after one withdrawal;
it is NOT a counterexample to the half-area inequality or even to the old
k-unit scalar lower bound. The scalar gain example in Sections 1-5 is a
different construction retaining M0, with surplus k-1 after one withdrawal.

## 7. Verification and formal scope

The standard-library checker verifies the exact expanded free graph, the
weighted tree certificate, both local equality patterns, arbitrary additional
T/new-matching choices, every joint frozen attainer and all physical payment
identities. It exhausts guard subsets through k=6 and checks representative
subsets through k=128. A separate independent local enumeration checks the
two equality patterns against every feasible nine-site local model. The
normalization obstruction is checked by actual iterative freezing AND the
explicit uniform rank certificate, with isolated-new-endpoint impossibility.

Lean 4.33.0 verifies 14 declarations: strict own-mate/mate-plus-one exclusion;
the exact weighted tree identity, universal bound six and mandatory equality
data; arbitrary-k/q disjoint count aggregation and margin; successor-donor
identity injection and disjointness from remaining reserves; the ledger;
necessary closure of new endpoints under old-edge retention; and the isolated
remainder obstruction and concrete isolated-site geometry. The all-k grid
adapter, complete two-pattern classification, right-to-left freezing and
physical charge adapter remain general written proofs with executable checks.
The all-k board results are not claimed as end-to-end Lean theorems.

    PYTHONDONTWRITEBYTECODE=1 python3 develop/check_selection_withdrawal_sharp_strips.py --output output/selection-withdrawal-sharp-strips-validation.json
    PYTHONDONTWRITEBYTECODE=1 python3 develop/check_selection_withdrawal_sharp_strips_formal.py --lean /path/to/lean-4.33.0/bin/lean --output output/selection-withdrawal-sharp-strips-formal-validation.json

What remains open is a replacement for two-port normalization when old guards
are withdrawn and actual edges simultaneously rematched, and the corresponding
general joint resource cut. Arbitrary mixed-direction footprints, deletion of
other old T/P and the universal 5/6 improvement remain open. The submitted
11 October manuscript, public main/PR #3, shared CI, C4/star-forming work and
correspondence are preserved.
