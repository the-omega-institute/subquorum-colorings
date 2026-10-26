# True fixed-P maxima can have completely frozen rank-one elbow loss

26 October 2026. Wenlin Zhang and Haobo Ma. Independent research continuation.

**Theorem.** There is a feasible16-by-28 grid with a fixed actual matching
M of35 edges such that:

1. |T|=186 is the maximum over **all** feasible selections with this fixed
   endpoint set P (not just extensions of an earlier T).
2. All70 matching endpoints are strictly frozen, and all four alpha terminals
   have occupied degree three.
3. For its canonical mixed H/V directions and the complete original resource
   pool, the specified two-tile elbow has delta=1 and withdrawal loss r=1,
   with the target unpaid in every old maximum. Payment stays1, with link
   cost decreasing from1 to0.
4. One other P-free tile flip alone pays both sources; doing the elbow after
   that successful repair reduces payment from2 to1. All owner bodies,
   terminal/source identities and physical links remain invariant.

This resolves the exact-maximality question left open by
[selected-extension stability](FROZEN_ELBOW_SELECTION_SATURATION.md).
The implications “full freezing implies zero loss” and “true fixed-P
selection maximality plus full freezing implies zero loss” are both false.
The numerical target still has positive slack3. A favorable direction choice
pays all sources, so this is no optimized-N obstruction and no universal5/6
improvement. The11 October submitted manuscript is preserved.

The subsequent [destructive-exchange selection theorem](DESTRUCTIVE_EXCHANGE_CHOICE.md)
gives a positive exact algorithm under a simultaneous replacement adapter:
old access and action access compete for the same capacity-one withdrawal
token. On this board it selects E alone and preserves old b, while allowing
both E and F as alternatives. It does not assume that all enabled actions
should be applied.

The later [coordinated-pivot analysis](FROZEN_COORDINATED_PIVOTS.md) changes
one additional P-free direction bit on this same extremal board. Its resulting
start has no improving single P-free pivot among all 81 candidates, yet two
such pivots jointly pay both sources. The local-trap claim is proved by
classifying the only three new gaps that can support the unpaid source.

## 1. Explicit extremal feasible board

Retain exactly the35 actual matching edges and tile directions from the
[fully frozen construction](FULLY_FROZEN_ELBOW_WITHDRAWAL_OBSTRUCTION.md).
Rebuild the selected vertices as displayed below. T means selected, P is an
actual matching endpoint, and a dot is blank; coordinates are zero based.
The [permanent fixture](../develop/fixtures/fixed_P_maximum_fully_frozen_elbow.json)
stores the complete186-point list, all35 actual edges, all tile bits,
the12 strict freezing layers and their two physical witnesses.

```text
 0 T..TT.T.T.T.T.TT.T.T.T.TT.TT
 1 T.T..T.T.T.T.T..T.T.T.T..T..
 2 .T.TT.T.T.T.T.TT.T.T.T.TT.TT
 3 T.T..TPPPPPPPT..T.T.T.T..T..
 4 T.T.T..T.PPP...T.T.T.T.T.T.T
 5 .T.T.TT.TPPPT.TPPPPPPPPPT..T
 6 T.T.T..T.PPP.T..T.PPP.T..TT.
 7 T.T.T.T.TPPPT.TT.TPPPT.TT..T
 8 .T.T.T.T.PPP.T..T.PPP.T..T.T
 9 T.T.T..PPPPP..TT.TPPPT.TT.T.
10 .T.T.TPPPPPPPT..T.PPP.T..T.T
11 T.T.T.T.T.T.T.TT..PPPPP..T.T
12 ..T.T..T.T.T.T..TPPPPPPPT.T.
13 TT.T.TT.T.T.T.TT.T.T.T.T.T.T
14 ..T.T..T..T..T..T.T.T.T..T..
15 TT.T.TT.TT.TT.TT.T.T.T.TT.TT
```

Every selected vertex has at most one occupied nearest neighbor. Checking
that condition on the displayed finite set proves feasibility. The actual
matching endpoints are disjoint from T, and all actual edges have length1.
No restricted resource pool or artificial reservation is introduced.

The baseline tile direction is V exactly on

    [2,12)×[6,12), [4,14)×[18,24),
    [12,14)×[12,14), [10,12)×[16,18),

and H elsewhere. Always use maximal canonical same-direction bands.
E changes the empty tile(10,16) to H. F changes tiles(2,12),(4,12) to V.

## 2. The unrestricted maximum186 is proved by a geometric cover

Only P is fixed in this optimization. Feasibility is hereditary under
removing selections. A site with at least two fixed P neighbors can never
be selected. In every2-by-2 square, three selections would give a selected
vertex two selected neighbors, so capacity is at most2. Where the candidate
sites are pairwise incompatible, capacity is at most1. Checking these
constant-size local conditions gives the aligned square capacities:

```text
2 2 2 2 2 2 2 2 2 2 2 2 2 2
2 2 2 1 1 1 2 2 2 2 2 2 2 2
2 2 2 2 1 0 2 2 1 1 1 1 2 2
2 2 2 2 1 0 2 2 2 0 1 2 2 2
2 2 2 1 0 0 2 2 2 0 1 2 2 2
2 2 2 1 1 1 2 2 2 0 0 1 2 2
2 2 2 2 2 2 2 2 2 1 1 1 2 2
2 2 2 2 2 2 2 2 2 2 2 2 2 2
```

Their sum is189. Three disjoint4-by-2 rectangles replace six cap2 squares
by three cap3 members. Their six candidate sites are partitioned as follows:

| patch origin | forbidden pair1 | forbidden pair2 | forbidden pair3 |
|---|---|---|---|
| (2,12) | (2,12),(2,13) | (3,13),(4,13) | (5,12),(5,13) |
| (8,12) | (8,12),(8,13) | (9,13),(10,13) | (11,12),(11,13) |
| (10,16) | (10,16),(10,17) | (11,16),(12,16) | (13,16),(13,17) |

Each pair is adjacent and at least one endpoint has an additional fixed P
neighbor. Both endpoints cannot be selected; each rectangle therefore has
at most three selections. The complete cover is disjoint, so no cell or
capacity saving is charged twice. It proves |T|<=189-3=186 for every feasible
T with this P. The explicit board above attains186. This is a proof of
unrestricted optimality, independent of any optimizer or finite global search.
It is the same cover as in the preceding note, now with a fully frozen
attainer realizing the elbow obstruction.

## 3. Complete strict freezing

A frozen event for p uses two distinct physical neighbors, each either
selected or an actual endpoint whose actual mate froze at a strictly smaller
rank. The event can never use p's own actual mate as an earlier witness,
since that would require p itself at a smaller rank.

The stored certificate has12 layers of sizes

    8,10,7,9,9,5,7,6,3,3,2,1,

covering all70 endpoints. The eight first-layer endpoints are

    (3,6),(3,12),(5,15),(5,23),
    (10,6),(10,12),(12,17),(12,23).

Each sees two selected witnesses in the displayed board. At each later
layer the fixture specifies both witnesses and the earlier actual-mate
rank. Induction on the12 layers proves every endpoint frozen. The ranks
depend only on T and M, so the same complete certificate applies to all
four direction states. This is a full witness proof, not a degree inference.

A useful necessary-condition calculation helped find this attainer. Let D
be the sites individually selectable with P alone. For an endpoint p,
possible strict witnesses lie in

    ((physical neighbors of p) minus {M(p)}) intersect (P union D).

If this set has exactly two vertices, every external vertex in it must
be selected in any completely frozen feasible board. Otherwise p could
never have two strict witnesses. For this P the rule forces15 selections:

    (2,8),(2,12),(3,13),(4,17),(4,21),(8,7),
    (10,5),(10,13),(10,22),(11,6),(11,12),
    (12,16),(12,24),(13,17),(13,23).

In particular full freezing itself forces the elbow's two selected seals
(2,12),(3,13). These necessary conditions are not asserted sufficient;
the complete12-layer certificate proves sufficiency for the exhibited T.

## 4. Complete original resources and source reachability

Restoring every actual matching edge across direction changes gives two
alphas, two betas and five mixed owners. Name the alphas and the relevant
mixed owner by their free tips:

    a: TP(3,12), TP(10,12),
    b: TP(5,17), TP(12,17),
    z: TP(5,15), BP(5,16).

Each of the four alpha tips has exactly three occupied physical neighbors.
The source-reachable system is precisely a, b and z. Its only nonself link
is b(5,17)->z(5,16). a and z have no external exit. The remaining mixed owners
form two unreachable chains terminating in the two whole-beta owners:

    mixed BP(4,9)/TP(5,9)
      -> mixed BP(6,9)/TP(7,9)
      -> beta BP(8,9)/BP(9,7),

    mixed BP(6,20)/TP(7,20)
      -> mixed BP(8,20)/TP(9,20)
      -> beta BP(10,20)/BP(11,22).

Self links carry no additional source payment. Thus neither unreachable
beta stems nor forks can help a or b; all actual edges and whole betas
are present in the model.

There are exactly three positive original forest units in the baseline:

    Q={(4,13),(5,13)}, supported only by z;
    U={(11,16),(11,17)}, supported by no owner;
    R={(8,12),(9,12)}, supported by no owner.

No owner has any other interval support. The inventory identity gives

    L=3, alpha=beta=2,
    S=area/2-|T|-|M|=224-186-35=3=L+beta-alpha.

All forest cells and all whole-support incidences are checked, not just
resources near the elbow. Therefore the sole old payment is b->z->Q,
with one link; a is unpaid in every maximum. Deleting a leaves value1.
Deleting a and withdrawing Q leaves value0, proving withdrawal loss r=1.

## 5. Exact elbow loss and destructive joint repair

F is the previously proved reflected two-tile elbow. Its only P site is
(3,12), its selected seals are(2,12),(3,13), outside P guards are(4,11),(5,11),
and its above/below neighboring tiles are H. Its complete physical adapter
hypotheses hold. It replaces Q by

    J={(4,12),(4,13)}, private to a.

R and U are unchanged. Every owner, terminal type and physical link remains
unchanged. Hence the new sole payment is a->J, of value1 and cost0. In the
exact transfer notation,

    delta=1, p=p_minus=1, p0=0, r=p_minus-p0=1,
    V_after_F=1+p0=1, C_after_F=0.

Thus the no-loss conclusion fails even when T is a true fixed-P maximum
and every endpoint is frozen. These hypotheses alone cannot supply the
missing reserve or net payment gain.

E instead merges the lower H band by changing the P-free tile(10,16) to H.
It replaces the unsupported U by

    K={(10,17),(11,17)}, private to a,

while preserving Q and R. This K is in column17, different from the
column16 unit in the earlier unsaturated board; actual forest identities
must be recomputed after reselecting T. E alone pays a from K and b through
z from Q, with value2 and one link. Applying F as well removes Q and adds J,
so the two supported units J,K both belong to a, and b has no reachable sink.

| E | F | full positive original pool | a support | z support | V | links |
|---|---|---|---|---|---:|---:|
| absent | absent | R,U,Q | empty | Q | 1 | 1 |
| absent | present | R,U,J | J | empty | 1 | 0 |
| present | absent | R,K,Q | K | Q | 2 | 1 |
| present | present | R,K,J | J,K | empty | 1 | 0 |

The table proves both lower and upper bounds: the displayed payments are
feasible, and every source-reachable sink is listed. Units are not spent
more than once, and a source cannot be paid twice. All four states have
L=S=3 and the same completely frozen T/M and source identities.

After E, a is essential in every maximum. F then achieves the allowed
one-payment decrease with e=r=1. This sharpens the necessity of the earlier
unpaid-target premise; it does not contradict the correctly conditioned
transfer formula. Physical operations commute, while payment gains do not
add. The failure concerns the automatic specified-elbow rule, not the existence
of a successful joint direction choice.

## 6. Verification, formal scope and remaining direction

```text
python3 develop/check_fixed_P_maximum_frozen_elbow.py \
  --output output/fixed-P-maximum-frozen-elbow-validation.json
python3 develop/check_fixed_P_maximum_frozen_elbow_formal.py \
  --lean /path/to/lean-4.33.0 \
  --output output/fixed-P-maximum-frozen-elbow-formal-validation.json
```

The standard-library validator checks the exact disjoint186 cover, explicit
feasibility, all70 strict ranks, exact owner/source/link invariance, the entire
three-unit pool and every owner support in all four states. It independently
optimizes all four states and target-deleted/withdrawn controls (8 optima),
invokes the general physical elbow adapter twice with8 independent optima,
and checks all four states under all8 dihedral symmetries with32 independent
optima. There are840 strict freezing event checks. Uniform H and uniform V
also pay all their sources; neither the fixed-adapter example nor the
counting slack obstructs optimizing N.

The concrete Lean module
[FixedPMaximumFrozenElbow.lean](../formal/SubQuorum/FixedPMaximumFrozenElbow.lean)
contains the actual selected indices, actual mate table, strict ranks and
physical witness indices. Its scope is the inventory, physical selected
feasibility, actual matching, concrete strict certificate and complete
freezing by the general soundness theorem. The186 geometric upper bound,
canonical owner/forest/link adapter and exact compensation table are outside
this formal scope; they have the proofs and independent executable checks
above. The associated validation record gives the exact kernel and axiom
audit outcome. The inventory audit is axiom-free; the five remaining declarations
use only Lean standard logical axioms propext and Quot.sound, with no new
axioms, sorry or native evaluation. No end-to-end formal optimal-compensation
claim is made.

An optimizer discovered the finite attainer. The permanent proofs use an
explicit board, a rank certificate, a disjoint geometric upper bound and
a complete source-reachable resource table. Finite search is not substituted
for an upper-bound or general implication proof.

No arbitrary-q rectangular exact-maximum claim follows from concatenation:
saturated border choices can conflict. The earlier arbitrary-copy statements
remain valid in their stated unsaturated/retained-extension settings.

The next substantive question is how to choose **jointly** among legal
direction changes so that genuinely different source demands receive distinct
usable resources, or whether a larger optimized-N obstruction can be built.
One-bit E is already a successful choice here, so further automatic elbow
variants must track old source demand and reachable original resource identity.
No maximum over changing P or the actual matching is asserted. A universal
improvement over5/6 remains open. No email operations, submitted
manuscript changes, public-main/PR3 changes, shared CI changes or C4 changes
are part of this continuation.
