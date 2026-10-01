# A proper-interval Hall reduction for bent compensation

2 October 2026. This note isolates a geometric condition under which the
weighted Hall test in [the guarded-donor note](GUARDED_HALF_DONORS.md) reduces
to consecutive source blocks. It is intended for bent or mixed-direction
routes whose admissible donor windows do not nest or cross back.

Let the source regions be ordered as `A_1,...,A_K` along the boundary of the
relevant residual strip. Let `D_1,...,D_L` be disjoint compensation regions,
with nonnegative capacities `c_j` (half-integers are allowed). Assume that the
admissible donor set of source `A_i` is an interval

```text
N_i = {D_l : left_i <= l <= right_i}.
```

The **proper-interval condition** is that both endpoints are strictly ordered:

```text
left_1 < left_2 < ... < left_K,
right_1 < right_2 < ... < right_K.
```

Thus two windows may overlap, but neither window contains another and the
windows cannot reverse their order. This is a geometric hypothesis; it is not
implied by the local tile labels alone.

## Lemma (proper-interval Hall reduction)

Under the proper-interval condition, the capacitated Hall inequalities

```text
sum(c_j for D_j in union(N_i for i in X)) >= |X|
```

hold for every source subset `X` if and only if they hold for every consecutive
block `X={a,a+1,...,b}`.

### Proof

The forward implication is immediate. For the converse, suppose a violating
subset `X` exists. Partition `X` into maximal groups whose donor intervals have
connected union; donor capacities add between distinct groups because their
unions are disjoint. Since the total capacity of the union is smaller than the
total number of selected sources, one group `Y` is violating.

Write `a=min(Y)` and `b=max(Y)`. Proper ordering gives
`left_a <= left_i <= left_b` and `right_a <= right_i <= right_b` for every
`a <= i <= b`. Because the donor intervals of `Y` have connected union, that
union is the full donor interval from `left_a` through `right_b`. Every source
between `a` and `b` has its donor interval contained in this same union.
Consequently

```text
union(N_i for i in Y) = union(N_i for a <= i <= b).
```

The consecutive block `{a,...,b}` has strictly more sources whenever `Y` has
a gap, but exactly the same donor capacity. It therefore also violates Hall,
contradicting the block inequalities. Hence no violating `X` exists. QED.

The statement remains valid for arbitrary nonnegative real capacities; the
half-integer case is the one used by the tile ledger. Multiplying capacities by
two gives an ordinary integral max-flow instance.

## Consequence for cross-component compensation

Suppose the source-to-compensation incidence graph is produced by a monotone
boundary routing and satisfies the proper-interval condition. Then it is enough
to verify

```text
sum(c_j for D_j in union(N_i for a <= i <= b)) >= b-a+1
```

for each consecutive source block. Combined with the weighted compensation
lemma, disjoint regions, and `rho(W) <= 0`, this yields `q <= 0` and therefore
the coefficient-one bound for that covered class. The block checks are still a
geometric obligation: a bent path can create a nested window, a repeated tile,
or a shared terminal, any of which invalidates the proper-interval hypothesis.

The condition also explains why the current abstract Hall lemma cannot yet be
applied to arbitrary bends. A source whose candidate donors surround another
source's candidates has a nested window; checking only prefixes or local
neighbors then misses a possible subset deficit. The properness requirement
rules out exactly that failure mode while allowing overlapping windows.

## A geometric sufficient condition

The following criterion is the form that can be checked for a restricted
single-bend family. Let `D_1,...,D_L` be donor tiles on one boundary row, in
left-to-right order. For each source `A_i`, suppose the proposed route has a
left connector and a right connector ending at donor tiles `D_{left_i}` and
`D_{right_i}`. Assume:

1. sources are ordered left-to-right, and the connectors start in that same
   order on the source boundary;
2. connectors of the same side are tile-disjoint, lie in the strip between
   the source boundary and the donor row, and have no horizontal backtracking;
3. left and right connectors do not cross one another or share a tile; and
4. the admissible donor region for `A_i` is exactly the donor interval between
   its two connector endpoints.

The planar order of disjoint connectors is preserved from one boundary of the
strip to the other. Hence

```text
left_1 < left_2 < ... < left_K,
right_1 < right_2 < ... < right_K.
```

The endpoint inequalities are strict because a shared endpoint tile would
violate the assumed tile-disjointness. Therefore this route family satisfies
the proper-interval hypothesis, and its weighted Hall obligation reduces to
the consecutive-block inequalities of the lemma above.

This criterion isolates the remaining geometric work instead of hiding it in
the word “interval”: one must prove that the candidate region is filled from
the two endpoints, and separately check that a capacity-two passage or a turn
does not make two connectors share a tile. If either property fails, the full
weighted Hall test is still required.

## Scope and controls

The result is a general combinatorial lemma, conditional on a geometric
incidence description. The accompanying control script exhaustively checks
small proper-interval families with capacities in `{0,1/2,1,3/2,2}` and records
the shortest non-proper counterexample to the block-only test. It is a finite
sanity check, not a substitute for proving properness in a tile configuration.

No manuscript or arXiv source is changed by this note.
