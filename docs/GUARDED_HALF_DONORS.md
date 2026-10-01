# Guarded same-direction donors and single-use allocation

1 October 2026. Research continuation of [mixed neutral donors](MIXED_NEUTRAL_DONORS.md), separate from the journal manuscript. The feasibility convention and exact tile ledger are those of [cross-component compensation](CROSS_COMPONENT_COMPENSATION.md). A selected vertex T has at most one occupied neighbor; occupied means T or a matching endpoint P. B denotes blank. For a deficient tile,

    2 rho(Q) = 2 t(Q) + p(Q) + s(Q) - 4.

Saturated tiles have charge zero. Each residual edge crossing a region boundary contributes its endpoint half to each region, so all tile charges add exactly to q=|T|+|M|-mn/2.

## 1. A sharp half-unit lemma

**Lemma 1 (guarded R,R donor).** Let Q be a tile of a feasible even-by-even rectangle. Its left and right neighbors are both saturated `TP/BT` tiles, and their P vertices are matched upward. Assume additionally:

1. the vertex immediately above Q's upper-left corner exists and is occupied;
2. the tile immediately above Q is not a saturated tile containing P.

Then Q is deficient and rho(Q)<=-1/2. No condition is imposed on the lower exterior, residual path shape, or the capacities of other tiles. Reflection gives the L,L version, with both caps `PT/TB` and the occupied vertex above Q's upper-right corner. Rotations give the other directions.

**Proof.** The left cap's lower T already sees its P, forcing Q's lower-left corner B. The right cap's upper-left T already sees its P, forcing Q's upper-right corner B. Q's upper-left corner sees the left cap P and the occupied vertex above it, so it cannot be T. The only possible selected corner is lower-right: t<=1 and Q is deficient.

Only the upper-left and lower-right corners can be P. An upper-left P cannot match sideways because the left cap P is already matched; it cannot match internally because its two internal neighbors are B. Its only possible mate is above, where hypothesis 2 excludes a saturated attachment. A lower-right P likewise cannot match internally or sideways, and can attach to a saturated tile only downward. Thus s<=1. If t=1, lower-right is T, so s=0 and p<=1, giving 2rho<=2+1-4=-1. If t=0, p<=2 and s<=1, giving 2rho<=2+1-4=-1. QED.

This uses the full boundary-aware tile charge, including residual endpoints; no additional port slack is available to count separately.

**Sharpness.** Use coordinates Q={0,1}x{0,1}. Put `TP/BT` caps at tile columns -1 and +1, with cap P edges (0,-1)--(-1,-1) and (0,3)--(-1,3). Set Q=`PB/BT`, match (0,0) to (-1,0), and make the rest of the tile above Q blank. All unspecified vertices are blank. The configuration is feasible, the upper guard is P, and t=1,p=1,s=0 gives rho=-1/2. Translation by (4,2) embeds it in a 6x6 rectangle. All matching edges and selected coordinates are archived by the checker.

In a neutral pressure band every saturated tile contains no P. Therefore hypothesis 2 is automatic when the tile above Q belongs to that band. Hypothesis 1 is not automatic. For a width-one R,R gap, the occupied-guard middle states in the existing neutral table are `PB/PT` and `PP/PP`; `TB/BT` and `PP/BT` have a blank guard. Reflection gives `BP/TP` and `PP/PP` for L,L. These are necessary label possibilities, not assertions of global realizability.

## 2. Two explicit obstacles to removing the guards

**Obstacle A: a same-direction gap can have charge zero.** Keep the same caps, but put Q=`TB/BT`. Above the three tiles (left cap, Q, right cap), put the neutral states

    TB/BP, TB/BT, TB/BP.

The two outer lower-right P vertices are exactly the cap mates (-1,-1) and (-1,3). Put a full P row at row -3, columns -2 through 3, matched in adjacent pairs. Every upper T in the parent triple has that P pressure as its single occupied neighbor. Q's upper-left T sees only the left cap P; its lower-right T has no occupied neighbor. The tile above Q is saturated without P, but the vertex above Q's upper-left corner is blank. Thus hypothesis 2 and a neutral P-pressure parent triple do not imply hypothesis 1. Q is saturated and rho(Q)=0.

Translation by (4,2) gives a full feasible 6x6 witness: |T|=10, |M|=5, q=-3. This refutes the unguarded same-direction half-unit rule, not the target q<=0. The triple is a local neutral pressure segment; it is not claimed to be an entire capped pressure band.

**Obstacle B: occupied pressure alone is insufficient.** Set Q=`PB/BP`. Its upper-left P is matched to a saturated upper tile `TB/PT`, and its lower-right P is matched to a saturated lower tile `TP/BT`. Keep the original side caps and their upward matching. The upper-left guard is occupied, but the upper tile contains P. Now t=0,p=2,s=2 and rho(Q)=0. Translation by (2,2) gives a feasible 6x6 witness: |T|=8, |M|=4, q=-6. Hence the second guard also cannot be discarded in arbitrary ambient configurations.

## 3. A donor tile has at most one geometric certificate

A full certificate is the earlier capped R,L pattern, budget 1. A half certificate is a guarded R,R or L,L pattern of Lemma 1, budget 1/2. Include all four rotations; reflections interchange R,R and L,L and preserve this list.

**Lemma 2 (local uniqueness).** In one feasible configuration a fixed tile cannot satisfy two distinct certificates from this twelve-pattern list.

**Proof.** First consider certificates whose cap axis is the same. Normalize one entrance to be from above. The cap label pairs are respectively (A,B), (A,A), (B,B), where A=`TP/BT` and B=`PT/TB`. They are distinct. Reversing the entrance rotates each cap through 180 degrees and swaps sides: its labels are drawn from `TB/PT` and `BT/TP`, neither of which equals A or B. Thus two distinct certificates on the same axis require conflicting labels on a shared cap.

For perpendicular axes, if either certificate is a half certificate, the other certificate requires a saturated cap containing P in that half certificate's parent position. This contradicts its second guard. It remains to compare two perpendicular full certificates. Normalize the first to the caps in the preceding section. Its cap edges use the diagonal exterior endpoints (-1,-1) and (-1,2). A clockwise perpendicular full certificate requires edge (-1,1)--(-1,2); a counterclockwise one requires (-1,0)--(-1,-1). Each reuses an already matched endpoint with a different mate. This contradicts the matching property. Rotational invariance covers all cases. QED.

The cap patterns alone do NOT establish uniqueness: four rotated R,R/L,L perpendicular pairs have compatible cap patterns. Their parent guards reject them. Nor does geometric uniqueness identify which distant source owns a donor. Two sources requesting the identical certificate still share one budget.

## 4. Cross-component accounting without duplicate budgets

**Proposition 3.** Let K pairwise tile-disjoint filled source corridors each have charge +1. Let F full donors and H half donors be distinct certified tiles outside the sources. Let N be any tile-disjoint neutral regions, disjoint from these tiles and sources, and let W be all remaining deficient tiles. Then, regardless of residual component membership,

    q <= K - F - H/2 + rho(W).

**Proof.** Sources contribute K, N contributes zero, each full donor contributes at most -1, and each half donor at most -1/2. Sum the exact ledger over this partition. Lemma 2 prevents alternative orientations from producing additional budgets for the same tile; identical claims must also be deduplicated by tile coordinate. QED.

For explicit assignment, make a bipartite incidence graph from sources to admissible certified donors. Give a full donor capacity 1 and a half donor capacity 1/2. A fractional assignment pays one unit to every source without reusing any donor budget if and only if

    sum(budget(d) for d in neighbors(X)) >= |X|

for every subset X of sources. This is the capacitated Hall condition: source-to-donor arcs have unlimited capacity, each source has incoming capacity 1 and each donor outgoing capacity equal to its budget. The finite max-flow/min-cut theorem gives the equivalence; multiplying all capacities by two makes them integral. Testing only individual sources is insufficient: two sources adjacent only to the same full donor each pass that test, but the two-source subset fails.

Under this Hall condition and rho(W)<=0, Proposition 3 gives q<=0, hence coefficient 1 in place of 5/6 on the stated covered class. This is a conditional improvement, not a new bound for arbitrary grids. The existence of enough donors, Hall for every source subset, and nonpositive remainder still need a general geometric argument. The incidence graph must come from justified reachability or an explicitly stated admissibility rule; local uniqueness alone does not supply it.

## 5. The earlier 6x20 obstruction now has certified outside donors

In the 6x20 witness of `MIXED_NEUTRAL_DONORS.md`, the parent exit word is R,R,L,L at tile columns 1,3,6,8. The width-two central R,L child, columns 4 and 5 below it, is saturated and contributes zero. The outside tiles at columns 2 and 7 are now guarded half donors: above them are respectively `PB/PT` and `BP/TP`, with occupied entry guards and deficient parent tiles. Their actual labels are `BB/BT` and `BB/TB`, each with charge -1, stronger than the certified -1/2.

The disjoint partition has charges +1 (source), 0 (parent), 0 (central child), -1 and -1 (outside donors), and 0 (remainder). Thus q=-1 exactly. Two distinct half budgets suffice to pay the source even though its sole R,L child gives nothing. The source's admissible set can explicitly be these two neighboring same-direction-gap tiles; there is only one source, so Hall holds here. This is a genuine extension beyond the previous R,L-child forest, but it does not establish the necessary allocation for overlapping roots or bent paths.

## 6. The unguarded same-direction classification

The adjacent-exit table is also restrictive. For an unguarded R,R middle tile, the necessary local possibilities are:

    left R   middle   right R
    PP/BP    PP/BT    PP/BP or TB/BP
    TB/BP    PP/BT    PP/BP or TB/BP
    TB/BP    TB/BT    PP/BP or TB/BP

These are local label/compatibility conditions only; they do not assert global matching realizability. Reflection gives the corresponding L,L table.

The one-step successor relation adds a useful distinction. After `PP/BT`, the next neutral tile is forced to be either another `PP/BT` or the next R-exit `PP/BP`; an L-exit is impossible. Thus `PP/BT` is a pure delay state. After `TB/BT`, the next state may continue through `TB/BT`, enter `PP/BT`, use `PP/PP`, or turn through `BT/PB`/`PP/PB`; it may also produce an R-exit. This is a finite necessary-state statement, so the eventual matching and boundary realization still need proof.

The complete necessary predecessor set for the first L exit is `BP/TP`, `BT/TB`, `PP/PP`, `PP/TB`, or `TB/BT`. Thus a first turn after an unguarded chain either comes directly from a `TB/BT`/`BT/TB` zero-charge state, or passes through one of the pressure-neutral `PP/PP`/`PP/TB` states. This isolates the only five local interfaces that a general mixed-interval lemma must address.

## 7. Why the local automaton is not enough

Assign two budget units to a known full R,L donor (a width-one interval or an interval whose parent states are all `PP/PP`), one unit to a guarded R,R or L,L donor, and zero to every unresolved mixed R,L interval. The necessary-state automaton admits words with one mixed R,L interval and zero known budget. The shortest examples are

    PP/BP, BT/TB, BP/TP, PP/PB
    PP/BT, PP/BP, BT/TB, BP/TP, PP/PB

The first has width four and the second width five; both satisfy the relaxed boundary and adjacent-state compatibility checks. This is not a counterexample to the grid theorem: the automaton omits global matching realizability. It proves instead that a local-state proof cannot establish the needed aggregate budget without adding a matching or residual-routing invariant.

The local neutral-state table gives a complete obstruction at a width-one R,R gap. If the entry guard above Q's upper-left corner is blank, the only compatible middle labels are `PP/BT` and `TB/BT`. The first is deficient with (t=1,p=2,s=0), hence (2\rho=0); the second is saturated and also has charge zero. Reflection gives `PP/TB` and `BT/TB` for L,L. Thus a width-one unguarded same-direction gap supplies no local negative charge at all. A finite compatibility enumeration through width 7 shows the same two states are the only unguarded one-tile middle states; wider intervals may contain these states mixed with neutral `PP/PP`, `PB/PT` or `BP/TP` tiles. This finite result is a discovery check, not a global realizability claim.

Consequently the next geometric statement cannot be another local donor lemma of the same form. It must show that an unguarded `PP/BT` or `TB/BT` gap forces either a later guarded donor, a negative aggregate over the whole same-direction interval, or a transfer across a bend. The existing zero-charge counterexample shows that any such statement must use neighboring exits or residual routing, rather than Q alone.

The two shortest zero-budget words above are not merely formal automaton paths. Complete finite matchings realize them in 6x12 and 6x14 rectangles, respectively. For the displayed selected sets, the archived endpoint/occupancy covers certify that the listed completions are maximum, and both give q=-3 with three units of negative residual excess and no positive component. A third 6x12 completion with the same width-four parent word has a fixed-`T` maximum with q=-2 and only two negative components. Thus these are genuine mixed-interval configurations, but still satisfy the target inequality. They show precisely what a future aggregate lemma must recover: the negative remainder that is invisible in the local donor budget. These are fixed-coordinate certificates, not a universal two- or three-unit bound over variable selected sets.

## 8. Verification and next proof obligation

Run `python3 develop/check_guarded_half_donors.py --output output/guarded-half-donors-controls.json`. It checks the relaxed local bound, all twelve certificate cap patterns and guard exclusions, direct full-grid sharpness/obstacle witnesses under eight symmetries, guarded recognition of the 6x20 outside donors, and the exact disjoint ledger. It records full coordinates, component charges and input hashes. The arguments above establish the general lemmas; finite controls do not replace them. No new Lean formalization or validation is claimed.

Next isolate the unguarded `TB/BT` and `PP/BT` R,R gaps (and reflected L,L gaps), then show either a justified transfer to another certified donor or a residual aggregate inequality. For several sources the missing statement is precisely a weighted Hall inequality for every source subset, together with the remaining charge control. Arbitrary turns, capacity-two revisits and wider mixed intervals remain outside the general allocation proof.
