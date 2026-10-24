# A neutral relay need not force any negative region

2 October 2026. Continuation of the [same-direction capacity lemma](SAME_DIRECTION_CAPACITY_DONORS.md).
We give an exact full-grid counterexample to unconditional propagation from
a zero-capacity receiving tile to a negative compensation region.

## 1. The candidate rule and its scope

The capacity lemma proves rho(Q)<=-r(Q)/2 between the specified same-direction
saturated caps. Its unresolved receiving tiles have r=d=rho=0. A possible
next rule would assert that such a relay necessarily forces a negative tile,
component, or tile-aligned band elsewhere, even without a positive-source
hypothesis. The following construction refutes every version of that rule.
It shows why the next statement must use additional source or routing geometry.

## 2. Complete coordinate construction

Use an 8-by-8 grid with rows and columns indexed 0 through 7. Set

```text
T = {(0,0),(0,2),(0,3),(0,5),(0,7),(1,7),
     (2,0),(2,2),(2,4),(2,6),(3,1),(3,5),(3,7),
     (4,0),(4,2),(4,4),(4,6),(5,1),(5,3),(5,5),(5,7),
     (6,0),(6,2),(6,4),(7,0),(7,2),(7,4),(7,7)}.

M = {((1,1),(2,1)), ((1,5),(2,5)),
     ((3,3),(4,3)), ((5,6),(6,6))}.
```

All vertices not in T or incident with M are blank. The aligned tile labels are

| Tile row | column 0 | column 1 | column 2 | column 3 |
| --- | --- | --- | --- | --- |
| 0 | `TB/BP` | `TT/BB` | `BT/BP` | `BT/BT` |
| 1 | `TP/BT` | **`TB/BP`** | `TP/BT` | `TB/BT` |
| 2 | `TB/BT` | `TP/BT` | `TB/BT` | `TB/PT` |
| 3 | `TB/TB` | `TB/TB` | `TB/TB` | `PB/BT` |

The marked tile Q=(1,1) has the required `TP/BT` side caps, with their
P vertices matched upward to (1,1) and (1,5). Its own P at (3,3) is
matched downward to the saturated tile (2,1). Thus Q has
(t,p,s,r,d)=(1,1,1,0,0), and its upper guard (1,2) is blank.

## 3. Verification as an exact obstruction

**Proposition.** This pair is feasible, contains the specified deficient
same-direction neutral relay, and satisfies rho(S)=0 for every set S of
aligned tiles. All residual components have zero excess, and q=0.

**Proof.** The four edges have disjoint endpoints outside T and unit grid
length. For an explicit selected-neighbor check, the T--T edges are

```text
(0,2)--(0,3), (0,7)--(1,7),
(6,0)--(7,0), (6,2)--(7,2), (6,4)--(7,4).
```

These five edges form disjoint pairs. The selected vertices adjacent to P,
with their unique occupied
neighbor, are

```text
(0,5): (1,5),
(2,0): (2,1), (2,2): (2,1), (2,4): (2,5), (2,6): (2,5),
(3,1): (2,1), (3,5): (2,5),
(4,2): (4,3), (4,4): (4,3), (5,3): (4,3),
(4,6): (5,6), (5,5): (5,6), (5,7): (5,6).
```

These vertices are distinct
from the endpoints of the actual T--T edges; every remaining T has no
occupied neighbor. Hence every T has at most one occupied neighbor.

There are twelve saturated tiles. The four deficient tiles are
(0,0), (0,2), (1,1), and (3,3); each has t=1,p=s=1,h=0, so r=d=0
and rho=0. Saturated tiles have charge zero by the exact ledger. No matching
edge survives as a residual edge: each joins a saturated tile to a deficient
tile. Thus the residual graph consists of four isolated zero-capacity vertices,
and every component excess is zero. Additivity now gives rho(S)=0 for every
tile set S, including wider bands and unions of components. Finally
|T|=28, |M|=4, so q=32-64/2=0. QED.

## 4. What a transfer theorem still needs

The failed rule is "a neutral relay alone forces a negative region".
The construction has no positive residual component, so it does not refute a
transfer theorem whose hypotheses include a positive source and a justified
connection between that source and the relay. It also satisfies the grid target
with equality.

At a neutral receiving tile, saturated-attachment edges have been deleted
from the residual graph and d=0. A residual walk cannot pass through that
tile. Any transfer using its saturated neighbors must therefore introduce
and justify an auxiliary geometric incidence; those matching edges do not
provide residual reachability or negative budget by themselves.

The remaining concrete obligation is to relate the incoming positive source
or its pressure band to a compensating region, with enough joint capacity
for all sources that reach the same region. Weighted Hall remains the
allocation criterion; the relay labels alone cannot prove its hypotheses.

## 5. Reproduction

Run `python3 develop/check_neutral_relay_obstacle.py --output output/neutral-relay-obstacle-controls.json`.
The checker rechecks complete coordinates, matching feasibility, the canonical
residual ledger, the relay patch and all tile charges under eight symmetries.
Full coordinates, component data and source hashes are archived. The witness
was discovered by a finite MILP search; the explicit feasibility and charge
calculation above prove the counterexample without relying on optimality or
an enumeration claim. No new Lean validation is claimed.
