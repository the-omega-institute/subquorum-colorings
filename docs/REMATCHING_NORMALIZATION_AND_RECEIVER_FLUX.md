# Matching exchange, a five-edge promotion, and the receiver flux

22 October 2026. Authors: Haobo Ma and Wenlin Zhang.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.

## 1. A stronger normalization than fixed-matching freezing

Let (T,M) be a feasible pair in a finite simple graph, P=V(M), T disjoint
from P. Every selected
vertex has at most one neighbour in A=T union P. Replacing M by any perfect
matching of G[P] preserves feasibility, P, T and |T|+|M|. Then apply any
nonempty feasible promotion bundle: promote one endpoint of each chosen
edge, delete its mate and delete that edge. This keeps the objective,
retains every original selection, and strictly reduces the endpoint set.

**Exchange-normalization lemma.** Every finite feasible pair has an
objective-preserving representative retaining its original T such that
no perfect matching of its remaining induced endpoint graph admits a
nonempty promotion bundle. It can be reached using at most the original
|M| promotion steps, each preceded by one matching replacement.

Proof. Whenever a matching replacement and bundle are possible, perform
them. Each step deletes at least one matching edge and never adds an
endpoint. The nonnegative integer |M| strictly decreases, proving
termination and the step bound. At termination the stated universal
condition is exactly the absence of another step. Feasibility, retention
and objective preservation hold at each step. This is an existence lemma;
it does not give an efficient algorithm for finding a suitable replacement.

The condition factors over actual endpoint components. Every perfect
matching and every bundle restricts to those components: matching edges
cannot cross them, and endpoint neighbours of a promoted vertex stay in
its component. Original selections stay occupied. Conversely, a local
matching replacement and bundle extend by the unchanged data elsewhere.
Thus other endpoint components cannot rescue a locally impossible step.
In particular the final representative is single-terminal, because an
endpoint of occupied degree at most two would admit a single promotion.

On a finite bipartite graph the existing complete freezing test may be
applied separately to every candidate perfect matching. Fixed-matching
freezing alone does not establish this stronger terminal condition.

For an extremal proof this stronger condition costs nothing: choose a feasible
pair maximizing |T|+|M|, and then maximizing |T| among those maximizers.
A matching replacement followed by a nonempty bundle would preserve the
first quantity and increase the second, a contradiction. The same argument
applies to a pair of maximum |T| among counterexamples to the half-area bound
on a fixed finite board, if a counterexample exists on that board. Thus a valid local exchange obstruction can be
excluded from a general-grid extremal argument, not just from a prescribed
source family.

## 2. General accounting: promotion redistributes charge

Use an even-by-even grid with its fixed physical two-by-two tiling.
Suppose the initial and final pairs are both single-terminal, and that
the final pair comes from matching replacements and promotions, with no
other moves. Fix one original endpoint component H and its closed tile
receiver R_H. All final endpoint components descended from H have
pairwise disjoint receivers contained in R_H. No final endpoint component
can join two old components, because endpoint sets only decrease.

Let F_H be the old receiver tiles that finally contain no endpoints.
Let t'_Q be their FINAL selected counts and d'_Q=2-t'_Q. Write rho_H for
the old whole corrected charge, and rho'_K for descendant whole charges.

**Exact receiver-flux lemma.**

    sum_(K descended from H) rho'_K
        = rho_H + sum_(Q in F_H) d'_Q.                 (1)

In particular total descendant charge is at least rho_H. A disappearing
endpoint receiver does not make its charge available as new compensation.

Proof. Rematching changes none of the counts in the whole-receiver
formula rho=T_R+|P_R|/2-2|R|. Let k be the total number of promotions
descended from H. All k promoted vertices lie in R_H, so the final total
selection count there is T_R+k. The remaining matching count is |H|/2-k.
The descendant receivers use |R_H|-|F_H| tiles. Their selected count is
T_R+k-sum_F t'_Q. Substitute these three counts into the sum of their
closed-receiver formulas; k cancels and the result is (1). All saturated
matching transfers are internal to each closed receiver. Feasibility
gives t'_Q<=2 and hence d'_Q>=0. QED.

**Positive receiver persistence.** A strictly positive old receiver cannot
lose all its endpoints under such a sequence. Otherwise its descendant sum
in (1) is zero, whereas the right side is strictly positive. In particular
normalization cannot simply erase every positive-demand component; the
remaining descendants still require genuine compensation.

Original no-endpoint tiles are unchanged: every new selection is an old
endpoint, and no endpoint is added. Consequently, with D and D' denoting
the total deficits on all old and final no-endpoint tiles,

    D'=D+sum_H sum_(Q in F_H) d'_Q,
    D'-sum_K rho'_K = D-sum_H rho_H.                  (2)

This is an exact global ledger for differently oriented components and
capacity-two tiles. Each freed physical tile has one old component owner,
appears once in F_H, and contributes the SAME amount to both sides of the
first difference. Its deficit cannot be counted again as a gain from the
normalization. Intermediate pairs need not be single-terminal; only the
two endpoint configurations of this accounting statement require that.

Thus the signed scalar bound D>=sum_H rho_H for all exchange-terminal
representatives would imply |T|+|M|<=mn/2 for every initial feasible pair.
When the initial pair is single-terminal, (2) also transports that same
signed scalar inequality directly. For a general initial pair, use objective
preservation; its receivers need not yet partition tiles. This does not
transport a geometric assignment of donors to individual receivers, or
replace signed charge by positive charge. The missing universal compensation
theorem and a universal coefficient improvement remain open.

## 3. A square exchange unlocks five matching edges

Here is a local move valid in every feasible grid exterior preserving
its six specified matching edges and three blank sites. Coordinates may
be translated or transformed by any grid isometry. In standard coordinates
the OLD matching contains

    (5,5)--(5,6), (6,2)--(7,2), (6,4)--(6,3),
    (7,5)--(6,5), (7,3)--(8,3), (7,4)--(8,4).

The sites (4,5),(6,1),(7,6) are blank. Exchange the last two vertical edges
for (7,3)--(7,4) and (8,3)--(8,4). The occupied labels do not change.
Now promote

    X={(5,5),(6,2),(6,4),(7,3),(7,5)},
    deleting Y={(5,6),(7,2),(6,3),(7,4),(6,5)}.

These are five distinct matching edges after exchange; the new horizontal
edge (8,3)--(8,4) remains. The only possible retained neighbours of the
promoted vertices are:

| Promoted endpoint | Only possible retained neighbour |
| --- | --- |
| (5,5) | (5,4) |
| (6,2) | (5,2) |
| (6,4) | (5,4) |
| (7,3) | (8,3) |
| (7,5) | (8,5) |

Every other neighbour is in Y or is one of the three prescribed blanks.
Hence each newly selected vertex has occupied degree at most one.
Old selected vertices only lose neighbours. This proves feasibility and
an objective-preserving decrease of five matching edges, with no assumptions
on unlisted exterior labels. Endpoint (7,3) always has occupied degree four
and loses three neighbours. Endpoint (6,4) also loses three neighbours;
it has degree four if (5,4) is occupied, as in the charge-two fixture and
in every single-terminal application. Without that extra occupancy it has
degree three. The move still necessarily involves a degree-four endpoint.

### A matching-independent geometric exclusion

Let S be the twelve endpoints of the six displayed OLD edges. Suppose all
vertices of S are in P, the three specified sites are blank, and G[P minus S]
has a perfect matching. Then the six displayed edges together with that
completion form a perfect matching of all P, irrespective of the current M.
Section3 applies to it and yields an objective-preserving five-edge promotion.

Consequently an exchange-terminal representative cannot have this twelve-site
endpoint/three-site-blank motif with a perfectly matchable complement, in any
translation or grid isometry. This is a concrete forbidden local pattern with
an explicit matching-extension condition. The condition is substantive: an
arbitrary partial matching need not extend, even when the whole endpoint graph
has a perfect matching. A four-vertex path with its middle edge prescribed is
the elementary counterexample.

The rule is algorithmic on arbitrary finite grids. For each of the linearly
many placements and eight orientations, test the required labels and find a
bipartite perfect matching of P minus S. If it exists, reconstruct the complete
matching, perform the exchange and promote the five endpoints. Repeat the full
motif search after each change. Ordinary single-edge promotions, found by
scanning endpoints, may be interleaved with the same repeated search.
Each accepted step deletes matching edges, so
the process terminates and uses polynomial time with a standard polynomial
bipartite-matching algorithm. This specific normalizer excludes this motif;
it does not decide exchange terminality for every possible bundle or establish
universal compensation. Its finite controls include a nonextendible middle
edge so that the completion condition is not silently omitted.

## 4. What happens to the known charge-two frozen obstruction

Apply Section 3 to the exact fixture CHARGE_TWO_FROZEN_RECEIVER.md, whose
complete specification remains unchanged. Its original 19-edge matching
is fully frozen. The square exchange above unlocks the five-edge bundle.
The final pair has 25 selections, 14 matching edges and the same objective39
in the same14-by10 rectangle. All 28 remaining endpoints are again frozen.

The old charge2 receiver splits into two receivers with respectively

    (endpoints, tiles, selections, charge)=(12,6,7,1),(16,8,9,1).

Exactly three old receiver tiles are freed, at tile indices (2,3),(3,1),
(3,2). Each has two final selections and deficit0. Total no-endpoint
deficit stays33, total receiver charge stays2, and half-area minus objective
stays31. This is an explicit distinction between fixed-matching freezing
and exchange terminality. It does not retract the original counterexample
to the charge-at-most-one rule under fixed-matching freezing, or prove
that the rule holds under the stronger normalization.

The final endpoint graph also has a degree-one forcing certificate. In the
following order, the first vertex of each pair has exactly the second as its
only remaining endpoint neighbour, after all earlier pairs are removed:

    (1,4)--(2,4), (3,1)--(4,1), (3,4)--(4,4),
    (5,1)--(5,2), (4,2)--(4,3), (5,3)--(5,4),
    (8,8)--(8,7), (8,6)--(8,5), (10,4)--(9,4),
    (8,4)--(8,3), (9,3)--(9,2), (8,2)--(8,1),
    (9,1)--(10,1), (11,1)--(12,1).

These pairs exhaust its endpoints. Every perfect matching must contain
each pair in order, so its matching is unique. Together with the final
freezing certificate, this shows the displayed final pair is exchange-terminal.
The original example thus becomes two irreducible charge1 components,
rather than merely two temporarily frozen components.

## 5. The thick-elbow obstruction survives matching replacement

For E(W,H) of ELBOW_SOURCE_EXCLUSION.md, even W>=6,H>=4, its induced
endpoint graph has exactly one perfect matching. This follows by successive
degree-one forcing, independently of its selected supports:

1. The left tip (2,0) forces its edge to (1,0).
2. For each even c=0,2,...,W-2, force (0,c)--(0,c+1), then, if c<W-2,
   force (1,c+1)--(1,c+2). At each step the first listed vertex has only
   its displayed neighbour left. After this only (1,W-1) remains in the bar.
3. For each odd r=1,3,...,H-1, force (r,W-1)--(r+1,W-1), then, if r<H-1,
   force (r+1,W-2)--(r+2,W-2).

The listed pairs exhaust E and agree with its prescribed matching.
Every perfect matching must contain each forced pair, inductively, so it
is unique. Existing general freezing then excludes every nonempty promotion
bundle, even in a feasible exterior retaining the complete elbow and its
supports. Matching replacement has no alternative. Together with the
previous source-subset exclusion, this rules out normalizing this elbow
to a complete U/rotor source cover by matching replacement and promotion
alone. Broader primitives or a different move are genuinely needed.

For persistence through a whole sequence, consider its first step touching
an elbow endpoint. Before it, the complete endpoint set and prescribed
supports are unchanged. Any replacement matching restricts to the unique
elbow matching; the retained-mate freezing certificate forbids that first
promotion, even when combined with other components. The source-subset
exclusion concerns endpoints alone, independently of all selected exterior
labels, so it continues to apply throughout such a sequence.

## 6. A nonzero-flux sign control

Take the four endpoint corners (3,3),(3,4),(4,3),(4,4), the two vertical
matching edges, and selections (2,3),(3,5),(5,4),(4,2) in an8-by8 rectangle.
Every endpoint has occupied degree3 and every selection has one endpoint
neighbour. Promote (3,3),(4,4) and delete their vertical mates. There are no
endpoints afterwards. The initial four-tile receiver has four selections
and two matching edges, hence charge -2; final receiver charge is0.
Two freed tiles have final deficit1 and two have final deficit0.
Thus the charge INCREASE is2, exactly the newly available no-endpoint
deficit. This verifies the positive sign in (1), and is a counterexample
to a proposed nonincrease-of-total-receiver-charge rule for promotions.
It does not violate objective preservation or the desired inequality.

## 7. Verification scope and remaining question

The written proofs above are all-parameter statements. The checker separately
reconstructs the local six-edge move, its exact labels, every perfect matching
of the finite charge-two fixture, terminal receiver charges, freed-tile
counts and transformed applications. It validates the degree-one forcing
certificate on finite elbow dimensions, with positive controls detecting
nonunique matching in a square.

Scoped Lean verifies local geometric uniqueness of retained neighbours and
the exact regional/global flux identities. Final local Lean4.33.0 execution
passes6theorems/4definitions/10individual axiom audits, with ordinary axioms
only and no errors, warnings, sorry or native evaluation. A local larger
heartbeat allowance resolves the geometry proof's initial default-limit
timeouts. The finite-graph termination, component factorization, matching
and source adapters remain written proofs.

The exact controls pass:8perfect matchings of the original fixture, of
which3are fully frozen and5are not; the final pair has one matching and
is fully frozen. Eight matching-independent completion controls, a
nonextendible-partial-matching control, a sparse exterior in which (6,4)
has degree3,24transformed flux checks including16strictly positive cases,
8generic motif-normalizer applications and3irreducible-elbow controls pass.
The342finite elbow forcing controls check15,048forced edges. These controls
do not replace the written all-parameter proofs.

Initial independent reviewd725ecea completed REVISE: it accepted the main
proof mechanisms but correctly identified the unqualified degree-four
description of (6,4). This is corrected and the sparse control added.
The review also requested explicit disjointness, signed-scalar scope and
the endpoint-only source-exclusion dependency, now supplied. It did not
execute code or Lean. Follow-up bc36dde9 completed ACCEPT at06:49UTC, covering
the revised full note, matching-independent rule and polynomial normalizer,
final forcing certificate, pinwheel control and full endpoint-only source
exclusion. The original prompt equals its session prompt, and the original
completed stream, terminal task and session responses agree exactly. The
observed model was gpt_6/pro. This is an independent mathematical review of
the written arguments and coordinates, not execution of code or Lean.

The open next step is a geometric compensation bound for exchange-terminal
components, using actual physical donors and the flux ledger. The new move
removes one known large-charge obstruction from that stronger class; the
irreducible elbow shows why a source-only decomposition still does not suffice.
Submitted manuscripts and the earlier complete-source39/41 theorem are preserved.
The immutable-source39/41 ledger is not automatically inherited after a
matching exchange changes source ownership. This note uses the physical
whole-receiver ledger; applying a source-labelled bound afterwards requires
reestablishing its own hypotheses.

Further structural reduction: exchange terminality does not imply a unique
perfect matching, even for a positive connected receiver. The explicit
fourteen-endpoint obstruction and all-even positive elbow graft in
EXCHANGE_TERMINAL_NONUNIQUE_MATCHINGS.md have exactly two perfect matchings,
both frozen. Thus the general compensation target must retain flexible
matching blocks rather than identifying exchange terminality with uniqueness.
