# Two boundary inputs activate an arbitrarily long rematching chain

27 October 2026. Wenlin Zhang and Haobo Ma. Research continuation.

The preceding zero-charge cap activated a switch of two terminal matching
edges. Its effect is not confined to that terminal square. The SAME six-column
cap and SAME two occupied interface contacts activate a rematching through
every core of an arbitrarily long occupied band. Precisely 8m+7 prescribed
edges disappear, while the selected and endpoint sets, local half-area,
matching closure and complete freezing of the union are retained.

We prove the exact four-state local response. One input unlocks a two-endpoint
trap, the other a trap of 9m+7 endpoints. This separates boundary input count
from rematching extent and physical surplus: both inputs are necessary, their
number stays two, and no physical token is left unspent. This is an explicit
family, not a classification of every feasible matching on this footprint.

## 1. Construction and statement

Use the board R, T*, P*, names and original prescribed matching M* from
[the frozen half-area construction](FROZEN_HALF_AREA_ATTAINERS.md). Put

    c=6m+9, n=3m+2, m>=2,
    R={0,...,5} x {0,...,c}.

Write e_left=(1,1)--(2,1). Define a new actual matching by the following
DISJOINT edge list, with no changes to T*:

    Mz = {e_left}
       union {E_j F_j, A_j U_j, B_j C_j, D_j G_j, H_j g_j:0<=j<=m}
       union {V_0 Z_0}
       union {b_i V_(i+1):0<=i<m}
       union {K_l Z_(l+1):0<=l<n-1}
       union {K_(n-1) Q}.                            (1)

Every edge is a grid edge. Every named endpoint appears exactly once: the
core part covers A,B,C,D,E,F,G,H,U,g; V_0 is paired below, V_j for j>=1 is
paired to b_(j-1), Z_0 is paired above, and the remaining lower row is covered
by the shifted K_l pairs. Thus V(Mz)=P*. Since T*/P* is unchanged, feasibility
is inherited for every m, without an enumeration premise.

The only common edges of Mz and M* are e_left and E_j F_j. Hence

    |Mz|=9m+9, |T*|=9m+21, J_R=18m+30=area(R)/2,
    |M* intersect Mz|=m+2,
    |M* minus Mz|=|Mz minus M*|=8m+7.                (2)

The new edge A_0 U_0 replaces A_0 B_0 in the leftmost core at column 5,
whose horizontal separation from the right boundary is c-5=6m+4. Thus both
the number and distance of changed edges are unbounded with two input ports.

Attach exactly the cap (T_C,M_C) of
[ambient band activation](AMBIENT_BAND_PORT_ACTIVATION.md), translated by
c+1. Keep its names p,a,q,b and its six early endpoints

    E_C={C0,A,Z,E,b,a}.

All interface feasibility checks are unchanged because T*/P* is unchanged.
Only g_m--p and Q--q join occupied sites across the seam. No actual matching
edge crosses it. The union has

    shape 6 x (6m+16), |T|=9m+32, |M|=9m+16,
    J=18m+48=area/2.                                (3)

The theorem below proves complete freezing, not just feasibility.

## 2. An all-length actual-mate rank certificate

The actual mates in this section are those of (1). A kept site is selected
or has its actual mate frozen. Consequently the table compares the ranks of
WITNESS MATES, never the ranks of the witness sites themselves.

First supply the outside site p=(3,c+1) as kept iff cap endpoint a has frozen,
and q=(4,c+1) iff cap endpoint b has frozen. Use the following ranks on R.
Put f_j=n+2+6j.

| Endpoint | Range | Rank | Two witness sites |
| --- | --- | ---: | --- |
| (1,1) | one | 0 | selected (0,1),(1,2) |
| (2,1) | one | 0 | selected (2,0),(3,1) |
| A_j | 0<=j<=m | 0 | selected (0,5+6j),(1,4+6j) |
| C_j | 0<=j<=m | 0 | selected (0,7+6j),(1,8+6j) |
| E_j | 0<=j<=m | 1 | B_j,U_j |
| V_j | 0<=j<=m | 2 | U_j,F_j |
| g_i | 0<=i<m | 3 | selected (2,9+6i),b_i |
| g_m | one | 3 | selected (2,c),outside p |
| G_j | 0<=j<m | 4 | F_j,H_j |
| G_m | one | n+3 | F_m,Z_(n-1) |
| K_l | 0<=l<n | 4+l | (3,6+2l),Z_l |
| Z_0 | one | 0 | selected (4,4),(5,5) |
| Z_l | 1<=l<n | n+2-l | selected (5,5+2l),K_l |
| Q | one | 2 | selected (5,c),outside q |
| F_j | 0<=j<=m | f_j | V_j,K_(3j) |
| U_j | 0<=j<=m | f_j+1 | E_j,V_j |
| B_j | 0<=j<=m | f_j+2 | A_j,E_j |
| D_j | 0<=j<=m | f_j+3 | C_j,E_j |
| H_j | 0<=j<=m | f_j+4 | G_j,K_(3j+1) |
| b_i | 0<=i<m | f_i+5 | g_i,K_(3i+2) |

All pairs are distinct adjacent sites and exclude the endpoint's own mate.
Here is a complete check of the dependencies for arbitrary length.

The witnesses for E_j have mates C_j,A_j of rank zero; those for V_j have
mates A_j,E_j of ranks zero and one. Internal g_i use mate V_(i+1) of rank
two, and g_m uses cap mate a of rank two. For j<m, G_j uses E_j,g_j of
ranks one and three.

For K_l, its upper witness has mate E_j if l=3j, g_j if l=3j+1, and
V_(j+1) if l=3j+2. These ranks are at most three. Its left witness Z_l has
mate V_0 of rank two at l=0 and mate K_(l-1) of rank 3+l at l>=1.
Thus every K_l comparison is strict. The exceptional G_m uses E_m of rank
one and K_(n-2) of rank n+2, both earlier than n+3. This witness choice is
important: G_m can freeze even when the p input is absent.

The white lower wave runs RIGHT TO LEFT, starting from Q of rank two.
Z_l for l>=1 uses site K_l, whose actual mate is Z_(l+1), or Q at the last
index. Its mate rank is n+1-l, one below n+2-l. The selected bottom site
supplies the second witness. Z_0 has two selected witnesses independently.

The remaining white wave runs LEFT TO RIGHT through the cores. At F_0,
site V_0 has mate Z_0 of rank zero. At F_j for j>=1, it has mate b_(j-1)
of rank f_j-1. The other witness K_(3j) has mate Z_(3j+1) of rank
n+1-3j<=n+1<f_j. Next U_j uses mates F_j and Z_0/b_(j-1); B_j uses
U_j,F_j; D_j uses B_j,F_j. At H_j, the mates are D_j of rank f_j+3 and
Z_(3j+2), or Q at j=m, of rank at most n+1. At b_i, the mates are H_i
of rank f_i+4 and Z_(3i+3), whose rank is at most n+1. This checks every
remaining row, including all terminal indices.

The cap's early ranks 0,1,2 and witnesses remain unchanged. Keep all cap
witness sites from the preceding note, but replace its late ranks by

    q:n+4, L:n+5, V:n+6,
    p:9m+9, F:9m+10, D:9m+11, B:9m+12, U:9m+13.    (4)

The two changed interface mate comparisons are exact: cap q uses inside
site Q, whose mate is now K_(n-1) of rank n+3; cap p uses inside site g_m,
whose mate is now H_m of rank f_m+4=9m+8. Its other witness has mate b of
rank one. The rest of the cap table then follows in its listed order.
In particular neither cap p nor cap q must itself freeze before R: R only
uses their mates a,b in the early cap set.

Every endpoint of the actual union has a valid strict-rank certificate,
of maximum rank 9m+13. Thus the union is completely frozen in at most
9m+14 synchronous rounds. This is a bound, not a minimal-depth assertion.

## 3. Exact four-state local interface

Call an endpoint black if its coordinate sum is even and white if odd.
A witness endpoint is the opposite colour from the endpoint it supports,
and its actual mate has that endpoint's colour. Hence freezing dependencies
preserve endpoint colour, even when sites of opposite colours touch.

Define

    Bz={g_m,K_(n-1)},
    Wz={all white endpoints of P*} minus {(2,1),Z_0},
    E_R=P* minus (Bz union Wz).                     (5)

There are 9m+9 endpoints of each colour, since the actual matching pairs
opposite colours. Thus

    |Bz|=2, |Wz|=9m+7, |E_R|=9m+9.                (6)

For I subset {a,b}, grant p kept exactly when a in I, and q kept exactly
when b in I. All other sites outside R remain unavailable. The EXACT local
least freezing closure is

    F_R(I)=E_R union (Bz if a in I) union (Wz if b in I).  (7)

For the positive inclusion, restrict the rank table to the indicated set.
All E_R witnesses have earlier mates inside E_R: in particular K_l for
l<n-1 never uses g_m, and G_m uses K_(n-2), not g_m. The only white
endpoints in E_R are the two rank-zero anchors. Adding a unlocks g_m,
then K_(n-1). Adding b unlocks Q, then the lower white wave and the entire
core return wave. All dependencies in that wave stay white; it does not
require completion of Bz. The rank table proves these inclusions for all m.

For the reverse inclusion, the complete maximal possible outside-trap support
lists, counted within R plus only its granted outside sites, are:

| Absent input | Trap | Endpoint | Possible selected / outside-trap-mate sites |
| --- | --- | --- | --- |
| a | Bz | g_m | selected (2,c) |
| a | Bz | K_(n-1) | Z_(n-1) |
| b | Wz | U_0,F_0 | V_0 |
| b | Wz | Z_l, 1<=l<n | its selected bottom neighbour |
| b | Wz | Q | selected (5,c) |
| b | Wz | all other members | none |

For Bz, the other local sites at g_m have mates g_m or K_(n-1), while
the upper site at K_(n-1) has mate g_m and its right site Q is its own mate.
For Wz, the only white endpoints outside it are (2,1) and Z_0. The former's
mate is not adjacent to Wz; Z_0's mate V_0 is adjacent exactly to U_0,F_0
among its members. Selected sites adjacent to Wz are precisely the bottom
selections below Z_l and Q. Every other endpoint neighbour has its actual
mate in Wz. The other input's granted site is not adjacent to a member of
this trap. These observations exhaust the table.

Each member has at most one such support, even if all endpoints outside
its trap are supplied frozen. A first-frozen-member argument excludes the
trap when its input is absent, proving (7). Therefore the numbers left
unfrozen in the four states are exactly

| Kept outside sites | Unfrozen endpoints |
| --- | ---: |
| none | 9m+9 |
| p only | 9m+7 |
| q only | 2 |
| p and q | 0 |

Thus two distinct inputs are necessary and sufficient for THIS matching.
This rematching does not need an increasing number of independent external
endpoints: the response region grows while the
input set stays fixed. No universal necessity theorem for other matchings
is being asserted.

## 4. Physical compensation and unbounded extent

The new matching preserves T*/P*, so every original tile charge and every
old payment identity is unchanged. The same cap has charge matrix

    -1  0  0
    +1  0  0
     0  0  0.

Its positive token pays its own negative demand. The complete union has
m+4 positive half-unit tokens paying exactly m+4 negative demands. Every
token is identified by its original physical tile and, at the +2 tile, its
separate index. No token is reused and no reserve remains. These are all-tile
counts, not the strip-exterior Cplus of the isolated-band inequality; no
geometric routing interpretation is claimed for the payment map.

Consequently there is no uniform constant bounding the number of missing
prescribed edges by the number of these input ports, nor a uniform radius
containing every changed edge around the ports. Both conclusions follow
directly from 8m+7 missing edges and a changed leftmost core at separation
6m+4, with exactly two inputs for every m. A proposed inequality charging
one reserve per missing edge, offset by any fixed cost per input port,
fails on this all-length family. This says nothing against the BINARY
isolated theorem under its local freezing hypothesis or against the global
half-area target, which (3) attains.

For any q>=1 the same two-row zero-charge separators as in the preceding
note permit q copies, choosing the canonical or zipper matching independently.
Their T/P is identical, so seam feasibility, ranks and the literal physical
payment map replay in disjoint copies. Width W=6m+16 and height 8q-2 give

    J=(4q-1)W=area/2.

There are at least 2^q actual frozen matchings. With f zipper copies the
number of missing prescribed interior edges is f(8m+7), still at zero
reserve. The q(m+4) donor tokens and demands are distinct across copies.
This is an all-q proof, independently of finite stack checks.

## 5. Evidence and limits

The proof is (1), the complete strict actual-mate table, the two explicit
traps and the disjoint physical payment map. A small matching enumeration
suggested the construction, but no all-matching classification or numerical
pattern from that enumeration is used as a theorem. General mixed-direction
geometric coverage and the universal grid 5/6 improvement remain open.

The solver-free coordinate verifier is
`develop/check_two_port_unbounded_rematching.py`. It checks all four local
closures against the rank and trap certificates, verifies full union ranks,
independently compares queue and synchronous freezing, counts actual matching
differences, checks original-token bijections, isometries and stack profiles.
The accompanying Lean scope is stated with its receipt; full coordinate and
concrete trap adapters remain written and executable.

Reproduce the saved checks from the repository root:

    python3 develop/check_two_port_unbounded_rematching.py --output output/two-port-unbounded-rematching.json
    python3 develop/check_two_port_unbounded_rematching_formal.py --output output/two-port-unbounded-rematching-formal.json

The saved solver-free run passes 33 lengths through m=100, 33 fully frozen
half-area unions, 132 exact interface responses, 60 exhaustive canonical/zipper
stack profiles, one larger 16-copy stack and 16 isometries. It checks 34,686
global actual-mate rank events, 39,096 partial-interface rank events and 94
literal physical-token bijections. Queue and independent synchronous closure
agree on all 33 single boards.

The local Lean 4.33.0 audit passes 17 declarations with no warnings, admitted
proofs or custom mathematical axioms. Its general results establish that
actual-mate dependencies preserve endpoint colour, and that changing the
initial kept sites outside one colour's neighbourhood leaves that colour's
least freezing closure unchanged. Conditional exact response and two-input
necessity/sufficiency make all coverage, positive-certificate and trap
hypotheses explicit. Further declarations audit the rank/count arithmetic
and unbounded changed-edge count and distance at two fixed ports. These
generic kernels are not an end-to-end coordinate theorem or a classification
of every matching on P*.

The [independent Oracle audit](../output/two-port-unbounded-rematching-oracle.json)
returns ACCEPT (observed gpt_6, pro), with no substantive revision requested.
It checks the new matching, missing-edge count, every rank dependency, exact
interfaces, physical ledger and arbitrary stacks, conditional on the inherited
cap and original attainer results. It executed no Python or Lean. The theorem
constructs actual frozen matchings on the same footprint; it does not assert
a dynamical sequence of freezing-preserving flips between them.
