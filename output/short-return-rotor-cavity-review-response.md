Verdict: ACCEPTNo mathematical blocker in the  $k=4$  noncompletion theorem or the standalone  $Q/R$  cavity lemma, under the stated complete original-source model. The proof covers every legal even  $b\ge 8$  and independently every legal even  $a\ge 4$ . It uses neither A/B/C nor marking or maximality.The correction is exact:
$$\boxed{(b,10)=Q(1,2)\text{ is an original Q bar endpoint, not a Q support}.}$$
This is a written mathematical audit. It does not certify code execution, Lean, or realizability. There is one source-access qualification: I could not independently retrieve the relatively linked earlier note. In particular, I distinguish checking the claimed rotor support’s coordinate and anchor from independently recovering its original support catalogue. The Q-support witness in §3 makes that rotor-support designation unnecessary for either noncompletion result.1. Endpoint coordinates and disjointnessWrite the original U endpoint convention as
$$E_{U(d,A,K)}
=
\bigl(\{0,1\}\times[1,d]\bigr)
\cup\bigl([2,A]\times\{1\}\bigr)
\cup\bigl([2,K]\times\{d\}\bigr),$$
where intervals denote integer coordinates.Applying the two displayed frames gives
$$\begin{aligned}
E_X={}&
\bigl([3,b]\times\{3,4\}\bigr)
\cup\bigl(\{3\}\times[5,a+3]\bigr)
\cup\bigl(\{b\}\times[5,7]\bigr),\\[2mm]
E_Q={}&
\bigl([b-4,b+1]\times\{10,11\}\bigr)
\cup\bigl(\{b+1\}\times[3,9]\bigr)
\cup\bigl(\{b-4\}\times[7,9]\bigr).
\end{aligned}$$
These sets are disjoint throughout the claimed parameter range:Q’s endpoints have first coordinate at least  $b-4\ge4$ , so they avoid X’s arbitrarily long near leg in row  $3$ .Q’s bars, in columns  $10,11$ , avoid X’s bars and far leg.Q’s near leg is in row  $b+1$ , beyond X’s bars.Q’s far leg is in row  $b-4$ , columns  $7,8,9$ ; it meets neither X’s bars nor either X leg.Thus no relation between  $a$  and  $b$  is being silently used.Relevant support and blocker coordinatesThe support transformations used in the proof are correct:World pointIntrinsic position and roleOriginal anchor $w=(b,8)$ Q near inner support  $Q(3,2)$  $Q(3,1)=(b+1,8)$  $w=(b,8)$ Also X far-terminal support  $X(5,b-2)$  $X(4,b-2)=(b,7)$  $q=(b-3,8)$ Q far inner support  $Q(3,5)$  $Q(3,6)=(b-4,8)$  $p=(b-3,9)$ Claimed canonical rotor support  $(1,4)$ , translated by  $(b-4,5)$ Translated  $(2,4)=(b-2,9)$ For Q, the two inner-support coordinates are precisely the odd-row near and far support positions:
$$(3,2),\qquad (3,6-1)=(3,5).$$
The three Q endpoint blockers are
$$\begin{aligned}
(b-4,8)&=Q(3,6),\\
(b,10)&=Q(1,2),\\
(b-1,10)&=Q(1,3).
\end{aligned}$$
For  $p$ , the displayed rotor endpoint set confirms that  $(b-2,9)$  is its only within-R endpoint neighbor. Its designation as an original support refers to the original rotor support catalogue; the proof can dispense with that designation by using  $q$ , as discussed below.The additional observation that  $w$  is also an original X support reinforces the forcing argument. Its omission from the submitted proof is harmless.2. Forcing a consumer at  $w$ , with ownership established firstThe west and south neighbors of  $w$  are
$$(b,7)\in E_X,\qquad (b+1,8)\in E_Q.$$
They are distinct occupied endpoints whose occupancy cannot disappear.If  $w$  remained an unconsumed Q support, it would have both its original anchor and another occupied neighbor. That contradicts the support condition. Therefore  $w$  must be consumed and must be an original endpoint of some source  $C$ .Crucially,
$$w\notin E_X\cup E_Q.$$
Consequently,
$$C\ne X,\qquad C\ne Q.$$
This establishes distinct ownership before using X and Q endpoints as blockers. By unique original endpoint ownership,  $C$  cannot own the west or south neighbor of  $w$ . Its own endpoint neighbors at  $w$  must therefore lie north or east.No fresh-owner assumption has entered.  $C$  may be a source already encountered elsewhere in a larger configuration; it simply cannot be either of these two fixed original sources.3. The U catalogue at  $w$  is exhaustive, including minimum dimensionsEvery U endpoint belongs to one of the following classes:U endpoint roleOwn endpoint neighborsPossibility at  $w$ Interior point of either bar rowThreeExcludedInner junction  $(1,1)$  or  $(1,d)$ ThreeExcludedNonterminal straight-leg pointTwo opposite neighborsExcludedLeg terminalOne neighborOnly north or eastOuter bar corner  $(0,1)$  or  $(0,d)$ Two perpendicular neighborsMust be north and eastThe remaining cases are blocked as claimed.North terminalA terminal whose own neighbor lies north belongs to a straight incident endpoint segment of length  $L\ge4$ , continuing through the row- $0$  outer corner. Hence the source owns the point at north distance four:
$$w+(-4,0)=(b-4,8)\in E_Q.$$
The boundary case  $L=4$  is covered: the blocker is then exactly the incident row- $0$  corner. There is no missing equality case.East terminalThe corresponding incident segment contains the point at east distance two:
$$w+(0,2)=(b,10)\in E_Q.$$
Every legal leg length  $L\ge4$  includes that point.Outer corner with bar extending northThe bar has width  $d\ge6$ , so its straight endpoint segment contains distances  $0,\ldots,d-1$  from the corner. In particular it contains north distance four, again hitting
$$(b-4,8)\in E_Q.$$
Outer corner with bar extending eastThe bar contains east distance two, hitting
$$(b,10)\in E_Q.$$
These arguments cover both intrinsic outer corners, either incident leg, all rotations and reflections, and arbitrary other-leg length. The “two outer-corner orientations” are exactly the two choices of whether the long bar follows the available north or east direction.Thus no legal U can own  $w$ . This is an unbounded catalogue argument; it does not depend on a finite dimension scan.4. Exactly four rotor tip footprints remain, and three share the stated blockerThe canonical rotor endpoint set is
$$E=
\{(1,2),(2,2),(2,3),(2,4),
  (3,1),(3,2),(3,3),(4,3)\}.$$
Its four central endpoints each have three own endpoint neighbors. Its four tips each have one. Therefore an endpoint placed at  $w$ , with only north/east own-neighbor directions available, must be a north or east tip.The endpoint footprint is invariant under quarter-turn rotation about  $(5/2,5/2)$ ; reflection gives the other chirality. Consequently there are two distinct endpoint placements for each of the two permitted tip directions.Using offsets from  $w$ , they are:FormEndpoint offsets $N_1$  $(-3,-1),(-2,-1),(-2,0),(-2,1),(-1,-2),(-1,-1),(-1,0),(0,0)$  $N_2$  $(-3,1),(-2,1),(-2,0),(-2,-1),(-1,2),(-1,1),(-1,0),(0,0)$  $E_1$  $(-2,1),(-1,1),(-1,2),(-1,3),(0,0),(0,1),(0,2),(1,2)$  $E_2$  $(2,1),(1,1),(1,2),(1,3),(0,0),(0,1),(0,2),(-1,2)$ Exactly  $N_2,E_1,E_2$  contain
$$(-1,2),$$
which is the world point
$$(b-1,10)=Q(1,3).$$
Since the consumer differs from Q, all three are forbidden.The sole remaining endpoint footprint  $N_1$  is exactly the displayed  $R$ .The matching is also fixedEach rotor tip has only one own endpoint neighbor. Matching the four tips therefore forces all four edges:
$$\begin{aligned}
(b-3,7)&\mathbin{-}(b-2,7),\\
(b-2,8)&\mathbin{-}(b-2,9),\\
(b-1,6)&\mathbin{-}(b-1,7),\\
(b-1,8)&\mathbin{-}(b,8).
\end{aligned}$$
These exhaust all eight endpoints. Thus there is no alternative matching on this endpoint graph that evades the subsequent argument.This classification concerns the source actually owning  $w$ . It does not assert that the surviving candidate can occur in a complete family.5. The standalone  $Q/R$  cavity lemma is validThis part does not use X,  $a$ , or the lower bound  $b\ge8$ . It applies to every integer lattice translation of the prescribed Q/R pair.DisjointnessEvery R endpoint has first coordinate in  $[b-3,b]$  and second coordinate at most  $9$ . It therefore belongs to none of the three pieces defining  $E_Q$ . Hence
$$E_Q\cap E_R=\varnothing.$$
Every lattice boundary point is occupiedFor
$$D=[b-4,b-2]\times[7,10],$$
the boundary ownership is:Boundary portionOwnerTop:  $\{b-4\}\times[7,10]$ QRight:  $[b-4,b-2]\times\{10\}$ QBottom except right corner:  $\{b-2\}\times[7,9]$ RLeft except top corner:  $[b-3,b-2]\times\{7\}$ RThe overlapping entries describe the same corner where appropriate; they do not create shared ownership between Q and R.The strict lattice interior is exactly
$$I=D^\circ\cap\mathbb Z^2
=\{(b-3,8),(b-3,9)\}.$$
Neither point is an original endpoint of Q or R.Q’s support alone forces entry into the cavityUse
$$q=(b-3,8)=Q(3,5).$$
Its original anchor is
$$(b-4,8)\in E_Q.$$
It also has the R endpoint neighbor
$$(b-3,7)\in E_R.$$
Indeed,  $(b-2,8)\in E_R$  is a further occupied neighbor, though it is unnecessary.Thus  $q$  cannot remain an unconsumed original support. It must become an original endpoint of a source  $T$ . Since
$$q\notin E_Q\cup E_R,$$
this source differs from both Q and R.This establishes the cavity contradiction without using any original R support membership.The alternative witness  $p=(b-3,9)$  has the claimed geometry: its within-R anchor is  $(b-2,9)$ , and Q owns its north neighbor  $(b-4,9)$ . Q also owns its east neighbor  $(b-3,10)$ . If the original rotor catalogue includes the stated canonical support  $(1,4)$ , its forcing argument is correct as well.The connected-graph argument has no escapeSuppose  $T$  had an endpoint outside  $I$ . Its connected unit-edge endpoint graph would contain a path from  $q$  to that endpoint.At the first step leaving  $I$ , the path must visit a lattice boundary point of  $D$ . Every such boundary point is already an original endpoint of Q or R. Unique original endpoint ownership forbids  $T$  from containing it.Therefore
$$E_T\subseteq I.$$
But  $I$  consists of two sites in a single row. No allowed U or rotor fits there. In particular:A U has at least five occupied rows in its intrinsic orientation; after exchanging the coordinate axes, its width gives at least six.A rotor spans four rows in every lattice orientation.This proves the standalone Q/R obstruction.The reasoning is specifically about paths in one source’s own endpoint graph. It neither assumes that foreign sources are globally separated nor uses paths through other owners or through supports.6. Repeated owners cannot bypass either stepThe proof handles repeated-owner possibilities correctly at both stages:The source owning  $w$  cannot be X or Q, because their fixed original endpoint sets omit  $w$ .The source owning an interior cavity point cannot be Q or R, because their fixed original endpoint sets omit both interior points.An interior consumer is allowed to be some other previously named owner. Its endpoint graph is still subject to the same boundary obstruction. Reusing an owner name cannot add endpoints to its fixed original footprint, change its original matching, or authorize sharing another owner’s endpoint.Accordingly, the proof needs no assertion that every newly encountered role has a fresh owner.7. Parameter range,  $k=6$ , and accounting scopeArbitrary  $b$  and independent  $a$ The proof uses  $b\ge8$  to ensure the stated X/Q endpoint disjointness and uses the legal minimum dimensions in the U catalogue. It imposes no upper bound on  $b$  or  $a$ , and no dependence of one on the other.Therefore the claimed exclusion includes all legal even  $b\ge12$ , as well as  $b=8,10$ . A/B/C, marking, and maximality play no role in the standalone theorem. Its application to an actual maximal Vcorner chain is valid whenever that chain supplies the two prescribed frames.Why this does not exclude  $k=6$ For
$$X_6=U(b-2,a,6)$$
in the same frame,
$$w=(b,8)=X_6(5,b-2)$$
is already an original far-leg endpoint. The step forcing a different consumer at  $w$  therefore fails.The proposed replacement point also fails to create a new-consumer argument:
$$(b,10)=Q(1,2)$$
is already a Q endpoint. More precisely, it is also
$$X_6(7,b-2),$$
the original far-terminal support of  $X_6$ , already consumed by Q. Neither fact forces the rotor R.Thus the text correctly leaves  $k=6$  outside this argument. Failure of the argument there supplies no realizability conclusion.Consequences for the earlier conditional result and ledgerTaking the earlier support-gap result as summarized in the submission:Its  $k=4$  assertion remains a valid conditional statement, but its complete-family hypothesis now has no instances in this prescribed short-return class.An impossible configuration contributes no realized pair, activation, reserve, or compensation receipt.The theorem adds no numerical term to the existing resource unions or to
$$\mu=N+R-G.$$
It does not change the convention that  $N$  counts positive owners.It supplies neither a universal improvement of the  $5/6$  bound nor the unrestricted allocation result.Those are the correct logical consequences. The historical descriptions of the earlier note and existing ledger are not independently re-certified by this audit.Blocking corrections: none. For a fully self-contained presentation, the one useful editorial strengthening is to make  $q=Q(3,5)$  the primary cavity witness. That makes explicit that the standalone obstruction requires only Q’s original support rule, the displayed rotor endpoints, immutable ownership, and connected unit-edge endpoint graphs.
