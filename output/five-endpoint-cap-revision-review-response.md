Verdict: REVISE, narrowlyThe substantive geometric repairs are successful:the five-endpoint cap is now sound under the explicit support/endpoint and source-local matching semantics;the activation quantity  $A$  is now defined in the correct owner-independent,  $(\text{source},\text{tile})$ -occurrence sense;the canonical-tile injection is substantially clarified;the complete positive regular-pair table closes the previous local-classification gap;the vertical  $4P0T$  argument is correctly repaired by the interval/stem collision proof;the reciprocal example now identifies the correct right reference gate.The two new consequences are also mathematically plausible and, with one remaining finite-role certificate, lead to the claimed width-six sign conclusion.I nevertheless give REVISE rather than ACCEPT for the full written package because two written obligations remain:the definition of  $P$  is still literally inconsistent with later uses of  $P$  as the final endpoint union; and  the new rotor consequence asserts that the two surviving gate roles have support  $p=(2,2)$ , but the revised note does not display the normalized rotor support data or the two inverse-coordinate checks needed to verify that assertion.These are local, repairable obligations. They do not undermine the five-endpoint cap, the singleton activation argument, or the positive-U exclusion once corrected.1. The  $P/T$  semantics are conceptually fixed, but  $P$  is still defined too narrowlyThe revised text says:Precisely,  $P$  is the union of original endpoint sets …It then says:A consumed original support belongs to  $P$  and is no longer selected.Those two sentences are not literally compatible if “original endpoint sets” means only endpoints already present before added sources are introduced. A consumed support such as  $p$  becomes an endpoint of an added source, so it belongs to the final endpoint union, but generally not to the union of the originally prescribed endpoint sets.The intended definition must be something like
$$P:=E_{\mathrm{final}}
 =\bigcup_{C\in\mathcal C_{\mathrm{selected}}} E(C),$$
where the union ranges over all selected source occurrences, including added U and rotor sources.Then define
$$T\subseteq S_{\mathrm{original}}\setminus P$$
together with any permitted optional selections, with  $T\cap P=\varnothing$ .The support constraint is
$$z\in T
\quad\Longrightarrow\quad
\#\bigl(N(z)\cap(P\cup T)\bigr)\le 1.$$
The occupied set is  $P\cup T$ .With this correction, the sentence “a consumed original support belongs to  $P$  and is no longer selected” is precise, and all subsequent arguments work as intended.This is a notation/definition defect rather than a geometric counterexample, but it should be corrected before claiming a fully closed written proof.2. The five-endpoint cap is now acceptedAfter the semantic repair above, Section 1 is sound.Let  $x=(2,2)$  and
$$B=\{(1,2),(2,1),(3,2),(2,6),(1,4)\}.$$
The three points
$$(1,2),\ (2,1),\ (3,2)$$
are occupied neighboring endpoints of  $x$ .If  $x\notin P$ , then  $x$  remains a mandatory support in  $T$ , and it has at least three occupied neighbors. Hence  $x\notin T$  is impossible. Therefore  $x\in P$ , and since no prescribed source owns  $x$  as an endpoint, an added source must own  $x$ .The only lattice neighbor of  $x$  not already occupied by a prescribed endpoint is
$$y=(2,3).$$
The explicit source-local matching rule forces  $y$  to be an endpoint of the same added source.U caseThe only U endpoints with exactly one same-source endpoint neighbor are terminal tips. A terminal-to-bar stem contains the successive endpoints
$$x+j(y-x),\qquad 0\le j\le 4,$$
because the relevant even leg height is at least four. Thus the added U owns
$$x+4(y-x)=(2,6),$$
which is already a prescribed endpoint in  $B$ . This contradicts endpoint disjointness.The argument is independent of maximum width, maximum height, translation bounds, or source count.Rotor caseThe source-local degree-one roles are the four outer rotor endpoints. Once  $x=(2,2)$  and  $y=(2,3)$  are fixed, the two chiral endpoint sets listed in the note are the complete role cases. Both contain  $(1,4)$ , another prescribed endpoint in  $B$ .The quarter-turn/reflection role reduction is legitimate because the rotor template has finitely many endpoint roles and the translation is fixed once  $x$  and  $y$  are fixed. This is not a bounded placement search.Therefore the cap theorem is ACCEPTED, subject to replacing the definition of  $P$  by the final endpoint union.3. The singleton activation argument is now soundThe revised activation definition fixes the principal issue from the earlier version.For an original regular singleton occurrence  $C=(j,Q)$ , activation is defined by
$$\operatorname{Act}(C)
\quad\Longleftrightarrow\quad
(T_j\cap Q)\cap P\ne\varnothing,$$
independently of which source owns the endpoint in  $P$ .In the normalized configuration, the support
$$p=(2,2)$$
has occupied endpoint neighbors
$$t=(3,2)
\quad\text{and}\quad
(2,1).$$
If  $p\notin P$ , then  $p\in T$  by mandatory support retention and violates the at-most-one-neighbor rule. Hence  $p\in P$ , and the singleton occurrence is activated under the revised definition.This implication is now valid even if an unrelated third source owns the endpoint at  $p$ .Occurrence-level injectionThe map should be read as
$$\{\text{marked sides}\}
\longrightarrow
\{\text{activated original singleton occurrences}\},$$

$$s\longmapsto (j_s,Q_s).$$
The revised explanation that the target occurrence uses the same physical tile  $Q$  as the producer canonical side is the right argument:the consumer’s sole relevant endpoint is the gate  $t$ ; $t$  lies in the physical tile  $Q$ ;the physical tiling assigns  $t$  to that unique tile;therefore the consumer occurrence is labelled by that same  $Q$ .If two marked sides mapped to the same  $(j,Q)$ , their producer canonical tiles would be the same physical tile. The assumed global distinctness of original positive canonical tiles then identifies the original sides. Hence the map is injective, even when multiple tiles belong to the same source.Thus
$$q_+\le A$$
is justified, provided “all original positive canonical donor tiles are distinct” is understood globally over source/tile occurrences, as the revised text does.LedgerThe ledger calculation remains correct:
$$2R
=q_+ +(A-q_+)+U_0+Z_0+H
\ge q_+.$$
Since  $R$  is an integer,
$$R\ge \left\lceil \frac{q_+}{2}\right\rceil,$$
and therefore
$$\mu=N+R-G
\ge
N-G+\left\lceil\frac{q_+}{2}\right\rceil.$$
The text is also correct that this does not create a second copy of the  $A$ -reserve. Since  $q_+\le A$ , the exact ledger already implies
$$R\ge \left\lceil \frac A2\right\rceil
\ge \left\lceil \frac{q_+}{2}\right\rceil.$$
The geometric content is the occurrence-level lower bound  $A\ge q_+$ , not an extra additive term beyond  $A$ .This section is now ACCEPTED after the  $P$ -notation correction.4. The forced transverse negative U is valid, with two small clarificationsThe new consequence is essentially correct.Assume a canonical gate consumer has original support
$$p=(2,2).$$
The producer and consumer provide the three persistent neighboring endpoints
$$(1,2),\quad (2,1),\quad (3,2).$$
The note should explicitly state that  $p$  is not already an endpoint of either prescribed source:it is an original support of the gate consumer, hence not one of that source’s endpoints;it lies in the producer’s empty canonical tile, hence is not a producer endpoint.With that understood,  $p$  must be covered by a third source.The only possible same-source neighbor of a new endpoint at  $p$  is
$$(2,3).$$
Rotor exclusionThe four blockers
$$(1,2),\quad (2,1),\quad (3,2),\quad (1,4)$$
already exclude both rotor outer-role endpoint sets from the cap argument. The fifth point  $(2,6)$  is unnecessary for this rotor exclusion.Therefore the third source must be a U.Because  $p$  has exactly one possible same-source endpoint neighbor, it is a terminal tip, and the stem points right. If  $h$  is the relevant even leg height, the U contains
$$(2,2+j),\qquad 0\le j\le h.$$
The producer has endpoint  $(2,w)$ . Hence the forced U cannot reach column  $w$ , so
$$h<w-2.$$
Since  $h,w$  are even,
$$4\le h\le w-4.$$
Consequently,
$$w\ge 8.$$
That height arithmetic is correct.Negative signThe forced source has both  $p=(2,2)$  and its matching-side neighbor  $(2,3)$  in the same physical tile. By the stated positive catalogue, a positive U terminal is an original regular singleton and does not have this two-endpoint terminal profile. Therefore the forced U is negative.This conclusion is valid assuming the positive/negative phase classification is invariant under the allowed tiling-preserving isometries, as the source model states.The sentenceNo endpoint ownership is changed in this argumentshould be rephrased. The support  $p$  is in fact newly covered by the third source and therefore changes role from support to endpoint. What remains unchanged is the ownership of the already existing prescribed endpoints. A more precise sentence would be:No existing prescribed endpoint is reassigned; the argument only forces a new source to cover  $p$ .With that wording change, the forced transverse negative-U consequence is ACCEPTED.5. The new rotor gate-owner consequence is only conditionally closedThe endpoint-role part of the argument is correct.The producer’s seven fixed endpoints are
$$E_{\mathrm{prod}}
=
\{(1,1),(1,2),(1,3),(1,4),(2,1),(3,1),(4,1)\}.$$
For a rotor endpoint placed at  $t=(3,2)$ , there are eight translation roles for the reference chirality and eight reflected roles.From the displayed reference endpoint set, the only roles whose complete endpoint sets avoid  $E_{\mathrm{prod}}$  are indeed:
$$R_+(2,0)
\quad\text{and}\quad
R_-(1,6).$$
The endpoint part can be checked structurally without a search cutoff: $R_+(2,0)$  is the role in which reference endpoint  $(1,2)$  maps to  $t$ ; $R_-(1,6)$  is the role in which reference endpoint  $(2,4)$  maps to  $t$ ;every other role contains one of the seven producer endpoints.However, the next assertion is not independently established in the written note:Both have original support  $p=(2,2)$ .To verify this, the normalized rotor support set must be displayed, or the two inverse-coordinate calculations must be written.For  $R_+(2,0)$ ,
$$p-(2,0)=(0,2),$$
so one needs
$$(0,2)\in S_{\mathrm{rotor}}^{+}.$$
For  $R_-(1,6)$ , with
$$(r,c)\mapsto (r+1,-c+6),$$
the inverse image of  $p=(2,2)$  is
$$(r,c)=(1,4),$$
so one needs
$$(1,4)\in S_{\mathrm{rotor}}^{\mathrm{ref}}.$$
If those two support memberships are part of the normalized rotor support catalogue, then the claim is proved. The note should add a small table:surviving rolegate reference endpointinverse image of  $p$ support fact $R_+(2,0)$  $(1,2)$  $(0,2)$  $(0,2)$  is a rotor support $R_-(1,6)$  $(2,4)$  $(1,4)$  $(1,4)$  is a rotor supportThe finite role exhaustion itself is acceptable and does not violate the prohibition on replacing general geometry by bounded enumeration: rotor roles are a fixed finite structural catalogue, and translations are uniquely determined by placing the gate at  $t$ . But the support-membership step must be visible in the written proof.Until that table or equivalent support calculation is included, the statement
$$\text{“every surviving rotor gate role has support }p\text{”}$$
is an unverified premise.This affects the new rotor consequence and the final width-six sign conclusion, but not the cap theorem.6. The positive-U exclusion is now closedThe revised positive regular-pair table resolves the earlier gap.The table gives all regular positive pair types:the two bar-end configurations;the two straight stem configurations.For each, the support/blank ordering forces the reflected continuation endpoint. The parameter ranges ensure that the continuation exists even for the pair immediately preceding a terminal singleton.This is a structural role classification over arbitrary even dimensions, not finite enumeration over placements. It transports under the unrestricted allowed isometries.The  $4P0T$  argument is also now correct:a horizontal bar containing columns  $2,3$  and having length at least six reaches column  $1$  or  $6$ , hence hits a producer stem;a vertical bar with interval  $[L,L+v-1]$ ,  $v\ge6$ , containing rows  $2,3$  has  $L\le2$ ;if  $L\le1$ , it hits the producer row-one bar;if  $L=2$ , the row-two stem reaches  $(2,1)$  or  $(2,6)$ .This proof no longer relies on a false parity invariant and covers arbitrary translations and rotations.Thus, assuming the stated positive profile catalogue, the positive-U exclusion is ACCEPTED.7. Final width-six conclusionThe desired conclusion is:
$$\text{Every width-six actual gate consumer is a negative U source.}$$
The logic is now:Positive  $1P2T$  consumers are excluded by the five-endpoint cap.Positive  $2P1T$  consumers are excluded by the complete continuation table and the cap.Positive  $4P0T$  consumers are excluded by the horizontal/vertical interval-and-stem argument.Rotor gate owners are reduced to the two surviving endpoint roles.If both surviving rotor roles have support  $p=(2,2)$ , the forced transverse-U argument gives  $w\ge8$ , excluding them for a width-six producer.Therefore the only possible width-six gate consumers are negative U sources.Steps 1–3 are now established. Step 5 is established once the two rotor support memberships are explicitly recorded. Therefore the final sign conclusion is conditionally valid, but the full package remains REVISE until that finite rotor support certificate is written.8. Overall statusComponentStatusFive-endpoint capACCEPT, after defining  $P$  as the final endpoint unionSource-local matching useACCEPTOwner-independent activationACCEPTCanonical physical-tile injectionACCEPT, assuming global tile-occurrence distinctnessLedger inequalityACCEPTForced transverse negative UACCEPT, with explicit  $p\notin$  existing endpoint sets and clearer ownership wordingPositive regular-pair exclusionACCEPTPositive  $4P0T$  exclusionACCEPTSixteen rotor gate-owner endpoint rolesACCEPTTwo surviving rotor roles have support  $p$ REVISE: display support set/preimage tableEvery width-six actual gate consumer is negative UConditional on the rotor support tableFull  $\mu\ge0$  allocation theoremOpenRectangular-grid equalityOpenSo the appropriate disposition is:REVISE, with only local remaining obligations.Correct the definition of  $P$ , display the two normalized rotor support checks for  $R_+(2,0)$  and  $R_-(1,6)$ , and rephrase the endpoint-ownership sentence. After those changes, the full revised geometric package should be accepted under the inherited source model and exact reserve ledger.

