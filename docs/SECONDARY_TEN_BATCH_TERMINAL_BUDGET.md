# A terminal budget for batches of distinct-owner residual repairs

21 October 2026. The [depth-eight exclusion](SECONDARY_TEN_DEPTH_EIGHT_COMPLETE_EXCLUSION.md)
removes the exceptional large contact debit from actual upper consumers.
This permits a batch nonreuse theorem under explicit owner-packing
hypotheses. An unbounded partial-inventory construction shows why the
exterior contact term in that theorem cannot simply be deleted.

## 1. The routes and the packing hypotheses

Use the fixed original-source model and the two prescribed eight-original
residuals A of the [unconditional compensation theorem](SECONDARY_TEN_UNCONDITIONAL_RESIDUAL_COMPENSATION.md).
Allow arbitrary isometries that preserve the fixed partition into 2x2
tiles, including translations by even vectors and appropriately shifted
reflections. Every transformation acts on endpoints, ORIGINAL supports
and matching edges together. All owner sets below refer to actual original
occurrences, rather than endpoint components or independent copies of a
reserve. Write b_i=Phi(Q_i,D_i,W_i).

Take a finite collection of distinct-owner routes in one complete feasible
family G. For each index i use one of the following choices:

| Route | Base block B_i | Selected U owner U_i | Claimed terminal x_i | Cost c_i |
|---|---|---|---|---:|
| East U, north frame | A_i | actual owner of t_i | t_i | 1 |
| East U, south frame | A_i | actual owner of t_i | t_i | 2 |
| East rotor R_N | A_i plus the actual R_N | actual owner of e_i | e_i | 1 |
| East rotor R_S | A_i plus the actual R_S | actual owner of e_i | e_i | 2 |

These are the normalized frame labels relative to each package's own
tile-preserving chart. A reflection of the whole package does not change
its cost. The source charge of every selected U is 1-h_U, h_U>=6 even.

Assume explicitly:

1. The original-owner sets B_i are pairwise disjoint.
2. Every selected U owner lies outside the union of the B_i.
3. All retained blocks and selected consumers are actual members of G.

Different indices may select the SAME U owner. There is no assumption of
spatial separation or absence of endpoint contacts between different
blocks. Hypotheses1 and2 are genuine packing restrictions: this note does
not prove that every global instance admits such a selection. The theorem
covers the distinct-owner routes, not the remaining common-owner routes.

Let C be the SET of distinct selected U owners, d_U the number of routes
assigned to U, and

    H=(union_i B_i) union C,
    r_U=(h_U-1)-sum_{i:U_i=U} c_i.

## 2. Physical terminal injection

**Lemma.** Under the packing hypotheses, distinct routes assigned to the
same U use distinct physical leg terminals. In particular d_U<=2 and

    r_U >= h_U-1-2d_U >= h_U-5 >=1.              (1)

**Proof.** At a U leg terminal x, the unique own endpoint neighbor determines
an inward unit vector v. The point x-v is a fixed physical endpoint, the
opposite anchor of that terminal. For an east-U route in its normalized
chart, v=east and x-v=(a+1,w+13), an endpoint of the retained E owner.
For a rotor route, v=north and x-v=(a+1,w+14), an endpoint of the retained
rotor R. These assertions are preserved by all permitted isometries.

If two routes use the same physical U terminal, its unique own neighbor
fixes the same v and hence the same opposite anchor. Unique original
endpoint ownership forces the two anchor owners to be equal. But the
anchor of each route belongs to its base B_i, contradicting disjointness
of the bases for distinct indices. This also excludes a mixed east-U /
rotor collision; a physical endpoint cannot have two original owners.

An actual U has exactly two leg terminals. Thus at most two routes can
claim it. Every route costs at most2, while its original negative mass
h_U-1 is at least5. Charging that mass ONCE to the actual owner gives(1).
No support is paid separately and no per-route copy of h_U-1 is used.

## 3. The exact batch ledger, including exterior contacts

Let F(B) and E(B) be the actual mixed full-tile and source-labelled
directed-event sets of an original inventory B. An event (owner,p,q)
excludes q when q belongs to that owner's unchanged ORIGINAL support set.
Use the same ledger Phi=N+S+2|F|-|E| throughout.

For each i define its locally claimed NEW sets

    F_i=F(B_i plus U_i) minus F(B_i),
    E_i=E(B_i plus U_i) minus E(B_i).

Regard the events as globally labelled by their actual owner. The accepted
exact receipts give, with epsilon_i=0 or1 for north/south east-U routes,
and sigma_i=0 or1 for north/south rotor routes,

    Phi(B_i)=b_i-1,        2|F_i|-|E_i|=-epsilon_i    (east U),
    Phi(B_i)=b_i-1-sigma_i, 2|F_i|-|E_i|=0           (rotor).

The second equality uses the complete-family depth-eight exclusion. Thus
in both cases the base deficit minus the local signed contact term is
exactly the cost c_i in the table.

All these internal and claimed sets are disjoint, as follows. Each event
has two uniquely determined endpoint owners. Internal base events have
both in one B_i; a claimed event has one owner U_i outside all bases and
the other in B_i. Different i therefore cannot claim the same directed
event, even when their U owner repeats. Internal event sets also cannot
overlap.

Every tile in F_i has exactly TWO U_i endpoints and TWO B_i endpoints.
This follows from the full local receipts: the possible east-U/W neutral
tiles and the upper-U/R_N neutral tile all have this 2+2 pattern; the
other contacts are not newly full. Two different bases cannot claim the
same full tile. Indeed its two endpoints belonging to B_i would be foreign
to both B_j and U_j, by the packing hypotheses. It could not then be full
inside B_j plus U_j. Internal base full tiles are also disjoint from one
another and from every F_i, since all four of their endpoints already
belong to their own base. This proof counts physical full tiles once.

Define the unclaimed remainder by SET differences in the global H:

    F_extra=F(H) minus (union_i F(B_i) union union_i F_i),
    E_extra=E(H) minus (union_i E(B_i) union union_i E_i).

These include inter-base contacts, other base/consumer contacts,
consumer/consumer contacts and any new full tile involving more than the
locally claimed pair. They are not assumed to have a favorable sign.

**Batch theorem.** There is an exact identity and the resulting bound

    Phi(H)=sum_i b_i + sum_{U in C} r_U
                         +2|F_extra|-|E_extra|,          (2)
    Phi(H)>=sum_i b_i + sum_{U in C}(h_U-1-2d_U)
                         +2|F_extra|-|E_extra|
           >=sum_i b_i + |C|+2|F_extra|-|E_extra|.       (3)

**Proof.** Original positive-owner counts and negative mass are additive
over disjoint owner sets. The distinct U owners each contribute h_U-1
to S and zero to N. Partition the global F and E sets into the disjoint
internal, local and extra sets just proved. Substitution in Phi gives

    Phi(H)=sum_i Phi(B_i)+sum_{U in C}(h_U-1)
                +sum_i(2|F_i|-|E_i|)+2|F_extra|-|E_extra|.

Replace each base deficit minus its signed local term by c_i, and group
the costs by their actual U owner. This is(2); apply(1) to obtain(3).

In particular the remaining sufficient exterior condition is

    |E_extra|-2|F_extra| <= sum_{U in C} r_U.          (4)

It is also necessary for Phi(H)>=sum_i b_i, by(2). This is an exact
reduction, not a proof of(4). The mass in(4) is the REMAINING per-owner
budget after all its terminal claims have been paid.

## 4. An unbounded obstruction to dropping the remainder

There is an explicit shared-consumer partial inventory with all base owner
sets disjoint for which the exterior term equals -(w+8). It shows that
neither disjoint bases nor a correct two-terminal budget makes that term
nonnegative.

For every even w>=12 take the FIRST residual with k=w+8,z=4 at odd a.
Let A_1=A and choose the north-frame east U

    U=U(16,4,4), (r,c)->(a+2-c,w+18-r).

Reflect the whole A by the tile-preserving map

    rho(row,column)=(2a-13-row,column),
    A_2=rho(A_1).

The full original U is invariant under rho, including its matching and
supports, because this reflection exchanges its equal intrinsic legs.
The two routes claim its two different terminals, t_1=(a+1,w+14) and
t_2=(a-14,w+14), and each has cost1. Its mass is15, counted once, so
r_U=13. All17 original endpoint sets in A_1,A_2,U are disjoint.

Here are uniform geometric reasons for the latter assertion. In the first
residual z=4, A_1 occupies rows from a-6 through a+10, while A_2 occupies
rows a-23 through a-7. The U is disjoint from A_1 by the accepted east-U
criterion, and rho-invariance makes it disjoint from A_2. Between the
bases, only their V bars reach adjacent rows: V_1's row-zero bar is at
a-6, and V_2's reflected row-zero bar is at a-7. Their other endpoint
rows lie on the opposite sides. Every other source of A_1 has row at
least a-4, and its reflection lies at most a-9, excluding further tiles.

The k columns B=4 through w+11 form k/2 aligned pairs. Each such tile
has two V_1 and two V_2 endpoints. Neither direction of either vertical
adjacency targets an original support: each target has intrinsic row -1
in the other V. Consequently its new receipt is one mixed full tile and
FOUR directed events, net -2. There are no U/base events or locally
claimed full tiles in these north-frame routes. Thus exactly

    |F_extra|=k/2, |E_extra|=2k,
    2|F_extra|-|E_extra|=-k=-(w+8).

Both baselines are w+9: the original Q,D,W charges are -1,-(w+3),-5,
and their inventory has no mixed full tile or surviving directed event.
Applying the
same exact accounting, without any completeness assumption, gives

    Phi(A_1 plus A_2 plus U)-2(w+9)=13-(w+8)=5-w<0,
    Phi(A_1 plus A_2 plus U)=w+23>0.

This refutes the ENDPOINT-DISJOINT partial-inventory rule that a deduplicated
terminal budget alone guarantees the sum of the baselines. It does not
refute the batch theorem with its explicit remainder, condition(4) in the
complete model, the global allocation target or the 5/6 bound.

The displayed inventory is INCOMPLETE. For example the two original
bar-corner supports (a-6,3) and (a-7,3) are both unconsumed, adjacent
to each other and each adjacent to its own V bar endpoint in column4.
Each therefore has at least two occupied neighbors, rather than the
required one. The subsequent
[opposing-batch exclusion](SECONDARY_TEN_OPPOSING_BATCH_COMPLETE_EXCLUSION.md)
proves that its ENTIRE prefix has no complete extension: a further actual
consumer forced at e has no possible U/rotor realization. Thus the negative
receipt remains valid, but this family cannot violate condition(4) inside
an actual complete extension. Other exterior contacts remain open.

## 5. What this closes and what remains

The physical terminal argument closes duplicate use of the same U charge
for packed distinct-owner routes. The partition proves that no locally
claimed event or full-tile credit is duplicated. The exact exterior
obstruction identifies a remaining loss that grows with occupied-band
length while the shared-consumer budget stays constant.

Universal base packing, consumers that belong to another base, common-owner
routes and condition(4) in actual complete closures remain open. The new
value beyond the earlier general extension identities is the route-specific
terminal injection, the associated per-owner capacity and the 2+2 local
tile disjointness; an exact signed extension identity alone was already
available. Lean and finite-control scopes are recorded with the sources
and validation receipts, rather than asserting end-to-end formalization.

The [control receipt](../output/secondary-ten-batch-terminal-controls.json)
records32 independent isometry batches, one mixed four-route batch,
120 shared-consumer batches,240 shared-consumer isometry batches and four
unbounded-debit controls. Additional opposing-prefix checks cover eight
forced sites,864 upper-U collisions and3588 bounded full-source east roles;
the reflected family has40 small-breadth collisions and32 exact separated
ledgers. All controls PASS. These are checks of the general proofs.

The [Lean execution receipt](../output/secondary-ten-batch-terminal-lean-validation.json)
records27 clean declarations with individual ordinary axiom checks, including
the subsequent opposing-prefix exclusion and reflected-pair classification.
Original review75530 covers the batch theorem, partial exterior obstruction
and initial16 declarations; the later complete exclusion and breadth
classification are OUTSIDE that input and require their own review.

Review update: the initial batch theorem and the subsequent complete-prefix
exclusion/reflected classification now each have a separate ACCEPT written
review; see the corresponding output receipts. Neither audit certifies
execution or arbitrary global allocation. The
[internal-consumer chain note](SECONDARY_TEN_INTERNAL_CONSUMER_CHAINS.md)
now gives an all-length obstruction to dropping the outside-bases
hypothesis, even for acyclic dependencies with zero exterior remainder.
