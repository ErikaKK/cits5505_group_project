import unittest

class TestSecurity(unittest.TestCase):
    def setUp(self):
        from app import create_app
        self.app = create_app({'TESTING': True, 'WTF_CSRF_ENABLED': False})
        self.client = self.app.test_client()

    def test_protected_route_requires_login(self):
        resp = self.client.get('/account/profile', follow_redirects=True)
        self.assertTrue(b'login' in resp.data or resp.status_code == 401 or resp.status_code == 302)

if __name__ == "__main__":
    unittest.main() 