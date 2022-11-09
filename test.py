import requests

url = "http://127.0.0.1:5000/comentario/add"
# myobj = {
#     "nombre": "Chaza5",
#     "categorias": ["Vivero"],
#     "ubicacion": "Perola",
#     "descripcion": "",
#     "urlImagen": "urltest4.com",
#     "telefono": 13548,
#     "horario": "13:00 - 18:00",
#     "propietario": "idPropietario4" ,
#     "comentarios": ["com1"],
#     "calificacion": 4,
#     "urlFotoChaza": "urlFoto3",
#     "reportes": ["rep1"],
# }

myComment = {
    'usuario': 'idUsuario',
    'fecha': 'nov 10 2020',
    'estrellas': 'comentario1',
    'upvotes': '1',
    'chazaId': '23131'
}

r = requests.post(url, json = myComment)
print(r.text)

# r = requests.post(url, json = myobj)
# print(r.text)

# r = requests.post("http://127.0.0.1:5000/chaza/list")
# print(r.json())