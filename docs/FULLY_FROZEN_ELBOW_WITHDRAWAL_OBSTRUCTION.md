# Complete freezing does not force zero elbow withdrawal loss

26 October 2026. Wenlin Zhang and Haobo Ma. Independent research continuation.

We resolve the full-freezing question left open by the
[physical rank-one example](PHYSICAL_ELBOW_WITHDRAWAL_OBSTRUCTION.md).
There is a **completely frozen** feasible board, with canonical mixed H/V
bands and the **entire original resource pool**, satisfying every hypothesis
of the two-tile elbow adapter, such that the old target is unpaid and the
withdrawal loss is r=1. All four alpha terminals have occupied degree three.

The repair transfers a payment from b to a without increasing the number
of paid sources. Complete freezing therefore does not supply the missing
zero-loss premise in the [exact local/joint theorem](LOCAL_ELBOW_RESOURCE_TRANSFER.md).
Arbitrarily many independent copies saturate its distinct-witness loss
bound even under full freezing.

This rejects a specific compensation rule. The target numerical inequality
holds with large slack. We do not assert that T is a true fixed-P maximum,
or that the obstruction survives optimization of N. In fact uniform V pays
both one-copy sources with no links, while uniform H also pays both sources.
The 11 October submitted manuscript is preserved.

## 1. Construction from the partially frozen board

Take the 16-by-28 board in the preceding physical example, including its
selected vertex (6,16). Make precisely these modifications:

1. Remove the actual edges (2,14)-(2,15) and (11,14)-(11,15), together
   with their four P endpoints. Those were exactly the unfrozen endpoints.
2. Retain every old selection. Add these 16 selections:

       (2,14),(2,15),
       (3,c) for even c=16,18,...,26,
       (2,c) for odd  c=17,19,...,27,
       (11,14),(10,15).

3. Change the direction of the empty physical tile [10,12) x [16,18)
   from H to V, and canonicalize. This tile has no P endpoint. All other
   old tile directions are retained.

The resulting full occupancy is as follows. Coordinates remain zero based.

```text
 0  ............................
 1  ............................
 2  ....T.T.T.T.T.TT.T.T.T.T.T.T
 3  .....TPPPPPPPT..T.T.T.T.T.T.
 4  ....T..T.PPP...T.T.T.T.T.T..
 5  ....T.T.TPPPT.TPPPPPPPPPT...
 6  .....T.T.PPP....T.PPP.T..T..
 7  ....T.T.TPPP.T.T.TPPPT.T.T..
 8  .....T.T.PPPT.T.T.PPP.T.T...
 9  ....T..PPPPP...T..PPPT.T.T..
10  .....TPPPPPPPT.T.TPPP.T.T...
11  ....T.T.T.T.T.T...PPPPP..T..
12  ..............T.TPPPPPPPT...
13  ...............T.T.T.T.T.T..
14  ............................
15  ............................
```

For an independent compact M specification, take the 17-edge list in the
preceding note, apply both f_L(r,c)=(r+2,15-c) and f_R(r,c)=(r+4,c+14),
and add just (5,15)-(5,16). These are 35 disjoint nearest-neighbor actual
matching edges, with exactly the 70 displayed P sites. There are 83 selections.

The complete old tile-direction specification is V exactly on

    [2,12) x [6,12),   [4,14) x [18,24),
    [12,14) x [12,14), [10,12) x [16,18),

and H on all other aligned tiles. Take maximal canonical bands. The
[permanent fixture](../develop/fixtures/fully_frozen_elbow_rank_one.json)
stores every selection, actual edge, tile bit and strict freezing layer.

## 2. Feasibility and the missing zero-capacity option

Every retained old selection remains feasible after removing the two shield
edges. New selections (2,14),(2,15) are adjacent to one another, and neither
has any other occupied neighbor. In particular (2,13),(2,16),(1,14),(1,15),
(3,14),(3,15) are blank. This is a legal selected dimer. A P-free zero-capacity
BT gap need not have strictly alternating selection rows: such a dimer can
change the row phase with no BB unit.

For columns16,...,27, the new selections alternate between rows3 and2.
They are pairwise nonadjacent, and none has an old occupied neighbor:
the old row4 selections are at odd columns whereas new row3 selections
are at even columns, and row1 has no occupied point. The first at (3,16)
is diagonal to (2,15). These checks also cover the outer board edge.

The new selection (11,14) sees only the old selected point (12,14), now that
the shield edge has gone. The old point (12,14) had no other occupied neighbor
after that deletion. Similarly the new (10,15) and old (9,15) form one isolated
vertical selected dimer. All their other neighbors in the displayed board
are blank. These three dimers are different and separated. Thus both old
and new selections have at most one occupied neighbor, proving feasibility.

The upper target gap is now columns13,...,27 of band rows2,3. Every column
is BT, including the dimer's consecutive upper selections at columns14,15,
so its capacity is zero. Changing tile (10,16) to V makes the lower target
H band end at column16. Its remaining gap columns13,14,15 has respectively
upper,lower,upper selections and is also entirely BT. The neighboring
selections outside that band form the two vertical dimers just checked;
they supply no interval credit.

This removes both unfrozen shield owners without introducing a new target
resource. The two old shield boundaries were a feature of the earlier
construction, rather than a consequence of the elbow hypotheses.

## 3. Complete strict freezing, with the old certificate unchanged

Let K be the 70 endpoints that froze in the preceding partially frozen
board. K is closed under the actual mate map: the omitted four endpoints
were exactly two complete actual edges. The remaining actual matching is
unchanged on K, and all old selections are retained.

In the old 11-wave certificate a retained-neighbor witness for p is either
selected, or is an endpoint x whose actual mate was frozen at an earlier
wave. In the latter case M(x) belongs to K; mate closure implies x belongs
to K as well. Consequently **no old witness uses a deleted shield endpoint**.
Every old selected witness is still selected. Replaying the exact same
70 vertex events, at exactly the same ranks, therefore freezes every
remaining endpoint. Added selections cannot invalidate such a rank witness.

This is a certificate-replay proof, not an inference from endpoint degree.
The fixture includes all 11 layers. The independent strict-rank checker
checks each pair of distinct physical neighbor witnesses against the actual
mate map and a strictly smaller rank. It verifies all 70 endpoints; a second
closure computation obtains the same complete set. Both the old and repaired
directions have this identical freezing certificate because T and M are fixed.

The general replay and rank-soundness statements have a standalone
[Lean proof](../formal/SubQuorum/FrozenCertificateReplay.lean): retaining
selections and removing endpoints outside a mate-closed partial frozen set
preserves every exact witness, and strong induction proves that any such
strict-rank certificate is contained in the freezing closure. Concrete board
coordinates and this particular 70-entry certificate remain executable and
written evidence; they are not encoded end to end in Lean.

## 4. Full source-reachable model and exact loss

Restoring every actual M edge, including direction crossings, gives exactly
two alphas, two betas and five mixed owners. The original alpha terminals
are unchanged:

    a: (3,12),(10,12),     b: (5,17),(12,17).

All four have occupied degree three. The complete forward-reachable system
from either alpha has just one further owner, the mixed z with TP (5,15),
BP (5,16), and actual edge between those endpoints. Its only external link
is the incoming b(5,17)->z(5,16). Other mixed links and every whole beta
remain in the full model, but none can be reached from a or b. The complete
interval supports of the reachable owners are

| Owner | Old support | Old non-self exits |
| --- | --- | --- |
| a | empty | none |
| b | empty | z |
| z | just Q={(4,13),(5,13)}, private to z | none |

To check the table, the old target's upper and lower gaps are the zero-capacity
BT gaps proved in Section2. Its vertical-body gaps are unchanged. For b,
the old uniform vertical body slab, both terminal seals and the isolated
tile at (12,12) still give no supported unit; the new tile at (10,16)
contains no P and is separated vertically from any other V tile of its
column pair, so its units acquire no P boundary owner. The paying gap at
rows4,5, columns12,13,14 is still BT,BB,BT, with one open P boundary z at
column15. It gives exactly the singleton Q. All M/PP owner bodies and free
terminal types are those of the preceding example after deleting the two
shield betas; new selections have no N partner in P.

No reachable beta exists, so no beta stem or fork can supply an additional
payment. The table gives the unique nonempty old source payment, b->z->Q.
It has one physical link. Thus the old optimum is (payment,links)=(1,1),
and a is unpaid in every old maximum. Removing a leaves that optimum intact;
also withdrawing Q leaves zero payment.

Now flip the two H tiles (2,12),(4,12) to V, with every other bit fixed.
This is the same reflected elbow as before: its only P site is a's terminal
(3,12), seals are (2,12),(3,13), outside P guards are (4,11),(5,11),
left-hand tiles are V, and the above/below tiles at (0,12),(6,12) are H.
The modified empty tile at (10,16) is outside this adapter and its guards.
All physical hypotheses hold.

The new patch word is BT,TP,BB,BT. Q disappears and one new singleton

    J={(4,12),(4,13)}

appears private to a. No other positive original forest changes its cells.
No non-target support changes outside Q; all M/PP owners, terminal types
and physical links remain identical. Thus after the repair the support
column of the table becomes {J},empty,empty. The sole payment is a->J,
with zero links. Explicitly,

    p=p_minus=1, p0=0, delta=1, r=p_minus-p0=1,
    V_new=1+p0=1, C_new=0.                              (1)

The new private credit cannot also keep b paid: b's only original sink
was withdrawn. Neither complete freezing nor its source degrees changes
this accounting fact.

## 5. Arbitrary simultaneous fully frozen sharpness

**Theorem.** For any q>=1, vertically concatenate q copies by translating
copy i by (16i,0), with its old directions. Apply the elbow exactly in a
subset F of copies. All 70q endpoints are strictly frozen, all 4q alpha
terminals have occupied degree three, and the complete full-fork model has

    alpha=2q, beta=2q, mixed=5q, L=106q,
    |T|=83q, |M|=35q, S=106q,
    V_old=q, C_old=q,
    V_old_without_all_targets=q,
    V_residual=q-|F|, C_residual=q-|F|,
    r=|F|, V_new=q, C_new=q-|F|.                        (2)

In particular repairing all q old unpaid targets can leave the total deficit
equal to q. The distinct-witness loss bound is sharp on completely frozen
physical boards with the full original pool.

**Proof.** Rows0,1,14,15 of every copy are entirely blank. The edge-neighborhoods
and selected-neighborhoods of different copies are disjoint. Replay their
same strict rank schedule in parallel waves. Every certificate witness is
internal to its copy, so all 70q endpoints freeze in 11 waves.

Both top and bottom guard tile rows are H. Canonical V bands cannot cross
the horizontal join between copies; H bands always run in fixed row pairs.
Hence the actual matching, PP graph, original forests, owner supports and
links split into disjoint one-copy systems. Their source-reachable tables
are precisely those in Section4, with separate Q_i and J_i. Counts and
exact one-copy values add. Deleting all a_i removes no old payment; jointly
withdrawing Q_i for i in F removes exactly |F| b_i payments. Every repaired
copy instead pays a_i at cost zero. Unrepaired copies pay b_i with one link.
This proves every assertion in (2) for arbitrary q,F, not just checked sizes. ∎

## 6. One empty-tile repair and a genuine destructive interaction

There is a simple successful alternative on this same completely frozen
board. Call E the action of changing only tile (10,16) back from V to H.
Its four sites contain no P, so it preserves all owner bodies, source and
terminal identities, and all physical links. Before E, its V band has the
unsupported singleton U={(11,16),(11,17)}. After E the merged lower H band
has instead K={(10,16),(11,16)}, private to a. No old supported unit is
withdrawn: U had no open owner at either boundary. The original z unit Q
survives. Thus E alone pays a from K and b through z from Q, with value2
and one link. Zero changed bits cannot pay both sources in the baseline,
so this one-bit full repair is also optimal in bit count for this board.

Call F the original two-tile elbow. The exact four-state profile is

| Empty-tile action E | Elbow action F | a's units | b's usable unit | Value | Links |
| --- | --- | --- | --- | ---: | ---: |
| absent | absent | none | Q via z | 1 | 1 |
| absent | present | J | none | 1 | 0 |
| present | absent | K | Q via z | 2 | 1 |
| present | present | J and K | none | 1 | 0 |

In the last row two different private units both belong to a; they cannot
pay b or pay a twice. The local numerical inventory L remains106 in all
four states. Consequently applying the elbow **after** the successful
empty-tile repair lowers payment from2 to1, with every endpoint still
frozen. The old target a is then essential in every old maximum, so this
does not contradict the previous theorem's unpaid-target nondecrease
condition. It shows that condition is necessary even on fully frozen grids,
and attains its allowed one-payment decrease with e=r=1.

The physical direction operations commute, but their payment gains are
not additive. Each changes its own original forest identities; the union
of old and new local resource pools is never available simultaneously.
Jointly rechecking target demand, source reachability and distinct usable
units is necessary even when the two physical patches are disjoint.

For arbitrary copy sets E,F, where E applies the one empty-tile action and
F the elbow, the same source-reachable proof gives exactly

    V(E,F)=q+|E minus F|,   C(E,F)=q-|F|,
    D(E,F)=q-|E minus F|.                                (3)

Indeed copy i pays a_i iff i lies in E union F, and pays b_i iff i is not
in F. These use distinct units and owners. Summing gives (3). This also
proves the upper bound: the only source-reachable units are precisely the
displayed one-copy units. Under this action class full payment2q requires
and permits E to be all copies and F empty. This restriction on action
choice is not a claim about all possible direction assignments.

## 7. Consequences and limits

The implication

    full freezing + canonical local elbow + unpaid old target => r=0

is false. So is the proposed inference that such q repairs automatically
raise payment by q, even when all original alpha terminals have degree three.
The exact formula V_new=p+q-r remains correct and is sharp under complete
freezing. Source identity and link-cost differences remain material.

This does not contradict the surviving-private-suffix criterion: z's old
affected suffix has exactly Q and no surviving private reserve. It is an
active, exhausted suffix witness even on a fully frozen board. A successful
stronger compensation theorem must use an additional geometric operation,
a larger proved resource interface, a different direction choice, or an
explicit reserve hypothesis; freezing alone is insufficient.

For one copy the numerical accounting is

    area/2=224, |T|+|M|=118, S=106=L+beta-alpha.

Thus this is not a counterexample to the grid counting inequality or the
5/6 bound. It is not claimed extremal in T for fixed P. Uniform V gives
alpha2,beta2,L106 and payment2 at cost0; uniform H gives alpha2,beta0,L108
and payment2 at cost2. These recompute owner identities for the new N.
The failed fixed-adapter rule is therefore not an optimized-N obstruction.

## 8. Verification and external review status

```text
python3 develop/check_fully_frozen_elbow_withdrawal.py \
  --output output/fully-frozen-elbow-withdrawal-validation.json
python3 develop/check_frozen_certificate_replay_formal.py \
  --lean /path/to/lean-4.33.0 \
  --output output/frozen-certificate-replay-formal-validation.json
```

Physical checks passed 42 stack/action profiles, all small action subsets,
large stacks through q32, 136 fully frozen rank-one transfers, 22,540 strict
freezing events using the unchanged independently replayed ranks, 56
independent primitive optima plus four through the normalized general
adapter, and eight dihedral controls with independent freezing/optimization.
Another 92 joint empty-tile/elbow profiles passed, including all84 small
action pairs with independent primitive optima and eight larger profiles;
two independent uniform-direction controls also passed.
The complete fixture, including ranks, is serialized and read back.
The general disjoint-union proof establishes all q,F.

Local Lean4.33.0 passed three general certificate-replay/soundness declaration
audits; all three are axiom-free, with no warnings, sorry or native evaluation. The run
measured local memory and actual lean/lake comm basenames before execution.
This formal scope does not include the physical board-to-network adapter.

An oracle-broker question about the then-open full-freezing conjecture ended
with `model_unavailable@selecting_model`, task
`0355d1ef-775f-4162-b2af-3d0706ac417c`. No mathematical answer or independent
oracle approval was obtained. The conjecture was subsequently resolved by
the explicit construction and checks above. The failure is recorded in the
small [attempt receipt](../output/frozen-elbow-oracle-attempt.json); it is
not used as evidence for any theorem. No broker/worker infrastructure was
changed. This continuation performs no email operations and leaves the
submitted manuscript, public main and PR3 intact.
