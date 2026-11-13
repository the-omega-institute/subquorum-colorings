# One auxiliary sixteen-cycle with arbitrary physical owner cycles

13 November2026. We prove a complete all-size sufficient class for the actual
all-helper target. The construction uses one final exterior exchange forest,
then chooses a reserved region while preserving every exact boundary choice.
Two mixed-cycle lemmas address cases not covered by square-owner estimates.

## 1. Physical statement and normalization

Let V have N=2b vertices. Let P,Q be disjoint perfect matchings such that
A=P union Q=sC4 disjoint-union C16. Let B be a simple union of even owner
cycles, all of length at least four. A physical colouring c is constant on
P-edges and opposite on Q- and B-edges. An omission set U is permitted when
B[V minus U] induces maximum degree at most one.

**Theorem.** There is a permitted U with

    nu(A[U]) <= floor(N/6).                              (1)

In the original physical graph on5b vertices this gives an actual dissociation
set containing all b helpers with cardinality at least ceil(8b/3).

The physical graph has one helper per P-edge, one witness and one owner per
index, helper-witness edges, the perfect witness-owner edges, witness edges Q
and owner edges B. For fixed omitted owners U, selected witnesses must be
independent in A[U]. As A is bipartite, the exact all-helper normalization is

    beta_I=3b-min_permitted_U nu(A[U]).                   (2)

This is not an identity for unrestricted beta_2 or SF_2. We use the established
base cases: all auxiliary squares; at most one auxiliary square; and owner
cycles of orders4 or6k only. Proofs are in the auxiliary-square forest
manuscript and `MIXED_OWNER_BRIDGES.md`. The preceding C12 theorem and its
supplier remain unchanged. The new statements do not solve arbitrary mixtures
of long auxiliary cycles or physical rectangular-grid routing.

## 2. Omission deficits and one common forest

A minimum omission set on an owner cycle of order m has size ceil(m/3).
Indeed, every three consecutive vertices must contain an omission, and gaps
of at most three attain this count. For minimum omissions everywhere, put

    M=N/3+d,
    d=sum_C d_C,
    d_C=2/3 if m=4 mod6, 1/3 if m=2 mod6, 0 if m=0 mod6.

Call positive-deficit cycles exceptional. For any U,

    delta(U)=|U|-2nu(A[U])

counts the odd-order components of A[U], including isolated vertices. For the
new cases below, it suffices to retain minimum owner counts and obtain

    delta(U)>=d-1/3.                                    (3)

For every oriented edge xy of an exceptional owner cycle, there are two
minimum omission sets differing exactly by replacing x with y. For C4 use
{x,opposite(x)} and replace x. For longer cycles arrange a gap2 immediately
before x and a gap3 immediately after x, all other gaps3 except for the
additional gap2 needed when m=1 mod3. The exchange replaces gaps2,3 by3,2.

Contract every auxiliary component to a node. Each exceptional owner cycle
provides its projected crossing edges, with its cycle label. A rainbow forest
uses at most one edge per label. With ell labels its maximum size is

    r=min_J (ell-|J|+rho(E_J)),                           (4)

where rho is graphic rank. This is Rado's independent-representatives formula;
the inherited forest manuscript supplies the proof and Rado1942 reference.
An empty crossing family remains a label in(4). Loops have rank zero.

Use the prescribed-edge exchanges associated with ONE such forest. In each
forest tree, parity switches from leaves toward the root can make every
nonroot node's omission count odd. A forest with r edges has r nonroot nodes,
so actual deficiency is at least r.

For a reserved union W of whole auxiliary components, contract W to one root
and remove its reserved whole owner cycles from the families. Root its forest
tree at W. All r nonroot nodes lie outside W. Freeze every unreserved owner's
entire omission choice, including its exact subset F0 on the free vertices
F of W. A local construction with deficiency gamma for every prescribed F0
then gives

    delta(U)>=r+gamma.                                  (5)

No auxiliary edge leaves W. This proves compatibility of actual deficiencies,
rather than adding independent forest maxima or merely compatible parities.
If W is enlarged, construct a fresh forest for that FINAL region and discard
the earlier forest's contribution entirely.

## 3. Square regions and one C8 closure

The full proof of the following local lemma is in
`BALANCED_BOUNDARY_MATCHING_CUT.md`. We recall its mechanism to fix the scope.
For k actual owner squares and4h balanced free vertices, every exact F0 has
an extension with two omissions per actual square and

    nu(A[U_W])<=floor((k+h)/2)+floor(|F0|/2),
    delta_W>=max(0,2k-2floor((k+h)/2))+(|F0|mod2).         (6)

Pair F0 vertices together separately in each physical colour as far as
possible, then pair its complement; each odd side leaves one mixed pair.
These virtual pairs form h temporary squares. The physical matching-cut
lemma gives an independent set Y of size ceil(3(k+h)/2), including any
specified vertex. If a side count is odd, force a leftover F0 vertex into Y.
Completing Y to one endpoint per opposite pair produces Z with
|Z intersect F0|>=ceil(|F0|/2) and matching cost at most floor((k+h)/2).
Replacing its boundary by F0 adds at most floor(|F0|/2), proving(6).
Temporary square edges are never added to A or imposed on final F0.

For four free vertices, the even-boundary guarantee is2floor(k/2), at least
2k/3 for all relevant k>=3. For eight free vertices and k=3 or4 the guarantee
is at least two. Odd boundary cardinality contributes one further unit.

A closed owner instance B=C8 disjoint-union kC4 is also settled for k>=3:
fix any three minimum omissions on C8, and apply(6) with h=2. The cost is at
most floor(k/2)+2. For k=3 this is3=floor(20/6). For k>=4 it is at most
k/2+2<=(2k+4)/3, hence at most floor((4k+8)/6). Smaller such instances in
the unique-C16 domain fall under the at-most-one-auxiliary-square base case.

## 4. Mixed local constructions

### 4.1. C8 plus two squares, four fixed free vertices

Assume all three reserved owner cycles meet at least two auxiliary components
of W. Then every F0 admits minimum reserved omissions with delta_W>=2.

Independently orient the proper two-colouring of each auxiliary component
(the auxiliary bipartition, not physical colour). A reserved cycle is
nonmonochromatic with probability at least1/2: either one component already
contains vertices of both auxiliary sides, or the cycle meets two or more
independently oriented components. Thus some orientation makes at least two
of the three cycles nonmonochromatic. On each of two such cycles choose an
owner edge with opposite auxiliary sides and use its two omission exchanges.
The choices are independent because their owner cycles are disjoint. Their
extreme left-side omission counts differ by two, so their side imbalances
differ by four. At least one has absolute imbalance at least two. Every
auxiliary matching pairs opposite sides, so its deficiency is at least this
imbalance. The third owner choice and F0 stay fixed. This pays the reserved
deficit1/3+2(2/3)=5/3.

### 4.2. C10 plus h squares, two fixed free vertices

The following lemma holds for every h>=0; the global proof needs h=2,3.
Let W consist of one reserved C10, h reserved C4s and two free vertices F,
one of each physical colour. For every prescribed F0, f=|F0|,

    nu(A[U_W])<=floor((h+4+f)/2),   delta_W>=h.           (7)

Put virtual opposite pairs R_op on the h squares only. Components of
P union R_op meeting C10 union F are alternating paths beginning and ending
with P, and hence have odd length. They pair the twelve free endpoints
within each physical colour. A coincident P,R_op edge has no free endpoint
and is a separate two-vertex component.

On one physical colour there are five C10 vertices and one F vertex. The
latter is paired to one C10 vertex; the other four form two contact pairs.
Under owner distance-two adjacency the five vertices form C5. Number them
cyclically0,...,4, with4 the F mate. Up to their three possible contact
pairings, assign bits as follows:

| Contact pairs | Bits at0,1,2,3,4 |
| --- | --- |
| 01,23 | 01011 |
| 02,13 | 01101 |
| 03,12 | 01010 |

Both contact pairs have opposite bits, and exactly one cyclic C5 edge has
equal bits. Give the F vertex its mate's opposite bit. These assignments
extend along the odd P,R_op paths; components without free endpoints can be
coloured independently. Repeat on the other physical colour.

Choose independently one bit in each physical colour, giving four equally
likely selections Uhat. Every actual square contributes two omissions, and
Uhat is P-independent. Hence A[Uhat] is a submatching of Q. Each Q edge is
selected with probability1/4, so

    E nu(A[Uhat])=|W|/8=(h+3)/2.                         (8)

An uncovered C10 owner triple can occur only at an equal-bit edge of one of
the two physical-colour C5s. There are at most two such triples; each is
uncovered with probability1/4. Add their centres, costing at most1/2 in
expected matching number. Initially each physical colour contributes two or
three C10 omissions; repairs add at most one of each colour. The repaired
set therefore has at most four vertices of either colour.

Prune the C10 omissions to an inclusion-minimal triple-hitting set. Its cyclic
gaps g_i satisfy g_i<=3 and g_(i-1)+g_i>=4, the latter by minimality. Thus
20=2sum g_i>=4j, where j is the omission count. Necessarily4<=j<=5. If j=5,
all adjacent sums equal four. Odd cyclic length forces every gap to equal two,
so all five vertices of one physical colour were selected, contradicting the
four-per-colour bound. Pruning therefore leaves exactly four omissions.

Finally impose F0. Its expected number of missing vertices is f/2. Deletion
and pruning cannot increase matching number; each addition costs at most one.
Combining with(8), expected final matching cost is at most(h+4+f)/2.
Some one of the four actual selections has cost at most its floor. Every
result has2h+4+f omissions, proving(7). The two global reserved deficits are
2 for h=2 and8/3 for h=3, both paid by delta_W>=h.

### 4.3. A contained exceptional cycle, fixed outside

Fix all regional omissions outside one exceptional owner cycle C, including
other reserved choices. Some minimum choice on C gives deficiency at least
one, and at least two if regional cardinality is even.

Odd cardinality is immediate. For even cardinality suppose all minimum C
choices were perfectly matched. For each owner edge xy, take the two
exchanged choices. Their perfect-matchings' symmetric difference contains
an even alternating path from x to y. Thus x and y lie on the same side of
one bipartite component of A[(fixed omissions) union C]. Following the owner
cycle places every vertex of C on that same side of one component K.
A perfect matching after retaining ceil(|C|/3) C vertices requires K's
original sides to differ by |C|-ceil(|C|/3)>=2. But K is a path or an even
cycle, with side imbalance at most one. Contradiction. For several anchors
we apply this argument once, fixing the others; their separate savings are
not added.

## 5. Capacity, full representatives and closures

Decompose A union B into connected components. Components without the C16 L
use the all-auxiliary-square theorem. In the component with L, first remove
the stated base cases and the one-C8-plus-squares closures from Section3.
Now assume that parent is connected and not one of those cases.

Contract a reserved W containing L. Every other auxiliary node has capacity
four. In a connected projected subfamily avoiding the root, with v nodes
and c owner-cycle labels, capacity gives v>=c. Equality forces all c cycles
to be squares filling all nodes, making a closed A union B component away
from L. Connectedness excludes this. Hence its rank v-1 is at least c.

For a root-containing support, let p be the free capacity, q its outside
auxiliary-square nodes, and write total exceptional lengths as4x+8y+6a,
where x counts4 mod6 owners, y counts2 mod6 owners and a>=0. Then

    4x+8y+6a<=4q+p,
    lambda=(2x+y)/3-q,
    3lambda<=p/2-q-3y-3a.                               (9)

If capacity is saturated, restoring reserved cycles gives a region closed
under both A and B, so connectedness makes it the entire parent. This also
excludes nonexceptional owners crossing a saturated region.

For p=2, more labels than root rank would require at least4(q+1)>4q+2
indices. Thus full independent representatives exist. For p=4, failure of
full representatives forces saturation by remaining owner squares. The
reserved owners here are all squares or one C8 with squares, so the closure
has already been handled. Again full representatives exist. The exterior
forest therefore has size ell, at least its total deficit d_out.

For p=8 with k=3 or4 square anchors, failure of full representatives gives
x+y>=q+1. Combined with capacity this forces a=0 and exactly one of:

- y=0,x=q+1: absorb these whole squares and their touched auxiliary nodes.
  The enlarged region has four free vertices and is handled by the preceding
  p=4 case. Its forest is constructed anew for that final region.
- y=0,x=q+2: a saturated all-square closure.
- y=1,x=q: a saturated one-C8-plus-squares closure.

Otherwise the exterior forest has size ell. For k=3, its two regional units
pay the reserved deficit2. For k=4, another exceptional cycle must remain,
or the parent would be in the owner-C4/6k base case. Consequently
ell-d_out>=1/3, and

    ell+2>=d_out+7/3=d-1/3.                              (10)

This is a single exterior contribution, not separately allocated to anchors.

## 6. No exceptional owner contained in L

Start with W=L, no reserved owners, and p=16. If every subfamily has weighted
rank loss at most1/3, Rado(4) gives r>=d-1/3 and settles(3). Otherwise a
root-containing support has

    4x+8y+6a<=4q+16,    2x+y>=3q+2,    q>=1.            (11)

The last inequality follows because no exceptional cycle lies inside L;
a whole cycle in one outside square would close it. Equations(9),(11) imply

    x+5y+(9/2)a<=10,   q+3y+3a<=6,   y+a<=1.

These are all-size integer bounds. Their eighteen solutions consist of nine
saturated closures, and exactly these nonclosed types:

| Reserved owners | q | Free vertices | Local guarantee |
| --- | ---: | ---: | ---: |
| 3C4 | 1 | 8 | 2 |
| 4C4 | 2 | 8 | 2, with exterior surplus(10) |
| kC4, k=4,5,6,7 | k-3 | 4 | 2floor(k/2) |
| C8+2C4 | 1 | 4 | 2 |
| C10+2C4 | 1 | 2 | 2 |
| C10+3C4 | 2 | 2 | 3 |

To verify exhaustion without finite graph enumeration: y=a=0 gives
ceil((3q+2)/2)<=x<=q+4,q<=6. Its nonsaturated solutions are the six pure-square
rows. For y=1,a=0, ceil((3q+1)/2)<=x<=q+2,q<=3 leaves only q=1,x=2 nonsaturated.
For y=0,a=1, ceil((3q+2)/2)<=x<=q+2,q<=3 gives(q,x)=(1,3),(2,4); the added six
length units make exactly one C10. Cases y+a>=2 are impossible. The remaining
nine solutions are saturated all-square or one-C8-plus-squares closures.

The pure-square types follow Section5. The C10 rows use(7) and p=2 full
representatives. In the mixed C8 row all three cycles cross auxiliary
components: none is contained in L, and a C4 in one outside square would
close it. Therefore Section4.1 applies, with p=4 exterior representatives.
All reserved deficits are paid, proving(3) in every row.

## 7. Every contained exceptional collection

Reserve ALL exceptional owner cycles wholly in L, denoting the collection I.
If they fill L, that closed parent is a base case. Otherwise the possibilities
and sufficient budgets are:

| I | p | Reserved deficit | Local gamma | Exterior loss epsilon |
| --- | ---: | ---: | ---: | ---: |
| C4 | 12 | 2/3 | 1 | 2/3 |
| 2C4 | 8 | 4/3 | 1 | 0 |
| 3C4 | 4 | 2 | 2 | 0 |
| C8 | 8 | 1/3 | 1 | 2/3 |
| C8+C4 | 4 | 1 | 1 | 0 |
| C10 | 6 | 2/3 | 1 | 1/3 |
| C10+C4 | 2 | 4/3 | 1 | 0 |
| C14 | 2 | 1/3 | 1 | 0 |

Because I contains every exceptional cycle inside L, remaining root supports
have q>=1. All one-unit entries use Section4.3 once, with other anchors
fixed. The three-square entry uses(6).

For I=C4,p=12, loss greater than2/3 in(9) forces y=a=0 and
(q,x)=(1,3),(1,4),(2,5),(3,6). The last three saturate and close all-square
parents. In the first, absorb the three additional squares, giving four
reserved squares and four free vertices; its local guarantee four pays
its deficit8/3 and p=4 supplies the exterior.

For I=2C4,p=8, positive loss gives y=a=0 and
(q,x)=(1,2),(1,3),(2,4),(3,5). Again the last three are saturated; the first
absorbs two more squares into the same four-square/four-boundary case.

For I=C8,p=8, loss greater than2/3 allows only(q,x,y,a)=(1,3,0,0), the closed
C8+3C4 case handled in Section3. At capacity four, failure of full
representatives gives the already handled closures. For I=C10,p=6, loss
greater than1/3 forces q=1,y=a=0; capacity gives x<=2 while the loss requires
x>=3, a contradiction. At capacity two, rank loss is nonpositive.

Following the proof route that eliminates every offending support by these
absorptions or closures, every subfamily has rank at least its deficit minus
the tabulated epsilon. By(4), r>=d_out-epsilon. The implemented constructor
can stop earlier when its total maximum forest already meets this threshold;
that early return does not assert the stronger separate subfamily bounds.
For its exact certificate the condition checked independently for every J is
ell-|J|+rho(E_J)>=d_out-epsilon, with rho(E_J)>=|J| retained on branches
promising full representatives. Every row
satisfies gamma-epsilon>=d_I-1/3. Equation(5) proves(3). Exact memberships of
unreserved cycles crossing the free indices have stayed fixed throughout.

## 8. Actual constructor, rounding and verification

The constructor obtains a Rado minimizer from the common forest's verified
dual cut. If C_reach are its reachable cycle labels, take J to be all
remaining labels minus C_reach, including empty families. All edges of J
are in the unreachable graphic part, so its rank is at most that part's
rank. The dual equality and Rado's lower bound force

    ell-|J|+rho(E_J)=r.

All nonroot supports have rank at least their number of labels, as proved
above. Thus a serious weighted loss or failure of full representatives has
a root-containing witness. The constructor extracts that whole support,
reserves its cycles, and uses precisely the local branch described above.
It never enumerates complete owner omission assignments. Earlier forests
serve only to find a final region, and contribute no final credits.

For the newly constructed nonbase cases minimum omission counts and(3) give

    2nu(A[U])=M-delta<=N/3+1/3,
    nu(A[U])<=floor((N+1)/6)=floor(N/6),

where the last equality uses that N is even. Sum component costs; the sum
of their floors is at most floor(N/6). The base cases already have their
own target cost certificates and need not meet the new minimum-count rule.
For the final physical set, select all helpers, owners outside U, and an
independent witness set of size |U|-nu(A[U]). Every helper has at most one
selected witness, every selected witness's owner is omitted, and Q has no
selected witness edge. Owners induce only edges and isolates. Its actual
cardinality is3b-nu(A[U])>=ceil(8b/3), proving the theorem.

Reproduce with assertions enabled:

    python3 -B scripts/check_balanced_boundary_matching_cut.py
    python3 -B scripts/check_unique_c16_compensation.py

The new regional C10 algorithm evaluates only four bit-phase selections,
repairs at most two triples and prunes to four omissions. The C8 routine
checks auxiliary-side orientations in its twenty-vertex region. Whole input
runtime also includes the inherited at-most-one-square colouring search;
no polynomial bound for that inherited feasibility search is asserted.

The checkers separately reconstruct the original5b-vertex physical graph,
check maximum matching by equal matching/cover and literal controls, count
actual induced deficiencies, verify small-subfamily Rado ranks and the new
dual witnesses, and check local fixed-boundary constructions independently.
The eighteen integer types are an exact arithmetic exhaustion justified by
the preceding bounds. Frozen branch models were discovered before the
checker. Some absorption proof alternatives can be preempted in full inputs
by a stronger base case or the ordinary forest; reports do not claim complete
execution coverage of all such alternatives. Finite computations test the
implementation, while the arguments above prove all orders. Independent
exact-source execution and scope are recorded in the review receipt when
available. No new Lean execution, priority claim, unrestricted SF-gap theorem,
or physical grid theorem is inferred. The October submitted manuscript is
not modified.
