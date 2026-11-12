# Direct witnesses in the colour exchange and a stronger cubic bound

All graphs are finite, simple and bipartite. A forming star has two leaves
and need not be induced. S is an inclusion-minimal two-star-forming set
whose selected components are stars, single edges or isolates. Put
d=|S|-beta_2(G), with beta_2 the unrestricted dissociation number.

**Theorem.** Every such selection in a nonempty cubic graph satisfies

    d<=floor(n/22).                                      (1)

This improves the earlier floor(7n/146) certificate in this selected-star
class. It is not asserted graph-sharp, and does not bound arbitrary
minimal sets having more complicated selected components. It also does
not settle full rectangular grids or a universal mixed-direction5/6 gain.

The new ingredient is a stronger colour exchange: direct centre witnesses
can be retained as well as leaf witnesses. The proof works at any degree
and gives a sharp correction to a false proposed general inequality.

## One permitted witness assignment

Use the assignment proved in SHARP_SELECTED_STAR_GAP.md. There are c
nontrivial star centres C, e=2c+s leaves, and selected isolates I. Put
m equal to the number of selected edge-component vertices. A centre is
counted in q when none of its leaves has a private outside deletion
witness. Choose one witness for each leaf, including one private witness
at every other centre, and one direct centre witness for each q-centre.

These distinct outside witnesses form W, of size e+q. Each has exactly
one active selected owner and at most one selected-isolate helper. A leaf
witness's owner is that leaf; a direct witness's owner is its centre.
No witness meets a selected edge endpoint or another active owner. Let

    h(i)=|N(i) intersect W|,
    a=#{i in I:h(i)=1}, b2=#{i:h(i)=2}, b3=#{i:h(i)>=3},
    t=a+b2+b3, z0=#{i:h(i)=0},
    U=V minus (S union W), u=|U|.

The compatible centre/helper repair matching has cardinality mu, with
both types of endpoint capacity one. The established ledgers are

    J=c+s+2q-t-b2-2b3>=0,
    R=c-q+b2+b3-mu>=2d,                                  (2)
    n=5c+2s+q+t+m+z0+u,
    B=2|S|-n=c-q+t+m+z0-u>=2d.                           (3)

The final inequality follows independently from beta_2>=n/2. The witness
incidence and compatible-repair arguments supplying (2) are established
inputs, not newly allocated resources in the present proof.

## Retain all witnesses of one colour

Fix the bipartition A,B. Let W_A=W intersect A and let I_A^* comprise
the selected isolates adjacent to W_A. Define

    D_A=((S minus C) union W_A) minus I_A^*.               (4)

This is dissociation. Every star centre is omitted. A retained leaf sees
at most its one chosen leaf witness. A chosen leaf witness retains its
leaf owner, while its possible helper is removed. A direct centre witness
loses both its centre owner and any helper, so is isolated. Selected edge
components retain their matching edges and meet no witness. Retained
isolates have no neighbour in W_A. Finally W_A is independent. This list
accounts for all possible induced edges, with each vertex used once.

Define D_B symmetrically. An isolate has all neighbours in just one
witness colour, so I_A^* and I_B^* are disjoint and their union has size t.
Consequently

    |D_A|+|D_B|=2(|S|-c)+(e+q)-t
                  =2|S|+s+q-t.

Both sets have size at most beta_2(G). Therefore the stronger ledger is

    T'=t-s-q>=2d.                                       (5)

The previous leaf-only exchange gave t-s>=2d. Including direct witnesses
produces the extra q without requiring a clean leaf at every centre.

## A corrected general excess inequality

Write X=T'-2d>=0, Y=R-2d>=0. Direct expansion gives

    (3X+Y+J)/2=c+t-s-q-(b3+mu)/2-4d>=0.

Subtracting this bound for4d from B yields

    4beta_2-2|S|-n>=m+z0-u+s+(b3+mu)/2.                 (6)

This is valid for every permitted witness assignment, even when d<=0.
In particular

    4beta_2>=2|S|+n-u.                                  (7)

Thus the uncorrected inequality holds if one permitted choice exhausts
the outside vertices, U empty. More generally it holds whenever
u<=m+z0+s+(b3+mu)/2. Exhaustion concerns one actual chosen W; having
some witness at each outside vertex is not the same condition.

The coefficient of u in (7) is sharp. In the exact padding family
P_(r,r), r>=2, the natural leaf witnesses have q=s=b3=mu=m=z0=0,
t=2r and u=2r. The graph has n14r, |S|8r, beta_2=7r. Thus the left
side of (6) equals-2r=-u, attaining (7) exactly. The previously proposed
uncorrected general inequality is therefore false, while (6)-(7) hold.

## The cubic counting identity

For a cubic graph the whole-cut capacity from
FULL_DEGREE_CAPACITY_FOR_SELECTED_STARS.md is

    F=3u-2c+s-3t+3q-2m-3z0>=0.                         (8)

It counts all S--U demand against the single total capacity3u. No unused
vertex is credited separately for different selected component types.
The following exact identity incorporates the stronger exchange:

    n=2J+2R+4T'+5B+2F
         +2(s+q+b3+mu+z0).                             (9)

For completeness, F+3B=m+c+s. Substitution in the count of n gives
n=4c+2t+2z0+2F+5B. Also J+R+T'=2c-b3-mu and t=T'+s+q.
These two substitutions give (9), or it may be checked coefficient by
coefficient in the ten nonnegative count variables.

Every term except R,T',B is nonnegative. By (2),(3),(5), their displayed
contributions total at least4d+8d+10d=22d. This proves (1), including
the trivial nonpositive-gap case. Unlike the earlier cubic certificate,
no negative coefficient of b3 occurs and no relaxation optimizer is used.

Equality in the real numerical ledger is possible: c=a=2d, m=4d, u=6d,
and all q,s,b2,b3,mu,z0 zero, gives n22d and J=F=0,R=T'=B=2d.
It is only a numerical resource point. It neither constructs a graph
with beta=n/2 nor establishes the graph-sharp coefficient1/22.

## Signed boundary version at maximum degree three

Suppose instead that the maximum degree is at most three, without a
minimum-degree assumption. For a vertex set Z put
epsilon_Z=sum_(v in Z)(3-deg(v)). The exact degree-sum identity gives

    Fhat=F+epsilon_S-epsilon_U
         =(c+s+2q-sum_(i in I)h(i))
             +2|E(G[U])|+|E(U,W)|>=0.                  (10)

Indeed |E(S,U)|=sum_(v in S)deg(v)-3e-m-q-sum h(i), and the residual
degree sum over U is2|E(G[U])|+|E(U,W)|. Subtracting these exact sums
proves (10). The incidence cap makes its first term nonnegative.

Replace F by Fhat-epsilon_S+epsilon_U in (9). Then

    d<=floor((n+2epsilon_S-2epsilon_U)/22).               (11)

The signed deficits refer to the disjoint actual sets S,U of the same
witness assignment. This does not require a positive numerator or d>0.
For cubic graphs both deficits vanish, recovering (1).

## Reproduction and review scope

The standalone entry point is
`python3 -B scripts/check_direct_witness_cubic_bound.py`, with assertions
enabled. It imports generic graph and witness utilities from the two
preceding public checkers; all three files must be present. It constructs
both actual exchange sets, verifies dissociation and their exact size
sum, checks (5)-(11), and compares exact one-part optima with independent
literal optimizers on its stated finite models. The general theorem uses
the proofs above, not extrapolation from those models. The finite report
covers876 graph inputs,275208 selected subsets,15761 eligible minimal
sets and23499 witness allocations, including15932 with q>0. Both actual
exchange sets are checked at every allocation. There are2512 cubic
allocations and5752 subcubic signed-boundary allocations. No cubic
positive gap occurs in this small range, so these checks do not establish
graph sharpness. Ten targeted models separately include positive gaps,
positive gaps with direct-only centres, and sharpness of the u correction.

The stronger exchange and correction (6)-(7) were proposed in the Oracle
research response and independently checked by Codex. The new cubic
identity (9), bound (1), and signed extension (11) were subsequently
derived by Codex. Exact-source independent review is pending. No new
Lean verification, literature-priority, unrestricted-SF or graph-sharpness
claim is made.
