# Residual fresh-tip domains: complete frozen-extension closure in the fixed rectangle

25 October 2026. Haobo Ma and Wenlin Zhang. Research branch only.

We close the remaining fresh-tip cases for **every completely frozen retained-
occupation extension of the actual 28-by-24 base, within that same rectangle**.
The matching may change arbitrarily, and both selected vertices and matching
endpoints may be added. In fact occupied degree at least three at every final
endpoint suffices; complete freezing is stronger than necessary. The proof uses
untouched mixed owners and checkerboard colors, rather than assigning another
resource to every remaining tip.

For arbitrary feasible extensions in this fixed rectangle, the same displayed
certificate loses at most one alpha payment. A saved 330P/51T **nonfrozen**
configuration has true ordinary deficit one in the restricted certificate pool,
so that bound is sharp for that pool. Its full resource pool has deficit zero.
This result does not establish universal grid compensation, does not apply
unchanged to larger rectangles or horizontal copies, and does not improve the
numerical 5/6 bound.

## 1. Setting and exact statement

Fix the 28-by-24, 49T/308P occupation (T0,P0) in
[`frozen_all_mixed_gate_cycle.json`](../develop/fixtures/frozen_all_mixed_gate_cycle.json).
Coordinates are zero-based. Use horizontal two-row bands, with band partner
bar(r,c)=(r xor 1,c). All old selections are saturated: each has exactly one
old occupied neighbor. Let (T,P,M) be any feasible configuration such that:

1. It is on the **same** rectangle, rows 0 through 27, columns 0 through 23,
   with the same band phase.
2. T contains T0, P contains P0, and T and P are disjoint. M is any grid
   perfect matching of P; no old mate or matching edge must be retained.
3. Each selected vertex has at most one occupied neighbor in T union P.
4. Column 0 is blank, and every band has at least one blank site in column 23.

Use the injective conditional certificate of
[Conditional Fresh-Tip Closure, Theorem 3](CONDITIONAL_FRESH_TIP_CLOSURE.md)
with one copy. Denote its selected BP links by C, and its distinct original
interval resources by J. Let U be its uncovered fresh TP tips. Let k be the
number of alpha paths after C whose two free TP ends both lie in U.
The earlier theorem supplies ordinary compensation of at least a-k of the
original a alphas, using only J and distinct original beta credit.

**Theorem 1 (fixed-rectangle closure).** Under assumptions 1--4:

* k is at most one.
* Any unpaid final alpha must connect D=(17,9) to A=(26,13) or Cb=(26,15),
  and D's actual M-mate must be (18,9).
* That mate has occupied degree at most two. Consequently, if every vertex
  of P has occupied degree at least three, then k=0 and all original alphas
  have ordinary compensation using the existing conditional certificate pool.
* In particular every completely frozen extension satisfying 1--4 is fully
  compensated, for arbitrary actual matching M.

The link and interval budgets of the previous theorem still apply:
B=18+h+p+q links, R=5-h+g-q distinct original units, with at most
min(R, floor((R+u)/2)) interval payments, where u is the number of uncovered
fresh tips. This theorem strengthens the estimate on k, without inventing
additional resources or double-counting any existing payment.

The sufficient degree condition can be weakened: it is enough to exclude
the actual edge D--(18,9). Global minimum degree three is a simple checkable
condition that excludes this edge for every extension of the fixed occupation.

## 2. Two general structural lemmas

**Lemma 2 (untouched mixed owner).** Suppose an uncovered TP v is actually
M-matched to a BP w, and w is not any of the chosen BP targets in C. Then
v--w is an original one-edge mixed owner, is untouched by C, and cannot
supply an end of a final alpha path.

**Proof.** TP and BP vertices both lack an incident PP band edge. Thus their
M-edge is their entire original M+PP component. C cannot meet v: v is
uncovered, hence not a source of a BP assignment, and cannot be a BP target.
C cannot meet w: it is a BP, hence not a source, and is not a chosen target
by hypothesis. The component stays mixed after C. QED.

This also explains why counting all uncovered tips as independent alpha
holes overestimates the deficit. A free TP on an isolated mixed owner is
not an unpaid alpha end.

**Lemma 3 (colored loss refinement).** Suppose a partial terminal certificate
assigns distinct interval identities, with at most one assigned tip per
original interval. Select all its BP links C, and remove uncovered tips
belonging to untouched mixed owners from the hole-end domain. Let the remaining
domain contain b black tips and w white tips. Then

    k <= min(b,w).

**Proof.** On physical endpoints the final multigraph consists of M and a
secondary matching: the retained PP band edges together with C. These secondary
edges are disjoint, since C only meets original terminals and itself is a
matching. All are adjacent grid edges. Every open component starts and ends
with M and alternates between the two matchings, so has an odd number of edges.
Its two ends therefore have opposite checkerboard colors. This remains true
when an M-edge and PP edge are parallel; such a component is a cycle.

Each of the k two-hole alpha paths uses a different black hole and a different
white hole. Distinct final components have disjoint endpoints. Every other
final alpha can still choose a covered end's own distinct interval resource,
as in the earlier certificate lift. Thus no interval is paid twice, and each
unpaid path consumes one endpoint of each color. QED.

The distinct-interval hypothesis is explicit. We do not apply this argument
unchanged to arbitrary two-slot assignments in which multiple free ends can
name one original interval.

## 3. Complete finite audit of the old geometry

Let O=T0 union P0, and F consist of column 0 and all old blank neighbors of
old selected vertices. Every site in F remains blank: its old selected guard
already sees its retained old occupied neighbor. This assertion is valid for
every extension, independent of matching and of complete freezing.

If v is a fresh TP and t=bar(v), then v,t were both old blank. Saturation of
old T excludes an old selected t, and retention excludes old P at t. Feasibility
of new t, which already sees v, implies that t has no old occupied neighbor.
Old saturation also forbids any old selected neighbor of fresh P v. Further,
v cannot be in column 0; if it were in column 23, v and t would violate the
one-blank boundary condition. Consequently v lies in the following necessary
candidate set:

    v,t outside O; N(t) intersect O empty; N(v) intersect T0 empty;
    0 < col(v) < 23.

There are exactly 66 candidates. Removing the 27 protected sites K leaves
these 39 unprotected candidates S:

| Row | Columns |
| --- | --- |
| 0 | 14,15,16,17,18 |
| 1 | 15,16,17 |
| 16 | 8,9 |
| 17 | 9 |
| 26 and 27, each | 1,3,5,7,9,10,12,13,14,15,16,18,20,22 |

Let Q be the union of every **possible** BP target of the conditional certificate:
the 18 retained targets, five flexible candidate sites, promotion target (3,13),
and 27 conditional fresh targets. Membership in Q does not mean that a target
is active; chosen BP targets are a subset of Q. Comparison of the literal
coordinates proves:

    No horizontal neighbor of any v in S belongs to Q.             (1)

A horizontal actual mate w of TP v is necessarily BP. Indeed bar(w) is a
horizontal neighbor of selected bar(v), which already sees v; therefore
bar(w) is blank. Equation (1) and Lemma 2 exclude every such mate case.

The band partner of TP v is selected and so cannot be its actual mate. The
only remaining direction is the transverse vertical neighbor, in the adjacent
band. For all but the seven rows below this neighbor is outside the rectangle
or in F. All seven possible mates are outside Q.

| TP v | Transverse mate w | bar(w) in F | Maximum occupied degree of w |
| --- | --- | --- | --- |
| (1,16) | (2,16) | yes | 2 |
| (1,17) | (2,17) | yes | 2 |
| (16,9) | (15,9) | yes | 1 |
| D=(17,9) | (18,9) | no | 2 |
| A=(26,13) | (25,13) | no | 3 |
| B=(26,14) | (25,14) | no | 4 |
| Cb=(26,15) | (25,15) | no | 3 |

The degree bounds count all in-board neighbors outside F, without assuming
they can be occupied simultaneously. They are valid upper bounds, not
assertions of attainability. The first three mates are BP because their
partners are forced blank. Lemma 2 excludes them as well. We have proved
that an uncovered end on a final alpha must lie in

    H = { D=(17,9), A=(26,13), B=(26,14), Cb=(26,15) }.             (2)

This is a finite check of the fixed old coordinate data, not an enumeration
of possible extensions. The necessary-condition argument and Lemma 2 explain
why the check controls **every** extension. The verifier recomputes S, F, Q
and the seven cases; Lean separately checks the literal completeness and
exclusion statements.

## 4. Proof of Theorem 1

Color by parity of row+column. D and B are even; A and Cb are odd.
B cannot be TP simultaneously with A or Cb. For example, A and B as TP would
force selected vertices (27,13) and (27,14); each selected vertex would see
both its own P tip and the other selected vertex. This violates feasibility.
The same argument applies to B and Cb.

If B is active, no odd tip in H is active. Otherwise D is the only possible
even tip in H. By (2) and Lemma 3, every two-hole final alpha must therefore
contain D, with its other end A or Cb. Since components are disjoint, at most
one such alpha exists, establishing k<=1 and the stated endpoint localization.

For D to survive the untouched-mixed exclusions, its actual mate must be
(18,9). Its horizontal neighbors as a mate, (18,8) and (18,10), are permanently
blank: old selected vertices (18,7) and (18,11), respectively, are saturated.
Thus this mate has only two possible occupied neighbors, D and (19,9), so
has occupied degree at most two. If all final P have occupied degree at least
three, this edge cannot occur. Then no two-hole alpha exists and k=0.

Finally, a completely frozen endpoint must have at least two occupied neighbors
other than its actual mate: these are needed even to start or support its
freezing rank. In particular its total occupied degree is at least three.
Hence complete freezing implies the sufficient condition just proved. The
existing certificate cancellation, distinct beta/interval ledger and ordinary
subset normalization pay all original alphas. No additional unit is created
by the color argument. QED.

## 5. Sharpness and the distinction between pools

[`residual_fresh_one_loss_nonfrozen.json`](../develop/fixtures/residual_fresh_one_loss_nonfrozen.json)
is an explicit 330P/51T extension. It retains the old 49T/308P, adds selected
sites (16,9) and (27,13), and may rematch the old endpoints. Its two fresh TP
tips are D and A. All five old flexible targets are occupied, no protected
fresh site is active, and there is no retained-endpoint promotion. Thus the
conditional certificate has 23 BP links and **no remaining assigned intervals**.
After those cancellations the unique two-hole alpha joins D to A. Its
physical path has 17 edges (nine M, eight PP, no C), so the two ends have
opposite colors even though the path bends through several columns.

The independent ordinary optimizer confirms true deficit one in that restricted
pool, not merely a bad choice of C. The full ordinary pool has deficit zero:
an additional available original interval in the alpha's whole-owner gap support
pays it without a cancellation link. In this witness it is the singleton in
band 8, column 5; the gap-support witness is at band 8, column 9. This is a
counting support incidence, not a claim that physical TP (17,9) is adjacent
to column 5.
The fixture is nonfrozen, as required by its degree-two mate (18,9). It
establishes sharpness of the restricted bound; it is not a counterexample to
the full compensation target or to a frozen-extension theorem.

Optional SAT code in
[`discover_residual_fresh_one_loss.py`](../develop/discover_residual_fresh_one_loss.py)
found the example. The saved fixture and all stated properties are checked
without a solver by the mandatory verifier. Solver discovery is not used in
the proof of Theorem 1.

A second compact fixture,
[`residual_fresh_degree_three_bottom.json`](../develop/fixtures/residual_fresh_degree_three_bottom.json),
has 318P/51T and activates A and Cb simultaneously. Every P has occupied degree
at least three, but this matching is not completely frozen. Its conditional
certificate still pays every alpha, demonstrating that the degree condition
covers more than frozen configurations.

A completely frozen positive control,
[`residual_fresh_frozen_bottom.json`](../develop/fixtures/residual_fresh_frozen_bottom.json),
uses the same 318P occupation, keeps all old matching edges, and has 52T.
Compared with the nonfrozen bottom control, add T=(26,16) and switch the
matching in the square on rows 24,25 and columns 14,15 to vertical edges.
Its two fresh TPs remain the unprotected A and Cb. The old freezing ranks
replay, followed by five explicitly recorded layers on the ten new endpoints:

    (24,12), (26,15)
    (24,14), (26,13)
    (24,13), (25,13), (25,14)
    (24,15), (26,14)
    (25,15)

The fixture records two already-kept neighbors for each endpoint; the
independent rank verifier checks all old and appended layers against the
actual matching. The old conditional bound u=2 alone only gives loss at
most one, while the new frozen-extension theorem guarantees zero. This is
an actual frozen case outside the earlier all-fresh-protected and u<=1
sufficient classes.

## 6. Verification and scope

Run from repository root:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 develop/check_residual_fresh_domains.py \
  --output output/residual-fresh-domains-validation.json
```

The verifier checks feasible retention, the complete residual audit, actual
matching/PP/C multigraphs, odd path lengths, opposite colors, untouched mixed
owners, the exact loss count, the minimum-degree implication and independent
ordinary/full packings on small controls. It exercises single and simultaneous
unprotected activations, forced transverse mates, actual rematches, the sharp
330P witness and the degree-three bottom example. The final receipt has
863 actual models (27 frozen, 836 feasible nonfrozen),
293 actual square rematches, 90 independent ordinary/full primitive
comparisons, 24 simultaneous activation runs, all seven forced transverse
cases, 95 minimum-degree-three models and 10,892 physical odd paths. All
71 loss-one controls have the exceptional localized pair. The frozen bottom
fixture additionally has its full rank certificate independently checked.
These controls corroborate the written all-extension proof.

In `formal/SubQuorum/EndpointExtensionReplacement.lean`, namespace
`ResidualFreshDomains` checks the actual residual-site audit, target avoidance,
seven transverse cases, forced partners, exceptional degree guard, the
bichromatic endpoint reduction, grid color flips, odd walks and disjoint-pair
loss accounting. All 12 new and 51 combined declaration audits pass locally
in Lean 4.33.0;
one new and 13 combined declarations are axiom-free, and the rest use only
standard propext, Classical.choice and Quot.sound. No warning, sorry or native
decision axiom occurs. The full coordinate-to-configuration adapter,
untouched-owner
argument, freezing implication and compensation lift are written proofs with
Python checks; this is **not** an end-to-end Lean grid-compensation theorem.

The fixed rectangle and both boundary conditions are essential to this proof.
For example, column 23 is no longer a boundary inside horizontal copies, and
new candidate tips there require another analysis. Growing the rectangle can
also add neighbors to old top/bottom sites. The earlier arbitrary-rectangle
conditional closure theorem remains available; Theorem 1 adds a stronger
conclusion only under its stated fixed-domain hypotheses.

A separate [seam footprint audit](../develop/audit_residual_copy_seams.py)
records necessary geometry for n=1,2,3,4 copies. In those finite footprints,
there are 39n+28(n-1) unprotected candidates and 4n+18(n-1) candidates after
the untouched-mixed exclusions. In particular, one seam contributes 18 new
potential transverse hole ends; none has been asserted simultaneously
activatable or frozen. These observations locate the next problem and are
not an arbitrary-n theorem or a compensation certificate.

The next question is whether a boundary-aware version of the untouched-mixed
and color argument closes the seam candidates of connected copies, or whether
new opposite-color hole pairs require additional distinct resources. Such
resources must be counted jointly across components, with their original
identities retained. The universal mixed-direction problem and the numerical
5/6 improvement remain open. No submitted-manuscript or email change is made.
