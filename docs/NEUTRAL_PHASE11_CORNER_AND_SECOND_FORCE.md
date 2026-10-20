# Phase11 forced owners are corners and can force another original owner

20 October 2026. Under the complete original-source hypotheses, a phase11 U
owning the forced point of an actual neutral01 contact cannot be a terminal.
It must be a particular bar corner. Its receiving tile is full, and the next
tile to the east contains an exact original irregular triple of that source.
The source width is at least two shorter than the active incident height.
Except at that smallest even separation, another original endpoint is forced
outside all three sources of this local configuration. These are local
arbitrary-dimension deductions, not coefficient-one or grid-equality theorems.

## 1. Hypotheses and normalization

Use the finite complete U/rotor source model of
[the forced-support injection theorem](DISTINCT_NEUTRAL_SUPPORTS_AND_ANY_PAIR_BUDGET.md):
legal even dimensions, pairwise disjoint original endpoint sets, unchanged
original matchings, mandatory support retention outside final P, and occupied
degree at most one for every retained support. Adjacency is cardinal. Original
supports that lie in P are consumed and not retained. Optional selections do
not remove original endpoints or the mandatory-support obligation.

Normalize one actual neutral01 contact, transporting its physical partition,
to active terminal p=(1,-1), passive terminal q=(1,0), and forced point z=(0,0).
The active source O has predecessor north and its other leg east. Its incident
height is a. In particular it owns

    (2-a,0) and every (t,-1) with 1-a<=t<=1.

These are its inner bar point and full collinear endpoint run. Its width is
at least6. The passive source B has predecessor east; its entire endpoint
set has normalized row at least1. The original forced-point argument proves
that z lies in P and belongs to neither O nor B. Write F for its original
owner, and suppose F is a phase11 U of width v and leg heights h,k, all even,
with v>=6 and h,k>=4. Do not assume F is a fresh owner at other contacts.

Write the actual inverse isometry as
`pull transpose flipRow flipColumn anchor point`. The normalized receiving
tile is [-1,0]^2. The proved lower-corner adapter in
[the phase10 note](NEUTRAL_PHASE10_DESCENT_AND_FULL_PAIR_EXIT.md) applies unchanged:

    origin = (anchor.row - (0 if flipRow else 1),
              anchor.column - (0 if flipColumn else 1)).

Phase11 means BOTH canonical origin coordinates are odd. Therefore

    anchor.row mod2 = 1 if flipRow else0;
    anchor.column mod2 = 1 if flipColumn else0.

Original-owner uniqueness excludes F from the four foreign endpoints
(0,-1),(-1,-1) of O and (1,0),(1,1) of B, exactly as in the phase10 adapter.

## 2. Exhaustive roles and elimination of all phase11 terminals

Split the canonical endpoint predicate into bar, near leg and far leg, and
split the eight signed coordinate permutations. Under those four blockers
and phase11 parity, only the following two types remain:

| Type | transpose | flipRow | flipColumn=false | flipColumn=true |
|---|---|---|---|---|
| Northward terminal, other leg west | false | false | anchor=(k,v) | anchor=(h,1) |
| Outer bar corner, bar north, legs east | true | false | anchor=(0,v) | anchor=(0,1) |

This exhaustion is a general case proof for arbitrary dimensions, checked by
`phase_eleven_forced_owner_role`; finite endpoint images only check the table.

The terminal type is impossible. Let s be its incident height. If s<=a, F's
inner bar contains (1-s,-1), and 1-a<=1-s<=1. O owns that point on its
collinear run, contradicting endpoint disjointness. If s>a, F's incident run
in column0 contains O's bar endpoint (2-a,0), another contradiction. The same
argument covers both reflected forms; no height bound or evenness is needed
for this terminal elimination beyond the legal minimum dimensions.

Thus **every physical phase11 U owner of z is the corner type in the table**.
The assembled Lean theorem derives parity and blockers from physical
tile-origin residues and unique original ownership, then uses O's actual
bar and run to eliminate the terminal. It does not assume the corner role.

## 3. Full receiver and an adjacent original irregular triple

In either corner form, F owns (-1,0),(0,0). Its forced receiving tile
[-1,0]^2 therefore contains those two endpoints opposite O's endpoints
(-1,-1),(0,-1), and is full2+2.

The adjacent physical tile Qe=[-1,0]x[1,2] contains exactly these F endpoints:

    (-1,1), (0,1), (0,2).

F owns neither (-1,2) nor any original support in Qe. Thus Qe has an exact
original3P0T profile for F. This statement concerns F's original profile;
another source may fill its fourth corner in the final configuration.
No final H contribution, unused reservation slot or new payment follows.

F also owns the full bar run (t,0) for 1-v<=t<=0, and has an original
bar-end support at y=(-v,0), which is not its own endpoint. These assertions
are direct consequences of the exact canonical endpoint and support
predicates, proved in `phase_eleven_corner_exit_geometry`.

## 4. Width restriction and a second forced original endpoint

O's endpoint (2-a,0) cannot lie on F's run [1-v,0]x{0}. Since a>=4,

    2-a < 1-v, hence a > v+1.

The even legal dimensions give

    v+2 <= a.                                                   (1)

The proof uses actual unique original ownership, not an independent width
assumption. Consequently active incident heights4 and6 exclude phase11
owners entirely. Together with the accepted phase10 height theorem, these
short active legs admit neither phase10 nor phase11 U owners at z. Positive,
other phase01 and rotor owners are still possible branches to analyze.

There are now two even cases. If a=v+2, y=(-v,0) is exactly O's inner-bar
endpoint (2-a,0). The original F support is already consumed by O; this
particular support produces no new owner. This is a local geometric boundary
case, not an asserted complete feasible family or a proof of closure.

If a>=v+4, y is an original support of BOTH O and F. For O, the normalized
inverse coordinates of y are (a-1-v,2). Their row is odd, at least3, and at
most a-1; thus this is an inward near-stem support. Its persistent O anchor
is y+W=(-v,-1). For F, y is the opposite bar-end support and its persistent
anchor is y+S=(1-v,0). The two anchors are distinct cardinal neighbors of y.

If y were outside final P, mandatory retention would select it; the two
persistent anchors would then give occupied degree at least2, impossible.
Therefore

    y=(-v,0) belongs to P.                                     (2)

Its owner differs from all THREE sources O,B,F: its O inverse coordinates
(a-1-v,2) are not an endpoint; its F inverse coordinates are a bar-end
support, not an endpoint; and its negative normalized row excludes B.
The latter fact follows directly from the passive isometry: canonical
column equals normalized row, while every canonical U endpoint has positive
column. The Lean geometry theorem proves the two supports, the two anchors,
and both relevant nonmembership assertions. The degree-one implication is
the already proved two-distinct-anchor consumption lemma.

This proves the following local continuation statement:

> A phase11 owner of a neutral01 forced point is an outer bar corner with
> v+2<=a. If a>=v+4, its opposite bar-end support forces an original endpoint
> belonging to none of the active, passive or phase11 owners.

The owner of y may already occur elsewhere. The next section proves that
different long phase11 contacts have different y, and that no such y equals
ANY first forced point. Neither statement supplies a decreasing rank on mixed
continuations or an additional shared reserve. The nearby original irregular
triple is already part of the original charge census, so treating it as fresh
slack would risk counting the same capacity twice.

## 5. Global injection and separation from every first forced point

Let L11 be the set of actual neutral01 contacts whose first forced owner is
phase11 and whose active height satisfies a>=v+4. For a contact with first
forced point z and cardinal frame (s,d), define

    y = z+v*s.

In the preceding normalization s=N and y=z+(-v,0). Tag EVERY original phase01
endpoint by `some s_owner`, where s_owner is its terminal predecessor
direction. Tag every other point by `none`. Original endpoint disjointness
makes this a well-defined single tag; both legs of a phase01 source have
the same directed predecessor. This construction does not tag only terminals.

Relative to y, the active owner has the three endpoints

    -s-d, -d, s-d, all tagged some s;

and F has endpoints

    -s, -s+d, both tagged none because F is phase11.

The new `long_corner_has_tagged_endpoint_stencil` theorem proves their actual
endpoint membership, using a>=v+4. In the base frame these are the active
points (-1,-1),(0,-1),(1,-1) and the F points (1,0),(1,1).

Suppose two contacts have the same y. Normalize the first frame to (N,E).
The seven different second frames contradict the single tag at these sites:

| Second frame | Shared site | First tag | Second tag |
|---|---|---|---|
| (S,E) | (0,-1) | some N | some S |
| (S,W) | (-1,-1) | some N | none |
| (E,S) | (0,-1) | some N | none |
| (E,N) | (0,-1) | some N | none |
| (N,W) | (1,-1) | some N | none |
| (W,S) | (-1,-1) | some N | some W |
| (W,N) | (1,-1) | some N | some W |

Thus their frames agree. They then share F's anchor y-s, so endpoint uniqueness
identifies the same original phase11 source F, including its fixed width v.
Recover z=y-v*s. The first forced points agree, so the accepted global first
forced-point injection identifies the same contact. This proves injection
of y on ALL of L11, across open or closed port components and recurring owners.
`second_forced_points_are_injective` formalizes the frame, owner and recovery
argument using unique original ownership and the already proved first-point
injection as explicit hypotheses.

There is also separation from the entire first forced-point set Z01, not
just from first points of L11. At a first forced point the active sites have
tags some s and the passive sites have tags some d. At a second forced point
the active sites have tags some s' and the two F sites have tag none. If the
positions coincided, the same eight frames give a contradiction. In frame
(N,E), the tag of (1,0) would be both some E and none; the other seven frames
have the active-site or phase conflicts listed above. The Lean proof exhausts
all ordered pairs of the eight cardinal frames, so it includes arbitrary
orientation of both contacts, not just a fixed base-frame hypothesis.

Writing Y11={y(c):c in L11}, the resulting exact joint count is

    |Y11|=|L11|,  Y11 intersect Z01 is empty,
    |Z01 union Y11|=C01+|L11|.                                  (3)

Here C01 counts all actual neutral01 contacts. Both sets consist of original
endpoints. Equation(3) counts positions once; it does not count distinct owners
or independent payments. Opposite endpoints of full receivers, older cap
reservations and other witness families are not asserted disjoint from Y11.
That additional shared-capacity question remains part of the unrestricted task.

## 6. Verification and remaining task

`formal/SubQuorum/NeutralPhaseElevenExit.lean` contains eleven theorem declarations
and one parity-helper definition. Its inputs expose the physical inverse
isometry, original ownership uniqueness and transported origin residues.
The conversion from a geometric neutral01 contact to the normalized active
bar/run and passive orientation is written here and in the accepted contact
theory; the new proofs do not rely on a bounded dimension search.
`formal/SubQuorum/NeutralPhaseElevenInjection.lean` adds five theorem declarations
for exact frame uniqueness, first/second stencil incompatibility, global
second-point injection, global first/second separation and duplicate-free
combined counting. The tag stencils, unique-owner anchor and recovery map
are connected to the physical geometry in Section5.

`develop/check_neutral_phase11_exit.py` reconstructs source modules, checks
the exact role table and adjacent original triple, tests actual endpoint
collisions over varied heights, checks both y cases from original support
sets and verifies the endpoint tags and all ordered cardinal-frame pairs.
These are partial source stencils, not complete feasible configurations.
Complete phase11-exit, closed01-contact and AA coverage are all zero in these
controls. No graph counterexample or full allocation claim is based on them.

The remaining unrestricted problem is to handle these corner/triple exits
and second forced points together with long phase10, positive, phase01 and
rotor branches using one consistent count. Equation(3) resolves duplication
between the first and these second endpoint positions, while the conversion
of those positions into a shared reserve remains unproved.
Coefficient one and rectangular-grid triple equality remain OPEN.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
