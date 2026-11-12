# Exact budget frontiers by candidate component forests and cycle rank

13 November 2026. For a fixed replacement list on an ambient degree-two
bipartite auxiliary graph, this note computes every exact-count optimum in
polynomial time when the candidate component multigraph is a forest, and in
O(2^k N(q+1)^2) arithmetic transitions for its cycle rank k. It gives an
all-scale physical class with unbounded minimum complete-component traversal
width but k=0, and an explicit nonmonotone budget frontier on a periodic
subfamily. Tree-factor inference, conditioning cycle-cut variables and the
path matching identities are standard; the claims here are their exact
adaptation, domain, witnesses and physical separation. No priority audit is
claimed. Complete proofs follow.

## Precise fixed-list setting

Let A have N vertices, be finite simple bipartite and have maximum degree2.
Fix U and q replacements x_i in U to y_i outside U, with all x_i distinct
and all y_i distinct. Every subset is allowed. Costs are unit maximum
matching numbers of the final induced A[U_S]. The target is every exact
operation count F(t), together with a selected-mask witness. No weighted TH
routing, universal graph parameter, rectangular-grid embedding or unrestricted
omission optimizer is asserted.

Let K be the multigraph with one vertex per complete ambient component of A,
and one edge per candidate joining the components containing its endpoints.
Allow loops and parallel edges. Let c=|V(K)| and d be the number of connected
components of K, counting isolated vertices. Put k=q-c+d (k=0 for empty K).
A spanning forest contains c-d edges; all remaining k edges, including loops,
will be frozen. This is the standard cycle rank, not a claim of new generic
factor-graph methodology.

## Forest messages and invariant

**Theorem1.** If K is a forest, the complete frontier and a witnessing subset
for every exact operation count are constructible with O(N(q+1)^2)
arithmetic transitions, with polynomial bit and witness overhead.

**Proof.**

First suppose K is a forest, so there are no loops or parallel cycles. Root
each tree. A nonroot auxiliary component C has a unique parent candidate e;
each child component D is attached by one child candidate f. At C, each such
candidate has exactly one endpoint. This uses the distinct-endpoint input
condition and absence of same-component candidate loops.

Define M_C(s,t) to be minimum summed matching cost over components in the
rooted subtree of C, with parent bit s_e=s, counting all selected candidate
edges whose child lies in that subtree. The counted set includes e exactly
once and every internal descendant edge once. The message records a full
selected mask for those counted edges. A root has no parent bit and counts
only its descendants. The cost is a sum of component costs, because complete
ambient components have no A-edge between them.

Compute messages bottom-up. For fixed parent bit s, scan C along its path or
even cycle. Initialize budget s and mask {e} if s=1, cost0; a root initializes
budget0/maskempty. Use exactly the present-run parity automaton of the current
frontier theorem, including the two closed traces on even cycles. A fixed
vertex uses its fixed membership in U. At the parent endpoint use membership
1-s for an x endpoint, s for a y endpoint, without another charge. At a child
endpoint, choose bit r=0/1 and a row M_D(r,j), add its cost, count j and mask,
and use the corresponding membership at that endpoint. Thus each candidate
is counted by its child message, never by both endpoints.

For each equal (scan position,budget,p,h) retain the minimum cost and a full
mask. The invariant is: its histories are exactly all choices in fully
processed child subtrees and processed component positions satisfying the
fixed parent bit and current parity; their only future-relevant information
is the displayed state. Child trees are disjoint, and the tree condition
rules out an unrecorded equality from one processed child to another or to a
future component position. This proves safe merging and exhaustive extension
by induction over child height and component scan positions. At component
completion, path traces are unrestricted at the end; cycle traces require
end p=h. The existing path/even-cycle identity makes every accepted component
trace its actual maximum matching cost, including full even cycles. Closing
and minimizing therefore yields exactly M_C(s,t), not merely a lower bound.

Combine root messages by budget convolution. Their counted edge sets and
ambient components are disjoint, so sum cost, count and union masks. Every
candidate is counted once, every subset appears, and every final budget has
a row. This proves the claimed forest frontier and witnesses. Final covers
and matchings follow componentwise as in the accepted frontier theorem.

A safe arithmetic bound is O(N(q+1)^2): at most constant-many parity and
parent-bit states per budget, at most q+1 child rows per choice, and one
vertex scan per ambient vertex. Root convolutions add at most c such steps,
where c<=N unless N=0 (handled directly). Costs and q-bit masks impose only
polynomial bit overhead. No bound on K's degrees is required; the path/cycle
automaton evaluates each high-arity component factor without enumerating all
its incident candidate assignments.

## General cycle rank

**Theorem2.** For general K, the complete frontier and witnessing subsets
are constructible with O(2^k N(q+1)^2) arithmetic transitions, with
polynomial bit and witness overhead. Empty inputs are returned directly.

**Proof.**

Choose a spanning forest of K. For each assignment z in {0,1}^k to its
nonforest edges, pin both endpoint memberships by z. Remove these variables
from the component coupling graph. They contribute their selected count and
mask once globally. All other candidate couplings form a forest and use the
preceding messages, with pinned endpoint memberships treated as constants.
A branch may omit some exact budgets; only its feasible rows are returned.
Minimize per budget over all pin assignments. This partitions all candidate
subsets, so the final frontier is exact. Bound O(2^k N(q+1)^2) arithmetic,
polynomial bit/witness overhead. Loops are pinned and parallel edges beyond
the forest are pinned. k=0 specializes to the forest algorithm. This
parameter is not always better than the earlier traversal width: local
same-component pairs may have small w and large k. The following family
establishes the opposite separation.

## Physical star family with unavoidable large complete-component width

**Theorem3.** For each even q>=2 and every binary type vector there is a
two-connected bipartite physical graph of order10q, minimum degree2 and
maximum degree3, with cardinality-minimum initial square-owner omissions
and q individually permitted distinct-owner replacements. Their candidate
component graph is a star. The minimum pair width over all complete-component
traversals is exactly q/2, while k=0.

**Construction and proof.**

For any even q>=2, use witnesses x_i,z_i in a central cycle C_(2q), and
witnesses y_i,w_i in a separate P2 for every i. Let

    P={(x_i,z_i),(y_i,w_i)},
    Q={(z_i,x_(i+1))},
    owner square=(x_i,y_i,z_i,w_i).

Physical colours: x_i,z_i=i mod2; y_i,w_i=1-i mod2. P endpoints have the same
physical colour, Q endpoints opposite, and owner squares alternate; the
helper construction is bipartite. There are b=2q helpers,4q witnesses,4q
owners, total10q. Helpers and non-Q witnesses have degree2, Q witnesses and
owners degree3. Each owner square together with its two P-helper paths is a
two-connected module, since the two paths are ears between distinct square
vertices and include all its helper/witness vertices. Q cyclically joins
modules. Any one vertex deletion preserves each module and removes at most
one joining edge; q>=4 leaves a connected quotient cycle/path, and q=2 has
two distinct joining edges so one remains. Hence the physical graph is
two-connected at every allowed q.

Choose arbitrary type bits a_i. Initially omit {x_i,z_i} for type0, or
{x_i,w_i} for type1. These are cardinality-minimum square omissions. The
single candidate in each square is x_i->y_i. Each resulting two-point owner
complement induces maximum degree at most1, so every subset/prefix is
permitted. The candidate multigraph K is a star: candidate i connects the
central cycle to leaf P2 i. Thus k=0.

In any complete-component traversal, let a leaves occur before the central
cycle. The cut immediately before it has a live pairs; the cut immediately
after it has q-a. Therefore w>=max(a,q-a)>=ceil(q/2), independent of all
component orientations and central rotations. For equality, scan leaves0,...,q/2-1 before the central cycle in natural
x0,z0,x1,z1,... order, then the remaining leaves. The first half of the
central scan closes the q/2 live pairs; the second half opens q/2 pairs.
No cut has more than q/2. This proves the exact minimum width. It separates
the bounded-cycle-rank class from every fixed complete-component-width class;
it does not assert a lower bound for arbitrary interleaved vertex traversals.
The two parameters need not dominate each other.

**Corollary4.** In the periodic type0011 subfamily with q=4r, r>=1,

    F(t)=max(2r-floor(t/2),r,t-2r),   0<=t<=4r.

The minimumr is first attained at2r operations; the full actual graph has
40r vertices and the resulting dissociation certificate has size23r.

**Proof.** For q=4r, types0011 repeated, the final auxiliary graph separates into r
independent cost tiles. Two absent type1 z-vertices break the central cycle
into a five-position run x0,z0,x1,z1,x2 (fixed z0,z1; variable x0,x1,x2)
and isolated x3, in each tile. Leaf costs are s2+s3. Enumerating the eight
possibilities of (s0,s1,s2) gives the following direct path costs, including
leaf cost s2. This is a local identity from the displayed five-position path,
not an extrapolation from family enumeration.

| (s0,s1,s2) | Central matching cost | Leaf s2 cost | Sum |
| --- | ---: | ---: | ---: |
| 000 | 2 | 0 | 2 |
| 001 | 2 | 1 | 3 |
| 010 | 2 | 0 | 2 |
| 011 | 1 | 1 | 2 |
| 100 | 2 | 0 | 2 |
| 101 | 1 | 1 | 2 |
| 110 | 1 | 0 | 1 |
| 111 | 0 | 1 | 1 |

The exact first-three-variable budget costs are(2,2,1,1); s3 independently
adds cost1 when selected. Thus the four-variable
tile frontier is (2,2,1,1,2).

Each tile costs at least1, can save at most floor(t_tile/2) from2, and costs
at least t_tile-2. Summing and using sum floor(t_i/2)<=floor(sum t_i/2) gives
F(t)>=max(2r-floor(t/2),r,t-2r). Equality: up to2r operations use two in
floor(t/2) tiles and one in an unused tile if t is odd; from2r to3r use two
or three per tile; above3r use four in t-3r tiles and three in the others.
Therefore

    F(t)=max(2r-floor(t/2),r,t-2r), 0<=t<=4r.

Minimumr is first attained at2r operations. With b=2q=8r helpers, the
certificate size is3b-r=23r. This is fixed-list matching optimality and an
actual lower certificate, not an unrestricted graph-parameter optimum. QED.

## Physical wrapper and exact domain

As in the preceding [nonisolated frontier theorem](NONISOLATED_EXCHANGE_BUDGET_FRONTIER.md),
A=P union Q is degree-two bipartite. Fix a permitted initial omission U and
at most one individually permitted replacement within each distinct owner
component. Every subset and prefix remains permitted, because distinct
components have disjoint owner edges. The wrapper verifies initial owner
complement degrees globally and each changed owner locally, then applies
Theorem2 to the whole candidate list. Given a final tight cover C of A[U_S],
select all helpers, owners outside U_S, and witnesses in U_S minus C. The
witnesses are independent in A, no selected witness meets its selected
owner, and selected owner degrees are at most1. The actual induced degrees
are therefore at most1 and the set has size3b-|C|. All exact-count rows have
masks reconstructing their matching and cover; the wrapper materializes the
best row's owners/witnesses certificate. Permission is independent of the
forest condition. The domain is this fixed list, not all omission states.

## Reproduction, verification and limits

Implementation: [component_cycle_frontier.py](../develop/component_cycle_frontier.py).
Run the complete assertion-enabled checker:

```sh
python3 -B scripts/check_component_cycle_frontier.py
```

The checker literally enumerates candidate subsets and maximum matchings
on its small inputs, independently of the message recurrence and endpoint
parity identity. It also compares the earlier pair-width solver, checks
candidate permutations and component order/direction/rotation, loops and
parallel edges, explicit cycle ranks, full even cycles, genuine random
component forests, and nested one-shot iterators. The physical family
controls check every returned row's actual dissociation certificate, exact
periodic formulas, and a traversal attaining q/2. Connectivity tests delete
every physical vertex throughq8; larger scales sample four vertices. General
connectivity and width claims rely on the all-size proof above. The saved
[report](../output/component-cycle-frontier-check.json) contains aggregate
counts, a digest and one q4 periodic example, not every comparison row.
The [audit receipt](../output/component-cycle-frontier-review.json) records
exact frozen bytes and independent execution scope after review.

The earlier pair-width and present cycle-rank algorithms give different
useful parameters, not a uniformly small parameter for all lists. Both are
standard exact DP adaptations. These algorithms optimize unit matching
cost. A candidate component forest is not a graph of HH sources, does not
provide physical multi-Hall geometric routing, and implies no rectangular
grid embedding. Universal8b/3, remaining sharp degree and regularity cases,
compatible multi-Hall routing, the unit5/6 gain and arbitrary-width grid
triple equality remain open in the full ACTIVE goal. No October manuscript,
Lean execution, email, submission or literature-priority claim is involved.
