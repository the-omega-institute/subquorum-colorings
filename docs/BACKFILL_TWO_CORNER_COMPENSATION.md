# Both corners of a phase01 backfill exit enter one compensation ledger

20 October2026. Under the COMPLETE finite original U/rotor hypotheses,
each phase01 singleton route at a critical U10 backfill supplies TWO
typed corner occurrences: two negative U singleton reservations, or one
negative reservation and one positive terminal activation. The positive
activation is separate from every filled phase11 cap activation. This
gives a simultaneous two-corner compensation inequality and an exact
single-pool reserve identity. It does not close the unrestricted
coefficient-one allocation or rectangular-grid triple equality.

## 1. Complete geometry and the second original owner

Use ALL complete-source, endpoint-uniqueness, unchanged matching, mandatory
support, degree-one and transported-partition hypotheses of
[the four-route theorem](BACKFILL_CORNER_ROUTING_AND_SHALLOW_BARRIER.md).
Normalize a critical U10 event to its backfill tile

    Qb={0,1}x{-2,-1}, q=(1,-1), r=(1,-2).

The original U11 companion F owns exactly(0,-2),(0,-1) in Qb and has
the original support r. The general backfill theorem forces q,r into P.
Consider ONLY route C: q belongs to an original phase01 U H as a south
terminal, and H owns exactly{q} in Qb. Its incident height is at least4,
so H also owns(2,-1),(3,-1). Its independent other height is unrestricted.
The actual original owner J of r differs from F,H,G. In particular J
owns exactly ONE endpoint in Qb, since its other three corners already
have the different original owners F and H.

J cannot be a rotor. The following complete original stencil is foreign
to J:

    {(0,-4),(0,-3),(0,-2),(0,-1)} from F,
    {(1,-1),(2,-1),(3,-1)} from H.                  (1)

Relative to r this is

    {(-1,-2),(-1,-1),(-1,0),(-1,1),(0,1),(1,1),(2,1)}.

All sixteen anchored two-chirality rotor roles meet this stencil. As in
the preceding theorem, quarter-turn invariance accounts for all signed
coordinate permutations, so the fixed catalogue proves exclusion at all
translations without a bounded source search. It follows that J is a U.

The complete U singleton catalogue now gives EXACTLY two alternatives:

- J is negative phase01 or10. Then r belongs to the original U-only
  negative singleton pool Pneg and to E1reg, since F supplies a foreign
  exact regular2P1T pair in Qb.
- J is positive phase00. Its singleton is an original terminal1P2T
  occurrence. Both original intratile supports are consumed because Qb
  is full. Thus r is an actual activation counted by A.

There is no phase11 U singleton. The rotor case was excluded from actual
complete source geometry, not omitted from the resource count.

## 2. Global injection and separation from other uses

Let KC count all route-C events, with recurring original owners and
different components allowed. Let Cminus count events whose r owner is
negative and Cplus those whose r owner is positive. Then

    Cminus+Cplus=KC.                                (2)

The accepted global backfill theorem makes the physical Qb pairwise
different and disjoint from ALL ordinary and critical receiving tiles.
Consequently the q/r positions of all these events are distinct, including
q versus r of different events. The KC q-points and Cminus r-points are
different original Pneg singleton occurrences in E1reg. They cannot
overlap E1old, the E1reg occurrences in the old receiving tiles. They also
cannot overlap E0, whose foreign exact original pair is irregular2P0T.
The pair at these new points is F's regular2P1T profile.

The Cplus points are distinct actual positive terminal activations. They
are separate from EVERY positive cap-filling activation counted by Fpos.
A cap-filling terminal's tile contains a foreign original phase11 triple.
The new r tile already contains F's exact original pair. If cap and pair
owners differ, five disjoint original endpoints would be required in one
four-point tile. If they agree, one source would have two different EXACT
profiles in the same tile. Both are impossible. Therefore

    Fpos+Cplus <= A.                                (3)

This is a separation of actual positive TERMINAL occurrences. Different
terminals of the same positive source are permitted and count separately.
It does not assign a new activation merely because its source is positive.

Let FnegSet contain all negative singleton cap fillers. The established
pair-versus-triple separation makes FnegSet disjoint from every E1reg and
E0 occurrence. Thus the following are disjoint subsets of ONE Pneg pool:

    FnegSet, E0, E1old, {all route-C q}, {negative route-C r}.

Let L be the cardinality of the complement of THIS union in Pneg. It is
nonnegative and includes any other old or new singleton reservation not
selected into the union. Using |Pneg|=2K01+2K10 gives the exact identity

    Fneg+|E0|+|E1old|+KC+Cminus+L=2K01+2K10.         (4)

K01,K10,K11 throughout are original SOURCE counts. KC is an event count.
No assumption of fresh owners, disjoint components, unfilled caps or
unused activation capacity has entered (2)--(4).

## 3. Two-corner compensation and the exact reserve identity

The original cap partition is Fneg+Fpos+U0=2K11. Substitute this and
(2)--(3) into (4), retaining only L>=0, to get

    2K11+|E0|+|E1old|+2KC
      <=2K01+2K10+A+U0.                            (5)

This replaces the preceding one-corner KC term by2KC while keeping ONE
joint cap/pair/activation budget. We do not also add the complete E1reg
count: it already contains the KC+Cminus negative corner occurrences.

There is a stronger exact form. Substitute (2), (4) and the cap partition
ONCE into the established geometric identity2R=A+U0+Z0+H:

    2R=2(K11-K01-K10)+|E0|+|E1old|+2KC
         +(A-Fpos-Cplus)+Z0+H+L.                   (6)

The activation remainder is nonnegative by (3), and L is a SINGLE
complement in the original Pneg pool. Thus

    2R>=2(K11-K01-K10)+|E0|+|E1old|+2KC+Z0+H.      (7)

Equation(6), rather than separate estimates added together, proves that
neither a negative cap filler, a selected old singleton reservation nor
a positive cap-filling activation was spent again. Each route-C event
has coefficient two in2R, equivalently one in R, together with the signed
source-census term and retained defects. That signed term cannot be
dropped when negative. The pre-existing H and Z0 occur once in the SAME
identity; they are not further independent payments.

This is a partial compensation lemma for ALL route-C backfill exits in
arbitrary finite complete mixed fusions. It is not an unconditional lower
bound R>=KC and does not prove N+R-G>=0. Routes A,B,D, other full and
neutral exits, recurring side reservations and arbitrary direction changes
still need a common allocation. No new uniform5/6 improvement follows.

### Sharing these reservations with all established stop classes

The positive occurrence separation also strengthens the existing shared
stop lemma. Retain its passive-corner partition

    B=D+C0+C1+Eterm,

where Eterm is the E1 activated TERMINAL claim class of
[the passive-corner theorem](PASSIVE_CORNERS_AND_NEUTRAL_OWNERSHIP_CYCLES.md).
Each Eterm terminal's physical tile contains the producing phase10
source's exact irregular2P0T pair. Such terminal occurrences inject by
the established theorem. A positive cap filler instead has a foreign
original triple in its tile; a Cplus terminal instead has F's regular
original2P1T pair. These three families of positive TERMINAL occurrences
are pairwise disjoint. A pair/triple coincidence is impossible by the
same exact-profile argument as above. A regular/irregular pair coincidence
requires either four foreign endpoints besides the common terminal, or
one original owner with two different EXACT profiles. Thus

    Eterm+Fpos+Cplus<=A.                            (8)

C1 still counts corner claims against the SAME activated legs and satisfies
C1<=A. A corner claim may use a leg whose terminal is also in one of the
three families in (8); the established factor two allows these two uses.
We do not declare a third copy of any activation capacity.

Let J=J01+J11+Jcrit be the established jointly disjoint nonfull ordinary/
critical stop counts. The accepted shared geometry gives D+C0+J<=H and
Tcrit<=Z0. Using (8), C1<=A, and the ONE exact reserve identity yields

    B+J+Tcrit+Fpos+Cplus+U0<=2R+A.                  (9)

This retains Fpos and Cplus in the same budget that already paid the
passive corners and ordinary/critical stops. Neither H nor Z0 is counted
again. Substituting the cap partition and (2),(4) ONCE gives

    B+J+Tcrit+2(K11-K01-K10)+|E0|+|E1old|+2KC+L
      <=2R+A.                                      (10)

Dropping only L>=0 gives a simultaneous cross-component compensation
inequality with both new corner occurrences and every established stop
class. It improves the preceding stop bound by the nonnegative Fpos+Cplus
in (9), and retains the doubled KC reservation after substitution. It
does not prove the final marked-side allocation: the signed source-census
term and the A on the right still require global control.

## 4. Verification boundaries

The written proof above supplies the actual complete-source adapters,
second-owner singleton classification, q/r injection, pair/triple
separation and pool partition. The Lean companion checks the exact16-role
rotor exclusion and conditional simultaneous/exact ledger arithmetic.
The checker tests the exhaustive second-corner rotor template separately
from sampled U role/barrier controls. Complete feasible critical U10
witness coverage remains ZERO; no realization or sharpness is claimed.
All six new Lean4.33.0 declarations compile on the user-selected local Mac,
and their scoped axiom audit passes with only propext and Quot.sound; the
rotor catalogue is axioms-free. No sorry/native_decide/additional axioms.
See the [source](../formal/SubQuorum/BackfillTwoCornerBudget.lean),
[execution/scope receipt](../output/backfill-two-corner-formal-check.json),
and [two fixed rotor catalogues](../output/backfill-corner-routing.json).
The independent same-conversation two-corner audit completed ACCEPT at
12:33:41 UTC, task0d801149-95fe-4c94-80d3-b941c4e74d47 in
conv_befbb4414446045a. Original stream25217 exited0/DONE and matches
all14227 response characters exactly; observed model gpt_6/pro. No must-fix
mathematical issue was found. The review covers the written source/activation
argument and equations(2)--(7), not execution or complete U10 realizability.
See the [review receipt](../output/backfill-two-corner-review.json) and
[full response](../output/backfill-two-corner-review-response.txt).
The initial two-corner packet likewise excludes the LATER shared-stop
extension (8)--(10); its new geometric input is the exact-profile separation
of Eterm from both Fpos and Cplus. That extension has two further scoped
arithmetic statements, both compiled and axiom-audited in the final
six-statement run. Its written review scope remains separate from the
first four-statement packet.

The distinct same-conversation follow-up for exactly(8)--(10), task
7ea29eb0-1eee-4164-8f8f-2e170581c38e, completed ACCEPT at12:45:02 UTC,
observedgpt_6/pro, with no must-fix issue. Original stream96016 ended with
unexpected EOF; the SAME task's completed11658-character response was
recovered from the broker API. No complete-stream or exact-match claim
is made. See its [receipt](../output/backfill-shared-stop-review.json) and
[full written review](../output/backfill-shared-stop-review-response.txt).
The packet includes the complete passive-corner and critical shared-stop
source notes and final six-statement Lean source. This independent ACCEPT
covers the later geometric adapter and shared ledger, not execution or the
subsequent [B/D occupied-band outputs](BACKFILL_OCCUPIED_BAND_OUTPUTS.md).

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
