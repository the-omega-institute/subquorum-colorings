# Two-colour repairs and stronger subcubic selected-star bounds

Let G be a nonempty finite simple bipartite graph of order n and maximum
degree at most three. A set S is two-star-forming if every vertex outside
S lies in a copy of K_(1,2) with exactly two selected vertices; the copy
need not be induced. Suppose S is inclusion-minimal and its induced
components are stars, single edges or isolates. Write beta_2(G) for the
unrestricted dissociation number, and d=|S|-beta_2(G).

**Theorem.** The following bounds hold:

| Hypotheses on G | Bound for d |
|---|---|
| Maximum degree at most three | floor(4n/57) |
| Minimum degree at least two, maximum degree at most three | floor(8n/121) |
| Cubic | floor(n/24) |

No connectivity assumption is required. The first bound allows pendant
and isolated vertices. The second strengthens the preceding 20/263
coefficient, and the third improves the preceding real coefficient 1/22.
All are bounds for the specified selected-component class; they do not
assert that every maximum minimal forming set has this structure.

The [compact two-connected family](COMPACT_SUBCUBIC_SELECTED_STAR_GAPS.md)
has n=64k, |S|=40k and beta_2=39k for all k>=1, with minimum degree and
vertex connectivity two. Therefore the best asymptotic gap coefficient
in that selected class lies between 1/64 and 8/121. Graph-sharpness of
the new upper coefficients remains undetermined.

## Fix the original witnesses

Use one permitted witness assignment from
[SHARP_SELECTED_STAR_GAP.md](SHARP_SELECTED_STAR_GAP.md). There are c
selected star centres C, e=2c+s selected leaves, selected isolates I,
and m selected vertices in edge components. The s surplus leaves are
nonnegative. A centre is clean if some leaf has a private outside deletion
witness, whose selected neighbourhood is precisely that leaf.

Choose one distinct outside witness per leaf, including a private witness
at each clean centre. At each of the q other centres choose one additional
direct centre witness. Their union W has size e+q. Every chosen witness
has exactly one active selected owner (a leaf or a direct centre), at
most one selected-isolate helper, and no other selected neighbour.

For each i in I put h(i)=|N(i) intersect W|, and define

    a=#{i:h(i)=1}, b2=#{i:h(i)=2}, b3=#{i:h(i)>=3},
    t=a+b2+b3, z0=#{i:h(i)=0}, U=V minus (S union W), u=|U|.

Let mu be the matching number of the labelled centre/helper repair graph:
each leaf witness touching an h=2 helper labels an edge from its centre
to that helper. Both endpoint types have capacity one. The established
ledgers and exact count are

    J=c+s+2q-a-2b2-3b3>=0,
    R=c-q+b2+b3-mu>=2d,
    T'=a+b2+b3-s-q>=2d,
    D=q+s+2mu-2b2>=0,                                 (1)
    n=5c+2s+q+a+b2+b3+m+z0+u.

The stronger free-vertex exchange defines

    I_+={i in I:h(i)>0},
    Z={v in U:N(v) intersect S is a subset of C union I_+}, g=|Z|,

and gives T'-g>=2d. See
[FREE_UNUSED_VERTICES_AND_DEGREE_REFINEMENT.md](FREE_UNUSED_VERTICES_AND_DEGREE_REFINEMENT.md).
All choices and counts here remain fixed throughout the proof.

## A new exchange inequality

**Lemma.** Under the maximum-degree-three hypothesis,

    3d <= c+s+b2+b3.                                   (2)

**Proof.** Every selected nontrivial star is P_3 or K_(1,3). Their
numbers are c-s and s. A nonclean centre cannot belong to a selected
K_(1,3), since its three selected leaves and direct witness would give
it at least four neighbours. Thus exactly c-q-s selected stars are
clean P_3's.

For each clean P_3 choose one of its fixed private witnesses, and label
its star and the two already chosen leaf witnesses as

    a_j - x_j - c_j - y_j - b_j,

where a_j has only x_j as a selected neighbour. The second witness b_j
may be private or helped. Let A be this set of private a_j vertices,
F=G[A], and

    E0={a in A:deg_F(a)<=1}, E=|E0|.

Every a in A has its owner edge and total degree at most three, so
Delta(F)<=2. More directly, F[E0] has maximum degree at most one.

Form D0 from selected vertices as follows. At each clean P_3 retain
c_j,y_j and omit x_j. At each nonclean P_3 retain its two leaves.
At each selected claw retain its three leaves. Retain all selected
isolates and all selected edge components. This is dissociation and

    B0=|D0|=|S|-c.

The only selected neighbour of every a in E0 is its omitted owner x_j.
Consequently D0 union E0 is dissociation, giving

    E <= beta_2(G)-B0=c-d.                              (3)

Now fix an ordered bipartition (X,Y), and construct a raw set. Initially
retain all original selected isolates and selected edge components.
At every selected star use the following state; w denotes the fixed
direct centre witness, and b_x denotes the fixed witness of leaf x.

| Star | Centre in X | Centre in Y |
|---|---|---|
| Clean P_3 labelled above | {a_j,c_j,y_j} | {x_j,c_j,b_j} |
| Nonclean P_3, leaves x,y | {x,y,w} | {c,b_x,b_y} |
| Claw, leaves x1,x2,x3 | {x1,x2,x3} | {c,b_x1,b_x2,b_x3} |

The raw set contains a witness of colour X only when it is one of
the a_j in A. Every other retained witness has colour Y. Every retained
witness has its active selected owner omitted. Within the retained
selected vertices, clean P_3's leave an edge and the other stars leave
independent vertices. The raw set can therefore have only two kinds
of additional conflict: witness--witness edges, and selected isolates
adjacent to multiple retained witnesses.

First delete every retained a in A intersect X having a retained
Y-witness neighbour. This neighbour lies outside A. Together with its
owner edge, that incident edge leaves at most one slot for neighbours
in F. Thus every deleted a belongs to E0. There are no witness--witness
edges after this repair, since each witness colour class is independent.

Next delete each original selected isolate meeting at least two of
the retained Y-witnesses. Such an isolate has h>=2. Every retained
witness now has at most its one helper as a neighbour; every retained
helper has at most one retained witness neighbour. The owner/helper
classification excludes all other additional selected adjacencies.
The repaired set is therefore dissociation.

Perform the same construction for (Y,X). A given a_j is retained as
a private witness in only one order, so the total number of its deletions
across the two sets is at most E. Each chosen witness occurs in exactly
one raw set. A selected isolate i has h(i)<=deg_G(i)<=3, since it has no
selected neighbour. Deletion in both orders would require at least two
retained witness neighbours in each, hence at least four distinct witnesses.
Thus an isolate requires deletion in at most one order. Their total repair
cost is at most b2+b3. A shared helper incident to
three retained witnesses costs one deleted vertex, not three.

Before repairs, each clean or nonclean P_3 contributes three vertices
in each order. A selected claw contributes four in one order and three
in the other. The total raw size is exactly

    2B0+2(c-q-s)+2q+s=2B0+2c-s.

All original selected isolates were included once per set, irrespective
of the number of incident witnesses. The two repaired dissociation sets
thus have total size at least 2B0+2c-s-E-b2-b3. As each has size at
most beta_2(G),

    2d <= s+E+b2+b3.                                   (4)

Substitute (3) to obtain 3d<=c+s+b2+b3, as claimed. Every vertex of U
was omitted throughout. In particular no minimum-degree hypothesis
was used. QED.

## Three exact nonnegative certificates

Put K=c+s+b2+b3, so the new lemma gives K>=3d. Direct expansion of the
fixed count in (1) yields

    4n=9J+2R+13T'+D+9K+2s+7b3+4(m+z0+u).              (5)

Every term is nonnegative and 2R+13T'+9K>=4d+26d+27d=57d.
Hence 57d<=4n, proving the first theorem by integrality.

Suppose now the minimum degree is at least two. Each h=1 isolate
has at least one neighbour in U. Each vertex in U minus Z spends one
degree slot on a selected neighbour of another type, so it supports
at most two of these isolate edges; each vertex in Z supports at most
three. Counting actual edges through their unique selected endpoint gives

    V0=2u+g-a>=0.                                      (6)

The exact certificate is

    8n=21J+2R+33(T'-g)+D+17K+4V0
         +10s+19b3+8(m+z0)+29g.                        (7)

Its constrained terms total at least 4d+66d+51d=121d. This proves
121d<=8n and the second bound. The g terms belong to the same actual
set Z in both (6) and the exchange, and cancel in the exact identity;
no unused degree slot is credited twice.

Finally suppose G is cubic. Choosing the larger bipartition class
gives beta_2(G)>=n/2. Thus

    B=2|S|-n=c-q+t+m+z0-u>=2d.

The total selected--U demand gives

    F0=3u-2c+s-3t+3q-2m-3z0>=0.                        (8)

To see this, write H0=sum h(i)<=c+s+2q. The exact selected degree
sum gives |E(S,U)|=3|S|-3e-m-q-H0, at least
2c-s+3t+2m+3z0-3q. It is at most 3u. This proves (8)
using one aggregate degree count on the actual set U.

The new cubic identity is

    n=2J+4T'+2K+5B+2F0+2b3+2z0.                       (9)

Now 4T'+2K+5B>=8d+6d+10d=24d. This proves n>=24d
and the third bound. All three arguments also hold when d<=0; the
corresponding floor inequalities are then immediate.

These are exact identities and explicit exchanges, independent of an
optimization program or a finite search. Numerical ledger points may
show the limits of these particular certificates without producing an
extremal graph.

## Verification and provenance

Run `python3 -B scripts/check_subcubic_colour_exchange.py` with assertions
enabled. It constructs the baseline, both raw states and both repaired
sets from one physical witness assignment. It verifies the induced edges,
the disjointness of repair charges, all size identities and all three
coefficient certificates using integer arithmetic. Small graphs enumerate
all selected subsets and permitted witness assignments; separate seeded
graphs exercise claws, direct centres, h=2 and h=3 helpers and both repair
types. The 48-vertex pendant and 64-vertex minimum-degree-two positive
controls have independently exact dissociation optima. General conclusions
are supplied by the proof above, not extrapolation from those controls.

The two-colour repair lemma and the 8/121 consequence were proposed in
the independent research response. The general 4/57 and cubic 1/24
certificates, and the direct eight-times-order identity (7), were derived
subsequently. This attribution distinguishes the new argument from the
earlier private-four-cycle construction. No graph-sharpness, unrestricted
SF_2 upper bound, full-grid theorem or new Lean verification is asserted.
