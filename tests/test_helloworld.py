import pytest
import requests

def getContent(url):
    return str(requests.get(url).content)

assert "Hello World" in getContent("http://localhost")