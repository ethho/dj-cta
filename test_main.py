from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_hello():
    response = client.get("/hello")
    assert response.status_code == 200
    # assert response.json() == {"msg": "Hello World"}

def test_song_request():
	response = client.get("/", params={'stopid': '12345'})
	assert response.status_code == 200
	assert response.json() == {"stopid": 12345}, response.json()


def test_spt_token():
    response = client.get("/spt_auth/token")
    assert response.status_code == 200
    # assert response.json() == {"msg": "Hello World"}
