# Exact component reserves under monotone mixed extension

25 October 2026. Haobo Ma and Wenlin Zhang. Research branch only.

An actual mixed extension can reach an interval already paying another alpha.
That does not create a new unit: the unpaid root may merely move into the
previously paid component. Two extensions can also reach the same previously
unowned interval. We give an exact common account of both phenomena.

For each component after a monotone incidence extension, let d be the number
of old deficient components it contains and S the number of **old unused
original units** in that component. Then the payment gain is exactly min(d,S).
The remaining deficit is at most one per resulting component. This is a
dynamic bookkeeping consequence of the established two-owner allocation
theorem, not a new general matching theorem. It gives an ownership-preserving
adapter for mixed continuation; it does not prove that arbitrary grids supply
a successful collection of continuations.

Dependencies: [two-owner interval allocation](ONE_SIDED_INTERVAL_AND_BETA_ALLOCATION.md),
[whole-support access](BOUNDARY_SEALED_GAP_OBSTRUCTION.md),
[the physical terminal donor collision](SHARED_DONOR_COLLISION_AFTER_MIXED_RELAYS.md),
and [the sharp direct-beta failure with mixed repair](BETA_CLOSING_AND_SHARP_MIXED_DEFECT.md).

## 1. Fixed identities, monotonicity and components

Let A be a fixed finite set of alpha demands and I a fixed set of distinct
available original interval units. Write E0(j),E1(j) for the sets of eligible
owners before and after a declared extension. Assume, for every j,

    E0(j) subset E1(j) subset A,       |E1(j)|<=2.           (1)

No new interval is created, no old incidence is lost, and alpha identity is
stable. Parallel resources remain different units. Two ports of the same
owner count as one owner. Keep beta units outside this interval account; in
the physical mixed-only specialization their number stays fixed.

As before, a two-owner unit is an edge of a multigraph on A, and a one-owner
unit is a private resource at that vertex. Zero-owner units lie outside the
owner components. For an old component C write n_C for its owner count and
m_C for its incident resource count. Connectivity implies

    m_C>=n_C-1.

It is deficient exactly when m_C=n_C-1, equivalently a tree with no private
unit. It otherwise has a full allocation, using n_C resources, and leaves
s_C=m_C-n_C>=0 unused resources. A maximum old allocation therefore leaves
one root unpaid in every deficient component and pays every other demand.
These are the previously proved static allocation facts.

By(1), every old owner component lies wholly within one new owner component.
For a new component H define

* d_H: the number of old deficient components inside H;
* s_H: the sum of m_C-n_C over all old nondeficient components inside H;
* l_H: the number of original units j with E0(j) empty and E1(j) meeting H;
* S_H=s_H+l_H.

The l_H units are newly **activated**, not newly created. Different H have
disjoint owners, old components and original units.

## 2. Exact merge and payment formula

**Theorem 1.** Under(1), for every new component H,

    |I_H|-|A_H| = S_H-d_H >= -1.                         (2)

The new component is deficient exactly when d_H=S_H+1. Its payment gain over
the old maximum allocation restricted to H is exactly

    g_H = min(d_H,S_H).                                   (3)

For **any** maximum old allocation F0, S_H is exactly the number of its unused
original units in I_H. In particular(3) counts the same old reserve pool for
every maximum baseline, even though the identities of particular unused units
may differ with that baseline.

**Proof.** Every new incident unit is either incident to an old component in
H already, or is one of the l_H formerly zero-owner units. These alternatives
are disjoint, by original identity. Old components partition A_H. Consequently

    |I_H|-|A_H| = sum_C (m_C-n_C)+l_H = -d_H+s_H+l_H.

The new owner graph is connected and each unit has at most two owners, so
it has at least |A_H|-1 incident units. This proves(2). If equality is -1,
the ordinary edges are a spanning tree and there is no private unit; otherwise
the component has an anchor or a cycle and is fully paid. Thus its new maximum
payment is |A_H|-epsilon_H, where epsilon_H=1 if d_H=S_H+1 and0 otherwise.
Its old maximum payment was |A_H|-d_H. The gain is d_H-epsilon_H. Because
d_H<=S_H+1, this is exactly min(d_H,S_H), proving(3).

Every old deficient component uses all m_C=n_C-1 of its resources. Every old
nondeficient component uses n_C and leaves exactly m_C-n_C unused. No old
allocation uses a formerly zero-owner unit. These exhaust the original units
in H, so the unused count is exactly S_H for every maximum F0. QED.

**Corollary 2 (global nonreuse and exact full-coverage test).** If t0,t1 are
the old and new deficient-component counts and U0,U1 the unused resource
counts at maximum allocation, then

    g = sum_H min(d_H,S_H) = t0-t1,
    U1 = U0-g,
    t1 = #{H : d_H=S_H+1}.                               (4)

Full interval compensation occurs if and only if d_H<=S_H for every H.
Every component separately consumes at most its own S_H old unused units;
these pools are disjoint across H, so g<=U0. If beta=b is unchanged, the
signed account is invariant:

    U0+b-t0 = U1+b-t1.                                    (5)

This criterion is exact **after the legal extensions and their incidences
are declared**. It does not assert that suitable extensions exist, that they
use disjoint mixed gates automatically, or that an arbitrary root can reach
every resource in the component.

## 3. Keeping old paid owners and used original units

**Theorem 3.** For any maximum old allocation F0 there is a maximum new
allocation F1 that keeps every old paid demand paid and keeps every used
original interval identity in use. It adds exactly g different previously
unused original units. It need not keep each old owner's particular assignment.

**Proof.** By monotonicity F0 is a legal matching in the new demand--resource
incidence graph. If not maximum, its symmetric difference with a larger
matching contains an augmenting alternating path from an unpaid demand to an
unused resource. Choose a simple such path. In its indexed order, write the
distinct owners v0,...,vn and distinct resources r0,...,rn, with old pairs

    v_(i+1) uses r_i,       i=0,...,n-1,

and eligible new pairs v_i uses r_i for i=0,...,n. Flip these assignments.
Each old owner on the path stays paid, each old used resource on the path
stays used, and v0 plus the previously unused rn are added. All off-path pairs
stay unchanged. Simplicity proves both owner and resource nonreuse. Repeat;
each step increases payment by one and the finite maximum is reached after
exactly g steps. This construction also shows all added units are different.
It applies component by component because H have disjoint resource pools. QED.

In particular reaching an already used interval is permitted, but the payment
counts only if the alternating reassignment ultimately reaches an old unused
unit. Counting the first reached used interval as fresh surplus is incorrect.

## 4. Legal mixed extension and the access-interface distinction

In the whole-support model, start after a fixed C0 and choose additional legal
mixed-only continuation paths. Each component of the additional owner splicing
must contain exactly one current alpha and otherwise only mixed owners; mixed
owners and terminal endpoints must not be reused, and no beta is consumed.
One resulting alpha corresponds to each old alpha. Its support is its old
support together with the traversed mixed supports. All old original P-column
witnesses remain in the same resulting alpha. Available original intervals and
their marks do not change. Thus old support incidences persist. The established
gap-side argument bounds each interval by two owners after splicing, so(1)
holds with stable owner labels. Theorems1--3 then apply.

This is a counting-interface statement, not a claim that internal PP access
can always be implemented by a free terminal route. Conversely free-tip-only
access is not generally monotone when a mixed link consumes a ported TP. For
that smaller interface Theorems1--3 apply only when(1) is separately checked.
One must not silently substitute one interface for the other.

The earlier actual [terminal/cap collision family](SHARED_DONOR_COLLISION_AFTER_MIXED_RELAYS.md)
does satisfy(1) in the following transitions. Before either continuation it
has two isolated terminal demands, no incident interval, d=2. After both
distinct mixed continuations their single shared original interval gives S=1.
They form one deficient component; g=min(2,1)=1, rather than2.

After only the left continuation, that same interval already pays the left
alpha; the right alpha is deficient. Adding only the right continuation now
merges one deficient tree with one tight, paid component. This has d=1,S=0,
so g=0. The right continuation reaches an interval but creates no credit.
The symmetric transition is identical. These are existing physical examples,
now placed in the exact before/after account, not new constructions.

For the **whole-support** interface, this collision family's original internal
PP supports already pay both alphas. Its terminal/cap d=2 must not be reported
as a whole-support deficiency. The archived sharp-beta-closing family instead
has a genuine whole-support d=1,S=1 mixed repair, giving g=1 and preserving
the specified old B->J assignment.

## 5. Evidence and remaining work

The general results are proved above using the established static allocation
and elementary augmenting paths. The verifier exhausts7,615 monotone old/new
incidence systems on three resources and at most three demands, adds1,200
seeded larger systems and three explicit controls, and checks357 alternative
maximum old baselines. It independently recomputes maximum payment and replays
baseline-preserving augmentation. Physical controls comprise4,005 legal
mixed-only batches on four frozen fixtures with stable alpha IDs, plus85
terminal/cap merge transitions in the archived all-even-width collision family.
Total13,265 models and23,302 component identities pass. These whole-support
fixture controls contain **zero** cross-component merge clusters; the actual
nontrivial merging controls here use the explicitly identified terminal/cap
interface. No physical whole-support collision is inferred from abstract ones.

Eleven scoped Lean declarations prove arbitrary-length indexed augmentation
preserves paid owners and used units, forbids owner/resource reuse, introduces
one new unit and pays a new root; component deficiency/gain arithmetic and
ledger conservation also pass. The finite component partition, cardinality
adapter, existence of augmenting paths and full physical specialization remain
written proofs with deterministic checks, not a full formalization. No new
external review is claimed.

The next task is constructive: find mixed continuations with enough distinct
old unused units in **every resulting component**, while retaining gate
capacity; or exhibit a genuine whole-support collision/obstruction. Theorem1
then supplies the exact audit and Theorem3 supplies the safe allocation update.
A general existence theorem and a universal5/6 improvement remain open.
