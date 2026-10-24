# Exact fork replacement deficits and exclusion of wide arm gaps

25 October 2026. Haobo Ma and Wenlin Zhang. Research branch only.

The [completely frozen beta fork](FROZEN_BETA_SUPPORT_FORK_AND_RESERVED_RESOURCE_GAIN.md)
settles physical existence, but has no unrestricted value advantage. We now
quantify its replacement problem and restrict where a genuinely useful fork
can occur. The main structural result is this: in a maximum-payment,
minimum-link normalized packing, every original interval visible before a
fork's beta must be blocked by a different outside certificate. Under the
physical two-owner hypothesis, these units have different unique outside
owners. In particular a pre-beta arm gap containing two available units
excludes that fork from every such optimum.

This is an optimization exclusion, not a claim that the frozen geometry
cannot contain the fork. A large gap on the **beta body alone** is not an
arm gap and is not excluded. The distinction is essential for the existing
physical fixture.

The finite matching ingredients below are standard. The contribution is
their specialization to owner-disjoint cancellation certificates, original
resource identities and link costs. They do not prove a universal grid bound.
The submitted11 October manuscript is unchanged.

## 1. Fixed routes, fixed reservations, exact value

Use the whole-owner-support system and normal form of
[the stem/fork theorem](WHOLE_SUPPORT_FORK_NORMAL_FORM.md). Work after any
immutable C0 has been contracted; original interval identities are retained,
and all link counts are additional to C0. Let H be a compatible pack of h
forks. Each fork has two different alpha roots, two owner-disjoint arms
through mixed owners, and a common terminal beta, entered at its different
BP tips. All fork owner sets are disjoint. Its chosen interval J_f belongs
to the beta's support; the J_f are different.

Keep any outside packing fixed and let R be its used interval set, together
with any additional explicitly forbidden intervals. Its owners are disjoint
from H, its used units avoid all J_f, and it cannot be modified. Restrict
new ordinary certificates to subsets of each fork's original links and
owners; no cross-fork link or route outside H is introduced. For f define

    S_f = owners on its two arms before the beta,
    A_f = union_{x in S_f} W(x),
    N_R(f) = A_f \ R.

All old fork intervals are released simultaneously before doing this
replacement optimization. An interval J_g may be in N_R(f), even for g≠f;
its original identity must still be spent at most once. The beta-body
support of f is not itself an ordinary access out of a beta sink.

Let mu be the maximum matching number from forks f to units in N_R(f), and
let v_arm be the maximum number of the2h fork sources paid by ordinary
stems in this restricted route system.

**Theorem1 (exact quantitative replacement).**

    v_arm = h+mu = 2h-delta,
    delta = h-mu = max_{Q subset H} (|Q|-|N_R(Q)|),         (1)

where N_R(Q) is the union of N_R(f), and Q may be empty.

**Proof.** In an arbitrary ordinary packing each fork pays0,1 or2 of its
original sources. Let D be the forks paying2. There is only one beta per
fork and an ordinary interval stem stops before that beta, so every fork
in D uses at least one interval from N_R(f). Choose one of its interval
payments. Global interval injectivity makes these choices a matching;
therefore |D|≤mu. The total payments are at most h+|D|≤h+mu.

Conversely take a matching of size mu. For a matched fork f, stop one arm
at a witness for its matched interval and use the other arm as a beta stem.
For each unmatched fork use either complete arm as a single beta stem.
All owners and links are subsets of disjoint original forks, all beta units
are different, and the matched intervals are different and avoid R. This
pays h+mu. The finite matching deficiency formula gives the final equality:
for any Q at most |N_R(Q)| of its vertices can be matched, whereas a maximum
matching and alternating reachability from its unmatched left vertices
produce a Q attaining h-mu. No resource is counted separately in two forks. ∎

Thus the earlier all-replacement Hall criterion is delta=0. The upper-bound
argument tolerates two interval payments in one fork; it does not assume a
beta is used in every ordinary optimum.

## 2. Two-owner supports: an exact deficient-tree count

Assume every available original unit belongs to at most two current open
owners, as supplied by endpoint-free gaps and preserved by C0 contraction.
Then each right vertex of the fork-to-unit graph has degree at most2.
Several supporting owners in one S_f still count as one neighboring fork.
Discard resources with no neighbor. Represent a unit with two different
neighboring forks as an edge of a multigraph on H; a unit with one neighbor
is a private resource at that fork. Parallel edges remain different units.
Here “private” means private to the **substitute graph**, not necessarily
private to the original physical owner graph.

**Corollary2.** If t is the number of connected components that are trees
with no private resource, including isolated vertices with no resource, then

    mu=h-t,    delta=t,    v_arm=2h-t.                    (2)

**Proof.** In a connected component with n vertices, the two-neighbor edges
contain a spanning tree. If these are exactly its n-1 resources, orient the
tree away from any root and assign each edge to its child. Exactly one fork
is unmatched. Otherwise choose a private resource as root anchor, or an
extra edge outside a spanning tree as anchor at one of its endpoints, and
orient the spanning tree away from that endpoint. This assigns n different
resources to all n vertices. Component upper bounds and disjoint resources
show these constructions are maximum. Sum over components. ∎

This reuses the earlier interval-tree allocation argument on a new left
vertex set: whole fork pairs, rather than original alpha owners. It must
not be confused with the number of original alpha support trees.

## 3. Cost of retaining a beta versus unrestricted ordinary cost

For f let its arm lengths be ell_0,ell_1, measured in terminal links,
each at least1. A witness x on arm a before the beta has prefix cost d(x),
with0≤d(x)<ell_a. For j∈N_R(f) put

    c(f,j) = min [d(x)+ell_(1-a)],                         (3)

over all supporting prefix witnesses x for j. If every fork is required to
retain exactly one whole-beta consumption and take one interval payment,
its exact minimum replacement cost is the minimum-weight saturating
matching with costs c(f,j). It is infeasible exactly when delta>0.

Indeed a matched edge fixes the interval arm and an optimal witness prefix;
the other arm runs to beta. Conversely every replacement of this specified
type chooses such an edge and prefix. Disjoint fork owner sets leave only
the global interval matching constraint. Each c(f,j)≤ell_0+ell_1-1, so a
saturating replacement saves at least h links relative to the fork pack.

This weighted assignment is **not** an exact formula for unrestricted
ordinary minimum link cost. With one fork, put a different interval directly
on each alpha root. Two zero-link interval stems pay both sources. A
beta-retaining replacement pays the same two with one beta link. The exact
costs are0 and1 respectively. In the985 finite controls below,413 full
replacements have unrestricted ordinary cost strictly below the
beta-retaining assignment cost. Equation(1), which concerns value, remains
exact in all of them.

## 4. The whole-network bound and its precise limit

Let P=H union K be any maximum-value normalized packing of a full declared
system D; K consists of its ordinary stems. Put k=payments(K), h=|H|, and
R=U, the actual interval set used by K. With delta computed in Section1,
Theorem1 gives an ordinary packing of the **full** system paying
k+2h-delta. Therefore

    0 <= nu(D)-nu0(D) <= delta(H|K).                      (4)

One may minimize this upper bound over all maximum-value packings. No
geometric assertion that this minimum vanishes is made.

Failure of fixed-arm Hall is not sufficient for unrestricted value gain.
The earlier abstract example has alphas A,C, beta B with body interval J,
and direct arms A->B,C->B. Its fixed-arm graph has no substitute, delta=1.
Add two mixed owners and a three-link ordinary route from C to another
witness for J. The full ordinary and fork values both equal2, although
their minimum link costs are3 and2. The new checker retains this explicit
counterexample. It distinguishes failure of the fixed-route replacement
rule from failure of an unrestricted target inequality.

## 5. Blocking injection and exclusion of capacity-two arm gaps

Now let P=H union K maximize payment and, among those packings, minimize
link count. The ordinary whole-support normal form guarantees this is the
correct lexicographic objective for arbitrary cancellations as well.
For each certificate p, its owners are disjoint from all other certificates,
and it uses at most one original interval. For a fork f retain A_f and its
entire owner set O_f, including its beta.

**Theorem3 (necessary blocking structure).**

(a) Every j∈A_f is used by a certificate outside f. In particular it cannot
be unused or equal f's own J_f.

(b) If every unit has at most two owner witnesses, each j∈A_f has exactly
one outside owner x_j∉O_f supporting it. The map j->x_j is injective.
Moreover these outside owners belong to different certificates of P.

**Proof.** If j is not used outside f, release f's J_f and replace f by one
prefix interval stem to j and the other beta arm. The two sources remain
paid and at least one link is removed; all other certificates stay fixed.
This contradicts minimum link count, proving(a).

For(b), an outside certificate using j must contain a supporting owner
outside O_f. At least one owner in S_f already supports j. The at-most-two
hypothesis therefore leaves exactly one outside owner x_j, and it lies in
the certificate using j. If different j,j' had the same x_j, owner-disjointness
would put both in one outside certificate, which cannot allocate two
intervals. More generally no outside certificate can be used to block two
members of A_f. Thus both maps are injective. ∎

**Corollary4 (wide gaps excluded from optimum).** Consider an original
endpoint-free gap bounded by a P column of an arm owner before its beta.
If it contains at least two currently available original units, f is absent
from every maximum-value minimum-link normalized packing.

**Proof.** Every unit in this gap is supported by that arm owner. The only
possible outside witness is the gap's other bounding open owner, the same
owner for all its units. If the other boundary is a pure cycle, a packet
edge, or another owner inside f, there is no outside witness at all.
Either no outside witness exists, contradicting Theorem3(b), or two
different units have the same outside owner, contradicting injectivity. ∎

The same proof excludes a one-unit arm gap whose available unit has no
outside witness. Consequently any optimum fork has only capacity-one
nonempty arm gaps, each with a different outside owner; each such owner's
certificate must actually use that particular unit. This counts unused
capacity rather than reusing the same external reserve.

The hypothesis concerns available units after the current fixed
reservations. A raw capacity-two gap with one permanently unavailable unit
need not satisfy it. Nor does the corollary exclude capacity-two tiles in
general, feasible forks, or a multiunit gap witnessed only by the fork's
beta. It applies equally to curved or long mixed arms because it uses
original owner incidence, not the direction or length of the arm.

For the frozen16-by14 fixture, A and C have private arm units already.
Thus the selected fork cannot be minimum-cost optimal in the full pool,
independently of enumerating all terminal matchings. The physical fork
remains feasible; the reserved interface removes those substitutes.

## 6. Fork dependencies are acyclic and end at ordinary blocking

In P above, draw a directed edge f->g when J_g∈A_f, allowing a potential
self-loop in the definition.

**Theorem5 (acyclic dependency and blocked sink).** This directed graph has
no directed cycle. If H is nonempty, there is a sink fork f with

    A_f subset U,                                        (5)

where U is the interval set used by the ordinary certificates K.

**Proof.** On a directed cycle, assign each f the old interval J_g of its
successor. Successors are different, so these intervals are different.
Release all cycle fork intervals together; the chosen units avoid every
unchanged certificate. Truncate each chosen interval arm and retain its
other beta arm. This preserves all cycle payments and strictly lowers
link count, a contradiction. A self-loop is the same one-fork replacement.

A finite nonempty acyclic digraph has a sink. By Theorem3(a) every arm unit
of that sink is allocated outside it. An allocation by another fork g
would create an outgoing edge, so all are allocated by K. This proves(5). ∎

Thus an optimal useful fork cannot be justified by a closed cycle of
fork-to-fork interval blocking. Any dependency chain must terminate in an
ordinary interval payment, or in a fork with empty pre-beta support.
Equation(5) is a necessary obstruction, not a supply of new compensation:
U is already spent and cannot be counted a second time.

An abstract all-length family shows this condition can be real. For q≥1,
take forks f_i with alphas A_i,C_i, beta B_i and two direct links into the
beta's different tips. Give B_i its private interval J_i. Put J_(i+1) on
A_i for i<q-1, put a different interval H on A_(q-1), and put H on an
outside isolated alpha D. C_i have no interval support. No other link or
support exists. Every original interval has at most two owners.

All q forks plus D->H pay all2q+1 sources with2q links. In any full payment,
D must take H. Then the last fork has no free arm interval and must use
its own J_(q-1), forcing the preceding fork to use J_(q-2), and so on.
Thus all forks are necessary and full minimum link cost is2q.

Ordinary flow has exactly q eligible arm intervals and q beta sinks, so
its value is at most2q. Assign A_i to J_(i+1), with J_q meaning H, and
C_i to B_i to attain2q with q links, leaving D unpaid. At least q beta
links are needed because there are only q ordinary interval resources.
Hence the exact optima are

    fork-capable: (2q+1,2q),   ordinary: (2q,q).           (6)

The dependency graph is a chain ending at H used by D. This is an
arbitrary-length abstract obstruction, not a frozen-grid realization.
Its ledger |I|+beta-alpha=(q+1)+q-(2q+1)=0 does not contradict the target
inequality. The search for a physical realization remains open.

## 7. A geometric external-token bound for direct original forks

A limited geometric specialization is available using the previously
proved [original-alpha token injection](INTERIOR_SUPPORT_TREE_CAPS_AND_EXTERNAL_WITNESSES.md).
Assume its aligned packet, feasibility and complete-freezing hypotheses.
Take C0 empty and a pack of **direct** forks: each has just two original
alpha owners, its original beta, and two direct entry links. There are no
mixed internal arm owners. These restrictions are necessary for applying
the existing original-alpha injection without extending its scope.

Each original alpha has two distinct tip tokens. An immediate BB port
names its original interval; otherwise the simultaneous injection names
an adjacent beta or mixed strand. Global destination capacities are2 per
unmarked interval,2 per whole beta,1 per mixed strand,1 per boundary-marked
interval. Tokens are witnesses, not allocations.

For any fork subset Q and fixed blocked interval set R, use N_R(Q) from
Section1. Define B_out(Q) to be the token beta destinations outside the
betas of Q, R_tok(Q) the blocked unmarked interval destinations, M(Q) the
mixed destinations and Z(Q) the boundary-marked interval destinations.
All are sets of distinct original identities reached by tokens of these
forks' original alphas.

**Proposition6.**

    2(|Q|-|N_R(Q)|)
       <= 2|B_out(Q)|+2|R_tok(Q)|+|M(Q)|+|Z(Q)|.          (7)

**Proof.** Q has2|Q| original alphas and hence4|Q| tokens. Every token to an
unblocked unmarked interval belongs to an alpha's whole support, hence to
N_R(Q), whose total token capacity is2|N_R(Q)|. The betas internal to Q
have total capacity at most2|Q|. All other destinations have exactly the
upper capacities displayed on the right. Add these capacities and subtract
2|Q|+2|N_R(Q)|. ∎

Thus a positive Hall-defect witness requires some outside beta/mixed/mark
witness or a genuinely blocked original interval. A blocked unit is not new
credit, and an outside beta can already belong to another compensation
certificate. Equation(7) localizes the obstruction; it does not automatically
repair it. It is not asserted for mixed internal arms or arbitrary C0.

## 8. Verification and current research consequence

The independent checker compares985 fixed-arm systems against ordinary
terminal min-cost flow:198 have positive delta, and754 satisfy the
two-owner condition, with203 deficient-tree occurrences. There are760
independent prefix/side/resource cost enumerations. Old fork intervals
are included as possible substitutes, with a cross-fork swap control.

For251 full abstract networks it checks(4), including21 optima containing
forks,20 strict value gaps and the explicit same-value cost-gap example.
Including six independently optimized chain lengths,27 optimal fork
dependency DAGs and42 two-owner external-witness injections are checked.
Twelve additional capacity2..13 controls and a private-arm control exclude
forks from the optimum. Twelve chain lengths verify(6), with full packing
optimization for q≤6 and exact ordinary optimization throughout.

Eight actual frozen stacks verify full arm defect0 versus reserved defectq.
Original-alpha tokens satisfy1506 physical subset inequalities(7), including
502 positive defects after explicit resource blocking. These finite controls
support the general proofs; they do not prove physical strict gain.

Twelve scoped local Lean4.33.0 declarations pass, without warnings or new
axioms, after memory/process checks. They prove the arbitrary finite-list
payment bound, original-unit nonreuse, the external-owner blocking
injection, private-unit/same-external-owner implications, strict prefix
saving, injective old-unit swaps, and the stated scalar deficit, tree,
global and token ledgers. Six of these declarations are axiom-free; the
others use only propext, Classical.choice and Quot.sound. The full matching,
route, minimum-cost DAG and geometric adapters remain written proofs.
No native_decide or incomplete proof is used. No new external review is
claimed.

Reproduce:

    python3 develop/check_fork_replacement_deficiency.py --output output/fork-replacement-deficiency-validation.json
    python3 develop/check_fork_replacement_deficiency_formal.py --lean /path/to/lean-4.33.0 --output output/fork-replacement-deficiency-formal-validation.json

The next geometric target is now a **thin, externally blocked sink fork**:
all its pre-beta nonempty gaps must have exactly one available original
unit, with different outside witnesses whose actual certificates spend
those units. A candidate must still be checked against every full-network
rerouting. This replaces an unrestricted search for arbitrary frozen forks
by a proved necessary structure for forks in an optimum. The general mixed
compensation theorem and universal5/6 improvement remain open.
