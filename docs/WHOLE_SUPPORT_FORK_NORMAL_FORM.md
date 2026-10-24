# Exact whole-support normal form: stems, beta forks, and residual flow

25 October 2026. Haobo Ma and Wenlin Zhang. Research branch only.

Whole-support access differs from free-tip access in a second way beyond
internal PP bypasses. An original beta can itself contain the witness for an
available original interval. Two alpha arms entering its **different BP tips**
then form one final alpha, consuming one beta and using that interval. This
pays two alpha demands with two different resource units: one whole beta and
one interval. Counting the beta twice would be wrong; disallowing its interval
witness without proof can also lose compensation.

We prove an exact normal form and optimization formula for arbitrary declared
owner-support systems. Its primitives are ordinary single-source stems and
this explicitly capacity-controlled beta fork. Every arbitrary cancellation
and whole-support allocation normalizes using a subset of its links, preserving
its compensation and its selected original interval units. Fixing disjoint
forks reduces the remainder to the established ordinary flow problem, with
exact maximum compensation and minimum additional link cost.

The strict examples below are **abstract strand systems**. Our frozen physical
controls contain zero feasible forks, and three specified finite discovery
templates are UNSAT. No frozen-grid fork realization, general geometric
saturation theorem, or improvement of the universal5/6 bound is claimed.
The11 October submitted manuscript is preserved.

**Later25 October result:** the [frozen beta-fork note](FROZEN_BETA_SUPPORT_FORK_AND_RESERVED_RESOURCE_GAIN.md)
constructs a completely frozen physical fork, refuting general fork exclusion.
Its reserved interface has strict gain2vs1; its full pool has no gain. The
zero-fork counts in this note describe the original controls only. The new
note also proves the exact Hall criterion for simultaneous fixed-arm ordinary
replacement; unrestricted strict gain remains unresolved.

## 1. Fixed supports and the problem being optimized

Start with the finite TP/BP strand system of
[the terminal flow normal form](COMPENSATION_FLOW_NORMAL_FORM.md). Each alpha
owner has two TP terminals, each beta two BP, and each mixed owner one of
each. Every declared link is TP--BP; cancellation C is a matching of such
terminal links. Owners have disjoint terminals. Mixed self-links can be
allowed in C; normalization removes their zero-credit cycles.

Fix distinct available original interval units I. Now give **every owner** x,
including betas, a set W(x) subset I of its whole-support eligible intervals.
A witness belongs to that owner's body, independently of which of its tips
remain free. A final strand K has support eligibility

    W(K) = union W(x), over its constituent current owners x.       (1)

An injective allocation F assigns different intervals to different final
alpha strands, each using a witness in(1). Cycles and final mixed/beta strands
cannot take an interval payment. The compensation and its two objectives are

    p(C,F) = b-b_C+|F|;
    first maximize p, then minimize |C|,                           (2)

where b is the original beta count and b_C the final beta count. This keeps
one consumption unit per whole beta; two BP tips do not create two beta units.

If a cancellation C0 is immutable, contract it first. Current virtual strands
are the owners, their supports are unions of constituent original supports,
and only links between their remaining free terminals are permitted. No step
below releases C0 or counts a consumed original beta again. All costs are
**additional** to C0. Closed components of C0 have no free terminals and are
not eligible owners for later payments.

No two-owner hypothesis on W is needed for the abstract theorem. The physical
gap adapter does supply it: each interval lies in an endpoint-free gap with
at most two bounding P columns, hence has at most two original strand owners.
Contraction can identify or remove those owners, never introduce a third.

## 2. Primitive certificates and capacity

A directed arm starts at one alpha, follows declared TP--BP links through
zero or more different mixed owners, and ends at a beta BP tip or at a
retained mixed owner. Alpha and beta owners cannot occur internally. The
arm retains its specific terminal links, not just owner-level reachability.

There are three primitives:

* **Interval stem:** one alpha followed by zero or more mixed owners, stopping
  at owner x, with a chosen interval j in W(x). It pays one demand with j.
* **Beta stem:** one alpha arm ending at a beta. It pays one demand by consuming
  that one whole beta, without using an interval.
* **Beta fork:** two arms from different alphas into the two **different** BP
  terminals of the same beta y, and one interval j in W(y). Their mixed
  interiors are disjoint. It pays two demands by consuming y once and using
  j once.

A primitive packing requires disjoint owner sets between primitives and
pairwise different interval units. The two arms within one fork meet only at
its beta. In particular, the same alpha, mixed owner, whole beta, terminal or
interval unit cannot be used by two primitives. A fork's two BP-entry witnesses
must be different even if several incoming links share the same beta owner.

**Lemma1 (lift).** A primitive packing with s interval stems, t beta stems,
f forks and l witnessed terminal links is a legal cancellation and allocation
with

    compensation s+t+2f, beta consumption t+f,
    interval payments s+f, link count l.                         (3)

**Proof.** A mixed owner's entry and exit are its different BP and TP tips.
A beta stem uses one beta tip; a fork uses its two distinct tips. Sources,
interiors and sinks are disjoint as specified, so all selected links form a
terminal matching. A stem ending at beta has equal alpha/beta counts and is
a final mixed strand. An interval stem has one alpha and no beta and is a
final alpha with its support witness retained. A fork has two alphas and one
beta, hence is a final alpha with witness j in its beta body. Its one consumed
beta and one selected interval are distinct resource identities. Other owners
remain unchanged and can be left unpaid. These components give exactly(3)
for the declared allocation. QED.

One incoming arm alone cannot take the beta-body interval: it forms a mixed
strand. Sending two arms into the same BP tip is not a terminal matching.
These are essential constraints, not optional refinements of an ordinary sink.

## 3. Complete normalization using only existing links

**Theorem2 (subset normalization).** For every legal(C,F) there is a primitive
packing that uses a subset of C, has compensation exactly p(C,F), and uses
exactly the original interval units selected by F. Consequently the largest
value and the minimum link cost in(2) equal those over primitive packings.

**Proof.** Work separately in each alternating component of the strand/C
multigraph. Suppress mixed owners. Every segment between retained alpha/beta
owners has one alpha and one beta endpoint: starting from a TP at alpha, a
link enters BP and each mixed strand exits TP, so the next nonmixed owner is
beta. Thus the retained sequence is an alternating alpha/beta path or cycle.
Segments and tails have disjoint mixed interiors and keep their witnessed
links from C.

For a component not allocated an interval, choose an adjacent matching of
the retained alternating path/cycle covering its smaller owner class. The
chosen segments are owner-disjoint beta stems, giving min(d,e) payments for
d alpha and e beta owners. In a cycle d=e; a pure mixed cycle contributes
zero. In a path d-e is0,1 or-1 according to its final type. This is exactly
the component's beta consumption in(2).

An interval-paid component must be a final alpha. Its retained sequence is

    a0,b0,a1,b1,...,b_(n-1),a_n,                              (4)

with n+1 alphas and n betas. Choose one original owner x witnessing its
allocated interval j. There are three possibilities.

If x=a_p, reserve that alpha as the zero-link interval stem. Pair every
other alpha a_i to b_i for i<p, and to b_(i-1) for i>p. These are adjacent
segments, cover every beta once and do not touch a_p.

If x is mixed, it lies in an end tail or in one segment between an alpha
and beta. Follow that tail/segment back to its adjacent alpha a_p and stop
at x. Reserve this prefix as an interval stem. Use the same adjacent matching
of all other owners just described. No chosen segment uses a_p or any part
of the reserved prefix, even if x lay inside the segment a_p--b_p or
b_(p-1)--a_p. Thus mixed-owner and terminal capacities hold.

If x=b_p, reserve the two adjacent alpha owners a_p,a_(p+1), both segments
into b_p, and their actual different BP-entry terminals. These form a beta
fork using j in W(b_p). Pair a_i to b_i for i<p and to b_(i-1) for i>p+1.
This covers every remaining beta once, excludes b_p, and uses no owner of
the fork. It produces n-1 beta stems plus the fork, giving n+1 payments.
For n=1 there are no remaining beta stems. This case accounts for an internal
beta witness without counting a second beta unit.

The first two cases give n beta stems plus one interval stem, also n+1
payments. In all cases every selected link is in C, j is retained exactly
once, and the component contributes its n consumed betas plus one interval.
Different components share no owners or terminals, and F already uses
different original intervals. Their primitive packings therefore combine.
They have exactly p(C,F) payments and retain precisely F's interval identities.
This proves the normalization statement.

Lemma1 lifts every packing with exactly its stated cost. Conversely normalize
an optimal(C,F); the selected subset has no more links. These two inequalities
prove equality of maximum cardinality and of minimum link cost. QED.

## 4. Exact optimization by reserving forks first

Let nu0(D),c0(D) be maximum compensation and minimum link cost for the
**ordinary stems** of an owner-support system D. It is exactly the established
integral-flow problem with one source per alpha, one unit gate per mixed,
one sink per whole beta, one sink per original interval, and access arcs
from alpha/mixed owner x to each j in W(x). These access arcs are labelled
by body witnesses. They are **not** a claim of physical free-tip access.
An ordinary stem can stop with its final TP unused while retaining that body.
The original flow proof therefore applies to this counting interface.

Let H range over all compatible beta-fork packings, including the empty one.
Delete every owner used by H, all incident terminal links, and the different
intervals paid by H. Keep all other original interval identities, supports and
link witnesses. Call the resulting system D-H and let l(H) be H's actual
link count.

**Theorem3 (exact residual-flow formula).**

    nu(D) = max_H [2|H|+nu0(D-H)].                         (5)

Among H attaining this maximum, the exact minimum additional link count is

    min_H [l(H)+c0(D-H)].                                 (6)

**Proof.** A fork packing and any ordinary-stem packing in D-H have disjoint
owners and original intervals, so Lemma1 gives the lower bound in(5).
Theorem2 normalizes an optimum into its fork subpacking H and ordinary stems
on D-H, giving the reverse bound. For each maximizing H, replace its ordinary
part by a minimum-cost maximum flow on D-H. This preserves the cardinality
in(5) and gives the upper bound in(6). Every normalized optimum's ordinary
part has at least c0(D-H) links, giving the lower bound. QED.

In particular, **if no feasible beta fork exists, whole-support compensation
and its minimum link cost are exactly an ordinary owner-support flow**. Merely
knowing that every beta is one resource does not establish this hypothesis.
Equation(5) is an exact finite optimization formula; enumerating fork packings
may be exponential. No polynomial-time general algorithm or new general flow
theorem is claimed.

The beta-free case is an unconditional specialization of this interface:
when b=0, there can be no fork, so whole-support maximum compensation and
minimum link cost are exactly an ordinary owner-support flow. This applies
to the entire frozen PP-seal donor-collision family from the preceding note,
including its fixed-C0 continuation states and arbitrary separated stacks.
Its full support, rather than only terminal access, can now be optimized by
this exact specialization.

## 5. Sharp possible gap and explicit controls

Let rho be the maximum matching size in the bipartite graph whose sides are
whole betas and original intervals, with y--j when j in W(y). Let k be the
alpha count. Then

    0 <= nu(D)-nu0(D) <= min(rho,floor(k/2)).               (7)

Indeed any packing contains at most rho forks because their betas and intervals
are distinct, and at most floor(k/2) because each uses two different alphas.
Replace each fork by one of its beta arms, discarding its interval and other
arm. The result is an ordinary-stem packing losing exactly one payment per
fork. Apply this to an optimum to prove(7). These are different units, not
independent local credits that may be added without a packing.

For a sharp abstract example take A=(0,1), B=(2,3) alpha, y=(4,5) beta,
links0--4 and2--5, and one interval J with W(y)={J} and W(A)=W(B)=empty.
Ordinary stems pay only one; the fork pays two, with exactly two links.
Both links into BP4 instead would pay only one. A single arm also pays only
one even though the beta sees J. Every original interval in this example
has at most one owner, so the physical two-owner bound alone does not remove
the abstract distinction.

Take q disjoint copies for arbitrary q>=1. Then k=2q,b=q,|I|=q,rho=q,
nu0=q,nu=2q, with2q actual links. The difference q attains(7). These are
abstract systems, not asserted completely frozen grids.

Cardinality equality does not make forks irrelevant to cost. Add to the
single-copy example two mixed owners m=(6BP,7TP),n=(8BP,9TP), links3--6
and7--8, and give n access to J as well. The interval now has exactly two
owners, y and n. Ordinary stems pay both with three links: A->y and
B->m->n->J. The beta fork pays both with two. Thus equations(5) and(6) are
both needed.

For any normalized packing with counts(s,t,f), write U=|I|-s-f for unused
original intervals, b'=b-t-f for unused whole betas and delta=k-s-t-2f.
The exact resource ledger is

    U+b'-delta = |I|+b-k.                                  (8)

There is no extra resource generated by a fork. Equation(8), like the prior
flow ledger, does not by itself prove the target's nonnegative margin.

## 6. Physical adapter, evidence and next geometric question

For a matching-closed aligned grid packet, keep all original unmarked interval
identities. W(x) consists of intervals lying in an endpoint-free gap bounded
by a P column of x's full original support. Pure PP cycles without free tips
are not strand owners and cannot be attached later by terminal links. Use only
actual permitted free-tip TP--BP adjacencies. Additional cancellation unions
support ownership exactly as in(1). This proves the adapter for arbitrary fixed
C0. It does not allow a marked interval, a nonterminal link, or a second use
of any selected interval.

The solver-free verifier checks10,906 abstract systems against105,625
independent terminal matchings and whole-support allocations. It separately
compares the primitive-packing optimizer, the fork-packing/residual-flow formula,
and the ordinary-stem flow. There are218 strict cardinality gains, one strict
cost gain,219 optima using forks,13,584 fork-pack residual-flow checks,332
subset-of-links normalization controls, and six sharp abstract stacks.
These are regression evidence for the written all-size theorem.

Physical checks cover2,442 fully frozen systems, including both bent actual
matchings, occupied adjacent bands, capacity-two rotors, branched stars,
all fixed cancellations on three existing frozen fixtures, and both whole-support
donor-collision families at W8/12 in four continuation states. There are2,402
independent exhaustive optimum comparisons over99,855 physical terminal
matchings. Every returned packing is replayed in the actual C0+C1 grid-support
model, keeping original interval identities. These physical controls contain
**zero feasible beta forks and zero physical strict fork gains**. Thus the
abstract gain examples do not establish a new frozen geometric phenomenon.

Three optional12-by14 Z3 discovery templates prescribe beta endpoints(5,6),
(8,6), an internal PP witness at band3/column6 and BB interval at column7,
with separate adjacent alpha entries. Same-side, opposite-side, and a relaxed
actual-matching version are UNSAT under their exact recorded constraints.
They neither prove general geometric nonexistence nor enter Theorems2--3.
The standalone script and receipts retain those restrictions.

Seven local Lean4.33.0 declarations pass without warnings, sorry or native
evaluation. They prove the arbitrary-length residual matching in(4) after
reserving either an alpha root or a beta with its two adjacent alphas: bounds,
adjacency, injectivity, coverage, exclusion of the reserved beta, and ledger(8).
Only propext and Quot.sound appear in their axiom audits. The full component
normalization, packing optimization and physical adapter remain written proofs.
No new external review is claimed.

Reproduce:

    python3 develop/check_whole_support_fork_normal_form.py --output output/whole-support-fork-normal-form-validation.json
    python3 develop/check_whole_support_fork_formal.py --lean /path/to/lean-4.33.0 --output output/whole-support-fork-lean-validation.json

The next geometric question is whether freezing forbids feasible beta forks,
forces an equally good ordinary-stem replacement, or admits an actual strict
gain. For the broader compensation goal, equations(5)--(8) also provide a
complete interface for combining interval ownership, mixed-gate capacity and
whole-beta use after immutable C0. A universal existence or numerical bound
still requires geometric control of those capacities and original resources.
