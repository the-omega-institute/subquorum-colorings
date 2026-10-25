# Two dead forced escapes, and an exact shared-relay compensation lemma

25 October 2026. Wenlin Zhang and Haobo Ma. Isolated research branch.

The [one-dead escape](DEAD_FORCED_MIXED_ESCAPE.md) leaves a possible rescue:
perhaps at least one of the two outward alternatives at a two-alpha mixed
fork must be productive. That rescue is false. We give a **beta-free,
completely frozen 56P/26T board** with a productive vertical mixed receiver
and two distinct, rank-forced, horizontal-BP mixed escapes, both dead in the
complete original resource pool.

The full board still pays its two alphas with zero links. More usefully,
we identify all its original payment routes and prove an exact compensation
and minimum-link formula for **every subset of its original intervals**.
The proof is a general two-source shared-relay lemma with support containment.
It distinguishes a second original unit from a second route through the
same capacity-one owner. No universal 5/6 improvement is claimed.

## 1. A two-sided physical obstruction

Use rows 0,...,13, columns 0,...,27, and the original bands (0,1),(2,3),... .
Selected points are T, actual matching endpoints P, and blanks dots:

```text
............................
............................
............................
........T...........T.......
......TPPT.T.T.T.T.TPPT.....
.......T..TPPPPPPPT..T......
............PPPPP...T.T.....
............PPPPP...PPPT....
..........TPPPPPPPPPPP......
...........PPPPPPPPPPP......
..........TP..PPPPPPPPPT....
...........T..T.T.T.T.T.....
............................
............................
```

The [fixture](../develop/fixtures/frozen_two_dead_mixed_escapes.json)
contains all 28 actual M edges, 26 selected points, and 13 strict freezing
layers of sizes 9,5,6,5,7,4,5,3,3,3,2,3,1. Its original open owners are
two alphas, no betas, and ten mixed owners. There is no physical deletion,
reservation or rematching in the following two-sided obstruction.

The source and receiving tips are

    A: (5,13), (10,11);    B: (5,15), (7,20);
    G: BP (5,14), TP (10,14).

Both source tips (5,13),(5,15) enter G's BP (5,14). These three points
have actual vertical mates (6,13),(6,15),(6,14), respectively. The
receiver-independent rank lemma from the preceding note forces their
outward BP alternatives. They are

    D_left : BP (5,12), TP (5,11), one actual horizontal M edge;
    D_right: BP (5,16), TP (5,17), one actual horizontal M edge.

They belong to different original owners. Each has empty whole support,
even including marked boundary BB columns, and only a self TP--BP output.
For D_right the right gap is BT at column 18, TB at column 19, then PP at
column 20. For D_left the left gap is TB at column 9, BT at column 10,
then PP at column 8. Neither gap contains a BB column. Their inner sides
are immediately blocked by source TP columns 13 and 15; they have no PP
body elsewhere. Thus neither escape is productive.

G is productive: its whole support consists of two different original,
unmarked singleton intervals (band 5,col 12),(band 5,col 13). This is a
fully frozen counterexample to **at least one outward H escape at a
productive two-alpha vertical mixed fork must be productive**. Previous
UNSAT results for a specified receiver location did not prove that claim.

## 2. Complete original routing and resource identities

Remove only self-links from the owner routing graph. All its nonself
links, including the two dead ones, are:

```text
A:(5,13) -> D_left:(5,12)
A:(5,13) -> G:(5,14)
B:(5,15) -> G:(5,14)
B:(5,15) -> D_right:(5,16)
B:(7,20) -> H_private:(7,21)
G:(10,14) -> H1:(10,15)
H1:(10,16) -> H2:(10,17)
H2:(10,18) -> H3:(10,19)
H3:(10,20) -> H4:(10,21)
```

Here H_private and H1,...,H4 are horizontal one-M-edge mixed owners.
H1,H2,H3 have no support, H4 has a support pool, and H_private has its
own support pool. The two remaining mixed owners are alpha-unreachable;
their original intervals remain present but cannot pay a source.
This list is checked against **all** original nonself links, not just
against the routes in a selected local rule.

Name the following sets of ORIGINAL interval identities:

| Pool | Original whole support | Size | Minimum route cost |
|---|---|---:|---:|
| L | W(A): band 4, cols 1--9; band 5, cols 1--9 and 12--13 | 20 | A directly, 0 |
| R | W(B): band 3, cols 17--19 | 3 | B directly, 0 |
| X | W(H_private): band 3, cols 24--26 | 3 | B via private H, 1 |
| S | W(G): band 5, cols 12--13 | 2 | either source via G, 1 |
| Y | W(H4): band 5, cols 24--26 | 3 | either source via G,H1,...,H4, 5 |

Every listed unit is an unmarked singleton interval. L,R,X,Y are pairwise
disjoint, while **S is a subset of L**, not two extra resources. All paths
to S or Y through G consume the SAME capacity-one mixed owner G.
The private H and the four tail owners are otherwise disjoint from the
sources and G. Consequently the H forest compression preserves exactly
these route costs and conflicts. A and B can also use their displayed
direct supports; those witnesses cannot be discarded because the question
started with a shared gate.

In the full original pool choose, for example, (band 5,col 12) for A and
(band 3,col 17) for B, without selecting any link. Thus V=2 and c=0.
This remains a counterexample to a **rule**, not to complete compensation.

## 3. General two-source shared-relay lemma

**Theorem 1 (exact support-shadow relay compensation).** Let L,R,X,Y be
pairwise disjoint sets of original unit identities and S subset L. There
are two sources A,B, private route owners disjoint from each other, and
one shared relay gate of capacity one. After removing nonpaying self-cycles,
the complete set of paying route types is:

    A -> L directly, cost 0;
    B -> R directly, cost 0;
    B -> X privately, cost p;
    A or B -> S through the shared gate, cost h;
    A or B -> Y through the shared gate, cost z.

Assume p,h,z are nonnegative, each type has its stated cost for every
resource in its pool, and the only simultaneous-route conflicts are
source identity, original resource identity and the one shared gate.
In particular there is at most one selected S/Y gate route in total.
Resources outside these pools may exist but have no source route.

For any available original pool Q put

    l=|Q∩L|, r=|Q∩R|, x=|Q∩X|, s=|Q∩S|, y=|Q∩Y|.

Build the following list C2 of costs, including a row exactly when its
condition holds:

| Condition | Two-payment certificate | Cost |
|---|---|---:|
| l>0 and r>0 | A uses L; B uses R | 0 |
| l>0 and x>0 | A uses L; B uses private X | p |
| s>0 and l>=2 | A uses a different L unit; B uses S through the gate | h |
| l>0 and y>0 | A uses L; B uses Y through the gate | z |
| r>0 and y>0 | A uses Y through the gate; B uses R | z |
| x>0 and y>0 | A uses Y through the gate; B uses private X | z+p |

If C2 is nonempty, the maximum payment is 2 and its minimum cost is
min C2. Otherwise build C1 from cost 0 when l+r>0, cost p when x>0,
cost h when s>0, and cost z when y>0. A nonempty C1 gives payment 1
at cost min C1; if C1 is empty, payment and minimum cost are both zero.

**Proof of achievability and resource accounting.** Each row of C2 uses
one source each. Distinct L,R,X,Y pools cannot share a resource identity.
For the third row, choose j in Q∩S. Since Q∩L has at least two different
units, choose k in Q∩L with k≠j. Pay B using j through the shared gate,
and A directly using k. The inclusion S subset L gives no extra copy
of j. Each row has at most one shared-gate route; the private route
owners are disjoint, so these are actual simultaneous certificates.
Their costs are exactly displayed. Each C1 entry is a single legal route.

**Proof of exhaustiveness and optimal cost.** A single paying route is
one of the five declared types, proving C1's exactness when two payments
are impossible. Consider two paying routes. They cannot both traverse
the shared gate. If neither does, A must use L and B must use R or X,
giving the first two rows. If B alone uses the gate, A uses L. A Y output
gives the fourth row. An S output requires a different L unit for A,
giving exactly s>0,l>=2 and the third row. If A alone uses the gate,
B uses R or X. A Y output gives the last two rows. An S output can be
replaced by A's direct access to the SAME unit of L: S subset L. This
preserves resource identities, frees the gate and costs no more because
h>=0. It reduces to the first two rows. Hence every two-payment packing
has cost at least a displayed feasible row, and every displayed row is
attainable. The stated optimum follows. QED.

This is a general counting and cost lemma, not an empirical classification.
Its hypotheses concern the **complete** route set and gate conflicts;
they must be checked before applying it to another physical board.
There is no claim that arbitrary mixed frontiers satisfy these hypotheses.

## 4. Exact application, missing units and missing capacities

**Corollary 2 (all subsets in this frozen board).** With the original
pools of Section 2 and p=1,h=1,z=5, Theorem 1 gives the exact maximum
compensation V(Q) and minimum actual-link cost c(Q) for every subset Q
of the board's complete original interval set, excluding only the usual
marked extreme intervals initially. This includes Q=I itself.

**Proof.** The complete original link list, independent actual PP/M
decomposition, and whole supports give precisely the five route types.
There are no betas, so there is no beta-body fork payment omitted by an
ordinary-route description. Dead and alpha-unreachable owners cannot be
on a paying path. G's four-owner tail and B's private H have no other
entrances or outputs, so compressing them keeps costs 5 and 1 exactly;
the two G entrances each cost one. Original whole-support normal form
then equates route packing to physical cancellation/allocation payment.
All owner and original-resource conflicts are those of Theorem 1. QED.

Several consequences separate distinct possible failures:

- If Q contains two different Y units and nothing else reachable, both
  sources can individually reach both units, but V(Q)=1,c(Q)=5. G is a
  capacity-one cut. More Y units cannot raise V(Q).
- If Q contains just one S unit, V(Q)=1,c(Q)=0. A second different unit
  in L raises V to 2 at cost 1. Counting that one S unit once as a G
  resource and once as an A resource would be false compensation.
- One S unit and one R unit pay both sources at cost 0 through their
  direct supports. The fact that both sources can enter G imposes no
  mandatory congestion when a direct witness exists.
- One Y unit plus one X unit pay both at cost 6, using G for A and the
  private route for B. They do not share any mixed owner or original unit.

These Q restrictions are expressly chosen resource exclusions on the
original frozen board. They are **not** claims of deficits in its complete
pool. They explain why neither mere resource reachability nor mere counts
of forced exits settle compensation.

**Proposition 3 (arbitrary copies and resource subsets).** For every q>=1
translate the physical board by (14i,0), i=0,...,q-1. It remains feasible
and completely frozen, has 2q alphas, no betas, 10q mixed owners, and 2q
distinct dead forced escapes at q productive mixed forks. For any original
pool Q, its value and minimum cost are the sums of Corollary 2's values
and costs on the q copies. In particular the complete pool gives (2q,0),
and the union of the Y pools alone gives (q,5q).

**Proof.** Blank border rows separate all occupied points between copies;
transport each strict rank layer in parallel. Even row translations preserve
band alignment. No actual M edge, PP strand or horizontal terminal link can
cross copies, and each original interval belongs to one band's copy. Thus
the complete routing graphs and all resource identities form a direct sum.
Any packing restricts to one in each copy, while the disjoint union of copy
optima is legal. Values add, and the minimum cost at the sum of maximum
values is the sum of the individual minimum costs. The dead and productive
properties transport unchanged. QED.

## 5. Verification and formalization scope

The standard-library-only verifier checks the actual rank certificate,
independent strand reconstruction, complete nonself link list, all five
original pools and their exact identities. It verifies the formula on all
243 representative threshold patterns for S,L\S,R,X,Y selected 0,1,2
each, plus 120 random subsets of the **entire** original resource set.
Theorem 1, rather than these representative tests, covers all choices.
Seven full physical terminal-matching enumerations check 97,020 matchings
in total. An independent named-resource path-packing implementation also
checks 300 abstract models with varied set sizes and nonnegative costs.
Eight transported symmetry images and q=2,3,5 frozen copy controls pass.
The existing forest verifier also passes with both new fixtures included:
24 frozen boards and 96 physical value/cost comparisons, alongside the
unchanged 220 abstract comparisons and 100 serial certificates. The
[new regression receipt](../output/two-sided-dead-escape-forest-regression.json)
is separate from the earlier milestone receipts.

The [Lean module](../formal/SubQuorum/TwoSidedDeadEscape.lean) checks the explicit physical feasibility, all 56 inductively
frozen endpoints via a general strict-rank theorem, the disjoint critical
alternating strands and TP/BP types, both actual outward matching edges,
both empty BB supports including boundary, and both self-only outputs.
It also checks G's two original BB columns and their direct support at A.
The BB predicate includes every endpoint-free gap BB column, so its
emptiness does not rely on withholding resources. The general whole-support
adapter, weighted relay theorem, exact physical payment normal form and
all-copy geometry remain written proofs plus Python checks; this is not
an end-to-end Lean proof of the compensation formula or the 5/6 conjecture.
Local Lean 4.33.0 passes all 11 reported statements; one is axiom-free and
the others use only propext/Quot.sound. There are no warnings, sorry,
native evaluation or new axioms. The [formal receipt](../output/two-sided-dead-escape-formal-validation.json)
records the scope separately from the [computational receipt](../output/two-sided-dead-escape-validation.json).

Reproduce the computational checks from the repository root:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 develop/check_two_sided_dead_escape.py \
  --output output/two-sided-dead-escape-validation.json
```

The optional discovery program accepts an endpoint bound. SAT was used
only to find explicit candidates; smaller-bound UNSAT refers solely to
that fixed motif, board size and typed constraints, not global minimality.
No new Oracle review is claimed. The submitted manuscript stays unchanged.

The remaining global question is a geometric restriction on complete
source-to-resource cuts, retaining every direct support, every private
bypass and every original unit. Two dead forced exits are now a verified
possibility, so a proof cannot assume even one productive outward escape
per such fork. Support containment can instead make a shared-gate payment
avoidable; Theorem 1 gives an exact instance of how to use that fact without
duplicating the contained resource pool.
