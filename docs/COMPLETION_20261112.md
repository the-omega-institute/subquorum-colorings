# Degree thresholds and source-dependent completion: 12 November 2026

## 13 November: actual short mixtures and cyclic reduction


[Short auxiliary mixtures and owner-path surplus](SHORT_AUXILIARY_COMPLETION_AND_PATH_SURPLUS.md)
prove beta_I>=ceil(8b/3+R(B)/6) for arbitrary owner paths/even cycles when
A has only P2/P4/C4 components; R sums owner path orders modulo3. One
rainbow-forest budget retains the path surplus, which pays exactly for an
odd-P2 ghost completion. Final physical certificates use original edges.
A connected200-vertex mixed example returns111 selected vertices (target107),
without claiming its exact optimum. Independent ACCEPT ran both the new and
inherited original checkers and reproduced their complete reports byte-for-byte;
the review receipt records its Python startup stderr warning.

[Physical cyclic reductions](CYCLIC_AUXILIARY_REDUCTION.md) complete two
copies to Q perfect, or four copies to Q perfect and owner B2-regular.
The sum of original-copy matching costs is bounded by the one completed
matching cost, and exact nested floors return a target original certificate
whenever the completed target is supplied. Thus universal8b/3 is equivalent
to the cyclic restriction; a failure can be localized to connected A unionB
containing both C4 and longer C4k auxiliary cycles, with cyclic owners.
This is a reduction, not a proof of that remaining case. Original checker
passes; independent ACCEPT executed that checker unchanged and reproduced the
complete report byte-for-byte. The remaining mixed cyclic target stays open.


## Primary complexity and tractable boundaries

[Unbudgeted primary fixed-list hardness](docs/UNBUDGETED_PRIMARY_EXCHANGE_HARDNESS.md)
uses charged source groups with exact no-increase rounding. Its optimum is
exactly the source vertex-cover number, with a self-contained connected
bridgeless normalization retaining two-connected bipartite physical min2/max3,
minimum square omissions and auxiliary P2/P4 components. There is no operation
budget or minimum-operation tie-break. This is fixed-list primary-cost
hardness, not unrestricted graph-parameter hardness.

[Connected-block cycle rank](docs/COMPONENT_BLOCK_RANK_AND_MATCHING_TRACTABILITY.md)
sharpens the exponent to the maximum rank of any candidate-component block;
ambient P2/isolated vertices give a polynomial complete frontier even when
total rank is unbounded. [Zero and small primary cost](docs/SMALL_PRIMARY_COST_AND_ZERO_THRESHOLD.md)
give an exact 2SAT zero-cost test and an exhaustive-cover XP algorithm in the
primary-cost threshold. These elementary algorithmic corollaries carry no
separate novelty claim. All three original checkers pass locally; three independent ACCEPT audits
executed their respective original checkers and reproduced the complete reports
byte-for-byte. Exact execution scope and limitations are preserved in the
separate review receipts.


## Initial matching choice and mixed-side deletion

The [constrained matching criterion](INITIAL_MATCHING_CHOICE_AND_MIXED_REMOVALS.md)
is necessary and sufficient over all initial maximum matchings for a fixed
cover and batch. Retirement is forced; mixed-side deletion charges each
original edge once even if both endpoints are removed. One matching test
returns a complete certificate or an explicit constrained Hall deficiency.
Enumerating covers/subsets then optimizes this broader inherited-cover rule.

All14 stored prior fixed-pair gaps close (outside-only all-pair choice closes12).
A two-connected30m unit-cost family has one-sided best costm and mixed cost0;
a second has all-pair mixed certificate2m but actual specified-list optimumm.
Both have general all-scale proofs; the latter prevents a completeness claim.
Original checker passes; independent ACCEPT reproduced the full original report byte-for-byte. Full goal ACTIVE, with
universal bounds and general grid questions still open.


## Matching-owned credit and neutral prerequisites

The [complementary transfer certificate](MATCHING_CREDIT_AND_NEUTRAL_PREREQUISITES.md)
removes points outside a fixed tight initial cover. Each matched removal owns
one initial matching edge and retires its cover mate; unmatched removals can
enable other savings. The inherited cover and surviving matching certify exact
final cost, including additions with retained-cover neighbours. Implications,
blockers and conflicts characterize this condition exactly; old edges within
the cover must also generate conflicts. An exact `2^k` polynomial algorithm
uses a conflict vertex cover of size k, with `4^tau` default parameter bound,
and minimizes operation count after maximizing nonnegative credit.

This reaches zero on the full 20m-vertex plateau and even-r odd-path barriers,
using m and one zero-credit prerequisites, respectively. It certifies endpoints,
not a general nonincreasing schedule. All 180 physical fixed-list rule optima
match enumeration; 14 still exceed the actual fixed-list minimum, and a full
example is retained. Original assertion-enabled checker passes; [independent ACCEPT](../output/matching-credit-exchange-review.json)
reproduced the complete report byte-for-byte. The full goal remains ACTIVE with all general bounds and grid
objectives below still open.

## Coordinated cover exchanges, cover choice and neutral plateaux

Four complementary results now have complete proofs, original checkers and
independent ACCEPT verdicts, with byte-identical report regeneration:

* [Cover saturation and dependency closure](COVER_SATURATED_COORDINATED_EXCHANGES.md):
  a minimum cover assigns each removal a different initial matching edge.
  Final-isolated additions allow shared components and closed cyclic dependencies.
  The largest fixed-cover batch is the complement of the predecessors of blockers.
* [Exact choice among all minimum covers](MINIMUM_COVER_CHOICE_FOR_COORDINATED_EXCHANGES.md):
  paths and even cycles have a complete cover catalogue. Enumerating it and
  recomputing filtered dependency closures optimizes the specified candidate rule.
  The total enumeration can be exponential.
* [A sharp exact-deletion barrier](EXACT_DELETION_CERTIFICATE_BARRIER.md):
  the best one-batch certificate has cost one while actual cost is zero;
  every order of a displayed shortest route has exactly one neutral step.
  Longer routes allowing increases may avoid neutral steps.
* [An unbounded local plateau](UNBOUNDED_NEUTRAL_EXCHANGE_PLATEAU.md):
  a two-connected $20m$-vertex bipartite minimum-degree-two, maximum-degree-three
  family starts at cost $m$ with no improving legal single-owner swap.
  No nonempty final-isolating exact-deletion batch exists, but actual all-helper
  cost is zero. Nonincreasing single-swap routes need at least $m$ neutral steps;
  an explicit route attains this in every order.

These are scoped certificate and method results. In both obstruction families,
the initial or certified cost already meets the $8b/3$ threshold; neither is a
counterexample to that target. General $8b/3$, the sharp unrestricted subcubic
coefficient and all general grid objectives remain open in the full ACTIVE goal.

## Pair conflicts and the exact activation-budget optimum

For fixed U*, the [conflict-graph theorem](PAIR_CONFLICTS_AND_ACTIVATION_BUDGET_OPTIMUM.md)
proves exact compatibility using pairwise tests. Individually eligible
cycles have even penalties d_C for odd components consumed from A[U*],
and an independent family gives cost<=nu0-sum(1-d_C/2). The optimum
numerical bound over ALL allowed activation sets W and candidate families
is nu0-alpha(Gamma0), on candidates with zero odd penalty. Greedy colouring
provides a polynomial sufficient construction and recovers the earlier
mixed long-cycle budget automatically.

A two-connected10r-vertex bipartite min2/max3 family for every evenr>=2
has conflict graph K_r and exact best budgetr-1, while a coordinated
independent omission set proves true cost0 and beta_I6r. Thus optimizing
this support criterion for a fixed minimum U* can miss8b/3 for all evenr>=4.
Changing U*, coordinated conflicting exchanges and iterative reconstruction
are distinct possibilities. Universal8b/3, the sharp subcubic constant and
all general grid objectives remain in the full ACTIVE goal.


## A common activation graph and inactive separators

The [activation theorem](ACTIVATED_AUXILIARY_SUPPORT_BUDGET.md) strengthens
the support condition by replacing A by A[W], with one common W containing
every possible changed omission. Disjoint full supports with even initial
counts give cost<=(m-o_W)/2-t. Edges to fixed vertices outside W can never
enter A[U]; every consumed region is charged once. Candidate changes require
recomputing W, its components, all parities and supports together.

A connected60r-vertex bipartite min2/max3 mixed-owner family has one C16r
and2r auxiliary squares. From the same U*, activation gives3r versus the
whole-component budget5r-1, and certifies8b/3 beyond earlier global tests
for r>=2. An explicit auxiliary-independent omission set proves exact
beta_I36r, so this budget is not claimed sharp. An older single-cycle
control gives r versus2r-1 but has true costceil(r/2). Universal8b/3,
unrestricted sharpness, unit5/6 and arbitrary-width grid equality remain
open in the full ACTIVE goal.

## Disjoint supports: simultaneous owner exchanges

The [new general support budget](DISJOINT_AUXILIARY_SUPPORT_BUDGET.md) proves
cost<=(m-o)/2-t for any permitted omission set with a packing of t eligible
exceptional owner cycles. Eligibility requires minimum omission on the cycle
and even initial counts in every auxiliary component it touches. Supports
are pairwise disjoint, so each component's capacity is spent once. Individual
component parities may change inside a chosen region and are not credited again.

The connected50r-vertex physical min2/max3 family has exact beta_I30r and
provides a genuinely crossing-cycle certificate beyond the previous global
tests for r>=2. The earlier two-connected20r family gives exact overlap-rule
overstatementceil(r/2), proving no independent saving per eligible cycle.
An exact2SAT wrapper decides whether some specified owner matching has<=1K4.
This is additional support for general8b/3, not a proof of it or a new sharp
SF coefficient. All general grid objectives remain in the ACTIVE full goal.

## Mixed owner bridges: 13 November continuation

The [complete standalone proof](MIXED_OWNER_BRIDGES.md) establishes the
all-helper8b/3 target for three mixed classes: at most one K4 in a specified
owner matching; arbitrary owner squares together with paths and6k-cycles;
and at most one exceptional owner cycle of arbitrary length. A global
four-label interface budget avoids repeating cross-component capacity.
A stronger local count lemma keeps arbitrary outside omissions fixed and
forces a matching-edge saving at even cardinality; this also certifies
some cases with several exceptional cycles.

The abstract A-proper/B-defect1 three-colouring holds for every maxdegree2
A and paths/even-cycle B. A connected30vertex physical counterexample has
exact beta_I17 while2b+h18, so the exact square normalization cannot be
used for arbitrary mixtures. A separate40vertex benchmark has restricted
one-owner-per-R-pair optimum21, target22 and actual beta_I24.
These results extend sufficient hypotheses for the existing conditional
5/51 ledger, without changing a universal coefficient. The full goal,
including general8b/3 and all general grid questions, remains ACTIVE.

## Connected maximum-witness retention obstruction

The [all-r family](CONNECTED_MAXIMUM_WITNESS_LOSS.md) has20rphysical vertices,
minimum degree2 and maximum degree3, is two-connected and bipartite, and satisfies
beta_I=11r+floor(r/2). Requiring the maximum possible b=4r witnesses reduces
the optimum to10r, belowceil(8b/3). The proof uses the complete local owner
objective and the cyclic adjacency of eight-index intervals. This identifies
a failed extension rule, while leaving general8b/3 and the existing bounds
unchanged. No unrestricted optimum or new sharp gap coefficient is claimed.


## All-owner auxiliary-square theorem: owner-size condition removed

The [new theorem](ALL_OWNER_AUXILIARY_SQUARES.md) proves beta_I>=ceil(8b/3)
for every physical template whose auxiliary graph is a union of squares,
with arbitrary owner paths and even cycles. A rainbow forest assigns one
exchange per owner cycle and pays every square rounding gain once. All-subset
rank inequalities follow from square capacity after removing two closed types.
The30vertex block attains equality. Rado's classical rank formula is included
with proof and attribution. The abstract theorem needs no physical colouring.

Construction/checker:2,644 physical certificates,331 beyond the previous
owner-size criterion,273 exact small forced optima,420 independently enumerated
coloured multigraphs and360 abstract colour-free controls. Rank cuts and physical
sets are independently checked. The general all-auxiliary8b/3 problem, sharp
subcubic interval[1/20,7/71] and general grid questions remain open.


## Auxiliary-square parity criterion: a new positive class

The [parity theorem](AUXILIARY_SQUARE_PARITY_CRITERION.md) proves all-helper8b/3
when A is a union of auxiliary C4s on N=2b indices and the path/even-cycle
owner graph satisfies beta_2(B)>=2ceil(N/3)-2. Exact normalization reduces the
problem to an A-independent B-dissociation set. A prescribed-edge exchange in
one owner cycle toggles parity in two auxiliary squares without changing the
global owner optimum; a coincident C4 supplies the exceptional case. This also
extends the sufficient class for the existing fixed-extraction5/51 bound.

The construction/checker covers2,133 templates/1,923 physical certificates,
241 exact forced optima,39,840 literal owner subsets and both parity repairs.
There are37 smaller applicable cases beyond the previous K4-free matching test.
Larger actual certificates reach64 helpers. General8b/3, the unrestricted
coefficient interval[1/20,7/71] and all general grid problems remain open.

## Sharp all-helper block and an odd-path coefficient refinement

The [complete proof](SHARP_ALL_HELPER_BLOCK_AND_ODD_PATH_REFINEMENT.md) gives
a connected30vertex bipartite min2/max3 template with beta_I16 and beta_2=17.
The all-helper8b/3 target is attained; the stronger11b/4 all-helper estimate
is false. Disjoint copies give exact16r and17r, by additivity. The upper proofs
use three charged-square cases and three ten-vertex physical blocks, respectively.
This is distinct from the preceding beta_I17 construction-loss example.

For an actual K4-free extraction with o odd-order owner paths and b' helpers,
if o>=2gamma b',0<=gamma<=1, the new ledger gives the conditional graph gap
floor((5+gamma)n/(51+12gamma)), interpolating5/51 to2/21. This is a structural
corollary of the earlier odd-path bonus, not an unrestricted coefficient claim.
Exact finite optima, local block properties and physical rational-ledger checks
are in output/sharp-all-helper-check.json; independent review scope is in
output/sharp-all-helper-review.json. Universal7/71 and all general grid questions
are unchanged, and the full collaboration goal remains ACTIVE.

## Owner matching criterion for arbitrary even owner cycles

The [owner matching theorem](OWNER_MATCHING_AND_FOUR_CYCLE_OBSTRUCTIONS.md)
proves beta_I>=ceil(8b/3+(o-2z)/6), where o counts odd owner paths and z counts
K4 components for the specified alternating/square-diagonal matching choice.
No auxiliary P/Q four-cycle implies z=0, allowing arbitrary even owner cycles
and mixtures with paths and squares. Exact2SAT characterizes K4 avoidance for
that family, with contradictory-path certificates and two-component clauses.
This extends the sufficient class for the existing conditional5/51 graph bound;
the unrestricted7/71 coefficient is unchanged.

A connected30vertex physical template has beta_I17, while both owner perfect
matchings have auxiliary independence number4 and the one-owner-per-edge
construction has optimum16. Disjoint copies give an additive loss r. The
full-cycle independence conjecture is satisfied in this example, not refuted.
The complete proof includes two eight-cycle independence bounds and an eight-row
all-helper upper classification. General8b/3 and the full collaboration goal
remain open/ACTIVE. Checker scope and exact independent audit are in the linked
note and output/owner-matching-review.json.


## Exact subcubic gap order/20 and all-helper optimization

The [supported-deletion theorem](TWENTY_VERTEX_SUPPORTED_DELETION.md)
proves exact SF_2(G_r)=12r for every r>=1 in the two-connected bipartite
20r-vertex family, with minimum degree2, maximum degree3 and beta_2=11r.
Thus its gap is exactly n/20. A complete local classification proves that
every13-set in the open block has an internally supported nonport deletion.
The generic lemma gives an all-ambient cap12 under arbitrary port attachments;
canonical minimality supplies attainment in the cyclic family. The earlier
port-avoiding dissociation composition and topology proofs are retained.

The [all-helper theorem](ALL_HELPER_EXACT_OPTIMIZATION.md) gives an exact
matching expression for beta_I, the optimum with every helper retained, and
proves the sharp loss0<=beta_2-beta_I<=b. Paths and6k-cycle owner cores form a
hereditary sufficient class for beta_I>=ceil(8b/3), yielding the conditional
5/51 graph gap bound for an actual fixed extraction. The coefficient was
already known for acyclic extracted cores; the added owner class allows6k-cycles.

Independent controls check77,520 thirteen-sets, explicit local branches and
3,000 arbitrary ambient models;686 exact all-helper models receive3,014,785
literal physical subset checks. The hereditary/lifting checker additionally
checks12,351 induced owner subgraphs,4,227 minimal selections on879 small
graphs and42 physical templates. Complete arguments are in the working
manuscript. Exact independent review scope is recorded in
`output/twenty-supported-and-all-helper-review.json`.

The sharp subcubic coefficient remains in[1/20,7/71]; the unrestricted
7/71 upper bound and the general8b/3 template question are unchanged.
The full cooperation goal, including general grid questions, remains ACTIVE.



## Square owner cores: compatible8b/3 template and conditional5/51 graph bounds

The [complete proof](SQUARE_CORE_TEMPLATE_COMPENSATION.md) proves
beta_2(H)>=3b-floor(2t/3)>=ceil(8b/3) when the extracted owner core has
only P1,P2,C4 components. The auxiliary graph uses witness P/Q conflicts
and transported same-colour opposite-owner pairs R from each C4. It is
simple, triangle-free, maximumdegree3; one-for-two independent-set exchanges
are polynomial and give all witness/helper/core choices simultaneously.
The retained extension then proves the exact nonnegative5n-51d certificate,
with structural correctionZ>=b'-2t+3ceil(4t/3)-4t. This is a condition on the
actual extraction, not on an arbitrary prior presentation. Eleven canonical
selected sets in finite template controls fail the later extraction condition
and are recorded rather than assigned this bound.

The new complete checker covers1,369templates/1,332exactoptima/61literaloptima,
4,227minimalsets in879smallgraphs,109nonemptytemplate+exteriorlifts including
five retainedtriple-leafcases,270generaltrianglefreeauxiliarygraphs and through
512helpers actualconstructions. It tests applicable and nonapplicable cases
separately. General-template8b/3 and graphsharpness remainopen. The unrestricted
7/71 bound is preserved; no new grid or Lean claim. Current28pageworkingmanuscript
compiledtwice,allpagesrenderedandvisuallyinspected. No email,submission,MacStudio
or Octoberpaperchange. Fullcollaborationgoal ACTIVE.


## Current unrestricted subcubic bound7/71: balanced witness marginals

The [complete proof](BALANCED_SIDE_AND_SUBCUBIC_BOUND.md) proves71d<=7n for
every minimal forming S in every finite simple bipartite maxdegree3graph,
emptyincluded. Current integerbound floor7n/71; no connectivity/mindegree/
balance/selectedcomponentcondition. Sharpness and attainment remain open.
Balanced physical-side distributions give owner/witness marginal<=1/2 and
mean cardinality11b/4-o/2. Componentwise optimization is compatible, avoiding
a Cartesian product. The penalty lemma charges both C and X with1/2;
physical exterior extension and paired margins yield14n-142d nonnegative.

Exact36-file independent audit ACCEPT; both original fullcheckers actually
run, freshreports compared. Local fullchecker43,756totalminimalinstances
includes5,200canonicaltemplates;580weightedinstances on116models(order<=10).
Larger prescribed templates check actualcandidates/allphases. Separate96local
auxiliaryshapes/1,312supports check exact marginals/cardinality. No newinteger
fullsetgain over51/517 in these controls;472gains are overolder15/152algorithm.
The general coefficient improvement is2/36707. Current26-page workingmanuscript
contains complete proofs; twicecompiled, allpagesrendered/visuallychecked.
No newLean, email, MacStudio, submission or Octoberpaperchange. Full goalACTIVE.


## Earlier unrestricted subcubic bound51/517: vertex penalties and exterior extension

The [boundary-expectation theorem](BOUNDARY_EXPECTATION_AND_SUBCUBIC_BOUND.md)
proves `517(|S|-beta_2(G)) <= 51n` for every minimal forming S in every finite
simple bipartite maximum-degree-three graph, including empty graphs. Hence
`SF_2-beta_2 <= floor(51n/517)`. Gain over 15/152 is exactly 3/78584;
sharpness and attainment remain open. There are no connectivity, minimum-degree,
side-balance or selected-component restrictions.

A general nonnegative vertex-penalty lemma controls potential and cardinality
together. Half the external degree as cost incorporates boundary loss into
conditional expectation. The chosen core solver remains unweighted; it charges
the retained superset using cost nonnegativity. Actual exterior and retained
extensions are compared separately. The paired-margin budget yields the exact
nonnegative ledger `102n-1034d=W+97r+241(alpha+pi)+144(e-b3)+47b3+92q+482tau`.

Exact 30-file independent audit ACCEPT, with original full checker execution
and fresh report comparison; see `output/boundary-expectation-review.json`.
Local checks: 43,684 minimal sets, 5,200 exact small templates, 28,635 cost
assignments, 103,470 weighted physical phases, 76,545 conditional controls,
580 weighted instances on 116 exact template models (order<=10) and ten literal crosschecks. Larger
templates check actual sets and all phases. The algorithm improves 472 full
candidates, choosing a smaller inner set on 680 instances. Costs include zero
and rationals with 401-bit numerators. The 26-page working manuscript was
compiled twice and rendered/visually inspected. No Lean, email, submission,
Mac Studio or change to October's submitted paper. Full goal remains ACTIVE.


## Earlier unrestricted subcubic bound15/152: two endpoints and paired margins

The [two-endpoint theorem](TWO_ENDPOINT_MARGIN_AND_SUBCUBIC_BOUND.md) proves
`152(|S|-beta_2(G))<=15n` for every minimal S in every finite simple bipartite
maximum-degree-three graph. Its integer bound was floor15n/152,
including the emptygraph andwithout connectivity, positive minimumdegree,
sidebalance orselectedcomponent conditions. Gain over31/314 is1/23864;
gain over8/81 is1/12312. Optimality andattainment remain open.

Both endpoint runs must be short for a physical path to be good. Its scores
supply1/6 inexpectation, withwholeP1/P2 events countedonce. Every bad path
ownsjustONEtriple. Both equal-order ordinary owner classes are combined to
pay their auxiliarypath'sONEflag. Distinguishedclasseshavenoflags. This
proves2tb+2sb<=12sigma once globally. Actual compatible sets satisfy
5D>=13b+3sigma+(3bG+2tg)/4. The retained-set and exterior-independent-set
extensions remainALTERNATIVES. The exact certificate is
30n-304d=W4+29r+71(alpha+pi)+42(e-b3)+13b3+28q+142tau>=0.

Exact26file independent audit ACCEPT with unchanged fulloriginalchecker
execution and fresh report comparison; fullactualscope is preserved in
`output/two-endpoint-review.json`. Local checkerexit0 in13.252635458949953s,
emptyseparatestderr.43862minimalsets/5200exacttemplates/19938physicalphases/
43734endpointwitnesses/1696simultaneousphysicalpairs. Literal-path control classifies all signed words throughorder6, then checks
14380GOODwords/168376GOODwordphases/12908simultaneouspairs. Classpair flags
exercise p0,p1,p>=2. Larger modelscheckactualsets/allphases, no largeexactoptima.
The25page workingmanuscript replaces theolder31/314subsection5.5,compiledtwice
andrendered/visuallychecked. CurrentMailrefresh/localindexstill5NovROWID26549;
servercompletenessunproved. NoLean,maildraft/send,MacStudio,submission orOctoberpaperchange.
GoalACTIVE foroptimalgraph/templatecoefficients,cubicspecifiedstar existence,
simultaneous physicalmultiHall completion,unit5/6 andgrid equality.


## Earlier unrestricted subcubic bound31/314: joint margin and physical boundary

The [joint-margin theorem](JOINT_MARGIN_AND_UNIFORM_SUBCUBIC_BOUND.md) proves
`314(|S|-beta_2(G))<=31n` for every minimal S in every finite simple bipartite
maximum-degree-three graph, including empty graphs. Its bound was
`SF_2-beta_2<=floor(31n/314)`. No connectivity, positive minimum degree,
side-balance or selected-component condition. The improvement over8/81 is
exactly1/25434; sharpness remains open.

A single shared allocation pays bad physical-path triples and bad auxiliary
path flags. Good ordinary components and good endpoint events strengthen
actual template sets. The physical boundary slots permit a second actual
full-graph construction with an exterior independent set. These are compared
with the retained-set alternative, never united. The exact seven-term
nonnegative certificate is62n-628d=W+61r+147(alpha+pi)+86(e-b3)+25b3+60q+294tau.

Exact23-file independent audit ACCEPT, including subsection5.5/abstract,
with original full checker execution and direct fresh-report comparison;
see `output/joint-margin-review.json` for complete evidence. Local checker
exit0 in10.805315500008874s, empty separately captured stderr;43,862minimal
sets,5,200exact small templates,19,938phases,36,520endpoint witnesses and
15,137conditional checks. Targeted controls include mixed-cycle loss,
bad-prefix triple and auxiliary-path flag on one class with disjoint physical
supports. Larger models have no unrestricted exact optimization claim.
Complete25page working manuscript compiled twice/rendered/visually checked.
No Lean, email, Mac Studio, submission or Octoberpaper change.
Full goalACTIVE for optimal graph/template coefficients,cubic specified-star
existence,simultaneous physical multiHall completion,unit5/6 and grid equality.


## Strict subcubic bound: all positive unrounded equality is impossible

The [zero-budget repair theorem](ZERO_BUDGET_REPAIR_AND_STRICT_SUBCUBIC_BOUND.md)
proves `81(|S|-beta_2(G))<8n` for every minimal S in every NONEMPTY finite
simple bipartite maximum-degree-three graph. Thus the unrestricted integer
bound is `SF_2-beta_2<=floor((8n-1)/81)`. No connectivity, minimum-degree,
selected-component or side-balance condition. All positive81d=8n equality
cases are settled negatively; they are no longer an open existence problem.
The graph coefficient is now improved to15/152 above; sharp graph and standalone-template13/5 questions remain open.

At sigma0 the new physical bound is `20beta(H)>=52b+3bO+t`.
Ordinary auxiliary components gain bO/4 by componentwise quotient replacement;
physical core paths gain t/12 in phase expectation, with disjoint resources
from core-cycle scores. Conditional expectations give actual compatible sets.
Template equality forcesQperfect andallcoredegree2. In the original equality
ledger, q0 closes the helper boundary as well; the extracted template is a
union of whole graph components. The remaining6mvertices have an independent
set of size3m, contradicting betaG41m via39m+3m. This avoids any assumption
that standalone-template equality is itself impossible.

Exact20-file independent audit ACCEPT, including manuscript5.4 and abstract.
Original full checker independently executed exit0 in19.268382722s, fresh
1387byte report byte-identical;19 non-report source hashes unchanged. The
full received startup warning/response is retained in
`output/zero-budget-repair-review.json`. Original local checker exit0;
no separate local timing orstderr claim. Counts:43,862 minimal sets,5,200
exact small templates,208 targeted zero models,624 phases,790 endpoint-event
witnesses,936 closed-extraction controls. No old main suites/Lean/large exact
optima. Working manuscript23pages compiled twice and visually inspected.
Cubic specified-star existence, simultaneous physical multiHall completion,
unit5/6 and arbitrary wide-grid triple equality remain open. Full goalACTIVE.


## Exact budget equality, integer refinement and a construction ceiling

The [exact owner-budget theorem](PHASE_BUDGET_EQUALITY_AND_METHOD_CEILING.md)
classifies sigma=0: ordinary phase classes are unions of whole monochromatic
core C4 components; each distinguished class has such components plus exactly
two remaining vertices. The two vertices need not be adjacent. Violating
classes contribute at least1/12 and1/6, respectively. Thus
`sigma>=N_O/12+N_D/6` and the same constructions give
`5beta_2(template)>=13b+3sigma`, yielding
`81d<=8n-3sigma<=8n-(N_O+2N_D)/4` for the original fixed extraction.
These are budget equalities and quantitative witness constraints, not
an equality-graph classification or vertex-edit stability theorem.

Positive unrounded equality81d=8n forces
`n162k,d16k,a=p=2k,b30k,b3=0,u62k,R32k,S98k,beta82k` for k>=1.
The parity proof yields the unconditional refinement
`SF_2-beta_2<=floor(8n/81)-1_{n=81 mod162}` for every nonempty
bipartite maximum-degree-three graph. The earlier strict theorem excludes all those equality cases; the joint-margin theorem above now improves the real coefficient too.

A connected50-vertex template has exact value26 within each of the two
specified one-core-side QUOTIENT construction families and every full
auxiliary phase with exact residual optimization, but an explicit
unrestricted dissociation set has27. Its sigma is zero. Disjoint unions
extend this precise method obstruction to all scales; no connected50t
claim for t>1, unrestricted beta50 value or arbitrary one-core-side
optimization claim is made.

Independent exact20-file review ACCEPT includes the final manuscript
subsection5.3. The unchanged full new checker ran with assertions, exit0
in16.115s; its fresh1462-byte report was byte-identical and19 non-report
source files were unchanged. The reviewer response abbreviates an unrelated
spreadsheet-startup stderr warning; that limitation is explicit in
`output/phase-budget-equality-review.json`, which retains the full response.
Local checker exit0 in11.3837s, empty stderr. The21-page manuscript was
compiled twice and visually checked. No Lean, email or submission.
All outstanding collaboration problems listed below remain tracked.


## Earlier unrestricted bound8/81 and sharp phase coefficient1/3

The complete [cycle-event pairing proof](SHARP_ODD_CYCLE_PHASE_COMPENSATION.md)
proves `81(|S|-beta_2(G))<=8n` for arbitrary minimal two-star-forming S in
bipartite maximum-degree-three graphs. The new partial-template13b/5 estimate
permits partial interfaces and unbalanced original sides. The key exact
phase expectation has sharp coefficient1/3, witnessed at all scales by
unions of an explicit connected30-vertex template. Actual alternative sets
are compared; all retained R vertices and chosen triple leaves lift together.
The previous19/192 and31b/12 milestones below are superseded.

The [core-cycle refinements](CORE_CYCLE_GAP_CERTIFICATES.md) give the
correlated square correction and a longer-cycle hierarchy approaching5/51;
none of these graph coefficients is asserted sharp. The manuscript contains
all new proofs. The separate sharp-phase and core-cycle execution reports
record their exact finite control scopes; imported older main suites are not
implicitly rerun. The exact final independent audit, including the corrected
8eta denominator explanation and manuscript translation, is in
`output/sharp-phase-compensation-review.json`: ACCEPT, both original full
checkers actually run, fresh reports byte-identical and all17 non-report
files unchanged. The first timing-wrapper launch failed before any checker
started; the successful original runs exited0 with empty stderr. Cubic specified-star positive-gap
existence, general physical multi-Hall routing, unit5/6 and arbitrary wide-grid
triple equality remain open. No Lean, mail or submission accompanies this batch.


## Earlier odd-cycle milestone: unrestricted bound19/192

The [stronger partial-template proof](ODD_AUXILIARY_CYCLE_COMPENSATION.md)
proves `|S|-beta_2(G)<=floor(19n/192)` for every inclusion-minimal
two-star-forming set in every finite simple bipartite graph of maximum
degree at most three. No connectivity, minimum-degree or selected-component
restriction. The previous11/111 coefficient is superseded; the new bound
improves it by1/7104 and1/10 by1/960. Optimality is open.

The template estimate is now `beta_2>=ceil(31b/12)`. Every odd quotient
cycle has two owner phase classes of order2 modulo4. An intact class has
an isolated non-C4 cycle; a broken class has at least two internal
low-degree vertices. Their separate credits do not overlap. Exact
conditional expectation constructs a phase certificate with gain o/4,
while the complementary one-side certificate has gain b/4-o/2.
Taking a convex combination of their guaranteed cardinalities cancels o;
the actual certificates are alternatives, never united. Simultaneous
retention and the exact nonnegative identity complete the global proof.

Independent fixed11-file review returned ACCEPT, including the faithful
manuscript integration. The reviewer ran the original full command
`python3 -B scripts/check_odd_cycle_compensation.py`, exit0 in19.3236s,
and reproduced the1389-byte report exactly. The unrelated Python startup
spreadsheet-runtime warning is preserved as received, with the full
response and manifest in `output/odd-cycle-compensation-review.json`.
Locally, the unchanged checker ran in7.9933s with empty stderr. It checks
43,623 minimal selections;5,200 exact partial templates;19,668 phases;
17,732 independent residual recurrences;14,054 conditional-expectation
comparisons;56 targeted all-phase models;and9 larger certificate-only
models, up to order760. General proof and finite checks have distinct roles.
The full18-page working manuscript was compiled and visually inspected.
No Lean, graph-sharpness, cubic specified-class existence or new grid result.

The earlier cubic existence task ended `response_timeout` without a
mathematical answer; it is not an active result or a nonexistence proof.

## Uniform subcubic improvement without selected-component restrictions

The [new partial-template proof](UNRESTRICTED_SUBCUBIC_GAP_IMPROVEMENT.md)
gives `|S|-beta_2(G)<=floor(11n/111)` for every minimal two-star-forming S
in every finite simple bipartite graph with maximum degree at most three.
There is no connectivity, minimum-degree or selected-component restriction.
It strengthens the previous equality-only exclusion to a uniform smaller
coefficient. Its template permits unbalanced sides, core maximum degree two
and partial witness matchings. Retaining all chosen selected triple leaves
simultaneously with R minus I0 yields the final nonnegative identity.
The complete argument is also in the working joint manuscript. Graph sharpness
remains open. Independent exact-source review and the final manuscript-consistency review
both returned ACCEPT. The final original checker ran unchanged with assertions,
exit0 and empty stderr, and reproduced the1070-byte report exactly. A minor
diagnostic label was corrected; the proof and algorithms required no change.
See `output/unrestricted-subcubic-gap-review.json` for both exact-source scopes.

The local original checker passes 43,623 minimal-selection checks. It checks
all minimal sets of 4,973 labelled graphs through order seven and 90 seeded
graphs at orders eight through twelve, the distinguished minimal set of each
of 5,200 exhaustively generated partial templates, and all 345 minimal sets
of the Heawood graph. There are 48 larger template certificate controls. The actual
report is `output/unrestricted-subcubic-gap-check.json`; finite tests support
the implementation, while the all-order theorem follows from the written proof.

The separate [integer boundary proof](CUBIC_SELECTED_STAR_SMALL_ORDER_OBSTRUCTION.md)
excludes every positive cubic specified-star/edge/isolate gap at orders below26.
Its two-source proof-only audit returned ACCEPT, with the established ledger
as premise. It does not exclude all n=24d equality cases or settle existence;
see `output/cubic-selected-star-small-order-review.json`.

## Completing degrees preserves minimality, but need not preserve a gap

The [regular-completion lemma](REGULAR_COMPLETION_CAN_DESTROY_SELECTED_GAPS.md)
works for every target degree r>=2 and any minimal two-star-forming set
whose old unselected vertices already have degree r. Appropriate new
selected edge components and unselected vertices fill every remaining
selected degree deficit. A cyclic incidence construction proves simple
completion exists; each old deletion failure and every new endpoint's
deletion failure remain valid. No selected-component hypothesis is needed.

The same note proves an all-k obstruction to gap preservation. The original
connected subcubic G_k has n48k, selected32k and true beta_2=31k. Its
completion K_k is two-connected cubic with n68k and selected36k, yet has
an explicit dissociation set of size38k. Its selected gap is at most-2k.
Thus this completion is safe for minimality while failing the desired
gap invariant. It does not decide the existence of positive cubic gaps
within the selected-star/edge/isolate class, or any unrestricted SF_2 value.
The all-scale argument uses one explicit fixed38-set and the old core cap,
not extrapolation from sampled completions. Exact-source review and
physical validation are in `output/cubic-completion-gap-loss-review.json`
and `output/cubic-completion-gap-loss-check.json`.

## Two-colour repairs: current subcubic upper bounds

The [two-colour repair theorem](SUBCUBIC_TWO_COLOUR_REPAIR_BOUND.md) proves
`d<=floor(4n/57)` at maximum degree three, `d<=floor(8n/121)` when the
minimum degree is also at least two, and `d<=floor(n/24)` for cubic graphs.
Here d=|S|-beta_2(G), with unrestricted beta_2, and S is a specified
inclusion-minimal two-star-forming set inducing stars, edges or isolates.
There is no connectivity assumption. The general maximum-degree bound
allows pendant and isolated vertices. These improve the older upper
certificates recorded below without changing their historical statements.

The key exchange inequality is `3d<=c+s+b2+b3`: complementary colour
constructions share one fixed witness assignment, and each necessary
private-witness or selected-helper deletion is charged at most once across
the two constructions. Explicit nonnegative identities supply all three
coefficients. Their proofs do not depend on a numerical optimizer or on
finite extrapolation. The checker covers degree-zero/one inputs, claws,
direct centres, twice/triply shared helpers, and both repairs on physical
graphs. Its full evidence and independent review are in
`output/subcubic-colour-exchange-check.json` and
`output/subcubic-colour-exchange-review.json`.

The [compact two-connected family](COMPACT_SUBCUBIC_SELECTED_STAR_GAPS.md)
has `n=64k, |S|=40k, beta_2=39k` for all k>=1, minimum degree and vertex
connectivity two and maximum degree three. Thus the best asymptotic
coefficient for this selected class, even restricting to two-connected
minimum-degree-two graphs, lies between 1/64 and 8/121. Its exact value,
cubic selected-class sharpness and low-degree-four/five sharpness remain
open. These are distinct from unrestricted SF_2 questions.

The full rectangular triple equality when both dimensions are at least
six, simultaneous physical completion for multiple Hall regions, the
universal unit-weight 5/6 improvement, and the simpler local incomplete-core
criterion also remain open. The existing multi-region theorem counts
endpoint budgets; it does not supply compatible geometric routes or a
full auxiliary matching. The full collaboration objective remains active.

## Subcubic positive gaps and exclusion of every cubic equality point

The [90-vertex subcubic construction](TWO_CONNECTED_SUBCUBIC_SELECTED_STAR_GAPS.md)
proves that, for every k>=1, n=90k, a specified minimal selected-star set
has size56k and true beta_2=55k, with minimum degree2, maximum degree3
and two-connectivity. The selection consists only of P_3's and isolates.
The general proof uses a ten-P_6 normalization obstruction, disjoint
attachment caps, a spanning ear certificate and cyclic safe-port gluing.
The two local checkers also establish the
[all-scale cubic equality obstruction](CUBIC_SELECTED_STAR_EQUALITY_OBSTRUCTION.md):
`d<=floor((n-2)/22)` in the specified selected-star class. Equality in
the previous n/22 certificate would force the private witness graph
to be a union of C_4's and the helped witnesses to form a matching;
balanced orientation of its quotient constructs a larger dissociation
set and excludes equality. These results do not give exact SF values,
an optimal subcubic coefficient, or a rectangular-grid theorem.

For **every integer delta>=3 and k>=1**, there is a finite simple bipartite
graph G with a specified inclusion-minimal two-star-forming selection S
inducing P_3's and isolates, such that

    n=14(delta-1)k, |S|=8(delta-1)k, beta_2(G)=7(delta-1)k,
    kappa(G)=delta(G)=delta, Delta(G)=4delta-7.

Thus the selected gap is exactly n/14 and attains the general coefficient
Delta*n/(12Delta+8delta-14), even at the maximum possible vertex
connectivity for its minimum degree. Here beta_2 is unrestricted; the
new families do not establish exact unrestricted SF_2 values.

| Construction | Range and mechanism | Exact result |
| --- | --- | --- |
| [Four selected-leaf ports](THREE_CONNECTED_DEGREE_THREE_THRESHOLD.md) | delta3,Delta5; arbitrary colour-preserving perfect port matchings | n28k, selected16k,beta14k for every interface; kappa3 exactly when the quotient has no edge cut of size<3 (k>=2); all k1 pairings are three-connected |
| [Dense witness multiports](MAXIMALLY_CONNECTED_DEGREE_THRESHOLD.md) | delta>=4; simultaneous diagonal deletions and parallel bundles | n14pk,selected8pk,beta7pk,kappa=delta=p+1 at every scale |
| [Balanced omissions](BALANCED_OMISSION_DEGREE_SHARPNESS.md) | t>=2,p>=max(t,5),t divides3p; delta=t+1,Delta=(4t-3)p/t | Gap pk=Delta*n/(12Delta+8delta-14), two-connected; includes(delta,Delta)=(4,15) |
| [Earlier uniform omissions](SHARP_HIGHER_MINIMUM_DEGREE_SUBFAMILY.md) | delta>=3,Delta=(4delta-7)r,r>=3 | Same exact coefficient, two-connected |

The degree-three cap is a direct arbitrary-dissociation-set argument by
witness distribution, with one shared connector capacity. An ordered
attachment proof handles every two-vertex cut and gives the exact quotient
criterion for arbitrary port interfaces. For larger minimum degrees, the
fixed witness kernel survives simultaneous deletions and disjoint bundles
retain kappa=delta. These are general proofs; finite optima are controls.

Separate final Oracle audits accepted each new theorem and executed its
unchanged original checker, reproducing the complete expected report
byte-for-byte. The dense maximal-connectivity audit exited0 and captured
1,064bytes of unrelated Python-startup spreadsheet-runtime stderr; its full
warning is preserved rather than reported as empty. Exact process streams,
manifests and execution qualifications are retained in the respective
output/*-review.json files. The exploratory four-port recurrence/table is
not a proof premise: the final source supplies a direct analytic argument.

The [degree-three single-port theorem](DEGREE_THREE_THRESHOLD_AND_SELECTED_PORT.md)
and [dense single-port theorem](DENSE_WITNESS_DEGREE_THRESHOLD.md)
remain as intermediate results. Every outside-to-outside port is unsafe in
the28-point degree-three base, so allowing selected-to-outside ports is
essential there. Other degree pairs, regular sharpness, wide rectangular
equality, compatible multi-Hall routing and a universal unit-weight5/6
improvement remain separate problems.

## Stronger shared degree cuts

The [combined centre/leaf degree cuts](COMBINED_CENTRE_LEAF_DEGREE_BOUNDS.md) strengthen the selected-star
bound at minimum degree at least3. Every specified minimal selection in
the stated class satisfies both
`d<=floor((Delta-1)n/[12(Delta-1)+4delta-6])` and
`d<=floor(Delta*n/[12Delta+8delta-14])`. The second is strictly stronger
for Delta>=delta>=3. They retain one actual unused-vertex capacity across
all counted selected types; no capacity is allocated independently per type.
The independent final exact-source audit returned ACCEPT, ran the original
checker to exit0 and reproduced its complete22,210-byte report exactly.
Other whole-cut/regular/cubic certificates remain applicable and should
be combined by taking their minimum. Sharpness now follows on the higher-degree parameter subfamily above;
other degree parameters remain separate questions.

## Sharp coefficients at minimum degree two, for all maximum degrees>=6

The [sharp minimum-degree-two theorem](SHARP_MINIMUM_TWO_DEGREE_BOUND.md)
closes the optimal coefficient for every maximum-degree allowance Delta>=6,
even with two-connectivity. For each p=Delta-1>=5 and k>=1 the explicit
bipartite family has n=(12p+2)k, a minimal selected-star/isolate set of
size8pk, true beta_2=7pk, minimum degree2 and maximum degree p+1. Its
selected gap pk attains the free-unused upper coefficient
`(Delta-1)/(12(Delta-1)+2)`. A single explicit circulant construction and a pure combinatorial
three-case cap prove the result for every p>=5, with no finite base-cap
premise. A separate exact witness-interface formula keeps one total degree
capacity at each unused vertex and independently verifies the implementation. At maximum
degree6 the coefficient is exactly5/62, closing the earlier interval.
The local checker passes556 interface graphs,2,819,008 independent one-part
subsets, all59,049 p5 ternary wing states and29 physical family models.
The independent final direct-proof audit returned ACCEPT, reconstructed
all9 source files, ran the original checker unchanged to exit0, and reproduced
the complete331,532-byte report exactly. The earlier fixed-base source
also received its own separately recorded ACCEPT. These claims concern
specified minimal selections inducing stars/edges/isolates; exact SF
values, sharpness at degree parameters outside the new subfamily,
minimum-degree-two maximum-degree3..5 sharpness in this class, regular selected-star sharpness
and general rectangular-grid equality remain separate questions. The maximum-degree2/minimum-degree2 case is
already settled by the earlier cycle theorem in SUBCUBIC_STAR_FORMING_GAPS.md.

## Free-unused-vertex refinement and bounded-degree lower families

The [free-unused-vertex refinement](FREE_UNUSED_VERTICES_AND_DEGREE_REFINEMENT.md)
proves, for every specified selected-star/edge/isolate inclusion-minimal
forming set in a nonempty bipartite graph with minimum degree at least
delta>=2 and maximum degree at most Delta,
`d<=floor((Delta-1)n/(12(Delta-1)+2(delta-1)))`. It strengthens the earlier
minimum-degree certificate for every feasible parameter pair. The proof
uses one fixed unused-vertex partition in both the enlarged colour exchange
and the degree-capacity count. Positive unrounded equality is impossible
when delta>=3. The proof-only review and the integrated exact-source/execution audit both
returned ACCEPT. The final auditor reconstructed all10 exact files, ran
both unchanged original checkers with assertions to exit0, and reproduced
both complete reports byte-for-byte. The full record is in
`output/degree-refinement-and-lower-family-review.json`.

The [two-connected bounded-degree family](TWO_CONNECTED_BOUNDED_DEGREE_SELECTED_GAPS.md)
has n=(12p+2)k, selected size8pk, true beta_2=7pk, minimum degree2 and
maximum degree2p+2, for every p>=2,k>=1. The proof uses disjoint P3/C4
partitions and an optimum avoiding all gluing endpoints. At maximum degree6
it gives selected gap n/13, while the new upper bound is5n/62. This earlier
family supplies the1/13 lower endpoint; the new sharp theorem above
attains5/62 and closes that interval. Local checks passed455 small graph
inputs,24,096 witness allocations and nine separately labelled targets,
and28 physical family models with7,280 literal deletion failures.
These results concern specified minimal selections, not an exact SF value
or general rectangular-grid equality. The new family is not regular.

## Direct witnesses and the strengthened cubic bound

The [direct-witness exchange](DIRECT_WITNESS_EXCHANGE_AND_CUBIC_BOUND.md) strengthens the colour ledger to
`t-s-q>=2d`: direct centre witnesses can be retained along with leaf
witnesses. An exact nonnegative whole-cut identity then improves the
cubic selected-star bound from `floor(7n/146)` to `floor(n/22)`.
The signed version at maximum degree three retains actual S/U degree
deficits. A general correction also proves `4beta_2>=2|S|+n-u`, where u
counts the outside vertices unused by one permitted witness assignment;
the padding family attains its coefficient of u exactly. These are
complete general proofs, with 876 graph inputs,23,499 witness allocations
and ten targeted finite models checked independently. No graph-sharp
cubic coefficient or unrestricted SF bound is asserted. Final exact-source
review returned ACCEPT, reconstructed all11 files, and ran both original
entry points unchanged with assertions. Both reports reproduced byte-for-byte;
see `output/selected-star-integrated-review.json` for actual execution scope.

## Exact padding and fixed minimum-degree/connectivity sharpness

The [exact universal-padding theorem](BIPARTITE_UNIVERSAL_PADDING_AND_CONNECTIVITY.md) proves, for every r>=2 and t>=1,
a bipartite selected-star family P_(r,t) with n=12r+2t, selected size8r,
true beta_2=max(7r,6r+t), and minimum degree and vertex connectivity both t+1.
For each fixed h>=2, taking t=h-1 gives h-connected graphs of minimum
degree h whose selected gap/order tends to1/12. Thus the sharp universal
selected-star coefficient remains asymptotically sharp under any fixed
lower bounds on minimum degree and vertex connectivity; maximum degree
is unbounded here. Taking t=r instead gives beta_2=n/2 but selected gap r,
refuting the candidate general inequality4beta_2>=2|S|+n even with no
selected edge components and arbitrarily high connectivity. These are
nonregular graphs, not full rectangles. A general exact padding formula
also covers isolated old vertices. The standard-library checker passes
1,364 exact padded small models,2,558 literal minimality-preservation
checks,6 exact family optima and2,498 vertex-split flows. The written
all-parameter proofs received independent proof-only ACCEPT. The final
integrated source/execution audit also returned ACCEPT, with both complete
reports reproduced byte-for-byte by the unchanged original programs.

## A regular selected-star gap family and exact cyclic composition

The [cyclic outside-edge composition theorem](REGULAR_SELECTED_STAR_GAP_FAMILY.md) now gives an explicit
two-connected four-regular bipartite family of order68r with true
`beta_2=35r` and a minimal selected-star/edge/isolate set of size36r,
for every positive r. Thus regularity and two-connectivity allow a linear
selected-star gap. The general theorem assumes that deleting a specified
outside port edge preserves beta; its proof gives exact beta addition
under cyclic switching and preserves every single-deletion witness.
The fixed68-point base and its deleted-edge cap have independent exact
integer max-sum certificates; no MILP result or finite lift sample is
used as a proof for all r. Another outside edge raises the deleted cap
to36, showing why that hypothesis needs verification. The coefficient
1/68 is an explicit lower family below the selected-star upper1/34;
no exact SF or graph-sharp coefficient is asserted. Independent review
returned ACCEPT, reconstructed the four exact source files, and ran the
original checker unchanged to reproduce its full report byte-for-byte.
See `output/regular-selected-star-gap-review.json`.

## Sharp selected-star coefficient without a clean-leaf assumption

The [complete proof](SHARP_SELECTED_STAR_GAP.md) establishes
|S|-beta_2(G)<=floor(n/12) for every minimal forming selection whose
selected components are stars, edges or isolates in a finite simple
bipartite graph. No clean leaf at every centre is assumed. Direct centre
witnesses enter the incidence ledger, while a capacity-one matching of
centres to twice-touched selected isolates gives simultaneously valid
repairs. Two exact weighted combinations prove the coefficient and
quantitative remainder bounds. Connected degree-six graphs attain it.
Positive equality forces c P3 components, c pendant selected isolates,
2c leaf witnesses, and degree two at every selected centre/leaf. Thus
minimum degree at least two yields floor((n-1)/12) for these selections.

The standalone audit passes on 5,399 graphs, 599,877 selected subsets,
39,880 witness assignments and 80,912 repaired sets, plus nine targeted
models and 22,937 feasible integer-ledger controls. Both independent proof reviews returned ACCEPT. The final reviewer
reconstructed all four exact artifacts, verified their hashes, ran the
original checker unchanged with assertions to terminal completion, and
reproduced the 27,335-byte report exactly. The complete response and execution
scope are in `output/selected-star-general-budget-review.json`. This does not assert that a maximizing minimal selection in
every bipartite graph or full rectangle has selected star components.

## Minimum-degree and maximum-degree refinement

For the same selected-star class, nonempty graphs with minimum degree at
least delta>=2 and maximum degree Delta satisfy the stronger bound

    |S|-beta_2<=floor(L*n/(12L+2(delta-1))),
    L=max(7(delta-1),Delta).

In particular minimum degree two and maximum degree at most seven give
floor(7n/86). The complete [proof](SELECTED_STAR_MINIMUM_DEGREE_BOUND.md)
counts real edges from singly touched selected isolates into unused outside
vertices and retains one exact global vertex remainder. Both degree reviews
returned ACCEPT; original checker executions reproduced their corresponding
reports exactly. The final public checker tests 727,240 feasible ledgers
and a real 38-vertex graph (minimum degree2, maximum8, selected24, beta22)
using 524,288 independent one-part subsets. The coefficient is not claimed
sharp, and this is a bound on specified selected-star minimal sets.

## Whole-cut capacity and boundary deficits

The [whole-cut degree theorem](FULL_DEGREE_CAPACITY_FOR_SELECTED_STARS.md)
counts the degree demands of all selected vertex types in a single cut and
adds the bipartition bound `beta_2>=n/2`. For the same selected-star minimal
sets, minimum degree at least delta>=3 and maximum degree at most Delta>=4 give
`d<=floor((Delta-delta+1)n/(2(5Delta+delta-7)))`. In regular degree k>=4 this
is `floor(n/(12k-14))`; cubic graphs satisfy `floor(7n/146)`.
A positive gap in regular degree at least four requires selected edge
components, with an explicit lower bound on their number of vertices.
The constants are optimal in the explicitly stated six-ledger relaxation
for the proved parameter ranges; graph-sharpness remains open.

Retaining actual degree deficits also gives a boundary-sensitive version
without a minimum-degree assumption. In a full h-by-w rectangle it implies
`d<=floor((hw+4h+4w)/34)` for every specified selected-star minimal set,
with a stronger location-dependent form in the note. This does not assume
that all minimal grid selections are of that form. Literal finite checks
and exact rational controls pass. The final [ACCEPT audit](../output/full-degree-capacity-review.json)
reviewed the complete proof, reconstructed all five files with matching
hashes, ran the original checker unchanged with assertions to completion,
and reproduced the report byte-for-byte.

The [regular equality-interface theorem](REGULAR_SELECTED_STAR_EQUALITY_INTERFACE.md) further shows that
positive equality `n=(12k-14)d` requires exactly d P3 centres in each
bipartition class and a witness interface with d vertices of degree k-1
and d of degree k-2 in each part. Thus `d>=floor(k/2)`: equality at
order34 in degree4, or order46 in degree5, is impossible. The necessary
witness interface is explicitly realized for every admissible k,d; this
is not a whole extremal graph construction. The same resource theorem
gives `d<=floor((h+w)/4)` in a full rectangle when S has no selected
edge components. Independent proof review returned ACCEPT; its scope
contains no new code-execution claim.

## Exact clean-witness port composition

For any finite simple interface graph R, orient its edges arbitrarily and
join the clean witness ports of copies of G_(1,1). The
[general composition theorem](SELECTED_STAR_PORT_COMPOSITION.md) proves
beta_2(F_R)=7r+alpha(R), while an explicit minimal forming selection has
size8r and only P3 stars/isolates. A full eight-set in a block forces both
internally matched ports, so the full blocks must form an independent
set. Seven-sets omitting both ports attain every complementary block.

Path interfaces give connected maximum-degree-four examples at all orders
12r with beta_2=7r+ceil(r/2), and selected deficit floor(r/2). Cycles give
beta_2=7r+floor(r/2) and deficit ceil(r/2) for r>=3. The r=2 path has
selected16 and true beta15. This is a genuine unrestricted gap. All-size
proofs and an independent checker received **ACCEPT** with no correction.
All three original artifacts were reconstructed with matching hashes; the
original checker ran unchanged with assertions and reproduced its entire
60,288-byte report. Its84 exact-solver calls cover up to48 vertices; the
22 large-family entries up to1536 vertices check certificates, with all-size
optimality supplied by the proof. See `output/selected-star-ports-review.json`.
No exact SF value or rectangular-grid conclusion is asserted.

## Genuine selected-star gaps and a sharp clean-leaf bound

The [complete new proof](SELECTED_STAR_COMPONENT_GAPS.md) refutes the
unrestricted selected-star minimal-set inequality. A connected18-vertex
bipartite graph has a minimal12-set inducing only P3 stars and isolates,
while its true unrestricted dissociation number is11. The general family
G_(a,b) has6(a+b) vertices, minimal selected size4(a+b), and exact
beta_2=3(a+b)+max(a,b,2), proved by four exhaustive structural cases and
three explicit attaining sets. Its forced leaf-retaining optimum is
3(a+b)+max(a,b), which equals the true optimum except at(1,1).

For every such selected-star/edge/isolate selection whose every centre
has a clean leaf with a private outside witness, a general distinct-helper
budget proves |S|-beta_2<=floor(n/12). The assumption is explicit; it is
not inferred from minimality. Connected maximum-degree-six graphs attain
this coefficient at all orders24r: |S|=16r and beta_2=14r. All-size proofs,
actual graph certificates and independent finite checks are included.
Independent review returned **ACCEPT**, with no mathematical correction. All
four original artifacts were reconstructed with matching hashes; the unchanged
checker ran with assertions and reproduced its entire report byte-for-byte.
See `output/selected-star-gap-review.json`. These graphs have pendant vertices and
are not full rectangles; no exact SF_2 value is asserted for them.

## Matching exchanges that retain selected star leaves

The [new exact exchange formula](STAR_LEAF_MATCHING_EXCHANGE.md) is

    max_(D subset S union W, L subset D, Delta(G[D])<=1)|D|
       =|S|-c+e-nu(G[W union I]).

Here selected components are stars/edges/isolates, c counts nontrivial star
centres, L their leaves, e=|L|=|W|, and I is the set of all selected isolates.
Witness conflicts and shared isolates appear in one bipartite graph, with
matching/cover dual certificates. At most one selected isolate implies the existence
of a dissociation set of at least |S| for every such minimal forming set,
even when centres occupy both bipartition classes and witnesses conflict.
The distinct-helper bound e-t>=2c-1 is another sufficient criterion. The
matching formula also certifies the prior full6-by-6 independence obstacle,
where c=2,e=4,nu=2 and the exact leaf-retaining optimum is18.

A connected bounded-degree family shows the exact limitation. Its minimal
forming S has size8r and beta=8r, while every dissociation set retaining all
star leaves has size at most7r. Four disjoint P3 paths per block prove the
true upper bound; explicit dissociation sets and matching/cover certificates
attain both values. It has12r vertices,15r-1 edges and maximum degree5 for
r>=2. The leaves' witnesses are unique and constitute every outside vertex,
so alternative witnesses or additional outside vertices cannot repair
leaf retention. These are full all-r proofs, with a standalone finite
checker. Independent review returned **ACCEPT** with no mathematical
correction: all three artifacts were reconstructed with matching hashes,
the original checker ran unchanged with assertions enabled, and its
50,622-byte report was reproduced exactly. See
`output/star-leaf-budget-review.json` for the complete response and scope. The broader selected-star inequality is refuted by the new construction
above. Arbitrary full-grid equality remains open.

## Geometry at arbitrary width

The [witness geometry note](GRID_WITNESS_GEOMETRY.md) proves, for every
minimal forming S in every full rectangle,

    2|S|-mn<=|Z|+|E|-|H|-ceil(K/2).

Here Z comprises selected components of order at most two, E the degree-two
or degree-three selections without a direct deletion witness, H the
degree-four selections, and K counts selected perpendicular siblings of
chosen clean leaves at exceptional centres. Two caps per H centre are
pairwise disjoint across distinct centres. Exceptional caps have capacity
at most two and are disjoint from H caps. Direct and clean witnesses are
reserved without counting the same leaf resource twice. The exact residual
identity retains the actual exceptional-cap union and unused omitted set.

A separate simultaneous auxiliary-multigraph exchange gives |S|<=beta_2
when selected components are stars/edges/isolates with independent chosen
leaf witnesses. This applies whenever selected degree-at-least-two vertices
lie in one bipartition class, at any width. A complete 6-by-6 example refutes
automatic independence but admits an explicit size-preserving exchange.
The finite audits cover 190,798 grid subsets, 28 protected degree-four
centres, and 50,196 exchange constructions on small bipartite graphs and
explicit cycle/dummy/conflict fixtures. General proofs are written in full.
The independent audit at2958b91 returned ACCEPT without mathematical
changes: all five manifest files were reconstructed, both original checkers
ran unchanged with assertions enabled, and both reports matched byte-for-byte.
Complete execution scope is in output/grid-witness-geometry-review.json.

## Five-row grids at every length

The [five-row proof](FIVE_ROW_STAR_FORMING_EQUALITY.md) establishes
`SF_2(P_5 square P_n)=beta_2=psi_sq=F(5,n)` for every positive n. The
value is 4,6,9 at n=1,2,3 and `8floor(n/3)+3(n mod3)` for n>=4. The
new conclusion is the SF upper bound. The same general deletion-witness
frontier, now stored compactly, gives complete vectors with 8,227,512
reachable states and the exact identity V17=V14+8. Transfer homogeneity
and exact initial values prove the result at arbitrary length.

The independent literal-star implementation compares all 33,554,432 local
kernel entries against the generator, reconstructs all seventeen prefixes
with standard unordered maps, compares every entry and complete support
at both endpoints, and verifies the translation. Its whole-board controls
compare individual subset acceptance with global minimality on 1,082,400
subsets of 5-by-1 through 5-by-4. The new generator also reproduces the
accepted h3/h4 endpoint vectors. Both existing width-five colouring
implementations were rerun and reproduced four archived outputs exactly.
No state truncation or new Lean execution is used. Independent final
review returned ACCEPT at c5d4c45: both original programs completed, both
large vectors were regenerated with exact hashes, and the checker report
and all four prior colouring outputs matched byte-for-byte; both dimensions of a still-uncovered rectangle must
now be at least six. Arbitrary-width equality and a universal 5/6 gain
remain open.

## The four-row extension

The [four-row proof](FOUR_ROW_STAR_FORMING_EQUALITY.md) closes the upper
forming number at height four for every positive length:
`SF_2(P_4 square P_n)=beta_2(P_4 square P_n)=2n+(n mod2)`.
An explicit alternating-column dissociation set attains the bound and has
self-deletion witnesses. The full-vector certificate is V17=V15+4, on all
342,768 reachable states in the 3^16 state domain. The general frontier
proof and homogeneous-transfer induction prove the infinite conclusion.

The independent Python implementation reconstructs both vectors by literal
stars and compares all entries. It also checks all 1,048,576 local masks
and 69,904 whole-board subsets. The vectors are regenerable output, with
their exact hashes in the concise report. With the prior width-four
colouring theorem, all three parameters coincide. This is a computer-assisted
result. The separate independent audit returned **ACCEPT**, ran both
unchanged implementations, and reproduced both reports byte-for-byte and
both vector hashes. It reconstructed the general frontier argument without
assuming the height-three numerical result. The reviewer-reported source
hashes match our pinned manifest; that manifest was not in their attachment.
[The review record](../output/grid-star-height-four-review.json) gives the
complete execution and provenance scope. No code or certificate changed.

## Upper forming number and triple equality at height three

The [three-row proof](THREE_ROW_STAR_FORMING_EQUALITY.md) establishes
`SF_2(P_3 square P_n)=beta_2(P_3 square P_n)=5floor(n/3)+2(n mod3)`
for every positive n. Together with Sahbi's prior width-three colouring
formula, it gives SF_2=beta_2=psi_sq on all three-row rectangles. The new
contribution is the SF upper bound, not a new colouring formula.

The exact frontier retains four columns with omitted/selected-unwitnessed/
selected-witnessed digits. All radius-two formation and deletion tests are
performed at the middle column of each five-column window. A general
soundness/completeness proof identifies accepted strings with globally
minimal forming sets. Both complete maximum-score vectors, at lengths
12 and 15, have 14,726 reachable states and satisfy V15=V12+5 entrywise.
Transfer homogeneity proves the recurrence for every later length.

An independent Python implementation uses literal star triples and
reconstructs both vectors from the empty prefix. It also compares every
44,954 selected subset on 21 small boards with literal global minimality.
The one-column boundary has its own corrected and exhaustively checked
tail. This is a computer-assisted theorem with a finite exact premise,
not scalar extrapolation. The independent audit returned **ACCEPT** and
ran both unchanged implementations and the prior Omega supplier. All
eight supplied result files were reproduced byte-for-byte; the reviewer
also reproduced the erroneous one-column tail and verified its correction.
The [review record](../output/grid-star-transfer-review.json) preserves the
complete answer, pinned source hashes and exact scope. The 33,824 local
patterns describe literal-kernel construction; the explicit per-subset
acceptance comparisons number 44,954. The full arbitrary-width triple
equality and universal 5/6 improvement remain open.

## Exact decoration formula and sharp path-residual values

The [decorated-interface theorem](EXACT_DECORATED_INTERFACE_FORMULA.md)
proves SF_2(D(H))=12|H|-sf_2(H) for every finite simple H. Each interface
vertex is replaced by the fixed 21-vertex F_2 module. A selected interface
with internal activity costs at least two of the twelve available units.
These extra units pay, once each, for any extra interface selections
needed to turn a globally minimal decorated set into a forming set of H.
Conversely every minimal forming set Q of H lifts to a minimal decorated
set of size 12|H|-|Q|. Taking Q minimum proves the exact identity.

For H=P_s, minimum forming sets have exact size
mu(s)=2floor(s/4)+min(s mod4,2), by selected-run counting and printed
attaining binary patterns. Hence the earlier connected residual has
SF_2(R_s)=12s-mu(s), and its single-ear discrepancy is exactly mu(s).
This closes the residual optimum, rather than merely proving it grows.
The roots in that family still have increasing degree; fixed-degree
error boundedness follows from the separate local-stability theorem.

The independent checker covers every interface graph through order 5,
all binary path strings through order 14, 1,265 lifted minimal sets, 70,717
specified deletion witnesses, and 44 seeded globally minimal decorations.
There is no exhaustive SF search over the large decorated graphs.
Independent **ACCEPT** reconstructed the general proof and dependencies,
ran the unchanged original checker with assertions enabled, and reproduced
its 550-byte report and stdout byte-for-byte. None of its original 1,309
upper-map calls triggers augmentation. The reviewer separately checked
two minimal decorations with 54 deletions, including two augmentation
indices choosing the same added vertex. A separate local literal-star
checker now reproduces these cases; its output is recorded separately.
The complete response and execution scopes are preserved in
`output/decorated-interface-review.json`.

## Fixed-degree local stability and arbitrary interfaces

The [local stability theorem](LOCAL_STAR_FORMING_STABILITY.md) proves,
for every finite simple graph G and U subset V(G), with H=G-U,

    SF_2(H)-b_3(U)<=SF_2(G)<=SF_2(H)+|U|+b_5(U),

where b_r counts surviving vertices within distance r of U. Its stronger
adaptive version repairs exactly the unformed residual vertices A,
which lie within distance two of U, and preserves all old selections
outside B_2(U) union B_3(A). Radius-three addition locality and radius-five
canonical-repair locality both have explicit sharp P9 witnesses. These
are sharp certificate radii, not sharp parameter-difference constants.

For k disjoint square ears, the exact two-selections cap improves this to

    0<=SF_2(G)-(2k+SF_2(F))<=|F intersect B_5(roots)|.

If Delta is the maximum degree of the final graph, its upper bound is
2k(Delta-2)sum_(j=0)^4(Delta-1)^j. Thus unbounded single-ear error
cannot occur at fixed maximum degree. The earlier unbounded examples
require growing root degrees, as their constructions explicitly state.
Deleting a general interface and using disjoint-union additivity gives
a two-sided composition estimate without assuming minimality of a
restriction to an arbitrary component.

The standalone literal checker passes1,100 exhaustive small graphs,
96 seeded larger graphs, the sharp P9 example and a claw regression:
973,858 induced-selection states,669,163 interface repairs and329 ear
models. The research-stage answer's overstrong all-minimal-set minimum
is explicitly rejected by the claw. Final statements use the correct
fixed-S inequality. Independent **ACCEPT** reconstructed the entire local proof and supplying
square theorem, ran the unchanged original C++17 checker with checks
active, and reproduced its622-byte report byte-for-byte. Exact input
hashes, full response and finite execution limits are recorded separately
in `output/local-star-stability-review.json`. No new Lean is claimed.

## Bipartiteness does not rescue exact partial-ear addition

The [bipartite obstruction note](BIPARTITE_PARTIAL_EAR_OBSTRUCTION.md)
gives exact connected families F_q,G_q, q>=1, with

    |V(F_q)|=10q+1, |V(G_q)|=10q+5,
    SF_2(F_q)=max(5q+1,6q-1), SF_2(G_q)=6q+2.

G_q is obtained by adding roots d,e with de,dy and attaching just one
square along de. Thus deleting the roots gives exactly F_q. For q>=2
the full SF exceeds2+SF(F_q) by one. Disjoint unions give an additive
error k with k ears, within bipartite graphs. The q=2 graph is connected,
has maximum degree five and exact SF=14, while the residual21-vertex
graph has SF=11. The violating selected pair in the ear is adjacent
and internally active; formation of the exterior y, rather than
root activity from the residual selection, permits the extra vertex.

The original Oracle research supplied the25-vertex lower witness and
residual upper proof. The local reconstruction proves the all-q local
caps with an arbitrary exterior at y, both residual attaining sets,
and the additional exact whole-graph upper bound6q+2. The independent
all-q audit returned **ACCEPT**, executed both unchanged original
checkers, and reproduced both reports byte-for-byte. The C++ checker
computes literal formation for all2,097,152 residual and33,554,432 final
subsets. A nonminimal set is rejected at its first forming deletion;
each accepted minimal set passes every deletion. It finds beta/SF=11/11
and13/14. Named-vertex certificates test q in {1,2,3,4,8,16,32,128},
not all integers up to128:16 models,3,314 deletions and1,180 specified
witnesses.

A stronger one-ear amplification has exact values

    |V(J_s)|=21s+4, SF_2(R_s)=11s, SF_2(J_s)=12s+2,
    SF_2(J_s)-(2+SF_2(R_s))=s.

Here the residual is the disjoint union of s copies of F_2, all attached
through their y vertices to a single root d. The base and final graph
are connected and bipartite. The arbitrary-exterior cap bounds each
copy by12; the common active root lets every copy attain12 simultaneously.
A separate independent **ACCEPT** reconstructs this all-s proof and ran
the unchanged new certificate checker, reproducing its report byte-for-byte:
s in {1,2,3,8,16,64}, six models and1,140 single deletions. The two complete
audits and exact input hashes are in
`output/bipartite-partial-ear-review.json`.

The [connected-residual amplification](CONNECTED_RESIDUAL_EAR_AMPLIFICATION.md)
adds a path through the y vertices and attaches its odd/even indices to
the two roots. It proves, for every s>=1,

    |V(R_s)|=21s, |V(J_s)|=21s+4,
    SF_2(R_s)<=12s-ceil(s/3), SF_2(J_s)=12s+2.

The base, final graph and residual are all connected and bipartite.
Every residual module contributing12 would omit y and all Z vertices;
formation of y then requires a selected neighbouring y, whose module
contributes at most11. The modules with a positive loss therefore form
a dominating set of the path, forcing at least ceil(s/3) total loss.
One active root pair removes this requirement in the final graph,
while each selected vertex retains a private deletion witness. The
single-ear discrepancy is consequently at least ceil(s/3). The residual
has maximum degree six; the final root degrees grow with s. The later
decorated-interface theorem above sharpens the residual bound to the exact
value 12s-mu(s), and the discrepancy to mu(s). The original proof and review
of this connected-residual construction establish the weaker domination
bound and the exact final-graph value independently of that later theorem.

The standalone checker passes seven sizes s in {1,2,3,4,8,16,64},1,190
single deletions and1,190 named witnesses, and32,766 path subsets. Its
independent review returned **ACCEPT** and ran this unchanged original
checker with assertions enabled, reproducing both its349-byte report
and stdout byte-for-byte. Its complete response and precise scope are
recorded separately in `output/connected-residual-ear-review.json`.
The reviewer also reconstructed the referenced square-ear lemma directly;
that accepted proof is now included in the note. The earlier audits do
not cover this later construction. All-s bounds rely on the written proof.

## Four exact parameters on two-connected outerplanar median graphs

The [ear-ladder family](EAR_LADDER_FOUR_PARAMETERS.md) gives, for every
r>=1, a graph of order16r, maximum degree4, two-connected, outerplanar
and median, with exact values

    beta_2=sf_2=SF_2=8r,
    psi_sq=Omega=9r.

The proof classifies the local representative budget of each attached
square. Only an opposite T pair with one old P root can exceed2 units,
contributing5/2. In each two-column ladder interval at most one of the
two row squares can have that type. This gives Omega<=9r, counting
each actual matching endpoint by one half. Alternating the selected
row in consecutive four-column blocks gives a legal9r-colour partial
sub-quorum colouring. The square-pair classification gives all star-forming
values and the exact dissociation value independently.

The standalone checker literally examines all65536 subsets of the
16-vertex base, its6668 actual matchings and1369324 possible disjoint
T subsets after the forced >=2-P-neighbour exclusion. It obtains
beta=SF=8, all1296 minimal forming sets, and Omega=9 without using the
exceptional-square upper proof. Ten sizes through r128 pass2620 coloured
closed-neighbourhood tests and2096 deletion witnesses. All-r statements
have the written proof; finite controls do not replace it.

The triple-equality extension to two-connected outerplanar median graphs
is therefore false. The weaker SF_2=beta_2 question in planar degree-four
median graphs remains open; this family satisfies that equality. It
does not consist of full rectangular grids. In fact H_r is the4-by-4r
grid with all between-pair edges on its first and last rows deleted;
for r=1 these are just two boundary edges. The note gives the explicit
coordinate isomorphism.

The new four-parameter theorem received independent **ACCEPT** at
snapshot a7737b0. The reviewer ran the original Python checker unchanged,
with assertions enabled, reproduced the report byte-for-byte, and
independently verified all-r counting, block-boundary colouring and
structural proofs. The checker does not enumerate all colourings or
calculate lower sf separately; those values follow from the proof.
Only a previous/next-block wording clarification and the explicit
coordinate identification were added afterward; no checker changed.
The complete response and exact scope are in
`output/ear-ladder-four-parameter-review.json`.

## Square attachments and the exact composition obstruction

The [square-ear note](SQUARE_EAR_STAR_FORMING_COMPOSITION.md) proves that
for an arbitrary finite simple base B and a matching of k old edges,
adding a square along each edge gives, with F the base minus all roots,

    beta_2(G)=2k+beta_2(F),
    2k+SF_2(F)<=SF_2(G)<=2k+|V(F)|.

Every minimal forming set selects exactly two vertices in each square.
For a perfect root matching all 6^k pair choices are precisely the minimal
forming sets, so beta_2=sf_2=SF_2=2k. There are companion pendant-path
formulas and a full-root classification with 3^k minimal sets.

The proposed exact SF addition for partial root sets is false. For every
m>=5 an explicit 6m-vertex square family has F=K_m disjoint-union K_m,
SF_2(F)=4, beta_2(G)=2m+4 and SF_2(G)=3m. The analogous pendant-path
example has 5m vertices and the same values. Full all-m upper proofs and
three explicit deletion witnesses per index explain the activity
dependency responsible for the error m-4. These families use cliques;
they do not refute a bipartite or median equality.

Square attachments preserve medianity, planarity and two-connectivity;
they preserve maximum degree four when all roots previously have degree
at most three. Fully covered ladders provide an infinite outerplanar
median degree-four class with no automorphism mapping every vertex to
a neighbour, and with all minimal forming sets classified.

The Python checker passes 329 square models,1099 path models,681648
literal subsets,126 fully covered models,2008 minimal-set lifts and58263
local-cap tests. It checks80 larger pair selections,7 structural median
models (including2 with interior-edge attachments),6651 metric triples,
117 vertex deletions, and2124 specified obstruction deletion witnesses.
The independent C++ implementation checks all7962624 two-per-square
sets and248832 two-per-path sets for m=5, obtaining exact SF=15 in both.
Its exhaustive domain uses the proved local-cap lemma; it does not
enumerate all 2^30 unrestricted subsets or assume the p/q upper proof.

## Restricted median graphs

The [restricted median note](RESTRICTED_MEDIAN_CUBE_CHAINS.md) reconstructs
the cube-chain theorem: in any finite planar median graph with Delta<=4,
every connected collection of intersecting induced cubes is an induced
convex C_4 square P_(r+1). External edges meet only the end layers and
number at most eight; when r>=2, each outside component attaches to one
end. Two-connectivity requires at least two attachment vertices per
nonempty outside component. Planarity is used through the bipartite
Euler bound, which excludes adjacent-face branching and cycles of cubes.

Every finite two-connected median graph with Delta<=3 is a ladder or
Q_3 and has SF_2=beta_2. The classification is explicitly attributed as a
consequence of Bandelt--Chepoi--Eppstein Proposition9, checked in the full
arXiv0905.4537v1 primary manuscript. The forbidden book has degree four;
the source's suspended cogwheels have hubs of degree at least five.
The existing bipartite prism theorem supplies the exact parameter values.

The structural checker passes39 models,84 cubes in24 components,69816
metric triples and786 vertex deletions. A nonplanar Q_4 control confirms
that degree four and medianity alone do not force the cube-chain property.
These checks support the implementation of the all-size proof. The
two-connected planar median Delta<=4 equality remains open, including
the exchange problem in cube-free squaregraph regions and compatible
activation/deletion data across square interfaces.

The independent complete-package audit found the new ear, pendant,
all-m obstruction and cube-chain arguments sound and ran all three
original checkers, reproducing every report byte-for-byte. Its verdict
was REVISE for one missing exact dependency locator: the upper-SF
prism theorem used in the parameter corollaries. The restricted note
now states that theorem precisely and links its complete proof at
957ef94, Section5 Theorem4/Corollary5, with definitions and the prism
isomorphism in Sections1/3. This supplier file is byte-identical to
the pinned revision. Targeted independent closure returned **ACCEPT**,
after reconstructing the full supplier proof and all three applications.
That closure did not rerun code or independently authenticate the remote
GitHub bytes; the local check verified that the supplied complete source
is byte-identical to the pinned Git object. The first complete audit's
three original checker executions remain the execution evidence.
Complete response and input scope are in
`output/square-ear-composition-review.json`. No new Lean execution is claimed.

## Median graphs: explicit failure and bounded-degree amplification

The [median obstruction note](MEDIAN_STAR_FORMING_OBSTRUCTION.md) proves
that for every r>=1 there is a connected median graph G_r with

    |V(G_r)|=38r, Delta(G_r)=5,
    beta_2(G_r)=21r, SF_2(G_r)>=22r.

The base is P_4 square P_4 square K_2 with two pendant leaves at each
of three lower corners. A four-cube pattern proof gives beta_2=15 after
removing those three attachment vertices; simultaneous leaf normalization
then gives beta_2=21. A 22-set has explicit witnesses for every deletion.
Bridging distinct leaf ports preserves medianity, the exact dissociation
value, and all minimality witnesses. This disproves the general median
SF/beta equality and shows a linear gap with a fixed maximum degree.
It does not determine exact SF_2 of these examples or refute rectangular-grid
equality. They contain pendant vertices and degree-five vertices.

The standalone checker passes all256 cube subsets, all4096 forced block
pattern tuples,893000 median triples, and10010 deletion witnesses over
10 family sizes through r=256. The written proof establishes the all-r
claim; the finite controls test its implementation. The original Oracle
research response supplied the fixed counterexample. A separate independent
review returned **ACCEPT** for the reconstructed proof and new connected
amplification. It inspected the checker source and supplied outputs but
did not execute code. Local execution and proof acceptance are distinguished
in output/median-obstruction-review.json. The final note makes the face
incidence count and the column containing the deleted vertices explicit.


## Arbitrary Cartesian prisms and their sharp gaps

The [complete prism note](ADJACENT_INVOLUTIONS_AND_PRISM_GAPS.md) proves

    SF_2(H square K_2)=Omega(H square K_2)=2n-nu(D(H))

for every finite simple H, with no bipartiteness requirement. The upper
witness argument extends to any graph with an adjacent involutory
automorphism; its quotient determines exact Omega and an SF upper bound.
Prism attainment uses a layer selection over the residual critical-set
graph, with explicit opposite-rung deletion witnesses. An arbitrary graph
with this involution need not attain the SF upper bound: K_(2n) has
SF_2=2 and Omega=n for n>=3.

Over all n-vertex bases, both maximum gaps SF_2-beta_2 and SF_2-psi_sq are
exactly max(0,n-4). For n>=5 their positive equality bases are respectively:

- K_n with any matching of edges deleted, for SF_2-beta_2;
- K_n or K_n with one edge deleted, for SF_2-psi_sq.

For H=K_n with m disjoint edges deleted, n>=5, the complete values are

| Parameter | Exact value |
| --- | --- |
| beta_2 | 4 |
| psi_sq | 4 if m<=1, and 5 if m>=2 |
| SF_2 and Omega | n |

These are all-size proofs. A complete-base prism is n-regular,
n-connected and vertex-transitive, so those properties alone do not
extend the bipartite four-way equality. The note also proves direct
terminal completion in any paired graph for every feasible independent
T, including selections using both layers. Independence excludes direct
TT paths; no such TT-free assertion is made for arbitrary adjacent T.

`python3 scripts/check_paired_graphs.py` passes 1,100 prism bases and
1,065,509 literal subsets, 60,296 minimal forming sets, 4,166 general
paired graphs and 1,052,741 further subsets, 89,860 further minimal sets,
6,715 representative pairs, 5,397 direct completions including 496
mixed-layer selections, and 3,396,244 canonical partial colourings over
79 models. The latter exhausts all bases through order four and three
near-complete bases of order five. Twelve larger prism certificates and
31 larger extremal-family certificates also pass.

The research-stage Oracle audit reconstructed and accepted all proposed
formulae and equality classifications; it did not inspect or run code.
The complete note, both new Python files and their existing matcher
dependency received independent **ACCEPT** at f44adbc. The reviewer ran
the original complete checker unchanged, with assertions enabled, and
reproduced the 813-byte report byte for byte. The final note clarifies
the n<=4 case of the gap corollary and refers explicitly to vertices of T
in representative attainment. Two later checker assertions require all
selected vertices to have deletion witnesses and connect the outer optimum
to its matching dual. A full local rerun with these assertions reproduced
the same report. The external run predates these small additions. Complete
responses and exact scopes are in `output/paired-graph-review.json`.
No new Lean verification or historical priority claim is made.

## Extended double covers and Cartesian prisms

The [complete extended-cover proof](EXTENDED_DOUBLE_COVER_PARAMETERS.md)
establishes, for every finite simple H of order n,

    SF_2(E(H))=beta_2(E(H))=psi_sq(E(H))=Omega(E(H))
              =n+delta(H)=2n-nu(D(H)).

The proof covers nonbipartite bases as well. The independent-set deficiency
delta(H) equals the ordinary double-cover Hall deficiency. A TP-to-PZ rung
injection bounds every feasible representative pair, allowing selected
vertices in both colours. A separate minimal-forming proof counts the
union of deletion witnesses with capacity two per empty rung. Neighbours
of isolated selected rung edges are reserved and contribute no witness
capacity to the other doubly selected rungs. This proves the SF upper
bound without a general-graph assertion SF_2<=Omega.

There are exact nonnegative remainders describing every optimal feasible
representative pair and every maximum minimal forming set in this class.
For example, a maximum minimal set can induce a square; the statement is
an equality of optima and includes these nondissociation maximizers.

The common value and an attaining set have polynomial matching/vertex-cover
certificates. If H is bipartite, E(H) is its Cartesian prism and the common
value is 2 alpha(H). This closes all four parameters on every bipartite
prism, including all ladders and all hypercubes of dimension at least two.
Taking a prism eliminates any SF_2/beta_2 gap in a bipartite base.

For arbitrary actual M and any feasible white selected set T, disjoint
two-rung swaps provide a full auxiliary matching that pairs all selected
vertices directly with black terminals. Thus the true TH optimum is zero
for every nonnegative weighting on the whole extended-cover class.

Run `python3 scripts/check_extended_double_cover.py`. The independent
literal controls cover all 1,100 labelled bases of orders zero through
five, 1,065,509 selected subsets, all 54,160 minimal forming sets and their
65,820 empty-rung budgets, 36,306 feasible representative pairs on bases
through order four, and 5,036 direct-terminal constructions. These certify
14,236 white selected subsets, rather than 14,236 separate construction
calls. Fifteen larger matching/dual and attaining-set certificates cover
base orders 8,17,64,257,1024. All-size conclusions use the written proofs.

The initial three-parameter theorem and zero-completion algorithm received
independent ACCEPT at snapshot 5044cd7; the reviewer ran its complete
embedded checker and reproduced the report. That reviewer also supplied
a malformed external certificate exploiting Python negative indices. The
checker now validates vertex domains before indexing and rejects that
exact regression. The new SF theorem, its equality remainders and the
expanded checker received a separate independent **ACCEPT** at snapshot
6000a72. The reviewer reconstructed the all-size proof, extracted the two
Python files verbatim, ran the full unchanged checker with assertions
enabled, and confirmed equality of the generated and attached JSON data.
The exact negative-index fake certificate was also separately rejected
before graph indexing. The final note adds the requested explicit standard
partial-colouring definition; no proof or algorithm change was needed.
`output/extended-double-cover-review.json` preserves both complete verdicts
and the exact attached-file manifests. No new Lean verification or full
priority comparison is claimed.

## Source-dependent TH completion

The [complete proof note](EXACT_TH_OPTIMIZATION_AND_LADDERS.md) gives five
results, with an exact integer implementation and independent controls:

1. Binary labels, fixed to one at selected white terminals and zero at
   other white terminals, and equal along actual and chosen auxiliary
   edges, minimize exactly the genuine TH expense. Label-one cycles can
   overcharge individual pairs but never improve the minimum. Every
   minimizing labelled pair gives a truly optimal full matching.
2. Deleting complete disjoint retained paths and adding their fixed
   expense gives the exact retaining problem, while allowing all remaining
   HH paths to reroute freely.
3. A standard frontier DP needs just the label and auxiliary matched bit
   per active vertex. At most h+1 vertices are active, for shorter bounding
   side h. It uses O(n 4^(h+1)) state transitions; tuple and integer-bit
   overheads are stated separately. It returns an optimum and full witness
   or reports infeasibility. This solves the unrestricted exact optimizer
   question left in the preceding residual-Hall notes at bounded width.
4. On every full 2-by-n ladder, any monochromatic selected Q set with at
   most one occupied neighbour per selected vertex has a zero-expense
   full completion. Disjoint adjacent-column swaps give a linear proof
   and construction for every n, arbitrary M and nonnegative weights.
5. On the full 3-by-6r grid, an explicitly feasible all-white-Q selection
   and four unit actual edges per block have exact optimum r. Each black
   centre needs its own paid component, and nine printed auxiliary edges
   per block attain the bound. Thus the height-two universal zero-expense
   conclusion cannot extend to height three.

## Reproduction

Run from the repository root:

```sh
python3 scripts/check_source_label_dp.py
```

The checker uses literal perfect-matching enumeration and overlay scoring,
not the DP recurrence, to determine small true optima. Its output records:

| Control | Exact scope |
| --- | --- |
| Rectangular models | 750 models, 37,659 full-N scores; 631 have feasible selected sets |
| Masked boards | 180 models, 279 full-N scores; 92 are infeasible |
| Alternative scans / value-only | 122 / 61 comparisons |
| Independent colour enumeration | 26 models |
| Full ladder actual-match enumeration | 10,992 matchings for n=1,...,8 |
| Selected subsets covered by maximal-T certificates | 79,016 combinations |
| Ladder DP / translation and transpose controls | 114 / 228 |
| Full versus retaining 2-by-4r | 36 controls, r through 128, 1,024 vertices |
| Positive 3-by-6r family | 18 controls, r through 128, 2,304 vertices |

The controls include zero and 401-bit actual weights, a positive-cost
ladder violating the neighbour condition, an infeasible retained-path
example and a balanced board with an isolated vertex. Finite tests check
implementation; all-size statements have the written proofs above.
No Lean execution or verification is claimed.

## Scope and review

The proof/source snapshot 4a3aa6e received independent **ACCEPT for the
mathematics and optimizer**. The reviewer inspected both Python files and
reported 17,788 calls to the unchanged optimizer using a new literal-reference
harness, including 13,148 full-matching scores. That harness also reproduced
the 10,992 ladder constructions and all 36 cascade work-counter records.
The original attached checker initially could not run because the attachment
omitted its helper-module dependency. This package issue is corrected: the
exact independent enumerator, overlay scorer and serializer are now included
in the checker, whose only project import is the optimizer under test; it
creates its output directory. An isolated local full rerun reproduced all
three committed reports byte-for-byte. No claim is made that the reviewer
executed this corrected original checker.

The later height-three theorem received its own independent **ACCEPT**, based
on its all-r proof and explicit coordinates; that reviewer did not claim code
execution. `output/source-label-dp-review.json` records both exact review
scopes, responses and the completed packaging correction. The empty-board,
preprocessing-memory and forced-scan conventions are explicit in the note.

The earlier forced-cascade review and its identical retry both ended with
terminal infrastructure failures and no mathematical response. The prior
positive-attainment equivalence and unit 18-by-18 optimizer-choice result
retain their existing ACCEPT, scoped to their original input.

## Remaining questions

| Question | Current status |
| --- | --- |
| All four parameters on E(H), and on every bipartite Cartesian prism | Proved by the matching and witness-capacity theorem above |
| SF_2 and Omega on arbitrary Cartesian prisms | Proved; sharp SF/beta and SF/psi gaps and all positive equality bases classified |
| Extending four-way prism equality to arbitrary bases | False; the exact near-complete families above separate the parameters |
| Exact genuine TH expense at fixed grid width, with retained paths | Solved by the source-label DP, exponential in width |
| Zero expense for all feasible ladder and E(H) instances | Proved, arbitrary M and nonnegative weights |
| Zero expense for every feasible full grid instance | False: the explicit 3-by-6r family has expense r with unit actual weights |
| Simultaneous endpoint counting for overlapping Hall-tight regions | Proved with one global HH budget; compatible physical routing and a universal coefficient gain remain open |
| SF_2=beta_2 for all finite median graphs | False; the bounded-degree connected family above has linear gap |
| SF_2=beta_2 for two-connected subcubic median graphs | Proved, using the cited ladder/cube classification and the prism theorem |
| Exact SF addition for arbitrary partial square or pendant-path attachments | False; explicit all-m families have additive error m-4 |
| Exact SF addition for partial square attachments to bipartite bases | False; unbounded error with exactly one ear, even with connected base, final graph and residual |
| Unbounded partial-ear error at fixed ear count and fixed maximum degree | Impossible; explicit radius-five footprint and degree bound above |
| General composition through a bounded deleted interface | Two-sided local-error theorem for every finite simple graph; optimal constants remain open |
| Full root coverage by square or pendant-path attachments | Complete minimal-set classification and exact beta_2=sf_2=SF_2 |
| SF_2=beta_2 for two-connected planar median graphs of maximum degree four | Open; cube chains and full-coverage ear classes proved |
| SF_2=beta_2=psi_sq for two-connected outerplanar median graphs of maximum degree four | False; H_r has beta_2=SF_2=8r and psi_sq=Omega=9r |
| Rectangular-grid SF_2=beta_2=psi_sq when one side is three | Proved for every positive other side; complete-vector computer-assisted proof, independently accepted with original executions |
| Rectangular-grid SF_2=beta_2=psi_sq when one side is four | Proved for every positive other side by the full-vector extension; separately accepted with original executions |
| Rectangular-grid SF_2=beta_2=psi_sq when one side is five | Proved for every positive other side; independent ACCEPT with both original executions and exact vector hashes |
| Exact exchange within S union W retaining all selected star leaves | Solved by bipartite matching for every fixed witness assignment |
| Selected-star minimal sets with at most one selected isolate | Proved cardinality at most beta_2, allowing witness conflicts and centres in both parts |
| Always retaining every selected star leaf in a size-preserving exchange | False; connected12r family has leaf optimum7r but true beta=8r equals the selected size |
| General selected-star minimal-set inequality without further hypotheses | False; both the18-vertex example and connected maximum-degree-four port families have genuine gaps |
| Exact dissociation composition through clean witness ports | Proved beta_2=7r+alpha(R) for every oriented finite interface graph; selected size8r and degree-four path/cycle counterexamples |
| Sharp gap for all selected-star minimal sets without the private clean-leaf hypothesis | Proved floor(n/12), sharp even connected maximum degree six; positive equality forces pendant vertices, so minimum degree two yields floor((n-1)/12) |
| Sharp gap for selected-star sets with a private outside witness at one leaf of every centre | Proved: floor(n/12), attained by connected maximum-degree-six graphs at all orders24r |
| Arbitrary-width rectangular-grid SF_2=beta_2=psi_sq | Open; arbitrary-width cap/exchange criteria and selected-star boundary-deficit bound proved, not an unconditional equality |
| Improvement of the universal mixed-direction 5/6 coefficient | Open |
| Sharp selected-star coefficient under fixed minimum-degree and connectivity lower bounds | Resolved asymptotically: the exact padding family tends to1/12 for every fixed pair of lower bounds; maximum degree grows |
| Stronger direct-centre witness exchange and cubic selected-star bound | Proved t-s-q>=2d; the new two-colour repair gives d<=floor(n/24), superseding the earlier n/22 certificate; graph sharpness open |
| Two-colour subcubic selected-star repair bounds | Proved 4n/57 at maximum degree3, 8n/121 also at minimum degree2, and n/24 in cubic graphs; no connectivity assumption. Compact two-connected lower family has n64k,d=k. Graph-sharp coefficients remain open |
| Sharp selected-star gap with bounded maximum degree or regularity | Minimum degree2 and every maximum-degree allowance Delta>=6 now have exact sharp coefficient(Delta-1)/(12(Delta-1)+2), attained two-connected. For every minimum degree delta>=3 the coefficient Delta/[12Delta+8delta-14] is now sharp along Delta=(4delta-7)r,r>=3, also two-connected. The four-selected-leaf-port and dense multiport constructions together reach Delta=4delta-7 and kappa=delta for every delta>=3. Balanced omissions give further parameter steps. Remaining intervening degree parameters, minimum-degree-two maximum-degree3..5 and regular selected-star sharpness remain open; quartic regular lower1/68/upper1/34, minimum-degree-two subcubic lower1/64/upper8/121 and cubic upper1/24 retain their separate scopes |
| Candidate strengthening4beta_2>=2|S|+n for general bipartite selected-star minimal sets | False: P_(r,r) has beta_2=n/2, selected size8r, order14r and connectivity r+1; no selected edge components |
| Intrinsic recognition of positive sharp n/10 equality in bipartite graphs | Proved by intrinsic layers and the exact all-subsets neighbourhood criterion; separate from E(H) |
| Unrestricted gap at maximum degree three | Uniform improvement proved: every minimal S satisfies |S|-beta_2<=floor(7n/71), including empty graphs, without connectivity, minimum-degree or selected-component restrictions. Balanced witness marginals, paired margins and exterior extension prove the exact14n-142d certificate; sharpness andattainment remain open |
| Replacing the incomplete-core all-subsets criterion by local conditions | Open simplification question; the exact recognition theorem is already proved |

The new structural theorem does not extend automatically to wider grids:
if both sides of a rectangle are at least three, a corner has degree two
but all its neighbours have degree three. No adjacency-preserving map can
send that corner to an adjacent vertex. Such a rectangle therefore cannot
admit the adjacent-pair involution used for the extended-cover argument.
This rules out applying this particular structural criterion, without
deciding the equality itself. No arbitrary-width polynomial claim is made.
The sharp bipartite n/10 gap theorem and previous composition manuscript
are preserved. No email, submission or submitted-version edit is implied.


## Shared odd-path neutral budgets and final-cover repair (13 November)

[Shared odd-path neutral budgets and final-cover repair](docs/ODD_PATH_NEUTRAL_BUDGET_AND_COVER_REPAIR.md)
charge the first removal once per touched initial odd path. Under an independent
tight initial cover, outside-cover removals and finally isolated additions,
final cover flips give exact cost nu0-|S|+O(S), with distinct initial matching
edges owning the savings. A conflict-cover algorithm optimizes the grouped
budget then minimizes operations in 2^k polynomial time. A two-connected20r
physical family has inherited best2r-2 but repaired fixed-list optimum r-1;
this improves a specified-start certificate, not a universal bound. Original
checker passes; independent ACCEPT reproduced the complete report byte-for-byte.

The exact budget allows many operations on the same initial component;
vertex-disjoint final repair regions own different initial matching edges.
All implications, blockers and pair conflicts express final isolation only.
The fixed-intersection optimizer has a unique smallest maximum-value batch;
there is no global uniqueness or arbitrary-exchange polynomial claim.
The physical all-square class was already settled by earlier unrestricted
results. This application repairs the inherited-certificate barrier from
one given U/list; universal8b/3, unit5/6, general physical multi-Hall routing,
sharp remaining degree parameters and arbitrary-width grid equality remain
OPEN in the full ACTIVE goal. October manuscript preserved.


## Mixed cover repair and minimum-operation complexity (13 November)

[Mixed isolated-addition repair and operation-count hardness](docs/MIXED_ISOLATED_REPAIR_AND_OPERATION_HARDNESS.md)
allow removals on both initial cover sides. Odd-component counts give exact
endpoint costs and explicit final covers/matchings. Maximum saving is exact
in 2^k polynomial time for conflict-cover size k; the fewest-operation
tie-break has an exact 2^s polynomial SCC enumeration. A self-contained
Vertex Cover reduction proves its minimum-operation decision problem NP-complete even for two-connected
bipartite min2/max3 physical graphs, all square owners, auxiliary P4/P2,
minimum omission and no addition conflicts. Primary maximum saving is easy
on these inputs; no unrestricted graph-parameter hardness is asserted.
Original checker passes; independent ACCEPT reproduced the full original report byte-for-byte; explanation-only audit errata are preserved in the receipt.

The exact saving is (|X|+o(G-X)-o(G))/2; new isolated additions are
excluded from o(G-X). The distinct destroyed-edge ledger is global, not
ownership by individual repair regions. The mixed class has no unique
smallest conditional maximizer even for one initial edge. The physical
reduction makes zero cost reachable by selecting all operations, while the
fewest such operations is D*tau(H); connected bridgeless normalization
provides the two-connectivity restriction without a cited restricted-hardness
assumption. This advances deletion/composition structure and computational
boundaries, not a new universal numerical bound or rectangular-grid result.
Mixed nonisolated additions, universal8b/3, compatible physical multi-Hall
routing, unit5/6, remaining sharp degree parameters and arbitrary-width grid
triple equality remain OPEN in the full ACTIVE goal. October manuscript intact.


## Arbitrary nonisolated exchange and all operation budgets (13 November)

[Nonisolated exchange budget frontiers](docs/NONISOLATED_EXCHANGE_BUDGET_FRONTIER.md)
compute the exact minimum matching cost at every operation count, allowing
mixed removals and arbitrary addition adjacencies. A two-state run-parity
automaton with closed traces on even cycles and retained candidate decisions
gives 2^w polynomial time for supplied traversal pair width w, with explicit
batch and final cover/matching witnesses. Two physical all-scale families
have sharp opposite slopes F(t)=t and F(t)=2r-t; the useful-addition family
improves the isolation domain, and earlier mixed inherited rules already
reach it. The method is exact for a fixed distinct-owner candidate list,
not unrestricted omission optimization or a universal small-width theorem.
Original corrected checker passes; independent ACCEPT reproduced all8,945 report bytes with empty stderr. Initial iterator/reporting findings and exact fixes are preserved in the audit receipt.

The full endpoint saving is half the change in ALL odd induced-component
counts, including new isolates, because replacement preserves cardinality.
The exact budget frontier is1-Lipschitz but need not be nonincreasing.
Candidate variables are charged once at first occurrence and retained until
their second, even across components. Cycle closure handles the fully
present case without guessing an absent vertex. The fixed-list problem is
now solved exactly with a pair-width parameter; a universally small width
or a universal structural fee guarantee remains unproved. Earlier zero-cost
operation-budget hardness survives without an explicit isolation condition,
since zero matching cost forces an edgeless final graph. This does not prove
unbudgeted primary hardness. Universal8b/3, unit5/6, compatible physical
multi-Hall routing, remaining sharp degree parameters and arbitrary-width
grid triple equality remain OPEN in the full ACTIVE goal. October manuscript
unchanged; no weighted TH or formal-kernel claim.


## Candidate component forests and cycle rank (13 November)

[The component-message theorem](COMPONENT_CYCLE_RANK_FRONTIER.md) solves the
whole fixed-list operation-budget frontier in O(2^k N(q+1)^2) arithmetic
transitions, with polynomial bit and witness overhead. The multigraph has
one vertex per complete ambient auxiliary component and one candidate edge;
k=q-c+d counts loops and parallel cycles. Every residual candidate is
charged once in its child message; fixed nonforest bits are counted once
globally. Closed path/even-cycle traces evaluate high-arity component factors
without enumerating their incident bit assignments. Forestk0 is polynomial.

For every evenq>=2, a two-connected bipartite physical graph of order10q,
min2/max3, minimum square omissions and q permitted distinct-owner swaps has
candidate graph a star, yet its minimum complete-component pair width is
exactlyq/2. No bound for arbitrary interleaved vertex traversals is claimed.
For q4r/type0011 the exact frontier is max(2r-floor(t/2),r,t-2r), first
minimumr at2r operations; the actual dissociation certificate has size23r
on40r vertices. This is fixed-list optimality, not unrestricted betaexactness.

The direct implementation supports general loops, parallel edges, candidate
permutations and nested iterator inputs. Independent literal matching and
candidate subset checks, actual physical certificates and width controls
pass. General and all-size conclusions rely on complete proofs. Standard
tree-factor/conditioning methods are acknowledged without priority claims.
Original checker passes; independent ACCEPT reproduced the complete report byte-for-byte. Preliminary audit tool timeouts and the successful unchanged execution are distinguished in the receipt.

Universal8b/3, remaining sharp degree/regularity coefficients, compatible
physical multi-Hall routing, unit5/6 and arbitrary-width grid triple equality
remain OPEN in the full ACTIVE goal. October submitted manuscript preserved.
