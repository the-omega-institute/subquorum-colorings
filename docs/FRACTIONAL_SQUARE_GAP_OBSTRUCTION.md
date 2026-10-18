# Fractional square capacity does not force star-forming equality

19 October 2026. For every d>=4 the previously proved sharp graph G_d
has a nonnegative fractional four-cycle cover with total incidence one
at every vertex, yet

    beta_2(G_d)=2d+1 < 2d+2=SF_2(G_d).

The graph and parameter values are established in
SHARP_REGULAR_BIPARTITE_GAP.md. The contribution here is an explicit
all-degree square certificate, a shorter independent dissociation cap,
and a precise obstacle to deriving star-forming equality from square
capacity alone. The graph is not asserted to be a rectangular grid or
to have a partition into disjoint square tiles. No priority claim is made.

## The graph and its selected set

Use independent classes A={a_i}, B={b_i}, X={x_i}, Y={y_i}, each of
size d, with indices modulo d, and two more vertices p,q. Its edges are

    a_i--b_j for i!=j;
    a_i--y_i, b_i--x_i, p--y_i, q--x_i;
    x_i--y_j when j-i modulo d is neither1nor2.

The bipartition is A union X union {p}, B union Y union {q}.
Every vertex has degree d and the order is 4d+2. The earlier proof shows
two-connectivity. For reference S=A union B union {p,q} has size 2d+2
and is minimal forming: every outside vertex has two selected neighbors;
deleting a_i uncovers y_i, now adjacent only to the selected isolate p;
deleting b_i similarly uncovers x_i; deleting p or q uncovers itself.
The established degree-capacity bound gives

    SF_2<=floor(d(4d+2)/(2d-1))=2d+2,

so this S attains the upper value without enumeration.

## Four classes of weighted squares

Use the following cycles, with each unordered neighbor pair counted once:

- Crown cycles a_i-b_j-a_k-b_l-a_i, in the crown on A union B.
- P-cycles p-y_j-x_i-y_k-p, for each x_i and pair of its Y neighbors.
- Q-cycles q-x_j-y_i-x_k-q, defined symmetrically.
- Mixed cycles a_i-b_j-x_j-y_i-a_i, whenever both required cross edges exist.

Assign each crown cycle weight

    alpha=6/[d(d-1)(d-2)(d-3)],

each P- or Q-cycle weight

    eta=2/[d(d-2)(d-3)],

and each mixed cycle weight gamma=1/d. These weights are positive for d>=4.
All other four-cycles may be assigned weight zero.

Put c=(d-1)(d-2)(d-3)/2 and t=(d-2)(d-3)/2.
The number of incident cycles of each class is

| Vertex class | Crown | P-cycles | Q-cycles | Mixed |
| --- | ---: | ---: | ---: | ---: |
| A or B | c | 0 | 0 | d-3 |
| X | 0 | t | 2t | d-3 |
| Y | 0 | 2t | t | d-3 |
| p | 0 | dt | 0 | 0 |
| q | 0 | 0 | dt | 0 |

Here a fixed a_i has d-1 choices of the other A vertex and then
choose(d-2,2) pairs of common B neighbors, giving c. A fixed x_i centers
t P-cycles. For a Q-cycle containing x_i, choose one of its d-2 adjacent
Y vertices and then one of the other d-3 X neighbors there, giving 2t.
The other cases follow by the same counts with the classes exchanged.
For a mixed cycle at a_i, y_i has d-2 X neighbors, and excluding x_i
because a_i-b_i is absent leaves d-3. This also counts mixed cycles
at every B,X,Y vertex. Finally p lies in t cycles for each of d X vertices.

Thus the total incident weight is, respectively,

    c alpha+(d-3)gamma=3/d+(d-3)/d=1,
    3t eta+(d-3)gamma=3/d+(d-3)/d=1,
    dt eta=1.

This proves an exact fractional square cover at every vertex. In particular,
all denominators and multiplicities are assigned once; the mixed-cycle
weight does not reuse the crown contribution.

The total weights of the four classes are 3/2,1,1,d-3, respectively,
with sum d+1/2=(4d+2)/4. This supplies a second direct check on the
weighted upper bound. All verification uses exact rational arithmetic.

## Consequences

Every dissociation set uses at most two vertices of each square. Multiplying
these inequalities by the weights and summing counts every selected vertex
with coefficient one, so beta_2(G_d)<=|V(G_d)|/2=2d+1. One bipartition
part attains 2d+1, proving the exact beta value with no neighborhood case
split. This is an alternative proof for the single-block graph only;
the edge-deleted block and connected-ring caps retain their separate proofs.

Together with the explicit minimal forming S this gives an obstruction
in every d>=4 to the implication

    exact fractional square-capacity cover implies beta_2=SF_2.

The same local square capacities prove the dissociation bound, but they
do not give the corresponding upper bound for inclusion-minimal forming
sets. Any attempt to use these capacities for the rectangular-grid triple
equality needs additional geometric or deletion-witness control.
This does not refute the rectangular-grid conjecture or a rule requiring
a partition into disjoint tiles.

At d=4 all three weights are 1/4. There are exactly18 displayed squares,
and every vertex lies in four. The graph has18vertices, beta_2=9 and
SF_2=10. At d=3 the denominators vanish and the construction is the
square-free Heawood graph. Its beta cap therefore needs a different
mechanism, consistent with the distinct cubic covering question.

## Verification

`scripts/check_dissociation_covers.py` checks these exact rational weights
and all cycle edges for d=4,...,12, verifies the incident coefficient one
at every vertex, and checks the displayed minimal selection using literal
stars. Small independent one-part optima check the resulting beta values.
These are controls for the all-degree counting proof above.
The general local square capacity is proved in
formal/StarForming/DissociationCover.lean; the weighted finite summation,
cycle counts and uniform all-degree certificate remain written proofs.
