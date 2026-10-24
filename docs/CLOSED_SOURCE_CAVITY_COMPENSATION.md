# Complete-component cavity closure compensates occupied distant bands

19 October 2026. This note proves a source-level compensation theorem that
permits endpoints in every prospective distant rung. It develops the cavity
candidate in completed research task f8af741f and extends it to any number
of enclosed parallel positive sources. It also gives a uniform explicit
family with zero mouth payment whose only negative-comb pair has an occupied
rung. The unrestricted grid bound and arbitrary positive bends remain open.

## 1. Precise setting and the closed region

Use the feasible pair, single-terminal representative and fixed physical
tiling of `COMPONENT_RECEIVERS_AND_SQUARE_FREE_BOUND.md`. Whole endpoint
components have their actual matchings. There are B prescribed positive
long sources, each with corrected whole-receiver charge +1. All other final
receivers are nonpositive; complete straight combs have charge zero. Thus

    Delta=mn/2-|T|-|M|=-B+D_all+E,       E>=0,          (1)

where D_all is the sum of deficits 2-t_Q over all original physical tiles
without endpoints. No individual endpoint tile is a donor.

Fix one source of even width w>=8 and depth h>=1. In its relative coordinates
the chamber is {0,1} x {0,...,w-1}, arms are columns 0,w-1 through row
r=2h+2, and physical tiles begin at even rows and odd columns. This is
the positive alignment in `LONG_BENT_BANDS_AND_TERMINAL_STRIP_COMPENSATION.md`.
Its closed inner cavity is the physical rectangle

    C={2,...,r+1} x {1,...,w-2}.                       (2)

The root source has no endpoints in C. Require that every endpoint
component meeting C, without exception for unlisted components, is contained
in C and is either a complete straight
comb or one of n additional prescribed positive long sources with horizontal
chambers. The enclosed sources may open up or down; positive physical
alignment, matching and supports are retained. Precisely, in the root's
relative frame a down-opening chamber begins at an even row and an even
column. Translations have even coordinates. Up-opening sources are images
under row reflections row -> odd_constant-row; these preserve both row
pairings. Column reflections column -> odd_constant-column also preserve
both column partitions as sets of pairs. A one-column translation or an
even-constant row reflection is not an allowed change of source phase.
Horizontal and vertical combs
may occur together, with arbitrary lengths and relative positions subject
to feasibility. No endpoint-free internal band or pairing hypothesis is used.

This is a genuine closure assumption. A component touching C and escaping
through its open lower side is excluded. Sources with perpendicular chambers
and other square-bearing components inside C are not covered by the exact
phase count below.

## 2. The whole-component two-partition identity

Let D_C be the original no-endpoint physical deficit in C. Delete its two
extreme columns and partition what remains into squares shifted horizontally
by one vertex. Let D'_C be the no-endpoint deficit in this auxiliary partition.
The shifted squares are only a counting device, not additional physical donors.

**Closed-cavity identity.** Under Section 1,

    D_C=2+2n+D'_C >= 2(n+1).                           (3)

Proof. On either extreme column of C, exactly the h inside supports in
rows 3,5,...,r-1 are selected. At even row 2 the next inside support in
row 3 is already adjacent to its arm endpoint; any occupied site in row 2
on this column would give that selected support a second occupied neighbor.
At every even row 4,...,r use the preceding inside support in row q-1
instead. This excludes both selections and endpoints, including row r.
At row r+1 the axial support in the adjacent arm column already sees the
tip in row r, and again excludes any occupied site. These cases exhaust
the column, including the first row and final two rows.
Deleting the two columns therefore removes 2h selections and no endpoints.

The original partition has (h+1)(w-2)/2 tiles; the shifted partition has
(h+1)(w-4)/2 squares. Their counts differ by h+1. Write t,p for selected
and endpoint counts in C, and define raw excess e(Q)=t_Q+p_Q/2-2 on an
endpoint-containing square. Let E_C,E'_C be sums of these raw excesses in
the two partitions. Counting vertices gives

    D_C=2N-t-p/2+E_C,
    D'_C=2N'-(t-2h)-p/2+E'_C,
    D_C-D'_C=2+E_C-E'_C.                              (4)

Component closure and absence of boundary endpoints ensure that the entire
receiver of every enclosed component is present in both partitions. Indeed,
C is a union of complete physical squares and retains the same complete
row pairs after trimming. Every remaining endpoint lies in one of the
shifted column pairs partitioning the trimmed interval, so its entire
shifted square lies in C. A support outside C can still force a label
inside C; containment of such a support is not needed for this argument.
In particular, trimming cannot leave only one raw end of a comb.

Each complete comb has whole raw sum zero in either tiling. An aligned comb
has only (p,t)=(2,1) tiles. A misaligned comb has those middle tiles and two
singleton ends (1,1),(1,2), whose raw halves cancel. Either transverse row
choice has the same count. This uses the complete-comb receiver proof, with
the horizontally shifted tiling in place of the original tiling.

Each enclosed parallel positive source has E=+1 in the original tiling and
E'=-1 in the shifted tiling. To check the second assertion, the chamber now
fits whole four-endpoint squares; nonterminal arm tiles have (2,1); and
each of its two last arm squares has (1,1), not (1,2). The axial support is
in the shifted last square, while its other inside sites are forced blank
by the preceding inside and axial supports. The outer side support lies in
the other column phase. Thus each tip contributes -1/2. The phase-preserving
vertical reflection specified in Section 1 preserves these counts.
In source-relative coordinates the shifted label table is: chamber
squares (p,t)=(4,0), nonterminal arm squares (2,1), tip squares (1,1).
For a left tip square {r,r+1} x {0,1}, vertices (r,0),(r+1,0) are the
endpoint and axial support. Corner (r,1) is blank because the inside
support (r-1,1) already sees its endpoint; (r+1,1) is blank because the
axial support already sees the tip. The right tip is symmetric. The same
preceding/next inside-support test fixes the nonterminal corners. These
tests apply even if a forcing support is outside the cavity. Thus all
labels contributing to the shifted count are fixed in retaining completions.

Tile ownership prevents different endpoint components sharing a square.
Consequently E_C=n and E'_C=-n. Substitute in (4). Every shifted square
contains at most two selections, so D'_C>=0. This proves (3). QED.

For n=0, this proves the previously proposed complete-comb cavity identity.
The 2n term extends it: an enclosed positive source supplies a favorable
phase difference rather than being an unaccounted obstruction.

## 3. Global consequences and unique allocation

If all B sources consist of the root and n=B-1 enclosed sources in one
closed cavity, (1),(3) immediately give the strict bound

    |T|+|M| <= mn/2-B.                                (5)

The same conclusion holds for disjoint closed root cavities whose root-plus-
enclosed source groups partition all B sources. Each cavity gives twice
the number of sources it accounts for, and each original donor is used once.

There is also a useful overlap version. For a family of closed cavities C_j
write k_j=1+n_j and K=sum_j k_j. Suppose every positive-deficit original
no-endpoint tile belongs to at most c cavities, for an integer c>=1. Then

    2K <= sum_j D_(C_j) <= c D_all,
    c Delta >= 2K-cB+cE.                             (6)

The second inequality counts the actual incidence of each original donor.
Endpoint tiles and shifted squares provide no extra capacity. Hence
2K>=cB suffices for coefficient one. In particular, if every source occurs
as a root or enclosed source at least once and cavity multiplicity is at
most two, K>=B and the theorem follows. Counting a source in several valid
cavity identities is allowed; every resulting physical claim is still
limited by the donor incidence inequality. No allocation is inferred from
source counts alone.

Equivalently, arbitrary nonnegative cavity weights lambda_j are valid when
sum_(j:Q in C_j)lambda_j<=1 on every positive donor and
sum_j 2lambda_j k_j>=B. Uniform completion statements require the incidence
condition on all potential positive donors, or a uniform proof that each
exempted tile remains deficit zero. This is a single use of (1), not an
addition of the original mouth and doubled-averaging ledgers.

For an initial-pair formulation, impose closure using the prescribed complete
frozen sources and combs initially. Each normalization step promotes an
existing endpoint to a selection and deletes its matching mate from the
endpoint set; it creates no endpoint and retains all old selections.
Every endpoint in C is frozen, so it
cannot be promoted, and no exterior endpoint can be promoted into C. Original
selections remain selected. Thus all labels in C, its closed components and
the two-partition hypotheses persist. Alternatively impose the hypotheses
directly at the fixed terminal representative. An arbitrary unprescribed
component crossing C is not covered by this preservation argument.

Relative to the universal |T|+(5/6)|M|<=mn/2, (5) removes the matching loss
and adds a B-unit strict margin on the stated closed class. Equation (6)
gives coefficient one on the covered overlapping class. Neither is a new
universal coefficient or a proof of the grid triple equality.

## 4. An explicit zero-mouth family whose only pair rung is occupied

For every even w>=32 and h>=3, use a root source with chamber origin (2,3)
in actual even/even physical coordinates, width w and depth h. Put y=2h+4.
The source mouth has rows y,y+1 and columns 4,...,w+1; its cavity is

    C={4,...,y+1} x {4,...,w+1}.

Add these complete consecutive-matching combs and their axial supports:

| Comb | Endpoint path | Alternating side support |
| --- | --- | --- |
| L | column 9, rows 7,...,y | column 8 at odd rows, 10 at even rows |
| R | column 22, rows 7,...,y | column 23 at odd rows, 21 at even rows |
| H | row 6, columns 14,...,17 | row 5 at even columns, 7 at odd columns |

The axial supports are (6,9),(y+1,9),(6,22),(y+1,22), and (6,13),(6,18).
All three complete combs lie in C. The vertical pair has upper saturated
and lower sparse singleton tiles. Their sparse ends lie in the source mouth
and saturated ends outside it, so F=-2. The horizontal comb contributes zero.

Add this explicit selection pattern in the mouth, retaining all supports:

- select both rows at columns 5,7 and every even column 24,...,w;
- in row y select columns 10,12,13,15,16,18,19,21;
- in row y+1 select columns 11,14,17,20.

The two axial supports in row y+1 at columns 9,22 are already present.
Every physical no-endpoint mouth tile has exactly two selections. The two
endpoint mouth tiles are sparse singleton tiles. Thus

    D_mouth=0, F=-2, A=D'=D_single=0,
    q_mouth=max(0,2B+F)=0.                           (7)

Both old structural mouth certificates are therefore zero. The only pair
of parallel negative combs is L,R. Reflecting vertically puts them in the
remote-rung normal form, but their saturated-tip rung is the image of

    {6,7} x {10,...,21},

which contains all endpoints of H. It fails the endpoint-free rung condition.
There is no second horizontal comb to provide another pair. This shows
that the saturated-tip endpoint-free pair criterion does not cover this
family; its sufficiency is unaffected. The lower sparse-tip mouth corridor
is not the saturated-tip resource required by that lemma. This does not
refute the coefficient-one target. The closed-cavity identity
applies and yields D_C=2+D'_C and Delta>=1.

For a general feasibility proof, all vertical comb endpoints are at least
six columns from source arms and at least four rows below its chamber.
The horizontal comb is three rows below the chamber, whose supports are
only at its outer columns; its upper supports in row 5 see no chamber
endpoint. Its axial supports in columns 13,18 are four columns from the
two vertical comb paths; closest other contacts are diagonal. Its lower
supports occur in columns 15,17 and are separated from the vertical comb
supports in columns 8,23. Each retained support has exactly its intended
endpoint as occupied neighbor. Distinct endpoint components do not join.

At the mouth, the vertical pairs in columns 5,7 and 24,...,w have only
their partners as occupied neighbors. The row-y pairs 12,13;15,16;18,19
are similarly isolated; the row-(y+1) selections 11,14,17,20 are isolated.
The row-y selections 10,21 see only their neighboring comb endpoints.
The axial supports at (y+1,9),(y+1,22) see only their endpoints. Required
supports in row y-1 occur in columns 4,8,23,w+1 and the continuing comb
endpoints are at 9,22; none is adjacent to a new selection above its row.
Since y>=10, the mouth pattern is separated from H and its supports.
All these checks are uniform in w,h; extending w only repeats isolated
vertical pairs on the right. The construction is not justified by the
finite strip optimizer.

## 5. An arbitrary-source nested family

For every a>=1, choose even extra width e>=0 and extra depth d>=0. Put
w=16a+32+e, h=4a+2+d. For i=0,...,a-1 place source i at chamber origin
(2+8i,3+8i), width w-16i and depth h-4i. All sources have the same tip row
y=2h+4. Every nonroot source lies wholly in the root cavity.

For each i add vertical combs in columns 6+8i and w-1-8i with endpoint
rows 7+8i,...,y. Their inward side supports occur at odd rows, so their
upper ends are saturated and their lower ends sparse. Add a horizontal
comb in row 6+8i with endpoint columns 10+8i,...,w-5-8i, and supports
above on even columns and below on odd columns. Include every axial support.
The total is a sources and 3a complete combs. All foreign endpoint components
are contained in the root cavity, F=-2a, and (3) gives

    D_C=2a+D'_C,       Delta>=a.                      (8)

Source chambers are separated by eight rows and nested arm columns by eight.
The only endpoint separation of three within the prescribed pieces occurs
between a source arm and its neighboring vertical comb, or a source chamber
and its horizontal comb. In the arm interface, the source's inside support
and comb's inward support are three columns apart on odd rows; on even rows
their outward supports are also three apart. Closest cross-row supports are
diagonal. In the chamber interface there is no source support below an
interior chamber vertex, so the potential facing-support adjacency does not
occur. Each horizontal comb is four columns from its two associated vertical
combs and four rows above the next source chamber. Other prescribed pieces
have endpoint distance at least four, which separates one-step supports.
For completeness the following bounds exhaust interfaces between pieces
with different indices. Distances refer to endpoint vertices before adding
their one-step supports; the two exceptional distance-three interfaces
are treated in the preceding paragraph.

| Interface | Uniform bound or exceptional case |
| --- | --- |
| Source i, source j, i!=j | Chambers have row distance at least seven; corresponding arms have column distance at least eight. An earlier arm is at least eight columns from a later chamber, and later arms begin at least nine rows below the earlier chamber. |
| Vertical comb i, source j!=i | For j=i+1 the nearest foreign arm has column distance five; farther arms have distance at least eleven. For j<=i the chamber is at least four rows above the comb's first endpoint; for j>i its column interval is at least five columns away. |
| Horizontal comb i, source j!=i | The next chamber is four rows below and earlier chambers are at least eleven rows above. Arms with j<=i are at least seven columns outside the comb interval; later arms start at least six rows below it. |
| Two vertical combs | Distinct lanes on the same side differ by at least eight columns; opposite-side lanes differ by at least 41+e columns. |
| Two horizontal combs | Distinct rows differ by at least eight. |
| Vertical comb i, horizontal comb j | For j>=i the horizontal endpoint intervals are at least four columns away; for j<i the horizontal row is at least nine rows above the vertical path. |

At endpoint distance at least four, supports of different pieces are at
distance at least two and cannot be adjacent; no support sees a foreign
endpoint. Within a piece the prescribed alternating pattern supplies
exactly its own endpoint as each support's occupied neighbor. The
distance-three exceptions have no facing supports, as checked above.
Adjacent endpoints cannot join different pieces. Diagonal endpoints in a
shared physical square would also have distance two, excluded here.
All supplied matching edges are internal to their prescribed pieces.
The endpoint formulas place every nonroot piece in rows 4,...,y+1 and
columns 4,...,w+1; the supplied axial/side supports fit in the ambient
rectangle with rows 0,...,y+3 and columns 0,...,w+7. Source translations
have coordinates (8i,8i), so all retain the exact positive phase.
These uniform margins prove feasibility and distinct complete components
for every a,e,d. Sources and combs remain frozen under feasible completions.
No subset of the nested cavity donors is charged separately without applying
the explicit incidence rule in Section 3.

## 6. Evidence and remaining work

The later `MIXED_DIRECTION_CAVITY_COMPENSATION.md` removes the parallel
restriction for fully enclosed prescribed positive sources. Its exact
identity retains an additional nonnegative phase slack; the parallel
identity (3) above remains exact with zero such slack.

`develop/check_closed_source_cavities.py` checks 48 physical configurations
and eight symmetries, including 16 explicit zero-mouth/occupied-rung instances,
16 arbitrary-depth/width nested instances and 16 filled nested completions.
It recomputes feasibility, terminality, freezing, both partitions, complete
component ownership, every component's raw excess, and the original ledger.
The explicit mouth selection is independently checked against the existing
strip optimizer. Finite checks test the written quantifiers above.

Scoped formal statements in `formal/SubQuorum/ClosedSourceCavities.lean`
cover complete-component phase sums, the conditional cavity partition,
finite donor multiplicity and the resulting multiplicity-two compensation.
Full geometry, closure preservation and the coordinate constructions remain
written proofs. The control receipt and formal audit are separate evidence.

This removes endpoint-free rung existence as a requirement on a nonempty
class missed by the previous mouth and rung certificates. Complete-component
closure remains essential: arbitrary components escaping a cavity, perpendicular
enclosed sources, overlapping cavities with insufficient physical capacity,
and arbitrary positive bent receivers are not settled. A general closure or
routing theorem and the universal grid/triple equality remain open.
