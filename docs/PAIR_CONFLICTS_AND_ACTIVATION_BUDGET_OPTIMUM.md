# Pair conflicts determine the best activation-support budget

For a fixed initial omission set, simultaneous activation-support exchanges
admit an exact conflict-graph description. Their best numerical budget is
the initial matching cost minus a maximum independent-set size. This gives
a polynomial sufficient certificate by greedy colouring and also identifies
an obstruction: a two-connected physical family has conflict graph $K_r$,
best activation budget $r-1$, and true minimum cost zero.

## Setup

Use the physical helper--witness--owner model of the
[activation theorem](ACTIVATED_AUXILIARY_SUPPORT_BUDGET.md). There are $b$
helpers, $N=2b$ witness/owner indices, and $5b$ physical vertices. The
auxiliary graph $A=P\cup Q$ is bipartite of maximum degree two: $P$ is a
perfect matching joining equal physical colours and $Q$ is a partial
matching joining opposite colours. The owner graph $B$ joins opposite
colours and has maximum degree two. An omission set $U$ is permitted if
$B[V\setminus U]$ has maximum degree at most one. The exact objective is

$$
 \beta_I=3b-\min_{U\text{ permitted}}\nu(A[U]).             \tag{1}
$$

Fix any permitted $U_*$, including one of nonminimum cardinality. Write
$m=|U_*|$, let $L_1,\ldots,L_s$ be the components of $A[U_*]$, let $o_0$
count the odd $|L_j|$, and put

$$
 \nu_0=\nu(A[U_*])=\sum_j\lfloor|L_j|/2\rfloor
                  =\frac{m-o_0}{2}.                     \tag{2}
$$

The equality uses that every component is a path or even cycle.
Candidate cycles are all owner components $C$ of exceptional length
($6\nmid|C|$) such that $|U_*\cap C|=\lceil|C|/3\rceil$.
Different candidates are vertex-disjoint. For each candidate define

$$
 W_C=U_*\cup C,\qquad
 R_C=\bigcup\{K:K\text{ a component of }A[W_C],\ K\cap C\ne\varnothing\}.
                                                               \tag{3}
$$

Call a candidate individually eligible when every component in (3) has
even initial count $|K\cap U_*|$. Let

$$
 d_C=\#\{j: L_j\subseteq R_C,\ |L_j|\text{ odd}\}.         \tag{4}
$$

Call it good when $d_C=0$. Every good candidate is individually eligible:
its activated components contain unions of entire even base components,
and the newly activated vertices have initial count zero.

Define the conflict graph $\Gamma$ on all candidates. Distinct $C,D$ are
adjacent when some component of $A[U_*\cup C\cup D]$ touches both.
Let $\Gamma_0$ be the induced graph on good candidates.

## Pairwise compatibility is exact

The following observation uses any finite simple graph $A$, any set $U_*$,
and any disjoint nonempty candidate sets. It does not require the matching
or physical hypotheses.

**Lemma.** For a selected candidate family $\mathcal S$, set
$W_{\mathcal S}=U_*\cup\bigcup_{C\in\mathcal S}C$.
No component of $A[W_{\mathcal S}]$ touches two selected candidates if and
only if $\mathcal S$ is independent in $\Gamma$. When this holds, every
component touching a selected $C$ is exactly a component touching $C$ in
$A[W_C]$. Consequently all its initial parity counts agree.

**Proof.** Necessity follows from inclusion of the two-candidate graph in
the common graph. For sufficiency, suppose a path in the common graph
touches two different selected sets. Scan its vertices that belong to any
selected set, recording their unique labels. There is a consecutive pair
of recorded vertices with different labels $C,D$. Every internal vertex
on the subpath between them lies in no selected set. It therefore lies
in $U_*$. The subpath is present in $A[U_*\cup C\cup D]$, producing a
conflict. This argument permits repeated appearances of the same label
and candidate vertices that were already in $U_*$.

If the supports are disjoint, a common component touching $C$ contains no
vertex of another selected candidate. It is therefore contained in $W_C$.
The reverse inclusion for its $A[W_C]$ component follows by monotonicity.
This proves component equality and the parity statement. ∎

The graph can be computed from the individual regions: $C,D$ conflict
exactly when $R_C\cap R_D\ne\varnothing$ or an $A$-edge joins $R_C$ and
$R_D$. Either condition joins the two sets in their pair graph. Conversely,
the consecutive-label subpath from the proof either is a direct edge,
or its internal vertices lie in one component of $A[U_*]$ reached from
both sets, hence included in both regions. This gives a polynomial pair
test without enumerating candidate subsets.

## Parity penalties and the best possible budget

**Theorem.** If $\mathcal S$ is an independent family of individually
eligible candidates, then every $d_C$ in the family is even and a
permitted set $U$ of cardinality $m$ can be constructed with

$$
 \boxed{\nu(A[U])\le
 \nu_0-\sum_{C\in\mathcal S}(1-d_C/2).}                 \tag{5}
$$

In particular, $t$ independent good candidates save at least $t$ matching
edges relative to the **actual** initial matching cost $\nu_0$.

**Proof.** Apply the activation theorem with $W=W_{\mathcal S}$.
The lemma preserves each individual region $R_C$. Distinct regions are
disjoint and have no auxiliary edge between them in this common graph.
Every base component meeting a region is wholly contained there. Initial
regional count is even by eligibility; its parity is also the parity of
$d_C$, so $d_C$ is even.

Every added vertex in $W_{\mathcal S}\setminus U_*$ belongs to its chosen
cycle and hence to an allocated region. Thus unassigned common components
are unchanged base components. Allocated components all have even initial
counts, so their contribution removes exactly $\sum_Cd_C$ odd base
components. Hence $o_W=o_0-\sum_Cd_C$. Substituting in
$(m-o_W)/2-|\mathcal S|$ and using (2) proves (5). The activation theorem
constructs the actual owner and witness sets. ∎

This accounts for a parity cost that an independent per-cycle allowance
would miss: an eligible cycle consuming two odd base components has
$d_C=2$ and no guaranteed gain relative to $\nu_0$. Four odd components
give a negative numerical gain. Neither is an extra positive credit.

There is also an exact optimum statement for this sufficient method.
Consider **all** choices of a candidate subfamily $\mathcal S$ and all
sets $W\supseteq U_*\cup\bigcup\mathcal S$ satisfying the activation
theorem: its full supports are disjoint and every touched component has
even initial count. Let $o_W$ count odd initial counts in components of
$A[W]$. The minimum numerical right side supplied by that theorem is

$$
 \boxed{\min_{\mathcal S,W}
 \left\{\frac{m-o_W}{2}-|\mathcal S|\right\}
       =\nu_0-\alpha(\Gamma_0).}                         \tag{6}
$$

Here $U_*$ is fixed. The empty subfamily and $W=U_*$ are allowed.
Equation (6) optimizes this bound, not the true matching cost over all
permitted omission sets.

**Proof of (6).** A maximum independent good family and its minimal common
activation attain the right side by (5). Conversely take any admissible
$(\mathcal S,W)$ and its allocated regions $R'_C$. Let $d'_C$ count odd
base components in $R'_C$. Every $d'_C$ is even, because its regional
initial count is even. Outside all allocated regions, components of
$A[W]$ can merge base components but cannot split them. Each odd resulting
component contains at least one odd base component, so

$$
 o_W\le o_0-\sum_{C\in\mathcal S}d'_C.
$$

Consequently

$$
 \frac{m-o_W}{2}-|\mathcal S|
 \ge\nu_0+\sum_{C\in\mathcal S}(d'_C/2-1)
 \ge\nu_0-z,
$$

where $z$ counts chosen cycles with $d'_C=0$. The minimal region $R_C$
is contained in $R'_C$, so each of those $z$ cycles is good. They are
pairwise nonconflicting: their two-candidate graphs lie inside $A[W]$,
whose full supports are disjoint. Thus $z\le\alpha(\Gamma_0)$, proving
the lower bound in (6). ∎

No polynomial maximum-independent-set algorithm is asserted. A constructive
sufficient corollary is immediate. If $q$ candidates are good and
$\Delta$ is the maximum degree of $\Gamma_0$, greedy colouring uses at
most $\Delta+1$ colours, one of whose classes has at least
$\lceil q/(\Delta+1)\rceil$ vertices. Therefore

$$
 \nu(A[U])\le\nu_0-\left\lceil\frac q{\Delta+1}\right\rceil,
 \qquad
 \beta_I\ge3b-\nu_0+\left\lceil\frac q{\Delta+1}\right\rceil. \tag{7}
$$

For $q=0$ the saving is zero. In particular, this certifies the $8b/3$
target when the cost bound in (7) is at most $\lfloor N/6\rfloor$.

## Automatic recovery on the mixed long-cycle family

In the earlier $60r$-vertex family, the prescribed $U_*$ has five
two-vertex base components per block, so $\nu_0=5r$. All four owner
cycles per block are good. Label them $X$ (the ten-cycle), $L,R$ (the
two squares on indices 12 through 19), and $G$ (the last gadget square).
The conflict edges in each block are exactly

$$
 XL,\quad XR,\quad GL,\quad GR.
$$

To see this directly, the only auxiliary connections between these
different candidate cycles are $4\!:\!13$ and $9\!:\!16$ for $X$,
and $14\!:\!20$ and $19\!:\!23$ for $G$; contracting the initially
selected two-vertex components introduces no further pair. The port
indices 10,11 are absent from the initial omissions and from every
candidate cycle, so blocks do not conflict across their port edges.
Thus $\Gamma_0=rC_4$ and $\alpha(\Gamma_0)=2r$. Equations (5),(6)
recover the budget $3r$ automatically. The documented deterministic
greedy colouring uses two colours and also selects $2r$ cycles.
This rederives the previous family's bound; the new result is the exact
pair criterion, the general parity formula and optimization identity.

## A two-connected obstruction with an arbitrarily large budget gap

For each even $r\ge2$, use $N=4r$ indices, $b=2r$ helpers, and

$$
 P=\{(2i,2i+1):0\le i<2r\},\qquad
 Q=\{(2i+1,2i+2\bmod4r):0\le i<2r\}.
$$

Thus $A=C_{4r}$. The physical colour of index $v$ is
$\lfloor v/2\rfloor\bmod2$. For $0\le i<r$, put $\pi(i)=i\mathbin{\mathrm{xor}}1$,
the permutation swapping consecutive pairs $0,1$; $2,3$; and so on.
Define the owner square

$$
 C_i=(2i,\ 2r+2\pi(i),\ 2i+1,\ 2r+2\pi(i)+1).           \tag{8}
$$

These squares partition all indices. The pair $2i,2i+1$ has physical
colour $i\bmod2$; since $r$ is even, the pair beginning at
$2r+2\pi(i)$ has the opposite colour. The displayed cyclic order
therefore alternates colours, so $B$ is physical. All helpers have
degree two, and every witness and owner
has degree three. The physical order is $10r$.

The witness/helper core is the cycle obtained from $A$ by subdividing
every $P$ edge with its helper. Each owner square attaches to this core
through four distinct witness--owner edges. The physical graph is
two-connected. Indeed, deleting a core vertex leaves a connected core
path, and every intact owner square retains at least three attachments.
Deleting an owner leaves a connected three-vertex owner path with three
attachments, while the core remains a cycle. In both cases the whole
remaining graph is connected. This proves the claim for every vertex
deletion and every even $r\ge2$.

Set

$$
 U_* = \{0,1,\ldots,2r-1\}.                             \tag{9}
$$

It omits the first consecutive base-index pair in each owner square, so
its owner complement consists of two isolated vertices per square. It is
minimum on every square: retaining three square vertices gives degree two.
The base graph $A[U_*]$ is a single even path, giving $\nu_0=r$.
Every cycle's individual region touches this same path, and no odd base
component exists. Thus all $r$ candidates are good and

$$
 \Gamma_0=K_r,\qquad\alpha(\Gamma_0)=1.
$$

The best numerical activation-support budget over **every admissible
common $W$ and candidate family**, with initial (9) fixed, is therefore

$$
 \boxed{r-1}.                                          \tag{10}
$$

There is also an exact statement about one owner exchange. If only square
$C_i$ changes, the other $r-1$ original $P$ edges inside $U_*$ remain
as a matching, so the resulting cost is at least $r-1$. The local
activation construction attains at most $r-1$. Therefore the exact
minimum after one such owner-component change is $r-1$.

On the other hand, let

$$
 U^0=\{0,2,4,\ldots,4r-2\}.
$$

This is auxiliary-independent and still minimum on each owner square.
The two remaining vertices in each square are the two odd indices, an
owner edge by (8). Hence $U^0$ is permitted and

$$
 \boxed{\min_U\nu(A[U])=0,\qquad \beta_I=6r}.            \tag{11}
$$

The upper cap $3b=6r$ follows from (1), or from the fact that a selected
witness excludes its owner when all helpers are retained. Thus the gap
between the best activation budget for (9) and the true cost is $r-1$,
unbounded even under two-connectivity and minimum degree two. For even
$r\ge4$, budget (10) exceeds $\lfloor N/6\rfloor=\lfloor2r/3\rfloor$.

This falsifies the rule “optimizing the activation-support budget for any
fixed minimum omission set always reaches the physical $8b/3$ target.”
It does not falsify that target: the explicit independent set gives a
stronger value. Nor does it exclude changing the initial set, coordinated
changes on conflicting cycles, or repeated reconstruction after an exchange.
All-owner squares were already covered by the earlier label theorem.

## Evidence and remaining problem

The constructor computes the conflict graph, base parity penalties, greedy
colour classes and an actual physical certificate. The checker tests the
pairwise lemma on arbitrary small graphs, then checks physical matching
costs and explicit all-parameter families independently. Small slices
enumerate candidate subsets and supersets $W$ to compare (6); large
instances audit supplied certificates, not unrestricted optima.

The next mathematical step is compatible **coordinated** exchanges when
the conflict graph is dense. The exact obstruction above shows why
independent support selection alone cannot complete the general $8b/3$
argument. The unrestricted subcubic sharp coefficient and the general
grid Hall-completion, unit-$5/6$ and triple-equality problems remain open.
