# Exact terminal routing and cycle credit for a network of square contacts

The shared-star theorem excludes closed P-only cycles by its leaf hypothesis.
For a general contact network, those cycles are possible and their M edges
must be removed from the payment ledger. This note gives an exact finite
permutation reduction, a sharp cycle-rank bound, and a feasible all-length
family repairing a TT/HH pair at zero incremental M cost. The result concerns
certificates at fixed actual M; it does not establish universal coverage or
improve the universal 5/6 bound.

## 1. Hypotheses and directed fragments

Work on a bipartite grid, with black vertices of even coordinate sum. Fix an
actual partial matching M, its endpoint set P, Q=V\P=T disjoint-union H, and
a full auxiliary perfect matching N. Assume the original configuration is
feasible. Choose e alternating unit squares with pairwise disjoint vertex
supports. At each square, its two N edges belong to DISTINCT original
terminal paths of M+N. There are n affected original paths. Original doubled
M/N edges and P-only cycles are not chosen. The contact multigraph G has
these n paths as vertices and the e chosen squares as edges; parallel edges
are retained. Let c be its number of connected components.

Switch all chosen squares, producing N'. All removed edges are outside M.
An inserted edge joins vertices from distinct original terminal paths, so it
also lies outside M. Disjoint supports make N' a perfect matching and give
M intersect N'=M intersect N. M and feasibility remain unchanged.

Orient every original terminal path from its BLACK Q endpoint to its WHITE
Q endpoint. This orientation exists because it has odd length, alternating
N,M,...,N. Its N edges run black to white and its M edges white to black.
At a square the only alternative bipartite matching sends each cut black
endpoint to the OTHER path's cut white endpoint. Thus a switch exchanges
the two outgoing continuations in these canonical orientations.

If path i has d_i chosen cuts in order, cutting them makes d_i+1 fragments.
Every original vertex and M edge has exactly one fragment owner; cuts are N
edges, so no M edge is cut. The total fragment count is n+2e.

## 2. The permutation theorem

For each path i introduce a marker s_i and a symbol x_(g,i) for each of its
chosen cuts. Define alpha to be the disjoint union of the n cycles

    (s_i, x_(g1,i), ..., x_(gd_i,i)),

where cuts are listed from black Q to white Q. Define tau to exchange the
two symbols belonging to every contact g, fixing all markers. Set

    f = alpha composed with tau.                         (1)

Attach a fragment R_y to each symbol y: R_(s_i) is the initial fragment
before the first cut; R_(x_(g_j,i)) is the fragment AFTER cut j, up to the
next cut or the white Q endpoint. Each fragment has its actual vertices
and M-edge set, including the possibility of a singleton terminal and no
M edges. A marker and a cut can refer to the same physical terminal when
the cut is the first edge; they remain distinct bookkeeping symbols with
a zero-edge initial fragment, so no physical vertex is duplicated.

**Permutation theorem.** Starting at s_i and iterating f until the next
marker s_j gives exactly the final directed terminal path from the black
endpoint of original path i to the white endpoint of original path j.
Each traversed f arc out of x owns fragment R_(tau(x)). Each f cycle with
no marker gives exactly one final P-only alternating cycle, with the same
fragment ownership rule. These paths and cycles partition all affected
physical vertices and M edges.

Proof. From a marker, tau fixes it and the initial fragment leads to the
first cut. From a cut black endpoint x, the inserted N' edge goes to the
white endpoint at the paired cut tau(x); following its unchanged fragment
ends at alpha(tau(x)). This is precisely (1). At the final fragment, the
white Q endpoint is denoted by the marker of its original path; stop there
instead of traversing the formal closure back to that path's black Q.
Thus successive markers give exactly the genuine terminal paths. A cycle
with no marker meets no Q and is exactly a P-only cycle. Conversely every
affected vertex belongs to one fragment and the two matchings prescribe
its continuation, so there are no other components. Since tau is a
permutation, every fragment is consumed by exactly one f arc. This proves
both completeness and unique physical ownership. The zero-length closure
at a marker identifies names only, never two actual Q vertices. In
particular, the physical fragment before a first-edge cut is a singleton,
and the fragment after that cut begins at its DISTINCT white endpoint.

Let pi(i)=j be this first return to the marker set. If B_i is the T/H label
of black endpoint i and W_j that of white endpoint j, the final endpoint
types are exactly

    (B_i, W_(pi(i))), i=1,...,n.                        (2)

In particular ALL affected terminal paths are TH iff B_i != W_(pi(i)) for
every i. This supplies an exact test, including arbitrary sharing and
closed cycles. It is not a Hall test on individually valid pairs. After
the geometric cuts have been sorted and the fragment M costs recorded,
permutation traversal takes O(n+e) time and space, independently of the
lengths of the original paths. Extracting the fragments from the actual
paths still takes time proportional to their total size.

## 3. A sharp topological bound

Let r be the number of NEW affected P-only cycles. Then

    0 <= r <= e-n+c.                                    (3)

In particular a forest of original-component contacts cannot create one.

Proof. First perform contacts of a spanning forest of G in an order that
successively joins its graph components. Inductively the processed part
has only terminal paths: the next contact cuts one N edge in each of two
different processed graph components, hence in two distinct terminal
paths. The four terminal arms reconnect into two terminal paths, with no
cycle. This proves the forest assertion without assuming any terminal
labels or ordering of several contacts on a shared original path.

There remain e-(n-c) contacts. A single two-edge switch increases the
number of P-only cycles by at most one. To see this, edges on distinct
terminal paths yield two terminal paths; edges on the same terminal path
can at most split off one cycle. A path and a cycle merge into a path;
two distinct cycles merge into one; two cuts on one cycle leave one or
two cycles. These cases exhaust degree-two path/cycle components. All
unperformed original cut edges are still present because the chosen
supports are disjoint. Starting at zero proves (3).

The ladder family below attains equality for every e>=1. The bound counts
cycles, not their physical M weights; even one cycle can carry arbitrarily
many M edges.

There is also an exact parity constraint. Let q be the number of cycles of
the first-return terminal permutation pi. The cycles of f consist of these
q marker-containing cycles and r marker-free cycles. On n+2e symbols,
alpha has n cycles and sign +1, whereas tau has sign (-1)^e. The sign
formula for f therefore gives

    r+q = n+e (mod 2).                                  (3a)

This is a necessary condition on any candidate routing and cycle ledger,
in addition to (3). It follows from the actual bipartite continuation rule,
not from a choice of arbitrary nonbipartite reconnection orientations.

### The two-contact dichotomy

Suppose exactly two distinct original paths have exactly two chosen
contacts with each other. Label the contacts g1,g2 in black-to-white order
on the first path. There are only two cases:

* If the second path has the SAME canonical contact order, pi is the
  identity and r=0.
* If the second path has the REVERSE order, pi exchanges the two terminal
  destinations and r=1.

To verify this directly, write the two alpha cycles as (s,a1,a2) and
either (t,b1,b2) or (t,b2,b1), with tau=(a1 b1)(a2 b2).
In the first case f has cycles (s,a1,b2) and (t,b1,a2).
In the second it has cycles (s,a1,t,b2) and (a2,b1).
The last cycle contains no marker. This also agrees with (3) and (3a).

For original TT and HH paths, the first case leaves one TT and one HH;
the second produces two TH paths and exactly one P-only cycle. Thus a
two-contact repair of this pair occurs IF AND ONLY IF its canonical
contact orders are reversed, and every such repair necessarily has a
cycle credit. That cycle consists of the two original inner fragments
between contacts and the two inserted edges joining their ends. Each
inner fragment starts and ends with M and contains at least one M edge,
so the credit is at least two actual M edges. Consequently every such
successful two-contact repair is strictly cheaper than charging the
entire two original bad paths. The ladder realizes it at every length.

More generally, for k contacts between just one TT and one HH path,
successful repair means pi is the transposition, and (3a) implies
r = k-1 (mod 2). An even number of contacts cannot successfully repair
that pair without creating at least one cycle. A single contact always
repairs it with no cycle. Extra contacts therefore cannot be assessed by
adding individual repair counts or retaining the original full-path cost.

The same-order case also occurs on a feasible actual grid. The complete
[8-by-6 fixture](../output/two-contact-same-order-witness.json) specifies
M,N,T and the squares (1,2),(1,4). Its T is {(5,3),(7,4)} and |M|=14.
The two affected paths contain 12 M edges; an unaffected P-only component
contains the other two. Initial global counts are (1,9,0). Either contact
alone gives (0,8,2), using all 12 affected M edges. Both contacts together
give (1,9,0), no new cycle, and zero TH payments: the original defect
returns. The checker verifies the canonical order and full physical sets.
The two selected sites can instead pay to holes (6,3) and (7,3) with zero
M cost. The fixture is therefore an obstruction to adding individually
successful prescribed switches, not to payment existence or the target.

## 4. The exact payment ledger and safe cycle normalization

Let O be the M-edge union of the affected ORIGINAL TH paths, and B the
M-edge union of their original TT and HH paths. Let U be the final TH
M-edge union, D the final TT/HH M-edge union, and C the new cycle M-edge
union. Unique fragment ownership gives the set identity

    O disjoint-union B = U disjoint-union D disjoint-union C.  (4)

Thus the exact signed cost identity is

    |U|-|O| = |B|-|D|-|C|.                              (5)

For partial repair D must remain in (5): deleting its cost from U does not
pay its TT endpoints. If all affected final terminal paths are TH, D is
empty and

    U=(O disjoint-union B)\C,
    |U|-|O|=|B|-|C|.                                    (6)

This can be zero or negative. It is not valid to charge all original bad
path resources and separately credit a cycle without checking (4).
Each physical edge in C is removed once, whether it came from O or B.
Unaffected paths/cycles cancel from the global comparison. Terminal
incidences independently give a0-a1=b0-b1=(t1-t0)/2; cycles introduce no
extra terminal or hole credit.

There is also a legitimate full auxiliary certificate realizing this
credit as retention: on every new P-only cycle replace N' by its M edges.
Call the result N*. A cycle contains only P; both matchings stay inside it,
and its M edges cover all its vertices. Different cycles are disjoint.
Therefore N* is a perfect matching, all terminal paths and their payments
are unchanged, and

    M intersect N* = (M intersect N) disjoint-union C.     (7)

No M edge in C was initially retained: it lay on an original terminal
path. The normalization changes only the auxiliary certificate, never
actual M. No new numerical inequality follows without a coverage theorem.

## 5. A feasible sharp ladder and exact span credit

For any even W>=4, use a 4-by-W board. On rows 1 and 2 take the two
horizontal terminal paths. Let

    M={ ((r,c),(r,c+1)): r in {1,2}, c=1,3,...,W-3 },
    N={ ((r,c),(r,c+1)): 0<=r<4, c=0,2,...,W-2 },
    T={ (1,0),(1,W-1) }.

All other Q vertices are holes. Each selected endpoint has exactly one
P neighbour, its horizontal neighbour; its vertical neighbours are holes.
This is a feasible actual configuration. The two affected original paths
are TT and HH. The outer-row N edges are unaffected HH paths.

Choose any nonempty set of distinct even columns

    0<=c_1<...<c_k<=W-2,

and flip the squares with top-left corners (1,c_j). Their supports are
vertex-disjoint. Each becomes two vertical N' edges. The final terminal
paths pair the two left endpoints and the two right endpoints and are
both TH. For every j<k, the two horizontal segments from column c_j+1
to c_(j+1), together with the two vertical N' edges at their ends, form
one P-only alternating cycle. There are no others, by this explicit
component partition. Their exact M-edge counts are c_(j+1)-c_j.

Consequently

    initial (a,b,t) = (1,W+1,0),
    final   (a,b,t) = (0,W,2),
    r=k-1=e-n+c,
    |B|=W-2,
    |C|=c_k-c_1,
    |U|=c_1+(W-2-c_k).                                (8)

Only the outermost contacts determine the payment cost; adding contacts
strictly inside their span partitions the same cycle-resource set into
more cycles and cannot claim that resource again. With contacts only at
0 and W-2, one cycle already saves W-2 M edges, without bound. The two
TH payments are adjacent vertical edges and use ZERO M edges, although
the individual single-square repair uses all W-2 original bad-path M
edges. With all W/2 contacts, the count bound (3) is sharp, with W/2-1
cycles of two M edges each and the SAME total zero payment cost.

Thus an acyclic, single-contact cost formula is not a lower bound for
general fixed-M surgery. Here the defect repair is genuine, but the board
has |T|+|M|=W<area/2=2W. This does not refute a target inequality or prove
universal 5/6 improvement, and no novelty over general permutation surgery
is claimed. The new application is the precise physical ledger and its
actual feasible grid realization within this compensation project.

## 6. Evidence and remaining question

The direct physical checker compares the compressed permutation with
direct M+N' path/cycle decomposition, including endpoint pairs and actual
resource SETS, and checks cycle normalization. It covers arbitrary chosen
subsets on small ladders, all-length family controls and networks spanning
four original paths, plus both single contacts and their simultaneous
failure in the feasible 8-by-6 same-order fixture. It also checks (3a) and
the two-contact dichotomy. These computations test the construction and adapter;
the arbitrary-size proofs above do not depend on finite enumeration.

The seven local Lean kernels in ContactCycleLedger.lean certify the
all-finite-resource ledger and conditional arithmetic, not the geometric
permutation adapter or the cycle-rank argument. See the accompanying JSON
for the executed scope. Universal covering networks and a universal 5/6
improvement remain open. A new cycle credit must be tested together with
terminal coverage, never inferred from the number of contacts alone.
