# A zero-charge exterior activates noncanonical equality matchings

27 October 2026. Wenlin Zhang and Haobo Ma. Research continuation.

The isolated-band matching-rigidity theorem does not transfer to a region
of a completely frozen larger grid merely because the actual matching is
closed in that region. A six-column exterior with zero total physical charge
activates a noncanonical half-area matching inside the region. In the flipped
case both regions fail to freeze completely on their own, but their union
freezes completely.
We give all-length rank certificates, exact interface responses, and arbitrary
stacks with 2^q actual matching choices and no unspent physical tokens.

Nonunique completely frozen matchings were already established in
[the exchange-terminal receiver note](EXCHANGE_TERMINAL_NONUNIQUE_MATCHINGS.md).
The new point here is the sharp half-area occupied-band setting: its entire
old selected/endpoint footprint is retained, its matching stays region-closed,
and the exterior that breaks its newly proved rigidity has net charge zero.
This does not refute the isolated-band theorem or the global half-area target.

## 1. Exact construction and claims

Let (T*,M*) be the explicit frozen half-area family on
R={0,...,5} x {0,...,c}, c=6m+9, m>=2. Write n=3m+2 and use the names in
[Frozen half-area attainers](FROZEN_HALF_AREA_ATTAINERS.md). In particular
G_m=(3,c-2), H_m=(3,c-1), g=(3,c), Q=(4,c),
Z_(n-1)=(4,c-2) and K_(n-1)=(4,c-1).
Put A_end=Z_(n-1), y=K_(n-1) in this note.

There are two actual matchings inside R:

    M_R(0)=M*,
    M_R(1)=(M* minus {G_m H_m,A_end y}) union {G_m A_end,H_m y}.   (1)

Selections T* and endpoints P*=V(M*) are identical in both cases.
Add the six-column rectangle C={0,...,5} x {c+1,...,c+6}.
In the following CAP coordinates columns are 0,...,5; translate them by c+1.

    T_C={(0,1),(0,3),(0,5),(1,0),(1,4),(2,5),(3,5),
         (4,4),(5,1),(5,3),(5,5)},
    M_C={(1,1)--(2,1), (1,3)--(1,2),
         (2,2)--(3,2), (2,3)--(3,3),
         (3,0)--(3,1), (4,0)--(4,1), (4,2)--(4,3)}.       (2)

No actual matching edge crosses R/C. The only contacts between occupied sites
on opposite sides are g--p and Q--q, where p=(3,0), q=(4,0) in cap coordinates.
The two full configurations have the same T and P and differ in two matching
edges in R. Both are feasible and completely frozen for every m>=2, and

    |T|=9m+32, |M|=9m+16,
    J=18m+48 = area/2,    shape=6 x (6m+16).              (3)

In the flipped case M_R(1), the induced configuration on R alone has exactly
four unfrozen endpoints H_m,g,y,Q. The induced cap alone freezes six of its
fourteen endpoints. Global freezing therefore does not imply either local
freezing hypothesis, even with matching-closed regions and unchanged T/P.

## 2. Feasibility and geometry for every length

The original T*/P* occupation is unchanged by (1). At the interface, the cap's
column zero is blank in rows 0,2,5, selected in row 1, and endpoints in rows
3,4. The old R column c is selected in rows 0,2,5, blank in row 1, and endpoints
in rows 3,4. Hence no old selection acquires an occupied neighbour. The only
new occupied/occupied interface edges are exactly g--p and Q--q.

For cap feasibility, the selected sites (0,1),(1,0) each see only (1,1);
(0,3),(1,4) each see only (1,3); (4,4),(5,3) each see only (4,3);
(5,1) sees only (4,1). The selected pair (2,5),(3,5) sees only each other.
The selections (0,5),(5,5) have no occupied neighbours. These lists also
exhaust possible selections adjacent to the interface. Every cap matching
edge is a distinct grid edge, and all avoid T_C. Thus feasibility and actual
matching disjointness are proved for every m, not extrapolated from a search.
There are eleven new selections and seven new edges, proving (3).

## 3. A complete all-length certificate in the actual union

A site is kept when selected or when its ACTUAL mate has already frozen.
Use the original rank certificate for R, with these changes:

* Q keeps rank n, but uses selected (5,c) and the cap site q.
* g keeps rank 3, but uses selected (2,c) and the cap site p.
* In the flipped case, y keeps rank 4 and uses A_end,Q; H_m keeps rank n+1
  and uses G_m,g. In the canonical case their original witnesses remain.

The other R witnesses remain valid. The only changed witness-mate comparisons
are improvements: at F_m and D_m, site G_m now has mate A_end of rank n-1 rather
than H_m of rank n+1; at K_(n-2), site A_end now has mate G_m of rank 2 rather
than y of rank 4. Own-mate changes at A_end require no new witness. All earlier
cores and all other listed mates are unchanged. These observations exhaust
the neighbours of the four vertices incident to the matching switch.

Name the cap endpoints as follows, still in local cap coordinates:

    C0=(1,1), D=(2,1), A=(1,3), B=(1,2), E=(2,2), F=(3,2),
    U=(2,3), V=(3,3), p=(3,0), a=(3,1), q=(4,0), b=(4,1),
    L=(4,2), Z=(4,3).

Their matching is C0D,AB,EF,UV,pa,qb,LZ. The table gives WITNESS SITES,
so comparisons are with the witnesses' actual mates, not their own ranks.
A cap coordinate refers to its translate by c+1 in the full grid.

| Endpoint | Rank | Two witness sites |
| --- | ---: | --- |
| C0 | 0 | selected (0,1),(1,0) |
| A | 0 | selected (0,3),(1,4) |
| Z | 0 | selected (4,4),(5,3) |
| E | 1 | B,D |
| b | 1 | selected (5,1),L |
| a | 2 | D,F |
| q | 4 | p,inside Q |
| L | 5 | F,b |
| V | 6 | F,Z |
| p | n+1 | q,inside g |
| F | n+2 | a,L |
| D | n+3 | a,E |
| B | n+4 | C0,E |
| U | n+5 | A,E |

Here E uses mates A,C0 of rank zero; b uses selected support and mate Z of
rank zero; a uses C0,E of ranks zero and one. Thus the outside sites p,q
can support R using earlier mates a,b, of ranks two and one. In the other
direction q uses a and inside g of ranks two and three; L uses E,q of ranks
one and four; V uses E,L of ranks one and five. The white return wave starts
at p using mates b and inside Q, of ranks one and n. At F the witness mates
are p and Z; at D they are p and F; at B they are D and F; at U they are B,F.
Each is strictly earlier than the listed endpoint.

The modified R witnesses at Q,g have earlier cap mates b,a. In the flipped
case y uses mates G_m,g of ranks two and three, while H_m uses mates A_end,Q
of ranks n-1,n. This proves every rank inequality and completes the union
certificate for both actual matchings. Since n+5=3m+7<=9m+7, the old maximum
rank 9m+7 still bounds the full certificate, hence at most 9m+8 synchronous
rounds suffice. No exact minimal-depth equality is asserted.

## 4. Exact interface responses and a general composition lemma

This gives a small interface description with all hypotheses visible.
For R in the flipped state, freeze internally first. The unchanged certificate
on P* minus {H_m,g,y,Q} proves that every other endpoint freezes. The white
set {H_m,Q} and black set {g,y} are separate traps. The complete lists of
possible selected or outside-trap-mate witness sites within R are

| Trap | Endpoint | Possible witness sites |
| --- | --- | --- |
| {H_m,Q} | H_m | G_m |
| {H_m,Q} | Q | selected (5,c) |
| {g,y} | g | selected (2,c) |
| {g,y} | y | A_end |

For example G_m has actual mate A_end, but g has actual mate Q and y has
actual mate H_m, so the latter two sites cannot start the white trap. Each
member has at most one witness even after all endpoints outside its trap
freeze. These four remain unfrozen with no cap input.

Now grant the outside site p as kept iff its cap mate a is supplied frozen,
and grant q iff its mate b is supplied frozen. Apart from these two granted
sites, compute the ordinary least local freezing closure. Its exact response is

    F_R(I)=P* minus {H_m,g,y,Q}
           union ({g,y} if a in I)
           union ({H_m,Q} if b in I),                  (4)

for I subset {a,b}. Indeed p lets g use selected (2,c), then y can use Q
whose mate g has frozen, together with A_end whose mate G_m is frozen. Likewise
q lets Q use selected (5,c), then H_m can use g whose mate Q has frozen,
together with G_m whose mate A_end is frozen. Without the corresponding granted
site its two-endpoint trap remains, regardless of activation of the other
colour. Here a,b are different actual endpoints, not two names for one input.

Inside the cap, the six endpoints

    E0={C0,A,Z,E,b,a}

freeze without R. The other eight are closed into two groups. Grant outside
g as kept iff its actual mate Q is supplied frozen; grant outside Q iff its
mate g is supplied frozen. Then the exact cap response is

    F_C(J)=E0 union ({p,F,D,B,U} if Q in J)
                 union ({q,L,V} if g in J),             (5)

for J subset {g,Q}. The displayed rank table proves the indicated activations.
Without input Q, the five white endpoints p,F,D,B,U form a trap; without
input g, the three black endpoints q,L,V form a trap. Their complete possible
selected or outside-trap-mate witness lists, with that input absent, are
counted within the cap plus the explicitly granted exterior sites:

| Trap | Endpoint | Possible witness sites |
| --- | --- | --- |
| {p,F,D,B,U} | p | q |
| {p,F,D,B,U} | F | L |
| {p,F,D,B,U} | D,B,U | none |
| {q,L,V} | q | p |
| {q,L,V} | L | F |
| {q,L,V} | V | F |

The other input may be present in each case: its outside kept site is not
adjacent to a member of this trap. A neighbouring site in the other colour's
completion group has its actual mate in the same-colour trap, so it is not
extra support. Each trap member still has at most one witness even when
every endpoint outside its trap is supplied frozen. A first-frozen-member
argument therefore proves (5) generally, independently of the verifier.

A useful general composition principle follows. Let a finite feasible grid
be partitioned into two regions closed under the actual matching. Suppose
some exterior endpoints E0 have a strict-rank certificate using local selections
and witness sites whose actual mates are earlier in E0. Suppose all endpoints
of the first region can then be frozen with E0 supplied, and the remaining
exterior endpoints can then be frozen with the first region and E0 supplied.
Then the union is completely frozen. Concatenate the three witness schedules;
each witness mate occurs earlier, so no circular assumption of global freezing
is needed. Local selections remain selected in the union and final feasibility
is an explicit hypothesis. No charge or resource credit is created by this
logical composition.

In this construction the cap supplies a,b within E0, equation (4) completes R,
and (5) completes the cap. In particular mutual geometric contact does not
justify assuming both regions frozen initially; their interface response and
starting endpoints establish that conclusion.

## 5. Exact physical ledger, and arbitrarily many activated bands

Original aligned 2x2 tiles in R have exactly the previous explicit charge table,
because charge depends on T and P, which (1) preserves. The cap offset c+1 is
even, so its tiles share the original alignment and no tile straddles R/C.
In cap coordinates,
its COMPLETE tile-charge matrix is

    rows 0/1:  -1   0   0
    rows 2/3:  +1   0   0
    rows 4/5:   0   0   0,                              (6)

with columns grouped as 0/1,2/3,4/5. In particular the cap has charge zero.
Its one positive half-unit token pays its one negative demand. Every original
positive token in R is already spent by the previous explicit bijection.
The union has m+4 positive tokens and m+4 demands, and zero reserve. These
are counts over ALL tiles, not the preceding note's Cplus restricted to the
exterior of its designated strip. The payment map accounts for physical
tokens; it asserts no geometric routing along grid paths. Treating
the cap's positive token as additional reserve would leave its negative tile
unpaid. Its two early freezing inputs a,b are not surplus-token identities.

For any q>=1, stack q copies at row offsets 8i, 0<=i<q, with common even
width W=6m+16. Between copies put two separator rows. At each even column
select both separator sites as a vertical TT pair; all other separator sites
are blank. All top/bottom selections of a copy lie in odd columns, and no
endpoint lies on its top/bottom row. Thus each added selection sees only
its partner, no copy's selection acquires an occupied neighbour, and all
endpoint certificates replay independently. Every separator tile has two
selections and no endpoints, so its charge is zero.

Choose either matching (1) independently in every copy. The resulting board
has shape (8q-2) x W and

    |M|=q(9m+16),
    |T|=q(9m+32)+(q-1)W,
    J=(4q-1)W=area/2.                                  (7)

There are at least 2^q distinct actual matchings with the same T,P; the lower
bound follows from the q disjoint switched edge pairs. If f copies are flipped,
there are 2f missing prescribed interior edges, and f interior regions that
fail to freeze locally, while the whole grid is completely frozen and has
zero reserve. The q(m+4) positive physical tokens pay q(m+4) negative demands
once each. The cap payment and original R payments have disjoint physical
tiles, and so do different copies: the row offsets 8i and both separator
heights are even. This is an all-q proof with an explicit
nonreuse map, not an extrapolation from finite enumeration.

Consequently, the rule "apply the isolated frozen-band binary reserve to every
matching-closed region of a globally frozen board" is false, even when each
region has the original retained T/P footprint and actual local half-area.
The failed hypothesis is LOCAL freezing. Matching closure alone does not give
closure under freezing witnesses. This is an obstruction to that transfer
rule, not a counterexample to the original isolated theorem or the global
half-area inequality, which these constructions attain exactly.

## 6. Verification scope

The proof is the explicit all-length construction, actual-mate rank table,
interface trap argument and arbitrary-q stacking above. Discovery used finite
optimization only. A four-column failed search is not claimed as a universal
minimality theorem. The permanent solver-free verifier recomputes selections,
actual mates, strict ranks, exact interface closures, tile-token bijections,
matching-closed region boundaries and stack profiles. The local Lean audit
covers strict actual-mate stage induction, conditional three-stage certificate
composition, seeded trap exclusion, phase lifting, rank arithmetic, counts,
indexed bijective payment nonreuse and stack area arithmetic. The full
coordinate adapter remains written and executable.

Reproduce the saved controls from the repository root:

    python3 develop/check_ambient_band_port_activation.py --output output/ambient-band-port-activation.json
    python3 develop/check_ambient_band_port_activation_formal.py --output output/ambient-band-port-activation-formal.json

The saved solver-free run checks 26 lengths through m=100, both actual
matchings on 52 boards, 208 exact interface responses, 186 exhaustive stack
profiles on 15 fixed-occupation families, three larger stacks, 32 isometries,
103,428 strict actual-mate rank events and 241 physical token bijections.
Every single-board queue closure is cross-checked against an independent
synchronous replay. The two regions are matching-closed regions, not distinct
endpoint components: their endpoints touch at the two interface edges.

The local Lean 4.33.0 run checks 17 declarations, without warnings, admitted
proofs or custom mathematical axioms. Three-stage composition and seeded trap
exclusion use no axioms. The stage induction is for arbitrary endpoint types
and arbitrary natural ranks, and the indexed bijection is for arbitrary index,
source and target types. Neither is a collection of fixed-board checks.

The [independent Oracle audit](../output/ambient-band-port-activation-oracle.json)
returns ACCEPT (observed gpt_6, pro). It checks the new written construction,
actual-mate ranks, exact interfaces, seams, stacks and nonreuse, using the
prior isolated upper bound, rigidity and attainers as inherited premises.
It executed no Python, optimizer or Lean. Its two requested wording
clarifications are incorporated: both regions fail local freezing in the
flipped case, and cap trap supports count only explicitly granted outside
sites. The all-tile/exterior-token distinction and alignment parity are
explicit above.
