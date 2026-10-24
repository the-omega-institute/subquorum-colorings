ACCEPT. Under the unchanged original U support, matching, and profile conventions, the catalogue, strengthened clearance argument, and complete eight-source obstruction are correct. The exit is an original regular  $2P1T$  pair, and the stated global counts give  $\mu=19>0$ .The witness refutes exactly the two proposed immediate local implications. It does not refute payment elsewhere in the configuration or establish a global allocation failure. No mathematical repair is required.Two meanings matter throughout: “occupied” includes retained selected supports as well as endpoints, and the least Horn hull is taken within the displayed eight-source family. These are the unchanged model conventions, not additional assumptions.1. The original full- $2\times2$  catalogue is exhaustiveAn original U has two stems separated by at least five columns. Below its bar, those stems cannot supply both adjacent columns of a full  $2\times2$  square. At a bar/stem junction, the row below the bar contains only one endpoint on that side, leaving the other corner missing.Therefore every full original U square lies entirely in its two-row bar.Horizontal formTo contain  $\{2,3\}^2$ , the bar rows must be  $2,3$ . Its column interval contains columns  $2,3$ . Starting at or before column one would include the producer’s endpoints  $(2,1),(3,1)$ . Consequently it starts at column two.Upward legs would meet the producer’s row-one bar, in particular at  $(1,2)$ . Thus they point down. After naming the near leg first, the frame is exactly
$$F_h(r,c)=(r+2,c+1).$$
Its bar occupies columns  $2,\ldots,d+1$ . Since the producer owns  $(2,w)$ , disjointness gives
$$d+1<w,\qquad d\le w-2.$$
Vertical formThe corresponding argument forces bar columns  $2,3$ , with its row interval starting at row two. Leftward legs meet  $(2,1)$ , so the legs point right:
$$F_v(r,c)=(c+1,r+2).$$
Its near row-two endpoint interval, including the bar corners, is columns  $2,\ldots,a+2$ . Avoiding  $(2,w)$  requires
$$a+2<w.$$
For even  $a,w$ , this gives
$$a\le w-4.$$
These are necessary clearances, as the table labels them. Other parts of a complete family can impose additional constraints, including constraints involving a far leg. The catalogue does not assert that its displayed inequalities alone imply feasibility.Both transported charges are  $-1$ The horizontal frame leaves the two bar rows in one aligned physical tile strip and shifts the column alignment by one. Its endpoint-containing original profiles consist of: $d/2$  full  $4P0T$  tiles; $(a+b-4)/2$  regular  $2P1T$  tiles;two terminal  $1P1T$  tiles.The first two profiles have zero original charge, and each  $1P1T$  profile has charge  $-1/2$ . Hence the source charge is
$$-1.$$
Moreover,
$$F_v=\operatorname{transpose}\circ F_h.$$
Physical transposition preserves the fixed tile partition and the transported matching/support profiles. The vertical form therefore has the same charge.In particular, neither form splits the two bar rows across adjacent tile strips. The larger dimension-dependent negative bar charge does not enter this catalogue.2. The occupied-support strengthening and both forced transitions are validIf the producer terminal  $(l,1)$  is unactivated, its original supports
$$(l,0),\qquad(l+1,1)$$
remain selected. The latter already has its own occupied anchor  $(l,1)$ . Therefore
$$(l+1,2)$$
must be unoccupied.Horizontal clearanceThe horizontal consumer has endpoints at column two in every row
$$2,\ldots,a+2.$$
Its original beyond-tip support is
$$(a+3,2).$$
That point is occupied in either possible status: it is selected if unconsumed and an endpoint if consumed. Thus the entire interval
$$\{(r,2):2\le r\le a+3\}$$
is occupied.If  $a\ge l-2$ , this interval contains  $(l+1,2)$ , contradicting the retained producer support’s unique occupied-neighbor condition. Evenness therefore gives
$$\boxed{a\le l-4.}$$
The boundary  $a=l-2$  is precisely where counting the beyond-tip support matters. An endpoint-only argument would miss that obstruction.Now set
$$q=(a+3,2).$$
It has its own anchor  $(a+2,2)$ . Since  $a+3\le l-1$ , it also has the producer endpoint
$$(a+3,1)$$
as a neighbor. It cannot remain selected, so complete feasibility forces its consumption.Neither displayed source owns  $q$  as an original endpoint, so a further endpoint owner is required. Finally,  $a\ge4$  implies  $l\ge8$ .Vertical clearanceThe vertical consumer’s bar owns column two in rows
$$2,\ldots,d+1.$$
If  $d\ge l$ , this includes the forbidden point  $(l+1,2)$ . Thus
$$\boxed{d\le l-2.}$$
Its relevant original support is
$$q=(d+2,2)=F_v(0,d+1),$$
the image of the original bar-end support. Its own anchor is
$$F_v(0,d)=(d+1,2).$$
Because  $d+2\le l$ , it also has the producer endpoint
$$(d+2,1)$$
as a neighbor. Again, it must be consumed by a further endpoint owner.Equality  $d=l-2$  is covered: the second endpoint neighbor is then the producer’s terminal  $(l,1)$ . Crucially,  $q=(l,2)$  lies outside that positive terminal’s original physical tile. Its consumption therefore does not itself imply activation of that terminal.Since  $d\ge6$ , this case also requires  $l\ge8$ .Both arguments establish forced ownership. Neither identifies the resulting tile as a reserve defect.3. The eight-source manifest is a complete feasible configurationFor the reconstruction, the unchanged U support pattern is the two outer bar-corner supports, the two beyond-tip supports, and the alternating leg supports:
$$\begin{aligned}
S(U(w,l,f))={}&
\{(0,0),(0,w+1),(l+1,1),(f+1,w)\}\\
&\cup\{(r,0):2\le r\le l,\ r\text{ even}\}\\
&\cup\{(r,2):3\le r\le l-1,\ r\text{ odd}\}\\
&\cup\{(r,w+1):2\le r\le f,\ r\text{ even}\}\\
&\cup\{(r,w-1):3\le r\le f-1,\ r\text{ odd}\}.
\end{aligned}$$
Transporting the endpoint sets in the manifest gives, in owner order  $A,\ldots,H$ ,
$$38,\ 18,\ 18,\ 20,\ 20,\ 22,\ 22,\ 26$$
endpoints. Their physical sets are pairwise disjoint, and these counts sum to  $184$ .The original matching is retainedThe U matching is fixed by leaf elimination. The legs pair rows
$$(1,2),(3,4),\ldots;$$
the upper bar pairs columns
$$(1,2),(3,4),\ldots;$$
and the remaining lower-bar interior pairs columns
$$(2,3),(4,5),\ldots.$$
Transporting these edges gives  $92$  unit lattice matching edges covering all  $184$  endpoints exactly once. No replacement matching is needed.All mandatory unconsumed supports are accounted forLet  $P$  be the final endpoint union and
$$T=\left(\bigcup_i S_i\right)\setminus P.$$
The selected supports are exactly:OwnerSurviving selected supportsA $(0,0),(2,0),(4,0),(6,0),(8,0),(9,1)$ B $(3,5),(6,5)$ C $(-1,15),(-1,20),(0,21),(1,16),(1,19),(2,21),(4,21)$ D $(6,10)$ E $(4,10),(9,13)$ F $(9,3),(12,-1),(12,1),(12,3),(13,-3),(14,-2),(14,0),(14,2),(14,4),(14,6)$ G $(6,15),(11,15),(12,13),(13,14),(13,16),(13,18)$ H $(10,8),(17,8),(18,6),(19,7),(19,9),(19,11)$ There are  $40$  points. Each has exactly one neighbor in the full occupied set  $P\cup T$ . In particular, there are no adjacent surviving selected supports. This checks the stronger occupancy condition needed in Section 2, rather than merely an endpoint-neighbor condition.Every endpoint has at least three occupied neighbors. Conceptually, each source already provides those neighbors in its original occupied configuration, and support consumption preserves occupancy at the consumed point. The resulting degree counts are  $118$  endpoints of occupied degree three and  $66$  of degree four.Thus the support feasibility claim does not depend on omitting any mandatory support.4. The Horn hull and connectedness have a direct finite proofThe following chain forces every other owner from  $\{A,B\}$ . Each forcing point is an original support of an already retained source and has two already retained endpoint neighbors.Forced supportOriginal support ownerTwo retained endpoint neighborsRequired endpoint owner $(2,7)$ B $A:(1,7)$ ,  $B:(2,6)$ D $(8,2)$ B $B:(7,2)$ ,  $A:(8,1)$ F $(3,13)$ A $D:(2,13)$ ,  $A:(3,14)$ E $(5,14)$ A $A:(4,14)$ ,  $E:(5,13)$ G $(9,7)$ E $E:(8,7)$ ,  $F:(9,6)$ H $(4,15)$ A $A:(4,14)$ ,  $G:(5,15)$ CWithin the manifest, each forcing point has the unique endpoint owner shown. Every feasible subfamily containing A and B must therefore contain all eight owners. Since the full family is feasible, it is exactly their least feasible Horn hull.This is a hull statement relative to the listed family. It does not assert that every arbitrary completion of the two-source pattern must use these same six additional sources.Connectedness follows from the same data. A and B already have adjacent endpoints, for example  $(2,1)$  and  $(2,2)$ . Each forced owner contains a point adjacent to an endpoint of an already retained owner. Since every original source endpoint graph is connected, the full endpoint graph is connected.5. The source charges and global reserve counts agree with the actual profilesThe original physical profiles reconstruct as follows:Owner $4P0T$  $2P1T$  $2P0T$  $3P0T$  $1P1T$  $1P2T$ ChargeA660002 $1$ B320020 $-1$ C044020 $-5$ D034200 $-5$ E250002 $1$ F044200 $-5$ G046020 $-7$ H440002 $1$ The unchanged catalogue weights in this column order are
$$0,\quad0,\quad-1,\quad-\tfrac12,\quad-\tfrac12,\quad+\tfrac12.$$
They give precisely the displayed charges. Hence the positive owners are A, E, and H, and  $N=3$ .For the final reserve occurrences, denote a physical tile by its even lower corner.Original caps and mixed triples are separateThe three unfilled original U triples are
$$(6,8)\text{ from D},\qquad
(8,4)\text{ from F},\qquad
(12,4)\text{ from F}.$$
Thus  $U_0=3$ .The three mixed nonfull triples are:TileEndpoint ownership $(2,6)$ One B endpoint and two D endpoints $(4,18)$ Two C endpoints and one G endpoint $(6,6)$ One B endpoint and two D endpointsThus  $L_3=3$ . None of the original-cap tiles is counted again as a mixed triple.The other non-A units are identifiableThe two remaining negative singleton tiles are
$$(4,20)\text{ from C},\qquad (12,18)\text{ from G},$$
giving  $L_1=2$ .The thirteen remaining original-bar  $2P0T$  tiles are:OwnerTile lower cornersC $(2,16),(2,18)$ D $(4,6),(4,8)$ F $(10,4),(10,6),(12,6)$ G $\{6,8,10\}\times\{16,18\}$ All thirteen are original bar pairs. They do not supply mixed mutual-pair occurrences. Consequently
$$L_{2\mathrm{bar}}=13,\qquad L_{2\mathrm{mutual}}=0.$$
There are no rotor owners, so  $Z_0=0$ .As a completeness check, the final endpoint-containing tiles partition into  $25$  full tiles,  $18$  regular  $2P1T$  pairs,  $13$  irregular  $2P0T$  pairs, six triples, two negative singletons, and two surviving positive singletons. Their endpoint total is
$$25\cdot4+18\cdot2+13\cdot2+6\cdot3+2+2=184.$$
There are four activation occurrencesThe activated original positive terminals are:OccurrenceTerminalPhysical tile lower cornerA far $(4,14)$  $(4,14)$ E far $(3,9)$  $(2,8)$ E near $(8,7)$  $(8,6)$ H near $(9,7)$  $(8,6)$ E near and H near occupy the same final full tile, but they are two distinct original terminal occurrences. The activation ledger therefore correctly counts four, not three:
$$A=4.$$
It follows that
$$C=3+0+2+2(13)+0+3=34,$$
and
$$2R=A+C=4+34=38,\qquad R=19.$$
6. The marked unactivated side and regular exit are exactly as claimedB’s bar occupies columns  $2,3$  in rows  $2,\ldots,7$ . It therefore owns every corner of A’s gate tile, including  $t=(3,2)$ . Canonical gate equivalence makes A’s near side marked.Nevertheless, the selected-support list contains both
$$(8,0),\qquad(9,1).$$
A’s original terminal  $(8,1)$  is unactivated.The next forced support is
$$q=(8,2)=B(0,7),$$
and its endpoint owner is F. This point is outside A’s original terminal tile. Its adjacency to A’s terminal does not consume either of the two displayed terminal supports.The exit profile is original regular  $2P1T$ Under F’s frame
$$F(r,c)=(14-c,6-r),$$
the exit tile has these exact inverse coordinates:Physical pointF original coordinatesOriginal role $(8,2)$  $(4,6)$ Far terminal endpoint $(8,3)$  $(3,6)$ Its matched predecessor $(9,2)$  $(4,5)$ Empty $(9,3)$  $(3,5)$ Selected supportThe original matching edge
$$(3,6)\text{--}(4,6)$$
is transported to
$$(8,3)\text{--}(8,2).$$
The support  $(9,3)$  survives in the final selected set, and  $(9,2)$  belongs to neither the endpoint union nor the support union.Thus this is the same original regular  $2P1T$  pair of F, not merely an arbitrary final tile with two endpoints. No other source contributes a point to that tile.It contributes zero to the listed non-A reserve classes and contains no original positive terminal activation. Relabeling it  $2P0T$  would spuriously add two units to  $C$ , equivalently one unit to  $R$ .7. The marks and path counts give  $\mu=19$ The six positive side occurrences have the following gates:SideGateStatusA near $(3,2)$ Consumed by negative B, full barA far $(3,13)$ Consumed by positive E, pairE near $(7,10)$ Consumed by negative DE far $(4,10)$ UnmarkedH near $(10,8)$ UnmarkedH far $(17,8)$ UnmarkedHence  $G=3$ .There is exactly one transfer:
$$A_{\mathrm{far}}\xrightarrow{P}E_{\mathrm{far}}.$$
The recipient normalization is consistent with the manifest: naming E’s physical far leg first gives the transported canonical P-recipient frame. Its incident length is four, and D supplies the corresponding transverse height six.The five path components are:PathBalance $A_{\mathrm{far}}\to E_{\mathrm{far}}$ , activated root and unmarked sinkSurplus  $2$ Isolated E near, activated and markedExactly paidIsolated A near, unactivated and markedDeficit  $1$ Isolated H near, activated and unmarkedSurplus  $2$ Isolated H far, unactivated and unmarkedSurplus  $1$ This verifies
$$q_{\mathrm{neg}}=2,\qquad
B_{\mathrm{bad}}=1,\qquad
S_{\mathrm{unmarked}}=5.$$
In particular, A’s near side is genuinely isolated: its lack of activation rules out an incoming transfer, and its negative-U gate consumer supplies no outgoing S/P/R transfer.Finally,
$$\boxed{\mu=N+R-G=3+19-3=19>0,}$$
and
$$\boxed{2\mu=34+5-1=38.}$$
8. Exactly which local rules are refutedThe complete connected witness disproves these two universal immediate implications:A full-bar gate consumer must activate the positive producer’s incident terminal.B consumes A’s gate with a full original bar tile, while A’s two original terminal supports remain selected.The next forced support consumption at such an unactivated exit must create a positive reserve defect in the specified adjacent exit tile.B’s forced support  $(8,2)$  is consumed by F, but that adjacent tile remains an original regular  $2P1T$  pair with zero reserve contribution.The second conclusion is local to that exit tile. The witness does not rule out a receipt elsewhere in F, compensation elsewhere in the family, or payment through a longer continuation. Its actual  $C=34$  and  $\mu=19$  make that distinction explicit.This acceptance concerns the written catalogue, clearance proof, and the concrete geometric and ledger argument above. It does not certify the reported executions, the unbounded formal adapter, the unadopted corridor leads, a universal coefficient improvement, or a grid theorem.
