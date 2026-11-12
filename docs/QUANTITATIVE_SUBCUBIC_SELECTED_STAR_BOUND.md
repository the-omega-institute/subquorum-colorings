# A quantitative subcubic selected-star bound

Let G be a nonempty finite simple bipartite graph, with minimum degree
at least two and maximum degree at most three. Let S be an
inclusion-minimal two-star-forming set whose induced components are
stars, single edges or isolates. Formation uses copies of K_(1,2)
which need not be induced. Write beta_2(G) for the unrestricted
dissociation number and d=|S|-beta_2(G).

**Theorem.** Every such selection satisfies

    d <= floor(20|V(G)|/263).                             (1)

The real coefficient 20/263 is strictly smaller than the preceding 1/13
bound in this class. The proof measures defects from the numerical
extremal structure and constructs compatible exchanges on all surviving
private four-cycles. It applies without a connectivity assumption.
For the two-connected subclass the
[compact construction](COMPACT_SUBCUBIC_SELECTED_STAR_GAPS.md) supplies
selected gaps of density 1/64. Thus its best asymptotic coefficient
lies between 1/64 and 20/263. No optimality of either endpoint or upper
bound on unrestricted SF_2 is asserted.

## One fixed witness assignment

We use the assignment and exact ledgers proved in
[Free unused vertices and the degree refinement](FREE_UNUSED_VERTICES_AND_DEGREE_REFINEMENT.md).
There are c selected nontrivial star centres C, e=2c+s selected leaves,
selected isolates I, and m vertices in selected edge components.
Choose one distinct outside deletion witness per leaf, including a
private witness at every clean centre; choose one direct centre witness
at each of the q centres without a clean leaf. A private witness has
only its owner as a selected neighbour. Every chosen witness has exactly
one active selected owner and at most one selected-isolate helper, and
has no other selected neighbour. Let W be this fixed chosen witness set.

For each selected isolate let h(i)=|N(i) intersect W|, and put

    a=#{i:h(i)=1}, b2=#{i:h(i)=2}, b3=#{i:h(i)>=3},
    t=a+b2+b3, z0=#{i:h(i)=0},
    U=V minus (S union W), u=|U|,
    I_+={i in I:h(i)>0},
    Z={v in U:N(v) intersect S is a subset of C union I_+}, g=|Z|.

Let mu be the cardinality of the established compatible centre/helper
repair matching, with capacity one at each centre and each h=2 helper.
The following ledgers all concern this same assignment:

    J=c+s+2q-t-b2-2b3>=0,
    R=c-q+b2+b3-mu>=2d,
    T'=t-s-q, T'-g>=2d,
    b2<=(s+q)/2+mu,
    H=b3+mu,
    2c=J+R+T'+H,                                      (2)
    n=(5/2)J+(5/2)R+(7/2)T'+(5/2)H
        +3s+2q+m+z0+u.                                (3)

The minimum/maximum-degree cut at two and three gives

    a<=2u+g,
    2d<=a+H-(s+q)/2-g.                                (4)

The first counts edges from h=1 isolates into U: a nonfree U vertex
spends at least one of its three degree slots on another selected type;
a free vertex can spend three on these isolates. The second is the
strong colour exchange with free vertices added. The derivation of (2)-(4)
is in the linked proof; no witness or unused vertex is reassigned here.

Assume d>0 and define the nonnegative slacks

    r=R-2d, x=T'-g-2d, eta=n-13d.

Equation (4) gives u-d>=-H/2+(s+q)/4. Substituting in (3) yields

    eta >= (5/2)(J+r)+(7/2)(g+x)+2H
              +(13/4)s+(9/4)q+m+z0.                  (5)

In particular eta>=0. We next show that every selected gap consumes
a controlled amount of this nonnegative remainder.

## Find many six-vertex blocks

Call a centre preliminary-good if its selected star is P_3, it is
clean, and its two chosen leaf witnesses consist of one private witness
a_j and one helped witness b_j whose helper i_j has h(i_j)=1. Label
the block

    a_j - x_j - c_j - y_j - b_j - i_j,

where x_j,c_j,y_j,i_j are selected. This path need not be an induced
component of G. Distinct preliminary-good blocks are vertex-disjoint:
their stars and witnesses are distinct, and their helpers have exactly
one W-neighbour. Let c0 count these blocks and b=c-c0 the other centres.

At most s selected stars are larger than P_3 and q are nonclean. The
union of these exceptions has at most s+q centres and at most
2(s+q)+s=3s+2q leaves. Their leaf witnesses and the q direct witnesses
can therefore account for at most 3s+3q h=1 helpers. At any remaining
clean P_3, one witness is private, so at most one witness can have an
h=1 helper; if it does, that centre is preliminary-good. Each h=1
isolate has its unique W-neighbour, and every witness supports at most
one helper. This injective count proves

    c0>=a-3s-3q, hence b<=c-a+3s+3q.                   (6)

By (2), c=2d+(J+r+g+x+H)/2. The lower bound for a in (4) gives

    c-a <= (J+r+x-g)/2+(3/2)H-(s+q)/2.

Consequently a convenient conservative form of (6) is

    b <= (J+r+x)/2+(3/2)H+(5/2)(s+q).                   (7)

All terms discarded in this step have the appropriate nonpositive sign.

## Recover private four-cycles

Let A consist of the c0 private witnesses in preliminary-good blocks.
The bipartite induced graph G[A] has maximum degree at most two:
each private witness has its selected owner in addition to any A-neighbours,
and the full graph has maximum degree three.

From S omit x_j at every preliminary-good star and the centre at every
other selected star. Retain all selected isolates and edge components.
The result is dissociation of size |S|-c: each preliminary-good star
retains the edge c_j y_j; every other star retains independent leaves.
Each private a_j has its only selected neighbour x_j omitted. Therefore
any dissociation set of G[A] can be added, giving

    beta_2(G[A]) <= c-d.                               (8)

For any bipartite graph R of maximum degree two, let v count the
vertices outside its C_4 components. Then

    beta_2(R) >= |V(R)|/2+v/10.                         (9)

Indeed its components are paths or even cycles. For a path of order l,
beta_2=ceil(2l/3); for an even cycle of order l, beta_2=floor(2l/3).
Partitioning paths into consecutive triples and taking the initial
segment of the word 110110... proves the path formula. Summing the
inequality at all cyclic triples proves the cycle upper bound; attaining
cyclic words for l=3q,3q+1,3q+2 are respectively (110)^q,
(110)^(q-1)1100 and (110)^q10. Paths exceed half their order by at
least l/6. For cycles l=6,8 the bound (9) follows by direct substitution;
for l>=10, floor(2l/3)>=2l/3-2/3>=3l/5. C_4 contributes exactly half
its order. Adding these component estimates proves (9), with the margin
1/10 attained on C_10.

Let v now refer to G[A]. Equations (8)-(9), and c0=c-b, imply

    v <= 10(c-d-c0/2)=5(c-2d+b).                        (10)

Call the c0-v blocks whose private vertices lie in C_4 components
final-good. Each such private vertex has one owner edge and two cycle
edges, filling all three of its degree slots. It has no other neighbours.
Each associated helped witness has its selected owner and unique h=1
helper, so at most one further neighbour. The graph induced by the
final-good helped witnesses is consequently a matching plus isolates.

## Simultaneous exchanges with one capacity per witness

Contract each private C_4 to a vertex, and put an edge between the
corresponding cycles for every matching edge b_j b_l. Loops and parallel
edges are allowed; loops contribute two to degree. This quotient has
maximum degree four because every cycle supplies four distinct blocks
and each helped witness lies on at most one matching edge.

Orient it with indegree at most two. To obtain such an orientation,
pair its odd-degree vertices with added edges. Each odd degree is at
most three, so the augmented degrees are even and at most four.
Orient Euler tours in each component, and then discard the added edges.
A loop gives one incoming incidence. Every original indegree is at
most two.

For an oriented matching edge put its head block in state A_j below.
The prescribed A blocks in each cycle are distinct and at most two;
fill further positions to obtain exactly two per cycle. Put the other
blocks in state B_j:

    A_j={a_j,c_j,y_j,i_j},
    B_j={x_j,c_j,b_j,i_j}.                              (11)

The two retained private vertices in a cycle induce at most one edge.
Every helped matching edge has at least one A endpoint, so it never
joins two retained helped witnesses. The private vertices have no
neighbours outside their own cycle and omitted owner. A retained helped
witness is paired with its helper, its owner is omitted, and its helper
has no other W-neighbour. Thus these choices are mutually compatible.

Keep all original selected vertices outside the final-good stars,
except omit the centre of every other selected star. Keep every selected
isolate and edge component. No newly retained witness meets another
active selected owner or an additional selected helper. This accounts
for every possible new edge and proves the whole set is dissociation.
Each final-good star loses one leaf and gains one witness, with its
helper already counted in S. Each other star loses exactly one centre.
The resulting set therefore has |S|-(b+v) vertices. In particular

    d<=b+v.                                           (12)

Every matching endpoint is used once in this simultaneous construction.
Neither a helper nor a private-cycle position is allocated twice.

## Close the quantitative estimate

Using (7),(10),(12) and c-2d=(J+r+g+x+H)/2 gives

    d <= 6b+5(c-2d)
      <= (11/2)(J+r)+(5/2)g+(11/2)x
           +(23/2)H+15s+15q.                          (13)

Every coefficient in (13) is at most 20/3 times the corresponding
coefficient in (5). For J,r,g,x,H,s,q the pairs of coefficients are

| Quantity | In (13) | 20/3 times (5) |
|---|---:|---:|
| J,r | 11/2 | 50/3 |
| g | 5/2 | 70/3 |
| x | 11/2 | 70/3 |
| H | 23/2 | 40/3 |
| s | 15 | 65/3 |
| q | 15 | 15 |

The m,z0 coefficients in (13) vanish. Hence 3d<=20eta=20(n-13d), or
263d<=20n. Integrality proves (1). If d<=0 the conclusion holds directly.
This proves a strict improvement of the real coefficient, rather than
just exclusion of exact n=13d equality.

## Verification

Run `python3 -B scripts/check_subcubic_star_stability.py`.
It constructs both physical exchanges from actual permitted witness
assignments; optimizes the private graph independently; and checks the
nonnegative remainder and final coefficient using integer arithmetic.
Its small graph range enumerates all selected sets and permitted witness
assignments for every graph of minimum degree two and maximum degree
three with fixed bipartition sizes (2,2),(2,3),(3,3),(3,4).
Separate kernel controls exercise arbitrary partial helped matchings,
quotient loops, odd degrees and isolated helped vertices, including full
enumeration at one and two private cycles. A separately exact 64-vertex
positive-gap graph checks the theorem outside the small zero-gap range.
The general theorem rests on (2)-(13); finite verification checks the
construction and accounting. No Lean validation or sharpness assertion
is made.
