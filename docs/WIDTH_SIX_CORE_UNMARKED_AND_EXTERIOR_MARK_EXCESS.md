# Unmarked width-six core and the actual exterior mark excess

22 October 2026. Authors: Haobo Ma and Wenlin Zhang.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.

## Model and resulting improvement

Retain the canonical nested core O of `LOCALIZED_COMPLETE_EXTERIOR_BUDGET.md`
with W=6 and ALL consecutive bar-row gaps equal to10. Thus a_i=a_0+10i,
all a_i are even, a_0>=2, and outer depths D,F are even and at least a_g+4.
The old sources are the outer charge-minus-one A and g+1 positive B_i=U(6,4,4).
Let K be any finite COMPLETE extension in the immutable full-even-U/standard-
rotor model. No extra width, orientation, leg equality, source-count or
connectivity restriction is imposed on the EXTERIOR originals.

Use the accepted complete width-six chamber classification: each of the g
chambers contains exactly one spanning D6 or U6 and no other added original.
Let d be the number of D chambers. Use the established source-to-grid ledger
for admitted feasible representative pairs:

    sigma=mn/2-|T_sel|-|M| >= Phi(K)-G.                 (1)

G counts ACTUAL marked canonical sides, at most two per positive source. This
ledger remains an explicit dependency, not a decomposition of arbitrary grid
representatives. The localized theorem gives

    Phi(K)>=4g+2d+2+P_out.                              (2)

The previous sufficient condition P_out<=4d paid two sides for EVERY positive
source. Here the internal marked demand is computed geometrically instead.

**Unmarked-core theorem.** All B_i for i<g and all chamber positive U6 sources
have zero actual marked sides. Only the last old B_g and positive exterior
sources may contribute to G.

Let h be the actual marked-side count of B_g, and let N_0,N_1,N_2 count
positive EXTERIOR originals with zero, one or two actual marked sides. Then

    G=h+N_1+2N_2,    0<=h<=2,
    P_out=N_0+N_1+N_2.

Combining (1),(2) gives the explicit bound

    sigma>=4g+2d+2-h+N_0-N_2.                           (3)

In particular,

    N_2<=N_0+4g+2d                                    (4)

is sufficient for coefficient one:

    |T_sel|+|M|<=mn/2.

More precisely, retain the nonnegative slack from (3) whenever its right side
is nonnegative. This is a condition on excess ACTUAL marked demand, not on the
number of exterior sources. Arbitrarily many singly marked exterior positives
cost no net unit in (3); an unmarked exterior positive pays one doubly marked
one. Exterior negative and zero sources are unrestricted and were already
included jointly in (2). The same Phi pays all marks once.

The cruder condition P_out<=4g+2d also suffices. Since d<=g, it contains the
previous P_out<=4d condition. Criterion (4) is stronger still and places no
upper bound on P_out. This is a refinement inside the stated canonical class,
not an unrestricted grid theorem. Coefficient-one results for unmarked fusions
and equal-leg width-six positive sources were already established elsewhere;
they are not claimed new here.

## The exact canonical mark witnesses

For a canonical positive U(6,a,b), the left canonical selected point, anchor
and remote guard are

    x=(3,2),  v=(3,1),  z=(1,3).

Its three protector endpoints are (2,1),(4,1),(1,3). Each originally has
occupied degree three. The only original blank neighbour of each is,
respectively,

    (2,2), (4,2), (2,3).                                (5)

A side is marked exactly when one of its protector endpoints reaches final
occupied degree four, equivalently when at least one point in (5) becomes
occupied. In a COMPLETE fusion such a newly occupied point must be a final
endpoint. If it remained a foreign support, it would have its own original
endpoint anchor, distinct from the protector endpoint, as a second occupied
neighbour. This contradicts retained support degree one. Optional selections
with no endpoint neighbour cannot create a mark either.

Reflecting column c to7-c gives the right-side missing neighbours

    (2,5), (4,5), (2,4).                                (6)

These are exactly the established two-side dual-guard mark tests, not a new
definition of G. Both independent leg depths can equal4; every displayed
protector is still an endpoint. Translations and tiling-preserving symmetries
transport the tests with their original source.

## Why all earlier B sources are unmarked

Translate (5),(6) by row a_i. Every possible mark witness for B_i lies at row
a_i+2 or a_i+4, and column2,3,4 or5. If i<g, these sites lie strictly inside
its next sealed chamber

    C_i=[a_i+2,a_i+9] x [1,6].

The old outer A has endpoints only on columns0,7 at these rows. Earlier B
sources end no later than a_i-6; B_i itself ends at a_i+4 and, at these witness
sites, has only columns1,6. Later B sources start no earlier than a_i+10.
Thus no OLD source endpoint is at any witness.

By sealed-chamber localization, no added source from another chamber or the
exterior has an endpoint there. The one chamber source is either

    D_i: U(6,4,4), chart(r,c)=(a_i+5+r,c),
    U_i: U(6,4,4), chart(r,c)=(a_i+9-r,c).

Both have all their endpoints at rows a_i+5 through a_i+9. Neither reaches
a_i+2 or a_i+4. Completeness excludes retained-support witnesses as above.
Therefore none of the six possible witnesses is occupied, proving both
canonical sides of B_i unmarked. No assertion about B_g is needed.

## Why every positive chamber U is unmarked

Only the U_i orientation is positive; D_i has charge1-6=-5. Transport (5),(6)
by U_i's chart. Its six potential missing neighbours now have rows a_i+7 or
a_i+5 and columns2,3,4 or5. All lie inside C_i.

The old A again has only side-wall endpoints there. B_i ends at a_i+4 and
B_(i+1) begins at a_i+10; all other B sources are farther away. The complete
chamber classification leaves no other new source inside C_i, and localization
excludes all exterior/other-chamber endpoints. The witnesses are originally
blank in U_i itself. They therefore cannot be final endpoints, nor can they
be retained supports. Both U_i sides are unmarked.

This exhausts all positive core/chamber sources. The old outer A is negative;
the D_i are negative. Hence G is exactly h+N_1+2N_2, proving (3),(4).

## Single-use compensation and comparison with earlier bounds

Substitution into Phi-G performs the allocation once. The exterior contribution
P_out in (2) supplies one unit per exterior positive original, and its own mark
count charges zero, one or two units. Its net is exactly +1,0,-1 for the three
classes. The internal budget4g+2d+2 is reduced only by the actual h at B_g.
No term is reused to pay both an internal mark and an exterior mark: the
internal marks just proved absent have no debit to pay.

The singleton-flow theorem already credits activated positive tips. In this
core all old B terminals and all positive chamber U terminals are activated,
giving the known core contribution2(2g+1-d). The accepted chamber/exterior
budget retains an additional4d. Thus the present mark-excess estimate should
be read as applying the exact unmarked-core geometry to that regional budget,
not as inventing a second activated-tip reserve. When d=0, the corresponding
core reserve is also available from the earlier singleton-flow argument.

It is useful to retain h in (3). For ordinary long-wall capped cores h=0,
so two additional units remain. This last statement concerns the explicit cap
family; h=0 is not assumed for arbitrary exterior extensions.

## Remaining scope

The mark-count refinement does not settle every exterior inventory: doubly
marked positives may exceed the available unmarked/core budget. Such excess
would need stronger exterior compensation or a further geometry theorem.
The sharp exterior constant between2 and5, wider-chamber classification,
arbitrary representative decomposition and rectangular-grid triple equality
remain open. The submitted11October focused manuscript is unchanged.

## Validation and independent review

The direct checker reconstructs canonical sides from immutable source geometry
and compares actual occupied-degree marks with the established paired-guard
implementation.40source-side reconstructions,640complete physical images and
150whole complete width-six families passed.143families meet the new sufficient
criterion, including73outside P_out<=4d and16outside the coarse G<=N test.
These controls have zero singly marked positive occurrences; arbitrary N_1 is
covered by the written argument, not a nonvacuous physical control. They do not
show singly marked sources impossible, or that all prior singleton criteria fail.

The scoped Lean source formal/SubQuorum/WidthSixMarkExcess.lean passed13theorems
and17individual declaration axiom audits on the user-selected local Mac, without
warnings, errors, sorry or native evaluation. Coordinate witness exclusions and
conditional arithmetic are formalized; geometric normalization, completeness,
classification/localization and the source-to-grid adapter remain written.

Independent same-conversation audit e748b41d-22d2-4c00-aa1a-c66f4bf3e2b3
ended with infrastructure_retry_exhausted/cdp_disconnected@typing,
without a mathematical verdict. Its failed receipt is preserved. After that
terminal state, fresh independent audit7fd0661d-40ab-4c29-893f-0e32f98fb5f8 was
dispatched in conv_4d5ca236606b7743 on original stream59944. Prior audit96e3f47c
ACCEPT covers the arbitrary cut conservation and previous coarse marked-slack
corollary only. See output/width-six-mark-excess-validation.json for commands
and original handles.

Later supplemental controls exercise N_1 nonvacuously:20complete whole-core
families contain90singly marked exterior positive occurrences. They use the
complete eight-source full-bar-exit block, whose positive mark counts are2,1,0
and whose Phi is22. Place k copies far apart from the capped g=0 core and from
one another. The fixed block's occupied bounding box is[-1,19]x[-3,21],
so translations by(200+80i,200),0<=i<k, suffice for the g=0 capped core.
Original endpoint/support sets are separated, so completeness,
Phi and marks add exactly. This realizes every k>=1 with

    P_out=1+3k, N_0=1+k, N_1=k, N_2=k, h=0,
    Phi=5+22k, G=3k, certified slack>=3.

The copies introduce no new marks on the fixed core or each other. Thus the
unbounded N_1 statement has actual complete realizations; the original640/150
controls still have no such occurrence. These supplemental fixtures were added
after the current independent review input and are not covered by its scope.
