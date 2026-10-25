# New selections: retained certificate, exact new-end defect, and a sharp reserved-pool obstruction

Continuation: [connected fully frozen extensions](CONNECTED_FROZEN_INTERVAL_REPAIR_OBSTRUCTION.md)
refute automatic applicability of the sufficient disjoint-new-interval Hall
condition below. After old C,4q new-new demands have whole-owner interval
rank only2q, but different beta stems pay all. The sufficient lemma itself
and the present extension theorem are unaffected.

25 October 2026. Haobo Ma and Wenlin Zhang. Isolated research branch.

The previous [endpoint-extension theorem](ENDPOINT_EXTENSIONS_AND_LOCAL_RESOURCE_REPLACEMENT.md)
fixed the selected set. We now allow arbitrary new selections as well as
arbitrary new endpoints and arbitrary simultaneous rematching. A local
exclusion audit shows that the OLD 23-TP certificate still persists. It need
not cover the genuinely new TPs. The resulting certificate loss is exactly
the number of post-cancellation alpha paths with TWO new TP ends, and is at
most floor(d/2), where d is the number of new TPs. In particular d<=1 gives
full ordinary compensation. Every new TP requires a different new selected
band partner, so d is at most the number s of new selections. Consequently
ANY endpoint extension with at most ONE new selection is fully compensated.

For this actual starting board, keeping the endpoint set fixed permits at
most ONE new physical TP. Consequently arbitrary feasible additions of
selections, arbitrary rematching of the 308 endpoints, and larger same-phase
rectangles have full ordinary compensation using the five old reserves.

There is also an unbounded feasible NONFROZEN obstruction to claiming that
these old reserves always suffice when both endpoints and selections grow.
It has d=2j and actual restricted deficit j, attaining the budget. Opening
its new interval resources restores complete compensation. Thus it refutes
the old-reserve rule, not compensation with all final resources, not a
frozen-only conjecture, and not the 5/6 target.

## 1. Hypotheses and what counts as a new TP

Start with the actual selected set T0 (49 sites) and endpoint set P0 (308)
of the 28-by-24 mixed-cycle fixture. Let a finite final rectangle contain it
with the same aligned two-row phase. Let

    T0 subset T,    P0 subset P,    T intersect P empty,

and let M be ANY grid perfect matching of P. Require the usual admissible
boundary and at most one occupied neighbour at each selected site. No old
matching edge or complete freezing is prescribed.

The 23 old physical TPs persist since both their endpoint and selected band
partner are retained. Write D for the set of final physical TPs outside
these 23, and d=|D|. A new TP may be a NEW endpoint with a new selected band
partner, or an OLD BP promoted by selecting its formerly blank partner.
The parameter is d, NOT the number of added selections or matching edges.

Every old selection has a retained occupied neighbour. Its other neighbours
remain blank even when T grows. Thus a new TP cannot have an old selected
band partner, and every old guarded BP target still has a blank partner.
All final alpha/beta owners and interval identities are recomputed from the
final configuration; no historical beta is spent.

Writing s=|T minus T0|, the band-partner map injects D into T minus T0, so
d<=s. This uses saturation of the old selections; retaining T0 alone would
not suffice on an arbitrary unsaturated starting geometry.

## 2. The five original flexible units survive new selections

Use the same 18 guarded old BP assignments and the following five candidates.
Each candidate u has a blank band partner q protected by the old selected
partner of its TP source v. In addition, u has the following two DIFFERENT
retained old endpoint neighbours:

| Source v | Candidate u | Two retained endpoint neighbours of u |
| --- | --- | --- |
| (12,14) | (12,15) | (11,15), (12,14) |
| (14,11) | (14,10) | (13,10), (14,11) |
| (19,11) | (19,10) | (19,11), (20,10) |
| (24,6) | (24,7) | (23,7), (24,6) |
| (24,17) | (24,16) | (23,16), (24,17) |

Hence u can NEVER become selected in a feasible extension. It either stays
blank or becomes an endpoint. The guarded two-state BB-to-BP replacement
therefore still applies, despite allowing new selections elsewhere.

It is also necessary to check the FINAL interval resource, not just its
candidate coordinate. The adjacent column containing v has a retained
endpoint and cannot become TT. Of the other adjacent columns, (band12,col8)
already contains retained endpoint (24,8). For the remaining four columns:

| Candidate's band | Adjacent column | Site s in that column | Retained endpoint w adjacent to s |
| --- | --- | --- | --- |
| 6 | 16 | (12,16) | (11,16) |
| 7 | 9 | (14,9) | (13,9) |
| 9 | 9 | (19,9) | (20,9) |
| 12 | 15 | (24,15) | (23,15) |

If both sites of such a column were selected, s would see its selected band
partner AND the different retained occupied w. This violates feasibility.
Thus neither adjacent column can ever become TT. In particular it is WRONG
to infer simultaneous TT feasibility merely because its two sites can each
be selected separately; the joint addition must be checked.

Every candidate that stays BB consequently remains the SAME strictly
internal, unmarked SINGLETON original interval. The five coordinates
(6,15), (7,10), (9,10), (12,7), (12,16) stay different resource identities.
No boundary propagation or interval merging is possible at these columns.

Let h be the number of candidate sites that become endpoints, and r=5-h.
We retain an injective partial physical certificate covering EXACTLY all
23 old TPs, using 18+h different BP targets and r different interval units.
All newly used BP targets were originally blank and are different from
the old 18. Their partners remain blank, so these targets cannot themselves
be promoted to TPs. Every new TP in D is a hole in this retained certificate.
An occupied candidate is an ENTRANCE and is not also an interval or beta credit.

## 3. Exact defect theorem for arbitrary joint extensions

Select the 18+h BP assignments as a physical terminal matching C. Let a,b
be final original alpha/beta counts and aC,bC the counts after cancellation.
Every free OLD TP has its own different assigned surviving unit; there are
exactly r such old free ends. Every member of D remains a free new TP,
because C uses old TP sources and guarded BP targets only.

Define k to be the number of post-C alpha paths whose TWO free ends are in D.
This is a quantity defined AFTER the final actual matching M and C, not by
pairing historical owner labels. Then

    2k <= d.                                                   (1)

Each other post-C alpha has at least one old free end. Choose such an end
and use its assigned surviving unit. These payments are different because
all old assignments are injective; every paying witness lies on its final
path. Exactly p=aC-k interval payments are made, with

    p <= min(r, floor((r+d)/2)).                                (2)

The first inequality counts distinct old ends used; the second counts two
different free ends per final alpha among at most r+d free TP ends.

The signed terminal ledger and beta monotonicity give

    a+bC=b+aC,   bC<=b,
    certified payment = b-bC+p = a-k.                          (3)

The established partial-certificate/ordinary-normal-form theorem turns this
into an ordinary packing with at least a-k payments using at most 18+h links
and at most p different original intervals. It preserves original resource
identities. No capacity is created by the normalization.

**Theorem.** For every joint extension in Section 1 and every available pool
Q containing the r surviving specified units,

    a - V_ord(Q) <= k <= floor(d/2),
    a - V_full(Q) <= a - V_ord(Q).                              (4)

Here k is the EXACT loss of the retained-assignment payment strategy; it is
an upper bound on the true optimum's loss. Other links or new intervals can
repair it. It is not legitimate to call k>0 a counterexample to full payment.
If k=0, both optima equal a and

    c_full(Q) <= c_ord(Q) <= 18+h.                             (5)

In particular d<=1 is sufficient, regardless of final rematching. More
generally, any rematching for which no final alpha joins two new ends is
fully compensated by the old retained certificate. This is a criterion, not
a general assertion that arbitrary new TP ends can be paired favourably.
Since d<=s, there is also the coarser bound floor(s/2). In particular adding
at most ONE selection and arbitrarily many endpoints is always fully paid.
All other interval units may be reserved. Which of the surviving units are
actually used still depends on the matching; (2) is not an arbitrary-subset
guarantee. An improved componentwise bound is available from the existing
partial-certificate theorem by counting new-end holes in each interaction
component; (4) is the simple global form.

**Disjoint-new-resource repair.** Suppose the k remaining new-new alpha
paths can be matched to k different FINAL original interval units outside
the r surviving specified units, with a valid physical interval-access
witness at one of each corresponding path's FREE new TP ends. Then pay those paths with that matching and
all other post-C alphas with their old assigned units. The two target sets
are disjoint, so no original interval is counted twice. The same ledger
and normal-form lift give full ordinary payment with at most 18+h links.
This is a sufficient condition. Failure of this restricted new-resource
matching need not imply failure of full compensation, because a different
choice of C or a joint reassignment of old units may work.

## 4. Arbitrary selection additions on the fixed old endpoint set

Suppose P=P0, with arbitrary T containing T0. Every new physical TP must be
an old BP whose formerly blank band partner is now selected. Any such new
selection s must satisfy BOTH necessary conditions:

1. It has at most one neighbour in the retained old occupied set T0 union P0.
2. It is not adjacent to any old selected site, since those sites are saturated.

The complete audit of all 308 actual old endpoints shows that, among blank
band partners, only s=(2,14) satisfies these conditions. It promotes endpoint
(3,14). All band partners are inside the original rectangle, so enlarging
the rectangle adds no other candidate for promoting an old endpoint.
Consequently D is a subset of {(3,14)}, and d<=1.

**Corollary.** Keeping exactly the 308 old endpoints, every feasible addition
of arbitrarily many selections, in any larger same-phase rectangle and with
ANY actual perfect matching of those endpoints, has full ORDINARY and full
fork compensation using only the five retained original singleton reserves
and final original beta resources. At most 18 links suffice.

The finite audit is an exact fact about the explicit initial data. The
extension/rematching argument is general and unbounded. This is not a
finite search over all possible selection subsets or matchings. Complete
freezing is unnecessary, so the statement covers every frozen member too.

## 5. An unbounded sharp obstruction to reserving every new resource

For any integer j>=1, put the old configuration into a (36+6j)-by-30 rectangle.
For each i=0,...,j-1 add

    selected: (30+6i,3), (33+6i,3),
    actual matching edge: (31+6i,3)--(32+6i,3).

The two selections are nonadjacent, each sees exactly its own adjacent
endpoint, and the gadgets are separated from each other and the old board.
All ordinary boundary conditions hold. The matching crosses a band boundary,
so both endpoints are TPs. Each gadget is a NEW original alpha owner with
no horizontal BP link. There are d=2j new TPs and h=0. The old C does not
touch any gadget, so each is also a post-C alpha with two new ends: k=j.

Let Q consist of ONLY the five surviving old specified interval units. Each
new alpha has no outgoing link and no accessible Q unit: all its supports
are in its new bands, whereas Q lies in old bands 6,7,9,12. It cannot be
paid, including by a beta-body fork. The original part is fully paid by
Section 3. Therefore the true ordinary AND full restricted deficits are
EXACTLY j=floor(d/2). This proves that (4) is sharp in the stated feasible
extension class, and disproves the rule "old reserves alone always suffice
under arbitrary additions of T and P."

If ALL final resources are available, each new alpha can instead use the
internal BB singleton at (band15+3i,col2). These units are different and
separate from the old five. Hence every alpha is paid in the full pool.
Exactly j NEW units are necessary and sufficient: each isolated new alpha
needs a different original interval, and the displayed j units achieve it.
This explicitly identifies the
missing resource and excludes confusing a reservation failure with failure
of the target all-resource compensation inequality.

These gadgets are NONFROZEN: each new endpoint has only its selected
neighbour and matched endpoint as occupied neighbours. It has no initial
freezing witness, and the separate pair cannot start a freezing chain.
Thus this is not a frozen-only obstruction and establishes no limitation
on the universal frozen-grid conjecture or 5/6 bound.

## 6. Validation and formal scope

The verifier checks simultaneous feasibility, FINAL physical labels, FINAL
original interval identities, the same retained partial certificate, its
exact new-new alpha loss, and ordinary/full optimizers independently of
the candidate count. It includes every individually feasible new selection
on the original rectangle, joint selection additions, endpoint/selection
additions together, rematching, and the explicit sharp family. It never
treats independent single-site selectability as joint TT feasibility.

All 450 models pass, including 224 completely frozen and 226 feasible
nonfrozen configurations. There are 126 independent primitive ordinary/full
comparisons. The controls comprise 310 single-new-selection/original-rematching
models (all 155 individually feasible sites, each in two matchings), 64
joint selected-only controls, 32 arbitrary-endpoint controls with one new
selection, 32 joint endpoint/selection controls, and 12 members of the sharp
reserved-pool family. Ninety-five models have genuine new TPs. The 12
positive certificate-loss controls are exactly the explicitly nonfrozen
sharp family; no frozen or all-resource counterexample is claimed.

See [computational receipt](../output/selected-extension-budget-validation.json),
[verifier](../develop/check_selected_extension_budget.py), and
[reserved-pool fixture](../develop/fixtures/selected_extension_reserved_obstacle.json).
The Lean additions check the general two-neighbour and selected-pair
exclusions, exact end counts, loss/interval/payment arithmetic, and the
concrete five-candidate/adjacent-column/unique-promotion audits. Physical
interval-network adaptation, arbitrary-M path decomposition and the ordinary
normal-form lift remain written/Python. This is NOT end-to-end Lean of the
joint extension theorem. No submitted manuscript, public main, PR3, shared
CI, correspondence or independent star-forming/C4 result is changed.

The new conclusion settles arbitrary selection growth with fixed P0 and
gives an exact retained-certificate defect for arbitrary joint growth. For
the general frozen problem, the remaining task is to pay or exclude the
post-cancellation alpha paths with two new TP ends, using final new resources
without reusing the units already assigned to old paths. Ordinary reachability
alone is insufficient if those resources are shared; a joint original-unit
matching or a sharp geometric obstruction is still required.

All ten new and all twenty-one combined local Lean4.33.0 audits pass with
exit0. The final log is clean; the axiom union is propext, Classical.choice
and Quot.sound, with no sorry or native evaluation. Six combined declarations
are axiom-free. Concrete local witnesses are supplied explicitly. See the
[formal receipt](../output/selected-extension-budget-formal-check.json),
[final Lean log](../output/selected-extension-budget-lean-validation.txt) and
[direct Lean source](../formal/SubQuorum/EndpointExtensionReplacement.lean).
