# Two-sided seam budgets, exact full-pool compensation and unbounded recourse

25 October 2026. Wenlin Zhang and Haobo Ma. Independent research branch.

The [one-sided path circuit](EXTREMAL_SHARED_UNIT_BUDGET_AND_FULL_POOL_PATH_CIRCUITS.md)
can be repaired by opening one additional upper shared unit. We prove that
this fixes an arbitrarily long path, but can force an arbitrarily large
number of old source assignments to change. We first solve every combination
of upper and lower seam openings on this physical family, including the exact
selection loss, maximum payment and minimum links. The general statements
have written proofs; finite checks and scoped Lean proofs corroborate them.

## 1. Fixed endpoints and simultaneous two-sided opening budget

Use P, its unique matching M, and the fully frozen maximum T* from
configuration(W,k), for even W>=8 and k>=1. Its shape is (W+2) by (10k+2),
and the true fixed-P maximum over every feasible selected set is

    t=(7k+2)W/2+3k+2.

A selected set U is feasible if U avoids P and every selected point has at
most one grid neighbor in U union P. At internal seam i=1,...,k-1 define

    upper right column: {(0,10i+1),(1,10i+1)};
    lower right column: {(W,10i+1),(W+1,10i+1)}.

An upper or lower seam is open when its corresponding right column is empty.
Let E+ and E- be prescribed upper and lower opening sets, respectively, and
m=|E+|+|E-|. The sets can overlap: two openings at the same seam have two
separate physical identities.

**Theorem 1.** The exact largest feasible selected set satisfying all these
openings has size t-m. A fully frozen attainer is

    T(E+,E-)=T* minus {(0,10i+1):i in E+}
                   minus {(W+1,10i+1):i in E-}.             (1)

For arbitrary feasible U, without retaining old selections,

    |U| + number of its open designated upper/lower seams <= t. (2)

**Proof.** Use the SAME disjoint cover in the preceding maximum theorem:
aligned 2-by-2 tiles, with the 2k designated 4-by-2 patch replacements.
Its total capacity is t. The upper seam tile is

    G_i^+={0,1} times {10i,10i+1},

and its lower counterpart is G_i^-={W,W+1} times {10i,10i+1}.
Each has old cap two. When open, only its two column10i cells can be
selected. The cell in row1 or W faces a fixed P neighbor in column10i-1,
so selecting both gives that selected cell two occupied neighbors. Its cap
is therefore at most one. All 2(k-1) seam tiles are pairwise disjoint and
avoid all replaced patches. Subtract one for every open tile in this one
cover to prove (2). No tile or loss is counted twice.

The removed cells in (1) are selected in T*, isolated from every other
selected cell and from P, with their other row partner already blank. Their
removal preserves feasibility and EVERY endpoint neighborhood. Hence the
old uniform freezing schedule replays exactly. The resulting selection
opens exactly E+,E- and has size t-m, proving sharpness. The neighboring
columns10i,10i+2 cannot be TT under any feasible U: the row1/W cells face
fixed P neighbors. Each designated open BB column is thus an isolated
original BB/TT-forest unit, not a column hidden in a balanced chain. QED.

## 2. Exact full original-pool support graph

From now on use the explicit attainer (1) and horizontal bands. All original
units remain available, including boundary units and unreachable units.
The upper and lower open units are

    j_i^+=(0,10i+1,10i+1),
    j_i^-=(W/2,10i+1,10i+1).

There are k alpha sources A_a (a=0,...,k-1), no betas and 7k mixed owners.
The original pool has 3k+m units and numerical slack S=2k+m.

**Complete-route classification.** The closure of A_a has exactly seven
owners A_a,U0_a,U1_a,U2_a,L0_a,L1_a,L2_a, with transitions

    A_a -> U0_a,U1_a,L0_a,L1_a;
    U1_a -> U2_a;   L1_a -> L2_a.

U0_a supports j_a^+ if open, U2_a supports j_(a+1)^+ if open; L0_a and
L2_a have precisely the analogous lower supports. Every other reachable
support is empty. All remaining 3k original units are unreachable.

To check the geometry, upper mixed tips in module a are respectively
(1,10a+3),(1,10a+4); (1,10a+6),(1,10a+7); and
(1,10a+8),(1,10a+9), with TP/BP types as in the one-sided note.
The lower mixed tips have row W and the same columns. Their exterior gaps
have three selected cells before opening and two after the isolated corner
selection is deleted. Thus precisely the central BB singleton is added.
The middle body of A_a has P immediately to either side and contributes no
support. Deleting points nonadjacent to P changes neither terminal labels,
actual/auxiliary strand bodies nor declared terminal links. The old closed
seven-owner table therefore persists with exactly these four possible
support additions. There is no exit to another owner or beta. This covers
routes of arbitrary length, including every resource in the full pool.

Consequently a payment assigns a source vertex a to one incident open
resource edge: j_a^side on its left or j_(a+1)^side on its right. Each
resource can be assigned once. A left resource costs at least ONE link;
a right resource costs at least TWO. These bounds are attained by

    left:  (r,10a+5) -> (r,10a+4);
    right: (r,10a+5) -> (r,10a+6),
           (r,10a+7) -> (r,10a+8),

where r=1 for upper and r=W for lower. The closure proves these lower
bounds, because only U0/L0 support left resources and only U2/L2 support
right resources. Different source modules have disjoint owners and terminal
links. Thus every injective incident assignment lifts to physical routes
with the stated costs. This establishes both directions of the reduction;
it does not merely infer physical feasibility from a resource count.

## 3. Rank, deficit and minimum links for every opening pattern

Make a multigraph with vertices0,...,k-1. At seam i insert an upper edge if
i in E+ and a lower edge if i in E-. A seam has zero, one or two edges.
A connected component is an interval [L,R]. Call it cyclic if at least one
of its seams has two edges. A singleton vertex with no edges is noncyclic.
Let c be the component count, h the cyclic component count and d the number
of doubled seams. In a cyclic component let p be its FIRST doubled seam,
so L<p<=R. Put

    distance_sum = sum over cyclic components of (p-L).

**Theorem 2.** In the complete physical original pool,

    maximum payment V=k-c+h;
    deficit D=c-h;
    minimum links at maximum value C=V+distance_sum;
    S+D=3k+d-h.                                           (3)

In particular, resources beyond the first doubled seam in a cyclic
component do not increase its payment rank. One cannot count every extra
open unit as an independent compensation gain.

**Proof of rank.** A noncyclic component with r vertices has exactly r-1
resources, so at most r-1 sources can pay. Omit its leftmost source and
assign every other source its left incident unit; this attains r-1 at r-1
links. A cyclic component has a first double p. Assign every source a<p
its right edge a+1, and every source a>=p its left edge a. The only repeated
seam is p, used by sources p-1 and p; assign its UPPER unit to p-1 and its
LOWER unit to p. Every other edge may use either available side. All
resources are distinct, and all r vertices pay. A larger value is impossible
because there are only r sources. Components have disjoint owner and unit
identities, so their values add.

**Proof of minimum cost.** A noncyclic component's r-1 payments each need at
least one link, and the preceding witness attains it. In a cyclic component
all sources must pay at maximum value. Source L cannot use nonexistent edge
L, so must use edge L+1. Inductively, for a<p, if source a used its left
edge a, the preceding source a-1 would already use that same edge. All
seams strictly before p have only one unit, so that would be a collision.
Therefore every source L,...,p-1 MUST use its right edge, each needing at
least two links. Every other source needs at least one. This gives at least
r+(p-L), attained by the explicit assignment above. No assumption about
routes elsewhere can circumvent the all-route closure. Summing proves C.

Finally m=k-c+d, S=2k+m and D=c-h, giving S+D=3k+d-h. QED.

## 4. A one-unit physical repair with unbounded optimal recourse

Start with all LOWER seams open and no upper seam. Its full original pool
has maximum payment k-1 and minimum links k-1. The unique minimum-link
original-unit allocation is

    A_a -> j_a^- for a=1,...,k-1; A_0 is unpaid.            (4)

Indeed every payment needs at least one link, and a one-link route can only
use its left resource. A_0 has no such resource. To pay k-1 sources at
k-1 links therefore requires exactly (4).

Now choose p in {1,...,k-1} and delete the ONE selected cell(0,10p+1).
The endpoints, matching, all terminal labels and declared links, and complete
freezing persist; exactly one original unit j_p^+ is added.

**Theorem 3.** This single-resource repair gives

    V_old=k-1, C_old=k-1;
    V_new=k,   C_new=k+p;
    C_new-C_old=p+1.                                     (5)

Every full-payment allocation changes the original unit assigned to at least
p-1 previously paid sources. This is sharp, including among minimum-link
full-payment solutions. The minimum old assignment recourse is thus p-1.

**Proof.** The new connected multigraph has its first and only double at p,
so Theorem2 proves (5). Its forcing proof says that every source a<p uses
right edge a+1. For each old paid source a=1,...,p-1 this differs from its
old left unit j_a^-. Thus at least p-1 old source-to-unit assignments change,
even if the new solution is allowed arbitrary extra links.

Attain the bound by keeping (4) for every a>=p; assign A_(p-1) to the NEW
upper j_p^+; and assign A_a to lower j_(a+1)^- for a=0,...,p-2. These are
distinct resources, all sources pay, and exactly the p-1 specified old
assignments change. Left sources use two links each and right sources one,
so this witness also attains the minimum k+p. QED.

Taking p=k-1 makes one isolated selection deletion and one new original
resource force k-2 old assignment changes and k extra links over the old
optimum. Hence no constant bound on old assignment recourse, or on the
increase of minimum links, follows just from a one-unit payment improvement.
The count is source-to-ORIGINAL-unit changes relative to the specified old
minimum-link optimum, not a claim about every possible edit metric.
Source identities can all be retained, as promised by the earlier
reoptimization lemma; a uniform bound on how many old assignments must
change is a stronger assertion that fails in this physical full-pool family.
Repair location matters: choosing p=1 instead gives full payment with no
old unit reassignment and exactly two more links. The unbounded conclusion
concerns a prescribed repair position; it does not say that every possible
one-cell repair of this board is expensive.

## 5. Interpretation, validation and scope

The simultaneous opening budget is exact over arbitrary feasible U with P
fixed. The rank and cost formulas concern the explicit frozen attainers
T(E+,E-). The support reduction is an incident-resource matching on a path
multigraph, a standard combinatorial model; the result here is its exact
physical realization, sharp all-U selection budget and geometric link costs.

One extra resource may repair an arbitrarily large component, while further
resources in that same component may have no additional payment value.
Thus extremal loss is additive in disjoint physical opening tiles, while
compensation rank and reassignment costs are global. They cannot be charged
by simply adding one local payment per opened unit.

This fixed-P family still admits full zero-link compensation with VERTICAL
bands for every feasible T, by the earlier guarded-reserve theorem. The
unbounded recourse result concerns the specified horizontal decomposition.
No claim is made that every alternative partition has this cost, or that
these results improve the universal5/6 bound. The manuscript is unchanged.

Reproduce the finite validation with

    python3 develop/check_two_sided_seam_recourse.py \
      --output output/two-sided-seam-recourse-validation.json

The [verifier](../develop/check_two_sided_seam_recourse.py) checks feasibility,
strict freezing, all original unit identities and seven-owner closures,
independent primitive packings on small boards, exact flow values/costs and
explicit disjoint routes attaining the formulas. The
[Lean source](../formal/SubQuorum/TwoSidedSeamRecourse.lean) verifies the
unbounded first-double forcing and injective repair allocation, changed-old-
assignment implication, and count/cost arithmetic. Physical coordinate
extraction, all-parameter freezing and finite-cardinality summation remain
written proofs plus independently checked adapters, not an end-to-end Lean
grid theorem.

The [computational receipt](../output/two-sided-seam-recourse-validation.json)
records 730 frozen physical boards, 166,266 strict freezing events, 3,618
complete seven-owner closures, 232 disjoint top/bottom seam-tile certificates
and 85 independent primitive packing profiles. It includes all four opening
states at every seam for k<=5 at W=8,10, plus larger-height and k=16 controls.
There are 44 single-repair cost/recourse controls; 36 of them enumerate all
full incident allocations, independently checking the least old-assignment
recourse on the smaller boards.
The [formal receipt](../output/two-sided-seam-recourse-formal-validation.json)
and [Lean log](../output/two-sided-seam-recourse-lean-validation.txt) record
15 declaration audits on local Lean 4.33.0, without warnings, placeholders,
native evaluation or new axioms. The exact excluded formal scope is recorded
in the receipt.
