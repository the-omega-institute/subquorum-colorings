# Parity and group-transport continuation

Date: 2026-09-27. This continues `grid-beta-uniform-2026-09-27.md`, Sections 11-13, without changing their statements. Full proofs and the reusable theoretical definitions of the initial port construction are maintained in trureturing PR #10765:

https://github.com/the-omega-institute/trureturing/pull/10765

Pinned initial theory: https://github.com/the-omega-institute/trureturing/blob/ee33195db81fb50c5ea0ba633488d38ff8666cc8/docs/develop/theory/RECTANGULAR_GRID_PARITY_TRANSPORT.md

**Continuation status.** Sections 1-6 below add a complete ordinary proof of the unconditional coefficient 4/5 on every even-by-even full rectangle. This strengthens the initial distance-conditional result recorded immediately below. The coefficient-one bound and the unrestricted all-parity coloring formula remain unproved. No Lean verification, independent referee approval, or worldwide priority claim is made.

## Initial typed ports and the exact defect

For the existing residual multigraph Gamma, a vertex of positive capacity r has one real port per incident residual edge and 2r-deg(v) distinct slack ports. Pair its 2r ports. A residual-zero leaf is an unpaired L terminal; a slack port is an H terminal. The resulting port graph decomposes into paths and cycles. Write a,b,c for LL,HH,LH path counts and o for odd-length LL paths. All real edges are retained individually.

Then q=C-R=a-b for every pairing. Capacity-one vertices have a unique pairing; capacity-two vertices have three pairings, with the auxiliary routing action S4/V4=S3. This acts on routing choices, not on physical colorings. The signed defect q is invariant under every routing switch.

With D=mn/2-|T| and the previously proved saturated-attachment budget, the initial paper bound on even-by-even rectangles is

    D >= 3q + 4b + 2c + o,
    2mn - 4|T| - 3|M| >= 4b + 2c + o.

If every two connected residual-zero leaves have distance at least d>=2, then

    |T| + ((d+1)/(d+2))*|M| <= mn/2.

At this initial stage d=3 gave 4/5 and d=4 gave 5/6 only under extra separation assumptions. The new Sections 1-6 remove the separation assumption for 4/5. No unconditional 5/6 or coefficient-one result is asserted. If no connected leaf pair exists, q<=0. Sharp abstract paths show that the abstract port/capacity assumptions alone cannot yield coefficient one.

## A real componentwise counterexample

On a 4x6 grid with row-major numbering 0,...,23, take

    T = {0,5,12,17,19,22}
    M = {(1,2),(3,4),(7,13),(10,16),(8,9)}.

This is feasible. Its residual capacities are [0,1,0,0,2,0], retaining saturated tiles as isolated zero-capacity vertices, and its residual edges are (0,1),(1,2). The path component has C-R=1, while the separate blank tile of capacity two compensates it. Global q=-1 and |T|+|M|=11<12. Thus the stronger proposed condition that every actual residual component must have nonpositive excess is false. The global grid conjecture is unaffected.

## Repository interfaces and limits

The trureturing companion separates coordinate parity, path-length parity, permutation parity, and prime-factor parity. It proves the classical checkerboard change of basis JQ=B and integer saturation of bipartite incidence; a nonnegative right-hand-side example on P4 shows why all-prime modular solvability cannot replace capacity inequalities. Prime-coordinate abelianization Z^2 ~= <2,3> and an integer Heisenberg lift distinguish endpoint information from path order. A unique-common-neighbor obstruction still prevents S^2=dI for same-support finite-dimensional invertible group gains.

The unrestricted Omega/psi_sq formula remains unproved. A prospective global LL-to-HH compensation must retain the surrounding geometry, including capacity outside a single residual component.

## Initial executed verification

The companion includes its standard-library checker and result record. Its recorded checks passed on all 24 S4 permutations; all 1,099 nonempty labeled graphs through order five for incidence ranks modulo 2,3,5,7; 21,845 lattice words; 261,868 feasible representative pairs on four even rectangles with one seeded routing per pair; 59 sharp abstract paths; and the explicit 4x6 instance. These are finite regression checks, not a universal or Lean proof.

Initial script SHA256: 9356bd14bba1f256015b4c1d023915dc30c4ffe71ad4e3eab01d0292cce898eb. Its recorded remote Git blob is cb1c75eb210236c98cd616c7ef3593cc87e9e3ba.

## 1. New geometric input: leaf-port exclusion

Throughout the continuation, m,n are positive even integers. Use the fixed aligned 2-by-2 tile partition and the residual construction from Section 11 of `grid-beta-uniform-2026-09-27.md`. Thus t_Q counts T in a tile, h_Q counts its internal matching edges, s_Q its matching edges to saturated tiles (tiles with t=2), and

    r_Q=2-t_Q-h_Q-s_Q.

Gamma retains matching edges between deficient tiles. Set H=mn/2, D=H-|T|, C=|E(Gamma)|, R=sum r_Q, q=C-R=|T|+|M|-H, and K=sum(h_Q+s_Q). Earlier proved facts are r_Q in {0,1,2}, D=R+K, and K>=ell, where ell is the number of residual-zero leaves. Such leaves are independent.

Each leaf's residual endpoint c has both its within-tile neighbors occupied. Up to square symmetries its tile has one of the forms

    T c         B s
    B s         s c

where every s is a P endpoint matched to a saturated tile. Each s has a B neighbor and a c neighbor within the tile; its attachment must leave through the side containing that B. This is the forced-blank lemma from the existing Section 11.

**Lemma 1.1 (companion exclusion).** Suppose a residual edge enters Q from a residual-zero leaf. The companion corner of Q along that shared side cannot be an endpoint of another residual edge to a residual-zero leaf.

**Proof.** Denote the leaf endpoint by c and its companion on the shared side by x. Both c and x are occupied. Suppose the corresponding companion corner in Q is another leaf-edge endpoint, hence P. Then x cannot be T: it would have both c and this P as occupied neighbors. Thus x is an s endpoint. Its forced attachment goes perpendicularly away from c, into the diagonally adjacent saturated tile S.

The second leaf edge cannot leave Q through the original shared side, since that would give the first leaf residual degree two. It must leave through the perpendicular side containing the companion corner. Its receiving leaf L' is adjacent to S. Along their common side, the T companion of the receiving P in S meets an occupied within-tile neighbor of the endpoint c' in L'. That T already has its within-S P neighbor, a contradiction. Rotation and reflection preserve every condition. All asserted saturated tiles exist because their attachment matching edges exist. QED.

**Corollary 1.2.** Every tile has at most two residual edges to residual-zero leaves.

**Proof.** Three such edges would occupy three distinct corners of a square. Among any three corners, one is adjacent within the square to both others. Its exterior matching edge must leave through a side containing one of those other corners, violating Lemma 1.1. The same argument handles four endpoints. QED.

## 2. Classifying the unavoidable two-step paths

**Lemma 2.1 (capacity-one fork).** If r_Q=1 and Q has two residual-zero leaf neighbors, then Q is a full P tile, h_Q=1, s_Q=t_Q=0. Its two residual endpoints are adjacent corners and leave across opposite sides; its other two corners form the internal matching edge. Thus this is a straight three-tile residual component.

**Proof.** The degree bound gives deg_Gamma(Q)=2. If t_Q=1, then h_Q=s_Q=0 and there are at most two P corners. They are adjacent, because the T permits at most one adjacent P and hence the second P is opposite T. Lemma 1.1 forces their two leaf edges to leave through opposite sides, away from their common side. The side whose companion is T would then make that T adjacent both to its within-Q P and to an occupied companion in the leaf tile. This is impossible.

Otherwise t_Q=0 and h_Q+s_Q=1. If h_Q=1, the internal matching and two residual endpoints occupy all four corners. The two remaining corners are adjacent, and Lemma 1.1 gives the stated exits.

If s_Q=1, its attachment requires a B corner. Thus Q has exactly three P and one B, and the attached P is adjacent to B. The two residual P corners are consequently adjacent and again exit across opposite sides. Normalize them to the upper row, with the attached P in the lower right and B in the lower left. The attachment from Q must go down. The right leaf's companion must be s, as it faces an occupied P; its attachment also goes down. Their two receiving saturated tiles have adjacent P endpoints across their common side, forbidden by the earlier forced-blank lemma. This excludes the last case. QED.

**Lemma 2.2 (forced companion tile).** For every fork Q in Lemma 2.1 there is a tile S on the other side of its internal matching edge with:

    t_S=s_S=deg_Gamma(S)=0,
    r_S in {1,2},             h_S=2-r_S.

Its half farther from Q is BB. Its nearer half is either BB or one internal PP matching edge. Call S the companion of Q.

**Proof.** Normalize Q to four P corners with its two leaf edges leaving left and right from the upper row, and with its lower row internally matched. The companion in each leaf tile along the interface is s, because it faces a P in Q. Both attachments therefore go down, into saturated tiles to the lower left and lower right of Q. A full rectangle contains the intervening tile S directly below Q.

The inward lower corners of the two saturated tiles are T and already have their within-tile P neighbor. Hence both lower corners of S are B. Each upper corner of S has two occupied neighbors: the internally matched P immediately above in Q and the attachment P to its left or right. Thus neither upper corner can be T. If it is P, its only available matching partner is the other upper corner: the lower neighbor is B, the neighbor above is already matched within Q, and the lateral neighbor is already matched to its leaf. Therefore the upper half is BB or an internal matching pair. This proves all assertions. QED.

**Lemma 2.3 (no overcharging).** If f_S forks have companion S, then f_S<=r_S. In particular sum_Q 1<=sum_(companion S) r_S, counting each distinct companion once.

**Proof.** A fork lies in one of the four tiles adjacent to its companion. For a source above S, the tiles to the left and right of S are its forced saturated tiles. Thus no perpendicular source can have the same companion: a source must be a full P tile and cannot be saturated. At most two sources can occur, on opposite sides. A source on either side forces the half of S away from it to be BB. Two opposite sources therefore force S entirely BB, giving r_S=2. One source requires only r_S>=1. QED.

## 3. Choosing the port routing and absorbing every short path

A positive-capacity tile has 2r_Q ports. Call a real port a leaf port when its residual edge ends at a zero-capacity leaf. At r=2 there are at most two leaf ports by Corollary 1.2. Choose a pairing which never pairs two leaf ports: with two such ports pair each with one of the two other ports; with at most one, any pairing suffices. At r=1 the pairing is unique.

This is a choice inside the previously defined S4/V4=S3 action; it does not alter T, M, or the residual graph. Let a,b,c count LL,HH,LH paths for this chosen routing, and let f count its LL paths of exactly two residual edges.

**Theorem 3.1 (short-path compensation).** The two-edge LL paths are exactly the capacity-one forks of Lemma 2.1, and

    f<=b.                                                     (3.1)

**Proof.** A two-edge LL path pairs two leaf ports at its sole internal tile. Our r=2 choice excludes that possibility there. At r=1 it is exactly a fork and occurs necessarily. Every fork's companion S has residual degree zero, so all its 2r_S ports are slack terminals. Any local pairing at S gives precisely r_S zero-length HH paths. Lemma 2.3 bounds the number of sources charged to S by that number. Summing proves (3.1), without needing distinct residual components to compensate themselves. QED.

**Theorem 3.2 (unconditional four-fifths absorption).** Every feasible pair on every positive even-by-even full rectangle satisfies

    |T|+(4/5)|M| <= mn/2,
    equivalently 5|T|+4|M| <= 5mn/2.                          (3.2)

For the selected routing there is the stronger bound

    D >= 4q+5b-f+2c >= 4q+4b+2c.                             (3.3)

**Proof.** Each of the f short LL paths has length two; every other LL path has length at least three. LH paths have length at least one. Other paths and cycles contribute nonnegative lengths, so

    C >= 2f+3(a-f)+c = 3a-f+c.

Terminal counting gives ell=2a+c, and the attachment budget gives K>=ell. Using D=C-q+K and q=a-b yields

    D >= (3a-f+c)-q+(2a+c)
      = 4q+5b-f+2c.

Now apply f<=b. In particular D>=4q. Since q=|M|-D, this is 4|M|<=5D, exactly (3.2). No assumption that q is positive is required in this derivation. QED.

**Corollary 3.3.** If q>0, then D>=4q and |M|>=5q. Thus the full objective bound |T|+|M|<=F(m,n) holds when |M|<=4 or |T|>=mn/2-3. A coloring exceeding F by d needs at least 5d edge-containing color classes. The earlier pure-direction necessity remains in force as well.

**Proof.** Use (3.3), |M|=D+q, and integrality. The source-faithful representative reduction makes |M| exactly the number of edge-containing color classes and |T|+|M| the color count. QED.

## 4. Actual objective-preserving normalization

The companion also supplies genuine moves of the representative pair, rather than only an auxiliary routing switch.

**Theorem 4.1.** Any feasible pair on an even-by-even full rectangle can be transformed into another feasible pair (T',M') with

    |T'|+|M'|=|T|+|M|,       |T'|>=|T|,       |M'|<=|M|,

whose residual graph has no capacity-one fork. The process terminates after at most the original number of matching edges internal to the fixed tiles.

**Proof.** Choose a fork Q and its companion S. In the normalized orientation of Lemma 2.2, let e_Q be the horizontal matching edge in the lower half of Q.

If S is all B, remove e_Q and its two endpoints from the occupied set, and promote one of the two upper vertices of S to T. That new T has exactly one occupied neighbor, the lateral P in a saturated tile. Its neighbor above has just been removed, and its two other neighbors within S are B. It has no T neighbors, so the promotion cannot increase another T's occupied degree. Old T vertices only lose occupied neighbors. The objective is unchanged, T grows by one, and M shrinks by one.

If S has a PP upper half, let e_S be its internal matching edge. The four endpoints of e_Q and e_S form a 2-by-2 square across the tile interface. Replace the two horizontal matching edges by the two vertical ones in that square. This preserves every occupied vertex, so feasibility and the objective are unchanged.

Both moves strictly decrease the total number of matching edges internal to the fixed tile partition: by one or two respectively. No other internal matching edge is changed. Therefore repetition terminates, and stopping means no fork remains. The stated inequalities hold at every step. QED.

The first move changes the feasible support and the second is a genuine matching plaquette flip. Neither is confused with the auxiliary S3 routing action. The theorem does not claim that all matching edges can be removed. After normalization a suitable port routing has no two-edge LL path, but longer LL paths still require further geometric analysis.

## 5. Exact verification and examples

The continuation checker is `develop/verify_grid_short_path_compensation.py`; the actual output is `develop/results/grid-short-path-compensation-verification.json`. It checks the companion-corner exclusion, at-most-two leaf incidence, exact fork classification, compulsory companion pattern, the no-overcharging bound, the chosen routing and inequalities, and both objective-preserving moves.

Its initial execution checked all 261,868 feasible pairs on 2x2,2x4,2x6,4x4 and 500 seeded random pairs across 4x6,6x6,8x10,12x14,20x20. The small exhaustive boards contain no capacity-one fork; the two explicit 4x6 witnesses below exercise its non-vacuous geometry and both moves. No claim that random configurations cover every large pattern is made. The self-contained universal proofs are Sections 1-4 above, not the finite runs.

Use the earlier 4x6 pair. Its all-B companion permits one promotion, preserving objective 11 while changing (|T|,|M|) from (6,5) to (7,4). Adding the edge (14,15) to that pair gives a second feasible instance, now with objective 12. Its companion has a PP upper half; flipping (8,9),(14,15) to (8,14),(9,15) removes the fork without changing T or the objective.

Executed script SHA256: afaf0d1adb404472680e008f6a28fdcffeaab356b8bb0f78bc2322ee094027af. All listed checks passed. The source only uses Python's standard library. No Lean, Scribe, CI-success, or independent referee claim is made.

## 6. Remaining coefficient-one problem

The initial abstract distance assumption is no longer needed for the uniform 4/5 bound. Its replacement is a proved geometric fact: unavoidable two-edge defects have nearby slack capacity, and that slack cannot be overcharged.

The remaining target is q<=0. The construction disposes of the shortest forced residual components and provides a terminating support/matching normalization. It does not yet supply compensation for every longer LL path, nor the required boundary accounting for arbitrary odd side lengths. These are retained as unresolved mathematical statements. Existing manuscript, strip certificates, formal files, and CI configuration are unchanged.
