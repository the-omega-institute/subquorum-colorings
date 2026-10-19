# Intrinsic stepped-patch recognition and coefficient one with attached exterior paths

19 October 2026. A prescribed stepped patch need not initially be a complete
endpoint component. Its matching and selected supports expose exactly one
possible endpoint attachment, at a vertex of occupied degree two. At most
one objective-preserving single promotion isolates the entire frozen patch.
Distinct prescribed patches are automatically disjoint after identical
endpoint sets are identified, and their isolation moves can be composed.

This gives a coefficient-one theorem from an initial structural hypothesis:
after deleting the prescribed patch endpoints, the remaining endpoint graph
is square-free. There is no initial terminality, component-completeness,
separation, channel-cover or Hall hypothesis. The theorem concerns this
explicit class and does not prove the universal receiver-charge ceiling or
the unrestricted grid inequality. Submitted manuscripts are unchanged.

## 1. Prescribed data and forced blanks

Let (T,M) be any feasible pair on an even-by-even rectangular grid. Set
P=V(M). Retain a copy of the endpoint set H_k, actual matching M_k and
selected supports S_k of `GUARDED_CORNER_AND_STEPPED_ARMS.md`, k>=1,
b=2k+4. Every named site belongs to the ambient grid. In this note these
conditions mean only M_k subset M and S_k subset T. Do not assume H_k is
a complete component, or that the surrounding pair is terminal.

For the counting theorem use the prescribed positive physical phase: relative
tile starts are even rows and odd columns, transported by physical-tile-preserving
symmetries. The boundary and isolation lemmas themselves are invariant under
every grid translation, rotation and reflection, without a phase condition.

Every selected support s in S_k has a unique neighbor p_s in H_k. Since
s already sees p_s, feasibility forces every other neighbor of s blank.
Put

    B_k = union_(s in S_k) (N(s) minus {p_s}).       (1)

All sites of B_k in the grid are blank in every feasible exterior preserving
the prescribed data. Blank extension outside the grid only strengthens
these exclusions. None of this uses component completeness.

## 2. Exact all-length boundary classification

Let U_k=N(H_k) minus (H_k union S_k union B_k). Then exactly

    U_k={(-1,3),(1,5),(4,3)}
          union {(r,3): r=6,8,...,b-2}.             (2)

Here and below an empty index range contributes no sites. The complete
boundary check is as follows; S and B in the table mean membership in
S_k and B_k, respectively.

| Boundary part | Labels or unresolved sites |
| --- | --- |
| Top row (-1,j), j=0,...,3 | B,S,B,unresolved |
| Outer left (r,-1), r=0,...,b | S on even r, B on odd r |
| Cap right (0,4),(1,4) | S,B |
| Upper chamber step (1,5) | unresolved |
| Outer right (r,6), r=2,...,b | S on even r, B on odd r |
| Inner left (r,3), r=4,...,b-1 | unresolved on even r, B on odd r |
| Bottom inner left (b,3) | S |
| Inner right (r,4), r=4,...,b | B on even r, S on odd r |
| Bottom (b+1,j), j=0,1,2,5 | S,B,S,S |

The upper step at (1,4) and lower chamber steps (4,3),(4,4) are already
included in the listed parts. These are every site adjacent to (1) of the
companion phase note, with duplicates removed. For example an odd outer
site neighbors the preceding even support. An odd inner-left site neighbors
the same-row inner-right support. An even inner-right site neighbors an
adjacent odd support, including r=4 since k>=1; at r=b it also neighbors
the prescribed (b,3). Top and bottom exclusions come from the displayed
axial supports. This verifies all B entries and proves (2) for arbitrary k.

After excluding B_k, the possible occupied neighbors of unresolved sites
are exactly bounded by this finite-type table:

| Unresolved site | Neighbors outside B_k |
| --- | --- |
| a=(-1,3) | q=(-2,3), p=(0,3) |
| (1,5) | (2,5) |
| (4,3) | (3,3),(4,2) |
| (r,3), even r=6,...,b-2 | (r,2) |

For the top port, (-1,2) is blank beside (-1,1), and (-1,4) is blank
beside (0,4). At (1,5), its other three neighbors are excluded by (0,4)
and (2,6). At (4,3), its lower and right neighbors are excluded by (5,4).
For every other even inner-left site, the two adjacent odd-row supports
exclude its upper, lower and right neighbors. All named neighbors other
than q belong to H_k and are already matched inside M_k.

**Intrinsic boundary lemma.** In any feasible extension retaining M_k,S_k,

    (P intersect N(H_k)) minus H_k subset {a}.       (3)

If a is an endpoint, its actual mate must be q, and its occupied neighbors
are exactly p,q. In particular deg_A(a)=2.

Proof. A site of S_k is selected and a site of B_k is blank. At every
other unresolved site except a, every possible endpoint neighbor already
has its prescribed mate in H_k. A new matching endpoint cannot be matched
to one of these vertices without replacing an edge of M_k. Thus none of
those unresolved sites is P. At a, p is similarly unavailable as a mate,
leaving only q. If q is outside the grid, a cannot be P either. If a is P,
the edge aq is present and both p,q are occupied; its other two neighbors
are blank by the table. This proves all assertions. QED.

Only the actual matching, not an assumption of component completeness,
excludes the unresolved degree-one and degree-two inner sites. In particular
(4,3) has two old endpoint neighbors and is not declared blank by (1).
It cannot be P because both neighbors are already matched, and cannot be
T because it would see those two endpoints. It is consequently blank.

## 3. One move isolates the patch

**Isolation theorem.** Every feasible pair retaining M_k,S_k admits a
feasible objective-preserving modification with the following properties:

- M_k and every original selected vertex are retained;
- H_k is one complete endpoint component;
- zero or one additional matching edge is removed, and at most one vertex
  is added to T;
- every endpoint of H_k remains universally frozen.

Proof. If a is not P, (3) already makes H_k complete. If a is P, its
actual edge is aq and deg_A(a)=2. Promote a to T and remove its mate q,
deleting that edge. The new selection a sees only p, while old selections
only lose occupied neighbors. Hence the new pair is feasible. One matching
edge is replaced by one selection, preserving |T|+|M|. Neither endpoint
of aq belongs to H_k, so M_k and S_k are unchanged. No other endpoint
can neighbor H_k by (3), so H_k is now complete. The earlier all-k frozen
certificate uses only M_k and S_k and therefore remains valid. QED.

In a globally single-terminal pair, a cannot initially be P because its
degree would be two. Thus a prescribed patch is already a complete component
in every such representative. This removes the previous completeness
hypothesis when applying the receiver and phase theorems to that representative.

After isolation, arbitrary exterior normalization cannot destroy the patch:
the frozen exclusion theorem prevents promotion of its endpoints, matching
closure prevents their mates from being removed by another edge, original
T is retained, and no promotion adds a new endpoint. Its whole receiver
charge, physical unit donor and both phase tables therefore apply exactly
with their original boundary/phase hypotheses.

## 4. Several patches: overlap and shared moves

Consider finitely many prescribed copies, possibly of different lengths and
orientations. No disjointness is assumed. Each copy's prescribed data alone
gives every endpoint occupied degree at least three. Equivalently, in its
ordered freezing certificate the two retained witnesses differ from its
actual mate, which is a third occupied neighbor.

**Overlap lemma.** Two prescribed endpoint sets that intersect are identical.

Proof. Suppose H and K intersect. Follow any path in the connected graph K
from the intersection. Its first step outside H would be an endpoint on
H's external boundary, hence the unique port a_H by (3). But a_H has
occupied degree two, whereas every endpoint of K has degree at least three.
The path cannot leave H, so K subset H. Reversing the argument gives
H subset K. Thus H=K. QED.

Deduplicate identical endpoint sets. They are now pairwise disjoint. An
occupied port of any patch has degree two, so belongs to none of these
prescribed endpoint sets. Its actual mate also belongs to none: otherwise
matching closure of that other patch would put the port there too.
Consequently each isolation move preserves all prescribed matching edges
and selections, and the same boundary certificate remains available at
the next step. No P is added, and at least the chosen occupied port ceases
to be P. After at most as many moves as distinct patches, all are isolated.

It is possible, without imposing the positive physical phase on both copies,
that two ports are the endpoints of the same matching edge. Promote one
endpoint and remove the other. This single move isolates both patches;
it must not be counted or performed twice. The sequential argument above
handles this automatically and does not assume one distinct edge per patch.

## 5. A coefficient-one theorem from an initial square-free exterior

**Prescribed-patches plus square-free exterior theorem.** Suppose a feasible
initial pair on an even-by-even rectangle contains finitely many prescribed
stepped patches in their positive physical phase, with their actual matchings
and supports. Let H_1,...,H_s be their distinct endpoint sets. Assume only
that the graph induced by

    P minus union_i H_i

contains no all-P unit square. Then

    |T|+|M| <= mn/2.                                 (4)

No initial terminality, completeness, external matching orientation, collar
separation or resource-allocation assumption is imposed.

Proof. The overlap lemma makes distinct H_i disjoint. Apply at most s
isolation singles, retaining every prescribed patch and the objective.
Then single-normalize the whole pair. No core endpoint can be promoted,
because its frozen certificate survives. All remaining endpoint components
outside the cores stay square-free since promotions only remove endpoints.
At the terminal representative the square-free component theorem makes
each such component a straight even comb of whole receiver charge zero.
Every H_i has whole charge one. Terminal tile ownership gives disjoint
whole receivers, including all saturated transfers.

For each H_i its prescribed guarded donor Q_i is endpoint-free and has
exactly one selection, hence d_(Q_i)=1. These tiles are distinct: sharing
a tile would identify its unique selected corner and its unique occupied
anchor, placing that endpoint in both cores, contrary to disjointness.
The exact receiver ledger consequently gives

    Delta=mn/2-|T|-|M|
         =sum_(Q no-P) d_Q-s
         =sum_(Q no-P, Q notin {Q_1,...,Q_s}) d_Q >= 0.     (5)

No donor is used twice. The objective was preserved throughout, proving
(4) for the initial pair. Equality holds precisely when every remaining
no-P tile in this terminal representative is saturated. QED.

The case s=0 is the earlier square-free endpoint theorem. This extension
allows a positive core to begin inside a larger endpoint component with
arbitrary square-free attachments, and allows multiple cores before their
automatic disjointness and isolation are established. It removes the entire
|M|/6 loss of the universal 5/6 bound on this explicit initial class. It
does not establish the required structural cover for arbitrary configurations.

## 6. Two exact attached families and partition bookkeeping

For one patch H_k, add a straight branch at its port. For any L>=1 add
endpoints (-j,3), j=1,...,2L, paired consecutively from j=1, and selections

    (-j,4) for even j=2,...,2L,
    (-j,2) for odd j=3,...,2L-1,
    (-2L-1,3).

Every new selection sees exactly its branch endpoint; they alternate sides
and are separated from S_k. The only nonterminal branch endpoint initially
is a=(-1,3), of degree two. All other branch endpoints have degree three,
including the far tip with its axial support. Promoting a removes (-2,3),
isolates H_k, preserves the objective, and leaves a square-free exterior.
The additional objective before or after isolation is exactly3L: there are
2L new selections and L new matching edges before the move. This proves
(4) on an arbitrary-length attached family without assuming a blank collar.

For a shared-edge example, take H_k at its given coordinates and a second
H_j mapped by (r,c) to (-3-r,6-c). Add the matching edge
(-1,3)--(-2,3). The footprints are feasible for all k,j>=1: their top-cap
supports face different column sides, with no new occupied adjacency except
this bridge and its two anchors. Both ports have degree two and both core
certificates survive. Either orientation of one single promotion isolates
both cores. This reflection changes the second core's column alignment;
its receiver charge is -j, not +1. The example tests shared-operation safety
but is not an example with two positive-phase cores.

For two positive-phase patches, use instead the reflection
(r,c) to (-2L-1-r,c), L>=2, and join their ports by the consecutive
vertical path (-h,3), h=1,...,2L, with its L consecutive matching edges.
No outside selections are added. The two nearest axial top-cap supports
are separated by at least three rows, so feasibility holds for all k,j,L.
The exterior path is square-free. Its L physical tiles each have two P
and no T. The initial giant receiver therefore has raw charge2-L, while
its two prescribed positive cores each have local receiver charge one.
Two port singles isolate the cores; subsequent singles remove the remaining
exterior matching edges. The final exact ledger is Delta=D_all-2>=0,
using the two distinct guarded unit donors. At L=1 the two nearest
top-cap selections would be adjacent, violating feasibility; no two-positive
shared-edge example is claimed.

In the mixed-alignment shared-edge family, the initial bridge tile has two
P and no T, raw charge -1. The two separate
core receivers have charges1 and -j. Thus the original giant receiver has
raw charge -j. After isolation the receiver charges sum to1-j, while the
now endpoint-free bridge tile has one T and deficit one. The global ledger
still has excess -j. Ignoring that newly exposed donor would misreport the
partition change. No universal ceiling is proved or refuted by this family.

## 7. Verification and open scope

`develop/check_stepped_patch_isolation.py` independently checks the boundary
certificate for34lengths through k128,16arbitrary-length branch controls,
128symmetry images,16shared-port cases in both promotion orientations,
and48two-positive-core path connections.
It recomputes actual matching feasibility, degrees, frozen certificates,
objective preservation, complete components, final receiver charges and the
shared-edge partition identity. These are controls for the all-k proof above.

The new Lean module checks the physical degree-two port bound, exclusion
of a new endpoint whose only possible mates are in a closed prescribed
matching, endpoint-path closure, and post-removal port feasibility. The
full coordinate boundary table, multi-patch operation/count proof and
coefficient-one adapter remain written proofs. Execution and external review
status are recorded separately; no full formalization is claimed.

The sequential local Lean4.33.0 audit completed ALL_CHECKS_PASSED for137scoped
declarations at2026-10-19T15:55:41.535105+00:00, including these four additions.
The real executable-basename Lean/Lake count was zero before execution;
peak child RSS was about1.05GB. The receipt is
`output/stepped-patch-isolation-formal-check.json`. No admitted or compiler
reduction axioms occur. The task-owned regenerable cache is removed after
confirming no real Lean/Lake process remains.

Reproduce the controls and scoped formal audit with:

    python3 develop/check_stepped_patch_isolation.py --output output/stepped-patch-isolation-controls.json
    python3 scripts/check_collar_formal.py --lean /path/to/lean-4.33.0 --output output/stepped-patch-isolation-formal-check.json

No independent written assessment of this isolation theorem has yet been
returned. Earlier guarded/stepped review and phase-review quota records have
their own scope; neither is an acceptance of this later extension.

Finite exploratory searches for a connected frozen charge-two receiver
remain finite only: a10by10rooted interior search was unsatisfiable, while
larger frozen/terminal searches timed out. They prove no universal ceiling.
The phase-note follow-up was again rejected by the broker's occupied
ten-task quota; there is no new task or mathematical verdict. Unique streams
and all previously live search handles are preserved.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
