# Full mixed/beta routing and size-two activation fees by one weighted matching

26 October 2026. Wenlin Zhang and Haobo Ma. Independent research continuation.

We remove the exponential sharing-pivot parameter from the preceding
[positive-extreme optimizer](POSITIVE_EXTREMES_AND_SHARED_FEES.md). On **every
passing uniform V→H P-free input of capacities zero, one and two**, one
ordinary maximum-weight matching now optimizes maximum payment, minimum
actual opening fee and minimum physical links, with arbitrary competing
mixed relays and beta forks. The construction has polynomial size and
integer weights of polynomial bit length.

The key is to encode the full routing network, not just source-to-resource
reachability. Every mixed capacity-one gate and every separate beta BP
entry becomes a two-port switch. A dominant weight forces all switch ports
to be matched: an unused switch matches internally, and a used switch has
one actual incoming link and one actual outgoing link or output. Thus matching
conservation retains the full routing capacities. An edge joining the two
slots of a fee group records a saved fee when neither slot is used.

This also gives a stronger generic theorem: a fixed full mixed/beta network
with independently available disjoint optional groups of one or two original
interval outputs, nonnegative per-access fees and one activation fee per
used group has an exact polynomial weighted-matching realization. The earlier
[dual resource parity formula](MIXED_RESOURCE_DUAL_PARITY.md) remains valid;
its rank-oracle-only limitation does not apply when this explicit routing
graph is supplied. We use standard maximum-weight matching, not a new blossom
algorithm or a claim about arbitrary oracle matroids.

The theorem remains a result for a proved physical adapter class. It does
not establish that arbitrary grid inputs pass the handoff test, repair lost
supports, allow mixed target directions, or improve the universal 5/6 bound.

## 1. Generic full-routing problem

Fix original owners, terminal types, actual TP→BP links and the original
interval inventory Q in the full fork model. The owner classes are:

* Alpha: two TP terminals; at most one paid source path starts at the owner.
* Mixed: one BP and one TP; at most one path traverses its capacity-one gate.
* Beta: two distinct BP terminals; at most one path uses each BP entry,
  and at most two paths enter the owner in total. The owner has one private
  whole-beta output. It has no outgoing terminal links.

A normalized pack consists of disjoint original-owner primitives, ordinary
interval paths and beta forks, as in the existing full-support theorem. Each
beta uses its private whole-beta output first, and consequently witnesses
at most one interval. Every actual interval is a capacity-one output.

Allow fixed free supports W_0(o)⊆Q and a list of extra access offers e,
with owner o(e), interval j(e), and nonnegative integer linear fee a_e.
Parallel offers may be replaced by the cheapest one between the same ports;
their chosen original labels are retained for reconstruction. Free fixed
support is a fee-zero alternative. No paid source-to-resource reachability
projection is used.

Choose disjoint groups G_i⊆Q of size one or two. Every group interval has
**no fixed free support**; its accesses are declared extra offers. Using any
interval of group i costs an activation fee c_i≥0 once, whether one or two
of its intervals are used. Ungrouped optional offers are allowed. For a
normalized pack P and chosen access offers E(P), the exact objective fee is

    f(P) = sum_(e∈E(P)) a_e
           + sum_(i: P uses an interval of G_i) c_i.             (1)

Every private whole-beta output is ungrouped and always free. Grouping a
private beta output, giving negative access fees, or changing terminal/mixed
capacities is outside this theorem. Access and activation fees are part of
the optimization model, not new physical resource counts.

A specified source set D⊆alpha can optionally be required. We optimize
lexicographically: satisfy all D if possible, then maximum paid sources,
minimum f, and minimum actual links. Infeasible D is reported explicitly.

## 2. The matching graph

Construct an undirected graph with these vertices:

1. One source vertex s_a per alpha owner a.
2. Two switch vertices m⁻,m⁺ per mixed owner m, with an internal edge m⁻m⁺.
3. For each actual BP terminal t of beta b, two vertices t⁻,t⁺ with internal
   edge t⁻t⁺. The two BP switches are separate, even when all other supports
   of their beta are the same.
4. One output vertex r_j for each original interval j∈Q and one private
   output vertex z_b per beta b.
5. For a singleton group, one dummy vertex d_i with no access edges.

An alpha has exit s_a, a mixed owner exit m⁺, and a beta has its two exits
t⁺, one per BP tip. Add these external edges:

* For each actual terminal link p→q between different owners, join the
  alpha/mixed exit of owner(p) to the mixed entry owner(q)⁻ or to the exact
  beta BP entry q⁻. Tag the edge by that original physical link.
* For every fixed support or extra offer o→j, join each exit of o to r_j.
  Beta support is accessible from either of its two exits, without identifying
  the two incoming BP capacities.
* Join each beta exit t⁺ to its one private output z_b.
* For each two-unit group add r_j r_k; for a singleton add r_j d_i.
  This is an **idle edge**, not a route or an extra resource. Its saving is
  c_i and it is available precisely when neither real output is route-used.

Source/output vertices are optional. Every switch vertex is designated an
internal port which the optimum must cover. The large weights in Section 3
force this property without asking a separate matching-feasibility solver.
The graph has O(alpha+mixed+beta+|Q|+groups) vertices and polynomially many
edges: at most a constant number per actual link or owner-output access.
A beta access adds two edges, not an unbounded-capacity hub.

## 3. Exact integer priorities

Let H=alpha+mixed, K=H+1, C=sum_i c_i and A=sum_e a_e. Let

    Delta = K(C+A)+H,
    J = Delta+1,
    R = J·alpha+Delta+1,
    T = R·|D|+J·alpha+Delta+1.                                  (2)

Every edge receives T for each internal-port endpoint, J for each alpha
source endpoint, and another R if that source belongs to D. Give it in
addition:

    internal edge or private beta access:   0;
    actual terminal-link edge:            −1;
    interval-access edge for offer e:      −K a_e;
    fixed free support edge:               0;
    idle edge of group i:                 +K c_i.               (3)

For parallel graph edges keep the largest weight and one exact original
label achieving it. Their source/port endpoints, hence all priority terms,
are identical. No future dependency is hidden in an edge label: generic
activation groups are determined solely by the output slot used.

**Lemma 1 (priority saturation).** Every maximum-weight matching covers all
internal ports. Subject to that it maximizes the number of matched sources
in D; subject to that it maximizes total matched sources.

**Proof.** Ignoring source and port bonuses, an arbitrary matching has
score between −KA−H and KC. Indeed an offer can be used at most once per
output edge; a beta's two copies of one offer share its same r_j, so cannot
both be matched. Thus the total access fee is at most A. Every actual link
leaves an alpha or mixed exit, and each such exit is matched at most once,
so at most H terminal links can be selected even before conservation holds.
Idle edges have total saving at most C. The complete lower score range
therefore has length at most Delta.

All internal edges together give a matching covering every port; idle edges
can simultaneously be included since they use disjoint output vertices.
Losing one covered port loses T, greater than the entire possible remaining
score range R|D|+J alpha+Delta. Thus a maximum-weight matching cannot leave
any port uncovered. Once port coverage is fixed, R exceeds the entire range
J alpha+Delta, so the number of matched required sources has priority. Then
J>Delta makes total matched sources the next priority. These are strict
integer inequalities, not floating-point perturbations. ∎

Weights can be large in magnitude, but (2) uses sums and products of input
fees and polynomial counts. Their bit lengths are polynomial in the binary
input size. All arithmetic in the implementation and chosen blossom routine
is integer arithmetic.

## 4. Full-port matching to real routes

**Lemma 2 (switch conservation).** A fully covered internal pair is either
matched internally, with no incident route, or its entry port is matched to
one incoming actual link and its exit port to one outgoing link/access.

**Proof.** The only edge between the pair is its internal edge. Entry ports
have external neighbours only at actual predecessor exits; exit ports have
external neighbours only at actual successor entries or outputs. If the
internal edge is absent, full coverage forces both external matches.
Matching degree one gives exactly one of each. ∎

Interpret external edges in their declared direction and each externally
used internal pair as a directed entry-to-exit step. Every active switch
now has one incoming and one outgoing step. Alpha source vertices have at
most one outgoing step and no incoming step. Interval/private beta outputs
have at most one incoming route step and no outgoing step. An idle edge is
kept separate: neither of its vertices can simultaneously have a route step.
Thus active routing decomposes into source-to-output directed paths and
source-free directed cycles.

**Lemma 3 (no cycles in an optimum).** A maximum-weight matching has no
active source-free directed cycle.

**Proof.** Replace the external matches of such a cycle by the internal
edge of every switch on the cycle. All internal ports remain covered;
no source, resource output, group idle edge or access offer is changed.
A directed cycle must use an actual terminal link: entry-to-exit steps
alone cannot reach another switch, and outputs terminate routes. At least
one negative unit link cost is removed. Therefore this replacement strictly
increases matching weight, contradiction. ∎

The resulting paths preserve mixed capacity one and each separate beta BP
entry capacity one. A beta has two switches and no outgoing terminal link,
so at most two paths terminate there, with different actual BP entries.
Interval outputs are unique. These are exactly the full fork-flow capacities;
no two independent source paths are allowed to consume the same mixed gate.

For any unused group, both real slots, or its singleton slot and dummy, are
unmatched unless the idle edge is already included. Add that edge. It cannot
conflict with any other match because groups are disjoint and no access
uses these outputs. A positive saving edge is already present at an optimum;
a zero-saving edge may safely be added for the exact identity below.

## 5. Beta normalization and the fee identity

A raw routing can use two different supported intervals at one beta without
using its private output. Replace one such interval termination by the
unused private output z_b, using the same beta BP switch. For one beta path,
perform the same change if necessary. Both are valid matching replacements:
z_b is unused, no incoming route or internal switch changes, and releasing
an interval can only permit another idle edge. This removes a nonnegative
access fee and can only remove groups from the used set; it never activates
a new group. Source identities and actual links are unchanged.

**Lemma 4 (optimal normalization).** At a maximum-weight matching this
operation preserves optimum weight and fee and yields a normalized physical
pack. An arbitrary raw matching need only have nonincreasing fee under
normalization.

**Proof.** The replacement leaves all three priority counts unchanged and
cannot decrease the lower score; idle-edge completion can only help. If
it strictly improved the score, the original matching was not maximum.
Hence its score and fee remain equal at the optimum. Every used beta now
has exactly one private whole-beta output and at most one interval, giving
the original normalized beta or fork primitive. Other paths are ordinary
interval primitives. Mixed capacity prevents shared ordinary owners, and
the two beta arms form one primitive, so all normalized owners and actual
resource assignments are valid. ∎

Let N_p be the number of internal ports and let p,d be the total and required
paid-source counts. For a fully covered cycle-free routing with all idle
edges completed, the weight is exactly

    weight = T N_p + J p + R d + K C − K f − ell,                (4)

where f is (1) and ell the number of actual links. A group contributes its
saved fee c_i if neither output is used and zero otherwise, yielding the
constant C minus the once-per-used-group activation sum. This holds when
only one real slot is used and when both are used; a singleton's dummy is
never mistaken for a real output. Access edges contribute their exact
chosen linear fees separately.

Conversely every normalized pack maps to a matching with all ports covered:
use its actual route/access edges, match every unused internal pair by its
internal edge, and add every unused group's idle edge. Original owner,
entry and output capacities give disjoint endpoints. Its weight satisfies
(4), with the same paid sources, access choices and actual links.

## 6. Exact polynomial theorem

**Theorem 5 (one full-routing weighted matching).** In the generic model of
Section 1, one maximum-weight matching, followed by path reconstruction,
idle completion and beta normalization, returns a maximum-payment normalized
pack with minimum actual fee and then minimum actual links. It enforces any
feasible prescribed source set D, or reports that set infeasible.

**Proof.** Lemma 1 supplies full port coverage and maximizes required sources
first. A matching covering all of D exists exactly when a normalized physical
pack covering D exists: one direction follows from Lemmas 2–4, the other
from pack-to-matching construction. Thus a missing required source after
optimization is a genuine infeasibility result.

Conditioning on all required sources, Lemma 1 next maximizes total payment.
Lemmas 2–4 turn its optimum into a valid normalized pack at the same weight.
Conversely every normalized competitor is present in the matching problem.
Equation (4) therefore proves equality of the optimum sets at fixed payment.
Since 0≤ell≤H and integer fees use scale K=H+1, decreasing f by one dominates
all possible link-count changes. Hence the lower score first minimizes fee
and then links. This proves both directions for the full three objectives.

The graph size and weight bit lengths are polynomial. Standard general
maximum-weight matching is polynomial, and route reconstruction is polynomial.
The construction never calls a packing enumerator, a resource-rank oracle,
or a gate/group-subset enumeration algorithm. ∎

This is a self-contained realization of the explicit routing/group problem
by classical weighted matching. It does not assert that a matroid supplied
only through arbitrary rank queries admits the same deterministic algorithm.
The routing graph contains the representation used by the reduction.

**Old source retention.** If D was payable before any optional operation,
any fee-optimal maximum-payment physical activation state contains that old
network. Augmentation preserves all original saturated source arcs, and beta
normalization preserves sources. Thus requiring D costs no additional fee
and does not reduce payment. The third objective is minimum links under
the source restriction; it can differ from the unrestricted link optimum.
For arbitrary feasible D not payable originally, this free-retention claim
need not hold; the algorithm still optimizes correctly under the restriction.

## 7. Physical consequence: remove every 2^h branch

Apply the complete critical-state recognizer and legacy-aware extreme
retraction to an arbitrary passing uniform V→H P-free input of capacities
zero, one and two. These preceding results have general proofs. Retain the
entire original inventory, fixed V supports and full owner/type/link network.
For each retained end offer e with actual prerequisite set D_e:

* Make its linear access fee a_e=sum_(g∈D_e\H_s) w_g, where H_s is the
  preceding theorem's set of positive sharing pivots.
* For each q∈H_s, form one group from its two private extreme original units
  and give the group fee w_q. Both units were initially unsupported.
* Keep every other original output ungrouped and every free old extreme
  access at fee zero.

Distinct q have disjoint original outputs. The physical sharing theorem
states that all other simultaneous positive gate charges are disjoint in
any normalized pack. Residual overlap on a shared single output or at a
coincident owner cannot be simultaneously used, and zero-fee overlap is
harmless. Hence (1) equals the fee of the **actual union** of prerequisite
gate tiles of the chosen normalized offers, charging each q once.

**Corollary 6 (all-capacity uniform physical optimizer).** Every input passing
the preceding all-capacity critical handoff test admits a polynomial exact
optimizer for maximum payment, minimum actual gate opening fee and minimum
links using one weighted matching. The result reconstructs an actual optimal
gate set and a normalized route pack. No restriction on the number h of
sharing pivots is required. Prescribed old paid sources can be retained at
the same first two objectives.

**Proof.** The generic assumptions follow from recognition, common original
IDs, extreme retraction and sharing classification. Theorem 5 gives the
optimum in the proxy with all routing competition retained. Open precisely
the prerequisite union of its used offers. The exact support compiler makes
that pack physically feasible, and sharing classification makes its generic
fee exactly the actual opening fee. Conversely any physical pack retracts
without changing sources/links or increasing fee and yields a generic
competitor. This proves equality of all three objectives. ∎

## 8. Checks, algorithm implementation and limits

The callable generic API is `solve_grouped_access`; the physical API is
`solve_positive_blossom`. Both return the reconstructed normalized paths,
paid sources, exact fee, actual links and graph statistics. The physical
API also returns the actual opened tiles. Rejection by the recognizer concerns
its support contract, not failure of the numerical grid inequality.

The standalone implementation uses NetworkX 3.5 `max_weight_matching`, with
`maxcardinality=False` and exact integer weights. It calls this routine
**once**, letting the priorities (2) define all objectives. NetworkX documents
O(n^3) time and integer-only arithmetic for integer weights. Its blossom and
primal-dual algorithm is standard; we do not claim to have independently
formalized or reimplemented it. Parallel physical arc alternatives are
collapsed only after preserving a maximum-weight original label.

Install this optional research tool and run the independent audit:

    python3 -m venv /tmp/subquorum-blossom-venv
    /tmp/subquorum-blossom-venv/bin/python -m pip install -r develop/requirements-blossom.txt
    /tmp/subquorum-blossom-venv/bin/python develop/check_full_routing_blossom.py --output output/full-routing-blossom-validation.json

Existing validators remain standard-library-only. No shared CI, default
runner, main branch, PR #3, 11 October manuscript or C4 result is modified.

The audit compares one-matching optima against the independent preceding
2^h full-flow algorithm and, separately, all manageable physical gate subsets
with primitive packing. It also checks arbitrary generic one/two-output
activation groups with access fees by enumerating all compatible normalized
packs, including prescribed source subsets. These generic randomized contracts
are not claimed grid embeddings. Specific controls preserve the shared
mixed capacity one, separate beta BP entries, the single whole-beta output,
and exclude dangling source paths and source-free cycles. Forced raw beta
normalization controls exercise cases that maximum matchings may avoid by
tie-breaking.

A completely frozen physical input stacks twelve existing 16×58 modules:
shape 192×58, T1992, M840, all 1680 actual endpoints strictly frozen. It
has 36 actual gates and 12 positive sharing pivots. Each central capacity-two
pivot has fee 5 and each alternative has fee 3. The exact result is payment
48, actual fee 60 and links 24. One matching suffices, compared with 4096
sharing-subset branches in the preceding algorithm. Physical supports and
fork flow are rebuilt at the returned actual gate state. API controls patch
subset enumeration, the old branching solver and packing routines to fail
if called; the one-matching physical optimizer still succeeds.

Six general Lean kernels in `formal/SubQuorum/FullRoutingMatching.lean`
check priority-digit dominance, port saturation from a full-cover baseline,
source priority, the complementary saved-fee identity, beta normalization's
fee monotonicity and integer fee/link lexicographic order. These are general
algebraic statements, not finite enumerations. The graph/path correspondence,
cycle argument, beta matching replacement and blossom correctness have not
been end-to-end formalized; the scoped report records that distinction.
Exact audit counts are in the JSON reports.

The final run compares 116 one-matching optima with the preceding independent
parameterized flow solver, and 114 joint optima with complete gate-subset
enumeration over 2,098 physical/contract states. Generic one/two-output
groups with access fees cover 130 full-routing models, 6,941 compatible
normalized packs including 859 beta-fork occurrences, and 1,200 prescribed
source checks. The physical/contract audit separately checks 816 feasible
source-restricted optima and 208 infeasible source sets. The returned routes
are checked against the original primitive generator on 246 reconstructed
packs, including 13 selected beta forks. There are 11 rebuilt optimal
physical states, 2,660 replayed strict-freeze events, two forced beta-output
normalizations, two empty/no-alpha controls and two API controls disabling
enumeration and the old branch solver. All six Lean kernels are axiom-free
under local Lean 4.33.0, with no warnings, admitted proofs or new axioms.

## 9. Remaining research boundary

For every passing uniform input, the chain from physical recognition through
support compilation and extreme retraction to exact joint optimization is
now polynomial; the previous exponential h parameter is eliminated. This
also supplies a deterministic explicit-network optimizer for the earlier
independent one/two-output mixed-resource parity adapter, even with linear
access fees. It does not invalidate its rank or cut identities.

The main unresolved geometric step remains compensation after a critical
guard fails. Old support can then belong to a different final boundary or
be cut away before its own tile opens. Its loss must be compared with gains
through a single original-resource and shared-routing ledger; independent
component slack cannot be reused. Mixed target directions and universal
coverage likewise remain open. No universal 5/6 improvement follows from
the restricted-class polynomial result alone.

References: J. Edmonds' classical blossom/primal-dual matching framework;
Z. Galil, "Efficient Algorithms for Finding Maximum Matching in Graphs,"
ACM Computing Surveys 18(1), 1986, DOI 10.1145/6462.6502; and
[NetworkX 3.5 maximum-weight matching documentation](https://networkx.org/documentation/3.5/reference/algorithms/generated/networkx.algorithms.matching.max_weight_matching.html).
