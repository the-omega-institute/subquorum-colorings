// Direct parameter enumeration, independent of the witness-ledger proof.
#include <algorithm>
#include <cstdint>
#include <iostream>
#include <random>
#include <stdexcept>
#include <vector>
using M=std::uint64_t;
unsigned pc(M x){return __builtin_popcountll(x);}
unsigned fst(M x){return __builtin_ctzll(x);}
void require(bool x,const char* s){if(!x)throw std::runtime_error(s);}
struct Graph{
 std::vector<M> adj; M side;
 explicit Graph(unsigned a,unsigned b):adj(a+b),side((M(1)<<a)-1){}
 void edge(unsigned a,unsigned b){adj[a]|=M(1)<<b;adj[b]|=M(1)<<a;}
};
std::uint64_t models=0,subsets=0,eligible=0,templates=0;
unsigned beta_private(const Graph& g,M omitted=0){
 unsigned best=0;M full=(M(1)<<g.adj.size())-1,B=full^g.side;
 B&=~omitted;M aside=g.side&~omitted;
 for(M X=aside;;X=(X-1)&aside){
  unsigned z=0;M private_owners=0;
  for(M scan=B;scan;scan&=scan-1){M ns=g.adj[fst(scan)]&X;
   if(!ns)++z;else if(!(ns&(ns-1)))private_owners|=ns;
  }
  best=std::max(best,pc(X)+z+pc(private_owners));if(!X)break;
 }
 return best;
}
std::pair<unsigned,unsigned> exact(const Graph& g){
 unsigned n=g.adj.size(),beta=0,sf=0,countmax=0;M end=M(1)<<n,full=end-1,maxset=0;
 std::vector<unsigned char> form(end);
 for(M S=0;S<end;++S){
  bool d=true,f=true;
  for(M scan=S;scan;scan&=scan-1)if(pc(g.adj[fst(scan)]&S)>1){d=false;break;}
  if(d)beta=std::max(beta,pc(S));
  for(M scan=full^S;scan;scan&=scan-1){
   M ns=g.adj[fst(scan)]&S;if(pc(ns)>=2)continue;
   if(!ns || !(g.adj[fst(ns)]&S)){f=false;break;}
  }
  form[S]=f;
 }
 for(M S=0;S<end;++S)if(form[S]){
  bool minimal=true;for(M scan=S;scan;scan&=scan-1)if(form[S^(scan&-scan)]){minimal=false;break;}
  if(minimal){if(pc(S)>sf){sf=pc(S);countmax=0;maxset=S;}if(pc(S)==sf)++countmax;}
 }
 require(beta==beta_private(g),"private-neighbour formula differs from literal subset enumeration");
 unsigned lo=n?unsigned(n):0,hi=0,n2=0;
 for(M ns:g.adj){lo=std::min(lo,pc(ns));hi=std::max(hi,pc(ns));n2+=pc(ns)==2;}
 int gap=int(sf)-int(beta);
 require(10*gap<=int(n),"universal inequality");
 if(gap>0 && 10*gap==int(n)){
  M I=0,X=0;
  for(unsigned v=0;v<n;++v)if(pc(g.adj[v])==2){I|=M(1)<<v;X|=g.adj[v];}
  require(pc(I)==n/5 && !(I&X),"intrinsic degree-two layer");
  require(countmax==1 && maxset==(full^X),"unique maximum minimal forming set");
 }
 if(lo>=2){
  ++eligible;
  require(int(10*hi+2)*gap<=int(hi*n+n2),"degree-two stability");
  require(int(10*hi+2*lo-4)*gap<=int(hi*n),"minimum/maximum degree refinement");
 }
 ++models;subsets+=end;return {beta,sf};
}
Graph template_graph(unsigned k,unsigned core,unsigned interface){
 unsigned h=5*k;Graph g(h,h);
 for(unsigned j=0;j<k;++j)for(unsigned t=0;t<2;++t){
  g.edge(5*j+2,h+5*j+3+t);g.edge(5*j+3+t,h+5*j+2);
  g.edge(5*j+t,h+5*j+3+t);g.edge(5*j+3+t,h+5*j+t);
 }
 for(unsigned i=0;i<2*k;++i)for(unsigned j=0;j<2*k;++j){
  if(core>>(2*k*i+j)&1)g.edge(5*(i/2)+i%2,h+5*(j/2)+j%2);
  if(interface>>(2*k*i+j)&1)g.edge(5*(i/2)+3+i%2,h+5*(j/2)+3+j%2);
 }
 return g;
}
unsigned pair_deficiency(unsigned k,unsigned matrix,bool reversed){
 unsigned best=0;
 for(unsigned J=0;J<(1u<<k);++J){
  unsigned neigh=0;
  for(unsigned a=0;a<2*k;++a)for(unsigned b=0;b<2*k;++b)
   if(matrix>>(2*k*a+b)&1){unsigned src=reversed?b:a,dst=reversed?a:b;if(J>>(src/2)&1)neigh|=1u<<dst;}
  unsigned z=0;for(unsigned p=0;p<k;++p)z+=((neigh>>(2*p))&3)==3;
  if(pc(J)>z)best=std::max(best,pc(J)-z);
 }
 return best;
}
int main(int argc,char** argv){
 if(argc==2 && std::string(argv[1])=="--intrinsic"){
  unsigned pass=0,full=65535;M ca=0,cb=0;
  for(unsigned j=0;j<2;++j)for(unsigned t=0;t<2;++t){ca|=M(1)<<(5*j+t);cb|=M(1)<<(10+5*j+t);}
  for(unsigned q=0;q<=full;++q){
   Graph g=template_graph(2,full,q);unsigned da=pair_deficiency(2,q,false),db=pair_deficiency(2,q,true);
   require(beta_private(g,ca)==10+da,"paired exact formula, omitted core A");
   require(beta_private(g,cb)==10+db,"paired exact formula, omitted core B");
   unsigned beta=beta_private(g);require((beta==10)==(!da&&!db),"complete-core equality criterion");
   pass+=beta==10;
  }
  std::mt19937 rng(20261112);unsigned controls=0;
  for(unsigned j=0;j<128;++j){unsigned c=rng()&65535,q=rng()&65535;Graph g=template_graph(2,c,q);
   require(beta_private(g,ca)==10+pair_deficiency(2,q,false),"arbitrary core one-side A");
   require(beta_private(g,cb)==10+pair_deficiency(2,q,true),"arbitrary core one-side B");++controls;
  }
  for(unsigned q:{0u,33825u,38505u,65535u}){
   auto [b,s]=exact(template_graph(2,full,q));
   require(b!=10 || s==12,"exact complete-core formation and intrinsic uniqueness control");
  }
  Graph bad=template_graph(2,0xCC33,33825);require(beta_private(bad)>=12,"incomplete-core counterexample");
  std::cout<<"{\"status\":\"PASS\",\"complete_core_interfaces\":65536,\"paired_formula_checks\":131328,\"equal_interfaces\":"<<pass<<",\"arbitrary_core_controls\":"<<controls<<",\"literal_twenty_vertex_models\":"<<models<<",\"literal_subsets\":"<<subsets<<"}\n";return 0;
 }
 if(argc==3 && std::string(argv[1])=="--cycle"){
  unsigned r=std::stoul(argv[2]),h=5*r;require(r>=1 && h<=22,"exact cycle family size");
  Graph g(h,h);
  for(unsigned j=0;j<r;++j){
   for(unsigned t=0;t<2;++t){g.edge(5*j+2,h+5*j+3+t);g.edge(5*j+3+t,h+5*j+2);g.edge(5*j+3+t,h+5*j+3+t);g.edge(5*j+t,h+5*j+3+t);g.edge(5*j+3+t,h+5*j+t);}
  }
  for(unsigned i=0;i<2*r;++i)for(unsigned j=0;j<2*r;++j)g.edge(5*(i/2)+i%2,h+5*(j/2)+j%2);
  unsigned beta=beta_private(g);require(beta==(r==1?6:h),"cycle family beta");
  std::cout<<"{\"r\":"<<r<<",\"n\":"<<2*h<<",\"beta_2\":"<<beta<<",\"side_subsets\":"<<(M(1)<<h)<<"}\n";return 0;
 }
 if(argc==3){
  unsigned d=std::stoul(argv[1]),r=std::stoul(argv[2]),s=d-2,h=5*r+s;
  require(d>=3 && r>=d && 2*h<64 && h<=22,"exact family control size");
  Graph g(h,h);const char* rows[]={"11001","11010","00011","01111","10111"};
  for(unsigned j=0;j<r;++j)for(unsigned a=0;a<5;++a)for(unsigned b=0;b<5;++b)
   if(rows[a][b]=='1')g.edge(5*j+a,h+5*j+b);
  for(unsigned q=0;q<s;++q)for(unsigned j=0;j<r;++j){g.edge(5*r+q,h+5*j+2);g.edge(5*j+2,h+5*r+q);}
  for(unsigned j=0;j<r;++j)for(unsigned k=0;k<r;++k)
   for(unsigned a=0;a<2;++a)for(unsigned b=0;b<2;++b){g.edge(5*j+a,h+5*k+b);g.edge(5*j+3+a,h+5*k+3+b);}
  unsigned beta=beta_private(g);require(beta==h,"exact family beta");
  std::cout<<"{\"d\":"<<d<<",\"r\":"<<r<<",\"n\":"<<2*h<<",\"beta_2\":"<<beta<<",\"side_subsets\":"<<(M(1)<<h)<<"}\n";return 0;
 }
 for(unsigned n=0;n<=8;++n)for(unsigned a=0;a<=n/2;++a){unsigned b=n-a;
  for(M bits=0;bits<(M(1)<<(a*b));++bits){Graph g(a,b);unsigned k=0;
   for(unsigned x=0;x<a;++x)for(unsigned y=a;y<n;++y,++k)if(bits>>k&1)g.edge(x,y);
   exact(g);
  }
 }
 auto exhaustive=models;std::mt19937 rng(11112026);
 for(unsigned j=0;j<160;++j){unsigned n=9+j%8,a=n/2;Graph g(a,n-a);
  for(unsigned x=0;x<a;++x)for(unsigned y=a;y<n;++y)if(rng()%8<2+j%7)g.edge(x,y);
  exact(g);
 }
 unsigned equality=0;
 for(unsigned c=0;c<16;++c)for(unsigned w=0;w<16;++w){
  unsigned deg[4]{};for(unsigned i=0;i<2;++i)for(unsigned j=0;j<2;++j)if(c>>(2*i+j)&1){++deg[i];++deg[2+j];}
  if(pc(c)<3 || *std::min_element(deg,deg+4)==0)continue;
  Graph g(5,5);
  const unsigned fixed[][2]={{2,8},{2,9},{7,3},{7,4},{0,9},{1,8},{5,4},{6,3}};
  for(auto& e:fixed)g.edge(e[0],e[1]);
  for(unsigned i=0;i<2;++i)for(unsigned j=0;j<2;++j){
   if(c>>(2*i+j)&1)g.edge(i,5+j);
   if(w>>(2*i+j)&1)g.edge(3+i,8+j);
  }
  auto [b,s]=exact(g);++templates;
  if(s-b==1){++equality;require(c==15 && w==15,"unexpected ten-vertex equality template");}
 }
 std::cout<<"{\n  \"status\":\"PASS\",\n  \"exhaustive_graph_presentations\":"<<exhaustive
 <<",\n  \"additional_seeded_graphs\":160,\n  \"ten_vertex_templates\":"<<templates
 <<",\n  \"ten_vertex_equality_templates\":"<<equality<<",\n  \"total_graph_presentations\":"<<models
 <<",\n  \"direct_subsets\":"<<subsets<<",\n  \"minimum_degree_at_least_two_presentations\":"<<eligible
 <<",\n  \"private_neighbour_formula_crosschecks\":"<<models<<"\n}\n";
}
