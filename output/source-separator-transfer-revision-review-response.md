ACCEPTThe two corrections resolve the reasons for my previous REVISE verdict. The inherited geometric theorem supplies  $R(J)\ge0$  for the actual complete feasible separator restrictions, and the revised negative-branch paragraph now distinguishes the two deletion criteria correctly.This acceptance is for the revised separator note, under its stated inherited constructor, catalogue, source-ledger, and rotor-bridge inputs. I checked the supplied reserve proof through the local classification and global cancellation needed for this application. I have not relied on its reported prior acceptance or certified any execution.1. The inherited theorem concerns exactly the same reserveThis identification is essential because the separator note uses
$$R(I)=S(I)+2|F_{\mathrm{mix}}(I)|-|E(I)|,$$
whereas the inherited theorem writes
$$R(I)=S(I)+C(I)-K(I),$$
with  $K$  counting only irregular events.Partition the actual source-labelled events by their tail’s original tile profile:
$$E(I)=E_{\mathrm{reg}}(I)\mathbin{\dot\cup}E_{\mathrm{irr}}(I).$$
Regularity here is a property of the original profile, not the sign of its source. In particular, a negative source’s  $2P1T$  or  $3P0T$  profile remains regular.The regular profiles have the following event behavior: $1P2T$ : no intratile event. Both adjacent corners are in the source’s original occupied set, even if foreign endpoints consume those supports. $2P1T$ : at most one event, into the remaining corner outside its original occupied set. If that event occurs, the original support corner has two distinct occupied neighbors: its original anchor and the newly occupied event target. Feasibility forces that support corner to be consumed too. Thus the tile becomes full. $3P0T$ : filling the missing corner produces exactly two regular events and makes the tile full. $4P0T$ : no event.Consequently, every regular event occurs in a mixed full tile. The inherited residual-credit table is exactly
$$c_Q=2\,\mathbf 1_{\{Q\in F_{\mathrm{mix}}(I)\}}
      -e_{\mathrm{reg}}(Q).$$
For clarity, its full-tile values are:Original-owner partitionRegular eventsResidual credit  $c_Q$  $4$ , originally full $0$  $0$  $3+1$  $2$  $0$  $2+2$ , with  $t$  irregular pairs $2-t$  $t$  $2+1+1$ , with irregular-pair indicator  $t$  $1-t$  $1+t$  $1+1+1+1$  $0$  $2$ Nonfull tiles have no regular events and no full-tile credit. Summing gives
$$C(I)=2|F_{\mathrm{mix}}(I)|-|E_{\mathrm{reg}}(I)|.$$
Since  $K(I)=|E_{\mathrm{irr}}(I)|$ ,
$$\begin{aligned}
S(I)+C(I)-K(I)
&=S(I)+2|F_{\mathrm{mix}}(I)|
  -|E_{\mathrm{reg}}(I)|-|E_{\mathrm{irr}}(I)|\\
&=S(I)+2|F_{\mathrm{mix}}(I)|-|E(I)|.
\end{aligned}$$
There is therefore no change of reserve, missing regular-event debit, or additional use of full-tile credit when the separator note invokes the inherited theorem.2. The supplied local defect proof supports the required nonnegativityThe local classification in inherited §2 checks out under the stipulated profile catalogue and mandatory-support rule.The important feasibility steps are valid:Two diagonal singleton endpoints are impossible in a nonfull tile. Each singleton requires an adjacent intratile original support. That corner is not either diagonal endpoint, remains selected, and sees both endpoints.Two adjacent singleton endpoints cannot retain both remaining corners as supports. Those corners are adjacent, so each would have an endpoint neighbor and an additional occupied support neighbor. This forces precisely the regular/irregular and mutual/nonmutual irregular alternatives listed.With three endpoints, the missing corner cannot retain an original support, because it sees two endpoints. This forces the support orientations used in both the pair-plus-singleton and three-singleton cases.The regular-pair argument above establishes that a regular event cannot remain on a nonfull tile.The full cases also have the stated defect values. In particular, the potentially delicate  $3+1$  case with an irregular singleton has
$$i=b=k=1,\qquad c=d=f=0,$$
because the original triple’s two regular events have already exhausted the mixed full-tile credit. Thus
$$\Lambda=1+1-2=0,$$
as claimed. It would be incorrect to assign additional residual full-tile credit here; the supplied proof does not do so.The remaining full cases give respectively  $\Lambda=0$ ,  $\Lambda=d$ , and  $\Lambda=d$ , with the stated  $f$ , so every full tile has  $h_Q=0$ . The nonfull cases give exactly the four listed defect classes and weights. Hence
$$H=\Lambda+F_U+F_R-A-D_R.$$
For the global step, the retained source-catalogue and pairing inputs give
$$U_0=2B_{11}-B_U-F_U,\qquad
Z_0=D_R-B_R-F_R.$$
The second identity needs only the stated implication
$$\text{paired triple is filled}\Longrightarrow
\text{paired singleton activates},$$
together with the bijection. It does not require the converse.Substitution yields
$$\begin{aligned}
A+U_0+Z_0+H
&=A+(2B_{11}-B_U-F_U)+(D_R-B_R-F_R)\\
&\quad+\Lambda+F_U+F_R-A-D_R\\
&=2B_{11}-B_U-B_R+\Lambda\\
&=2R.
\end{aligned}$$
Thus
$$\boxed{
R=\frac{A+U_0+Z_0+L_1+2L_{2\mathrm{bar}}
                 +2L_{2\mathrm{mutual}}+L_3}{2}\ge0.
}$$
This derivation uses neither allocation nonnegativity nor minimum-counterexample reasoning. It also handles the simultaneous occurrence counts by exact cancellation, rather than asserting that different labels independently supply additional capacity.The exhaustive triple-owner classification, the phase- $11$  U triple count, the rotor pairing/support bridge, and the half-slot source identity remain the explicitly inherited source inputs. They are not consequences of the numerical profile labels alone.3. The separator restrictions satisfy the inherited theorem’s hypothesesThe application in revised §5 is valid because §2 establishes actual complete feasible restrictions, including all mandatory restorations.For either restriction  $J$ :It contains finitely many whole original U/rotor sources.Its endpoint set and matching are the unions of those retained sources’ original endpoint sets and unchanged matching edges.Endpoint ownership remains disjoint.Its occupied set is exactly  $\bigcup_{i\in J}O_i$ .Every retained original support outside the retained endpoint union is restored.The two-step consumption proof establishes the required selected-vertex occupied-neighbor condition after those restorations.Original dimensions, phases, isometries, profile labels, and support data remain unchanged.The physical tile partition remains fixed.Original singleton–triple pairings remain intact because entire owners are retained.Activation, fullness, and defect counts are then recomputed from the restriction’s actual endpoint union. They need not retain their full-family values; the reserve theorem applies anew to that complete feasible restriction.There is no additional connectedness, saturation, width, gate, or single-positive-source hypothesis in inherited §§1–3. In particular, the revised argument does not depend on the later saturation consequences in inherited §4.4. All stated minimum-counterexample reductions now followLet  $F$  have negative margin and the least number of original sources among such complete feasible families. Both separator restrictions are proper because  $A,B\ne\varnothing$ , so minimality gives
$$\mu(L)\ge0,\qquad \mu(\mathrm{Right})\ge0.$$
The unchanged exact identity is
$$\mu(F)=\mu(L)+\mu(\mathrm{Right})-N_s-S_s+d_s.$$
Zero-charge articulation. Here  $N_s=S_s=d_s=0$ , so the full margin is the sum of two nonnegative margins. The exclusion follows.Positive articulation with a duplicated canonical-side mark. Here  $N_s=1$ ,  $S_s=0$ . If  $d_s\ge1$ ,
$$\mu(F)=\mu(L)+\mu(\mathrm{Right})+(d_s-1)\ge0.$$
Applying this to component partitions after deleting  $s$  gives the stated restriction: each separator side can be marked from at most one branch in a minimal counterexample. Multiple witnesses within that branch remain permitted.Unmarked positive branch with no other positive source. For such a branch  $J$ ,
$$N(J)=1,\qquad G(J)=0,\qquad \mu(J)=1+R(J)\ge1.$$
There is no duplicated separator mark. If  $K$  is the complementary restriction,
$$\mu(F)=\mu(J)+\mu(K)-1=R(J)+\mu(K),$$
so
$$\boxed{\mu(K)=\mu(F)-R(J)\le\mu(F)<0.}$$
This is a smaller counterexample, contradicting minimality. The previously unresolved  $R(J)=-1$  possibility is excluded by the inherited geometric theorem.Negative articulation. The shared mass still has to be paid:
$$\mu(F)\ge0
\quad\Longleftrightarrow\quad
\mu(L)+\mu(\mathrm{Right})\ge S_s.$$
For a branch  $J$  without positive sources,  $\mu(J)=R(J)$ , and
$$\boxed{\mu(K)=\mu(F)+S_s-R(J).}$$
Therefore the revised distinctions are exact:
$$\mu(K)\le\mu(F)
\quad\Longleftrightarrow\quad
R(J)\ge S_s,$$
whereas, for a specified negative full margin,
$$\mu(K)<0
\quad\Longleftrightarrow\quad
R(J)>S_s+\mu(F).$$
The inherited bound  $R(J)\ge0$  does not automatically supply the stronger shared-mass bound  $R(J)\ge S_s$ . The note correctly leaves that geometric obligation open.5. Scope of this acceptanceThe event and mixed-full-tile partitions, the actual mark-OR argument, the positive  $+d_s$  correction, and the multibranch subtraction formulas remain valid under the stated hypotheses. The newly supplied reserve dependency completes the formerly unsupported positive-branch reduction.The formalization boundary also remains accurate: the three separator Lean results concern abstract restriction feasibility, event coverage, and event disjointness. The physical catalogue application, tile and mark counting, inherited reserve identity, and counterexample reductions are written mathematics here. This ACCEPT does not certify compilation, axiom audits, controls, or physical fixture reconstruction.The revised note establishes the claimed structural reductions. It does not establish the unrestricted mixed U/rotor allocation inequality or rectangular-grid equality.
