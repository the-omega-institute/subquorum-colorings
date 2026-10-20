# Counting marked-side owners' matching costs improves the uniform bound

20 October 2026. In the entire permitted finite complete U/rotor model,
the matching coefficient improves from12/13 to14/15. If every actual
double-marked positive is nonexceptional, the coefficient improves from
17/18 to21/22. The corrected improvement counts the matching cost of the
original negative U owners assigned marked positive sides. It uses
the existing two-slot compensation theorem and exact source ledger,
not a new defect injection or an arbitrary-grid decomposition. The newer
MARKED_SIDE_MATCHING_BUDGET.md proves stronger33/35 and26/27 coefficients.
This note originally conflated marked sides G with negative original charge S;
the replacement bridge in Section2 is essential. The original review and
formal arithmetic were conditional on that previously unjustified bridge.

## 1. Exact hypotheses and conclusion

Keep every hypothesis of COMPLETE_SOURCE_UNIFORM_COEFFICIENT.md:
finite complete U/rotor sources with arbitrary permitted dimensions,
phases, translations and isometries; pairwise disjoint original endpoint
sets and unchanged matchings; retention of every original support outside
their union P; final selected occupied degree at most one; and the same
ambient even-by-even rectangle/source-ledger assumptions. In particular

    sigma=mn/2-|T|-|M| >= mu=N+R-G,
    mu>=n0-e-floor(s/2), R>=0,
    2R=A+U0+Z0+H, A>=s.

N counts ALL positive charge-one U sources. G counts marked original
canonical positive sides. The sum S of absolute original negative charges
is a DIFFERENT quantity, entering reserve R=S+C-Kirregular. No rotor owns
a marked-side assignment. e counts actual exceptional double-marked positives;
s counts nonexceptional doubles with exactly one activated terminal.
They are disjoint positive-source lists, so N>=e+s. Other one-mark and
unmarked positives remain unrestricted. Nonexceptional dimensions are
width6 with arbitrary permitted heights, or width8/10 with both heights4/6.

Then EVERY such complete-source fusion satisfies

    |T|+(14/15)|M| <= mn/2.                       (1)

If e=0, the stronger statement is

    |T|+(21/22)|M| <= mn/2.                       (2)

The e=0 condition only restricts actual DOUBLE-MARKED positives; it does
not restrict one-mark or unmarked positive dimensions. Neither coefficient
is claimed sharp. Coefficient one and arbitrary-grid triple equality remain
OPEN. Relative to5/6 on the same configurations, the gains are |M|/10
and4|M|/33, respectively. The gains over12/13 and17/18 are2|M|/195
and|M|/99, respectively.

## 2. Every marked side has an original negative U owner

An original U(w,a,b) has matching size

    m=w+(a+b)/2-1, w>=6, a,b>=4.

Every positive U has m>=9, and each positive counted by e has m>=13.
Thus all positive original matchings together cost at least9N+4e.
The established all-phase marked-side assignment injects actual marked
sides into original endpoints of negative U sources. A phase01 source has
at most two eligible upper corners, phase10 at most two terminal tips,
and phase11 at most those four endpoints. Rotor owners are excluded.
If B is the negative U count and Mneg their original matching size, then

    G<=4B, Mneg>=9B, hence 9G<=4Mneg and Mneg>=G.

This is a matching-size argument counted ONCE per original source. It
does not identify negative original charge with marked sides, and does
not spend a geometric defect or an activation a second time.
Original endpoint disjointness and unchanged matching ownership give

    |M|>=9N+4e+G
       =10N+4e+R-mu.                             (3)

G in(3) is the actual marked-side count used in mu=N+R-G. Original
matching ownership, rather than a charge identification, supplies its
cost. The stronger9G<=4Mneg budget is used in the newer note.

## 3. Universal coefficient fourteen-fifteenths

If mu>=0, sigma>=0 immediately implies(1). Otherwise put ell=-mu>0.
The compensation theorem and n0>=0 give

    ell<=e+floor(s/2)<=e+s/2.

By N>=e+s and R>=0, equation(3) gives

    |M|>=14e+10s+R+ell
         >=14(e+s/2)+ell
         >=15ell.

Hence mu>=-|M|/15 and sigma>=-|M|/15. Substituting sigma proves(1),
equivalently the integer inequality30|T|+28|M|<=15mn.

## 4. Nonexceptional coefficient twenty-one-twenty-seconds

When e=0 and mu<0, compensation gives ell<=floor(s/2). Thus
s>=2ell. The exact defect identity also gives2R>=A>=s, hence R>=ell.
Equation(3), now with N>=s, yields

    |M|>=10N+R+ell>=10s+R+ell>=22ell.

The mu>=0 case is immediate as before. Therefore sigma>=-|M|/22,
which proves(2), or44|T|+42|M|<=22mn.

All activation and defect occurrences are used only through the existing
scalar inequalities. Original matching edges provide a separate size
budget: none is a defect-slot payment, and no old compensation resource
is assigned again. The argument permits shared negative sources and
arbitrary contact graphs. It does not count one negative source once
for each incident positive; it sums its original matching and charge ONCE.

## 5. Verification scope and remaining target

formal/SubQuorum/CompleteSourceCoefficient.lean adds six declarations:
the negative U matching-cost inequality, the exact combined budget,
both scaled-slack deductions, and both integer boundary conversions.
The physical source-charge formulas, ownership partition and existing
compensation theorem remain written dependencies. The scaled-slack
lemmas permit arbitrary finite counts and signed mu/sigma, with no
dimension cutoff or finite enumeration in their proofs.

develop/check_charge_aware_source_coefficient.py independently reconstructs
representative U phases and rotor charges/matching sizes and checks
the signed arithmetic budgets. These finite controls supplement the proof.
No new complete physical-fusion fixture is claimed. The main research
target remains finite closure or a complete feasible obstruction for
the remaining coupled width-six staircases, then the unrestricted model
and the required connection to arbitrary rectangular grids.

All six new declarations pass local Lean4.33.0 source checking, object
build and individual axiom audits using only propext and Quot.sound,
without sorry/native_decide. The complete file now has thirteen compiling
declarations. Controls pass1216 U images (912 negative/304 positive),32
rotor images,83583 signed universal budgets (37908 negative margins)
and4602 nonexceptional budgets.
See output/charge-aware-source-coefficient-formal-check.json and
output/charge-aware-source-coefficient-controls.json.
Historical independent audit a20e87ca completed ACCEPT at2026-10-20T05:51:15.164UTC,
observed gpt_6/pro,5073characters. Original stream32411 exits0/DONE and
exactly matches the terminal response. Its supplied inputs mislabeled G
as original negative charge while also supplying mu=N+R-G. Thus that
verdict supports conditional arithmetic, not the missing physical bridge.
Section2 now supplies a different bridge from the existing actual side
assignment; the newer note's independent audit is separate. The original
source/charge controls and signed budgets did not verify G=S and must
not be presented as doing so. New controls reconstruct actual marked
assignments and keep G,S separate. No arbitrary-grid decomposition follows.
See output/charge-aware-source-coefficient-review.json.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
