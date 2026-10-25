# From the hypercube solution to grids and structural characterization

The starting point is the completed proof of Sahbi's Conjecture 6.4:
psi_sq(Q_n)=2^(n-1) for every n>=2. Its Lean formalization checks this
all-dimensional statement. The boundary injection and its Hall-matching
consequence supply the main conceptual link to further research.

## Rectangular grids

25 October: [forced short-beta PP guards and cyclic-block elimination](FORCED_POCKET_GUARDS_AND_CYCLE_ELIMINATION.md)
derives the adjacent occupied PP columns from complete freezing, rather
than assuming a guarded construction history. Every short horizontal beta
between alpha TP tips is an exclusive whole resource. Non-tree components
of their complete multigraph eliminate with exact V=n+V_res; if their
alphas have empty direct interval support, c=n+c_res too. The tight frozen
fixture contains a second, older beta, so its completed two-alpha component
is a parallel-edge resource cycle. 752 systems/268 frozen boards/1,636 motifs,
290 independent packs and three scoped Lean declarations pass. A degree-three
nonfrozen board refutes the weaker guard rule. The remaining trees require
a joint exterior cut proof; universal compensation and 5/6 remain open.

25 October: [filled-pocket tree exterior compression](POCKET_TREE_EXTERIOR_COMPRESSION.md)
retains the full exterior mixed/BP/beta/interval network and replaces each
internal tree by one residual source choosing an original alpha exit.
Exact original payment is B+R. If grouped alphas have empty direct support,
minimum links are exactly B+d; a frozen board refutes this cost equality
without the assumption. A discounted circulation restores exact general
cost, accounting for multiple exterior exits by saved internal links.
866 models/1,732 checked lifts, including 264 frozen boards and 285 independent
primitive packs, plus four scoped Lean declarations pass. The remaining
geometric obligation is a joint exterior cut inequality; universal 5/6 is open.

25 October: [shared-pocket joint deficit and full-pool cost obstruction](SHARED_POCKET_COMPLETION_AND_JOINT_DEFICIT.md)
extends the guarded-pocket geometry to different alpha owners. In the declared
pocket interface, any multigraph has exact payment V=k-t and minimum links
c=k-t-z, where t counts all-filled tree components and z counts vertices
incident to empty pockets. Strict-distance parent-edge injection prevents
joint reuse. A new completely frozen tight-support board keeps full payment
two but raises full-pool minimum links from zero to two after filling one
shared pocket; q copies have exact cost 2|S|. This refutes cost-nonincreasing
shared completion, not universal compensation. General written proofs,
2,912 abstract graph states, 422 physical controls and four scoped Lean
declarations pass. The submitted manuscript and the 5/6 bound are unchanged.

25 October: [protected singleton reserves](PROTECTED_SINGLETON_RESERVES.md)
settles a positive completion class left by the sealed escape-cycle example.
A fixed selected guard and three old matched neighbors force a private
original BB singleton to survive every feasible monotone extension. For q
such sources, ordinary/full-fork optima obey V=q+V_res and c=c_res, with
source and resource removed together. A new frozen one-support variant has
exact reservation cost r for any r reserved protected units. General written
proofs, 26,568 value/cost comparisons, 13,061 independent primitive packs,
160 physical extensions and three scoped Lean declarations pass. No claim
that every fork has this reserve, or that 5/6 improves.

25 October: [frozen beta-fork escape geometry](FROZEN_BETA_FORK_ESCAPE.md)
proves a forced diagonal P, strict rank dependencies, an outward actual mate,
and an injection of escape sites. A pure two-point escape cycle can serve at
most one distinct alpha owner. An explicit fully frozen 12x14 construction
puts the escape in such a cycle; a PP plug seals its adjacent interval while
preserving freezing. Thus a forced P is not automatically a new local payment.
All-q copy/padding proofs, 712 frozen scans/484 motifs and six scoped Lean
declarations pass. Global compensation and 5/6 remain open.

25 October: [all-live shared-gate certificate tradeoff](LIVE_GATE_CERTIFICATE_TRADEOFF.md)
settles the abstract maximum-certificate question even after safe pruning.
Any two full binary merge/split trees sharing one mixed root give q alpha
sources, all mixed owners live and terminal degree at most two. Every maximum
certificate has 4q-2 assignments and pays only one alpha, whereas q direct
beta links pay all q. The largest certificate paying at least p has exactly
4q-1-p assignments; full payment must sacrifice q-1 assignments from maximum
coverage. No frozen realization is claimed. On 576 existing actual frozen
boards, explicit maximum certificates attain ordinary optimum. General written
proofs, exhaustive named small cases and nine scoped Lean declarations pass;
the universal geometric question and 5/6 bound remain open.

25 October: [paired holes and certificate optimization](PAIRED_HOLES_AND_CERTIFICATE_OPTIMIZATION.md)
make the fine partial-certificate budget exact: each assigned-incidence component
has at most two holes and loses one payment exactly when it has two. Minimizing
this budget over all partial certificates equals the ordinary compensation
deficit; direct unused-target additions preserve an optimum. Maximum cardinality
does not: a unique-maximum abstract trap has an unbounded copywise payment loss.
A completely frozen mirrored 10x30 board has two holes in one interaction
component even after safe pruning, with both bad and repaired maximum
certificates. Reassigning one slot to a distinct original interval repairs the
bad certificate at unchanged links and coverage; restricting both resource and
link pools creates a real restricted deficit, while full original beta links
still pay both alphas. General written proofs, 80 physical systems and scoped
Lean pass; the universal 5/6 bound is not improved.

25 October: [partial tip compensation and safe mixed pruning](PARTIAL_TIP_COMPENSATION_AND_SAFE_PRUNING.md)
strengthens the two-slot test: a partial injective assignment leaves at most
sum floor(h_C/2) unpaid alphas, counting holes separately in final-alpha
components joined by original assigned intervals. Original interaction-component
matching defects h_D similarly give sum min(a_D,floor(h_D/2)); one hole per
component is harmless. The bound is sharp with two owners per original resource.
Deleting mixed owners off all alpha-to-resource routes preserves ordinary/full
payment and link optima, but the physical PP-sealed board still has one impossible
alpha end after deletion. All q separated copies nevertheless have deficit zero
by the new criterion. Written proofs, independent controls and scoped local Lean
pass; general frozen geometry and the universal 5/6 improvement remain open.

25 October: [two-slot sufficiency and a frozen internal Hall obstruction](FROZEN_TIP_SLOT_OBSTRUCTION.md)
prove that a complete TP-to-BP/two-interval-slot assignment suffices for full
ordinary whole-support compensation; three slots are already unsound. Complete
freezing does not imply the two-slot certificate, even among alpha-reachable
owners. An explicit PP-sealed 10 by 16 board has exact terminal Hall defect one
and full compensation one at one link. For all q separated copies and arbitrary
even blank right padding, defect is q while all q alpha payments remain possible
at exactly q links. The failed condition overcounts neutral mixed TP demands.
Independent controls and scoped local Lean pass; universal geometric saturation
and the 5/6 improvement remain open. The submitted manuscript is preserved.

21 October: [all-length terminal-companion injection](ALL_LENGTH_SINGLETON_COMPANION_INJECTION.md)
extends the joint E/S versus S/P/R activation assignment to arbitrary negative
singleton incident length b. The exhaustive next-owner roles are E,S,H and
Vcorner; the last is a genuinely additional role beyond b=6. Exact dimension
disjunctions replace short-case bounds that cannot be extrapolated.
A NEW mandatory C support lies INSIDE the old shortest-south enclosure,
so the TWO prescribed owners have NO arbitrary complete U/rotor extension.
The old unmarked S4 implication is vacuous, not a realized capacity bonus;
at b=6 only E/H survive. Retaining actual s gives the sharper conditional
floor mu>=n0+u+p+ceil((m8-s-t)/2), without losing unused lower pairs.
E/S terminal branches of EVERY length leave the unresolved t count.
The C=U(V,6,4),g>=V south subclass also has no complete extension, by a
separate THREE-COLUMN mandatory-support enclosure.23scoped local Lean
declarations and independent110fixed/6180partial-role plus101narrow-enclosure
controls PASS. Full allocation/grid equality remain OPEN. The prior corridor
and residual notes are now independently ACCEPTED; the short-note audit
requested a gate-specific singleton/terminal wording repair, applied.
The separate all-length auditc1605aa3 ACCEPTS that repair and the complete
initial all-length/S4/retained-s theorem,15929chars exactstream/API,
original76340exit0. Its packet predates the later three-column obstruction;
a separate addendum audits that result.

21 October: [short negative-singleton endings](SHORT_NEGATIVE_SINGLETON_ENDINGS.md)
exclude incident length four in arbitrary complete U/rotor extensions.
At length six, the forced next owner is one of E/S/H: the positive cases
inject into actual activations jointly with ALL S/P/R targets, while the
negative case injects into existing protected lower pairs. East requires
w>=W+8>=14; south requires d<=min(h-2,W-2) and its DISTINCT owner stays
unmarked. Counting each capacity once gives
mu>=n0+u+ceil((p+m8-t)/2). Longer negative singleton endings remain open.
A fixed three-source tight-return stencil has no arbitrary U/rotor completion;
increasing the transverse width gives a complete connected eleven-source
H witness with278endpoints,139matching edges,62selected supports and
POSITIVE margin27. This is not an allocation counterexample. Twelve scoped
general Lean declarations and independent role/count/32image controls PASS;
the separate concrete eight-declaration kernel certificate and axiom audit
also PASS locally, with NO axioms.
Independent audit cc4dd625/original13551 is live. It separately rechecks the
previous corridor note's repaired endpoint/support ownership sentence and
explicit reserve integrality after e2d1db08 returned REVISE. Full unrestricted
allocation, universal coverage and rectangular-grid triple equality stay OPEN.

21 October: [permanent corridors and single-use strip compensation](PERSISTENT_CORRIDOR_AND_STRIP_CAPACITY.md)
prove a complete corridor dichotomy for arbitrary U/rotor extensions. When
v>=d-4, a mixed cap and the whole upper-bar strip are permanent. Distinct
physical caps, once-per-owner strips and enclosed lower pairs are disjoint
from prior m8 receipts, giving L<=R(I)-p-u-ceil((A(I)+m8(I)+z)/2) in ONE
family attaining all component losses. A complete all-parameter I/J/K
family realizes both opposite caps on ONE strip; taller legal extensions
fill every lower pair and lose exactly one reserve. Twelve scoped local Lean
declarations,960phase/isometry images,480component subunions and an actual
two-loss certificate PASS. The new written theorem is submitted separately
for independent review; the original full-bar obstruction review5a86d678
has completed ACCEPT. Filled corridors/vertical regular exits and universal
demand coverage remain OPEN; no universal5/6 improvement or manuscript change.
The later [residual-coverage corollary](CORRIDOR_RESIDUAL_COVERAGE.md) proves
mu>=p+u+ceil((m8-t)/2), where t counts still-uncertified negative-U gates.
Thus t<=2(p+u)+m8+1 suffices for coefficient one in covered source families.
This deduction postdates the initial corridor review request, which failed
with a terminal broker browser error. A fresh independent review includes
BOTH notes. That reviewe2d1db08 completed REVISE: one endpoint/support
ownership sentence is corrected and reserve integrality is explicit.
Same-conversation re-reviewcc4dd625 is live; no full-target result follows.

21 October: [full-bar clearance and an unactivated exit](FULL_BAR_UNACTIVATED_EXIT_OBSTRUCTION.md)
classify the two full-bar gate forms at all dimensions. A complete connected
eight-source certificate refutes both full-bar-implies-producer-activation
and forced-exit-implies-positive-local-defect: the forced exit is an actual
regular2P1T pair with zero defect.184endpoints/92matching/40selected supports,
all32phase/isometry controls and eight kernel-only Lean declarations PASS,
with no axioms. Its margin is POSITIVE19; full allocation/grid OPEN.
The earlier PS/PR addendum2b910319 now ACCEPTS both written exclusions,
9355chars exactstream/API. Full-targetb90c01ca also completed with26023chars
of research leads. The corridor/strip and I/J/K parts are reconstructed in
the later note above; short negative-singleton branches remain unadopted.

21 October: [rotor activation transfer and negative-U path endings](ROTOR_TRANSFER_AND_NEGATIVE_U_PATH_ENDINGS.md)
extend the physical activation injection to ALL positive/rotor gate consumers.
An explicit single-use path allocation gives2mu=C+Sunmarked-Bbad, retaining
isolated bad negative-U endings. Consecutive P transfers drop width by at
least8 every two edges; P->S is impossible at any dimensions. A P->R exit
requires companion leg>=6 and intermediate width>=14.16scoped localLean,
31904legal restrictions and3166abstract path controls PASS; actual complete
S/R/PP/PR examples are absent from this fixture library. Written review3f49db6b
ACCEPTS the initial proof; companion north-bar/self-producer explanations
are explicit. Same-conversation addendum2b910319 now ACCEPTS the later stronger
two exclusions,9355chars exactstream/API. No full demand payment or grid equality follows from acyclicity.

21 October: [positive pair transfers and protected defects](PAIR_GATE_TRANSFERS_AND_PROTECTED_DEFECTS.md)
inject ALL positive gate consumers into distinct activated terminals. Marked
height-six recipients with forced height-eight transverse owners protect
distinct permanent U0/L3 occurrences, m8<=U0+L3. Counting all losing groups
ONCE strengthens the loss bound to2L<=2R(H)-A(H)-m8(H). Two complete connected
five-source examples increase the persistent integer floor from1to2.
12scoped Lean declarations,832images33728legal restrictions2024component
subextensions PASS; independent written reviewcc5ab6b7 ACCEPT with endpoint
wording and marked-label preservation clarified. General source/count adapters
remain written. Arbitrary negative-U endings/full-bar channels and FULL
allocation/grid equality remain OPEN; no universal coefficient improvement.

21 October: [feasible contact-hull localization](CONTACT_HULL_LOCALIZATION_AND_RAW_CONTACT_OBSTRUCTION.md)
identifies each component collection's UNIQUE least old contact carrier by exact
Horn closure. All R/N/G/mu increments localize to that complete feasible core;
aggregate losing groups use its reserve once. Raw endpoint neighbors alone can
be infeasible: an explicit J24 support forces a third old owner with no direct
new contact. Four NEW source-level Lean declarations,704images383680contact
subextensions and a60-endpoint/26-selection counterexample certificate pass.
Written review088ddf2e accepts the result with the empty-core convention now
made explicit. Contact-core standalone reserve is not uncommitted margin;
FULL allocation and rectangular-grid equality remain open.

21 October: [exact component loss and the marked-demand gap](COMPONENT_LOSS_AND_THE_MARKED_DEMAND_GAP.md)
give a general simultaneous loss bound for every complete feasible mixed-source
extension: all new-endpoint component subunions are legal and R/N/G/mu are affine.
Selecting all reserve-losing groups once proves2L<=2R(I)-A(I). A single old
owner can have TWO simultaneously losing groups, each with unbounded loss;
the nine-source all-k family supplies the explicit obstruction to loss
exclusivity. Six finite-list Lean declarations and704physical images pass.
Independent written reviewb4910cb9 ACCEPT. The full target is still the
stronger L<=mu(H) for the canonical demand hull, including the H=J core case;
the persistent activation floor alone does not pay all marked demand.

21 October: the [five-endpoint cap and gate-consumer restriction](FIVE_ENDPOINT_CAP_AND_POSITIVE_GATE_CONSUMERS.md)
exclude an unfillable support from EVERY U/rotor extension. A gate consumer
having the upper intratile support forces a transverse NEGATIVE U tip with
4<=h<=w-4. Width-six actual gate consumers must therefore be negative U
sources; all positive and rotor consumer roles are excluded. A positive
regular singleton consumer gives one distinct activated terminal occurrence,
already within A, with no duplicate payment. Nine scoped Lean declarations
and 49,152 U endpoint-role / 672 complete-image controls pass. Initial review
accepted the cap but requested semantic/role clarifications. After two explicit
repair rounds, final review c71bb9e1 ACCEPTS the written package, including the
new transverse/rotor consequences, under the inherited source model and ledger. Full
allocation and grid equality remain open.

21 October: [periodic strip compression](PERIODIC_STRIP_COMPRESSION.md)
reduces ANY n-source complete feasible family to coordinate spans at most
512n+2, with the identical legal-owner Horn lattice and canonical demand
hull. Every legal restriction's margin can only decrease, by half the
deleted nonnegative tile defect. Thus every hypothetical negative-margin
counterexample has this bounded geometric representative, for arbitrary n.
Three seam-level Lean lemmas and 6,480 physical compression steps pass;
general catalogue, reverse-clause and counting adapters are written.
Independent review accepted the substantive argument under the stated ledger,
but required restricting descent to internal strips. That correction is now
explicit, with strict span decrease checked at every operation. The
same-conversation correction re-review returned ACCEPT for the full written
compression theorem under the inherited source model and reserve ledger.
The full allocation inequality remains open.

21 October: [canonical gate consumption](MARKED_SIDE_GATE_CONSUMPTION.md)
identifies every actual positive-side mark with one fixed support consumer.
It gives a unique least demand-preserving Horn hull and eliminates duplicate
mark corrections in [feasible shared-core gluing](FEASIBLE_CORE_SEPARATOR_TRANSFER.md):
mu(F)=mu(L)+mu(K)-mu(C), subtracting actual core reserve once. Six scoped
source-level Lean declarations and geometric controls pass; catalogue/count
adapters have written proofs. Canonical hull reserve loss remains unbounded
in the connected nine-source family. Full allocation and grid equality remain
open; the next target is loss controlled by the existing hull margin.

The target is Sahbi's formula for arbitrary rectangular grids. Widths
8,9,10,11 are now proved at all positive lengths using exact full-vector
certificates and the existing periodic lower-bound constructions.

The [uniform grid arguments](GRID_RESULTS.md) now prove beta_2=F and
Omega_H=Omega_V=F at all dimensions. On even-by-even rectangles they give
|T|+(5/6)|M|<=mn/2 for arbitrary matching directions. The next step is to
strengthen this coefficient to one by controlling longer residual paths and
their global compensation, then account for odd-side boundaries. Exact
frontier states and constructed geometric examples test these arguments.

The [local-quota cut theorem](LOCAL_QUOTA_CUTS_AND_FROZEN_BATCH_OBSTRUCTION.md)
strengthens the two strip-allocation rules and reduces the first possible
charge-five resource failures to three leaf-free motifs. It also gives
an unbounded fully frozen family where every nonempty batch of the four
current corner-rule donors lowers the budget. Safe donor ordering or
reserving all donors cannot be assumed in the remaining coverage proof.

The [branched rotor theorem](BRANCHED_ROTOR_NETWORKS_AND_UNBOUNDED_RECEIVER_CHARGE.md)
extends coefficient-one compensation to admissible networks of two-leg and
four-port rotor modules. It assigns a distinct actual unit donor to every
positive module, even within the same receiver. An arbitrary-length fully
frozen occupied-degree-three family has receiver charge k+1, disproving any
constant ceiling in that setting while still satisfying compensation. This
separates the false receiver-ceiling rule from the open universal inequality.

The [physical fusion theorem](DEGREE_THREE_FUSION_AND_PROTECTED_DONORS.md)
removes prescribed ports and once-used-port restrictions. Actual receiver
charges add with an exact minus-two correction per new aligned full endpoint
square, plus the intratile new-neighbor defect if degree four appears.
Protected donor loss and this latter defect use disjoint degree-four endpoint
events. A physical count criterion therefore proves coefficient one with
controlled degree-four contacts, including an all-width fully frozen pair of
occupied adjacent bands. General decomposition into covered modules is open.

The [opposed-band theorem](OPPOSED_BANDS_AND_HARMLESS_DEGREE_FOUR_CONTACTS.md)
rules out automatic validity of the coarse degree-four criterion. For every
even width w>=6 and height h>=4 it gives a fully frozen physical fusion with
S=w-1, J=K_in=0, L=1 and d4=2h+4. The finer compensation credit is w-2
and the exact half-area slack is h(w-4)/2+2. Thus harmless intertile contacts
can grow without bound while the actual tax stays one. All four alignment
phases satisfy the finer criterion. Twenty parameter pairs,80alignment checks,
640symmetry images and67scoped Lean declarations pass, including actual
mixed-bundle exclusion for the8-by10configuration. General geometry has its
own written all-parameter proof; the broad d4 rule cannot be a universal bridge.

The [two-guard surplus theorem](DUAL_GUARDS_AND_CROSS_COMPONENT_SURPLUS.md)
retains two distinct actual unit donors per positive two-leg module. If N
positive covered modules have G marked sides and additional supported modules
have total old charge tau, it proves D>=2N-G, K_in+G<=d4 and
sigma>=N+S+2J-K_in-G-tau. The credit gains one unit per unmarked right side
over the previous canonical-left budget. Four-way cycles and rotor stars now
have guaranteed slack six, and k-star chains have slack at least 7k-1.
An explicit three-component assignment pays an external charge two without
reusing a tile. General geometry has a written proof; 57 cases, 288 phase
images and 19 scoped Lean declarations pass. This improves the surplus in
the stated module class, without a universal grid or ownership-flow claim.

The [positive-phase fusion theorem](POSITIVE_PHASE_FUSIONS_AND_TILE_DEFECT_CANCELLATION.md)
makes the finer budget automatic when every original two-leg module has
positive phase: both donors survive, G=0 and K<=2J, so sigma>=N. Its proof
uses the thirteen receiver-tile profiles and two boundary properties, without
decomposing a large feasible fusion into feasible pairs. A four-way cycle
explicitly has no feasible two-module subset. In mixed two-leg/rotor fusions,
positive-source intratile tails still use at most two correction units per
new full tile. Setting C=2J-K_positive>=0 gives
sigma>=N+S+C-K_nonpositive-G, isolating the remaining tax without reusing
tile credits. Controls pass 240 module images, 57 all-positive and 306 mixed
fusions, including 76 with actual positive-source events; 14 scoped Lean
declarations pass. Full mixed coverage and general decomposition remain open.

The [regular-tile and rotor barrier theorem](REGULAR_TILES_ZERO_ROTORS_AND_IRREGULAR_TAX.md)
extends automatic compensation to positive two-leg modules with arbitrary
zero-charge rotors: G=0, D>=2N, K<=2J and sigma>=N. In fact rotors of any
phase preserve both positive donors. For arbitrary module phases, the
seventeen regular tile profiles pay K_regular<=2J; the remaining irregular
profiles have total capacity exactly 2S-2H, independent of leg heights,
where H counts effective source phase (1,1) two-leg modules. Thus
sigma>=N-S+2H+(2J-K_regular)-G. With only positive two-leg modules and
R_minus negative rotors this gives sigma>=N-2R_minus+(2J-K_regular).
An actual all-length feasible zero-rotor chain has K_regular=4(k-1) and
J=2(k-1), testing unbounded degree-four defects at equality; full freezing
is not asserted. Controls pass 112 phase cases, 48 rotor barrier cases,
296 mixed fusions and seven chains; 22 scoped local Lean declarations pass.
The remaining target is the coupled payment of irregular 1P1T/2P0T events
and marked positive sides, without reusing negative mass or full-tile credit.
General decomposition and unrestricted grid/triple equality remain open.

The [minus-one joint witness theorem](MINUS_ONE_JOINT_WITNESS_COMPENSATION.md)
puts irregular tip events and marked donor sides into distinct tip and
bar-corner slots of charge-minus-one two-leg modules. A seven-of-twelve
outer-ring packing argument proves even the LOST original canonical donor
tiles are distinct. Even minus-one tips retain endpoint continuation;
marked sides arise exactly from upper bar corners invading donor gates.
Thus G<=2B_minus, with no reuse of irregular tip slots. If all two-leg
modules have charge +1 or -1, with B_minus negative ones and R_minus
negative rotors, this gives K_irregular+G<=4B_minus+4R_minus and
sigma>=N-3B_minus-2R_minus+C_regular. Thus N+C_regular>=3B_minus+2R_minus
is sufficient. The all-parameter assignment remains written; 28 scoped
Lean declarations, 224 boundary images and twenty-one physical
controls pass. An explicit seven-module fusion loses both positive donors,
refuting G=0 in the enlarged class while retaining finer budget five.
Fourteen of the Lean declarations verify that actual seven-module
configuration, including feasibility, original charges, both consumed
donors, zero intratile defect and exact final slack69. Its failure of
the density test does not refute compensation. No irregular
tip event was found in the controls; a bounded UNSAT search is not a
general exclusion. The full residual inequality remains open.

A proof of Omega(G_mn)<=F(m,n) would settle the grid coloring conjecture.
A counterexample to that stronger Omega bound would require revisiting the
reduction's sharpness; it would not by itself refute the coloring conjecture.

## Structural characterization

The target is to identify conditions under which psi_sq(G)=beta_2(G).
The signed boundary theorem gives a sufficient class, including appropriate
bipartite Cartesian products. The grafting formula gives exact counterexamples
to overly broad conditions: the gap can be unbounded even on subcubic trees.
The equality class is not hereditary, so a general characterization purely
by forbidden induced subgraphs is unavailable.

The next step is to examine natural restricted graph families, use the exact
tree recurrence to test candidate conditions, and prove conditions that
explain equality beyond the current signed-matrix hypothesis. Compare the
tree results with the earlier caterpillar work cited by Sahbi.

## Role of formalization and the manuscript

The current Lean proof covers the hypercube coloring-number equality.
Formalizing the general boundary theorem and subsequent structural lemmas
will support the two research directions. New computation and formalization
should be connected to a stated mathematical claim.

The manuscript's narrative is: solve the hypercube problem, extract the
boundary mechanism, then establish progress on grids and structural equality.
State the solved conjecture at its full strength and distinguish the exact
strip theorems from the still-open arbitrary-width grid conjecture.
