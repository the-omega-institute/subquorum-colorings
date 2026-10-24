# Single-tile donors after a failed pressure successor

1 October 2026. Continuation of [branching interval compensation](BRANCHING_INTERVAL_COMPENSATION.md).
The statements below use the exact tile ledger and feasibility convention of
[boundary-aware compensation](CROSS_COMPONENT_COMPENSATION.md). They remain
research material separate from the current joint manuscript.

## 1. A donor that does not need a pressure row

**Lemma 1 (capped single-tile donor).** In any feasible even-by-even rectangular
grid, let a tile Q have a saturated left neighbor `TP/BT` and a saturated right
neighbor `PT/TB`. Both displayed P vertices are matched upward, away from Q.
There is no hypothesis on the vertices above or below Q, or on their matching.
Then Q is deficient and

    rho(Q) <= -1.

In particular a width-one interval between receiving caps of a right-then-left
exit pair supplies a full unit of compensation even when its pressure row
contains selected or blank vertices.

**Proof.** Each cap's lower T already neighbors its own P. Its neighbor in Q
must therefore be B. Both lower corners of Q are B. An upper T in Q has the
lateral cap P as an occupied neighbor, so its other upper corner must be B.
Thus Q has at most one T and is deficient.

Let t,p,s be its selected, matching-endpoint and saturated-attachment counts.
If t=1, the other three corners are B; hence p=s=0 and
2rho(Q)=2t+p+s-4=-2. If t=0, all P vertices are upper and p<=2. No matching
edge leaves sideways, since the cap P's are already matched; none leaves
downward, since the lower corners are B. A saturated attachment upward forces
the other upper corner of Q to be B, by the forced-blank attachment lemma.
Consequently p=2 implies s=0; p=1 implies s<=1; and p=0 implies s=0.
In every case p+s<=2, and 2rho(Q)=p+s-4<=-2. QED.

The bound is independent of residual routing. If Q has an edge to another
deficient accounting region, its endpoint half is already included in rho(Q).
Neither both slack ports nor the whole residual component are counted again.

## 2. All neutral pressure bands have oriented outer exits

The preceding pressure lemma requires P immediately above the band's upper
row. It does not require the band's own upper row to be P. In a neutral such
band every deficient tile is neutral individually, and a saturated tile has
no P. The complete list of possible neutral label/exit states is:

| Labels | Saturated attachment |
| --- | --- |
| PP/PP | none |
| PP/BP | downward at lower-right: R |
| PP/PB | downward at lower-left: L |
| PP/BT, PP/TB | none |
| TB/BP | downward at lower-right: R |
| BT/PB | downward at lower-left: L |
| BP/TP, PB/PT | none |
| BB/TT, BT/TB, TB/BT | saturated, none |

This is a necessary local list; membership does not establish the existence
of a global matching. To derive it, an upper T must have both within-tile
neighbors B, and a lower T has at most one occupied within-tile neighbor.
For a deficient tile with t=1, p<=2. Neutrality says 2t+p+s=4, so either
p=2,s=0 or p=1,s=1. In the latter case the exit and its blank companion occupy
the lower row, and the upper T is opposite the exit. If t=0, neutrality gives
p+s=4; an exit requires a distinct lower blank companion, leaving either
p=4,s=0 or p=3,s=1. Saturated tiles have the three displayed T/B patterns.
These observations give precisely the table.

**Lemma 2 (outer-exit orientation).** Every neutral pressure band has a first
exit R and a last exit L. It has at least one consecutive R,L pair. If these
exits are in tile columns i<j, then j-i>=2, and their receiving tiles have the
two cap orientations of Lemma 1.

**Proof.** The side caps and P pressure prohibit upper-endpoint T vertices
and force lower endpoints B. The first tile can consequently be only PP/BT
or PP/BP. A PP/BT tile ends in a lower T that already sees an upper P, forcing
the next lower-left corner B. Its upper-right P and the pressure row also
prohibit an upper-left T in the next tile. The table then allows only PP/BT
or PP/BP again. A whole band of PP/BT tiles violates the right lower endpoint
B, so its first exit is R. Reflection gives a last exit L. The ordered list
must therefore contain a transition R,L. Their receiving saturated tiles are
TP/BT and PT/TB. If adjacent, their facing lower T vertices would each have
two occupied neighbors, contradicting feasibility. QED.

**Corollary 3 (mixed one-tile continuation).** If a consecutive R,L pair has
j-i=2, the intervening tile one row below has charge at most -1. No P pressure
row is required for it. If j-i>2 and every intervening parent tile is PP/PP,
the interval below is a pressure band, as in the previous successor lemma.

The first alternative allows a saturated diagonal or another mixed state
in the intervening parent tile. The second alternative uses only that
particular interval's lower row of P; the entire parent need not have an
upper row of P. Wider mixed intervals remain outside this continuation rule.

## 3. Forest accounting with mixed one-tile leaves

**Theorem 4.** Let K filled source corridors lie in the same tile row and
orientation, with disjoint full column spans including source end tiles.
Each has charge +1 and supplies its first pressure band. Require every
generated pressure band to be either:

- closed: sigma=0, giving a terminal band of charge at most -1; or
- neutral, with every consecutive R,L pair enclosing either a single tile
  or only PP/PP parent tiles.

Generate all these intervals one tile row below. A single-tile child is
terminal by Lemma 1, with arbitrary feasible labels. A wider child is a
pressure band and must satisfy the same recursive alternatives. Let D count
all terminal regions and W the deficient tiles outside source and band regions.
Then

    D >= K,
    q <= K-D+rho(W).

If rho(W)<=0, coefficient one follows on this class. The previous upper-row-P
forest is contained in this class, and the 6-by-14 mixed-neutral obstacle is
also included.

**Proof.** Lemma 2 gives every neutral node a child. Widths decrease by at
least two and tile rows increase, so recursion terminates. Two consecutive
R,L pairs cannot share an exit, so child intervals are disjoint. Descendant
intervals remain inside their parent interval, different depths occupy
different rows, and the roots have disjoint full spans. Hence each terminal
has one owner and no charged tile is reused. Each source contributes +1,
each neutral band zero, and each terminal at most -1 by the pressure lemma
or Lemma 1. Summing the exact ledger gives the inequality; each root has
at least one terminal, so D>=K. QED.

This is still a covered-class theorem. It does not establish the recursive
alternatives or rho(W)<=0 for an arbitrary grid configuration. In particular
it does not handle wide mixed intervals, overlapping roots, or rotated paths.
It strengthens the continuation mechanism without changing the universal
five-sixths theorem or resolving the unrestricted conjecture.

## 4. What happens in the 6-by-14 example

Use the complete coordinates in the preceding branching note. Its source
tiles are 0,...,6. The neutral band's five tiles are

    PP/BP, BT/TB, BT/PB, BP/TP, PP/PB.

The exits in tile columns 1,3,5 have orientations R,L,L. The first two supply
receiving caps in bottom tile columns 1 and 3. Their intervening tile 16,
at vertex rows 4,5 and columns 4,5, is `BT/BB`. Lemma 1 forces its full unit
of negative charge even though the row above it is TB. This donor lies in
a different residual component from the positive source.

The second donor, tile 18 at rows 4,5 and columns 8,9, is `BB/TB`. In this
particular matching it also has rho=-1. The exact decomposition is

    rho(source)=1, rho(parent)=0, rho(tile16)=-1,
    rho(W)=-1, q=1+0-1-1=-1.

Thus the missing P pressure does not prevent compensation in this witness:
the receiving caps alone force the first donor. The extra unit in W is
verified for this witness; Lemma 1 does not assert that every failed pressure
successor forces an extra unit in the unallocated remainder.

## 5. A closed wider successor can have no deficit

The single-tile lemma cannot be extended to an arbitrary closed interval
between R,L receiving caps. Here is a feasible 6-by-20 configuration:

```text
TPPPPPPPPPPPPPPPPPPT
BPPPPPPPPPPPPPPPPPPB
TPPPPBTBTBBTBTBPPPPT
BTBPPTBPBTTBPBTPPBTB
TBTPBBTPTBBTPTBBPTBT
BTBTBTBTBTTBTBTBTBTB
```

Take every displayed T as selected. With zero-based coordinates, match P by

    {((0,2i+1),(0,2i+2)): 0<=i<=8},
    {((1,2i),(1,2i+1)): 1<=i<=8},
    ((1,1),(2,1)), ((1,18),(2,18)),
    ((2,2),(2,3)), ((2,4),(3,4)),
    ((2,15),(3,15)), ((2,16),(2,17)),
    ((3,3),(4,3)), ((3,7),(4,7)),
    ((3,12),(4,12)), ((3,16),(4,16)).

The endpoints are disjoint and exhaust all P positions. Every T has at most
one occupied neighbor, directly checkable from the displayed six rows.
The source is the filled corridor of width eight, of charge +1. The inner
parent band, in rows 2,3 and tile columns 1,...,8, has states

    PP/BP, PB/PT, TB/BP, TB/BT, BT/TB, BT/PB, BP/TP, PP/PB.

It is neutral and has four saturated exits R,R,L,L, in tile columns 1,3,6,8.
Its only consecutive R,L pair is at columns 3,6. The candidate child below
is the two-tile interval in columns 4,5, with labels `TB/BT`, `BT/TB`.
Both tiles are saturated. The child has no P vertices, no matching edge
entering or leaving, sigma=0, and rho=0. The pressure row above it is BTTB.

The two negative tiles instead lie in bottom tile columns 2 and 7, outside
that R,L interval: their labels are `BB/BT` and `BB/TB`, respectively.
Each is an isolated residual component of charge -1. All other nonsource
deficient tiles are neutral. Hence

    |T|=32, |M|=27, mn/2=60, q=-1,
    component excesses: +1, six zeros, -1, -1.

This refutes the proposed rule that every consecutive R,L pair supplies
one unit from its closed child, even after removing the P-pressure condition.
The target inequality holds: 59<60. The negative resource may lie outside
every child produced by that pairing, so a proof restricted to those child
intervals still misses real cross-component compensation.

## 6. Verification

`python3 develop/check_mixed_neutral_donors.py --output
develop/results/mixed-neutral-donors-2026-10-01.json` checks the necessary local
capped-tile cases, neutral-word boundary/orientation conditions, and the
complete 6-by-14 and 6-by-20 coordinates in all eight rectangle symmetries. Matching
flips exercise capacity-two passages while preserving the accounting regions.
It also reuses the previously checked branching constructions as controls.
The general proofs are above; finite controls are not an all-grid proof or a
new Lean formalization. The current manuscript is unchanged.
