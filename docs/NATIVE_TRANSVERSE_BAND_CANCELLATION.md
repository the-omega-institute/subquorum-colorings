# Native transverse matching: compensation across occupied bands

22 October 2026. Authors: Haobo Ma and Wenlin Zhang.

This note extends the occupied-strip flux theorem to an aligned packet of
adjacent two-row bands. Individual bands need not be matching-closed or
receiver-closed. A specific native support condition makes every charged
internal exit cancel through a common path count. Thus arbitrarily many
split receivers can be handled without spending the same original slack
twice. General transverse exits without that condition remain open.

## 1. Precise hypotheses and conclusion

Let (T,M) be a feasible pair, with P the actual matching endpoints and each
selected vertex having at most one occupied neighbor. Let J consist of
2k consecutive rows and n consecutive columns, k>=1 and n>=2. Partition J
into its k consecutive two-row bands I_1,...,I_k. All bands use the same
column interval. In every band the first column is blank in both rows and
at least one corner of the last column is blank. The exterior is arbitrary
feasible data subject to these two additional matching hypotheses:

1. No endpoint of a TP column in any I_i has its actual mate outside J.
   Other endpoint types may have mates outside J.
2. For each matching edge between distinct bands having a TP endpoint in
   either band, BOTH endpoints have at least two neighbors in the original
   selected set T. These witnesses are original selections, not endpoints
   retained after a freezing process.

Call such an edge charged. Let r be their number. If n is even, let t be
the number of bands whose last column is also entirely blank; if n is odd,
set t=0. With the same weighted regional balance as before,

    S_J=kn-|T intersect J|-|P intersect J|/2,

the theorem is

    S_J >= k+t.                                         (1)

If a counts matching edges with exactly one endpoint in J and M_in the
edges wholly inside J, this equivalently states

    |T intersect J|+|M_in|+a/2 <= kn-k-t.                (2)

No terminality is needed. Native hypothesis 2 is a sufficient geometric
condition, not a consequence of exchange terminality or complete freezing.
The theorem applies after reflection or transposition of the whole packet.

## 2. Every charged edge has a forced pinwheel

Use local coordinates for an edge u=(1,c), v=(2,c) crossing two adjacent
bands, whose other rows are 0 and 3. The TP endpoint can be taken to be u
by vertical reflection, so (0,c) is selected. Put

    upper lateral candidates: (1,c-1),(1,c+1),
    lower lateral candidates: (2,c-1),(2,c+1).

An upper and lower lateral candidate in the same column cannot both be
selected: the upper one would see u and the lower selection. Each endpoint
needs two original selected neighbors among its three nonmate neighbors.
Thus each requires at least one lateral selection. The lateral choices
must be disjoint. Neither endpoint can use both lateral positions, since
that would leave no lateral position for the other. Consequently each
uses exactly one lateral position, the choices are opposite, and both
outer positions (0,c),(3,c) are selected. In particular v is also in a
TP column.

For one orientation the four supports are

    (0,c), (1,c+1), (2,c-1), (3,c).                     (3)

The reflected orientation reverses the lateral signs. In (3), feasibility
at (0,c) and (2,c-1) makes both vertices of the upper-band column c-1
blank. Similarly (1,c+1) and (3,c) make both vertices of the lower-band
column c+1 blank. Every exclusion forbids endpoints as well as selections:
the excluding selection already has its occupied matched-endpoint neighbor.

Thus each charged edge produces a BB column immediately to its left in
one band and a BB column immediately to its right in the other band. Both
TP columns are internal columns. The same exclusions show that u and v
have no other endpoint neighbors, so they form an isolated original K2
endpoint component and freeze immediately. No separate K2 assumption was
used in obtaining the pinwheel.

Every mixed export from a band is such a charged edge: hypothesis 1 rules
out exits from J, and an internal export necessarily crosses the horizontal
boundary to the next two-row band. The pinwheel proves the converse TP
incidence as well. Therefore

    sum_i e_i=2r.                                      (4)

## 3. Join the BB--TT forests, rather than paying exits separately

In band i form the BB--TT forest from the occupied-strip proof. Its
connected components are alternating intervals BB,TT,...,TT,BB, including
isolated BB columns. Each has odd length. There are B_i-A_i components.
Let F be their total number over all bands.

Make a new graph G whose vertices are these intervals. For each charged
matching edge at column c, join the interval containing the forced left
BB column c-1 to the interval containing the forced right BB column c+1.
Orient this edge left to right. The left interval ends exactly at c-1
and the right interval begins exactly at c+1, since the intervening column
is TP in each corresponding band.

Each interval has at most one outgoing edge. Such an edge must use the
column immediately after its right endpoint in its own band; that column
has a unique TP endpoint and that endpoint has only one actual mate.
The same argument gives at most one incoming edge. Distinct matching
edges cannot create parallel copies of the same directed connection.
Along each edge every column of the destination interval is strictly
farther right than every column of the source interval. Directed cycles
are impossible. A finite graph with these indegree/outdegree bounds and
no directed cycles is a disjoint union of directed paths and isolated
vertices. If h is its number of path components, then

    F-r=h.                                             (5)

This argument applies across arbitrarily many adjacent bands. No planarity
or unproved global source injection is assumed.

Each band's first BB column lies in an interval starting at the first
column of J. That vertex has no incoming edge. These k distinct vertices
belong to distinct directed paths, because a directed path has only one
source. Hence h>=k.

For the even sealed improvement, a directed path through intervals of odd
length spans an odd number of columns. Indeed the initial interval has
odd length, and each further interval is separated by exactly one TP
column. Extending the path adds one plus an odd interval length, which
is even. Each sealed final BB interval is a sink at the last column.
There are t such distinct sinks on distinct paths. None is on a path
containing one of the k first-column sources: that path would span all
n columns, contrary to even n. Therefore

    h>=k+t.                                            (6)

The use of interval lengths in this proof is combinatorial. The paths can
switch bands, and their intervals are not additional physical donor tiles.

## 4. Exact joint accounting and ownership

Let u_i=D_i-C_i+e_i be the nonnegative unused BP-column count in band i;
here D_i denotes the BP COLUMN count, not physical tile deficit. Write
U=sum_i u_i. Sum the exact occupied-strip identities and use (4),(5):

    2S_J+2r=2F+U,
    S_J=h+U/2 >= k+t.                                  (7)

Thus the apparent r units of half-debit from the 2r internal mixed exits
are removed by subtracting exactly r edges from the common forest count.
There is no separate allocation of the same empty column to two exports.
The object counted is the connected-path count h, once for the whole
packet. Neither an internal signed receiver fragment nor a forced empty
column is also credited as an outside component resource.

For an original physical-tile packet J in a single-terminal configuration,
assume only UNION receiver closure: every original endpoint component
meeting J has its complete physical receiver contained in J. Individual
bands may split those receivers. For tile-disjoint packets satisfying the
theorem, let q,R_out be the total positive and absolute nonpositive charges
of components outside all packets, and let D_out be the outside original
endpoint-free tile deficit. The original ledger is exactly

    mn/2-|T|-|M|=sum_packets S_J+D_out-q+R_out.

Consequently q<=sum_packets(k+t) proves coefficient one. Rotated packets
may be mixed provided their physical tiles are disjoint. This is a strict
relaxation of requiring every receiver to lie inside one two-row band.
Components inside a packet are counted entirely in its S_J, regardless of
their signs. This theorem supplies no allocation for overlapping packets.

## 5. A sharp family with arbitrarily many split receivers

For each r>=1 take a 4-by-(4r+2) board. Column 0 is blank. For each
i=0,...,r-1 put c=4i+3 and add the matching edge

    (1,c)--(2,c).

At column c select rows {0,3}. For even i, select these additional rows:

    column c-2: {0,1,3}; column c-1: {2}; column c+1: {1}.

For odd i, select

    column c-2: {0,2,3}; column c-1: {1}; column c+1: {2}.

In the final column 4r+1 select rows {0,2} if r is odd, or {1,3} if r is
even. There are no other occupied vertices. The orientation alternates
between pinwheels. Each block has seven selections and one matching edge;
the final column has two selections. Therefore

    |T|=7r+2, |M|=r, S_J=2.                            (8)

Feasibility can be checked for all r without enumeration. At every even-i
pinwheel the support pattern is (3), and at every odd-i pinwheel it is its
vertical reflection. Each lateral support sees only its adjacent endpoint.
Each outer support in the pinwheel sees only its endpoint. At the preceding
column c-2, the two selections in one band form a vertical pair; the third
selection is isolated. Their neighboring columns in their selected rows
are blank. At consecutive block interfaces, the last lateral support of
one block faces a blank vertex in its row in the next block's first column.
The final two selections are isolated and avoid the preceding lateral
support's row. Thus every selection has at most one occupied neighbor.

Each endpoint has exactly its mate and two native selected witnesses, and
distinct matching edges are four columns apart. The endpoint graph is r
disjoint K2 components, with unique matching and immediate full freezing.
Every component's physical receiver consists of one upper-band tile and
one lower-band tile. Its two raw charges are -1/2,+1/2 in one order, so
its whole charge is zero. Each original receiver is split between bands,
and the former individual-band closure hypothesis fails for all r>=1.

There are e_i=r exports in each band, U=0, F=r+2 and h=2. For odd r the
individual band balances are 1/2 and 3/2; for even r they are both 1.
The naive sum of the separate flux lower bounds is only 2-r, while the
joint theorem gives the exact value 2 for every r. Arbitrarily many split
receivers therefore require no growing outside compensation budget.

Deleting either or both final selections seals the corresponding band
without affecting any endpoint's native witnesses. The resulting S_J is
3 or 4, respectively, so the even sealed improvement k+t is also sharp.
The examples demonstrate sharpness for this stated packet theorem, not
failure of the global half-area target or coverage of all terminal grids.

### A positive outside source with split neutral receivers

There is also a nonvacuous original positive-source application. Start with
the prescribed neutral-pair elbow with even H>=4, even W>=6r+16 and r>=1.
Its complete original root component has charge 1. For c=11+6i,
i=0,...,r-1, insert the vertical matching pair

    (9,c)--(10,c),
    original selections (8,c),(9,c+1),(10,c-1),(11,c).

Take the aligned two-band packet in rows 8,...,11, with columns 6,...,W+3
at H=4, or 6,...,W+1 at H>=6. The root receiver is outside this packet.
Each foreign K2 has one receiver tile in each band, charges -1/2,+1/2,
and whole charge zero. Its complete receiver is inside the packet, while
neither individual band is receiver-closed. The native pinwheel theorem
applies to all r transverse matching edges.

For all parameters the added vertices are feasible and separated. Their
occupied columns range from 10 through 6r+7. Portal data end at column 7;
root data in these intermediate columns are in rows at most 6, two rows
above the first added selection. The nearest right-leg support is at
column W+2>=6r+18. Successive additions are six columns apart and cannot
give any selection a second occupied neighbor. Rows 8,...,11 lie in the
board even at H=4. Both packet boundary columns remain blank.

Thus all foreign receivers stay inside the packet, every added pair is
immediately frozen, and the root's unique matching and freezing persist.
Whole counts are M=W+H+r and T=H+7+4r. Here q=1, k=2, t=2, and the
union-level original ledger proves coefficient one. This supplements the
zero-charge sharp examples with an actual positive outside source.

## 6. Limits and validation status

The all-length proof is Sections 2--4; the construction proof in Section 5
is also uniform in r. The permanent verifier is
develop/check_native_transverse_band_cancellation.py, with results in
output/native-transverse-band-cancellation-validation.json. It passes
6352 packet models, including all short full-board label/matching choices
within the native hypotheses; 320 sharp parameters through r=80; 128
symmetry images; 40 multiband pinwheel packets and 40 feasible selection
extensions; 36 positive-source packets and 32 images; and nonmixed
internal/external matching controls. It directly checks 16462 charged
matching edges, 42380 band-forest intervals and 25918 joint paths.

Run it with

    PYTHONDONTWRITEBYTECODE=1 python3 develop/check_native_transverse_band_cancellation.py --output output/native-transverse-band-cancellation-validation.json

Lean4.33.0 passes 16 scoped theorems and 16 individual axiom audits on the
local Mac, without warnings, sorry or native evaluation. The formalization
checks the finite native pinwheel, forced-blank implication, arbitrary
path-span parity, arbitrary-size indegree/source count, exact joint flux,
coefficient-one arithmetic and all-parameter sharp counts. The grid-to-graph
adapter, actual interval-edge uniqueness, boundary source/sink ownership,
and explicit coordinate constructions remain written proofs. The execution
receipt is output/native-transverse-band-cancellation-lean.json.

The new independent written review completed ACCEPT for Sections 1--5 and
the complete occupied-strip dependency. Its original request agrees exactly
with the recorded session prompt, and its original DONE-stream answer agrees
exactly with both terminal task and session. The full 15463-character answer
is archived in output/native-transverse-band-cancellation-oracle.json,
actual gpt_6/pro, task083d42b8. This is a written mathematical review, not
certification of verifier or Lean execution.

The later positive-source coordinate application and following residual
witness were added after dispatch and are not claimed as covered by that
review. Their permanent finite controls pass separately. No review job for
the native transverse theorem remains live.

The genuinely residual exits are those whose endpoints cannot both exhibit
two original selected neighbors, including longer endpoint components that
freeze only after retained endpoints become available. Unaligned bands,
partial receivers outside a packet and overlapping perpendicular packets
also remain outside this theorem. General compensation and grid triple
equality remain open.

One explicit residual is the original neutral portal itself. The actual
matching edge q=(7,5)--s=(8,5) is a mixed export between row bands {6,7}
and {8,9}. The upper column is PP, while the lower column is PT. Endpoint
q has only one original selected neighbor, c=(7,6), whereas s has two.
The retained endpoint p=(6,5) is required to freeze q. Even taking the
whole board as a packet, with both exterior columns blank and matching
closed, does not make the native hypothesis true. The complete configuration
has unique matching and fully freezes. Nine parameter controls verify these
facts. This is an obstruction to deriving our native hypothesis from full
freezing, not a counterexample to either the packet bound or global target.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
