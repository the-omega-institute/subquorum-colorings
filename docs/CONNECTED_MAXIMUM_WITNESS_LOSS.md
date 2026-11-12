# Connected obstruction to retaining the maximum witness count

The square constructions retain every helper and b witness vertices. That
witness requirement cannot be imposed on a general auxiliary cycle: a connected
minimum-degree-two, maximum-degree-three family has an arbitrarily large
additive loss under it. The target all-helper8b/3 bound remains valid on this
family; the counterexample identifies a failed construction rule.

For every integer r>=1, the physical partial template H_r below satisfies

    |V(H_r)|=20r, b=4r,
    beta_I(H_r)=11r+floor(r/2),
    max{|D|:I subset D, D dissociation, |D intersect X|=b}=10r.

The restriction therefore loses exactly r+floor(r/2) vertices, with
two-connectedness and both degree bounds retained for every r. Its restricted
value10r is belowceil(8b/3). A proof of the general target must allow the
witness count to change on this family.

## Explicit template and proof

Take8r indices in cyclic order. P pairs(0,1),(2,3),..., Q pairs consecutive
odd/even indices cyclically, so A=P union Q=C_(8r). In each consecutive
eight-index interval, B contains one C4 on even offsets0,2,4,6 and another
on odd offsets1,3,5,7. Witness index v has physical colourfloor(v/2)mod2;
P joins equal colours, Q and B join opposite colours. Subdivide the P edges
by helpers, attach the owner copy through the witness-owner matching, and
add the stated owner edges. This gives a connected bipartite20r-vertex graph.
Helpers have degree2 and every witness and owner has degree3. The graph is
two-connected: deleting a helper/witness leaves a connected backbone path,
with at least three attachments per owner cycle; deleting an owner leaves
its owner cycle as a path attached to the intact backbone.

For any independent witness set T in A, let k_i^0,k_i^1 be the even/odd
witness counts in interval i. A C4 with k forbidden vertices has exact
dissociation optimummin(2,4-k). Maximizing owners for this fixed T therefore
gives the exact total objective

    8r+sum_i g_i, where g_i=min(k_i^0,2)+min(k_i^1,2).

Every interval induces P8 before the cyclic boundary edges. Thus g_i<=4.
Equality forces four independent witnesses, two of each parity; both boundary
vertices must be selected. Adjacent intervals cannot both attain4, including
the cyclic closing edge. At mostfloor(r/2) intervals attain4 and the others
contribute at most3. This proves the all-helper upper bound.

Choosefloor(r/2) nonadjacent intervals cyclically (none whenr=1). On these,
select witness offsets{0,2,5,7} and owner offsets{1,3,4,6}; on every other
interval select witness offsets{1,3,6} and owner offsets{0,2,5,7}. Select
all helpers. These choices respect all boundary edges and attain the bound.

The only maximum independent sets of A=C_(8r) are its two bipartition
classes. Either maximum witness choice forbids all owners of one C4 per
interval, leaving exactly2r selectable owners, and hence a total10r.

The [complete manuscript proof](../manuscript/maximum-witness-loss-proof.tex)
treatsr=1and2 explicitly in the boundary argument. Every parameter value is
covered by the written proof, not by extrapolation from the checks.

## Construction and validation

[Construction](../develop/maximum_witness_loss.py) returns raw P/Q/B data and
actual owner/witness selections. [Fixed inputs and selections forr=1and2](../develop/fixtures/maximum-witness-loss.json)
are also supplied. Run:

    python3 -B scripts/check_maximum_witness_loss.py

The checker independently enumerates all256 local witness subsets and all256
forbidden/selected C4 pairs. It retains all55 local independent-subset states,
including both boundary bits, in a full-vector cyclic dynamic program. This
checks exact objective values for67 listed sizes, throughr=256. Forr=1and2,
the original exponential all-helper optimizer gives exact optima11and23;
all65,792 auxiliary subsets are separately checked for the maximum-witness
restriction. There are134 direct maximum-phase controls. Actual physical
certificates, articulation-free connectivity, bipartition and degree bounds are checked through
5,120vertices. All720single-vertex deletions forr=1through8 are also checked
by independent searches. Eight small cases also pass the preceding owner-matching
construction. The final independent audit and actual execution scope are
recorded in output/maximum-witness-loss-review.json.

This family has no auxiliary C4, and the preceding Brooks theorem already
proves8b/3 for it. Its role is to show why the maximum witness count from the
square proof cannot be retained in a general extension. No unrestricted
beta_2 or SF_2 optimum is asserted. General mixed auxiliary8b/3, the sharp
unrestricted subcubic coefficient, physical multiple-Hall routing, universal
unit5/6 improvement and arbitrary-width rectangular triple equality remain
open. October's submitted manuscript is unchanged.
