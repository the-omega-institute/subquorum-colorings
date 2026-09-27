// Exact frontier DP for Omega on a width-by-length rectangular grid.
// Digits: 0 unused; 1/2 T with 0/1 occupied processed neighbors;
// 3 matched endpoint; 4 endpoint awaiting below; 5 endpoint awaiting right.
#include <algorithm>
#include <deque>
#include <fstream>
#include <iostream>
#include <limits>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <utility>
#include <vector>

using State = unsigned long long;
using Table = std::unordered_map<State, int>;
using Vector = std::vector<std::pair<State, int>>;

int digit(State s, int c) { return int((s >> (3*c)) & 7); }
State put(State s, int c, int d) {
  return (s & ~(State(7) << (3*c))) | (State(d) << (3*c));
}
void improve(Table& next, State s, int value) {
  auto [it, inserted] = next.emplace(s, value);
  if (!inserted && value > it->second) it->second = value;
}
Table step(const Table& old, int c, int width) {
  Table next;
  next.reserve(old.size()*2);
  for (const auto& [s, value] : old) {
    int up = digit(s,c), left = c ? digit(s,c-1) : 0;
    if (up == 5) throw std::runtime_error("unclosed horizontal matching edge");
    int forced = (up == 4) + (left == 5);
    if (!forced) improve(next, put(s,c,0), value);
    // Any newly occupied vertex consumes one neighbor allowance of nearby T.
    if (up == 2 || left == 2 || forced == 2) continue;
    State base = s;
    if (c && left == 1) base = put(base,c-1,2);
    if (c && left == 5) base = put(base,c-1,3);
    if (forced) {
      improve(next, put(base,c,3), value+1);
    } else {
      int occupied = (up != 0) + (left != 0);
      if (occupied <= 1) improve(next, put(base,c,1+occupied), value+2);
      improve(next, put(base,c,4), value+1);
      if (c+1 < width) improve(next, put(base,c,5), value+1);
    }
  }
  return next;
}
bool terminal(State s, int width) {
  for(int c=0;c<width;++c) if(digit(s,c)>=4) return false;
  return true;
}
int conjecture(int m,int n) {
  return std::max(((m+1)/2)*((2*n+2)/3)+(m/2)*(n/3),
                  ((n+1)/2)*((2*m+2)/3)+(n/2)*(m/3));
}
void save(const Vector& v,const std::string& path) {
  std::ofstream out(path);
  if(!out) throw std::runtime_error("cannot write certificate");
  for(auto [s,w]:v) out<<s<<'\t'<<w<<'\n';
}
int main(int argc,char** argv) {
  if(argc<3) throw std::runtime_error("usage: grid_omega WIDTH MAX_LENGTH [CERT_PREFIX]");
  int width=std::stoi(argv[1]), limit=std::stoi(argv[2]);
  if(width<1 || width>12 || limit<1) throw std::runtime_error("unsupported size");
  Table table{{0,0}};
  std::deque<std::pair<int,Vector>> history;
  bool certified=false;
  std::cout<<"width,length,states,omega,conjectured\n";
  for(int n=1;n<=limit;++n) {
    for(int c=0;c<width;++c) table=step(table,c,width);
    int best=0;
    for(auto [s,w]:table) if(terminal(s,width)) {
      if(w%2) throw std::runtime_error("odd completed matching weight");
      best=std::max(best,w/2);
    }
    std::cout<<width<<','<<n<<','<<table.size()<<','<<best<<','<<conjecture(width,n)<<std::endl;
    if(!certified) {
      Vector v(table.begin(),table.end());std::sort(v.begin(),v.end());
      for(auto it=history.rbegin();it!=history.rend();++it) {
        const auto& [k,old]=*it;
        if(old.size()!=v.size())continue;
        int delta=v.front().second-old.front().second;
        bool same=true;
        for(size_t i=0;i<v.size();++i)
          if(v[i].first!=old[i].first || v[i].second-old[i].second!=delta){same=false;break;}
        if(same) {
          std::cerr<<"FULL_VECTOR_TRANSLATION width="<<width<<" start="<<k
                   <<" period="<<n-k<<" doubled_increment="<<delta
                   <<" states="<<v.size()<<std::endl;
          if(argc>3) {
            save(old,std::string(argv[3])+"-start.tsv");
            save(v,std::string(argv[3])+"-end.tsv");
            std::ofstream meta(std::string(argv[3])+".json");
            meta<<"{\"width\":"<<width<<",\"start\":"<<k<<",\"period\":"<<n-k
                <<",\"doubled_increment\":"<<delta<<",\"states\":"<<v.size()<<"}\n";
          }
          certified=true;break;
        }
      }
      history.emplace_back(n,std::move(v));
      if(history.size()>6)history.pop_front();
      if(certified)history.clear();
    }
  }
}
