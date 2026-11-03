#pragma once
#include <stdint.h>
#include <math.h>

// Lógica independente do Arduino: também utilizada nos testes nativos.
class Monitor {
public:
  enum Event { NONE, START, END, REMINDER };
  bool available = false, occupied = false, alert = false;
  float load = 0;
  uint32_t started = 0;
  explicit Monitor(uint32_t reminder = 60000) : reminderMs(reminder) {}
  const char* state() const { return !available ? "indisponivel" : occupied ? "ocupado" : "livre"; }
  uint32_t elapsed(uint32_t now) const { return available && occupied ? uint32_t(now-started) : 0; }
  Event step(uint32_t now, bool hasSample, float kg = 0) {
    if (hasSample && isfinite(kg)) {
      lastSample = now; seen = true;
      values[index] = kg; index = (index+1)%5; if (count<5) ++count;
      float sum=0; for (uint8_t i=0;i<count;++i) sum+=values[i]; load=sum/count;
    }
    if (!seen || uint32_t(now-lastSample)>2000) {
      available=false; occupied=false; alert=false; entering=false; leaving=false;
      emptyPending=false; count=0; index=0; return NONE;
    }
    // Após inicialização/falha, somente cinco leituras e assento vazio por 2 s rearmam.
    if (!available) {
      if (count==5 && load<=5) {
        if (!emptyPending) { emptyPending=true; emptySince=now; }
        if (uint32_t(now-emptySince)>=2000) { available=true; emptyPending=false; }
      } else emptyPending=false;
      return NONE;
    }
    if (!occupied) {
      if (load>=10) {
        if (!entering) { entering=true; enteredAt=now; }
        if (uint32_t(now-enteredAt)>=2000) {
          occupied=true; alert=false; entering=false; started=now; lastReminder=now; return START;
        }
      } else entering=false;
      return NONE;
    }
    if (load<=5) {
      if (!leaving) { leaving=true; leftAt=now; }
      if (uint32_t(now-leftAt)>=10000) {
        // elapsed() ainda pode ser lido pelo chamador ANTES deste step.
        endedDuration=uint32_t(now-started); occupied=false; alert=false; leaving=false; return END;
      }
    } else leaving=false;
    if ((!alert && uint32_t(now-started)>=reminderMs) ||
        (alert && uint32_t(now-lastReminder)>=60000)) {
      alert=true; lastReminder=now; return REMINDER;
    }
    return NONE;
  }
  uint32_t endedDuration = 0;
private:
  uint32_t reminderMs, lastSample=0, enteredAt=0, leftAt=0, emptySince=0, lastReminder=0;
  bool seen=false, entering=false, leaving=false, emptyPending=false;
  float values[5] = {0}; uint8_t count=0,index=0;
};
