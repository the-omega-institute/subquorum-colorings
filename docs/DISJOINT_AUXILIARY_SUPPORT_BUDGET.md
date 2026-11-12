# Disjoint auxiliary supports for simultaneous owner exchanges

## Data and the precise budget

Use the physical template notation in [the mixed-owner proof](MIXED_OWNER_BRIDGES.md).
There are $b$ helpers and $N=2b$ indices. The perfect matching $P$ joins
same physical colours; the partial matching $Q$ and the maxdegree-two owner
graph $B$ join opposite colours. Thus $A=P\cup Q$ is bipartite and has
maximum degree two. An omission set $U$ is permitted when
$B[V\setminus U]$ has maximum degree at most one, and

$$
 \beta_I=3b-\min_{U\text{ permitted}}\nu(A[U]).              \tag{1}
$$

Fix **any** permitted omission set $U_*$, of size $m$. It need not have
minimum global cardinality. Let $K_1,\ldots,K_s$ be the auxiliary components,
let $m_j=|U_*\cap K_j|$, and let $o$ be the number of odd $m_j$.
Call an owner cycle exceptional when its order is not divisible by six.
For an exceptional owner cycle $C$, define its full auxiliary support

$$
 \sigma(C)=\{j:K_j\cap V(C)\ne\varnothing\}.              \tag{2}
$$

A cycle is eligible if $|U_*\cap V(C)|=\lceil|C|/3\rceil$ and every
$m_j$ with $j\in\sigma(C)$ is even. A packing is any set $\mathcal P$
of eligible cycles whose supports (2) are pairwise disjoint. It is enough
to provide such a packing; it need not be maximum.

**Theorem.** If $t=|\mathcal P|$, there is a permitted $U$ of the same
cardinality as $U_*$ for which

$$
 \boxed{\nu(A[U])\le\frac{m-o}{2}-t.}                    \tag{3}
$$

In particular, if $(m-o)/2-t\le\lfloor N/6\rfloor$, then
$\beta_I\ge\lceil8b/3\rceil$. The certificate can be constructed with
at most $2\sum_{C\in\mathcal P}|C|$ bipartite matching tests after the
packing has been supplied. A greedy support packing is polynomial; no
claim is made that it maximizes $t$.

The supports include **all** auxiliary components touched by a cycle. The
cycle is not required to fit in one component. Other owner components
may cross freely between the regions used in the proof.

## General proof

We recall the fixed-outside count lemma, with its full reason. Let $C$
be an exceptional owner cycle, fix an arbitrary outside omission set
$U_0$, and suppose $|U_0|+\lceil|C|/3\rceil$ is even. For each edge
$xy$ of $C$ there are two minimum omission choices on $C$ differing only
by $x\leftrightarrow y$. They are given by cyclic gaps at most three:
gaps two before $x$ and three after $x$ switch to three and two after
replacing $x$ by its successor. When needed there is one other gap two;
the four-cycle case is the direct two-point exchange.

If every exchanged choice gave a perfect auxiliary matching, the symmetric
difference for each pair would have an even alternating path between
$x,y$. These paths all lie in $A[U_0\cup V(C)]$. Consequently all of $C$
lies on one bipartition side $L$ of one connected component $D$ of this
graph. In any assumed perfect matching, all vertices of $D\setminus C$
are retained, and exactly $k=\lceil|C|/3\rceil$ vertices of $C$ are
retained. There can be no matching edge leaving $D$, so its sides would
satisfy $|L|-|R|=|C|-k\ge2$. A connected bipartite graph of maximum degree
two is a path or even cycle and has side difference at most one. This is
a contradiction. Some exchanged choice therefore has no perfect matching.
This lemma is valid for the auxiliary graph restricted to any union of
whole auxiliary components, not only for the whole board.

For each $C\in\mathcal P$ put

$$
 R_C=\bigcup_{j\in\sigma(C)}K_j.
$$

The regions $R_C$ are vertex-disjoint and no auxiliary edge joins two
regions or joins one of them to an unassigned auxiliary component. Put
$M_C=|U_*\cap R_C|$. By eligibility, $M_C$ is even and $U_*\cap C$ is a
minimum omission choice on that cycle. Keep $(U_*\cap R_C)\setminus C$
fixed and apply the local lemma in $A[R_C]$. It returns minimum $U_C$
on $C$ with local matching cost at most $M_C/2-1$.

Make all these replacements simultaneously. Every replaced $C$ is an
entire owner component, distinct replacements concern distinct cycles,
and no other owner membership changes. Hence the result is permitted
even if other owner components cross regions. Its total size is still
$m$. Matching cost adds across these regions and the remaining auxiliary
components. For each unassigned component it is at most
$\lfloor m_j/2\rfloor$. All initial odd components are unassigned, giving

$$
 \nu(A[U])\le\sum_{C\in\mathcal P}(M_C/2-1)
       +\sum_{j\text{ unassigned}}\lfloor m_j/2\rfloor
       =\frac{m-o}{2}-t.
$$

Every chosen region is charged exactly once. A replacement can change the
individual $m_j$ inside its region: the theorem preserves their regional
sum, **not** every component count. Any new odd components created inside
that region are already included in its local cost bound and are not
credited a second time. This proves (3) and the construction claim. ∎

A previous candidate incorrectly treated each auxiliary component merely
*intersecting* an exceptional cycle as an independent exchange location.
That fails when the cycle crosses components. The support (2) consumes all
those locations together; disjoint support is the sufficient condition.

## A connected physical family beyond the earlier global tests

For every integer $r\ge1$, use $r$ blocks of twenty indices. Below numbers
are local to one block, with an offset $20i$ in block $i$. Put

$$
\begin{aligned}
 P={}&\{(0,2),(1,3),(5,7),(6,8),(4,10),(9,11),\\
       &\qquad (12,14),(13,15),(16,18),(17,19)\},\\
 Q={}&\{(0,3),(1,2),(5,8),(6,7),(4,13),(15,12),(9,16),(18,17)\}.
\end{aligned}
$$

Pairs denote unordered edges. Physical colour is the parity of the local
index. The owner graph has local cycles

$$
 C_{10}(0,1,\ldots,9),\qquad C_4(12,13,14,15),\qquad C_4(16,17,18,19)
$$

and the $r$ cross-block owner edges

$$
 (20i+10)\,(20(i+1\bmod r)+11).                         \tag{4}
$$

These edges are disjoint $P_2$ owner components. All physical colour and
matching requirements hold. The auxiliary components in each block are

$$
 C_4(0,2,1,3),\quad C_4(5,7,6,8),\quad
 P_6(10,4,13,15,12,14),\quad P_6(11,9,16,18,17,19).
$$

The resulting physical graph has $50r$ vertices, minimum degree two and
maximum degree three. Each block without the owner edges (4) is connected:
its ten owner-cycle vertices connect the first ten witness indices, and
the remaining helper, witness and owner vertices attach through the two
listed paths and their local owner cycles. Both port owners 10 and 11
belong to this component. Edges (4) join these connected blocks in a
cycle, proving connectedness. No two-connectivity claim is made.

Start with the following local omissions in every block:

$$
 U_*\cap\text{block}=\{0,2,5,7,12,14,16,18\}.            \tag{5}
$$

This is minimum on every owner component: four omissions on the $C_{10}$,
two on each $C_4$, none on the $P_2$'s. Thus $m=8r$ and every auxiliary
component contains exactly two omissions, so $o=0$.

There are two useful packings. The $r$ owner ten-cycles touch four
auxiliary components each. Their supports are disjoint, so (3) gives
cost at most $3r$. This is a genuine cross-component application of the
local exchange and is enough for $\beta_I\ge27r\ge\lceil80r/3\rceil$.
Alternatively the $2r$ owner four-cycles each fit in its own auxiliary
six-path. Packing them gives the stronger cost bound $2r$, and hence
$\beta_I\ge28r$.

For $r\ge2$ the earlier global criteria all fail:

- $A$ is not a union of squares.
- Owner ten-cycles exclude the owner-square/path/$6k$ class; there is more
  than one exceptional cycle.
- $\beta_2(B)=12r<2\lceil20r/3\rceil-2$.
- Every specified owner matching has exactly $r$ obstructing $K_4$'s.
  On each owner ten-cycle the phase starting at 0 supplies the two missing
  diagonals of the first auxiliary square; the opposite phase supplies
  those of the second. The other square fails, and no six-path can supply
  an auxiliary square. Thus no specified choice has at most one $K_4$.

This demonstrates a new sufficient construction beyond these *global
tests*. It is not a claim of external priority or of inability to derive
individual instances by other decomposition arguments.

The budget is not asserted sharp on this family. In fact there is an
explicit zero-cost minimum omission set in every block:

$$
 U^0=\{0,1,4,7,14,15,16,17\}.                            \tag{6}
$$

It is auxiliary-independent. Its owner complement consists of the three
edges $23,56,89$ on the ten-cycle, one edge on each four-cycle, and the
cross-block owner edges (4). These components do not interact. Hence (6)
is permitted and (1) gives the exact value

$$
 \boxed{\beta_I=30r.}                                    \tag{7}
$$

The upper bound follows from the universal all-helper cap $3b$, not
finite computation. This family proves applicability; it does not improve
the unrestricted star-forming gap coefficient.

## A precise obstruction to counting every eligible cycle independently

Use the previously proved two-connected family $H_r$ in
[the maximum-witness note](CONNECTED_MAXIMUM_WITNESS_LOSS.md):
$N=8r$, $A=C_{8r}$, $B$ consists of $2r$ owner four-cycles, and

$$
 \beta_I(H_r)=11r+\lfloor r/2\rfloor.
$$

Take any minimum owner omission set: $m=4r$, and the single auxiliary
component has an even count. Every one of the $2r$ owner cycles is eligible,
but every support equals the same singleton. A legal support packing has
size at most one. If one incorrectly granted a saving to every eligible
cycle, the proposed bound would be $m/2-2r=0$. Equation (1) and the exact
family theorem instead give

$$
 \boxed{\min_U\nu(A[U])=\lceil r/2\rceil>0.}              \tag{8}
$$

Thus the overstatement grows without bound. The failed rule is independent
per-cycle credit, not (3) or the physical $8b/3$ target. Generality in (8)
comes from the existing all-$r$ proof, not from new finite enumeration.

## Exact search for the existential one-K4 criterion

The prior implementation accepts a specified owner matching. The new
wrapper decides whether *some* specified matching has at most one bad
square. The existing 2SAT formula has one avoidance clause per auxiliary
square, including repeated or empty clauses. Solve the whole formula,
then solve each formula with one clause omitted. Any returned assignment
violates at most that omitted clause. Conversely an assignment with at
most one bad square satisfies one of these formulas. This is an exact
polynomial decision for the specified alternating/square-diagonal family;
it says nothing about arbitrary owner matchings. The physical repair is
then performed by the prior theorem. Separate contradiction paths are
returned when all the formulas fail.

## Evidence and remaining questions

`develop/component_omission_budget.py` implements (3), the connected family,
and the existential 2SAT wrapper. The checker verifies physical sets and
support ownership, uses literal matching recurrence on small instances,
and enumerates small phase assignments and coloured packing subsets. Its
report and the independent review state their exact scopes.

The general physical $8b/3$ inequality, the sharp subcubic coefficient,
and the arbitrary-width grid $5/6$ and triple-equality questions remain
open. The theorem gives a safe simultaneous exchange rule; it does not
prove that a large enough support packing always exists, nor that the
budget in (3) is generally attained with equality. No Lean execution is
claimed, and the October submitted manuscript is unchanged.
