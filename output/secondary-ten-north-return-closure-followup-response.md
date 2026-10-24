Verdict: ACCEPT both notes under the revised assumptionsThe explicit D4 rotor catalogue resolves the specification issue from the previous review. I find the strengthened escaped-left classification, the full mandatory-support inventories, and the conditional rotor repair correct for every stated dimension and translation.Your closure correction is also correct: the previous eight-site list was the endpoint-driven subset. With retained occupation of original supports, the nine-owner inventory has fourteen forced sites.The principal results are:ClaimAudit resultNecessary next-consumer forms under the explicit U/rotor catalogueACCEPTRight and interior-left formulas (1)–(2)ACCEPTComplete escaped-left disjointness and formulas (3)–(5)ACCEPTExact classification of the remaining deficit after the next consumer of  $x$ ACCEPT $T_0,T_1,T_2$  insertion counts and their stated scopeACCEPTFull mandatory-support counts  $7,9,13,14$ ACCEPTAllowed rotor  $Z$ , its three consumed sites, and  $\Delta\Phi=2$ ACCEPTTen-owner closure counts: eleven full-mandatory sites, seven endpoint-drivenACCEPTNo theorem or numerical formula needs repair. The arguments below distinguish the prescribed partial inventories from complete realizability and distinguish physical sites from original owners and credits.This is an audit of the written mathematics. I did not inspect or execute the cited checkers or Lean files, and this verdict supplies no execution evidence.1. Accounting and the carried-over geometryRetained occupation changes the closure test, not the defined functionalWrite
$$P_I=\bigcup_i P_i,\qquad A_I=\bigcup_i A_i,\qquad O_I=P_I\cup A_I,$$
with  $P_i$  the endpoints and  $A_i$  the original supports.A site in  $A_I-P_I$  is “missing” as an endpoint. Under the revised hypothesis it is already mandatorily occupied as a support. That distinction is essential.The stronger occupation rule does not change the stipulated  $S,N,F,Ev$ :Source charges still use each source’s original support set. $F$  still counts endpoint-full tiles, with original-source full tiles excluded. $Ev$  still counts intratile endpoint-to-endpoint events, using original-support exclusions.Consuming a support does not delete it from an old owner’s exclusion set or change that owner’s charge.Thus the earlier numerical counts remain applicable while the closure inventory becomes larger.The U charges remain  $1-k$ , including arbitrarily long legsLet
$$H=\frac{\ell+z}{2}.$$
Every candidate U has
$$|M|=k+H-1.$$
For the left-pointing frame, the bar interval starts at an even column and ends at an odd column. Its two bar rows lie in different tile rows. Consequently
$$\tau=k+H-2,\qquad
|A_V\cap\{\text{endpoint tiles of }V\}|=H-2.$$
Therefore
$$q_V=(k+H-1)+(H-2)-2(k+H-2)=1-k.$$
The other relevant horizontal phase has  $\tau=k+H$  and  $H+2$  counted original supports, giving the same charge. Hence every displayed U insertion has
$$\Delta S=k-1,\qquad \Delta N=0.$$
This calculation places no upper bound on  $\ell$  or  $z$ .The revised catalogue makes the branching lemma exhaustiveAt
$$x=(a+2,w+11),$$
west and south are occupied by fixed foreign endpoints.The U endpoint roles therefore leave only a north terminal, an east terminal, or an outer corner with north/east own neighbors. The latter two contain
$$x+(0,3)=(a+2,w+14),$$
which is a  $C$  endpoint. A north-terminal U has exactly the two stated frames, after naming the terminal leg  $\ell$ .For the specified rotor orbit, the inner endpoint roles have three own neighbors and are excluded. Both handed north-tip forms contain the relative endpoint  $(-2,-1)$ , blocked by  $T_0$  at  $(a,w+10)$ . Both east-tip forms contain  $(-1,2)$ , blocked by  $E$  at  $(a+1,w+13)$ .The quarter-turn
$$(r,c)\mapsto(c,5-r)$$
preserves the displayed endpoint, support, and matching sets. Reflection gives the other handed form. The revised hypothesis explicitly exhausts the allowed rotors by these images, so there is no remaining catalogue gap.This proves a classification of endpoint roles without imposing a dimension bound on the surviving U sources.The right and interior-left counts remain exactThe insertion counts into the seven-owner inventory are:CandidateDisjointness condition $\Delta F$  $\Delta Ev$  $\Delta\Phi$  $V_{\rm right}$ ,  $\ell=4$ Every legal  $k,z$  $2$  $5$  $k-2$  $V_{\rm right}$ ,  $\ell\ge6$ Every legal  $k,z$  $3$  $6$  $k-1$  $V_{\rm left}$ ,  $k\le w+6$ Exactly  $z\le\ell-8$  $3$  $7$  $k-2$ The zero-event shared tiles are correctly included:In the right branch with  $\ell\ge6$ , tile  $(a-5,w+10)$  is shared but contributes  $F=Ev=0$ .For  $\ell=4$ , tile  $(a-3,w+10)$  is shared and likewise contributes zero.In that short right branch, the exceptional tile  $(a-1,w+12)$  contributes the single event  $V\to E$ . The reverse targets  $E$ ’s original axial support.In the interior-left branch, the top tile instead contributes  $V\to T_0$ , producing the one-unit debit.The three full seam tiles each retain two of their four possible directed horizontal events. These are tile-level counts; the two surviving events can occur on the same row.2. Complete escaped-left classification: formulas (3)–(5) are correctSet
$$n=w+11,\qquad f=w+12-k\le4,\qquad
d=a+2-\ell,\qquad t=d+z.$$
Here  $n,d,t$  are odd and  $f$  is even. The candidate has bar rows  $d,d+1$ , spanning  $f,\ldots,n$ , with near terminal at row  $a+2$  and far terminal at row  $t$ .Exact endpoint disjointnessFor  $\ell=4$ , the bar intersects  $T_0$ ’s near stem. For  $\ell=6$ , it overlaps  $T_0$ ’s bar. These collisions hold for every  $f\le4$ .For  $\ell\ge8$ , the bar is above  $T_0$ , and the near column  $w+11$  is endpoint-disjoint from the fixed sources. Its terminal lies above the  $E$  bar.Only the far column can cause a collision: $f=4$ : it intersects  $Q$ ’s horizontal near stem if it reaches row  $a+10$ . $f\le2$ : no fixed endpoint has column  $f$ .Because  $t$  has the same odd parity as  $a$ , avoiding row  $a+10$  is exactly  $t\le a+8$ . Thus
$$\boxed{\ell\ge8,\qquad f=4\Longrightarrow d+z\le a+8.}$$
This proves both directions of (3), including arbitrarily negative far columns.The branch  $\ell\ge10$ The bar now shares no endpoint tile with the fixed inventory. The near seam contributes
$$(\Delta F,\Delta Ev)=(3,7),$$
exactly as in the interior-left branch.The possible far-column contributions are exhaustive:Far column and thresholdTileContribution $f=4,\ t\ge a-4$  $(a-5,4)$  $F=0,\ Ev=1$  $f=4,\ t\ge a-2$  $(a-3,4)$  $F=1,\ Ev=2$  $f=4,\ t\ge a$  $(a-1,4)$  $F=1,\ Ev=2$  $f=2,\ t\ge a+10$  $(a+9,2)$  $F=0,\ Ev=1$  $f\le0$ None $0,0$ At  $(a-5,4)$ , the surviving direction is  $V\to T_0$ ;  $T_0$ ’s reverse targets its original top-corner support. The two subsequent full stem tiles have cancelling contributions to  $2F-Ev$ .There is no  $Q$  contact when  $f=4$ : the admissibility bound  $t\le a+8$  leaves the candidate’s last possible tile row at  $a+7$ , whereas  $Q$ ’s near stem lies in tile row  $a+9$ .When  $f=2$ , the contact is with  $Q$ ’s tip  $(a+10,3)$ . Its surviving direction is  $V\to Q$ . The reverse targets  $Q$ ’s original axial support  $(a+10,2)$ .More explicitly, for feasible candidates in this branch,
$$\Delta F
=3+[f=4,\ t\ge a-2]+[f=4,\ t\ge a],$$
and
$$\begin{aligned}
\Delta Ev={}&7+[f=4,\ t\ge a-4]\\
&+2[f=4,\ t\ge a-2]+2[f=4,\ t\ge a]\\
&+[f=2,\ t\ge a+10].
\end{aligned}$$
The balanced terms cancel, giving
$$\boxed{
\Delta\Phi
=k-2-[f=4,\ d+z\ge a-4]
     -[f=2,\ d+z\ge a+10].
}$$
The brackets are mutually exclusive, so
$$\Delta\Phi\ge k-3\ge w+5\ge17.$$
Formula (4) is correct.The branch  $\ell=8$ Now  $d=a-6$ , and the candidate’s lower bar row  $a-5$  shares tiles with  $T_0$ ’s upper bar row  $a-4$ .The common contributions are:Tile classNumberPer-tile  $(F,Ev)$  $(a-5,c)$ ,  $c=6,8,\ldots,w+8$  $(w+4)/2$  $(1,4)$ Near end  $(a-5,w+10)$  $1$  $(1,3)$ Three lower near-stem tiles $3$  $(1,2)$ For  $f=4$ , the far end tile contributes  $(1,3)$ ; tile  $(a-3,4)$  always contributes  $(1,2)$ ; and tile  $(a-1,4)$  contributes  $(1,2)$  exactly when  $z\ge6$ . Endpoint disjointness gives  $4\le z\le14$ . Hence
$$\Delta F=w/2+8+[z\ge6],$$

$$\Delta Ev=2w+22+2[z\ge6],$$
and
$$\boxed{\Delta\Phi=1.}$$
For  $f\le2$ , the far end tile  $(a-5,4)$  has two candidate bar endpoints and one  $T_0$  endpoint, contributing  $(0,2)$ . Both vertical directions survive. The far stem lies in a different tile column.Thus
$$\Delta F=w/2+6,$$

$$\Delta Ev=2w+19+[f=2,\ z\ge16].$$
The last bracket is precisely the  $Q$ -tip contact, since
$$a-6+z\ge a+10\iff z\ge16.$$
Consequently,
$$\boxed{
\begin{array}{ll}
k=w+8:&\Delta\Phi=1,\quad 4\le z\le14,\\
k=w+10:&\Delta\Phi=2-[z\ge16],\\
k\ge w+12:&\Delta\Phi=k-w-8\ge4.
\end{array}}$$
Formula (5) is correct.The residual classification is exact within the stated local problemAfter  $T_0$ , the inventory is two below  $Q/D/W$ . Therefore the next insertion leaves a negative difference exactly when its increment is one.Across all the right, interior-left, and escaped-left branches, that occurs precisely for
$$\ell=8,\quad k=w+8,\quad 4\le z\le14,$$
or
$$\ell=8,\quad k=w+10,\quad z\ge16.$$
Both leave difference  $-1$ . The  $k=w+10,\ell=8,z<16$  branch is neutral. Every other admissible branch has positive margin.The proof is exhaustive because it separates bar, near-column, and far-column tile intersections using coordinate intervals. It does not extrapolate from a bounded dimension search.3. The explicit return chain retains its stated countsThe successive counts remain
$$\begin{array}{c|rrrrr}
\text{Insertion}&\Delta S&\Delta F&\Delta Ev&\Delta N&\Delta\Phi\\ \hline
T_0&w+5&w/2+2&2w+8&0&1\\
T_1&w+7&w/2+8&2w+22&0&1\\
T_2&w+9&w/2+5&2w+19&0&0.
\end{array}$$
The support-retention correction does not change these endpoint/event counts.For  $T_1$ , the central band contributes  $(1,4)$  per tile; its two end tiles contribute  $(1,3)$ ; and the four lower shared stem tiles contribute  $(1,2)$ .For  $T_2$ , the  $T_1$  bar band contributes  $(1,4)$  per tile. The two  $E$  tiles contribute  $(0,1)$  and  $(1,2)$ . The single event in the three-endpoint tile is  $E\to T_2$ , since the opposite direction targets  $T_2$ ’s original lateral support.Thus the nine-owner family remains exactly one below the base. The proposed  $T_3$  terminal is already an  $E$  endpoint, so this particular translated pattern stops. Neither fact classifies arbitrary later consumers.4. The stronger mandatory-support rule gives exactly  $7,9,13,14$ Define
$$H_I=\{s\in A_I-P_I:\ |N(s)\cap O_I|\ge2\}.$$
This is the full mandatory-consumer set for the prescribed inventory under the revised rule.If two missing original supports are adjacent, each has its own endpoint anchor and the other mandatorily occupied support as two distinct occupied neighbors. Both are forced. Consuming one does not remove its occupied site, so it cannot make the other retainable.The persistent set  $B$ The six stated sites are correct:SiteOriginal owner(s)Why forced $e=(a,w+14)$  $E$ Own endpoint west; support  $z$  south $z=(a+1,w+14)$  $C$  $E$  west;  $C$  south $(a+3,w+4)$  $W$ Own endpoint north; support  $(a+3,w+5)$  east $(a+3,w+5)$  $L$  $W$  north;  $L$  east $(a+7,w+6)$  $L,W$  $L$  north;  $W$  west $(a+9,6)$  $D,Q$  $D$  north;  $Q$  southOnly four are endpoint-driven. The two additional sites are  $e$  and  $(a+3,w+4)$ .The far-side pairsThe formulas
$$q_j=(a+1-2j,5-j),\qquad
r_j=(a+2-2j,5-j)$$
and their ownership are correct: $j$  $q_j$ , owned by  $T_j$  $r_j$ Owner of  $r_j$  $0$  $(a+1,5)$  $(a+2,5)$  $D$  $1$  $(a-1,4)$  $(a,4)$  $T_0$  $2$  $(a-3,3)$  $(a-2,3)$  $T_1$ Each  $q_j$  has its own endpoint north and a preceding owner’s endpoint east. Each  $r_j$  has its own endpoint east and  $q_j$  north. Both members of every pair are therefore forced, although  $r_j$  is not endpoint-driven in the displayed family.Exact evolutionPut
$$p=(a+2,w+10),\quad x_0=(a+2,w+11),\quad x_1=(a+2,w+12),$$

$$u=(a,w+12),\quad v=(a+1,w+12),\quad
g=(a-2,w+13).$$
The complete sets are exactly:InventoryFull mandatory-consumer setCountEndpoint-only countSix owners $B\cup\{p\}$  $7$  $5$ Plus  $T_0$  $B\cup\{q_0,r_0,x_0\}$  $9$  $6$ Plus  $T_1$  $B\cup\{q_0,r_0,q_1,r_1,u,v,x_1\}$  $13$  $9$ Plus  $T_2$  $B\cup\{q_0,r_0,q_1,r_1,q_2,r_2,y,g\}$  $14$  $8$ The transitions are
$$7-1+3=9,\qquad
9-1+5=13,\qquad
13-3+4=14.$$
The three consumed sites in the last transition are  $u,v,x_1$ . They belong to original support sets of  $T_1,E,T_1$ , respectively, and the one near stem of  $T_2$  consumes all three.The site  $g$  is  $T_2$ ’s original near lateral support at canonical  $(6,0)$ . Before any rotor is inserted, it already has  $T_2$  west and the mandatory support  $y$  south. Its inclusion in the fourteen-site list is necessary.5. Exhaustiveness certificate for the nine-owner support inventoryThe full forced lists by original owner are:Original ownerForced missing original supports $Q$  $(a+9,6)$  $D$  $(a+2,5),(a+9,6)$  $L$  $(a+3,w+5),(a+7,w+6)$  $C$  $(a+1,w+14)$  $E$  $(a-1,w+13),(a,w+14)$  $W$  $(a+3,w+4),(a+7,w+6)$  $T_0$  $(a+1,5),(a,4)$  $T_1$  $(a-1,4),(a-2,3)$  $T_2$  $(a-3,3),(a-2,w+13)$ These are sixteen owner/support incidences at fourteen physical sites. The duplicated incidences are the common  $Q/D$  support and the common  $L/W$  support.For completeness, the following table lists every other unconsumed original support. In this table only,  $(h,c)$  means the physical point  $(a+h,c)$ .OwnerAll remaining unconsumed supports $Q$  $(4,9),(4,11),(6,8),(9,4),(9,8),(10,2)$ , and  $(11,c)$  for  $c=3,5,7,9,11$  $D$  $(4,5),(6,5),(7,7),(8,5)$  $L$  $(3,8),(5,w+5)$  $C$  $(h,w+15)$  for  $h=2,4,6$  $E$ None $W$  $(6,w+4)$ , and  $(8,w+s)$  for  $s=1,3,5$  $T_0,T_1$ None $T_2$  $(h,c)$  for  $h=-8,-6,-4$  and  $c\in\{2,w+13\}$ Each of these thirty sites has exactly one neighbor in  $O_I$ , its own endpoint anchor. Every original support not in these two tables is already an endpoint.Thus the nine-owner family has exactly:Fourteen forced missing support sites.Thirty other unconsumed support sites.Forty-four distinct unconsumed support sites in total.This is a symbolic completeness certificate. All nine leg lengths are fixed, so their support sets are fixed finite lists of affine expressions in  $a,w$ . Membership and adjacency reduce to the displayed stem and bar intervals. The left support columns are at most  $11$ , while the right support columns are at least  $w+1$ ; for  $w\ge12$ , no additional direct adjacency appears between these groups. The spanning bars are handled by their exact row coordinates and column intervals.6. The rotor  $Z$  is allowed and has exactly the claimed incrementExact source identification and endpoint separationThe map
$$(r,c)\longmapsto(a+2-r,w+12+c)$$
transforms all three parts of the standard constructor—endpoints, original supports, and matching—into the listed data for  $Z$ .In particular, it maps standard endpoints to
$$y=(a-1,w+13),\quad e=(a,w+14),\quad z=(a+1,w+14),$$
as claimed.All  $Z$  endpoint columns are at least  $w+13$ , separating it from  $Q,D,L,W,T_0,T_1,T_2$ . Against  $E$ , its only endpoint in column  $w+13$  lies at row  $a-1$ , above  $E$ ’s far stem. Against  $C$ , its endpoints in column  $w+14$  have rows at most  $a+1$ , while  $C$ ’s far stem starts at  $a+2$ . The bars of  $C,E$  lie lower.Hence endpoint disjointness is uniform in every stated  $a,w$ .Intrinsic chargeThe five endpoint tiles of  $Z$  are
$$(a-3,w+14),$$

$$(a-1,w+12),\quad(a-1,w+14),\quad(a-1,w+16),$$

$$(a+1,w+14).$$
The middle tile  $(a-1,w+14)$  is full in  $Z$  alone and is excluded from  $F$ .Exactly four original supports lie in those five tiles:
$$(a-3,w+15),\quad(a-1,w+12),\quad
(a,w+17),\quad(a+2,w+14).$$
Therefore
$$q(Z)=4+4-2(5)=-2,$$
so
$$\Delta S=2,\qquad \Delta N=0.$$
Exact new eventsThere are exactly two shared endpoint tiles.At  $(a-1,w+12)$ ,  $Z$ ’s endpoint  $y$  fills the missing fourth corner. The new physical contacts give:Directed candidate eventResult $T_2:(a-1,w+12)\to Z:y$ Counted $Z:y\to T_2:(a-1,w+12)$ Excluded by  $Z$ ’s original support $Z:y\to E:(a,w+13)$ Counted $E:(a,w+13)\to Z:y$ Excluded by  $E$ ’s original axial supportThe pre-existing event
$$E:(a,w+13)\to T_2:(a,w+12)$$
remains in the inventory and is not counted again.This tile contributes
$$(\Delta F,\Delta Ev)=(1,2).$$
At  $(a+1,w+14)$ ,  $Z$ ’s  $z$  is adjacent to  $C$ ’s far terminal. Both directions target original axial supports of their respective source owners. The tile is shared but contributes
$$(\Delta F,\Delta Ev)=(0,0).$$
The other three  $Z$  endpoint tiles contain no old endpoints. Therefore
$$\boxed{
\Delta S=2,\quad
\Delta F=1,\quad
\Delta Ev=2,\quad
\Delta N=0,\quad
\Delta\Phi=2.
}$$
The absolute functional values are consequently
$$\begin{array}{c|c|c}
\text{Inventory}&\Phi&\Phi-\Phi(Q,D,W)\\ \hline
Q,D,W&w+9&0\\
\text{Six fixed owners}&w+6&-3\\
\text{Plus }T_0&w+7&-2\\
\text{Plus }T_1&w+8&-1\\
\text{Plus }T_2&w+8&-1\\
\text{Plus }Z&w+10&+1.
\end{array}$$
7. Exactly eleven mandatory sites remain after  $Z$ The rotor consumes exactly the three old forced sites
$$y,\qquad z,\qquad e.$$
Its other endpoint sites were not unconsumed original supports of the old inventory.The remaining forced set is
$$\boxed{
\{q_0,r_0,q_1,r_1,q_2,r_2,g\}
\cup
\{(a+3,w+4),(a+3,w+5),(a+7,w+6),(a+9,6)\}.
}$$
Its cardinality is eleven.This is more than the subtraction  $14-3$ ; the new support list must also be checked. Of  $Z$ ’s original supports: $(a-1,w+12)$ ,  $(a+1,w+13)$ , and  $(a+2,w+14)$  are already old endpoints. $g=(a-2,w+13)$  is an already forced original support of  $T_2$ .The four new unconsumed supports
$$(a-3,w+15),\quad(a-2,w+16),\quad
(a,w+17),\quad(a+1,w+16)$$
each have only their own  $Z$  anchor as a neighbor in the enlarged  $O$ .The added occupied sites give no second neighbor to any of the thirty previously unforced supports. In particular, the nearby surviving  $C$  supports in column  $w+15$  and the upper  $T_2$  supports in column  $w+13$  remain separated by nonadjacent coordinates.Therefore no new physical forced site appears.The endpoint-driven subset is exactly
$$\boxed{
\{q_0,q_1,q_2,g,
(a+3,w+5),(a+7,w+6),(a+9,6)\},
}$$
of size seven. The other four— $r_0,r_1,r_2,(a+3,w+4)$ —still require the support-adjacency test.The status of  $g$  is handled correctly: before  $Z$ , it is forced by  $T_2$ ’s endpoint west and the retained support  $y$  south; afterward,  $y$  is a  $Z$  endpoint. It becomes endpoint-driven without becoming a new demand.8. Nonreuse and the precise scope of acceptanceThe revised package consistently keeps the relevant counts separate: $Z$  is one original source consuming three already forced sites.Its contribution is its intrinsic negative-charge mass  $2$ , followed by its actual signed tile/event increment. $N$  does not increase. The sole positive original owner in the displayed inventories remains  $C$ , counted once.Original supports remain in their owners’ charge and directed-exclusion data after consumption.The old  $E\to T_2$  event is retained once. $Z$ ’s own full tile is excluded from  $F$ .The zero-event  $Z/C$  shared tile is retained in the geometric classification.The shared support  $g$  creates another original-support incidence, not another physical site or credit.Eleven remaining forced sites do not imply eleven distinct future owners.The escaped-left theorem now classifies every dimension of the next consumer of  $x$ , after the prescribed  $T_0$ , in the stated local inventory. The rotor theorem repairs the particular displayed nine-owner chain. It remains conditional on adding  $Z$ ; it does not establish that  $Z$  is forced or unique, or that every family in the two residual branches admits this same continuation.Under those expressly stated scopes, both notes receive ACCEPT. The revised support-retention treatment corrects the earlier closure incompleteness, and the new all-dimension and rotor arguments establish their claimed local results.
