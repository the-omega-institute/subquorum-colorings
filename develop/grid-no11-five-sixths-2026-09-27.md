# No11 interfaces and unconditional five-sixths matching absorption

Date: 2026-09-27. Continuation of `grid-parity-transport-2026-09-27.md` at commit `bee8bf429c0dc0ff53c75775496113c7782f9115`, in the same PR #1. The preceding beta_2, directional, residual and four-fifths proofs are retained.

**Status.** This note supplies an ordinary written proof, for every positive even m,n and every feasible representative pair, of

    |T| + (5/6)|M| <= mn/2.

The coefficient-one bound and unrestricted all-parity rectangular coloring formula remain UNPROVED. The Fibonacci interface is exact at its stated types; no compression of the entire weighted grid frontier to 21 states is asserted. Finite checks accompany the paper proof. No Lean verification, independent referee approval, CI result, or worldwide priority claim is made.

## 1. The precise six-bit interface

Write X_j for the length-j binary words containing no adjacent ones. The repository has a formal theorem `D5/S1/Words/AdmissibleWords/AdmissibleCount.admissibleWord_card_eq_fib` proving |X_j|=Fib(j+2), with Fib(0)=0,Fib(1)=1. Its inspected Lean blob is `af8e217d2a3b279bab05d10ca9b965d4d74c2109`. Thus the 64 unrestricted six-bit words contain 21 admissible words and 43 excluded words; |X_7|=34 and |X_8|=55.

The symbols 12|34 in a four-port pairing mean the pairs {1,2} and {3,4}. They are port labels, not a numerical derivation of 21 or 34. The label 10 for that pairing can be a vector in F_2^2 after fixing the four port labels. The following connection uses a proved bijection instead.

**Proposition 1.1 (an explicit no11/matching/even-gap bridge).** There are bijections

    X_j <-> matchings of P_(j+1) <-> even-gap subsets of [j+1].

Here a subset S is even-gap when every maximal interval of its complement has even length.

**Proof.** A one at position i selects the edge {i,i+1}. Two selected edges intersect exactly when their indices are consecutive, proving the first bijection. Send a matching to its set S of unmatched vertices. Each component of the matched-vertex set is an interval tiled by adjacent matched pairs, so its length is even. Conversely each even interval has a unique perfect matching by its first two vertices, next two vertices, and so on. Applying this to every complementary interval reconstructs the matching and proves both inverse identities. This includes j=0. QED.

The same path matching can tile a two-row ladder: every selected edge occupies a two-column horizontal domino pair, and every unmatched column carries a vertical domino. Reading the leftmost column shows that these are exactly its perfect matchings. Thus the no11 word is an exact encoding of a restricted one-dimensional matching choice, with all selected edges recoverable.

The even-gap indexing sets of East, Johnson and Kambites [EJK], Definition 6.4, use n boundary points and have f_n elements with f_0=f_1=1. Therefore our X_6 corresponds to their SEVEN-point index set of size 21; their six-point index set has size 13. Their Theorem 6.14 is a faithful involutive representation of ordinary Temperley-Lieb diagrams over a nontrivial idempotent semiring, and does not preserve the ordinary tensor product. It does not by itself preserve the current graph's capacities, exposed matching obligations, or colored-support weights.

For arbitrary real weights w_i, the maximum of sum w_i x_i over X_j obeys

    V_0=0, V_1=max(0,w_1),
    V_i=max(V_(i-1),V_(i-2)+w_i).

Splitting on the last bit proves this recurrence, including negative weights. The repository's `PathStableSetPolytope.convexHull_vertices` proves that the associated convex hull is exactly 0<=x_i<=1, x_i+x_(i+1)<=1. Thus a one-dimensional weighted matching choice can be treated without losing its objective. It does not license forgetting additional two-dimensional boundary data.

The new grid improvement below keeps those data. The essential refinement distinguishes an internal matching edge from an unused port. Fibonacci counting alone is not an assumption in the absorption proof.

## 2. Residual input and a stronger attachment budget

Throughout the remaining sections, m,n are positive even integers. A feasible representative pair consists of a matching M and a disjoint T, every t in T having at most one neighbor in A=T union V(M). Put P=V(M), B=V\A. The source-faithful coloring reduction gives psi_sq<=Omega=max(|T|+|M|).

Partition the full rectangle into aligned 2-by-2 tiles. Write t_Q for the number of T vertices. A tile with t_Q=2 is saturated. For a deficient tile let h_Q count its internal matching edges and s_Q count matching edges from it to saturated tiles. Set

    r_Q=2-t_Q-h_Q-s_Q.

Gamma retains matching edges between two different deficient tiles; parallel edges and endpoint corners are retained. Let deg_Q be its residual degree. The earlier residual lemmas prove r_Q in {0,1,2}; deg_Q<=1 for r_Q=0 and deg_Q<=2r_Q otherwise; and independence of the zero-capacity residual leaves. A saturated tile incident to a matching edge has P at its attachment corner, T at the two adjacent corners, and B at the opposite corner. P corners of different saturated tiles cannot be physically adjacent across a shared side.

Write

    H=mn/2, D=H-|T|, C=|E(Gamma)|, R=sum r_Q,
    q=|T|+|M|-H=C-R,
    h=sum h_Q, s=sum s_Q, K=h+s.

Then D=R+K=C-q+K. If ell is the number of zero-capacity residual leaves, each such leaf has at least one saturated attachment, charged at that leaf tile alone. Consequently the earlier proof gives the more informative inequality

    s>=ell,                 K>=h+ell.                         (2.1)

It is the retained h term, together with the next three-step classification, that improves four-fifths to five-sixths.

At r>0 a tile has one real port for each residual edge and 2r-deg_Q slack H ports. A zero-capacity leaf has one terminal L port. Local perfect pairings and real edges decompose the port graph into paths and cycles. Let a,b,c count LL,HH,LH paths, respectively. Length counts only real residual edges. For any routing,

    ell=2a+c,                q=a-b.                           (2.2)

Zero-length HH paths are allowed. The routing is auxiliary and does not change the actual feasible pair.

## 3. A slack-first and companion-side routing

Corner names are TL,TR,BL,BR. A leaf port is a real endpoint whose residual matching partner is in a zero-capacity leaf tile. Its side companion is the other corner of its own tile along the side through which that residual edge enters.

A zero leaf has, up to square symmetry, either

    T c        B s
    B s        s c,

where c is its residual endpoint and every s is matched to a saturated tile. Both corners adjacent to c are occupied; the corner opposite c is B. An s attachment must leave along the unique side containing its B neighbor. The previous companion-exclusion lemma says that a leaf port's side companion cannot itself be another leaf port, and every tile has at most two leaf ports.

**Lemma 3.1 (physical leaf-endpoint exclusion).** The residual endpoints c of two distinct zero leaf tiles cannot be physically adjacent across their common side, even if the grid edge between them is not in M.

**Proof.** The two companion corners along that common side are both occupied. If either companion is T, it has its own within-tile c neighbor and the occupied opposite companion, contradicting feasibility. Thus both companions are attachment endpoints s. Their forced attachments leave through the same perpendicular side into two adjacent saturated tiles, at P corners adjacent across those saturated tiles' common side. This is forbidden by the saturated-tile rule. No step uses the assumption that the original c-c adjacency is a matching edge. QED.

**Lemma 3.2 (full-tile prescriptions do not conflict).** In a full P tile of capacity two, pairing each leaf port to its side companion gives disjoint pairs.

**Proof.** A companion cannot be another leaf port. A repeated companion can only occur for two diagonal leaf ports. Normalize their corners to TL and BR, with the repeated companion TR. The TL leaf edge enters from above and the BR leaf edge from the right. The companions inside both receiving leaf tiles face occupied corners of the full P tile, so they are s, not T. Their forced attachments both require the same BL P corner of the diagonally upper-right saturated tile. Two distinct matching edges would then share an endpoint. This contradiction rules out the repeated companion. The other cases are square symmetries. QED.

**Definition 3.3 (the selected routing).** Capacity-one pairings are unique. At capacity two, t_Q=h_Q=s_Q=0, so its four corners can be identified with its four ports: real corners are P and other corners are B/slack.

- If slack exists, pair as many leaf ports as possible with distinct slack ports, then pair the remaining two ports, if any. Ties may be broken arbitrarily.
- If all four ports are real, use the prescriptions of Lemma 3.2 and complete the remaining pair, if any.

These rules always avoid directly pairing two leaf ports. With slack present, a leaf is paired to another real port only in the case of three real ports, two leaf ports and one slack port. In that case the tile has one immediate one-edge LH path and one remaining leaf-to-real pair. Call this a slack-paid tile. It can support at most one LL path and supplies a distinct one-edge LH path to pay for it.

This selected routing is not asserted to be planar. A slack-first pairing can cross when the relevant corner positions are diagonal. The earlier planar routing observation supplies a different optional choice; no Temperley-Lieb planarity assumption is used below.

**Lemma 3.4 (two-step payment retained).** Let f_2 count length-two LL paths in this routing. Then f_2<=b. Each such path has a distinct capacity-one center with h_Q=1.

**Proof.** Direct leaf-leaf pairing is excluded at capacity two, so every length-two LL has a capacity-one center. The earlier fork theorem classifies it as a full P tile with an internal matched edge and opposite residual exits. The earlier companion theorem supplies a residual-isolated tile of capacity one or two behind that internal edge, and bounds the number of forks charged to each such tile by its capacity. Any routing at a residual-isolated positive-capacity tile consists of exactly r_Q zero-length HH paths. Summing proves f_2<=b. Each capacity-one center has only its unique pairing and therefore lies on only one of these paths. QED.

## 4. Paying for three-edge LL paths

**Lemma 4.1 (capacity-one local types).** A capacity-one tile of residual degree two has two adjacent real P corners. Its other corners, in their two possible orders, are T,B; an attachment endpoint s,B; or one internal matched pair P,P. There are five ordered types for each specified adjacent real pair.

**Proof.** Since r=1, either t=1,h=s=0 or t=0,h+s=1. In the first case T permits at most one adjacent P and at most the opposite P. Two real P corners therefore consist of one adjacent and one opposite to T, and are adjacent to each other; the remaining corner is B. If h=1, the internal edge occupies the other adjacent pair and all four corners are P. If s=1, its endpoint and a required adjacent B occupy two adjacent corners, leaving the adjacent real pair. These cases are exhaustive. QED.

**Lemma 4.2 (companion escape).** Suppose a length-three LL path uses a full capacity-two tile as one of its internal tiles, and its selected pairing at that tile follows Definition 3.3. Then its other internal tile must be slack-paid.

**Proof.** Normalize the middle residual edge to Q.TR--R.TL with Q on the left and R on the right. For Q's leaf port to pair with Q.TR by the companion rule, that leaf port must be Q.TL and its leaf edge must enter from above. The alternative Q.BR port would have to receive its leaf through the right side, but that neighbor is R, a positive-capacity internal tile.

The leaf above Q has residual endpoint BL. Its BR companion faces occupied Q.TR, so it must be s. Its forced attachment goes right into the BL corner of a saturated tile above R. That saturated tile's BR corner is T and already has its BL P neighbor. It forces R.TR to be B. Thus R cannot be a full capacity-two tile.

If R had capacity one, Lemma 4.1 forces its other real corner to be BL, since TR is B. Its leaf edge exits down; it cannot exit left into Q. Its BR corner is either T or s. If it is T, its within-R BL P neighbor and the occupied companion of the leaf below R give two occupied neighbors. If it is s, its attachment exits right. The TR companion inside the leaf below R faces this occupied s, so it too must be s and attach right. The two receiving saturated P corners in the two tiles to the right are vertically adjacent, again forbidden. This excludes capacity one.

The remaining possibility is a capacity-two tile with slack. For a length-three LL path to pass through it rather than terminate at slack, Definition 3.3 makes it slack-paid. All asserted neighboring saturated tiles exist because the specified attachment edges exist; a missing boundary tile would already exclude the configuration. QED.

**Lemma 4.3 (the two capacity-one case).** If a length-three LL path has two capacity-one internal tiles, at least one of them has an internal matching edge.

**Proof.** Again normalize the middle edge to Q.TR--R.TL. Lemma 4.1 leaves exactly the following leaf exits:

    Q: left from TL, up from TL, or down from BR;
    R: right from TR, up from TR, or down from BL.

The other outward option would lead to the positive-capacity internal neighbor, which cannot be a leaf. Thus these nine spatial cases are exhaustive.

Any up case is impossible: the argument of Lemma 4.2 only used Q.TL and Q.TR being occupied at its first tile, not its other two corners. It therefore gives the same contradiction at a capacity-one R. Reflection handles an up exit at R. The down/down case is impossible by Lemma 3.1, since the two leaf c corners immediately below the middle edge would be physically adjacent.

Consider left/right and suppose neither internal tile has an internal matching edge. Q.BL cannot be T: it would see Q.TL and the occupied side companion in the left leaf. Lemma 4.1 then makes Q.BL=B and Q.BR either T or s. Symmetrically R.BR=B and R.BL is T or s. The two inner lower corners Q.BR and R.BL are adjacent and occupied. Neither can be T, since it already has the P corner above it. Thus both are s, and their forced downward attachments enter adjacent saturated tiles at adjacent P corners, a contradiction.

For left/down, suppose Q has no internal matched edge. The same first argument gives Q.BL=B and Q.BR either T or s. Since R.BL is the second leaf's real P endpoint and is adjacent to Q.BR, Q.BR must be s. Its downward attachment enters a saturated tile below Q at TR. That saturated tile's BR corner is T. It faces the occupied BL companion of the leaf below R, while already having its own TR P neighbor. This is impossible. Therefore Q has an internal matched edge. The down/right case is the reflected argument, forcing the internal edge at R.

All cases are now covered. For reference the table is

                 right             up              down
    left         at least one h=1  impossible      h_Q=1
    up           impossible        impossible      impossible
    down         h_R=1             impossible      impossible.

QED.

**Theorem 4.4 (injective short-path charges).** Let f_3 count length-three LL paths in the selected routing. There is an integer z>=0 such that

    f_2+f_3 <= h+z,              z<=c.                        (4.1)

**Proof.** Charge each length-two LL to the internal matched edge at its capacity-one fork center. For each length-three LL, first use an internal edge at an internal capacity-one tile if one is present. If both internal tiles have capacity one, Lemma 4.3 guarantees such an edge. If a full capacity-two tile occurs, Lemma 4.2 forces a slack-paid tile at the other internal position. Every other capacity-two internal tile is partial and, to occur on this path under Definition 3.3, must also be slack-paid. Thus when no internal-edge charge is used, charge the path to a slack-paid tile on it and to that tile's immediate LH path.

A tile with an internal edge that lies on a residual route has capacity one and only one port pair. It cannot be charged by two distinct port paths, including a length-two and a length-three path. A slack-paid tile has one leaf-H pair and just one other pair. Hence at most one LL path can charge it. Its immediate one-edge LH path cannot also be the immediate LH path of another slack-paid tile, since its other endpoint is a zero-capacity leaf. These are distinct available c paths. Taking z to be the number of slack charges proves (4.1). QED.

## 5. The unconditional five-sixths theorem

**Theorem 5.1.** On every positive even-by-even full rectangle, every feasible pair satisfies

    |T|+(5/6)|M| <= mn/2,
    equivalently 6|T|+5|M| <= 3mn.                            (5.1)

The selected routing satisfies the stronger estimate

    D >= 5q+6b-f_2+2c-z >= 5q+5b+c.                          (5.2)

**Proof.** Length-two LL paths use two residual edges, length-three paths use three, and every other LL uses at least four. Every LH uses at least one. HH paths and cycles have nonnegative lengths. Therefore

    C >= 2f_2+3f_3+4(a-f_2-f_3)+c
      = 4a-2f_2-f_3+c.

Use (2.1), ell=2a+c, and D=C-q+K:

    D >= (4a-2f_2-f_3+c)-q+(h+2a+c)
      = 5q+6b-2f_2-f_3+2c+h
      >= 5q+6b-f_2+2c-z.

The last inequality is precisely the injective charge bound (4.1). Finally f_2<=b and z<=c give the second inequality in (5.2). In particular D>=5q. Substituting q=|M|-D yields 5|M|<=6D, proving (5.1). The proof does not require q>0. QED.

**Corollary 5.2 (new counterexample restrictions).** If q>0, then

    mn/2-|T| >= 5q,             |M| >= 6q.

Consequently the full objective bound |T|+|M|<=F(m,n) holds whenever |M|<=5 or |T|>=mn/2-4. A sub-quorum coloring exceeding F by d>=1 requires at least 6d color classes containing an internal edge. The earlier requirement of at least d pure horizontal and d pure vertical edged classes also remains valid.

**Proof.** Use D>=5q, |M|=D+q and integrality. Under the source-faithful representative reduction, |T|+|M| is the color count and |M| is the number of edged color classes. QED.

The coefficient in (5.1) has no leaf-separation assumption. The new step pays for every three-edge LL path using internal matching or a distinct immediate slack path, in addition to the earlier payment for length-two paths. It does not establish an LL-to-HH injection for all longer paths, and does not supply the odd-side boundary terms required for the full conjecture.

## 6. Exact checks and non-vacuous witnesses

Run

    python3 develop/verify_grid_five_sixths.py --output develop/results/grid-five-sixths-verification.json

The helper `develop/grid_three_step_patterns.py` independently enumerates the complete five-type local classification in Lemma 4.1. It records actual P/T/B positions, matching endpoints and compulsory saturated tiles, rejecting only inconsistent assignments, duplicate matching endpoints and T-degree violations. All unspecified positions can be B, so accepted patches are realizable finite-grid configurations after an even translation.

The actual run checked all 2,025 normalized local cases: nine exit geometries, five ordered types at each internal tile, and three leaf shapes at each endpoint. Exactly 32 pass. None has zero internal matched edges. The accepted counts by number of internal edges (0,1,2) are (0,4,4) for left/right, (0,8,4) for left/down and down/right, and zero for the other six geometries. The ordinary geometric proof is Lemma 4.3; this table is its independent finite check.

All 32 realizable patches were embedded under eight square symmetries and nine even translations. The 2,304 resulting feasible rectangles each contain a three-edge LL path under the actual selected routing, and all satisfy the charging and five-sixths inequalities. Two earlier 4-by-6 fork examples additionally exercise f_2 and both companion types.

The checker also ran through all 261,868 feasible pairs on 2x2,2x4,2x6,4x4 and 500 seeded random pairs across 4x6,6x6,8x10,12x14,20x20. Those bulk cases have no length-two or length-three LL paths; the non-vacuous planted tests above are therefore reported separately. The slack-paid branch is retained as a valid case in the proof; the planted three-step examples use internal-edge charges and are not claimed to test every possible slack-paid geometry.

Finally the no11/even-gap bijection and inverse were checked on all binary words through length 14 and all boundary subsets through order 15, as well as weighted no11 optimization for all weights in {-2,-1,0,1,2} through length six. This validates the stated one-dimensional interface, not a weighted quotient of the entire grid transfer.

The result JSON contains executed script hashes and the exact counts. All listed checks passed. No Lean/Scribe or CI-success claim follows from these finite computations. Existing formal files, manuscript and width-specific certificates are unchanged.

## Sources and attribution

[AC] trureturing, `D5/S1/Words/AdmissibleWords/AdmissibleCount.lean`, inspected blob `af8e217d2a3b279bab05d10ca9b965d4d74c2109`, and its Blueprint. The definition is no two consecutive true bits; the count is Fib(j+2).

[PS] trureturing, `D5/S1/Words/AdmissibleWords/PathStableSetPolytope.lean`, inspected blob `7b3a7abc40ee3678f93ab7eaf0712f4276902e58`, and its Blueprint. This supplies the existing path stable-set convex-hull interface.

[EJK] J. East, M. Johnson, M. Kambites, *Faithful linear and relational representations of diagram categories and monoids*, arXiv:2605.04630v1, 6 May 2026, Definition 6.4, Lemma 6.6 and Theorem 6.14. The HTML was inspected. https://arxiv.org/html/2605.04630 . The diagram representation theorem is attributed to these authors. The new grid inequality is proved separately above.

[G] This PR, `develop/grid-beta-uniform-2026-09-27.md` Sections 11-13 and `develop/grid-parity-transport-2026-09-27.md` Sections 1-6, pinned at `bee8bf429c0dc0ff53c75775496113c7782f9115`. These contain the residual input, companion exclusion, fork classification and short compensation used here.

[S] R. Sahbi, *Sub-quorum colorings of graphs*, arXiv:2609.25128v1, Definition 2.2 and Lemma 5.4, for the partial coloring/representative interface. Historical priority qualifications from the earlier notes remain in force.
