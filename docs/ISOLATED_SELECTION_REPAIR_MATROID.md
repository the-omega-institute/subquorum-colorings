# Choosing isolated-selection repairs with protected sources and exact budgets

Follow-up: [fixed-partition coverage obstruction and exact strip repair](ISOLATED_COVERAGE_OBSTRUCTION_AND_STRIP_REPAIR.md) disproves automatic full candidate coverage even after all occupied-isolated selections are deleted, and gives a zero-loss direction repair with actual matching crossings.

25 October 2026. Wenlin Zhang and Haobo Ma. Independent research branch.

The preceding [two-sided path analysis](TWO_SIDED_SEAM_BUDGET_AND_UNBOUNDED_RECOURSE.md)
shows that the position of a one-resource repair controls its rerouting cost.
Here we give a general location-selection principle, retaining arbitrary mixed
routing, both physical beta entry gates and whole-beta forks. Deleting an
isolated selected point adds one immutable original resource and changes no
old terminal data. Candidate repair gains are a contraction of the standard
resource matroid. This gives the exact deletion budget, weighted greedy
selection and one joint optimization of repairs and link costs while
retaining every previously paid source.

The matroid and flow arguments are standard. The contribution is the physical
isolated-deletion adapter and its precise integration with the full strand
model, including source preservation and the distinction between selecting
repair locations and merely rerouting a fixed location. Full compensation
requires an explicit feasibility test; it is not inferred from freezing.

## 1. Physical hypothesis and an identity-preserving deletion lemma

Fix a feasible pair (T,M) on an even-by-even board, partitioned into disjoint
even-by-even rectangles, with horizontal or vertical two-line bands chosen
in each. The uniform horizontal decomposition is a special case. P=V(M)
and this auxiliary matching N are fixed. Restore all actual matching edges,
including crossings of the region boundaries, before identifying global
owners. Use the complete BB/TT-forest resource convention, including boundary
units, and whole-owner supports.
Choose ANY candidate set X contained in T such that each x in X is isolated
in the occupied graph induced by T union P: x has NO occupied grid neighbor.
We do not combine resource identities from different decompositions.

Each x=(r,c) has a blank band partner; its original band column is BT. Define

    j_x=(region, local band, local column, local column).

In the single horizontal-region compiler this reduces to
j_x=(floor(r/2),c,c); a fixed concatenation of all region bands is another
equivalent immutable encoding. The band column means the two-cell N pair,
with columns along that region's band direction.

These identities are different for different x: two selected candidates
cannot occupy the two cells of one auxiliary pair, since that would make
them adjacent. Put E={j_x:x in X}, and let Q0 be the complete old pool.

**Lemma 1 (commuting physical deletion).** For every Y subset X, delete just
Y from T, retaining P,M and the bands. Then:

1. the pair remains feasible;
2. every endpoint neighborhood and the old freezing process are unchanged;
3. all original strands, terminal TP/BP types, links and beta entry gates
   are unchanged;
4. the new original pool is EXACTLY Q0 disjoint-union {j_x:x in Y};
5. all old support incidences persist; each new unit has exactly the whole
   owners bounding its unchanged no-P gap as its support;
6. numerical slack increases by |Y|.

In particular, full freezing is preserved if present initially. Isolation
in T alone is insufficient: the no-P-neighbor condition is required for
endpoint neighborhoods and types to stay unchanged.

**Proof.** Deleting selected points cannot increase occupied degrees, so
feasibility persists. No candidate touches P, hence all selections adjacent
to endpoints and all actual mates are identical. The old freezing schedule
has precisely the same witnesses, and the complete endpoint closure process
is identical. Auxiliary PP edges depend only on P. A terminal's TP label
depends on its selected band partner, which is adjacent to it; no candidate
is such a partner. Thus strand bodies, types, links and beta tips persist.

Deleting x changes its single auxiliary column from BT to BB. Neither
adjacent column can be TT before deletion: a selected cell of such a TT
column would see its selected auxiliary mate and x, two occupied neighbors.
Deletion creates no TT column. Consequently this new BB column is an
isolated BB/TT-forest component, with identity j_x. No old BB/TT component
can merge or split, since the changed column was BT and its neighboring
columns are not TT. This remains true under simultaneous deletion; distinct
new BB columns do not connect to each other, because a forest adjacency
requires a TT endpoint. Thus all old identities are literally unchanged,
and each deletion adds one different unit. P and no-P gap boundaries are
unchanged, proving the support assertion. Finally |T| falls by |Y| while
area and |M| stay fixed. QED.

This lemma deliberately excludes deleting a member of an adjacent TT pair.
For an explicit counterexample to that broader identity claim, take a 2-by-4
board with no P and T={(0,1),(1,1)}. Initially Q0={(0,0,2),(0,3,3)}. Delete
(0,1); the new pool is {(0,0,0),(0,2,2),(0,3,3)}. Its count rises by one,
but the old identity (0,0,2) disappears and two new ones replace it. Thus
having no P neighbor alone does not justify resource-only extension.

## 2. One candidate repair matroid, including all beta capacities

Compile the unchanged terminal network once, allowing every candidate
resource in E. Mixed gates have capacity one. Each beta has its TWO distinct
physical BP entry gates, each capacity one, and ONE private whole-beta sink.
All original interval sinks have capacity one globally. Candidate resources
are the new distinct interval sinks; no beta credit is duplicated.

For C subset E let V(C) be the maximum payment with Q0 union C available,
and set

    p=V(empty),    r(C)=V(C)-p,    R=r(E).                   (1)

Private beta sinks remain available for every C. In particular p need not
be zero, and beta payments may survive when all candidates are absent.

**Theorem 2 (exact candidate selection).** The function r is a matroid rank
on the finite candidate set E. For any initially chosen maximum payment
of p old alpha sources, ALL those source identities can be retained while
attaining V(C), for every C. Consequently:

    maximum payment with at most b deletions = p+min(b,R);  (2)
    minimum deletions to attain V(E) = R.                  (3)

An inclusion-minimal repair set attaining V(E) is exactly a basis of r;
it has R members. Full compensation of all k alpha sources is achievable
by these deletions if and only if V(E)=k, and then exactly k-p deletions
suffice and are necessary within this candidate operation class.

**Proof of rank.** The established resource-gluing cut argument shows that
V(C) is integer, monotone and submodular as a function of the available
original sink set, with every one-unit increment at most one. Equivalently,
first regard V_total(F)-V_total(empty) as the standard resource matroid rank
on all intervals, with private-beta baseline subtracted; fix Q0 available
and contract it. The contracted rank is precisely (1). It is normalized,
integer and submodular, 0<=r(C)<=|C|, so it is a matroid rank.

For completeness, a cut consists of source-arc costs plus unit gates and
original sink arcs. Uncross two minimum source sides for candidate sets
C,D: use the intersection of their source sides for C union D, and the
union of their source sides for C intersect D. The resulting cuts have
total capacity at most the original two. A candidate sink charged in the
union/intersection contributes
no more than its contributions in the two original cuts. All private-beta
and internal gates are the same in both networks. This proves submodularity.
Deleting the at-most-one path ending at a newly added resource proves the
single-increment bound. Thus beta forks do not invalidate the rank argument.

For source preservation, represent the chosen old maximum as integral flow.
Enable C and augment along simple source-to-sink residual paths, stopping at
the first sink visit. Such a path never re-enters the super-source, so it
never traverses the reverse of a source arc. Every initially saturated old
source arc stays saturated. Flow normalization at a beta preserves starting
source identities. This yields V(C) while keeping all p old payments.

An independent subset B of a basis of size R has r(B)=|B|, proving (2)'s
lower bound. Every C has gain at most |C| and at most R, proving the upper
bound. A basis gives (3). If a spanning set is inclusion-minimal, each of
its elements is indispensable, so it is independent and has size R; a
redundant element could otherwise be removed without lowering its rank.
Conversely each basis is minimally spanning. Apply Lemma1 to identify every
chosen candidate subset with its actual simultaneous physical deletions.
No resource or deleted point is used twice. QED.

**Corollary 2a (no hidden joint opening gain).** If V({j_x})=p for EVERY
candidate x, then V(E)=p. More generally, once no remaining single candidate
increases the reoptimized value at the current repaired pool, no combination
of those remaining candidates can increase it. This follows from diminishing
returns: each zero marginal remains zero as the pool grows. It concerns
the fully reoptimized value with old source identities retained, not a test
against one fixed old routing. Thus it supplies an exact stopping criterion
without checking all simultaneous opening subsets. The earlier path's need
for large joint WITHDRAWAL tests is compatible with this statement: losses
under removal and gains under addition have different marginal directions.

**Corollary 2b (one combined budget).** Let S0 be the old numerical slack,
D0=k-p the old deficit, and SY,DY the corresponding values after deleting
Y. With C={j_x:x in Y},

    SY+DY=S0+D0+|Y|-r(C) >= S0+D0.                         (4)

Equality holds exactly for independent repair sets. Lemma1 gives
SY=S0+|Y|, while DY=D0-r(C); adding proves the identity. Each physical
deletion is counted once and each payment gain is one rank increment.
Opening resources can improve payment but cannot lower this combined
budget. Redundant deletions make its excess strictly larger. In particular,
the optimal R-deletion repair preserves S+D exactly. This extends the
previous path family's budget identity to arbitrary internal gates, beta
forks and fixed mixed-direction partitions under the isolation hypothesis.

The exact R-operation claim concerns this specified family of isolated
selection deletions. It does not optimize over arbitrary reselection of T,
replacement of P or changes of auxiliary partition.

## 3. Weighted repair locations and the limit of greedy selection

Give every candidate an integer nonnegative deletion weight w_x. Among
minimum-count repairs attaining V(E), minimum total weight is obtained by:

    sort candidates by nondecreasing w;
    start C empty;
    add x exactly when V(C union {j_x}) > V(C).

**Corollary 3.** The result has exactly R members, achieves V(E), retains
all old paid source identities after rerouting, and has minimum total
weight among such repairs.

**Proof.** This is the standard matroid minimum-weight basis argument.
At each step extend the current chosen independent set to an optimal basis.
If the next greedy element is absent from that basis, basis exchange gives
an element outside the current chosen set that it can replace. That element
cannot have smaller weight: if processed earlier and rejected, it was
already dependent on an earlier greedy subset and remains dependent after
that subset grows. Replacing it preserves an optimal extending basis.
Induct until rank R. Source preservation follows from Theorem2. QED.

Greedy ties do NOT promise minimum link cost. In the lower-path physical
family every one of the upper seams is a one-element basis for the
remaining gain. All can have the same deletion weight. Choosing position
p costs k+p links; choosing p=1 costs k+1. An arbitrary equal-weight tie
can therefore have unbounded excess link cost. This does not refute greedy
minimum deletion weight; it refutes adding a secondary link guarantee to it.

## 4. Joint repair choice and route optimization in one flow

There is no need to enumerate all bases to include link cost. Use the network
containing Q0 and ALL candidate resources. Mark the chosen p old paid source
arcs. First maximize flow value. Among maximum flows lexicographically:

    retain the greatest number of marked old sources;
    minimize the number of candidate sink units used;
    minimize their total deletion weight;
    minimize actual selected link count.                  (5)

Assign the corresponding lexicographic costs to marked source arcs,
candidate sink arcs and declared link arcs. Capacities retain the actual
mixed and separate beta-entry gates. A minimum-cost maximum flow with these
ordered integer costs implements (4). This is ordinary lexicographic
min-cost flow; sufficiently separated integer weights give the same result.

**Theorem 4.** This optimization retains all p old sources, reaches V(E),
uses exactly R candidate units, and chooses a minimum-weight R-deletion
repair. Its routes have the minimum link count among all such repairs that
retain those old source identities. Delete precisely the isolated points
corresponding to USED candidate sinks; the result is a physical repair with
these values and costs.

**Proof.** Theorem2 guarantees a value-V(E) flow retaining every marked
source, so the first tie-break retains all p. Every such flow using q new
candidate units has V(E)<=p+q, hence q>=R: alternatively delete its q paths
ending at new sinks to leave a baseline feasible flow of value at most p.
A basis has R members, and Theorem2 gives a value-V(E) flow on that pool
retaining the marked sources, so the minimum is exactly R. The same argument
for every basis identifies minimum total deletion weight with the basis
optimum. The final cost then gives the claimed minimum links.

Every used candidate is an actual one-capacity original sink. An unused
candidate need not be physically created and is therefore not deleted.
Removing unused candidate sinks preserves all paths of the chosen flow;
Lemma1 identifies the remaining network with the physical result. If a beta
used an interval before its private whole-beta sink, normalize it to use
the latter. Freeing a candidate would contradict the optimal R lower bound;
freeing an old interval preserves (5). This normalization retains links
and starting sources, giving the actual stem/fork certificate. QED.

Unmarked old alpha sources may become paid as part of the gain; there is no
assumption that only newly introduced interface sources receive it. The
new objects here are resources, not new alpha owners. This distinguishes
this operation from restoring actual matching ports.

## 5. Optimal free-location repair of the adjacent maximum family

For the known configuration(W,k), let X be ALL occupied-isolated selections,
with no restriction to the designated seams. The old horizontal model has
k sources, maximum payment zero and empty own support for every alpha.
Theorem2 gives a lower bound of k deletions for full compensation.

Choose exactly the k upper selections

    x_a=(0,10a+1),   a=0,...,k-1.

They are isolated in the explicit maximum pattern. Their deletion opens
the left exterior singleton j_a=(0,10a+1,10a+1) for module a; for a>=1
this is the shared seam unit, and for a=0 it is the boundary singleton.
Pay A_a from j_a through the one actual outward link

    (1,10a+5) -> (1,10a+4).

Different sources, mixed owners, links and original units are distinct.
Thus k deletions and k links suffice, and freezing remains unchanged.
No smaller deletion set from X can attain full value, by the unit-gain
bound. No such repair can use fewer than k links: P fixes both neighbors
of every middle column of an alpha body, so its own support is empty even
after ALL isolated candidates are deleted; every payment must take a first
link. Hence the exact free-location optimum, among all isolated deletions,
is k deleted selections and k links for every W,k in this family.

The repaired selection has size t-k and numerical slack 3k. This does not
turn the original maximum into a full-paying configuration without loss;
the k deleted selections are explicitly included in the budget. It gives
the constructive optimum for this operation class, while the preceding
path note quantifies the cost of prescribing a worse repair location.

## 6. Validation and remaining geometric question

Reproduce with

    python3 develop/check_isolated_repair_selection.py \
      --output output/isolated-selection-repair-validation.json

The verifier compares simultaneous physical deletion against resource-only
restriction of a single compiled network, including exact old identities,
all terminal types and links, supports and freezing. Abstract controls include
mixed gates and beta-body forks. It checks every small candidate subset,
rank submodularity and exact deletion budgets, weighted greedy against every
basis, and the joint lexicographic flow against independent primitive
source-protected optimizations. Enumeration corroborates the general proofs.

The new theorem provides an exact repair criterion WHEN a sufficient family
of isolated candidates exists. It does not prove V(E)=k for arbitrary frozen
mixed-direction configurations. Establishing that geometric coverage, or
charging the residual deficit when the candidate rank is insufficient,
remains necessary before a universal5/6 improvement. Neither deleting an
occupied-adjacent selected pair nor treating a capacity-two tile as two
independent usable gates is covered. The submitted manuscript is unchanged.

The [Lean source](../formal/SubQuorum/IsolatedSelectionRepair.lean) verifies
the arbitrary-finite-list augmentation and minimum-count core under explicit
monotonicity, diminishing-returns and unit-increment hypotheses, together
with candidate distinctness, endpoint-neighborhood preservation and the local
TT exclusion. It does not formalize the flow-to-rank submodularity adapter,
weighted basis exchange or the full geometric/flow equivalence. Those have
written proofs and independent computational checks.

The [computational receipt](../output/isolated-selection-repair-validation.json)
records 111 candidate-network models, 1,102 resource subsets, 24,642 rank
submodularity comparisons, 740 zero-marginal stopping certificates, 380
exact deletion-budget entries and 333 weighted
greedy/joint-flow profiles. There are 358 independent source-protected
primitive value checks and 126 independent lexicographic repair optimum
checks. Twenty frozen physical boards yield 578 commuting deletion variants,
including 192 mixed-direction variants and 320 checks of actual matching
crossings. Twelve larger all-candidate adjacent controls, through W=64/k=8,
verify the exact k-deletion/k-link optimum. The nonisolated TT identity
counterexample is checked separately. The
[formal receipt](../output/isolated-selection-repair-formal-validation.json)
and [compiler log](../output/isolated-selection-repair-lean-validation.txt)
record 14 scoped local Lean 4.33.0 declaration audits, without warnings,
unproved placeholders, native evaluation or new axioms.
