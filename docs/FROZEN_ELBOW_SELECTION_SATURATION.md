# Fully frozen elbow loss survives every retained-selection extension

26 October 2026. Wenlin Zhang and Haobo Ma. Independent research continuation.

The fully frozen elbow obstruction is stable under **every feasible addition
of selected vertices**, including inclusion-maximal extensions and extensions
of maximum cardinality retaining the original selections. On the 16-by-28
board the exact retained-selection maximum is **184**, with numerical slack
and full original resource count both **5**. All 70 matching endpoints remain
frozen. The four-state destructive repair interaction survives unchanged.

The unrestricted fixed-P maximum is instead **186**. We prove both maxima
by disjoint geometric covers and explicit feasible attainers; the optimizer
used to discover attainers is unnecessary for checking either bound. Thus
retaining the original selection pattern costs exactly two selections. This
is a strengthening of a fixed-adapter obstruction, not a proof that unrestricted
fixed-P maximization preserves it, nor an obstruction after optimizing N.
The earlier [singleton saturation result](SELECTION_MAXIMUM_SINGLETON_OBSTRUCTION.md)
already distinguishes retained and unrestricted maxima on a different P
family. The contribution here is stability of the **fully frozen rank-one
elbow withdrawal and destructive joint direction repair**, with exact 184/186
bounds for this board. The submitted 11 October manuscript is untouched.

## 1. Fixed objects and the four direction states

Use exactly the board, actual matching M, 83 selected vertices T0 and
canonical tile bits in [the full-freezing construction](FULLY_FROZEN_ELBOW_WITHDRAWAL_OBSTRUCTION.md).
Let P be its 70 actual matching endpoints; |M|=35 and area/2=224. The old
11-wave strict freezing certificate covers all P. Coordinates are zero based.

E changes only the P-free tile (10,16) from V to H. F changes the two H tiles
(2,12),(4,12) to V. Canonicalize into maximal same-direction bands separately
in each state. All source/owner identities and physical links are the same
in the four states. The two alpha owners are a with tips (3,12),(10,12),
and b with tips (5,17),(12,17). The only other source-reachable owner is mixed
z with TP (5,15), BP (5,16); its sole incoming external link is b->z.
No reachable beta or further mixed exit exists. There are two beta and five
mixed owners globally, and all original units are retained in the model.

Write the three original resource identities by their physical forest cells:

    Q={(4,13),(5,13)}, J={(4,12),(4,13)}, K={(10,16),(11,16)}.

| E | F | a's entire support | z's entire support | b's support | V | minimum links |
|---|---|---|---|---|---:|---:|
| absent | absent | empty | Q | empty | 1 | 1 |
| absent | present | J | empty | empty | 1 | 0 |
| present | absent | K | Q | empty | 2 | 1 |
| present | present | J,K | empty | empty | 1 | 0 |

Each displayed unit is private to its indicated owner. In particular two
units assigned to a cannot pay b or pay a twice. These facts were established
for T0 in the preceding note; we now prove that arbitrary feasible extensions
T containing T0 preserve this entire table.

## 2. A general protection lemma

Fix any graph, a set P, and disjoint selected vertices T0. Feasibility means
that each selected vertex has at most one neighbor in P union T. Define

    C(T0)={v outside P union T0 : T0 union {v} is feasible}.

**Lemma (candidate hull and protected regions).** If T is feasible and
T0 is contained in T, then T minus T0 is contained in C(T0). Consequently,
if a vertex set G is disjoint from C(T0), then T intersect G=T0 intersect G.
If an initially blank vertex has two distinct neighbors in P union T0,
it remains blank in every such extension.

**Proof.** Feasibility is hereditary under deletion of selected vertices:
deleting selections can only decrease occupied neighbor counts at every
retained selected vertex. For v in T minus T0, the subset T0 union {v}
is therefore feasible. This is exactly v in C(T0). A changed label in a
protected G would be such a v, contradicting disjointness. A vertex with
two baseline occupied neighbors could not itself be selected in any extension,
since those neighbors remain occupied. This proves all assertions on arbitrary
graphs, without a finiteness, maximality or enumeration hypothesis. ∎

For computing C(T0), a blank v belongs precisely when (i) v has at most
one baseline occupied neighbor, and (ii) every adjacent old selected vertex
has zero baseline occupied neighbors. Condition (ii) ensures that adding v
does not create a second neighbor at an old selection. Thus exclusion is
certified by a selected vertex with two distinct occupied neighbors after
adding v, using only a constant-size local neighborhood.

Four general statements are formalized in
[SelectedExtensionProtection.lean](../formal/SubQuorum/SelectedExtensionProtection.lean):
heredity, candidate hull containment, protected-region label invariance, and
the two-occupied-neighbor obstruction. All are axiom-free. The region theorem
assumes decidable baseline membership, as provided by this finite board.
Concrete coordinates, the cover below and the physical compiler are outside
that Lean scope.

Subsequent [fixed-P extremal construction](FIXED_P_MAXIMUM_FROZEN_ELBOW.md)
resolves the question left open here: a different186-point attainer is
completely frozen and retains the rank-one elbow and destructive E/F
interaction. The184 retained-extension bound in this note remains exact.

## 3. Protecting all types, links and source-reachable supports

First protect the type of **every** free P tip, not just the tips in the
reachable kernel. Every old TP retains its selected N partner. The nine old
BP partners have these two-neighbor obstructions:

| BP tip | blank N partner | two baseline occupied neighbors |
|---|---|---|
| (4,9) | (4,8) | (3,8),(4,7) |
| (5,16) | (4,16) | (3,16),(4,15) |
| (6,9) | (6,8) | (5,8),(6,7) |
| (6,20) | (6,21) | (5,21),(6,20) |
| (8,9) | (8,8) | (7,8),(8,7) |
| (8,20) | (8,21) | (7,21),(8,20) |
| (9,7) | (9,6) | (9,7),(10,6) |
| (10,20) | (10,21) | (9,21),(10,20) |
| (11,22) | (11,23) | (11,22),(12,23) |

None of these N partners changes under E or F. No BP can become TP. P, M
and the PP part of N are fixed in each state; hence every owner body, all
terminal types, alpha/beta/mixed classes and physical TP->BP links are
unchanged under every extension. No new alpha or exit can appear remotely.
In particular the source-reachable owner set stays exactly {a,b,z}.

It remains to protect **all maximal no-P gaps with a boundary in any of the
three owner bodies**. Testing only terminal tips would miss body-supported
resources. For the state without E or F the complete gap list is:

| orientation | rows (inclusive) | columns (inclusive) | capacity |
|---|---|---|---:|
| H | 2..3 | 13..27 | 0 |
| H | 4..5 | 12..14 | 1 |
| H | 10..11 | 13..15 | 0 |
| H | 12..13 | 14..16 | 0 |
| V | 2 | 10..11 | 0 |
| V | 11 | 10..11 | 0 |
| V | 4 | 18..19 | 0 |
| V | 13 | 18..19 | 0 |

All these gap cells are disjoint from C(T0), which has 181 vertices.
The [protection certificates](../output/frozen-elbow-selection-saturation-validation.json)
list every gap cell and an explicit selected degree-two witness for **every
blank cell** in the list. They are local certificates, not an infeasibility
claim from a black-box optimizer.

Under E, replace the H gap at rows10..11 by columns13..17, capacity1.
Under F, remove the first two H gaps in the table and replace them with
H rows4..5 column14 (capacity0), V row2 columns12..13 (capacity0), and
V rows4..5 columns12..13 (capacity1). The other gaps are unchanged.
Applying both makes both replacements. Each resulting gap is again disjoint
from C(T0), with its own complete blank-cell certificates. Thus all four
states have protected complete body-boundary gap lists (8,9,8,9 gaps).

By the protection lemma all selected/blank labels in these gaps stay fixed.
P and the band boundaries stay fixed as well. Therefore their positive
BB/TT forests and their whole-support incidences retain their exact physical
cell identities. No unprotected remote forest is adjacent to a reachable
owner, so no remote change can supply a new payment. The table in Section1
holds for **every** feasible extension, including all optimal ones retaining
T0. Added selections also preserve the old strict freezing witnesses, so
all 70 endpoints remain frozen; the four alpha tips remain of degree three,
since their only initially blank neighbors already face two occupied vertices.

The full raw inventory may decrease dramatically outside the kernel. It is
not assumed constant under adding selections. Because alpha=beta=2 remain
fixed, the exact inventory identity is

    L=S=224-|T|-35=189-|T|.

## 4. Exact retained-selection maximum: 184

Partition the board into aligned disjoint 2-by-2 tiles. Every new selection
lies in C(T0). Any three selected sites in a 2-by-2 square give one selected
site two selected neighbors, so every tile holds at most two new selections.
A tile with no candidate holds zero; a tile with a single candidate holds
at most one. Here those rules give the following additional-selection bounds,
with rows corresponding to top coordinates 0,2,...,14 and columns0,2,...,26:

```text
2 2 2 2 2 2 2 2 2 2 2 2 2 2
2 2 0 0 0 0 0 0 0 0 0 0 0 0
2 2 0 0 0 0 0 0 0 0 0 0 0 2
2 2 0 0 0 0 1 0 0 0 0 0 0 2
2 2 0 0 0 0 0 0 0 0 0 0 0 2
2 2 0 0 0 0 0 0 0 0 0 0 0 2
2 2 2 2 2 2 2 0 0 0 0 0 0 2
2 2 2 2 2 2 2 2 2 2 2 2 2 2
```

Their sum is101. (The sole cap1 tile has just one candidate.) Consequently
every extension satisfies |T|<=83+101=184. The permanent
[fixture](../develop/fixtures/frozen_elbow_selection_saturation.json) gives
an explicit feasible 184-point set containing T0. It attains every tile
bound. Checking its selected neighbor counts proves attainability, so the
maximum is exactly184 without relying on any global search certificate.

For every attaining extension, Section3 gives L=S=5 and the exact four-state
values (1,1), (1,0), (2,1), (1,0). All 70 endpoints remain frozen. In
particular F still has withdrawal loss r=1 when applied to an unpaid old a;
and applying F after E still reduces total payment from2 to1. The original
large slack106 was unnecessary for this rule failure. Slack5 is positive,
so this remains no counterexample to the numerical target inequality.

## 5. Exact unrestricted fixed-P maximum: 186

Now retain only P and M, allowing all T to be rebuilt. The same square rule
and exclusions from fixed P give these aligned-tile upper bounds:

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

For cap1 tiles, every pair of candidates creates a selected vertex with two
occupied neighbors; the validation record provides the explicit witness
for each pair. Cap0 has no individually allowed site; cap2 is universal.
The sum is189. Three **pairwise disjoint** 4-by-2 patches each improve their
two constituent cap2 tiles to cap3. It suffices to give a partition of each
patch's six allowed sites into three forbidden pairs:

| patch origin | forbidden pair 1 | forbidden pair 2 | forbidden pair 3 |
|---|---|---|---|
| (2,12) | (2,12),(2,13) | (3,13),(4,13) | (5,12),(5,13) |
| (8,12) | (8,12),(8,13) | (9,13),(10,13) | (11,12),(11,13) |
| (10,16) | (10,16),(10,17) | (11,16),(12,16) | (13,16),(13,17) |

Each pair is physically adjacent, and at least one endpoint already faces
a fixed P neighbor. Selecting both would give it two occupied neighbors.
The middle exclusions and outer exclusions are instances of the earlier
adjacent-tile cap3 argument, not a new principle. At most one site from
each pair may be selected. Replacing the six original cover tiles by these
three disjoint patches therefore gives |T|<=189-3=186. No cell or saving is
used twice. A second explicit feasible set in the fixture has186 selections,
proving equality by direct neighbor checks.

This particular unrestricted attainer freezes only45 of70 endpoints. It
loses some old seals and changes the source types. We draw **no conclusion**
that all unrestricted maxima behave this way, that none can be fully frozen,
or that no unrestricted maximum can realize some other elbow obstruction.
The established fact is exact: no maximum of size186 can retain all T0,
because the retained maximum is184. The next stronger question is whether
one can retain enough, or rearrange the seals, to obtain both unrestricted
maximal cardinality and the completely frozen rank-one interaction.

## 6. Arbitrary copies and arbitrary feasible global extensions

Take any q copies with the old 16-row spacing and H guard tile rows, as in
the preceding theorem. Let E,F be arbitrary sets of copies on which the
respective direction operations are applied. Let T be **any feasible global
extension** of the union of all translated T0, possibly adding vertices at
the copy borders. Then

    V(E,F;T)=q+|E minus F|,
    C(E,F;T)=q-|F|,
    D(E,F;T)=q-|E minus F|.

**Proof.** The baseline occupied-neighbor certificates, all BP partners and
all protected reachable gaps are internal to their copies. Every new selected
vertex in a copy is individually allowed at its baseline: restriction to
that copy deletes selections and preserves feasibility. The Section3 proof
therefore holds in every copy. The fixed M/N ownership graph has no copy
crossing: P is internal, all actual M edges are internal, H guard tile rows
prevent V-band crossings, and H bands and links stay in row pairs. Adding
selections changes none of these facts. Thus no new source or payment exit
can connect two copies, even if feasibility of added boundary selections
couples the choices. Each a_i is paid iff i is in E union F, while b_i is
paid iff i is outside F. Their units and owners are all distinct. Each paid
b_i uses its single necessary link. Summing proves the three formulas. ∎

All70q endpoints retain the translated 11-wave certificate. The theorem
applies in particular to every inclusion-maximal extension and every maximum
retaining the baseline, whose existence follows from finiteness. We do not
assert that these q-copy maxima equal184q or186q: the exhibited saturated
one-copy attainers have incompatible top/bottom occupancies when concatenated.
No additive extremal cardinality formula is needed for this theorem.

## 7. Validation and remaining question

```text
python3 develop/check_frozen_elbow_selection_saturation.py \
  --output output/frozen-elbow-selection-saturation-validation.json
python3 develop/check_selected_extension_protection_formal.py \
  --lean /path/to/lean-4.33.0 \
  --output output/selected-extension-protection-formal-validation.json
```

The standard-library validator checks the two feasible attainers, disjoint
geometric cover bounds, every BP obstruction, every blank in every reachable
body-boundary gap in all four states, all181 single-addition boards,
16 independently generated inclusion-maximal extensions (q=1,2,3,7), and
792 extension/action profiles. All36 selected independent primitive optima
agree with the flow optimizer; 65,520 independently replayed strict-rank
events pass. The arbitrary-extension and arbitrary-q conclusions follow
from the general proofs above, not extrapolation from these samples.

Four Lean declarations pass locally with no axioms, warnings, sorry or native
evaluation. Memory and actual lean/lake comm basenames are measured before
the run. This formalization covers the graph-theoretic protection mechanism;
physical coordinate certificates, the covers and network optima remain
written and executable verification, not end-to-end Lean.

A temporary Z3 optimization discovered the two attainers. No Z3 dependency,
solver output or optimality claim is needed by the permanent validator:
upper bounds are the stated disjoint covers and lower bounds are feasible
point lists. The prior freezing-replay formalization is reused unchanged.

The remaining gap is **unrestricted fixed-P extremality together with full
freezing and this resource-loss mechanism**, or a theorem explaining how a
joint direction choice avoids that loss. A universal improvement over5/6
has not been established. This continuation performs no email operations,
changes no submitted manuscript, public main, PR3, shared CI or C4 result.
