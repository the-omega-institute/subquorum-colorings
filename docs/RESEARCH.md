# From the hypercube solution to grids and structural characterization

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

The [local-quota cut theorem](LOCAL_QUOTA_CUTS_AND_FROZEN_BATCH_OBSTRUCTION.md)
strengthens the two strip-allocation rules and reduces the first possible
charge-five resource failures to three leaf-free motifs. It also gives
an unbounded fully frozen family where every nonempty batch of the four
current corner-rule donors lowers the budget. Safe donor ordering or
reserving all donors cannot be assumed in the remaining coverage proof.

The [branched rotor theorem](BRANCHED_ROTOR_NETWORKS_AND_UNBOUNDED_RECEIVER_CHARGE.md)
extends coefficient-one compensation to admissible networks of two-leg and
four-port rotor modules. It assigns a distinct actual unit donor to every
positive module, even within the same receiver. An arbitrary-length fully
frozen occupied-degree-three family has receiver charge k+1, disproving any
constant ceiling in that setting while still satisfying compensation. This
separates the false receiver-ceiling rule from the open universal inequality.

The [physical fusion theorem](DEGREE_THREE_FUSION_AND_PROTECTED_DONORS.md)
removes prescribed ports and once-used-port restrictions. Actual receiver
charges add with an exact minus-two correction per new aligned full endpoint
square, plus the intratile new-neighbor defect if degree four appears.
Protected donor loss and this latter defect use disjoint degree-four endpoint
events. A physical count criterion therefore proves coefficient one with
controlled degree-four contacts, including an all-width fully frozen pair of
occupied adjacent bands. General decomposition into covered modules is open.

The [opposed-band theorem](OPPOSED_BANDS_AND_HARMLESS_DEGREE_FOUR_CONTACTS.md)
rules out automatic validity of the coarse degree-four criterion. For every
even width w>=6 and height h>=4 it gives a fully frozen physical fusion with
S=w-1, J=K_in=0, L=1 and d4=2h+4. The finer compensation credit is w-2
and the exact half-area slack is h(w-4)/2+2. Thus harmless intertile contacts
can grow without bound while the actual tax stays one. All four alignment
phases satisfy the finer criterion. Twenty parameter pairs,80alignment checks,
640symmetry images and67scoped Lean declarations pass, including actual
mixed-bundle exclusion for the8-by10configuration. General geometry has its
own written all-parameter proof; the broad d4 rule cannot be a universal bridge.

The [two-guard surplus theorem](DUAL_GUARDS_AND_CROSS_COMPONENT_SURPLUS.md)
retains two distinct actual unit donors per positive two-leg module. If N
positive covered modules have G marked sides and additional supported modules
have total old charge tau, it proves D>=2N-G, K_in+G<=d4 and
sigma>=N+S+2J-K_in-G-tau. The credit gains one unit per unmarked right side
over the previous canonical-left budget. Four-way cycles and rotor stars now
have guaranteed slack six, and k-star chains have slack at least 7k-1.
An explicit three-component assignment pays an external charge two without
reusing a tile. General geometry has a written proof; 57 cases, 288 phase
images and 19 scoped Lean declarations pass. This improves the surplus in
the stated module class, without a universal grid or ownership-flow claim.

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
