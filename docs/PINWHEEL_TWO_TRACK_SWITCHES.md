# Exact two-track direction switches at degree-three pinwheel tiles

26 October 2026. Wenlin Zhang and Haobo Ma. Research branch; submitted
manuscripts and public main are unchanged.

**Beta continuation:** [fixed outside beta cores](PINWHEEL_BETA_CORE_SWITCHES.md)
remove the two-mixed restriction using a stub-supported fork normalization.
All selected degree-three pinwheel roots now optimize jointly by one flow,
with one private credit per beta core and an exact direction-optimized cut
criterion. The theorem below retains its original two-mixed scope.

The [alpha-localization theorem](FOUR_OUTWARD_ALPHA_LOCALIZATION.md) excludes
alpha wires at degree-three four-outward tiles in a uniform direction.
Here we identify the remaining physical routing, prove an exact joint
direction-optimization theorem for tiles with two mixed owners, and give
an all-length restricted-original-pool repair family. No fresh credit is
assigned to a tile or an interface. Universal 5/6 remains open.

## 1. Physical hypotheses and the forced pinwheel

Let (T,M) be feasible on a finite even-by-even grid, with P=V(M), every
p in P of occupied degree exactly three, and no feasible nonempty oriented
simultaneous promotion bundle. Start with uniform horizontal two-row bands,
so the auxiliary matching N is vertical. Use the original whole-owner
support model with each original interval used once, each mixed owner
capacity one, each beta having two actual BP entries but only one private
whole-beta unit. Available original intervals may be restricted arbitrarily.

Let Q be an aligned full-P tile, all four actual mates outside Q. Then
its four actual exit directions, in NW,NE,SW,SE order, are exactly

    (N,E,W,S)   or   (W,N,S,E).                            (1)

**Proof.** A face with two outward actual M edges would be an actual
alternating unit square. Promoting either color deletes both occupied
neighbors on that square at every promoted vertex and leaves degree at
most one. This is a forbidden bundle. Thus no face has two exits. There
are four exits and four faces, so each face has exactly one. Choosing the
NW direction forces successively all other directions, giving (1).
The fourth, unused outside neighbor at each corner is blank, since its
two internal P neighbors and actual mate already give occupied degree
three. Therefore each neighboring tile along a face contains one actual
mate and one forced blank in its column adjacent to Q. Q has no full-P
tile as a side neighbor. QED.

Each vertical N wire in Q has exactly one horizontally actually matched
corner x. Its outside mate b=m(x) has a blank vertical N partner, forced
by the OTHER corner's degree. Thus b is a BP terminal in that very owner.
The BP terminals forced by the two wires have the SAME checkerboard color.
An open M/N strand starts and ends with M edges and hence has odd length;
its terminal colors are opposite. The two wires therefore belong to
DISTINCT open owners, each mixed or beta, never alpha or cycle.

Across all such Q, the forced BP terminals are different: each belongs to
its unique actual root corner. Consequently a mixed owner meets at most
one such tile, and a beta owner meets at most two. In particular, for a
collection F the 2|F| wire incidences inject into different original BP
terminals, giving 2|F|<=gamma_F+2 beta_F. This is an incidence bound, not
a count of independently available beta credits.

## 2. Two mixed owners give an actual two-track switch

Select any collection S of these tiles whose two ORIGINAL owners are
both mixed. All 2|S| affected owners are distinct by the preceding BP
injection. This is the key additional hypothesis; do not apply the
following theorem to tiles involving beta tracks.

For a root Q remove its two N edges, keeping all physical T,P,M fixed.
Each affected mixed path breaks into:

* a stub S_i consisting of its horizontally exiting corner x_i and the
  outside BP b_i=m(x_i), joined by their actual M edge;
* its remaining tail L_i, ending at the original TP t_i, i=0,1.

These four fragments are disjoint paths. In the uniform direction the
pairing is S_0--L_0 and S_1--L_1. Changing only Q's auxiliary direction to
horizontal pairs them as S_0--L_1 and S_1--L_0. Each new owner is again
mixed. No alpha, beta, or TP/BP terminal identity is created or removed.
Other original owners are unchanged.

This is an authorized choice between TWO local pairings, not a claim
that a fixed-direction tile is an all-to-all router. The degree-four
[same-owner obstruction](SINGLE_SQUARE_WIRES_AND_SOURCE_FREE_PRUNING.md)
violates the hypotheses and remains valid.

### Preserve actual links and the original resource pool

Realize every simultaneous choice as an even-rectangle partition: in each
two-row band isolate the selected 2-by-2 root tiles and retain the remaining
horizontal strips; flip just the selected roots. A root has no side-adjacent
root, so every outside BP's N partner stays unchanged.

No root corner is a TP or BP before or after. Hence no actual terminal
link crosses a new root boundary, and all external horizontal TP--BP links
are exactly the same in every partition. Potential old self-links must
be retained in this COMMON list: exchanging tails may turn one into a
nonself link. Conversely, a link that is self in a chosen orientation is
irrelevant to its minimum-cost optimum.

Every original BB/TT resource component lies in a P-free interval. It
cannot cross a root's PP column. Cuts at root boundaries therefore split
no such component, including balanced boundary chains. The flipped root
contains only PP pairs and contributes no resource. Identify a unit by
the actual cells of its BB/TT component, not by a changing band index.
Thus the entire original pool, and every prescribed available subset,
is identical in all direction choices.

The two PP columns in Q support no resource: their outside neighbor
columns each contain P and a forced blank. The flipped root also supports
none. All support witnesses lie on fixed outside fragments. Let W(S_i)
and W(L_i) be their original gap-adjacency supports. A single unit can
occur in both sets; its identity is never duplicated. In orientation pi
the exact support of the owner with BP b_i is

    W(S_i) union W(L_pi(i)),                              (2)

where pi is either identity or transposition. This proves the physical
adapter, including costs and arbitrary original-unit restrictions.

## 3. One flow optimizes all 2^|S| orientation choices exactly

Start from the complete BP-aware whole-support fork network. Retain all
unaffected alpha, mixed, beta-entry, private-beta and original-resource
gates. For each selected tile replace its two mixed gates as follows:

    BP b_i -> stub_i, capacity 1;
    tail_i -> TP t_i, capacity 1;
    stub_i -> tail_j, capacity 1, for all i,j in {0,1}.

Each stub has support arcs to W(S_i), and each TP output to W(L_i).
Support arcs use the usual large capacity k+1. Every external physical
link has cost one; every new internal switch/gate/support arc has cost
zero. Each original interval still has ONE global capacity-one sink.
Existing beta owners retain two distinct BP entry gates and ONE private
whole-beta sink; their fork normalization is unchanged.

**Exact joint optimization theorem.** For any available original resource
subset, maximum whole-support payment over all simultaneous root direction
choices equals the integral maximum-flow value of this one network. The
minimum number of physical links attaining that payment equals its minimum
cost. An optimum flow yields actual directions at every selected root.

**Proof, physical choice to flow.** Fix its pairing pi. An incoming use
of a switched mixed owner enters through its BP gate. If its payment uses
a stub support, send it directly from stub_i to that interval. Otherwise
send it on stub_i->tail_pi(i), and then either its tail support or its
physical TP output link. Equation (2) covers all whole-owner supports.
The ordinary/fork normal form supplies the same paths for unaffected
owners. Owner-disjointness implies entry and output capacities. No new
cost is incurred. Thus the relaxed network dominates every physical choice.

**Proof, flow to physical choice.** In an integral minimum-cost maximum
flow, the used internal arcs at each root form a partial matching of
two inputs and two outputs. Input capacity one includes paths ending
immediately at a stub resource; output capacity one includes all paths
continuing through that tail. Every partial matching on two inputs and
two outputs extends to either the identity or the transposition. In
particular, two used arcs cannot demand inconsistent parities. Choose
the corresponding physical direction independently at each root. Inputs
ending at stub resources impose no tail choice, so the remaining pairing
can still be completed. No other flow can occupy that remaining tail:
any occupied output already occurs in the partial matching.

All used paths now embed in the chosen actual mixed owners, with at most
one unit per owner. External links keep their actual TP/BP identities.
Every forward directed cycle contains a positive-cost external link, so
minimum cost eliminates circulations. A physical link made self by the
chosen pairing would close such a cycle and therefore is not used.
Apply the established private-beta normalization at untouched beta
owners: use its private whole-beta unit first, and at most one original
interval for a second incoming path. This preserves value and external
link cost. The resulting ordinary stems/beta forks are a legal physical
pack with the flow's payment and cost. Both optimizations are equal. QED.

The network has four internal crossing arcs per root and polynomial
size in owners, physical links and resource-support incidences. This
optimizes payment, then LINKS. It does not optimize the number of flipped
tiles; charging each crossing arc would incorrectly charge a two-track
transposition twice.

## 4. Sharp one-unit repair ceiling per root

Let V0 be payment in the original uniform direction and V* the optimized
payment over these q=|S| roots, on the SAME available pool. Then

    0 <= V* - V0 <= q.                                   (3)

More generally any fixed direction choice differing at s roots has payment
at most V0+s; applying the same argument backwards gives absolute change
at most s. This controls payment, not link cost.

**Proof by cuts.** Represent the original identity pairing with the same
split entry/output gates but only the two diagonal internal arcs. Take
a minimum cut in this network. Adding the two off-diagonal arcs at one
root increases its capacity by zero, one or two. In the first two cases
the increase is at most one. If BOTH added arcs cross, both stub nodes
are on the source side and both tail nodes on the far side. Both original
diagonal arcs already crossed, contributing two. Move both stub nodes
to the far side. Now no internal crossing arc leaves those stubs; their
two incoming capacity-one entry gates contribute at most two instead.
All their other incident arcs are OUTGOING resource supports, whose
crossing contributions can only decrease. All other arcs stay unchanged.
Thus this root contributes no increase over the old cut. The stub moves
at distinct roots concern disjoint nodes, so performing them together
increases total cut capacity by at most q. Max-flow/min-cut proves the
upper bound. Identity is an allowed choice, proving the lower bound.
For a specified subset use just those switches; reverse the two pairings
to obtain the absolute-change statement. QED.

## 5. All-q physical repair on a restricted original pool

Use the [66-endpoint degree-three frozen fixture](../develop/fixtures/degree_three_four_outward_live_mixed.json),
with its root at rows4--5/columns4--5. Here we flip the ROOT, rather than
the left-neighbor tile used in the localization boundary example. The
fixed original alpha enters BP (5,3) along the actual link

    (5,2) -> (5,3).

Its two original mixed tracks have TP endpoints (3,4) and (6,5).
The original unit R={(6,4),(7,4)} is on the right tail's support, with no
direct alpha support. When R alone is available, the original direction
pays zero. Flipping the root pairs BP (5,3) to the right tail, paying the
alpha with the displayed single link. The symmetric original unit
L={(2,5),(3,5)} illustrates why an arbitrary flip is not monotone: with
L alone available, the same flip changes payment one to zero. Joint
optimization chooses the better direction for the actual available pool.

For ANY q>=1 translate q copies by (16k,0), k=0,...,q-1, in a
(16q-2)-by-14 rectangle. The two blank separator rows prevent physical
contacts between copies; they form their own horizontal band and have
no support adjacency to any endpoint. Feasibility, all endpoint degrees
and the strict freezing schedule are inherited independently. Thus

    |P|=66q, |M|=33q, |T|=26q.

Make available exactly the q distinct translated R units. In each copy
the alpha reaches only the left BP/mixed tail before a flip, which has
no available resource or reachable beta; after a flip it reaches R.
There are no inter-copy links or owner supports in a common band.
Consequently for ANY flipped subset H,

    payment = |H|,    minimum links = |H|.                 (4)

Flipping all q roots attains the gain q ceiling in (3). This is a
family proof, not extrapolation from a finite search. The complete
original pool already pays all q alphas with zero links in every copy's
original direction. Thus (4) is a robust reserved/available-pool repair,
not a full-pool compensation counterexample or a new numerical grid bound.

For completeness the base reachability used above is explicitly recorded
by the verifier from actual terminals; the alpha-reachable owner set is
exactly the alpha and the owner containing BP (5,3), in BOTH root
orientations. In the original orientation the latter's support excludes
R; after flipping it includes R. This finite base identity, together with
the separated-copy construction, establishes (4) for every q.

## 6. Verification, scope and next geometry

Run:

    python3 develop/check_pinwheel_two_track_switches.py --output output/pinwheel-two-track-switches-validation.json

The standard-library checker reconstructs all physical original resource
identities, exact owner bodies and stub/tail supports after every tested
direction choice. It compares the joint switch flow against all 2^q
actual orientation assignments, then lifts its selected physical links
to the chosen actual partition. Independent terminal matching enumeration
checks the base controls. Additional abstract systems test shared original
resources, interacting switches, old self-links and existing beta gates;
these test the network theorem, not new physical realizations.

The passing receipt covers 18 physical controls, 30 pinwheel occurrences,
26 two-mixed switches, 70 actual orientation assignments, 140 joint
available-pool comparisons, 7,168 independently enumerated terminal
matchings and 660 strict-rank events. All 30 subsets in the q=1..4 sharp
family controls satisfy (4). A further 320 abstract interacting switch
systems pass 1,490 independent fixed-orientation comparisons, including
the per-flip value bound and actual terminal-link lifts.

The companion [Lean source](../formal/SubQuorum/PinwheelTwoTrackSwitches.lean)
checks the 16-case pinwheel classification, two-by-two partial matching
extension and the local cut repair underlying (3), plus count arithmetic.
The geometric stub/resource adapter, general integral-flow equivalence,
all-q separated-copy assembly and arbitrary graph min-cut application
remain written proofs, supported by executable physical controls. They
are not claimed end-to-end Lean formalizations.

The theorem requires exact occupied degree three, a uniform background,
and TWO ORIGINAL MIXED owners at every selected root. It does not handle
beta tracks joining different roots, arbitrary occupied-band interfaces,
or degree-four repeated-owner tiles. Those are genuine next cases. The
remaining donor-coverage problem is still to pay all original sources
from jointly unused credit on general complete resource cuts.
