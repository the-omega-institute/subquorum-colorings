# Exact pinwheel direction optimization with one credit per beta core

Continuation: [terminal-defect full-pool theorem](TERMINAL_DEFECT_PORT_COMPENSATION.md)
settles the complete original pool on standard-boundary packets whenever
alpha terminals have degree three, without root flips. It also quantifies
degree-four terminal and raw-boundary exceptions and exact port withdrawals.
This does not apply to arbitrarily reserved pools or discard boundary defects.

26 October 2026. Wenlin Zhang and Haobo Ma. Isolated research continuation.
Submitted manuscripts, public main and shared CI are unchanged.

This removes the two-mixed-owner restriction from
[two-track pinwheel switches](PINWHEEL_TWO_TRACK_SWITCHES.md). Arbitrary
selected degree-three pinwheel tiles, including beta owners joining two
roots, admit ONE exact integral min-cost-flow optimization of all direction
choices. Every whole-beta credit is identified with a fixed outside path
fragment and is used once. A stub-supported fork normalization is essential.
We also give an actual frozen duplicate-credit counterexample. It refutes
the duplicated-beta rule, not the numerical grid inequality. General donor
coverage and universal 5/6 remain open.

## 1. Setting and fixed outside cores

Use a feasible pair (T,M) on an even-by-even grid, P=V(M), every endpoint
of occupied degree exactly three, and no nonempty feasible simultaneous
promotion bundle. Initially use uniform horizontal two-row bands, so N
is vertical. Choose ANY collection S of aligned full-P tiles all four
of whose actual mates lie outside the tile. No two-mixed condition is
imposed. The argument rotates for a uniform vertical background.

The established pinwheel lemma gives the two possible actual exit patterns
(NW,NE,SW,SE)=(N,E,W,S) or (W,N,S,E). At each root its two horizontally
matched corners are diagonal. Each corner x and outside mate b=m(x)
form a two-vertex **stub**. The vertical N partner of b is forced blank,
so b is an actual BP terminal. The other two diagonal root corners are
**core ports**. Both legal auxiliary pairings connect each stub to one
core port; changing root direction transposes that two-by-two pairing.

At a root the two forced BPs have the same grid color. An open M/N path
has opposite-colored ends, so the root's two wires have distinct open
owners. They are mixed or beta. Across roots the forced BP identities
are all different. A mixed owner can meet at most one selected root;
a beta can meet at most two, once per actual BP.

Remove every stub from its ORIGINAL owner, retaining the remaining
nonempty path as that owner's **core**. Equivalently delete the selected
root N edges and distinguish the two-vertex stub components from the
remaining components. There are three affected-core types:

| Original owner | Core interfaces | Fixed external ends |
|---|---|---|
| Mixed | one root port | one TP |
| Beta meeting one root | one root port | one BP |
| Beta meeting two roots | two root ports | none |

Unchanged original owners are their own cores. Alpha owners and cycles
never meet a selected root. A beta core joining two roots is ONE path
fragment, even though it has two ports. It gets ONE private whole-beta
unit, not one per port or one per incident root.

For every simultaneous direction choice, each port acquires exactly one
stub. No pairing joins two cores: the root's stub corners are diagonal,
as are its port corners. Thus each new owner is exactly one old core
plus its newly assigned stubs. Mixed cores remain mixed, beta cores remain
beta, and all original alpha, beta and mixed counts are invariant. The
core is a permanent identity for the whole-beta credit even when its
actual BP endpoints change.

## 2. Exact physical links and resource identities

Use the legal even-rectangle partition that isolates each selected root
inside its original two-row band and retains the intervening horizontal
strips. No pinwheel root has a side-adjacent full-P tile: each face has
one actual outside mate and one forced blank. Hence changing other
selected roots does not change any stub BP's outside N partner.

All root corners remain PP, so no actual TP/BP endpoint or external
physical terminal link is created or deleted. Keep the entire common
TP--BP link list, including original self-links, since changing root
pairings may make them nonself. Only actual external links cost one.

Every original BB/TT resource component is separated from a root boundary
by its PP column. The root's adjacent outside columns are PB, so its
corners have no original support. Isolating or flipping the root creates
no unit and splits no old BB/TT component, including balanced boundary
chains. Identify each unit by the actual cells of that component. The
whole pool and ANY chosen available subset are identical in all partitions.

Let W(C) be the support witnessed on core C, and W(s) that witnessed on
stub s, in the original outside bands. For a chosen direction assignment,

    W(new owner of C) = W(C) union union_(s assigned to C) W(s).   (1)

These are unions of original identities. A unit shared by two fragments
still has a single capacity-one resource sink. The complete owner body
and this exact support union, rather than just its cardinality, are
reconstructed in the physical verifier.

## 3. The network and exact joint optimization theorem

Retain the ordinary whole-support network for all unchanged alpha and
mixed owners. Use the following gates for every selected root:

    actual BP b -> stub s, capacity 1;
    root port p -> its fixed core, capacity 1;
    stub s_i -> root port p_j, capacity 1, all i,j in {0,1}.

An affected mixed core exits at its fixed TP, with support W(C). An
affected beta core has one body node, ONE private whole-beta sink edge,
support W(C), and, when applicable, its unchanged external BP entry gate.
An unchanged beta has its usual two BP gates and one private beta sink.
Each stub also has direct support arcs to W(s). Support arcs have capacity
k+1, where k is the number of original alphas. Every available original
interval has ONE global capacity-one sink edge. All new internal arcs
cost zero; each actual TP--BP link costs one.

**Theorem 1.** Maximum whole-support payment over ALL simultaneous choices
of the selected root directions equals the integral maximum-flow value
V of this single network. Minimum physical link count among all such
maximum-payment choices equals the network's minimum cost. An integral
optimum produces actual root directions and a legal ordinary-stem/beta-fork
packing with that payment and cost.

### Physical packing to flow: stub-supported beta forks

First put a fixed-direction physical pack into the established whole-support
stem/fork normal form. A mixed stem through a selected root either pays
from its incoming stub support directly or traverses its fixed core port
and uses a core support or TP output. This respects the selected pairing.

A one-arm beta stem uses its core's private whole-beta unit. For a
two-arm beta fork, one payment uses that unit and the other a single
original interval j. If j is in W(C), both incoming paths traverse their
core entry ports and the usual beta-body flow applies. Otherwise (1)
puts j in a particular assigned stub s. The fork has an incoming path at
EACH of its two actual BPs, including b(s). Let that incoming path end
directly at j from its stub, before the switch; let the other use the
private whole-beta sink. This changes no physical selected link, source
set, payment, cost or resource identity. An interval on an unchanged
external-BP part of the beta belongs to W(C) and needs no special case.

All selected crossing arcs are a subset of the chosen physical pairing.
Owner-disjointness and separate beta BP entries imply all unit capacities.
Thus the network dominates every fixed-direction pack. Omitting stub
support arcs is incorrect: a valid beta fork may have no supported
interval on its core but an eligible interval on an incoming stub.

### Flow to directions: account for direct stub payments too

At each root the integral used stub-to-port arcs form a partial matching
of two inputs and two outputs, by their entry/port capacities. Every such
matching extends to either identity or transposition. Choose its physical
root direction. A stub flow that already paid an interval puts no used
crossing edge into this partial matching; assign it one of the remaining
ports when completing the pairing.

Every occupied port is already in the used matching. Consequently a
direct-paying stub can only be assigned an UNUSED port. Counting these
assigned direct payments together with flows actually traversing a port
gives at most ONE incoming unit per completed physical BP-to-port pairing.

An affected mixed core therefore has at most one incoming unit, counting
direct stub payments and paths continuing through its TP. An affected beta
has at most two incoming units TOTAL: its two completed root ports, or
one completed port and one unchanged external BP entry. The same holds
for unchanged beta owners. This total includes payments that never visited
the beta body in the relaxed flow; the body's inflow alone is insufficient.

Now group paths by the actual beta owner determined by its fixed core.
If r>0 incoming units are present, r is one or two. There is at most one
network use of its private beta unit. All other outputs, including direct
stub payments, use different available original intervals in that owner's
support. If no unit used its private beta sink, redirect one of these
interval payments to that private unit. This releases the old interval,
uses no new interval, and changes no actual link or source. The resulting
group is a beta stem for r=1 or a beta fork for r=2, with exactly one
whole-beta unit and at most one original interval. In the latter case
an interval necessarily exists: two payments cannot have used the single
private unit alone. Perform this independently for each fixed beta core.

Global resource sink capacities keep every retained interval different.
Root-port completion prevents two mixed paths occupying one owner.
Every forward directed cycle contains a positive-cost external link,
so minimum cost removes circulations; a selected link made self by the
chosen pairing would close such a cycle and cannot occur. Thus all
remaining paths give a legal physical terminal matching and normal-form
pack, with the flow's payment and exactly its external link cost. This
proves equality in both directions. QED.

Normalization may RELEASE a used original interval. The theorem preserves
the available pool, payment, selected links and sources; it does not promise
to preserve an arbitrary prescribed set of used interval identities.

The network has four crossing arcs per root and polynomial size. It
optimizes payment and then link count, not the number of flipped roots.

## 4. Exact unified cuts and the one-unit-per-flip gain ceiling

Let G contain every unit gate except alpha source arcs: stub BP entries,
root crossings and port gates, ordinary mixed gates, unchanged beta BP
entries, ONE private sink per beta core, and available original interval
sinks. For Z subset G delete these gates, and let U_Z be the original
alpha sources from which no sink path remains. Standard max-flow/min-cut,
now combined with the physical equivalence above, gives the EXACT identity

    k - max_(root directions) payment = max_Z (|U_Z| - |Z|).       (2)

For clarity, a packing pays at most |Z| blocked sources through these
different unit gates, giving the lower deficit bound. Conversely a minimum
cut has capacity at most k and crosses no k+1 support/link arc. Let H be
its source-side alphas and Z its other crossing gates. Then H subset U_Z,
the cut has capacity k-|H|+|Z|, and the preceding bound forces equality.
Each beta core or shared original interval in Z occurs ONCE. This is
the familiar separator theorem applied to the new exact direction model,
not a new abstract max-flow theorem or a proof that all physical cuts pass.

The previous sharp gain bound also extends unchanged:

    V0 <= max_(root directions) payment <= V0 + |S|.              (3)

Indeed, represent the original direction with only diagonal root crossing
arcs. Starting from any minimum cut, adding two off-diagonals at a root
adds at most one unless both cross. In the latter case the two old diagonals
already cross, contributing two; move both stub nodes far, replacing them
by at most two incoming entry gates. All stub resource arcs are outgoing
and can only lose cut contribution. Fixed beta cores do not move, so the
same correction is valid when their ports lie at different roots. Corrections
at distinct roots are disjoint. This proves (3), and reversing any specified
s flips gives absolute payment change at most s. The prior all-q two-mixed
physical family already attains this bound on a restricted original pool.

## 5. Actual frozen obstruction to duplicated beta credit

The permanent [30-by-70 fixture](../develop/fixtures/pinwheel_beta_bridge_duplicate_credit.json)
is the transpose of the existing two-module rotor chain. It has 322 P,
161 actual matching edges, 86 selected vertices, all occupied endpoint
degrees exactly three, and an independently checked 89-wave strict-rank
certificate covering every endpoint. It has selected roots at
(row14,col14) and (row14,col54), zero-based.

There are four original alpha owners and ONE beta core joining those two
roots. Originally its BP endpoints are (14,16) and (14,53). Make no
original interval available. The exact direction-optimized payment is
one, minimum links three. In fact the unified separator is precisely
the one private whole-beta-core sink: deleting it blocks all four sources,
giving deficit 4-1=3 in (2). Every one of the four root direction choices
still has payment one. The beta's two entry ports do not give two private
whole-beta units.

An intentionally incorrect model giving that same beta core two private
units reports payment two at six links. One returned physical direction
flips the first root only, making the beta's actual BPs (15,13) and
(14,53). Its selected links are

    (15,8)->(15,9), (15,10)->(15,11), (15,12)->(15,13),
    (14,48)->(14,49), (14,50)->(14,51), (14,52)->(14,53).

These are six distinct legitimate physical terminal links. Their actual
cancellation/payment is ONE, not two. Independently enumerating all
64 subsets of this six-link set gives optimum payment one and minimum
links three. Thus the failure is an exact accounting error even when the
proposed physical links and directions themselves are valid. The saved
fixture and verifier reproduce the counterexample without a search solver.

This uses an empty available ORIGINAL INTERVAL pool, leaving the one whole
beta credit. The complete original interval pool pays all four sources
with zero links. It is not a full-pool compensation counterexample, and
does not refute the grid target. Longer transposed chain controls test
the same repeated-credit mechanism, without claiming a new all-q physical
deficit formula from enumeration alone.

## 6. Reproduction and formal scope

Run:

    python3 develop/check_pinwheel_beta_core_switches.py --output output/pinwheel-beta-core-switches-validation.json

The checker compares the core flow to EVERY tested physical direction
assignment, reconstructs exact core-plus-stub owner bodies and supports,
preserves original resource cell identities and physical terminal links,
and lifts selected links to the returned directions. It separately deletes
the returned unit separator and recomputes blocked alpha sources. Abstract
systems test shared original units, multiple beta cores, direct stub
payments and existing forks, without claiming new physical realizations.
Finite checks test the complete proofs above rather than replace them.

The passing controls cover 16 physical models, 25 selected roots, six beta
core occurrences with two root ports and nine with one root port. There
are 62 actual direction assignments, 102 joint resource-pool comparisons,
2,890 independent strict-rank events and 3,648 independently enumerated
terminal matchings, including the 64-link-subset duplicate-credit check.
Twelve tested available-pool cases retain positive deficit even after
joint direction optimization. A further 360 abstract core systems pass
1,680 independent fixed-orientation comparisons. An explicit stub-only
fork control pays two with the correct stub arcs and only one if those
arcs are wrongly omitted.

The companion [Lean source](../formal/SubQuorum/PinwheelBetaCoreSwitches.lean)
checks completed port occupancy INCLUDING direct stub payments, the total
two-entry beta bound, and the interval needed for a second payment and
normalization. Prior finite pinwheel and cut-repair declarations remain
in [the two-track source](../formal/SubQuorum/PinwheelTwoTrackSwitches.lean).
Arbitrary-grid geometry, general flow equivalence/normal-form assembly
and the physical 322-endpoint certificate remain written proofs plus
executable controls, not an end-to-end Lean formalization.

The remaining geometric problem is to establish sufficient JOINT unused
credit on complete physical cuts, including degree-four/repeated-owner
tiles, capacity-one configurations and general occupied-band interfaces.
The theorem now solves joint direction choice for all exact-degree-three
four-outward roots; it does not establish universal donor coverage or
improve 5/6 by itself. No manuscript or email changes were made.
