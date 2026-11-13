# One auxiliary twelve-cycle with arbitrary owner even cycles

We prove the physical all-helper bound when the auxiliary graph consists of
arbitrarily many squares and one twelve-cycle. The proof fixes all exterior
omission choices before choosing a reserved region. A local lemma works for
every prescribed subset of its four boundary vertices, so the exterior and
interior savings are compatible.

## Setting and statement

Let V have N=2b vertices. Let P,Q be disjoint perfect matchings whose union
A is s C4 disjoint-union C12. Let B be a simple union of even cycles, each
of length at least four, on V. A physical colouring c:V->{0,1} is constant
on P-edges and opposite on Q- and B-edges. An omission set U is permitted
if B[V\U] has maximum degree at most one. Write nu for matching number.

**Theorem.** Under these hypotheses, there is a permitted U with

    nu(A[U]) <= floor(N/6).

In the original 5b-vertex physical graph this gives

    beta_I >= ceil(8b/3),

where beta_I is the largest dissociation set containing every helper.

The physical graph has a helper for each P-edge, one witness and one owner
for each index. Each helper joins its two witnesses; witness v joins owner
v; Q joins witnesses, and B joins owners. A dissociation set induces maximum
degree at most one. If every helper is selected, selected witnesses must be
independent in A, and a selected owner excludes its witness. Thus, for a
fixed owner set V\U, the maximum size is

    b+(N-|U|)+alpha(A[U]) = 3b-nu(A[U]),                 (1)

using bipartiteness of A. Maximizing over permitted U proves the exact
identity beta_I=3b-min_U nu(A[U]). This is the normalization used below.

The proof uses the previously proved all-auxiliary-square theorem, the
at-most-one-K4 theorem, and the owner-C4/6k theorem. Their exact statements
and proofs are in [the square forest manuscript](../manuscript/auxiliary-square-forest-proof.tex),
[Mixed owner bridges, Theorems 2 and 3](MIXED_OWNER_BRIDGES.md), and
[the preceding cyclic rank note](CYCLIC_RANK_EXTENSIONS_AND_PARITY_OBSTRUCTION.md).
The at-most-one-K4 theorem applies here whenever A has at most one square:
a K4 in A union an owner matching requires an auxiliary square, since
removing the matching leaves a four-cycle. Each A-square supplies at most
one such K4. Physical owner C4s use virtual opposite pairs as specified in
the bridge theorem; the underlying B-permission remains its actual edges.

## Omissions, deficiency and a common forest

On an owner cycle C of length m the minimum omission count is ceil(m/3):
every three consecutive vertices must contain an omission, and gaps of at
most three attain the bound. Therefore minimum choices on all owner cycles
have total size

    M=N/3+d,    d=sum_C d_C,
    d_C=2/3 for m=4 mod6; 1/3 for m=2 mod6; 0 for m=0 mod6.    (2)

Call the cycles with d_C>0 exceptional. Set

    delta(U)=|U|-2nu(A[U]).

Every induced component of A[U] is a path or an even cycle; delta is exactly
the number of odd-order induced components, including isolated vertices.
For a minimum-cardinality U it suffices to prove

    delta(U)>=d-1/3.                                      (3)

Indeed nu(A[U])<=(N+1)/6, and for even N,
floor((N+1)/6)=floor(N/6). This last equality uses the residues 0,2,4 mod6;
no real inequality nu<=floor(N/6) is inferred without integer rounding.

For each prescribed oriented edge xy of an exceptional owner cycle there
are two minimum omission choices differing exactly by replacing x by y.
Here is an explicit construction, writing the cyclic order from x. For
m=4 use {x,the opposite vertex}. Otherwise take gaps 3 between successive
omissions, except a final gap 2; when m=4 mod6 also replace the second gap
by 2. These gaps sum to m. Replacing x by y increases the final gap to 3
and decreases the first to 2, so both choices are permitted and minimum.

Project each auxiliary component to one node. Each exceptional owner cycle
provides the family of its edges crossing distinct nodes; retain the owner
label on each projected edge. A rainbow forest chooses at most one edge
per family. Its maximum size is

    r = min_J (h-|J|+rho(E_J)),                            (4)

where h is the number of families and rho is graphic rank, including
isolated nodes in the vertex ground set. This is Rado's independent
representative theorem in the graphic matroid; the square forest manuscript
includes a proof of the exact deficiency formula and its Rado42 reference.
The consequence needed here is: if rho(E_J)>=d_J-epsilon for every J, then
r>=d-epsilon, because h-|J|>=d_(all\J).

Choose the minimum omissions associated with the selected forest edges.
Each edge exchange toggles the parities at its two ends. In a tree one
can prescribe odd counts at all vertices except possibly a chosen root:
take its root parity to agree with the total, then process the leaves
inwards. Thus a forest of r edges yields at least r odd auxiliary counts,
and hence delta>=r. All families participate in **one** forest.

The rooted form reserves whole owner cycles inside a union R of whole
auxiliary components. Contract R to one root, leaving the other components
as nodes; omit the reserved families from the forest. Root its tree at R.
At least r nodes outside R then have odd counts. Freeze every unreserved
owner choice, including its exact membership on

    F=R\(union of the reserved owner cycles).

Choose reserved omissions last, with their counts unchanged. No A-edge
leaves R, so the resulting actual induced deficiency satisfies

    delta(U)>=r+delta_R,   delta_R=|U intersect R|-2nu(A[U intersect R]).   (5)

This construction preserves all exterior memberships, not just their parities.

## Two local lemmas with fixed exterior choices

**Fixed-outside lemma.** Let C be an exceptional owner cycle, let R be a
union of whole auxiliary components containing C, and fix omissions on
R\C. Some minimum choice on C gives positive regional deficiency; when
the resulting regional size is even, its deficiency is at least two.

For odd regional size the assertion follows from parity. For even size,
suppose all prescribed-edge choices above gave perfect matchings. For
each owner edge xy, take perfect matchings for the two choices differing
by x/y. Their symmetric difference contains an even alternating path from
x to y, in H=A[(fixed exterior) union C]. Thus x and y lie on the same
side of one bipartite component of H. Since the owner cycle is connected,
all vertices of C lie on the same side of one component of H. Every other
vertex of that component is retained. A perfect matching after retaining
ceil(|C|/3) vertices of C would require its original two sides to differ
by |C|-ceil(|C|/3)>=2. But a component of H is a path or an even cycle,
whose side sizes differ by at most one. This contradiction proves the lemma.
The matching argument uses only A and the fixed membership; no physical
owner edges are inserted into the induced auxiliary graph.

**Four-boundary lemma.** Let R be a union of whole physical auxiliary cycles,
|R|=4(k+1), with k=3 or 4 disjoint whole owner C4s inside it. Let F be the
remaining four vertices. For every prescribed F0 subset F, one can choose
exactly two omissions on each reserved square, retaining exactly F0 on F,
with delta_R>=2. If |F0| is odd, one can achieve delta_R>=3.

If |F0| is even, fix any two omissions on all but one square and apply the
fixed-outside lemma to the last. The regional cardinality is even, giving
two deficiency units.

If |F0| is odd, Q[R] is an opposite-colour perfect matching and every owner
square has two vertices of each physical colour. Hence F also has two of
each. Give F a temporary alternating owner square. Let D pair opposite
vertices of all k+1 squares. The union P[R] union D is two-colourable:
its components are alternating even cycles or single shared edges. Denote
a proper second colouring by t, and label a vertex by (c,t). Opposite owner
vertices have the same c and different t, so every square has all four
labels, each label occurs k+1 times, and every A-edge joins distinct labels
(P changes t; Q changes c).

For a fixed label lambda, the three label pairs containing lambda induce
a total of 2(k+1) A-edges: every edge incident with its label class is counted
once and no other edge is counted. The three pairs avoiding lambda also
have total 2(k+1), because A[R] has 4(k+1) edges. In either family some
pair induces at most h_k=floor(2(k+1)/3) edges.

For |F0|=1, use its unique vertex's label lambda, choose a low-edge pair
containing lambda, and delete the other selected vertex of F. For |F0|=3,
use the missing vertex's label, choose a low-edge pair avoiding lambda,
and add the remaining required F vertex. Each reserved square retains
exactly two vertices. The first operation cannot increase matching number;
the second increases it by at most one. In both cases

    delta_R >= 2k+1-2h_k = 3  (k=3,4).

The artificial square is used for labels only. No exterior owner cycle or
its prescribed F0 is changed.

## Connected reductions and contained exceptional cycles

Decompose A union B into connected components. Costs and permissions add.
Components without the twelve-cycle L have only squares and are already
covered. In the component with L, the earlier results cover at most one
auxiliary square and all owners of length four or divisible by six. Hence
assume from now on that this component is connected, contains at least
two auxiliary squares, and has an exceptional owner cycle of length at
least eight. A union of whole auxiliary components filled by whole owner
C4s would be closed under both A and B, hence the entire connected component,
contradicting the last assumption. We use this exclusion below.

The contained exceptional cycles in L have lengths 4,8,10. Three contained
C4s, or C8+C4, would fill L and close it, already removed. The remaining
possibilities are as follows. Reserve all contained exceptional cycles,
contract L, and write d_other for the remaining weight.

| Reserved cycles | Reserved weight | Free capacity at root | Forest lower bound |
| --- | ---: | ---: | --- |
| C10 | 2/3 | 2 | r>=d_other |
| C8 | 1/3 | 4 | r>=d_other |
| two C4s | 4/3 | 4 | r>=d_other |
| one C4 | 2/3 | 8 | r>=d_other-1/3 |

For completeness, consider any projected subfamily. In a connected support
component with v nodes and x cycles of type 4 mod6 and y of type 2 mod6,
capacity four gives v>=x+2y. Its rank v-1 pays (2x+y)/3 whenever x+5y>=3.
The failing possibilities are one or two C4s saturating one or two nodes.
Away from the root these form excluded closed all-C4 components. At the
root, capacity two forbids saturation for C10; restoring two reserved C4s
makes an excluded closed all-C4 component; restoring C8 gives L alone or
L plus one auxiliary square, removed by the at-most-one-square case. Thus
the first three rows satisfy full rank on every subset.

For the last row, a support containing the root and q squares has capacity
4q+8 and rank q. A loss exceeding 1/3 requires 2x+y>=3q+2. Together with
4x+8y+6a<=4q+8 (a>=0), this implies x+5y+(9/2)a<=4. The only possibilities
are C4-only families: x=1 or 2 at q=0, x=3 at q=1, or x=4 at q=2. The
first is another contained square, excluded in this row; the other three
saturate the free region and close an all-C4 component after restoring the
reserved square. At most one support contains the root, so all subset
ranks lose at most 1/3. Formula (4) proves the table's last row.

Apply the rooted construction and freeze the outside. With two reserved
squares fix one arbitrarily, then apply the fixed-outside lemma to the
other; no independent second saving is claimed. In all four rows the
internal deficiency is at least one. Formula (5) gives respectively

    delta>=d+1/3, d+2/3, d-1/3, d.

All imply (3), settling every contained-cycle case.

## Classification when no exceptional cycle is contained in L

For a connected projected exceptional subfamily containing L and q squares,
write the sum of its owner lengths as 4x+8y+6a. Capacity and a rank loss
exceeding 1/3 require

    4x+8y+6a<=4q+12,      2x+y>=3q+2.                 (6)

There is no contained exceptional cycle, so q>=1. Combining these inequalities
gives x+5y+(9/2)a<=7. If a>=1, then y=0 and x<=2, incompatible with the
second inequality for q>=1. Thus a=0. Now y is zero or one. If y=1, then
x<=2 and (6) forces x=2,q=1. If y=0, then x<=7 and the integer interval
ceil((3q+2)/2)<=x<=q+3 gives exactly the following list:

| q | Owner cycles | Status |
| ---: | --- | --- |
| 1 | three C4s | 12 vertices in L plus one square, four free vertices |
| 2 | four C4s | 16 vertices in L plus two squares, four free vertices |
| 1,2,3,4 | respectively 4,5,6,7 C4s | saturated closed all-C4 component |
| 1 | two C4s and one C8 | saturated closed component with at most one square |

The last two rows were removed. Call the first two configurations T3 and T4.
Support components avoiding L have full square-capacity rank, with the same
excluded closed small components. Therefore, if neither T3 nor T4 occurs,
all subset ranks are at least d_J-1/3. One common rainbow forest and (3)
settle this case. This is an integer classification valid at all sizes.

## Reserving a region with four free vertices

For T3 reserve its three owner squares inside R=L union K. For T4 reserve
its four inside R=L union K1 union K2. In either case the contracted root
has four free vertices, and every remaining node is an auxiliary square.

For T3 the capacity-four argument gives rho(E_J)>=d_J for every remaining
subfamily. Its small saturated failures would close an all-C4 component,
also when the root is present: restore its three reserved squares. Hence
r>=d_other. Freeze the exterior choices, use the four-boundary lemma with
k=3, and obtain delta>=d_other+2=d. This proves (3).

For T4 we need the stronger statement

    rho(E_J)>d_J for every nonempty remaining subfamily J.   (7)

For a connected support with v nodes and counts x,y, capacity gives

    (v-1)-(2x+y)/3 >= (x+5y-3)/3.

This is positive when x+5y>=4. Otherwise y=0 and x=1,2,3. Failure of
strictness forces v=x; those x owner C4s saturate all x four-vertex
capacities. Away from the root the region is closed all-C4; at the root
restore the four reserved squares to obtain the same contradiction. Thus
each occupied support has strict rank, proving (7). Empty crossing families
are included as occupied isolated supports in this reasoning.

There is at least one remaining exceptional cycle, since otherwise all
original owners would have length four or divisible by six, an earlier
base case. In (4), J empty gives h>d_other because every family weight is
at most 2/3; J nonempty gives

    h-|J|+rho(E_J)>d_other.

Consequently r>d_other and, since all weights are thirds,
r>=d_other+1/3. The four-boundary lemma with k=4 gives two internal units.
Therefore

    delta>=r+2>=d_other+7/3=d-1/3,

as the four reserved squares have weight 8/3. This completes (3), and
integer rounding proves the theorem. The proof needs two internal units,
not four, in this case.

Reassemble components. Each local matching cost is at most floor(N_i/6),
whose sum is at most floor(N/6). For the constructed U take an independent
witness set of size |U|-nu(A[U]) and every owner outside U. Formula (1)
then supplies an actual all-helper certificate in the original graph.

## Construction, checks and attribution

[The constructor](../develop/reserved_owner_squares.py) uses the inherited
rainbow-forest routine and returns actual matching/cover certificates. It
finds T3/T4 by searching auxiliary-square regions with at most two squares;
there is no exhaustive search over complete omission assignments. The
inherited at-most-one-square colouring routine is a feasibility search;
no polynomial runtime claim for the whole constructor is made.

[The checker](../scripts/check_reserved_owner_squares.py) separately traverses
induced auxiliary components, verifies matching/cover equality and original
5b-vertex dissociation sets, and compares every small subfamily rank to the
Rado formula. It controls every marked four-subset and every fixed exterior
pattern on C12, contained C8/C10 choices, and the four-boundary construction
against literal matching. It also includes frozen physical instances of
every new branch and seeded larger controls. Reproduce with assertions on:

    python3 -B scripts/check_reserved_owner_squares.py

The report states the finite scope. The proof above establishes arbitrary
sizes independently of those controls. The proposal came from the retained
Oracle research conversation; this note reconstructs its argument, applies
it to actual physical certificates and records a separate exact-source
independent audit in output/unique-c12-review.json when that audit completes.
It extends the preceding one-C8 and square-incidence results. General mixed
auxiliary cycles, the unrestricted sharp star-forming gap, and physical
multiple-Hall grid routing remain separate open questions. This working
research note makes no priority or journal-readiness claim and does not
modify the October submitted manuscript.
