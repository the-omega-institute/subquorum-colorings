# Compensation can travel arbitrarily far through neutral bands

30 September 2026. Follow-up to
[boundary-aware compensation](CROSS_COMPONENT_COMPENSATION.md).
All coordinates and distances use the fixed aligned 2x2 tiling.

We prove two results. First, the boundary debt of a filled corridor can pass
through an arbitrary number of specified neutral bands and be paid exactly
once by a terminal band. This gives coefficient one for the stated class,
including matching configurations with capacity-two passages. Second, an
explicit equality family has its only negative-excess residual component
at arbitrarily large tile distance from its positive component. Consequently
no uniform finite-radius rule can always pay positive components using only
the initial negative residual charges in that radius.

The second result is an obstruction to a charging rule, not to the grid
inequality. Every member satisfies the coefficient-one bound with equality.
It does not exclude local changes of the matching that alter the residual
components or create a different distribution of charges.

## 1. Ledger and a band entrance

For a deficient tile Q put rho(Q)=deg_Gamma(Q)/2-r_Q. Give saturated tiles
charge zero. Then q=sum_Q rho(Q). For a tile region S,

    rho(S)=C_inside(S)+C_crossing(S)/2-R(S).

The preceding note proves that a two-row band of even vertex width, flanked
by the saturated end tiles of a filled corridor, has

    rho(S)=-Delta(S)+sigma(S)/2,    Delta(S)>=1.             (1)

Here Delta=(number of B-number of T)/2 and sigma counts matching edges from
the band to saturated tiles outside it. The same proof uses only these
entrance conditions:

- Every vertex immediately above the upper row of the band is occupied.
- The tile immediately to the left has corners `T P / B T`, its P matched
  to the row above; the tile immediately to the right is its reflection
  `P T / T B`, likewise matched above.
- The complete surrounding pair is feasible.

The side P vertices exclude T at the upper band endpoints. The lower endpoint
vertices are blank because they face saturated T vertices already adjacent
to their own P. Any upper-row T in the band must have all its within-band
neighbors blank, because it has an occupied neighbor above. These are exactly
the blank-surplus lemma's hypotheses. Saturated tiles within the band have
no P, so the matching count giving (1) applies unchanged. External edges to
deficient tiles are allowed and retain their half-edge contribution.

## 2. A neutral band transmits its boundary debt

Consider a band S of w>=3 tiles satisfying the entrance conditions. Impose
the following labels in its upper/lower rows:

    first tile       intermediate tiles       last tile
        P P                 P P                   P P
        B s                 P P                   s B

Both s vertices are matching endpoints attached straight down into saturated
tiles. All other displayed P vertices may have arbitrary matching partners,
subject to feasibility and the displayed attachments. No internal matching
edge is required at the other P vertices.

**Lemma 1 (neutral transfer).** Every tile of S has charge zero. The two
receiving saturated tiles are the left and right entrance caps of a new
band S_next one tile row below, with width w-2. Every vertex immediately above
the new band's upper row is P. The new band therefore satisfies (1), in any
feasible surroundings.

**Proof.** In a full-P intermediate tile no attachment to a saturated tile
is possible, since it would require a blank side companion. With h internal
edges its capacity is 2-h and its residual degree is 4-2h, hence rho=0.

The first tile has exactly one saturated attachment, the prescribed s.
Its other two P vertices cannot supply a second attachment: the upper-right
corner has no blank within-tile companion; the upper-left corner could only
exit left through a side with a blank companion, but the receiving cap's
facing P is already matched above. Its capacity is 1-h and residual degree
2-2h, again giving rho=0. Reflection handles the last tile. Thus sigma(S)=2,
Delta(S)=1 and every tile, not just their sum, has charge zero.

Below the first tile the attachment enters the top-right P corner of a
saturated tile. Its other corners must be `T P / B T`. The right attachment
similarly gives `P T / T B`. The w-2 intervening tiles exist because the
ambient graph is the full rectangle. Above each of their upper vertices is
one of the displayed lower-row P vertices of an intermediate tile of S.
These are precisely the new entrance conditions. QED.

Two such end attachments are impossible when w=2: their receiving P vertices
would be adjacent in distinct saturated tiles, contradicting the forced-blank
lemma. When w=1 the two required endpoint shapes are inconsistent. Thus every
neutral transfer strictly decreases the positive width by two.

## 3. An arbitrary-depth compensation theorem

Begin with the filled source corridor U of Theorem 2 in the preceding note:
its two zero-capacity leaves contribute rho(U)=1. Its first band S_1 has
width k>=2 and satisfies the entrance conditions. Suppose S_1,...,S_(d-1)
have the neutral-transfer form, and S_d is an arbitrary feasible terminal
band with no matching attachment to a saturated tile outside it. All these
bands lie successively below one another; S_i has width k+2-2i>=1.

**Theorem 2 (compensation through neutral bands).** Under these hypotheses,

    rho(U union S_1 union ... union S_d) <= 0.              (2)

The conclusion allows arbitrary feasible matching partners of the P vertices
in the source and neutral bands, including capacity-two tiles and residual
edges crossing the accounting regions.

**Proof.** Apply Lemma 1 successively. Each earlier band has rho=0 and supplies
the next entrance. The terminal band satisfies (1) with sigma=0, so its charge
is at most -1. The source contributes +1. The regions occupy different tile
rows and are disjoint, so adding their charges proves (2). Any intervening
saturated caps have charge zero. The width decreases by two at every transfer;
the stipulated chain has d<=floor((k+1)/2). QED.

For any collection of these chains with pairwise disjoint charged tile sets,
add (2) and the charge rho(W) of the remaining deficient tiles. If rho(W)<=0,
then q<=0, or |T|+|M|<=mn/2. This improves 5/6 to 1 on this covered class.
Each terminal band is counted once, regardless of how many times an auxiliary
route visits it. A terminal band shared by two candidate chains cannot be used
twice; such overlapping chains fall outside this disjointness hypothesis.

This is a closure of the specific neutral-transfer case. A general occupied
band can have other labels, different attachment positions or directions,
or several competing exits. Width decrease and disjointness have not been
established for those cases or for arbitrary bent paths.

## 4. An explicit family with no nearby negative charge

Let d>=1 and k>=max(2,2d-1). Use a rectangle with

    tile rows 0,...,d and tile columns 0,...,k+1;
    vertex rows 0,...,2d+1 and vertex columns 0,...,2k+3.

For each layer i=1,...,d set L_i=i and R_i=k+1-i. Its band consists of tile
columns L_i,...,R_i. Put T at (0,0) and (0,2k+3), and also at

    (2i,2j),   (2i+1,2j+1)    whenever 1<=i<=d and 0<=j<i;
    (2i,2j+1), (2i+1,2j)      whenever 1<=i<=d and k+1-i<j<=k+1.

Thus all exterior tiles are saturated: use even-parity diagonal T vertices
on the left and odd-parity diagonal T vertices on the right. Take the matching
edges below; every unspecified vertex is B.

**Source row:**

    ((0,2j+1),(0,2j+2))        for 0<=j<=k;
    ((1,2j),(1,2j+1))          for 1<=j<=k;
    ((1,1),(2,1)), ((1,2k+2),(2,2k+2)).

**Upper half of every band, 1<=i<=d:**

    ((2i,2j),(2i,2j+1))        for L_i<=j<=R_i.

**Lower half of each nonterminal band, 1<=i<d:**

    ((2i+1,2j),(2i+1,2j+1))    for L_i<j<R_i;
    ((2i+1,2L_i+1),(2i+2,2L_i+1));
    ((2i+1,2R_i),(2i+2,2R_i)).

**Lower half of the terminal band:**

    ((2d+1,2j+1),(2d+1,2j+2))  for L_d<=j<R_d.

When k=6,d=3, the tile layout is

```text
L F F F F F F L
A E D D D D E A
O A E D D E A O
O O A C C A O O
```

Here L is a source leaf; F a full-P capacity-one source tile; A an attached
saturated cap; O a saturated tile without P; E an end tile with h=s=1;
D a full-P tile with h=2; and C a terminal capacity-one tile. The two C tiles
form the only negative-excess component. A, O, E and D have charge zero.

**Proposition 3 (feasibility and exact residual components).** The displayed
construction is feasible for every permitted k,d, has no capacity-one fork,
and its residual components are exactly:

1. One source LL path of k+1 edges, capacity k, and excess +1.
2. (d-1)(k+2-d) isolated zero-capacity tiles, each of excess zero.
3. One terminal path of w-1 edges and capacity w, where w=k+2-2d>=1,
   with excess -1. For w=1 it is an isolated capacity-one tile.

All other tiles are saturated and absent from the residual graph. In particular

    |T| = 2+2d(d+1),
    |M| = 2(d+1)(k+2-d)-2,
    |T|+|M| = 2(d+1)(k+2) = mn/2.

**Proof.** The listed edges have disjoint endpoints: the upper and lower band
edges use separate rows; the two lower endpoint positions reserved for
attachments are outside the internal-edge ranges; receiving endpoints lie in
the two caps outside the next band. None is a listed T vertex.

Every T in the left exterior lies on even checkerboard parity, and every T
in the right exterior lies on odd parity. No two T vertices in either region
are adjacent. The two regions are separated by the nonempty band. The nearest
left exterior tile to the band is its attached cap. Each of that cap's two
T vertices has its within-tile P neighbor; its other within-tile neighbor is B.
Its upper-left T has a blank neighbor above, namely the preceding band's lower
left endpoint (the source's lower left blank when i=1), and a blank to its left.
Its lower-right T has the lower band endpoint B to its right and a blank below,
or the rectangle boundary at the last layer. Reflection verifies the right cap.
T vertices farther into either exterior have only blank neighbors: the only
exterior P is in the cap, and its exterior neighbors are its two cap T vertices
and its matched partner above. The two source T vertices each see exactly one
P on their row and a blank below. All T constraints follow.

In the source, the outer tiles have t=s=1,r=0 and residual degree one. The
k inner tiles have h=1,r=1 and degree two. The source is therefore the stated
path, and k>=2 excludes a fork. Each nonterminal band end has h=s=1 and r=0;
each interior tile has h=2 and r=0. All have residual degree zero. The band
widths sum to (d-1)(k+2-d) over i<d. At the terminal band every tile has h=1,
r=1. Its lower-row edges join consecutive tiles, giving the path of w-1 edges
and the claimed excess. Saturated exterior tiles supply no residual edges.

There are 2i exterior tiles in layer i, each with two T vertices, plus the
two source T vertices. This gives the T formula. Summing the component
excesses gives q=0, hence the M formula; it also follows by counting the
displayed edge ranges directly. QED.

## 5. No fixed radius suffices for initial residual charges

Distance here is Manhattan distance in the grid of aligned tiles, **not**
distance in the residual graph, whose source and donor are disconnected.
In Proposition 3, every tile with rho<0 is in the terminal tile row d. Its
distance from the source component, which occupies every tile of row zero,
is exactly d. For w>=2 only the two terminal end tiles are negative, with
rho=-1/2 each; for w=1 the single terminal tile has rho=-1.

**Corollary 4.** For each integer radius R>=0 there is a feasible fork-free
configuration for which a residual component has excess +1 but its radius-R
tile neighborhood contains no tile with negative rho, and no negative-excess
component meets that neighborhood.

**Proof.** Choose d=R+1 and k=2d in Proposition 3. The only negative component
and all negative tile charges lie exactly d>R tile steps away. QED.

Thus a rule assigning to each positive component enough **initial negative
tile charge**, or enough negative-component excess, from a uniformly bounded
tile radius cannot prove q<=0 for all feasible configurations. The examples
are already fork-free and attain equality. The statement does not exclude
a radius depending on source length, a chain that transports debt as in
Theorem 2, different tilings, or objective-preserving changes to the matching.

## 6. Matching flips and capacity-two passages

Replace two horizontal matching edges occupying a square in vertex rows
2i+1 and 2i+2 by its two vertical edges, when both horizontal edges exist and
their columns form an aligned tile column. The square straddles two tile rows.
This operation preserves T, P, matching size and feasibility. Both participating
tiles are deficient in this family; the saturated attachment edges are retained.

In each affected tile h decreases by one, r increases by one, and residual
degree increases by two. Therefore rho=deg/2-r is unchanged tile by tile.
Such flips produce capacity-two passages and may merge the formerly separate
residual components. The support and amount of negative tile charge stay
unchanged, so the corresponding statement about distance from the fixed source
tile region still holds. The separate-components claim in Proposition 3 applies
to the displayed matching before these flips.

The prescribed routing after flips need not retain an LL and an HH path:
it can instead give two LH paths, depending on the port pairing and symmetry.
The invariant used here is rho, not the identities of the auxiliary routes.
There remain exactly two leaf terminals and two slack terminals, so a=b and
2a+c=2. This avoids a false routing-invariance assumption.

## 7. Reproduction and next proof boundary

```sh
python3 develop/check_compensation_transport.py --output develop/results/compensation-transport-2026-09-30.json
```

The recorded run checks depths 1,...,16 with four widths per depth, giving
64 base configurations and 128 partial/full matching-flip variants. All eight
square symmetries are checked, totaling 1,536 images. The verifier reuses the
existing direct-coordinate feasibility check, residual reconstruction,
fork-geometry checker and prescribed-routing/five-sixths verifier. It checks
the component classification, zero intermediate charges, exact donor distance,
per-band boundary term, matching counts and unchanged occupied sets under flips.
The smallest terminal bands of one and two tiles are both covered. Explicit
coordinate witnesses are archived with source hashes.

The finite controls accompany the written arbitrary-depth arguments; they do
not prove the all-size statements by enumeration. No new Lean theorem is claimed.
The previous boundary-aware verifier and its 928 images remain unchanged.

The next generalization must permit debt to travel unbounded distance. The
remaining geometric questions are how to route competing boundary debts through
turns or multiple exits, establish termination outside the decreasing-width
case, and assign terminal resources without reuse when candidate chains overlap.
The present lemmas settle the specified straight nested class; they leave
general bent paths and the unrestricted coefficient-one inequality open.

For a later joint manuscript addition, place the neutral-transfer lemma and
the arbitrary-distance obstruction after the boundary-aware result. No change
to the current arXiv source or manuscript is made by this research note.
