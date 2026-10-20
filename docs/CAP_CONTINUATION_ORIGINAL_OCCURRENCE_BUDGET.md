# A simultaneous original-occurrence budget for caps and paired continuations

20 October 2026. This reconstructs the cap-count proposal in
NEGATIVE_PAIRED_CONTINUATION_RESEARCH_LEADS.md and strengthens its simultaneous
count to arbitrary complete-source fusions. It does not assume the proposed
global paired-path classification. Each count below is defined from actual
original geometry. No unused payment is inferred merely from a new owner.

## 1. Model, exact counts and statements

Use the finite complete U/rotor model of
ALL_PHASE_JOINT_COMPENSATION_SLOTS.md: even widths w>=6, independent even
heights a,b>=4, arbitrary translations/isometries and rotor phases, disjoint
original endpoint sets, unchanged original matchings, retained original
supports outside the endpoint union P, and final selected occupied degree
at most one. The physical aligned partition is fixed and transported under
every normalization. Optional selections obey the established restrictions.

Write K01,K10,K11 for original U counts in the three negative effective
phases. Keep the exact geometric reserve identity and allocation ledger:

    2R=A+U0+Z0+H,       mu=N+R-G,       sigma>=mu.

G is the number of marked original positive sides; it is not negative source
charge. A counts activated original positive terminal-singleton occurrences;
U0 counts unfilled original phase11 U triple caps. The other nonnegative
counts have their established meanings. No matching-size estimate is used
in the new occurrence argument.

Define Fpos to be the number of filled phase11 U caps whose missing corner
belongs to an original positive U. Each such corner identifies one original
positive terminal-singleton occurrence. In particular Fpos<=A.

Define the following two actual, typed continuation counts. Normalize a
phase10 parent to U(w,a,b), with bar rows0,1 and columns1..w. The transported
physical partition has row pairs{-1,0},{1,2},... and column pairs{0,1},{2,3},...
Both tips and corners below refer to their original owners.

- c counts parents for which the two points (2,2),(2,w-1) are the two tips
  of a common phase01 source

      (r,col) -> (D+2-r,col+1) on U(w-2,D,D),

  for an even D>=4, so w>=8. The full source, not just its two points, is required.
- i counts those same parents for which the points (2,3),(2,w-2) are the
  outer bar corners of a common phase10 source

      (r,col) -> (r+2,col+2) on U(w-4,a',b'),

  with legal independent heights, so w>=10. Thus i<=c. Count each original
  parent once in each applicable count. Parents can have arbitrary
  other contacts; the intermediate or child owners are not assumed fresh.

These definitions count the proposed outer and indirect motifs precisely.
They do not assert that every possible common owner has one of these forms.
No H=0, U0=0, AA census, acyclic contact graph, finite dimension bound or
restriction on other sources is needed for the following theorem:

    2K11+2c+2i <= 2K10+2K01+Fpos+U0
               <= 2K10+2K01+A+U0.                 (1)

In particular

    R >= K11+c+i-K10-K01.                          (2)

Let Dsrc=K11+c+i-K10-K01, a signed integer. Retaining the other terms of
the existing exact identity gives the more informative consequence

    2R >= 2Dsrc+(A-Fpos)+Z0+H.                     (3)

The later [any-pair extension](DISTINCT_NEUTRAL_SUPPORTS_AND_ANY_PAIR_BUDGET.md)
also reserves U singleton endpoints beside exact original regular2P1T pairs.
It retains the Epair set defined here as E0, and proves a simultaneous count
using the same endpoint pool and an exact unused-slot identity.

There is a stronger source-wide form. Define Epair as the cardinality of the
set of endpoints q in Pneg whose physical tile also contains another original
owner's EXACT 2P0T profile. Here Pneg contains only original phase01 U terminal
endpoints and phase10 U outer-corner endpoints. Negative rotor singleton
endpoints are excluded. Count each endpoint once, including endpoints at
splits and contacts outside the typed motifs. Then

    Epair>=2c+2i,
    2K11+Epair <= 2K10+2K01+Fpos+U0,               (4)
    2R >= 2(K11-K10-K01)+Epair+(A-Fpos)+Z0+H.      (5)

Thus the count applies to all actual contacts of this kind, without a
common-owner classification or a path hypothesis. This is one joint count
of the original resource pool. It is not a new reserve to add to an
independent lower bound for R.

## 2. Source singleton catalogue and rotor exclusion at a cap

The complete original profile catalogue gives:

| Effective U phase | Original singleton endpoints | Number |
|---|---|---:|
| 00 | the terminal tips, profile1P2T | 2 |
| 01 | the terminal tips, profile1P1T | 2 |
| 10 | the upper outer bar corners, profile1P1T | 2 |
| 11 | none; the two lower outer corners give triple caps | 0 |

This follows by pairing the two bar rows and the endpoint columns in the
fixed partition. In phases00/01 the two bar rows are paired together. A
length-aligned bar pairs its exterior corner with its next row, leaving
only terminal singletons; shifting its length instead makes each whole
bar tile full and again leaves terminal singletons. In phases10/11 the
bar rows lie in different row pairs. At length-aligned ends the upper row
has a singleton outer corner; at length-shifted ends the lower bar corner
shares its tile with the first stem point and its bar neighbor, a triple.
Interior bar/stem points occur in pairs or full tiles. Legal extra widths
and heights add only those interior profiles.

If an original phase11 cap is full, its missing corner q belongs to a
different original owner. That owner has exactly one endpoint in the cap
tile, because the other three corners already have the cap's original
owner. Thus the U alternatives are precisely the first three rows above.

A rotor cannot own q. Normalize the parent to U(w,a,b), its left cap
triple to (1,1),(1,2),(2,1), and q=(2,2). Its original endpoints include

    {0,1} x {1,...,6}, and {2,3,4} x {1}.

These are a fixed minimum stencil, present for every legal width and near
height. A central rotor point has three original endpoint neighbors, so
cannot fit at q with its north and west neighbors blocked. A rotor tip's
central neighbor can only be east or south. If east, a central square above
that neighbor hits row1 of the parent bar; a square below it has the
pinwheel's north tip in that bar. If south, a central square to its left
hits the original stem; a square to its right has its west tip in that
stem. All collisions are within the displayed minimum stencil.

Equivalently, quarter-turn invariance leaves two rotor chiralities and eight
original endpoint roles per chirality. Assigning q to a role uniquely fixes
the translation, and each of these sixteen placements overlaps that
stencil. The Lean finite rotor table checks this complete fixed-role
classification. It is not a search over a bounded set of translations.
Reflection handles the other cap, and transporting the physical partition
handles every source orientation.

## 3. One pool for all negative U singleton uses

Let Pneg be the set of original phase10 outer-corner endpoints and original
phase01 U terminal endpoints; phase10 corners are also U-owned. Original
endpoint disjointness gives

    |Pneg|=2K10+2K01.

Each filled cap with a negative owner uses its missing-corner point in
Pneg. Distinct original caps occupy distinct physical tiles: two disjoint
original triples cannot fit in one tile, and one source's two caps are
distinct. Hence their filler points are distinct. Positive cap fillers
are likewise distinct original positive terminal occurrences. Their tiles
are full, so both of their original intratile supports are consumed. They
are actual activations; this proves Fpos<=A without assigning a terminal
activation twice.

Each parent counted by c uses the two tips of its phase01 intermediate in
Pneg. Each parent counted by i additionally uses its child's two phase10
outer corners. At either end all these contact points lie in the physical
tile containing the parent's original bar pair. In the normalized left
tile Q={1,2}x{2,3}, that original pair is (1,2),(1,3), the intermediate
point is (2,2), and the indirect child corner is (2,3). The right tile is
the reflection. Both parent profiles are exactly2P0T.

There are two independent nonreuse obligations.

First, two different parents cannot use the same contact point q. In its
physical tile each parent would supply two original endpoints other than
q. Different original owners have disjoint endpoints, requiring four
points among the tile's other three corners. This is impossible. Within
one parent the left/right points are distinct, and the intermediate-tip
points differ from the indirect-corner points. The phase01/phase10
distinction also separates their original occurrence classes. A recipient
owner may still recur at different points; owner distinctness is not used.

Second, no such continuation point can also fill an original phase11 cap.
That cap's triple occupies all three other corners of the tile, including
the parent's original pair. If the cap and parent owners were different,
their original endpoints would overlap. If they were the same, their exact
original profile in the same fixed tile would have to be both3P0T and
2P0T. Both alternatives are impossible.

More generally, every endpoint counted by Epair shares its physical tile
with an original2P0T pair. The same triple-versus-pair argument separates
ALL those endpoints from negative cap fillers, including arbitrary split
contacts. Epair is a set cardinality, so an endpoint or recipient owner is
never counted once per contacting source. Two original pairs cannot both
share the tile with the singleton, since that would require five endpoints.
All typed continuation points belong to this set and are distinct, proving
Epair>=2c+2i. Consequently

    Fneg+Epair <= |Pneg|=2K10+2K01.

Here Epair reserves original endpoint slots; it does not count defect units.
Its definition also permits a nonfull mixed triple tile. The H contribution
of that tile remains in the existing exact identity, with no new deficit
assigned to Epair. More explicitly, let L=|Pneg\(FnegSet union EpairSet)|.
The disjointness just proved gives |Pneg|=Fneg+Epair+L, so the cap identity
and exact reserve identity give

    2R=2(K11-K10-K01)+Epair+(A-Fpos)+Z0+H+L.

Dropping L>=0 proves(4)-(5), even when Epair and H describe the same tile.

In particular negative cap fillers, the2c intermediate tips and the2i indirect
corners are simultaneously distinct members of Pneg. With Fneg denoting
the negative cap filler count,

    Fneg+2c+2i <= 2K10+2K01,
    Fneg+Fpos+U0 = 2K11.

Elimination proves(1). Combine with2R=A+U0+Z0+H and Fpos<=A for(2).
Keeping the difference A-Fpos and the nonnegative Z0,H gives(3).
No A, U0, full-tile correction or older H witness has been spent a second
time. This proof applies across all source components simultaneously.

## 4. Positive activation cannot fill a cap in the AA residual

Here AA means the established failing nonexceptional R1 component. The
accepted saturation and transverse-exclusion theorems give precisely two
double-marked width6 positives, one activated short terminal on each,
A=2 and U0=Z0=H=0. Other one-mark positives and arbitrarily many negative
sources/rotors remain allowed. The incoming-owner normalization below is
the accepted WIDTH_SIX_FOUR_STEM_COMPENSATION.md dependency, not a new
restriction introduced to close the count.

Normalize either positive to O=U(6,a,b), a>b, activated short tip z=(b,6).
The other incoming gate has original owner

    Rowner(r,col)=(k+2-r,col+4) on U(v,k,f), k>=b, v>=6, f>=4.

Its near stem lies in column5, rows2..k+2. In particular it owns
p=(b+1,5), while it does not own (b,7): the latter pulls back to
(k+2-b,3), below the bar and strictly between the two stem columns.

If z filled a phase11 cap, its original owner C would have the triple
(b,7),(b+1,6),(b+1,7), with missing corner z. At the elbow(b+1,7) one
of its two arms extends west, either along its bar or along its stem.
The legal minimum width/height implies that C also owns p=(b+1,5).

For completeness the arbitrary-parameter Lean lemma proves this arm fact
directly from the U endpoint predicate in all eight orientations: three
corners north/west/elbow present and the northwest corner absent imply
the endpoint two steps west is present. No phase or height bound beyond
the legal minima is supplied as a conclusion premise.

C cannot equal Rowner, since C owns(b,7) and Rowner does not. Thus their
shared p contradicts disjoint original endpoints. Neither of the only
two activated positive terminals can fill a phase11 cap. Consequently
Fpos=0 throughout AA. All counts and the activation census here concern the
same endpoint component. Substituting U0=0 in(4) and then using Epair>=2c+2i
gives the simultaneous necessary condition

    Epair <= 2(K10+K01-K11),
    K11+c+i <= K10+K01.                            (6)

If Delta=K10+K01-K11, then c+i<=Delta and2i<=Delta. Delta=0 excludes
every typed paired phase01 intermediate counted by c; Delta=1 excludes
every typed indirect phase10 child counted by i. These exclusions do not
classify arbitrary other contacts. This is not a complete AA exclusion.

## 5. Verification boundaries and the remaining closure

The scoped Lean companion proves the universal arbitrary-dimension
triple-arm lemma, complete sixteen-role rotor exclusion, finite-list
simultaneous occurrence capacity and conditional count/reserve/census
deductions. The physical source singleton catalogue, normalization,
identification of continuation point lists and their geometric nonreuse
are written adapters. This is not an end-to-end formalization of every
physical fusion.

The checker independently reconstructs cap owners, singleton occurrences,
motifs, actual activations and exact reserves in existing complete physical
fixtures. It also tests endpoint-disjoint indirect motifs separately;
those local motifs have infeasible retained supports and are explicitly
not complete feasible AA examples. Finite controls supplement this general
proof and do not establish universal closure. Execution counts and audit
scope are recorded in output/cap-continuation-budget-controls.json and the
separate formal receipt.

All fifteen scoped Lean4.33.0 declarations compile/build locally and pass
individual axiom audits, using only propext, Classical.choice and Quot.sound
as applicable, with no warnings, sorry or native_decide. The fixed rotor
barrier uses no axioms. Controls pass641 complete feasible images,114 filled
U caps (64 positive and50 negative fillers),33 actual paired motifs,116
pair-reserved original occurrences, and25 images where the all-contact
reservation count strictly exceeds2c+2i. One separated feasible fixture
contains both negative cap fills and a paired motif. Indirect motifs have
ZERO complete feasible coverage here;24 endpoint-disjoint partial images
all have infeasible retained supports. The universal triple-arm proof has
8656 endpoint-role controls including112 triple-arm cases; the exact rotor
orbit has16 cases and incoming-stem coordinates have54 controls. None of
these is a complete feasible AA realization.

Independent review760d11e0 ACCEPTS the initial cap/typed-continuation proof
and12-declaration snapshot. Its original stream83433 failed with EOF;
the completed response was recovered from the same task API. No successful
stream completion is claimed. The later reviewf8944cd2 accepts the all-contact
extension after explicitly restricting Epair to the U-only Pneg pool and
correcting the AA equation reference; both repairs are incorporated above.
It also supplies the exact unused-slot identity with L. Its original
stream40411 contains DONE and matches the completed response. Neither
review certifies local execution. See the two separate review receipts.

This theorem makes the previously proposed cap count and one simultaneous
nonreuse constraint concrete. The unrestricted compensation goal is still
open. A split can contact distinct tips of the same source, change its bar
axis or midpoint, and escape a decreasing-width path. Neither the cap
budget nor a fresh owner supplies an additional independently spendable
reserve. Existing lower bounds for R can be combined by a maximum; adding
them needs a separate disjointness proof. No arbitrary-grid decomposition
or rectangular-grid triple equality follows from this note.

In particular, a proof forcing Epair>2(K10+K01-K11) in every finite AA
candidate would exclude that residual. This is a precise next counting
target, not a claim that the strict inequality has been established.
Reconstruct the all-owner paired-row classification and finite descending
paths, then track transfers at their genuine ownership splits against this
same original-occurrence pool. Preserve the signed allocation
margin mu versus actual ambient slack sigma distinction throughout.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
