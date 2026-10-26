# Private prefix/suffix reserves: exact polynomial bridge compensation

26 October 2026. Wenlin Zhang and Haobo Ma. Independent research continuation.

The [single-bridge theorem](SINGLE_BRIDGE_COMPENSATION.md) shows why unused
resources in a receiving component alone do not repair an incoming deficient
path: both sources can still need the same capacity-one mixed entrance. Here
we give a geometric sufficient condition that avoids that obstruction. Two
different original units, private to the receiving request, must be available
on opposite sides of the entrance. A fully blank capacity-two tile in a suitable
internal gap supplies exactly this certificate.

For bridges on disjoint pairs of reference stems, this condition replaces the
previous 2^k routing-mode search by a polynomial construction. Its exact gain
is the number of **distinct deficient donor trees**, rather than the number
of bridges. It minimizes actual new-bridge fees and retains every paid source
and used original interval of any maximum reference request allocation and
its standard lift. These are results for the stated class; universal 5/6
improvement and arbitrary shared-stem bridge networks remain open.

## 1. Fixed resource pool and reference requests

Fix an actual whole-owner compensation model, including original alpha,
mixed and beta bodies, actual TP-to-BP links, private whole-beta outputs and
original interval pool Q. Each unit has at most two owner users. Unsupported
units remain in Q. This can be the final state after arbitrary destructive
mixed-direction P-free changes; support monotonicity is not needed.

Take an owner-disjoint reference normalized packing P0 with p source labels
and old links E0, and g additional eligible alpha sources N outside its owner
set. Append each source a in N as a singleton routing skeleton (a), with no
old link. This declares a request; it does not assert that a has an old
payment. In particular, a singleton with empty support is permitted to donate
a new bridge.

As in [old-link repair](OLD_LINK_BATCH_REPAIR.md), make one request for each
ordinary interval stem, one for each beta fork, and one for each appended
singleton. A beta singleton has no request; every beta singleton/fork supplies
one baseline whole-beta payment. Let D be the number of requests and B the
baseline, so B+D=p+g. Request C sees precisely the union J(C) of final supports
of its owners. Each original unit has at most two distinct request users.

The request resource graph has a vertex per request, a full edge for a unit
with two users, and a private half-edge for a unit with one user. A deficient
component is a tree with no private resource, including an isolated vertex
with no resource. If there are t0 such components, maximum request allocation
has D-t0 assignments and old-link payment is

    V0 = B+D-t0 = p+g-t0.

Fix **any** maximum old request allocation M0 in this final pool. Its standard
lift truncates a matched ordinary stem to an owner supporting its assigned
unit; an unmatched stem is omitted. A fork keeps its baseline and, when matched,
uses its assigned unit either at beta or on one truncated arm while the other
arm goes to beta. Fix those baseline arm choices as part of the lift. In this
note “old paid sources” and “old used units” refer to this lifted M0. This is
not a retention assertion about resources that disappeared in an earlier state,
or every alternative physical maximum using two interval arms instead of the
standard whole-beta normalization. Individual assignments and old selected
links may change.

## 2. Hypotheses and exact theorem

A candidate bridge e is an actual new TP-to-BP link from an owner of one
ordinary reference stem A to a **mixed** owner b_j of another ordinary
reference stem C=(b_0,...,b_s), j>=1. A may be an appended singleton. Neither
stem contains beta. Different candidate bridges use pairwise disjoint pairs
of reference stems: no stem is an endpoint of two candidates. Other beta
singleton/fork primitives remain allowed and unchanged as skeletons.

Write C^-=(b_0,...,b_(j-1)) for the strict receiver prefix and
C^+=(b_j,...,b_s) for its suffix. Require for every candidate:

1. A's request lies in a deficient component of the reference request graph.
2. There are two **different original units** u_e and v_e with
   u_e supported by an owner of C^- and v_e supported by an owner of C^+.
3. Each of u_e,v_e has request-user set exactly {C}, relative to **all**
   declared requests, including forks and new singletons.

The witnesses can additionally support the other side of C; the two support
sets need not be disjoint. The receiver belongs to a nondeficient component,
since it has private resources. Several receivers may belong to the same
nondeficient component. Several donors may belong to the same deficient tree.
Let d be the number of distinct deficient donor components represented by at
least one candidate, and let w_e>=0 be a candidate's actual activation fee.
Optimize using only E0 and the declared bridges and only the p+g declared
sources.

**Theorem.** The exact maximum payment, minimum fee at that maximum, and minimum
number of actually used new bridges are respectively

    V = p+g-t0+d = V0+d,
    W = sum_(represented deficient tree T) min_(e donated by T) w_e,
    K = d.

There is a construction attaining all three simultaneously. Starting with any
fixed maximum M0, it retains every paid source and every used original unit
of its standard lift, and adds exactly d different previously unused original
units. Recognition and construction are polynomial in the explicit support
incidences and reference paths. There is no 2^k mode search, primitive-packing
enumeration or full routing optimization in the production construction.
No minimum total old-plus-new link count is asserted.

## 3. General proof and the nonreuse ledger

**Reroot one deficient donor tree.** For each represented tree T choose a
cheapest candidate e, with donor request A. A deficient n-vertex tree has
exactly n-1 original edge units and no private units. Every maximum allocation
uses all those units and leaves one request unmatched. Root T at A and give
every other vertex its parent-edge unit. This leaves A unmatched and retains
exactly the old used unit set in T, independently of the old root. All other
requests in T are now matched. If a request is a fork, its now-matched standard
lift pays both sources; thus a previously paid fork baseline source is kept.

**Split the receiver without losing its old unit.** Receiver C is matched in
every maximum allocation because its connected component is nondeficient.
Let r be its assigned unit in M0, and let u=u_e,v=v_e. Since the prefix and
suffix cover C, r is supported on at least one side. Choose a prefix unit l
and suffix unit s as follows:

- If r is u or v, use (l,s)=(u,v).
- Otherwise, if r has prefix support, use (l,s)=(r,v).
- Otherwise use (l,s)=(u,r).

In every case l!=s, one is r, and the other is unused in M0: a private witness
could only have been assigned to C, whose sole assignment was r. Preserve C's
source using l on the strict prefix. Send A's source along its own prefix
through the bridge tail and then along C's suffix, terminating at an owner
supporting s. The old donor suffix is discarded. The paths have disjoint
owners and do not both occupy the mixed entrance. Both units are original.

**Combine all chosen bridges.** Donor trees are disjoint components, and their
old edge units are disjoint. Distinct candidates have disjoint stem pairs.
Their receiver witnesses are private to different requests and hence cannot
be the same original unit, even if the receivers lie in one component. A newly
chosen witness cannot be an old used unit of another request, or any donor
tree edge. Leave every other allocation unchanged. The resulting allocation
and its physical lift preserve all old paid sources and used units, add exactly
one fresh unit and one bridge per represented tree, and gain exactly d payments.
This proves the lower bound and the claimed simultaneous retention.

**Upper bound.** A deficient tree not represented among donors has no candidate
bridge endpoint: receivers are nondeficient. Its n requests still have only
n-1 neighbouring original units and its own unchanged whole-beta baselines,
so it loses at least one request payment in every legal packing. Distinct
untouched trees give t0-d disjoint Hall obstructions. There are only p+g
declared sources, hence V<=p+g-(t0-d).

**Exact fees.** Attaining this upper bound forces every represented donor tree
to lose no request payment. If none of its outgoing bridges is actually used,
it retains its n versus n-1 obstruction. At least one bridge from each such
tree must therefore be used. Every bridge has exactly one donor tree, so their
actual fees sum to at least W and their number is at least d. The construction
uses one cheapest bridge per tree, attaining both bounds. Nonnegative fees
allow zero-cost ties without changing the statement. This argument concerns
actual used bridges, rather than labels of unused mode switches. ∎

The only new credit in this proof is the explicitly unused private witness.
Tree rerooting transfers old units without creating credit. In particular,
two donors in one deficient tree cannot be counted as two repairs: that tree
has just one missing request. Nor can one resource shared by two receivers be
declared private separately for each.

## 4. Physical certificates: capacity-two tiles and occupied bands

Use the restored actual-owner model and the original positive BB/TT forest
components in local two-row bands, rotating the description for vertical bands.
An internal no-P gap has at most two boundary owners, and every unit in the
gap is supported by its boundary owners. Suppose one boundary owner belongs
to C^- and the other to C^+, both in the same receiver request C.

If the gap contains a fully blank aligned capacity-two tile, its two adjacent
BB columns lie in different forest components: an alternating BB/TT component
cannot connect adjacent BB columns. Internal-gap components are positive,
since a TT end next to P would violate feasibility. Thus these two components
are different original units. Both are supported at both gap boundaries and
by no outside owner, so each is private to request C and has both prefix and
suffix support. They certify u_e,v_e without creating synthetic tile credits.

More generally the [two-BB-ends lemma](BENT_GAP_PRIVATE_RESERVES.md) gives two
different units in an internal **even-length** gap with BB at both ends.
With the same receiver-boundary placement this is another certificate.
An odd-length BB,TT,BB gap can have just one unit and does not suffice.

Two different exclusive gaps can instead supply one prefix and one suffix
unit. [Adjacent-band pressure](ADJACENT_BAND_BOUNDARY_REPAIR.md) and the
[occupied-row estimates](BENT_GAP_PRIVATE_RESERVES.md) establish positive
resources under their respective hypotheses, but their output must still be
checked for the required prefix/suffix support and request privacy. Different
maximal gaps have disjoint unit sets. Multiple lower bounds for the same gap
are combined by a maximum, never by addition. Occupied adjacent bands or a
component's scalar surplus alone do not imply this theorem's hypotheses.

## 5. A fully frozen capacity-two bridge, with old unit identities retained

Use the existing [28 by 24 fixture](../develop/fixtures/frozen_all_mixed_gate_cycle.json),
with all local tiles H. No pivot is needed. It has |T|=49, |M|=154, and all
308 actual endpoints are strictly frozen. Fixed compiler owner IDs below are
only names for the actual original bodies.

Choose three old ordinary stems and their actual distinct old interval units:

| Old source and receiver | Actual old link | Old used unit, given by its two cells |
| --- | --- | --- |
| left alpha 6 to mixed 7 | (5,4) to (5,5) | {(14,6),(15,6)} |
| right alpha 12 to mixed 24 | (24,19) to (24,20) | {(24,23),(25,23)} |
| bottom alpha 20 to mixed 14 | (24,17) to (24,18) | {(14,13),(15,13)} |

The new eligible source is top alpha 8, whose direct support is empty. It is
a deficient singleton request. Add the actual bridge (5,6) to (5,5), from
this top source into mixed 7. In the old left stem the strict prefix is alpha 6
and the suffix is mixed 7.

The aligned tile with upper-left corner (14,6) has four blank cells. Its two
original units are

    u = {(14,6),(15,6)},  v = {(14,7),(15,7)}.

For each unit the complete owner-user set is exactly {6,7}. They lie in one
internal gap, so are both private to the left request and available on both
sides of the entrance. Left alpha 6 now stops directly using its **same old
unit u**. Top alpha 8 uses the new bridge, mixed 7, and v. The right and bottom
stems retain their two old units. Payment goes from 3 to 4, all three old paid
source identities and old used units are retained, and just one unused original
unit and one new bridge are added.

For arbitrary q>=1 translate these bodies, selections, actual matching edges,
and links by (30i,0), 0<=i<q, leaving two blank separator rows. The board is
(30q-2) by 24. There is no P owner or declared link across a separator. New
separator interval units have no request users, and are retained in the original
pool without extra credit. The original strict freezing order works independently
in each copy. Thus the construction and the q empty singleton obstructions prove
for **every q**, without extrapolating from enumeration,

    old value = 3q, new value = 4q, minimum new bridges = q,
    old used units retained = 3q, fresh original units added = q.

The full original ledger is |T|=49q, |M|=154q, L=155q-24,
S=L+beta-alpha=157q-24. These boards satisfy the target counting inequality;
they are a nontrivial bridge certificate, not an extremal or negative example.
With bridge fee w_i=1+(i mod 3), the q=16 check gives 48 to 64 payments,
48 retained units, 16 new units/bridges, and minimum fee 31.

## 6. Counting consequence and remaining question

If the reference sources together with N are all original alphas, then the
constructed normalized pack uses each original interval or private whole beta
at most once. Consequently

    L+beta >= alpha-t0+d.

Using the established original ledger S=L+beta-alpha=area/2-|T|-|M| gives

    |T|+|M| <= area/2+t0-d.

If every deficient tree has a qualifying bridge, d=t0, this proves the
coefficient-one inequality |T|+|M|<=area/2 on this certified class. Compared
with the previous old-link certificate the residual term drops by exactly d.
This does not improve the universal 5/6 theorem: existence of these private
pre/post certificates for all residual configurations has not been established.
The earlier upper-bridge obstruction fails precisely at prefix support and is
excluded here. Shared-stem bridges, nonprivate reserves, beta entrances and
external relays require additional arguments. A rejected certificate does not
disprove the target inequality or even full payment in the original network.

## 7. Validation and formal scope

The [production solver and independent checker](../develop/check_private_prefix_bridge.py)
checks actual supplied geometric witnesses rather than trusting their labels.
It accepts an arbitrary supplied maximum baseline allocation and reconstructs
the lift from its specific original unit IDs. The saved
[Python report](../output/private-prefix-bridge-validation.json) records:

- 31 independent maximum-payment/minimum-bridge-fee comparisons, with primitive
  and full-flow value checks, and 31 source/unit-set retention checks;
- 169 checks over every maximum baseline allocation in the selected small
  controls, including old assignments different from either displayed witness;
- a two-bridge, one-donor-tree control with exact value 3 to 4, gain 1 rather
  than 2, and minimum fee 2 rather than 5;
- rejection of a shared reserve private only to the union of two receivers;
- four frozen boards q=1,2,4,16 and 7,084 replayed strict freezing events;
- an independent polynomial full-flow comparison for q=4, and a production
  q=16 run in which mode enumeration, primitive optimization and full flow
  are explicitly disabled. Independent primitive comparisons use q<=2.

These finite checks audit implementation and examples. The theorem and all-q
extension are proved above without finite enumeration.

The [Lean source](../formal/SubQuorum/PrivatePrefixBridge.lean) proves the general
local resource exchange: given distinct private pre/post witnesses and an old
used unit supported on some side, one can keep that old unit and add an unused
different unit on the other side. The proof covers the old unit equalling
either witness or neither. Its declaration has **no axiom dependencies** under
Lean 4.33.0, as recorded in the
[formal audit](../output/private-prefix-bridge-formal-validation.json).
There is no sorry, native_decide, added axiom or compiler warning. This kernel
does not formalize tree rerooting, physical routing, exact costs or geometry;
those have the written proofs and executable audits described above.

Reproduce the executable check and the scoped local Lean audit with:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 develop/check_private_prefix_bridge.py \
  --output output/private-prefix-bridge-validation.json
PYTHONDONTWRITEBYTECODE=1 python3 develop/check_private_prefix_bridge_formal.py \
  --lean /path/to/lean-4.33.0 \
  --output output/private-prefix-bridge-formal-validation.json
```

The formal runner measures available memory and enumerates actual lean/lake
processes by the basename of the full comm field immediately before each Lean
executable invocation. Execution remains a local per-task verification detail.
