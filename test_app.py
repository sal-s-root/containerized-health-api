import json
import threading
import unittest
import urllib.error
import urllib.request
from http.server import ThreadingHTTPServer
from app import Handler

class API(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        cls.worker = threading.Thread(target=cls.server.serve_forever)
        cls.worker.start()
        cls.base = "http://127.0.0.1:" + str(cls.server.server_port)
    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.worker.join()
    def test_health(self):
        with urllib.request.urlopen(self.base + "/healthz", timeout=2) as response:
            self.assertEqual(response.status, 200)
            self.assertEqual(json.load(response), {"status": "ok"})
    def test_version(self):
        from unittest.mock import patch
        with patch.dict("os.environ", {"APP_VERSION": "1.2.3"}):
            with urllib.request.urlopen(self.base + "/version", timeout=2) as response:
                self.assertEqual(json.load(response), {"version": "1.2.3"})
    def test_readiness(self):
        with urllib.request.urlopen(self.base + "/readyz", timeout=2) as response:
            self.assertEqual(json.load(response), {"status": "ok"})
    def test_metrics(self):
        with urllib.request.urlopen(self.base + "/metrics", timeout=2) as response:
            text=response.read().decode()
            self.assertIn("# TYPE demo_http_requests_total counter",text)
            self.assertIn('route="/metrics"',text)
    def test_missing_route(self):
        with self.assertRaises(urllib.error.HTTPError) as caught:
            urllib.request.urlopen(self.base + "/missing", timeout=2)
        self.assertEqual(caught.exception.code, 404)
        caught.exception.close()

if __name__ == "__main__":
    unittest.main()
