# Intrinsic recognition and paired-neighbourhood equality criteria

11 November 2026. Graphs are finite, simple and bipartite; formation uses
non-induced two-leaf stars and inclusion-minimal selected sets. We use the
[proved universal bound](SHARP_BIPARTITE_STAR_FORMING_GAP.md).
Positive equality in this note always means SF_2-beta_2=n/10>0, not merely
attainment of floor(n/10). The general criterion below is an exact test by
adjacency and all-subset neighbourhood counts, not a finite list of local
blocks or a polynomial-time recognition claim.

## Intrinsic layers and a unique maximizing minimal set

**Theorem 1.** Every positive equality graph has order 10k for an integer
k>=1, and SF_2=6k, beta_2=5k. It has exactly 2k=n/5 degree-two vertices.
Put

    I={v:deg_G(v)=2}, X=N_G(I), C=V(G) minus (I union X).

These sets are disjoint. The neighbours of different vertices of I are
disjoint pairs partitioning X. The edges between C and X form a perfect
matching. All other edges lie inside G[C] or G[X]. Both bipartition sides
have size 5k; I has k vertices on each side, and C,X have 2k on each side.
Furthermore delta(G[C])>=2 and delta(G[X])>=1.
The unique maximum-cardinality inclusion-minimal forming set is

    S_max=I union C=V(G) minus N_G(I).                         (1)

**Proof.** Apply the saturated ledger to any maximizing minimal set S.
It gives p=a=0, u=2b, |R|=b, n=5b and no unused outside vertices.
Let I=R, C=S minus I, X=V minus S for the moment. Every c has one
unique outside witness x_c, with selected neighbourhood {c,i(c)}.
Every isolate has exactly two witnesses and there are no other outside
vertices. Thus all stated matching and pair incidences hold. In particular
|S|=3b and beta_2=5b/2, so b=2k and the parameter values follow.
If I has r,s vertices on the two sides, their orders are 3r+2s and
2r+3s. Both sides are independent and beta_2=5k, forcing r=s=k.

Suppose c in C_A has at most one neighbour in C_B. Let i be its paired
isolate and x_c its matched witness. Starting with the whole independent
side B, remove x_c and add c and i. The vertex c sees at most its one
core neighbour. The vertex i sees just its other witness, whose owner
is distinct from c. Those two possible partners are distinct. Thus the
new set is dissociation of size 5k+1, a contradiction. This proves
minimum core degree two, so full core degrees are at least three.

Suppose x in X_A has no neighbour in X_B. The set C_A union X_B union I_B
has size 5k and induces only the matching C_A--X_B; I_B is isolated.
Adding x pairs it only with its unique I_B neighbour: its core owner
is in the omitted C_B and it has no X_B neighbour. Again the result has
size 5k+1, a contradiction. Hence the interface minimum degree is one
and its full vertex degrees are at least three.

It follows that the originally selected isolates are exactly ALL full
degree-two vertices of G. Their neighbours are exactly X, and the rest
is C. These definitions no longer depend on S. Applying the same argument
to any other maximizing minimal set gives the identical layers and (1),
proving uniqueness. This concerns maximizing minimal sets, not all minimal
sets of other sizes.

## Exact recognition using a strengthened Hall condition

For a bipartite graph with parts A,B, let priv(T) count the vertices
v in T, for T subset A, that have at least one private neighbour:
there exists w in B with N(w) intersect T={v}. Multiple such neighbours
of the same owner count once. Directly optimizing the B part after fixing
its A part gives the elementary identity

    beta_2(G)=|B|+max_(T subset A)(|T|+priv(T)-|N(T)|).          (2)

Indeed all B vertices with no T neighbour may be selected; those with at
least two may not; among neighbours with unique owner v, choose at most
one for each v, and one whenever it exists. These choices are compatible
because B is independent. This proves both directions of (2).

**Theorem 2.** A nonempty finite simple bipartite graph has positive
unrounded equality if and only if the following adjacency conditions hold.
Define I={deg_G=2}, X=N(I), C=V minus (I union X).

1. I is nonempty and independent.
2. Each x in X has exactly one neighbour in I.
3. The edges between C and X form a perfect matching covering C union X.
4. There is a balanced bipartition A,B, and for every T subset A,

       |N(T)| >= |T|+priv(T).                                (3)

**Proof.** Necessity of the layers and balance is Theorem 1; (2) gives
(3). Conversely, if b=|I|, the pair incidences give |X|=2b, the matching
gives |C|=2b, and n=5b. The set S=I union C is forming: each x has its
unique core owner and its unique isolate as selected neighbours.
Deleting an isolate uncovers that deleted vertex, and deleting a core
owner leaves its witness with just an isolated selected neighbour. Thus
S is minimal, with size 3b. By (2), balance and (3), beta_2=n/2=5b/2.
The universal bound gives SF_2<=5b/2+b/2=3b, so equality holds throughout.
Integrality and balance force b even. No star-forming or dissociation
parameter is an input to this recognition criterion.

## Paired-neighbourhood conditions and complete cores

Use the structural template with |I_A|=|I_B|=k and |C_A|=|C_B|=|X_A|=
|X_B|=2k, matching C--X, and the disjoint I-centred witness pairs. No
assumption about the internal core edges is needed initially. Let P_A
partition X_A into pairs centred in I_B, and P_B partition X_B into
pairs centred in I_A. For a collection J of pairs in P_B, define

    z_Q(J)=#{P in P_A:P subset N_Q(union J)}, Q=G[X].

Define the reversed version for J subset P_A.

**Theorem 3.** For all such templates,

    max_(D dissociation, D intersect C_B empty)|D|
       =5k+max_(J subset P_B)(|J|-z_Q(J)).                    (4)

Thus each equality graph must obey both paired-neighbourhood conditions

    z_Q(J)>=|J| for all J subset P_A and all J subset P_B.    (5)

When k>=2 and the core is complete bipartite K_(2k,2k), conditions (5)
are also sufficient for beta_2=5k, SF_2=6k and positive equality.

**Proof.** A dissociation set avoiding C_B can be enlarged or exchanged
to contain all C_A. For a missing c, add it if its witness is absent or
isolated; otherwise remove that witness and add c. The only possible
selected neighbour of c is its own witness because C_B is absent. All
operations preserve dissociation and never reduce size.

With C_A fully selected, put T=D intersect X_B. Every selected witness
in T is already paired with its core owner. Its I_A centre and all its
Q-neighbours must be omitted. If t(T) counts witness pairs touched by T
and f(T) counts whole pairs contained in T, then |T|-t(T)=f(T).
There are k-t(T) available I_A centres. For each I_B-centred pair, the
centre plus its available X_A witnesses contribute two vertices if at
least one witness is available, and one if both are forbidden. If z(T)
counts opposite pairs wholly contained in N_Q(T), the exact attainable
total is

    2k+|T|+[k-t(T)]+[2k-z(T)]=5k+f(T)-z(T).

All these choices are compatible: every Q neighbour of T was excluded,
the available pairs are vertex-disjoint, and no selected C_B is present.
Remove singleton selections from T. This preserves f(T) and can only
reduce z(T), so a maximum is attained by a union of whole pairs. This
proves (4). Its reversal gives the necessary conditions (5).

For a complete core, any dissociation set meeting both core sides uses
at most one vertex of each side. Each of the 2k disjoint I-centred P3
triples contributes at most two vertices, so such a set has size at most
2+4k<=5k for k>=2. Formula (4) and (5) handle every other set. A whole
side gives beta_2=5k. The designated 6k-set I union C is minimal forming,
and the universal bound gives exact SF_2=6k.

More generally, the same sufficiency argument works for any core whose
dissociation subsets meeting both sides all have size at most k.
The condition on those mixed subsets is separate from paired expansion.

## The mixed-core condition is essential

Paired expansion alone is not sufficient for an arbitrary core. Take k
aligned disjoint K_(2,2) cores and a pair-preserving perfect matching
interface, as in the six-cycle construction L_k but without its cross-core
edges. Both paired conditions hold with equality. Within each ten-vertex
component choose i_j,k_j,y_(j,0),x_(j,1),a_(j,1),b_(j,0).
The only induced edges are the three disjoint edges i_j--y_(j,0),
k_j--x_(j,1),a_(j,1)--b_(j,0). Their union is a dissociation set of size
6k>5k. Thus the paired conditions do not imply positive equality in
general. They exactly control the one-core-side alternatives; (3) also
controls arbitrary mixed alternatives.

The [all-r six-cycle family](DEGREE_STABILITY_AND_FIRST_EQUALITY.md)
has a complete core and pair-preserving matching interface, hence also
follows from Theorem 3. Its stronger non-composition property is that no
copy of H can contain any of its degree-two vertices: in H each such
vertex has two degree-four neighbours, whereas every actual neighbour
of a degree-two vertex of L_k has degree three. This remains an obstruction
for non-induced copies. Consequently L_k has no spanning H-factor,
even allowing arbitrary attachments to all vertices of proposed blocks.

## Verification scope and remaining question

These are general proofs. The private-neighbour formula is independently
checked against literal full-subset dissociation enumeration on all
reported finite models. Complete-core controls range over every one of
the 2^16 interfaces at k=2; additional controls test arbitrary incomplete
cores, exact maximum minimal sets and the explicit mixed-core obstruction.
The remaining simplification question is to replace the full all-subsets
criterion (3) by more local conditions for arbitrary incomplete cores.
The exact recognition theorem and complete-core classification above do
not depend on resolving that simplification. No new Lean verification or
comprehensive historical priority claim is made.
