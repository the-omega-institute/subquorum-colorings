# Vertex penalties, exterior extensions and the unrestricted 51/517 bound

12 November 2026. All graphs are finite, simple and bipartite. A minimal
two-star-forming set is inclusion-minimal; every outside vertex belongs to
a not necessarily induced copy of K_(1,2) with exactly two selected vertices. Write beta_2(G)
for the maximum size of a set inducing maximum degree at most one.

**Theorem.** Every graph G of maximum degree at most three, and every
minimal two-star-forming set S, satisfy

    517(|S|-beta_2(G)) <= 51|V(G)|.

Consequently SF_2(G)-beta_2(G)<=floor(51n/517). This includes the empty
graph and requires no connectivity, minimum degree, balance or condition
on the components induced by S. The coefficient improves 15/152 by
3/78584. Sharpness and attainment remain open.

The new step is a template construction with arbitrary nonnegative vertex
penalties. Assigning half the external degree as penalty incorporates the
boundary cost into the same conditional expectation that chooses the phase.
The paired-margin and two-endpoint lemmas, fixed witness extraction and
compatibility are established in [the preceding proof](TWO_ENDPOINT_MARGIN_AND_SUBCUBIC_BOUND.md).
We retain their notation and supply all new inferences below.

## 1. Template data used from the preceding proof

The extracted template H has disjoint layers I,C,X of orders b,2b,2b.
Each helper in I has two witnesses in X; each witness has one matched owner
in C. Its core H[C] has maximum degree two, and H[X] is a partial matching.
Pairing the witnesses of each helper gives an auxiliary matching P, distinct
from physical edges; its union with H[X] consists of even paths and cycles
of order divisible by four. A fair bit on each auxiliary component selects
one witness of each helper. Let Y be those b witnesses and A the b owners
whose witnesses are omitted. Each witness and each owner belongs to Y or A,
respectively, with probability exactly 1/2. This remains true when many
vertices share one bit.

There is a pointwise cycle-and-endpoint score s such that

    beta_2(H[A]) >= 2b/3+s,
    E s >= -rho+t_g/6,
    rho = b/6-o/3-sigma.

Here o counts auxiliary cycles of order four modulo eight, t_g counts
physical core paths whose two endpoint literal runs have length at most two,
and sigma is the total nonnegative owner-class margin. Whole P1/P2 events
are counted once. The supports of endpoint and cycle scores are disjoint.
For every phase, choosing an optimal residual core set Z gives an actual
dissociation set I union Y union Z.

Two one-side constructions D_0,D_1 also satisfy

    |D_0|+|D_1| >= 11b/2-o.

Their owner parts are the two bipartition sides of C, so each owner belongs
to exactly one of these sets. Each helper and witness belongs to at most two.
The same proof gives these inequalities for auxiliary paths as well as cycles.

For the existing resource counts t_b,s_g,s_b,b_G, the paired budget is

    t_b+s_b <= 6sigma,       4s_g <= b_G.                 (1)

Every bad physical path contributes one triple; every bad auxiliary path
has one flag. Each owner-class margin is used once in (1).

## 2. A general nonnegative vertex-penalty lemma

Assign arbitrary nonnegative real costs w_v to H. Put w(K)=sum_(v in K)w_v
and Phi(D)=|D|-w(D). There is an actual dissociation set D of H satisfying

 Phi(D) >= 13b/5+3sigma/5+t_g/10-w(I)-w(C)/2-7w(X)/10.    (2)

**Proof.** For a phase and its residual optimum Z subset A, nonnegativity
of costs gives

 Phi(I union Y union Z)
 >= 8b/3+s-w(I)-w(Y)-w(A).

Take expectations. Every owner and witness is retained with probability
1/2, regardless of dependence among their bits. Thus some actual phase set
has potential at least

 F = 5b/2+o/3+sigma+t_g/6-w(I)-(w(C)+w(X))/2.             (3)

This phase can be found by conditional expectation on the score
s-w(Y)-w(A). Each penalty is a one-bit event. After fixing every bit,
compute an optimal unweighted dissociation set in the retained core;
the preceding pointwise inequality still proves (3). No weighted-optimal
residual solver is assumed.

For the one-side sets, count costs before averaging. Owners occur once,
and helpers and witnesses at most twice, giving

 (Phi(D_0)+Phi(D_1))/2
 >= O = 11b/4-o/2-w(I)-w(C)/2-w(X).                      (4)

Choose the largest potential among the phase set and D_0,D_1. Its potential
is at least (3F+2O)/5. The o terms cancel, giving exactly (2). This compares
three actual sets; no union between them is taken. QED.

The proof covers zero and arbitrary nonnegative real costs. The executable
uses exact rational costs, including rationals with 401-bit numerators.

## 3. Boundary-aware exterior extension

Now let H be the template extracted from a minimal S in G; write b'=b-b_3
for its number of helpers. Set

    w_v = |N_G(v) outside H|/2.

Let B_I,B_C,B_X count physical boundary incidences on their respective
template layers. For any dissociation set D of H, delete N_G(D) from each
exterior bipartition side. The two surviving independent sides are both
compatible with D, and their sizes sum to at least

    n-5b' - 2w(D).

Selecting the larger side therefore gives an actual full-graph set of
size at least n/2-5b'/2+Phi(D). Shared exterior neighbours only reduce
the number deleted, so counting incidences is valid without a disjointness
assumption. Applying (2) gives

 beta >= n/2+b'/10+3sigma/5+t_g/10
         -B_I/2-B_C/4-7B_X/20.                           (5)

The established physical boundary counts are

 B_I<=3q,  B_C<=2(t_g+t_b),  B_X<=2(s_g+s_b).

Owners have one internal witness edge and at most the unused endpoint
slots of their core paths. Witnesses have internal owner and helper edges,
leaving only two unmatched interface slots per auxiliary path. An extra
helper neighbour must be among the q unallocated outside vertices: allocated
triple witnesses have only their selected leaf as selected neighbour, and
every allocated pair witness meeting an h=2 helper already belongs to H.
Consequently (5) implies

 beta >= n/2+b'/10+3sigma/5-2t_g/5-t_b/2
         -7(s_g+s_b)/10-3q/2.                            (6)

The retained-set extension from the preceding theorem remains a separate
actual full-graph candidate. Its lower bound and (6) concern the same beta;
the retained set is never united with an exterior independent side.

## 4. Exact nonnegative ledger

Use the fixed witness counts from the preceding proof. R contains selected
isolates and isolated edges; p is the number of disjoint selected-centre,
selected-leaf, private-outside-witness triples. The remaining u selected
core vertices have distinct pair witnesses. Let a count selected isolates
with one pair-witness neighbour, b those with at least two, and b_3 those
with three. Put

 m=min(a,p), alpha=a-m, pi=p-m,
 e=u-a-2b, r=|R|-a-b, q=n-|S|-p-u,
 d=|S|-beta, tau=m+b-2d, b'=b-b_3,
 L=|R|-b'+p, Z=5beta-5L-13b'.

All alpha,pi,r,q,tau,b_3,e-b_3 are nonnegative. The preceding compatible
template construction proves

 Z>=3sigma+(3b_G+2t_g)/4.                                 (7)

The exact witness identities are

 n-10d=m+r+3(alpha+pi)+2e+q+5tau,
 8n-81d=Z+8r+19(alpha+pi)+11e-8b_3+8q+38tau,
 2beta-n-b'/5=-2m-alpha-pi+r-2e-3b_3-q+2Z/5.

Write T=2m+alpha+pi+2e+3b_3. Rearranging (6) and using the last identity,

 T<=r+2q+2Z/5+4t_g/5+t_b+7(s_g+s_b)/5-6sigma/5
  <=r+2q+2Z/5+4t_g/5+36sigma/5+7b_G/20
  <=r+2q+14Z/5.                                         (8)

The middle step uses (1): t_b+7s_b/5<=7(t_b+s_b)/5<=42sigma/5,
and 7s_g/5<=7b_G/20. For the final step, (12/5) times (7) supplies
36sigma/5+6t_g/5+9b_G/5, which is at least the required expression.
Hence

    W=5r+10q+14Z-5T>=0.

Taking 14 times the second witness identity minus 10 times the first,
and substituting W, gives exactly

 102n-1034d = W+97r+241(alpha+pi)+144(e-b_3)
                 +47b_3+92q+482tau >=0.                  (9)

Each term is nonnegative. Division by two proves 517d<=51n. Maximizing
over minimal S and using integrality gives the stated floor. When G is
empty every quantity is zero. QED.

## 5. Verification scope

`python3 -B scripts/check_boundary_expectation.py` checks actual weighted
candidate sets, their phase scores, conditional expectations and physical
exterior extensions. Its graph controls enumerate every minimal forming set in binary bipartite
adjacency models of total order at most seven and maximum degree at most
three, with a smaller bipartition side placed first, as well as ninety seeded
models and the specified fourteen-vertex cubic graph. Separately, each of
5,200 small templates (b<=3, order<=15) is checked with its canonical minimal
selection S=I union C and an exact unrestricted unweighted dissociation
optimum. The 43,684 minimal-selection cases combine those two scopes; they
are instance checks, not counts of isomorphism classes.

The weighted controls cover 28,635 cost assignments on 5,727 templates,
103,470 physical phases and 76,545 conditional expectations. Independent
excluded/isolated/paired recursion checks 580 weighted optimization instances on 116 template models
of order at most ten; ten instances (five costs on each of two models) also
use literal subset checking.
Costs include zero and rationals with 401-bit numerators. Larger prescribed
templates check actual candidates and all phases, not unrestricted optima.
The new full candidate improves the preceding algorithm on 472 controls;
680 controls choose an inner template set with fewer vertices before
exterior extension. This verifies that potential and cardinality are
distinct objectives in the implementation.

The theorem has the general proof above. The earlier imported main suites
are not executed, and the new result has no Lean formalization. Unit-weight
grid compensation and arbitrary rectangular-grid equality retain their
previous open status.
