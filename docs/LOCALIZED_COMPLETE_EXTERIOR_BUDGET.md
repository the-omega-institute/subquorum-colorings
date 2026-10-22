# A complete exterior compensation theorem with finite outer walls

22 October 2026. Authors: Haobo Ma and Wenlin Zhang.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.

## Statement and relation to the existing reserve theorem

Work in the full-even-U/standard-rotor immutable-source model. Each original
J has disjoint endpoint and support sets T_J,H_J and a matching M_J covering
T_J. Different originals have disjoint endpoint sets. Every unconsumed
original support is retained; in a complete fusion its occupied degree is
exactly one. Every endpoint has intrinsic occupied degree three, every
original support has intrinsic occupied degree one, and original endpoint
graphs are connected. Full U breadths are even >=6 and their independent
depths are even >=4; every orientation and translation is permitted.

For aligned tiles {2i,2i+1}x{2j,2j+1}, use the unchanged original charge

    q_J=|M_J|+|H_J inside tiles meeting T_J|-2|tiles meeting T_J|.

Let F be full mixed tiles, E the source-labelled directed intratile events
(J,x,y) with x in T_J, y a foreign endpoint, and y not in H_J. Put

    Phi=sum_J(max(0,-q_J)+I[q_J>0])+2|F|-|E|.

Retain the old nested family O:

    A=U(W+2,D,F), chart(r,c)=(r,c-1),
    B_i=U(W,4,4), chart(r,c)=(a_i+r,c), 0<=i<=g,

where W>=6, a_i>=2,D,F are even, a_(i+1)-a_i>=10, and
D,F>=a_g+4. In particular a wall may end EXACTLY at the last inner tip,
the two depths need not agree, and added sources may pass around either
wall tip or lie outside A. Suppose K=O union Y is any finite complete
fusion of permitted originals. By sealed-chamber localization, partition
ALL added originals into the chambers

    C_i=[a_i+2,a_(i+1)-1]x[1,W]

and the exterior. Let P_i and P_out count charge-+1 added originals in
the respective classes. Define the marginal of one class against O,
without assuming this restricted inventory itself complete:

    Delta_i=Phi(O union Y_i)-Phi(O),
    Delta_out=Phi(O union Y_out)-Phi(O).

**Localized compensation theorem.** Every such complete fusion satisfies

    Delta_i>=3+P_i for each chamber,
    Delta_out>=2+P_out>=2.                              (1)

Thus the unrestricted exterior sign is resolved in this explicit source
model. No cap, source-count, connectivity, dimension or finite-window
assumption is imposed on Y_out. This controls their AGGREGATE contribution;
the previous both-complete negative marginal examples remain valid.

The earlier `ACTIVATED_SINGLETON_FLOW_CANCELLATION.md` already proves
Phi(K)>=P(K) for every complete fusion, since its raw event reserve is
nonnegative. That GLOBAL sign is not new here. The new result is the
localized statement (1), with the exact incomplete boundary baseline.
Global nonnegativity cannot simply be subtracted between two inventories.
The proof below independently rewrites the same reserve; it does not create
another pool of available capacity.

## Exact physical-tile identity, including incomplete inventories

Two facts follow from intrinsic endpoint degree three and support degree one.

First, an original meets each endpoint tile in a connected endpoint set.
The sole disconnected possibility is a diagonal pair. Either remaining
corner, if occupied, would be a support adjacent to both endpoints. If
both corners are blank, either endpoint has occupied degree at most two.
Both alternatives are impossible.

Second, if h in H_J shares a tile with an endpoint of J, its unique own
endpoint neighbour is in that tile. Otherwise the only possible endpoint
of J in that tile is diagonally opposite h. That endpoint needs an occupied
intratile neighbour to have degree three. Such a neighbour must be another
support of J, adjacent to h as well, contradicting support degree one.

For an arbitrary endpoint-disjoint inventory, completeness NOT required,
define in each endpoint tile tau:

* n_tau: number of endpoints; e_tau: unordered endpoint-to-endpoint edges;
* k_tau: number of original endpoint owners meeting the tile;
* h_tau: original support INCIDENCES (J,h) in this tile with J meeting it;
* r_tau: those incidences not consumed by any endpoint;
* c_tau: indicator of a full tile owned by one original;
* f_tau: indicator of a full mixed tile.

Support multiplicity is essential: two originals can name the SAME
unconsumed support at the incomplete old baseline.

The total original intratile edge count is n_tau-k_tau+c_tau, by the
connected-subset fact. Hence cross-owner edges number
e_tau-(n_tau-k_tau+c_tau). Each gives two directed contacts. The second
fact gives a bijection between consumed counted support incidences and
the directed contacts excluded by the immutable support predicate. Thus

    |E_tau|=2(e_tau-n_tau+k_tau-c_tau)-(h_tau-r_tau).     (2)

Since |M_J|=|T_J|/2, the tile contribution to -sum(q_J) is
2k_tau-n_tau/2-h_tau. The original charge catalogue has q<=0 or q=1,
and only U originals have q=1. If P counts them, then
sum(max(0,-q)+I[q>0])=-sum(q)+2P. Substituting (2) yields

    Phi=2P+sum_tau beta_tau,
    beta_tau=3n_tau/2-2e_tau-r_tau+2I[n_tau=4].          (3)

This is an exact identity on incomplete inventories as well. It counts
every source-labelled direction and support exclusion once.

For reference, put t=(d+e)/2 for an untransformed U(b,d,e). In the four
translation phases (row,column) its (endpoint tiles,inside supports,q) are

    00: (b/2+1+t,4+t,1),
    10: (b+t,2+t,1-b),
    01: (b/2+t,t,-1),
    11: (b-2+t,t-2,1-b).

Its matching size is b-1+t. The two normalized rotor shapes have phase
charges 0,0,0,-2 up to permutation: their profiles are respectively
two Ls plus two singletons, four adjacent pairs, or one full square plus
four singletons. Their tile/inside-support counts are 4/4,4/4,5/4 with
matching size4. Tile-preserving lattice symmetries cover all orientations.

## Complete tile table and an injective rotor cancellation

In a complete fusion, a retained support cannot belong to two originals:
their distinct endpoint anchors would give it at least two neighbours.
The two preceding tile facts also hold for the final occupied set. Thus
r_tau is now the number of actual retained support SITES in the tile,
and e_tau=n_tau-1+I[n_tau=4]. The complete table is

| Endpoints n | Retained supports r | beta |
|---|---|---|
| 1 | 1 | 1/2 |
| 1 | 2 | -1/2 |
| 2 adjacent | 0 | 1 |
| 2 adjacent | 1 | 0 |
| 3 | 0 | 1/2 |
| 4 | 0 | 0 |

A singleton needs an occupied intratile neighbour; a diagonal retained
support would be adjacent to that support and is impossible. For two
adjacent endpoints the other corners are adjacent, so at most one is
retained. With three endpoints the missing corner has two endpoint
neighbours and cannot be retained. These observations prove the table.

Only a singleton with two retained supports has negative weight. Both
supports must belong to its endpoint's original: a foreign support would
have its different own endpoint anchor as well. In a U this endpoint must
be a terminal. At the left terminal (d,1), the supports (d+1,1),(d,0)
both share its tile exactly in phase00; the right terminal gives the
same test. Thus only charge-+1 U originals supply negative U tiles, at
most TWO per original, in any orientation.

For rotors, only the two-L phases have such singleton tiles. Normalize to
shape A translated by (1,0), with endpoints

    {(1,1),(2,1),(2,2),(2,3),(3,0),(3,1),(3,2),(4,2)}.

The singleton (1,1) has supports (0,1),(1,0). Pair its negative tile
with [2,3]x[0,1], containing three endpoints and missing (2,0). If
(1,0) remains a support, (2,0) cannot become an endpoint: that support
would then have two occupied neighbours. The mate therefore remains a
three-endpoint tile, of weight +1/2. Similarly pair singleton (4,2)
with [2,3]x[2,3]; the retained support (4,3) forbids its missing (3,3).
Tile-preserving symmetries transport these two pairs to every rotor phase
which has negative tiles.

The mates within a rotor are distinct. Mates of different rotors are
distinct because each contains three endpoints of its rotor, and different
original endpoint sets are disjoint. A mate cannot itself be a negative
singleton tile. Hence this is a genuine injection into DISTINCT positive
physical tiles; no positive tile is used again to pay another deficit.

## A general tile-cut compensation inequality

The same proof gives a reusable statement beyond this nested core. Let O
be ANY fixed endpoint-disjoint inventory, let K=O union Y be complete, and
let Q be a set of physical tiles such that each added original has either
ALL its endpoint tiles in Q or NONE there. Let Y_Q be the first class,
P_Q its positive-source count, and B_Q=sum_(tau in Q) beta_tau(O), with
original support-incidence multiplicity at the possibly incomplete O.

Let b_Q count OLD U terminal tiles in Q which contain exactly that one
old endpoint and both of that original's intratile supports. Equivalently,
these are old charge-+1 terminal occurrences whose physical tile could
still be a negative singleton after adding sources. Count each such tile
once. Also require that whenever an OLD rotor has an original singleton
with its two original intratile supports in a tile of Q, its paired
original triple tile belongs to Q. The cut compensation inequality is

    2[Phi(O union Y_Q)-Phi(O)]>=2P_Q-b_Q-2B_Q.           (11)

**Proof.** Identity (3) restricts to Q because no added source crosses its
tile cut; other added classes contribute no endpoint or counted support
incidence there. Thus the marginal is 2P_Q+sum_Q[beta(K)-beta(O)].
Every negative new U tile is one of at most2P_Q terminal occurrences.
Every negative OLD U tile was already a singleton endpoint tile of O:
endpoint sets only increase, and its two supports belong to the same old
terminal original. It is therefore among the b_Q tiles. The number of
negative U tiles is at most2P_Q+b_Q. A negative rotor belongs either to
an old or a new source. For a NEW rotor, its mate is in Q by the cut
assumption. For an OLD rotor it is in Q by the stated old-rotor mate
condition. Hence the injective rotor cancellation restricts to Q, giving
sum_Q beta(K)>=-P_Q-b_Q/2. Subtract B_Q to obtain (11). QED.

The old-rotor mate condition is automatic if every old rotor has its
entire endpoint footprint inside Q or outside it, and it is vacuous in
the nested A/B application. It cannot be omitted for an arbitrary cut.
For a disjoint collection of admissible cuts, every physical tile and
rotor mate is counted in at most one cut; every added source weight
belongs to exactly one class; each old terminal debit is assigned once.
Their inequalities therefore sum without reusing a surplus or pair.
This is an aggregate inequality, not source-addition monotonicity.

The old-rotor condition is necessary for this rule. Take the single
complete zero-charge rotor displayed above as O=K, take no additions,
and let Q=[0,1]x[0,1] contain just its upper negative singleton tile.
Then Delta_Q=0,P_Q=b_Q=0,B_Q=-1/2. Omitting the mate condition would
assert 0>=1 in (11). Including the paired triple tile makes the two
weights cancel. This is a fully complete counterexample to an arbitrary
tile-cut rule that drops old rotor mates, not to the exterior theorem or
to the target grid inequality.

## Localize the identity before applying the complete table

The physical footprint Q_i of C_i is exactly

    [a_i+2,a_(i+1)-1]x[0,W+1].

Its outside one-step boundary is filled with retained endpoints. A connected
new endpoint set meeting C_i cannot leave it without hitting such an old
endpoint. Every site of Q_i outside C_i is an old wall endpoint. Thus
every new original has ALL its endpoint tiles in one Q_i, or ALL in the
complement Q_out. These footprints are disjoint.

Identity (3) may therefore be restricted to a class X:

    Delta_X=2P_X+sum_(tau in Q_X)[beta_tau(K)-beta_tau(O)]. (4)

Indeed other classes have no endpoints or counted support incidences in
Q_X. A support in the tile is consumed exactly when that site is an
endpoint there, also unchanged by deleting other classes. Outside Q_X
the inventory O union Y_X has precisely O's tile data. This proves (4)
without assuming O union Y_X complete. Apply the complete table only to K.

No negative tile in Q_X belongs to an old original. A has charge -1.
Each old B terminal shares its physical tile with an A endpoint, including
the coincident-wall-tip case, so it is not a singleton. Every negative U
tile therefore belongs to a new charge-+1 source in this SAME class.
Every rotor mate remains in this class, since it contains three endpoints
of that same rotor. After the injective rotor cancellation, write N_X for
the number of negative U tiles and R_X for the sum of all remaining
nonnegative weights. Then

    sum_(Q_X) beta(K)=-N_X/2+R_X,
    N_X<=2P_X, R_X>=0.                                 (5)

This is a single partition of physical resources, not separate uses of
one source's surplus for several chambers.

## Compute the incomplete old boundary baseline

Put L=a_g+4. On the left, if D>L the gate tile
{L,L+1}x{0,1} contains three endpoints and a SINGLE unconsumed site
(L+1,1) named as support by BOTH A and B_g. Thus n=3,e=2,r=2 and
beta=-3/2. The separate outer-wall terminal tile has n=1,r=1 and
beta=+1/2. Their sum is -1.

If D=L these two tiles coincide. They contain the two endpoints
(L,0),(L,1) and the two axial supports (L+1,0),(L+1,1), so
n=2,e=1,r=2 and beta=-1 directly. The independent right depth F gives
the same answer. Every other old exterior tile is full or an ordinary
wall tile with n=2,e=1,r=1, of weight zero. Therefore

    sum_(Q_out) beta(O)=-2.                             (6)

In each chamber the two earlier B gate tiles have beta=-3/2 apiece;
every other old tile has weight zero. Hence

    sum_(Q_i) beta(O)=-3.                               (7)

The old supports were counted with multiplicity in (6),(7); replacing
their incidences by support sites would give a WRONG baseline. As a check,
(3) gives Phi(O)=2(g+1)-3g-2=-g.

Combining (4)--(7) proves the exact regional certificates

    Delta_out=2+2P_out-N_out/2+R_out>=2+P_out,
    Delta_i=3+2P_i-N_i/2+R_i>=3+P_i.

This proves (1), including all finite-wall and detached exterior sources.

## Consequences, examples and remaining scope

Together with exact chamber separation, (1) gives

    Phi(K)>=2g+2+sum_(new sources) I[q=1].               (8)

This global consequence also follows from the existing activated-singleton
theorem: the two terminals of every old B are already activated by A.
Its value here is a check on the localized accounting, not a new global
reserve theorem.

At W=6 with all gaps ten, the accepted full chamber classification has
Delta_i=5 or7. If d chambers use D, it now gives for EVERY complete
extension retaining O

    Phi(K)=4g+2d+Delta_out>=4g+2d+2+P_out.              (9)

The previous exact identity no longer carries an unresolved exterior sign.
For arbitrary W, the same applies when each chamber has a spanning D or U,
using the accepted complete-six-row pocket budget for each U chamber.
No classification of all wider chambers without a spanning source is asserted.

More explicitly, if d chambers have spanning D, u spanning-U pockets are
nonempty without H, and h spanning-U pockets contain H, the accepted pocket
bounds yield

    Phi(K)>=4g+(W-4)d+2+P_out+2u+5h.                  (10)

All other spanning-U pockets may be empty. The single exterior term in
(10) is paid once, independently of how many chambers are present.

### A concrete coefficient-one subclass

To connect the source inventory to the original matching inequality, use
the established dual-guard ledger of `ALL_PHASE_JOINT_COMPENSATION_SLOTS.md`.
For an admitted feasible representative pair in an even m-by-n rectangle,
write T_sel for its selected vertices, M for its matching, N for its total
charge-+1 source count, and G for its ACTUAL marked positive sides. Then

    sigma=mn/2-|T_sel|-|M|>=Phi-G,   G<=2N.             (12)

These are hypotheses supplied by that existing source-to-grid ledger;
they are not a decomposition theorem for arbitrary representative pairs.
At W=6 and gap10 every chamber is exactly D_6 or U_6, with no additional
source there. Hence

    N=(g+1)+(g-d)+P_out=2g+1-d+P_out.

Combine (9) and (12), paying ALL marked sides from the SAME inventory:

    sigma>=Phi-2N>=4d-P_out.                           (13)

Therefore whenever P_out<=4d this full class satisfies

    |T_sel|+|M|<=mn/2-(4d-P_out)<=mn/2.                (14)

This improves the established five-sixths coefficient to one in the
explicitly stated subclass, with additional slack4d-P_out. At the same
matching size the objective bound improves by |M|/6+4d-P_out relative
to the five-sixths theorem. The number, dimensions and orientations of
exterior negative/zero-charge sources are unrestricted; they have already
been included in Delta_out. No separate exterior budget is spent a second
time to pay G. If P_out>4d, (13) remains a valid lower bound but does not
establish coefficient one. The unrestricted grid inequality remains open.

There are genuine complete wall-tip crossings beyond the one-source cap.
Choose a_i=2+10i, fill earlier gaps by spanning U, set L=a_g+4,
D=L,F>=L+6, and add

    C=U(W,4,4), chart(r,c)=(L+5-r,c),
    Q=U(b,f,e), chart(r,c)=(L+1+e-r,c-b),

for independent even b>=6,e,f>=4. Q's right terminal consumes A's axial
support (L+1,0), its leg continues column0, and its far leg lies at
column1-b. C's left supports and Q's right outside supports on rows
L+1,L+3,L+5 consume one another. Q's unconsumed inward supports start
in column-1 at even row L+2, two rows after A's last outward support.
Its remaining outside supports are in column1 at odd rows >=L+7, beyond
C. Its far leg/supports have columns <=-4 and cannot meet the old core.
On the right the depth bound F>=L+6 isolates the remaining supports.
The old and earlier chamber support lists are unchanged. These separations
exhaust all retained supports, proving whole completeness for arbitrary
independent b,e,f. Matching coverage and endpoint degree persist.

Both added originals have charge+1. C creates three full mixed tiles and
four events on the long right side, none on the short left, so its marginal
is3. Q creates exactly three mixed tiles across columns0,1, on row pairs
{L,L+1},{L+2,L+3},{L+4,L+5}, and four directed events on the two even
rows L+2,L+4; all other contacts are immutable support exclusions. Its
marginal is3 as well. The complete exterior therefore has Delta_out=6
for unbounded b,e,f. This proves existence, not just endpoint disjointness.

The sharp exterior minimum remains between2 and5; the long-wall one-source
cap attains5. A hypothetical value below5 must have P_out<=2. With P_out=2,
integrality forces value4, N_out=4 and R_out=0. Extendibility of those
remaining patterns is open. Negative marginal examples21->20 and25->24
are compatible with the new AGGREGATE bound.

No general grid source decomposition, payment of marked-side demands
outside the stated subclass, unrestricted5/6 improvement or rectangular-grid triple equality
is claimed. The11October submitted manuscript remains unchanged.

## Validation and provenance

The source-level checker `develop/check_localized_exterior_tile_budget.py`
passed29 physical local states,136 original source images,640 complete
fusion images with72 explicit rotor mate cancellations,1087 incomplete
inventories,144 nonuniform complete chamber families and486 complete
short-wall crossings, including both reflected sides. It independently
checks direct source-labelled events, original support multiplicities,
the tile identity, regional marginals and no repeated mate tile.
It also checks13444 admissible single-source tile cuts, excludes28 cuts
that lose an old rotor mate, and verifies the complete single-rotor
counterexample to dropping that explicit hypothesis.

These finite controls corroborate the general proof above. The original
research Oracle task49a148fa returned the exterior argument as actual
gpt6/pro, with exact task/session response and original prompt matches.
The region-by-region chamber inequality and relation to prior global
theorems are further deductions here. Independent audit of this final
localized theorem is still required; a research suggestion is not review
acceptance. Formal checks and final audit status are recorded separately.
The first independent audit taskcdc1a744 terminated with no assistant
output and supplied no mathematical verdict. Final-version auditd8adad0c
in the existing independent review conversation is live and also covers
the general cut inequality and its missing-mate counterexample. No ACCEPT
is yet claimed for this new localized theorem.

The local Lean file `formal/SubQuorum/LocalizedExteriorBudget.lean` passed
18theorems and31individual declaration axiom audits without warnings,
errors,sorry or native evaluation. It proves the complete four-corner
occupancy table by kernel reduction over the81possible ternary states,
the exact local event cancellation, four general charge formulas, both
wall baseline cases, and the conditional regional/global inequalities.
The source-to-tile adapters, coordinate rotor injection, regional geometric
partition and general finite summation are written proofs, not end-to-end
Lean formalizations. The full local occupancy table itself uses no axioms.
