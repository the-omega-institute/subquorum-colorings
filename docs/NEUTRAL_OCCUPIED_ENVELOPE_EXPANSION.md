# Neutral occupied envelopes: sharp guard costs and a fully frozen completion

27 October 2026. Wenlin Zhang and Haobo Ma.

Opening an occupied interior interface cannot be priced solely by the two
endpoints that directly touch the old band. A six-cell envelope adds one
further endpoint, rematches one old edge, and cancels exactly one original
positive-token/negative-demand pair. Arbitrarily many disjoint envelopes
remain completely frozen with NO outside input and at exact half-area.
Two local rematchings can be mixed independently, giving at least 2^|S|
actual matchings on each enlarged footprint and 3^m configurations overall.

We prove the full all-length construction, its literal actual-mate rank table,
its physical-token cancellation, and the precise restricted rule it defeats.
For arbitrary partial occupations throughout the full six-cell permission
domain, an exact pooled budget also classifies every neutral T/P footprint.
The universal grid 5/6 improvement and arbitrary endpoint invasion remain open.

## 1. Exact original footprint

Let m>=2, c=6m+9, n=3m+2 and R={0,...,5} x {0,...,c}.
Use the following endpoints in each core j=0,...,m, with t=6j:

    A=(1,5+t), B=(1,6+t), C=(1,7+t), D=(2,7+t),
    E=(2,6+t), F=(3,6+t), G=(3,7+t), H=(3,8+t),
    U=(2,5+t), V=(3,5+t).

Also g_j=(3,9+6j) for 0<=j<=m, b_j=(3,10+6j) for 0<=j<m,
Z_l=(4,5+2l), K_l=(4,6+2l) for 0<=l<n, and Q=(4,c).
The isolated edge is (1,1)--(2,1).
The original matching M0 consists of that edge, AB,CD,EF,GH,UV in each core,
g_j b_j for j<m, g_m Q, and Z_l K_l. Let P0 be its endpoint set.
The original selections T0 have columns

    rows 0 and 5: every odd column 1,3,...,c;
    row 1: {2} union {4+6j,8+6j:0<=j<=m};
    row 2: {0,3} union {9+6j:0<=j<=m};
    row 3: {1,3}; row 4: {0,2,4}.

Thus |T0|=9m+21, |M0|=9m+9 and J0=|T0|+|M0|=18m+30=area(R)/2.
M is a matching of nearest-neighbour grid edges; N_R(x) denotes the
nearest-neighbour grid sites inside R. A labeled configuration (T,M) includes
its actual matching, so different matchings can share one T/P footprint.
A feasible pair (T,M) has disjoint selected sites and matching endpoints,
and every selected site has at most one occupied neighbour in T union P.
An endpoint freezes once TWO distinct adjacent sites are kept. A site is kept
when selected or its ACTUAL mate has previously frozen. Initially no endpoints
are frozen. No exterior sites are granted in this note.
Equivalently, with actual-mate involution mu, F_0 is empty and

    F_(r+1)=F_r union {x in P: |N_R(x) intersect (T union mu(F_r))|>=2}.

A rank witness y at x is selected, or y is an endpoint with
rank(mu(y))<rank(x). In particular y=mu(x) can never be such a witness:
it would require rank(x)<rank(x).
Even coordinate sum means black; odd means white. Witness-mate dependencies
preserve colour, so black and white rank orders can be supplied independently.

## 2. A sharp restricted entry budget, and its boundary

For j<m write the two DIRECT black entry sites and their shields as

    d_j=(2,8+6j), e_j=(2,10+6j),
    a_j=(1,8+6j), b'_j=(1,10+6j), f_j=(2,9+6j).

Here a_j,b'_j,f_j belong to T0. The first two have original occupied neighbours
C_j and A_(j+1), respectively; f_j has original occupied neighbour g_j.
All those neighbours belong to the retained endpoint set P0. Occupying d_j
therefore forces a_j and f_j OUT OF THE SELECTED SET. Occupying e_j forces
b'_j and f_j out. This is a selected-degree argument and does not assume any
matching on the enlarged endpoint set.

For any X subset {d_j,e_j:0<=j<m}, let G(X) be this union of forced shields,
and let h(X) count indices j with d_j or e_j in X. Then the shields have exact
union size

    |G(X)|=|X|+h(X).

Every entry has its own private row-1 shield, while the two entries at one j
share precisely f_j. Counting f_j twice would overstate the physical loss.

**Restricted budget lemma.** Suppose all of P0 is retained, every site of X
is a new endpoint, no selected site is added outside T0, and every other new
endpoint is a converted site of G(X). Allow arbitrary actual rematching.
Then

    J <= J0-h(X).

Proof: the original endpoints have equal colour counts. All sites of X are
black and all sites of G(X) white. A perfect matching on the enlarged set
therefore requires exactly |X| converted white endpoints. At least |G(X)|
original selections must be withdrawn. Thus |M|-|M0|=|X| and
J-J0<=|X|-|G(X)|=-h(X). Equality is feasible for every X: withdraw G(X), pair
each entry with its PRIVATE shield, and leave all common f_j empty, retaining
M0. These private pairs are disjoint, and the selected-degree condition holds.
This sharpness statement is about feasibility, not complete freezing.

The footprint restriction is essential. The construction below includes one
additional BLACK endpoint w_j, not adjacent to any original WHITE endpoint.
It lies outside this lemma's allowed new endpoint set and restores one unit
of objective for each occupied pair d_j,e_j. Applying the restricted inequality
to that larger footprint would be false.

There is also a freezing obstruction in the restricted class. Any converted
private shield has at most two occupied neighbours (its old black neighbour
and its entry); it has no selected neighbour. Excluding its own mate leaves
at most one possible support, so it is a singleton trap. A common shield f_j
can possibly freeze only when BOTH entries are present: with only one it has
at most two occupied neighbours. Hence a completely frozen restricted model
could convert at most one shield per double-occupied index, at most |X|/2,
whereas matching colour balance requires |X| conversions. No nonempty X in
this restricted model can completely freeze. This uses no finite search.

## 3. The neutral six-cell completion

Choose ANY S subset {0,...,m-1}, and put s=|S|. At each j in S add also

    w_j=(1,9+6j).

Convert all three shields a_j,b'_j,f_j from selected sites to endpoints,
and fill the three formerly empty black sites d_j,e_j,w_j. Thus the new
six-cell rectangle is rows 1,2 and columns 8+6j,9+6j,10+6j.
Define

    T_S = T0 minus union_j{a_j,b'_j,f_j},
    M_S = M0 minus {C_j D_j:j in S}
          union {C_j a_j, D_j d_j, w_j b'_j, f_j e_j:j in S}.       (1)

Every displayed pair is a grid edge. The envelope rectangles are disjoint;
their old attachment edges CD are disjoint too. The new matching retains
EVERY original endpoint and changes just one old matching edge per envelope.
Its endpoint set is exactly P0 plus the six new sites per envelope. In
particular

    |T_S|=9m+21-3s, |M_S|=9m+9+3s,
    |P_S|=18m+18+6s, J_S=18m+30=area(R)/2.           (2)

For a small reproducible example take m=2, S={0}, on the 6x22 board.
Remove edge (1,7)--(2,7), withdraw selections (1,8),(1,10),(2,9), and add

    (1,7)--(1,8), (2,7)--(2,8),
    (1,9)--(1,10), (2,9)--(2,10).

All other original edges and selections are as in Section 1. There are now
36 selected sites and 30 matching edges, so J=66=132/2; all 60 endpoints
freeze. This is a counterexample to imposing a loss of one for the occupied
pair (2,8),(2,10) while omitting (1,9) from its accounting. The two changed
nonzero tile charges are at (0,10) and (2,10).

Feasibility is local. Every new black site d/e is adjacent to its withdrawn
shields; no other retained selection gains an occupied neighbour there.
The new w_j is adjacent to the retained top selection (0,9+6j), which had NO
occupied neighbour before and now has exactly one. All other original
selected degrees are unchanged or decrease. This proves feasibility for
arbitrary S, including consecutive envelope indices.

**Neutral expansion theorem.** For every m>=2 and every S, (1) is completely
frozen within R, WITHOUT either right grant. Equations (2) are exact. Every
envelope cancels one original physical positive token and precisely its
original negative demand, leaving a bijection on all remaining tokens.

The next two sections give the all-length strict-rank proof. Ranks are
nonnegative integers; each witness site's ACTUAL mate has strictly lower
rank, unless the witness site is selected.

## 4. Complete white rank table

Let r_j=n+1+9(m-j). Give the isolated white endpoint (2,1) rank 0,
Z_l rank l, and Q rank n. Their witnesses are, respectively,

    (2,1): selected (2,0),(3,1);
    Z_0: selected (4,4),(5,5);
    Z_l, l>=1: selected (5,5+2l), K_(l-1);
    Q: selected (5,c), K_(n-1).

The actual mate of K_(l-1) is Z_(l-1), and that of K_(n-1) is Z_(n-1).
Thus the entire lower white wave is independent of S and needs no q.
Use the following remaining ranks and witness SITES:

| White endpoint | Rank | Two witness sites |
| --- | ---: | --- |
| H_j | r_j | g_j,K_(3j+1) |
| F_j | r_j+1 | G_j,K_(3j) |
| D_j | r_j+2 | E_j,G_j |
| f_j, j in S | r_j+3 | g_j,d_j |
| b'_j, j in S | r_j+4 | A_(j+1),e_j |
| a_j, j in S | r_j+5 | d_j,w_j |
| B_j | r_j+6 | C_j,E_j |
| U_j | r_j+7 | A_j,E_j |
| b_(j-1), j>=1 | r_j+8 | V_j,K_(3j-1) |

For H_m, site g_m has mate Q of rank n. For j<m, g_j has mate b_j,
whose rank is r_(j+1)+8=r_j-1. All lower K sites have their already frozen
bottom white mates. The two mates at F are H_j and a bottom Z; those at D
are F_j,H_j, even when D's actual mate is now d_j.

At an envelope, f_j uses mates b_j (rank r_j-1) and D_j (rank r_j+2).
The next white shield b'_j uses mates B_(j+1) (rank r_j-3) and f_j.
Then a_j uses D_j and b'_j. The new black site w_j is kept because its
mate b'_j has frozen; we never assume that w_j itself is already frozen.
At B_j the mate of site C_j is a_j if j in S, otherwise D_j; both precede
r_j+6. At U the mates are B_j,F_j. At b_(j-1) they are U_j and a bottom Z.
Every comparison is strict for all m,j. This covers every white endpoint.

## 5. Complete black rank table

Give the isolated black endpoint (1,1) rank 0 with selected witnesses
(0,1),(1,2). First propagate along the top from left to right:

| Black endpoint | Rank | Two witness sites |
| --- | ---: | --- |
| A_j | 3j | (0,5+6j),(1,4+6j) |
| C_j | 3j+1 | (0,7+6j),B_j |
| w_j, j in S | 3j+2 | (0,9+6j),a_j |

At A_j the left site is selected unless j>=1 and j-1 in S; in that case
its actual mate is w_(j-1) of rank 3j-1. At C_j the top site stays selected
and B_j has mate A_j. At w_j the top site was originally an isolated
selection and stays selected; a_j has mate C_j. Hence these ranks also work
for consecutive envelopes. No new w is assumed to be an independent seed.

Put L=3m+1 and t_j=L+1+10(m-j). Complete a reverse wave:

| Black endpoint | Rank | Two witness sites |
| --- | ---: | --- |
| e_j, j in S | t_j | b'_j,U_(j+1) |
| d_j, j in S | t_j+1 | a_j,f_j |
| E_j | t_j+2 | B_j,D_j |
| G_j | t_j+3 | D_j,F_j |
| g_j | t_j+4 | (2,9+6j),H_j |
| K_(3j+2), j<m | t_j+5 | b_j,Z_(3j+3) |
| K_(3j+1) | t_j+6 | H_j,Z_(3j+2) if j<m; H_m,Q if j=m |
| K_(3j) | t_j+7 | F_j,Z_(3j+1) |
| V_j | t_j+8 | F_j,Z_(3j) |

At an envelope e_j uses mates w_j and V_(j+1); the latter has rank
 t_(j+1)+8=t_j-2. Then d_j uses C_j,e_j. The two mates at E_j are A_j
and d_j if expanded, otherwise A_j,C_j. At G_j they are d_j,E_j if
expanded, otherwise C_j,E_j. At g_j its upper site is selected unless
expanded, in which case its mate is e_j; H_j always has mate G_j.
This includes g_m, whose upper site remains selected, so no p is required.

The K_(3j+2) mates are g_j and K_(3j+3) from the completed next block.
The next two lower steps use respectively G_j with K_(3j+2), and E_j
with K_(3j+1). The terminal K_(3m+1) instead uses G_m,g_m. Finally V_j
uses E_j,K_(3j). All comparisons are strict. The maximum rank is at most
13m+10, hence at most 13m+11 synchronous rounds suffice. This is a bound,
not a claim about the minimal freezing depth.

## 6. Literal physical token cancellation

Use the original 2x2 tiles starting at even row and column. In half-unit
units their charges are

    chi(tile)=4-2|T intersect tile|-|P intersect tile|.

The original nonzero charges are exactly

    +1 at (0,0),
    -1 at (0,4+6k), 0<=k<=m,
    -1 at (2,0), +2 at (2,4),
    +1 at (2,4+6k), 1<=k<=m,
    -1 at (4,4).

Each positive half-unit has its own (tile,index) identity, including the two
separate units at (2,4). The original complete payment bijection is

    (0,0)#0 -> (0,4)#0;
    (2,4)#0 -> (2,0)#0;
    (2,4)#1 -> (4,4)#0;
    (2,4+6k)#0 -> (0,4+6k)#0, 1<=k<=m.              (3)

One envelope j changes only two tile charges:

    chi(0,10+6j): -1 -> 0,
    chi(2,10+6j): +1 -> 0.                         (4)

Indeed converting a selected site to an endpoint adds 1 half-unit, while
filling an empty site with an endpoint subtracts 1. At tile (0,8+6j),
a_j's +1 and w_j's -1 cancel. At (2,8+6j), f_j's +1 and d_j's -1
cancel. The remaining sites b'_j and e_j give precisely (4).
Different envelopes have disjoint tile supports. Delete from (3) exactly
the pairs k=j+1 for j in S. Every surviving original positive token pays
one surviving original negative demand, and none is used twice. There are
m+3-s positive tokens and the same number of demands. No token is invented,
redirected or released as reserve. The original +2 tile retains its two
separate identities. This proves the physical statement for all S.

## 7. Two local rematchings can be mixed independently

The CD-based choice (1) is not necessary. For any subset A of S, use (1)
at the indices of S minus A. At each j in A instead retain C_j D_j,
remove g_j b_j, and add

    g_j f_j, b_j e_j, a_j d_j, w_j b'_j.             (5)

All four are grid edges. The patches are disjoint for arbitrary S and A.
Call the resulting matching M_(S,A). It has precisely the same endpoint
set P_S, selected set T_S, objective and tile charges as (1).

**Independent mixed-expansion theorem.** Every M_(S,A) is completely frozen
without outside input. For each S there are at least 2^|S| different such
matchings on the SAME T/P footprint; over all S there are at least 3^m
different fully frozen half-area configurations. This is a lower bound,
not a classification of all matchings or footprints.

Here is a complete mixed certificate, including consecutive indices of
different types. The isolated endpoints, Z_l and Q keep their base witnesses
and ranks. Use the same r_j=n+1+9(m-j). At j not in A use the white table
in Section 4 unchanged. At j in A use this replacement table:

| White endpoint | Rank | Two witness sites | Actual-mate dependencies |
| --- | ---: | --- | --- |
| b'_j | r_j | A_(j+1),e_j | B_(j+1),b_j |
| f_j | r_j+1 | w_j,e_j | b'_j,b_j |
| H_j | r_j+2 | g_j,K_(3j+1) | f_j,Z_(3j+1) |
| F_j | r_j+3 | G_j,K_(3j) | H_j,Z_(3j) |
| D_j | r_j+4 | E_j,G_j | F_j,H_j |
| a_j | r_j+5 | C_j,w_j | D_j,b'_j |
| B_j | r_j+6 | C_j,E_j | D_j,F_j |
| U_j | r_j+7 | A_j,E_j | B_j,F_j |
| b_(j-1), j>=1 | r_j+8 | V_j,K_(3j-1) | U_j,Z_(3j-1) |

At either patch type, B_(j+1) and b_j retain ranks r_j-3 and r_j-1.
Thus all dependencies entering from the next block precede the current
block, irrespective of its type. Every within-block comparison is strict.
At a CD-based block the dependencies use that block's original Section 4
table. No assumption about an adjacent block's choice is needed.

For black endpoints use this top forward wave at EVERY j:

    A_j: rank 6j, witnesses (0,5+6j),(1,4+6j);
    C_j: rank 6j+1, witnesses (0,7+6j),B_j.

At j in A additionally put E_j,G_j,d_j at ranks 6j+2,6j+3,6j+4,
with witnesses B_j,D_j; D_j,F_j; D_j,H_j, respectively. Their actual-mate
dependencies are A_j,C_j; C_j,E_j; C_j,G_j. At every j in S put w_j
at rank 6j+5, using selected (0,9+6j) and a_j. The mate of a_j is C_j
for a CD patch and d_j for a gb patch, so both precede w_j. The left
site at A_(j+1), if converted, has mate w_j of rank 6j+5<6(j+1).
Consequently this wave works across consecutive patches of either type.
All these forward ranks are at most 6m+1.

Now set t_j=6m+2+10(m-j). Use the Section 5 reverse table with this
new t_j at j not in A. At j in A omit d_j,E_j,G_j from the reverse
table because they were handled in the top wave. Keep

    e_j: rank t_j, witnesses b'_j,U_(j+1), with mates w_j,V_(j+1);
    g_j: rank t_j+4, witnesses H_j,b_j, with mates G_j,e_j.

All K and V rows keep their Section 5 ranks and witness sites. The only
changed K dependency is at K_(3j+2): the mate of witness b_j is now e_j,
of rank t_j, instead of g_j of rank t_j+4. Both precede t_j+5.
At EVERY next block, V_(j+1) has rank t_j-2 and K_(3j+3) has rank
t_j-3. Hence all reverse cross-block dependencies are strict regardless
of the choices in S and A. The terminal block is not expanded and keeps
its original seeds. This covers all black endpoints, with maximum rank
at most 16m+10, and proves the theorem by strict-rank induction.

Each expanded position independently chooses whether to remove CD or gb;
those two old edges are distinct, and all patches use disjoint old edges.
The resulting 2^|S| matchings are therefore distinct. Different S give
different endpoint footprints. Summing 2^|S| over S gives 3^m. The ledger
in Section 6 depends only on S, so EVERY one of these matchings uses the
same surviving physical payments, with no extra reserve from the choices.

## 8. Sharp budget and all neutral footprints in the full envelope domain

There is a stronger upper bound that does not prescribe S or require whole
envelopes in advance. Retain all original endpoints P0. Allow arbitrary
new black endpoints B among ALL d_j,e_j,w_j for 0<=j<m, arbitrary new
white endpoints Y among ALL a_j,b'_j,f_j, arbitrary T subset T0, and
arbitrary actual perfect matching on P0 union B union Y. No original
matching edge or freezing condition is imposed for this upper bound.
Write B_j=B intersect {d_j,e_j,w_j}.

Let G_j be the forced withdrawal set of original white selections at index j.
The old neighbours C_j,A_(j+1),g_j are retained endpoints. Consequently

    d_j present forces a_j,f_j withdrawn;
    e_j present forces b'_j,f_j withdrawn;
    w_j present forces ALL a_j,b'_j,f_j withdrawn.

The last line uses adjacency of w_j to f_j as well as a_j,b'_j. The
G_j are physically disjoint across indices. Put delta_j=|G_j|-|B_j|.
The complete local table is

| New black sites B_j | Black count | Forced guard count | delta_j |
| --- | ---: | ---: | ---: |
| empty | 0 | 0 | 0 |
| d only, or e only | 1 | 2 | 1 |
| d,e | 2 | 3 | 1 |
| w only | 1 | 3 | 2 |
| d,w, or e,w | 2 | 3 | 1 |
| d,e,w | 3 | 3 | 0 |

**Sharp pooled envelope budget.** For every prescribed B in this domain,

    max J = J0 - sum_j delta_j,                    (6)

where the maximum ranges over feasible T,Y and actual matchings. The
maximum does not require complete freezing. Moreover J=J0 is possible
if and only if EVERY B_j is empty or full. In that case its entire T/P
footprint is forced to be exactly T_S/P_S for the full-cell index set S;
that equality footprint DOES have completely frozen attainments by
Sections 3--7. Matching equality is not classified.

Proof. Since each matching edge joins opposite colours and P0 is balanced,
|Y|=|B| and |M|=|M0|+|B|. Set L=|T0 minus T|. All G_j must be
withdrawn, so L>=sum_j |G_j|. Thus

    J=J0+|B|-L <= J0+sum_j(|B_j|-|G_j|)=J0-sum_j delta_j.

This is one GLOBAL colour-balance count: white conversions may be pooled
across different indices and matched to old endpoints. No local perfect
matching or local colour-balance premise is assumed in the upper bound.
Equality in (6) is feasible for every B: withdraw exactly union_j G_j,
retain M0, and add d_j--a_j, e_j--b'_j, w_j--f_j for whichever black
sites are present. These three possible new edges have distinct targets.
The selected-degree check is the same as in Section 3. This proves (6)
without an optimization or a finite-enumeration premise. Such a sharp
matching need not be completely frozen.

If J=J0, every nonnegative delta_j must vanish. The table forces each
B_j empty or full. Also L=sum_j|G_j|=|B|. Because Y is disjoint from T,
Y lies among the withdrawn selections; its cardinality |B| equals L.
Hence Y=T0 minus T=union_j G_j. This proves the full equality-footprint
classification. Conversely the mixed-expansion construction supplies
completely frozen equality for every such footprint. This concludes the
proof for arbitrary length and arbitrary pooling across envelopes.

The plain half-area upper bound already follows from colour balance and
Y lying among withdrawn selections: L>=|Y|=|B|. The additional content of
(6) is the exact strictly positive loss for every proper nonempty local
black mask, feasible sharpness for EVERY prescribed B, and the complete
classification of equality footprints despite arbitrary global pooling.

## 9. Exact scope of the obstruction and the next cut problem

For the specified enlarged endpoint footprint P_S and any T subset T0,
no selected site in the three converted shields per envelope can be retained.
Every actual matching has |P_S|/2 edges. Therefore J<=J0, irrespective of
freezing or rematching; (1) attains equality with complete freezing. This is
the exact maximum for that specified endpoint footprint and selection domain.
Section 8 extends this to the full six-cell permission domain, with complete
equality-footprint classification and exact costs of partial black masks.
Neither statement is a maximum over arbitrary new sites or new selections
outside T0.

The pair-only inequality in Section 2 correctly loses one objective unit
per occupied d/e pair, but (1) has those same direct pairs and loses none.
The failed extension of that rule omitted w_j from the permitted footprint.
It also omitted the cross matching C_j--a_j,D_j--d_j used in (1), or an
alternative such as (5). Some old matching edge MUST change when S is
nonempty. Indeed, if all old M0 edges were retained, every new black
endpoint would have a converted white shield as mate. Before the first
such shield freezes, none of the new black sites can be kept. Each shield
has just one occupied neighbour outside the new black sites: C_j, A_(j+1), or g_j.
It has no selected neighbour, so no first shield can freeze. This traps
the entire converted white pool, independently of how its new edges are
matched. This does not force a particular old edge to change.
The counterexample thus
refutes an unqualified per-direct-entry cost, not the restricted lemma or
the global half-area target.

A logical interval hitting count can still constrain a matching while its
T/P and EF reduction remain fixed. It cannot be promoted to a physical
cost after these six-cell expansions without redoing the footprint and mate
accounting. In (1) both occupation and the old CD mate change; in (5),
gb changes instead. The corrected
joint cut must include the outer w site and record the cancelled successor
token/demand pair, rather than charge the same old donor once to each direct
entry or assume it remains available to another component.

Each S gives a different T/P footprint, so there are at least 2^m distinct
fully frozen half-area configurations already within R, without a cap.
This is a constructive lower bound, not a classification of enlarged
footprints or a sequence of freezing-preserving intermediate moves.

## 10. Verification and formal scope

The written all-length proof is (1) and (5), the complete strict actual-mate
rank tables (including the mixed table) and the literal deletion from (3).
Finite enumeration is used
only to discover and check it. The coordinate verifier checks arbitrary
subsets on small lengths, structured larger subsets, literal ranks,
independent freezing closures, feasibility and every surviving physical
payment identity. Its saved receipt states the actual tested scope.

Run the standard-library checks with

    python3 develop/check_neutral_occupied_envelopes.py --output /tmp/envelopes.json
    python3 develop/check_neutral_occupied_envelopes_formal.py --output /tmp/envelopes-formal.json

The saved coordinate [receipt](../output/neutral-occupied-envelopes.json)
covers 1,645 boards: 524 original CD-based controls (every S for m=2,...,8,
and the all/even/first/last subsets at m=10,25,50,100), plus 1,121 mixed
controls (all ternary patterns for m=2,...,6 and structured larger patterns).
It checks 282,246 strict actual-mate witness events, agreement of independent
queue and synchronous closures, 6,658 literal token/demand cancellations,
and 10,093 surviving payments. Distinct literal matching edge sets check
the 3^m count at m=2,...,6. Restricted controls
cover every entry set for m=2,3,4 and all 19,183 colour-balanced conversion
pools. An additional 576 arbitrary black-mask profiles and all 49,544
colour-balanced white conversion pools check the enlarged-domain budget,
including conversions pooled across different indices. Each profile has an
explicit feasible sharp matching. Forty-two retained-old-matching controls
check the whole converted-white pool trap. No optimizer or external solver
is used.

Nine declarations in
[NeutralOccupiedEnvelopes.lean](../formal/SubQuorum/NeutralOccupiedEnvelopes.lean)
include five kernels for injective physical shield coordinates, exact shared-guard counts for
arbitrary finite entry words, strict conversion shortage, the actual-mate
singleton trap, and the conditional restricted no-freezing contradiction,
plus four kernels checking all eight enlarged masks, the arbitrary-length pooled budget,
zero deficit if and only if all cells are empty/full, and the objective
equality criterion under explicit colour-balance/withdrawal premises.
The [local Lean receipt](../output/neutral-occupied-envelopes-formal.json)
records Lean 4.33.0, memory/process preflight before each invocation, and
axiom closures with no sorry or nonstandard axioms. The singleton proof reuses
the existing trap lemma; the full freezing argument reuses the existing
strict-rank induction from FrozenHalfAreaAttainers. Coordinate rank support,
feasibility, all-length matching construction and physical cancellation
remain written proofs with the executable adapter above. The Lean result
does not claim an end-to-end coordinate formalization.

Independent review is recorded with separate scopes. The
[original audit](../output/neutral-occupied-envelopes-oracle.json) returned
REVISE, accepted the original construction and supplied the alternative gb
patch as proof assistance; the terminal definition and overstrong CD-edge
necessity wording were corrected. A fresh
[mixed-construction audit](../output/neutral-occupied-envelopes-mixed-oracle.json)
returned ACCEPT for the arbitrary mixed rank proof, labeled 3^m count,
restricted rule and physical cancellation. Its occupied-neighbour wording
clarification is applied. Neither audit executed the verifier or Lean.
The later sharp pooled budget and equality-footprint classification in
Section 8 have a [separate follow-up record](../output/neutral-occupied-envelopes-pooled-oracle.json);
that record states the actual request status, without borrowing the earlier
ACCEPT for a result outside its input.

## 11. Proposed research-note addition

The useful addition to a future grid paper is the sharp pooled envelope
budget (6), its complete equality-footprint classification, and the
independent mixed expansions attaining equality. Its scope is essential:
an interface cost must depend on the
entire allowed footprint and the actual matching. The six-cell family is
a checked obstruction to charging a fixed positive amount to every occupied
direct-entry pair, even under complete freezing; it leaves the global
half-area target intact. It also gives a literal example in which both an
old donor and its old debt disappear, so a coarse compensation argument
must cancel them jointly before using any surviving resource. No edit to
the submitted 11 October manuscript is proposed by this local obstruction.
