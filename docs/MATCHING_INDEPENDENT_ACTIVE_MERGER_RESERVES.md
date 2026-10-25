# Frozen matching rigidity and matching-independent active-merger reserves

25 October 2026. Haobo Ma and Wenlin Zhang. Isolated research branch.

For the active short-tail merger, the four completely frozen cap states have
**unique completely frozen actual matchings at fixed endpoint set**. This
remains true after any feasible addition of selected vertices. Thus the
private payments proved in the
[completion note](ACTIVE_MERGER_COMPLETION_AND_PERSISTENT_PAYMENTS.md) cannot
be destroyed by rematching these fixed endpoint sets. For any number q of
separated copies, with arbitrary choices of the four states and arbitrary
feasible selected supersets, both compensation models satisfy

    k = V = 2q,                 c = f,

where f is the number of cycle-plus-beta states. Every paid source consumes
one distinct original interval or whole beta. The resource surplus receives
no extra credit from this elimination.

The proof uses an arbitrary-graph closed-trap lemma and explicit edge
exclusions, not enumeration of matchings. Independent enumeration is only a
control. This result removes the matching-retention assumption for the
specified fixed-endpoint class. It does not remove that assumption from the
previous theorem about arbitrary additions of endpoints. Those are different
extension classes. The universal compensation inequality and the 5/6 bound
remain open.

## 1. Precise scope

Start with the saved
[14 by 18 actual board](../develop/fixtures/frozen_active_short_tail_merger.json).
Use the six cap modifications E,T,C,H,B,CB from the completion note. For one
chosen state, retain exactly its endpoint set P and all its selected points
T0, but allow **any** nearest-neighbor perfect matching M on P and any
selected superset T of T0. Require feasibility, complete freezing for M,
and the same admissible packet boundary and standard boundary marks. No
arbitrary resource reservations are added. An even blank right padding can
be fixed before choosing T. The phase and the left boundary stay fixed.

The four good states are E (empty), T (selection w), C (cycle uv), and CB
(cycle uv plus beta wx), where

    u=(4,3), v=(5,3), w=(5,4), x=(5,5).

For q copies translate each board by (14i,0). No other endpoints are added.
The selected superset can be chosen globally; it need not be chosen by a
product construction. The copies' endpoint graphs have no connecting edge.
All claims concern the actual final matching, not an auxiliary PP matching.

There is no universal matching-uniqueness assertion. In particular,
[the exchange-terminal fourteen-endpoint core](EXCHANGE_TERMINAL_NONUNIQUE_MATCHINGS.md)
has two different completely frozen matchings; both are retained as controls.

## 2. A closed-trap lemma for arbitrary candidate matchings

Let P be any endpoint set, let T be the actual selected set, and let E be a
candidate matching graph containing every actual matching edge. Let S be
any upper bound on the selected vertices relevant to the endpoints:
every selected neighbor of P belongs to S. S is allowed to be infeasible.

For a nonempty set U of endpoints, define the optimistic retained neighbors
of v in U by

    R_E,S,U(v) = N(v) intersect
                (S union {y in P : E(y) has a vertex outside U}).

**Lemma 1 (closed trap).** If every v in U has at most one vertex in
R_E,S,U(v), the actual matching is not completely frozen.

**Proof.** Suppose otherwise, and choose the first endpoint of U to freeze.
Each of its two distinct retained neighbors is selected, or is an endpoint
y whose actual mate froze earlier. In the latter case the actual mate is
outside U and belongs to E(y). Both retained neighbors therefore lie in
R_E,S,U(v), contradicting its size bound. Equivalently, induction on the
freezing derivation proves that every frozen endpoint avoids U. This proof
uses no number-of-vertices or rank bound and applies to arbitrary graphs.
It even grants different neighbors mutually incompatible candidate mates,
so finding a trap under this optimistic rule is a valid exclusion. QED.

**Lemma 2 (sound edge reduction).** The following operations preserve every
completely frozen perfect matching compatible with E:

1. If an endpoint a has a single candidate mate b, pin ab: remove every
   other candidate edge incident to a or b.
2. To exclude a candidate ab, temporarily pin it, perform any number of
   singleton forcings, and exhibit a nonempty closed trap for the resulting
   candidate graph. Then remove ab from the unconditioned graph.

**Proof.** Operation 1 follows from perfect matching and uniqueness of a's
mate. A matching containing ab would remain compatible after pinning and
every singleton forcing in operation 2. Lemma 1 would then contradict its
complete freezing. Consequently no such matching contains ab. Induction
over the reduction sequence proves preservation. If the final graph has a
single candidate mate at every endpoint, every completely frozen matching
equals that graph. QED.

This is a proof system, rather than a test of all matchings: one blocked
set can simultaneously exclude arbitrarily many matching completions. A
certificate checker needs only local adjacency, singleton candidate sets
and the displayed bound of one possible retained neighbor.

## 3. A selected-support upper bound that covers every feasible extension

At fixed P, feasibility depends on occupied and selected vertices, not on
which perfect matching pairs P. Deleting added selections preserves
feasibility. Thus every newly selected neighbor y of P in a feasible T must
itself be a feasible single-selection addition to T0. Every such y is in
N(P), so there are only finitely many local sites to inspect, even with
arbitrary blank right padding. Direct inspection of the supplied coordinates
gives the following *complete* lists:

| State | Possible new selections touching P |
| --- | --- |
| E | (5,4), (8,14), (8,15) |
| T | (8,14), (8,15) |
| C | (8,14), (8,15) |
| CB | (8,14), (8,15) |
| H or B | (8,14), (8,15) |

For example the site (8,16) cannot be added because T0 already contains
(7,16), whose occupied neighbor allowance is used; analogous selected
guards exclude all other adjacent blanks. Selected points not touching P
cannot enter a freezing witness. Set S=T0 together with all the listed
helpers. The simultaneous union S need not be feasible: it is deliberately
an upper bound. Lemma 1 consequently covers **every feasible selected
superset**, without enumerating those supersets or assuming their additions
occur in a special order. For the global inclusion T subset S used in the
Lean statement, add every site outside N(P) to S; this changes none of the
retained-neighbor tests at endpoints.

## 4. Fixed-graph rigidity certificates

Start E with every physical nearest-neighbor edge joining points of P.
The
[certificate](../develop/fixtures/merger_matching_rigidity_certificate.json)
records the complete proof sequence for each good state. A `leaves` entry
lists the forcing endpoint and its sole candidate mate, in order. An
`exclude` entry lists the assumed edge, the branch's singleton forcings,
and a nonempty trap U. After each exclusion the next listed global forcing
is applied. For every trap the
[validation receipt](../output/merger-matching-rigidity-validation.json)
also lists the at-most-one optimistic retained neighbor at every v in U.
These are coordinate certificates of Lemma 2, not lists of tested matchings.

| State | Endpoints | Trap exclusions | Final matching |
| --- | ---: | ---: | --- |
| E | 62 | 5 | the original 31 edges |
| T | 62 | 5 | the original 31 edges |
| C | 64 | 9 | the original 31 edges and uv |
| CB | 66 | 10 | the original 31 edges, uv and wx |

One small exclusion illustrates the mechanism. After the preceding
certificate reductions, assume (5,9)--(5,10). In its forced branch the
two-point set

    U={(5,12),(6,11)}

is a trap. The two endpoint neighbors (5,11) and (6,12) each have candidate
mates only in U. The endpoint (5,12) can therefore use at most its selected
neighbor (4,12). The endpoint (6,11) can use at most its other neighbor
(7,11). Neither endpoint can be first to freeze, irrespective of how the
remaining matching is completed. Other exclusions use the same argument
with traps of two to fourteen points.

For H and B, w has only two occupied neighbors even in S. Any perfect
matching uses one as w's mate. With that pair pinned, {w} is a closed trap:
w's mate has no candidate mate outside {w}, leaving at most the other
occupied neighbor as retained. Thus **no matching** on either endpoint
shape can be completely frozen. This exclusion also covers arbitrary
feasible added selections.

**Theorem 3 (rigidity).** In every good state and every feasible selected
superset, the only completely frozen matching on P is the saved matching
for that state. H and B have no completely frozen matching.

**Proof.** The selected-support bound in Section 3 applies to every candidate
in the statement. Replay the explicit local certificates of Lemma 2; their
final graphs are exactly the saved matchings. The preceding singleton-trap
argument handles H and B. For existence in each good state, its saved
matching has a strict complete-freezing certificate, already verified in
the completion note. Adding feasible selections preserves all those
witnesses. This proves existence as well as uniqueness. QED.

The geometric certificate is finite because the seed graph is finite.
The logical proof applies to arbitrary actual matchings and arbitrarily
large freezing ranks. In particular no completeness statement about a
matching enumerator is needed for Theorem 3.

## 5. Simultaneous compensation and the remaining gap

**Corollary 4.** Under Section 1's q-copy hypotheses, every completely frozen
actual matching is the union of the saved state matchings. The number of
alphas is 2q, all can be paid, and the minimum number of actual links is f
in both the ordinary and full BP-aware models.

**Proof.** Distinct copies have no neighboring endpoints, so every perfect
matching restricts to a matching on each copy. Every selected neighbor
within a copy is covered by its local S; complete freezing restricts too,
since there is no external endpoint dependency. Apply Theorem 3 to each
copy. We have now derived preservation of the original matching rather
than assumed it. The previous private-payment elimination theorem applies:
J_R is private to the right alpha, and the left alpha uses J_L in E,T,C
or its exclusive empty-body beta in CB. Every copy contributes two sources
and two distinct resources. None of the listed helper sites lies opposite a P in its band column,
so added selections cannot turn a beta or mixed tip into a new alpha.
There are no other alphas. Therefore V=2q.
The filled-cap alpha has empty direct whole support, so needs at least one
actual link; its private beta gives exactly one. All other private payments
use zero links, proving c=f. All source/resource identities are distinct,
so no unit of slack is used twice. QED.

The ledger is exactly

    k_res=k-2q, I_res=I-(2q-f), b_res=b-f,
    I_res+b_res-k_res=I+b-k.

The new result is compatible with the earlier arbitrary matching-retaining
extension theorem but does not subsume it: here P is fixed, whereas that
theorem allowed extra endpoints and exterior coupling. An extension that
adds endpoints and rematches an old endpoint into the new region is covered
by neither theorem unless one separately proves matching retention. Such
an edge may defeat the local traps by creating new candidate mates outside
U. That is the precise remaining hypothesis to investigate. No failure of
the compensation inequality is claimed.

## 6. Verification and formal scope

Run the solver-free checker, which replays the saved certificates first:

    python3 develop/check_merger_matching_rigidity.py --output output/merger-matching-rigidity-validation.json

It checks all 29 explicit trap exclusions, both bad fixed-endpoint shapes,
and the final singleton graphs directly from raw geometry. The optional
`--refresh-certificate` discovers a new proof sequence; discovery is not
needed to check the saved proof. Independent controls enumerate 22,22,330
and3966 perfect matchings in E,T,C,CB respectively: in each case only the
saved matching freezes even under the optimistic S. Fifteen feasible helper
subsets preserve the exact value/cost payment, checked with 30 independent
primitive packs. The pre-existing core with two fully frozen matchings is
checked separately, preventing a false global interpretation.

[MatchingRigidityTraps.lean](../formal/SubQuorum/MatchingRigidityTraps.lean)
proves the arbitrary-graph inductive closed-trap theorem, nonempty trap
exclusion, upper-support monotonicity, singleton forcing, compatibility
under pinning/deletion, uniqueness at singleton candidate graphs, and the
resource ledger. Its first seven audited statements have no axioms; the
integer ledger uses only the standard propext/Classical.choice/Quot.sound.
Local Lean4.33.0 passes. The specific coordinate certificate replay and
support-list completeness are checked by Python and the written adapter;
they are **not claimed as end-to-end Lean uniqueness of this board**.
No independent external review was received in this round.

The 11 October submitted manuscript, public main, PR3, shared CI and email
were not changed. These are research notes for later discussion or a
separately reviewed manuscript addition.
