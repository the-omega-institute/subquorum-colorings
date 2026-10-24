# A maximal H return forces the adjacent incident leg

21 October 2026. This is a new consequence of the independently accepted
[four-column barrier](FOUR_COLUMN_CORNER_BARRIER.md). It removes the
matched-near-leg hypothesis from one unbounded H subclass. Unrestricted
mixed allocation and rectangular-grid triple equality remain OPEN.

## Statement

Use the finite complete original U/rotor model: original endpoint sets are
disjoint, unconsumed original supports are retained, and every retained
selected point has exactly its original anchor as its occupied neighbor.
Every source endpoint graph is connected. Work in the aligned physical
tile chart. All dimensions have their usual evenness and minimum bounds.

Suppose the complete family contains

    B=U(6,b,b-2), B(r,c)=(b+3-r,c+1),
    H=U(d,a,k),   H(r,c)=(r+3,c+2),
    b>=6, d>=6, 4<=a<=b-2, k>=4.

Then necessarily a=b-2. Consequently the physical tile

    Q={4,5} x {4,5}

is permanently H's original irregular 2P0T pair, under every complete
extension by arbitrary permitted sources. There is no bound on b,d,k or
the number of other owners. This is a necessary-condition theorem; it
does not assert existence for every independent choice of d,k.

## General proof

Consider D=[4,b+2] x [2,7]. B's near leg occupies column2 from row3
through b+1; its far leg occupies column7 from row5 through b+1; its
upper bar occupies row b+2 from column2 through7. H's lower bar occupies
row4 from column3 through d+2, which includes columns3 through7.
Together they occupy EVERY boundary vertex of D, including all corners.

The strict interior has four columns3,4,5,6. B has no interior endpoints.
H's only possible interior endpoints lie on its near leg in column3:
its far leg is in column d+2>=8 and both bars lie above or on the top
boundary. In particular the fixed owners have no endpoint on

    {5,...,b+1} x {6}.

Reflect the accepted four-column barrier by (r,c)->(r,9-c). The full
boundary is still full and column6 becomes the first interior column3.
The barrier therefore excludes EVERY foreign endpoint from the strict
interior. The reflection preserves adjacency and the permitted source
catalogue; no assertion that four columns alone exclude rotors is used.

If a<b-2, H's mandatory beyond-tip support x=(a+4,3) is strictly inside
D. Indeed a>=4 gives its row at least8 and a<b-2 gives a+4<b+2.
Its original anchor (a+3,3) is H's near terminal. B supplies the distinct
occupied neighbor (a+4,2), since 3<=a+4<=b+1. Retaining x would violate
its unique-anchor condition, so completeness requires x to be an endpoint.
It is not H-owned: it lies beyond that near terminal. It is not B-owned:
its column is3 and its row is strictly less than b+2. Thus it would have to
be foreign, contradicting the barrier. We conclude a=b-2. In fact this
step does not require evenness, though the source model does.

With that equality, the earlier three-column rectangle
[4,b+2] x [3,7] has its entire endpoint boundary and no fixed interior
endpoint. A foreign connected source cannot cross the boundary or fit
inside its three columns. Thus neither (5,4) nor (5,5) can be an endpoint.
Each is adjacent to H's endpoint above. A retained selection there would
therefore have to be an original H support, by anchor ownership. Their
intrinsic coordinates (2,2),(2,3) are not H supports. They are unoccupied,
and Q contains exactly H's lower-bar pair (4,4),(4,5), as claimed.

## Counting and residual scope

The counting dependency is the **long-H payment theorem**, Sections1--2 of
[A permanent pair for arbitrarily long negative H companions](LONG_HORIZONTAL_CORNER_CHANNEL.md),
not the width-six-H consequence in the four-column note. Its exact source
range is B=U(6,b,e), H=U(d,b-2,k), b>=6,d>=6,k>=4,e>=b-2 in the frames
used here, with the same complete source model. It was independently
accepted in review5a0cae69. Our equality a=b-2 and prescribed e=b-2 satisfy
ALL its hypotheses for every independent d,k allowed in this note. No
assumption d=6 or k>=b-2 is imported from the other barrier application.

For clarity, a claim is an actual labelled marked side (positive original
owner, intrinsic leg index), not one copy of each certificate detecting
it. Normalize that side as in the all-length companion theorem: A is its
positive producer, B consumes t=(3,2), C consumes p=(2,2), and H consumes
y=(3,3) as its outer upper corner. The physical receipt Q identifies H
by unique endpoint ownership. Its first lower-bar pair identifies the
bar end and upper corner y; the first pairs at opposite ends have columns
{4,5} and {d,d+1}, distinct even when d=6. At that y, its west endpoint
t is the actual B terminal and its north endpoint is C's straight-leg
point. B also owns (4,2), leaving (3,1) as the only possible external
positive-producer anchor at t. Unique ownership and canonical-gate
uniqueness recover the labelled original side. The argument is uniform
in d,k and b. A collision with an old short-H assignment identifies the
same side; in particular its b cannot simultaneously equal6 and exceed6.

The old corridor lower pairs need not all have assigned claims; they
still supply actual physical receipts. If a pair already assigned to a
claim is encountered again, reconstruction identifies that SAME claim.
It cannot pay an additional distinct side. Thus taking both the claim
union and physical receipt union preserves the injection, rather than
assuming that set union alone establishes it.

The other old resources cannot reuse Q. An upper-bar pair of H lies on
its different intrinsic bar row, and a different original owner cannot
own Q's two endpoints. Caps and m8 have three endpoints; Q has exactly
two. Q has no original terminal, ruling out any terminal occurrence
receipt there. It has no positive canonical-gate support: at either occupied
corner, both potential external anchors are H endpoints on the adjacent
upper/lower bar rows, so neither can belong to a positive producer. Any
original support at a permanently blank corner would have to remain selected,
a contradiction. Hence it
is the sole-owner lower irregular-bar-pair term of the exact defect
identity, distinct from upper pairs, triples, mutual pairs and activation
occurrences. The n0 contribution comes from the separate 2N-G estimate,
not a second use of a tile in 2R. These are the nonreuse interfaces of
the cited long-H payment theorem, restated for the present parameter range.

For an actual marked H claim, assign Q using the accepted reconstruction
from its unique original owner, first lower-bar pair and adjacent corner.
This is the SAME assignment as the long-H theorem after the forced
equality is substituted. Combine these receipts with old receipts by one
physical set union P; put p=|P|. Count the union of resolved claims as s,
and the remaining claims as t. Joint injectivity and disjoint receipt
profiles are inherited from the long-H theorem, giving

    s<=p,
    mu>=n0+u+p+ceil((m8-s-t)/2).

No new summand is created. If a newly recognized claim supplies a
previously uncertified physical pair, p increases by1 while moving that
claim from t to s leaves s+t unchanged; the certified lower bound rises
by1. If Q was already in P, recognizing it again gives no numerical gain.
The impossible shorter-a branches supply no extra n0 or reserve bonus.

For this W=6, e=b-2 subclass, unmatched near legs are now excluded rather
than assumed absent. The complete eleven-source family in the earlier
note realizes a=k=e=b-2 for all even b>=6. We do not claim new complete
examples with independently larger d or k. Cases e<b-2, wider returns,
Vcorner, occupied corridors and vertical exits still require work; no
universal improvement to the 5/6 bound follows from this subclass alone.

## Verification scope

The new checker independently reconstructs endpoint/support catalogues,
the reflected full boundary, its empty last interior column, and the
forced shorter-near support with two fixed neighbors. It also checks
matched-pair profiles and the already complete unbounded witness family.
Finite checks support the general proof and do not replace it. The
scoped Lean file checks boundary and reflected-column coordinates, the
forced support geometry and the equality deduction under the explicit
support-forcing and no-foreign-endpoint interfaces. Its full source-model
and physical counting adapters remain written. This new consequence is
outside the earlier independent review's submitted scope.

Local Lean4.33.0 compilation and all five individual axiom checks pass,
session89748 exit0, with only propext/Classical.choice/Quot.sound and no
sorry or native reduction. Preflight measured59% free memory and no real
lean/lake comm basename. Coordinate controls pass512 two-owner patterns,
432 impossible-short-near stencils,80 matched pair profiles and five
instances of the complete unbounded eleven-source family, through b=66.
The first independent written corollary review da2e66b8 confirms the geometry
but requests an explicit counting dependency. The exact long-H theorem,
claim reconstruction and cross-class nonreuse are now supplied above.
The directional phrase in its older packet has also been replaced by
the coordinate statement that the forced point's row is less than b+2.
Its original streaming session85537 is retained. Follow-up3519bcb2
ACCEPTS the repaired corollary and counting transfer, including all
independent d,k. Its8526-character response matches originalstream29030
exactly, exit0, observedgpt_6/pro. It does not certify program execution,
the separately referenced family construction or unrestricted allocation.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
