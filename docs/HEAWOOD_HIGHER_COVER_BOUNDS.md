# Dissociation density and gap bounds above Heawood double quotients

19 October 2026. This extends the completed double-cover theorem to
arbitrary finite covers admitting a connected two-sheeted intermediate
cover. The covering degree above that intermediate cover is unrestricted.
The result does not assert an exact SF value in higher covers.

## General density transfer

Let B be a finite cubic bipartite graph on b vertices, and suppose
D is a dissociation set of size a. If G is a uniform t-sheeted graph
cover of B, then its full pullback is a dissociation set of size ta.
Indeed two selected neighbors of a selected lift project to the same
selected base neighbor, and local injectivity makes the lifts equal.
Counting disjoint fibers gives |pi^-1(D)|=t|D|. Thus, writing n=tb,

    b beta_2(G)>=a n.                                     (1)

The general graph pullback is already checked in DissociationCover.lean;
the finite fiber count is the written argument just given. Cubicity and
bipartiteness also pull back. Apply the proved compensation inequality
7SF_2<=3n+2beta_2, and put g=SF_2-beta_2. It gives

    7g<=3n-5beta_2,
    7b g<=(3b-5a)n.                                      (2)

This uses one actual dissociation set in the intermediate graph, counted
once per fiber. It does not sum incompatible quotient selections or
reuse their surplus. Connectedness is not needed for(1)or(2).

## Every connected double quotient improves the coefficient

Suppose G->H->Heawood, where H is a connected two-sheeted cover and
G->H is t-sheeted. Then b=28 and the structural double-cover theorem
supplies a>=15. Consequently

    beta_2(G)>=15t=15n/28,
    SF_2(G)-beta_2(G)<=floor(9n/196).                      (3)

Here n=28t, so the gap bound also reads floor(9t/7). The coefficient
9/196 is strictly smaller than the general cubic coefficient1/14.
No assertion is made that(3)is sharp for this subclass. A cover of
Heawood without a connected double quotient is outside this conclusion.

In particular(3)holds for every connected regular Heawood cover with a
nontrivial finite2-group as deck group, and for every connected regular
cover with a cyclic deck group of even order.

For completeness, any nontrivial finite2-group has an index-two normal
subgroup. Its class equation shows that its center has even order; taking
a suitable power of a nonidentity central element gives a central subgroup
of order two. Induct on group order: for order two the trivial subgroup
works; otherwise apply induction to the quotient by this central subgroup
and take the preimage of an index-two subgroup. For a cyclic group of
even order, the even powers are directly an index-two subgroup.

Quotient a connected regular cover by that subgroup. The subgroup orbits
above each base vertex give two intermediate vertices; freeness and
transitivity of the deck action on each fiber give two such orbits
uniformly. The original graph covers this quotient locally bijectively:
above a fixed vertex, distinct neighbors have distinct base images, and
every adjacent quotient vertex has its unique neighbor lift. The same
argument makes the quotient a two-sheeted cover of the base. It is
connected as the image of a connected graph. These facts justify the
intermediate cover required in(3), rather than assuming every even-degree
cover has such a factorization.

## Two double-cover types have a sixteen-vertex certificate

Use the coordinates and switching invariant Phi of
HEAWOOD_DOUBLE_COVER_GAIN.md. Suppose the quotient matrix has
characteristic polynomial t^3+t=t(t+1)^2. The proved algebraic classification
reduces it to precisely two types:

    S=diag(1,1,0), or J=S+E_12.

Both quotient graphs have beta_2=16, by the certificates below and the
ordinary cubic upper bound floor(3*28/5)=16. This establishes a sufficient
algebraic condition for beta=16; it does not claim the converse without
a proof excluding16-sets in the other four types.

Vertex labels pi mean label p on sheet i, with point and line columns
representing different parts. U and Q list matching endpoints in order;
Z lists additional isolated lines. There are no additional selected points.

| Type | Twisted flags | U(points) | Q(lines) | Z(lines) |
|---|---|---|---|---|
| S | (3,3),(1,2),(2,1) | 60,20,50,10,70,30 | 10,11,20,21,30,31 | 41,51,61,71 |
| J | (3,3),(2,1) | 40,41,20,31,51,70,61,50 | 10,31,40,41,51,60,61,70 | empty |

The line-neighborhood rule from the earlier note gives exactly U_r at
each Q_r and the empty set at each Z. The selected induced graphs are
respectively six matching edges plus four isolates, and eight matching
edges. Each has sixteen vertices. Both full local graph assertions and
their selected cardinalities are now checked in Lean4.33.0, without
native-decide or compiler-trust axioms.

If G has a double quotient of either type, use b=28,a=16 in(1)--(2):

    beta_2(G)>=16t=4n/7,
    SF_2(G)-beta_2(G)<=floor(n/49)=floor(4t/7).             (4)

The finite graph certificates and the conditional arithmetic implications
for(3)--(4)have six Lean axiom audits. Group factorization, matrix
classification and arbitrary finite-fiber counting retain written proofs.
The sequential local run takes13.622seconds across five modules, with
peak child RSS1,639,612,416bytes; preflight finds no active lean/lake
processes and records memory. The exact statements are in
formal/StarForming/HeawoodCertificates.lean and the full receipt in
output/heawood-certificates-formal-check.json. Only standard axioms occur.

## Binary-character rank, including nonabelian deck groups

For a connected regular Heawood cover with arbitrary finite deck group K,
put r=dim_F2 Hom(K,F_2). A nonzero binary character chi:K->F_2 gives
a connected double quotient. Connectedness of the full cover says that
its cycle voltages generate K: after setting spanning-tree voltages to
the identity, the vertices in the fiber reached by closed walks are
exactly the subgroup generated by cotree voltages. This argument does
not assume K is abelian.

Composing each character signing with Phi gives a linear map

    Hom(K,F_2) -> sl_3(F_2).

Its kernel is zero. A zero matrix would mean a switch-trivial character
signing, so chi would vanish on every cycle voltage and therefore on K.
Consequently these quotient invariants form an r-dimensional subspace W.
In particular r<=8, in agreement with the eight cotree generators.

If W contains a matrix with characteristic polynomial t^3+t, bound(4)
applies. The threshold is now proved in TRACELESS_SUBSPACE_THRESHOLD.md:
every four-dimensional subspace does contain such a matrix. It follows
from the existing1-specdimension theorem of de Seguins Pazzis; a complete
elementary binary proof is provided as well. Strictly upper-triangular
matrices give an avoiding subspace of dimension three, making the threshold
sharp. Thus every connected regular Heawood cover with at least four
independent binary characters of its deck group unconditionally satisfies
beta>=4n/7and gap<=floor(n/49). The elementary abelian case(F_2)^r,
4<=r<=8,is a special case. The general statement also covers groups
of arbitrarily large order: the dihedral group of order2^m, m>=3,
times(F_2)^2has four independent characters. It is generated by four
elements, so assigning these generators to four of the eight cotree
edges, with identity on every other edge and all tree edges, constructs
a connected regular Heawood cover. Its order is14*2^(m+2), unbounded
as m grows. The four characters are rotation parity, reflection parity,
and the two additional binary coordinates. The dihedral relation is
respected because the rotation order is even. This establishes that
the stronger bound applies to an unbounded class; no equality claim follows.
The subspace enumeration remains discovery only, and is not used in
the dimension proof. The original Oracle research answer is complete;
its proposed argument and the cited primary source were checked.

## Verification and scope

Reproduce with

    python3 scripts/check_heawood_matrix_certificates.py --output output/heawood-matrix-certificates.json
    python3 scripts/check_heawood_cover_transfer.py --output output/heawood-cover-transfer-controls.json
    python3 scripts/check_cover_pullback_formal.py --audit heawood --lean PATH_TO_LEAN --output output/heawood-certificates-formal-check.json

The higher-cover controls test local bijectivity, sheet counts and actual
pulled-back certificates in96cyclic covers above the displayed quotients,
five elementary abelian covers of ranks4through8,and three nonabelian
dihedral-times-binary covers. These104controls check27,552lifted vertices
in total. The nonabelian examples have orders448,896,1792and displayed
dissociation sets of sizes256,512,1024,respectively.
They are controls for the uniform proof, not its justification. The
subspace exploration checks its own extension and deduplication counts
but does not replace the structural argument now supplied separately.

All conclusions concern the star-forming/dissociation collaboration.
They neither settle the rectangular-grid beta/psi/SF bridge nor improve
the existing5/6sub-quorum bound. The submitted DMGT manuscript is preserved.
