# Minus-one tip events occur, and their own full tile need not pay them

20 October 2026. Two explicit physical fusions exclude two proposed
shortcuts for the mixed-direction compensation problem. The first has
one charge-minus-one two-leg module with BOTH terminal tips gaining new
intratile endpoint neighbors, and no negative rotors. The second has a
new full tile with two regular events and one minus-one tip event. Its
own two correction units are exhausted by the regular events, so the
tip requires payment elsewhere. Both complete finer budgets are positive.
Neither example refutes the target compensation inequality.

## 1. Precise hypotheses and definitions

We use the complete retained-support fusion class in
MINUS_ONE_JOINT_WITNESS_COMPENSATION.md. Original module endpoint sets
are pairwise disjoint; each comes with its own grid perfect matching,
original occupied endpoint degree three, and selected supports having
exactly one occupied neighbor. Final selections are the union of the
old supports minus all final endpoints, and must again have occupied
degree one. Final endpoint degree four and arbitrary contact patterns
are allowed. No optional selections are needed here.

For reference U(w,a,b), w>=6 even and a,b>=4 independently even,

    P=({0,1} x {1,...,w}) union ({2,...,a} x {1})
      union ({2,...,b} x {w}),
    T={(r,0): r=0,2,...,a} union {(r,w+1): r=0,2,...,b}
      union {(r,2): r=3,5,...,a-1}
      union {(r,w-1): r=3,5,...,b-1}
      union {(a+1,1),(b+1,w)}.

The full alternating inward lists are essential. The matching uses the
alternating horizontal bar pairs and the vertical leg pairs printed in
the constructor source. The rotor R has

    P_R={(1,2),(2,2),(2,3),(2,4),(3,1),(3,2),(3,3),(4,3)},
    T_R={(0,2),(1,1),(2,5),(1,4),(5,3),(4,4),(3,0),(4,1)}.

Its four leaf edges give its matching. All coordinates below refer to
these unshifted reference constructors. Transform a point by reflecting
the indicated coordinates, then transposing if indicated, then adding
the printed offset. The ambient tiling is the fixed even 2-by-2 tiling.

Write J for the number of new full mixed-owner physical tiles,
K_reg and K_irr for original-owner regular and irregular intratile
new-neighbor tails, C=2J-K_reg, and G for marked positive donor sides.
The preceding theorem proves K_reg<=2J, with regular costs paid first.
Let N and B be the positive and minus-one two-leg counts. Both examples
have only zero-charge rotors, so S=B. The exact ledger and finer bound are

    rho_final=N-B-2J+K_reg+K_irr,
    sigma=mn/2-|T|-|M| >= N+B+C-K_irr-G.

## 2. Seven modules: both tips gain, with no negative rotors

| Module | Coordinate reflection | Offset |
|---|---|---|
| U(14,8,4) | none | (6,7) |
| U(6,4,4) | c -> -c | (8,15) |
| U(6,4,4) | c -> -c | (8,21) |
| U(6,4,4) | r -> -r | (17,8) |
| R | none | (10,19) |
| U(6,8,4) | r -> -r | (21,14) |
| U(6,8,4) | (r,c) -> (-r,-c) | (23,9) |

Translate the whole union by (-6,-2) into an 18-by-24 rectangle. The
original charges, in table order, are [-1,1,1,1,0,1,1]. All original
endpoint sets are disjoint. All original and final selected supports
have exactly one occupied neighbor; the union of the original matchings
is an actual perfect matching on the final endpoint set.

The minus-one tips and their newly occupied intratile blanks are

    (4,19) -> (4,18),    (8,6) -> (8,7).

Both final tip tiles are full. Each has original endpoint partition
2+1+1, one regular event and one irregular event. The first tile has
one endpoint from the negative source, two from table row three and
one from the rotor. The second has one negative endpoint, two from
table row four and one from table row seven.

The independently reconstructed counts are

    |P|=144, |M|=72, |T|=41,
    N=5, B=1, G=0, J=13, K_reg=21, K_irr=2, C=5,
    |receiver|=43, t_receiver=15, rho_final=1,
    finer guaranteed slack=9, actual sigma=103.

Thus the proposed universal rule K_minus_one=0 is false even with one
negative two-leg module and no negative rotors. Both of that module's
two available tip slots can be used simultaneously.

## 3. Nine modules: a tip tile needs three units

| Module | Coordinate reflection | Offset |
|---|---|---|
| U(14,8,4) | none | (6,7) |
| U(6,4,4) | c -> -c | (8,21) |
| U(6,4,4) | r -> -r | (15,1) |
| U(6,4,4) | r -> -r | (17,14) |
| U(6,4,4) | (r,c) -> (-r,-c) | (15,27) |
| R | none | (12,7) |
| U(6,8,4) | c -> -c | (2,8) |
| U(6,8,4) | c -> -c | (8,15) |
| U(6,8,4) | (r,c) -> (-r,-c) | (25,15) |

Translate everything by (-2,0) into a 24-by-28 rectangle. The charges
are [-1,1,-1,1,1,0,-1,1,1]. Again all original sources, matching data,
endpoint disjointness and complete retained-support feasibility hold.

Consider Q={12,13} x {8,9}, physical tile index (6,4). The negative
source contributes p=(12,8); the zero-charge rotor contributes

    v=(12,9), u=(13,8), z=(13,9).

The old negative profile on Q is 1P1T: p is its endpoint and u its
selection; v was its blank neighbor. The old rotor profile is 3P0T,
whose missing corner is p. Final Q is full with partition 3+1.

Exactly THREE original tails gain a new intratile neighbor:

    p -> v : one irregular event owned by the minus-one module;
    v -> p : one regular event owned by the rotor;
    u -> p : one regular event owned by the rotor.

The old u was already occupied for the minus-one source, so p->u
is not a new-neighbor event. This distinction is checked explicitly.
The two units attached to Q pay the two regular rotor events, leaving
zero local remainder. The irregular p->v event cannot also spend one
of these units. Therefore extending the capacity-two rule to ALL tails,
or paying each irregular tail only from its own tile's unused regular
credit, is false. Counting Q once as a new full tile does not cure this
shortfall. Cross-tile allocation or another independent resource is needed.

For the complete configuration,

    |P|=184, |M|=92, |T|=51,
    N=5, B=3, G=0, J=13, K_reg=21, K_irr=2, C=5,
    |receiver|=58, t_receiver=23, rho_final=-1,
    finer guaranteed slack=11, actual sigma=193.

The other irregular event is (8,21)->(8,20). The global residual credit
five exceeds the total irregular cost two, despite zero remaining credit
on Q. This example obstructs a purely local payment rule and supports
investigating a nonduplicated transport of the remaining credit; it is
not a counterexample to global compensation.

## 4. Scope, reproducibility and consequences

These are complete finite mathematical counterexamples to the specified
universal rules: every coordinate and matching edge is explicit, and
feasibility and all relevant counts are verified independently of SAT.
They do not prove an all-configuration compensation theorem. Neither is
fully frozen: the existing promotion procedure freezes 86 of 144 endpoints
in the first and 92 of 184 in the second. Both endpoint unions are
connected. Explicit legal one-color bundles promote 25 and 69 endpoints,
respectively; the resulting configurations are independently checked.
Consequently neither example refutes a rule restricted to
fully frozen configurations. No minimality among all module families
is claimed; greedy reduction and a bounded six-module UNSAT search do
not prove such minimality.

Earlier UNSAT checks fixed narrow seeds and small module libraries. A
width-14 source with unequal heights permits these examples. The old
finite exclusions retain their stated narrow scopes; no general theorem
was established by them and none is being retracted.

Reconstruct both examples and all sixteen tiling-preserving dihedral
images with

    python3 develop/check_minus_one_tip_obstructions.py \
      --output output/minus-one-tip-obstruction-controls.json

The controls use the existing original-owner physical ledger. The separate
Std-only Lean module formal/SubQuorum/MinusOneTipObstructions.lean checks
the actual coordinate lists, original charges and feasibility, matching,
final feasibility, both tip events, event/full-tile counts, the overloaded
3+1 tile and exact receiver charges and half-area slacks. Its axiom audit
and execution scope are preserved in
output/minus-one-tip-obstruction-formal-check.json. Seventeen declarations
and their individual axiom audits pass under local Lean 4.33.0, using
kernel decide with no sorryAx or native_decide. It does not formalize
a general decomposition, freezing theorem or compensating injection.

Next: determine whether unused regular credit can always be transported
to minus-one tip events without conflicting with marked-side payment.
The donor corner and tip pools remain distinct, as already proved. A
successful lemma must permit a tile with three events while preserving
K_reg<=2J and using each remaining unit only once. The separate Oracle
review of the preceding joint theorem does not include these later
examples unless they are explicitly supplied in a subsequent turn.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
