# Short-beta deletion can destroy freezing, even for unsupported alphas

25 October 2026. Haobo Ma and Wenlin Zhang. Research branch only.

The [forced-guard theorem](FORCED_POCKET_GUARDS_AND_CYCLE_ELIMINATION.md)
recognizes an exclusive short-beta resource in a completely frozen board.
Its full-network elimination is an algebraic projection and lift. It does
not assert that a residual network is itself the strand system of a frozen
subconfiguration. We now refute that geometric inference with an actual
16-by-14 board, including **empty whole support for both adjacent alphas**.

Deleting one recognized actual beta edge leaves a feasible matching but
destroys complete freezing. A four-point closed dependency core excludes
every possible strict freezing order. The concrete original geometry and
complete freezing, deletion feasibility, and this all-orders impossibility
are kernel checked in Lean. Arbitrarily many separated copies give the
same obstruction independently and simultaneously.

Deletion also creates two different original interval units and reduces
minimum compensation links from two to zero. Thus the obstruction refutes
reverse frozen completion and an induction based on that rule; it refutes
neither algebraic compensation nor the numerical grid target. The universal
compensation theorem and improvement of 5/6 remain open.

## 1. Explicit board and actual matching

Use zero-based coordinates, aligned bands (0,1),(2,3),...,(14,15), and the
following rows. A dot is blank, T selected, and P an actual matching endpoint.

```text
..............
.T.....T.T.T..
.PPPPPPPPPPPT.
.PPPPPPPPPP...
.PP.PPPPPPPT..
.PPPPPPPPP....
.PPPPPPPPPPT..
.PPPPPPPPPP.T.
.PPPPPPPPPPT..
.PP.T..T..T.T.
.PP...........
.PP......T....
.PPPPPPPPPT...
.T.PPPPPP.....
...T....T.....
..............
```

The permanent coordinate fixture
`develop/fixtures/frozen_short_beta_deletion.json` specifies **every**
matching edge, selection, and all 32 strict freezing layers. The row picture
does not determine M and must not be used without that matching. There are
18 selections, 45 actual matching edges and 90 endpoints. Every endpoint
freezes. Feasibility and the full strict certificate are checked by grid
coordinates independently of the discovery solver and also by Lean.

The original alpha tips are

    A: (8,4), (12,1);     B: (8,7), (8,10).

There are five original betas, no mixed strands, and both alphas have empty
whole-body interval support. The complete recognized short-beta resource
graph contains exactly

    E={(8,5),(8,6)} between A and B,
    F={(8,8),(8,9)} as a loop at B.

Here is a direct check of the empty-support assertion. Their complete
P-column supports, written as band:columns, are

    A: 1:{1,2,3,4}, 2:{1,4}, 3:{1,4}, 4:{1,4}, 5:{1}, 6:{1};
    B: 2:{7,8}, 3:{7,8,9,10}, 4:{7,10}.

The only endpoint-free gaps adjacent to these supports are A's column0
gaps and B's right-hand gaps in bands3,4. Each A gap contains just the marked
boundary BB unit at column0. Each B gap has types BT,BT,BB at columns11,12,13;
its only BB unit is the marked boundary unit at13. Every other neighboring
column of the displayed supports is P-containing. Thus neither alpha sees
an unmarked unit, including from any internal PP column.

The PP guards of E are columns5,6 in rows6,7. The PP guards of F are
columns8,9 in the same band. Thus these are exactly the completely frozen
motifs of the preceding theorem, including its original-alpha hypotheses.
The graph has two vertices and two edges, so its entire component is
algebraically eliminable. One original compensation pays A with E and B
with F, at exactly two links. Neither source can pay without a link because
its direct whole support is empty. Both ordinary and full-fork optima are
therefore (V,c)=(2,2), without reliance on finite optimization.

## 2. A four-point obstruction after deleting E

Keep every selection and every actual edge except E. All remaining strands
and their original alpha types persist: E had no PP continuation. Deleting
its two endpoints preserves feasibility. Set

    y=(5,3), x=(6,4), z=(7,3), w=(8,4), C={y,x,z,w}.

Their actual mates after deletion are respectively

    (6,3), (5,4), (8,3), (7,4).

For a nonmate neighbor v of p, an endpoint v can be retained at p only if
its actual mate freezes earlier than p. A selected v is immediately usable.
The complete possible nonmate witnesses of the four points are:

| Endpoint | Witnesses whose mates belong to C | Possible witness supplied from outside C |
| --- | --- | --- |
| y=(5,3) | (5,4), with mate x | (5,2) |
| x=(6,4) | (6,3), with mate y; (7,4), with mate w | (6,5) |
| z=(7,3) | (6,3), with mate y; (7,4), with mate w | (7,2) |
| w=(8,4) | (8,3), with mate z | selected (9,4) |

Every unlisted neighbor is either the actual mate or blank. In particular
(8,5) is blank after E is deleted. Each point has at most **one** possible
nonmate witness whose availability does not require another point of C.

**Proposition 1 (closed-core obstruction).** No point of C can be the first
point of C to freeze. Consequently the deleted board is not completely
frozen, regardless of the exterior ranks or the choice of certificate.

**Proof.** Before any point of C freezes, an endpoint neighbor with mate in
C is not retained. The table leaves at most one other nonmate witness at
each point. Two distinct retained nonmates are required. Hence there is no
first freezing event in C. QED.

For an equivalent strict-rank proof, every proposed full certificate would
have to satisfy

    rank(x)<rank(y),                  rank(z)<rank(w),
    rank(y)<rank(x) or rank(w)<rank(x),
    rank(y)<rank(z) or rank(w)<rank(z).

The first and third force rank(w)<rank(x)<rank(y); with rank(z)<rank(w),
neither alternative in the last line can hold. This proof permits every
outside witness in the table to be available immediately. Thus no rearranged
or deeper exterior certificate can remove the obstruction.

The implementation also checks that no nonempty proper subset of these
four points is itself a closed core. This is a statement about this displayed
core, not a claim that the board is a smallest possible counterexample.

The final peeling computation freezes 48 of the remaining 88 endpoints;
40 remain unfrozen. That exact count has an explicit finite certificate
and a closed remaining set. The four-point proof suffices for impossibility
and is the core checked in Lean.

**A complete resource-tree variant.** Delete F first instead. All 88
remaining endpoints still freeze; the verifier stores a new explicit strict
certificate. The complete recognized graph is now the single A--E--B tree.
A still has empty support; B has the two units created by deleting F.
Now delete E: the same four-point core is closed, and 39 of the remaining
86 endpoints cannot freeze. Thus the failure is present even after the
recognized graph has become a tree. This variant does not keep B unsupported;
the primary example above keeps both alphas unsupported. The two statements
have separate hypotheses and are not combined into an unsupported-tree claim.

## 3. Resource changes and why compensation still succeeds

The original inventory is alpha=2, beta=5 and I=30 distinct available
unmarked intervals. Its exact signed ledger is

    I+beta-alpha = 30+5-2 = 33
                = 16*14/2 - 18 - 45 - 16.

The last16 is the two boundary marks per band. Deleting E changes only its
two BP columns inside the gap bounded by A:(8,4) and B:(8,7). It creates
two BB singleton units, with coordinate identities

    J5=(band4,first5,last5),   J6=(band4,first6,last6).

There are no TT columns between them; they are different interval units.
Both are strictly internal and unmarked. Each is eligible for both A and B
by the two sides of that gap. Every other interval identity is unchanged.
Assign A->J5 and B->J6. This pays both at zero links. Accordingly

    after deletion: I=32, beta=4, alpha=2, (V,c)=(2,0),
    signed ledger = 32+4-2 = 34.

Thus the physical deletion changes the available interval set. It cannot be
identified with the previous algebraic reduction, which keeps all original
interval identities while removing selected source and beta identities.
Neither process duplicates a resource; they are different operations with
different hypotheses and resulting systems.

For the tree variant, deleting F first gives I=32, beta=4 and (V,c)=(2,1):
pay A using E and B using a new unit. A's empty support gives the one-link
lower bound. Deleting E next gives I=34, beta=3 and (V,c)=(2,0). Its ledger
increases from34 to35, again without a failure of compensation.

## 4. Arbitrarily many simultaneous copies

For q>=1 translate the entire original board by (16i,0), i=0,...,q-1, into
a 16q-by-14 board. Old occupied rows lie between1 and14 in each copy; copies
have no intercopy occupied adjacency. The translations preserve the two-row
band alignment. Replay the original certificate simultaneously in each copy.
All 90q endpoints freeze, with no assumption on a finite upper bound for q.

Delete E_i for an arbitrary subset S of the copies. The translated closed
cores C_i have no intercopy witnesses; each independently has no first
freezing event. The finite base fixed-point certificate therefore gives
exactly 40|S| unfrozen remaining endpoints. All original alpha types persist,
and resources of different copies have different band identities. Hence

    alpha=2q, beta=5q-|S|, I=30q+2|S|,
    signed ledger=33q+|S|,
    ordinary/full V=2q, minimum links=2(q-|S|).

For the upper bound, use the two distinct new intervals in a deleted copy
and E_i,F_i in an undeleted copy. For the lower bound, each of the two
alphas in an undeleted copy has empty support and needs an actual link;
there are no links or supports between copies. This proves the formulas
for all q and S, not by extrapolation from checked stacks.

Blank right padding preserves feasibility, old freezing before deletion,
and the local closed-core obstruction after deletion. It can make former
boundary intervals available to an alpha. We therefore do not extend the
empty-support or cost-2 assumptions to padded boards. The verifier handles
these separately and checks their actual costs.

## 5. Verification and formal scope

`develop/check_short_beta_deletion.py` needs no SAT solver. It reconstructs
original strands and complete short-beta graphs, checks the explicit strict
certificate independently, verifies actual PP guards and empty alpha
support, compares the ordinary/full before-and-after optima, checks actual
link packs, and verifies every translated closed core. It includes all
deletion subsets through four copies, further controls through twelve
copies, 16 even padding controls and eight carried-band isometries.

The final run passes 130 deletion pairs, with 260 ordinary/full before-after
comparisons, 520 actual-link pack checks and 60 independent primitive-pack
comparisons. It checks 417 translated four-point cores and independently
replays 55,386 partial post-deletion rank events; the remaining endpoints
are checked as a closed set. The original-board motif scans, including the
separate resource-tree variant, total 131 checks and 1,621 short betas. Six
additional optimizations check that variant, and all 14 nonempty proper core
subsets are checked. The supported degree-two control is separate.

The separate supported control fixture is simpler: deleting its beta leaves
the exposed alpha tip (8,4) with only one occupied nonmate neighbor, selected
(9,4). Its original alpha supports need not be empty; 25 remaining endpoints
lose freezing. The primary example above strengthens this control by keeping
both original alpha supports empty and proving a four-point obstruction.

`formal/SubQuorum/ShortBetaDeletion.lean` kernel checks eight declarations:
finite minimum-rank selection, the general closed-core exclusion argument,
the original concrete feasibility and complete freezing, deletion feasibility,
the actual core's closure and endpoint membership, and impossibility of any
strict freezing certificate after deletion. The original witness/rank tables
are explicit. Kernel reduction uses neither native evaluation nor sorry.
Only propext and Quot.sound occur in the axiom audits.

The original alpha/beta/PP type adapter, interval inventory, compensation
construction, exact 40-endpoint remaining set and all-q stacking arguments
are written proofs with independent computational checks; those portions
are not claimed fully formalized. Discovery used optional Z3; no UNSAT or
timeout result is promoted to a general statement. No new independent
external review is claimed.

## 6. Consequence for the remaining research

The earlier cyclic-block elimination and tree compression retain their
full algebraic validity. Their residual systems need not be frozen physical
subboards obtained by deleting the internal beta edges. Any further geometric
estimate must refer to the **original** completely frozen board and carry
its actual matching, old interval identities, and dependency certificate
through the accounting. A recursive proof that simply deletes short betas
and reapplies a frozen-board lemma is invalid without an additional preservation
hypothesis or a separate geometric repair theorem.

The next question remains the joint exterior capacity of the residual trees,
but its geometry must be established on the original board. This counterexample
does not show that the required exterior inequality fails. The submitted
11 October manuscript, public main and existing PR3 remain unchanged.
