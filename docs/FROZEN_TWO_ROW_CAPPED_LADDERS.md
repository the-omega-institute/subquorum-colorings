# Fully frozen two-row components with arbitrarily many squares

19 October 2026. This gives an explicit all-length obstruction to extending
PURE_TWO_ROW_COMPONENT_REDUCTION.md from complete rectangles to arbitrary
endpoint components contained in two rows. The submitted manuscript is
preserved. Coordinates below are normalized; all unlisted vertices are blank.

## 1. The family and exact hypotheses

Fix any integer w>=3 and put q=w mod 2. Take the endpoint set

    H=({0,1} x {0,...,w-1}) union {(0,-1),(q,w)}.

Thus a full two-row ladder has one extra horizontal endpoint at each end,
on the same row for even w and opposite rows for odd w. The matching has
the following w+1 edges:

- (0,-1)--(0,0);
- (j mod 2,j-1)--(j mod 2,j), for 1<=j<=w.

Write out(0)=-1 and out(1)=2 for the two exterior row coordinates.
Take precisely these six selected supports:

    T={(-1,-1),(0,-2),(2,0),
       (out(q),w),(q,w+1),(out(1-q),w-1)}.

Translation by (2,2) embeds the configuration in a rectangle of height six
and even width W=w+4 for even w, W=w+5 for odd w. Unlisted sites are blank;
the axial supports can lie on the left and right ambient boundaries.
It preserves the even alignment of the central ladder.
The endpoint graph has one complete component H. Every selected support
has exactly its intended endpoint neighbor and no selected neighbor: the
supports on each exterior row are separated by at least three columns.
Hence the pair is feasible. Every endpoint has occupied degree three:
the two tails have one endpoint neighbor and two selected supports, the
two opposite-row end corners have two endpoint neighbors and one support,
and every other
endpoint has three endpoint neighbors. The pair is single-terminal.

The exact counts are

    |T|=6, |P|=2w+2, |M|=w+1, |T|+|M|=w+7.

There are w-1 all-P unit squares, including floor(w/2) squares aligned with
the fixed even 2-by-2 tiling. The whole endpoint component, including
both pendant endpoints, lies in two consecutive rows.

## 2. A general acyclic freezing proof

Let m denote the displayed actual matching involution. Define the left wave

    z_0=(0,-1),
    z_j=(1,j-1) for odd j, and (0,j-1) for even j, 1<=j<=w.

These are exactly the w+1 endpoints of odd grid color. The initial tail
z_0 freezes because it has two selected supports. Its retained mate is
(0,0). Vertex z_1=(1,0) therefore freezes using that retained neighbor
and its southern selected support (2,0).

For every 0<=j<=w-2, the next wave vertex z_(j+2) has the two distinct
neighbors m(z_j) and m(z_(j+1)). To check this directly, m(z_0)=(0,0),
and for j>=1 the mate of z_j has the same row and column j, including
the terminal case z_w=(q,w-1), whose mate is the right tail (q,w).
The row alternation makes one of these two incidences horizontal and the
other vertical. Their columns differ, so the two neighbors are distinct.

Induction now freezes z_(j+2) after the preceding two vertices: their
mates must remain occupied in every feasible bundle. No assumption that
a retained mate keeps its endpoint label is made. This freezes the entire
left wave without any cyclic premise.

For even w use J(r,c)=(r,w-1-c), and for odd w use
J(r,c)=(1-r,w-1-c). This map preserves T and the matching and exchanges
the two grid colors in both cases. It gives a second wave containing
exactly all even-color endpoints. The waves are disjoint and exhaust H.
Therefore every endpoint is universally frozen. No nonempty feasible
promotion bundle exists in the displayed baseline, even with mixed orientations.
In arbitrary feasible exterior completions retaining H, its matching and
the six supports, no global bundle can use an edge of H. Other components
can still admit their own promotions. The reflection need preserve only
the prescribed matching-and-support pattern, not the completed exterior.

The displayed baseline has no matching edges outside H, so no sequence
of nonempty promotions can even start. Thus square-eliminating
normalization is impossible in this two-row-supported component. This
refutes the proposed shape extension, not the complete-rectangle theorem:
its two horizontal pendant endpoints are part of the component and their
matching edges leave the central rectangle.

## 3. An exact constant receiver budget

Use the even 2-by-2 tiling after the even translation above. Let R be
exactly the set of tiles containing endpoints of H. It consists of
floor(w/2) central full-P tiles and two end tiles.

For clarity, t,p,b count selected, endpoint and blank sites in a tile;
h counts its internal matching edges; s counts its endpoints whose mates
are in saturated tiles. A tile is saturated when t=2, and deficient when
t<=1. The residual degree d counts matching incidences to other deficient
tiles and r=2-t-h-s. Since p=2h+s+d, a deficient tile has

    rho=d/2-r=t+p/2-2+s/2=(t-b+s)/2.

A saturated tile has charge zero. Charges are always measured in the full
original configuration, and rho(U) is their sum over the physical tiles
in U. In particular the correction s/2 must not be dropped in a general
region. All receiver tiles below are deficient and have s=0.

For completeness, this is the original global ledger, not the raw physical
excess assigned independently to every tile. Let a be the number of
saturated tiles containing a matching endpoint. Such a tile has exactly one
P, no internal matching edge, and its mate lies in a deficient tile, by
Lemma A.1 of GRID_ABSORPTION_PROOF.md. Hence sum_deficient s=a. Summing
the raw quantity t+p/2-2 over saturated tiles gives a/2, exactly the
correction transferred to deficient tiles. On an even-by-even rectangle,

    rho(grid)=sum_all_tiles(t+p/2-2)=|T|+|M|-mn/2.

This proves both the global objective identity and additivity on disjoint
tile regions while retaining every saturated attachment correction.

Each central tile contains one internal lower horizontal matching edge.
Its two upper endpoints are matched across tile boundaries, including
the end crossings to the two end tiles. All tiles in R are
deficient, so s=0. Consequently each central tile has

    (t,p,b,h,s,r,d)=(0,4,0,1,0,1,2),   rho=0.

The left tail tile has the upper-row axial T and tail P, and two lower
blanks. Its P is matched into the central ladder. For even w the right
end tile is its reflection. Each therefore has

    (t,p,b,h,s,r,d)=(1,1,2,0,0,1,1),   rho=-1/2.

For odd w the right end tile instead contains the last core column and
the lower-row tail. It has three P, one blank and one internal lower
matching edge; its other endpoint is matched across its left boundary.
Its counts are

    (t,p,b,h,s,r,d)=(0,3,1,1,0,1,1),   rho=-1/2.

These end-tile labels are forced in every feasible exterior that retains
H as a complete endpoint component, its matching and the six supports.
At the left end, the axial T at (0,-2), already adjacent to the tail,
forces (1,-2) blank. The remaining corner (1,-1) cannot be selected
because it touches both the tail and (1,0), and cannot be P because it
would join H. For even w the reflected argument handles the right end.
For odd w its only missing corner (0,w) touches the upper last core
vertex and the lower tail, so is neither T nor P and must be blank.
All central tile sites are already P. Thus arbitrary feasible exterior
components cannot alter any label or charge of R.

The other selected supports lie outside R. The exact original receiver counts are

    |R|=floor(w/2)+2,  T_R=2-q, P_R=2w+2, B_R=4-q,  rho(R)=-1.

Every matching edge has both endpoints in R. The charge is computed once
per physical tile, retaining all internal matching incidences. It is the
original ledger of SQUARE_FREE_ENDPOINTS_AND_OWNED_DONORS.md, not a new
normalization-dependent charge.

Thus a fully frozen endpoint component can have arbitrarily many all-P
squares, or arbitrarily many aligned full-P tiles, while its endpoint-tile
receiver has only one unit of negative charge. No fixed positive payment
per square can be allocated from this receiver at every width. The same
one-unit budget cannot be counted separately for all its overlapping squares.
An enlarged exterior receiver may contain additional resources; this result
does not bound all such enlargements or refute the global grid inequality.
Indeed the displayed whole objective is w+7, whereas half the ambient
area is 3W>=3w+12, larger by at least 2w+5.

## 4. Automatic packing and a component-level compensation lemma

Consider L distinct endpoint components of the capped-ladder form above,
allowing different widths and tile-preserving translations, reflections
and transposition, in one feasible configuration. Retain all six stated
supports and the actual matching for each component. Let R_i be exactly
the tiles containing its endpoints.

**Capped-component compensation lemma.** The R_i are automatically
pairwise tile-disjoint, and

    rho(union_i R_i)=-L.

For any pairwise tile-disjoint source regions S_1,...,S_K outside these
receivers with rho(S_j)<=1, and remainder W, the exact global partition
therefore gives

    rho(whole grid) <= K-L+rho(W).

In particular K<=L and rho(W)<=0 imply |T|+|M|<=mn/2 on an even-by-even
ambient grid. This is a coefficient-one sufficient class, not a universal
improvement of 5/6 or a proof of source coverage.

Proof. Every tile in R_i has its complete nonempty P set in its own
component, by the forced labels just proved. If it also belonged to R_j,
it would contain a P from that distinct component, a contradiction.
Thus the receivers are disjoint without an extra collar-disjointness
hypothesis. Sum rho(R_i)=-1 once per component, and then add the source
bounds over the disjoint physical tile partition. The remainder term
is retained explicitly. QED.

This allocates two negative end-tile half-contributions only once per
entire capped component. Their number does not grow with the number of
squares. For odd w the three-P end tile is not an endpoint donor with
at most two occupied vertices, so that earlier donor lemma is not silently
invoked; its actual original charge is used directly.

## 5. Verification and next geometric question

The general freezing induction and tile count above are the proofs.
The physical verifier checks every w from 3 through 64, all eight
grid symmetries, the complete endpoint component, actual matching,
single-terminality, both waves, exact receiver ledger and full freezing.
It exhausts all orientations for w=3,...,8; the first case has 80 nonempty
oriented choices and no feasible one. Finite checks do not replace the
all-length induction.

The generic two-step freezing induction is checked in
formal/SubQuorum/BipartitePromotion.lean. Its coordinate adapter and the
family's exact tile geometry retain the written proof. The separate
complete-freezing theorem also shows that both one-color cores are empty.

Oracle task c41e37b4-8e1f-48f1-bf9c-e96ce8824052 returned an explicit
eight-endpoint 4-by-7 counterexample at 07:05:30 UTC, observed gpt_6/pro.
It is the odd case w=3 above, with a different padding translation. Its
exact response is archived and the original coordinates independently
checked. The response also independently confirms the general bipartite
color-factorization and complete-freezing arguments. The all-width family,
constant receiver budget, code and Lean induction are subsequent work;
they were not reviewed in that response.

The subsequent written-proof review c9c582db-aa9b-440a-8334-fcb958d84650
completed at 07:24:57 UTC, observed gpt_6/pro. Its verdict is REVISE solely
for missing ledger definitions and the global objective identity in the
submitted excerpt; it confirms the all-width construction, both freezing
waves, odd-width geometry, forced labels and receiver packing. The exact
response is archived in output/capped-ladder-review-response.json. Section 3
now supplies the actual corrected ledger and its objective identity; the
reviewer's proposed raw per-tile excess is used only where s=0, not substituted
for the original ledger on arbitrary regions. The boundary and exterior-scope
clarifications are incorporated above. These repairs were independently
checked; no subsequent ACCEPT or code/Lean execution review is claimed.

```sh
python3 develop/check_frozen_two_row_caps.py --output output/frozen-two-row-caps-controls.json
```

The residual problem must permit genuinely frozen components with several
squares even at total endpoint height two. Further work should treat a
whole capped ladder as one receiver, with its actual total budget, and
prove how distinct positive sources may be assigned to that receiver
without reusing its two negative end-tile contributions. No universal source-coverage or
improved 5/6 theorem follows yet.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
