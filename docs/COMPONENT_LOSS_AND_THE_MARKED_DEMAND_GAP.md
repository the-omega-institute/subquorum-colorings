# Exact component loss and the remaining marked-demand gap

21 October 2026. For every legal complete mixed U/rotor extension I subset J,
all unions of connected groups of new endpoints are complete feasible. Reserve,
positive sources, actual marked sides and allocation margin are affine on this
Boolean family. This gives a simultaneous, one-use bound on ALL reserve-losing
groups. Applied to the canonical demand hull, it identifies the exact aggregate
loss inequality still needed for the FULL unrestricted allocation target.
Neither that target nor rectangular-grid triple equality is proved here.

## 1. Complete-source hypotheses and the component theorem

Use the original catalogue and complete-source feasibility in
[SOURCE_RETENTION_HORN_CLOSURE.md](SOURCE_RETENTION_HORN_CLOSURE.md), with every
allowed dimension, phase, isometry and arbitrary finite U/rotor mixtures.
All original endpoints are disjoint, original source matching is fixed, and
every original support outside the retained endpoint union is mandatory.
Both I and J are complete feasible retained families, I subset J. In particular,
the assumption on I includes supports restored when J's other owners are absent.
Throughout, N counts POSITIVE source occurrences; the total number of all
source owners is |J|. These are different counts.

The endpoint graph of EACH original U or rotor source is connected. For a U,
its two-wide bar and both attached stems form a connected graph. For a rotor,
the central four-cycle and four attached outer endpoints form a connected graph.
Consequently the connected components of the lattice graph on P(J) minus P(I)
partition the added OWNERS into nonempty sets B1,...,Bm. There is no endpoint
edge between different Bj. No connectedness of I or of the full graph is assumed.

For T subset {1,...,m}, set

    X(T)=I union (union over j in T of Bj),    Kj=I union Bj.

Every X(T) is complete feasible. For each Q in {R,N,G,mu},

    Q(X(T))=Q(I)+sum over j in T [Q(Kj)-Q(I)].             (1)

Proof. The cases T empty and T all are immediate. Otherwise split J into
I union A union B, where A and B are the selected and omitted component
groups. The complete core I is feasible and there is no A--B endpoint edge.
The [feasible-core theorem](FEASIBLE_CORE_SEPARATOR_TRANSFER.md), Section 2,
proves that BOTH restrictions are complete feasible, including restored
support/support conflicts. Thus every X(T) is legal, not merely Horn-closed
under a relaxation. Empty exclusive parts require no gluing theorem.

The same theorem gives exact reserve inclusion and exclusion across I.
Source count N is additive by original ownership. For actual marks, the
[canonical gate theorem](MARKED_SIDE_GATE_CONSUMPTION.md) identifies each
marked side with its unique gate consumer. Producer and consumer have adjacent
endpoints, so a new incidence cannot join different Bj; a side marked in two
restrictions containing its producer already has its consumer in their common
core. Hence the duplicate-new-core term is zero. This gives the exact G
valuation, and mu=N+R-G gives the margin valuation. Iterating over the chosen
components proves (1). These arguments do not assume demand preservation or
restrict the signs of newly added sources.

## 2. A simultaneous one-use bound on losing components

Write dj=R(Kj)-R(I), and define the integer aggregate loss

    L=sum_j max(0,-dj).

Let Tminus={j:dj<0}. Equation (1) gives

    min over T of R(X(T))=R(X(Tminus))=R(I)-L.             (2)

This is an actual complete feasible family attaining the minimum. It follows
by choosing every negative term and no positive term in the finite sum.
There is no assumption that arbitrary legal source restrictions are modular.
Only the particular component family constructed in Section 1 is used.

Activated positive singleton occurrences already present in I persist when
sources are added: their original support intersection with the endpoint union
can only grow. Thus A(X(Tminus))>=A(I). Apply the SAME exact reserve ledger
2R=A+U0+Z0+H to this one complete feasible family, obtaining

    2L <= 2R(I)-A(I),
    L <= R(I)-ceil(A(I)/2).                              (3)

The bound is simultaneous. Bounding each losing component individually by
R(I) and adding those bounds would spend the core repeatedly. Instead, all
losses in L occur TOGETHER in X(Tminus), and its surviving reserve is still
at least ceil(A(I)/2). Equation (3) spends at most the actual old reserve
outside that persistent floor. Original source mass, newly full-tile credit
and events are not added as further payment pools.

No pointwise local reserve linearization is required for (3), and no remote
zero-rotor pairing is silently omitted: the global exact ledger already includes
U0, Z0 and all weighted H terms with their actual ownership.

There is a genuine simultaneous-loss example on ONE shared owner. In the
complete nine-source family Jk of
[the marked-hull obstruction](DEMAND_HULL_RESERVE_COMPARISON_OBSTRUCTION.md),
take I={V3}. The new endpoint components are exactly
B1={V1,V2,V4} and B2={V5,V6,V7,V8,V9}. The displayed constructor contacts
connect each group and exclude edges between the groups. Both restrictions
are feasible by Section 1, and the established reserve formulas give

| Complete family | Actual reserve |
|---|---|
| I | k+7 |
| I union B1 | k/2+13 |
| I union B2 | k/2+18 |
| I union B1 union B2 | 24 |

For every even k>=24, BOTH groups lose reserve, respectively k/2-6 and
k/2-11. Their aggregate loss is k-17 and occurs against the same single
old source. It reduces k+7 to exactly24, in agreement with (2).
The formulas follow from the existing all-k constructor/insertion proof,
not extrapolation from the new controls. This disproves a possible rule
that each old owner can interact with at most one losing new component.
It is not a failure of (3) or of the allocation target: the full margin is23.

## 3. The exact target on the canonical demand hull

Now let I=H be the canonical least demand-preserving Horn hull of J. All
positive owners and unique consumers of all full-family marked sides are in H.
Every X(T) therefore has exactly N(J) positives and G(J) marked sides.
Write D=G(J)-N(J), so mu(H)=R(H)-D. Equation (1) sharpens to

    min_T mu(X(T))=mu(H)-L.                              (4)

Consequently ALL these actual subextensions satisfy allocation if and only if

    L <= mu(H)=R(H)-D.                                  (5)

The newly established loss bound (3) proves (5) whenever ceil(A(H)/2)>=D.
In the remaining case it leaves the precise demand gap

    D-ceil(A(H)/2) > 0.                                 (6)

This gap concerns reserve that still has to pay actual marked demand. The
bound L<=R(H)-ceil(A(H)/2) cannot be cited as if it proved L<=mu(H).
Our earlier connected marked-hull family still disproves reserve monotonicity;
it does not violate (5). No scalar assignment is a physical counterexample.

This reduction retains arbitrary source count and all configurations. If any
complete family fails allocation, its X(Tminus) also fails, because its reserve
is no larger while its demand is unchanged. Thus it suffices to exclude
negative-reserve component extensions of every canonical demand hull, provided
the case H=J is included. Source-count bounds and finite enumeration do not
settle (5).

## 4. Structure forced on a source-minimal counterexample

Suppose J were an allocation counterexample with the smallest source count,
and its canonical demand hull H were proper. Then mu(H)>=0. Every added
endpoint component has dj<0: if dj>=0, omitting Bj is a proper complete
feasible demand-preserving family with margin mu(J)-dj<0, a contradiction.
In particular every group loses an integer amount ellj=-dj>=1, and

    sum_j ellj >= mu(H)+1,
    sum over j in T of ellj <= mu(H) for every proper T. (7)

The second inequality follows from minimality applied to X(T). This is a
simultaneous competition for a single actual core reserve, not a supply of
mu(H) separately available to each branch. If H=J, this decomposition has
no added components and the core itself is the unresolved obstruction.

The [five-endpoint cap](FIVE_ENDPOINT_CAP_AND_POSITIVE_GATE_CONSUMERS.md)
restricts possible gate consumers inside H, and qplus<=A(H) reserves existing
activation units. It supplies no additional term to (3). The missing research
step is to show that the remaining demand D-ceil(A(H)/2) is protected from
aggregate losses, or exhibit a complete physical negative-margin configuration.

## 5. Validation scope

The checker exercises actual complete-source restrictions, every component
subunion in each tested extension, event/full-tile partitions, actual marks,
monotone activations and the minimizing subunion. It includes cases with
multiple strictly reserve-losing groups attached to one shared core.
Finite controls supplement the all-parameter proof above.

The Lean file formalizes arbitrary finite signed component lists, attainment
and minimality of their negative-part sum, the simultaneous activation-floor
loss bound, and the exact margin-budget equivalence. It does not formalize the
physical connected-component construction, complete-source feasibility or the
geometric ledger adapters. Those are the written arguments and inherited
theorems in Sections 1--2. There is no end-to-end Lean or full target claim.

Six scoped Lean4.33 declarations compile and pass axiom audit with only
propext and Quot.sound. Physical controls pass704phase/isometry images,
26272legal core extensions and383680component subunions, including192cases
with multiple strictly losing groups and13848demand-preserving extensions.
The written theorem received independent reviewb4910cb9 ACCEPT,11663characters,
actualgpt6/pro, original41916exit0. That review precedes the illustrative
two-loss Jk table added afterward; the latter derives from the existing
all-k construction and is also exercised by the physical controls.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
