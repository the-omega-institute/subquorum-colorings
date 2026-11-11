// Full literal subset verification of F_2 (21 vertices) and G_2 (25 vertices).
// c++ -O3 -std=c++17 scripts/check_bipartite_ear_obstruction.cpp -o /tmp/bip-ear
// /tmp/bip-ear > output/bipartite-ear-literal-check.json
#include <algorithm>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <vector>
using Mask=std::uint32_t;
struct Result{int order=0,beta=0,SF=0;std::uint64_t subsets=0,minimal=0;};
Result solve(bool ear){
    int n=ear?25:21;std::vector<Mask> adj(n);
    auto edge=[&](int a,int b){adj[a]|=Mask(1)<<b;adj[b]|=Mask(1)<<a;};
    for(int c=0;c<2;++c){int o=10*c;
        for(int i=0;i<2;++i)for(int j=0;j<2;++j){edge(o+i,o+2+j);edge(o+4+i,o+6+j);}
        for(int i=0;i<2;++i){edge(o+i,o+6+i);edge(o+2+i,o+4+i);
            edge(o+8,o+6+i);edge(o+9,o+4+i);edge(20,o+6+i);}
    }
    if(ear){edge(21,22);edge(21,20);edge(21,23);edge(23,24);edge(24,22);}
    Mask end=Mask(1)<<n;std::vector<unsigned char> formed(end);
    Result r;r.order=n;r.subsets=end;
    for(Mask s=0;s<end;++s){
        Mask active=0;bool diss=true;
        for(Mask bits=s;bits;bits&=bits-1){int v=__builtin_ctz(bits);Mask ns=adj[v]&s;
            if(ns)active|=Mask(1)<<v;
            if(ns&(ns-1))diss=false;
        }
        int size=__builtin_popcount(s);if(diss)r.beta=std::max(r.beta,size);
        bool ok=true;
        for(Mask bits=(end-1)^s;bits;bits&=bits-1){int v=__builtin_ctz(bits);Mask ns=adj[v]&s;
            if(!(ns&(ns-1)) && !(adj[v]&active)){ok=false;break;}
        }
        formed[s]=ok;
        if(ok){bool minimal=true;
            for(Mask bits=s;bits;bits&=bits-1){Mask bit=bits&(~bits+1);
                if(formed[s^bit]){minimal=false;break;}
            }
            if(minimal){++r.minimal;r.SF=std::max(r.SF,size);}
        }
    }
    if(r.SF!=(ear?14:11) || r.beta!=(ear?13:11))std::exit(1);
    return r;
}
int main(){
    Result f=solve(false),g=solve(true);
    auto row=[](const char* name,const Result& r){std::cout<<"  \""<<name<<"\": {\"order\": "
        <<r.order<<", \"subsets\": "<<r.subsets<<", \"minimal_sets\": "<<r.minimal
        <<", \"beta\": "<<r.beta<<", \"SF\": "<<r.SF<<"}";};
    std::cout<<"{\n  \"status\": \"PASS\",\n  \"domain\": \"all vertex subsets, with all single deletions tested\",\n";
    row("F",f);std::cout<<",\n";row("G",g);std::cout<<"\n}\n";
}
