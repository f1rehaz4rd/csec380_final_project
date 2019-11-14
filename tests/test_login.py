import pytest
import requests

def test_server():
    values={'username': 'admin', 'password': 'admin'}
    assert requests.post("http://localhost", data=values)
