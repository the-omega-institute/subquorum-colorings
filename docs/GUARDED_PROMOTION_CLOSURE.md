# Guarded promotion closure: count only TPs on genuinely added endpoints

25 October 2026. Haobo Ma and Wenlin Zhang. Independent research branch.

We strengthen the [joint selected/endpoint extension theorem](SELECTED_EXTENSIONS_AND_NEW_TP_DEFECT_BUDGET.md).
An old endpoint that becomes TP need not remain a hole in the certificate.
Its newly selected band partner can itself guard an unused old BP target.
For the actual 49T/308P geometry this repairs EVERY possible old-endpoint
promotion. It works simultaneously in arbitrarily many connected copies,
with arbitrary new selections/endpoints and arbitrary actual rematching.

Only TPs on genuinely ADDED matching endpoints remain holes. If their
number is e, the true ordinary deficit is at most floor(e/2), and the exact
retained-strategy loss is the number of post-cancellation alpha paths whose
two free ends are such fresh endpoints. In particular e<=1 guarantees full
ordinary compensation, even with arbitrarily many new selections. This is
a general-extension theorem for the declared retained geometry, not a
universal frozen-grid theorem or a new numerical improvement of 5/6.

## 1. A general guarded-promotion augmentation lemma

Work in the usual feasible grid model: T and P are disjoint, every selected
site has at most one occupied neighbour in T union P, and M is a perfect
grid matching on P. Let bar(v) be v's aligned two-row band partner.
Suppose a partial physical TP certificate is already valid in the FINAL
configuration. It assigns different TP sources to different BP targets or
declared interval slots. The following lemma concerns the assignment only;
it does not prescribe M, historical strand owners, or historical beta units.

Let S be a set of further TP endpoints not yet covered. For every v in S
choose a retained endpoint u(v) horizontally adjacent to v, in the SAME
row, such that:

1. the u(v) are different;
2. none is already a BP target of the current certificate;
3. bar(v) is selected in the final configuration and u(v) is retained in P.

**Guarded-promotion lemma.** Each u(v) is an actual BP target in the final
configuration, and appending all v->u(v) gives a valid injective certificate.

**Proof.** Put t=bar(v) and q=bar(u(v)). Since u(v) and v are horizontal
neighbours in the same row, t and q are horizontal neighbours. The selected
t already sees the occupied v. The different neighbour q must be blank,
otherwise t would have two occupied neighbours. Thus u(v) is in P with
blank band partner q: it is BP. The physical TP--BP link is available.
The hypotheses make its target new and all targets different. The sources
are new and different, and a point cannot simultaneously be TP and BP.
Interval assignments are unchanged. This proves the certificate assertion.
No whole-beta identity has been assumed or spent. QED.

The lemma is conditional on a joint injective choice of targets. Separate
existence of a target for each source does NOT imply such a choice: two
sources can name the same physical BP. The new hypotheses must be checked,
including possible collisions with flexible BB-to-BP replacements.

## 2. Exact retained geometry and extension scope

Let B be the fixed 28-by-24, 49T/308P board. For n>=1 let B_n consist of
n copies shifted by (0,24i), i=0,...,n-1. For n=1 use B itself. For n>1
use exactly the closed PP seam splices in
[the connected frozen construction](CONNECTED_FROZEN_INTERVAL_REPAIR_OBSTRUCTION.md).
Its selected set T0 has49n sites, its endpoint set P0 has308n+4(n-1)
sites, and its occupied graph is connected. Every endpoint is completely
frozen for the displayed initial matching. The theorem below requires only
feasibility of the FINAL extension, not complete freezing.

Let a final finite same-phase rectangle contain B_n, retain T0 subset T
and P0 subset P, and allow ANY actual perfect grid matching M on P. Old
edges need not remain. Arbitrary selections and matching endpoints may be
added simultaneously, subject to feasibility and the standard admissible
band boundary. No preservation of old beta owners or old interval IDs is
assumed; all final owners and resources are recomputed.

The initial geometry has23n physical TP endpoints. The old adaptive
certificate uses, per copy,18 guarded physical BP targets and five distinct
flexible candidates. A candidate remaining BB supplies an original
singleton; a candidate newly occupied supplies an actual BP entrance.
The [previous joint-extension proof](SELECTED_EXTENSIONS_AND_NEW_TP_DEFECT_BUDGET.md#2-the-five-original-flexible-units-survive-new-selections)
shows that neither candidate can become T, its partner stays blank, and
its adjacent columns cannot become TT. These local facts translate to
every copy. The surviving units are internal, so final global boundary
marks and other copies do not merge their identities.

Let h count occupied flexible candidates over all copies. Then r=5n-h
different surviving original units and18n+h different BP targets cover
exactly the old23n TP endpoints. All49n old selections remain saturated
by retained occupied neighbours; a TP on a genuinely new endpoint cannot
have an old selected band partner.

## 3. Every old-P promotion has its own unused BP target

In one base copy, an old endpoint v can become a NEW physical TP only if
its originally blank band partner can become selected. A necessary condition
is that this partner has only one retained occupied neighbour, namely v.
A complete base-coordinate audit gives exactly ONE possibility:

    v=(3,14),       new selection t=(2,14).                  (1)

For every other old endpoint, its partner is already in T0 or P0, or has
at least two different retained occupied neighbours. This is a finite
certificate of exclusions on the fixed geometry; it applies to ALL later
extensions because the occupied blockers are retained. The existing Lean
unique-promotion audit is rerun. The new verifier additionally lists two
explicit retained occupied blockers for each other blank-partner endpoint.

The extra seam endpoints have occupied band partners and cannot become
TP. Thus (1), translated by (0,24i), exhausts all possible old-P promotions
in B_n, even after arbitrarily many further additions and rematchings.

For (1), choose

    u=(3,13),       q=bar(u)=(2,13).                        (2)

Both v,u are retained endpoints. The new selected t is adjacent to v and
q, so it forces q blank. Hence u is a permanent BP WHILE (1) is activated.
If (1) is not activated, no claim that q must stay blank is needed.

The point (3,13) is not one of the18 old BP targets, nor one of the five
flexible candidates. Distinct translated targets (3,13+24i) are different
and cannot equal targets or flexible candidates of another copy: all of
those lie strictly inside their own24-column block. The guarded-promotion
lemma therefore applies simultaneously to every activated copy.

Write p for the number of activated promotions,0<=p<=n. The augmented
certificate covers23n+p TP endpoints using

    physical BP assignments = 18n+h+p,
    different original units = r=5n-h.                      (3)

This is a physical certificate independent of actual M. A BP entrance is
not a second beta resource, and no old beta strand is claimed to survive.

## 4. Exact fresh-end loss and the stronger compensation bound

Let E be the set of FINAL physical TP endpoints in P minus P0, e=|E|.
All physical TPs outside E are now covered by (3). Every endpoint in E
remains unassigned. Each has a newly selected band partner, and these
partners are different from the p promotion selections. Thus, with
s=|T minus T0|,

    e+p<=s.                                                 (4)

Choose the18n+h+p BP assignments as a physical terminal matching C. Use
the FINAL original strands, and let a,b be original alpha/beta counts,
aC,bC their post-C counts. Exactly r covered TP ends remain free, each
assigned its different surviving original unit. The e fresh TP endpoints
also remain free. No physical TP end is counted twice.

Let k be the number of post-C alpha paths whose TWO free ends belong to E.
Each other post-C alpha has an assigned free TP end. Pay it using that
end's original unit. The units used by different such paths are different,
because their assigned ends and all certificate resource identities are
different. Therefore the number of interval payments is exactly

    used = aC-k <= min(r,floor((r+e)/2)),
    2k<=e.                                                  (5)

The signed cancellation ledger gives a+bC=b+aC, with bC<=b. Consequently
the retained-assignment strategy makes exactly

    b-bC+used=a-k                                            (6)

payments. The established physical-certificate lifting/ordinary normal form
turns this into an ordinary packing with at least a-k payments, using at
most18n+h+p actual links and the indicated distinct final original units.
It may normalize to a subset of C; it need not retain every selected link.

**Theorem (promotion-closed arbitrary extension).** Under Section2, for
every available original interval pool Q containing these r surviving units,

    a-V_full(Q) <= a-V_ord(Q) <= k
               <= floor(e/2) <= floor((s-p)/2).              (7)

Here k is EXACT for the displayed retained-assignment payment strategy,
not asserted equal to the true optimum's deficit. The bound holds for
every actual rematching, frozen or not. If e<=1, or more generally k=0,
both compensation models pay all a sources, and

    c_full(Q)<=c_ord(Q)<=18n+h+p.                            (8)

In particular arbitrarily many new selections at old endpoint partners
are harmless: they create no remaining certificate holes. Keeping P=P0
allows arbitrary feasible additions of T and arbitrary simultaneous actual
rematching and guarantees full ordinary compensation for EVERY n. The same
holds with arbitrarily many added endpoints if at most one of them is TP.

Compared with the previous unaugmented certificate, the coarse number of
new TP ends was p+e. Its bound floor((p+e)/2) is replaced by floor(e/2).
This can remove an unbounded artificial loss as n grows. It does not
assert the old strategy actually attained that coarse bound in this family.
The original one-selection theorem remains correct; (7) gives a larger
class with arbitrary many selections and at most one fresh-end TP.

## 5. Sharpness and verification limits

The fresh-end budget cannot be reduced without additional hypotheses.
Start with one base board and activate (1). Far below it add j separated
gadgets, each with selections (30+6i,3),(33+6i,3) and actual matching edge
(31+6i,3)--(32+6i,3). These create e=2j fresh TP endpoints, while p=1.
Their post-C alphas have both ends fresh, so k=j. If only the old five
units are available, the actual ordinary deficit is j. Opening one new
original unit beside each gadget gives full compensation.

These separated gadgets are feasible but NONFROZEN. They prove sharpness
of the retained-pool extension budget in the theorem's feasible domain;
they do not refute compensation with all original resources or a
frozen-only bound.

A separate actual310P example is completely frozen and has TWO new
selections, at(2,14),(18,9). Its new physical TPs are the retained endpoint
(3,14) and the genuinely added endpoint(19,9). The new certificate absorbs
the first and leaves only e=1, proving full compensation for ANY actual
rematching of this occupation. The saved initial matching is fully frozen;
an arbitrary rematching need not be. The old coarse two-new-TP criterion
alone gave no zero-deficit guarantee, although the old strategy happens
also to have zero loss for this particular displayed matching.

The verifier rebuilds final physical terminals, interval identities and
certificate slots. It tests literal connected copies, simultaneous
promotions, arbitrary extra selections, filled flexible candidates, new
TP endpoints and actual square rematchings across the full rectangle.
Independent primitive packings check selected ordinary/full optima. The
358 controls include201 frozen and157 feasible nonfrozen models,188 actual
rematchings (153 switches outside the first copy),12 many-selection
extensions and28 independent primitive comparisons. All frozen/nonfrozen
labels are recomputed, not inferred from feasibility.

    PYTHONDONTWRITEBYTECODE=1 python3 develop/check_guarded_promotion_closure.py
    cd formal
    lean SubQuorum/EndpointExtensionReplacement.lean

See [computational receipt](../output/guarded-promotion-closure-validation.json),
[formal scope](../output/guarded-promotion-closure-formal-check.json), and
[the actual310P fixture](../develop/fixtures/guarded_promotion_fresh_tip_frozen.json).

Eight new scoped Lean declarations check the guarded target, simultaneous
target injection, actual fresh target, arbitrary-copy injection, fresh-end
budget and selection injection arithmetic, payment ledger and interval
budget. The21 earlier audits in the same source are rerun. Full geometric
extraction, the arbitrary-extension adapter and physical certificate
lifting remain written/Python; this is not an end-to-end Lean proof.

Continuation: [protected shared columns and fresh ends](PROTECTED_SHARED_COLUMNS_AND_FRESH_ENDS.md)
gives a completely frozen sharp retained-pool family, disproves localization
by matching-difference components alone, and proves a persistent shared-unit
compensation class under arbitrary rematching. It does not solve all fresh ends.

The remaining general obstacle is the simultaneous payment of alpha paths
with TWO genuinely fresh matching endpoints. Their interval-only repair is
already known to fail under freezing in other configurations, so their
mixed routes, final original beta identities and original interval units
must be treated jointly. Universal compensation and a numerical5/6
improvement remain open. The submitted manuscript is unchanged.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
