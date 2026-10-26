# Uniform zero-capacity openings: two-state recognition and exact compilation

26 October 2026. Wenlin Zhang and Haobo Ma. Independent research continuation.

We give a polynomial recognition test and exact optimizer for a class of
direction choices on an arbitrary feasible physical grid. The input gates
are aligned P-free tiles of capacity zero, all initially V, with opening
meaning V→H. A single comparison of the all-closed and all-open **original
support incidences** decides whether every gate subset is support-monotone.
If it passes, the actual grid automatically decomposes into the
[protected linear corridors](PROTECTED_LINEAR_CORRIDORS.md) of the preceding
theorem. One min-cost fork flow then optimizes maximum payment, minimum actual
gate fee and minimum links, including arbitrary external mixed/beta competition.

This replaces an assumed all-subset corridor contract by a check on two
physical states and a proved geometric compiler. It includes zero-capacity
balanced TT/BB tiles, for which coarse forest cell sets can change. Common
positive fine anchors, rather than coarse cell equality, preserve resource IDs.

The test is not a comparison of total flow values. A new completely frozen
28×48 control has payments 3,2,4,3 in its four gate states. Its all-closed
and all-open payments agree, while ten old incidences are lost and an
intermediate subset pays four. The full incidence test correctly rejects it.
Rejection concerns the monotone support contract, not the grid inequality.

## 1. Physical input and common original identities

Fix any feasible T and actual matching M on an even-by-even rectangular grid.
Let P be the actual matching endpoints. Choose one H/V direction bit per
aligned 2×2 tile and use maximal canonical same-direction bands. Restore all
M/PP edges before identifying original owners, types, actual TP--BP links,
whole-owner interval support, mixed capacity-one gates, distinct beta BP
entries and one whole-beta output. This is the existing full fork-flow model.
Freezing and global extremality are not assumptions of the general theorem.

Choose a set G of different tiles Q satisfying:

    Q intersect P is empty,    |Q intersect T|=2,
    Q initially has direction V.

Opening g means changing its tile to H. All other direction bits, T and M
remain fixed. Fees w_g are nonnegative integers, charged per actual opened
tile. The transpose gives the corresponding uniform H→V result.

Every state F subset G remains physically feasible, since T,M are unchanged.
Every P endpoint keeps its auxiliary mate, so every original owner body,
terminal type and actual terminal link is the same. This is the owner/link
invariance of the [P-free pivot ledger](P_FREE_PIVOT_INTERFACE.md), applied
simultaneously to tiles containing no P.

Refine the bands fully into 2×2 tiles. A P-free tile has

    number of positive fine forests = 2-|T intersect Q|.

Thus each variable tile has zero positive children in either direction.
This allows both diagonal BT/BT patterns and adjacent-T balanced TT/BB
patterns; the latter can merge or split coarse forest shapes. Every positive
fine child lies in an unchanged tile. Its cell set, orientation and identity
are therefore common to all F. By the [positive-child coarsening theorem](CANONICAL_BAND_COARSENING_AND_REPAIR.md),
each positive coarse forest contains exactly one positive fine child, and
every positive fine child has one positive coarse parent. Use that fine child
as the original unit's **anchor ID** in every state.

The complete raw original pool Q is now fixed. No resource is created,
discarded or duplicated; alpha, beta, raw L and S=L+beta-alpha stay fixed.
Partition Q into H-anchors and V-anchors, according to their unchanged tile
orientation. This partition is independent of F. Let W_F(o) subset Q be the
full original support of owner o in state F.

## 2. Two opposite monotonicities

**Lemma 1 (axis dichotomy).** For F subset F' and every original owner o,

    W_F(o) intersect Q_H  subset W_F'(o) intersect Q_H,
    W_F'(o) intersect Q_V subset W_F(o) intersect Q_V.          (1)

**Proof for H anchors.** Opening only adds H tiles. The maximal H run
containing any fixed H-anchor can only extend across newly opened tiles.
Its old P columns are unchanged, and a gate contains no P. Any old first
P boundary remains a boundary of the anchor's enlarged no-P gap; an old
artificial band boundary can be replaced by a new P boundary or remain absent.
It cannot replace an old P boundary. Its old open-owner support therefore
persists. The resource may acquire an additional boundary owner. Transport
the coarse forest by its unchanged unique positive fine child.

**Proof for V anchors.** Opening only removes V tiles. Its V run can only
split or shrink, and no P column is inserted or moved. A first P boundary
can be cut off and replaced by an artificial band boundary, but no new P
boundary becomes reachable. Thus support can only shrink. Coarse forest
splitting does not change this argument, by the common anchor bijection. ∎

Balanced variable forests need not have fixed cell sets. Only the positive
anchor and its direction must stay fixed, which capacity zero guarantees.

**Theorem 2 (two-state recognition).** The following conditions are equivalent:

1. All old incidences survive in the full-open state:

       W_empty(o) subset W_G(o) for every original owner o.     (2)

2. The V-anchor support is the same at both extreme states.
3. For every F subset F' subset G, W_F(o) subset W_F'(o) for every o.
4. Every V-anchor support incidence is constant over all gate subsets.

**Proof.** Lemma 1 already gives increasing H support and decreasing V support.
Thus (2) is equivalent to equality of V support at the extremes. Every
intermediate V support lies between those extremes:

    W_G(o) intersect Q_V subset W_F(o) intersect Q_V
                           subset W_empty(o) intersect Q_V.

Equality of the extremes forces equality for every F. Combining this constant
part with increasing H support proves full support monotonicity for every
ordered pair F subset F'. Conversely full monotonicity implies (2). Constant
V support plainly gives extreme equality. ∎

Only two physical models are required to recognize the class, with common
anchor IDs. Every failed incidence in (2) belongs to a V-anchor and is an
explicit witness to the support-only contract's failure. Total payment,
maximum-flow rank, counts of unused units or coarse forest cell equality
cannot substitute for this incidence comparison.

## 3. The grid itself supplies disjoint protected corridors

Assume (2). Compute the full-open canonical bands. In each H band take its
maximal no-P gaps, bounded by the first P columns or band edges. For each gap:

* List its H-anchor IDs in left-to-right order.
* Its two boundary owners are the open owners of those first P columns;
  use an absent symbol for a band edge or a closed-cycle boundary.
* List every variable gate tile in that gap in physical order. A P-free
  gate cannot cross a P column and therefore belongs to exactly one gap.

No H-anchor belongs to two gaps, and no variable gate belongs to two gaps.
Boundary owners can coincide or be shared by many gaps. Keep V-anchor support
as the fixed external resource pool; all original routing capacities and
actual links stay in the same competing network.

**Theorem 3 (exact physical compiler).** For every F subset G, a gap's left
owner supports one of its H-anchors precisely when all variable gates between
that boundary and anchor are open. The analogous suffix condition holds on
the right. No other owner supports that anchor. All V supports remain fixed.
Consequently the compiled corridor network has exactly the physical W_F for
every state, with the same owners, links and original resource IDs.

**Proof.** In the full-open gap, the only possible P boundaries are its two
ends. A closed variable gate deletes its two columns from the H run, leaving
an artificial band boundary. All other tiles and P columns stay fixed. An
anchor is in the H no-P segment incident to the left end exactly when none
of the intervening gate tiles is closed. If a gate is closed, it separates
that boundary from the anchor. If none is closed, every intervening tile
belongs to the same canonical H band, and no P column occurs in between.
Whole-owner support is precisely this no-P-gap incidence. The right statement
is identical. There is no other reachable P boundary, so no outside owner
can use that anchor. Theorem 2 supplies fixed support for every V-anchor.

Each gate and H-anchor is assigned to its unique full-open gap, so these
corridors have disjoint actual gates and resource IDs. Coarse forests may
change shape through balanced variable tiles, but their anchor is in the
correct unique segment in every state. Hence all support equalities, including
noncorridor support, hold simultaneously. ∎

This proves the previous protected-corridor contract from a physical
two-state test. It also explains why no resource-support branching survives
in this uniform lossless class: the gaining-axis gap is a line with only
two possible boundary owners, and losing-axis support is constant. The
owner routing network can still branch, cycle, and contain competing beta
forks; it is retained, not assumed independent.

## 4. Exact optimization and no duplicate gate fees

Apply the [extreme-resource theorem](PROTECTED_LINEAR_CORRIDORS.md) to each
compiled gap. With two or more original units, retain the leftmost for the
left boundary and rightmost for the right boundary; reassign uses simultaneously
without changing owners, sources or links. With one original unit retain
one shared capacity-one output. An empty gap has no interval offer.

For each retained offer, its prerequisite is the actual gate prefix or suffix
to its extreme unit. These two sets are disjoint within the gap, and gates
from different gaps are disjoint. Internal gates between the extreme units
can be omitted after reassignment. Unused original units remain in L.

Give an offer arc cost K times the sum of its different prerequisite gate
fees, and a physical terminal-link arc cost one, where

    K=number of original alpha owners + number of mixed owners + 1.

**Corollary 4 (polynomial joint choice).** Two endpoint models, the support
inclusion audit, the final-gap compiler and one integral minimum-cost maximum
fork flow give the exact lexicographic optimum:

    maximize payment; minimize actual opening fee; minimize links.

The result includes all original mixed gates, separate actual beta BP entries
and whole-beta outputs. Used offer prerequisites reconstruct actual operations.
No actual gate is charged twice; no original interval pays twice. Any old
feasible paid-source set can be retained at the same first two optima, and
source lower bounds/priority compute the conditional minimum-link optimum.

**Proof.** Theorem 3 establishes the full protected-corridor contract, so the
previous exact two-way costed fork-flow theorem applies. Every normalized
pack uses at most one interval per witness owner, including a beta fork's
one interval plus one whole-beta unit. This proves simultaneous extreme
reassignment and bounds physical link count by K-1. Nonnegative integer fees
and the scale K therefore give the lexicographic objectives. The gate/resource
disjointness above proves exact once-per-gate cost reconstruction. The old
source-preservation and conditional-flow arguments transfer unchanged.
All constructions have polynomial size in the explicit grid, support network,
gate lists and fee bit lengths, and use standard min-cost flow. ∎

No enumeration of 2^|G| states is part of this optimizer. The independent
validator does enumerate small choices to check the general theorem.
The callable `solve_openings(cur,bits,gates,weights,required)` performs the
two-state audit and costed flow without primitive-pack enumeration; it returns
actual opened tiles, or explicit owner/anchor loss witnesses on rejection.
Independent primitive enumeration is confined to the verification path.

## 5. Frozen accepted and rejected controls

### 5.1 A balanced gate changes forest cells but passes

Start from the previous two-unit frozen double corridor with n_L=n_R=2,
q=6: a 16×58 board with T166/M70 and its four upper BT gates. Append eight
empty columns, giving width 66. Add the adjacent selected pair

    (2,62),(2,63),

and set tiles (0,62),(2,62),(4,62) to V. Only (2,62) is an additional
variable gate; keep the other two V. The added pair is isolated from all old
occupancy and has selected degree one. The old 140 endpoints remain strictly
frozen in their eleven waves, and the original owner/type/link kernel stays
fixed. Now T168/M70, alpha=beta=4, mixed=10, and raw L=S=290.

In its V band, the gate contains one TT row and one BB row. The TT row
joins adjacent BB rows into a positive forest with a positive fine anchor
outside the gate. Opening it makes its two H columns BT/BT, so that positive
coarse forest loses the gate cells while retaining its anchor. Sixteen of
the 32 gate states have changed positive coarse cell sets relative to the
initial state. No P occurs in the appended strip's V arms, so this shrinkage
loses no owner support. The two-state test accepts the whole five-gate input.
The physical compiler is checked against complete support for all 32 states.

With gate fees 1,2,3,4,1 in the validator's ordering (the first four are the
original two-side BT chains), exact maximum payment is four, minimum opening
fee ten and minimum links two. The extra balanced gate is not needed for
that optimum. Its purpose is to show that coarse cell invariance is not
a necessary hypothesis of the recognition/compiler theorem.

### 5.2 A uniform fully frozen opening genuinely loses support

Transpose the existing [zero-local-capacity support-loss family](P_FREE_PIVOT_INTERFACE.md),
at extension m=0, swapping H/V bits. Its board is 28×16, T73/M35; all
70 endpoints remain strictly frozen. The sole variable gate (16,2) is
initially V, P-free and capacity zero. Opening it H removes ten old support
incidences, on V-anchor resources. Raw L=S=116 and all positive coarse forest
cell sets survive. Payment drops from two to one at unchanged minimum one
link. The two-state test rejects it. Thus feasibility, full freezing and
zero local capacity alone do not imply the lossless-opening contract.

### 5.3 Equal endpoint payments hide destructive repair choices

Place the transposed loss module at rows 0..27, columns 0..15. Place the
old one-gate gain corridor, height 16 and width 30, at rows 0..15,
columns 18..47. Leave columns 16,17 empty and permanently V, and fill the
remaining lower-right empty rectangle with H tiles. The two columns form
a horizontal support barrier; lower-right H tiles terminate the right
module's old V bands. There is no P adjacency between the two modules.
New blank-gap resources have no owner support. Thus owners, links and
supported resources are a direct sum of the old modules.

This gives a feasible completely frozen 28×48 board, T156/M70,
alpha=beta=4, mixed=10, all 140 endpoints frozen in eleven parallel waves,
and raw L=S=446. Both declared gates are V→H, P-free and capacity zero:

    d=(16,2),        g=(2,34).

The first destroys the loss module's one direct payment; the second repairs
the gain module's previously unpaid alpha. Their exact state table is

| Opened gates | Maximum payment | Minimum links |
|---|---:|---:|
| none | 3 | 2 |
| d only | 2 | 2 |
| g only | 4 | 2 |
| both | 3 | 2 |

The values follow by adding the independently proved old kernels; the empty
separator excludes new support or routing interactions. Ten old incidences
are lost even in the full-open state. Hence a scalar endpoint test would
pass, yet miss both a destructive intermediate step and the best gate subset.
The incidence test rejects with exact original-owner/resource witnesses.
The numerical grid inequality is not refuted, nor does rejection say that
the useful g operation cannot be selected by a broader destructive optimizer.

## 6. Validation, Lean scope, and remaining work

Run from the repository root:

```sh
python3 develop/check_uniform_zero_capacity_openings.py \
  --output output/uniform-zero-capacity-openings-validation.json
python3 develop/check_uniform_opening_guard_formal.py \
  --lean /absolute/path/to/lean-4.33.0 \
  --output output/uniform-opening-guard-formal-validation.json
```

The [physical compiler/validator](../develop/check_uniform_zero_capacity_openings.py)
checks common anchors, owner bodies, types, actual links, the opposite H/V
monotonicities, endpoint-test equivalence to every Boolean-lattice edge on
complete small gate families, all-state physical/proxy support equality, and
the flow's optimum against independent physical gate choice plus primitive
packing. Longer known frozen corridors check empty/full/each singleton/every
one-gate omission, including length pair (16,17). The accepted balanced gate
and both rejected frozen controls are checked in full. Exact counts are in
[the validation record](../output/uniform-zero-capacity-openings-validation.json).

Four general declarations in [UniformOpeningGuard.lean](../formal/SubQuorum/UniformOpeningGuard.lean)
prove antitone constancy from endpoint inclusion, axis-split all-state
monotonicity, the recognition equivalence, and localization of a rejected
incidence to the decreasing axis. They quantify over arbitrary state and
item types, with no finite state enumeration. All four are axiom-free in
Lean 4.33.0; [the audit](../output/uniform-opening-guard-formal-validation.json)
records preflight and exact scope. Physical axis monotonicity, common-anchor
construction, final-gap compilation, flow reconstruction and frozen-grid
controls remain written proofs and independent executable checks, not
end-to-end Lean.

The theorem recognizes and optimizes arbitrary feasible inputs satisfying
this uniform capacity-zero lossless criterion. It does not assert that all
residual mixed-direction configurations satisfy it, that the recognized class
has enough payment to settle every demand, or that an input can be made to
pass without a numerical cost. Capacity-one/two pivot tiles have positive
units whose anchors change orientation, and mixed target directions do not
have the proved global axis dichotomy. Destructive supports also remain a
separate problem. These are concrete boundaries for the next geometric step.
The universal 5/6 bound remains open. The 11 October manuscript, public main,
PR #3 and shared CI are preserved; no email operation is included.
