const fs=require('node:fs'),path=require('node:path');
const root=path.resolve(__dirname,'..');
const func=fs.readFileSync(path.join(root,'node-red/process-message.js'),'utf8').replace(/if \(typeof module[^\n]+/,'')+'\nreturn processMessage(msg, context);';
const flow=[
 {id:'chair-flow',type:'tab',label:'Monitor tempo sentado',disabled:false,info:'MQTT remoto, validação, painel e gravação JSONL.'},
 {id:'chair-broker',type:'mqtt-broker',name:'HiveMQ público',broker:'broker.hivemq.com',port:'1883',clientid:'',autoConnect:true,usetls:false,protocolVersion:'4',keepalive:'15',cleansession:true,autoUnsubscribe:true},
 {id:'chair-input',type:'mqtt in',z:'chair-flow',name:'Telemetria, eventos e status',topic:'mack/ods3/7c92a1/cadeira01/+',qos:'0',datatype:'utf8',broker:'chair-broker',nl:false,rap:true,rh:0,x:190,y:100,wires:[['chair-process']]},
 {id:'chair-tick',type:'inject',z:'chair-flow',name:'Verificar atualização (1 s)',props:[{p:'topic',vt:'str'},{p:'payload'}],topic:'__tick',payload:'',payloadType:'str',repeat:'1',once:true,onceDelay:0.5,x:180,y:180,wires:[['chair-process']]},
 {id:'chair-process',type:'function',z:'chair-flow',name:'Validar e acompanhar',func,outputs:2,noerr:0,initialize:'',finalize:'',libs:[],x:450,y:100,wires:[['chair-dashboard'],['chair-file']]},
 {id:'chair-file',type:'file',z:'chair-flow',name:'Mensagens recebidas (JSONL)',filename:'data/mqtt.jsonl',filenameType:'str',appendNewline:true,createDir:true,overwriteFile:'false',encoding:'utf8',x:750,y:180,wires:[[]]},
 {id:'chair-base',type:'ui-base',name:'Monitor IoT',path:'/dashboard',includeClientData:true,acceptsClientConfig:['ui-notification','ui-control'],showPathInSidebar:false,navigationStyle:'default',titleBarStyle:'default',showReconnectNotification:true,notificationDisplayTime:5,showDisconnectNotification:true,allowInstall:false},
 {id:'chair-theme',type:'ui-theme',name:'Monitor',colors:{surface:'#ffffff',primary:'#087f8c',bgPage:'#edf3f6',groupBg:'#ffffff',groupOutline:'#d5e0e5'},sizes:{density:'default',pagePadding:'12px',groupGap:'12px',groupBorderRadius:'8px',widgetGap:'12px'}},
 {id:'chair-page',type:'ui-page',name:'Tempo sentado',ui:'chair-base',path:'/cadeira',icon:'chair',layout:'grid',theme:'chair-theme',breakpoints:[{name:'Default',px:'0',cols:'3'},{name:'Tablet',px:'576',cols:'6'},{name:'Desktop',px:'1024',cols:'12'}],order:1,className:'',visible:true,disabled:false},
 {id:'chair-group',type:'ui-group',name:'Monitoramento',page:'chair-page',width:'12',height:'1',order:1,showTitle:false,className:'',visible:'true',disabled:'false',groupType:'default'},
 {id:'chair-dashboard',type:'ui-template',z:'chair-flow',group:'chair-group',name:'Assento e eventos',order:1,width:'12',height:'0',format:fs.readFileSync(path.join(root,'node-red/dashboard.vue'),'utf8'),storeOutMessages:true,passthru:false,resendOnRefresh:true,templateScope:'local',className:'',x:760,y:80,wires:[[]]},
 {id:'chair-catch',type:'catch',z:'chair-flow',name:'Erros de processamento/gravação',scope:null,uncaught:false,x:220,y:270,wires:[['chair-debug']]},
 {id:'chair-debug',type:'debug',z:'chair-flow',name:'Falhas do fluxo',active:true,tosidebar:true,console:false,tostatus:false,complete:'true',targetType:'full',x:490,y:270,wires:[]}
];
fs.writeFileSync(path.join(root,'node-red/flows.json'),JSON.stringify(flow,null,2)+'\n');
fs.copyFileSync(path.join(root,'firmware/ChairMonitor/diagram.json'),path.join(root,'diagram.json'));
console.log('flows.json e diagrama da raiz atualizados.');
