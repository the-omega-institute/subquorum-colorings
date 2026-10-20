# Shared bar tiles pay; singleton negative owners carry the residual tax

20 October 2026. We sharpen the general defect inequality from
[the preceding note](SEPARATED_NEGATIVE_RECEIVER_COMPENSATION.md).
Two-endpoint negative bar overlap needs no extra tax by itself. Only
negative1P1T owners create the remaining local debit. This removes
receiver separation entirely for positive U sources, phase-(1,1)
negative U sources and arbitrary zero-charge rotors.

## 1. Model and statement

Use the exact complete fixed-source fusion model and established inputs
of ALL_PHASE_JOINT_COMPENSATION_SLOTS.md. Source U(w,a,b) has even w>=6,
independently even a,b>=4, and any effective phase/isometry. Rotors of
every phase are allowed. Original endpoint sets are disjoint; final P
and M are exactly their original unions, and final T is the complete
original support union minus P. Require final feasibility. Optional
extra selections are outside all original receivers and have no
endpoint neighbor. There is no receiver-separation, contact-graph,
pair-feasibility, port, freezing or final-degree-three assumption.

Keep N positive U sources, B negative U sources, R negative rotors,
sigma=mn/2-|T|-|M|, L=sum_row_shifted(w_i-2), S=L+B+2R,
and the tilewise residual credit c_Q>=0 after regular events. A counts
marked-side assignments to phase11 upper corners, E=G-A, and the
established boundary injection gives E<=2N and E<=2B.

For each physical receiver tile Q, let r_Q count its NEGATIVE original
endpoint owners and h_Q count those with original profile1P1T. Define

    O = number of Q with r_Q>=2 and h_Q>=1,
    F = number of Q with h_Q=4,
    H = number of Q with r_Q=h_Q=1 and a zero-charge3P0T owner.

All counts keep ORIGINAL source ownership, including after components
merge. F tiles are counted once in O and once more in F. Then

    Kirregular+A <= C+L+O+F+H,                         (1)
    sigma >= |N-B|+2R-O-F-H.                          (2)

In particular O+F+H<=|N-B|+2R suffices for coefficient one. This sharpens
the previous D+H criterion: O+F<=D, where D counted every vulnerable
negative owner in a shared tile. No automatic global coverage of O,F,H
is asserted. The unrestricted grid inequality/triple equality remain open.

**All-bar negative-source corollary.** If no negative source has a1P1T
receiver profile, then O=F=H=0 and

    sigma >= |N-B| >=0.                              (3)

In the present catalogue, the negative U sources are then exactly the
phase-(1,1) class and there are no negative rotors. Positive U sources
and arbitrary zero-charge rotors are permitted. Negative sources may
overlap in receiver tiles without restriction. All widths, independent
leg heights and transported directions remain allowed. Coefficient one
strengthens the previous5/6 matching coefficient by |M|/6 in this class.

## 2. Local catalogue and basic facts

Every original endpoint subset inside a physical tile is connected.
Original selections in that tile are adjacent to their unique original
endpoint anchor. The complete signed local catalogue is

| Owner sign | Allowed profiles |
|---|---|
| nonnegative | 1P2T, 2P1T, 3P0T, 4P0T |
| negative | 1P1T, 2P0T, 2P1T, 3P0T, 4P0T |

The nonnegative3P0T owner must be a zero rotor. A1P2T endpoint has
no adjacent intratile blank; its only blank is diagonal. A2P1T profile
has at most one regular event; a3P0T profile has exactly two regular
events if its missing corner becomes an endpoint. A negative1P1T
profile has at most one irregular event. A negative2P0T profile has
at most two, one per endpoint. All endpoints remain occupied.

For a retained selection, its original anchor and any second occupied
neighbor would violate feasibility. Thus original supports remain
occupied, but must become original foreign endpoints when such a
second occupied neighbor appears. No new endpoints may be invented:
all forcing conclusions are necessary conditions on the fixed union P.

Let k_Q count irregular events and l_Q negative2P0T profiles, with
multiplicity by owner. Let a_Q count phase11 upper-corner assignments.
An assigned upper corner keeps its unique original intratile blank
outside P, so its event is absent and the tile is not full. Each
negative2P0T owner has at most one such corner in a given tile. Hence
its own events plus assignments are at most two. Since a tile with a
bar owner and a blank corner has room for at most one other singleton
owner, a_Q<=1; if h_Q>=2, then a_Q=0.

## 3. No singleton negative owner: local payment is complete

Suppose h_Q=0. If an irregular event occurs, its original owner is
negative2P0T. Its foreign event target belongs either to a second
negative2P0T owner, in which case the two adjacent endpoint pairs
already fill Q, or to a regular owner. The latter cannot have3P0T or
4P0T because two original negative endpoints already occupy Q.
A1P2T or2P1T target owner forces Q full by the original support
argument in the preceding note. Thus any irregular-event tile is new
mixed full.

In a full event tile there are just three endpoint partitions:

| Original owners in Q | k_Q | Kregular(Q) | l_Q | c_Q+l_Q-k_Q |
|---|---:|---:|---:|---:|
| two negative2P0T pairs | 4 | 0 | 2 | 0 |
| negative2P0T pair and a2P1T pair | 2 | 1 | 1 | 0 |
| negative2P0T pair and two1P2T singletons | 2 | 0 | 1 | 1 |

The last singletons must be nonnegative because h_Q=0. No other
partition fits. In particular k_Q<=c_Q+l_Q.

If a_Q=1, Q is not full, so it has no irregular event by the implication
just proved. Its one bar reservation pays that assignment. If a_Q=0
and no event occurs, use c_Q,l_Q>=0. Therefore

    h_Q=0 implies k_Q+a_Q<=c_Q+l_Q.                  (4)

This is the step that removes the overlap tax from bar-only contacts.

## 4. One singleton negative owner

Suppose h_Q=1. If it is the only negative owner, the preceding
forced-full theorem pays its event from c_Q, except for a3P0T foreign
owner. Such an owner fills the other three corners and is a zero rotor;
it gives k_Q=1, Kregular(Q)=2, c_Q=l_Q=a_Q=0. Charge its H unit.

If there is another negative owner, there can be at most one: it needs
at least two endpoint corners. With a partial three-endpoint tile,
the second owner is2P0T or2P1T. For2P0T, its endpoint adjacent to the
singleton can incur one event. The singleton's old selection must be
one of the pair's endpoints: selecting the missing corner would force
that corner into P because it sees two final endpoints. Its other
intratile neighbor is that blank corner, so the singleton has no event.
Thus k_Q<=1, a_Q<=1, and l_Q=1. For2P1T the only possible irregular
event is the singleton's, so k_Q<=1 and a_Q=l_Q=0. Both cost at most
one beyond c_Q+l_Q.

For a full tile the other corners are either a3P0T owner, a2P0T/2P1T
owner and a nonnegative1P2T singleton, or three nonnegative1P2T owners.
Their exact respective upper bounds on k_Q-c_Q-l_Q are1,0,0 and-1.
Full tiles have a_Q=0. Consequently

    h_Q=1 implies k_Q+a_Q<=c_Q+l_Q
                         +indicator(r_Q>=2)+indicator(Q counted in H). (5)

## 5. Two, three or four singleton negative owners

For h_Q=2, a_Q=0: a bar owner plus two singletons would fill Q.
In a partial tile the two singletons cannot both incur irregular
events. If their endpoints are adjacent, two events would require their
original selected neighbors at the other two corners; these adjacent
supports must both become endpoints by final feasibility. If they are
opposite, either original selected neighbor is adjacent to both final
endpoints and hence must become an endpoint. If one additional endpoint
leaves a three-endpoint tile, its owner is a nonnegative1P2T singleton.
It must occupy the elbow of the L: at an outer vertex, one of its two
original selections would be the missing corner, which sees two endpoints
and would be forced into P. The negative singletons are therefore the
outer vertices. Each selects the elbow and has its blank at the missing
corner, so neither incurs an event. Thus a partial tile has k_Q<=1
(and this three-endpoint case has k_Q=0).

In a full tile, the other two endpoints are a negative2P0T pair, a
regular2P1T pair, or two nonnegative1P2T singletons. The corresponding
values of k_Q-c_Q-l_Q are1,1,0. Thus the single O unit suffices.

For h_Q=3, a_Q=l_Q=0. A partial tile has three singleton endpoints in
an L. No original support can occupy its missing corner because it
would see two final endpoints. Both outer endpoints therefore use the
middle endpoint as their selected neighbor and incur no event. The
middle one incurs at most one. If the tile is full, its fourth owner
is nonnegative1P2T (otherwise h_Q=4), so k_Q=3, c_Q=2. Again the
single O unit suffices.

For h_Q=4 the tile is full, all four owners have1P1T, k_Q=4,
Kregular(Q)=0 and c_Q=2. There is no bar reservation or assignment.
Exactly two further units are needed in this relaxed local catalogue:
one O unit and one F unit. This local necessity is not a claim that
every such signed profile packing extends to complete feasible sources.

Together with (4)-(5), every physical tile satisfies

    k_Q+a_Q <= c_Q+l_Q
                +indicator(r_Q>=2,h_Q>=1)+indicator(h_Q=4)+indicator(Q in H).

Sum once over tiles to prove (1). The established ledger and mass identity
give sigma>=N+B+2R-E-O-F-H. Applying E<=2N,2B proves (2), and (3)
follows. No square credit or bar reservation is used in two tiles, and
the gate exclusion prevents its simultaneous use for two costs in one tile.

## 6. Verification scope and remaining problem

The local checker enumerates the complete42 signed oriented profiles,
their660 endpoint-disjoint tile packings and434 packings satisfying
retained intratile support feasibility. The local upper bound also
allows a bar mark whenever one of its missing neighbors is outside P;
this is a relaxation of the actual canonical-side geometry. It does
not assert existence of a positive source producing every allowed mark.
The all-parameter proof is Sections2-5, not an extrapolation from a search.

All640 existing complete physical images pass the refined tilewise and
global bounds. All640 now have a nonnegative lower bound;160 improve
strictly on the earlier D+H bound, which certified496. These fixtures
do not prove automatic compensation for every complete source fusion.
Seventeen Lean declarations and individual axiom audits pass locally with
Lean4.33.0. Kernel reduction checks the complete local catalogue, both local
payment rules, an additional half-slot rule and actual rotor coordinates
in all four translation phases. Conditional arithmetic checks the global
consequences. The complete source-to-profile adapter and global injection
remain written inputs; this is not a full Lean proof of arbitrary fusions.
See output/singleton-negative-defects-formal-check.json.

The remaining problem is to pay O+F+H from |N-B|+2R, or to give a
complete feasible obstruction to this sufficient rule and distinguish
it from a counterexample to the target. No change to a submitted
manuscript or email is part of this note.

Review5005a44b-4be2-40b3-a689-18c97389128a completed ACCEPT for this
written bound and its all-bar corollary, alongside repaired Section6
and the half-slot note. Its h_Q=2 elbow clarification is implemented
above. Original stream23629 exits0/DONE and matches all18005 terminal
response characters, observed gpt_6/pro. Established geometric ledger,
source catalogue, marked-side injection and rotor barrier remain inputs.
The separate rotor-only theorem is outside that accepted scope.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
