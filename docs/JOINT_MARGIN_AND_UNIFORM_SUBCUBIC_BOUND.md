# A shared-margin repair improves the unrestricted coefficient to 31/314

12 November 2026. Graphs are finite, simple and bipartite. Write beta_2(G)
for the maximum size of a dissociation set (its induced maximum degree is at
most one). A two-star-forming set forms every outside vertex by a not
necessarily induced K_(1,2) having exactly two selected vertices. Minimal
means inclusion-minimal; SF_2(G) is the largest size of such a minimal set.

**Theorem.** If G has maximum degree at most three and order n, then every
minimal two-star-forming set S satisfies

    314(|S|-beta_2(G)) <= 31n.

Consequently SF_2(G)-beta_2(G) <= floor(31n/314). There is no connectivity,
minimum-degree, balance or selected-component hypothesis. The empty graph
is included. The real coefficient improves 8/81 by exactly 1/25434.
Sharpness of the new coefficient is not asserted.

The proof combines actual dissociation sets with a single shared class
budget. The two uses of the template (retained witnesses, or an exterior
independent set) give alternative full-graph constructions.

## 1. Template notation and accepted phase accounting

A partial template H has layers I,C,X of orders b,2b,2b. Each helper i in I
has its assigned pair of X neighbours; these pairs partition X. The owner
edges form a perfect C--X matching. The physical core F=H[C] has maximum
degree two; Q=H[X] is a partial matching. There are no other template edges.
The auxiliary pairing P of helper neighbours is not a physical graph edge.
Every P union Q component is an even path or a cycle of order 4ell. Its two
proper phase classes have equal size. Independently choose one X phase in
each component; its owners are omitted. The complementary owners A have
order b. With a dissociation set Z of F[A], I union Y union Z is dissociation.
An owner's retention literal is the component bit value that retains it.

The accepted cycle accounting in SHARP_ODD_CYCLE_PHASE_COMPENSATION.md
provides a pointwise score supported on full physical core-cycle components.
Its expectation is -rho relative to the baseline 2b/3 for beta_2(F[A]).
Each positive loss is assigned once to one owner phase class U. Monochromatic
cycles contribute delta/2, where delta is their rounding deficit; a C4 uses
exactly |C4|/12, while every other even monochromatic cycle leaves slack at
least 1/2. Each assigned mixed-cycle loss is at most 1/12 and has a supporting
group of at least three vertices of U. All these physical supports are
disjoint. Classes belonging to odd-ell auxiliary cycles are distinguished.
Their orders are 2 mod 4. Define

    B_U = |U|/12 - (1/6 if U is distinguished, else 0),
    M_U = B_U - (actual cycle loss assigned to U),
    sigma = sum_U M_U = b/6-o/3-rho >= 0,

where o counts odd-ell auxiliary cycles. The accepted zero-set classification
says an ordinary class has M_U=0 exactly when it is a union of monochromatic
physical C4 components. A distinguished zero class has such C4s and exactly
two residual vertices. Every bad ordinary class has M_U >= 1/12.

The two accepted one-core-side constructions have maximum size at least
11b/4-o/2. The phase construction has size at least 5b/2+o/3+sigma.
All these are actual sets, not values of an incompatible union.

## 2. Paths and auxiliary defects share one budget

Call an ordinary auxiliary component good when both its owner classes are
unions of monochromatic core C4s. Such a component is isolated within H:
its core edges stay in those C4s and its Q, helper and owner edges stay in
the same component. Let b_G count its helpers over all good components.
Let s_g count good auxiliary paths and s_b the other auxiliary paths.
A good component has a positive number of helpers divisible by four, hence

    4s_g <= b_G.                                           (2)

Assign each bad auxiliary path's one flag to exactly one failing owner
class of that component. Thus each ordinary class has f_U in {0,1}, and
every distinguished class has f_U=0. The sum of these flags is s_b.

For each physical core path, including an isolated vertex, fix one endpoint.
Follow its initial run of vertices having the same retention literal. If
this run has length one or two, call the path good. Retain that run and
omit its next vertex, if present. This event uses at most two fair bits and
is consistent: if the next vertex belongs to the same bit, its opposite
literal automatically omits it. The retained endpoint piece is P1 or P2.
Its rounding surplus above 2|V|/3 is 1/3 or 2/3. The event probability is
at least 1/4, so its expected score is at least 1/12. The rest of that
physical component consists of paths and has nonnegative surplus. Let t_g
count these good physical paths.

For each remaining, bad physical path, assign its first three vertices to
their single owner class U; let p_U count the resulting triples and t_b
count all bad paths. Triple supports are disjoint because the physical
paths are disjoint. They avoid every physical cycle, in particular every
monochromatic cycle and mixed-cycle loss support.

**Shared-margin lemma.**

    2t_b+2s_b <= 24sigma.                                  (3)

**Proof.** Remove the monochromatic cycles of U and let r_U be the number
of residual vertices. Let q_U count its assigned mixed losses. Their
supports avoid the 3p_U path vertices, so

    3q_U <= r_U-3p_U.

For an ordinary class, its residual contribution to M_U is at least
(r_U-q_U)/12 >= p_U/4, and all monochromatic-cycle slack is nonnegative.
If p_U=0, a flag requires a bad ordinary class and hence M_U>=1/12.
If p_U>=1, then 24M_U>=6p_U>=2p_U+2f_U. Thus in either case

    2p_U+2f_U <= 24M_U.

For a distinguished class we claim p_U<=6M_U. If it has a non-C4
monochromatic cycle, its slack at least 1/2 pays the distinguished deduction
1/6 and gives M_U>=1/3+p_U/4, which implies the claim. Otherwise all its
monochromatic cycles are C4s, so r_U=2 mod 4. For p_U>=1, r_U>=max(3p_U,6),
and, using an inequality because actual mixed charges can be smaller,

    M_U >= (r_U-q_U-2)/12.

When p_U=1, r_U>=6 and q_U<=(r_U-3)/3 give M_U>=1/4>=1/6.
When p_U>=2, r_U>=3p_U gives M_U>=(3p_U-2)/12>=p_U/6.
For p_U=0 the claim is immediate. These classes have no flags and satisfy
2p_U<=12M_U. Sum the two class inequalities to obtain (3). This is one
allocation: the margin is not spent independently on the two defect types.

## 3. A strengthened, physically compatible template certificate

Within each good ordinary auxiliary component, choose the better one-side
construction. It has size at least 11b_j/4; a phase restriction there always
has size 5b_j/2, so replacement gains b_j/4. These components have zero
margin and no physical core paths. Remove them, keeping the same sigma and
t_g on the remainder. Add the t_g endpoint-event scores to its accepted
cycle scores. These scores have disjoint physical-component supports;
sharing phase bits does not affect pointwise addition or expectation.
Conditional expectations fix bits without decreasing the score. Exact
optimization on the residual core paths/cycles then gives an actual set
of size at least

    5b/2+o/3+sigma+b_G/4+t_g/12.

All replacements are compatible since their components are isolated in H.
Compare this set and the global one-side alternatives with respective
weights 3/5 and 2/5. The o terms cancel. The largest actual set D satisfies

    5|D| >= 13b+3sigma+(3b_G+t_g)/4.                       (4)

This is a polynomial construction using exact rational event scores. No
finite enumeration is a premise of (3) or (4).

## 4. Ambient boundary and two different ways to extend D

Use the fixed witness extraction for an arbitrary minimal S, as proved in
UNRESTRICTED_SUBCUBIC_GAP_IMPROVEMENT.md. Its selected vertices partition
into R (isolated vertices and isolated edges) and the remaining core.
Choose p disjoint centre--selected-leaf--outside triples using leaves with
a private outside neighbour. After deleting their centres and leaves, pair
each remaining core vertex with its chosen private witness, allowing one
additional selected neighbour only if it is isolated in S. There are u
such pairs. For each selected isolated vertex i, h(i) counts adjacent pair
witnesses; a counts h=1, b counts h>=2, and b_3 counts h=3. The h=2 helpers
I_0 and their assigned owners C_0 and witnesses X_0 form an induced partial
template H with b'=b-b_3 helpers and order 5b'. All these definitions use
one fixed allocation, with both triple centres and selected leaves removed
before residual pairing. In particular |S|=|R|+2p+u.

Every dissociation set of H can be extended by the SAME retained set
(R minus I_0) together with the chosen triple leaves. Its size is

    L=|R|-b'+p.

This compatibility, including all cross-edge exclusions, is part of the
accepted extraction proof. Therefore (4) gives, with beta=beta_2(G),

    Z=5beta-5L-13b' >= 3sigma+(3b_G+t_g)/4.               (5)

For the second extension, count B, the physical edges from H to its
complement. Owners C_0 have their witness already internally; their unused
core-degree slots total 2(t_g+t_b), as every physical core path contributes
two deficits, including an isolated vertex. Thus at most this many edges
leave C_0. Witnesses X_0 have their owner and helper internally; only an
unmatched Q slot can meet the exterior. There are exactly two such slots
per auxiliary path, giving at most 2(s_g+s_b) leaving edges. Finally I_0
is isolated in S. A triple witness has selected neighbourhood exactly its
chosen leaf; every allocated pair witness adjacent to a helper contributes
to its h=2 and is already in X_0. Hence an extra helper neighbour must be
one of the q=n-|S|-p-u unallocated outside vertices. Each such vertex has
degree at most three, giving at most 3q leaving edges. Consequently

    B <= 2(t_g+t_b)+2(s_g+s_b)+3q.                        (6)

Take the actual D in (4). For each of the two ambient bipartition sides,
retain the exterior vertices of that side except neighbours of D. They
form an independent set compatible with D. The sum of their sizes is at
least n-5b'-B, so one gives at least half this many. Using (2), (4) and (6),

 beta >= n/2+b'/10+3sigma/5
                  -(19t_g+2b_G)/20-t_b-s_b-3q/2.         (7)

The sets from (5) and (7) are ALTERNATIVE full-graph candidates. No exterior
set is united with the earlier retained set. Formula (7) remains valid
when its lower bound for the exterior size is negative.

## 5. Exact ledger and the new coefficient

Put d=|S|-beta and use the accepted nonnegative witness slacks

    m=min(a,p), alpha=a-m, pi=p-m,
    e=u-a-2b, r=|R|-a-b, q=n-|S|-p-u,
    tau=m+b-2d, b'=b-b_3.

In particular e>=b_3. The previous witness proof supplies tau>=0 from its
independent deletion constructions, not from the bound being proved here.
Its exact identities, obtained by substituting |S| and n, are

 n-10d=m+r+3(alpha+pi)+2e+q+5tau,
 delta=8n-81d=Z+8r+19(alpha+pi)+11e-8b_3+8q+38tau,
 2beta-n-b'/5=-2m-alpha-pi+r-2e-3b_3-q+2Z/5.

Rearrange (7), use (3), and then (5):

 2m+alpha+pi+2e+3b_3
 <= r+2q+2Z/5+(19t_g+2b_G)/10+2t_b+2s_b-6sigma/5
 <= r+2q+2Z/5+19t_g/10+b_G/5+114sigma/5
 <= r+2q+8Z.                                            (8)

For the last step multiply (5) by 38/5. The sigma and t_g coefficients
are exactly the required 114/5 and 19/10; its b_G coefficient is 57/10,
which exceeds 1/5. Add 2Z/5. Thus every inequality compares proved bounds
on actual sets and uses the shared margin only as in (3).

Define the nonnegative integer

    W=r+2q+8Z-(2m+alpha+pi+2e+3b_3).

Direct substitution into the exact identities yields the certificate

 62n-628d = W+61r+147(alpha+pi)+86(e-b_3)+25b_3+60q+294tau. (9)

All seven summands are nonnegative. Dividing by two proves 314d<=31n.
Taking the largest minimal S and using integrality proves the theorem.

## 6. Implementation and verification scope

`develop/subcubic_joint_margin.py` constructs (4) and both full-graph
extensions, checks each layer's physical boundary, and returns the seven
terms in (9). `scripts/check_joint_margin.py` checks all minimal sets of
its finite graph controls with an independent exact dissociation optimizer;
small partial templates also use a separate private-neighbour formula.
Larger prescribed templates enumerate phase scores and check actual sets,
without claiming unrestricted large optima. Targeted models include mixed
cycle loss, a bad-prefix triple, and an auxiliary-path flag charged to the
same owner class with disjoint supports. Shared bits are allowed throughout.
The computation checks the construction; the general result follows from
Sections 1--5. The exact-source independent review and execution record are
stored separately in `output/joint-margin-review.json` when completed.
