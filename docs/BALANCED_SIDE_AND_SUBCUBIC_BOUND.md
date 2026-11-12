# Balanced witness marginals and an unrestricted 7/71 subcubic bound

12 November 2026. All graphs are finite, simple and bipartite. A two-star-forming
set is a set S such that every outside vertex belongs to a not necessarily
induced K_(1,2) with exactly two vertices in S; minimal means inclusion-minimal.
The dissociation number beta_2 is the maximum size of a vertex set inducing
maximum degree at most one.

**Theorem.** For every graph G of maximum degree at most three and every
minimal two-star-forming set S,

    71(|S|-beta_2(G)) <= 7|V(G)|.

Thus SF_2(G)-beta_2(G)<=floor(7n/71), including the empty graph. No connectivity,
minimum-degree, balance or selected-component assumption is imposed. The
coefficient improves 51/517 by 2/36707. Its sharpness and attainment are open.

The vertex-penalty argument in BOUNDARY_EXPECTATION_AND_SUBCUBIC_BOUND.md
charges witnesses at coefficient 7/10. We improve that coefficient to 1/2 by
balancing the one-side constructions. The phase score, fixed witness extraction,
paired-margin inequalities and physical boundary estimates are unchanged.

## 1. Template and auxiliary quotient

Use disjoint layers I,C,X of orders b,2b,2b. Each helper i in I has two witnesses
in X, each with its own distinct owner in C. These are all helper/witness and
owner/witness incidences within the template. The core on C has maximum degree
two; physical edges on X form a partial matching Q. Pair the two witnesses of
each helper by an auxiliary edge P. The graph P union Q consists of paths of even order
and cycles of order divisible by four. Alternating helper colours along a
component mean that any cyclic component has an even number of helpers.

For a fixed physical bipartition side epsilon, call the helpers on that side
eligible. On an auxiliary path, order its eligible helpers along the path;
on an auxiliary cycle use their cyclic order. Two consecutive eligible helpers
are the neighbours of a helper on the opposite side. Thus the eligible-helper
quotient is a path or cycle. With only one eligible helper on a cycle it has a
loop; with two, its two edges are parallel. Our independent-set convention
for these cases gives only the empty set for a loop; the two maximum
independent sets in the parallel-edge case are the singletons.

Choose the physical side fairly. Conditional on that side, choose J as follows,
independently across auxiliary components:

* On a path choose either parity class of the ordered eligible helpers fairly,
  including the empty class when the order has length one.
* On a cycle with ell eligible helpers choose a uniformly rotated independent
  set of size floor(ell/2), using every rotation with its multiplicity. For
  ell=1 this is the empty set.

Each eligible path helper lies in J with probability 1/2. On a cycle the
probability is p=floor(ell/2)/ell<=1/2. Consecutive eligible helpers are never
both in J.

## 2. Actual one-side sets and their marginals

Include every owner on the chosen physical side. For each helper in J include
both witnesses and omit the helper; include every helper not in J. For each
helper on the opposite physical side, include one witness whose Q-mate was
not double-selected. Such a witness always exists: two blocked witnesses
would require both adjacent eligible helpers in J. At a path endpoint with
one unmatched witness choose the matched witness whenever it is available,
and otherwise the unmatched witness. At an isolated helper choose either
witness fairly. On a cycle, when both witnesses are available choose fairly.
At interior path helpers exactly one witness is available.

Every resulting set is a dissociation set. Selected owners are all on one
physical side, so have no core edges between them. A double-selected witness
has its own owner selected and its helper omitted. A singleton witness has
its helper selected and its owner omitted. The choice avoids Q-edges between
selected witnesses. Included eligible helpers have no selected witness.
These statements also prove compatibility across different auxiliary
components, even if their owners are joined by core edges.

Each owner has marginal 1/2 and each helper has marginal at most one.
We next prove that **each witness has marginal at most 1/2**. Conditional on
its helper being eligible, it is chosen exactly when that helper lies in J,
with probability at most 1/2. Conditional on the opposite side being chosen:

* At an interior helper of a path, its adjacent eligible neighbours lie in
  opposite parity classes. Each witness is forced in one of the two choices,
  so each has probability 1/2.
* At a path endpoint, the neighbouring eligible helper is in J with probability
  1/2. The specified matched-first rule therefore chooses the matched and
  unmatched witnesses each with probability 1/2. An isolated helper is fair
  by definition.
* On a cycle with at least two eligible helpers, the two adjacent J-membership
  events are disjoint and each has probability p. A given witness is forced
  when the other witness is blocked (probability p); if neither is blocked
  (probability 1-2p), it is selected fairly. Its probability is
  p+(1-2p)/2=1/2. For ell=1, J is empty and the fair choice gives the same
  probability directly.

Averaging the two physical-side cases proves the claimed marginal bound.
No independence between different witnesses is assumed.

For a component with h helpers, of which k are eligible, the constructed
size is 3k+2(h-k)+|J|. Averaging over the physical side makes the first two
terms 5h/2. On a path E|J|=h/4. On a cycle E|J|=floor(h/4), equal to h/4
minus 1/2 when h/2 is odd. Let o count those odd quotient cycles. Summing
across the components gives

    E|D_side|=11b/4-o/2.

For arbitrary nonnegative vertex costs w and Phi(D)=|D|-w(D), linearity of
expectation and the marginal bounds now imply

    E Phi(D_side)>=O_bal=11b/4-o/2-w(I)-(w(C)+w(X))/2.       (1)

## 3. Polynomial deterministic choice and the penalty lemma

For each physical side and each auxiliary component enumerate its two path
parity sets or its ell cycle rotations. For a fixed J choose a cheapest
available singleton witness at every opposite-side helper. This choice has
potential at least the random singleton rule, including the matched-first
endpoint rule. Choose a component option of largest potential. The owner
colour is fixed globally, so the independently optimized component options
can be united without conflict. Their potentials add. Comparing the two
resulting global sides therefore gives an actual potential at least (1).
Only the sum of component option counts is enumerated, never their Cartesian
product. Empty components and an empty template cause no exception.

The established phase construction has actual potential at least

    F=5b/2+o/3+sigma+t_g/6-w(I)-(w(C)+w(X))/2.

Its residual solver remains unweighted: if A is the retained owner set and
Z_A an unweighted optimum on it, then w(Z_A)<=w(A). Conditional expectation
on s-w(Y)-w(A) finds such a phase.

Comparing actual candidates, with weights 3/5 and 2/5, gives

    Phi(D)>=13b/5+3sigma/5+t_g/10-w(I)-(w(C)+w(X))/2.       (2)

This is a comparison of valid sets and not a union of a phase set and a side
set. Costs may be arbitrary nonnegative real numbers; code uses exact rationals.

## 4. Actual exterior extension and the 7/71 ledger

Let H be the extracted template in the original graph. Its helper count is
b'=b-b_3. Assign w_v=|N_G(v) outside H|/2. After choosing D in H, delete
its exterior neighbours and take the larger surviving independent side.
This gives a dissociation set of size at least n/2-5b'/2+Phi(D), since the
total number of exterior deletions is at most 2w(D). Repeated exterior
neighbours reduce that number, so incidence counting is safe. With boundary
incidences B_I,B_C,B_X, (2) gives

    beta>=n/2+b'/10+3sigma/5+t_g/10-B_I/2-(B_C+B_X)/4.

Use B_I<=3q, B_C<=2(t_g+t_b), B_X<=2(s_g+s_b), to obtain

    beta>=n/2+b'/10+3sigma/5-2t_g/5-t_b/2
          -(s_g+s_b)/2-3q/2.                             (3)

The retained extension from the two-endpoint proof is a separate actual
full-graph candidate. Write its usual nonnegative surplus as

    Z=5beta-5L-13b'>=3sigma+(3b_G+2t_g)/4,                (4)

where L=|R|-b'+p. The established paired budget is t_b+s_b<=6sigma and
4s_g<=b_G. Its resources are allocated globally only once.

Recall the fixed witness counts m=min(a,p), alpha=a-m, pi=p-m,
e=u-a-2b, r=|R|-a-b, q=n-|S|-p-u, d=|S|-beta, tau=m+b-2d, and b_3.
The nonnegative terms are alpha,pi,r,q,tau,b_3,e-b_3. Put
T=2m+alpha+pi+2e+3b_3. The exact witness identities are

    2beta-n-b'/5=-T+r-q+2Z/5,
    n-10d=m+r+3(alpha+pi)+2e+q+5tau,
    8n-81d=Z+8r+19(alpha+pi)+11e-8b_3+8q+38tau.

Combining the first identity with (3) and then the paired budget gives

 T<=r+2q+2Z/5+4t_g/5+t_b+s_b+s_g-6sigma/5
  <=r+2q+2Z/5+4t_g/5+24sigma/5+b_G/4
  <=r+2q+2Z.                                            (5)

For the last step, (8/5) times (4) supplies
24sigma/5+4t_g/5+6b_G/5, at least the required coefficients.
Thus W2=r+2q+2Z-T>=0. Twice the 8n-81d identity minus twice the
n-10d identity gives the exact equality

 14n-142d=W2+13r+33(alpha+pi)+20(e-b_3)+7b_3+12q+66tau>=0.

Every term is nonnegative. Dividing by two proves the theorem, including
n=0. The argument establishes a uniform bound; it does not establish that
the coefficient is optimal.

## Verification scope

Finite computations support the construction and implementation, while the
preceding arguments prove all orders. The original complete checker uses all minimal selections in its graph controls,
plus the canonical S=I union C selection on each of 5,200 prescribed small
templates. These give 43,756 total selection instances; the templates are
included in that total. All 5,200 use exact unrestricted unweighted beta.
The 5,727 template models receive 28,635 cost assignments, with 103,470
physical phase checks and 76,545 conditional controls. Independent unrestricted
weighted optima cover 580 weighted instances on 116 models of order at most
ten; ten instances on two five-vertex models also use literal subset checks.
Larger templates check actual candidate sets and every phase, without computing
unrestricted large weighted optima. Costs include zero and 2^400/3, whose
numerator has 401 bits. Older imported main suites are not executed.

Separate independent local-support controls check 96 auxiliary path/cycle
shapes and 1,312 physical-side/support cases, through 64 helpers. They check
exact witness marginals and mean sizes, including quotient loops, parallel
edges and endpoints. These finite controls support the construction; the
universal theorem follows from the proof above. No sharpness, Lean or new
grid result is claimed.
