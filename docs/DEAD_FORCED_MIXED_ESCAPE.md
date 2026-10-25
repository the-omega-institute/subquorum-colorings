# A forced mixed escape can be completely unproductive

25 October 2026. Wenlin Zhang and Haobo Ma. Isolated research branch.

We exhibit a fully frozen original board in which two different alpha
owners enter one vertically matched BP of a productive mixed owner G.
One alpha's outward alternative, forced by freezing, is a horizontally
matched BP belonging to a mixed owner D. Yet D has **no original support
and no nonself outgoing link**. It cannot pay a source or relay one to any
resource, even with the complete original resource pool.

This refutes the candidate rule that a forced exterior mixed escape at
such a fork must be productive, and therefore cannot be assigned an
automatic unit of compensation. The complete board still pays both
alphas, at minimum actual-link cost one. The obstruction concerns the
local rule, not the target grid inequality or the universal 5/6 bound.

Follow-up: [two dead forced escapes and the support-shadow relay lemma](TWO_SIDED_DEAD_ESCAPES_AND_SHADOW_RELAY.md)
gives a beta-free frozen board with BOTH alternatives dead and a productive
receiver. Its complete original-pool-subset payment/cost function is proved
by a general shared-relay lemma retaining direct source support.

The [horizontal-BP forest theorem](HORIZONTAL_BP_FORESTS.md) remains valid:
D is an alpha-reachable, single-entry, one-vertex H tree with no output.
Alpha reachability and resource productivity are different conditions.
Earlier [tip-slot obstructions](FROZEN_TIP_SLOT_OBSTRUCTION.md) already
contain dead mixed owners. The additional configuration here puts a dead
owner exactly at the rank-forced alternative of a real two-alpha,
productive **mixed** receiver fork, with original full supports checked.

## 1. The rank argument also applies to a mixed receiver

Use a feasible original selected set T and actual matching M, aligned
two-row bands, original PP/M owners, and a finite strict freezing rank
rho on every endpoint P. At each endpoint v at least two neighbors are
retained: a selected neighbor always is, and an endpoint w is retained
when rho(mate(w)) < rho(v). Keep all original links and original supports;
the usual marked extreme intervals K are the only resource exclusions.

**Lemma 1 (receiver-independent physical escape).** Let b be an original
BP. Its two horizontal neighbors t,u are original TP tips of owners
different from b's owner. Suppose t's actual mate is vertical. Its
horizontal neighbor n away from b is either:

1. a blank point with blank within-band partner, hence an immediate BB port;
2. a BP whose actual mate is its horizontal neighbor away from t.

If t belongs to an alpha, or to a mixed owner whose own BP is vertically
matched, case 2 is a nonself link to another open owner. The receiving
owner of b may be beta **or mixed**. Different such vertical tips have
different BP escape targets; at one common checkerboard phase their
escape owners are different. Neither a BB port's availability nor a
mixed escape's productivity is asserted.

**Proof.** This is the rank mechanism of the
[serial escape lemma](FROZEN_SERIAL_FORK_ESCAPE.md), with the receiver
hypothesis weakened from beta to an open owner with two external TP
neighbors. Normalize t=(r,c) in the lower row of its band and write

    b=(r,c-1), u=(r,c-2), n=(r,c+1),
    a=(r+1,c), b*=(r+1,c-1), z=(r+1,c+1), h=(r+2,c).

The band partner of b is blank. It cannot actually match t or u, since
either would join different original owners. Thus mate(b)=b*. To freeze
b its two horizontal TP neighbors must both be retained, so

    rho(a) < rho(b).                                      (1)

At a its own mate t is not retained through itself. Retaining b* would
require rho(b)<rho(a), contradicting (1). Its other two potential neighbors
z,h must therefore both be retained. Missing boundary neighbors would
make the hypotheses impossible, so cause no extra case.

The selected band partner (r-1,c) of t forces both (r-1,c-1) and
(r-1,c+1) blank: it already sees occupied t. If n were selected, it would
see occupied t and occupied z, violating feasibility. If n is blank we
have BB. Otherwise n is BP. The retained z cannot be selected, because
it sees a and n. Hence z is an endpoint with
rho(mate(z))<rho(a). If mate(n)=z, this implies rho(n)<rho(a).
But n then has its band partner blank and its own mate z not retained;
it requires t retained to freeze, giving rho(a)<rho(n), a contradiction.
Thus n cannot match vertically. It cannot match t either, since t's
mate is a. It must match horizontally outward.

An alpha has no BP of its own; a mixed owner's vertically matched BP
cannot equal this horizontally matched n. These are the stated nonself
cases. If two vertical TPs shared one escape BP, the outward-mate rule
would match that BP to the other TP, contradicting its vertical mate.
Targets are therefore distinct. Common-phase TP tips give common-phase
BP targets; a beta's two BPs have opposite colors and a mixed owner has
only one BP. Thus target owners are distinct at a common phase.
Reflection handles either band row and direction. QED.

The distinction in the lemma matters for a general long mixed t: vertical
matching at its TP alone does not rule out returning to its own horizontal
BP through a long strand. We do not silently assume that every such link
is nonself. Our witness below uses two alphas.

## 2. An explicit completely frozen witness

Coordinates are zero-based. The board is 14 by 18, with bands
(0,1),(2,3),...,(12,13). T is selected, P an actual matching endpoint,
and a dot blank:

```text
..................
............T.....
...........TPPPT..
............PPP...
..T..T.T.T.TPPPPT.
.TPPPPPPPPT..T.T..
..PPPPPPP.........
.TPPPPPPP.........
...PPPPPPPT.......
...PPPPPPP......T.
.TPPP.T..PT.......
..T.T....T....TT..
.......T..........
..................
```

The [permanent fixture](../develop/fixtures/frozen_dead_forced_mixed_escape.json)
specifies all 25 actual matching edges and all strict rank layers. Its
50 endpoints freeze in ten layers of sizes
6,6,6,8,8,7,6,1,1,1. The certificate is checked directly: every endpoint
has two selected or strictly earlier-mate neighbors, independently of
the repository's peeling implementation. Feasibility, terminal types and
PP/M components are also reconstructed independently of the discovery solver.

The critical original owners are:

| Owner | Original tips | Whole support in available original units |
|---|---|---|
| A_L, alpha | (5,2), (5,5) | empty |
| A_R, alpha | (5,7), (10,9) | includes all three units below and other bypasses |
| G, mixed | BP (5,6), TP (10,4) | (band 5,col 5), (band 5,col 7), (band 5,col 8) |
| D, mixed | BP (5,8), TP (5,9) | empty, including before boundary exclusions |
| Z, beta | BP (5,3), BP (5,4) | empty |

Each listed G unit is a different original unmarked singleton interval;
they are not new copies of the same unit. The full board has two alphas,
one beta, five mixed owners, and three closed PP/M cycles.

The fork and forced alternative are actual original horizontal links:

    A_L:(5,5) --> (5,6):G <-- (5,7):A_R --> (5,8):D.

The actual mates of (5,5),(5,6),(5,7) are (6,5),(6,6),(6,7), respectively.
Lemma 1 at t=(5,7), b=(5,6), u=(5,5) forces the outward BP (5,8).
Its actual mate is (5,9). D has only this one M edge and no PP body.

**Why D is dead, without an enumeration argument.** Its BP end at column
8 has a TP in column 7 on its other side. Its TP at column 9 has a
selected point (5,10) on its right, not a BP, and on its left only its
own BP (5,8). Its sole outgoing candidate is the self-link
(5,9)->(5,8); there is no nonself continuation.

For supports, in band (4,5) the columns to the right of D are

    column 9: TP, 10: BT, 11: TB, 12: PP.

The whole gap between TP and PP contains two BT-type columns and no BB.
There is no interval there; the gap to the left is blocked immediately
by the TP at column 7. With no PP body there are no other places for D
to meet a gap. Thus W(D) is empty in the full original resource pool,
even if marked intervals were put back. Removing D from the routing
graph by productivity pruning loses no paying path. No physical point
has been deleted or rematched in this argument.

**Why the complete board still pays both sources.** Select the single
original link (5,2)->(5,3), paying A_L by whole beta Z. Pay A_R directly
by, for example, the original unit (band 5,col 5). These use different
owners and resource types; the interval is used once. Hence V=2, the
maximum possible with two sources. Zero links cannot pay A_L because
its whole available support is empty, so the minimum link cost is
exactly one. A_L has a marked extreme port; it is not an available
unit under the stated convention.

G's three units also lie in A_R's own whole support. Therefore even
restricting the pool to those units does **not** by itself force both
sources through G. We do not infer a two-source gate deficit by discarding
this direct support. A rule that only uses prescribed routes is a
separate restricted rule, not the complete original board.

## 3. Arbitrarily many dead forced alternatives

**Proposition 2 (all-copy family).** For every integer q>=1 there is a
14q by 18 feasible completely frozen board with 2q original alphas,
q betas, 5q mixed owners, and q pairwise distinct dead forced H escapes
at two-alpha productive mixed forks. In the full original fork network
V=2q and the minimum actual-link cost is q.

**Proof.** Translate copy i of the witness by (14i,0), for 0<=i<q, retaining
its T and M. Each copy has blank rows 0 and 13; occupied rows in adjacent
copies are separated by at least three. Consequently feasibility and
every strict-rank witness transport unchanged, and original actual M and
PP strands cannot cross copies. Translation by an even row count preserves
bands and checkerboard phases. Copy the ten rank layers in parallel.

Every original interval is confined to one two-row band. Bands from
different copies are different, so unit identities and all whole supports
are separate even when their column numbers coincide. All original links
are horizontal and also stay within their copy. Each D is still dead,
and each G still has its three different available units. The explicit
one-beta-link plus one direct-interval payment in each copy gives payment
2q at cost q without reusing any owner, BP entrance, beta or interval.
No larger payment exists because there are only 2q alpha sources. Each
A_L has empty available support and must use a link in any full payment;
links from distinct copies are different. Hence cost is at least q.
This also follows from the direct-sum original routing networks. QED.

The conclusion is an unbounded family of failures of **automatic escape
credit**, not an unbounded unpaid deficit. We have not embedded the full
serial skeleton from the earlier theorem in this family. The theorem's
careful decision to leave exterior mixed escapes uncredited is preserved.

## 4. Verification and consequence for the remaining problem

Run from the repository root, with Python's standard library only:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 develop/check_dead_frontier_escape.py \
  --output output/dead-frontier-escape-validation.json
```

The solver-free verifier checks the explicit rank certificate, independent
PP/M strands, complete original supports and links, the dead single-vertex
H tree, and productivity pruning. It compares full fork flow, weighted H
compression and the pruned full graph: all give (V,c)=(2,1).
Independently enumerating all 390 terminal matchings of the base board
confirms this optimum. Eight transported symmetry images each pass the
same checks and all 390 matchings. Transposed images transport the bands;
they are not reinterpreted using unrelated horizontal bands.
Copies q=2,3,5,8 pass the original-pool checks, with V=2q,c=q.
These are finite checks of the construction, separate from its all-q proof.
The existing forest verifier also passes with the new fixture included:
23 frozen fixtures, 92 physical value/cost comparisons, 220 abstract
comparisons and the prior 100 serial certificates. Its separate
[regression receipt](../output/dead-frontier-forest-regression.json)
preserves the earlier milestone's original receipt.

The optional discovery script uses Z3; the permanent fixture and verifier
do not. A bounded two-dead, typed rich-gate search returned UNSAT for its
fixed motif. This is not an impossibility theorem for two dead alternatives
or a classification. An untyped two-dead SAT control identifies a source
with the receiver and does not meet the distinct external alpha hypotheses.
No new Lean theorem or Oracle review is claimed in this milestone.

The remaining compensation problem must account for **both** productivity
and joint capacity after the H forest compression. Distinct H roots alone
give no positive resource credit. Productive roots can still compete at a
vertical mixed gate or for one original interval; dead roots give none.
The next useful step is a frozen-geometric restriction on full source-to-
resource cuts with every bypass and every original unit retained, or a
stronger explicit full-board obstruction. The present example establishes
the precise failure of one tempting local repair rule and leaves the
universal 5/6 bound open.
