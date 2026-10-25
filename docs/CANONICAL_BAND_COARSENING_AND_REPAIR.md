# Canonical bands at fixed N: resource transport and a sharp repair frontier

26 October 2026. Wenlin Zhang and Haobo Ma. Independent research continuation.

The [mixed-terminal theorem](MIXED_TERMINAL_DEFECT_AND_FROZEN_OBSTRUCTION.md)
requires the ordinary local-band boundary term b as well as the seam term s.
Here we remove unnecessary boundaries before trying to optimize directions.
For **every** feasible (T,M), any aligned even-rectangle H/V partition can
be replaced by canonical maximal bands with the **same auxiliary matching N**.
Every global owner and terminal is unchanged; positive original forest units
have a bijection; every old support, link, beta entry and payment pack embeds.
This holds for any jointly transported available resource pool and preserves
each already paid source identity and its routes. No freezing or degree
hypothesis is needed for this general coarsening theorem.

Consequently the canonical bands dominate every compatible rectangle
partition with that N. Under the degree-three terminal hypothesis, d4, s
and eHV stay fixed, while b and the exact port deficit cannot increase.
This reduces partition selection to choosing one H/V bit per aligned 2x2
tile: the cuts along equal-direction runs can be removed without loss.
It does **not** solve that remaining orientation problem.

The improvement can be unbounded even with **no direction change at all**.
For an actual unique-M fully frozen fixed-P maximum, 2x2 all-V regions have
full original-pool deficit k; canonical V bands pay all k at zero links.
N, T, M, all owner bodies, the 2k original units and numerical slack 2k
are the same. Only resource access was truncated by the cuts. Thus a full
deficit in a needlessly subdivided model is not an obstruction at fixed N
once same-direction coarsening is allowed.

On this family we also prove the exact frontier under arbitrary sealed T
reselection, partial axial cut removal, and a deficit limit d:

    max |T| = tau - max(0, k-d-j),                      (1)

where j is the allowed number of removed elementary axial cuts. All upper
bounds and attainments below are general proofs; finite checks test their
adapters. The universal 5/6 improvement and arbitrary-P orientation problem
remain open. This is not a revision of the submitted manuscript.

## 1. Canonical bands determined by N

Use the board, feasible T, actual matching M, full restored M/PP owners,
whole-owner no-P-gap support, original BB/TT forests, physical TP-to-BP
within-band links, and beta fork convention of the preceding notes.
All actual matching edges are restored **before** identifying owners.

Every rectangle in an even-by-even rectangle partition has even boundary
coordinates: a horizontal interior line is tiled from zero by even-length
intervals, and the vertical argument is identical. Hence each rectangle
is a union of the standard tiles

    Q(r,c) = {2r,2r+1} x {2c,2c+1}.

Within a tile the auxiliary matching has just the H choice (vertical pairs,
horizontal band axis) or V choice (horizontal pairs, vertical band axis).
The resulting N determines that bit uniquely. Calling it a direction bit
does not introduce a choice of actual M or a second matching phase.

For each tile row, take each maximal consecutive H run and make its union
one height-two H rectangle. For each tile column, take each maximal V run
and make its union one width-two V rectangle. Call the resulting collection
C(N). Its members are disjoint, cover the board and have even side lengths.
Its auxiliary matching is exactly N. Every band of every rectangle partition
realizing N is an axial subinterval of one of these canonical bands.

One may split a tall H rectangle into its constituent height-two bands,
or a wide V rectangle into width-two bands, without changing any band.
Then C(N) is obtained solely by concatenating adjacent same-direction bands
on the same physical row pair or column pair. Nothing is identified across
different canonical bands. The canonical rectangles are unique up to their
order in the list; no greedy rectangle-cover choice is involved.

## 2. General resource transport theorem

Let F be any compatible rectangle partition and C=C(N). There is a
bijection

    rho : positive original forests of F
           -> positive original forests of C              (2)

such that the cells of j are contained in the cells of rho(j). In particular
the total original-unit count L and the exact ledger S=L+beta-alpha do not
change. Resource identities in different partitions are transported by rho;
we do not pretend that a merged forest has exactly the same cell set.

**Proof of the bijection.** Along a fixed physical band the labels of every
column are the same before and after concatenation. Forest edges join
consecutive BB/TT columns precisely when at least one is TT. Removing a cut
can add such an edge; it cannot remove an existing forest edge. Each fine
forest is therefore contained in exactly one coarse forest. The fine
forests inside a coarse forest partition its physical columns and cells.

Every forest on any of the allowed even-length bands has capacity
number(BB)-number(TT) equal to zero or one. To see nonnegativity without
an extra assumption, feasibility forces every existing neighbour of TT
to be BB. A forest alternates. It starts and ends with BB unless it hits
a band boundary with TT. A forest with two TT ends would have to fill
the whole band, whose length would then be odd, contrary to the even
side length. All other cases have difference zero or one. A single BB is
the remaining positive case.

For a coarse forest K, capacity is additive over its fine forest children:

    cap(K) = sum_{j child of K} cap(j).                   (3)

All summands are zero or one. If cap(K)=0, every child has capacity zero.
If cap(K)=1, **exactly one child** has capacity one. Conversely every positive
fine forest has a positive parent by (3). This proves (2), including
injectivity: two old positive units can never merge into one positive unit.
Balanced forests contribute zero and are not separately credited. QED.

**Support and pack embedding.** Global M/PP bodies depend only on M and N,
so the same bodies, terminal coordinates/types, alpha sources, beta BP
entry gates and whole-beta capacity-one sinks occur in F and C. Every
within-band TP-to-BP edge in F is still within its containing band in C.

Suppose an old positive unit j is supported by owner a. Its fine maximal
no-P gap has a P column of a immediately at one boundary. In the coarse
band that P column is still present, hence still blocks extension at that
boundary. The no-P gap can extend through removed cuts only on the other
side. The containing positive forest rho(j) lies in that enlarged gap:
a BB/TT forest cannot cross a column containing P. Thus rho(j) is supported
by a. We have

    rho(W_F(a)) subset W_C(a),    links_F subset links_C.  (4)

Each old interval primitive keeps its exact owner path, links, terminal
coordinates and interval witness owner, replacing j by rho(j). A beta
primitive keeps its old beta and BP entry. A fork keeps its two distinct
BP entries, all owner-disjoint arms, one whole-beta sink and its one
transported interval, if required. No owner or link is duplicated. Since
rho is injective, two distinct spent interval units remain distinct.
Thus **every old simultaneous pack**, with all its source identities and
link costs, embeds in C. This proves the theorem for the complete model,
including beta forks, rather than just for a scalar terminal bound.

In particular, for ANY old available subset U, compare F restricted to U
with C restricted to rho(U). Every old pack still embeds. The same holds
when specifying an old paid source set and when withdrawing arbitrary
units jointly. The two pools are alternatives under (2), never added.
For any fixed attainable target/source prescription the minimum link cost
cannot increase. If the maximum value increases, this does not compare the
cost of two different maximum-value targets.

The assertion concerns the stated within-band support/link model. It does
not prohibit extra physically justified links in a larger model. If such
links are also retained under coarsening, the same embedding proof includes
them; they are not needed for the theorem here.

## 3. Consequence for the mixed-terminal tax

Assume every global alpha terminal has occupied degree at least three,
as in the preceding mixed-terminal theorem. N and the occupied physical
graph do not change. Thus d4 and the seam condition

    w=2v-N(v) is blank

are invariant terminal by terminal. The H/V bit at every site is also fixed,
so the set of actual M edges with opposite-direction endpoints, and hence
eHV, is invariant. Total rectangle-crossing M counts need not be invariant;
we only assert invariance of the actual opposite-direction edge set.

An old positive terminal port remains positive under (2). A previously
missing local-axis port can become internal, and a balanced port can enter
a positive coarse forest. Neither event creates a new zero incidence.
Consequently

    b_C <= b_F,    D_port,C <= D_port,F,
    2 D_port,C <= d4+b_C+s <= d4+b_C+eHV.               (5)

For the deficit assertion, transport the old terminal-to-positive-forest
allocation using rho, as in Section2. This keeps every old paid alpha and
uses each positive forest at most once. There is no need to assume that
the abstract zero vertices or path components themselves remain identical.

The criterion d4+b_C+s<=2beta+1 therefore proves the coefficient-one
numerical bound whenever it holds after canonical coarsening. It is at
least as strong as checking any compatible finer partition.

Every canonical axial endpoint is either an outer board boundary or abuts
a tile of the opposite orientation. Balanced boundary forests can extend
from a terminal to such an endpoint. Those **genuine** direction interfaces
and outer boundary effects remain in b_C. They cannot be discarded by
renaming the bands or by minimizing eHV alone.

In particular the preceding H4/V6 sharp seam family already has maximal
axial bands. Canonicalization only splits rectangles transversely into
the same constituent bands, so its model is unchanged: b=0, s=eHV=2k and
full deficit k remain. The present theorem removes artificial cuts and
does not remove that genuine seam obstruction at its fixed mixed N.

## 4. Fully frozen maxima with a same-N unbounded repair

Use configuration(W,k) and the existing unique-M/fixed-P maximum theorem,
for even W>=8 and k>=1. Put c_i=10i. The board and exact counts are

    (W+2) x (10k+2),
    tau = (7k+2)(W/2)+3k+2,
    |M| = k(3W/2+5),    S=2k.                          (6)

T* has size tau and all endpoints are frozen. Choose V in **every tile**.
First take every aligned 2x2 tile as its own region. Then concatenate
vertically to form the canonical full-height width-two V bands. Both
partitions have exactly the same N. The global components are the existing
uniform-V components. For each module there is one alpha L_i with ordinary
ends

    (1,c_i+3), (W,c_i+3),

and body the central P columns c_i+4,c_i+5, together with those two leaves.
No other component is alpha. There are k betas, k(W/2-2) mixed owners and
exactly 2k original forest units. Every alpha end has occupied degree three.

The only original units in T* lie at the two blank rows in the vertical
column pair {c_i+2,c_i+3}:

    upper J_i^+ = {(2,c_i+2),(2,c_i+3)},
    lower J_i^- = {(W-1,c_i+2),(W-1,c_i+3)}.             (7)

The complete word in that column pair is BT at row0, TP at row1, BB at
row2, only BT/TB at rows3,...,W-2, BB at rowW-1, TP at rowW, and BT at
rowW+1. Here TP denotes the physical column with one T and one P, without
asserting that the selected site is itself a terminal. The central column
pair contains P in every row1,...,W and one selection at each exterior cap.

In 2x2 regions both units in (7) are separated from the leaf by a region
cut. The central exterior caps are BT, and no other band has a P column
of L_i. Thus its **complete** original support is empty. Its two ordinary
ends have no outgoing link: the only local-axis neighbour within their
2x2 band is one of the selected leaf seals. No beta or mixed route can
be reached from L_i. Therefore the complete model, not just the port
certificate, has

    V_fine=0, D_fine=k, d4=s=eHV=0, b_fine=2k.          (8)

After concatenation, (7) are two private positive singleton forests in
L_i's whole support, immediately beyond its leaves. They are not supported
by any other open owner. All k alphas are paid by different upper units,
at zero links:

    V_canonical=k, D_canonical=0, b_canonical=0.         (9)

These particular singleton cell sets do not even change during concatenation.
There is no extra slack, selected-point loss, rematching, direction flip or
new beta credit. This rules out treating an arbitrary-cut full-pool deficit
as an intrinsic fixed-N deficit. It also shows that omitting b from a
fine-partition argument would be wrong even when s=eHV=d4=0.

## 5. Arbitrary T, exact local gates and the joint quota frontier

Keep this fixed P,M and all-V N. Allow ANY final feasible T retaining only
the four leaf seals in each module:

    (0,c_i+3), (1,c_i+2), (W,c_i+2), (W+1,c_i+3).       (10)

No old-T retention is assumed. As in the prior sealed-frontier theorem,
freezing the two designated column3 leaves implies precisely these seals;
full freezing suffices. Every L_i is still alpha with degree-three ends,
no other component is alpha, and no L_i has an outgoing band link.

Consider ANY segmentation of each width-two V band at even row coordinates.
Start with all 2x2 bands and remove a set Z of elementary axial cuts. Write

    q_i = 1 if (2,c_i+2) or (W,c_i+2) belongs to Z,
          0 otherwise;       q=sum_i q_i,
    h_i = loss(0,c_i+4)+loss(W,c_i+4),
    ell = tau-|T|.                                        (11)

The two loss terms in h_i are capacities minus selected counts on the
top/bottom central aligned 2x2 cover tiles. Each has capacity one; losses
are zero or one. These 2k tiles are distinct and are not among the patched
four-row tiles in the existing ALL-T cover, hence

    ell >= sum_i h_i.                                     (12)

**Exact local rule.** L_i has positive support iff q_i=1 or h_i>0. All its
supported original units are private relative to EVERY other open owner.
Consequently, over the complete original pool,

    V = #{i:q_i=1 or h_i>0},
    D = #{i:q_i=0 and h_i=0},    minimum links=0,
    ell+D+q >= k,    q <= |Z|.                             (13)

**Proof.** Feasibility and (10) force both rows2 and W-1 of the leaf column
pair to be BB, independently of all other choices of T. In an interior
row, a TT pair in these columns is impossible: its column3 selection would
see its column2 partner and the fixed P in column4. At the exterior rows,
the seals force BT. Thus there are no TT columns in this entire vertical
band, and every BB is its own positive singleton forest.

The upper leaf's segment reaches the forced upper singleton iff its first
cut at row2 is removed; the lower statement uses rowW. If neither is
removed, the two leaf segments contain only the respective exterior BT
cap and the P leaf column, giving no unit. If a cut is removed, its forced
singleton is positive and supported regardless of how far the segment
continues or which other cuts are retained.

In the central band, every interior row contains P, so the only possible
no-P support gaps are the two exterior one-row caps. Each is BB exactly
when its cap loss is one. Any positive unit so obtained is private to
L_i. The leaf-band gaps also have only the same L_i as possible P boundary
owner, on either or both sides. No other band contains any of L_i's body.
This exhausts its support, including arbitrarily reselected T, and proves
the local rule and privacy. Its selected seals still prevent terminal exits
in every segmentation. Distinct sources therefore compete for no resource,
and beta routes cannot add payment to an unsupported source. This proves
the first two lines of (13).

There are k-D paid modules. At most q are hit by a removed guard cut. Each
remaining paid module has h_i>=1, using distinct cap losses in (12). Hence
k-D<=q+sum_i h_i<=q+ell. One physical cut can hit only its one module's
column pair, so q<=|Z|. A module hit at both ends still contributes only
one to q; its two reserve units cannot pay two sources. QED.

In particular canonical full-height bands always pay all k for every T
satisfying (10), without changing T or N. On T* all h_i=0, so the exact
value is the number of modules hit at an upper or lower guard cut.
Removing unrelated cuts has no payment benefit, and two guard cuts in
one module have the same value as one.

**Sharp joint frontier.** For integers j>=0 and 0<=d<=k, the maximum final
|T| among fully frozen final selections and vertical segmentations with
at most j removed elementary cuts and D<=d is exactly (1).

The upper bound follows from ell>=0 and (13): ell>=k-d-j. For attainment
put q=min(j,k-d). Starting with T*, remove the q upper guard cuts in q
different modules. In each of k-d-q further modules delete exactly the
upper central outer selection (0,c_i+5), opening one private central BB
singleton. Leave every other cut and selection intact. The first q modules
are paid by their old upper guard units; the next k-d-q by their new cap
units; the remaining d are unpaid. All routes have zero links and use
different physical original units.

There are k-d-q=max(0,k-d-j) deletions. The existing common strict-rank
freezing certificate from the inventory frontier works with these upper
central partners absent; it depends on neither N nor the segmentation.
Thus all endpoints remain frozen and the upper bound is attained. With
j=0 this recovers a net-loss-k full-repair obstruction under the tiled
decomposition. With j>=k-d it attains tau with no point loss at the same N.
The elementary-cut count charges cuts separately in each physical band;
merging a larger rectangle may remove several such cuts at once.

## 6. Verification and remaining scope

Run the physical checker and the separately scoped Lean audit:

    python3 develop/check_canonical_band_coarsening.py --output output/canonical-band-coarsening-validation.json
    python3 develop/check_canonical_band_fork_controls.py --output output/canonical-band-fork-controls.json
    python3 develop/check_canonical_band_coarsening_formal.py --lean /path/to/lean-4.33.0 --output output/canonical-band-coarsening-formal-validation.json

The physical checker independently extracts all fine/coarse forest cells,
partitions each parent into its children, verifies capacity addition and
the positive-unit bijection, transports all owner supports and links, and
checks every individual old primitive on small models, including forks.
It compares complete and jointly restricted original pools, independent
primitive optima, terminal-tax monotonicity, arbitrary T rebuilt from only
seals, arbitrary relevant/irrelevant cuts, sharp quotas, strict freezing
certificates and a serialized permanent fixture. Random unfrozen boards
exercise the general theorem without terminal degree assumptions.

The separate fork controls ensure the pack claim is nonvacuous for beta
forks: eight actual two-entry beta-fork primitives embed under coarsening.
They also check four sharp same-N family instances, including equality of
the positive singleton physical cell sets before and after coarsening,
and four H4/V6 seam controls whose deficit correctly remains k.

Completed physical checks passed 346 general coarsening models (80 with
random unfrozen geometry), 38,291 positive-resource transport checks,
477 complete-pool/joint-withdrawal comparisons, 157 independent primitive
optimum pairs and 266 terminal-tax monotonicity comparisons. Family checks
passed 1,101 arbitrary-T/cut profiles, including 200 rebuilt from only
leaf seals, 435 maximum-T arbitrary-cut profiles, 465 sharp frozen joint
quota attainers and 224,812 strict freezing events. The supplemental
nonvacuity controls passed 108 individual old primitive embeddings and
nine additional independent optimum pairs. Local Lean4.33.0 passed all
16 declaration audits without warnings, sorry, native evaluation or new
axioms. The receipts record the separate scopes and counts.

Lean verification proves the arbitrary-length nonnegative-child uniqueness
argument behind resource injectivity, transport of disjoint resource packs
and selected source witnesses under an injective resource map, and the
joint cap-loss/cut quota arithmetic. The coordinate canonical-band adapter,
geometric support inclusion, actual forest partition, freezing schedule
and all-size family classification remain written proofs and executable
checks. No end-to-end Lean grid theorem is claimed.

The next geometric problem is now more precise: after choosing the tile
orientation and forming C(N), control the **remaining** ordinary boundary
defects and seam defects together, or give deficient paths additional
whole-body resources in one global allocation. A defect caused entirely
by an avoidable cut has been eliminated from that problem. No result here
guarantees that all orientation mosaics, or even an optimal one, pay every
alpha on arbitrary frozen P.
