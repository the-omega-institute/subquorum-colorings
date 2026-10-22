# Frozen missing-port terminals admit distinct adjacent BP terminals

22 October 2026. Authors: Haobo Ma and Wenlin Zhang.

Complete freezing does more than force a BP neighbor beside a missing port:
it guarantees a simultaneous injection into distinct adjacent BP TERMINALS.
The proof excludes an alternating path obstruction by a closed dependency
set with no possible first freezing event. This is a genuine geometric
ownership lemma. A BP terminal is not itself a unit credit: two terminals
can belong to one BP--BP path, and a BP terminal can belong to a zero-credit
TP--BP path. The remaining compensation problem is not declared solved.

## 1. Hypotheses and statement

Use the matching-closed aligned packet J, column labels and actual PP path
decomposition of INTERVAL_CONNECTOR_CYCLES_AND_MISSING_PORTS.md. Let (T,M)
be feasible. Assume EVERY endpoint in the entire original configuration
has a finite freezing certificate for this actual matching. Concretely,
start with no frozen endpoints. An endpoint can freeze once it has two
distinct nonmate neighbors that are either original selections or endpoints
whose actual mates froze earlier. All endpoints must eventually freeze.
The certificate can use vertices outside J. The proof below allows them.

Let A be the set of TP TERMINALS of TP--TP paths that have no immediately
adjacent BB column in their own band. Include both terminals of a path
when both are missing. Let D be the set of BP terminals horizontally
adjacent to some vertex of A in that band. The theorem is that there is
an injection

    f:A -> D,  f(v) horizontally adjacent to v.          (1)

Every image is a distinct original endpoint, not a virtual support or an
entire PP matching path. No uniqueness of the actual matching is assumed.

## 2. Local facts supplied by the geometry

Every endpoint in a completely frozen pair has occupied degree at least
three: its actual mate and the two nonmate witness neighbors in its
freezing certificate are distinct occupied original vertices.

For v in A, its actual mate is vertical across the band boundary. A
horizontal mate would be in a BP column and terminate a TP--BP path instead.
The TP selection is the vertical neighbor within the band. The two
horizontal neighbors of that selection are blank by feasibility. Thus
every horizontal endpoint neighbor of v lies in a BP column. The exact
port formula gives occupied degree four for v. Its two horizontal
neighbors are occupied.

They cannot both be selections: such selections force the two horizontal
neighbors of the vertical actual mate to be blank, leaving that mate
occupied degree at most two. Hence v has one or two horizontal BP endpoint
neighbors. These are exactly its neighbors in D.

Form the simple bipartite graph H with parts A,D and those horizontal
adjacencies. Every A vertex has degree one or two, and every D vertex has
degree at most two. Every component lies in a single physical row of a
single band. Since edges connect consecutive grid columns, H is a union
of alternating paths; no cycle is possible along a finite row. Isolated
D vertices are absent by definition and isolated A vertices were excluded.

A path can match all its A vertices to different adjacent D vertices
unless BOTH its endpoints are in A. For opposite endpoint types the parts
have equal size and alternating edges give a perfect matching. If both
endpoints are D, they have one extra vertex, and alternating edges from
one end match all A. Thus it is enough to exclude an A--A path component.

## 3. A purported Hall obstruction has no first freezing event

Suppose a component is an A--A path. Its vertices are consecutive occupied
positions in one row, with alternating types

    A_0, D_1, A_1, D_2, ..., D_s, A_s,   s>=1.       (2)

The packet boundary hypotheses ensure TP columns are internal. At each
end of (2), the other horizontal neighbor is occupied because the A
endpoint has no port. It cannot be an endpoint, since that would be a BP
neighbor and extend H. It is therefore selected.

Reflect vertically for notation so that (2) lies in row r and its TP
selections in row r-1. Every A_i has actual mate in row r+1. Every D_j
also has actual mate directly below in row r+1: its neighbor in row r-1
is blank, and its two horizontal neighbors A_{j-1},A_j are already matched
vertically and cannot be its actual mate. Matching closure and the BP label
exclude every other option. Write a_i and d_j for these respective mates.
All are distinct original endpoints.

Consider the nonempty set of endpoints

    U={D_1,...,D_s} union {a_0,...,a_s}.               (3)

For a D_j, the only nonmate occupied neighbors are A_{j-1},A_j. To freeze,
BOTH of their actual mates a_{j-1},a_j in U must have frozen earlier.
There is no selected neighbor in row r-1 and no outside horizontal neighbor.

For an a_i, its actual mate is A_i. Its horizontal neighbors inside the
segment are d_i and/or d_{i+1}. At an end of the segment, the outer horizontal
neighbor is blank: the selected neighbor just outside (2) in row r already
sees A_i, and forbids an occupied vertex immediately below itself. Besides
these horizontal neighbors, a_i has just one remaining nonmate neighbor,
in row r+2. Regardless of whether that vertex is selected, retained or
outside J, it can provide at most ONE of the two required witnesses.
Thus freezing a_i requires at least one d_j retained, whose mate D_j in
U must have frozen earlier.

Every member of U therefore requires another member of U to have frozen
STRICTLY earlier. Choose the earliest member of U in the full freezing
certificate. Its necessary predecessor contradicts earliestness. This
excludes (2), even with arbitrary feasible data and certificate events
outside the packet. No finite enumeration or bound on freezing depth was used.

## 4. Constructing the injection and the exact remaining limitation

By Section3 every path component of H has an endpoint in D. Start at such
an endpoint and pair each encountered A with the preceding D along that
path. This matches every A exactly once. Different components and different
pairs use different D vertices, proving (1). This is an explicit finite
construction, not an assumed Hall inequality.

If m TP--TP paths have a missing port and q_4 is the number of their missing
terminals, then m<=q_4<=2m. The injection supplies q_4 DISTINCT adjacent BP
terminals. But it does not establish m distinct unit credits. An actual
BP--BP path has two BP terminals, and a TP--BP path has one BP terminal and
zero signed credit. The all-parameter missing-port family has beta=0 and
all its assigned BP terminals lie on mixed TP--BP paths. It is already a
counterexample to interpreting (1) as an injection into BP--BP RESOURCES.

One possible next step is to cancel distinct adjacent TP/BP terminal pairs
and follow the resulting zero-charge paths toward original interval ports.
Such a continuation must prove its own multiplicity and termination bound;
new terminals must not be silently assumed to have BB ports. That continuation
and the unified inequality h_2+u<=h_0+beta remain open.

## 5. Degree-three terminality alone does not suffice

On a 4-by-10 board, take actual vertical matching edges

    (1,c)--(2,c), c=2,3,4,5,6,

and original selections

    (0,2),(0,4),(0,6),(3,2),(3,4),(3,6),(1,1),(1,7).

All unlisted vertices are blank. Each selection sees exactly one occupied
neighbor. Each endpoint has occupied degree at least three. The columns
2,4,6 give TP--TP paths and 3,5 give BP--BP paths. In the upper band the
three missing TP terminals at (1,2),(1,4),(1,6) have only the two adjacent
BP terminals (1,3),(1,5). This is an A--A component and has no saturating
matching. In the lower band only (2,4) lacks a port; the obstruction above
already suffices to refute (1).

Only (1,2),(1,6) freeze in the complete peeling procedure; the remaining
eight endpoints do not. Set (3) for the upper obstruction is exactly
{(1,3),(1,5),(2,2),(2,4),(2,6)}, a closed dependency set. Thus the example
violates complete freezing, as required, and shows why replacing that
hypothesis by occupied degree>=3 would be false. It is a counterexample
to the weaker injection rule, not to a global grid bound.

## 6. Validation and scope

The permanent companion checker constructs H from actual column paths,
checks its row/path geometry, constructs its matching, and checks that any
A--A obstruction yields the closed dependency set (3). For the explicit
nonfrozen control it checks feasibility, minimum occupied degree, the
actual freezing result and maximum adjacent-terminal matching size.
Finite controls do not replace Sections2--4.

The companion Lean source proves the generic impossibility of a nonempty
closed dependency set with a strictly decreasing freezing rank, including
the two witness classes used in (3). The actual grid geometry, construction
of H and path-by-path matching remain written mathematical proofs. No full
formalization of (1) is claimed.

The permanent checker develop/check_frozen_missing_port_bp_injection.py passes
450 models, including 433 fully frozen models and 143 nonempty frozen
injections. It checks 351 parameter triples, 26 mixed inventories and 72
fixture symmetry controls. The explicit nonfrozen configuration and its
symmetry images yield nine checked closed dependency obstructions. Its
path-based matching agrees with an independent augmenting-path algorithm.
Results are in output/frozen-missing-port-bp-injection-validation.json.

Local Lean4.33.0 passes both generic dependency theorems and their individual
ordinary-axiom audits, with no errors, warnings, sorry or native evaluation;
execution is recorded in output/frozen-missing-port-bp-injection-lean.json.
This verifies the strict-descent mechanism, not the whole grid injection.

Independent follow-up 45fb9297-002f-4008-a22d-e942edca9c41 in conversation
conv_9a8ee0adac356fe3 reviews this complete new theorem and the local
port-degree/adjacent-BP additions to the preceding note. The original
49645-character request is live; acceptance is not inferred from the
earlier partial-connector review.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
