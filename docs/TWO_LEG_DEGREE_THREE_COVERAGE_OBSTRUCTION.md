# Three corner rules fail even in frozen occupied-degree-three networks

20 October 2026. The restriction left open after
[the 22-endpoint obstruction](THREE_RULE_FROZEN_COVERAGE_OBSTRUCTION.md)
is false: all three corner rules can have zero capacity even when every
endpoint has occupied degree exactly three. This note proves an unbounded
three-parameter family, not just one solver output. It also identifies a
degree-sensitive unit donor that pays this family's charge. Four-rule
coverage in the occupied-degree-three class remains open; the existing
22-endpoint example already refutes unrestricted four-rule coverage.
The general grid target remains open.
Submitted manuscripts are unchanged.

## 1. Construction and statement

Let w>=6, a>=4 and b>=4 be even integers. Work in the rectangle

    {0,...,max(a,b)+1} x {0,...,w+1}.

The endpoints are a two-row bar and two legs:

    P=({0,1} x {1,...,w})
      union ({2,...,a} x {1}) union ({2,...,b} x {w}).

On the left select (0,0), (a+1,1), and for each r=2,...,a select
(r,0) if r is even and (r,2) if r is odd. On the right reflect this
prescription in the line c=(w+1)/2, using height b: select (0,w+1),
(b+1,w), and (r,w+1) for even r, (r,w-1) for odd r=2,...,b.
Call the resulting selection set T. All unlisted vertices are blank.

The actual matching M consists of

- (0,j)--(0,j+1) for odd j=1,3,...,w-1;
- (1,j)--(1,j+1) for even j=2,4,...,w-2;
- (r,1)--(r+1,1) for odd r=1,3,...,a-1;
- (r,w)--(r+1,w) for odd r=1,3,...,b-1.

These edges cover P once. Let S=(a+b)/2. The complete component H=P has

    |P|=2(w+S-1),  |M|=w+S-1,  |T|=2S+2.

**Two-leg obstruction theorem.** For all the stated parameters:

1. The configuration is feasible, H is connected, and every endpoint has
   occupied degree exactly three.
2. No nonempty simultaneous endpoint promotion bundle is feasible,
   including mixed checkerboard directions.
3. Its original complete receiver has corrected charge rho_H=1.
4. Capped, selected-guarded and same-component two-endpoint-guarded corners
   all have zero capacity in every orientation.
5. Two distinct physical squares, Q_(1,1) and Q_(1,w/2-1), each have
   actual deficit one, detected by the degree-three guard of Section 5.

For w=6 and a=b=4 the whole rectangle is 6-by-8:

```text
TPPPPPPT
.PPPPPP.
TP....PT
.PT..TP.
TP....PT
.T....T.
```

Here P denotes an actual endpoint and T a selection. There are 18 endpoints,
10 selections and nine matching edges. This example is not claimed minimal.
Its full matching and 18-row certificate are in
`develop/two_leg_degree_three_obstruction.json`.

## 2. Feasibility and a general freezing proof

Every selection has precisely its displayed leg/bar endpoint as its only
occupied neighbor. Successive side supports alternate columns, while the
two inner support columns 2 and w-1 are separated by at least three.
At odd row 3 the bar is two rows away, so the inner supports also avoid it.
These observations check every type of selection, including both bottom
supports. They prove feasibility for all a,b, not just equal leg lengths.

Interior bar endpoints have three P neighbors. Each upper bar corner has
two P neighbors and one selection; each lower corner has two bar neighbors
and its leg neighbor. Interior leg endpoints have two P neighbors and one
selection; bottom leg endpoints have one P neighbor and two selections.
Thus every endpoint has occupied degree three and P is connected.

Write m for the actual mate. We give an order of all endpoints. Each row
has two distinct adjacent witnesses other than its own mate, each either
selected or equal to m(v) for an earlier frozen endpoint v.

First work up each leg's even rows r=h,h-2,...,2, where h is its height.
At (r,c) use its exterior selected neighbor and (r+1,c). At r=h the latter
is the bottom selection; otherwise it is the mate of the already frozen
(r+2,c). The two legs may be processed in either order.

Next freeze (0,1) using (0,0) and (1,1)=m(2,1). Move left to right through
columns j=2,...,w-1, freezing (1,j) for even j and (0,j) for odd j. Use its
vertical bar neighbor and the neighbor in the preceding column. At j=2
these are m(0,1) and m(2,1). Thereafter one is the mate of the preceding
wave vertex and the other of the vertex two steps earlier.

Independently start at (0,w), with witnesses (0,w+1) and (1,w)=m(2,w).
Move right to left through j=w-1,...,2, freezing row (w-j) modulo 2,
again using the vertical and preceding wave neighbors. Since w is even,
this second wave is disjoint from the first. Together they freeze every
upper bar endpoint and every lower interior bar endpoint.

Freeze the two lower bar corners, using their upper and inward bar
neighbors. Each witness is now the mate of a frozen bar endpoint. Finally
work down the odd leg rows r=3,5,...,h-1: use the inner selected support
and (r-1,c)=m(r-2,c). This accounts for each endpoint exactly once.

For any nonempty proposed bundle choose its first promoted endpoint in this
order. Both witnesses remain occupied: original selections remain, and
removing the mate of an earlier endpoint would require promoting that earlier
endpoint. The promoted vertex consequently retains two occupied neighbors,
contrary to feasibility. The argument covers every bundle at once and does
not assume one checkerboard direction. This proves assertion 2 generally.

## 3. Exact receiver charge and the full ledger

Use the original aligned tiles Q_(i,j)={2i,2i+1} x {2j,2j+1}.
The bar occupies w/2+1 tiles. Below it, the left and right legs occupy
a/2 and b/2 further tiles; these are disjoint because w>=6. Therefore

    |R_H|=w/2+1+S,  |T intersect R_H|=S+4.

The second count comprises the two upper supports, the even-row exterior
supports on the two legs, and their two bottom supports. The odd-row inner
supports lie outside the receiver. It follows that the receiver has S+2
blanks, and

    rho_H=|T intersect R_H|+|M|-2|R_H|=1.

This is the original corrected charge of the complete receiver. Raw tile
excesses need not equal individual corrected charges: the two bottom
saturated endpoint tiles each transfer their half unit to the tile of
their actual mate. All mates belong to H. Specifically the transfers go
from Q_(a/2,0) to Q_(a/2-1,0) and from Q_(b/2,w/2) to
Q_(b/2-1,w/2), each with weight one half. Thus both transfers stay in R_H
and cancel in its sum. The independent checker also computes the corrected
graph ledger and checks this equality directly.

Put Hmax=max(a,b). The whole objective and deficit are exactly

    |T|+|M|=w+3S+1,
    mn/2-|T|-|M|=Hmax*(w+2)/2-3S+1.

Since S<=Hmax and w>=6, this deficit is at least
Hmax*(w-4)/2+1>0. In the base example the objective is 19, half-area is 24,
outside deficit is 6, and total deficit is 5=6-1. Thus this family refutes
a coverage rule and does not refute the target grid inequality.

## 4. Exhaust all three old witness types

The only horizontal runs of at least four P vertices are the two bar rows.
The only vertical runs of at least four are the two leg columns, including
their bar corners. A cap needs four consecutive P vertices on an exterior
side of one physical tile, a P tip beside it, and a selected support next
to that tip along the side. We exhaust these runs, allowing even blank
padding around the construction.

For the upper bar row, a physical tile having it as exterior side is above
the bar; its necessary tip is blank. For the lower bar row, the tile is
below the bar. Its tip can be an endpoint only in a leg column. Its support
is then the next endpoint down that same leg, not a selection. For a leg
column, the physically aligned tile is toward the interior of the two-leg
shape. A required transverse P tip can occur only in bar row 1; its required
support is then another interior bar endpoint, again not a selection.
All remaining candidate tips are not endpoints; they are blank or selected.
For example, when (w,a,b)=(6,6,4), Q_(2,1) has the extended west endpoint
side (3,1),...,(6,1), but its upper transverse tip (3,2) is selected, not
an endpoint. This excludes that orientation before the other cap conditions.
The same non-endpoint exclusion covers every remaining cap orientation.

For either guard rule, the selected corner must have its unique occupied
neighbor outside its physical tile. The upper supports, even-row exterior
supports and bottom supports have that neighbor inside their tile. The
only eligible corners are therefore the odd-row inner supports:

    x=(r,2),  z=(r-1,3),  r=3,5,...,a-1,

and their right-hand reflections, using height b. For the left-hand z its
exterior neighbors are (r-2,3) and (r-1,4). The second is always blank;
the first is a bar endpoint when r=3 and is blank when r>=5. Neither is
selected, and they are never both endpoints. Reflection gives the same
conclusion on the right. Hence both guard rules fail even before their
same-component ownership conditions are imposed. This proves assertion 4.

Translation by an even vector and blank padding preserve the argument.
No boundary absence is responsible for the failure. Tile-preserving
rotations and reflections give all other physical orientations.

## 5. A degree-sensitive local donor

**Degree-three endpoint guard lemma.** Let x be a selected corner of Q,
with exterior endpoint anchor p in component H. Let z be the opposite
corner. Suppose an exterior neighbor q of z is an endpoint of H, its
three neighbors other than z are endpoints, and deg_A(q)<=3. Then Q
has exactly one occupied site, x, and actual deficit one.

Proof. Feasibility at x, which already sees p, forces its two neighbors
inside Q blank. The three named neighbors of q already occupy its full
degree allowance. Thus z cannot be occupied at all. This proves the claim.
Notice the degree upper bound is essential; this rule is not automatically
available at occupied-degree-four junctions. The local blankness proof
itself does not need terminality at z. QED.

For the family take Q_(1,1), x=(3,2), p=(3,1), z=(2,3), q=(1,3).
The other neighbors of q are (0,3),(1,2),(1,4), all endpoints. Its occupied
degree is three. Reflection gives Q_(1,w/2-1). The two physical tiles are
distinct even at the smallest width w=6, where they are adjacent. Reserve
either one to pay rho_H=1; their adjacency creates no overlapping resource.
For widths larger than six, the same two witnesses remain valid.

**Mixed ownership.** This rule can join the three earlier rules in the
conditional weighted compensation theorem. Its sole selection x and unique
occupied neighbor p identify the same owner for any two guard descriptions
on one physical tile. To compare with a capped description, normalize that
cap as in ELBOW_OWNED_DONORS.md. Its left corners are blank. If x is upper
right, its north endpoint is in the cap's component and must be p. If x is
lower right, the two exterior neighbors of its opposite upper-left corner
are both endpoints of the cap's component. The new q must be one of them,
and is required to belong to H. Thus the owners coincide in this case too.
The same argument compares with both earlier selected-corner guard rules.

Consequently, in a feasible single-terminal even-by-even grid, if each
positive complete receiver H has a set W_H of these
four kinds of witnesses with total actual capacity at least rho_H, then

    sum_(rho_H>0)rho_H <= sum_H sum_(Q in W_H)d_Q <= D_all.

Sets remove duplicate descriptions within H; the mixed-owner proof makes
different W_H disjoint. The original identity
mn/2-|T|-|M|=D_all-sum_H rho_H then proves the half-area bound for that
class. This is a conditional extension and explicit compensation of the
new obstruction. No unrestricted improvement of the existing five-sixths
bound follows from it.

In fact the previous 22-endpoint example also defeats this fourth rule.
Its four eligible selected-corner anchors are exhaustively listed in
THREE_RULE_FROZEN_COVERAGE_OBSTRUCTION.md. The first two have no exterior
endpoint at their opposite corner. For x=(4,3), the only possible guard
q=(5,1) has just two other endpoint neighbors, (4,1) and (6,1); (5,0) is
blank. For x=(5,2), q=(3,3) has the three required endpoint neighbors
(2,3),(3,2),(3,4), but also sees the selection (4,3), so its occupied
degree is four. It fails the degree upper bound. Thus unrestricted four-rule
coverage is false, while its occupied-degree-three restriction is open.

## 6. Verification and remaining problem

Run the independent physical controls:

    python3 -B develop/check_two_leg_corner_obstruction.py --output output/two-leg-corner-obstruction-controls.json

They check 39 parameter triples, including unequal legs and large widths,
and 624 physical/blank-padded symmetry images. Every original case has a
complete ordered freezing certificate. Each image is also checked by an
independent freezing closure and original corrected ledger, with zero
three-rule capacity and two distinct new unit donors. Separated two-, three-
and four-component controls combine all four rule types, check agreement
of repeated descriptions, and reserve distinct physical capacities. The
previous 22-endpoint fixture also has zero capacity under the fourth rule.
These checks test the construction; Sections 1-5 provide the unbounded proofs.

The optional discovery encoder now supports the third rule and an exact
occupied-degree-three constraint. Its simplified symbolic expressions agree
with the independent physical scanner in 80 controls across five connected
fixtures, both rule settings and all eight symmetries. The original 8-by-8
and 8-by-10 solver outputs are retained separately. The first reduces to
the base example by removing two empty top rows; the second has the same
matching with extra isolated selections. No finite unsatisfiability result
is used as a theorem.

`formal/SubQuorum/SaturatedEndpointCorners.lean` contains two locally
kernel-checked statements: the general normalized degree-sensitive local
lemma and the parameter-independent receiver arithmetic identity. The full
geometric family, mixed ownership and global adapter are written proofs,
not claimed formalized by these two statements. Execution and axiom audit
scope is recorded in `output/two-leg-corner-formal-check.json`.

The occupied-degree-three restriction does not rescue the old coverage
conjecture. The next structural target is a whole-network resource allocation
or an objective-preserving normalization that goes beyond endpoint promotion.
Any candidate must handle this bar with two independent legs and must prevent
capacity shared between components or routes from being spent twice. The
unrestricted grid bound and triple equality remain open. The original Oracle
review baa7b7d4 returned REVISE on 20 October Singapore: it found the
all-parameter construction, freezing, exact charge, local lemma and mixed
ownership sound, but corrected the non-endpoint-tip sentence in Section 4
and requested the omitted 22-endpoint dependency. The sentence is repaired
above and the complete dependency is supplied in the follow-up review.
The repaired package subsequently received ACCEPT in task82a21aa0-7a36-4278-b14c-847541ce4b23
at18:18:44.619UTC on19October, observed gpt_6/pro; the exact original
stream matches the archived terminal response. Acceptance includes the
all-parameter theorem, degree-sensitive guard/mixed ownership and old22
four-rule counterexample. The later remote-deficit and sealed-strip results
are outside its scope. Code and Lean execution retain separate receipts.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
