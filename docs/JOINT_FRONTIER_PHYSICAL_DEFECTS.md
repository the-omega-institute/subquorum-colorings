# Joint boundary labels: exact unrestricted defects and physical fees

The strip and bridge-block results optimize full auxiliary matchings N
confined to prescribed two-column cells. Their obstruction examples show
that a chosen cell class can leave TT paths even when an unrestricted N
has none, and that feasible half-area grids need not have bounded block
cycle rank. This note removes BOTH restrictions from the physical model.

A four-label formulation records every residual TT component and its real
TH expense. A joint boundary transfer then optimizes over ALL full grid
matchings N, without assuming low cycle rank, bridge separation, or an
independent scalar reserve per port.

Finite-state frontier dynamic programming and integer scalarization of a
bounded lexicographic objective are standard methods. The contribution here
is the exact physical four-label adapter, including residual components,
and its use to optimize the actual fixed-M certificates. No new general
frontier-DP method or universal numerical 5/6 bound is asserted.

## 1. Exact unrestricted objective

Let G be an h-by-w rectangular grid, with black vertices at even coordinate
sum. Let M be a fixed actual partial grid matching, P its endpoint set,
T a subset of Q=V\P, and H=Q\T. Each actual e in M has a nonnegative
integer weight w_e. No selected-degree hypothesis is needed for this model;
examples used for the sub-quorum application identify feasibility separately.

N ranges over ALL full grid domino matchings, including edges crossing any
previous cell boundary. In the tagged union M+N, shared edges are doubled
P-only components. Every other component is a P-only alternating cycle or
an odd alternating path with endpoints in Q. Put

    a(N) = number of TT paths,
    f(N) = sum of actual M weights on all TH paths.

The objective is the lexicographic minimum (a,f): first minimize the residual
TT count, then the real expense among matchings with that minimum count.
Thus the optimum number of unpaid selections in these certificates is 2a.
Complete coverage exists if and only if the minimum a is zero.

For positive even area a full N always exists. For odd area none exists,
and the implementation returns None. T may have more vertices than H;
the solver then returns the exact residual rather than treating absence
of complete coverage as a failed or infeasible optimization run.

## 2. Four labels and an exact nonnegative objective

Use 0,R,B,D with the following allowed vertex labels:

| Vertex | Allowed labels |
| --- | --- |
| black T | R or D |
| white T | B or D |
| black H | 0 or B |
| white H | 0 or R |
| P | 0, R, B or D |

Both endpoints of EVERY actual M edge and EVERY chosen N edge must agree.
Write W=sum_e w_e and U=W+1. Assign the scalar label cost

    L = U * number of black T vertices labelled D
        + sum_(e in M) w_e [label(e) is R or B].          (1)

**Four-label exactness theorem.** The minimum (1) equals the minimum of
U*a(N)+f(N) over all full physical N. Its minimizers, after free-cycle
normalization, attain the exact lexicographic minimum (a,f).

Proof. An M+N terminal path starts and ends with N, hence has odd length
and opposite-checkerboard-colour endpoints. The restrictions imply:

* an R terminal path is black T to white H;
* a B terminal path is black H to white T;
* a 0 terminal path is HH;
* a D terminal path is TT, with exactly ONE black T endpoint.

In particular no connectivity pairing needs to be guessed to determine
the contribution of a monochromatic complete component. Every black
T labelled D belongs to exactly one D terminal path: it is an unmatched-M
vertex and cannot lie on a P-only cycle. Thus the first term of (1) is
EXACTLY U*a(N), not a relaxation or an upper estimate.

Given any full physical N, label its four terminal path types accordingly
and its P-only cycles 0. This is feasible and (1)=U*a(N)+f(N). Conversely,
a feasible labelled matching has the same exact TT term; the second term
charges all TH actual edges and perhaps extra R/B P-only cycle edges.
Recolour each entire such cycle 0, leaving M and N fixed. Its vertices
all lie in P, so terminal restrictions and the TT term are unchanged.
Nonnegative weights make the change nonincreasing. The two optimum
inequalities prove equality. D cycles also contain no selected vertex
and may be recoloured 0; zero-weight R/B cycles are harmless.

Finally 0<=f(N)<=W. If a_1<a_2 then

    U*a_1+f_1 <= U*a_1+W < U*(a_1+1) <= U*a_2+f_2.

For equal a, comparing the scalar compares f. Hence U=W+1 implements the
lexicographic order exactly, including W=0 and arbitrarily large weights.
No floating-point infinity, infinitesimal, or bound on weight size is used.

## 3. A sufficient joint separator state

Transpose if necessary, so the scan has height s=min(h,w) and length
ell=max(h,w). Transposition preserves bipartition parity, physical grid
edges, weights and terminal types. Process vertices column by column,
within each column from top to bottom.

At the introduction of v=(r,c), the frontier contains the most recent
processed vertex of each row. Its row-r slot holds (r,c-1), if c>0;
the row-(r-1) slot holds (r-1,c), if r>0. The other slots hold either
the current or previous column as determined by the scan stage.
Initially unintroduced slots are implicit from that stage.

For each live frontier vertex retain its FOUR-WAY LABEL and whether it
has ALREADY been covered by a chosen N edge. These are eight possibilities
per slot. The full joint tuple, not its marginals or total capacity, is
the separator state.

Why it is sufficient. Every edge joining a processed vertex to an
unprocessed vertex touches one of these frontier vertices. An actual M
edge has its equality checked when its second endpoint is introduced.
Each possible N edge is selected, or omitted, at that same later endpoint.
Therefore two prefixes with the same joint labels and covered bits admit
exactly the same continuations, with the same remaining costs. Paths that
already closed have fully local cost (1); future feasibility does not depend
on their internal pairing. The four-label exactness theorem is what permits
this omission of connectivity-pairing states.

This does not justify replacing a joint tuple by independent port labels:
the table value is an arbitrary function of the entire tuple. Such a
factorization would lose physical correlations at shared cells.

## 4. Local transition and correctness induction

At v choose an allowed colour, and choose exactly one of these actions:

1. Add no N edge to the prefix: v remains uncovered for a future neighbour.
2. Match v to the left vertex, if that vertex is uncovered and has the
   same label. Mark v covered and forget the now-covered left vertex.
3. Match v to the upper vertex, if that vertex is uncovered and has the
   same label. Mark both covered.

In actions 1 and 3, a left vertex being forgotten must already be covered.
In every action, enforce equality with a prior actual-M neighbour, if any.
There is at most one such M neighbour since M is a matching. Its actual
weight is charged once NOW if the label is R or B. Charge U once at a
black selected v when its chosen label is D. Labels and covered bits at
other frontier slots remain unchanged.

The left vertex has no unprocessed neighbour after v, so forgetting it
only when covered enforces matching completeness. An upper vertex is
retained for a possible later right neighbour. Since an N edge is inserted
only when its new and old endpoints are both uncovered, degrees never
exceed one. Every N edge of any full matching appears as one of these left
or upper choices, so the transition loses no physical matching.

Induct on the scan prefix: the table at each joint state is the minimum
cost (1) among exactly its physical labelled prefixes, with every forgotten
vertex N-covered and every wholly processed M edge checked and charged.
The local actions establish both directions of this invariant. Initially
there is the empty prefix with cost zero. At the end require every remaining
frontier vertex covered; forgotten vertices were already checked. Thus
the final minimum is the full labelled matching optimum, and Section 2
turns it into the desired exact physical pair (a,f).

Backtracking stores predecessor states and the selected physical edge at
each introduction. It reconstructs the complete N, global labels and actual
edge sets. A final one-pass M+N decomposition verifies a, TH expense and
the disjoint partition of M into paid, bad-path and free-cycle resources.
Free cycles are normalized only after the GLOBAL minimum is selected.

## 5. Operation and storage bounds

**Joint-frontier theorem.** At s=min(h,w), the algorithm makes
O(|V|*8^s) bounded-arity state transitions and integer arithmetic operations.
It uses O(8^s) active table entries, and O(|V|*8^s) predecessor entries for
the delivered full-witness reconstruction. Input and output also use O(|V|).

There are at most eight possibilities per live slot and at most four
colours times three actions per state. Packed three-bit slots implement
each update without scanning the s slots. The scan stage determines which
initial slots are empty, so no ninth state is needed. Each actual edge and
selected vertex has one owner for its cost, and no component scan is hidden
inside a transition. Final decomposition is linear.

This is a state-transition/arithmetic bound. A packed mask has O(s) bits;
finite cost bit lengths are O(log(1+U|T|+W)). Python big-integer operations,
hashing and stored state keys have their corresponding bit costs. The
claim is not constant machine-word cost for arbitrary s or arbitrary weights.
If an explicit resource limit is reached the implementation raises an
exception, never returns a truncated approximate optimum.

## 6. Geometric consequences and precise limits

The earlier 4-by-w closed-chain selection has no complete covering in its
specified two-column cells, but unrestricted N attains (a,f)=(0,0).
With unit actual-edge weights, its relocated selection has cell-confined
covering cost exactly w/2, whereas unrestricted N attains (0,0) for every
nonnegative weighting. The existing two-batch explicit
N proves the upper bounds for every width; nonnegativity proves the fee
lower bounds. The new algorithm recovers these exact unrestricted optima
without receiving those two-batch witnesses.

The 2-by-2n half-area double-edge chain has one bridgeless cell block of
rank n-1. The global-feedback and bridge-block algorithms would enumerate
3^(n-1) label assignments to n-1 feedback edges, but this joint transfer has frontier height two
and at most 64 states, uniformly in n. Its explicit all-vertical witness
proves (a,f)=(0,0) for all n; the implementation tests up to n=256. This
shows exactly how a joint separator handles the prior rank obstacle.

The method also quantifies genuine residuals instead of requiring complete
coverage: on a 2-by-3 board with M empty and all four corner vertices
selected, T is feasible but |T|=4, |H|=2. Hence a>=1, and a full N with
one TT and two TH components attains (a,f)=(1,0). Complete coverage is
impossible for a numerical endpoint-count reason, not a local lifting error.

For general N, let b count HH paths, t count TH paths, and J=|M|+|T|.
The invariant

    |T|=2a+t, |H|=2b+t, J=|V|/2-(b-a)

still holds. Optimizing a can repair a physical certificate but does not
change the numerical b-a invariant. No universal 5/6 coefficient improvement
or universal full-coverage statement follows from an exact algorithm.

The next substantive geometric task is to characterize the difficult joint
boundary relations, or prove a signed resource inequality over them that
improves the numerical target. Independence of scalar reserves or bounded
bridge-block rank may not be assumed. No new Lean formalization is claimed;
the previous word-grammar Lean file does not formalize this global theorem.

## 7. Reproducible validation

The checker enumerates full unrestricted physical N independently of the
four-label DP, scores each by its actual component pair (a,f), and compares
the minimum. Exhaustive controls include every selected subset of Q, so
positive residuals are tested as well as feasible original selections;
transposed and one-dimensional boards are included. Additional random
boards, huge positive fees, odd-area rejection and explicit state-limit
failure exercise the implementation. Every arbitrary-size conclusion above
has its own proof; finite enumeration supports the code rather than
replacing the frontier induction or four-label exactness argument.
