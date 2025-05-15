import pytest

def test_protected_route_requires_login(client):
    resp = client.get('/account/profile', follow_redirects=True)
    assert b'login' in resp.data or resp.status_code == 401 or resp.status_code == 302 