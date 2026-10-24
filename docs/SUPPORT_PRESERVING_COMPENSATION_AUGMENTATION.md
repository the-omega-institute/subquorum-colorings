# Compensation augmentation preserving paid sources and used resources

23 October 2026. Authors: Haobo Ma and Wenlin Zhang.

The frozen-chain obstruction rules out fixing every old demand-to-resource
assignment. A weaker invariant does extend to a maximum compensation: preserve
the identities of paid sources and used resources, allowing the routes and
their pairings to change. This is an application of standard integral-flow
augmentation to the previously proved compensation normal form. It supplies
the precise invariant for a possible grid argument, not the missing geometric
budget or a new general flow theorem.

## 1. Hypotheses and statement

Fix a finite strand system, a set of permitted witnessed TP--BP links, and
terminal-to-interval accesses as in COMPENSATION_FLOW_NORMAL_FORM.md. Each
alpha owner is a unit-capacity source; each mixed owner has a unit-capacity
entry-to-exit arc; every whole beta and every distinct permitted interval is
one unit-capacity sink resource. Link and access arcs have capacity k+1, where
k is the number of alpha owners. Retain their terminal witnesses, including
parallel arcs. Mixed self-links are omitted.

If there is a previous immutable cancellation C0, first contract it to the
current strand system. Every source identity below refers to that system.
No step changes C0 or grants access to a marked/excluded interval.

Let f be a feasible integral packing of witnessed source-to-resource routes.
It is already in the directed-path normal form. Write D(f) for its paid
original alpha source identities and R(f) for its used beta/interval resource
identities. Do not identify D(f) with arbitrary pre-normalization names of
final alpha strands or with an arbitrary earlier pairing.

**Augmentation lemma.** If f is not maximum, there is a feasible normal-form
packing f' of value |f|+1 such that

    D(f) is contained in D(f'),    R(f) is contained in R(f').

Each difference has size exactly one. All resource and mixed-owner capacities
remain one; its selected terminal links form a legal matching. Iteration gives
a maximum packing with nested paid-source and used-resource sets.

The statement permits replacing links selected after C0, changing intermediate
mixed owners, and changing source-to-resource pairings. It makes no assertion
that minimum link cost among all maximum packings is attained while preserving
these sets, or that every individual low-level edit preserves every payment.

## 2. Proof

Adjoin a super-source s with one capacity-one arc s->a for each alpha a, and
a super-sink t with one capacity-one arc z->t for each resource z. There are
no original arcs into s or out of t. Use the ordinary residual directed
multigraph with separate reverse arcs for each witnessed original arc.

If f is not maximum, its residual network contains an s--t path. Indeed,
otherwise the set reachable from s defines a saturated forward/empty backward
cut whose capacity is |f|, establishing maximality. Choose a simple residual
path P and augment one integral unit along it. Residual capacity guarantees
all updated flows remain integral and between zero and their capacities;
each interior vertex has one entering and one leaving residual step, so flow
conservation holds and the value increases by one.

A used source arc s->a cannot lose flow. To decrease it, P would have to use
its specific reverse arc a->s, returning to its initial vertex. Simplicity
excludes this. A used resource arc z->t cannot lose flow either: its reverse
t->z would depart from t before the path ends, revisiting the final vertex.
Simplicity excludes that as well. These arguments concern the specific
reverse arcs, so parallel witnessed internal arcs cause no ambiguity.

The first residual step leaves s along a previously unused original source
arc. The last enters t along a previously unused original resource arc.
All boundary capacities are one, so exactly one source and one resource are
added and every previously used boundary arc remains saturated.

Remove any directed positive-flow cycles in the original network and decompose the remaining flow
into simple s--t routes. No original directed cycle contains s or t, hence
cycle removal preserves all boundary flows and the two support sets. Each
mixed owner's split arc has capacity one, so distinct routes cannot share it;
the same holds for source and resource arcs. The forward direction of the
normal-form theorem then supplies a legal terminal matching and interval
allocation with precisely this compensation value. In particular, a whole
beta is still used at most once and no interval or terminal is duplicated.
This proves the lemma. Repetition terminates at the finite maximum. QED.

The augmentation is a simultaneous change of a certificate. If implemented
by removing old links and adding new links, intermediate partial matchings
can lose payments. Only the resulting normalized packing and the sequence
of completed augmentation certificates have the stated preservation property.

## 3. Replacement of a selected link can be essential

Here is an abstract strand example, not a claimed frozen-grid realization.
Take alpha pairs (0,1), (2,3), and mixed pair (4,5), with 4 labelled BP and
all other terminals TP. Permit exactly links (0,4), (2,4). Let TP5 access
interval x and TP1 access a different interval y; no other access exists.

The old route pays alpha (0,1) through link (0,4), the mixed owner and x.
If this selected link must remain, alpha (2,3) cannot enter the occupied
mixed owner, and it has no other route. Compensation is at most one.

The full packing instead pays alpha (0,1) directly at y, and pays alpha
(2,3) through (2,4), the mixed owner and x. The old source and old resource
x both remain used, but link (0,4) is replaced by (2,4). Its residual
augmenting path uses the reverse of the old link. Thus allowing only newly
added links, even while permitting resource reassignment, is insufficient
for this general lemma. C0 remains fixed; the replaced link was selected
after C0.

## 4. Cost and geometric limitations

Preserving old support can obstruct unrestricted minimum link cost. With one
alpha (0,1), one mixed pair (2,3), link (0,2), and accesses TP3->x and TP1->y,
the old route via the mixed owner uses x and costs one. Any route retaining
resource x costs one, whereas the unrestricted maximum has value one and
cost zero by paying directly at y. Cardinality preservation does not imply
preservation of an unconstrained cost optimum.

The frozen shared chain gives a physical test of the lemma's useful scope.
Start from F_(r-1), in which g_i pays d_i. A residual augmenting path from
d_(r-1) reverses each occupied access in turn, until d_0 can use its one
remaining mixed gate and private h_0. The final packing still uses all old
g_i and pays all old sources, while changing all r-1 old pairings. There is
one new link, one new source and one new resource. This reconciles the
augmentation lemma with the protected-chain obstruction.

Neither theorem proves that an arbitrary frozen grid has enough routable
resources. After reaching maximum value nu, the exact ledger remains

    S-B = Q-delta,    Q=|I|+b-nu,    delta=k-nu.

Augmentation eliminates deficits caused only by a poor existing allocation.
A positive terminal deficit still needs a geometric proof that Q>=delta,
or another valid physical compensation mechanism. Outside/boundary corrections
must retain their existing multiplicity; the lemma creates no new credit.

## 5. Verification scope

The independent augmentation checker starts from arbitrary feasible packings,
including nonoptimal ones, uses residual BFS with reverse witnessed arcs,
and checks capacities, conservation and both nested support sets after each
augmentation. It reconstructs the actual terminal matching and payment
incidences and compensation value. Source and resource identity inclusion is
checked on flow boundary tags, rather than independently reconstructed
component identities. A separate feasible-flow fixture contains a nonzero
internal circulation; normalization discards it while preserving both boundary
supports. Small strand systems are compared with exhaustive terminal-link
matchings; larger controls are compared with the accepted maximum-flow solver.
The replacement example forces a reverse link. Physical shared chains are
checked both with all permitted links and with only the known root-0 repair
link allowed; the latter forces an unbounded number of reverse accesses.
The unrestricted BFS need not minimize link count and may use the nearer
two-link repair instead. Finite checks support this written
proof and do not replace it.

The recorded run checks 4,608 exhaustive strand models against 34,304 terminal
matchings, 160 larger random models, and 48,523 initial-packing controls with
32,334 completed augmentations. There are 69 physical chain families and
138 physical augmentations, plus 69 unrestricted last-resource deletion
certificates for the subsequent Pareto theorem. For W=6 and r=2,3, a separate
enumeration checks 4,896 arbitrary additional terminal matchings and 1,140
full interval allocations, recovering the exact Pareto frontiers.

The five Lean interface theorems verify that an injective finite path cannot
re-enter its start or leave its finish; forward residual availability and
reverse walk incidence then imply saturated source/resource arcs are
untouched, and residual moves avoiding an arc preserve its flow. Integral
max-flow existence, decomposition, the normal-form adapter and the geometry
remain written proofs.

Run the finite checker:

    PYTHONDONTWRITEBYTECODE=1 python3 develop/check_compensation_augmentation.py --output output/compensation-augmentation-validation.json

The new Oracle review was submitted before the final all-matching/all-allocation
controls and the last three Lean interface lemmas were added. Its input already
contained the written augmentation theorem and the exact Pareto-frontier proof;
later execution evidence is recorded separately.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
