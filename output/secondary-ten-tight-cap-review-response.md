Verdict: REVISE — one missing placement declarationThe new general tight-cap theorem and the narrow-cap complete-family exclusion pass this mathematical audit. Their endpoint-role classification, unbounded collision arguments, source charges, and directed-event counts are correct on the stated parameter ranges. The older pair-compensation and negative-marginal identities also check.The required repair concerns the  $T_2/Z$  insertion-order paragraph: the supplied package gives  $T_2$ ’s dimensions but refers to an omitted note for its placement. Dimensions alone do not determine its contacts or its marginal. With the explicit placement below, all four entries in that paragraph are correct.This is an ordinary mathematical review of the supplied definitions and readable proofs. I have not executed the reported checkers or Lean.1. Required repair: define  $T_2$ , and make its interaction receipt explicitInsert the following declaration into the insertion-order paragraph:
$$\boxed{
T_2=U(w+10,10,4),\qquad
T_2(r,c)=(a-8+r,\;w+13-c).
}$$
For clarity, also spell out the rotor transformation already identified by its stated consumed sites:
$$\boxed{
Z(r,c)=(a+2-r,\;w+12+c)
}$$
applied to the supplied standard rotor.Under this  $T_2$  placement, direct general counting gives
$$q(T_2)=-(w+9),\qquad
\Delta F(T_2\mid A)=\frac w2+5,\qquad
\Delta E_v(T_2\mid A)=2w+19,$$
and therefore
$$\Delta\Phi(T_2\mid A)
=(w+9)+2\left(\frac w2+5\right)-(2w+19)=0.$$
The  $T_2/Z$  mixed interaction consists of both:One jointly completed mixed full tile, at  $(a-1,w+12)$ .One additional surviving directed event,
$$T_2:(a-1,w+12)\longrightarrow Z:(a-1,w+13).$$
The reverse direction is excluded because  $(a-1,w+12)$  is an original support of  $Z$ . Consequently the mixed second difference is
$$\boxed{2\cdot1-1=1}.$$
This proves the stated insertion table:Insertion $\Delta\Phi$  $T_2$  into  $A$  $0$  $Z$  into  $A$  $1$  $Z$  into  $A+T_2$  $2$  $T_2$  into  $A+Z$  $1$ I recommend adding the displayed directed event to the prose. Saying only that their joint presence fills the tile leaves the reader to reconstruct the one-event debit that reduces the full-tile contribution from two to one.This is a missing-definition issue, not a counterexample to the intended identity. With the displayed placement inserted, I find no remaining blocking mathematical issue in the package.2. The mandatory-support argument and the complete consumer catalogue are soundThroughout, take a tile to be
$$T(R,C)=\{R,R+1\}\times\{C,C+1\},
\qquad R,C\in2\mathbb Z.$$
Since  $a$  is odd, all the displayed lower-corner rows  $a+\text{odd}$  have the required even phase.The persistent pair  $e,t$ The points
$$e=(a,w+14),\qquad t=(a+1,w+14)$$
are original supports of  $E$  and  $C$ , respectively. Their original endpoint anchors are
$$(a,w+13)\in E,\qquad (a+2,w+14)\in C.$$
Each support therefore has its own anchor and the other member of the adjacent support pair as occupied neighbors. Under the stated retention convention, consumption does not remove either occupied site.Thus both must be consumed in a complete extension. This conclusion does not require distinct consumers and does not create two independent numerical credits.The forced point  $p$ For
$$p=(a+2,w+12),$$
the inverse  $V$ -coordinates are  $(8,0)$ . Hence  $p$  is precisely an original even-indexed near lateral support of  $V$ , anchored at
$$(a+2,w+11)\in V.$$
The other specified occupied neighbors are
$$(a+2,w+13)\in E,\qquad
(a+3,w+12)\in E.$$
The point  $p$  is absent from the endpoint sets of  $A+K_s$ . If it remained unconsumed, it would have three occupied neighbors, contradicting the requirement that its occupied neighbor be exactly its original anchor. Therefore an additional original must own  $p$ .Its original matching partner must be north of  $p$ , because the west, east, and south sites already have foreign endpoint owners.Why this exhausts all endpoint rolesFor every legal canonical  $U$ :The two leg terminals have exactly one neighboring endpoint of their own original.Interior leg endpoints have two.The outer corners of bar row zero have two.The remaining bar endpoints have three.These facts are preserved by every translation and  $D_4$  transformation. An endpoint with two or more own endpoint neighbors cannot occupy  $p$ , since only its north neighboring site remains available to that original.Thus a  $U$  consumer must be a north terminal. After exchanging the leg labels when necessary, the two frames in the notes are exhaustive:
$$J_{\mathrm{right}}(r,c)
=(a+2-d+r,w+11+c),$$

$$J_{\mathrm{left}}(r,c)
=(a+2-d+r,w+13-c).$$
For the standard rotor, the four central endpoints have degree three in its endpoint-neighbor graph and the four tips have degree one. Fixing a tip at  $p$  with its neighbor north gives exactly the two displayed reflected footprints. Both contain
$$p+(-2,1)=(a,w+13),$$
which is already  $E$ ’s far terminal.The rotor exclusion is complete for the stated standard-rotor  $D_4$  catalogue. No freshness assumption or dimension-bounded enumeration is needed.3. The narrow-cap complete-family exclusion is correctThe four collision witnesses are valid throughout their stated ranges. Their intrinsic coordinates make the boundary cases transparent:CaseCoordinates in the candidate  $J$ Coordinates in the blockerEither direction,  $d\ge\ell$  $(d-\ell,1)$  $K_s:(1,3)$ Right,  $4\le d<\ell$  $(1,3)$  $K_s:(\ell+2-d,1)$ Left,  $4\le d\le8$  $(1,2)$  $V:(9-d,1)$ Left,  $10\le d<\ell$  $(1,s-2)$  $K_s:(\ell+2-d,s)$ In the first case,  $d=\ell$  puts the candidate point on bar row zero, so equality is covered.In the last case,
$$2\le \ell+2-d\le\ell-8.$$
For  $s\in\{6,8\}$ ,
$$4\le s-2\le6\le h,$$
so the candidate’s bar necessarily reaches the blocking far stem. Evenness of  $d$  closes the apparent gap between depths eight and ten.Together with the rotor exclusion, every permitted original consumer of  $p$  is ruled out. Adding further originals cannot remove a collision with a retained original endpoint.Therefore the conclusion
$$\boxed{
A+K_s\text{ has no complete feasible extension for }s=6,8
}$$
is a valid complete-family exclusion, including arbitrarily many additional originals and arbitrarily large legal dimensions.4. The general tight-cap disjointness dichotomy is exactAssume
$$6\le s\le w+10,\qquad \ell\ge12,$$
with the specified evenness conditions, and put
$$g=w+15-s.$$
The right-pointing and long-leg collision witnesses remain valid for every such  $s$ . Hence every possible consumer must have the left frame
$$J=U(h,d,f),\qquad
J(r,c)=(a+2-d+r,w+13-c).$$
NecessityAvoiding the cap bar forces  $d<\ell$ . Avoiding the short-left collision with  $V$  forces  $d\ge10$ . By evenness,
$$10\le d\le\ell-2.$$
If  $h\ge s-2$ , the lower bar row contains
$$(a+3-d,g),$$
which lies on  $K_s$ ’s far stem. Therefore
$$h<s-2,
\qquad\text{hence}\qquad h\le s-4.$$
Now let
$$c=w+13-h$$
be  $J$ ’s far column. The preceding bound gives
$$c\ge g+2\ge7,$$
while  $h\ge6$  gives  $c\le w+7$ . Thus  $c$  lies inside  $V$ ’s upper bar in both residual branches.If  $f\ge d-8$ , the far stem reaches
$$(a-6,c),$$
an existing  $V$  endpoint. Consequently
$$f<d-8,
\qquad\text{hence}\qquad f\le d-10.$$
Since  $f\ge4$ , this also forces  $d\ge14$ .These are exactly
$$\boxed{
6\le h\le s-4,\qquad
14\le d\le\ell-2,\qquad
4\le f\le d-10.
}$$
SufficiencyUnder those inequalities: $J$ ’s bar ends at row
$$a+3-d\le a-11.$$
Its far stem ends at row
$$a+2-d+f\le a-8.$$
Every endpoint of  $A$  has row at least  $a-6$ .Thus the bar and far stem avoid  $A$ .The remaining near stem lies in column  $w+12$ , ending at row  $a+2$ . The earlier sources other than  $C,E$  do not reach that column;  $E$ ’s endpoints in that column begin at row  $a+3$ , and  $C$ ’s begin still later.Relative to  $K_s$ , the complete column interval of  $J$  lies strictly between the cap stems:
$$g<c\le w+12<w+14.$$
Moreover,  $J$ ’s first bar row lies at least two rows after the cap’s last bar row:
$$(a+2-d)-(a+2-\ell)=\ell-d\ge2.$$
This proves separation from the cap.The proof covers all extreme equalities:
$$h=s-4,\qquad d=\ell-2,\qquad f=d-10,\qquad s=w+10.$$
Accordingly, the endpoint-disjointness equivalence is correct. Its inequalities are satisfiable exactly when
$$s\ge10,\qquad \ell\ge16$$
within the stated internal-cap range. For example,  $h=6,d=14,f=4$  satisfies them whenever those two conditions hold.That supplies an endpoint-disjoint candidate, while complete feasibility still requires the remaining mandatory-support conditions. The manuscript preserves this distinction correctly.5. The new cap and consumer charges and contacts are correctGeneral cap  $K_s$ The cap bar begins at the even row  $a+1-\ell$ , and its columns run from the odd column  $g$  to the even column  $w+14$ . Its counts are
$$|M_{K_s}|=s+\ell-5,$$

$$|\mathcal T_{K_s}|=\frac s2+\ell-3,$$

$$\left|\Sigma_{K_s}\cap
\bigcup_{T\in\mathcal T_{K_s}}T\right|=\ell,$$
where  $\Sigma_{K_s}$  denotes its original support set.The counted supports are two bar corners, two terminal axial supports, and  $\ell-4$  even-indexed outward lateral supports. Thus
$$q(K_s)
=(s+\ell-5)+\ell-2\left(\frac s2+\ell-3\right)=1.$$
Exactly two endpoint tiles are shared with  $A$ :
$$T(a-7,g-1),\qquad T(a+1,w+14).$$
In the first, the only new surviving event is
$$V:(a-6,g)\longrightarrow K_s:(a-7,g).$$
The reverse target is  $K_s$ ’s original axial support. In the second, the two adjacent terminals are reciprocal original axial supports, so both directions are excluded.Neither shared tile becomes full. Therefore
$$\boxed{
\Delta N=1,\quad
\Delta S=\Delta F=0,\quad
\Delta E_v=1,\quad
\Delta\Phi=0.
}$$
At  $s=w+10$ , the first shared tile has columns  $4,5$ , still inside both residual  $V$  bars. There is no hidden failure at that endpoint of the range.Surviving left consumer  $J$ Put  $H=(d+f)/2$ . Here both bar rows and both column ends cross tile boundaries. The exact counts are
$$|M_J|=h+H-1,\qquad
|\mathcal T_J|=h+H,$$

$$\left|\Sigma_J\cap
\bigcup_{T\in\mathcal T_J}T\right|=H+2.$$
The counted supports are the two bar corners and all  $H$  even-indexed lateral supports. Both terminal axial supports lie outside the endpoint tiles, as do the odd-indexed inward lateral supports. Hence
$$\boxed{q(J)=1-h}.$$
Thus  $\Delta S=h-1$  and  $\Delta N=0$ .The only shared old endpoint tiles are
$$T(a-1,w+12),\qquad T(a+1,w+12).$$
Here is the complete directed-contact audit:RowDirectionResult and original-support reason $a$  $J\to E$ Excluded: target is  $J$ ’s near outward support at even intrinsic row  $d-2$ . $a$  $E\to J$ Survives: target has  $E$ -coordinates  $(4,5)$ , outside  $E$ ’s support set. $a+1$  $J\to E$ Survives:  $J$ ’s intrinsic row  $d-1$  is odd, so its lateral support is west. $a+1$  $E\to J$ Excluded: target is  $E$ ’s original support  $(3,5)$ . $a+2$  $J\to E$ Excluded: target is  $J$ ’s original support  $(d,0)$ . $a+2$  $E\to J$ Survives: target has  $E$ -coordinates  $(2,5)$ , outside  $E$ ’s support set.Therefore the three surviving events are exactly those stated in the note:
$$E:(a,w+13)\to J:(a,w+12),$$

$$J:(a+1,w+12)\to E:(a+1,w+13),$$

$$E:(a+2,w+13)\to J:(a+2,w+12).$$
The lower tile becomes mixed full; the upper tile remains incomplete. Thus
$$\boxed{
\Delta F=1,\qquad
\Delta E_v=3,\qquad
\Delta\Phi=(h-1)+2-3=h-2\ge4.
}$$
The tile-separation argument is also valid at the limiting parameters. In particular,  $J$ ’s far terminal lies at most at  $a-8$ , so its last tile ends before  $V$ ’s first tile row  $a-7$ . Its stem tile columns are separated from both cap stems.Using the independently checked baseline below gives
$$\boxed{
\Phi(A+K_s+J)-\Phi(Q,D,W)=h-3\ge3.
}$$
6. The older absolute inventory identities checkFrom the supplied constructor, the original charges are:OwnerOriginal charge $Q$  $-1$  $D$  $-(w+3)$  $L$  $1-w$  $C$  $1$  $E$  $-1$  $W$  $-5$  $T_0$  $-(w+5)$  $V$  $1-k$ Only  $C$  is a positive original owner in  $A$ . Consequently
$$N(A)=1,\qquad S(A)=3w+k+13.$$
For  $Q,D,W$ , there are no mixed full tiles and no surviving directed events. In their shared  $Q/D$  terminal tile, both possible directions are excluded by the relevant original supports. Hence
$$\Phi(Q,D,W)=1+(w+3)+5=w+9.$$
For the full inventory, let
$$\iota=
\begin{cases}
0,&z=4,\\
1,&z\ge6
\end{cases}$$
in the first residual branch. An analytic partition by endpoint tile rows gives:Residual branch $N$  $S$  $F$  $E_v$  $\Phi$  $k=w+8,\ 4\le z\le14$  $1$  $4w+21$  $3w/2+20+\iota$  $6w+54+2\iota$  $w+8$  $k=w+10,\ z\ge16$  $1$  $4w+23$  $3w/2+18$  $6w+52$  $w+8$ The first branch’s change at  $z=6$  adds one mixed full tile and two events, which cancel in  $\Phi$ .In the second branch, the additional late contact is
$$V:(a+10,2)\longrightarrow Q:(a+10,3).$$
Its reverse targets  $Q$ ’s original axial support and is excluded. Arbitrarily increasing  $z$  produces no further contact with the fixed inventory.Thus the claimed absolute identity, including both parameter families, is correct:
$$\boxed{\Phi(A)=w+8,\qquad \Phi(Q,D,W)=w+9.}$$
7. Both conditional pair-compensation receipts are correctRight-pointing  $U$ For
$$J_{\mathrm R}=U(h,\ell,f),\qquad
J_{\mathrm R}(r,c)=(a+1-\ell+r,w+13+c),$$
the near leg contains both  $e$  and  $t$ . Its far column is at least  $w+19$ , so arbitrarily increasing  $f$  cannot create contacts with the old sources.Writing  $H=(\ell+f)/2$ ,
$$|M|=h+H-1,\qquad
|\mathcal T|=h/2+H,\qquad
|\Sigma\cap\cup\mathcal T|=H.$$
The counted supports are the two axial supports and  $H-2$  odd-indexed inward lateral supports. Hence  $q=-1$ .The only shared endpoint tile is  $T(a+1,w+14)$ , where both directions are excluded by original axial supports. It does not become full. Therefore
$$\boxed{\Delta\Phi(J_{\mathrm R}\mid A)=1}.$$
Its own full bar tiles are properly excluded from  $F$ .Reflected rotorUnder the explicit map in §1, the rotor has four matching edges, five endpoint tiles, and four original supports in those tiles:
$$q(Z)=4+4-2\cdot5=-2.$$
Its central full tile belongs to  $Z$  alone and contributes nothing to  $F$ . The two shared old tiles are precisely the ones stated in the note.The only surviving new event is
$$Z:(a-1,w+13)\longrightarrow E:(a,w+13).$$
The reverse targets  $E$ ’s original axial support. Hence
$$\boxed{\Delta\Phi(Z\mid A)=2-1=1}.$$
Both prescribed consumers therefore repair exactly the old one-unit deficit. The extra support  $y$  consumed by  $Z$  does not create an additional receipt.8. The negative-marginal identity remains correct, and its complete-family exclusion followsFor
$$H=U(6,4,w+4),\qquad H(r,c)=(a-13+c,4+r),$$
the source counts are
$$|M_H|=\frac w2+9,\qquad
|\mathcal T_H|=\frac w2+8,\qquad
|\Sigma_H\cap\cup\mathcal T_H|=\frac w2+8,$$
so  $q(H)=1$ .The shared-tile partition is exhaustive:Each tile  $T(a-7,c)$ , for  $c=4,6,\ldots,w+6$ , adds one mixed full tile and three events.The terminal tile  $T(a-7,w+8)$  adds one mixed full tile and one event.In a central tile, both  $V\to H$  events survive. Exactly the even-column  $H\to V$  event is excluded by an original support of  $H$ .In the terminal tile, both  $H/K$  directions are excluded;  $H\to V$  is excluded;  $V\to H$  survives. The pre-existing  $V\to K$  event is correctly left in the old inventory.Therefore
$$\Delta F=\frac w2+3,\qquad
\Delta E_v=\frac{3w}{2}+7,$$
and
$$\boxed{
\Delta\Phi(H\mid A+K_6)
=1+2\left(\frac w2+3\right)
-\left(\frac{3w}{2}+7\right)
=-\frac w2.
}$$
The remaining shared support  $(a+9,6)$  is indeed missing, with a  $D$  endpoint north and a  $Q$  endpoint south.More decisively, the proved narrow-cap exclusion already rules out every complete family retaining  $A+K_6$ . Any family retaining  $A+K_6+H$  also retains that forbidden prefix. The exclusion of the entire displayed negative-marginal branch from the complete model therefore follows.Its partial-inventory identity remains valid:
$$\Phi(A+K_6+H)=\frac w2+8,$$
with baseline difference  $-w/2-1$ .9. Accounting and final scopeThe package consistently uses the required original-source convention:Original support memberships continue to exclude directed events after consumption.Each endpoint keeps its original owner and original matching partner.A forced support must be consumed, but consumption itself supplies no extra numerical credit.One original may consume several outstanding supports. $N$  counts positive original owners once. $K_s$ ’s positive-owner unit and its old  $V\to K_s$  debit remain in the prefix when  $J$  is inserted.The lower  $E/J$  full tile and its directed events are counted once.The  $T_2/Z$  interaction, with the missing placement supplied, is one full-tile contribution of two minus one cross-event debit.The complete-family consequences are exactly the stated necessary conditions and exclusions. The endpoint-disjointness converse does not establish complete extendibility, and the prescribed receipts do not control arbitrary exterior signed contributions. Wider caps  $s>w+10$  remain outside this theorem.The supplied Lean statements match the geometric lemmas audited here. They do not themselves supply the full catalogue-to-completeness bridge or the cardinality accounting, and this review makes no execution claim.Required revision: add the explicit  $T_2$  affine map, and preferably the explicit  $T_2\to Z$  event explaining the mixed second difference. With that declaration, the ordinary mathematical package is acceptable on its stated scope. The unrestricted allocation and rectangular-grid triple-equality target remain open.
