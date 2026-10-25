# A physical rank-one elbow withdrawal and its exact joint loss

26 October 2026. Wenlin Zhang and Haobo Ma. Independent research continuation.

The loss term in the [two-tile elbow theorem](LOCAL_ELBOW_RESOURCE_TRANSFER.md)
is necessary on its stated feasible-grid class. We construct a canonical
mixed H/V board with the **complete original resource pool** on which the
old target is unpaid, one different source is paid through a mixed owner,
and the elbow withdraws that source's only usable unit. The repair pays the
target instead. The exact values and minimum link counts are

| Model | Payment | Minimum links |
| --- | ---: | ---: |
| Old full model | 1 | 1 |
| Old model with the target removed | 1 | 1 |
| Also withdraw the lost original unit | 0 | 0 |
| New full model after the two flips | 1 | 0 |

Thus delta=1 and r=1. The newly private reserve relocates one payment; it
does not add a payment. This is a physical realization, unlike the previous
abstract nonadditive-withdrawal control. It does not assert that singleton
losses are nonadditive on this particular board.

Both original alpha bodies and the paying mixed owner are frozen, and all
four alpha terminals have occupied degree three. Four auxiliary beta
endpoints remain unfrozen. We therefore refute zero loss from the local
elbow hypotheses, or even from those hypotheses plus frozen degree-three
alpha bodies. We **do not refute zero loss under full freezing**. The
numerical target inequality also holds by a wide margin on this board.

## 1. Complete board specification

Rows are 0,...,15 and columns 0,...,27. T denotes a selected vertex, P an
actual matching endpoint, and a dot a blank vertex. The following gives
every site; rows 0,1,14,15 are included deliberately as separation guards.

```text
 0  ............................
 1  ............................
 2  ....T.T.T.T.T.PP............
 3  .....TPPPPPPPT..............
 4  ....T..T.PPP...T.T.T.T.T.T..
 5  ....T.T.TPPPT.TPPPPPPPPPT...
 6  .....T.T.PPP....T.PPP.T..T..
 7  ....T.T.TPPP.T.T.TPPPT.T.T..
 8  .....T.T.PPPT.T.T.PPP.T.T...
 9  ....T..PPPPP...T..PPPT.T.T..
10  .....TPPPPPPPT...TPPP.T.T...
11  ....T.T.T.T.T.PP..PPPPP..T..
12  ..............T.TPPPPPPPT...
13  ...............T.T.T.T.T.T..
14  ............................
15  ............................
```

Here is a compact independent specification of M. Start with these 17 edges:

```text
(1,5)-(2,5)  (3,5)-(4,5)  (5,5)-(6,5)  (7,5)-(8,5)
(2,6)-(3,6)  (4,6)-(5,6)  (6,6)-(7,6)
(1,6)-(1,7)  (1,8)-(1,9)  (8,6)-(8,7)  (8,8)-(8,9)
(7,7)-(7,8)  (1,3)-(1,4)  (2,4)-(3,4)  (8,3)-(8,4)
(7,4)-(6,4)  (4,4)-(5,4)
```

Apply each map f_L(r,c)=(r+2,15-c) and f_R(r,c)=(r+4,c+14) to all
17 edges. Add the three edges

```text
(5,15)-(5,16),   (2,14)-(2,15),   (11,14)-(11,15).
```

These are 37 disjoint nearest-neighbor edges and their 74 endpoints are
exactly the displayed P sites. There are 67 selections. At each displayed
T, counting its four neighbors gives at most one occupied neighbor, so T
is feasible. No restriction of the resource pool is part of the construction.

Tile lower-left coordinates are even. Choose V precisely on

* tiles in [2,12) x [6,12);
* tiles in [4,14) x [18,24);
* the one tile [12,14) x [12,14).

Choose H on every other tile and take the canonical maximal bands. This
specifies N without artificial cuts. The serialized
[fixture](../develop/fixtures/physical_elbow_rank_one.json) contains all T,
M and tile bits as well as the expected answers.

## 2. The complete source-reachable system

Restore every actual M edge, including all direction crossings, before
forming M/PP components. The only alphas are a and b, with terminals

```text
a: (3,12), (10,12)
b: (5,17), (12,17).
```

Their selected N partners are, respectively,
(2,12),(11,12),(4,17),(13,17). All four terminals have occupied degree
three. The additional actual edge (5,15)-(5,16) is the mixed owner z:
(5,15) is TP, with selected partner (4,15); (5,16) is BP, with blank
partner (4,16). There are four beta and five mixed owners in total.

Inspect the canonical bands in the displayed diagram. Both alphas have
empty whole-owner interval support. Among links reachable from either
alpha, the only link between different owners is

    (5,17) -> (5,16),                 b -> z.             (1)

Owner z has no link to a different owner. Its sole supported original unit
is the BB singleton

    Q = {(4,13),(5,13)},                                (2)

private to z. There are links and resources in other components; they
remain in the full model. None of those owners is reachable from a or b.
In particular **no whole-beta sink is source-reachable**. This distinction
matters: the board has 118 positive original units and four whole betas,
but only the unit (2) can pay an old source.

These support claims can be checked directly without optimization: for
each vertical slab scan its two-column no-P gaps, and for each remaining
horizontal row pair scan its maximal same-direction run. Record BB/TT
forest cells and the P owners at each no-P gap boundary. The two shield
edges at rows 2 and 11 terminate the target's horizontal gaps before any
positive unit; the isolated V tile at (12,12) terminates b's lower H band.
The paying mixed gap has columns 12,13,14, whose words are BT,BB,BT.
Its left end is a band boundary at column 12 and its only P boundary is z
at column 15. All other no-P gaps meeting a or b have capacity zero.

Consequently the only nonempty primitive payment in the old source-reachable
system is the one-link stem b->z spending Q. A fork is impossible because
there is no reachable beta. It follows directly that the old optimum is
payment 1 with one link, a is unpaid in every old maximum, and removing a
does not change either optimum. Removing Q as well leaves no payable source.
This is a source-reachability proof on a specified graph, rather than an
inference from a finite search failing to find a second payment.

## 3. Exact two-tile transfer

Use the horizontal reflection of the previous elbow: the patch is
[2,6) x [12,14), the target is (3,12), its selected seals are (2,12),(3,13),
and the exterior P guards are (4,11),(5,11). The tiles immediately left
are V. The same-column-pair tiles above and below, at (0,12),(6,12),
are H and remain unflipped. The patch's only P site is the target.
Thus every hypothesis of the local adapter holds after horizontal reflection.

Flip exactly the tiles (2,12),(4,12) to V. The new V word, from top to
bottom, is BT,TP,BB,BT. Exactly Q disappears and exactly

    J = {(4,12),(4,13)}                                 (3)

appears, private to a. The original units Q and J overlap at a physical
blank cell, but are different complete original forests in the two models.
They replace each other. They are never simultaneously counted as resources.
All other positive original forest cell sets survive, the supports of
non-target owners outside Q are unchanged, and all M/PP owners, endpoint
types and physical TP-to-BP links are identical.

The new reachable system has a->J with zero links; z has no usable unit,
and b->z has no sink. Thus the new optimum is payment 1 with zero links.
Equivalently the old target-deleted model has value 1, its Q-withdrawn
residual has value 0, and the exact local theorem gives

    r=1-0=1,       V_new=1+0=1.                          (4)

The old paid source b cannot stay paid after this repair. Preserving total
payment therefore does not imply preservation of the old paid source set.
Conversely the repair is useful for reducing link cost; failure of strict
payment gain does not mean every objective fails to improve.

## 4. Arbitrarily many simultaneous saturated losses

**Proposition.** For every q>=1 vertically concatenate q copies of the
16-by-28 board, translating copy i by (16i,0), retaining its directions.
For any subset F of copies, apply the one elbow in each copy of F. The
exact full-pool values and minimum links are

    V_old=q,           C_old=q,
    V_old_without_all_targets=q,
    V_residual=q-|F|,   C_residual=q-|F|,
    r=|F|,
    V_new=q,           C_new=q-|F|.                     (5)

**Proof.** Each copy has four blank border rows, 0,1,14,15. At a concatenation
boundary the neighboring tiles are H, so no canonical V run crosses that
boundary. H bands run horizontally within their fixed row pairs and cannot
join different copies. Actual matching edges, PP edges, original forest
units, no-P gap supports and physical links are therefore a disjoint union
of their per-copy systems. The source-reachable system in each unrepaired
copy is exactly (1)-(2), and in each repaired copy exactly a_i->J_i.
No beta becomes reachable. Sum the exact one-copy values and link costs.
Deleting all targets has no effect on any old one-copy optimum; withdrawing
Q_i for i in F removes precisely those |F| old one-link payments. This proves
every assertion in (5). Each unit is withdrawn once, and its witness z_i is
different from all other witnesses. ∎

In particular repairing every unpaid old target need not reduce the total
deficit: old and new alpha counts are 2q, both deficits are q, and the upper
bound r<=number of distinct old witnesses is attained with equality q.
This is sharpness on feasible physical grids, not just an abstract network.

## 5. Freezing and numerical scope

On one copy, the ordinary strict freezing closure freezes exactly 70 of
74 endpoints. The four exceptions are the two shield beta edges' endpoints

    (2,14),(2,15),(11,14),(11,15).                        (6)

Every endpoint of the two original translated modules and both endpoints
of z are frozen. In particular a and b have fully frozen bodies, including
all their three-degree terminals. This remains true after the direction
change, because freezing depends on T and M rather than N. The fixture is
**not fully frozen**; replacing that condition by just frozen alpha bodies
would be an unjustified weakening. For example (2,14) has degree two, and
its two other possible neighbor sites (2,13),(3,14) are forced blank by the
fixed target seals. This construction cannot be made fully frozen merely
by adding occupied sites while preserving those seals and old mates.

The same closure acts independently in vertical stacks, giving exactly
70q frozen endpoints and the four exceptions (6) per copy. The validation
records the exact exceptions rather than using source degrees as a proxy
for full freezing.

Numerically one copy has

    area/2=224, |T|=67, |M|=37, L=118, beta=4, alpha=2,
    S=224-67-37=120=118+4-2.                            (7)

Thus |T|+|M|=104<224 already. This is neither a counterexample to the target
counting inequality nor an obstruction after optimizing N. It rejects the
candidate automatic-zero-loss compensation rule and establishes the sharp
loss range in the local transfer theorem. Full freezing may impose extra
constraints absent here; that question remains open.

## 6. A sufficient surviving-suffix criterion

The counterexample has a **saturated** affected gap: its entire positive
inventory is Q. The following useful specialization of private-reserve
replacement separates that case from patches with an actual spare unit.

**Lemma.** In a joint collection satisfying the previous local/joint elbow
hypotheses, remove the target sources and withdraw the union Q once. For
each different non-target old witness z, suppose either it has a surviving
positive original unit private to z, or call z unprotected. If u is the
number of different unprotected witnesses, then the joint loss satisfies

    0<=r<=u.                                            (8)

In particular r=0 if every affected witness is protected. It suffices that
each affected old no-P suffix with an open non-target boundary has more
positive units than are withdrawn from that suffix by the **whole joint
action set**. This condition is checked jointly, not once per patch.

**Proof.** Choose an old maximum with the targets disabled and put it in
owner-disjoint primitive normal form. A used unit in Q is witnessed by its
unique boundary owner z. There is at most one affected interval assignment
per different z, including a beta-fork interval witnessed by its beta body.
For protected z, replace its lost assignment by one surviving private unit.
No other certificate can already spend that unit: spending it requires z,
which belongs to this certificate alone. Different protected witnesses
have different private units. For an ordinary stem truncate to its z
witness, adding no links; for a beta fork retain both arms and replace
its interval assignment. These changes preserve all its paid sources.
For each unprotected witness whose assignment was lost, discard that
ordinary payment, or retain one fork arm at the same private whole-beta
sink and lose only its other payment. Different such witnesses cost at most
u payments. All untouched certificates and units remain fixed. This gives
the lower residual value and hence (8); withdrawal cannot increase value.

For the suffix criterion, the old affected gap ends at a band boundary and
has at most one open P owner. Every positive unit in it is private to that
owner. If at least one survives the joint withdrawal, it protects z as
above. The suffix's old and new local resource pools are still replacements,
not an additional reserve counted twice. ∎

This lemma applies existing private-reserve exchange to the elbow geometry;
it is not a new general matching theorem. The example shows that the
surviving-inventory condition cannot simply be omitted. A next full-freezing
argument must exclude or compensate active saturated suffix witnesses,
including mixed witnesses reached from another source as in (1).

## 7. Reproduction and verification scope

```text
python3 develop/check_physical_elbow_withdrawal.py \
  --output output/physical-elbow-withdrawal-validation.json
```

The checker reconstructs the board and its full canonical pools, verifies
feasibility, source/owner identities, source-reachable physical links, exact
private forest cells, all unchanged links and owner bodies, the precise
freezing exceptions, full-fork flow optima, independent primitive optima,
every small action subset, large stacks and all eight dihedral images.
It also normalizes the reflected patch and invokes the preceding general
adapter with independent primitive optimization. The fixture is serialized
and read back. The written disjoint-union proof, rather than these finite
tests, establishes arbitrary q and F.

No additional Lean theorem is claimed for this physical construction. The
earlier scoped Lean rank/value arithmetic remains applicable; it does not
formalize this board's physical-to-network adapter or freezing closure.
The submitted manuscript, public main and PR3 are preserved. This research
continuation does not read, draft or send email.
