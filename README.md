# Sub-quorum colorings: hypercubes, boundary matchings, and grids

New [exact physical strip compensation and fee/depth tradeoff](docs/STRIP_TREE_PHYSICAL_COMPENSATION.md):
same-colour matching in an arbitrarily tall two-column cell is equivalent
to even runs of identical mixed rows. A red/blue/unused model prices actual
TH M edges exactly, with coloured-cycle normalization at the global optimum.
An 18-state physical transfer gives linear arithmetic complexity when the
actual cross-cell M multigraph is a forest; conditioning its k feedback
edges gives an exact O(3^k |V|) extension, retaining parallel-edge identities.
The solver reconstructs a full N rather than reporting scalar compensation.
For the old 4-by-w family after one T relocation, the new sharp deduction
is one-batch minimum fee w/2 versus two-batch fee zero, for every even w>=6.
Another inherited isolated-hole family has a new strip-confined horizontal
full completion of exact fee k. All-size proofs accompany 2,192 exhaustive
weighted actual models / 9,864 auxiliary comparisons, 100 further models,
12,842 colour profiles, 50 relocated widths and 16 long-relay parameters.
Five local Lean declarations prove the arbitrary-alphabet word normalization;
the physical extraction and global algorithm are written proofs.

New [physical obstruction to capacity-preserving cell coarsening](docs/CAPACITY_PRESERVING_MACROCELL_OBSTRUCTION.md):
the regional/debt formula on arbitrary balanced cells is exact for the
complete-port relaxation. Its use for physical domino matchings requires
a local routing lift. For uniform 4-by-2 cells on a connected 8q-by-w board,
all coarse debts can be paid using distinct actual M edges within receiving
budgets, yet every cell-confined auxiliary matching leaves exactly q TT.
Thus the gap is unbounded even without any duplicated compensation resource.
The missing constraint is the forced connection of the two top ports.
For the same stacked family, the optimum over a single independent batch
from horizontal N is exactly one TT; exactly two batches achieve zero at
zero final M cost. This separates static coarsening from successive routing.
The physical base family/forced-port argument are inherited and credited;
the relaxation interpretation and capacity-preserving amplification are new
deductions. Controls: 86 models, 5,440 regional cuts, 19,500 active-cell
auxiliaries and five local Lean declarations. Global arguments are written;
the numerical 5/6 bound and universal batch coverage remain open.
An exact physical lifting criterion supplements the flow: both red and
unmarked cell port subgraphs must satisfy Hall. All 70 balanced local bit
profiles are checked against the five physical phases; exactly 44 lift.
The criterion is existential over integral flows and retains intra-cell
M loops; a failed test for one flow alone is not a global impossibility proof.
Independent review [ACCEPT](output/macrocell-review.json) covers the general
relaxation, capacity-respecting physical obstruction, amplification and sharp
one/two-batch separation. The reviewer reproduced the submitted checker JSON
in full and did not run Lean. The later local Hall follow-up terminated
with an infrastructure failure and no mathematical verdict; it is not
included in the initial acceptance.

New [general physical ports and exact tile compensation](docs/GENERAL_SQUARE_PORTS_AND_TILE_CUTS.md):
same-path cuts, cut original P-only cycles and retained M/N doubled edges
now fit the coverage flow and joint-cost model. Physical cut ports preserve
self-loops, parallel fragments and single ownership. With a fixed 2-by-2
tiling the exact residual TT count is

    delta_tile = max_U (T(U)+M_internal(U)-2|U|)
               = (total debt - maximum debt-to-reserve flow)/2.

Each debt tile has two diagonal T and one P; each other tile contributes
reserve max(4-2T-P,0). Every actual cross-tile M edge has one undirected
compensation capacity. This is an exact joint criterion; it does not assert
that all feasible grid cuts pass. Every intra-tile actual M edge may be
retained without changing terminal pairings or increasing payment cost.

A NEW consequence for the existing unique-matching 4-by-w family gives an
actual positive regional cut at EVERY even w>=6: two debt ends lie on a closed
zero-reserve M chain, so the best of ALL product-tile phases leaves exactly
one TT. The construction still admits unrestricted zero-M adjacent-hole
payments. Fixed-tiling universal coverage is therefore disproved; flexible
pool selection and the numerical target remain open. Fifty widths and all
product phases at widths 6,8,10 validate this written deduction.

A stronger forced-port argument proves EVERY independent square pool fails
at the all-horizontal auxiliary baseline in that family, for all even w>=6.
In fact all 5^(w/2) auxiliaries confined to the 4-by-2 column strips retain
a TT: interior strips always connect their top M ports, and both end ports
terminate at T. The optimal residual is exactly one. Controls check 3,875
strip-confined full auxiliaries and all 504 maximal pools at widths 6,...,16.
The zero-M unrestricted N is explicit; changing the baseline or permitting
controlled successive overlapping batches is necessary for this example.
An explicit optimal repair now uses exactly TWO batches: flip all even-column
squares in both two-row bands, then all odd-column squares. Every T ends
on a direct hole edge with zero M cost. A full set ledger traces payment
2 -> 0 -> 0 and distinguishes absorbed old free edges from new free edges;
the two batches overlap each other and are individually independent.

The same note proves an all-even-H old-cycle relay barrier: the original
bad-path M count is TWO, yet the unique covering subset of two prescribed
squares costs H+2 by absorbing H previously free cycle edges. A 2-by-2 example
already refutes a bad-only cost ledger (payment 0 to 1). The corrected signed
ledger includes old and new free cycles and any remaining HH-path M.
These are pool/rule obstructions; the all-H family has unrestricted zero-M
payments and is not a numerical counterexample.

[General physical controls](output/general-square-ports.json) exhaust 10,512
small actual models / 22,618 subset surgeries, plus 140 larger actual models,
573 exhaustive product-tile models and 140 larger tile models. They check
6,402 tile-phase normalizations, both directed and debt flows, forty even-H
relay families and the complete 567 local label/matching cases.
[Fifteen scoped Lean declarations](formal/SubQuorum/GeneralSquarePorts.lean)
and [local execution/axiom audits](output/general-square-formal.json) pass.
Physical extraction, global flow/min-cut, normalization and all-H embeddings
are written proofs; the universal 5/6 improvement remains open.
[Independent core audit ACCEPT](output/general-square-review.json) reproduces
both original submitted Python outputs exactly, without running Lean. The
[separate stronger audit ACCEPT](docs/reviews/2026-10-27-all-independent-pool-obstruction-review.txt)
checks the all-width closed cut, every independent pool and explicit full N,
reproducing its complete submitted checker JSON exactly, without Lean. The
subsequent optimal two-batch repair has a separate live review. The original
closed-cut-only follow-up remains an independently tracked pending task.


New [exact arbitrary-contact coverage and cut](docs/CONTACT_FLOW_CUT_AND_EXACT_COST.md):
for any prescribed pool of vertex-disjoint squares satisfying the original
terminal-path contact hypotheses, an integral unit flow gives the EXACT
minimum remaining TT count B_T-F over every subset. The complete directed
fragment cut counts each shared capacity once, including zero-M fragments.
It detects the shared-star bottleneck and distinguishes mandatory wrong-order
batches from pools that admit successful smaller subsets. A separate two-colour
binary-flow model gives exact total M cost with one shared fragment capacity.

New [three internal contacts defeat red-first cost optimization](docs/ONE_COLOUR_GREEDY_BARRIER.md):
for every even L>=4, first minimizing red and THEN optimally completing blue
costs L^2+12L+80, while joint optimization costs only 10L+78. The ratio is
unbounded; the unique red minimum forces the bad operation. An actual
30-by-130 board gives 720 versus 278. This is a failure of sequential cost
optimization, not of the coverage flow or the numerical sub-quorum target.

Local checks pass 360 abstract networks / 224 weighted models, 3,508 actual
subset surgeries on 158 row/star pools, 48 long star controls, three weighted
five-contact models and six diagonal greedy-family boards. Eleven scoped Lean
declarations prove general local switch completion and conditional cut/ratio
arithmetic; the global flow and physical adapters remain written. Separate
post-submission controls check zero-M terminals and eight off-diagonal boards.
[Independent audit ACCEPT after one summary-quantifier correction](output/contact-flow-review.json):
submitted main reproduced with full parsed-JSON equality; no Lean or later
edge-case execution. The follow-up accepts the corrected package and conditional
numerical ledger, emphasizing that delta-b_opt=a-b is switch-invariant.
General geometric pool selection and universal 5/6 remain open.

New [five indispensable contacts](docs/FIVE_CONTACT_SPARSIFICATION_BARRIER.md):
one actual TT/HH pair and five vertex-disjoint prescribed squares give an
unbounded cost gap between all five and EVERY successful proper subset.
For every even L>=12, the best proper subset costs L^2+L+14, whereas all
five cost 5L+78. A general coordinate and two-block routing proof establishes
the result; 27 actual boards / 837 subsets validate it and six scoped Lean
arithmetic declarations pass. The theorem concerns this prescribed contact
pool; alternative squares/N and the numerical 5/6 target remain open.
[Independent audit ACCEPT](output/five-contact-barrier-review.json) confirms the
written theorem, reproduces all 837 subsets with parsed-JSON equality, and
adds 62 boundary subset controls; it did not run Lean.

The [exact disjoint-pair optimizer](docs/DOUBLE_CONTACT_OPTIMAL_COVER.md)
remains valid in its stated one/two-contact class: strict reverse-order prefix
coordinates give maximum single-cycle credit in O(d log d), and minimum-cost
TT/HH matching gives the exact full-cover cost without reusing original paths.
Controls pass 1,000 local comparisons, 144 actual matching assignments,
132 zero-cost packings and 20 direct-Hall failures repaired by TH relays;
seven scoped Lean declarations pass. The first independent review requested
two quantifier corrections, both applied; its follow-up ended with an
infrastructure failure and no verdict. [Precise review scope](output/double-contact-cover-review.json).

New [contact-network routing and cycle credit](docs/CONTACT_NETWORK_CYCLE_CREDIT.md)
reduces all chosen square contacts to a canonical bipartite continuation
permutation, with exact terminal pairing and unique physical-M ownership.
New P-only cycles are bounded by the contact multigraph cycle rank; a parity
constraint and a complete two-contact order dichotomy follow. A feasible 8-by-6
fixture has two individually successful contacts whose combination restores
TT/HH. Conversely, an all-length ladder repairs the pair at zero M payment
cost: one cycle can remove arbitrarily many original bad-path M resources.
The exact cost change is original bad resources minus final bad and cycle
resources. Direct physical checks pass 1,012 ladder subsets, 240 length controls,
1,248 multi-path networks and the 8-by-6 fixture; seven local Lean ledger
kernels pass. Another 80 TH-ladder controls verify negative cost increments,
and an M-free bad-path fixture separates resource cost from terminal coverage.
[Independent network review ACCEPT](output/contact-cycle-review.json) reports
reproducing the submitted 2,500 analysis calls, with no Lean; later fixture and
negative-increment additions were checked locally. General geometric coverage
and universal 5/6 remain open.

New [exact shared-TH star capacity](docs/SHARED_TH_STAR_CAPACITY.md): a single
original TH path supports arbitrarily many TT/HH repairs when its contact
labels alternate HH,TT,HH,TT. Cutting all contacts gives a complete physical
fragment partition and exact residual counts for every word. Coarse Hall
matching over individually valid ordered relays fails without bound: all
s-by-s pairs are valid and all chosen squares are vertex-disjoint, yet the
contact word H^sT^s repairs only one pair and leaves s-1 TT/HH pairs.
Explicit feasible 6-by-(12s+2) families realize both words for every s, with
the same actual M, auxiliary N, contacts and selection count. For s>=2 selection
placement differs; at s=1 both words coincide. Both have zero-M unrestricted payments; the obstruction is
to the specified simultaneous certificate, not the numerical target.
All 510 short actual words, 40 positive/40 obstruction lengths, 204 individual
pair controls and seven local Lean word-classification declarations pass.
General coverage across multiple shared TH components and the universal 5/6
improvement remain open.
[Separate independent star review ACCEPT](output/shared-th-star-review.json)
reports reproducing the submitted 510/40/40/204 Python output, with no Lean
execution. Its three wording clarifications are incorporated; it does not
certify the later contact-network/cycle-credit theorem.

New [ordered TH relay theorem](docs/ORDERED_TH_RELAY_COMPENSATION.md) extends
fixed-M square compensation through arbitrarily many intermediate TH paths.
With disjoint square supports, all paths become TH if and only if every
intermediate path meets its outgoing contact before its incoming contact in
T-to-H order. Incremental payment uses exactly the two original bad paths'
M-resource sets; intermediate TH edges are rearranged once. Component-disjoint
chains batch without sharing resources. A feasible 6-by-12 wrong-order witness
leaves a TT after both disjoint switches, refuting the order-free rule rather
than payment existence or the numerical target. An arbitrary-length actual
family has no initial direct TT/HH square yet admits these relays, and separated
copies give arbitrary chain packings. Eighty lengths, 40 packings, 32 tiny
matching controls and seven scoped Lean resource/uniqueness kernels pass.
General chain coverage and a universal 5/6 improvement remain open.
[Separate independent review ACCEPT](output/ordered-th-relay-review.json) covers
the written theorem and constructions; the reviewer reproduced the submitted
80/40/32+counterexample output, not Lean or later local checker additions.

New [mixed-terminal square compensation](docs/MIXED_TERMINAL_SQUARE_COMPENSATION.md)
keeps the actual matching M fixed and switches only a full auxiliary certificate N.
A matching of s original TT/HH component pairs with alternating-square witnesses
repairs exactly 2s selected endpoints, without sharing physical M edges;
Hall coverage of TT gives J=area/2-(b-a) and the exact weighted margin
(b-a)+|M|/6. The geometric Hall hypothesis remains explicit. At balanced equality,
legal payment cost is |M| minus maximum retention over TH-admissible certificates;
unrestricted retention can underestimate it. An arbitrary-height feasible
4-column family has terminal penalty exactly one and an explicit square repair.
Checks cover 7,345 small-strip controls, 360,432 matching-pair controls,
6,117 feasible balanced core selections and 41 family parameters. Seven scoped
local Lean arithmetic declarations pass; decomposition, gluing, Hall and grid
assembly remain written proofs. No universal 5/6 improvement is claimed.
[Independent written review ACCEPT](output/mixed-terminal-compensation-review.json)
covers this mixed-terminal result and the all-k relay-cost theorem below;
it reports no Python or Lean execution.

New [isolated-hole obstruction and actual-edge detours](docs/ISOLATED_HOLE_OBSTRUCTION_AND_MATCHING_DETOURS.md):
on a 6-by-8q footprint, every feasible selection satisfies J<=area/2, sharply,
by an explicit disjoint cover with seven guarded pairs, six endpoint-free squares
and one forced-hole detour pair per cell. The sharp selection has exact adjacent
T-to-H matching deficiency q. Colour conservation rules out even fractional
exact covers made only of forced-hole singletons, guarded adjacent pairs and
endpoint-free unit squares, in all alignments. Exactly q distinct actual matching
edges are necessary and sufficient for disjoint alternating-path payments;
even padding moves the isolated holes arbitrarily far from the boundary.
The endpoint matching is unique. Fifty q controls, 200 arbitrary selections,
four padded boards, independent arbitrary-T column DP and seven scoped local
Lean declarations pass. The numerical six-row half-area bound was already known;
the new contribution is the structural cover, obstruction and exact relay cost.
General cover existence and the universal 5/6 improvement remain open.
[Independent review ACCEPT](output/isolated-hole-detours-review.json) covers
this all-q theorem and reports reproducing the supplied Python output, not Lean.

The [unbounded isolated-hole relay-cost theorem](docs/UNBOUNDED_ISOLATED_HOLE_RELAY_COST.md)
separates defect count from path cost: for every k>=1 an explicit (4k+2)-square
board attains J=area/2 and has adjacent deficit ONE, yet every complete
disjoint alternating-path payment needs at least k actual matching edges,
under every rematching on its P. One specified M attains k with a single
length-(2k+1) path and otherwise adjacent payments. Thus adding any FIXED
maximum length of forced-hole detours cannot yield a universal cover, even
with nonnegative fractional exact coverage. Forty actual boards and another
actual rematching per board pass; two further scoped Lean kernels verify the
distance/cost deduction. The lower bound is geometric and holds at every k.
Its [first separate review terminated with an infrastructure failure](output/unbounded-hole-relay-review.json):
the broker exhausted three browser-input retries. No mathematical verdict
was returned for that first task. A fresh [written review ACCEPT](output/mixed-terminal-compensation-review.json)
now covers this addendum; its execution scope and the earlier q-cell review
remain separate.

New [unique-matching hole-compensation barrier](docs/UNIQUE_MATCHING_HOLE_COMPENSATION_BARRIER.md):
for every even w>=6, one explicit endpoint footprint on 4-by-w has a unique
perfect matching and exact FREE-selection maximum J=2w-1=area/2-1.
Two forced holes and w disjoint guarded adjacent pairs give a hole injection
for every feasible T and prove the bound at arbitrary width. A sharp T has
ownership demand w but only w-1 actual resources; its all-P tile set has q=+2.
Thus no rematching, or even arbitrary regrouping of endpoint charges with the
unchanged tile inequalities, can repair this family. Actual hole credit does
pay it, with exactly two unused holes. One adjacent relocation of a selection
preserves P/M/cardinality and restores ownership. Fifty widths, 7,290 selector
profiles (3,697 feasible) and seven scoped Lean declarations/axiom audits pass;
the coordinate cover and uniqueness induction remain written. General hole
transport, selection normalization and the universal 5/6 improvement remain open.
[Independent review ACCEPT](output/unique-matching-hole-barrier-review.json)
covers the written all-width results; the reviewer reports reproducing the
Python output, and did not compile Lean.

New [fixed-matching component-cut obstruction and square exchange](docs/ACTUAL_MATCHING_COMPONENT_CUT_AND_SQUARE_EXCHANGE.md):
for every even h>=6 an explicit feasible h-by-4 board attains J=area/2,
yet a closed tile set needs h distinct actual resources and has only h-1.
Thus universal compensation along fixed actual matching edges fails, even
with unrestricted intratile routing. Its complementary component has precisely
one physical spare. A capacity-two alternating square exchange gives a complete
ownership certificate at every height, keeping T/P and matching size while
changing two actual edges. On the original matching the same repair pairs a +2 edge with one -2 edge;
a general alternating-cycle ledger transports any consistent rematched charge
certificate without counting overlapping flips as separate payments. Negative
tile credit and negative edge payment are the same reserve and cannot be added. Fifty coordinate/ledger/exchange controls
pass; the written argument covers every even height. Universal rematching is refuted by the new unique-matching barrier above;
the numerical 5/6 improvement remains open.

The [actual-edge ownership lemma and bent relay family](docs/TURNING_ACTUAL_EDGE_COMPENSATION.md)
give an exact Hall/endpoint-charge criterion and resource margin
J=area/2-unused_edges-sparse_tile_units. Each physical matching edge has one
owner at most, including internal edges. In a sharp 4-by-(2q+2) family, restoring
one selected vertex from an explicit reversed baseline forces 2q+1 old owners
to change and one reserve to activate,
although source and reserve tiles are adjacent. The actual matching and all old
used resources remain fixed in this relay result. Fifty actual boards and seven
scoped local Lean declarations/axiom audits pass; Hall/grid/exchange adapters
remain written. A per-tile choice of old H/V charges already fails on a sharp
4-by-4 board. The broader fixed-M Hall criterion is itself obstructed above. Independent
written reviews accept the original notes and the later original-M/cycle
lemmas; [precise review and execution scope](output/turning-compensation-independent-review.json) distinguishes the two accepted bundles, local Lean, later local controls
and one terminal infrastructure failure without a mathematical verdict.

New [two-row signed compensation lemma](docs/TWO_ROW_SIGNED_BOUNDARY_COMPENSATION.md):
an explicit block classification proves the exact actual-edge ledger
T-H = cross-boundary charge + internal-edge charge - block slack.
Internal edges have nonpositive charge. Cross-strip terms can be positive:
an explicit sharp 6-by-w family for every even w>=4 has cross charge +2,
two distinct internal payments -1 each, zero block slack and J=area/2.
Thus automatic boundary cancellation fails even at equality; the target bound
is not refuted. Local checks cover all 50 feasible block states and 422
interfaces. The general cross-strip compensation inequality remains open.

The proposed [four-to-two-column compression rule is false](docs/TWO_COLUMN_COMPRESSION_OBSTRUCTION.md):
a realizable boundary has exact best short reward -1, but four columns yield +1.
A structural two-case proof gives the short upper bound; both attaining boards
use actual matching edges. This rules out that candidate induction, not the
half-area target or the independent boundary invariant below.

New [anchor-free six-row boundary invariant](docs/SIX_ROW_BOUNDARY_INVARIANT.md):
an explicit two-phase integer certificate and arbitrary-length induction give
the exact maximum J=3w+(w mod 2) for any 6-by-w rectangle, with arbitrary
actual matching and selected vertices. No retained endpoints are required.
The independent solver-free checker covers 2,404 states, 145,524 transitions
in both phases, and all seed/terminal cases. Four Lean declarations verify the
general induction and arithmetic with these local inequalities as hypotheses;
the table and coordinate adapter remain outside Lean. This is a
computer-checked invariant proof; a purely structural six-row proof and the
universal 5/6 problem remain open. Separate independent reviews accept the full
invariant proof and the structural signed-strip lemma/sharp obstruction.

New [arbitrary-selection colour-switch theorem](docs/ARBITRARY_SELECTION_COLOUR_SWITCH.md):
for every m>=2, retaining P0 alone permits arbitrary selections of either colour,
arbitrary whole-board new endpoints and any actual matching, with exact maximum
J=18m+30=area/2. No freezing is needed; the known completely frozen family attains.
A black prefix can genuinely borrow the single boundary hole (5,4); four actual-mate
capacities and thirteen explicit nonnegative affine identities show that this
state admits a complementary white budget. Switching colours rules out a global
excess without spending the same hole twice. All coefficients are published and
exact-checked without an optimizer; 461 boards, 2,247 five-white Hall controls and
19 scoped local Lean declarations pass. Independent review accepts the full
counting proof and coefficients; frozen attainment cites the established rank
construction. The full coordinate adapter is written,
not an end-to-end Lean grid theorem. The universal 5/6 problem remains open.


New [neutral occupied envelopes](docs/NEUTRAL_OCCUPIED_ENVELOPE_EXPANSION.md):
allowing the selected/endpoint footprint to change defeats a direct-entry-only
cost. An explicit six-cell expansion adds three matching edges, withdraws
three selections and rematches one old edge. Every subset of m possible
expansions stays completely frozen at exact half-area, without exterior input.
Complete actual-mate rank tables prove this for arbitrary m, including
consecutive expansions. Two local rematchings can be chosen independently
at each expanded site, giving at least 2^|S| matchings on each enlarged
footprint and 3^m configurations overall. Each expansion deletes one already paired
physical surplus/demand; no reserve is released or counted twice. In the
restricted direct-entry footprint the exact loss is one per active index,
and no nonempty conversion can completely freeze. Solver-free checks cover
1,645 expanded boards and 19,183 restricted conversion pools. The complete
six-cell permission domain has an exact pooled upper bound: each partial
black mask pays its forced-guard deficit, and half-area equality forces every
cell empty or full. All 49,544 small pooled conversion profiles satisfy it;
576 explicit matchings attain every prescribed black-mask bound. Nine scoped local
Lean kernels check shield identities/counts, conditional traps and the
arbitrary-length budget and equality criterion.
The complete coordinate adapter is written; the universal 5/6 question is open.

New [complete two-port matching classification](docs/TWO_PORT_MATCHING_CLASSIFICATION.md):
on the SAME fixed selected/endpoint footprint, exactly 5m+4 actual perfect
matchings completely freeze with both right inputs. A geometric interval trap
forces all odd vertical matching edges into one column or two adjacent odd
columns; lower-path parity reconstructs the entire matching. Explicit ordered
waves prove sufficiency for every length. If EITHER input is absent, only the
canonical matching freezes. Exact four-state deficits are proved for every
listed matching. The same zero-charge cap and exhausted physical ledger give
at least (5m+4)^t independent stack matchings at half-area. Solver-free checks
cover 1,454 candidates and all 53,900 reduced matchings at m=2,3,4. Lean covers
the separated-front barrier and abstract root normal form; the coordinate
adapter remains a written proof. The universal grid 5/6 question stays open.

New [two-port activation of an unbounded rematching chain](docs/TWO_PORT_UNBOUNDED_REMATCHING.md):
the same six-column zero-charge cap activates a matching change through every
core of the band. It removes exactly 8m+7 prescribed edges, including the
leftmost core arbitrarily far from the two right-boundary ports, while keeping
T/P and half-area unchanged. An all-length actual-mate rank table proves
complete freezing. Exact interface states leave 9m+9, 9m+7, 2 or 0 endpoints
unfrozen; both inputs are necessary for this matching. Every physical token
is already spent. Fixed input count therefore bounds neither rematching
extent nor distance. This is an explicit family, not an all-matching
classification. Solver-free controls and 17 local Lean audits pass.

New [zero-charge ambient activation of occupied bands](docs/AMBIENT_BAND_PORT_ACTIVATION.md):
a six-column cap preserves the old band's selected and endpoint footprint and
keeps its actual matching region-closed, yet activates a two-edge matching
switch at exact half-area. The switched band alone has four unfrozen endpoints;
the cap alone has eight. Their union is completely frozen for every m>=2.
Exact interface response maps and a three-stage certificate explain the
activation. Arbitrary stacks allow at least 2^q actual matchings on identical
occupation, with every physical token already spent. Thus isolated-band
rigidity and binary reserve cannot be applied to a region using global
freezing and matching closure alone. Solver-free controls and 17 local Lean
audits cover the stated kernels; the general grid 5/6 question remains open.

New [complete frozen equality-matching rigidity](docs/FROZEN_EQUALITY_MATCHING_RIGIDITY.md):
half-area equality forces the ENTIRE actual matching M*, not only four terminal
edges. A stronger pocket-port certificate starts a backwards actual-mate time
argument through every occupied block; a final two-endpoint trap excludes extra
pocket edges. Any missing prescribed edge restores one unit of reserve. The
fully frozen all-g family misses 3m+4 prescribed edges but loses only one unit,
so separate edge deficits cannot each claim that same reserve. Different
selected sets can attain equality with the same unique matching. The all-length
proof has solver-free controls and 16 scoped Lean audits; general grid 5/6
improvement remains open.

New [completely frozen half-area frontier and terminal-port compensation](docs/FROZEN_HALF_AREA_ATTAINERS.md):
for every m>=2 the exact frozen bound is J<=18m+29+epsilon, where epsilon
records the actual terminal vertical matching edge. Both values are attained
while retaining M0. An explicit all-length rank certificate proves complete
freezing of half-area attainers, and a local trap proof forces four terminal
edges at equality. The physical budget Cplus>=Cminus+m+2(1-epsilon) never
reuses a token; the half-area family has an explicit bijection spending all
positive tokens. The earlier one-unit reserve therefore requires a boundary
condition even under complete freezing.

New [terminal-guard half-area frontier](docs/TERMINAL_GUARD_HALF_AREA_FRONTIER.md):
after also allowing the terminal row-three guard to be withdrawn, the exact
unrestricted actual-matching maximum becomes 18m+30=area/2 for every m>=2.
A ten-site terminal inequality proves the upper bound; a three-chunk periodic
family attains it. Physical surplus pays exterior debts and the strip deficit
once, with no additional reserve. That initial sharp family has a provably nonfrozen
endpoint; the subsequent frozen-frontier theorem above resolves the frozen
optimum and its sharp terminal-port condition.
The preceding stronger theorem remains valid with its retained terminal guard.

New [boundary withdrawals and propagation of compensation](docs/BOUNDARY_WITHDRAWAL_AND_PROPAGATED_COMPENSATION.md):
the exact maximum 18m+29 survives after EVERY old row-four selection becomes
optional, including the three former boundary guards. A left-pocket gain of
one forces a state that crosses each saturated block and is paid by the first
unsaturated block or the reduced right-end capacity. The local inequalities
L<=9+p0, b_i+p_i<=7+p_(i+1), e+p_m<=4 telescope without reused credit.
The written proof holds for every m>=2, with arbitrary actual rematching;
frozen attainers persist. Thirteen scoped Lean audits include the arbitrary
length induction and potential sum. Other endpoint footprints remain open.

New [exact integer compensation for the connected occupied band](docs/CONNECTED_BAND_INTEGER_COMPENSATION.md):
for simultaneous G/H/F permissions, retained old endpoints and arbitrary
actual rematching, the true whole-board maximum is J=18m+29=area/2-1
for every m>=2, attained by completely frozen configurations. A disjoint
chessboard-weight cover and a new pocket certificate 4W<=39 close the
integer frontier left open by the preceding fractional matching obstruction.
Original physical tile credits pay exterior debts and the strip deficit
once, leaving two half-unit tokens. Checks include 147,297 pocket models,
20 sharp frozen lengths, 144 actual rematchings and ten scoped Lean theorems.
Other residual geometries and the universal 5/6 improvement remain open.

New [sharp completion and distinct reserves for negative frozen strips](docs/FROZEN_STRIP_SHARP_COMPLETION_AND_RESERVES.md):
for the original k-module endpoint footprint, EVERY feasible reselection has
T<=13k+11, by disjoint local face/pair covers. A periodic completion retains
all old selections and freezing, attains this true fixed-P maximum, and keeps
regional2S=1-k. For every retained completion, distinct original tiles give
one half-unit rebate per D4; the internal half unit pays the exterior boundary
demand, and k different full-unit endpoint-free reserves remain unused.
The sharp whole-board surplus is k. Checks include 80 retained extensions,
independent all-selection/retained DP optima, 24 isometries and 15 Lean audits,
including universal local cover proofs and the concrete 18-endpoint optimum.
Arbitrary-footprint geometric coverage and universal 5/6 improvement remain open.

New [no uniform exterior-donor radius for degree-four exports](docs/DEGREE_FOUR_EXTERIOR_LOCALITY_OBSTRUCTION.md):
an all-h completely frozen connected construction has two actual unported
degree-four TP exports in disjoint original-tile-aligned strips, each at
exact nearest exterior-donor distance h+1. It contains arbitrarily many
original capacity-two tiles. Its internal half-unit budget10 already covers
D4=2, with regional surplus4 and whole surplus14: this refutes unconditional
pointwise local access, not residual compensation or the grid target.
Checks replay 6,596 written freezing events plus 24 isometries; Lean verifies
the concrete 52-endpoint h=2 board and its exact exterior tile inventory.
The next target is residual demand AFTER internal payment, jointly with
outside positive charge and unique physical capacity ownership.

New [sharp occupied-strip degree-four budget](docs/OCCUPIED_STRIP_DEGREE_FOUR_BUDGET.md):
every transverse TP export either occupies a different BB--TT forest end or
is an unported degree-four exception. For disjoint mixed-direction strips,
the exact joint ledger becomes 2S=B+r+u+V-D4, with V>=0 and distinct refund
targets. Fully frozen, uniquely matched all-k families attain 2S=b-k for
one-corner and sealed even bands; every complete receiver is neutral, each
module contains an original capacity-two tile, and all endpoint-free regional
tiles are saturated. The outside half-unit charges are identified exactly.
Checks cover 990 geometric budgets and 6,594 freezing events; Lean verifies
the concrete 18-endpoint negative strip from feasibility through inductive
freezing, plus general arithmetic. Universal 5/6 improvement remains open.

New [cross-band matching refunds for occupied strips](docs/OCCUPIED_STRIP_EXPORT_CANCELLATION.md):
actual TP-column-to-BP-column matching exports cancel across disjoint strips,
including different directions, through distinct BP targets. The exact regional
ledger retains only one debit per TP-TP edge and half per TP-PP or exterior
TP export. All coefficients have frozen sharp controls. A fully frozen split
receiver crosses two bands and violates the former per-strip receiver-closure
hypothesis, while joint compensation applies; all-q copies supply 5q physical
surplus without reused tiles. Single-terminal safe parallel exports force a
boundary P-square. Checks cover 922 joint models/806 exhaustive matchings/1798
freezing events and 6 scoped Lean kernels, two axiom-free. The remaining target
is unpaid demand versus unused physical slack; freezing alone does not force
full routing, and a universal improvement over the 5/6 bound remains open.

New [identity-safe admission of previously unused betas](docs/NEW_BETA_IDENTITY_SAFE_AUGMENTATION.md):
the reachable-beta saturation guard is removed. Among minimum-cost residual
augmentations, choosing the fewest residual arcs keeps every beta normalized
from first activation. Exact maximum payment, minimum actual new-link fee and
then minimum new-link count retain all old paid alphas, original interval IDs
and whole-beta credits. Net gain is fresh intervals plus new beta credits,
counted separately. The proof covers any normalized zero-cost baseline, with
no initial maximality or two-owner-support requirement in the core network.
An explicit equal-cost tie shows why post-hoc normalization alone can lose an
old unit. Checks include 1,210 independent lex optima, 437 new-beta models,
63 augmentations with reverse links, an r=64 beta-transport production run,
frozen q=1,2,4,16 new-beta admission and four scoped Lean kernels. Geometric
cut lower bounds and universal 5/6 improvement remain open.

New [general mixed-head retention and deficient-tree relays](docs/GENERAL_BRIDGE_RETENTION_AND_DEFICIENT_RELAYS.md):
one resource-first flow handles arbitrary shared stems and deficient receivers
when every reachable beta already has its old whole-beta credit saturated.
All mixed-head additions satisfy this guard. Maximum payment, minimum actual
new-link fee and then minimum new-link count retain every old paid source and
original used interval ID. A deficient junction needs two outgoing bridges and
one incoming; one-outlet contraction cannot be extended unchanged. An all-length
abstract chain needs r+1 new links for one gain. A fully frozen shared-stem
example has separate bridge values 3/3 and joint value 4, retaining three old
units; all-q copies need 2q new bridges. Checks include 330 independent optima,
7,084 freezing events and three scoped Lean kernels. Newly reachable unused
betas are covered by the identity-safe continuation above; universal 5/6
improvement remains open.

New [shared prefix/suffix bridge compensation in one flow](docs/SHARED_PREFIX_BRIDGE_FLOW.md):
private reserves are no longer required when donors lie in deficient trees,
receivers in nondeficient components and candidate stem pairs are disjoint.
One receiver-slot min-cost flow gives exact declared-link payment and minimum
actual bridge fees, preserving every paid source and used original unit of
any maximum reference allocation. The upper bound covers multiple bridges
from one tree; one per repaired tree suffices. A frozen capacity-one pivot
gives shared-suffix payment 2 to 3, retaining both already used shared units;
all-q copies give 2q to 3q. Checks include 300 mode optima, 454 baseline audits
and 7,084 freezing events, plus two scoped Lean kernels. General shared-stem
geometry and universal 5/6 improvement remain open.

New [private prefix/suffix bridge compensation](docs/PRIVATE_PREFIX_BRIDGE_COMPENSATION.md):
two distinct request-private original units across a mixed entrance give
polynomial exact payment p+g-t0+d, with d distinct deficient donor trees.
One cheapest bridge per tree attains minimum actual bridge fees and retains
every paid source and used original unit of any maximum reference allocation.
A fully frozen capacity-two gap gives 3 to 4 payments; arbitrary separated
copies give 3q to 4q with q fresh units and bridges. Checks include 31 independent
optima, 169 maximum-baseline identity audits and 7,084 freezing events; a 16-copy
run forbids mode enumeration and full optimization. One general local exchange
kernel is axiom-free in Lean; the complete theorem has a written proof.
This certifies a coefficient-one counting class, while universal 5/6 remains open.

New [actual bridge compensation and a frozen entrance obstruction](docs/SINGLE_BRIDGE_COMPENSATION.md):
one added link between two old interval stems has exactly two routing modes,
giving payment p+g-min(t0,te) and exact source-preservation tests. For k bridges
on disjoint pairs of old stems, 2^k global resource-graph modes give maximum
payment then minimum actual bridge fees without repeated reserve credits.
On one fully frozen board a single capacity-one pivot changes the same old
three-source packing from payment 3 to 2. An upper bridge into five receiving
units still gives 2; a lower bridge with a usable prefix resource restores 3.
All-q separated copies prove the obstruction and repair scale exactly; the
unrestricted full original board still pays all 4q sources. Checks cover 184
bridge optima, 4,344 prescriptions and 576 batch fee/prescription optima.
The mode and geometric proofs are written, with independent executable checks;
no new end-to-end Lean or universal 5/6 improvement is claimed.

New [exact mixed-target zero-capacity optimization](docs/MIXED_ZERO_CORRIDOR_OPTIMIZATION.md):
all-state support monotonicity makes the final H and V gaps an exact protected
corridor family when variable tiles carry no positive units. Disjoint extreme
prerequisites give maximum payment, minimum actual activation fee and minimum
links in one full fork flow. With p positive-capacity variables, only their
2^p assignments need branching; zero-gate subsets are never enumerated.
Frozen two-direction fixtures give real payment gains from 4 to 8, and 36 zero
gates representing 2^36 states are solved in one flow. Independent checks cover
318 single-flow and 360 parameterized optima, including prescribed sources;
two logical Lean kernels are axiom-free. Unbounded-p polynomial optimization
for general mixed targets and a universal 5/6 improvement remain open.

New [three-snapshot signed support compiler for mixed target directions](docs/SIGNED_MIXED_SUPPORT_COMPILER.md):
arbitrary P-free changes of capacities zero, one and two have an exact
four-corridor-term description per original unit. Positive and negative gate
requirements retain destructive accesses; a polynomial test gives adjacent
physical loss witnesses. On passing inputs negative literals retract exactly.
An all-length feasible bent-owner family nevertheless acquires new support
before its own gate changes, refuting a final-direction-only compiler and
its access-fee estimate. Checks cover 1,509 states and 4,213 lattice edges;
two general logical Lean kernels are axiom-free. The zero-capacity and
positive-gate-parameterized joint fee continuation is linked above; general
unbounded-p polynomial optimization and universal 5/6 remain open.

New [exact destructive batch repair with no new physical links](docs/OLD_LINK_BATCH_REPAIR.md):
after arbitrary mixed-target P-free pivots, aggregate the new supports along
each old primitive and permit prefix truncation or beta-arm splitting. With
p old paid sources, g newly eligible direct sources and t deficient resource
trees, the exact optimum using subsets of the old pack's links is p+g-t.
Prescribed source sets have an exact mandatory-root test. Every original unit
is allocated once; the rule handles lost supports and occupied bands without
lossless handoff assumptions. Checks cover 976 optima and 3,862 prescriptions;
two structural Lean kernels are axiom-free. Full new-link repair and universal
5/6 remain separate questions.

New [full routing and shared activation fees by one weighted matching](docs/FULL_ROUTING_WEIGHTED_MATCHING.md):
the explicit mixed-capacity and separate beta-entry network has an exact
two-port matching representation. Dominant port-coverage weights enforce
routing conservation; idle edges save a one/two-output group's fee once.
This removes every 2^h branch for the recognized all-capacity uniform class:
one polynomial maximum-weight matching gives maximum payment, minimum actual
opening fee and minimum links, with prescribed sources and full competing
beta/mixed routing. A fully frozen 192×58 input with 12 sharing pivots gives
48 payments, fee 60 and 24 links in one matching. Six general priority/fee
Lean kernels are axiom-free; failed-guard compensation and universal 5/6 remain open.

New [positive-pivot extreme retraction and exact shared-fee optimization](docs/POSITIVE_EXTREMES_AND_SHARED_FEES.md):
every passing all-capacity uniform input retracts to the original first/last
gap units while preserving sources, owners and links, including old V-phase
local support. The only simultaneously shared positive fee is a containing
capacity-two pivot supplying its gap's two initially unsupported units to
distinct boundary owners. With h such pivots the exact joint payment/fee/link
optimum takes at most 2^h full min-cost flows; h=0 includes all capacity-one
inputs. A fully frozen adapter distinguishes actual fee 5 from the erroneous
per-end fee 6. Six ordered/fee Lean kernels are axiom-free; unrestricted
polynomial optimization and the universal 5/6 bound remain open.

New [positive-capacity handoffs: linear-state recognition and exact support compiler](docs/POSITIVE_CAPACITY_HANDOFFS.md):
uniform V→H P-free gates of capacities zero, one and two admit exact recognition
of all-subset support monotonicity in at most 2+2p physical snapshots, where p
counts positive gates. Closed-phase and singleton handoff guards replace the
old two-state test. A feasible all-length bent-owner family passes full endpoint
incidence inclusion but loses support in intermediate states; it is not fully
frozen and does not contradict the numerical grid bound. Passing inputs compile
to exact H-gap gate prerequisites, preserving actual shared fees without claiming
a general fee optimizer. Checks cover 1,332 states and 2,669 lattice edges;
three general phase lemmas are axiom-free in Lean. Universal 5/6 remains open.

New [uniform zero-capacity openings: two-state recognition and physical compiler](docs/UNIFORM_ZERO_CAPACITY_OPENINGS.md):
on any feasible grid, uniform V→H P-free capacity-zero gates have increasing H
resource support and decreasing V support. Full endpoint incidence inclusion
is equivalent to support monotonicity for every gate subset. Passing inputs
automatically compile into disjoint protected no-P corridors and one polynomial
costed fork flow, including arbitrary mixed/beta competition. Fine anchors allow
balanced TT/BB gates with changing coarse forest cells. A fully frozen28×48
control has payments3/2/4/3: equal endpoint values do not certify losslessness.
Checks cover954 physical states,2721 lattice edges and1750 strict freeze events;
four general recognition lemmas are axiom-free in Lean. Universal5/6 remains open.

New [protected linear corridors and extreme-resource joint repair](docs/PROTECTED_LINEAR_CORRIDORS.md):
arbitrarily many resource/gate prefixes collapse to the first and last original
units. Their disjoint end prerequisites give one polynomial min-cost fork flow
for maximum payment, minimum actual gate fee and then minimum links, with
arbitrary competing mixed/beta cores. A single-unit corridor keeps one shared
output. All-length fully frozen two-ended families realize both cases; an
outside-owner control proves why protection is required. Checks pass926 abstract
states,93 joint lex optima,507 protected-source optima and2088 physical states,
plus four scoped Lean lemmas. Original inventory is retained; universal5/6
and arbitrary branched/shared-gate adapters remain open.

New [mixed-resource dual parity and exact shared activation fees](docs/MIXED_RESOURCE_DUAL_PARITY.md):
arbitrary competing mixed relays and beta forks can participate in independent
one/two-original-unit gate bundles. Output linkability is a matroid; closing
paired groups preserves maximum payment exactly when their union is independent
in its dual. Weighted parity therefore minimizes once-per-group activation
fees, with one exact cross-component cut ledger and old-source retention at
the same optimum fee. A 16×58 fully frozen 32-state adapter includes genuinely
optional mixed routes. Reachability matching and group-index greedy have
explicit failed controls. Independent checks and four scoped Lean audits pass;
no polynomial rank-oracle parity algorithm or universal 5/6 improvement is claimed.

New [mixed-direction terminal defects and a sharp frozen obstruction](docs/MIXED_TERMINAL_DEFECT_AND_FROZEN_OBSTRUCTION.md):
for any valid even-rectangle H/V partition with actual M restored, each seam
terminal defect charges a different cross-direction actual edge. The global
port deficit obeys 2D_port<=d4+b+s<=d4+b+eHV, with one common original pool;
d4+b+s<=2beta+1 gives the coefficient-one counting bound on this class.
A fully frozen true maximum has all alpha ends degree3, d4=b=0 and full
D=k=eHV/2, proving the seam term sharp. Its mixed decomposition has an exact
all-T private-support profile and frozen net-loss frontier tau-k+d, attained
at zero links. General proofs, physical controls and scoped Lean audits
accompany the result; universal5/6 remains open.

New [exact frozen repair frontier under arbitrary selection exchange](docs/FROZEN_SELECTION_REPAIR_FRONTIER.md):
for the all-width adjacent-module family, every feasible T freezing the two
column3 leaves per module satisfies ell+D>=k+central_beta. Missing central
partners, terminal beta credits and original terminal intervals charge disjoint
physical cover members. The fully frozen optimum under D<=d is exactly
tau-k+d for 0<=d<=k; fixing central alpha/beta counts a,b sharpens it to
tau-k-b+min(a,d). Every frozen true maximum has D=k; arbitrary reselection
cannot avoid a net loss of k points to repair this horizontal decomposition.
Vertical bands repair the same maximum without loss. Written general proofs,
physical checks and scoped Lean audits accompany the result; universal5/6
remains open.

New [permanent links, the sharp completion budget and frozen birth circuits](docs/MONOTONE_COMPLETION_DEFICIT_AND_BIRTH_CIRCUITS.md):
for arbitrary fixed physical mixed-direction bands, feasible T additions retain
every old TP--BP band link. Exact full deficit is monotone and grows by at most
p-s, where p selections are added and s old betas become alpha. Any old packing
loses at most gap-capacity loss plus beta-to-mixed count of its old sources;
double-converted betas had no old incoming route and are not charged twice.
An all-width frozen family controls source births, private beta removals and
shared intervals jointly: deficit counts tree resource components with every
vertex endangered. Arbitrarily large birth sets have every proper subset
payable, but the whole set not payable, on the full original pool. Checks pass
2,260 controlled boards,10,436 event edges and scoped Lean audits. Universal5/6
remains open.

New [degree-changing bent completions and sharp full-network withdrawals](docs/DEGREE_CHANGING_BENT_COMPLETIONS.md):
the endpoint-degree-preservation assumption is removed for the occupied-bent
family. Every feasible fixed-P,M,old-T completion retains exactly q alphas,
each with a sharp private reserve of three units at w=6 and two at even w>=8.
All are paid at zero links on the full original pool. Degree-changing sealed
mixed chains make the full standard band-link withdrawal bound floor(r/g)
sharp, with no reachable beta fallback. A general fixed-body birth theorem
injects newly born alphas into distinct actual edges with nonadjacent physical
N partners; fully frozen mixed-seam families attain this tax. Checks pass196
family models,756 full-network withdrawals,24 sharp frozen seams and12 scoped
Lean audits. Universal5/6 remains open.

New [sharp private reserves in occupied bent gaps and exact beta repair](docs/BENT_GAP_PRIVATE_RESERVES.md):
occupied neighbours can force a blank row even when immediate BB exposure fails.
For every even width w>=6, all retaining degree-profile-preserving completions
of the frozen occupied-band family have at least floor(w/3)+2 private units per
alpha. An explicit completion attains this exact minimum. Distinct dedicated
beta owners repair arbitrary interval withdrawals: full value is always the
alpha count, and minimum links equal the direct deficit. Checks pass140 frozen
family models,56 mixed cuts,1,400 withdrawals and10 scoped Lean audits. The
correct density allows horizontal selected pairs; universal5/6 remains open.

New [frozen boundary obstruction and adjacent-band repair](docs/ADJACENT_BAND_BOUNDARY_REPAIR.md):
freezing and exact degree three do not exclude double-zero terminal-port paths.
An explicit frozen 144-endpoint board has two such paths, yet its complete
whole-support pool pays both at zero links. Two adjacent exposed BB/P bands
always supply a positive original unit; band-disjoint pairs avoid reusing units
within an owner. At least two pairs per global alpha give simultaneous zero-link
payment, including mixed-direction regions with actual matching seams restored.
The global incidence criterion G+2beta>=2alpha-1 gives coefficient one on this
class. Every fixed-P degree-three selection extension of the example family
retains four private reserves per alpha, with deficit at most floor(r/4) after
r unit withdrawals. Checks pass 215 physical models, 48 mixed partitions,
36,476 abstract withdrawals and 17 scoped Lean audits; universal 5/6 remains open.

New [terminal-defect compensation and exact joint withdrawals](docs/TERMINAL_DEFECT_PORT_COMPENSATION.md):
with the complete original interval pool and standard packet boundaries,
all degree-three alpha terminals have simultaneous zero-link payments, before
any pinwheel switch. More generally the exact port deficit is the number of
paths with two zero ends, and twice that deficit is at most the degree-four
alpha-terminal count plus explicit lateral-boundary defects. The note gives
the exact simultaneous interval-withdrawal profile and the coefficient-one
criterion d4+b<=2beta+1. Arbitrary interior degree-four vertices are allowed.
1180 physical models, 4720 withdrawal profiles, 5227 abstract optima and
16 scoped Lean declarations pass; general raw-boundary coverage and universal
5/6 remain open.

New [beta-core pinwheel switches and exact direction-optimized cuts](docs/PINWHEEL_BETA_CORE_SWITCHES.md):
the two-mixed restriction is removed. Any selected degree-three four-outward
pinwheel tiles, including beta paths joining two roots, optimize all directions
by one exact integral min-cost flow. A fixed outside beta core owns ONE whole
credit; stub-supported fork payments are normalized before the local switch.
This yields an exact joint source/resource/gate separator and retains the
one-unit-per-flipped-root gain bound. An explicit frozen 322-endpoint bridge
shows duplicated beta credit falsely reports payment two instead of one;
all 64 subsets of its six proposed links verify the actual payment. Its full
original pool already pays all four sources. Checks pass 102 physical pool
comparisons, 1,680 abstract orientation comparisons and four scoped Lean
declarations. General donor coverage and universal 5/6 remain open.

New [exact two-track switches at degree-three pinwheel tiles](docs/PINWHEEL_TWO_TRACK_SWITCHES.md):
every four-outward full-P tile in the degree-three bundle-terminal class has
two distinct BP-bearing owners; each mixed owner meets at most one such tile.
When both tracks are mixed, flipping the root exchanges their BP-to-TP
pairing, preserving all physical terminals, links and original resource
identities. Any number of these switches optimize jointly by ONE exact
two-by-two-switch min-cost flow, including shared resources and untouched
beta forks. Gain is at most one per flipped root. An all-q frozen physical
family attains gain q on a restricted original pool, with q actual links;
the full pool already pays q at cost zero. Checks pass 140 physical pool
comparisons, 1,490 abstract orientation comparisons and six scoped Lean
declarations. General donor coverage and universal 5/6 remain open.

New [four-outward alpha localization by degree defects and direction interfaces](docs/FOUR_OUTWARD_ALPHA_LOCALIZATION.md):
for any collection F of four-outward full-P tiles in a bundle-terminal pair,
the number I_F of original alpha wire incidences satisfies I_F<=2J4+E_dir.
Here J4 counts occupied-degree-four endpoints and E_dir counts actual matching
edges between opposite auxiliary directions. The sharper local inequality
2i_Q<=3a_Q+b_Q+2c_Q retains endpoint and seam identities, so no edge is
credited twice. Exact degree three with uniform direction excludes all
alpha wires at these tiles, even in multi-square components. A frozen 14-by-14
example attains i_Q=c_Q=1 after one tile's direction changes, and separately
shows source-reachable mixed owners cannot simply be pruned. Checks pass
728 partitions/4,853 tiles and 11 scoped Lean declarations. This localizes
the geometry; unused donor coverage and universal 5/6 remain open.

New [four-outward capacity-two slab with one unit of negative charge](docs/FOUR_OUTWARD_SLAB_AND_ONE_UNIT_OBSTRUCTION.md):
for every h>=1 a fully frozen (2h+4)-by-8 board has 2h aligned full-P tiles,
each with all four actual mates outside, yet its ENTIRE negative physical
charge is just one unit. Every such tile contains a wire of the same alpha
and a wire of the same PP/M cycle. This refutes removing square uniqueness
from the two-unit compensation theorem while keeping four outward mates;
independent per-tile credit fails without bound. The board itself has
objective half-area minus one and its sole alpha is paid on the full pool.
Checks pass 75 physical models, all 19,682 nonempty oriented bundles on the
smallest witness, and 13 Lean declarations including its physical freezing
and complete one-unit charge certificate. Universal 5/6 remains open.

New [joint direction/deletion repair and the exact two-budget frontier](docs/JOINT_DIRECTION_AND_ISOLATED_DELETION_REPAIR.md):
guarded switches and outside occupied-isolated deletions compile to one fixed
candidate-resource network; inside-strip deletions are dominated. For switch
budget s and deletion budget d, gain is exactly min(R,s+d,s+RC,d+RH).
A single lex flow retains old paid sources and minimizes point loss, flips,
weights and links. At maximum payment the sharp S+D improvement is min(s,RH);
deletions cannot improve that budget beyond the available direction rank.
A fully frozen all-candidate family has exact value min(q,s+d,s+q-1): deleting
ALL isolated points still leaves one unpaid, while one flip plus q-1 effective
deletions pays all, or q flips pay all with zero point loss. The universal
5/6 question remains open. Checks pass 930 physical models, 108 actual-grid
quota profiles, 149 independent lex optima and 15 scoped Lean declarations.

New [guarded strip switches and dual-source repair](docs/GUARDED_STRIP_SWITCHES_AND_DUAL_REPAIR.md):
explicit physical guards let a strip direction change preserve all old owner
identities, used resources and links, while opening private zero-link payments.
For any eligible F, exact value is |F|+r(A minus F), with minimum links equal
to the old complement-source optimum. Gains are a standard dual source-matroid
rank, giving optimal switch counts, weighted choice and old-source retention.
A fully frozen shared-seam stack realizes one repair credit per path component:
every single flip can gain one while all flips together still gain only one.
Checks pass 1508 physical models, 480 exact value/cost profiles and 13 scoped
Lean declarations. No selected points move and no reserve is credited twice.
Universal 5/6 is open.

New [isolated-candidate obstruction and exact strip-direction repair](docs/ISOLATED_COVERAGE_OBSTRUCTION_AND_STRIP_REPAIR.md):
for all even W>=8 and k>=1, a fully frozen mixed partition with 2k actual
matching crossings has k unpaid sources even after ALL occupied-isolated
selections are removed. Every such source has a one-owner reachable closure
and empty support, so arbitrary routes and beta forks cannot help. Flipping
any f prescribed narrow strips pays exactly f sources with zero links,
unchanged physical source identities, and no deletion required. Private
singleton reserves prevent duplicate credit. Checks pass 568 physical
models, 244 independent primitive profiles and 13 scoped Lean declarations.
This refutes automatic
candidate coverage in a fixed conservative mixed network; the family has
a zero-loss direction repair and gives no numerical 5/6 counterexample.

New [isolated-selection repair choice and one combined budget](docs/ISOLATED_SELECTION_REPAIR_MATROID.md):
in any fixed even-rectangle mixed-direction partition, deleting occupied-
isolated selections adds distinct original singleton sinks while preserving
all old resource identities, terminal gates, links and freezing. Candidate
payment gains are a standard contracted resource-matroid rank, including
mixed and beta forks. If all candidates gain R payments, exactly R deletions
suffice, retaining every old paid source. A single lexicographic flow chooses
minimum-count, minimum-weight repairs and then minimum links. Zero individual
optimized gains imply zero joint gain, and S+D increases exactly by deleted
count minus rank gain. The adjacent maximum family has exact free-location
optimum k deletions/k links. Full geometric candidate coverage and 5/6 remain
open; the general proof does not assert all isolated candidates always suffice.

New [two-sided seam budgets and unbounded prescribed-repair recourse](docs/TWO_SIDED_SEAM_BUDGET_AND_UNBOUNDED_RECOURSE.md):
any m prescribed upper/lower singleton openings lower the true fixed-P
selection maximum by exactly m, with frozen attainers. Their full-pool
compensation is an exact path multigraph: each component with a doubled
seam pays all sources; each other component leaves one unpaid. The first
double's distance from the left boundary gives the exact extra link cost.
Opening one upper unit at position p repairs a k-source lower path, but
forces p-1 old unit reassignments and raises minimum links from k-1 to k+p.
The bounds are attained; choosing p=1 instead avoids old reassignments.
Checks pass 730 frozen boards, 85 independent primitive profiles and 15
scoped Lean declarations. Other partitions and the universal 5/6 bound
remain outside this result; vertical full compensation holds for this P.

New [sharp seam-opening budget and FULL-pool path circuits](docs/EXTREMAL_SHARED_UNIT_BUDGET_AND_FULL_POOL_PATH_CIRCUITS.md):
on the adjacent-module endpoint family, prescribing any m shared singleton
seams open lowers the true fixed-P maximum by exactly m, with frozen attainers.
Their full original pools pay m of k sources. Opening all k-1 seams gives
an arbitrarily large minimal unpayable source set and a unique violating
withdrawal of size k-1; bounded-order withdrawal checks cannot suffice.
Keeping all sources except source r costs exactly k-1+r links.
A mixed interface specialization is exactly one selection below the true
maximum. Checks pass 95 frozen boards, 629 path withdrawals, 100 maximum
source-basis costs and 17 new scoped Lean declarations. This endpoint family
still admits vertical full compensation; the universal 5/6 bound remains open.

New [FULL-pool interface singleton and exact repairs](docs/FULL_POOL_INTERFACE_SINGLETON_AND_REPAIR_PROFILE.md):
for every even W>=8 and every subset of s repairs among q frozen copies,
closed local systems pay q and the interface alone pays q, yet the full
restored mixed-direction model pays exactly q+s, leaving q-s unpaid.
An arbitrary-route eight-owner closure excludes all other original units
and every beta sink. Unrestricted minimum links are s; retaining all old
paid source identities costs exactly 2q-s. A selected lower-route baseline
has nu=0 even on the full pool, while theta=s; locally minimum-cost baselines
already attain nu=s. Checks pass 92 full-pool frozen boards, 1,176 withdrawals,
24 independent primitive profiles and 21 scoped local Lean declarations.
This extends the existing sealed-board singleton family; global extremality,
alternative partitions and the universal 5/6 improvement remain open.

New [interface reserve reoptimization](docs/INTERFACE_RESERVE_REOPTIMIZATION.md):
local routes can be rearranged while retaining every initially paid old
source. The exact additional interface payment has one joint original-resource
cut criterion, with withdrawals restricted to units shared by local and
interface networks. It dominates matching into one fixed pack's unused units.
A fully frozen all-even-height mixed-direction family gives a strict gain
on a stated two-unit pool; its chosen baseline maximizes value, not minimum
link cost. A two-entry beta fork shows why direct matching rank cannot be
added without charging old withdrawal losses. Checks pass 293 models,
72 prescribed maximum old paid sets and 14 scoped local Lean declarations.
Full-pool geometric control and the universal 5/6 improvement remain open.

New [strict beta-cut promotion and shared reserve](docs/BETA_CUT_PROMOTION_AND_SHARED_RESERVE_OBSTRUCTION.md):
in the largest-source-side minimum cut, every nonempty receiver set Q has
at least |double-entry receivers in Q|+1 different far-side interval witnesses.
Double-entry receivers admit a matching even after deleting any one interval;
under two owners their witness graph has degree at least two and no pure
cycle component. An all-q abstract family nevertheless has only one globally
unused interval, refuting per-receiver fresh-reserve accounting. A complete
finite frontier of 6136 frozen boards (four old matchings, at most two added
selections/edges) has full ordinary compensation. Checks pass 137,272 strict
promotion inequalities, six scoped Lean audits and the original flow suite.
The general geometric cut bound and universal 5/6 improvement remain open.

New [one exact whole-support fork flow and resource cuts](docs/WHOLE_SUPPORT_FORK_FLOW_AND_RESOURCE_CUTS.md):
separate capacity-one gates for the two physical beta BP entries, one private
whole-beta sink and beta-body support arcs give a single polynomial min-cost
maximum-flow formulation of the full stem/fork optimum. Free private-beta
normalization proves the reverse lift; compatible-fork enumeration is no
longer needed. The exact deficit is max_Z(|U_Z|-|Z|), now including BP entry
gates and whole-beta support closure. Checks pass 11,308 independent packing
comparisons, 96,843 terminal matchings, 24 frozen stacks and five scoped Lean
audits. All four perfect matchings on the base fixed endpoint footprint also
have no strict ordinary/full gap. Mandatory interval-identity retention is
outside this unrestricted optimum theorem; the general grid bound is open.

New [guarded pockets and monotone fork replacement](docs/GUARDED_POCKETS_AND_MONOTONE_FORK_REPLACEMENT.md):
a general two-column pocket in an occupied adjacent-band pattern either
retains private interval credit or becomes one forced beta accessible only
from its old alpha root. Any fork rooted there, including bent mixed arms,
has an ordinary replacement preserving every outside certificate and not
increasing links. Tertiary fork minimization gives full ordinary exactness
when all feasible forks meet guarded roots. All-q base stacks with arbitrary
pocket insertions have exact value 3q and minimum links q+|S|. Checks pass
224 frozen boards/308 replacements and four scoped local Lean audits.
The filled case can tie link cost; not every optimal fork is excluded.
General grids and the 5/6 improvement remain open.

New [joint allocation exchange and exact terminal-fork defects](docs/FORK_ALLOCATION_EXCHANGE_AND_CLOSED_TREES.md):
ordinary interval assignments may reroute while preserving every old paid
ordinary source and every old used interval identity. With h forks, m interval
stems and joint matching number mu, the exact fixed-route ordinary value is
t+h+mu. In a minimum-link maximum packing with two-owner supports, each
terminal fork sees disjoint closed ordinary trees with one private entrance
each, and the joint defect is exactly the number of terminal forks. An
arbitrary-length abstract chain reduces the fixed-assignment defect q to 1.
Selected-only shielding of the known C gap is impossible; inserting a matching
edge instead creates an ordinary beta resource. Checks pass 714 exchanges,
638 exact terminal-defect identities, 12 frozen lifts, the 68-endpoint insertion
and 13 scoped local Lean audits. Full-network geometric sufficiency and a
universal 5/6 improvement remain open.

New [exact fork deficits and wide-arm-gap exclusion](docs/FORK_REPLACEMENT_DEFICIENCY.md):
fixed fork arms have ordinary value h+mu=2h-delta, with delta the Hall defect;
under two-owner supports delta counts deficient substitute trees. In a
maximum-payment minimum-link packing, every pre-beta arm unit must be blocked
by a different outside certificate and, under the physical two-owner condition,
a different unique outside owner. Thus an arm gap with two available original
units excludes that fork from an optimum. Fork interval dependencies are
acyclic and end at an ordinary-blocked sink or empty arm support. An all-length
abstract chain has full value2q+1 versus ordinary2q; physical realization
remains open. Checks pass985 replacement systems,251 full networks,1506 physical
token inequalities and12 new scoped Lean audits. Exact beta-retaining cost is
distinguished from unrestricted ordinary cost; the submitted paper is preserved.

New [completely frozen beta fork and exact arm-replacement criterion](docs/FROZEN_BETA_SUPPORT_FORK_AND_RESERVED_RESOURCE_GAIN.md):
an explicit16-by14 board with66 frozen endpoints refutes universal beta-fork
exclusion. Two different alpha arms enter different tips of one beta and
use its internal original interval: one whole beta plus one interval pays2.
A reserved interface has strict value2vs1; unrestricted value remains3 with
one link. Arbitrary separated copies give reserved gapq; right padding
releases a boundary unit and lowers full link cost to0. A general fixed-arm
Hall criterion exactly characterizes simultaneous ordinary replacement and
saves at least one link per replaced fork; shared substitutes must be counted
once. Checks pass20 physical boards/16 stacks,784 abstract replacement systems,
and12 new scoped Lean audits. Unrestricted strict gain and the general5/6
bound remain open; the submitted manuscript is preserved.

New [exact whole-support stem/fork normal form](docs/WHOLE_SUPPORT_FORK_NORMAL_FORM.md):
whole-support interval witnesses can belong to beta bodies. Two different
alpha arms entering its different BP tips then consume one whole beta plus
one distinct original interval, paying two demands. Every cancellation and
support allocation normalizes with a subset of its links into ordinary stems
and disjoint beta forks. Reserving forks gives an exact residual-flow formula
for maximum compensation and minimum link cost; without feasible forks,
including every beta-free system, ordinary owner-support flow is exact.
The possible value gap is at most the beta-to-support-interval matching number
and half the alpha count, sharply in abstract systems. Checks pass10,906
abstract/2,442 frozen physical systems and7 scoped Lean audits. Physical
controls contain zero forks; abstract gains are not claimed frozen-grid gains.
General grid compensation and the5/6 bound remain open.

New [actual whole-support donor collision and frozen PP seals](docs/WHOLE_SUPPORT_DONOR_COLLISION_AND_FROZEN_PP_SEALS.md):
an all-even-height frozen family has two genuinely deficient whole-support
components. Distinct legal mixed continuations each pay one separately, yet
together expose the same original interval and pay only one (d=2,S=1).
Adding the second route after the first also realizes d=1,S=0, gain0.
Pure PP seals remove the old internal-support bypass; arbitrary blank right
padding preserves the collision and separated stacks give residual defectq.
Different lower original intervals repair all copies, with exact further-link
costs and positive target margin. Checks pass84 boards/420 transitions/24
stacks, plus10 new scoped Lean audits. Full mixed compensation and a universal
5/6 improvement remain open; the submitted manuscript is unchanged.

New [exact mixed-extension component reserves](docs/MIXED_SUPPORT_COMPONENT_MERGE_ACCOUNTING.md):
for every monotone interval-incidence extension retaining at most two owners
per original unit, each resulting component gains exactly min(d,S) payments,
where d counts its old deficient components and S its OLD unused original
units. An already used interval is not fresh credit; distinct continuations
to the same unused unit still share one reserve. Augmentation preserves the
old paid-owner set and used-unit set, adding exactly the actual payment gain
in different old unused units. Checks pass13,265 models, including4,005 physical
whole-support batches and85 explicitly terminal/cap collision transitions;
these whole-support controls have no cross-component merges. Eleven scoped
Lean audits pass. Finding generally sufficient legal mixed continuations
remains open; the submitted manuscript is unchanged.

New [sharp physical beta Hall defects and mixed repair](docs/BETA_CLOSING_AND_SHARP_MIXED_DEFECT.md):
one safe selection changes a beta into a mixed strand while preserving all
freezing certificates, original interval identities and alpha supports.
All-length capped boards and arbitrary separated stacks have actual direct-beta
Hall defectq, attaining the two-external-witness bound with2q mixed witnesses
and no boundary witness. Thus universal direct-beta saturation under feasibility
and freezing is false. Full compensation still takes exactlyq mixed links to
different original unused intervals, preserving all old B-to-J assignments;
the target margin remains positive. Checks cover105 physical models, including
9 with betas confined to other components, plus8 new scoped Lean audits.
The general mixed continuation problem remains open.

New [interior frozen caps and external-witness bound](docs/INTERIOR_SUPPORT_TREE_CAPS_AND_EXTERNAL_WITNESSES.md):
an explicit all-length PP cap seals the earlier two-owner support tree's boundary
exits without adding beta credit. Its interval defect survives arbitrary blank
right padding; distinct direct-beta and mixed repairs retain exact resource
ledgers. For original alphas before cancellation, every deficient support tree
has two external terminal witnesses. Whole-beta capacity2 and mixed/mark
capacity1 imply t-mu <= floor((q+h)/2), with identities counted globally once.
This sharpens the remaining obstruction rather than proving full compensation.
Checks cover96 cap/isometry/padding boards,36 stacks,59 physical token models,
1,847 abstract models and24,619 subset inequalities. Eight scoped local Lean
audits pass; the general geometric and matching adapters remain written proofs.
No physical beta Hall failure or universal5/6 improvement is claimed.

New [actual frozen support-tree rerooting](docs/FROZEN_SUPPORT_TREE_AND_FORCED_REROOT.md):
a 12-by-18 grid with 46 completely frozen matching endpoints has two alpha
owners sharing exactly one unmarked original interval, and one beta directly
reachable by only one alpha. A specified maximum interval baseline therefore
requires one old assignment change for full direct beta compensation.
Disjoint stacking gives any number of simultaneous physical tree rerootings.
An explicit mixed repair instead adds a new interval and keeps the old
assignment; right blank padding releases two marked exits and removes the
tree defect. Checks cover all 1,980 fixed terminal matchings, including 504
nonsingleton positive reroot controls, eight isometries, sixteen stacks and
sixteen padding controls. Thirteen new scoped Lean audits pass locally.
Interior Hall obstructions and a universal grid bound remain open.

New [joint support-tree / whole-beta compensation](docs/JOINT_TREE_BETA_COMPENSATION.md):
after any fixed cancellation, match deficient interval trees to distinct whole
virtual betas, then choose the unpaid tree roots at the witnessed beta links.
The exact direct-interface optimum is k-t+mu, with exactly mu extra beta links,
while preserving all previously paid demand owners and used original interval
identities. A minimum-weight maximum matching gives the exact minimum number
of old interval assignments changed, using tree-distance rerooting costs.
Checks pass 5,413 exhaustive and 7,544 independent flat optimization comparisons,
491 physical fixed-cancellation lifts, and 14 scoped local Lean theorem audits.
Those original frozen controls repair 56 tree occurrences but contain only
singleton deficient support trees; the later constructions above supply
nontrivial physical rerooting. Geometric beta Hall expansion remains open.
General written proofs are distinguished from the
scoped formal checks. The submitted manuscript is unchanged.

New [full-gap obstruction and whole-support compensation](docs/BOUNDARY_SEALED_GAP_OBSTRUCTION.md):
complete freezing and a unique actual matching do not force compensation
even in the full endpoint-free-gap terminal network. An all-parameter family
has no reachable unmarked interval and positive margin on the ENTIRE board;
separated copies give arbitrarily large unpaid count with an empty two-phase
unit cut. The target grid inequality is not refuted. A general whole-support
gap adapter admits internal PP witnesses, retains at most two virtual-alpha
owners per original interval and gives exact standard tree-defect allocation.
It repairs the whole obstructed family without a new link. Eleven scoped
Lean audits pass locally; the physical all-parameter and allocation proofs
are written. A separate real frozen control shows interval-only defect zero
is not automatic either; whole beta resources remain necessary.

New [extreme-interval compression theorem](docs/BT_CORRIDOR_PORTS_AND_BOUNDED_ACCESS_OBSTRUCTION.md):
every full endpoint-free-gap interval payment can be moved to one available
extreme per candidate terminal while preserving the paid virtual alphas,
paying terminals and all chosen links. Maximum compensation and minimum link
cost are unchanged, including arbitrary fixed reservations when available
extremes are recomputed. With boundary reservations alone these are exactly
first-BB accesses through BT corridors, at most two targets per terminal.
The proof retains each original interval as one unit. Checks pass 1,840
optimization/transport controls and 9,727 reserved local transports; 16 scoped
Lean theorem audits pass locally. A smaller frozen access obstruction has
exact one-sided cost 2, two-ended cost 2+H/2 and positive packet margin;
the general impossibility of bounded-radius access was already established
in the earlier gap note. Universal grid compensation remains open.

New [blocked-mark capacity theorem](docs/BLOCKED_MARK_CAPACITY_AND_39_41.md):
forced original corner events exclude mark slots instead of creating another
reserve pool. A terminal-to-corner injection prevents reuse across the three
residual types, including occupied adjacent bands. Together with the complete
cost-fifteen classification this gives coefficient39/41 on the SAME specified
COMPLETE source/representative-ledger domain. Twelve scoped Lean theorems and
three definitions pass15individual axiom audits. Exact checks cover864complete
images,152fired corner occurrences and151875conditional budgets; complete
cost-fifteen bad cases occur ZERO times, so those branches rely on the general
written proof. Independent review13e74748 ACCEPTS this theorem and the
previous tight-clearance supplement under enumerated established dependencies.
No arbitrary-grid theorem is claimed.

New [cost-fourteen compensation theorem](docs/COST_FOURTEEN_GEOMETRY_AND_37_39.md):
U(8,6,8) forces a protected pair tile; an uncompensated U(8,4,10) forces a
distinct original negative height-eight leg. Their shared physical injection
and original matching budget give coefficient37/39 for the specified COMPLETE
source model under the existing representative ledger. Nine new geometry
Lean lemmas complement the six previously checked counting lemmas. Exact
controls allocate256actual defect slots in832complete images, with ZERO new
cost-fourteen double occurrences; those branches rely on the written
all-parameter proof. Independent reviewacdb2fae ACCEPTS Sections1--6 under
the enumerated dependencies, with the same-tile gate bridge explicit. The earlier
[conditional reduction](docs/COST_FOURTEEN_COMPENSATION_REDUCTION.md) is preserved.
Section7 gives a later arbitrary-height tight-terminal pair lemma, strengthening
the shared reserve to2R>=2z+s+2t+p and expanding the26/27 actual-double class;
three more Lean lemmas and1408local masks pass. This supplemental extension is
OUTSIDE that completed review; the later39/41 review independently ACCEPTS it.

New general complete-source coefficient:
[the low-cost double obstruction](docs/LOW_COST_EXCEPTIONAL_DOUBLES_AND_35_37.md)
excludes two occupied, unactivated gates for U(8,4,8) and its reflection.
Adding these shapes to the single-use two-slot class raises the remaining
exceptional matching cost from13to14, giving35/37 instead of33/35 for every
complete-source fusion under the existing representative ledger.15scoped Lean
theorems/16audits,323role collisions,704complete physical images and19691signed
budgets pass; independent written review ACCEPTS this35/37 theorem. No newly covered double shape
occurs in the physical fixtures, and arbitrary-grid decomposition remains OPEN.

Latest complete-exterior checkpoint: the [localized general theorem](docs/LOCALIZED_COMPLETE_EXTERIOR_BUDGET.md)
now has independent ACCEPT: every complete extension of the specified canonical
nested core has exterior marginal>=2+P_out and chamber marginal>=3+P_i,
including finite unequal/coincident wall tips and detached exterior sources.
The original support-incidence multiplicity is retained at the incomplete old
boundary.18 scoped Lean theorems and exact controls pass. Its later width6
marked-slack consequence sigma>=4d-P_out improves5/6 to1 when P_out<=4d,
under the existing source-to-grid ledger; that corollary now has independent
ACCEPT. The new [arbitrary tile-cut identity](docs/ARBITRARY_TILE_CUTS_AND_SIGNED_ROTOR_FLUX.md)
allows cuts through added U/rotor sources by assigning physical terminal credits
and conserving signed rotor transfers.122572 cuts through736 complete inventories
and13 scoped Lean theorems pass; independent written review ACCEPTS it. Source-crossing
regional accounting terms are not source-addition marginals. Sharp exterior5,
arbitrary grid decomposition/marked allocation and the global grid targets remain
OPEN. The11October submitted manuscript is unchanged.

The [actual-mark refinement](docs/WIDTH_SIX_CORE_UNMARKED_AND_EXTERIOR_MARK_EXCESS.md)
proves that earlier old B sources and positive chamber sources are unmarked.
For width6 and all gaps10, coefficient one therefore follows when the number
of doubly marked exterior positives minus unmarked exterior positives is at
most4g+2d. This removes an upper bound on the total exterior-positive count.
The written proof,640 physical images,150 whole families and13 scoped Lean
theorems pass; its separate independent written review ACCEPTS this theorem. The initial controls
have no singly marked exterior examples;20supplemental complete families now
exercise90such occurrences and realize unbounded single-mark counts.

Latest width5 checkpoint: a [general forced-stack theorem](docs/SECONDARY_TEN_WIDTH_FIVE_STACK.md)
classifies every actual cavity owner in a complete extension as a left-bar
U(H,4,4), with even heights>=6 partitioning N=z-2. A right-bar owner
would force a further original into a sealed width3 notch and is excluded.
The whole stack has exact increment N/2-k-4>=4; the width5 enlarged
group has gain>=L/2+11>=14. Across the stated staircase branches a
specified single group has gain>=L/2+9>=12.248 exact controls including
32 nonuniform staircases and34 scoped Lean declarations PASS. For pairwise
disjoint physical tile footprints, the new stack increments add exactly and
give >=4 per cavity; the OLD prefix reserves still need allocation. Independent
review ACCEPTS the stack classification/ledger and single-group theorem;
the simultaneous corollary is outside that input. Full immutable data under
long-axis reversal and the extension-dependent selection are explicit.
The preceding sealed-cavity/>=10 theorem is also ACCEPT.
Allocation among overlapping groups and the global grid targets remain OPEN.

Latest complete-prefix checkpoint: a [general sealed-cavity proof](docs/SECONDARY_TEN_SEALED_ROOT_CAVITY.md)
excludes width1/3 trapped-support prefixes from every complete extension in
the explicit full-U/rotor model. For the stated actual four-row staircase,
complete extendibility therefore strengthens the selected-union bound to
DeltaPhi>=L/2+7>=10. The earlier six-unit equality family remains a correct
geometric calculation but cannot extend to a complete configuration.
192 exact cavity controls,216 U/8 rotor orientation controls and28 scoped
Lean declarations pass. Independent review completed ACCEPT; its width3
control-range correction6<=L<=v-2 is implemented. A width5 geometric
control attains10; its complete extendibility and global allocation remain OPEN.

Latest sharp-staircase checkpoint: a [general all-parameter proof](docs/SECONDARY_TEN_ROOT_SHARP_STAIRCASE.md)
improves the actual-staircase selected-union bound to DeltaPhi>=L/2+3>=6.
Only J1/J2 can have a far-pair receipt, and the owners debited by A and
P1 are disjoint. An unbounded geometrically admissible family attains
L/2+3 for every even6<=L<=v; complete extendibility is not asserted.
128 equality-family controls,70 nonuniform controls, targeted boundaries
and13 scoped local Lean declarations pass. Both the earlier >=2 theorem
and the new sharp theorem/equality family have independent ACCEPT.
Full-family allocation and the global grid targets remain OPEN.

Latest actual-staircase checkpoint: a [general receipt partition](docs/SECONDARY_TEN_ROOT_ACTUAL_STAIRCASE.md)
gives DeltaPhi>=L/2-1>=2 for ANY endpoint-disjoint actual dimensions in
the forced four-row staircase, conditional on the explicit full-U/rotor
model and retained H3+B+R+A. Two possible P1 contacts share ONE width
budget; staircase-pair tiles and old-boundary receipts are assigned once.
113 reproducible exact-set samples, simultaneous-contact and long-chain
controls, and11 scoped local Lean theorems pass. Its independent geometric
review completed ACCEPT; the nonfull upper boundary event is clarified.
This is a selected-union
compensation lemma, not complete-family allocation or a global grid bound.

Latest forced-chain checkpoint: the fourth owner forces THREE further
distinct west-terminal U's, forming a four-row support staircase. A
[general depth-height tradeoff and geometric frontier](docs/SECONDARY_TEN_ROOT_SUPPORT_STAIRCASE.md)
force L<=v or L=v+2,f<=z-12. Explicit witnesses prove the geometric
converse; their exact seven-owner ledger is v/2+L/2+10-3epsilon>=19,
including the tight P1 contact debit. Arbitrary actual staircases need
not be these witnesses.1280full-original witnesses,130exact-set controls
and20scoped local Lean declarations pass. Its original independent review
terminated with no_assistant_output and no mathematical verdict;
the fourth/reflected review completed ACCEPT. Complete-family
allocation and the global grid targets remain OPEN.

Latest fourth-owner checkpoint: after the reflected cavity exclusions,
R's missing support forces a fresh west-terminal U with a downward bar.
The [full parameter classification and exact four-owner ledger](docs/SECONDARY_TEN_ROOT_FOURTH_CONSUMER.md)
give joint gain u/2+v+L/2+19>=40, with TWO three-owner full tiles each
counted once. The fourth marginal is 1-(u+L+12)/2 and can be arbitrarily
negative. Geometric feasibility also forces L<=v+6 or L=v+8,f<=z-10.
76608classification/1376exact-set controls and25scoped local Lean
declarations pass; reflected/fourth independent follow-up completed ACCEPT.
Geometric compatibility is not complete extendibility or a global bound.

Latest complete-root checkpoint: the [two-direction cavity lemma](docs/SECONDARY_TEN_ROOT_CAVITY_EXCLUSION.md)
excludes depth8 and, by reflection at R's missing support, ALL depth6 and
tight-width depth4 t0 owners. Conditional on the specified first deep B,
actual t0 owners must have incident4, even breadth6..v+10 and far4..z-8.
Their exact triple gain is u+v+L+24>=54, counted in one nonreused ledger.
40scoped local Lean declarations and full-original controls pass. The
fresh triple retry and initial generic-cavity/d8 audit both completed
ACCEPT. Coordinate wording and the eight rotor matching placements
(four non-tips, four tips) are clarified. Reflected applications are in
the fourth-owner independent follow-up, which completed ACCEPT. No
complete extension or global bound is asserted.

Latest root triple checkpoint: the actual t0 owner, conditional on the
specified deep B and arbitrary forced E owner R, has an all-parameter
left-U classification with incident depth4/6/8 and explicit breadth/far
bounds. The [single joint ledger](docs/SECONDARY_TEN_ROOT_DEEP_TRIPLE.md)
gives gain>=46. The depth8 partial branch has marginal-3 or-2, so adding
a previously positive one-owner receipt would double-count occupied-band
resources.33984classification/1152exact-set controls and29scoped local
Lean declarations pass; independent triple audit completed ACCEPT. The prior
root pair audit completed ACCEPT. Full global allocation remains OPEN.

Latest surviving-depth checkpoint in the full U/rotor model: the specified
first/root right B with incident depth z+4 and far depth4 forces its actual
E-support owner to be a RIGHT U(L,8,f), every even L>=h+2,f>=4. Its
original charge is+1 and exact marginal+1, giving selected-pair gain
u+v+25>=49. The [general classification and physical receipts](docs/SECONDARY_TEN_ROOT_DEEP_PAIR.md)
count an essential three-owner bottom tile once.22scoped local Lean
declarations and exact-set controls pass; independent written review ACCEPT.
Complete extendibility and global bounds are not asserted.

Latest complete-extension checkpoint within the full U/rotor model:
each old E support forces a fresh
north-terminal U owner containing nine consecutive specified endpoints.
The [general mandatory-footprint proof](docs/SECONDARY_TEN_MANDATORY_E_FOOTPRINT.md)
excludes BOTH recent unraised/raised right-band families, including their
shortest far legs. Their exact joint receipts remain correct for partial
inventories; they have no complete-family instances. Arbitrary right
incident depth D/far g in the same breadth frame must satisfy D<=z-12
or D-g>=z. Also2n same-color forced terminals need2n distinct fresh
owners. E-owner original charges are-1left/+1right, each contributing1
to N+S, so the selected-owner inventory is sum(t breadth-1)+n>=6n.
The earlier claim that every fresh owner has negative mass>=5 is withdrawn.
34scoped local Lean declarations and exact controls, including5040physical
phase charge counts, pass. Initial written review confirmed the geometry
but required this charge correction and explicit global U/rotor premise;
corrected follow-up completed ACCEPT. No net global bound or general-grid
catalogue exhaustion follows. Global5/6 and grid equality remain OPEN.

Latest mixed-direction checkpoint: a prescribed right-band owner has
unbounded exterior debit -(u+13), yet its forced actual predecessor is
completely classified and their exact joint gain is v+10+epsilon>=22.
An essential three-owner full tile contributes+2; each physical receipt
and original source mass is used once across arbitrary paired chains.
The [general proof](docs/SECONDARY_TEN_RIGHT_BAND_FORCED_PREDECESSOR.md)
has an ACCEPT audit for far depth4, with41scoped local Lean declarations
and exact-set controls passing. The geometric far-depth6/8 corollary also
has an ACCEPT audit; an additional matching argument excludes those two
depths from every complete extension. Thus actual owners in this specified
family have far depth4. Arbitrary right owners and global bounds remain OPEN.

Latest old-chain exterior checkpoint: one arbitrary actual LEFT consumer
has exact gain H-1-delta against the entire old renewed-support chain,
where delta is0or1 and the latter requires H>=28. Thus the gain is at
least5, with equality exactly at H6. The
[unbounded classification and physical-set proof](docs/SECONDARY_TEN_LEFT_CHAIN_EXTERIOR.md)
has a separate ACCEPT review after explicit parity/frontier clarifications;
130302collision and64164exact-set controls through24blocks and24local
Lean declarations pass. Interactions among multiple new consumers and
the global complete-family bounds remain OPEN.

Latest arbitrary-consumer checkpoint: every actual renewed-support consumer
in the prescribed single block has local gain at least1, with all unbounded
U parameters classified and the equality cases identified. An explicit
arbitrary-length nested family has exact joint gain H_0-3n+2 even though
every insertion after the first has marginal gain-3. Its forced outer
breadth pays the losses using each source mass once. The
[general proofs and scope](docs/SECONDARY_TEN_ARBITRARY_T_CONSUMERS.md)
have an ACCEPT written review;48local Lean declarations and exact
full-original controls pass. Arbitrary multi-block consumers, global5/6
improvement and rectangular-grid triple equality remain OPEN.

Latest internal-owner checkpoint: arbitrarily long acyclic consumer paths
have zero signed exterior remainder but lose one unit per block against
the summed baselines. Completeness forces one fresh negative U per block,
all distinct by terminal checkerboard color. A simultaneous full-original
choice of those consumers still has exactly zero gain, because occupied
adjacent-band losses exhaust their mass. The inventories are explicitly
incomplete and do not refute a complete-model bound. See the
[general construction, fresh-owner lemma and exact receipts](docs/SECONDARY_TEN_INTERNAL_CONSUMER_CHAINS.md).
Thirty-four local Lean declarations and exact chain/isometry controls pass.
The new written proof has an ACCEPT independent review, with preceding
blocks separated by columns even where their row ranges meet. The earlier packed
batch theorem and reflected complete-exclusion/classification both now
have separate ACCEPT written reviews.

Latest batch checkpoint: packed distinct-owner repairs admit a two-terminal
injection and a single-owner budget, with an exact signed exterior remainder.
The reflected shared-consumer family has a full breadth classification:
small breadths overlap, breadth16 has no complete extension, and every
actual complete extension with breadth>=18 has selected-subinventory excess
h-3>=15. Twenty-seven new scoped Lean declarations and full-source controls
pass. See the [batch budget](docs/SECONDARY_TEN_BATCH_TERMINAL_BUDGET.md) and
[complete exclusion and reflected-pair compensation](docs/SECONDARY_TEN_OPPOSING_BATCH_COMPLETE_EXCLUSION.md).
Universal packing and complete-model exterior control remain open.

Latest residual checkpoint: the all-actual-consumer local compensation
theorem for the two prescribed residual families has an ACCEPT written
review. A new complete-extension exclusion removes the depth-eight
upper-left U branch and strengthens distinct-owner baseline excess from1
to3. Ten additional local Lean declarations and explicit collision controls
pass; the exclusion and stronger bound also have an ACCEPT written review.
See the [exclusion proof and scope](docs/SECONDARY_TEN_DEPTH_EIGHT_COMPLETE_EXCLUSION.md).
Global owner-budget nonreuse and exterior signed contacts remain open.

21 October research checkpoint: a complete nine-source family refutes
least-marked-hull reserve comparison even when BOTH endpoint graphs are
connected. The hull has R=k/2+13 and the full extension has R=24, with
fixed added negative mass17 and unchanged actual demand N1G2. The full
margin remains23, so unrestricted allocation and grid equality stay OPEN.
See the [construction, general insertion proof and exact signed loss](docs/DEMAND_HULL_RESERVE_COMPARISON_OBSTRUCTION.md).
The [shared-source separator theorem](docs/SOURCE_SEPARATOR_SIGNED_TRANSFER.md)
also now states its inherited R>=0 dependency and exact deletion criterion;
its initial independent REVISE verdict and subsequent corrections are tracked.

[![Verification](https://github.com/the-omega-institute/subquorum-colorings/actions/workflows/verify.yml/badge.svg)](https://github.com/the-omega-institute/subquorum-colorings/actions/workflows/verify.yml)

Research sources and reproducibility materials for **From hypercubes to grids:
sub-quorum colorings and structural bounds**, with contributions by Wenlin
Zhang (National University of Singapore; The Omega Institute) and Haobo Ma
(ChronoAI Pte Ltd; The Omega Institute).

**Start with the [current mathematical results](docs/GRID_RESULTS.md)**:
the profile proof of the known grid dissociation formula, directional matching bounds, and the
five-sixths estimate for mixed directions. This companion includes complete
proofs and extends the earlier manuscript, which covers the hypercube,
structural results and exact strip certificates.

The starting result resolves Conjecture 6.4 of Rafik Sahbi's
[Sub-quorum colorings of graphs, arXiv:2609.25128v1](https://arxiv.org/abs/2609.25128v1):
the sub-quorum coloring number of the n-dimensional hypercube is 2^(n-1)
for **every n >= 2**, with a dimension-independent Lean proof.

Starting from this solved family, the project advances two research directions:

1. **Rectangular grids:** use exact strip certificates and the boundary viewpoint
   to seek a proof of Sahbi's formula at arbitrary width and length.
2. **Structural characterization:** determine conditions for psi_sq=beta_2,
   using the signed boundary theorem as a sufficient mechanism and the grafted
   tree families as explicit obstructions.

The [research agenda](docs/RESEARCH.md) connects current results to the next
mathematical targets. The manuscript follows the same progression from the
hypercube solution to these geometric and structural questions.

## Results and verification

The [AA B-exit exclusion](docs/AA_B_SECOND_CORNER_AND_NEGATIVE_ONLY_ROUTE_BUDGET.md)
rules out the positive-corner occupied-band branch throughout the specified
saturated AA component. An actual incoming endpoint removes the two otherwise
surviving rotor roles; opposite incoming owners exclude a positive terminal,
and a stem/bar crossing excludes the remaining negative terminal. The AA
all-route census consequently has an exact negative-only form, without the
previous right-hand A=2. Ten further scoped Lean/axiom checks pass. This later
proof has its own pending review; it does not exclude all AA configurations.

The [D-interior two-corner enhancement](docs/BACKFILL_D_INTERIOR_TWO_CORNER_COMPENSATION.md)
exposes one additional typed singleton/activation per D-interior event, using
an enlarged complement in the SAME original negative pool. The joint all-route
inequality gains +d, with no reuse of cap fills, terminal activations or stops.
In the specified saturated AA residual, the incoming source also excludes the
positive second-corner branches of BOTH C and D, including recurring owners.
Sixteen scoped local Lean declarations and axiom checks pass. The D/AA written
extension has ACCEPT, as does the preceding complete
B/D+A/all-four-route theorem. Source/mark census control, complete
critical U10 realizability and the full allocation/grid equality remain open.

The [backfill corner routing theorem](docs/BACKFILL_CORNER_ROUTING_AND_SHALLOW_BARRIER.md)
classifies the original owner of a critical U10 backfill corner into four U
roles and excludes rotors. Complete bars force strict dimension drops:
incident height4 or6 requires the companion leg to exceed the root width
by at least2; when both widths are6, root incident height is at least12.
Phase01 exits enter the existing singleton pool without reusing old receiver
reservations; phase11 exits identify actual existing cap occurrences.
Twenty-three scoped local Lean/axiom checks pass. Complete U10 critical
witness coverage is zero; the general proof is geometric. Initial written
audit ACCEPT is joined by a separate ACCEPT for the height12 strengthening.
The [later two-corner compensation lemma](docs/BACKFILL_TWO_CORNER_COMPENSATION.md)
uses the second phase01-exit corner as either another negative singleton
reservation or a positive terminal activation separate from all cap fillers.
Its exact single-pool identity retains2KC in2R with the signed source
census and remaining defects; it does not assert R>=KC unconditionally.
Its later shared-stop extension reserves positive cap/backfill activations
beside the existing passive-corner, ordinary and critical stops in ONE
H/Z0 ledger. Six further scoped Lean/axiom checks pass; written two-corner
review is live and excludes that later shared-stop extension.
Full coefficient-one allocation and grid equality remain open.

The [critical return theorem](docs/CRITICAL_PHASE01_BAR_RETURNS.md) replaces
blanket freshness with two original bar slots per phase01 owner, attained
by a complete seven-source family with two returns into ONE closed owner.
The [ALL-critical separation proof](docs/ALL_CRITICAL_REGULAR_RECEIVER_SEPARATION.md)
then excludes every critical point from every first/LONG receiving tile,
using complete U/rotor ownership beyond endpoint tags. External exits and
closed full-bar returns now have an exact joint endpoint ledger with one
shared H pool. Nineteen new scoped Lean/axiom checks pass;112 complete
images include216 critical returns and104 two-return owners. The general
family has a written source/row-table proof and independent ACCEPT.
The later ALL-critical theorem's separate audit is live.
Original full tiles are not fresh reserve; unrestricted allocation remains open.

The [all-first/LONG receiver theorem](docs/FULL_FIRST_AND_LONG_RECEIVER_INJECTION.md)
now has independent written-proof ACCEPT: distinct physical receivers, including
full ones, give an exact joint endpoint count and share the existing H pool.
The [new complete critical obstruction](docs/CRITICAL_CLOSED_OWNER_COUNTEREXAMPLE.md)
shows why its LONG restriction matters. Six original U sources in a 20 by 30
grid place a critical second point in a closed phase01 owner's original full
bar. Six concrete Lean declarations and eight partition-preserving Python
images pass. This refutes blanket critical closed-owner exclusion; it is not
a coefficient-one counterexample, and unrestricted allocation/grid equality
remain open. The new fixture was not in the preceding independent audit.

The [phase10 descent and complete full-pair exit](docs/NEUTRAL_PHASE10_DESCENT_AND_FULL_PAIR_EXIT.md)
classify a phase10 owner of a neutral01 forced endpoint as a terminal with
incident height at least four shorter than the active leg. A dimension-independent
Lean role proof excludes this branch at active height four or six. A complete
three-source family attains the four-step gap and has full forced receivers
whose forced point lies outside the U-only singleton reservation pool. Thus the
unconditional full-receiver-to-singleton-slot rule fails. Six new scoped Lean
checks and384complete images pass, including96full forced receivers; the fixed
18x18 witness has78frozen endpoints and positive source/ambient slack. Complete
closed01 and AA coverage remain zero. The local descent is not a global mixed
chain termination rule, and full allocation/grid equality remain open.

The [closed neutral receiver theorem](docs/CLOSED_NEUTRAL_RECEIVER_SEPARATION.md)
proves that closed phase01 contacts force distinct physical receiving tiles,
including full ones. Both opposite endpoints of each full receiver avoid all
closed phase01 owners and remain in the same full endpoint component. The exact
outside count is2*C01-Jc; the same-component AA specialization requires at least
eight distinct outside endpoint positions per closed curve. These positions may
share owners and do not become fresh reserve. Eleven scoped Lean declarations
and640complete controls pass; those controls have zero complete closed01-contact
coverage, recorded explicitly. The endpoint-disjoint four01 partial polygon has
four distinct receivers/eight prescribed positions but is infeasible. General
finite allocation and grid equality remain open. Its separate written-proof
review completed ACCEPT; closed-union scope is explicit and the general
open-component formula includes unused port incidences.

The [neutral-support injection and any-pair budget](docs/DISTINCT_NEUTRAL_SUPPORTS_AND_ANY_PAIR_BUDGET.md)
prove that distinct neutral phase01 contacts force distinct original endpoint
positions, even across different port components. Those endpoints avoid every
closed phase01 owner. Nonfull regular stops share one defect pool with passive
corner stops, giving B+J01<=2A+H. The cap reservation pool now includes endpoints
beside both exact original pair types, with an exact unused-slot identity to
prevent repeated payment. Eleven scoped Lean declarations and641 complete
feasible controls pass;97 images obtain a strictly stronger cap constraint.
The U-port turning theorem and this injection/budget extension each have a
separate independent ACCEPT review. The initial controls have zero AA/full
receiver coverage; the later phase10 family above supplies complete full exits.
General coefficient one and grid equality
remain open, with full receiver, rotor and open-path exits still unresolved.

The [charge-aware matching budget](docs/CHARGE_AWARE_COMPLETE_SOURCE_COEFFICIENT.md)
improves the complete-source coefficient from12/13 to14/15, and from17/18
to21/22 when no actual double-marked positive is exceptional. Original
negative matchings cost at least their original total charge G, giving
|M|>=9N+4e+G=10N+4e+R-mu. This counts every source once and reuses no
defect witness. Six new scoped Lean arithmetic declarations and source/
signed-budget controls pass; independent review accepts both deductions
under the stated complete-source ownership and ledger hypotheses.

The [bottom-owner lemma](docs/WIDTH_SIX_BOTTOM_OWNER_AND_WRAPPING_OBSTRUCTION.md)
forces a sixth original owner at every unpaid full-chain width-six double.
At clearance four/six it is a horizontal terminal; a universal all-image U
role proof is checked in Lean. Upward wrapping is locally possible, but
zero-defect saturation excludes it at clearance four, leaving a phase10
continuation. Six scoped Lean declarations and local role controls pass;
independent review accepts this structural argument, with a clarified
two-neighbor premise and explicit even-dimension phase dependencies.
These results do not settle the coupled
finite closure, unrestricted coefficient one or arbitrary-grid equality.

The [four-stem compensation theorem](docs/WIDTH_SIX_FOUR_STEM_COMPENSATION.md)
extends the all-reserve coefficient-one class to positive width-six U
sources with leg-height difference at most eight, leaving all negative
dimensions and phases unrestricted. A full unpaid incoming chain forces
two additional original U tips, hence four strictly ordered incident
heights and positive height difference at least ten. Their far legs
also impose an exact height-width budget; at positive gaps ten/twelve
the four incoming widths are at least(12,10,8,6).
The [transverse-gate theorem](docs/TRANSVERSE_GATE_COMPENSATION_AND_AA_EXCLUSION.md)
provides new distinct irregular-pair payments Y, proves
U0+H>=J+X+max(2z+r,Y), and excludes the short width-eight/ten branch
of the nonexceptional one-reserve AA obstruction. A maximum avoids
assuming non-reuse against the older irregular-pair witnesses.
Thirty new scoped Lean/axiom checks and local role/support controls
pass; complete physical coverage of the new branches is zero and
geometric adapters remain written. Independent review accepts the
four-stem core theorem; its later height-width additions are outside
that review. The repaired transverse theorem also passed independent review,
including its explicit dimension partition and four-stem dependency.
The remaining finite width-six closure and arbitrary grids
are open; no complete allocation counterexample is supplied.

The [positive bottom-owner obstruction](docs/POSITIVE_BOTTOM_OWNER_RESERVE_OBSTRUCTION.md)
works at arbitrary clearance: a positive owner of the forced bottom point
consumes both of its original exterior bar-end supports. Its two distinct
legs each supply an activation or an accepted exterior-chain occurrence.
Together with the original double's opposite activation this gives A+X>=3
and R>=2. Thus the R1 residual cannot close this point with any positive
source, including arbitrary one-mark positives. Five further scoped Lean
declarations and representative role/support controls pass; independent
review is pending. Closure through further negative owners remains open.

The [uniform complete-source coefficient](docs/COMPLETE_SOURCE_UNIFORM_COEFFICIENT.md)
improves five-sixths to12/13 for every permitted finite complete U/rotor
fusion, with arbitrary source counts, dimensions, phases and contacts.
When all positive dimensions are nonexceptional it improves to17/18.
The accepted residual loss e+floor(s/2) costs at least13 matching edges
per unit in aggregate, since exceptional doubles cost at least13 and
other single-activation doubles at least9. This is a general written
deduction with seven scoped Lean arithmetic checks; finite constructor
and budget controls supplement the proof. No arbitrary-grid decomposition
or coefficient-one theorem is claimed.

The [support-chain common-pool theorem](docs/SUPPORT_CHAIN_COMPENSATION_AND_RESIDUAL_SATURATION.md)
adds payments from broken phase11 terminal-gate chains J and unactivated
positive exterior chains X. Their original regular pairs cannot coincide
with any old irregular-pair witness, proving U0+H >= 2z+r+J+X and
sigma >= n0-e-floor((s-r-J-X)/2), with signed integer floor. Component
rounding strengthens this by floor(o/2) when o components have odd
residuals. Twelve scoped local Lean declarations/audits and769 physical
controls pass;65 images improve the earlier bound. Broken-gate L3 stops
after full caps have no complete fixture here; their propagation proof
is written. A failing nonexceptional R1 component must have every
original endpoint-containing phase11-U receiver full and no consumed exterior support on any
unactivated positive leg. Independent review accepts this written extension
under its stated dependencies; all seven checks on revision374c3b7 pass. The coupled
full-chain obstruction and unrestricted grid theorem remain open.

The [width-six interleaving theorem](docs/WIDTH_SIX_TWO_GATE_INTERLEAVING.md)
proves joint allocation at every reserve when all positive U sources have
width six and even leg-height difference at most four, with arbitrarily
many positives and unrestricted negative U/rotor dimensions and phases.
This improves the matching coefficient from five-sixths to one on this
complete-source class. A common pool pays zero-activation doubles with
two distinct defect slots and certain single-activation doubles with one:
H >= 2z+r and sigma >= n0-e-floor((s-r)/2). Tight longitudinal gates
provide exclusive witnesses, so no slot is reused. Seventeen scoped local
Lean declarations and individual axiom audits pass;771 physical images
include142 tight marked-side occurrences, while complete paid-single-double
and interleaving fixture coverage is zero. The general geometric adapters
remain written; independent review accepts the written extension under
its stated complete-source dependencies. The remaining
nonexceptional A+A candidate needs width-six height gaps at least six or
short width-eight/ten transverse gates. Unrestricted mixed allocation and
arbitrary-grid equality remain open.

The [two-slot compensation theorem](docs/TWO_SLOT_COMPENSATION_FOR_UNACTIVATED_DOUBLES.md)
pays every unactivated nonexceptional double-marked positive from distinct
actual defect slots, without sharing resources between sources or witness
types. If s doubles have exactly one activated terminal, e actual doubles
are exceptional, and n0 positives are unmarked, the source ledger gives
sigma >= n0-e-floor(s/2). Thus e+floor(s/2)<=n0 guarantees joint allocation
at every reserve value; in particular all nonexceptional sources with
s<=1 are covered. The first nonexceptional one-reserve failure now has
only the A+A census, with no nonfull defect tiles. Sixteen scoped Lean
declarations and664 physical controls pass; complete-image fixtures do not
exercise blank/single-activation branches, whose geometry remains written.
The two-slot written theorem has an independent ACCEPT review under its
stated catalogue and ledger dependencies. Unrestricted mixed
allocation and arbitrary-grid equality remain open.

The [short-leg defect injection](docs/SHORT_LEG_DEFECT_INJECTION.md) assigns
every nonexceptional doubly marked positive source a distinct activated
terminal occurrence or irregular-pair/mixed-triple defect tile. Original pair-corner ownership
and an eight-orientation exclusion prevent sharing a forced tile with a
blank-gate mark. The weighted consequence excludes fourteen of the seventeen
defect patterns in a one-reserve allocation failure, leaving three connected
alternatives. Eleven scoped Lean declarations and664 physical controls pass;
the full geometric adapters are written. Unrestricted joint allocation and
rectangular-grid triple equality remain open.

The [leaf-spliced network theorem](docs/LEAF_SPLICED_TWO_LEG_NETWORKS.md)
proves exact corrected-charge additivity for arbitrarily many differently
oriented two-leg modules joined at their tail ports. Positive modules cannot
be neighbors, so path receivers have charge at most one and cycle receivers
have nonpositive charge. Distinct physical unit guards pay all positive
networks, proving the coefficient-one bound on this explicit geometric class.
The three first-charge-five resource motifs are excluded in the class even
after valid reservations. An all-length frozen zigzag makes the path charge
bound sharp. The geometry has a written proof;17scoped Lean declarations
check path induction, splice arithmetic and the donor/reservation interfaces.
The unrestricted grid bound remains open.

The [strip incidence theorem and capacity-one obstruction](docs/STRIP_INCIDENCE_ALLOCATION_AND_CAPACITY_ONE_OBSTRUCTION.md)
replace the capacity-two threshold by an exact physical-slot criterion: a
chosen set of runs is payable precisely when it contains no whole tree
component of the horizontal/vertical incidence multigraph. The maximum
one-unit-per-run credit is the sum of min(vertices,edges) over components;
reserving additional distinct old credits cannot worsen the combined score.
A fully frozen 32-endpoint example has positive receiver charge, no donor
from any of the four corner rules, and every maximal run has capacity at most
one. It refutes universal corner-plus-capacity-two coverage while the exact
incidence allocation pays it. All 729 small capacity multigraphs, 23328 request
subsets, 2916 reservation steps and 96 physical cases pass. Forty-six local
Lean declarations verify the finite freezing and original charge/strip
obstruction; the general graph theorem has a written proof. Universal grid
coverage remains open.

The [sealed-strip compensation theorem](docs/SEALED_STRIP_OVERLAP_AND_GLOBAL_COMPENSATION.md)
handles overlapping horizontal and vertical maximal endpoint-free runs of any
length. Blank outer columns or rows force at least two units of actual strip
capacity. Since a physical tile belongs to at most two runs, every subset of
strips has enough distinct capacity slots to allocate one unit per strip.
Earlier credits are reserved first and eligibility uses residual capacity.
A fully frozen example makes the one-unit guarantee sharp: two strips share
the same capacity-two tile, so two units per strip would double-count it.
144 physical cases and six mixed-component controls pass; six local Lean
statements compile with explicit axiom audits. Enough-strip coverage for
arbitrary representatives and the unrestricted grid bound remain open.

The [remote-deficit frozen obstruction](docs/REMOTE_DEFICIT_FROZEN_OBSTRUCTION.md)
has charge one, yet every endpoint-free physical tile sharing an edge or corner
with its receiver has deficit zero. Its only positive resource is a blank tile
at tile distance two. The complete 28-step certificate and all eight physical
symmetries pass independent checks. Thus even all immediate neighboring tiles
cannot universally supply compensation; the global bound still holds here
with deficit one. A selected-border completion preserves the obstruction
with all endpoints in the interior; all eight images pass. No new Lean or
unchanged blank-padding invariance is claimed for it.

The [two-leg degree-three obstruction](docs/TWO_LEG_DEGREE_THREE_COVERAGE_OBSTRUCTION.md)
refutes three-rule corner coverage even when every endpoint has occupied
degree exactly three. A written proof covers all even bar widths at least six
and independently chosen even leg heights at least four: every member is
fully frozen, has corrected charge one and zero old-rule capacity. A new
degree-sensitive guard pays the charge without reuse. 39 parameter cases and
624 physical/padded images pass; two local Lean statements verify the local
guard and receiver arithmetic, with the full geometry and ownership written.
The previous 22-endpoint example also defeats unrestricted four-rule coverage;
four-rule coverage within occupied degree three and the grid target remain open.

The [three-rule coverage obstruction](docs/THREE_RULE_FROZEN_COVERAGE_OBSTRUCTION.md)
is fully frozen with charge one and no donor of any of the three local corner
types. Its22-step certificate and original corrected charge pass independent
checks in all physical and blank-padded symmetries. Thus the conditional
corner theorems remain valid, while universal coverage by these rules is false.
Global compensation needs resources or normalization beyond these corners.

The [frozen corner-coverage obstruction and repair](docs/CORNER_FREE_FROZEN_RECEIVER_AND_ENDPOINT_GUARDS.md)
has occupied degree exactly three, charge one, and no capped or selected-guarded
donor in any direction. An explicit20-step freezing proof excludes every mixed
bundle. A new same-component two-endpoint guard pays the missing unit; its
local lemma and compatibility with both old ownership rules extend the weighted
criterion without donor reuse. The finite graph/charge proof and local guard
lemma pass35new local Lean declarations. The separate22endpoint example
refutes general three-rule coverage; the newer two-leg family also refutes
its occupied-degree-three restriction.

The [charge-two frozen receiver](docs/CHARGE_TWO_FROZEN_RECEIVER.md) refutes
the proposed universal receiver ceiling rho_H<=1. Its complete 14-by-10
physical configuration has 38 endpoints; an explicit acyclic certificate
excludes all mixed-direction promotion bundles. Original corrected charges
and all eight physical symmetries pass independent checks. Four distinct
owned donor tiles are present, and two unit deficits pay its charge without
reuse. The note extends the old owned-witness criterion to multiple donor
tiles per component; universal weighted coverage and the grid target remain open.

The [straight-chamber network reduction](docs/DEGREE_THREE_CHAMBER_NETWORKS.md)
handles arbitrary terminal endpoint geometry of maximum endpoint degree three.
Its P-face chambers are straight ladders joined by straight paths; when
occupied degree is exactly three and bundles are impossible, long chambers
have exactly two forced matching exits. General face turns can be localized
at degree-four P vertices. The proof and finite controls are separate from
the refuted universal receiver ceiling. A [punctured-receiver family](docs/PUNCTURED_RECEIVER_EULER_OBSTRUCTION.md)
also disproves an uncorrected Euler charge bound under single terminality;
explicit color bundles exclude the fully frozen hypothesis.

The [frozen rail extension theorem](docs/FROZEN_RAIL_ELBOW_EXTENSIONS.md)
adds arbitrary even occupied rails to thick elbows. Two anchored freezing
waves show that no endpoint-promotion bundle can extract the original elbow;
positive examples retain whole charge one. Each added rail nevertheless has
exact charge t-ell-2epsilon<=0, so the old owned corner pays the enlarged
receiver without reusing a donor or counting the rail loss twice. This
extends the explicit coefficient-one class and obstructs a generalization
of stepped-core isolation, while leaving arbitrary grid configurations open.
The repaired written proof has independent ACCEPT; 141 scoped local Lean
declarations and the physical controls have separate passing receipts.

The [stepped-patch isolation theorem](docs/STEPPED_PATCH_ISOLATION.md) removes
the completeness assumption from prescribed arbitrary-length stepped cores.
At most one single promotion per core isolates them, preserving the objective
and their frozen certificates. If all other initial endpoints are square-free,
distinct guarded unit donors give coefficient one with an exact deficit
decomposition. The all-length boundary and multi-core proof is written;
137 scoped Lean declarations pass, including four matching/path/port interfaces.
The [phase and channel note](docs/STEPPED_ARM_PHASE_AND_CHANNELS.md) separately
proves sharp two-direction phase bounds and a translated all-length obstruction
to paying every negative phase from the component's negative charge alone.
Neither note proves the universal grid inequality; their new written assessments
are outstanding while Oracle's task quota is occupied.

The [whole-channel compensation theorem](docs/COMB_CHANNEL_COMPENSATION.md)
allows a remote terminal band to contain matching endpoints. Its exact
boundary payment is two for aligned comb ends and one for unequal heights,
plus actual source phase and signed complete-comb end flux. Pointwise
residual capacity combines it with the original mouth ledger without donor
reuse. Uniform zero-mouth families include an occupied terminal comb and
a contained perpendicular source; actual source phase repairs an otherwise
invalid weight-two allocation. There are 194 physical controls, eight
symmetry images and three additional conditional Lean statements, with
123 scoped declarations audited cumulatively. General channel existence
and unrestricted grid equality remain open. Its independent written review
completed ACCEPT; physical and Lean execution have separate receipts.

| Result | Scope | Verification |
| --- | --- | --- |
| Hypercube coloring number | All dimensions n >= 2 | Lean 4, pinned Mathlib; original modules from trureturing |
| Boundary matching | Feasible (T,M) in graphs with signed adjacency S^2=dI, d>=2 | Written energy estimate and Hall argument |
| Bipartite signed graphs and Cartesian products | All graphs satisfying the stated hypotheses | Written proof and exact matrix controls |
| Exact grafting theorem | Every finite nonempty base graph F | Written proof; tree-DP cross-checks |
| Unbounded gap on subcubic trees | R(P_k), every k>=1; gap floor(k/3) | Written proof; checks k=1..30 |
| Rectangular grid formula | Widths 8,9,10,11 at every positive length | Exact full-vector certificates, independently recomputed |
| Known grid dissociation number beta_2=F | Every positive width and length | New row-profile proof with equality information; exact finite checks |
| Directional Omega_H=Omega_V=F | Every positive width and length | Written ladder-rigidity argument; exact finite checks |
| Mixed matching bound with coefficient 5/6 | Every positive even-by-even rectangle | Written residual-geometry proof; exhaustive and constructed controls |
| Mixed matching bound with coefficient 1 | Even-by-even grids whose endpoint components are thin, have at most one P-square, or are prescribed positive bent caps with their forced matching/supports | General thin classification, all-alignment receiver budgets and injective no-P donor compensation; scoped Lean interfaces and exact controls |
| Attached stepped cores with coefficient 1 | Prescribed positive-phase stepped matchings/supports; all other initial endpoints square-free; no initial completeness or terminality | All-length intrinsic boundary, sequential isolation and exact distinct-donor proof; physical controls and four scoped Lean interfaces |

The Lean theorem explicitly states psi_sq(Q_n)=2^(n-1). The beta_2 identity
was already established by Sahbi and also follows from the written proof;
beta_2 is not defined in the archived Lean module. The subsequent structural
and full-grid results are not yet Lean formalized. The conditional band and
endpoint compensation lemmas below now have Lean proofs; the unrestricted
mixed-direction grid coloring formula remains open.

The [thin-component theorem](docs/THIN_COMPONENT_CLASSIFICATION_AND_BOUND.md)
classifies every bundle-terminal component contained in two rows or columns,
including arbitrary odd tails and optional degree-four supports. Whole receivers
are nonpositive in every alignment. The
[bent-source compensation theorem](docs/POSITIVE_BENT_RECEIVERS_AND_SPARSE_COMPENSATION.md)
then handles an all-width three-row family whose complete receiver has charge
positive one: terminality makes its canonical donor a no-P tile, and eight
explicit relative-orientation witnesses prove donor injectivity. The exact
aggregate formula spends each tile once; width-four bent sources supply one
strict deficit unit. Both are written general proofs with precisely scoped
Lean support. Their independent reviews are tracked separately from the
previous accepted one-square theorem. Arbitrary multi-square source coverage
and the universal coefficient-one bound remain open.

The [long-arm occupied-mouth theorem](docs/TRANSVERSE_COMBS_AND_OCCUPIED_MOUTH_COMPENSATION.md)
allows any number of prescribed complete perpendicular combs to cross a
positive long source's terminal mouth. Distinct actual no-P tiles pay at
least two units per mouth, giving |T|+|M|<=mn/2-B in the covered class.
The corrected long-arm proof and this extension have a completed independent
ACCEPT. A fully frozen two-ending-comb fixture instead makes that mouth
payment zero, refuting the unrestricted mouth-only rule, not the grid target.

The [exact comb-end ledger](docs/COMB_END_DEBT_AND_EXACT_MOUTH_LEDGER.md)
now allows prescribed complete combs to start or stop within mouths. Each
mouth has no-P deficit D=2-S+A, with S the number of sparse end tiles and A
a nonnegative integer shifted-square slack. Each complete comb owns at most
one sparse end, even across several mouths. Hence the broader covered class
satisfies |T|+|M|<=mn/2-B+S_total, giving coefficient one when S_total<=B.
There is a general written proof and 696 optimized controls; this later
extension is outside the previous ACCEPT and has no new Lean claim.
Its own exact-debt written-proof review subsequently completed ACCEPT;
the later closed-network theorem below is reviewed separately.

The [two-tiling end-flux theorem](docs/COMB_END_FLUX_AND_CLOSED_CONTACT_NETWORKS.md)
identifies the saturated-end payment hidden in that slack: D=2-S+U+D',
where D'>=0 is an auxiliary shifted no-P count. Internal complete-comb
connections cancel, leaving only unmatched sparse/saturated ends O,J on the
boundary of the mouth collection. The covered initial class satisfies
|T|+|M|<=mn/2-B+O-J; if every sparse contact has its opposite saturated end
in a mouth, the strict mn/2-B bound holds regardless of the number of internal
connections. General proofs, 696 contact/138 bridge controls and 85 scoped
local Lean declarations are available; unmatched exterior compensation and
the universal grid bound remain open.

The [directional averaging theorem](docs/DIRECTIONAL_AVERAGING_SOURCE_COMPENSATION.md)
removes all crossing restrictions for prescribed source-only mouths, and
more generally for nonnegative multiplicity-weighted comb flux. The
[adaptive strip certificate](docs/ADAPTIVE_STRIP_COMPENSATION_AND_NEGATIVE_FLUX.md)
now permits negative flux: choose a maximum-weight independent collection
of coalesced strips, using a classical bipartite cut. Original donor tiles
are used once. An explicit all-k family has 3k sources, flux -k and an
exclusive certificate of weight 3k, beyond the earlier nonnegative-flux
and exact crossing-loss criteria. General negative-flux compensation is
still open. There are 70 physical controls, 32 symmetry images, 1,024
abstract graph controls and 100 scoped local Lean declarations; the
geometric adapter and all-k proof remain written.

The [capacity-aware extension](docs/CAPACITY_AWARE_STRIP_COMPENSATION.md)
permits overlapping selected strips, deducting at most two units per shared
physical tile. An all-even-width family has eight sources, flux -4 and
exclusive weight only six, but a capped certificate of eight, strengthened
to nine by a retained support. The
[remote-rung theorem](docs/REMOTE_COMB_RUNG_COMPENSATION.md) then pays negative
flux from distant endpoint-free physical strips, including unequal comb
lengths and the existing zero-mouth-payment locality examples. It includes
the integral consequence F>=-1 implies coefficient one in the retained
class. There are 45 capacity-aware and 54 remote physical controls, with
106 scoped local Lean declarations. The first exclusive-note review found
a chamber-distance proof gap, now repaired with actual support formulas;
its follow-up completed ACCEPT; the separate new-mechanism review is pending. General
existence of sufficient distant capacity and arbitrary bent-source coverage
remain open; these are written geometric theorems with scoped formal support.

The [whole-cavity theorem](docs/CLOSED_SOURCE_CAVITY_COMPENSATION.md) pays
even when a negative-comb pair's saturated-tip rung is occupied. Complete
comb exits contribute an [exact signed boundary flux](docs/CAVITY_BOUNDARY_FLUX_AND_COMPENSATION.md).
The [mixed-direction extension](docs/MIXED_DIRECTION_CAVITY_COMPENSATION.md)
proves that every fully enclosed perpendicular positive source has phase
gain at least two, sharply, by pairing its chamber-flank sites. Enclosed
source orientations are therefore unrestricted. Actual physical donor
incidence controls overlap between cavities; shifted squares are counting
devices only. The new extension has 69 physical controls, eight symmetry
images and 117 scoped local Lean declarations in the cumulative audit.
Full geometry remains written; adequate cavity coverage and the universal
grid theorem remain open. The earlier cavity
review returned REVISE; its wording and proof-detail corrections are
[recorded explicitly](docs/reviews/2026-10-19-closed-cavity-assessment.md).

That repaired complete-source theorem has now received
[independent ACCEPT](docs/reviews/2026-10-19-mixed-cavity-assessment.md).
The later [open-source cavity extension](docs/OPEN_SOURCE_CAVITY_COMPENSATION.md)
also permits prescribed sources to escape the cavity: all their raw phase
contributions are nonnegative, with parallel contacts counted by actual
tip membership. A sharp all-a family has a partial sources in one cavity
but physical deficit exactly two. It disproves crediting two units per
touching source, with unbounded overclaim, while staying inside the proved
source-only global class. The new extension has separate controls and
review; neither ACCEPT nor a universal grid conclusion is inherited.

The [pressured-collar theorem](docs/PRESSURED_COLLAR_COMPENSATION.md) extends
straight shared receivers to arbitrary bent paths and branching tile trees
under explicit occupied-face and blank-cap assumptions. Each distinct leaf
contributes one unit of charge compensation, with the complete boundary
parity correction and a single-use aggregate source budget. Six standalone
Lean declarations and physical matching controls cover the local/counting
interfaces; arbitrary overlapping or thick receivers remain open.

The [attachment-corrected extension](docs/ATTACHMENT_CORRECTED_COLLAR_COMPENSATION.md)
removes pressure on all unmarked tiles and allows thick regions. Its exact
ledger retains internal saturated attachments as debt and corrects parity
for incoming saturated endpoints. Zero internal debt and zero saturated
export suffice for arbitrary receiver geometry. A connected arbitrary-length
bent path shows that internal debt cannot be paid merely by route length.
Four additional Lean declarations pass; arbitrary internal-debt compensation
and overlapping ownership remain open. The original pressured theorem now
has an independent ACCEPT; this later extension is reviewed separately.

The [square-free endpoint and owned-donor theorem](docs/SQUARE_FREE_ENDPOINTS_AND_OWNED_DONORS.md)
classifies single-terminal endpoint graphs without an all-P unit square:
their components are straight even paths with alternating selected supports,
and every endpoint freezes. A separate allocation theorem uses actual matching
endpoints to assign half-payments from tiles with at most two occupied vertices,
including a physical two-source patch sharing a two-endpoint donor. Anchored
diamond donors are automatically exclusive when their central cores are disjoint.
Seven new standalone Lean declarations pass; the full graph classification
and geometric allocation have written proofs. General coverage remains open.

The [exact promotion-core and frozen-obstacle note](docs/PROMOTION_CORES_AND_ANCHORED_OBSTRUCTIONS.md)
gives a greatest fixed-side promotion core and an8-by8obstacle excluding every
oriented bundle while retaining positive central charge. Its earlier core/frozen
package received an independent ACCEPT and full CI; the later donor geometry,
tight completion and newest classification are reviewed separately.

The [whole-component receiver theorem](docs/COMPONENT_RECEIVERS_AND_SQUARE_FREE_BOUND.md)
upgrades the mixed-matching coefficient to one whenever the initial endpoint
graph has no all-P unit square, allowing both matching directions and arbitrary
tile alignment. Single promotions reach straight combs. In a terminal pair,
each tile has only one endpoint-component owner; saturated corrections stay
inside its complete receiver, and every comb receiver has exact charge zero.
The remaining no-P tiles give the full deficit. Pure rectangular endpoint
components also reduce into this class; each prescribed aligned capped
component gives an additional strict unit of deficit. Four new scoped Lean
statements and 24,296 finite configurations support the written proof, with
65 declarations passing the combined local audit. Full component partition,
normalization and all-length geometry remain written. General square-bearing
component coverage and the unrestricted grid theorem remain open.

The [all-alignment one-square extension](docs/ALL_ALIGNMENT_SINGLE_SQUARE_BOUND.md)
also permits a P-square and four straight arms in each component, with arbitrary
alignment. Extending an arm by two adds one receiver tile, one selected vertex
and two endpoints, so its charge is unchanged. Explicit parity base shapes
give only zero or negative receiver charges in every phase. Hence coefficient
one holds whenever every initial endpoint component contains at most one
P-square, allowing branches and both matching directions. An exact deficit
identity and a frozen equality example accompany the proof. New controls cover
2,380 family cases and 22,217 small qualifying pairs; the general geometric
extension remains written rather than a new Lean theorem.

The [complete bipartite promotion theorem](docs/BIPARTITE_PROMOTION_COMPLETENESS.md)
now proves the converse to the frozen certificate. In every finite bipartite
graph, the closure is exactly the universally unpromotable endpoint set;
each color's entire unfrozen complement is a feasible greatest one-color
bundle. Empty cores on both sides therefore exclude arbitrary mixed bundles.
The graph-level equivalences and an unbounded freezing induction are checked
in ten new Lean statements, with 61 declarations passing the combined audit.
Independent controls exhaust all 512 labeled three-by-three bipartite graphs,
55,924 feasible configurations and 169,048 oriented choices. This decides
promotion existence, not an optimal global mixed bundle or the grid bound.

The [frozen capacity-two cross](docs/FROZEN_CAPACITY_TWO_CROSS.md) treats a
terminal square component with four pendant matching branches. Its four
side tiles are forced half-donors with exclusive matching ownership, giving
charge-2 without assuming disjoint nine-tile collars. An all-size connected
family attains this budget. These geometric proofs and physical controls
are outside the current classification review and full Lean geometry.

The [odd-arm transport theorem](docs/ODD_ARM_COMPENSATION.md) removes the
fixed selected anchors for single-terminal components containing exactly one
aligned P-square whose four corners are matched outward. Such a component is
necessarily a pinwheel of four odd straight arms. Intermediate arm tiles are
neutral and four terminal half-donors pay exactly two units at arbitrary
distance; receivers from distinct components are automatically disjoint.
This disproves adjacent-only payment under these weaker hypotheses while
preserving the enlarged receiver inequality. The general proof,271physical
cases/2168symmetry images and32scoped Lean declarations pass. Source coverage
and multi-square components remain open. Reviewd3705dc5 ended with no assistant
output, hence no mathematical verdict; the new transport was outside its input.

The [complete single-square classification](docs/SINGLE_SQUARE_PARITY_AND_ALIGNMENT.md)
removes the four-outward-mates restriction. Seven central matching patterns
force zero, two adjacent, or four odd arms. The all-even case has a feasible
central two-point promotion; the other cases freeze and aligned receivers
pay one or two units exactly. A second alignment phase gives neutral frozen
receivers at every odd arm length. A fully neutral8-by8completion disproves
alignment-free strict payment even with arbitrary exterior resources, attaining
the target inequality with equality. The general proof,1806cases/14448images,
41scoped Lean declarations and exact seven-theorem finite obstacle certificate
pass. A6-by6component with two overlapping P-squares freezes in three rounds
but pays only one unit, with saturated attachments neutralizing the two-P
core tile. This excludes independent square-by-square payments. Independent
written-proof reviews122da19b andfc9e74ce completed REVISE: corrected
capacity and the later neutral-family/fixture calculations are confirmed;
the fixture refutes a broad payment rule, not removal of uniqueness while
retaining four outward mates. All requested scope clarifications are applied;
no overall ACCEPT is inferred.
Multi-square geometry and source coverage remain open.

The [exact ladder guard criterion](docs/FOUR_GUARD_LADDER_REDUCTION.md)
now treats genuine multi-square strips. In a full-P two-row strip of width
at least four whose strict interior is closed under matching, promoting
one interior grid color is feasible exactly when its two opposite-color
boundary guards are blank. The move preserves the objective and removes all
strip squares, for arbitrary mixed matching directions and exterior labels.
Four straight nonempty corner arms with outward corner mates force those
guards blank, so this entire long-core class reduces to square-free paths.
A bundle-terminal strip with closed interior instead needs at least two
occupied guards, one of each color. This is a necessary obstruction, not a
sufficient terminality test. Width three is sharply exceptional. The general
written proof, independent physical controls and scoped arbitrary-width Lean
neighbor geometry are included; this later result was outside both reviews.

The [pure two-row component theorem](docs/PURE_TWO_ROW_COMPONENT_REDUCTION.md)
now removes the blank-guard and interior-closure hypotheses altogether when
the entire endpoint component is a full two-row rectangle. For every width
at least two and arbitrary mixed matching, a constructive switch of grid
color leaves at most one matching edge and preserves the objective. No
single-terminality or alignment assumption is needed. Matching blocks and
an arbitrary-length blank-switch argument give the general proof;1211616
complete small cases and larger controls verify its implementation. A
three-column example proves that one remaining edge can be necessary.

The [mixed-color and ownership follow-up](docs/MIXED_COLOR_LADDERS_AND_CONTACT_OWNERSHIP.md)
also gives an all-length family in which every square-removing bundle must
use both colors. Its complete feasible-bundle family consists of independent
left prefixes and right suffixes, with exactly(k+1)(l+1)-1nonempty choices
and a unique square-removing maximum. Compatible edge-disjoint bundles
compose safely; endpoint components factor exactly. Occupied contacts of
distinct components have unique vertex ownership, but a checked pair of
fully frozen components has two contacts in one zero-charge saturated tile.
Thus vertex exclusivity alone does not supply tile compensation. The full
graph-level proofs, finite controls and scoped Lean interfaces are separate.
Its independent written-proof review completed ACCEPT; requested local-scope
and ledger clarifications are incorporated, without claiming execution review.

The [frozen capped-ladder family](docs/FROZEN_TWO_ROW_CAPPED_LADDERS.md)
shows exactly why the pure-rectangle theorem cannot extend to every endpoint
component contained in two rows. For every width w>=3, two horizontal caps
freeze the entire component by acyclic retained-mate waves. There are w-1
endpoint squares but the complete endpoint-tile receiver has charge exactly
-1 at every width. Even arbitrarily many aligned P-squares therefore do not
provide a proportional compensation budget. The smallest displayed instance
has eight endpoints; every one of its 80 nonempty orientations fails. The
general proof, 62 family cases and 496 symmetry images are supplied. This
refutes the shape-extension and per-square payment rules, not the global target.

The [long-corridor follow-up](docs/RESIDUAL_CORRIDORS.md) constructs fork-free
positive residual components of arbitrary length and proves an objective-preserving
replacement when the adjacent band is blank. It also records a bounded search
for simple all-capacity-one paths without internal matching edges.

The [boundary-aware compensation note](docs/CROSS_COMPONENT_COMPENSATION.md)
proves a filled-corridor adjacent-band inequality, including occupied bands and
capacity-two passages. An explicit family shows why outward attachments to
saturated tiles require a boundary correction. Its written proof, sharp examples
and coordinate verifier are separate from the current joint manuscript.

The [compensation transport follow-up](docs/COMPENSATION_TRANSPORT.md) proves a
neutral-band propagation lemma and constructs fork-free equality configurations
whose compensating component lies arbitrarily far from the positive component.
It excludes fixed-radius charging of the initial negative residual contributions.

The [pressure-band follow-up](docs/PRESSURE_BAND_BRANCHING.md) proves that every
tile of a band under the specified full-P entrance has nonpositive charge,
giving the sharp aggregate bound rho(S)<=min(0,-1+sigma/2). A feasible infinite
family has arbitrarily many outgoing saturated attachments despite every band
tile being neutral. Thus general neutral bands need an allocation rule beyond
the two-exit transport case; shared terminal ownership remains open.

The [mixed-neutral donor note](docs/MIXED_NEUTRAL_DONORS.md) proves that a single
tile between the specified receiving caps supplies one unit without a P
pressure row, and extends the interval forest to such mixed terminal leaves.
It accounts for the 6-by-14 obstacle. A new feasible 6-by-20 configuration has
a closed two-tile successor of zero charge and negative components outside
that interval, identifying the next obstacle to interval-only allocation.

The [guarded half-donor note](docs/GUARDED_HALF_DONORS.md) proves sharp
half-unit compensation in same-direction gaps with two explicit guards,
and unique geometric certificates for full and half donors. Two feasible
6-by-6 witnesses show why those guards matter. The 6-by-20 outside donors
now have certificates; multiple-source allocation requires the stated
weighted Hall condition and remainder control.

The [same-direction capacity note](docs/SAME_DIRECTION_CAPACITY_DONORS.md)
removes the entry guards when the receiving tile has positive residual
capacity: the cap geometry proves `d<=r`, giving budget `r/2`. Sharp
half-unit and capacity-two witnesses accompany a complete zero-charge
classification. A deficient gap can still have zero capacity and zero charge;
such neutral relays cannot be assigned a donor budget.

The [neutral-relay obstacle](docs/NEUTRAL_RELAY_OBSTACLE.md) gives an 8-by-8
full-grid completion containing this relay with every tile charge zero.
Thus the relay alone forces no negative band or component; a transfer theorem
must use additional positive-source or routing hypotheses.

The [diagonal-relay normalization](docs/DIAGONAL_RELAY_NORMALIZATION.md)
removes neutral relays by promoting their diagonal P endpoints and deleting
the matching attachments. It preserves the objective, every tile charge and
all nonzero residual components. In the normalized pair, every deficient
same-direction capped gap supplies at least a half-unit; the remaining zero
gaps are saturated. Cap certificates must be checked after the move.

The [neutral-attachment normalization](docs/NEUTRAL_ATTACHMENT_NORMALIZATION.md)
extends this move to adjacent occupied corners and three-P neutral tiles.
An attachment endpoint can be promoted exactly when it has at most two occupied
neighbors. All tile charges and residual edges and capacities remain fixed;
the complete normalization is independent of processing order. In a normalized
neutral pressure band every surviving exit is in a three-P tile and has an
occupied lateral blocker. The 8-by-8 all-neutral example becomes fully saturated.
This is a reduction of the remaining cases, not a proof of general compensation.

The [mixed-successor boundary-debt note](docs/MIXED_BAND_BOUNDARY_DEBT.md)
constructs an arbitrary-length normalized equality family, also with
capacity-two passages, whose whole successor has charge `b/2-1` despite no
outward saturated attachment. Residual exports carry compensation outside
that region. Using the established all-length width-six Omega theorem, the
note proves the corrected local bound `rho(C)<=-1+beta/2+tau`, with sharp
residual-export coefficient one-half. Tile-disjoint patches and shared donor
capacities give a precise conditional global ledger; arbitrary bent geometry
and universal allocation remain open. Coordinate and boundary-role controls
are separate from the preserved journal manuscript.

The [exterior-component follow-up](docs/EXTERIOR_COMPONENT_BUDGETS.md)
computes the exact half-port budget from capacity-zero/two tiles and cycle
rank. It proves single-use compensation when actual exterior components
meet the stated balance condition, including bent trees and shared receivers.
Arbitrarily long bent two-port paths and a parallel-edge cycle show why
length, raw capacity and route visits alone do not certify a donor. A second
local corollary closes an eight- or ten-row source envelope using existing
all-length strip theorems, even when the component condition is unavailable.

The [cycle-pruning and parity note](docs/RESIDUAL_CYCLE_PRUNING.md)
proves automatic half-unit compensation for any one-port region without
positive zero-capacity leaves, allowing arbitrary bends and cycles. An
alternating-circuit cancellation preserves occupation, objective, every tile
charge and all boundary matching, including circuits visiting a capacity-two
tile twice. After pruning, every remaining simple residual cycle has at least
two diagonal capacity-two passages. An explicit irreducible cycle attains
that count and still supplies negative compensation; a positive one-port
leaf example shows why the parity lemma needs its leaf hypothesis.

The grid extension uses Sahbi's Omega reduction and max-plus method. Huang's
signed hypercube matrix is the key input to the hypercube proof. Tree-result
priority is still to be compared with the earlier caterpillar work cited
by Sahbi; the draft makes no historical priority claim about that work.

The guarded-donor controls also classify the remaining width-one same-direction
obstruction: an unguarded R,R middle state is necessarily `PP/BT` or `TB/BT`,
both of charge zero (with the reflected L,L states `PP/TB` and `BT/TB`). Any
further compensation argument must therefore use a wider interval, a bend, or
residual routing rather than another one-tile local bound.

The [proper-interval Hall note](docs/PROPER_INTERVAL_HALL.md) gives a
conditional reduction for bent compensation: when source donor windows have
strictly ordered endpoints, all weighted Hall checks reduce to consecutive
source blocks. The properness hypothesis excludes nested or returning windows;
the accompanying finite control records both the reduction and a shortest
non-proper counterexample.

The [interval-deficiency note](docs/INTERVAL_HALL_DEFICIENCY.md) removes that
properness restriction at the allocation level. For arbitrary nested or
repeated interval windows, Hall is equivalent to checking every donor interval
`J` against the number of source windows contained in `J`. A disjoint-interval
dynamic program computes the exact shortage `delta`; the ledger then gives
`q <= delta + rho(W)`, while `delta=0` recovers coefficient one. The control
compares exhaustive subsets, the dynamic program, and doubled-capacity max-flow.

The [attachment-aware note](docs/ATTACHMENT_AWARE_COMPENSATION.md) applies the
same ledger to occupied bands with outward saturated attachments. It treats
`sigma/2` as an explicit half-integral debt and requires a shared-capacity Hall
allocation of certified negative donor regions. Its exact flow control includes
the minimal shared-donor obstruction, so receiving saturated tiles are never
counted as compensators or reused across components. When the incidence Hall
condition fails, the same note records the exact attachment deficiency
`delta_att` and the audited fallback `q <= delta_att + rho(W)`.

## Contents

- `manuscript/paper.tex`: research draft, proofs and tree recurrence appendix.
- `docs/GRID_RESULTS.md`: current grid results and links to their complete proofs.
- `develop/`: two exact C++ transfer implementations, independent small controls,
  tree recurrence, and mathematical notes.
- `develop/results/`: full integer state vectors, finite readouts and hashes.
- `formal/`: standalone Lean package with the original two proof modules.
- `docs/REPRODUCE.md`: build and verification instructions.
- `docs/RELEASING.md`: verification, version tags and Zenodo connection.

See [releases](https://github.com/the-omega-institute/subquorum-colorings/releases)
for the PDF and source/reproduction archives. CI recomputes certificate endpoints
from the empty state, runs finite controls, builds the paper, and checks Lean.

## Attribution and license

This repository is an Omega Institute research artifact. Sahbi is credited for
the source problems and methods; this deposit does not assign him authorship
of the current draft. The manuscript author list is provisional.
AI assistance included mathematical exploration, code development, cross-checking
and drafting, as described in the manuscript.

Original material and the imported trureturing modules are distributed under
Apache-2.0; see `LICENSE` and `NOTICE`. External dependencies retain their
upstream licenses. Cite `CITATION.cff`; a DOI will be added only after Zenodo
confirms an archival record for this repository.
# Terminal-strand follow-up

The [opposed-source compensation](docs/OPPOSED_SOURCE_COMPENSATION.md) proves
that one occupied band with two occupied fronts and four forced endpoint
blanks supplies two units. It pays two mixed-color sources while counting
the receiver once, including actual source-to-band matching edges and
capacity-two receiver tiles. A third Lean module checks the all-length
surplus, boundary parity and two-source charge consequence. Sharp all-width
grid families, small exhaustive receiver completions and independent
coordinate/strand checks accompany the proof. Arbitrary bent and staggered
source fronts remain open.

The [parity-enhanced band compensation](docs/PARITY_ENHANCED_BAND_COMPENSATION.md)
proves that an even-length occupied band with an odd number of crossing
matching edges has at least three more blanks than selected vertices.
This pays a filled source even with one saturated export when its residual
band-port count is even, extending the previous zero-export sufficient class.
Two new Lean modules prove the all-length geometric surplus, its matching and
charge consequences, and a global injective one-color endpoint allocation
with component ownership. Full-grid geometry adapters remain explicit written
interfaces. The protected manuscript is unchanged.

The [mixed-color cut obstruction](docs/MIXED_COLOR_CUT_OBSTRUCTION.md) proves
pairing-independent directed terminal cut bounds. Disjoint regions can sum
bounds using one fixed endpoint color; black and white certificates may count
the same strand and cannot be added. An explicit feasible 6-by-(8+2k) family
has one connected region with zero shortage, one PP debt, one SS donor and
one PS strand for every maximum pairing. No auxiliary switch sequence can
cancel that debt despite numerical balance. This refutes a connectivity-based
switch rule, while aggregate compensation and the grid target remain intact.
Run `python3 develop/check_mixed_color_cuts.py --output output/mixed-color-cut-controls.json`.

The [terminal pruning and color compensation follow-up](docs/TERMINAL_PRUNING_AND_COLOR_COMPENSATION.md)
proves complete terminal-free pruning even with negative reserves, and an
injective compensator for components whose L/P terminals have one color.
It also retains the export mismatch term for general disjoint accounting
partitions. Written proofs and independent coordinate controls check the
external review suggestions; mixed-color global allocation remains open.

The [directed strand relay](docs/DIRECTED_STRAND_RELAY.md) extends the local
switch through an arbitrary ordered chain of LS/PS strands. One SS donor
travels along their S sides and cancels a terminal debt, with explicit
degree-four junction and order hypotheses. General reachability and disjoint
relay packing remain open. Its checker tests abstract strand graphs only.

The [strand-switch normal form](docs/STRAND_SWITCH_NORMAL_FORM.md) proves
pairing-choice and checkerboard invariants, cancels debt and SS strands
sharing a capacity-two tile, and assigns distinct reserves encountered by
debt strands. The remaining debts share no tile with an SS donor and meet
no reserve. This simplifies the geometry without changing the net shortage.
Run `python3 develop/check_strand_switches.py --output output/strand-switch-controls.json`.

The [terminal-strand accounting note](docs/TERMINAL_STRAND_ACCOUNTING.md)
proves an exact single-use decomposition for arbitrary deficient regions,
including capacity-two junctions and diagonal passages. It identifies
LL/LP/PP debt, SS donors and unused-slot reserves, shows neutral receivers
only pair ports, and completely prunes closed neutral regions. Run
`python3 develop/check_terminal_strands.py --output output/terminal-strand-controls.json`.
The universal donor-allocation inequality remains open.

The [minus-one tip obstructions](docs/MINUS_ONE_TIP_EVENTS_AND_LOCAL_OVERLOAD.md)
give actual feasible seven- and nine-module fusions. Both tips of one
negative two-leg module gain even with no negative rotors. A full tile
with endpoint partition 3+1 has two regular events and one irregular
event, so its own two correction units cannot pay all three. This
refutes tip exclusion and payment only from that same tile's remaining
credit; both global compensation budgets stay positive. Sixteen symmetry
images and seventeen actual-coordinate Lean declarations pass. The
examples are not fully frozen; unrestricted grid equality remains open.

The [fully frozen zero-credit tip family](docs/FROZEN_ZERO_CREDIT_TIP_FAMILY.md)
strengthens that obstruction: a connected three-module parameter family
has one irregular tip event with J=K_regular=C=0, and every endpoint is
frozen under matching promotion. Thus even globally transported square
credit cannot pay every tip event. Separated copies give arbitrarily
large pure-credit deficits, while negative-module mass keeps the finer
compensation budget positive. The note gives a uniform geometric and
freezing proof; 144 parameter controls, eight symmetry images and six
copy controls pass. Twenty-three Lean declarations verify the reference
coordinates, its complete 76-step freezing certificate and separate
scalar consequences. General joint allocation of S+C-G remains open.

The [all-phase joint-slot theorem](docs/ALL_PHASE_JOINT_COMPENSATION_SLOTS.md)
now covers both row-shifted U phases as well, with arbitrary rotor phases.
Its complete boundary classification assigns marked donor sides and
irregular events to distinct actual slots, including an inactive-event
rule at their shared upper-corner candidates. It proves
K_irregular+G<=2S+2B01+2B10, hence the explicit sufficient condition
N+C>=S+2B01+2B10 for the coefficient-one bound. The condition depends on
source widths but not leg heights. All 896 boundary images, 512 complete
physical images and 25 scoped Lean declarations/audits pass. An existing
fully frozen opposed band explains why the old minus-one-only gate
classification cannot be extended unchanged. Universal residual payment
remains open. The preceding zero-credit family's separate review has
completed ACCEPT; it does not cover this later all-phase theorem.
The all-phase review returned REVISE: the standalone statement now
explicitly fixes final endpoints and matching to the original unions,
defines all exceptions source-locally and gives the exact event trigger.
Its complete marked-side proof clarifies foreign ownership of consumed
supports and the old protector adjacent to v. The original review and
[assessment](docs/reviews/2026-10-20-all-phase-joint-slot-assessment.md)
are retained. The follow-up completed ACCEPT for the repaired source-fusion
theorem, conditional on its expressly established ledger, rotor barrier,
donor-ring injectivity and rotor-slot inputs. Original stream DONE exactly
matches the terminal review; execution checks remain separate evidence.

The [separated-negative-receiver theorem](docs/SEPARATED_NEGATIVE_RECEIVER_COMPENSATION.md)
removes that density hypothesis when no physical receiver tile contains
endpoints of two negative sources. For arbitrary U widths, independent
leg heights and all phases it proves sigma>=|N-B|+2R, where B counts
negative U sources and R negative rotors. Zero-charge rotors are permitted
in the 2P1T-only phase. Actual irregular events force a full tile with
one unused correction unit; the only remaining bar cost and an upper
corner side assignment use the same one-unit reservation exclusively.
Counting the remaining marked sides by both positive and negative
sources closes the inequality without a density condition. All13 local
states,344 physical images and14 scoped Lean declarations/audits pass;
296 images outside the hypotheses are excluded explicitly. General
negative-receiver overlap and zero-rotor3P0T payment remain open.
The independent Sections1-5 review completed ACCEPT for the written
deduction from the established inputs. Its diagonal-blank and reservation
wording clarifications are implemented; original stream DONE matches
all11921 terminal response characters. Execution evidence is separate.

A separate extension in Section6 removes receiver separation and allows
all rotor phases at the cost of two explicit local defects. It proves
sigma>=|N-B|+2R-D-H, where D counts vulnerable negative owners in tiles
shared by negative sources and H counts the negative1P1T/zero3P0T role.
All640 complete physical images pass both the tilewise and global
inequalities;496 give a nonnegative lower bound. The new sufficient
condition is D+H<=|N-B|+2R. This extension is outside the scope of the
accepted Sections1-5 review. Its separate review returned REVISE, narrowly
requesting the exhaustive zero-rotor catalogue. Section6 now states that
catalogue and proves the four-phase reduction explicitly; the review is
archived without relabelling its verdict.

The [singleton-defect refinement](docs/SINGLETON_NEGATIVE_DEFECT_COMPENSATION.md)
proves sigma>=|N-B|+2R-O-F-H. Shared bar profiles pay themselves; O counts
shared tiles with a negative1P1T owner, while F is the extra unit when
all four owners are negative1P1T. Thus positive U sources, negative
phase11 U sources and arbitrary zero rotors satisfy coefficient one
with unrestricted receiver overlap. All434 feasible signed local packings
pass; the refined bound is nonnegative on all640 physical controls,
strictly improving the old D+H bound on160 of them.

The [actual-demand half-slot theorem](docs/ACTUAL_IRREGULAR_HALF_SLOT_BUDGET.md)
proves Kirregular<=S+C+floor(BR/2), with BR counting actual zero-rotor
3P0T/negative1P1T contacts. It gives sigma>=N-G-floor(BR/2) and removes
the rotor-count restriction when all U sources are positive and zero
rotors have only2P1T profiles. With no positive U, arbitrary negative
U phases and negative rotors also satisfy reserve when zero rotors have
only2P1T profiles. Local credits are used after regular expenditure.
The half-slot bound is nonnegative in592 of640 physical controls; the
two new sufficient bounds complement one another.

Seventeen additional Lean declarations and individual axiom audits pass
locally, covering local profile reduction, all four rotor phase catalogues
and conditional global arithmetic. The full geometric adapter remains
written. Same-conversation review5005a44b completed ACCEPT for the repaired
general bound, both refinements, automatic subclasses and remaining exact
identity. Its L-elbow clarification is implemented; original stream DONE
matches all18005 response characters. The later rotor-only result has a
separate review scope.

The [rotor-only reserve theorem](docs/ROTOR_ONLY_RESERVE_AND_RECTANGULAR_COMPONENTS.md)
proves S+C-Kirregular>=2cminus and sigma>=2cminus for every finite complete
rotor fusion, with arbitrary phases, chiralities and contacts. Exact
sixteen-role ownership and finite support propagation exclude irregular
contacts with zero rotors. Negative contact components are Cartesian
rectangles in rotated tile coordinates. Distinct full tiles pay the
excess events by a vertex-edge-face identity, leaving two units per
component. All-negative fusions attain equality in reserve; a complete
all-parameter family shows why source mass alone is insufficient.
Six owner tables, eight all-index support-role calculations,59 physical
controls and19scoped Lean declarations/axiom audits pass. Finite descent,
the general rectangle proof and geometric adapters remain written.
Independent reviewd8ed1445 completed ACCEPT for this written theorem;
event, optional-selection and proof-dependency clarifications are implemented.
The exact reserve is 2cminus+Cother, with nonnegative other-tile credit.
See the [review assessment](docs/reviews/2026-10-20-rotor-only-reserve-accepted-assessment.md).
Unrestricted mixed-source payment and the
rectangular-grid triple equality remain open.

A [positive U cap obstruction](docs/POSITIVE_U_CAP_NONCOMPLETION_OBSTRUCTION.md)
excludes one specific attempted termination of the forbidden rotor chain,
even with arbitrarily many further U sources of any permitted dimensions
and arbitrary rotor images. A universal four-site stencil blocks every U
owner; the unique remaining rotor closes a two-site cavity which cannot
contain a complete new source. The general noncompletion proof is written;
13 scoped Lean declarations and individual axiom audits pass, including
the all-dimension/eight-orientation U stencil theorem. Exact geometry and
27 dimension/216 isometry controls pass. This excludes that partial seed,
not every cap or the mixed-source target. Separate review9a35516b completed
ACCEPT for the all-parameter written noncompletion proof and its adapters;
see the [assessment](docs/reviews/2026-10-20-positive-U-cap-accepted-assessment.md).

The later [width-eight cap theorem](docs/WIDTH_EIGHT_U_CAP_NONCOMPLETION.md)
also rules out a cap for which a U owner DOES fit at the first forced
support. A general endpoint-role lemma forces that owner's four-step
stem and a further original support. Both the U and rotor ownership
branches then force the same second site, which has no permitted owner.
The new six-site corridor exclusion applies to all U dimensions and
isometries.30 dimension/240 isometry controls check8768 endpoints.
Its16 universal coordinate/local declarations and individual axiom audits
pass locally. The general source-image/support adapter and noncompletion
assembly remain written. Its separate reviewfd908a7c completed ACCEPT for
both ownership branches and the full-support/source-image adapters;
see the [assessment](docs/reviews/2026-10-20-width-eight-U-cap-accepted-assessment.md).

The [arbitrary-width admission barrier](docs/SHORT_TIP_CAP_ADMISSION_BARRIER.md)
now treats caps U(W,A,4)+(-4,-W) with every even W>=6 and A>=4.
Any complete extension needs W>=12 and an incoming leftward U terminal
of height8<=h<=W-4, with its bar downward. A fixed43-endpoint mask excludes
rotor ownership; short U tips create an inward support with no permitted
owner. This eliminates widths6,8,10 for every independent cap left height,
while leaving all longer incoming legs explicitly open. General mixed
joint compensation and arbitrary grids remain open.
The new17 scoped Lean declarations/individual axiom audits pass, including
the distance-parametrized stencil, arbitrary opposite-height support
consequence, mask geometry and all-parameter cap inclusions.30 source
dimensions/240 isometries check8768 endpoints;24 independent cap parameters
and4 width-six left heights check the geometric adapters. The full
admission theorem assembly and physical wall argument remain written.

Independent strip-tree review: task `355b1665-3f6d-4499-8d79-e57afbdd56b9`, conversation `conv_114a15870b1dd1fd`, currently dispatched/waiting_response. Identity checked by exact submitted-prompt equality. No mathematical verdict or independent execution is available yet; see [receipt](output/strip-tree-review.json). The pending review inputs and stream are archived outside the disposable checkout.
