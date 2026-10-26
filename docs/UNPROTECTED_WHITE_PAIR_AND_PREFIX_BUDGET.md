# Unprotected white selections, sharp terminal cost and a prefix obstruction

Successor: [arbitrary-selection colour switch](ARBITRARY_SELECTION_COLOUR_SWITCH.md) removes the black-selection restriction under retained P0 and proves the sharp whole-board half-area bound.

27 October 2026. Wenlin Zhang and Haobo Ma.

The two bottom white sites in the previous whole-board endpoint theorem need
not be prohibited from the selected set. Selected degree and actual mates
together imply the SAME joint capacity, so the sharp half-area bound holds
with arbitrary white selections under the occupied-anchor/black-selection
skeleton. We give an unchanged-rank fully frozen equality family selecting
both previously prohibited white sites. Selecting the single permitted new
black terminal has exact cost one, with a fully frozen all-length attainer.

For new black selections, we prove a disjoint periodic six-hole budget and
exhibit a real all-length obstruction to sealing the remaining left prefix:
its nine selected black sites face only eight of its allowed white holes,
while the whole board is at exact half-area. The missing hole is the single
physical exterior site (5,4). This refutes the proposed independent prefix
rule, not the global target or its completely frozen version.

## 1. Exact hypotheses and capacity without protected white sites

Let R={0,...,5} x {0,...,c}, with c odd and c>=5. Grid edges have L1 distance
one. M is an actual matching, P its endpoint set, T is disjoint from P,
O=T union P and H=R minus O. Every selected site has at most one occupied
neighbour. Black means even coordinate sum. Retain the previous sufficient
skeleton:

    T_black subset Bstar,
    Bstar={(2,0),(3,1),(3,3),(4,0),(4,2),(4,4),(5,1),(5,3)}
           union {(5,k):k odd,5<=k<=c};
    (2,1) and (4,k) for every odd k>=5 are occupied.

There is now NO restriction on where white sites can be selected, apart from
feasibility. New endpoints and actual rematching are unrestricted as before.

Write r_site=(5,0), s_site=(5,2), and name their black neighbours

    d=(4,0), e=(4,2), g=(5,1), h=(5,3).

Their complete neighbour sets are N(r_site)={d,g} and N(s_site)={e,g,h}.
Let D count selected sites among d,e,g,h, and let r,s be the indicators that
r_site,s_site are genuinely EMPTY. Then, for EVERY feasible actual matching,

    D <= 2+r+s.                                             (1)

Unlike the earlier proof, an occupied r_site or s_site need not be an endpoint.
We must treat selected white sites as well.

**Structural proof.** If both white sites are empty, D<=4 suffices. If exactly
one is occupied, D=4 is impossible: the occupied site could neither be selected
(it has at least two occupied selected neighbours) nor be an endpoint (all its
possible mates are selected). Thus D<=3.

Suppose both white sites are occupied and D>=3. The common neighbour g cannot
be selected, since it would have two occupied neighbours. Hence d,e,h must all
be selected. The white s_site sees selected e,h, so cannot be selected itself;
it must be an endpoint, whose only possible mate is g. Thus g is occupied.
Now r_site sees occupied d,g, so it cannot be selected either. It too must be
an endpoint with only g as possible mate, since d is selected. Two actual
matching endpoints cannot share g. This contradiction proves D<=2, and (1).
No freezing, old matching, or local colour-balance assumption is used.

This argument identifies precisely where selection replaces endpoint status:
when a white site becomes selected, its own degree constraint restricts its
neighbours. It cannot be treated as a freely deleted endpoint demand.

## 2. Extended half-area theorem and sharp fully frozen witnesses

Use the eight black pocket selectors and nine white EMPTY indicators from
[the preceding note](WHOLE_BOARD_ENDPOINT_INVASION.md). Its degree inequalities
remain valid when r_site or s_site is selected: the variables r,s mean empty,
not unselected. Equation (1) supplies exactly its missing joint constraint.
The preceding four-case algebraic pocket proof therefore applies unchanged.
The tail selections (5,k) are still paid by different forced empty sites
(5,k-1), disjoint from the nine pocket sites. Consequently

    card(T_black) <= card(H_white),
    J=card(T)+card(M) <= 3(c+1)=area/2.                       (2)

The unchanged three-term nonnegative slack identity from the preceding note
also holds. Thus the two protected-white assumptions can be removed entirely
from that sufficient skeleton. Black selection locations and occupied anchors
are still hypotheses. This is not a theorem for arbitrary selections yet.

For c=6m+9, m>=2, start with the established fully frozen pair (T0,M0), and put

    T'=(T0 minus {(5,1),(5,3)}) union {(5,0),(5,2)}, M'=M0.    (3)

The new white selection (5,0) has just the occupied neighbour (4,0); the new
white selection (5,2) has just (4,2). Both old selections (4,0),(4,2) previously
had no occupied neighbour and now have exactly one. Other selected degrees
are unchanged or decrease. Hence (3) is feasible. Its objective stays
18m+30=area/2, and P0 is unchanged.

Every witness site in the original strict actual-mate rank certificate remains
selected or has the same actual mate and rank: neither removed site (5,1) nor
(5,3) is used as a selected witness. Therefore the SAME complete rank table
proves that (3) is fully frozen for every m. No search, new rank ansatz or
external grant is required. This proves sharpness with BOTH formerly forbidden
white sites selected, not just hypothetical admissibility.

## 3. A sharp one-unit cost for a selected terminal black site

Allow black selections in Bstar union {v}, where v=(1,c), and REQUIRE v in T.
White selections remain arbitrary. Keep the same occupied anchors as Section 1.
The only three board neighbours of v are the WHITE sites

    X={(0,c),(1,c-1),(2,c)}.

At least two sites of X must be genuinely empty, by the selected-degree
condition. X is disjoint from the nine old white pocket sites AND the bottom
hole set L. The preceding pocket and tail proofs apply to all black selections
except v, and use only their own disjoint hole sets. Hence

    card(H_white) >= card(T_black minus {v})+2
                  = card(T_black)+1,
    J <= area/2-1.                                         (3a)

This is a global joint count: the two terminal holes are not also charged to
the old pocket or tail. It needs neither complete freezing nor prescribed
mates. It is an exact maximum for this permissions class, as follows.

For c=6m+9, start from (T0,M0) and define

    T_v=(T0 minus {(0,c),(1,c-1),(2,c)}) union {(1,c)},
    M_v=M0 union {((2,c-1),(2,c))}.                         (3b)

The two added endpoints were respectively empty and selected; they do not
belong to P0. All original endpoints and all old matching edges remain. At
v its only occupied neighbour is (2,c). Other retained selections gain no
occupied neighbours: the new endpoint (2,c-1) only touches the withdrawn
(1,c-1) besides endpoints; (2,c) and v only touch withdrawn selections,
old endpoints or one another. Thus (3b) is feasible, with

    card(T_v)=9m+19, card(M_v)=9m+10,
    J_v=18m+29=area/2-1.

Here is the complete modification of the established baseline strict-rank
certificate, proving fully frozen sharpness for ALL m. Write n=3m+2 and
use its usual core labels, with A_m=(1,c-4), B_m=(1,c-3), C_m=(1,c-2),
D_m=(2,c-2), E_m=(2,c-3), F_m=(3,c-3), G_m=(3,c-2),
H_m=(3,c-1), g_m=(3,c), Q=(4,c). The added black endpoint is d*=(2,c-1),
and its white mate is f*=(2,c). Keep every original WHITE endpoint rank and
witness. Give f* rank n+1 with witness sites selected v and g_m; the actual
mate of g_m is Q, whose white rank is n.

For BLACK endpoints, keep all old ranks and witnesses except:

| Endpoint | New rank | Witness sites |
| --- | ---: | --- |
| C_m | 1 | selected (0,c-2), B_m |
| E_m | 2 | B_m,D_m (old witnesses) |
| G_m | 3 | D_m,F_m (old witnesses) |
| added d* | 4 | D_m,H_m |
| g_m | 5 | f*,H_m |
| every K_l=(4,6+2l) | old rank +2 | old witnesses |
| V_0=(3,5) | old rank +2 | old witnesses |

The mates along the first five rows are A_m of rank 0; A_m and C_m;
C_m and E_m; C_m and G_m; and d* and G_m, respectively. Every comparison
is strict. The terminal K_(n-1) depends on G_m and g_m, now ranks 3 and 5,
and has new rank 6. For every other K_l the old actual-mate dependency
increases by at most 2, so adding 2 to its own rank preserves strictness.
The only other affected old black dependency is V_0 through K_0; shifting
V_0 by 2 suffices. V_j for j>=1 depends on g_(j-1), which is unchanged,
so those ranks remain valid. No original white witness uses any removed
white selection, and the other black witness sites are unchanged. This covers
EVERY actual endpoint. The maximum rank remains at most 9m+7, hence at most
9m+8 synchronous rounds suffice; no minimal-depth claim is made.

Therefore (3a) is sharp even under complete freezing. This does not assert
a one-unit loss for arbitrary simultaneous new black selections. In particular
allowing additional top black selections can make them share the same terminal
holes; those overlaps must be counted jointly, as in the next section.

## 4. A disjoint periodic budget for new black selections

Keep P0 of the original family but now consider arbitrary new selections.
A site with two retained P0 neighbours cannot be selected. By the explicit
row table for P0, all possible new black selections outside Bstar lie in

    row 0 at even columns;
    row 1 at columns 3,9,15,...,c;
    (2,2),(2,4).

For a=4+6j, 0<=j<=m, group

    A=(0,a), B=(0,a+2), C=(0,a+4), D=(1,a+5),

and six possible white holes

    u=(0,a+1), v=(1,a), w=(0,a+3),
    x=(0,a+5), y=(1,a+4), z=(2,a+5).

Reuse the letters for Boolean selection/empty indicators. Feasibility and
retained (1,a+2) imply

    A<=u+v; B<=u,w; 2C<=w+x+y; 2D<=x+y+z.                  (4)

At A we omit its exterior left neighbour; at D we omit its possible right
neighbour. These weaken the degree conditions. The last D is at the right
boundary and still has the three displayed neighbours, so (4) holds there too.

The binary inequalities (4) imply

    A+B<=u+v+w, C+D<=x+y+z,
    A+B+C+D<=u+v+w+x+y+z.                                 (5)

For the first inequality, B=0 uses A<=u+v, and B=1 forces u=w=1 and uses
A<=1. For the second, C=1 forces x+y>=1 because w<=1; D=1 requires two
blanks among x,y,z. If their triple sum is 0 both selectors vanish, if it is
1 then D=0 and C<=1, and at sums at least 2 use C+D<=2. This proves (5).

Different j use disjoint hole coordinates and disjoint black selectors. Their
six-hole sets are also disjoint from the old nine-hole pocket and bottom tail.
The only new black positions left outside these blocks are

    (0,0),(0,2),(1,3),(2,2),(2,4).                         (6)

This is a useful all-length reduction, but simply combining (5) with a larger
independent left pocket is false, as the next explicit construction shows.

## 5. An all-length sharp obstruction to an independently sealed prefix

A natural attempted repair puts the old eight black pocket sites, the five
sites (6), and A,B from the first top block into one left prefix. Its black
positions are

    Bp=Bstar_pocket union
        {(0,0),(0,2),(1,3),(2,2),(2,4),(0,4),(0,6)}.

Its candidate white-hole positions are

    Wp=old_nine_white_sites union
        {(0,1),(0,3),(1,2),(0,5),(0,7),(1,4)}.

Both sets have size 15. The proposed bound is

    card(T_black intersect Bp) <= card(H_white intersect Wp). (FALSE)

For EVERY m>=2, c=6m+9, take just the following NINE black selections:

    T={(0,0),(0,2),(0,4),(1,3),(2,2),(2,4),(3,3),(4,4),(5,3)}.

Use six matching edges in columns 0,...,4:

    (1,1)--(2,1), (1,0)--(2,0), (3,0)--(4,0),
    (3,1)--(4,1), (4,2)--(5,2), (5,0)--(5,1).

For EVERY column k=5,...,c add three vertical matching edges

    (0,k)--(1,k), (2,k)--(3,k), (4,k)--(5,k).                (7)

All edges are disjoint and nearest-neighbour. The only original P0 sites left
of column 5 are (1,1),(2,1), covered by the first edge; all other original
endpoints lie in the fully matched columns k>=5. Thus P0 subset P.

The genuinely empty sites are EXACTLY the nine white sites

    H={(0,1),(0,3),(1,2),(1,4),(2,3),
        (3,2),(3,4),(4,3),(5,4)}.                          (8)

This follows directly by partitioning the 30 sites in the first five columns
into nine selected, twelve matching endpoints and nine empty; all other
columns are fully matched. Every selected site has zero or one occupied
neighbour: the respective occupied-neighbour counts in the displayed order
of T are 1,0,1,0,1,1,0,1,1. Hence this is a feasible ACTUAL matching.

Its counts are

    card(T)=9; card(M)=6+3(c-4)=3c-6;
    J=3c+3=18m+30=area/2.

Yet all nine selected sites lie in Bp, and precisely eight of (8) lie in Wp:

    card(T_black intersect Bp)=9,
    card(H_white intersect Wp)=8,
    H minus Wp={(5,4)}.                                   (9)

The exterior white hole (5,4) pays the single missing unit exactly once.
There is no second exterior hole to spend, and (5,4) is the FIRST hole of the
old bottom-tail budget. Charging it once to this prefix and again to another
region would double count. This is an explicit all-length example at GLOBAL
equality, rather than a loose local pattern or a low-objective finite board.

The example is not frozen. Every matching endpoint has at most one selected
neighbour, so no first freezing event occurs. In particular the retained
endpoint (1,1) has only two occupied neighbours, including its own mate (2,1),
and is a singleton trap. This leaves the fully frozen prefix inequality open;
finite searches do not establish it. Nor does (9) refute the global half-area
target, which the example attains exactly.

The 15-by-15 candidate prefix is not a union of original 2x2 physical tiles.
Its imbalance is a boundary-budget failure, not a new negative total tile
charge. Every aligned tile actually has charge ZERO: its (selected count,endpoint
count) is (0,4), (1,2), or (2,0). For the three pairs of rows, the left two
tiles have these types respectively (1,2)/(2,0), (0,4)/(2,0), and
(0,4)/(1,2); the column-4 tile always has (1,2), and all later tiles have
(0,4). Thus the candidate prefix imbalance is not a physical negative tile
that can be billed to an existing positive tile. A valid new-black
proof must preserve boundary flow/empty-site identities or use a frozen
obstruction; it cannot assume each such prefix pays itself.

## 6. Verification and remaining scope

The all-length arguments are the structural cases proving (1), reuse of the
written pocket proof, disjoint coordinates in (5), the unchanged rank
certificate for (3), and explicit formulas (7),(8). Enumeration is used only
to check these proofs and discover candidate rules.

The standard-library verifier checks all 379 feasible six-site projections,
including selected/endpoint white mixtures and optimistic distinct exterior
mates for black sites. It checks 354 binary top-block models, 105 generalized
whole boards, 41 frozen sharp white replacements plus 41 frozen sharp new-black terminal
constructions, with 36,946 strict-rank events, and 41 prefix obstructions at lengths through m=100. It also checks the terminal upper bound on 105 boards, including 64 actual
rematchings that change old edges. The saved receipt states exact coverage. Coordinate verification uses independent synchronous
and queue freezing checks.

Seven local Lean 4.33.0 declarations verify the selected/occupied/actual-mate
projection, the two-white capacity without a white-selection prohibition,
the top-block inequality and the disjoint terminal one-unit budget arithmetic. They use no sorry or nonstandard axioms and
pass without warnings. Every Lean invocation is preceded by local memory and
comm-basename process checks. The full coordinate adapter, unchanged frozen
rank family and explicit prefix matching remain written proofs with executable
controls; no end-to-end Lean grid theorem or CI result is claimed.

Run

    python3 develop/check_unprotected_white_pair.py --output /tmp/white-pair.json
    python3 develop/check_unprotected_white_pair_formal.py --output /tmp/white-pair-formal.json

See [Lean source](../formal/SubQuorum/UnprotectedWhitePair.lean),
[coordinate receipt](../output/unprotected-white-pair.json) and
[formal receipt](../output/unprotected-white-pair-formal.json).

The specified single-terminal black permission is settled by (3a),(3b).
With arbitrary black AND white new selections under retained P0, the global
half-area target is still open. Finite optimizations at m=2,3,8 support it but
do not prove it; [discovery statuses and exact scopes](../output/unprotected-white-pair-discovery.json)
are recorded separately from proof verification. At m=2 a frozen search with some new black selection found
maximum 65 rather than 66; that is a finite observation, not a general
one-unit loss theorem. The unrestricted prefix failure (9) does not settle
the completely frozen case. The universal 5/6 improvement remains open.

Independent broker review of the white-selection extension, periodic budget and
prefix obstruction is pending at this publication; its submitted text predates
Section 3. The terminal theorem has the written proof and local executable/Lean
checks stated above, with no independent Oracle acceptance claimed. A separate
live proof-assistance request concerns the still-open arbitrary-selection target.
