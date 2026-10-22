# Internal mixed relays: endpoint signs and an open-strand obstruction

## Replacement model

Fix actual M, PP auxiliary A, the original TP/BP free-end labels, and
the exact packet ledger S_J-B=|I|+b-k. Choose r different original alpha
paths and r different original beta paths, one free terminal on each.
Let U be those chosen terminals. Their internal edges and other free
ends are unchanged. In addition to original closed PP cycles, permit
internal auxiliary changes on t original mixed paths. Call their original
free ends F. Every original mixed free end remains A-free and N-free;
only their internal PP vertices may be rematched. All other original
open paths stay untouched.

The new auxiliary N is one matching. On the affected region it covers
all original A-covered vertices and all vertices of U, and leaves exactly
F uncovered. All changes remain inside that region, and new edges have
declared permitted witnesses. These are conditional geometric hypotheses;
no universal availability or disjoint-linkage theorem is asserted.

Contract each selected alpha/beta's unchanged tail to its chosen terminal.
The reduced actual M covers every relay/cycle vertex and no vertex of U.
The reduced N covers every vertex except F. Components of M union N
are paths with ends in U union F or cycles. Expanding the tails preserves
the labels at U. Labels at F are already the final physical labels.

## The sign reversal at mixed free ends

On each original mixed path choose its unique alternating vertex-sign
colouring with

    original mixed TP free end: plus,
    original mixed BP free end: minus.                 (1)

These are the reverses of their physical terminal signs. Both original
M and A edges then cross signs. On each original cycle either alternating
colouring is allowed. At U use the usual physical signs TP=minus,
BP=plus. Thus every reduced M edge crosses signs.

This reversal is forced by the boundary incidence: a vertex of U is
matched only by N in the reduced graph, whereas a vertex of F is matched
only by M. Using physical signs at both sorts of boundary would give
the wrong charge identity. All mixed relay colours are fixed by (1);
only closed-cycle colours can be flipped independently.

**Mixed-and-cycle relay theorem.** Let h_minus and h_plus be the counts
of N edges with two minus ends and two plus ends. Then

    h_minus=h_plus=:h,
    alpha_affected=beta_affected=a<=h,
    mixed_affected=r+t-2a.                             (2)

In the full packet,

    alpha_N=k-r+a, beta_N=b-r+a, mixed_N=g+r-2a.         (3)

In particular if every new N edge crosses the prescribed signs, all r
selected alpha/beta pairs disappear. Internal mixed relays and closed
cycles may be shared by arbitrarily many surgeries as long as the single
complete N is a matching satisfying the coverage assumptions. No new
PP free ends or cut debt occur. Original interval identities and all
untouched local old payment certificates are preserved.

Proof. The N-covered set consists of U, every cycle vertex, and every
internal PP vertex of each original mixed relay. U has r signs of each
type; every cycle has equal sign counts; each relay's internal vertices
are paired by old A edges, which cross signs. Therefore the sign sum of
the N-covered set is zero, yielding h_minus=h_plus.

For one final reduced component D, count vertex incidences of N minus
vertex incidences of M. All internal incidences cancel. Vertices of U
contribute plus their colour sign; vertices of F contribute minus their
colour sign. By (1), this difference is exactly the sum of the physical
terminal signs of D. Every M edge crosses signs, so its endpoint sign
sum is zero. Consequently

    #plus-plus N in D - #minus-minus N in D
       = -1 for alpha, +1 for beta, 0 for mixed/cycle.  (4)

A final alpha needs at least one minus--minus N edge. Distinct final
components have disjoint N edge sets, so a<=h_minus without reuse. The
affected full free ends comprise r+t TP and r+t BP ends; thus alpha=beta
and mixed=r+t-2a. Add unchanged components to obtain (3). Original
labels are retained and equal numbers of original TP and BP ends are
newly covered, giving the same zero-debt physical ledger. QED.

A final relay path consisting of a single M edge and no N edge is
necessarily mixed, and contributes zero to (4). It is not omitted from
the endpoint count.

## Fixed mixed colours in the parity certificate

The previous XOR certificate extends to this model. Put each original
cycle in its own variable owner. Put U and every vertex of every mixed
relay in ground, with their individually prescribed colour bits.
For each N edge uv require

    f_owner(u) XOR f_owner(v) = 1 XOR colour(u) XOR colour(v).

Keep multiplicity and contradictory loops; discard only tautological
loops. A spanning forest gives a coherent colouring or a contradictory
closed-walk certificate. Its q nonforest constraints bound the number
of violating N edges. By h_minus=h_plus these violations come in pairs,
so

    a<=h_forest<=floor(q/2).                           (5)

The same proof as for closed-cycle relays applies, now using (4).
q<=1 still suffices for full compensation. A missing coherent certificate
is not by itself a residual-alpha certificate. Internal mixed orientation
is prescribed by its original physical ends and cannot be flipped to
repair a contradictory ground loop.

Neither coherence nor forest rank is an optimization theorem over all
possible N. The statement preserves the exact ledger; it does not by
itself improve the scalar grid bound. To turn it into a packet bound,
remaining alphas must have distinct legitimate interval payments, with
their local access certificates still valid. The global outside-overlap
correction remains once where applicable.

## An eight-endpoint obstruction beyond cycle normalization

Take eight distinct endpoints t,t',p,p',q_T,x,y,q_B with

    actual M: t--t', p--p', q_T--x, y--q_B,
    old auxiliary A: x--y.

t,t',q_T are TP and p,p',q_B are BP. The original strands are one
alpha, one beta and the mixed path q_T--x--y--q_B. There is no cycle.
The internal relay colours from (1) are

    q_T plus, x minus, y plus, q_B minus.

The augmentation t--x--y--p is simple and uses exactly one original
alpha and one different original beta. Replace A by

    N_bad: t--x, y--p.

The final open paths are t'--t--x--q_T and p'--p--y--q_B: one alpha
and one beta, no mixed path. Thus the operation eliminates neither
original unit of signed demand/donor count. It reroutes them through the
old mixed strand. Its N edges are respectively minus--minus and
plus--plus, so h=1 and (2) is sharp. The parity graph has one ground
vertex and two requirement-one loops, giving q=2 and a=floor(q/2)=1.

In contrast the augmentation t--y--x--p gives

    N_good: t--y, x--p.

Both new edges cross signs. Its final paths are t'--t--y--q_B and
p'--p--x--q_T, both mixed. The one alpha and one beta disappear, as
the theorem states. No extra resource was created in either case.

Even allow every edge of M, A, N_bad and N_good as an actual edge of
the abstract endpoint graph. Its actual perfect matching is unique:
the four degree-one vertices t',p',q_T,q_B force all four edges of M.
There are no original PP cycles to normalize, and no alternative actual
matching can remove this example's mixed-relay orientation issue.
Disjoint copies give arbitrarily many such failed augmentations with
distinct sources, donors and relay strands; reversing their passages
repairs all of them when those alternative edges are permitted.

This refutes extending cycle-only automatic compensation to unrestricted
internal mixed passages. It does not refute the target packet/grid
inequality, or rule out another admissible N. The example is abstract;
no feasible frozen-grid embedding or minimality among all obstructions
is asserted.

## Verification scope

The checker reconstructs reduced and full-tail multigraphs, separately
tracks N-free mixed ends and M-free chosen ends, verifies (4) on every
component, counts distinct same-sign edges, and checks all cycle flips
and the parity/forest rank bound. The explicit bad/good example also
checks uniqueness of the actual matching including both candidate
edge sets. Finite controls test the written general proof, not replace it.

The local run passes 24,413 general mixed-relay replacements, plus the
two explicit bad/good controls, with 59,581 signed-colouring controls
and 24,415 independent full-tail and parity/rank reconstructions. It
includes 8,235 coherent certificates and 5,435 low-rank complete repairs.
The 20,221 replacements whose A union N path components are TP--BP may
also contain independent alternating-cycle exchanges; no pure-path-only
classification is inferred. Occurrences of a retained single-M mixed
path with no N edge are also checked explicitly.

The Lean source proves the endpoint-incidence identity from a supplied
permutation of vertex occurrences, verifies the opposite-edge actual
matching contribution is zero, and derives the compulsory same-sign
edge witnesses for alpha and beta components. Graph component existence,
incidence permutations, disjoint edge identities and geometric availability
remain supplied by the written graph argument and reconstruction checks.
All six named statements and individual axiom audits pass locally in
Lean 4.33.0: the neutral actual-edge sum uses propext, and the other five
use propext and Quot.sound. No sorry, native-evaluation step or new axiom
is used. The formal incidence permutation is supplied, not derived from
an encoded graph. It records sign occurrences; distinct vertex/edge
identities and component disjointness remain in the written application.

The remaining problem includes internal passages through other original
alpha or beta strands, and geometric existence of enough admissible
replacements. Actual closed-cycle normalization and fixed mixed-relay
colouring address different parts of that problem. Universal grid
compensation, the universal 5/6 improvement and triple equality remain open.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
