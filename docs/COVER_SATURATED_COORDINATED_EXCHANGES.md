# Cover-saturated coordinated exchanges

A batch of owner exchanges can save several matching edges while all its
operations touch the same auxiliary component. The certificate uses a minimum
vertex cover instead of disjoint activation supports. Each removed cover
vertex owns a different edge of an initial maximum matching. Additions need
only be isolated **after** the whole batch; cyclic dependencies are allowed.
For a fixed cover and a specified compatible candidate list, a dependency
closure finds the unique largest batch satisfying this isolation rule.

## Physical setting and objective

Use the [helper--witness--owner model](PAIR_CONFLICTS_AND_ACTIVATION_BUDGET_OPTIMUM.md).
There are $b$ helpers and $N=2b$ witness/owner indices. $P$ is a perfect
matching on the indices joining equal physical colours; $Q$ is a partial
matching joining opposite physical colours. Assume $A=P\cup Q$ is bipartite
(as in the physical model) and has maximum degree two. The owner graph $B$
has maximum degree two and joins opposite physical colours. An omission set
$U$ is permitted when $B[V\setminus U]$ has maximum degree at most one.
For all-helper dissociation sets the exact objective is

$$
 \beta_I=3b-\min_{U\text{ permitted}}\nu(A[U]).                 \tag{1}
$$

All costs below are unweighted matching cardinalities. Physical colours need
not be a bipartition of $A$: $P$ joins equal physical colours.

## The exact deletion criterion

**Lemma 1.** Let $G$ be any finite bipartite graph and $X\subseteq V(G)$.
Writing $\nu_0=\nu(G)$, the following are equivalent:

$$
 \nu(G-X)=\nu_0-|X|
 \quad\Longleftrightarrow\quad
 X\subseteq C\text{ for some minimum vertex cover }C\text{ of }G.  \tag{2}
$$

Here “minimum” means minimum cardinality, not inclusion-minimal.

**Proof.** Removing $X$ destroys at most $|X|$ edges of a maximum matching,
so $\nu(G-X)\ge\nu_0-|X|$. If $C$ is a minimum cover containing $X$,
König's matching--cover equality gives $|C|=\nu_0$, and $C-X$ covers
$G-X$. Thus the reverse inequality also holds.

Conversely, if equality holds, take a minimum cover $C'$ of $G-X$.
König's equality gives $|C'|=\nu_0-|X|$. The set $C'\cup X$ covers
$G$ and has size $\nu_0$, so it is a minimum cover containing $X$. ∎

The statement concerns a standard consequence of bipartite matching duality;
its use here is to certify coordinated physical exchanges. It imposes no
same-side or component-disjointness condition on $X$. For example, in the
path $0-1-2-3$, $X=\{1,2\}$ belongs to the minimum cover $\{1,2\}$
and saves two edges despite using opposite bipartition sides. By contrast,
$X=\{0,1\}$ saves only one edge. In a three-vertex path, removing an
endpoint saves no edge. Bipartiteness cannot be dropped: in a triangle every
single vertex belongs to a minimum cover, but deleting it leaves a matching
of size one, equal to the original matching size.

There is a useful certificate refinement. For **any** minimum cover $C$ and
**any** maximum matching $M$ of a bipartite graph, every edge of $M$ has
exactly one endpoint in $C$, and $M$ saturates $C$. Indeed, $|M|=|C|$;
every matching edge needs a cover endpoint, and the endpoints are distinct.
An edge with two cover endpoints or an unmatched cover point would exceed
this exact count. Hence the vertices in $X\subseteq C$ charge $|X|$
different matching edges. Deleting these edges from $M$ gives a maximum
matching of $G-X$, certified by the cover $C-X$.

## Exact physical replacement and resource ownership

**Theorem 2.** Fix a permitted $U$ and a minimum vertex cover $C$ of
$A[U]$. Choose operations $(K_i,x_i,y_i)$ such that:

1. The $K_i$ are different connected components of the owner graph $B$.
2. $x_i\in U\cap C\cap K_i$ and $y_i\in K_i\setminus U$.
3. Each local replacement $(U\setminus\{x_i\})\cup\{y_i\}$ is permitted.
4. Put $X=\{x_i\}$, $Y=\{y_i\}$ and $U'=(U-X)\cup Y$.
   There is no $A$-edge between $Y$ and $U-X$, nor within $Y$.

Then, with $t$ operations,

$$
 |U'|=|U|,\qquad U'\text{ is permitted},\qquad
 \boxed{\nu(A[U'])=\nu(A[U])-t}.                         \tag{3}
$$

A maximum matching and minimum cover of $A[U']$, as well as the actual
physical dissociation set, can be returned without a final matching solve.

**Proof.** Different owner components have no $B$-edges between them. On
component $K_i$, the final omission set agrees with its single permitted
local replacement; on every other component it agrees with $U$. This proves
joint permittedness. Distinct components also make the removals and additions
distinct, establishing the cardinality statement.

Condition 4 makes every added point isolated in $A[U']$. Thus $A[U']$
is $A[U-X]$ plus isolated vertices, and Lemma 1 proves (3).
More explicitly, start with any maximum matching $M$ of $A[U]$.
Charge to $x_i$ its unique incident matching edge. These $t$ edges are
all different, even if every operation touches one shared component.
Remove exactly them; the surviving edges form a matching $M'$ on $U'$.
The set $C'=C-X$ covers $A[U']$ and

$$
 |M'|=|C'|=\nu(A[U])-t.
$$

These are matching lower and cover upper certificates. Put $T'=U'\setminus C'$;
this is a maximum independent set of $A[U']$. Select every helper, the
owners indexed by $V\setminus U'$, and the witnesses indexed by $T'$.
A selected owner has no selected witness of its index, and has at most one
selected owner neighbour. A selected witness has its one helper neighbour;
$P$ ensures that no helper has two selected witness neighbours, and $Q$
ensures that no selected witness has a selected witness neighbour.
Consequently this is a physical dissociation set, with size

$$
 b+(2b-|U'|)+(|U'|-|C'|)=3b-\nu(A[U])+t.                 \tag{4}
$$

Each saving is owned by a distinct initial matching edge. There is no
per-component credit that could be counted again for another operation. ∎

The cover condition is exact for the **deletion** rule. The isolation and
one-operation-per-owner hypotheses are sufficient restrictions for this
replacement method, not necessary conditions for every cost-saving exchange.
If one allows several operations in one owner component, their joint owner
permittedness must instead be checked explicitly. Individual checks alone do
not suffice: on the owner cycle $0-1-\cdots-7-0$, take $U=\{0,2,5\}$.
The swaps $0\mapsto7$ and $2\mapsto3$ are each permitted; together they
leave the retained owner path $0-1-2$, which is not dissociation.
Isolation also matters: for $A=0-1-2-3$, $U=\{0,1\}$ and $C=\{0\}$,
replacing $0$ by $2$ leaves the edge $1-2$ and saves nothing.

## Largest dependency-closed batch for a fixed cover

**Theorem 3.** Fix $U,C$ and a list of candidate operations satisfying
conditions 1--3 of Theorem 2, with all candidate additions pairwise
$A$-nonadjacent. Define a directed dependency graph on candidate labels:

$$
 i\longrightarrow j \quad\text{if } y_i x_j\in E(A).
$$

Call a label permanently blocked when $y_i$ has an $A$-neighbour in
$U\setminus\{x_j:\text{all candidates }j\}$. Let $R$ consist of every
blocked label and every label that can reach a blocked label by directed
dependencies. Then

$$
 \boxed{S_{\max}=\{\text{all candidate labels}\}\setminus R}    \tag{5}
$$

is the unique largest batch satisfying final isolation. It contains every
feasible batch, attains the largest possible saving under this rule, and
is computable by reverse reachability. The certificate in Theorem 2 gives
cost exactly $\nu_0-|S_{\max}|$.

**Proof.** For a chosen subset $S$, all chosen additions remain independent.
The only obstruction to isolation of $y_i$, $i\in S$, is an initial
neighbour that was not removed. If the neighbour is $x_j$ this says that
$j$ must also belong to $S$; otherwise $i$ is permanently blocked.
Therefore $S$ is feasible exactly when it is closed under all outgoing
dependencies and contains no blocked label. No such $S$ can contain a
label reaching a blocker. Conversely, the complement of $R$ contains no
blocker and is closed: an edge from it into $R$ would itself give a path
to a blocker. Hence it is feasible and includes every feasible subset. ∎

For a fixed candidate list the adjacency scan and reverse reachability
are polynomial (linear after the graphs and minimum cover are supplied).
The theorem does not optimize over covers, alternative replacement choices,
conflicting additions, or multiple operations on one owner component.
Directed cycles require no special tie-breaking: a cycle without a path
to a blocker can be selected in its entirety.

## Cyclic dependencies with an unbounded advantage over support budgets

For every integer $r\ge3$, let $N=4r$, $b=2r$. In block $i$, indices
modulo $r$, write

$$
 z_i=4i,\quad x_i=4i+1,\quad y_i=4i+2,\quad w_i=4i+3.
$$

Set

$$
 P=\{z_ix_i,y_iw_i:0\le i<r\},\qquad
 Q=\{x_iy_i,w_iz_{i+1}:0\le i<r\}.
$$

Thus $A=C_{4r}$. Give $z_i,x_i$ physical colour zero and $y_i,w_i$
physical colour one. Let the owner components be the squares in cyclic order

$$
 K_i=(x_i,y_{i+1},z_i,w_{i+1}).                            \tag{6}
$$

They partition the indices and alternate physical colours. There are $10r$
physical vertices, each of degree two or three. The physical graph is
two-connected: its witness/helper core is the $A$ cycle with every $P$ edge
subdivided by its helper. Deleting a core vertex leaves a connected core
path; each intact owner square retains at least three attachments. Deleting
an owner leaves a three-vertex owner path with three attachments to the
intact core. In either case the remaining physical graph is connected.

Take

$$
 U=\{z_i,x_i:0\le i<r\},\qquad C=\{x_i:0\le i<r\}.
$$

The induced graph $A[U]$ is $r$ disjoint edges $z_ix_i$, so $C$ is a
minimum cover and $\nu_0=r$. On every owner square the omission has minimum
size two; its complement consists of **two isolated vertices**.
Consider one operation per owner:

$$
 x_i\longmapsto y_{i+1}.                                \tag{7}
$$

Its local complement is the edge $x_iw_{i+1}$, hence it is permitted.
The additions are independent, and the only initial neighbour of $y_{i+1}$
is $x_{i+1}$. Therefore the dependency graph is exactly the directed cycle
$i\to i+1$. The empty set and the full set are its only closed subsets.
No nonempty proper subset of (7) satisfies final isolation, while the whole
batch does. The final omission set is

$$
 U'=\{z_i,y_i:0\le i<r\}=\{0,2,\ldots,4r-2\},
 \qquad \nu(A[U'])=0,\qquad\boxed{\beta_I=6r}.             \tag{8}
$$

The equality uses the upper cap $3b$ from (1). This does not say that an
individual swap cannot reduce actual cost: it says it fails the specified
isolation test, so this exact certificate needs the closed batch.

There is an exact comparison with the previous activation-support method
for this **same initial $U$**. Its base components are the even edges
$L_i=\{z_i,x_i\}$. The individual activated region for $K_i$ is

$$
 R_i=L_i\cup L_{i+1}\cup L_{i+2}\cup\{y_{i+1},w_{i+1}\}.
$$

All candidates are good. Two regions conflict precisely when their labels
have cyclic distance at most two: shared base edges give distance one or
two, and the displayed regions have no further inter-region edge at larger
distance. Thus $\Gamma_0=C_r^2$ (complete for $r=3,4,5$).
An independent family occupies disjoint cyclic intervals of three labels,
so its size is at most $\lfloor r/3\rfloor$. Selecting labels
$0,3,\ldots,3(\lfloor r/3\rfloor-1)$ attains that value. The previous
[all-activation optimum identity](PAIR_CONFLICTS_AND_ACTIVATION_BUDGET_OPTIMUM.md)
therefore gives the exact best numerical support budget

$$
 \boxed{r-\lfloor r/3\rfloor=\lceil2r/3\rceil}.            \tag{9}
$$

In contrast the coordinated certificate gives actual cost zero. The
advantage is unbounded. When $3\nmid r$, budget (9) even exceeds the
$8b/3$ cost threshold $\lfloor N/6\rfloor=\lfloor2r/3\rfloor$ by one.
This demonstrates a stronger fixed-initial certificate, not a newly settled
universal class: all-owner squares already satisfy the earlier global label
theorem. Equation (8) is the all-helper optimum, with no claim of exact
unrestricted physical dissociation number.

## Arbitrarily many savings in one shared odd component

In the previous [clique family](PAIR_CONFLICTS_AND_ACTIVATION_BUDGET_OPTIMUM.md),
for even $r\ge4$, use $A=C_{4r}$ and owner squares

$$
 K_i=(2i,2r+2(i\mathbin{\mathrm{xor}}1),2i+1,
             2r+2(i\mathbin{\mathrm{xor}}1)+1).
$$

Put $U_1=\{1,\ldots,2r-1\}\cup\{2r+2\}$. This is permitted and
minimum on every square. Its auxiliary graph is the odd path on
$1,\ldots,2r-1$ plus the singleton $2r+2$, with cost $r-1$.
The minimum cover of the path is

$$
 C=\{2,4,\ldots,2r-2\}.
$$

For each $j=2,\ldots,r-1$, replace

$$
 2j\longmapsto2r+2(j\mathbin{\mathrm{xor}}1).               \tag{10}
$$

Each operation belongs to a different square. Its remaining two owners form
an edge. The added even indices lie between $2r+4$ and $4r-2$, are mutually
nonadjacent, and have no initial neighbour in $U_1$. Thus every subbatch
satisfies isolation. The removals $\{4,6,\ldots,2r-2\}$ form a
**subset**, not all, of $C$. Theorem 2 gives exact cost $r-1-t$ after
any $t$ of these operations, and cost one after all $r-2$ operations.
All removals lie on the same odd base path. Every exceptional owner square
touches this odd path, so there are no good candidates for $U_1$ and the
previous best numerical activation budget is still $r-1$. The new method
handles a shared odd component that contributes no positive support credit.
This cost-one result is for the displayed batch, not a proof that the
unrestricted optimum is one; the same physical family has a separate
cost-zero omission set.

## Verification and scope

`develop/cover_saturated_exchange.py` constructs the cover, distinct matching
charges, surviving matching and final physical set. Its fixed-cover dependency
routine returns both the selected labels and permanent-blocker propagation.
The independent checker enumerates matchings and vertex covers on small
bipartite graphs, checks the replacement criterion, directly reconstructs
physical graphs, enumerates feasible candidate subbatches, checks both families,
and tests failure of the omitted hypotheses. Large controls verify explicit
primal/dual certificates; they do not enumerate unrestricted large optima.
The report records the exact enumeration scope and counts. Independent review returned **ACCEPT**. The reviewer ran the original
checker unchanged with assertions and reproduced its complete report
byte-for-byte. The full response, frozen hashes and actual execution scope
are preserved in [`output/cover-saturated-exchange-review.json`](../output/cover-saturated-exchange-review.json). No Lean execution is used.

The remaining mathematical task is to choose minimum covers and candidate
operations together when additions conflict or several changes share one owner.
The sharp unrestricted subcubic coefficient, the general physical $8b/3$
certificate, general grid multi-Hall completion, unit-$5/6$ and arbitrary-width
rectangular-grid triple equality remain open in the full active objective.
