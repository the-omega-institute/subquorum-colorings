# A five-endpoint cap forbids every complete-source extension

21 October 2026. A fixed five-endpoint stencil leaves an original support
with no possible endpoint owner, even after arbitrarily many allowed U or
rotor sources are added. This gives a geometric exclusion for the FULL
source catalogue, rather than an exclusion within a bounded placement
search. One consequence is that a width-six positive source cannot have
a positive source as its canonical gate consumer. Positive gate consumers
are possible at larger widths, so their sign cannot be restricted globally.
The unrestricted allocation and rectangular-grid equality remain OPEN.

## 1. The local cap theorem

Use the complete-source hypotheses of SOURCE_RETENTION_HORN_CLOSURE.md:
original endpoints are disjoint, original matchings are retained, all
original supports outside the final endpoint union are mandatory, and
each finally selected point has at most one occupied neighbor. Every U
has even width at least six and independent even leg heights at least
four. All phases, isometries, rotor types and finite source counts are
allowed. No pairwise-feasibility assumption is made.

Precisely, P is the final endpoint union over ALL selected source occurrences,
including every added source. Each occurrence contributes its original endpoint
set; a prescribed source's original endpoint ownership is never reassigned.
T contains every original support outside P, together with any permitted optional selections.
T is disjoint from P. The at-most-one occupied-neighbor
condition applies to T, not to P. A consumed original support belongs to P
and is no longer selected. Every original matching edge stays within its
own source's endpoints; an added endpoint cannot use a prescribed different
source's endpoint as its matching mate. Occupied means membership in P union T.

Suppose a prescribed source subfamily has an original support x=(2,2),
does not already own x as an endpoint, and has endpoints at all five sites

    B={(1,2),(2,1),(3,2),(2,6),(1,4)}.

Then NO complete feasible extension by any allowed sources exists.

Indeed x already has three persistent endpoint neighbors, so it cannot
remain selected. Some added source must own x as an endpoint. Its only
possible same-source endpoint neighbor is y=(2,3), since the other three
neighbors are endpoints of prescribed, different sources. Every original
endpoint has a matching mate among its endpoint neighbors, so y must
belong to this added source and be its unique endpoint neighbor at x.

In a U, the only endpoints with exactly one same-source endpoint neighbor
are its terminal tips. The two bar rows give every bar endpoint at least
two endpoint neighbors; each nonterminal stem point has its two stem
neighbors. From a terminal tip the straight stem continues for at least
four edges, including the upper bar corner. Thus the added U would also
own x+4(y-x)=(2,6), a collision with B. This argument uses only the minimum
height, not a maximum height, width or translation cutoff.

In a rotor, only the four outer endpoints have one endpoint neighbor.
Normalize an outer endpoint to x with its central neighbor y. Up to the
two chiralities, the complete endpoint sets are

    {(0,3),(1,3),(1,4),(1,5),(2,2),(2,3),(2,4),(3,4)},
    {(1,4),(2,2),(2,3),(2,4),(3,3),(3,4),(3,5),(4,3)}.

Both contain (1,4), again a collision. Quarter-turn invariance reduces
all rotor orientations to these two translation families; specifying x
and its unique neighbor y fixes the translations. These are complete
role cases, not a bounded search. This proves the cap theorem. Isometries
and translations transport it to any position and direction.

## 2. Regular singleton consumers activate, with an injective count

Normalize one positive side as in MARKED_SIDE_GATE_CONSUMPTION.md. Its
fixed support gate is t=(3,2), its anchor is (3,1), and its canonical tile
is Q={2,3}x{2,3}. The producer has endpoint (2,1).

Suppose the unique consumer of t has ORIGINAL regular singleton profile
1P2T in Q. Its original supports include p=(2,2) and u=(3,3). The support
p sees both its consumer anchor t and the producer endpoint (2,1).
Hence p must be consumed into an endpoint. The consumer singleton is
therefore activated. This applies to positive terminals and to regular
zero-rotor singleton occurrences alike.

An original regular singleton occurrence is the labelled pair (j,Q) of
its source and physical tile. It is activated exactly when
(T_j intersect Q) intersect P is nonempty, independently of WHICH source
owns the endpoint consuming that support. Thus A counts activated positive
singleton OCCURRENCES, not sources acquiring endpoints or distinct sources.

Let qplus count marked sides whose fixed gate consumer is an original
POSITIVE regular singleton in that side's canonical tile. Then

    qplus <= A,
    2R = qplus+(A-qplus)+U0+Z0+H,
    mu >= N-G+ceil(qplus/2).

The injection is geometric: all original positive canonical donor tiles
are distinct, by the established seven-endpoints-in-a-twelve-site-ring
argument. The consumer occurrence uses the SAME physical tile Q as the
producer's canonical side, because its sole endpoint is the gate t in Q.
Equality of two target occurrences would imply equality of these producer
canonical tiles, hence equality of the original sides. Each counted gate
therefore maps to a different consumer
singleton occurrence (source, tile). It cannot use one activated terminal
twice, even if several sides have the same consumer source.

This identifies HALF a reserve unit per counted side. It does not spend
the same A occurrence again, add qplus to the existing A bound, or assert
that a side has received a full unit. For zero-rotor consumers activation
alone is not an extra reserve unit: its paired triple may be full, so
the established rotor forwarding cancellation still applies.

## 3. A forced transverse negative tip, and the width-six exclusion

There is a stronger all-width consequence of the same cap argument.
Suppose a canonical gate consumer has original support p=(2,2), as every
regular singleton consumer does, and p is not an endpoint of the prescribed
producer or consumer. Then p has three persistent endpoint
neighbors (1,2),(2,1),(3,2) and must be consumed by a THIRD source. Its
only possible same-source endpoint neighbor is (2,3). A rotor owner is
impossible already from the four blockers (1,2),(2,1),(3,2),(1,4), without
using the fifth blocker (2,6). The two rotor outer-role sets in Section 1
both meet (1,4).

Thus the third source is a U whose terminal tip is p, with a straight
stem pointing right. Write h for that stem's original even height. The
stem endpoints include (2,2+j) for EVERY 0<=j<=h. The producer has endpoint
(2,w), so disjointness forces h<w-2. Since h and w are even,

    4 <= h <= w-4, and hence w>=8.

This forced U is NEGATIVE: p and its matching-side neighbor (2,3) lie in
the same physical tile, whereas every positive U terminal is an original
regular singleton. Original endpoint ownership of the producer and consumer
is retained; the third source must contribute its own original endpoint at p,
thereby consuming their original support there.
It is a forced transverse source with an explicitly bounded relevant leg,
not an assumed route or an extra reserve pool.

For a width-six producer, the regular singleton consumer in Section 2
would have original support x=p=(2,2). The producer supplies endpoints
(1,2),(2,1),(2,6),(1,4), and the consumer supplies endpoint (3,2).
These are precisely the cap stencil B. None of the already prescribed
sources has an endpoint at x: it is the consumer's original support and
is inside the producer's empty canonical tile. Section 1 rules out EVERY
complete extension. This also excludes zero-rotor regular singletons;
the consumer need not be positive for this conclusion.

In particular the following explicit reciprocal positive pair is
uncompletable: U(6,4,4) and its image (r,c)->(7-r,c-4). Their gates
(3,2) and (4,1) are endpoints of the other source, respectively. Their
second gate is the image of the reference RIGHT gate (3,5); it maps to
(4,1), while the first gate is the reference LEFT gate (3,2). Their
endpoint sets are disjoint, but the first forced support (2,2) has the
unfillable cap above. No number or dimensions of additional sources repair
the pair. This excludes the configuration itself, rather than merely a
candidate compensation rule. It is not an allocation counterexample.

## 4. A width-six positive cannot have a positive gate consumer

Here is the remaining catalogue argument, including non-singleton roles.
Suppose a positive U consumes t in Q. Its original profile in Q is one
of 1P2T, 2P1T or 4P0T; the positive phase has no other endpoint profile.
Section 3 excludes 1P2T in any complete extension.

For 2P1T, its other endpoint is p=(2,2) or u=(3,3). If that endpoint is
p, both neighbors of p outside Q, (1,2) and (2,1), belong to the producer.
Thus p has exactly one endpoint neighbor in its own source, namely t.
It would have to be a terminal tip. But a positive U terminal has
singleton profile, not 2P1T, a contradiction.

Otherwise the pair is {t,u}. If its original support is p, the same cap
argument applies. The only other possible support is r=(2,3). In that
case the other intratile neighbor p of t is originally blank. A positive
U endpoint in a regular pair with an adjacent intratile blank continues
straight past the pair: reflection of its paired neighbor through it is
another original endpoint. For a stem pair this is the next stem point;
positive terminal tips are singletons. For either bar-end pair it is the
first stem point; the other bar corner has a support rather than a blank
at that neighbor. This verifies the continuation directly in the complete
positive catalogue and transports under isometries. Applied at t, with
paired neighbor u, it would put the producer anchor (3,1) in the consumer's
original endpoints. That collision excludes the last regular-pair case.

For completeness, the continuation used here is a separate local lemma:
in any original positive 2P1T pair, if an endpoint has an adjacent intratile
blank, reflection of its pair neighbor through it is an original endpoint.
Here is its complete normalized proof. The only regular pairs are the
two bar-end pairs and the straight stem pairs:

| Pair endpoints | Its intratile support | Endpoint with the intratile blank | Reflected continuation |
|---|---|---|---|
| (0,1),(1,1) | (0,0) | (1,1) | (2,1) |
| (0,w),(1,w) | (0,w+1) | (1,w) | (2,w) |
| (2k,1),(2k+1,1) | (2k,0) | (2k+1,1) | (2k+2,1) |
| (2k,w),(2k+1,w) | (2k,w+1) | (2k+1,w) | (2k+2,w) |

The left stem rows have 1<=k<=a/2-1; the right have 1<=k<=b/2-1.
Thus the displayed continuation always exists, including the final pair
before a terminal singleton. The other endpoint of each pair has a support
at its other intratile neighbor, so it is not a blank case. Interior bar
tiles are full and terminal tiles are singletons. This exhausts the
positive pair catalogue for arbitrary even dimensions, and a physical
isometry transports the statement together with its original tile.

For 4P0T, Q is part of the consumer's two-wide bar. A horizontal bar
of length at least six containing Q intersects one of the producer's
stems at column 1 or 6 in row 2 or 3. A vertical bar has columns 2,3
and a consecutive row interval [L,L+v-1], v>=6, containing rows 2 and 3.
Thus L<=2. If L<=1 the bar includes the producer endpoints (1,2),(1,3).
If L=2, a horizontal stem is attached at its row-2 end. A left-going stem
reaches (2,1); a right-going stem, of height at least four, reaches (2,6).
Both are producer endpoints. This direct interval/stem argument is
independent of orientation parity and covers every reflection and rotation.
It exhausts all positive-consumer profiles.

Consequently every actual positive-to-positive gate incidence has a
producer of width at least eight. The general positive-consumer example
in the translated nine-source family is consistent with this restriction.
No sign restriction for consumers at larger widths, no directed-acyclicity
claim, and no payment of non-singleton consumer channels follows here.

The rotor case can also be exhausted at the GATE itself. The producer's
seven fixed endpoints are

    {(1,1),(1,2),(1,3),(1,4),(2,1),(3,1),(4,1)}.

Among all sixteen original rotor endpoint roles placed at t=(3,2), only
Rplus(2,0) and Rminus(1,6) avoid this set. Here Rplus(a,b) translates the
reference rotor, while Rminus(a,b) applies (r,c)->(r+a,-c+b). The reference
rotor's complete original support set is

    {(0,2),(1,1),(2,5),(1,4),(5,3),(4,4),(3,0),(4,1)}.

The support assertion follows from these two explicit inverse-coordinate checks:

| Surviving role | Reference endpoint mapping to t | Inverse image of p | Original support membership |
|---|---|---|---|
| Rplus(2,0) | (1,2) | (0,2) | (0,2) belongs to the displayed support set |
| Rminus(1,6) | (2,4) | (1,4) | (1,4) belongs to the displayed support set |

Thus neither surviving rotor owns p as an endpoint, and both have original
support p=(2,2). Section 3 forces a transverse negative U and
w>=8. In particular NO rotor can consume a width-six positive gate.
Combining this with the positive-U exclusion proves:

    Every width-six positive gate consumer is a negative U source.

This conclusion concerns actual fixed gate consumers, distinct from the
earlier assigned negative witness-endpoint role. It does not impose that
sign restriction on wider positive producers.

## 5. Verification and the remaining global question

The general cap proof, activation injection and positive-consumer exclusion
are Sections 1--4. The checker independently reconstructs original U
matching/support data, verifies all one-neighbor U roles on parameter
controls, exhausts the sixteen rotor ownership roles without a translation
cutoff, checks the explicit reciprocal pair, and audits endpoint-disjoint
positive consumer profiles. Its parameter controls are supplementary;
their finite ranges do not prove the arbitrary-parameter statements.

The Lean source checks normalized terminal classification and continuation,
the sixteen rotor owner-role collisions at both cap and gate, the abstract
five-endpoint contradiction, the singleton activation stencil and the
even-height bound. The source-to-support forcing uses the explicit
unique-anchor feasibility hypothesis in the activation lemma.
The arbitrary-source role adapter, isometry transport, canonical-tile
injection and positive profile/bar classification remain written. No
end-to-end Lean claim for the geometric theorem or full target is made.

For the unrestricted signed-loss problem, regular positive singleton
consumers now have a fixed, nonreusable A occurrence, whereas positive
pair/bar consumers and negative/rotor forwarding remain to be controlled
together. The cap stencil also supplies a local obstruction that any
proposed saturated configuration or global routing must avoid. Neither
the full allocation mu>=0 nor grid equality is established.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
