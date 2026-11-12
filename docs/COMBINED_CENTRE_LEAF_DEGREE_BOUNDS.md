# Shared degree capacity for centres, leaves and isolate helpers

Let G be a nonempty finite simple bipartite graph of order n, with
minimum degree at least the integer delta>=2 and maximum degree at most
the integer Delta. Let S be an inclusion-minimal two-star-forming set
whose induced components are stars, single edges or isolates. Formation
uses a not necessarily induced K_(1,2). Write beta_2(G) for the unrestricted
dissociation number and d=|S|-beta_2(G).

**Theorem.** Put A=Delta-1. Every such selection satisfies both

    d<=floor(A*n/[12*A+4*delta-6]),                       (1)
    d<=floor(Delta*n/[12*Delta+8*delta-14]).              (2)

For delta=2, (1) is the previously proved sharp coefficient at Delta>=6;
(2) is weaker. For every Delta>=delta>=3, (2) is strictly stronger as a
real coefficient than (1), and (1) strictly strengthens the previous
A/[12*A+2*(delta-1)] bound. The other whole-cut bounds and the cubic n/22
bound remain applicable; one should take the minimum of all applicable
certificates. In particular (2) improves the previous whole-cut coefficient
when delta=3 and Delta>5, and agrees with it at Delta=5.

These are bounds for the specified selected-star/edge/isolate minimal set.
No sharpness at delta>=3, exact SF_2, unrestricted selected-component
theorem, grid equality or universal mixed-direction 5/6 gain is asserted.

## Fix the actual witness and unused-vertex sets

Use one permitted witness assignment from
[SHARP_SELECTED_STAR_GAP.md](SHARP_SELECTED_STAR_GAP.md). Its distinct
chosen outside witnesses W consist of one leaf witness per selected leaf
and one direct centre witness at each of the q centres lacking a clean
leaf. Each witness has exactly one active selected owner and at most
one selected-isolate helper. There are c selected centres C, e=2c+s
leaves L, selected isolates I and m vertices P in selected edge components.
For i in I put h(i)=|N(i) intersect W|. Define

    a=#{i:h(i)=1}, b2=#{i:h(i)=2}, b3=#{i:h(i)>=3},
    t=a+b2+b3, z0=#{i:h(i)=0}, H=b3+mu,
    U=V minus (S union W), u=|U|,
    Z={v in U:N(v) intersect S is a subset of C union I_+},
    I_+={i in I:h(i)>0}, g=|Z|.

Here mu is the matching number of the labelled centre/helper graph with
one unit of capacity at each centre and each h=2 helper. The established
strong exchange and exact ledgers, with T'=t-s-q, are

    J=c+s+2q-t-b2-2b3>=0,
    R=c-q+b2+b3-mu>=2d,
    T'-g>=2d,
    D=q+s+2mu-2b2>=0,
    n=5c+2s+q+t+m+z0+u.                                (3)

The exchange adds the genuinely free vertices Z of one colour to the
same-colour witness construction; its proof is in
[FREE_UNUSED_VERTICES_AND_DEGREE_REFINEMENT.md](FREE_UNUSED_VERTICES_AND_DEGREE_REFINEMENT.md).
No witness is reassigned between the cuts below. In particular

    2d<=a+H-(s+q)/2-g,
    2c=J+R+T'+H>=4d+g+H.                               (4)

The first inequality follows by substituting b2<=(q+s)/2+mu in T'-g>=2d.
Writing eta=n-12d, the exact order ledger gives

    eta>=u+(7/2)g+(5/2)H+3s+2q+m+z0.                  (5)

All these parameters describe one fixed actual partition of V.

## Count centres and h=1 isolates through the same cut

Every centre has exactly its own selected leaves as selected neighbours.
Summed over C, these are e=2c+s incidences. Its neighbours in W are exactly
the q direct witnesses, one at each q-centre: a leaf witness has a leaf
as its unique active owner, and a direct witness meets no other active
selected vertex. Therefore

    |E(C,U)|>=delta*c-(2c+s)-q.

Each of the a isolates with h=1 has no selected neighbour and exactly
one W-neighbour, so contributes at least delta-1 edges to U. Let Q be
the disjoint union of C and these a isolates. Then

    |E(Q,U)|>=(delta-2)c+(delta-1)a-s-q.                 (6)

A vertex of U minus Z has a neighbour in L union P union (I minus I_+),
which is disjoint from Q. It spends at least one degree slot there and
supports at most A counted edges. A vertex of Z supports at most Delta.
Thus the single aggregate capacity is

    (delta-2)c+(delta-1)a-s-q<=A*u+g.                    (7)

This is one cut, not a separate capacity allocation to each selected type.
Substitute both lower bounds from (4) into its left side. Their multipliers
delta-2 and delta-1 are nonnegative. Rearrangement gives

    2(2delta-3)d<=A*u+(delta/2)H
                    -((delta-3)/2)(s+q)
                    -(3/2)(delta-2)g.                 (8)

Subtract (8) from A times (5). The retained remainder is

    A*eta-2(2delta-3)d
      >=[(7/2)A+(3/2)(delta-2)]g
        +[(5/2)A-delta/2]H
        +[3A+(delta-3)/2]s
        +[2A+(delta-3)/2]q+A(m+z0).                    (9)

Every coefficient is strictly positive for Delta>=delta>=2. This includes
delta=2: the positive (s+q)/2 term in (8) is absorbed by (5), rather than
discarded with an incorrect sign. Consequently A*n>=(12A+4delta-6)d,
proving (1) by integrality. This calculation also applies when d<=0.

## Retain the degree demand of leaves and edge components

The preceding cut reserves only one non-Q neighbour at a nonfree vertex.
Minimum degree also forces a total demand from those other selected types.
Every leaf has exactly one selected neighbour and exactly one neighbour in
W (its own chosen leaf witness). No other chosen witness can meet that
active leaf. It therefore has at least delta-2 neighbours in U. Every
vertex of P has one selected neighbour and none in W, so has at least
delta-1 neighbours in U. An h=0 isolate has all its at least delta
neighbours in U.

Count edges from the disjoint union Q union L union P union (I minus I_+)
into U. Counting each actual edge at its unique selected endpoint gives

    3(delta-2)c+(delta-1)a+(delta-3)s-q
                  +(delta-1)m+delta*z0<=Delta*u.        (10)

Neither helpers with h>=2 nor any edges inside U or from W are credited
as extra capacity; omitting their demand only weakens this valid cut.
Substitute (4) again and rearrange:

    (8delta-14)d<=Delta*u+((4-delta)/2)H
                   -((3delta-7)/2)s-((delta-3)/2)q
                   -((5delta-8)/2)g
                   -(delta-1)m-delta*z0.              (11)

Together with (5), this yields a second explicit remainder:

    Delta*eta-(8delta-14)d
      >=[(7Delta+5delta-8)/2]g
        +[(5Delta+delta-4)/2]H
        +[3Delta+(3delta-7)/2]s
        +[2Delta+(delta-3)/2]q
        +(Delta+delta-1)m+(Delta+delta)z0.               (12)

All coefficients are strictly positive even at delta=2. Thus
Delta*n>=(12Delta+8delta-14)d, proving (2).

The coefficient in (2) is smaller than that in (1) exactly when

    Delta*(4delta-8)>8delta-14.

It holds for every Delta>=delta>=3, since at delta=3 the two sides are
at least12 and10, and the difference at Delta=delta grows thereafter.
For delta=2 the inequality fails, so (1) remains the useful certificate.
At delta=3, comparison with (Delta-2)/(10Delta-8) reduces to
2(Delta-5)(Delta+2)>0, as stated above.

## What numerical equality would require

If d>0 and equality holds in either unrounded coefficient, its positive
remainder forces g=H=s=q=m=z0=0. Equation (5) and the exact count then
force J=0, R=T'=2d, c=a=2d and b2=b3=mu=0. Thus every selected star is a
P_3, every selected isolate has exactly one chosen witness, and no selected
edge component or untouched isolate remains.

For (1), equality in (7) forces each U vertex to have degree Delta,
exactly A neighbours in Q and exactly one leaf neighbour. The leaves
collectively need at least (delta-2)e=4(delta-2)d edges into U, hence
u>=4(delta-2)d. But equality in (1) gives

    u=(4delta-6)d/A<=((4delta-6)/(delta-1))d.

For delta>=3 this is strictly less than4(delta-2)d, a contradiction.
Thus positive real equality in (1) is impossible at delta>=3; equivalently
the integer bound may there be written floor((A*n-1)/(12A+4delta-6)).
The stronger coefficient (2) should normally be used instead.

For (2), equality instead requires u=(8delta-14)d/Delta, every counted
selected vertex at degree delta and every U vertex of degree Delta using
all its capacity on the counted selected classes. The independent
beta_2>=n/2 ledger gives u<=2d, so necessarily Delta>=4delta-7. These are
necessary conditions only. No graph attaining (2) is constructed here.
If Delta<4delta-7, positive real equality in (2) is impossible and the
same integrality refinement gives floor((Delta*n-1)/(12Delta+8delta-14)).

## Verification and scope

The standalone entry point is
`python3 -B scripts/check_combined_centre_leaf_degree_bounds.py`, with
assertions enabled. It constructs actual enlarged colour exchanges,
counts physical centre-to-W incidences and both actual cuts, and checks
the ledgers, remainders, integer bounds and conditional strictness.
The complete general proofs are (3)-(12); finite checks serve as controls.
The report covers455 graph inputs,277,856 selected subsets,16,240 eligible
minimal selections and24,096 permitted witness allocations. It verifies
48,192 actual enlarged exchanges and182,982 degree-parameter checks,
including150,178 physical long-cut edges and18,566 short-cut edges counted
over those allocations. There is no positive gap in that small range.
Seven targeted controls are separate; three have positive gaps at minimum
degrees2,3,4, and the others test witness choices, large helpers, selected
edges and untouched isolates outside the minimum-degree theorem when
appropriate. There are1,716 exact rational basis-identity checks and three
large-integer controls, including1024-digit scale.

The independent research response supplied a full proof of (1), its
remainder and the leaf obstruction to equality. The further leaf/edge
capacity (10), coefficient (2), remainder (12) and its necessary equality
conditions were then derived separately. Their final exact-source review
has its own evidence record; earlier acceptance is not reused to certify
this new theorem. The independent final audit returned **ACCEPT**. The
reviewer reconstructed all9 files with exact manifest hashes, ran the
unchanged entry point with assertions enabled to exit0 and empty stderr,
and reproduced the complete22,210-byte report byte-for-byte (SHA-256
e77cf0249156332898adc00ac1e2fcd51cf67e51d4c20c97319e4f9fb219f0be).
See `../output/combined-centre-leaf-degree-review.json` for the frozen
source manifest, full responses and execution scope. Only this verification
paragraph was added after the reviewed source freeze.
No Lean or literature-priority claim is made.
