// Independently enumerate local assignments, then compare every DP entry
// against the saved translation vectors. No solver or first implementation used.
#include <algorithm>
#include <array>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <vector>
using Key=unsigned long long;
using Values=std::unordered_map<Key,int>;

std::vector<int> decode(Key s,int width) {
  std::vector<int> a(width);
  for(int i=0;i<width;++i){a[i]=s%8;s/=8;}
  return a;
}
Key encode(const std::vector<int>& a) {
  Key s=0;for(auto it=a.rbegin();it!=a.rend();++it)s=8*s+*it;return s;
}
Values advance(const Values& values,int c,int width) {
  Values next;next.reserve(values.size()*2);
  for(auto [key,score]:values) {
    auto a=decode(key,width);
    int up=a[c],left=c?a[c-1]:0;
    // Candidate labels: empty, T, matched-to-past, matched-below, matched-right.
    for(int candidate:std::array<int,5>{0,1,3,4,5}) {
      bool occupied=candidate!=0;
      int requests=(up==4)+(left==5);
      if(up==5 || requests>1) continue;
      if((candidate==3)!=(requests==1))continue;
      if(candidate==5 && c==width-1)continue;
      if(occupied && (up==2 || left==2))continue;
      if(candidate==1 && (up!=0)+(left!=0)>1)continue;
      auto b=a;
      b[c]=candidate;
      if(candidate==1)b[c]=1+(up!=0)+(left!=0);
      if(c && occupied && left==1)b[c-1]=2;
      if(c && left==5 && candidate==3)b[c-1]=3;
      Key target=encode(b);
      int newscore=score+(candidate==1?2:occupied?1:0);
      auto it=next.find(target);
      if(it==next.end())next.emplace(target,newscore);
      else it->second=std::max(it->second,newscore);
    }
  }
  return next;
}
Values load(const std::string& file) {
  std::ifstream in(file);if(!in)throw std::runtime_error("missing vector");
  Values v;Key key;int value;
  while(in>>key>>value)if(!v.emplace(key,value).second)throw std::runtime_error("duplicate state");
  return v;
}
int main(int argc,char** argv) {
  if(argc!=6)throw std::runtime_error("usage: check_omega WIDTH START PERIOD DELTA PREFIX");
  int width=std::stoi(argv[1]),start=std::stoi(argv[2]),period=std::stoi(argv[3]),delta=std::stoi(argv[4]);
  auto first=load(std::string(argv[5])+"-start.tsv");
  auto last=load(std::string(argv[5])+"-end.tsv");
  if(first.size()!=last.size())throw std::runtime_error("support mismatch");
  for(auto [s,w]:first)if(!last.count(s)||last.at(s)!=w+delta)throw std::runtime_error("translation mismatch");
  Values values{{0,0}};
  for(int n=1;n<=start+period;++n) {
    for(int c=0;c<width;++c)values=advance(values,c,width);
    if(n==start && values!=first)throw std::runtime_error("start vector mismatch");
    if(n==start+period && values!=last)throw std::runtime_error("end vector mismatch");
  }
  std::cout<<"PASS width="<<width<<" start="<<start<<" period="<<period
           <<" doubled_increment="<<delta<<" states="<<last.size()<<'\n';
}
