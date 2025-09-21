import requests
url = "http://192.168.10.32"
path = "/add"
s = url+path

body = {"name":"Dongyeog"}

response = requests.post(s, json=body)
print(response.text)