# A shared mixed gate in a completely frozen grid

24 October 2026. Authors: Haobo Ma and Wenlin Zhang.

We give an explicit feasible, completely frozen grid in which two different
bent alpha paths have horizontal links into the same mixed path. That mixed
path has access to two distinct, unreserved physical interval units. On the
declared relay-only rule, source-to-resource reachability has matching value
2, but legal compensation has value 1. In the full physical network both
alpha paths have other exits and can be paid, with no cancellation links.

Thus complete freezing does **not** imply the source-separation hypothesis of
the quota-to-route bridge lemma. This is a physical realization of the
previous abstract shared-gate obstruction, with the exact limitation of the
local rule made explicit. It is not a counterexample to the global grid
inequality, and does not exclude source separation for a more carefully
selected set of residual sources or relays.

## 1. The physical configuration

Use coordinates `(row,column)` starting at zero, in a `14 x 16` rectangle.
`T` means selected, `P` means a matching endpoint, and `.` means blank.

```text
................
....T.T.........
....PPPT....T...
....PP.....TP...
..T.PP.T.T..PPT.
.TP.PPPPPP..PP..
..PPPPPPPPPPPP..
..PPPPPPPPPPPP..
..PPPPP.PP.PPPT.
.TPP..T.PPPP....
...PT..TP.PPPT..
...T....T.T.T...
................
................
```

The 32 matching edges are the following unordered pairs:

```text
(2,4)-(3,4)    (2,5)-(2,6)    (3,5)-(4,5)    (3,12)-(4,12)
(4,4)-(5,4)    (4,13)-(5,13)  (5,2)-(6,2)    (5,5)-(5,6)
(5,7)-(6,7)    (5,8)-(6,8)    (5,9)-(6,9)    (5,12)-(6,12)
(6,3)-(6,4)    (6,5)-(6,6)    (6,10)-(6,11)  (6,13)-(7,13)
(7,2)-(7,3)    (7,4)-(7,5)    (7,6)-(7,7)    (7,8)-(8,8)
(7,9)-(7,10)   (7,11)-(7,12)  (8,2)-(9,2)    (8,3)-(8,4)
(8,5)-(8,6)    (8,9)-(9,9)    (8,11)-(9,11)  (8,12)-(8,13)
(9,3)-(10,3)   (9,8)-(10,8)   (9,10)-(10,10) (10,11)-(10,12)
```

Every listed edge is a grid edge, no endpoint is repeated, and these are
exactly the 64 positions labelled `P`. There are 20 selected positions. Each
selected position has at most one neighbour in `T union P`, so this is a
feasible selected-set/matching configuration.

## 2. A strict freezing certificate

Write `mate(v)` for the actual matching partner of an endpoint. The freezing
process starts with no frozen endpoint. An endpoint freezes when it has at
least two neighbouring positions that are selected, or whose matching
partners froze earlier.

Here is a general certificate criterion, used for this particular witness.
Assign each endpoint a nonnegative integer rank. Suppose every endpoint `v`
has two distinct grid neighbours `w` such that either `w` is selected, or `w`
is an endpoint and `rank(mate(w)) < rank(v)`. Then all endpoints freeze.
Indeed, induction on the rank shows that every endpoint of rank `j` freezes
after the endpoints of ranks less than `j`. The strict inequality prevents
a cyclic assumption, including a dependency on `v` through its own mate.

For the configuration in Section 1 the following rank classes form such a
certificate:

```text
0:  (2,6) (3,12) (5,2) (10,3) (10,8) (10,12)
1:  (2,4) (4,13) (9,2) (10,10)
2:  (3,5) (5,12) (7,2) (8,3) (9,9) (9,11)
3:  (4,4) (6,3) (6,13) (7,4) (8,8)
4:  (5,5) (6,5) (7,9) (7,12) (8,5) (8,13)
5:  (5,7) (6,11) (7,6) (7,11) (8,11)
6:  (6,6) (6,7) (6,8) (7,7) (7,10) (8,12)
7:  (5,6) (5,9) (6,4) (6,9) (7,5) (7,8) (7,13) (8,6)
8:  (5,4) (5,8) (6,10) (6,12) (7,3) (8,4) (8,9)
9:  (4,5) (5,13) (6,2) (8,2) (9,8) (9,10)
10: (3,4) (4,12) (9,3) (10,11)
11: (2,5)
```

For example `(10,8)` has selected neighbours `(10,7)` and `(11,8)`, so
has rank zero. The shared entrance `(5,8)` has neighbouring endpoints
`(5,7)` and `(5,9)`, whose mates `(6,7)` and `(6,9)` have ranks 6 and 7;
both are less than its rank 8. The report supplies two explicit witnesses
for every one of the 64 endpoints. Checking the displayed coordinates and
strict ranks proves complete freezing; it is not an inference from a finite
search failing to find a counterexample.

## 3. Two bent alpha paths and their common mixed path

Band `b` consists of the row pair `(2b,2b+1)`. Represent its column `c` by
`(b,c)`. Form the actual-matching PP-path decomposition: matching edges join
these band columns, and a PP column has degree two. The three relevant
paths, listed as sequences of band columns, are:

```text
A: (1,12),(2,12),(3,12),(3,11),(3,10),(3,9),(2,9)
B: (2,2),(3,2),(3,3),(3,4),(3,5),(3,6),(3,7),(2,7)
g: (2,8),(3,8),(4,8),(5,8)
```

The physical terminal pairs are

```text
A: (3,12), (5,9)     both TP
B: (5,2),  (5,7)     both TP
g: (5,8) BP, (10,8) TP.
```

The paths have respectively 6, 7 and 3 actual matching edges. `A` and `B`
are bent and are different original alpha owners. The two additional
permitted horizontal terminal links are

```text
(5,9) -> (5,8),       (5,7) -> (5,8).
```

Consequently the mixed owner `g` is reachable from both alpha sources even
by a single link. This directly disproves the blanket implication
“complete freezing implies source separation” for the original strand system.

## 4. Two actual resources, but one unit of mixed capacity

At the exit `(10,8)` of `g` there are two available interval accesses:

* `Rright` is the BB column `(b,c)=(5,9)`, consisting of `(10,9),(11,9)`.
  It is directly adjacent to the TP column `(5,8)`.
* `Rleft` is the BB column `(5,6)`, consisting of `(10,6),(11,6)`.
  The intervening column `(5,7)` consists of selected `(10,7)` and blank
  `(11,7)`, and provides the selected-cap access from `(10,8)`.

These are distinct original singleton interval units. Neither is a left
or right boundary mark. They do not share a selected cap or a BB column.
The resource identities are retained before any cancellation.

Consider the **restricted rule** with alpha sources `A,B`, mixed gate `g`,
the two displayed links, and only the two accesses at the exit of `g`.
All other source exits and all other strand resources are omitted from this
rule. Its source-resource reachability projection is `K_{2,2}`. It therefore
has a matching of size 2, for example `A -> Rleft, B -> Rright`.

Legal compensation in this rule has value exactly 1. Both links use the
same BP terminal `(5,8)`, so at most one belongs to a terminal matching.
After choosing one link, the resulting alpha has the free TP `(10,8)` and
can use either resource, giving value at least 1. No other source has a
declared interval access. Thus the optimum is 1, the minimum link cost is 1,
and the shortfall from the projected quota is exactly 1. Equivalently,
deleting the single mixed owner separates both sources from both resources.

This realizes the earlier abstract gate obstruction inside a completely
frozen grid. Distinct final resource identities do not prevent reuse of
an intermediate mixed strand. It is the relay-only rule that fails here.

## 5. What survives in the full network

The full physical network has two simple bypass payments:

* `A` uses its other TP `(3,12)` and the BB unit `(1,13)`;
* `B` uses its other TP `(5,2)` and the BB unit `(2,3)`.

Both units are unreserved, distinct and directly accessible. Thus the full
network pays both alpha sources using zero cancellation links: `nu=2`,
minimum cost `0`. The local relay cut is not a cut of that full network.
In particular, these alphas would already disappear under a preprocessing
step that pays these bypasses. The example does not rule out a theorem
about sources remaining after such a step.

For reference the full original ledger is

```text
alpha = 2, beta = 2, mixed = 5,
balance = 60, boundary budget = 14, surplus_twice = 120.
```

Here `balance` is `#BB - #TT` in the column ledger, and
`surplus_twice = 2*(balance+beta-alpha)`. The boundary-adjusted margin is
`120 - 2*14 = 92`, so this configuration has ample exterior surplus.

The next geometric question must therefore retain how sources are selected:
does there exist a simultaneous choice of bypass payments and residual mixed
routes whose unit capacities suffice? Applying a run-slot quota to *all*
reachable sources and then citing freezing to infer source separation cannot
answer that question. The full mixed-capacity network, or a proved residual
selection invariant, is still needed. No improvement of the universal `5/6`
bound is asserted, and the 11 October submitted manuscript is unchanged.

Update, 25 October: [first-destination allocation and an unported shared gate](FIRST_DESTINATION_ALLOCATION_AND_UNPORTED_GATE.md)
prove a simultaneous first-step allocation and exact beta-compensation formula.
A new frozen witness has no direct or selected-cap access at any original
alpha tip, so even maximum direct prepayment does not restore source separation.
Its full network still pays both sources, now by two different beta strands.

## 6. Reproduction and scope

Run the standard-library verifier:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 develop/check_frozen_shared_mixed_gate.py --output output/frozen-shared-mixed-gate.json
```

It checks feasibility, all strict freezing witnesses independently of the
peeling implementation, the three actual-matching paths, both physical
resource accesses and their boundary reservations, the restricted optimum
and its cut, and the full-network optimum. It repeats the certificate checks
under all eight grid isometries, carrying the band system with the grid.
The report includes the complete configuration and witnesses. No Z3 is needed
for verification. Discovery used Z3 5.3.1 in a fixed rectangle, followed by
deletion of three unnecessary selected positions; no minimality is claimed.

The explicit coordinate/rank certificate and the one-terminal capacity
argument are the proof. The eight transformed checks are regression checks,
not a proof of a general compensation inequality.

The Lean 4.33.0 module
`formal/SubQuorum/FrozenSharedMixedGate.lean` proves the general strict-rank
criterion from an inductive definition of endpoint freezing. It also checks
this witness's grid/matching feasibility, all 64 strict-rank certificates,
the three disjoint alternating physical paths and their terminal types,
the shared entrance, both resource locations, and the bypass locations.
In particular `all_endpoints_frozen` is derived from the inductive process.
The file passes locally with:

```sh
cd formal
lean SubQuorum/FrozenSharedMixedGate.lean
```

These are kernel-checked proofs using ordinary `decide`, with no `sorry`,
extra axioms or `native_decide`. The checked theorem dependencies are
`propext` and `Quot.sound`. The formal module does not formalize the general
strand-normalization/flow equivalence or optimize the full physical network;
the exact values in Sections 4 and 5 have the displayed elementary arguments
and the Python flow/cut checks.

An Oracle review was attempted through the independent broker (task
`f85e222e-91e5-4ae0-8613-8005e7cd54fd`), but failed with
`model_unavailable@selecting_model` and produced no review. No independent
ACCEPT is claimed for this new physical witness.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
