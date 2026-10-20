# The critical phase11 band forces a disjoint second endpoint too

20 October 2026. Every phase11 owner of a first neutral01 forced point now
produces an additional distinct original endpoint, including the previously
unresolved critical case a=v+2. A physical-tile corner invariant is essential
for separating these critical points from the existing point sets. This
extends the accepted long-case endpoint count; it does not create independent
reserve payments or settle coefficient one or rectangular-grid equality.

## 1. Standing hypotheses and the two even cases

Use precisely the complete finite original U/rotor source, ownership, fixed
transported tile partition and mandatory support hypotheses in
[the accepted phase11 theorem](NEUTRAL_PHASE11_CORNER_AND_SECOND_FORCE.md).
Normalize an actual neutral01 contact to first forced point z=(0,0), active
terminal p=(1,-1), passive q=(1,0), and frame s=N,d=E. The active phase01
source O has width W, incident height a and opposite height b, all legal even
dimensions. In normalized coordinates its inverse map is

    (r,c) -> (r+a-1,c+2).

The original passive source B has every endpoint in row at least1. The first
forced owner F differs from O and B. If F is phase11 of width v, the accepted
role theorem makes it an outer bar corner with bar north and legs east,
and gives v+2<=a. Evenness leaves exactly two cases:

    long: a>=v+4;     critical: a=v+2.

The long case already forces y=z+v*s. Those points are injective across all
long contacts and disjoint from every first forced point. Write their set
Ylong and their contact set L11. The present note resolves the critical case.

## 2. An occupied band cannot end at the opposite terminal

Assume a=v+2. Let h be F's leg height at the NORTH end of its bar, opposite
the corner z. In the two allowed inverse frames h is left or right respectively:

    pull true false false (0,v): h=left;
    pull true false true  (0,1): h=right.

The opposite leg contains every (1-v,c),0<=c<=h. Its terminal is (1-v,h),
and its original terminal support is

    t=(1-v,h+1).

This support is not an F endpoint. These are exact consequences of the
canonical endpoint/support predicates, for arbitrary v,h and the other leg.

O's far stem owns (1-v,W-2): its canonical coordinates are (2,W), and b>=4.
If h>=W-2, this point is also on F's opposite leg, violating original endpoint
disjointness. Since h and W are even,

    h+4<=W.                                                     (1)

In particular W>=8: a width6 active source admits no critical phase11 branch.
This restriction is obtained from the complete opposite stem, not just from
the original four endpoint blockers.

Now O's inner bar has row -v and occupies columns[-1,W-2]. Equation(1) puts
(-v,h+1) in that bar. Thus t has two persistent occupied cardinal neighbors:

    O anchor: (-v,h+1),     F anchor: (1-v,h).

If t lay outside final P, F's original support would have to be retained,
giving it two occupied neighbors. This contradicts the degree-one condition.
Therefore t is an original endpoint. It belongs to none of O,F,B: its O
inverse coordinates are (2,h+3), strictly between the two stems; it is F's
original terminal support, not an endpoint; and its normalized row1-v<0
excludes B. The owner need not be globally fresh.

The active source also supplies three endpoints immediately above t:

    t+s-d, t+s, t+s+d,

all tagged by its phase01 predecessor s. F supplies t-d and t-2d, both
tagged none under the established phase01-only endpoint tag. The three O
points have canonical coordinates (1,h+2),(1,h+3),(1,h+4), all in its bar
by(1). The F points lie on its opposite terminal run because h>=4.

## 3. Physical tile corners remove the apparent coincidences

Tag every original phase01 endpoint by some(predecessor direction), and every
other point by none, exactly as in the accepted global injection proof.
Relative to their forced positions, the three types have these stencils:

| Type | phase01 sites and tags | Other sites and tags |
|---|---|---|
| First point z | -s-d,-d,s-d: some s | -s,-s+d: some d |
| Long second point y | -s-d,-d,s-d: some s | -s,-s+d: none |
| Critical second point t | s-d,s,s+d: some s | -d,-2d: none |

Tags ALONE do not suffice for the critical points. With the first critical
frame fixed to(N,E), they permit four critical frames, one long frame and two
first-point frames. One must not promote a tag-only count to an injection.

The missing invariant is the opposite corner of the actual physical tile.
The normalized partition has both lower-corner coordinates odd because the
receiving tile of z=0 is[-1,0]^2. For an even normalized coordinate, its partner
in that tile interval is one smaller; for an odd coordinate it is one larger.
Thus z and long y=(-v,0), whose coordinates are even, have opposite-corner
displacement(-1,-1), while critical t=(1-v,h+1), whose coordinates are odd,
has displacement(1,1). Transporting back through the actual signed isometry
gives the coordinate-free displacements

    first or long: s-d;     critical: -s+d.                     (2)

The physical partition is never reset. At one physical point, its tile's
opposite-corner displacement is a single fixed vector. Equal forced positions
must therefore have equal vectors in(2). The formal normalized parity lemmas
prove both partner formulas. Arbitrary signed coordinate permutations preserve
opposite corners, so their vector transport gives(2) in every cardinal frame.

Exhaust the eight ordered perpendicular cardinal frames. For a critical frame
(N,E), a shared tile corner allows a second critical frame only(N,E) or(W,S).
The latter puts a differently tagged active site at(-1,-1). Hence critical
coincidence forces equality of frames. A first or long point at the same
tile corner would require frame(S,W) or(E,N). Each conflicts with the critical
stencil: for(S,W), first/long active point(-1,1) has tag some S versus critical
some N. For(E,N), a first-point passive site(0,-1) has tag some N, whereas
the critical F endpoint there has tag none; a long-point corner site(-1,-1)
has tag none, whereas the critical active endpoint there has tag some N.
The exact ordered-frame proof checks
all64 pairs for each comparison; no dimension or placement enumeration is
being used to prove the general orientation claim.

## 4. Global critical injection and the all-phase11 count

Suppose two critical contacts force the same t. Tags plus(2) give the same
frame(s,d). Their F owners share the terminal endpoint t-d, so original
endpoint uniqueness identifies the same original source F. This step is
independent of v or h.

The source has a fixed width v. Its terminal point t-d has a unique incident
height h in the original source model: canonical terminals are(left,1) and
(right,v), with distinct columns because v>=6. Therefore the original source
and this fixed terminal determine h, even if the two leg heights agree.
Recover

    z=t-(v-1)*s-(h+1)*d.

Both first forced points agree. The accepted first-point injection identifies
the original contact. Thus critical second points are globally injective.

The first/critical and long/critical stencil incompatibilities with(2) show
that their point sets are disjoint. Combined with the previously accepted
first/long separation, this gives three pairwise disjoint sets. Let C11 denote
the set of critical contacts and N11 the number of ALL actual neutral01
contacts whose first forced owner is phase11. Write Ycritical for their new
points, and Y11=Ylong union Ycritical. Then

    N11=|L11|+|C11|,
    |Y11|=N11,  Y11 intersect Z01 is empty,
    |Z01 union Y11|=C01+N11.                                   (3)

All are original endpoint positions. No distinct-owner assumption is used,
and these positions are not claimed independent of opposite full-receiver
endpoints, cap reservations, irregular-triple capacity or other witness pools.

## 5. Formal and computational boundary

All ten critical-geometry and eight critical-injection theorems compile locally
with Lean4.33.0. Together with the seven shared-budget theorems, all25 scoped
axiom prints pass using only propext, Quot.sound and, where reported,
Classical.choice. The execution receipt is
[`phase11-critical-shared-budget-formal-check.json`](../output/phase11-critical-shared-budget-formal-check.json).
Independent review task88c8a838-d1cb-407b-a50f-6ef7ef3f9492 ended with a terminal
typing infrastructure failure and no mathematical verdict. A shorter replacement
in the same conversation includes [the full-receiver extension](FULL_FIRST_AND_LONG_RECEIVER_INJECTION.md);
its review status is recorded separately. No acceptance is inferred from failure.

`NeutralPhaseElevenCritical.lean` proves the opposite-leg profile, critical
far-stem collision/height bound, active bar stencil and blank, degree-one
forcing, passive exclusion, normalized tile partners and exhaustive even
case split. `NeutralPhaseElevenCriticalInjection.lean` proves all ordered-frame
incompatibilities, owner/terminal recovery, global injection and three-set
counting. The physical tag and tile-diagonal adapters are written explicitly
in Sections2--4; source uniqueness precedes all dimension-dependent recovery.

The controls reconstruct216 source pairs, of which186 have disjoint endpoints
and30 hit the active far stem;1488 isometry images preserve the actual aligned
partition. They check the three64-pair tag/partition comparisons separately.
The critical tag-only survivor count32 drops to8 with the physical corner;
long and first tag-only survivor counts8 and16 both drop to0.

These are partial stencils. Complete feasible critical phase11/closed01/AA
coverage remains ZERO. The existence of a complete configuration satisfying
these local branches is not inferred from endpoint-disjoint pairs. General
implications(1)--(3) use the complete-source assumptions and proofs above.

The long-second receivers can additionally join the established nonfull-stop
budget, as proved in [the shared-budget note](SECOND_FORCED_RECEIVERS_SHARED_BUDGET.md).
Critical second points do not have that same original-pair receiving profile;
they are excluded from that particular H charge. The full unrestricted reserve
inequality, mixed-chain termination and rectangular-grid equality remain OPEN.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
