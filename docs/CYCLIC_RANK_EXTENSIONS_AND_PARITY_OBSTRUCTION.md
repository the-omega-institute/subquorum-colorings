# A unique auxiliary eight-cycle, square incidence, and the limit of coarse parity

13 November 2026. Two further sufficient classes satisfy the actual all-helper
bound. A connected physical family proves that even optimizing whole-component
parity over every permitted omission cannot prove the unrestricted target.
The unrestricted mixed cyclic problem remains open.

## 1. Exact objective and one simultaneous exchange forest

Work in the [completed cyclic domain](CYCLIC_AUXILIARY_REDUCTION.md): P and Q
are perfect, A=P union Q consists of cycles C_(4k), and the owner graph B is
a union of even cycles. There are N=2b indices and5b physical vertices.
Physical colours agree on P and differ on Q and B. Define

    tau=min_{Delta(B[V minus U])<=1} nu(A[U]),   beta_I=3b-tau.       (1)

The target is tau<=floor(N/6). No mixed identity beta_I=2b+h is used.

For any U let delta(U)=|U|-2nu(A[U]). Since A[U] has only paths and even
cycles, delta(U) is exactly the number of its odd-order components, including
isolates. This counts induced components INSIDE each original auxiliary
cycle, not merely the parity of the total intersection with that cycle.

Permission on an owner cycle of order n means that each three consecutive
vertices meets U. Its minimum omission size is ceil(n/3): gaps between
successive omissions must be at most three, and that bound is attained.
For exceptional owner cycles C_i, of order not divisible by six, put

    d_i=2/3 for |C_i|=4 mod6;  d_i=1/3 for |C_i|=2 mod6.
    m=sum_C ceil(|C|/3)=N/3+d,  d=sum_i d_i.                 (2)

For EVERY prescribed oriented edge xy of an exceptional owner cycle there
are two minimum omissions differing exactly by x<->y. For C4 choose any
two omissions containing x but not y, then swap. Otherwise choose x with
preceding gap2 and succeeding gap3, all other gaps3 except one additional
gap2 when the order is1 mod3. The swap changes adjacent gaps (2,3) to(3,2),
preserving size and permission. Such gap lists have precisely ceil(n/3) terms
and sum n (the smallest non-C4 lengths are8 and10).

Project each owner crossing edge onto its two distinct auxiliary-component
labels; keep parallel edges. Let E_i be the crossing-edge family of C_i.
The occupied projection of one owner cycle is connected, even if some of its
edges project to loops. An owner cycle inside one auxiliary component has an
occupied isolated node and empty crossing family.

**Forest lemma.** If a forest of r projected edges uses at most one edge from
each exceptional owner cycle, some minimum-cardinality permitted U satisfies

    nu(A[U])<=floor((m-r)/2).                               (3)

Use the two omission choices on each chosen owner cycle and fix minimum
omissions on all others. The binary choices are independent across owner
components. Switching an edge toggles omission parity at its two projected
endpoints. On a tree these toggles realize every vector with the original
total parity, by solving at leaves. Make every node except possibly the root
odd. Thus at least r original auxiliary intersections are odd, each giving
at least one odd induced component. Equivalently,

    nu(A[U])<=sum_K floor(|U intersect K|/2)<=(m-r)/2.

This is one common forest, not separate savings assigned to overlapping
supports. One may specify any root; in particular, all r odd intersections
can be outside a distinguished root component.

We use the graphic independent-representative formula already proved in the
[square-forest manuscript](../manuscript/auxiliary-square-forest-proof.tex):

    r_max=min_{J subset [h]} (h-|J|+rank(E_J)).              (4)

This is the graphic form of Rado's independent-representative theorem. If
rank(E_J)>=sum_(i in J)d_i-epsilon for every J, then (4) gives r_max>=d-epsilon,
because each unselected family's unit contribution is at least its d_i.
The inherited manuscript includes a self-contained proof and its Rado42
bibliographic entry; no new literature-priority claim is made here.

For a connected occupied projection using v auxiliary squares, with x owner
cycles of order4 mod6 and y of order2 mod6, disjointness gives

    4v>=4x+8y,  v>=x+2y,  rank=v-1.                       (5)

If x+5y>=3, this pays rank>=(2x+y)/3. The only exceptions are one ownerC4
filling one auxiliary square, or two ownerC4s filling two auxiliary squares.
They are closed components of A union B: all vertices of those auxiliary
components are occupied by complete owner cycles. These closed components
already satisfy the all-square theorem. All uses below either remove them
or work in a connected mixed component where they cannot occur.

## 2. Theorem A: arbitrary squares and at most one C8

**Theorem A.** If A consists of any number of C4s and at most one C8, then
tau<=floor(N/6), for arbitrary physical owner even cycles.

Decompose over connected components of A union B. Permission and matching
cost are independent between components; their costs add and the sum of
their individual floor bounds is at most the global floor bound. Components
containing only squares are already solved. For the component containing
the C8, denoted L, the no-auxiliary-square theorem handles absence of squares,
and the owner-C4/6k theorem handles the case all owners are C4s. Thus assume
that A union B is connected, contains L and at least one square, and not all
owner cycles are C4s. A saturated collection of whole auxiliary components
filled by ownerC4s would then be a forbidden closed proper component.

### Case I: no owner C4 is contained in L

For every exceptional-owner subfamily J we claim

    rank(E_J)>=d_J-1/3.                                   (6)

Each occupied projected component avoiding L has the exact square-capacity
bound (5); its two exceptions would be closed proper components. The unique
occupied projected component containing L, if any, has s square nodes and
exceptional counts x,y. Its rank is s, and

    4s+8>=4x+8y,  s>=x+2y-2.                              (7)

If x+5y>=6 this is at least(2x+y)/3. All other nonempty possibilities are:

| x,y | Required count and reason |
|---|---|
| 1,0 | s>=1, since an ownerC4 entirely in L is excluded |
| 2,0 | s>=1; s=0 fills L with two ownerC4s, a closed component |
| 3,0 | s>=2; s=1 fills L and one square with three ownerC4s |
| 4,0 | s>=3; s=2 fills L and two squares with four ownerC4s |
| 5,0 | s>=3 by capacity, a deficit of1/3 relative to10/3 |
| 0,1 | s>=0, a deficit of at most1/3 |

The saturated rows are impossible under the connectedness assumptions.
Thus only this one projected component can lose1/3, proving (6). Formula(4)
supplies r>=d-1/3. By (2)-(3),

    nu(A[U])<=floor(N/6+1/6)=floor(N/6).                    (8)

The last equality holds for every even N (in this domain N is divisible by
four). Its residue modulo six is0,2 or4, so adding1/6 cannot cross an integer.

### Case II: an owner C4 lies entirely in L

Reserve one such owner cycle C_* and do not use it in the exchange forest.
For the remaining exceptional cycles d'=d-2/3. Four vertices of L are no
longer available to those cycles. Hence a projected component containing L
now has

    4s+4>=4x+8y,  s>=x+2y-1.                              (9)

This pays its full deficit when x+5y>=3. The only two possible failures are
one further ownerC4 filling the rest of L, or two further ownerC4s filling
the rest of L and one square. Together with C_* these are closed all-owner-C4
components, excluded above. Components avoiding L obey(5). Therefore every
unreserved subfamily has rank at least its deficit. Formula(4) gives r>=d'.

Root the forest at L in its tree. Its switches make at least r auxiliary
components OUTSIDE L odd. The omitted pair on C_* can be chosen last: it
changes no outside choice and no parity of |U intersect L|.

We need the following fixed-outside lemma. Let X be any fixed subset of
L minus C_*. Some choice of two omitted vertices of C_* gives matching
deficiency at least one if |X| is odd and at least two if |X| is even. The
odd case follows from parity. For the even case suppose every two-vertex
choice on C_* gave a perfect matching of A[X union pair]. For any distinct
x,y in C_* choose a third z and compare perfect matchings on X union{x,z}
and X union{y,z}. Their symmetric difference contains an even alternating
path from x to y in A[X union C_*]. Thus all four marked vertices lie on the
same bipartition side of one connected component of this host graph.
Every other vertex in that component is fixed. Deleting two marked vertices
from that side leaves a perfectly matched component, so the full component
would have bipartition imbalance two. A path or even cycle has imbalance at
most one. This contradiction proves the lemma. It is an internal induced
matching argument, independent of the parity of the whole intersection.

Use its choice on C_*. The global deficiency is at least r+1>=d+1/3, since
the r outside contributions and L's contribution are disjoint. Consequently

    nu(A[U])=(m-delta(U))/2<=N/6-1/6,
    nu(A[U])<=floor(N/6-1/6)<=floor(N/6).                   (10)

The final floor uses integrality; the real inequality N/6-1/6<=floor(N/6)
is not assumed. This completes both cases and Theorem A.

The same conclusion holds componentwise if every connected component of
A union B containing squares has at most one long auxiliary cycle and that
cycle is C8, with arbitrary square-free components also allowed.

## 3. Theorem B: a square-incidence condition for arbitrary long cycles

Let S be the union of all auxiliary-square vertices. Suppose every exceptional
owner cycle satisfies

    |C_i intersect S|>=3 if |C_i|=4 mod6,
    |C_i intersect S|>=2 if |C_i|=2 mod6.                   (11)

Then tau<=floor(N/6), with no bound on the number or lengths of long auxiliary
cycles. Multiple exceptional owner cycles may share a long component.

Remove the closed square components from(5). For any remaining subfamily J,
consider a connected occupied projection with s square nodes and ell long
nodes. If ell=0 use(5). If ell>=1, disjointness and(11) give

    4s>=3x+2y,
    rank=s+ell-1>=s>=(3x+2y)/4>=(2x+y)/3.                  (12)

The last inequality is equivalent to x+2y>=0 after multiplication by12.
Sum over components: rank(E_J)>=d_J for EVERY J. Formula(4) gives r>=d;
the forest lemma yields nu(A[U])<=floor((N/3+d-r)/2)<=floor(N/6).
Restore the already solved closed components, adding costs and then floors.

Both theorems return actual physical all-helper sets. For permitted U choose
owners V minus U and a maximum independent witness set in A[U]. Since A[U]
is bipartite, this set has size |U|-nu(A[U]). With all b helpers the size is
3b-nu(A[U])>=ceil(8b/3). Independence on P/Q and owner permission verify
the actual selected degrees, using only original edges.

## 4. Exact unbounded obstruction to whole-component parity

For every integer t>=1 put r=6t, L=8r+8, N=L+8=48t+16, and use indices0..N-1.
Set

    A=C_L(0,...,L-1) union C4(L,...,L+3) union C4(L+4,...,L+7).

On each displayed natural cycle P uses consecutive even-start pairs and Q
the remaining alternating edges. Set physical c(v)=floor(v/2) mod2. P joins
equal colours and Q joins opposite colours, with both matchings perfect.

For0<=i<r put an ownerC8 on indices8i..8i+7, in cyclic order

    8i+(0,2,1,3,4,6,5,7).

Writing a=8r, put one ownerC16 on the remaining sixteen indices in the order
obtained by concatenating (a+4j,a+4j+2,a+4j+1,a+4j+3), j=0,1,2,3.
Every four-entry group has physical colours0,1,0,1; B is physical and
2-regular. The final C16 meets all three auxiliary components, making
A union B and the actual graph connected. Helpers have degree2 and all
owners/witnesses degree3, so this lies in the residual physical cyclic domain.

Define

    U0=union_(i<r)(8i+{0,3,6}) union (a+{0,3,5,10,12,14}).   (13)

On every ownerC8 the omission positions are0,3,5 with gaps3,2,3. On the final
C16 they are0,3,6,9,12,13 with gaps3,3,3,3,1,3. Thus U0 is permitted. It is
independent in A: the first blocks use natural indices0,3,6; the last eight
vertices of L use0,3,5; its last vertex is absent, protecting the closing edge.
The first square has one omission and the second an opposite pair. Therefore

    tau=0,  beta_I=3b,  |U0|=m=3r+6=18t+6.                 (14)

For the three WHOLE auxiliary components K_j, consider the coarser estimate

    q(U)=sum_(j=1)^3 floor(|U intersect K_j|/2),
    nu(A[U])<=q(U).

Every permitted U has |U|>=m and q(U)>=(|U|-3)/2>=(m-3)/2=9t+3/2.
Integrality gives q(U)>=9t+2. The three intersections of U0 have sizes
18t+3,1,2, so equality is attained. Thus the EXACT optimization identities are

    min_permitted q(U)=9t+2,    min_permitted nu(A[U])=0,
    floor(N/6)=8t+2.                                       (15)

Even optimizing this whole-component estimate over EVERY permitted U misses
the target by exactly t, while the true cost is zero. At t=1 there are64
indices/160 actual vertices: the best coarse estimate is11, target10, cost0.

Each initial ownerC8 projects to a single isolated node and has no crossing
edge. The final C16 connects the three nodes but is only one owner family.
The maximum rainbow forest therefore has exactly one edge, yielding
floor((m-1)/2)=9t+2, precisely the optimized coarse estimate. This is not a
target counterexample; it proves an unbounded limitation of the statistic
even without restricting omission size, starting state, or exchange list.

## 5. Verification, provenance and the next obligation

[cyclic_rank_extensions.py](../develop/cyclic_rank_extensions.py) constructs
the two sufficient classes componentwise, with original physical certificates,
forest/dual records, reserved-pair candidates, and the exact obstruction family.
Run `python3 -B scripts/check_cyclic_rank_extensions.py`. Literal checks cover
all order8 physical owner2-regular graphs for two canonical auxiliary types,
every four-marked/fixed-outside subset on C8, prescribed-edge exchanges,
independent subset-rank/Rado comparisons, original physical adjacency and
induced deficiencies, exact small controls and all-scale family coordinates.
Report and independent review are separate evidence. Finite checks validate
implementation; the general arguments establish the theorems.

The original two theorem proposals and obstruction construction came from
the preserved Oracle research answer; this note reconstructs their proofs,
corrects the real-to-integer rounding in CaseII, and supplies constructors
and independent checks before a separate audit. No Lean/kernel or external
priority audit is claimed.

The unrestricted mixed cyclic theorem remains open. A concrete next bounded
case is auxiliary squares plus one C12: capacity there gives
s>=x+2y-3 and pays the full deficit when x+5y>=9. The remaining patterns are
y=0,1<=x<=8, or y=1,0<=x<=3. Any reserved-cycle/internal-deficiency extension
must specify compatible exterior choices and count induced odd components
once, rather than awarding an independent saving to every owner cycle.
Sharp unrestricted graph gaps, general safe composition and physical grid
multiple-Hall/unit5/6/triple-equality objectives remain separate open goals.
