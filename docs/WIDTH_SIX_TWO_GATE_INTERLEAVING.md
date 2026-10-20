# Width-six gate interleaving and height gaps at most four

20 October 2026. Complete width-six positive sources whose two even leg
heights differ by at most four satisfy the joint allocation at every
reserve, with arbitrarily many sources and unrestricted negative U/rotor
dimensions and phases. The new step pays a single-activation double from
one actual forced defect tile, in addition to its own activation. The
same witness exclusivity joins this payment to the earlier two-slot pool.
The remaining connected A+A candidate requires larger width-six height
gaps, or transverse unactivated gates at the short width-eight/ten sources.
Unrestricted mixed allocation and arbitrary-grid equality remain open.

## 1. Complete-source assumptions and counts

Use the unchanged finite complete U/rotor model: disjoint original
endpoint sets, original endpoint/matching unions P,M, retention of every
original support outside P, and final selected occupied degree at most
one. Each U has even width at least six and independent even heights at
least four. Original ownership is never reassigned. All lattice isometries
and translations are allowed. Keep actual canonical marks, not a relaxed
endpoint mask. The exact source ledger and defect identity are

    sigma >= n0+R-n2,
    R=S+C-Kirregular is a nonnegative integer,
    2R=A+U0+Z0+H,
    H=L1+2L2bar+2L2mutual+L3.

Nonexceptional positive sources have width6 at arbitrary allowed heights,
or width8/10 with both heights in{4,6}. As before z,s,t count their actual
double-marked sources with zero/one/two activated terminal occurrences;
e counts actual exceptional doubles and n0 counts all unmarked positives.

Call a nonexceptional single-activation double paid here if either it has
a blank-gate mark, or its unactivated side has an occupied longitudinal
phase11 gate of incident height exactly its positive height minus two.
Let r count these sources, once per source, so 0<=r<=s. Then

    H >= 2z+r,
    2R >= 2z+s+2t+r,
    sigma >= n0-e-floor((s-r)/2).                 (1)

Consequently e+floor((s-r)/2)<=n0 suffices at every reserve. The geometric
definition of r determines an actual injection before the inequality;
it does not round one unit of defect separately for each demand.

## 2. There are no width-six blank-gate marks

The accepted complete-source blank-gate rigidity theorem makes any
blank marked canonical tile exactly an original phase11 upper-corner
2P0T pair. Normalize a left side by

    u=(2,2), x=(3,2), zeta=(2,3), y=(3,3),
    positive anchor (3,1), positive protector (1,3).

The accepted pointwise X_i argument identifies each occupied x or zeta
as its owner's A_i upper corner after excluding the F_i terminal role.
Thus x or zeta itself is the corner; y is not an additional corner case.

The pair is either{x,y} or{zeta,y}, and its other two corners are not
original endpoints of that owner. If the upper corner is x, its bar must
run right and its near stem down: the blank u excludes the other signs.
Its complete bar contains{(3,c):2<=c<=v+1}, v>=6. This contains the
positive endpoint(3,6), since the opposite positive height is at least4.

If the upper corner is zeta, its bar runs down and its near stem right.
The near stem contains{(2,c):3<=c<=h+3}, h>=4. This contains the positive
endpoint(2,6). Both contradict original endpoint disjointness. Reflection
gives the right side. Thus every actual width-six mark has an occupied gate.
The argument applies to every source, independently of other sources and R.

## 3. Two occupied gates interleave their incident heights

Take a doubly marked width-six U(6,a,b) whose left terminal is unactivated.
Its retained beyond-tip support(a+1,1) forces(a+1,2) finally blank, hence
outside every original endpoint and support set. The complete occupied-
gate catalogue and the width-six footprint exclusion leave one left role:
a phase11 terminal at u=(2,2), predecessor down, bar right. Let its
incident height be h>=4 and its width v>=6. Its original near stem and bar are

    stem: column2, rows2,...,h+2,
    bar: rows h+1,h+2, columns2,...,v+1.

Blankness beside the retained positive tip gives h<=a-2. The bar reaches
positive column6, so endpoint disjointness from the opposite leg gives
h>=b. These facts alone do not yet force a tight height.

At the right gate(2,5), the width-six catalogue again leaves a terminal
whose predecessor is down; let its incident height be k>=4. Its near
stem is column5, rows2,...,k+2. The two gates cannot have one original
owner. Two terminal roles of one U have displacement(k'-h',v'-1) in
reference coordinates; making the displacement horizontal by a signed
coordinate permutation forces h'=k' and distance v'-1>=5. The gate
distance is3. A corner owner is already excluded at width six.

The two distinct original owners cannot share(h+1,5). The left bar
contains this point, so it is outside the right stem. Therefore

    k+2 < h+1, hence k<=h-2.                       (2)

If the right owner were phase11, its bar would extend left from column5
through positive column1 in rows k+1,k+2. But k<=h-2<=a-4, so(k+1,1)
is an original positive endpoint. This is impossible. The right owner is
phase10 and its bar extends right. Avoiding positive column6 in the same
two rows gives k>=b, as also follows from its existing activation proof.
It activates the right positive terminal. We have proved the general
width-six two-gate implication

    b <= k <= h-2 <= a-4.                          (3)

In particular an unactivated side is the longer side, by at least four.
If a-b<=4, equality forces

    a=b+4, h=a-2=b+2, k=b.                         (4)

Thus height differences0 or2 force both terminal occurrences activated
on every double. Difference4 permits only the tight form(4) when exactly
one is activated. No zero-reserve or full-tile hypothesis entered this proof.

## 4. A tight longitudinal gate forces an exclusive defect tile

This local lemma holds for ANY positive width and height. Suppose an
unactivated positive side has height a and its occupied longitudinal
phase11 gate has incident h=a-2. The incoming original bar corner tile is

    Q={a,a+1} x {2,3},
    p=(a,2), t=(a,3), q=(a+1,2).

Its original profile is exactly{p,t},2P0T, without original support.
The positive also has no original support in Q at arbitrary height:
its terminal z=(a,1) already has predecessor(a-1,1) and its prescribed
supports(a,0),(a+1,1), so p=(a,2) cannot be another original support.
The other three corners of Q have no adjacent original positive endpoint;
the opposite leg is in column w>=6 and the positive bar is in rows0,1.
Unique original endpoint anchoring excludes their being positive supports.
The positive's retained tip support(a+1,1) makes q finally blank.
The fourth corner is blank or a foreign endpoint: a finally selected
support there would need an original anchor, which either differs from t
and gives two occupied neighbors, or equals t and identifies its owner
with the original pair owner, which has no support in Q. Hence Q is an
actual L2bar or L3 tile and supplies at least one unit of H.

The local data after translating p to(0,0) are exactly those in the
earlier short-leg injection: original pair p=(0,0),t=(0,1), same-owner
endpoints(-1,0),(-1,1),(0,2), positive endpoint z=(0,-1), blank q=(1,0).
These data do not depend on the incident height being four. Within the
original incoming owner, p has endpoint degree two and t degree three.
Thus the pair reconstructs its corner, bar direction and positive
endpoint z=p-(t-p). Two forced constructions using one tile must therefore
come from the same positive source. This remains true across different
positive widths and heights and across zero/single activation classes.

The earlier eight canonical orientations also exclude Q from EVERY
blank-gate canonical tile: its blank corner cannot be an original support;
negative-owned exterior anchors identify an impossible pair-owner support;
the remaining positive anchor/protector identifies this positive, which
has no original support in Q. Translation does not change any of these
eight exclusions. Hence a tight witness cannot also pay another source
or be spent as a blank-gate tile.

## 5. One common pool, and the width-six theorem

Select all witnesses simultaneously. Each zero-activation nonexceptional
double takes two slots by the accepted two-slot proof: both slots of one
blank canonical L2bar tile, or one slot from each of its two forced tiles.
Each of the r single-activation doubles takes one slot from its own blank
canonical tile if available, otherwise one slot from its tight forced tile.

Canonical tile distinctness handles all blank choices, including different
classes of positives. Section4 makes every forced tile exclusive to its
positive, and excludes every forced/blank coincidence. A positive cannot
belong both to the zero-activation and single-activation classes. The two
forced tiles of a zero-activation source are distinct. Thus this constructs
2z+r distinct labelled slots from the actual H pool. Each paid single
keeps its separate original A occurrence; the exact defect identity
already proves simultaneous additivity of A and H. Therefore H>=2z+r
and A>=s+2t prove(1), using integer parity just once globally.

**Width-six height-gap theorem.** Suppose every positive U has width6 and
|a-b|<=4. Negative dimensions, rotor phases, source number and reserve are
unrestricted. Sections2--3 show z=0 and every single-activation double has
the tight form(4), so r=s. Two-activation doubles supply their own two A
occurrences. Consequently

    2R >= 2(s+t)=2n2,
    sigma >= n0+R-n2 >= n0 >= 0.

This proves the exact joint allocation and |T|+|M|<=mn/2 on this complete-
source class, improving the5/6 matching coefficient by |M|/6. There may
be arbitrarily many unequal positive sources; the earlier Uneq<=1
restriction is absent. Height differences greater than four and arbitrary
positive widths remain part of the unrestricted objective.

## 6. Sharper geometry of the connected A+A residual

In a nonexceptional failing R1 component, the accepted two-slot R1 reduction gives
n0=z=t=0,s=2,A=2,H=U0=Z0=0. Inequality(1) now forces r=0.

For either double of width6, its unactivated side is longer by at least
four, by(3). Equality4 would give a tight witness and r>=1, impossible.
Evenness therefore makes the height difference at least SIX. The opposite
gate has a distinct phase10 owner; non-tightness sharpens(3) to
b<=k<=h-2<=a-6.

For either double of width8/10 with heights4/6, the unactivated gate must
be occupied. The accepted short-side support argument excludes phase01;
phase10 would activate this terminal. A longitudinal phase11 role has
a=6,h=4=a-2 and would again be paid. Thus this gate is necessarily the
transverse phase11 tip, predecessor right/bar down in left normalization.

These are necessary conditions on a complete connected candidate. They
neither realize it nor prove its impossibility. Arbitrarily many one-mark
sources and unrestricted negative dimensions remain allowed.

## 7. Verification scope

The companion checker reconstructs actual marks, activations and physical
labelled slots before testing counts. It checks interleaving on finite
endpoint/support role pairs and tests the universal coordinate formulas.
Role pairs are not reported as complete feasible fusions. Explicit
complete one-mark tight-gate fixtures exercise the forced tile at several
incident heights, alongside the existing physical controls. Coverage of
paid SINGLE-ACTIVATION DOUBLES is reported separately and may be zero.
Finite checks do not replace Sections2--5.

The Lean companion covers general bar-corner profiles, intrinsic corner
degrees, blank-corner overlap coordinates, distinct-gate displacement,
interleaving/tight-height arithmetic, finite-slot count, integer budget
and the sharpened A+A gap. Source-to-role normalization and physical
source/mark/slot adapters remain written. Execution and independent
review are recorded separately; earlier verdicts do not cover this theorem.

Local Lean4.33.0 source check, object build and all17 individual axiom
audits pass, using only propext, Classical.choice and Quot.sound where
needed; no sorry or native_decide. The final physical-checker run passes
771 images,142 tight marked-side occurrences,123 covered width-six images
and35 images with multiple tight witnesses. Complete paid-single-double
and interleaving occurrences are BOTH ZERO. Separate role controls pass
1044 interleaving pairs including90 gap-four pairs,96 blank-corner overlap
checks and24 arbitrary-height corner profiles. Those pairs are not complete
feasible fusions. The general proof is Sections2--5, not this enumeration.

Independent follow-up task7def602b-459c-44c6-a58b-01e75e356708 completed
ACCEPT at04:22:52UTC, observed gpt_6/pro,19387characters. Original stream61113
ended exit0. Acceptance covers the new written interleaving, general-height
tight witness, simultaneous non-reuse, shared count and all-reserve class
under the supplied complete-source catalogue and ledger. It does not
execute code/Lean or establish a complete two-gate fixture. Its three
exposition clarifications are incorporated above; no earlier verdict was
inherited. See output/width-six-interleaving-review.json.
See output/width-six-interleaving-formal-check.json,
output/width-six-interleaving-controls.json and
output/width-six-interleaving-review-live.json for scope and task identity.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
