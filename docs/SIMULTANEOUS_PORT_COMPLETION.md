# Simultaneous exterior ports and separated-core completion

11 November 2026. This note gives a physical completion theorem for several
centre paths at once, an exact optimizer for a specified form, and two grid
obstructions to choosing exterior entrances independently. Ordinary weighted
bipartite matching supplies the algorithm. The matching contraction and its
physical expansion are proved below.

## 1. Model and the form being optimized

Let V be a finite balanced board in the square grid; even coordinate sum is
black. An actual matching M covers P, and Q=V minus P. White Q vertices are
partitioned into selected T and HH sources W. Each t in T has at most one P
neighbour. Black Q vertices consist of exterior B and distinct centres h_i,
one for each of r>=1 cores P_i. The P_i partition P, are pairwise nonadjacent,
and are covered internally by M. Every P neighbour of h_i is in P_i, and
no centre has a direct T neighbour. The actual-edge weights are nonnegative.
Auxiliary N must perfectly match V. Empty feasible minima have value
positive infinity. A terminal path in tagged M union N
starts at white Q and ends at black Q; its interiors are in P. A path from
T is TH and pays its actual edges; a path from W is HH and pays zero.

A **local relay** from x to h_i has all its interior in P_i. A direct
W--h_i edge is allowed. Write c(t,i) for the minimum actual expense of a
local T relay, omitting unavailable pairs. HH reachability x--i means that
a local relay exists; its objective fee is zero regardless of its length
or actual weights. Nonnegative weights allow every minimum to be chosen
simple, by deleting directed alternating cycles.

The centre-relay/direct-exterior form requires every centre to receive one
local relay and every other terminal path to be a direct Q--Q edge ending
in B. P-only components are free and may be replaced by doubled unused M
edges. This form allows several TH centres and direct exterior HH paths.
It restricts non-centre relays; its optimum U_dir is an upper bound on the
unrestricted TH optimum f*, not a replacement for that optimum.

## 2. Coupled physical completion

Build a weighted bipartite graph K, with left side T disjoint-union W and
right side B disjoint-union I, where I indexes the centres. Its edges are:

| Edge | Condition | Fee |
| --- | --- | --- |
| t--i | local T relay exists | c(t,i) |
| z--i, z in W | local HH relay exists | 0 |
| x--b, x in T union W | direct grid adjacency | 0 |

Both sides have equal size, since M and V are balanced.

**Completion theorem.** U_dir is the minimum fee of a perfect matching of
K. A minimizing matching constructs a full physical N with exactly that
TH expense. If K has no perfect matching, a right-side Hall set with fewer
left neighbours certifies failure of this specified form.

**Proof.** Choose a shortest TH relay for every matched t--i and any HH
relay for every matched z--i. Different centre edges use different cores.
Thus their P interiors are disjoint; their white sources and black centres
are distinct by the matching. For every matched x--b take the direct edge.
These direct endpoints are Q vertices not used by another matched edge.
No actual M pair crosses one of the paths: its whole pair occurs internally
on that alternating path. Take all the paths' auxiliary edges, add the
direct edges, and double every unused actual edge. Each vertex of V has
exactly one auxiliary incidence. This is a perfect N. Only relays starting
in T pay, giving exactly the fee of K's matching.

Conversely, contract the local relays and the direct exterior paths of any
full N in this form. Each Q terminal occurs once, so this gives a perfect
matching of K; its fee is no greater than N's, because each paid relay may
be replaced by a shortest relay with the same endpoints. Such replacements
are simultaneous: there is only one relay per core. The two inequalities
prove equality of the minima. Hall's theorem gives the failure certificate.
QED.

In particular, matching capacity belongs to the entire choices, rather than
separate copies of their endpoints. No physical actual edge is paid twice;
HH relays remain free even when their actual edges are expensive.

## 3. Several exposed entrances

Forbid W--B edges, requiring every HH source to serve a centre. Suppose

    q = r-|W| = |T|-|B| >= 1,

the direct exterior graph G_O on B,T saturates B, and the HH incidence
graph Gamma on W,I saturates W. Exactly q centres are then TH. Denote the
restricted optimum by U_c. A candidate consists of a q-set J of TH centres,
a q-set A of selected entrance whites, and a bijection A->J by available
local relays. It completes exactly when Gamma matches W onto I minus J
and G_O matches B onto T minus A. These choices are all made together by
the same assignment theorem, with W--B edges deleted.

**Exterior capacity criterion.** A q-set A is exposable simultaneously iff

    |A intersect N_T(D)| <= |N_T(D)|-|D|       for every D subset B.  (1)

Indeed, Hall's condition after deleting A reads
|N_T(D) minus A|>=|D|, which is exactly (1). This also characterizes whether
an arbitrary A of size at most q can be included in an exposed q-set:
a B-saturating matching avoiding A leaves exactly q unmatched whites,
including A. Thus single-port exposure tests discard indispensable capacity
information. A tight neighbourhood has capacity zero; one with slack one
permits at most one chosen entrance.

For context, the T-subsets matchable injectively into B form the standard
transversal matroid; its bases have size |B|. The exposed q-sets are their
complements, hence the bases of its dual. Likewise the feasible J are
complements of W-saturating right sets in Gamma. The proof and implementation
need ordinary matching and (1); no matroid algorithm or polynomial-time
equality-recognition assertion is being introduced.

## 4. Exact attainment of the q-root source budget

Let rho_i=min_t c(t,i) be finite for every centre, and put

    Lambda_q = min_(Gamma matching saturating W)
                  sum_(centres unmatched by that matching) rho_i.   (2)

This is a relaxation: it has no entrance or exterior compatibility condition.
It is computed by matching W plus q dummy roots to I, giving an HH edge fee
zero and every dummy-root--i edge fee rho_i.

**Budget theorem.** For arbitrary full N under these hypotheses,

    Lambda_q <= f* <= U_dir <= U_c.                                  (3)

If every actual weight and every rho_i is strictly positive, then

    f*=Lambda_q  iff  U_c=Lambda_q.                                  (4)

For nonnegative weights, U_c=Lambda_q is sufficient for attainment.

**Proof.** If k centres are TH, their other r-k centres receive distinct
HH sources. Their local relays give a partial matching in Gamma. Extend
this matching to one saturating W: an augmenting path preserves all right
vertices already matched and adds one right vertex, and Gamma admits a
W-saturating matching. The q unmatched centres are therefore among the
original k TH centres. Since different actual paths are disjoint and
weights are nonnegative,

    f(N) >= sum_(TH centres) rho_i >= sum_(those q centres) rho_i
         >= Lambda_q.

The completion theorem and inclusion of the two forms prove (3), with
infinity for an unavailable form. If equality with Lambda_q holds under
strict positivity, k>q would make the second inequality strict. Hence k=q,
all HH sources serve centres, and the centre paths already spend Lambda_q.
All other TH paths have zero expense. Strictly positive actual weights
force these paths to be direct. Thus N belongs to the U_c form, and (3)
gives U_c=Lambda_q. Its attaining construction proves the converse. QED.

The q=1, all-HH-to-centres case recovers the earlier one-centre completion
criterion. The theorem here handles simultaneous choices of several
entrances, with source and exterior capacity enforced jointly.

## 5. A unit-weight 8-by-12 joint exposure obstruction

The false rule is: “if every chosen entrance can individually be exposed,
and the remaining centres can receive distinct HH sources, then those
entrances can be used simultaneously at their local path fees.”

Use the full board [0,7] x [0,11]. Three 3-by-3 squares have origins
(1,3), (1,9), (5,5), centres (2,4), (2,10), (6,6), and cores obtained
by removing their centres. In each core translate these four actual edges:

    (0,0)--(0,1), (0,2)--(1,2), (2,2)--(2,1), (2,0)--(1,0).

Their union is M. The cores are nonadjacent. Exactly one white Q vertex
has two P neighbours: W={(4,5)}. Select every other white Q vertex. Then
|T|=35, |B|=33, q=2, and every centre has no direct selected neighbour.
The following two disjoint TH relays both have unit expense:

    A: (4,9),(3,9),(2,9),(2,10),
    C: (5,8),(5,7),(6,7),(6,6).

The remaining source (4,5) relays to h_0, so the source assignment is valid.
Let

    D={(4,10),(5,9),(5,11),(6,8),(6,10),(7,9),(7,11)},
    F={(4,9),(4,11),(5,8),(5,10),(6,9),(6,11),(7,8),(7,10)}.

Direct coordinate inspection gives N_T(D)=F, |D|=7 and |F|=8. Both chosen
entrances are in F. Removing them leaves six white neighbours for seven
black vertices, violating (1).

Each entrance is individually usable even in a fee-two full N with the
same two TH centres: replace C's source by (4,7), or replace A's source
by (3,8), respectively. The modified relay enters the same first black P
vertex and uses the same actual edge. Two explicit complete N lists are
in the certificate file. They also give exterior matchings after the
corresponding pairs of entrance deletions.

An explicit exterior construction avoids any dependence on a matching
search. In both good cases take these nine vertical edges:

    (0,2)--(1,2), (0,7)--(1,7), (1,6)--(2,6),
    (1,8)--(2,8), (2,2)--(3,2), (2,7)--(3,7),
    (3,6)--(4,6), (4,4)--(5,4), (6,4)--(7,4).

For entrances {(4,9),(4,7)} add (3,8)--(4,8); for entrances
{(3,8),(5,8)} add (4,9)--(5,9). Remove all three square footprints,
W and the chosen entrances, and the vertical endpoints. Every remaining
horizontal interval has even length, and pairing consecutive cells tiles
it. This supplies the direct exterior part of each complete N.

The bad pair cannot extend at expense two even outside the specified form.
There are three centres and only one HH source, so at least two centres
are TH; each needs an actual edge. The pair already spends both units.
The third centre must consume the only HH source, and all other TH paths
must be direct. The exterior 7/6 Hall deficit prohibits that. Meanwhile
either good completion attains two, so the true unit optimum is exactly
two. The obstruction concerns which minimum pair can be used together,
not the existence of an optimum or the numerical colouring target.

## 6. A fixed footprint with Lambda_q=2 and f*=K+1

Use the full 12-by-18 board [0,11] x [0,17]. The three 5-by-5 square origins
are (1,3), (1,13), (7,7), with centres h_0=(3,5), h_1=(3,15), h_2=(9,9).
Remove each centre to form P_i. Here |T|=71, |B|=69, W={(6,7)} and q=2.
All T vertices are feasible and every centre is surrounded by its own P.

The local actual matching is explicit. Use the four edges

    (0,2)--(1,2), (2,0)--(2,1),
    (2,4)--(2,3), (4,2)--(3,2),

and horizontally tile each of the four corner 2-by-2 squares with origins
(0,0),(0,3),(3,0),(3,3). Translate this 12-edge pattern into every core.
Give edges (5,15)--(4,15) and (9,11)--(9,10) fee one, all other M edges fee
the integer K>=2. Then

    Lambda_q=2,      f*=U_dir=U_c=K+1.                              (5)

**Proof.** Every TH centre costs at least one. The HH source reaches core
0 via

    (6,7),(5,7),(5,6),(5,5),(4,5),(3,5),

leaving centres 1 and 2, each with a one-edge TH route, so (2) equals two.
The ONLY centre relays using no K edge are

    (6,15),(5,15),(4,15),(3,15),
    (9,12),(9,11),(9,10),(9,9).

Each cheap edge lies in a different core; its black endpoint has a unique
white Q neighbour, and its white endpoint is adjacent to its own centre.
There are no other cheap edges in either core, and none in core 0.
Thus a cheap-only TH path to a centre must be exactly the stated relay.

Let D be the 17 black vertices listed in the coordinate certificate. They
are the black vertices in

    ({6} x [13,17]) union ([7,11] x [12,17]).

Their selected neighbourhood F consists of the 18 white vertices in that
same region; direct inspection gives N_T(D)=F. Both cheap entrances
(6,15),(9,12) lie in F. Deleting both leaves only 16 neighbours for D.

Every full N has at least two TH centres. If any paid path uses a K edge,
some other centre TH path uses a distinct actual edge, so f(N)>=K+1.
Otherwise both centres must use the two cheap-only relays. These exhaust
all available paid actual edges; core 0 must receive W, all other TH paths
are direct, and the 17/16 exterior Hall deficit is impossible. Therefore
every full N costs at least K+1.

For attainment, retain the cheap relay into centre 1, replace the other by

    (9,6),(9,7),(9,8),(9,9),

and use the displayed HH relay to centre 0. The exterior matching is
explicit: take vertical edges (a,b)--(a+1,b) for a=1,3,5 and b=2,12,
and also (7,6)--(8,6), (10,6)--(11,6). After removing the square footprints,
W, the two chosen entrances and these vertical endpoints, the remaining
row intervals are [0,17] in row 0; [0,1],[8,11] in rows 1--5;
[0,1],[3,6],[8,11],[13,14],[16,17] in row 6; and [0,5],[12,17] in
rows 7--11. They all have even length and tile horizontally. This directly
matches all B to T minus {(6,15),(9,6)}. Doubling unused actual edges
therefore produces a full N. Its two paid edges have fees one and K, and
its HH path is free. This same N works for every K. It proves the upper
bound in (5); inclusion proves both form optima. QED.

The alternative centre-1 entrance (3,12), together with the cheap centre-2
entrance (9,12), has another complete certificate of fee K+1. Thus each
cheap entrance is individually exposable, the omitted-core source matching
is valid, and their simultaneous use still fails. Their local budget is
always two, while its gap and ratio to the true optimum are unbounded.

## 7. Verification and the remaining scope

Run `python3 scripts/check_multiport_completion.py`. The checker compares
the assignment solver against literal permutations, checks residual
potential certificates and Hall cuts, independently scores full physical
matchings, checks (1) against exhaustive exterior matchings, and enumerates
all 18,061 full auxiliary matchings of a 4-by-10 control board. The JSON
report and complete 8-by-12 and 12-by-18 coordinate lists are in `output/`.
Integer tests include zero and 401-bit fees. General theorems and (5) have
the written proofs above; the finite checks diagnose their implementation.

The complement-of-bases observation is standard transversal-matroid theory;
the algorithm is standard weighted assignment. The application here is the
exact physical expansion under one-relay-per-core separation. Additional
non-centre alternating relays remain outside U_dir; no unrestricted exact
optimizer, general unit-weight 5/6 improvement, grid triple equality, or new
Lean verification is inferred.
