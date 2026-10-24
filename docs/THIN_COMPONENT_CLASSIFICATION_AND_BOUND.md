# Arbitrary thin components: classification and all-alignment coefficient one

19 October 2026. Submitted manuscripts are unchanged. A thin endpoint component
is contained in two consecutive rows or in two consecutive columns. Its shape
need not be rectangular, its matching can initially have either direction, and
different components can have different orientations. This note proves a general
classification after bundle normalization and its original whole-receiver budget.
Finite controls are auxiliary, not the proof of the classification or bound.

## 1. Hypotheses and promotion convention

Let (T,M) be a feasible pair on a finite rectangular grid. Let P=V(M) and
A=T union P, with T disjoint from P and each selected vertex having at most
one neighbor in A. Coordinates outside the grid are blank. A promotion bundle
chooses one endpoint of each of some matching edges, promotes those endpoints
to T and makes their mates blank. Feasibility is tested simultaneously. The
occupied set only shrinks and |T|+|M| is preserved. Bundle terminality means
there is no nonempty feasible bundle; it implies occupied degree at least three
at every endpoint. Completeness always refers to a whole component of G[P].

The bipartite completeness theorem in BIPARTITE_PROMOTION_COMPLETENESS.md
supplies finite bundle normalization: repeatedly take a nonempty greatest
one-color bundle until both color cores are empty. Each step deletes at least
one matching edge, so the process terminates and its terminal pair admits no
mixed bundle either. No endpoint is added and endpoint components cannot merge.

## 2. Matching-closed maximal chambers can be reduced

Work with a complete component supported in rows 0 and 1. Its occupied columns
are consecutive and nonempty. Call a maximal consecutive run of columns
containing both endpoint rows a chamber. A chamber of width w>=2 is a full
2-by-w rectangle. Suppose all matching mates of its vertices stay in it.

**Chamber reduction lemma.** Such a chamber admits a feasible bundle on its own
matching edges, removing all but at most one of those edges. This holds with
lateral endpoint attachments belonging to the rest of the complete component.

Proof. No perpendicular neighbor of the chamber can be P: that would lie in
the same complete component outside its two supporting rows. Hence perpendicular
occupied neighbors are selected supports. Their indicators tau_r(j) satisfy
tau_r(j)+tau_r(j+1)<=1. At either lateral boundary, at most one of the two
sites is occupied. Indeed, if both were P, the chamber would not be maximal;
if at least one were T, it would see its core endpoint and the other occupied
lateral site, violating feasibility. This also covers a physical grid boundary.

Call a corner doubly supported when both its exterior neighbors are occupied,
allowing a lateral neighbor to be P. At most one such corner occurs per end.
Its lateral occupied neighbor forces the other lateral site blank. These are
exactly the exterior facts used in Sections 2--4 of
PURE_TWO_ROW_COMPONENT_REDUCTION.md; the word selected for a lateral contact
there can be replaced by occupied throughout its construction. For precision,
the construction and checks are recalled here.

The actual internal perfect matching decomposes uniquely into one-column V
blocks and two-column HH blocks. If all doubly supported corners have the same
checkerboard color, promote the other color throughout. Every promoted vertex
then has no retained core neighbor and at most one exterior occupied neighbor.

Otherwise the two opposite-end doubled corners have different colors. Promote
color C avoiding the left corner, and color D=1-C avoiding the right. For block
i=[a_i,b_i], let L_i be the perpendicular support at the C-colored vertex in
column a_i-1, or zero at the left end. Let R_i be the perpendicular support
at the D-colored vertex in column b_i+1, or zero at the right end. An existing
end guard is opposite the doubled corner and has blank lateral site. Consecutive
guard sites are adjacent in their exterior row, so R_i+L_(i+1)<=1. The first
block with R_i=0 has L_i=0, since the first L is zero and every preceding R
is one. Such a block exists because the last R is zero.

For a V switch block, retain its edge. Promote C on blocks to its left and D
on blocks to its right. Only the two outside guards can see retained core P;
each sees one and has no exterior occupied neighbor. Other promoted vertices
have no retained core neighbor and at most one exterior occupied neighbor.

For an HH switch block [a,a+1], retain the row-q edge whose endpoints have
colors D,C from left to right. The outside promoted guards are in row q. In
the other row the two perpendicular supports cannot both be selected; promote
an endpoint with blank perpendicular support and delete its horizontal mate.
It sees exactly its retained vertical neighbor. Its outer horizontal neighbor
is blank, and its lateral exterior site, if present, is blank because the
doubly supported corner at that end is in row q. Both guards again see one
retained P and no exterior occupied neighbor. All other checks are as for V.

Thus the construction promotes w or w-1 vertices and leaves at most one edge.
Original selected vertices remain feasible because A only shrinks. Exterior
P contacts are counted as occupied in the promoted-vertex checks and remain
unchanged. This proves the claimed generalization. QED.

## 3. Classify every bundle-terminal thin component

**Classification theorem.** A complete bundle-terminal endpoint component
supported in two rows is either a straight even comb, or, after translation
and reflections, has the following form:

    H=({0,1} x {0,...,w-1})
      union {(0,-j):1<=j<=L}
      union {(q,w+j-1):1<=j<=R},

where w>=3, q=w mod 2, and L,R are positive odd integers. Its matching is
unique and horizontal. Its forced selected supports are listed in Section 4;
additional selected supports may occur along chamber interiors. In particular
one must allow occupied degree four, not just the six-support baseline.

Proof. First exclude an isolated full column with any attachment. Normalize
the column to 0 and a left attachment to (0,-1). The site (1,-1), not P,
touches that attachment and (1,0), so cannot be T either. Terminality at
(0,-1) then forces (-1,-1) to be T. This selected support forces (-1,0)
blank. Terminality at (0,0) now requires (0,1) occupied, and terminality at
(1,0) requires (1,1) occupied. Since these two sites are adjacent and each
touches a core P, neither can be T. Both are P, contradicting the isolated
full column. Reflections cover every attachment direction. A component
consisting solely of that full column is just the vertical even comb.
Every other chamber consequently has width at least two.

Between consecutive chambers, a run of single-P columns has one fixed row:
without a full column a row change would disconnect the component. The absent
partner-row site at either end touches the path endpoint and the adjacent
opposite-row chamber corner, so is blank. Each path endpoint is terminal
and hence has a selected support on the exterior side of the two-row band.
At each subsequent path position terminality requires a perpendicular support;
consecutive supports cannot be on the same side. Starting from the forced
first support therefore determines exactly one at each position, alternating
sides. Both ends require the exterior side, so every bridge has odd length.
The same propagation applies to an outer tail from its chamber outward; its
tip additionally needs an axial selected support.

A matching on an odd bridge has exactly one exit into its neighboring chambers.
Indeed there is at most one at each end, and after deleting exit endpoints
the path's remaining order must be even. An odd path therefore has one, rather
than zero or two, exits. Similarly an outer tail has an exit precisely when
its length is odd. Every chamber has even order, so its number of matching
exits is even and at most two. Zero exits is forbidden by the chamber reduction
lemma and bundle terminality. Thus every chamber has exactly two exits.

If there are c>=1 chambers, their c-1 bridges supply exactly c-1 matching
exits in total: each crossing edge counts at its one incident chamber. The two
outer tails supply at most two. Consequently

    2c <= (c-1)+2 = c+1,

so c=1. Both tails must be present and odd. This is a finite incidence count
for arbitrary c, not an enumerated cutoff. If there is no chamber, connectivity
makes the component a straight horizontal even path, whose supports are the
usual terminal comb pattern.

Normalize the left tail row to 0. Removing the two outward-matched chamber
corners must leave equal numbers of both checkerboard colors. The two removed
corners therefore have opposite colors, forcing the right tail row q=w mod 2.
The remaining matching is forced: bottom column 0 must match horizontally to
column 1; the unmatched top vertex in column 1 must match to column 2; continue
alternating rows. The two odd tails have their forced internal path matchings.
For w=2 the two opposite-row corner supports are adjacent selected vertices,
each already touching P, impossible. Hence w>=3. QED.

## 4. Forced supports, optional supports and freezing

Put out(0)=-1 and out(1)=2. The forced selected supports are:

- At left-tail position (0,-j): (-1,-j) for odd j, (1,-j) for even j;
  also the axial support (0,-L-1).
- At right-tail position (q,w+j-1): (out(q),w+j-1) for odd j and
  (1-q,w+j-1) for even j; also the axial support (q,w+R).
- The opposite-row chamber corners have supports (2,0) and
  (out(1-q),w-1).

These labels follow from the alternating argument above and terminality of
the corner with only two endpoint neighbors. At every tail position the
other perpendicular support is blank because it neighbors a forced support
at the next path position, or touches two P at its chamber end. The axial
tip support forces its adjacent perpendicular outer sites blank. The other
chamber corners' exterior sites are blank next to the first tail supports.

All additional selected neighbors of H therefore lie in these two lists:

| Width | North row -1 | South row 2 |
| --- | --- | --- |
| even w | columns 1,...,w-2 | columns 2,...,w-3 |
| odd w | columns 1,...,w-3 | columns 2,...,w-2 |

Each row is an independent set of selected sites. The interval lengths are
even: w-2 and w-4 for even w, and w-3 on each row for odd w. Pair consecutive
sites in each interval. Each pair contributes at most one T, so the total
number k of optional selected supports satisfies

    0<=k<=w-3.                                            (1)

This bound is attainable by choosing alternating sites in each interval.
These optional supports have one P neighbor, and the lists exclude all sites
adjacent to the forced supports. Any independent selection from the lists
therefore gives a feasible local completion with the forced supports.

For completeness the classified patterns are fully frozen even without the
optional supports. An odd tail tip freezes using its two selected supports.
Proceed inward through every second tail vertex: each has its perpendicular
T and the retained mate of the previous frozen vertex. This freezes the
first tail vertex at its chamber end. At the left end, that frozen vertex
retains its chamber mate (0,0); the opposite corner (1,0) freezes using it
and its southern support. The two-step zigzag recurrence of
FROZEN_TWO_ROW_CAPPED_LADDERS.md then freezes every odd-color chamber endpoint.
The analogous right wave freezes every even-color chamber endpoint. The
right wave exists regardless of the two tail lengths; it is the reflected
unit-tail chamber calculation after the inward tail waves.

Finally the newly frozen chamber corner retains the first tail vertex, so
the second tail vertex freezes using that neighbor and its perpendicular T.
Continue outward through the even positions of each tail. Together these
acyclic inward, chamber and outward waves exhaust H. Optional selected supports
only strengthen the witnesses. No exterior symmetry or equal-tail assumption
is used. This proves the converse freezing assertion in arbitrary feasible
exteriors preserving the component and displayed supports.

## 5. Original receiver budget in every alignment

Now assume an even-by-even ambient rectangle, with its fixed aligned 2-by-2
tiles. Let R_H be exactly the tiles containing endpoints of H, and let u,v be
the upper-left chamber coordinate parities. The terminal ownership theorem
and original saturated-transfer cancellation give

    rho(R_H)=T_R+|H|/2-2|R_H|.                            (2)

Every T in R_H touches an endpoint in that tile, as proved in
ALL_ALIGNMENT_SINGLE_SQUARE_BOUND.md, Section 1. Hence the forced/optional
support list is exhaustive for receiver counts, even in arbitrary feasible
exteriors. Other components cannot supply unrelated receiver T.

Write N=(L+R-2)/2. Extending either odd tail by two changes the receiver counts by

    Delta |R_H|=1, Delta T_R=1, Delta |H|=2.               (3)

Here is a direct all-length geometric proof. The two new P positions on the
tail add one tile in that tail's occupied row band. That tile lies beyond
the old component's column range, so no other endpoint already occupies it.
If the band contains both chamber rows (u=0), exactly the new perpendicular
support on the inside row lies in the receiver. If the chamber rows split
between two tile bands (u=1), exactly the new exterior perpendicular support
lies in the tail's band; the inside support is in the other band beyond all
its endpoints. For an odd old tail length, the new even-position support is
at least two columns beyond the chamber and cannot enter a chamber receiver
tile in the other band. Other supports and the other tail are separated by
the unchanged chamber. The old axial support is replaced by P. Its membership
indicator e in the old receiver equals the new axial support's membership
in the new receiver, since translation by two preserves that end phase.
Thus the selected count changes by -e+e+1=1. Reflection covers the right tail.
This is a pattern count, not a feasible surgery in a fixed exterior.

For unit tails L=R=1, count tile columns by floor((column+v)/2). When u=0 the
core occupies one tile row, all optional supports lie outside R_H, and

    |R_H|=floor(w/2)+2             if v=0,
    |R_H|=floor((w+1)/2)+1         if v=1,
    T_R=2|R_H|-w-2, |H|=2w+2.

The T count can also be read directly: for even w, both axial supports enter
when v=0 and neither when v=1; for odd w exactly one enters. The opposite-row
corner supports and all perpendicular exterior tail supports lie outside this
single tile row. Consequently rho=-1 in both phases.

When u=1, the core occupies two tile rows. For even w and v=0 the two tail
tiles are additional; for odd w exactly one is additional; for even w and v=1
neither is additional but the core meets one more tile column. In every case
|R_H|=w+2. The two corner supports and the two exterior tail supports are all
inside. Among axial supports, both enter for even w,v=0, neither for even
w,v=1 and one for odd w. All k optional supports are inside. Thus

    T_R=6+k             if w even, v=0,
    T_R=4+k             if w even, v=1,
    T_R=5+k             if w odd.

Combining (2), (3) and these base counts gives the all-length exact table:

| Chamber row phase | Width/column phase | rho(R_H) | Consequence from (1) |
| --- | --- | --- | --- |
| u=0 | any w,v | -1 | strict one-unit deficit |
| u=1 | odd w, any v | 2-w+k | at most -1 |
| u=1 | even w,v=0 | 3-w+k | at most 0 |
| u=1 | even w,v=1 | 1-w+k | at most -2 |

For arbitrary odd L,R, both receiver tile and selected counts increase by N
and the endpoint count increases by 2N. The table is unchanged. In particular
every bundle-terminal thin component has nonpositive original receiver charge.

There is a sharp neutral multi-square obstruction to demanding one strict
unit from every such component: take w=4, L=R=1, u=1,v=0 and the sole optional
support (-1,1). The fully frozen component has three P-squares, k=1 and rho=0.
Its unit-tail counts are (|R_H|,T_R,|H|)=(6,7,10). The exact coordinates,
matching and freezing checks are recorded in the control receipt. This
refutes that strict payment rule, not the coefficient-one inequality.

## 6. A larger coefficient-one theorem

**Thin-or-one-square theorem.** On an even-by-even rectangular grid, suppose
each initial complete endpoint component is either thin or contains at most
one all-P unit square. Then

    |T|+|M|<=mn/2.                                        (4)

The supporting rows/columns and orientation can differ by component. There
is no initial terminality, alignment or uniform matching-direction assumption.

Proof. Apply finite bundle normalization from Section 1. Every final component
is a subset of an initial one, so it remains thin or has at most one P-square.
All final components are bundle-terminal and hence single-terminal. A thin
component has either a zero-charge comb receiver or a nonpositive capped
receiver from Sections 3--5. A possibly nonthin one-square component has the
nonpositive budget of ALL_ALIGNMENT_SINGLE_SQUARE_BOUND.md. Terminal ownership
makes the complete receivers disjoint; no-P tiles Z form their complement.
The exact original ledger is

    mn/2-|T|-|M| = sum_H (-rho(R_H)) + sum_(Q in Z)(2-t_Q). (5)

All terms are nonnegative. Each tile appears once, and every actual saturated
attachment stays in its matching endpoint's complete receiver. Objective
preservation gives (4) for the initial pair. QED.

Equation (5), with the displayed tables, is the precise compensation formula.
Equality holds exactly when every final receiver is neutral and every no-P
tile has two selected vertices. In particular a thin nonstraight receiver
can be neutral only for even w,u=1,v=0,k=w-3. A prescribed row-aligned capped
component still contributes its strict one-unit deficit. The theorem improves
the matching coefficient from five-sixths to one on this larger initial class,
including arbitrarily many interacting squares in each thin component. General
components genuinely extending over three or more rows and columns, a universal
coefficient-one theorem, and general rectangular-grid triple equality remain open.

## 7. Verification scope

The discovery program check_two_row_terminal_shapes.py independently enumerates
connected two-row shapes, actual matchings and all feasible terminal neighboring
support patterns through span eight. It checks the matching-closed chamber
construction and proposed classification. The separate program
check_thin_component_receivers.py constructs arbitrary odd tails and optional
supports, checks original receiver accounting in every phase, verifies freezing,
tail extension, symmetries and finite initial-pair normalization. Its neutral
three-square fixture distinguishes failure of strict per-component payment from
failure of (4). Neither enumeration supplies the general proof above.

```sh
python3 develop/check_two_row_terminal_shapes.py --max-width 8 --output output/two-row-terminal-shape-controls.json
python3 develop/check_thin_component_receivers.py --output output/thin-component-receiver-controls.json
```

Formal scope and independent review results are recorded separately as they
complete. The earlier two ACCEPT receipts cover the previous receiver and
one-square theorems, not the new thin-component extension in this note.

Completed controls: 7,992 family configurations, 384 symmetry images and 2,664
tail-extension comparisons. Small enumeration considers 24,296 feasible pairs;
22,375 have every initial component thin and satisfy normalization, nonpositive
final receivers and the exact deficit. A separate mixed fixture includes thin
components of both orientations, a nonthin one-square branch and a removable
pure square. The neutral multi-square receiver and its degree-four support
are explicitly checked. These are local execution results, not existing CI.

The combined local Lean audit has 73 declarations. Four new thin statements
cover physical attached-column extension, the conditional chamber-exit count,
optional-support budget and two-step ledger invariance. Four later bent
statements cover physical donor sparsity/terminal endpoint exclusion, conditional
payment and a fixed footprint-orientation check. The global geometric adapters
and this theorem remain written. The new thin review is task
c15a9bea-87aa-4338-8b5c-f8d86190155d, conversation conv_834b102697199117,
original stream 25445. It completed ACCEPT at 08:29:19 UTC on 19 October,
observed gpt_6/pro. Its exact response and independent scope assessment are
archived in output/thin-component-review-response.json and
docs/reviews/2026-10-19-thin-component-assessment.md. It verifies the general
classification, all-length table and global covered-class theorem; no code,
Lean execution or external priority assessment is inferred from this verdict.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
