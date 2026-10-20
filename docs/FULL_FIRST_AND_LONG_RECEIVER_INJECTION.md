# Full first and long receivers are globally distinct

20 October 2026. Complete original-source geometry strengthens the earlier
nonfull receiver injection: ALL first neutral01 receivers and ALL long
phase11 second receivers are distinct physical tiles, even when full and
even across open components. This gives an exact joint endpoint count and
extends the exclusion from closed phase01 owners. It does not create reserve
from a full tile or settle unrestricted coefficient one or grid equality.

## 1. Hypotheses and the missing fourth endpoint

Use the complete finite original U/rotor source, endpoint uniqueness, matching,
mandatory support retention, selected degree at most one and fixed transported
physical tile partition hypotheses of
[the preceding phase11 result](NEUTRAL_PHASE11_CORNER_AND_SECOND_FORCE.md).
All U dimensions are legal and even, with width at least6 and both leg heights
at least4. Sources and endpoint components may recur; there is no acyclicity,
closed-component or fresh-owner assumption in the receiver injection.

The event family consists of each actual neutral01 contact's first forced
point, and its long phase11 second point whenever that branch exists. Write
C01 and L11 for these two event counts. At either type, normalize its forced
point to0, predecessor s=N and contact direction d=E. Its physical tile is
Q=[-1,0]^2; its active original phase01 owner O has exact original2P1T profile
with pair {(-1,-1),(0,-1)} and UNIQUE original support0.

The earlier direction stencil recorded original endpoints at (1,-1),(0,-1),
(-1,-1). Completeness gives a fourth endpoint (-2,-1), with the same phase01
source tag N. In canonical coordinates the original support row is r and
the four endpoint rows are r+1,r,r-1,r-2, all at column1. For a first point,
r=a-1 and a>=4, so r-2>=1. For a long second point r=a-v-1 and a>=v+4,
again r-2>=1. The limiting row1 is an inner bar endpoint, which has the same
source tag as the stem. This is why the fourth point remains valid at the
minimum dimension; omitting the bar would lose precisely the needed endpoint.

Thus, relative to either forced point, the active original endpoints are

    -s-d, -d, s-d, 2*s-d, all tagged some(s).

The other original owner has endpoints -s,-s+d. At a first point they have
tag some(d), from the passive original phase01 source. At a long second point
they have tag none, from the original phase11 corner source. Tags are assigned
to ALL phase01 endpoints by their source's common directed predecessor; all
other positions have tag none. Original uniqueness makes this assignment
consistent. No assertion about the forced point's own tag is needed.

## 2. Two complementary pair cases exclude a repeated full tile

Suppose two first/long events use the same physical tile Q. If their active
original owners agree, both points equal that owner's unique original support
in Q. The accepted joint first/long forced-point injection identifies the same
event. This argument permits repeated occurrences of one original source.

If the owners differ, their original pairs are disjoint by endpoint uniqueness.
Both pairs lie in Q, so they fill it. With the first event normalized above,
the second pair must be the opposite edge {(-1,0),(0,0)}. A regular original
phase01 pair is parallel to its directed predecessor. Its support lies across
the pair, so there are exactly two possibilities:

| Second forced point | Second frame | Incompatible original endpoints |
|---|---|---|
| (0,-1) | (N,W) | Its active endpoint (1,0) has tag some(N), while the first event gives that point tag none or some(E). |
| (-1,-1) | (S,W) | Its other-owner endpoint (-2,-1) has tag none or some(W), while the first active source gives that point tag some(N). |

Both are impossible. The second line is the previously missing use of the
fourth active endpoint. This proves receiver injection for ALL first/long
events, without nonfullness or closed-owner exclusion.

The Lean companion also proves the stronger universal tag statement directly:
for any two of the eight cardinal frames, if their four-corner tile sets agree,
the four active tags and the allowed passive tags force the same forced point.
Its finite frame proof covers the complete definition of cardinal orientation;
it imposes no bound on dimensions, number of sources or lattice placement.
The physical tile-set adapter is explicit: a point x with frame(s,d) has tile
{x,x+s,x-d,x+s-d}. Equality of actual tiles gives exactly the translated
membership hypotheses used by the generic formal injection theorem.

## 3. Both opposite endpoints avoid every closed phase01 owner

At either first/long forced point0, the west and south original endpoints are
foreign to its owner. A phase01 owner F at0 must have0 as an original terminal:
nonterminal stems have two opposite own neighbors and cannot avoid both foreign
directions; interior/lower bar roles likewise collide. An upper outer bar corner
in phase01 belongs to an original full4P0T bar tile and would overlap O's pair
in Q. The formal role theorem checks this for all original endpoint roles and
signed coordinate permutations, using the pulled physical tile's canonical
origin parity(0,1). It does not infer phase from a freely reset partition.

Every phase01 owner on ANY closed component of the specified neutral U-port
graph has both terminal tiles actual neutral2P1T, with exactly two final
endpoints. Q contains O's pair and0, hence at least three. Therefore0 belongs
to none of those original owners. This extends the accepted first-point
exclusion to long second points, including events on open components.

If Q is full, let w=s be its other endpoint outside O's pair. If w belonged
to a closed phase01 owner F, that owner's original phase01 profile in Q is
one of singleton terminal, regular pair, or full bar. The terminal contradicts
the closed-terminal final2P profile. A different owner's full bar overlaps O.
A disjoint regular pair must be {0,w}, contradicting the just-proved exclusion
of0. O itself has only its original pair in Q. Thus w also avoids ALL closed
phase01 owners. This uses the same original-profile catalogue as the accepted
closed-first-receiver proof, with the new long-point terminal exclusion.

## 4. Exact joint endpoint count in one physical ledger

Let X be the union, over ALL first/long event receivers Q, of their final
endpoints outside their own active original pair. Let J=J01+J11 count the
nonfull receivers, where J11 counts only the LONG second receivers. Distinct
aligned physical tiles are disjoint, so every point in this union is counted
once. Nonfull receivers contribute their forced point, full receivers contribute
the forced point and w. Consequently

    |X|+J01+J11 = 2*(C01+L11),
    X intersect Pclosed01 = empty.                             (1)

Here Pclosed01 includes the ORIGINAL endpoints of all phase01 owners on all
closed specified port components. Equation(1) counts positions, not owners.
It is valid also for contacts on open components. Selecting a subfamily of
events preserves injection and gives the corresponding exact count, with
nonfull stops selected from that SAME event family.

The existing single-pool bound B+J01+J11<=2*A+H therefore gives

    |X|+2*A+H >= 2*(C01+L11)+B.                               (2)

This is substitution in the SAME H ledger. It is not an extra payment to add
to a previously spent H bound. A full tile supplies zero H units, and no
separation from cap, irregular-triple or other reserved slots is asserted.

Each point of X is adjacent to one of its own active original pair's endpoints.
Those endpoints lie on the connected original U source. Thus X stays in the
same full endpoint component as its original contact. All counts in a
componentwise use of(1)--(2) refer to that same full endpoint component.

For a chosen union of ell closed neutral curves in one nonexceptional AA
endpoint component, the accepted incidence and turning formulas give
C01=M01-M10>=4*ell. Let L11 now count long exits from those chosen contacts.
Since H=0, the direct shared pool gives J01=J11=0 for this family; A need not
vanish. Equation(1) yields

    |X|=2*(C01+L11) >= 8*ell+2*L11.                           (3)

This strengthens the earlier8*ell outside-endpoint requirement. It neither
forces a positive reserve nor proves that mixed chains terminate.

## 5. Critical points and the remaining gap

Critical phase11 second points are globally distinct from forced first/long
points, but that does NOT separate them from the OTHER opposite endpoint w
of a full first/long receiver. Exact local tag/tile controls still admit such
a coincidence. These are compatible partial stencils, not complete feasible
configurations or counterexamples to a stronger geometric statement. One
cannot add the critical-point count to |X| using the present proof.

A subsequent [complete six-source certificate](CRITICAL_CLOSED_OWNER_COUNTEREXAMPLE.md)
shows a different, stronger obstruction to blanket critical closed-owner
exclusion: a critical second point can be an original full-bar corner of
a phase01 owner on a closed neutral component. This does not establish the
other-corner coincidence above and does not affect the LONG restriction here.

The unrestricted finite complete-source coefficient-one allocation and
rectangular-grid triple equality remain OPEN. The next step is to account for
these disjoint physical receivers through original owners and the existing
reserve, allowing full/critical coincidences, recurring owners and rotor exits.

## 6. Verification boundary

All nine new scoped theorems in
[`NeutralFullReceiverInjection.lean`](../formal/SubQuorum/NeutralFullReceiverInjection.lean)
compile locally with Lean4.33.0, and all nine axiom prints pass using only
propext, Quot.sound and the recorded Classical.choice cases. The physical
tag construction, tile-set and closed-terminal/profile adapters are written
explicitly above; the generic formal injection retains those hypotheses.
See [the formal receipt](../output/full-neutral-receivers-formal-check.json).

Independent controls check all256 same-tile orientation/kind cases. The older
three-point stencil admits32 distinct-point coincidences; the fourth endpoint
removes them all. Original geometry controls check1056 phase01 endpoint images,
36 surviving terminal roles and42 first/long four-run profiles.

Across1024 complete feasible images, the verifier reconstructs104 actual first
receivers:96 full and8 nonfull, yielding200 distinct additional endpoints.
Complete long/critical phase11 exits, closed01 contacts and AA coverage all
remain ZERO. Actual full first receivers are tested; no claim of complete
coverage of the long extension or AA deduction is made. The general argument
is Sections1--4, not inference from those finite controls.
See [the control receipt](../output/full-neutral-receivers-controls.json).

Oracle task9b95cb72-5264-46ce-bea9-cd2b283fc736 continues the accepted phase11
conversation and reviews this proof together with the critical and shared-H
extensions. It ended with a terminal typing infrastructure failure and no
mathematical verdict, as did preceding task88c8a838. After these terminal
failures, a fresh independent audit uploads a single complete context file;
it completed with ACCEPT, with the inherited census/reserve/AA hypotheses
retained. See [the assessment](FULL_RECEIVERS_INDEPENDENT_REVIEW_ASSESSMENT.md)
and full-receivers-independent-review.json. Its nonfull generic Tile adapter
uses the subtype of nonfull physical tiles. The failed tasks provide no
mathematical acceptance or rejection. The later complete critical fixture
was not in the audit packet.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
