# Frozen ear rematching: an old edge can change without losing compensation

25 October 2026. Haobo Ma and Wenlin Zhang. Isolated research branch.

Adding endpoints genuinely defeats the matching-retention conclusion of
[fixed-endpoint rigidity](MATCHING_INDEPENDENT_ACTIVE_MERGER_RESERVES.md).
On the actual active-merger board, four added endpoints and two added
selections permit a completely frozen rematching of an old edge. We prove a
general freezing-preserving ear insertion by lifting every old freezing
rank, rather than treating a solver result as proof. In this physical
family the operation consumes four original interval units, creates no new
alpha or beta, and retains all old private payments. It refutes old-matching
retention under endpoint additions, **not** the compensation inequality.

For q separated copies, choose any of the four good cap states and any
subset H of copies in which to insert the ear. On the explicit boards,

    k=V=2q, c=f,                    I_after=I_before-4|H|,

where f counts filled left caps, independently of H. For arbitrary further
feasible completely frozen monotone extensions retaining the modified
selections and matching, the old sources still eliminate exactly:

    V=2q+V_res,                    c=f+c_res.                 (1)

This is a class of actual rematchings followed by arbitrary retained-matching
completion, not a theorem for unrestricted repeated rematching. Universal
compensation and a numerical improvement of 5/6 remain open.

## 1. A general freezing-preserving matched-edge ear

Start with any feasible completely frozen pair (T,M), and an actual edge
uv. Add four fresh endpoints a,b,d,e and two fresh selected guards s,t.
Replace uv by

    ua, vb, de.

Assume the physical graph contains the following additional adjacency:

    ab, ad, be, ds, et.

All old adjacency and selections are retained. The new selected guards and
endpoints must make a feasible configuration; this is a real hypothesis,
not something freezing alone guarantees. The six fresh sites are distinct
and disjoint from the old occupied set. Extra adjacency can only help the
following freezing proof, although it must still satisfy feasibility.

**Lemma 1 (rank lifting).** The modified matching is completely frozen. If
rho is any old strict freezing certificate, a new one is

    rho'(x)=3 rho(x)                         for every old endpoint x,
    rho'(d)=3 rho(u)+1, rho'(b)=3 rho(u)+2,
    rho'(e)=3 rho(v)+1, rho'(a)=3 rho(v)+2.

**Proof.** The new matching covers precisely the old endpoints plus a,b,d,e,
once each, and has two more edges. New edges are physical by hypothesis.

For an old retained endpoint neighbor y, its new actual mate has rank at
most 3 rho(mate_old(y))+2. This is immediate for y=u or v from the displayed
formula, and for every other y its mate is unchanged. If the old witness
required rho(mate_old(y))<rho(x), then

    rho'(mate_new(y)) <= 3 rho(mate_old(y))+2 < 3 rho(x).

Old selected witnesses remain selected. Thus every old endpoint keeps its
two distinct old freezing witnesses at its scaled rank, including u,v.

The new endpoint d uses selected s and endpoint a, whose new mate u has
lower rank; e uses selected t and endpoint b, whose new mate v has lower
rank. The new endpoint b uses a and e: their mates are u and d, both lower
than b. The new endpoint a uses b and d: their mates are v and e, both
lower than a. These are distinct physical neighbors. The strict ranks
therefore certify complete freezing of all old and new endpoints. QED.

The factor three handles the delayed dependencies back into the old board.
It would be insufficient merely to freeze the old board first: old
witnesses touching u or v now depend on a or b, whose mates have changed.
The simultaneous rank construction resolves those dependencies explicitly.

**Lemma 2 (strand preservation under a PP detour).** Suppose the auxiliary
matching is A and is extended by ad,be, with all new sites PP. Then each old
component of M union A is retained, with the edge uv replaced by the
alternating path

    u --M-- a --A-- d --M-- e --A-- b --M-- v.

No new component or free end is created. In particular alpha, beta and
mixed counts and the identities of old terminal pairs are unchanged.

**Proof.** The displayed detour has four fresh internal vertices, each
incident to one M edge and one A edge. It connects exactly the old two
ends of uv. Every other edge and terminal is untouched. Replacing one edge
of a path or cycle by this detour preserves its type and endpoints. QED.

Neither lemma says an arbitrary original interval payment survives: the
new occupied sites can consume old gaps. That must be checked with original
interval identities, as below.

## 2. A concrete actual rematching of the active merger

In the saved 14 by 18 board take

    u=(7,14), v=(7,15),
    a=(8,14), b=(8,15), d=(9,14), e=(9,15),
    s=(10,14), t=(9,16).

Remove the old actual edge u--v and add u--a, v--b, d--e, together with
selected s,t. All old endpoints and selected vertices remain occupied.
The four new endpoints were blank. None is adjacent to an old selection;
each new selection sees exactly its designated new endpoint and no other
occupied vertex. The two guards are not adjacent. The configuration is
therefore feasible. Its complete freezing follows from Lemma 1, using the
old certified ranks. The actual
[fixture](../develop/fixtures/frozen_four_endpoint_ear_rematching.json)
stores the new matching, all strict witnesses and the extended right alpha.

Both new vertical band pairs ad,be are PP: rows8,9 form one standard band.
Hence Lemma 2 applies. The original right alpha still has terminal pair
(5,12),(3,15), now with a16-endpoint path instead of12. The left alpha and
all beta/mixed components are unchanged. This works in all four good left
cap states E,T,C,CB. Thus an old matching edge really changes in a feasible,
completely frozen monotone **occupied-set** extension.

This is outside the previous theorem's fixed-P hypotheses, so it is not a
counterexample to that theorem. It is a counterexample to extending its
matching-retention conclusion to arbitrary endpoint additions.

## 3. Why the shorter two-endpoint square flip fails here

Try adding only a=(8,14),b=(8,15), replacing uv by ua,vb. The site (8,16)
must stay blank: old selected (7,16) already sees old endpoint (7,15).
At (8,13), a new selection would see both old endpoint (8,12) and a, and
cannot be feasible; it is not an endpoint when only a,b are added.

Consequently a needs selected (9,14) as well as neighbor b to have two
retained nonmate neighbors. Likewise b needs selected (9,15) as well as a.
But (9,14),(9,15) are adjacent, and each already sees its endpoint above.
They cannot both be selected in a feasible configuration. Thus this
two-endpoint square flip cannot be completely frozen under any added
selections. This is an incompatibility of the two necessary supports;
granting each support separately as a mutually incompatible optimistic
upper bound would miss it.

Adding d,e as endpoints, together with the nonadjacent selected guards s,t,
resolves that obstruction by Lemma 1. This proves the failure of the shorter
flip and validity of the four-endpoint ear. It is not a general lower bound
on the number of endpoints required by every conceivable rematching.

## 4. Four original units are consumed; no new credit appears

The only available original interval identities that disappear are

    (band4,14,14), (band4,15,15), (band4,16,16), (band5,14,14).

There are no newly available intervals. The two new PP columns occupy the
first two units. Selected (9,16) changes the third from BB to BT; selected
(10,14) changes the fourth to TB. None of these local changes joins
remaining BB sites through TT, and all other band columns are unchanged.
The standard boundary marks are unchanged too. Direct coordinate inspection
therefore proves exactly four lost units, rather than a numerical
difference inferred from an optimizer.

| Left cap | I before | I after | Alpha | Beta | V | c |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| E | 56 | 52 | 2 | 2 | 2 | 0 |
| T | 55 | 51 | 2 | 2 | 2 | 0 |
| C | 55 | 51 | 2 | 2 | 2 | 0 |
| CB | 53 | 49 | 2 | 3 | 2 | 1 |

Thus I+b-k decreases by4. The objective |T|+|M| increases by4: two new
selections and two net new matching edges. New endpoints are not independent
surplus credits. The new bottom actual edge de is internal to the same
alpha's alternating detour, **not a newly available whole beta**.

The surviving payments are the left J_L=(band2,5,5), or its exclusive
empty-body beta in CB, and the right J_R=(band2,13,13). Neither is one of
the four consumed units. Both boundaries of J_R still belong to the same
right alpha, by Lemma 2. The left payment and its whole-support exclusion
are untouched. Hence the complete-pool optimum remains V2 and cost0 or1.

## 5. All-q and arbitrary subsequent retained-matching completions

Take q14-row translated copies with standard fixed packet boundaries and
optional initial even blank right padding. On any subset H perform the
ear insertion. The modified actual matching, old selections and new ear
guards are now retained. Allow arbitrary additional selections and
disjoint matching edges, subject to feasibility and complete freezing;
these may couple surrounding components and introduce residual alphas.

**Theorem 3 (persistent elimination after actual rematching).** Let f be
the number of filled left guarded caps in the final configuration. For
ordinary and full BP-aware compensation, equation(1) holds. Every outside
attainable paid-source set stays attainable while the old2q sources are
paid simultaneously, with exactly f links for their private routes.

**Proof.** Every old left alpha and every modified right alpha persists:
all its actual edges, internal PP pairs and selected terminal partners
are retained. The guarded left cap is unchanged, so its six-state
classification, four frozen states, private interval/exclusive beta and
filled-cap empty whole support remain valid. At the right, the old
selections still force blanks (4,13),(5,14); the old matched endpoints
(5,12),(6,13) still exclude occupation of (5,13). The BB13/BT14 gap thus
persists with both boundaries on the modified right alpha. Its singleton
J_R remains private. The detour is far from this gap and cannot introduce
a second owner into it. The left alpha's only potentially usable old
gaps remain its cap and the marked first-column boundary gaps; its exact
cost argument is unchanged.

Choose J_R for each right alpha, and J_L or the exclusive whole beta for
each left alpha. Distinct copies and gaps use different original resource
identities. The old private-source rerouting proof now applies directly
to the **modified** strands. Reroute each paid old source onto its private
unit, add any unpaid old source via its free private unit, and delete these
paths. No outside used resource is taken, and no route's link cost rises.
Conversely extend any residual packing by all old private payments. Each
filled left cap requires at least one actual link and has a private route
of exactly one. These two directions prove(1), including minimum cost.
The complete exterior BP gates, mixed owners, beta bodies/private sinks
and original interval units remain in the residual network. QED.

In the explicit uncoupled boards before further extension, the only alphas
are the old2q, so V=2q,c=f. The per-ear four-unit loss sums exactly to4|H|;
it is not asserted for arbitrary counterfactual before/after surgeries in
an unrelated exterior board. Elimination itself always has ledger

    k_res=k-2q, I_res=I-(2q-f), b_res=b-f,
    I_res+b_res-k_res=I+b-k.

No consumed interval or paid beta is counted again as an outside reserve.

## 6. Checks, formalization and the next question

The solver-free command is

    python3 develop/check_frozen_ear_rematching.py --output output/frozen-ear-rematching-validation.json

The checker verifies the saved actual fixture and witnesses; lifts strict
ranks in all four cap states; checks the exact four lost original interval
identities; and checks source/terminal-pair preservation. It validates
1,107 frozen elimination models,184 independent primitive packs, all584
eight-state choices in up to3copies,315 frozen single additions among673
feasible ones,192 multi-addition prefixes, and12 positive residual cases.
The four support choices of the failed two-endpoint square flip are also
checked. These are checks of the general proofs, not their replacement.

[FrozenEarRematching.lean](../formal/SubQuorum/FrozenEarRematching.lean)
proves the arbitrary-size strict rank lift, old-witness preservation, full
inductive freezing, endpoint closure, matching involution and resource
ledger. Seven audited declarations pass local Lean4.33.0, using only
standard propext/Classical.choice/Quot.sound, without sorry or native
evaluation. The physical embedding, selection feasibility, PP strand
adapter, exact original-interval loss and private-resource flow projection
are written proofs checked by Python, not claimed as end-to-end Lean
geometry. There is no new external review in this round.

The optional
[Z3 discovery script](../develop/search_monotone_endpoint_rematching.py)
can search for endpoint-adding rematchings; the final fixture was reduced
to the two necessary selected guards and verified independently. No UNSAT
or finite endpoint budget is used as a general impossibility theorem.

The remaining problem is unrestricted additions and rematching that change
the ownership of a reserve, rather than merely detouring the same alpha.
The right singleton's blank-site lock alone is insufficient to prove
private ownership when its two boundaries can acquire different owners.
New searches should target that separation and measure the resulting joint
capacity. Failure of matching retention by itself is now settled and does
not establish failure of compensation. The submitted11October version,
public main, PR3, shared CI and correspondence were preserved.

Follow-up: [actual reserve boundary splitting](RESERVE_BOUNDARY_SPLIT_AND_JOINT_COMPENSATION.md)
now realizes different owners on J_R's preserved gap and proves the exact
all-reservation joint compensation/link cost, including an overlap-correct
all-q repair formula. Unrestricted original pools remain fully payable.
