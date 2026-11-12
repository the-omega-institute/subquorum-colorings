# Free unused vertices and a sharper minimum/maximum-degree bound

Let G be a nonempty finite simple bipartite graph of order n, with minimum
degree at least delta>=2 and maximum degree at most Delta. Let S be an
inclusion-minimal two-star-forming set whose induced components are stars,
single edges or isolates. The stars used for formation need not be induced.
Write d=|S|-beta_2(G), where beta_2 is the unrestricted dissociation number.

**Theorem.** Every such selection satisfies

    d<=floor((Delta-1)n/[12(Delta-1)+2(delta-1)]).          (1)

The old minimum-degree certificate used L=max(7(delta-1),Delta) and gave
floor(Ln/[12L+2(delta-1)]). The new bound is strictly stronger as a real
coefficient for every feasible pair Delta>=delta>=2. For example,
delta=2,Delta=4 gives floor(3n/38), replacing floor(7n/86).
For delta=2,Delta=6 it gives floor(5n/62).

This is a bound for the specified selected-star/edge/isolate minimal set,
not a statement that every maximizing minimal selection has that form.
It should be combined with the stronger existing regular whole-cut bounds
and the cubic n/22 theorem. No graph-sharpness or general-grid equality
claim is made. A positive equality in the unrounded version of (1) is
impossible when delta>=3; a structural proof is given below.

## One witness assignment and its established ledgers

Use the permitted assignment in SHARP_SELECTED_STAR_GAP.md and the stronger
colour exchange in DIRECT_WITNESS_EXCHANGE_AND_CUBIC_BOUND.md. There are c
nontrivial star centres C, e=2c+s leaves L, selected isolates I and m
selected edge-component vertices P. Let q count centres without a clean
leaf. Choose one outside deletion witness per leaf, with a private one
at every clean centre, and one direct centre witness for each q-centre.

The witnesses form a set W of size e+q. Each has exactly one active
selected owner and at most one selected-isolate helper. Put

    h(i)=|N(i) intersect W|,
    a=#{i in I:h(i)=1}, b2=#{i:h(i)=2}, b3=#{i:h(i)>=3},
    t=a+b2+b3, z0=#{i:h(i)=0},
    U=V minus (S union W), u=|U|.

The labelled centre/helper repair matching has size mu, with capacity one
at both endpoint types. The established inequalities and exact count are

    J=c+s+2q-t-b2-2b3>=0,
    R=c-q+b2+b3-mu>=2d,
    T'=t-s-q>=2d,
    D=q+s+2mu-2b2>=0,                                  (2)
    n=5c+2s+q+t+m+z0+u.                                (3)

They refer to one fixed assignment. No new choice of W is made between
the degree counts and exchanges below.

## Include every genuinely free unused vertex

Let I_+= {i in I:h(i)>0} and I_0=I minus I_+. Define

    Z={v in U:N(v) intersect S is a subset of C union I_+},
    g=|Z|.                                              (4)

Thus v is outside Z exactly when it has a selected neighbour in
L union P union I_0. This classification uses actual selected adjacency.

Fix the bipartition A,B. In the established colour exchange, select

    D_A=((S minus C) union (W intersect A)) minus I_A^*,

where I_A^* consists of the selected isolates touched by W intersect A.
This is dissociation. Every leaf is paired with at most its own witness;
direct witnesses lose their centre owners and helpers; selected edges
remain matching edges; retained isolates meet no retained witness.

Now add every vertex of Z intersect A. Such a vertex has no neighbour in
the retained witnesses, since they have the same colour. Each of its
selected neighbours is either a removed centre or a touched isolate in B.
Every touched isolate in B is in I_A^*, since all its W-neighbours lie
in A. Hence each added vertex has no neighbour in D_A. Added vertices
are mutually independent, so the enlarged set D_A^+ is dissociation.
The symmetric construction gives D_B^+.

Each touched isolate is removed in exactly one colour construction, and
each free unused vertex is added in exactly one. Consequently

    |D_A^+|+|D_B^+|=2|S|+s+q-t+g,

and therefore

    T'-g=t-s-q-g>=2d.                                  (5)

The two sets are alternatives whose sizes are summed. No outside vertex
is counted twice, and (5) uses the same Z,W throughout.

## A degree slot spent on a different selected vertex

An h=1 selected isolate has no selected neighbour and exactly one
neighbour in W. It has at least delta-1 neighbours in U. Count all actual
edges between these a isolates and U, once through each endpoint.

Every vertex of Z can support at most Delta such edges. Every vertex of
U minus Z has at least one neighbour in L union P union I_0, disjoint
from the h=1 isolates, so supports at most Delta-1 of the counted edges.
Thus the single aggregate capacity gives

    (delta-1)a<=Delta*g+(Delta-1)(u-g)
                =(Delta-1)u+g.                         (6)

A free vertex earns its contribution in (5); a nonfree vertex spends a
real degree slot in (6). These are two statements about the same partition
of U, rather than independent copies of its available capacity.

## The coefficient bound

From the exact identities

    t=T'+s+q,
    2c=J+R+T'+b3+mu,

equation (3) becomes

    n=(5/2)J+(5/2)R+(7/2)T'+(5/2)(b3+mu)
         +3s+2q+m+z0+u.                                (7)

Put eta=n-12d and H=b3+mu. By (2),(5),

    eta>=u+(7/2)g+(5/2)H+3s+2q+m+z0.                  (8)

Also D>=0 gives b2<=(q+s)/2+mu. Substituting this in (5),

    2d<=a+H-(s+q)/2-g.                                 (9)

Multiply (9) by delta-1 and use (6):

    2(delta-1)d<=(Delta-1)u+(delta-1)H
                    -(delta-1)(s+q)/2-(delta-2)g.       (10)

Since Delta>=delta>=2, we have Delta-1>=delta-1>0. The right side of
(10) is at most (Delta-1)eta by (8): the H term costs only delta-1
per unit whereas (8) supplies (5/2)(Delta-1); the s,q,g terms in (10)
are nonpositive, and all remaining terms in (8) are nonnegative.
Therefore

    2(delta-1)d<=(Delta-1)(n-12d),

proving (1) by integrality. The nonpositive-gap case also satisfies (1).
There is no asymptotic or finite-search assumption in the argument.

## A quantified remainder and the unrounded equality obstruction

The same calculation retains the explicit nonnegative remainder

    (Delta-1)eta-2(delta-1)d
      >=[(7/2)(Delta-1)+delta-2]g
        +[(5/2)(Delta-1)-(delta-1)]H
        +[3(Delta-1)+(delta-1)/2]s
        +[2(Delta-1)+(delta-1)/2]q
        +(Delta-1)(m+z0).                               (11)

All coefficients are strictly positive. If d>0 and equality holds in
the unrounded version of (1), (11) forces g=H=s=q=m=z0=0. Equality in
(7)-(8) then gives J=0,R=T'=2d, so c=a=t=2d and b2=b3=mu=0.
In particular the selected stars are P3's and every selected isolate
has exactly one chosen witness.

Equality in (6) now forces every U vertex to have degree Delta, exactly
Delta-1 neighbours among the h=1 isolates, and exactly one other
neighbour. Since U minus Z is all of U, that other neighbour lies in
L union P union I_0; m=z0=0 makes it a leaf. All U degree capacity has
been used, so no U vertex meets a selected centre.

No selected centre meets W either: q=0 and the witness classification
gives every chosen witness a leaf owner and at most one isolate helper.
The remaining selected graph gives each centre exactly its two leaves.
Thus every selected centre has full graph degree two. Since c=2d>0,
this contradicts minimum degree at least three. This proves the stated
strict unrounded obstruction for delta>=3. It does not settle sharpness
at delta=2 or the optimal asymptotic coefficient at other parameters.

## Verification status

Run `python3 scripts/check_free_unused_degree_refinement.py` with assertions
enabled. The standalone checker constructs both enlarged colour exchanges,
counts the actual h=1-isolate cut, and verifies the exact identities, bound
and remainder using integer arithmetic. It passes455 stated graph inputs,
277,856 selected subsets,16,240 eligible minimal selections,24,096 permitted
witness allocations,48,192 enlarged exchange sets and182,982 degree-parameter
checks. The nine targeted models separately exercise positive gaps, both
free and nonfree vertices, direct-only centres, helpers with h>=3, selected
edges and untouched isolates. Some target controls have minimum degree below
2; they test exchanges and identities, not an inapplicable degree theorem.
There are no positive gaps in the455-input small-model range; positive
controls are explicitly separated in the report.

The new general proof received independent proof-only ACCEPT, including the
delta=2 boundary and the strict unrounded obstruction at delta>=3. That
review made no code-execution claim. The final exact-source/execution
review, also covering the new bounded-degree lower family, returned ACCEPT.
The reviewer reconstructed all10 files with matching byte counts and hashes,
ran both original checker entry points unchanged with assertions enabled,
and reproduced both complete reports byte-for-byte(24,963 and11,730 bytes).
See `../output/degree-refinement-and-lower-family-review.json` for the frozen
manifest, full response and actual execution scope. Imported helper modules
were exercised; their separate main suites were not rerun.
Finite controls support the implementation; the general proof is(4)-(11).
No new Lean, graph-sharpness or historical-priority claim is made.
