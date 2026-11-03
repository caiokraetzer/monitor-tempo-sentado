const fs=require('node:fs'),assert=require('node:assert/strict'),vm=require('node:vm');
const flow=JSON.parse(fs.readFileSync('node-red/flows.json','utf8'));
const ids=new Set(flow.map(n=>n.id));assert.equal(ids.size,flow.length);
for(const n of flow){for(const group of n.wires||[])for(const id of group)assert(ids.has(id),`Ligação ausente: ${id}`);if(n.type==='function')new Function('msg','context',n.func);}
const embedded=flow.find(n=>n.type==='function').func;
const source=fs.readFileSync('node-red/process-message.js','utf8').replace(/if \(typeof module[^\n]+/,'');
assert(embedded.startsWith(source),'Fluxo precisa ser regenerado');
for(const file of ['diagram.json','firmware/ChairMonitor/diagram.json','node-red/package.json'])JSON.parse(fs.readFileSync(file));
assert.equal(fs.readFileSync('diagram.json','utf8'),fs.readFileSync('firmware/ChairMonitor/diagram.json','utf8'));
console.log('JSON, ligações do fluxo e sincronização de fontes verificados.');
