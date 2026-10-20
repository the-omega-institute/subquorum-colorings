# All-length negative-singleton companions and a joint activation injection

21 October 2026. This extends the positive-companion part of
[short negative-singleton endings](SHORT_NEGATIVE_SINGLETON_ENDINGS.md)
to EVERY permitted incident length. It does not extend the short negative
corner's permanent-pair conclusion to arbitrary lengths. The unrestricted
allocation mu=N+R-G>=0 and rectangular-grid triple equality remain OPEN.

## 1. Complete-source assumptions and four general roles

Work with finite complete original U/rotor families under
[source retention](SOURCE_RETENTION_HORN_CLOSURE.md). Original endpoint sets
are disjoint; matchings and every unconsumed original support are retained.
Every retained support has occupied degree one. Source endpoint graphs are
connected. Widths are even>=6 and independent leg lengths even>=4. Use fixed
aligned physical tiles and normalize the producer by an isometry preserving
that partition. N counts positive owners and Aactivation counts original
activated positive terminal occurrences, once per occurrence.

Normalize the positive producer A=U(w,L,K), canonical gate t=(3,2),
other tile positions p=(2,2), y=(3,3). Suppose t's actual consumer is an
original negative-U singleton. The established terminal and transverse-tip
arguments give distinct original owners

    B=U(W,b,e), B(r,c)=(b+3-r,c+1),
    C=U(V,h,f), C(r,c)=(c+1,h+2-r),
    4<=h<=w-4.

B consumes t; C consumes B's mandatory support p. C's mandatory support y
has C's anchor (2,3) and B's terminal (3,2) as occupied neighbors, so it
must be consumed by an original owner D distinct from A,B,C. The earlier
three-row enclosure excludes b=4; hence b>=6. There is NO upper bound on b.

At y, D can have own endpoint neighbors only east and/or south. A U
endpoint is therefore a terminal in one of those directions, or an upper
outer bar corner with both neighbors. There are TWO orientations of that
corner. Every bar/stem junction and internal bar point has three own
neighbors and is excluded. Nonterminal straight leg points require
opposite neighbors and are excluded. Rotor central points have three own
neighbors. The four possible rotor-tip footprints meet one of C(2,4),
C(2,5), B(5,2), B(4,2), exactly as in the short proof. These blockers
exist at every allowed b>=6, so no rotor case remains.

After naming the incident leg g, the exhaustive necessary forms are:

| Case | Original owner and frame | Necessary conditions |
|---|---|---|
| E | U(d,g,k), (r,c)->(c+2,g+3-r) | g<=h-4; d<=b-2 OR g>=W |
| S | U(d,g,k), (r,c)->(g+3-r,c+2) | g<=b-2; d<=h-2 OR g>=V |
| H | U(d,a,k), (r,c)->(r+3,c+2) | a<=b-2; d<=h-2 |
| Vcorner | U(d,a,k), (r,c)->(c+2,r+3) | d<=b-2; a<=h-4 |

E and S are positive sources; H and Vcorner are negative. These are
necessary forms, not sufficient conditions for complete realizability.
The symbol Vcorner is a role label; V in the inequalities is C's width.

For an east terminal, the upward bar would meet C's row-two stem, so its
bar points south. The row-three stem reaches column g+3 and must stop
before C's bar at h+1, giving g<=h-4. If d>=b and g<W, the endpoint
(b+2,g+2) is on BOTH E's bar and B's bar, a contradiction. Evenness gives
the stated disjunction. In particular g>=W is forced when b=6; it is NOT
a uniform bound at larger b.

For a south terminal, its stem would hit B's bar at (b+2,3) if g>=b,
so g<=b-2. A leftward bar would meet B's incident leg, hence it points
right. If d>=h and g<V, point (g+2,h+1) belongs to both bars; parity
gives the second disjunction. When d<=h-2, the far leg additionally obeys
k<=g: otherwise it includes (2,d+2), on C's row-two stem. One must not
silently use d<=h-2 or k<=g in the alternative g>=V branch.

For H the incident leg hits B at (b+2,3) if a>=b; its row-three bar hits
C at (3,h+1) if d>=h. For Vcorner its vertical bar hits B at (b+2,3)
if d>=b, and its row-three leg hits C at (3,h+1) if a>=h-2.
Parity yields all four stated bounds. In particular Vcorner is impossible
at b=6 because d>=6; its omission from a short classification must not
be propagated to longer b.

## 2. Every terminal companion transfers to an activation

If D is E or S, y is a positive original terminal singleton. Its two
original intratile supports are exactly t=(3,2) and (2,3), consumed by
B and C. Thus y is ONE actual activated terminal occurrence, even though
both supports have vanished. Assign the original marked side to y.

This assignment is injective over all such marked sides, allowing arbitrary
b,g,d,k. From y and its physical tile, the original support roles distinguish
B's terminal from C's internal straight-leg point. They identify t and its
actual owner B. At t, the two potential external producer anchors are
(3,1) and (4,2); the latter is an endpoint of negative B. The positive
producer therefore owns (3,1). Unique endpoint ownership and the established
canonical-gate uniqueness determine the original marked side. The proof
does not use b=6 or g=4.

The transfer must also be disjoint from the established S/P/R activation
targets of positive or rotor gate consumers. Here S in the next table
denotes the old singleton channel, not the south-companion role.

| New companion | Old channel | Forced old producer frame | Colliding original endpoint |
|---|---|---|---|
| E | S | (r,c)->(5-c,r) | (1,5) maps to A(0,1) |
| S | S | (r,c)->(r,5-c) | (0,4) maps to A(0,1) |
| E | P | (r,c)->(r,g+5-c) | (0,1) maps to A(0,g+4) |
| S | P | (r,c)->(g+5-c,r) | (1,g+2) maps to A(3,1) |

These frames follow by composing the actual companion frame with the
inverse of the established old recipient frame, permitting either incident
leg to be named first. For the third row, g+4<=h<=w-4 puts the collision
on A's original top bar. In the fourth row, the old P-channel bound says
g<=w_old-4, so the old endpoint (1,g+2) exists even for large g.
This is the extra dimension check needed to extend the earlier g=4 proof.

The hypothetical old producer cannot equal A. The first, second and fourth
frames have bar endpoints in column zero, whereas A has no endpoint there.
For the third, every old endpoint has column<=g+4<w, whereas A owns (0,w).
Thus all displayed overlaps are genuine different-owner contradictions,
including the potential self-producer cases.

Every old R target has an intratile support owned by the preceding rotor.
Both support owners B,C at a new target are U owners; unique original
endpoint ownership therefore excludes any collision with R. This argument
does not depend on the terminal's direction or dimensions.

Let q0 count all established positive/rotor-consumer marked sides, and qT
all negative-singleton sides whose next owner at y is E or S, at ANY b.
Then the combined physical injection proves

    q=q0+qT <= Aactivation.                         (1)

There is no second activation pool and no per-component copying. The two
positive-companion roles are now resolved at arbitrary incident length.
An unresolved negative-singleton gate must have a negative H or Vcorner
companion, not a positive terminal or rotor companion.

## 3. A stronger obstruction: south incident length four is impossible

If the south companion has g=4, the alternative g>=V is impossible because
V>=6. Hence d<=h-2 and 4<=k<=g=4, so D=U(d,4,4) with frame(7-r,c+2).

The entire boundary of [2,6]x[3,d+2] is C's row-two stem or D's endpoints,
with neither owner having an interior endpoint. The strict interior has
three rows and contains BOTH canonical gates of D, (4,4) and (4,d+1).
Any foreign connected endpoint graph reaching the interior would be trapped;
no allowed U or rotor fits in three rows. This recovers the earlier necessary
unmarked-owner conclusion, independently of B's incident length b.

There is, however, also a mandatory point INSIDE that enclosure. Put

    x=(3,d+1).

It is an ORIGINAL inner support of C: its original coordinates are
(h-d+1,2), where h-d+1 is odd, at least3 and at most h-5. The inequalities
use d<=h-2, d>=6 and evenness. Its original anchor is (2,d+1), an endpoint
of C. The south companion's far terminal (3,d+2) is a second occupied
neighbor. Therefore x cannot remain selected and must be consumed by an
endpoint. But x lies strictly inside the three-row enclosure; neither
boundary owner has an interior endpoint and no foreign source can fit.
This is a contradiction.

Thus the TWO prescribed owners C and U(d,4,4) in the south frame have NO
complete U/rotor extension whenever d<=h-2. B and A are not needed for this
last obstruction. In particular an actual south companion must have g>=6,
and then b>=g+2>=8. At b=6 the old three necessary roles sharpen to E or H.

This proof explains why the earlier partial S patterns did not produce a
complete witness. The older implication that an S4 owner would be unmarked
remains valid but is vacuous on complete families. It cannot be advertised
as an extra realized source of unmarked-owner compensation. Nor does this
exclude every south companion of larger g.

### A further obstruction in the long-south alternative

There is a second two-source exclusion. Suppose C=U(V,6,4) with frame
(c+1,8-r), and S=U(d,g,k) with frame(g+3-r,c+2), where g>=V.
This is in the alternative where S may pass below C's bar. Regardless of
d,k and the number or dimensions of added sources, these two owners have
NO complete U/rotor extension.

The whole boundary of [2,V+1]x[3,7] consists of their original endpoints:
C supplies the top and right boundaries, C's far leg supplies the bottom
from column4 onward, and S's incident leg supplies the left including the
bottom-left corner. Neither owner has an interior endpoint. Its strict
interior has exactly three columns, so no allowed connected U/rotor endpoint
graph can meet it. But x=(V,4) is S's mandatory original inner support:
its original near-leg position g+3-V is odd, at least3 and at most g-3.
Its neighbors (V,3) in S and (V+1,4) in C are fixed endpoints. It must be
consumed inside that forbidden interior, a contradiction.

This proof explains the larger-leg S6 discovery failure below. It excludes
this transverse-height-six/far-length-four subclass, not all longer south
companions. This subsection was added AFTER the c1605aa3 review packet;
that review must not be credited as checking it without a later addendum.

## 4. Effect on the conditional allocation and remaining obstruction

Use the existing disjoint cap/strip/lower-pair/m8 ledger. Let n0 count any
independently certified distinct positive owners with both sides unmarked;
one may always take n0=0. The impossible S4 role contributes NO such owner.
Let c count
certified full-bar cap claims; s the earlier b=6 negative H claims assigned
injectively to existing protected lower pairs, so s<=p; and t all remaining
negative-U marked sides after removing the all-length terminal-companion
claims now included in q. These classes partition actual marked sides.
The previous nonreuse theorem and (1) give

    G=q+c+s+t <= 2(N-n0),
    q<=Aactivation, s<=p,
    2R>=Aactivation+m8+c+2p+2u.

R=S+C-K and mu=N+R-G are integral. Applying the inequalities in the SAME
complete family yields

    2mu >= (2N-G)+(Aactivation-q)+m8+2p+2u-s-t
         >= 2n0+2u+2p+m8-s-t,
    mu >= n0+u+p+ceil((m8-s-t)/2).                  (2)

Thus s+t<=2n0+2u+2p+m8+1 is sufficient for mu>=0. This retains every
certified lower pair at full weight, while charging the actual s assigned
claims once. Eliminating s using s<=p recovers the convenient weaker bound
mu>=n0+u+ceil((p+m8-t)/2) and its threshold
t<=2n0+2u+p+m8+1. Unlike immediately substituting s<=p, (2) retains the
extra lower capacity whenever p>s. Neither bound allocates p a second time.

Here t now excludes E/S companions of EVERY length. Every old certificate
is retained; no short negative-corner pair is extrapolated to a taller
enclosure. No additional contribution s is added to the p pool.

For complete-source configurations satisfying this condition, the established
sigma>=mu implication gives coefficient one instead of 5/6, a gain |M|/6.
Universal coverage and the arbitrary-grid source decomposition are unproved.
Long H, Vcorner, filled-corridor and vertical regular exits remain the
substantive global obligations. A dimensional decrease in the table alone
does not pay those endings or prove termination of a new global allocation.

## 5. Validation scope

The independent role checker reconstructs original matching and supports.
It checks all four roles over independent parameter controls, including
Vcorner and east companions with g<W at b>6. These are endpoint-disjoint
PARTIAL patterns. No complete E/S realization is claimed from them.
Two initial bounded U-only completion searches for b=8 E/S seeds are UNSAT;
this excludes their specified finite libraries only. A larger S library is
also UNSAT. The separate all-dimension support/enclosure argument in Section3
now proves that S seed has NO arbitrary U/rotor completion, while the E seed's
finite search alone makes no such claim. A longer S6 seed was also UNSAT
in a41713candidate library; the separate three-column enclosure proves its
subclass impossible for arbitrary sources. Finite search is discovery and
validation, not a proof substitute.

formal/SubQuorum/AllLengthSingletonCompanions.lean contains twenty-three scoped
unbounded coordinate/dimension, predecessor-collision, both enclosure
obstructions and retained-count integer lemmas, checked locally
with ordinary propext/Classical.choice/Quot.sound, NO sorry or native_decide.
The all-source role catalogue, reconstruction, joint physical injection and
unmarked-owner/count adapters are written proofs, not end-to-end Lean claims.
The earlier residual integer lemmas apply unchanged with the new q,t,n0.
Independent review of this later all-length extension must be separate from
cc4dd625, whose supplied packet predates it.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
