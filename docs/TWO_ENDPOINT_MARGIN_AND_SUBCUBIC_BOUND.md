# Two endpoint credits and paired margins give the unrestricted15/152 bound

12 November2026. All graphs are finite, simple and bipartite. beta_2(G)
is the maximum size of a set inducing maximum degree at most one. A
minimal two-star-forming set is inclusion-minimal and forms every outside
vertex by a not necessarily induced K_(1,2) with exactly two selected vertices.

**Theorem.** For every graph G of maximum degree at most three and every
minimal two-star-forming set S,

    152(|S|-beta_2(G)) <= 15|V(G)|.

Consequently SF_2(G)-beta_2(G)<=floor(15n/152). The theorem includes the
empty graph and has no connectivity, minimum-degree, side-balance or
selected-component condition. The coefficient improves31/314 by1/23864
and8/81 by1/12312. Optimality and attainment are open.

The preceding JOINT_MARGIN_AND_UNIFORM_SUBCUBIC_BOUND.md proves the fixed
witness extraction, physical boundary estimate, retained-set compatibility,
class-margin accounting and a31/314 certificate. The present proof keeps
those ingredients and improves BOTH the path credit and the shared budget.
The current meaning of a good PHYSICAL path is changed explicitly below.

## 1. Common template data

A partial template H has disjoint layers I,C,X of orders b,2b,2b. The
helper pairs partition X, the owner C--X matching is perfect, the physical
core F=H[C] has maximum degree two, and the physical interface Q=H[X]
is a partial matching. There are no other edges. Auxiliary P pairs the
two witnesses of each helper; P is not a physical graph edge. P union Q
components are even paths or cycles of order4ell. Each has a fair phase
bit, choosing half its witnesses and retaining the complementary owners.
For the retained b owners A, any dissociation set Z in F[A] gives an actual
set I union Y union Z in H. An owner's retention literal specifies its
auxiliary component bit and its retaining value.

The accepted core-cycle score has expectation-rho relative to2b/3 and
has pointwise support only on full physical core-cycle components. Its
losses are assigned once to owner phase classes. A monochromatic core C4
uses its exact vertex budget |C4|/12. Every other even monochromatic core
cycle leaves at least1/2 of slack. An assigned mixed-cycle loss costs at
most1/12 and uses at least three vertices of the class. These mixed supports
are disjoint physical groups in different full core cycles. An auxiliary
odd-ell cycle has two distinguished owner classes, each of order2mod4.
Other classes, including all auxiliary-path classes, are ordinary.

For a class U define its actual margin

    M_U=|U|/12-1_(distinguished)/6-(loss assigned to U).

The accepted accounting gives M_U>=0 and

    sum M_U = sigma = b/6-o/3-rho,

where o counts odd-ell auxiliary cycles. An ordinary class has zero margin
exactly when it is a union of whole monochromatic core C4s; any other
ordinary class has margin at least1/12. A distinguished zero class consists
of such C4s and two residual vertices. The two classes belonging to ANY
auxiliary component have the SAME order h.

Call an ordinary AUXILIARY component good when both classes are unions
of whole monochromatic core C4s. Its template vertices are isolated from
the other template vertices: all core edges stay within those full C4s,
and helper/owner/interface edges stay in its auxiliary component. Let b_G
count its helpers. Let s_g count good auxiliary paths and s_b bad auxiliary
paths. Since every good component has positive helper order divisible by4,

    4s_g<=b_G.                                             (1)

Assign ONE flag to each bad auxiliary path, never one per class. No cycle
component needs a flag. Thus the number of flags is s_b.

## 2. Two endpoints of a physical core path

A physical core path K is good if BOTH endpoint runs of equal retention
literals have length at most two. An isolated vertex is good. Otherwise
call it bad and choose ONE endpoint whose initial literal run has length
at least three. Allocate its first three vertices to their single owner
class U; let p_U count allocated triples. Let t_g,t_b count good and bad
physical paths, respectively. Even if a bad path has two bad endpoints,
it contributes ONE triple. These triples are disjoint across physical
paths and avoid all full core-cycle loss supports.

**Two-endpoint lemma.** Every good physical path contributes an endpoint
event score with expected rounding surplus at least1/6 over2|A intersect K|/3.
These scores can be added pointwise to each other and to the cycle scores.

**Proof.** For an endpoint whose initial run has length one or two, retain
that run and omit its next vertex if present. The requirements specify at
most two bits and are consistent; when the next vertex uses the same bit,
its different literal automatically makes it omitted. The retained prefix
is a full residual P1 or P2 component. Its surplus is1/3 or2/3, respectively.
The event probability is at least1/4.

For |K|>=3 use both endpoint events. Whenever both fire, they describe
DIFFERENT residual path components. Indeed, a residual component containing
both physical endpoints would be the entire physical path, of order at
least three; each specified endpoint component has order at most two.
Consequently the two active pieces neither overlap nor have a retained
edge between them. Their surpluses add, and every other residual path piece
has nonnegative rounding surplus. Each endpoint event has expectation at
least1/12, giving at least1/6 together.

For P1 use its sole retention event once: expected surplus1/6. For P2 with
identical literals use its whole-path event ONCE, with expected surplus1/3.
If its literals differ, the two endpoint-isolation events are disjoint,
consistent, and each has probability at least1/4 and surplus1/3. Thus their
total expectation is at least1/6. This also includes opposite values of the
same bit, whose two isolation events each have probability1/2.

Different physical paths have disjoint vertices, and physical paths avoid
full physical core cycles. Thus all these scores add pointwise. Their bits
may coincide; no independence between score events is required. QED.

## 3. The sharper shared budget

**Paired-margin lemma.** With the above one-triple-per-bad-path allocation,

    2t_b+2s_b <= 12sigma.                                  (2)

**Proof.** For each U remove all its monochromatic core cycles and let r_U
count its residual vertices. If q_U mixed losses are assigned there, their
physical supports avoid the 3p_U path vertices, so3q_U<=r_U-3p_U. Ordinary
classes satisfy

    M_U>=sum_(monochromatic K)(|K|/12-loss(K))+(r_U-q_U)/12
       >=p_U/4.                                           (3)

Distinguished classes satisfy p_U<=6M_U by the same class calculation as
in the preceding proof: a non-C4 monochromatic cycle gives
M_U>=1/3+p_U/4; otherwise r_U=2mod4 and
M_U>=(r_U-q_U-2)/12. For p_U=1, r_U>=6 gives M_U>=1/4.
For p_U>=2, r_U>=3p_U gives M_U>=(3p_U-2)/12>=p_U/6.
For p_U=0 the claim follows from M_U>=0. Their contribution is therefore
2p_U<=12M_U and they have no flags.

For an ordinary auxiliary component, combine its TWO class margins
M_0+M_1, and put p=p_0+p_1. Without a flag, (3) gives
12(M_0+M_1)>=3p>=2p. In particular this pays every ordinary cycle and every
good auxiliary path. Suppose the component is a bad auxiliary path, with
one flag. We prove12(M_0+M_1)>=2p+2:

* If p>=2, (3) gives3p>=2p+2.
* If p=1, consider the class containing the triple. A non-C4 monochromatic
  cycle gives margin at least1/2 even before its residual vertices, already
  enough. Otherwise every removed monochromatic cycle is C4. If the common
  class order h is0mod4, the residual order is a positive multiple of4 and
  at least4;3q_U<=r_U-3 implies r_U-q_U>=4, so M_U>=1/3. If h is not0mod4,
  the OTHER class cannot consist only of C4s; it contributes at least1/12,
  in addition to the first class's margin at least1/4 from(3). Again their
  sum is at least1/3, and12 times this pays2p+2=4.
* If p=0, two bad classes give margins at least1/12 each, paying the flag.
  If exactly one class is bad, the good one forces h=0mod4. The bad one
  either has a non-C4 monochromatic cycle with slack at least1/2, or has
  residual r_U>=4 divisible by4. Then3q_U<=r_U and r_U-q_U>=3 give margin
  at least1/4. This also pays the sole flag.

These cases exhaust p and the possible class conditions. Sum ONCE over
ordinary auxiliary components and distinguished classes. Owner classes
partition C, each triple is assigned once, and each bad auxiliary path
has one flag. This proves(2) without a second use of any margin. QED.

## 4. Compatible template and ambient constructions

Good auxiliary components have zero margin and no physical core paths.
Remove them and replace their phase restrictions by their optimized
one-side alternatives, gaining b_G/4. On the remainder add the endpoint
scores of Section2 to the accepted cycle scores. Conditional expectations
fix all fair phase bits without decreasing the sum of the scores. Exact
residual path/cycle optimization and the compatible good-component sets
give an actual dissociation set of size at least

    5b/2+o/3+sigma+b_G/4+t_g/6.

Compare with the accepted global one-side guarantee11b/4-o/2, taking
weights3/5 and2/5. The larger actual set D satisfies

    5|D|>=13b+3sigma+(3b_G+2t_g)/4.                        (4)

For a minimal S in an ambient graph G, use the fixed extraction and counts
of the preceding proof. Explicitly, R consists of selected isolated
vertices and selected isolated edges. There are p disjoint selected
centre--selected leaf--private outside witness triples; after deleting
both selected vertices of each triple, the u remaining selected core
vertices have distinct pair witnesses. For a selected isolate i, h(i)
counts its pair-witness neighbours. Let a count h=1, b count h>=2, and b_3
count h=3. The h=2 helpers I_0 and their pair witnesses X_0 and owners C_0
induce H with b'=b-b_3 helpers and order5b'. The exact identities include
|S|=|R|+2p+u. Every dissociation set of H extends by the SAME retained
(R minus I_0) and chosen triple leaves, of size L=|R|-b'+p. Thus, writing
beta=beta_2(G),

    Z=5beta-5L-13b'>=3sigma+(3b_G+2t_g)/4.                (5)

Physical boundary accounting is unchanged: the t_g+t_b core paths give
at most2(t_g+t_b) owner boundary slots; the s_g+s_b auxiliary paths give
at most2(s_g+s_b) witness boundary slots. The helpers can have extra
neighbours only among q=n-|S|-p-u unallocated outside vertices, giving
at most3q helper boundary incidences. An allocated triple witness has only
its selected leaf as selected neighbour. An allocated pair witness meeting
an h=2 helper is already its template witness. Hence

    B<=2(t_g+t_b)+2(s_g+s_b)+3q.

For the actual D of(4), remove its neighbours from each exterior
bipartition side. These are two independent sets each compatible with D,
with sizes summing to at least n-5b'-B. Choose the larger side and use(1):

 beta>=n/2+b'/10+3sigma/5-(18t_g+2b_G)/20-t_b-s_b-3q/2.   (6)

This is an alternative to the earlier retained-set extension, not a union
with it. Both are genuine full-graph constructions. Negative lower bounds
for the exterior size cause no difficulty.

## 5. Final certificate

Set d=|S|-beta and use the nonnegative slacks from the accepted fixed
witness extraction:

    m=min(a,p), alpha=a-m, pi=p-m,
    e=u-a-2b, r=|R|-a-b, q=n-|S|-p-u,
    tau=m+b-2d, b'=b-b_3, e>=b_3.

The independent deletion exchanges already prove tau>=0. The exact witness
identities are

 n-10d=m+r+3(alpha+pi)+2e+q+5tau,
 8n-81d=Z+8r+19(alpha+pi)+11e-8b_3+8q+38tau,
 2beta-n-b'/5=-2m-alpha-pi+r-2e-3b_3-q+2Z/5.

Combine the last identity with(6), then(2):

 2m+alpha+pi+2e+3b_3
 <=r+2q+2Z/5+(18t_g+2b_G)/10+2t_b+2s_b-6sigma/5
 <=r+2q+2Z/5+9t_g/5+b_G/5+54sigma/5
 <=r+2q+4Z.                                              (7)

For the last step multiply(5) by18/5. This supplies exactly54sigma/5
and9t_g/5; its b_G coefficient27/10 exceeds1/5. Add2Z/5.
Therefore W_4=r+2q+4Z-(2m+alpha+pi+2e+3b_3) is nonnegative. Substitution
in the exact witness identities gives

 30n-304d=W_4+29r+71(alpha+pi)+42(e-b_3)+13b_3+28q+142tau. (8)

All seven summands are nonnegative. Divide by two, then maximize over
minimal S and use integrality. This proves the theorem, including n=0.

## 6. Code and verification

`develop/subcubic_two_endpoint.py` implements both endpoint events (deduplicating
whole P1/P2 events), assigns only one triple per bad physical path, sums
ordinary class margins per auxiliary component, and builds(4) plus both
full-graph extensions. It returns the exact seven terms of(8).

`scripts/check_two_endpoint.py` checks all minimal sets in its finite graph
controls, independent exact small-template optima, all phases on larger
prescribed templates, actual simultaneous endpoint-piece disjointness and
all three physical boundary layers. An independent literal-path calculation
classifies all signed literal words through path order six; every phase of
each good word is checked for the pointwise endpoint-score inequality.
Bad words receive zero endpoint score, and their residual path pieces have
nonnegative rounding surplus by the general proof. These finite
controls corroborate the general proofs above. They do not replace them,
compute unrestricted large-template optima, establish sharpness or settle
the separate cubic/grid questions. The independent exact-source review is
recorded separately in `output/two-endpoint-review.json` when completed.
