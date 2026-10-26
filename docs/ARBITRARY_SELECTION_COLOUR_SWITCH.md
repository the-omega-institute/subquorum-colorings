# Arbitrary selections under retained endpoints: sharp half-area by switching colours

27 October 2026. Wenlin Zhang and Haobo Ma.

**Theorem.** For every integer m>=2 let c=6m+9 and R={0,...,5}×{0,...,c}, with nearest-neighbour grid edges. Let M be an actual matching, P its endpoints, T disjoint from P, O=T∪P and H=R\O. Each selected site has at most one neighbour in O. Retain only the endpoints

    P0={(r,k): r∈{1,2}, k∈{1}∪{5+6j,6+6j,7+6j:0≤j≤m}}
         ∪{(r,k):r∈{3,4},5≤k≤c} ⊆ P.

Then

    J=|T|+|M| ≤ 18m+30 = |R|/2.

The bound is attained by the established completely frozen family (T0,M0), whose [explicit construction and full strict-rank proof](FROZEN_HALF_AREA_ATTAINERS.md) also give the freezing definition, and by T=∅ with any board perfect matching. Thus it is the exact maximum even if complete freezing is additionally required. The proof needs no freezing. Selections may now occur anywhere, with either colour; new endpoints and actual rematching are unrestricted. This removes the Bstar restriction from the preceding [white/terminal theorem](UNPROTECTED_WHITE_PAIR_AND_PREFIX_BUDGET.md). It does not classify all equality configurations and does not solve the universal grid 5/6 problem. The submitted 11 October manuscript is unchanged.

## 1. Why a colour switch repairs the failed local budget

Write t_v,h_v,p_v for the selection, genuine-hole and endpoint indicators, so t_v+h_v+p_v=1. Black means even coordinate sum, white means odd. Abbreviate a local site (r,k) by rk. Define

    B13={00,02,13,20,22,24,31,33,40,42,44,51,53},
    W13={01,03,10,12,14,23,30,32,34,41,43,50,52},
    B15=B13∪{04,06}, W15=W13∪{05,07},
    δB=Σ_{B15}t−Σ_{W15}h, δW=Σ_{W13}t−Σ_{B13}h.

We prove two fixed local lemmas:

    δB ≤ h54,                                      (L1)
    δB≥1 ⇒ δW≤0.                                  (L2)

The disjoint maps outside these pockets give

    |T_black|−|H_white| ≤ δB,                       (B)
    |T_white|−|H_black| ≤ δW+t54.                  (W)

Every actual edge has one endpoint of each colour. Therefore

    D:=J−|R|/2=|T_black|−|H_white|
                =|T_white|−|H_black|.

If D>0, integrality and (B) imply δB≥1. By (L1), h54=1; disjointness of selection and holes gives t54=0. By (L2) and (W), D≤δW+t54≤0, a contradiction.

The white hole 54 is used in (L1) to determine its state. We never add (L1) to a black payment ledger that also spends 54. After the switch, the actual payment targets are black holes. This is a joint counting argument without double use of the contested boundary hole.

## 2. Four actual-mate capacities

For any finite set Q of white sites, actual mates inject P∩Q into P∩N(Q), where N is the complete grid neighbourhood. Hence

    Σ_Q p ≤ Σ_{N(Q)} p.                            (M)

The following consequences hold with arbitrary white selections.

**Top capacity.** Take Q={01,21}. Its neighbourhood is {00,02,11,20,22,31}. Retention gives p11=p21=1. Substituting p=1−t−h in (M) yields

    t00+t02+t20+t22+t31
      ≤4+h01+t01−h00−h02−h20−h22−h31.

If t01=1, the different retained neighbour 11 forces h00=h02=1. Thus t01−h00−h02≤0 in either case. Dropping the other nonpositive terms gives

    t00+t02+t20+t22+t31 ≤4+h01.                    (C1)

**Bottom capacity.** Take Q={50,52}, N(Q)={40,42,51,53}. Substitution in (M) gives the desired right side 2+h50+h52, plus t50+t52 minus the holes in N(Q). Selected 50 has a hole in {40,51}; selected 52 has a hole in {42,53}. These pairs are disjoint. The extra terms are therefore nonpositive, proving

    t40+t42+t51+t53 ≤2+h50+h52.                    (C2)

**Corner capacity.** If 50 is empty the following is immediate. If selected it has at most one occupied neighbour among 40,51. If an endpoint its actual mate is one of 40,51 and cannot be selected. Hence

    t40+t51 ≤1+h50.                               (C3)

**Eleven-selector capacity.** Put

    Q={01,10,12,21,30,32,41,50,52},
    K={00,02,13,20,22,31,33,40,42,51,53}.

Then N(Q)=K∪{11}, |Q|=9 and |N(Q)|=12. We first prove an injection T∩Q→H∩N(Q). Site 21 is retained, so not selected. Selected 01,10,12 may respectively use the distinct forced holes 02,00,13, because each has the different retained neighbour 11. Reserve these targets.

For the five remaining possible white selections, all available black neighbours avoid the reserved targets:

| Selected white | Complete black neighbourhood | Holes required by degree |
| --- | --- | ---: |
| 30 | {20,31,40} | 2 |
| 32 | {22,31,33,42} | 3 |
| 41 | {31,40,42,51} | 3 |
| 50 | {40,51} | 1 |
| 52 | {42,51,53} | 2 |

Their genuine-hole neighbourhoods satisfy Hall for every subfamily of selected whites. One or two sources have enough holes, since only 50 may have just one. A three-source subfamily contains 32 or 41, either requiring three holes, or is {30,50,52}; in that case 30 and 52 require two holes each in disjoint neighbourhoods. A four-source subfamily either contains both 32,41, whose potential neighbourhoods meet only in {31,42}, giving at least 3+3−2=4 holes, or contains the disjoint pair 30,52. If all five had at most four available holes, 30 and 52 would account for all four. Neither 22 nor 33 could be a hole, so 32 would have only 31,42 available, contradicting its requirement of three. This proves Hall and the claimed injection.

The actual-mate injection P∩Q→P∩N(Q) has image disjoint from these genuine holes. Thus

    |Q|−|H∩Q|=|T∩Q|+|P∩Q|
        ≤|H∩N(Q)|+|P∩N(Q)|=|N(Q)|−|T∩N(Q)|.

Using retained 11,21 gives

    Σ_{b∈K}t_b ≤3+h01+h10+h12+h30+h32+h41+h50+h52. (C4)

This is the additional joint mate capacity needed beyond the earlier pocket. Merely balancing the total number of black and white endpoints does not imply it.

## 3. Exact nonnegative identities for the local lemmas

All coefficients are given in the companion [affine identities](COLOUR_SWITCH_AFFINE_IDENTITIES.md) and [machine-readable certificate](../output/colour-switch-affine-certificates.json). They are exact affine polynomial identities, not numerical optimization bounds assumed as premises.

For (L1) put Δ=δB−h54. For a black s∈B15 let ε_s=1 precisely at {06,20,22,24,31,44}, and zero elsewhere. These six sites have a retained neighbour outside the listed white sites. For any listed neighbour subset Q with |Q|+ε_s≥2,

    Σ_{w∈Q}h_w−(|Q|+ε_s−1)t_s ≥0.

Indeed a selected s has at most one occupied neighbour, including the retained neighbour if ε_s=1. Use these slacks, (C1)–(C4), and indicator bounds. The explicit identities give:

| Case | Rational bound for Δ |
| --- | ---: |
| t44=1 | 7/9 |
| t44=t33=h41=0 | 1/2 |
| t44=t33=0, h41=1 | 3/4 |
| t44=0, t33=1, t24=0 | 8/9 |
| t44=0, t33=t24=1, h41=0 | 2/3 |
| t44=0, t33=t24=h41=1 | 11/12 |

The six cases exhaust the Boolean states of these indicators. Each bound is strictly below one, so the integer Δ≤0. This proves (L1).

For (L2) assume δB≥1. Besides indicator bounds use the following nonnegative slacks: 1−t_v−h_v; Σ_{u∈Q}h_u−(|Q|−1)t_v for any subset Q of neighbours of v; h_u−t_v if v has a different retained neighbour; 2−Σ_square t for the four corners of a unit square; and δB−1. The square slack is valid since three selected corners would include a selected corner with two occupied selected neighbours. Retained sites have t=h=0 and are substituted accordingly.

The seven explicit identities give:

| Case | Rational bound for δW |
| --- | ---: |
| t32=t41=h00=0 | 37/42 |
| t32=t41=0, h00=1 | 25/27 |
| t32=0, t41=1, h23=0 | 1/2 |
| t32=0, t41=h23=1 | 4/5 |
| t32=1, h13=h03=0 | 0 |
| t32=1, h13=0, h03=1 | 1/2 |
| t32=h13=1 | 3/5 |

These exhaustive cases again give the integer δW≤0. This proves (L2). Every named degree subset, forced neighbour and retained substitution is determined by the displayed geometry. Exact re-expansion verifies each identity coefficient by coefficient; a local Lean kernel checks the same nonnegative sums and the exhaustive case splits.

## 4. Uniform disjoint budgets outside the pockets

A selected vertex is outside P0 and has at most one P0 neighbour. The explicit P0 row table therefore gives these necessary candidate lists (not a sufficiency assertion):

| Row | Black selections may occur at columns | White selections may occur at columns |
| --- | --- | --- |
| 0 | Every even column | Every odd column |
| 1 | 3,9,15,...,c | 0,2,4 and 8+6j,10+6j within R |
| 2 | 0,2,4 | 3,9,15,...,c |
| 3 | 1,3 | 0,2,4 |
| 4 | 0,2,4 | 1,3 |
| 5 | Every odd column | Every even column |

For example, row 2 outside columns 0,...,4 and the gap centres 9+6j is either retained or has both a retained horizontal neighbour and a retained neighbour in row 3. Row 1 outside its displayed candidates is retained; row 0 is unrestricted by this necessary test. The bottom row has the retained neighbour in row 4 at every column >=5. The remaining finitely many left columns give exactly the displayed entries by direct adjacency.

**Black budget.** For a=4+6j, 0≤j≤m, let

    A=(0,a), B=(0,a+2), C=(0,a+4), D=(1,a+5),
    u=(0,a+1), v=(1,a), w=(0,a+3),
    x=(0,a+5), y=(1,a+4), z=(2,a+5).

For j≥1, selected A,B inject into holes among {u,v,w}: selected B forces u=w=1 because (1,a+2) is retained; assign B to w and any selected A to u. If B is absent, selected A has at least one hole among u,v. For every j, selected C,D inject into holes among {x,y,z}. Selected D forces at least two holes in that triple; selected C forces at least one of x,y (at C the other top neighbour can account for at most one of its two required holes). If C is selected assign it a hole in {x,y}, then give D a different hole. If C is absent simply assign D any hole. At j=m the terminal D has exactly x,y,z as neighbours, so the same argument holds.

The first A,B pair is already in B15, with its three targets in W15, and is omitted from these maps. Different remaining top groups have disjoint target sets outside W15. Each selected bottom black (5,k), odd k≥5, forces its distinct hole (5,k−1), since (4,k) is retained. Bottom targets are disjoint from the top targets and W15. The candidate list shows that these maps account for every black selection outside B15, proving (B).

**White budget.** For the same a put

    U=(0,a+1), W=(0,a+3), X=(0,a+5),
    Y=(1,a+4), V=(1,a+6), Z=(2,a+5),

with black targets

    A=(0,a), B=(0,a+2), C=(0,a+4),
    D=(1,a+5), E=(2,a+4), F=(2,a+6).

At j=m omit the nonexistent V,F. Retention and degree imply: selected U forces A empty; selected W forces B empty; selected Y forces C,D,E empty; selected V forces D,F empty; selected Z forces D,E,F empty, omitting F at the terminal.

Assign U→A and W→B. If D is empty, assign any remaining selections X→D, Y→C, V→F, Z→E. If D is occupied, none of Y,V,Z is selected; any selected X forces C empty, so assign X→C. These targets are all distinct, both within and between groups, and avoid B13.

Each selected bottom white (5,k), even 6≤k≤c−1, forces its distinct black hole (5,k−1), again using its retained neighbour in row 4. These targets avoid the top targets and B13. The candidate list leaves only 54 outside W13 and these sources. Therefore the maps give (W), completing the theorem.

## 5. Literal sharp obstruction to a sealed prefix

For every m≥2 take

    T={00,02,04,13,20,22,24,31,33,40,42,44,50,52},
    M={11--21} ∪ { (r,k)--(r+1,k):r∈{0,2,4},5≤k≤c }.

All edges are disjoint grid edges and P0⊆P. Sites 00,02,13,33 have no occupied neighbour. Sites 04,20,22,31,24,40,42,44,50,52 respectively have the single occupied neighbour 05,21,21,21,25,50,52,45,40,42. Thus the configuration is feasible. Its counts are |T|=14 and |M|=1+3(c−4)=18m+16, so J=18m+30.

But |T∩B15|=12 and |H∩W15|=11: δB=1, h54=1 and δW=0. It refutes the independently sealed-prefix inequality and attains the global target. For completeness, an endpoint x freezes when two different neighbour sites are selected or have their actual mate already frozen; its own mate cannot support its first event. Exactly endpoint 21 freezes, using selected neighbours 20,22,31. Its actual mate is 11, whose other neighbours 01,10,12 are all holes, so 11 never freezes. Every right-side endpoint initially has at most one selected neighbour. The sole newly supported site 11 is adjacent only to those three holes and the already frozen21, so no further event follows. This is not a frozen counterexample. The earlier nine-selected prefix obstruction is another sharp instance. Neither refutes the theorem. The disputed boundary site is resolved by switching colours rather than billed twice.

## 6. Verification, provenance and remaining questions

The proof consists of the actual-mate injections, the five-source Hall argument, the displayed exact affine identities, the all-length coordinate maps and the final integer contradiction. Optimizers served only to discover certificates; the permanent checker uses Python's standard library and exact integer arithmetic, never an optimizer.

The [coordinate checker](../develop/check_colour_switch_budget.py) verifies the identities, capacities, all candidate lists, distinct physical payment targets and actual mate images, the inherited frozen families and two explicit obstruction families through m=100, plus arbitrary-selection/rematching controls. See its [result](../output/colour-switch-budget.json) for exact coverage. The [Lean source](../formal/SubQuorum/ColourSwitchBudget.lean) checks thirteen affine cases, both exhaustive local budgets, the five-white numerical hole inequality, disjoint-injection transport and global switching/objective arithmetic. Its [audit](../output/colour-switch-formal.json) records the local execution, process/memory preflights and axiom closures. The complete grid coordinate adapter and Hall/mate geometry remain written proofs with executable controls; no end-to-end Lean grid theorem or CI claim is made.

Proof assistance came from broker task 2c09bc42-24b6-446f-b006-13d2048cc7b1, observed gpt_6/pro. Its original stream exactly equals the terminal response. The returned route suggested (L1),(L2) and the four capacities; the claimed PDF coefficients were not available through the response, so all thirteen affine certificates here were rebuilt separately and checked exactly, with several stronger rational bounds. Assistance is not independent acceptance. The separate earlier successor-note review c6f17905 failed at cdp_disconnected@typing with no mathematical response; it supplies no verdict.

Independent attachment-based review f4f2f745-c9eb-49ba-aafc-dae9ba06f92d is COMPLETED/ACCEPT, observed gpt_6/pro; its original stream exactly equals the terminal reply. It checks the complete retained-P0 counting proof, all thirteen coefficients, both all-length maps and ordinary sharpness without relying on computational claims. It does not independently verify the previously established fully frozen family; the precise construction/rank reference above supplies that ancillary dependency. The first full-text review22a2040c failed at cdp_disconnected@typing with no mathematical reply. [Verdict and exact scope](../output/colour-switch-independent-review.json).

The retained-P0 arbitrary-selection half-area problem is settled by the written proof and the checks above. The subsequent [six-row boundary invariant](SIX_ROW_BOUNDARY_INVARIANT.md) removes retained anchors through a fixed local integer certificate and arbitrary-length induction; a purely structural anchor-free proof remains open. Other remaining directions include the full equality footprint/matching classification and geometric compensation for unrelated bands. The universal 5/6 improvement remains open. No manuscript revision or email is made by this research publication.
