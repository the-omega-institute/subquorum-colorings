# An unbounded plateau for strictly improving owner exchanges

For every integer $m\ge1$, there is a two-connected bipartite physical graph
on $20m$ vertices, of minimum degree two and maximum degree three, with a
minimum-cardinality permitted omission $U$ such that:

$$
 \nu(A[U])=m,\qquad \min_{W\text{ permitted}}\nu(A[W])=0.
$$

Every legal one-vertex replacement within one owner component has cost at
least $m$. Moreover, every nonempty cardinality-preserving exact-deletion
batch with final-isolated additions is impossible, even if all minimum covers
and arbitrary replacement points are allowed. The best certificate cost is
therefore $m$, while the true all-helper cost is zero. An explicit route has
$m$ neutral and $m$ decreasing steps, in every ordering of its operations.
Among nonincreasing single-replacement routes to zero, $m$ neutral steps are
necessary and sufficient.

## Coordinates and physical hypotheses

Use $N=8m$ indices, $b=4m$. In each eight-index block $j$, write
$v_{j,t}=8j+t$, with block labels modulo $m$. The auxiliary graph is the
single cycle $A=C_{8m}$, with

$$
 P=\{(2i,2i+1):0\le i<4m\},\qquad
 Q=\{(2i+1,2i+2\bmod8m):0\le i<4m\}.
$$

Give index $v$ physical colour $\lfloor v/2\rfloor\bmod2$. The two
owner squares per block, in cyclic order, are

$$
 L_j=(v_{j,0},v_{j,6},v_{j,1},v_{j,7}),\qquad
 R_j=(v_{j,2},v_{j,4},v_{j,3},v_{j,5}).                    \tag{1}
$$

They partition all indices and alternate physical colours. The physical
graph consists of the helper subdivisions of $P$, witness edges $Q$,
indexwise witness--owner attachments and owner squares (1). It has order
$5b=20m$, helper degree two and witness/owner degree three. Its witness/helper
core is a subdivided cycle. Deleting a core point leaves a connected path
with at least three attachments per owner square; deleting an owner leaves
an owner path with three attachments to the intact core. Thus it is
bipartite and two-connected at every scale.

Set

$$
 U=\bigcup_j\{v_{j,1},v_{j,2},v_{j,3},v_{j,6}\}.
$$

There are exactly two omissions per owner square, the minimum needed for
its retained subgraph to have maximum degree at most one. Thus $U$ is
minimum-cardinality permitted. The auxiliary graph on $U$ is $m$ copies
of $P_3$ and $m$ isolates, with

$$
 \nu_0=m,\qquad C=\{v_{j,2}:0\le j<m\}.                  \tag{2}
$$

Its minimum cover $C$ is unique: each three-vertex path has only its middle
vertex as a minimum cover, and isolates contribute nothing.

## No positive exact-deletion batch, and no improving local exchange

Every point outside $U$ has an initial neighbour in $U\setminus C$:

$$
 v_{j,0}\sim v_{j,1},\quad v_{j,4}\sim v_{j,3},\quad
 v_{j,5}\sim v_{j,6},\quad v_{j,7}\sim v_{j,6}.           \tag{3}
$$

A deletion set contained in a minimum cover must be a subset of the unique
$C$. The neighbours in (3) therefore persist after every such deletion.
No point outside $U$ can become an isolated addition. Any nonempty equal-size
replacement needs at least one addition, so no nonempty batch satisfies the
exact-deletion plus final-isolation rule. The empty batch attains cost $m$.
This argument even allows arbitrary $X,Y$ without the owner restriction.

For a single legal within-owner replacement, if the removed point is outside
$C$, deleting it leaves matching cost $m$: removing an endpoint from $P_3$
or an isolate loses no matching edge. Adding a point cannot lower that cost.
If the removed point is $v_{j,2}\in C$, the only same-owner additions are
$v_{j,4}$ and $v_{j,5}$. They create, respectively, the edges
$v_{j,3}v_{j,4}$ and $v_{j,5}v_{j,6}$. Either is disjoint from a size
$m-1$ matching on the other blocks, so final cost is again at least $m$.
This proves an actual local minimum for all such single replacements, not
merely failure of their cover certificates.

## Exact optimum and optimal nonincreasing route

The even-index omission $E$ is independent in $A$ and permitted: each owner
square retains its two odd indices, an owner edge. It gives zero cost and
hence the exact all-helper value

$$
 \boxed{\beta_I=3b=12m}.                                 \tag{4}
$$

Change $U$ to $E$ by the following operations on distinct owner components:

$$
 L_j:\ v_{j,1}\mapsto v_{j,0},\qquad
 R_j:\ v_{j,3}\mapsto v_{j,4}.                            \tag{5}
$$

Every prefix in any order remains permitted. No cross-block auxiliary edge
has both endpoints selected along this route, because $v_{j,7}$ is never
selected. In each block the four possible route states are

| Operations completed | Selected local indices | Matching cost |
| --- | --- | --- |
| Neither | $1,2,3,6$ | 1 |
| Only $L_j$ | $0,2,3,6$ | 1 |
| Only $R_j$ | $1,2,4,6$ | 1 |
| Both | $0,2,4,6$ | 0 |

Thus the first operation in each block is neutral and the second decreases
cost by one. Every permutation of all $2m$ operations has exactly $m$
neutral steps, $m$ decreasing steps and no increases.

This is optimal among nonincreasing single-replacement routes to zero. A
zero-cost omission of the preserved size $4m$ must be one of the two maximum
independent sets $E,O$ of $C_{8m}$. Each block of $U$ contains two indices
of each parity, so $|U\setminus E|=|U\setminus O|=2m$. Any such route
therefore needs at least $2m$ replacements. A single replacement changes
matching number by at most one. On a nonincreasing route from $m$ to zero,
exactly $m$ steps decrease it; all further steps are neutral, giving at least
$m$ neutral steps. Route (5) attains this number.

The nonincreasing qualification matters: if cost increases are allowed, the
counting relation is $L=m+2i+z$, so extra increasing/decreasing pairs can
replace neutral steps. No lower bound of $m$ on neutral steps is asserted
for arbitrary routes with increases or for larger batch operations.

## Scope and verification

This is an unbounded limitation of strict local descent and of the exact
one-edge-per-deletion certificate. It does not disprove the physical $8b/3$
target: the initial cost $m$ already lies below its threshold
$\lfloor N/6\rfloor=\lfloor4m/3\rfloor$. Equation (4) concerns the
all-helper optimum, not the unrestricted physical dissociation number.
The general grid and sharp gap questions remain open.

The standalone standard-library checker reconstructs the physical graph,
checks its pointwise deletion connectivity at small scales, enumerates all
five local states per owner for $m=1,2,3$, verifies every legal single-owner
swap, checks all route permutations at those scales, and audits larger
explicit certificates and random orders. It imports no project algorithm.
Independent review returned **ACCEPT**. The reviewer ran the original
checker unchanged with assertions and reproduced its complete report
byte-for-byte. The full response, frozen hashes and actual execution scope
are preserved in [`output/neutral-exchange-plateau-review.json`](../output/neutral-exchange-plateau-review.json). General claims have the proofs above; finite
checks validate the coordinates and implementation. No Lean is used.
