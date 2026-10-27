# Closed ladders admit direct, zero-fee compensation

The closed-ladder numerical bound in [GRID_PROFILE_PROOF.md](GRID_PROFILE_PROOF.md),
Theorem 6.1, does not prescribe an auxiliary physical matching. This note
strengthens that certificate statement: except for its known odd extremizer,
every selected vertex can be paired DIRECTLY to an unoccupied, unselected
vertex. No actual matching edge pays for a TH path. Both directions of the
fixed actual matching are allowed.

This is a stronger physical certificate for an already bounded class, not
a new universal numerical bound. In particular it does not improve the
existing universal 5/6 coefficient. It identifies actual matching edges
crossing two-row band seams as a necessary feature of positive optimum
TH fees on even-by-even boards, and removes all matching-closed bands from
that remaining obstruction class.

## 1. Hypotheses and conclusion

Let G=P_2 square P_n, n>=1, with coordinates (r,c), r in {0,1} and
0<=c<n. Let M be any actual grid matching, P=V(M), T a subset of V\P,
and H=V\(P union T). The feasibility hypothesis is precisely

    |N_G(v) intersect (P union T)| <= 1   for every v in T.       (1)

There is no restriction to horizontal M, prescribed two-column cells,
low cycle rank, selection maximality, or an extremal choice of M.

N will be a full grid matching. In the tagged union M+N a shared actual
and auxiliary edge is a doubled P-only cycle. A TH component joins a
selected T endpoint to an H endpoint. Its fee is the sum of the weights
of the actual M edges on that component. Weights may be arbitrary
nonnegative real numbers; the construction does not inspect them.

**Theorem 1 (direct compensation on a closed ladder).** There exists a
full N such that every TH component is a single N edge, and every T is
an endpoint of such an edge, with exactly the following exception:

    n is odd, M is empty,
    columns c even are TT and columns c odd are HH.              (E)

In (E) there exists a full N with exactly one TT component and every
other T directly paired to H. For arbitrary nonnegative weights, the
exact lexicographic optimum (number of TT components, TH fee) is therefore

    (1,0) in (E), and (0,0) otherwise.                           (2)

In particular every feasible even-width closed ladder admits complete
zero-fee compensation. More strongly, its PAID ACTUAL EDGE SET is empty,
independently of the chosen weights.

## 2. Two disjoint kinds of column blocks

Write each column as its ordered pair of T,P,H labels. A name such as TP
allows either vertical order when the order is immaterial.

**Lemma 2 (forced occupied companion).** Every TP column has an adjacent
PH column, and the two P vertices are paired by M. Different TP columns
have different companion PH columns.

Proof. The P vertex cannot be M-matched vertically because its vertical
neighbour is T. Its M mate is horizontal, in an adjacent column. The T
vertex already has its one allowed selected-or-occupied neighbour, namely
the vertical P. Hence its horizontal neighbour in that companion column
is H. The companion is PH. Its sole P has only one M mate, so no two TP
columns can use it. TP and PH types are disjoint. Thus all resulting
two-column blocks are vertex disjoint. QED.

On each such block, put BOTH horizontal edges in N. One is a direct TH
edge; the other is exactly its actual M edge, now a doubled free component.
Both P endpoints in the block are internally M-matched. No actual edge
can leave the block.

**Lemma 3 (distinct empty companions).** All TT columns can be matched
injectively to adjacent HH columns, except in (E). In (E), all but one TT
column can be so matched.

Proof. A T in a TT column already has a vertical T neighbour. By (1),
every vertex in either adjacent column belongs to H. Form the graph on
TT and HH columns whose edges join physically adjacent columns of opposite
types. Every nontrivial component is an alternating path. An endpoint of
such a path of type TT must lie at a boundary of the entire ladder: any
existing adjacent column would be HH and extend the path.

If a component has two TT endpoints, both physical boundaries belong to
it. It is therefore the entire column path, has odd length and is exactly
the alternating word (E). Every other nontrivial component has at least
one HH endpoint. Start at an HH endpoint and pair each successive TT
with its preceding HH; this covers all its TT columns. An isolated TT
can occur only when n=1, which is (E). Isolated HH columns demand nothing.
In (E), pair the first n-1 columns in consecutive TT/HH pairs, leaving
one boundary TT. QED.

Put both horizontal edges into N on each chosen TT/HH pair. They are two
direct TH edges. These blocks are mutually disjoint by the injection.
They are also disjoint from Lemma 2's blocks, since their column types
TT,HH differ from TP,PH. Every one of their vertices is outside P.

## 3. Complete gluing and exactness

After the two block constructions, use a vertical N edge on every unused
column. The blocks cover whole columns and are disjoint, so this produces
a full physical matching of ALL vertices without conflict.

Every TP column was removed in Lemma 2 and every TT column was removed
in Lemma 3, apart from the exceptional leftover. Thus any remaining T
lies in a TH column, whose vertical edge pairs it directly to H. A direct
TH edge is an entire tagged component because neither endpoint belongs
to P. Actual edges cannot attach to or merge any of these components.
The internally occupied TP/PH blocks also cannot communicate with the
remaining P vertices. The remaining components consequently contain only
H endpoints or P-only cycles, and cannot carry a TH fee.

Outside (E) the constructed N has a=0 and paid actual edge set empty.
Both objectives are nonnegative, proving the exact optimum (0,0).
In (E), |T|=n+1 and |H|=n-1. Every terminal path has two endpoints, so
if a,b,t count TT,HH,TH paths, respectively, then

    |T|=2a+t,  |H|=2b+t,  a-b=1.

Thus a>=1 for every full N. The construction leaves exactly one vertical
TT edge and otherwise direct TH edges, attaining (1,0). This proves
Theorem 1, including both necessity and sufficiency of the exception.

There is no shared-reserve double spending: one distinct PH companion
is used per TP column, one distinct HH companion per paired TT column,
and no column occurs in both families. Two units supplied by an HH
column go to the two DIFFERENT T vertices of its unique assigned TT
column. All actual M edges used in TP/PH blocks become free doubled
components, and none is also counted as a TH payment.

The construction takes O(n) column operations and O(n) storage. In
Lemma 3, scan TT columns from left to right, preferring an unused left
HH neighbour and otherwise taking its right HH neighbour. Within an
alternating component this pairs to the left when it starts in HH,
and to the right when it starts in TT. Only (E) leaves a final TT.
Feasibility checks, mate-map construction and the final M+N component
traversal are linear as well. The implementation does not run a matching
optimizer or a frontier table to construct this certificate.

## 4. Occupied bands and the precise remaining obstruction

**Corollary 4 (matching-closed bands).** On an even-by-even rectangular
grid satisfying (1), suppose every actual M edge has both endpoints in
one of the disjoint two-row bands {0,1},{2,3},... . There is a full N,
also confined to those bands, for which every T is directly paired to H
and the paid actual edge set is empty.

Proof. Restrict M and T to each band. No actual edge is cut, so its P is
the restriction of global P. Discarding outside neighbours preserves (1).
Apply Theorem 1 in each even-width ladder, where (E) is impossible, and
take the union of the disjoint N matchings. Neither M nor N crosses a
band boundary, so components and their actual resource ownership agree
with their local versions. QED.

Consequently, if the exact full-N optimum on a feasible even-by-even
board differs from (0,0), M must cross a seam of this fixed band partition.
Applying the transposed corollary gives the analogous necessary condition
for a partition into two-column bands. Thus any unavoidable TT residual
or positive optimum TH fee requires BOTH a vertical actual edge crossing
a two-row seam AND a horizontal actual edge crossing a two-column seam.
A seam edge alone does not imply a nonzero optimum; these are necessary
conditions only.

The hypothesis cannot simply be removed. The existing feasible 4-by-4
example, under unit actual-edge weights, has

    M = {(0,1)--(0,2), (1,1)--(2,1)},
    T = {(0,0),(0,3),(2,0),(2,3),(3,1),(3,3)}.

Its unrestricted optimum is (a,f)=(0,1), as follows without enumeration.
With unit weights, a=0 and f=0 would force every T to be directly
N-matched to H. But the four selected vertices

    S = {(0,0),(2,0),(3,1),(3,3)}

have only THREE neighbours in H: {(1,0),(3,0),(3,2)}. They cannot be
matched injectively to H. Hence a=0 implies f>=1. The full auxiliary
matching

    N = {(0,0)--(0,1), (0,2)--(1,2), (0,3)--(1,3),
         (1,0)--(2,0), (1,1)--(2,1), (2,2)--(2,3),
         (3,0)--(3,1), (3,2)--(3,3)}

attains a=0,f=1: its sole paid actual edge is (0,1)--(0,2), the other
actual edge is a doubled free component, and all other T have direct
TH edges. This is a counterexample to extending ZERO-FEE compensation
without the closed-band hypothesis; it is not a counterexample to the
numerical target or to coverage. The exact four-label solver and all
full N provide additional implementation checks. The second actual edge
crosses the horizontal band seam, and the first crosses
the vertical band seam. Hence neither orientation of Corollary 4 applies.
The general proof of the frontier solver is in
[JOINT_FRONTIER_PHYSICAL_DEFECTS.md](JOINT_FRONTIER_PHYSICAL_DEFECTS.md).

Deleting seam M edges is NOT an application of this corollary to the
original pair: it changes their endpoints from P to unoccupied vertices.
Restoring those edges can then join terminal paths or consume H endpoints.
No fee bound proportional to the number of seam edges, nor a universal
5/6 improvement, is asserted by the present argument.

## 5. A general direct-hole deficit lower bound

The same obstruction supplies a useful lower bound without the ladder or
selected-degree hypotheses. Form the bipartite graph consisting of grid
edges between T and H, and let nu be its maximum matching size. Its Hall
defect is d=|T|-nu=max_(S subset T)(|S|-|N_H(S)|).

**Lemma 5 (residual-versus-fee lower bound).** For every full N, if a counts
TT components and p counts the DISTINCT actual M edges on TH components,
then

    2a+p >= d.                                                 (3)

For unit actual weights this is 2a+f(N)>=d. For complete coverage it
gives f(N)>=d, without attributing the same paid actual edge twice.

Proof. There are |T|-2a TH components. Say k of these contain actual M
edges. The remaining |T|-2a-k are direct TH edges and form a matching
in the T-to-H graph, so |T|-2a-k<=nu. Distinct nontrivial TH components
contain disjoint nonempty actual edge sets, giving p>=k. These two
inequalities prove (3). The equality between the matching defect and
the maximum Hall deficiency is the standard bipartite matching theorem.
QED.

This is an elementary general matching lower bound; it is not an upper
bound or a geometric proof of global compensation. In the odd ladder
exception d=2, and the constructed pair a=1,p=0 attains (3). In the
4-by-4 seam example, the displayed Hall set proves d>=1 and the given
witness has a=0,p=1, hence d=1 and (3) is sharp. On all nonexceptional
closed ladders Theorem 1 proves d=0 as well as extendibility of its
direct TH matching to a full physical N. A Hall test alone on a general
grid would not establish that latter extension.

## 6. Evidence and attribution

The forced TP-to-PH injection and the TT-column boundary rigidity already
appear in the numerical proof of Theorem 6.1 cited above. The additional
deduction here is their simultaneous physical realization by disjoint
column blocks, giving direct payments and an EMPTY actual fee set for
arbitrary weights. No claim of a new general path-matching method is made.

The implementation is `develop/closed_ladder_compensation.py`; its checker
compares against actual full auxiliary matchings and the existing frontier
solver on small ladders, tests mixed-direction occupied blocks, and checks
large explicit families and the band-seam witness. These finite checks
validate the delivered code. The all-size assertions follow from the
column injection, alternating-path proof and disjoint gluing above.
This note makes no new Lean verification claim and does not modify the
11 October manuscript or the public manuscript revision.
