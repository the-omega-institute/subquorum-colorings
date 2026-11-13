# Any number of owner squares with four fixed boundary vertices

13 November 2026. This local theorem strengthens the four-boundary lemma in
`UNIQUE_C12_RESERVED_REGION_THEOREM.md`. It allows arbitrarily many reserved
owner squares and preserves every specified boundary membership. The proof
uses the physical matching-cut construction in
`SQUARE_CORE_MATCHING_CUT_THEOREM.md` and a prescribed-vertex refinement proved
here. It does not assume that separate local savings can be added.

## Statement

Let R be a union of whole physical auxiliary cycles, with disjoint perfect
matchings P,Q and A=P union Q. A physical colouring c is constant on P-edges
and opposite on Q-edges. Suppose R contains k disjoint whole owner C4s and
exactly four remaining vertices F. Each owner square alternates physical
colour. Necessarily |R|=4(k+1); assume F has two vertices of each physical
colour, as holds in the physical balanced auxiliary-cycle setting.

**Theorem.** For every prescribed subset F0 of F, there is a set U with
exactly two omissions in each reserved owner square and U intersect F=F0
such that

    delta_R(U):=|U|-2nu(A[U])
       >=2floor(k/2)+(|F0| mod 2).                       (1)

The case k=0 is included. All nonboundary omissions belong to the reserved
squares. No exterior owner choice or auxiliary edge is modified. In a larger
instance, exact choices on every unreserved owner therefore stay fixed.

For k=3 this recovers deficiency at least two, or three for an odd boundary.
For k=4 it strengthens the earlier lower bound to four, or five for an odd
boundary. For k=5,6,7 the even-boundary lower bounds are respectively 4,6,6.
These are lower guarantees; no sharpness of (1) is claimed.

## Prescribing an independent vertex

Recall the matching-cut lemma: on 4t vertices, P is a partial matching
preserving physical colour, Q is a partial matching reversing it, and R_op
is a perfect matching preserving it. Each physical side has 2t vertices.
Every P union R_op component inside a side has equally sized proper classes.
Selecting one class per component on one side gives exactly t vertices;
removing their at most t Q-neighbours from the other side leaves at least t
vertices in a bipartite graph. Choosing larger proper classes there gives
an independent set Y in P union Q union R_op of size at least ceil(3t/2).

**Prescribed-vertex lemma.** Any specified vertex z can be required to belong
to Y without changing that size guarantee.

**Proof.** Start in z's physical colour side. Orient the proper classes of
the component containing z so that its chosen class contains z; orient the
other components arbitrarily. Equal class sizes still give exactly t
vertices in that side. The Q-neighbour deletion and larger-class choices
in the other side are unchanged. Thus z belongs to the resulting independent
Y and its order is still at least ceil(3t/2). QED.

This requires R_op to cover every vertex. A general triangle-free subcubic
graph without the physical matching-cut structure is outside this lemma.

## Proof with every fixed boundary subset

Give F a temporary physical owner square, solely to define its opposite
pairs. Together with the k reserved squares this yields t=k+1 squares.
Let R_op be the matching of opposite vertices in all these squares.
Apply the matching-cut lemma, using its prescribed-vertex version when
specified below. Extend Y to a set Z choosing exactly one vertex from each
R_op pair. This is possible because Y is independent in R_op. Hence

    |Z|=2(k+1),
    Z contains exactly two vertices per square,
    Y subset Z is independent in A,
    nu(A[Z]) <= |Z|-|Y| <= floor((k+1)/2).               (2)

For the matching inequality, Z minus Y is a vertex cover of A[Z], so every
matching has at most that many edges; equality or an optimization theorem
is unnecessary. Z selects one vertex of each physical colour on F.

Construct Z depending on f=|F0|:

- If f is zero or four, no prescribed vertex is needed. Passing from Z to
  U=(Z minus F) union F0 adds respectively zero or two vertices.
- If f is two, prescribe any z in F0 to belong to Y. Since Y subset Z,
  Z intersect F0 is nonempty. Only one vertex of F0 at most must be added.
- If f is one, prescribe its vertex to belong to Y. It is already in Z,
  so no addition is needed.
- If f is three, let x be the missing boundary vertex and prescribe its
  opposite partner in the temporary square to belong to Y. Exactly one
  endpoint of that opposite pair is in Z, so x is absent. Both boundary
  vertices of Z therefore lie in F0, and only one addition is needed.

In every case U has precisely the required boundary subset, keeps two
omissions on every actual reserved square, and is obtained with at most
floor(f/2) additions. Deleting vertices cannot increase matching number;
adding one vertex increases it by at most one. Therefore (2) gives

    nu(A[U]) <= floor((k+1)/2)+floor(f/2),
    |U|=2k+f,
    delta_R(U) >= 2k+f-2floor((k+1)/2)-2floor(f/2)
               =2floor(k/2)+(f mod 2).

This proves (1) for every k and every specified F0. The temporary square
places no requirement on the final F0 and contributes no artificial graph
edge to A. All cost comparisons and returned matchings use the original
P,Q edges. QED.

## Compatibility, construction and exact finite controls

When R is a union of whole auxiliary components, no A-edge leaves R.
Thus an exterior common exchange forest can first fix every unreserved
owner choice, including its exact subset F0 on F, and then invoke this
local theorem. Regional deficiency adds to actual exterior deficiency
without any resource reuse. Applying this lemma separately to overlapping
regions would need a further compatibility argument; no such addition is
part of this statement.

`develop/fixed_boundary_matching_cut.py` constructs a prescribed independent
set, extends it to Z, replaces the boundary and computes an actual maximum
matching. The original square-core supplier remains unchanged.
Reproduce the standalone controls with assertions enabled:

    python3 -B scripts/check_fixed_boundary_matching_cut.py

The checker separately optimizes matching size by a literal vertex-mask
recurrence, checks every one of the sixteen fixed boundary subsets in
each placement, and checks a prescribed independent vertex at every vertex
of the stated smaller controls. Larger seeded placements include a single
C16 and many squares, but do not prove the full unique-C16 theorem. Exact
finite scope is recorded in `output/fixed-boundary-matching-cut-check.json`;
the argument above proves all k. Independent audit status is recorded in
`output/fixed-boundary-matching-cut-review.json`. No new Lean execution or
unrestricted graph-gap improvement is claimed by this local theorem.
