# Whole-board endpoint invasion: a sharp half-area compensation theorem

Successor: [unprotected white selections, sharp new-black terminal cost and prefix obstruction](UNPROTECTED_WHITE_PAIR_AND_PREFIX_BUDGET.md) removes the two protected-white assumptions and settles one new black-selection permission.

27 October 2026. Wenlin Zhang and Haobo Ma.

We remove the six-cell permission restriction from the previous occupied-envelope
budget. Retain the original endpoints P0 of the frozen half-area family, and
allow T to be ANY subset of its original selections T0. New endpoints may occur
ANYWHERE on the board and the actual matching may change arbitrarily. Then

    |T| + |M| <= 18m+30 = area/2, for every m>=2.                 (1)

No freezing assumption, local colour balance or retained old matching edge is
needed. The old fully frozen family and all its mixed six-cell expansions attain
(1), so this is the exact whole-board maximum in the stated class. This goes
beyond the previous six-cell domain, but does not classify all equality footprints
in the larger domain. The universal 5/6 problem remains open. No revision of the
submitted 11 October manuscript is made.

## 1. Definitions and a stronger sufficient skeleton

Write c=6m+9 and R={0,...,5} x {0,...,c}. A feasible pair consists of selected
sites T and a matching M of nearest-neighbour edges. Write P for its endpoints,
O=T union P, and H=R minus O for the genuinely empty sites. T and P are disjoint;
each selected site has at most one occupied neighbour. Black means even
coordinate sum; white means odd. Every matching edge joins one of each colour.
Thus, writing subscripts for colours,

    J=|T|+|M|=|T_black|+|O_white|,
    area/2-J=|H_white|-|T_black|.                              (2)

In fact the proof only needs the following weaker hypotheses. They make the
geometric and actual-matching content explicit.

* c is odd and c>=5, with the same six-row board.
* Black selected sites belong to

      B*={(2,0),(3,1),(3,3),(4,0),(4,2),(4,4),(5,1),(5,3)}
          union {(5,k):k odd, 5<=k<=c}.

* (2,1) and every (4,k) for odd k from 5 through c are occupied (T or P).
* The two white sites (5,0),(5,2) are NOT selected. If occupied, they therefore
  have distinct actual matching mates, as required by a matching.

Under these hypotheses (1), with right side 3(c+1), holds. Other white selections
may be placed anywhere consistent with feasibility and these hypotheses; other
endpoints are unrestricted. For the original family T subset T0 and P0 subset P
imply all the hypotheses: its black selections are exactly B*, its displayed
anchors belong to P0, and the two bottom white sites are absent from T0.

Feasible sharpness alone has an even simpler construction: set T empty and
match each column vertically as (0,k)--(1,k), (2,k)--(3,k), (4,k)--(5,k).
This covers the entire board, retains P0 and attains J=area/2. It is not frozen:
with no selected seeds the freezing process never starts. Thus feasible
sharpness is independent of prior frozen constructions; the established fully
frozen family supplies the stronger sharpness statement used above.

The original T0 is specified by

    rows 0 and 5: all odd columns 1,...,c;
    row 1: {2} union {4+6j,8+6j:0<=j<=m};
    row 2: {0,3} union {9+6j:0<=j<=m};
    row 3: {1,3}; row 4: {0,2,4}.

Its original endpoints have rows

    {(r,k):r=1,2; k in {1} union {5+6j,6+6j,7+6j:0<=j<=m}}
       union {(r,k):r=3,4; 5<=k<=c}.

The established matching construction has |T0|=9m+21, |M0|=9m+9
and complete freezing; it supplies sharpness, not an upper-bound premise.

## 2. The nine-hole pocket lemma

The eight possible black pocket selections, in order, are

    a=(2,0), b=(3,1), d=(4,0), e=(4,2),
    f=(4,4), g=(5,1), h=(5,3), with C=(3,3).

Use the lower-case Boolean indicators a,b,C,d,e,f,g,h for whether these sites
are selected. The nine distinct WHITE pocket sites are

    u=(1,0), v=(3,0), w=(3,2), x=(4,1), y=(2,3),
    z=(3,4), q=(4,3), r=(5,0), s=(5,2).

Here u,v,w,x,y,z,q,r,s denote the Boolean indicators that these sites are
EMPTY, rather than merely unselected. Selected-degree constraints and the
occupied anchors (2,1),(4,5) give

    a<=u; b<=v,w,x; f<=z,q;
    3C<=w+y+z+q;
    2d<=v+x+r; 3e<=w+x+q+s;
    2g<=x+r+s; h<=q+s.                                      (3)

For example, C has four displayed neighbours and needs three of them empty.
The neighbour (5,4) of h is deliberately omitted: a selected h still needs at
least one of q,s empty. It will belong to the separate bottom-boundary budget.

There is one additional ACTUAL-MATCHING capacity constraint. Each occupied r
or s is an endpoint because those two sites are not selected. Their complete
neighbour union is {d,e,g,h}. Their mates must be different members of this
union and cannot be selected. Therefore

    d+e+g+h <= 2+r+s.                                       (4)

This uses two physical sites and four physical potential mates. It is not a
fractional matching assumption or a second use of an existing surplus token.

**Pocket lemma.** Binary variables satisfying (3),(4) satisfy

    a+b+C+d+e+f+g+h <= u+v+w+x+y+z+q+r+s.                    (5)

Here is a direct algebraic proof, valid whenever these hypotheses hold.
First a<=u, so cancel that pair. Put D=d+e+g+h and k=v+w+x+y+z+q.
We repeatedly use the following two elementary consequences of (3):

    C+f <= w+y+z, and C+f <= y+z+q.                         (6)

Indeed, C=1 requires at least two blanks in either indicated triple, while
f=1 requires a member (z) of the first triple, and both z,q of the second.
When the triple sum is 0 or 1, C=0; when it is at least 2 the sum C+f<=2
suffices. Also, for any binary E with E<=w+q,

    C+f+E <= w+y+z+q.                                      (7)

For the four-blank sum 0, E=0 as well; at sum 1, C=f=0; at sum 2, C=0;
at sums at least 3 use C+f+E<=3. This proves (6),(7) without enumeration.
Now split only on the two bottom blank indicators r,s.

* r=s=1. We have d<=max(v,x), b<=min(v,x), g+h<=2, and e<=w+q.
  Hence b+d<=v+x. Equation (7), with E=e, gives
  b+C+f+D <= v+x+(w+y+z+q)+2=k+r+s.
* r=1,s=0. If e=0, (3) gives D<=max(v,x)+x+q. If e=1,
  w=x=q=1, and the same right side equals 3; (4) gives D<=3.
  In either case b+D<=v+2x+q. Add the first bound in (6), and use x<=1,
  to obtain b+C+f+D<=k+1.
* r=0,s=1. If v=0 then b=d=0, g<=x, h<=1, and e<=w+q.
  Equation (7) gives C+f+D<=w+y+z+q+x+1=k+1.
  If v=1 then D<=2+x: for x=0, d=g=0, and for x=1 use (4).
  Now b<=w and the second inequality in (6) give the same k+1 bound.
* r=s=0. If q=0 then e=f=g=h=0, b,d<=min(v,x), and
  C<=w+y+z. Thus b+C+f+D<=v+x+w+y+z=k.
  If q=1 then (3),(4) imply D<=1+x*max(v,w). To see this, when x=0
  only h can be 1; when x=1 at least one of v,w must be 1 to allow d or e,
  and (4) caps their joint contribution with h at 2.
  Since b<=v*w*x and v*w+max(v,w)=v+w for binary v,w,
  b+D<=1+x*(v+w). Add C+f<=w+y+z from (6) and
  x*(v+w)<=v+x to obtain k (recall q=1).

These four algebraic cases prove (5). Finite Boolean checks below validate this
written proof; they are not the all-length argument.

## 3. Disjoint global compensation

Every other possible black selection is t_k=(5,k), for odd k>=5. Its upper
neighbour (4,k) is occupied by hypothesis. Feasibility forces the distinct
white site ell_k=(5,k-1) EMPTY whenever t_k is selected. Thus

    |T_black outside pocket| <= |H_white intersect L|,
    L={(5,k-1):k odd,5<=k<=c}.                              (8)

All nine white pocket sites are distinct, and none belongs to L. In particular
(5,4), omitted from the local h constraint, is the FIRST site of L; it is
never counted as a pocket payment. Add (5) and (8). Since every allowed black
selection occurs in one and only one of their left sides, they yield

    |T_black| <= |H_white intersect pocket|+|H_white intersect L|
              <= |H_white|.                               (9)

Equation (2) proves the theorem. The two sets on the right side of (9) are
physical sites, disjoint by their coordinates. The pocket capacity (4) counts
actual mates injectively. This is the unified cross-region inequality; neither
an empty site nor a mate is counted twice.

A useful explicit refinement is

    area/2-J = (H_pocket-T_pocket)+(H_L-T_tail)+H_other,       (10)

where H_pocket counts empty sites among the nine displayed WHITE pocket sites,
T_pocket counts the eight BLACK pocket selections, H_L=|H intersect L|,
T_tail counts selected t_k, and H_other=|H_white minus (pocket union L)|.
Each summand is nonnegative. Equality forces ALL three summands to
vanish. This is a necessary and sufficient scalar criterion, not a
classification of equality footprints or their matchings. It exposes how a
local pocket deficit cannot be hidden by reusing bottom-boundary holes.

On the original aligned 2x2 tiles, use chi=4-2|T intersect tile|-|P intersect tile|.
The tile sum is area-2J, so the theorem also gives a capacity-respecting global
payment: distinguish every positive half-unit by (tile,index), pay every
negative half-unit once, and leave exactly area-2J unspent units. This global
existence statement does not claim a local routing or preservation of a chosen
old payment. In contrast, (9),(10) explicitly preserve the identities of the
physical empty sites used in this proof. Neutral mixed envelopes keep their
previous literal token/debt cancellation, independently of this new bound.

## 4. Why the actual-matching condition is necessary to this proof

The degree-only version of (5) is false. For instance set

    a=b=0; C=d=e=f=g=h=1;
    (u,v,w,x,y,z,q,r,s)=(0,0,1,1,0,1,1,1,0).

All degree implications (3) hold. Six pocket selections demand only five
empty sites. But r is empty and s is occupied; s=(5,2) has all three possible
mates e,g,h selected. It cannot be an actual matching endpoint. Equation (4)
reads 4<=3 and fails. This refutes a rule using degree constraints alone; it
is not a feasible grid counterexample or a failure of (1). A second degree-only pattern makes the joint nature explicit:

    a=g=0; b=C=d=e=f=h=1;
    (u,v,w,x,y,z,q,r,s)=(0,1,1,1,0,1,1,0,0).

Again six selections face only five blanks, and (3) holds. Both r,s are now
occupied. Each has a possible individual mate, but both can only use g=(5,1),
because d,e,h are selected. Paying both occupancies with g would use the SAME
physical endpoint twice. The two-site constraint (4) excludes this pattern,
whereas checking these two singleton capacities separately would not suffice.
This is a local algebraic obstruction, not a feasible global counterexample.

## 5. Verification, provenance and limits

The proof of arbitrary length is (2)--(9), including the explicit four-case
pocket argument. The standard-library verifier checks the local algebra,
physical-coordinate hypotheses, actual-mate capacity and the exact identity
(10). It also verifies all original and previously proved mixed frozen
attainers used for sharpness, and checks literal unrestricted-invasion
examples produced in separate solver discovery. The portable verifier itself
uses no optimizer. Its JSON receipt gives exact counts and coverage.

The accompanying Lean file checks the local binary compensation inequality,
the helper bounds, actual two-site capacity arithmetic and the disjoint global
counting consequence. Coordinate adjacency, actual-mate injection into the
four sites and the existing frozen construction are written proofs with
executable controls; no end-to-end formalization of the whole grid is claimed.

Discovery uses CP-SAT with all grid edges available, P0 retained, T subset T0,
selected-degree constraints, and optionally strict actual-mate ranks. Discovery
is evidence for choosing the proof, not a premise or proof of the theorem.
The frozen search checks strict rank feasibility independently against the
existing freezing closure. No shared CI or manuscript is changed.

The saved solver-free receipt covers 655 boards, including 438 fully frozen
sharp attainers, 128 arbitrary whole-board matching/selection controls and
22 controls with new white selections outside T0 under the weaker skeleton.
It checks 14,619 distinct bottom-boundary payments, 179 actual two-site mate
events and 3,329 global tile payments. Local controls cover 11,640 degree-feasible
binary models, of which 11,355 pass actual matching capacity; ten degree-only
deficit models are excluded by that capacity. There are 100 tight local models.
Six scoped Lean 4.33.0 declarations pass locally, without warnings, sorry or
nonstandard axioms. The local process/memory preflight is recorded before
each Lean invocation; no CI result is claimed.

A literal equality example outside the former six-cell domain is included in
[the example data](../output/whole-board-endpoint-invasion-examples.json).
On the 6x22 board it has 31 selections and 35 actual matching edges; all 70
endpoints freeze. Besides both interior six-cell envelopes it converts
(1,20),(2,21), fills (1,21),(2,20), and rematches actual edges as recorded in
the data. This is a checked finite example, not an asserted all-length new
terminal construction. The original six-cell equality-footprint classification
was scoped to its permission domain and is not contradicted.

Reproduce with

    python3 develop/check_whole_board_endpoint_invasion.py --output /tmp/invasion.json
    python3 develop/check_whole_board_endpoint_invasion_formal.py --output /tmp/invasion-formal.json

See the [coordinate receipt](../output/whole-board-endpoint-invasion.json),
[Lean source](../formal/SubQuorum/WholeBoardEndpointInvasion.lean) and
[formal receipt](../output/whole-board-endpoint-invasion-formal.json).

Independent broker review
[30681da6-c890-4c0c-8d79-02f4bf58b14e](../output/whole-board-endpoint-invasion-oracle.json)
completed with ACCEPT, observed gpt_6 / pro. The exact original stream agrees
with the terminal response. It checked the written pocket cases, actual-mate
capacity, disjoint coordinates, stronger skeleton, objective identity and
scalar equality criterion. It did not execute code or independently establish
the existing complete-frozen constructions. Its clarification of the slack
counts is applied above; its simpler perfect-matching feasible attainer is
recorded as proof assistance, separate from frozen sharpness.

The former six-cell exact partial-mask deficits remain useful inside their
scope. This theorem settles their previously open whole-board endpoint
extension at the half-area level. Selecting new black sites outside B*,
withdrawing the occupied anchors, general mixed configurations, sharp losses
for prescribed arbitrary invasions and full equality classification remain
open. In particular this result does not establish a universal improvement
of the existing 5/6 bound.
