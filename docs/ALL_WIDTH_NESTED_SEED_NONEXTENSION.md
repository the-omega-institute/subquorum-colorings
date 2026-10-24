# An all-width three-original nonextension theorem

22 October 2026. Authors: Haobo Ma and Wenlin Zhang.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.

## Theorem and its consequence for the compensation programme

Use the same original-source model as `WIDE_GATE_ESCAPE_PAIR_COMPENSATION.md`:
every original is a full U with even breadth>=6 and even depths>=4, or a
standard eight-endpoint rotor; arbitrary lattice orientations are allowed.
Endpoint sets of distinct originals are disjoint. Original supports and
matchings remain immutable. An original support that is not consumed as an
endpoint must have exactly one occupied neighbour in a complete extension.
In particular, two retained endpoint neighbours force consumption. This
source decomposition is a hypothesis, not a theorem about arbitrary grids.

Let W>=6 and a>=2 be even. Retain just the three originals

    A=U(W+2,D,F), chart(r,c-1), D,F even >=a+12;
    B=U(W,4,4), chart(a+r,c);
    C=U(W,4,4), chart(a+8+r,c).                              (1)

There is no complete extension containing (1) by any collection of
endpoint-disjoint originals in this model. Additional retained originals
cannot repair the obstruction.

Consequently, for every even W>=6 and n>=2, the entire nested family
A=U(W+2,D,F) with n copies U(W,4,4) at even rowsa+8i and even
D,F>=a+8(n-1)+4 has no complete extension: use A,B_0,B_1.

The earlier contact-ledger identities and selected-inventory compensation
formulas remain exact. However, the preceding claims about actual owners
in a complete extension of THIS seed now have empty hypotheses. They do
not yield an improved bound for any realizable complete grid family. The
new result is the exclusion of this whole candidate obstruction family,
not a global compensation theorem or an exhaustive multicycle exclusion.

## Reduction to one far axial support

At W=6 the three-original two-gate collision theorem in
`EVEN_BAR_CONTACT_LEDGER_AND_TWO_GATES.md` applies. For W>=8 use the
all-parameter owner arguments in the two wide-gate notes. Both gates
(a+5,1),(a+5,W) are forced; all U owners are excluded; lower rotor
owners cannot completely extend. The upper rotors force two rotated
U(6,k,f) escape owners. Their near stems must be disjoint, and their
short far offsets are excluded. Thus an alleged complete extension has
W>=20 and a left escape with

    k,f even, 8<=k, 4<=f<=k-4, k<=W-10.                    (2)

Subtract a from rows for the rest of the proof. The left escape has
chart(r,c)=(1+c,2+k-r). Put s=k+1-f; then

    s odd, 5<=s<=k-3.

Its far axial support z=(7,s) is absent from the retained-plus-rotor-plus-
escape endpoint set. Its east neighbour (7,s+1) belongs to the escape,
and its south neighbour (8,s) belongs to C. Therefore z must belong to
an additional original, whose internal endpoint directions can only be
north or west. We classify every such owner and then exclude all of them.

## Complete classification of U owners at z

The endpoint graph of a full U has degree-three branch/bar points,
degree-two straight stem points, degree-two outer bar corners, and
degree-one terminals. With only north/west free, only a north/west
outer corner or a north or west terminal is possible.

A west terminal has a continuous west-going stem from (7,s) to a
perpendicular bar in an odd column q. If q<1, it passes through the
outer wall (7,0). If q>=1, the bar either goes down through C's row8,
or goes up through row2. The latter point is on B's stem when q=1,
and on the escape near stem when q>=3. Thus every west terminal is
excluded, for arbitrary depth and breadth.

A north terminal has even near depth d>=4. If d>=6, its continuous
stem crosses the escape near stem at (2,s). Hence d=4 and its outer
bar is in row3. If its bar goes right, it either crosses the escape
inner bar at (3,k+1), or ends before that bar. In the latter case its
other stem, of depth>=4, reaches the escape far stem in row7, strictly
right of column s. Thus the bar must go left. Write its even breadth
b>=6 and other endpoint column l=s+1-b. The other depth cannot exceed4,
as a depth>=6 would cross C's row8. Also l>=6: l<=0 crosses the wall,
l=2 hits the upper rotor at (3,2), and l=4 hits it at (4,4).

For a north/west corner, a north-going bar of breadth>=6 reaches the
escape near stem at (2,s). Its bar must therefore go west in row7,
with two north-going stems. The near depth is exactly4, since a larger
even depth crosses row2 at column s. The same wall and upper-rotor
contacts give l>=6, after which a larger far depth also crosses the
escape near stem in row2. Hence its far depth is exactly4 as well.

We have proved that every surviving U record is exactly one of

    U(b,4,4), chart(r,c)=(3+r,s+1-c),                       (3a)
    U(b,4,4), chart(r,c)=(7-r,s+1-c),                       (3b)

where b is even and6<=b<=s-5. If s<11 there are none. Both records
have the complete right stem {(r,s):3<=r<=7}. Supports and matchings
are the images of the canonical originals; they are not reassigned.

## Complete classification of rotor owners at z

Every endpoint of a standard rotor has degree one or three. Hence its
owner at z must be a north or west terminal. Both west-terminal forms
contain (8,s-2), on C. The two north-terminal endpoint sets are

    R_1={(4,s-1),(5,s-1),(5,s),(5,s+1),
         (6,s-2),(6,s-1),(6,s),(7,s)},
    R_2={(4,s+1),(5,s-1),(5,s),(5,s+1),
         (6,s),(6,s+1),(6,s+2),(7,s)}.                      (4)

R_1 is excluded at s=5 by the upper rotor's point (6,3); otherwise
both may be endpoint-disjoint from the retained inventory. We exclude
both as complete-extension owners, without presuming either exists.

## A sealed horizontal gate excludes both rotors

For R_1 put c=s-1; for R_2 put c=s+1. Directly transforming its canonical
support record shows that y=(3,c) is its original support and (4,c)
is its endpoint. Also (2,c) is on the escape near stem. The support y
is absent from all these endpoints and must be consumed. Its north and
south directions are occupied, so only east/west are available internally.
The bounds5<=s<=k-3 give4<=c<=k-2.

No full U can have this role. A degree-three point or an outer corner
cannot fit opposite directions. A horizontal terminal or straight stem
leads continuously to a perpendicular bar in some column q. If q<=1,
the stem crosses B at (3,1); if q>=k+1 it crosses the escape inner
bar at (3,k+1). Otherwise2<=q<=k. A bar pointing up intersects the
escape near stem at (2,q); a bar pointing down has breadth>=6 and
intersects C at (8,q). This exhausts all bar columns and directions,
with no bound on U dimensions.

A rotor must be an east or west terminal. In either direction its two
fixed forms contain a row2 endpoint at column c+1 or c+2 (east), or
c-1 or c-2 (west). Since4<=c<=k-2, all these columns lie in [2,k+2],
on the escape near stem. Thus no rotor fits either. The forced support
y has no owner, excluding both records (4) in a complete extension.

## A sealed corner gate excludes both U records

For either record (3a) or (3b), y=(3,s+1) is an immutable original
support. It is absent from the endpoints, has north neighbour (2,s+1)
on the escape near stem, and west neighbour (3,s) on the new U's right
stem. Only east and south can be internal directions of its owner.

For a full U, the possible roles are an east/south outer corner, an
east terminal, or a south terminal. A south-going continuous stem of
depth>=4 hits the escape far stem at (7,s+1), while a south-going bar
of breadth>=6 hits C at (8,s+1). These exclude both corner orientations
and the south terminal. For an east terminal, its stem either reaches
the escape inner bar at columnk+1 in row3, or its bar lies in a column
q between s+1 and k. An upward bar hits row2, and a downward bar of
breadth>=6 hits row8. Every case is blocked.

An east-terminal rotor has a row2 endpoint in column s+2 or s+3;
both are on the escape near stem since s<=k-3. A south-terminal rotor
has, in both of its fixed forms, endpoint (5,s). That point is on
the common right stem of (3a) and (3b). Thus no rotor can fit either.
Again y is forced but has no possible owner. This excludes every U
record in the exhaustive classification.

Every possible owner of z has now been excluded. This contradicts its
forced consumption, proving the theorem. Existing additional retained
originals do not help: any that already consumes one of these supports
is itself an owner in the exhaustive classification and must satisfy
the same endpoint-disjointness constraints.

## Validation and formalization scope

`develop/check_wide_gate_sealed_return_obstruction.py` reconstructs full
endpoint/support/matching records, compares all surviving far-owner
records to (3)/(4), and checks every next sealed gate against all sampled
U orientations/roles and all standard rotor roles. It includes every
admissible breadth of (3) in each concrete case, reflection/even-translation
controls, and large-parameter examples. The infinite parameter exhaustion
is the written proof above, not a bounded-source enumeration.

`formal/SubQuorum/WideGateSealedReturnObstruction.lean` formalizes the
normalized top/bottom/side barrier geometry, all-bar-column horizontal
U collision, both-direction rotor collision, far-rotor gate bounds,
east-terminal and south-stem/bar collisions at the corner gate, and
both south-rotor collisions. Complete original-to-role adapters, canonical
support identifications and the full assembly are written, not claimed
as a fully formal theorem about all source decompositions.

Local controls completed18 parameter cases,62 normalized U and33 rotor
survivor records,156 complete short-U shapes and189 sealed gates. They
excluded364800 U roles and3024 rotor roles; reflection/even-translation
controls also passed. Two further large cases at W=200,k=100,f=40 and
W=2000,k=1000,f=900 checked148 additional gates,140288 U roles and2368
rotor roles. Final Python process89822 exited0. Final Lean4.33.0 process
94747 exited0 with15 declarations/10 local theorems individually audited,
ordinary axioms only, no warnings/sorry/native. Preflight39% memory free
and comm-basename process inspection found no active Lean/lake invocation.

Independent continuation reviewda0dcf4e-7214-4c46-bd46-1749adde75db,
original stream89055, conversationconv_ed4025a182e9f9d9, completed ACCEPT.
Its18509-character answer exactly matches the terminal receipt and the
original stream, which exited0; observed modelgpt6/pro. The review covers
both the far-offset exclusion and this all-width closure, including the
immutable support adapters, every dimension/orientation and additional
retained originals. It is a written audit, without independent execution
of Python or Lean. The spacing corollary below was outside this review.
The predecessor's two-layer proof also remains independently ACCEPTED.

The broader research targets remain open: unequal/deeper inner sources,
other multicyclic contact components, mixed orientations, full-family
allocation, the global5/6 improvement and rectangular-grid triple equality.
The next research step should leave this now-excluded nested seed rather
than accumulate further conditional compensation layers for it.

## Post-submission corollary: minimum spacing ten

There is also a shorter obstruction at bar spacing6. Retain A as above,
B=U(W,4,4) at even rowa>=2, and C=U(W,4,4) at rowa+6, with even
D,F>=a+10. The original support p=(a+5,1) has retained north, west
and south neighbours, so its owner can only be an east terminal.
For a full U of near depth k, k>=W crosses A's opposite wall. Otherwise
its perpendicular bar is within columns1..W. An upward bar of breadth
at least6 hits B's rowa, and a downward bar hits C's rowa+6. The two
standard east-terminal rotors both contain (a+6,3), on C. No owner
can exist, so spacing6 cannot completely extend either.

Consequently, suppose a complete extension contains A and n coextensive
positive U(W,4,4) originals with even bar rows

    2<=a_0<a_1<...<a_(n-1), D,F>=a_(n-1)+4.

Endpoint disjointness requires each even gap to be at least6. The preceding
short argument excludes6, and the all-width theorem excludes8. Therefore

    a_(i+1)-a_i>=10, and a_(n-1)-a_0>=10(n-1).             (6)

This is a necessary spacing condition for complete extensions, not for
arbitrary endpoint-disjoint partial inventories. It does not exclude
spacing10 or prove a global budget bound. Spacing10, unequal legs and
different contact components are the appropriate next cases.

This corollary was added after taskda0dcf4e was submitted and is outside
its initial review scope. Four further source controls at W=6,8,20,100
exclude1024 U roles and32 rotor roles. They were run separately after the
previous complete verifier passed. The final Lean file adds the general
spacing-six U collision, the translated rotor collision and even-spacing
frontier; it has20 declarations/13 local theorems. The complete source
adapters and the finite-sequence summation in (6) remain written arguments.
