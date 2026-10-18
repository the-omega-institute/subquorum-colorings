# A sharp traceless threshold and its Heawood-cover consequence

19 October 2026. The matrix-space dimension bound used here is an existing
result of Clement de Seguins Pazzis, not a newly claimed theorem. The
binary traceless corollary and its application to our cover certificates
are developed explicitly below, with a self-contained special-case proof.
The original Oracle answer supplied this shorter argument and the reference;
both have been independently read and checked. A locally developed
alternative proof, written before reading that answer, is preserved in
TRACELESS_SUBSPACE_QUADRATIC_PROOF.md. No priority claim is made for
the traceless corollary or the elementary special-case proof either.

## The traceless threshold

Every subspace W of sl_3(F_2) with dimension at least four contains a
matrix with characteristic polynomial t^3+t. The threshold is sharp:
the strictly upper-triangular matrices form a three-dimensional space
whose matrices all have characteristic polynomial t^3.

Write q(M) for the second characteristic coefficient. For traceless M,

    chi_M(t)=t^3+q(M)t+det(M).

Thus M has both0and1as eigenvalues precisely when det(M)=0,q(M)=1.
If W avoids this characteristic polynomial, put S=W+F_2 I_3. Adding
the identity interchanges0and1in the spectrum, so no matrix of S has
both eigenvalues. Since tr(I_3)=1,dim(S)=dim(W)+1. The next elementary
dimension bound gives dim(S)<=4, proving dim(W)<=3 by contraposition.

## Two-dimensional trivial-spectrum lemma

Let R be a linear subspace of End(F_2^2) with no matrix having eigenvalue
one. Then dim(R)<=1. For a nonzero vector u, the evaluation image R u
does not contain u, so has dimension at most one. If dim(R)>=2, take
a basis u,v and nonzero A,B in R with Au=0,Bv=0, using rank-nullity
for the two evaluations. A nonzero singular2-by-2matrix without eigenvalue
one is nilpotent: its other eigenvalue is its trace in F_2, which cannot
be one. It has rank one, with image equal to kernel. Consequently

    Av=u, Bu=v, and (A+B)(u+v)=u+v,

contradicting the hypothesis on R. This proves the lemma.

## Three-dimensional dimension bound

Let S be a linear subspace of End(E), E=F_2^3, no member of which has
both0and1as eigenvalues. We prove dim(S)<=4.

First there is a nonzero x such that no nonzero A in S has image
contained in F_2 x. Otherwise, for each of the seven nonzero x choose
a nonzero rank-one operator A_x=x phi_x in S. Since A_x is singular,
phi_x(x)=0, or it would also have eigenvalue one. For distinct x,y
we cannot have phi_x(y)=phi_y(x)=1: A_x+A_y would interchange x,y,
fix x+y, and still be singular, since its image has dimension at most
two. Thus it would have both eigenvalues.

But each nonzero covector phi_x takes value one on four vectors, none
equal to x or zero. There would be7*4=28oriented pairs(x,y), with at
most one orientation for each of the binomial(7,2)=21unordered pairs.
This contradiction proves the claimed direction x exists.

Fix that x and let K={A in S:Ax=0}. Every A in K induces a linear
operator on E/F_2 x. This quotient-operator map is injective: an element
in its kernel has image in F_2 x and is zero by the choice of x.
None of the quotient operators has eigenvalue one. In a basis beginning
with x, the characteristic polynomial of A is t times that of the
quotient; eigenvalue one below would give both zero and one above.
The two-dimensional lemma gives dim(K)<=1. Finally evaluation at x
has image of dimension at most three, so

    dim(S)=dim(K)+dim(S x)<=1+3=4.

This establishes the dimension bound and the traceless threshold.
The counting uses actual distinct oriented pairs and excludes reciprocal
pairs before summing, so no pair supplies two units of the same capacity.

## Relation to the literature

Clement de Seguins Pazzis, *Spaces of matrices with a sole eigenvalue*,
[arXiv:1105.1872v3](https://arxiv.org/abs/1105.1872v3), Definition1and
Theorem2,printed pages2--3, defines a1-specspace by requiring at most
one eigenvalue **in the base field**, allowing an empty base-field spectrum.
Theorem2bounds its dimension by1+binomial(n,2), except for n=2in
characteristic two. It therefore applies directly to S above with
n=3,K=F_2. The n=2exception is irrelevant: our auxiliary two-dimensional
space has the stronger condition of no nonzero base-field eigenvalue.

The original PDF and definition/theorem text were fetched and inspected;
the separate literature receipt preserves the exact statements and URL.
The full general matrix-space theorem is not our contribution. The
short argument above supplies a standalone proof of the specific binary
case needed by the covering theorem.

## Unconditional high-rank covering theorem

Let G be a connected regular cover of the Heawood graph with finite deck
group K and r=dim_F2 Hom(K,F_2)>=4. Necessarily r<=8, since the base
cycle rank is eight. The group K need not be abelian or a2-group.
Its binary characters, followed by the switching-to-matrix map Phi, inject
into sl_3(F_2), as proved in HEAWOOD_HIGHER_COVER_BOUNDS.md. The image
therefore contains a matrix with characteristic polynomial t^3+t.
The corresponding connected double quotient has a sixteen-vertex
dissociation certificate in one of its two possible similarity types.
Pull back that one certificate to G. It gives

    beta_2(G)>=4|V(G)|/7.

The proved cubic compensation inequality then gives

    7(SF_2-beta_2)<=3n-5beta_2<=n/7,
    SF_2(G)-beta_2(G)<=floor(n/49).

This conclusion holds for every such cover, without enumerating voltage
assignments, subspaces or graph optima. It neither identifies equality
cases nor gives an exact SF value in higher covers. Its graph certificates
and conditional density-to-gap arithmetic are Lean checked; the general
matrix-space, character and fiber-count arguments have written proofs.
The dihedral-times-two-binary-factors construction in the covering note
gives examples of unbounded order. Elementary abelian covers of ranks
four through eight are a particularly direct special case.
