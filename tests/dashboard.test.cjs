const {test}=require('node:test');
const assert=require('node:assert/strict');
const {processMessage}=require('../node-red/process-message');
const prefix='mack/ods3/7c92a1/cadeira01/';
function ctx(){const m=new Map();return {get:k=>m.get(k),set:(k,v)=>m.set(k,v)};}
const occupied={estado:'ocupado',ocupado:true,tempo_s:60,alerta:true,uptime_ms:68000};
test('telemetria válida, relógio de recebimento e desatualização',()=>{
 const c=ctx();let r=processMessage({topic:prefix+'telemetria',payload:JSON.stringify(occupied)},c,1000);
 assert.equal(r[0].payload.stale,false);assert.equal(r[0].payload.telemetry.tempo_s,60);
 assert.equal(JSON.parse(r[1].payload).recebido_em,'1970-01-01T00:00:01.000Z');
 assert.equal(processMessage({topic:'__tick'},c,16001)[0].payload.stale,true);
});
test('rejeita JSON inválido, tópico estranho, campos e estados incoerentes',()=>{
 for(const payload of ['{',null,[],{...occupied,tempo_s:-1},{...occupied,tempo_s:NaN},{...occupied,uptime_ms:1.5},{...occupied,ocupado:false},{...occupied,estado:'livre'}])
   assert.equal(processMessage({topic:prefix+'telemetria',payload},ctx(),0),null);
 assert.equal(processMessage({topic:'outro/telemetria',payload:occupied},ctx(),0),null);
});
test('indisponível distingue falha de assento livre',()=>{
 const c=ctx();const r=processMessage({topic:prefix+'telemetria',payload:{estado:'indisponivel',ocupado:null,tempo_s:0,alerta:false,uptime_ms:2}},c,0);
 assert.equal(r[0].payload.telemetry.ocupado,null);
});
test('eventos, limite de memória e status',()=>{
 const c=ctx();for(let i=0;i<205;i++) processMessage({topic:prefix+'evento',payload:{tipo:'inicio',tempo_s:0,uptime_ms:i}},c,i);
 const r=processMessage({topic:prefix+'status',payload:'offline'},c,300);
 assert.equal(r[0].payload.events.length,200);assert.equal(r[0].payload.status,'offline');
 assert.equal(processMessage({topic:prefix+'evento',payload:{tipo:'invalido',tempo_s:0,uptime_ms:1}},c,0),null);
});
test('reinício limpa gráfico sem fabricar eventos',()=>{
 const c=ctx();processMessage({topic:prefix+'telemetria',payload:occupied},c,1000);
 let r=processMessage({topic:prefix+'telemetria',payload:{...occupied,uptime_ms:3}},c,2000);
 assert.equal(r[0].payload.history.length,1);assert.equal(r[0].payload.events.length,0);
});
