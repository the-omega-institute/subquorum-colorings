# Two-tile elbow repair: exact resource transfer and joint compensation

26 October 2026. Wenlin Zhang and Haobo Ma. Independent research continuation.

We give a local repair for a genuine H/V seam in the canonical band model.
It changes only **two** tile direction bits in a 4-by-2 patch, rather than
requiring a full-height P-free strip. All global M/PP owners, source and
terminal identities, and physical TP-to-BP links remain unchanged.

The repair relocates resources; it does not create numerical slack. Exactly
delta in {1,2} old positive forests disappear and delta new private units
for the target alpha appear. The old units can support at most one old
owner. An exact full-network formula, including beta forks, decides whether
the transfer gives an extra payment or displaces an old payment.

For a noninteracting collection of q patches with distinct targets, let p
be an old maximum that leaves those targets unpaid. Delete the targets
and withdraw ALL lost old units together. If the resulting maximum is
p-r, the new model has exactly

    V_new = p+q-r,       0<=r<=number of distinct old witness owners<=q. (1)

Thus the joint repair never decreases payment, and gains exactly q-r.
The loss r is one joint withdrawal rank; separate marginal losses cannot
be added. If the q targets are all the old residual sources and r=0, this
proves complete compensation and the coefficient-one numerical bound on
the stated geometric class. We do not prove universal patch coverage or
that full freezing alone forces r=0.

For the existing fully frozen H4/V6 obstruction, r=0 is proved for arbitrary
sealed final T, and the complete support profile and optimal selection
frontier are exact. One leaf-tile flip alone merely transfers a seam defect
to the boundary term b. Flipping its adjacent tile completes the repair.
The submitted manuscript, main and existing PR are unchanged.

## 1. Physical hypotheses of a single elbow

Use a feasible (T,M), P=V(M), the full original positive BB/TT forest pool,
whole-owner support, both physical beta BP entries and the single whole-beta
sink, with every actual M edge restored before identifying owners. Work
with the [canonical bands](CANONICAL_BAND_COARSENING_AND_REPAIR.md).

Normalize the patch to rows r,...,r+3 and columns c,c+1, with even r,c.
Assume:

1. Both patch tiles are H. Each of their canonical H bands ends at c+2;
   equivalently, the immediately right-hand tiles are V. The patch is
   inside the board, including column c+2.
2. The tile in column pair {c,c+1} immediately above and immediately below
   the patch, if present, is H. Thus after the two flips the patch is one
   canonical V band of length four, with no axial continuation.
3. Its **only P site** is v=(r+1,c+1), which is a terminal of a global alpha a.
   The two seals (r,c+1),(r+1,c) belong to T.
4. The two outside sites (r+2,c+2),(r+3,c+2) belong to P.

No condition is imposed on P to the left of the patch, on the rest of the
body of a, on other component types, or on occupied neighbouring bands.
Feasibility, not full freezing, is enough for this adapter. Rotation and
reflection give the other sides and terminal positions.

Switch both patch tiles from H to V and canonicalize. T, P and actual M
are fixed. The constraints above are explicit sufficient hypotheses; the
note does not assert that every bent path possesses such an elbow.

## 2. Exact geometric adapter

The first two physical rows of the patch are

    B T
    T P

because the upper seal faces v and forbids its left neighbour. The third
row is BB: its left site is forbidden by the left seal, and its right site
has two P neighbours, v and the outside right guard. The fourth row has
at most one selection, since a TT pair there would make its right selection
see both its selected partner and the outside P guard. It contains no P.
Put

    delta=2-|T intersection {(r+3,c),(r+3,c+1)}| in {1,2}. (2)

**Owner and link invariance.** Neither old nor new auxiliary pairing adds
a PP edge inside the patch, since it has just one P site. Outside the two
tiles auxiliary pairs are unchanged. The N partner of v changes from the
upper selected seal to the left selected seal, so v stays TP. All other
terminal partners are unchanged. Hence the entire global M/PP multigraph,
all owner bodies, alpha/beta/mixed classes and terminal coordinates/types
are identical. This conclusion does not discard actual crossing edges.

Old links in the affected H bands cannot touch a removed patch boundary:
the patch has no P on its leftmost column and none in its lower two rows.
The only patch terminal v has selected/blank local-axis neighbours before
and after the operation, never another P terminal. In the new V band its
neighbours along the axis are the upper seal and the forced blank below.
There are no new links at its axial ends, which meet H tiles. Thus the
**entire physical TP-to-BP link set is identical**. This is stronger than
assuming that just a chosen old routing survives.

**Old positive resources.** The two removed columns of the upper H band
are BT and TP. No BB/TT forest meets them. All positive forests in its
remaining prefix retain their exact cells. Removing the P column can
remove support from a, but it changes support of no other owner.

In the lower H band the two removed columns contain delta BB columns and
the other columns are BT. There is no TT in the removed tail. Every old
positive forest wholly in the remaining prefix stays identical. A forest
meeting the removed tail either disappears or leaves a balanced forest
at the new boundary; it cannot leave a positive forest with a changed cell
set. Indeed, a crossing forest is cut immediately before its final BB,
leaving TT at its right end and capacity zero. Capacity addition, or the
BB-minus-TT identity on the two even-length bands, shows that exactly delta
positive old units are lost. Call their set Q_a.

Both removed columns are in one maximal no-P suffix. It has at most one
P boundary, on the left, so all units of Q_a are supported by at most
**one** old open owner z_a. If that boundary is a closed cycle or does
not exist, the units have no open support. Some forest cells may extend
far to the left of the two flipped tiles; we withdraw the complete original
forest unit, not an invented fractional piece of it.

**New positive resources.** The new V word is BT,TP,BB followed by BT or BB.
It has exactly delta positive singleton forests. They lie below v and are
supported by a alone, because this canonical band contains no other P.
Call them J_a. The band guards in hypothesis2 are necessary for this
privacy assertion; a longer vertical gap might instead have a second owner.

There is a physical-cell identification of every unit outside Q_a with a
new unit outside J_a. For all owners other than a their supports under
that identification are exactly equal. The new private units and the old
lost units **replace** one another:

    |Q_a|=|J_a|=delta,       L_new=L_old.                (3)

We never retain both local pools. The numerical slack is unchanged also
directly from its definition area/2-|T|-|M|.

## 3. Exact payment, costs and source preservation

Write V(F) and C(F) for maximum payment and, at that value, minimum physical
link count in a full fork-capable model F. In the OLD model remove alpha a
as a permitted source, keeping every mixed and beta gate. This is safe:
an alpha has no BP entry and cannot be a transit owner. Denote its value
p_minus. Also withdraw Q_a; denote the resulting model F0 and value p0.
All other original units are available.

The geometric adapter proves

    V_new = 1+p0,        C_new=C(F0),
    r_a=p_minus-p0 in {0,1}.                           (4)

**Exactness.** Pay a directly by one of its new private units. A maximum
pack of F0 embeds with the same physical routes and costs, proving the
lower bound and cost upper bound. Conversely, in any new pack a can be
paid directly by that private unit. Replacing its previous interval path
frees the used gates/resources. If a was one arm of a beta fork, keep the
other arm and end it at the whole-beta sink, freeing the fork interval.
If both arms are removed, free the whole fork. These replacements do not
reduce other payments or increase links. The remaining pack contains no a
and uses no J_a, and is exactly a pack of F0. This proves both equalities.

For r_a<=1, take an old maximum pack without a. Every resource in Q_a has
the same sole possible witness z_a. Owner-disjoint normal form allows at
most one used resource with that witness in a simultaneous pack, regardless
of whether delta is one or two. If that resource is used by an interval
primitive, discard its one source. If it is used by a beta fork, keep one
arm at its beta sink and discard just the other source. At most one
payment and no additional links are lost. This proves the rank bound.

In particular, if an old maximum of value p can leave a unpaid, then

    V_new=p+1-r_a in {p,p+1}.                           (5)

The operation pays a and can keep all but at most one source of ANY such
old maximum pack. Strict gain is equivalent to the explicit joint-pool
condition p0=p. For a prescribed old paid set B, retaining every identity
in B and adding a is possible iff the old F0 can pay all of B. Equal maximum
values alone do not establish that identity-preservation condition.

If a must be paid in every old maximum, (4) still holds; no monotonicity
claim follows just from an attractive local reserve. This is why the
unpaid-source hypothesis is retained in (5).

## 4. Joint elbows and a single withdrawal rank

Take q patches satisfying Section1 with distinct target alphas. Require
their two affected canonical H bands to be pairwise different, their
physical patches disjoint, and their immediately above/below H guard tiles
to remain unflipped. These conditions prevent new V bands from merging
and make the geometric adapters simultaneous. They are stronger than
physical cell-disjointness alone and are checked before using this theorem.

The old lost unit sets Q_a are disjoint because their old H bands differ.
The new units J_a are private to their distinct targets. All non-target
owners, links and remaining positive physical units are unchanged after
ALL flips. Suppose an old maximum p leaves all q targets unpaid. Set

    Q=union_a Q_a,
    p0=V(old model without all q targets, with Q withdrawn),
    r=p-p0.

Pay each target by one of its own new units and repeat the exactness proof
of Section3. It gives (1), including minimum link cost C_new=C(F0). For
the loss bound, group all Q_a by their actual old witness owner z_a, ignoring
witnesses that are themselves omitted target sources. A normal pack can
use at most one interval with each such witness. Removing that primitive,
or one arm of its beta fork, loses at most one old payment per distinct
witness. Thus

    r<=number of distinct non-target witness owners<=q.  (6)

The same owner appearing beside several patches is charged only once,
not once per lost physical forest. This proves joint nondecrease and the
exact gain q-r. Source identities can again be prescribed in the F0 flow.
For any chosen old pack, the number of distinct affected witnesses bounds
the number of its source identities that need to be lost; the scalar
maximum-value formula alone does not identify which sources survive.

**Why individual tests are insufficient.** An explicitly ABSTRACT example
has one old source b supported by old units u1,u2, and two unpaid targets
a1,a2. A local action replaces ui by a private unit for ai. Withdrawing
u1 alone loses no old payment; withdrawing u2 alone also loses none. The
joint withdrawal loses one. After both actions the maximum is2, so the
gain is1, not2. This is a completely specified resource-incidence model,
not a claimed frozen-grid embedding. The general physical theorem uses
the joint r and does not depend on realizing this example geometrically.

**Numerical corollary.** More generally write D_old=alpha-p. Since a full
normal pack pays at most L+beta sources, (1) gives the unified count

    |T|+|M| <= area/2 + D_old-q+r.                       (7a)

The residual term is a single joint loss, not the sum of independently
available local slacks. If the targets are all D_old old unpaid alphas,
and r=0, every alpha is paid after the flips. A normal pack spends at
most one credit per original interval and per whole-beta sink; a fork
pays two sources with one of each. Hence alpha<=L+beta and

    |T|+|M|<=area/2.                                   (7b)

This is a coefficient-one improvement on the explicitly stated elbow/
joint-withdrawal class. It does not assert universal coverage or add beta
credits to an already counted interval payment.

## 5. Constant-size repair of the actual H4/V6 obstruction

Use configuration(W,k), even W>=8, with its unique actual M, four leaf
seals per module, and mixed H4/V6 canonical N from the preceding note.
The actual P and all-size component description are unchanged. For each
module i put c_i=10i. There are two candidate elbow actions:

    upper: rows[0,4), columns[c_i+2,c_i+4),
    lower: rows[W-2,W+2), same columns.                  (8)

The upper patch meets Section1 with r=0,c=c_i+2. Reflecting rows proves
the lower case. Every patch has only its designated column3 P leaf, its
two selected seals, and the required exterior central P guards. The next
unflipped H tile separates the patches, even when W=8. Only four rows of
P-free clearance are used. No full-height P-free strip is required.

Allow ANY feasible final T retaining only the four old leaf seals in each
module. From the existing arbitrary-T mixed-support theorem, the old source
L_i has private support size h_i equal to the losses on the four disjoint
cover tiles at (0,c_i),(W,c_i),(0,c_i+4),(W,c_i+4). All sources have no
terminal exits, and ell=tau-|T|>=sum_i h_i.

The old lower-band suffix units Q_a in each patch have NO P boundary in
their whole old H band, so they have no open support at all. Their removal
cannot hurt any other source, jointly or individually. The upper terminal
band can lose old support of L_i, which is replaced by its new private
guard resource. Other sources' private resources and routes are unchanged.
Therefore for ANY upper/lower action set F, allowing both actions in the
same module but counting its one source once,

    V(F,T)=#{i:h_i>0 or at least one action of F hits i},
    D=k-V,           minimum links=0.                  (9)

Every assertion concerns the complete original pool. If both ends of the
same source are repaired, neither its two guards nor the repeated action
are counted as two source payments. This case is handled directly by (9),
not by the distinct-target hypothesis of Section4.

On the true fixed-P maximum T*, all h_i=0. Flipping just its upper **leaf
tile** changes that terminal's seam condition into a missing local-axis
port: the forced BB row remains in the next H tile. The new V band has
only BT,TP and no interval, so no source is paid. Exactly one seam defect
becomes one boundary defect; d4+b+s stays constant. Flipping the adjacent
tile gives the length-four V band and its private positive guard. Thus
one such two-tile action pays one previously unpaid source. After k upper
actions, every source is paid with no T deletion and only 2k direction-bit
changes, independently of W. This is not a proof that 2k is globally the
minimum over every possible tile-direction scheme.

For integer patch budget j>=0 and deficit limit 0<=d<=k, (9) and the old
disjoint cap cover give the exact fully frozen optimum

    max |T|=tau-max(0,k-d-j).                            (10)

Indeed if q different modules are hit, k-D-q remaining paid modules each
consume at least one distinct cap loss, so ell+D+q>=k and q<=j. For
attainment perform q=min(j,k-d) upper actions in distinct modules, and
delete the upper central outer partner (0,c_i+5) in k-d-q further modules.
Those deletions open private central singletons, giving exactly k-d paid
sources. The common inventory strict-rank freezing schedule tolerates all
these absent upper central partners; directions do not enter that schedule.
Thus all endpoints remain frozen and (10) is attained.

## 6. Verification and unresolved question

Run:

    python3 develop/check_local_elbow_resource_transfer.py --output output/local-elbow-resource-transfer-validation.json
    python3 develop/check_joint_elbow_resource_transfer.py --output output/joint-elbow-resource-transfer-validation.json
    python3 develop/check_local_elbow_resource_transfer_formal.py --lean /path/to/lean-4.33.0 --output output/local-elbow-resource-transfer-formal-validation.json

The permanent checker compares complete original pools, exact positive
forest cell sets, lost/new unit counts and privacy, all global owners and
links, non-target support equality, full fork-flow values and costs against
the residual model, and independent primitive optima. It checks mixed
mosaics, genuinely supported old losses, delta2 cases, every small family
upper/lower action set, arbitrary T rebuilt from seals, sharp frozen quotas
and a permanent serialized fixture. Written proofs establish all-size
claims; finite checks only test the adapters and attainments.

Completed checks passed 233 general local adapters, including 215 mixed
mosaics, 25 delta2 cases and 49 cases with an old lost resource supported
by a different owner. Independent primitive optimization passed 72 adapter
comparisons and 27 family comparisons. The family passed 457 arbitrary-T/
action profiles, all 252 small upper/lower action sets, 72 T rebuilt from
only seals, 18 seam-to-boundary single-tile controls, 132 sharp frozen quota
attainers and 113,704 strict freezing events. Simultaneous checks passed
64 physical joint models, 106 joint targets/lost units and 88 independent
primitive optima. The explicitly abstract nonadditive withdrawal control
passed. No positive local withdrawal loss was found among the checked
general models; this observation is not used in the theorem.

The Lean audit covers exact rank/value arithmetic, one effective payment
per old witness rather than per local unit, the joint compensation and
source-count budget, the nonadditive abstract withdrawal example, and
the family quota/constant-size action consequences. The geometric forest
and support adapter, full pack normalization, joint band separation and
all-size freezing remain written/executable, not end-to-end Lean.
Local Lean4.33.0 passed all 17 declaration audits without warnings, sorry,
native evaluation or new axioms. Preflight measured memory and actual
lean/lake comm basenames and preserved the unrelated Lean4.35 processes.

The next question is whether freezing plus further local geometry forces
the joint r to vanish, or bounds it by other genuinely unused original
resources. No full-pool physical example with r=1 is claimed here, and
computed zero losses do not prove that it is impossible. Universal elbow
coverage, optimized-N obstructions and the universal5/6 improvement remain
open. The exact theorem makes the outstanding condition explicit instead
of presuming a free gain from each newly visible BB reserve.
