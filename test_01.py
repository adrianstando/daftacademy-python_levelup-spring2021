from fastapi.testclient import TestClient
from datetime import date, timedelta

from main import app

client = TestClient(app)

tab = [{"name": "A", "surname": "B"}, {"name": "C", "surname": "D"}]


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello world!"}


def test_method_main():
    response = client.get("/method")
    assert response.status_code == 200
    assert response.json() == {"method": "GET"}

    response = client.post("/method")
    assert response.status_code == 201
    assert response.json() == {"method": "POST"}

    response = client.delete("/method")
    assert response.status_code == 200
    assert response.json() == {"method": "DELETE"}

    response = client.put("/method")
    assert response.status_code == 200
    assert response.json() == {"method": "PUT"}

    response = client.options("/method")
    assert response.status_code == 200
    assert response.json() == {"method": "OPTIONS"}


def test_password():
    response1 = client.get(
        "/auth?password=haslo&password_hash=013c6889f799cd986a735118e1888727d1435f7f623d05d58c61bf2cd8b49ac90105e5786ceaabd62bbc27336153d0d316b2d13b36804080c44aa6198c533215")
    assert response1.status_code == 204

    response2 = client.get(
        "/auth?password=haslo&password_hash=f34ad4b3ae1e2cf33092e2abb60dc0444781c15d0e2e9ecdb37e4b14176a0164027b05900e09fa0f61a1882e0b89fbfa5dcfcc9765dd2ca4377e2c794837e091")
    assert response2.status_code == 401


def test_password_empty():
    response2 = client.get(
        "/auth?password=&password_hash=")
    assert response2.status_code == 401


def test_register():
    d = date.today().strftime("%Y-/%m-/%d")
    i = 1

    for elem in tab:
        response = client.post("/register", json=elem)
        assert response.status_code == 201

        d_vac = (date.today() + timedelta(days=len(elem.get('name')) + len(elem.get('surname')))).strftime("%Y-/%m-/%d")
        assert response.json() == {'id': i,
                                   'name': elem.get('name'),
                                   'surname': elem.get('surname'),
                                   'register_date': d,
                                   'vaccination_date': d_vac}

        i += 1


def get_patient():
    i = 1
    d = date.today().strftime("%Y-/%m-/%d")

    for elem in tab:
        response = client.get("/patient/" + str(i))
        assert response.status_code == 200

        d_vac = (date.today() + timedelta(days=len(elem.get('name')) + len(elem.get('surname')))).strftime("%Y-/%m-/%d")
        assert response.json() == {'id': i,
                                   'name': elem.get('name'),
                                   'surname': elem.get('surname'),
                                   'register_date': d,
                                   'vaccination_date': d_vac}

        i += 1

    response = client.get("/patient" + str(i + 10))
    assert response.status_code == 404

    response = client.get("/patient/0")
    assert response.status_code == 400
