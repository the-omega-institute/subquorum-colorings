# Mixed-direction matching absorption on rectangular grids

For every feasible representative pair (T,M) on a positive even-by-even rectangle,

    |T| + (5/6)|M| <= mn/2.

The proof retains the corners at which matching edges meet an aligned 2-by-2 tiling. Short residual paths are charged to internal matching edges or available slack. The exact final count appears in Theorem C5.1. See the [research overview](GRID_RESULTS.md) for the definitions and consequences.

## A. The residual matching graph

Put P=V(M), A=T union P, and B=V(G)\A. Every vertex of T has at most one neighbor in A.

Throughout this section m,n are positive even integers and H=mn/2=F(m,n).
Tile the rectangle by the aligned, disjoint 2-by-2 squares. For a tile Q
let t_Q=|T intersection Q| and delta_Q=2-t_Q. Each t_Q<=2: three T
vertices in a square would include a T with two occupied neighbors.
Call a tile saturated when t_Q=2, and deficient otherwise.

A saturated tile containing P must have two diagonally opposite T
vertices, one P vertex, and one B vertex. If its T vertices are adjacent,
they prohibit every other occupied vertex in that tile. In particular a
saturated tile contains no internal matching edge and at most one P.

**Lemma A.1 (forced blank at an attachment).** If a matching edge joins
a saturated tile to another tile, the companion corner of the receiving
tile, along the shared side, is B. Consequently no matching edge joins
two saturated tiles.

**Proof.** The companion corner in the saturated tile is T. It already
has its P neighbor within its tile, so the opposite corner across the
shared side must be unoccupied. A saturated receiving tile would have
T at that corner, which is impossible. The same reasoning shows that
P vertices in two saturated tiles cannot be adjacent across their shared
side, even if their adjacency is not the chosen matching edge. QED.

For each deficient tile let h_Q count matching edges internal to Q and
s_Q count matching edges from Q to saturated tiles. Each such attachment
is counted only at its deficient end. Define

    r_Q = delta_Q-h_Q-s_Q.

Let Gamma be the finite multigraph on deficient tiles, with one edge for
each remaining matching edge between two different deficient tiles.
Parallel edges are kept; no loop is included. Write C=|E(Gamma)| and
R=sum_Q r_Q.

**Lemma A.2 (local capacities).** Every r_Q is nonnegative. A tile with
r_Q=0 has Gamma-degree at most one. A tile with r_Q>0 has Gamma-degree
at most 2r_Q. Every residual-zero tile of positive Gamma-degree has
s_Q>=1.

**Proof.** If t_Q=1, its T corner allows at most one adjacent P and at
most the opposite P, hence at most two P vertices. If both occur they
are adjacent. One of the two P vertices then has T and P at its two
neighboring corners, so by Lemma A.1 it cannot be attached to a saturated
tile. Thus h_Q+s_Q<=1. If r_Q=0 and h_Q=1, no external endpoint remains.
If r_Q=0 and s_Q=1, at most one endpoint remains for Gamma. For r_Q=1,
there are at most two Gamma endpoints.

If t_Q=0, an attachment to a saturated tile needs a B corner adjacent to
its endpoint. Three such attachment endpoints would leave at most one B;
only two corners of a square are adjacent to that B. Thus three
attachments are impossible. One internal matching edge and two
attachments would occupy all four corners, leaving no required B.
Two internal matching edges leave no external endpoint at all. This
proves h_Q+s_Q<=2.

For r_Q=2 there are at most four Gamma endpoints. For r_Q=1, either one
internal edge uses two corners, or one attachment uses a P corner and
requires a B corner; there are at most two remaining Gamma endpoints.
For r_Q=0, the cases (h_Q,s_Q)=(2,0),(1,1) leave none, and (0,2) leaves
at most one because some corner is B. Every residual-zero tile with a
remaining endpoint therefore has an attachment. QED.

**Lemma A.3 (residual-zero leaves are independent).** No Gamma edge
has two endpoints with residual capacity zero.

**Proof.** By the preceding proof, a residual-zero tile incident to Gamma
has exactly one of the following forms, up to square symmetries. A letter
s denotes a P endpoint matched to a saturated tile, and c denotes its
sole Gamma endpoint:

    Type I:  T c          Type II:  B s
             B s                    s c

All corners neighboring c within its tile are occupied. Every such
neighbor that is P is an s corner. An s corner has one neighboring B
corner and one neighboring c corner, so Lemma A.1 forces its attachment
to leave through the unique side containing the B corner.

Suppose two c corners are matched across the shared side of two such
tiles. Consider their companion corners along that side. If either is
T, that T has both its within-tile c neighbor and an occupied companion
across the side, violating feasibility. Thus both companions are s.
Their forced attachments leave on the same perpendicular side of the
two tiles. The two receiving saturated tiles are adjacent and their P
endpoints are adjacent across their shared side. This is prohibited by
the last assertion of Lemma A.1. The contradiction proves the lemma.
Boundary cases introduce no exception: an asserted attachment must exist
inside the original rectangle. QED.

**Theorem A.4 (exact residual reduction).** Put D=H-|T|=sum delta_Q and
q=|T|+|M|-H. Then

    q = C-R.                                                  (A.1)

If every connected component of Gamma has at most one residual-zero
vertex of degree one, then q<=0.

**Proof.** Every matching edge is internal to a deficient tile, joins a
saturated tile to a deficient tile, or is counted by Gamma. Hence
|M|=sum h_Q+sum s_Q+C, which proves (A.1). In a component with at most
one residual-zero leaf, Lemma A.2 and the degree sum give
2|E|<=2 sum r_Q+1. Both |E| and sum r_Q are integers, so |E|<=sum r_Q.
Sum over components. QED.

## B. Short-path geometry

Use the residual construction of Part A. Put K=sum(h_Q+s_Q), and let ell count the residual-zero leaves.

Each leaf's residual endpoint c has both its within-tile neighbors occupied. Up to square symmetries its tile has one of the forms

    T c         B s
    B s         s c

where every s is a P endpoint matched to a saturated tile. Each s has a B neighbor and a c neighbor within the tile; its attachment must leave through the side containing that B. This is the forced-blank lemma from Part A.

**Lemma B1.1 (companion exclusion).** Suppose a residual edge enters Q from a residual-zero leaf. The companion corner of Q along that shared side cannot be an endpoint of another residual edge to a residual-zero leaf.

**Proof.** Denote the leaf endpoint by c and its companion on the shared side by x. Both c and x are occupied. Suppose the corresponding companion corner in Q is another leaf-edge endpoint, hence P. Then x cannot be T: it would have both c and this P as occupied neighbors. Thus x is an s endpoint. Its forced attachment goes perpendicularly away from c, into the diagonally adjacent saturated tile S.

The second leaf edge cannot leave Q through the original shared side, since that would give the first leaf residual degree two. It must leave through the perpendicular side containing the companion corner. Its receiving leaf L' is adjacent to S. Along their common side, the T companion of the receiving P in S meets an occupied within-tile neighbor of the endpoint c' in L'. That T already has its within-S P neighbor, a contradiction. Rotation and reflection preserve every condition. All asserted saturated tiles exist because their attachment matching edges exist. QED.

**Corollary B1.2.** Every tile has at most two residual edges to residual-zero leaves.

**Proof.** Three such edges would occupy three distinct corners of a square. Among any three corners, one is adjacent within the square to both others. Its exterior matching edge must leave through a side containing one of those other corners, violating Lemma B1.1. The same argument handles four endpoints. QED.

### Classifying the unavoidable two-step paths

**Lemma B2.1 (capacity-one fork).** If r_Q=1 and Q has two residual-zero leaf neighbors, then Q is a full P tile, h_Q=1, s_Q=t_Q=0. Its two residual endpoints are adjacent corners and leave across opposite sides; its other two corners form the internal matching edge. Thus this is a straight three-tile residual component.

**Proof.** The degree bound gives deg_Gamma(Q)=2. If t_Q=1, then h_Q=s_Q=0 and there are at most two P corners. They are adjacent, because the T permits at most one adjacent P and hence the second P is opposite T. Lemma B1.1 forces their two leaf edges to leave through opposite sides, away from their common side. The side whose companion is T would then make that T adjacent both to its within-Q P and to an occupied companion in the leaf tile. This is impossible.

Otherwise t_Q=0 and h_Q+s_Q=1. If h_Q=1, the internal matching and two residual endpoints occupy all four corners. The two remaining corners are adjacent, and Lemma B1.1 gives the stated exits.

If s_Q=1, its attachment requires a B corner. Thus Q has exactly three P and one B, and the attached P is adjacent to B. The two residual P corners are consequently adjacent and again exit across opposite sides. Normalize them to the upper row, with the attached P in the lower right and B in the lower left. The attachment from Q must go down. The right leaf's companion must be s, as it faces an occupied P; its attachment also goes down. Their two receiving saturated tiles have adjacent P endpoints across their common side, forbidden by the earlier forced-blank lemma. This excludes the last case. QED.

**Lemma B2.2 (forced companion tile).** For every fork Q in Lemma B2.1 there is a tile S on the other side of its internal matching edge with:

    t_S=s_S=deg_Gamma(S)=0,
    r_S in {1,2},             h_S=2-r_S.

Its half farther from Q is BB. Its nearer half is either BB or one internal PP matching edge. Call S the companion of Q.

**Proof.** Normalize Q to four P corners with its two leaf edges leaving left and right from the upper row, and with its lower row internally matched. The companion in each leaf tile along the interface is s, because it faces a P in Q. Both attachments therefore go down, into saturated tiles to the lower left and lower right of Q. A full rectangle contains the intervening tile S directly below Q.

The inward lower corners of the two saturated tiles are T and already have their within-tile P neighbor. Hence both lower corners of S are B. Each upper corner of S has two occupied neighbors: the internally matched P immediately above in Q and the attachment P to its left or right. Thus neither upper corner can be T. If it is P, its only available matching partner is the other upper corner: the lower neighbor is B, the neighbor above is already matched within Q, and the lateral neighbor is already matched to its leaf. Therefore the upper half is BB or an internal matching pair. This proves all assertions. QED.

**Lemma B2.3 (no overcharging).** If f_S forks have companion S, then f_S<=r_S. In particular sum_Q 1<=sum_(companion S) r_S, counting each distinct companion once.

**Proof.** A fork lies in one of the four tiles adjacent to its companion. For a source above S, the tiles to the left and right of S are its forced saturated tiles. Thus no perpendicular source can have the same companion: a source must be a full P tile and cannot be saturated. At most two sources can occur, on opposite sides. A source on either side forces the half of S away from it to be BB. Two opposite sources therefore force S entirely BB, giving r_S=2. One source requires only r_S>=1. QED.

## C. Routing and the five-sixths bound

Throughout the remaining sections, m,n are positive even integers. A feasible representative pair consists of a matching M and a disjoint T, every t in T having at most one neighbor in A=T union V(M). Put P=V(M), B=V\A. The source-faithful coloring reduction gives psi_sq<=Omega=max(|T|+|M|).

Partition the full rectangle into aligned 2-by-2 tiles. Write t_Q for the number of T vertices. A tile with t_Q=2 is saturated. For a deficient tile let h_Q count its internal matching edges and s_Q count matching edges from it to saturated tiles. Set

    r_Q=2-t_Q-h_Q-s_Q.

Gamma retains matching edges between two different deficient tiles; parallel edges and endpoint corners are retained. Let deg_Q be its residual degree. The earlier residual lemmas prove r_Q in {0,1,2}; deg_Q<=1 for r_Q=0 and deg_Q<=2r_Q otherwise; and independence of the zero-capacity residual leaves. A saturated tile incident to a matching edge has P at its attachment corner, T at the two adjacent corners, and B at the opposite corner. P corners of different saturated tiles cannot be physically adjacent across a shared side.

Write

    H=mn/2, D=H-|T|, C=|E(Gamma)|, R=sum r_Q,
    q=|T|+|M|-H=C-R,
    h=sum h_Q, s=sum s_Q, K=h+s.

Then D=R+K=C-q+K. If ell is the number of zero-capacity residual leaves, each such leaf has at least one saturated attachment, charged at that leaf tile alone. Consequently the earlier proof gives the more informative inequality

    s>=ell,                 K>=h+ell.                         (C2.1)

It is the retained h term, together with the three-step classification below, that improves four-fifths to five-sixths.

At r>0 a tile has one real port for each residual edge and 2r-deg_Q slack H ports. A zero-capacity leaf has one terminal L port. Local perfect pairings and real edges decompose the port graph into paths and cycles. Let a,b,c count LL,HH,LH paths, respectively. Length counts only real residual edges. For any routing,

    ell=2a+c,                q=a-b.                           (C2.2)

To see the second identity, the number of slack terminals is 2R-(2C-ell)=2R-2C+ell. It is also 2b+c, whereas ell=2a+c. Subtracting gives C-R=a-b. Zero-length HH paths are allowed. The routing is auxiliary and does not change the actual feasible pair.

### C3. A slack-first and companion-side routing

Corner names are TL,TR,BL,BR. A leaf port is a real endpoint whose residual matching partner is in a zero-capacity leaf tile. Its side companion is the other corner of its own tile along the side through which that residual edge enters.

A zero leaf has, up to square symmetry, either

    T c        B s
    B s        s c,

where c is its residual endpoint and every s is matched to a saturated tile. Both corners adjacent to c are occupied; the corner opposite c is B. An s attachment must leave along the unique side containing its B neighbor. The previous companion-exclusion lemma says that a leaf port's side companion cannot itself be another leaf port, and every tile has at most two leaf ports.

**Lemma C3.1 (physical leaf-endpoint exclusion).** The residual endpoints c of two distinct zero leaf tiles cannot be physically adjacent across their common side, even if the grid edge between them is not in M.

**Proof.** The two companion corners along that common side are both occupied. If either companion is T, it has its own within-tile c neighbor and the occupied opposite companion, contradicting feasibility. Thus both companions are attachment endpoints s. Their forced attachments leave through the same perpendicular side into two adjacent saturated tiles, at P corners adjacent across those saturated tiles' common side. This is forbidden by the saturated-tile rule. No step uses the assumption that the original c-c adjacency is a matching edge. QED.

**Lemma C3.2 (full-tile prescriptions do not conflict).** In a full P tile of capacity two, pairing each leaf port to its side companion gives disjoint pairs.

**Proof.** A companion cannot be another leaf port. A repeated companion can only occur for two diagonal leaf ports. Normalize their corners to TL and BR, with the repeated companion TR. The TL leaf edge enters from above and the BR leaf edge from the right. The companions inside both receiving leaf tiles face occupied corners of the full P tile, so they are s, not T. Their forced attachments both require the same BL P corner of the diagonally upper-right saturated tile. Two distinct matching edges would then share an endpoint. This contradiction rules out the repeated companion. The other cases are square symmetries. QED.

**Definition C3.3 (the selected routing).** Capacity-one pairings are unique. At capacity two, t_Q=h_Q=s_Q=0, so its four corners can be identified with its four ports: real corners are P and other corners are B/slack.

- If slack exists, pair as many leaf ports as possible with distinct slack ports, then pair the remaining two ports, if any. Ties may be broken arbitrarily.
- If all four ports are real, use the prescriptions of Lemma C3.2 and complete the remaining pair, if any.

These rules always avoid directly pairing two leaf ports. With slack present, a leaf is paired to another real port only in the case of three real ports, two leaf ports and one slack port. In that case the tile has one immediate one-edge LH path and one remaining leaf-to-real pair. Call this a slack-paid tile. It can support at most one LL path and supplies a distinct one-edge LH path to pay for it.

This selected routing is not asserted to be planar. A slack-first pairing can cross when the relevant corner positions are diagonal. Only the path decomposition is used below.

**Lemma C3.4 (two-step payment retained).** Let f_2 count length-two LL paths in this routing. Then f_2<=b. Each such path has a distinct capacity-one center with h_Q=1.

**Proof.** Direct leaf-leaf pairing is excluded at capacity two, so every length-two LL has a capacity-one center. Lemma B2.1 classifies it as a full P tile with an internal matched edge and opposite residual exits. Lemmas B2.2 and B2.3 supply a residual-isolated tile of capacity one or two behind that internal edge, and bound the number of forks charged to each such tile by its capacity. Any routing at a residual-isolated positive-capacity tile consists of exactly r_Q zero-length HH paths. Summing proves f_2<=b. Each capacity-one center has only its unique pairing and therefore lies on only one of these paths. QED.

### C4. Paying for three-edge LL paths

**Lemma C4.1 (capacity-one local types).** A capacity-one tile of residual degree two has two adjacent real P corners. Its other corners, in their two possible orders, are T,B; an attachment endpoint s,B; or one internal matched pair P,P. There are five ordered types for each specified adjacent real pair.

**Proof.** Since r=1, either t=1,h=s=0 or t=0,h+s=1. In the first case T permits at most one adjacent P and at most the opposite P. Two real P corners therefore consist of one adjacent and one opposite to T, and are adjacent to each other; the remaining corner is B. If h=1, the internal edge occupies the other adjacent pair and all four corners are P. If s=1, its endpoint and a required adjacent B occupy two adjacent corners, leaving the adjacent real pair. These cases are exhaustive. QED.

**Lemma C4.2 (companion escape).** Suppose a length-three LL path uses a full capacity-two tile as one of its internal tiles, and its selected pairing at that tile follows Definition C3.3. Then its other internal tile must be slack-paid.

**Proof.** Normalize the middle residual edge to Q.TR--R.TL with Q on the left and R on the right. For Q's leaf port to pair with Q.TR by the companion rule, that leaf port must be Q.TL and its leaf edge must enter from above. The alternative Q.BR port would have to receive its leaf through the right side, but that neighbor is R, a positive-capacity internal tile.

The leaf above Q has residual endpoint BL. Its BR companion faces occupied Q.TR, so it must be s. Its forced attachment goes right into the BL corner of a saturated tile above R. That saturated tile's BR corner is T and already has its BL P neighbor. It forces R.TR to be B. Thus R cannot be a full capacity-two tile.

If R had capacity one, Lemma C4.1 forces its other real corner to be BL, since TR is B. Its leaf edge exits down; it cannot exit left into Q. Its BR corner is either T or s. If it is T, its within-R BL P neighbor and the occupied companion of the leaf below R give two occupied neighbors. If it is s, its attachment exits right. The TR companion inside the leaf below R faces this occupied s, so it too must be s and attach right. The two receiving saturated P corners in the two tiles to the right are vertically adjacent, again forbidden. This excludes capacity one.

The remaining possibility is a capacity-two tile with slack. For a length-three LL path to pass through it rather than terminate at slack, Definition C3.3 makes it slack-paid. All asserted neighboring saturated tiles exist because the specified attachment edges exist; a missing boundary tile would already exclude the configuration. QED.

**Lemma C4.3 (the two capacity-one case).** If a length-three LL path has two capacity-one internal tiles, at least one of them has an internal matching edge.

**Proof.** Again normalize the middle edge to Q.TR--R.TL. Lemma C4.1 leaves exactly the following leaf exits:

    Q: left from TL, up from TL, or down from BR;
    R: right from TR, up from TR, or down from BL.

The other outward option would lead to the positive-capacity internal neighbor, which cannot be a leaf. Thus these nine spatial cases are exhaustive.

Any up case is impossible: the argument of Lemma C4.2 only used Q.TL and Q.TR being occupied at its first tile, not its other two corners. It therefore gives the same contradiction at a capacity-one R. Reflection handles an up exit at R. The down/down case is impossible by Lemma C3.1, since the two leaf c corners immediately below the middle edge would be physically adjacent.

Consider left/right and suppose neither internal tile has an internal matching edge. Q.BL cannot be T: it would see Q.TL and the occupied side companion in the left leaf. Lemma C4.1 then makes Q.BL=B and Q.BR either T or s. Symmetrically R.BR=B and R.BL is T or s. The two inner lower corners Q.BR and R.BL are adjacent and occupied. Neither can be T, since it already has the P corner above it. Thus both are s, and their forced downward attachments enter adjacent saturated tiles at adjacent P corners, a contradiction.

For left/down, suppose Q has no internal matched edge. The same first argument gives Q.BL=B and Q.BR either T or s. Since R.BL is the second leaf's real P endpoint and is adjacent to Q.BR, Q.BR must be s. Its downward attachment enters a saturated tile below Q at TR. That saturated tile's BR corner is T. It faces the occupied BL companion of the leaf below R, while already having its own TR P neighbor. This is impossible. Therefore Q has an internal matched edge. The down/right case is the reflected argument, forcing the internal edge at R.

All cases are now covered. For reference the table is

                 right             up              down
    left         at least one h=1  impossible      h_Q=1
    up           impossible        impossible      impossible
    down         h_R=1             impossible      impossible.

QED.

**Theorem C4.4 (injective short-path charges).** Let f_3 count length-three LL paths in the selected routing. There is an integer z>=0 such that

    f_2+f_3 <= h+z,              z<=c.                        (C4.1)

**Proof.** Charge each length-two LL to the internal matched edge at its capacity-one fork center. For each length-three LL, first use an internal edge at an internal capacity-one tile if one is present. If both internal tiles have capacity one, Lemma C4.3 guarantees such an edge. If a full capacity-two tile occurs, Lemma C4.2 forces a slack-paid tile at the other internal position. Every other capacity-two internal tile is partial and, to occur on this path under Definition C3.3, must also be slack-paid. Thus when no internal-edge charge is used, charge the path to a slack-paid tile on it and to that tile's immediate LH path.

A tile with an internal edge that lies on a residual route has capacity one and only one port pair. It cannot be charged by two distinct port paths, including a length-two and a length-three path. A slack-paid tile has one leaf-H pair and just one other pair. Hence at most one LL path can charge it. Its immediate one-edge LH path cannot also be the immediate LH path of another slack-paid tile, since its other endpoint is a zero-capacity leaf. These are distinct available c paths. Taking z to be the number of slack charges proves (C4.1). QED.

### C5. The unconditional five-sixths theorem

**Theorem C5.1.** On every positive even-by-even full rectangle, every feasible pair satisfies

    |T|+(5/6)|M| <= mn/2,
    equivalently 6|T|+5|M| <= 3mn.                            (C5.1)

The selected routing satisfies the stronger estimate

    D >= 5q+6b-f_2+2c-z >= 5q+5b+c.                          (C5.2)

**Proof.** Length-two LL paths use two residual edges, length-three paths use three, and every other LL uses at least four. Every LH uses at least one. HH paths and cycles have nonnegative lengths. Therefore

    C >= 2f_2+3f_3+4(a-f_2-f_3)+c
      = 4a-2f_2-f_3+c.

Use (C2.1), ell=2a+c, and D=C-q+K:

    D >= (4a-2f_2-f_3+c)-q+(h+2a+c)
      = 5q+6b-2f_2-f_3+2c+h
      >= 5q+6b-f_2+2c-z.

The last inequality is precisely the injective charge bound (C4.1). Finally f_2<=b and z<=c give the second inequality in (C5.2). In particular D>=5q. Substituting q=|M|-D yields 5|M|<=6D, proving (C5.1). The proof does not require q>0. QED.

**Corollary C5.2 (new counterexample restrictions).** If q>0, then

    mn/2-|T| >= 5q,             |M| >= 6q.

Consequently the full objective bound |T|+|M|<=F(m,n) holds whenever |M|<=5 or |T|>=mn/2-4. A sub-quorum coloring exceeding F by d>=1 requires at least 6d color classes containing an internal edge. The directional theorem also requires at least d pure horizontal and d pure vertical edged classes; see Corollary 7.2 of the [row-profile proof](GRID_PROFILE_PROOF.md).

**Proof.** Use D>=5q, |M|=D+q and integrality. Under the source-faithful representative reduction, |T|+|M| is the color count and |M| is the number of edged color classes. QED.

The coefficient in (C5.1) has no leaf-separation assumption. The new step pays for every three-edge LL path using internal matching or a distinct immediate slack path, in addition to the earlier payment for length-two paths. It does not establish an LL-to-HH injection for all longer paths, and does not supply the odd-side boundary terms required for the full conjecture.

## D. Objective-preserving normalization

The following moves change the representative pair while preserving its objective.

**Theorem D.1.** Any feasible pair on an even-by-even full rectangle can be transformed into another feasible pair (T',M') with

    |T'|+|M'|=|T|+|M|,       |T'|>=|T|,       |M'|<=|M|,

whose residual graph has no capacity-one fork. The process terminates after at most the original number of matching edges internal to the fixed tiles.

**Proof.** Choose a fork Q and its companion S. In the normalized orientation of Lemma B2.2, let e_Q be the horizontal matching edge in the lower half of Q.

If S is all B, remove e_Q and its two endpoints from the occupied set, and promote one of the two upper vertices of S to T. That new T has exactly one occupied neighbor, the lateral P in a saturated tile. Its neighbor above has just been removed, and its two other neighbors within S are B. It has no T neighbors, so the promotion cannot increase another T's occupied degree. Old T vertices only lose occupied neighbors. The objective is unchanged, T grows by one, and M shrinks by one.

If S has a PP upper half, let e_S be its internal matching edge. The four endpoints of e_Q and e_S form a 2-by-2 square across the tile interface. Replace the two horizontal matching edges by the two vertical ones in that square. This preserves every occupied vertex, so feasibility and the objective are unchanged.

Both moves strictly decrease the total number of matching edges internal to the fixed tile partition: by one or two respectively. No other internal matching edge is changed. Therefore repetition terminates, and stopping means no fork remains. The stated inequalities hold at every step. QED.

The first move changes the feasible support and the second is a genuine matching plaquette flip. Neither is confused with the auxiliary S3 routing action. The theorem does not claim that all matching edges can be removed. After normalization a suitable port routing has no two-edge LL path, but longer LL paths still require further geometric analysis.

## Reproduction

The [reproduction guide](REPRODUCE.md#uniform-grid-arguments) gives the exact finite checks of these lemmas, including the constructed short-path examples. The universal statements follow from the geometric proofs above. Sahbi's [original paper](https://arxiv.org/abs/2609.25128v1) supplies the representative reduction.
