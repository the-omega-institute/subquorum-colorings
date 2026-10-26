# Complete matching classification on the occupied two-port band

27 October 2026. Wenlin Zhang and Haobo Ma.

For a subsequent change of the selected/endpoint footprint, see
[neutral occupied envelopes](NEUTRAL_OCCUPIED_ENVELOPE_EXPANSION.md).
That construction supplies at least 2^m completely frozen half-area footprints
without exterior input. It does not alter this fixed-footprint classification.

Fix the selected set T* and endpoint set P* of the frozen half-area band.
The actual matching is allowed to be ANY perfect matching of the induced grid
on P*. With both right ports kept, exactly **5m+4** actual matchings completely
freeze. If either port is absent, the only completely frozen matching is M*.
The proof uses two geometric white traps, a path matching argument and explicit
freezing sequences. Finite enumeration is a check, not a proof premise.

The result classifies this fixed footprint. It does not classify arbitrary
mixed-direction configurations or improve the universal 5/6 bound. It upgrades
the preceding existence example to a complete local interface classification.

## 1. Geometry and exact theorem

Use all coordinates and the exact T* from
[FROZEN_HALF_AREA_ATTAINERS.md](FROZEN_HALF_AREA_ATTAINERS.md). Write

    m>=2, c=6m+9, n=3m+2, R={0,...,5} x {0,...,c}.

In core j, s=6j, the endpoints are

    A=(1,5+s), B=(1,6+s), C=(1,7+s), D=(2,7+s),
    E=(2,6+s), F=(3,6+s), G=(3,7+s), H=(3,8+s),
    U=(2,5+s), V=(3,5+s).

Also g_j=(3,9+6j), b_j=(3,10+6j) for j<m,
Z_l=(4,5+2l), K_l=(4,6+2l) for l<n, and Q=(4,c).
For completeness, the selected columns in each row are exactly:

    rows 0 and 5: all odd columns 1,3,...,c;
    row 1: {2} union {4+6j,8+6j:0<=j<=m};
    row 2: {0,3} union {9+6j:0<=j<=m};
    row 3: {1,3}; row 4: {0,2,4}.

The isolated edge is (1,1)--(2,1). Every row-3 and row-4 cell in columns
5 through c is an endpoint. The other endpoints are the three columns
5+6j,6+6j,7+6j in rows 1 and 2, and the isolated edge.

Even coordinate sum means black; odd means white. The canonical matching M*
uses AB,CD,EF,GH,UV in every core, g_j b_j for j<m, g_m Q,
and Z_l K_l. There are 9m+9 endpoints of each colour.

Only outside sites p=(3,c+1) and q=(4,c+1) can be granted kept; every other
outside site is unavailable. No actual matching edge crosses the boundary.
Starting with no frozen endpoints, an endpoint freezes once at least two
DISTINCT nearest-neighbour sites are kept. More precisely, with granted set I,

    F_0=empty,
    F_(t+1)=F_t union {v in P*: |N(v) intersect (T* union I union mate(F_t))|>=2}.

A site is kept when selected or its ACTUAL mate has frozen. Thus freezing
of a white endpoint depends only on white endpoints, and likewise for black.
The two kept grants influence black and white respectively.

**Theorem.** Let M be any perfect matching on P*. With p and q kept, M
completely freezes if and only if it belongs to the list in Section 4.
The list has 5m+4 distinct members. M* completely freezes with no grants.
Every other listed member needs BOTH grants. For every listed noncanonical
member the exact unfrozen sets are

    no grants: B union W; p only: W; q only: B; both: empty,
    B={g_m,K_(n-1)}.

The white set W and its size are given in Section 6. In particular, for ANY
matching on P*, complete freezing with either port absent forces M=M*.

## 2. Forced cores and odd vertical edges

The isolated edge is forced by its component. Every EF is also forced in
any completely frozen matching, even with both grants. If EF is absent,
A,C,E must all match into S={B,U,D}; disjointness exhausts S. At B all three
endpoint neighbours A,C,E have mates in S; at U only V can have its mate
outside S; at D only G can. No grant is adjacent to S, and none of its
members has a selected neighbour. Thus each member has at most one possible
kept support even if every endpoint outside S has frozen. The first member
of S cannot freeze.

With EF fixed, the path V-U-A-B-C-D-G has five internal vertices and no
other available neighbours at these vertices. Exactly one of its ends is
used. Its only two possibilities are

    L: AB,CD,UV (G remains available below),
    R: AU,BC,DG (V remains available below).

There is an exact compression, useful for the reconstruction argument.
Delete A,B,C,D,E,U in each core and replace its four matching edges by
V_j F_j in state L, or F_j G_j in state R. This gives a perfect matching of
the FULL two-row rectangle {3,4} x {5,...,c}, with every F_j horizontal.
Conversely each such rectangle matching expands uniquely by the L/R rule.
The compression preserves every actual row-3/row-4 vertical edge.
A two-row rectangle matching decomposes uniquely, from its first uncovered
column, into one-column vertical blocks and two-column horizontal blocks:
if that column is not vertical both its vertices must match to the next.
This proves unique reconstruction from the vertical columns and will also
force the L prefix/R suffix, without a cycle-count assumption.

A vertical matching edge from row 3 to row 4 at odd column x will be called
an odd rung. Let O be its set of columns, INCLUDING x=c when g_m Q is used.
The lower row is a path of odd length 6m+5, so it must have a vertical edge.
Its successive vertical columns start odd, alternate odd/even, and end odd:
the unmatched lower-row segments before, between and after them must have
even length. Therefore O is nonempty. Between consecutive odd rungs there
is exactly one even rung. Once all vertical columns are specified, the
remaining lower-row matching is unique.

## 3. Two geometric traps

We use the first-member trap principle: if a nonempty endpoint set S has
at most one neighbour in T*, among granted sites, or with actual mate
outside S, at each member, no member of S ever freezes. This grants all
outside endpoints in advance and therefore excludes cross-component circular
justifications.

**Interval trap.** If x,z belong to O and z-x>=4, then

    S_(x,z)={white endpoints v: x<column(v)<z}

is a nonempty trap, even with BOTH grants.

Here is the complete boundary check. A bottom white endpoint strictly
between the cuts has its single selected neighbour below. Every endpoint
neighbour has its mate inside S: at the left cut, K immediately to the right
cannot match the cut's bottom white endpoint, since that endpoint is already
matched vertically; the same argument applies at the right cut. All other
bottom-row neighbours and their mates stay strictly between the cuts.

An upper white endpoint has no selected neighbour. Away from the two cuts,
its black neighbours have white mates inside the interval. Across a left
cut x, possible outside-mate support occurs only as follows:

| Cut type | Upper white endpoints immediately right of cut | Outside-mate witness |
| --- | --- | --- |
| V_j at x=6j+5 (core R) | B_j; F_j | A_j; V_j, respectively |
| G_j at x=6j+7 (core L) | H_j | G_j |
| g_j at x=6j+9 | b_j, if present | g_j |

Across a right cut z the complete corresponding list is

| Cut type | Upper white endpoints immediately left of cut | Outside-mate witness |
| --- | --- | --- |
| V_j at z=6j+5 (core R) | b_(j-1), if present | V_j |
| G_j at z=6j+7 (core L) | B_j; F_j | C_j; G_j, respectively |
| g_j at z=6j+9 | H_j | g_j |

Each listed endpoint receives at most one such support. A vertex in both
boundary lists would require x+1=z-1, excluded by z-x>=4. Forced EF keeps
the remaining E-neighbour dependencies inside the interval. These lists
also cover the upper vertices lying on a cut, which themselves are excluded.
Neither exterior grant is adjacent to S. Thus every member has at most one
possible support. Nonemptiness follows from the bottom white endpoint at
column x+2.

Consequently all odd rung columns in a completely frozen matching differ
by at most two. Since they are distinct odd integers, O is a singleton or
an adjacent pair {x,x+2}.

**Right-tail trap.** If q is absent and x in O with x<c, put

    W_x={white endpoints v: column(v)>x},
    adding U_j when x=6j+5.

This is a nonempty trap, even with p kept. At the bottom every member has
only its selected support, by the same shielding of the cut's vertical
edge. In the upper part the left-boundary table above is exhaustive. When
x=V_j, including U_j removes A_j as an outside-mate witness; U_j itself
has only V_j as an outside-mate support, and F_j also has only V_j.
No other upper member receives a support from outside W_x. Q has just its
selected bottom neighbour when q is absent. This proves the claim for every
matching with forced EF, without any assumption on its other rungs.

If q is absent in a completely frozen matching, O therefore has no column
before c. The bottom-row path then forces Z_l K_l for all l and g_m Q.
V_0 cannot be free, so core 0 is L. Inductively G_j must pair H_j and g_j
must pair b_j, leaving no mate for a free V_(j+1); hence every next core
is L. This recovers M*. Together with the EF trap this already proves
one-input rigidity for arbitrary matchings when q is absent.

## 4. The complete list and its count

If O={x}, there are NO even vertical edges; if O={x,x+2}, the unique even
vertical edge is at x+1. This follows from lower-row parity, not from freezing.
No pair {V_j,G_j} is possible, because both cannot be free after the L/R
core reduction. Thus the only possibilities are

    singleton V_j, G_j or g_j, 0<=j<=m: 3(m+1) choices;
    pair G_j,g_j, 0<=j<=m: m+1 choices;
    pair g_j,V_(j+1), 0<=j<m: m choices.

For each choice the matching is UNIQUE. Before the first rung the bottom
pairs are canonical; after the last rung they are shifted K_l Z_(l+1),
ending K_(n-1) Q unless Q itself is a rung. The optional even rung is
vertical. In the upper part, V_0 forces L until the first exceptional
location; after that location the exposed b_j must use V_(j+1), forcing R
successively to the right. Within each free top path the remaining adjacent
pairs are forced. This is also seen directly from its first unmatched vertex.

For explicit reconstruction, a rotated suffix starting at 1<=r<=m has five
transitions, with prefix L and suffix R. Put j=r-1. The exceptional edges are

| Type | Exceptional edges at the transition |
| --- | --- |
| V | V_r Z_(3r), with G_j H_j and g_j b_j canonical |
| gA | g_j Z_(3r-1), b_j V_r, with G_j H_j |
| gB | g_j Z_(3r-1), b_j K_(3r-1), V_r Z_(3r), with G_j H_j |
| GA | G_j Z_(3r-2), H_j g_j, b_j V_r |
| GB | G_j Z_(3r-2), H_j K_(3r-2), g_j Z_(3r-1), b_j V_r |

All R cores use EF,AU,BC,DG,Hg; subsequent b_i use V_(i+1). Complete the
remaining lower path intervals by their unique horizontal matching.
There is also the full suffix r=0 (the zipper of the preceding note).
When no core is R the three terminal choices are canonical; square flip
G_m Z_(n-1),H_m K_(n-1),g_m Q; and shifted tail
G_m Z_(n-1),H_m g_m,K_(n-1) Q.

The choices are distinct because their odd rung sets differ. Thus the exact
number is 3(m+1)+(m+1)+m=5m+4, equivalently 1+5m+3.
The interval trap has excluded EVERY other matching. It remains to prove
that all listed matchings actually freeze.

## 5. General positive freezing certificate

The following ordered waves use only actual mates. Each named witness is a
site; a previously frozen mate makes that site kept. Disjoint colours may
be processed separately. Repeating a wave for finitely many indices gives
a strict-rank certificate for every m.

For WHITE endpoints, the isolated white endpoint freezes immediately, as do
Z_0 (two selected sites) and Q (selected bottom site and granted q).
The lower horizontal pairs before the first rung propagate Z from left to
right: each next Z uses its selected bottom site and the left K whose mate
is the preceding frozen Z. After the last rung, the shifted lower pairs
propagate from Q right to left, using the right K instead. These two waves
freeze every bottom white endpoint, including the one or two odd-rung
endpoints. If there are two rungs, their intervening upper white endpoint
(H_j or b_j) freezes using the two neighbouring odd top sites whose mates
are now frozen below. Hence EVERY lower-row K site is now kept.

Here are the transition seeds, using those kept K sites throughout:

| Transition | First white seeds beyond the lower wave |
| --- | --- |
| V | mate(V_r)=Z_(3r) is frozen; b_(r-1), if present, uses V_r and its lower K |
| gA | H_j uses g_j and lower K; b_j uses g_j and lower K |
| gB | b_j already froze between the two odd rungs; H_j uses g_j and lower K; mate(V_r) is frozen below |
| GA | H_j uses G_j and lower K; then b_j uses g_j and lower K; F_j uses G_j and lower K |
| GB | H_j already froze between the two odd rungs; b_j uses g_j and lower K; F_j uses G_j and lower K |

The full zipper starts with mate(V_0)=Z_0. In every R suffix, propagate
left to right in the order

    F_j, U_j, B_j, D_j, H_j, b_j (omit b_m).

F_j uses V_j and lower K; U_j uses E_j and V_j; B_j uses A_j and E_j;
D_j uses C_j and E_j; H_j uses G_j and lower K; b_j uses g_j and lower K.
Their actual witness mates, respectively, are (incoming white,F's lower
white), (F,incoming), (U,F), (B,F), (D,lower white), (H,lower white).
The output b_j is the incoming mate of V_(j+1).

In the L prefix propagate right to left. Once H_j is frozen, use

    F_j, D_j, B_j, U_j, b_(j-1), H_(j-1).

F_j uses G_j and lower K; D_j uses E_j and G_j; B_j uses C_j and E_j;
U_j uses A_j and E_j; b_(j-1) uses V_j and lower K;
H_(j-1) uses g_(j-1) and lower K. Their mates are, in that order,
(H_j,lower white), (F_j,H_j), (D_j,F_j), (B_j,F_j),
(U_j,lower white), (b_(j-1),lower white).
At a G transition F_j is already seeded and D_j uses E_j,G_j with mates
F_j,Z_rung. At a g transition H_j is seeded. At a V transition the seeded
b_(r-1) gives H_(r-1), starting this reverse wave.

For the three terminal cases: canonical H_m uses g_m (mate Q) and lower K;
the square case already seeded H_m and F_m uses G_m (mate Z_rung) and
lower K; the tail case H_m uses G_m and lower K (mates Z_rung and Q),
and F_m uses G_m and its lower K. These start the same reverse L wave.
This covers every white endpoint.

For BLACK endpoints, first freeze the isolated black endpoint, all A_j,C_j
using their selected neighbours, then E_j using B_j,U_j in R or B_j,D_j
in L. Their mates are A_j,C_j. Next G_j in L uses D_j,F_j (mates C_j,E_j),
and V_j in R uses U_j,F_j (mates A_j,E_j).
Every internal g_i now freezes using its selected upper site and either
H_i with mate G_i in the canonical prefix, or b_i with mate V_(i+1) in the
suffix. The transition cases always have at least one of these two choices.
The terminal g_m uses its selected site and p. Therefore the top black
endpoint of every odd rung is frozen. If there is an even rung, its lower
black endpoint K uses its two lower horizontal neighbours whose mates are
the two frozen odd top endpoints.

All other lower K endpoints now propagate away from the rung(s) in both
directions. Each uses an upper site with early frozen mate E_j,G_j,g_j or
V_(j+1), and the horizontal neighbour whose mate is the preceding lower K
or an odd top root. The sole exceptional upper mate is the K at an even
rung, already frozen. The canonical prefix runs right to left; the shifted
suffix runs left to right. Finally every still-unfrozen V_j in L, or G_j in
R, uses F_j (mate E_j) and its lower Z site, whose mate has now frozen.
All black endpoints are covered. This proves sufficiency for every length.

The canonical matching needs NEITHER grant. Its lower white wave from Z_0
continues through all Z_l and then Q: Q uses its selected bottom site and
K_(n-1), whose mate Z_(n-1) has frozen. Its terminal black g_m uses the
selected site (2,c) and H_m, whose mate G_m has frozen in the early L wave.
The reverse white core wave and the lower black wave then run as above.
This supplies the no-grant seeds directly, without appealing only to the
older attainer certificate.

## 6. Exact response and one-input rigidity

Every noncanonical listed matching has either H_m g_m and K_(n-1) Q,
or the terminal square edges H_m K_(n-1),g_m Q. If p is absent,

    B={g_m,K_(n-1)}

is a trap: g_m has only its selected upper neighbour as possible support;
K_(n-1) has only Z_(n-1). The other neighbours have actual mates in B.
The black positive sequence above freezes every other black endpoint without
p: omit g_m and the final K, run the lower waves up to K_(n-2), and use
F_m,Z_(n-1) for G_m in an R core (mates E_m,K_(n-2)). Thus B is the EXACT
unfrozen black set. The q grant has no black effect.

For q absent, the exact white trap is W_x from Section 3 at the FIRST odd
rung x. Its complement freezes: the lower left-to-right wave reaches the
first rung's bottom endpoint; at a V cut this seeds b_(r-1) and the reverse
L wave; at a G cut F_j uses the rung and its lower K, starting its L core;
at a g cut H_j uses the rung and its lower K. These sequences freeze every
white endpoint outside W_x, with no right input. The p grant has no white
effect. Together with the two-input positive certificate, this gives the
entire four-state response, rather than just necessary-input claims.

Put k=m-r+1 for a nonempty R suffix. Direct coordinate counting gives

| Type | Missing edges of M* | |W| | Unfrozen with no inputs |
| --- | ---: | ---: | ---: |
| Full zipper r=0 | 8m+7 | 9m+7 | 9m+9 |
| V, r>=1 | 8k-1 | 9k-2 | 9k |
| gA or gB | 8k+1 | 9k | 9k+2 |
| GA or GB | 8k+3 | 9k+2 | 9k+4 |
| Terminal square | 2 | 2 | 4 |
| Terminal tail | 3 | 2 | 4 |
| Canonical | 0 | 0 | 0 |

For p only the deficit is |W|; for q only it is 2, except canonical has zero
in every state. The missing-edge column is d(M)=|M* minus M|=|M symmetric_difference M*|/2;
it is HALF the symmetric-difference edge count. These counts do not assume
that the symmetric difference is a single cycle.

Necessity with q absent was already proved for arbitrary matchings. If p
is absent but q is present, complete freezing would, after adding p, place
M on the classified list. The black trap rules out every noncanonical list
member. This proves the asserted rigidity with EITHER input missing.

## 7. Physical compensation and ambient consequences

T*/P* is fixed, so every original tile charge, demand and distinct donor
token is unchanged. Attach the SAME six-column cap from
[AMBIENT_BAND_PORT_ACTIVATION.md](AMBIENT_BAND_PORT_ACTIVATION.md).
Its early endpoints supply p and q independently of M. After the band has
frozen, all cap endpoints complete: every interface witness has its actual
mate inside the now-frozen band, irrespective of its identity.

The cap's early/completion sequences, its contribution |T_C|+|M_C|=18,
its zero net charge and token bijection, and the separator construction are
INHERITED premises from that note, not newly proved or independently audited
here. The present argument verifies their transfer to every classified band
matching. Concrete checks replay 215 such cap unions; the all-length
inherited proofs, rather than those finite checks, justify the general use.

Every classified matching therefore gives a completely frozen ambient
half-area configuration, with the SAME physical payment bijection and zero
reserve. The union has area 6(6m+16), and J=18m+48=area/2.
The cap supplies the two grants, so exactly 5m+4 band matchings (with cap
matching fixed) freeze. Separated stacks of t copies with the existing
zero-charge separators give at least (5m+4)^t fully frozen matchings on
identical T/P, again at half-area and with disjoint per-copy tokens.
This is a lower bound for the ambient board's full matching count; cap or
separator rematchings are not classified here.

Thus one-port absence restores complete local rigidity, whereas two ports
allow exactly linear-in-length local matching diversity and exponential
independent stack diversity. A compensating reserve cannot be assigned to
these rematching choices: every one uses the same already exhausted physical
ledger. This leaves the global half-area target intact and still open.

## 8. Verification scope

The accompanying coordinate verifier reconstructs all 5m+4 templates, checks
all four exact closures and trap supports, and independently compares queue
and synchronous closure. A separate exhaustive reduced-matching control
checks every matching, not just accepted ones, at m=2,3,4. Neither these
finite controls nor a Lean arithmetic audit replaces the general proofs
in Sections 2--6. The concrete coordinate adapter remains a written proof
unless explicitly identified as formalized in the formal receipt.


The saved coordinate run passes 1,454 candidate boards across 21 lengths
through m=40, 5,816 exact interface responses, 252,180 literal white-wave
steps, 1,763,658 strict actual-mate rank events, 860 independent synchronous
responses and 215 completely frozen cap unions. It rechecks 21 inherited
physical token bijections. Exhaustive reduced controls contain 495, 4,900,
48,505 matchings at m=2,3,4, with exactly 14,19,24 accepted; all 257,109
right-tail and 618,561 interval trap instances pass literal support checks.

The local Lean 4.33 audit passes five declarations without warnings, admitted
proofs or custom axioms. The main kernel turns the two separated boundary
support lists into exclusion from least freezing closure for arbitrary types;
the root normal form proves singleton/adjacent-pair structure at arbitrary
length without enumeration. The coordinate localization, EF/L/R reduction,
path parity/reconstruction and positive waves remain written, not end-to-end
Lean verified. The formal runner checks memory and real lean/lake processes
before every Lean invocation and removes its temporary compiled dependency.

Reproduce from the repository root:

    python3 develop/check_two_port_matching_classification.py --output output/two-port-matching-classification.json
    python3 develop/check_two_port_matching_classification_formal.py --output output/two-port-matching-classification-formal.json


Proof provenance: the local development and the separate Oracle proof-discovery
request both obtained the separated-odd-rung interval barrier and the same
classification. The [discovery response](../output/two-port-matching-classification-discovery.json)
also supplied the exact two-row rectangle compression, incorporated above.
That request is proof assistance, NOT an independent audit of the final note.
It uses inherited selected-neighbour incidences, now made fully explicit in
Section 1 and checked against the inherited constructor. It executed no code.
The final note has a separate audit request; its actual status is recorded
in the audit receipt, without treating a browser delivery failure as a
mathematical verdict.


The [separate independent final-note audit](../output/two-port-matching-classification-oracle.json)
returns narrowly REVISE, while explicitly finding the local all-length
classification, every positive wave, exact partial closures, uniqueness and
all table entries sound. Its requested edge-count wording, explicit canonical
no-grant seeds and threshold-two definition have been applied above. Its
ambient conclusion is conditional on the referenced cap, separator and ledger
certificates; that inherited scope is now explicit. The audit executed no
Python or Lean. We retain its actual REVISE verdict and do not relabel it as
an unconditional ACCEPT after making these presentation corrections.
