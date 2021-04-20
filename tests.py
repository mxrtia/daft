from fastapi.testclient import TestClient

import pytest
import json
from datetime import date, datetime, timedelta
from main import app

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello world!"}


@pytest.mark.parametrize("name", ["Zenek", "Marek", "Alojzy Niezdąży"])
def test_hello_name(name):
    response = client.get(f"/hello/{name}")
    assert response.status_code == 200
    assert response.json() == {"msg": f"Hello {name}"}


def test_counter():
    response = client.get(f"/counter")
    assert response.status_code == 200
    assert response.text == "1"
    # 2nd Try
    response = client.get(f"/counter")
    assert response.status_code == 200
    assert response.text == "2"
    # 3rd Try
    response = client.get(f"/counter")
    assert response.status_code == 200
    assert response.text == "3"
    
 
def test_method_get():
    response = client.get("/method")
    assert response.status_code == 200
    assert response.json() == {"method": "GET"}


def test_auth():
    response = client.get(f"/auth?password=haslo&password_hash=013c6889f799cd986a735118e1888727d1435f7f623d05d58c61bf2cd8b49ac90105e5786ceaabd62bbc27336153d0d316b2d13b36804080c44aa6198c533215")
    assert response.status_code == 204
    response = client.get(f"/auth?password=haslo&password_hash=f34ad4b3ae1e2cf33092e2abb60dc0444781c15d0e2e9ecdb37e4b14176a0164027b05900e09fa0f61a1882e0b89fbfa5dcfcc9765dd2ca4377e2c794837e091")
    assert response.status_code == 401
    
 
def test_register():
    response = client.post("/register", json={"name": "1! żJan", "surname": "2% ąNowak"})
    assert response.status_code == 201
    today = date.today()
    todayplus8 = today+timedelta(len('żJan')+len('ąNowak'))
    today=today.strftime("%Y-%m-%d")
    todayplus8=todayplus8.strftime("%Y-%m-%d")
    assert response.json() == {'id': 1, 'name': '1! żJan', 'surname': '2% ąNowak', 'register_date': today, 'vaccination_date': todayplus8}
    
    
def test_getinfo():
    today = date.today()
    todayplus8 = today+timedelta(len('1! żJan')+len('2% ąNowak'))
    today=today.strftime("%Y-%m-%d")
    todayplus8=todayplus8.strftime("%Y-%m-%d")
    
    response = client.get("/patient/0")
    assert response.status_code == 400
    
    response = client.get("/patient/1")
    assert response.status_code == 200
    assert response.json() == {'id': 1, 'name': '1! żJan', 'surname': '2% ąNowak', 'register_date': today, 'vaccination_date': todayplus8}
    
    response = client.get("/patient/100")
    assert response.status_code == 404
    
    
    

    
    
