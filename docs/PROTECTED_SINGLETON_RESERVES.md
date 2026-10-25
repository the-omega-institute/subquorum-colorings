# Protected singleton intervals: persistent compensation and exact elimination

25 October 2026. Continuation of
[FROZEN_BETA_FORK_ESCAPE.md](FROZEN_BETA_FORK_ESCAPE.md).

The sealed escape-cycle example has a useful positive feature: a different
original interval beside the far end of its bent alpha cannot be sealed by
any feasible extension retaining the old selections and actual matching.
It is a private, persistent payment for that alpha. We prove the geometric
locking lemma, identify its exact ownership, and eliminate any collection of
such sources from both ordinary and full beta-fork compensation, preserving
maximum value and minimum links exactly. A sharpened frozen family has only
one such alpha-support interval per copy; reserving r of these units forces
exactly r links, paid by r different whole betas.

These results settle a concrete completion class, not the existence of a
protected interval at every frozen fork. The universal grid compensation
statement and 5/6 improvement remain open.

For residual sources sharing two-column pockets rather than possessing
private singletons, see
[SHARED_POCKET_COMPLETION_AND_JOINT_DEFICIT.md](SHARED_POCKET_COMPLETION_AND_JOINT_DEFICIT.md).
Its exact joint graph count and frozen full-pool cost obstruction distinguish
shared completion from this private-source elimination.

## 1. A single column that cannot be filled

Use zero-based horizontal bands. Let r be even and c strictly inside the
board. In a feasible starting pair (T0,M0), write P0=V(M0), and suppose

    u=(r,c),       v=(r+1,c)       are blank;
    a=(r,c+1),    x=(r,c-1), h=(r-1,c) are in P0;
    t=(r+1,c+1)                  is in T0.

Thus the upper blank has three occupied, already matched neighbors, while
the lower blank is next to a selected vertex already seeing a:

```text
                   P h
               P x . u P a
                   . v T t
```

The displayed positions are all distinct. The diagram does not prescribe
the old mates of a,x,h beyond their belonging to M0. The reflected patterns
are included by transporting the grid, band convention and old matching.

A *monotone feasible extension* has T0 subset T1 and M0 subset M1; it may
add selections, matching edges, rows or columns, but keeps the old band
phase and old coordinates. Every new selected vertex still has at most
one occupied neighbor, and the new matching is disjoint from all selections.
No final freezing assumption is imposed.

**Lemma 1 (protected singleton).** Both u and v remain blank in every such
extension.

**Proof.** The old selected vertex t still sees a. It cannot have a second
occupied neighbor v, so v stays blank. The vertex u cannot be selected,
because it sees the two distinct old occupied vertices a and x. If u were
a new matching endpoint, its actual mate would be one of a,x,h,v. The first
three retain their old matching partners, and none could have been matched
to the initially blank u. Matching uniqueness excludes all three. The fourth
is blank. Thus u cannot be a matching endpoint either. QED.

This is a statement about arbitrary feasible extensions, with no appeal to
finite searches or freezing ranks. It uses occupied neighboring bands and
old actual mates; the alpha may have arbitrarily many bends elsewhere.

## 2. Private ownership and persistence

Add the following hypotheses:

- a is a TP tip of an original alpha A;
- y=(r+1,c-1) is P0, and the PP column {x,y} belongs to an original pure
  PP/M cycle C;
- the singleton interval (band=r/2, first=c, last=c) is available, with
  only the standard outer boundary marks or other reservations excluding it.

**Lemma 2 (persistent private interval).** The same coordinate interval
remains an available original singleton with exactly one eligible open
owner, A, throughout every monotone feasible extension. The entire original
alpha A and cycle C retain their vertex sets and types.

**Proof.** Every vertex of A retains its actual mate. Its internal PP columns
retain both endpoints and their fixed band partners. Its two TP ends retain
their selected partners, so cannot acquire new PP partners. Thus the whole
original A component is unchanged. Likewise all old cycle vertices retain
their actual mates and PP partners; C stays a closed cycle, with no opening
through which a new strand could join it.

Lemma 1 preserves the BB column. Its immediately neighboring columns remain
P-containing: the alpha TP on the right and the cycle PP on the left. It
therefore stays a maximal one-column endpoint-free gap, with a singleton
BB--TT interval identity independent of any integer renumbering elsewhere.
Being strictly internal, it has no outer boundary mark. Whole-support
eligibility comes only from these two boundary columns. The cycle has no
open owner, and A is the sole eligible open owner. QED.

The left boundary need not be a two-vertex cycle: any original closed PP/M
cycle works. The matching-lock argument uses the old three neighbor mates,
not freezing invariance under cycle normalization.

For any q different original alphas with such private intervals, choose one
for each. These q choices are automatically different: a shared coordinate
interval cannot have two different sole eligible owners. Consequently all q
sources have simultaneous zero-link payments, with no beta spent. The same
proof applies after other available interval units have been reserved.
A deliberate reservation of one of the q private units removes that payment
and is outside this conclusion.

## 3. Exact elimination in the whole-support models

The following elementary network reduction makes the consequence stronger
than a collection of separately valid payments. It applies to the ordinary
model and the [full two-BP beta-fork model](WHOLE_SUPPORT_FORK_FLOW_AND_RESOURCE_CUTS.md).
No new general flow theorem is claimed.

Let S be q alpha sources, and assign a different available original interval
j_a to each a in S. Assume j_a is supported by a and by **no other open
owner**, including mixed and beta bodies. Delete these q sources, their
links, and these q interval identities to obtain the residual system N^-.
Other owner supports lose only those identities. Write V,c for maximum
payment and minimum link count at that value, and V^-,c^- for the residual
optima.

**Theorem 3 (exact private-source elimination).**

    V = q + V^-,            c = c^- .                         (1)

Every attainable set of paid outside sources remains attainable after
requiring all of S to be paid by their private units. This can release
shared resources and links; it does not promise to preserve an arbitrary
old used-resource set or the literal old fork decomposition.

**Proof.** A residual packing extends by q zero-link private payments.
In the network, add the q disjoint paths s->a->j_a->t. This gives value
q+V^- at cost c^-.

Conversely take any integral full flow. A path reaching j_a must come
directly from source a: the only support arc into j_a is from a, and no
other source can enter an alpha node. If a is unpaid, its private unit is
unused and its private path can be added. If a is paid along another route,
replace that route by its private path. This releases all its former
mixed, BP-entry, beta and interval capacity and adds no link cost. Distinct
j_a make all replacements compatible. No outside source path is removed.

All q sources can therefore be paid privately. Removing their paths leaves
a feasible residual flow. At a full maximum V this proves V-q<=V^-; the
extension bound gives equality. At a minimum-cost maximum, removing the
private paths yields a residual maximum of cost at most c, so c^-<=c.
The initial extension gives c<=c^-, proving (1).

In the full model, removal of one arm can leave a beta's remaining arm
ending at an interval instead of its unused private beta sink. The existing
free beta normalization redirects that arm to the whole beta, preserving
value and links while releasing the interval. Thus the network argument
lifts to legal ordinary stems and beta forks, including this case. QED.

For the physical ledger, if k is the full alpha count and I the available
original interval set, then

    |I|+b-k = (|I|-q)+b-(k-q),
    k-V = (k-q)-V^-,
    |I|+b-V = (|I|-q)+b-V^- .                                (2)

Each private source and its one unit disappear together. There is **no
additional q-unit surplus** to add elsewhere. Equation (1) settles the
protected sources and leaves exactly the residual problem. If every alpha
has such a reserve, all are paid with zero links and the conditional packet
bound S_J>=B follows. This does not make the hypothesis universal.

## 4. The sealed-cycle family has such a reserve

In the previous plugged 12x14 fixture use

    r=8, c=10;
    a=(8,11), t=(9,11), x=(8,9), y=(9,9), h=(7,10).

The left pair {x,y} is an original two-point pure cycle. The upper neighbor
h is also already matched. Thus the original singleton (4,10,10) is private
to the bent alpha with TP tips (5,5),(8,11), and Lemmas 1--2 protect it in
every feasible extension retaining the old matching and selections.

For q copies translated by (12i,0), the protected identities are
(4+6i,10,10). This remains true with any even blank right padding. Boundary
padding can release *other* original intervals; the assertion is persistence
of these q identities, not equality of the padded supports to the old lists.
Any such extension has at least these q settled old sources. New sources
and their residual compensation must still be handled separately.

## 5. A sharp one-unit variant and reservation cost

Start with the plugged fixture and add the selected point w=(4,12).
It has only one occupied neighbor, (4,11); all its other neighbors are blank.
No old selected point becomes adjacent to it, so feasibility holds. All old
freezing witnesses remain valid. There are now 20 selections and 52 matching
endpoints, all frozen, with the same one alpha, one beta and two mixed
strands. The added selection removes precisely the other alpha-support
singleton (2,12,12). There are 26 available original intervals, and the
alpha's whole support is **exactly** {(4,10,10)}.

Take q separated copies, with no extra right padding. Each original alpha
has just its one distinct protected unit, there are q distinct original
betas, and all q direct links (5+12i,5)->(5+12i,4) exist. The construction
and freezing certificate transport to every q, giving 20q T, 52q P,
26q available original interval units, q alphas, q betas and 2q mixed owners.

**Proposition 4 (exact reservation profile).** Reserve any subset R of the
q protected interval identities. In both ordinary and full models,

    maximum payment = q,
    minimum number of links at full payment = |R|.             (3)

**Proof.** Pay every unreserved source by its own unit, and pay each reserved
source using its direct link into its own beta. All units and all beta
owners are different. This gives q payments with |R| links. Every reserved
source has no remaining zero-link interval payment, so its unit source
flow must use at least one link before reaching any resource. Different
source paths use different link arcs, including in the full model with
separate BP entries; hence at least |R| links are necessary. QED.

The |R| beta credits are existing credits, not additional resources created
by reservation. Formula (3) is for the specified unpadded family; padding
or unrelated additions can provide additional source supports and lower
the cost, so the equality is not asserted for arbitrary extensions.

## 6. Why the fixed-old-matching hypothesis matters

Retaining T0 and the old endpoint set alone is insufficient for Lemma 1.
In the plugged fixture, use the alternating augmentation

    (8,10), (7,10), (6,10), (5,10),
    (5,9),  (4,9),  (4,8),  (3,8).

Remove its three old matching edges at positions 1--2,3--4,5--6 and insert
its four even-position edges. The old T and every old P survive; the two
new endpoints are (8,10) and (3,8). No new endpoint touches a saturated old
selection. The pair is feasible, but u=(8,10) now occupies the protected
column. Its mate (7,10) has changed, exactly violating the locking hypothesis.

This particular extension has only 32 of its 54 endpoints frozen. It is a
counterexample to dropping fixed mates from the **arbitrary feasible
extension** theorem. It does not refute a stronger theorem with complete
freezing imposed, nor persistence under the stated monotone extensions.
No finite failed rematching search is used as a nonexistence proof.

## 7. Verification and remaining scope

The solver-free checker scans the actual labels, old PP/M cycle ownership
and coordinate interval identities. It reconstructs the physical frozen
copy/padding controls, the one-unit variant, and feasible monotone random
extensions with old selections/matching retained. Extensions retain empty
outer columns so the existing packet adapters apply. It compares (1) for
both ordinary flow and full beta-fork flow, and uses independent primitive
packing on the small abstract and physical controls. It checks every
reservation subset through eight physical copies and representative sizes
through twelve; Proposition 4 proves all q and all subsets.

The abstract controls enumerate every terminal-link subset and single
external-unit support pattern for AAB, AAM, ABB and AMM, with and without
the external unit reserved, plus seeded larger models. A two-alpha one-unit
negative control confirms that shared resources cannot be called private.
Finite checks corroborate the proofs above and do not replace them.

The final run passes 26,568 full/residual value-and-cost comparisons and
13,061 independent primitive-packing comparisons, 72 frozen copy/padding
boards and 12 sharp one-unit boards, 160 feasible monotone extensions
with 8,435 accepted additions and 319 protected-source checks, and 556
physical reservation subsets (1,112 ordinary/full solver comparisons and
14 independent physical packs). There are 12,800 exhaustive abstract
models, 240 seeded models and the two explicit hypothesis controls.
These counts describe overlapping check families, not disjoint universes.

Lean proves the actual integer-grid locking implication from selected
feasibility, four-neighbor adjacency and the actual mate involution, derives
old-neighbor mate exclusions from retention, and proves private-choice
injection. The full original-strand persistence, flow elimination and all-q
physical profile remain written proofs with computational checks. The formal
scope is recorded separately, with no custom axioms, sorry or native_decide.

```sh
python3 develop/check_protected_singleton_reserves.py \
  --output output/protected-singleton-reserves-validation.json
cd formal
lean SubQuorum/ProtectedSingletonReserve.lean
```

No new external review, mailbox read, draft edit or send is claimed. The
submitted 11 October manuscript, public main, PR #3, shared CI and separate
star-forming/C4 work are preserved. The next step is to analyze residual
sources with no protected singleton and determine whether their longer-cycle
or mixed-path boundary provides a different jointly usable reserve. This
note does not assert that every escape cycle forces the protected pattern.
