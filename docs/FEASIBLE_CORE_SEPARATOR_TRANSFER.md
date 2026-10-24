# Exact compensation transfer across a feasible shared core

21 October 2026. The shared-source separator theorem extends to an arbitrary
complete feasible shared subfamily C. The overlap correction is its ACTUAL
reserve R(C), not its original negative mass S(C). Internal directed events,
mixed full tiles and already marked core sides must also be counted once.
This gives a structural reduction for the full unrestricted allocation
problem. It does not establish allocation or rectangular-grid equality.

## 1. Hypotheses and the binary theorem

Let F be any finite complete feasible mixed U/rotor source family, with its
fixed original endpoint/support/matching data and aligned physical tiles.
Partition its owners into disjoint A,C,B, with A and B nonempty. Assume:

1. The complete retained subfamily C is feasible, including every restored
   original support outside its own endpoint set.
2. No lattice edge joins an endpoint of an A-owner to an endpoint of a B-owner.

Put L=A union C and K=B union C. There is no restriction on dimensions,
phases, numbers of owners, source recurrence or the shape of C. In particular
C may have several sources and need not have a connected endpoint graph.
Then BOTH L and K are complete feasible, and

    R(F)=R(L)+R(K)-R(C).                              (1)

For every positive owner in C and each of its actual canonical sides, let
bL,bK,bC be its marking indicators in the three complete restrictions. Define

    D=sum over positive core sides of bL*bK*(1-bC).

This counts a side marked from both restrictions but not already marked
within the core. The general OR-indicator calculation gives

    mu(F)=mu(L)+mu(K)-mu(C)+D.                        (2)

The subsequent [canonical gate theorem](MARKED_SIDE_GATE_CONSUMPTION.md)
proves D=0 for every actual complete-source configuration under these
hypotheses. Thus the physical theorem sharpens to

    mu(F)=mu(L)+mu(K)-mu(C).                         (2a)

The OR calculation below is retained to identify precisely which possible
correction is eliminated. No assumption about a minimal counterexample is
needed for this elimination.

When C is one source, R(C)=max(0,-charge(C)), its original sides are
unmarked and mu(C)=N_C+R(C). Thus the previous single-source theorem is
the special case of(1)--(2). A multi-source core can have internal events
and mixed full tiles, so replacing R(C) by S(C) would generally be wrong.

## 2. Legal restrictions, including restored support/support conflicts

For each original owner i let Pi,Ti be its endpoints and supports and
Oi=Pi union Ti. Every retained support stays occupied, whether finally
selected or consumed. Original occupied sets therefore persist under retention.
Each original support x has its fixed endpoint anchor ai(x).

Take a selected point x in L, a retained producer i and a hypothetical second
occupied neighbor y different from ai(x). Full feasibility forces x to be
an endpoint of a removed B-owner j. If i were in A, the endpoint edge
ai(x)--x would contradict hypothesis2. Hence i is in C. Since x is not
an L-endpoint, it is not a C-endpoint either: x is selected in C.

Feasibility of C now implies y is NOT occupied in C. Choose a retained owner
k producing y's occupancy. It therefore lies in A. If y is an endpoint of
k, its edge to x in B is forbidden. Otherwise y is an original support of k,
with its own anchor ak(y). That anchor differs from x by endpoint ownership
uniqueness. In F, the two distinct occupied neighbors x,ak(y) force y to be
consumed into an endpoint of some owner ell.

If ell is in A, y--x is a forbidden A--B endpoint edge. If ell is in B,
ak(y)--y is a forbidden A--B endpoint edge. Thus ell is in C. But then
y is occupied in C, contradicting the feasibility observation above.

No selected x can have a second occupied neighbor. This proves feasibility
of L; the proof for K is symmetric. Original endpoint degrees stay at least
three because the retained original occupied sets persist, and disjoint
original endpoints preserve the unchanged matching. These are actual
complete-source restrictions, with no support omission or relaxed boundary.

The shared-core hypothesis supplies exactly the last contradiction. When
the core is one source it follows from intrinsic single-source feasibility.
For a general overlap one must check actual complete feasibility. In
particular an arbitrary union of desired boundary owners is not enough.
If C is the intersection of two known legal retained families, the exact
Horn intersection theorem supplies this hypothesis.

## 3. Event and full-tile inclusion and exclusion

Label each directed event by its ORIGINAL producer and actual source/target
vertices. Such an event joins endpoints of two original owners. By hypothesis2
it belongs to L or K; it cannot join their exclusive parts. An event belongs
to BOTH exactly when both of its endpoint owners lie in C, by unique endpoint
ownership. Therefore the actual event sets satisfy

    E(F)=E(L) union E(K), E(L) intersection E(K)=E(C). (3)

There is also a physical full-tile statement; it does not follow from event
counting alone. Every nonempty endpoint tile of the feasible complete core
has connected endpoint profile. The only disconnected nonempty square subset
is a diagonal pair. Both missing corners of such a pair have two endpoint
neighbors and cannot be selected. Each diagonal endpoint would then have at
most its two outside-tile occupied neighbors, contradicting occupied degree
at least three inherited from its complete original source.

In a full tile of F, the complement of the core endpoint profile is connected:
it is the whole square, or the complement of a connected nonempty square
subset, or empty. If that complement contained exclusive endpoints from
both A and B, its connectedness would force a forbidden A--B endpoint edge.
Consequently every full tile of F is already full in L or K. It is full in
both exactly when all four endpoints lie in C.

An original one-owner full tile cannot become mixed on passing to a larger
subfamily, since all four physical endpoints already have that owner. A mixed
full tile cannot become one-owner full after adding disjoint original
endpoints. Hence the same union/intersection identities hold for the actual
mixed full-tile sets:

    Fmix(F)=Fmix(L) union Fmix(K),
    Fmix(L) intersection Fmix(K)=Fmix(C).             (4)

Original negative mass is modular by source ownership:

    S(F)=S(L)+S(K)-S(C).

Apply ordinary finite inclusion and exclusion to(3)--(4) in the SAME reserve
definition R=S+2|Fmix|-|E| to obtain(1). This is one signed valuation:
shared core source mass, internal full-tile credits and internal directed
events are all subtracted with their original signs. No second reserve
pool is introduced.

## 4. Actual demand overlap

A positive owner in A loses none of its actual marked-side witnesses on
restriction to L. A foreign fourth occupied neighbor at one of its original
protectors must be an endpoint: an unconsumed foreign support would have
both that protector and its distinct original anchor as occupied neighbors.
Such an endpoint cannot be in B by hypothesis2. The same applies in B/K.

For a positive owner in C, every full-family witness lies in at least one
restriction containing that positive. Thus bF=max(bL,bK), while
bC<=min(bL,bK). For each such side,

    bF=bL+bK-bC-bL*bK*(1-bC).

Summing actual sides, rather than witnesses, gives

    G(F)=G(L)+G(K)-G(C)-D;
    N(F)=N(L)+N(K)-N(C).

Together with(1) these prove(2). A side marked inside C is shared already;
it is not an additional D occurrence. Several witnesses for one side still
give only one binary mark.

In the actual U catalogue, every marked side is equivalent to consumption
of its fixed original support by one unique endpoint owner. If it is marked
in both restrictions, that same consumer is in C. Hence D=0, as proved in
the canonical gate note, and the displayed demand count is an exact
valuation without a duplicate correction.

## 5. Several branches and a minimum-counterexample consequence

Let F=C union A1 union ... union Ar, r>=2, with disjoint exclusive owner
sets and no endpoint edge between different At. Assume C complete feasible.
The same argument proves every branch It=C union At feasible. Iterating the
binary theorem, or using the exact occurrence multiplicities, gives

    R(F)=sum_t R(It)-(r-1)R(C),
    mu(F)=sum_t mu(It)-(r-1)mu(C)+D_r.               (5)

For an actual positive core side unmarked inside C, let m be the number of
branches marking it. Its contribution to D_r is max(0,m-1). Sides already
marked inside C contribute zero. Exclusive positive sides retain their own
unique branch. Every original core event/full tile is counted r times in
the branch sum and corrected r-1 times, leaving it once.

Suppose a genuine negative-margin allocation counterexample exists and has
the smallest number of original sources. For the following inference assume
at least TWO exclusive sets A_t are nonempty, equivalently every counted
branch I_t=C union A_t is a proper subfamily of F. (The valuation identities
above do not require this extra condition and remain valid with empty parts.)
Every proper legal branch has
nonnegative margin. Since the margin is integral, equation(5) forces

    (r-1)mu(C)>=D_r+1.                              (6)

In particular it has NO nontrivial separator with a complete feasible
ZERO-margin shared core. For r=2 every eligible core must have
mu(C)>=D+1. This extends the zero-charge single-source articulation
exclusion to arbitrary feasible zero-margin overlaps. It is a necessary
condition on a hypothetical minimal counterexample, not a solution of the
full allocation problem. Separate nonnegative branch inequalities do not
pay a positive core margin automatically.

The canonical gate theorem also gives D_r=0 for every physical branch
decomposition: a marked side belongs precisely to the branches retaining
its one consumer. Equations (5)--(6) therefore simplify to
mu(F)=sum_t mu(It)-(r-1)mu(C) and (r-1)mu(C)>=1.

## 6. Nontrivial connected five-source overlap

Use the nine-source family J_k of the
[connected marked-hull obstruction](DEMAND_HULL_RESERVE_COMPARISON_OBSTRUCTION.md).
Take C={V3,V6,V7,V8,V9}, A={V1,V2,V4}, B={V5}. There is no A--B endpoint
edge. C is complete feasible and endpoint-connected. It has original negative
mass k+19, two mixed full tiles and six directed events, so

    S(C)=k+19, R(C)=k+17, N(C)=G(C)=0.

The actual values at k24 are

    R(L)=35, R(K)=30, R(C)=41, R(F)=24;
    mu(L)=34, mu(K)=30, mu(C)=41, D=0, mu(F)=23.

Thus35+30-41=24 and34+30-41=23. Subtracting shared original negative mass43
instead would give22 and21, respectively: that overlooks the shared core's
internal signed reserve correction. All four endpoint graphs are connected.

The following explicit support certificate verifies this core for all even
k>=6. Its remaining original V3 selections are

    (2,10),(1,1), (2,c) for c=2,4,6,8,
    (0,c) for c=3,5,7, and(-k-5,7).

The first nine have unique anchors(1,10),(1,2),(1,c),(1,c), respectively;
the last has anchor(-k-6,7). Its four other original supports are consumed
by V6,V7 exactly as listed in the preceding construction. The26 selections
of V6,V7,V8,V9 and their unique anchors are exactly its upper-source table.
Their normalized coordinates and these ten V3 points have no cross-neighbor
conflict for k>=6. Thus C has2k+108 endpoints, k+54 original matching edges
and36 selections; all mandatory supports and endpoint degrees are covered.
The contacts V3--V7,V7--V6,V7--V8,V8--V9 prove its connectivity.

The core's two V7/V8 mixed full tiles and six directed events are fixed;
lengthening V3 contributes only original source mass. For L to F, adding V5
contributes mass5, k/2+3 mixed full tiles, k+7 old-to-new and k/2+3 new-to-old
events, so R(F)-R(L)=1-k/2. These occurrence counts and the previously
proved single-source split give the exact general reserves
R(C)=k+17,R(L)=k/2+23,R(K)=k/2+18,R(F)=24.

Run `python3 develop/check_feasible_core_separator.py` for complete geometric
controls over feasible multi-source cores, all32 phase/isometry images per
eligible fixture, event AND full-tile unions/intersections, actual marks and
the exact reserve/margin correction. Small core subsets and component
partitions have the documented exhaustive ranges; larger ones are sampled.
The general proof is Sections2--5, not extrapolation from those controls.

`formal/SubQuorum/FeasibleCoreSeparator.lean` states three source-level
lemmas: legal restriction across a feasible shared core, exact event
intersection and event cover. Physical square-profile/full-tile valuation,
finite cardinality and actual-mark adapters remain written. Its compilation
and axiom status are recorded separately; no end-to-end Lean claim for
(1)--(6), unrestricted allocation or grid equality is made.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
