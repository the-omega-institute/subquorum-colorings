# Horizontal-BP mixed forests and the first vertical-gate frontier

25 October 2026. Wenlin Zhang and Haobo Ma. Isolated research branch.

The [frozen serial-fork escape](FROZEN_SERIAL_FORK_ESCAPE.md) leaves distinct
exterior mixed owners, not additional sinks. Those owners have a useful
stronger property: their BP actual mates are horizontal. We prove that all
alpha-reachable mixed owners of this type form single-entry directed trees.
Different serial escapes therefore cannot merge while they remain in this
class. They can merge at the first vertically matched BP, or compete for an
original interval or whole beta. These are retained explicitly.

This extends the [short horizontal-chain reduction](SHORT_MIXED_CHAINS_AND_CORRIDOR_HOLE_BUDGET.md)
to mixed owners with bent, arbitrarily long bodies and possibly branching
outputs. It also gives an exact weighted compression in the complete original
BP-aware fork network. The graph consequences and flow substitution are
elementary; the content is the physical single-entrance criterion and its
application without inventing resources or dropping actual costs. No general
compensation theorem or improvement of the universal 5/6 bound is asserted.

## 1. Original physical class and the unique entrance

Use the feasible original selected set T, actual matching M, aligned two-row
bands, original PP/M strands and horizontal TP--BP links of the previous
notes. Keep every original whole-owner support W, unit interval identity,
beta's two separate BP entries and one private whole-beta sink. For the
structural results of Sections 1--3, complete freezing is NOT required.
Thus they apply in particular to the frozen boards of the serial theorem.
No physical deletion or rematching is performed.

Let H be ALL original mixed owners whose BP endpoint is actually matched
horizontally. This includes one-edge short owners and long bent mixed owners.
Remove self-links from the owner-routing graph; they close a neutral cycle
and are not needed for maximum payment at minimum link cost.

**Lemma 1 (unique original external entrance).** Every h in H has at most
one incoming nonself physical TP--BP link, counting the actual TP identity,
not merely its owner.

**Proof.** Let x be its BP and v its horizontal actual mate. The only possible
horizontal predecessors are v and x's other horizontal neighbor. If v is TP,
its actual M edge already joins it to x in the SAME original owner h, so its
link to x is self. If v is not TP, it is no candidate predecessor. Only the
other neighbor remains as a possible nonself incoming TP. QED.

This uses actual horizontal matching at BP. A vertically matched BP can have
two different horizontal TP predecessors; it is exactly the frontier at which
this conclusion stops. A long mixed owner's TP may be vertical even though
its BP is horizontal. No short-strand assumption has been inserted.

## 2. Reachable owners form source-separated trees

Reachability here means a directed path from an original alpha in the
original routing graph; beta bodies terminate such paths. Let H_live be the
alpha-reachable owners in H. Keep every H-to-H physical nonself link.

**Theorem 2 (single-entry forest).** The induced H_live graph is a disjoint
union of finite rooted directed trees oriented away from their roots.
Each root has exactly one incoming original link from outside H, and all
other vertices have their one incoming link from their tree parent. There
are no other incoming links into any vertex of a tree. Each vertex has at
most two outgoing nonself links overall, since its TP has two horizontal
neighbors. Different trees can share final resources or non-H frontier
owners, but cannot share any H owner or internal actual link.

**Proof.** By Lemma 1 every H owner has total nonself indegree at most one.
A directed H cycle already uses the unique incoming edge at every cycle
vertex, so no path from outside that cycle can first enter it. It contains
no alpha. No alpha-rooted path can enter such a cycle, nor can it reach an
H descendant of that cycle: following unique predecessors backwards would
lead to the same closed cycle. In particular a cycle is absent from H_live.

Starting at a live H vertex, repeatedly follow its unique predecessor while
that predecessor is in H. Each predecessor is live. Finiteness and absence
of cycles force termination at a root with its incoming predecessor outside
H. There is an incoming edge there because the root is alpha-reachable and
is not an alpha. The unique-parent chain gives one root and one internal
root-to-vertex path. Two such trees cannot merge: trace the unique parents
backwards from a hypothetical common vertex. The resulting roots would be
the same. These arguments exhaust all incoming edges, proving the claim. QED.

An H component with no external entrance, including a directed cycle and its
H descendants, is alpha-unreachable and carries no paying path. Its flow
vertices may be pruned, preserving ALL original interval sinks and the
original physical board. We do not claim physically frozen H cycles exist;
unreachable-cycle controls below are abstract.

**Corollary 3 (the serial escapes do not merge inside H).** For the
owner-disjoint same-phase serial skeletons of the previous note, each forced
exterior mixed escape Y_i is a different ROOT of an H_live tree. These trees
are disjoint and lie outside the union of all the skeleton owners.

**Proof.** Its BP has horizontal actual mate by the escape lemma. Its unique
incoming link is the forced t_2 -> BP(Y_i). That predecessor belongs to X_2,
whose BP is vertical, so X_2 is outside H. Distinct escape BP/owners were
already proved. Within any skeleton, X_j for j>=2 has vertical BP and cannot
belong to H. If X_1 has horizontal BP, its unique external predecessor is
its own alpha tip a_1, so it roots a different H tree. Alphas and betas are
not mixed H owners. Thus none of these exterior trees contains a listed
skeleton owner. QED.

The common phase is inherited by all TP outputs on a route, because a
TP--BP link flips checkerboard color and each original mixed strand flips it
again. The forest theorem itself needs no common phase; the serial beta and
resource accounting retains the hypothesis of the previous theorem.

## 3. Exact compression in the complete original fork network

For each live H tree F with root r, let d(h) be the number of INTERNAL actual
terminal links on its unique root-to-h path. The original incoming link
from outside F to r is NOT included in d. For each output keep its best
witness route:

- Original interval j supported at any h in F: a support output with toll
  min{d(h): j in W(h)}.
- Original boundary link from TP(h) to a BP q outside H: an output to that
  SAME actual mixed entry or beta BP entry, with toll min{d(h)+1} over its
  possible witnesses. Keep different actual beta entries distinct.

Replace F's mixed gates by one capacity-one root gate. Keep its original
external incoming link at cost one. Give each output its above toll and
its original internal-path witness. Keep every non-H owner, its capacities,
all original unit sinks and all other supports/links. H-unreachable vertices
can be omitted. Do not merge resource IDs, beta entries or vertical gates.

**Theorem 4 (exact value and actual-link cost).** This compressed full fork
network has the same maximum payment V and minimum actual-link cost c at V
as the complete original network. An optimum lifts to distinct original
terminal links with exactly the compressed cost. Both checkerboard phases
and arbitrary external mixed cycles are allowed in this theorem.

**Proof, original to compressed.** Use the established integral stem/fork
normal form and discard nonpaying cycles. Any paying path first entering F
must use its root's unique incoming edge, and then its root gate. At most
one unit can enter F. Inside it the path follows the unique internal route
to its supported interval or first boundary link. No path can reenter F
without revisiting the root gate; such a paying path is simple. Replace
its F segment by the corresponding output. The minimum witness toll is no
larger than that segment's link count. No external gate or original sink
changes, so the compressed flow has the same value and no greater cost.

**Proof, compressed to original.** In an integral flow without circulation,
each root gate carries at most one unit. Expand that unit's chosen output
along its recorded original root-to-witness path, followed by its boundary
link when present. Two selected outputs from different trees cannot share
H vertices or internal links. Inside a tree only one output is selected.
There are no external entrances into descendants. Original capacities
outside the trees are unchanged, including both BP entry gates, the single
whole-beta sink and all shared original intervals. Therefore the expansion
is a feasible original flow with the same value and exactly the stated cost.
Apply the existing beta-private-sink normalization and physical packing lift.
The two directions imply equality of V and of c at V. QED.

A single uniform toll for all tree outputs is generally wrong: a root's
support has internal cost zero, whereas a child's support has internal cost
one. With only the root unit available the total entry-plus-support cost
is one; with only the child's unit it is two. The controlled example below
checks both availability sets. An H tree is a selector with output-dependent
costs, not an extra resource or a collection of simultaneous free routes.

## 4. A stronger unchanged-C serial certificate

Return to q same-phase owner-disjoint frozen serial skeletons, with N total
alpha sources. Fix ALL C and the previous beta baseline: t_1->b_1 and
t_i->b_(i-1) for i>=3 in each skeleton. These N-q beta payments use no
interval. Exactly one source, A_2--X_2, remains per skeleton. Baseline links
including C total 2N-q. Let B_base be those original whole-beta identities.

Consider the following DECLARED certificate class. Keep the baseline fixed.
A remaining source may use only its forced escape: its single available BB
unit, its forced beta, or its forced exterior H root followed by a path
inside that root's tree. From a tree it may end at any supported available
original interval, or at any original beta not in B_base accessible by an
outgoing actual link. These betas may include the unused Z_n of a skeleton.
Do not pass into a vertical-BP mixed frontier gate. Marked ports give no
resource in this class. Other original supports or routes are retained in
the full board but deliberately not used by this certificate.

Let R_i be the resulting set of resource IDs for residual source i, tagging
intervals and whole betas as different types. For a beta escape R_i is its
one whole-beta unit; for an available BB escape it is the one original J;
for a marked port it is empty. For an H-tree escape it is the union described
above. Each incidence carries its shortest ACTUAL link count starting at
t_2, including the entry to the root and any final beta link. Intervals and
betas shared by different choices are the SAME vertices in this graph.

Let nu be the maximum bipartite matching size between the q residual sources
and these original resource IDs, and tau the minimum total incidence weight
among matchings of size nu.

**Theorem 5 (forest-extended joint compensation).** There is an original
packing retaining every C and every baseline beta link with

    payment >= N-q+nu,       selected links = 2N-q+tau,
    Delta <= q-nu.

In the declared certificate class, N-q+nu is the EXACT maximum payment and
2N-q+tau its minimum selected-link count. For the full board these are a
payment lower bound and an explicit certificate's cost, not necessarily the
full optimum or its minimum cost.

**Proof.** Choose a matching and the shortest witness route for each selected
incidence. Corollary 3 makes all selected H paths disjoint from one another
and from all skeleton owners. Each residual source selects only one path.
The matching prevents reuse of a final interval or whole beta. B_base is
excluded, so no baseline beta is spent again. Direct beta and BB escapes
are included in the SAME matching and therefore cannot collide with tree
outputs either. The selected links form a legal physical terminal matching.
Add its nu payments to the N-q baseline, with the stated cost.

Conversely, in this certificate class every additional payment uses one
residual source and one resource of its R_i, and no resource can be used
twice. Its payments project to a bipartite matching; each route's cost is
at least the corresponding incidence weight. Thus no certificate in the
class beats nu, or beats tau at nu. This proves exactness in that class. QED.

In particular Hall's criterion on these R_i proves full compensation of the
skeleton sources without changing C. If b,r are the previous direct-beta
and distinct forced-BB counts, then nu>=b+r: keep those old choices and use
no H-tree output. Hence this bound is never weaker than the previous one,
and improves it whenever extra tree outputs admit a larger joint matching.
Reachability alone is still insufficient: |R_i|>0 for every i does not imply
Hall's condition. This is the point at which shared resource IDs remain
essential, even though the H interiors are source-separated.

## 5. A real first-frontier obstruction and verification scope

The EARLIER [active short-tail merger](ACTIVE_SHORT_TAIL_MERGER_AND_SEALED_ESCAPE.md)
already supplies an actual completely frozen 14x18 board with 62 endpoints
and 25 selected sites. Its two alpha-entered horizontal-BP roots are
BP(5,7)--TP(5,8) and TP(5,10)--BP(5,11). Their outgoing links both enter the
SAME vertically matched BP(5,9), whose mixed owner ends at TP(10,9).
Retaining only those two alphas, two H roots, the receiving mixed owner and
the original units (band5,col10),(band5,col12), each source individually
reaches both units but their joint value is one, at minimum two links.
Our independent terminal enumeration rechecks this exact restricted model.

This is not a new frozen fixture, nor a full-board deficit: the earlier note
shows both alpha sources pay through different original bypass intervals
in the complete pool. It establishes the necessity of retaining the first
vertical frontier gate after H compression. A separate abstract control
shows two trees sharing one original interval also pay only one. An abstract
branching tree with root/child supports tests output-dependent tolls; a
sealed abstract H cycle is correctly pruned as alpha-unreachable.

The solver-free checker verifies 22 compatible saved frozen fixtures,
157 H-owner occurrences including four long bent H owners, 65 reachable
H owners and eight multi-owner trees. No branching H owner was found in
these physical fixtures; branching controls are abstract. It compares
full-network payment AND minimum actual-link cost on 88 physical original-
availability controls and 220 abstract models, including 26 abstract
branching-owner occurrences and 124 models with pruned H vertices. Small
independent terminal enumeration covers 39 randomized models plus the real
restricted frontier control, totaling 1,587 terminal matchings.

One hundred decorated ABSTRACT serial interfaces check the resource-matching
certificate, exact fixed-baseline value/cost and the lower bound in the full
fixed-C model; 54 strictly improve the previous direct-escape bound.
Seven have further gains through the excluded vertical frontier,
confirming that the restricted matching value need not be the full optimum.
They are not claimed frozen serial embeddings. General unbounded claims are
proved above; enumeration only checks the adapters and controls.

Eight local Lean statements verify arbitrary-length unique-root/disjointness,
closed-cycle entry exclusion from supplied predecessor hypotheses, the local
one-row neighbor equation, depth monotonicity, and serial counting. Four are
axiom-free; the others use only propext and Quot.sound. Full original geometry,
finite forest extraction, weighted flow substitution and physical packing
adapter remain written/Python, not an end-to-end Lean theorem.

    PYTHONDONTWRITEBYTECODE=1 python3 develop/check_horizontal_bp_forests.py \
      --output output/horizontal-bp-forests-validation.json
    cd formal
    lean SubQuorum/HorizontalBPForests.lean

The next geometric target is now the VERTICAL-BP frontier, with global
original interval/beta identities: which joint cuts can actually remain
unsatisfied after these single-entry regions and all bypasses are retained?
No numerical improvement of 5/6 follows yet. The 11 October submitted
manuscript, public main/PR3 and shared CI remain unchanged. No email was read,
drafted or sent in this research turn, and no new Oracle review was requested.
