# Protected shared columns: arbitrary-rematching compensation and fresh-end obstruction

25 October 2026. Haobo Ma and Wenlin Zhang. Research branch only.

We give an unbounded completely frozen family of long alpha paths whose
compensation survives **arbitrary feasible additions of T and P and arbitrary
actual rematching**. Neighbouring alpha owners share two different permanent
original interval units. An explicit injective assignment pays all sources
at zero links; the entire block can be eliminated from both ordinary and
full beta-fork compensation, preserving the residual maximum and minimum
cost exactly. No retention of old actual matching edges is assumed.

The same family gives a fully frozen obstruction to counting fresh TP
endpoints separately in components of the matching symmetric difference:
each such component can contain at most one fresh TP while the original
PP/M strands still have two fresh TP ends. It also realizes the retained-old-
pool loss bound k<=floor(e/2) sharply in the frozen domain. The full pool
repairs these examples. This is a failure of a proposed localization rule,
not a counterexample to universal compensation or a numerical 5/6 improvement.

The two-slot allocation is elementary and already implicit in the empty-edge
case of [shared-pocket allocation](SHARED_POCKET_COMPLETION_AND_JOINT_DEFICIT.md).
The new point is the geometric, saturated-T protection and matching rigidity
under arbitrary rematching, its all-length frozen realization, and the exact
residual reduction. The earlier
[protected singleton lemma](PROTECTED_SINGLETON_RESERVES.md) instead protects
a private unit using retained old actual mates; its explicit rematching
counterexample prevents using that argument here.

## 0. A general restriction on the old/new interface

The following observation is not limited to the column family. Let
(T0,M0) be any completely frozen grid configuration. In any feasible
extension retaining T0 and P0=V(M0), a **fresh TP** means a final endpoint
v in P minus P0 whose within-band partner t is selected. Old mates need
not be retained.

**Fresh-tip separation lemma.** A fresh TP has no horizontal neighbour in
P0. If every old selected vertex was saturated by an old occupied neighbour,
it also has no horizontal neighbour in T0. In particular its only possible
actual mate in P0 is its transverse vertical neighbour across the band
boundary, never a horizontal old endpoint.

**Proof.** Every completely frozen old endpoint u has at least three old
occupied neighbours: at its first freezing step it has two distinct retained
witnesses, neither of which is its own actual mate (that would require u
itself to have frozen earlier), in addition to its old mate.

Suppose a fresh TP v has a horizontal old endpoint neighbour u. The band
partner q of u is horizontally adjacent to t. Since selected t already
sees occupied v, feasibility forces q blank in the final configuration,
and hence in the old one. The fresh v was old blank too, since old T and
P are retained and disjoint in the extension. Thus u had two distinct old
blank neighbours v and q. Its old occupied degree was at most two, a
contradiction. If v is adjacent to an old saturated selection, that selection
would have both its old occupied neighbour and the distinct fresh v; this
proves the extra assertion under saturation. Finally v's within-band
vertical neighbour is selected, so only its other vertical neighbour can
be an old P mate. QED.

This narrows the possible retained/fresh matching interface to transverse
vertical edges. It does not control the PP band edges between new endpoints;
Section 5 explains why those edges still defeat independent counting by
matching-difference component. The degree argument uses complete freezing
of the starting board, not of the extension. Its extraction and grid
adjacency argument are written proofs, not among the seven Lean audits.

## 1. Geometry and precise extension hypotheses

Coordinates are zero-based; horizontal bands pair rows 2b and 2b+1. Fix

    m>=2, L>=2, odd r>=3, c>=2, c_i=c+3i (0<=i<m).

Use an even-by-even finite rectangle with blank padding around the displayed
pattern. In particular all displayed sites, their neighbours, and strictly
internal gaps lie inside it. The starting P and its actual matching are

    P_i={(r+j,c_i): 0<=j<2L},
    M_i={ {(r+2h,c_i),(r+2h+1,c_i)}: 0<=h<L }.

The retained selections are

    (r-1,c_i), (r+2L,c_i),
    (r+j,c_i-1) for even j,
    (r+j,c_i+1) for odd j.

All other displayed sites are initially blank. For L=2 a single column is

```text
         T                 row r-1
       T P .               row r
       . P T               row r+1
       T P .               row r+2
       . P T               row r+3
         T                 row r+4
```

Actual edges pair rows r with r+1 and r+2 with r+3. Band pairing instead
joins the two middle P sites. Thus the PP/M graph is one alpha with TP ends
(r,c_i) and (r+2L-1,c_i). There are no beta or mixed owners in the isolated
pattern. Every selected vertex sees exactly one P. Columns three apart do
not add another occupied neighbour to any selection, so the whole pattern
is feasible.

An extension retains every displayed T as T and every displayed P as P,
may add arbitrary T and P, and chooses **any** nearest-neighbour perfect
matching on its final P disjoint from T. Feasibility requires every selected
vertex to have at most one occupied neighbour. The rectangle may grow with
the same coordinates and band phase, keeping these gaps internal. It may
contain arbitrary exterior components; it need not be completely frozen.
Available intervals use only the standard outer boundary marks. More general
reservations are allowed if the m assigned units below remain available.

The same arguments apply when this pattern is embedded in an existing
feasible board: it suffices to retain the stated T/P sites and initially
blank sites. Feasibility itself forces the blank collar described next.

## 2. Saturated guards force the old matching

**Lemma 1 (permanent blank collar).** Every initially blank horizontal
neighbour of P_i stays blank in every feasible extension.

**Proof.** At index j even, the nonselected horizontal neighbour is
q=(r+j,c_i+1). The selected guard t=(r+j+1,c_i+1) exists because j+1<2L.
It already sees p=(r+j+1,c_i). Since p and q are distinct neighbours of t,
q cannot be occupied. At index j odd, use q=(r+j,c_i-1), selected guard
t=(r+j-1,c_i-1), and its occupied anchor p=(r+j-1,c_i). Here j>=1.
These include the two extreme indices. No actual-mate assumption occurs.
QED.

The other horizontal neighbour of each P_i vertex is retained selected.
The vertical neighbours outside the column at both ends are the retained
caps. Consequently every actual mate of a P_i vertex lies in P_i and is
its immediately preceding or succeeding vertical neighbour. No endpoint
outside P_i can be matched to it.

**Lemma 2 (matching rigidity and strand persistence).** Every final matching
restricts to exactly M_i on P_i. The original alpha A_i persists with the
same body and ends, and has no outgoing TP-to-BP link.

**Proof.** An even finite path has a unique perfect matching: its first
vertex must be matched to the second, then delete them and repeat. This
gives M_i independently of the exterior matching. Internal band pairs are
unchanged; the two end partners remain selected caps. The two horizontal
neighbours of either TP end are retained T and forced blank, so neither is
a BP target. An alpha has no BP entrance, hence no outside route can enter
A_i either. QED.

This is stronger than assuming a fixed old matching. All actual-mate
retention used in the conclusion has been derived from retained occupation
and selected-vertex feasibility.

**Lemma 3 (all-length freezing).** The starting pattern is completely frozen.
Its P_i endpoints retain the following strict ranks in every feasible
extension, irrespective of whether the exterior becomes frozen:

    rho(r+2h,c_i)=h,
    rho(r+2h+1,c_i)=L-h-1.

**Proof.** Every endpoint has its horizontal selected neighbour as one
witness. An even endpoint with h=0 has the upper cap as its second witness.
For h>0 its preceding P neighbour has actual mate at index 2h-2 of rank
h-1. An odd endpoint with h=L-1 has the lower cap. Otherwise its succeeding
P neighbour has actual mate at index 2h+3 of rank L-h-2. Each nonselected
witness therefore has a strictly earlier frozen mate. Induction on rank
freezes all 2Lm endpoints. Lemma 2 and retained selections preserve these
witnesses in an arbitrary extension. QED.

## 3. Two shared permanent original units per gap

For 0<=i<m-1 define coordinate interval identities

    J_i^top    = (band=(r-1)/2,     first=c_i+1, last=c_i+1),
    J_i^bottom = (band=(r+2L-1)/2, first=c_i+2, last=c_i+2).

These are original interval identities, not tip slots or separately numbered
copies belonging to the two owners.

**Lemma 4 (persistent shared units).** Every J stays the same available
internal original singleton in every extension. Its eligible whole-support
owner set is exactly {A_i,A_(i+1)}. All 2(m-1) identities are distinct.

**Proof.** In the top band the two columns between the P boundaries c_i and
c_i+3 have labels BB, BT. Both sites of the BB column stay blank: its upper
site is guarded by cap (r-1,c_i), already seeing (r,c_i), and its lower site
is guarded by (r+1,c_i+1), already seeing (r+1,c_i). The blank of the BT
column is guarded by the next column's cap (r-1,c_i+3); the other site is
the retained side selection (r,c_i+2). Thus both columns keep their labels.

In the bottom band their labels are BT, BB. The blank of the BT column is
guarded by cap (r+2L,c_i). The upper site of its BB neighbour is guarded by
(r+2L-2,c_i+2), anchored to (r+2L-2,c_i+3); the lower site is guarded by
cap (r+2L,c_i+3). All these guards are saturated by distinct retained P
anchors, as in Lemma 1.

The two P boundary columns persist by Lemma 2. Each gap therefore has one
BB and one BT, with no TT, and its unique original unit is exactly the
displayed singleton. It is internal and unmarked. The two gap boundary
columns belong to A_i and A_(i+1); no other open owner borders this gap, so
no mixed or beta body acquires its support. Top and bottom bands differ
by L>0, and same-band identities have columns spaced by three. This proves
availability, ownership and distinctness simultaneously. QED.

## 4. Exact compensation and elimination

**Theorem 5 (persistent shared-block compensation).** In every feasible
extension, all m alphas A_i can be paid simultaneously by different original
units with zero links. Specifically assign

    A_0 -> J_0^top,
    A_1 -> J_0^bottom,
    A_i -> J_(i-1)^top for 2<=i<m.

Each assignment has the stated support. The first two resources are in
different bands; subsequent top resources have different gap indices, all
at least one. Thus no resource is used twice. This proves the theorem for
arbitrary m,L, not by finite extrapolation.

Write V,c for the maximum compensation value and the minimum links at
that value, separately in either the ordinary or full beta-fork model.
Delete the m owners A_i and exactly their m assigned units from the
**certificate system**, keeping all other physical owners, links and
original units, to obtain N_res. The physical board is not erased or
recomputed. Then

    V = m + V_res,                 c = c_res.                 (1)

**Proof.** Any residual packing extends by the m direct payments. They use
only deleted owners and units, so their union is legal and adds no links.

Conversely take a full packing. The A_i have no outgoing link and cannot
be entered. Every primitive involving A_i is therefore just its direct
interval payment. Remove all such payments. Each removed assigned unit
was supported only by A_i owners, by Lemma 4, so no surviving outside
primitive used one. The remaining outside packing is feasible in N_res.
If q<=m of the A_i were paid, its value is V-q, proving V<=m+V_res.
Together with extension this gives equality. At a maximum, q must equal
m and the surviving packing is residual-maximum. Removed primitives have
zero cost, so c_res<=c; extension gives c<=c_res. The same projection works
with full beta forks because none can have an A_i arm. QED.

This removes the requirement of private single-owner units from the earlier
private-source elimination, but replaces it with a sealed set of owners
and explicitly shared internal resources. It is not a general extension
theorem for arbitrary shared pockets.

Let a,b,I be the full alpha count, beta count and set of available original
units. Removing m assigned units and m alphas preserves the ledger exactly:

    |I|+b-a = (|I|-m)+b-(a-m).                              (2)

The remaining m-2 shared units are now unsupported and unused. Alternatively
delete **all** 2m-2 shared units; the same exact value and cost reduction (1)
holds, and the full ledger is the residual ledger plus m-2. The two
descriptions account for the same surplus. The leftover units must not be
credited to another component. Exterior units supported by A_i and outside
owners remain in the residual and are available to those outside owners.

For m=1 there is no internal shared gap and Theorem 5 is not asserted.
Its isolated column still has exterior units and is fully compensated on
the padded board; m>=2 is essential to the internal-unit certificate.

## 5. A frozen obstruction to matching-difference localization

Take any nonempty old completely frozen board with a known compensation
certificate and blank separation below it. Add one or more columns of
Section 1 entirely in new bands, together with their caps and side
selections. Retain all old matching edges for this example. The union is
feasible and completely frozen by the independent strict ranks. New
occupied components need not be connected to the old board.

Every component of M symmetric-difference M0 is just **one** new actual
matching edge. For L>=2 the two outer edges of each new column each contain
one fresh TP; internal edges contain none. Hence every matching-difference
component contains at most one fresh TP. Nevertheless the intervening PP
band edges join all L matching edges into one alpha with two fresh TP ends.
An old TP-to-BP cancellation certificate cannot touch this strand. Thus
the implication

    <=1 fresh TP per matching-difference component  =>  no new-new alpha

is false even under complete freezing. The missing interface is the PP
band pairing, not an unverified failure of freezing. A matching-difference
component cannot be given independent payment credit without tracking that
interface.

For an explicit old board use two protected L=2 columns, already paid at
zero links. Append m new L>=2 columns below it. With only the old original
units and old beta pool available, the new block has no eligible resource:
the new alphas have no links and all their support lies in new bands. Its
true restricted deficit is m. With e=2m fresh TP endpoints and k=m residual
new-new alphas, this attains k=floor(e/2) in the frozen domain. On the full
pool the appended block is paid at zero links, internally by Theorem 5 for
m>=2 and from exterior support for m=1. This proves sharpness of the
**retained-pool** budget; it does not show a full-pool deficit.

The previous [promotion closure](GUARDED_PROMOTION_CLOSURE.md) gave only a
nonfrozen sharp restricted family. This construction supplies a frozen
one, while isolating a positive arbitrary-rematching compensation class.
The same graft works on its actual 49T/308P starting board: put the new
columns in new lower bands, preserve the old matching, and replay the old
strict ranks followed by the column ranks. The old five-unit certificate
and all old beta resources remain separate from the new bands. Thus that
specific geometry also has frozen extensions with exact retained-pool
deficit m, e=2m, k=m, and zero full-pool deficit. It does not require replacing
the 308P base by the smaller demonstration core.
The connected counterexamples already in
[connected interval-repair obstruction](CONNECTED_FROZEN_INTERVAL_REPAIR_OBSTRUCTION.md)
still prevent extrapolating this class to all frozen boards.

## 6. Verification and precise formal scope

The [verifier](../develop/check_protected_shared_columns.py) independently
checks local feasibility, explicit strict ranks, actual mates, final
terminal pairs, singleton identities, exact support sets, ordinary and
full optima, and residual elimination. The
[receipt](../output/protected-shared-columns-validation.json) records:

* 409 extension/base models: 155 completely frozen and 254 feasible
  nonfrozen; 30 explicit all-endpoint rank certificates;
* all 326 single-addition candidates on a fixed board, with all 217 feasible
  extensions checked, and 64 accepted multi-addition prefixes;
* 80 actual exterior square rematchings, and 18 exterior controls with
  strictly positive residual cost;
* 808 exact eliminations (chosen units and all shared units), each checked
  in both ordinary and full models; 40 independent primitive comparisons;
* six additional small completely frozen matching-difference counterexamples
  with m=1,...,6, restricted deficit m and unrestricted deficit zero;
* six completely frozen extensions of the actual 308P board, with 312
  through 332 P, independently checked complete strict ranks, e=2m,
  exact old-five-unit-pool deficit m and unrestricted deficit zero.

These are finite corroborations of the preceding general proofs. A
[permanent actual fixture](../develop/fixtures/protected_shared_columns_fresh_obstruction.json)
records old/new actual edges and selected sites for the m=2,L=2 example.

[Lean source](../formal/SubQuorum/ProtectedSharedColumns.lean) checks seven
scoped facts: unique even-path matching, the side-guard index cases, strict
rank arithmetic, the shared assignment's injection and eligibility,
physical coordinate injection, and both ledger formulas. The geometric
collar extraction, interval support adapter, and exact primitive-packing
projection remain written proofs checked by the Python controls; this is
not an end-to-end Lean proof of the geometric compensation theorem.

Run from repository root:

    PYTHONDONTWRITEBYTECODE=1 python3 develop/check_protected_shared_columns.py --output output/protected-shared-columns-validation.json

Run from formal (Lean 4.33.0):

    lean SubQuorum/ProtectedSharedColumns.lean

The numerical 5/6 bound and the universal mixed-direction compensation
problem remain open. No submitted manuscript or correspondence is changed.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
