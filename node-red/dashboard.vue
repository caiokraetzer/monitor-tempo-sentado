<template>
  <section class="chair-panel">
    <h2>Monitor de tempo sentado</h2>
    <p>ESP32 · HX711 · MQTT — demonstração acadêmica</p>
    <div class="chair-status" :class="{bad: !msg?.payload || msg.payload.stale || msg.payload.status === 'offline'}">
      {{ !msg?.payload || msg.payload.stale ? 'Dados desatualizados — aguardando telemetria' : msg.payload.status === 'offline' ? 'Dispositivo offline' : 'Recebendo dados' }}
    </div>
    <div class="chair-stats">
      <article><small>Estado do assento</small><strong>{{ msg?.payload?.telemetry?.estado || 'Aguardando' }}</strong></article>
      <article><small>Tempo do ciclo</small><strong>{{ msg?.payload?.telemetry?.tempo_s?.toFixed(1) ?? '—' }} s</strong></article>
      <article><small>Lembrete de pausa</small><strong>{{ msg?.payload?.telemetry?.alerta ? 'Ativo' : 'Inativo' }}</strong></article>
    </div>
    <p>Última telemetria recebida: {{ msg?.payload?.lastReceived ? new Date(msg.payload.lastReceived).toLocaleString('pt-BR') : '—' }} · Status MQTT: {{ msg?.payload?.status || 'desconhecido' }}</p>
    <h3>Duração do ciclo nas últimas amostras</h3>
    <svg viewBox="0 0 600 160" role="img" aria-label="Histórico do tempo sentado em segundos">
      <line x1="35" y1="140" x2="590" y2="140" stroke="#64748b"/>
      <line x1="35" y1="10" x2="35" y2="140" stroke="#64748b"/>
      <text x="0" y="14" font-size="11">{{ maxY.toFixed(0) }} s</text><text x="15" y="142" font-size="11">0</text>
      <polyline :points="points" fill="none" stroke="#087f8c" stroke-width="3"/>
      <text x="35" y="157" font-size="10">{{ firstTime }}</text><text x="500" y="157" font-size="10">{{ lastTime }}</text>
    </svg>
    <h3>Eventos recebidos</h3>
    <button @click="downloadCsv">Exportar eventos para CSV</button>
    <table><thead><tr><th>Recebimento</th><th>Evento</th><th>Tempo (s)</th><th>Uptime (ms)</th></tr></thead>
      <tbody><tr v-for="(e,i) in rows" :key="i"><td>{{e.recebido_em}}</td><td>{{e.tipo}}</td><td>{{e.tempo_s}}</td><td>{{e.uptime_ms}}</td></tr></tbody>
    </table>
    <p>O painel mantém até 200 eventos e 180 amostras. O arquivo JSONL do Node-RED preserva as mensagens válidas recebidas. Dados simulados não demonstram benefícios clínicos.</p>
  </section>
</template>
<script>
export default {
  computed: {
    rows() { return [...(this.msg?.payload?.events || [])].reverse(); },
    history() { return this.msg?.payload?.history || []; },
    maxY() { return Math.max(1,...this.history.map(p=>p.y)); },
    points() { const h=this.history; const min=h[0]?.x||0; const span=Math.max(1,(h[h.length-1]?.x||0)-min); return h.map(p=>`${35+555*(p.x-min)/span},${140-125*p.y/this.maxY}`).join(' '); },
    firstTime() { return this.history.length ? new Date(this.history[0].x).toLocaleTimeString('pt-BR') : ''; },
    lastTime() { return this.history.length ? new Date(this.history[this.history.length-1].x).toLocaleTimeString('pt-BR') : ''; }
  },
  methods: {
    downloadCsv() {
      const rows=this.msg?.payload?.events||[];
      const csv='recebido_em,tipo,tempo_s,uptime_ms\n'+rows.map(e=>[e.recebido_em,e.tipo,e.tempo_s,e.uptime_ms].join(',')).join('\n');
      const url=URL.createObjectURL(new Blob(['\uFEFF'+csv],{type:'text/csv;charset=utf-8'}));
      const a=document.createElement('a'); a.href=url; a.download='eventos-mqtt.csv'; a.click(); URL.revokeObjectURL(url);
    }
  }
}
</script>
<style>
.chair-panel{font-family:system-ui;color:#172b3a;padding:16px}.chair-panel h2{margin-bottom:0}.chair-status{padding:12px;background:#d8f3e6;border-radius:8px}.chair-status.bad{background:#fff0cd}.chair-stats{display:flex;gap:12px;flex-wrap:wrap;margin-top:18px}.chair-stats article{flex:1;min-width:145px;padding:16px;background:#eef5f7;border-radius:8px}.chair-stats small,.chair-stats strong{display:block}.chair-stats strong{font-size:22px;margin-top:8px}.chair-panel table{border-collapse:collapse;width:100%;font-size:12px}.chair-panel td,.chair-panel th{padding:7px;text-align:left;border-bottom:1px solid #ddd}.chair-panel button{background:#087f8c;color:white;border:0;border-radius:6px;padding:10px 16px;margin-bottom:12px;cursor:pointer}.chair-panel svg{width:100%;max-height:220px}
</style>
