ACCEPTThe corrected theorem is mathematically sound as stated. The repairs close the defects identified in the initial review: $0\le i<n$  is explicit. $H,d,f$  are all explicitly even, so  $y$  and  $\ell$  have the required odd parity and the prescribed matching reaches both terminals.The partner-column argument now correctly allows a same-row  $P_k^0$  endpoint while excluding endpoints above the relevant frontier.Later-block row separation is used only after the legal  $y$ -bound has been imposed.The  $k=n-1$  case is handled.The no- $k$  case uses column and physical-tile separation alone.I find no remaining mathematical counterexample to the theorem or to its three-row classification.1. Parity and legal-source domainThe revised domain
$$H,d,f\in 2\mathbb Z,\qquad H\ge 6,\qquad d,f\ge4$$
is the necessary one for the stated matching convention. Since  $a_0$  is odd,  $s_0$  is even, and every  $z_j,w_j$  is even, induction gives
$$a_j\ \text{odd},\qquad s_j\ \text{even}.$$
Therefore
$$\ell=s_i+1-H$$
is odd, and
$$y=a_i-4-d+f$$
is also odd. The event cases indexed by rows  $a_k-2+2j$  are consequently exhaustive in the activated first-column case.The explicit exclusion of odd leg depths also removes the previous failure mode in which the far-lateral support changed side and the event count became wrong.2. Selection of the first later blockThe recurrence
$$s_{j+1}=s_j-w_{j+1}-12$$
makes the  $s_j$  strictly decreasing, with a decrease of at least  $24$ . If  $k$  is the first  $j>i$  satisfying
$$\ell\ge s_j-3,$$
then minimality gives
$$\ell<s_{k-1}-3.$$
Because  $\ell$  is odd and  $s_{k-1}$  is even,
$$\ell\le s_{k-1}-5.$$
Together with  $\ell\ge s_k-3$ , this gives precisely
$$s_k-3,\quad s_k-1,\quad
s_k+1\le \ell\le s_{k-1}-5.$$
For  $k=i+1$ , the upper bound follows from
$$\ell=s_i+1-H\le s_i-5=s_{k-1}-5$$
because  $H\ge6$ .The first-contact index is therefore selected correctly by the far column, with no finite-depth or finite-width cutoff.3. Earlier-block exclusionEvery old block  $j$ , including  $P_j^0,Z_j,X_j$ , has minimum endpoint column  $s_j-4$ , which is even. In the no- $k$  case,
$$\ell\le s_{n-1}-5,$$
so the far stem is in the immediately preceding physical tile column or farther left. The same argument applies to every earlier block. Since the relevant old endpoint columns are separated by a global tile boundary, there is neither a shared endpoint nor an intratile event.When  $k$  exists, minimality similarly gives
$$\ell\le s_{k-1}-5.$$
All blocks before  $k$  have endpoint columns at least  $s_{k-1}-4$ , so their endpoints lie across the next physical tile boundary from the far stem. This remains true even for arbitrarily long old  $V_j$  stems, because their row length does not change their column support.The near stem is a separate local configuration. Its two-full-tile/four-event receipt against  $P_i^0$  is unchanged for every even  $d\ge4$ , including the  $d=4$  case in which the upper tile is supplied partly by the new bar and partly by the first leg cells.4. The three frontiersThe three stated first endpoints are correct.Case 1:  $\ell=s_k-3$ The first old endpoint in the far column is the  $X_k$  bar at row  $a_k+1$ . The partner column  $s_k-4$  contains the  $X_k$  far stem beginning at row  $a_k-2$ .Since the far stem of  $T$  contains every row up to  $y$ , endpoint disjointness is equivalent to
$$y\le a_k.$$
If  $y=a_k-2$  or  $y=a_k$ , the partner-column interaction produces the exceptional receipt. If  $y\le a_k-4$ , the far leg stops before the relevant physical tile row and produces no extra event.Case 2:  $\ell=s_k-1$ The first old endpoint in the far column is the  $Z_k$  endpoint at row  $a_k-4$ . The partner column  $s_k-2$  has no endpoint above that row. Therefore the exact disjointness threshold is
$$y\le a_k-6.$$
At  $y=a_k-6$ , the far leg ends in the preceding physical tile row, so there is no same-tile event with the  $Z_k$  frontier.Case 3:
$$s_k+1\le \ell\le s_{k-1}-5.$$
The first old endpoint in the far column is the  $P_k^0$  bar at row  $a_k-8$ . The partner column has no endpoint above that row. When  $\ell\ge s_k+3$ , it may contain a same-row  $P_k^0$  bar endpoint, but the legal bound
$$y\le a_k-10$$
places the terminal in the preceding physical tile row. At  $\ell=s_k+1$ , the partner-column endpoints start strictly lower.Thus the third threshold
$$y\le a_k-10$$
is also correct.The upper bound
$$\ell\le s_{k-1}-5=s_k+w_k+7$$
lies inside the  $P_k^0$  bar, whose columns extend through  $s_k+w_k+12$ .5. Later-block exclusionThe revised proof handles the unbounded  $f$  issue correctly.For a legal  $T$ , the relevant table row always gives  $y\le a_k$ . If  $k<n-1$ , every later block has minimum endpoint row at least
$$a_{k+1}-8
\ge a_k+10,$$
because  $z_k\ge24$ . Hence no later block can contact the far stem of a legal  $T$ . If  $k=n-1$ , there is no later block and the assertion is vacuous.The proof also correctly states that without the legal  $y$ -bound one cannot compare arbitrary far-terminal rows to later blocks. This is the required qualification for unbounded  $f$ .In the no- $k$  case, the proof uses column separation alone, so it remains valid for arbitrarily large  $f$ .6. Exact event ledgerIn the only activated case,  $\ell=s_k-3$ , write
$$y=a_k-2+2m,\qquad m\in\{0,1\}.$$
The event list is correct:
$$X_k:(a_k-2+2j,s_k-4)
\longrightarrow
T:(a_k-2+2j,s_k-3),
\qquad j=0,\ldots,m,$$
and, when  $m=1$ ,
$$T:(a_k-1,s_k-3)
\longrightarrow
X_k:(a_k-1,s_k-4).$$
Thus: $m=0$ :  $\Delta F=0,\ \Delta E=1$ ; $m=1$ :  $\Delta F=1,\ \Delta E=3$ .In both cases,
$$2\Delta F-\Delta E=-1.$$
The support exclusions are also correctly assigned:For  $X_k$ , the rightward target is excluded on odd intrinsic stem rows and survives on even intrinsic stem rows.For  $T$ , the leftward target is excluded on even intrinsic far-leg rows and survives on odd intrinsic far-leg rows.The vertical adjacency from  $T$ 's terminal at row  $a_k$  to the  $X_k$  bar at row  $a_k+1$  crosses a global physical tile boundary, so it contributes no event. The upper partial tile is not full.No extra event or full tile appears in the second or third column cases under their legal  $y$ -bounds.7. Gain formulaThe charge of the new original is
$$1-H,$$
so its negative mass contributes  $H-1$ . The own  $P_i^0$  receipt contributes
$$2\cdot 2-4=0.$$
The exceptional far receipt contributes  $-1$  exactly in the first row with  $y\in\{a_k-2,a_k\}$ . Therefore
$$\Phi(H_3\cup\{T\})-\Phi(H_3)=H-1-\delta.$$
If  $\delta=0$ , then  $H-1\ge5$ . If  $\delta=1$ , then
$$\ell=s_k-3$$
implies
$$H=s_i-s_k+4.$$
Since  $s_i-s_k\ge24$ ,
$$H\ge28,$$
and the gain is at least
$$28-2=26.$$
Consequently the gain is always at least  $5$ , and equality occurs exactly when  $H=6$ . No arithmetic defect remains.Minor editorial clarificationOne sentence could be made slightly more formal:“Write  $y=a_k-2+2m,\ m\in\{0,1\}$ .”This should ideally read:“In the activated cases  $y\ge a_k-2$ , write  $y=a_k-2+2m$  with  $m\in\{0,1\}$ .”Below the activation threshold,  $y$  can be  $a_k-4,a_k-6,\ldots$ , so  $m$  is not in  $\{0,1\}$ . The following sentence explicitly handles that below-threshold case, so this is an editorial clarification rather than a mathematical defect.The phrase “later blocks start below its terminal” should likewise be understood as referring to the fixed near-stem terminal; the later paragraph correctly prevents it from being read as an unconditional statement about the unbounded far terminal.Subject to those optional wording refinements, the corrected one-consumer theorem is ACCEPT. The result remains properly limited to one new arbitrary left consumer; it does not establish any monotonicity for multiple consumers or resolve the separate right-frame interaction problem.
