# Unique actual mates and exact maxima for adjacent frozen modules

25 October 2026. Haobo Ma and Wenlin Zhang. Independent research branch.

We remove two restrictions from the preceding [fixed-P maximum
result](SELECTION_MAXIMUM_SINGLETON_OBSTRUCTION.md): the actual matching is
now proved unique, and the number of horizontally adjacent modules is
arbitrary. Fix even W>=8 and q>=1, and put n=W/2. On the endpoint set P
specified below in the (W+2)-by-(10q+2) grid,

    M is the unique perfect matching of the grid graph induced by P;
    max over ALL feasible T disjoint from P of |T| = (7q+2)n+3q+2;
    max (|T|+|M|) = |V|/2-2q.                              (1)

An explicit attaining T is completely frozen, has q alpha strands, no beta
and 7q mixed strands, and has zero compensation even with the entire original
interval pool available. Its unpaid demand is q; its numerical slack is 2q.
The physical regions proving the bound are disjoint across modules as well
as within each module. This establishes an exact additive slack-versus-deficit
statement on an unbounded two-parameter family. It does not establish a bound
for other endpoint sets or other choices of bands.

## 1. Coordinates, feasibility and canonical matching

Rows are 0..W+1 and columns are 0..10q+1. In a single module let P consist of

    columns4,5,6: all rows1..W;
    columns3,9: rows1,W;
    columns7,8: rows1,W-1,W.

Translate this set by 10i columns for i=0..q-1 and take the union. Different
P slabs have horizontal separation four between their nearest endpoint
columns, so their induced endpoint graphs have no edges between slabs.
There are q(3W+10) endpoints.

Define the matching in each slab by the following ordered pairs. In a pair
(a,b), a is the designated leaf. Translate both entries by 10i in module i.

1. For r=1,W, take ((r,3),(r,4)) and ((r,9),(r,8)).
2. Take ((1,7),(1,6)).
3. For odd r=1,3,...,W-1, take ((r,5),(r+1,5)). If r+1<W, then take
   ((r+1,4),(r+2,4)) and ((r+1,6),(r+2,6)).
4. Take ((W,6),(W,7)), then ((W-1,7),(W-1,8)).

These are adjacent disjoint pairs covering exactly the displayed endpoint
set; there are 3n+5 pairs per slab. A selected set is feasible if it avoids P
and each selected vertex has at most one grid neighbour in T union P. This
is the same feasibility condition as the preceding note.

## 2. Matching uniqueness, independent of T

At each step of the displayed order, the first endpoint has exactly its
named mate left in the remaining endpoint graph. Here is a direct check.
The four outer column3/9 vertices are initially leaves. Removing them and
their mates makes (1,7) a leaf. At the start of the odd-r iteration, all
column4/6 vertices above r have already been removed, and their row-r
vertices have also been removed. The vertex (r,5) has only (r+1,5) left:
its upward neighbour, if any, was removed in the preceding vertical pair.
After this central pair is removed, (r+1,4) and (r+1,6) each have only their
row-(r+2) neighbour left. For r+1<W their possible outer side neighbours
are absent: column3 occurs only at rows1,W, and column7 only at rows1,W-1,W;
r+1 is even and strictly between1 and W. At the last iteration the already
removed bottom column4 vertex and the retained bottom relay account for the
stated final two pairs. They are successive leaves as well.

Every perfect matching must contain an edge incident to a leaf, and that
edge is forced. Remove its two vertices and repeat. Induction forces every
displayed edge and proves uniqueness. Disjoint slabs give the same conclusion
for any q. This proof does not refer to T, freezing or the band decomposition.
In particular, allowing a different actual matching on this fixed P cannot
repair its compensation obstruction.

A reusable formulation is: give each canonical pair its position as rank,
choose one leaf endpoint in each pair, and require every other neighbour of
that leaf to lie in an earlier pair. Any other adjacent involutive mate map
must equal the canonical map. Strong induction proves this: if a leaf were
matched to an earlier vertex u, the induction hypothesis at u and involutivity
would force its mate to be the leaf, contradicting the canonical pairing.
This general implication is formalized in Lean without a size bound.

## 3. Upper bound for every feasible T, without a retention hypothesis

A point in P or with at least two P neighbours cannot be selected. Tile the
whole board into aligned2-by2 squares. Any feasible T has at most two points
in a square, since among any three one has two selected neighbours. Applying
the endpoint exclusions gives the following cap rows, one five-entry block
per module, followed by one final tile of cap2:

    top and bottom bands:    [2,2,1,1,1] repeated q times, then2;
    ordinary interior bands:[2,2,0,1,2] repeated q times, then2;
    penultimate band:        [2,2,0,0,1] repeated q times, then2.

The ordinary interior bands have upper rows2,4,...,W-4. Entries0 have no
allowable point; entries1 have a single candidate, or an adjacent candidate
pair facing P so both cannot be selected. Entries2 use the square bound.
These local reasons follow from the endpoint columns in Section1, and are
unchanged at an inter-module seam. There are n+1 bands, of which exactly one
has sum5q+2; all others have sum7q+2. The initial cap is

    (7q+2)n+5q+2.

For each i, replace the two old tiles in each4-by2 patch with top-left
coordinates (0,2+10i) and (W-2,2+10i). If the top-left is (r,c), the only
P-allowable sites in the patch are

    (r,c),(r,c+1), (r+1,c), (r+2,c), (r+3,c),(r+3,c+1).

Partition these six sites into the top horizontal pair, the middle vertical
pair, and the bottom horizontal pair. Each pair has an endpoint with an
existing P neighbour; selecting both would give it at least two occupied
neighbours. Thus its cap is3 instead of the old4. Top and bottom patches
have disjoint row sets because W>=8. Patches in different modules have
disjoint columns. All patch boundaries coincide with old tile boundaries.
Replace these2q old contributions, keeping every remaining tile once; the
result is the upper bound in(1). No region or spare capacity is counted twice.

This proof applies to arbitrary simultaneous choices of T and allows old
selections to be removed. It is not an extension-only bound.

## 4. A uniform attaining and fully frozen selected set

Let I={0,...,q-1}. The following are sets of column indices:

    O = odd columns1,3,...,10q+1;
    E = {10i,10i+2:i in I} union {10q};
    F = {0} union {10i+8,10i+11:i in I};
    U = {10i,10i+2,10i+8:i in I} union {10q};
    D = {10i+1,10i+3,10i+7,10i+9:i in I} union {10q+1}.

Take T in the following rows:

    rows0,W+1: O;
    rows1,W: E;
    row2: F; row3: D;
    upper interior rows r=4,6,...,W-4: U;
    lower interior row r+1: D, except at W-3;
    rowW-3: (D minus {1,3}) union {0,2};
    rowW-2: (U minus {0,2}) union {1,3};
    rowW-1: {0} union {10i+11:i in I}.

This is exactly `configuration(W,q)` in the verifier. All entries are inside
the board and outside P. Here is the feasibility check independent of board
size. In each ordinary interior pair of rows, the U/D pattern alternates on
the free columns; consecutive modules join with columns8,10,12 in U versus
9,11,13 in D. No two selected points are adjacent there, and inspection of
columns modulo10 gives at most one P neighbour. At the exceptional lower
left interface, columns0 and2 form two vertical T pairs in rowsW-4,W-3;
the adjacent rows avoid these columns, their horizontal neighbours are blank,
and they face no P. The switched rowW-2 uses columns1,3 instead. The other adjacent T pairs are (1,0)--(2,0),
(2,10i+11)--(3,10i+11) for i=0..q-1, and
(W-1,0)--(W,0). Each has no P neighbour and no third selected neighbour.
At the top interface, compare the O,E,F,D rows;
at the bottom compare the switched U, the sparse rowW-1, E,O. Each selected
vertex either faces a single P or has no occupied neighbour, except for the
isolated vertical pairs just listed. The same modulo10 check covers
the module seams and the final two columns.

The row counts sum to

    2(5q+1)+2(2q+1)+(2q+1)+(4q+1)
      +(n-3)(7q+2)+(3q+1)+(q+1)
      = (7q+2)n+3q+2.

Thus T attains the upper bound. For q=2 it is precisely the previous note's
all-T maximum; q=1 already gives the10-by12 example with41 selected points.

For completeness, freezing transfers uniformly from the previous note's
right-hand module reduced-selection certificate, with that module translated
left by10. Its selected witnesses form the following small seed:

    row0: O restricted to1..11;
    row1: 0,2,10; row2:8; row3:3,7; rowW-2:8;
    rowW:0,2,10; rowW+1:3,5,7,9,11.

Every translate of this seed is contained in the present T. The preceding
note proves the seed freezes its entire P slab by the direct-core induction,
upper and reverse lower seal inductions, and the two postponed lower relay
events. Those witness endpoints and their canonical mates all lie inside
the same slab. Consequently its strict-rank schedule translates independently
to every module; no other module is used as a freezing witness. Adding the
rest of T preserves the certificate. The verifier transports precisely this
formula schedule and independently checks every pair of nonmate witnesses.
This is a proof by the previous uniform induction, not a guess from finitely
many peeling runs.

## 5. Complete original pool, zero payment, exact additive margin

Use aligned horizontal bands(0,1),(2,3),...,(W,W+1), and the whole-band
BB/TT adapter of the preceding note, including balanced boundary chains
with zero credit. In each module the original strand inventory is one alpha,
no beta and seven mixed strands. Its alpha tips are (1,5),(W,5), translated
by10i. Its non-self directed mixed routes, in each terminal row r=1,W, are

    A_i -> mixed columns(3,4);
    A_i -> mixed columns(6,7) -> mixed columns(8,9).

All these coordinates translate by10i. The extra mixed owner in the
penultimate band is unreachable. Interior PP bodies are shielded from no-P
gaps by the adjacent P columns. The module seams contain no endpoint-to-
endpoint links, so they create no new mixed route. In each terminal band,
every no-P gap incident to these reachable owners has zero capacity: its
number of selections equals its number of columns. This includes the
between-module gaps, whose terminal rows alternate E with O. Therefore
the union of the complete interval supports of ALL reachable owners is empty.

The no-beta cancellation argument applies: a component carrying an alpha
has outward mixed arms and cannot merge with another alpha, and an interval
payment must use a resource in that closed reachable support. Thus no alpha
can be paid, including through longer routes or through another module.
The exact whole-pool optimum is0, attained with zero links, and the deficit
is q. All raw resources are available; there are no reservations or locked
resources in this claim.

Equation(1) gives S=|V|/2-|T|-|M|=2q. The exact whole-band ledger
S=L+beta-alpha then gives L=3q. These raw units exist outside the reachable
support. With all of them unused and q unpaid demands,

    unused original intervals minus unpaid demands = 3q-q = 2q. (2)

The same positive margin follows from the disjoint physical cover before
any compensation routing is attempted. It is never justified by assigning
a reachable unit to two different demands. The precise cap replacement and
the zero-support calculation are separate proofs of separate statements.

## 6. Verification and scope

Run from the repository root:

    python3 develop/check_forced_mates_and_adjacent_maxima.py --output output/forced-mates-adjacent-maxima-validation.json
    python3 develop/check_forced_mates_formal.py --lean /path/to/lean-4.33.0 --output output/forced-mates-adjacent-maxima-formal-validation.json

The geometry checker covers W in{8,10,12,20,40,64}, q in{1,2,3,4,7,12}:
36 fully frozen attaining boards,7569 forced mate pairs,348 disjoint patch
replacements and6 comparisons with the previous two-module construction.
It independently checks feasibility, forced elimination, strict leaf ranks,
translated freezing ranks, band inventory, full-pool flow and the scalar
ledger. The permanent smallest fixture stores41 selected points,17 matching
edges,34 frozen endpoints, all witnesses and the physical upper certificate.
These finite checks test the proofs above; they do not replace them.

The Lean source proves generic strict-leaf-rank mate uniqueness and arbitrary
n/q scalar budget identities, and checks actual W8/q1 feasibility, all34 frozen
endpoints and its leaf-pair rank certificate. The all-W/q coordinate
specialization, the cover-to-count adaptation and the band/cancellation
adapter remain written proofs with Python checks. We do not describe this
as end-to-end formal verification of the grid maximum.

Matching freedom on this P has been closed. Changing P and choosing another
band direction or phase remain possible mechanisms, and are not covered by
this theorem. In particular the result refutes a universal full-compensation
rule even after fixed-P selection optimization and actual rematching, while
its positive slack provides no counterexample to the target numerical
inequality. No universal improvement of5/6 is claimed. The11 October
manuscript and the public main branch are unchanged.
