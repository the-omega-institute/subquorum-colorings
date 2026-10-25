# Joint direction/deletion repair: an exact two-budget frontier

26 October 2026. Haobo Ma and Wenlin Zhang. Independent research branch.

We combine the [isolated-deletion adapter](ISOLATED_SELECTION_REPAIR_MATROID.md)
and [guarded direction switches](GUARDED_STRIP_SWITCHES_AND_DUAL_REPAIR.md)
in one physical repair model. The two operations can be selected jointly,
with separate limits, preservation of old paid sources, and exact point-loss
and link accounting. The numerical optimization follows from standard
integral flow and resource-matroid theory. The contribution is proving that
the physical operations commute in the required sense, handling deletions
inside changing strips, and realizing the complete tradeoff on actual fully
frozen boards with ALL isolated candidates available.

The result does not establish that arbitrary bent components possess a
suitable guarded strip, nor a universal improvement of the numerical 5/6 bound.

## 1. Fixed geometry and joint physical adapter

Fix a feasible T, actual matching M and P=V(M), on an even board partitioned
into disjoint even rectangles with local horizontal/vertical bands. Restore
all actual M crossings before identifying global owners. Use complete BB/TT
forest units, whole-owner support, mixed capacity-one gates, both physical
beta BP gates and the unique whole-beta sink.

Take pairwise disjoint guarded regions R_a for DISTINCT alpha sources a,
exactly as in the guarded-strip theorem: height W_a+2, width2, even W_a>=8;
local P is only (1,1),(W_a,1), the ordinary tips of a; four H/V partners
(0,1),(W_a+1,1),(1,0),(W_a,0) are selected; the exterior neighbor (r,2)
is in P for every interior row2..W_a-1; links touching the tips are the
local-band links. Each region initially uses H and may change to V.
Let H be the set of these switch actions. T and actual M do not change
when switching. Let X be ANY subset of the selections isolated in T union P.
Let C be the deletion actions for candidates OUTSIDE the union of guarded
regions. Distinguish operation identities from original interval identities.

**Joint adapter lemma.** For any F subset H and Y subset X, deletion and
switching preserve P, all global owner bodies, terminal types, actual crossing
edges and the old freezing witnesses. Every old unit OUTSIDE guarded strips
retains its physical band/forest identity and support. Each deleted outside
candidate x adds a distinct original singleton j_x with a support independent
of F. A switched strip gives its source at least two private singleton units,
of which at most one is needed. No old used resource or link is lost.
Deletions INSIDE guarded regions are dominated: removing them from Y changes
neither maximum payment nor its minimum link cost, for every fixed F, while
retaining more selections. They may be modeled as loop actions if all X
are retained in an action list.

**Proof.** Isolation is a property of the occupied physical graph and is
independent of auxiliary directions. Every candidate has no P neighbor.
The four selected H/V partners in each guarded strip DO have P neighbors,
so none is a candidate and the guards survive all Y. The exterior P column
is fixed. Thus the guarded switch lemma remains applicable after every Y.
Conversely every candidate remains occupied-isolated after changing bands
or deleting any other candidates. All endpoint neighborhoods and freezing
witnesses are identical, so every owner body, type and declared link survives.

For an outside candidate, its auxiliary band is never changed by a switch.
The isolated-deletion lemma therefore adds precisely j_x: BT becomes BB;
neighboring TT is forbidden by the candidate's occupied-degree condition;
no old forest component merges or splits. Gap P boundaries and actual
owners do not change, so its support is independent of F. Distinct deleted
points give distinct singletons, all outside the switched strips. Identify
outside bands by their actual cell sequences, since numerical band offsets
can shift when another rectangle changes direction.

Before a guarded strip is switched, none of its internal units has owner
support. Afterwards all supported internal units belong to its one alpha,
which already has two forced BB reserves at original rows2 and W_a-1.
Neither reserve can be destroyed by deleting selections: their cells are
already blank, and all interior TT remain forbidden. Thus additional
inside deletions create only unsupported units, or additional redundant
private units for that same source. An alpha supplies one path and cannot
be a transit owner, so such units change neither value nor minimum links.
Deleting inside points affects no outside band, endpoint type or link.
Omitting those deletions proves the domination assertion. QED.

**One fixed proxy network.** Omit old strip units, which had no support.
Keep all old usable resources Q0 and the entire terminal network. Add one
candidate sink h_a accessible only to a for each switch; it represents the
actual forced upper singleton AFTER that switch, not an additional physical
slack unit. Add the distinct j_x sinks for outside deletions, with their
fixed whole-owner supports. Different action sinks are distinct: switches
represent inside-strip units, deletions create outside-strip units. Retain all usable
original boundary resources and all private beta sinks; unsupported old
strip nodes may be omitted without changing the physical optimum.

This fixed network has exactly the same payment values and minimum link
costs as every chosen physical combination. Packs map both ways: outside
units retain identity, a private switch sink uses the chosen true guard unit,
and unused actions need not be performed. Multiple private strip units can
be replaced by that one guard unit since only their one source can use them.
We NEVER add the old and new raw strip pools together. Only deletions increase
numerical slack, by one per actual deleted selection.

## 2. One normalized rank and four exact quota cuts

Let A be all k alpha sources. For an action set Z subset H union C, let
V(Z) be the full-network payment with precisely these candidate sinks enabled,
and put

    p=V(empty),  g(Z)=V(Z)-p,
    R_H=g(H),   R_C=g(C),   R=g(H union C).               (1)

The fixed proxy network makes g the standard contracted resource-matroid
rank. In particular it is normalized, integer, monotone, submodular, and
has unit increments. All beta private sinks remain in the baseline p.
The H restriction equals the preceding dual-source rank, while the C
restriction is the isolated-candidate resource rank. They are now restrictions
of ONE rank, not two numbers to be added independently.

Let s,d be nonnegative integer limits on switches and deletions.

**Exact joint quota theorem.** The maximum payment is

    V_max(s,d)=p+G(s,d),
    G(s,d)=min{ R, s+d, s+R_C, d+R_H }.                  (2)

For every chosen old maximum paid source set of size p, there is an optimum
with all those source identities retained. Routes and used resources may
change; the formula is not a promise of identity-preserving routing.

**Proof of (2), without bounded enumeration.** Enable all action nodes in
one flow network. Send each H action's unit-capacity terminal edge to a
collector u_H, and each C action to a collector u_C. The two collectors
have capacity s,d to the sink. Original Q0 and private beta edges still go
directly to the sink. An integral flow uses at most s switch actions and d
deletion actions, so its used sinks prescribe a physical feasible action set.
Conversely every allowed physical pack embeds in this quota flow.

A minimum source/sink cut has just four possible collector positions:

| Collectors on the source side | Minimum cut capacity |
| --- | --- |
| neither | V(H union C)=p+R |
| only u_H | s+V(C)=p+s+R_C |
| only u_C | d+V(H)=p+d+R_H |
| both | s+d+V(empty)=p+s+d |

To justify each entry exactly, when a collector is on the source side,
move all its candidate resource nodes there as well. This cannot increase
a cut: those nodes have only support arcs incoming and their terminal arc
to that collector outgoing. Their support arcs then contribute no forward
cut cost, so this entire action class is omitted from the remaining cut.
Its collector-to-sink quota is charged once. A collector on the sink side
instead gives the ordinary unit sink arcs for that class. The residual cut
is exactly the stated fixed-pool problem, whose minimum is the listed V.
Every such cut can also be constructed from its fixed-pool minimizer.
Taking the minimum of the four entries and integral max-flow proves (2).
No gate or original resource is independently credited to two components.

For source preservation, start with a chosen old maximum flow before adding
actions. It is feasible in the quota network. Augment by simple residual
source-to-sink paths. Such paths never revisit the super-source and hence
never reverse an already saturated source arc. Thus all p old source arcs
stay saturated up to a new maximum. Beta normalization preserves starting
sources. QED.

## 3. Minimum point loss, joint budgets and an algorithmic caution

For any target additional payment t, with at most s switches, some repair
exists iff

    t<=R and t<=s+R_C.                                 (3)

When feasible, its minimum deletion count is exactly

    d_min(t;s)=max{0, t-s, t-R_H}.                       (4)

Indeed, (2) reaches t iff all four entries are at least t. The two remaining
conditions on d give (4). Its value never exceeds |C|: submodularity gives
R<=R_H+R_C, and (3) bounds both positive lower terms by R_C. For full payment
t=k-p, (3) is an explicit feasibility condition; freezing alone does not
supply it.

A more precise optimal-count statement follows. Put h=min(s,R_H) and let
G=G(s,d). Then an optimum with FEWEST deletions and, next, FEWEST switches
uses exactly

    h switches and G-h deletions.                      (5)

Since G>=h, equation(4) at t=G gives G-h deletions. Unit increments force
at least h further actions; apply (2) with budgets h,G-h to obtain an
optimum with exactly that many switches. Thus its G actions are independent
in the joint rank. Minimum counts preserve any chosen old paid source set:
for any enabled action set attaining the target value, old-source retention
is possible without enabling more actions.

Let S0,D0=k-p be the old numerical slack and deficit. For arbitrary F,C'
actually performed, omitting dominated inside deletions,

    S_new+D_new=S0+D0+|C'|-g(F union C').                (6)

All S+D bookkeeping charges deletions, never proxy switch sinks. The rank
bound g(F union C')<=R_H+|C'| and the unit bound give

    S_new+D_new >= S0+D0-min(s,R_H)                     (7)

under a switch limit s. The maximum payment in (2) can attain equality:
use the counts in (5). Therefore isolated deletions may complete missing
payments, but cannot improve this combined budget beyond the independent
zero-point-loss switch rank. With unrestricted switches, reaching the full
candidate value needs exactly R-R_H deletions and can lower S+D by exactly
R_H. These are exact statements for the allowed operation class, not a
universal numerical grid bound.

**Do not greedily optimize the two classes separately under quotas.** An
explicit ABSTRACT two-source example has no old payment. Switch h_1 pays
source1 privately, switch h_2 source2 privately, and deletion c privately
pays source1. If h_1 is cheaper than h_2 and s=d=1, selecting the cheapest
switch first leaves c redundant and pays only1; joint choice {h_2,c} pays2.
All three individual gains are1. This is a completely specified flow/rank
example, not a claimed physical-grid counterexample. The quota theorem
handles it; unconstrained weighted matroid greedy does not enforce these
separate class limits.

One integral lexicographic min-cost max-flow solves the full selection:
first maximize payment; then retain all prescribed old paid sources; then
minimize deletion count, switch count, action weight and finally links.
Put those additive costs on source arcs, candidate terminal arcs and actual
link arcs; the two collectors enforce quotas. Only USED actions are physically
performed. If beta normalization could release a positive-cost candidate
sink, it would improve the chosen cost vector, contradicting optimality.
Otherwise normalization changes no action costs or source identities.
The same argument preserves both physical BP entry capacities and ensures
that each original or private resource pays at most once.

## 4. Actual fully frozen family and ALL-candidate frontier

Fix even W>=8, q>=1. Stack q copies of `configuration(W,1)`, with FOUR spacer
rows between consecutive copies, retaining width12. Let h=W+2,
o_a=a(W+6); total height is q(W+6)-4. Keep every translated original T and M.
At seam a add exactly these five selections:

    (o_a+h,4),
    (o_a+h+1,5), (o_a+h+1,6),
    (o_a+h+2,4), (o_a+h+3,4).                           (8)

The first is an occupied-isolated candidate x_a. The next two form a
horizontal selected pair; the last two a vertical selected pair. None
faces P. Adjacent copy-cap cells in their columns are blank, so the original
copy selections and all five new ones remain feasible. In particular the
extra selection at column6 pairs off the otherwise isolated column5 point;
there is precisely ONE isolated point in the L-accessible seam gap.

All actual P and M slabs are separated. The original leaf forcing order
therefore still proves uniqueness of M. Every original copy's unchanged
strict freezing schedule translates internally, and adding spacer selections
cannot destroy it. Thus the entire board is completely frozen for all W,q.

Use full-height V rectangles on columns[0,2),[4,10),[10,12). On [2,4), give
each copy its own H/V guarded strip, and each four-row spacer its own V
rectangle. Exactly 2q actual M edges cross region boundaries. Every choice
of flips keeps alpha=q,beta=q,mixed=q(W/2-2). Each alpha L_a has no outgoing
link; only its own supported resources can pay it.

In vertical band(4,5) the six no-P seam rows have labels

    BT, BT, BT, BT, BT, BT.

Only x_a, in the first spacer row, is occupied-isolated in these two columns:
cap selections face P and the other three gap selections belong to their
horizontal/vertical pairs. Deleting x_a changes precisely that one BT row
to BB, giving a genuine SINGLETON original unit shared by L_a,L_(a+1).
No other isolated deletion opens a resource supported by an unflipped L.
Exterior caps are BT. Within a flipped guarded strip any additional isolated
deletion creates only redundant private resources, as in the joint lemma.
Consequently this classification includes ALL occupied-isolated candidates,
not an artificial restriction of an otherwise usable repair pool.

For any deletion set Y subset X (all isolated selections), let O(Y) be the
seams whose x_a were deleted. Let C_i be the path components on q vertices
with these seam edges. For ANY flip set F,

    V(F,Y)=|O(Y)|+number of C_i meeting F,
    D(F,Y)=q-V(F,Y),  minimum links=0.                   (9)

The proof is the whole-pool matching argument: each unhit tree component
of v sources has v-1 distinct edge resources and leaves one source unpaid;
a hit component has a private switched unit and pays all v. Orient the tree
toward one private source and assign each other source its parent edge.
Neither a shared edge nor a private reserve is used twice. Root closures
have no outgoing links, so other raw resources or beta forks cannot help.

The initial p is0. For the FULL candidate sets,

    R_H=q,    R_C=q-1,    R=q.

Thus the exact physical budget frontier is

    V_max(s,d)=min{q, s+d, s+q-1}.                       (10)

Even deleting ALL isolated selections without a switch leaves one unpaid.
A single switch plus q-1 effective seam deletions pays all; q switches pay
all without any point loss. If s>=1, the minimum deletion count for full
payment is max(0,q-s). With s=0 full payment is impossible in this operation
class, however many isolated candidates are deleted. This is consistent
with the guarded-switch theorem and refines its resource-count tradeoff.

The exact physical counts are

    |T|=q(9W/2+5)+5(q-1),   |M|=q(3W/2+5),
    |X|=q(7W/2-14)-1,
    S0=|Q0_physical|=21q-19,    S_Y=21q-19+|Y|.         (11)

For |X|, each copy contributes 7W/2-15 isolated selections, no such vertex
gets a spacer neighbor, and each of q-1 spacers contributes only x_a.
The other four spacer selections are paired, not isolated. Area and the
first two counts give the slack. Alpha and beta counts coincide, giving
the resource count by the exact ledger. Switches change resource decomposition
without changing that count; deletions alone add one physical unit each.

The permanent W8,q2 fixture has shape24-by12, originally87 selections,
34 actual matching edges,68 fully frozen endpoints and slack23. There are27
isolated candidates but only one effective seam deletion. Deleting all27
alone pays1 of2; one switch plus just the effective deletion pays2, leaving
86 selections and slack24; two switches pay2 with all87 selections retained.
All variants use the full original resource pool.

## 5. Validation, formal scope and remaining geometry

Run:

    python3 develop/check_joint_direction_deletion_repair.py --output output/joint-direction-deletion-repair-validation.json
    python3 develop/check_joint_repair_formal.py --lean /path/to/lean-4.33.0 --output output/joint-direction-deletion-repair-formal-validation.json

The verifier checks all quota pairs, every target/deletion threshold, the
combined-budget minimum and lexicographic action/weight/link optima against
independent primitive packings. It retains mixed gates, individual beta BP
entries and old-source protection. Physical checks cover complete small
flip/seam-deletion sets, dominated inside candidates, ALL other isolated
candidates, and larger all-X controls. Physical band/forest identity is
checked outside changed strips, with no use of shifting integer offsets
as identity. All formula freezing witnesses are checked independently of
the generic freezing routine. Enumeration corroborates the general proofs.

Completed checks passed 45 abstract action networks, 308 exact quota and
optimal-action-count profiles, 149 independent full lexicographic optima,
223 target/minimum-deletion profiles and 45 exact combined-budget optima.
The explicit cheapest-first failure and shared-versus-distinct beta BP entry
controls passed. Physical checks passed 930 configurations, 180408 strict
freezing events and 50 independent primitive value/cost comparisons, through
W64 and q16. The actual grid units were also compiled into the joint quota
solver: all 108 such profiles matched the complete-candidate physical
frontier, checked independently at 108 entries. These controls include full-X
deletions and dominated inside-strip candidates.

Local Lean4.33.0 passed 15 declaration audits with no warnings, sorry,
native evaluation or new axioms. Preflight measured memory and actual
lean/lake comm basenames and preserved unrelated jobs.

The Lean audit proves scalar consequences of the four-cut minimum under
explicit rank hypotheses: exact target feasibility/minimum deletion,
optimal action counts, no repeated budget benefit, combined-budget equality,
and the path-family frontier and counts. The four-cut network adapter,
commuting geometry, all-height source support/freezing classification and
lexicographic flow normalization remain written proofs and executable checks.
No end-to-end formal grid result is claimed.

The remaining obstacle is geometric: a general residual bent or capacity-two
configuration need not possess these guarded strips or isolated outside
candidates. The exact residual deficit after exhausting this repair class
is k-p-R. It must be charged by further physical structure, rather than
assuming automatic candidate coverage or adding separate marginal gains.
The submitted manuscript, main branch and shared CI remain outside this
research update; the universal5/6 question stays open.
