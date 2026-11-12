# Core-cycle certificates for unrestricted subcubic gaps

12 November 2026. Graphs are finite, simple and bipartite. Formation uses
non-induced K_(1,2) with exactly two selected vertices, minimality is by
inclusion, and beta_2 is unrestricted dissociation. Fix any minimal
forming S in a graph of maximum degree at most three. The unrestricted8/81 bound is proved in
SHARP_ODD_CYCLE_PHASE_COMPENSATION.md. This note gives additional
instance certificates and a hierarchy under longer-core-cycle conditions.

## 1. Template and one fixed physical allocation

Use the witness decomposition in SHARP_BIPARTITE_STAR_FORMING_GAP.md and
ODD_AUXILIARY_CYCLE_COMPENSATION.md. With the notation there, put

    d=|S|-beta_2, m=min(a,p), alpha=a-m, pi=p-m,
    e=u-a-2b, r=|R|-a-b, q=n-|S|-p-u, tau=m+b-2d.

All these slacks except possibly d are nonnegative, including e-b3.
The exact universal ledger is

    n-10d=r+m+3alpha+3pi+2e+q+5tau.                  (1)

The h=2 helpers, their witnesses and distinct owners induce a partial
template with b'=b-b3 helpers,2b' witnesses X and2b' owners C. Its core
F=G[C] has maximum degree two; the witness interface is a partial matching.
The original bipartition need not be balanced. Every template dissociation
set can be enlarged simultaneously by the retained R vertices outside
the template and all p chosen selected triple leaves. Denote their total
size by L=|R|-b'+p. Their cross-edge exclusions are supplied in the cited
proof; no new witness choice is made below.

Pair each helper's two witnesses by an auxiliary P edge and use Q for
the actual witness-interface matching. Each P union Q component has two
proper phase classes of equal size. Independently select one class in
each component, forming Y of size b'. Retain the owners

    A=C minus {owner(x):x in Y},   |A|=b'.

For every dissociation Z of F[A], I union Y union Z is dissociation.
Thus a core bound beta_2(F[A])>=lambda b'+t gives a template certificate
of size at least(2+lambda)b'+t. This phase selection is unrelated to the
original graph bipartition.

## 2. Exact correlated square correction

For a core component K isomorphic to C4 let k_K=|A intersect K|. Every
induced subgraph of C4 has dissociation number min(k_K,2). Set

    f(k)=5min(k,2)-3k,   f(0..4)=(0,2,4,1,-2),
    eta=sum_(K a C4 component of F) E[f(k_K)].             (2)

Each vertex's retention is a literal of its auxiliary-component phase.
Therefore each expectation involves at most four fair bits, with repeated
bits retained exactly, including opposite literals. Complementing all bits
replaces k by4-k. Also8eta is an integer: with at most three distinct
bits the denominator divides8; with four distinct bits the four indicators
are independent and their expected f is17/8. Complement pairing alone
would not justify this denominator claim.

Every path P_t has beta_2(P_t)=ceil(2t/3)>=3t/5. Every even cycle other
than C4 has beta_2(C_t)=floor(2t/3)>=3t/5: check t6,8,10 directly; for
even t>=12, floor(2t/3)>=2t/3-2/3>=3t/5. A cycle in F[A] is an entire
component of F, since its vertices already use both core degrees.
Consequently, pointwise,

    5beta_2(F[A])>=3b'+sum_K f(k_K).                       (3)

The square terms refer to disjoint actual core components. All remaining
components are counted once by their density bound. Taking expectations,
then choosing a phase at least as good as the average, proves

    beta_2(template)>=(13b'+eta)/5,
    beta_2(G)>=L+(13b'+eta)/5.                            (4)

This is constructive: evaluate each local expectation by at most16
assignments, fix successive bits without decreasing the expected sum,
and optimize the residual paths/cycles. No global exponential phase
expectation is required. The correction can be negative; its sign must
not be discarded.

Set Z=5beta_2(G)-5L-13b'-eta>=0. Substitution in(1) gives

    d+Z=8m+5alpha+5pi+2tau+5e+8b3-eta,

    8n-81d=Z+8r+19alpha+19pi+3e
                 +8(e-b3)+8q+38tau+eta.                 (5)

Hence the general instance-dependent certificate is

    d<=floor((8n-eta)/81).                               (6)

All terms in(5) other than eta are nonnegative. Multiplying by8 gives
an exact integer certificate. Combined with the unrestricted8/81 bound, the result gives
 d<=floor((8n-max(0,eta))/81). Positive eta strengthens that bound.

A square wholly in one auxiliary phase class has expected f=-1.
Every other square has expected f>=1/4. Here is a complete calculation,
not an independent-vertex approximation. If opposite literals of the
same bit occur, k cannot equal4; symmetry gives Pr(k=3)<=1/2, and
E[f]=4-5(Pr(k=3)+2Pr(k=4))>=3/2. Otherwise the literal groups are
independent. Their size partitions and expected f are

    (4): -1; (3,1):1/4; (2,2):3/2;
    (2,1,1):3/2; (1,1,1,1):17/8.

These values follow by choosing each group with probability1/2 and
using f(0..4). Thus eta>=0 whenever no core square is wholly within
one auxiliary phase class. In that case, as well as when F has no
square component, (6) gives d<=floor(8n/81).
In particular every C4-free original graph satisfies this bound.
No connectivity or selected-component condition is imposed.

## 3. A hierarchy from longer core cycles

Let h>=1 be an integer. If every cycle of F has length at least6h,
then every residual core component has dissociation density at least

    lambda_h=(2h+1)/(3h+2).                               (7)

Paths have density at least2/3. For a residual even cycle, write its
length as6j,6j+2 or6j+4. In the last two cases j>=h. Comparing its
floor(2t/3)/t with (7), the cross-multiplied differences are respectively
2j-h and2j-2h, both nonnegative. For6j the density is exactly2/3.
The density bound is sharp for the cycle C_(6h+4).

For every phase the template certificate is at least

    ((8h+5)/(3h+2))b'.

Put Z_h=(3h+2)beta_2(G)-(3h+2)L-(8h+5)b'>=0. Direct substitution
in the same fixed ledger yields

 (5h+3)n-(51h+30)d = Z_h+(5h+3)r
       +(12h+7)(alpha+pi)+(2h+1)e+(5h+3)(e-b3)
       +(5h+3)q+(24h+14)tau >=0.                         (8)

Therefore

    d<=floor((5h+3)n/(51h+30)).                          (9)

An original graph of girth at least6h suffices. An acyclic graph is
understood to have infinite girth. The actual hypothesis concerns only
the extracted core; shorter cycles elsewhere need not be excluded.
For h1,2,3 the bounds are8n/81,13n/132,6n/61, respectively.

If F is acyclic, all residual components are paths, with density at
least2/3. The limiting certificate is an attained finite argument:

    Z_inf=3beta_2(G)-3L-8b'>=0,
    5n-51d=Z_inf+5r+12(alpha+pi)+2e
                  +5(e-b3)+5q+24tau>=0.                 (10)

Thus d<=floor(5n/51). No limit exchange or finite search is used.
None of the graph coefficients is asserted graph-sharp.

## 4. The random-phase ceiling and a rejected shortcut

The connected30-vertex fixture has b'=6,o=3 and three auxiliary4-cycles.
All eight phases leave exactly two P3 components in the core. Thus

    beta_2(F[A])-b'/2=4-3=1=o/3

for every phase. Disjoint unions of k copies give the exact expectation
k=o/3 at every scale. This proves that a universal phase-expectation
coefficient greater than1/3 is impossible. The matching universal
o/3 lower bound is proved in SHARP_ODD_CYCLE_PHASE_COMPENSATION.md.
This ceiling does not refute a stronger unrestricted template bound:
other dissociation sets need not arise from these phase choices.
The fixture and its eight explicit residual decompositions make this an
all-scale component argument, not extrapolation from random tests.

The initial research response proposed beta_2(C_t)>=2t/3 for even t>=6.
That step is false for C8 and C10. Its C4-only2/3-density reduction is
not used. The correct3/5 bound and the exact square correction above
retain all cycle floors and phase dependencies. The universal o/3
lower bound in the separate note uses cycle-event pairing and disjoint
owner-class budgets, retaining the correct cycle floors.
