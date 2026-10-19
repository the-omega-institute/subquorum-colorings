# Sub-quorum colorings: hypercubes, boundary matchings, and grids

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
