# An alternative quadratic proof of the binary traceless threshold

19 October 2026. This proof was developed locally while the original
Oracle research stream28109was still active, before its answer was read.
The shorter primary proof and attribution to the existing matrix-space
theorem are now in TRACELESS_SUBSPACE_THRESHOLD.md. This alternative
argument is retained as independently developed supporting mathematics.
The preceding subspace enumeration was discovery only. The proof below
uses quadratic forms and three explicit matrix representatives; its
coverage follows from group orders and invariant pairs, not a list of
all four-dimensional subspaces. No historical priority claim is made.

## Theorem

Every linear subspace W of sl_3(F_2) of dimension at least four contains
a matrix with characteristic polynomial t^3+t. The threshold is sharp:
the three-dimensional strictly upper-triangular space is nilpotent.

Write q(M) for the second characteristic coefficient and d(M)=det(M).
For traceless M its characteristic polynomial is t^3+q(M)t+d(M).
The forbidden matrices are precisely q=1,d=0. Let K denote the matrices
with characteristic polynomial t^3+t+1. If W avoids the forbidden type,
every element of W with q=1 belongs to K. We derive a contradiction
already for a four-dimensional subspace.

## The ambient quadratic form

On traceless matrices, polarizing q gives

    B(M,N)=q(M+N)+q(M)+q(N)=tr(MN).

Put the diagonal entries a,b,a+b and pair each upper off-diagonal entry
with its opposite lower entry. Then q has the explicit form

    a^2+ab+b^2 + x1*y1+x2*y2+x3*y3.                       (1)

Its polar form is nondegenerate and alternating. The first summand is
an anisotropic binary plane and the other three are hyperbolic planes.
In particular no four-dimensional subspace has q identically zero.
Here is a direct count-based proof of this last standard fact, using
the formula rather than enumerating matrices. The sum of(-1)^q is
(-2)*2^3=-16, so q has(256-16)/2=120zeros. If a four-dimensional
totally singular subspace existed, its basis e1,...,e4 could be paired
with dual vectors f1,...,f4 under B. Adding suitable e-vectors makes
each q(fi)=0 and each B(fi,fj)=0, without altering duality: first add
ei when needed to fix q(fi), then for i<j add B(fi,fj)ei to fj.
The latter additions preserve q(fj)because B(fj,ei)=0 for i!=j.
The resulting hyperbolic basis would give four hyperbolic planes,
with(256+16)/2=136zeros, a contradiction.

## Three local facts about irreducible matrices

We prove the following facts for K:

1. There are no four distinct elements of K pairwise orthogonal under B.
2. If A,D,A+D all belong to K, then D=A^2 or A^4. Thus such a plane
   consists of the nonzero elements of span(A,A^2), since A^4=A+A^2.
3. No element of K is orthogonal to both A and A^2 for any A in K.

Here is a complete algebraic reduction proving all three facts. The
polynomial t^3+t+1 is irreducible over F_2. Every matrix in K is conjugate
to its companion matrix

    A = [0 0 1; 1 0 1; 0 1 0].

Indeed every nonzero vector is cyclic, so choosing v,Av,A^2v fixes the
companion form. Its commuting algebra is F_2[A], a field of order eight:
a commuting map is determined by the image of a cyclic vector. Its
invertible centralizer consequently has order seven. Since
|GL_3(F_2)|=(8-1)(8-2)(8-4)=168, the conjugacy class K has24elements.
The matrix A has order seven and A^4=A+A^2.

Consider conjugation by A on K. The three elements A,A^2,A^4 are fixed.
Take the following representatives:

    R = [1 1 1; 1 1 0; 1 0 0],
    T = [0 1 1; 0 0 1; 1 0 0],
    U = [1 0 1; 1 1 0; 0 1 0].

Direct multiplication gives the following small identity table. Each
representative has characteristic polynomial t^3+t+1 and fails to commute
with A. The displayed trace pairs are invariant under conjugation by A.

| Representative | tr(AD) | tr(A^2 D) | det(A+D) |
|---|---|---|---|
| R | 0 | 1 | 0 |
| T | 1 | 1 | 0 |
| U | 1 | 0 | 0 |

Their orbits each have length seven, because the acting group has prime
order and none of these representatives is fixed. The three orbits are
disjoint because their trace pairs differ. Together with the three fixed
elements they account for3+3*7=24elements, proving completeness.
Also tr(A*A^2)=tr(A*A^4)=1, by A^3=A+I and A^4=A+A^2.

It follows that the elements of K distinct from A and orthogonal to A
are exactly

    R_i=A^i R A^(-i),  i in Z/7Z.                        (2)

Three further direct trace identities are

    B(R,R_1)=0, B(R,R_2)=1, B(R,R_3)=1.                 (3)

Symmetry and invariance give the values for negative differences too.
Thus distinct R_i,R_j are orthogonal exactly when j-i=+1or-1modulo7.
Their orthogonality graph is a seven-cycle, which has no triangle.
If four elements of K were pairwise orthogonal, conjugate one to A;
the other three would make a triangle in this seven-cycle. This proves1.

For2, conjugate the first element to A. Every element in the R orbit
has B(A,D)=0 and therefore q(A+D)=0, so its sum is not in K. In the
T and U orbits the table gives determinant zero, again excluding K.
Only A^2,A^4 remain, and their sums with A are respectively A^4,A^2.

For3, an element orthogonal to A is either A itself or in the R orbit.
But B(A^2,A)=1, and the table gives B(A^2,R_i)=1 for every i. This
excludes every possibility. The local facts are proved.

## Every four-dimensional restriction contradicts those facts

Suppose W has dimension four and avoids the forbidden matrices.
By(1),q|W is not identically zero. The alternating polar form restricted
to W has rank zero,two or four. Let Rad be its radical.

If its rank is zero, q|W is a nonzero linear functional. Its eight
q=1vectors include four distinct, pairwise orthogonal elements of K,
contrary to local fact1.

If its rank is two, Rad has dimension two. If q vanishes on Rad,
choose x in W with q(x)=1. All four vectors of x+Rad have q=1,
and every pair is orthogonal, again contradicting1. If q does not
vanish on Rad, choose any x outside Rad. The three-dimensional space
Rad+span(x)has zero polar form and a nonzero linear q. Its four q=1
vectors give the same contradiction.

Finally suppose the restriction is nondegenerate, of rank four. It has
an anisotropic two-dimensional subspace P. To justify this directly,
split the symplectic space into two orthogonal nondegenerate planes.
A binary quadratic plane is either hyperbolic or anisotropic. If either
is anisotropic it supplies P. If both are hyperbolic, with bases e_i,f_i
and q(e_i)=q(f_i)=0,B(e_i,f_i)=1, take

    a=e1+f1, b=e1+e2+f2.

Then q(a)=q(b)=q(a+b)=1, so span(a,b)is anisotropic.
Every nonzero element of P belongs to K. By local fact2 these three
elements are A,A^2,A^4for some A, after conjugation if necessary.
The orthogonal complement P^perp inside W is a nondegenerate plane,
so its quadratic form is not identically zero. It has an element C
with q(C)=1. Then C belongs to K and is orthogonal to both A and A^2,
contradicting local fact3.

All three ranks are impossible. This proves the theorem. Every larger
W contains a four-dimensional subspace, giving the full statement.

## Covering consequence and verification

For a connected regular Heawood cover with elementary abelian deck group
(F_2)^r, its character switching invariants form an r-dimensional subspace
of sl_3(F_2). For every4<=r<=8, the theorem supplies a double quotient
with characteristic polynomial t^3+t. The two sixteen-vertex certificates
and the general transfer therefore give

    beta_2(G)>=4|V(G)|/7,
    SF_2(G)-beta_2(G)<=floor(|V(G)|/49).

The character injection, cover factorization and compensation proof are
given in HEAWOOD_HIGHER_COVER_BOUNDS.md. This establishes the formerly
conditional rank-at-least-four consequence. It does not classify equality
or determine SF exactly in these covers.

The dedicated checker independently verifies the three small matrix
representatives and the trace identities. The earlier subspace discovery
counts are retained in a separate receipt; those counts are not
premises of this proof. The quadratic-space argument and orbit reduction
are written general proofs, not newly Lean-formalized. The two local
sixteen-vertex graph certificates and the density-to-gap arithmetic have
their separate six-declaration Lean audit.

Reproduce the small local identities with
`python3 scripts/check_traceless_local_identities.py --output output/traceless-local-identities.json`.
The earlier subspace controls are in output/heawood-cover-transfer-controls.json.
