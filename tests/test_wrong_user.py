import requests

url="http://localhost/login"
vals={'username': 'USER', 'password': 'admin'}

r=requests.post(url, data=vals)
print(b"Welcome admin!!!" in r.content)
