ACCEPTThe corrected package resolves both issues from the previous review.The standing model hypothesis now supplies the required exhaustive owner catalogue, and the corrected physical-phase calculation gives the exact selected-owner identity
$$\boxed{\Delta(N+S)=\sum_{j=0}^{n-1}\bigl(L_j^{(t)}-1\bigr)+n\ge6n.}$$
Within that explicitly restricted model, the ordinary proof establishes:the mandatory nine-endpoint footprint  $K_j$ ;exclusion of both specified right-band families, including unraised and raised  $g=4$ ;the necessary arbitrary-depth dichotomy;at least  $2n$  distinct fresh consuming originals;the corrected immutable charge inventory, with each selected original counted once.I find no remaining mathematical defect in those claims. This acceptance does not depend on the reported finite controls or Lean checks.1. The standing hypothesis is sufficient for the catalogue argumentThe corrected hypothesis explicitly restricts every actual original to a lattice-isometric image of a full permitted even U or the standard rotor, carrying its complete original endpoint, matching, and support sets.That supplies the missing logical implication. Once the consuming owner of  $y_j$  is shown to have exactly one own endpoint neighbor, the proof is entitled to exhaust the degree-one roles in those two families. It no longer relies on transferring a local classification at  $t_j$  to an otherwise unrestricted owner at  $y_j$ .The canonical matchings cover every endpoint:In a U, the bar matchings and the two even-depth leg matchings cover all endpoints.In the rotor, the four specified matching edges cover its eight endpoints.Thus a consuming original must supply a matching neighbor for  $y_j$ . With three neighboring sites already occupied by retained originals, endpoint disjointness forces that matching neighbor to be north.The proof therefore uses precisely the stated model assumption. It makes no claim that arbitrary grid configurations possess this catalogue.The full rotor roles are exhaustedThe rotor has four degree-one tips and four core vertices of own degree three. Since  $y_j$  has only one available own neighbor, a core role is impossible.Quarter-turn symmetry reduces the tip placements with own neighbor north to one normalized endpoint set; reflection gives the other chirality. These are exactly the two full sets displayed in the note.The first contains the relative point  $(-1,-1)$ , giving the retained endpoint
$$(a-2,C-1)\in P_j^0.$$
The second contains  $(-1,1)$ , giving
$$(a-2,C+1)$$
in the root or preceding  $V$  leg.Both rotor roles are therefore excluded. No cropped-tip approximation or unexamined rotor role is involved.The two U frames are exhaustiveEvery nonterminal U endpoint has at least two own endpoint neighbors, so  $y_j$  must be a leg terminal.The north matching direction fixes the incident leg’s vertical direction. Exchanging the two legs allows that terminal to be designated canonical  $(d,1)$ . For even breadth, this exchange preserves the full matching and exchanges the support formulas correctly.The remaining horizontal choices are precisely
$$(r,c)\mapsto(a-1-d+r,C+1-c)$$
and
$$(r,c)\mapsto(a-1-d+r,C-1+c).$$
Thus the catalogue-to-coordinate argument is now complete under the standing hypothesis.2. The retained geometry forces the nine-site footprintFix block  $j$ , and write
$$a=a_j,\qquad s=s_j,\qquad u=w_j,\qquad C=s+u+13.$$
The recurrence preserves odd  $a$  and even  $s$ , so  $C$  is odd.The identification of
$$y=(a-1,C)$$
as an original  $E_j$  support is exact:
$$(5,6)\longmapsto(a+4-5,\ s+u+7+6)=(a-1,C).$$
The neighboring column intervals are correctFrom the full original charts, the relevant occupied intervals are:Retained originalColumnOccupied rows $P_j^0$  $C-1$  $[a-8,a+2]$ Root, when  $j=0$  $C+1$  $[a-6,a]$  $V_{j-1}$ , when  $j>0$  $C+1$  $[a-z_{j-1},a]$ The root interval includes its canonical row-0 endpoint at
$$(a-6,C+1).$$
That endpoint is essential to the depth- $6$  exclusion.For  $j>0$ , the earlier- $V$  interval follows from
$$s_{j-1}+2=C+1$$
and
$$a_{j-1}-6=a-z_{j-1}.$$
Its far column contains every canonical row from  $0$  through  $z_{j-1}$ , so both ends of the stated interval are included.These intervals give the three retained neighbors of  $y$ : west in  $P_j^0$ , south in  $E_j$ , and east in the root or earlier  $V$ .Freshness holds against the entire old inventoryThe assertion that  $y$  is absent from H3 is correct.Within its own block,  $P_j^0$  and the left-reaching originals miss the specified column or row; the source rotor begins at column  $C+1$ ; and the relevant  $E_j$  and  $C_j$  endpoints begin at row  $a$  or below.For earlier blocks, the base originals lie at columns at least  $C+1$ , while the earlier supplementary originals end by
$$a_{j-1}+2\le a-16.$$
Later blocks begin at least at row  $a+10$ . The root also misses  $y$ .Therefore an actual consuming owner is fresh. Completeness forces such an owner because an unconsumed support at  $y$  would already have three occupied neighbors.Its west, south, and east neighbors belong to retained originals. Its own matching neighbor must be north, and it has exactly one own endpoint neighbor.Every shallow U depth is correctly excludedFor a left frame, the lower-bar endpoint  $(1,2)$  maps to
$$(a-d,C-1).$$
At  $d=4,6,8$ , this hits  $P_j^0$  at rows
$$a-4,\qquad a-6,\qquad a-8.$$
The last collision uses  $P_j^0$ 's row-0 bar endpoint. Hence
$$d_{\mathrm{left}}\ge10.$$
For a right frame, the same endpoint maps to
$$(a-d,C+1).$$
At  $j=0$ , depths  $4$  and  $6$  hit the root. The second collision is exactly the root’s row-0 endpoint at  $a-6$ , so
$$d_{\mathrm{right}}\ge8.$$
At  $j>0$ , the earlier  $V$  column blocks every even depth
$$4\le d\le z_{j-1}.$$
This includes equality, through the earlier  $V$ 's row-0 endpoint. Consequently
$$d_{\mathrm{right}}\ge z_{j-1}+2.$$
These arguments establish necessary lower bounds; they do not assert that every remaining frame is realizable.The footprint includes all nine endpointsIn either U frame, the incident column  $C$  is occupied continuously from
$$a-1-d
\quad\text{through}\quad
a-1.$$
The bar supplies canonical rows  $0,1$ , and the leg supplies rows  $2,\ldots,d$ .Since every surviving frame has  $d\ge8$ ,
$$[a-9,a-1]\subseteq[a-1-d,a-1].$$
Thus
$$\boxed{
K_j=\{(r,C):a-9\le r\le a-1\}
\subseteq\operatorname{End}(R_j).
}$$
This is an all-parameter consequence of the full-original geometry.3. Both right-band families are impossible as actual ownersFor a right owner of  $t_{j+1}$  with breadth  $u+v+26$  and incident depth  $D$ , its bar begins at
$$b=a+z-10-D,$$
and its far column is
$$s'-1+(u+v+26)=C.$$
That column contains every row in
$$[b,b+g].$$
For the two specified families,
$$D=z+2k,\qquad k\in\{0,1\},$$
so
$$b=a-10-2k.$$
The site  $(a-8,C)$  has intrinsic row
$$2+2k,$$
which is  $2$  or  $4$ . Therefore it belongs to  $B$  for every  $g\ge4$ .It also belongs to the mandatory footprint  $K_j$ .The two owners are distinctAn endpoint-disjoint candidate cannot reach the retained  $E_j$  endpoint  $(a,C)$ . For these two bar positions, this requires
$$g\le8+2k.$$
Its far-column terminal is consequently at most  $a-2$ , so  $B$  misses
$$y=(a-1,C).$$
It is therefore distinct from  $R_j$ .The two distinct originals would then share endpoint  $(a-8,C)$ , contradicting endpoint disjointness.Any greater even  $g$  already collides with retained  $E_j$ . Thus every far-depth choice is excluded for both  $D=z$  and  $D=z+2$ , including both  $g=4$  cases.This proves the claimed vacuity of those complete-family hypotheses in the stated model. It does not assume that H3 has a complete extension: the argument assumes an extension containing the specified  $B$  and derives a contradiction.The exclusion is independent of the earlier  $22$  and  $44$  receipt values. It neither needs those calculations nor changes a correctly established identity for an incomplete selected inventory.4. The arbitrary-depth dichotomy is exact as a necessary avoidance conditionFor general even  $D,g$ , the far-column interval is
$$I=[a+z-10-D,\ a+z-10-D+g].$$
Both endpoints have odd row parity.First, a geometrically endpoint-disjoint  $B$  cannot contain  $y$ . If its far interval contained the even row  $a-1$ , its odd terminal row would necessarily be at least  $a$ . Continuity would then force the retained endpoint  $(a,C)$  into  $B$ .Therefore  $B\ne R_j$  for every admissible  $D$ , including choices whose bar begins below  $E_j$ .Its far interval must consequently avoid both  $K_j$  and the retained  $E_j$  endpoint. These together occupy every integer row in
$$[a-9,a].$$
A contiguous interval with odd endpoints avoids this block exactly when either
$$\max I\le a-10$$
or
$$\min I\ge a+2.$$
Substituting the endpoints gives
$$D-g\ge z$$
or
$$D\le z-12.$$
Hence
$$\boxed{D\le z-12\quad\text{or}\quad D-g\ge z}$$
is correct.In the deep alternative,  $g\ge4$  implies
$$D\ge z+4.$$
At equality,  $D=z+4$ , the condition forces  $g=4$ .These are the first values not excluded by this necessary footprint test. The note correctly leaves further old collisions, geometric admissibility, and complete extendibility unresolved.5. The  $2n$  sites and their consuming owners are all distinctThe revised column argument is correct.For the  $t_j$  sites,
$$s_j-s_{j+1}=w_{j+1}+12>0.$$
Their columns therefore strictly decrease.For the  $y_j$  sites,
$$C_j=s_j+w_j+13,$$
while
$$C_{j+1}
=s_{j+1}+w_{j+1}+13
=s_j+1.$$
Thus
$$\boxed{C_j-C_{j+1}=w_j+12>0.}$$
Every  $t_j$  column is even and every  $y_j$  column is odd, so the two site families cannot intersect. Together these facts prove that there are exactly  $2n$  distinct forced sites.Their checkerboard colors agree:
$$(a_j-4)+s_j\equiv1\pmod2,$$
and
$$(a_j-1)+C_j\equiv1\pmod2.$$
Under the supplied  $t_j$  role exclusions and the now-justified  $y_j$  role exclusions, each site is a terminal of its consuming U. The two terminals of a permitted even U have opposite colors:
$$(d,1)\text{ has odd color},\qquad
(f,L)\text{ has even color}.$$
A lattice isometry preserves their having opposite colors, even if it interchanges the two color classes.One original cannot therefore own two of these distinct same-color forced sites. All their owners are fresh because the sites are absent from H3.Consequently, the selected set consists of
$$\boxed{2n\text{ distinct fresh originals}.}$$
This is the owner-level nonreuse result required for the subsequent ledger.6. The corrected full-original charge counts are validFor a  $y_j$ -owner, put
$$p=\frac{d+f}{2}.$$
A full  $U(L,d,f)$  has
$$2L+d+f-2$$
endpoints, so its perfect matching has
$$M=L+p-1$$
edges.The crucial phase is now handled correctly:  $y$  has even row and odd column, and the bar origin  $a-1-d$  is even. Both bar rows lie in one physical tile row.Left  $y$ -ownerThe bar columns run from
$$C+1-L\quad\text{to}\quad C,$$
an even-to-odd interval. The bar occupies  $L/2$  endpoint tiles.The legs add  $d/2+f/2=p$  tiles, including their terminal tiles. Therefore
$$T_{\mathrm{left}}=\frac L2+p.$$
The original supports inside endpoint tiles are:the odd-intrinsic-row inward lateral supports, totaling  $p-2$ ;both axial terminal supports, adding  $2$ .The axial supports belong to the terminal endpoint tiles because each terminal has even absolute row and its axial support has the next odd row. The bar-exterior supports and even-row lateral supports lie outside this original’s endpoint tiles.Hence
$$J_{\mathrm{left}}=p,$$
and
$$\operatorname{charge}_{\mathrm{left}}
=(L+p-1)+p-2\left(\frac L2+p\right)
=\boxed{-1}.$$
Right  $y$ -ownerThe bar columns run from odd  $C$  to even  $C-1+L$ , so the bar meets  $L/2+1$  physical tile columns. Including the legs,
$$T_{\mathrm{right}}=\frac L2+1+p.$$
The counted original supports are:the even-intrinsic-row lateral supports, totaling  $p$ ;both axial terminal supports;both bar-exterior supports in the two partial edge tiles.Thus
$$J_{\mathrm{right}}=p+4,$$
and
$$\operatorname{charge}_{\mathrm{right}}
=(L+p-1)+(p+4)
-2\left(\frac L2+1+p\right)
=\boxed{+1}.$$
The corrected symbolic table is exact: $y$ -owner frameMatching edges  $M$ Endpoint tiles  $T$ Original supports inside them  $J$ ChargeLeft $L+p-1$  $L/2+p$  $p$  $-1$ Right $L+p-1$  $L/2+1+p$  $p+4$  $+1$ These are full-original counts. In particular, an axial support remains counted even when another original consumes it. The incident axial support of  $R_j$  is at the retained  $E_j$  terminal; its consumption does not remove it from  $J$ .The earlier  $t_j$ -owner charge remains  $1-L$ For comparison, the  $t_j$ -owner bar origin is odd. With the same notation  $p=(d+f)/2$ , its full-original counts are: $t$ -owner frame $M$  $T$  $J$ ChargeLeft $L+p-1$  $L+p$  $p+2$  $1-L$ Right $L+p-1$  $L+p-2$  $p-2$  $1-L$ Thus the correction properly distinguishes the two physical phases despite their common checkerboard color.7. The exact selected-owner ledger counts each original onceLet the selected originals be the  $n$  owners of the  $t_j$  sites and the  $n$  owners of the  $y_j$  sites. Section 5 establishes that these are  $2n$  distinct originals, all outside H3.Let  $n_L,n_R$  count the  $y_j$ -owners in the two frames. Then
$$n_L+n_R=n.$$
Their contributions are:Selected originalContribution to  $S$ Contribution to  $N$ Owner of  $t_j$  $L_j^{(t)}-1$  $0$ Left owner of  $y_j$  $1$  $0$ Right owner of  $y_j$  $0$  $1$ Because  $N$  and  $S$  are sums of immutable per-original contributions, adding these selected owners to H3 gives exactly
$$\boxed{
\Delta S=\sum_j\bigl(L_j^{(t)}-1\bigr)+n_L,
\qquad
\Delta N=n_R.
}$$
Consequently,
$$\boxed{
\Delta(N+S)
=\sum_j\bigl(L_j^{(t)}-1\bigr)+n.
}$$
Every  $L_j^{(t)}\ge6$ , so
$$\boxed{\Delta(N+S)\ge6n.}$$
There is no reuse of a source charge:no selected owner is an old H3 original;no selected owner serves two of the forced sites;every selected owner appears once in the ledger;consumption changes none of the original charges.The word selected also has the correct scope. The identity concerns these  $2n$  forced owners; it does not assert that a complete family contains no additional originals.The note correctly refrains from converting this into a net  $\Phi$  bound. Full-tile completions and directed events can involve multiple originals, and their contributions still require separate control.Acceptance scopeThis is an ACCEPT of the corrected ordinary theorem within the explicitly stated complete feasible U/rotor-family model.The global catalogue restriction now justifies the owner-role classification. The nine-site footprint, both branch exclusions, the arbitrary-depth dichotomy, and the distinct-owner count follow. The corrected  $-1/+1$  charge calculation yields the exact selected-owner  $N+S$  identity without reconstructing or reusing an original.No existence of a complete extension is asserted. No exhaustion theorem for arbitrary grid configurations is inferred. The reported finite controls and scoped Lean results are separate validation claims; I have neither used them as substitutes for proof nor treated this audit as their execution certification.
