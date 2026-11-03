// Esta função é incorporada ao fluxo por scripts/build-flow.cjs e testada sem Node-RED.
function processMessage(msg, context, now = Date.now()) {
  const prefix = 'mack/ods3/7c92a1/cadeira01/';
  let s = context.get('chair') || {telemetry:null, lastReceived:null, status:'desconhecido', events:[], history:[]};
  let record = null;
  if (msg.topic !== '__tick') {
    if (typeof msg.topic !== 'string' || !msg.topic.startsWith(prefix)) return null;
    const kind = msg.topic.slice(prefix.length);
    let p = msg.payload;
    if (kind === 'status') {
      if (p !== 'online' && p !== 'offline') return null;
      s.status = p;
    } else {
      if (typeof p === 'string') { try { p = JSON.parse(p); } catch { return null; } }
      if (!p || typeof p !== 'object' || Array.isArray(p)) return null;
      if (!Number.isFinite(p.tempo_s) || p.tempo_s < 0 ||
          !Number.isInteger(p.uptime_ms) || p.uptime_ms < 0 || p.uptime_ms > 4294967295) return null;
      if (kind === 'telemetria') {
        if (!['livre','ocupado','indisponivel'].includes(p.estado) || typeof p.alerta !== 'boolean') return null;
        if ((p.estado === 'indisponivel' && (p.ocupado !== null || p.alerta || p.tempo_s !== 0)) ||
            (p.estado === 'livre' && (p.ocupado !== false || p.alerta || p.tempo_s !== 0)) ||
            (p.estado === 'ocupado' && p.ocupado !== true)) return null;
        if (s.telemetry && p.uptime_ms < s.telemetry.uptime_ms) s.history = [];
        s.telemetry = p; s.lastReceived = now;
        s.history.push({x:now, y:p.tempo_s}); s.history = s.history.slice(-180);
      } else if (kind === 'evento') {
        if (!['inicio','fim','lembrete'].includes(p.tipo)) return null;
        s.events.push({tipo:p.tipo, tempo_s:p.tempo_s, uptime_ms:p.uptime_ms, recebido_em:new Date(now).toISOString()}); s.events = s.events.slice(-200);
      } else return null;
    }
    record = {payload:JSON.stringify({recebido_em:new Date(now).toISOString(), topic:msg.topic, payload:p})};
  }
  context.set('chair', s);
  return [{payload:{...s, stale:s.lastReceived === null || now-s.lastReceived>15000, now}}, record];
}
if (typeof module !== 'undefined') module.exports = {processMessage};
