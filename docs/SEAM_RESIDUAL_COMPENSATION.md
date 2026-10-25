# Seam completion: all retained degree-three extensions of connected copies

25 October 2026. Haobo Ma and Wenlin Zhang. Research branch only.

Continuation: [colored interval slots](COLORED_INTERVAL_SLOTS_AND_MONOCHROMATIC_HOLES.md)
extracts the portable color-capacity rule and gives a completely frozen
same-color-hole obstruction to allowing two uncolored slots per resource.
The one-tip-per-original-unit hypothesis used here is sufficient and unchanged.

The [fixed-rectangle theorem](RESIDUAL_FRESH_DOMAINS.md) now extends to **every
number of horizontally connected copies**, with arbitrary additions of T/P
and arbitrary actual rematching, provided the final rectangle keeps height 28,
width 24n and the original boundary conditions. Every final endpoint having
occupied degree at least three is sufficient; complete freezing implies this
condition. The construction pays all original alphas by an ordinary packing.

The new ingredients are an injective seam certificate, a bounded bottom BT
corridor, and a reduction of all relevant uncovered alpha ends to one color.
No interval is assigned to two certificate tips. A completely frozen all-n
family shows an unbounded real improvement over the previous restricted pool:
its old deficit is n-1, and exactly one distinct new unit per seam repairs it.
The unrestricted numerical 5/6 improvement and universal grid compensation
remain open; the retained old occupation and fixed height are essential scope.

## 1. Precise theorem and ledger

Let B_n be the 28-by-24n retained occupation from
[connected frozen copies](../develop/check_connected_frozen_interval_repair_obstacle.py),
with n>=1: n translated 49T/308P bases, plus the existing PP seam endpoints
at rows 2,3 and columns 23+24i,24+24i for 0<=i<n-1. Its initial endpoint count
is 308n+4(n-1). The reference matching specifies B_n but is **not retained**
in the theorem. The two PP sites in each seam band remain endpoints.

Let (T,P,M) be any configuration on that SAME rectangle, with the same
horizontal two-row bands, satisfying:

1. All initial selections T0 and endpoints P0 of B_n are retained, and T,P
   are disjoint. M is any adjacent-grid perfect matching of P.
2. Every selected site has at most one occupied neighbor in T union P.
3. Column 0 is blank. In column 24n-1, each band has at least one blank site.
4. Every vertex of P has at least three occupied neighbors **inside this
   rectangle**. No freezing order or retained M edge is assumed.

**Theorem 1 (seam-completed retained-extension compensation).** Every original
alpha of (T,P,M) admits ordinary compensation by different original beta
resources and available original BB--TT interval units.

In particular this holds for every completely frozen retained-occupation
extension of B_n on the same rectangle, for every n and every actual M.

Start with the previous conditional certificate. Let h count filled old
flexible targets, p retained-P promotions, g active protected fresh tips, and
q their occupied conditional BP targets. Let z count **nonbottom unprotected
seam TPs**, at rows 8--23 and columns 23+24i or 24+24i. Let b count active
bottom-even tips (26,14+24i). Let z_BP,b_BP count their new BP assignments.
The new certificate covers precisely the old covered tips plus those z+b:

    covered = 23n+p+g+z+b,
    B = 18n+h+p+q+z_BP+b_BP,
    R = 5n-h+g-q+(z-z_BP)+(b-b_BP).

All B physical BP targets are different, and all R original interval
identities are different, **one tip per original unit**. Thus covered=B+R.
Selecting these B links and applying ordinary subset normalization gives the
claimed compensation with at most B links. These are certificate cost bounds,
not assertions of minimum cost. The beta/interval ledger counts each actual
resource once across all connected components.

## 2. Necessary sites and periodic geometry

Write bar(v) for the other site in v's two-row band, and O0=T0 union P0.
Let F include old blank neighbors of saturated old selected sites, as well
as the actual blank first column. Each such site stays blank under retention.
Every old selected site is saturated, including after the original PP splice.

For a fresh TP v, its selected partner t=bar(v) and v were both old blank,
N(t) has no old occupied site, and N(v) has no old selected site. The two
outer boundary columns cannot contain a TP. These necessary conditions give:

* The 39 local residual candidates in the fixed-rectangle note, translated
  into every copy, after removing the old 27-site protected set.
* At each internal seam, the following 28 additional candidates, translated
  by 24i columns:

| Rows | Seam columns |
| --- | --- |
| 8,9,10,11,12,13 | 23 and 24 |
| 14,15,16,17,18,19,20,21 | 23 |
| 22,23 | 23 and 24 |
| 26,27 | 23 and 24 |

This is an arbitrary-n coordinate reduction, not an inference from testing n
values. Away from columns 0,23 of a copy, the old local occupation repeats
with period 24; the added splice endpoints occur only at rows 2,3. Around
an internal seam the nearest-neighbor stencil is exactly the same two-copy
stencil, independent of n and of other seams. The outer physical boundaries
remove the outer seam candidates. Checking the literal local and seam
stencils therefore covers every translate. The verifier also recomputes the
full necessary set for n=1,...,6 to check this adapter.

Let Q be the union of all possible old conditional BP targets: old 18n,
flexible sites, promotion sites and protected fresh targets. The literal
coordinate comparison gives no horizontal adjacency from any unprotected
candidate to Q. For interior copies this is checked in the same periodic
stencil, not by treating their column 0 or 23 as a physical boundary.

Two further old-geometry facts will be used repeatedly:

* At rows 8--23, both sites of each band at local columns 3 and 20 are
  retained P. Therefore these columns cannot be BB or TT; local columns 2
  and 21 cannot be TT either, since a selected pair there would see a
  distinct retained neighboring P.
* In the bottom band, row-26 sites at local columns 2,4,6,8,11,17,19,21
  are permanently blank, guarded by old saturated selections in row 25.
  In particular these columns cannot be TT. Old guards also force
  (25,12),(25,16),(25,22), and their translates blank.

## 3. Covering every nonbottom seam TP

**Lemma 2 (one active seam TP per band).** In one band, columns 23+24i
and 24+24i cannot both be TP. Also there is only one TP site per TP column.

**Proof.** A TP column is occupied at both sites, one P and one T. If its
neighboring column were also TP, the first column's T would see its own
within-column P and an occupied horizontal neighbor. This violates feasibility,
regardless of the two TP orientations. P/T disjointness excludes two opposite
TP orientations at one column. QED.

For each nonbottom seam TP v, inspect its horizontal neighbors. Feasibility
of bar(v) forces their band partners blank. Consequently each neighbor is
blank (a BB port), selected (BT), or a BP endpoint.

**Lemma 3 (a usable target).** If a BB port exists, its original interval is
available and lies entirely within columns 21+24i through 26+24i. Otherwise
v has a horizontal BP neighbor.

**Proof.** A BB port is in column 22,23,24 or 25 of the seam stencil. Its
BB--TT interval cannot pass the left retained PP column 20, or the right
retained PP column 27 (local column 3 of the next copy). Columns 21 and 26
cannot be TT, as noted above. This bounds the component's BB vertices between
21 and 26; its BB--TT path is internal and unmarked, hence available.

If there is no BB port and no BP, both horizontal neighbors of v are selected.
Its actual mate cannot be either selected neighbor or its selected band
partner, so it must be transverse vertical. The two lateral selections force
the two horizontal neighbors of that mate blank. The mate then has only its
actual mate v and at most one other vertical occupied neighbor, contradicting
minimum occupied degree three. If the transverse site is outside the board,
there is no actual mate to begin with. Thus a BP exists. QED.

Choose one available port unit when there is a BB port; otherwise choose
one horizontal BP. These assignments are compatible with the old certificate:

1. New BPs are outside Q. Targets of two seam sources can coincide only
   for sources in the same physical row two columns apart. The possible
   seam source columns are 23,24 modulo 24, with different seams 24 apart;
   such a pair does not occur. BP targets are therefore injective.
2. At most one TP per band per seam is active by Lemma 2. Different bands
   have different interval identities. Different seams have disjoint
   [21+24i,26+24i] interval windows. Thus new units are injective.
3. Every assigned old interval is a singleton, at one of the old flexible
   or protected target coordinates. Those columns have residues 2--21.
   The new physical BB port has residue 22,23,0 or 1. If it named the same
   original interval as an old singleton, its BB coordinate would have to
   equal that singleton coordinate, which it does not. This also excludes
   collisions when a larger new interval contains a different potential
   old target that is **not active as an old singleton in this configuration**.

The old promotion targets are BP typed and included in Q. No new unit is
introduced merely because a potential seam site exists: its source must be
an actual TP in the final configuration.

## 4. Bottom-even protection through a bounded BT corridor

Consider v=(26,14+24i) when it is TP. Suppress the copy translation below.
Its selected partner is (27,14), so (27,13) is blank. Put w=(26,13).

* If w is P, then it is BP. Assign v to that physical BP.
* If w is blank, columns 13 is BB. Assign v to its interval.
* If w is selected, it forces (26,12) blank. The site (27,12) cannot be P:
  its upper neighbor is blank, and a bottom-row site then has at most its
  two horizontal occupied neighbors. If (27,12) is blank, column 12 is BB;
  assign its interval to v through the BT column 13.
* Otherwise (27,12) is selected. It forces (27,11) blank. Old T=(25,11)
  forces (26,11) blank, so column 11 is BB. Assign its interval to v through
  the two BT columns 13,12.

These are exhaustive final states. The BT corridor supplies a full gap-support
incidence of v's original owner, as in the established corridor theorem; it
does not assert a physical TP--BP cancellation link through the corridor.

The interval in column 13 can extend left only through TT12/BB11 and
TT10/BB9, since column 8 cannot be TT. Its first BB is 9,11 or 13 and its
last is 13. The column-12 alternative is a singleton: columns 11 and 13
cannot be TT. The column-11 alternative has first 9 or 11 and last 11.
Thus every bottom assigned interval is available, lies within [9,13]+24i,
and has first coordinate in {9,11,12,13}+24i.

Old assigned intervals are in bands at most 12; nonbottom seam assignments
are in bands 4--11. The new bottom intervals are in band 13, and their
[9,13]+24i windows are disjoint across copies. All interval identities are
therefore different. A bottom BP target (26,13+24i) is outside old Q,
outside all new seam target rows, and different in different copies. This
proves simultaneous compatibility, including the BT alternatives.

## 5. Why every remaining relevant hole is odd

Select all BP links of the enlarged certificate as C. We classify an
uncovered TP v using its **actual M-mate**, before any virtual contraction.

A TP matched to a BP has an original one-edge mixed owner. If neither end
is incident to C, that mixed owner remains mixed and cannot supply a final
alpha end. This is the untouched-mixed lemma of the fixed-domain proof.

For the translated local 39-site candidates:

* Horizontal mates give BPs, and old C avoids those BPs by the Q comparison.
  New nonbottom seam links cannot touch their BPs: a collision would require
  a local candidate in column 1 or 22, in the same physical row as a new seam
  source two columns away. The only local residual candidates at these
  columns are in rows 26,27; all new seam sources are in rows 8--23.
* A new bottom BP target at column 13 could meet a horizontal hole at column
  12 or 14. Column14 is covered. A TP at (26,12) has forced blank neighbors
  (25,12),(26,11), leaving at most two occupied neighbors, and is excluded
  by minimum degree three.
* The same seven local transverse cases as before remain. The first three
  have BP mates untouched by C. The exceptional mate (18,9) has degree at
  most two and is excluded. The bottom-even TP at column14 is now covered.
  Only (26,13+24i) and (26,15+24i) can remain as uncovered final alpha ends.

For the seam candidates in the bottom band, no new allocation is needed:

* A TP in row27 must be horizontally matched. Its mate's upper neighbor is
  forced blank by the TP selection in row26, so that mate has degree at most
  two. Hence no such TP exists under the degree condition.
* A row26 seam TP at column23 or24 cannot be transversely matched. The
  potential mate (25,23) has forced blanks (24,23),(25,22); the potential
  mate (25,24) has forced blanks (24,24),(25,25). Each has degree at most
  two. Thus these seam TPs are horizontally matched, and their one-edge
  mixed owners are untouched: old Q avoids them, new seam links are in
  other rows, and bottom-even targets are at column13, far from the seam.

Therefore every uncovered TP that can be an end of a final alpha lies at
(26,13+24i) or (26,15+24i). All have odd checkerboard color.

**Proof of Theorem 1.** The physical multigraph after C is the union of actual
perfect matching M and the secondary matching consisting of PP band edges
and C. Each open path starts and ends with M, so has odd length and opposite-
colored ends. Consequently no final alpha has two uncovered ends, since all
relevant holes are odd. Each final alpha chooses one covered free end and
its assigned original interval. All assignments are injective, so the chosen
units are different across all components.

If a,b are original alpha/beta counts and a_C,b_C the final counts,
cancellation gives a+b_C=b+a_C, with b_C<=b. Distinct beta payments plus these
interval payments total b-b_C+a_C=a. Ordinary subset normalization removes
unused links and cycles without increasing B. This proves complete ordinary
compensation and the ledger of Section 1.

A completely frozen endpoint needs two kept nonmate neighbors when its rank
is first established. Its actual mate cannot be kept before this endpoint
freezes, since being kept would require this same endpoint at an earlier
rank. Thus occupied degree is at least three. The frozen corollary follows.
QED.

## 6. An all-n frozen family with exact reserve deficit

The compact [cap specification](../develop/fixtures/seam_frozen_caps.json)
adds, at every seam i, the actual edge

    (9,23+24i)--(10,23+24i)

and selections (8,23),(11,23),(9,22),(10,24), translated by 24i.
Keep the reference matching of B_n. Each new endpoint has two indicated
selected neighbors, so freezes immediately. Old freezing ranks replay:
none of the added selections or endpoints changes a retained endpoint's
actual mate, and the original PP seam rank construction is unchanged.
The patches are 24 columns apart. This proves feasibility and complete
freezing for every n, not only the checked sizes.

The counts are P=314n-6, T=53n-4, and a=5n-1. Each seam adds one isolated
one-edge alpha. Its two TPs have no horizontal BP neighbor, so it has no
terminal cancellation link; the old conditional interval pool supports none
of these new alphas. The old 4n alphas remain compensated by the old pool.
Hence its true ordinary restricted-pool deficit is exactly n-1.

Choose one extra singleton per seam: band4, column24+24i. Each is available,
and the corresponding new alpha supports it. Among this selected new set,
a seam alpha supports exactly its own unit; it has no link to another source
or resource. For any subset J of these n-1 units, therefore,

    maximum ordinary payment = maximum full payment = 4n+card(J),
    exact deficit = n-1-card(J).

The lower bound uses the old allocation plus those direct unit payments;
the upper bound counts isolated new demands whose own unit is absent.
Exactly n-1 additional distinct units are necessary and sufficient in this
specified reserve model. This is an unbounded repair of the old pool, not
an unrestricted counterexample or a claim of universal improvement of 5/6.

For n=2, the actual frozen board has 622P/102T: old true deficit1 becomes0.
The general injective certificate chooses two distinct seam units; for this
particular family only one per seam is needed for payment. These are separate
claims, so two certificate endpoint assignments are not billed as two required
payments for one alpha.

## 7. Verification, formalization and limits

Mandatory, solver-free verification:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 develop/check_seam_residual_compensation.py \
  --output output/seam-residual-compensation-validation.json
PYTHONDONTWRITEBYTECODE=1 python3 develop/check_seam_cap_reserve_ledger.py \
  --output output/seam-cap-reserve-ledger-validation.json
cd formal
lean SubQuorum/SeamResidualCompensation.lean
```

The main verifier reconstructs original units, full actual M/PP/C multigraphs,
injective assignments, their ledger, untouched holes, the odd relevant-hole
domain, actual opposite-color path ends and ordinary payment. It checks the
complete periodic footprint for n<=6, cap and bottom-cap families through
n=8, independently verifies cap ranks, and exercises all BP/BB/one-BT/two-BT
bottom alternatives. The saved 24 discovery controls have arbitrary rematching
and minimum degree three; their frozen status is recomputed, not assumed.
Optional Z3 discovery is isolated in a separate script and is not needed to
validate the saved cases or prove the theorem. The main receipt contains
408 actual models (48 frozen, 360 degree-three nonfrozen), 368 actual square
rematches, eight independent full cap-rank checks and six independent
ordinary/full primitive comparisons. It checks 1,569 seam assignments,
including 195 BP targets, 78 bottom-even assignments, 26 models with actual
odd uncovered alpha ends, and 9,603 physical odd paths. All four bottom
alternatives occur. The reserve ledger independently checks 40 unit-open
profiles and six more primitive comparisons; these 12 comparisons are in
separate runs, not counted as 12 different model geometries.

The standalone Lean file checks the neighbor-uniqueness contradiction,
seam BP column injection, guarded-degree exclusion, arbitrary-copy interval
window injection, bottom-private coordinate injection, same-color-hole
exclusion and exact certificate/payment ledgers, together with saturated
blank guards and literal local guard geometry. All ten declarations pass
locally in Lean4.33.0: four are axiom-free and the rest use only standard
propext, Classical.choice and Quot.sound. No warning, sorry or native-decision
axiom occurs. The arbitrary-n necessary-site
adapter, BB--TT extraction, actual matching degree argument, bottom corridor,
untouched-owner classification, ordinary normalization and cap-family reserve
isolation are complete written proofs with Python checks. This is not an
end-to-end Lean grid theorem; no independent external review is claimed.

The theorem permits arbitrary M and added T/P, but fixes the full retained
occupation, physical height28, width24n, band phase and boundary conditions.
It does not prove compensation on boards which do not contain these retained
copies, on larger-height rectangles, or under arbitrary removal of old occupied
sites. The next task is to extract geometry-only sufficient conditions from
this construction, and determine whether other occupied adjacent bands provide
the same injective seam protection and monochromatic residual domain. The
11 October submitted manuscript, public main/PR3, shared CI and email are
unchanged by this research branch.
