import requests
import pytest

url="http://localhost/login"
vals={'username': 'admin', 'password': 'admin'}

def login():
    r=requests.post(url, data=vals)
    return b"Welcome admin!!!" in r.content

def test_wrong():
    assert login() == True