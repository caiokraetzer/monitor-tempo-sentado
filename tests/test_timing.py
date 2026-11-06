import unittest,subprocess,tempfile,json,sys
from pathlib import Path
SCRIPT=Path(__file__).resolve().parents[1]/'scripts/analisar_tempos.py'
def fixture():
 rows=[]
 for id,d in [(1001,100000),(1002,4000000)]:
  rows += [
   {'kind':'tx','host_us':d+950000,'topic':'ensaio/sync_req','payload':{'id':id}},
   {'kind':'rx','host_us':d+1050000,'topic':'ensaio/sync','payload':{'id':id,'d1_us':d,'d2_us':d}}]
 for id,d in enumerate([300000,600000,900000,1200000],1):
  rows.append({'kind':'rx','utc':'2026-11-05T23:00:00Z','host_us':d+1250000,'topic':'ensaio/sensor','payload':{'id':id,'detected_us':d,'load_kg':20}})
 for id,d in enumerate([400000,700000,1000000,1300000],1):
  rows += [
   {'kind':'tx','host_us':d+600000,'topic':'ensaio/comando','payload':{'id':id}},
   {'kind':'rx','utc':'2026-11-05T23:00:00Z','host_us':d+1300000,'topic':'ensaio/atuador','payload':{'id':id,'received_us':d-10000,'action_us':d,'gpio':23,'level':1}}]
 return rows
class TimingTests(unittest.TestCase):
 def execute(self,rows):
  with tempfile.TemporaryDirectory(prefix='timing-unit-') as folder:
   p=Path(folder);(p/'mensagens.jsonl').write_text('\n'.join(json.dumps(r) for r in rows),encoding='utf8')
   result=subprocess.run([sys.executable,str(SCRIPT),str(p)],capture_output=True,text=True)
   data=json.loads((p/'analise-tempos.json').read_text(encoding='utf8')) if result.returncode==0 else None
   return result,data
 def test_clock_offset_and_one_way_delays(self):
  result,data=self.execute(fixture());self.assertEqual(result.returncode,0,result.stderr)
  self.assertAlmostEqual(data['resumo']['Sensor HX711']['media_ms'],250)
  self.assertAlmostEqual(data['resumo']['Buzzer GPIO23']['media_ms'],400)
  for r in data['medidas']:
   self.assertAlmostEqual(r['incerteza_relogio_ms'],50)
   if r['componente']=='Buzzer GPIO23':self.assertAlmostEqual(r['processamento_local_ms'],10)
 def test_requires_clock_bracketing(self):
  result,_=self.execute([r for r in fixture() if r['payload'].get('id')!=1002])
  self.assertNotEqual(result.returncode,0);self.assertIn('Faltam sondas',result.stderr)
 def test_requires_four_sensor_observations(self):
  result,_=self.execute([r for r in fixture() if not (r.get('topic','').endswith('/sensor') and r['payload']['id']==4)])
  self.assertNotEqual(result.returncode,0);self.assertIn('esperado 4',result.stderr)
 def test_requires_gpio_feedback(self):
  rows=fixture()
  for r in rows:
   if r.get('topic','').endswith('/atuador'):r['payload']['level']=0
  result,_=self.execute(rows);self.assertNotEqual(result.returncode,0);self.assertIn('GPIO sem',result.stderr)
if __name__=='__main__':unittest.main()
