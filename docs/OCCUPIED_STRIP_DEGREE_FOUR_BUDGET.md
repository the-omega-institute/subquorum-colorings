# Occupied-band compensation: the sharp unported degree-four budget

26 October 2026. Wenlin Zhang and Haobo Ma. Independent research continuation.

The [cross-band matching ledger](OCCUPIED_STRIP_EXPORT_CANCELLATION.md) left
TP--TP, TP--PP and exterior matching debits. We now bound their TOTAL using
the actual ends of BB--TT forests. A transverse TP export either uses a
different physical forest end or is a degree-four TP with no BB port.
This gives a uniform half-boundary budget with only the latter exceptions.
It does not require freezing, matching closure or a receiver inside one band.

The coefficient of the exception is sharp. Explicit completely frozen,
uniquely matched families have boundary-end count b=1 or 2, exactly k
unported degree-four TP exports, and regional surplus (b-k)/2 for EVERY
k>=0. Every complete endpoint receiver is neutral, every endpoint-free tile
inside the band is saturated, and every eight-endpoint module contains an
original capacity-two tile. Thus neutral whole components and freezing do
not justify discarding a regional exterior debit. The 18-endpoint k=2,b=1
negative-surplus instance is checked from feasibility through inductive
freezing and the negative regional count in Lean.

This is a geometric refinement of the existing strip-flux and port-degree
arguments, not a new abstract matching theorem. The universal improvement
of 5/6 remains open.

## 1. Hypotheses and the physical end-incidence injection

Let (T,M) be feasible on a rectangular nearest-neighbor grid, P=V(M).
Every selected vertex has at most one occupied neighbor in T union P.
Take a two-row or two-column consecutive rectangular strip I, with n>=2
columns in its own orientation. The first column is BB and the last has
a blank corner. B means blank, not beta. TP/BP below are physical column
labels, not strand terminal types. Count ACTUAL matching edges.

Put

    S_I = n-|T intersect I|-|P intersect I|/2,
    K_I = #BB-#TT,
    b_I = 1 + indicator(last column is BB).

Thus b_I=1 or 2, including odd lengths. Form the usual BB--TT forest:
join neighboring columns if one is TT. Every TT has its two neighboring
columns BB and is internal, by feasibility and the boundary assumptions.
Every component is an alternating BB,TT,...,BB interval. There are K_I
components, and each has TWO labelled end incidences, including two sides
of an isolated BB column. Hence there are 2K_I end incidences.

Exactly b_I of these incidences point out of the strip at its blank ends.
They cannot be ports of an internal TP. If both boundary columns belong to
one alternating interval, its two incidences are still different; nothing
here assumes even length or two distinct boundary intervals.

Let e_I count TP endpoints whose actual mate is outside I. A TP is internal
under the boundary assumptions, so every such matching edge is transverse.
Let d_I count these exported TP endpoints having NO adjacent BB column.
Then d_I is exactly the number of exported TP endpoints of occupied degree
four. Indeed its selected within-column partner forces the other corner of
each neighboring column blank. A missing BB port means the endpoint-row
neighbor is occupied on that side. Together with the selected partner and
the transverse actual mate, the two occupied side neighbors give degree four.
Conversely degree four leaves no blank endpoint-row neighbor and no BB port.

For every other exported TP choose one adjacent BB port. It lies at the
facing end of its BB--TT component. Two different exported TPs cannot choose
the SAME end incidence: that end has exactly one exterior neighboring column,
which contains exactly one TP endpoint. Opposite ends of one interval remain
two HALF-debit slots of that one interval; they are not two payable units.
The b_I boundary incidences are unavailable. Consequently, with

    a_I = e_I-d_I,
    v_I = 2K_I-b_I-a_I,

we have v_I>=0. It counts end incidences not used by these chosen exports,
after removing boundary incidences. The value is independent of which one
port was chosen at a two-port export. No physical tiles have been reset,
no mate has been replaced, and no source has acquired a second resource.

## 2. Exact defect ledger and the mixed-direction union theorem

Let u_I be the BP columns not used as ACTUAL mates of TP endpoints in I.
The established injection of nonexported TP endpoints into different BP
columns gives u_I>=0 and

    2S_I = 2K_I+u_I-e_I.

Substitute e_I=a_I+d_I and the end-incidence count. This proves the new
exact ledger and its uniform consequence:

    2S_I = b_I+u_I+v_I-d_I,
    S_I >= (b_I+u_I-d_I)/2 >= (b_I-d_I)/2.          (1)

Only feasibility and the actual matching were used. In particular, if
all exported TP endpoints have degree at most three, then every such strip
has S_I>=1/2, or S_I>=1 when both ends are BB. Arbitrarily many matching
exports and arbitrary endpoint components outside the strip are allowed.
This hypothesis concerns exported TP endpoints, not all endpoints in P.

Now take finitely many VERTEX-DISJOINT strips of possibly different directions
and lengths. Write U for their union, B=sum b_I, D4=sum d_I, V=sum v_I.
Let r count actual TP-to-BP matching edges crossing from one selected strip
to another. Let u be the number of BP columns in U not used as mates of
any regional TP. The preceding joint theorem gives

    sum u_I = r+u.

Therefore the geometric joint theorem is

    2S_U = B+r+u+V-D4,
    2S_U >= B+r+u-D4.                            (2)

All r refund targets are different BP columns. All chosen forest ends are
different original incidences within their respective disjoint strips.
V>=0 and u>=0. Every term remains in this ONE physical surplus identity.
In particular neither r, u nor V is a second donor pool to add to S_U.

Equivalently let h count actual TP--TP edges ONCE, j TP--PP edges and o
regional TP endpoints matched outside U. The old edge count satisfies

    r+2h+j+o = sum e_I <= 2 sum K_I-B+D4.          (3)

Thus the remaining three debit types are now jointly limited by available
forest ends and actual unported degree-four exports. One need not bound
each debit type separately or round half-units independently.

## 3. Original-grid compensation without repeated credits

Assume the full board and U consist of original aligned 2-by-2 tiles.
Partition endpoint-bearing tiles OUTSIDE U into disjoint blocks. Let Q+
be their total positive raw charge, Q- the absolute total negative charge,
and D_out the endpoint-free deficit outside U. These are regional RAW
charges, not whole-component charges when a receiver crosses the boundary.
The original tile partition gives exactly

    2S_whole = B+r+u+V-D4 + 2D_out-2Q+ +2Q-.

Consequently

    D4+2Q+ <= B+r+u+2D_out+2Q-                  (4)

is a sufficient coefficient-one condition. The conservative version drops
the nonnegative r,u,D_out,Q- terms as appropriate. When all exported TPs
have degree at most three, the boundary budget is automatic even for
occupied strips whose receivers cross several strips or leave U.

On this explicit covered class, (4) gives |T|+|M|<=area/2, removing the old
|M|/6 allowance there. A universal geometric cover or a bound on all D4
has not been proved. Existing whole-receiver charge bounds can be reused
only for receiver blocks actually wholly outside U. The family below shows
why full-component neutrality is insufficient to erase regional charges.

## 4. A completely frozen eight-endpoint module with forced actual mates

In local coordinates put

    M0 = { (1,2)--(1,3), (1,4)--(2,4),
           (2,3)--(3,3), (3,4)--(3,5) },

    T0 = { (0,2),(0,4),(1,1),(1,5),
           (4,3),(4,5),(3,6) }.

Its eight endpoints are the vertices displayed by M0. All seven T have
one occupied neighbor. The endpoint (1,4) has occupied degree FOUR: its
neighbors are (0,4),(1,3),(1,5),(2,4). Each of the other seven endpoints
has occupied degree THREE. This degree-four exception must not be dropped.

Here is a four-layer strict freezing certificate. Each listed pair consists
of distinct nonmate neighbors. A P witness is retained when its ACTUAL mate
froze in an earlier layer.

| Layer | Endpoint | Two retained witnesses |
| --- | --- | --- |
| 0 | (1,2) | (0,2), (1,1), both T |
| 0 | (1,4) | (0,4), (1,5), both T |
| 0 | (3,5) | (4,5), (3,6), both T |
| 1 | (2,3) | (1,3), (2,4), mates in layer 0 |
| 1 | (3,3) | (4,3) in T; (3,4), mate in layer 0 |
| 2 | (2,4) | (2,3), (3,4), mates in layers 1 and 0 |
| 2 | (3,4) | (3,3), (2,4), mates in layers 1 and 0 |
| 3 | (1,3) | (1,4), (2,3), mates in layers 2 and 1 |

The actual matching is UNIQUE on this P set. In any perfect matching of
the induced P graph, leaf (1,2) forces (1,2)--(1,3); then (1,4) forces
(1,4)--(2,4); leaf (3,5) forces (3,5)--(3,4); the remaining two endpoints
force (2,3)--(3,3). This is a leaf-elimination proof, not a restriction of
the alternative matching search. The same proof is copywise below.

The local P graph contains two adjacent unit squares. Their relation to
the original tile alignment is fixed by the placement in the next section.

## 5. Sharp families for one-corner and sealed even strips

Fix k>=0. For the one-corner version set r0=0 and use a 6-by-(6k+4) board.
For the sealed version set r0=2 and use an 8-by-(6k+6) board. For i=0,...,k-1
place the preceding module by the translation

    (r,c) -> (r+r0,c+3+6i).

Add the selected bridge vertices (r0,3+6i) for i=0,...,k. Add the left
matching edge and its four selected supports

    (r0+1,1)--(r0+2,1),
    T_left = {(r0,1),(r0+1,2),(r0+2,0),(r0+3,1)}.

For the SEALED version only, put c=6k+4 and also add

    (2,c)--(1,c),
    T_right = {(3,c),(0,c),(1,c+1)}.

The fourth support of that edge is the already listed bridge (2,c-1).
Let I be the entire-width band in rows r0,r0+1. Put b=1 or 2 for the
one-corner or sealed version. Every unnamed vertex is blank.

**All-size feasibility and freezing proof.** Different modules' P sets
have no adjacency: their column spans are 5+6i,...,8+6i, separated by two
columns. Their selected supports do not touch other occupied data of the
next module; the closest right support and next left support are at row
distance two and column distance one. Each bridge has no occupied neighbor:
its two horizontal neighbors and its within-band partner are blank. The
left added pair has exactly two T supports per endpoint, and its occupied
data are separated from the first module. The sealed right pair likewise
has two T supports at each end and is separated from the last module.
Thus direct inspection of the module and these separated boundary lists
proves feasibility for EVERY k. Each module replays the displayed four-layer
certificate; the added boundary endpoints freeze at layer 0. Its forced-leaf
matching proof replays independently in each P component. No extrapolation
from the checked finite k values is used.

There are k eight-endpoint P components and b two-endpoint components,
all uniquely matched and completely frozen. Exactly k endpoints have degree
four; all 7k+2b others have degree three. The whole-board counts are

    |T|=8k+2+3b,     |M|=4k+b,     |P|=8k+2b.

In the chosen band, direct columns give

    n=6k+2+2b,    |T intersect I|=5k+2+b,    |P intersect I|=3k+b,
    #TP=2k+b,     #BP=k,     #TT=0,     #BB=K=b,
    e=k+b,       a=b,        d=k,       u=v=0.

The sole extra degree-four export per module is its right TP. The b added
boundary TPs have one BB port each; their chosen ports occupy all nonboundary
forest ends. The b=2 band has even length and both ends BB. It follows that

    2S_I = b-k = b+u+v-d.                         (5)

Therefore (1) is sharp for EVERY k and BOTH boundary types. Taking k>b
gives negative regional surplus. For any integer A>=0 take k=b+2A+1;
then S_I=-A-1/2. Freezing, uniqueness of the actual matching, sealed even
ends and neutral complete receivers do not impose a fixed lower bound
independent of d. The failed rule is omission of the degree-four/exterior
debit, not the grid inequality.

## 6. Exact capacity-two and inside/outside physical accounting

Original tiles always start at even row and column coordinates. For each
module let C=3+6i. Its two upper-band receiver tiles have total raw charge
+1/2: their counts are (t,p)=(2,1) and (1,2). Its two lower receiver tiles
have counts (0,4) and (1,1), of charges 0 and -1/2. Thus the receiver is
NEUTRAL, and its all-P original tile is a genuine capacity-two tile. Its
negative half-unit lies OUTSIDE I and occurs in a different original tile
for every module.

Each added boundary pair also has a neutral complete receiver; its band
part has charge -1/2 and its exterior part +1/2. All receivers are tile-
disjoint. Every endpoint-free tile inside I has two diagonal selections:
the bridge and the next left support, including the left prefix tile of
columns 2,3. Therefore the exact physical inventory is

    D_I=0,     rho_I=(k-b)/2,     rho_out=(b-k)/2,
    every complete receiver charge=0.

For the one-corner board D_out=6k+6 and S_whole=6k+6. For the sealed board
D_out=12k+14 and S_whole=12k+14. In each case

    S_whole = S_I + D_out - rho_out.

The exterior signed charge cancels its own regional partner exactly once.
Replacing rho_out by the COMPLETE component charge zero, while keeping S_I,
would lose this half-unit transfer. Conversely one must not add the full
receiver and its regional negative piece as two independent credits.
This explicitly connects occupied-band loss, original capacity-two tiles,
and a verifiable outside compensation location without asserting full routing.

## 7. Verification, scope and the next mathematical question

The saved run checks 990 geometric port budgets and joint ledgers, including
806 exhaustive two-strip matching controls, 80 disjoint mixed-direction
region controls and the earlier cross-band refund families. It allocates
561 actual forest-end incidences and checks 622 unported degree-four TP
occurrences, 6,594 strict freezing events and 1,878 forced actual matching
edges. The sharp family is checked at k=0,1,2,3,4,5,8,16,64,128 with both
boundary types, plus 48 transported isometries. Six small instances also
have an independent perfect-matching count of one. Finite checks only
corroborate the general injection and coordinate proofs above.

Lean 4.33.0 passes ten audited declarations, with only standard propext and
Quot.sound, no sorry, native evaluation, added axioms or warnings. For the
concrete k=2,b=1 instance it verifies matching geometry and T feasibility,
all 18 endpoints INDUCTIVELY frozen, its actual two degree-four endpoints,
and the regional surplus -1/2. Generic arithmetic covers the port ledger,
mixed union, raw original-grid implication and all-k sharp count. The general
forest-end injection, geometric separation for all k, forced matching
uniqueness and full receiver accounting remain written proofs with executable
checks; the general theorem is not end-to-end Lean. Local memory and actual
comm-basename lean/lake checks precede every Lean executable invocation.

The open target is now more specific: cover the unported degree-four TP
exports by UNUSED physical slack, accounting for shared forest ends and
whole receivers crossing U. The family shows that full freezing alone does
not bound their number, and complete receiver neutrality alone does not
remove their regional cost. Its outside neutral-pair half-units do repair
this family; a general ownership/injection theorem for such exterior pieces
has not been established. Existing full-pool unpaid-alpha obstructions still
rule out assuming universal full routing from freezing alone.

Artifacts:

- [Physical validator](../develop/check_occupied_strip_degree_four_budget.py)
- [First sharp negative instance](../develop/fixtures/frozen_strip_degree_four_sharp_q2.json)
- [Lean source](../formal/SubQuorum/OccupiedStripDegreeFourBudget.lean)
- [Physical validation](../output/occupied-strip-degree-four-budget-validation.json)
- [Lean validation and exact scope](../output/occupied-strip-degree-four-budget-formal-validation.json)

Reproduce:

    PYTHONDONTWRITEBYTECODE=1 python3 develop/check_occupied_strip_degree_four_budget.py --output output/occupied-strip-degree-four-budget-validation.json
    PYTHONDONTWRITEBYTECODE=1 python3 develop/check_occupied_strip_degree_four_formal.py --lean /path/to/lean-4.33.0 --output output/occupied-strip-degree-four-budget-formal-validation.json

No correspondence operations, submitted-manuscript revisions, public main,
PR #3, shared CI or C4/star-forming changes are part of this continuation.
