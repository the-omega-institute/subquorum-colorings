# A structural obstruction to four-to-two-column compression

The four-column compression proposed in proof assistance
`3c84927d-3525-46ae-a285-c48899fbd366` is false. A realizable six-row boundary
has best closed two-column reward **-1**, while an explicit closed four-column
completion has reward **+1**. The following upper bound is a direct classification
argument; finite enumeration only discovered and checks the example.

## Boundary and reward

Use rows `0,...,5`. Immediately before the completion, the boundary column has
one selected vertex in row 2 and endpoints in rows 1,4,5, all of which have their
actual mates in the completion's first column. The other boundary vertices are
holes. It is a realizable one-column prefix, not an unreachable state:

    Oold={1,2,4,5}, F_old={2}, R_old={1,4,5}.

The selected row-2 vertex already has its occupied vertical row-1 neighbour, so
the first completion column's row 2 is forced to be a hole. In mask notation
the state is `(54,4,50)`, base-four index 3884. It cannot stop immediately,
because it has three pending matching endpoints.

For a completion of `l` columns define

    reward = 2|T_completion|+|P_completion|-6l
           = |T_completion|-|H_completion|.

The three incoming actual matching edges each contribute their single endpoint
inside the completion once. All other matching edges are wholly inside it;
its right boundary is closed.

## Exact upper bound for any closed two-column completion

Name the completion columns A,B. The sites A1,A4,A5 are endpoints, already
matched to the old boundary, and A2 is a hole. Tile this six-by-two rectangle
into three two-by-two blocks on row pairs `(0,1),(2,3),(4,5)`, and let their
charges `q=|T|-|H|` be `q_top,q_middle,q_bottom`.

Every two-by-two block has `q<=1`, and its only positive type has two diagonal
selected sites, one endpoint and one hole, by the elementary selected-degree
classification in the [signed-strip lemma](TWO_ROW_SIGNED_BOUNDARY_COMPENSATION.md).

First, `q_bottom<=0`: this block already contains the two endpoints A4,A5, so
it cannot have the unique-endpoint positive type. Also `q_middle<=0`. If the
middle block were positive, its hole would have to be A2; its two selected sites
would be A3,B2, and its endpoint B3. But then selected A3 has both B3 and A4
occupied, a contradiction.

If `q_top<=0`, total reward is therefore at most zero. The number of endpoints
inside the completion is odd: it is three incoming endpoints plus twice the
number of wholly internal matching edges. Consequently `|T|-|H|` is odd and
the reward is at most -1.

It remains to handle `q_top=1`. Since A1 is an endpoint, the positive pattern
forces A0,B1 selected and B0 a hole. Selection of B1 forces B2 to be a hole.
Now both A2,B2 are holes. Write `x=A3`, `y=B3`. The following are impossible:

* x,y both selected: x sees selected y and endpoint A4.
* x selected and y an endpoint: x sees endpoints y and A4.
* x an endpoint and y selected: x has no available actual mate. A2 is a hole,
  A4 already has its prescribed incoming mate, y is selected, and x's left
  neighbour in the old boundary is the hole in row 3.

Thus the two remaining sites of the middle block cannot both be occupied with
at least one selected. They give `q_middle<=-2`: two endpoints give -2, one
selected and one hole give -2, and all other cases are smaller. Hence total
reward is at most `1-2+0=-1` in this final case also.

The bound is attained. In A use only the three incoming endpoints A1,A4,A5 and
no selections. In B select rows `0,2,3,5` and leave rows 1,4 empty; add no
matching edges. Every selected vertex has at most one occupied neighbour.
There are 4 selected vertices, 3 endpoints and 5 holes in the completion, so
its reward is -1. Therefore the best zero-or-two-column completion value is
exactly `K0=-1`.

## Four columns with reward +1

Use these masks in consecutive completion columns A,B,C,D:

| Column | Selected rows | Endpoint rows and actual mates | Weight |
|---|---|---|---|
| A | 0,3 | rows 1,4,5, matched to the old boundary | 7 |
| B | 2,4 | row 1, matched to C1 | 5 |
| C | 0,3,5 | row 1, matched to B1 | 7 |
| D | 1,3,5 | none | 6 |

Every endpoint has the indicated actual mate. Selections in A each see one
vertical endpoint; B2 sees B1, B4 sees A4; C0 sees C1; C3,C5 see D3,D5;
D1 sees C1; and D3,D5 see C3,C5. No selected vertex has another occupied
neighbour. The old selected vertex in row 2 still sees only its old row-1
neighbour, because A2 is empty.

The completion has 10 selected vertices, 5 endpoints and 9 holes. Its weight
is 25 and its reward is `25-24=1`. Together with the one-column prefix this
is an actual closed six-by-five board with 11 selected vertices and four
matching edges: `J=15=area/2`. Thus it is feasible and respects the global
bound; it has not created a counterexample to the six-row theorem.

The proposed compression would require this reward +1 to be attainable by a
zero- or two-column completion, whose exact maximum is -1. It fails by two
units. Likewise, the proposed potential based on these short completions
cannot satisfy both transition inequalities everywhere. The independent
fixed boundary certificate is unaffected; it does not use this compression.

## Checks and next obligation

[check_two_column_compression_obstruction.py](../develop/check_two_column_compression_obstruction.py)
checks both literal closed boards directly from actual coordinates, reconstructs
the incoming state, and checks all two-column completions as a finite control.
The upper bound above does not depend on that enumeration. No claim that a
longer bounded-lookahead completion suffices is made.

A structural proof must retain enough information to pay these deferred
boundary gains, or use a different geometric invariant. This example closes
the proposed four-to-two rule rather than leaving it as an unverified lemma.
