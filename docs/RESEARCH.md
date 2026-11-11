# From the hypercube solution to grids and structural characterization

Current status (12 November): the [extended-double-cover theorem](EXTENDED_DOUBLE_COVER_PARAMETERS.md)
settles SF_2=beta_2=psi_sq=Omega for every E(H), including every bipartite
Cartesian prism H square K_2. Its value is 2n-nu(D(H)), or 2 alpha(H) in
the bipartite prism case. A shared two-per-empty-rung witness budget gives
the star-forming upper bound. This supplies a structural equality class
beyond the signed-matrix criterion. The [current completion record](COMPLETION_20261112.md)
also contains the exact fixed-width TH optimizer, the general zero-expense
extended-cover theorem and the positive-expense height-three family.
Wider rectangular-grid triple equality and the universal 5/6 improvement
remain open; the adjacent-pair involution cannot exist when both grid
dimensions are at least three.

The starting point is the completed proof of Sahbi's Conjecture 6.4:
psi_sq(Q_n)=2^(n-1) for every n>=2. Its Lean formalization checks this
all-dimensional statement. The boundary injection and its Hall-matching
consequence supply the main conceptual link to further research.

## Rectangular grids

The target is Sahbi's formula for arbitrary rectangular grids. Widths
8,9,10,11 are now proved at all positive lengths using exact full-vector
certificates and the existing periodic lower-bound constructions.

The [uniform grid arguments](GRID_RESULTS.md) now prove beta_2=F and
Omega_H=Omega_V=F at all dimensions. On even-by-even rectangles they give
|T|+(5/6)|M|<=mn/2 for arbitrary matching directions. The next step is to
strengthen this coefficient to one by controlling longer residual paths and
their global compensation, then account for odd-side boundaries. Exact
frontier states and constructed geometric examples test these arguments.

A proof of Omega(G_mn)<=F(m,n) would settle the grid coloring conjecture.
A counterexample to that stronger Omega bound would require revisiting the
reduction's sharpness; it would not by itself refute the coloring conjecture.

## Structural characterization

The target is to identify conditions under which psi_sq(G)=beta_2(G).
The signed boundary theorem gives a sufficient class, including appropriate
bipartite Cartesian products. The grafting formula gives exact counterexamples
to overly broad conditions: the gap can be unbounded even on subcubic trees.
The equality class is not hereditary, so a general characterization purely
by forbidden induced subgraphs is unavailable.

The next step is to examine natural restricted graph families, use the exact
tree recurrence to test candidate conditions, and prove conditions that
explain equality beyond the current signed-matrix hypothesis. Compare the
tree results with the earlier caterpillar work cited by Sahbi.

## Role of formalization and the manuscript

The current Lean proof covers the hypercube coloring-number equality.
Formalizing the general boundary theorem and subsequent structural lemmas
will support the two research directions. New computation and formalization
should be connected to a stated mathematical claim.

The manuscript's narrative is: solve the hypercube problem, extract the
boundary mechanism, then establish progress on grids and structural equality.
State the solved conjecture at its full strength and distinguish the exact
strip theorems from the still-open arbitrary-width grid conjecture.
