import json
import time
import unittest

from main import app


class EndToEndTest(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        self.app = app.test_client()

        self.assertEqual(app.debug, False)

    def test_example03(self):
        response = self.app.get("/run/Example03?inputs={'app3.in': 'app3.in', 'application3': './application3'}", follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_example04(self):
        response = self.app.get('/run/Example04?inputs={}', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_example03_post(self):
        response = self.app.post('/run/Example03', data="{'app3.in': 'app3.in', 'application3': './application3'}", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        exec_id = self.extract_execution_id_from_response(response)
        time.sleep(12)
        outputs = self.app.get('/info/' + exec_id, follow_redirects=True)
        outputs_json = json.loads(outputs.data.decode())
        expected_outputs_json = json.loads('{"app3.out": "app3.out", "log": "mupif.log"}\n')
        self.assertEqual(outputs_json, expected_outputs_json)

    def test_example04_post(self):
        response = self.app.post('/run/Example04', data="{}", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        exec_id = self.extract_execution_id_from_response(response)
        time.sleep(12)
        outputs = self.app.get('/info/' + exec_id, follow_redirects=True)
        outputs_json = json.loads(outputs.data.decode())
        expected_outputs_json = json.loads('{"example1": "example1.vtk", "mesh": "mesh.dat", "log": "mupif.log", "example2": "example2.vtk","field": "field.dat" }\n')
        self.assertEqual(outputs_json, expected_outputs_json)

    def test_example05_post(self):
        response = self.app.post('/run/Example05', data="{}", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        exec_id = self.extract_execution_id_from_response(response)
        time.sleep(12)
        outputs = self.app.get('/info/' + exec_id, follow_redirects=True)
        self.assertEqual(outputs.data.decode(), '{}\n')

    def extract_execution_id_from_response(self, response):
        exec_id = response.data.decode()
        prefix = 'Execution id = '
        suffix = '\n'
        if exec_id.startswith(prefix):
            exec_id = exec_id[len(prefix):]
        if exec_id.endswith(suffix):
            exec_id = exec_id[:-len(suffix)]
        return exec_id


if __name__ == '__main__':
    unittest.main()
