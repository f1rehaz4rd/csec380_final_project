import pytest
import requests

def test_server():
    values={'username': 'admin', 'password': 'WRONGPASS'}
    assert requests.post("http://localhost/login", data=values)
