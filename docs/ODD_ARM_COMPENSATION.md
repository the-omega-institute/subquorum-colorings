# Unique-square components transport four half-donors along odd arms

The later [exact routing classification](SINGLE_SQUARE_WIRES_AND_SOURCE_FREE_PRUNING.md)
shows that these receivers have only source-free horizontal-BP mixed chains
and PP/M cycles. Their routing gates may be pruned while all original units
and the physical negative budget remain; shared units cannot be deleted.

19 October 2026. This extends the fixed-anchor cross in
FROZEN_CAPACITY_TWO_CROSS.md. All claims concern the original feasible
configuration and its original tile charges. The submitted paper is unchanged.

## Hypotheses and statement

Let (T,M) be feasible in a finite even-by-even rectangular grid, with
P=V(M), A=T union P, and every vertex in T having at most one neighbor in A.
Assume every P has at least three neighbors in A (single terminality).
Let H be a connected component of the graph induced by P. Assume:

1. H contains exactly one all-P unit square Q, counting all unit squares,
   including ones not aligned with the fixed tiling.
2. Q is an aligned tile of the fixed2-by2tiling.
3. The matching mate of each of its four vertices lies outside Q.

**Odd-arm compensation theorem.** H consists of Q and four straight arms,
one on each face in one of two pinwheel orientations. Their lengths outside
Q are odd, say 2a_N+1,2a_E+1,2a_S+1,2a_W+1, with each a_i>=0.
All vertices of H have occupied degree exactly three and freeze under the
general promotion certificate; no oriented bundle can promote any of them.

In the fixed tiling, the center and all arm tiles form a tile-connected
receiver R. Write N=a_N+a_E+a_S+a_W. The center has charge zero and
residual capacity2/degree4. There are N neutral arm tiles, each with
(t,p,b,s)=(1,2,1,0), and four terminal half-donors, each with
(t,p,b,s)=(1,1,2,0). Consequently

    |R|=N+5,      rho(R)=-2.

The region contains every matching edge of H, P=2N+8, T=N+4, B=N+8
and |M|=N+4. Its selected supports, including those outside R, number
2N+8. These formulas and the receiver charge hold in any feasible exterior
under the hypotheses; they do not require a blank exterior.

## General structural proof

Extend labels outside the rectangle by blank. Normalize Q to the corners
(0,0),(0,1),(1,1),(1,0), in clockwise order. Each face has a pair of
external neighbor positions, one incident to each of its two corners.

At most one position of each face pair is occupied. If both were occupied
and either were T, that T would see both its central P and its adjacent
external occupied vertex, contradicting feasibility. If both were P, the
face pair and the two central corners would form another P-square in H.
On the other hand, each central corner has its two central neighbors in P,
so terminality requires at least one of its two external neighbors occupied.
There are four face pairs and four corners: the upper bounds on faces and
lower bounds on corners have the same total four. Thus every face pair and
every corner has exactly one external occupied incidence. These incidences
are a perfect matching of the alternating corner/face8-cycle, which has
exactly two perfect matchings. They give the two pinwheel orientations.
Each central corner has occupied degree exactly three. Since its matching
edge leaves Q, its unique occupied external neighbor is P and is its mate.

The local branch lemma in SQUARE_FREE_ENDPOINTS_AND_OWNED_DONORS.md forces
a P-square containing the branching vertex itself. The proof of its local
turn lemma likewise produces a P-square containing the turning vertex.
Thus no vertex of H outside Q can branch or turn: either would produce a
second square. Starting from each external mate, the component therefore
continues straight out from its face and ends after finitely many vertices.
The four outward rays do not intersect. No additional endpoint vertex can
join them without a branch or turn, or join Q without a fifth occupied
external incidence. This proves the complete description of H.

Write an arm v,p_1,...,p_l with v in Q. The edge v--p_1 belongs to M.
Every further endpoint must be matched inside this same arm; successively
p_2--p_3,p_4--p_5,... are forced. It follows that l is odd.

Every arm vertex has at most one perpendicular T. Otherwise the adjacent
endpoint's two perpendicular neighbors would both be forced blank, leaving
it at most two occupied neighbors. This is the two-side-support argument
from the preceding note, also valid next to Q. Inner arm vertices therefore
have one perpendicular T; the tip has one perpendicular T and an axial T.
All have occupied degree three. Consecutive perpendicular supports alternate:
two on the same side would be adjacent T already incident to P. At p_1 the
support on the side facing the neighboring central corner is impossible,
since it would see that P as well as p_1. Thus the entire support pattern
is forced. Supports are distinct even between arms, since a T cannot see
two P. The support count is sum_i(l_i+1)=2N+8.

For freezing, each tip has two T neighbors and freezes immediately.
Induct inward by two positions: a frozen p_(2j+1) retains its mate p_(2j),
which together with the perpendicular T freezes p_(2j-1). Hence all four
p_1 freeze and retain all four central corners. Every central corner now
has two retained central neighbors and freezes. Finally propagate outward
to the even arm positions, starting with p_2 using the retained p_1 and
its T support. All witnesses are necessarily retained in any bundle, even
one using other endpoint components. This proves the bundle exclusion.

## Exact tile ledger and exclusive allocation

Consider the north arm from (0,0), pointing upwards in one orientation.
For j=1,...,2a_N+1 its endpoint is (-j,0). Its perpendicular support is
(-j,-1) for odd j and (-j,1) for even j. The axial tip support is
(-2a_N-2,0). These are actual forced labels, not a replacement configuration.

Each of the first a_N arm tiles has labels PT/PB in TL,TR/BL,BR order:
the two P lie on the arm, the upper-right T is the forced support, and
the lower-right vertex is blank because that T already sees a P.
The last tile has TB/PB: the top-left T is the axial tip support, and
the upper-right position is forced blank by its axial T. The lower-right
position is the unused external face incidence if this arm has length one;
otherwise the preceding perpendicular selected support forces it blank.
Rotation gives the other arms. The center is all P. In particular every
tile's full P set belongs to H, and no extra exterior T or P can alter
these labels. Every M mate in R lies in R and in a deficient tile, so s=0.
For every deficient tile, the original ledger is 2rho=t-b+s. It gives zero
at the center and each intermediate tile and -1/2 at each terminal tile.
The receiver counts and rho(R)=-2 follow by addition. No exterior boundary
attachment has been discarded: there are none on its matching endpoints.

Receivers from distinct endpoint components satisfying the hypotheses are
automatically tile-disjoint. Indeed every receiver tile has at least one P,
and all P in that tile belong to its component. A shared tile would identify
the two components. This applies even if their surrounding selected supports
interact. Thus c such components provide total charge exactly -2c, with
four distinct physical half-donors per component and no reused neutral tile.

For K pairwise disjoint source regions, each of charge at most one, assume
each source tile has (t,p)=(2,1), or (t,p)=(1,2) with s>=1. These sources
are automatically disjoint from the receivers: their labels exclude centers
and donors, while the s>=1 condition excludes intermediate arm tiles.
Writing W for the remaining tiles gives the sufficient inequality

    rho(whole grid) <= K-2c+rho(W).

Alternatively require source/receiver disjointness explicitly and drop the
source label restriction. K<=2c and nonpositive remainder yield
|T|+|M|<=mn/2 on this stated class. Neither source coverage nor the sign of
the general remainder has been proved. The unrestricted5/6bound is unchanged.

## Obstacle to a purely adjacent payment rule

If all a_i>=1, each of the four tiles immediately adjacent to Q is neutral,
not a half-donor. For a_i=L>=1, the four actual half-donors are at tile
distance L+1 from Q. The constructor below realizes every L and arbitrary
unequal nonnegative a_i by the displayed forced supports and blank elsewhere.
Feasibility follows because supports on an arm alternate, no support is
shared, and the four ray/support strips have no extra occupied contacts.
The only P-square is Q and every P has degree three.

This is an all-length counterexample to the rule that these weaker structural
hypotheses force four *adjacent* half-donors, and indeed to any fixed-radius
version for these arm receivers. It is not a counterexample to the compensation
inequality: the enlarged receiver always pays exactly two units at its tips.
The earlier fixed-eight-anchor adjacent-donor lemma remains valid; its anchors
are absent when an arm is extended.

## Verification and remaining scope

The written proof above is general. The companion physical checker constructs
unequal odd arms, verifies feasibility independently, counts all endpoint
squares/components, checks exact tile labels and original charge, confirms
every endpoint freezes, and checks tile-preserving symmetries. It also tests
separated multi-component receivers and the failure of adjacent payment.
The checker passes271parameter choices,2168symmetry images and8328nonempty
oriented bundles, plus a two-component receiver of charge-4. The largest
equal-arm control has each half-donor at tile distance17 from its center.
The two new Lean declarations check the face-pair exclusion and the eight
incidences forcing the two pinwheel orientations. These are local interfaces;
the full structural, geometric and transport theorem remains a written proof.
All32declarations in the local sequential Lean4.33.0audit pass with only
standard logical axioms, no sorry or compiler-reduction axioms. The earlier
Oracle packet does not include this result; its taskd3705dc5 ended with
no_assistant_output and provides no mathematical verdict. Full preceding
CI39203601140 at9aa88b3completed success; this milestone's CI is separate.
SINGLE_SQUARE_PARITY_AND_ALIGNMENT.md subsequently removes the outward-mate
restriction and classifies all central matchings. It also gives a fully
neutral misaligned8-by8frozen fixture, explaining why strict payment needs
alignment. General multi-square components, nonaligned classification,
source coverage and the rectangular-grid triple equality remain open.

    python3 develop/check_odd_arm_compensation.py --output output/odd-arm-controls.json

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
