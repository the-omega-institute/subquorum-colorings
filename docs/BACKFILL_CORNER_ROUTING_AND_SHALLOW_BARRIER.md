# Backfill corners route into four source roles, with strict barrier drops

20 October2026. In the COMPLETE finite original U/rotor model, the first
forced corner of a critical U10 backfill has no rotor owner. Its U owner
has exactly one of four roles below. Complete source bars give strict
dimension drops, excluding shallow U10 roots when the companion's opposite
leg is no longer than the root width. The phase01 branch also reserves a
distinct singleton in the EXISTING cap/pair pool. These are general source
geometry and simultaneous reservation statements. The unrestricted
coefficient-one allocation and rectangular-grid triple equality remain OPEN.

## 1. Complete-source hypotheses and the two barriers

Use ALL hypotheses of
[the critical U10 backfill theorem](CRITICAL_PHASE10_BACKFILL_AND_RECEIVER_SEPARATION.md):
complete original U/rotor sources, even U width at least6 and independent
even heights at least4, original endpoint uniqueness, unchanged matchings,
mandatory support retention, retained-support occupied degree at most one
and the FIXED transported physical partition. Original owners may recur.

Normalize the critical root to t=(0,0), frame(N,E). Let G be its U10
original owner, of width u and incident height g. Let F be its U11
companion, of width v and opposite-terminal incident height h. The actual
backfill tile is Qb={0,1}x{-2,-1}; write q=(1,-1), r=(1,-2).
The preceding theorem proves that Qb is full, that q,r belong to neither
F nor G, and that all Qb are different and avoid ALL ordinary and critical
receiving tiles. In particular q has an actual original owner H.

Reflect canonical U labels, if needed, to describe G by its right terminal
and F by its first terminal. This only swaps the two independent canonical
height labels and preserves endpoint/support sets and the physical partition.
Complete original geometry supplies the following endpoint barriers:

    F: (0,c), -h-1<=c<=-1;
       (row,-h-1),(row,-h), 0<=row<=v-1.

    G: (row,0), 0<=row<=g;
       (g-1,c),(g,c), 1-u<=c<=0.                    (1)

Only these subsets of F,G are used below. They are actual complete run/bar
subsets; the unlisted opposite stems need not have equal heights. Every
endpoint of H must avoid (1), because H differs from F and G. These
barriers imply in particular that H avoids north and east of q.

## 2. Rotor exclusion and the exact U routing table

A central rotor point has three original endpoint neighbors and cannot
occupy q with its north and east neighbors foreign. For the rotor tip
roles, use the minimum original blocker stencil

    {(0,-1),(0,-2),(0,-3),(0,-4)} union
    {(0,0),(1,0),(2,0),(3,0)}.                      (2)

Both parts follow from h>=4 and g>=4. Quarter-turn invariance reduces
arbitrary rotor placements to two chiralities times eight anchored roles.
Every one of these16 roles meets (2). The exact finite catalogue in Lean
and the independent checker exhausts the fixed template, not a bounded
search over translations or source dimensions. Thus H is a U.

Split a U endpoint into bar/near-stem/far-stem roles and the eight signed
coordinate permutations. Avoiding north and east leaves only an upper
outer bar corner with its two inward directions west/south, a south
terminal, or a west terminal. Interior stem points have two opposite own
neighbors, and interior/lower bar points have at least three, so fail.
At a south or west terminal either direction for its remote bar initially
remains. The complete barriers eliminate the two wrong turns:

* A south terminal cannot have its bar open right. If its incident height
  is a and a+1>=g-1, its stem meets G at(g-1,-1). If a+1<g-1,
  its rightward bar contains(a,0), on G's stem.
* A west terminal cannot have its vertical bar extend up. If its incident
  height is a and a+1>=h, its run contains(1,-h), on F's bar.
  Otherwise its upper bar contains(0,-a), on F's horizontal run.

The remaining complete roles, exact ORIGINAL profiles in Qb, and necessary
dimension bounds are:

| Role of H at q | Effective phase | P_H intersect Qb | S_H intersect Qb | Necessary bound |
|---|---|---|---|---|
| A: upper-right corner of a horizontal bar, stems down | 11 | {q,r} | empty | a<=g-4; w<=h-2 |
| B: upper end of a vertical bar on columns-2,-1, arms left | 00, positive | {q,r} | {(0,-1)} | w<=g-2 |
| C: south-pointing terminal, bar below and to the left | 01 | {q} | {(0,-1)} | a<=g-4; w<=h-2 OR v<=a |
| D: west-pointing terminal, bar to the left and extending down | 10 | {q,r} | {(0,-1)} | a<=h-2; w<=g-2 OR u<=a |

Here w is H's canonical width. In A,C, a is its incident vertical height;
in D, a is its incident horizontal height. The other height is independent.
The phase/profile column comes from pairing these exact runs with the
transported tile Qb, whose physical origin is(0,-2). No phase is inferred
from a reset tiling. In A the horizontal bar occupies rows1,2 and columns
-w,...,-1. In B the vertical bar occupies columns-2,-1 and rows1,...,w.
In C the bar occupies rows a,a+1, ending in column-1. In D the vertical
bar occupies columns-a-1,-a and rows1,...,w.

For A,C, H owns(row,-1) for1<=row<=a+1. Avoiding G's bar gives
a+1<g-1. Both a,g are even, so a<=g-4. For B, the same collision with
its vertical bar gives w<g-1, hence w<=g-2. For D, avoiding F's bar
gives a+1<h, hence a<=h-2. If w>=g-1 and a<=u-1, its bar contains
(g-1,-a), which belongs to G's bar. This proves the last disjunction.
These arguments prove the table for arbitrary dimensions and source counts.

## 3. A general shallow occupied-band obstruction

If g is4 or6, roles A,C would require an even a>=4 to be at most2,
and B would require w>=6 to be at most4. Thus ONLY role D is possible.
Its width w>=6 also rules out w<=g-2, leaving

    u <= a <= h-2, hence h>=u+2.                   (3)

Consequently NO complete feasible critical U10 event can have

    g in{4,6} and h<=u.                            (4)

This excludes an all-parameter family, including arbitrarily large other
heights, widths, source counts and surrounding components. It is stronger
than the F/G barrier disjointness test alone: for g<=6 that test permits
h=u, while (4) does not. Exclusion uses the required original owner of q;
it is not an UNSAT extrapolation. Conversely (3) is only NECESSARY. This
note supplies no complete event attaining it and makes no realizability
or sharpness claim. In the remaining role D, its incident length is
strictly smaller than F's opposite leg. This is a geometric continuation
constraint, not by itself a global termination theorem.

There are two additional necessary bounds in the table: role A has
w<=h-2; role C has w<=h-2 OR v<=a. For A, w>=h would put(1,-h)
on both its horizontal bar and F's vertical bar. For C, the same collision
at(a,-h) occurs if w>=h and a<=v-1. Evenness of w and h turns w<h into
w<=h-2. These use F's full bar, rather than only its local terminal pair.

### The narrow equal-band case forces g>=12

Suppose u=h=6. Let b>=4 be G's OTHER original height, independent of g.
Its complete opposite stem gives another foreign barrier:

    (row,-5) in P_G for g-b<=row<=g.                (4a)

Role A is impossible, since it would require w>=6 and w<=h-2=4.
For C, w>=6=h makes the additional bound give a>=v>=6. Its lower bar
row contains(a+1,-5), since w>=6, while a+1<=g-3. Avoiding (4a) therefore
requires a+1<g-b; in particular g>=12.

For B, its bottom arm contains(w,-5) because its independent bottom
incident height is at least4. For D, a<=h-2=4 forces a=4, and its bar
likewise contains(w,-5). In both cases w<=g-2: this is the B bound, and
for D the alternative u<=a would assert6<=4. Avoiding (4a) now requires
w<g-b. Since w>=6 and b>=4, g>=11, and even g gives g>=12.

Thus no complete feasible critical U10 event has u=h=6 and g<=10,
for ANY independent opposite heights, companion width, number of sources
or surrounding fusion. This includes g=8,10, which the shallow theorem
alone leaves open. The threshold12 is necessary, not claimed sharp or
realizable. This strengthening uses the additional complete far stem;
its execution evidence and review scope must be distinguished from the
initial four-route review packet, which did not contain this subsection.

## 4. Actual singleton and cap reservations, without a second use

Let KC count role-C events. Their q points are different, since the
preceding backfill theorem gives distinct Qb. Every such q is an original
phase01 terminal-singleton occurrence. F supplies a foreign EXACT2P1T
profile in its tile. Therefore all these q lie in the existing E1reg
set of [the any-pair budget](DISTINCT_NEUTRAL_SUPPORTS_AND_ANY_PAIR_BUDGET.md).

Let T_old be the union of all ordinary and critical receiving tiles,
and define E1old=E1reg intersect T_old, interpreting T_old as vertex sets.
Backfill separation makes the new role-C q set disjoint from E1old.
It is also disjoint from E0 and from all negative cap-filler occurrences,
by the existing EXACT pair-versus-triple separation. Therefore the
simultaneous single-pool bound is

    2K11+|E0|+|E1old|+KC
      <=2K01+2K10+Fpos+U0.                        (5)

K01,K10,K11 in (5) are ORIGINAL SOURCE counts, not critical-event counts.
This retains the KC reservations together with the old selected subfamily,
instead of separately assigning the same singleton to both. The full
E1reg count in the older theorem already includes these endpoints; (5)
does not add KC to that full count and does not improve that scalar bound.

A role-A corner identifies the corresponding lower cap of its phase11 H:

    triple {(2,-2),(2,-1),(3,-1)}, missing corner(3,-2).           (6)

This is an actual original cap in the next physical tile. The map from
role-A events to these caps injects. A given cap determines its source
and corresponding upper outer corner q; distinct original triples cannot
share a physical tile, and q already identifies its backfill event. Thus
the unfilled such caps are a subfamily of EXISTING U0; filled ones use
the original negative singleton or positive activation cap pools. The
associated cap tiles are not claimed separate from other receiver families.
Adding their unfilled count to the already complete U0 would double count.

Role B identifies an upper outer corner of a positive source, rather than
an activated positive terminal. Distinct q give at most two such corners
per original positive source, so KB<=2N. These incidences are NOT new A
activations or an unused copy of the already committed2N capacity.
Role D uses one of the two original terminals of its phase10 owner,
with a strict incident drop; recurrence through other owners remains open.

## 5. Validation and unresolved compensation

The Lean companion checks the exhaustive normalized U endpoint role
classification, exact16-role rotor exclusion, both wrong-turn collision
arguments, the strict run/bar inequalities and shallow-band consequence.
These are normalized geometry statements with explicit original-owner
disjointness premises. Constructing the actual F/G barriers, source phases,
global q/cap injections and adapting (5) to the existing singleton pool
remain the written arguments above. This is not end-to-end formalization
of complete source fusions or of the unrestricted compensation theorem.

The checker samples arbitrary independent U heights and bar parameters,
verifies every surviving role/profile/bound, and explicitly includes the
new h=u shallow boundary cases and the stronger width-six g=8,10 exclusions.
Its U images and role examples are PARTIAL
source geometry, not complete feasible fusions; complete critical U10
witness coverage remains ZERO. The fixed rotor catalogue is exhaustive.
The controls contain432 two-blocker U roles and240 barrier parameter sets,
130 originally disjoint after adding G's far stem. There are4 nontrivial
shallow excluded parameter sets and8 width-six excluded sets; these counts
exclude already incompatible F/G barriers. All four routed roles have
positive PARTIAL geometric coverage. See the
[control receipt](../output/backfill-corner-routing.json).

All23 declarations compile with Lean4.33.0 on the selected local Mac.
Their scoped axiom audit passes with only propext, Quot.sound and
Classical.choice; the exact rotor catalogue is axioms-free. No sorry,
native_decide or additional axioms. See the
[formal source](../formal/SubQuorum/BackfillCornerRouting.lean) and
[execution/scope receipt](../output/backfill-corner-routing-formal-check.json).
The [initial four-route written audit](../output/backfill-corner-routing-review.json)
completed ACCEPT at12:17:40 UTC, observed gpt_6/pro, with no must-fix issue.
Original streaming process54235 exited0/DONE and its16628-character answer
exactly matches the terminal broker response. The
[full response](../output/backfill-corner-routing-review-response.txt) checks
complete source/partition adapters, all original roles/phases, rotor and
wrong-turn exclusions, the initial strict bounds and shallow obstruction,
and actual singleton/cap injections with recurring owners. It does not
certify execution, complete U10 realization or the allocation/grid target.
Its packet excludes the later extra A/C width bounds and width-six height12
strengthening. The DISTINCT
[extension audit6d9a713e](../output/backfill-width-six-barrier-review.json)
also completed ACCEPT, observed gpt_6/pro. Original streaming process93766
exited0/DONE and its9529-character answer exactly matches the terminal
response. It checks all A/B/C/D cases of the extra bounds and height12
conclusion, conditional on the separately accepted four-route theorem.
Its two nonblocking cross-reference/parity wording corrections are applied.
Neither audit includes the later
[two-corner compensation theorem](BACKFILL_TWO_CORNER_COMPENSATION.md),
which has a separate same-conversation review.

The next allocation task remains to join these four routes to ONE actual
cap/singleton/marked-side ledger, treating recurring owners and other full
receivers simultaneously. A strict local length drop cannot be composed
around arbitrary turns without proving which length is transported. No
new reserve, uniform coefficient improvement, general U10 nonexistence or
rectangular-grid equality follows from this note.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
