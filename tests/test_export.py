import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location('export_csv', Path(__file__).parents[1] / 'scripts/export_csv.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

class ExportTest(unittest.TestCase):
    def test_received_data_and_no_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            source, target = Path(tmp)/'in.jsonl', Path(tmp)/'out.csv'
            records = [
                {'recebido_em':'2026-11-03T00:00:00Z','topic':'x/status','payload':'online'},
                {'recebido_em':'2026-11-03T00:00:01Z','topic':'x/evento','payload':{'tipo':'fim','tempo_s':72.3,'uptime_ms':80000}}
            ]
            source.write_text('\n'.join(map(json.dumps, records)), encoding='utf-8')
            self.assertEqual(module.convert(source, target), 2)
            self.assertIn('72.3', target.read_text())
            with self.assertRaises(FileExistsError):
                module.convert(source, target)

    def test_bad_line_fails_explicitly(self):
        with tempfile.TemporaryDirectory() as tmp:
            source, target = Path(tmp)/'in.jsonl', Path(tmp)/'out.csv'
            source.write_text('{', encoding='utf-8')
            with self.assertRaisesRegex(ValueError, 'Linha 1'):
                module.convert(source, target)

if __name__ == '__main__':
    unittest.main()
