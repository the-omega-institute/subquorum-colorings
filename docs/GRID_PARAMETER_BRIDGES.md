# Exact scope of the upper-domination comparison on grids

Write Gamma(G) for the maximum size of an inclusion-minimal dominating set.
The classical bipartite identity Gamma=alpha and the known dissociation formula
give the exact baseline for a prospective grid coloring upper bound. They
do not by themselves bound the sub-quorum coloring number from above.

## A direct proof of the bipartite identity

Let G=(A,B;E), and let D be a minimal dominating set. Write I for the vertices
isolated in G[D]. Every a in (D intersect A)\I has an outside private neighbor
p_a: otherwise deletion of a would still dominate every vertex, including a
itself, which already has a neighbor in D. Thus N(p_a) intersect D={a}.
The p_a's are distinct and lie in B.

The set

    (D intersect B) union (I intersect A) union {p_a:a in (D intersect A)\I}

is independent and has size |D|. Its B-side vertices have no edges among
themselves. Its retained A-side vertices have no neighbors in D, nor in the
private-neighbor set. Hence |D|<=alpha(G). Conversely a maximum independent
set is maximal independent, therefore minimal dominating, giving Gamma>=alpha.
This proves Gamma=alpha without a grid-specific domination argument.

For P_m square P_n, the larger checkerboard class has ceil(mn/2) vertices.
A matching of size floor(mn/2) bounds every independent set by ceil(mn/2).
When one dimension is even, pair along that dimension. When both are odd,
pair the first m-1 rows vertically, then pair consecutive columns in the last
row, leaving one corner. Thus Gamma=ceil(mn/2).

## The boundary term and all equality cases

Use the [known dissociation formula F(m,n)](GRID_RESULTS.md), and put

    g(k)=k-2 floor(k/3),
    delta(m,n)=max{(m mod 2)g(n),(n mod 2)g(m)}.

Since ceil(2k/3)=k-floor(k/3), expanding each term of F gives

    2 beta_2(P_m square P_n)-mn=delta(m,n).

Consequently the exact gap is

    epsilon(m,n)=beta_2-Gamma=(delta(m,n)-(mn mod 2))/2.   (1)

For positive dimensions, epsilon=0 precisely when either both sides are
even, or both sides belong to {1,3}. Indeed g(2a)>0; on odd k, g(k)=1 exactly
for k=1,3, and otherwise g(k)>=3. The parity expansion then proves the claim.

| Grid | Gamma | beta_2 | epsilon |
| --- | --- | --- | --- |
| 2-by-3 | 3 | 4 | 1 |
| 3-by-3 | 5 | 5 | 0 |
| 3-by-4 | 6 | 7 | 1 |
| 4-by-4 | 8 | 8 | 0 |

Since beta_2<=psi_sq, an upper bound psi_sq<=Gamma fails on 2-by-3. On all
rectangles, any proposed bound psi_sq<=Gamma+c(m,n) needs c>=epsilon. Choosing
c=epsilon makes the proposed bound exactly the existing target psi_sq<=F;
the domination identity supplies the baseline, not the missing upper proof.
On even-by-even grids epsilon vanishes and the missing bound is psi_sq<=Gamma.

The [double star](STAR_FORMING_CERTIFICATES.md) likewise shows that a comparison
psi_sq<=SF_2 cannot hold on all bipartite graphs. Neither comparison can be
extended to a broader graph class from the parameter equalities alone.

## Verification

The controls in `develop/check_star_forming_certificates.py` independently
enumerate dissociation sets and minimal dominating sets of all 16 rectangular
grids with dimensions 1 through 4, and compare their maxima with (1). The
general statements follow from the proofs and parity algebra above.
