import pytest
import requests

def getContent(url):
    return str(requests.get(url).content)

def test_server():
    assert "Hello World" in getContent("http://localhost")
