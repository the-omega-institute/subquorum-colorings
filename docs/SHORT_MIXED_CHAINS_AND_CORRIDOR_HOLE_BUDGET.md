# Short mixed chains, corridor holes and exact weighted contraction

25 October 2026. Haobo Ma and Wenlin Zhang. Isolated research branch.

We prove that original one-edge horizontal mixed strands assemble into
same-row directed chains. All internal chain links can be added simultaneously
to the geometric partial certificate, without competing with the vertical-TP
injection. Using the established BT-corridor interval slots first, the remaining
holes are only unported chain tails and marked-boundary exceptions. This
strengthens the component deficit bound below. We also prove an exact weighted
contraction for the full BP-aware flow, preserving both maximum payment and
minimum actual links. A restricted-pool example on a completely frozen board
shows why the internal-link toll cannot be dropped. Universal compensation
and an improvement of the unrestricted 5/6 bound remain open.

## 1. Hypotheses and notation

Use the original feasible selected set T, actual matching M and matching-closed
aligned two-row packet of [the vertical-tip theorem](VERTICAL_TP_INJECTION_AND_SHORT_MIXED_HOLES.md),
Section 1: blank first column, a blank corner in the last column, and a finite
complete freezing certificate for every actual matching endpoint. The original
certificate may use neighbors outside the packet. Keep the original PP strands,
TP/BP terminal identities, all permitted horizontal TP--BP links, original
BB--TT interval identities, original marked boundary intervals K, and available
intervals I (all intervals except K). There are no additional reservations.
A short mixed owner means an original strand consisting of one horizontal
actual matching edge, with one BP and one TP end. It is not a virtual strand.

Use whole-owner interval support W, the full BP-aware fork network, and the
ordinary submodel from [the whole-support normal form](WHOLE_SUPPORT_FORK_FLOW_AND_RESOURCE_CUTS.md).
Write k for the original alpha count, V_full and V_ord for their respective
maximum payments, and c_full for the least number of actual terminal links
among full maximum-payment packings. Thus V_full >= V_ord; equality is not
assumed. Original interaction components D use every original owner link and
whole-support incidence, including beta bodies and the same shared interval
identity. Write a_D for the original alpha count of D.

A physical corridor port of a TP is the first BB column reached in either
horizontal direction through zero or more BT columns, with its original
interval identity. By [BT corridor compression](BT_CORRIDOR_PORTS_AND_BOUNDED_ACCESS_OBSTRUCTION.md),
Sections 2--3, each interval side has at most one such TP user globally.
There are at most two users of an interval, at most one for a marked boundary
interval. This is a certificate with two labelled slots for an interval,
not two payable resource units. Full gap support at a terminal can contain
more intervals than its compressed corridor ports; retain full W in the
exact contraction below.

## 2. The physical chain theorem

**Lemma 1 (short chains).** Nonself links between short mixed owners form
vertex-disjoint directed paths. A path of m >= 1 owners has, after possibly
reflecting the physical row, the consecutive layout

    BP_0, TP_0, BP_1, TP_1, ..., BP_(m-1), TP_(m-1).

Its actual matching edges are BP_i--TP_i. Its m-1 internal terminal links
are TP_i -> BP_(i+1). Every external nonself link entering this chain uses
BP_0; every external nonself link leaving it uses TP_(m-1).

**Proof.** Each short owner occupies two consecutive sites in one physical
row, already matched to each other. Its TP has only two horizontal neighbors:
its own BP and the site on the opposite side. Its BP similarly has its own TP
and at most one other candidate incoming TP. Removing the self link therefore
leaves indegree and outdegree at most one in the short-owner graph. If the
opposite neighbor of TP_i is a short BP, that BP's own mate must be the next
site in the same direction, since TP_i is already matched. Thus every
successive owner has the same orientation. Its column strictly increases
(or strictly decreases after reflection), excluding a directed cycle.
Components are finite paths, with the displayed layout. The same neighbor
argument excludes any other external entrance or exit at an interior owner. □

**Lemma 2 (simultaneous internal links).** Every non-tail TP has no physical
corridor port and is unassigned by the corridor/vertical certificate below.
Every non-head BP is unused by the vertical injection. Hence all m-1 internal
links of every short chain can be added at once, with distinct sources and
targets and without disturbing any previous assignment.

**Proof.** A non-tail TP has its own BP on one side and the next BP on the
other, so neither side starts an endpoint-free gap. It is horizontally mated,
so is not a vertical-injection demand. A non-head BP has only its own short
TP and the preceding short TP as horizontal TP neighbors. Both are
horizontally mated, so neither is a vertical-injection demand. Distinct
internal links use distinct such physical tips; different chains are
disjoint. Thus none conflicts with an interval slot, a vertical demand or
a BP target already used. These are legal links in the original board,
not links justified by assuming a modified board still frozen. □

The direct-extension lemma of [the paired-hole certificate note](PAIRED_HOLES_AND_CERTIFICATE_OPTIMIZATION.md)
then says their simultaneous addition cannot increase the fine certificate
deficit. A neutral cycle or a neutral mixed residual need not pay an alpha;
no extra payment is inferred merely from having added a link.

## 3. Corridor-first certificate and the sharper component bound

Build one partial two-slot certificate as follows.

1. Assign every TP with an available physical corridor port to one slot of
   a chosen such original interval. This is simultaneous: each interval has
   at most two possible TP users before any choices.
2. Among the unassigned TPs with no immediate BB port, inject all whose
   actual matching edge is vertical into distinct adjacent BP tips. This is
   the subset version of the vertical-tip theorem, including mixed exits.
3. Add all internal short-chain links of Lemma 2.

The three target/source allocations are compatible by Lemma 2. The remaining
holes split disjointly into E and H. E consists of chain-tail TPs with no
physical corridor port at all. H consists of the remaining holes with at least
one physical port, all of whose interval identities are marked. In particular,
a short tail with only marked ports belongs to H, not E. A vertical hole must
have had an immediate marked BB port; otherwise step 2 covers it. There are
no other holes: an unassigned horizontal TP is a one-edge short mixed TP by
the earlier geometric theorem, and step 3 covers it unless it is a tail.

Put e_D = |E in D| and h_D = |H in D|. The number of H tips is at most |K|,
since each has a marked port and each marked interval has at most one physical
corridor user. This uses only the actual boundary marks; arbitrary extra
reservations would require extra exceptions and recomputing available ports.

**Theorem 3 (chain-tail deficit bound).** Under Section 1's hypotheses,

    k - V_full <= k - V_ord
               <= sum_D min(a_D, floor((e_D+h_D)/2)).          (1)

An ordinary packing attaining the stated payment lower bound exists using
at most

    |X_remaining| + sum_chains (m_chain-1)                    (2)

actual links, where X_remaining is the vertical demand set in step 2. This
bounds the cost of that partial payment, not necessarily c_full when its
payment is below maximum.

**Proof.** Steps 1--3 give a valid original partial two-slot certificate.
Apply the established partial-certificate projection and allocation lift:
each final alpha has two free TP ends; a surviving original interval has at
most two assigned slots but is used for at most one actual payment. In each
connected final-alpha/assigned-interval component, unpaid alpha count is at
most half the holes, rounded down. These components lie inside D, since
cancellation links and support incidences were included in D from the start.
Summing their floors is at most floor((e_D+h_D)/2), and the deficit is at most
a_D. Sum over D. The ordinary normal form removes unused links and neutral
cycles without increasing their number. The only chosen actual links were
those in steps 2 and 3, giving (2). Every ordinary packing is a full packing,
which proves the first inequality. □

All final holes are a subset of the earlier direct-port certificate holes
in the same original components. Formula (1) is therefore never weaker than
the earlier short-owner exception bound. In particular, if every
alpha-containing original interaction component has at most one unported
chain tail or marked-port exception in total, ordinary full compensation
holds. Without boundary exceptions it suffices to have at most one unported
chain per alpha-containing component, regardless of the lengths of these
chains or of the bent/long mixed strands elsewhere.

The count avoids duplicate compensation in three places: both interval slots
carry the SAME original resource identity; the BP injections and internal
chain links have disjoint physical targets; and the floors are taken inside
the full original interaction graph. Shared beta bodies or intervals cannot
be split into fictitiously independent surplus accounts.

## 4. Support at an entered chain's tail

**Lemma 4.** If the head BP of a short chain has an external incoming nonself
link, every non-tail owner has empty W, and the union of W over the chain is
exactly the full endpoint-free gap support of its tail TP.

**Proof.** A short owner has no internal PP body. Its possible interval
support is exactly at its free physical ends. At the head's BP, one neighbor
is its actual TP mate, and the other is the external incoming TP; neither
side is an endpoint-free gap. At any later BP, the other neighbor is the
previous short TP. At every non-tail TP, the other neighbor is the next BP.
Thus the only site which can border a support gap is the last TP. Keeping all
original intervals in its adjacent gap gives precisely its full gap support.
The two ends of the actual matching edge supply no separate body support. □

A short chain reachable by an alpha-rooted directed route necessarily has
such an external entrance: it has no alpha owner internally, and Lemma 1
allows entry only at the head. Chains not reachable from any original alpha
carry no source-to-resource flow. They can be pruned as graph vertices while
preserving ALL original intervals and the original physical freezing data.
This is not physical deletion or a claim about freezing after deletion.

## 5. Exact weighted contraction with full exterior capacities

**Theorem 5.** Delete only unreachable short-chain flow vertices. Replace
each reachable chain of m owners by one capacity-one conduit from its head
BP entrance to its tail TP exit, with toll m-1. Keep all external terminal
links with cost one, the tail's full original support set, all other mixed
gates, individual beta BP entrance capacities, each beta's single private
sink, beta-body supports, and all original unit interval sinks. Then the
maximum integral flow is V_full, and its minimum cost is c_full. Each optimum
lifts to actual distinct original terminal links with exactly that cost.

**Proof.** First use the established full fork normal form. By Lemmas 1 and
4, a reachable short chain is a series of capacity-one mixed gates joined
by exactly m-1 unit-cost internal links, with no external entry, exit, sink
or support before its head/tail interface. Any source-to-sink flow entering
it traverses the entire series at the same amount, either zero or one.
Its actual internal link cost is m-1. Projection onto the conduit therefore
preserves flow value and cost and retains its tail support witness.
Conversely a used conduit expands to every original gate and internal link
in its chain. Different conduits have disjoint internal tips; all external
physical BP entrance capacities remain in force, so this creates no repeated
source or target. The remaining resource capacities are unchanged. Both
maps are inverse on source-to-sink paths. Cyclic components with no payment
can be removed; costs are nonnegative. Thus maximizing value and then
minimizing actual link count agree in both networks. Unreachable vertices
cannot occur on an alpha-rooted paying path, so their earlier removal is
safe. □

This is a standard series-flow reduction applied to a proved physical
configuration. The geometric content is the chain structure and absence of
earlier support. It does not license collapsing a receiving nonshort mixed
gate or treating two chains at the same physical BP as independent. If two
exits meet a single BP, its capacity stays one. If they meet DIFFERENT BPs
of one beta, retain both entrances, its one private beta sink, and its
original body/interval resources: two entrants may jointly use the private
sink and an interval, but do not create two beta resources. Abstract controls
check these distinctions; we do not claim a new fully frozen merger fixture.

## 6. A frozen-board obstruction to zero-toll contraction

Use the saved 14x16 board with 20 selections and 33 actual matching edges:
[fixture and strict ranks](../develop/fixtures/frozen_vertical_mixed_missing_tip.json).
Its feasibility and all 66 endpoint freezing statements were checked from
the inductive definition in [VerticalTipInjection.lean](../formal/SubQuorum/VerticalTipInjection.lean).
The physical board is unchanged in this example. Restrict ONLY the allocation
model: keep the alpha with TP (5,7), all original mixed owners, no beta owners,
and just the original interval at band 5, column 14 (one-based coordinates).
This is an allowed-source/resource control, not the unrestricted target.

The alpha can pay by exactly these three actual terminal links:

    (5,7)  -> (5,8)       into the long mixed strand,
    (10,8) -> (10,9)      into the two-owner short chain,
    (10,10)-> (10,11)     its internal link.

The chain's last TP is (10,12), with a BT cap at (10,13) leading to the
available BB interval at column 14. The restricted owner graph has six
owners, source 0, and precisely the nonself edges

    0 -> 1 -> 4 -> 5,

with only owner 5 supporting the available interval. Owners 2 and 3 are
unreachable. This proves V=1 and c=3: the displayed path is a witness, and
there is no shorter route. Alternatively the potential values 0,1,2,3 at
owners 0,1,4,5 increase by at most one per allowed link, so any paying walk
has length at least three, without a bound on walk length.

The correct contraction retains toll one for the two-owner chain. Dropping
the toll returns value one but reports cost two, while its actual lifted
links still number three. Thus the failed rule is zero-cost short-chain
contraction, not the target compensation inequality. In the complete original
allocation pool this SAME physical board has V_full=2 and c_full=0 through
two distinct old alpha bypass intervals.

For every q>=1, translate q copies by 14 rows, retaining each copy's indicated
alpha/interval and all its mixed owners. Occupied sets and support/link
incidences are separated by blank rows. The old finite rank witnesses replay
independently, so all copies remain frozen. The potential argument gives a
three-link lower bound for each paid source, and the displayed paths are
disjoint. Hence restricted V=q,c=3q, whereas zero-toll contraction reports
2q. The complete pools still have V=2q,c=0. This is an all-q proof; the eight
computed copy sizes only check its coordinates and identities.

## 7. Verification, formal scope and remaining problem

Run from the repository root:

    python3 develop/check_short_mixed_chains.py --output output/short-mixed-chains-validation.json

The permanent [receipt](../output/short-mixed-chains-validation.json) records
213 completely frozen boards, 1,108 short chains/2,108 short owners, 1,000
simultaneous internal links, 644 entered-chain tail-support equalities,
213 exact full value/cost contractions and actual link lifts, and 1,464 mixed
gates removed. There are 1,574 corridor-slot assignments, 150 strict coarse
budget improvements and 121 nonempty-alpha cases where the old positive
budget becomes zero. There are 155 independent primitive-pack comparisons,
32 abstract chain lengths and 96 abstract shared-receiver controls, plus
eight full-pool and eight restricted-pool copy checks.

The sealed single-slot board's coarse budget improves 1->0; the paired
sealed board's improves 2->1, while its fine corridor certificate already
has deficit zero and full V=2,c=2. The 66-endpoint mixed-vertical board has
no remaining holes, improving its coarse budget 1->0. In this sample chain
links ALONE never strictly improve the fine prechain certificate deficit;
their general monotonicity and the stronger hole bound should not be
reported as an observed repair of a positive fine deficit. The remaining
51 positive constructed-certificate deficits are not full-flow deficits.

[ShortMixedChains.lean](../formal/SubQuorum/ShortMixedChains.lean), checked
locally with Lean 4.33.0 and no mathlib dependency, proves internal column
adjacency/disjointness, strict progress exclusion, toll arithmetic, hole-budget
monotonicity, an arbitrary-length owner-walk potential bound, the exact
three-edge paying witness and all-q cost ledger. The checker verifies the
actual restricted owner graph matches this formal graph. See the
[formal receipt](../output/short-mixed-chains-formal-check.json) and
[axiom audit](../output/short-mixed-chains-lean-validation.txt). The complete
physical chain classification, corridor adapter, partial-certificate lift
and full exterior projection/lift are WRITTEN general proofs; they are not
claimed as end-to-end Lean theorems or deductions from enumeration. No new
independent external review is claimed.

The residual geometric problem has narrowed to multiple unported chain
tails/marked exceptions in an alpha-containing original interaction component,
and their joint access through occupied adjacent bands or a nonshort gate.
A positive hole budget does not prove a payment loss. The next proof must
retain actual entrance caps and original shared resource identities, or
exhibit a fully frozen obstruction for the specific proposed stronger rule.
The submitted 11 October manuscript, public main, PR #3 and shared CI are
not modified by this research branch.

## Continuation: a realized active merger

The [active short-tail merger note](ACTIVE_SHORT_TAIL_MERGER_AND_SEALED_ESCAPE.md)
constructs a fully frozen two-source common-BP merger with both short owners
alpha reachable and two distinct downstream intervals. It also proves a
necessary injective retained-escape lemma and realizes an escape in a sealed
pure cycle. The obstruction survives the exact reductions here; complete
original compensation still holds through different old bypass intervals.
