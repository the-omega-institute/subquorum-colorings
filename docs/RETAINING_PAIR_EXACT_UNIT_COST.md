# A bad minimum pair forces exactly four unit expenses

11 November 2026. This sharpens the retaining-pair lower bound in Section 5
of `SIMULTANEOUS_PORT_COMPLETION.md`. It does not change the unrestricted
optimum two, the all-K example, or the accepted fifteen-page working PDF.

Use the same 8-by-12 board, matching M and terminal sets. Coordinates are
zero-based. The three 3-by-3 square origins are (1,3), (1,9), (5,5), and
their black centres are (2,4), (2,10), (6,6). Each square minus its centre
is a core. Translate the local actual edges

    (0,0)--(0,1), (0,2)--(1,2),
    (2,2)--(2,1), (2,0)--(1,0)

into every core. Let W={(4,5)}; every other white vertex outside the cores
is selected. All actual edges have unit weight. A full auxiliary matching
is charged only for actual edges on TH paths. HH paths and closed components
are free. Require the following two terminal paths to remain intact:

    A: (4,9),(3,9),(2,9),(2,10),
    C: (5,8),(5,7),(6,7),(6,6).

**Proposition.** Among all full physical auxiliary matchings retaining A
and C, the minimum TH expense is exactly four. Thus an arbitrary minimum
local path pair can cost twice the unrestricted optimum after completion,
even when every actual weight is one.

## Lower bound for every retaining completion

Put

    D={(4,10),(5,9),(5,11),(6,8),(6,10),(7,9),(7,11)},
    F={(4,9),(4,11),(5,8),(5,10),(6,9),(6,11),(7,8),(7,10)}.

Then N_T(D)=F, |D|=7 and |F|=8. In any terminal bijection of a full
matching, at least two selected sources in F are sent outside D: A and C
end at centres. Therefore at most six of the eight sources in F can end
in D. Since D has seven endpoints, some terminal path must enter D from
a white source outside F. This is a direct pigeonhole argument; it does
not assume that the third centre is HH or fix the number of TH centres.

That incoming path cannot start at W. Delete the vertices of A and C.
The white states reachable from (4,5) by alternating steps whose interiors
remain in P are exactly

    (4,5), (3,4), (2,3), (1,4), (2,5), (5,6).

Here the middle four states lie in core 0. No vertex of D is adjacent to
that core or to (4,5). The final state (5,6) lies in core 2: its possible
next black vertices are the exterior (4,6), the used centre (6,6), the used
vertex (5,7), and its preceding actual mate (5,5). Thus it cannot continue
to D. Alternating paths cannot pass through an intermediate Q terminal.
There is no HH path to D in a completion retaining A and C.

Consequently the incoming path is TH, starts in T minus F, and ends in D.
It is not direct, since N_T(D)=F. It also cannot use just one actual edge.
The only white P vertices adjacent to D are (3,10) and (6,7). Vertex (6,7)
belongs to the retained path C. The actual mate of (3,10) is (3,11), whose
only white Q neighbour is (4,11), a member of F. Hence a one-actual-edge
path into D cannot start in T minus F.

The incoming TH path therefore contains at least two actual edges. It is
a different terminal component from A and C, each of which contains one.
Their actual edge sets are disjoint in a full matching. Every retaining
completion consequently has TH expense at least 1+1+2=4.

## An attaining full matching

Retain A and C, and take the two additional relays

    H: (4,5),(3,5),(3,4),(2,4)        [HH, free],
    E: (0,11),(1,11),(2,11),(3,11),(3,10),(4,10)  [TH, expense 2].

These four paths are vertex-disjoint. For the direct exterior part take
vertical edges (a,b)--(a+1,b) for

    (a,b)=(0,2),(0,7),(0,8),(1,6),(2,2),(2,7),
          (2,8),(3,6),(4,2),(4,11),(6,4).

Delete the three square footprints, W, the three selected sources
(4,9),(5,8),(0,11), the exterior endpoint (4,10), and the endpoints of
these vertical edges. The remaining row intervals are:

| Row | Intervals |
| --- | --- |
| 0 | [0,1], [3,6], [9,10] |
| 1, 2, 3 | [0,1] |
| 4 | [0,1], [3,4], [7,8] |
| 5 | [0,1], [3,4], [9,10] |
| 6, 7 | [0,3], [8,11] |

Every interval has even length, so pair consecutive vertices horizontally.
Use the auxiliary edges of the four relays and retain every unused M edge.
This covers all 96 vertices exactly once. Its TH expense is 1+1+2=4;
the single actual edge on H is free. This proves attainment and the
proposition.

Run `python3 scripts/check_retaining_pair_optimum.py`. The checker builds
the board and matching directly from the coordinates, checks the reachability
and one-edge obstruction, constructs all 48 auxiliary edges from the row
tiling, and scores tagged terminal components independently. Its complete
matching and paths are in `output/retaining-pair-exact-four.json`. The
coordinate argument above proves the lower bound over every full matching;
the program does not enumerate or assume all completions have a prescribed
normal form. No new Lean verification is claimed.
