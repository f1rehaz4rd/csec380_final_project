import requests
import pytest

def uploadfile():
    """
    Upload Video File
    """
    logindata = {"username": "admin", "password": "admin"}
    titledata = {"title": "Upload Test"}
    filesdata = {"file": open('test.mp4','rb')}

    with requests.Session() as s:
        req = s.post("http://localhost/login", data=logindata, allow_redirects=True)
        upreq = s.post("http://localhost/uploadfile", files=filesdata, data=titledata, allow_redirects=True)
        check = s.get("http://localhost/home")
        return b"Upload Test" in check.content

def uploadlink():
    """
    Upload Video Link
    """
    logindata = {"username": "admin", "password": "admin"}
    linkdata = {"title": "Upload Test2", "videourl": "https://test-videos.co.uk/vids/bigbuckbunny/mp4/h264/1080/Big_Buck_Bunny_1080_10s_1MB.mp4"}

    with requests.Session() as s:
        req = s.post("http://localhost/login", data=logindata, allow_redirects=True)
        upreq = s.post("http://localhost/uploadlink", data=linkdata, allow_redirects=True)
        check = s.get("http://localhost/home")
        return b"Upload Test2" in check.content

def deletevideo():
    """
    Delete Video Test
    """
    logindata = {"username": "admin", "password": "admin"}
    deletedata = {"selected": "Upload Test", "submit_button": "delete"}
    deletedata2 = {"selected": "Upload Test2", "submit_button": "delete"}

    with requests.Session() as s:
        req = s.post("http://localhost/login", data=logindata, allow_redirects=True)
        # delreq = s.post("http://localhost/account/admin", data=deletedata, allow_redirects=True)
        delreq2 = s.post("http://localhost/account/admin", data=deletedata2, allow_redirects=True)

        check = s.get("http://localhost/home")

        if b"Upload Test" in check.content or b"Upload Test2" in check.content:
            return False
        else:
            return True

def test_uploading():
    # assert uploadfile() == True
    assert uploadlink() == True
    assert deletevideo() == True