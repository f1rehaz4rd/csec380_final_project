import pytest
import requests

def getStatus(url):
    return requests.get(url).status_code

def test_server():
    assert 200 == getStatus("http://localhost")
