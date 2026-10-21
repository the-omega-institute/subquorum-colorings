ACCEPTUnder the stated full-original U/rotor model and the accepted B/R pair premise, the all-parameter classification of A, every displayed ledger count, and the joint bound  $\Delta\Phi\ge46$  are correct. No count correction is needed.There is one local wording error in the sufficiency proof: when  $d=4$ , A’s bar is not above every first-block endpoint. It occupies the same two rows as P₀’s bar, and disjointness follows from their column intervals. The supplied charts give a direct replacement proof, detailed below.This is a mathematical audit of the supplied classification and ledger. It makes no execution-certification claim and uses no result from the separate cavity-exclusion review.1. Exhaustion of the possible owners of  $t_0$ The three retained neighboring endpoints are
$$(a-4,s-1),\qquad (a-4,s+1),\qquad (a-3,s),$$
west, east and south of  $t_0=(a-4,s)$ . The west and south points belong to the retained west rotor; the east point belongs to  $P_0$ .Because different originals have disjoint endpoint sets, the new owner of  $t_0$  cannot have its own endpoint at any of those three positions. Its matching neighbor must therefore be north.Every nonterminal endpoint of a full U has at least two neighboring endpoints of that same original. Consequently,  $t_0$  must be one of its two stem terminals. Relabeling the incident stem as the near stem leaves exactly the two charts
$$(r,c)\longmapsto(a-4-d+r,\ s+1-c)$$
and
$$(r,c)\longmapsto(a-4-d+r,\ s-1+c).$$
The relabeling preserves the specified matching and supports because the breadth is even.For the standard rotor, the four tips form one rotational orbit. Fixing a tip at  $t_0$  with matching neighbor north leaves two reflected placements. Both contain
$$t_0+(-2,1)=(a-6,s+1).$$
This is a  $P_0$  endpoint—its canonical far-stem point at row  $2$ . Both rotor roles are therefore excluded.Thus the two U frames exhaust the possibilities under the stated model.All stated collision blockers are validThe following table records the actual shared endpoint in each excluded case.Candidate caseShared endpointRetained ownerEither frame,  $d\ge10$  $(a-13,s)$ B, lower barRight frame,  $d=4$  $(a-8,s+1)$  $P_0$ , upper barRight frame,  $d\in\{6,8\}$ ,  $L\le u+12$  $(a-8,s+L-1)$  $P_0$ , upper barRight frame,  $d=6$ ,  $L\ge u+14$  $(a-9,C)$ R, near endpointRight frame,  $d=8$ ,  $L\ge u+14$  $(a-11,C)$ B, far stemLeft frame,  $L\ge v+14$  $(a-4-d,s_1)$ B, near stemIn the first row, the incident column of either U frame contains every row from  $a-4-d$  through  $a-4$ , so it contains  $a-13$  whenever  $d\ge10$ .For the small-width right-frame cases, the far stem reaches row  $a-8$ : its canonical row there is  $d-4$ , equal to  $2$  or  $4$ , and  $f\ge4$ . Its far column lies inside P₀’s bar interval.Evenness leaves no width between  $L\le u+12$  and  $L\ge u+14$ . Hence every right frame is excluded, and every surviving left frame satisfies
$$d\in\{4,6,8\},\qquad 6\le L\le v+12.$$
The far-depth bound is exactWrite
$$r_0=a-4-d,\qquad F_c=s+1-L,\qquad q=r_0+f,$$
using  $F_c$  for the far column to distinguish it from the mixed-tile set.The width bounds give
$$s_1+1\le F_c\le s-5.$$
P₁’s upper bar is exactly at row
$$a_1-8=a+z-14$$
with column interval
$$[s_1+1,s].$$
Thus A’s far column lies in that interval.The far endpoint column of A is continuous from  $r_0$  through  $q$ . It hits P₁’s bar whenever
$$f\ge(a+z-14)-r_0=z+d-10.$$
Since  $f,z,d$  are even, avoiding this collision is equivalent to
$$f\le z+d-12,$$
or
$$q\le a+z-16.$$
This proves precisely the necessary parameter list
$$\boxed{
A=U(L,d,f),\quad
(r,c)\mapsto(a-4-d+r,s+1-c),\quad
6\le L\le v+12,\quad
d\in\{4,6,8\},\quad
4\le f\le z+d-12,
}$$
with all three parameters even.2. Sufficiency, including the wording correctionThe converse is valid for endpoint disjointness, uniformly in every allowed R.A has:bar rows  $r_0,r_0+1$ , ending no later than  $a-7$ ;near column  $s$ , ending at  $a-4$ ;far column  $F_c\le s-5$ , ending at  $q\le a+z-16$ .Directly from the supplied charts, every first-block original other than the west rotor and  $X_0$  has minimum endpoint column at least  $s+1$ . These originals cannot collide with A, whose endpoint columns are at most  $s$ .The two exceptions are also separated:The west rotor starts at row  $a-4$ , has minimum column  $s-2$ , and has its column- $s$  endpoints only at rows  $a-3,a-2,a-1$ . Its top endpoint is  $(a-4,s-1)$ , not  $t_0$ . $X_0$  starts at row  $a-2$  and has minimum column  $s-4$ .A’s bar lies above both exceptions, its near stem ends before their column- $s$  endpoints, and its far column lies strictly to their left.Required local prose replacementThe sentence saying that A’s bar “is above all old first-block endpoints” should be replaced by:For  $d=6,8$ , A’s bar lies above every first-block endpoint. For  $d=4$ , A and P₀ have the same bar rows  $a-8,a-7$ , but their endpoint column intervals are disjoint:
$$A:[F_c,s],\qquad P_0:[s+1,s+u+12].$$
Every other first-block original starts below those bar rows.This repairs the sentence without changing the theorem or any count.For the later blocks, every endpoint starts at row at least  $a+z-14$ , while every A endpoint is at row at most  $a+z-16$ . The latter statement includes the near terminal because  $z\ge24$ .Against B, its bar ends at  $a-13$ , whereas A starts at  $a-12$  or later, and its stem columns satisfy
$$s_1<F_c,\qquad C>s.$$
Against R, every endpoint column is at least  $C>s$ . The argument is independent of R’s arbitrarily large far depth.This proves the geometric converse. Freshness and distinctness also follow:  $t_0$  was absent from H3, B and R both miss  $t_0$ , and A misses  $y_0$ .3. A’s immutable charge is exactly  $1-L$ The endpoint count gives
$$M_A=L+\frac{d+f}{2}-1.$$
Here  $r_0$  is odd, the near column  $s$  is even, and the far column  $F_c$  is odd. The two bar rows therefore occupy different physical tile rows. Together they meet  $L+2$  tiles. The remaining portions of the stems add
$$\frac{d-2}{2}+\frac{f-2}{2}$$
tiles, giving
$$T_A=L+\frac{d+f}{2}.$$
The original supports in these tiles are exactly:both bar-exterior supports;the even-indexed lateral supports on each stem.Neither axial terminal support lies in an A endpoint tile. Hence
$$J_A=2+\frac{d+f}{2}.$$
Therefore
$$\boxed{\operatorname{charge}(A)=M_A+J_A-2T_A=1-L.}$$
A contributes  $L-1$  to  $S$  and zero to  $N$ . These quantities remain unchanged when its original supports are occupied by other originals.4. The exact new receipts of APut
$$\delta=\mathbf1_{\{d=8\}},\qquad
\epsilon=\mathbf1_{\{L=v+12\}}.$$
The complete receipt partition is
$$\begin{array}{c|c|c}
\text{Receipt}&\text{New mixed full tiles}&\text{New directed events}\\ \hline
A/P_0\text{ near strip}&2&4\\
A/B\text{ upper bar band}&\delta(L/2-1)&2L\delta\\
A/B\text{ tight far contact}&\epsilon(f/2+\delta)&\epsilon(f+1)
\end{array}$$
Near stripThe two full tile minima are
$$\boxed{(a-7,s),\qquad(a-5,s).}$$
At each  $r\in\{a-7,a-5\}$ , the two directed events are
$$A:(r,s)\longrightarrow P_0:(r,s+1),$$

$$P_0:(r,s+1)\longrightarrow A:(r,s).$$
The other possible contact rows are  $a-8,a-6,a-4$ . At those rows, both directions target an immutable original support of the source owner and are excluded. Thus this receipt contributes exactly
$$2(2)-4=0.$$
Upper bar band,  $d=8$ B’s lower bar row  $a-13$  is even, and A’s upper bar row  $a-12$  is odd. For every integer  $c\in[F_c,s]$ , the two new events are
$$B:(a-13,c)\longrightarrow A:(a-12,c),$$

$$A:(a-12,c)\longrightarrow B:(a-13,c).$$
Neither target is an original support of its source owner. There are exactly  $2L$  events.The interior full tile minima are
$$\boxed{
(a-13,F_c+1),\ (a-13,F_c+3),\ldots,(a-13,s-2),
}$$
a total of  $L/2-1$ .The right boundary tile remains partial. The left boundary tile becomes full only in the tight case, and is allocated to the next receipt. Thus the upper band contributes
$$2(L/2-1)-2L=-L-2.$$
Tight far contact,  $\epsilon=1$ Here
$$F_c=s_1+1,$$
so A’s far stem and B’s near stem share one physical tile column.The directed events are exactly
$$B:(r,s_1)\longrightarrow A:(r,F_c),
\qquad r=r_0,r_0+2,\ldots,q,$$
and
$$A:(r,F_c)\longrightarrow B:(r,s_1),
\qquad r=r_0+1,r_0+3,\ldots,q-1.$$
Their respective counts are  $f/2+1$  and  $f/2$ , totaling  $f+1$ .At  $r_0$ , the reverse A-to-B direction targets A’s original bar-exterior support. At subsequent rows, the immutable lateral supports produce exactly the stated alternation.The full tile minima are
$$\boxed{
(r_0+1,s_1),\ (r_0+3,s_1),\ldots,(q-1,s_1),
}$$
giving  $f/2$  tiles.When  $d=8$ , there is also exactly one full tile
$$\boxed{(a-13,s_1).}$$
Its upper two cells and lower-left cell belong to B; its lower-right cell belongs to A. It is distinct from the upper-band list, whose first column is  $s_1+2$ .Its vertical events are already in the bar list, while its horizontal event is already in the far list. Counting the tile once therefore gives the exact tight correction
$$2(f/2+\delta)-(f+1)=2\delta-1.$$
5. Receipt exhaustion and nonreuseThe exhaustion can be established directly from the charts, without relying on finite controls or an unavailable earlier proof.First-block originals. Every first-block original other than  $P_0$ , the west rotor and  $X_0$  has minimum endpoint column at least  $s+2$ . Its physical tile columns therefore miss every A tile, whose rightmost tile column is  $[s,s+1]$ .Only P₀’s column  $s+1$  can share an A tile. Its endpoints there are exactly the rows  $a-8,\ldots,a-4$ , already exhausted by the near receipt.The west rotor’s only tile as high as tile-row minimum  $a-5$  is
$$(a-5,s-2),$$
which A does not meet. Its remaining tiles, and all  $X_0$  tiles, lie below A’s near terminal and to the right of A’s far-strip tile column. A’s bar is higher still.Later blocks. Since  $a+z-16$  is odd, every tile meeting A ends at a row at most  $a+z-16$ . The first possible later-block tile starts at row
$$a+z-15.$$
Thus no later original shares a physical tile with A.B and R. R is separated by tile columns. Of B, only the lower bar when  $d=8$ , and the near stem when  $\epsilon=1$ , share A tiles. B’s far stem is separated to the right.These observations exclude both additional events and additional full-tile completions involving multiple old owners.The nonreuse claims also hold exactly:Near events have owner pair  $A/P_0$ ; the other events have owner pair  $A/B$ .Bar events are vertical; tight far events are horizontal.The full-tile lists have distinct columns or rows, including the separately allocated tight corner.Every new event contains an A endpoint, and every new full tile was missing at least one A cell before insertion.Old events persist because source-support membership is immutable.An old mixed full tile cannot become wholly owned by the fresh, endpoint-disjoint A.In particular, the pair’s three-owner tile at  $(a-1,C-1)$  remains remote and counted once.6. Totals, lower bound and explicit negative marginalAdding A’s receipts to the accepted pair gives
$$\boxed{\Delta S=u+v+L+24,\qquad \Delta N=1,}$$

$$\boxed{
\Delta F=
8+\delta(L/2-1)+\epsilon(f/2+\delta),
}$$

$$\boxed{
\Delta E=17+2L\delta+\epsilon(f+1).
}$$
These are exactly the manuscript’s formulas.Consequently,
$$\boxed{
\Delta\Phi=
\begin{cases}
u+v+L+24-\epsilon,&d=4,6,\\[2mm]
u+v+22+\epsilon,&d=8.
\end{cases}}$$
Subtracting the accepted pair gain  $u+v+25$ , A’s exact marginal is
$$\boxed{
\Delta\Phi(A\mid H3+B+R)=
\begin{cases}
L-1-\epsilon,&d=4,6,\\
-3+\epsilon,&d=8.
\end{cases}}$$
The stated lower bounds are valid. The  $d=4,6$  estimates can actually be sharpened: because  $\epsilon=1$  requires  $L=v+12\ge24$ , the minimum marginal there is  $5$ , and the minimum joint gain is  $54$ . The manuscript’s weaker bounds  $4$  and  $53$  are not errors. The uniform displayed bound remains  $46$ .Explicit coordinates for the supplied exampleTake
$$a=31,\quad s=0,\quad u=v=12,\quad z=24,
\qquad L=6,\ d=8,\ f=4.$$
Then
$$s_1=-24,\qquad C=25,\qquad
r_0=19,\qquad F_c=-5,\qquad q=23,\qquad \epsilon=0.$$
A’s chart is
$$(r,c)\longmapsto(19+r,1-c).$$
Its four new mixed full tiles are
$$\boxed{(24,0),\ (26,0),\ (18,-4),\ (18,-2).}$$
Its events are:four horizontal events between A and P₀ at rows  $24,26$ , between columns  $0,1$ ;twelve vertical events between B’s row  $18$  and A’s row  $19$ , at columns
$$-5,-4,-3,-2,-1,0.$$
Thus A’s marginal additions, in the order  $(S,N,F,E)$ , are
$$(5,0,4,16),$$
and
$$\Delta\Phi_A=5+2\cdot4-16=-3.$$
The triple totals are
$$\boxed{(\Delta S,\Delta N,\Delta F,\Delta E)=(54,1,10,29),}$$
so
$$\boxed{\Delta\Phi=54+1+20-29=46.}$$
This confirms the claimed failure of nonnegative marginal for the selected partial inventory. The accepted conclusion is the conditional owner classification and exact nonreused joint ledger; complete extendibility, later exclusions, and allocation across multiple root triples remain outside this audit.
