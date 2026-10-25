# Exact selection optima at an opposed interface: freezing costs one

25 October 2026. Haobo Ma and Wenlin Zhang. Independent research branch.

We settle the one-point uncertainty in the [opposed-direction construction](OPPOSED_DIRECTION_INTERFACES_AND_PIECEWISE_COMPENSATION.md).
For its fixed endpoint set, the unrestricted selection maximum is one larger
than the displayed fully frozen configuration. Among configurations in which
all endpoints are frozen, the displayed configuration is an exact maximum.
Both statements hold for every module count, with the actual matching unique.
The upper bound needs only TWO particular endpoints to be frozen. Its proof
is a local interface inequality, rather than a finite optimization result.

## 1. Statement and scope

For q>=1 let W=10q, L=W+2 and let P,M be the endpoint set and actual matching
of the opposed L-by-2L construction. Each isolated square has exact selection
maximum t=35q^2+13q+2. A selection U is feasible when it avoids P and every
v in U has at most one neighbour in U union P. Freezing uses the original
nonmate two-witness inductive rule. Then

    max_feasible |U| = 2t = 70q^2+26q+4;
    max_feasible_and_all_P_frozen |U| = 2t-1 = 70q^2+26q+3.       (1)

In fact |U|<=2t-1 if just

    p=(1,L-3),    z=(4,L+1)                                (2)

are frozen. These are physical endpoints, not abstract source owners. The
known one-deletion configuration freezes all endpoints and attains this bound.
Since P has a unique perfect matching, these maxima also allow arbitrary
rematching on P. They do not optimize over replacing P.

At the attaining fully frozen configuration, BOTH aligned uniform band
directions still pay exactly q of their2q alphas, with the entire original
pool available. The valid opposite-direction square partition pays all2q.
Consequently the earlier obstruction survives EXACT selection optimization
within the fully frozen class. This is an existential statement about a
maximizer: it does not say every fully frozen maximizer has the same network,
or that every unrestricted maximizer fails compensation. The unrestricted
maximum itself need not remain frozen. There is no new universal5/6 bound.

## 2. A local four-tile loss forced by two frozen endpoints

Use column offsets from L. Let D be the two-row, eight-column strip

    rows2,3; columnsL-6,...,L+1.

Split it into four consecutive2-by2 tiles D0,D1,D2,D3. The old endpoint-only
cover gives caps1,2,2,1 on these tiles, respectively. We prove the sharper
local inequality

    |U intersect D| <= 5                                  (3)

whenever p,z in(2) are frozen. All other selected points may be changed.

Here is the full stencil. A feasible selection in D is contained in

    row2: columns L-4,L-3,L-2,L-1,L;
    row3: columns L-5,L-4,L-3,L-2,L-1,L.

The remaining sites are endpoints or have at least two endpoint neighbours.
In particular the only selectable site in D0 is a=(3,L-5). Both sites in
D3 face endpoints in columnL+1, so at most one is selected. D1,D2 use the
usual cap2 for a2-by2 square.

**What freezing actually forces.** The endpoint p=(1,L-3) has its actual
mate(1,L-4). Its three nonmate neighbours are(0,L-3),(1,L-2),(2,L-3),
none of which belongs to P. At any last step of its freezing derivation,
at least two of these three must therefore be selected. In particular

    (2,L-3) not in U  implies  (1,L-2) in U.                (4)

The endpoint z=(4,L+1) has its actual mate(5,L+1). Its three nonmate
neighbours are(3,L+1) in P,(4,L),(4,L+2). The last site has two endpoint
neighbours, z and(5,L+2), so is never selected. At most ONE nonmate witness
can therefore be supplied from P; freezing z requires

    (4,L) in U.                                          (5)

These are necessary conditions for the inductive freezing rule. They do not
assume a particular rank schedule, nor do they assume that the other P
witness for z has already become usable. Allowing it only weakens the test.

Suppose, for a contradiction, D attains its old cap6. All four tiles must
attain their individual caps. In D0 this forces a=(3,L-5). The point a
already faces P(3,L-6), so(3,L-4) is unselected. To attain2 in D1, the
only remaining candidates are b=(2,L-4),c=(2,L-3),e=(3,L-3). The point c
faces P(1,L-3), so cannot be selected together with b or e. Thus b and e
must both be selected and c must not. By(4), u=(1,L-2) is selected. It
faces P(1,L-3), and therefore excludes f=(2,L-2).

D2 must contain two selections among g=(2,L-1),h=(3,L-2),i=(3,L-1),
because f is excluded. If g were absent, both h and i would be selected,
and h would have two selected neighbours e,i. Thus g is selected.

D3 must contain one of j=(2,L),k=(3,L). By(5), k cannot be selected:
it would face both P(3,L+1) and U(4,L). Therefore j is selected. But j
then faces both P(2,L+1) and g, contradicting feasibility. This proves(3).
The argument uses a fixed sixteen-cell strip and two explicit freezing
requirements; it works unchanged for every q>=1. QED.

An equivalent integer certificate is useful for independent verification.
Let a,b,c,d,e,f,g,h,i,j,k be the0/1 indicators of the eleven listed sites,
where d=(3,L-4), and let u indicate(1,L-2). Feasibility, tile caps and the
two freezing requirements imply

    b+c+d+e<=2, f+g+h+i<=2, j+k<=1,
    a+d<=1, b+c<=1, c+e<=1,
    c+u>=1, u+f<=1, h+e+i<=2, j+g<=1, k=0.              (6)

Together with0<=a,...,u<=1 and integrality, these yield a+...+k<=5.
This is a local packing inequality. In particular the loss is charged to a
single physical strip; no source or interval credit is spent twice.

## 3. Inserting the loss into the old disjoint cover

Recall the exact upper cover for each isolated square: aligned2-by2 tiles,
with2q disjoint4-by2 patch replacements of cap3 instead of4. Its total is t.
Transport the entire right cover by the reflected transpose. Combining the
covers gives a disjoint physical cover of the full board of total cap2t.

The four tiles making D are all UNREPLACED members of this cover. On the
left their column pairs are L-6,L-4,L-2; their upper row is2. The replaced
left patches have columns2+10i,3+10i, so none overlaps these three tiles
in the last module. On the right, the tile rows2,3 and columnsL,L+1 is the
image of the original tile rows0,1 and columnsW-2,W-1; its columns are not
those of a replaced patch either. It has cap1. Thus the four old cap entries
are exactly1+2+2+1=6, and their cells meet no other cover member.

Replace precisely these four contributions with the single cap5 from(3).
Keep every other cover member once. This proves |U|<=2t-1 under the two
freezing hypotheses. The earlier fully frozen one-deletion construction
attains2t-1. This establishes the second maximum in(1), with no assumption
that previously selected points must be retained.

## 4. An unrestricted maximum exists for every q

The upper bound2t holds for every feasible U by restricting to the two
squares. Here is an explicit uniform modification that attains it. Start
from the earlier one-deletion selection T, change only the LEFT square,
and put

    E={10i+2,10i+10:0<=i<q},
    I={10i+1:1<=i<q},    J={10i+11:0<=i<q}.

Remove

    {(0,c):c=3,5,...,L-1} union ({1} times E) union ({2} times I),

and add

    {(0,c):c=2,4,...,L-2} union ({2} times E) union ({1} times J). (7)

All removed points are in T, all added points are absent from T, and all
are outside P. The three removed sets have5q,2q,q-1 points; the three
added sets have5q,2q,q points. The total increases by exactly1.

For completeness, feasibility can be checked uniformly without search.
The changed rows become

    row0: {1} union {2,4,...,L-2};
    row1: {0} union J;
    row2: {0} union {10i+8:0<=i<q} union E.

Row0 has only the selected adjacency1--2; neither endpoint of that pair
has any other occupied neighbour. Its other points are horizontally separated and have at most their single
vertical occupied neighbour in row1. The point(1,0) retains its sole
occupied neighbour(2,0). A point in row1 with column in J has blank sites
above and below and no horizontal occupied neighbour; J columns are1 mod10
and lie between the P slabs. Every point of E in row2 has blank neighbours
above, below and horizontally; the removed I points are exactly the possible
old horizontal contacts there. The unchanged(2,10i+8) points face their one
endpoint above and no new occupied neighbour. The only remaining old
occupied pair in these rows is(1,0)--(2,0). In row3 the changed row2 adds
only above columns2 or0 mod10, while all its old selected columns are1,3,7,9
mod10. Its occupied-neighbour counts therefore do not increase. Lower rows
are unchanged.

At the square seam the changed left boundary now has row1 selected and
rows0,2 blank. The right seam at row1 is blank, and the old contacts at
rows0,2 have disappeared. Every other cross-seam contact is unchanged.
The full modified configuration is feasible and has2t selections.

It is not fully frozen: for p=(1,L-3), ALL THREE nonmate neighbours
are absent from the modified selection. Indeed L-3=10q-1 is odd and greater
than1, so row0 omits it; the row1 point in E was removed, and the row2 point
is in neither E nor any retained row2 set. No nonmate neighbour is an
endpoint. Thus p cannot have a freezing derivation. This explains why
reaching the unrestricted bound does not contradict Section3.

## 5. Checks and formal scope

The permanent checker uses no SAT/MILP solver. It verifies the local packing
bound by all2^14 assignments to the eleven strip candidates, the two other
possible witnesses for p, and the forced point for z. It checks actual
coordinate adjacency and endpoint occupancy, and extracts the implication(4)
from the two-witness requirement. These checks corroborate Section2's
general proof; they do not replace it.

It also checks all-q formula instances, exact disjoint-cover membership,
both explicit selections, and complete freezing of the lower attaining
configuration on q=1..8,10,12. The unrestricted maximum's witness failure
at p is checked directly. The old directional certificates apply unchanged
to the frozen configuration, and are linked rather than reinterpreted for
the unrestricted maximum.

Local Lean4.33.0 passes13 new declaration audits and47 dependency audits,
without warnings, placeholders, native evaluation or new axioms.
Lean proves the general integer packing inequality(6), the two-witness
necessary condition for any inductively frozen endpoint, the substitution
of a local loss into an arbitrary nonnegative cover remainder, and the
all-q count/slack identities. Concrete certificates check the sharp local strip, the actual endpoint
stencil, the feasible100T unrestricted q1 construction, and its witnessless
endpoint’s inductive nonfreezing. The all-q stencil
transport, cover membership, explicit unrestricted construction and its
coordinate feasibility remain written proofs plus Python checks. No
end-to-end Lean verification of the grid optimum is claimed.

The substantive new conclusion is the exact distinction between unrestricted
selection optimality and selection optimality subject to complete freezing.
The next geometric question remains how to construct adaptive directional
partitions when actual matching edges cross the proposed boundaries. Public
main, the11 October manuscript, and all email drafts remain unchanged.

Reproduce from the repository root:

    python3 develop/check_frozen_interface_optimality.py --output output/frozen-interface-optimality-validation.json
    python3 develop/check_frozen_interface_formal.py --lean /path/to/lean-4.33.0 --output output/frozen-interface-optimality-formal-validation.json
