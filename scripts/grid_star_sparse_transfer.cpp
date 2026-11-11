// Sparse exact deletion-witness transfer for height four.
#include <algorithm>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <fstream>
#include <string>
#include <filesystem>
#include <stdexcept>
#include <unordered_map>
#include <vector>
using U=uint32_t;using Table=std::unordered_map<U,int>;
int main(int argc,char**argv){
 int h=argc>1?std::atoi(argv[1]):4,limit=argc>2?std::atoi(argv[2]):40;
 size_t cap=1000000;
 std::string out=argc>3?argv[3]:"output";std::filesystem::create_directories(out);
 if(h!=4||limit<17||limit>100000)throw std::invalid_argument("require height 4 and 17<=limit<=100000");int vertices=5*h,masks=1<<h,windows=1<<vertices;
 U oldbits=(U(1)<<(4*h))-1,first=masks-1;
 std::vector<U> adj(vertices);for(int c=0;c<5;c++)for(int r=0;r<h;r++){
  int v=c*h+r;for(auto[a,b]:std::vector<std::pair<int,int>>{{c-1,r},{c+1,r},{c,r-1},{c,r+1}})if(a>=0&&a<5&&b>=0&&b<h)adj[v]|=U(1)<<(a*h+b);
 }
 std::vector<U> active(windows);for(int s=0;s<windows;s++)for(int v=0;v<vertices;v++)if((s>>v&1)&&(adj[v]&s))active[s]|=U(1)<<v;
 auto formed=[&](int x,U s){U near=adj[x]&s;return bool((near&(near-1))||(adj[x]&active[s]));};
 std::vector<int> kernel(windows,-1);for(int s=0;s<windows;s++){
  bool ok=true;U marked=0;for(int r=0;r<h;r++){int x=2*h+r;
   if(s>>x&1){if(!formed(x,s^(U(1)<<x)))marked|=U(1)<<x;}
   else{if(!formed(x,s)){ok=false;break;}for(int v=0;v<vertices;v++)if((s>>v&1)&&!formed(x,s^(U(1)<<v)))marked|=U(1)<<v;}
  }if(ok)kernel[s]=marked;
 }
 auto step=[&](U key,U column,bool real,U &target){U s=(key&oldbits)|(column<<(4*h)),flags=key>>(4*h);
  if(real){if(kernel[s]<0)return false;flags|=U(kernel[s]);}if((s&first)!=(flags&first))return false;
  target=(s>>h)|((flags>>h)<<(4*h));return true;};
 auto end=[&](U key,int n){for(int j=0;j<4;j++){U target;if(!step(key,0,0<=n+j-2&&n+j-2<n,target))return false;key=target;}return key==0;};
 int period=2,increment=4;Table table{{0,0}};std::vector<Table> history(period);
 std::vector<int> pop(masks);for(int s=0;s<masks;s++)pop[s]=__builtin_popcount(s);
 std::vector<int> optima;size_t certificate_states=0;bool translated=false;
 for(int n=1;n<=limit;n++){
  Table next;next.reserve(std::min(cap+10000,table.size()*2));
  for(auto[key,score]:table)for(int col=0;col<masks;col++){U target;if(!step(key,col,n>=3,target))continue;
   auto[it,fresh]=next.emplace(target,score+pop[col]);if(!fresh)it->second=std::max(it->second,score+pop[col]);
   if(next.size()>cap)throw std::runtime_error("resource state limit; no certificate produced");
  }
  table.swap(next);int best=-1;for(auto[key,score]:table)if(end(key,n))best=std::max(best,score);
  auto &previous=history[n%period];int mismatch=0;if(previous.empty())mismatch=-1;else{
   for(auto[key,score]:table){auto it=previous.find(key);if(it==previous.end()||it->second+increment!=score)mismatch++;}
   for(auto[key,score]:previous)if(!table.count(key))mismatch++;
  }
  optima.push_back(best);
  if(n==15||n==17){
   std::vector<std::pair<U,int>> rows(table.begin(),table.end());std::sort(rows.begin(),rows.end());
   std::ofstream cert(out+"/grid-star-h4-v"+std::to_string(n)+".tsv");
   if(!cert)throw std::runtime_error("certificate open failed");
   for(auto[key,score]:rows)cert<<key<<'\t'<<score<<'\n';
  }
  if(n==17){if(mismatch!=0)throw std::runtime_error("full-vector translation failed");translated=true;certificate_states=table.size();}
  std::cerr<<"height="<<h<<" length="<<n<<" SF="<<best<<" reachable="<<table.size()<<" mismatches="<<mismatch<<'\n';
  previous=table;
 }
 std::ofstream report(out+"/grid-star-transfer-h4.json");
 if(!report)throw std::runtime_error("report open failed");
 report<<"{\n  \"status\": \"PASS\",\n  \"height\": 4,\n  \"state_domain\": 43046721,\n  \"five_column_patterns\": 1048576,\n  \"optima\": [";
 for(size_t i=0;i<optima.size();i++){if(i)report<<", ";report<<optima[i];}
 report<<"],\n  \"translation_checked\": "<<(translated?"true":"false")<<",\n  \"start\": 15,\n  \"period\": 2,\n  \"increment\": 4,\n  \"reachable_certificate_states\": "<<certificate_states<<",\n  \"new_Lean\": false\n}\n";
 std::cout<<"PASS height=4 lengths="<<limit<<" translation="<<translated<<'\n';
}
