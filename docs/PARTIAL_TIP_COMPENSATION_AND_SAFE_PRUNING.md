# Partial terminal certificates: component parity and safe mixed pruning

25 October 2026. Wenlin Zhang and Haobo Ma. Research branch only.

The [two-slot certificate](FROZEN_TIP_SLOT_OBSTRUCTION.md) need not cover
every TP terminal to prove full compensation. An arbitrary partial injective
assignment gives the general bound

    unpaid original alphas <= sum_C floor(h_C/2),             (1)

where C runs over genuinely separate final-alpha/assigned-interval components
and h_C counts their unassigned free TP ends. In particular, one missing end
per such component costs NO alpha payment. Shared original interval identities
must be merged before taking the floors.

There is also a certificate requiring only maximum bipartite tip matching
on the original system. If h_D is its terminal deficiency in each original
owner/resource interaction component D, then

    ordinary compensation deficit <= sum_D min(a_D,floor(h_D/2)).   (2)

Thus every interaction component with h_D<=1 is fully compensated, although
arbitrarily many tips can remain uncovered globally. The bound is sharp on
abstract systems even when each original interval has at most two owners.

Separately, mixed owners outside every alpha-to-resource route can be safely
deleted from the compensation graph. This preserves optimum payment and link
cost, but does not make a complete all-TP assignment necessary: the previous
fully frozen physical counterexample retains one impossible alpha end after
this strongest reachability/productivity deletion. Its remaining alpha is
still paid from its other end, exactly as (2) certifies.

These are statements about the declared whole-support compensation model.
They do not prove geometric saturation for every frozen grid, classify all
mixed-direction configurations, or improve the universal 5/6 grid bound.

## 1. Fixed identities and partial assignment

Use the finite original alpha/beta/mixed strand system of
[the normal form](WHOLE_SUPPORT_FORK_NORMAL_FORM.md). Owners have disjoint
TP/BP terminal pairs, actual declared TP--BP links L, available original
interval identities I, and fixed whole-support sets W(x) subset I.
Only alpha and mixed owners have TP terminals. A beta has two different BP
tips and one whole-beta payment unit. Any immutable earlier links must be
contracted before fixing this system.

A partial certificate assigns SOME TP terminals injectively to the disjoint
target set

    {BP terminal identities} disjoint-union (I x {0,1}).

A BP assignment must be a declared link. An interval-slot assignment
v->(j,k) requires j in W(owner(v)). An unassigned TP is a **hole**. Two
owners naming j still share the same two slots; supports are witnesses and
do not duplicate original resources. Assignments are only counting objects;
they do not assert a physical free-tip route to every interval witness.

Select the BP-assigned links, giving a terminal matching C. After the
cancellation, every free TP is either assigned an interval slot or is a hole.
In particular every final alpha path has exactly two such free TP ends.
Free TP ends of final mixed paths are not alpha demands and may be ignored.

Form the bipartite graph Q whose left vertices are final alpha paths and
whose right vertices are ORIGINAL intervals actually assigned to their free
ends. Two assigned slots of the same interval give one right vertex. A final
alpha with no assigned end is an isolated left vertex of Q. For each connected
component C of Q let h_C count holes among its final alpha ends. Isolated
intervals having no assigned alpha end can be omitted.

## 2. General partial-certificate compensation theorem

**Theorem 1.** From any partial certificate, construct ordinary whole-support
compensation leaving at most B=sum_C floor(h_C/2) original alpha demands
unpaid, with at most the number of its BP-assigned links. The original BP,
whole-beta and interval capacities are respected simultaneously.

**Proof.** For any set K of final alphas in one component C, let h(K) be its
number of hole ends and N(K) the distinct original intervals assigned to its
other ends. There are exactly 2|K|-h(K) assigned slot identities. Injection
and the two-slot allowance give

    2|K|-h(K) <= 2|N(K)|,
    |K|-|N(K)| <= floor(h(K)/2) <= floor(h_C/2).             (3)

Write d_C=floor(h_C/2). Add d_C auxiliary dummy interval vertices, each
adjacent to every alpha of this component. For every nonempty K, (3) is
exactly Hall's condition in this enlarged graph. Hall therefore matches
all its final alphas. Discard dummy assignments; at most d_C alphas remain
unpaid. All other assignments use actual different original intervals,
each witnessed by one of the paid path's free TP owners. Apply this to
every Q component. They have different right-resource identities, so their
real allocations combine without conflict.

Write a,b for original alpha and beta counts and a_C,b_C for final counts
after all BP-assigned links. If r final alpha paths receive real intervals,
the signed endpoint conservation and payment ledger give

    a_C-b_C=a-b,
    p=b-b_C+r=a-(a_C-r).                                  (4)

The number a_C-r is at most B by the preceding Hall construction. Every
whole beta is consumed once in b-b_C, and every real interval is assigned
once by the combined matching. Thus no slot is itself counted as an
additional payment.

The normal-form subset argument gives ordinary stems without beta-body
forks: every interval-paid path has a witness on a free TP's alpha/mixed
owner, so the non-beta-root normalization applies. Unpaid components
normalize into beta stems covering their smaller alpha/beta class. The
normalized links form a subset of C, preserving p. This proves both the
ordinary-compensation and link-count statements. QED.

No maximum-matching hypothesis on the partial certificate is needed.
The dummies prove a lower bound and are then discarded; they are never
physical resources or additions to the original ledger.

**Corollary 2 (one hole per final component).** If every Q component has at
most one hole, all original alpha demands are compensated. More generally,

    2B = sum_C h_C - #{C : h_C is odd}.                    (5)

This is the exact parity benefit of summing component floors. Mixing
unrelated components before rounding can lose half of their odd credits.
Holes belonging to final mixed paths do not enter (1) at all.

## 3. A criterion from the original terminal matching alone

Build an undirected interaction graph with original owner vertices and
original interval vertices. Join owners whenever a declared TP--BP link
connects them. Join owner x to every j in W(x). Including beta-body supports
is safe, even though the terminal assignment itself never assigns a beta
TP. Each connected component D has a_D original alpha owners. A resource
appears once as one vertex, irrespective of its number of owner witnesses.

The two-slot bipartite tip graph separates across these components. Let h_D
be the number of unmatched TP terminals in a maximum matching of its
component. Maximum global matching is equivalent to taking independent
maximum matchings on these components.

**Theorem 3 (original component criterion).** Ordinary compensation has
deficit at most the right side of (2). In particular h_D<=1 for every
component containing alphas implies complete ordinary compensation.

**Proof.** Take the component's maximum tip matching as a partial
certificate. Every selected link, original strand, assigned interval and
Q component in Theorem1 remains inside D. If their hole counts are g_i,
then sum_i g_i<=h_D: some original holes can instead end up on final mixed
paths and need not be charged. Consequently

    sum_i floor(g_i/2) <= floor((sum_i g_i)/2) <= floor(h_D/2).

Unpaid demands in D are also at most a_D. Combine the actual certified
payments independently across D, keeping every resource and beta identity
inside its unique component. QED.

This criterion is sufficient, not necessary. It is a counting theorem
derived from a partial certificate, not an assertion that frozen geometry
always has h_D<=1. A genuine compensation counterexample must have at least
two terminal holes in some alpha-containing interaction component; one-hole
obstructions of the previous note cannot establish a payment deficit.

**Sharpness and the resource-identity hazard.** Take two alphas and one
original interval j, with W(A0)=W(A1)={j}, and no BP terminals or links.
Exactly two of four TP ends can use j's two slots. Thus h=2, maximum payment
is1, and the deficit1=floor(h/2) is sharp. The resource has just two owner
users. Taking q separate copies gives deficit q and2q terminal holes.

If j is mistakenly renamed j_left and j_right in the two owners' local
accounts, both local tip graphs have h=0 and would falsely certify payment2.
The correct original interaction graph connects the two alphas through the
ONE j. This is an explicit counterexample to unmerged local rounding and
resource duplication, not a frozen-grid counterexample.

The final-alpha refinement can also strictly improve (2). As an abstract
example use one alpha A, one beta B and two mixed owners M,N, no intervals,
and links from A's first TP to B's first BP, from A's second TP to M's BP,
from M's TP to its own BP, and from N's TP to M's BP. Maximum tip matching
leaves two holes and the original interaction graph is connected, so (2)
only bounds the deficit by1. Select the two A links as its BP assignments.
A,B,M become a final mixed path, while N is another mixed path. There are
no final alpha paths: h_C totals zero and Theorem1 certifies full payment1.
The two unmatched mixed TP ends are not two unpaid alpha demands.

## 4. Safe deletion of mixed branches, with unchanged original resources

Use the directed owner graph whose arcs are declared non-self TP--BP links.
Let R be the owners forward-reachable from an original alpha. Let P be the
owners that can reach either a beta or an alpha/mixed owner x with
W(x) nonempty. A beta is productive because of its private whole-beta unit;
beta-body interval witnesses do not need an extra productivity hypothesis.
Keep all original alphas and betas, and keep a mixed owner only if it lies
in R intersection P. Delete links incident to deleted mixed owners and
discard their support incidences, retaining the ENTIRE original interval
identity set I. All other supports remain unchanged.

**Theorem 4 (safe graph pruning).** This deletion preserves maximum
compensation and minimum link cost, both for ordinary stems and for full
whole-support stem/fork compensation. It also preserves feasible canonical
packings with specified paid alpha identities or specified used interval
identities. The same statement applies after fixing a source subset and
deleting any declared interval resources, with liveness recomputed there.

**Proof.** Every mixed owner used by an ordinary stem lies on that stem's
alpha-to-interval-witness or alpha-to-beta route. It is therefore reachable
from an alpha and can reach a declared productive target, so it belongs to
R intersection P. The same holds for a mixed owner on either beta-fork arm,
which ends at a beta. Thus every primitive in EVERY original valid packing
already avoids all deleted owners, not just one optimal packing. It survives
unchanged with exactly the same source identities, beta and interval units,
payment and links. Conversely any reduced packing is a valid original
packing, since the reduced links/supports are subsets with original identities.
The attainable packing values and costs, including the stated identity
constraints, are therefore equal. Apply the existing normalization equivalence
for the unconstrained cancellation optimum. QED.

This is a directed-path pruning principle applied to the exact strand model,
not a new general network-flow theorem. Crucially it is **graph deletion**:
the grid's T/M sets and frozen endpoints remain physically present. One
must not erase the corresponding P points, recompute endpoint-free gaps or
manufacture newly available intervals. It does not justify retaining arbitrary
old nonnormalized cancellation links as additional mandatory constraints;
immutable links must first be contracted as in the underlying model.

## 5. A physical obstruction remains after all safe pruning

Take the completely frozen PP-sealed10x16 board from the previous note,
with alpha A ending at(3,6),(6,6), beta B ending at(3,5),(4,5), and mixed
R ending at(3,7),(3,8). The three other mixed owners are safely removed:
D is a dead self-loop branch, the lower-left mixed self-loop is unproductive,
and the remaining mixed owner has an interval witness but is unreachable
from any alpha. Only R is both reachable and productive.

The lower alpha tip(6,6) now has no BP target and still has W(A)=empty.
Graph pruning did not erase any physical endpoints or add any witnesses.
Thus the complete all-TP certificate still fails. The other alpha tip
can be assigned to B's BP and R's TP to its own BP or one of its interval
slots. Exactly one of the three remaining TP tips is unmatched. All owners
belong to one alpha-containing interaction component, so Theorem3 certifies
full payment with h_D=1. Directly, the one A-to-B link pays the alpha.

For q vertically separated copies, every alpha-containing component has
one hole before AND after pruning. The number of uncovered tips is q, while
(2) gives deficit zero. In contrast, the unseparated global bound floor(q/2)
would grow with q. The actual payment is q at minimum q links by the previous
all-parameter geometry proof. Arbitrary even blank right padding preserves
the PP seals and this entire argument.

This settles the proposed safe-deletion question for the declared graph,
and demonstrates why that deletion alone cannot restore the old necessary
all-TP assertion. The partial-certificate theorem handles the remaining
one-ended source directly.

## 6. Verification and formal scope

```sh
python3 develop/check_partial_tip_compensation.py \
  --output output/partial-tip-compensation-validation.json
cd formal
lean SubQuorum/PartialTipCompensation.lean
```

The deterministic controls cover1269 systems, including1200 random systems,
20 sharp two-owner-resource examples, one strict final-alpha refinement and
48 actual frozen copy/padding boards. They check4461 lifted partial
certificates; additional partial assignments are subsets of a particular
maximum matching, not an exhaustive enumeration of all matchings. There are
45 strict improvements from component rounding, one strict improvement from
discarding final mixed holes,147 non-full tip covers certifying full payment
with nonempty original alpha demands, and347 positive cases attaining the
original component deficit bound. The non-full-cover count is160 if the13
zero-alpha controls are included.

Ordinary and full-fork values AND costs agree before/after pruning in2538
comparisons;342 systems have an actual owner deletion. Another2012 comparisons
fix different original alpha subsets and delete interval subsets before
recomputing liveness (1290 comparisons have a nonempty source subset).
The explicit resource-renaming countercontrol verifies
that splitting a shared identity would indeed overstate compensation.
No exhaustive claim about all random systems, all terminal matchings or all
frozen geometries follows from these controls.

Local Lean4.33.0 passes the generic distinct-slot cardinality theorem for
arbitrary resource types/lists, its two-end/hole inequality, component parity
identity and rounding, one-hole-per-component arithmetic, merging odd hole
counts, and the exact cancellation/payment ledger. The cardinality proof uses
an actual injection into the list of two labelled slots per original resource,
rather than assuming the factor-two bound. Standard dependencies are propext,
Quot.sound and Classical.choice; no custom axioms, sorry or native_decide.
The general Hall existence/normalization, graph-pruning equivalence and
physical adapter are written proofs and independently checked computations,
not claimed as fully formalized Lean theorems.

The submitted11 October manuscript and public main are preserved. This round
does not read or send mail. A single broker review attempt, task
`12627397-d50d-4e85-9e24-380f2bcc1ada`, ended with
`model_unavailable@selecting_model` and no mathematical answer. This is no
independent review or acceptance; the terminal failure is archived and was not
retried. The next
geometric target is a bound on original interaction defects or on the final
alpha hole components that can actually arise from frozen mixed-direction
configurations. Components with two or more holes require joint capacity
analysis; resource identities and any earlier reservations remain shared once.
