# First destinations can be separated; residual reachability need not be

25 October 2026. Authors: Haobo Ma and Wenlin Zhang.

We prove a simultaneous first-destination lemma for the original alpha paths
of a completely frozen configuration. Each alpha can either use an interval,
cancel with a whole beta, or make one link into a mixed strand, with all chosen
destinations different. The proof combines the established missing-port BP
terminal injection with the elementary matching property of two-witness
incidence graphs. It is a geometric application of that property, not a new
general matching theorem or a proof that mixed continuations can all finish.

We also strengthen the previous physical shared-gate obstruction. In a new
fully frozen grid both alpha paths have **no** direct or selected-cap interval
access at either end. Thus maximum direct prepayment is zero, and both sources
survive that preprocessing. Nevertheless they can reach the same mixed strand,
whose exit has two different available interval units. The restricted shared
relay rule pays only one, while the full network pays both via two different
beta strands. This separates first-destination selection from later route
reachability, even after maximum direct prepayment.

## 1. Hypotheses and the two endpoint witnesses

Use a feasible selected set T and actual grid matching M, with every matching
endpoint completely frozen for M. Use a matching-closed aligned two-row packet
J with a blank first column and a last column containing a blank corner, as
in FROZEN_MISSING_PORT_BP_TERMINAL_INJECTION.md. Freezing certificates may use
vertices outside J. The actual PP paths partition their terminal endpoints
into alpha (TP--TP), beta (BP--BP) and mixed (BP--TP) owners. Keep the original
BB--TT interval identities and the existing marked boundary intervals.

Let D be the original alpha owners. Each has two different physical TP tips.
At each tip v choose one witness by this rule:

* If v has an immediately adjacent BB column, choose one such port, and use
  its original interval as the destination of this witness.
* Otherwise use the proved simultaneous injection f of all missing original
  alpha tips into different adjacent BP terminals. The destination is the
  original beta or mixed owner of f(v). Retain the terminal link v--f(v).

In particular the second case uses the original-alpha injection theorem;
we do not extend that theorem to arbitrary mixed TP tips or virtual alphas.
Selected-cap access is not needed for this first-destination lemma.

There are two witness tokens per alpha, even if their destinations coincide.
Every interval receives at most two tokens: a directly accessible port is an
end of that interval, and each end has at most one candidate physical TP tip.
Every beta receives at most two tokens because it has two BP terminals and f
is injective. Every mixed owner receives at most one token because it has
only one BP terminal. These are bounds on chosen tokens, not on all possible
source-to-resource routes. Types are retained so an interval and a strand
can never accidentally be treated as one destination.

For a subset X of alpha owners, let N_I(X), N_beta(X), N_mixed(X) denote its
chosen witness destinations. Counting the 2|X| tokens gives the weighted bound

    2|X| <= 2|N_I(X)| + 2|N_beta(X)| + |N_mixed(X)|.       (1)

Consequently |X| <= |N_I(X)|+|N_beta(X)|+|N_mixed(X)|.
The stronger coefficient-one mixed term in (1) records its single entrance;
it does not give mixed owners half a unit of payment credit.

## 2. Simultaneous first-destination lemma

**Theorem 1.** Under Section 1's hypotheses there is an injective assignment
of every original alpha owner to one of its two chosen witness destinations.
Choose the witnessed direct access or single horizontal link accordingly.
All selected terminal links are jointly legal, different alpha sources use
different beta or mixed owners, and all selected intervals are different.

**Proof.** Form a finite bipartite multigraph with alpha owners on the left,
destinations on the right, and one edge per witness token. Every left vertex
has degree exactly two. Every right vertex has degree at most two, including
edge multiplicity. A finite connected component of maximum degree two is a
path or a cycle, permitting a two-edge cycle of parallel edges. A path cannot
end on the left, since its end has degree one and every left degree is two.
Hence both its ends are on the right; alternating edges starting at one end
match all its left vertices, leaving one right vertex unmatched. In a cycle,
the bipartition makes its length even; alternating edges match every left
and right vertex. Applying this independently in each component gives the
required injection. Equivalently the weaker consequence of (1) is Hall's
condition.

For legality, each selected link starts at a tip of a different original
alpha. Its other endpoint is BP, hence never an alpha tip. Distinct chosen
beta/mixed owners supply distinct BP endpoints. No destination can be another
alpha, so the selected links form disjoint alpha--destination pairs at owner
level; an alpha's unused TP remains free. Selected direct payments have no
link incident to their alpha. Their interval identities are different. Thus
the matching and allocations are simultaneously legal. QED.

Write i for the number assigned to unmarked intervals, b for the number
assigned to beta owners, m for the number assigned to mixed owners, and h
for the number assigned to marked intervals. Then

    |D| = i+b+m+h,
    actual compensation = i+b,
    remaining unpaid alpha strands = m+h.                 (2)

Indeed a beta destination consumes exactly one alpha and one whole beta;
a mixed destination transfers one alpha demand and supplies zero credit.
An unmarked interval pays its untouched alpha. A marked interval is only a
provisional destination, supplies zero permitted credit, and its alpha stays
unpaid. No marked interval is released or silently spent in this construction.
All unused beta and interval resources retain their identities. Formula (2)
accounts for every destination and every residual demand exactly once.

If an assignment can be chosen using only beta and unmarked interval
destinations, it is already a full compensation certificate. The theorem
does not assert that such a restricted assignment always exists.

The theorem supplies a safe first simultaneous step. It does not provide an
iteration invariant: after a mixed transfer a newly exposed TP belongs to an
original mixed path, so the original-alpha missing-port injection need not
apply to it. Reusing Theorem 1 on arbitrary virtual alphas without a new proof
would assume precisely the continuation property still at issue.

## 3. Exact beta compensation when all original alpha tips are unported

There is a stronger conclusion when **both** tips of every original alpha
have no adjacent BB port. Use any injection f from Section 1. Every destination
in its two-witness graph is now a beta or a mixed owner. Let q be the number
of different mixed destinations in this chosen graph. Let t count its path
components with a mixed destination at **both** ends.

**Theorem 2.** Among the terminal links supplied by f, the maximum number of
different alpha owners that can be cancelled against different whole beta
owners is exactly

    |D|-t,             with t <= floor(q/2).                 (3)

Moreover one can simultaneously cancel those |D|-t pairs and transfer each
of the t remaining alpha demands into a different mixed owner, using exactly
one selected link per original alpha. No owner or terminal is reused.

**Proof.** Every alpha has degree two; mixed vertices have degree one. Thus
a cycle contains only alpha and beta vertices, in equal numbers. Alternating
edges pair every alpha to a different beta. A path has destination endpoints.
With no mixed endpoint it has one more beta than alpha; with exactly one
mixed endpoint its beta and alpha counts are equal. In both cases alternating
alpha--beta edges cover all alphas. With two mixed ends it has one more alpha
than beta. At most all but one can be paired with beta; attain this by
reserving the alpha next to one mixed end and pairing consecutively along
the remaining path. Assign the reserved alpha to that mixed end. Different
components are disjoint, and each exceptional path uses two different mixed
endpoints, giving 2t<=q. Theorem 1 proves legality of all selected links. QED.

The exact value in (3) is for the declared injection links. Other candidate
links, another injection or further relays may improve beta compensation.
A mixed endpoint remains zero credit; the exact unpaid count of this
optimized first step is t, not q or the number of BP terminals.

In particular q<=1 implies t=0 and all original alpha demands are paid by
different whole beta owners in one link each. More generally t=0 is a full
compensation certificate even when mixed candidates exist. Since the packet
has L>=B interval units before excluding its B marks, |D|<=beta also gives
S-B=L-B+beta-|D|>=0 in the established packet ledger. This settles a conditional
compensation class, without a universal `5/6` improvement.

A beta-only first step fails exactly on the two-mixed-ended components of
the chosen witness graph. It does not fail merely because two sources can
reach the same mixed owner elsewhere. This is the structural reduction for
subsequent cross-component compensation.

## 4. No-direct-access physical shared gate

Use a 14-by-20 rectangle, coordinates starting at zero. The explicit physical
configuration is below (`T` selected, `P` a matching endpoint, `.` blank).

```text
....................
....................
....T.T.............
...TPPPPT...........
.....PPP.T.T........
.....PPPPPPPPPPPT...
.....PPPPPPPPPPP....
.....PPPPPPPP..PT...
...TPPPPPPPPP..T....
....PPPPPPPPP.......
...TP..PPPPPPPT.....
....T.TPP..T.T......
........T...........
....................
```

The permanent fixture `develop/fixtures/unported_shared_mixed_gate.json`
lists all 17 selected points, 33 actual matching edges, and the 16 strict
freezing rank classes covering all 66 matching endpoints. Every matching edge
is a grid edge and endpoints are distinct. Each selected point has at most
one occupied neighbour. The strict-rank criterion of FROZEN_SHARED_MIXED_GATE.md
therefore proves complete freezing: each endpoint has two distinct neighbours
that are selected, or whose actual mates have strictly smaller rank.

With band b the row pair (2b,2b+1), the three critical PP paths are:

```text
A: (1,6),(2,6),(3,6),(3,7),(3,8),(3,9),(2,9)
B: (2,11),(3,11),(4,11),(5,11)
g: (2,10),(3,10),(4,10),(4,9),(4,8),(5,8),
   (5,7),(4,7),(4,6),(4,5),(4,4),(5,4).
```

Their terminal pairs are

```text
A: (3,6), (5,9)      TP--TP
B: (5,11), (10,11)   TP--TP
g: (5,10) BP, (10,4) TP.
```

These are the only two original alpha owners. At each of their four tips,
both horizontal neighbours are matching endpoints. Thus neither neighbouring
column is BB and neither is a BT selected-cap column. None of these tips has
any direct or selected-cap access, even before excluding marked intervals.
The maximum original-alpha direct-prepayment matching is exactly zero.

Nevertheless the horizontal links

    (5,9) -> (5,10),       (5,11) -> (5,10)

make g reachable from both surviving sources. The exit (10,4) has direct
access to singleton BB interval (band,column)=(5,5). It also has selected-cap
access via selected (10,3) and blank (11,3) to singleton BB interval (5,2).
Both intervals are interior, distinct and unmarked. No prior cancellation
or resource reservation is imposed on this fixture.

The restricted rule containing only these two links and the two exit accesses
again has projection K_{2,2}, value 2. Its true compensation value is exactly
1, minimum cost 1, and deficit 1: both links require the same BP terminal.
Deleting the single mixed gate blocks both sources. This remains an explicit
failure of source separation **after maximum direct prepayment**, since that
prepayment has no effect here. It does not claim failure after a preprocessing
step that is allowed to cancel alpha--beta pairs or alter the matching itself.

## 5. Full repair by two different whole betas

The full network has different first destinations. Let x be the beta path
with terminals (3,7),(5,8). Its actual-matching endpoint trace is

    (3,7)--M--(4,7)--PP--(5,7)--M--(5,8).

Let y be the different beta path consisting of actual edge (5,12)--(5,13).
Use the two terminal links

    (3,6) -> (3,7),       (5,11) -> (5,12).

The first consumes A with x, and the second consumes B with y. No terminal
or strand owner is reused, and each whole beta is charged once. Thus the
full compensation value is 2 with two links. This is optimal both in value
and in link cost: there are only two alpha sources, and neither has an
interval access. Every normal-form paid route therefore requires at least
one link. Two paid routes cost at least two, attained by these links.

For reference the full ledger is

    alpha=2, beta=5, mixed=3, balance=87,
    boundary budget=14, surplus_twice=180.

The boundary-adjusted scalar margin is 180-28=152. This is not a counterexample
to the global grid inequality. It is a counterexample to replacing simultaneous
route selection by a source-separated reachability assertion. The two-beta
repair exemplifies why choosing different first destinations is weaker and
more useful than requiring that every reachable mixed gate have only one
potential source.

The component-root extension is proved in
[COMPONENT_ROUTE_CERTIFICATES_AND_GROUPED_BETA_RESERVES.md](COMPONENT_ROUTE_CERTIFICATES_AND_GROUPED_BETA_RESERVES.md).
It groups each beta-surplus path as one reserve, chooses internal matchings
after exterior routes, and lifts reduced route packings without repeated credit.

## 6. Verification and remaining theorem

The standard-library verifier checks all 10,348 partitions of 2n witness
tokens into singleton/pair destination blocks for 1<=n<=5. It checks the
weighted Hall bound and a saturating assignment in each. Those finite checks
support, and do not replace, Theorem 1's general proof. Another 25,787 typed
unported token systems check Theorem 2's exact beta deficit, t<=floor(q/2),
and a simultaneous optimized assignment of every source to beta or mixed.
For n<=4 all singleton destinations are independently typed beta/mixed;
for n=5 both all-beta and all-mixed singleton choices are checked (coincident
choices are checked once). Pair blocks are always beta. This is an explicitly
bounded regression family, not exhaustive arbitrary graph coverage.

For the geometric adapter it checks 168 frozen packet models, with 128 alpha
owners and 336 weighted Hall subset checks, including the previous and new
gate fixtures, missing/cycle/collision families, grid symmetries and parity
offsets. The first-destination assignments reconstruct actual terminal
matchings and payments and verify (2). The new obstruction is separately
checked in all eight isometries carrying its band system. It checks original
alpha exhaustion, empty access sets at all four tips, strict rank witnesses,
both gate resources/reservations, the restricted optimum/cut and full optimum.
There are 104 all-unported controls (including empty-alpha cases) for the
exact beta formula. An existing frozen missing-port family attains t=1 with
q=2, so the bound on the beta-only first step is sharp. Its t is relative to
the chosen injection links; selected-cap payments or other links can improve
the full compensation and are not excluded by this example.

Run:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 develop/check_frozen_first_destination_allocation.py --output output/frozen-first-destination-allocation.json
```

`formal/SubQuorum/UnportedSharedMixedGate.lean` imports the general strict-rank
theorem from `FrozenSharedMixedGate.lean`. It kernel-checks this fixture's
feasibility and complete freezing, the three disjoint alternating physical
paths, terminal labels, absence of direct/cap access at all four alpha tips,
the two exit-resource locations and the explicit beta-exit data. Local
Lean 4.33.0 passes using ordinary `decide`; no `sorry` or `native_decide`.
Printed theorem dependencies are `propext` and `Quot.sound`. The generic
first-destination matching lemma, general flow normalization and full-network
optimization remain written proofs; they are not claimed formalized here.

The standalone Lean check requires only Lean core plus the previous module;
compile that local dependency into a temporary import directory, for example:

```sh
cd formal
mkdir -p /tmp/subquorum-first-destination-lean/SubQuorum
lean -o /tmp/subquorum-first-destination-lean/SubQuorum/FrozenSharedMixedGate.olean SubQuorum/FrozenSharedMixedGate.lean
LEAN_PATH=/tmp/subquorum-first-destination-lean lean SubQuorum/UnportedSharedMixedGate.lean
```

The Lean fixture's selected set and matching were also compared directly with
the canonical JSON fixture. Discovery used Z3 5.3.1 with the constraints in
`develop/search_unported_shared_mixed_gate.py`, followed by removal of five
unneeded selections and one two-endpoint mixed strand, and translation two
columns right to put both gate-exit intervals away from boundary marks. The
certificate proves this resulting fixture; no search completeness or size
minimality is claimed.

Oracle broker task `c9b98bb4-1af8-4685-84a3-be70985cb704` was submitted with
Theorem 1, the physical witness, the verifier and the prior injection theorem.
It failed with `model_unavailable@selecting_model` and produced no review.
Theorem 2 was developed after that submission. Neither new theorem nor witness
has an independent ACCEPT; the local proofs/checks above are separate evidence.

The next task is an invariant for later virtual alpha tips and jointly selected
complete routes, or a geometric budget for their exact separator deficits.
Theorem 1 removes immediate destination conflicts; the new witness shows why
this alone cannot certify that all future reachable gates are source-separated.
The universal grid inequality and `5/6` improvement remain open. The 11 October
submitted manuscript is unchanged.

Follow-up (25 October):
[Frozen fork exclusion and row surplus](FROZEN_FORK_EXCLUSION_AND_ROW_SURPLUS.md)
sharpens the row graph to isolated edges and BP-ended paths, proves exact
subset surplus and minimum mixed-target use, and supplies a full geometric
beta-only compensation class. It also explains the two-link beta allocation
of the no-direct-access shared-gate fixture. The universal grid bound remains
open.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
