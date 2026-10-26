# Four-arm accounting for a P-free direction pivot

26 October 2026. Wenlin Zhang and Haobo Ma. Independent research continuation.

A single P-free 2×2 direction change has an exact five-block support ledger.
It preserves every global owner, terminal and physical link, and the total
positive resource count. It can nevertheless change support on arbitrarily
many surviving resources. We prove a payment stability bound using the owners
with their own surviving arm resources, and exhibit a fully frozen grid family
where **all positive forest cell sets survive unchanged but payment falls by
one**. In that family the pivot itself has zero positive resources.

The constructive bound identifies what must be reserved before making a pivot;
it does not charge support loss merely to physically disappearing forests.
It applies to occupied adjacent bands and capacity-two tiles without assuming
that their boundary owners are distinct. It is not a universal improvement of
the 5/6 bound. The 11 October submitted manuscript is preserved.

## 1. Hypotheses and identities

Take a feasible pair (T,M) on an even-by-even rectangular grid. P is the set of
endpoints of the actual matching M. Choose H/V directions on aligned 2×2 tiles
and use their canonical maximal same-direction bands, as in
[canonical band coarsening](CANONICAL_BAND_COARSENING_AND_REPAIR.md).
Use the full restored M/PP owner bodies, their TP/BP terminal types, physical
within-band TP→BP links and whole-owner no-P-gap support. Payment means the
maximum number V of alpha sources paid in the full fork-capable model: mixed
owners have capacity one, a beta has two distinct physical BP entry gates and
one private whole-beta sink. An owner-disjoint normal pack uses at most one
interval per owner; a beta fork uses one interval and one whole-beta sink.

Fix a P-free tile Q={r,r+1}×{c,c+1}, with r,c even. Change its direction H→V,
leaving all other directions fixed, and recanonicalize. H has vertical pairs
and a horizontal band axis; V has horizontal pairs and a vertical band axis.
The reverse case follows by transposing the board.

**Owner and link invariance.** The auxiliary matching N changes only on Q.
Every endpoint in P retains its auxiliary mate, since Q contains no P.
Thus all M/PP bodies, cycles, terminals and owner types are identical. A
physical TP→BP link can change only inside Q or across a newly split/merged
band boundary touching Q. Such an edge has an endpoint in Q and hence not in
P, so is not a terminal-terminal link. All physical links are identical.
Feasibility and freezing concern T,M alone and are unchanged. In particular
alpha, beta, the numerical slack S and the raw positive forest count L are
unchanged, with S=L+beta−alpha.

We need a common resource identity even when a coarse forest changes cells.
Refine both canonical partitions fully into their 2×2 tiles. The coarsening
theorem gives exactly one positive fine child in every positive coarse forest,
and a bijection between positive fine children and positive coarse forests.
Use that child as the resource anchor. All fine children outside Q are
identical before and after. Inside Q there are

    kappa = 2 − |T∩Q| ∈ {0,1,2}

positive children on each side: this follows either from the tile inventory
or directly from its BB/TT labels. Pair these local children arbitrarily.
The resulting common resource IDs are bijections on both full resource pools.
This transports resource identity; it does not assert equality of the physical
cells of every coarse forest.

## 2. Exact five-block support ledger

In the old H band, walk left and right from Q through no-P columns, stopping
at the first P column or band boundary. Let L,R be the open global owners of
those first P columns. At a band boundary or a closed-cycle boundary use no
owner. Define X_L,X_R to be the positive fine anchors in these two open arms,
with sizes ell,h. In the new V band do the same above and below Q, giving
owners U,D and positive-anchor sets X_U,X_D of sizes u,d. Let X_0 be the kappa
paired local IDs in Q. These five blocks are disjoint.

Boundary symbols are global owner identities. Two or more can coincide, even
across the two directions. In the following table remove absent owners and
deduplicate identities; braces denote sets, not multiple access credits.

| Resource block | Size | Old supporting owners | New supporting owners |
| --- | ---: | --- | --- |
| X_L | ell | {L,R} | {L} |
| X_R | h | {L,R} | {R} |
| X_0 | kappa | {L,R} | {U,D} |
| X_U | u | {U} | {U,D} |
| X_D | d | {D} | {U,D} |

Every other anchored resource has exactly the same supporting owners.

**Proof.** Before the pivot the two horizontal arms and Q form a single
maximal no-P gap bounded by L,R. Afterwards each horizontal arm terminates
at Q and retains only its far boundary. The vertical arms were separate gaps
terminating at Q; after the pivot they and Q form one gap bounded by U,D.
Whole-owner gap support gives each displayed entry. There are no other
changed bands except these splits and concatenations. A positive forest
cannot cross a P column, so every positive coarse forest lies in one no-P
gap; its unique fine anchor therefore identifies exactly the gap in question.
All unchanged outside bands/gaps retain their supports. This proves the table
also when balanced forest pieces merge into a positive forest. ∎

## 3. A constructive payment stability theorem

Let H be the set of distinct nonabsent old boundary owners L,R. Say L has
an arm reserve if ell>0, and R has an arm reserve if h>0. If L=R, either
arm suffices for that one owner. Let H_back be the resulting owner set and
H_0=H\H_back. Define

    b_H = min(ell+h+kappa, |H_0|).

Similarly let V_0 be the distinct new boundary owners U,D without their own
positive arm (u for U, d for D), and put

    b_V = min(u+d+kappa, |V_0|).

**Theorem.** Under Section 1,

    −b_H ≤ V_new − V_old ≤ b_V.                         (1)

More strongly, every old feasible paid source set loses at most b_H of its
members under a constructive repair. No new physical links are needed, and
the number of links of the repaired pack is at most the old number. The
symmetric statement holds from new to old with b_V.

**Proof of the lower bound.** Start with an owner-disjoint normal old pack.
Call an interval use horizontal if its assigned resource lies in
X_H=X_L∪X_R∪X_0. Its witness belongs to H by the table. Distinct used
intervals have distinct resources and distinct witness owners, including
the interval used by a beta fork.

For each horizontal witness in H_back, select one positive unit in its own
arm. If L,R are distinct their own arms are disjoint, so these reservations
are distinct. If L=R there is at most one such witness and we reserve only
one unit. The reserved unit is supported by that witness after the pivot.
Reassign **all** these backed horizontal uses simultaneously to their own
reservations. Reassigning them together is necessary: a reservation might
previously have been assigned to the opposite boundary owner.

Discard the payment of every horizontal use witnessed by H_0. An ordinary
interval primitive loses its one source and can be removed. For a beta fork,
remove only its interval branch, retaining the other source at the same
whole-beta sink and its old physical BP entry. This loses one source, not
two. It frees owners and links and introduces no new ones.

All retained nonhorizontal interval uses have old resources outside X_H.
Their support cannot shrink: only X_L,X_R,X_0 have potentially lost old
incidences. Reservations lie inside X_H, so they cannot collide with these
unchanged assignments. Reservations are mutually distinct as just proved.
Every other resource formerly in X_H belonged either to a reassigned use
or a discarded interval branch. There is consequently no double spending.
Retained whole-beta payments, owner disjointness and physical links remain
valid, including a retained half-fork. Thus the repaired pack pays the same
sources except for one per discarded horizontal witness.

The discarded witnesses inject into H_0 by their distinct owner identities,
and into X_H by their distinct old assigned resources. Their number is at
most both |H_0| and ell+h+kappa. This gives the lower bound and the stronger
source-set and link statements. Apply the same construction to the reverse
V→H pivot to obtain the upper bound. ∎

**Consequences.** If both distinct old boundary owners have positive own
arms, b_H=0 and every old paid source set survives. This is a sufficient
condition for safe payment preservation, even when Q has capacity two or
the new vertical gap is occupied. If the analogous reserve condition holds
vertically as well, V_new=V_old. These conditions use distinct owners and
disjoint actual unit reservations, rather than adding two local surpluses.

Universally a single pivot satisfies

    |V_new−V_old| ≤ max(1,kappa).                       (2)

Indeed |H_0|≤2. If kappa=0 and ell+h=0 then b_H=0. If kappa=0 and
ell+h>0, either H is empty or a positive arm backs its boundary owner if
present. Two unbacked distinct owners would require both ell=h=0, which
is impossible. Hence b_H≤1. For kappa=1 the same reasoning handles
ell+h>0, while ell+h=0 gives b_H≤kappa=1. For kappa=2 use |H_0|≤2.
The vertical argument is identical. The abstract ledger with two alpha
owners L,R, no outside arms, kappa=2 and no U,D realizes loss two. This
is a sharp abstract control, not a claimed frozen-grid embedding.

## 4. Zero local resources and arbitrarily many lost surviving supports

Here the loss-one bound for kappa=0 is attained on an actual fully frozen
grid. The complete base coordinates, direction bits and strict rank layers
are serialized in
[P_free_support_only_pivot.json](../develop/fixtures/P_free_support_only_pivot.json).
They specify a finite construction, not an optimization/exhaustion claim.
There is also a transparent derivation from the earlier explicit
[fully frozen elbow](FULLY_FROZEN_ELBOW_WITHDRAWAL_OBSTRUCTION.md): keep its
16×28 matching M with 35 edges and its direction bits, and delete exactly
the ten T sites in rows 2,3 and columns 18,...,27. Call this T_0. Thus |T_0|=73.
The old V cut at tile (10,16) is kept.

For any integer m≥0 append 2m empty columns to the right and make every new
tile H. Keep T=T_0, M and all old directions fixed. Flip only tile (2,16)
from H to V. For every m the following statements hold:

| Quantity | Before | After |
| --- | ---: | ---: |
| Board | 16×(28+2m) | same |
| Selected sites / matching edges | 73 / 35 | same |
| Frozen endpoints | 70, in the old 11 strict waves | same |
| alpha / beta / mixed owners | 2 / 2 / 5 | same |
| Raw original units L = slack S | 116+16m | same |
| Positive original forest cell-set collection | full old collection | identical |
| Supports at alpha a | 10+2m units | none |
| Maximum payment V / minimum links | 2 / 1 | 1 / 1 |

**Proof for all m.** Removing selections preserves feasibility. The removed
sites are not adjacent to P; the old strict freezing certificate is internal
to the retained configuration and its endpoint neighbourhoods are unchanged.
The empty extension does not change any such neighbourhood. The same eleven
strict rank layers therefore freeze all 70 endpoints for every m, independent
of N. Since no T-neighbour of P changed, the owner terminal types are the
old ones; there are two alpha owners

    a: TP tips (3,12),(10,12),
    b: TP tips (5,17),(12,17),

and the source-reachable external link set is exactly

    b(5,17) → z(5,16),
    z: TP (5,15), BP (5,16).

The unchanged z has exactly the private unit {(4,13),(5,13)}; b has none.
Neither a nor z has another external exit, and no beta is reachable from
either alpha. All four alpha tips retain occupied degree three. These
statements concern a fixed finite kernel; the appended columns contain no
P and cannot introduce new terminal-terminal links or new P boundaries.

In rows 2,3 the old horizontal gap has a as left boundary and no right
boundary. Columns 13,...,17 are BT. Its right arm consists exactly of
the singleton BB units

    {(2,j),(3,j)},  j=18,...,27+2m.                     (3)

These are the 10+2m units supported solely by a. The lower a arm remains
cut off by the unchanged V tile (10,16), so a has no other support. The
pivot (2,16) has the diagonal selections (3,16),(2,17). Its two columns
are BT before, and its two rows are BT after. It contains no forest in
either direction. No BB/TT forest can merge through a BT column or row.
All bands change only by splitting/joining through this BT tile, so **every
positive forest retains exactly the same physical cell set**. The vertical
gap has no positive outside arms and no open boundary owners. The complete
four-arm data are

    (ell,h,kappa,u,d) = (0,10+2m,0,0,0),
    (L,R,U,D) = (a,absent,absent,absent).

After the flip, all units (3) remain as the same singleton forests in a
right H band with no P boundary. They lose their sole support a; all other
owners' supports, under the identical cell-set resource IDs, stay unchanged.

Before the flip pay a directly using any unit (3), and pay b using the one
link through z and z's private unit. These two primitives are owner/resource
disjoint, and two is the upper bound because there are only two sources.
After the flip a has neither support nor an external exit, while the same
b→z payment remains, so the exact optimum is one. Each optimum needs the
one b→z link. Finally L=S follows from alpha=beta, and

    S=16(28+2m)/2 − 73 − 35 = 116+16m.

This proves the formulas and unbounded support loss for every m. ∎

This refutes the rules “a pivot with no positive local unit is harmless” and
“if no positive forest disappears, every old payment survives”. The target
numerical inequality is not refuted: the family has large positive slack
and makes no fixed-P extremality claim. The failure is in those proposed
payment-preservation rules. In particular full freezing and degree-three
source tips do not repair them.

## 5. Relation to optional destructive exchanges

The earlier [exact token choice theorem](DESTRUCTIVE_EXCHANGE_CHOICE.md)
requires its simultaneous physical adapter, including supports of all
nonactivated owners. A generic P-free pivot preserves owners and links,
but the five-block table shows why this does not imply that adapter.
Surviving units in X_L or X_R can lose an old boundary owner; units in
X_U or X_D can gain another owner. Those incidences must be included in
any new adapter or common optimization model. Counting only forests whose
cell sets disappear would miss every lost support in Section 4.

The present theorem supplies a general safe test and a quantitative loss
budget. It does not assert that two disjoint pivot tiles are independent:
canonical bands can join them, and a positive reserve allocated to one
pivot may be demanded by another. For a sequence of pivots, (1) telescopes
only with arm data recomputed at each intermediate state. That is a valid
sequential bound; it is not a parallel repair theorem. A joint theorem must
reserve distinct actual units across the whole chosen family or explicitly
encode all competing support changes.

## 6. Reproduction and formal scope

Run from the repository root:

```sh
python3 develop/check_P_free_pivot_interface.py \
  --output output/P-free-pivot-interface-validation.json
python3 develop/check_pivot_support_repair_formal.py \
  --lean /absolute/path/to/lean-4.33.0 \
  --output output/pivot-support-repair-formal-validation.json
```

The physical validator checks 2,237 pivots, including every P-free tile of
the 186-point fully frozen maximum and both directions on sampled feasible
boards. It independently checks both optima by primitive-pack optimization,
the full common-anchor support table (41,900 resource entries), invariant
owners/types/links, all kappa values and 15 cases with both horizontal arm
reserves positive. A further 500 abstract ledger models include 120 coincident
boundary pairs and 81 beta-fork certificates; an explicit kappa-two abstract
control attains loss two. The support-only family is checked at m=0,1,2,4,16,64,
with 420 strict freeze events replayed, and all eight dihedral images of its
base obstruction are checked. Enumeration tests the adapters and formulas;
Sections 1–4 give the general proofs.

The validator also reconstructs 5,474 bidirectional repairs of checked packs,
verifying every resulting primitive, paid-source containment, physical-link
containment and joint owner/resource disjointness. These include 658 own-arm
reassignments and six beta forks truncated to one retained whole-beta payment.

Three general declarations in
[PivotSupportRepair.lean](../formal/SubQuorum/PivotSupportRepair.lean) prove
that the simultaneous repair keeps valid support for every retained witness,
that assignments remain injective, and that each dropped old witness is
unbacked and had an affected old assignment. All three are axiom-free in
Lean 4.33.0, with no sorry, native decision or warnings. The module checks
the no-double-spending assignment kernel for arbitrary types; the geometric
table, beta-path truncation, finite cardinality bound and grid construction
are written proofs with independent executable checks, not end-to-end Lean.

Next: extend joint action selection to these exact support changes, reserving
arm units globally; or find a genuine grid configuration requiring several
coordinated pivots for a net payment gain. A universal coverage/5/6 result
is still open.

The subsequent [frozen coordinated-pivot construction](FROZEN_COORDINATED_PIVOTS.md)
realizes an arbitrary-length all-gates prerequisite on genuine frozen grids,
with zero-capacity pivots and unchanged positive forest cells. It also gives
a true fixed-P maximum with no improving single P-free pivot but a successful
two-pivot repair.
