# Private bypasses, many relay modules, and a joint compensation bound

25 October 2026. Wenlin Zhang and Haobo Ma. Isolated research branch.

The preceding [two-source shared-relay lemma](TWO_SIDED_DEAD_ESCAPES_AND_SHADOW_RELAY.md)
uses direct support to release a shared mixed gate. We extend this to any
finite number of sources and relay modules, with original resource identities
shared arbitrarily. A unit-capacity module with at most two source entrants
can have its capacity constraint removed if at most one available output
unit lacks a suitable private bypass at either entrant. The covered outputs
need not all belong to one fixed source: two assignments may be swapped.

More generally, a capacity-c module with at most c+1 source entrants is safe
when at most c available output units lack such bypasses. A joint packing
number kappa counts the remaining possible losses using disjoint input groups
AND distinct original resource units. If nu is the ordinary source-resource
matching rank after relaxing the relay capacities, then

    payment >= nu-kappa,
    unpaid <= (number of sources-nu)+kappa.                 (1)

The reduction and counting proofs are general for the specified one-stage
model. A physical adapter covers beta-free original strand systems whose
reachable vertical-BP mixed owners receive links directly from alphas and
whose downstream horizontal-BP forests do not feed another vertical owner.
Freezing does not by itself imply that adapter hypothesis. We verify it on
the earlier completely frozen 56P/26T board and its copies; no new grid is
claimed. Capacity-two results below concern common-output relay modules,
not arbitrary capacity-two geometric tiles. The universal 5/6 bound remains
open.

## 1. Complete model and what a private bypass means

Let A be a finite source set, I a finite set of ORIGINAL resource identities,
and G a finite relay set. Fix an arbitrary available subset Q of I.
Each source can be paid at most once and each resource can be used once.
For each source a, private resources D_a subset I have costs d_a(j)>=0.
A private route may be direct access or a route through owners belonging
only to a. Private route owner sets of DIFFERENT sources, and private
versus relay owner sets, are disjoint. Different private routes of one
source may overlap because that source selects at most one route.

Relay g has capacity c_g>=1, source entrants U_g subset A, common outputs
R_g subset I, and nonnegative entry/output costs e_g(a),o_g(j).
Every entrant can use every output through that relay, at cost

    e_g(a)+o_g(j).                                        (2)

The only conflicts among routes through relay modules are source identity,
resource identity and each module's total capacity c_g. Internal paths must
realize these costs and have no extra conflicts below that capacity. In
particular no hidden owner may be reused by supposedly separate modules.
Source sets U_g and resource sets R_g may overlap between modules.
This theorem assumes

    |U_g| <= c_g+1                                        (3)

for every g. The model is one-stage: a paying route uses either its private
route or one relay module, not a succession of relay modules. Private
costs and relay output costs are defined in the ORIGINAL board before Q
is restricted; no resource identity or original support is recomputed.

All these hypotheses concern the complete paying-route description. If
only selected original routes are included, the theorem gives a certificate
for that selected class, and equality claims do not extend to the full board.

## 2. Covered output units and the local exchange

Call j in R_g **covered at g** if some a in U_g has a private route to the
SAME original unit j at no greater cost:

    j in D_a and d_a(j) <= e_g(a)+o_g(j).                  (4)

Let E_g(Q) be the available output units not covered at g:

    E_g(Q) = (Q intersection R_g) minus
             union_(a in U_g) {j in D_a: (4) holds}.      (5)

This is a set of original IDs, not a list of support witnesses. Direct
whole support has cost zero and hence always covers its own unit. More
expensive private routes cover a unit only when the inequality holds.

**Lemma 1 (local exchange).** Consider a projected packing that retains
distinct sources and distinct original units but temporarily ignores relay
capacities. If a relay is overloaded, it carries exactly c_g+1 routes,
uses every source of U_g, and exceeds capacity by one. If one of its used
units is covered, those routes can be replaced with the same number of
payments and the SAME set of original units, using only c_g relay routes,
without increasing cost.

**Proof.** By (3), an overload must have c_g+1 distinct entrants and uses
all of U_g. Let j be a used covered unit and a its covering entrant.
Let source b currently receive j, and let k be a's assigned unit.
If a=b, simply change its route to the private route to j. Otherwise
assign j privately to a, and assign k to b through g. All other assigned
units, sources and routes stay. This is a transposition of two assignments;
it does not create a new copy of either unit. The common-output hypothesis
ensures b can use k. One route leaves the module, meeting its capacity.

The old cost across these two entrants is e_g(a)+e_g(b)+o_g(j)+o_g(k).
The new cost is d_a(j)+e_g(b)+o_g(k), no greater by (4). For a=b the
same inequality applies without a swap. The private route cannot collide
with another source's route or another relay by the ownership hypotheses.
QED.

For c_g=1 this repairs the two-source collision. The covering source may
differ between units. Requiring a single source to cover ALL R_g is
unnecessary. Preserving each source's initially assigned resource is also
unnecessary; preserving the distinct original unit set suffices.

## 3. Arbitrarily many modules: exact matching reduction

Form the weighted source-resource projection. Source a can use j in Q
privately at cost d_a(j), or via any g with a in U_g and j in R_g at
cost (2). Keep parallel route labels, or select the least-cost available
label for each source-resource edge. A projected matching uses different
sources and original units. It temporarily ignores all relay capacities.
Let nu be its maximum cardinality, and let C_proj be the minimum cost at nu.

**Theorem 2 (safe capacity removal).** If every relay satisfies

    |U_g| <= c_g, or |E_g(Q)| <= c_g,                     (6)

then the original module system has maximum payment nu and minimum cost
C_proj. Every projected matching can be lifted preserving its payment
count and its used original unit set, with no greater cost.

**Proof.** A module with at most c_g entrants cannot overload. Otherwise
an overload uses c_g+1 different available output units. Under (6), not
all can belong to E_g(Q), so Lemma 1 repairs it. Its overload source set
is exactly U_g. Two overloaded modules cannot share a selected source:
that source has only one selected route label. Repair changes only the
routes of that module's selected sources, preserves all their resources,
and introduces only a private route. It cannot increase another module's
load, alter its entrants, or create any new resource collision. Each step
removes one overloaded module. Finiteness gives a legal packing with the
same count and no greater cost.

Every legal packing projects to a matching, so its value is at most nu.
Lifting a maximum matching gives value nu. Apply the same argument to a
minimum-cost maximum projected matching: the legal optimum costs at least
C_proj because the projection is a relaxation, while the lift costs at
most C_proj. Equality follows. QED.

Thus unit-capacity relays with at most two entrants are safe if there is
at most ONE uncovered available unit per relay. Capacity-two relays with
at most three entrants are safe if there are at most TWO uncovered units.
The output eligibility and cost conditions in Section 1 still apply.

With (6), full compensation is equivalent to a single finite Hall condition:

    |X| <= |N_Q(X)| for every X subset A,                 (7)

where N_Q(X) is the union of private units of X and outputs of every
relay having at least one entrant in X, intersected with Q. All unions
use original identities. In particular shared support is not counted once
per witness owner. Minimum actual route cost is then a weighted matching
problem on that same graph, not independent per-source choices.

## 4. When some modules are unsafe: a joint defect, not one loss per module

Fix ANY projected matching P. Repair every overloaded module with a covered
used unit by Lemma 1. If an overloaded module's c_g+1 assigned units all lie
in E_g(Q), delete one of its routes instead. Individual route costs are
nonnegative, so this also does not increase cost. Let b(P) count these
deletions. Then the original module system has an explicit packing with

    payment = |P|-b(P), cost <= cost(P).                  (8)

No other original unit is reassigned by a deletion. Module repairs retain
their complete unit sets. Consequently this procedure never spends the
same original resource, source or private owner twice.

**Corollary 3 (a matching-specific exactness test).** If a minimum-cost
maximum projected matching has b(P)=0, its lift is an optimum for value and
cost, even when some modules violate (6). Thus (6) is sufficient for ALL
projected matchings, not a necessary condition for exactness of a given
instance.

For a matching-independent bound, call g potentially bad when

    |U_g|=c_g+1 and |E_g(Q)|>=c_g+1.

Define kappa(Q) as the maximum number of relays in a family F satisfying:

1. their full entrant sets U_g are pairwise disjoint;
2. for each g in F one can choose c_g+1 different units of E_g(Q), with
   all chosen units different ACROSS the entire family.

This is a joint packing constraint on original source and resource IDs.
For unit-capacity relays, entrant sets are pairs and the resource demand is
two units per selected pair. One can check a proposed source-disjoint
family's resource constraint by a single bipartite matching with c_g+1
slots per module. Those slots do not create payment resources; they test
whether that many DIFFERENT original unit identities exist.

**Theorem 4 (unified compensation inequality).** For the complete model,

    V >= nu-kappa(Q),
    |A|-V <= max_(X subset A)(|X|-|N_Q(X)|)+kappa(Q).      (9)

For every maximum projected matching, b(P)<=kappa(Q). Hence (8) is at
least as strong as the first bound for that matching, and may be stronger.

**Proof.** Every deleted module uses all its c_g+1 different entrants in P,
and c_g+1 different original units from E_g(Q). These entrant sets are
disjoint because P assigns one route per source. The used unit sets are
disjoint because P is a resource matching. Thus the deleted family, with
its actual used units, is feasible in the definition of kappa. Equation
(8) gives V>=nu-b(P)>=nu-kappa. The finite matching deficiency identity
nu=|A|-max_X(|X|-|N_Q(X)|) then gives the second bound.

For completeness, the deficiency identity follows from ordinary finite
bipartite matching: any matching misses at least |X|-|N_Q(X)| sources of
X. Conversely, starting from unmatched sources of a maximum matching,
follow alternating paths; the reachable source set X has every reachable
unit matched back into X, or an augmenting path would exist. Their count
difference is exactly the number of unmatched sources. This proves both
directions without treating local supports as independent supplies. QED.

Coarser usable upper bounds on kappa are the number of potentially bad
modules; the largest family of disjoint full entrant sets; and

    floor(|union_(potentially bad g) E_g(Q)| / d_min),     (10)

where d_min=min(c_g+1) in that family of potentially bad modules. Use the
MINIMUM of these bounds, not their sum. Computing kappa also enforces
the resource matching constraint, which can be stronger.

A feasible family for kappa provides a projected matching of
sum_(g in F)(c_g+1) sources, so this sum is at most nu. For unit capacities,
2*kappa<=nu and therefore V>=ceil(nu/2). For uniform capacity two,
3*kappa<=nu and V>=ceil(2*nu/3). These are projection-relative bounds for
this specified module class; they are not numerical grid-coloring bounds.

## 5. Physical adapter and the existing frozen witness

Consider a beta-free original aligned-band strand system. Keep complete
whole supports, actual TP--BP links, and original unmarked interval IDs.
Let H be horizontal-actual-BP mixed owners from the forest theorem.
Require every alpha-reachable mixed owner outside H to have incoming
nonself links ONLY from original alpha tips. In particular no reachable
vertical-BP owner is fed by an H tree or by another vertical owner.

By the H forest theorem each reachable H tree has a single external
entrance and no other incoming link. A tree rooted at an alpha belongs
to that source's private region. A tree rooted at a vertical mixed owner
belongs to that owner's relay module. Include the vertical owner itself
in the module. Different such regions have different original owners.
No relay region can feed another relay under the stated incoming-link
condition, so these regions form a complete one-stage route model.

For a source, define d_a(j) as the least actual link count to a supporting
owner in its private region, including cost zero for its own support.
For a relay g, define o_g(j) as the least link count from g to a supporting
owner in its region. Its entrance from an original alpha costs one,
independently of j. Each original mixed root has one BP and at most two
horizontal TP predecessors, so |U_g|<=2. Its whole module has capacity one.
One selected paying route per module can use its minimum internal witness
without a second route colliding inside it. Source-private regions are
also used by at most one route per source. This proves all model hypotheses,
including separable costs and the private ownership needed by Lemma 1.
Original interval sharing is retained in the global resource matching.
Original self-cycles and unreachable mixed owners add no payment routes.
The whole-support normal form gives equality with physical payment/cost.

This adapter allows long bent mixed owners and branching H trees; it does
not assume they are one-M-edge strands. It does require a single layer
of vertical mixed roots. Two immediate predecessors of a root do not
imply two possible ORIGINAL source entrants in a multilayer network.

On the earlier 56P/26T board the only shared relay is G. Its S outputs
cost 0 internally and its Y tail outputs cost 4; entry costs one. Source
A directly supports all S, so S is covered. The three Y units have no
source-private bypass. Thus

    E_G(Q)=Q intersection Y.

The private H of source B is genuinely disjoint from the relay module;
its three X outputs have private cost one. Consequently if Q opens at
most one Y unit, all relay capacities can be removed and a weighted
source-resource matching is EXACT. Across the 243 threshold patterns in
the previous note, 162 satisfy this new uniform condition. Only one of
the 243 patterns has a cardinality gap between projection and the full
original flow: two Y units with no available private resource.

For q disjoint frozen copies with only the Y pools available, nu=2q,
kappa=q and V=q, at cost 5q. This attains (9). These are explicitly
restricted original pools; the complete original pool pays 2q at cost zero.
For each copy with one S unit and one Y unit available, (6) holds and
both sources pay, with cost 5 per copy. With the full pool a minimum-cost
projection already uses only direct routes, so b(P)=0 even though Y has
three units and the uniform condition is not satisfied.

## 6. Conditions that cannot be silently omitted

Three independently checked abstract controls locate the limits:

- **Too many entrants.** One capacity-one gate with three entrants and
  three outputs, all outputs directly supported by just the first source,
  has projected value 3 but actual value 2. Covered outputs alone do not
  help a covering source already assigned to a different route. Condition
  (3) ensures every covering entrant is in an overloaded module's group.
- **Nonseparable costs.** Two sources and units j,k have gate costs
  (11,1) for A and (1,11) for B. A has a direct route to j costing 1.
  Only k is uncovered by the pointwise cost test. Projection uses A->k,
  B->j for cost 2, but the gate-capacity-one optimum paying both costs 12.
  The transposition's unchanged-entry/output cost sum fails. A common
  original mixed root supplies the separability needed by our adapter.
- **A shared purported private bypass.** Two modules have four distinct
  source entrants in two disjoint pairs and four distinct output units.
  Each module's outputs have a bypass at its first source, but both
  bypasses pass through the SAME extra capacity-one owner. Treating them
  as private gives projected value 4; keeping that owner's capacity gives
  actual value 3. This is reuse of a hidden capacity across components,
  despite all resource IDs being different. Such an owner must remain a
  shared gate, and is outside the private-region hypothesis.

These are controls of the stated abstract rules; no new frozen embedding
of these three failure cases is asserted. Source-overlap and resource-
overlap controls also show why two potentially bad relays can have joint
defect only one. A capacity-two control with three entrants is safe with
two uncovered units, and fails to lift three payments when all three units
are uncovered. Applying this abstract case to an actual capacity-two tile
requires its common outputs and internal path capacities to be proved.

## 7. Verification and next mathematical question

The standard-library-only verifier compares weighted projected matching,
full capacitated flow and explicit repairs. Independent route enumeration
checks small models. It checks the source/resource coupling in kappa and
all named assumption countercontrols. The final receipt records 620 models:
451 satisfy the uniform safe condition, and 609 minimum-cost projected
optima lift without loss. There are 8 strict value gaps and 3 cost gaps
at equal value. Independent enumeration covers 43 models and 7,104 named
route packings. Nineteen models give a joint correction strictly smaller
than the number of potentially bad modules. The 243 physical original-pool
patterns are compared to the COMPLETE original fork verifier, and 12 copy-
pool controls use q=2,3,5 fully frozen copies with original unit identities.
The general theorem and all-q argument are proofs, not enumeration claims.

The [Lean module](../formal/SubQuorum/MultiSourceRelayBypass.lean) formalizes
the arbitrary-resource two-route transposition and cost inequality, the
one-uncovered-unit implication, disjoint overloaded source sets, finite
normalization under its stated progress/cost/payment hypotheses, and the
deficiency/projection arithmetic including capacity two. The full finite
matching adapter, joint-rank extraction, higher-capacity exchange and
physical region decomposition remain written proofs plus independent Python
checks. It is not an end-to-end formalization of Theorems 2/4 or the grid
conjecture. The [formal receipt](../output/multisource-relay-bypass-formal-validation.json)
and [computational receipt](../output/multisource-relay-bypass-validation.json)
separate those scopes. No new Oracle review is claimed.

Reproduce the computational checks:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 develop/check_multisource_relay_bypass.py \
  --output output/multisource-relay-bypass-validation.json
```

The unresolved geometric question is now more precise: after exact H
compression, can the remaining vertical layers be reduced to one-stage
modules with bounded uncovered original outputs, or can a shared bypass
force a larger coupled obstruction? Source-private ownership must be
checked before using it as compensation. Another useful branch is to
test actual capacity-two tile interfaces against the common-output and
three-entrant hypotheses, preserving their occupied neighboring bands.
The submitted manuscript, public main/PR3 and existing correspondence
direction are unchanged.
