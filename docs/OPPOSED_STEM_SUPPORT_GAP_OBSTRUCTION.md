# Opposed stems at gaps two and three cannot be completed

21 October 2026. A general two-source obstruction removes the entire
first family of short-leg opening intruders, even before their proposed
shared consumer is added. Its proof uses original support occupancy,
including support-support conflicts. It also gives a necessary escape
form for any intrusion into the first lower pair and pays a further
small-incident-length class of actual Vcorner demands. The unrestricted
allocation and rectangular-grid triple equality remain OPEN.

## 1. Model and an arbitrary-dimension two-source theorem

Keep the finite complete original U/rotor model: pairwise disjoint original
endpoints, unchanged matching, and every unconsumed original support retained
with its original endpoint anchor as its sole occupied neighbor. Optional
selected vertices have no endpoint neighbor. Source endpoint graphs are
connected by unit lattice edges. All U widths are even and at least six,
all independent legs even and at least four. A retained original support
is always OCCUPIED, whether finally selected or consumed as an endpoint.

Suppose two original sources have frames

    D=U(d,n,t), D(r,c)=(c-d,r),
    Q=U(s,g,t), Q(r,c)=(s-delta-c,t+2-r),
    delta in {2,3}, d,s>=6, n,g,t>=4,

with all source dimensions even. Their endpoints are disjoint for every
such choice. There is NO complete extension by any finite number of
original U/rotor sources, with arbitrary permitted dimensions and phases.
For this obstruction arbitrary lattice translations are allowed; no
tile-alignment-dependent receipt is claimed.

**Proof.** D has bars in columns0,1, from row1-d through0, a near stem
on row1-d and a far stem on row0 extending through column t. Q has bars
in columns t+1,t+2, from row-delta through s-delta-1, a far stem on
row-delta covering columns2 through t+2, and a near stem below row0.
These descriptions establish endpoint disjointness, including the corners.

The entire boundary of [-delta,0] x [1,t+1] consists of D/Q endpoints:
D supplies the left and bottom except the bottom-right corner; Q supplies
the top except the top-left corner and the right. Neither source has an
endpoint strictly inside. There are only delta-1, hence at most TWO,
strict-interior rows. Any foreign original endpoint graph entering the
interior is confined by the occupied boundary. No U or rotor fits in two
rows: their minimum row extents are respectively five and four.

D's original support p=(-1,3), with its anchor (0,3), lies strictly inside.
Its intrinsic coordinates are (3,d-1), valid since t>=4. If delta=2,
Q owns the additional endpoint (-2,3), so p must become an endpoint.
If delta=3, Q produces the original support q=(-2,3), whose intrinsic
coordinates are (t-1,s-1). Even t makes t-1 odd, so it is an inner far-leg
support. q remains occupied whether selected or consumed. It is a second
occupied neighbor of p, distinct from D's anchor. Therefore p must again
become an endpoint. D and Q do not own p, and the thin enclosure excludes
every foreign consumer. Contradiction in either case.

For delta=2, p is also Q's original inner support, with a different anchor;
the proof needs only its adjacent Q endpoint. For delta=3, counting only
support-endpoint conflicts would MISS this obstruction: p and q initially
each have only their own endpoint anchor, but are adjacent mandatory
supports. Consuming q alone would leave p beside both q and its anchor,
so the full retention obligation forces p too. This is the existing Horn
occupancy principle, not an assumption that the two consumers differ.

## 2. Application to the previous opening intruder

The earlier partial stencil has

    Q=U(6,8,4), Q(r,c)=(b+2-c,11-r),
    D=U(6,4,4), D(r,c)=(b-7+c,r+5).

Translate the delta=3 theorem by (b-1,5). These are exactly its d=s=6,
n=t=4,g=8 case. Thus the TWO prescribed sources alone have no arbitrary
complete extension, for any b. The earlier endpoint-disjoint construction
and the single P consumer of three forced supports remain correct as
partial stencils, but neither can be completed. P never repairs the
adjacent inner supports at (b-3,8),(b-2,8).

More generally, for every d>=6 and n>=4,

    D=U(d,n,4), D(r,c)=(b-1-d+c,r+5)

is excluded with that Q by the same delta=3 theorem. If its bottom stem
is instead on row b-2, the delta=2 theorem excludes it. Both statements
permit arbitrary other legs and widths. Exchanging a U's leg names does
not produce a new exception.

These are noncompletion results. They do not contribute a reserve unit,
activation, or unmarked-positive bonus. They remove impossible claims.

## 3. Any lower-corner intrusion has a specific north-terminal escape

Use an actual normalized marked-side chain

    A=U(w,L,K), A(r,c)=(r,c),
    B=U(W,b,e), B(r,c)=(b+3-r,c+1),
    C=U(V,h,f), C(r,c)=(c+1,h+2-r),
    X=U(b-2,a,k), X(r,c)=(c+2,r+3),
    Q=U(6,8,4), Q(r,c)=(b+2-c,11-r),
    b>=8, W>=12, h>=8, 4<=a<=h-4, h<=w-4,
    k in {4,6}.

All source dimensions are legal even integers and endpoint disjointness is
required. X is the actual Vcorner at y=(3,3), and Q is the actual consumer
of X's support (b+1,3). Additional sources are unrestricted. Put

    v=(b-1,5), u=(b-2,5).

**Escape theorem.** If v becomes an endpoint, its original owner is

    H=U(d,j,z), H(r,c)=(b-1-j+r,c+4),
    6<=j<=b-6,

with legal even d,j,z. Thus b>=12 is necessary. H is a north-pointing
terminal at v with its horizontal bar to the right. This is a necessary
form, not an assertion that every such H is completable or supplies a
new positive activation.

First check existing owners. Neither A,B,X,Q owns v. C could own it
only on its far stem when V=b-2. That stem's interval
[h+2-f,h+2] has an even lower endpoint; inclusion of column5 implies
inclusion of4, which would collide with X at (b-1,4). Hence its consumer
differs from all five named owners before any blocking endpoint is used.

At v, west is X's bar and south X's far stem, so own endpoint neighbors
can only be north/east. The U catalogue leaves north/east terminals and
two outer-corner orientations. A rotor must be a tip, since all its
nontip endpoints have three own neighbors. Its two north-tip forms hit
X at (b-2,4) or (b-3,4); its two east-tip forms hit X at (b,7) or (b,6).

An east U terminal has incident length4: any length>=6 reaches Q's
column10 on row b-1. With length4 its bar has columns8,9. An upward
bar crosses Q's far stem on row b-4; a downward bar crosses Q's near
stem on row b+1. Both are impossible at every bar width>=6.

A horizontal outer bar to the east includes Q's (b-1,10). A vertical
outer bar to the north has columns5,6 and its incident east leg must
have length4, since length>=6 again hits Q on column10. After exchanging
leg names it is precisely the delta=3 source in Section2, with arbitrary
bar width and other leg. The two-source theorem excludes it.

Only a north terminal remains. If its bar points left, its rightmost
stem is column5 and its upper bar row is R=b-1-j. For R>=2 one of its
two bar rows hits X in column4 (R=2 uses row3); for R<=1 its stem meets
C at (2,5). Thus the bar must point right, giving the displayed H frame.
Incident j=4 makes the lower bar meet Q at (b-4,10), so j>=6. If R<=2
the column5 stem meets C at (2,5). R=3 meets X's near stem at (3,5).
Parity makes R odd, hence R>=5, equivalently j<=b-6. This proves the
escape theorem with no enumeration cutoff.

## 4. An endpoint at the upper missing corner forces the lower one

In the same complete actual-chain model,

    u is an endpoint ==> v is an endpoint.

Suppose instead that u is an endpoint and v is not. Existing owners do
not own u: C's far stem has odd physical row, whereas u.row=b-2 is even;
the other exclusions follow immediately from their frames. West at u
is X-owned and south v is not an endpoint, so own neighbors again can
only be north/east, with the same U terminal/corner catalogue.

Both east U bar directions hit Q: incident length is4 by column10,
then the upward bar crosses row b-4, the downward bar row b+1. A horizontal
outer bar to the east also hits Q in column10. A vertical outer bar up
columns5,6 has its bottom stem on row b-2 and incident length4, and is
excluded by the delta=2 theorem. A north terminal has v as its original
beyond-tip support; v also has the west X endpoint as a neighbor. Hence
retention forces v to be an endpoint, contradiction.

The two north rotor tips hit X's column4. One east rotor tip hits X
at (b,6). The other is the R- footprint at u from the four-row note;
it has the original support u+(1,0)=v, whose X west neighbor again forces
consumption. Thus every rotor is excluded as well. This proves the
implication without presuming distinct consumers or treating absence
of an endpoint as absence of an original support.

## 5. New permanent pairs and joint single-use compensation

For b in {8,10}, the escape theorem's 6<=j<=b-6 is impossible. Consequently
neither v nor u is an endpoint. Neither can be selected: each has a west
X endpoint but is not an original X support, at intrinsic coordinates
(2,b-3),(2,b-4). Optional selected vertices cannot have endpoint neighbors.
Thus J={b-2,b-1} x {4,5} is permanently X's irregular 2P0T pair in this
entire actual-chain class. If either were a retained original support, its
west X endpoint would have to be its sole occupied anchor; unique endpoint
ownership then identifies the support owner as X, contrary to the stated
intrinsic coordinates. Its Q has the shorter far leg4, so it is not
covered by the prior short saturated Q=U(6,8,6) theorem.

The demand reconstruction and old-H nonreuse in the previous notes depend
only on X's first lower pair and the actual B gate: they apply unchanged.
Take the UNION of these new residual Vcorner demands, previous W10 and
short-saturated Vcorner demands, and all certified H demands. They inject
jointly into ONE physical lower-pair union P, so s<=p=|P|. A demand or
pair carrying multiple certificates is counted once. The exact existing
ledger remains

    mu>=n0+u_upper+p+ceil((m8-s-t_residual+rho)/2).

If t_residual=0, it yields

    mu>=n0+u_upper+(p-s)+ceil((m8+s+rho)/2)>=0.

Thus automatic coefficient-one coverage extends to this additional class;
the full allocation and grid decomposition are not proved. Holding other
certificate quantities fixed, the floor gain is exactly the number of
new physical pair tiles absent from Pold. The cross-component loss floor
still applies once in the intermediate family containing all losing
components, using certificates whose supporting owners are retained. For
this new class that includes the actual A/B/C/X/Q premises, particularly
C's blocking endpoint (2,5); retaining X/Q alone does not suffice. Impossible
two-source intruders do not create a second resource.

The subsequent [short-return rotor-cavity theorem](SHORT_RETURN_ROTOR_CAVITY_OBSTRUCTION.md)
excludes this entire actual k=4 return class at every b: Q's forced
near-leg support has one rotor consumer, whose single-row cavity with Q
prevents completion. The conditional k4 pair corollary above therefore has
no complete instances; it creates no extra resource. The subsequent
[six-step escape obstruction](INCIDENT_SIX_NORTH_ESCAPE_OBSTRUCTION.md)
excludes j=6 for k=6 as well, strengthens the necessary conditions to
8<=j<=b-6 and b>=14, and certifies the actual b12 lower pair using the
same joint physical-pair union. Longer north escapes remain OPEN. No claim that the
entire short-leg class is impossible or permanently protected is made.
Other return widths, nonmaximal corners and saturated adjacent bands
also remain unresolved. There is still no complete Vcorner realization.

## 6. Validation status

The independent [controls](../develop/check_opposed_stem_support_gap.py)
PASS ([receipt](../output/opposed-stem-gap-controls.json), session74804
exit0):576 parameter patterns at each gap,54 translated intruder identities,
and anchored U/rotor roles at b=8,10,12,18 for both k=4,6. Another1716
lower-corner same-owner and2808 upper-corner parity exclusions pass. All576
gap-three patterns have only one endpoint neighbor at each conflicting
support, confirming that endpoint-only diagnostics miss the contradiction.
The role library bounds widths and legs at18; it is not an unbounded
enumeration or a complete-family realization.

All19 scoped Lean4.33.0 theorems PASS, finalsession25297 exit0, with
individual axioms only propext, Classical.choice and Quot.sound, no
sorry/native axiom. The authorized local Mac had49% free memory and no
actual lean/lake executable by comm basename before starting. An earlier
standalone-core tactic failure in the new composition theorem was repaired;
that failed run is not validation. The formal source proves the two-source
contradiction over an arbitrary owner family under explicit connectivity,
row-extent, unique ownership and support-retention hypotheses. Catalogue
adaptation for every U/rotor and the complete corner-role/global joint
injection arguments remain written. See the [direct Lean source](../formal/SubQuorum/OpposedStemSupportGap.lean)
and [formal receipt](../output/opposed-stem-gap-formal-check.json).

Independent written review c65b8358 ACCEPTS the full conditional obstruction,
corner-role classification, escape form, small-b pair corollary and inherited
joint accounting. Its15675-character response exactly matches original
stream62943 exit0 and the completed task API, with [DONE], no stream errors
and observed gpt_6/pro. The review's original-support ownership explanation
and retained C blocking premise are explicit above. It does not certify
execution, complete realizability or the unrestricted target. See the
[full review](../output/opposed-stem-gap-review-response.md) and
[receipt](../output/opposed-stem-gap-review.json). General proofs are given
above; bounded controls do not replace them. The first intruder and
shared-consumer stencils retain their previous endpoint-only validity and
now have a general noncompletion proof.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
