import requests

url = "http://127.0.0.1:5000/user/add"
myobj = {
    "id" : "123456",
    "name" : "Usuario prueba"
}


r = requests.post(url, json = myobj)
print(r.text)