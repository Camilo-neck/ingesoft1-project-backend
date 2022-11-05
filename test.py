import requests

# url = "http://127.0.0.1:5000/user/add"
# myobj = {
#     "id" : "987654",
#     "name" : "Usuario prueba 2"
# }

# r = requests.post(url, json = myobj)
# print(r.text)

r = requests.get("http://127.0.0.1:5000/user/list")
print(r.json())