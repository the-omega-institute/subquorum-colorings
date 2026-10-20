# Full-bar consumers: exact clearance and a complete unactivated exit

21 October 2026. The unrestricted allocation mu=N+R-G>=0 and the grid
triple equality remain OPEN. This note classifies full-bar gate consumers
and gives a complete connected counterexample to two candidate local rules:
full-bar consumption need not activate the positive producer's terminal,
and its forced next support consumer need not leave a positive defect in
the adjacent terminal tile. Neither failure is an allocation counterexample.

## 1. Model and an all-dimension classification

Use the complete original-source hypotheses and persistent occupancy of
[source retention](SOURCE_RETENTION_HORN_CLOSURE.md), the fixed aligned
physical tiles, and [canonical gate consumption](MARKED_SIDE_GATE_CONSUMPTION.md).
Normalize the positive producer to A=U(w,l,l'), its gate t=(3,2), and its
incident terminal (l,1). Widths are even and at least six; both incident
and far leg lengths are independently even and at least four.

Suppose an original U consumer contains ALL four corners of the physical
tile {2,3} squared. After naming its incident leg, it has exactly one form:

| Form | Consumer and frame | Necessary endpoint clearance |
|---|---|---|
| Horizontal | Fh=U(d,a,b), (r,c)->(r+2,c+1) | d<=w-2 |
| Vertical | Fv=U(d,a,b), (r,c)->(c+1,r+2) | a<=w-4 |

Both are negative U sources of charge minus one. No row-shifted bar mass
is introduced by these full-tile contacts.

Proof. A full original U tile lies in its two-row bar: separate stems at
distance at least five cannot supply a full two-by-two tile. A horizontal
bar must have rows2,3. Its column interval contains2,3 but cannot contain
column1, which the producer already owns on both rows. It therefore starts
at column2. Upward legs meet the producer's row-one bar, so they point down.
Avoiding the producer's far stem at(2,w) forces d+1<w; evenness gives
d<=w-2. For a vertical bar the identical argument uses columns2,3 and the
producer's row-one endpoints: its row interval starts at2. Leftward legs
meet(2,1), so they point right. The near leg must stop before(2,w), giving
a+2<w and hence a<=w-4. The original profile catalogue gives charge minus
one in both transported frames. These arguments impose no upper dimension
or source-count bound and do not require the producer-consumer pair to be
feasible by itself.

## 2. Unactivated producers force a next consumer, not an immediate receipt

If A's incident terminal is UNACTIVATED, its two original terminal supports
(l,0),(l+1,1) remain selected. In particular(l+1,2) must be unoccupied:
otherwise(l+1,1) sees both its anchor(l,1) and that additional neighbor.

The original occupied column of Fh includes every row2 through a+3 at
column2, including its beyond-tip support at(a+3,2). Thus a>=l-2 would
occupy(l+1,2). Evenness proves the stronger clearance a<=l-4. Now its
support(a+3,2) has its own anchor(a+2,2) and producer endpoint(a+3,1),
since a+3<=l-1. Complete feasibility forces that support to be consumed
by another original endpoint owner.

For Fv its bar occupies column2 on rows2 through d+1. If d>=l it occupies
(l+1,2), so an unactivated producer requires d<=l-2. Its original bar-end
support(d+2,2) then has its own anchor(d+1,2) and producer endpoint(d+2,1).
It too must be consumed. In either form l>=8.

These are forced ownership transitions. They do NOT create an activation
unit or a nonfull-defect unit merely by forcing another endpoint. The
following complete example exhibits the missing payment explicitly.

## 3. An explicit complete connected eight-source obstruction

The table specifies actual original sources, including their unchanged
matchings and all mandatory supports. The U constructor is the one in
Section1; the final endpoint and support sets are their mandatory unions.

| Owner | Dimensions (width,near,far) | Map of original point(r,c) | Charge |
|---|---|---|---|
| A | (14,8,4) | (r,c) | 1 |
| B | (6,4,4) | (c+1,r+2) | -1 |
| C | (6,4,4) | (4-r,c+14) | -5 |
| D | (6,6,4) | (c+1,r+7) | -5 |
| E | (6,6,4) | (9-c,13-r) | 1 |
| F | (6,8,4) | (14-c,6-r) | -5 |
| G | (8,4,4) | (c+4,18-r) | -7 |
| H | (10,4,4) | (c+8,11-r) | 1 |

There are184 pairwise distinct original endpoints,92 unchanged lattice
matching edges and40 final selected supports. Every surviving selected
point has exactly one occupied neighbor; every endpoint has at least
three. The endpoint graph is connected. Starting with{A,B}, its exact
least feasible Horn hull consists of ALL eight listed owners. No partial
pattern, optional support omission or pairwise-feasibility approximation
is used for this example.

B owns every corner of A's gate tile, including t=(3,2), so the side is
actually marked. However both(8,0) and(9,1) remain selected. A's left
terminal(8,1) is therefore unactivated. This already refutes the rule
that a full-bar gate must activate its producer's incident terminal.

This is the tight vertical clearance d=l-2=6. B's forced support q=(8,2)
is indeed consumed, by F. But in Q={8,9} by{2,3} the exact final profile is

    (8,2): F endpoint       (8,3): F endpoint
    (9,2): unoccupied       (9,3): F selected support.

This is one ORIGINAL REGULAR2P1T pair. It contributes zero to each of
L1,2L2bar,2L2mutual,L3,U0,Z0 and to positive activation A in the exact
geometric reserve. Treating the two endpoints as an irregular2P0T pair
would incorrectly create two units. Thus even this tight forced transition
does not guarantee a positive defect in its adjacent exit tile.

The general [path allocation](ROTOR_TRANSFER_AND_NEGATIVE_U_PATH_ENDINGS.md)
has one P edge, two negative-U sinks, five paths, one bad isolated path
and unmarked-path surplus five in this example. A's unactivated marked
left side is precisely that isolated bad path: it has neither an incoming
activation transfer nor an outgoing positive/rotor gate transfer.

## 4. Exact target status and verification

The actual global counts are

    N=3, G=3, A=4, U0=3, Z0=0,
    L1=2, L2bar=13, L2mutual=0, L3=3,
    C=34, R=19, mu=19.

The path identity is38=34+5-1. All resources in C are actual existing
occurrences, used once. Thus the example refutes the TWO LOCAL RULES,
not mu>=0 and not any grid statement. It supplies no universal improvement
of the existing5/6 bound. No minimality among source counts is claimed.

Run python3 develop/check_fullbar_unactivated_obstruction.py. Independent
matching/support reconstruction checks the complete certificate, exact
reserve, actual marks and Horn hull. All32 phase/isometry images remain
complete feasible; eight preserve the positive producer and the displayed
obstruction. The other24 are controls, not instances of the positive-side
claim.66distinct anchored full-bar consumers,720endpoint-disjoint producer
patterns and300unactivated-clearance patterns check the written catalogue
within the stated finite dimension library; the general proof is Section1-2.

formal/SubQuorum/FullBarUnactivatedObstruction.lean independently constructs
all eight sources and checks their concrete endpoint/matching/support data,
complete feasibility, full gate consumption, unactivated terminal and the
regular exit-pair profile by ordinary kernel reduction. This is a finite
counterexample certificate; it does not formalize the unbounded catalogue,
the global event-reserve adapter or rectangular-grid equality. Execution
and axiom status are recorded separately in the formal receipt.

SAT was used only to discover the eight-source manifest. The permanent
checker and Lean certificate do not call SAT. The earlier smaller discovery
library returned UNSAT; that excluded only that bounded library and is
superseded as a lead by this complete witness. No general obstruction was
inferred from it.

Next: analyze longer negative-U/full-bar continuations and actual persistent
caps/strips. A complete Oracle research response proposes such a corridor
theorem and parameterized families; it is archived as an unadopted research
lead until its geometry and nonreuse are independently reconstructed. Keep
the exact residual obligation Bbad<=C+Sunmarked and do not count a forced
regular pair as new capacity.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
