# Two-row signed compensation and a sharp failure of automatic cancellation

This note proves an anchor-free structural compensation lemma, using the actual
matching. It also gives an exact half-area six-row configuration where positive
cross-strip boundary charges are paid by negative internal matching edges.
Thus the failure belongs to the rule that discards those internal payments and
assumes automatic boundary cancellation, not to the half-area target.

## 1. Definitions and block classification

Let a two-row strip `S` of even width lie in a feasible rectangular grid.
As usual, `P` is the endpoint set of an actual matching `M`, `T` is disjoint
from `P`, `O=T union P`, `H` is the unoccupied set, and every selected vertex
has at most one occupied neighbour. Tile `S` by disjoint two-by-two blocks.
Write `q(B)=|T intersect B|-|H intersect B|`.

Assign a charge `sigma_B(p)` to each actual matching endpoint in a block.
Horizontal and vertical refer to the two-row strip. All rotations within the
following types are interpreted with respect to those fixed directions.

| Block type | Endpoint charges |
|---|---|
| Two diagonal T, one P, one H | +1 on the unique P |
| One T, two horizontally adjacent P, one H | +1 on the P vertically adjacent to T, -1 on the other P |
| One T, two vertically adjacent P, one H | 0 on both P |
| Four P | 0 on all P |
| Two T and no P | no endpoint charges |
| No T, three P, one H | -1 on the P vertically adjacent to H, 0 on the others |
| Every other feasible type | -1 on every P |

The list is exhaustive. A block contains at most two T. With two adjacent T,
the remaining two sites must be holes. With two diagonal T, at most one other
site can be occupied. With one T, at most two sites can be P, and when there
are two they must be adjacent. Thus the only positive block is the first type,
with `q=1`; its unique endpoint must be matched outside the block. The four
neutral types have `q=0`. The three-P type has `q=-1`. In every remaining case,
putting `t=|T intersect B|` and `p=|P intersect B|`, we have `t+p<=2`, whence

    q(B)=2t+p-4 <= -p = sum_{p in P intersect B} sigma_B(p).

For every listed exceptional type the same inequality is equality. Hence

    q(B) <= sum_{p in P intersect B} sigma_B(p).                 (1)

## 2. Actual internal matching edges

Every actual matching edge `uv` wholly inside `S` satisfies

    sigma(u)+sigma(v) <= 0.                                   (2)

Only an edge incident to a +1 endpoint needs proof. A +1 endpoint has a
selected vertex directly above or below it. Its actual mate cannot be that
vertical neighbour, so an internal mate must be horizontal.

If the mate is in the same block, the type is the horizontal two-P neutral
block and the partner has charge -1. If the mate lies across a block boundary,
the selected vertical neighbour of the +1 endpoint already has its one occupied
neighbour. It therefore forces the vertex vertically adjacent to the receiving
endpoint to be a hole. Inspect the exhaustive types above: any P with a vertical
hole has charge -1. In a horizontal neutral block it is precisely the negative
endpoint; in a three-P block it is the specified negative endpoint; the other
feasible receiving types charge every P by -1. Positive blocks, vertical neutral
blocks and all-P blocks have no P with a vertical hole. This proves (2).

There is no assumption that an endpoint retains an earlier prescribed partner.
It is the actual mate, and hence the actual horizontal receiving endpoint,
that is used in this argument.

## 3. Signed-boundary compensation lemma

Let `Q_S` be the endpoints in `P intersect S` whose actual mates lie outside
`S`. Define

    B_S = sum_{p in Q_S} sigma(p),
    E_S = sum_{uv in M, u,v in S} (sigma(u)+sigma(v)),
    L_S = sum_blocks [sum_{p in P intersect B} sigma(p)-q(B)].

Then **exactly**

    |T intersect S|-|H intersect S| = B_S + E_S - L_S,          (3)

where `E_S<=0` and `L_S>=0`. In particular

    |T intersect S|-|H intersect S| <= B_S.                    (4)

To prove the identity, every endpoint in `S` belongs to one actual matching
edge. An edge wholly inside `S` contributes its two endpoint charges to `E_S`;
an edge leaving `S` contributes its unique internal endpoint charge to `B_S`.
This partitions the endpoint set. Subtracting the block slacks from (1) gives
(3), and (1),(2) give the signs. Every physical block slack and every actual
matching edge appears once. In particular (3) retains the negative internal
edge payments which would be lost by using only (4).

For a closed two-row board, `B_S=0`, so `|T|<=|H|` and
`|T|+|M|<=|S|/2`. For several two-row strips covering a board, (3) sums to

    |T|-|H| = B_cross + E_internal - L,

where each crossing edge contributes the sum of its two strip-side charges
**once**, each internal edge contributes once, and `L>=0`. The crossing charge
need not be nonpositive. Its legitimate available compensation is
`-E_internal+L`. A sufficient unified inequality is therefore

    B_cross <= -E_internal + L.                               (5)

This note does not prove (5) for arbitrary strip collections. It makes the
remaining obligation explicit and excludes automatic cancellation as a shortcut.

## 4. Exact half-area obstruction on six rows

Use rows `0,...,5`, columns `0,...,3`, with the three row-pair strips. Set

    T = {(0,0),(3,0),(5,0)}

and take the nine actual edges

    (1,0)--(2,0),  (1,1)--(1,2),  (0,2)--(0,3),
    (1,3)--(2,3),  (2,1)--(2,2),  (3,2)--(3,3),
    (4,1)--(5,1),  (4,2)--(4,3),  (5,2)--(5,3).

All endpoints are distinct. The three holes are `(0,1),(3,1),(4,0)`.
The selected vertices have, respectively, the single occupied neighbours
`(1,0),(2,0),(5,1)`. The matching and selection are feasible, and

    |T|=3, |M|=9, |H|=3, J=12=area/2.

In the first left block the endpoints `(1,0),(1,1)` have charges `+1,-1`.
In the second left block `(2,0),(2,1)` have charges `+1,-1`.
The last left block is the vertical neutral type, with charges zero.
All three right blocks contain only P, with charges zero. Every block slack
is therefore zero: `L=0`.

The crossing edge `(1,0)--(2,0)` has charge sum +2. The other crossing edge,
`(1,3)--(2,3)`, has charge sum zero. Hence `B_cross=2>0`. Exactly two internal
edges have negative charge sum: `(1,1)--(1,2)` and `(2,1)--(2,2)`, each -1.
All others have charge sum zero, so `E_internal=-2` and (5) holds with equality.

Thus the positive cross-component demand consumes two distinct actual internal
edge payments. Discarding those payments and claiming the boundary terms cancel
would fail **at an extremal configuration**, despite the target bound being true.
The bottom-row modification makes this example sharper than the original
six-row assistance example, whose bottom two rows were empty.

For every even width `w>=4` the same obstruction extends sharply: keep the first
four columns as above, fill all added columns with actual vertical matching
edges on row pairs `(0,1),(2,3),(4,5)`, and add no selected vertices. The old
selected vertices lie in column zero, so none gains a neighbour. The added
two-by-two blocks have zero charges; `B_cross=2`, `E_internal=-2`, `L=0` and
`J=3w` persist for every such width. This is an all-length construction, not
a claim inferred from examples.

## 5. Verification and provenance

The structural proof above is independent of a fixed-width optimizer or the
six-row potential table. The accompanying checker exhausts local block types
and adjacent block interfaces only to check the classification, charges and
local proof. It also independently rebuilds actual endpoint sets, selected
degrees and the exact ledger for the sharp obstruction and its extensions.

Proof assistance: broker task `3c84927d-3525-46ae-a285-c48899fbd366`, conversation
`conv_caf3bce504d3be56`, observed gpt_6/pro. It supplied the signed two-row lemma
and a non-sharp six-row boundary-cancellation obstruction. The sharp bottom
extension, exact retained-edge ledger and arbitrary-even-width construction
are deductions here. Assistance is not independent acceptance. Its proposed
four-column compression lemma remains unproved and is not a premise of this
note or of the separately checked boundary invariant.

Independent review `1502c35a-6718-4fa0-832b-62c7a3984897`, observed gpt_6/pro,
is COMPLETED/ACCEPT for Sections 1–4: the structural lemma, exact ledger and
sharp family for every even width. It verifies the written classification,
edge charges and construction without treating finite checker results as
premises, and does not claim code execution or a full-freezing result.
Its stream equals the terminal response. [Verdict and scope](../output/two-row-signed-independent-review.json).
The subsequent [four-to-two compression counterexample](TWO_COLUMN_COMPRESSION_OBSTRUCTION.md)
refutes the unproved assistance proposal; it was not part of this independent
review and is supported by its own written proof and checks.
