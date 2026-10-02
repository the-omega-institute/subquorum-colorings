# Same-direction capped tiles: capacity donors and neutral relays

2 October 2026. This note extends the [guarded half-donor lemma](GUARDED_HALF_DONORS.md)
using the exact ledger of [cross-component compensation](CROSS_COMPONENT_COMPENSATION.md).
It is research material separate from the journal manuscript.

## 1. Definitions and geometric hypothesis

Work in a feasible pair (T,M) on an even-by-even rectangular grid, tiled by
aligned 2-by-2 squares. T denotes selected vertices, P matching endpoints,
and B blank vertices. Every T has at most one occupied neighbor.
For a deficient tile Q (t(Q)<2), let t count selected vertices, h internal
matching edges, s endpoints matched to saturated tiles, r=2-t-h-s the
residual capacity, and d the degree after removing saturated attachments.
The exact charge is rho=d/2-r. Saturated tiles have charge zero, and the
charges sum to q=|T|+|M|-mn/2. A residual edge crossing two regions contributes
one endpoint half to each region.

Normalize Q to {0,1} x {0,1}. Its two lateral neighbors have labels

```text
left cap   Q       right cap
TP         ??      TP
BT         ??      BT
```

Both cap P vertices are matched upward, away from Q. Thus the cap edges are
(0,-1)--(-1,-1) and (0,3)--(-1,3). The caps are saturated. No guard or
condition on the tiles above and below Q is assumed. Reflection gives L,L;
rotations give the other cap directions.

## 2. The capacity lemma

**Lemma 1.** Under this geometric hypothesis, a deficient Q satisfies

```text
h=0,   d=p-s,   r=2-t-s,
d <= r,   rho(Q)=-(r+2-t-p)/2 <= -r/2 <= 0.
```

In particular, r=1 supplies at least one half-unit and r=2 at least one unit.
Both constants are sharp. A saturated Q has charge zero.

**Proof.** The left cap's lower-right T already sees its own P, forcing
Q's lower-left corner B. The right cap's upper-left T likewise forces Q's
upper-right corner B. The only potentially occupied corners of Q are its
upper-left and lower-right corners. They are diagonal, so t+p<=2 and h=0.

An upper-left P cannot match internally, since both internal neighbors are B;
it cannot match left, since the cap P is already matched. It can therefore
match only upward. A lower-right P can similarly match only downward: its
right neighbor is cap B and its internal neighbors are B. Of these p edges,
exactly s are removed as saturated attachments. Thus d=p-s and r=2-t-s.
Subtracting gives r-d=2-t-p>=0, and substituting into rho=d/2-r gives the
displayed identity and bound. Since s<=p, r>=0 as well. This proves the
statement in arbitrary ambient configurations, including bent residual paths
and capacity-two tiles. QED.

The proof uses capacity only after establishing d<=r from this particular
geometry. Capacity alone is not a donor budget on arbitrary deficient tiles.
The vacancy term 2-t-p can strengthen the budget beyond r/2.

## 3. Exact zero-charge classification

**Corollary 2.** A deficient same-direction capped tile has zero charge if
and only if both surviving corners are occupied and every P there is matched
to a saturated tile. Equivalently its labels and attachments are one of

| Q labels | Required saturated attachment(s) | t,p,s | r,d |
| --- | --- | --- | --- |
| `TB/BP` | lower-right P downward | 1,1,1 | 0,0 |
| `PB/BT` | upper-left P upward | 1,1,1 | 0,0 |
| `PB/BP` | upper-left upward and lower-right downward | 0,2,2 | 0,0 |

The remaining zero-charge possibility is the saturated tile `TB/BT`.

**Proof.** For a deficient tile, Lemma 1 gives
2rho=-r-(2-t-p), a sum of two nonpositive terms. Equality requires r=0
and t+p=2. Substituting into r=2-t-s yields s=p. Conversely these conditions
give d=0 and rho=0. The three rows list all nonsaturated ways to occupy
the two surviving corners. The geometric hypothesis fixes each P direction.
Every deficient zero tile is therefore an isolated residual vertex of
capacity zero; it supplies no compensation. QED.

Consequently the proposed rule "every deficient same-direction gap supplies
one half-unit" is false. Replacing "deficient" by "positive residual capacity"
gives a valid rule with a general proof.

## 4. Sharp witnesses and the deficient obstruction

Keep the two caps and their edges specified above. All unspecified vertices
are blank. Translation by (2,2) embeds each construction in a 6-by-6 grid.

* **Sharp r=1:** Q=`TB/BP`, edge (1,1)--(2,1), with the other corners of
  its receiving tile blank. Then (t,p,s,r,d)=(1,1,0,1,1), rho=-1/2.
  The upper entry guard (-1,0) is blank, so the old guarded lemma does not apply.
* **Sharp r=2:** Q=`PB/BP`, edges (0,0)--(-1,0) and (1,1)--(2,1), with
  both receiving tiles otherwise blank. Then (t,p,s,r,d)=(0,2,0,2,2), rho=-1.
* **Deficient neutral relay:** use the sharp r=1 construction but put
  T at (2,0) and (3,1), making its lower receiving tile `TP/BT` saturated.
  Now (t,p,s,r,d)=(1,1,1,0,0), rho=0. The full grid has |T|=7, |M|=3,
  q=-8. It refutes the deficient-gap donor rule, not the target q<=0.
* The reflected relay, the two-attachment neutral relay, and the saturated
  zero tile are also archived to check every row of the classification.

## 5. Single-use allocation and the conditional improvement

Give each distinct deficient capped tile Q capacity c(Q)=r(Q)/2, or the exact
local budget (r(Q)+2-t(Q)-p(Q))/2 if all these data are tracked. Both follow
from Lemma 1. A tile may also have an older full or guarded certificate;
its budget is a single verified bound on -rho(Q), never the sum of certificates.
Identify resources by tile coordinate, not by certificate or orientation.
If a compensation band includes Q, either use the band as one resource or
partition it and prove the separate bounds; do not count Q again.

For K pairwise tile-disjoint sources of charge at most one, disjoint donors D,
neutral regions N, and remaining deficient tiles W, the exact ledger gives

```text
q <= K - sum(c(Q) for Q in D) + rho(W).
```

If the geometrically justified source-to-donor incidence satisfies
sum(c(Q) for Q in neighbors(X))>=|X| for every source subset X, weighted
Hall supplies a fractional assignment using each budget at most once.
Together with rho(W)<=0 this proves q<=0, hence |T|+|M|<=mn/2 on that
covered class. This is coefficient one in place of the universal 5/6 bound
6|T|+5|M|<=3mn. The ledger and Hall proof are those of
[weighted Hall compensation](GUARDED_HALF_DONORS.md#boundary-deficits-as-fractional-donors).

The new lemma enlarges the available local donors: its sharp r=1 witness
has no occupied guard, and its r=2 witness supplies a full unit. It does not
prove that arbitrary sources can reach enough donors. Neutral relay tiles
remain precisely the cases for which a wider band, bend, or global routing
argument must supply compensation. The earlier unguarded parent states
`PP/BT` and `TB/BT` describe tiles in the neutral pressure band above Q;
their zero charge is compatible with this receiving-tile lemma.

## 6. Reproduction

The [all-neutral relay completion](NEUTRAL_RELAY_OBSTACLE.md) shows that a
zero-capacity relay does not unconditionally force any negative region, even
in a complete finite grid. It leaves source-dependent transfer as the relevant
next hypothesis.

Run `python3 develop/check_same_direction_capacity_donors.py --output output/same-direction-capacity-controls.json`.
The checker tests 16 necessary local algebraic models, full coordinate
witnesses for sharpness and all zero types under eight symmetries, and the
canonical residual ledger. It records coordinates, routing, component
charges and source hashes. These are finite controls for the written proof;
no new Lean verification or arbitrary-grid allocation theorem is claimed.
