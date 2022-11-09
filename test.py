import requests

def createComment():
    ''' Create new comment in database with dummy data'''

    # Flask view URL
    url = "http://localhost:5000/comentario/add"

    # JSON object to be added
    newComment = {
        "usuario": "idUsuario",
        "fecha": "nov 10 2020",
        "estrellas": "3",
        "upvotes": "1",
        "chazaId": "23131"
    }

    r = requests.post(url, json = newComment)  # Add it to database
    print(r.text)  # Get success or error message

def getCommentSummary(id):
    '''Get JSON object summary from a given comment id
    
    Args:
        id: Firestone comment id
    '''
    url = 'http://localhost:5000/comentario/' + str(id)

    r = requests.get(url)
    print(r.text)



def createChaza():
    ''' Create new chaza in database with dummy data'''

    # Flask view URL
    url = "http://127.0.0.1:5000/comentario/getCommentSummary/00e985c559724472be71d415b78b252b"

    # JSON object to be added
    newChaza = {
    "nombre": "Chaza5",
    "categorias": ["Vivero"],
    "ubicacion": "Perola",
    "descripcion": "",
    "urlImagen": "urltest4.com",
    "telefono": 13548,
    "horario": "13:00 - 18:00",
    "propietario": "idPropietario4" ,
    "comentarios": ["com1"],
    "calificacion": 4,
    "urlFotoChaza": "urlFoto3",
    "reportes": ["rep1"], }

    r = requests.post(url, json = newChaza)  # Add it to database
    print(r.text)  # Get success or error message
    


'''Code execution section'''
getCommentSummary('33aefc97261c483b81fb405a3a0ea611')