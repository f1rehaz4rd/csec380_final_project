import pytest
import requests

def test_server():
    values={'username': 'WRONGUSER', 'password': 'admin'}
    assert requests.post("http://localhost/login", data=values)
