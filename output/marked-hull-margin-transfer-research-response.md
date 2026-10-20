I have not proved the unrestricted allocation inequality or constructed a complete physical violation. The target
$$\mu=N+R-G=n_0+R-n_2\ge0$$
remains unresolved in this investigation.I can, however, prove two general results that address the signed-loss problem without restricting dimensions, phases, orientations, or U/rotor mixtures:Every legal extension factors over its connected groups of new endpoints. Feasibility, reserve, marked demand, and margin all factor exactly. This gives a bound on aggregate reserve loss using actual old geometric capacity units once.Every complete  $q$ -source family admits physical compression into a  $52q$ -square. Compression preserves every marked side and changes the margin only by removing actual sole irregular-bar tiles. The same compression can be applied simultaneously to a legal extension, isolating all loss caused by arbitrarily long repetitive interfaces.There is also a sharper separator consequence: the duplicate-mark correction  $d_s$  is always zero under complete-source feasibility, not merely zero in a source-minimal counterexample.The missing step is precise: the old capacity units identified by these results have not been proved to be available after paying the old marked demand. I will keep that distinction explicit.1. Framework and scopeWrite a complete family  $X$  as
$$P_X=\bigcup_{i\in X}P_i,\qquad
O_X=\bigcup_{i\in X}(P_i\cup T_i),\qquad
T_X=O_X\setminus P_X.$$
Thus consumed supports remain occupied, and every support outside the final endpoint set remains mandatory.The arguments below retain the full catalogue: even U widths  $w\ge6$ , independently even heights  $L,H\ge4$ , all translations and lattice orientations, every effective phase, and arbitrary mixtures with the complete rotors. The source-profile facts used below are those of the all-phase complete-source catalogue.I use your established identities
$$R(X)=S(X)+2|F_{\mathrm{mix}}(X)|-|E(X)|
\tag{1}$$
and
$$2R(X)=A(X)+U_0(X)+Z_0(X)+H(X),
\tag{2}$$
with all events, full tiles, activations, and defects counted in their actual original ownership. These agree with the signed-extension ledger and exact geometric reserve identity.All capacity accounting below uses (2). Original source mass and full-tile credit are not added to it as further payment pools.2. General component transfer theoremLet  $I\subseteq J$  be complete feasible families.Form the graph induced by the new endpoints
$$P_J\setminus P_I,$$
using unit lattice edges between those endpoints. Let its connected components determine new-owner sets
$$B_1,\ldots,B_m.$$
Each original source has a connected endpoint set, so an entire new source belongs to one  $B_j$ .Put
$$K_j=I\cup B_j,\qquad
X_T=I\cup\bigcup_{j\in T}B_j
\quad(T\subseteq\{1,\ldots,m\}).$$
Theorem 1Every  $X_T$  is complete feasible. Moreover, for each
$$Q\in\{R,N,G,\mu\},$$
one has
$$\boxed{
Q(X_T)=Q(I)+\sum_{j\in T}\bigl(Q(K_j)-Q(I)\bigr).
}
\tag{3}$$
In particular, new positives and new marked sides are allowed. Preservation of  $N,G$  is not a hypothesis of this theorem.This is a statement about a geometrically defined collection of legal subextensions. It does not assert modularity on the entire feasible-source lattice.2.1 Complete feasibility, including restored support/support conflictsTake a mandatory selected point  $x\in T_{X_T}$ .If  $x$  is selected in  $J$ , it remains safe because
$$O_{X_T}\subseteq O_J.$$
Otherwise  $x$  is an endpoint of an omitted new component: it is a support restored by the restriction. Choose a retained producer of  $x$ , with original anchor  $a$ .That producer cannot be new. If it were, the endpoint edge  $a--x$  would put the producer and omitted consumer in the same new component. Consequently the producer is in  $I$ , and  $x$  is selected—and safe—in  $I$ .Suppose  $x$  nevertheless has an additional occupied neighbor  $y\ne a$  in  $X_T$ . Feasibility of  $I$  gives
$$y\notin O_I.$$
If  $y$  is a retained endpoint, it is new, and its edge to  $x$  joins a retained and an omitted new component, a contradiction.If  $y$  is a retained original support, its producer must be new because  $y\notin O_I$ . Let  $b$  be that producer’s retained endpoint anchor. In  $J$ , the point  $y$  has occupied neighbors  $b$  and  $x$ , so it cannot remain selected. It must be consumed into an endpoint. This consumer is new, and the edge  $b--y$  places it in the retained producer’s component. But  $y--x$  then joins that retained component to the omitted component, again a contradiction.Thus every restored support has its unique occupied neighbor. Endpoint disjointness and the retained original matching are unchanged; original occupied sets ensure endpoint degree at least three.This proves actual complete feasibility of every  $X_T$ .2.2 Actual events and full tiles partition onceEvery fresh directed event involves one new component. If both its producer and consumer are new, the event itself is an endpoint edge joining them.For full tiles, first observe that the endpoint set of a nonempty tile in any complete feasible family is connected. The only potentially disconnected nonempty profile is a diagonal pair. Such a pair is impossible: each original singleton has an intratile support, and a support at either remaining corner would see both diagonal endpoints unless consumed, producing a third endpoint.Now consider a tile newly full in  $J$ . Its old endpoint set has size  $0,1,2$ , or  $3$ . When it has two endpoints, they are adjacent. In every case, the complementary new corners are connected. They therefore belong to one new component.Hence every fresh event and every newly mixed full tile is assigned to exactly one  $B_j$ . Together with sourcewise additivity of  $S$ , equation (1) proves the  $R$  case of (3).2.3 An unmarked canonical tile is endpoint-emptyThis is the key fact for marked demand.Normalize an old positive left side as
$$u=(2,2),\quad z=(2,3),\quad
x=(3,2),\quad y=(3,3),\quad v=(4,2).$$
The canonical tile is
$$Q=\{u,z,x,y\}.$$
Here  $x$  is the positive’s original support anchored at  $(3,1)$ ; the triggers are  $u,v,z$ .Suppose the side is unmarked in  $I$ . Then
$$u,v,z\notin P_I.$$
The point  $u$  cannot be selected either: it has the fixed positive endpoint neighbors  $(1,2)$  and  $(2,1)$ . Thus  $u\notin O_I$ .If  $x$  were an endpoint of a foreign retained source, its original occupied degree at least three, together with the absence of its neighbor  $u$ , would force its other three neighbors—including  $v$ —to be originally occupied. Persistence would make  $v$  occupied in  $I$ . But  $v$ , with endpoint neighbors  $x$  and  $(4,1)$ , could not remain selected. Hence  $v\in P_I$ , contradicting the unmarked side.Therefore  $x\notin P_I$ , and it remains a mandatory positive support. If  $y\in P_I$ , that support would have two endpoint neighbors,  $y$  and its anchor. This is also impossible.We conclude
$$\boxed{\text{An unmarked positive side has }P_I\cap Q=\varnothing.}
\tag{4}$$
This proof uses complete physical occupancy and original endpoint degree, rather than a restriction on possible foreign source phases.2.4 Each newly marked side belongs to one new componentIf an old side becomes marked in  $J$ , its canonical tile becomes nonempty in endpoints:a trigger at  $u$  or  $z$  is already in the tile;a trigger at  $v$  forces the original support  $x$  to be consumed.By (4), all these tile endpoints are new. Their tile profile is connected, so they belong to one new component. A trigger at  $v$  is adjacent to  $x$ , and belongs to that same component.For a new positive source, every trigger is adjacent to one of that source’s own endpoints. A new witness therefore belongs to the positive’s new component; an old witness is already present in the corresponding  $K_j$ .Thus every actual new marked-side occurrence is assigned to one component, proving the  $G$  case of (3). The  $N$  case is immediate, and the  $\mu$  case follows.One useful exact consequence is
$$\boxed{
\min_T\mu(X_T)
=
\mu(I)+\sum_j\min\{0,\mu(K_j)-\mu(I)\}.
}
\tag{5}$$
The remaining issue is the sign of this minimum.3. A pointwise reserve identity and a one-use loss boundFor each physical tile  $Q$ , define
$$\kappa_X(Q)=a_X(Q)+u_X(Q)+z_X(Q)+h_X(Q),$$
where the terms are the actual contributions to  $A,U_0,Z_0,H$ .For a  $Z_0$  occurrence, use its original singleton tile as its home. Its value still depends on the paired triple tile. Then
$$\sum_Q\kappa_X(Q)=2R(X).
\tag{6}$$
This convention matters: a local reserve calculation must retain the remote zero-rotor pairing.3.1 Exact pointwise linearizationLet
$$\eta_X(Q)=
2\,\#(\text{original irregular pairs in }Q)
+\#(\text{original irregular singletons in }Q)
+\#(\text{original U}_{11}\text{ triples in }Q).$$
For every paired zero-rotor singleton/triple occurrence  $\zeta$ , let  $f_\zeta(X)$  indicate that its original triple is filled. Set this indicator to zero when its owner is absent.Then
$$\boxed{
\begin{aligned}
\kappa_X(Q)
={}&\eta_X(Q)+4F_{\mathrm{mix},X}(Q)-2E_X(Q)\\
&+\sum_\zeta f_\zeta(X)
\left(
\mathbf1_{Q=Q_\zeta^{\rm tr}}
-\mathbf1_{Q=Q_\zeta^{\rm si}}
\right).
\end{aligned}}
\tag{7}$$
This follows from the exact local defect table. Adding the activation, unfilled-U-triple, and unfilled-paired-rotor terms cancels activated regular singletons and filled U triples. A filled zero-rotor triple leaves the displayed transfer between its triple tile and paired singleton home. The exact reserve note supplies the underlying local table and singleton/triple cancellation.The last line of (7) uses the same filled-triple occurrence twice with opposite signs. It supplies no additional capacity.Every term of (7) factors over the new components. For the zero-rotor term:an old triple has a unique missing-corner consumer;if its owner is new, any new filler is adjacent to the owner’s original triple and therefore belongs to the same new component.Consequently
$$\boxed{
\kappa_{X_T}(Q)
=
\kappa_I(Q)+
\sum_{j\in T}\bigl(\kappa_{K_j}(Q)-\kappa_I(Q)\bigr).
}
\tag{8}$$
3.2 Actual old capacity pays aggregate local net loss onceFor a fixed tile  $Q$ , choose
$$T_Q=\{j:\kappa_{K_j}(Q)<\kappa_I(Q)\}.$$
Theorem 1 makes  $X_{T_Q}$  complete feasible. Old positive activations persist, so
$$\kappa_{X_{T_Q}}(Q)\ge a_I(Q).$$
Using (8),
$$\boxed{
\sum_j\bigl(\kappa_I(Q)-\kappa_{K_j}(Q)\bigr)_+
\le \kappa_I(Q)-a_I(Q).
}
\tag{9}$$
This has a literal one-use interpretation. Label the actual old non- $A$  capacity units at  $Q$ , with the weights prescribed by (2). The integer net deficits on the left can be assigned disjoint sets of those labels. No label is used twice.The minimizing subset  $T_Q$  may depend on  $Q$ . That causes no problem: the proof only needs each such subunion to be feasible.Summing gives
$$\boxed{
\sum_j\bigl(R(I)-R(K_j)\bigr)_+
\le R(I)-\frac{A(I)}2.
}
\tag{10}$$
Since the left side is integral, it is also at most
$$R(I)-\left\lceil\frac{A(I)}2\right\rceil.$$
This is an unrestricted reserve-loss theorem with actual capacity units used once. It is not yet the requested allocation-margin theorem.The distinction is that these labels have not been proved uncommitted to the old marked demand. Equation (9) allocates net losses within the old reserve; it does not simultaneously allocate the positive demands.4. The separator correction vanishesYour established separator identity is
$$\mu(F)=\mu(L)+\mu(K)-N_s-S_s+d_s,$$
where
$$F=A\cup\{s\}\cup B,\qquad
L=A\cup\{s\},\qquad K=B\cup\{s\},$$
and there is no endpoint edge from  $A$  to  $B$ . The general identity and legality of these restrictions are recorded in the source-separator transfer note.Apply Theorem 1 with  $I=\{s\}$ . An isolated source has no actual marked side. No new endpoint component can cross from  $A$  to  $B$ . By marked-side uniqueness, a side of a positive separator can become marked in at most one branch.Therefore
$$\boxed{d_s=0}
\tag{11}$$
for every such complete separator split, and
$$\boxed{
\mu(F)=\mu(L)+\mu(K)-N_s-S_s.
}
\tag{12}$$
For  $r$  branches sharing  $s$ , the corresponding formula is
$$\mu(F)=\sum_{t=1}^r\mu(I_t)-(r-1)(N_s+S_s).
\tag{13}$$
This sharpens the transfer identity. It does not restore shared-mass branch coverage: your negative-separator branch still has
$$R(K)=k/2+18<S_s=k+7$$
for the stated lengths.5. Physical compression of every finite familyThe next result addresses long interfaces directly.Theorem 2Let  $F$  be any complete feasible family of  $q\ge1$  sources in the full catalogue. There exists another complete feasible family  $F^\circ$  such that:it has the same owners, source types, orientations, and effective phases;U widths and independent heights may be shortened by even amounts, remaining admissible;every positive side retains its actual marked/unmarked status; $A,U_0,Z_0,L_1,L_{2\mathrm{mutual}},L_3$  are unchanged;for a nonnegative integer  $b$ ,
$$L_{2\mathrm{bar}}(F^\circ)=L_{2\mathrm{bar}}(F)-b;$$
hence
$$\boxed{
R(F^\circ)=R(F)-b,\qquad
\mu(F^\circ)=\mu(F)-b;
}
\tag{14}$$
all original endpoints and supports fit, after an even translation, inside an even-aligned square of side  $52q$ .Here  $b$  counts actual removed nonfull sole irregular-bar tiles, each once.This constructs a different physical family with shortened source parameters. It is not a legal-retention assertion about deleting points while keeping the original instance’s matching literally unchanged.5.1 Protect the exceptional geometryFor each U, protect the physical images of the four intrinsic anchors
$$(0,1),\quad(0,w),\quad(L,1),\quad(H,w).$$
In either physical coordinate these have at most three distinct projections. Protect every integer coordinate within distance  $6$  of each projection.For each rotor, protect distance  $6$  around the physical image of its canonical origin in each coordinate. Its complete endpoint/support footprint lies within that collar.Thus each axis has at most  $3q$  protecting intervals, each containing  $13$  integer levels.These collars protect all:positive mark stencils, including the distance-four triggers;positive terminal receiver tiles;U singleton and U11 triple occurrences;rotor footprints and their singleton/triple pairings.5.2 Every unprotected strip is two-periodic owner by ownerBetween protected coordinate levels, each owner’s endpoint and original-support masks are two-periodic along that coordinate.For a horizontal-bar U, an unprotected row strip can meet ordinary straight stems, whose endpoints are constant and supports alternate with period two. It cannot meet a bar, tip, or support-pattern transition.For a vertical-bar U, such a strip can meet only ordinary bar interior or nothing. The statement follows after transposition. Rotors are absent from these strips.This is a direct constructor argument for arbitrary legal dimensions.5.3 Delete one complete physical tile stripIf an unprotected row gap has at least five levels, choose an even  $d$  such that
$$d-1,d,d+1,d+2$$
all lie in the gap. Delete rows  $d,d+1$ , and shift later rows by  $-2$ .Every source becomes the same oriented constructor with an appropriate even shortening:a crossed stem loses two units of its corresponding height;a crossed vertical bar loses two units of width;other sources translate or stay fixed;no rotor is cut.The protected collars prevent shortening below the allowed minimum dimensions.For each owner, the new  $P_i,T_i$  are precisely the images of its surviving original points. The map is injective on surviving points, so endpoint uniqueness persists.At the seam, two-periodicity gives
$$O(d+2,c)=O(d,c),\qquad
O(d-1,c)=O(d+1,c),$$
with the same equalities ownerwise for endpoint and support masks. Every new selected-point neighborhood at the seam is therefore a copy of a previously feasible neighborhood. This preserves mandatory-support feasibility, including support/support conflicts.The shortened source receives its prescribed canonical matching. When a cut crosses two matching edges along one source’s straight chain, their surviving endpoints reconnect across the seam. This is exactly the matching of the shortened constructor. Every endpoint also retains occupied degree at least three within its new original source.Thus the compressed family is physically complete feasible.5.4 The reserve change is exactEvery surviving physical tile retains its original owner profiles and final endpoint occupancy.In a deleted tile, an original endpoint profile can only be
$$2P0T,\qquad 2P1T,\qquad 4P0T.$$
Singletons, triples, and rotors are protected. Endpoint disjointness therefore leaves only endpoint partitions
$$\varnothing,\quad 2,\quad 2+2,\quad 4.$$
Among these possibilities, the only nonzero contribution to (2) is a nonfull sole original  $2P0T$  tile. Its weight is two in  $2R$ , or one in  $R$ .Consequently each deletion satisfies
$$R'=R-b_d,\qquad \mu'=\mu-b_d,$$
where  $b_d$  is its actual number of removed sole irregular-bar tiles. All other listed quantities remain unchanged.This proves (14) without treating deleted full tiles, original masses, or events as extra resources.5.5 The size boundRepeat row deletions until every gap between protected components has at most four levels, then do the same for columns.If an axis has  $m\le3q$  protecting intervals, its span contains at most
$$13m+4(m-1)=17m-4\le51q-4$$
integer levels.All source points lie within this span. At most two additional levels are needed for even tile alignment. Hence  $52q$  is a valid bound in both directions.Column compression does not enlarge the row span or change the row coordinates of the protected anchors.6. Exact transfer along arbitrarily long interfacesFor a legal extension  $I\subseteq J$ , use the protected coordinates from all owners of  $J$  and perform the same compression on both families.The argument is ownerwise, so it preserves the complete feasibility of  $I$ , including supports restored there. It also preserves the individual marked-side data of both families.Let  $b_X$  count the actual sole irregular-bar tiles removed from  $X$ , for  $X=I,J$ . Then
$$\mu(X)=\mu(X^\circ)+b_X,$$
and therefore
$$\boxed{
\mu(I)-\mu(J)
=
b_I-b_J+\mu(I^\circ)-\mu(J^\circ).
}
\tag{15}$$
This isolates the entire contribution of the removed long strips.More explicitly, for each compressed gap  $g$ , let  $t_g$  be the number of removed two-row or two-column periods. Its contribution has the form
$$b_g(X)t_g,\qquad b_g(X)\in\mathbb Z_{\ge0}.$$
The coefficients remain unchanged under transverse compression: a tile whose row pair and column pair are both unprotected contains no original source point. Every U point is near either its bar-row anchor or a stem-column anchor, and rotors are protected.Thus
$$\mu(X)=\mu(X^\circ)+\sum_g b_g(X)t_g,
\tag{16}$$
with nonnegative coefficients.At an individual removed tile, positive extension loss occurs only when an old sole irregular-bar tile becomes full. That old tile supplies its one reserve unit once. Hence
$$\boxed{
\sum_g\bigl(b_g(I)-b_g(J)\bigr)_+t_g
\le
\sum_g b_g(I)t_g.
}
\tag{17}$$
This is a general physical bound for loss along arbitrarily long transition-free interfaces.Your nine-source family fits this accounting exactlyUsing your explicit two-row insertion and its  $k=6$  base,
$$\mu(H_k)=15+\frac{k-6}{2},
\qquad
\mu(J_k)=23.$$
Each inserted period contributes one actual irregular-bar reserve unit to  $H_k$ , and zero reserve to  $J_k$ . Therefore
$$\mu(H_k)-\mu(J_k)
=
\frac{k-6}{2}-8.$$
The unbounded part of the loss is exactly the old irregular-bar contribution. The base extension contributes a margin gain of eight.This explains the loss using its actual geometric source. It does not invoke the fixed added mass  $17$ , or assign a second credit to the newly full tiles.7. What compression does—and does not—reduceFor each fixed source count  $q$ , Theorem 2 gives
$$\boxed{
\min_{\substack{F\text{ complete feasible}\\|F|=q}}\mu(F)
=
\min_{\substack{F\text{ complete feasible}\\|F|=q\\F\subseteq[0,52q-1]^2}}\mu(F).
}
\tag{18}$$
The minima exist because margins are integers bounded below by  $-q$ . The inequality in one direction follows from inclusion; the other follows by compressing a minimizing family without increasing its margin.Thus a target violation with  $q$  sources always has a bounded physical representative with the same source count and the same marked-side demand.The quantifier remains
$$\boxed{\text{for every }q.}$$
There is no bound here on the number of sources. Checking finitely many source counts cannot establish the unrestricted allocation.The reduction does establish that arbitrarily large dimensions are not independently necessary for a violation at fixed  $q$ : their removable contributions are nonnegative actual bar terms.8. The exact unresolved margin obligationFor a demand-preserving marked-hull extension,  $N$  and  $G$  are fixed. Write the local net losses and gains as
$$\ell_j(Q)=\bigl(\kappa_I(Q)-\kappa_{K_j}(Q)\bigr)_+,
\qquad
g_j(Q)=\bigl(\kappa_{K_j}(Q)-\kappa_I(Q)\bigr)_+.$$
Then the exact component identity gives
$$2\mu(J)
=
2\mu(I)-\sum_{j,Q}\ell_j(Q)+\sum_{j,Q}g_j(Q).
\tag{19}$$
The requested margin theorem would need
$$\boxed{
\sum_{j,Q}\ell_j(Q)
\le
2\mu(I)+\sum_{j,Q}g_j(Q).
}
\tag{20}$$
What is proved above is
$$\sum_{j,Q}\ell_j(Q)\le2R(I)-A(I).
\tag{21}$$
The gap between (20) and (21) is precisely the demand already charged against  $R(I)$ .Likewise, compression gives
$$\mu(I)=\mu(I^\circ)+b_I.$$
It identifies  $b_I$  as the actual old contribution that pays repetitive-interface losses. But calling all of  $b_I$  available margin would require knowing the sign of  $\mu(I^\circ)$ . That sign is still part of the unrestricted target.For extensions that also add positives or marks, the exact formula retains the additional term:
$$2\mu(J)
=
2\mu(I)+2(\Delta N-\Delta G)
-\sum\ell+\sum g.
\tag{22}$$
No source or demand class has been excluded from the unresolved step.I therefore do not claim that these results prove the target. Nor did the exploratory physical completion work produce a complete negative-margin family; finite exclusions and a stalled completion attempt supply no unrestricted verdict.The advances justified here are the full-family component theorem, its one-use reserve-loss bound, the universal vanishing of  $d_s$ , and exact physical compression of long interfaces. A proof that the remaining capacities pay marked demand once—or a complete compressed configuration with  $\mu<0$ —is still needed. Even the latter would be an allocation counterexample; a grid counterexample would additionally require actual negative ambient slack, which these reductions do not establish.

