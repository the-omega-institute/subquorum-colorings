# Zero-capacity gap barriers and cross-component beta compensation

23 October 2026. Authors: Haobo Ma and Wenlin Zhang.

Full access to the original interval units of maximal endpoint-free gaps
still need not route any compensation in a completely frozen configuration.
We give a two-parameter, uniquely matched family with one alpha and two beta
strands, where the alpha cannot reach either beta or any unmarked interval
through ordinary terminal links and arbitrary-length gap resource access.
The obstruction is already certified by the empty separator.

The new mechanism is an endpoint-free corridor containing only BT columns.
Its interval capacity is exactly zero; length does not make it a donor.
A virtual opposite-label pairing across such a corridor transfers one
existing whole-beta credit between components without creating any interval
credit. One such pairing pays the displayed family. It changes accounting
strands, not the actual matching, selections or freezing procedure.

This is an obstruction to completeness of the previous access model and a
new geometric pairing witness. The exact flow and cancellation theorems are
the earlier theorems applied to the enlarged witnessed link relation.
No universal grid inequality or improvement of the universal 5/6 is claimed.

## 1. A zero-capacity corridor is not a resource

Use the matching-closed aligned packet, original strands and original
BB--TT interval units of ENDPOINT_FREE_GAP_COMPENSATION.md. A maximal
P-free gap G has raw capacity L_G = #BB - #TT. If L_G=0, its BB--TT forest
has no component, hence it contains no BB or TT. Every column is BT.
Conversely an all-BT gap has L_G=0. In particular its exact weighted
surplus is zero:

    |G|/2 - |T intersect G| = 0.                           (1)

This concerns raw capacity, before boundary reservations. A gap with raw
capacity one that loses its unit to a boundary mark is a different case.

If G is bounded at both ends by columns containing exactly one free
terminal each, and their labels are opposite TP/BP, record a witnessed
virtual link between those terminals. The witness consists of G and its
two boundary terminals. It can join different physical rows of its band.
A PP boundary column or an internal endpoint of a strand supplies no such
free terminal; no cut or new pairing at an internal PP node is assumed.

There is at most one such candidate link per gap. Distinct maximal gaps
are disjoint in their interiors. They may meet the same boundary terminal,
so chosen links must still be a terminal matching. An all-BT corridor
supplies no interval unit to any other payment, whether or not its virtual
link is selected.

## 2. Exact conditional compensation with corridor pairings

Add the witnessed links of Section 1 to the ordinary TP--BP adjacency
links. Keep the same original strand pairs, whole-beta resources and gap
interval accesses. Apply the integral directed-path normal form with unit
capacity at every mixed owner and beta resource and at every original
unmarked interval. Let its maximum value be nu, with initial alpha k,
beta b and unmarked interval set I. Then

    delta = k-nu,  Q = |I|+b-nu,
    S_J-B = Q-delta.                                     (2)

Every integral route packing gives a legal VIRTUAL cancellation and
injective interval payment. In particular, nu=k implies S_J>=B.

Proof. The abstract normal-form theorem allows any declared opposite-label
terminal links. Its proof uses disjoint original strands, free boundary
terminals and their TP/BP labels, not grid-edge adjacency. Both ordinary
and corridor links meet those hypotheses. Its reconstruction supplies a
terminal matching, so two links cannot consume one terminal and two routes
cannot share a mixed owner. A whole beta has one sink unit, regardless of
its two boundary terminals or how many candidate links approach it.

An interval payment uses one original unmarked BB--TT unit. Section 1's
corridors contain none of those units; no corridor length, selection or
new virtual link creates a resource. In the enlarged cancellation graph
the invariant b_C-alpha_C=b-k is unchanged. If F is its final interval
payment, compensation is b-b_C+|F|. The original physical identity
S_J-B=|I|+b-k therefore gives (2). This is the same invariant and reverse
normalization as the earlier theorem; no new flow theorem is needed. QED.

This applies the abstract theorem with enlarged fixed relations on original
physical terminals and interval identities, extending its earlier physical
adapter. Disjointness concerns strand owners, terminal use and resource units.
The witnesses do not assert physical transport through disjoint grid paths.

The geometric witness is useful for locating a specific cross-component
pairing. It is not a promotion rule, a replacement of the actual matching,
or permission to allocate beta by terminal count. Global use still requires
the original receiver closure and the exact outside-overlap correction
2N_out. Interior packet resources cannot also pay outside demands.

## 3. An arbitrary-length fully frozen barrier

Let W>=6 be even and d>=1. Write D(V)=direct_family(V,4), with its
established selection and actual-matching support lists. Superimpose three
translated copies:

    central: D(W),     displacement (0,0);
    left:    D(W+2),   displacement (-1,-2d-5);
    right:   D(W+2),   displacement (-1, 2d+5).

The central terminal rows are r=5 and r=W+4. Their opposite rows in the
same bands are r*=4 and r*=W+5. In each such band fill the two corridors
as follows, for s=1,...,2d:

    left column 2-2d+s: select row r* if s odd, r if s even;
    right column 7+s:  select row r if s odd, r* if s even.

The first and last selections in each corridor are already the two old
caps. There are exactly 8(d-1) new selections in the four corridors.
Consecutive selections alternate physical rows; all newly inserted
selections are isolated in the final occupied set. The old endpoint
neighbours and all old selections' occupied degrees are unchanged.

The three old endpoint graphs are separated by at least two columns with
no endpoint. They remain disjoint, with their respective unique matchings.
The explicit all-V freezing certificates replay separately: their selections
and actual mates are unchanged and no new event is needed. Thus the union
is feasible, completely frozen and uniquely matched for every W,d.

Translate all columns by 2d+4. Take J to have raw rows 2..W+7 and columns
-2d-4..2d+15. These are complete aligned physical tiles. J contains all
selections, endpoints, actual matching edges and original receiver tiles.
Both end columns in each band are BB singleton interval units, so

    dimensions = (W+6) by (4d+20),
    |T|=8d+31,  |M|=3W+16,  B=W+6,
    S_J-B=(2d+6)W+4d+7 > 0,
    L-B=(2d+6)W+4d+6.                                  (3)

The added selections are inside P-free columns, not vertically beside an
endpoint. They do not change any strand pair or terminal label.

### Exact inventories of the shifted flanks

The central copy has its old alpha=1, beta=0, mixed=5. For a flank use
the old unshifted coordinates of D(V), V=W+2, but its odd row displacement
changes the band phase. Every actual column-3 edge is now also its band's
vertical PP pairing; these form isolated alternating two-edge cycles.

There is one mixed strand, the actual upper horizontal pair
(5,6)--(5,7), now labelled TP/BP. The remaining noncyclic strand is beta:
it starts at (5,5), takes the actual edge to (5,4), follows the alternating
actual/PP vertical chain in column 4 to (V+4,4), and then follows

    lower4 -- lower5 -- upper5 -- upper6 -- lower6 -- lower7,

where lower=V+4, upper=V+3. The edges alternate actual matching and vertical
PP pairing. The final endpoint is (V+4,7). Both free ends are BP in this
phase. This exhausts the remaining edges of D(V), proving beta=1 and
mixed=1 for each flank, with no alpha. Thus the whole inventory is

    alpha=1, beta=2, mixed=7.                            (4)

### Full gap resource access and arbitrary ordinary links still give zero

The central alpha has TP3 in each extreme row. In each row its only
ordinary outgoing links lead to BP4/TP5 and then BP6/TP7. Every reachable
TP tip is therefore one of columns 3,5,7 in those two rows. Its adjacent
P columns and ordinary link candidates are unchanged.

TP5 lies between two P columns. The left gap beside TP3 and right gap
beside TP7 contain exactly 2d BT columns each and no BB--TT unit. Their
raw and unmarked capacities are zero. Full arbitrary-length gap resource
access therefore gives none of the six reachable TP tips any interval.
There is no ordinary terminal link through these all-BT corridors and no
beta among the reachable central owners. No link reaches either flank.

Consequently the full-gap network, with C0 EMPTY and every ordinary link
allowed, has

    nu=0, delta=1, Z empty.                              (5)

This is not a conflict between two users of one unit: it is lack of any
reachable resource. Arbitrarily long gap access by itself is insufficient,
despite both existing whole-beta resources elsewhere in the same packet.
The exact target margin (3) is positive, so (5) refutes completeness of
that routing model, not the target inequality or the grid conjecture.

### One zero-capacity pairing reaches an original beta

In raw coordinates the left flank's lower beta endpoint is

    v=(W+5, 2-2d).

The central alpha's lower free terminal is u=(W+4,3). Their two boundary
columns enclose the left all-BT gap, of length 2d. Section 1 permits the
single witnessed virtual TP--BP link u--v. It joins the one central alpha
to the left whole beta and produces a mixed component. The other beta
remains unused. Hence alpha_C=0, beta_C=1, and

    compensation=1, used interval units=0,
    S_J-B=(L-B)+1.                                      (6)

There is no double use of a beta or interval. This one link is optimal
for total link count: with zero links, (5) gives no compensation; the
displayed one-link cancellation attains full payment. Ordinary links are
not needed in this witness. Its horizontal span is 2d+1 and its endpoints
lie in opposite rows, so the grid distance is 2d+2. A fixed bounded span
for this new pairing would again miss sufficiently long members.

## 4. Reflected PP boundaries block the enlarged link rule too

There is a stronger variant. Reflect the LEFT D(W+2) copy horizontally
by c -> 10-c before its stated translation. Keep the other two copies
and the four corridor fillings unchanged. Feasibility, unique matching,
the replayed freezing certificates, all counts (3), and inventory (4)
are preserved. Reflection does not change the vertical PP band pairing.

At its rightmost endpoint column, the reflected left copy now presents
its original column-3 vertical matching edges. In the odd phase these
are PP columns whose vertical auxiliary edges coincide geometrically
with the actual matching edge. Each is an alternating two-edge cycle.
The unchanged right copy already presents that same type of PP column
at its left side. Thus all FOUR far boundary columns of the central
zero-capacity corridors are PP, with no original free terminal.

The central alpha's reachable TP3,TP5,TP7 tips still have no interval
access. No corridor link of Section 1 can leave them, because the far
end is an internal PP column rather than a single free BP terminal.
Ordinary links remain confined to the two central row chains. Hence
even after allowing EVERY zero-capacity terminal-to-terminal link,

    nu=0, delta=1, Z empty, beta=2.                       (7)

This all-length frozen, uniquely matched example blocks both interval
gap access and the new free-terminal corridor rule. Existing beta credit
does not automatically become reachable through an occupied PP boundary.
The unreflected one-link theorem remains valid; it did not claim general
routing completeness of the enlarged rule.

### Opening an internal PP edge creates a unit of debt

The next tempting continuation is to cut an auxiliary PP pairing and
treat its two newly exposed endpoints as BP ends. That operation needs
an exact correction. For ANY fixed matching-closed packet, remove q
distinct vertical PP auxiliary edges while keeping the actual matching
and all selections. Give each new free end positive BP sign. Before
cutting, the original free-end counts satisfy n_BP-n_TP=2(b-k). Cutting
adds 2q positive free ends and removes no old free end. Thus the resulting
strand counts, and any subsequent opposite-label terminal cancellation,
satisfy

    beta_C-alpha_C=b-k+q,
    S_J-B=|I|+beta_C-alpha_C-q.                           (8)

The physical interval set and surplus have not changed. The cut debt q
is mandatory; it is not an optional loss charged to the chosen virtual
route. This argument covers cuts on paths and cycles and uses no freezing
assumption. The newly labelled BP ends are accounting ends, not a claim
that their physical PP column changed its original label.

In the reflected family choose the left far PP boundary of the lower
corridor. Its actual matching edge and auxiliary edge form one two-edge
cycle. Cutting only its auxiliary edge exposes a NEW beta consisting of
that same actual matching edge. Pair the central lower TP with one of
these new positive ends through the corridor. The apparent inventories
become alpha_C=0, beta_C=2. The two ORIGINAL beta resources are untouched.
Without the q=1 correction one would report |I|+2, exceeding the actual
margin |I|+1 by exactly one. Equation (8) restores the true count. This
virtual operation has supplied no net original-resource compensation.
It is not a counterexample to the grid target; it is an explicit failure
of treating an opened PP pair as a free extra donor.

## 5. Balanced auxiliary rematching pays the reflected family without debt

The reflected obstruction can be paid by a complete auxiliary rematching,
without changing the actual matching or leaving newly opened PP ends free.
This is a further operation beyond the fixed-strand flow model above.

**Auxiliary rematching lemma.** Let A be the original matching of the two
endpoints in every PP column. Let N be another matching on the actual
endpoint set P. Assume N covers every endpoint originally covered by A,
and additionally covers equally many original free TP and BP terminals.
Then all remaining free ends retain their original TP/BP labels, and the
paths of M union N satisfy

    beta_N-alpha_N=b-k,
    S_J-B=|I|+beta_N-alpha_N.                            (9)

In particular alpha_N=0 implies S_J>=B. More generally, an injective
allocation of original interval units to every remaining alpha also
implies that bound. The new auxiliary edges need declared geometric
witnesses; no assertion that such N exists in every frozen grid is made.

Proof. Both M and N are matchings and M covers all endpoints, so their
union is a disjoint union of alternating paths and cycles, retaining
parallel edges when an actual and auxiliary pair coincide. All original
PP endpoints remain matched in N; no new free endpoint has been created.
Exactly equal numbers of the two original terminal signs were removed.
Thus the signed number of remaining free ends is still 2(b-k). Each beta
has two positive ends, each alpha two negative ends, and mixed paths or
cycles contribute zero. This proves the first identity; the original
physical ledger proves the second. Each actual edge belongs to one final
component and interval identities are unchanged. QED.

This lemma gives a conditional ledger, not a flow normal form for optimizing
over auxiliary rematchings. Original strands can split during rematching;
the earlier fixed-strand flow equivalence is not asserted for this larger
optimization problem.

### Explicit two-edge replacement

In the reflected left flank put c=2-2d, a=4, z=5, using raw coordinates.
The two columns c,c-1 in band (a,z) are PP. Remove their two vertical
auxiliary pairs and add the following three auxiliary edges:

    (z,3)--(a,c),
    (z,c)--(z,c-1),
    (a,c-1)--(a,c-2).                                   (10)

The first edge has the upper-left all-BT corridor as its zero-surplus
witness. The other two are horizontal grid edges between occupied
endpoints. The first original free terminal (z,3) is the central alpha's
upper TP. The last (a,c-2) is the reflected left beta's upper BP: it is
the old endpoint (5,5) of D(W+2), after reflection and translation.

The five edges comprising three additions and two removed vertical pairs
form a simple A-alternating path from that TP to that BP. The four internal
PP vertices are distinct and remain covered after replacement. Other
auxiliary pairs are unchanged. Thus N is a matching, covers every old PP
vertex, and covers exactly one additional TP and one additional BP.
Equation (9) applies with no cut debt.

To identify the final strand, start at the central alpha's lower TP and
follow its old actual/auxiliary path to (z,3). The first new edge enters
(a,c), the old boundary PP cycle. Its actual vertical edge leads to
(z,c), whose new horizontal pair enters the adjacent column c-1 at row z.
Follow that column's old actual/auxiliary chain downward and the unchanged
bottom continuation of the left beta. It ends at (W+5,c-4), the old
left beta's lower BP. These are now the two free ends of one mixed strand.

The remaining short upper beta segment from (a,c-1) to (a,c-2) has its
actual edge duplicated by the third new auxiliary edge and becomes a
two-edge cycle. The original right beta and the seven original mixed
strands remain. The resulting inventory is therefore

    alpha_N=0, beta_N=1, mixed_N=8.                      (11)

This consumes one genuine original alpha/beta credit pair, uses no interval
unit, and attains the exact margin (3). There is no claim of minimum edge
replacement cost. All changes are to the auxiliary accounting matching;
the original actual matching and selected set are fixed.

The debt interpretation agrees. Opening the PP cycle and cutting the
adjacent beta path first creates two units of apparent signed credit.
The corridor TP--BP join preserves signed charge. The two subsequent
BP--BP reconnections each remove one unit, repaying both cut units.
The complete replacement has net debt zero. Keeping the opening while
omitting either repayment would give an incorrect ledger.

## 6. Validation and remaining question

The permanent checker covers W in {6,8,12,20}, d=1..24, and both orientations
of the left flank: 192 fully frozen, uniquely matched controls. It independently
checks complete feasibility and freezing, unique matching, isolated new
selections, the original all-width certificates, exact compact-packet
inventory and (3), the empty-separator obstruction with full gap access,
the zero-surplus corridor witness, and full compensation with one virtual
link into a whole original beta in all 96 unreflected cases. The 96 reflected
cases remain blocked even with all zero-capacity links. For each it explicitly
removes one PP auxiliary edge, reconstructs the resulting path components,
and checks the exact one-unit overcount if the cut debt is omitted. It
reconstructs cancellation components and checks the unchanged ledger.
These are controls for the all-length proof, not a substitute for it.

All 96 reflected cases also check the explicit two-edge/three-edge auxiliary
replacement: matching validity, coverage of every original PP vertex,
exactly one original TP and BP newly covered, final inventory (11), the
two free ends of the joined source/donor strand, and the exact physical
ledger. Another 220 selected cut-set controls reconstruct components after
single cuts or nested prefixes of the full PP edge list in four small
models. The single cuts include alpha paths, beta paths and cycles; these
are not an exhaustive enumeration of all cut subsets.

The local Lean source PPCutDebt.lean also verifies the cut correction for
an arbitrary finite strand-rewriting trace. Its operations include opening
an internal path edge, opening an existing cycle, opposite-label joining
and closing, reversal, reordering, lifting and composition. Structural
induction proves that final signed charge is original charge plus exactly
the number of cuts. The corrected packet ledger is invariant, and a concrete
alpha/cycle opening followed by pairing retains the original negative unit.
The extended trace also allows BP--BP joining and closing, each repaying
one unit. It proves exact signed debt under arbitrary finite composition,
the invariant ledger for net-zero debt, and the two-cut/two-repayment
alpha/beta repair trace. Nine named theorems and their individual
ordinary-axiom audits pass locally in Lean 4.33.0. The physical availability
of a chosen PP edge, the grid embedding and freezing are not formalized
by this abstract trace interface.

Run:

    PYTHONDONTWRITEBYTECODE=1 python3 develop/check_zero_capacity_gap_beta_compensation.py --output output/zero-capacity-gap-beta-compensation-validation.json

The earlier endpoint-free gap theorem remains correct under its stated
incidence assumptions; its universal routing completeness was not claimed.
This new obstacle shows that improving its interval access alone will not
establish that missing universal conclusion. The next question is the
enlarged network's joint source/mixed/beta/gap-unit budget, including PP
boundaries that do not supply free terminals and the mandatory debt for
opening their auxiliary edges. The first combined Oracle submission includes
Sections 1--3 and the preceding endpoint-free gap theorem. The reflected
variant and PP-cut correction in Section 4, the auxiliary rematching
lemma/repair in Section 5, and the nine Lean statements were developed
after that submission and are outside that review input. The general grid inequality,
universal 5/6 improvement and triple equality remain open. No new Lean
verification of the geometric construction is claimed.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
