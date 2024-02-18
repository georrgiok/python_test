from fastapi.testclient import TestClient

from app import main

app = main.app

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200


def test_name():
    response = client.get('/hello/Tester')
    assert response.status_code == 200
    assert response.json() == {"message": f"Hello Tester"}
