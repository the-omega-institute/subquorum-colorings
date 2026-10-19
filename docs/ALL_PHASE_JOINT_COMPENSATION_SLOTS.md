# Single-use joint compensation slots in every two-leg phase

20 October 2026. We extend the joint corner/tip witness theorem from
positive and charge-minus-one U modules to ALL four source phases, with
arbitrary-phase rotors. The new ingredient is a complete boundary
classification for the two row-shifted phases and a shared slot rule:
an upper bar corner used to witness a marked side cannot simultaneously
incur its irregular event. The density criterion below is sufficient;
unrestricted residual payment and arbitrary grid decomposition remain open.

## 1. Hypotheses, notation and theorem

Use the COMPLETE U(w,a,b) constructor, matching and original supports in
MINUS_ONE_TIP_EVENTS_AND_LOCAL_OVERLOAD.md, with even w>=6 and independently
even a,b>=4. Arbitrary translated, reflected and transposed copies and
the standard eight-endpoint rotor are allowed. Endpoint sets of original
modules are pairwise disjoint; every original endpoint has occupied degree
three and every original selection a unique original endpoint anchor.
Retain the union of all supports except those becoming endpoints, and
require the complete final union to be feasible. Optional selections are
outside all original receivers and have no endpoint neighbor.

There is no prescribed contact graph, pair-feasibility, port, freezing or
final-degree-three assumption. The physical tiling is fixed. Transport it
back to each constructor to identify its effective source phase (s,t).
Equivalently use U shifted by (s,t), followed by a tiling-preserving
isometry. The all-phase charge and event catalogue is already established
in REGULAR_TILES_ZERO_ROTORS_AND_IRREGULAR_TAX.md.

Write N for the positive phase-(0,0) U count, B01,B10,B11 for the other
three U counts, and Rminus for charge-minus-two rotors. Widths may differ.
Let

    S = B01 + sum_phase10(w_i-1) + sum_phase11(w_i-1) + 2Rminus.

Thus sum of original charges is N-S. Keep ORIGINAL event ownership,
K=Kregular+Kirregular, J new aligned mixed-owner all-endpoint tiles,
C=2J-Kregular>=0, and G the number of marked canonical positive sides.
A marked side is counted once even when its donor survives. The established
dual-guard and regular-tile ledgers give

    sigma := mn/2-|T|-|M| >= N+S+C-Kirregular-G.       (1)

**All-phase joint-slot theorem.** Under these hypotheses,

    Kirregular+G <= 2S+2B01+2B10,                      (2)
    sigma >= N-S-2B01-2B10+C.                         (3)

Consequently

    N+C >= S+2B01+2B10                                (4)

is sufficient for |T|+|M|<=mn/2. Its width-expanded form is

    N+C >= 3B01 + sum_phase10(w_i+1)
                    + sum_phase11(w_i-1) + 2Rminus.   (5)

No leg height occurs in this condition. The contact-independent density
condition obtained by dropping C is also sufficient. Neither necessity
nor sharpness of the coefficients is claimed. With B10=B11=0, (2)-(3)
recover the previous minus-one theorem exactly.

## 2. Complete all-parameter boundary catalogue

In reference coordinates AFTER the phase shift, define the two upper
bar corners and two terminal tips by

    A={(s,1+t),(s,w+t)},
    F={(a+s,1+t),(b+s,w+t)}.

For each original endpoint p, call it an exterior exception if it has no
original endpoint neighbor OUTSIDE its physical tile. Call p a continuation
exception if some adjacent intratile ORIGINAL blank v has other intratile
neighbor u such that 2p-u is not an original endpoint. Let E be the first
exception set, X the second. Let I be the endpoints with an adjacent
intratile original blank and irregular receiver profile (1P1T or 2P0T).
Every irregular event uses one distinct endpoint in I, since its original
occupied degree is three.

The complete catalogue is

| Source phase | rho | E | X | I size | Joint pool |
|---|---:|---|---|---:|---|
| (0,0) | 1 | empty | empty | 0 | empty |
| (0,1) | -1 | A | empty | 2 | I union A, size 4 |
| (1,0) | 1-w | F | empty | 2w-2 | I union F, size 2w |
| (1,1) | 1-w | F | A union F | 2w-4 | I union F, size 2w-2 |

For (0,1), I consists of the tips. For (1,1), A is a subset of I,
whereas F is disjoint from I. In (1,0), F is disjoint from I too.
The tips in the two row-shifted phases have regular 2P1T profiles;
they need separate slots when used for marked-side costs.

Here is a direct proof valid for all dimensions. In the unshifted bar
a point has consecutive horizontal endpoint neighbors until a bar end;
there are two bar rows. The paired stem has consecutive vertical endpoint
neighbors until its terminal tip. Checking whether a physical tile boundary
lies between each of these consecutive pairs gives E: no exceptions in
(0,0), the upper corners in (0,1), and the final tips in (1,0),(1,1).
A nonterminal stem endpoint has an endpoint on the reflected side of
its intratile neighbor. A bar interior has the analogous horizontal
continuation. Lower bar corners continue into the upper row or first
stem segment. Thus a continuation failure can occur only at an upper
bar corner or terminal tip.

In phases (0,0),(0,1), the full bar or two-selection corner profile either
has no adjacent intratile blank or continues to the next bar/leg endpoint.
For (1,0), an upper corner's other intratile neighbor is its outward
selection, and reflection continues into the bar; its terminal tip has
no adjacent intratile blank. In (1,1), the upper corner's reflection is
the outward selection rather than an endpoint. At a terminal tip the
other intratile neighbor is the preceding stem endpoint, whose reflection
is the beyond-tip selection. These are exactly A union F, proving X.
The existing exact receiver-profile counts give |I|. In phase (1,1)
the upper corners lie in the 2P0T bar tiles, while the two tips lie in
regular 2P1T tiles; the claimed inclusions and pool sizes follow.
Additional bar length and leg height insert only ordinary interior pairs.
All statements are invariant under tiling-preserving isometries.

## 3. A marked side gets a distinct endpoint slot

All 2N ORIGINAL canonical donor tiles are distinct, including those later
lost. The proof from MINUS_ONE_JOINT_WITNESS_COMPENSATION.md applies
unchanged: each such tile has seven original positive endpoints in its
twelve-site outer ring; two owners would overlap. Within one positive
module its two canonical tiles are distinct for w>=6.

Normalize any positive left side as

    Q={2,3}x{2,3},
    gate u=(2,2), old selection x=(3,2),
    opposite z=(2,3), y=(3,3),
    old anchor p=(3,1), guard q=(1,3).

The canonical protectors have old blank neighbors u, v=(4,2), z.
Every new occupied old blank adjacent to an old endpoint is a foreign
endpoint, by persistent occupancy and final selected feasibility.

If the side is marked and u is an endpoint, let its original owner be i.
It cannot have an original endpoint neighbor outside Q: the two possible
sites (1,2),(2,1) are positive endpoints of the fixed owner. Thus u belongs
to E_i. The complete rotor gate barrier excludes a rotor owner. Section 2
then permits only a phase-(0,1) upper corner or a row-shifted terminal tip.
Assign the side the slot u.

If u is not an endpoint, it cannot be selected because both displayed
outside positive neighbors persist. Therefore u is finally blank, and was
originally blank in EVERY source. A marked side has v or z an endpoint.
If v is an endpoint, x cannot remain selected, because p and v would both
be its occupied neighbors. Thus at least one of x,z is an endpoint.
Choose one, denoted t, and its original owner i. If t had continuation
across the other intratile neighbor, the original endpoint 2t-other
would be p or q. Those belong to the fixed positive owner. Therefore
t belongs to X_i. The rotor x/z barrier with blank gate again excludes
a rotor. Section 2 forces source phase (1,1), with t in A_i union F_i.
Assign t to this side.

The rotor barrier used here is the established complete source-role proof:
quarter-turn invariance leaves two rotor translation classes, with eight
endpoint roles each; at the gate every role overlaps the positive endpoint
core, and at x/z every role overlaps it or occupies u. It is not a bounded
translation search and covers arbitrary rotor phases.

Every assigned endpoint lies in its side's ORIGINAL donor tile Q.
Distinct old canonical tiles therefore give distinct assigned endpoints,
even if sources merge or a single foreign module witnesses several sides.
Each assigned endpoint lies in its original module's joint pool.

## 4. No slot is used for both an irregular event and a side loss

For (0,1) the assigned gate slots are A and irregular slots are F; they
are disjoint. For (1,0) all marked slots are terminal tips F, outside I.
For (1,1), an assignment at a terminal tip also lies outside I.

The only possible overlap of the two candidate pools is a phase-(1,1)
UPPER bar corner. Such a corner is not in E, so Section 3 can assign it
only in the BLANK-GATE case. Its adjacent intratile original blank is
exactly that gate u. Original occupied degree three leaves only this one
blank neighbor. Since u remains blank, this corner incurs NO irregular
event. Consequently actual side assignments and actual irregular tails
are disjoint even in this shared candidate pool.

Rotors have no side assignments; negative rotors supply their four
irregular endpoint slots, and zero-charge rotors supply none. Endpoint
disjointness separates the pools of different original modules. No
endpoint, donor side or physical correction unit is used twice.

Summing the exact pool sizes gives

    4B01 + sum_phase10(2w_i) + sum_phase11(2w_i-2) + 4Rminus
       = 2S+2B01+2B10.

The injective side assignments and irregular tails fit disjointly into
these slots, proving (2). Insert (2) into (1) to get (3), and (4)-(5)
follow. Regular costs were already paid once from their own full tile's
two correction units; only the unused C enters this calculation.

## 5. Actual row-shifted gate losses and the limit of the theorem

The previously proved opposed-band family already shows why the new
terminal-tip slots are necessary. In its standard width-six phase there
is one positive U module and one phase-(1,1) U module of charge -5,
with G=2, B01=0, J=Kregular=Kirregular=C=0. The two marked gates are
tips of the negative module. Every endpoint is frozen. Thus extending
G<=2B01 or the assertion that every consumed gate belongs to an original
full foreign bar tile to all source phases is FALSE.

This is a new use of the existing opposed-band construction, not a new
claim about that family's origin. Its finer budget is N+S-G=4. In the
original 8-by-10 rectangle it has 44 endpoints, 22 matching edges and
12 selections, hence actual slack 6. The checker also tests an even
translation into a padded 10-by-12 rectangle with slack 26; this changes
the ambient deficit, not the source slots or finer budget. The new
sufficient lower bound (3) is -4 there:
the criterion is not necessary and must not be presented as automatic
compensation for every admissible fusion. The fully frozen zero-credit
tip family from the preceding note supplies a different obstruction to
pure-C payment; both reinforce the need for a finer joint allocation.

When (4) holds, coefficient one improves
|T|+(5/6)|M|<=mn/2 by |M|/6. Any positive right side of (3) is further
guaranteed slack. This remains a theorem for the stated complete source
fusion class, with its explicit density condition, rather than a theorem
about every grid configuration or the proposed triple equality.

## 6. Verification and remaining question

Run

    python3 develop/check_all_phase_joint_slots.py \
      --output output/all-phase-joint-slot-controls.json

The checker verifies the catalogue on 896 oriented source images,
including unequal and long legs, and checks 512 complete physical images.
Sixteen physical images have marked sides assigned to row-shifted sources.
Every actual side assignment is distinct and disjoint from actual irregular
events, and the exact pool sum and scalar lower bound are checked separately.
These controls support, but do not replace, Sections 2-4's all-parameter proof.

The accompanying Std-only Lean module checks concrete source coordinates
in all four phases, their exception sets, irregular/pool counts and the
abstract single-use accounting and sufficient-density arithmetic. Its
scope is recorded separately in output/all-phase-joint-slot-formal-check.json;
the general geometric adapter and arbitrary-fusion injection remain written.
The preceding review of the zero-credit tip family does not cover this
later all-phase extension.

The next question remains whether the ACTUAL demand Kirregular+G can be
paid from N+S+C in every admissible fusion, without first replacing it by
the worst-case slot capacity. If not, an actual feasible witness should
separate failure of that sufficient rule from failure of sigma>=0.
The all-phase pool theorem identifies every local source slot such a
proof or obstruction must handle.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
