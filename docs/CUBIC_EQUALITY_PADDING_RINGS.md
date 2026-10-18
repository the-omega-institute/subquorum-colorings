# Two cut pairs without shared compensation: cubic equality rings

19 October 2026. Graphs are finite, simple, cubic and bipartite;
star formation is non-induced and minimality is by inclusion. This
extends the [single-obstruction padding construction](CUBIC_STABILITY_PORTS.md)
from a fixed gap of one to unbounded gaps while preserving equality in
7SF_2<=3n+2beta_2. It does not improve the best already constructed
asymptotic cubic gap coefficient1/28. No priority claim is made.

## A two-parameter exact family

Theorem. For every r>=1 and positive integers k_1,...,k_r there is a
two-connected cubic bipartite graph R with, writing K=sum_i k_i,

    n=14r+20K,
    beta_2(R)=7r+12K,
    SF_2(R)=8r+12K,
    SF_2(R)-beta_2(R)=r,
    7SF_2(R)=3n+2beta_2(R).                                (1)

Also Gamma(R)=alpha(R)=n/2 by the established regular bipartite
comparison. For k_i=1 this gives gap n/34 and unbounded gaps at linear
compensation equality. Letting both r and the k_i grow gives unbounded
gap while SF_2/n tends to3/5. The previous padding family had the
latter limiting ratio with gap fixed at one.

The new ingredient is an all-length four-port lemma. Its elementary
weighted identity excludes using a second cut to recover the deficit
forced by the first cut. No port restriction is counted twice.

## The periodic equality core with two cut edges

Recall C_k on20kvertices, with m=6k and classes H,U,X,Y:

    H={h_i:0<=i<m}, U={u_i:0<=i<m}, X={x_i:0<=i<m},
    Y={y_(2b),y_(2b+1):0<=b<k}.

H and X induce cycles in their index order. Add h_i--u_i--x_i,
and join u_(6b+j) to y_(2b+(j mod2)). Indices on the cycles are modulo m.
Use the bipartition with h_i,x_i of color i mod2, u_i of the other
color, and y_j of color j mod2. The existing proof gives two-connectivity,
beta_2(C_k)=SF_2(C_k)=12k, and the minimal selection H union U.

Delete the two disjoint edges

    e0=x_0--x_1,       e2=x_2--x_3,

and call the result Q_k. The four ports have degree two; all other
vertices have degree three.

Lemma. Every dissociation set D in Q_k has size at most12k. If D
omits both endpoints of either e0 or e2, then |D|<=12k-1.

First recall the exact deficiency identity. For any graph F with
maximum degree at most three, put N=|V(F)|,
R=sum_v(3-deg_F(v)), R_D=sum_(v in D)(3-deg_F(v)). If D is dissociating,
let i_D count its isolated vertices and e_T the edges inside its
complement. The two cut counts give the exact identity

    3N-5|D|-R+2R_D=i_D+2e_T.                              (2)

Indeed, the D-side cut has size2|D|-R_D+i_D, whereas the complement
side gives3(N-|D|)-(R-R_D)-2e_T. Thus (2) follows without assigning
any port capacity to more than its actual vertex.

For Q_k, N=20k,R=4 and R_D=p, the number of selected ports. Hence
5|D|<=60k-4+2p<=60k+4, so |D|<=12k. Suppose both endpoints of e0
are omitted and |D|=12k. Then p<=2, and (2) reads

    2p-4=i_D+2e_T>=0.

Thus p=2, both e2 ports belong to D, D induces a perfect matching,
and its complement is independent in Q_k. These consequences are
simultaneous equalities, not independent reusable capacities.

## A six-periodic weight proves the strict loss

Assign the following integer weights, repeated in every block of six
indices, and give every Y vertex weight zero.

| Index modulo six | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| w(h_i) | 1 | 0 | 0 | -1 | 2 | -2 |
| w(u_i) | 0 | -1 | 1 | 0 | -1 | 1 |
| w(x_i) | -1 | 2 | -2 | 1 | 0 | 0 |

In the uncut C_k these weights satisfy

    sum_(v in N(a)) w(v)+2w(a)=0       for every a,
    sum_a w(a)=0.                                         (3)

For H and X this is direct substitution of their two cyclic neighbors
and their U neighbor. For U use its H,X and zero-weight Y neighbors.
For a Y vertex, the three incident U weights sum to zero, both for
even and odd indices. The cycle wrap respects the same six-periodic
table because m is divisible by six. This proves (3) for every k.

Let d(a) be the indicator of D. Under the equality consequences above,
restoring the two cut edges gives, in the uncut core,

    |N_(C_k)(a) intersect D|+2d(a)
      =3-1_(a in endpoints(e0))+1_(a in endpoints(e2)).     (4)

At an omitted e0 port, its two Q_k neighbors lie in D; the restored
edge has both ends outside D. At a selected e2 port, its internal
selected degree was one and becomes two after restoration. Every
other selected vertex has one selected neighbor, and every other
omitted vertex has three. This proves every case in (4).

Multiply (4) by w(a) and sum over a. Symmetry of adjacency and (3)
make the left side zero. The right side is

    3sum_a w(a)-(w(x_0)+w(x_1))+(w(x_2)+w(x_3))
      =0-1+(-1)=-2,

a contradiction. If the e2 endpoints are omitted instead, the same
argument reverses the signs and gives+2. This proves the four-port
lemma uniformly in k. The weight table is an explicit certificate;
its proof does not require identifying a spectrum or an eigenvalue.

## Construction of the ring and its exact dissociation number

For each i take a broken Heawood block B_i obtained by deleting its
point0--line8 edge, and a disjoint Q_(k_i). Their ports have the colors
used above. Add

    point0_i--x_1_i,       line8_i--x_0_i,
    x_2_i--x_3_(i+1),

where i+1 is cyclic modulo r. The last edge restores e2 when r=1.
Every port receives exactly one edge. The graph is simple, cubic and
bipartite, including r=1 and r=2.

The established saturated-port Heawood lemma gives |D intersect B_i|<=8.
If equality holds, both Heawood ports are selected and each already
has a selected internal neighbor. Hence both neighboring x_0_i,x_1_i
must be omitted. The four-port lemma then gives

    |D intersect Q_(k_i)|<=12k_i-1.

Otherwise |D intersect B_i|<=7 and the unconditional core cap is12k_i.
In both cases the disjoint vertex blocks contribute at most7+12k_i.
Summing these independent local bounds proves beta_2(R)<=7r+12K.
No extra condition on a neighboring core is consumed by this bound;
each strict core cap already permits arbitrary choices at its other
two ports. This is why shared compensation cannot defeat the sum.

For attainment, take all seven points in each Heawood block and

    U_i union H_(odd,i) union X_(even,i)

in each core. This has size7r+12K and induces a matching plus isolates.
Every new edge has an omitted endpoint: x_1 and x_3 are omitted,
as is the Heawood line8. Thus it is a dissociation set in R and proves
the exact beta_2 value in (1).

## Minimality, the exact SF value and connectivity

In every Heawood block use its established eight-vertex minimal
selection, and in every core select H_i union U_i. All removed and
added edges have endpoints outside this selection. A covering two-star
for any subset of S uses at most one vertex outside that subset;
an edge with both endpoints outside S cannot occur in it. Hence the
old covering and deletion witnesses survive every interface, and S
remains minimal with size8r+12K.

The established cubic compensation theorem gives

    7SF_2(R)<=3n+2beta_2(R)=7(8r+12K).

The displayed selection attains it. This proves exact SF_2 and linear
equality. Unlike the single-obstruction case, the regular order bound
alone would not establish this upper bound for arbitrary r.

For connectivity, first join each broken Heawood block to C_(k_i)
through the e0 edge swap. The earlier padding proof gives a two-connected
graph G_i. Now delete its surviving e2 and reconnect the G_i cyclically.
Every edge-deleted G_i is connected. After deleting a non-port vertex
of one G_i, deleting e2 either leaves that block connected or splits it
into two pieces containing its two ports; the path through the other
blocks reconnects the two pieces. After deleting a port, that block
minus the port is connected, and the remaining cyclic interfaces give
a path joining every block. The other blocks are unaffected. For r=1
the edge is simply restored and the earlier proof applies. Thus R is
two-connected in every case.

## The smallest endpoint padding core in this architecture

There is a useful limitation on replacing C_k by a smaller endpoint
core. Suppose C is cubic and bipartite, S is minimal, |S|=3|V(C)|/5,
and the outside graph G[V(C) minus S] contains an edge. Then

    |V(C)|>=20.                                           (5)

The established regular-order equality partition has no selected
isolates: its high vertices each have one selected leaf, its high graph
is two-regular, and all outside edges lie among the degree-one witnesses
in bijection with these highs. Thus an outside edge forces a nonempty
simple even high cycle. If h is the number of highs, then h>=4 and
|S|>=2h>=8. A cubic bipartite graph has even order, and the equality
5|S|=3|V(C)| makes that order divisible by five. Hence the order is a
multiple of ten; order ten would give |S|=6, a contradiction. This
proves (5), and C_1 attains20.

Consequently, in the specific architecture with one14-vertex Heawood
obstruction and one regular-order endpoint core per unit of gap, outside
edge swaps cannot improve the gap coefficient beyond1/34 by shrinking
the core. This is a limitation of this padding architecture, not of
all cubic equality graphs or all cubic bipartite constructions. It
explains why a different port mechanism is needed to improve on the
earlier1/28asymptotic gap family. This corollary was added after the
four-port Oracle review input and is outside that input's scope.

## Scope and verification

The four-port lemma and all-order ring theorem above are general
written proofs. Fixed-size searches found the port behavior; they are
not used to prove the periodic identity, strict loss, or global bounds.
The new construction remains on the cycle stratum of the equality
classification. It demonstrates unbounded gap on that stratum but
does not determine the best connected cubic gap coefficient, which
is still between1/28 and1/14. Rectangular-grid equality remains open.

The [Lean source](../formal/StarForming/CubicPaddingRings.lean) has seven
audited declarations. Kernel decision checks the displayed six-periodic
weight rows and the unequal cut-pair weights. A conditional theorem
for arbitrary integer-valued count functions proves that the twenty
periodic balance equations force zero transferred cut flux. To obtain
those equations from (4), sum selected indicators separately over each
residue class of H,U,X and the two types of Y. The six high rows, six
leaf rows, six outside rows and two Y rows are exactly the theorem's
hypotheses; the two hypothetical omission cases have flux+1 or-1,
contradicting its zero conclusion. Three further declarations check
the four-port deficiency equality implications, ring parameter
arithmetic and the conditional SF upper bound. One additional conditional
arithmetic theorem verifies the endpoint-core order threshold from its
cycle, cardinality and parity hypotheses. The graph cut identity,
class aggregation, construction and connectivity retain written proofs.
The [formal receipt](../output/cubic-padding-ring-formal-check.json)
records local Lean4.33.0, standard axioms only, memory/process preflight
and sequential compilation. No full graph formalization is asserted.

The [independent controls](../output/cubic-padding-ring-controls.json)
check all1,048,576subsets of Q_1, including all77,511dissociation sets
and their exact deficiency identities. All sixteen prescribed port
patterns have independently recorded exact optima and witnesses.
Sixteen periodic cores, k=1,...,16, check2,720individual weight rows.
Fifteen ring instances with equal and unequal positive core sizes pass
literal formation, all1,548selected deletion checks, the displayed
dissociation witnesses, exact equality accounting and all2,618vertex
deletion connectivity checks. For r=1 their full graphs and selections
agree with the independently implemented previous padding family.
Larger beta/SF labels are explicitly consequences of the written
four-port and compensation proof, not additional solver optima.

Run `python3 scripts/check_cubic_padding_rings.py --output output/cubic-padding-ring-controls.json`.
The proof has a separate
[Oracle review request](reviews/2026-10-19-cubic-padding-ring-review-question.md)
and [status receipt](../output/cubic-padding-ring-oracle-review.json).
The accepted augmented-isolate review predates this construction and
does not by itself review the new four-port lemma or ring theorem.
