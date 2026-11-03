#include "../firmware/ChairMonitor/Monitor.h"
#include <assert.h>
#include <stdio.h>
#include <vector>
struct Seen { Monitor::Event kind; uint32_t at; uint32_t duration; };
struct Rig {
  Monitor m; std::vector<Seen> events;
  void sample(uint32_t now, float kg) {
    auto e=m.step(now,true,kg);
    if(e!=Monitor::NONE) events.push_back({e,now,e==Monitor::END?m.endedDuration:m.elapsed(now)});
  }
  void range(uint32_t from, uint32_t to, float kg) { for(uint32_t t=from;t<=to;t+=100) sample(t,kg); }
  void boot() { range(0,3000,0); assert(m.available && !m.occupied); }
  void occupy() { range(3100,5600,20); assert(m.occupied); assert(events.size()==1); assert(events[0].at==5300); }
};
int main() {
  for(int repetition=0;repetition<5;++repetition) {
    { Rig r; r.boot();r.range(3100,30000,0);assert(r.events.empty()); }
    { Rig r; r.boot();r.occupy();r.range(5700,15000,7);assert(r.m.occupied && r.events.size()==1); }
    { Rig r; r.boot();r.occupy();r.range(5700,8700,0);r.range(8800,12000,20);assert(r.m.occupied && r.events.size()==1); }
    { Rig r; r.boot();r.occupy();r.range(5700,125300,20);
      assert(r.events.size()==3);assert(r.events[1].kind==Monitor::REMINDER);
      assert(r.events[1].at==65300 && r.events[1].duration==60000);
      assert(r.events[2].at==125300);assert(r.m.alert); }
    { Rig r; r.boot();r.occupy();r.range(5700,17000,0);
      assert(!r.m.occupied && !r.m.alert);assert(r.events.size()==2);assert(r.events[1].kind==Monitor::END);
      assert(r.events[1].at==16000);assert(r.events[1].duration==10700);
      r.range(17100,20000,20);assert(r.events.size()==3 && r.events.back().kind==Monitor::START); }
    { Rig r; r.boot();r.occupy();r.m.step(8001,false);assert(!r.m.available && !r.m.occupied);
      r.range(8100,12000,20);assert(!r.m.available);r.range(12100,15000,0);assert(r.m.available);
      assert(!r.m.occupied && !r.m.alert); }
    { Monitor m;uint32_t base=0xfffff000;
      for(uint32_t i=0;i<=3000;i+=100) m.step(base+i,true,0);
      for(uint32_t i=3100;i<=5600;i+=100) m.step(base+i,true,20);
      assert(m.available && m.occupied && m.elapsed(base+5600)==300); }
    { Monitor m; m.step(0,true,NAN);assert(!m.available); }
  }
  puts("40 cenarios nativos aprovados (8 casos x 5 repeticoes). Nao sao ensaios Wokwi/hardware.");
}
