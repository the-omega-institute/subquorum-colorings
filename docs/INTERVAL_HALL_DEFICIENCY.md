# Nested donor windows: containment tests and exact allocation deficiency

2 October 2026. This is an interval specialization of capacitated Hall and
max-flow/min-cut, not a novelty claim for matching theory. It strengthens the
allocation tool in [the proper-interval note](PROPER_INTERVAL_HALL.md): nested,
identical and unordered donor windows are allowed. The geometric existence of
these windows in arbitrary residual configurations remains unproved.

## Containment criterion

Let `D_1,...,D_L` be distinct, pairwise tile-disjoint compensation regions with
nonnegative capacities `c_j`. Each source has demand one and an admissible
neighborhood `N_i` which is either empty or a nonempty interval of this donor
order. No source order or monotonicity of interval endpoints is assumed. For
a donor interval `J=[l,r]` define

```text
C(J) = sum(c_j for l <= j <= r),
n(J) = number of sources with nonempty N_i contained in J.
```

**Theorem 1.** All sources admit a fractional allocation with each donor
spending at most its capacity if and only if no source has an empty window
and `n(J) <= C(J)` for every donor interval `J`.

**Proof.** If allocation exists, every source counted in `n(J)` must receive
its entire unit from donors in `J`; these donors can supply at most `C(J)`.
An empty neighborhood cannot supply one unit.

Conversely, suppose capacitated Hall fails for a source subset `X`. The union
of its nonempty neighborhoods decomposes into disjoint maximal consecutive
donor intervals `J_1,...,J_s`. Every neighborhood of a source in `X` lies in
exactly one such interval, since it is itself an interval. Assuming no empty
windows, write `X_t` for these source groups. The Hall failure says

```text
sum(|X_t| - C(J_t)) > 0.
```

Some `t` has `|X_t| > C(J_t)`. Every member of `X_t` is counted in `n(J_t)`,
so `n(J_t) > C(J_t)`, contradicting the containment tests. Thus Hall holds,
and capacitated max-flow/min-cut supplies the allocation. QED.

Only `L(L+1)/2` donor-interval inequalities are needed. The sources counted
by one test need not be consecutive in any previously chosen source order.
For example, windows `{D_1}`, `{D_1,D_2,D_3}`, `{D_1}` with capacities one
pass every consecutive-source-block test, yet `J={D_1}` traps two units of
demand with only one unit of capacity. The missing half of the rule is now an
explicit violated donor interval. This is an allocation obstruction, not a
feasible grid counterexample.

## Exact deficiency and disjoint obstruction certificates

Let `e` be the number of empty-window sources. Define the Hall deficiency

```text
delta = max_X (|X| - C(union(N_i for i in X))).
```

The empty source subset is allowed, so `delta >= 0`. By max-flow/min-cut the
maximum paid demand is `K-delta`.

**Theorem 2.** For arbitrary interval windows,

```text
delta = e + max_F sum(n(J)-C(J) for J in F),
```

where `F` ranges over collections of pairwise disjoint donor intervals,
including the empty collection.

**Proof.** For any source subset, decompose its nonempty donor union as in
Theorem 1. Each group's source count is at most `n(J)`, and there are at most
`e` empty sources. Its deficit is therefore at most the right-hand side.

For the reverse inequality, choose any disjoint interval collection `F`.
Take all empty sources and every source whose nonempty window is contained
in one of its intervals. These sources are distinct, because a nonempty
window cannot be contained in two disjoint intervals. Their donor union is
contained in the union of `F`; nonnegative capacities imply that its capacity
is at most `sum(C(J))`. The chosen sources thus have deficit at least
`e+sum(n(J)-C(J))`. Maximizing proves equality. QED.

Negative-scoring intervals can be omitted. Optimal disjoint intervals and
the trapped sources give an exact shortage certificate without counting a
shared donor twice. A maximum-flow solution gives the complementary feasible
partial allocation.

Writing `best(0)=0`, the nonempty-window term is computed by

```text
best(r) = max(best(r-1),
              max_{1 <= l <= r}(best(l-1) + n([l,r]) - C([l,r]))).
```

An optimal collection either avoids donor `r`, or has a last interval ending
at `r`; all earlier intervals then lie before its left endpoint. This proves
the recurrence. Computing containment counts directly costs `O(K L^2)`;
given those counts and prefix capacities the dynamic program costs `O(L^2)`.
The supplied checker uses doubled integer capacities for exact arithmetic.

## Consequence for the tile ledger

Retain the disjoint source/compensation/neutral/remainder partition of the
[weighted compensation lemma](GUARDED_HALF_DONORS.md), with `rho(A_i)<=1`,
`rho(D_j)<=-c_j`, and `rho(W)<=0`. Theorem 1 replaces the all-source-subset
Hall hypotheses by the donor-interval containment inequalities. When they
hold, `q<=0`, giving coefficient one on that explicitly covered class.

Even when some interval tests fail, `K-delta` units can be allocated, and

```text
q <= K - sum(c_j) + rho(W) <= delta + rho(W).
```

The first inequality is always the stronger ledger statement. A positive
`delta` is a failure of the proposed incidence allocation: donors outside
the admissible windows may still make the total charge nonpositive. Neither
an allocation deficit nor a skipped positive-capacity donor proves failure
of the grid inequality.

Different sources may legitimately name the same donor region. It receives
one capacity arc in the flow, and appears once in the tile ledger. Repeated
route visits and raw residual capacity do not create extra negative charge.
This removes nesting and shared-candidate ownership as obstacles to the
allocation *test*, while preserving the need to prove interval incidence,
certified negative charges, and control of the remainder.

The `6 x 20` closed-successor witness illustrates the diagnostic role of
`delta`. If the source is assigned only its central child interval, whose
capacity is zero, the interval model has `delta=1`. If the two actual outer
negative tiles are included in the source's ordered window, the intervening
tiles are zero-capacity holes and the same model has `delta=0`. The latter is
the correct incidence description for compensation; the former measures only
the failure of the child-only charging rule.

If an actual window omits only zero-capacity donors from an interval, filling
those holes preserves every Hall union capacity. The same theorems apply to
the filled intervals. Arbitrary positive-capacity holes need not be intervals
and remain outside this reduction.

## Laminar forest corollary

The shrinking-band forest is a direct sufficient condition for `delta=0`.
Index terminal bands on one ordered donor row. For each source root `A_i`, let
`I_i` be the interval from its leftmost to rightmost terminal descendant, and
assume:

1. terminal descendants of different roots are tile-disjoint and their
   intervals are disjoint;
2. each terminal has a nonnegative capacity, and the total capacity below
   every root is at least one; and
3. all internal successor intervals stay inside their root interval and are
   used only to identify descendants, not as additional source demands.

For any donor interval `J`, the roots with `I_i` contained in `J` have disjoint
terminal descendants. Their total terminal capacity is at least their number,
and all those terminals lie in `J`. Hence `n(J) <= C(J)`. Theorem 1 gives
`delta=0`, regardless of how deeply the internal successor intervals nest.

This is the allocation form of the existing branching compensation theorem:
the geometric forest proof supplies the disjoint leaf ownership, while the
interval deficiency theorem supplies the cross-root Hall step. A branch that
turns, merges, shares a positive-capacity terminal, or leaves a root interval
breaks one of these hypotheses and must be measured by `delta` instead.

## Two-source overlap rule

For two nonempty source windows `I_1` and `I_2`, the full interval test has a
particularly transparent form. Let `U=I_1 union I_2`, which is the interval
from the smaller left endpoint to the larger right endpoint. Then `delta=0`
if and only if

```text
C(I_1) >= 1,
C(I_2) >= 1,
C(U) >= 2.
```

The first two inequalities pay the sources individually; the third prevents
their overlapping portions from being spent twice. If the individual tests
pass but `C(U)<2`, the exact shortage is `delta=2-C(U)`. In particular, two
sources that can reach only one shared unit of donor capacity have `delta=1`,
even though each source passes its own local test. This is the smallest
cross-component shared-terminal obstruction and is independent of residual
route names.

## Verification scope

Run `python3 develop/check_interval_hall_deficiency.py --output /tmp/interval-hall.json`.
It compares three independent quantities: exhaustive subset deficiency,
disjoint-interval dynamic programming, and integral maximum flow on doubled
capacities. Exhaustive families include empty, repeated and nested windows;
specific controls exercise zero-capacity holes and separated simultaneous
shortages. Coordinate feasibility is not inferred from these incidence tests.
The general results above are written proofs; no new Lean result, arbitrary
bent-path theorem, manuscript addition or arXiv replacement is claimed.
