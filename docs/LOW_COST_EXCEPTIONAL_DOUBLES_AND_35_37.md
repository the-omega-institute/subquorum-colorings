# A low-cost double obstruction and the coefficient 35/37

22 October 2026. Authors: Haobo Ma and Wenlin Zhang.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.

## Scope and results

Use the finite COMPLETE immutable full-even-U/standard-rotor source model,
all allowed phases and lattice isometries, endpoint-disjoint originals, their
unchanged matchings, and mandatory retention of every unconsumed original
support. U widths are even w>=6 and independent leg heights are even a,b>=4.
Retain the existing representative/source ledger in an even-by-even rectangle:

    sigma=mn/2-|T_sel|-|M| >= mu=N+R-G,
    R>=0,    2R=A+U0+Z0+H.

N counts original positive sources, G ACTUAL marked canonical sides and A
activated original positive terminal occurrences. R is the event reserve,
not original negative charge. The complete gate-role catalogue, blank-gate
two-slot theorem and old occupied-witness injection are dependencies below.
No decomposition of arbitrary rectangular-grid representatives is asserted.

We prove a new obstruction for U(8,4,8), and by reflection U(8,8,4): a
double-marked positive with both original terminal occurrences unactivated
cannot have both canonical gate corners occupied. Consequently the existing
two-slot compensation theorem extends to these two additional dimensions.
All remaining exceptional positives have at least14 original matching edges,
instead of the previous threshold13. This improves the matching coefficient
from33/35 to35/37 for EVERY complete-source fusion under the stated ledger:

    |T_sel|+(35/37)|M| <= mn/2,
    equivalently 74|T_sel|+70|M| <= 37mn.             (1)

This improves by4|M|/1295 over33/35 and25|M|/222 over5/6, strictly for |M|>0, on
the SAME admitted configurations. No sharpness of35/37 is asserted.

## The two occupied gates cannot coexist without activation

Normalize the positive producer to U(8,4,8), with its bar at rows0,1 and
legs in columns1,8. The left/right canonical gate corners are (2,2),(2,7).
The corresponding original positive terminal tiles are unactivated precisely
when neither of their original intratile supports is consumed. In particular
the beyond-tip supports (5,1),(9,8) remain selected. Their original anchors
are (4,1),(8,8); selected occupied degree one forces

    (5,2) and (9,7) finally blank.                    (2)

Every original endpoint AND support is finally occupied, whether a support
is retained or consumed. Thus no original occupied set can contain either
point in (2). We assume both gate corners occupied and derive a contradiction.

Use the accepted all-parameter occupied-gate catalogue in
OCCUPIED_GATE_ACTIVATION_AND_WIDTH_SIX.md: the owner at a normalized occupied
left gate is a phase01 upper corner, a phase10 terminal, or one of the two
phase11 terminal forms. Rotors and positive owners are excluded at this gate
corner. This gate is different from the fixed original support at (3,2)
whose consumption characterizes marking. Phase10 forces the corresponding
positive terminal activated, so cannot occur on either side here.

At the LEFT gate, either orientation of a phase01 corner has endpoints in
column2 from row2 through at least row6: its downward near leg has height>=4,
or its downward bar has width>=6. It contains (5,2), contradicting (2).
A longitudinal phase11 tip has a downward stem from row2 through h+2,
h>=4, and also contains (5,2). Therefore the left owner L must be the
transverse phase11 tip, whose predecessor goes right and whose bar goes down.

Write v>=6 for its breadth, h>=4 for its incident leg and e>=4 for its
other leg, all even. Its exact chart from the canonical U(v,h,e) is

    (r,c) -> (c+1,h+2-r).

Its near stem runs along row2, columns2 through h+2. The positive producer
already owns (2,8), so h+2<8; evenness gives h=4. Consequently L has

    {(r,c): 2<=r<=v+1, c in {5,6}} as its bar, v>=6. (3)

and has no endpoint in a column greater than6. In particular it does not
own the right gate (2,7); the right owner is a different original.

Reflect the same gate catalogue into the RIGHT gate. A phase01 corner in
either orientation contains (2,6), as does every transverse phase11 tip.
But L already owns (2,6), so original endpoint disjointness excludes them.
Only a longitudinal phase11 tip remains. If its incident leg is k>=4,
its stem contains column7, rows2 through k+2. The forbidden point (9,7)
and evenness force k in {4,6}. Its bar has rows k+1,k+2 and extends left
from column7 by a breadth at least6. Hence it contains

    (k+1,6), with k+1 in {5,7}.                     (4)

Both alternatives belong to L's bar (3), since v+1>=7. The two originals
therefore own the SAME original endpoint at (5,6) or (7,6), contradicting
original endpoint disjointness. The other incident and far leg lengths
were unrestricted throughout. Reflection in column9-c proves the exchanged
positive dimensions, and tiling-preserving isometries transport the proof.
This is an arbitrary-dimension obstruction, not a finite role search.

## Extend the compensation class without reusing any slot

Call an actual double compensated if its positive dimensions belong to C*:

- w=6, with arbitrary legal a,b;
- w in {8,10}, with a,b in {4,6};
- w=8, with {a,b}={4,8}.

Let z,s,t count actual compensated doubles with zero, one or two activated
terminal occurrences. Let e count all other ACTUAL doubles. Let n0 be the
number of unmarked positives; one-mark positives remain unrestricted.

The existing universal blank-gate theorem assigns TWO actual nonfull defect
slots to every blank canonical marked tile. Distinct such tiles are disjoint.
For the original class, every zero-activation double with both gates occupied
has the two original forced witness tiles, distinct across producers and
disjoint from EVERY blank canonical marked tile. The proof is in
TWO_SLOT_COMPENSATION_FOR_UNACTIVATED_DOUBLES.md, Sections2--5.

Every zero-activation double newly added to C* has a blank gate by the new
obstruction. It therefore uses one blank canonical tile's two slots. Assign
one such tile to each zero-activation double having a blank gate; the source
and side labels are injective into PHYSICAL tiles by the inherited global
canonical donor-tile theorem. Let Bzero be this pool of compensated
zero-activation doubles with a blank gate and Cocc its complement, so
z=|Bzero|+|Cocc|. The remaining zero-activation doubles
are in the old class with both gates occupied and use their old distinct
witness tiles. These two pools are physically disjoint by the inherited
cross-type injection. Thus, in the SAME exact defect pool,

    H>=2z,    A>=s+2t,
    2R>=2z+s+2t.                                    (5)

No extra use of A, full-tile credit or original source charge is made.
If n1 counts one-mark positives, N=n0+n1+z+s+t+e and
G=n1+2(z+s+t+e), so G-N=(z+s+t+e)-n0. Because R is integer, (5) yields

    mu=n0+R-z-s-t-e >= n0-e-floor(s/2).              (6)

In particular e+floor(s/2)<=n0 still suffices for coefficient one, now on
the expanded class. The previous26/27 theorem also applies whenever e=0,
with this expanded definition. It still uses R>=s/2 and the existing marked
matching budget; its arithmetic is unchanged. Unmarked and one-mark sources
of dimensions outside C* have no restriction.

## The improved matching budget and coefficient

A positive U(w,a,b) has original matching size m=w+(a+b)/2-1>=9. If it is
outside C*, its matching has at least14 edges. Indeed, suppose m<=13.
If w=6 it is already in C*. If w>=12 then m>=15, impossible. For w=10,
m<=13 forces a=b=4. For w=8, m<=13 forces a+b<=12. Either both heights
are in {4,6}, or their unordered pair is {4,8}. These are precisely the
remaining possibilities in C*. All cases are exact integer inequalities.

Consequently all original positive matchings together have

    Mplus>=9N+5e.                                   (7)

The established marked-side assignment counts original endpoints injectively.
Negative U phases01/10/11 supply at most2/2/4 slots, each negative U has at
least9 matching edges, and rotors own no assigned marked-side endpoint.
Hence 9G<=4Mminus, independently of the defect pool in (5). Positive and
negative original matchings are disjoint, so

    4|M|>=36N+20e+9G
          =45N+20e+9R-9mu.                         (8)

If mu>=0, coefficient one already holds. Otherwise put ell=-mu>0. From
(6), ell<=e+s/2, while N>=e+s and R>=0. Apply these to (8):

    4|M|>=65e+45s+9R+9ell
           >=65(e+s/2)+9ell
           >=74ell.

Therefore sigma>=mu>=-2|M|/37, proving (1). This counts each original
matching once and each marked side once; (7)--(8) are size constraints,
not a second pool of geometric compensation. The scalar census
N=e=2,s=R=0,G=4,mu=-2,|M|=37 saturates these supplied inequalities. It
is NOT a complete physical realization or a geometric sharpness example.

## Validation scope

The companion checker exercises exact original endpoint/support masks for
all anchored catalogue roles in its dimension library, including long unequal
legs, the forced left form and the stated right collision points. These are
finite controls of the general proof, not an unbounded search proof. It also
checks the matching-size classification, the new conditional arithmetic and
complete physical fusions with actual degree-based marks and original-owner
matching partitions. Any absence of newly covered double shapes in complete
fixtures is reported explicitly rather than presented as exercised coverage.

The scoped Lean source formal/SubQuorum/LowCostExceptionalDoubles.lean checks
universal coordinate collision inequalities, exact low-matching dimension
classification, the compensation arithmetic, the improved matching budget and
coefficient. Complete role normalization, physical single-use injections and
the source-to-grid ledger remain written/dependencies. This is not end-to-end
Lean verification of arbitrary source fusions or a universal grid theorem.

Local validation PASS:323distinct-owner role collisions,2584symmetry collision
images,2548positive dimension controls,704complete physical images (72marked),
and19691signed budgets (2515negative margins). The physical fixtures contain
16singly marked positive occurrences but ZERO newly compensated double shapes.
The newly covered branch relies on the general proof and source-role masks;
it is not presented as a completed physical example.

All15scoped Lean theorems and16individual declaration axiom audits passed on
the user-selected local Mac, with50percent free memory and no real lean/lake
before the final invocation. No warning, error, sorry or native evaluation
occurs; only ordinary propext, Classical.choice and Quot.sound axioms or none.
Independent audit43ac52be-e334-492c-9794-7bd17b5c31ad completed ACCEPT at
05:12:20UTC, observed gpt_6/pro, 11648 characters. Original prompt matches
the session; original stream38214 ended DONE and its response exactly matches
the task and session. The audit accepts the written proof under the explicit
gate catalogue, physical two-slot injection and marked-side budget dependencies;
it did not execute code or Lean. Its coordinate, source-census, physical-pool
and strictness clarifications are incorporated above. See
output/35-37-and-mark-excess-independent-reviews.json and
output/low-cost-exceptional-35-37-validation.json for commands and scope.
