# Mixed auxiliary components: three physical bridges and a normalization obstruction

## Setting and scope

Use the partial-template notation of `manuscript/starforming-gap.tex`.
There are $b$ helpers, $N=2b$ witness indices $V$, and one owner per
index, hence $5b$ physical vertices. The perfect matching $P$ pairs the
two witnesses of each helper; $Q$ is the matching of witness--witness
edges, and $A=P\cup Q$. Physical colours are equal along $P$ and
opposite along $Q$ and the owner graph $B$. The latter has maximum
degree two, so its components are paths and even cycles. The auxiliary
graph $A$ is bipartite: its cycles alternate $P,Q$; a cycle with $k$
$Q$-edges changes physical colour $k$ times, so its order is divisible
by four. Auxiliary paths are allowed.

An omission set $U\subseteq V$ is *permitted* if $B[V\setminus U]$
has maximum degree at most one. Write $\beta_I$ for the largest physical
dissociation set containing every helper. The existing exact formula is

$$
 \beta_I=3b-\min_{U\text{ permitted}}\nu(A[U]).                 \tag{1}
$$

Indeed, fix the selected owners $V\setminus U$. The available witness
indices form $U$, and their maximum allowed number is
$\alpha(A[U])=|U|-\nu(A[U])$ by bipartite matching. This gives (1).
In particular, the physical target is equivalent to finding a permitted
$U$ with $\nu(A[U])\le\lfloor N/6\rfloor$.

The three physical theorems below prove this target on additional mixed
classes. None assumes that an owner component stays inside one auxiliary
component. They do not prove the unrestricted physical inequality, a new
unrestricted star-forming gap coefficient, or a grid (5/6) improvement.
The abstract colouring theorem alone does not imply (1)'s target; the last
section gives an exact counterexample to that conversion.

## 1. A general mixed colouring theorem

**Theorem 1.** Let $A$ be any finite simple graph of maximum degree two,
and let $B$ on the same vertices be a disjoint union of paths and even
cycles. There is a three-colouring proper on $A$ in which each colour
class induces maximum degree at most one in $B$. In particular some
$A$-independent $B$-dissociation set has size at least
$\lceil |V|/3\rceil$.

**Proof.** Alternate actual edges along each $B$ component to obtain
matchings $R,F$ partitioning $E(B)$. This uses actual edges even on
owner four-cycles. The simple graph $J=A\cup R$ has maximum degree three.
Every $K_4$ is a whole connected component. At each of its vertices
exactly two distinct edges come from $A$ and one from $R$. Removing
the $R$-matching leaves a whole $A$-four-cycle, whose $R$-edges are
its two diagonals.

Temporarily remove all such $K_4$ components. Properly three-colour the
remainder of $J$ using Brooks's theorem; components of degree at most
two, including odd cycles, admit three colours as well. Restore the
removed squares one at a time. At a restored vertex forbid the colour of
its $F$-neighbour if already coloured. Each available list has at least
two colours, because $F$ is a matching. An internal $F$-edge must be an
$A$-edge: the square's two non-$A$ pairs are already the $R$-diagonals.

A four-cycle is two-choosable. Trim each list to two colours. If all lists
agree, alternate the two colours. Otherwise choose adjacent vertices with
different lists, give the first a colour absent from the second's list,
and colour around the other direction greedily, reaching the second vertex last.
Its first neighbour forbids no available colour, so its other neighbour
still leaves a choice. Thus restore the square properly on $A$, while
respecting every $F$-edge to an earlier vertex. Any $F$-edge between
two restored squares is respected by the later one.

Outside restored squares all $R$-edges are proper; at restored vertices
all incident $F$-edges are proper. Thus any vertex has at most its one
$F$-neighbour or its one $R$-neighbour of the same colour, respectively.
All $A$-edges are proper. A largest class proves the size assertion. ∎

This is an existence proof; the supplied implementation uses a feasibility
colouring search. No polynomial bound is asserted for that search.
The only external theorem used is the same Brooks theorem already cited
in the manuscript: R. L. Brooks, “On colouring the nodes of a network,”
*Proceedings of the Cambridge Philosophical Society* 37 (1941), 194–197.
There is no external literature-priority claim here.

## 2. Physical repair when a specified matching has at most one K4

For this section choose $R$ by the existing physical rule: perfect
matching on even-order owner paths, an alternating matching leaving an
endpoint on odd-order paths, either perfect matching on non-square even
cycles, and **opposite pairs** on owner four-cycles. Let $o$ be the
number of odd-order paths, including singletons, and let $W$ be the
covered vertices. Let $z$ be the number of $K_4$ components in
$J_R=A[W]\cup R$.

**Theorem 2.** If some specified choice has $z\le1$, then
$\beta_I\ge\lceil8b/3\rceil$. In particular this holds whenever $A$
has at most one four-cycle component, with arbitrary other auxiliary and
owner components.

**Proof.** The existing matching bound is
$$
 \beta_I\ge\left\lceil8b/3+(o-2z)/6\right\rceil.
$$
It covers $z=0$, and $z=1,o\ge2$. Since $o$ is even, only
$z=1,o=0$ remains. Now $R$ is perfect. Let $K$ be its obstructing
auxiliary square, with $R$-diagonals $e,f$. They are actual owner
edges: an auxiliary square has physical colours (0,0,1,1) cyclically,
so its diagonals join opposite colours; a virtual owner-square diagonal
joins equal colours.

Properly three-colour $J_R-K$. For each colour $t\in\{0,1,2\}$, take
the exterior colour class and both endpoints of $f$ as witnesses. They
are $A$-independent because $K$ is an entire auxiliary component.
Ordinarily select one owner outside the witness set from each exterior
$R$-pair, and one endpoint owner of $e$.

There are at most two exterior owner neighbours of the endpoints of
$e$. If there are two, they cannot be mates in $R$: their matching
edge, $e$, and the two links would form an entire owner four-cycle, on
which $R$ would instead use virtual diagonals. Thus their exterior
$R$-pairs are distinct. Choose $t_*$ different from the colours of
their mates (at most two colours). In construction $t_*$, select both
owners of $e$, and in each of these exterior pairs select the mate of
the neighbour. These prescribed owners lie outside colour $t_*$.

The doubled edge $e$ has no selected exterior owner neighbour; any
neighbour on $f$ is also excluded. In every other ordinary owner
component a singleton from each $R$-pair can have at most one selected
neighbour, through $B-R$. Virtual owner squares retain exactly two
owners, any two of which induce maximum degree at most one. Hence all
three selections are physical dissociation sets containing all helpers.

Across the three constructions, the exterior contributes $N-4$
witness occurrences and $3(N-4)/2$ owner occurrences. The square
contributes six witness and four owner occurrences. Including helpers,
the sum of the three cardinalities is exactly
$$
 3b+\tfrac52(N-4)+10=8b.
$$
One therefore has size at least $\lceil8b/3\rceil$. Every $K_4$
needs a distinct whole auxiliary square, proving the last assertion. ∎

An explicit connected (40)-vertex benchmark in the fixture has
$A=C_4+C_{12}$, $B=P_{12}+C_4$, and the specified $J_R$ has one $K_4$ component. Its connected
12-vertex remainder has a spanning collection of four vertex-disjoint
triangles, with additional edges between them. These five cliques bound
its independence number by five; $\{0,4,7,10,13\}$ attains five,
so the “one owner per R-pair” restriction gives at most (8+8+5=21),
below the target 22. The repair supplies a valid target certificate.
The **actual** all-helper optimum is 24 (cost zero), not 22. This example
separates a construction restriction from the physical optimum.

## 3. Any number of owner squares, with paths and 6k-cycles

**Theorem 3.** Suppose every owner cycle has length four or a multiple
of six. Owner paths and auxiliary components are arbitrary. Then
$\beta_I\ge\lceil8b/3\rceil$. A permitted omission set achieving the
target can be constructed in polynomial time.

**Proof.** Let $I\subseteq V$ be the union of the owner four-cycles,
and $O=V\setminus I$. Label each vertex of $I$ by two bits. The first
is its physical colour. For the second, properly two-colour the union of
$P[I]$ and the matching of opposite pairs in each owner square. The
union of two matchings consists of paths and even cycles (a shared edge
is simply one edge), so this is possible. On each owner square the four
labels are distinct: adjacent vertices differ in the first bit and
opposite vertices differ in the second. Every $A[I]$-edge has distinct
labels, since its $P$-edges differ in the second bit and $Q$-edges
in the first.

Choose uniformly one of the six pairs of labels, putting the vertices
with these labels into $U_I$. Independently on each owner component in
$O$, choose uniformly one of the three residue classes of positions
modulo three, putting it into $U_O$. Every owner square loses exactly
two vertices; every consecutive owner triple in $O$, including wrap
triples on $6k$-cycles, meets $U_O$. Thus $U=U_I\cup U_O$ is always
permitted. A vertex in $I$ is omitted with probability (1/2), one in
$O$ with probability (1/3). An internal $I$-edge is fully omitted
with probability (1/6); an edge crossing $I,O$ has that probability
by independence and the marginals.

For **any** matching of $A[U]$, let $m_I,m_O,m_\partial$ count its
edges inside $I$, inside $O$, and crossing the interface. Its distinct
$O$-endpoints imply $2m_O+m_\partial\le|U_O|$. Consequently
$$
 \nu(A[U])\le F(U):=\frac{|U_O|}{2}
       +|E_A(U_I)|+\frac{|E_A(U_I,U_O)|}{2}.                 \tag{2}
$$
The degree sum on $I$ now gives a **single global budget**:
$$
 \mathbb E F(U)
 =\frac{|O|}{6}+\frac{2|E_A(I)|+|E_A(I,O)|}{12}
 \le\frac{|O|+|I|}{6}=\frac N6.                            \tag{3}
$$
Each interface edge enters (2) once, and a matching consumes each
$O$-endpoint once. No per-component interface allowance is added.
Some permitted $U$ has integer matching cost at most
$\lfloor N/6\rfloor$, proving the target via (1).

For a polynomial construction, enumerate the six label pairs. For a fixed
$U_I$, twice (2)'s budget is
$$
 2|E_A(U_I)|+
 \sum_{v\in U_O}\bigl(1+\deg_A(v,U_I)\bigr).               \tag{4}
$$
Independently on each component of $B[O]$, choose the residue class
minimizing the sum in (4). This cannot exceed its average over phases.
Taking the best of the six label pairs cannot exceed the overall average
in (3). Compute a maximum matching of $A[U]$ and its complementary
maximum independent set to recover the physical certificate. ∎

This is a bound on matching cost, not just an expected omission size.
The interface term is essential when owner components cross auxiliary
components. Multiple exceptional owner four-cycles are allowed.

## 4. At most one exceptional owner cycle, of arbitrary length

Call an even owner cycle *exceptional* if its order is not divisible by
six. The omission exchange needed below is explicit. For any edge $xy$
of an exceptional cycle $C_m$, there are minimum omission sets differing
exactly by replacing $x$ with $y$. For $m=4$, use
$\{x,z\},\{y,z\}$ with $z$ the vertex opposite $x$. For $m>4$
put $k=\lceil m/3\rceil$. Start with omission $x$, cyclic gap three
after it and gap two before it. All other gaps are three, except one
additional gap two when $m\equiv1\pmod3$. Their sum is $m$.
Replacing $x$ by its successor $y$ changes adjacent gaps (2,3) to
(3,2). Both sets have $k$ omissions and meet every consecutive triple.
There is room for the extra gap when needed: the next case after four
is ten, with $k=4$.

**Theorem 4.** If $B$ has at most one exceptional cycle, with arbitrary
paths, other owner cycles and auxiliary components, then
$\beta_I\ge\lceil8b/3\rceil$. A target omission set can be found in
polynomial time.

**Proof.** A path of order $l$ needs exactly $\lfloor l/3\rfloor$
omissions, and a cycle exactly $\lceil l/3\rceil$. These follow by
covering consecutive triples; residue classes attain the path bound and
cyclic gaps of size at most three attain the cycle bound. The minimum
global omission cardinality $m$ therefore satisfies
$m\le N/3+2/3$. The trivial matching bound
$\nu(A[U])\le\lfloor m/2\rfloor$ suffices unless
$$
 N=6k+4,\qquad m=2k+2.                                    \tag{5}
$$
For completeness, in residues $N=6k,6k+2$ the maximum possible integer
$m$ is respectively $2k,2k+1$, which gives cost at most $k$.
Equality (5) requires the exceptional cycle $C$ to have order $4\bmod6$,
and every other owner component to have order divisible by three: its
(2/3) surplus is the only positive surplus and every path residue loss
must vanish. In particular, every other component admits each of its
three residue classes as a minimum omission set.

It suffices to find a minimum $U$ whose auxiliary induced graph has no
perfect matching. The following stronger local lemma supplies this.

**Local count lemma.** Fix *any* omission choice $U_0$ outside an
exceptional owner cycle $C$ (it need not be minimum). If
$|U_0|+\lceil |C|/3\rceil$ is even, then some minimum omission choice
$U_C$ on $C$ makes $A[U_0\cup U_C]$ have no perfect matching.
It suffices to test the two exchanged choices for each edge of $C$.

Suppose all these exchanged choices had perfect matchings. For any edge
$xy$ of $C$, their symmetric difference contains an even alternating
path from $x$ to $y$, inside $A[U_0\cup V(C)]$. Thus all of $C$
lies on one bipartition side $L$ of a single connected component $K$
of that auxiliary induced graph. Put its other side equal to $R$.
The graph $K$ is a path or even cycle, hence
$||L|-|R||\le1$. In any one of the assumed perfect matchings, every
vertex of $K$ outside $C$ is retained, and exactly
$\lceil |C|/3\rceil$ of its $C$-vertices are retained. There can
be no matching edge leaving $K$. Perfect balance would require

$$
 |L|-|R|=|C|-\lceil |C|/3\rceil\ge2,
$$

contradicting the path/cycle bound. The last inequality uses
$|C|\ge4$. This proves the local lemma. Notice that all outside
choices stay fixed; no separator or outside phase change is necessary.

Under (5), the minimum omission size is even, and the local lemma
reduces matching cost from at most $k+1$ to at most $k$. Formula
(1) proves Theorem 4. For construction test the two exchanged minimum
choices at each edge of the exceptional cycle, keeping the initial
minimum outside choice fixed. There are at most $2|C|$ polynomial
matching tests. ∎

**Stronger cardinality corollary.** Let $m$ be the minimum global
omission cardinality for an arbitrary owner graph of paths and even
cycles. If $m$ is even and some owner cycle is exceptional, then

$$
 \min_{U\text{ permitted}}\nu(A[U])\le m/2-1.             \tag{5a}
$$

Keep minimum omissions outside that cycle and apply the local lemma.
Together with the universal bound $\lfloor m/2\rfloor$, this proves
the physical target whenever either that bound is at most
$\lfloor N/6\rfloor$, or $5a$ is at most that target. Multiple
exceptional cycles are allowed. This improves the omission-cardinality
criterion by one matching edge; it does not assert an independent saving
for every exceptional cycle.

**Owner-size form of the corollary.** For arbitrary physical auxiliary
components, the sufficient condition is

$$
 \beta_2(B)\ge 2\lceil N/3\rceil-2.                         \tag{5b}
$$

Indeed, for even $N$,
$N-2\lfloor N/6\rfloor-2=2\lceil N/3\rceil-2$.
Thus (5b) says $m\le2\lfloor N/6\rfloor+2$. Odd $m$ already gives the
target by $\lfloor m/2\rfloor$. At the only extra even value, one saving
suffices by (5a); an exceptional cycle must exist, since otherwise
$m\le\lfloor N/3\rfloor$. This removes the auxiliary-square hypothesis
from the earlier owner-size parity criterion. It remains a sufficient
owner-size condition, not an unrestricted physical theorem.

## 5. An exact mixed normalization counterexample

The exact identity $\beta_I=2b+h$ for a union of auxiliary squares,
where $h$ is the largest $A$-independent $B$-dissociation set, cannot
be extended to arbitrary auxiliary mixtures. Set $b=6$,

$$
\begin{aligned}
 P&=\{01,23,45,67,89,(10)(11)\},\\
 Q&=\{08,19,2(11),3(10),57\},\\
 B&=C_{12}(0,7,4,8,3,11,2,10,1,6,5,9).
\end{aligned}
$$

Here edges such as (2(11)) denote the pair ({2,11}). Physical colours
are zero on $0,\ldots,5$ and one on $6,\ldots,11$. Thus

$$
 A=C_4(0,1,9,8)+C_4(2,3,10,11)+P_4(4,5,7,6).
$$

All physical hypotheses hold, and the (30)-vertex physical graph is
connected since its owner graph is one spanning cycle. The set
$\{0,9,2,10,4,6\}$ is compatible and has size six. The perfect
matching $P$ bounds any $A$-independent set by six, so $h=6$.
Nevertheless

$$
 \boxed{\beta_I=17<18=2b+h.}                               \tag{6}
$$

For the lower bound, $U=\{0,1,2,5,8\}$ is permitted. Its only
auxiliary edges are (01,08), giving matching cost one. To exclude cost
zero, suppose $U$ is auxiliary-independent and its owner complement
$D$ is dissociation. Enlarge $U$ to maximal independence, which only
shrinks $D$. A maximal independent set on a four-cycle is an opposite
pair. Thus on the first square $D$ contains either $\{1,8\}$ or
$\{0,9\}$, and on the second either $\{3,11\}$ or $\{2,10\}$.
In the first case one of the owner paths (8,3,11) and (2,10,1) is
entirely in $D$. In the second, the selected owner edge (0,9) forces
both outside neighbours (7,5) into $U$, contradicting auxiliary edge
(57). Hence the minimum cost is exactly one, proving (6).

Even a compatible set of the requested threshold size need not convert:
$S=\{0,2,4,6\}$ has size $\lceil N/3\rceil=4$, but its complement
has matching cost three, one from each auxiliary component, exceeding
$\lfloor b/3\rfloor=2$. This refutes that conversion, not the physical
target. Here the physical optimum 17 exceeds its target 16.

## Consequences and evidence

Together with the previously proved all-auxiliary-square theorem, the
bridges narrow any remaining physical counterexample: its auxiliary graph
must mix squares with a non-square component; every specified owner
matching must produce at least two $K_4$'s; and it must have at least two
exceptional owner cycles, including one of order at least eight. This is
a necessary condition for a possible counterexample, not its existence.

For a fixed witness extraction in a bipartite subcubic graph, any of the
three physical hypotheses on its **actual** extracted template makes the
existing ledger term $Z=3\beta-3L-8b'$ nonnegative. The unchanged identity

$$
 5n-51d=Z+5r+12(\alpha+\pi)+24\tau+7(e-b_3)+2b_3+5q
$$

then gives $51d\le5n$. A statement about the maximum minimal forming set
requires an extraction of that set with this property. This extends the
scope of the existing conditional (5/51) bound; it is not a universal
coefficient improvement.

The proof is general. `scripts/check_mixed_owner_bridges.py` checks actual
physical sets, exhaustive small controls, prescribed-edge exchanges and
local balance cases. Its script specifies the tested ranges and its report
gives the counts; these computations do not replace the arguments above. Both exact counterexamples, including the
distinction between the restricted value 21 and exact value 24, are stored
in `develop/fixtures/mixed-owner-bridges.json`. The independent review and
its execution scope are recorded in `output/mixed-owner-bridges-review.json`.
The research lead came from Oracle task
`a51b730e-b68d-4ef1-99f3-a43e66efbdff`; the independent audit is a separate
task. No Lean execution or formal verification claim is made.
