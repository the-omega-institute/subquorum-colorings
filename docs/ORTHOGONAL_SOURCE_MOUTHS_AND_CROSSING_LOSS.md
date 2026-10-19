# Orthogonal source mouths: nonnegative phase gains and exact crossing loss

19 October 2026. The source mouths in this theorem can run in either
direction, with no restriction on foreign prescribed-source contacts.
They may cross. A nonnegative perpendicular-source phase gain replaces
the earlier signed type-swap claim, and an explicit crossing loss corrects
the union count. The general grid problem remains open.

## 1. Initial hypotheses and notation

Use the even physical rectangle, feasible initial pair (T_0,M_0), actual
matching, objective-preserving normalization and whole-component ledger
from `COMPONENT_RECEIVERS_AND_SQUARE_FREE_BOUND.md`. There are B distinct
complete positive long sources with exactly the prescribed endpoint shapes,
actual matching, supports, even width at least eight, depth at least one,
and positive tile-preserving alignments in
`LONG_BENT_BANDS_AND_TERMINAL_STRIP_COMPENSATION.md`, Section 1.
Each complete source receiver has corrected charge +1 and is universally
frozen. Reflecting or transposing a prescribed source is allowed.

Every other initial complete endpoint component is thin, contains at most
one P-square, or is a prescribed complete straight contact comb with its
actual consecutive matching, alternating side supports and both axial
supports. Every endpoint initially in a source mouth must belong to a
prescribed source, in any direction, or a prescribed contact comb, in
either direction. No contact between these prescribed types is excluded.
These are coverage hypotheses, not automatic properties of all grid pairs.

All mouth endpoints are frozen. Normalization therefore preserves the
mouth labels and prescribed data; all other final receivers retain the
thin/one-square nonpositive bound. Work at a single-terminal representative.
Any physical or shifted unit square containing P has a unique complete
endpoint-component owner, by the accepted terminal ownership lemma.

Coalesce overlapping/adjacent parallel mouths within each physical row or
column band. This produces C strips G_i. Strips of the same direction
are disjoint. Strips of different directions intersect in at most one
physical tile, and each physical tile belongs to at most two strips.
Let G be their union, and let X be the number of tiles belonging to two
strips. The two extreme vertex columns of a horizontal strip, or rows of
a vertical strip, are forced blank by the extreme sources' supports.

For every complete comb, flag whether its physical sparse and saturated
singleton end tiles are in G. Missing singleton ends have neither flag.
Let O,J count sparse-only and saturated-only membership. Membership here
is once in the union, even if an end tile is in two strips.

## 2. Perpendicular sources have nonnegative phase gain

For a square Q write e(Q)=t_Q+p_Q/2-2. In each strip compare the physical
partition with the partition shifted by one vertex along that strip,
after deleting its two extreme blank columns or rows. For a component K
let E_i(K),E'_i(K) be its total e over endpoint-containing squares in
these two partitions. These are raw auxiliary weights, not partial
corrected matching charges.

Parallel contact combs are wholly contained between the strip's blank
extremes and have zero whole raw weight in both phases. Perpendicular combs
have the previously proved endpoint swap. Thus the sum of E_i-E'_i over
comb components is U_i-S_i, where S_i,U_i count physical sparse/saturated
comb singleton ends in that strip, including ends of parallel combs.

A source parallel to the strip has difference exactly one per physical
terminal tip in the strip. Its chambers and full arms have zero raw excess
in both phases. This is the source table from
`MIXED_COMB_AND_PARALLEL_SOURCE_CONTACTS.md`.

**Perpendicular-source lemma.** If a prescribed source K perpendicular to
G_i has any endpoints in G_i, then

    E_i(K)-E'_i(K) >= 0.                              (1)

Proof. Transpose the strip to be horizontal. The source's chamber occupies
two adjacent columns forming a physical column pair and an even interval
of rows starting at an odd row. Its two horizontal arms occupy the two end
rows of that chamber and end at their actual tips. A physical row band
meeting this source has exactly one of the following forms.

**Interior chamber band.** Both rows lie strictly between the chamber's end
rows. The intersection with the source is its full two-by-two chamber
square. This square has (p,t)=(4,0), hence physical raw excess zero.
The shifted partition cuts it into two squares, each containing a full
column of two endpoints. Each such square can contain at most one selected
vertex in its other column: two would be adjacent to one another and to
endpoints, violating selected-vertex feasibility. Write a,b in {0,1} for
these counts. The shifted excesses are -1+a and -1+b. The phase gain is
therefore 2-a-b>=0. The chamber need not supply two: a and b can both be one.

**End-row arm band.** The band contains one chamber end row and its exterior
neighbor. If any endpoint of its horizontal path lies in the strip, the
entire path from the chamber through the terminal tip lies there, since
it cannot cross a forced-blank extreme column. This path includes the two
chamber columns and the odd arm, so it has an odd number of endpoints.
The physical endpoint-square raw sum is +1/2: every full path tile is
(2,1), and the terminal tip tile is (1,2).

In the shifted partition all full path tiles are still (2,1). At the
chamber end there is one singleton square. It contains its chamber endpoint
and the required lateral chamber support in the other row of the same
column. Feasibility forces the diagonally opposite corner blank; the
remaining corner may be selected or blank. If a in {0,1} records that
optional selection, this square has (p,t)=(1,1+a), so E'_i=-1/2+a.
The phase gain is 1-a>=0. Reflections cover a source opening the other way
and the other chamber end row. These two cases exhaust every physical row
band meeting a perpendicular source, proving (1). QED.

Let A_i be the sum of these perpendicular-source phase gains. Each is an
integer, and A_i>=0. Let L_i count tips of sources parallel to G_i whose
physical tip tiles lie in G_i. Combining all component owners gives

    sum_K(E_i(K)-E'_i(K)) = L_i+U_i-S_i+A_i.          (2)

Optional lateral selections are counted in the shifted endpoint squares;
they are not silently discarded or treated as no-P donors.

## 3. The strip identity and parallel-tip count

Let n_i count physical tiles in G_i, let mu_i=|T in G_i|+|P in G_i|/2,
let D_i be its physical no-P deficit, and let D'_i be its shifted no-P
deficit. Both partitions count the same occupied vertices; the shifted
partition has n_i-1 squares. Directly summing raw excess gives

    D_i=2n_i-mu_i+sum_K E_i(K),
    D'_i=2(n_i-1)-mu_i+sum_K E'_i(K).

Consequently

    D_i=2+L_i+U_i-S_i+A_i+D'_i,    A_i,D'_i>=0.      (3)

The exact parallel-tip count remains

    sum_i L_i=2B-2C.                                 (4)

For each merged strip with b member source mouths, exactly two of their
2b distinct tip tiles are outside its interval: its extreme left/right
or upper/lower tips. All other tips are internal. No excluded extreme tip
can lie in a different parallel strip of the same band, since its own
mouth and that strip would then be adjacent and coalesced. Different
parallel bands cannot contain it. Perpendicular strips may contain it,
but L_i deliberately counts only tips parallel to that strip. Thus
perpendicular contacts do not invalidate (4). Tip distinctness follows
from physical endpoint-component ownership. This proves (4) without any
disjointness assumption between the two strip directions.

## 4. Count each crossing once

For a crossing tile Q define its loss k(Q) by its actual physical type:

| Tile type | k(Q) |
|---|---:|
| No endpoint | 2-t_Q |
| Sparse singleton end tile of a contact comb | +1 |
| Saturated singleton end tile of a contact comb | -1 |
| Any other endpoint tile | 0 |

Put K=sum_(crossing Q) k(Q), and A=sum_i A_i. The complete-component
ownership lemma makes these types exclusive. Selected-square capacity gives

    -X <= K <= 2X.                                   (5)

There are two independent corrections when summing (3). A no-P crossing
tile's deficit is counted twice and must be subtracted once. A crossing
comb end is counted twice in sum_i(U_i-S_i), but only once in the union
membership J-O. The additional saturated-minus-sparse multiplicity is
the negative of the last two nonzero cases in the table. Equation (4)
therefore gives the exact physical union identity

    D_G=2B+J-O-K+A+sum_i D'_i.                       (6)

Every physical no-P tile in D_G appears once. A crossing tile with a source
endpoint is not a physical donor; any associated phase gain already belongs
to A or L_i. Shifted squares are auxiliary counts and supply no second
set of physical resources. Matching transfers remain inside each original
whole source or comb receiver.

## 5. Initial-pair theorem and improvement over 5/6

Let R be the sum of physical no-P deficits outside G and deficits of final
nonprescribed receivers. Then R>=0. Each source whole receiver contributes
+1, and each complete contact comb contributes zero. Substituting (6)
in the original physical ledger and using normalization gives

    mn/2-|T_0|-|M_0|=B+J-O-K+A+sum_i D'_i+R.         (7)

**Crossing-loss theorem.** Under the initial coverage hypotheses in Section 1,

    |T_0|+|M_0| <= mn/2-B+O-J+K
                 <= mn/2-B+O-J+2X.                 (8)

In particular K+O<=B+J implies coefficient one; the purely combinatorial
condition 2X+O<=B+J is sufficient. For the subclass satisfying K+O<=B+J,
this removes the entire |M_0|/6 loss in the existing universal
|T_0|+(5/6)|M_0|<=mn/2 bound. For source-only configurations paired into crossing pairs, with
no further mouth intersections, B=2r and X=r, so the coarse criterion
already yields coefficient one. Isolated sources are allowed too.

More generally, suppose every coalesced strip intersects at most one
perpendicular strip, and O=0. Then the strip intersection graph is a
matching, so 2X<=C<=B. Equation (8) proves coefficient one for any number
of such crossing pairs, parallel overlaps inside each strip, and closed
comb connections between their mouths. In particular, any configuration
with at most two prescribed positive sources and O=0 satisfies the bound,
regardless of their relative direction or whether their mouths cross.
This corollary retains all the coverage hypotheses of Section 1.

When X=0, this recovers the earlier bound while admitting perpendicular
source contacts that had previously been excluded. With arbitrary crossings
the exact K criterion can be stronger than its 2X simplification. No bound
on X or K valid for every prescribed-source configuration is asserted.

### Directional averaging removes the crossing restriction for source-only mouths

There is a stronger consequence that does not bound X at all. Let F be the
sum of comb end fluxes over individual strips, with multiplicity: each
saturated end contributes its number of containing strips and each sparse
end subtracts that number. Thus

    F=sum_i(U_i-S_i).

Let D_1 be the physical deficit on no-P tiles of G covered by exactly one
strip; let D_2 be the deficit on those covered by two strips. These are
disjoint actual physical tile sets. Therefore

    sum_i D_i=D_1+2D_2,
    D_G=D_1+D_2,
    2D_G=sum_i D_i+D_1.                              (10)

Summing (3),(4) gives sum_i D_i=2B+F+A+sum_i D'_i. Substitute this and
(10) in the original whole-receiver ledger, with the same R as in (7):

    2(mn/2-|T_0|-|M_0|)=F+A+sum_i D'_i+D_1+2R.     (11)

This is an exact alternative identity for the same physical resources.
In particular F>=0 implies coefficient one for arbitrary source directions
and arbitrarily many mouth crossings. A sufficient end condition is that
every comb's saturated end belongs to at least as many strips as its sparse
end; aggregate nonnegative F is enough. Union closure O=0 by itself does
not impose this multiplicity condition and is not claimed sufficient here.

**Source-only mouth theorem.** Retain all Section 1 coverage hypotheses and
require each endpoint in any source mouth to belong to a prescribed source.
Then

    |T_0|+|M_0| <= mn/2

for every number of prescribed sources, at arbitrary positive tile-preserving
orientations, with unrestricted source contacts and mouth intersections.

Proof. No contact-comb endpoint occurs in any strip, so F=0. All other
terms on the right of (11) are nonnegative. QED. Complete combs outside
the mouths and all the previously allowed nonprescribed outside components
remain permitted. This is a general geometric compensation theorem for its
stated source class; arbitrary positive bent components are not prescribed
sources automatically.

Equivalently, assign each strip only half its no-P deficit. A donor in one
strip is used by one half, and a donor in two is used by two halves. Total
use never exceeds its actual physical deficit. Equations (3),(4) supply at
least B in these half claims when F>=0, covering the B whole source charges.
This explains why many crossings do not obstruct this theorem. The crossing
loss and averaging estimates are alternatives; their resources cannot be
added as two independent compensation supplies.

## 6. An explicit all-width obstacle to the unchanged strict payment

For every even W>=22 use a 28-by-(W+10) rectangle. Place a downward source
H with width W, depth six and chamber origin (2,3). Its mouth is rows16,17,
columns4,...,W+1. Place a rightward source K by transposing the standard
width14, depth-four source and adding (4,4). Its chamber is rows7,...,20,
columns6,7; its tips are (7,16),(20,16); its mouth is columns16,17,
rows8,...,19. Retain all prescribed matching edges and selected supports.

Add this fixed set of 19 selected vertices:

    (9,16),(9,17),(11,17),(12,16),(13,16),(14,17),(15,17),
    (16,5),(16,8),(16,11),(16,14),(16,16),
    (17,9),(17,10),(17,12),(17,13),(17,15),(18,16),(18,17).

Also add (16,c),(17,c) at every even c=18,20,...,W. Leave other sites blank.

The sources are distinct complete endpoint components. Their chambers are
separated from each other's endpoints: H's chamber is at rows2,3, K's starts
at row7; H's arm columns3,W+2 lie outside K's occupied column range5,...,17.
The only chamber intrusion is K's two-column chamber through H's mouth.
The displayed extra selected vertices have the following occupied neighbors:

- (16,5),(16,8) see their intended K chamber endpoints and no other occupied
  vertex; all their other adjacent sites are blank.
- The fixed horizontal selected pairs (17,9)--(17,10) and
  (17,12)--(17,13), and vertical pair (12,16)--(13,16), are isolated
  selected pairs in the occupied graph. The remaining fixed pairs are
  (9,16)--(9,17), (14,17)--(15,17), and (18,16)--(18,17).
- Every remaining added selected vertex is isolated among added selections
  and has at most its single prescribed-support neighbor. In particular
  (16,14),(17,15),(16,16) have no occupied neighbors among themselves.
- Every tail pair (16,c)--(17,c) is separated from the next by a blank
  column and has no occupied neighbor in rows15,18. At c=W the possible
  H support in column W+1 is diagonal; at c=18 the preceding column17
  is blank in rows16,17.

The prescribed selected supports retain their intended endpoint as their
sole occupied neighbor: the added sites avoid all their other neighbors.
These explicit adjacency facts establish feasibility for every W; they are
not inferred from finite checks. Prescribed source freezing persists in
every such feasible completion.

The two mouths overlap in exactly the physical tile rows16,17, columns16,17.
It contains only the selected vertex (16,16), so its physical deficit is one.
H's mouth has just two deficient no-P tiles: columns4,5 and columns16,17,
each with one selected vertex. The chamber tile columns6,7 has four endpoints;
every other no-P tile has two selected vertices. Thus D_H=2.
K's mouth has deficient tiles rows10,11 and rows16,17, each with one selected
vertex; all its other tiles contain two selected vertices. Thus D_K=2.
Consequently

    B=2, X=1, O=J=0, K=1,
    D_H+D_K=4, D_G=3, A=0, sum_i D'_i=0.             (9)

In the perpendicular chamber contact both optional flank selections are
present at (16,5),(16,8), so the phase gain is 2-1-1=0.
The exact counts are |T|=W+55 and |M|=W+36. Equation (6) is attained in
this local union count. The rule D_G>=2B, valid under the earlier contact
hypotheses, fails after those hypotheses are dropped. The two source charges
are nevertheless paid by D_G=3. This is a counterexample to that unchanged
local payment rule, not to the coefficient-one grid inequality or to a global
strict-margin bound whose exterior may supply further payment.

## 7. Validation scope and open work

`develop/check_orthogonal_source_mouths.py` checks the original physical
ledger, terminal ownership, freezing, each perpendicular contact case,
parallel-tip count, multiplicities, crossing types and equations (6),(7).
The explicit construction uses no optimizer; an earlier finite optimization
only discovered its selected pattern. Written arbitrary-width and arbitrary
configuration arguments supply the proofs. The archived finite receipt and
any scoped formal audit must be read with their own stated scopes.

At milestone619acdc the archived receipt `output/orthogonal-source-mouth-controls.json` passes
442 configurations and 40 symmetry images. It includes explicit filled
obstacles through width200, pair clusters through eight pairs, one source
meeting twelve perpendicular mouths, both perpendicular contact cases,
and sparse/saturated comb ends counted in two crossing strips. The generator
for the many-crossings controls is only finite validation evidence here;
the general theorem uses no assertion about that generator at arbitrary size.

At that milestone the local Lean 4.33.0 audit passes 95 scoped declarations, with source hashes
in `output/orthogonal-source-mouth-formal-check.json`. Its five new declarations
in `formal/SubQuorum/OrthogonalMouthFlux.lean` prove actual local feasible-label
flank capacity and the cap selected count, crossing-loss bounds for an
arbitrary list of declared physical tile types, and the conditional global
bound from the stated ledger. Classification of entire source contacts,
geometric/counting adapters and equation (7) remain written proofs. There
is no claim that Lean checks the full geometric theorem.

The subsequent directional-averaging extension has its own current controls
and 97-declaration audit in `output/directional-averaging-controls.json` and
`output/directional-averaging-formal-check.json`; see
`DIRECTIONAL_AVERAGING_SOURCE_COMPENSATION.md` for its stronger source-only
theorem without a crossing restriction. The historical receipts above
retain their original source revision and scope.

Independent review task d54c5a35-91a6-4a9c-b795-680d3f013063 completed
ACCEPT at 11:21:06 UTC, observed gpt_6/pro. The full source definition,
crossing-loss theorem and explicit all-width obstacle were in its input,
granting the prior receiver/freezing/parallel-phase dependencies. Its one
scope-wording clarification above is incorporated. The exact response and
independent assessment are archived in `output/orthogonal-source-mouth-review-response.json`
and `docs/reviews/2026-10-19-orthogonal-mouth-assessment.md`.
The later directional averaging theorem was outside that input and receives
a separate follow-up review. The previous mixed-contact review's infrastructure
failure is a separate terminal task.

Reproduce the controls and scoped formal audit with:

```sh
python3 develop/check_orthogonal_source_mouths.py --output output/directional-averaging-controls.json
python3 scripts/check_collar_formal.py --lean /path/to/lean-4.33.0 --output output/directional-averaging-formal-check.json
```

The remaining task is to control K using the nonnegative phase gains A,
shifted deficits and exterior R beyond K+O<=B+J, and to cover arbitrary bent
components. The earlier all-radius end-locality obstacle remains valid.
This theorem does not prove grid triple equality or the unrestricted bound.
