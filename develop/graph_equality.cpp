// Exhaust all labelled simple graphs on n<=6 vertices and all partial colorings.
// For fixed support S, a color class C is allowed exactly when every v in C
// has 1+degree_S(v) <= 2*(1+degree_C(v)). Maximize an exact partition into C's.
#include <algorithm>
#include <iostream>
#include <stdexcept>
#include <vector>
int bits(unsigned x){return __builtin_popcount(x);}
int main(int argc,char** argv) {
  int n=argc>1?std::stoi(argv[1]):6;
  if(n<1||n>6)throw std::runtime_error("range 1..6");
  int edgecount=n*(n-1)/2,limit=1<<n,total=1<<edgecount;
  long long gaps=0,bipartite_count=0;
  for(int graph=0;graph<total;++graph) {
    std::vector<unsigned> adj(n);int e=0;
    for(int i=0;i<n;++i)for(int j=i+1;j<n;++j,++e)
      if(graph>>e&1){adj[i]|=1u<<j;adj[j]|=1u<<i;}
    int beta=0,psi=0;
    for(unsigned s=1;s<(unsigned)limit;++s) {
      bool valid=true;
      for(int v=0;v<n;++v)if((s>>v&1)&&bits(adj[v]&s)>1){valid=false;break;}
      if(valid)beta=std::max(beta,bits(s));
      std::vector<bool> allowed(limit,false);
      for(unsigned c=s;c;c=(c-1)&s) {
        allowed[c]=true;
        for(int v=0;v<n;++v)if((c>>v&1)&&1+bits(adj[v]&s)>2*(1+bits(adj[v]&c))){allowed[c]=false;break;}
      }
      std::vector<int> partition(limit,-100);partition[0]=0;
      for(unsigned remaining=1;remaining<(unsigned)limit;++remaining)if((remaining&s)==remaining) {
        unsigned anchor=remaining&-remaining;
        for(unsigned c=remaining;c;c=(c-1)&remaining)
          if((c&anchor)&&allowed[c])partition[remaining]=std::max(partition[remaining],1+partition[remaining^c]);
      }
      psi=std::max(psi,partition[s]);
    }
    bool bip=false;
    for(unsigned side=0;side<(unsigned)limit&&!bip;++side) {
      bip=true;
      for(int v=0;v<n;++v)
        if(adj[v]&((side>>v&1)?side:((limit-1)^side))){bip=false;break;}
    }
    bipartite_count+=bip;
    if(psi<beta)throw std::runtime_error("lower bound violation");
    if(psi>beta){
      ++gaps;
      std::cout<<"GAP n="<<n<<" graph_mask="<<graph<<" beta2="<<beta<<" psi="<<psi<<" bipartite="<<bip<<'\n';
    }
  }
  std::cout<<"COMPLETE n="<<n<<" labelled_graphs="<<total<<" bipartite_graphs="<<bipartite_count<<" strict_gaps="<<gaps<<'\n';
}
