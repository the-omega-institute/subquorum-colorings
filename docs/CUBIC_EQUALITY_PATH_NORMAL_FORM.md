# Cubic equality candidates: paths, distinct witnesses and component debt

19 October 2026. All graphs here are finite, simple, cubic and bipartite.
Two-star formation is non-induced, and minimal means inclusion-minimal.
The results concern a fixed minimal forming selection S, not necessarily
one whose size already equals SF_2. They extend the
[regular remainder](REGULAR_COMPENSATION_EQUALITY.md) beyond its
[isolate-tight stratum](CUBIC_ISOLATE_TIGHT_STRUCTURE.md).

## The accounting condition

Put n=|V|, s=|S| and beta=beta_2(G). Let I be the selected isolates,
P the selected matching vertices, U the selected leaves with a high
support, and H the selected vertices of selected degree at least two.
Write a(v)=|N(v) intersect S|. Choose the injective high deletion-failure
map f from the [sharp exchange proof](SHARP_CUBIC_BIPARTITE_GAP.md).
An owner is good when f(v) is nonadjacent to v. Its witness has selected
degree one, through a selected leaf supported by v. Reserve that leaf.
Different good owners have different reserved leaves.

Let K=|U|-number of good owners, and let r_j count outside vertices of
selected degree j not used by f. For v in H put

    q_v=3-a(f(v))-(a(v)-1)>=0,
    A=sum_H q_v+r_1+(r_1+r_2-K),
    W=3n+2beta-7s.

The established leaf-witness injection gives K<=r_1+r_2. The exact
cubic remainder is

    W=(beta-|D_L|)+(beta-|D_R|)+A.                         (1)

All three terms are nonnegative. In particular, equality W=0 forces
A=0 and both corrected exchanges to be maximum. Call A=0 **zero
accounting remainder**. This condition by itself does not assert W=0.
It is equivalent to q_v=0 for every high owner, r_1=0 and r_2=K.

## Complete normal form for zero accounting remainder

Theorem. Zero accounting remainder holds if and only if G,S admit the
following partition with the displayed witness choices. Classes may be empty.

- S=I union P union H2 union H3 union U0 union Ue. Here I consists of
  isolates, P induces a matching, H2,H3 have selected degrees two,three,
  and U0,Ue are leaves with a unique high support.
- Outside vertices split into X1,X2b,X2e,Y of selected degrees one,two,
  two,three. There are bijections H3<->U0<->X1 along paths h--u--x.
  The chosen witness of h in H3 is its X1 partner, and u is its reserved leaf.
- There is a bijection H2<->X2b along edges. Each X2b vertex has just
  its H2 owner and one I vertex as selected neighbors.
- There is a bijection Ue<->X2e along edges. Each X2e vertex has just
  its Ue partner and one I vertex as selected neighbors.
- Every U0 or Ue vertex has its remaining neighbor in Y. Each P vertex
  has its mate and two Y neighbors. All remaining I edges go to Y.
  Every Y vertex has all three neighbors in I union P union U0 union Ue.
- Every H2 vertex has exactly one outside neighbor, in X2b. Every H3
  vertex has no outside neighbors. In G[H], each vertex has degree two
  minus its number of attached Ue leaves.
- G[X1 union X2b union X2e] has degree two at X1 and degree one at
  X2b union X2e. It consists of cycles in X1 and paths with distinct
  endpoints in X2b union X2e. Direct edges between two endpoints are
  allowed. Vertices Y have no outside edges.

Proof of necessity. Vanishing q excludes adjacent degree-one high
witnesses. An adjacent degree-two witness forces selected degree two
at its owner; its other selected neighbor is an isolate. A nonadjacent
degree-one witness forces selected degree three at its good owner.
This identifies H2,H3,X2b,X1 and the reserved leaves U0. Every other
selected leaf is in Ue, so |Ue|=K.

Each leaf has an adjacent deletion-failure witness of selected degree
one or two, distinct from the witnesses of other leaves. If such a
witness is also f(h), the overlap lemma forces h to be that leaf's
unique high support and to be good. Its sole selected neighbor is then
the reserved leaf of h. Thus no Ue witness can lie in f(H). This is
the point that excludes reuse of a high witness as an extra-leaf budget.

There are no unused degree-one vertices, since r_1=0. Hence the K
distinct extra leaves inject into the r_2=K unused degree-two vertices.
The injection is a bijection; these vertices are X2e. Each has the
associated extra leaf and an isolate as its selected neighbors. Every
remaining outside vertex has selected degree three and lies in Y.
The identified selected neighborhoods now force each leaf's third edge
to Y: all X1 and X2 vertices have already used their specified selected
incidences. They likewise force the P and I statements. Cubicity gives
the outside degrees and the selected high degrees. This proves necessity.

Proof of sufficiency. X1 is covered through its U0--H3 path; X2b and
X2e have two selected neighbors, and Y has three. Deleting an I or P
vertex uncovers that vertex. Deleting an H2 vertex uncovers its X2b
partner, left with only an isolated selected neighbor. Deleting H3 or
its reserved U0 leaf uncovers its X1 partner. Deleting a Ue leaf
uncovers its X2e partner, again left with only an isolate. Thus every
single deletion fails. Formation is monotone under enlarging the
selection, so S is inclusion-minimal. The specified high witnesses
are injective, their q values vanish, and the unused degree-two vertices
are precisely X2e. Thus r_1=0,r_2=|Ue|=K, proving sufficiency.

## Every high path costs two distinct witnesses

Let c be the number of path components of G[H], counting an isolated
high vertex as one path, and put t=|Ue|. The high degrees are at most
two. A cycle uses no extra leaves, a nontrivial path uses one at each
endpoint, and an isolated high vertex uses two. Therefore

    t=K=r_2=2c.                                           (2)

This is a componentwise count of actual distinct leaves and distinct
outside witnesses. In particular a single unused witness cannot pay
both endpoints of a path, or endpoints of two different paths.

Put b=|H2|, h=|H3|, p=|P|, z=|I| and y=|Y|. Counting Y incidences gives

    3y=h+2p+3z-b,
    s=z+p+b+2h+t,
    n=z+p+2b+3h+2t+y,
    3n-5s=z+t=z+2c,       b+t<=3z.                        (3)

The last inequality counts the b+t distinct X2 incidences at isolates,
retaining the actual degree-three capacity of each isolate. It does
not treat an isolate as a witness that can be spent without multiplicity.

## Quantized bipartition balance

Use subscripts L,R for high class counts. Define t_L,t_R by the color
of the **high support** of an extra leaf, rather than the leaf's color.
Thus t_L+t_R=2c. Write Delta b=b_L-b_R, and similarly Delta h,Delta t.
Counting the edges of G[H] from its two parts gives

    2(Delta b+Delta h)=Delta t.

The outside degree sums give

    2Delta h-Delta b+Delta t=0,

since X1 has the color of its H3 owner, X2b the opposite color to its
H2 owner, and X2e the color of the high support of its leaf. Consequently

    Delta b=-4Delta h,       Delta t=-6Delta h.             (4)

If c<=2, then |Delta t|<=2c<=4, so both high classes and the support
colors of the extra leaves are balanced. In particular, if there is
exactly one high path, its two endpoints have opposite colors. An
isolated high vertex cannot be the only high path.

## Exact exchange debt and cross-component compensation

Let z_L,z_R count selected isolates. The corrected exchange D_L keeps
H in L, I in R, all P and leaves, and f(H) in R; at kept highs it
retains the reserved leaf and removes all extra leaves. Reverse colors
for D_R. Their sizes are

    |D_L|=s-z_L-t_L+Delta b,
    |D_R|=s-z_R-t_R-Delta b,
    |D_L|+|D_R|=2s-z-t,
    |D_L|-|D_R|=-(Delta z+2Delta h).                        (5)

For example, the first identity counts p+h+t-t_L leaves/matching
vertices, z_R isolates, b_L+h_L high vertices and b_L+h_R witness
vertices. The final identity uses the high-edge balance above.

Set M=max(|D_L|,|D_R|). Equations (1) and (5) give the exact identity

    W=|Delta z+2Delta h|+2(beta-M).                         (6)

This generalizes the isolate-tight identity, which has c=0 and Delta h=0.
It separates unavoidable color debt from a possible dissociation gain
beyond the two exchanges. In particular,

    W>=|Delta z+2Delta h|.

There is a stronger componentwise statement. Restrict the selection,
witness map and reserved leaves to each connected graph component Q.
The selection remains minimal there. The nonnegative accounting terms
add to zero, so each component has zero accounting remainder. Dissociation
number, n and s are additive across components. Applying (6) separately gives

    W=sum_Q (|Delta z_Q+2Delta h_Q|+2(beta_Q-M_Q))
     >=sum_Q |Delta z_Q+2Delta h_Q|.                       (7)

Thus opposite debts in different graph components cannot cancel and
their exchange surpluses are not reused. The components in (7) are
components of G, not just paths or cycles of G[H]; interactions within
a connected G remain part of the unresolved maximum-exchange problem.

The subsequent [augmented exchange proof](AUGMENTED_ISOLATE_COMPENSATION.md)
adds the witness of every extra leaf to the exchange retaining that
leaf as an isolated vertex. Additions on either side form disjoint
pairs. This restores all t=2c lost vertices, yielding the stronger
general path penalty W>=2c. With the same notation, if Mplus is the
larger augmented exchange size, its exact refinement is

    W=2c+|Delta z-4Delta h|+2(beta-Mplus)
     >=2c+sum_Q |Delta z_Q-4Delta h_Q|.

The equality in the first line and componentwise inequality in the
second are understood separately: the sum is over graph components
and follows by applying the identity within each component. Thus every
high path forces positive slack; it cannot occur at actual linear equality.

## An explicit obstacle to inferring equality from balanced accounting

Zero accounting remainder and zero color debt do not force the two
exchanges to be maximum. Here is a connected 28-vertex counterexample
to that candidate rule. The right part is

    R={1,3,5,7,8,10,13,15,16,18,21,23,25,26}.

The left part consists of the row labels in this complete neighborhood table.

| Left vertex | Its three neighbors in R |
|---|---|
| 0 | 1,8,10 |
| 2 | 1,3,13 |
| 4 | 3,5,16 |
| 6 | 5,7,18 |
| 9 | 8,16,21 |
| 11 | 10,13,25 |
| 12 | 1,15,25 |
| 14 | 3,15,26 |
| 17 | 5,15,25 |
| 19 | 18,21,23 |
| 20 | 7,21,26 |
| 22 | 7,23,26 |
| 24 | 13,16,23 |
| 27 | 8,10,18 |

Every right vertex also has degree three. Take

    S={0,1,2,3,4,5,6,7,8,10,14,18,20,22,24,25}.

Its high graph is the path 0--1--2--3--4--5--6--7. The normal form is

    H2={1,2,4,5}, H3={0,3,6,7}, I={24,25}, P=empty,
    U0={10,14,18,20}, Ue={8,22},
    X1={11,15,19,21}, X2b={12,13,16,17}, X2e={9,23},
    Y={26,27}.

The reserved paths are 0--10--11,3--14--15,6--18--19,7--20--21.
The H2 partners are 1--12,2--13,4--16,5--17, and the extra-leaf
partners are 8--9,22--23. These lists and the table verify every
normal-form condition and hence minimality directly. Connectedness
also follows directly: the high path reaches all its leaves and all
X1,X2b,X2e vertices through their displayed supports; each isolate and
Y has a neighbor among those already reached.

Here c=1,z=2,s=16,n=28,Delta z=Delta h=0 and both exchanges have size14.
Nevertheless

    D={0,2,4,5,7,9,10,12,13,14,18,21,23,25,26}

is a dissociation set of size15. Its only edges are

    0--10,2--13,4--5,9--21,12--25,14--26;

the other three vertices 7,18,23 are isolated in G[D]. Thus beta>=15,
both exchanges fail to be maximum, and W>=2. This explicit witness
is enough to refute the balanced-accounting rule, without an optimizer
or any exhaustive search. The accompanying exact finite calculation
also returns beta=15, but that upper bound is not used in the refutation.
The target compensation inequality remains valid; the failed step is
the inference that a balanced normal form must attain it.

## What this proves about equality, and what remains open

For a cubic bipartite minimal selection, W=0 holds exactly when it has
the displayed normal form, Delta z+2Delta h=0 and both exchanges are
maximum dissociation sets. Componentwise balance is forced as well.
The maximum condition is essential; a normal form with balanced color
debt need not attain the parameter inequality.

Equations (2)--(3) and the linear equality would imply

    s-beta=z/2+c.                                         (8)

The augmented exchange now proves that c=0 is necessary, so (8) reduces
to s-beta=z/2 and z is even. The high graph consists of even cycles,
both high classes are balanced and selected isolates are balanced in
each connected graph component. The precise equality criterion is
therefore the previously characterized isolate-tight partition with
balanced isolates and maximum exchanges, now valid in the cubic case too.

The original [Oracle question](reviews/2026-10-19-cubic-equality-path-question.md)
asked exactly whether W=0 forces c=0. Its
[completed response](reviews/2026-10-19-cubic-equality-path-response.txt)
provided the compatible augmentation and W>=2c. That graph proof has
been independently checked; the arbitrary-bipartite extension and
refined component debt are separate subsequent local deductions.
Classifying every graph whose remaining cycle exchanges are maximum
and determining the connected cubic asymptotic optimum remain open.

These results reduce an equality-class problem; they do not improve
the general cubic coefficient, settle the connected optimum, or improve
the rectangular-grid five-sixths bound.

## Verification scope

The normal form, path decomposition, finite cardinal counts and
component sum above are general written proofs. The new
[Lean source](../formal/StarForming/CubicPathAccounting.lean) proves two
general graph lemmas, for overlap exclusion and simultaneous isolated-pair
augmentation, and ten conditional arithmetic lemmas for the displayed
counts, debt, isolate compensation and path penalty. It does not
formalize the complete graph partition or claim that arithmetic
hypotheses imply that partition.

The [formal receipt](../output/cubic-path-accounting-formal-check.json)
records twelve passing declarations, with only standard axioms, compiled
sequentially on the authorized local machine after process/memory preflight.
Independent literal-star, distinct-witness, exchange and exact-beta controls
are recorded in [the finite report](../output/cubic-path-accounting-controls.json).
Run `python3 scripts/check_cubic_path_accounting.py --output output/cubic-path-accounting-controls.json`.
It checks 340 new instances and seven established controls, 347 minimal
selections, 694 original and 694 augmented exchanges in total. The 300 connected one-path
instances have n=28,s=16,exchange sizes14, with beta15 in68cases and
beta16 in232cases. Forty further instances have two isolated high
vertices, testing the two-endpoint cost of an isolated high as well.
No sampled path instance attains W=0. This is a new reproducible sample,
separate from the earlier inline discovery mentioned in the Oracle input.
Enumeration tests examples and originally motivated the path question;
it is not a premise of its now completed general proof.
