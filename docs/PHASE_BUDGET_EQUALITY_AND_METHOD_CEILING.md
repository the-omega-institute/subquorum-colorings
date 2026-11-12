# Equality budgets, an integer refinement, and a ceiling of the constructions

12 November2026. Graphs are finite, simple and bipartite. beta_2 is
unrestricted dissociation and SF_2 is maximum cardinality among
inclusion-minimal two-star-forming sets. Formation uses non-induced
K_(1,2) with exactly two selected vertices.

## 1. The exact residual budget and its zero set

Use the fixed partial template and cycle pairing in
SHARP_ODD_CYCLE_PHASE_COMPENSATION.md. Let b be its number of helpers,
o its number of odd-ell auxiliary cycles, and rho the sum of expected
uncancelled core-cycle losses. Put

    sigma=b/6-o/3-rho>=0.

For each owner phase class U, let M_U be its monochromatic core-cycle
vertices and r_U=|U minus M_U|. A class is distinguished when it belongs
to an odd-ell auxiliary cycle; its size is2 modulo4. Other classes are
ordinary, including auxiliary-path classes of possibly odd size.

**Theorem1 (exact zero budget).** sigma=0 if and only if:

* Every ordinary class is partitioned into whole monochromatic C4
  components of the physical core.
* Every distinguished class consists of such C4 components and exactly
  two remaining vertices.

The two remaining vertices need not be adjacent or form one path. The
statement does not specify how they connect to other classes. It does
not classify equality in the actual residual dissociation number.

More quantitatively, let N_O and N_D count violations of these two class
conditions, respectively. Then

    sigma>=N_O/12+N_D/6.                                (1)

**Proof.** A monochromatic core cycle K of order m has loss delta/2,
where delta is its floor deficit relative to2m/3. For C4 its loss is
exactly m/12=1/3. Every other even cycle has slack at least1/2 between
m/12 and its loss; lengths6,8,10 attain that minimum.

Assign each positive mixed-cycle loss once to a residue0mod3 group,
using at least three vertices of U, as in the preceding proof. If q_U
losses are assigned to U, their supports are physically disjoint, so
3q_U<=r_U and each costs at most1/12.

For an ordinary class, the margin between its budget |U|/12 and its
charge is at least

    sum_(monochromatic K in U)(|K|/12-loss(K))+(r_U-q_U)/12.

If a non-C4 monochromatic cycle occurs the margin is at least1/2.
Otherwise r_U=0 gives margin0, while r_U>=1 gives margin at least1/12:
q_U<=floor(r_U/3), hence r_U-q_U>=1. Thus an ordinary class has zero
margin exactly when it is partitioned into monochromatic C4s, and any
violation costs at least1/12.

For a distinguished class the budget is(|U|-2)/12. If a monochromatic
non-C4 occurs, its1/2 slack minus the1/6 reserve gives margin at least1/3.
Otherwise all removed cycles are C4 and r_U=2mod4, hence r_U>=2.
For r_U=2 we have q_U=0 and margin0. For r_U>=6,

    (r_U-q_U-2)/12>=(r_U-floor(r_U/3)-2)/12>=1/6.

These exhaust the cases. Summing margins over the partition of C equals
sigma exactly, since every loss was assigned once. This proves(1) and
the exact zero set, independently of which eligible mixed support was chosen.
If every class satisfies the conditions, there is no room for a mixed
support of size>=3, so only the enumerated C4 losses remain. QED.

## 2. Strengthened certificates and near-equality constraints

**Theorem2.** The existing physical constructions already guarantee

    beta_2(template)>=ceil((13b+3sigma)/5).               (2)

For the same fixed extraction from an arbitrary minimal S in a graph G
of maximum degree at most three, with b now the original witness count
and b'=b-b3 the template helper count, compute sigma on that template.
Then

    81(|S|-beta_2(G))<=8n-3sigma
                      <=8n-(N_O+2N_D)/4.                (3)

**Proof.** The cycle score gives
E beta_2(F[A])>=2b/3-rho=b/2+o/3+sigma. Conditional expectations produce
an actual phase set of size at least5b/2+o/3+sigma. Compare it with the
one-side guarantee5b/2+b/4-o/2, using weights3/5 and2/5, respectively.
This proves(2), without adding incompatible sets or changing the previous
phase algorithm.

Use L=|R|-b'+p and all the original nonnegative slacks. Put

    Z_sigma=5beta_2(G)-5L-13b'-3sigma>=0.

The already proved identity becomes

 8n-81d = Z_sigma+3sigma+8r+19alpha+19pi+3e
                         +8(e-b3)+8q+38tau.             (4)

All displayed terms are nonnegative, proving(3). The class budgets use
disjoint physical vertices; the lifting retains all R outside the template
and every chosen triple leaf simultaneously, as proved previously. QED.

If sigma>0, integrality gives d<=ceil(8n/81)-1. More generally, if the
unrounded deficit8n-81d is at most epsilon, then

    N_O+2N_D<=4epsilon,
    r,q<=epsilon/8, alpha,pi<=epsilon/19,
    e<=epsilon/3, e-b3<=epsilon/8, tau<=epsilon/38.

These count class violations and fixed witness slacks. No vertex-edit
distance or sharp asymptotic stability claim is made.

## 3. A new unconditional integer refinement

**Theorem3.** Every nonempty bipartite maximum-degree-three graph satisfies

 SF_2(G)-beta_2(G)<=floor(8n/81)-1_(n=81 mod162).           (5)

If positive unrounded equality81d=8n occurs for a minimal S, there is an
integer k>=1 for which

 n=162k, d=16k, a=p=2k, b=30k, b3=0,
 u=62k, |R|=32k, |S|=98k, beta_2(G)=82k.                 (6)

The owner classes obey Theorem1. These are necessary conditions, not an
existence theorem or a classification of all equality graphs.

**Proof.** Equality in(4) forces sigma=Z_sigma=r=alpha=pi=e=q=tau=0 and
b3=0. Thus a=p=m. The exact identity from the previous proof,

    d+Z=8m+5alpha+5pi+2tau+5e+8b3,
    Z=5beta_2(G)-5L-13b',

gives d=8m. Hence b=2d-m=15m, u=a+2b=31m, |R|=a+b=16m,
|S|=|R|+2p+u=49m, beta_2=41m and n=81m.

By Theorem1 every ordinary owner class has order divisible by4.
In particular, an auxiliary path on2h witness vertices has owner classes
of order h, so h is divisible by4. Auxiliary cycles contribute2ell helpers,
an even number. Summing over all auxiliary components, b' is even. Since
b3=0, b=15m is even, and m=2k. Positive equality gives k>=1 and(6).
Consequently equality is impossible for n=81mod162; integrality subtracts
one from the prior floor bound exactly at those orders. QED.

## 4. A connected50vertex ceiling for all three construction families

**Theorem4.** There is a connected50vertex partial-template graph with
b10,o3, perfect Q, bipartition25+25 and all degrees2 on I and3 on C union X
such that:

* Either optimized one-core-side QUOTIENT construction has maximum26.
* Every full auxiliary phase, with an optimal residual core set, has26.
* A separate explicit dissociation set has27.

Thus even optimal phases, optimized quotient choices, and choosing these
families independently by connected component cannot replace13b/5 by a
larger universal coefficient. This is a ceiling for these specified
construction families, not an upper bound on unrestricted dissociation.
The graph coefficient8/81 and the optimal template coefficient remain open.

**Construction.** Start with the explicit30vertex fixture from the preceding
note. It has helpers0..5, witnesses6..17, owners18..29, the listed core
C6s and interface edges(6,9),(7,8),(10,13),(11,12),(14,17),(15,16).
Delete(6,9). Add witnesses30..37, owners38..45 and helpers46..49.
For j0..7 join30+j to38+j and to46+floor(j/2). Add interface edges

    (9,30),(31,32),(33,34),(35,36),(37,6).

Finally add the core squares

    (38,40,42,44), (39,41,43,45).

All old edges except(6,9) remain. Give30+j original colour floor(j/2)mod2,
its owner the opposite colour, and its helper the colour opposite its
witnesses. These colours agree with both inserted interface boundary edges.
The replaced auxiliary4cycle is now a12cycle; the other two stay4cycles.
The new squares are each wholly in one phase class of the12cycle.
All graph and selected-set minimality conditions follow from the template:
each witness has exactly its helper and owner as selected neighbours;
removing a helper fails at itself, and removing an owner fails at its witness.
The old core has degree2, so the latter witness's remaining helper is an
isolate in the deleted selected graph.

**Proof of the ceiling.** In either one-core-side construction, the base
is25. Quotient lengths are3,1,1; their optimized gains are1,0,0 by the
cyclic-run argument, including the loop cases. Hence the exact maximum
within each specified quotient family is26.

The insertion preserves the old owner phases on the30vertex core. In
every phase that core leaves2P3 with dissociation4, by the explicit
transitive core automorphisms proved previously. Exactly one of the two
new squares is retained, adding dissociation2. Thus the residual core
has optimum6 in EVERY phase. Adding ten helpers and ten chosen witnesses
gives26. No tie-breaking or exhaustive phase optimization improves it.

An explicit27set is

 {0,1,3,4,5,6,8,10,11,14,16,19,22,23,24,25,27,
  30,32,34,36,39,41,46,47,48,49}.

Its old17vertices are the preceding fixture's dissociation witness. Its
new part comprises four helper--witness edges and the core edge(39,41).
The only new-to-old boundary edges are(9,30) and(6,37): vertex9 and vertex37
are both omitted, so neither creates an additional selected edge. Hence
all selected degrees are at most one. This proves the asserted lower
witness, without computing the unrestricted optimum.

Unions of t copies give n50t,b10t, construction maximum26t and an explicit
27t-set for EVERY integer t>=1. Each connected component is the obstructing
50vertex graph. This proves an all-scale failure of the construction rule,
including optimizations applied separately to each connected component.
No connected50t family for t>1 or exact unrestricted beta is claimed.

The new class-slack correction sigma is zero on this graph: the elongated
odd component has one C4 and two residual vertices in each class, and the
other distinguished classes each have their two residual vertices. Thus
this example also explains the limit of the zero-budget classification:
sigma=0 is a precise counting equality, not actual graph optimality.
