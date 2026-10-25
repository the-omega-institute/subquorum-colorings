# A persistent beta-paid core around the actual frozen mixed cycle

25 October 2026. Haobo Ma and Wenlin Zhang. Isolated research branch.

The [cyclic tree/gap criterion](CYCLIC_BETA_ESCAPE_CUTS.md) exposed an
entrance obstruction in a restricted interface. For the actual frozen
four-source cycle we now settle an entire class of COMPLETE extensions:
if its old selected sites and actual matching edges are retained, arbitrary
feasible additions cannot remove its four compensating beta paths or make
them accessible to outside sources. Every old source can be paid using
these four different original betas and five links, without any interval.

Consequently the four-source core eliminates exactly from the whole original
ordinary AND beta-fork allocation networks, with all final interval identities
and reservations retained. This holds for arbitrarily many separated initial
copies even when later additions connect their surrounding components.
It does not cover rematching old edges, an arbitrary different mixed cycle,
or universal compensation/improvement of5/6. The reduction is algebraic;
deleting the core need not leave an actual feasible or frozen subboard.

The flow reduction is elementary. The new geometric content is a finite
local certificate that proves persistence against ALL feasible additions,
including additions of new endpoints, rather than testing a finite list of
extensions.

## 1. Extension scope and the two blank rules

Use the actual28x24 fixture with49 selections and154 matching edges.
An extension retains EVERY old selected site and EVERY old matching edge,
and can add selected sites and disjoint nearest-neighbour matching edges.
It is feasible: a selected site sees at most one occupied neighbour, T/P
are disjoint, and matching endpoints have unique mates. The final board
may be any larger finite rectangle containing the old board, with the
same two-row band phase; an even translation is allowed. Use the final
board's standard admissible boundary marks and any subset Q of its eligible
original intervals. Nothing requires an old interval identity to survive.

The initial board is completely frozen. The preservation theorem itself
requires only feasibility of the extension, so also applies whenever the
extension is completely frozen. Arbitrary rematching is NOT allowed.

**Rule A (selected guard).** If a retained selection t already sees a
retained occupied w, a different neighbour q of t is permanently blank.
Otherwise t would see the two occupied neighbours w,q.

**Rule B (matched-neighbour enclosure).** Suppose q was blank, has at
least two different retained occupied neighbours, and every neighbour of q
is either a retained old matching endpoint or a permanently blank site.
Then q is permanently blank. It cannot be selected, by the two occupied
neighbours. If it were a new endpoint, its mate could not be blank and
could not be an old endpoint: that endpoint's retained old mate would
give it a second mate. These exhaust ALL physical neighbours.

Rule B does not assume that every unoccupied site is initially forced
blank, or that additions must occur in a particular order. Its fixed old
mates are the reason it remains valid with arbitrary simultaneous additions.

## 2. Fifteen blank certificates preserve all eight entrances

Here are twelve Rule-A blanks, with the actual retained selection and an
occupied neighbour already using its allowance. Coordinates are zero-based.

| Forced blank q | Retained selection t | Its old occupied neighbour w |
| --- | --- | --- |
| (3,4) | (3,5) | (2,5) |
| (3,19) | (2,19) | (2,20) |
| (4,3) | (4,4) | (5,4) |
| (4,5) | (3,5) | (2,5) |
| (4,15) | (3,15) | (3,14) |
| (4,16) | (4,17) | (5,17) |
| (4,18) | (4,17) | (5,17) |
| (4,20) | (4,19) | (5,19) |
| (19,16) | (19,15) | (18,15) |
| (21,16) | (20,16) | (20,17) |
| (25,5) | (25,4) | (24,4) |
| (25,18) | (25,17) | (24,17) |

The following three blanks then follow by Rule B. Their listed old endpoints
are matched by retained old edges; the list exhausts the four neighbours.

| Forced blank q | Old P neighbours | Rule-A blank neighbours |
| --- | --- | --- |
| (3,3) | (2,3),(3,2) | (3,4),(4,3) |
| (3,20) | (2,20),(3,21) | (3,19),(4,20) |
| (21,17) | (20,17),(21,18),(22,17) | (21,16) |

Thus all BP band partners of the four designated mixed gates and the four
chosen whole betas remain blank. The old alpha TP partners and mixed TP
partners remain selected. Every internal PP pair remains occupied and every
old actual edge remains its mate edge. Following M/PP from an old strand
can therefore neither change an internal edge nor acquire a new end beyond
its old terminal. The four old alphas, four mixed gates and four chosen
betas retain their exact endpoint bodies and terminal types in EVERY extension.

Denote these old alpha sources by A,B,C,D and the mixed gates by g0..g3,
as in the preceding notes. The chosen beta identities, given by terminal
pairs, are

    bA: (5,15)/(5,16),    bB: (2,20)/(5,20),
    bD: (2,3)/(5,3),      bC: (20,17)/(18,16).

They are different original strands in the FINAL extension, not historical
credits borrowed from strands that have since merged or changed type.

## 3. No outside source can enter the protected owners

Let K consist of A,B,C,D, all four designated gates and these four betas.
All original TP--BP links are horizontal. Inspect BOTH horizontal neighbours
of every BP entrance in K. This exhausts the possible incoming links,
including links that a future extension might attempt to add.

* g0's predecessors are D,A; g1's are A,B; g2's are C,B; g3's are D,C.
  These are the fixed original alpha TP neighbours of their BPs.
* bA has only incoming A at (5,16). Its other neighbours are fixed PP,
  or the other BP of bA, so cannot become TP.
* bB has only incoming B at (5,20). The other neighbours are retained T
  or fixed PP.
* bD has only incoming D at (5,3). At its far BP(2,3), the side(2,2)
  is fixed PP and side(2,4) cannot become TP because its partner(3,4)
  is a Rule-A blank. The other side of BP(5,3) is fixed PP.
* bC has only incoming g2, from (18,15) to (18,16). The other neighbours
  are retained T or fixed PP.

An alpha has no BP entrance. Hence EVERY link entering K has its TP owner
in K. A path rooted at an outside alpha cannot first enter K: its first
such link would have an outside predecessor, a contradiction. This is
closure of all original incoming links, not just closure of the routes
used by the displayed payment witness. A two-arm beta fork cannot admit an
outside arm into one of these four betas either.

The internal witness pays all four sources by

    A: (5,17)->(5,16) into bA,
    B: (5,19)->(5,20) into bB,
    D: (5,4)->(5,3) into bD,
    C: (24,17)->(24,18) into g2,
       then (18,15)->(18,16) into bC.

It uses four different beta identities, different source/mixed owners and
five different actual links. It spends NO original interval. No outside
payment can occupy any of its owners, by the incoming closure.

## 4. Exact elimination for every original interval subset

In the FINAL original allocation network delete the owners K and their
incident links. Keep EVERY final original interval identity, with the SAME
availability set Q; keep all other owners, beta BP capacities, beta-body
supports and whole-beta resources. Let V_res,c_res denote the residual
maximum payment and minimum link cost at that value. Let V,c be the full
original optima.

**Theorem (persistent closed mixed-cycle core).** In BOTH ordinary and
full beta-fork compensation, for EVERY feasible retained-matching extension
and EVERY Q,

    V = 4 + V_res,
    c_res <= c <= 5 + c_res.                               (1)

Every paid outside source set can be preserved while paying the four old
sources. The statement does not require the old sources to be interval-
deficient in the final board.

**Proof.** A residual packing extends by the four beta stems above. No
outside path enters K; the four added beta resources are absent from the
residual network and no interval is spent. This adds exactly4 payment
and5 links, proving the lower bound on V and the upper bound on c once
maximum values are identified.

Conversely project any full primitive packing by removing all paths rooted
at A,B,C,D. No outside path uses an owner in K, by Section3. If an old source
was paired with an outside source in a fork at an EXTERIOR beta, keep the
outside arm as a stem to that same whole-beta resource and release its
interval. At most one outside arm survives such a two-arm fork. This uses
the existing beta normalization and preserves the outside source and all
its links. The projected packing is residual and loses at most4 payments,
so V<=4+V_res. It has no greater link cost, giving c_res<=c for a full
maximum packing after the equality of values. In fact every maximum pays
all four old sources: otherwise retaining its outside payments and adding
the four internal stems would strictly improve it. This proves(1). QED.

No exact additive link cost of5 is claimed. In the original full interval
pool V4/c2, whereas with no available intervals V4/c5. Allowing additions
can create further alternatives. The universal5-link internal witness
gives a bound independent of every final interval reservation.

Let k,b,I be the final full source, whole-beta and eligible-interval counts.
The residual model has k-4 sources, b-4 beta units and the SAME I, so

    I+b-k = I+(b-4)-(k-4).                                 (2)

No old interval is claimed to persist through additions. No interval
identity is removed, and each of the four eliminated whole-beta resources
is spent exactly once. The numerical ledger is unchanged. The residual
network is an allocation model, not a physically deleted frozen board.

## 5. Arbitrarily many cores and scope of verification

Initially put copy i at row offset32i+2 in a32q-by24 rectangle. These even
translations preserve the band phase and separate the original cores and
their guard certificates. After that allow ANY feasible additions retaining
all initial selections and matching edges, including additions connecting
the exterior components across buffers or in a larger rectangle.
Each blank certificate and horizontal entrance classification is local;
no such addition changes them. Thus the q protected owner sets are disjoint
and closed to outside incoming paths. Their witnesses spend4q different
whole betas and5q links. Applying the same projection/extension proof gives

    V=4q+V_res,       c_res<=c<=5q+c_res,
    I+b-k=I+(b-4q)-(k-4q).                                 (3)

This is an all-q, arbitrary-extension theorem, not a claim from bounded
enumeration. In particular the previous local cycle obstruction cannot
be made into an uncompensated COMPLETE counterexample by adding sites
while retaining the actual matching of this fixture.

The new verifier reconstructs the15 local blank certificates and exhausts
both horizontal neighbours at every protected BP. It compares full and
residual flows, with independent primitive controls and final-original
interval reservations, on feasible single additions, multi-addition
prefixes, literal multi-core boards and nonempty exterior research patches.
The receipt states which tested extensions are completely frozen; arbitrary
feasible controls are not relabeled frozen.

The new Lean file proves the two arbitrary-extension blank rules, the
concrete15-blank coordinate adapter using retained local guards, no entry
from outside into an incoming-closed owner set along arbitrary-length paths,
and the nonreuse ledger. Whole-strand persistence, complete interface/flow
elimination and the physical adapter beyond those blank certificates are
written/Python, not an end-to-end Lean allocation theorem. The previous308P
freezing certificate remains unchanged and is not rerun as a new result.

What remains: rematching old edges can defeat the Rule-B retention
hypothesis, and an arbitrary frozen mixed cycle need not contain these
local guards or exclusive exits. The full five-source shared-resource
obstruction and universal compensation still require their general geometric
analysis. This result resolves the retained-matching completion class of
THIS actual mixed-cycle family, without changing the submitted manuscript.
