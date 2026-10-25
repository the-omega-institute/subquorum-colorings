# Endpoint additions and rematching: guarded local replacement preserves full compensation

25 October 2026. Haobo Ma and Wenlin Zhang. Isolated research branch.

The [fixed-occupation certificate](OCCUPANCY_CERTIFICATE_AND_ALL_REMATCHINGS.md)
settled every perfect matching of exactly the old endpoint set. We now allow
arbitrarily many new endpoints, arbitrary simultaneous rematching of old and
new endpoints, and a larger rectangle. The selected set T is kept EXACTLY
fixed. The resulting board need only be feasible; complete freezing and
retention of old actual matching edges are unnecessary.

For this actual 49-selected/308-old-endpoint geometry, ALL such extensions
have full ordinary compensation. An adaptive certificate uses 18+h physical
BP targets and 5-h different final original intervals, where h is the number
of five specified candidate sites occupied by new endpoints. Its interval
payments number at most floor((5-h)/2). If at least four candidates are
occupied, beta resources alone suffice, regardless of final rematching.

This is a general proof over all such extensions, not a bounded-extension
search. Additional selected sites are outside its scope; the universal grid
compensation statement and 5/6 improvement remain open.

## 1. Extension hypotheses and the useful saturated-selection fact

Use the original 28-by-24 mixed-cycle geometry, selected set T0 of size 49
and endpoint set P0 of size 308. A final finite rectangle contains it in the
same aligned two-row phase. Even translations are permitted. Its endpoint
set P contains P0 and is disjoint from T=T0. M is ANY actual grid perfect
matching of P. Each selected site has at most one occupied neighbour in T
union P; use the final rectangle's standard admissible boundary convention.
No old matching edge is prescribed, and no final freezing assumption is made.

**Saturation fact.** Every one of the 49 original selections has exactly one
neighbour in T0 union P0. These neighbours remain occupied in every extension.
Consequently every other neighbour of every selected site stays blank.
In particular no NEW endpoint can have a selected band partner: it would be
a second occupied neighbour of that selection. The set of physical TPs stays
EXACTLY the same 23 old TPs. This holds even for endpoints outside the old
rectangle, and does not follow merely from keeping T fixed on an arbitrary
unsaturated starting board.

The matching can nevertheless alter all whole-owner paths and their terminal
pairing. New endpoints can change BP counts and create arbitrarily long
paths; no persistence of old alpha/beta identities is assumed.

## 2. A local replacement that is valid before choosing M

Let v be an old TP, t its selected band partner, and let u be horizontally
adjacent to v. Let q be the band partner of u; it is horizontally adjacent
to t. Since t already sees retained occupied v, q is permanently blank.
The following rules use this same selected guard.

* If u was an old BP, it remains an endpoint with a blank partner q. Thus
  v->u remains a permitted physical link under every extension/rematching.
* Suppose u,q were a BB column. Choose its eligible singleton original unit.
  T is fixed, so u cannot become selected. Either u remains blank and that
  unit remains available, or u becomes a new endpoint, with q still blank.
  In the second case u is a physical BP and v->u is a permitted link.

For the singleton persistence assertion, its column is strictly internal
and neither adjacent column is TT. As T is fixed, no new TT can appear.
If the column remains BB, its BB--TT component therefore remains the same
unmarked singleton. Changes elsewhere do not merge it into a boundary unit.
When u is occupied, the old unit is removed; it is NOT also retained as a
payment resource. The replacement is a BP ENTRANCE, not an additional beta
credit. Only the final cancellation/payment ledger produces beta payments.

This rule needs immediate horizontal adjacency. An arbitrary interval behind
a BT corridor does not have the same direct BP replacement. Accordingly we
replace the preceding certificate's (band6,col12) choice by the immediately
adjacent (band6,col15) unit for TP (12,14). The other four choices are unchanged.

## 3. All simultaneous replacements are disjoint

Keep the 18 fixed BP assignments listed in the preceding occupation note.
For the five remaining TPs use:

| Old TP v | Candidate u | Permanently blank q | Unit if u is blank |
| --- | --- | --- | --- |
| (12,14) | (12,15) | (13,15) | (6,15) |
| (14,11) | (14,10) | (15,10) | (7,10) |
| (19,11) | (19,10) | (18,10) | (9,10) |
| (24,6) | (24,7) | (25,7) | (12,7) |
| (24,17) | (24,16) | (25,16) | (12,16) |

All five candidate sites were blank and are different. Thus any newly used
BP target is distinct from the 18 old endpoint targets and from every other
new target. All surviving singleton units are different. BP and interval
targets are different target types. The sources are the 23 different old
TPs, with no new TP by Section 1. This proves a complete injective physical
certificate for the FINAL board, regardless of its actual matching.

Write h for the number of these five candidates in P. The certificate has

    selected links = 18+h,
    assigned different final original intervals = r = 5-h,
    total assigned physical TP sources = 23.                 (1)

The eligible interval IDs may be renumbered in the final board. All statements
refer to the coordinate singleton identities in the FINAL original network.
Any additional reservations are permitted provided they exclude the surviving
5-h specified units. No other interval resource is required.

## 4. Universal extension theorem and quantitative interval budget

**Theorem.** For every extension of Section 1 and every final available pool
Q containing the surviving units of Section 3,

    V_ord = V_full = a,
    c_full <= c_ord <= 18+h,                                (2)

where a is the FINAL original alpha count. There is an ordinary full payment
using at most

    floor((5-h)/2) different original interval units.          (3)

In particular, if h>=4, even Q empty has full beta-only ordinary compensation.
The identities of the intervals actually used may depend on M; (3) is not
a claim that an arbitrary subset of that many surviving units always suffices.

**Proof.** Select all 18+h BP assignments as a terminal matching C. Section 3
establishes compatibility globally, including all new endpoints. Every TP
remaining free after C must be interval-assigned; all other TPs were used by
C. There are exactly r such free TPs. Each final alpha path has TWO different
free TP ends; final mixed paths have one, while cycles have none. Therefore

    2 aC <= r = 5-h,                                        (4)

where aC is the post-cancellation alpha count. Choose one free TP from each
final alpha and pay it with its assigned interval. Global target injection
makes these aC original units different, and their physical witnesses remain
on the corresponding final path. Thus at most floor(r/2) units are needed.
Unused assignments, including those on mixed paths, are not payments.

Let b be the FINAL original beta count and bC the count after C. The exact
signed endpoint ledger gives

    a+bC=b+aC,        bC<=b,
    payment = b-bC+aC = a.                                 (5)

Normalize to ordinary disjoint stems using a subset of C, as in the established
partial-certificate theorem. It preserves the payments without increasing
links or interval use. This proves (2)--(3). The full model contains ordinary
packings and can never pay more than a, so it has the same value and no larger
minimum cost. If h>=4, then r<=1 and (4) forces aC=0. Equation (5) then uses
only original beta credits. QED.

All inequalities hold under arbitrary simultaneous new endpoint additions;
there is no sequential-freezing induction. Old matching components can merge
and new matching edges can connect occupied bands. The argument tracks final
free ends and final original resources instead of assuming old private
ownership or prepaying a historically chosen beta.

## 5. Relation to the general geometric criterion

The proof applies to any feasible starting occupation satisfying:

1. Every retained selection has a retained old occupied neighbour, and no
   additional selection is allowed.
2. All old physical TPs admit an injective cover by old horizontal BP targets
   and immediately adjacent, eligible internal BB singleton columns.
3. The candidate BB columns are different, and their adjacent columns are
   not TT, so unchanged selections keep surviving units singleton/unmarked.

For m fixed BP assignments and r0 flexible unit assignments, the same proof
gives m+h links, r0-h surviving assigned units, at most floor((r0-h)/2)
interval payments and full compensation for every arbitrary endpoint extension
and rematching of this class. This is an occupation criterion, not a universal
consequence of complete freezing. The partial-certificate sufficiency itself
was already established; the new geometric step is preservation by guarded
unit-to-entrance substitution with no new TP demands.

If new selections are allowed, they can give new TP ends and can change a
surviving interval's BB--TT component. The old selected guards still constrain
some positions, but the full-TP cover proof no longer applies automatically.
Those new demands and interval changes must enter the joint accounting.

## 6. Verification and honest freezing labels

All 435 extension/rematching models pass the same adaptive certificate and
restricted ordinary/full flow comparison, with 136 independent primitive-pack
comparisons. They include all 32 requested fill subsets, 192 subsequent
old/new rematching controls, 191 feasible single new matching-edge additions,
and 20 larger-rectangle controls. Actual h is recomputed, not assumed from
the requested subset. Every h from zero to five occurs.

Seven models are completely frozen and 428 are feasible nonfrozen. The actual
one-target (12,15) extension is a 310-endpoint completely frozen example.
The saved all-five example has 318 endpoints, is explicitly NONFROZEN, and
has beta-only full value four at minimum cost four. It is a control for the
stronger feasibility theorem, not a claimed frozen construction. No inference
that every fill subset has a frozen realization is made.

The written proof covers arbitrary many additions and arbitrary matchings;
finite controls are not an exhaustion of this extension class. The Lean file
checks the general selected guard, no-new-TP saturation lemma, local two-state
replacement and simultaneous target injection, plus the interval budget,
four-fill beta-only arithmetic and ledger. Concrete audits cover all 49
saturated selections, the 23 selected guards, disjoint target data and the
five internal singleton guard columns. Physical arbitrary-M path decomposition,
final interval-forest adapter and ordinary normal-form lift remain written/
Python, not an end-to-end Lean extension theorem. Validation receipts give the
final exits, axioms, machine scope and exact counts.

The next research scope is extensions with NEW selections or occupations
without such a guarded cover. These can create genuine new TP demand while
altering interval resources. The universal grid compensation and 5/6 target
remain open.

All eleven local Lean 4.33.0 audited declarations passed with exit zero,
using only propext/Quot.sound where needed and no sorry/native evaluation.
Four declarations are axiom-free. See the
[formal receipt](../output/endpoint-extension-replacement-formal-check.json),
[computational receipt](../output/endpoint-extension-replacement-validation.json)
and [direct Lean source](../formal/SubQuorum/EndpointExtensionReplacement.lean).
The [310P positive fixture](../develop/fixtures/endpoint_extension_one_target_frozen.json)
has an independently checked complete rank certificate; its freezing is not
claimed as a new Lean theorem.
