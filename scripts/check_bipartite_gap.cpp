// Finite verification of the general written proof, including both exchanges.
// All minimal sets and dissociation optima are computed directly.
#include <algorithm>
#include <array>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <random>
#include <stdexcept>
#include <vector>

using Mask = std::uint32_t;
struct Counts { std::uint64_t graphs=0, subsets=0, minimal=0, exchanges=0, equalities=0; };
Counts counts;
unsigned current_n;
Mask current_s;

void require(bool okay, const char* message) {
    if (!okay) {
        std::cerr << "Failure n=" << current_n << " selected=" << current_s << ": " << message << '\n';
        throw std::runtime_error(message);
    }
}
unsigned size(Mask x) { return __builtin_popcount(x); }
unsigned first(Mask x) { require(x != 0, "nonempty mask"); return __builtin_ctz(x); }
bool dissociation(const std::vector<Mask>& adj, Mask s) {
    for (Mask scan=s; scan; scan &= scan-1) {
        Mask ns = adj[first(scan)] & s;
        if (ns & (ns-1)) return false;
    }
    return true;
}

void proof(const std::vector<Mask>& adj, Mask side, Mask s, unsigned beta) {
    unsigned n=adj.size();
    Mask all=(1u<<n)-1, outside=all^s, r=0, isolates=0;
    current_n=n; current_s=s;
    for (Mask scan=s; scan; scan &= scan-1) {
        unsigned v=first(scan), degree=size(adj[v]&s);
        if (degree==0) { r |= 1u<<v; isolates |= 1u<<v; }
        if (degree==1 && size(adj[first(adj[v]&s)]&s)==1) r |= 1u<<v;
    }
    Mask c=s^r, used=0, witnesses=0;
    std::vector<std::array<unsigned,3>> triples;
    for (Mask scan=c; scan; scan &= scan-1) {
        unsigned center=first(scan);
        bool found=false;
        for (Mask leaves=adj[center]&c; leaves && !found; leaves &= leaves-1) {
            unsigned leaf=first(leaves);
            if ((adj[leaf]&s)!=(1u<<center)) continue;
            for (Mask outs=outside; outs; outs &= outs-1) {
                unsigned x=first(outs);
                if ((adj[x]&s)!=(1u<<leaf)) continue;
                Mask vertices=(1u<<center)|(1u<<leaf)|(1u<<x);
                require(!(vertices&used), "triples disjoint");
                used |= vertices; witnesses |= 1u<<x;
                triples.push_back({center,leaf,x}); found=true; break;
            }
        }
    }
    std::vector<std::array<unsigned,2>> pairs;
    std::array<unsigned,20> h{};
    for (Mask scan=c&~used; scan; scan &= scan-1) {
        unsigned v=first(scan);
        bool found=false;
        for (Mask outs=outside; outs; outs &= outs-1) {
            unsigned x=first(outs);
            Mask ns=adj[x]&s, rest=ns&~(1u<<v);
            if (!(ns&(1u<<v)) || size(rest)>1 || (rest&~isolates)) continue;
            Mask vertices=(1u<<v)|(1u<<x);
            require(!(vertices&used), "pairs disjoint from triples and other pairs");
            used |= vertices; witnesses |= 1u<<x;
            if (rest) ++h[first(rest)];
            pairs.push_back({v,x}); found=true; break;
        }
        require(found, "remaining vertex has form-1 or form-2 witness");
    }
    unsigned p=triples.size(), u=pairs.size(), a=0, b=0;
    Mask touched=0, multiple=0;
    for (Mask scan=isolates; scan; scan &= scan-1) {
        unsigned i=first(scan);
        if (h[i]) touched |= 1u<<i;
        if (h[i]==1) ++a;
        if (h[i]>=2) { ++b; multiple |= 1u<<i; }
    }
    require(!(used&touched), "touched isolates are new resources");
    require(size(s)==size(r)+2*p+u, "selected partition");
    require(u>=a+2*b, "isolate witness capacity");
    require(n>=3*p+2*u+a+b, "disjoint whole-graph budget");
    require(n>=3*p+3*a+5*b, "reduced budget");
    int first_sum=0, second_sum=0;
    for (Mask left : {side, all^side}) {
        Mask d=r&~(touched&left);
        for (auto triple:triples) {
            auto center=triple[0], leaf=triple[1], x=triple[2];
            d |= (1u<<leaf)|((left&(1u<<center)) ? (1u<<center) : (1u<<x));
        }
        for (auto pair:pairs) if (left&(1u<<pair[0])) d |= (1u<<pair[0])|(1u<<pair[1]);
        require(dissociation(adj,d), "first exchange is dissociation");
        require(size(d)<=beta, "first exchange bounded by direct optimum");
        first_sum+=size(d);
        Mask e=((s|witnesses)&left)|(r&~left&~multiple);
        require(dissociation(adj,e), "second exchange is dissociation");
        require(size(e)<=beta, "second exchange bounded by direct optimum");
        second_sum+=size(e);
        counts.exchanges+=2;
    }
    require(first_sum==2*int(size(s))-int(a+b), "first average identity");
    require(second_sum==2*int(size(s))-int(p+b), "second average identity");
    require(5*std::min(a,p)<=3*a+3*p, "arithmetic combination");
    require(10*(int(size(s))-int(beta))<=int(n), "sharp gap inequality");
    if (size(s)>beta && 10*(size(s)-beta)==n) {
        require(a==0 && p==0 && u==2*b && n==5*b, "equality budget");
        for (Mask scan=multiple; scan; scan &= scan-1)
            require(size(adj[first(scan)])==2, "equality isolate degree two");
        ++counts.equalities;
    }
}

void graph(const std::vector<Mask>& adj, Mask side) {
    unsigned n=adj.size();
    current_n=n; current_s=0;
    Mask limit=1u<<n, all=limit-1;
    std::vector<unsigned char> forming(limit);
    unsigned beta=0, sf=0;
    for (Mask s=0; s<limit; ++s) {
        if (dissociation(adj,s)) beta=std::max(beta,size(s));
        bool forms=true;
        for (Mask scan=all^s; scan; scan &= scan-1) {
            unsigned x=first(scan); Mask ns=adj[x]&s;
            if (size(ns)>=2) continue;
            if (!ns || !(adj[first(ns)]&s)) { forms=false; break; }
        }
        forming[s]=forms;
    }
    for (Mask s=0; s<limit; ++s) if (forming[s]) {
        bool minimal=true;
        for (Mask scan=s; scan; scan &= scan-1) {
            Mask bit=scan&-scan;
            if (forming[s^bit]) { minimal=false; break; }
        }
        if (!minimal) continue;
        sf=std::max(sf,size(s));
        proof(adj,side,s,beta); ++counts.minimal;
    }
    require(10*(int(sf)-int(beta))<=int(n), "exact parameter gap");
    ++counts.graphs; counts.subsets+=limit;
}

int main() {
    for (unsigned n=0; n<=8; ++n) for (unsigned a=0; a<=n/2; ++a) {
        unsigned b=n-a;
        for (Mask pattern=0; pattern<(1u<<(a*b)); ++pattern) {
            std::vector<Mask> adj(n);
            unsigned k=0;
            for (unsigned x=0; x<a; ++x) for (unsigned y=a; y<n; ++y,++k)
                if (pattern&(1u<<k)) { adj[x]|=1u<<y; adj[y]|=1u<<x; }
            graph(adj,(1u<<a)-1);
        }
    }
    auto exhaustive_graphs=counts.graphs, exhaustive_subsets=counts.subsets;
    std::mt19937 rng(20261111);
    for (unsigned trial=0; trial<256; ++trial) {
        unsigned n=9+trial%8, a=1+(trial/8)%(n-1);
        std::vector<Mask> adj(n);
        unsigned density=1+(trial/24)%7;
        for (unsigned x=0; x<a; ++x) for (unsigned y=a; y<n; ++y)
            if (rng()%8<density) { adj[x]|=1u<<y; adj[y]|=1u<<x; }
        graph(adj,(1u<<a)-1);
    }
    const std::array<const char*,5> rows{"11001","11010","00011","01111","10111"};
    std::vector<Mask> sharp(10);
    for (unsigned x=0; x<5; ++x) for (unsigned y=0; y<5; ++y)
        if (rows[x][y]=='1') { sharp[x]|=1u<<(y+5); sharp[y+5]|=1u<<x; }
    graph(sharp,31);
    std::cout << "{\n  \"status\":\"PASS\",\n  \"exhaustive_graph_models\":" << exhaustive_graphs
              << ",\n  \"exhaustive_subsets\":" << exhaustive_subsets
              << ",\n  \"scope\":\"All binary bipartite adjacency matrices with a+b<=8 and 0<=a<=b; no isomorphism reduction. Plus 256 seeded orders 9-16 and the sharp ten-vertex graph.\""
              << ",\n  \"graph_models\":" << counts.graphs << ",\n  \"subsets\":" << counts.subsets
              << ",\n  \"minimal_sets\":" << counts.minimal << ",\n  \"dissociation_exchanges\":" << counts.exchanges
              << ",\n  \"positive_exact_equality_selections\":" << counts.equalities << "\n}\n";
}
