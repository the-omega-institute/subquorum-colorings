# The first consumer at secondary length ten: four necessary forms

21 October 2026. This identifies the first new branching after the
[secondary-eight double activation theorem](SECONDARY_EIGHT_DOUBLE_ACTIVATION.md).
It is a necessary-form theorem and one local activation theorem, not a
compensation theorem for the entire secondary-ten class. Full allocation
and rectangular-grid triple equality remain OPEN.

## Model and theorem

Use the same complete original U/rotor model, immutable original endpoint
ownership and matching, retained unconsumed original supports with their
original anchors as sole occupied neighbors, and fixed aligned two-by-two
tiles. Widths are even and at least six; both independent legs are even
and at least four. The parameter b is even and only translates the picture.
Prescribe distinct original sources

    Q=U(6,8,4), Q(r,c)=(b+2-c,11-r),
    D=U(m,10,t), D(r,c)=(b-11+r,c+5).

In every complete extension the support q=(b-5,7) must be an endpoint of
a third original owner. That owner is a U in one of the following four
forms. Here w is its width and v its independent far leg.

| Form | Physical chart | Necessary restrictions | Isolated charge |
|---|---|---|---|
| North terminal | (b-9+r,c+6), U(w,4,v) | 6<=w<=m-2 | 1-w |
| Outer corner | (b-5-r,c+6), U(w,4,v) | v>=6 implies w>=m; t>=6 implies w<=m-2, hence t>=6 implies v=4 | +1 |
| East terminal, bar down | (b-6+c,g+7-r), U(w,g,v) | g>=6; t>=6 implies g<=m-4 | +1 |
| East terminal, bar up | (b-4-c,g+7-r), U(w,g,v) | t=4 and g>=m | -1 |

The restrictions are necessary, not a sufficient description of disjoint
sources or of complete realizations. In the outer-corner case the near
terminal z=(b-9,7) has both original supports consumed by D, giving ONE
actual positive activation. No global injection or nonreuse claim is made
for this new activation.

## Proof of exhaustion

The west neighbor of q is D(6,1)=(b-5,6), and its south neighbor is
Q(4,6)=(b-4,7). Since q is Q's original support (4,7), it cannot remain
retained. It is in neither prescribed endpoint set. Its consumer therefore
has own endpoint neighbors only north and/or east. The U catalogue leaves
terminals and an outer corner with these two perpendicular neighbors;
straight interiors and degree-three roles cannot occur.

Both north rotor tips contain q+(-2,-1)=(b-7,6)=D(4,1).
The two east rotor tips contain, respectively, q+(1,2)=(b-4,9) and
q+(1,3)=(b-4,10), both Q endpoints. All rotor alternatives are excluded.

D's lower bar contains q+(-5,0)=(b-10,7)=D(1,2).
For a north terminal the contiguous incident stem therefore has length at
most four, hence exactly four. A corner's north-bearing incident leg has
the same bound. If instead its north neighbor starts the bar, that bar
has at least six columns and contains the endpoint five steps north,
which is impossible. Thus its bar points east and its north leg is four.
For either north-bearing form a leftward bar contains (b-9,6)=D(2,1).
The two displayed charts follow. East terminals have the two displayed
bar directions; their incident length g is an even integer at least four.
This proves catalogue exhaustion for arbitrary dimensions.

## Restrictions and the corner activation

For the north terminal its upper bar is the complete interval at row
b-9, columns 7 through w+6. D's far endpoint (b-9,m+5)=D(2,m)
exists for every t>=4. Hence w+6<m+5, which by evenness gives w<=m-2.

For the outer corner, if v>=6, its far stem contains (b-10,w+6).
If w<=m-2, that point also lies in D's lower bar. Thus v>=6 forces
w>=m. If t>=6, D(6,m)=(b-5,m+5) exists and the corner's complete
bar interval at row b-5 forces w<=m-2. These inequalities exclude
v>=6 when t>=6. Its near terminal z is original (4,1), whose original
supports are (5,1) and (4,0). Their physical images are
(b-10,7)=D(1,2) and (b-9,6)=D(2,1), respectively. Both are consumed.
The owner is positive by the charge calculation below, so z is activated.

For a downward east bar, g=4 puts its bar endpoint (b-4,11) in Q;
therefore g>=6. If t>=6, D(6,m) lies on q's row. Its collision with
the incident stem is excluded only when g+7<m+5, giving g<=m-4.
For an upward east bar, w>=6 guarantees an endpoint at row b-10,
column g+7. If g<=m-2 this is in D's lower bar, so g>=m.
When t>=6 the same incident-row bound g<=m-4 contradicts that
inequality; thus an upward bar requires t=4. The shorter far leg is why
the eight-step far-stem bound cannot be used here without qualification.

## Direct isolated-charge calculation

Put L=(near+far)/2. Every U has w-1+L original matching edges.
Count original supports inside touched physical tiles, whether subsequently
consumed or retained, as in the existing isolated-charge definition.
The four charts have the following counts:

| Form | Touched tiles | Original supports in those tiles |
|---|---|---|
| North terminal | w+L | L+2 |
| Outer corner | w/2+L+1 | L+4 |
| East, bar down | w/2+L+1 | L+4 |
| East, bar up | w/2+L | L |

These follow by pairing the consecutive bar columns and even leg rows
in each displayed chart; the two bar rows occupy one tile row for the
positive charts and two for the north chart. Substituting into
matching+inside-2*tiles gives 1-w, +1, +1, -1 respectively.
In particular the north branch cannot be treated as an activation of a
positive owner. It has a width-dependent isolated deficit.

## What an endpoint-only rule fails to prove

For every even w>=6, choose m=w+2, t=4 and the north terminal U(w,4,4)
in the displayed chart. Q, D and this owner have pairwise disjoint
endpoint sets. The consumer at q has charge 1-w, arbitrarily negative.
Thus endpoint disjointness alone does not imply a positive first consumer
or a uniformly bounded isolated deficit at secondary length ten.

The subsequent [support-closure theorem](SECONDARY_TEN_SUPPORT_CLOSURE.md)
excludes w=6 in the complete model for every far leg, and excludes the
entire upward g=m case. Upward branches force a U bar in an explicit
integer window; at g=m+2 the successor is positive and activated, with
width at most w-2. Its global target nonreuse remains open.

This is a partial stencil. Its unconsumed original supports may force
further owners, so it is NOT a counterexample to a theorem about complete
extensions, the desired compensation inequality or rectangular grids.
The next task is the support closure of this negative north branch and
the upward east branch, together with a global injection for the corner
activation into the one existing inventory. No credit is added to the
old ledger at this stage.

## Verification scope

[Independent controls](../develop/check_secondary_ten_first_consumer.py)
enumerate all bounded endpoint roles and rotor tips and check the four
charts, necessary restrictions and direct charge counts. They also check
the arbitrary-width partial stencil at separated test widths. These are
finite discovery and validation, not the proof of exhaustion above.
[Control output](../output/secondary-ten-first-consumer-controls.json).

[Scoped Lean](../formal/SubQuorum/SecondaryTenFirstConsumer.lean)
checks fixed blockers, the north-stem bound, chart collision implications,
corner support coordinates and charge arithmetic. It does not formalize
the U/rotor catalogue adapter, geometric tile counts, completeness or a
global allocation. See the
[validation receipt](../output/secondary-ten-first-consumer-formal-check.json).

Submitted DMGT and primary star-forming/C4-free work are preserved.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
