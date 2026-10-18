import json
import threading
import unittest
import urllib.error
import urllib.request
from http.server import HTTPServer

from app.main import Handler


class HealthTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = HTTPServer(("127.0.0.1", 0), Handler)
        cls.port = cls.server.server_address[1]
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()

    def test_healthz_returns_ok(self):
        url = f"http://127.0.0.1:{self.port}/healthz"
        with urllib.request.urlopen(url) as resp:
            self.assertEqual(resp.status, 200)
            self.assertEqual(json.load(resp), {"status": "ok"})

    def test_unknown_path_returns_404(self):
        url = f"http://127.0.0.1:{self.port}/nope"
        with self.assertRaises(urllib.error.HTTPError) as ctx:
            urllib.request.urlopen(url)
        self.assertEqual(ctx.exception.code, 404)


if __name__ == "__main__":
    unittest.main()
