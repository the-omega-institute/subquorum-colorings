# No uniform exterior-donor radius for frozen degree-four exports

26 October 2026. Wenlin Zhang and Haobo Ma. Independent research branch.

The [degree-four occupied-strip budget](OCCUPIED_STRIP_DEGREE_FOUR_BUDGET.md)
reduces regional losses to actual unported degree-four TP exports. A tempting
next assertion is that every such endpoint has an exterior positive-surplus
original tile within a universal distance. **This assertion is false for every
fixed radius, even with complete freezing, a connected endpoint receiver,
original-tile-aligned disjoint strips, and arbitrarily many capacity-two tiles.**

The construction below proves this for all parameters. It also identifies
an essential qualification: these D4 demands are already covered by the
INTERNAL strip budget. Thus this is an obstruction to unconditional pointwise
exterior-donor access, not to coverage of the remaining unpaid demand. It is
not a counterexample to the grid inequality or an improvement of 5/6.

## 1. Precise statement

An original tile Q_(a,b) has corners {2a,2a+1} x {2b,2b+1}. Write

    c(Q) = 4 - 2|T intersect Q| - |P intersect Q| = 2 sigma(Q).

Positive c is actual physical surplus in half units. It is counted whether
or not Q contains endpoints. Let U consist of two disjoint, original-tile-
aligned vertical strips. Only original tiles wholly outside U qualify as
exterior resources. Distances below are between original tile indices;
Chebyshev distance includes both edge and corner neighbors.

**Theorem.** For every integer h>=1 there is a feasible actual pair (T,M)
on a (4h+10)-by-10 board with these properties:

* Every endpoint is completely frozen for the actual matching. P is connected.
* Both strips start BB and finish with a blank corner. There are exactly two
  unported degree-four TP exports, one per strip. Each actual mate is outside U.
* For EACH source, the nearest exterior positive-surplus original tile is at
  Chebyshev distance h+1 and Manhattan distance h+2.
* All exterior tile surpluses are nonnegative. Their total is 20 half units,
  on exactly five distinct original tiles. The whole board has surplus 14.
* There are 2h+2 original all-P tiles. For h>=2, exactly 2h-4 of them have
  residual capacity two, all with raw physical surplus zero.
* The exact joint ledger is

      B=2, r=0, u=2, V=6, D4=2,
      2S_U = B+r+u+V-D4 = 10-2 = 8.

For any proposed universal radius R, choose h>=max(1,R). Neither source
has ANY exterior positive-surplus tile within distance R, let alone a
pointwise allocation into different nearby tiles. The internal budget 10
already pays both source half units. Requiring a separate exterior donor
for these sources would impose an unnecessary condition.

The example uses two parallel strips, sufficient to disprove a rule asserted
for arbitrary mixed directions. It does not claim an obstruction that
requires mixed directions, nor a negative regional surplus.

## 2. Coordinates and actual matching

Use the existing [four-outward frozen slab](FOUR_OUTWARD_SLAB_AND_ONE_UNIT_OBSTRUCTION.md),
restated here to fix the actual matching. Set L=2h+4. Its selections T0 are

    (r,1),(r,6) for even r in 0,...,L-1;
    (r,0),(r,7) for odd r in 0,...,L-1;
    (L-1,2),(L-1,5).

Its matching M0 consists of

    (0,2)--(0,3), (0,4)--(0,5);
    (1,3)--(1,4), (2,3)--(2,4);
    (1,c)--(2,c)                    for c=2,5;
    (r,c)--(r+1,c)                  for odd r=3,...,2h-1, c=2,3,4,5;
    (2h+1,3)--(2h+1,4);
    (2h+1,c)--(2h+2,c)              for c=2,5.

Its endpoints are rows 0,...,2h+1, columns 2,...,5, together with
(2h+2,2),(2h+2,5). The odd-r range is empty when h=1.

Place two copies by the maps

    lower(r,c) = (L+2+r,c+1),
    upper(r,c) = (L+1-r,c+1).

They occupy rows L+2,...,2L+1 and 2,...,L+1 respectively. Preserve ALL
matching edges of both copies. Remove just the two upper selections

    upper(0,1)=(L+1,2), upper(0,6)=(L+1,7).

For each copy, add the outer selections f(r,-1), f(r,8) for every even
original row r, where f is its placement map. These are board columns 0,9.
Rows 0,1 are entirely blank; all other unlisted sites are blank.

Let I_left be columns 2,3 and I_right columns 6,7, each through ALL board
rows in increasing order, and U=I_left union I_right. The two sources are

    x_left  = lower(0,2)=(L+2,3),
    x_right = lower(0,5)=(L+2,6).

Their actual mates lower(0,3), lower(0,4) are in columns 4,5, outside U.
The source tile indices are (h+3,1), (h+3,3).

## 3. General feasibility, connectivity and freezing

The original slab selections are feasible: even side supports see one side
endpoint; odd outer supports are isolated; each final extra selection sees
one tip. After shifting by one column, the added selections at columns 0,9
are isolated inside each copy. Across the join, the two selections in each
of columns 0,9 become an adjacent pair; each sees exactly that one selection
and no endpoint. These are the only new selection-selection adjacencies.

The potentially conflicting original side supports at rows L+1,L+2 would
be adjacent and both see endpoints. Removing the upper two eliminates this
conflict. No other original selection gains an occupied neighbor across
the join. Both matching copies use disjoint endpoints; removing selections
leaves the endpoint set unchanged. This proves feasibility for every h.
The two full four-column endpoint rectangles touch across the join, and
each extreme tip attaches to its rectangle. Hence P is connected.

For completeness, the standard slab freezing schedule is the following
nine waves, in original coordinates. A row entry means both stated columns;
inside any wave all retained-mate witnesses belong to strictly earlier waves.

1. Side columns 2,5 at even rows 2h+2,2h,...,2, descending.
2. Side columns 2,5 at row 0.
3. Middle columns 3,4 at row 1.
4. Middle columns 3,4 at row 0.
5. Side columns 2,5 at row 1.
6. Middle columns 3,4 at row 2.
7. Middle columns 3,4 at odd rows 3,5,...,2h-1, then row 2h+1, ascending.
8. Middle columns 3,4 at even rows 2h,2h-2,...,4, descending.
9. Side columns 2,5 at odd rows 3,5,...,2h+1, ascending.

Each side endpoint in wave 1 uses its selected support and a retained
neighbor below, or the two selections at the last tip. Wave 2 uses its side
selection and the retained side endpoint in row 1. Waves 3--6 propagate across the top
cap using retained mates of the already frozen side/middle endpoints. Waves
7--9 propagate along the two middle wires and the side wires. The explicit
witness proof is also given in the cited slab note; empty ranges are harmless.

First run ALL these waves on the lower copy. Its selections and edges are
unchanged, and adding other endpoints cannot invalidate two retained witnesses.
Then run the waves on the upper copy. All original witnesses are preserved
except the two removed selections used in wave 2. For upper(0,2), replace
upper(0,1) by its adjacent endpoint lower(0,2). Its actual mate lower(0,3)
already froze in the completed lower schedule, so this is a retained witness.
For upper(0,5), similarly use lower(0,5), whose actual mate lower(0,4) is
already frozen. Each replacement is distinct from the other old witness
in the same step and from the endpoint's actual mate. Thus the modified
schedule freezes every upper endpoint too. This is an induction valid for
all h and uses no bounded search or assumed preservation after deletion.

## 4. Exact original-tile ledger and distances

All nonzero values of c are the following; all unspecified tiles have c=0:

| Original tile indices | c, in half units | Location |
| --- | ---: | --- |
| (0,b), b=0,...,4 | 4 each | two added blank rows |
| (1,2), (2h+4,2) | 4 each | the two extreme cap centers |
| (1,1),(1,3),(2h+4,1),(2h+4,3) | -1 each | cap flanks inside U |
| (h+2,1),(h+2,3) | 2 each | removed upper supports inside U |

To check this generally, every noncap side tile has one T and two P, hence
c=0; every central noncap tile is all P; every outer nonpadding tile has
two diagonal T. Each extreme cap flank has two diagonal T and one P, so
c=-1, while its central tile is empty, c=4. Removing each upper support
adds exactly two half units in its own side tile. This exhausts the board.

Outside U the only positive tiles are therefore

    (0,0), (0,2), (0,4), (1,2), (2h+4,2),

each with c=4. In particular no outside negative tile is being ignored.
For each source tile (h+3,1) or (h+3,3), the bottom cap center is the
nearest exterior donor: row displacement h+1 and column displacement one.
The top cap center has row displacement h+2; the padding has row
displacement h+3. Thus the claimed minimum distances are exact.

Summing the ledger gives 28 half units globally, eight inside U and twenty
outside. Equivalently

    |T|=12h+26, |M|=8h+10, |P|=16h+20,
    area/2=20h+50, |T|+|M|=20h+36.

The all-P tiles are precisely (a,2) for a=2,...,2h+3: 2h+2 tiles. For h>=2,
the three horizontal middle matching edges in each slab occupy three
different such tiles. Those six tiles have one internal matching edge,
residual capacity one. Every other all-P tile has no internal matching
edge, residual capacity two; there are 2h-4. For h=1 the collisions give
two capacity-one and two capacity-zero tiles instead. All these tiles
have raw physical surplus ZERO: residual capacity is not a second donor.

## 5. What is paid internally, and the correct remaining research question

Each vertical strip has two BB columns (the initial blank rows), no TT,
2h+3 TP and 2h+3 BP columns, and two TB columns. Exactly one TP is exported:
the specified degree-four source. All other TP endpoints have their actual
mates in different BP columns of the same strip. Hence K=2, b=1, e=d=1,
a=0, v=3, u_local=1. No actual matching edge crosses between the two strips.
Their joint values are B=2, r=0, u=2, V=6, D4=2, and 2S_U=8.

Both sources have selected within-strip partners and occupied neighbors
on both longitudinal sides, so neither has an immediate BB port. Its
selected partner, actual transverse mate and two longitudinal P neighbors
give occupied degree four. These are actual matching exports, not virtual
strand links. The regions are disjoint unions of ORIGINAL tiles.

The example separates three questions:

1. Unconditional pointwise access from every D4 to a nearby exterior donor:
   **false for every fixed radius**, by this all-h construction.
2. Access only for D4 left after the internal budget B+r+u+V: this construction
   has no such residual demand and gives **no counterexample**.
3. A joint global allocation covering residual D4 AND exterior positive
   charge, using each physical half unit once: still open.

In particular a search for a radius bound must formulate question 2 or 3.
It must allow the internal budget to pay its share before imposing exterior
access. Merely finding a D4 without a nearby donor is not evidence against
the grid target. Conversely, a pointwise donor for each source would not
prove simultaneous ownership when different sources share its capacity.

For a fixed allowed access graph, the correct capacity test is the capacitated
Hall condition. Give every D4 demand one half unit, every outside tile with
c<0 demand -c, the internal pool capacity C=B+r+u+V, and every outside tile
with c>0 capacity c. If the internal pool is accessible to every demand,
then for EVERY demand subset A one needs

    demand(A) <= C + sum_{Q in N(A)} c(Q).

Here C is the budget in the existing regional ledger, not an extra physical
donor pool to add again to S_U. The complete arithmetic remains
2S_whole=C-D4+sum_outside c(Q).

This is necessary by summing distinct capacities and sufficient by splitting
integer capacities into distinct slots and applying Hall. It does not assert
that geometry supplies the condition. It counts each original tile's capacity
once, also when different sources or components reach it. On this family the
outside negative demand is zero and C=10 already exceeds D4=2, so every such
subset passes even if no local exterior edges are allowed. The theorem
above is a geometric obstruction to a stronger premise, not a new Hall theorem.

## 6. Reproducibility and actual formal scope

`develop/check_degree_four_exterior_locality.py` constructs this family with
standard Python, replays the written schedule and independently recomputes
freezing, actual exports, forest budgets, the entire raw-tile inventory,
capacity-two counts and both nearest-donor metrics. It checks h=1,...,16,
24,32,64,128, plus 24 carried isometries. Finite checks corroborate Sections
2--5; they are not the general proof. The saved h=2 witness is an 18-by-10
board with 50 T, 26 M and 52 P, nearest exterior donor distance three.

`formal/SubQuorum/DegreeFourExteriorLocality.lean` kernel-checks that concrete
board's feasibility, actual mate closure, all 52 endpoints inductively frozen,
the two actual D4 sources, exact five exterior positive tiles, absence of
any radius-two donor, and regional/global counts. It also checks general
coordinate-separation and internal-coverage arithmetic. The all-h geometric
adapter, schedule replacement, raw inventory and capacity-two counting are
written proofs with executable checks, not an end-to-end general Lean theorem.

Reproduce from the repository root:

    PYTHONDONTWRITEBYTECODE=1 python3 develop/check_degree_four_exterior_locality.py --output output/degree-four-exterior-locality-validation.json
    PYTHONDONTWRITEBYTECODE=1 python3 develop/check_degree_four_exterior_locality_formal.py --lean /path/to/lean-4.33.0/bin/lean --output output/degree-four-exterior-locality-formal-validation.json

The Lean runner measures memory and checks actual lean/lake executable
basenames before each invocation. No shared build or CI change is required.
Discovery additionally found individual finite radius-two/three/four access
failures. Those solver examples and a bounded UNSAT control were not used
as evidence for this general construction. No new email or manuscript edit
is part of this milestone.
