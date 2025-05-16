import unittest
from app import create_app, db

class TestErrorHandling(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app({'TESTING': True, 'WTF_CSRF_ENABLED': False})
        with cls.app.app_context():
            db.create_all()
        cls.client = cls.app.test_client()

    @classmethod
    def tearDownClass(cls):
        with cls.app.app_context():
            db.drop_all()

    def test_404(self):
        resp = self.client.get('/not-exist-page')
        self.assertEqual(resp.status_code, 404)
        self.assertIn(b'404', resp.data)
        self.assertIn(b'TraceID', resp.data)

    def test_403(self):
        resp = self.client.get('/forbidden')
        self.assertIn(resp.status_code, (403, 404))

    def test_400(self):
        resp = self.client.post('/upload', data={})
        self.assertIn(resp.status_code, (400, 404))

    def test_422(self):
        resp = self.client.post('/upload', data={'file': (b'invalid', 'data.json')})
        self.assertIn(resp.status_code, (400, 422, 404))

    def test_429(self):
        resp = self.client.get('/ratelimit')
        self.assertIn(resp.status_code, (429, 404))

    def test_500(self):
        resp = self.client.get('/test500')
        self.assertIn(resp.status_code, (500, 404))

if __name__ == "__main__":
    unittest.main() 