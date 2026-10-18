# A structural dissociation gain in every connected Heawood double cover

19 October 2026. The proof uses binary linear algebra and six explicit
certificates. The classification is proved algebraically; the earlier
255-signature search is not a premise. The matrix model and certificates
were proposed by the archived Oracle response, then independently checked
and expanded here. No literature-priority claim or new Lean verification
is made for this theorem.

## Theorem

Let H be a two-sheeted graph cover of the Heawood graph. Then

    beta_2(H)=14 if and only if H is disconnected.

If H is connected, beta_2(H) is either15or16. In every case SF_2(H)=16,
by the already proved triangle-free pullback and cubic degree-capacity
bound. Consequently a connected double cover has SF_2-beta_2 at most one;
it cannot preserve the gap two of two disjoint base copies. This makes
no assertion about higher covering degrees or arbitrary connected cubic
bipartite graphs.

Here a dissociation set induces maximum degree at most one. Vertices in
the point part and line part are distinct even when their labels agree.

## Switching classes as traceless matrices

Put V=F_2^3. Nonzero columns p represent Fano points, nonzero rows ell
represent lines, and incidence is ell p=0. A binary signing sigma assigns
an element of F_2 to each of the21flags. Its two-lift has adjacency

    p_i ~ ell_j iff ell p=0 and i+j=sigma(p,ell).

Switching at a base vertex interchanges its two sheet labels. Define

    Phi(sigma)=sum_(ell p=0) sigma(p,ell) p ell.

Every summand has trace ell p=0. Switching at a point changes this sum
by p times the sum of the three nonzero covectors annihilating p, which
is zero. Switching at a line similarly changes it by zero. Thus Phi
annihilates the vertex-switching space.

Phi is onto the eight-dimensional traceless matrix space. Single flags
(e_i,e_j*) for i!=j give all six off-diagonal matrix units E_ij. Also

    (e_i+e_j)(e_i*+e_j*)+E_ij+E_ji=E_ii+E_jj.

The first term is an allowed flag in characteristic two. Taking the
pairs(1,2)and(1,3)gives two independent diagonal directions. Hence the
kernel of Phi has dimension21-8=13. The vertex-to-edge switching map
has kernel exactly the two constant assignments, because the base is
connected, so its image also has dimension14-1=13. Its image is therefore
exactly ker Phi. We have proved an isomorphism

    F_2^E / vertex switchings  ~=  {3-by-3 binary matrices of trace zero}.

An invertible coordinate change g sends(p,ell)to(gp,ell g^-1), preserves
incidence and sends Phi to g Phi g^-1. Consequently conjugate invariant
matrices give isomorphic cover graphs: transport one signing by g; its
difference from the other has Phi zero and is a vertex switching.

Finally the lift is disconnected precisely for switch-trivial signings.
To see this directly, switch all signs on a spanning tree to zero. The
lifted tree consists of two trees. A negative cotree edge joins these
two components, while the all-zero signing leaves two disjoint copies.
Thus connectedness is equivalent to Phi!=0.

## Complete algebraic classification

A traceless3-by-3binary matrix has characteristic polynomial
t^3+a t+b, with a,b in F_2. There are four cases.

1. For t^3, Cayley-Hamilton gives M^3=0. A nonzero M with M^2=0 has
   image contained in kernel and therefore rank one. Choose v with
   Mv!=0 and a kernel vector independent of Mv; this gives the single
   Jordan block of length two and one zero block. If M^2!=0, the vectors
   M^2v,Mv,v for a suitable v form a basis and give the block of length three.
2. For t^3+t=t(t+1)^2, the coprime primary decomposition gives a
   one-dimensional zero block and a two-dimensional eigenvalue-one block.
   On the latter,(M+I)^2=0, so it is either I_2 or one length-two Jordan block.
3. For t^3+1=(t+1)(t^2+t+1), the coprime factors give one linear block
   and the unique irreducible quadratic block. For a nonzero vector in
   that two-dimensional block, v,Mv is a basis, fixing its companion form.
4. For t^3+t+1, neither0nor1is a root, so the polynomial is irreducible.
   Any nonzero v is cyclic: a dependence among v,Mv,M^2v would give a
   polynomial of degree at most two annihilating v; its greatest common
   divisor with the characteristic polynomial is one, a contradiction.
   The basis v,Mv,M^2v fixes the companion form.

These arguments give exactly six nonzero similarity types. Write
1=e_1,2=e_2,4=e_3 and use binary addition for the other labels. Let
S=diag(1,1,0) and C=E_13+E_21+E_32. Representatives and signings are:

| Type | Matrix | Characteristic polynomial | Twisted flags(point,line) |
|---|---|---|---|
| N1 | E_12 | t^3 | (1,2) |
| N2 | E_12+E_23 | t^3 | (1,2),(2,4) |
| S | S | t^3+t | (3,3),(1,2),(2,1) |
| J | S+E_12 | t^3+t | (3,3),(2,1) |
| C | C | t^3+1 | (1,4),(2,1),(4,2) |
| K | C+E_23 | t^3+t+1 | (1,4),(2,1),(4,2),(2,4) |

Direct outer-product summation gives the listed matrices. For example,
the flag(3,3)gives E_11+E_12+E_21+E_22. The listed representatives
realize both nilpotent types and both t(t+1)^2 types, as distinguished
respectively by M^2 and by whether the eigenvalue-one block is scalar.
The remaining two types have different characteristic polynomials.
Thus every connected double cover is isomorphic to one of these six.

## Fifteen-vertex certificates

The line triples in these coordinates are

    T1={2,4,6}, T2={1,4,5}, T3={3,4,7}, T4={1,2,3},
    T5={2,5,7}, T6={1,6,7}, T7={3,5,6}.

In each row below U and Q are ordered matched point and line lists.
W consists of additional isolated points, Z of additional isolated lines.
The notation pi means point p on sheet i in point columns, and line p
on sheet i in line columns. All entries within a part are distinct.

| Type | U(points, ordered) | Q(lines, same order) | W(points) | Z(lines) |
|---|---|---|---|---|
| N1 | 10,20,21,30,40,41,51 | 60,50,41,70,20,31,71 | empty | 61 |
| N2 | 10,11,20,31,40,41,60 | 40,61,50,71,30,11,70 | empty | 51 |
| S | 60,20,50,10,70,30 | 10,11,20,21,30,31 | empty | 41,51,61 |
| J | 60,20,70,30 | 10,11,30,31 | 10,50 | 21,41,51,61,71 |
| C | 10,20,41,60,70 | 41,40,31,10,30 | 50 | 21,51,61,71 |
| K | 20,30,31,40,50,51,70 | 11,40,31,10,20,51,60 | empty | 61 |

For A=U union W, every selected line neighborhood is determined by

    N(ell_j) intersect A
       = {p_i in A: p in T_ell and i=j+sigma(p,ell)}.       (*)

Substitution gives N(Q_r) intersect A={U_r} at every position and
N(z) intersect A=empty for every z in Z. These are all possible edges
in the selected induced graph, since each bipartition part is independent.
It is therefore exactly the displayed matching with isolates. The rows
have respectively7,7,6,4,5,7matching edges and1,1,3,7,5,1isolates;
each totals15vertices. Equation(*)and the table are explicit local
certificates, rather than an optimization claim. The accompanying checker
records each of these neighborhoods independently.

For instance, in rowN1the only twisted flag is(1,2). Among the selected
points incident with line2_0, point1_0is excluded by its twist and
point5_1by its sheet, leaving only4_0. Line6_0sees only1_0 and line6_1
sees no selected point. The remaining entries follow the same rule.

Conjugation and switching transfer these certificates to any nontrivial
signing. Hence every connected lift has beta_2>=15.

## Upper bound, rigidity and research consequence

For any dissociation set D in a cubic28-vertex graph, each selected
vertex has at least two outside neighbors. Therefore

    2|D| <= e(D,V minus D) <= 3(28-|D|),

giving |D|<=16. A disconnected double cover is two Heawood graphs;
the established base value beta_2=7 and componentwise additivity give14.
Together these prove the theorem.

The earlier255normalized-signature calculation remains useful as a
control, but is not used in the proof. In particular, this theorem settles
the strict gain in covering degree two, while the connected cubic
asymptotic coefficient and the rectangular-grid beta/psi/SF bridge remain
open. The failure of a generic strict-gain principle for prism covers
explains why the Fano matrix structure is essential here.

Reproduce local certificates and the quotient-map rank checks with:

    python3 scripts/check_heawood_matrix_certificates.py --output output/heawood-matrix-certificates.json

The complete original Oracle response and completion metadata are archived
separately. Its proposed argument has been checked here; this is not a
second independent Oracle review of the expanded note.
