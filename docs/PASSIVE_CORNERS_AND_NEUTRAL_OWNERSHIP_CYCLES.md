# Passive phase10 corners and the limits of ownership-cycle charging

20 October 2026. This reconstructs a new transfer rule proposed by research
task f583ea6c and checks its complete four-rotor counterexample. A phase shift
of the established rectangular rotor array strengthens that counterexample
to arbitrarily large ownership cycle rank with zero reserve. The new corner
rule uses actual activations and defect tiles, with explicit shared capacity.
Unrestricted complete-source coefficient one and grid triple equality remain
OPEN. The later neutral-port turning proposal is not used here.

## 1. Complete-source assumptions and the counted corner

Use the complete U/rotor source model and exact geometric reserve identity:
arbitrary finite source count, even U widths>=6 and independent even heights
>=4, all translations/isometries and rotor phases, pairwise disjoint original
endpoint sets, original matchings unchanged, every original support outside
P retained, and final selected occupied degree<=1. Optional selections are
outside original receivers and have no endpoint neighbor. Original ownership
and the physical aligned partition are fixed and transported under normalization.

Keep A,U0,Z0,H,R and mu from EXACT_GEOMETRIC_EVENT_RESERVE.md:

    2R=A+U0+Z0+H, R>=0, mu=N+R-G, sigma>=mu.

G counts marked positive sides, not original negative charge.

Let B count original phase10 outer-corner singleton occurrences whose actual
receiver is nonfull2P1T, whose original support is consumed, and whose original
blank is not an endpoint. Count each original corner once. The theorem is

    B <= 2A+H,
    B+H+2U0+2Z0 <= 4R.                            (1)

In the established nonexceptional failingR1 AA component, the stronger
conclusions are

    B <= A=2,
    a phase10 owner with one B corner has its other corner receiver full. (2)

The AA census and all its consequences below concern the SAME endpoint
component. Other components may have additional positive activations.

## 2. A passive corner either stops at H or reaches a positive source

Normalize the counted phase10 corner with outer bar row0, columns1..v,
inner bar row-1 and legs pointing north. Its original singleton tile is
{0,1}x{0,1}, with endpoint p=(0,1), support q=(0,0), and original adjacent
blank b=(1,1). Since q is consumed, the actual endpoints are p,q. The actual
selected point must be t=(1,0), not b. Otherwise a retained b would already
see p; its unique original anchor would have to be p, making it an original
support of p's owner, contrary to the original1P1T profile. Optional selections
cannot neighbor p either. Hence t is retained, and b and(2,0) are unoccupied.

The next bar receiver Q={0,1}x{2,3} has the original2P0T pair(0,2),(0,3).
Neither other corner can be finally selected: its original anchor would
have to be the adjacent parent endpoint, yet this original profile has no
support. If Q is nonfull, it is an actual2P0T or mixed3P0T tile and gives
at least one H unit. Call this a direct D stop.

If Q is full, consider x=(1,2). Its north neighbor is an original endpoint
of the parent. Its west neighbor b is neither an endpoint nor an original
support of x's owner: such a support would have to remain selected and would
see both p and x. Thus west is x's unique original blank. Original occupied
degree three forces north to be an original support, now consumed.

The complete original role possibilities are:

| Original owner at x | Role and direction | Outcome |
|---|---|---|
| U | upper outer corner, bar south, legs east | positive U |
| U | terminal, predecessor south, exterior east, bar west | positive U |
| rotor | its unique role with north support and west blank | endpoint at(2,0), impossible |

Interior bar/lower-corner roles have three own endpoint neighbors and cannot
have a foreign endpoint north. A stem-interior role with west blank would
have an own endpoint north. At the two surviving U roles the source's even
dimensions and transported physical partition give phase00. The symbolic
Lean role proof uses arbitrary dimensions in all eight orientations.

For rotors, quarter-turn invariance reduces all translations to two
chiralities and eight endpoint roles. The uniquely translated surviving
role has an endpoint at(2,0), forbidden by retained t. This fixed16-role
table excludes every rotor phase; it is not a bounded translation search.

The corner role consumes the positive leg's original index-zero exterior
support at(0,2). If that leg is unactivated, the accepted exterior-chain
propagation gives a first nonfull original regular2P1T receiver, hence an
L3 stop. If all receivers were full, the original terminal would activate.
Call this case C0. The activated-corner case is C1. A positive terminal at
x has its singleton tile full, so is actually activated; call this E1.

## 3. Shared resources and the factor two

Every counted corner has exactly one of the alternatives D,C0,C1,E1.
Direct D stops contain their original negative2P0T pair. Two such stops
cannot share a nonfull tile: distinct original pairs would fill four
positions. The two ends of one parent use different bar receivers for v>=6.

C0 routes belong to distinct positive legs. A corner claim determines an
original positive corner, hence its leg. Two parents cannot claim that same
corner: their original bar pairs would overlap in its fixed physical tile.
Thus different C0 routes have disjoint original positive regular receiver
pairs and cannot stop in one nonfull tile. A D stop and a C0 stop cannot
coincide either: their negative irregular and positive regular pairs have
different original owners and would make the tile full. Consequently

    D+C0<=H.

A C1 claim uses a particular activated original positive leg through its
outer corner. Each such corner can receive at most one claim. An E1 claim
uses the same kind of activated occurrence through its terminal, and each
terminal can receive at most one claim: two original parent pairs cannot
fit disjointly into the other three corners of its tile. The fourth full
corner is allowed a third owner; no2+2 ownership assumption is needed.

    C1<=A, E1<=A, hence B=D+C0+C1+E1<=H+2A.

The factor TWO is deliberate. One activated leg could receive one corner
claim and one terminal claim. It has not become two independent activation
occurrences. Combining this shared bound with the existing exact identity
proves the second part of(1). The D stops are not proved disjoint from all
older z/r irregular-pair witnesses; do not add them again to that older
common pool. C0 routes are the already-defined exterior routes, not fresh X.

## 4. AA exclusions and the other receiver

The established AA saturation and width-six reductions give A=2,H=U0=Z0=0.
The only two activations are the short terminals of the two double-marked
width6 positives. The incoming normalization for either O=U(6,a,b), a>b,
is Rowner(r,col)=(k+2-r,col+4) on U(vR,k,f), with k>=b and k+10<=a.

In the full adjacent receiver, an E1 short-terminal claim would place the
positive's inward neighbor at the forbidden west point b. But Rowner owns
that inward neighbor: (b,5) belongs to its near stem. Thus E1=0. Since H=0
also excludes D and C0, every B corner injects through C1 into one of the
two actual activations. This proves B<=2 without introducing a new payment.

Normalize such a charged positive O to its standard coordinates with short
corner(0,6). The charging phase10 source F has bar columns7,8, rows-1..v-2,
and legs pointing east. Rowner's bar has rows k+1,k+2 and contains columns7,8.
They are different original owners, as Rowner also owns a near tip in column5,
while F's endpoints have columns>=7. Original bar disjointness and evenness
give

    v<=k+2<=a-8.                                  (3)

If both F corners were counted, the two charged positives have opposite leg
directions and are different originals. Returning to F's horizontal bar
normalization, their long legs have endpoint intervals in row6

    [2,aL+2], [v-1-aR,v-1], aL,aR>=4.

Disjointness forces v>=aL+aR+4, contrary to v<=aL-8 from(3). Thus the
other corner cannot be another B occurrence.

In the coordinates relative to O, the other F corner is p*=(v-2,7), with
original support t*=(v-1,7) and original blank q*=(v-2,6). Suppose its
opposite nonfull2P1T orientation occurred: t* retained and q* an endpoint.
Then b*=(v-1,6) cannot be an endpoint, since t* sees its own anchor p*.

Pulling b* back to Rowner gives(k+3-v,2). If v=k+2, this is original bar
endpoint(1,2), impossible. Otherwise v<=k, so its row is odd and between3
and k-3. It is an original mandatory interior support, anchored at(v-1,5).
Because b* is not consumed, it remains selected and also sees occupied q*,
again impossible. These arithmetic/source-support alternatives are checked
for arbitrary even v,k in Lean.

The H=0 local profile catalogue leaves only the two actual nonfull2P1T
orientations for an original irregular singleton; other nonfull cases
incur L1,L2mutual or mixed L3. Both orientations have just been excluded.
Therefore F's other corner receiver is full. Fullness is a structural
constraint and is not an additional ledger payment.

## 5. Complete zero-reserve ownership cycles, with unbounded cycle rank

The broad rule “a finite ownership cycle forces a positive reserve or
A/X/U0/Z0/H contribution” is false. This does not refute a rule retaining
the special negative-U and AA-core hypotheses.

The smallest control here has four reference rotors translated by

    (1,3), (3,1), (3,5), (5,3).

Keep all original matchings and retain every original support outside their
endpoint union. The endpoint sets are disjoint. Its mixed full tiles have
owner pairs(0,1),(0,2),(1,3),(2,3), forming a4-cycle. There are32 endpoints,
16 matching edges and16 retained supports, each with one occupied neighbor.
Every rotor has effective phase11 and four regular2P1T profiles. The four
mixed full tiles each have two regular events, so C=2*4-8=0. Also S=0 and
Kirregular=0, hence R=mu=0 and all A,X,U0,Z0,H vanish. It fits in12x12,
with actual ambient slack40, so it is not an ambient counterexample.

More generally, for arbitrary integers h,j>=1 take the rotors with translations

    tau(r,c)=(2r+2c+1, 2r-2c+2j-1),
    0<=r<h, 0<=c<j.

This is an odd/odd translate of the established rectangular rotor array in
ROTOR_ONLY_RESERVE_AND_RECTANGULAR_COMPONENTS.md. It is a consequence of
that existing constructor and support proof, not a new claimed array
construction. Translation preserves endpoint disjointness, original
matchings, support retention and feasibility, while changing the physical
profile phase to the zero-charge four-regular-pair type.

Here is a direct all-size count. Distinct translated original supports never
coincide, as follows from the original finite support-difference catalogue.
Each source has two supports toward each of its four index neighbors, and
only that neighbor can consume them. The established rectangular support
proof shows boundary supports are retained with their unique original anchor.
If V=hj and E=(h-1)j+h(j-1), there are4E consumed original supports and

    |P|=8hj, |M|=4hj, |T|=8hj-4E=4(h+j).

Each original receiver is a regular pair. In tile indices its four receivers
form a2x2 square. Two source receiver sets intersect only when their(r,c)
indices are cardinal neighbors; the unique shared tile is full with two
disjoint original pairs. This follows by subtracting receiver offsets:
an intersection requires both |dr+dc|<=1 and |dr-dc|<=1, leaving exactly
the four index neighbors for distinct integer indices. Thus Jfull=E and
Kregular=2E, with no additional mixed full tiles or irregular events.

The ownership graph is exactly P_h square P_j and its cycle rank is

    E-V+1=(h-1)(j-1).

Nevertheless C=S=Kirregular=R=mu=0 for every size. All nonfull receiver
tiles have one original regular-pair owner, so H=0; this rotor phase has no
singleton or triple profiles, so Z0=0. A=X=U0=0 because there are no U sources.
Cycle rank is unbounded while all these quantities vanish. The construction
fits in the even square of side2(h+j)+4, where the actual ambient slack is
2h^2+2j^2+4h+4j+8, strictly positive.

An invariant based only on the existence or number of arbitrary ownership
cycles cannot prove the desired compensation. It must retain the negative-U
roles or their actual defect/activation transfers. The neutral-port turning
proposal from the original research response has not been reconstructed or
used as a theorem in this note.

## 6. Validation scope and next missing transfer

Scoped Lean statements prove the universal U owner-role and positivity
classification, complete rotor-role exclusion, conditional shared charging,
and the unbounded AA coordinate contradictions. Original occupancy-to-role,
normalization, physical witness injection, AA census and saturation adapters
remain written. Execution receipts are separate.

All12 declarations compile/build locally with Lean4.33.0 and pass individual
axiom audits, using only propext, Classical.choice and Quot.sound as applicable.
The two exact rotor declarations and retained-support contradiction use no
axioms. See output/passive-corner-transfer-formal-check.json. The first proof
splits original bar rows and stem columns before arithmetic elimination,
avoiding an exponential unsplit role search.

The physical checker reconstructs actual passive corners and charges from
complete retained-support fusions. Its current existing fixtures cover only
the direct H branch; positive-corner/terminal routing remains covered by the
general written proof and symbolic role classification, not a claimed
complete physical example. The complete four-rotor cycle and all-size family
have separate nonvacuous physical controls. No complete AA fixture is claimed.

Controls PASS640 complete feasible images with136 counted corners, all on
the direct H branch;32 phase images of the four-rotor cycle; and8 rectangular
family sizes, up to cycle rank49. These are discovery/verification controls,
not substitutes for the general proofs above. Independent review is running
in conversation conv_58f8d949019f143a, original stream session20374; no accepted
review verdict is claimed yet.

The missing step is to force a relevant negative-source continuation to
reach these chargeable corners, or to handle its full-receiver/phase01/rotor
exit with a quantity that is not reused. The other receiver being full
does not itself pay anything. The Epair cap budget is a separate necessary
constraint on the same reserve; neither lower bound is added to the other
without a new disjointness proof. Preserve mu versus actual sigma throughout.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
