# Regular tiles, rotor barriers and height-independent residual tax

20 October 2026. We extend automatic compensation from positive two-leg
modules to zero-charge rotors, prove donor preservation in the presence of
rotors of ANY phase, and localize the remaining intratile tax for all phases.
All fusions use Section 8 of DEGREE_THREE_FUSION_AND_PROTECTED_DONORS.md:
the original modules have occupied endpoint degree exactly three, pairwise
disjoint endpoint sets and their original matching edges. Retain the union
of original selections except sites becoming endpoints, and require this
complete final retained-support fusion to be feasible. Optional extra
selections are outside all original receiver tiles and have no endpoint
neighbor. No pair-feasibility, port, forest, freezing or final-degree-three
assumption is made.

## 1. Statements

A receiver tile profile is REGULAR if it has one of the following forms:

    one endpoint, its two adjacent corners selected;
    two adjacent endpoints, one remaining corner selected;
    three endpoints, no selections;
    four endpoints, no selections.

All unlisted corners are blank. There are seventeen oriented profiles.
The two IRREGULAR profiles occurring in this module family are one endpoint
with one adjacent selection, and two adjacent endpoints with no selections.

Partition K=K_regular+K_irregular by the original tail's RECEIVER TILE
profile, keeping its original module ownership after components merge.
Write N for the number of positive two-leg modules, S=N-sum_i rho_i, and
G for the total marked canonical left/right sides. Let H count two-leg
modules whose effective source phase is (1,1). Then the following hold.

**Regular-tile theorem.** For arbitrary-phase two-leg/rotor fusions,

    K_regular <= 2J,
    C_regular := 2J-K_regular >= 0,
    K_irregular <= 2S-2H,
    sigma >= N+S+C_regular-K_irregular-G
          >= N-S+2H+C_regular-G.                  (1)

In particular the still-conditional residual payment test is
K_irregular+G<=N+S+C_regular. The geometric tax bound 2S-2H is independent
of both leg heights. The theorem does not assert the residual test always
holds, and its coarser last inequality need not be sharp.

**Rotor barrier theorem.** If all two-leg modules have positive phase, then
arbitrary rotors, in ANY phase, preserve both canonical donors of every
positive module. Thus G=0 and D>=2N.

If all rotors have charge zero, every source tile is regular and S=0.
Consequently the complete arbitrary-contact class satisfies

    G=0, D>=2N, K<=2J, rho_final=N-2J+K,
    sigma>=N+2J-K>=N.                             (2)

More generally, let R_minus count charge-minus-two rotors, while all other
rotors have charge zero and all two-leg modules are positive. Then

    sigma >= N+2R_minus+C_regular-K_irregular
          >= N-2R_minus+C_regular.                (3)

Thus N>=2R_minus is an explicit sufficient condition independent of the
contact graph. Equation (3) retains the actual event count when available.

Here sigma=mn/2-|T|-|M| for the even-by-even ambient rectangle. Thus (2)
gives |T|+|M|<=mn/2-N for its complete module class. Compared with the
existing |T|+(5/6)|M|<=mn/2 estimate, the coefficient-one bound gains
|M|/6 and the new guaranteed slack contributes a further N. With arbitrary
rotor phases, (3) gives |T|+|M|<=mn/2-N+2R_minus-C_regular. These are
bounds for the stated fusion classes; their existence does not establish
that all configurations relevant to the unrestricted grid problem belong
to those classes.

## 2. Regular events force full tiles, with capacity two

For a one-endpoint/two-selection profile there is no adjacent intratile
blank. A full original tile has none. In a two-endpoint/one-selection
profile, an event fills its blank corner with a foreign endpoint. Its
original selection would then touch two endpoints, so it too is consumed;
the tile is full and mixed. Exactly one old tail can contribute there.

In a three-endpoint/no-selection profile the only blank corner is adjacent
to two original endpoints. If newly occupied, it must be a foreign endpoint
and the tile becomes full and mixed. Both adjacent old tails contribute,
so this profile contributes at most two events and uses three original
endpoints. The implication that a newly occupied old blank adjacent to an
old endpoint is a foreign endpoint is the established persistent-anchor
lemma; optional selections do not touch endpoints.

Assign each regular-source event to its own full physical tile. Endpoint
groups of different original modules are disjoint. The only partitions of
four original endpoints, with their regular event capacities, are

| Original endpoint partition | Sum of regular capacities |
|---|---:|
| 4 | 0 |
| 3+1 | at most 2 |
| 2+2 | at most 2 |
| 2+1+1 | at most 1 |
| 1+1+1+1 | 0 |

An irregular group can be present, but its events are excluded from this
sum. A singleton group has no regular event. Thus even in the presence of
irregular groups the regular events use at most two units per new full
tile. This proves K_regular<=2J. Set C_regular equal to what remains AFTER
that payment. No full endpoint tile is also counted as an actual donor.

## 3. The complete phase catalogue and the residual bound

Put n=(a+b)/2. Counting the bar, paired stem and final tip tiles gives the
following exhaustive reference-phase catalogue. Transport the physical
tiling back to the original constructor to define each effective source
phase, including reflected or transposed modules.

| Module/phase | Receiver profiles and counts | rho | Maximum irregular tails |
|---|---|---:|---:|
| Two-leg (0,0) | 4P: (w-2)/2; 2P1T: n; 1P2T: 2 | 1 | 0 |
| Two-leg (0,1) | 4P: w/2; 2P1T: n-2; 1P1T: 2 | -1 | 2 |
| Two-leg (1,0) | 2P0T: w-2; 2P1T: n; 1P1T: 2 | 1-w | 2w-2 |
| Two-leg (1,1) | 2P0T: w-2; 2P1T: n-2; 3P0T: 2 | 1-w | 2w-4 |
| Rotor (0,0) | 4P: 1; 1P1T: 4 | -2 | 4 |
| Rotor (0,1) or (1,0) | 1P2T: 2; 3P0T: 2 | 0 | 0 |
| Rotor (1,1) | 2P1T: 4 | 0 | 0 |

For the two-leg catalogue, the unshifted bar interior is a row of full
tiles and each stem is paired until its final even tip. A column shift
combines the two bar ends into full bar tiles, moves one selection outside
each tip tile, and leaves n-2 paired-stem tiles. A row shift separates the
two bar rows: their interior horizontal endpoint pairs produce w-2 tiles
of type 2P0T. With no column shift there are two one-endpoint bar-end tiles
and n paired-stem tiles. With a column shift the two lower bar ends each
include the first leg endpoint, giving 3P0T, and n-2 paired-stem tiles.
These lists exhaust the endpoints. Independent heights change only n.

For the rotor, its central four endpoints and four ports give the stated
tiles directly from the fixed coordinate lists in Section 4. In particular
zero-charge rotors have only regular tiles, including the previously absent
three-endpoint profile. Some ports fail exterior endpoint support, so that
positive-two-leg boundary property cannot simply be assumed for rotors.

An irregular 1P1T tile has exactly one blank adjacent to its endpoint, so
at most one irregular tail. A 2P0T tile has one blank adjacent to each
endpoint, so at most two. These are counts of distinct original tails.
The last column follows and is independent of height.

Each nonpositive module contributes -rho_i to S. Comparing its last column
with twice this contribution gives equality in every row except source
phase (1,1), which has two units to spare. Positive modules contribute zero
to both sides. Summing proves K_irregular<=2S-2H. Substituting
K=K_regular+K_irregular into the preceding dual-guard theorem proves (1).

## 4. A fixed rotor barrier, for every orientation and translation

Normalize the positive left donor tile with

    u=(2,2), x=(3,2), z=(2,3), y=(3,3).

Every positive two-leg module contains the following fixed endpoint core,
regardless of its width and independent leg heights:

    B = {0,1} x {1,2,3,4,5,6} union {(2,1),(3,1),(4,1)}.

Here is a complete placement lemma for any affine copy R of the rotor:

    u in P_R implies P_R intersects B;
    x in P_R implies P_R intersects B or u in O_R;
    z in P_R implies P_R intersects B or u in O_R. (4)

To prove it for ALL placements, use the actual rotor lists

    E={(1,2),(2,2),(2,3),(2,4),(3,1),(3,2),(3,3),(4,3)},
    T={(0,2),(1,1),(2,5),(1,4),(5,3),(4,4),(3,0),(4,1)}.

They are invariant under the quarter turn (r,c)->(c,5-r). Thus every affine
grid image is a translate of (E,T) or its reflection (r,c)->(r,-c), denoted
R+ and R-. For a target v, choosing its original endpoint role e determines
the translation EXACTLY: v-e. The following table exhausts the sixteen
roles. Each coordinate is an actual endpoint in B after that translation;
"u occupied" means the translated original occupied set contains u.

| Template/source endpoint | Target u: blocker | Target x: blocker or alternative | Target z: blocker or alternative |
|---|---|---|---|
| R+ (1,2) | (4,1) | u occupied | u occupied |
| R+ (2,2) | (1,2) | (4,1) | (1,3) |
| R+ (2,3) | (1,1) | (2,1) | (1,2) |
| R+ (2,4) | (2,1) | (3,1) | (1,1) |
| R+ (3,1) | (0,3) | (1,3) | (0,4) |
| R+ (3,2) | (0,2) | (1,2) | (0,3) |
| R+ (3,3) | (0,1) | (1,1) | (0,2) |
| R+ (4,3) | (0,1) | (0,1) | (0,2) |
| R- (1,-2) | (3,1) | (4,1) | (3,1) |
| R- (2,-2) | (1,2) | (3,1) | (1,3) |
| R- (2,-3) | (1,3) | (3,1) | (1,4) |
| R- (2,-4) | (1,4) | u occupied | (1,5) |
| R- (3,-1) | (0,1) | (1,1) | (0,2) |
| R- (3,-2) | (0,2) | (1,2) | (0,3) |
| R- (3,-3) | (0,3) | (1,3) | (0,4) |
| R- (4,-3) | (0,1) | (0,3) | (0,2) |

Every entry follows by adding target-source to the displayed E,T lists.
This is a complete finite orbit classification, not a bounded search over
translations or parameters: the role equation accounts for every possible
translation and the quarter-turn symmetry accounts for every orientation.
It proves (4), with the same fixed B in every allowed positive module.

## 5. Donor survival with arbitrary rotors, and automatic zero-rotor compensation

Suppose all two-leg modules are positive, while rotor phases are arbitrary.
The old gate u cannot be a foreign endpoint of a positive two-leg module,
by its exterior endpoint property and the original endpoints at (1,2),(2,1).
It cannot be a rotor endpoint by the first implication in (4). It cannot
be selected since it sees those two old endpoints. Thus u is finally blank,
and persistence makes it originally blank in every foreign module.

Consumption of x by a positive module contradicts blank-corner continuation,
as in the preceding positive-phase proof. Consumption by a rotor contradicts
the second implication of (4): endpoint disjointness excludes its blocker,
and final blankness excludes original occupancy at u. Thus x survives as
selected. Its other neighbors y and (4,2) stay blank by feasibility.

The positive-module continuation property and the last implication in (4)
likewise exclude any endpoint at z. A foreign selection at z would touch
its own persistent anchor and the old endpoint q=(1,3); optional selections
cannot touch q. Thus z stays blank. All three protecting blank sites stay
blank, and this side is unmarked with an actual unit donor. Reflect to get
the right side. Distinct donors cannot coincide by the retained-anchor
injection. Hence G=0,D>=2N for arbitrary rotor phases.

For zero-charge rotors all source tiles are regular, so K<=2J and the
original total charge is N. The exact ledger proves (2). With R_minus
negative rotors, S=2R_minus and at most 4R_minus irregular tails remain.
This gives (3). All full-tile credit and actual donor units stay separate.

## 6. An actual degree-four chain at every length

For k>=1 place rotor i at translation (2i,2i+1), for 0<=i<k, in the
(2k+4)-by-(2k+6) rectangle. Each original rotor has effective phase (0,1)
and charge zero. The original endpoint sets are disjoint and connected
through consecutive modules. For the first consecutive pair the complete
foreign endpoint contacts and the new-neighbor tails are

| Contact | New-neighbor tail |
|---|---|
| (2,5)--(3,5) | (2,5) in rotor 0 |
| (3,4)--(3,5) | (3,4) in rotor 0 |
| (4,4)--(4,5) | (4,5) in rotor 1 |
| (4,4)--(5,4) | (5,4) in rotor 1 |

The pair consumes exactly rotor 0's supports (4,5),(5,4) and rotor 1's
supports (2,5),(3,4). Its twelve retained selections are

    (0,3),(1,2),(1,5),(2,6),(3,1),(3,7),
    (4,2),(4,8),(5,3),(6,4),(6,7),(7,6).

Substitution into the displayed E,T lists shows each sees only its own
persistent anchor. Its new full tiles are (1,2) and (2,2), as tile indices.
All consecutive-pair data are their even translations by (2i,2i). Rotors
two positions apart have no common occupied site or adjacent occupied sites,
again by the explicit lists. For larger separation their occupied bounding
boxes are separated in both coordinates, giving Manhattan distance at least
two. Hence there are no further interactions.

For completeness, pair feasibility is SUFFICIENT here. A globally retained
selection of rotor i is retained in every pair containing i. Each such pair
permits no occupied neighbor beyond its own persistent anchor. Taking the
union therefore introduces no new neighbor at that selection. This does
not assume the false converse that every feasible fusion has feasible pairs.

An interior rotor receives its two previous-interface new-neighbor events
at source roles (2,2),(3,1), and its two next-interface events at source
roles (2,4),(3,3). They are distinct. The support consumption sets at its
two interfaces are also disjoint. It follows for every k that

    |P|=8k, |M|=4k, |T|=4k+4,
    |R|=2k+2, t_R=4,
    d4=K_regular=4(k-1), J=2(k-1),
    K_irregular=0, rho_final=0.

The receiver count uses two shared tiles at each interface and none at
larger separations. The retained receiver-selection count follows either
from the four displayed consumptions or the exact incidence ledger with
four intratile foreign edges per interface. This is an all-length
degree-four example with equality in K_regular<=2J. No complete freezing
claim is made: the ordered routine certifies ten of sixteen endpoints in
the k=2 control, which is insufficient to assert full freezing.

## 7. What is still unresolved

For arbitrary-phase two-leg modules, the remaining tax is now concentrated
on 1P1T tips/bar ends and unselected 2P0T bar tiles. Long regular stem regions
cannot create unpaid intratile tax, including the zero-charge rotor phases.
The remaining problem is the COUPLING between irregular events and marked
positive sides, rather than a separate worst-case bound for each.

The rotor barrier is relative to an old positive endpoint core. If negative
two-leg modules can fill its gate, other modules can participate in consuming
its donor. We do not charge each affected side injectively to a negative
module without a proof, and do not assume a negative module's S unit can pay
both its irregular event and a donor loss independently. General decomposition,
the unrestricted grid bound, triple equality and external priority remain open.

## 8. Verification and review scope

Run the physical controls with

    python3 develop/check_regular_tile_compensation.py --output output/regular-tile-compensation-controls.json

The saved run passes 112 phase-catalogue cases, all 48 fixed rotor target/role
cases, 296 mixed physical fusions and seven zero-rotor chains of lengths
1,2,3,4,8,16,32. Of the fusion/chain controls, 154 have actual regular-source
events. The chains demonstrate nonzero degree-four defects growing without
bound, with equality in their full-tile cancellation. They are feasible;
complete freezing is not asserted. These computations check the written
all-parameter proofs in Sections 2-6, rather than replacing them.

The 22 declarations in formal/SubQuorum/RegularTileCompensation.lean and
their individual axiom audits pass under local Lean 4.33.0. The scope is
the complete fixed rotor orbit barriers and translation adapter, all
seventeen regular profiles and final masks, four-corner owner partitions,
twelve irregular profiles and capacities, and the scalar phase potentials,
budgets and chain cancellation. Only standard propext and Quot.sound occur;
there is no sorryAx or native_decide. The all-parameter geometric catalogue,
arbitrary global coordinate adapters, distinct donor selection, global
event assignment and chain geometry remain written proofs. See
output/regular-tile-compensation-formal-check.json for the precise scope.

The previous all-positive two-leg theorem's independent review completed
ACCEPT, but does not cover the present extensions. This note has a separate
same-conversation review cd57f384-c7e4-4dc9-bb68-7849b67e4ee8, original
stream execution 64375. At this checkpoint it is live with no verdict;
preserve that task and stream. Its actual status is tracked in
output/regular-tile-compensation-review-live.json.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
