# Complete compensation with separated negative receivers

20 October 2026. The density condition in the preceding all-phase theorem
can be removed when different negative sources do not share a physical
receiver tile. The proof pays actual irregular events locally, reserves
one unit for each row-shifted bar tile, and then counts the remaining
marked sides in two different ways. Widths and leg heights disappear.

## 1. Exact model and conclusion

Use the complete fixed-source fusion model of
[the all-phase theorem](ALL_PHASE_JOINT_COMPENSATION_SLOTS.md): original
endpoint sets are pairwise disjoint, P is their union, the original
matchings are retained, and T is the union of all original supports minus
P. The complete final union must be feasible. Optional extra selections
are outside every original receiver and have no endpoint neighbor.

Complete U(w,a,b) modules have even w>=6 and independent even a,b>=4;
all effective phases and grid isometries are allowed. Rotors of charge
-2 are allowed. A zero-charge rotor is allowed here only when all its
original receiver profiles are 2P1T (the reference phase-(1,1) class).
In particular the theorem applies to U modules alone.

The additional geometric hypothesis is

    R_i intersect R_j = empty for distinct negative sources i,j,   (H)

where R_i is the set of PHYSICAL tiles containing an original endpoint
of source i. This does not separate their occupied sets, forbid contacts
across tile boundaries, or restrict contacts with positive sources.
There is no contact-graph, pair-feasibility, port, complete-freezing or
final-degree-three assumption. The restriction on zero rotors is material:
their other zero-charge phases have 3P0T tiles, which the argument below
excludes among the other owners of an irregular-event tile.

Let N count positive U sources, B count all negative U sources, and R
count negative rotors. With sigma=mn/2-|T|-|M|, we prove

    sigma >= |N-B|+2R >= 0.                                  (1)

Thus |T|+|M|<=mn/2 throughout this class, without a source-density
condition and independently of all widths and leg heights. Relative to
the existing 5/6 matching coefficient, coefficient one strengthens the
bound by |M|/6. This is a theorem for (H), not for every fusion or every
rectangular-grid configuration. The unrestricted triple equality is open.

## 2. A foreign regular profile completes an irregular tile

Call an original local profile GOOD when it is 1P2T, 2P1T, or 4P0T,
with connected endpoints and every selection adjacent to its unique
original endpoint anchor. Every positive U tile and every permitted zero
rotor tile is GOOD. Original 3P0T profiles are deliberately not included.

Suppose Q has an original irregular profile of its sole negative owner:
either 1P1T or 2P0T. If an irregular event occurs in Q, a formerly blank
neighbor of a negative endpoint is a foreign original endpoint. By (H)
its owner has charge nonnegative, so its profile in Q is GOOD.

For 1P1T, normalize the negative endpoint to corner 0, its selected
neighbor to corner 1, and the newly occupied blank to corner 2; corner
3 is opposite 0. Corner indices have adjacency given by xor 1 or xor 2.
A foreign 1P2T profile at 2 has original selections at 0 and 3. Hence 3
is finally occupied. The old negative selection at 1 would then have
its anchor 0 and the occupied neighbor 3, so it must become an endpoint.
The site 3 cannot remain selected beside endpoints 1 and 2, so it also
is an endpoint. A foreign 2P1T profile at 2 must have its other endpoint
at 3: the alternative adjacent corner 0 has the negative owner. This
again forces selection 1 to become an endpoint. A foreign 4P0T profile
would overlap corner 0 and is impossible. Thus Q is full.

For 2P0T normalize the negative endpoints to 0,1 and an event target to
2. A foreign 1P2T profile at 2 occupies corner 3 as an original selection;
it cannot remain selected because it sees the two distinct endpoints 1
and 2. A foreign 2P1T profile must have its other endpoint at 3, while
4P0T again overlaps the negative owner. Q is full in every case.

These arguments use persistent occupancy of every original selection,
including a selection consumed by an endpoint. They do not assume that
any pair of sources is feasible on its own.

## 3. Exact local payment and the bar reservation

Use the established original-owner ledger

    sigma >= N+S+C-Kirregular-G,
    C=sum_Q c_Q,  c_Q=2 indicator(Q is a new mixed full tile)-Kregular(Q)>=0.

The last inequality is tilewise by the regular-tile theorem. In an
irregular-event tile, (H) leaves either one or two negative endpoints.
The remaining endpoint owners are GOOD. An owner with a singleton
1P2T profile has no original intratile blank and contributes no regular
event. There can be at most one owner with a 2P1T profile in the remaining
corners, and it contributes at most one regular event. A 4P0T owner
cannot coexist with the negative endpoint. Consequently Kregular(Q)<=1
and c_Q>=1 whenever an irregular event occurs in Q.

For a negative 1P1T tile there is at most one irregular tail, so

    Kirregular(Q) <= c_Q.                                   (2)

For a negative 2P0T tile there are at most two irregular tails, so

    Kirregular(Q) <= c_Q+1.                                 (3)

If no event occurs, both statements follow from c_Q>=0. Negative rotors
have only 1P1T irregular profiles. A phase-(0,1) negative U likewise has
only its two 1P1T tips. Each row-shifted negative U has exactly w-2
2P0T bar tiles; its remaining irregular profiles are 1P1T.

Let L=sum_row_shifted(w_i-2). Each such bar tile receives ONE reserved
unit, independent of the number of endpoints or possible event slots.
Let A count marked-side assignments to phase-(1,1) upper bar corners.
The all-phase injection proves that the corresponding gate stays blank,
so that tile is not full. Section 2 then excludes every irregular event
there. There is at most one such upper corner per 2P0T bar tile, and
distinct marked sides have distinct original donor tiles. Therefore a
bar tile used for an A assignment costs one reservation unit and no
irregular-event unit. In a bar tile without an A assignment use (3).
Summing (2)-(3) and these mutually exclusive uses gives

    Kirregular+A <= C+L.                                    (4)

Every c_Q is used only in its own tile; every bar reservation is used
once, for the excess event or the corner assignment. No correction
unit, endpoint witness, or donor side is counted twice.

## 4. Two bounds on the remaining marked sides

Put E=G-A. By the all-phase boundary classification these assignments
use only phase-(0,1) upper corners or row-shifted terminal tips. There
are exactly two such candidate endpoints per negative U source. Rotors
cannot receive a marked-side assignment. The existing endpoint injection
therefore gives E<=2B. Independently, there are just two canonical sides
per positive U source, so E<=G<=2N.

Writing R for the negative rotor count, the exact source formula gives

    S = L+B+2R.

Indeed each phase-(0,1) U has charge -1 and no bar reservation; a
row-shifted U has mass w-1=(w-2)+1. Insert (4) in the ledger:

    sigma >= N+S+C-Kirregular-A-E
          >= N+B+2R-E
          >= N+B+2R-2 min(N,B)
           = |N-B|+2R.

This proves (1). In particular one negative U of any phase, arbitrarily
many positive U modules, and any permitted zero rotors satisfy the
coefficient-one bound automatically. More generally N and B need not
be comparable. This improves the preceding sufficient density criterion
on a geometrically specified class instead of claiming that criterion
is necessary.

## 5. Boundaries of the proof and validation

If two negative owners share a receiver tile, a foreign endpoint need
not have a GOOD profile, and a partial irregular tile need not become
full. The already established fully frozen zero-credit three-U family
has just such a tile; it does not contradict the target inequality.
Similarly a 1P1T negative owner combined locally with a 3P0T zero rotor
can have one irregular event, two regular events and c_Q=0. This is a
local obstruction to the payment rule (2), not by itself a complete
feasible counterexample to (1).

The control program finds 13 feasible normalized local profile states and
checks 344 complete physical images under symmetries and all phases; 296
other images are explicitly excluded by the hypotheses. Eight accepted
images have actual irregular events and 32 have marked sides. In 272
accepted images the preceding coarse density lower bound is negative,
while the new bound is nonnegative. No physical upper-corner side
assignment is claimed in these fixtures; that case has the written
blank-gate proof and finite local reservation checks.

Ten scoped Lean declarations and individual axiom audits pass on the
user-selected local Mac with Lean4.33.0, one job and50% free memory at
preflight. They include exhaustive normalized tile completion/payment
checks, the excluded 3P0T role, arbitrary-list tile-payment summation and
the abstract arbitrary-count accounting. No sorryAx/native_decide is used.
The general source/isometry adapter and geometric injection remain written.
See output/separated-negative-compensation-formal-check.json and
output/separated-negative-compensation-controls.json for execution scope.

Independent review task70a45736-9bc5-4b3b-ba71-38215e198023 in
conversation conv_7a76379ee5f4fe05 is dispatched on original stream79182.
No final ACCEPT is claimed while it is live. The earlier all-phase ACCEPT
is an input result, not a review of this new theorem. A separate exploratory
Oracle taskf629ba4e asks about unrestricted reserve payment; it has no
completed result yet. A scoped one-negative-rotor SAT discovery returned
UNKNOWN at120 seconds, which supplies no exclusion or proof.

    python3 develop/check_separated_negative_compensation.py \
      --output output/separated-negative-compensation-controls.json

The remaining global problem is to handle tiles shared by negative
sources and the excluded zero-rotor 3P0T roles, with actual single-use
compensation. No change to a submitted manuscript is part of this note.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
