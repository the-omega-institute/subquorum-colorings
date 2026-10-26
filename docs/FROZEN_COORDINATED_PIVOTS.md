# Genuine frozen-grid coordination and a fixed-P maximum local trap

26 October 2026. Wenlin Zhang and Haobo Ma. Independent research continuation.

We give two physical grid results beyond the earlier abstract coordination
example. First, a true fixed-P maximum with complete freezing has payment one
and admits **no improving single P-free pivot**, although two such pivots
jointly pay both sources. Second, for every n there is a completely frozen
grid with n specified P-free pivots for which every proper chosen subset pays
one source and the full set pays two. In the second construction every pivot
has local capacity zero and **every positive forest cell set stays identical
under every chosen subset**. Only access to two surviving units changes.

These are obstructions to restricted local optimization and to treating
individual direction repairs as independent new access arcs. They do not
refute the numerical target inequality or prove a universal 5/6 improvement.
The submitted 11 October manuscript is preserved.

## 1. Model and previous results used

Use the feasible (T,M) grid model, restored global M/PP owners, canonical
maximal H/V bands, whole-owner no-P-gap resource support, physical TP→BP links
and full fork-capable payment convention from the preceding notes. A P-free
pivot changes the H/V direction of an aligned 2×2 tile with no actual matching
endpoint. All owners, types and physical links stay invariant under any
simultaneous family of such changes: N changes only at P-free sites, and a
new/deleted axial seam touches such a site and cannot carry a terminal link.
This does not assert that supports are independent between pivots.

We use the [four-arm ledger](P_FREE_PIVOT_INTERFACE.md), which says that a
single pivot can add support only in the newly joined axial no-P gap, and
the existing [fixed-P maximum construction](FIXED_P_MAXIMUM_FROZEN_ELBOW.md).
The latter supplies an explicit 16×28 feasible T of size 186, an actual
35-edge matching M, all 70 endpoints frozen in 12 strict waves, and a
general geometric upper bound |T|≤186 for this P. Its three original units
are denoted Q,R,U, with Q private to mixed owner z and U,R unsupported.

The relevant source kernel is the same throughout this note:

    a: TP tips (3,12),(10,12),
    b: TP tips (5,17),(12,17),
    z: TP (5,15), BP (5,16).

There are alpha=2, beta=2, mixed=5 owners. The only external source-reachable
link is b(5,17)→z(5,16). Neither a nor z has an external exit. The owner a is

    {3,...,10}×{10,11} ∪ {(3,12),(10,12)}.              (1)

All four alpha tips have occupied degree three. The sole supported unit of
z is {(4,13),(5,13)}. These statements are explicit finite-kernel identities,
not assumptions about a random or optimized grid.

## 2. A genuine local trap at a true fixed-P maximum

Retain T186,M and all directions from the maximum fixture, except set tile
g=(10,14) to V. Tile h=(10,16) is already V. Both are P-free. Define action
g or h to mean changing that tile to H. All other directions stay fixed.
The exact four-state table is

| Chosen actions | Support of a | V | Minimum physical links |
| --- | --- | ---: | ---: |
| none | empty | 1 | 1 |
| g only | empty | 1 | 1 |
| h only | empty | 1 | 1 |
| g and h | {K} | 2 | 1 |

Here K={(10,17),(11,17)}. Owners/types/links and all non-a supports are the
same in these four states. The raw pool has exactly three units and slack
S=3. Changing directions does not change T,M or their extremality/freezing.

**Direct proof of the joint table.** Below a's tip (10,12), the H gap starts
at column 13. Columns 13,14,15 are BT when horizontal. The gate g contains
the two selections (11,14),(11,15), so its H capacity is zero. The tile h
contains the one selection (10,16); in V its sole unit is the horizontal
pair U={(11,16),(11,17)}, while in H it is the vertical pair K. A V gate g
separates a from tile h in either h direction. Opening g without h reaches
only the BT columns 13,...,15 and then stops. When both are H, a's gap reaches
K. The upper a gap still has no positive resource. Owner b always retains
the one-link route through z and Q. Thus one is always feasible, and two is
feasible precisely when both gates are H. Since a has no external exit and
there are only two sources, these values are exact. The b route requires
one link in either optimum. ∎

**Stronger theorem: all single P-free pivots fail to improve this start.**
There are 81 P-free tiles in this board. None of their individual flips
raises V above one; consequently the minimum number of arbitrary P-free
tile changes needed to reach full payment is exactly two.

**Geometric proof without using 81-case optimal-value enumeration.** Since
a has no external exit under any P-free flip, paying both sources requires
that a gain an interval support. Its old support is empty. By the four-arm
ledger, an added support must belong to the newly joined axial gap and a
must be one of that gap's P-boundary owners. Using the body (1) and the
fixed directions of its occupied tiles, the only P-free tiles whose new
axial gap can have boundary owner a are the following three:

| Tile flipped | New direction | Entire new a-side no-P gap | Positive count |
| --- | --- | --- | ---: |
| (0,10) | V | rows 0,1,2 in column pair 10,11 | 0 |
| (10,14) | H | columns 13,14,15 in row pair 10,11 | 0 |
| (12,10) | V | rows 11,12,13 in column pair 10,11 | 0 |

To verify completeness, the occupied V column-pair 10,11 carrying (1) can
only extend at its top/bottom free tiles (0,10),(12,10). Its side extensions
would require changing an occupied tile to H first. The two extra occupied
tiles containing tips (3,12),(10,12) are H: their free top/bottom neighbours
cannot reach their P columns in V while those tip tiles remain H. A new H
gap can extend the lower tip band through (10,14); the analogous upper tile
(2,14) is already H, so its flip is to V and cannot create this H access.
All remaining P-free tiles either miss (1)'s axial bands or are blocked
from it by unchanged direction/P boundaries.

Each listed gap consists entirely of BT columns/rows. In particular the
tile selections are respectively {(0,10),(1,11)}, {(11,14),(11,15)} and
{(12,11),(13,10)}. The intervening one-column/row portions are BT as shown
by the explicit T186 coordinates. Each gap therefore has no positive unit.
So no single pivot can give a support, and V≤1. The two-gate construction
above attains two; minimum distance two follows. ∎

As a check, explicit enumeration finds 80 single pivots keep V=1 and the
remaining pivot (4,12) decreases it to zero. All eight dihedral images give
the same local-trap and joint-gain statements. The theorem concerns P-free
pivots; changing an occupied tile may change the owner system and is outside
this local-neighbourhood claim. This board has a better direction assignment,
so it is not an obstruction after global optimization of N.

## 3. Arbitrarily long coordination with zero-capacity pivots

For any integer n≥1 put q=max(n,6). Start from the explicit fully frozen
T83,M35 construction returned by `configuration_one()` in
[check_fully_frozen_elbow_withdrawal.py](../develop/check_fully_frozen_elbow_withdrawal.py).
Its full base coordinates, directions and strict layers are already stored in
[fully_frozen_elbow_rank_one.json](../develop/fixtures/fully_frozen_elbow_rank_one.json).

Extend its 16×28 board to 16×(18+2q), keeping every old matching edge, old
selection and old direction. In the new columns put selections only at

    (3,c) for even c, and (2,c) for odd c,
    28 ≤ c < 16+2q.                                   (2)

All new tiles are H initially. The old construction already has this same
diagonal-selection pattern in rows 2,3 and columns 16,...,27. Keep the
far-right tile at (2,16+2q) empty and H. Its two BB units are

    J_0={(2,16+2q),(3,16+2q)},
    J_1={(2,17+2q),(3,17+2q)}.                         (3)

Declare n gate tiles

    G_i=(2,16+2i),  0≤i<n.

Set all these gates to V at the start. An action opens one gate by changing
it to H. The other q−n diagonal tiles along this upper corridor remain H.
The old lower cut at (10,16) remains V.

**Theorem (all n, all subsets).** For every chosen gate set F⊆{0,...,n−1},
the resulting grid is feasible, all 70 endpoints are strictly frozen in the
same old 11 waves, and

    |T|=71+2q,  |M|=35,  L=S=38+14q,
    V(F)=1+1[F={0,...,n−1}],  minimum links=1.          (4)

Each gate is P-free and has kappa=0. Every positive forest has precisely
the same physical cell set for every F. All non-a supports are unchanged.
The only variable support is

    W_a(F) = {J_0,J_1} if F is all gates; empty otherwise.  (5)

**Proof.** The added selections (2) are isolated within rows 2,3; beyond
column 27 all other new sites are empty and there is no P. They introduce
no extra occupied neighbour of an old selection or matching endpoint. At
the old/new join the same diagonal phase continues, so feasibility is
unchanged there as well. The new selections do not meet any P-neighbourhood,
and the old strict rank certificate remains valid at every endpoint. Thus
all 70 endpoints remain frozen. Each gate contains the diagonal T sites
(2,17+2i),(3,16+2i), giving BT/BT in both H and V. In particular no gate
contains a positive or balanced BB/TT forest in either direction.

Every direction change occurs at these BT-only gates. A BB/TT forest
cannot connect through a BT row/column. Splitting or joining bands there
therefore leaves the cells of every positive forest unchanged. There is
also no new P boundary at a gate. The vertical band above the gate row
ends at the unchanged H row-pair 0,1; hence a gate cannot join its old
lower vertical arm to a new P owner above. Any lower-arm resource retains
exactly its old boundary support. Horizontally, all intermediate corridor
columns are BT. The only positive corridor units are (3), at the far right.

The upper a boundary is at column 12, followed by BT columns 13,14,15 and
the q diagonal tiles. If every declared gate is H, that one H no-P gap
reaches (3), which become private to a. If even one gate is V, the remaining
rightmost H segment containing (3) has no P boundary at either end, so
they remain unsupported. All other horizontal pieces contain no positive
unit. This proves (5) and all non-a support claims. The source kernel in
Section 1 is unchanged by the new empty columns/diagonal T or P-free flips.
The lower a corridor is still cut at (10,16) and has no old accessible unit.

Owner b always pays through z at one link. Owner a has no external exit,
so it pays if and only if (5) is nonempty. The two newly accessible units
give only one extra payment, because a is one capacity-one alpha source.
There are no other alpha sources. This proves the exact V and link counts.
There are 2(q−6) added selections, so |T|=83+2(q−6)=71+2q. Since alpha=beta,
the raw count equals the slack, namely

    16(18+2q)/2 − (71+2q) − 35 = 38+14q.

All assertions hold for every n and F; no bounded search enters this proof. ∎

## 4. Consequences for repair selection

On the declared corridor actions, enabled-set and applied-set optima coincide:
the value in (4) is monotone, and selecting a proper subset cannot achieve
the extra payment. Thus a budget b of these actions has exact optimum

    max_{|F|≤b} V(F) = 1 + 1[b≥n].                    (6)

For n≥2 let A be all gates except one and B all gates except another.
Then V(A)=V(B)=V(A∩B)=1, while V(A∪B)=2. Hence

    V(A)+V(B)=2 < 3=V(A∪B)+V(A∩B),

so payment, or payment gain above baseline, is not submodular. This is
now a genuine fully frozen grid embedding, with all pivot capacities zero
and no physical resource withdrawal. Any strictly improving local search
restricted to fewer than n of these gate actions has no first improving
move. Neutral moves may still lead to the full opening.

The all-n action budget is for the declared upper corridor. The same
construction still has a one-pivot repair outside that set: opening the
old lower tile (10,16) pays a directly. We verify this control for every
tested n. Thus the all-n theorem does not assert an unrestricted n-pivot
distance lower bound. The separate T186 theorem does prove a distance-two
barrier across **all** P-free single pivots. Extra actions elsewhere do not
remove the non-submodularity witness formed by subsets of the upper gates.

The earlier [single-token choice theorem](DESTRUCTIVE_EXCHANGE_CHOICE.md)
requires a simultaneous physical replacement adapter. No individual
zero-capacity gate here creates an unconditional private unit, and no unit
physically disappears at all. Giving each gate its own direct target-access
arc would invent unsupported access. The entire corridor may be represented
as one compound action with cost n, or by a serial gate constraint recording
that all its physical cuts have opened. Its two units remain original units;
they are neither n new units nor two extra source payments. General joint
repair must account for such geometric prerequisites as well as resource
competition and surviving-support losses.

## 5. Verification and formal scope

Run the checks from the repository root:

```sh
python3 develop/check_frozen_coordinated_pivots.py \
  --output output/frozen-coordinated-pivots-validation.json
python3 develop/check_coordinated_pivot_gates_formal.py \
  --lean /absolute/path/to/lean-4.33.0 \
  --output output/coordinated-pivot-gates-formal-validation.json
```

The validator checks every P-free single pivot of the extremal trap (81),
all four joint states and the three boundary candidates of the geometric
proof, as well as the existing disjoint geometric cover proving maximum
186. It replays the freeze ranks and checks every single pivot in all eight
dihedral images (648) and their joint repair. For n=1,...,8 it checks all
gate subsets; for n=16,32,64 it checks full/empty, both parity sets, every
one-gate omission and every singleton. These give 746 joint family states,
with all owner/type/link invariants, complete forest cell-set equality,
all non-a support equalities and exact support (5) checked. All small and
large state optima are also checked by independent primitive-pack optimization.
There are 854 independent primitive optimum comparisons in total.
There are 11 alternative-lower-repair controls and 770 strict family freeze
events replayed. These are construction checks, not the all-n proof.

[CoordinatedPivotGates.lean](../formal/SubQuorum/CoordinatedPivotGates.lean)
checks five general finite-list statements: all gates open iff every listed
gate is enabled; value two iff complete; any missing gate gives value one;
monotonicity; and the strict submodularity violation for any two distinct
required gates. The Lean 4.33.0 audits use only propext and Quot.sound, with
no new axioms, sorry or native decision. The frozen-grid embedding, fixed-P
maximality, local-gap classification and geometric action counts are the
written proofs above with independent executable checks, not end-to-end Lean.

The next positive task is to combine the exact support-change ledger with
joint prerequisite constraints and globally disjoint resource reservations.
Single-pivot no-gain is insufficient evidence that a residual path cannot
be repaired, even at a completely frozen true fixed-P maximum.
