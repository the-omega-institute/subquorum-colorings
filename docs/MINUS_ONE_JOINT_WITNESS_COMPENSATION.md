# Joint payment for charge-minus-one modules and marked donor sides

20 October 2026. We give a joint witness budget for arbitrary-contact
fusions of positive and charge-minus-one two-leg modules with arbitrary
rotors. Marked sides are caused precisely by upper bar corners of
minus-one modules invading the old donor gate. Irregular events use
different endpoints, the terminal tips. A packing lemma makes even lost
donor tiles distinct, giving these costs a nonduplicated endpoint ledger.
The resulting density criterion is sufficient; general mixed-phase
compensation and unrestricted grid decomposition remain open.

## 1. Hypotheses and theorem

Use the physical fusion hypotheses of Section 8 of
DEGREE_THREE_FUSION_AND_PROTECTED_DONORS.md. Original modules have occupied
endpoint degree exactly three, connected pairwise-disjoint endpoint sets,
their own perfect matchings, and selections with unique original endpoint
anchors. Form the complete retained-support fusion, removing only supports
that become endpoints, and require final selected feasibility. Optional
extra selections lie outside all original receiver tiles and have no
endpoint neighbor. The ambient even-by-even rectangle has its fixed
disjoint 2-by-2 tiling. No pair-feasibility, port, forest, final-degree-three
or complete-freezing assumption is made.

The two-leg modules have even width w>=6 and independently even leg
heights a,b>=4. In this theorem their original corrected charges must be
+1 or -1, namely effective source phase (0,0) or (0,1). Rotors may have
ANY effective phase. Write N for the number of positive two-leg modules,
B_minus for the number of charge-minus-one two-leg modules, and R_minus
for the number of charge-minus-two rotors. Other rotors have charge zero.
Thus the negative mass is S=B_minus+2R_minus. Use the original ownership
partition K=K_regular+K_irregular and set C=2J-K_regular>=0 as in
REGULAR_TILES_ZERO_ROTORS_AND_IRREGULAR_TAX.md. G counts marked canonical
left/right sides, once per side, even if its donor actually survives.

**Joint witness theorem.** Under these hypotheses,

    K_irregular + G <= 4B_minus + 4R_minus,            (1)
    sigma >= N-3B_minus-2R_minus+C,                   (2)

where sigma=mn/2-|T|-|M|. Consequently

    N+C >= 3B_minus+2R_minus                          (3)

is sufficient for |T|+|M|<=mn/2. The simpler density condition
N>=3B_minus+2R_minus is sufficient independently of the contact graph.
More precisely, split irregular events into tip events of minus-one
modules and rotor events. The proof establishes the stronger intermediate
inequality

    K_minus_one + G <= 4B_minus.                     (4)

More precisely G<=2B_minus, and a canonical donor fails exactly when its
gate is one of the minus-one modules' upper bar corners. Its entire
physical tile then belongs to that foreign module's original full bar.

Neither (3)'s necessity nor sharpness of its coefficient three is claimed.
The theorem does not assert that (3) holds for every feasible fusion.
The two-leg phases with charge 1-w are outside this theorem's hypothesis.

## 2. Old canonical donor tiles are already distinct

This packing fact does NOT require the donors to survive fusion. Normalize
a positive left donor tile as Q={2,3}x{2,3}. The original module contains
the seven endpoints

    {(1,1),(1,2),(1,3),(1,4),(2,1),(3,1),(4,1)}.

All lie in Q's twelve-site outer ring: {1,2,3,4} squared minus Q.
Every permitted orientation and either canonical side has seven original
endpoints in the corresponding twelve-site ring. These points exist even
at width six and height four. If two canonical donor tiles from different
positive modules were the same Q, their seven-site subsets of that ring
would overlap in at least 7+7-12=2 sites. This contradicts the original
endpoint sets being disjoint. Within a positive module its left and right
donor tiles are distinct for w>=6. Therefore ALL 2N original canonical
donor tiles are different, including those eventually marked or consumed.

This is a twelve-site pigeonhole proof valid at every position and
orientation. The finite eight-orientation checks are an independent
verification of its local geometry, not a search over possible fusions.

## 3. Exactly four exceptional endpoints per minus-one module

In reference source phase (0,1), after translation by (0,1), define

    C_i={(0,2),(0,w+1)},
    F_i={(a,2),(b,w+1)}.

C_i consists of the two upper exterior bar corners. F_i consists of the
two terminal leg endpoints. These four endpoints are distinct. Their
transported definitions are intrinsic: C_i is precisely the endpoints
having no original endpoint neighbor outside their physical tile; F_i is
the two leaves of the original endpoint graph.

Every endpoint outside C_i has an original endpoint neighbor outside its
tile. To check all parameters, bar interiors have a horizontal neighbor
across a tile boundary. Lower bar corners have their next leg endpoint
outside the tile. Paired stem endpoints have a preceding or succeeding
leg endpoint outside it; the final tips have their preceding endpoint.
The only exceptions are the two upper corners, whose two original
endpoint neighbors are both inside their full bar tile.

For EVERY endpoint p and every adjacent intratile blank v, if u is its
other intratile neighbor then 2p-u is an original endpoint. Outside F_i,
u itself is an endpoint too. Full bar tiles have no such v. In a paired
stem tile, u is the consecutive leg endpoint, and continuation is the
preceding or succeeding endpoint, including the final tip. These exist
at a,b>=4. At a terminal tip u is selected, but 2p-u is STILL the
preceding leg endpoint. Thus the continuation-only property has NO
exception. Each tip has a 1P1T tile and one adjacent intratile blank.

Thus all irregular tails of a minus-one module belong to F_i. C_i lies
in original full tiles and supplies no irregular tail. This is a complete
all-parameter boundary classification; arbitrary lengths add ordinary
paired stem tiles and no new exception.

## 4. Each marked side uses an exceptional endpoint inside its own tile

Fix a positive module and normalize its left pattern by

    Q={2,3}x{2,3},
    u=(2,2), x=(3,2), z=(2,3), y=(3,3),
    p=(3,1), q=(1,3).

Here x is the original selected donor corner, p its anchor, and z the
opposite corner. Its three protector endpoints (2,1),(4,1),q have unique
old blank neighbors u,v=(4,2),z. By the persistent-anchor lemma, any newly
occupied one of these blanks is a foreign endpoint. Every original
occupied site remains occupied in the final fusion.

Suppose the side is marked.

**Case A: u is a final endpoint.** Its original module cannot be positive:
that module would have an original endpoint neighbor of u outside Q,
but both such sites (1,2),(2,1) belong to the fixed positive module.
It cannot be a rotor by the complete rotor gate barrier from the preceding
note. If it belongs to a minus-one module, the same outside-neighbor
argument forces u into C_i. Assign this side the endpoint u. It lies
inside Q and is not an irregular tail.

**Case B: u is not a final endpoint.** It cannot be selected because it
touches (1,2) and (2,1); hence it is finally blank and was originally
blank in every module. Since the side is marked, either v or z is a final
endpoint. If v is an endpoint, x cannot remain selected: it would touch
both p and v. Thus at least one of x,z is a final endpoint.

Let t be such an endpoint. It cannot belong to a positive module, since
blank-corner continuation at t with blank u would force p, respectively
q, into that foreign module's endpoint set. It cannot belong to a rotor
by the rotor x/z barrier with u blank. The continuation-only property
in Section 3 excludes EVERY minus-one endpoint, including its tips:
at x it forces p=(3,1) into the foreign endpoint set, and at z it forces
q=(1,3) there. Both contradict original endpoint disjointness. Case B is
impossible. No marked side needs a terminal-tip witness.

The reflected right pattern has the identical proof. Every assignment
lies in its positive side's original physical donor tile Q. Section 2
makes these tiles distinct even for marked sides, so no assigned endpoint
is reused by two sides. This is where survival-only donor distinctness
would have been insufficient. Since C_i lies in an original full bar
tile, an assigned gate makes all of Q foreign endpoints. Conversely a
gate endpoint raises the occupied degrees of both adjacent positive
protectors, marking the side. With a blank gate the same argument
excludes x,z endpoints, and feasibility then excludes v; the donor
survives. This proves exact donor-failure classification and G<=2B_minus.

## 5. One pool pays both kinds of demand

For each minus-one module use the four endpoint slots C_i union F_i.
All irregular minus-one events use distinct slots of F_i. All G marked
sides have different assigned slots in C_i by Section 4. The two allocations
are therefore disjoint, including within a single minus-one module.
Original endpoint disjointness separates pools of different modules.
This proves (4).

Each negative rotor has at most four irregular events, from its four
1P1T tiles. Zero-charge rotors and positive two-leg modules have no
irregular events. Adding these distinct rotor-tail events proves (1).
The previous regular-tile proof already paid K_regular out of each
physical full tile's two correction units. Only its unused remainder
C is carried forward. No full endpoint tile is counted as an actual
endpoint-free donor.

Use the established dual-guard budget and S=B_minus+2R_minus:

    sigma >= N+S+C-K_irregular-G
          >= N+B_minus+2R_minus+C-4B_minus-4R_minus
           = N-3B_minus-2R_minus+C.

This proves (2) and (3). In particular the same tip is never used once
to incur an irregular tax and again to pay a side loss. The sharper
classification G<=2B_minus and the distinct two-tip pool give (4)
directly, without a second spending of S.

For B_minus=0 this recovers the preceding arbitrary-rotor budget.
For B_minus=R_minus=0 it gives sigma>=N+C. When (3) holds, coefficient
one improves the existing |T|+(5/6)|M|<=mn/2 estimate by |M|/6;
any positive right side of (2) is additional guaranteed slack. It is
still a result for this module class, not an unrestricted coloring bound.

## 6. An explicit feasible loss of both positive donors

Use one U(14,4,4) translated by (6,6). Add six U(6,4,4) modules:

| Symmetry | Translation |
|---|---|
| identity | (8,7) |
| identity | (8,13) |
| (r,c) -> (-r,c) | (15,1) |
| (r,c) -> (-r,c) | (15,19) |
| (r,c) -> (-r,c) | (17,7) |
| (r,c) -> (-r,c) | (17,13) |

Translate the whole union by (-6,0) into a 12-by-28 rectangle. The first
module has charge +1 and the other six have charge -1. Direct substitution
into the U constructor verifies disjoint endpoint sets and that every
retained support has only its own persistent endpoint anchor. The positive
gates (2,8),(2,19) are upper bar corners of the first and second negative
modules. Both old donor tiles become full foreign endpoint tiles. Thus

    N=1, B_minus=6, R_minus=0, G=2,
    J=K_regular=K_irregular=0, rho_final=-5,
    |P|=142, |M|=71, |T|=28,
    sigma=69, finer_budget=N+S+C-K_irregular-G=5.

This refutes extension of automatic G=0 to minus-one modules. It does
NOT refute compensation: the exact finer budget is positive. The density
condition (3) fails here although compensation holds, demonstrating that
this sufficient criterion is not necessary. The construction is feasible;
no complete-freezing claim is made.

## 7. Verification, limitations and next target

Run

    python3 develop/check_minus_one_joint_compensation.py --output output/minus-one-joint-compensation-controls.json

The saved controls check all 64 oriented seven-core overlaps, 224
minus-one boundary images including unequal and long legs, and twenty-one
complete physical fusions: positive/minus-one zigzags, mixed rotor-star
chains, actual degree-four zero-rotor chains, nonhereditary four-way
fusions, and Section 6's two actual marked sides. None has an irregular
minus-one tip event; sharpness of the four-slot bound is not asserted.
A finite SAT search found the seven-module witness, then independently
reconstructed by the physical checker. A separate 24-by-28 SAT search
forcing an irregular tip event with at most eight modules was UNSAT.
That exclusion covers only its fixed seed, window and small library,
not arbitrary parameters or larger fusions. Neither SAT result is a
premise of the general proofs in Sections 2-5.

formal/SubQuorum/MinusOneJointCompensation.lean checks the finite ring
packing interfaces, tip/gate exclusion and disjoint four-slot capacity,
and the scalar budget implications. Its compilation, axiom audit and
exact scope are recorded separately. All fourteen declarations and
individual axiom audits pass under local Lean 4.33.0; only standard
propext/Quot.sound occur, with no sorryAx/native_decide. Global module classification,
coordinate adapters and the assignment of actual marked sides to slots
remain written proofs.

The fourteen additional declarations in formal/SubQuorum/MinusOneGateWitness.lean
kernel-check the actual seven-module example: all original charges and
source feasibility, actual matching and distinct endpoints, complete final
selected feasibility, rectangle containment, 142/71/28 counts, zero
intratile new-neighbor defect, zero new full tiles, both original unit
donor profiles, their full consumption, final receiver charge -5 and
actual slack69. Its separate compilation and individual axiom audit pass,
with no sorryAx/native_decide. Together the two sources have 28 checked
declarations. This does not assert complete freezing or formalize the
all-parameter module adapter. No prior Oracle verdict covers this extension.

Next determine whether feasible fusions in this phase class can have
irregular-tip demands, and whether the geometry forces
the full residual inequality K_irregular+G<=N+S+C even below (3).
If a candidate sharper rule fails, give a feasible physical witness and
distinguish failure of that rule from failure of the target. Finite pair
searches cannot classify the pairs inside larger feasible unions.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
