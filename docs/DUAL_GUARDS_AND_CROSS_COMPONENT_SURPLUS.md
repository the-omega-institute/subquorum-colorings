# Two protected guards per positive module and cross-component surplus

20 October 2026. We reuse the two actual guard patterns of a positive
two-leg module and count BOTH of their capacities. This gives a general
nonduplicated loss theorem and a stronger scalar compensation budget. It
does not assert that every grid configuration decomposes into these modules.

## 1. Physical hypotheses and exact quantities

Use the supported-module fusion hypotheses of
DEGREE_THREE_FUSION_AND_PROTECTED_DONORS.md: original modules have connected
pairwise-disjoint endpoint sets, occupied endpoint degree exactly three,
and each original selection has exactly one original endpoint neighbor.
Keep the union matching and all original supports not consumed by endpoints.
Require final selected feasibility. Optional added selections are outside
the original receiver union and have no endpoint neighbor. No port, once-use,
matching-direction, forest or freezing assumption is imposed.

Covered modules are affine copies of the two-leg constructors with even
width w>=6 and independent even leg heights a,b>=4, and of the four-port rotor.
Let N be the number of positive covered modules and define

    S = N - sum_{covered i} rho_i >= 0.

The phase table gives positive charge one only for the reference two-leg
phase; other two-leg phases and all rotor phases are nonpositive. Additional
supported original modules may be present: write tau for their TOTAL original
corrected charge, counted once per original module. Set tau=0 when all
modules are covered. All receivers and deficits below belong to the FINAL
physical configuration, including those additional modules.

As before, J counts new mixed full PHYSICAL TILE squares, K counts degree-four
endpoints whose unique new occupied neighbor is inside the same tile, and
d4 is the total number of degree-four endpoints. The established exact ledger is

    rho_final = N-S+tau-2J+K,
    sigma := mn/2-|T|-|M| = D-rho_final.               (1)

Here D is the total endpoint-free physical tile deficit. All saturated-mate
transfers are retained in rho_final. A favorable new full square is used
only through -2J; it is not an additional endpoint-free donor.

## 2. The paired protected patterns

For a positive two-leg module in reference coordinates, the left pattern is

    x_L=(3,2), p_L=(3,1), z_L=(2,3), q_L=(1,3),

and the right pattern is its image under the tile-preserving reflection
C(r,c)=(r,w+1-c):

    x_R=(3,w-1), p_R=(3,w), z_R=(2,w-2), q_R=(1,w-2).

In each pattern x is selected, p is its own endpoint anchor, z is the
opposite tile corner, and q is the saturated endpoint guard. The three
protecting endpoints are

    A_L={(2,1),(4,1),(1,3)},
    A_R={(2,w),(4,w),(1,w-2)}.                        (2)

The old unique blank neighbors, in the corresponding order, are

    B_L={(2,2),(4,2),(2,3)},
    B_R={(2,w-1),(4,w-1),(2,w-2)}.                  (3)

Each blank site lies outside its protector's physical tile. For the first
two right pairs this uses even w: the columns w-1,w are in different tiles.
For the third pair the rows1,2 are in different tiles. The left pairs have
the same property. Tile-preserving transport retains these relations.

The two protector sets in(2) are disjoint for w>=6, including the minimum
width. Their row-two and row-four columns differ, while their row-one
columns are3 and w-2>=4. Different rows cannot coincide. The two donor
tiles are also distinct: their column indices are1 and(w-2)/2>=2. Unequal
leg heights cause no exception because each height is at least four and
the top two rows contain both saturated guards.

Call a SIDE marked if at least one of its three protectors acquires degree
four. Let G_L,G_R be the numbers of marked left and right sides among the
N positive modules, and put G=G_L+G_R. Each side is charged at most once,
even if more than one of its protectors acquires degree four.

## 3. General two-guard compensation theorem

**Theorem.** Under Section1's hypotheses,

    D >= 2N-G,                                      (4)
    K+G <= d4,                                      (5)
    sigma >= N+S+2J-K-G-tau
          >= N+S+2J-d4-tau.                        (6)

In particular K+G+tau<=N+S+2J is sufficient for the coefficient-one half-area
bound. If tau=K=G=0, then sigma>=N+S+2J. This is strictly positive when
N+S+2J>0, in particular if at least one positive covered module is present.

Proof of(4). Consider an unmarked side. At the anchor p, the two opposite
old endpoint neighbors a,b retain occupied degree three. Thus their old
blank neighbors adjacent to x remain blank. If x became a foreign endpoint,
it would have at most two occupied neighbors, contradicting the minimum
endpoint degree of three. Hence x survives as selected. Final feasibility
keeps its adjacent tile corners blank. The saturated guard q keeps the
opposite corner z blank by degree preservation. The tile is endpoint-free
with exactly one selection and has actual physical deficit one.

There are 2N-G such unmarked sides. The two tiles belonging to one module
are distinct by Section2. If tiles from two different modules coincided,
their sole selected sites would coincide. That retained selection would
then touch two different old endpoint anchors, which persist and belong to
disjoint original endpoint sets, violating final feasibility. Thus ALL
2N-G tiles are distinct. All other endpoint-free tiles have nonnegative
deficit: three selected corners would give a selection two occupied
neighbors. Their unit deficits are counted once in D, proving(4).
No claim about additional surviving donors is needed.

Proof of(5). Choose one degree-four protecting endpoint for each marked
side. Two sides of one module use disjoint protector sets by(2), and different
modules use disjoint endpoint sets. Therefore the G chosen endpoints are
different. Each has exactly one new occupied neighbor, its original unique
blank site from(3). All those events are INTERTILE, so none belongs to the
K intratile events. The K events themselves have distinct tail endpoints,
since each original degree-three endpoint gains at most one new occupied
neighbor in a grid. This constructs K+G different degree-four tail endpoints.
The count does not require their new-neighbor head sites to be distinct.
This proves(5) without charging any endpoint twice.

Finally substitute(4) and(1):

    sigma >= (2N-G)-(N-S+tau-2J+K)
          = N+S+2J-K-G-tau.

Apply(5) for the second inequality. This proves(6). QED.

## 4. Comparison with the previous one-guard budget

For tau=0, the old canonical-left count L is exactly G_L. Its guaranteed
slack was S+2J-K-G_L. The difference between the new and old credits is

    [N+S+2J-K-(G_L+G_R)]-[S+2J-K-G_L] = N-G_R >= 0.

Thus the new credit never decreases and gains one unit for every unmarked
right side. This is a quantitative improvement, not a proof that some
unrestricted configuration failing the old sufficient condition is now
covered. That broader coverage question remains open.

For degree-three fusions, G=K=0. We now retain TWO distinct actual unit
donors per positive module and certify slack at least N+S+2J, strictly
positive whenever this bound is positive.
Concrete all-parameter consequences are:

| Family | N | S | J | New guaranteed slack | Previous slack |
|---|---|---|---|---|---|
| Four-way cycle, even w>=8 | 4 | 0 | 1 | 6 | 2 |
| Rotor star, even w>=6 | 4 | 2 | 0 | 6 | 2 |
| Chain of k stars and k-1 connectors | 4k | 3k-1 | 0 | 7k-1 | 3k-1 |
| Occupied adjacent bands, even w>=6 | 1 | w-1 | 2 | w | w-1 |

The occupied adjacent bands have K=4 but G=0 on both sides. The two full
square credits cancel K only once. For opposed bands in canonical alignment,
N=1,S=w-1,J=K=0,G=2: BOTH original donor tiles are consumed. The new credit
is w-2, exactly the previous credit. Thus the obstruction is not removed
by pretending that an actually consumed donor survived.

These results improve the certified surplus inside the stated module class.
They do not establish a universal improvement beyond the existing5/6bound
or the general grid triple equality.

## 5. Actual cross-component payment and its scope

Equation(6) allows the covered modules' surplus to pay the TOTAL charge tau
of additional receivers, provided their presence satisfies all physical
hypotheses and the final protected-side checks. Each unmarked side contributes
one distinct actual endpoint-free unit-deficit tile. A demand assignment
must use each such tile at most once.
This is a global closed-receiver counting statement. It does not impose
receiver-owned adjacency constraints or establish a receiver-labelled Hall
or flow theorem.

A completely explicit example has three endpoint components. In a32-by32
grid take positive two_leg_case(6,4,4) modules translated by(0,0) and(0,12),
and take the width-six rotor star translated by(16,16). Their occupied
sets are separated; each original component remains feasible, occupied
degree three and fully frozen. Their corrected charges are1,1,2.

Treat the first two modules as covered and the star as an additional
supported original module. Then N=2,S=J=K=G=0,tau=2. Assign:

* the first module's left tile to its own charge;
* its right tile to the first unit of the star's charge;
* the second module's left tile to its own charge;
* its right tile to the second unit of the star's charge.

The four physical tiles are distinct and each has actual deficit one. Thus
four units pay total charge four with no reuse, without using any donor of
the star. The independent checker verifies this assignment and the complete
receiver identity. No adjacency-based donor ownership is claimed by this
example.

## 6. Verification and bounded discovery

Run the physical checker:

    python3 develop/check_dual_guard_compensation.py --output output/dual-guard-compensation-controls.json

It passes57physical parameter cases, including27unequal-height single
modules, and288phase/symmetry images. It verifies both protector sets, all
intertile blank pairs, actual distinct unit donors, distinct marked-side
witnesses and disjointness from the actual intratile event endpoints. New
credits strictly improve48canonical cases and72images. The three-component
payment example is checked separately. Its raw discovery budget also agrees
with the independent physical ledger on every supplied case.

DualGuardCompensation.lean kernel-checks the general left/right local
disjointness, distinct tiles, intertile protector geometry, generic
owner/side and donor-tile injections, and all scalar budgets, including
external charge and the exact improvement. The arbitrary physical-configuration
adapters and global witness selection have the written proofs above and
coordinate controls; this is not claimed as a fully formal global geometry
theorem. All 19 declarations and their individual axiom audits pass locally
with Lean 4.33.0. The audit uses only propext and Quot.sound, with neither
sorryAx nor native_decide. See output/dual-guard-compensation-formal-check.json.

Separately, exhaustive pair discovery tested the28module types consisting
of w in6,8,10, a,b in4,6,8 and the rotor. It found16684feasible contact
placements, or66736cases with all four tile phases:424coarse-rule failures,
zero failures of the previous finer condition. This is a bounded statement,
not an all-parameter pair theorem.

A758-placement SAT search in16-by16for3through6modules with one fixed
positive module at(2,2) returned UNSAT. A fixed feasible fully frozen
three-module assignment passed both the encoding and independent ledger
controls. Removing the anchor restriction returned UNKNOWN at the 60-second
solver budget, with recorded reason_unknown="canceled"; the process was not
cancelled by the user. This is not an exclusion. The search does not assume freezing and is used
only for discovery. Commands and precise restrictions are in the search
sources and receipts. No universal claim is inferred from either search.

The preceding general fusion/opposed-band packet has now received its own
ACCEPT review. The present two-guard theorem was developed later and is
outside that review's input. Its separate same-conversation followup
6660d0c2-5beb-4e53-a33c-a544835ae700 completed ACCEPT at
2026-10-19T21:51:49.657UTC, observed gpt_6/pro. Original stream 82701
ended successfully with DONE and exactly the terminal response's 19131
characters. We applied its two prose qualifications: strict positivity
requires a positive lower bound, and only unmarked sides supply guaranteed
physical units. Its assessment is
reviews/2026-10-20-dual-guard-compensation-assessment.md. This review does
not cover the later automatic positive-phase fusion theorem.

The later positive-phase fusion theorem now proves automatic protection and
K<=2J when all modules are positive, and localizes mixed-phase intratile
costs to nonpositive source modules after using each full-square credit once.
See POSITIVE_PHASE_FUSIONS_AND_TILE_DEFECT_CANCELLATION.md. Next: control
that remaining nonpositive-source tax and affected sides, or produce a
genuine fine-rule failure. General decomposition and external priority remain open.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
