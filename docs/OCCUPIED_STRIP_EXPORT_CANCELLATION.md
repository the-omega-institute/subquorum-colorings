# Occupied strips: cross-band refunds and the exact unmatched debit

26 October 2026. Wenlin Zhang and Haobo Ma. Independent research continuation.

The [occupied-strip flux theorem](OCCUPIED_STRIP_MATCHING_FLUX.md) charges half
a unit whenever a TP-column endpoint is matched outside its strip. We identify
which of these apparent losses cancel when disjoint occupied strips are used
together. An actual TP-to-BP matching edge has a different BP column available
for the refund, even across strip boundaries and different strip directions.
The only remaining deductions are one unit per TP-to-TP edge, half per
TP-to-PP edge, and half per TP endpoint matched outside the entire union.
All three coefficients have fully frozen sharp regional controls.

This supplies a geometric compensation criterion allowing an original endpoint
component to cross several selected bands. The old requirement that each
complete receiver lie inside one strip is unnecessary. A general finite mate
injection and a column-forest identity prove the result. These are elementary
counting tools, not a new matching or max-flow theorem. We do not claim a
universal 5/6 improvement or that all frozen alpha demands are routable.

## 1. Regions and the original column ledger

Let (T,M) be feasible on a finite rectangular nearest-neighbor grid. Write
P=V(M); every T has at most one occupied neighbor in T union P. Terminality
or freezing is unnecessary until the geometric refinement in Section 4.
Take finitely many **vertex-disjoint** regions I_i, each a two-row or two-column
rectangle of consecutive columns in its own orientation. Orient each so that:

- its first column is entirely blank;
- its last column has at least one blank corner;
- it has n_i>=2 columns.

Here blank excludes both T and P. The regions may have different directions,
may have odd lengths, and need not individually follow the original 2-by-2
tile boundaries. When using the physical tile ledger below, their UNION must
be a union of original tiles; we do not reset the tiling.

Use the original column types TT, BB, TP, BP, BT and PP. The letter B in
these types means blank, not beta. These are physical cell labels, not
strand TP/BP terminal types; the edges counted here belong to the actual M,
not to a selected terminal-link routing. Put

    K_i = (# BB columns) - (# TT columns),
    K = sum_i K_i,
    S_i = n_i - |T intersect I_i| - |P intersect I_i|/2,
    S_U = sum_i S_i.

Let delta_i=2 if both end columns are blank and n_i is even; otherwise
let delta_i=1. The established BB--TT column forest gives

    K_i >= delta_i,       Delta = sum_i delta_i.             (1)

For clarity, every TT column has two neighboring BB columns and cannot occur
at an end. The graph on BB/TT columns with edges incident to TT is a subgraph
of the column path, with twice as many edges as TT vertices. Its number of
components is K_i, and the first BB ensures at least one. If both ends are
BB, equality K_i=1 forces the entire trace to alternate BB,TT,...,BB, of odd
length. Even n_i therefore gives K_i>=2. No endpoint-free hypothesis is used.

Let C,D count all TP and BP columns in these regions. Direct label counting
on the SAME vertices gives

    2S_U = 2K + D-C.                                      (2)

All subsequent accounting concerns this regional surplus itself. Refunds
must not be added again to S_U as independent donor resources.

## 2. The exact joint matching-edge theorem

Classify actual matching edges incident to regional TP endpoints:

- g: edges from a TP endpoint to a BP endpoint somewhere in the union;
- h: edges whose two endpoints are in TP columns of the union;
- j: edges from a TP endpoint to a PP-column endpoint in the union;
- o: edges from a regional TP endpoint to a mate outside the union.

A TP-to-TP edge is counted ONCE in h, not once at each end. Each BP column
has one endpoint, hence can be the target of at most one g edge. Put

    u = D-g >= 0.

This u is the count of BP columns not used as mates of regional TP endpoints.
It is an exact residual count, not a second supply of physical interval units.

**Theorem 1 (joint flux and cancellation).**

    2S_U = 2K + u - 2h - j - o.                            (3)
    S_U >= Delta - h - (j+o)/2.                            (4)

In particular, if every regional TP endpoint has its actual mate in a BP
column of the union, then

    S_U >= Delta,                                         (5)

even though strips can have transverse matching exports and a complete
original receiver may be split across several strips.

**Proof.** Each regional TP endpoint has exactly one actual mate. The mate
is either outside, or in a column with one or two endpoints. Inside the
union its type is therefore BP, TP or PP. These cases exhaust all possibilities.
A g edge accounts for one TP endpoint, an h edge for two, and a j or o edge
for one. Thus

    C = g + 2h + j + o,        D = g+u.

The map from g edges to their BP columns is injective: a BP column contains
one endpoint and its actual matching mate is unique. Disjoint regions keep
each endpoint and column in one place, including perpendicular region choices.
Substituting these equalities into (2) proves (3). Apply K>=Delta and u>=0
to obtain (4). Under the hypothesis of (5), h=j=o=0. ∎

A TP endpoint matched within its own strip always has a horizontal BP-column
mate in that strip: the TP's T already sees its P, so the adjacent T-row
position must be blank. Consequently h and j are genuinely cross-strip
interactions. Let r count g edges crossing between different strips, and let
e_i,u_i be the previous single-strip export and unused-BP counts. Then exactly

    sum_i e_i = r+2h+j+o,       sum_i u_i = r+u.             (6)

Each safe crossing was a half-unit export deduction in its first strip and
an unused-BP half-unit credit in its target strip. They cancel once. Equation
(3) exposes that cancellation without assuming receiver closure in each strip.
It does not strengthen or contradict the earlier exact single-strip identity;
it gives a more permissive geometric sufficient condition from their joint use.

## 3. Consequence for the original grid, without resource reuse

For this section assume the board is tiled by its original 2-by-2 tiles,
and the union U is a union of those tiles. Let D_U be the
original endpoint-free tile deficit and rho_U the RAW charge of its endpoint-
bearing tiles, with each such tile's charge |T in tile|+|P in tile|/2-2. Then

    S_U = D_U-rho_U.

Partition the endpoint-bearing tiles outside U into any disjoint blocks.
For each block use the sum of its raw tile charges. Let q be their total
positive charge and R the absolute total negative charge. Let D_out be the
endpoint-free deficit outside U. Each original tile appears in exactly one
of these terms, so the whole-board margin is exactly

    S_whole = S_U+D_out-q+R.

Together with (3), this gives the sufficient criterion

    q+h+(j+o)/2 <= K+u/2  ==>  S_whole>=0.                  (7)

A conservative version replaces K+u/2 by Delta. Both keep all signed
half-units until the final sum; separate upward rounding is unjustified.
For example, if h=j=o=0 and q<=Delta, then

    |T|+|M| <= area/2.

Thus the coefficient-one bound holds on this explicit class, eliminating
the |M|/6 allowance of the old 5/6 bound THERE. No claim that every grid
admits these regions and outside-charge estimates is made.

Blocks need not be complete endpoint receivers; their charge is then RAW,
not the charge of a separately counted full component. To reuse existing
complete-receiver source bounds, one sufficient condition is that every
receiver meeting U be entirely inside U, and all outside receiver blocks
be disjoint. A receiver may be split across several I_i. In a single-terminal
configuration distinct endpoint components have disjoint receiver tiles:
if separate components occupied two diagonal corners of a tile, degree at
least three would require another occupied corner; it cannot be T adjacent
to both P, so a P corner would join the components. This proves the needed
disjointness. Internal matching transfers cancel over each whole receiver.

The criterion concerns the physical margin, and can remain valid with unpaid
alpha demands in the complete fork flow. Indeed the known
[full-pool frozen singleton family](FULL_POOL_SINGLETON_OBSTRUCTION.md) already
rules out deriving universal full routing from freezing alone. The correct
next target is deficit versus unused physical slack, rather than requiring
alpha-F to vanish in all frozen configurations.

## 4. Single-terminal geometry of a safe parallel export

**Lemma 2 (a boundary P-square is forced).** Suppose two parallel selected
strips have a TP-to-BP actual matching edge crossing their boundary, and every
endpoint has occupied degree at least three. The matching edge lies on at
least one all-P unit square spanning that boundary.

**Proof.** Rotate/reflect coordinates so its TP endpoint is v=(0,0), its
mate w=(1,0), its selected partner in the TP column is (-1,0), and the
other site of the target BP column is (2,0), which is blank. These axial
positions follow because the matching edge leaves both disjoint parallel
strips transversely.

The TP endpoint needs at least one occupied horizontal neighbor. The BP
endpoint has one occupied mate above and a blank below, so BOTH horizontal
neighbors must be occupied. Choose a side where v has an occupied neighbor
x. It cannot be T: it would already see v and also the occupied neighbor y
of w on that side. Nor can y be T, because it sees w and x. Therefore x,y
are P, and {v,w,x,y} is the required square. ∎

Choose one such square for every safe parallel edge. At most two chosen
edges can have the same square: the actual matching edges are disjoint,
and a square has four vertices. Hence r_parallel<=2 times the number of
chosen distinct squares. This is a witness multiplicity bound, not another
resource allocation. For aligned horizontal bands these squares cross a
band boundary and need not be aligned capacity-two tiles. In particular,
one must not credit two interval units merely for seeing such a square.
Perpendicular-strip refunds still obey Theorem 1; this square classification
is stated only for parallel strips.

## 5. A frozen split receiver outside the former closure condition

The permanent [coordinate fixture](../develop/fixtures/frozen_occupied_strip_export_refund.json)
is an 8-by-10 feasible board with these matching edges:

    (3,4)--(4,4), (3,5)--(3,6), (4,5)--(5,5).

Its six mandatory supports are (2,4),(4,3),(2,6),(3,7),(5,6),(6,5).
Add the following feasible selections, giving thirteen T in total:

    (2,2),(2,8),(3,2),(4,1),(4,8),(5,2),(5,8).

The original P-component is the square at rows3,4/columns4,5, with one
outward arm to the east and one to the south. Each endpoint has occupied
degree three. Its two arm tips (3,6),(5,5) freeze using their two T supports;
then (3,4),(4,4) freeze using a T and a retained central neighbor; finally
the other two central endpoints freeze. The fixture stores the complete
three-layer certificate. Added selections are disjoint and preserve each
mandatory support's unique occupied neighbor, as checked directly by the
coordinate lists.

Take I_1=rows2,3 times columns0..9 and I_2=rows4,5 times columns0..9.
Their ends are blank and lengths even, giving Delta=4. The edge
(3,4)--(4,4) exports a TP from I_1 to a BP column in I_2. Every other TP
mate is internal to a strip. Thus h=j=o=0, r=1 and u=0. Direct labels give
K=5, so

    S_U=5,     D_U=5,     rho_U=0.

The whole original receiver lies in U but intersects both strips. It is
contained in neither strip, so the former per-strip receiver-closure
hypothesis fails. The new joint criterion applies, with five units in the
exact forest budget (or four in the conservative boundary budget).
A finite independent column DP confirms the supplied T-completion on this
fixed footprint; neither the general theorem nor the family proof uses
finite optimality as a substitute for a geometric argument.

For every q>=1 place copies at horizontal shifts (0,12i). Their occupied
supports end two or more blank columns before the next copy, so no new
occupied adjacency arises. In an 8-by-(12q-2) rectangle they have 13q T,
3q M, 6q frozen endpoints, 2q disjoint selected strips, q safe exports,
K=5q, Delta=4q, u=h=j=o=0, and S_U=5q. This follows by separation and
summing the explicit per-copy labels for ALL q.

For a nonvacuous source-compensation instance, place five complete positive
elbow(6,4) components and one split-receiver fixture in each 12-by-112 block,
using horizontal offsets 0,20,40,60,80 for the elbows and 100 for the fixture.
Each elbow has its established whole-receiver charge +1. Use only the two
strips in each split fixture. Their raw receiver charge is zero, and each
contributes five endpoint-free deficit units. All blocks have even offsets,
separated occupied data and the original freezing certificates. Consequently
K=5q pays the five q outside positive charges under (7), with the outside
endpoint-free deficit retained once. The enclosing board can have width
112q-2. This is an all-q coefficient-one sufficient family, not universal
coverage or a claim of extremal selected sets.

## 6. Sharp frozen obstructions to omitting the other deductions

**TP--TP.** On a 4-by-3 board take P=(1,1),(2,1), matched together, and

    T={(0,1),(1,2),(2,0),(3,1)}.

Both endpoints freeze immediately. Let the upper strip read columns0,1,2,
and the lower strip read2,1,0. Both have delta=1. The single TP-to-TP edge
gives h=1, K=2,u=j=o=0, so S_U=1=Delta-1. Omitting its unit debit would
claim two units where there is one.

For every q>=1, take 2q translates by (0,3i). The resulting 4-by-6q board
is feasible and fully frozen, with 8q T,2q M and true margin2q. Its four q
strips have total Delta=4q and h=2q, giving equality S_U=2q. Individual
strips have odd length and can cut tiles, but their union is the entire
original tile-closed board. Thus the failure persists in a physical global
ledger and cannot be repaired by counting both endpoints of an edge twice.

**TP--PP.** On a 6-by-4 board put the vertical four-endpoint comb at
(1,1),(2,1),(3,1),(4,1), with mates1--2 and3--4, and select

    (0,1),(1,2),(2,0),(3,2),(4,0),(5,1).

The end endpoints freeze first and retain the inner mates; the two-step
induction freezes the whole comb. Take the upper strip in rows0,1,
columns0..2, and the middle strip in rows2,3, reading columns3,2,1,0.
They have Delta=2. The upper TP endpoint is matched to one endpoint of the
middle PP column. Here j=1,h=o=u=0,K=2 and S_U=3/2: the half-unit deduction
is exact. Adding the lower strip rows4,5 reading columns2,1,0 gives Delta=3,
j=2 and S_U=2. A PP column has two endpoints, not two compensating BP
columns, and cannot refund either TP as though it were BP. These are sharp
REGIONAL controls; the whole board's remaining blank cells are retained in
its positive physical margin.

**Exterior.** The earlier fully frozen all-width single-strip family has
Delta=1,o=1,h=j=u=0 and S_U=1/2. It continues to show that a mate outside
the whole selected union cannot be refunded without accounting for its region.

Each counterexample rejects a proposed debit-free rule, not coefficient one
or the established 5/6 theorem. They also show why separate rounding of
regional half-units would invent unavailable compensation.

## 7. Verification and formal scope

The saved run passes 922 joint models, including 806 exhaustive two-strip
matchings and 80 mixed-direction region controls. It checks 3,242 individual
strips, 134 safe crossing occurrences, 118 parallel P-square witnesses and
1,798 strict endpoint-freezing events.

The [checker](../develop/check_occupied_strip_export_cancellation.py) reconstructs
actual labels, matching mates, column forests, refund-target injections and
both old and new flux identities. It checks physical raw ledgers only when
the union is an original tile union. The
[receipt](../output/occupied-strip-export-cancellation-validation.json) includes:

- every label/matching configuration in a specified two-strip 4-by-3 frontier,
  with actual transverse matching completions into blank outer rows;
- mixed horizontal/vertical disjoint strip selections in the existing fully
  frozen 28-by-24 board, and its complete original band partition;
- the sharp three debit types, the six-endpoint frozen refund fixture,
  q=1,2,3,4,8,16,32 separated copies and tile-preserving symmetry images;
- five-positive-source-per-refund families and all-q sharp TP--TP controls;
- independently replayed endpoint freezing witnesses and actual P-square
  witnesses for safe parallel exports under single terminality.

The [Lean source](../formal/SubQuorum/OccupiedStripExportCancellation.lean)
and [formal report](../output/occupied-strip-export-cancellation-formal-validation.json)
cover six general/local kernels: actual-mate injection into distinct BP
columns, the finite single-terminal square stencil, the exact joint matching-
edge ledger, corrected and debit-free union bounds, and the original-grid
partition implication. The first two are axiom-free; the arithmetic theorems
use only standard propext and Quot.sound. No sorry, native_decide, added axioms
or warnings occur. The grid-to-column adapter, finite cardinality sums,
column-forest argument, full coordinate freezing and all-q constructions
are written proofs with executable checks, not end-to-end Lean formalizations.
Local memory and actual comm-basename lean/lake process checks precede every
Lean executable invocation.

The [arbitrary tile-cut rotor ledger](ARBITRARY_TILE_CUTS_AND_SIGNED_ROTOR_FLUX.md)
already conserves its own signed rotor transfers; this note classifies the
DIFFERENT boundary terms of the actual M matching and TP/BP/PP column types.
The two identities must not be treated as separate extra resource pools.
The physical source coverage and the general deficit-versus-unused-slack
bound remain open. Submitted manuscripts, public main, PR #3 and shared CI
are unchanged; this research continuation does not operate on correspondence.

Reproduce:

    PYTHONDONTWRITEBYTECODE=1 python3 develop/check_occupied_strip_export_cancellation.py --output output/occupied-strip-export-cancellation-validation.json
    PYTHONDONTWRITEBYTECODE=1 python3 develop/check_occupied_strip_export_formal.py --lean /path/to/lean-4.33.0 --output output/occupied-strip-export-cancellation-formal-validation.json
