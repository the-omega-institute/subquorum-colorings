# All four critical-backfill routes share one original-occurrence budget

20 October 2026. A's selected cap cannot be reused by a B/D cap output.
This separates the last cap-reservation families in the four-route ledger.
Together with the occupied-band output theorem it gives one inequality
covering ALL critical U10 backfill events, with an extra term for C events.
Original negative-source counts and the remaining marked-side allocation
are still present. This does not prove unrestricted coefficient one or
the rectangular-grid triple equality.

## 1. Complete-source setting and the previously established outputs

Use precisely the complete finite original-source, legal even independent
dimensions, endpoint uniqueness, unchanged matching, mandatory support,
occupied-degree and transported physical partition hypotheses of
[the four-route theorem](BACKFILL_CORNER_ROUTING_AND_SHALLOW_BARRIER.md).
Keep the global critical-root and backfill injection theorems and the
actual source phases. Original owners may recur across events/components.

Every critical U10 backfill has exactly one route A,B,C,D. Write their
event counts KA,KB,KC,KD and Kback=KA+KB+KC+KD. These are event counts,
whereas K01,K10,K11 below are ORIGINAL U source counts.

The established route outputs are:

- A selects the adjacent original phase11 cap of its q owner; these caps
  inject, whether filled or unfilled.
- B/D have the cap/interior alternatives of
  [the occupied-band output theorem](BACKFILL_OCCUPIED_BAND_OUTPUTS.md).
  Write KB=KBcap+b, KD=KDcap+d. Cap outputs are actual original companion
  caps, inject jointly across B and D. Interior output tiles inject jointly
  and avoid all ordinary/critical/backfill receivers.
- C reserves its original q negative singleton and either another negative
  singleton or a positive activation at r, all in its original backfill tile.

Distinct B/D cap tiles follow directly from original triples: coincident
caps identify the same original companion and cap, hence its leg and
terminal, hence the same critical event. In particular B and D cannot
use the same cap. The missing corner's actual original owner would also
have to be both phase00 and phase10, which is impossible.

## 2. An A-selected cap's terminal cannot be a critical companion

Normalize one A event as in the routing theorem. Its critical root owner
G is phase10 of width u and incident height g, and owns

    (row,0), 0<=row<=g.

Its q owner V is phase11, with horizontal bar rows1,2 and right stem in
column-1. Name the incident height a. The original run/bar collision gives
a<=g-4. V's selected right cap has

    triple {(2,-2),(2,-1),(3,-1)}, missing corner(3,-2).         (1)

This cap identifies V's right original leg and its original terminal

    f=(a+1,-1).

Suppose another critical event used V as its original U11 companion and
this same leg. The terminal's outward incident direction is south, so its
critical root would have to be

    t'=f+(1,0)=(a+2,-1).

The actual physical partition in this normalization has even row/column
origins. Since a is even, t' is an even-row/odd-column corner; its physical
opposite-corner displacement is(1,-1). A critical root's displacement is
-s'+d', and d'=south=(1,0). Therefore s'=east=(0,1).

The critical active source must be phase01 and own t'+s'=(a+2,0). But G
already owns this endpoint: a>=4 and a<=g-4 put a+2 between0 and g.
G's fixed original phase is10. Original endpoint uniqueness would identify
two sources with different phases, a contradiction.

This is a fixed transported-tile argument, not an assumed compatible turn
or a descent through unrelated dimension parameters. It proves that the
original leg corresponding to EVERY A-selected cap is unavailable as the
companion leg of ANY critical event anywhere in the same source fusion.

Consequently no A-selected cap can coincide with a B/D cap output. A
coincident original triple would identify the same original owner and
cap/leg, contradicting the preceding paragraph. Distinct cap owners would
require six original endpoints in a four-point tile.

## 3. The actual disjoint cap reservation

Let Csel be the union of all A-selected caps and all B/D cap outputs. The
individual injections and Section2 make this a disjoint union, so

    |Csel|=KA+KBcap+KDcap<=2K11.                              (2)

Let Q be the cardinality of the complement of Csel in the set of ALL
original phase11 U caps. Then Q>=0 and the stronger exact identity is

    2K11=KA+KBcap+KDcap+Q.                                  (3)

Q is a count of unselected ORIGINAL cap occurrences. It is not additional
unfilled reserve U0, unused positive activation, or an independently
spendable resource. Its caps may be filled and used elsewhere; only its
nonnegativity will be used.

For an equivalent typed capacity certificate, split A-selected caps into
unfilled Au, negative-filled An and positive-filled Ap. Then

    KA=Au+An+Ap,
    Au<=U0, An+KDcap<=Fneg, Ap+KBcap<=Fpos.

These are joint subfamily bounds, not separate uses of Fneg/Fpos. The cap
partition Fneg+Fpos+U0=2K11 gives(2) directly. Cap triples also prevent
coincidence with any B/D interior output tile, so there is no hidden
cap/pair overlap in the common occurrence accounting.

## 4. All-route inequality and exact single-pool reserve

Use E0,E1old,Cplus and the SINGLE unused negative singleton complement L
from the occupied-band theorem; let e=|E0|+|E1old|. That theorem proves

    2K11+e+2KC+d+b<=2K01+2K10+A+U0,                         (4)

and the exact reserve identity

    2R=2(K11-K01-K10)+e+2KC+d+b
         +(A-Fpos-Cplus-b)+Z0+H+L.                          (5)

Its activation remainder and L are nonnegative and come from actual
jointly disjoint source-occurrence families. Do not redefine L using the
full E1reg set or infer unused capacity from Q.

Substitute (3) and the B/D partitions ONCE. Since

    KA+KBcap+KDcap+2KC+d+b=Kback+KC,

equation(5) becomes the ALL-ROUTE exact identity

    2R=Kback+KC-2(K01+K10)+e+Q
         +(A-Fpos-Cplus-b)+Z0+H+L.                          (6)

Thus

    Kback+KC+e+Q<=2(K01+K10)+A+U0,
    2R>=Kback+KC-2(K01+K10)+e+Q+Z0+H.                     (7)

Dropping Q>=0 is allowed. These statements cover A,B,C,D simultaneously,
with coefficient one for every event and an extra coefficient one for C.
They improve coverage of the previous source-census form, rather than
claiming that a negative term has vanished: the original negative source
count 2(K01+K10) still requires control in a full allocation proof.

Keep Bpass for the old passive-corner count, J for the jointly packed
ordinary/critical H stops, and Tcrit for its Z0 subfamily. The occupied-band
shared-stop inequality, substituted in the SAME way, yields

    Bpass+J+Tcrit+Kback+KC-2(K01+K10)+e+Q+L<=2R+A.          (8)

The proof is literal substitution into the already budgeted cap/pair/
activation block, not addition of independently available reserve bounds.
All original cap fillers, negative singleton occurrences, terminal claims,
H stops and Z0 stops retain their previous single-use or justified
two-claims-per-activated-leg capacities.

## 5. Verification boundary and remaining goal

The Lean companion checks the normalized G wall endpoint, the forced
critical frame and tag contradiction, typed joint cap capacity, and
conditional all-route exact/retained/shared ledger arithmetic. Actual phase
and physical-partition transport, identification of A's cap with its
original leg, global event/cap injections and selected-cap complements are
the written adapters in Sections1--4. Execution and independent review
are recorded separately; no end-to-end source fusion theorem is claimed.

All8 declarations compile cleanly with Lean4.33.0 on the user-selected
local Mac; all8 scoped axiom checks PASS, with only propext, Classical.choice
and Quot.sound. No sorry/native_decide/additional axioms. Final source46978
exit0 and audit43235 exit0 both measured68% free memory; actual ps comm
basenames lean/lake were checked before every sequential invocation. See
the [Lean source](../formal/SubQuorum/BackfillFourRouteBudget.lean) and
[formal scope/receipt](../output/backfill-four-route-budget-formal-check.json).

The [controls](../output/backfill-four-route-budget-controls.json) pass216
endpoint-disjoint G/V source pairs with the required phase-tag collision,
all8 cardinal frames, and6723conditional all-route identity instances,
including4698positive cap complements. These pairs/identities are partial
geometry/algebra, not complete critical events or realizability evidence.

The combined Oracle review of BOTH this proof and the B/D band-output
theorem completed ACCEPT at13:18:39UTC on20October, task29f4d714, with
20394response characters and observedgpt6/pro. Original stream96627 exited0
and reached DONE; its answer matches the terminal task response exactly.
The review checks the written source/phase adapters, original profiles,
global output injections and receiver separation, A-leg nonreuse, joint
cap/singleton/activation pools and exact all-route/shared-stop substitutions.
It identifies no must-fix mathematical issue. See the
[review receipt](../output/backfill-four-route-budget-review.json) and
[full response](../output/backfill-four-route-budget-review-response.txt).
The verdict does not certify reported Lean execution or finite controls,
complete critical U10 realizability, unrestricted allocation or grid equality.
The earlier failed B/D audit and accepted prior shared-stop review retain
their separate scopes. Any subsequent D-second-corner enhancement is outside
this combined review.

Complete critical U10 realizations still have ZERO control coverage. Finite
parameter/frame and arithmetic checks can test the formulas; they cannot
prove the general nonreuse statement or unrestricted allocation. The
unrestricted marked-side inequality and grid triple equality remain OPEN.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
