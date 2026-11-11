// Independent exhaustive control: all two-per-cluster choices, not the p/q proof.
// c++ -O3 -std=c++17 scripts/check_ear_activity_obstruction.cpp -o /tmp/ear-check
// /tmp/ear-check > output/ear-activity-exhaustive-check.json
#include <algorithm>
#include <array>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <vector>
using Mask=std::uint64_t;
struct Result {std::uint64_t candidates=0,forming=0,minimal=0;int best=0;};
bool forms(const std::vector<Mask>& adj,Mask selected){
    Mask active=0;
    for(int v=0;v<int(adj.size());++v)
        if((selected>>v&1) && (adj[v]&selected))active|=Mask(1)<<v;
    for(int v=0;v<int(adj.size());++v) if(!(selected>>v&1)){
        Mask ns=adj[v]&selected;
        if(!(ns&(ns-1)) && !(adj[v]&active))return false;
    }
    return true;
}
Result run(bool square,int m){
    int base=(square?4:3)*m,n=base+2*m;
    std::vector<Mask> adj(n);
    auto edge=[&](int u,int v){adj[u]|=Mask(1)<<v;adj[v]|=Mask(1)<<u;};
    for(int i=0;i<m;++i)for(int j=i+1;j<m;++j){edge(i,j);edge(m+i,m+j);}
    std::vector<std::vector<Mask>> choices;
    for(int i=0;i<m;++i){
        int d=2*m+i,a=base+2*i,b=a+1;
        edge(d,i);edge(d,m+i);edge(d,a);edge(a,b);
        std::vector<int> cluster={d,a,b};
        if(square){int e=3*m+i;edge(d,e);edge(e,b);cluster.push_back(e);}
        std::vector<Mask> pairs;
        for(int j=0;j<int(cluster.size());++j)for(int l=j+1;l<int(cluster.size());++l)
            pairs.push_back((Mask(1)<<cluster[j])|(Mask(1)<<cluster[l]));
        choices.push_back(pairs);
    }
    std::vector<Mask> selections={0};
    for(const auto& pairs:choices){
        std::vector<Mask> next;
        for(Mask prefix:selections)for(Mask pair:pairs)next.push_back(prefix|pair);
        selections.swap(next);
    }
    Result result;
    for(Mask ears:selections)for(Mask f=0;f<(Mask(1)<<(2*m));++f){
        ++result.candidates;Mask s=ears|f;
        if(!forms(adj,s))continue;
        ++result.forming;bool minimal=true;
        for(Mask bits=s;bits;bits&=bits-1){
            Mask v=bits&(~bits+1);
            if(forms(adj,s^v)){minimal=false;break;}
        }
        if(minimal){++result.minimal;result.best=std::max(result.best,__builtin_popcountll(s));}
    }
    // Local cap is a proved premise of the exhaustive domain. No p/q pruning.
    if(result.best!=3*m)std::exit(1);
    return result;
}
int main(){
    const int m=5;
    Result square=run(true,m),path=run(false,m);
    auto row=[](const char* name,const Result& r){
        std::cout<<"  \""<<name<<"\": {\"candidates\": "<<r.candidates
                 <<", \"forming\": "<<r.forming<<", \"minimal\": "<<r.minimal
                 <<", \"maximum_size\": "<<r.best<<"}";
    };
    std::cout<<"{\n  \"status\": \"PASS\",\n  \"m\": 5,\n"
             <<"  \"domain\": \"all two-per-cluster sets and all residual subsets; local-cap lemma assumed\",\n";
    row("square",square);std::cout<<",\n";row("path",path);std::cout<<"\n}\n";
}
