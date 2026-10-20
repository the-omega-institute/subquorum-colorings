# Rotor activation transfer and the exact negative-U path deficit

21 October 2026. Work in the complete original U/rotor model, with every
hypothesis of [source retention](SOURCE_RETENTION_HORN_CLOSURE.md),
[canonical gates](MARKED_SIDE_GATE_CONSUMPTION.md) and the
[exact geometric reserve](EXACT_GEOMETRIC_EVENT_RESERVE.md). N counts positive
sources, not all owners. Every original endpoint and matching edge retains
its owner; every unconsumed original support remains selected. Arbitrary
permitted dimensions, phases, isometries and finite source counts are allowed.
All coordinates use the fixed aligned two-by-two tiles.

The full unrestricted allocation mu=N+R-G>=0 and rectangular-grid triple
equality remain OPEN. This note proves a source-level rotor transfer, a
nonreusing path allocation and geometric restrictions on the remaining debt.
The path identity below is a reduction of the target, not its solution.

## 1. Normalization and the established positive channels

Normalize a positive producer A=U(w,l,l') and its marked side to gate
t=(3,2), support corner p=(2,2), other corner y=(3,3), and physical tile
Q={2,3} squared. Its anchor is (3,1). Each positive side is paired with
the terminal on that same original leg. Hence there are exactly2N side
vertices and exactly A activated vertices in the notation of the reserve
identity2R=A+C, where

    C=U0+Z0+L1+2L2bar+2L2mutual+L3.

Use the [proved positive-consumer injection](PAIR_GATE_TRANSFERS_AND_PROTECTED_DEFECTS.md).
Its singleton S channel targets the consuming positive terminal. Its pair
P channel has recipient B=U(W,a,b), frame T(r,c)=(c+2,r+2), and targets
that incident terminal. The forced negative U is

    C0=U(V,h,f), frame (r,c)->(c+1,h+2-r),
    4<=a, a+2<=h<=w-4.                              (1)

Targets are actual activated terminal occurrences, and positive S/P targets
do not repeat, including mixed-channel collisions.

We will also need a producer-activation fact for S. If its consuming terminal
has original incident length b, the singleton consumer's incident frame is

    (r,c)->(b+3-r,3-c).                              (2)

The intratile north/east neighbors are its original supports, while the
west neighbor belongs to A. Its own predecessor is therefore south,
forcing (2). Its bar contains (b+2,1), so disjointness from A's incident leg
forces b+2>l, hence b>=l by evenness. Its column-two endpoints include
(l+1,2). A's original beyond-tip support (l+1,1) then has that endpoint
and A's terminal (l,1) as occupied neighbors. Complete feasibility forces
consumption of the support. Consequently the PRODUCER terminal is activated
too. This does not create a second activation at the recipient.

## 2. Every rotor consumer forces a positive companion

**Rotor theorem.** Every rotor gate consumer has the normalized footprint

    B0={(3,2),(4,2),(4,3),(4,4),
        (5,1),(5,2),(5,3),(6,3)}.                    (3)

It is a negative rotor. The producer incident length is l=4, its terminal
is activated, and w>=12. A positive U companion has a terminal at y=(3,3),
with incident frame

    D=U(d,g,e), frame Vg(r,c)=(c+2,g+3-r),
    4<=g<=h-4, 8<=h<=w-4.                          (4)

The companion terminal is activated. Transfer R assigns the original marked
side to this specific companion terminal, not to either rotor singleton.

Here is an exhaustive rotor-role proof, independent of source dimensions.
A rotor has four central endpoint roles and four tip roles in either
chirality, giving sixteen distinct endpoint footprints at t. Six central
roles require the west neighbor (3,1), already owned by A. The other two
require (2,1) or (4,1). West-pointing tips meet (3,1). North-pointing tips
meet (2,1) or (1,1). One south-pointing tip meets (4,1), and one east-pointing
tip meets (1,3). Besides (3), the sole surviving endpoint footprint is

    {(3,2),(3,3),(4,3),(5,3),
     (2,4),(3,4),(4,4),(4,5)}.                       (5)

Both survivors have original support p. The all-width transverse-tip theorem
forces a negative U endpoint at p pointing east, including (2,4). Thus (5)
is impossible. This uses the established four-blocker cap argument, with
no width cutoff or assumption that the transverse source was already given.

For (3), its endpoint (5,1) and A's incident leg force l=4. It consumes the
producer's original beyond-tip support, so that terminal is activated.
Its support p forces C0 in (1). The upward-bar direction meets A's top bar,
so the frame displayed there is forced, with4<=h<=w-4.

The original support y of C0 sees the rotor endpoints t and (4,3), and
must be consumed. At y, north is a C0 endpoint and west/south are B0
endpoints. The new owner's only possible own endpoint neighbor is east.
It is a terminal. The two east-pointing rotor-tip footprints meet (2,4)
of C0 or (4,4) of B0. Therefore it is a U terminal pointing east.

Its north-directed bar is impossible: avoiding A's far stem first forces
its bar columns inside A's width, and the bar would cross A's top row.
The remaining frame is Vg. Its row-three stem must avoid C0's bar at
columns h+1,h+2, so g+3<h+1, hence g<=h-4 by evenness. This proves (4)
and w>=12. The frame preserves physical tiles and gives a positive source.
Its original intratile supports (2,3) and (3,2) are consumed by C0 and B0,
respectively. It is one actual activation, even though both supports vanish.

## 3. All S/P/R transfers are jointly injective

The established S/P injection already handles its two same-channel cases
and its mixed collision. For R, the companion terminal and its incident
direction determine its original beyond-tip support t. This fixes the
unique rotor endpoint owner. Of t's two neighbors outside Q, (4,2) belongs
to that rotor; only (3,1) can be the positive producer's anchor. The distinct
canonical-tile theorem identifies a unique producer side. Thus R targets
do not repeat.

An R target cannot also be an S target. At y the two possible producer
anchors outside its physical tile are (3,4), owned by its companion, and
(4,3), owned by the rotor. Neither can belong to a different positive owner.

An R target cannot also be a P target. A P target determines its recipient
incident frame and hence its hypothetical preceding producer frame. Here it
would be Vg composed with T inverse:

    (r,c)->(r,g+5-c).

That positive producer would own (0,g+4), the image of its endpoint (0,1).
But g+4<=h<=w-4, so this is an endpoint of the original A top bar. If the
hypothetical producer is another owner, this violates endpoint disjointness.
If it were A itself, its bar interval would have to equal
[g+5-width,g+4]=[1,w], forcing g+4=w, the same contradiction. Thus this
case is excluded even when the producer source might otherwise coincide.

**Theorem 1.** All marked sides with positive or rotor gate consumers inject
into distinct actual positive terminal activations. Denote their number by q.
Then q<=A. S and R edges also activate their producer side. Every remaining
marked side has a negative-U consumer.

The negative/positive distinction in the collision proofs concerns actual
source signs. Different names or different transfer types alone do not
establish nonreuse.

## 4. Explicit allocation along paths and cycles

Make the2N positive side occurrences the vertices of a directed graph. Draw
one edge for each S/P/R transfer. A vertex has outdegree at most one by
unique gate consumption and indegree at most one by Theorem1. Every target
is activated and every edge source is marked. Components are directed paths
or cycles, with isolated vertices regarded as paths of length zero.

Give vertex v its one base unit bv and, exactly when activated, its actual
activation unit av. A marked vertex requires two units. For an edge v->z,
pay v with bv+az. Injection makes all these payments disjoint. Every cycle
is fully paid with no leftover positive units.

For a path v0->...->vk, the unused positive units are exactly bvk and,
if activated, av0. Every vertex except the sink has already had its mark
paid. If the sink is marked, its consumer is negative U: otherwise it would
have an outgoing edge. Pay that sink with these remaining positive units.
It is fully paid if the initial vertex was activated, and otherwise lacks
exactly one unit. An unmarked sink leaves1+a(v0) units unused.

Let Bbad count paths whose initial vertex is unactivated and whose sink is
marked. Let Sunmarked=sum(1+a(v0)) over paths with unmarked sink. Counting
the actual units, with C the existing non-A reserve units, gives

    2mu=C+Sunmarked-Bbad.                            (6)

This is an EXACT identity, not just a bound. Equivalently, if r0 is the
number of activated graph roots and qneg is the number of marked sinks,

    2mu=C+(2N-q)+r0-2qneg.                          (7)

One may verify (7) directly: A=q+r0 and G=q+qneg. The geometric content
behind (6)-(7) is Theorem1's physical injective map. The ledger algebra
alone would not supply it. In particular a bad nontrivial path must start
with a P edge, since S/R would activate its initial vertex. Bad isolated
vertices are retained: they are unactivated marked sides with negative-U
consumers and are not eliminated by this reduction.

Every m8 occurrence from the protected-defect theorem is a distinct marked
sink: its consumer is negative U and its preceding P edge exists. Its
protected receipt lies in C, and can be spent at most once. Those paths
whose initial vertex was already activated do not need the receipt; their
receipt remains available for another bad path. We do NOT infer Bbad<=m8
or Bbad<=C+Sunmarked for every family. The latter is exactly the remaining
full allocation target. Checking it only on nontrivial paths would omit
the isolated negative-U endings.

Theorem1 also gives mu>=-floor(qneg/2), since
2mu>=2N-G-qneg>=-qneg. Thus qneg<=1 guarantees allocation, regardless
of how many rotor consumers occur. Any actual negative margin has at least
two negative-U marked sinks, and (6) forces Bbad>=C+Sunmarked+2. These are
necessary conditions for a counterexample, not a geometric exclusion of it.

## 5. Two-step descent and a gap restriction on consecutive channels

**Theorem 2.** For consecutive P edges A->B->D, if A has width w and D
has width d, then

    d<=h-4<=w-8,                                    (8)

where h is the forced transverse height of the first edge.

In A's frame, B is T(U(W,a,b)). Since the second edge uses B's same
incident side, D is T composed with T applied to U(d,g,e):

    D(r,c)=(r+4,c+4).

Its top bar occupies rows4,5 and columns5 through d+4. The first forced
transverse source C0 owns (4,h+1), since this is the image of its original
bar endpoint (1,3). If d+4>=h+1, this same point belongs to D's top bar;
h>=6 ensures it is beyond the start of that bar. The two owners have
opposite signs. Disjointness gives d+4<h+1, hence d<=h-4. Equation (1)
gives the second inequality. This is a general interval argument.

Thus consecutive P chains have no directed cycles. Every other source
width decreases by at least8. If the first two widths are w0,w1, a P run
has at most

    1+floor((w0-6)/8)+floor((w1-6)/8) edges.         (9)

The first channel alone needs w0>=10. A run of two edges needs w0>=14.
Independently, in the initial side's frame T preserves the diagonal
orientation and increases row+column of each successive canonical gate
by4. This also excludes a P-only cycle. The width statement is stronger
than a bare acyclicity argument, and does not bound S/P/R mixed paths.

If a P edge with recipient incident length a and transverse
height h is followed by an S edge with singleton incident length b, then

    a<=b<=h-6.                                      (10)

Use B's own frame. Its forced transverse source is (r,c)->(h-r,c-1),
and owns (h-1,2). The S consumer has frame (2); its column-two interval
is rows3 through b+3. Disjointness therefore gives b+3<h-1. Evenness
gives b<=h-6, and the producer-activation proof gives b>=a. In particular
P->S would require h-a>=6. There is in fact a stronger obstruction.

**Theorem 3.** No P edge can be followed by an S edge, for ANY allowed
dimensions, slack h-a or surrounding complete sources.

The forced transverse source in B's frame owns the ENTIRE column-zero
interval from row0 through h, including its bar corners. The hypothetical
S bar contains (b+2,0), the image of its endpoint (1,3). If b+2<=h, this
is already a transverse endpoint. If b+2>h, the S column-two interval
from3 through b+3 contains (h-1,2), already on the transverse bar. Thus
both alternatives contradict disjointness. The two owners have opposite
signs. No rounding, dimension bound or realizability search is needed.

An R exit requires the recipient incident length a=4 by the rotor theorem.
For a tight attachment this forces h=6, whose side is permanently unmarked
by the proved enclosure theorem. Hence a tight P attachment cannot be
followed by S or R. Its positive continuation, if any, is P and obeys (8).
At a=6,h=8 no P continuation fits either, recovering the protected negative
ending class. This does not yet pay larger tight attachments or arbitrary
slack attachments. In particular a negative-U full-bar exit is not made
harmless just by the absence of a transfer cycle.

**Theorem 4.** If P is followed by R, that R companion must have incident
length g>=6. In particular the intermediate positive producer has width
at least14, by g<=hR-4<=width-8 from the rotor theorem.

Suppose instead that g=4. In the intermediate producer B's frame its
rotor is B0 and its companion D has frame V4(r,c)=(c+2,7-r). D's own
canonical gate is V4(3,2)=(4,4), an endpoint of the SAME rotor. Applying
the rotor theorem again, to that marked side of D, forces another positive
companion E with incident length k>=4 and frame

    V4 composed with Vk: (r,c)->(k+5-r,5-c).        (11)

The earlier P transverse source, in B's frame, owns column0 from0 through
h, and row h-1 from column0 through V-1, with V>=6. The E bar contains
(k+4,0). If k+4<=h, that point is already on the occupied column. If
k+4>h, E's column-four stem from row5 through k+5 contains (h-1,4),
already on the occupied row. Since h>=6 and E has width at least6,
both witness memberships hold at the minimum dimensions. The owners are
opposite in sign. Both cases contradict endpoint disjointness, proving
the claim. A run P->R->R using a length-four first R companion is therefore
excluded; this does not exclude R->R paths with no preceding P.

## 6. Verification and provenance

The rotor and flow proposal was present in completed Oracle task1adc9732;
it was explicitly unadopted in the earlier protected-defect milestone.
Sections1-4 reconstruct it with the actual owner-collision cases. The
two-step width descent, P->S gap/exclusion and small-companion P->R
obstruction in Section5 are derived here
from the normalized source intervals. No priority or literature novelty
claim is inferred from either derivation or external review.

[Physical/path controls](../output/rotor-transfer-path-controls.json) PASS:
800 phase/isometry images,31904 complete legal restrictions,792 actual P
transfers,3504 negative-U sinks and1376 bad paths. Every tested margin obeys
the exact identity (6). Abstract controls enumerate3166 labelled partial
injection graphs through four vertices, including cycles and isolated bad
paths. The local checks cover all16 rotor footprints,1904 PP width controls,
182 P->S collisions,182 second-companion wall collisions and91 rotor
companion activation patterns. Partial coordinate patterns are not asserted
to have complete feasible extensions. Complete physical S,R,PP,PS,PR and
cycle counts are ZERO in this existing fixture library; no unobserved
physical rotor-consumer example is claimed.

[Sixteen scoped Lean declarations](../formal/SubQuorum/RotorTransferPathEndings.lean)
compile locally and pass ordinary-axiom audit, without sorryAx or native
decision axioms. They verify the actual coordinate collisions, P iteration
for arbitrary length and conditional count arithmetic. The original rotor
catalogue, global physical injection and graph/count adapters remain written.
The [execution receipt](../output/rotor-transfer-path-formal-check.json)
records the initial missing width hypothesis and simp-name correction.

Independent written review3f49db6b, original7745, remains LIVE. Its submitted
snapshot includes the initial rotor/injection/path proof, PP descent and
weaker P->S gap. The stronger universal P->S exclusion and small-companion
P->R obstruction above were derived later and require addendum review after
the current answer. See the [review status](../output/rotor-transfer-path-review.json).
Original full-target taskb90c01ca/original91743 is also live and preserved.
No review verdict, full allocation or universal grid result is inferred.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
