import requests

# url = "http://127.0.0.1:5000/usuario/edit/f42c3a0c77b74c32ba4c215c4178dea4"
# myobj = {
#     "nombre": "TESTEO USUARIO2",
#     "tipoUsuario": "Estudiante",
#     "urlFotoPerfil": "urltest2.com",
#     "correo": "prueba3@gmail.com",
#     "password": "1234567"
# }
# r = requests.post(url, json = myobj)

# r = requests.get("http://127.0.0.1:5000/usuario/list")
# print(r.text)


# url = "http://127.0.0.1:5000/usuario/add"
# myobj = {
#     "nombre": "TESTEO USUARIO2",
#     "tipoUsuario": "Estudiante",
#     "urlFotoPerfil": "urltest2.com",
#     "correo": "prueba2@gmail.com",
#     "password": "1234567"
# }
# r = requests.post(url, json = myobj)

# r = requests.get("http://127.0.0.1:5000/usuario/")
# print(r.text)



# url = "http://127.0.0.1:5000/chaza/add"
# myobj = {
#     "nombre": "TESTEO CHAZA",
#     "categorias": ["Vivero"],
#     "ubicacion": "Plaza Che",
#     "descripcion": "",
#     "urlImagen": "urltest4.com",
#     "telefono": 117513,
#     "horario": "13:00 - 18:00",
#     "propietario": "idPropietario9" ,
#     "comentarios": ["com1"],
#     "calificacion": 4,
#     "urlFotoChaza": "urlFoto3",
#     "reportes": ["rep1"],
# }

# r = requests.post(url, json = myobj)
# print(r.text)
# r = requests.get("http://127.0.0.1:5000/chaza/")
# print(r.text)

# def createComment():
#     ''' Create new comment in database with dummy data'''
    # JSON object to be added
    # newComment = {
    #     "usuario": "idUsuario",
    #     "fecha": "feb 14 2022",
    #     "estrellas": "5",
    #     "upvotes": "23",
    #     "chazaId": "2c3318cdb84148eba49b9239b7ed6102"
    # }

#     # Flask view URL
#     url = "http://localhost:5000/comentario/add"

#     # JSON object to be added
#     newComment = {
#         "usuario": "idUsuario",
#         "fecha": "nov 10 2020",
#         "estrellas": "3",
#         "upvotes": "1",
#         "chazaId": "23131"
#     }

#     r = requests.post(url, json = newComment)  # Add it to database
#     print(r.text)  # Get success or error message

# def getCommentSummary(id):
#     '''Get JSON object summary from a given comment id
    
#     Args:
#         id: Firestone comment id
#     '''
#     url = 'http://localhost:5000/comentario/' + str(id)

#     r = requests.get(url)
#     print(r.text)



# def createChaza():
#     ''' Create new chaza in database with dummy data'''

#     # Flask view URL
#     url = "http://127.0.0.1:5000/comentario/getCommentSummary/00e985c559724472be71d415b78b252b"

#     # JSON object to be added
#     newChaza = {
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
#     "reportes": ["rep1"], }

#     r = requests.post(url, json = newChaza)  # Add it to database
#     print(r.text)  # Get success or error message
    

# def createReport():
#     ''' Create new comment in database with dummy data'''

#      # Flask view URL
#     url = "http://localhost:5000/reporte/add"

#     # JSON object to be added
#     newReport = {
#         "contenido": "La comida es peligrosa y dudosa",
#         "fecha": "nov 1 2021",
#         "estado_resuelto": "false"
#     }

#     r = requests.post(url, json = newReport)  # Add it to database
#     print(r.text)  # Get success or error message


# def getReportSummary(id):
#     '''Get JSON object summary from a given report id
    
#     Args:
#         id: Firestone comment id
#     '''
#     url = 'http://localhost:5000/reporte/' + str(id)

#     r = requests.get(url)
#     print(r.text)


# def resolveReport(id):
#     '''Resolve a given report
    
#     Args:
#         id: Firestone report id
#     '''

#     # Flask view URL
#     url = "http://localhost:5000/reporte/resolve/" + str(id)

#     r = requests.post(url)  # Modify database
#     print(r.text)  # Get success or error message


# def getAllUnresolvedReports():
#     '''Gets all the unresolved reports in JSON format'''

#     # Flask view URL
#     url = "http://localhost:5000/reporte/getUnresolvedReports"
#     r = requests.get(url)
#     print(r.text)


# '''Code execution section'''
# createReport()
# getAllUnresolvedReports()
# def getCommentsByChazaID(id):
#     '''Get all comments related to a Chaza

#     Comments have a 'chazaID' attribute and this function filters by this field.
    
#     Args:
#         id: Given firestone chaza unique id
#     '''
#     # Flask view URL
#     url = "http://localhost:5000/chaza/getChazaComments/" + str(id)
#     print(url)
#     r = requests.get(url)
#     print(r.text)


# '''Code execution section'''
# getCommentsByChazaID("2c3318cdb84148eba49b9239b7ed6102")
