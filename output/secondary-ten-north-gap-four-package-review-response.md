# Independent mathematical review — initial narrow north package

Task e9f464de-09c5-43d8-9652-152c4290f1ac. Verdict: ACCEPT. Later cavity theorem and six-source family are outside this input. This review does not certify executions, full formalization, realizability, novelty or the unrestricted target.

ACCEPTUnder the precise original-source assumptions you supplied, the consumer dichotomy, the neutral two-owner package identity, and the endpoint-only external-sign obstruction are correct for arbitrary legal dimensions. I found no missing mathematical hypothesis in these three claims.The essential hypotheses are already present: aligned  $2\times2$  tiles; even  $b$ , widths and leg lengths; the exhaustive U/rotor catalogue; fixed original endpoint ownership and matching; and immutable original support sets, including supports subsequently consumed. Completeness is needed for the forced-consumer conclusions. The accounting identities themselves apply to endpoint-disjoint partial families.Below is an independent reconstruction of the general proof and the explicit obstruction. At the end I identify two wording clarifications that would improve precision without changing the verdict.1. Definitions that determine the accountingFor an original owner  $X$ , write  $V_X$  for its endpoint set,  $B_X$  for its original support set, and  $\mathcal T_X$  for its endpoint-touched tiles. Its original charge is
$$q_X
=
|M_X|
+
\left|B_X\cap\bigcup_{T\in\mathcal T_X}T\right|
-
2|\mathcal T_X|.$$
For an endpoint-disjoint family  $\mathcal A$ ,
$$S(\mathcal A)=\sum_{X\in\mathcal A}\max(0,-q_X),
\qquad
N(\mathcal A)=|\{X\in\mathcal A:q_X>0\}|.$$
The mixed-full count is
$$F(\mathcal A)
=
\left|
\left\{
T:
T\subseteq\bigcup_{X\in\mathcal A}V_X,\
T\not\subseteq V_X\text{ for every }X\in\mathcal A
\right\}
\right|.$$
An event from  $X$  is a directed intratile adjacent pair  $x\to y$ , with
$$x\in V_X,
\qquad
y\in\bigcup_{Y\in\mathcal A}V_Y
\setminus(V_X\cup B_X).$$
Consequently, consuming an original support neither changes the original charge nor turns a previously excluded direction into an event. This convention is indispensable in both the package calculation and the seven-event witness.From the constructor, the intrinsic U endpoint set is exactly
$$V_{U(k,h,f)}
=
\bigl(\{0,1\}\times\{1,\ldots,k\}\bigr)
\cup
\bigl(\{2,\ldots,h\}\times\{1\}\bigr)
\cup
\bigl(\{2,\ldots,f\}\times\{k\}\bigr),$$
and its matching-edge count is
$$|M|=k-1+\frac{h+f}{2}.$$
These formulas suffice for the role classification and the charge calculations below.2. The first forced consumer is exactly as statedPut  $a=b-9$ . Thus  $a$  is odd.At
$$u=(a,w+7),$$
the west neighbor  $(a,w+6)$  is the original L anchor, while the north neighbor  $(a-1,w+7)$  is a D endpoint. The point  $u$  belongs to none of the endpoint sets  $Q,D,L$ .If  $u$  remained an unconsumed L support, it would have at least these two occupied neighbors. Completeness therefore requires an endpoint at  $u$ . Its owner  $C$  is a distinct original owner from each of  $Q,D,L$ .U rolesThe intrinsic endpoint graph has precisely the following roles:RoleOwn endpoint neighborsLeg terminalOneStrict leg interiorTwo oppositeTop-bar cornerTwo perpendicularOther bar or junction endpointThreeAt  $u$ , north and west are occupied by foreign owners, so  $C$ 's own endpoint neighbors can only be south or east.A straight interior is impossible because it requires opposite neighbors. A degree-three role is impossible. An east-facing terminal contains the endpoint two steps east of  $u$ , since its incident leg has length at least four. A corner with south/east neighbors also contains that point: its eastward arm is either a leg of length at least four or a bar of width at least six.But
$$u+(0,2)=(a,w+9)\in V_D.$$
Thus the only possible U role is a terminal with its own neighbor to the south. After naming its incident leg as the first intrinsic leg, its bar points either right or left, giving exactly
$$C_R(r,c)=(a+h-r,w+6+c)$$
or
$$C_L(r,c)=(a+h-r,w+8-c).$$
No additional U endpoint role is omitted.Rotor rolesThe supplied rotor graph has four degree-one tips and four degree-three endpoints. Its degree-three roles are impossible at  $u$ . Rotations and reflections leave two tip forms with own neighbor south and two with own neighbor east.The listed blockers are all valid:Tip formMandatory relative endpointPhysical blockerOriginal ownerSouth A $(2,-1)$  $(a+2,w+6)$  $L(2,w)$ South B $(1,-1)$  $(a+1,w+6)$  $L(1,w)$ East A $(-2,1)$  $(a-2,w+8)$  $D(0,w+3)$ East B $(-1,2)$  $(a-1,w+9)$  $D(1,w+4)$ These endpoints exist throughout the stated dimension range. No upper bound on any dimension is being used.Incident-length boundsFor  $C_R$ , its first physical bar row is  $a+h-1$ , and the bar contains column  $w+9$ . D’s far stem occupies that column through row  $a+t-2$ . If  $h<t$ , evenness gives  $h\le t-2$ , producing a collision. Hence
$$h\ge t.$$
For  $C_L$ , the first bar row contains column  $w+6$ , where L’s far stem continues through row  $a+v$ . If  $h\le v$ , these endpoints collide. Therefore
$$h\ge v+2.$$
The left-pointing form is correctly presented as a necessary form with possible further disjointness restrictions.The terminal’s axial original support is  $(a-1,w+7)$ , consumed by D in both cases. Its lateral original support is consumed by L for  $C_R$ ; for  $C_L$ , that support is the second forced site  $u_2$ .3. The second forced consumer, owner distinctness, and sign reversalFor  $C_L$ , put
$$u_2=(a,w+8).$$
This is its original lateral terminal support, anchored at  $u$ . It belongs to none of  $Q,D,L,C_L$ . Its occupied neighbors include
$$\begin{array}{c|c}
\text{Direction from }u_2&\text{Owner}\\ \hline
\text{West}&C_L\\
\text{North}&D\\
\text{East}&D.
\end{array}$$
Completeness forces an endpoint at  $u_2$ , whose owner  $C_2$  is distinct from all four of those original owners.Only south remains available for an own endpoint neighbor. Thus every U nonterminal role and every rotor nontip is excluded. The two south rotor tips have mandatory endpoints at one of
$$u_2+(2,-1),\qquad u_2+(1,-1).$$
Both positions belong to  $C_L$ ’s near stem. The stated bound  $h\ge v+2\ge6$  ensures their presence. Hence  $C_2$  must again be a south-terminal U.Its two charts are
$$C_{2,R}(r,c)=(a+h_2-r,w+7+c),$$

$$C_{2,L}(r,c)=(a+h_2-r,w+9-c).$$
For the right-pointing form, crossing D’s far-stem column gives
$$h_2\ge t.$$
For the left-pointing form, the first bar row crosses  $C_L$ ’s near-stem column. Since that stem extends through  $a+h$ , disjointness requires  $h_2>h$ , and therefore
$$h_2\ge h+2.$$
These are necessary bounds; they do not assert complete realizability.Direct reconstruction of the chargesLet
$$\lambda=\frac{h+f}{2}.$$
All four relevant frames have matching-edge count  $k-1+\lambda$ . Their reflected row phase puts intrinsic bar rows  $0,1$  in one physical tile row. The two column phases give:FramesEndpoint-touched tilesOriginal supports in those tilesOriginal full bar tilesCharge $C_R$  at  $u$ ; left-pointing  $C_2$  at  $u_2$  $k/2+1+\lambda$  $4+\lambda$  $k/2-1$  $+1$  $C_L$  at  $u$ ; right-pointing  $C_2$  at  $u_2$  $k/2+\lambda$  $\lambda$  $k/2$  $-1$ In the first row, the support count comprises two bar-end supports, two axial terminal supports, and  $\lambda$  even-row lateral supports. In the second row, it comprises two axial terminal supports and  $\lambda-2$  odd-row lateral supports.Thus, directly from the prescribed charge,
$$(k-1+\lambda)+(4+\lambda)
-2(k/2+1+\lambda)=1,$$
and
$$(k-1+\lambda)+\lambda
-2(k/2+\lambda)=-1.$$
The move from column  $w+7$  to  $w+8$  changes column parity and exchanges these phases. Therefore the claimed signs are correct:
$$q(C_R)=+1,\qquad q(C_L)=-1,$$

$$q(C_{2,R})=-1,\qquad q(C_{2,L})=+1.$$
The claim that two consecutive consumers can both be negative at the endpoint-disjoint level also has an explicit instance. For  $b=40,w=12,t=4,v=6$ , take
$$C_L=U(6,8,4),\qquad C_L(r,c)=(39-r,20-c),$$

$$C_{2,R}=U(6,4,4),\qquad C_{2,R}(r,c)=(35-r,19+c).$$
Together with the prescribed  $Q,D,L$ , these endpoint sets are pairwise disjoint, and both additional charges are  $-1$ . This establishes exactly the stated endpoint-level possibility. It provides no completeness assertion.4. The preceding debit of two is correctFor  $m=w+4$ , the D/L shared endpoint tiles have the following exhaustive partition:Tile classNumberAdded mixed full tiles per tileDirected events per tileLeft upper-bar end $1$  $1$  $3$ Upper-bar interior $w/2-1$  $1$  $4$ Separated right upper-bar end $1$  $0$  $2$ Near parallel stems $2$  $1$  $2$ At the left end, the missing fourth direction is L’s direction into its original bar-end support. In each parallel-stem tile, one direction from each owner is excluded by its alternating original support. Those exclusions persist when the other owner consumes the support.Neither original D nor original L has a full tile of its own in these phases. Thus every full tile listed here is mixed.Summing gives
$$\Delta F=\frac w2+2,
\qquad
\Delta E=2w+5.$$
The original L charge is  $1-w$ , so
$$\Delta S=w-1,\qquad \Delta N=0.$$
Consequently,
$$\Delta\Phi
=(w-1)+2\left(\frac w2+2\right)-(2w+5)
=-2.$$
Q does not change this calculation. Its endpoint tiles begin at row  $b-4$ , while L’s near/bar endpoint tiles end by row  $b-5$ . L’s far-stem tile columns begin at  $w+6\ge14$ , beyond Q’s last endpoint column  $11$ .The preceding note’s tight-case count is also consistent with this partition: the right-end tile becomes  $3+1$ , and  $\min(t-2,v)/2$  far-stem tiles are added. These changes yield its stated debit of one.5. The outward insertion has exactly the claimed countsAssume  $C=C_R$ , with arbitrary legal  $k,h,f$  and  $h\ge t$ .Its endpoints are disjoint from  $Q,D,L$ . Its bar lies below D’s far-stem endpoint range. Its near stem is in the new column  $w+7$ . Its far stem lies at
$$w+k+6\ge w+12,$$
strictly beyond all D/L endpoint columns. That far stem may extend arbitrarily high as  $f$  varies; its column separation still excludes contact. Q is farther left.The terminal tileThe tile containing  $u$  is
$$T_0=\{a-1,a\}\times\{w+6,w+7\}.$$
Before insertion it contains two D endpoints on its upper row and the L endpoint  $(a,w+6)$ . Adding  $u$  makes it mixed full.Exactly one new event occurs:
$$D:(a-1,w+7)\longrightarrow C_R:(a,w+7).$$
The other three potential directed contacts are excluded as follows:DirectionReason for exclusion $L:(a,w+6)\to u$ Target is L’s original upper bar-end support $C_R:u\to(a-1,w+7)$ Target is  $C_R$ ’s original axial terminal support $C_R:u\to(a,w+6)$ Target is  $C_R$ ’s original lateral terminal supportThus this tile contributes
$$(\Delta F,\Delta E)=(1,1).$$
The parallel-stem tilesPut
$$d=\frac{\min(h,v)}2.$$
The remaining shared endpoint tiles are exactly
$$T_i
=
\{a+2i-1,a+2i\}\times\{w+6,w+7\},
\qquad 1\le i\le d.$$
Each contains two L endpoints and two  $C_R$  endpoints, so each contributes one mixed full tile.For physical row  $a+j$ , L’s intrinsic row is  $j$ , while  $C_R$ ’s intrinsic row is  $h-j$ . These have the same parity because  $h$  is even.On odd  $j$ , both cross-column directions are events.On even  $j$ , both cross-column directions meet the respective owner’s original support.Therefore each  $T_i$  contributes exactly two events.This remains valid at all relevant boundaries:At  $j=1$ , L is at its bar/stem junction; its eastward direction is still an event.At  $j=v$ , L’s terminal lateral support suppresses the even-row direction.At  $j=h-1$ ,  $C_R$  is on its first bar row; the westward direction remains an event.At  $j=h$ ,  $C_R$ ’s intrinsic row is  $0$ , so its original bar-end support suppresses the direction previously suppressed by an even-row leg support.If  $h=v$ , both endpoint effects occur in the same final shared tile.The  $h=t$  boundaryThis boundary requires tile parity, not merely endpoint disjointness.At equality, D’s final far-stem row is
$$a+h-2,$$
which is odd. Its tile row is
$$\{a+h-3,a+h-2\}.$$
The first  $C_R$  bar row is
$$a+h-1,$$
which is even, and belongs to
$$\{a+h-1,a+h\}.$$
Thus these adjacent physical rows lie in different aligned tile rows. No additional D/ $C_R$  event or shared endpoint tile appears at equality.Original full tiles within  $C_R$ They do exist, and their exclusion is necessary.The bar contains exactly  $k/2-1$  original full tiles, in the bar tile row and column pairs
$$(w+8,w+9),\ldots,(w+k+4,w+k+5).$$
They contribute nothing to  $F$ . Endpoint disjointness prevents any previous owner from having an endpoint inside such a four-endpoint original tile.The left bar-end tile, with columns  $w+6,w+7$ , contains only one column of  $C_R$  endpoints. When L fills its other column, it is genuinely mixed, including when this is the last parallel-stem tile.Resulting ledgerThe partition gives
$$\Delta F=1+d,\qquad
\Delta E=1+2d.$$
Since  $q(C_R)=+1$ ,
$$\Delta S=0,\qquad \Delta N=1.$$
Hence
$$\Delta R_{\rm raw}
=2(1+d)-(1+2d)=1,$$

$$\Delta\Phi=1+1=2.$$
Combining this with L’s debit of two proves
$$\boxed{
\Phi(Q\cup D\cup L\cup C_R)=\Phi(Q\cup D).
}$$
The cancellation holds for independent legal widths and leg lengths. It leaves no additional local credit.6. The external identity is an exact partitionLet  $B=\{Q,D\}$ ,  $P=\{L,C_R\}$ , and let  $I$  be the mixed full tiles added by inserting  $P$  into  $B$ .Every tile in  $I$  contains a P endpoint absent from  $B\cup W$ . Endpoint disjointness prevents W from occupying that cell. Therefore each such tile is necessarily new in the larger insertion as well.Moreover,  $B\cup P$  already fills every cell of an internal full tile, so W has no endpoint anywhere in that tile.There is no hidden deletion or reclassification of an old mixed full tile: an old full tile already has endpoints in all four cells, leaving no cell available to a new endpoint-disjoint owner. Conversely, a tile full within a newly inserted original owner had no base endpoints and is excluded from the mixed-full count.Thus
$$\Delta F=|I|+F_{\rm extra}.$$
The added events partition uniquely by the original owners of their endpoints:
$$\Delta E=E_{\rm internal}+E(P,W).$$
This includes both directions and permits external tiles involving several owners. Original support consumption changes none of these event exclusions.The changes in  $S$  and  $N$  depend only on the inserted original owners. Subtracting the established internal neutral identity therefore gives
$$\boxed{
\Phi(Q/D/W/P)-\Phi(Q/D/W)
=
2F_{\rm extra}-E(P,W).
}$$
No positivity statement follows from this partition.7. The five-source obstruction reconstructs exactlyFor the displayed parameters,
$$b=40,\quad a=31,\quad w=12,\quad t=4,\quad v=6,$$
the isolated original charges reconstruct as follows:Original ownerMatching edgesEndpoint-touched tilesOriginal supports in those tilesCharge $Q$ 1196 $-1$  $D$ 22215 $-15$  $L$ 16177 $-11$  $C_R$ 988 $+1$  $W$ 9106 $-5$ Thus  $C_R$  is the only positive original owner.The five endpoint sets are pairwise disjoint. W’s endpoints have columns at most  $17$ , while  $C_R$ ’s endpoint-touched column pairs start at  $(18,19)$ , so these two owners share no endpoint tile.The L/W shared tiles are exactly:Lower tile coordinateEndpoint partitionExtra mixed-full countDirected events $(32,12)$  $2L+1W$ 01 $(32,14)$  $2L+2W$ 13 $(32,16)$  $2L+2W$ 13The seven events are
$$L:(32,c)\longrightarrow W:(33,c),
\qquad c=13,14,15,16,17,$$
and
$$W:(33,c)\longrightarrow L:(32,c),
\qquad c=14,16.$$
The reverse directions at  $c=13,15,17$  hit W’s original supports
$$(32,13),\quad(32,15),\quad(32,17).$$
They remain excluded even though L consumes them. Hence
$$F_{\rm extra}=2,\qquad E(P,W)=7,$$
and
$$\boxed{2F_{\rm extra}-E(P,W)=4-7=-3.}$$
The complete algebraic ledger for the compared partial families is:Family $N$  $S$  $F$  $E$  $R_{\rm raw}$  $\Phi$  $Q,D$ 016001616 $Q,D,L,C_R$ 12711341516 $Q,D,W$ 021002121 $Q,D,W,L,C_R$ 13213411718In particular,  $C_R$ ’s original full tiles at  $(34,20)$  and  $(34,22)$  are excluded from  $F$ . The whole package decreases  $\Phi$  by exactly three in this endpoint-disjoint partial family.8. Why this is incomplete and supplies no target counterexampleThe first forced site is repaired:
$$u=(31,19)\in V_{C_R}.$$
Its two original terminal supports are consumed by D and L:
$$(30,19)\in V_D,\qquad (31,18)\in V_L.$$
However,
$$q=(32,20)$$
belongs to no endpoint set in the displayed five-source family. It is simultaneously:D’s original support  $D(3,15)$ , anchored at
$$D(3,16)=(32,21);$$
 $C_R$ ’s original support  $C_R(3,2)$ , anchored at
$$C_R(3,1)=(32,19).$$
These are two distinct occupied endpoint anchors adjacent to the same unconsumed support. The sole-occupied-neighbor requirement therefore fails.Every complete extension must consume  $q$  with an endpoint of an additional original owner. That owner’s entire matching, support set, charge, tile contribution and events must enter the accounting. Its contribution cannot be discarded or presumed favorable.The witness consequently disproves the endpoint-only external nonnegativity assertion. It does not establish a violation in a complete feasible family, the existence of a complete extension, the impossibility of such an extension, or a target allocation counterexample.9. Wording clarificationsTwo small changes would make the accepted scope more explicit:In the external partition proof, replace “W cannot occupy it” with “W cannot have an endpoint in it.” Original W supports may coincide with other owners’ endpoints; that is allowed and does not disturb the proof.Replace “finite checks validate the written general argument” with wording such as “finite checks corroborate the formulas on the tested instances; the catalogue exhaustion and tile partition establish the general statements.” The general audit above rests on those written arguments.Neither clarification changes a mathematical hypothesis or formula. The supplied proof supports the three stated claims, with  $N$  counting positive original owners exactly once and with no additional global allocation conclusion.
