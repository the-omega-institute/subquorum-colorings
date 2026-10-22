# Complete ten-row chambers: a closed D branch and the full width-six classification

22 October 2026. Authors: Haobo Ma and Wenlin Zhang.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.

## Assumptions and whole-chamber conclusions

Use the immutable full-even-U/standard-rotor model, old inventory O and even
bar rows of `ALL_EVEN_GAP_AXIAL_COMPENSATION.md`. The permitted source
decomposition is an explicit hypothesis. Every source has a connected
nearest-neighbour endpoint graph. In a complete extension an unconsumed
original support has exactly one occupied endpoint neighbour. These
necessary support conditions suffice for the exclusion arguments below.
Let Y_i contain ALL new originals in chamber C_i, as in
`SEALED_CHAMBER_LOCALIZATION_AND_REPAIR.md`, and put

    Delta_i=Phi(O union Y_i)-Phi(O).

At a ten-row gap, normalize the upper bar to row0 and write W for the even
width. Thus C=[2,9] x [1,W]. The following statements control entire
chambers, including all originally unselected sources.

1. For ANY even W>=6, if the actual left owner is the spanning downwards
   source D_W=U(W,4,4), chart(r,c)=(5+r,c), then Y_i={D_W}. Consequently
   Delta_i=W+1 exactly. No other new source can occur in that chamber.
2. At W=6 every complete chamber is exactly one of

       Y_i={D_6}, Delta_i=7;
       Y_i={U_6}, Delta_i=5,

   where U_6=U(6,4,4), chart(r,c)=(9-r,c). This classification is exhaustive
   for ALL new sources in the chamber, rather than only for its gate owners.
   It does not assert global complete-extension existence.
3. If every old gap is ten and W=6, let d count D chambers and let g be the
   number of gaps. Every complete extension has the exact full inventory

       Phi(full)=4g+2d+Delta_out.                         (1)

   The contribution of every chamber is now known; Delta_out remains open.

For contrast, after a spanning U_W is selected at a ten-row gap of arbitrary
width, endpoint-disjoint additions can still drive Phi to minus infinity.
The explicit zero-rotor chain below gives Phi=5-k for k added rotors. Its
first two rotors cannot completely extend. This rules out the endpoint-only
nonnegativity shortcut without contradicting the complete-chamber conjecture.

## A spanning D closes the entire chamber

The upper old B occupies rows0,1 and its two side stems through row4.
D_W occupies complete rows5,6 and its side stems through row9. Therefore
the columns1,W are occupied throughout rows2..9, and rows5,6 are full.
All remaining points of C are exactly the two open rectangles

    P_top=[2,4] x [2,W-1],
    P_bottom=[7,9] x [2,W-1].                           (2)

A new source cannot leave C by the previously proved chamber lemma. Its
endpoint graph is connected and cannot cross rows5,6, so it lies in ONE
rectangle in (2). Each has only three rows.

Every orientation of a full U has vertical span at least four: without
transposition one of its continuous stems supplies vertical difference
at least4, and after transposition its breadth supplies difference at
least5. Every standard rotor has vertical span3, in every orientation.
Neither can fit within three rows, whose largest vertical difference is2.
This proves there is no additional source, with no dimension cutoff or
completeness search. The earlier exact D receipt gives Delta_i=W+1.

## The width-six gate must be one spanning U

The accepted all-parameter axial catalogue at gap10, together with the
accepted lower-rotor exclusion, leaves only D_6, U_6 and the upper rotor H
as a left actual gate owner. The right list is its reflection in c=7/2.
D_6 and U_6 each occupy BOTH gate points, so their actual right owner is
the same original, counted once.

If the left owner is H, the right owner cannot be D_6 or U_6: either would
also occupy the left gate already belonging to H. Thus it would be the
reflected H. But the two full rotor endpoint records intersect at

    (4,3) and (4,4).

Indeed the left H has endpoints

    {(3,2),(4,2),(4,3),(4,4),(5,1),(5,2),(5,3),(6,3)}.

Reflection gives the other list and the displayed intersection. Endpoint
disjointness excludes this pair. Hence D_6 or U_6 is the actual owner.
This uses the complete canonical gate catalogue, not finite width sampling.

## The upward width-six pocket also has no new source

For a spanning U_W the columns1,W are occupied throughout rows2..9,
and its full bar is in rows8,9. The unoccupied chamber points form

    P=[2,7] x [2,W-1].                                 (3)

P has a completely occupied one-step boundary. Its first row and column
are even, and its last row and column are odd. Consequently its tiles
are wholly inside P, so any source confined to P has no physical-tile
contact with O+U_W. All its supports outside P are on the old boundary
and already consumed. This separation concerns accounting; completeness
at supports inside P still sees the boundary neighbours.

At W=6 translate P to [0,5] x [0,3]. A full U cannot fit: an untransposed
U needs at least6 columns, and a transposed U needs at least5. A rotor
has a 4-by-4 bounding box. Quarter-turn symmetry of its complete T/H/M
record leaves exactly two normalized handednesses, with endpoint sets

    A={(0,1),(1,1),(1,2),(1,3),(2,0),(2,1),(2,2),(3,2)},
    B={(0,2),(1,0),(1,1),(1,2),(2,1),(2,2),(2,3),(3,1)}. (4)

Its horizontal position is forced, while its top row t is0,1 or2. Write
A_t,B_t for those vertical translations. The following table exhibits an
endpoint common to every pair of distinct candidates:

| Pair | A_0 | B_0 | A_1 | B_1 | A_2 |
|---|---|---|---|---|---|
| B_0 | (1,1) | | | | |
| A_1 | (1,1) | (1,1) | | | |
| B_1 | (1,2) | (1,2) | (2,1) | | |
| A_2 | (2,1) | (2,1) | (2,1) | (3,1) | |
| B_2 | (2,2) | (2,2) | (2,2) | (2,2) | (3,1) |

Thus at most ONE rotor can be selected. Every single candidate, however,
has an unconsumed original support with two already occupied neighbours:

| Rotor | Original support z | Own endpoint adjacent to z | Boundary neighbour |
|---|---|---|---|
| A_0 | (0,0) | (0,1) | (-1,0) |
| B_0 | (0,0) | (1,0) | (-1,0) |
| A_1 | (0,1) | (1,1) | (-1,1) |
| B_1 | (0,2) | (1,2) | (-1,2) |
| A_2 | (2,0) | (2,1) | (2,-1) |
| B_2 | (2,0) | (3,0) | (2,-1) |

Each z is absent from that rotor's T. It must be consumed by a different
actual original. U originals cannot fit, and every other rotor collides
with the retained one. An exterior source cannot enter the pocket through
its occupied boundary. Thus each of the six possibilities is impossible
in a complete extension. This is an exhaustive fixed-record coordinate
proof, not an enumeration substituted for an unbounded dimension argument.
Therefore P has no new source and Delta_i=5 for U_6. The D proof gives7.

The displayed pair table is also independently checked by the companion
full-record verifier. Substitution verifies the retained-support conditions
inside the chamber for each of the two surviving chamber states. This is
local admissibility only; old supports elsewhere still require attention.

## Exact simultaneous consequence

Different chambers have disjoint new-source tile footprints, even though
their old wall owner is shared. In width six with g ten-row gaps, d D
chambers and g-d U chambers, the accepted common-baseline identity gives

    -g+Delta_out+7d+5(g-d)=4g+2d+Delta_out.

No originally unselected source can reduce a chamber's contribution here:
there are no such sources in any chamber. The exterior class is still a
genuine unknown; (1) is not a proof that the full inventory is nonnegative.
For arbitrary W, each spanning-D chamber can similarly be replaced by its
known exact contribution W+1 in the whole-family identity.

## An unbounded partial obstruction in the upward pocket

Use the A rotor in (4), with its full original support and matching record.
At any even W>=3k+3 put k copies A_j at pocket coordinates (0,3j),
0<=j<k, in the spanning-U_W chamber. Their endpoint sets are disjoint.
Every charge is0: direct tile counts give4 edges,4 endpoint tiles and4
inside-tile supports at either horizontal parity. Each individual
therefore contributes zero source mass.

Consecutive sources have precisely three foreign endpoint adjacencies:

    (1,3j+3)--(1,3j+4),
    (2,3j+2)--(2,3j+3).
    (1,3j+3)--(2,3j+3).

The third always crosses a tile-row boundary. For even j only the second
is intratile, with an event from A_j to A_(j+1); its reverse is excluded
by A_(j+1)'s original support. For odd j only the first is intratile,
with an event from A_(j+1) to A_j; its reverse is excluded by A_j's
original support. Their shared physical
tiles have only three endpoints, so no new mixed full tile occurs. Sources
two or more positions apart have no adjacent endpoints or shared tiles.
Thus the complete exact added sets have |F|=0, |E|=k-1, and

    Phi(O+U_W+all A_j)=4-(k-1)=5-k.                     (5)

This defeats any nonnegative-marginal rule for arbitrary extra originals
even in a fully compensated ten-row chamber; its loss has no fixed bound.

It does NOT give a complete-chamber counterexample. For any consecutive
pair, z=(0,3j+3) is an original support of A_j and is not occupied by any
rotor of the chain. It has occupied neighbours above on the old pocket
boundary, east in A_(j+1), and south in A_j. Completeness forces a new
original at z with its sole possible internal direction west. But every
permitted U/rotor west terminal also contains the endpoint two steps west,
which is (0,3j+1), already occupied by A_j. This is impossible. The argument
uses just the two rotors and the occupied top boundary, and allows arbitrary
extra sources anywhere else; the forbidden pair cannot completely extend.

This continuation obstruction explains precisely why finite endpoint-only
negative inventories cannot decide the sign of complete chamber budgets.

## Verification and frontier

The companion verifier checks full-source exclusion in the D pockets,
the exact six width-six rotor records, every pair intersection and every
support witness, gate intersections, local support admissibility, exact
chain charges/full-tile/event SETS, and simultaneous mixed D/U chambers.
The written proofs above give the unbounded statements.

`discover_six_row_chamber_budget.py` separately builds finite complete
retained-support SMT models in the six-row pocket. Widths8,10,12,14,16,20
have no negative local inventory in that finite model; this is discovery
evidence, NOT the arbitrary-width sign theorem. At widths12 and above
there are complete local states with two rotated U originals, so extending
the width-six no-extra-source classification to all widths is false.
The solver checks the neighbours of the FULL retained occupied set, whereas
the general exclusion proof needs only the weaker endpoint condition.

One such wider-pocket witness is explicit. At W=12, in the pocket coordinates
of (3), take two U(6,4,4) originals with charts (r,c)->(6-c,r) and
(r,c)->(6-c,9-r). Their joint top/bottom rows0,5 fill columns0..9; their
vertical bars occupy columns0,1 and8,9. The cross-consumed original supports
are at rows0,5 and columns4,5. The only remaining supports inside the pocket
are (1,3),(4,3),(1,6),(4,6), each with its single endpoint neighbour on row0
or5. Other original supports are on the occupied boundary and consumed.
The old core's interior side supports are consumed by the bars. Thus the
state is locally complete even for the full retained occupied set. Each
source has charge-1; there are no new mixed tiles or events, so the added
inventory is exactly2. This is a direct counterexample to extending the
width-six EMPTY-pocket classification to all widths, with no implication
of negative budget or complete global existence.

The accepted sealed-chamber localization/RZ repair task f5f62488 completed
on original73515, exit0/DONE,19028 characters exactly matching its terminal
API, observed gpt_6/pro. It requested no mathematical correction and reports
fresh negative/repair set computations and a heterogeneous common-baseline
partition control. It did not independently rerun Lean. This present note
was written later and is outside that completed review's scope.

The entire six-row pocket sign theorem, other actual gate branches, wider
gaps, the exterior contribution, universal source decomposition and global
5/6/grid-equality objectives remain open. The submitted manuscript is unchanged.

Final full-record Python invocation4bf947 exited0:48 source-span controls,
six complete rotor records/24 dihedral images,15 exact pair intersections,
six support witnesses,two width-six gate states,40 core inventories and80
simultaneous mixed full-chamber batches. Fourteen chain controls through
k=200 compare514 exact source-labelled events, including the alternating
emitting owner, and reach partialPhi=-195. Ninety-six terminal controls
and the explicit locally complete W12 two-U witness pass. Width/depth2000
controls are included. The initial guessed chain profile/event direction
was corrected before this final pass, without changing its stated Phi.

Final local Lean4.33.0 invocationad8134 exited0:38 explicit definitions/
theorems including20 local theorems, plus SourceWalk, all39 declarations
individually audited. Only ordinarypropext/Classical.choice/Quot.sound
or none; no warnings/sorry/native. Preflight72% memory free and no real
lean/lake by comm-basename inspection. The formal source covers abstract
connected-walk pocket separation, all-frame unbounded U/rotor span
obstructions, fixed six-rotor witnesses/closure, gate collision, terminal
continuation and the exact arithmetic. Actual source-role/connectivity
adapters, geometric inventory assembly and completeness remain written.

A distinct review of the new complete-chamber/chain proposition is live
on originalstream58738 in conversationconv_e18bcaa504addda4, after pool
preflight17ready/8busy/1needs_attention/0queued. The request contained the
proof and verifier before the final explicit W12 witness paragraph/check
was added; that addition is not claimed reviewed. The Lean statements were
supplied with their local validation still pending; the final role proof
was then refactored and kernel-checked. No new verdict is yet inferred.
