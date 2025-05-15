import pytest

def test_homepage_ui(client):
    resp = client.get('/')
    assert resp.status_code == 200
    assert b'Welcome to SpotifyDash' in resp.data
    assert b'Spotify listening habits' in resp.data 