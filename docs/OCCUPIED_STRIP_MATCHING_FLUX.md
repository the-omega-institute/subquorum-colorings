# Occupied two-row strips: a sharp mixed-column matching flux

**Continuation:** [cross-band export cancellation](OCCUPIED_STRIP_EXPORT_CANCELLATION.md)
allows a receiver to cross several strips. A TP export matched to a BP column
in their disjoint union is refunded once; only TP-TP, TP-PP and exterior TP
mates remain as debits. Their coefficients have frozen sharp controls. This
extends the geometric sufficient class without asserting universal full routing.

22 October 2026. Authors: Haobo Ma and Wenlin Zhang.

The neutral-portal corridor theorem required endpoint-free corridors. Here
we allow arbitrary occupied columns and prove a general regional inequality.
The precise obstruction is a matching edge leaving a column containing one
selection and one endpoint. It creates a half-unit debit. We identify that
debit exactly, prove closed-strip bounds, and give an all-width terminal
counterfamily to omitting it. A receiver-closure criterion then permits
occupied corridors in an original-board compensation argument.

## 1. Region, labels and column counts

Let(T,M) be any feasible pair on a rectangular nearest-neighbor grid:
T is disjoint from P=V(M), M is a matching, and each selected vertex has
at most one occupied neighbor in T union P. No terminality assumption is
needed for the local theorem. Take a two-row region I with n>=2 consecutive
vertex columns. Its first column is blank in both rows, and at least one
corner of its last column is blank. Blank excludes both T and P.
The exterior may be any feasible configuration.

Use the following column types, with either vertical order allowed:

| Count | Column | Selected plus half-endpoint weight |
| --- | --- | --- |
| A | TT | 2 |
| B | BB | 0 |
| C | TP | 3/2 |
| D | BP | 1/2 |
| E | BT | 1 |
| F | PP | 1 |

Here B in a column label means blank; the count B is the number of BB
columns. Thus n=A+B+C+D+E+F. Write

    S_I=n-|T intersect I|-|P intersect I|/2.

Let e be the number of TP columns whose endpoint is matched outside I.
This is an actual matching incidence, not a count of endpoint adjacency
edges. Each TP column has exactly one endpoint. A TP column cannot be the
first or last column under the boundary assumptions, so such a matching
exit is transverse to the two-row band, not through a column end.

## 2. Matching gives a distinct BP mate for every nonexported TP

The endpoint of a TP column cannot match its vertically adjacent selected
vertex. If its mate lies inside I, it is horizontal. The selected vertex
in the TP column already sees its endpoint neighbor; therefore the neighbor
in that selected row must be blank. The mate column is consequently BP.
Distinct nonexported TP endpoints have distinct mates, and a BP column has
only one endpoint. This gives an INJECTION into BP columns:

    C-e<=D,       u=D-C+e>=0.                            (1)

This is where actual matching matters. Replacing a mate by any occupied
neighbor would not prove the injection. A BP endpoint can be the mate of
at most one of these TP endpoints even if it has other endpoint neighbors.

The exact column identity is

    S_I=B-A+(D-C)/2,
    2S_I+e=2(B-A)+u.                                    (2)

All terms refer to the single original configuration. Neither u nor e is
a new independent physical donor; u records the unused BP count in(1),
while e is a debit when estimating S_I.

## 3. The BB--TT forest gives the boundary surplus

Every TT column has both horizontal neighboring columns BB: its two
selections already see each other, so all their horizontal neighbors must
be unoccupied. TT cannot be at either end of I. Form the graph with one
vertex for every BB or TT column, joining neighboring columns when one
is TT. It is a subgraph of the column path, hence a forest. Every TT
vertex has degree two. With A TT vertices, B BB vertices and 2A edges,
its number of connected components is B-A. The first BB column makes
this nonempty, and hence

    B-A>=1.                                             (3)

If the last column is also BB and n is even, B-A>=2. Indeed equality
B-A=1 would put both boundary BB vertices in one connected alternating
BB/TT path. Connecting the first and last columns in a subgraph of the
column path forces every column of I into that path. It would have
one more BB than TT and therefore odd length, a contradiction.

This parity qualification is necessary. For odd n, alternating BB,TT,
...,TT,BB has both ends blank and only one unit of S_I.

## 4. General flux theorem and the closed-strip consequences

Set delta=1 in the one-corner case, or delta=2 when both end columns
are blank and n is even. Equations(1)--(3) prove, for arbitrary lengths,

    S_I >= delta-e/2.                                   (4)

In particular, if no TP endpoint is matched outside I, S_I>=delta.
Full matching closure of I implies this condition, but is stronger than
necessary: exported endpoints of BP or PP columns do not create this
mixed-column debit.

If M_in consists of matching edges wholly inside I and a is the number
of all matching edges with exactly one endpoint in I, then
|P intersect I|=2|M_in|+a and e<=a. Consequently the theorem also gives

    |T intersect I|+|M_in|+(a-e)/2 <= n-delta.            (5)

Thus |T intersect I|+|M_in|<=n-delta even without matching closure.
Under matching closure a=e=0, this is the earlier closed-strip candidate:
the exact selected-plus-matching objective has a one-unit boundary surplus,
or two with sealed even length. The proof is the all-length injection and
forest argument; finite searches are not its justification.

## 5. A sharp all-width terminal obstruction to dropping the debit

For every even n>=4 use the4-by-n board. Put

    M={ (1,1)--(2,1) },
    T={ (0,1),(2,0),(3,1) }
       union { (1-(j mod2),j) : 2<=j<n }.

All unlisted vertices are blank. The occupied endpoint graph is the single
matching edge. Endpoint(1,1) sees selected(0,1),(1,2), and endpoint(2,1)
sees selected(2,0),(3,1). Each of these selections sees only its endpoint;
the remaining alternating selections are isolated. Thus the pair is
feasible, each endpoint has degree three, the matching is unique, and both
endpoints freeze immediately. It is fully exchange-terminal.

Take I to be its first two rows. Its columns are BB,TP,BT,TB,BT,TB,...
and the last lower corner is blank. Exactly one TP endpoint is exported,
so e=1, B-A=1,u=0 and

    |T intersect I|=n-1, |P intersect I|=1, S_I=1/2.

The debit-free claim S_I>=1 fails, and(4) is exact. In fact every
endpoint-free physical tile in I is saturated: D_I=0.

For the sealed variant remove the last selected vertex(0,n-1). Both
boundary columns are then BB, B-A=2,e=1,u=0 and S_I=3/2. This refutes
the debit-free sealed claim S_I>=2 and again attains(4).

These are counterexamples to the proposed REGIONAL debit-free rule, not
to the global half-area target. In the first family total T=n+1,M=1,
so the actual global margin is n-2; the sealed variant has margin n-1.
The complete endpoint receiver has charge0 in both. Its upper-band raw
charge is-1/2 and its lower-band raw charge is+1/2. Counting the former
as a whole negative component while omitting the latter would be another
incorrect payment rule. The finite verifier records both sides explicitly.
During direct feasibility checking the alternating row phase was corrected
to1-(j mod2); the opposite phase gives selected(0,1) two occupied neighbors
and is not feasible.

## 6. Original physical ledger and occupied corridor compensation

When I is a union of original physical tiles, define D_I using only its
endpoint-free tiles, and define the RAW regional receiver charge

    rho_I=sum_(Q in I, Q meets P)(|T intersect Q|+|P intersect Q|/2-2).

Direct tile summation gives S_I=D_I-rho_I. Therefore(4) is the exact
kind of regional correction needed in occupied bands:

    D_I-rho_I >= delta-e/2.                              (6)

The raw rho_I need not be a whole-component charge. Do not add its
negative part as an independent resource while retaining the full charge
of that same component elsewhere.

Here is a sufficient ORIGINAL-component closure application. Start with
a single-terminal pair and its complete original endpoint receivers.
Choose tile-disjoint two-row or two-column regions I_j satisfying the
boundary hypotheses. Require that every original endpoint component
meeting their union has its ENTIRE physical receiver contained in one
I_j. Their matching edges then stay inside that region, so e_j=0.
Receiver closure is a hypothesis to verify, not inferred from terminality.

For the remaining components outside all I_j let q be the sum of their
positive charges and R_out the absolute sum of their nonpositive charges.
Let D_out be the original endpoint-free deficit outside these regions.
The physical ledger splits exactly as

    mn/2-|T|-|M| = sum_j S_(I_j)+D_out-q+R_out
                 >= sum_j delta_j+D_out-q+R_out.         (7)

Thus q<=sum_j delta_j proves coefficient one. All internal component
charges, whatever their sign, have already entered the regional S terms;
they are not added a second time as R_out. The disjoint regions use each
original donor tile once. Mixed region directions are permitted subject
to that physical disjointness. No crossing or nesting coverage theorem
is asserted here.

In particular the neutral elbow portal can have occupied corridor tiles
if all foreign components meeting that corridor have complete receivers
inside it and the root is a separate complete original component whose
receiver is disjoint from the corridor. The root is exactly the prescribed
elbow together with its attached neutral pair, not a component that may
acquire additional endpoints in the corridor. The
native supports still seal the entry and block the final lower corner.
For H4 the final upper corner cannot be selected because it sees two root
endpoints; receiver closure also excludes its being a foreign endpoint
connected to that outside root, so it is blank. Hence delta2 is retained
at H4, delta1 at H>=6. One such corridor pays the root's charge1 when
all other outside components are nonpositive. Arbitrarily many complete
neutral components inside it are allowed.

## 7. A genuine occupied neutral family

Take the neutral-pair elbow family with even H>=4 and even W>=6r+16, r>=1.
For i=0,...,r-1 set j=11+6i and add the isolated horizontal matching pair

    (8,j)--(8,j+1),
    selected supports (8,j-1),(7,j),(8,j+2),(9,j+1).

The two endpoint receiver tiles are wholly in the portal corridor. They
contain respectively one and two selections, so the complete component
charge is1+3-4=0. Its fourth support(7,j) is outside its receiver. Each
endpoint sees its mate and two distinct selections, so both freeze at once.
These supports have exactly their own endpoint as occupied neighbor.

Successive endpoint pairs are six columns apart; all occupied data of
one lie in columns j-1..j+2. Consecutive supports are separated by at
least three in Manhattan distance. The first pair is separated from the
portal at columns4..7; the last data reach at most6r+7, while the root's
nearest right-leg support column is W+2>=6r+18. No endpoint components
join, no selections coincide or acquire another occupied neighbor. Every
vertex lies in the board(H+8)-by-(W+12).

The root component has charges1+0=1, each new component charge0. Unique
matching and full freezing follow for all parameters. Exact whole counts
are M=W+H+r and T=H+7+4r. Equation(7) proves coefficient one despite the
occupied corridor, using its original regional balance once.

The new theorem removes endpoint-freeness for matching-closed regional
balance, and for the stated receiver-closed compensation class. It does
not extend the previous first-stop directional injection across occupied
tiles: a marker can now lie inside another occupied route. Controlling
transverse exits, partial component receivers and overlapping occupied
regions remains open. So do unrestricted grid compensation and the
proposed grid triple equality.

## 8. Verification and formal scope

Run the finite controls with

    PYTHONDONTWRITEBYTECODE=1 python3 develop/check_occupied_strip_matching_flux.py --output output/occupied-strip-matching-flux-validation.json

They check1168regional models, including all feasible labels and all partial
matchings with transverse completions at lengths2..4, and all closed
matchings at length5. There are198mixed-export and280nonmixed-only export
models. The explicit terminal counterfamilies cover98even-width/sealing
parameter pairs through width100,48symmetry images and15odd sealed parity
obstructions. The genuine occupied family has54parameter triples,
108feasible selection extensions and32images,194receiver-closed models in
total. Original receivers, matching closure, signed ledger and unique frozen
matching are checked directly. These finite controls support, and do not
replace, the arbitrary-length proofs above.

The local Mac run of formal/SubQuorum/OccupiedStripMatchingFlux.lean passes
12theorems and12individual axiom audits with Lean4.33.0, no warnings,
no sorry and no native evaluation. It proves an arbitrary-length column-trace
invariant, sealed parity, finite local TP feasibility and the exact arithmetic
consequences. The grid-to-trace adapter, actual mate injection/cardinality,
physical receiver ownership and coordinate examples remain written proofs.
The execution receipt is output/occupied-strip-matching-flux-lean.json.

The independent written review is tracked separately; it does not certify
verifier or Lean execution. The original review independently identified
the same alternating-phase error, explicitly verified the corrected family,
and confirmed the general theorem and receiver-closed application. Its full
response and exact request/stream/task/session checks are archived in
output/occupied-strip-matching-flux-initial-review.json. The extra follow-up
with the corrected complete note was cancelled by the service without any
execution or answer; no extra acceptance is inferred. Its original handle
was retained until authoritative terminal status, as recorded in
output/occupied-strip-matching-flux-review-live.json. The corrected proof
is also supplied in full as a dependency to the separate native transverse
band theorem review.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
