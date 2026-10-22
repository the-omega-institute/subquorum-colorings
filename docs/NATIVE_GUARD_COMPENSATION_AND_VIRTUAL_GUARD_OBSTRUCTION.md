# Native-guard compensation and a virtual-guard donor obstruction

22 October 2026. Authors: Haobo Ma and Wenlin Zhang.

This note combines the even-bridge reduction with an original-board physical
payment lemma, then shows why its native-support hypothesis matters. General
proofs are provided; finite controls and scoped Lean results are auxiliary.

The complete written theorem and two-elbow obstruction received an independent
ACCEPT; see output/native-guard-compensation-oracle.json. A subsequent, separate
construction in NEUTRAL_PAIR_DONOR_SATURATION.md shows that a zero-charge
neighbor can also erase a local unit donor by saturation. That later result
is outside this accepted review's scope.

## 1. Completed pieces and original selections

Use the setting and all-even-bridge decomposition of
EVEN_BRIDGE_SUPPORT_COMPLETION.md. The original pair is feasible and
single-terminal on an even-by-even rectangle. The endpoint sets K partition
P. Every edge between different pieces is a removed even bridge, and

    mn/2-|T|-|M|=D-sum_K rho(completed K),                     (1)

where D counts endpoint-free deficits in the ORIGINAL pair only.

A completed selection is native if it belongs to original T. The other
completed selections are virtual supports: original endpoints in other
pieces. They are selected only in the completed pair. This distinction
does not affect charge additivity, but does affect physical donor transport.

Let Q={0,1}x{0,1} be a physical tile in local coordinates. A capped-corner
witness for one completed piece K consists of

    (-1,-1),(-1,0),(-1,1),(-1,2),(0,-1) in K,
    q=(1,-1) selected in the completed K,
    (0,0),(0,1) not in K.                                    (2)

Allow all eight tile-preserving orientations. The existing completed-pair
local donor lemma says Q has no K endpoints and at most one completed
selection. We ask whether Q is still an endpoint-free donor originally.

## 2. Native support lifts the physical donor

**Native-guard lifting lemma.** If the support q in (2) belongs to ORIGINAL
T, then Q contains no original endpoint and at most one original selection.
Its original physical deficit is at least one.

Proof. First show the two upper corners contain no foreign endpoints.
The corner a=(0,0), if an original endpoint outside K, would form the
endpoint cycle

    a--(-1,0)--(-1,-1)--(0,-1)--a.

Its edges incident to K would be edges between pieces lying on a cycle,
contradicting the fact that every such edge is a bridge. It cannot belong
to K by (2), nor be selected because it sees two K endpoints. Thus a is
originally blank.

Suppose b=(0,1) is an original endpoint. It is foreign, by (2). Set
x=(0,2). If x were an endpoint, the four-cycle

    (-1,1)--b--x--(-1,2)--(-1,1)

would contain the cross-piece edge (-1,1)--b, again impossible. If x were
selected, it would see both b and (-1,2), violating feasibility. Hence x
is blank. The two blank neighbors a,x leave b occupied degree at most two,
contradicting single terminality. Therefore b is not an original endpoint.
This argument also works if x is outside the board: it is then blank.

The native selected q already sees (0,-1), so c=(1,0) is blank. If d=(1,1)
were an endpoint, b could not be selected because it would see both d and
(-1,1). Then d would have two blank neighbors b,c, impossible. Thus Q is
endpoint-free. Only b,d can be selected, and they cannot both be selected:
b already sees (-1,1). The original deficit is at least one. QED.

Notice where the bridge hypothesis enters: it excludes foreign endpoints
in the upper row. The original whole-component lemma assumed those two
corners excluded globally; after cutting, that exclusion must be proved.

**Native-owner injection.** Two native-guard witnesses for different completed
pieces cannot claim the same physical Q, even when the two pieces belong
to the same original endpoint component.

Proof. Equal full sides give the same four-point run. Adjacent full sides
have extended runs meeting at their common exterior corner. Either case
shares an endpoint, so the pieces coincide. With opposite full sides,
rotate the first witness into (2). The other run includes (2,-1). The
native selected q=(1,-1) would see both (0,-1) and (2,-1), impossible.
This covers every orientation and proves injectivity. QED.

## 3. A compensation theorem for completed positive cores

**Theorem.** Suppose every completed piece K with positive receiver charge
has rho(K)<=1 and a capped-corner witness whose support is native. Other
pieces may have arbitrary shape and nonpositive charge. Then

    |T|+|M|<=mn/2.                                          (3)

Proof. Choose one native witness per positive piece. Section2 assigns
distinct original endpoint-free tiles, each of physical deficit at least
one. If there are b positive pieces, then

    sum_K rho(K) <= sum_(rho(K)>0)rho(K)
                 <= b <= sum_(chosen Q)d_Q <= D.

Substitute in (1). Each original tile is paid once. No completed-board
deficit, interface correction chi or raw matching-block buffer is added
as a second supply. QED.

The theorem does not require an upper bound on the charge of an entire
original endpoint component: its charge is the signed sum of its completed
pieces. It handles differing orientations and arbitrarily many even bridges
by the already proved decomposition. On this precisely stated class it
replaces the existing coefficient5/6 by1, removing |M|/6 of loss. It does
not prove the unrestricted compensation inequality or a new universal
coefficient. Whether a given configuration belongs to this class is a
geometric hypothesis to verify, not an automatic consequence of terminality.

## 4. A virtual guard can hide occupied donor corners

Here is an all-parameter exchange-terminal obstruction to dropping the
native-guard hypothesis from the DONOR-LIFTING rule. The target inequality
will hold with a strict surplus.

Write E(w,h) for the standard elbow from ELBOW_SOURCE_COMPENSATION.md:

    P(w,h)=({0,1}x{0,...,w-1})
           union ({2,...,h-1}x{w-2,w-1})
           union {(2,0),(h,w-1)},

with selected supports

    (0,-1),(0,w),(2,-1),(3,0),(h+1,w-1),
    (r,w) for even r in[2,h],
    (r,w-3) for odd r in[3,h-1].

Use its prescribed unique matching: top-row pairs at columns0,2,...,w-2;
bottom-row pairs at columns1,3,...,w-3; the left short tip paired upward;
right-column pairs starting at rows1,3,...,h-1; inner-column pairs starting
at rows2,4,...,h-2. The all-length leaf-forcing and freezing proofs of the
standard elbow establish uniqueness and terminality for these data.

For precision, an explicit leaf-forcing order proving uniqueness starts
with(2,0)--(1,0). For j=0,...,w-2 force the edge
(j mod2,j)--(j mod2,j+1), in this order: its left endpoint has lost its
upper/lower and preceding horizontal neighbor and is a leaf. Next force
(1,w-1)--(2,w-1). For r=2,...,h-1, force
(r,w-2)--(r+1,w-2) when r is even, and
(r,w-1)--(r+1,w-1) when r is odd. The lower strip has the same alternating
leaf recurrence; its final odd-r edge contains the bottom tip. This consumes
exactly all2w+2h-2 endpoints, proving uniqueness for every width and height.

Choose even w>=6,h>=4,W>=w+6,H>=4. Place the outer E(W,H) at offset(4,5),
and the inner E(w,h) at offset(7,5). For the inner elbow, replace its
top-left exterior support(7,4) by the support p=(6,5). Its top-left endpoint
is q=(7,5). Take the union of the matchings and the union of selected sets,
removing selections that are now endpoints. Exactly two supports are consumed:
outer support q and inner support p. The two endpoint sets are disjoint,
and their only cross-edge is p--q.

The construction fits in an even rectangle with

    rows=max(H+8,h+10), columns=W+12.

### Feasibility, uniqueness and terminality for all parameters

The inner occupied region starts at row7, except for its new support p in
row6. The outer bar is in rows4,5, and its only endpoint below the bar
near column5 is p. Its thick right strip is in columns W+3,W+4; the
inner endpoints reach at most column w+4 and its right supports reach
w+5. The inequality W-w>=6 leaves at least three columns between the
inner supports and the outer inward supports at W+2. The outer left
support nearest the inner data is(6,4), while the nearest retained inner
left support is(9,4); the deleted inner(7,4) is precisely the site that
would have violated this separation. Thus retained selections acquire no
extra occupied neighbor, and both p,q simply exchange an occupied selected
neighbor for an occupied endpoint. Feasibility and single terminality follow.

In the completed inner pair, moving its original top-left support from
the west neighbor to the north neighbor preserves the standard elbow
freezing argument. That support is used only to freeze the top-left
endpoint, together with the mate of the left short tip. It is still
distinct from that second witness and still adjacent. All other freezing
witnesses are unchanged. The endpoint graph and its unique matching are
unchanged as well. The completed outer pair is exactly the standard elbow.

The only cross-edge p--q is an even bridge. Perfect-matching factorization
and terminality equivalence therefore show that the whole construction has
exactly one perfect matching and admits no feasible nonempty exchange.
This conclusion is for every parameter choice, not a finite observation.

Every body edge of either elbow lies on an endpoint unit square; its only
other edges are the two leaf-tip edges, whose cuts are odd. Thus p--q is
the only even bridge of the joined construction. The two displayed sides
are exactly its completed even-bridge-irreducible pieces.

### The lost donor and exact signed payment

In the completed outer elbow the actual tile

    Q={6,7}x{6,7}

has no endpoints and no selections, hence local deficit2. It is the capped
corner donor with virtual support q=(7,5). In the ORIGINAL configuration,
(7,6),(7,7) are inner endpoints. Thus Q is endpoint-bearing and supplies
NONE of the original endpoint-free deficit D. All the other witness vertices
remain outer endpoints. This is a direct failure of donor lifting despite
unique matching and full exchange terminality.

Nevertheless its signed ledger is favorable. The completed outer elbow
has charge1. For the completed inner elbow, its endpoints number2w+2h-2,
its receiver has w+h tiles, and it has h+2 selections in that receiver.
To count tiles, its first two physical row bands each meet w/2+1 column
bands; the remaining h/2-1 row bands each meet two. The receiver selections
are its new north support, top-right support, short-tip west support,
h/2 outer-leg supports, and(h-2)/2 inner-leg supports. Its lower short-tip
and bottom-tip supports lie outside the receiver. Hence

    rho(inner)=(w+h-1)+(h+2)-2(w+h)=1-w,
    rho(whole)=1+(1-w)=2-w.

There are H+h+6 original selections and W+H+w+h-2 matching edges.
Equation(1) gives

    mn/2-|T|-|M|=D+w-2>=w-2>=4.                         (4)

So this is a counterexample to the proposed donor transport rule, not
to the native-guard theorem or the half-area target. The correct accounting
retains the negative inner charge once; it does not spend the vanished
capacity2 donor, then spend the same negative charge again. The virtual
guard branch needs an aggregate signed argument or further geometry.

## 5. Scope and next question

The native-guard theorem supplies one complete physical compensation rule
after even-bridge decomposition. The explicit virtual-guard family explains
why local donor certificates cannot all be transported automatically. It
does not show that every virtual guard is harmful, or that every occupied
local donor can always be paid by its neighboring core's negative charge.
Those broader assertions remain to prove or refute. In particular the
unrestricted inequality X<=D+B+2J is still open.

## 6. Reproducibility and formal scope

Run

    PYTHONDONTWRITEBYTECODE=1 python3 develop/check_native_guard_compensation.py --output output/native-guard-compensation-validation.json

The suite passes1339input models and1677completed pieces, including all
1086small endpoint-box controls,121native witness checks,49nonvacuous
compensation cases,180obstruction parameter quadruples and32obstruction
symmetry images. It checks7920rows of the explicit all-length leaf template
and17184independently chosen leaf-forcing edges. All572tested whole/side
pairs in those obstruction controls have a forced unique matching and a
complete freezing certificate. The reference quadruple is(W,H,w,h)=(12,8,6,4),
with completed charges1,-5 and whole charge-4.

NativeGuardCompensation.lean passes11theorems and11individual axiom audits.
It checks local label implications excluding a foreign upper corner, the
native-support donor label bound, the opposite-run contradiction, the
original-board payment implication, all-width donor endpoint/selection
coordinates, and the exact count/surplus arithmetic. Cycle-to-bridge
contradictions, global witness injectivity, all-parameter placement,
unique-matching leaf induction and the freezing-template adapter remain
written proofs. The whole graph theorem is not claimed fully formalized.

The earlier even-bridge theorem is independently ACCEPT. A separate
follow-up review of this new note and the complete standard-elbow freezing
dependency is pending in the same conversation. It is not included in
the earlier accepted verdict.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
