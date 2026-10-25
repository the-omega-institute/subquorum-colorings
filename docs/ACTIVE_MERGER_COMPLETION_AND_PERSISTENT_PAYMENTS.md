# Active-merger completions: a forced cycle and persistent private payments

25 October 2026. Haobo Ma and Wenlin Zhang. Isolated research branch.

The active two-source short-tail merger is a genuine restricted-interface
obstruction, but its original bypasses cannot both be removed for free by
retaining the original matching and selections. We classify a guarded
three-column gap: six feasible local states reduce to four under complete
freezing. Filling the last alpha interval forces a pure PP/M cycle FIRST,
then creates a whole beta available only to that alpha. The other alpha has
a permanently private BT-corridor interval.

For ANY completely frozen monotone extension on the fixed packet rectangle,
the two old alphas eliminate exactly from ordinary and full compensation.
For q copies, including extensions that connect the surrounding components,

    V = 2q + V_res,             c = f + c_res,               (1)

where f is the number of filled guarded gaps. Each private interval or whole
beta is consumed once; the resource surplus is unchanged. This settles the
entire matching-retaining completion class of the new active-merger family.
It does not assert that an arbitrary frozen short-tail merger has such a gap,
or prove universal compensation or an improvement of5/6.

The private-source and empty-body-beta flow reductions are elementary and
build on [protected singleton reserves](PROTECTED_SINGLETON_RESERVES.md) and
[guarded pockets](GUARDED_POCKETS_AND_MONOTONE_FORK_REPLACEMENT.md). The new
content is the three-column completion classification, the freezing-forced
cycle prerequisite and their persistent application to the active merger.

## 1. Extension scope and the original board

Start with the [14x18 active-merger board](../develop/fixtures/frozen_active_short_tail_merger.json),
with25 selections and31 actual matching edges, or q copies translated by14i
rows. One may first append any even number of blank columns at the right.
Fix that rectangle, band phase and coordinates. A monotone extension keeps
EVERY old selection and actual matching edge, and may add further selections
and disjoint nearest-neighbor matching edges anywhere in the rectangle.
It must remain feasible, completely frozen, and an admissible aligned packet:
the first column of every band stays blank and its last column retains a
blank corner. The packet boundary marks are the usual ones computed in the
extended original board; there are no arbitrary extra reservations.

The fixed rectangle and first blank column matter for the EXACT COST in
(1). Expanding the board on its left or changing boundary reservations is
not included: it can release other intervals. The local gap classification
and the displayed private-payment constructions themselves use only their
listed guards. No freezing assertion is inferred by deleting a physical
matching edge. All extensions are checked on their actual final matching.

Every old alpha path persists. Its actual matching edges and internal PP
partners are fixed, and each old TP end keeps its selected partner, so a
new PP edge cannot extend that end. An old pure PP/M cycle likewise remains
closed. Other old beta or mixed paths may change type or join new paths;
these belong to the residual problem.

## 2. General guarded three-column gap

Use odd r, column s, and the following initially blank sites:

    u=(r-1,s),  a=(r-1,s+1),  d=(r-1,s+2),
    v=(r,s),    w=(r,s+1),    x=(r,s+2).

There is an old alpha TP A at (r,s+3) with selected partner (r-1,s+3).
The two old P sites at (r-1,s-1),(r,s-1) are an actual two-point PP/M pure
cycle. The sites (r-2,s), (r+1,s), (r+1,s+1), (r+1,s+2) are old matching
endpoints. Finally (r-2,s+1) is selected and already sees the old endpoint
(r-2,s). All these old actual mates and selections are retained.

In the active fixture take r=5,s=3. The cap is columns3,4,5, the left old
cycle is column2, and the alpha TP is (5,6).

**Lemma 1 (six feasible states).** In every monotone feasible extension,
a,d remain blank. Among u,v,w,x the ONLY possibilities are

| State | New selections | New actual matching edges |
|---|---|---|
| E | none | none |
| T | w | none |
| C | none | uv |
| H | none | vw |
| B | none | wx |
| CB | none | uv and wx |

These refer to all changes at these six sites, regardless of changes outside.
All six states are feasible when added alone to a feasible initial board.

**Proof.** The selected (r-2,s+1) already sees its old P neighbor, so a
cannot be occupied. The selected partner of A similarly excludes d.
The site u cannot be selected, because it sees the two old endpoints above
and left. Its possible mates above and left are already matched, and a is
blank, so u can match only v. The site v sees two old endpoints left and
below, so cannot be selected and can match only u or w. Likewise x sees A
and the old P below, so cannot be selected and can match only w. The only
site that could be selected is w; if it is, its old P neighbor below already
uses its occupied-neighbor allowance, so v,x must be blank, which also
forces u blank. If w is not selected, matching uniqueness permits only
subsets of uv,vw,wx with disjoint endpoints. This gives the other five rows.
No outside vertex can be used as an alternative mate: every such candidate
at the mutable sites is an old matched P or a forced blank.

Conversely none of the three added edge types meets an old selection, and
their endpoints were blank. Adding w as selected gives it exactly its old P
neighbor below and does not add an occupied neighbor to another selection.
Thus the listed local additions are all feasible. □

**Lemma 2 (complete freezing forces the cycle).** States H and B are
impossible in EVERY completely frozen extension, even with arbitrary outside
additions. If wx is present, uv must therefore also be present. The other
four states E,T,C,CB are completely frozen when added alone to an initially
completely frozen board.

**Proof.** In H or B the endpoint w has its actual mate on one horizontal
side and the old P below. Above is a forced blank; the other horizontal
neighbor is blank by Lemma1 and matching uniqueness. Thus w has only ONE
occupied nonmate neighbor. It cannot have two distinct retained neighbors
in any strict rank certificate. The missing sites cannot be filled by
outside additions without leaving the six-state classification. This is
an all-ranks degree obstruction, not an unsuccessful finite search.

For E no change is needed, and T only adds a selected point, preserving all
old freezing witnesses. For C, both new uv endpoints freeze after the old
board: u uses its old P neighbors above and left, v its old P neighbors
left and below. For CB, first freeze that pure cycle; x can freeze using A
and its old P neighbor below, then w using its old P below and v, whose
mate u is now frozen. Old witnesses remain valid throughout because all
old actual mates and selections were retained. □

## 3. The left payment never disappears without replacement

**Lemma 3 (private interval or exclusive beta).** In E,T,C the original
singleton interval

    J_L=(band=(r-1)/2, first=s+2, last=s+2)

persists, is unmarked and has A as its SOLE eligible open owner. In CB,
wx is a whole beta with EMPTY whole support, and its only possible incoming
TP link is from A to x. These resources are private to A even in arbitrary
outside monotone feasible completely frozen extensions.

**Proof.** In E,T,C, x and d are blank, so their column is BB. Every upper
site in the three-column cap is blank, except the PP cycle uv in C. No TT
column can join this singleton to another BB. It therefore retains exactly
the same original coordinate identity, strictly inside the packet. The
endpoint-free gap containing it has A at the right boundary. Its left
boundary is either the old closed PP/M cycle in column s-1 (E,T), or the new
closed PP/M cycle in column s (C). Neither is an open owner. There is no
other boundary through which an open owner supports this unit. All these
boundary paths and selected/blank guards persist, proving exclusivity.

In CB, a,d are blank, so w,x are BP ends and their actual edge is a whole
beta. On its left stands the closed PP cycle uv, and on its right stands A.
Thus the beta has no endpoint-free support gap and W(beta) is empty. The
left BP's other horizontal neighbor v is permanently PP, not TP. The right
BP's other horizontal neighbor is the fixed alpha TP A. Hence no source
except A can enter this whole beta. Outside changes cannot modify either
blank partner or either neighboring old/new closed component. □

This is why the apparent way to seal the last alpha interval fails to
remove its payment: complete freezing forces the closed cycle and then
replaces the interval by an exclusive beta. The beta is ONE resource,
not one unit for each BP.

## 4. A permanently private right corridor interval

For the second alpha A_R in the actual fixture, consider columns13,14 of
band2. The selected (4,12) already sees its old TP (5,12), so (4,13) stays
blank. The selected (4,14) already sees the old P (4,15), so (5,14) stays
blank. The site (5,13) sees the two old P sites (5,12) and (6,13), excluding
selection. Its only possible mates would be those two old matched endpoints
or the two forced blanks (4,13),(5,14). Thus it too stays blank.

**Lemma 4.** The interval J_R=(band2,first13,last13) stays an available
original singleton in every such extension. Its gap is the fixed BB13,
BT14 pair, bounded by old alpha A_R at TP column12 and PP column15.
It therefore has ONLY A_R as eligible open owner.

**Proof.** The locking argument fixes BB13 and BT14. The bounding old alpha
path cannot change. BT14 prevents this BB singleton from joining a further
BB--TT component, while the two occupied boundary columns fix its whole
support ownership. It is strictly internal and unmarked. □

This uses a BT corridor and the actual matching locks, rather than assuming
a new generic freezing witness always produces a protected singleton.

## 5. Why a filled left cap requires one actual link

For exact cost we must exclude an unrelated zero-link payment for A_L.
On the actual original board the compressed band-column nodes of its path
are precisely

    (1,1), (2,1), (2,6), and (3,j), 1<=j<=6.

The ONLY adjacent endpoint-free gaps are the three-column cap (band2,
columns3..5) and the one-column LEFT BOUNDARY gaps at column0. This follows
also by expanding the permanent actual alternating path: every other
neighboring band column contains an old matching endpoint.

In a monotone extension all those old occupied neighbor columns stay
occupied; the old alpha cannot grow. Any new adjacent gap is contained in
one of those old gaps. The first column of the fixed packet is still BB
and marked, so its one-column gaps supply no available interval. In CB all
three cap columns contain P. Consequently

    W(A_L)=empty in EVERY admissible extension with its cap filled. (2)

Thus any payment for A_L uses at least one actual terminal link. Its
exclusive beta route uses exactly one. In E,T,C its private interval uses
zero links. This is an original-source cost statement, not an inference
from the cost of a particular preselected route.

## 6. Exact simultaneous elimination, including arbitrary exterior coupling

Take q translated copies of the actual fixture on a fixed rectangle with
the stated packet boundary. The extension may connect other components,
add new alphas, change old non-alpha strands or create beta forks anywhere.
Only the old matching and selections and the packet assumptions are fixed.
The local classification holds separately at each cap. Let f count the
CB caps; 0<=f<=q.

For each old right alpha choose J_R. For each old left alpha choose J_L
in E,T,C or its exclusive whole beta in CB. Distinct copies have different
band/coordinate identities, and the selected beta edges are different.
No chosen unit can be entered from any other source. Let N_res delete all
2q old alpha source owners, the 2q-f chosen original interval units and
the f chosen empty-body beta owners, retaining EVERY other exterior owner,
BP gate, beta private sink, whole support and original interval identity.
This is deletion in the allocation network, not physical deletion.

**Theorem 5 (persistent private-payment elimination).** For both ordinary
compensation and the full BP-aware fork model, equation(1) holds exactly.
Every attainable set of paid outside sources remains attainable while all
old 2q alphas are settled by the displayed private units.

**Proof.** An outside residual packing extends by the 2q private payments,
using f actual links. Private intervals have only their chosen alpha as
support owner; an exclusive beta has only its chosen alpha as an entrant
and empty W. Thus these additions reuse no outside source, BP, beta or
interval. This gives V>=2q+V_res and c<=f+c_res.

Conversely every maximum must pay every chosen old alpha. If one were
unpaid, its private unit would be unused: only that alpha can reach it.
Its private path could be added, increasing the value. In any full flow,
reroute each old alpha onto its private unit. This preserves all outside
source payments and releases other used capacities. The replacement costs
zero in an interval case and one in a beta case. By(2) the beta case's old
route already cost at least one, so cost never increases. All replacements
are compatible because the units have distinct original identities.

Remove the 2q private paths. What remains is a feasible residual packing
of value V-2q, so V<=2q+V_res. Removing their exactly f links from a
minimum-cost maximum yields a residual maximum of cost at most c-f;
hence c>=f+c_res. Combine with the extension bound. Full beta forks outside
these units cause no difficulty: the full network preserves individual BP
entrance capacities, and after any route is removed the existing free beta
normalization can redirect a remaining arm to its unused private sink
without adding links. Ordinary stems are the same argument in the ordinary
subnetwork. QED.

If k is the extended board's alpha count, I its original available intervals
and b its beta count, the residual ledger is

    k_res=k-2q,    |I_res|=|I|-(2q-f),    b_res=b-f,
    |I_res|+b_res-k_res = |I|+b-k,
    k-V = (k-2q)-V_res.

There is NO additional 2q surplus to credit elsewhere. Exactly one interval
or whole beta is removed with each settled source. Any remaining conjectural
bound is precisely the residual problem, with its complete exterior coupling
retained. If there are no other alphas, all old2q sources are paid and the
minimum actual link count is exactly f.

## 7. Checks, formalization and limits

The solver-free command is

    python3 develop/check_merger_completion_reserves.py --output output/merger-completion-reserves-validation.json

The [receipt](../output/merger-completion-reserves-validation.json) records
1,035 frozen completion models with exact value/cost elimination,144 independent
primitive-pack comparisons, all six local feasible states with two explicit
nonfreezing controls,340 four-state copy choices,359 frozen one-addition
extensions among805 feasible packet additions, and288 accepted multi-addition
prefixes. Twelve controls retain a NONEMPTY residual problem with positive
payment and link cost, instead of verifying only empty residuals. These
finite tests validate coordinates and implementations; Lemmas1--4 and the
network proof establish the arbitrary-extension statement.

[MergerCompletionReserves.lean](../formal/SubQuorum/MergerCompletionReserves.lean)
derives actual complete inductive freezing for all four concrete completions
from strict witnesses. It proves that either degree-two completion admits
NO strict certificate for ANY rank assignment, verifies the conditional
four-state classification, and checks the elimination/resource ledgers.
The geometric derivation of all possible local edges, persistent ownership,
source support exclusion and the general full-network projection are written
proofs, not claimed as end-to-end Lean. See the
[formal receipt](../output/merger-completion-reserves-formal-check.json).
No new independent external review or Oracle acceptance is claimed.

This result resolves arbitrary matching-retaining completions of the active
merger family. It does NOT classify arbitrary matching changes that reroute
old edges, nor prove every frozen merger contains these guards. The next
question is whether an arbitrary residual shared entrance can be assigned
a jointly sufficient reserve of this kind, or whether changing the old
matching can remove the reserves without creating compensating credit.
The submitted11October manuscript, public main, PR3, shared CI and mail are
outside this research branch.

Follow-up: [fixed-endpoint matching rigidity](MATCHING_INDEPENDENT_ACTIVE_MERGER_RESERVES.md)
now removes the matching-retention assumption for the four fixed-endpoint
states and arbitrary feasible selected supersets, including all separated
copies. It does not yet cover simultaneous endpoint additions and rematching.
