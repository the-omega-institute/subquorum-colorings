# Critical U10 exits force distinct full backfill tiles

20 October2026. Under the COMPLETE finite original U/rotor source model,
every critical root owned by a phase10 U forces a second, adjacent physical
tile to be full. These backfill tiles inject and avoid every first/LONG
and critical receiving tile. This eliminates an additional source of
endpoint reuse without treating any original endpoint as fresh reserve.
The FULL coefficient-one allocation and rectangular-grid triple equality
remain OPEN.

## 1. Hypotheses and the two-step continuation stencil

Adopt ALL ownership, legal even dimensions, unchanged original matching,
mandatory support retention, occupied degree at most one and transported
physical partition hypotheses of
[the critical profile theorem](CRITICAL_OWNER_PROFILES_AND_SHARED_STOPS.md).
Retain its critical-point injection and ordinary/critical receiver separation.
Original owners may recur; no freshness or closed-component hypothesis is used.

For ANY critical event with frame(s,d) and root t, its original owner has
one of the following two original endpoint runs:

    t-s,t-2s; or t+d,t+2d.                                  (1)

For a U this follows directly from the complete endpoint predicate and the
two foreign neighbors t+s,t-d. An endpoint avoiding those neighbors is an
upper outer bar corner or a terminal; the legal width>=6 and incident
height>=4 supply two steps along at least one available direction. This
does not assume its phase. For a rotor, a central endpoint has three
neighbors, so the root is a tip; its adjacent central square supplies the
second step along the tip's incident direction. The fixed two-chirality
root catalogue checks this exact assertion. Equation(1) concerns ONE
original owner, not merely two occupied endpoints with unrelated labels.

## 2. A U10 root forces an adjacent tile to be full

Normalize such an event to t=(0,0), frame(N,E). Write O for its active U01,
F for its first U11 owner, and G for its U10 root owner. The accepted full
bar/wall theorem excludes eastward G terminals, leaving the south terminal.
Its exact phase10 geometry gives

    (0,0),(1,0),(2,0) in P_G,
    (1,-1) in S_G,
    (1,-1),(1,-2),(1,1) not in P_G.                         (2)

Here S_G is the ORIGINAL support set. The opposite canonical stem is at
least5 columns away, and the normalized row1 is still strictly below the
canonical two-row bar because the incident height is at least4.

F's opposite terminal is f=(0,-1), with its incident run pointing west.
The actual neighboring tile is

    Qb={0,1}x{-2,-1}.

Its exact ORIGINAL F profile is

    P_F intersect Qb={(0,-2),(0,-1)},
    S_F intersect Qb={(1,-2)}.                             (3)

F also owns (0,-3), and it does not own (1,-1),(1,-2). These are arbitrary
dimension canonical terminal formulas, with F's actual phase11 partition.
In particular F and G are different original owners.

Let q=(1,-1). Its two persistent anchors are (1,0) in G and (0,-1) in F.
Since q is an original G support, mandatory retention forces q into final P.
Next r=(1,-2) is an original F support with persistent anchors q and
(0,-2) in F. It too must be in P. Together with (3), Qb is FULL.
Both q and r belong to neither F nor G; their owners need not be fresh.

The root receiver Q={0,1}^2 and Qb are different physical partition tiles.
This conclusion holds whether Q is full or is an eligible mixed3P0T stop.
The fill of Qb does not create another H stop or an independent R payment.

## 3. No backfill tile is an ordinary receiving tile

Use the established phase01-only endpoint tag. In normalized coordinates
the following tags are fixed:

    (-1,-1),(-1,0),(-1,1): some N, from O;
    (0,-2),(0,-1): none, from F;
    (0,0),(1,0),(2,0): none, from G.                        (4)

An ordinary first/LONG receiver at x with frame(s',d') has tile
x+{0,s',-d',s'-d'} and active tags some s' at
x-s'-d',x-d',x+s'-d',x+2s'-d'. These are FOUR original active endpoints,
including the complete-source fourth point; omitting it is invalid.

Exhaust the eight cardinal frames and four x in Qb. Exactly eight choices
have this actual receiving tile. Every one contradicts an active tag in(4).
Thus Qb cannot coincide with ANY first/LONG receiving tile. The finite
frame calculation exhausts a fixed definition; it is not a bounded search
over source dimensions or a statistical inference.

## 4. No backfill tile is a critical receiving tile

For a second critical event with root x and frame(s',d'), use its actual
tile x+{0,-s',d',-s'+d'}, its active triple tags some s' and its companion
pair tags none. Comparing with(4) leaves precisely five possibilities:

| x | (s',d') |
|---|---|
| (0,-2) | (N,E) |
| (0,-2) | (W,S) |
| (0,-1) | (N,W) |
| (1,-2) | (S,E) |
| (1,-2) | (W,N) |

Each is impossible using actual original owners, not freshness.

For x=(0,-2), its owner is F. In either frame, the two alternatives of(1)
are a south run or an east run. The south run requires (1,-2), an original
F support rather than an F endpoint. The east run requires (0,0), a G
endpoint. Both contradict original F ownership.

For x=(0,-1), frame(N,W), the second event's original phase11 companion
owns x-d'=(0,0). But this point belongs to G, a phase10 owner. Unique
original ownership would identify sources with different effective phases.

For x=(1,-2), its owner H differs from F because r is an original F
support, and from G by(2). In frame(S,E), a north run of(1) hits the F
endpoint(0,-2), while an east run hits G at(1,0). In frame(W,N), an east
run hits G at(1,0), while a north run hits F at(0,-2). Each alternative
violates original endpoint disjointness. All five cases are excluded.

Aligned tiles form a partition. Excluding all critical roots from Qb
therefore separates Qb from EVERY critical receiving tile, including
receivers of events on other components or with recurring owners.

## 5. Backfill tiles are mutually distinct

For each U10 critical event remember the pair(F,Qb). This pair determines
the event. A fixed phase11 U has only two original terminals, separated
by width-1>=5 in a canonical coordinate, so Qb contains at most one of
them. This terminal's unique incident direction determines d and hence
t=f+d. Global critical-point injection identifies the event.

Suppose two different events have the same Qb. Their F owners are distinct,
so their exact original pairs in that tile are disjoint. Normalize the
first pair to Qb's top row as in(3). The second pair fills its bottom row.
Because that pair contains its original companion terminal f', the
second critical root/frame must be exactly one of

    t'=(1,0), frame(S,E); or t'=(1,-3), frame(S,W).           (5)

In the first case t' belongs to the first event's G. The critical profile
classification would make it a terminal of that U10 owner. But(1,0) is
the preceding, nonterminal stem endpoint of G's terminal(0,0); the other
terminal is in a different canonical column. This is impossible.

In the second case f'=(1,-2), and the second phase11 F' owns the complete
west-terminal incident run pointing east. Legal height>=4 makes (1,0)
an F' endpoint two steps along that run. It is already a G endpoint,
and F' phase11 differs from G phase10. Again endpoint uniqueness fails.
This proves global injection of backfill tiles.

## 6. One joint endpoint requirement, without a reserve claim

Let K10 be the number of critical events whose root owner is phase10.
Their backfill union Wb is disjoint from every ordinary or critical
receiving tile and has exactly4K10 original endpoint positions.
For X,J,C01,L11,Ve,Vc,Ke,Ke3,Ke4,Kc as in the critical profile theorem,

    |X union Ve union Vc union Wb|+J
      =2(C01+L11)+2Ke+Ke3+2Ke4+4Kc+4K10.                   (6)

If C is the chosen set of closed U01 owners, at least the2K10 companion
endpoints in Wb are outside P_C, because their owners are phase11. The
two newly forced corners may belong to C; they are not declared external.
Thus the corresponding outside count has the additional lower bound2K10,
and a qualifying SAME AA endpoint component gives

    |P_component minus P_C|>=8ell+2L11+2Ke+Ke3+2Ke4+2K10.  (7)

All four backfill endpoints connect to their critical root through the
F terminal, so the same-component qualification is preserved. The existing
one-ledger compensation lemma remains unchanged. Full backfill tiles can
have zero square credit; (6)--(7) are necessary endpoint counts, not fresh
R/H/Z0 payments. The remaining full and neutral branches still require
a common connection to the cap/singleton/marked-side reservation ledger.

## 7. Validation and scope

All11 declarations in
[CriticalPhaseTenBackfill.lean](../formal/SubQuorum/CriticalPhaseTenBackfill.lean)
compile with Lean4.33.0 on the selected local Mac. Their scoped axiom audit
passes with only propext, Quot.sound and Classical.choice; the fixed rotor
statement is axioms-free. No sorry/native_decide/additional axioms are used.
See the [formal receipt](../output/critical-phase10-backfill-formal-check.json).
The source checks the normalized arbitrary-dimension U geometry, complete
rotor roles, successive forcing, exact frame catalogues, critical owner
collisions and count arithmetic. Physical source/partition adapters and
mutual backfill injection remain the explicit written proof above.

The [checker](../develop/check_critical_phase10_backfill.py) verifies all32
ordinary frame/corner cases (8same tile,0survivors), the8same-tile critical
cases with exactly the5listed survivors, and64backfill frame/root cases
(8same tile,2distinct-companion possibilities). It controls14,400 anchored
U images,432two-blocker roles,72U10 southern terminal profiles,72U11
companion profiles and4exact two-blocker rotor roles. The216complete
feasible images have96critical events but ZERO U10 critical events. This
batch therefore supplies no nonvacuous complete witness for the new
backfill conclusion; its proof is the general geometry in Sections1--5.
See the [control record](../output/critical-phase10-backfill.json).

A separate [finite completion search](../develop/discover_critical_phase10_completion.py)
fixes O=U(26,12,4), F=U(10,8,4), B=U(6,4,4) and a U10 root owner
G=U(6,4,20), using the maps in its recorded specification. With all2629
eligible contained U(6,4,4)/rotor candidates in30x32, at most24sources
and preservation of the actual neutral contact, Z3 returns UNSAT in2.796s.
This excludes only that seed/window/library/count, even when the critical
root receiver is allowed full. It proves no general nonexistence of U10
critical events or failure of a target inequality. The
[search receipt](../output/critical-phase10-completion-discovery.json)
records this limitation; it supplies no complete backfill witness.

Independent review9ca65557-0687-465b-8f7f-676d470555a9 is live in conversation
conv_efc478f328ada385. Its packet includes the imported endpoint, rotor and
frame definitions. It received the initial source snapshot; local alias,
adjacency proof elaboration and unused-hypothesis fixes do not change the
written theorem. No verdict or execution certification is inferred.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
