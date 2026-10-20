# A wider positive U cap also cannot be completed

20 October 2026. The width-six cap obstruction uses a four-site stencil
that excludes every U owner at its first forced support. Enlarging that
cap to width eight removes that exclusion: a U source can own the site
without an endpoint collision. We prove that complete support retention
still makes the width-eight cap impossible. Both possible source types
at the first forced support lead to an unownable second support.

## 1. Model and statement

Use the complete U/rotor model, original endpoint disjointness and matching
union of POSITIVE_U_CAP_NONCOMPLETION_OBSTRUCTION.md. Original supports
outside final P must remain selected; a selected site cannot have two
occupied neighbors. Every final endpoint has an original source owner.

**Theorem.** The partial seed

    Rplus(0,0), Rplus(-3,0), Rplus(-1,-3),
    U(8,4,4)+(-4,-8)                                (1)

has no complete feasible extension by any number of permitted U(w,a,b)
sources and rotors, in arbitrary phases, translations and isometries.
Here even w>=6 and independent even a,b>=4 are unbounded. The theorem
also holds after a common lattice isometry of the whole seed. Optional
selections cannot remove original support obligations.

The seed has46 disjoint original endpoints. We do not assume it is
itself feasible. This theorem excludes (1), not every wider cap and not
the mixed-source allocation target.

## 2. Three local facts for arbitrary U dimensions

All offsets below are physical offsets from an endpoint z. A blocking
site is a known foreign original endpoint, so a candidate owner cannot
include it in its own endpoint set. The reference U endpoint set is the
two-row bar and its two stems as in the preceding note.

**Left-ray lemma.** If right, down and two-up from z are blocked, every
permitted U owning z has all four endpoints z+(0,-d), 1<=d<=4.

For completeness, the three-neighbor and opposite-neighbor cases of
the U endpoint classification are impossible because right and down
are blocked. An upper bar corner whose long bar points upward collides
at two-up; if its bar points left, its attached lower corner and stem
put an endpoint at two-up. The remaining possibility is a terminal
stem tip pointing right, with its stem going left. Its back-ray has
length at least four. This also proves the reference-coordinate normal
form: the physical left direction maps to negative stem row, and the
reference endpoint is (a,1) or (b,w).

**Support lemma.** If in addition six-left and two-up/four-left from z
are blocked, then z+up is an original selection of its U owner.

The left-ray description puts the terminal's height h between4 and5,
since a back-ray of length six would hit six-left. As permitted heights
are even, h=4. The two adjacent bar columns are four-left and three-left.
The bar cannot extend upward, since its outer column would contain
two-up/four-left. It therefore extends downward. At an even terminal
tip the exterior side support is upward, proving the claim. Its being
an original selection also proves that it is not an endpoint of this
same source. Each assertion is invariant under the source's isometry.

**Corridor exclusion lemma.** No U can own z if all six offsets

    right, up, down, six-left, up/four-left, down/four-left              (2)

are blocked.

The three adjacent blockers leave only left as an own-endpoint neighbor.
A bar corner has at least two such neighbors and a nonterminal stem
has an opposite pair; hence z is a terminal tip with its stem leftward.
Six-left bounds its height by5. For either h=4 or h=5, one of the two
bar columns is four-left. Whichever vertical direction the bar takes,
it hits up/four-left or down/four-left. This contradiction needs only
integer lower bounds on dimensions, even without a parity assumption.

These are general role proofs. They do not infer a dimension bound from
finite samples. For an image f(x)=t+Ax, the corresponding formal
coordinates are f-inverse(z+delta)=e+A-inverse(delta); signed coordinate
permutations exhaust all eight source isometries.

## 3. The first forced support has only two ownership branches

Let P0 be the seed endpoint union. The original support p=(-1,-1) is
not in P0 and has the two persistent endpoint neighbors (-1,0),(0,-1).
Thus every complete feasible extension must put p in its endpoint set.
Its owner is foreign to the four seed sources.

The seed contains the five blockers required by the support lemma:

    (-1,0), (0,-1), (-3,-1), (-1,-7), (-3,-5).          (3)

If p's owner is a rotor, exact normalization to two chiralities and eight
endpoint roles each leaves the unique noncolliding rotor Rplus(-3,-5).
This finite role table exhausts all integer translations, not a bounded
source library. If its owner is a U, the left-ray and support lemmas
apply without bounding that U's width or either independent height.

## 4. Rotor ownership of p is impossible

The forced rotor Rplus(-3,-5) is endpoint-disjoint from P0 and has the
original support q=(-2,-1), the image of reference support (1,4).
The points (-3,-1),(-2,0),(-1,-1) are persistent endpoint neighbors of q.
Therefore q must be an endpoint of another source, foreign to the five
known sources. It is not an endpoint of any of those sources.

The four known endpoints

    (-3,-1), (-2,0), (-2,-3), (2,-1)                  (4)

form a signed transposed image of the preceding note's universal U
blocking stencil relative to q: up, right, two-left, four-down. Thus
no U can own q. The exact sixteen-role rotor table against the known
endpoint union is empty, so no rotor can own it either. Contradiction.

## 5. U ownership of p is impossible

By the left-ray lemma, the U owning p contains the five endpoints

    (-1,-1),(-1,-2),(-1,-3),(-1,-4),(-1,-5).           (5)

By the support lemma, q=(-2,-1) is an original support of this same U.
It is not that U's endpoint. It is also not a seed endpoint. Since q
has the persistent endpoint neighbors (-3,-1),(-2,0),(-1,-1), it must
belong to the original endpoint set of a further, foreign source.

Already P0 together with only the five guaranteed endpoints in (5)
contains the six-site corridor barrier (2) around q:

    (-2,0),(-3,-1),(-1,-1),(-2,-7),(-3,-5),(-1,-5).

The corridor exclusion lemma rules out every U owner of q. The exact
sixteen-role rotor table against that same lower bound on known
endpoints is empty. Adding more endpoints can only remove candidate
owners, so considering the U's remaining endpoints cannot help.
Again q has no permitted owner. This proves the theorem.

The proof is static inside a hypothetical extension. A source already
present among its additional sources must obey the same owner exclusions;
no chronological construction is assumed. Optional selections cannot
remove either required original support or its persistent neighbors.

## 6. Verification and scope

develop/check_width_eight_u_cap_obstruction.py checks the exact seed,
three complete16-role tables, both second-support neighbor conditions
and the four-/six-site barriers. It also checks the endpoint/support
lemmas on representative independent U dimensions and all isometries.
Those finite controls only test the general arguments above.

The Lean development formal/SubQuorum/WidthEightUCapObstruction.lean
contains universal coordinate lemmas and exact local geometry. All16
declarations compile and pass individual axiom audits locally with
Lean4.33.0, one job,57% free memory before the source run and59% before
the full-current-source audit. No real lean/lake process was active at
either preflight, checked by comm basename. No sorryAx/native_decide.
See output/width-eight-U-cap-obstruction-formal-check.json.
The source-image adapters, connection of the
support formula to the complete constructor, and assembly of the two
branches into noncompletion are written; no full Lean theorem of all
arbitrary source extensions is claimed.

A finite24x24 SAT check with a fixed U(6,4,4)/rotor library found UNSAT
for this cap. That result alone excludes only that finite search. The
proof above permits all U dimensions and all source counts and does not
depend on that UNSAT conclusion.

This width-eight theorem is later than the accepted width-six review;
no earlier ACCEPT covers it. Arbitrary wider caps and the general mixed
U/rotor compensation inequality remain open. No email, draft or submitted
manuscript action is part of this result.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
