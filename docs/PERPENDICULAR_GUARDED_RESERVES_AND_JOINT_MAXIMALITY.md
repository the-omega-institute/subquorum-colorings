# Perpendicular guarded reserves and joint inclusion maximality

25 October 2026. Haobo Ma and Wenlin Zhang. Independent research branch.

The [adjacent frozen module family](FORCED_MATES_AND_ADJACENT_MAXIMA.md)
has a unique actual matching and a true fixed-P selection maximum, yet its
horizontal whole-pool compensation is zero. We now prove two further facts.

* For EVERY feasible selected set T with this P, the aligned VERTICAL bands
  fully compensate every alpha with zero links. Each alpha has two distinct
  private singleton reserves. This requires neither maximum selection nor
  complete freezing.
* For the displayed maximum T*, no monotone enlargement of T or P is possible,
  even if the matching may be completely changed. Thus those horizontally
  uncompensated examples are inclusion maximal jointly in T and P. Changing
  direction repairs them; monotone growth does not.

Both conclusions hold for all even W>=8 and all q>=1. They concern the stated
endpoint family, not arbitrary grids. Joint inclusion maximality is not a
maximum over replacements that delete old selected points or old endpoints.
The universal5/6 improvement remains open.

## 1. Fixed data and the actual operation

Use exactly the board, P, matching M and maximum T* of the preceding note:
rows0..W+1, columns0..10q+1; module i is translated by10i. Before translation,
P has all rows1..W in columns4,5,6; rows1,W in columns3,9; and rows1,W-1,W
in columns7,8. The actual matching is uniquely forced by its leaf order.
Put n=W/2.

A general T in Sections2–5 is any set disjoint from P such that every selected
vertex has at most one neighbour in T union P. No old T is required to remain.
We now pair COLUMNS(0,1),(2,3),...,(10q,10q+1). The board, T and M do not
move. In code we transpose coordinates only to reuse the horizontal-band
compiler; its resource(band,first,last) then means an original vertical band
and a range of original rows. This is a new band direction, not a claim
that carrying an old band decomposition through a grid isometry fixes it.

## 2. Complete vertical strand classification

In each module the open original strands have these endpoint pairs in
original coordinates:

    L: ((1,3),(W,3));
    R_r: ((r,6),(r+1,6)), r=2,4,...,W-4;
    R_end: ((W-2,6),(W-1,8)).                             (1)

There are n open strands and four pure2-cycles per module. The inventory is
independent of T; only a tip's TP/BP label depends on selection of its vertical-
band partner.

To verify(1), follow L from(1,3) along M to(1,4), the band edge to(1,5),
M to(2,5), the band edge to(2,4), and M to(3,4). Repeating this alternating
pattern visits all endpoints in columns4,5 and ends through(W,4) at(W,3).
Each R_r is just its actual vertical matching edge. The last such edge
continues through the band pair(W-1,6)--(W-1,7), then M to(W-1,8), giving
R_end. The horizontal matching pairs in columns6,7 and8,9 at rows1,W are
four closed2-cycles. These objects are disjoint and cover all3W+10 endpoints.
Translating the argument proves the classification for arbitrary q.

No R_r is an alpha. Its band partners are(r,7),(r+1,7); each would see its
own P neighbour in column6. If both were selected, they would also see one
another, violating feasibility. The last tip(W-1,8) cannot be TP: its band
partner(W-1,9) has two P neighbours,(W-1,8) and(W,9). Thus R_end is not an
alpha either.

Consequently the complete alpha set is

    A={L_i: (1,10i+2) and(W,10i+2) are both in T}.         (2)

In particular |A|<=q. This accounts for every possible alpha, including
those arising after arbitrary changes in T.

## 3. Two forced private original interval units per alpha

Consider L_i in A, initially suppressing the column translation. The upper
selected partner s=(1,2) already sees the endpoint p=(1,3). Its neighbour
(2,2) cannot be selected: otherwise s would have two occupied neighbours.
The other cell(2,3) sees two P neighbours,(1,3),(2,4), so it cannot be
selected either. Neither cell is in the fixed P. Thus the original vertical
column consisting of physical cells{(2,2),(2,3)} is BB.

The same argument at the lower TP tip makes{(W-1,2),(W-1,3)} BB. Their
original interval identifiers in the transposed compiler are

    J_i^+=(5i+1,2,2),    J_i^-=(5i+1,W-1,W-1).           (3)

These are actual singleton units, not merely two BB vertices extracted from
one longer BB/TT component. Indeed, in every interior row2..W-1 of this
vertical band the column3 cell has a P neighbour in column4. A TT pair in
columns2,3 would give that selected cell a second occupied neighbour, so no
TT occurs anywhere in the interior no-P gap. Hence its BB/TT forest has
isolated BB components. The two forced BB columns give distinct units since
W>=8. Its boundary columns at original rows1,W both belong to L_i, so every
unit in this gap is in L_i's complete support.

The support is private, even relative to other original owners. The same
band(2,3) has only these two P tips, both in L_i. Its outer boundary gaps
also touch only L_i. The L_i body occupies band(4,5), whose endpoint columns
run through rows1..W and also belong only to L_i. Its two outer gaps are
therefore private as well. No other band contains L_i. Different translated
modules use disjoint band-index sets{5i+1,5i+2}. Thus the entire supports of
different L_i are disjoint, and no other owner shares a unit with an alpha.

There is no non-self outgoing TP--BP link from L_i: its only TP tips lie at
original rows1,W in column3; their axis neighbours in that band, at rows0,2
and W-1,W+1, contain no endpoint in column3. A route cannot leave an alpha
through another original owner. A direct payment of L_i from either unit
in(3) uses zero links. Choose one unit per alpha; the assignment is injective
because the supports are private. This proves full compensation with zero
links, without any optimization or finite search.

## 4. Exact available-pool formula and a deficit bound with no repeated reserve

Let F be ANY available subset of the original interval pool, and W_i the
complete original support of alpha L_i. All other resources and beta sinks
may remain available. Then the exact whole-support maximum and minimum cost
are

    V(F)=|{L_i in A: W_i intersects F}|,    c(F)=0.         (4)

For the upper bound, a source with empty remaining support has no outgoing
route and cannot pay a beta. For the lower bound, every other source takes
one remaining unit in its private support. These choices never conflict.
No stem through a mixed owner or beta fork can improve this formula because
no alpha has a first outgoing link.

Write d(F)=|A|-V(F), and let G be the union of the2|A| forced units in(3).
Each unpaid source has BOTH its forced units removed. Different sources'
units are distinct, so the direct injection(source,sign) -> J_i^sign gives

    2d(F) <= |G minus F| <= |Q minus F|.                  (5)

Thus removing at most one of the two forced units for each alpha preserves
full compensation, regardless of what happens to the other original units.
This is a cross-component deficit inequality on the entire fixed-P selection
class, with an explicit mechanism preventing repeated reserve use. A BB
inside a balanced boundary TT chain is never counted as a positive unit;
Section3 proves the specified reserves are genuine isolated components.

For T*, exactly q sources are alpha, q strands are beta and q(n-2) are mixed.
The two-reserve construction already gives2q original units. The exact band
ledger S=L+beta-alpha, together with the previous exact S=2q, gives L=2q;
there are no other original units. Consequently(4) simplifies to

    V(F)=q-|{i: neither J_i^+ nor J_i^- is in F}|.         (6)

Deleting r original units can cause at most floor(r/2) unpaid sources, and
this is sharp for each0<=r<=2q by deleting complete pairs first. With the
full pool, the very same T*,P,M have the following contrasting decompositions:

    horizontal: alpha=q, beta=0, raw intervals=3q, V=0;
    vertical:   alpha=q, beta=q, raw intervals=2q, V=q, c=0.

Both have S=2q. The q-unit reduction in raw intervals is exactly offset by
the q beta units. The two decompositions describe the same objective ledger;
their apparent resources may not be added together.

## 5. A reusable guarded-strip lemma

The local argument is not tied to the module's other strands. In any
feasible pair, take a two-cell-wide no-P strip between two P boundary columns
of one source. Suppose the source has TP boundary tips on the same flank,
their selected partners face those tips, and every cell on that flank of
the interior strip has an exterior P neighbour. If the first and last
interior columns have the two-P exclusion on that flank, then each is BB:
its other cell is excluded by the saturated selected boundary partner.
The exterior P guards forbid TT throughout the strip, so these are two
original singleton resources. If the two boundary columns belong to the
same source and no other owner touches the strip, they are private.

For any family of such strips with disjoint original units, the same direct
assignment proves full payment for their sources. Under resource removals,
2 times the number of sources losing all their support is at most the number
of removed guarded units. Distinct source supports suffice for exact(4);
without that hypothesis only the two designated disjoint reserves are
promised. This states the geometry and ownership assumptions explicitly;
no inference from freezing alone to private reserves is made.

## 6. Joint inclusion maximality of the attaining configuration

Now fix T=T*, the maximum construction of the preceding note. Consider
ANY feasible pair(T',M') with

    T* subset T',     P subset P'=V(M').                 (7)

The old matching need not be retained. We prove T'=T*, P'=P and M'=M.
This is monotone maximality, not optimality among arbitrary replacements.

First T'=T*. Removing new endpoints cannot violate feasibility of selected
vertices. Thus(T',M) would be feasible with the original P. The preceding
exact ALL-T fixed-P upper bound equals |T*|, so the inclusion in(7) forces
equality of the finite selected sets.

For a possible new endpoint x, every neighbouring selected point must
currently have NO occupied neighbour: adding x would otherwise exceed its
allowance. Define the necessary endpoint hull

    H={x outside(T* union P): for every t in T* adjacent to x,
                              N(t) intersects(T* union P) is empty}. (8)

Any P' in(7) has P' minus P contained in H. This is only a necessary candidate
hull; its elements are not asserted to be simultaneously insertable.
Substitute the displayed row patterns of T* and the explicit P. The exact
hull rows are as follows; i runs from0 to q-1 unless otherwise stated.

    row4: {10i+9} union {1 if W>=10};
    even rows r=6,8,...,W-4:
          {10i+9,10i+11} union {1 if r<W-4};
    odd rows r=5,7,...,W-3:
          {10,20,...,10q} union {0 if r<=W-7};
    rowW-2: {10i+11};
    rowW-1: {10i+9} union {10i+3:1<=i<q};
    all other rows: empty.                              (9)

Empty row ranges contribute nothing; the first row rule handles W8 and W10
without overlapping another rule. This finite row-type table is valid under
arbitrary repetition of the ordinary interior strip. To check it directly,
use(8): a blank is excluded precisely when it touches a selected vertex
already facing P or its vertical T companion. The ordinary U/D rows give
the alternating odd-colour sites in(9); the top F/D interface forbids all
new endpoints through row3 and removes the 10i+11 choices at row4. Near the
last interior band, the two vertical T pairs in columns0,2 remove the
otherwise possible column0 one row above and column1 in that band. The
switched penultimate selection row leaves only10i+11. In the last row before
P's bottom boundary, two-P-side pockets remain at10i+9, and at10i+3 except
in the first module, where the retained selection(W-2,3) excludes it.
Every remaining listed site's selected neighbours are isolated in T* union P;
every omitted blank has a saturated selected neighbour. These are tests on
the finitely many row/residue types, so establish(9) for all W,q, not by
induction over an enumerated list of boards.

Let E be the last row of(9). Each E vertex has checkerboard colour0:
W-1 and its column are both odd. Every other hull vertex has colour1 and
has no neighbour in P: the residues in(9) lie outside the full P columns
and outside the terminal P caps. There are no edges within H minus E
because those vertices have one colour. There are also no edges from H
minus E to E: the nearest rowW-2 has columns10i+11, differing by two from
the nearest E column; rowW contains no hull vertex, and rowW-1 contains
only E. Thus every vertex of H minus E is isolated in the induced graph
on P union H.

No matching covering P' can contain an isolated candidate. Hence all new
endpoints would lie in E. The original P has equal colour counts, since
its known matching joins opposite colours. Adding ANY nonempty subset of E
makes those counts unequal. Every matching in a bipartite grid covers equal
numbers of the two colours, so such a perfect matching is impossible.
Therefore P'=P; the previous unique-matching theorem gives M'=M. QED.

A general certificate behind this argument is useful beyond the present
family: if a balanced old endpoint set P has a necessary extension hull H,
and all hull vertices of one colour are isolated in P union H, then no
matching-covered endpoint superset of P exists. This uses the same hull for
all simultaneous insertions and all rematchings, not single-edge failure
as a substitute for joint maximality.

## 7. Verification, formalization and consequences

The solver-free geometry checks312 feasible fixed-P selected sets, including
24 attaining boards over W in{8,10,12,20,40,64}, q in{1,2,3,7}; other selected
sets are generated without retaining T0 and half the controls force all
potential left alphas. It checks388 forced reserve pairs and2914 available-
pool comparisons against BOTH the whole-support flow and independent
primitive-certificate packing. For maximum boards with q<=3, it checks every
available subset of their2q intervals. General pool claims are proved in
Sections3–4, not inferred from that census. The controls observe377 balanced
boundary chains, handled with zero credit by the existing even-width compiler.

For the24 maxima it independently recomputes every endpoint hull from(8),
compares the full row table(9), and checks all2705 isolated candidates. For
W8 and q=1,2 an independent bipartite augmenting matcher checks all528 hull
subsets, including the two empty controls; only the empty extension admits a
perfect matching. These checks validate the isolation/balance proof.

The Lean source contains the general saturated-guard and two-P exclusions,
an arbitrary-index injective choice of available reserves, survival after
at most one removal per reserve pair, and opposite-colour matching balance
with the no-single-colour-extension consequence. It also checks the actual
W8/q1 transposed feasible41T geometry, all34 frozen endpoints, the exact
finite endpoint hull and its isolation certificate, and the two physical BB
witnesses. General coordinate/strand classification, whole-resource ownership,
the arbitrary-size hull table, and the flow-to-geometry adapters remain
written proofs with Python checks. This is not end-to-end Lean verification
of the all-grid statement.

Reproduce from the repository root:

    python3 develop/check_perpendicular_guarded_reserves.py --output output/perpendicular-guarded-reserves-validation.json
    python3 develop/check_perpendicular_reserves_formal.py --lean /path/to/lean-4.33.0 --output output/perpendicular-guarded-reserves-formal-validation.json

The family therefore excludes monotone maximality as a universal justification
for horizontal full compensation, even after arbitrary rematching. It is
nevertheless fully repaired by the perpendicular decomposition for every
feasible T with its P. A genuine obstruction to choosing the better of the
two aligned directions would need a different geometry, or an interaction
between perpendicular guarded strips. Replacement exchanges that delete old
T/P and a universal direction-selection theorem remain open. The submitted
11 October manuscript is preserved; no email is sent by this research update.
