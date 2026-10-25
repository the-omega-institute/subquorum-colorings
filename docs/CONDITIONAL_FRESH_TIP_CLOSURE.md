# Conditional fresh-tip closure under arbitrary occupation extensions

25 October 2026. Haobo Ma and Wenlin Zhang. Research branch only.

The previous [guarded promotion closure](GUARDED_PROMOTION_CLOSURE.md)
absorbed all new TP tips on retained endpoints, but counted every TP on a
new matching endpoint as a hole. We now absorb a prescribed set of **27
potential fresh-tip sites per copy** as well. An activated tip either has
a different available original singleton, or a different actual BP target.
The choice is determined by the final occupation. The construction remains
valid under arbitrary additions of T/P and arbitrary actual rematching;
the final board need only be feasible, not completely frozen.

Only fresh TP tips outside this protected set remain holes. This is a
stronger arbitrary-extension compensation class on the actual 308P base
and its PP-connected copies. It is not a new abstract flow theorem or a
universal grid compensation proof. The numerical 5/6 bound remains open.

## 1. A conditional local witness

Let T0 and P0 be retained old selections and endpoints in a feasible grid
extension (T,P,M). Use horizontal bands, and write bar(v) for the other
site in v's band column. Suppose v and t=bar(v) were old blank sites, and
v is now a TP: v is in P and t in T. Let w be a horizontal neighbour of v,
and q=bar(w). Assume:

1. w was old blank. It has an old occupied neighbour a in T0 union P0,
   distinct from v and q.
2. In the next column beyond w away from v, called z's column, either
   there is an old endpoint, or a site has an old occupied neighbour
   outside that column. All relevant sites are internal to the board.
3. The resulting original singleton is available under the standard outer
   boundary marks. No additional reservation of this unit is imposed.

There is no old-mate retention hypothesis.

**Lemma 1 (conditional singleton or BP).** In every such extension q is
blank and w cannot be selected. If w is a final endpoint, it is an actual
BP terminal adjacent to v. Otherwise w,q are BB and their original interval
is exactly the available singleton (band(w),col(w),col(w)), supported by
v's original owner.

**Proof.** Selected t already sees occupied v. Since q is another neighbour
of t, q is forced blank. If w were selected, it would see both v and a,
contradicting feasibility. Thus w is blank or an endpoint, proving the BP
alternative when occupied.

In the blank alternative, w's column is BB. Its neighbour on v's side is
TP, hence not TT. The other neighbour cannot be TT: an old endpoint is
retained P, or a selected pair would have both its within-column selected
neighbour and the distinct retained occupied external neighbour. Thus neither
adjacent column is TT. In the original BB--TT interval graph the BB vertex
is isolated, so its coordinate identity is the stated singleton, regardless
of changes to other intervals elsewhere. It is internal and unmarked.
Since v is its immediately adjacent TP, this singleton is a valid support
witness for v's owner. QED.

This uses the earlier local replacement mechanism, but activates it at a
**new endpoint with a new selected partner**, rather than just at the five
old retained TP tips. It produces a witness for a TP, not an independent
payment for each BP terminal. Whole-beta and mixed-owner accounting still
requires the global certificate lift.

## 2. The 27 conditional witnesses in the actual geometry

Use the actual 28-by-24, 49T/308P starting configuration of promotion closure.
The pairs below give source v -> conditional target w:

| Source v | Target w |
| --- | --- |
| (1,14) | (1,13) |
| (1,18) | (1,19) |
| (8,22), (9,22) | (8,21), (9,21), respectively |
| (10,1), (11,1) | (10,2), (11,2), respectively |
| (10,22), ..., (21,22) | (10,21), ..., (21,21), respectively |
| (16,10) | (16,11) |
| (17,8) | (17,7) |
| (17,10) | (17,11) |
| (19,9) | (19,8) |
| (21,13) | (21,12) |
| (21,14) | (21,13) |
| (24,13) | (24,12) |
| (24,14) | (24,13) |
| (24,15) | (24,14) |

This is a fixed set K of 27 sites; we do not claim it contains every possible
fresh TP or that it is optimal among all possible conditional witness rules.
A site is active only when it is actually TP in the final configuration.
A potential site's absence or infeasibility creates no resource or credit.

The [verifier](../develop/check_conditional_fresh_tip_closure.py) records an
explicit retained blocker and an old-endpoint or external occupied witness
for the no-TT condition for every row. For example:

* v=(19,9), w=(19,8): old P (20,8) forbids selecting w. In the outer column,
  old T (18,7) has an old occupied neighbour outside its column, preventing
  TT. Activation uses new T (18,9).
* v=(24,15), w=(24,14): old P (23,14) forbids selecting w. Old P (23,13)
  next to the outer column prevents TT. Activation uses new T (25,15).

These are finite audits of a specified starting geometry. Lemma 1 is the
proof for **every extension**, not an inference from finitely many extensions.

**Lemma 2 (simultaneous compatibility).** All active conditional targets
have distinct physical BP identities when occupied and distinct original
singleton identities when blank. They are disjoint from the old 18 BP
targets, old five flexible BP candidates/interval identities, and the
promotion target (3,13).

**Proof.** The 27 physical target sites are all different. Each is old blank,
whereas the 18 old BP targets and promotion target are old P. Direct comparison
with the five listed flexible sites excludes physical equality and equality
of their band/column interval coordinates.

The only pairs of entries whose target sites share a band/column have
sources that are each other's band partners. Such sources cannot both be
TP: one would require a site P while the other requires that same site T.
Thus two active blank targets cannot name the same singleton. This last
check is essential: different physical target sites alone would not prove
resource identity separation. QED.

For arbitrary n>=1, use the previous n-copy family B_n, translating each
entry by 24i columns for 0<=i<n. For n>1 retain the existing PP seam splice.
The new seam endpoint sites are outside all listed sources, targets and
old-blank band partners; all old occupied blockers remain occupied. The
same local arguments therefore apply. Target columns have residues between
2 and 21 modulo 24, so equality of target coordinates from different copies
forces the same copy. Equality with old five-unit or BP coordinates is
likewise excluded in the same copy. The 27n potential sites form K_n.

## 3. Stronger defect budget and exact certificate ledger

Let a,b be the final original alpha and beta counts. As before:

* p counts retained endpoints promoted to TP by a new selected partner;
* h counts occupied old flexible targets, with 0<=h<=5n;
* E is the set of final TP endpoints in P minus P0, e=card(E);
* G=E intersect K_n, g=card(G);
* q counts active conditional targets w in P, so 0<=q<=g;
* U=E minus K_n is the remaining hole set, u=e-g;
* s=card(T minus T0) is the number of newly selected vertices.

**Theorem 3 (conditional fresh-tip closure).** For every feasible retained-
T0/P0 extension of B_n, with arbitrary actual matching and a rectangle
retaining the band phase, there is a partial terminal certificate covering
exactly all TP tips outside U. It uses

    B = 18n+h+p+q                      different BP assignments,
    R = 5n-h+g-q                       different original interval assignments.

Each interval is used as a certificate target **once**, stronger than the
general allowance of two slots. The covered-tip count is exactly

    23n+p+g = B+R.                                           (1)

Select all B BP links as C. Let a_C,b_C be final alpha/beta counts after
these cancellations, and k the number of those final alpha paths whose
two free ends both belong to U. Then this displayed certificate pays
exactly a-k alphas, with distinct original units and no more than B links
before ordinary normalization. In particular

    ordinary true deficit <= k <= floor((e-g)/2)
                             <= floor((s-p-g)/2).             (2)

The full beta-fork deficit is no larger. The exact interval payment count
from this certificate is a_C-k and satisfies

    a_C-k <= min(R, floor((R+u)/2)).                          (3)

If u<=1, all original alphas are paid by an ordinary packing with at most
18n+h+p+q links. This allows arbitrarily many protected fresh tips: it is
not restricted to e<=1 or to one new selected vertex. If an extension has
only protected fresh TP sites, it is fully compensated for every actual M.

**Proof.** Start with promotion closure's old 23n+p tip assignments. Keep
its 18n+h+p distinct BP assignments and its 5n-h surviving original units.
For each active v in G apply Lemma 1, assigning it to the physical BP w if
occupied, and to its original singleton if blank. Lemma 2 proves all targets
are different, including their compatibility with the old targets. There
are exactly q new BP assignments and g-q new singleton assignments. This
proves (1) and injectivity. The only TP tips not covered are precisely U.

The selected BP links are a terminal matching; they may include a neutral
cycle and are not required to retain actual M edges. Every covered free TP
end after C has its distinct interval assignment. Any final alpha with at
least one covered end can therefore choose such an end's assigned interval.
No two final alphas choose the same resource, since all assignments are
injective and their free endpoints are disjoint. The k alphas with two
holes have no interval assignment in this displayed rule. Thus exactly
a_C-k final alphas are interval-paid, while 2k<=u.

Cancellation gives a+b_C=b+a_C, with b_C<=b. Its beta payments plus interval
payments are b-b_C+(a_C-k)=a-k. The existing subset normalization yields an
ordinary packing without increasing links or repeating beta/interval credit.
The remaining final alphas have 2a_C free TP ends; at most R are assigned
ends and at most u are holes. This gives 2a_C<=R+u, while each paid final
alpha uses one of the R distinct assignments, proving (3).

Distinct TP tips have distinct selected band partners. The e fresh tips
and p retained-P promotions have different such partners, all in T minus
T0 because old selections were saturated. Thus e+p<=s. Together with
2k<=e-g this proves both bounds in (2). If u<=1, k=0. QED.

The exact loss k is for the displayed certificate, not necessarily the
true optimal deficit. The extra units can also be shared in the full
owner-support network; constructing this particular injective certificate
is what makes the stated count safe across components.

**Concrete frozen all-n corollary.** In every copy add actual edges
((19,9),(19,10)) and ((24,15),(24,16)), and selections (18,9),(25,15)
and (2,14). This gives p=n, g=2n, h=2n, q=0 and u=0. The retained geometry
has 312n+4(n-1) endpoints and 52n selections; for n>1 the 4(n-1) term is
the existing PP seam. The theorem gives full ordinary compensation for
**every actual matching** on this occupation, with at most 21n links and
at most floor(5n/2) interval payments. The upper link bound is a certificate
bound, not claimed to be the optimal cost.

The displayed matching is completely frozen for every n: replay the old
B_n ranks and then freeze all four new endpoints per copy in a final layer.
The new endpoints (19,9),(24,15) each have their new selected partner plus
an old endpoint below/above as witnesses. The new BP endpoints (19,10)
and (24,16) each see two retained old P neighbours, respectively
{(19,11),(20,10)} and {(24,17),(23,16)}. All their old actual mates have
already frozen. Old actual matching edges retain their B_n mates. The new
selection (2,14) is feasible and only adds a witness to the old board.
Thus no finite-copy freezing inference is used. The old floor(e/2) budget
would only guarantee loss at most n; it does not assert that this displayed
matching actually suffers that old loss.

## 4. Relation to the remaining problem

The old coarse budget charged every fresh TP, including the two sites
(19,9) and (24,15) and many side-boundary sites. They are now individually
removed from the hole count whenever activated, with a proof covering all
future occupation changes and matching choices. This is a strict improvement
of the guaranteed budget whenever removing g changes the floor in (2).
It does not assert that the old bound was attained on every such occupation.

A separate permanent [328P/60T feasible nonfrozen example](../develop/fixtures/conditional_fresh_tip_old_pool_loss_nonfrozen.json)
does exhibit an actual improvement in the guaranteed resource pool. It has
11 fresh TP tips, all protected, and five occupied conditional BP targets.
The old five-unit pool has true ordinary deficit one; the enlarged
conditional certificate pool has deficit zero, both at minimum two links.
The complete unrestricted pool already had deficit zero. This demonstrates
repair of a failed old pool, not an unrestricted compensation counterexample.
Its matching is explicitly **not completely frozen**.

The [protected shared-column family](PROTECTED_SHARED_COLUMNS_AND_FRESH_ENDS.md)
still supplies a sharp frozen old-pool loss outside this protected footprint:
its new bands lie outside K_n. Full resources pay that family independently.
Thus protected closure does not eliminate the general residual problem.

The general fresh-tip separation lemma still implies that an unprotected
fresh TP cannot horizontally neighbour old P, so any actual retained/fresh
matching interface is transverse vertical. Separately, the universal vertical
TP injection leaves short horizontal mixed exceptions. Future work must
combine those restrictions and the existing mixed-gate/beta/interval cuts;
it cannot treat a matching-difference component as its own payment unit.

## 5. Verification and formal scope

The companion verifier checks every local witness, simultaneous source and
resource separation, all final TP/BP types, original singleton identities,
retained/promoted/fresh coverage, exact strategy loss, both budgets and
ordinary/full optima. Independent primitive enumeration is restricted to
small copy counts; the larger controls use the established exact flow
implementations. The all-n and arbitrary-extension claims are proved above.

Validation counts and concrete models are recorded in the
[receipt](../output/conditional-fresh-tip-closure-validation.json).
There are 2,573 models: 58 completely frozen and 2,515 feasible nonfrozen;
243 actual square rematchings, 82 target-occupation controls, 48 simultaneous
activation runs with up to 70 active protected fresh tips, and 92 independent
ordinary/full primitive comparisons on small systems. Eight PP-connected
frozen cap families have independent complete rank checks. Nine additional
frozen controls combine protected caps with genuinely unprotected new-band
alphas: their restricted deficit equals u/2 while full resources pay all.
The frozen one-copy cap fixture is a concise explicit
[occupation/matching extension](../develop/fixtures/conditional_fresh_tip_frozen_caps.json)
of the actual base, not merely P labels without actual edges.

[Lean source](../formal/SubQuorum/EndpointExtensionReplacement.lean), namespace
ConditionalFreshClosure, checks ten new scoped facts: activated target
protection, the literal 27-site guard geometry, target injection, the
band-partner collision property, separation from old targets/resources,
column bounds, incompatible activations, arbitrary-copy column injection,
certificate counts and the improved hole budget. The earlier 29 audits in
the same file are rerun. The interval extraction, complete all-n geometric
adapter, cancellation and packing lift remain written/Python proofs; this
is not an end-to-end formalization of Theorem 3.

Run from root:

    PYTHONDONTWRITEBYTECODE=1 python3 develop/check_conditional_fresh_tip_closure.py --output output/conditional-fresh-tip-closure-validation.json

Run from formal with Lean 4.33.0:

    lean SubQuorum/EndpointExtensionReplacement.lean

No submitted manuscript or correspondence is changed.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.

## Fixed-domain continuation

[Residual fresh-tip domains](RESIDUAL_FRESH_DOMAINS.md) closes the remaining
holes under the additional hypothesis that the rectangle remains exactly
28-by-24: all feasible extensions have displayed loss at most one, and every
minimum-occupied-degree-three (in particular completely frozen) extension is
fully paid. The proof removes untouched mixed owners and uses path colors;
it adds no resource credit. This conclusion is NOT asserted for arbitrary
rectangle extensions or the internal boundaries of horizontal copies.
