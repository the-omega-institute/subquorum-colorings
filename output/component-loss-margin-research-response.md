I do not have a proof of the full unrestricted allocation inequality, or a complete physical counterexample. I can establish two new geometric payment results, including a stronger signed-loss theorem:
$$\boxed{\quad
2L\le 2R(\mathcal H)-A(\mathcal H)-m_8(\mathcal H).
\quad} \tag{1}$$
Here  $m_8$  counts a precisely defined class of marked pair recipients. Each occurrence has a distinct actual  $U_0$  or  $L_3$  capacity which survives every complete extension. These capacities are already in the reserve identity; the proof protects them against loss and uses each once.The other result is unrestricted in its local dimensions: all positive and rotor canonical gate consumers admit an injective transfer into actual positive activations. This reduces the unpaid demand to distinct negative-U endings, with an explicit allocation along paths. The  $m_8$  theorem pays one substantial class of those endings.The full missing inequality remains unproved for the other negative-U endings. I describe that boundary after proving the results.1. Units, gates, and what must be paidWrite
$$C:=U_0+Z_0+H,
\qquad 2R=A+C.$$
Work in doubled units. Each of the two side occurrences of a positive source has one base unit, giving  $2N$  units altogether. Each actual activated positive terminal contributes one additional unit to  $A$ . Each marked side requires two units. Thus
$$2\mu=2N+A+C-2G. \tag{2}$$
An activation means that at least one of the original positive terminal’s two intratile supports is consumed. Consuming both still contributes only one unit.Normalize a positive producer as  $U(w,\ell,\ell')$ , with its relevant side on the left, and put
$$t=(3,2),\qquad p=(2,2),\qquad
z=(2,3),\qquad y=(3,3).$$
Its canonical tile is  $Q=\{2,3\}^2$ . All other owners remain in the complete ambient family.A marked side is exactly a consumed canonical supportThis follows directly from complete feasibility.The three possible trigger points are  $p=(2,2)$ ,  $(4,2)$ , and  $z=(2,3)$ . An endpoint at either of the first two gives the original support  $t$  an extra occupied neighbor, forcing its consumption.If  $z$  is an endpoint, its original occupied degree is at least three. Unless  $p$  or  $y$  is occupied, it has only the two possible occupied neighbors  $(1,3)$  and  $(2,4)$ . Hence  $p$  or  $y$  is occupied, again forcing consumption of  $t$ .Conversely, if  $t$  is an endpoint, its original occupied degree forces  $p$  or  $(4,2)$  to be occupied: the west and east neighbors alone cannot provide degree three. Either occupied point must be an endpoint. At  $p$ , two fixed producer endpoints prohibit a retained support; at  $(4,2)$ , the producer endpoint  $(4,1)$  and the endpoint  $t$  do so.Consequently every marked side has one well-defined actual endpoint consumer of  $t$ .All normalizations below preserve the physical tile partition. In particular, exchanging a positive source’s two legs uses  $c\mapsto w+1-c$ , which preserves tiles because  $w$  is even. Unequal leg lengths and every allowed orientation are retained.2. An unrestricted injection for positive and rotor consumersThere are three transfer types. Their recipients are actual activated positive terminal occurrences.TypeConsumer of the canonical supportRecipient of the transfer $S$ Positive terminal singletonThat consuming terminal $P$ Positive bar-end pairThe terminal on that bar-end’s incident leg $R$ Negative rotor portA forced positive companion terminalI will prove that all three types together have injective recipients.2.1 Positive consumers: exactly  $S$  and  $P$ A positive original tile is a terminal singleton, a regular pair, or a full bar tile.A positive full tile cannot consume  $t$ : its endpoint at  $p$  would require a further own endpoint north or west, where the original producer already has endpoints.A vertical positive pair  $\{p,t\}$  is also impossible. Its endpoint  $p$  would have only one own endpoint neighbor, making it a terminal; a positive terminal has an original singleton profile.This leaves precisely the following two forms.Singleton form  $S$ . If the receiving terminal has incident length  $b$ , the receiver’s frame is
$$S_b(r,c)=(b+3-r,\,3-c).$$
Its terminal is  $t$ , with original intratile supports  $p,y$ . The support  $p$  is necessarily consumed, so the terminal is activated.There is an additional useful fact: the producer’s corresponding terminal is activated too. The receiver’s bar intersects the producer’s column-one stem unless
$$b\ge \ell.$$
Its column-two stem then contains  $(\ell+1,2)$ . That occupied point forces consumption of the producer’s original terminal support  $(\ell+1,1)$ .Pair form  $P$ . The only positive pair form has endpoints  $\{t,y\}$ , with  $t$  its upper bar corner. Its frame is
$$T(r,c)=(c+2,\,r+2). \tag{3}$$
Let  $a$  be its incident leg length. Its original support at  $p$  invokes your unrestricted transverse-tip theorem. The forced third source has frame
$$C(r,c)=(c+1,\,h+2-r),
\qquad 4\le h\le w-4.$$
The receiver’s incident stem must stop before this transverse source’s bar. Therefore
$$4\le a\le h-2\le w-6. \tag{4}$$
In particular, a positive pair consumer requires  $w\ge10$ .The receiver’s terminal is at  $(3,a+2)$ . Its original outer support  $(2,a+2)$  belongs to  $C$ , so this terminal is activated.These two cases exhaust positive consumers. The distinction matters: an  $S$  transfer activates both its producer and recipient; a  $P$  transfer has no general producer-activation conclusion.2.2 All rotor roles reduce to one negative rotorThe complete rotor classification gives the following stronger all-width statement.Rotor-consumer theorem. A rotor can consume a positive canonical support only in the footprint
$$\begin{aligned}
P_B=\{&
(3,2),(4,2),(4,3),(4,4),\\
&(5,1),(5,2),(5,3),(6,3)\}.
\end{aligned} \tag{5}$$
It is the negative phase- $00$  rotor. The producer’s relevant leg has length  $4$ , its terminal is activated, and a further positive activated terminal is forced at  $y=(3,3)$ . The producer width is at least  $12$ .Here is the exhaustive role argument.A rotor has four central endpoint roles and four tip roles in each chirality. Six of the eight central roles require an own endpoint at the occupied west neighbor  $(3,1)$ . The remaining two force an endpoint at  $(2,1)$  or  $(4,1)$ , also belonging to the producer.The west-pointing tips are immediately excluded. The north-pointing tips force  $(2,1)$  or  $(1,1)$ ; one south-pointing tip forces  $(4,1)$ ; and one east-pointing tip forces  $(1,3)$ .The remaining east-pointing footprint is
$$\{(3,2),(3,3),(4,3),(5,3),
  (2,4),(3,4),(4,4),(4,5)\}.$$
It has original support  $p=(2,2)$ . Your transverse-tip theorem forces a U terminal at  $p$  pointing right, which necessarily owns  $(2,4)$ . That conflicts with this rotor footprint. Thus only (5) survives.Because (5) contains  $(5,1)$ , the producer’s leg must have length  $4$ . The rotor consumes its beyond-tip support  $(5,1)$ , activating the terminal  $(4,1)$ .For the forced companion, the rotor’s original support  $p$  gives the transverse source
$$C(r,c)=(c+1,h+2-r),
\qquad 4\le h\le w-4.$$
This source has original support  $y=(3,3)$ . The support sees additional rotor endpoints and must be consumed. At  $y$ , north, west, and south are already endpoints of  $C$  or the rotor, so its consumer has exactly one own endpoint neighbor, to the east.Both rotor-tip possibilities there collide with  $(2,4)\in P_C$  or  $(4,4)\in P_B$ . The consumer is therefore a U terminal pointing east. Its bar must run south, giving the frame
$$V_g(r,c)=(c+2,\,g+3-r). \tag{6}$$
Its stem must stop before  $C$ ’s bar, so
$$4\le g\le h-4,
\qquad h\le w-4. \tag{7}$$
The map (6) preserves tiles, making this companion positive. Its two original intratile supports,  $(2,3)$  and  $(3,2)$ , are consumed by  $C$  and the rotor. It is an actual activated terminal.In particular,  $w\ge12$ . This excludes rotor gate consumers at widths  $6,8,10$ , while retaining every rotor phase and chirality in the proof.2.3 Why no activation recipient is used twiceFirst, distinct positive side occurrences have distinct canonical physical tiles. There is a short uniform proof.Translate a canonical tile to  $\{0,1\}^2$ . Its positive producer contains the fixed endpoint set
$$E=\{-2,-1\}\times[-1,4]\;\cup\;[0,2]\times\{-1\}. \tag{8}$$
Every D4 image of  $E$  about the tile center intersects  $E$ . For identity and column reflection, use  $(-1,0)$ ; for row reflection, transpose and a  $270^\circ$  rotation, use  $(0,-1)$ ; the remaining three cases intersect at  $(-1,2)$ . Thus two different positive producers cannot have the same canonical tile. The two sides of one producer have different tiles because  $w\ge6$ .It follows that two  $S$  receipts cannot use the same terminal. Two  $P$  receipts cannot either: the target terminal determines its incident upper bar corner, hence the consumed canonical support and tile.The mixed collisions require geometry.A  $P$  recipient cannot also be an  $S$  recipient. In the pair receiver’s own frame, its forced transverse source is
$$(r,c)\mapsto(h-r,c-1)$$
and owns column zero through rows  $0,\ldots,h$ . The recipient terminal is  $(a,1)$ , with  $a+2\le h$ . A positive singleton producer for that same terminal would have frame  $S_a$ ; its endpoint  $(1,3)$  would map to
$$(a+2,0),$$
already owned by the transverse source.Two  $R$  receipts cannot coincide. For the forced positive companion, its beyond-tip original support is exactly the rotor port  $t$ . A common recipient terminal therefore fixes the same port and its unique rotor owner. Of the port’s two neighbors outside its tile, one is the rotor’s own predecessor; the other uniquely identifies the positive producer’s anchor and side.An  $R$  recipient cannot be an  $S$  recipient. At the companion  $y=(3,3)$ , the two possible outside-tile producer anchors are  $(3,4)$  and  $(4,3)$ . They already belong to the companion and the rotor.An  $R$  recipient cannot be a  $P$  recipient. Using (3) and (6), the hypothetical pair producer would have frame
$$V_g\circ T^{-1}(r,c)=(r,g+5-c).$$
Its endpoint  $(0,1)$  would lie at  $(0,g+4)$ , on the original producer’s bar, because  $g+4\le h\le w-4$ .This proves the unrestricted injection
$$\boxed{
\#\{\text{marked gates consumed by a positive source or rotor}\}
\le A.
} \tag{9}$$
Equation (9) identifies actual units already counted in  $A$ .3. A single-use transfer along physical pathsMake the  $2N$  positive side occurrences the vertices of a directed graph. For every  $S,P,R$  transfer, draw an edge from its marked producer side to its activated recipient terminal.Outdegree is at most one because a canonical support has one endpoint consumer. Indegree is at most one by the preceding injection. The graph is therefore a disjoint union of directed paths and cycles, including isolated vertices.Give vertex  $v$  its base unit  $b_v$ , and, when activated, its actual activation unit  $\alpha_v$ . For each edge
$$v\longrightarrow w,$$
pay the mark at  $v$  with
$$b_v+\alpha_w. \tag{10}$$
Every label in (10) is used at most once.On a path
$$v_0\longrightarrow\cdots\longrightarrow v_k,$$
all marks except a possible mark at  $v_k$  are paid. The remaining positive units are precisely
$$b_{v_k},
\qquad
\alpha_{v_0}\ \text{if the initial vertex is activated}.$$
Thus:An unmarked endpoint leaves  $1+a(v_0)$  units unused.A marked endpoint is fully paid if the initial vertex is activated.A marked endpoint with an unactivated initial vertex needs exactly one further unit.Every cycle pays all its marks exactly.Every marked path endpoint has a negative U consumer. A positive or rotor consumer would have supplied another edge.Let  $\mathcal B$  be the paths with unactivated initial vertex and marked endpoint, and let  $\mathcal U$  be the paths with unmarked endpoint. Then the explicit allocation gives
$$2\mu
=
C+\sum_{P\in\mathcal U}(1+a(s(P)))-|\mathcal B|. \tag{11}$$
The substantive content of (11) is the physical, injective construction (10). In particular, no bad nontrivial path begins with  $S$  or  $R$ , since those would activate its initial vertex.This allocation persists from a marked hull to every legal extension preserving all positives and marks. The positive recipients are retained; preservation of a marked side forces its actual canonical-support consumer; and all activation witnesses used above persist.The next theorem supplies non- $A$  payments for some of the remaining negative-U endpoints.4. A minimal pair attachment has a permanently unmarked recipientConsider a  $P$  transfer. In its recipient’s frame, write the positive recipient and forced transverse source as
$$B=U(W,a,b),\qquad
C(r,c)=(h-r,c-1).$$
If  $h=6$ , (4) forces  $a=4$ .Put  $m=\min(W,V-1)$ , where  $V$  is  $C$ ’s width. The entire boundary of
$$[1,5]\times[1,m] \tag{12}$$
consists of endpoints of  $B,C$ .The top is  $B$ ’s bar. The left side is  $B$ ’s near leg completed by  $C$ ’s bar. The bottom is  $C$ ’s bar. The right side is supplied by the nearer of the two far legs; their minimum allowed length four suffices.The recipient’s canonical support  $(3,2)$  lies strictly inside (12), whose interior has only three rows.Every U endpoint graph is connected and has both bounding-box dimensions at least five. Every rotor endpoint graph is connected and has a  $4\times4$  bounding box. A different owner cannot cross the occupied endpoint boundary, and neither source type can fit inside it. Therefore no source can consume this support.So the recipient side is permanently unmarked in every complete extension.In particular,
$$\boxed{
\text{Every positive pair transfer from a width-10 producer ends at an unmarked side.}
} \tag{13}$$
This pays the whole transfer path ending there, using the labels in Section 3.5. A permanent, injective defect payment when  $a=6,\ h=8$ Here is the new non- $A$  capacity theorem.Protected-defect theorem. Suppose a positive side  $B$  receives a  $P$  transfer and, in its own frame,
$$B=U(W,6,b),\qquad
C=U(V,8,f),\qquad C(r,c)=(8-r,c-1).
\tag{14}$$
If that side of  $B$  is marked, it has a negative-U consumer and can be assigned one actual  $U_0$  or  $L_3$  occurrence which persists in every complete extension.These assignments are injective across all such marked recipients.Here  $W,V\ge6$  and  $b,f\ge4$  are arbitrary even parameters. All surrounding sources, phases and dimensions remain unrestricted.Let  $m_8$  count the marked recipients in (14). The theorem gives
$$\boxed{m_8\le U_0+L_3} \tag{15}$$
with actual nonrepeated receipts.5.1 Exhaustive consumer formsIn this frame,  $B$  owns  $(3,1)$  and  $(1,2)$ , while  $C$  owns  $(7,2)$ . Let  $D$  consume  $t=(3,2)$ .There are exactly three possible U forms:TypeSource and physical mapNecessary conditionsI $D=U(d,4,e)$ ,  $(r,c)\mapsto(r+2,c+1)$  $d+1<W$ II $D=U(d,4,e)$ ,  $(r,c)\mapsto(6-r,c+1)$ Further parameters governed by ambient feasibilityIII $D=U(d,g,e)$ ,  $(r,c)\mapsto(c+2,g+2-r)$  $V\le g\le W-4,\ f=4$ For Type I,
$$\begin{cases}
e=4,&d+1<V-1,\\
f=4,&d+1>V-1,
\end{cases}
\qquad
d+1=V-1\ \text{is impossible}. \tag{16}$$
The phases are respectively  $01,11,10$ , so all three consumers are strictly negative.To see exhaustiveness, a vertical U bar through  $t$  would require at least six consecutive endpoints in column two, but the blockers at rows one and seven leave only rows two through six.If  $t$  lies on a horizontal bar, its occupied west neighbor forces it to be the left bar end. It therefore belongs to the full bar-end/leg column interval. The same interval argument applies if it lies on a vertical leg. Such an interval has at least five vertices; it must be exactly rows two through six. This forces incident length four and gives I or II according to the bar’s end.Otherwise  $t$  lies on a horizontal leg. Its blocked west neighbor makes it the leftmost point. The bar-end possibility would require the excluded vertical bar, so  $t$  is an east-pointing terminal. Its bar cannot point north: avoiding  $B$ ’s top bar would make the stem cross  $B$ ’s far leg. The south-pointing form is III. Crossing  $C$ ’s row-seven bar forces  $g\ge V$ ; avoiding  $B(3,W)$  forces  $g\le W-4$ ; crossing  $C$ ’s far column forces  $f=4$ .The comparisons in (16) follow by checking the far-leg columns. Equality gives endpoint overlap.Finally, a rotor consumer would force the producer’s incident leg to be four by Section 2.2. Here it is six. Thus the classification covers every allowed consumer.5.2 Three height-three enclosures give the receiptsWe use the same enclosure principle as in (12). A missing point inside a rectangle with three strict interior rows cannot acquire an endpoint from any other complete source. In each case below, it is also absent from the specified owners’ original endpoint sets.Consumer caseEndpoint rectangleMissing pointPermanent receiptII $[1,5]\times[2,\min(W,d+1)]$  $(4,3)$  $D$ ’s near  $U_{11}$  capIII, or I with  $d+1>V-1$  $[3,7]\times[1,V-1]$  $(6,V-2)$  $C$ ’s far  $U_{11}$  capI with  $d+1<V-1$  $[3,7]\times[1,d+1]$  $(6,d)$ A mixed  $L_3$  tileFor completeness, the actual tiles are as follows.Type II. The top boundary comes from  $B$ , the left and bottom from  $D$ , and the right from the nearer far leg. When the right side is column  $W$ ,  $B$  supplies it through row four and  $D$ ’s bar supplies  $(5,W)$ . This covers  $b=4$ .The tile
$$\{4,5\}\times\{2,3\}$$
retains exactly
$$(4,2),\ (5,2),\ (5,3)\in P_D.$$
Its missing point  $(4,3)$  is trapped. This is one actual unfilled original  $U_{11}$  cap.Type III, or crossing Type I. Here  $D$  owns row three through columns  $2,\ldots,V-1$ , and  $f=4$ . Together with  $B$ ’s column-one leg and  $C$ ’s bar and far leg, these endpoints bound the second rectangle.The tile
$$\{6,7\}\times\{V-2,V-1\}$$
retains exactly
$$(6,V-1),\ (7,V-2),\ (7,V-1)\in P_C.$$
Its missing point  $(6,V-2)$  is trapped. This is  $C$ ’s actual far  $U_{11}$  cap.Short Type I. Here  $e=4$ . The third rectangle is bounded by  $B$ ’s near leg,  $D$ ’s bar and far leg, and  $C$ ’s row-seven bar.The tile
$$\{6,7\}\times\{d,d+1\}$$
retains exactly
$$\underbrace{(6,d+1)}_{\text{owner }D},
\qquad
\underbrace{(7,d),(7,d+1)}_{\text{owner }C}.$$
Its missing point  $(6,d)$  is trapped. This is one actual mixed  $L_3$  occurrence.Each missing point has two fixed endpoint neighbors. It therefore cannot become a retained support either. These are permanently exact  $3P0T$  tiles in every complete extension.5.3 The receipt injection, including the cross-type collisionTwo Type-II receipts at the same cap identify its owner and associated terminal. That terminal lies in  $B$ ’s marked canonical tile. Canonical-tile separation identifies the same side.Two receipts at the same far cap of  $C$  identify its opposite terminal—the transverse tip belonging to the preceding pair interaction. This identifies the preceding producer’s canonical tile, hence the same pair edge and recipient.There is one more substantial collision to exclude: a cap might appear as a Type-II receipt in one configuration and a far- $C$  receipt in another.Normalize the first cap owner as
$$F=U(d,4,e),\qquad F(r,c)=(6-r,c+1).$$
The first positive  $B$  owns  $(1,3)$ . For that cap to be a far- $C$  receipt elsewhere,  $F$ ’s other leg must be eight. The second recipient frame maps into the first by
$$\Psi(r,c)=(r-2,d+1-c),$$
because
$$\Psi(8-r,c-1)=(6-r,d+2-c),$$
which represents  $F$  with its legs exchanged.Every far- $C$  receipt requires its negative gate consumer to own second-frame row three in columns  $2,\ldots,d-1$ . Under  $\Psi$ , this becomes old row one in columns  $2,\ldots,d-1$ , including  $(1,3)$ .That point already belongs to the first positive  $B$ . The owners are distinct, so endpoint disjointness excludes the collision.Finally, a mixed  $L_3$  receipt has a unique actual  $2+1$  owner split. Its singleton is the specified terminal of  $D$ , which determines the opposite lower bar corner used as  $B$ ’s canonical support. Two such receipts therefore identify the same marked side.An original cap, with all three endpoints from one owner, cannot coincide with one of these mixed triples.This proves the global injection (15). Its receipt tiles contain only negative owners, so they are also separate from the positive activation occurrences used in Section 3.6. The stronger signed-loss theoremLet  $\mathcal H\subseteq\mathcal J$  be a legal marked hull and complete extension, preserving all positives and actual marks. Let  $B_j$  be the new endpoint components, and use your established component-cube theorem:
$$L=\sum_j\bigl(R(\mathcal H)-R(\mathcal H+B_j)\bigr)_+.$$
All owners needed for a certificate counted by  $m_8$  already lie in  $\mathcal H$ :The positive producer and recipient are retained.Their pair interaction forces the transverse owner  $C$ .The recipient’s preserved mark forces its actual canonical-support consumer  $D$ .Every legal component subunion therefore retains all  $A(\mathcal H)$  activation labels and the  $m_8(\mathcal H)$  distinct permanent defect labels.Choose precisely the components with negative reserve increment. Their feasible union  $\mathcal F_-$  satisfies
$$R(\mathcal F_-)=R(\mathcal H)-L.$$
Its actual geometric identity gives
$$2R(\mathcal F_-)
=
A(\mathcal F_-)+U_0(\mathcal F_-)+Z_0(\mathcal F_-)+H(\mathcal F_-)
\ge A(\mathcal H)+m_8(\mathcal H).$$
Hence
$$\boxed{
2L\le2R(\mathcal H)-A(\mathcal H)-m_8(\mathcal H).
} \tag{17}$$
This proves a sufficient margin-transfer criterion:
$$\boxed{
A(\mathcal H)+m_8(\mathcal H)\ge2(G-N)
\quad\Longrightarrow\quad
L\le\mu(\mathcal H).
} \tag{18}$$
No original negative mass is charged. No mixed full-tile credit is repeated. The permanent caps and triples are protected occurrences already contained in  $2R$ .In the path allocation, a marked  $m_8$  recipient is necessarily a negative-U endpoint. If its path has an unactivated initial vertex, its assigned  $U_0/L_3$  unit pays exactly the one outstanding unit. Thus the protected-defect theorem closes an actual part of the missing margin obligation.7. The remaining unrestricted problemThe results above establish:
$$\begin{gathered}
\text{an injective activation transfer for every positive and rotor gate consumer},\\
\text{permanently unmarked endings at transverse length six},\\
\text{distinct permanent defect payments at }(a,h)=(6,8),\\
\text{and the stronger general signed-loss bound (17).}
\end{gathered}$$
They do not establish that every residual negative-U endpoint reaches an unused actual capacity.One remaining geometric channel is the negative  $U_{01}$  full-bar consumer
$$D(r,c)=(r+2,c+1).$$
Its original full tile can own the producer’s canonical support without supplying a positive-activation receipt. When surrounding positive legs force consumption of its terminal supports, its original singleton capacities cannot simply be retained as available units. A general proof still has to follow those actual completions through negative bars and show that the resulting demands receive distinct surviving capacity.The width contractions and local cap restrictions alone do not complete that transport. Nor have I constructed a complete physical negative- $\mu$  family from this remaining channel.Accordingly, the unrestricted allocation target is unresolved here. The new contribution is the explicit, extension-stable payment above and its strict improvement of the aggregate loss bound. The broader grid triple equality remains open; a future allocation counterexample would still require actual negative ambient slack before it could furnish a grid counterexample.
