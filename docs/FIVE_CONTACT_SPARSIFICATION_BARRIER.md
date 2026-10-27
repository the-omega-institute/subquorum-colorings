# Five indispensable contacts and an unbounded sparsification gap

There is NO constant-factor guarantee for replacing a successful contact
subset by at most FOUR contacts, even between just ONE original TT path
and ONE original HH path on a feasible rectangular grid, at fixed actual
M and with five prescribed, pairwise vertex-disjoint squares. This is a
failure of this sparsification rule and of unrestricted use of the
[one/two-contact class optimizer](DOUBLE_CONTACT_OPTIMAL_COVER.md). It is
not a counterexample to that optimizer's stated class theorem or to a
numerical sub-quorum inequality.

An Oracle consultation supplied an explicit board with costs 263 versus
151. The two-parameter construction below extends that board and proves
an unbounded multiplicative gap. All coordinates and costs are derived
here; the checker reconstructs actual M/N and every subset physically.

## 1. Domino coordinates and full auxiliary matching

Let L>=4 be EVEN and d>=1. Physical vertices have coordinates (x,y) with

    -6<=x<=4d+43,  -4<=y<=L+5.

The rectangle has height L+10 and width 4d+50. Its auxiliary N consists
of horizontal domino edges D(i,j)={(2i,j),(2i+1,j)} for all
-3<=i<=2d+21 and -4<=j<=L+5. This covers the entire board exactly once.
Black means x+y even. A domino-coordinate path traverses each D(i,j)
from its black vertex to its white vertex, then takes an M edge from
that white vertex to the next domino's black vertex. Permitted steps are

* east by one domino on an even row;
* west by one domino on an odd row;
* up or down by one domino on any row.

Each such step is one physical unit M edge. A simple domino path has
disjoint black incoming/white outgoing M incidences; two disjoint such
paths therefore define an actual partial matching. A path with k steps
has k M edges and N,M,...,M,N edge sequence. Unvisited dominoes are
N-only components.

Set c3=d+9, c4=d+13, c5=2d+14. Arrows below include every unit step.

## 2. Explicit two original paths

Path A starts (0,0)->(c4,0)->(c4,2). On rows j=2,...,L-1 it traverses
between columns c4 and c4+d: east on even j, west on odd j, moving up
one step after every row. Since L is even, it arrives at (c4,L).
Finish (c4,L)->(c5,L)->(c5,0)->(c5+4,0).

Path B starts (c3+1,1)->(c3,1)->(c3,3). On rows j=3,...,L it traverses
between columns 9 and c3: west on odd j, east on even j, moving up after
every row. It arrives at (c3,L+1). Continue through

    (8,L+1)->(8,1)->(7,1)->(7,L+4)
    ->(2d+20,L+4)->(2d+20,-3)->(c5+1,-3)
    ->(c5+1,-1)->(c4,-1)->(c4,-3)
    ->(-2,-3)->(-2,2)->(4,2)->(4,1).

All horizontal moves have the allowed parity direction. A's serpentine
rectangle is columns d+13,...,2d+13, rows 2,...,L-1, with its top row L
and separate return column c5. B's serpentine rectangle is columns
9,...,d+9, rows 3,...,L, with top row L+1 and return column 8. These
rectangles and returns are disjoint. B's next ascending column is 7;
its top connector at L+4 is above A; its right return 2d+20 is beyond
A's end column 2d+18. Its negative-row connectors are below A. Its
final column -2 and row-2 segment through columns -2,...,4 are left of
both serpentine rectangles. The successive segments meet only at their
listed consecutive endpoints. This proves simplicity and disjointness
for EVERY allowed L,d, not just checked instances.

Let M be exactly the connecting edges on A and B. Select the physical
endpoints of A:

    T={(0,0),(4d+37,0)}.

Both are outside P=V(M). The first sees only (1,0) in P union T; its
other neighbours (-1,0),(0,-1),(0,1) are unvisited holes. The second sees
only (4d+36,0); its other neighbours (4d+38,0),(4d+37,-1),(4d+37,1) are
also holes by the coordinate separations above. Hence the actual
configuration is feasible. The endpoints of B are physical (2d+21,1)
and (8,1), both holes. Thus the original paths are TT and HH. Every
other original component is an untouched N-only HH path.

## 3. Five prescribed squares and fragment weights

The five old domino pairs are

| Contact | Domino on A | Domino on B |
| --- | --- | --- |
| 1 | D(4,0) | D(4,1) |
| 2 | D(8,0) | D(8,1) |
| 3 | D(c3,0) | D(c3,1) |
| 4 | D(c4,0) | D(c4,-1) |
| 5 | D(c5,0) | D(c5,-1) |

Each is an actual unit square with opposite N edges. Distinct horizontal
domino columns ensure all five supports are vertex-disjoint. In the
canonical black-to-white orientations the orders are

    A: 1,2,3,4,5;   B: 3,2,5,4,1.                  (1)

Name A's four successive inner M-gap weights x,y,z,w and B's u,v,t,s.
Counting unit domino steps gives

    x=4, y=d+1, z=4,
    w=u=(L-1)d+2L+1,
    v=2L+2d+32, t=d+1, s=d+29.                     (2)

For w, count initial ascent 2, (L-2) horizontal rows of length d,
L-2 intervening upward steps, top segment d+1, and descent L. Their
sum is (L-1)d+2L+1. B's first serpentine has the same step count.
For v count 1+(L+3)+(2d+13)+(L+7)+5+2+1. For s count
2+(d+15)+5+6+1. The remaining gaps are straight. Exterior tail weights
are 4,4 on A and 1,0 on B, with sum E=9. Therefore

    |M|=E+x+y+z+w+u+v+t+s
        =(2L+3)d+6L+82.                            (3)

All five flips preserve the auxiliary matching and actual M. Using
the exact continuation permutation, write

    alpha=(a,1A,2A,3A,4A,5A)(b,3B,2B,5B,4B,1B),
    tau=(1A 1B)...(5A 5B).

Direct composition gives

    alpha tau=(a,1A,b,3B,4A,1B,2A,5B)(3A,2B)(5A,4B).

The marker-containing cycle supplies two TH paths. The other cycles
own exactly the disjoint inner fragments A[2,3]+B[3,2] and
A[4,5]+B[5,4], of weights y+u and w+t. Consequently the successful
five-contact payment cost is

    C5=E+x+z+v+s=2L+3d+78.                          (4)

No M edge is credited twice. The two circles consume different fragments
of the same two original components; forbidding all sharing at the
original-component level would discard this legitimate operation.

## 4. Complete comparison with all one/two-contact repairs

Every singleton repairs TT/HH and costs all of |M|. From (1) the reverse
pairs are exactly {1,2},{1,3},{1,4},{1,5},{2,3},{4,5}. The other four
pairs fail to repair. Their cycle credits are respectively

    x+v+t+s,
    x+y+u+v+t+s,
    x+y+z+s,
    x+y+z+w+t+s,
    y+u,
    w+t.

This is a symbolic classification of the fixed five-contact pattern:
the two-contact order theorem proves the list for ALL L,d. Nonnegative
weights show {1,3} dominates {1,2} and {2,3}; {1,5} dominates {1,4}
and {4,5}. The two remaining pair costs are E+z+w and E+u+v. Since
u=w and v>4=z, the first is smaller. Thus the exact optimum using at
most two prescribed contacts is

    C2=(L-1)d+2L+14,
    C2-C5=(L-4)d-64.                                (5)

In fact (5) is the optimum over EVERY proper subset of the five contacts,
not just subsets of size at most two. Here is a structural proof. Temporarily
omit contact 1. The remaining contacts are two serial blocks {2,3} and {4,5},
with the same block order on both strands and reversed order inside each
block. An empty block acts as the identity; any nonempty block exchanges
the two strand destinations. A full block additionally creates its local
cycle of credit y+u or w+t. Thus without 1, success requires exactly one
nonempty block and is already a one/two-contact operation.

Restore contact 1, which occurs before all others on A and after all others
on B. If both blocks are nonempty, their serial composition is the identity;
contact 1 cuts distinct terminal paths, swaps their destinations and creates
no additional cycle. Unless ALL four block contacts are present, at most one
block is full. Its only credit is therefore that of pair {2,3} or {4,5}, or
zero, and a one/two-contact choice has at most the same cost. If only one
block is nonempty, there are at most three contacts including 1. With one
block contact the choice is already a pair. With two, the three contact orders
are completely reversed; the two cycles partition exactly the same inner
M intervals as the outermost pair {1,3} or {1,5}, so that pair has equal cost.
With no block contact the choice is the singleton 1. These cases exhaust all
proper successful subsets, proving domination by a one/two-contact subset
without enumerating grids. Consequently

    min_(successful proper S) cost(S)=C2,
    min_(all successful S) cost(S)=min(C2,C5).          (5a)

Whenever the gap in (5) is positive, ALL FIVE contacts are indispensable
for the optimum: every successful deletion is strictly more expensive.

Take d=L and even L>=12. Equations (4)-(5) become

    C2=L^2+L+14,   C5=5L+78,
    C2-C5=L^2-4L-64>0,
    C2/C5 -> infinity.                              (6)

The last statement follows directly by dividing numerator and denominator
by L. More explicitly, C5<=12L for L>=12. For any integer K>=0 choose
even L=20(K+1)>12K; then C2>=L^2>K*12L>=K*C5. Here the successful-subset optimum C* equals C5 by (5a). This rules out
EVERY fixed approximation factor for the best repair using at most FOUR
prescribed contacts, not only two. The conclusion is proved for every
even L>=12; it is not inferred from enumeration of larger grids.

For L=20,d=11 the board is 30-by-94, |M|=675 and C2=263,C5=151.
To make every chosen contact strictly internal, append (4,1)->(2,1)
to B. This path stays simple/disjoint and preserves the displayed T
feasibility. It adds two M edges to the exterior tail, increasing BOTH
costs by two and leaving their difference unchanged. With d=L the
ratio still diverges. Thus the phenomenon does not depend on terminal
cuts or singleton fragments.

## 5. Exact scope and evidence

All alternative operations in (5) must use this SAME prescribed family.
The assertion does not restrict other squares, another N or unrestricted
payments. In fact each selected endpoint has an adjacent unused hole
outside these paths. The board's actual J=|M|+2 remains below half-area
by 17d+19L+166; no numerical sub-quorum target is refuted.

The disjoint pair optimizer remains correct within its declared class.
This counterfamily proves its extension to arbitrary selected subsets
would be false even with two original components and only five contacts.
A broader optimizer must retain the costs of SEVERAL independently owned
inner fragments of one original path, along with terminal routing.

The checker builds the full physical board, matching edges and selected
sites; directly decomposes M+N' for every one of the 31 nonempty subsets;
checks the best proper-subset costs, two disjoint cycle-resource sets and cycle
normalization; and covers an entirely internal-contact variant. These
are validation controls. The all-size coordinate and cost proof above
establishes (6) independently. The separate Lean file verifies the exact
accounting identities and quantified cost-ratio witness, conditional on
the geometric adapter which remains written.

The [review receipt](../output/five-contact-barrier-review.json) separates the
fixed-board discovery consultation from the independent audit of the full
theorem and from local computational/formal validation.

Independent audit ACCEPT confirms the all-size theorem and a stronger exact
replacement statement in the proper-subset cases: the successful one/two-contact
replacement can be chosen INSIDE the original proper subset and has exactly
the same credited physical M set. The auditor reproduced all 27 boards / 837
subsets with parsed-JSON equality and two L=4,d=1 boundary variants (62 more
subsets). Lean was inspected but not executed in that audit.
