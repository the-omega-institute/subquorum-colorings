# A frozen elbow contains no allowed U or rotor source

22 October 2026. Authors: Haobo Ma and Wenlin Zhang.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.

## Statement and relevance

The coefficient 39/41 in BLOCKED_MARK_CAPACITY_AND_39_41.md applies to its
specified complete immutable full-even-U/standard-rotor source model. A
possible bridge would decompose every frozen endpoint component into those
sources without changing its endpoints. The following family rules out this
bridge, even if matching and selected-support compatibility are ignored.

For even W>=6 and H>=4 define

    E(W,H) = ({0,1} x {0,...,W-1})
           union ({2,...,H-1} x {W-2,W-1})
           union {(2,0),(H,W-1)}.

**Theorem.** E(W,H) contains no translated grid isometric image of the
endpoint set of any allowed U(w,a,b), w>=6 and a,b>=4, and contains no such
image of a standard rotor. Consequently it has no cover by these endpoint
sets, including covers that allow overlap. This holds in every physical
tiling phase. The exclusion itself does not require even W,H,w,a,b.

These are actual feasible fully frozen single-terminal endpoint components,
with the prescribed matching and supports in ELBOW_SOURCE_COMPENSATION.md,
Section 1 and develop/check_elbow_sources.py::elbow. Their feasibility,
freezing, receiver charge 1 and owned-donor payment are existing results.
The new statement is exclusion of even a *subset* source, not just failure
to identify the whole component with a single source.

## General proof

Write a unit square by its top-left corner (r,c). If all four square
vertices lie in E, then either r=0 or c=W-2. To see this, below the top
two-row strip, the only two consecutive occupied columns are W-2,W-1.
The exceptional left tip (2,0) has no horizontal occupied neighbour at
(2,1), and the bottom tip (H,W-1) has no neighbour (H,W-2).
Thus neither tip produces an additional full square.

Any full horizontal two-row bar of length at least 3 has squares at its
first and last column pairs. If its top row were not 0, the square
classification would force both pairs to start at column W-2, impossible
for length at least 3. Hence it is in rows 0,1. Similarly any full vertical
two-column bar of length at least 3 is in columns W-2,W-1.

An allowed U has a full two-row bar of length w>=6, and both thin legs
extend from the bar's end columns to at least row 4 in standard coordinates.
Consider all possible orientations of its bar and legs:

- For a horizontal bar, its rows must be 0,1. Upward legs are impossible
  since row -1 contains no endpoint. For downward legs, the two leg sites
  in row 3 must both lie in {W-2,W-1}. Their separation is w-1>=5,
  whereas those two columns differ by at most 1. This is impossible.
- For a vertical bar, its columns must be W-2,W-1. Rightward legs would
  meet empty column W. For leftward legs, consider the two leg sites at
  column W-4. Since W>=6, this column is at least 2 and is neither of the
  two right-strip columns. Its only possible endpoint rows are 0,1.
  The leg origins are separated by w-1>=5, again impossible.

This exhausts rotations and reflections and excludes every allowed U.

A standard rotor has a central full unit square and a protruding endpoint
across each of its four sides, under every grid isometry. If its square is
in rows 0,1, its north protrusion is absent from E. Otherwise the square
classification puts it in columns W-2,W-1, whose east protrusion is absent.
Thus no rotor is contained. Translations and tiling phases do not affect
these endpoint-set arguments. Since E is nonempty and contains no individual
source, no union of contained sources can cover it. QED.

## What this obstruction settles

This refutes unchanged-endpoint decomposition into the present source
inventory. It is not a counterexample to the desired grid inequality or
triple equality, nor does it refute a normalization that changes endpoints
and proves that the objective and feasibility are preserved. The elbow's
own charge is already paid by its known uniquely owned sparse donor.

A general-grid proof therefore needs a broader primitive inventory, an
objective-preserving normalization with support compatibility, or a direct
receiver-and-donor inequality that bypasses complete source decomposition.
Adding elbows alone is not a completed bridge: any common ledger must also
prove that an elbow donor is not spent again as a U/rotor reserve tile.
The existing physical receiver partition is a useful common accounting
domain, but a universal compensation theorem remains open.

## Verification and its scope

formal/SubQuorum/ElbowSourceExclusion.lean defines the exact infinite
endpoint predicate, full squares and full bars. It proves the square and
bar classifications, all four U-orientation exclusions, and rotor
exclusion over arbitrary integer coordinates. These are universal geometry
lemmas; they do not formally encode the existing freezing certificate,
the source constructors, or their isometry-to-motif adapters. Those
adapters are the explicit geometric observations in the proof above.

Run the independent containment controls with

    PYTHONDONTWRITEBYTECODE=1 python3 develop/check_elbow_source_exclusion.py --output output/elbow-source-exclusion-validation.json

The search enumerates every placement and all eight orientations of each
minimum-leg template U(w,4,4), with every even width that fits the host
bounding box, and of the standard rotor. Every allowed U(w,a,b) contains
U(w,4,4) at the same bar, so this tests all feasible dimensions within each
finite host. Positive controls place each template inside a translated copy
of itself. The finite search checks the constructors and the proof's
application; it does not replace the general argument.

Completed local verification: all 8 geometry theorems and 4 definitions have
individual axiom audits, with only propext and Quot.sound used by the
theorems; no errors, warnings, sorry or native evaluation. The finite
controls pass for 72 feasible frozen base elbows, 2,304 endpoint images,
1,584 full-square checks and 288 positive search controls over 72 oriented
templates, with zero contained sources. See the validation receipts in output/.

No submitted manuscript is changed. Independent mathematical review bc36dde9
completed ACCEPT on22October at06:49UTC, including the full endpoint-only
source exclusion and its use in the matching-exchange persistence argument.
See output/rematching-receiver-flux-review-accepted.json. This review concerns
the written proof and coordinates, not execution of code or Lean.
