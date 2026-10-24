Verdict: REVISEThe five-endpoint cap is essentially correct as a general geometric argument. The width-six exclusion of regular singleton consumers follows from it. The activation ledger is algebraically correct, but the sentence asserting that the consumer singleton is activated needs a precise occurrence-level definition or an additional owner-uniqueness lemma. The final width-six positive-consumer corollary is not established as written because the positive-phase odd-start/even-end parity assertion for a vertical  $4P0T$  bar is false or, at minimum, unsupported under the stated isometry and translation allowances. That part is repairable by a direct stem-collision argument.The gaps do not invalidate the five-endpoint cap. They affect:the activation injection if “activation” means ownership by the consumer source rather than support consumption by the consumer occurrence; and  the  $4P0T$  portion of the width-six positive-consumer corollary.The unrestricted  $\mu\ge 0$  problem and the rectangular-grid equality remain open.1. Required semantic clarificationLet  $E$  denote the final union of all selected source endpoints.The cap and activation arguments use the following support-role semantics:
$$z\notin E,\ z\text{ an original support}
\quad\Longrightarrow\quad
z\text{ remains selected as a support},$$
and every retained support  $z$  must satisfy
$$\#\bigl(N(z)\cap E\bigr)\le 1.$$
If  $z\in E$ , its original support obligation is discharged because it has been converted into an endpoint of some source.This must be stated explicitly. If “every finally selected point” literally includes all endpoint points as well as retained supports, then the intermediate sentence “ $x$  cannot remain selected, so some added source must own  $x$  as an endpoint” is not the stated rule: the new endpoint at  $x$  would still have the three neighboring endpoints in  $B$ . The cap conclusion would then be even more immediate, but the proof would be using a different semantic route.Similarly, the matching condition used in the cap must apply to every added U or rotor source and must be source-local:Every endpoint of an added source has its matching endpoint among adjacent endpoints of that same source.Without source-local matching, one of the three prescribed neighboring endpoints could in principle serve as the mate, and the cap proof would not follow.Under the standard support-versus-endpoint semantics and source-local matching, the cap proof is sound.2. Five-endpoint cap2.1 Forcing  $x$  into the final endpoint unionThe prescribed support is
$$x=(2,2),$$
and the prescribed endpoint set contains
$$B=\{(1,2),(2,1),(3,2),(2,6),(1,4)\}.$$
The three points
$$(1,2),\quad (2,1),\quad (3,2)$$
are the three lattice neighbors of  $x$  that lie in  $B$ .If  $x\notin E$ , then  $x$  remains a mandatory selected support and has at least three occupied endpoint neighbors. Hence the support-neighbor condition fails. Therefore
$$x\in E.$$
Since  $x$  is not already an endpoint of the prescribed source subfamily, and endpoint ownership is disjoint, some added source  $C$  must own  $x$  as an endpoint.The only lattice neighbor of  $x$  not already occupied by a prescribed endpoint is
$$y=(2,3).$$
Consequently, source-local matching forces  $y$  to be an endpoint of the same added source  $C$ .This step is valid for arbitrary additional source counts and arbitrary translations. It does not use a placement cutoff.2.2 U sourcesFor a U source of even width at least six and even leg heights at least four:every nonterminal stem endpoint has two same-source endpoint neighbors;every bar endpoint has at least two same-source endpoint neighbors;the only endpoints with exactly one same-source endpoint neighbor are the two terminal tips.Therefore  $x$  must be a terminal tip of the added U.The vector from  $x$  to its matched neighbor  $y$  is
$$y-x=(0,1).$$
From a terminal tip, the stem continues in that direction toward the bar. Since the relevant leg height is at least four, the points
$$x,\ x+(y-x),\ x+2(y-x),\ x+3(y-x),\ x+4(y-x)$$
are all endpoints of the same U. In particular,
$$x+4(y-x)=(2,6)$$
is an endpoint of the added U.But  $(2,6)\in B$  is already an endpoint of a prescribed different source. This violates endpoint disjointness.Thus no added U can own  $x$ .This part is a genuine parameter-free geometric argument. The lower height bound is exactly what is used; no upper height, width, or translation bound is needed.2.3 Rotor sourcesFor a rotor, the only endpoints with exactly one same-source endpoint neighbor are the four outer endpoints. Fixing
$$x=(2,2),\qquad y=(2,3)$$
as the outer endpoint and its unique same-source endpoint neighbor determines the translation. The two possible chiral endpoint sets are the displayed sets
$$R_1=
\{(0,3),(1,3),(1,4),(1,5),(2,2),(2,3),(2,4),(3,4)\},$$
and
$$R_2=
\{(1,4),(2,2),(2,3),(2,4),(3,3),(3,4),(3,5),(4,3)\}.$$
Both contain
$$(1,4).$$
Since  $(1,4)\in B$ , either rotor chirality collides with a prescribed endpoint.Provided the stated two-chirality orbit lemma is part of the source definition, quarter-turns, reflections, and translations are fully covered. There is no hidden finite placement enumeration here.Cap conclusionThe five-endpoint cap is ACCEPTED, subject only to the semantic clarifications above:retained supports cannot simply be discarded;added endpoints obey the same source-local matching rule;endpoint disjointness applies to the final extension.The conclusion is genuinely uniform over the full U/rotor source class.3. Regular singleton activation and the injectionThis section has a valid geometric forcing step, but its activation sentence requires a definition.3.1 What the geometry forcesIn the normalized side configuration,
$$t=(3,2),\qquad a=(3,1),\qquad Q=\{2,3\}\times\{2,3\},$$
with producer endpoint
$$e=(2,1),$$
a regular singleton consumer with profile  $1P2T$  has original support
$$p=(2,2)$$
and original endpoint anchor
$$t=(3,2).$$
The support  $p$  has two occupied endpoint neighbors:
$$t=(3,2),\qquad e=(2,1).$$
If  $p\notin E$ , it remains a mandatory support and violates the at-most-one occupied-neighbor rule. Therefore
$$p\in E.$$
That implication is sound.3.2 The missing definition of “activated”The next sentence says:The consumer singleton is therefore activated.This is correct only if activation is defined at the occurrence level by support consumption, for example:
$$\operatorname{Act}(C)
\quad\Longleftrightarrow\quad
S_C\cap E\ne\varnothing,$$
where  $C=(\text{source},\text{tile})$  is an original singleton occurrence and  $S_C$  is its original support set.Under this definition,  $p\in E$  immediately implies  $\operatorname{Act}(C)$ , independently of which source owns the endpoint at  $p$ .If instead  $A$  counts only singleton sources that themselves own  $p$ , or only cases where the consumer source acquires a particular endpoint, the proof has a real gap. The forced endpoint at  $p$  could belong to an unrelated added U or rotor source. The width-six cap does not provide a general owner-exclusion theorem for arbitrary producer widths.Thus the proof must choose one of the following:Preferred repair: define activation as support consumption by the original singleton occurrence, independent of endpoint owner; orprove a separate source-owner uniqueness lemma showing that every endpoint occupying  $p$  must belong to the consumer source.The first option is the natural one and is sufficient for the stated ledger use.3.3 InjectivityThe intended map is
$$\{\text{marked positive gate sides}\}
\longrightarrow
\{\text{activated original positive singleton occurrences}\},$$

$$g\longmapsto C(g)=(\text{consumer source},\text{consumer tile}).$$
The injection is valid if the following are stated:a regular singleton tile has one relevant gate endpoint, so one tile occurrence cannot serve as two distinct gate incidences;distinct tile occurrences of one consumer source count separately;the “all original positive canonical tiles are distinct” fact is global over source/tile occurrences, not merely a statement that distinct producer shapes occupy different geometric regions.Then two different marked sides cannot map to the same  $(\text{source},\text{tile})$  occurrence. This remains true when several sides have the same consumer source, provided they use distinct tile occurrences.A small logical point should be made explicit: the seven-endpoint ring argument proves injectivity only if the rings being compared are the rings of the target tile occurrences in the map. If “donor tiles” refers only to producer-side tiles, then one still needs the incidence lemma connecting distinct producer gates to distinct consumer occurrences.With that occurrence-level interpretation, one obtains
$$q_+\le A.$$
3.4 Ledger algebraThe ledger identity is correct:
$$2R=A+U_0+Z_0+H.$$
Partitioning  $A$  into the  $q_+$  marked positive-singleton activations and the remaining activations gives
$$2R
=
q_+ +(A-q_+)+U_0+Z_0+H.$$
All terms on the right are nonnegative, so
$$2R\ge q_+.$$
Since  $R\in\mathbb Z_{\ge0}$ ,
$$R\ge \left\lceil\frac{q_+}{2}\right\rceil.$$
Using
$$\mu=N+R-G,$$
one obtains
$$\mu
\ge
N-G+\left\lceil\frac{q_+}{2}\right\rceil.$$
This calculation is correct.However, it is bookkeeping from the existing ledger rather than a new reserve mechanism. Since  $q_+\le A$ , the same identity already gives
$$2R\ge A\ge q_+,$$
and therefore
$$R\ge \left\lceil\frac A2\right\rceil
\ge
\left\lceil\frac{q_+}{2}\right\rceil.$$
So the geometric work establishes the useful fact  $A\ge q_+$ , but one should not describe  $q_+$  as an additional contribution added on top of the existing  $A$ -term. The text correctly warns against double spending; the formal statement should preserve that caution.Activation verdictThe support-forcing geometry is ACCEPTED.The activation injection is REVISE, unless the pre-existing definition of  $A$  already explicitly counts support-consumption activations of  $(\text{source},\text{tile})$  occurrences independently of endpoint ownership.This issue does not affect the five-endpoint cap.4. Width-six regular singleton exclusionFor a width-six producer, the regular singleton profile  $1P2T$  has support
$$p=(2,2),$$
while the producer supplies endpoints
$$(1,2),\quad (2,1),\quad (2,6),\quad (1,4),$$
and the consumer supplies endpoint
$$t=(3,2).$$
Thus the five points are exactly
$$B=\{(1,2),(2,1),(3,2),(2,6),(1,4)\}.$$
The support  $p$  is not already an endpoint of the prescribed sources. The cap therefore excludes every complete extension, regardless of whether the endpoint that would cover  $p$  belongs to the consumer or to a third source.Consequently:width-six positive regular singleton gate consumers are excluded;width-six zero-rotor regular singleton consumers are excluded as well, provided they have the same  $p,t$  local stencil.This part is ACCEPTED once the cap semantics are made explicit.The reciprocal pair is a valid illustrative instance if the second gate is understood as the image of the opposite-side support of the first U. It is not needed for the general theorem. The proof should specify which original support maps to  $(4,1)$ , since applying the displayed affine map to  $(3,2)$  itself gives a different point.5. Width-six positive consumers: regular pairsThe positive profile catalogue gives the three cases
$$1P2T,\qquad 2P1T,\qquad 4P0T.$$
The  $1P2T$  case is already excluded by the cap.The  $2P1T$  case is mostly correct, but the final regular-pair continuation must be stated as a separate structural lemma.Let
$$p=(2,2),\quad r=(2,3),\quad t=(3,2),\quad u=(3,3).$$
The complete support placements are as follows.Consumer endpoints in  $Q$ Support in  $Q$ Status $\{t,p\}$  $r$  or  $u$  $p$  has only one same-source endpoint neighbor, namely  $t$ ; hence  $p$  would be a terminal tip, but a positive terminal has singleton profile $\{t,u\}$  $p$ five-endpoint cap $\{t,u\}$  $r$  $p$  is blank; continuation lemma forces  $(3,1)=2t-u$  to be a consumer endpoint, colliding with the producer anchorThis does exhaust the regular-pair support placements, assuming the stated profile catalogue already proves that the second endpoint must be  $p$  or  $u$ .The first row is sound:  $p$ 's other lattice neighbors  $(1,2)$  and  $(2,1)$  are producer endpoints, so  $p$  has only  $t$  as an endpoint neighbor belonging to the consumer. A positive U endpoint with exactly one same-source endpoint neighbor is a terminal tip, and the catalogue says terminal tips have the singleton profile rather than  $2P1T$ .The second row is exactly the cap.The third row needs the following lemma.Required regular-pair continuation lemmaFor a positive U, suppose  $t$  and  $u$  are adjacent endpoints of a regular pair,  $p$  is the other intratile neighbor of  $t$ , and  $p$  is blank. Then
$$2t-u$$
is also an original endpoint of that U.This is a structural classification, not a finite placement enumeration:for a straight stem pair, the stem continues through the reflected point;for a bar-interior pair, the bar continues through the reflected point;for a bar-end pair, the positive U support/endpoint pattern determines which side is blank; in the blank- $p$  orientation, the reflected point is the first stem endpoint;the alternative bar-end orientation has a support at the relevant corner and therefore does not produce the  $p$ -blank case.The current text asserts this classification, but it does not show enough of the normalized U endpoint/support data to make the bar-end case independently checkable. If the “stated profile catalogue” is an admitted hypothesis containing precisely this role classification, cite that catalogue directly. Otherwise, add this lemma and prove the three geometric role cases from the normalized U definition.Once the lemma is stated, it gives
$$2t-u=(3,1),$$
which is the producer anchor and therefore an endpoint collision.Thus the regular-pair part is REVISE for exposition and a missing local lemma, but it does not appear to require a new global idea or finite enumeration.6. Width-six  $4P0T$  bars and the parity problemThe horizontal-bar argument is sound.If the consumer’s  $4P0T$  tile is part of a horizontal two-wide bar, then the bar occupies rows  $2$  and  $3$ , because  $Q$  contains all four endpoints in those rows. Its long-axis interval has even length at least six and contains columns  $2$  and  $3$ . Therefore it must contain column  $1$  or column  $6$ :if its left endpoint is at most  $1$ , it contains column  $1$ ;if its left endpoint is  $2$ , length at least six forces its right endpoint to be at least  $7$ , so it contains column  $6$ .Hence it collides with a producer stem endpoint at row  $2$  or  $3$ .The vertical-bar argument as written is not valid.6.1 The parity assertion is false under the stated isometriesThe text claims that the positive phase forces the long-axis interval to start at an odd coordinate and end at an even coordinate after every allowed reflection or rotation.That is not invariant under the allowed quarter-turns.Take the canonical phase- $00$  U and apply
$$g(r,c)=(-c,r).$$
Its horizontal bar becomes a vertical bar whose long-axis interval is
$$\{-w,\ldots,-1\}.$$
For even  $w$ , this starts at an even coordinate and ends at an odd coordinate. Translating by the even vector  $(w+2,2)$  gives a vertical bar on
$$\{2,\ldots,w+1\}\times\{2,3\}.$$
This translation is compatible with the usual two-periodic tiling preservation, yet the long-axis interval starts at  $2$ , not at an odd coordinate, and it does not intersect the producer bar at row  $1$ .Therefore the statement“The odd-start/even-end assertion holds after any tiling-preserving reflection or rotation”is false unless “tiling-preserving isometry” is given a much narrower definition that excludes this ordinary quarter-turn and even translation. That restriction is not stated and would conflict with the earlier allowance of all isometries and translations.This is a genuine gap in the  $4P0T$  vertical-bar proof.6.2 Direct repair without parityThe corollary can be repaired uniformly, without enumeration and without restricting the source class.Write the vertical bar's long-axis interval as
$$I=[L,L+w-1],
\qquad w\ge 6,$$
and suppose it contains rows  $2$  and  $3$ . Then necessarily
$$L\le 2.$$
There are two cases.Case 1:  $L\le 1$ Then row  $1$  lies in the consumer bar. Since the bar occupies columns  $2$  and  $3$ , it contains consumer endpoints at
$$(1,2)\quad\text{and}\quad(1,3),$$
which collide with the producer's original bar endpoints.Case 2:  $L=2$ One end of the vertical bar is at row  $2$ . At that bar end, one of the U's horizontal legs is attached. In a U geometry, a left-going leg starts at the outer bar column and proceeds through column  $1$ , while a right-going leg starts at the outer bar column and proceeds through column  $6$ . The minimum even leg height  $4$  is more than enough to reach one of those columns.Thus the consumer contains either
$$(2,1)
\quad\text{or}\quad
(2,6),$$
both of which are producer stem endpoints.This proves the vertical  $4P0T$  exclusion for every translation, reflection, and quarter-turn. It uses only the actual U geometry and the minimum leg-height bound.The proof should replace the parity paragraph by this two-case interval/stem lemma.7. Status of the claimed consequencesAfter the above repairs, the conclusions have the following status.ClaimStatusFive-endpoint cap for every finite U/rotor extensionACCEPT, with explicit support-role and source-local matching semanticsWidth-six exclusion of regular  $1P2T$  singleton consumersACCEPT, by the capWidth-six exclusion of zero-rotor regular singleton consumersACCEPT, assuming the same local stencil $q_+\le A$ ACCEPT only if  $A$  counts occurrence-level support activations; otherwise REVISE with an owner lemmaInjectivity when several sides use one consumer sourceACCEPT once tiles are counted as distinct source/tile occurrences and the global tile-distinctness statement is usedLedger inequality  $\mu\ge N-G+\lceil q_+/2\rceil$ ACCEPTClaim that  $q_+$  is an additional reserve beyond the existing  $A$ -termREJECT this interpretation; it is already contained in the exact ledgerWidth-six exclusion of positive  $2P1T$  consumersREVISE, requiring the explicit regular-pair continuation lemmaWidth-six exclusion of positive  $4P0T$  consumersREVISE as written, because the parity argument fails; repairable by the direct stem-collision lemmaEvery positive-to-positive gate incidence has producer width at least eightNot established by the present text, but follows after the pair-continuation and vertical-bar repairsTherefore the proper manuscript-level disposition is:REVISE, not REJECT.The cap theorem and width-six singleton obstruction are valid geometric results. The activation injection needs an explicit occurrence-level activation definition. The positive-consumer width-six corollary requires a local regular-pair lemma and replacement of the false/unjustified vertical-bar parity argument by a direct interval-and-stem proof.No part of this audit establishes unrestricted  $\mu\ge0$ , directed acyclicity, a global sign restriction on positive consumers, or rectangular-grid equality.
