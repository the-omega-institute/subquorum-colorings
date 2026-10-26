# Positive pivots: extreme reassignment and the exact shared-fee core

26 October 2026. Wenlin Zhang and Haobo Ma. Independent research continuation.

We settle the next question left by [positive-capacity handoff recognition](POSITIVE_CAPACITY_HANDOFFS.md).
On **every passing uniform V→H P-free input of capacities zero, one and two**,
all normalized packs retract simultaneously to the first and last original
unit of each final H gap. This remains true when positive tiles retain old
V-phase support. It preserves paid sources, whole-owner primitives and actual
links, not only the scalar optimum.

We then classify all possible simultaneous positive-fee sharing after that
retraction. It can occur only when a final H gap has exactly two original
units, both supplied by the same capacity-two gate, both initially unsupported,
with two distinct boundary owners. Only that containing gate can have a
shared fee. All other prefix and suffix fees become additive on normalized
packs; a one-unit gap stays one capacity-one output.

If h such containing gates have positive fee, the full joint objective
(maximum payment, minimum actual gate fee, minimum links) is solved by at most
**2^h integral min-cost maximum fork flows**, after polynomial recognition
and compilation. No subset of the remaining gates is enumerated. In particular,
h=0 gives one polynomial flow, including *every passing capacity-one input*
and many capacity-two inputs. General h is an exact fixed-parameter algorithm,
not a polynomial-time claim in the unrestricted input size.

This advances the exact compensation-selection model and isolates its
remaining fee interaction. It does not repair failed handoffs, allow mixed
opening directions, or improve the universal 5/6 grid bound.

## 1. Exact physical contract inherited from recognition

Fix a feasible even rectangular grid, T, actual matching M, endpoint set P,
canonical maximal direction bands and the full restored original-owner network.
Select aligned P-free tiles, initially V, opening uniformly to H, with
nonnegative integer actual opening fees w_g. Use common original interval IDs:
fixed positive fine anchors outside gates and a fixed local pairing inside
positive gates. Retain mixed capacity one, distinct beta BP entries and the
single private whole-beta output. No freezing or selection-maximality
assumption is required for the general theorem.

Require the preceding theorem's complete critical guards to pass. They are
necessary and sufficient for original support monotonicity in every ordered
state pair and take at most 2+2p snapshots for p positive gates. In particular:

* Every fixed V unit has constant support.
* A local unit of g has constant original support while g is closed.
* Every local original incidence survives at the singleton-open state {g}.
* Once a local tile is open, support is exactly its H-gap connectivity.

In the full-open state, each H no-P gap C has a left owner L and right owner
R, possibly absent or equal, ordered original unit IDs u_0,...,u_(m−1), and
a linearly ordered set of its actual gate tiles. Different gaps have disjoint
unit and gate sets. A gate contributes precisely its capacity κ(g) units to
that gap, κ(g)∈{0,1,2}. A fixed H tile can also contribute units.

Let B(o,j) mean original support in the all-closed state. Let A_L(j) consist
of all variable tiles from the left boundary to the unit's final H anchor,
**including the containing tile if it is variable**; similarly A_R(j).
The exact full support in state F is

    W_F(o) contains j iff
       B(o,j), or [o=L and A_L(j)⊆F], or [o=R and A_R(j)⊆F].       (1)

For a fixed V unit only the constant original part applies. A coincident
boundary owner uses the OR of its two end alternatives. Every old incidence
of a final H unit belongs to a boundary owner: it survives at full opening,
where those are the only owners of the gap. Original IDs, raw inventory,
alpha and beta remain fixed throughout.

Every normalized full-support pack uses at most one interval witnessed by
a particular owner, including a beta: its fork uses one interval and its
private whole-beta output. Owners can be boundaries of many gaps and can
compete in the same external routing network.

## 2. The missing legacy-support argument

**Lemma 1 (legacy access reaches an extreme).** If L≠R and L supports any
unit of C in state F, then L supports u_0 in that same state. Symmetrically,
R supports u_(m−1). If L=R, support of any unit implies support of at least
one of the two extrema.

**Proof, H access.** A left H route to any unit opens every gate on the
shorter prefix to u_0. A right H route similarly reaches u_(m−1).

**Proof, old incidence on a fixed H unit.** That old incidence already
comes from a zero-activation H route at one end. The same shorter-prefix
or shorter-suffix argument applies in the original state and hence in F.

**Proof, old incidence on a g-local unit j.** Its owner o must also support
that unit when only g is open, by the singleton handoff guard. In that
singleton state j is H and can reach only the final gap's boundary owners.
Suppose that access is from the left. Every gate between L and j, other
than g itself, would still be closed and block the route. Hence no other
variable gate lies before g. If u_0 is strictly before g, its entire left
prefix is empty, so L supports it originally and in F. Otherwise u_0 is
another original unit in g. All local units of a P-free tile have identical
support in every state; the old incidence on j therefore also backs u_0,
and support monotonicity preserves it in F.

The right-hand case is identical. When L≠R, an incidence owned by L cannot
use the right end, so it reaches u_0; the R case reaches u_(m−1). When L=R,
the singleton can use either end and the corresponding argument supplies
at least one supported extreme. Absent boundaries cannot support an incidence.
This exhausts (1). ∎

This is why retaining old V support does not introduce an outside owner or
an unprotected interior demand into a passing gap. Without the singleton
handoff, a closed local resource could be owned by an owner outside the final
H boundaries and the statement would not follow.

## 3. Simultaneous original-ID retraction

For m≥2 retain only L→u_0 and R→u_(m−1), with their actual support predicates;
for m=1 retain the one original unit with both end alternatives. For m=0
retain no interval access. Suppress other H-gap supports only in the
optimization proxy; keep every omitted ID in the original raw inventory.
Keep fixed V support and the entire owner/type/link/beta network unchanged.

**Theorem 2 (legacy-aware extreme retraction).** In every gate state, every
normalized physical pack transfers to this proxy with the same paid sources,
owner primitives, value and actual selected links. Consequently maximum
payment, minimum links, and any feasible prescribed paid-source restrictions
are unchanged at that state.

**Proof.** For distinct boundaries, at most one used interval of C has
witness L and at most one has witness R. By Lemma 1 send every L-witnessed
use to u_0 and every R-witnessed use to u_(m−1). For m≥2 the two IDs are
different. A formerly occupied extreme is reassigned as part of the same
simultaneous operation; no interior or opposite-boundary use is left behind
to compete with it. No third owner supports a gap unit. No other gap or
external pool contains those IDs.

For L=R, the owner witnesses at most one interval in the entire normalized
pack. Choose a supported extreme supplied by Lemma 1. For m=1 leave the
shared original output intact; it is used at most once. These cases create
no resource or owner collision. Apply the construction independently in all
gaps. A beta fork keeps its two source arms, one interval and private whole
beta. No actual link or original owner changes. Conversely every proxy
support is actual physical support, so its packs are already physical. ∎

For a retained end offer e=(o,j), set

    D_e = empty                         if B(o,j),
          A_L(j) or A_R(j)              otherwise.               (2)

For distinct ends these are exactly the retained support predicates. With
coincident ends the two offers give their OR; if B(o,j) holds, the empty
choice represents its unconditional legacy access. Thus the proxy itself
can be implemented by optional access arcs with actual prerequisite sets
D_e. An owner can choose either end when they coincide; it still has at
most one normalized interval use. No duplicate output is introduced.

After transferring a pack, open just the union of D_e for the offers it
uses. All its chosen supports remain valid, fixed support is unchanged,
and no routing capacity changes. This operation cannot increase fee. We
do not claim unused physical gates must be closed in every optimum when
they have fee zero; only that an optimum with this union representation exists.

## 4. Complete classification of retained fee overlap

**Theorem 3 (one possible sharing tile per gap).** If the left and right
retained nonempty prerequisite sets intersect, their intersection is exactly
the variable tile q containing both extreme anchors. All the gap's units
then lie in q. In particular:

1. If m=1, both end offers lead to the same capacity-one output and cannot
   be simultaneously used.
2. If m≥2, then m=2, κ(q)=2, and no other positive tile or fixed positive
   unit exists in that gap. Both original units are initially unsupported.
3. If the boundary owners coincide, a normalized pack can use at most one
   of the two end offers.
4. With m=2, distinct existing boundaries, no old local support and w_q>0,
   q is the only gate whose positive fee can be shared by two simultaneous
   retained uses. All other left/right prerequisites are disjoint.

Different gaps never share an actual gate. Therefore (4) lists **all**
possible simultaneous positive-fee overlaps after Theorem 2.

**Proof.** An intersecting gate lies at or before the first unit's containing
tile, to be in the left prefix, and at or after the last unit's containing
tile, to be in the right suffix. Since the first tile is no later than the
last, all three tile positions are equal. All intervening unit anchors are
in that same tile as well. The containing tile contributes at most two
positive fine children, so m≤2. An overlap requires that tile to be variable;
it belongs to both inclusive prerequisites, and no other gate can have the
same position. Thus the intersection consists exactly of q.

When m=2, that tile has capacity two. If either of its local units had an
old owner, both would, since their supports are identical. The owner is a
boundary owner by (1), so at least one retained offer would have been made
empty in (2). There would be no intersection. Thus both local supports
were empty. The shared-output and single-witness exclusions follow from
actual unit capacity and normalized primitives respectively. A zero fee
has no effect on additive cost even if both corresponding gates are opened.
Finally disjoint final gaps have disjoint gate tiles. ∎

Call the gates in case (4) the **sharing pivots**, and let H_s be their set,
h=|H_s|. This is a geometric and fee-dependent certificate computed from the
recognized physical input, not a parameter chosen by arbitrary routing paths.
Each such pivot may still be unused or have only one end used in an optimum;
we claim it is potentially shared, not necessarily used twice.

For one such pivot write l,r for the fees of its remaining left and right
outer prefixes. If the end-use indicators are x,y∈{0,1}, its actual local fee is

    w_q·1[x or y] + l·x + r·y.                                    (3)

Charging each end independently gives (3) plus w_q·1[x and y]. This exact
identity isolates the whole possible duplicate charge. The outer prefixes
can be arbitrarily long; only the containing positive pivot is shared.

**Polynomial corollary.** Passing instances with no sharing pivots have an
additive fee representation on normalized packs. This includes all inputs
whose gates have capacities zero or one, gaps with at least three original
units, and capacity-two-only gaps backed by any old local owner. The conclusion
also holds when any residual overlap is a zero-fee gate, a shared single
output, or one common boundary owner. It does not require independent source
components or an independent mixed/beta baseline.

## 5. Exact optimization by 2^h costed full flows

Enumerate A⊆H_s. In branch A:

* Disallow an end offer if its prerequisite contains a sharing pivot outside A.
* Enable every other end offer e with access-arc fee

      f_e = sum_(g∈D_e\H_s) w_g.

* Add the branch constant c_A=sum_(q∈A) w_q.
* Retain the complete competing fixed network, fixed V supports, every raw
  original output and each private whole-beta output.

Let H be the number of alpha plus mixed owners and K=H+1. Give an offer
access arc cost K f_e and each actual terminal-link arc cost one. All other
arcs cost zero. Compute an integral min-cost maximum fork flow. Compare the
branches lexicographically by (maximum value, minimum c_A+offer fee, minimum
link count). Reconstruct the actual open set from the union of prerequisite
sets of the used offers, discarding any unused positive-fee branch pivot.

**Theorem 4 (exact uniform positive-pivot optimizer).** This algorithm attains
maximum physical payment over all gate choices, then minimum actual opening
fee among those choices, then minimum physical links. It uses at most 2^h
full flows and polynomial preprocessing, and outputs an actual optimal set
of physical gate tiles. With h=0 it is one polynomial min-cost max-flow.

**Physical pack to branch.** Apply Theorem 2 and retain only its used-offer
prerequisite union. Let A be the sharing pivots in that union. Every used
offer is enabled in branch A. Every sharing pivot is paid once by c_A;
by Theorem 3, no other positive gate can be paid twice by simultaneous
normalized uses. Map the normalized pack to the full fork network. Its
branch fee is exactly the actual gate-union fee and its link count is
unchanged.

**Branch flow to physical pack.** Remove any circulations. Every directed
cycle in the forward original network contains a positive-cost actual link,
so a minimum-cost flow needs none. Normalize each used beta to its private
whole-beta output first, releasing at most one interval and introducing no
new interval or link. All offer costs are nonnegative, so this cannot increase
branch cost and preserves all sources. At a min-cost optimum it cannot
strictly reduce cost, or the original flow would not be min-cost. We now
have a normalized pack.

Its selected offers are genuinely physical whenever their prerequisite
union is open. Theorem 3 makes their non-sharing fees additive. The actual
fee is at most c_A plus their access fees: a branch may have paid a pivot
that the resulting pack did not use. Such an unused positive pivot can be
removed by considering the branch with only used pivots, with no loss of
payment or increase of links. Across the globally optimal branch, an actual
fee strictly smaller than the chosen nominal fee would contradict the
physical-pack-to-branch direction. Thus the reconstructed global optimum
has actual fee equal to its nominal fee.

These directions show equality of maximum payment and minimum fee. Every
normalized selected actual link leaves an alpha or mixed TP owner, and
there is at most one such link per such owner. Hence link count is between
0 and H. Integer fees and K=H+1 therefore make the min-cost scalar objective
optimize fee before links exactly. The same two directions, retaining link
counts, give the correct third objective too. The network and offer lists
are polynomial in the explicit grid/model size; only the h certified pivot
bits are enumerated. ∎

For a fixed branch, source priority or ordinary lower bounds can enforce a
prescribed feasible old paid-source set P_0. The state contains the original
zero-activation network after retraction. Starting from its P_0 flow,
augment without unsaturating those source arcs to reach that branch's rank;
then apply normalization and retraction, which preserve paid sources. Every
minimum-fee maximum-payment state therefore admits all P_0 at the same first
two objective values. Minimize links *subject to retaining P_0*; that third
optimum can differ from the unrestricted one. The implementation uses source
priority greater than K times the sum of all gate fees plus H. Its API also
reports infeasible prescribed source sets if they cannot be paid in the
full recognized input.

This is a new proved geometric reduction and exact parameterized optimizer
for the recognized physical class, using standard min-cost flow as a tool.
It is not an unrestricted polynomial shared-charge flow algorithm, a proof
that group-index greedy works, or an application of a generic oracle matroid
parity algorithm.

## 6. Concrete frozen controls and an invalid shortcut

Use the previously verified completely frozen 16×58 bundle board:
T166, M70, 140 strictly frozen endpoints, capacity-two central pivot
q=(2,28), and capacity-one alternatives a=(10,16), b=(10,40).
All three open V→H, and the critical handoff recognizer accepts the input.
In the full-open H gap containing q, the only two units are q's, old support
is empty, and the two boundary alpha owners are distinct. Thus h=1 if w_q>0.
The fixed lower mixed/beta network is retained in the flow.

Maximum payment is four, with minimum links two. Giving each alternative
fee 3 yields

    minimum actual fee = min(w_q, 6).

For w_q=5, the correct state opens only q and pays fee 5. The invalid ordinary
per-end charging rule charges q twice and chooses the two alternatives at
fee 6. The failure is fee optimality, not payment, and is not a counterexample
to the grid bound. The new optimizer returns the correct choice with two
flows. Costs w_q=0,3,5,7 independently check the transition; zero fee gives
h=0 and needs one flow.

Stacking two copies vertically gives a completely frozen 32×58 input,
T332/M140 and 280 strict freeze events, with two sharing pivots. All 64
physical gate states are checked. With both central fees 5 and alternatives
3, the optimum is payment 8, fee 10, links 4; four flows suffice. This is
a physical two-pivot control; independent abstract controls separately test
arbitrary competing beta forks and mixed capacity-one relays across cores.

For the all-length frozen corridor board, add the central positive pivot
to arbitrarily long zero-capacity left and right gate prefixes. With two
central original units h=1; with one central unit h=0 and both end routes
compete for one output. Actual API controls use 34 gate tiles and need only
two and one flow respectively, with all physical-subset and primitive-pack
enumeration routines patched to raise if called. No 2^34 state enumeration
is performed by these calls.

## 7. Verification and formal scope

The standalone validator independently enumerates manageable gate sets,
rebuilds physical support, compares primitive-pack optima before and after
retraction, and compares the algorithm's full three-objective optimum with
all physical gate subsets. Every transferred optimal pack retains exact
owners, source identities and links. Small abstract controls also enumerate
**every compatible normalized pack**, not only optimal ones. All feasible
old source subsets of the small controls are independently checked for the
constrained joint objectives. Randomized abstract instances are contracts
for checking the general reduction; they are not claimed grid embeddings.
Rejected physical inputs receive no optimization conclusion.

The six general Lean kernels in `formal/SubQuorum/PositiveExtremeFees.lean`
cover singleton legacy access excluding earlier cuts, legacy-aware extreme
reachability, localization of overlapping prerequisites, intervening units
in a common tile, the exact local duplicated-fee identity, and absence of
that duplication under exclusive end use. All are axiom-free in local
Lean 4.33.0, without `sorry`, `native_decide`, new axioms or warnings.

The physical legacy geometry, simultaneous whole-pack theorem, complete
capacity-two classification, beta normalization and 2^h optimizer have
general written proofs and independent executable checks. The six Lean
kernels do not constitute an end-to-end formalization of these results.
The runner measures local memory and enumerates actual lean/lake executable
basenames before each executable invocation. No shared CI change is made.
Exact execution counts and permanent control outputs are in the JSON reports.

The completed audit checks 2,762 states before and after retraction, 139 exact
joint optima against all manageable gate choices, 748 rebuilt physical support
equalities and 37 reconstructed optimal physical states. It transfers 13,960
compatible normalized packs exhaustively on small controls, for 16,722 pack
transfers overall, including 1,759 beta-fork transfers; all preserve source,
owner and actual-link identities. There are 663 prescribed-old-source joint
optima, 1,540 replayed strict-freeze events, three API controls disabling
physical-subset/packing enumeration, and one infeasible source-set API control.
The 143 optimizer models include 130 single-flow cases and 13 with positive
sharing pivots, including genuinely competing two/three-core abstract networks
and the two-pivot frozen physical board. Random physical recognition accepts
14 sparse boards for optimization and rejects 26 without applying this theorem.

## 8. Next mathematical question

All-capacity uniform support recognition now has an exact geometric
retraction and a fee optimizer with its only remaining combinatorial
parameter explicitly localized. A substantial next step is to exploit the
fact that a sharing pivot has two private extreme offers at fixed boundary
owners: can all such cores, together with asymmetric outer-prefix costs and
the full competing beta/mixed network, reduce to an explicitly represented
linear or valuated parity problem? The earlier independent output-bundle
parity theorem cannot be invoked without establishing its activation and
cost hypotheses. We leave unrestricted polynomial elimination of 2^h open.

The other main direction is compensation *after* a critical guard fails.
That requires a shared original-resource/cut ledger for losses and gains,
not reuse of the same unused capacity in independent components. Mixed
target directions, arbitrary bent-path coverage and the universal 5/6
improvement remain open. The 11 October manuscript, public main, PR #3,
shared CI, C4 results and correspondence state are preserved.
