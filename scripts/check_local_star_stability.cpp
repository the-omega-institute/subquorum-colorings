// Independent literal finite controls for local upper-star-forming stability.
// c++ -O3 -std=c++17 scripts/check_local_star_stability.cpp -o /tmp/star-locality
// /tmp/star-locality > output/local-star-stability-check.json
#include <algorithm>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <random>
#include <vector>
using M=std::uint32_t;
using U=std::uint64_t;
struct Graph {
    std::vector<M> a;
    explicit Graph(int n):a(n){}
    void edge(int v,int w){a[v]|=M(1)<<w;a[w]|=M(1)<<v;}
    M all()const{return (M(1)<<a.size())-1;}
    M ball(M start,int radius)const{
        M seen=start;
        for(int r=0;r<radius;++r){M added=seen;
            for(M bits=seen;bits;bits&=bits-1)added|=a[__builtin_ctz(bits)];
            seen=added;
        }
        return seen;
    }
    M failed(M h,M s)const{
        M active=0,result=0;
        for(M bits=s;bits;bits&=bits-1){int v=__builtin_ctz(bits);
            if(a[v]&s)active|=M(1)<<v;}
        for(M bits=h^s;bits;bits&=bits-1){int v=__builtin_ctz(bits);M ns=a[v]&s;
            if(!(ns&(ns-1)) && !(a[v]&active))result|=M(1)<<v;
        }
        return result;
    }
    M literal(M h,M s)const{
        M result=0;
        for(M bits=h^s;bits;bits&=bits-1){int x=__builtin_ctz(bits);bool ok=false;
            for(M one=s;one && !ok;one&=one-1){int v=__builtin_ctz(one);
                for(M two=one&(one-1);two;two&=two-1){int w=__builtin_ctz(two);
                    int edges=bool(a[x]&(M(1)<<v))+bool(a[x]&(M(1)<<w))
                              +bool(a[v]&(M(1)<<w));
                    if(edges>=2){ok=true;break;}
                }
            }
            if(!ok)result|=M(1)<<x;
        }
        return result;
    }
};
struct Counts {
    U exhaustive_graphs=0,seeded_graphs=0,literal_star_subsets=0;
    U induced_selection_states=0,minimal_sets=0,addition_pairs=0;
    U protected_addition_witnesses=0,interface_repair_pairs=0;
    U protected_repair_vertices=0,lower_lifts=0,protected_lower_vertices=0;
    U parameter_bounds=0,ear_models=0,ear_literal_subsets=0;
} c;
void need(bool test,const char* label){if(!test){std::cerr<<"FAIL "<<label<<"\n";std::exit(1);}}
struct Tables {
    int side;M full;std::vector<M> failure;std::vector<int> sf;
    std::vector<std::vector<M>> minimal;
    explicit Tables(const Graph& g):side(g.all()+1),full(g.all()),
        failure(side*side),sf(side),minimal(side){
        for(M h=0;h<=full;++h){
            for(M s=h;;s=(s-1)&h){failure[h*side+s]=g.failed(h,s);
                ++c.induced_selection_states;if(!s)break;}
            for(M s=h;;s=(s-1)&h){
                if(!get(h,s)){bool ok=true;
                    for(M bits=s;bits;bits&=bits-1){M bit=bits&(~bits+1);
                        if(!get(h,s^bit)){ok=false;break;}}
                    if(ok){minimal[h].push_back(s);sf[h]=std::max(sf[h],__builtin_popcount(s));++c.minimal_sets;}
                }
                if(!s)break;
            }
        }
    }
    M get(M h,M s)const{return failure[h*side+s];}
};
void test(const Graph& g){
    Tables t(g);M full=g.all();
    for(M s=0;s<=full;++s){need(t.get(full,s)==g.literal(full,s),"literal star predicate");++c.literal_star_subsets;}
    for(M s:t.minimal[full]){
        M comp=full^s;
        for(M added=comp;;added=(added-1)&comp){
            M near=g.ball(added,3);++c.addition_pairs;
            for(M bits=s&~near;bits;bits&=bits-1){M bit=bits&(~bits+1);
                M old=t.get(full,s^bit),now=t.get(full,(s|added)^bit);
                need(old && !(old&~now),"all original far addition witnesses survive");
                ++c.protected_addition_witnesses;
            }
            if(!added)break;
        }
        for(M u=0;u<=full;++u){M h=full^u,sh=s&h;
            M added=t.get(h,sh),repair=sh|added;
            need(!(added&~g.ball(u,2)),"repair in radius two");
            need(!t.get(h,repair),"repair forms induced graph");
            M forced=sh&~(g.ball(u,2)|g.ball(added,3));
            for(M bits=forced;bits;bits&=bits-1){M bit=bits&(~bits+1);
                M old=t.get(full,s^bit)&h,now=t.get(h,repair^bit);
                need(old && !(old&~now),"original repair witnesses survive");
                ++c.protected_repair_vertices;
            }
            M minimized=repair;
            for(int v=0;v<int(g.a.size());++v){M bit=M(1)<<v;
                if((minimized&bit) && !t.get(h,minimized^bit))minimized^=bit;}
            need(!(forced&~minimized),"forced selections retained on minimization");
            need(__builtin_popcount(s)<=t.sf[h]+__builtin_popcount(s&u)
                 +__builtin_popcount(sh&(g.ball(u,2)|g.ball(added,3))),"adaptive upper");
            ++c.interface_repair_pairs;
        }
    }
    for(M h=0;h<=full;++h){M u=full^h;
        need(t.sf[full]>=t.sf[h]-__builtin_popcount(h&g.ball(u,3)),"lower parameter bound");
        need(t.sf[full]<=t.sf[h]+__builtin_popcount(u)+__builtin_popcount(h&g.ball(u,5)),"upper parameter bound");
        ++c.parameter_bounds;
        for(M s:t.minimal[h]){M lifted=s|u;need(!t.get(full,lifted),"lower lift forms");
            for(M bits=s&~g.ball(u,3);bits;bits&=bits-1){M bit=bits&(~bits+1);
                need(t.get(full,lifted^bit)!=0,"lower lift protected vertex");++c.protected_lower_vertices;}
            ++c.lower_lifts;
        }
    }
}
int literal_sf(const Graph& g,M h){
    std::vector<M> failed(g.all()+1);int result=0;
    for(M s=h;;s=(s-1)&h){failed[s]=g.failed(h,s);if(!s)break;}
    for(M s=h;;s=(s-1)&h){if(!failed[s]){bool minimal=true;
        for(M bits=s;bits;bits&=bits-1){M bit=bits&(~bits+1);if(!failed[s^bit]){minimal=false;break;}}
        if(minimal)result=std::max(result,__builtin_popcount(s));}
        ++c.ear_literal_subsets;if(!s)break;}
    return result;
}
void ear_case(const Graph& base,const std::vector<std::pair<int,int>>& matching){
    int n=base.a.size(),k=matching.size();Graph g(n+2*k);M roots=0;
    for(int v=0;v<n;++v)for(int w=v+1;w<n;++w)if(base.a[v]&(M(1)<<w))g.edge(v,w);
    for(int j=0;j<k;++j){auto [d,e]=matching[j];int a=n+2*j,b=a+1;
        g.edge(d,a);g.edge(a,b);g.edge(b,e);roots|=(M(1)<<d)|(M(1)<<e);}
    M residual=base.all()^roots;int small=literal_sf(base,residual),large=literal_sf(g,g.all());
    int footprint=__builtin_popcount(residual&base.ball(roots,5));
    int delta=0;for(M row:g.a)delta=std::max(delta,__builtin_popcount(row));
    int numeric=0,power=1;for(int j=0;j<5;++j){numeric+=power;power*=std::max(0,delta-1);}
    numeric*=2*k*std::max(0,delta-2);
    need(large>=2*k+small && large<=2*k+small+footprint,"ear footprint bound");
    need(footprint<=numeric || !k,"ear BFS bound");
    ++c.ear_models;
}
void enumerate_matchings(const Graph& base,int v,M used,std::vector<std::pair<int,int>>& matching){
    if(v==int(base.a.size())){ear_case(base,matching);return;}
    enumerate_matchings(base,v+1,used,matching);
    if(used&(M(1)<<v))return;
    for(int w=v+1;w<int(base.a.size());++w)if(!(used&(M(1)<<w)) && (base.a[v]&(M(1)<<w))){
        matching.push_back({v,w});enumerate_matchings(base,v+1,used|(M(1)<<v)|(M(1)<<w),matching);matching.pop_back();}
}
int main(){
    for(int n=0;n<=5;++n){int edges=n*(n-1)/2;
        for(M bits=0;bits<(M(1)<<edges);++bits){Graph g(n);int at=0;
            for(int v=0;v<n;++v)for(int w=v+1;w<n;++w,++at)if(bits&(M(1)<<at))g.edge(v,w);
            test(g);++c.exhaustive_graphs;
            if(n<=4){std::vector<std::pair<int,int>> matching;enumerate_matchings(g,0,0,matching);}
        }
    }
    std::mt19937 rng(20261112);
    for(int n=6;n<=9;++n)for(int sample=0;sample<24;++sample){Graph g(n);
        unsigned threshold=unsigned(sample%8+1)*10;
        for(int v=0;v<n;++v)for(int w=v+1;w<n;++w)if(rng()%100<threshold)g.edge(v,w);
        test(g);++c.seeded_graphs;
    }
    Graph path(9);for(int j=0;j<8;++j)path.edge(j,j+1);
    M s=(M(1)<<0)|(M(1)<<1)|(M(1)<<4)|(M(1)<<5)|(M(1)<<6)|(M(1)<<8),a=M(1)<<2,v=M(1)<<5;
    need(!path.failed(path.all(),s),"sharp path formation");
    for(M bits=s;bits;bits&=bits-1)need(path.failed(path.all(),s^(bits&(~bits+1)))!=0,"sharp path minimality");
    need(!path.failed(path.all(),(s|a)^v),"sharp addition witness");
    M h=path.all()^1,sh=s&h;need(path.failed(h,sh)==a,"sharp deletion repair");
    need(!path.failed(h,(sh|a)^v),"sharp repaired deletion");
    need(!(path.ball(a,2)&v) && (path.ball(a,3)&v),"addition distance exactly three");
    need(!(path.ball(1,4)&v) && (path.ball(1,5)&v),"deletion distance exactly five");
    test(path);++c.seeded_graphs;
    // A research-stage minimum over ALL minimal forming sets is false.
    // Taking U=V(K1,3) would incorrectly give SF(K1,3)<=2.
    Graph claw(4);for(int j=1;j<4;++j)claw.edge(0,j);
    Tables claw_tables(claw);int smallest=4;
    for(M selected:claw_tables.minimal[claw.all()])
        smallest=std::min(smallest,__builtin_popcount(selected));
    need(claw_tables.sf[claw.all()]==3 && smallest==2,"false all-minimal minimum regression");
    std::cout<<"{\n  \"status\": \"PASS\",\n";
#define ROW(name) std::cout<<"  \"" #name "\": "<<c.name<<",\n"
    ROW(exhaustive_graphs);ROW(seeded_graphs);ROW(literal_star_subsets);ROW(induced_selection_states);
    ROW(minimal_sets);ROW(addition_pairs);ROW(protected_addition_witnesses);
    ROW(interface_repair_pairs);ROW(protected_repair_vertices);ROW(lower_lifts);
    ROW(protected_lower_vertices);ROW(parameter_bounds);ROW(ear_models);ROW(ear_literal_subsets);
    std::cout<<"  \"sharp_addition_radius\": 3,\n  \"sharp_repair_radius\": 5,\n"
             <<"  \"false_all_minimal_minimum_counterexample\": {\"SF_K13\": 3, \"smallest_minimal\": 2},\n"
             <<"  \"new_Lean\": false\n}\n";
}
