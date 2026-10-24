# Exchange-terminal positive receivers need not have unique matchings

22 October 2026. Authors: Haobo Ma and Wenlin Zhang.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.

The stronger normalization in REMATCHING_NORMALIZATION_AND_RECEIVER_FLUX.md
does not reduce the residual problem to uniquely matched endpoint graphs.
We give a fourteen-endpoint exchange-terminal graph with exactly two perfect
matchings, then an all-even-parameter connected positive-charge family with
the same two matching choices. Both statements have written certificates
for every matching, rather than an inference from one frozen matching.
The counterexample concerns a proposed structural reduction, not the grid
half-area bound or universal compensation. Its positive family has an actual
distinct donor of capacity two paying charge one.

## 1. A finite core with two matchings

Use a6-by8rectangle, zero-based coordinates and nearest-neighbor adjacency.
All unspecified sites are blank. Let

    T={(0,1),(0,3),(1,0),(1,5),(3,6),
       (4,0),(4,5),(5,1),(5,3)}.

The endpoint set P is the union of the following five forced pairs

    (1,1)--(1,2), (3,5)--(3,4), (4,1)--(4,2),
    (4,3)--(3,3), (3,2)--(2,2),

and the four corners of the square

    a=(1,3), b=(1,4), c=(2,3), d=(2,4).

The complete occupied drawing is

    .T.T....
    TPPPPT..
    ..PPP...
    ..PPPPT.
    TPPP.T..
    .T.T....

Every selection has exactly one occupied neighbor. Every endpoint has
occupied degree at least three; precisely a,c,(3,3) have degree four.
The endpoint graph is connected. These properties follow directly from
the displayed coordinates and are separately kernel-checked for the core.

**Matching classification.** The five displayed pairs occur in every perfect
matching, and the remaining edges are either ab,cd or ac,bd. In particular
there are exactly two perfect matchings, called horizontal and vertical.

Proof. Initially (1,1),(3,5),(4,1) have unique endpoint neighbors, forcing
the first three pairs. Removing them leaves (4,3) adjacent only to (3,3),
forcing the fourth. Removing that pair leaves (3,2) adjacent only to (2,2),
forcing the fifth. The four remaining endpoints induce exactly the square
abcd. Its two perfect matchings are the two stated choices. QED.

## 2. No promotion under either matching

Write m for the chosen actual matching involution. A frozen endpoint cannot
be promoted in any feasible bundle, and its mate consequently stays occupied.
If an endpoint has two distinct occupied neighbors, each either an original
selection or the mate of an earlier frozen endpoint, it too is frozen.
The least-first-promoted argument proves this rule for arbitrary mixed-color
bundles. The rule also applies when a support has another reason to remain
occupied; its label need not remain selected.

Both matching certificates start with the following rows:

| Endpoint | First retained neighbor | Second retained neighbor |
| --- | --- | --- |
| (1,1) | (0,1) in T | (1,0) in T |
| (3,5) | (3,6) in T | (4,5) in T |
| (4,1) | (4,0) in T | (5,1) in T |
| a | (0,3) in T | (1,2)=m(1,1) |
| (4,3) | (5,3) in T | (4,2)=m(4,1) |

For the horizontal matching continue in this order:

| Endpoint | First retained neighbor | Second retained neighbor |
| --- | --- | --- |
| d | b=m(a) | (3,4)=m(3,5) |
| (3,2) | (3,3)=m(4,3) | (4,2)=m(4,1) |
| (2,2) | (1,2)=m(1,1) | c=m(d) |
| c | (2,2)=m(3,2) | (3,3)=m(4,3) |
| (3,3) | c=m(d) | (3,4)=m(3,5) |
| b | (1,5) in T | d=m(c) |
| (3,4) | d=m(c) | (3,3)=m(4,3) |
| (4,2) | (3,2)=m(2,2) | (4,3)=m(3,3) |
| (1,2) | a=m(b) | (2,2)=m(3,2) |

For the vertical matching continue instead:

| Endpoint | First retained neighbor | Second retained neighbor |
| --- | --- | --- |
| (2,2) | (1,2)=m(1,1) | c=m(a) |
| d | c=m(a) | (3,4)=m(3,5) |
| (3,2) | (3,3)=m(4,3) | (4,2)=m(4,1) |
| (3,3) | c=m(a) | (3,4)=m(3,5) |
| c | (2,2)=m(3,2) | (3,3)=m(4,3) |
| (4,2) | (3,2)=m(2,2) | (4,3)=m(3,3) |
| (1,2) | a=m(c) | (2,2)=m(3,2) |
| b | a=m(c) | (1,5) in T |
| (3,4) | d=m(b) | (3,3)=m(4,3) |

Each list accounts for all fourteen endpoints. In a hypothetical nonempty
bundle, its first promoted endpoint in the appropriate list retains the two
distinct listed neighbors, contradicting feasibility. Together with Section1,
this excludes bundles for EVERY perfect matching: the core is exchange-terminal.
Any sequence of rematching and promotion cannot start a promotion either.
In any feasible exterior preserving this complete endpoint component and its
selected supports, no bundle can contain an endpoint of the protected
component, including a bundle also involving exterior endpoints. Promotions
confined to unrelated components are allowed. The completeness assumption
excludes new cross-matching edges to exterior endpoints, and the certificate
excludes a first promotion touching the protected component in any sequence.

Its receiver has7physical tiles,7selections and7matching edges, hence charge0.
The objective is16, half-area24 and total no-endpoint deficit8. Thus this
first obstruction alone is not a positive-demand receiver.

## 3. A connected positive family for all even widths and heights

Let w>=6,h>=4 be even. Take the frozen elbow E(w,h) with relative endpoint
and selected data from ELBOW_SOURCE_COMPENSATION.md. In its relative coordinates
the bar occupies {0,1}x{0,...,w-1}, its thick leg occupies
{2,...,h-1}x{w-2,w-1}, with tips (2,0),(h,w-1).
Transform the entire elbow by

    g(u,v)=(1-u,5+v).

Form the union matching with either matching of the finite core. Take the
union of the two selected sets, removing sites that are now endpoints.
Exactly two old selections are consumed: core support q=(1,5) becomes the
elbow's g(0,0) endpoint, and elbow support p=(1,4)=g(0,-1) is already the
core endpoint b. All other prescribed selections remain selected.
Translate everything by the even vector(h+2,2) into a sufficiently large
even rectangle; for example(h+10)-by(w+14) works. Physical tiling is fixed.

**Positive nonunique irreducible family.** This construction is feasible,
has one connected endpoint component, has exactly two perfect matchings,
is exchange-terminal, and has whole corrected receiver charge exactly1.

### Feasibility and matching choices

The elbow's endpoints lie in columns at least5 and rows at most1; the only
endpoint edge between the old endpoint sets is p--q. The only old selection
of either source consumed by the other source is its mutual support at p or q.
After those two selections are removed, no retained selection acquires an
extra occupied neighbor. Explicitly the core's remaining sites in columns
at least5 are confined to rows3,4, whereas the elbow bar is in rows0,1;
the remaining elbow support closest to the core is(-1,4), at distance at
least two from every core occupied site. All other support separations only
increase with w,h. Occupied neighbor sets of all original endpoints are
unchanged. Hence feasibility and single terminality hold for every parameter.

The sole cross-edge p--q is a bridge separating two even endpoint sets.
No perfect matching can use it: after matching its endpoints, either side
would have an odd number of vertices needing internal pairing. Thus every
matching restricts independently to the two sides. The elbow has its unique
matching by the all-length degree-one forcing theorem; Section1 supplies
exactly two choices on the core side. This proves the exact matching count
without enumerating matchings of arbitrarily large examples.

### A freezing proof that repairs the consumed supports

Fix either matching. The five common initial rows of Section2 still work:
none uses the consumed core support q. In particular a is frozen.

For the horizontal choice p=b=m(a) is therefore retained. For the vertical
choice c=m(a) is retained; endpoint d then has retained neighbors c and
(3,4)=m(3,5), so d is frozen and p=b=m(d) is retained. Thus p stays occupied
in EVERY feasible bundle, in both matching cases, before using elbow freezing.

The established all-parameter elbow freezing transcript can now be applied
in full. Its only consumed selection is p, already shown retained; all other
support sites remain original selections, and all elbow mates are unchanged.
Every use of p as an occupied witness is therefore valid. All elbow endpoints
freeze, so q is retained as the mate of a frozen elbow endpoint.

Finally apply the complete core transcript from Section2, using the now
retained q wherever its former selection was used. Both cases freeze all
core endpoints too. This is a uniform first-promoted proof, not an inference
from checking finitely many w,h. In particular positivity does not restore
the proposed matching-uniqueness reduction. QED for exchange terminality.

### Exact charge and a physical compensator

The isolated core and transformed elbow receivers overlap in precisely
Q={0,1}x{4,5}, before the final even translation. There is no selected spill
between their other tiles. Both consumed selections p,q lie in Q. Hence
the final counts are

    |P|=2w+2h+12,       |M|=w+h+6,       |T|=h+11,
    |R|=w/2+h+7,       |T intersect R|=h+9.

For the receiver counts, add core values7tiles/7selections and elbow
values(w/2+h+1)tiles/(h+4)selections, then subtract one shared tile and
two consumed selections. It follows that

    rho=(h+9)+(w+h+6)-2(w/2+h+7)=1.

Tile Q has three final endpoints, no selection and one blank. This is an
exact physical union count, with no extra matching-transfer or fusion credit.
The old elbow capped-corner donor becomes

    Q_E={-2,-1}x{6,7}

before translation. It contains no endpoints or selections, so has actual
deficit2. Its capped witness is unchanged: the consumed support p is not
among that witness's support sites. After translation its tile index is
(h/2,4). The old unique-owner lemma therefore applies and assigns Q_E to
the combined component. In this canonical blank-exterior construction its
deficit is exactly2, paying the whole charge1 with one unit left. In a general
feasible terminal exterior retaining the capped witness, its deficit is
guaranteed only to be at least1: selecting g(2,2)=(-1,7) can reduce it to1.
Both amounts still pay this family's charge. In particular this is a counterexample to uniqueness,
not to compensation or the target inequality.

## 4. What this rules out and what remains

The occupied-degree-three uniqueness criterion remains valid under its
original degree hypothesis. Our core has degree-four endpoints of both colors
on its alternating square. Both perfect matchings are frozen, so no strategy
of choosing a different matching can unlock it. Appending a positive elbow
retains this obstruction in an actual positive-demand connected receiver.

A compensation argument for exchange-terminal configurations must therefore
allow flexible matching blocks as well as uniquely matched chambers.
Collapsing an entire receiver to one matching or treating every alternating
cycle as a removable tile is unjustified. The new family is compensated;
it does not settle how to cover arbitrary mixed-direction positive receivers.
The complete-source39/41 result and submitted manuscripts are unchanged.

## 5. Verification scope

The initial endpoint-box search found the core in the4-by5endpoint domain.
The4-by4domain was fully checked:1050nonunique endpoint sets and5737feasible
single-terminal support models contained no counterexample. This is finite
discovery evidence only, with no general minimality claim.

The standard-library verifier checks both exact core matchings, their freeze
transcripts, all8core symmetries,72parameter pairs,288phase applications and
24positive-family symmetry applications, and72sharp-flank controls reducing
the canonical donor deficit from2to1. Every graft application has exactly
two matchings and both are frozen. Only the designated physical phase is
claimed positive in the general theorem; other phase counts are controls.

formal/SubQuorum/ExchangeTerminalNonunique.lean proves the core's complete
two-matching classification from an arbitrary matching involution, validates
both finite ranked freeze transcripts, and deduces exclusion of every bundle
for every matching. It checks core coordinates, feasibility and terminality.
The general positive-family geometry and freezing adapter are written proofs;
the final charge arithmetic has a separate scoped Lean theorem. Execution
passes locally on Lean4.33.0, with10theorems and10individual axiom audits,
using only propext and Quot.sound; there are no errors, warnings, sorry or
native evaluation. The receipt is output/exchange-terminal-nonunique-formal-check.json.
Independent review4eb5ea4d completed ACCEPT at07:27UTC, covering the complete
written argument and inherited dependencies. It requested the explicit
protected-component exterior scope and canonical-versus-general donor capacity
distinction now stated above. Its exact original completed stream, terminal
task and session responses agree; the observed model was gpt_6/pro. It did
not execute the checker or Lean. The accepted response is archived in
output/exchange-terminal-nonunique-review-accepted.json. The separate earlier
research question8d529046 completed with partial structural lemmas, leaving
the uniqueness question unresolved in that response. Our counterexample
settles that question negatively. The research response is archived in
output/exchange-terminal-uniqueness-research-response.json, with exact
original stream/task/session comparisons. It is not a review of this note.
