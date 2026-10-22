# Shared PP cycles: coherent orientation and exact compensation loss

## Scope and endpoint model

Keep the matching-closed packet, actual perfect matching M, original PP
auxiliary matching A, terminal labels and original interval set I of
COMPONENT_ISOLATED_AUXILIARY_COMPENSATION.md. The physical ledger remains
S_J-B=|I|+b-k. New edges require a declared permitted relation. None of
the arguments below supplies a universal geometric-existence theorem.

Choose r distinct original alpha paths and r distinct original beta
paths, and choose one free terminal on each. Let U be these 2r chosen
terminals. The other terminal of each chosen original path remains free.
Let C be a union of original alternating cycle components. A replacement
auxiliary matching may change edges only on U union V(C). It covers all
these vertices, and all other original A edges remain unchanged. Thus
every original PP endpoint stays covered, and r original TP and r original
BP terminals become covered. Original open paths have no changed internal
edges. Shared cycles can be used by any number of operations, provided the
complete replacement is one matching.

For analysis, replace each chosen original open path by its chosen end,
retaining that end's TP or BP label. Its unchanged tail leads to the other
free end with the same label. On the remaining reduced graph M matches
the cycle vertices, and N matches all vertices, including U. Components
are paths with ends in U and cycles. Their endpoint types are exactly the
types of the corresponding full final strands. This contraction is only
an analysis of unchanged tails, not a change to the actual matching.

## Shared-cycle orientation theorem

Choose, independently on each original cycle, one of its two alternating
vertex colourings by signs minus/plus. Both old M and A edges cross signs.
Give chosen TP terminals sign minus and chosen BP terminals sign plus.
Let h_minus and h_plus count replacement N edges with two minus ends and
two plus ends, respectively. All counts refer to distinct edges of the
single matching N, not to candidate operations separately.

**Theorem.** Write a for the number of final TP--TP paths inside this
affected region. Then

    h_minus=h_plus=:h,
    alpha_affected=beta_affected=a<=h,
    mixed_affected=r-2a.

The full final counts are therefore

    alpha_N=k-r+a, beta_N=b-r+a, mixed_N=g+r-2a.

In particular, if every new N edge crosses signs, then h=0 and all r
selected alpha/beta pairs are eliminated, even if all their surgeries
share the same original cycle. Other original components and local old
payment certificates supported on them remain unchanged. There is no
cut debt. No cycle component needs to be reserved for just one operation.

Proof. An alternating even cycle has equally many plus and minus vertices.
The chosen terminals also have equal counts of both signs. Summing signs
over all vertices and then over the edges of the perfect matching N on
this reduced vertex set gives 2(h_plus-h_minus)=0.

Consider one reduced final path or cycle. Its internal M edges pair all
vertices except the two path ends, and each such M edge has sign sum zero.
The sum of its vertex signs is thus the sum of its end signs (zero for
a cycle). Alternatively all its vertices are paired by N, so that sum is
twice the number of its plus--plus N edges minus twice its minus--minus
N edges. Consequently, on each component,

    #plus-plus N - #minus-minus N
       = -1 for alpha, +1 for beta, 0 for mixed or cycle.       (1)

Each final alpha contains at least one minus--minus N edge; different
alphas contain different edges. Thus a<=h_minus. Similarly beta<=h_plus.
There remain exactly r TP and r BP full free ends, so alpha=beta and
mixed=r-2a. Adding unchanged components gives the full inventories.
Coverage and terminal balance give the original zero-debt ledger. QED.

The minimum h over the two colour choices on each touched original cycle
is a computable upper bound on the residual alpha count. It is an
orientation-certificate bound, not an assertion that this minimum equals
the actual residual count. Different frustrated passages can cancel.
Nor does this theorem extend to internal surgeries through other open
strands; the cycle-only internal-support hypothesis is essential here.
The theorem refines routing certificates, not the scalar packet ledger
itself: signed balance is invariant under every admissible replacement.

## A parity certificate and a cycle-rank bound

The coherent-colouring test is linear in the size of the replacement.
Build a signed constraint multigraph H with one vertex for each touched
original cycle and one ground vertex for all chosen original terminals.
Fix a canonical alternating bit-colouring on each cycle (plus=1), and
use the prescribed sign bits on terminals. A variable f_C flips a cycle's
colouring; the ground variable is fixed to zero. For an N edge uv, its
opposite-sign constraint is

    f_owner(u) XOR f_owner(v) = 1 XOR colour(u) XOR colour(v).  (4)

Keep parallel constraints. Discard a loop with right side zero, since it
is always satisfied; retain a loop with right side one. Let q=|E(H)|-
|V(H)|+components(H), counting isolated vertices in both latter terms.

**Parity and rank corollary.** A coherent certificate exists exactly when
these binary constraints are consistent, equivalently every closed walk
has XOR of edge requirements zero. A spanning-forest traversal either
constructs it or gives a violated nonforest constraint and its fundamental
closed walk. Moreover, without any consistency assumption, the traversal
constructs a colouring with

    alpha_affected <= h_forest <= floor(q/2).             (5)

In particular q<=1 suffices for complete alpha/beta elimination, even
when original-cycle supports overlap. This is a condition on a supplied
replacement, not an algorithm for finding a universally adequate N.

Proof. Propagate f along a spanning forest, starting at ground with zero
in its component and at an arbitrary zero root in every other component.
Every forest edge is satisfied. A nonforest edge is consistent precisely
when its requirement agrees with the XOR along its forest path; a loop
has an empty path. These tests give both the equivalence and certificates.

There are q nonforest edges, so at most q N edges violate their crossing
constraint. Discarded loops never violate it. Each violating edge is
either minus--minus or plus--plus. The preceding theorem proves these
two counts equal for every assignment of flips. Consequently the number
of violations is 2h_forest, so 2h_forest<=q. Combine a<=h_forest to obtain
(5). This uses a single final matching and assigns each violating edge
to exactly one component. QED.

The minimum-orientation budget is half the minimum number of violated
constraints, but a spanning-forest certificate already gives (5). No
optimization algorithm or complexity classification for that minimum is
claimed. Inconsistency of (4) means absence of this sufficient coherent
certificate; it need not mean a final alpha survives, since bad edges
can occur in final cycles or cancel within mixed paths.

## Arbitrary-length obstruction with distinct original donors

For every r>=2 take r alpha actual edges (t_i,t'_i), r beta actual edges
(p_i,p'_i), and one alternating cycle on x_i,y_i, with indices modulo r:

    old A: x_i--y_i,
    actual M on the cycle: y_i--x_(i+1).

All t terminals are TP and all p terminals are BP. The initial inventory
is alpha=r, beta=r, mixed=0 and one cycle. Choose any cyclic binary word
epsilon_0,...,epsilon_(r-1). For every i replace the old A edge by two edges:

    epsilon_i=0: t_i--x_i, y_i--p_i;
    epsilon_i=1: t_i--y_i, x_i--p_i.                    (2)

Each replacement is a simple A-augmenting path from its own alpha to its
own beta. The r augmenting paths are vertex disjoint, use r different
alphas and r different betas, and have no other open strand in their
supports. Their supports share precisely the old cycle. All old PP
vertices remain covered; the replacement is a matching.

**Exact loss formula.** Let c_10 be the number of cyclic transitions
1->0 in epsilon. Then

    alpha_N=beta_N=c_10,
    mixed_N=r-2c_10.                                  (3)

Proof. Every final reduced path consists of one actual cycle edge
y_i--x_(i+1), its two new N edges, and two terminals. Its types are:

| epsilon_i | epsilon_(i+1) | Ends | Final strand |
|---|---|---|---|
| 0 | 0 | p_i, t_(i+1) | mixed |
| 0 | 1 | p_i, p_(i+1) | beta |
| 1 | 0 | t_i, t_(i+1) | alpha |
| 1 | 1 | t_i, p_(i+1) | mixed |

Every actual cycle edge belongs to exactly one such path, so this list
is exhaustive and nonoverlapping. A cyclic binary word has equally many
0->1 and 1->0 transitions, by telescoping successive values. Equation
(3) follows. The unchanged original tails preserve all endpoint labels.
QED.

Uniform epsilon gives zero residual alpha and r mixed paths. Alternating
epsilon gives c_10=floor(r/2), the maximum possible value: each 1->0
transition uses a distinct 1 and a distinct 0, so c_10<=min(#0,#1)<=r/2.
Thus distinct donors and vertex-disjoint augmentations can still leave
an arbitrarily large number of alphas. The failed rule is simultaneous
one-for-one alpha/beta elimination without orientation control. The
example is abstract endpoint accounting; no frozen grid embedding or
counterexample to the target inequality is claimed. Signed charge remains
zero for every word.

The smallest r=2 obstruction has 12 endpoints. Take epsilon=(0,1):
the final inventory is alpha=beta=1 and mixed=0, although both source
and donor choices were distinct. For the same graph, epsilon=(0,0)
gives alpha=beta=0 and mixed=2. The distinction is the direction of the
second passage through the shared cycle, not a shortage of original beta
resources or an invalid replacement matching.

For the colouring x_i=plus,y_i=minus, every reversed passage contributes
one minus--minus and one plus--plus edge, so h=#1. Reversing the whole
cycle gives h=#0. The orientation bound becomes a<=min(#0,#1), and is
sharp for alternating words. It need not be exact: the word 000111 has
c_10=1 but min(#0,#1)=3. No minimum-orientation-cost optimality claim is made.

## Verification and remaining geometric problem

The permanent checker reconstructs complete actual/auxiliary multigraphs,
including parallel edges. It checks the per-component identity (1), the
global orientation budget, the exact family formula (3), valid vertex
disjoint augmentations and distinct original donors. Finite controls
support the written all-r and arbitrary-replacement proofs.

The local run passes 5,422 arbitrary balanced replacements (3,195 also
decompose into distinct-source/distinct-donor TP--BP augmentations), 8,536
cyclic-word controls, 38,427 signed colourings and 13,958 parity/rank
certificates. Among these, 1,452 low-rank replacements completely repair
the sources. Another 915 cases have no coherent orientation certificate
but no residual alpha, confirming that coherence is sufficient rather
than necessary. The word controls include all words of lengths 2--12
and uniform, alternating and single-block words through length 128.

The associated Lean source formalizes signed N-edge sums along arbitrary
finite alternating walks, the compulsory same-sign-edge witnesses for
alpha/beta paths, and summed nonreuse bounds for arbitrary finite lists
of supplied routes. Its interface does not construct graph components,
prove they are disjoint, or certify physical grid availability. Those
steps belong to the written proof and graph reconstruction checks.
Ten main statements and their individual axiom audits pass locally in
Lean 4.33.0 using only propext and, except for the walk identity,
Quot.sound. The rank theorem consumes the separately proved forest-error
bound as a hypothesis; it does not implement the graph traversal.

The next geometric question is whether frozen grid PP cycles admit
coherent passages for enough demands, or whether a geometric orientation
conflict must be paid by original interval units. The earlier reflected
family uses a two-edge cycle and an internal donor path; that explicit
repair remains covered by the previous theorem, rather than automatically
falling under this cycle-only extension. Universal grid compensation,
the universal 5/6 improvement and triple equality remain open. The global
outside-overlap correction is still retained once where applicable.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
