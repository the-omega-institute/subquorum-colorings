# Fixed inactive vertices separate simultaneous owner exchanges

## The activation budget

Use the physical notation and exact matching formulation of
[the whole-support theorem](DISJOINT_AUXILIARY_SUPPORT_BUDGET.md).
There are $b$ helpers, $N=2b$ witness/owner indices, and $5b$ physical
vertices. The auxiliary graph $A=P\cup Q$ is bipartite of maximum degree
two, the owner graph $B$ consists of paths and even cycles, and

$$
 \beta_I=3b-\min_{U\text{ permitted}}\nu(A[U]).             \tag{1}
$$

Permitted means that $B[V\setminus U]$ has maximum degree at most one.
Fix any permitted $U_*$ and distinct exceptional owner cycles
$C_1,\ldots,C_t$ (their lengths are not divisible by six), with
$|U_*\cap C_i|=\lceil|C_i|/3\rceil$. Choose **one common** vertex set

$$
 U_*\cup C_1\cup\cdots\cup C_t\ \subseteq W\subseteq V.    \tag{2}
$$

Let $K_j$ be the connected components of $A[W]$, put
$m_j=|U_*\cap K_j|$, $m=|U_*|$, and let $o_W$ count the odd $m_j$.
Define full activated supports

$$
 \sigma_W(C_i)=\{j:K_j\cap C_i\ne\varnothing\}.
$$

**Theorem.** Suppose these supports are pairwise disjoint, and every
$m_j$ touched by a support is even. There is a permitted $U\subseteq W$
of cardinality $m$ such that

$$
 \boxed{\nu(A[U])\le\frac{m-o_W}{2}-t.}                  \tag{3}
$$

The certificate is constructive with at most $2\sum_i|C_i|$ matching
tests once $W$ and the cycles are given. If the right side of (3) is at
most $\lfloor N/6\rfloor$, then $\beta_I\ge\lceil8b/3\rceil$.
Taking $W=V$ recovers the previous theorem. No optimum selection of
cycles or activation set is claimed.

## Proof and resource ownership

For each chosen cycle allocate the entire region
$R_i=\bigcup_{j\in\sigma_W(C_i)}K_j$. These regions are disjoint and
have no edges between them **in $A[W]$**. They may have edges in $A$ to
vertices outside $W$, but those vertices are absent from every possible
resulting omission set, so such edges never belong to $A[U]$.

The fixed-outside lemma from the previous proof applies in the bipartite
maximum-degree-two graph $A[R_i]$. In detail, let
$U_0=(U_*\cap R_i)\setminus C_i$, and write $q=|C_i|$,
$k=\lceil q/3\rceil$. For each consecutive pair $x,y$ on $C_i$, the
minimum omission family contains two choices differing only by
$x\leftrightarrow y$. If every tested choice had a perfect auxiliary
matching, symmetric difference would give an even alternating path
between each consecutive $x,y$. Thus all vertices of $C_i$ lie on the
same side $L$ of one component $D$ of $A[U_0\cup C_i]$. In a perfect
choice all vertices of $D\setminus C_i$ remain, and exactly $k$ cycle
vertices remain. Hence $|L|-|R|=q-k\ge2$. This contradicts the side
difference at most one in a connected bipartite graph of maximum degree
two. Some tested choice therefore has no perfect matching.

The initial regional count $M_i=|U_*\cap R_i|$ is even. Replacing only
the omissions on $C_i$ by the returned minimum choice gives regional
cost at most $M_i/2-1$. Make all replacements simultaneously. Every
replaced cycle is a whole owner component; all other owner memberships
are fixed. The resulting set is permitted, has size $m$, and stays
inside $W$ by (2). Its matching cost adds over the allocated regions and
the unassigned activated components. Every initially odd component is
unassigned. Therefore

$$
 \nu(A[U])\le\sum_i(M_i/2-1)
       +\sum_{j\text{ unassigned}}\lfloor m_j/2\rfloor
       =\frac{m-o_W}{2}-t.
$$

Each region is used once. Individual activated-component counts inside a
region may change; only their regional sum is preserved. Newly odd
components are not credited again. This proves (3). The per-edge exchange
families have at most $2q$ members, proving the algorithmic claim. ∎

There is a necessary consistency rule in using this sufficient condition:
changing the proposed cycle set can change $W$, its components, their
parities and their supports. These quantities must be recomputed together.
One cannot give each cycle its own smaller activation graph and then add
the resulting savings.

## Mixed owner cycles on one long auxiliary cycle

For every $r\ge1$, use $r$ blocks of 24 indices. Local pairs below are
unordered, and every index in block $i$ receives offset $24i$.

$$
\begin{aligned}
P={}&\{(0,2),(1,3),(5,7),(6,8),(4,10),(9,11),\\
 &\qquad(12,14),(13,15),(16,18),(17,19),(20,21),(22,23)\},\\
Q_0={}&\{(0,3),(1,2),(5,8),(6,7),(4,13),(15,12),\\
 &\qquad(9,16),(18,17),(14,20),(21,22),(23,19)\}.
\end{aligned}
$$

Add to $Q$ the edges
$(24i+10,24(i+1\bmod r)+11)$. The owner components are the local cycles

$$
 C_{10}(0,1,\ldots,9),\quad C_4(12,13,14,15),\quad
 C_4(16,17,18,19),\quad C_4(20,22,21,23),
$$

and the same cross-block $P_2$ edges between 10 and the next block's 11.
Physical colour is local parity for indices 0 through 19; indices
20,21 have colour one and 22,23 colour zero. Thus $P$ joins equal
physical colours and $Q,B$ join opposite colours. $P,Q$ are perfect
matchings. Here $b=12r$ and the physical order is $60r$.

The auxiliary graph consists of $2r$ squares and **one** cycle of order
$16r$. In each block the long cycle traverses

$$
 10,4,13,15,12,14,20,21,22,23,19,17,18,16,9,11
$$

and then block $i-1$'s 10, with block indices modulo $r$. The two local squares are
$(0,2,1,3)$ and $(5,7,6,8)$.

Take the minimum owner omissions

$$
 U_*\cap\text{block}=\{0,2,5,7,12,14,16,18,21,22\}.     \tag{4}
$$

Then $m=10r$. All original auxiliary counts are even: two in each square
and $6r$ in the long cycle. Choose the $2r$ owner squares on indices
12 through 19, and take the minimal $W$ in (2). In each block $A[W]$
has five components:

$$
 (0,2),\quad(5,7),\quad(14,12,15,13),\quad
 (16,18,17,19),\quad(21,22).
$$

Each has initial count two. Each chosen cycle consumes its own four-path;
the full activated supports are disjoint. Thus $o_W=0$, $t=2r$, and

$$
 \nu(A[U])\le3r\le\lfloor N/6\rfloor=4r,
 \qquad \beta_I\ge33r>32r=8b/3.                        \tag{5}
$$

For the same $U_*$ the whole-component rule has a maximum support packing
of size **one**: every exceptional owner cycle touches the unique long
auxiliary component. Its bound is only $5r-1$, which exceeds $4r$ when
$r\ge2$. The improvement in this budget is $2r-1$, unbounded.
This comparison concerns the same prescribed initial set (4); it does
not assert that no other initial set could help the earlier theorem.

The preceding global criteria also fail for $r\ge2$: $A$ is not all
squares, $B$ contains multiple ten-cycles, and
$\beta_2(B)=14r<16r-2=2\lceil N/3\rceil-2$.
Every specified owner matching has exactly $r$ obstructing $K_4$'s:
on each ten-cycle its two phases create one or the other local auxiliary
square obstruction. There are no other auxiliary squares. Consequently
the existential at-most-one-$K_4$ criterion fails for $r\ge2$.
This is a sufficient class beyond these listed tests, not an external
priority claim or a claim that other decomposition arguments cannot work.

The physical graph is connected, bipartite, with minimum degree two and
maximum degree three. The long auxiliary cycle connects its witness and
helper vertices, and every corresponding owner attaches to its witness.
The owners on the local ten-cycle attach the two remaining auxiliary
squares to this connected part. Every vertex is accounted for. Helpers
have degree two; witnesses have degree three; cycle owners have degree
three and the port owners on cross-block edges have degree two.
No two-connectivity claim is made.

The budget is not sharp on this family. The explicit minimum omission set

$$
 U^0\cap\text{block}=\{0,1,4,7,14,15,16,17,21,23\}       \tag{6}
$$

is auxiliary-independent. Its owner complement is a dissociation set:
on the ten-cycle its edges are $23,56,89$; on each owner square the
complement is one edge; both cross-block port owners are retained and
have only their mutual owner edge. No listed $P$ or $Q$ edge is contained
in (6). Equations (1) and (6) prove

$$
 \boxed{\beta_I=36r.}                                   \tag{7}
$$

The upper cap $3b$ also has a direct physical proof. With every helper
retained, a selected witness already has a selected helper neighbour, so
its owner cannot be selected. Thus at most $N$ witnesses and owners in
total can be selected, and adding $b$ helpers gives $3b$.

## An older single-cycle control and the limit of the new rule

In the earlier $H_r$ family, $A=C_{8r}$ and $B$ consists of $2r$ squares.
Take $U_*$ locally $\{0,1,2,3\}$ in each eight-index block and choose the
owner square on its even indices. The common minimal $W$ has local
vertices $\{0,1,2,3,4,6\}$. Missing vertices 5 and 7 separate blocks.
Each chosen square touches one path $0,1,2,3,4$ and the singleton 6,
with initial counts four and zero. Equation (3) gives cost at most $r$,
whereas the whole-component budget gives $2r-1$. The known true cost
is $\lceil r/2\rceil$, so the activation budget need not be exact.
All-owner squares were already settled by the earlier label theorem;
this control is not a newly settled physical class.

Nor may both parity squares in every block be independently credited.
Their common activation graph is the entire cycle, so their supports
overlap. Adding their separate local savings would predict cost zero,
contradicting the all-$r$ exact cost $\lceil r/2\rceil>0$.

## Verification and remaining questions

The accompanying constructor returns the actual owner and witness sets,
the one common activation graph, support allocation, local exchanges and
a maximum matching. The checker reconstructs the physical graph and
activated supports from raw edges, checks dissociation directly, and
counts path/cycle matching sizes independently. Small slices also use
literal matching recurrence and exhaustive permitted omission sets.
All-$r$ claims above follow from proofs and explicit coordinates;
finite checks only audit their implementation.

The universal physical $8b/3$ question, the sharp unrestricted subcubic
gap coefficient, general grid Hall completion, unit $5/6$, and arbitrary
rectangular-grid triple equality remain open. This result gives a new
sufficient separation condition, not an exact optimization algorithm or
a general local-descent theorem. No Lean execution is claimed.
