The pointwise source-cut bridge still fails after imposing positive demand and endpoint connectivity. There is now a complete eight-source family in which:the full fusion is endpoint-connected; $N=n_2=1$ ,  $n_0=0$ , and  $G=2$ ;deleting just one negative original owner leaves a connected endpoint set containing the positive source and the original owner of both marked gates;the exact minimum restored-support omission count is unbounded, while the actual resource vector remains
$$(A,U_0,Z_0,H)=(1,5,0,30).$$
At the concrete parameter  $k=70$ ,
$$\boxed{\kappa=37>36=A+U_0+Z_0+H.}$$
The complete fusion has
$$\boxed{\mu=17,\qquad \sigma=623.}$$
Thus this is a complete positive-demand counterexample to that bridge, with positive margins for both allocation and the ambient inequality.There is also a general structural improvement to the retention proposal: the exact retention constraints can be expressed entirely as Horn implications involving at most three distinct original owners. This gives a canonical least feasible closure. For the cut above, however, that closure restores the deleted owner and returns the entire original fusion.Neither result settles the unrestricted allocation. They identify more precisely what a successful signed transfer must handle.1. Exact source retention is a Horn closure systemFor an original source  $i$ , write
$$O_i=P_i\cup T_i.$$
For a retained owner set  $I$ , the mandatory rule gives
$$P_I=\bigcup_{i\in I}P_i,\qquad
T_I=\left(\bigcup_{i\in I}T_i\right)\setminus P_I.$$
Consequently
$$\boxed{P_I\cup T_I=\bigcup_{i\in I}O_i.}
\tag{1}$$
This identity is decisive: consuming a support changes its status from selected to endpoint, but does not remove its occupancy.Let  $a_i(t)\in P_i$  be the unique original occupied neighbor of  $t\in T_i$ . Whenever
$$t\in T_i,\qquad q\in O_j,\qquad q\sim t,\qquad q\ne a_i(t),
\tag{2}$$
the full feasible fusion forces  $t$  to be consumed. Let  $c(t)$  be its unique original endpoint owner. Associate the implication
$$\boxed{(i\land j)\Longrightarrow c(t).}
\tag{3}$$
A nontrivial implication has three distinct owners. The producer cannot consume its own support, and its own occupied set contains no neighbor of that support other than its original anchor.TheoremA subset of original owners is a feasible complete-source subfamily if and only if it satisfies every implication (3).Necessity. If  $i,j\in I$ , both  $a_i(t)$  and  $q$  remain occupied by (1). Omitting  $c(t)$  would leave  $t$  selected with two distinct occupied neighbors.Sufficiency. Suppose a mandatory selected point  $t\in T_I$  had a second occupied neighbor besides its original anchor. Choose a retained producer  $i$  of  $t$ , and choose a retained source  $j$  whose original occupied set contains that second neighbor. Implication (3) puts  $c(t)$  in  $I$ , contradicting the fact that  $t$  is selected.Original matching edges remain a matching because original endpoint sets are disjoint. Original endpoints retain their original occupied neighborhoods, so the endpoint degree condition is preserved as well.This proves the characterization for arbitrary finite complete mixed U/rotor families, without dimension restrictions or fresh-owner assumptions.Relation to the proposed disjunctive clausesThe combined Horn-plus-disjunction description need not be discarded. It can be reduced to pure Horn form.For two adjacent original supports, consuming one leaves that point occupied. In the nontrivial four-owner situation, retaining both producers therefore forces both consumers, through the two directed instances of (3). The apparent choice of one consumer is not a free choice once all endpoint-conflict implications are included. The original-anchor exceptions are handled automatically by the condition  $q\ne a_i(t)$ .It follows that every seed  $S$  has a unique least feasible owner set:
$$S_{r+1}
=
S_r\cup
\{c(t):\text{an implication (3) has both antecedents in }S_r\}.
\tag{4}$$
There are at most as many proper additions as initially omitted owners. Every addition is forced in every feasible superset of the seed, so the final closure is independent of the order of additions.This supplies an exact closure operation. It does not yet supply a signed reserve balance or a proper smaller region.2. General written verification of the earlier two-parameter familyTo remove the outstanding dependency, here is the all-parameter verification used below.Let  $k\ge4$ ,  $h\ge8$  be arbitrary even integers. In the unchanged physical partition
$$\{2i,2i+1\}\times\{2j,2j+1\},$$
define the four-source family  $\mathcal F(k,h)$  byOwnerComplete sourcePhysical map $V_1$  $U(h,k+4,k+2)$  $(r,c)\mapsto(r-k-2,c-1)$  $V_2$  $U(6,h-2,4)$  $(r,c)\mapsto(c+1,h-1-r)$  $V_3$  $U(k+8,h,4)$  $(r,c)\mapsto(2-c,h+1-r)$  $V_4$  $U(h-2,k,k)$  $(r,c)\mapsto(-r,c)$ Every endpoint, support, and matching edge comes from the original constructor.Endpoint disjointnessThe exact endpoint sets are
$$\begin{aligned}
P_1={}&
\{-k-2,-k-1\}\times[0,h-1]\\
&{}\cup[-k,2]\times\{0\}
\cup[-k,0]\times\{h-1\},\\[1mm]
P_2={}&
[2,7]\times\{h-2,h-1\}\\
&{}\cup\{2\}\times[1,h-3]
\cup\{7\}\times[h-5,h-3],\\[1mm]
P_3={}&
[-k-6,1]\times\{h,h+1\}\\
&{}\cup\{1\}\times[1,h-1]
\cup\{-k-6\}\times[h-3,h-1],\\[1mm]
P_4={}&
\{-1,0\}\times[1,h-2]
\cup[-k,-2]\times\{1,h-2\}.
\end{aligned}
\tag{5}$$
All intervals contain integer coordinates.These blocks are pairwise disjoint. In particular: $V_1$ 's bar lies above  $V_4$ 's two tips, and its stems lie outside  $V_4$ 's stems. $V_3$ 's bar lies in columns  $h,h+1$ , outside the other three sources. $V_3$ 's near stem is in row  $1$ , between the bar of  $V_4$  and the near stem of  $V_2$ .The two short far stems occupy separated rows.Thus
$$|P|=6k+6h+28,\qquad |M|=3k+3h+14.
\tag{6}$$
The entire retained selected setDirect substitution into the support constructor gives the following disjoint families. The last column lists the unique neighbor in the full occupied set  $P\cup T$ .OwnerRetained selected point or familyUnique occupied neighbor $V_1$  $(r,-1)$ , even  $r$ ,  $-k-2\le r\le2$  $(r,0)$  $V_1$  $(3,0)$  $(2,0)$  $V_2$  $(3,c)$ , even  $c$ ,  $2\le c\le h-4$  $(2,c)$  $V_2$  $(8,c)$ ,  $c\in\{h-5,h-3,h-1\}$  $(7,c)$  $V_2$  $(7,h-6)$  $(7,h-5)$  $V_2$  $(6,h-4)$  $(7,h-4)$  $V_3$  $(2,h+1)$  $(1,h+1)$  $V_3$  $(-k-7,c)$ ,  $c\in\{h-3,h-1,h+1\}$  $(-k-6,c)$  $V_3$  $(-k-6,h-4)$  $(-k-6,h-3)$  $V_3$  $(-k-5,h-2)$  $(-k-6,h-2)$  $V_4$  $(r,2)$ , odd  $r$ ,  $-k+1\le r\le-3$  $(r,1)$  $V_4$  $(r,h-3)$ , same odd  $r$  $(r,h-2)$ The endpoint ranges (5) exclude any additional endpoint neighbor. The listed ranges and parity also exclude any selected–selected adjacency. The inequalities  $k\ge4$ ,  $h\ge8$  include all boundary cases.For example, the odd-row interior supports of  $V_1$ 's near leg are consumed by  $V_4$ , except the final point  $(1,1)$ , consumed by  $V_3$ . Every support of  $V_1$ 's far leg is consumed by  $V_3$  or  $V_4$ . Its remaining supports are exactly the first two rows of the table. The other three sources give the remaining rows by the same substitution.The four retained-support counts are
$$\frac k2+4,\qquad \frac h2+3,\qquad 6,\qquad k-2,$$
hence
$$\boxed{|T|=\frac{3k+h}{2}+11.}
\tag{7}$$
This proves complete feasibility for all the parameters, including selected–selected feasibility.Exhaustive nonfull tile classificationWrite  $n=h/2$ , and specify a tile by its even lower-coordinate origin. Every nonfull endpoint-bearing tile is one of the following:Tile origin or family of originsActual profile $(2,0)$ Neutral  $2P1T$  $(2,2j)$ ,  $1\le j\le n-2$ Regular  $2P1T$  $(6,h-4)$ ,  $(-k-6,h-2)$ Regular  $2P1T$  $(6,h-6)$ ,  $(-k-6,h-4)$ Original singleton  $1P1T$  $(-2,2j)$ ,  $1\le j\le n-2$ Original  $V_4$  irregular  $2P0T$ Every other endpoint-bearing tile is full, by (5). Therefore the general census is
$$\begin{array}{c|c}
\text{Profile}&\text{Count}\\ \hline
4P0T&3k/2+h+7\\
2P1T&h/2+1\\
2P0T&h/2-2\\
1P1T&2.
\end{array}
\tag{8}$$
The original phases are  $01,01,01,10$ , so
$$A=U_0=Z_0=0,\qquad
H=2+2(h/2-2)=h-2,\qquad
R=(h-2)/2.
\tag{9}$$
Equations (5)–(9) provide the general written verification of the earlier family. The finite parameter controls are not premises of this proof.3. The complete positive-demand extensionNow specialize the first block to  $\mathcal F(k,8)$ , with arbitrary even  $k\ge4$ , and append four fixed complete sources.The full eight-source manifest is:OwnerComplete canonical sourcePhysical mapOriginal phase $V_1$  $U(8,k+4,k+2)$  $(r-k-2,c-1)$  $01$  $V_2$  $U(6,6,4)$  $(c+1,7-r)$  $01$  $V_3$  $U(k+8,8,4)$  $(2-c,9-r)$  $01$  $V_4$  $U(6,k,k)$  $(-r,c)$  $10$  $V_5$  $U(8,8,6)$  $(r+12,17-c)$  $00$ , positive $V_6$  $U(6,6,4)$  $(c+19,r+9)$  $11$  $V_7$  $U(12,8,4)$  $(20-c,r+7)$  $11$  $V_8$  $U(6,4,4)$  $(18-r,16-c)$  $11$ The appended block is the complete family  $\mathcal F(4,8)$  under the lattice isometry
$$\Psi(r,c)=(r+18,16-c).
\tag{10}$$
Feasibility is preserved by this isometry. Its original phases are recomputed in the unchanged standard partition; no partition is reset.The complete joining argumentThe endpoint sets of the blocks are disjoint: the first block's endpoints end at row  $7$ , and the appended block's endpoints start at row  $8$ .All possible cross-block interactions occur in this fixed interface. Entries list columns before joining.BlockRowEndpoint columnsSelected columnsFirst $6$  $6,7$  $4$ First $7$  $3,4,5,6,7$  $2$ First $8$ none $3,5,7$ Appended $7$ none $7,9,11$ Appended $8$  $7,8,9,10,11$  $12$ Appended $9$  $7,8$  $10$ All other occupied points of the first block have row at most  $5$ ; all other occupied points of the appended block have row at least  $10$ .Exactly two previously retained supports are consumed:
$$(8,7)\in T_{\mathcal F(k,8)}\cap P_7,
\qquad
(7,7)\in\Psi(T_{\mathcal F(4,8)})\cap P_2.
\tag{11}$$
After these consumptions, the table excludes every additional occupied neighbor of every retained selection. The sole cross-block endpoint edge is
$$(7,7)\in P_2\quad\sim\quad(8,7)\in P_7.
\tag{12}$$
This proves complete feasibility and endpoint connectivity for all  $k$ . The changing long geometry lies entirely away from the interface.The entire selected set has the exact description
$$T=
\bigl(T_{\mathcal F(k,8)}\setminus\{(8,7)\}\bigr)
\sqcup
\bigl(\Psi(T_{\mathcal F(4,8)})\setminus\{(7,7)\}\bigr).
\tag{13}$$
Thus the earlier all-parameter table and the explicit isometry specify every retained selection and its anchor.The counts are
$$\boxed{
|P|=6k+176,\qquad
|M|=3k+88,\qquad
|T|=\frac{3k}{2}+34.
}
\tag{14}$$
4. Actual marked positive sides and the actual reserveThere is exactly one positive original source:
$$V_5=U(8,8,6).$$
Both marks have their actual original ownerUnder the map of  $V_5$ , its canonical left marked set contains the witnesses
$$(2,2)\mapsto(14,15),\qquad
(4,2)\mapsto(16,15),$$
both original endpoints of  $V_8$ .The right marked set contains
$$(2,7)\mapsto(14,10),\qquad
(4,7)\mapsto(16,10),$$
also original endpoints of the same source  $V_8$ .Each side is counted once. Therefore
$$\boxed{N=n_2=1,\qquad n_0=0,\qquad G=2.}
\tag{15}$$
This is actual marked-side demand, not an inference from original source charge.The terminal at  $(20,16)$  has both original supports
$$(20,17),\ (21,16)$$
retained. It is unactivated.The terminal at  $(18,9)$  has both original supports
$$(18,8),\ (19,9)$$
consumed by  $V_7$ . Hence
$$\boxed{A=1.}
\tag{16}$$
Actual tile and defect censusThe blocks' endpoint-bearing tiles are disjoint: rows  $7$  and  $8$  lie on opposite sides of an aligned tile boundary. The two consumed seam supports were outside their own blocks' endpoint-bearing tiles. Thus joining the blocks changes none of those tile profiles.The exhaustive census is
$$\begin{array}{c|c}
\text{Actual profile}&\text{Count}\\ \hline
4P0T&3k/2+25\\
2P1T&15\\
2P0T&14\\
3P0T&5\\
1P1T&2\\
1P2T&1.
\end{array}
\tag{17}$$
All fourteen  $2P0T$  tiles contain exact original irregular pairs: two from  $V_4$ , four from  $V_6$ , seven from  $V_7$ , and one from  $V_8$ .The five  $3P0T$  tiles are unfilled original U11 caps, with origins
$$(20,10),\ (24,10),\ (8,8),\ (16,10),\ (16,14).$$
The sixth original U11 cap, with origin  $(18,8)$ , is filled by the activated positive terminal  $(18,9)$ . No mixed triple is being classified as a cap or spent as a separate  $L_3$ .The two  $1P1T$  tiles are the original far terminal receivers of  $V_2,V_3$ . Therefore
$$U_0=5,\qquad Z_0=0,$$

$$L_1=2,\qquad L_{2\mathrm{bar}}=14,\qquad
L_{2\mathrm{mutual}}=L_3=0,$$
and
$$\boxed{
H=30,\qquad
2R=A+U_0+Z_0+H=1+5+0+30=36,\qquad R=18.
}
\tag{18}$$
This uses the stipulated single reserve identity once. The positive cap filler and its activation are not introduced as two independent payments.5. Delete only one negative source: the retained endpoints remain connectedTake the cut
$$I=\{V_2,V_3,V_4,V_5,V_6,V_7,V_8\}.
\tag{19}$$
Thus only  $V_1$ , an original phase01 negative source, is deleted.The retained endpoint graph is connected: $V_2$  and  $V_3$  are adjacent at  $(2,1)$  and  $(1,1)$ ; $V_3$  and  $V_4$  are adjacent at  $(1,1)$  and  $(0,1)$ ; $V_2$  and  $V_7$  retain the joining edge (12);the entire appended block remains connected.The positive source  $V_5$ , the gate owner  $V_8$ , and both marked-side witnesses remain in this one retained endpoint component. No positive-demand source has been deleted.Exact restored supportsThe restored support set is
$$\begin{aligned}
W_I={}&
\{(-2j,0),(-2j,7):0\le j\le k/2\}\\
&{}\cup
\{(-k-1,1),(-k-1,6),(1,0),(2,0)\}.
\end{aligned}
\tag{20}$$
There are  $k+6$  restored points.The multiple-anchor set is exactly
$$W_2=\{(-2j,7):0\le j\le k/2\}.
\tag{21}$$
For  $j\ge1$ , its point has the two persistent endpoint neighbors
$$(-2j,6)\in P_4,\qquad
(-2j,8)\in P_3.
\tag{22}$$
At  $j=0$ , there is also the persistent neighbor  $(1,7)\in P_3$ .Thus every point of  $W_2$  must be omitted in any relaxed repair keeping the retained endpoints fixed:
$$|W_2|=\frac k2+1.$$
Among the remaining restored supports, the only edges form the path
$$(0,0)\text{—}(1,0)\text{—}(2,0).
\tag{23}$$
Their respective persistent endpoint anchors are
$$(0,1)\in P_4,\qquad
(1,1)\in P_3,\qquad
(2,1)\in P_2.$$
The path has minimum vertex-cover size one, attained by its middle point  $(1,0)$ . Consequently
$$\boxed{\kappa(I)=\frac k2+2.}
\tag{24}$$
An attaining relaxed omission set is
$$W_2\cup\{(1,0)\}.
\tag{25}$$
After those omissions every remaining selection has exactly one occupied neighbor. Mandatory support retention forbids this repair in the actual source model.The three-anchor point is counted once in  $\kappa$ . The separate total degree excess is
$$\boxed{\beta(I)=\frac k2+6.}
\tag{26}$$
Here the middle point of (23) also has degree three, so the excess differs from the earlier cut deleting both  $V_1,V_2$ .Horn completion returns the entire original fusionEvery point in (22) realizes the same owner implication:
$$\boxed{(V_3\land V_4)\Longrightarrow V_1.}
\tag{27}$$
Its producer is  $V_4$ , its extra persistent endpoint owner is  $V_3$ , and its unique original consumer is  $V_1$ .The cut (19) already contains every other original owner. Therefore every feasible retained source set containing  $I$  must restore  $V_1$ :
$$\boxed{\operatorname{cl}(I)=\{V_1,\ldots,V_8\}.}
\tag{28}$$
For this positive-demand, connected cut, “delete the boundary owner and then take the least feasible closure” makes no source-family progress.6. A concrete checked member, with  $\mu$  and ambient  $\sigma$  separateTake  $k=70$ . The first four sources are then
$$U(8,74,72),\quad U(6,6,4),\quad U(78,8,4),\quad U(6,70,70),$$
with their maps in the manifest; the appended four sources are fixed.The full fusion has
$$|P|=596,\qquad |M|=298,\qquad |T|=139.$$
The seven retained sources after deleting  $V_1$  have a connected endpoint set of size  $436$ .The cut has  $76$  restored supports. Exactly  $36$  have multiple persistent endpoint anchors, and the remaining restored-support graph has exactly the two edges in (23). Therefore
$$\boxed{\kappa=36+1=37>36=A+U_0+Z_0+H.}
\tag{29}$$
I independently reconstructed this member from the original constructor, checked occupied degree in  $P\cup T$  for all  $139$  final selections, checked full and retained endpoint connectivity, and checked the attaining omission set (25). The all-parameter proof is the coordinate and interface argument above.Allocation marginThe original negative source census is
$$(K_{01},K_{10},K_{11})=(3,1,3).$$
Its negative charge is
$$S=8+5+11+5=29.$$
The actual marked-positive-side count is  $G=2$ , not  $29$ .For every  $k$  in the family,
$$\boxed{\mu=N+R-G=1+18-2=17.}
\tag{30}$$
Actual ambient slackAll original endpoints and supports lie in the aligned rectangle
$$[-k-8,27]\times[-2,17],$$
of dimensions
$$(k+36)\times20.$$
Hence
$$\begin{aligned}
\sigma
&=10(k+36)-(3k+88)-\left(\frac{3k}{2}+34\right)\\
&=\boxed{\frac{11k}{2}+238}.
\end{aligned}
\tag{31}$$
At  $k=70$ , the rectangle is  $106\times20$ , and
$$\boxed{\sigma=1060-298-139=623.}$$
The concrete summary is therefore
$$\boxed{
N=1,\quad G=2,\quad S=29,\quad
R=18,\quad \kappa=37,\quad
\mu=17,\quad \sigma=623.
}$$
7. What this changes in the central transfer questionThe pointwise bridge is false even after imposing all of the following: $n_2>n_0$ ;endpoint connectivity of the complete feasible fusion;endpoint connectivity of the retained endpoint set;retention of every positive source;retention of the actual original owner of both marked gates;deletion of only one negative original source.Moreover, the resource vector, original source counts,  $N$ ,  $G$ , and  $S$  are fixed along this family, while
$$\kappa(I)=k/2+2\longrightarrow\infty.$$
Thus no bound on these pointwise boundary omissions can depend only on those counts. Replacing the omission count by its optimal vertex-cover repair does not fix the problem.The Horn theorem also gives a precise alternative to an unrestricted clause search: there is a canonical least feasible closure, with no essential disjunctive branching. But its termination is a statement about adding back original consumers. It is not spatial descent, and it is not reserve production.There is an important remaining escape. In this construction, the two complete blocks are joined by a genuine endpoint contact with mutual support consumption, but their nontrivial Horn implications remain separate. The cross-block implications are tautological because their consumers are already among their antecedent owners. The positive block can itself be retained as a feasible family. Therefore this does not prove that a closure generated solely by the positive source and its marking dependencies must include the long obstructing band.That is a sharper remaining distinction than positive-source presence or endpoint connectivity. A successful bridge could still require a proved connection between the chosen boundary state and the positive demand’s actual retention dependencies, or carry each whole occupied boundary owner with a signed balance. The repeated witnesses in (22) all belong to one implication (27); counting that original consumer once is fundamentally different from paying for every restored support.The missing full result remains
$$\boxed{2(n_2-n_0)\le A+U_0+Z_0+H.}$$
No allocation counterexample or grid counterexample has been produced here. The concrete advance is that the positive-demand and connectivity escape for the pointwise cut rule is now excluded, and the exact retention problem has been reduced to a geometric Horn closure whose failure to give recursive progress is realized by complete original sources.
