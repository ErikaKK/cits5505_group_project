import unittest

class TestUI(unittest.TestCase):
    def setUp(self):
        from app import create_app
        self.app = create_app({'TESTING': True, 'WTF_CSRF_ENABLED': False})
        self.client = self.app.test_client()

    def test_homepage_ui(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b'Welcome to SpotifyDash', resp.data)
        self.assertIn(b'Spotify listening habits', resp.data)

if __name__ == "__main__":
    unittest.main() 