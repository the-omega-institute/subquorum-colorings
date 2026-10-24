# A frozen nonsingleton support tree with forced direct-interface rerooting

25 October 2026. Research branch only.

The previous [joint tree--beta theorem](JOINT_TREE_BETA_COMPENSATION.md)
had physical controls only for singleton deficient support trees. Here is a
completely frozen 12-by-18 example with a genuine two-vertex deficient tree.
Relative to a specified maximum interval baseline, its unique direct beta
repair **must change one old interval assignment**. Disjoint stacking gives
arbitrarily many simultaneous physical rerootings, with exact nonreuse.

This is a physical realization of the preceding mechanism. The cardinality
and weighted matching theorems are not being claimed again as new results.
The example has two marked boundary exits. Extending the board to the right
releases those exits and removes the tree defect; this boundary dependence is
part of the result. It does not exhibit a Hall failure or improve the universal
5/6 bound.

## 1. Coordinates and actual matching

Use zero-based coordinates, with T selected, P an endpoint of the actual
matching, and a dot blank:

```text
..................
........T.........
..T.T.........T...
..T.PT...T.TPPPT..
...TP.T.T.T.PP....
....PT.TP.PPPP....
..TPP.T.PPPPPPPT..
...PPPPPPPPPPPP.T.
.TPPPPPPPPP.PPPT..
..T.T.T.T.T.T.T.T.
..................
..................
```

The 23 actual matching edges are

```text
(3,4)-(4,4),   (3,12)-(4,12), (3,13)-(3,14), (4,13)-(5,13),
(5,4)-(6,4),   (5,8)-(6,8),   (5,10)-(6,10), (5,11)-(5,12),
(6,3)-(7,3),   (6,9)-(7,9),   (6,11)-(6,12), (6,13)-(6,14),
(7,4)-(7,5),   (7,6)-(7,7),   (7,8)-(8,8),   (7,10)-(7,11),
(7,12)-(7,13), (7,14)-(8,14), (8,2)-(8,3),   (8,4)-(8,5),
(8,6)-(8,7),   (8,9)-(8,10), (8,12)-(8,13).
```

All endpoints are different and avoid T. Directly count at most one occupied
neighbor at every selected point. The permanent fixture
`develop/fixtures/frozen_support_tree_reroot.json` supplies all coordinates
and ten strict freezing-rank classes. Every one of the 46 endpoints v has two
different nonmate neighbors that are selected or whose actual mates have
smaller rank. Induction over these ten ranks proves that all endpoints are
frozen. The verifier checks these witnesses independently using coordinates;
Lean checks all 46 instances and applies the general strict-rank induction.
Uniqueness of this matching is neither needed nor claimed.

## 2. Exact strand and gap account

Use the whole-board two-row bands (0,1),(2,3),...,(10,11). The PP decomposition
has exactly two alpha strands, one beta, eight mixed strands and three pure
two-edge PP cycles. The alpha tips and beta tips are

    A: (5,8), (8,8);    B: (5,10), (8,14);
    beta: (3,12), (5,11).

For a readable check, their walks on physical P endpoints, alternating actual
matching and within-band PP edges, are

```text
A: (5,8),(6,8),(7,8),(8,8)
B: (5,10),(6,10),(7,10),(7,11),(6,11),(6,12),
   (7,12),(7,13),(6,13),(6,14),(7,14),(8,14)
beta: (3,12),(4,12),(5,12),(5,11).
```

Consequently the P-column supports of A and B, in (band,column) notation,
are respectively

    A: (2,8),(3,8),(4,8);
    B: (2,10),(3,10),(3,11),(3,12),(3,13),(3,14),(4,14).

These are the **whole** strand supports, including internal PP columns. The
complete list of nonempty endpoint-free gaps adjacent to them is:

| Owner | Band | Gap columns | Column types | Available original interval units |
|---|---:|---|---|---:|
| A | 2 | 5--7 | BT, BT, BT | 0 |
| A and B | 2 | 9 | BB | 1 |
| B | 3 | 15--17 | BT, BT, BB | 0: column 17 is marked |
| B | 4 | 15--17 | BT, BT, BB | 0: column 17 is marked |

All other adjacent columns are P, so there is no additional endpoint-free gap.
Let J denote the original singleton BB unit at band 2, column 9, with physical
cells {(4,9),(5,9)}. Thus both A and B are eligible for J and **no other
unmarked original interval**. The support graph is the two-vertex tree A--J--B.
It has t=1 and interval-only optimum one.

The entire packet has 57 BB--TT interval units, twelve boundary marks, hence
45 available original units. The TT merger is retained: the 46 interior BB
sites must not be mistaken for 46 different interval resources. Counts are
|T|=29, |M|=23 and

    S-Boundary = 12*18/2 - 29 - 23 - 12 = 44.

With one interval used, U=44, beta=1 and t=1, agreeing with U+beta-t=44.

## 3. A forced reroot in the direct whole-beta interface

Among alpha--beta links the only possible one is

    (5,10) -> (5,11),                 B -> beta.

Neither tip of A is horizontally adjacent to either beta tip. B's other tip
(8,14) has no beta adjacency. Therefore the collapsed tree--beta graph has one
edge and mu=1. Fix the maximum interval baseline **B uses J, A is unpaid**.

Theorem: in this direct interface, maximum coverage is two, minimum extra beta
links is one, and minimum number of previously paid owners whose interval
assignment changes is one.

Proof: full coverage cannot use two interval units because A and B see only J.
It must use the sole beta, whose only possible alpha owner is B. Thus B must
release J and use the displayed beta link; A must receive J. This changes B's
previous interval assignment exactly once. The two original resources J and
beta are different and each is used once. The old paid demand B stays paid,
and the used original interval set remains exactly {J}. This attains both
lower bounds. Equivalently the old root A and beta root B have tree distance
one. After the link, B and beta form a mixed strand, A retains its support and
uses J. The current inventory is alpha=1,beta=0,t=0,U=44. QED.

This is relative to the stated baseline. Starting with A already using J
would allow beta payment of B with zero old assignment changes. Neither the
weighted theorem nor this example optimizes over an unspecified old baseline.

## 4. A wider mixed repair and a precise scope distinction

The same actual grid also has the mixed strand with tips BP (8,9), TP (8,10).
Instead select

    (8,8) -> (8,9).

It extends A to an alpha with tips (5,8),(8,10). That alpha can use a **new**
original interval K, the singleton BB at band 4, column 11, physical cells
{(8,11),(9,11)}. Keep B's old payment at J. Both original demands are now paid,
the old interval assignment is unchanged, beta is unused, and only one link
was added. The resources are distinct: J at band2/column9 and K at band4/column11.

The two valid accounts are

| Repair | Used intervals | Consumed betas | Old interval assignments changed | U + beta - t |
|---|---|---:|---:|---:|
| Direct beta reroot | J | 1 | 1 | 44+0-0=44 |
| Mixed extension | J,K | 0 | 0 | 43+1-0=44 |

Thus the direct theorem's minimum beta count is not the minimum when mixed
routes may open new interval resources. Nor does its forced change apply to
the larger class. The full terminal network has minimum link count one:
zero links can use only the common J, and either displayed one-link repair
attains full coverage. No flow solver is needed for this lower/upper proof.

## 5. General physical stacking and the boundary release test

For any integer q>=1, translate copies by (12i,0), i=0,...,q-1, inside a
12q-by-18 board. Occupied rows in one copy range from 1 to 9; the next copy's
first occupied row is 13. Thus selected vertices, matching endpoints and all
freezing witnesses remain disjoint and create no new occupied adjacency.
The translation stride is even, so bands and their interval identities stay
separate. Each band still has its two original boundary marks.

Each copy contributes its own tree, J, beta and root choice. Therefore, for
every q (not merely the checked q<=16),

    alpha=2q, beta=q, t=q, mu=q, |I|=45q, U=44q,
    S-Boundary=44q.

Relative to B_i -> J_i in each copy, direct joint full payment requires q
different betas, q links and exactly q old assignment changes. The proof in
Section 3 applies independently in each band block, and resources cannot
cross blocks. It preserves all q previously paid B_i owners and all q original
J_i identities. The alternative mixed construction uses q links, no beta and
2q distinct intervals, preserving all old assignments. This gives an
unbounded simultaneous physical family, not an arbitrarily long single tree.

Boundary dependence can also be computed for every r>=1. Extend just the
right side of the original board by 2r blank columns, leaving T and M fixed.
The old column17 units of B are now unmarked. Each of its two right-hand gaps
has exactly 2r available BB units at columns17,...,16+2r, before the new last
column17+2r is marked. A still sees only J. Pay A with J and B with the old
column17 unit in band3: no link or beta is needed. The resulting interval
component has a private resource and is not deficient. Precisely

    |I|=45+12r, interval optimum=2, t=0, beta=1,
    U=43+12r, S-Boundary=44+12r.

No occupied vertex changes, so the freezing proof survives. This rules out
presenting this witness as a defect stable under empty right padding. In
particular it does not settle the stronger search for interior deficient trees
or for different deficient trees competing for one whole beta.

## 6. Reproduction, discovery limits and formal coverage

The positive fixture was found with Z3, then recompiled and checked without
Z3. Run:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 develop/check_frozen_support_tree_reroot.py \
  --output output/frozen-support-tree-reroot-validation.json
PYTHONDONTWRITEBYTECODE=1 python3 develop/check_frozen_support_tree_formal.py \
  --lean /path/to/lean --output output/frozen-support-tree-lean-validation.json
```

The solver-free checks cover the base plus eight carried isometries, sixteen
separated stacks, sixteen right-padding controls, every one of the 1,980 legal initial terminal matchings C0,
and independent flat allocation optimization. Among those fixed-C0 controls,
504 have a nonsingleton deficient support tree and a positive physical reroot
cost. Every proposed beta link is actually executed and retained original
interval witnesses are rechecked. The fixed baseline/reversed baseline and
wider mixed alternative are retained as separate controls.

Discovery receipts include a second two-vertex fixture, and a restricted
competition template with three designated alphas, two designated mixed
destinations, one common beta and only the target shared unmarked gap. That
template is UNSAT at12x18, and UNKNOWN after60s at14x20. The UNSAT verdict is
only for those explicit constraints and that board size; the timeout is not
nonexistence evidence. No general Hall expansion proof follows from either.

The Lean module audits the actual geometry, all46 frozen endpoints, full PP
partition into11 paths/3cycles, alpha/beta inventory, direct beta asymmetry,
whole original-alpha support access at all interior BB sites, both marked
exits, singleton shared gap, explicit mixed alternative and numeric/stacked
ledger. Thirteen new theorem axiom audits pass, plus sixteen dependency audits,
without warnings, sorry or native evaluation. The45-unit BB--TT forest count,
all-q geometric stacking/right-padding
and general matching optimality remain written proofs with finite regression
checks. The prior generic reroot module covers arbitrary indexed path length.
No universal grid bound, external review or matching uniqueness is claimed.
