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

The Lean theorem explicitly states psi_sq(Q_n)=2^(n-1). The beta_2 identity
was already established by Sahbi and also follows from the written proof;
beta_2 is not defined in the archived Lean module. The subsequent structural
and full-grid results are not yet Lean formalized. The conditional band and
endpoint compensation lemmas below now have Lean proofs; the unrestricted
mixed-direction grid coloring formula remains open.

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
