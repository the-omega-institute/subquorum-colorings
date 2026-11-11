# Whole-cut degree capacity for selected-star forming sets

Let G be a nonempty finite simple bipartite graph of order n, with minimum
degree at least delta>=3 and maximum degree at most Delta. Let S be an
inclusion-minimal two-star-forming set whose selected components are stars,
edges or isolates. Put d=|S|-beta_2(G).

**Theorem.** If Delta>=4, then

    d <= floor((Delta-delta+1)n / (2(5Delta+delta-7))).       (1)

For a cubic bipartite graph the stronger special certificate below gives

    d <= floor(7n/146).                                     (2)

In particular every such selected-star minimal set in a k-regular
bipartite graph, k>=4, satisfies

    d <= floor(n/(12k-14)).                                 (3)

These statements concern the specified selected-star minimal set. Their
constants are optimal consequences of the numerical ledgers specified below
in the stated parameter ranges; graph-theoretic sharpness is not claimed.
The bounds can be combined with preceding bounds when Delta is large.

The key additional constraint is beta_2(G)>=n/2. It couples the degree
capacity to the number of selected edge components. In a k-regular graph
we prove the more informative resource inequality

    m >= 2kd+(2k-7)c+(k-3)q+(k-4)s,                         (4)

where m counts vertices of selected edge components. Consequently, for
k>=4, if G[S] contains no edge component then |S|<=beta_2(G).

## One fixed witness assignment

Use the witness construction and exchanges proved in
[SHARP_SELECTED_STAR_GAP.md](SHARP_SELECTED_STAR_GAP.md). Here are all
its parameters and inequalities needed in this proof. Let C be the c
centres of selected stars of order at least three, L their e=2c+s leaves,
and I the selected isolates. Thus s>=0. The remaining selected vertices
P form edge components; put m=|P|, counting vertices rather than edges.

A centre is counted in q if none of its leaves admits a private outside
witness with selected neighbourhood exactly that leaf. Choose one witness
per leaf, including one private witness at every other centre, and one
direct deletion witness per q-centre. Each has exactly one active selected
owner and at most one selected-isolate helper. The chosen witnesses W are
distinct and |W|=e+q. Define h(i)=|N(i) intersect W| for i in I. Let

    a=#{i:h(i)=1}, b2=#{i:h(i)=2}, b3=#{i:h(i)>=3},
    t=a+b2+b3, z0=#{i:h(i)=0}, U=V minus (S union W), u=|U|.

Let mu be the matching number of the labelled centre/helper graph: each
leaf witness touching an h=2 isolate labels a centre-to-helper edge.
Parallel edges are retained, and each centre/helper has capacity one.
The preceding compatible exchanges prove

    J := c+s+2q-a-2b2-3b3 >=0,
    T := t-s >=2d,
    R := c-q+b2+b3-mu >=2d,
    D := q+s+2mu-2b2 >=0.                                  (5)

All counts refer to this one witness assignment. The exact vertex and
selected-size counts are

    n=5c+2s+q+t+m+z0+u,
    |S|=3c+s+t+m+z0.                                       (6)

Choosing a larger bipartition class is a dissociation set, so beta_2>=n/2.
Thus a fifth ledger, not implied by the earlier witness exchanges, is

    B := 2|S|-n=c-q+t+m+z0-u >=2d.                          (7)

## Count every edge from S into U once

Put H=sum_(i in I)h(i). The witness neighbourhood classification gives

    H<=c+s+2q,
    |E(S,W)|=e+q+H,
    2|E(G[S])|=2e+m.                                      (8)

Summing whole-graph degrees over S, the number of actual S--U edges is

    |E(S,U)|=sum_(v in S)deg_G(v)-(2e+m)-(e+q+H)
       >=delta(c+e+t+m+z0)-3e-m-q-H
       >=(3delta-7)c+(delta-4)s+delta t
          -3q+(delta-1)m+delta z0.                         (9)

Every edge counted on the left has a unique selected endpoint. The
vertices of U can collectively support at most Delta u of these edges,
regardless of how many selected vertex types share the same U vertex.
Consequently

    F := Delta u-(3delta-7)c-(delta-4)s-delta t
             +3q-(delta-1)m-delta z0 >=0.                  (10)

This retains the demands of all selected vertex types. No vertex of W
is reused as unused capacity; W is disjoint from U by definition.

## A general certificate when Delta>=4

Put h=Delta-delta+1>0. Direct coefficient expansion using (6) gives

    h n = (2Delta-5)J+(2Delta-3)T+(2Delta-3)R+D
          +2F+(Delta+delta-1)B
          +(2Delta-5)(s+mu)+(2Delta-7)b3+2z0.               (11)

All coefficients are nonnegative for Delta>=4. Apply (5), (7) and (10):

    h n >= 2(5Delta+delta-7)d,

proving (1) by integrality. When d<=0 the claimed bound is immediate.
For Delta=delta=k>=4 this is (3). For example k=4 gives floor(n/34),
and k=5 gives floor(n/46).

The exact identity (11) is also a stability certificate: each surplus
leaf, compatible helper repair, h>=3 helper and untouched isolate pays
its displayed nonnegative contribution. These terms are not allocated
independently to different components.

## Cubic certificate

When delta=Delta=3, direct expansion instead gives

    7n = 8J+18T+20R+4D+14F+35B
         +6s+4a+12mu+14z0.                                (12)

Every term except T,R,B is nonnegative; those three are at least 2d.
Therefore 7n>=146d, proving (2). The coefficient of b3 in (11) would be
negative for Delta=3, which is why (12) is required.

## Selected edges are necessary for regular positive gaps

For Delta=delta=k, add F+kB. The u and t terms cancel, giving

    F+kB = m-(2k-7)c-(k-3)q-(k-4)s >=2kd.                  (13)

This proves (4). For k>=4 all coefficients on the right of (4) are
nonnegative. If m=0, positive d is impossible. If d>0, the selected
subgraph has at least kd edge components, with the additional c,q,s
costs shown in (4). For k=3, the exact relation is m>=6d-c-s;
the nonnegative-coefficient corollary is not asserted in degree three.

## A boundary-sensitive form without a minimum-degree assumption

Now drop the minimum-degree hypothesis and take any integer k>=4 at
least the maximum degree of G. For X subset V define the actual degree
deficit

    epsilon_X=sum_(v in X)(k-deg_G(v)).

Keep the same S,W,U and witness assignment. Write F_k for (10) evaluated
at delta=Delta=k. The exact degree sum and cut capacity give

    |E(S,U)|>= (3k-7)c+(k-4)s+kt-3q+(k-1)m+kz0-epsilon_S,
    |E(S,U)|<=ku-epsilon_U.

Hence Fhat:=F_k+epsilon_S-epsilon_U>=0. Substituting
F_k=Fhat-epsilon_S+epsilon_U into the identity (11) proves

    d <= floor((n+2epsilon_S-2epsilon_U)/(12k-14)),          (14)
    m+epsilon_S-epsilon_U
       >=2kd+(2k-7)c+(k-3)q+(k-4)s.                       (15)

The degree deficits are exact sums over disjoint vertex classes; their
difference is signed. All remaining terms in (11) have nonnegative
coefficients, and T,R,B>=2d even for d<=0. Thus no positivity assumption
on d or on the numerator is needed in (14). For regular graphs both
deficits vanish, recovering (3)-(4).

For a full h-by-w rectangular grid, let k=4. The sum of deficits over
all vertices is exactly 2h+2w, since the grid has 2hw-h-w edges. In
particular every selected-star minimal forming set in this grid satisfies

    d<=floor((hw+2epsilon_S-2epsilon_U)/34)
      <=floor((hw+4h+4w)/34).                             (16)

The first inequality retains the actual location of the selection and
chosen witnesses, and the second forgets it. This bounds the deficit of
the specified selected-star set. It does not prove that arbitrary minimal
forming sets in a rectangle have this form, does not assert equality of
SF_2,beta_2,psi_sq, and does not improve the universal mixed-direction
5/6 coefficient.

## The precise limit of these six numerical ledgers

Consider nonnegative real variables c,q,s,a,b2,b3,mu,m,z0,u, with t=a+b2+b3,
counts (6), and the six inequalities J,D,F>=0 and T,R,B>=2d. Normalize d=1.
This is a relaxation of the graph problem, not a graph construction.

For any integers delta>=3 and max(delta,4)<=Delta<=4delta-7, set

    h=Delta-delta+1,
    c=a=2, q=s=b2=b3=mu=z0=0,
    m=2(4delta-7-Delta)/h, u=m+2.                          (17)

These are nonnegative. They have J=D=F=0 and T=R=B=2. Their order is
n=2(5Delta+delta-7)/h. Thus (1) is optimal over the explicitly defined
real-valued relaxation throughout this parameter range.

For cubic parameters, set

    c=q=12/7, b2=6/7, b3=8/7, m=u=30/7,
    s=a=mu=z0=0.                                          (18)

Again J=D=F=0 and T=R=B=2, and n=146/7. Hence (2) is also optimal over
this relaxation. These rational points do not prove the existence of
extremal graphs, or the value of SF_2. A stronger graph bound may use
structural information absent from these six inequalities.

## Relation to earlier regular results and verification

The general regular bipartite theorem in
[SHARP_REGULAR_BIPARTITE_GAP.md](SHARP_REGULAR_BIPARTITE_GAP.md) has the
sharp unrestricted SF_2-beta_2 coefficient1/(4k+2). Its attaining selections
have a six-cycle or a denser crown component, so the selected-star
hypothesis here excludes them. In particular the Heawood eight-set has
an induced six-cycle and two isolates. It is not an exception to (2).

The new whole-cut capacity and the explicit algebraic certificates give
the proof for all graphs under the stated hypotheses. Run
`python3 -B scripts/check_full_degree_capacity.py` with assertions enabled.
The checker enumerates literal formation and deletion failures, classifies
eligible selected components, and checks every permitted witness choice
in its stated finite graph range. It independently compares two exact
dissociation optimizers, counts actual cut edges, checks the six ledgers
and identities, and verifies the regular selected-edge resource bound.

The report covers 194 graph inputs (193 distinct labelled adjacency lists),
237,760 selected subsets, 12,510 eligible
minimal selections and 20,248 witness assignments. The exhaustive labelled
ranges are cubic graphs with fixed parts (3,3) and (4,4), and quartic
graphs with fixed parts (4,4) and (5,5); larger regular and nonregular
models are seeded controls. None of these eligible finite selections has
positive d. Thus these runs test the ledgers and identities on actual
graphs, without witnessing sharpness or positive-deficit attainment in
this minimum-degree range. Exact rational controls additionally check
20,460 basis identities, 5,858 low-dispersion primal points, the cubic
primal point and six large-integer identities.

The boundary extension is also checked on all 125,262 selected subsets
of 18 specified rectangles, yielding 1,467 eligible minimal selections
and 1,783 witness assignments. Across the rectangle checks there are
1,357 parameter instances with epsilon_S<epsilon_U. Two separate
nonrectangular controls have positive gaps: orders 18 and 24, with
selected/beta values 12/11 and 16/14. Those two graphs have minimum
degree one and test the boundary extension, not the minimum-degree-three
theorem. The finite report is `output/full-degree-capacity-check.json`.

The first independent proof review returned **ACCEPT** on the original
nonempty-graph domain. Its requested scope repair, explicitly retaining
delta<=Delta in the standalone relaxation range, is included above. That
first pass did not review the subsequently added boundary extension and
requested no code execution. The final full-source review returned
**ACCEPT**, including the boundary extension. The reviewer reconstructed
all five supplied files, verified their manifest hashes, ran the original
checker unchanged with assertions enabled to terminal completion, and
reproduced its complete report byte-for-byte. The complete response and
actual scope are recorded in `output/full-degree-capacity-review.json`. No
Lean verification, historical-priority or graph-sharpness claim is made.
