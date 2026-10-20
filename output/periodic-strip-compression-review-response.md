Verdict: REVISE — one correction is needed in the termination ruleThe substantive compression argument passes under the supplied complete-source/Horn model and the stated half-slot ledger. This includes arbitrary source counts, independent even U dimensions, all phases and isometries, exact preservation of the original-owner Horn clause keys, and simultaneous reserve monotonicity for every legal retained subfamily.The required correction is in §6: restrict candidate deletions to strips inside the current occupied bounding interval. With the present definition, there are always permitted strips arbitrarily far outside a finite configuration. Such deletions do not reduce its span, and the stated stopping condition, “no permitted even  $q$  exists,” can never hold.This is a counterexample to the written descent assertion. The compression theorem itself admits a direct repair without changing its scope or constants.I refer below to the two supplied manuscripts as Compression and Reserve.Audit itemResultFeature count and coverage of interval changesPassReconstruction of every allowed U and rotor, including canonical matchingPassFeasibility in both directions for every retained owner setPassPreservation of Horn keys whose witnesses lie in deleted rowsPassActual side marks and positive-owner identitiesPassInherited local defect calculation and incidence cancellationPass under the stated half-slot ledgerAll-subfamily  $A,U_0,Z_0$  invariance and reserve lossPassTermination as presently writtenRevise: restrict to internal stripsLinear bound after that correctionPass; the argument gives  $440n+2$ 1. The precise termination gap and its repairTake the normalized single U with
$$w=6,\qquad a=b=4.$$
Its occupied rows, and all the distinguished row coordinates prescribed in Compression §2, lie between  $0$  and  $5$ .The even choice  $q=10$  satisfies the stated protection condition: neither  $10$  nor  $11$  is within distance four of a distinguished row coordinate. Nevertheless, deleting those rows changes no point of the configuration. Its occupied row span does not decrease.More generally, for every finite distinguished-coordinate set  $D$ , sufficiently large even  $q$  satisfies
$$\operatorname{dist}(q,D)>4,\qquad
\operatorname{dist}(q+1,D)>4.$$
Consequently, “repeat until no permitted even  $q$  exists” has no terminal configuration if “permitted” retains its unrestricted §3 meaning.Required replacementFor a nonempty current configuration, let
$$\ell=\min\{r:(r,c)\text{ is occupied}\},\qquad
u=\max\{r:(r,c)\text{ is occupied}\}.$$
During row compression, consider only even  $q$  satisfying
$$\ell<q,\qquad q+1<u,$$
in addition to the existing feature-protection condition.The beginning of §6 can then read:Consider only deletions whose two rows lie strictly inside the current occupied bounding interval. Its extremal occupied rows are distinguished and protected. Every permitted internal deletion therefore leaves occupied vertices on both sides and reduces the occupied row span by exactly two. Repeat until no permitted internal deletion remains.The empty family is handled separately with zero span.This supplies a decreasing nonnegative integer measure. It also makes the subsequent counting argument apply to precisely the finite interval being bounded.2. The feature budget covers the unrestricted source catalogue2.1 U sourcesThe  $18$  base feature points have the advertised coverage:Six opposite corners cover both coordinate endpoints of the three endpoint rectangles.Four isolated-support points cover their singleton coordinates.Eight string endpoints cover both ends of the four period-two support strings.Every endpoint or support piece is therefore an axis-aligned rectangle, singleton, or period-two interval whose coordinate interval endpoints are distinguished. Opposite corners suffice for this purpose; all four rectangle corners are unnecessary.The two four-point guard records add at most eight points. The U catalogue has at most two regular-singleton/triple tiles, contributing at most eight further corners. Hence
$$18+8+8=34$$
is a valid bound.The special-tile assertion agrees with the given constructor:In the positive phase, the two terminal endpoint tiles are regular singletons.In phase  $11$ , the two bar-corner tiles are triples.The other phases have neither kind of special tile.Independent even heights do not change these counts. In particular, unequal leg lengths introduce no additional terminal profile type.2.2 RotorsThe supplied matching gives the endpoint set
$$\{(1,2),(2,2),(2,3),(2,4),
  (3,1),(3,2),(3,3),(4,3)\}.$$
Together with the eight supplied supports, this gives sixteen base feature points.Directly partitioning these points into aligned tiles gives the following phase catalogue, up to the corresponding parity adjustment under lattice isometry:Rotor phaseEndpoint-profile arrangementRegular-singleton/triple tiles $00$ One full profile and four irregular singletons $0$  $01$ Two triples and two regular singletons $4$  $10$ Two triples and two regular singletons $4$  $11$ Four regular pairs $0$ Thus
$$16+4\cdot4=32$$
feature points suffice.Isometries permute coordinates and phases without increasing these bounds. Therefore, in either axis,
$$K\le 40n$$
is valid, with room to spare. No feature count depends on U width or leg length.2.3 The larger periodic band follows from these featuresLet  $D$  be the distinguished row-coordinate set. The exclusion of distinguished coordinates within distance four of either deleted row implies
$$D\cap[q-4,q+5]=\varnothing.$$
On this band, each individual source piece either misses the band entirely or continues through it with constant or period-two row pattern. This statement holds separately for endpoint membership and original-support membership, owner by owner.That is the correct strength of periodicity for the subsequent proof. Periodicity of the full-family occupied indicator alone would not suffice.3. Source reconstruction is valid for all allowed orientations and dimensionsFor a U whose stems are parallel to the compression axis, a permitted cut can shorten either crossing stem by two. A stem ending before the cut retains its height. The bar and all interval changes remain protected, so no other deformation occurs.For a U whose bar is parallel to the compression axis, an interior cut shortens the width by two. One outer stem and its entire support pattern translate with that side of the bar. Reflections determine which side moves; they introduce no additional geometric case.The minimum-dimension condition is protected with substantial slack. For example:A cut through a normalized stem must be sufficiently far from both its start coordinate  $2$  and its terminal coordinate. An affected even height is at least  $14$  before such a cut, hence at least  $12$  afterward.A cut through a bar requires its two endpoint coordinate levels to be sufficiently separated. Its width is at least  $12$  before the cut, hence at least  $10$  afterward.These conservative bounds already exceed the required height  $4$  and width  $6$ . Additional guard features can only exclude more cuts.The explicit support strings reconstruct correctly because shortening and translation occur by two. Their parity classes remain unchanged, and their endpoint supports move to the corresponding new endpoint positions.Canonical matchingRegenerating the matching is necessary and sufficient. For the reconstructed U:The odd-starting row- $0$  edges pair every row- $0$  endpoint.The even-starting row- $1$  edges pair the interior row- $1$  endpoints.The odd-starting stem edges pair the two remaining row- $1$  corners and all stem endpoints.Even dimensions ensure that every endpoint is paired exactly once.The coordinate deletion map is injective on surviving vertices. Thus disjoint original endpoint sets remain disjoint, and the regenerated source matchings form a valid matching on their union.Rotor rigidityEvery rotor endpoint and support row is distinguished. If a rotor straddled a permitted strip, it would have an occupied row at most  $q-5$  and another at least  $q+6$ . Its row diameter would therefore be at least eleven.The supplied rotor has diameter five in each coordinate. It cannot straddle the strip and consequently undergoes a rigid translation or remains fixed.These arguments establish the reconstruction claim for the entire supplied catalogue.4. The owner-labelled argument proves feasibility for every subsetWrite the original endpoint and support label fields as
$$E(x)=\{i:x\in P_i\},\qquad
S(x)=\{i:x\in S_i^{\mathrm{orig}}\}.$$
The support label is retained in  $S(x)$  even when an endpoint consumes that support.For an owner set  $I$ , the complete-source occupied and selected sets in the stipulated Horn model are determined by
$$x\in O_I
\iff
I\cap(E(x)\cup S(x))\ne\varnothing,$$
and
$$x\in T_I
\iff
I\cap S(x)\ne\varnothing
\quad\text{and}\quad
I\cap E(x)=\varnothing.$$
These formulas explain why the argument covers restored supports after owners are removed. They also make the quantifier over all retained owner sets explicit.Let
$$\phi(r,c)=
\begin{cases}
(r,c),&r<q,\\
(r-2,c),&r\ge q+2
\end{cases}$$
on surviving old vertices. Source reconstruction gives
$$(E',S')(\phi(x))=(E,S)(x).$$
Away from the seam, neighbors transport directly. At its two boundaries:At old row  $q-1$ , the new lower neighbor comes from old row  $q+2$ , whose label field equals that of the deleted old neighbor in row  $q$ .At old row  $q+2$ , the new upper neighbor comes from old row  $q-1$ , whose label field equals that of the deleted old neighbor in row  $q+1$ .Thus, for every  $I$ , every surviving vertex has the same selected status, endpoint-owner label, and occupied degree after transport.This proves forward feasibility. It also preserves every old violation whose center survives.Deleted violations and deleted Horn witnessesThe reverse direction is covered by the larger periodic band.For a witness centered in row  $q$ , copy its center and radius-one neighborhood two rows downward. For a witness centered in row  $q+1$ , do the same. The needed row-field equalities are
$$L_{q-1}=L_{q+1},\qquad
L_q=L_{q+2},\qquad
L_{q+1}=L_{q+3},\qquad
L_{q+2}=L_{q+4},$$
where  $L_r$  denotes the entire owner-labelled row field.The copied center lies outside the deleted strip. Its data retain:The original support-producing owner.That support’s unique original endpoint anchor.The owner supplying the second occupied neighbor.The unique endpoint owner consuming the support.Therefore the same original-owner Horn key has a surviving occurrence.Conversely, a new witness lifts to its surviving old center, using the seam equalities when one neighbor crosses the seam. Its owner key is unchanged.Hence the raw sets of nontrivial clause keys are equal:
$$\mathcal C(F')=\mathcal C(F).$$
Witness multiplicities may change; the claimed key set does not.The stipulated exact Horn characterization now gives
$$I\text{ feasible in }F
\iff
I\text{ feasible in }F'$$
for every  $I$ , and equality of Horn closure on every seed. Support/support conflicts are included because occupancy uses both endpoint and original-support labels.5. Actual marks survive without a new gate equivalenceThe supplied marking adapter identifies a side indicator through the occupied-degree-four predicate on its canonical leg/guard protectors.The protected records correspond to the reconstructed constructor’s records:Under stem shortening, the bar-end records remain fixed.Under bar shortening, one record remains fixed and the reflected record translates by two. The reflection midpoint moves by one, exactly as required by the new width.Rigidly translated sources transport their records rigidly.Their associated protector endpoints survive. The degree-preservation argument above applies to these endpoints for every retained owner set.Consequently, each positive owner has the same two actual side indicators in every legal restriction. Even displacement preserves source phase, so positive-owner identities also remain unchanged:
$$N'(I)=N(I),\qquad G'(I)=G(I).$$
The consuming endpoint-owner label at each protected support is preserved as well. This establishes the labelled incidence information needed later for the canonical hull.The direct degree argument is sufficient; no additional consumption-to-marking equivalence is required.6. The inherited reserve proof passes its local and global auditsI checked the derivation in Reserve §§2–3 using its stated half-slot identity and event/residual-credit definitions. The prior review verdict is unnecessary for this calculation.6.1 Local nonnegative defectThe local quantity is
$$h_Q
=i_Q+b_Q-2(k_Q-c_Q)+f_Q-d_Q.$$
The nonfull cases have exactly the four positive defect classes stated in the manuscript:Nonfull tile class $h_Q$ One irregular singleton $1$ One original irregular pair $2$ Two mutually supporting irregular singletons $2$ Three endpoints with multiple original owners $1$ Every other feasible nonfull class $0$ The feasibility exclusions used to obtain this table are valid:Diagonal singleton endpoints: an original intratile support of either singleton would remain unconsumed and have both endpoints as occupied neighbors.Adjacent singleton endpoints: the two complementary corners cannot both remain selected, because they are adjacent and each already has an endpoint neighbor.Three endpoints: the missing corner cannot retain an original support, because it has two endpoint neighbors.These restrictions give precisely the support placements in the supplied two-owner and three-owner cases. In particular, they justify the distinction between the mutually supporting irregular pair and the adjacent irregular pair with one active event.For full tiles, the residual-credit calculations give:Full owner partition $\Lambda_Q$  $d_Q$  $f_Q$  $h_Q$  $4$  $0$  $0$  $0$  $0$  $3+1$ , regular singleton $0$  $1$  $1$  $0$  $3+1$ , irregular singleton $0$  $0$  $0$  $0$  $2+2$  $0$  $0$  $0$  $0$  $2+1+1$ , with  $j$  irregular singletons $2-j$  $2-j$  $0$  $0$ Four singletons, with  $j$  irregular owners $4-j$  $4-j$  $0$  $0$ For example, in the  $2+1+1$  case, with  $t$  indicating an irregular pair,
$$i=k=2t+j,\qquad c=1+t,$$
so
$$\Lambda_Q=(2t+j)-2\bigl((2t+j)-(1+t)\bigr)=2-j=d_Q.$$
In the  $2+2$  case,
$$i=2t,\qquad k=2t,\qquad c=t,$$
which gives  $\Lambda_Q=0$ .Thus the local identity
$$h_Q=l_1+2l_{2,\mathrm{bar}}
       +2l_{2,\mathrm{mutual}}+l_3$$
and its nonnegativity are justified.6.2 The rotor bridge follows from the supplied coordinatesConsider the mixed phase whose original-coordinate tile intervals have odd row starts and even column starts.Its two triple tiles are
$$\{1,2\}\times\{2,3\},
\qquad
\{3,4\}\times\{2,3\},$$
with missing corners  $(1,3)$  and  $(4,2)$ .The first is paired to the regular singleton  $(2,4)$ . If a foreign endpoint fills  $(1,3)$ , the original support  $(1,4)$  has the two endpoint neighbors
$$(1,3),\qquad (2,4).$$
Feasibility forces  $(1,4)$  to be consumed by an endpoint, activating that singleton.The second is paired to the regular singleton  $(3,1)$ . Filling  $(4,2)$  similarly forces the original support  $(4,1)$  to be consumed, because its endpoint neighbors are
$$(4,2),\qquad (3,1).$$
This is a bijective pairing of the two triples with the two regular singleton occurrences. The other mixed phase and all isometries transport this argument. It does not require the owner filling a triple to be the owner consuming its bridge support.6.3 The global cancellation has no duplicate expenditureThe occurrence identities are
$$D=A+D_R,$$

$$U_0=2B_{11}-B_U-F_U,$$
and, by the bridge and bijective pairing,
$$Z_0=D_R-B_R-F_R.$$
Summing the local defect identity gives
$$H=\Lambda+F_U+F_R-A-D_R.$$
Therefore
$$\begin{aligned}
A+U_0+Z_0+H
&=A+(2B_{11}-B_U-F_U)\\
&\quad +(D_R-B_R-F_R)
 +(\Lambda+F_U+F_R-A-D_R)\\
&=2B_{11}-B_U-B_R+\Lambda\\
&=2R.
\end{aligned}$$
The last equality uses the stipulated half-slot identity. The displayed cancellation establishes the simultaneous contributions directly; it does not allocate the same residual credit twice.7. All-subfamily invariance and exact margin loss followEvery original regular-singleton and triple tile is protected by all four corners. Therefore none lies in the deleted tile row.For any retained owner set  $I$ , each such tile preserves:Its original endpoint-owner profiles.Original support labels, including consumed supports.Activation of each retained regular singleton.Final fullness.The rotor singleton–triple pairing, because the rotor remains rigid.Consequently,
$$A'(I)=A(I),\qquad
U_0'(I)=U_0(I),\qquad
Z_0'(I)=Z_0(I).$$
Because  $q$  is even, rows  $q,q+1$  form one complete aligned tile row. Every new physical tile is the image of exactly one undeleted old tile. Its original profiles and retained endpoint-owner labels are identical, so its local defect is identical.Thus, for every legal  $I$ ,
$$H'(I)=H(I)-H_{\mathrm{strip}}(I).$$
Applying the reserve identity to both feasible configurations yields
$$\boxed{2\bigl(R(I)-R'(I)\bigr)=H_{\mathrm{strip}}(I)\ge0.}$$
Together with preservation of  $N$  and  $G$ ,
$$\boxed{2\bigl(\mu(I)-\mu'(I)\bigr)=H_{\mathrm{strip}}(I)\ge0.}$$
The same geometric splice works for every  $I$ . The deleted defect total may depend on  $I$ , but it is nonnegative for every legal  $I$ . Its evenness follows from the equality between integer reserves.This argument correctly concerns shortening geometry. It invokes no reserve monotonicity under adding or deleting owners.8. The corrected iteration gives the advertised linear boundUse the internal-cut rule from §1 of this audit.Each row deletion reduces the occupied row-span length by two. Source reconstruction preserves the catalogue and its feature bound, so the process terminates after finitely many steps.At termination, let  $K\le40n$  be the number of distinguished row coordinates in the resulting configuration. Inside its occupied bounding interval:The radius-four protective intervals cover at most  $9K$  integer rows.Their union has at most  $K$  components.There are at most  $K+1$  complementary unprotected runs.Every such run has length at most two.The last assertion follows because three consecutive integers contain an even-starting consecutive pair, which would be an available internal cut.Therefore
$$\operatorname{span}_{\rm rows}
\le 9K+2(K+1)
=11K+2
\le440n+2
\le512n+2.$$
The argument uses the features of the final reconstructed configuration. It does not require feature coordinates to remain fixed throughout iteration.Column compression applies the same proof. It introduces no new row coordinates, so the established row bound remains valid. An even translation places each lower coordinate at  $0$  or  $1$ ; extending to even side lengths needs at most two additional rows or columns. Hence the stated
$$512n+4$$
rectangle bound follows.Every step preserves the same legal owner sets and labelled marks, and decreases every legal subfamily margin. Induction therefore proves the simultaneous assertions for the whole finite sequence.9. The canonical-hull consequence is validThe demand data retain the same positive-owner and consuming-owner labels. The raw Horn keys are identical. Hence the demand seed and its Horn closure give exactly the same owner subset before and after compression.There is also no hidden monotonicity assumption in the signed-loss consequence. For a demand-preserving hull  $H$ ,
$$N(H)=N(F),\qquad G(H)=G(F),$$
so
$$\mu(H)-\bigl(R(H)-R(F)\bigr)=\mu(F).$$
Thus failure of
$$R(H)-R(F)\le\mu(H)$$
is exactly  $\mu(F)<0$ . Since compression preserves the hull’s owner identity and makes  $\mu(F)$  nonincreasing, that failure survives.This does not require  $R(H)-R(F)$  itself to be monotone.Required editorial action: insert the internal-strip restriction into §6 and change its stopping condition accordingly. With that correction, the written argument supports the full stated compression reduction. It supplies neither a bound on the number of sources nor a proof of  $\mu\ge0$  or rectangular-grid equality; the stated local scope of the Lean formalization remains unchanged.
