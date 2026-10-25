# Exact extremal cost of shared units and full-pool path circuits

25 October 2026. Wenlin Zhang and Haobo Ma. Research branch only.

We link the shared-singleton obstruction to a sharp selection budget. On the
known adjacent-module endpoint family, opening each designated shared unit
costs at least one selection relative to the TRUE fixed-P maximum. The bound
is simultaneously attainable, with full freezing, for every subset of units.
These near-maximum boards realize arbitrarily long path circuits in their
FULL original resource pools: every proper source subset is payable, but
all sources are not, and every bounded-order withdrawal test can miss the
unique violating withdrawal. We determine the cost of every maximum paid
source set. A two-module specialization gives a positive-local-payment
mixed interface obstruction exactly one selection below the true maximum.

This develops the existing [adjacent maximum family](FORCED_MATES_AND_ADJACENT_MAXIMA.md),
the [full-pool interface profile](FULL_POOL_INTERFACE_SINGLETON_AND_REPAIR_PROFILE.md)
and the [resource-gluing path proof](ENDPOINT_COMPONENT_RESOURCE_GLUING.md).
The earlier path example used a restricted pool and its full pool paid all
sources. The present family has the path obstruction with EVERY actual
original unit available. It is not a new general matching theorem. This
fixed-P family also has the existing vertical full-compensation theorem;
we do not claim failure for all auxiliary partitions, global P/T extremality,
a counterexample to the grid inequality or a new universal 5/6 bound.

## 1. Fixed endpoints and exact constrained maximum

Fix even W>=8 and k>=1. Use P and its unique actual matching M from
configuration(W,k), on the (W+2)-by-(10k+2) grid. A feasible selected set U
avoids P and each selected vertex has at most one occupied neighbor in U
union P. The proved maximum over ALL such U is

    t(W,k)=(7k+2)W/2+3k+2.                                    (1)

Let T* be the explicit fully frozen attainer in that note. For each seam
index i=1,...,k-1 designate the two cells

    b_i=(W,10i+1),   x_i=(W+1,10i+1),
    j_i=(W/2,10i+1,10i+1).                                   (2)

Say seam i is open if both b_i,x_i are unselected. These are not endpoints.
The neighboring bottom-band columns10i and10i+2 cannot be TT under ANY
feasible U: their upper cells face fixed endpoints at10i-1 and10i+3,
respectively. Thus an open seam's BB column is indeed an isolated original
BB/TT-forest unit j_i; it is not merged into a balanced boundary chain.

**Theorem 1 (exact simultaneous opening budget).** For any E subset
{1,...,k-1}, the maximum |U| over all feasible U for which every seam in E
is open is

    max |U|=t(W,k)-|E|.                                      (3)

A fully frozen attainer is

    T_E=T* minus {x_i : i in E}.                             (4)

It opens exactly E. More generally if B(U) is the set of all open seams,

    |U|+|B(U)| <= t(W,k).                                   (5)

This allows arbitrary removal/reselection of U; it is not an extension-only
claim and does not assume the original terminal types survive.

**Proof.** Retain the disjoint cover proving (1): aligned two-by-two tiles,
with the 2k disjoint four-by-two patch replacements at (0,2+10a) and
(W-2,2+10a), each lowering cap four to three. Its total cap is t(W,k).
For an open seam i, the UNREPLACED tile

    G_i={W,W+1} times {10i,10i+1}

has its column10i+1 empty. The only possible selected sites are its two
column10i cells. They cannot both be selected: the upper one would then
have its fixed P neighbor (W,10i-1) and its selected lower neighbor.
So cap(G_i)<=1, one below its old cap two. All G_i are pairwise disjoint
and disjoint from every replaced patch. Subtracting one for every open seam
in the SAME cover proves (5) and the upper bound in (3), without reusing a
physical tile or a surplus.

In T*, b_i is blank and x_i is an isolated selected vertex. Its three board
neighbors are unoccupied, and no P is adjacent to it. Delete just the x_i
for i in E. Feasibility and every old endpoint neighborhood are unchanged;
the old all-W/k strict freezing schedule replays unchanged. The resulting
size is t-|E| and exactly those seams are open. This attains (3). ∎

The fixed-P matching is unique, so allowing arbitrary rematching on P does
not alter this optimum. Neither theorem optimizes over replacing P itself.

## 2. Exact FULL-pool compensation after any opening subset

Use the original aligned horizontal bands and ALL original resource units,
including boundary units and units outside any source-reachable closure.
Put m=|E|. For T_E,

    alpha=k, beta=0, mixed=7k, raw units=3k+m;
    numerical slack S=2k+m>0;
    full maximum payment V=m, deficit D=k-m;
    minimum links at that maximum=m.                         (6)

Thus S+D=3k throughout this explicit deformation. This is a formula for
T_E, not an asserted rank formula for every U satisfying the seam constraints.

**All-route proof.** Module a (a=0,...,k-1) has one original alpha
A_a with ordinary tips (1,10a+5),(W,10a+5). Its directed owner closure has
exactly seven owners: A_a, three upper mixed branches and three lower
mixed branches. The complete non-self transitions are

    A_a -> U0_a,U1_a,L0_a,L1_a;
    U1_a -> U2_a;      L1_a -> L2_a.                        (7)

This follows from the same sealed column lists as the previous interface
proof. All upper branch supports are empty. L0_a supports only j_a if
a is in E (a>=1); L2_a supports only j_(a+1) if a+1 is in E; every other
reachable support is empty. There are no beta owners, and no non-self exit
leaves these seven-owner closures. The remaining one mixed owner per module
and all cycles are unreachable. In particular the 3k other actual original
units remain physically present but cannot pay an alpha, even after arbitrary
rerouting.

For clarity, L0_a has tips (W,10a+3) TP and (W,10a+4) BP. Its left gap
columns10a,...,10a+2 has precisely three selected cells before opening,
and two after deleting x_a; the only new BB is j_a. L2_a has tips
(W,10a+8) BP and (W,10a+9) TP, and the corresponding right gap has only
j_(a+1) after that seam is opened. A_a's interior body in column10a+5
has P columns on either side in every middle band, so it has no hidden
middle support. The top gaps remain sealed. This proves (7) and the full
support list uniformly for every W,k,E.

Each payment must therefore use one of the m DIFFERENT units j_i, giving
V<=m. For each i in E pay the RIGHT source A_i by j_i through its one
outward link

    (W,10i+5)->(W,10i+4).                                  (8)

The source IDs, links, mixed owners and original resource IDs are all
distinct, so these m payments coexist and give V=m at m links. No source
has own support, hence every payment needs at least one link and that
cost is minimal. Counting T,M and area gives S=2k+m; the exact original
resource ledger L=S+alpha-beta then gives L=3k+m. ∎

The original grid-neighbor P-components are exactly the k separated slabs,
not just components of a chosen terminal matching. Every actual link stays
inside one slab. After source-reachability pruning, retaining ALL original
unit IDs, j_i is supported by exactly L2_(i-1) and L0_i. Each such class
has one original unit; the exact saturation lemma cannot privatize it.
The shared-resource support graph is the path on A_0,...,A_(k-1), with
only the edges in E present. Each connected run leaves exactly one source
unpaid; isolated vertices also contribute one. Thus D=k-m also counts
components of this path forest.

## 3. Arbitrarily large FULL-pool circuits and a unique violating withdrawal

Take k>=2 and E={1,...,k-1}. Every P-component can separately pay its one
alpha, yet the full model pays exactly k-1. ALL original units are available:
there are 4k-1 of them, so the failure is not a raw resource-count shortage.
Its numerical slack is 3k-1, and it is exactly k-1 selections below the
true fixed-P maximum, the optimal price of opening these k-1 seams.

Every proper subset of the k source identities is payable. To see this,
choose an omitted source A_r (0<=r<k). Assign

    A_a -> j_(a+1) if a<r,
    A_a -> j_a     if a>r.                                (9)

These are precisely the k-1 distinct units, each incident to its assigned
source. Left-of-r sources use their two-link lower inward routes; right-of-r
sources use the one-link outward routes. They are disjoint inside each
module and across modules. A smaller source subset follows by removing its
unneeded source paths. The set of all k sources is therefore a minimal
unpayable set, on the full original pool.

There is also a unique violating withdrawal in the ENTIRE original pool.
Let Q be the full original pool, Qpath={j_1,...,j_(k-1)}, and let V_a(F)
be the original P-component maximum with F available. Then V_a(Q)=1.
For J subset Q define its joint withdrawal excess

    excess(J)=sum_a[V_a(Q)-V_a(Q minus J)]-|J|.              (10)

**Theorem 2.** excess(J)>0 if and only if J=Qpath, in which case it is one.
In particular, for every bound b choose k>=b+2. Every withdrawal of at most
b units passes the no-overlap inequality, while full compensation still
fails on the complete original pool.

**Proof.** A component loses its payment exactly when all its incident path
edges have been withdrawn. If an edge j_(r+1) survives, send every losing
vertex toward that edge: a<r maps to j_(a+1), and a>r+1 maps to j_a. Its
image is withdrawn because it is incident to that losing vertex. The two
image ranges are disjoint and each range is injective, giving at most
|J intersect Qpath| losing components. Thus excess(J)<=0.

If all path edges are withdrawn, all k components lose their payment and
excess(J)=k-|J|. With J=Qpath it is k-(k-1)=1. If even one other actual
original unit is additionally withdrawn, |J|>=k and the excess is at most
zero. Other originals do not affect the component ranks, by the arbitrary-
route closure. These exhaust all withdrawals and prove the uniqueness. ∎

This strengthens the earlier restricted-pool path diagnostic: here the
FULL physical pool itself has the circuit, and the sharp selection budget
quantifies how far its opening pattern lies below the fixed-P optimum.
It refutes a bounded-order full-pool withdrawal checking rule, not the
numerical grid inequality.

## 4. Every maximum source basis has an exact link cost

In the full path, prescribe that all sources except A_r remain paid.
Every maximum uses every j_i. Its matching is forced: j_1 must go to A_0
if r>0, then j_2 to A_1, and so on up to r; the same forcing from the
right boundary assigns j_(k-1) to A_(k-1) down to r+1. Hence (9) is the
unique original-unit allocation for that paid source set. The left r
sources need two links each, and the right k-1-r sources one each. Thus

    minimum links preserving {A_a:a≠r} = k-1+r.              (11)

The explicit routes attain this lower bound. In particular all k maximum
paid source sets exist, but their minimum costs range from k-1 to 2(k-1).
The difference comes from routing the same original shared units to different
source identities; there is no change of physical board or resource pool.

## 5. One-below-maximum mixed interface specialization

For k=2 and E={1}, the construction is T*=fixed_p_maximum(W) minus
{(W+1,11)}, so |T|=8W+7. Theorem 1 proves this is the exact largest feasible
selection with that shared original unit open, whereas the unconstrained
true fixed-P maximum is 8W+8. All endpoints remain frozen.

Now use the legitimate two-region partition: columns0,...,13 horizontal,
columns14,...,21 vertical. Its two actual M crossings and right CC relay
create one interface alpha I with tips (1,13),(W,13); the left closed alpha
A has tips (1,5),(W,5). As in the eight-owner interface closure, A can only
reach j_1 in two lower links, and I supports j_1 directly with no other exit.
Selected extensions in the middle change source-free owners but introduce
no exit from this closure. Thus, with the FULL original pool,

    local old payment=1 at two links;
    interface standalone matching=1;
    joint/full payment=1, theta=0, deficit=1;
    unconstrained minimum links=0, old-source-protected minimum links=2.

Here alpha=2, beta=1, mixed=W/2+5, original units=6 and numerical slack=5.
This is a positive-old-payment interface obstruction exactly one selection
below the true fixed-P maximum; its one-point distance is sharp for retaining
this BB singleton. It does not show that an exact maximum with another
network or another P has no such obstruction. The finite partition searches
on the known maximum attainers are diagnostic only, not a general theorem.

## 6. Verification, formal scope and next question

    python3 develop/check_extremal_path_circuits.py \
      --output output/extremal-path-circuits-validation.json

The verifier independently checks physical feasibility, all endpoints frozen,
the uniform strict schedule and unique-matching leaf order; the disjoint
upper cover and seam-tile loss; exact owner reachability and FULL original
supports; values, deficits, minimum costs and proper source bases; and joint
withdrawals with and without inaccessible original units. Small models use
independent primitive packing. The all-parameter statements above rely on
written proofs, with enumeration used only to corroborate their adapters.

[Lean source](../formal/SubQuorum/ExtremalPathCircuits.lean) verifies the local
two-neighbor obstruction behind the tile loss, the additive selection-budget
arithmetic, an injective payment for every omitted source, the forced left
and right allocations of every maximum source basis, its exact cost arithmetic,
and the retained-edge injection used for proper withdrawals. The actual
small physical fixture is aligned with the compiler separately. General
coordinate extraction, full freezing, finite-cardinality sums and the full
flow equivalence remain written proofs plus independent code, not an
end-to-end Lean grid theorem.

The [computational receipt](../output/extremal-path-circuits-validation.json)
records 95 frozen horizontal boards, 28,010 strict freezing events, 14,005
forced matching pairs, 339 independent seam-tile capacity checks, 434 exact
seven-owner closures, 48 independent primitive packing profiles, 100 maximum
source-basis cost checks, 184 proper-source-subset checks and 629 full-pool
path withdrawals. These include 100 withdrawals with actual inaccessible
units added, plus seven mixed-interface heights through W=128.
The [formal receipt](../output/extremal-path-circuits-formal-validation.json)
and [compiler log](../output/extremal-path-circuits-lean-validation.txt) record
Lean 4.33.0 passing 17 new declaration audits and 11 dependency audits, with
no warnings, unproved placeholders, native evaluation or new axioms.
The general statements use written arguments; these finite and scoped formal
checks do not enlarge their stated scope.

The next general problem is to charge shared singleton obstructions against
valid extremality losses or changes of auxiliary partition without counting
the same physical tile twice. In this specific endpoint family all feasible
T have the previously proved vertical full compensation. Thus these results
locate the obstruction and its exact selection price in the chosen horizontal
or mixed partition; the universal grid bound remains open.
