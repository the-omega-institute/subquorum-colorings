// Exact minimal two-star-forming transfer; full definition in the proof note.
#include <algorithm>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <fstream>
#include <string>
#include <stdexcept>
#include <filesystem>
#include <limits>
#include <vector>
using U=uint32_t;
int main(int argc,char**argv){
 int h=argc>1?std::atoi(argv[1]):3,limit=argc>2?std::atoi(argv[2]):15;
 std::string out=argc>3?argv[3]:"output";std::filesystem::create_directories(out);
 if(h!=3||limit<15||limit>100000)
  throw std::invalid_argument("require height 3 and 15<=limit<=100000");
 int vertices=5*h,states=1;for(int i=0;i<4*h;i++)states*=3;
 int masks=1<<h,small=1<<(4*h),windows=1<<vertices;U low=masks-1;
 std::vector<U> adj(vertices);for(int c=0;c<5;c++)for(int r=0;r<h;r++){
  int v=c*h+r;for(auto[a,b]:std::vector<std::pair<int,int>>{{c-1,r},{c+1,r},{c,r-1},{c,r+1}})if(a>=0&&a<5&&b>=0&&b<h)adj[v]|=U(1)<<(a*h+b);
 }
 std::vector<U> active(windows);for(int s=0;s<windows;s++)for(int v=0;v<vertices;v++)if((s>>v&1)&&(adj[v]&s))active[s]|=U(1)<<v;
 auto formed=[&](int x,U s){U near=adj[x]&s;return bool((near&(near-1))||(adj[x]&active[s]));};
 // Local certificates at every vertex of the middle column. Selected
 // centres may certify only their own deletion; omitted centres may certify
 // every deletion that destroys their formation. -1 rejects unformed centres.
 std::vector<int> witness(windows,-1);for(int s=0;s<windows;s++){
  bool valid=true;U bits=0;for(int r=0;r<h;r++){
   int x=2*h+r;
   if(s>>x&1){if(!formed(x,s^(U(1)<<x)))bits|=U(1)<<x;}
   else{if(!formed(x,s)){valid=false;break;}for(int v=0;v<vertices;v++)if((s>>v&1)&&!formed(x,s^(U(1)<<v)))bits|=U(1)<<v;}
  }if(valid)witness[s]=bits;
 }
 std::vector<int> enc(small);for(int s=1;s<small;s++)enc[s]=enc[s>>1]*3+(s&1);
 // The recurrence above puts bit i at ternary position i.
 std::vector<U> selected(states),marked(states);for(int code=0;code<states;code++){
  int z=code;for(int v=0;v<4*h;v++){int digit=z%3;z/=3;if(digit)selected[code]|=U(1)<<v;if(digit==2)marked[code]|=U(1)<<v;}
 }
 // Separate real-centre and absent-centre transfers. Absent positions
 // cannot witness deletions and have no formation obligation.
 std::vector<int> next(states*masks),skip(states*masks);
 for(int code=0;code<states;code++)for(int mask=0;mask<masks;mask++){
  U s=selected[code]|(U(mask)<<(4*h)),base=marked[code];
  auto transfer=[&](bool use){if(use&&witness[s]<0)return -1;U flags=base|(use?U(witness[s]):0);
   if((flags&low)!=(s&low))return -1;return enc[s>>h]+enc[flags>>h];};
  next[code*masks+mask]=transfer(true);skip[code*masks+mask]=transfer(false);
 }
 // At length>=2 the right tail has two real and then two absent
 // centres. At length one its first centre is absent and its second real.
 std::vector<uint8_t> end(states),end_one(states);for(int code=0;code<states;code++){
  int z=code;for(int k=0;k<4&&z>=0;k++)z=(k<2?next:skip)[z*masks];end[code]=(z==0);
  z=code;for(int k=0;k<4&&z>=0;k++)z=(k==1?next:skip)[z*masks];end_one[code]=(z==0);
 }
 constexpr int neg=-1000000;std::vector<int> value(states,neg),old(states,neg);value[0]=0;
 std::vector<std::vector<int>> history(3);std::vector<int> pop(masks);for(int mask=0;mask<masks;mask++)pop[mask]=__builtin_popcount(mask);
 std::vector<int> optima;bool translated=false;
 for(int n=1;n<=limit;n++){
  std::fill(old.begin(),old.end(),neg);auto &transition=n<=2?skip:next;size_t reachable=0;
  for(int code=0;code<states;code++)if(value[code]>neg)for(int mask=0;mask<masks;mask++){
   int z=transition[code*masks+mask];if(z>=0)old[z]=std::max(old[z],value[code]+pop[mask]);
  }
  value.swap(old);int best=neg;for(int code=0;code<states;code++)if(value[code]>neg){reachable++;if((n==1?end_one:end)[code])best=std::max(best,value[code]);}
  int mismatches=-1;if(!history[n%3].empty()){
   mismatches=0;int delta=5;
   for(int code=0;code<states;code++)if((value[code]==neg)!=(history[n%3][code]==neg)||(value[code]>neg&&value[code]!=history[n%3][code]+delta))mismatches++;
  }
  optima.push_back(best);
  if(h==3&&(n==12||n==15)){
   std::ofstream cert(out+"/grid-star-h3-v"+std::to_string(n)+".tsv");
   if(!cert)throw std::runtime_error("certificate open failed");
   for(int code=0;code<states;code++)if(value[code]>neg)cert<<code<<'\t'<<value[code]<<'\n';
  }
  if(h==3&&n==15){if(mismatches!=0)throw std::runtime_error("full-vector translation failed");translated=true;}
  std::cerr<<"height="<<h<<" length="<<n<<" SF="<<best<<" reachable="<<reachable<<" mismatches="<<mismatches<<'\n';
  history[n%3]=value;
 }
 if(h==3&&limit<15)throw std::runtime_error("need all certificate lengths through 15");
 std::ofstream report(out+"/grid-star-transfer-h"+std::to_string(h)+".json");
 if(!report)throw std::runtime_error("report open failed");
 report<<"{\n  \"status\": \"PASS\",\n  \"height\": "<<h<<",\n  \"state_domain\": "<<states<<",\n  \"five_column_patterns\": "<<windows<<",\n  \"optima\": [";
 for(size_t i=0;i<optima.size();i++){if(i)report<<", ";report<<optima[i];}
 report<<"],\n  \"translation_checked\": "<<(translated?"true":"false")<<",\n  \"start\": 12,\n  \"period\": 3,\n  \"increment\": 5,\n  \"new_Lean\": false\n}\n";
 std::cout<<"PASS height="<<h<<" lengths="<<limit<<" translation="<<translated<<'\n';
}
