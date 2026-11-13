# Square-owner compensation with any balanced prescribed boundary

13 November 2026. This theorem extends the fixed-four-boundary construction
to an arbitrary balanced boundary. It supplies local choices after a common
exterior forest has fixed exact boundary memberships. It does not authorize
adding savings from overlapping regions.

Let W be a union of whole physical auxiliary cycles A=P union Q, with disjoint
perfect matchings P,Q. Physical colour is constant on P and opposite on Q.
Suppose W contains k disjoint whole owner four-cycles, leaving a free set F
of size4h, with2h vertices of either physical colour. For any prescribed
F0 subset F, write f=|F0|.

**Theorem.** There is U containing exactly two omissions on each actual owner
square, with U intersect F=F0, such that

    nu(A[U]) <= floor((k+h)/2)+floor(f/2),                 (1)
    |U|-2nu(A[U]) >= max(0,2k-2floor((k+h)/2))+(f mod2). (2)

The empty instance k=h=0 is included. The ordinary matching number is used;
no physical edge is added by the temporary construction below.

## Opposite pairs adapted to the prescribed membership

On each physical side of F, pair vertices inside F0 together as far as
possible, and do the same for vertices outside F0. If their counts are odd,
pair the one remaining inside vertex to the one remaining outside vertex.
Both counts have the same parity, since each side has order2h. These are h
same-colour pairs on either side. Pair one pair from each side to form h
temporary physical owner squares. These squares define virtual opposite
pairs only; their actual edges are never added to A.

Put a_c=|F0 intersect physical side c|. Any choice of exactly one endpoint
per opposite pair contains at least floor(a_0/2)+floor(a_1/2) vertices of F0.
If at least one a_c is odd, prescribe the F0 endpoint of one mixed pair to
belong to the independent set in the next step. Its contribution increases
that guaranteed intersection by one. Thus in all parity cases the chosen
set Z will satisfy

    |Z intersect F0| >= ceil(f/2).                        (3)

Indeed, when both a_c are even, the basic sum is f/2. When one is odd, adding
one gives (f+1)/2. When both are odd, adding one gives f/2. A mixed pair
exists whenever it is required: odd a_c is strictly between0 and2h.

## Independent set and matching cover

There are t=k+h actual or temporary owner squares. On their4t indices let
R_op pair opposite vertices. The physical matching-cut lemma and its
prescribed-vertex refinement are proved in
`SQUARE_CORE_MATCHING_CUT_THEOREM.md` and `FIXED_FOUR_BOUNDARY_MATCHING_CUT.md`.
For completeness: on either physical side, every P union R_op component
has equally sized proper classes. Select one class per component on the
first side, orienting the specified vertex's component to include it.
This gives exactly t vertices. Removing their at most t Q-neighbours leaves
at least t vertices in the other side's bipartite P union R_op graph.
Taking larger classes there gives an independent set Y in P union Q union
R_op, with |Y|>=ceil(3t/2), including the specified vertex when needed.

Extend Y to Z selecting exactly one endpoint of every R_op pair. Then
|Z|=2t, and Z minus Y covers all A[Z] edges. Therefore

    nu(A[Z]) <= |Z|-|Y| <= floor(t/2).                    (4)

The pair choices above prove (3) for this Z. Now set U=(Z minus F) union F0.
This deletes some vertices and adds at most floor(f/2). Matching number
cannot increase upon deletion; adding one vertex increases it by at most
one. Equation(4) proves(1). As |U|=2k+f,

    |U|-2nu(A[U]) >= 2k-2floor((k+h)/2)+(f mod2).

Also |U|-2nu is nonnegative and has parity f, giving(2). The actual reserved
squares retain exactly two omissions, and the final boundary is exactly F0.
No requirement from the temporary squares remains. This proves the theorem.

## Compatibility and verification

No A-edge leaves W. An exterior common exchange forest may therefore fix all
unreserved owner memberships first, then call this construction on its actual
F0. Actual interior and exterior induced deficiencies add. A separate proof
would be needed to apply it additively on overlapping regions.

For h=1, formula(2) recovers the all-k four-boundary guarantee
2floor(k/2)+(f mod2). For h=2,k=3 or4, it gives at least2+(f mod2), the two
eight-boundary cases needed in the unique auxiliary C16 theorem. The pairing
may depend on F0 precisely because F is free of final temporary owner
conditions. It does not change any exterior owner cycle or selected index.

`develop/balanced_boundary_matching_cut.py` returns the base independent set,
actual opposite pairs, base omissions, added vertices and exact final matching.
The inherited prescribed-vertex supplier is unchanged. Reproduce with
assertions enabled:

    python3 -B scripts/check_balanced_boundary_matching_cut.py

The checker tests every boundary subset in its stated placements through
h=3, including the entire4096-pattern twelve-vertex boundary in one placement.
Larger tests cover specified side-cardinality pairs with one seeded support
per pair. They do not exhaust all physical placements. Independent literal
matching and directly rebuilt temporary10(k+h)-vertex physical graphs check
the returned certificates. The report records exact scope; the argument
above proves all k,h. The theorem does not by itself settle arbitrary mixed
auxiliary cycles or physical grid routing. Its use in the unique C16 proof
and the independent audit are documented separately.
