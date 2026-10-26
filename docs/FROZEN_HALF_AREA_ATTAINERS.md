# Completely frozen half-area attainers with the old matching retained

27 October 2026. Wenlin Zhang and Haobo Ma. Research continuation.

Complete freezing does not restore the additional unit of reserve after the
terminal guard becomes optional. We give an explicit completely frozen
half-area attainer for every length. It retains every old matching edge.
A sharp terminal-port criterion restores the unit of reserve exactly when
the terminal vertical edge is forbidden. The construction proof uses two
freezing waves through a fully occupied lower row and a return wave through
the old cores. An explicit strict-rank certificate covers
every endpoint; finite discovery is not needed to justify the construction.

## 1. Exact statement

Use the board, old configuration (T0,M0), P0=V(M0), and retained set R'' of
[the terminal-guard theorem](TERMINAL_GUARD_HALF_AREA_FRONTIER.md). The board
is {0,...,5} x {0,...,6m+9}, m>=2. Retained selections are

    R''={(0,c): c odd, 1<=c<=6m+9}
         union {(1,2)} union {(1,4+6j),(1,8+6j):0<=j<=m}
         union {(2,0),(3,1)}.

The previous theorem proves J=|T|+|M|<=18m+30 for every feasible actual
matching with R'' subset T and P0 subset P, without assuming freezing.

**Theorem.** For every m>=2 there is a feasible, completely frozen
configuration satisfying

    T intersect T0=R'',  M0 subset M,
    |T|=9m+21,  |M|=9m+9,
    J=18m+30=area/2.                                 (1)

More precisely, for any completely frozen configuration under these
permissions, put epsilon=1 if the ACTUAL edge (3,c)--(4,c) belongs to M,
and epsilon=0 otherwise, where c=6m+9. Then

    J <= 18m+29+epsilon.                             (3)

The bound is sharp for each epsilon in {0,1} and every m>=2, with M0 retained
in both attaining families. Thus omitting the terminal vertical edge suffices
to restore the one-unit reserve, even without retaining the old terminal
selection. Section 5 proves this criterion for arbitrary actual rematching.

Consequently the exact maximum is half-area even in the subclass that
retains M0 and requires complete freezing. In particular a positive uniform
reserve after paying the strip deficit is false in this class. This is not
a counterexample to the half-area upper bound or to a universal 5/6 theorem.

## 2. Construction and feasibility

Put c=6m+9 and n=3m+2. Define

    T=R'' union {(2,3),(3,3),(4,0),(4,2),(4,4),(5,1),(5,3)}
          union {(2,9+6i):0<=i<=m}
          union {(5,5+2l):0<=l<=n}.

The last bottom selection has column 5+2n=c. Set

    M=M0
      union { (2,5+6j)--(3,5+6j):0<=j<=m }
      union { (3,9+6i)--(3,10+6i):0<=i<m }
      union { (3,c)--(4,c) }
      union { (4,5+2l)--(4,6+2l):0<=l<n }.            (2)

For reference, name the old core vertices for 0<=j<=m by

    A_j=(1,5+6j), B_j=(1,6+6j), C_j=(1,7+6j), D_j=(2,7+6j),
    E_j=(2,6+6j), F_j=(3,6+6j), G_j=(3,7+6j), H_j=(3,8+6j).

The old matching is {A_j B_j,C_j D_j,E_j F_j,G_j H_j:0<=j<=m}
plus (1,1)--(2,1). Thus (2) visibly retains M0. Write

    U_j=(2,5+6j), V_j=(3,5+6j),
    g_i=(3,9+6i)              (0<=i<=m),
    b_i=(3,10+6i)             (0<=i<m),
    Z_l=(4,5+2l), K_l=(4,6+2l) (0<=l<n), Q=(4,c).

The new edges are U_j V_j, g_i b_i (i<m), g_m Q, and Z_l K_l.
Their coordinate residues show that all new endpoints are distinct and
avoid P0. All edges are grid edges and avoid T. In particular g_i are
endpoints, not restored selections; no old optional selection is retained.

Here are explicit selected-neighbour checks for every family in T. Selections
in R'' have their old occupation neighbourhoods: the new available set has
no edge to R''. The new pair (2,3),(3,3) sees only each other. The sites
(4,0),(4,2),(5,1),(5,3) have no occupied neighbours. The site (4,4) sees
only Z_0=(4,5). Each (2,9+6i) sees only g_i. Each bottom selection
(5,5+2l), 0<=l<n, sees only Z_l; the last one (5,c) sees only Q.
All other neighbours in these lists are blank, as follows directly from (2)
and T. This proves feasibility for every m, not only sampled lengths.

There are 5m+10 retained selections, seven exceptional new ones, m+1 new
row-two selections and n+1=3m+3 new bottom selections. Hence |T|=9m+21.
The matching counts are

    |M|=(4m+5)+(m+1)+m+1+n=9m+9.

These counts prove (1) once complete freezing is established.


The endpoint geometry can also be stated without matching names:

| Board row | Endpoint columns |
| --- | --- |
| 0 and 5 | none |
| 1 and 2 | {1} union {5+6j,6+6j,7+6j:0<=j<=m} |
| 3 and 4 | every column from 5 through c |

Thus the construction has two entire adjacent rows of endpoints over an
arbitrarily long band. Complete freezing of this occupied band is proved
below, rather than assumed from its density or matching coverage.

## 3. What the strict-rank certificate means

An endpoint v freezes when it has two distinct adjacent kept sites. A site
is kept if it is selected, or if it is an endpoint whose ACTUAL mate has
already frozen. Thus it is enough to assign a nonnegative integer rank r(v)
to every endpoint, and for each v give two distinct adjacent sites a,b,
neither its own mate, such that each witness is selected or is an endpoint
whose mate has rank strictly smaller than r(v).

Induction on rank then freezes every endpoint. At rank zero both witnesses
must be selected; at higher rank all earlier mates have already frozen.
The induction does not assume that the old endpoints are frozen in advance,
and never uses an endpoint as its own earlier justification.

## 4. Explicit witnesses and ranks for every length

Define h_j=n+1+6(m-j), 0<=j<=m. The following table lists every endpoint
exactly once. The entries in the final column are neighbouring SITES; the
rank comparison is with each site's mate when that site is an endpoint.

| Endpoint | Range | Rank | Two neighbouring witnesses |
| --- | --- | ---: | --- |
| (1,1) | one site | 0 | (0,1), (1,2) |
| (2,1) | one site | 0 | (2,0), (3,1) |
| A_j | 0<=j<=m | 0 | (0,5+6j), (1,4+6j) |
| C_j | 0<=j<=m | 0 | (0,7+6j), (1,8+6j) |
| E_j | 0<=j<=m | 1 | B_j, D_j |
| G_j | 0<=j<=m | 2 | D_j, F_j |
| g_i | 0<=i<=m | 3 | (2,9+6i), H_i |
| V_j | 1<=j<=m | 4 | b_(j-1), F_j |
| V_0 | one site | n+4 | F_0, Z_0 |
| Z_0 | one site | 0 | (5,5), (4,4) |
| Z_l | 1<=l<n | l | (5,5+2l), K_(l-1) |
| Q | one site | n | (5,c), K_(n-1) |
| K_l | 0<=l<n | n+3-l | (3,6+2l), (4,7+2l) |
| H_j | 0<=j<=m | h_j | g_j, K_(3j+1) |
| F_j | 0<=j<=m | h_j+1 | G_j, K_(3j) |
| D_j | 0<=j<=m | h_j+2 | E_j, G_j |
| B_j | 0<=j<=m | h_j+3 | C_j, E_j |
| U_j | 0<=j<=m | h_j+4 | A_j, E_j |
| b_i | 0<=i<m | n+6(m-i) | V_(i+1), K_(3i+2) |

All coordinates in the table are in the board. Distinctness and adjacency
of the two witnesses, and their difference from the endpoint's own mate,
follow by substituting the displayed coordinates and matching (2).
Here are all the rank comparisons, grouped by the induction they implement.

First A_j,C_j and the isolated left pair have two selected witnesses.
E_j uses the mates A_j,C_j of B_j,D_j, both rank zero. G_j uses C_j and
E_j of ranks zero and one. Each g_i uses its selected upper neighbour and
mate G_i of H_i, of rank two. Each V_j for j>=1 uses g_(j-1) and E_j,
of ranks three and one. V_0 uses E_0 and K_0, whose ranks are 1 and n+3,
both smaller than n+4.

The lower white wave starts at Z_0, using the selected left neighbour (4,4)
and selected bottom neighbour (5,5). Each subsequent Z_l uses its selected
bottom neighbour and K_(l-1), whose mate Z_(l-1) has rank l-1. Q then uses
its selected bottom neighbour and K_(n-1), whose mate has rank n-1<n.

The lower black wave starts from the right. The upper witness (3,6+2l)
of K_l is F_j if l=3j, H_j if l=3j+1, and b_j if l=3j+2. Its mate is
respectively E_j,G_j,g_j, of rank 1,2,3. These indices include F_m,H_m
but no nonexistent b_m, since l<n=3m+2. The right witness is Z_(l+1)
when l<n-1, whose mate K_(l+1) has rank n+2-l<n+3-l. At l=n-1 it is
Q, whose mate g_m has rank three, less than rank K_(n-1)=4. Every upper
witness likewise has mate rank at most three. This proves the black wave.

Finally the remaining white endpoint wave returns through the old cores,
from j=m down to zero. At H_m, mate(g_m)=Q has rank n<h_m=n+1.
For j<m, mate(g_j)=b_j has rank n+6(m-j)=h_j-1. The other witness
K_(3j+1) has mate Z_(3j+1), of rank 3j+1<=n-1<h_j.
At F_j the witness mates are H_j and Z_(3j), of ranks h_j and 3j.
At D_j they are F_j,H_j; at B_j they are D_j,F_j; at U_j they are
B_j,F_j. All have smaller ranks than their listed endpoint. At b_i the
mates are U_(i+1), with rank

    h_(i+1)+4 = n+6(m-i)-1,

and Z_(3i+2), of rank 3i+2<n. Both precede b_i. This also explains the
next return-wave step at H_i. These comparisons exhaust the table.

Every endpoint therefore freezes by the rank induction. The largest listed
rank is r(U_0)=h_0+4=9m+7. Hence the certificate proves freezing in at most
9m+8 synchronous rounds, if round one freezes rank-zero endpoints. We do
not need an exact minimal-depth theorem for the sharpness result.

## 5. A sharp terminal-port compensation criterion

This argument concerns ANY half-area equality configuration under the retained
set R'', with any actual matching. The prior equality theorem gives the unique
terminal occupation pattern and the forced blanks from retained selections.
Name these sites:

    g=(3,c), Q=(4,c), K=(2,c), y=(4,c-1), A=(4,c-2),
    G=(3,c-2), H=(3,c-1), x=(4,c-3), Z=(4,c-4), F=(3,c-3).

Here G,H,F are old endpoints; g,x,y are not selected; A,Q,K are occupied;
(5,c-2),(5,c) are selected; (5,c-3),(5,c-1),(2,c-1),(1,c) are blank.
The previous block gives occupied Z; the conclusion xZ in the actual matching
below will force Z to be an endpoint. All mate choices below use the ONE
actual matching, so a site already paired elsewhere cannot be reused.

We repeatedly use the following elementary trap principle. If a nonempty
set S of endpoints has, at each member, at most one possible kept neighbour
whose mate lies outside S (count selected neighbours as outside support),
then no member of S can freeze. At the first layer meeting S, every neighbour
whose mate is in S is unavailable, leaving at most one witness. This contradicts
the requirement of two distinct witnesses. The same proof uses a minimum
strict rank if a rank certificate is supplied.

First g cannot be blank. If g were blank and Q an endpoint, Q would have to
pair with y, since its other neighbours are g and selected (5,c). Then Q
has just one usable nonmate neighbour, (5,c), and can never freeze. If Q
were selected, its selected bottom neighbour would force y blank. H would
then have only G as an eligible endpoint neighbour, so GH would be forced
and H could never freeze. These cases exhaust occupied Q.

Thus g is an endpoint. Its only possible mates are K,H,Q. If g pairs with
K, the endpoint K has only its mate as an occupied neighbour, so cannot
freeze. If g pairs with H, K must be selected, since its only possible mate
is already used. Q cannot be selected (it sees both g and its selected bottom
neighbour), so it is an endpoint paired with y. Now S={Q,H} is a trap:
Q has only its selected bottom neighbour outside S in the mate sense, while
H has only G as possible outside support; the y and g neighbours have mates
in S. Therefore this choice also prevents complete freezing. The only
remaining choice is

    gQ in M,  K in T.                               (4)

This already proves the needed terminal-port criterion. There is some extra
local rigidity useful for subsequent work. Q needs a second kept neighbour
besides selected (5,c), so y must be an endpoint. Its only available mates
are A,H (Q is already paired). If y pairs with H, the same trap S={Q,H}
applies: Q needs H to freeze earlier, while H needs Q earlier. Hence Ay
is forced. Covering H then forces GH. Further, A cannot freeze without
support from x before the mutually dependent Q,H can support it. If x
were blank, S={A,Q,H} would be a trap: A and Q each have only their
selected bottom neighbour as outside support, while H has none. Thus x is an endpoint and its only
available mates are F,Z. The choice xF gives the trap S={x,G,y,g}:

| Member | Neighbours with mates in S | At most one outside support |
| --- | --- | --- |
| x | F (mate x), A (mate y) | Z |
| G | F (mate x), H (mate G), A (mate y) | its upper old endpoint |
| y | A (mate y), H (mate G), Q (mate g) | none |
| g | H (mate G), Q (mate g) | selected K |

Therefore every completely frozen equality board actually has all four edges

    gQ, Ay, GH, xZ in M, and K in T.                 (5)

These are necessary local conditions, not a claimed classification of the
whole equality matching. The fixed local cases use the coordinate neighbours
above and the trap principle, not a finite exhaustive search as proof.

To prove (3), start with the unconditional upper bound J<=18m+30.
If epsilon=0, (4) excludes equality and integrality gives J<=18m+29.
If epsilon=1, use the unconditional bound. The family in Sections 2--4
attains the epsilon=1 value. The [earlier all-subset frozen attainer](SELECTION_WITHDRAWAL_SHARP_STRIPS.md#4-an-all-subset-frozen-attainer-with-no-circular-freezing) retains
the terminal old selection, has J=18m+29 and epsilon=0, and retains M0.
This proves sharpness for both values, for every length.

For a unified compensation inequality, (3) gives

    Cplus >= Cminus+m+2(1-epsilon).                 (6)

Allocate exterior negative demands first and strip demands second from the
single set of distinct original positive tokens. At least 2(1-epsilon)
tokens remain, and no token allocated to either demand set is counted as
reserve. The next section describes the zero-reserve equality case explicitly.

## 6. Physical compensation and the obstruction to a positive reserve

For aligned original 2x2 tiles use charge(Q)=4-2|T intersect Q|-|P intersect Q|.
Equation (1) gives whole-board charge zero. The unchanged upper occupied
strip has charge -m. Consequently exterior positive half-unit tokens and
exterior negative demands satisfy exactly

    Cplus=Cminus+m.

Allocate the first Cminus distinct positive tokens to exterior negative
charges and the next m to strip demands. No token is reused and none remains.
Thus even completely frozen configurations retaining M0 can exhaust the
entire compensation budget. Complete freezing cannot be used as a substitute
for an additional, proved source of reserve under these permissions.
There is also an explicit payment map on every original tile, with no search
for a suitable donor. With tile coordinates denoting their top-left SITE,
the complete nonzero charge table is

| Tile top-left | Charge | Range |
| --- | ---: | --- |
| (0,0) | +1 | one tile |
| (0,4+6j) | -1 | 0<=j<=m |
| (2,0) | -1 | one tile |
| (2,4) | +2 | one tile |
| (2,4+6j) | +1 | 1<=j<=m |
| (4,4) | -1 | one tile |

All other aligned tiles have charge zero, by substitution of T and P by
column residue. Pay (0,4) using the token of (0,0). Label the two tokens of
(2,4) distinctly and use them for (2,0) and (4,4), respectively. For each
1<=j<=m use the token of (2,4+6j) for (0,4+6j). This is one explicit
bijection from all m+3 positive half-unit tokens to all m+3 negative demands.
In particular the two-token tile (2,4) is already fully spent on the two
exterior negatives; counting it again as a strip reserve would double-use
its entire charge.

The earlier extra-unit theorem remains correct when its terminal guard is
retained. The construction identifies that boundary hypothesis as essential
for its positive margin, including in the completely frozen subclass.

The result is an aggregate original-tile budget, not a geometric routing
certificate and not a universal improvement or refutation of the 5/6 bound.
The terminal-port exclusion above is one precise condition preventing this
saturation mechanism and preserving positive margin. For other endpoint
footprints the next task is to derive the corresponding forced ports and
state potentials, then combine their demands in a single nonreuse ledger.

## 7. Verification scope

The standard-library verifier generates the construction and independently
checks actual edges, selected degrees, retained old edges, all strict-rank
witnesses, complete synchronous freezing, the inherited local upper-bound
certificates and physical token allocation. It also transports the certificate
through the eight grid isometries for three representative lengths.
The construction and general rank argument above supply the all-length proof.
Finite optimization was used to discover the family; replaying its verification
requires no optimization package.

The Lean audit covers the generic well-founded rank implication and universal
rank arithmetic for the displayed families. Coordinate-to-graph membership,
matching disjointness, witness adjacency and selection, and the full graph
adapter remain written proofs with independent executable checks. We do not
claim an end-to-end Lean grid theorem.


Reproduction from the repository root:

    python3 develop/check_frozen_half_area_attainers.py --output output/frozen-half-area-attainers.json
    python3 develop/check_frozen_half_area_attainers_formal.py --output output/frozen-half-area-attainers-formal.json

The saved exact run checks 41 half-area frozen lengths and 41 inherited
no-port frozen sharp lengths through m=100, 24 isometry controls, 20,736
strict-rank endpoint events, 41 complete physical token bijections and 82
aggregate token allocations. Seventeen local terminal matching models have
sixteen explicit trap certificates and one optimistically freezable pattern,
which forces the four displayed edges. These local checks verify the case
proof and do not replace it. The certificate bound is 9m+8 rounds; exact
minimal depth is observed in the sampled new family only.

The [first independent Oracle review](../output/frozen-half-area-attainers-oracle.json)
accepts the all-length construction, actual-mate ranks and exact tile-token
bijection, with the preceding half-area upper bound as premise. It does not
execute Python or Lean and precedes the added terminal-port criterion.


The local [Lean audit](../output/frozen-half-area-attainers-formal.json) passes
24 declarations using Lean 4.33.0. Besides the rank and counting arithmetic,
it proves the generic strict-rank implication and generic trap exclusion for
the least freezing closure. It does not instantiate the coordinate graph;
the latter adapter is covered by the written proof and executable witnesses.


The [second independent Oracle review](../output/frozen-terminal-port-oracle.json)
accepts the added terminal-port proof, all four forced edges and the sharp
parameterized compensation inequality, using the prior half-area/equality
facts and previously accepted constructions as premises. Its optional request
to specify the exact outside supports in the three-endpoint trap has been
incorporated. It does not execute the validators.
