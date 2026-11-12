# Mixed isolated-addition repair: exact costs and an operation-count barrier

Allowing removals on both sides of the initial cover retains an exact
endpoint cost and a constructive final cover. Maximum saving remains
tractable with a conflict-cover parameter. The minimum-operation tie-break,
however, is NP-complete even in a tightly restricted physical family with
no conflicts. This distinguishes two algorithmic questions that coincide
in the preceding outside-cover grouped-budget theorem.

The matching identities are elementary path facts. The complexity statement
below is a self-contained reduction from the classical NP-completeness of
Vertex Cover; no literature-priority claim is made for the reduction or its
restrictions. It concerns a fixed starting state and candidate list, not the
complexity of the unrestricted graph parameters or general grid equality.

## 1. Exact endpoint repair without an initial-cover restriction

Let A be a finite simple graph and U an initial omission set. Assume G=A[U]
is bipartite with maximum degree at most two. Each candidate i removes a
different point x_i in U and adds a different y_i outside U. Both sides of
any initial minimum cover may contain removals. For selected labels S put
X={x_i:i in S}, Y={y_i:i in S}, and U_S=(U-X) union Y. Require every new point
to be isolated in A[U_S].

Let o0 be the number of odd-order initial components, counting isolated
points. Let oX be the number of odd-order components of G-X, again counting
isolates. All cycles here are even, so these odd components are paths.
The count oX excludes the newly added isolates Y.

**Theorem 1 (mixed endpoint formula).** With nu0=nu(G),

    nu(A[U_S]) = (|U|-|X|-oX)/2,
    nu0 - nu(A[U_S]) = (|X|+oX-o0)/2.

Both expressions are integers. One can construct a final minimum cover and
maximum matching by ordering each remaining path or even cycle, taking
its smaller bipartition side as cover, and pairing consecutive vertices.
No supplied initial independent cover and no final matching optimizer are
required.

**Proof.** A path of order a has matching and cover sizes floor(a/2).
An even cycle has matching and cover sizes a/2. Summing gives
nu(G)=(|U|-o0)/2 and nu(G-X)=(|U|-|X|-oX)/2. The newly added points are
isolated and contribute zero. Consecutive pairing and the smaller sides
supply a matching and cover of the displayed common size, proving both
bounds directly. Deleting points cannot increase matching size, so the
saving is nonnegative. QED.

For any fixed initial maximum matching M0, let L be its edges meeting X.
M0-L survives as a matching of G-X. Hence saving<=|L|, so an injective
ledger can charge each saving to a different edge of L. Unlike the preceding
outside-cover theorem, this is a **global cardinality ledger**: no ownership
by a specific final repair region is asserted. The implementation constructs
a canonical initial M0 and records the first 'saving' destroyed edges.
It does not claim that each destroyed edge earns a saving, nor that this
argument preserves weighted costs or original TH resource routing.

Final isolation is characterized exactly as before: an initial neighbour
x_j of y_i gives i implies j; an initial neighbour unavailable for removal
blocks i; and adjacent additions conflict. These conditions inspect every
possible final edge incident with Y. The formula is an endpoint theorem;
it does not imply a nonincreasing intermediate-cost schedule. Without final
isolation the formula can fail: U={0,1}, initial edge01, operation1->2 and
additional edge02 give final cost1 instead of the predicted0.

## 2. Maximum saving and the separate tie-break

For a feasible batch write v(S)=nu0-nu(G-X). This is monotone under inclusion
of removal labels: deleting more vertices cannot increase the matching size.
The formula of Theorem 1 evaluates it in polynomial time by path components.

**Theorem 2 (parameterized maximum saving).** Given a vertex cover K of the
addition-conflict graph, the greatest saving among all feasible batches can
be found in 2^|K| times polynomial time. This conclusion does not promise
the fewest operations among maximum-saving batches.

**Proof.** For every F subset K, reject internal conflicts, exclude blocked
labels, K-F and conflict neighbours of F, and propagate exclusions backward
through implications. Reject if this excludes a label of F. The remaining
set L is the greatest feasible batch with L cap K=F: implications are
closed, conflicts outside K do not exist, and every conflict touching F
has been excluded. Every feasible batch in that class is a subset of L.
Monotonicity therefore makes L maximum-saving in that class. Compare its
value across assignments. Each evaluation uses Theorem 1. QED.

A greedy maximal conflict matching supplies |K|<=2 tau, giving 4^tau times
polynomial time. With no conflicts this primary optimization is polynomial.
A greatest batch may contain unnecessary neutral operations. Even a single
initial edge01 and isolated replacements0->2,1->3 gives two incomparable
one-operation maximum-saving batches. Their intersection is empty and earns
no saving; their union is maximum-saving but uses two operations. Thus the
unique smallest conditional maximizer of the preceding outside-cover rule
already fails when K is empty and there are no dependencies.

**Theorem 3 (exact SCC enumeration).** Let s be the number of strongly
connected components of the implication graph. Maximum saving followed by
minimum operation count can be solved in 2^s times polynomial time.

**Proof.** A feasible implication-closed batch contains all or none of each
SCC. Enumerate these unions, reject blockers, violated implications and
conflicts, then compare Theorem 1 values and operation counts. Every feasible
batch is enumerated. No polynomial bound in s is claimed. QED.

The code uses iterative Kosaraju traversal. An SCC is an indivisible label
group, not a new independent physical surplus. Edges between SCCs still
impose implications and are checked after enumeration.

## 3. A physical Vertex Cover encoding

Here is the physical model used in the preceding notes. There are N=2b
witness indices, a perfect matching P on them, another matching Q, and owner
edges B with path/even-cycle components. Each P-pair has one centre adjacent
to its two witnesses. Each witness is joined to its own owner; Q-edges join
witnesses and B-edges join owners. Physical witness colours agree on P-pairs
and differ on Q and B edges. Owners and centres receive opposite colours
from their adjacent witnesses. A permitted omission U has owner complement
inducing maximum degree at most one in B. The matching cost is nu((P union Q)[U]);
a tight final cover gives a dissociation set of size 3b-cost with all centres.

**Theorem 4 (exact physical encoding).** For any finite simple H on k>=1
vertices, put D=max(1,Delta(H)) and q=kD. A polynomial construction gives:

- N=4q, b=2q and a physical graph of order10q, bipartite, minimum degree2,
  maximum degree3;
- q square owner components, a minimum-cardinality permitted initial
  omission U, and q individually permitted operations on distinct owners;
- auxiliary A=P union Q consisting only of P4 and P2 components, while A[U]
  is a matching of size |E(H)| plus isolates;
- no addition conflicts or blockers, and exactly k disjoint directed cycles
  of implications, each containing D labels;
- a bijection between final-isolation feasible batches S and subsets Z of
  V(H), with

      |S|=D|Z|,       cost(S)=|E(H-Z)|.

In particular every instance has an attainable maximum saving |E(H)|, and

    minimum operations to attain that saving = D*tau(H).

If H is connected and bridgeless, the physical graph is two-connected.
A single-vertex edgeless H also gives a two-connected physical graph.

**Construction.** Give each v of H a group of D labels: one incidence label
(v,e) for each incident edge e, padded with dummy labels. Each old edge uv
becomes a Q-edge between its two incidence labels; those edges are a
matching. Let the q labels be indexed i. Introduce four witness indices
x_i,y_i,z_i,w_i for each label. The initial omission contains every x_i and
z_i. Candidate i replaces x_i by y_i in its own square owner.

Cyclically order the labels of each v-group. If j follows i, put y_i x_j in
P. Thus final isolation requires i implies j, forming exactly that directed
cycle, including a harmless self implication when D=1. Assign physical
colours to the x-incidences: for old edge uv with u<v, its u-incidence gets0
and its v-incidence gets1. Dummy x's get0. Give y_i the colour of x_j, so
these P-pairs are monochromatic and every Q-edge is bichromatic.

Choose padding colours within each group as follows. If x_i,y_i have the
same colour c, give z_i,w_i colour1-c. If x_i,y_i differ, give z_i,w_i
opposite colours, choosing z-colour0 on half of these indices and1 on the
other half. The number of changes around a cyclic binary word is even,
so this split is possible. Each four-point owner block has two points of
each colour and can be ordered as an alternating square. In each group
the number of z-points of either colour equals the number of w-points of
that colour: equal-colour cases contribute equally, and the unequal cases
have an even half split. Complete P by pairing same-colour z's and w's
**within that group**. Every witness lies in one P-pair, and Q remains a
matching. All colour and owner requirements hold.

Each square has exactly two omitted points. Fewer than two omissions leave
at least a three-vertex owner path of degree2; any two omissions are permitted.
Thus U is minimum-cardinality permitted, every candidate is individually
permitted, and every batch and prefix is permitted regardless of isolation.

Each y_i has exactly one auxiliary neighbour, x_j, so final isolation is
exactly whole-group selection. No y_i is adjacent to another y or padding
point. At a whole-group batch all original P-edges have one endpoint absent;
padding P-edges have z present and w absent. Precisely the old Q-edges with
neither endpoint's group selected survive. They form a matching, giving the
claimed cost and operation count. Each Q-edge together with its two P-edges
is a P4; dummy x's produce P2s, as do padding pairs. This proves all cost,
permission and auxiliary assertions without enumeration.

**Connectivity.** First consider only one group. Its owner squares, original
x/y witnesses and centres for the y_i x_j pairs form a cyclic assembly of
squares connected through two distinct ports per square. This is
two-connected: deleting any internal vertex leaves the cyclic connection
through the other direction, and each square with one vertex removed is
connected and retains at least one attachment. For D=1 it is one square
with an additional path between its distinct x/y owner ports. More formally,
choose one path between the two ports in every square. Together with the
inter-square links these form a cycle; the other port-to-port path of each
square is an ear. A cycle and successive ears with distinct ends are
two-connected.

Each padding P-pair adds a path from its z-owner to its w-owner, with both
ends distinct and in the same group. These paths are further ears and
preserve two-connectivity. Denote the resulting group module by R_v.
The only edges between different modules are Q-edges, one per old H-edge.
Deleting one physical vertex leaves each module connected and destroys at
most one Q-edge, since Q is a matching. When H is connected and bridgeless,
the quotient H with at most one edge removed is connected. All surviving
modules therefore remain connected. This proves two-connectivity.
Centres and non-Q witnesses have degree2, Q witnesses and owners degree3.
The prescribed physical colours prove bipartiteness. QED.

The last hypothesis concerns H, not a hidden connectivity assumption on the
auxiliary paths. For general H the cost encoding still holds; physical
two-connectivity is asserted only under the displayed sufficient hypothesis.

## 4. Self-contained connected and bridgeless normalization

**Lemma 5.** Any simple h-vertex graph F can be transformed in polynomial
time to a simple connected bridgeless graph J such that

    tau(J)=2m+tau(F)+1,

where m is the edge count of an explicitly constructed intermediate graph.

**Proof.** Add a new apex adjacent to all h old vertices and to h+2 new
leaves, forming F+. It is connected. Any cover omitting the apex contains
all old vertices and all new leaves, of size2h+2. Including the apex and
all old vertices already gives sizeh+1, so every minimum cover includes
the apex. Therefore tau(F+)=tau(F)+1. Let m=|E(F+)|.

Replace each edge uv of F+ by two internally disjoint length-three paths,
u-a-b-v and u-c-d-v, using four new vertices for that edge. The resulting J
is simple and connected; every edge lies on its gadget's six-cycle, hence
there are no bridges.

Fix a choice Z of the old F+ vertices in a cover of J. Each gadget needs
exactly two internal cover vertices if at least one of u,v is chosen, and
four if neither is chosen. This follows directly by inspecting the two
length-three paths, whose internal vertices are disjoint. Hence the minimum
cover size for that Z is

    2m+|Z|+2*|E(F+-Z)|.

If an edge is uncovered by Z, add one endpoint. This costs one vertex and
removes at least one penalty of two, strictly decreasing the expression.
An optimum must therefore cover F+, and its value is2m+tau(F+). QED.

**Corollary 6 (operation-count NP-completeness).** Given a physical instance
of the restricted type in Theorem 4 and an operation budget t, deciding
whether some final-isolation batch reaches matching cost0 with at most t
operations is NP-complete. This remains so for two-connected bipartite
physical graphs of minimum degree2 and maximum degree3, all square owners,
minimum-cardinality initial omission, auxiliary P4/P2 components and no
addition conflicts or blockers.

**Proof.** Membership in NP is direct: a batch certifies permission, final
isolation, size and zero matching cost (the final auxiliary graph is
edgeless). For hardness start with Vertex Cover instance (F,t0), apply
Lemma 5 and Theorem 4 to J, and use operation budget
D*(2m+t0+1). Theorem 4 gives minimum cost-zero operation count
D*tau(J)=D*(2m+tau(F)+1), so the answers agree. All constructions, including
q=|V(J)|*max(1,Delta(J)), are polynomial. Lemma 5 provides the connected
bridgeless hypothesis needed for two-connectivity. QED.

Thus conflict-cover size zero does not suffice for polynomial-time
**minimum-operation** optimization in the mixed class unless P=NP. This
does not contradict Theorem 2: maximum saving is easy, and in the reduction
selecting all groups always reaches cost0. Nor is it a hardness result for
unrestricted all-helper optimization, dissociation, star-forming parameters,
the universal8b/3 target, or rectangular grids. The physical all-square
class already has positive unrestricted results in the existing research.

## 5. Implementation, verification and remaining scope

Implementation: [mixed_isolated_cover_repair.py](../develop/mixed_isolated_cover_repair.py).
The generic algorithms require only an initial degree-two bipartite induced
graph; they allow higher ambient degrees outside it. The physical reduction
satisfies the stronger ambient P4/P2 restriction. To rerun the assertion-enabled
complete checker:

```sh
python3 -B scripts/check_mixed_isolated_cover_repair.py
```

The [frozen report](../output/mixed-isolated-cover-repair-check.json) gives
literal matching and cover comparisons, full small mixed-removal systems,
all small directed dependency graphs, random larger controls, physical
vertex-cover costs/tie-breaks, normalization gadgets, explicit final
certificates and vertex-deletion checks. General statements rely on the
proofs above. The [independent audit receipt](../output/mixed-isolated-cover-repair-review.json)
records the actual exact-source and execution scope, not a formal-kernel
or priority audit.

Mixed deletion with nonisolated additions still needs a different endpoint
analysis. General compatible physical multi-Hall routing, a universal unit
5/6 improvement, arbitrary-width rectangular-grid triple equality and the
remaining sharp degree/gap parameters stay in the full ACTIVE research goal.
The October submitted manuscript is not changed by this note.
