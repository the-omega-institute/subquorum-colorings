# Guarded strip switches: exact dual-source repair and shared-seam competition

Joint continuation: [direction/deletion repair and exact quota cuts](JOINT_DIRECTION_AND_ISOLATED_DELETION_REPAIR.md) proves the physical commuting adapter, a four-cut two-budget formula, minimum point loss and a sharp combined budget, with a fully frozen all-isolated-candidate realization.

26 October 2026. Haobo Ma and Wenlin Zhang. Independent research branch.

The [previous obstruction](ISOLATED_COVERAGE_OBSTRUCTION_AND_STRIP_REPAIR.md)
showed that isolated deletions can all have zero gain, while specified narrow
strip direction changes repair its family. We now give a geometric sufficient
condition allowing such switches in an otherwise arbitrary strand network,
and an exact selection theorem. The payment gain is the STANDARD DUAL of the
original SOURCE matroid, rather than a sum of per-strip gains. A new fully
frozen physical family makes this distinction sharp: any one of arbitrarily
many switches repairs its shared deficit, but all switches together still
improve payment by only one. No selections or actual matching edges move.

The matroid and flow theorems used below are standard. The contributions are
the physical switch adapter, exact complement-rank/cost interpretation, and
its completely frozen original-resource realization. No universal 5/6
improvement follows here.

## 1. A sufficient guarded-strip condition

Fix a feasible T, actual matching M with endpoints P, and the established
local-band whole-owner-support network of an even-rectangle partition.
Restore actual matching crossings before determining global owners. Work
with all original BB/TT units and both physical beta BP gates, as in the
[complete fork-flow theorem](WHOLE_SUPPORT_FORK_FLOW_AND_RESOURCE_CUTS.md).
The rest of the board, including bent paths, occupied adjacent bands and
capacity gates, is unrestricted.

A switchable region R is an even-height width-two rectangle. Translate its
coordinates to rows0,...,W+1, columns0,1, where even W>=8. Require:

1. P intersect R is exactly {(1,1),(W,1)}, and these are the two ordinary
   endpoints of the SAME global alpha owner a. Both actual M edges may cross
   R's boundary; neither is discarded.
2. The four alternative auxiliary partners (0,1),(W+1,1),(1,0),(W,0)
   belong to T. Thus both H and V pairing label both ordinary tips TP.
3. For every r=2,...,W-1, the neighboring cell (r,2), just outside R,
   belongs to P. The fixed board contains this neighbor column.
4. Initially R uses horizontal bands; the operation changes only R to
   vertical bands. Declared links touching its tips are the local-band
   links. All other rectangles, their auxiliary pairing and declared links
   stay fixed.

Take finitely many pairwise disjoint such regions with DIFFERENT alpha
owners; write E for these eligible source identities. Every subset F of E
can be switched simultaneously.

**Geometric lemma.** Under these hypotheses all physical owners, source
identities, tip types, actual matching crossings and freezing status remain
unchanged. Outside switched strips, original resources retain their PHYSICAL
band/forest identity, support and links. Inside an unswitched strip no resource
is supported by any owner. Inside a switched strip every supported resource
is private to its own alpha, with at least two distinct genuine singleton
units. In particular no old payment certificate loses a used resource or link.

**Proof.** Neither H nor V auxiliary pairing inside R joins two P points,
so N[P] and hence M union N[P] are identical. Both ordinary tips keep TP by
condition2, and no other tip lies in R. Thus all global owner bodies and types
are identical, including any portion outside R or across actual M cuts.

In the two H bands containing these tips, the only no-P gap is the single
left column. It is BT because (1,0) or (W,0) is selected. Therefore a has
no old support inside R. Every other H band in R contains no P, hence no
owner boundary and no support at all. There is no declared terminal link:
each tip's horizontal axis neighbor inside its band is selected, not P.

In the V band (0,1), the no-P interior gap runs through rows2,...,W-1,
with a at both boundaries. A TT row there is impossible: its right selected
cell would see its selected mate and P at (r,2). Its BB rows are therefore
separate singleton forest units. At row2 the left cell cannot be selected
because (1,0) already sees P at (1,1); the right cell has two P neighbors,
(1,1),(2,2), and also cannot be selected. Thus row2 is BB. The same reasoning
gives BB at row W-1; these rows differ since W>=8. Only a meets this band,
so the units are private. The exterior rows0,W+1 are BT, since a selected
right cell there already sees P and cannot have its left mate selected.
No outgoing link is created: axis neighbors of both tips have no P.

Auxiliary bands in every other rectangle are unchanged. Identify a unit
outside R by its actual band cell sequence and forest interval, not by an
integer band offset, which can shift when R changes its number of bands.
Under that identity every outside unit and its support survives. The same
holds for links. Different regions have disjoint band/resource identities,
and their alphas differ, so the switches compose with no shared private unit.
T and M are unchanged, hence feasibility and freezing are unchanged. QED.

The lemma requires conditions on physical geometry, not a promise that a
chosen optimizer succeeded. It does not assert that arbitrary direction
changes preserve strands, supports, or old payments.

## 2. Exact value and link cost after any allowed switches

Let A be ALL old alpha sources, k=|A|. In the original network define
r(S) as the maximum number of paid sources when only S subset A are enabled,
retaining every mixed gate, both beta BP entry gates, private beta sinks,
and all original resources. Let c(S) be the minimum link count attaining
r(S), with c(empty)=0. Put p=r(A).

**Theorem.** For every eligible F subset E, after switching precisely F,

    V(F)=|F|+r(A minus F),
    D(F)=k-|F|-r(A minus F),
    minimum links at V(F)=c(A minus F).                 (1)

Moreover every chosen old maximum paid SOURCE SET can remain paid at this
new maximum. This promise concerns source identities; its routes/resources
may change and the identity constraint can increase minimum link cost.

**Proof.** By the geometric lemma, strip units previously had no usable
support. After the switch the only effective change is one or more private
zero-link sinks accessible to a in F alone. Since each source supplies at
most one unit, two or more such units are equivalent to just one private sink.
Unsupported old strip resources can be omitted from the network. This is
an equivalence of payment problems, not an addition to numerical slack.

Pay every a in F by a distinct private strip unit, and run an old optimal
pack for A minus F. These owners cannot be transit vertices of that pack:
an alpha has no BP entry. Its old resources are outside switched strips,
and every new private resource is inside its own strip. Thus the union is
valid and attains the first expression in (1), at cost c(A minus F).

Conversely take any switched pack. Remove its paths starting in F. Any
remaining path uses neither their private resources nor an alpha as a transit
owner, so it is an old pack whose sources are in A minus F. Its value is
at most r(A minus F). At most |F| paths were removed, proving the upper bound.
At a maximum all F must be paid: an unpaid a could independently use its
private unit to increase value. Redirect each F path to that private sink;
this removes links and releases old resources, without touching other paths.
The remaining r(A minus F) old paths cost at least c(A minus F), proving the
cost equality. Private-beta normalization retains the remaining source paths
and respects their two separate BP gate capacities.

For old-source retention, let B be any old paid basis of size p. B minus F
is independent in the old source matroid restricted to A minus F; extend it
to a basis of that restriction. Combine this basis with private payments for
F. It includes all B and has the optimal cardinality in (1). QED.

## 3. Dual rank, optimal switch count and weights

The old function r is a source matroid rank. For completeness, remove the
super-source and let d(U) be the capacity of the fixed-network edges leaving
U, with sink outside U. Integral max-flow/min-cut gives

    r(S)=min_U [d(U)+|S minus U|].                       (2)

For minimizers U,V for S,T, directed cut submodularity and the pointwise
source-membership inequality imply

    d(U)+d(V) >= d(U union V)+d(U intersect V),
    |S minus U|+|T minus V|
      >= |(S union T) minus (U union V)|
          +|(S intersect T) minus (U intersect V)|.

Taking the two resulting cuts proves rank submodularity. Monotonicity,
r(empty)=0 and unit increments follow by enabling one capacity-one source
arc. These are the standard finite matroid rank axioms. In particular the
source rank includes bottlenecks at mixed owners, individual beta BP entries
and original shared intervals; a mere source-to-resource reachability graph
cannot replace it.

By (1) the payment GAIN is

    g(F)=V(F)-p=|F|+r(A minus F)-r(A)=r_dual(F).         (3)

It is the standard dual-source rank, restricted to eligible E. This is a
DIFFERENT matroid from the contracted resource-candidate matroid for isolated
point deletions. The geometry establishes which model applies.

Consequently, with R=g(E), at most b allowed switches yield exactly
p+min(b,R) payments. Reaching the best eligible value requires exactly R
switches. Full compensation is possible iff A minus E is independent in
the old source matroid; if possible it needs exactly k-p switches. Equivalently
some original source basis has its entire complement in E. Any chosen old
maximum paid source set can still be retained after a suitable repair.

For nonnegative switch weights, sort eligible sources by weight and accept a
switch precisely when the fully optimized gain increases. Standard matroid
basis exchange gives a minimum-weight R-switch repair. This greedy statement
does not optimize secondary link cost; (1) identifies that cost as the old
complement problem, so weighted ties must be resolved accordingly.

Submodularity also gives a stopping rule: zero individual marginal gains at
a current set imply zero further joint gain. Per-strip gains must not be
summed. T and M do not change, so S is fixed and

    (S+D)_after=(S+D)_before-g(F).                      (4)

This improves a compensation deficit budget on the same physical board.
It is not a new universal numerical bound: (4) applies only to switches
satisfying the geometric hypotheses.

## 4. A fully frozen realization with arbitrary shared-seam components

Fix even W>=8 and q>=1. Stack q copies of `configuration(W,1)` vertically,
with two empty spacer rows between consecutive copies, keeping width12.
Let h=W+2 and offset o_a=a(W+4); total height is q(W+4)-2.
Take a subset O of the q-1 seams as OPEN. In each copy translate its original
T and M. At seam a, after copy a, put the following additional spacer selections:

* Closed seam: (o_a+h,4),(o_a+h+1,4); keep the next copy's top selection
  (o_a+h+2,5).
* Open seam: (o_a+h+1,4),(o_a+h+1,5); DELETE the next copy's top selection
  (o_a+h+2,5).

These define the board once. Subsequent strip switches do not delete points.
The original actual matchings remain unique: P slabs are separated by four
no-P rows, and the earlier leaf order forces each slab independently.
Feasibility holds within each retained copy; spacer selections have one
selected mate and no P neighbor. The deleted top-cap point only removes an
occupied neighbor. Spacer pair neighbors at the two adjacent cap rows are
blank in the same column, so no selected degree exceeds one.

Use vertical full-height rectangles on columns[0,2),[4,10),[10,12).
On columns[2,4), each copy's h-by2 rectangle uses H or V according to whether
its source is switched; each two-row spacer rectangle uses V. This is a
valid disjoint even-rectangle partition. The guarded-strip hypotheses hold
for every copy. Exactly 2q actual matching edges cross strip boundaries.
The unchanged inventory is alpha=q, beta=q, mixed=q(W/2-2).

Each L_a has no outgoing link in either direction. Its only OLD support can
lie in the full-height vertical band(4,5), in a gap between consecutive P
slabs. A closed seam has the four no-P row labels

    BT, BT, BT, BT,

and hence zero resources. An open seam has

    BT, BB, TT, BB.

The last three rows form ONE original BB--TT--BB interval unit J_a,
with interval [o_a+h,o_a+h+2]. It is supported by exactly L_a and L_(a+1).
The exterior top/bottom gaps are BT. No other band meets L_a outside its
narrow strip. Thus the ENTIRE old alpha-accessible pool consists exactly of
one shared original unit per open seam; all other raw units are unreachable
from these sources. Different J_a have disjoint physical forest intervals.

Let C_1,...,C_t be the path components on q source vertices with edges O;
t=q-|O|. Matching source vertices to incident edge resources gives

    r(S)=sum_i min(|S intersect C_i|, |C_i|-1).          (5)

Indeed, an entire component of v vertices has only v-1 units, and every
proper subset can be matched: choose an omitted vertex as root, orient the
path away from it, and assign each included vertex its edge toward that
root. No edge is assigned twice. Components are disjoint. Equations(1),(5)
therefore give the exact physical law

    V(F)=|O| + number of components C_i meeting F,
    D(F)=t - number of components C_i meeting F,
    minimum links=0.                                   (6)

One switch per component is necessary and sufficient; the cheapest full
repair chooses a cheapest eligible source in each component. A component
with no eligible source cannot be fully repaired by this operation.
The flip-gain matroid is a partition matroid with one credit per component.

For ALL q-1 seams open, old V=q-1 and D=1. EVERY single strip flip raises
payment by one, but ANY nonempty collection of flips still raises it by
only ONE. For q=2 both single-switch gains are1 while the joint gain is1,
not2. This is an actual fully frozen whole-pool example of duplicated repair
benefit; it is not just an abstract rank example.

The counts on this board, before any switches, are

    |T|=q(9W/2+5)+2(q-1)-|O|,
    |M|=q(3W/2+5),
    S=|Q|=12q-10+|O|.                                  (7)

Source/beta counts coincide, so the exact ledger gives the last equality.
Switches preserve all counts in (7). Shared seam units are paid at most once;
private switched units are never pooled with old unsupported strip units.

## 5. Uniform complete freezing despite cap deletion

An all-height certificate can use the one-copy configuration with (0,5)
removed as a common seed, even for copies where it is retained. Start from
the original uniform one-copy strict schedule. Postpone exactly

    (r,5) for odd r=1,...,W-1;
    (r,6) and (r,4) for even r=2,...,W;
    (W-1,7),(W,8).

Retain all other events in their old order. Inspection of the old four
event families shows their selected witnesses avoid (0,5), and their endpoint
witness mates are retained earlier events. The removed top-cap witness is
needed first at (1,5); all resulting forward-chain dependencies are among
precisely the postponed events. Now append:

| New event | Two retained nonmate neighbors |
| --- | --- |
| (1,5) | (1,4),(1,6) |
| (r,6), even r=2,...,W | (r-1,6),(r,5) |
| (r+1,5), immediately after each preceding event if r<W | (r,5),(r+1,6) |
| (W-1,7) | (W-1,6),(W,7) |
| (W,8) | (W,7),(W-1,8) |
| (r,4), even r increasing from2 toW | (r-1,4),(r,5) |

In each row of this table, each endpoint neighbor's actual mate has already
frozen: for the alternating middle chain these mates are the preceding
odd-column5 and even-column6 events; in the final column4 chain they are
the preceding even-column4 and already completed column5 events. The first
row uses the retained outer-tip/core events. This is a strict certificate
for every W, not a peeling-size extrapolation. It covers all 3W+10 endpoints.
Translate it to each slab; witnesses never leave that slab. Added spacer
selections cannot invalidate it. Thus every board in Sections4-5 is fully
frozen for arbitrary q and O. The executable checker replays this formula
schedule independently and also compares with the generic freezing routine.

## 6. Validation and remaining scope

Run the physical and abstract verifier, then the scoped standalone Lean audit:

    python3 develop/check_guarded_strip_dual_repair.py --output output/guarded-strip-dual-repair-validation.json
    python3 develop/check_guarded_strip_formal.py --lean /path/to/lean-4.33.0 --output output/guarded-strip-dual-repair-formal-validation.json

The verifier compares private-sink values with old complement-source ranks,
checks dual submodularity, exact switch budgets and weighted greedy against
exhaustive selection, and independently checks primitive packings and protected
old paid bases. Abstract controls retain mixed gates and beta BP entry gates.
Physical controls check the ENTIRE original alpha support, physical identity
transport outside changed strips, freezing ranks, exact raw ledger and all
small seam/flip subsets, plus larger W/q controls. Finite enumeration tests
the written proofs; it is not the reason (1)-(7) hold.

The completed checks passed 64 abstract networks, 480 exact complement-value
and minimum-link profiles, 4480 dual submodular pairs, 408 switch-budget
controls and 128 weighted choices; 180 independent primitive values and 276
independent protected-old-basis comparisons passed. On physical boards,
1508 models, 348660 strict freezing events and 84 independent primitive
value/cost comparisons passed, through W64 and q16. Every small open-seam
and flip subset is checked. These totals are recorded in the JSON receipt.

The smallest shared-seam fixture has W8,q2: a22-by12 board, 83 selections,
34 actual matching edges and68 frozen endpoints, slack15, one shared original
seam unit, old value1 and deficit1. Either one of its two strip flips gives
value2; flipping both still gives value2. The physical selection set is
identical across these direction choices.

Local Lean4.33.0 passed 13 declaration audits, with no warnings, sorry,
native evaluation or new axioms. Preflight measured memory and actual
lean/lake comm basenames and preserved unrelated jobs.

Lean validates the dual-rank submodular algebra under explicit old-rank and
cardinality hypotheses, unit/zero-marginal deductions, complement/full-payment
arithmetic and component representative nonreuse. General geometric extraction,
source-matroid flow equivalence, weighted exchange, the coordinate freezing
schedule and full cost normal form remain written proofs with executable
checks. No end-to-end formal grid theorem is claimed.

Guarded source strips are a sufficient repair class. General bent components
may have no such strip; capacity-two tiles can share a capacity-one owner;
arbitrary switches can change PP paths or destroy old supports. The next
geometric question is how to recognize more allowed switches or prove their
absence creates a usable defect/slack inequality. Universal5/6 remains open.
